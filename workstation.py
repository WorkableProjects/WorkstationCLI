#!/usr/bin/env python3
"""
Workstation CLI — Entry Point
Education-first offline chemistry and AI CLI tool.
"""

import sys

from ai.menu import run_ai_menu
from chemistry.menu import run_chemistry_menu
from core.about import display_about
from core.banner import display_banner
from core.menu import display_menu


def main() -> None:
    """Launch the category-based Workstation CLI menu."""
    display_banner()
    main_options = [
        ("1", "Chemistry"),
        ("2", "AI"),
        ("3", "CLI Information"),
        ("0", "Exit"),
    ]
    handlers = {"1": run_chemistry_menu, "2": run_ai_menu, "3": display_about}

    while True:
        choice = display_menu("WORKSTATION CLI", main_options)
        if choice == "0":
            print("\nThank you for using Workstation CLI! Goodbye.")
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
        print("\n\nExiting Workstation CLI...")
        print("Goodbye!")
        sys.exit(0)
