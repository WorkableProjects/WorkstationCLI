from core.banner import VERSION, ORGANIZATION, AUTHOR

def display_about() -> None:
    print("\n" + "=" * 50)
    print("           CLI INFORMATION PAGE           ")
    print("=" * 50)
    print(f"  Application : Workstation CLI")
    print(f"  Version     : {VERSION}")
    print(f"  Author(s)   : {AUTHOR}")
    print(f"  Organization: {ORGANIZATION}")
    print("=" * 50)
    print("\n  Offline Chemistry Suite & Calculator Engine.")
    print("  Education First.")
    print("\n" + "=" * 50)
    input("\nPress ENTER to return to the main menu...")
