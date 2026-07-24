from core.formatter import format_header
from utils.validation import validate_positive_float

def run_dilution_calculator() -> None:
    print(format_header("DILUTION CALCULATOR (M1V1 = M2V2)"))
    print("Leave exactly ONE variable blank (press ENTER) to calculate it.\n")
    try:
        m1_str = input("Initial Concentration M1 (M or mol/L, or blank): ").strip()
        v1_str = input("Initial Volume V1 (mL or L, or blank): ").strip()
        m2_str = input("Final Concentration M2 (M or mol/L, or blank): ").strip()
        v2_str = input("Final Volume V2 (mL or L, or blank): ").strip()

        blanks = [x == "" for x in [m1_str, v1_str, m2_str, v2_str]]
        if blanks.count(True) != 1:
            print("\n[Error] Please leave EXACTLY ONE variable blank.")
            input("\nPress ENTER to return...")
            return

        if m1_str == "":
            v1 = validate_positive_float(v1_str, "V1")
            m2 = validate_positive_float(m2_str, "M2")
            v2 = validate_positive_float(v2_str, "V2")
            m1 = (m2 * v2) / v1
            print(f"\nResult: Initial Concentration M1 = {m1:.4f} M")
        elif v1_str == "":
            m1 = validate_positive_float(m1_str, "M1")
            m2 = validate_positive_float(m2_str, "M2")
            v2 = validate_positive_float(v2_str, "V2")
            v1 = (m2 * v2) / m1
            print(f"\nResult: Initial Volume V1 = {v1:.4f} (same units as V2)")
        elif m2_str == "":
            m1 = validate_positive_float(m1_str, "M1")
            v1 = validate_positive_float(v1_str, "V1")
            v2 = validate_positive_float(v2_str, "V2")
            m2 = (m1 * v1) / v2
            print(f"\nResult: Final Concentration M2 = {m2:.4f} M")
        elif v2_str == "":
            m1 = validate_positive_float(m1_str, "M1")
            v1 = validate_positive_float(v1_str, "V1")
            m2 = validate_positive_float(m2_str, "M2")
            v2 = (m1 * v1) / m2
            print(f"\nResult: Final Volume V2 = {v2:.4f} (same units as V1)")

    except Exception as e:
        print(f"\n[Error] Dilution calculation failed: {e}")

    input("\nPress ENTER to return to menu...")
