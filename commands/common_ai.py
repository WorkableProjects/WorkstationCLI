"""Shared helpers and settings for AI command modules."""

from dataclasses import dataclass
from typing import Any, Optional

from services.config import CONFIG_FILE, DEFAULT_MODEL, load_config, open_config_in_editor, save_config
from services.ollama_client import OllamaClient
from services.ollama_prompts import ReasoningLevel


@dataclass
class AISettings:
    """Runtime AI settings shared by AI commands during a CLI session."""

    model: str = DEFAULT_MODEL
    base_url: str = "http://localhost:11434/api"
    timeout: float = 60.0
    reasoning_level: ReasoningLevel = ReasoningLevel.MEDIUM


settings = AISettings()


def _coerce_reasoning_level(value: Any) -> ReasoningLevel:
    """Return a valid reasoning level from config or fallback to Medium."""
    for level in ReasoningLevel:
        if value == level.value:
            return level
    return ReasoningLevel.MEDIUM


def load_ai_settings() -> None:
    """Load AI settings from the local configuration file."""
    ai_config = load_config().get("ai", {})
    settings.model = str(ai_config.get("model", DEFAULT_MODEL))
    settings.base_url = str(ai_config.get("base_url", settings.base_url)).rstrip("/")
    try:
        settings.timeout = float(ai_config.get("timeout", settings.timeout))
    except (TypeError, ValueError):
        settings.timeout = 60.0
    settings.reasoning_level = _coerce_reasoning_level(ai_config.get("reasoning_level"))


def save_ai_settings() -> None:
    """Persist current AI settings to the local configuration file."""
    save_config(
        {
            "ai": {
                "model": settings.model,
                "base_url": settings.base_url,
                "timeout": settings.timeout,
                "reasoning_level": settings.reasoning_level.value,
            }
        }
    )


load_ai_settings()


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
    print(f"Config file     : {CONFIG_FILE}")
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
    # Persist AI settings along with appearance preference
    # Merge into existing config to avoid overwriting unrelated keys
    from services.config import load_config, save_config
    cfg = load_config()
    cfg["ai"] = {
        "model": settings.model,
        "base_url": settings.base_url,
        "timeout": settings.timeout,
        "reasoning_level": settings.reasoning_level.value,
    }
    # Ask for theme preference (light/dark)
    appearance = cfg.get("appearance", {})
    current_theme = appearance.get("theme", "dark")
    theme_choice = input(f"Appearance theme (light/dark) [{current_theme}]: ").strip().lower() or current_theme
    if theme_choice not in ("light", "dark"):
        print("\n[Warning] Invalid theme. Keeping previous value.")
        theme_choice = current_theme
    cfg["appearance"] = {"theme": theme_choice}
    save_config(cfg)
    print(f"\nSettings saved to {CONFIG_FILE}.")
    input("\nPress ENTER to return to menu...")


def edit_ai_config_file() -> None:
    """Open the local configuration file in an editor, then reload settings."""
    print(f"\nLocal config file: {CONFIG_FILE}")
    if open_config_in_editor():
        load_ai_settings()
        print("\nAI settings reloaded from config file.")
    else:
        print("\nNo EDITOR/VISUAL environment variable is set, so the file was not opened automatically.")
        print(f"Edit this file manually, then restart or reopen this menu: {CONFIG_FILE}")
    input("\nPress ENTER to return to menu...")


def display_ai_settings() -> str:
    """Return a short settings summary for menu display."""
    return f"Model: {settings.model} | Reasoning: {settings.reasoning_level.value}"


def test_ollama_connectivity() -> None:
    """Run an Ollama connectivity check and print actionable diagnostics."""
    client = build_client()
    print("\nChecking Ollama connectivity...")
    result = client.check_connectivity()
    status = "OK" if result.ok else "FAILED"
    print(f"\nOllama connectivity: {status}")
    print(f"Endpoint: {result.endpoint}")
    if result.version:
        print(f"Version: {result.version}")
    print(result.message)
    if result.models:
        print("\nInstalled models:")
        for model in result.models:
            print(f"  - {model}")
    elif result.ok:
        print("\nNo installed models were found. Install one with the Ollama app or `ollama pull <model>`.")
    else:
        print("\nTroubleshooting:")
        print("  - If the Ollama desktop app is installed, open it; you do not need `ollama serve`.")
        print("  - Verify Settings points to http://localhost:11434/api unless you changed Ollama's host.")
        print("  - If another process is using port 11434, change the endpoint or stop that process.")
    input("\nPress ENTER to return to menu...")
