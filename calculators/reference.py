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
    navigation.push("Periodic Table Lookup")
    try:
        print(format_header("PERIODIC TABLE LOOKUP"))
        query = input("Enter Element Symbol, Name, or Atomic Number: ").strip()
        if not query:
            input("\nPress ENTER to continue...")
            return
        
        pt = load_periodic_table()
        found = None
        
        for symbol, data in pt.items():
            if (query.lower() == symbol.lower() or 
                query.lower() == data["name"].lower() or 
                (query.isdigit() and int(query) == data["number"])):
                found = (symbol, data)
                break

        if found:
            sym, data = found
            print(f"\n" + "=" * 40)
            print(f"  Element       : {data['name']} ({sym})")
            print(f"  Atomic Number : {data['number']}")
            print(f"  Atomic Mass   : {data['mass']} g/mol")
            print(f"  Category      : {data['category'].title()}")
            print("=" * 40)
        else:
            print(f"\n[Error] Element '{query}' not found in database.")
        input("\nPress ENTER to continue...")
    finally:
        navigation.pop()


def run_periodic_table_menu() -> None:
    """Interactive periodic table viewer: paginated, searchable, and detail view."""
    from core import navigation
    navigation.push("Periodic Table")
    try:
        pt = load_periodic_table()
        elements = sorted(pt.items(), key=lambda kv: kv[1]["number"])
        per_page = 20
        page = 0
        while True:
            start = page * per_page
            chunk = elements[start:start + per_page]
            print(format_header(f"PERIODIC TABLE (Page {page+1})"))
            headers = ["#", "Symbol", "Name", "Mass", "Category"]
            rows = [[str(data["number"]), sym, data["name"], str(data["mass"]), data.get("category", "")] for sym, data in chunk]
            print(format_table(headers, rows))
            print("Commands: [n]ext page, [p]rev page, [s]earch, [v]<symbol/number> view, [q]uit")
            cmd = input("Enter command: ").strip()
            if not cmd:
                continue
            if cmd.lower() == "q":
                break
            if cmd.lower() == "n":
                if start + per_page < len(elements):
                    page += 1
                else:
                    print("\n[Info] Last page.")
                continue
            if cmd.lower() == "p":
                if page > 0:
                    page -= 1
                else:
                    print("\n[Info] First page.")
                continue
            if cmd.lower().startswith("v"):
                target = cmd[1:].strip()
                if not target:
                    print("\n[Error] Provide a symbol or atomic number after 'v'.")
                    continue
                # reuse lookup logic
                found = None
                for sym, data in elements:
                    if (target.lower() == sym.lower() or target.isdigit() and int(target) == data["number"] or target.lower() == data["name"].lower()):
                        found = (sym, data)
                        break
                if found:
                    sym, data = found
                    print("\n" + "=" * 40)
                    print(f"  Element       : {data['name']} ({sym})")
                    print(f"  Atomic Number : {data['number']}")
                    print(f"  Atomic Mass   : {data['mass']} g/mol")
                    print(f"  Category      : {data['category'].title()}")
                    print("=" * 40)
                else:
                    print(f"\n[Error] Element '{target}' not found.")
                input("\nPress ENTER to continue...")
                continue
            if cmd.lower() == "s":
                q = input("Search by name, symbol, or number: ").strip()
                if not q:
                    continue
                matches = []
                for sym, data in elements:
                    if q.lower() in sym.lower() or q.lower() in data["name"].lower() or (q.isdigit() and int(q) == data["number"]):
                        matches.append((sym, data))
                if not matches:
                    print(f"\n[Info] No matches for '{q}'.")
                    input("\nPress ENTER to continue...")
                    continue
                # show short list
                headers = ["#", "Symbol", "Name", "Mass"]
                rows = [[str(d["number"]), s, d["name"], str(d["mass"])] for s, d in matches]
                print(format_table(headers, rows))
                sel = input("Enter symbol or number to view (or ENTER to cancel): ").strip()
                if sel:
                    # display selected
                    found = None
                    for s, d in matches:
                        if sel.lower() == s.lower() or (sel.isdigit() and int(sel) == d["number"]) or sel.lower() == d["name"].lower():
                            found = (s, d)
                            break
                    if found:
                        s, d = found
                        print("\n" + "=" * 40)
                        print(f"  Element       : {d['name']} ({s})")
                        print(f"  Atomic Number : {d['number']}")
                        print(f"  Atomic Mass   : {d['mass']} g/mol")
                        print(f"  Category      : {d['category'].title()}")
                        print("=" * 40)
                    else:
                        print(f"\n[Error] Selection '{sel}' not found in results.")
                input("\nPress ENTER to continue...")
                continue
            print("\n[Error] Unknown command.")
        # end while
    finally:
        navigation.pop()

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
