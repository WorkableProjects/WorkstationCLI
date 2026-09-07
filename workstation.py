#!/usr/bin/env python3
"""
Workstation CLI — Entry Point
Education-first offline chemistry and AI CLI tool.
"""

import sys
import random

from core import theme_manager
from core.about import display_about
from core.banner import display_startup_animation
from core.ui import HorizontalTabMenu

# Import Chemistry tools
from calculators.concentration import run_concentration_calculator
from calculators.dilution import run_dilution_calculator
from calculators.gas_laws import run_gas_laws_calculator
from calculators.limiting_reagent import run_limiting_reagent_calculator
from calculators.molar_mass import run_molar_mass_calculator
from calculators.percent_yield import run_percent_yield_calculator
from calculators.reference import run_chemistry_reference
from calculators.stoichiometry import run_stoichiometry_calculator
from chemistry.periodic_table import run_interactive_periodic_table

# Import AI tools
from ai.menu import run_ai_chat, configure_ai_settings, edit_ai_config_file, test_ollama_connectivity, display_ai_settings

# Import Graphing tools
from graphing.menu import (
    run_custom_function_plot,
    run_multi_series_plot,
    run_derivative_plot,
    run_integral_plot,
    run_preset_functions_menu,
    run_plot_settings_menu,
    run_graph_help_menu
)

# Import Settings tools
from commands.settings import toggle_theme, toggle_startup_animation, get_animation_status, show_config_location


def main() -> None:
    """Launch the category-based Workstation CLI tabbed menu."""
    # Load and apply theme on startup
    theme_manager.apply_theme()
    
    display_startup_animation()

    tabs = [
        {
            "name": "Chemistry",
            "options": [
                ("Molar Mass Calculator", run_molar_mass_calculator),
                ("Gas Laws Calculator", run_gas_laws_calculator),
                ("Stoichiometry Calculator", run_stoichiometry_calculator),
                ("Limiting Reagent Calculator", run_limiting_reagent_calculator),
                ("Percent Yield Calculator", run_percent_yield_calculator),
                ("Chemistry Reference", run_chemistry_reference),
                ("Dilution Calculator", run_dilution_calculator),
                ("Concentration Calculator", run_concentration_calculator),
                ("Interactive Periodic Table", run_interactive_periodic_table),
            ]
        },
        {
            "name": "AI",
            "options": [
                ("AI Chat", run_ai_chat),
                (lambda: f"Configure AI Settings ({display_ai_settings()})", configure_ai_settings),
                ("Edit Local Config File", edit_ai_config_file),
                ("Test Ollama Connection", test_ollama_connectivity),
            ]
        },
        {
            "name": "Graphing",
            "options": [
                ("Plot Custom Function", run_custom_function_plot),
                ("Compare Multiple Functions", run_multi_series_plot),
                ("Numerical Derivative Plot", run_derivative_plot),
                ("Definite Integral Calculation", run_integral_plot),
                ("Preset Functions Library", run_preset_functions_menu),
                ("Plot Settings & Defaults", run_plot_settings_menu),
                ("Graph Help & Documentation", run_graph_help_menu),
            ]
        },
        {
            "name": "Settings",
            "options": [
                ("Change Appearance Theme", toggle_theme),
                (lambda: f"Toggle Startup Animation ({get_animation_status()})", toggle_startup_animation),
                ("AI & Model Configuration", configure_ai_settings),
                ("Graphing Defaults Configuration", run_plot_settings_menu),
                ("View Config File Location", show_config_location),
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
