"""Essay helper command using the shared Ollama client."""

from commands.common_ai import build_client, choose_reasoning_level
from services.ollama_client import OllamaClientError
from services.ollama_prompts import essay_helper_prompt


def run_essay_helper() -> None:
    """Help outline an essay for a requested topic."""
    topic = input("Essay topic: ").strip()
    if not topic:
        print("\n[Error] Topic cannot be empty.")
        return
    client = build_client()
    reasoning = choose_reasoning_level()
    try:
        response = client.generate(essay_helper_prompt(topic, reasoning), reasoning_level=reasoning)
        print(f"\n{response.content}")
    except OllamaClientError as exc:
        print(f"\n[Error] {exc}")
    input("\nPress ENTER to return to menu...")
