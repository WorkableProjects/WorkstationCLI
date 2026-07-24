#!/usr/bin/env python3
"""
Workstation CLI — Entry Point
Education-first offline chemistry CLI tool.
"""

import sys
from core.banner import display_banner
from core.menu import display_menu
from core.about import display_about
from core.loader import registry

# Import calculator modules to register handlers
from calculators.molar_mass import run_molar_mass_calculator
from calculators.gas_laws import run_gas_laws_calculator
from calculators.stoichiometry import run_stoichiometry_calculator
from calculators.limiting_reagent import run_limiting_reagent_calculator
from calculators.percent_yield import run_percent_yield_calculator
from calculators.reference import run_chemistry_reference

def register_modules() -> None:
    registry.register("1", run_molar_mass_calculator)
    registry.register("2", run_gas_laws_calculator)
    registry.register("3", run_stoichiometry_calculator)
    registry.register("4", run_limiting_reagent_calculator)
    registry.register("5", run_percent_yield_calculator)
    registry.register("6", run_chemistry_reference)
    registry.register("7", display_about)

def main() -> None:
    register_modules()
    display_banner()

    main_options = [
        ("1", "Molar Mass"),
        ("2", "Gas Laws"),
        ("3", "Stoichiometry"),
        ("4", "Limiting Reagent"),
        ("5", "Percent Yield"),
        ("6", "Chemistry Reference"),
        ("7", "CLI Information"),
        ("0", "Exit")
    ]

    while True:
        choice = display_menu("MAIN MENU", main_options)
        
        if choice == "0":
            print("\nThank you for using Workstation CLI! Goodbye.")
            sys.exit(0)
        
        executed = registry.execute(choice)
        if not executed:
            print("\n[Error] Invalid selection. Please choose an option from the menu.")

if __name__ == "__main__":
    main()
