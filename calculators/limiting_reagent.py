from core.formatter import format_header
from utils.parser import parse_chemical_formula, load_periodic_table
from utils.validation import validate_positive_float

def get_molar_mass(formula: str) -> float:
    periodic_table = load_periodic_table()
    counts = parse_chemical_formula(formula)
    return sum(periodic_table[elem]["mass"] * cnt for elem, cnt in counts.items())

def run_limiting_reagent_calculator() -> None:
    print(format_header("LIMITING REAGENT CALCULATOR"))
    try:
        r1_formula = input("Reagent 1 Formula (e.g. H2): ").strip()
        r1_coeff = validate_positive_float(input(f"Stoichiometric coefficient for {r1_formula}: ").strip(), "Coeff 1")
        r1_mass = validate_positive_float(input(f"Mass of {r1_formula} (g): ").strip(), f"Mass {r1_formula}")

        r2_formula = input("\nReagent 2 Formula (e.g. O2): ").strip()
        r2_coeff = validate_positive_float(input(f"Stoichiometric coefficient for {r2_formula}: ").strip(), "Coeff 2")
        r2_mass = validate_positive_float(input(f"Mass of {r2_formula} (g): ").strip(), f"Mass {r2_formula}")

        prod_formula = input("\nTarget Product Formula (e.g. H2O): ").strip()
        prod_coeff = validate_positive_float(input(f"Stoichiometric coefficient for {prod_formula}: ").strip(), "Prod Coeff")

        mm_r1 = get_molar_mass(r1_formula)
        mm_r2 = get_molar_mass(r2_formula)
        mm_prod = get_molar_mass(prod_formula)

        moles_r1 = r1_mass / mm_r1
        moles_r2 = r2_mass / mm_r2

        # Reactions possible based on stoichiometry
        rxn_units_r1 = moles_r1 / r1_coeff
        rxn_units_r2 = moles_r2 / r2_coeff

        if rxn_units_r1 < rxn_units_r2:
            limiting = r1_formula
            excess = r2_formula
            limiting_units = rxn_units_r1
            used_moles_excess = rxn_units_r1 * r2_coeff
            remaining_moles_excess = moles_r2 - used_moles_excess
            remaining_mass_excess = remaining_moles_excess * mm_r2
        else:
            limiting = r2_formula
            excess = r1_formula
            limiting_units = rxn_units_r2
            used_moles_excess = rxn_units_r2 * r1_coeff
            remaining_moles_excess = moles_r1 - used_moles_excess
            remaining_mass_excess = remaining_moles_excess * mm_r1

        prod_moles_theoretical = limiting_units * prod_coeff
        prod_mass_theoretical = prod_moles_theoretical * mm_prod

        print("\n" + "=" * 45)
        print(f"  LIMITING REAGENT : {limiting}")
        print(f"  EXCESS REAGENT   : {excess}")
        print("-" * 45)
        print(f"Remaining Excess ({excess}): {remaining_mass_excess:.4f} g ({remaining_moles_excess:.4f} mol)")
        print(f"Theoretical Product ({prod_formula}): {prod_mass_theoretical:.4f} g ({prod_moles_theoretical:.4f} mol)")
        print("=" * 45)

    except Exception as e:
        print(f"\n[Error] Calculation failed: {e}")

    input("\nPress ENTER to return to menu...")
