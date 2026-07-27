#!/usr/bin/env python3
"""
Workstation CLI — Entry Point
Education-first offline chemistry and AI CLI tool.
"""

import sys
import random

from core import theme_manager
from ai.menu import run_ai_menu
from chemistry.menu import run_chemistry_menu
from core.about import display_about
from core.banner import display_banner
from core.menu import display_menu
from commands.settings import run_settings_menu


def main() -> None:
    """Launch the category-based Workstation CLI menu."""
    # Load and apply theme on startup
    theme_manager.apply_theme()
    
    display_banner()
    main_options = [
        ("1", "Chemistry"),
        ("2", "AI"),
        ("3", "Settings"),
        ("4", "CLI Information"),
        ("0", "Exit"),
    ]
    handlers = {
        "1": run_chemistry_menu,
        "2": run_ai_menu,
        "3": run_settings_menu,
        "4": display_about
    }

    while True:
        choice = display_menu("WORKSTATION CLI", main_options)
        if choice == "0":
            exit_messages = [
                "Thanks for using Workstation CLI — see you next time!",
                "Take care! Hope Workstation CLI helped your studies.",
                "Goodbye! Keep experimenting safely in the lab."
            ]
            print("\n" + random.choice(exit_messages))
            sys.exit(0)
        handler = handlers.get(choice)
        if handler is None:
            print("\n[Error] Invalid selection. Please choose an option from the menu.")
            continue
        handler()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit_messages = [
            "Interrupted — session ended. Stay curious!",
            "Session closed. See you again soon!",
            "Take care! Exiting Workstation CLI."
        ]
        print("\n\n" + random.choice(exit_messages))
        sys.exit(0)
