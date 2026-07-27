from utils.parser import parse_chemical_formula, load_periodic_table
from core.formatter import format_header, format_table
from core.console import preserve_output
from core import history, navigation
from core import exporter


def run_molar_mass_calculator() -> None:
    navigation.push("Molar Mass")
    try:
        print(format_header("MOLAR MASS CALCULATOR"))
        print("Enter a chemical formula (e.g. H2O, Ca(OH)2, Al2(SO4)3, CuSO4·5H2O)")
        formula_input = input("\nFormula: ").strip()

        if not formula_input:
            print("\n[Error] Formula cannot be empty.")
            input("\nPress ENTER to return...")
            return

        # Support history re-run shortcut like !1
        if formula_input.startswith("!") and formula_input[1:].isdigit():
            idx = int(formula_input[1:])
            prev = history.get_recent(idx)
            if prev and prev.get("type") == "molar_mass":
                formula_input = prev["params"]["formula"]
                print(f"Re-running previous molar mass for: {formula_input}")
            else:
                print(f"\n[Error] No molar mass history entry #{idx}.")
                input("\nPress ENTER to continue...")
                return

        try:
            element_counts = parse_chemical_formula(formula_input)
            periodic_table = load_periodic_table()

            headers = ["Element", "Symbol", "Count", "Atomic Mass (g/mol)", "Subtotal (g/mol)", "Mass %"]
            rows = []
            total_molar_mass = 0.0

            subtotals = {}
            for symbol, count in element_counts.items():
                elem_data = periodic_table[symbol]
                mass = elem_data["mass"]
                subtotal = mass * count
                subtotals[symbol] = subtotal
                total_molar_mass += subtotal

            for symbol, count in element_counts.items():
                elem_data = periodic_table[symbol]
                name = elem_data["name"]
                mass = elem_data["mass"]
                subtotal = subtotals[symbol]
                percent = (subtotal / total_molar_mass) * 100.0 if total_molar_mass > 0 else 0.0
                
                rows.append([
                    name,
                    symbol,
                    count,
                    f"{mass:.4f}",
                    f"{subtotal:.4f}",
                    f"{percent:.2f}%"
                ])

            out_lines = []
            out_lines.append("Breakdown:")
            out_lines.append(format_table(headers, rows))
            out_lines.append("-" * 50)
            out_lines.append(f"Total Molar Mass of {formula_input}: {total_molar_mass:.4f} g/mol")
            out_lines.append("-" * 50)

            result_text = '\n'.join(out_lines)
            preserve_output(result_text)

            # Save to history
            history.add({"type": "molar_mass", "params": {"formula": formula_input}, "result": result_text})

            # Offer export
            save_choice = input("\nSave result to file? (y/N): ").strip().lower()
            if save_choice == "y":
                path = exporter.save_text(result_text, prefix="molar_mass")
                print(f"Saved to: {path}")
            else:
                # Try clipboard copy if requested
                copy_choice = input("Copy result to clipboard? (y/N): ").strip().lower()
                if copy_choice == "y":
                    ok = exporter.copy_to_clipboard(result_text)
                    if ok:
                        print("Copied to clipboard.")
                    else:
                        print("\n[Info] Clipboard not available. Install 'pyperclip' to enable this feature.")

        except Exception as e:
            preserve_output(f"\n[Error] Failed to calculate molar mass: {e}")

        input("\nPress ENTER to return to menu...")
    finally:
        navigation.pop()
