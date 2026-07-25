"""Socratic tutor command using the shared Ollama client."""

from commands.common_ai import build_client, choose_reasoning_level
from services.ollama_client import OllamaClientError
from services.ollama_prompts import socratic_tutor_prompt


def run_socratic_tutor() -> None:
    """Start a short Socratic tutoring exchange."""
    topic = input("Tutoring topic: ").strip()
    if not topic:
        print("\n[Error] Topic cannot be empty.")
        return
    client = build_client()
    reasoning = choose_reasoning_level()
    try:
        response = client.generate(socratic_tutor_prompt(topic, reasoning), reasoning_level=reasoning)
        print(f"\n{response.content}")
    except OllamaClientError as exc:
        print(f"\n[Error] {exc}")
    input("\nPress ENTER to return to menu...")
