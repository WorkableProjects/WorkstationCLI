from core.formatter import format_header
from core.menu import display_menu
from utils.parser import parse_chemical_formula, load_periodic_table
from utils.validation import validate_positive_float
from typing import Tuple


def count_sig_figs(num_str: str) -> int:
    """Return the number of significant figures in a numeric string.
    Handles integers, decimals, and scientific notation.
    """
    s = num_str.strip().lower()
    # Remove exponent part if present
    if 'e' in s:
        s = s.split('e')[0]
    # Strip sign
    if s.startswith('+') or s.startswith('-'):
        s = s[1:]
    if '.' in s:
        int_part, frac_part = s.split('.')
        # Count significant digits in integer part (exclude leading zeros)
        int_sig = len(int_part.lstrip('0'))
        if int_sig > 0:
            # All fractional digits are significant
            sig = int_sig + len(frac_part)
        else:
            # No non‑zero integer part; leading zeros in fraction are not significant
            sig = len(frac_part.lstrip('0'))
        return max(sig, 1)
    else:
        # Integer without decimal point: count digits after stripping leading zeros
        sig = len(s.lstrip('0'))
        return max(sig, 1)

AVOGADRO = 6.02214076e23
MOLAR_VOLUME_STP = 22.414  # L/mol
from core.menu import display_menu
from utils.parser import parse_chemical_formula, load_periodic_table
from utils.validation import validate_positive_float

AVOGADRO = 6.02214076e23
MOLAR_VOLUME_STP = 22.414  # L/mol

def get_molar_mass(formula: str) -> float:
    periodic_table = load_periodic_table()
    counts = parse_chemical_formula(formula)
    return sum(periodic_table[elem]["mass"] * cnt for elem, cnt in counts.items())

def run_stoichiometry_calculator() -> None:
    while True:
        options = [
            ("1", "Mass ⇄ Moles"),
            ("2", "Moles ⇄ Particles (Atoms / Molecules)"),
            ("3", "Moles ⇄ Volume at STP (Gases)"),
            ("4", "Reaction Conversion (Species A -> Species B)"),
            ("0", "Return to Main Menu")
        ]
        choice = display_menu("STOICHIOMETRY CALCULATOR", options)
        
        if choice == "1":
            _mass_moles_conversion()
        elif choice == "2":
            _moles_particles_conversion()
        elif choice == "3":
            _moles_volume_conversion()
        elif choice == "4":
            _reaction_conversion()
        elif choice == "0":
            break
        else:
            print("\n[Error] Invalid choice.")

from core.console import preserve_output

def _mass_moles_conversion() -> None:
    print(format_header("MASS ⇄ MOLES CONVERSION"))
    formula = input("Chemical Formula (e.g. H2O): ").strip()
    try:
        mm = get_molar_mass(formula)
        preserve_output(f"Molar mass of {formula}: {mm:.4f} g/mol")
        
        mode = input("\nConvert (1) Mass -> Moles or (2) Moles -> Mass: ").strip()
        if mode == "1":
            mass_str = input("Enter Mass (g): ").strip()
            mass = validate_positive_float(mass_str, "Mass")
            moles = mass / mm
            preserve_output(f"\nResult: {mass:.4f} g of {formula} = {moles:.6f} moles")
        elif mode == "2":
            moles_str = input("Enter Moles (mol): ").strip()
            moles = validate_positive_float(moles_str, "Moles")
            mass = moles * mm
            preserve_output(f"\nResult: {moles:.6f} mol of {formula} = {mass:.4f} g")
        else:
            preserve_output("[Error] Invalid selection.")
    except Exception as e:
        preserve_output(f"[Error]: {e}")
    input("\nPress ENTER to continue...")

def _moles_particles_conversion() -> None:
    print(format_header("MOLES ⇄ PARTICLES CONVERSION"))
    try:
        mode = input("Convert (1) Moles -> Particles or (2) Particles -> Moles: ").strip()
        if mode == "1":
            moles_str = input("Enter Moles (mol): ").strip()
            moles = validate_positive_float(moles_str, "Moles")
            particles = moles * AVOGADRO
            print(f"\nResult: {moles} mol = {particles:.6e} particles")
        elif mode == "2":
            part_str = input("Enter number of particles: ").strip()
            particles = validate_positive_float(part_str, "Particles")
            moles = particles / AVOGADRO
            print(f"\nResult: {particles:.6e} particles = {moles:.6f} moles")
        else:
            print("[Error] Invalid selection.")
    except Exception as e:
        print(f"[Error]: {e}")
    input("\nPress ENTER to continue...")

def _moles_volume_conversion() -> None:
    print(format_header("MOLES ⇄ VOLUME AT STP"))
    try:
        mode = input("Convert (1) Moles -> Volume or (2) Volume -> Moles: ").strip()
        if mode == "1":
            moles_str = input("Enter Moles (mol): ").strip()
            moles = validate_positive_float(moles_str, "Moles")
            vol = moles * MOLAR_VOLUME_STP
            print(f"\nResult: {moles} mol = {vol:.4f} L at STP")
        elif mode == "2":
            vol_str = input("Enter Volume (L): ").strip()
            vol = validate_positive_float(vol_str, "Volume")
            moles = vol / MOLAR_VOLUME_STP
            print(f"\nResult: {vol:.4f} L = {moles:.6f} mol at STP")
        else:
            print("[Error] Invalid selection.")
    except Exception as e:
        print(f"[Error]: {e}")
    input("\nPress ENTER to continue...")

def round_sig_figs(val: float, sig_figs: int = 3) -> float:
    if val == 0:
        return 0.0
    import math
    return round(val, sig_figs - int(math.floor(math.log10(abs(val)))) - 1)

def format_sig_figs(val: float, sig_figs: int = 3) -> str:
    if val == 0:
        return "0.0"
    import math
    decimals = sig_figs - int(math.floor(math.log10(abs(val)))) - 1
    if decimals <= 0:
        return f"{round(val, decimals):.0f}"
    else:
        return f"{val:.{decimals}f}"

def _reaction_conversion() -> None:
    print(format_header("REACTION CONVERSION (SPECIES A -> Species B)"))
    try:
        # Q1: Reaction
        reaction = input("Q1) What is the reaction with coefficients? (e.g. 2H2 + O2 -> 2H2O): ").strip()
        
        formula_a = input("Enter chemical formula for Species A: ").strip()
        coeff_a_str = input(f"Enter stoichiometric coefficient for Species A ({formula_a}): ").strip()
        coeff_a = validate_positive_float(coeff_a_str, "Coefficient A")
        
        formula_b = input("\nEnter chemical formula for Species B: ").strip()
        coeff_b_str = input(f"Enter stoichiometric coefficient for Species B ({formula_b}): ").strip()
        coeff_b = validate_positive_float(coeff_b_str, "Coefficient B")
    
        # Q2: Molar mass of A
        mm_a = get_molar_mass(formula_a)
        print(f"\nQ2) What is the molar mass of A? (Use periodic table)")
        print(f"    => Molar mass of {formula_a} = {mm_a:.2f} g/mol")
    
        # Q3: Molar mass of B
        mm_b = get_molar_mass(formula_b)
        print(f"\nQ3) What is the molar mass of B? (Use periodic table)")
        print(f"    => Molar mass of {formula_b} = {mm_b:.2f} g/mol")
    
        # Unit selection for Q4
        print("\nConversion units:")
        print("1. Grams A ⇄ Grams B")
        print("2. Moles A ⇄ Moles B")
        print("3. Grams A ⇄ Moles B")
        print("4. Moles A ⇄ Grams B")
        unit_choice = input("Select conversion unit option (1-4, default 1): ").strip() or "1"
    
        if unit_choice == "2":
            # Moles to Moles
            moles_a_str = input(f"\nQ4) Given moles of A ({formula_a}), how many moles of B ({formula_b}) will be produced/reacted?: ").strip()
            moles_a = validate_positive_float(moles_a_str, f"Moles of {formula_a}")
            moles_b = moles_a * (coeff_b / coeff_a)
            sig = count_sig_figs(moles_a_str)
            print("\n" + "-" * 40)
            print(f"Reaction: {reaction}")
            print(f"Given: {format_sig_figs(moles_a, sig)} mol of {formula_a}")
            print(f"Result: {format_sig_figs(moles_b, sig)} mol of {formula_b} will be produced/reacted.")
            print("-" * 40)
        elif unit_choice == "3":
            # Grams to Moles (B)
            mass_a_str = input(f"\nQ4) Given a mass of A ({formula_a}) in grams, how many moles of B ({formula_b}) will be produced/reacted?: ").strip()
            mass_a = validate_positive_float(mass_a_str, f"Mass of {formula_a}")
            moles_a = mass_a / mm_a
            moles_b = moles_a * (coeff_b / coeff_a)
            sig = count_sig_figs(mass_a_str)
            print("\n" + "-" * 40)
            print(f"Reaction: {reaction}")
            print(f"Given: {format_sig_figs(mass_a, sig)} g of {formula_a} ({format_sig_figs(moles_a, sig)} mol)")
            print(f"Result: {format_sig_figs(moles_b, sig)} mol of {formula_b} will be produced/reacted.")
            print("-" * 40)
        elif unit_choice == "4":
            # Moles to Grams (B)
            moles_a_str = input(f"\nQ4) Given moles of A ({formula_a}), how many grams of B ({formula_b}) will be produced/reacted?: ").strip()
            moles_a = validate_positive_float(moles_a_str, f"Moles of {formula_a}")
            moles_b = moles_a * (coeff_b / coeff_a)
            mass_b = moles_b * mm_b
            sig = count_sig_figs(moles_a_str)
            print("\n" + "-" * 40)
            print(f"Reaction: {reaction}")
            print(f"Given: {format_sig_figs(moles_a, sig)} mol of {formula_a}")
            print(f"Result: {format_sig_figs(mass_b, sig)} g of {formula_b} will be produced/reacted.")
            print("-" * 40)
        else:  # "1" or fallback, Grams to Grams
            mass_a_str = input(f"\nQ4) Given a mass of A ({formula_a}) in grams, how many grams of B ({formula_b}) will be produced/reacted?: ").strip()
            mass_a = validate_positive_float(mass_a_str, f"Mass of {formula_a}")
            moles_a = mass_a / mm_a
            moles_b = moles_a * (coeff_b / coeff_a)
            mass_b = moles_b * mm_b
            sig = count_sig_figs(mass_a_str)
            print("\n" + "-" * 40)
            print(f"Reaction: {reaction}")
            print(f"Given: {format_sig_figs(mass_a, sig)} g of {formula_a} ({format_sig_figs(moles_a, sig)} mol)")
            print(f"Result: {format_sig_figs(mass_b, sig)} g of {formula_b} will be produced/reacted.")
            print("-" * 40)
    
    except Exception as e:
        print(f"[Error]: {e}")
    input("\nPress ENTER to continue...")
