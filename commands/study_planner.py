"""Study planner command using the shared Ollama client."""

from commands.common_ai import build_client, get_reasoning_level
from services.ollama_client import OllamaClientError
from services.ollama_prompts import study_planner_prompt


def run_study_planner() -> None:
    """Generate a study plan for a goal or exam. Try to make the best plan you can, since this CLI is not a chat interface. Check your plan BEFORE submitting."""
    goal = input("Study goal: ").strip()
    if not goal:
        print("\n[Error] Goal cannot be empty.")
        return
    client = build_client()
    reasoning = get_reasoning_level()
    try:
        response = client.generate(study_planner_prompt(goal, reasoning), reasoning_level=reasoning)
        print(f"\n{response.content}")
    except OllamaClientError as exc:
        print(f"\n[Error] {exc}")
    input("\nPress ENTER to return to menu...")
