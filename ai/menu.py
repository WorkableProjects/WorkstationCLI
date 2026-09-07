"""Menu routing for AI-powered study commands."""

from core.menu import display_menu
from commands.common_ai import configure_ai_settings, display_ai_settings, edit_ai_config_file, test_ollama_connectivity
from commands.ai_chat import run_ai_chat
from core import navigation

def run_ai_menu() -> None:
    """Display the AI submenu and route to AI commands."""
    from core import theme_manager
    navigation.push("AI")
    try:
        handlers = {
            "1": run_ai_chat,
            "2": configure_ai_settings,
            "3": edit_ai_config_file,
            "4": test_ollama_connectivity,
        }
        while True:
            options = [
                ("1", "AI Chat"),
                ("2", f"Settings ({display_ai_settings()})"),
                ("3", "Edit Local Config File"),
                ("4", "Test Ollama Connection"),
                ("0", "Return to Main Menu"),
            ]
            choice = display_menu("AI", options)
            if choice == "0":
                return
            handler = handlers.get(choice)
            if handler is None:
                print("\n" + theme_manager.error("[Error] Invalid selection. Please choose an option from the menu."))
                continue
            handler()
    finally:
        navigation.pop()
