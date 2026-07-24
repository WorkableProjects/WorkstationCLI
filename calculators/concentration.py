from core.formatter import format_header
from core.menu import display_menu
from utils.validation import validate_positive_float

def run_concentration_calculator() -> None:
    while True:
        options = [
            ("1", "Molarity (mol solute / L solution)"),
            ("2", "Molality (mol solute / kg solvent)"),
            ("3", "Mass Percent (% w/w)"),
            ("4", "Volume Percent (% v/v)"),
            ("5", "Parts per Million (ppm) & Parts per Billion (ppb)"),
            ("0", "Return to Main Menu")
        ]
        choice = display_menu("CONCENTRATION CALCULATOR", options)
        
        if choice == "1":
            _calc_molarity()
        elif choice == "2":
            _calc_molality()
        elif choice == "3":
            _calc_mass_percent()
        elif choice == "4":
            _calc_volume_percent()
        elif choice == "5":
            _calc_ppm_ppb()
        elif choice == "0":
            break
        else:
            print("\n[Error] Invalid choice.")

def _calc_molarity() -> None:
    print(format_header("MOLARITY (M = moles / Liters)"))
    try:
        moles_str = input("Moles of solute (mol): ").strip()
        vol_str = input("Volume of solution (L): ").strip()
        moles = validate_positive_float(moles_str, "Moles")
        vol = validate_positive_float(vol_str, "Volume")
        molarity = moles / vol
        print(f"\nResult: Molarity = {molarity:.4f} M (mol/L)")
    except Exception as e:
        print(f"\n[Error]: {e}")
    input("\nPress ENTER to continue...")

def _calc_molality() -> None:
    print(format_header("MOLALITY (m = moles solute / kg solvent)"))
    try:
        moles_str = input("Moles of solute (mol): ").strip()
        mass_str = input("Mass of solvent (kg): ").strip()
        moles = validate_positive_float(moles_str, "Moles")
        mass = validate_positive_float(mass_str, "Mass of solvent")
        molality = moles / mass
        print(f"\nResult: Molality = {molality:.4f} m (mol/kg)")
    except Exception as e:
        print(f"\n[Error]: {e}")
    input("\nPress ENTER to continue...")

def _calc_mass_percent() -> None:
    print(format_header("MASS PERCENT (% w/w)"))
    try:
        solute_str = input("Mass of solute (g): ").strip()
        total_str = input("Total mass of solution (g): ").strip()
        solute = validate_positive_float(solute_str, "Mass of solute")
        total = validate_positive_float(total_str, "Total mass")
        if solute > total:
            print("\n[Warning] Mass of solute exceeds total solution mass.")
        percent = (solute / total) * 100.0
        print(f"\nResult: Mass Percent = {percent:.4f}%")
    except Exception as e:
        print(f"\n[Error]: {e}")
    input("\nPress ENTER to continue...")

def _calc_volume_percent() -> None:
    print(format_header("VOLUME PERCENT (% v/v)"))
    try:
        solute_str = input("Volume of solute (mL): ").strip()
        total_str = input("Total volume of solution (mL): ").strip()
        solute = validate_positive_float(solute_str, "Volume of solute")
        total = validate_positive_float(total_str, "Total volume")
        percent = (solute / total) * 100.0
        print(f"\nResult: Volume Percent = {percent:.4f}%")
    except Exception as e:
        print(f"\n[Error]: {e}")
    input("\nPress ENTER to continue...")

def _calc_ppm_ppb() -> None:
    print(format_header("PARTS PER MILLION / BILLION (ppm / ppb)"))
    try:
        solute_str = input("Mass of solute (mg or g): ").strip()
        total_str = input("Mass of solution (same unit as solute): ").strip()
        solute = validate_positive_float(solute_str, "Solute mass")
        total = validate_positive_float(total_str, "Solution mass")
        
        ppm = (solute / total) * 1e6
        ppb = (solute / total) * 1e9
        print(f"\nResult:")
        print(f"  Concentration in ppm : {ppm:.4f} ppm")
        print(f"  Concentration in ppb : {ppb:.4f} ppb")
    except Exception as e:
        print(f"\n[Error]: {e}")
    input("\nPress ENTER to continue...")
