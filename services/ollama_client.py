"""Reusable Ollama API client used by every AI command."""

import json
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Optional

from services.ollama_prompts import ReasoningLevel


@dataclass
class OllamaResponse:
    """Normalized Ollama response data."""

    content: str
    raw: dict[str, Any] = field(default_factory=dict)


class OllamaClientError(RuntimeError):
    """Raised when Ollama cannot complete a request cleanly."""


class OllamaClient:
    """Small dependency-free client for Ollama's local HTTP API."""

    def __init__(self, base_url: str = "http://localhost:11434/api", model: str = "llama3.2", timeout: float = 60.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def chat(
        self,
        messages: list[dict[str, str]],
        reasoning_level: ReasoningLevel = ReasoningLevel.MEDIUM,
        stream: bool = False,
        json_schema: Optional[dict[str, Any]] = None,
    ) -> OllamaResponse:
        """Send a chat request through Ollama and return normalized response text."""
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": self._reasoning_options(reasoning_level),
        }
        if json_schema is not None:
            payload["format"] = "json"
        data = self._post("/chat", payload)
        content = data.get("message", {}).get("content", "")
        return OllamaResponse(content=content, raw=data)

    def generate(self, prompt: str, reasoning_level: ReasoningLevel = ReasoningLevel.MEDIUM, json_output: bool = False) -> OllamaResponse:
        """Generate a single response from a prompt."""
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": self._reasoning_options(reasoning_level),
        }
        if json_output:
            payload["format"] = "json"
        data = self._post("/generate", payload)
        return OllamaResponse(content=data.get("response", ""), raw=data)

    def parse_json(self, response: OllamaResponse) -> dict[str, Any]:
        """Parse a structured JSON response with clear error reporting."""
        try:
            parsed = json.loads(response.content)
        except json.JSONDecodeError as exc:
            raise OllamaClientError(f"Ollama returned invalid JSON: {exc}") from exc
        if not isinstance(parsed, dict):
            raise OllamaClientError("Ollama JSON output must be an object.")
        return parsed

    def list_models(self) -> list[str]:
        """Return installed model names, or an empty list if Ollama is unavailable."""
        try:
            data = self._get("/tags")
        except OllamaClientError:
            return []
        return [item.get("name", "") for item in data.get("models", []) if item.get("name")]

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.base_url + path,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError) as exc:
            raise OllamaClientError(f"Unable to reach Ollama at {self.base_url}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise OllamaClientError(f"Ollama returned malformed JSON: {exc}") from exc

    def _get(self, path: str) -> dict[str, Any]:
        try:
            with urllib.request.urlopen(self.base_url + path, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError) as exc:
            raise OllamaClientError(f"Unable to reach Ollama at {self.base_url}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise OllamaClientError(f"Ollama returned malformed JSON: {exc}") from exc

    def _reasoning_options(self, reasoning_level: ReasoningLevel) -> dict[str, Any]:
        """Return native reasoning controls only for models that advertise thinking support."""
        if not self._model_supports_native_reasoning():
            return {}
        effort = {
            ReasoningLevel.MINIMAL: "minimal",
            ReasoningLevel.LOW: "low",
            ReasoningLevel.MEDIUM: "medium",
            ReasoningLevel.MAX: "high",
        }[reasoning_level]
        return {"reasoning_effort": effort}

    def _model_supports_native_reasoning(self) -> bool:
        """Best-effort detection for Ollama models with native thinking controls."""
        lowered = self.model.lower()
        known_reasoning_families = ("deepseek-r1", "qwen3", "gpt-oss")
        return any(name in lowered for name in known_reasoning_families)
