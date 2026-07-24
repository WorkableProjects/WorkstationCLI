from typing import List, Tuple, Optional

def display_menu(title: str, options: List[Tuple[str, str]]) -> str:
    """
    Displays a formatted menu given a list of options: [(key, description), ...]
    Returns user input string.
    """
    print("\n" + "=" * 40)
    if title:
        print(f" {title.center(38)} ")
        print("=" * 40)
    for key, desc in options:
        print(f"  {key}. {desc}")
    print("=" * 40)
    choice = input("\nSelect an option: ").strip()
    return choice
