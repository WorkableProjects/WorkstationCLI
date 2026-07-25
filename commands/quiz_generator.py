"""Quiz generator command using the shared Ollama client."""

from commands.common_ai import build_client, get_reasoning_level
from services.ollama_client import OllamaClientError
from services.ollama_prompts import quiz_generator_prompt


def run_quiz_generator() -> None:
    """Generate a study quiz for a requested topic."""
    topic = input("Quiz topic: ").strip()
    if not topic:
        print("\n[Error] Topic cannot be empty.")
        return
    client = build_client()
    reasoning = get_reasoning_level()
    prompt = quiz_generator_prompt(topic, reasoning)
    try:
        response = client.generate(prompt, reasoning_level=reasoning)
        print(f"\n{response.content}")
    except OllamaClientError as exc:
        print(f"\n[Error] {exc}")
    input("\nPress ENTER to return to menu...")
