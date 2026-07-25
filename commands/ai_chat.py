"""Interactive AI chat mode backed by the shared Ollama client."""

from commands.common_ai import build_client, get_reasoning_level
from services.ollama_client import OllamaClientError
from services.ollama_prompts import ai_chat_prompt


def run_ai_chat() -> None:
    """Run a continuous conversation until the user exits."""
    client = build_client()
    reasoning = get_reasoning_level()
    messages = [{"role": "system", "content": ai_chat_prompt(reasoning)}]
    print("\nAI Chat started. Type /clear to reset history or /exit to return.\n")
    while True:
        user_message = input("You: ").strip()
        if user_message.lower() in {"/exit", "exit", "quit"}:
            return
        if user_message.lower() == "/clear":
            messages = [{"role": "system", "content": ai_chat_prompt(reasoning)}]
            print("\nChat history cleared.\n")
            continue
        if not user_message:
            continue
        messages.append({"role": "user", "content": user_message})
        try:
            response = client.chat(messages, reasoning_level=reasoning)
        except OllamaClientError as exc:
            print(f"\n[Error] {exc}\n")
            messages.pop()
            continue
        messages.append({"role": "assistant", "content": response.content})
        print(f"\nAI: {response.content}\n")
