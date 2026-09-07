import json
from pathlib import Path
from core.formatter import format_header, format_table
from core.menu import display_menu
from utils.parser import load_periodic_table, load_constants

DATA_DIR = Path(__file__).parent.parent / "data"

def load_reference_data() -> dict:
    with open(DATA_DIR / "reference.json", "r", encoding="utf-8") as f:
        return json.load(f)

def run_chemistry_reference() -> None:
    from core import theme_manager
    ref_data = load_reference_data()
    
    while True:
        options = [
            ("1", "Periodic Table Lookup"),
            ("2", "Polyatomic Ions"),
            ("3", "Solubility Rules"),
            ("4", "Strong Acids & Bases"),
            ("5", "SI Prefixes"),
            ("6", "Physical & Chemical Constants"),
            ("0", "Return to Main Menu")
        ]
        choice = display_menu("CHEMISTRY REFERENCE DATA", options)
        
        if choice == "1":
            _lookup_element()
        elif choice == "2":
            _display_polyatomic_ions(ref_data.get("polyatomic_ions", []))
        elif choice == "3":
            _display_solubility_rules(ref_data.get("solubility_rules", []))
        elif choice == "4":
            _display_acids_bases(ref_data.get("strong_acids", []), ref_data.get("strong_bases", []))
        elif choice == "5":
            _display_si_prefixes(ref_data.get("si_prefixes", []))
        elif choice == "6":
            _display_constants()
        elif choice == "0":
            break
        else:
            print("\n" + theme_manager.error("[Error] Invalid choice."))

def _lookup_element() -> None:
    from core import navigation
    from chemistry.periodic_table import find_element, format_element_detail
    navigation.push("Periodic Table Lookup")
    try:
        print(format_header("PERIODIC TABLE LOOKUP"))
        query = input("Enter Element Symbol, Name, or Atomic Number: ").strip()
        if not query:
            input("\nPress ENTER to continue...")
            return

        res = find_element(query)
        if res:
            sym, data = res
            print("\n" + format_element_detail(sym, data))
        else:
            print(f"\n[Error] Element '{query}' not found in database.")
        input("\nPress ENTER to continue...")
    finally:
        navigation.pop()


def run_periodic_table_menu() -> None:
    """Launch interactive Periodic Table tool."""
    from chemistry.periodic_table import run_interactive_periodic_table
    run_interactive_periodic_table()

def _display_polyatomic_ions(ions: list) -> None:
    print(format_header("COMMON POLYATOMIC IONS"))
    headers = ["Name", "Formula", "Charge"]
    rows = [[item["name"], item["formula"], item["charge"]] for item in ions]
    print(format_table(headers, rows))
    input("\nPress ENTER to continue...")

def _display_solubility_rules(rules: list) -> None:
    print(format_header("SOLUBILITY RULES"))
    for idx, rule in enumerate(rules, 1):
        print(f"  {idx}. {rule}")
    input("\nPress ENTER to continue...")

def _display_acids_bases(acids: list, bases: list) -> None:
    print(format_header("STRONG ACIDS & BASES"))
    print("--- STRONG ACIDS ---")
    headers = ["Name", "Formula"]
    rows_acids = [[item["name"], item["formula"]] for item in acids]
    print(format_table(headers, rows_acids))
    
    print("\n--- STRONG BASES ---")
    rows_bases = [[item["name"], item["formula"]] for item in bases]
    print(format_table(headers, rows_bases))
    input("\nPress ENTER to continue...")

def _display_si_prefixes(prefixes: list) -> None:
    print(format_header("SI PREFIXES"))
    headers = ["Prefix", "Symbol", "Factor"]
    rows = [[p["prefix"], p["symbol"], p["factor"]] for p in prefixes]
    print(format_table(headers, rows))
    input("\nPress ENTER to continue...")

def _display_constants() -> None:
    print(format_header("PHYSICAL & CHEMICAL CONSTANTS"))
    constants = load_constants()
    print(f"  Avogadro's Number (N_A) : {constants['avogadro_number']:.7e} mol^-1")
    print(f"  Molar Volume at STP    : {constants['molar_volume_stp_L_per_mol']} L/mol")
    print(f"  Standard Temperature   : {constants['standard_temp_K']} K (0 °C)")
    print(f"  Standard Pressure      : {constants['standard_pressure_atm']} atm = {constants['standard_pressure_mmHg']} mmHg = {constants['standard_pressure_kPa']} kPa")
    print(f"  Ideal Gas Constant (R) :")
    print(f"    - {constants['R_gas_constant']['L_atm_per_mol_K']} L·atm/(mol·K)")
    print(f"    - {constants['R_gas_constant']['J_per_mol_K']} J/(mol·K)")
    print(f"    - {constants['R_gas_constant']['L_mmHg_per_mol_K']} L·mmHg/(mol·K)")
    input("\nPress ENTER to continue...")
