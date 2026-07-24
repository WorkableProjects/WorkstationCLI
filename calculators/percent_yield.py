from core.formatter import format_header
from utils.validation import validate_non_negative_float, validate_positive_float

def run_percent_yield_calculator() -> None:
    print(format_header("PERCENT YIELD CALCULATOR"))
    print("Formula: (Actual Yield / Theoretical Yield) × 100\n")
    try:
        actual_str = input("Actual Yield (g or mol): ").strip()
        theoretical_str = input("Theoretical Yield (same unit as actual): ").strip()

        actual = validate_non_negative_float(actual_str, "Actual Yield")
        theoretical = validate_positive_float(theoretical_str, "Theoretical Yield")

        if actual > theoretical:
            print("\n[Warning] Actual yield is greater than theoretical yield (exceeds 100%). Check for impurities/error.")

        percent_yield = (actual / theoretical) * 100.0

        print("\n" + "=" * 40)
        print(f"  Actual Yield      : {actual}")
        print(f"  Theoretical Yield : {theoretical}")
        print(f"  PERCENT YIELD     : {percent_yield:.2f}%")
        print("=" * 40)

    except Exception as e:
        print(f"\n[Error] Calculation failed: {e}")

    input("\nPress ENTER to return to menu...")
