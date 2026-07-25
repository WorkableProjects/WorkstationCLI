from core.formatter import format_header
from core.menu import display_menu
from utils.validation import validate_positive_float
from utils.units import pressure_to_atm, atm_to_pressure, temp_to_kelvin, kelvin_to_temp, volume_to_liters

R_ATM = 0.08206  # L·atm/(mol·K)

def run_gas_laws_calculator() -> None:
    while True:
        options = [
            ("1", "Ideal Gas Law (PV = nRT)"),
            ("2", "Boyle's Law (P1V1 = P2V2)"),
            ("3", "Charles's Law (V1/T1 = V2/T2)"),
            ("4", "Gay-Lussac's Law (P1/T1 = P2/T2)"),
            ("5", "Combined Gas Law (P1V1/T1 = P2V2/T2)"),
            ("6", "Avogadro's Law (V1/n1 = V2/n2)"),
            ("0", "Return to Main Menu")
        ]
        choice = display_menu("GAS LAWS CALCULATOR", options)
        
        if choice == "1":
            _solve_ideal_gas_law()
        elif choice == "2":
            _solve_boyles_law()
        elif choice == "3":
            _solve_charles_law()
        elif choice == "4":
            _solve_gay_lussacs_law()
        elif choice == "5":
            _solve_combined_gas_law()
        elif choice == "6":
            _solve_avogadro_law()
        elif choice == "0":
            break
        else:
            print("\n[Error] Invalid selection.")

def _solve_ideal_gas_law() -> None:
    print(format_header("IDEAL GAS LAW (PV = nRT)"))
    print("Leave the unknown variable blank (press ENTER) to calculate it.\n")
    try:
        p_str = input("Pressure P (in atm, or blank): ").strip()
        v_str = input("Volume V (in L, or blank): ").strip()
        n_str = input("Moles n (in mol, or blank): ").strip()
        t_str = input("Temperature T (in K, or blank): ").strip()

        blanks = [x == "" for x in [p_str, v_str, n_str, t_str]]
        if blanks.count(True) != 1:
            print("\n[Error] Please leave EXACTLY ONE variable blank to solve for it.")
            input("\nPress ENTER to continue...")
            return

        if p_str == "":
            v = validate_positive_float(v_str, "Volume")
            n = validate_positive_float(n_str, "Moles")
            t = validate_positive_float(t_str, "Temperature")
            p = (n * R_ATM * t) / v
            print(f"\nResult: Calculated Pressure P = {p:.2f} atm")
        elif v_str == "":
            p = validate_positive_float(p_str, "Pressure")
            n = validate_positive_float(n_str, "Moles")
            t = validate_positive_float(t_str, "Temperature")
            v = (n * R_ATM * t) / p
            print(f"\nResult: Calculated Volume V = {v:.2f} L")
        elif n_str == "":
            p = validate_positive_float(p_str, "Pressure")
            v = validate_positive_float(v_str, "Volume")
            t = validate_positive_float(t_str, "Temperature")
            n = (p * v) / (R_ATM * t)
            print(f"\nResult: Calculated Moles n = {n:.2f} mol")
        elif t_str == "":
            p = validate_positive_float(p_str, "Pressure")
            v = validate_positive_float(v_str, "Volume")
            n = validate_positive_float(n_str, "Moles")
            t = (p * v) / (n * R_ATM)
            print(f"\nResult: Calculated Temperature T = {t:.2f} K")
    except Exception as e:
        print(f"\n[Error] Calculation failed: {e}")
    input("\nPress ENTER to continue...")

def _solve_boyles_law() -> None:
    print(format_header("BOYLE'S LAW (P1V1 = P2V2)"))
    print("Leave one variable blank to solve.\n")
    try:
        p1_str = input("P1: ").strip()
        v1_str = input("V1: ").strip()
        p2_str = input("P2: ").strip()
        v2_str = input("V2: ").strip()

        blanks = [x == "" for x in [p1_str, v1_str, p2_str, v2_str]]
        if blanks.count(True) != 1:
            print("\n[Error] Leave exactly one variable blank.")
            input("\nPress ENTER to continue...")
            return

        if p1_str == "":
            v1 = validate_positive_float(v1_str, "V1")
            p2 = validate_positive_float(p2_str, "P2")
            v2 = validate_positive_float(v2_str, "V2")
            p1 = (p2 * v2) / v1
            print(f"\nResult: P1 = {p1:.2f}")
        elif v1_str == "":
            p1 = validate_positive_float(p1_str, "P1")
            p2 = validate_positive_float(p2_str, "P2")
            v2 = validate_positive_float(v2_str, "V2")
            v1 = (p2 * v2) / p1
            print(f"\nResult: V1 = {v1:.2f}")
        elif p2_str == "":
            p1 = validate_positive_float(p1_str, "P1")
            v1 = validate_positive_float(v1_str, "V1")
            v2 = validate_positive_float(v2_str, "V2")
            p2 = (p1 * v1) / v2
            print(f"\nResult: P2 = {p2:.2f}")
        elif v2_str == "":
            p1 = validate_positive_float(p1_str, "P1")
            v1 = validate_positive_float(v1_str, "V1")
            p2 = validate_positive_float(p2_str, "P2")
            v2 = (p1 * v1) / p2
            print(f"\nResult: V2 = {v2:.2f}")
    except Exception as e:
        print(f"\n[Error] Calculation failed: {e}")
    input("\nPress ENTER to continue...")

def _solve_charles_law() -> None:
    print(format_header("CHARLES'S LAW (V1/T1 = V2/T2)"))
    print("Temperatures must be in Kelvin. Leave one variable blank.\n")
    try:
        v1_str = input("V1: ").strip()
        t1_str = input("T1 (K): ").strip()
        v2_str = input("V2: ").strip()
        t2_str = input("T2 (K): ").strip()

        blanks = [x == "" for x in [v1_str, t1_str, v2_str, t2_str]]
        if blanks.count(True) != 1:
            print("\n[Error] Leave exactly one variable blank.")
            input("\nPress ENTER to continue...")
            return

        if v1_str == "":
            t1 = validate_positive_float(t1_str, "T1")
            v2 = validate_positive_float(v2_str, "V2")
            t2 = validate_positive_float(t2_str, "T2")
            v1 = (v2 * t1) / t2
            print(f"\nResult: V1 = {v1:.2f}")
        elif t1_str == "":
            v1 = validate_positive_float(v1_str, "V1")
            v2 = validate_positive_float(v2_str, "V2")
            t2 = validate_positive_float(t2_str, "T2")
            t1 = (v1 * t2) / v2
            print(f"\nResult: T1 = {t1:.2f} K")
        elif v2_str == "":
            v1 = validate_positive_float(v1_str, "V1")
            t1 = validate_positive_float(t1_str, "T1")
            t2 = validate_positive_float(t2_str, "T2")
            v2 = (v1 * t2) / t1
            print(f"\nResult: V2 = {v2:.2f}")
        elif t2_str == "":
            v1 = validate_positive_float(v1_str, "V1")
            t1 = validate_positive_float(t1_str, "T1")
            v2 = validate_positive_float(v2_str, "V2")
            t2 = (v2 * t1) / v1
            print(f"\nResult: T2 = {t2:.2f} K")
    except Exception as e:
        print(f"\n[Error] Calculation failed: {e}")
    input("\nPress ENTER to continue...")

def _solve_gay_lussacs_law() -> None:
    print(format_header("GAY-LUSSAC'S LAW (P1/T1 = P2/T2)"))
    print("Temperatures must be in Kelvin. Leave one variable blank.\n")
    try:
        p1_str = input("P1: ").strip()
        t1_str = input("T1 (K): ").strip()
        p2_str = input("P2: ").strip()
        t2_str = input("T2 (K): ").strip()

        blanks = [x == "" for x in [p1_str, t1_str, p2_str, t2_str]]
        if blanks.count(True) != 1:
            print("\n[Error] Leave exactly one variable blank.")
            input("\nPress ENTER to continue...")
            return

        if p1_str == "":
            t1 = validate_positive_float(t1_str, "T1")
            p2 = validate_positive_float(p2_str, "P2")
            t2 = validate_positive_float(t2_str, "T2")
            p1 = (p2 * t1) / t2
            print(f"\nResult: P1 = {p1:.2f}")
        elif t1_str == "":
            p1 = validate_positive_float(p1_str, "P1")
            p2 = validate_positive_float(p2_str, "P2")
            t2 = validate_positive_float(t2_str, "T2")
            t1 = (p1 * t2) / p2
            print(f"\nResult: T1 = {t1:.2f} K")
        elif p2_str == "":
            p1 = validate_positive_float(p1_str, "P1")
            t1 = validate_positive_float(t1_str, "T1")
            t2 = validate_positive_float(t2_str, "T2")
            p2 = (p1 * t2) / t1
            print(f"\nResult: P2 = {p2:.2f}")
        elif t2_str == "":
            p1 = validate_positive_float(p1_str, "P1")
            t1 = validate_positive_float(t1_str, "T1")
            p2 = validate_positive_float(p2_str, "P2")
            t2 = (p2 * t1) / p1
            print(f"\nResult: T2 = {t2:.2f} K")
    except Exception as e:
        print(f"\n[Error] Calculation failed: {e}")
    input("\nPress ENTER to continue...")

def _solve_combined_gas_law() -> None:
    print(format_header("COMBINED GAS LAW (P1V1/T1 = P2V2/T2)"))
    print("Temperatures must be in Kelvin. Leave one variable blank.\n")
    try:
        p1_str = input("P1: ").strip()
        v1_str = input("V1: ").strip()
        t1_str = input("T1 (K): ").strip()
        p2_str = input("P2: ").strip()
        v2_str = input("V2: ").strip()
        t2_str = input("T2 (K): ").strip()

        blanks = [x == "" for x in [p1_str, v1_str, t1_str, p2_str, v2_str, t2_str]]
        if blanks.count(True) != 1:
            print("\n[Error] Leave exactly one variable blank.")
            input("\nPress ENTER to continue...")
            return

        if p1_str == "":
            v1, t1 = validate_positive_float(v1_str, "V1"), validate_positive_float(t1_str, "T1")
            p2, v2, t2 = validate_positive_float(p2_str, "P2"), validate_positive_float(v2_str, "V2"), validate_positive_float(t2_str, "T2")
            p1 = (p2 * v2 * t1) / (v1 * t2)
            print(f"\nResult: P1 = {p1:.2f}")
        elif v1_str == "":
            p1, t1 = validate_positive_float(p1_str, "P1"), validate_positive_float(t1_str, "T1")
            p2, v2, t2 = validate_positive_float(p2_str, "P2"), validate_positive_float(v2_str, "V2"), validate_positive_float(t2_str, "T2")
            v1 = (p2 * v2 * t1) / (p1 * t2)
            print(f"\nResult: V1 = {v1:.2f}")
        elif t1_str == "":
            p1, v1 = validate_positive_float(p1_str, "P1"), validate_positive_float(v1_str, "V1")
            p2, v2, t2 = validate_positive_float(p2_str, "P2"), validate_positive_float(v2_str, "V2"), validate_positive_float(t2_str, "T2")
            t1 = (p1 * v1 * t2) / (p2 * v2)
            print(f"\nResult: T1 = {t1:.2f} K")
        elif p2_str == "":
            p1, v1, t1 = validate_positive_float(p1_str, "P1"), validate_positive_float(v1_str, "V1"), validate_positive_float(t1_str, "T1")
            v2, t2 = validate_positive_float(v2_str, "V2"), validate_positive_float(t2_str, "T2")
            p2 = (p1 * v1 * t2) / (v2 * t1)
            print(f"\nResult: P2 = {p2:.2f}")
        elif v2_str == "":
            p1, v1, t1 = validate_positive_float(p1_str, "P1"), validate_positive_float(v1_str, "V1"), validate_positive_float(t1_str, "T1")
            p2, t2 = validate_positive_float(p2_str, "P2"), validate_positive_float(t2_str, "T2")
            v2 = (p1 * v1 * t2) / (p2 * t1)
            print(f"\nResult: V2 = {v2:.2f}")
        elif t2_str == "":
            p1, v1, t1 = validate_positive_float(p1_str, "P1"), validate_positive_float(v1_str, "V1"), validate_positive_float(t1_str, "T1")
            p2, v2 = validate_positive_float(p2_str, "P2"), validate_positive_float(v2_str, "V2")
            t2 = (p2 * v2 * t1) / (p1 * v1)
            print(f"\nResult: T2 = {t2:.2f} K")
    except Exception as e:
        print(f"\n[Error] Calculation failed: {e}")
    input("\nPress ENTER to continue...")

def _solve_avogadro_law() -> None:
    print(format_header("AVOGADRO'S LAW (V1/n1 = V2/n2)"))
    print("Leave one variable blank.\n")
    try:
        v1_str = input("V1: ").strip()
        n1_str = input("n1 (mol): ").strip()
        v2_str = input("V2: ").strip()
        n2_str = input("n2 (mol): ").strip()

        blanks = [x == "" for x in [v1_str, n1_str, v2_str, n2_str]]
        if blanks.count(True) != 1:
            print("\n[Error] Leave exactly one variable blank.")
            input("\nPress ENTER to continue...")
            return

        if v1_str == "":
            n1 = validate_positive_float(n1_str, "n1")
            v2 = validate_positive_float(v2_str, "V2")
            n2 = validate_positive_float(n2_str, "n2")
            v1 = (v2 * n1) / n2
            print(f"\nResult: V1 = {v1:.2f}")
        elif n1_str == "":
            v1 = validate_positive_float(v1_str, "V1")
            v2 = validate_positive_float(v2_str, "V2")
            n2 = validate_positive_float(n2_str, "n2")
            n1 = (v1 * n2) / v2
            print(f"\nResult: n1 = {n1:.2f} mol")
        elif v2_str == "":
            v1 = validate_positive_float(v1_str, "V1")
            n1 = validate_positive_float(n1_str, "n1")
            n2 = validate_positive_float(n2_str, "n2")
            v2 = (v1 * n2) / n1
            print(f"\nResult: V2 = {v2:.2f}")
        elif n2_str == "":
            v1 = validate_positive_float(v1_str, "V1")
            n1 = validate_positive_float(n1_str, "n1")
            v2 = validate_positive_float(v2_str, "V2")
            n2 = (v2 * n1) / v1
            print(f"\nResult: n2 = {n2:.2f} mol")
    except Exception as e:
        print(f"\n[Error] Calculation failed: {e}")
    input("\nPress ENTER to continue...")
