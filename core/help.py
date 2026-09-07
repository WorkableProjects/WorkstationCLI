"""Context-sensitive help/tooltip system for menus."""

HELP_MAP = {
    "WORKSTATION CLI": "Top-level menu. Choose a category to begin (Chemistry, AI, Graphing, Settings, Info).",
    "CHEMISTRY": "Chemistry calculators and reference tools. Pick a calculator or reference lookup.",
    "AI": "AI study tools: chat, quiz generation, and study planners.",
    "GRAPHING TOOL": "Graphing tool. Plot custom functions f(x) or explore preset mathematical functions.",
    "PRESET FUNCTIONS": "Explore predefined common mathematical functions.",
    "PLOT SETTINGS": "Configure default domain bounds, vertical scaling, and plot dimensions.",
    "INTERACTIVE PERIODIC TABLE": "Navigate 118 elements in 2D layout with arrow keys or jump with search (/ or s).",
    "CHEMISTRY REFERENCE DATA": "Lookup periodic table elements, polyatomic ions, and constants.",
    "MOLAR MASS CALCULATOR": "Enter a chemical formula to compute molar mass and composition.",
}


def show_help(menu_title: str) -> None:
    text = HELP_MAP.get(menu_title.upper(), "No help available for this menu.")
    print("\nHELP:\n")
    print(text)
    print()
    input("Press ENTER to return to menu...")
