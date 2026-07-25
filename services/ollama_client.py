"""Reusable Ollama API client used by every AI command."""

import json
import socket
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


@dataclass
class OllamaConnectivityResult:
    """User-facing diagnostics for an Ollama connectivity check."""

    ok: bool
    endpoint: str
    message: str
    models: list[str] = field(default_factory=list)
    version: Optional[str] = None


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


    def check_connectivity(self) -> OllamaConnectivityResult:
        """Verify that Ollama is reachable and that its API responds correctly."""
        api_attempts: list[str] = []
        version: Optional[str] = None

        for path in ("/version", "/tags"):
            try:
                data = self._get(path)
                if path == "/version":
                    version = str(data.get("version", "")) or None
                    continue
                models = [item.get("name", "") for item in data.get("models", []) if item.get("name")]
                summary = "Ollama API is reachable."
                if models:
                    summary += f" Found {len(models)} installed model(s)."
                else:
                    summary += " No installed models were reported."
                return OllamaConnectivityResult(True, self.base_url, summary, models, version)
            except OllamaClientError as exc:
                api_attempts.append(f"{self.base_url}{path}: {exc}")

        root_url = self._server_root_url()
        try:
            root_text = self._get_text(root_url)
        except OllamaClientError as exc:
            message = (
                "Could not reach Ollama. Confirm the Ollama app/service is running and that the "
                f"configured endpoint is correct. Tried API endpoint {self.base_url}. Details: {exc}"
            )
            return OllamaConnectivityResult(False, self.base_url, message)

        message = (
            "Ollama responded on the server port, but the configured API endpoint did not return "
            "valid Ollama API data. This usually means the endpoint should be "
            f"{root_url.rstrip('/')}/api or another process is answering on that port. "
            f"Server response preview: {root_text[:120]!r}. API attempts: {'; '.join(api_attempts)}"
        )
        return OllamaConnectivityResult(False, self.base_url, message)

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
        except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
            raise OllamaClientError(f"Unable to reach Ollama at {self.base_url}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise OllamaClientError(f"Ollama returned malformed JSON: {exc}") from exc

    def _get(self, path: str) -> dict[str, Any]:
        try:
            with urllib.request.urlopen(self.base_url + path, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
            raise OllamaClientError(f"Unable to reach Ollama at {self.base_url}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise OllamaClientError(f"Ollama returned malformed JSON: {exc}") from exc


    def _get_text(self, url: str) -> str:
        try:
            with urllib.request.urlopen(url, timeout=self.timeout) as response:
                return response.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
            raise OllamaClientError(f"Unable to reach {url}: {exc}") from exc

    def _server_root_url(self) -> str:
        if self.base_url.endswith("/api"):
            return self.base_url[:-4]
        return self.base_url

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
