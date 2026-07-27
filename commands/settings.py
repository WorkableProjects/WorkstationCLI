"""CLI-wide settings menu (theme, appearance preferences)."""

from core.menu import display_menu
from services.config import load_config, save_config


def run_settings_menu() -> None:
    """Display settings menu for appearance, theme, and other CLI preferences."""
    while True:
        options = [
            ("1", "Change Theme (Light/Dark)"),
            ("2", "View Config File Location"),
            ("0", "Return to Main Menu"),
        ]
        choice = display_menu("SETTINGS", options)
        
        if choice == "1":
            _toggle_theme()
        elif choice == "2":
            from services.config import CONFIG_FILE
            print(f"\nConfig file location: {CONFIG_FILE}")
            print("Edit manually to change other settings.")
            input("\nPress ENTER to continue...")
        elif choice == "0":
            return
        else:
            from core import theme_manager
            print("\n" + theme_manager.error("[Error] Invalid selection."))


def _toggle_theme() -> None:
    """Prompt user to select a theme and save preference."""
    from core import theme_manager
    from core.formatter import format_header
    
    cfg = load_config()
    appearance = cfg.get("appearance", {})
    current_theme = appearance.get("theme", "dark")
    
    print("\n" + "=" * 40)
    print(" APPEARANCE THEME ".center(40))
    print("=" * 40)
    print(f"Current theme: {theme_manager.header(current_theme)}")
    print("\nAvailable themes:")
    print("  1. Dark")
    print("  2. Light")
    print("=" * 40)
    
    choice = input("\nSelect theme (1 or 2): ").strip()
    
    theme_map = {"1": "dark", "2": "light"}
    new_theme = theme_map.get(choice)
    
    if not new_theme:
        print("\n" + theme_manager.error("[Error] Invalid selection."))
        input("\nPress ENTER to return...")
        return
    
    if new_theme == current_theme:
        print(f"\nTheme already set to {current_theme}.")
        input("\nPress ENTER to return...")
        return
    
    cfg["appearance"] = {"theme": new_theme}
    save_config(cfg)
    
    # Reload theme in memory
    theme_manager.apply_theme()
    
    print("\n" + theme_manager.ok("✓ Theme changed to ") + theme_manager.header(new_theme))
    print(theme_manager.ok("✓ Changes saved and applied immediately."))
    
    # Show a preview with the new theme
    print("\n" + format_header("THEME PREVIEW"))
    print(theme_manager.ok("This text is OK/success"))
    print(theme_manager.warn("This text is WARNING"))
    print(theme_manager.error("This text is ERROR"))
    
    input("\nPress ENTER to return...")
