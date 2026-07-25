"""Menu routing for AI-powered study commands."""

from core.menu import display_menu
from commands.common_ai import configure_ai_settings, display_ai_settings, edit_ai_config_file, test_ollama_connectivity
from commands.ai_chat import run_ai_chat
from commands.quiz_generator import run_quiz_generator
from commands.study_planner import run_study_planner


def run_ai_menu() -> None:
    """Display the AI submenu and route to AI commands."""
    handlers = {
        "1": run_ai_chat,
        "2": run_quiz_generator,
        "3": run_study_planner,
        "4": configure_ai_settings,
        "5": edit_ai_config_file,
        "6": test_ollama_connectivity,
    }
    while True:
        options = [
            ("1", "AI Chat"),
            ("2", "Quiz Generator"),
            ("3", "Study Planner"),
            ("4", f"Settings ({display_ai_settings()})"),
            ("5", "Edit Local Config File"),
            ("6", "Test Ollama Connection"),
            ("0", "Return to Main Menu"),
        ]
        choice = display_menu("AI", options)
        if choice == "0":
            return
        handler = handlers.get(choice)
        if handler is None:
            print("\n[Error] Invalid selection. Please choose an option from the menu.")
            continue
        handler()
