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
from graphing.menu import run_graphing_menu
from core.about import display_about
from core.banner import display_startup_animation
from commands.settings import run_settings_menu
from core.ui import HorizontalTabMenu


def main() -> None:
    """Launch the category-based Workstation CLI tabbed menu."""
    # Load and apply theme on startup
    theme_manager.apply_theme()
    
    display_startup_animation()

    tabs = [
        {
            "name": "Chemistry",
            "options": [
                ("Open Chemistry Menu", run_chemistry_menu),
            ]
        },
        {
            "name": "AI",
            "options": [
                ("Open AI Menu", run_ai_menu),
            ]
        },
        {
            "name": "Graphing",
            "options": [
                ("Open Graphing Menu", run_graphing_menu),
            ]
        },
        {
            "name": "Settings",
            "options": [
                ("Open Settings Menu", run_settings_menu),
            ]
        },
        {
            "name": "About",
            "options": [
                ("View CLI Information", display_about),
            ]
        }
    ]

    menu = HorizontalTabMenu("WORKSTATION CLI", tabs)
    menu.run()

    exit_messages = [
        "Thanks for using Workstation CLI — see you next time!",
        "Take care! Hope Workstation CLI helped your studies.",
        "Goodbye! Keep experimenting safely in the lab."
    ]
    print("\n" + random.choice(exit_messages))
    sys.exit(0)


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
