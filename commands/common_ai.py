"""Shared helpers for AI command modules."""

from services.ollama_client import OllamaClient
from services.ollama_prompts import ReasoningLevel


def choose_reasoning_level() -> ReasoningLevel:
    """Prompt for a universal reasoning mode."""
    options = list(ReasoningLevel)
    print("\nReasoning Modes:")
    for index, level in enumerate(options, start=1):
        print(f"  {index}. {level.value}")
    choice = input("Select reasoning mode [3]: ").strip() or "3"
    try:
        return options[int(choice) - 1]
    except (ValueError, IndexError):
        print("\n[Warning] Invalid reasoning mode. Using Medium.")
        return ReasoningLevel.MEDIUM


def build_client() -> OllamaClient:
    """Create an Ollama client from CLI input with sensible defaults."""
    model = input("Ollama model [llama3.2]: ").strip() or "llama3.2"
    return OllamaClient(model=model)
