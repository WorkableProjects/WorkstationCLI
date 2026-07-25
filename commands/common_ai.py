"""Shared helpers and settings for AI command modules."""

from dataclasses import dataclass
from typing import Optional

from services.ollama_client import OllamaClient
from services.ollama_prompts import ReasoningLevel


@dataclass
class AISettings:
    """Runtime AI settings shared by AI commands during a CLI session."""

    model: str = "llama3.2"
    base_url: str = "http://localhost:11434/api"
    timeout: float = 60.0
    reasoning_level: ReasoningLevel = ReasoningLevel.MEDIUM


settings = AISettings()


def choose_reasoning_level(default: Optional[ReasoningLevel] = None) -> ReasoningLevel:
    """Prompt for a universal reasoning mode."""
    options = list(ReasoningLevel)
    current = default or settings.reasoning_level
    default_index = options.index(current) + 1
    print("\nReasoning Modes:")
    for index, level in enumerate(options, start=1):
        marker = " (current)" if level == current else ""
        print(f"  {index}. {level.value}{marker}")
    choice = input(f"Select reasoning mode [{default_index}]: ").strip() or str(default_index)
    try:
        return options[int(choice) - 1]
    except (ValueError, IndexError):
        print(f"\n[Warning] Invalid reasoning mode. Using {current.value}.")
        return current


def build_client() -> OllamaClient:
    """Create an Ollama client from the current AI settings."""
    return OllamaClient(base_url=settings.base_url, model=settings.model, timeout=settings.timeout)


def get_reasoning_level() -> ReasoningLevel:
    """Return the currently configured universal reasoning level."""
    return settings.reasoning_level


def configure_ai_settings() -> None:
    """Configure model, Ollama endpoint, timeout, and reasoning defaults."""
    print("\nAI Settings")
    print(f"Current model   : {settings.model}")
    print(f"Current endpoint: {settings.base_url}")
    print(f"Current timeout : {settings.timeout:g} seconds")
    print(f"Current reasoning: {settings.reasoning_level.value}")

    model = input(f"\nOllama model [{settings.model}]: ").strip()
    if model:
        settings.model = model

    base_url = input(f"Ollama API endpoint [{settings.base_url}]: ").strip()
    if base_url:
        settings.base_url = base_url.rstrip("/")

    timeout = input(f"Timeout seconds [{settings.timeout:g}]: ").strip()
    if timeout:
        try:
            parsed_timeout = float(timeout)
            if parsed_timeout <= 0:
                raise ValueError
            settings.timeout = parsed_timeout
        except ValueError:
            print("\n[Warning] Invalid timeout. Keeping previous value.")

    settings.reasoning_level = choose_reasoning_level(settings.reasoning_level)
    print("\nAI settings saved for this session.")
    input("\nPress ENTER to return to menu...")


def display_ai_settings() -> str:
    """Return a short settings summary for menu display."""
    return f"Model: {settings.model} | Reasoning: {settings.reasoning_level.value}"
