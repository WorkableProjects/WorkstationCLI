"""Category menu for chemistry calculators and reference tools."""

from core.menu import display_menu
from calculators.concentration import run_concentration_calculator
from calculators.dilution import run_dilution_calculator
from calculators.gas_laws import run_gas_laws_calculator
from calculators.limiting_reagent import run_limiting_reagent_calculator
from calculators.molar_mass import run_molar_mass_calculator
from calculators.percent_yield import run_percent_yield_calculator
from calculators.reference import run_chemistry_reference
from calculators.stoichiometry import run_stoichiometry_calculator


def run_chemistry_menu() -> None:
    """Display the chemistry submenu and route to existing chemistry commands."""
    options = [
        ("1", "Molar Mass"),
        ("2", "Gas Laws"),
        ("3", "Stoichiometry"),
        ("4", "Limiting Reagent"),
        ("5", "Percent Yield"),
        ("6", "Chemistry Reference"),
        ("7", "Dilution"),
        ("8", "Concentration"),
        ("0", "Return to Main Menu"),
    ]
    handlers = {
        "1": run_molar_mass_calculator,
        "2": run_gas_laws_calculator,
        "3": run_stoichiometry_calculator,
        "4": run_limiting_reagent_calculator,
        "5": run_percent_yield_calculator,
        "6": run_chemistry_reference,
        "7": run_dilution_calculator,
        "8": run_concentration_calculator,
    }

    while True:
        choice = display_menu("CHEMISTRY", options)
        if choice == "0":
            return
        handler = handlers.get(choice)
        if handler is None:
            print("\n[Error] Invalid selection. Please choose an option from the menu.")
            continue
        handler()
