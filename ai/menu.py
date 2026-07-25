"""Menu routing for AI-powered study commands."""

from core.menu import display_menu
from commands.ai_chat import run_ai_chat
from commands.essay_helper import run_essay_helper
from commands.quiz_generator import run_quiz_generator
from commands.socratic_tutor import run_socratic_tutor
from commands.study_planner import run_study_planner


def run_ai_menu() -> None:
    """Display the AI submenu and route to AI commands."""
    options = [
        ("1", "AI Chat"),
        ("2", "Quiz Generator"),
        ("3", "Study Planner"),
        ("4", "Essay Helper"),
        ("5", "Socratic Tutor"),
        ("0", "Return to Main Menu"),
    ]
    handlers = {
        "1": run_ai_chat,
        "2": run_quiz_generator,
        "3": run_study_planner,
        "4": run_essay_helper,
        "5": run_socratic_tutor,
    }
    while True:
        choice = display_menu("AI", options)
        if choice == "0":
            return
        handler = handlers.get(choice)
        if handler is None:
            print("\n[Error] Invalid selection. Please choose an option from the menu.")
            continue
        handler()
