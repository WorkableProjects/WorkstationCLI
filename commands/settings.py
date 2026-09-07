"""CLI-wide settings menu (theme, appearance preferences)."""

from core.menu import display_menu
from services.config import load_config, save_config


def run_settings_menu() -> None:
    """Display settings menu for AI, UI appearance, graphing defaults, and system config."""
    from commands.common_ai import configure_ai_settings
    from graphing.menu import run_plot_settings_menu

    while True:
        options = [
            ("1", "AI & Model Configuration"),
            ("2", "UI & Appearance Preferences"),
            ("3", "Graphing Defaults Configuration"),
            ("4", "Config File & Developer Utilities"),
            ("0", "Return to Main Menu"),
        ]
        choice = display_menu("CLI SETTINGS & PREFERENCES", options)

        if choice == "1":
            configure_ai_settings()
        elif choice == "2":
            run_ui_settings_menu()
        elif choice == "3":
            run_plot_settings_menu()
        elif choice == "4":
            run_developer_settings_menu()
        elif choice == "0":
            return
        else:
            from core import theme_manager
            print("\n" + theme_manager.error("[Error] Invalid selection."))


def run_ui_settings_menu() -> None:
    """Submenu for UI and display preferences."""
    from core import theme_manager
    while True:
        cfg = load_config()
        theme_name = cfg.get("appearance", {}).get("theme", "blue")
        anim_enabled = cfg.get("appearance", {}).get("startup_animation", True)
        anim_status = "Enabled" if anim_enabled else "Disabled"

        options = [
            ("1", f"Change Theme (Current: {theme_name})"),
            ("2", f"Toggle Startup Animation ({anim_status})"),
            ("0", "Return to Settings Menu"),
        ]
        choice = display_menu("UI & APPEARANCE PREFERENCES", options)

        if choice == "1":
            _toggle_theme()
        elif choice == "2":
            _toggle_animation()
        elif choice == "0":
            return
        else:
            print("\n" + theme_manager.error("[Error] Invalid selection."))


def run_developer_settings_menu() -> None:
    """Submenu for developer tools and configuration file access."""
    from core import theme_manager
    from services.config import open_config_in_editor, CONFIG_FILE

    while True:
        options = [
            ("1", "View Config File Path"),
            ("2", "Open Config File in Editor"),
            ("0", "Return to Settings Menu"),
        ]
        choice = display_menu("DEVELOPER & SYSTEM CONFIG", options)

        if choice == "1":
            print(f"\nConfig file path: {CONFIG_FILE}")
            input("\nPress ENTER to continue...")
        elif choice == "2":
            success = open_config_in_editor()
            if success:
                print(theme_manager.ok("Opened config file in system editor."))
            else:
                print(theme_manager.warn(f"Could not open editor. Please edit directly at: {CONFIG_FILE}"))
            input("\nPress ENTER to continue...")
        elif choice == "0":
            return
        else:
            print("\n" + theme_manager.error("[Error] Invalid selection."))


def toggle_startup_animation() -> None:
    """Toggle startup animation preference."""
    _toggle_animation()


def toggle_theme() -> None:
    """Prompt user to select a theme and save preference."""
    _toggle_theme()


def get_animation_status() -> str:
    """Get status string for startup animation setting."""
    cfg = load_config()
    enabled = cfg.get("appearance", {}).get("startup_animation", True)
    return "Enabled" if enabled else "Disabled"


def show_config_location() -> None:
    """Display the configuration file path."""
    from services.config import CONFIG_FILE
    print(f"\nConfig file location: {CONFIG_FILE}")
    print("Edit manually to change other settings.")
    input("\nPress ENTER to continue...")


def _toggle_animation() -> None:
    """Toggle startup animation preference."""
    from core import theme_manager
    cfg = load_config()
    current = cfg.get("appearance", {}).get("startup_animation", True)
    new_val = not current
    cfg["appearance"]["startup_animation"] = new_val
    save_config(cfg)
    status_str = "Enabled" if new_val else "Disabled"
    print("\n" + theme_manager.ok(f"✓ Startup animation is now {status_str}."))
    input("\nPress ENTER to return...")


def _toggle_theme() -> None:
    """Prompt user to select a theme and save preference."""
    from core import theme_manager
    from core.formatter import format_header
    
    cfg = load_config()
    appearance = cfg.get("appearance", {})
    current_theme = appearance.get("theme", "blue")
    
    print("\n" + "=" * 40)
    print(" APPEARANCE THEME ".center(40))
    print("=" * 40)
    print(f"Current theme: {theme_manager.header(current_theme)}")
    print("\nAvailable themes:")
    print("  1. Blue (Dark Blue)")
    print("  2. Pink (Refined Pink)")
    print("  3. Red")
    print("  4. Orange")
    print("  5. Green")
    print("  6. Cyan")
    print("  7. Black (High Contrast)")
    print("=" * 40)
    
    choice = input("\nSelect theme (1-7): ").strip()
    
    theme_map = {
        "1": "blue",
        "2": "pink",
        "3": "red",
        "4": "orange",
        "5": "green",
        "6": "cyan",
        "7": "black"
    }
    new_theme = theme_map.get(choice)
    
    if not new_theme:
        print("\n" + theme_manager.error("[Error] Invalid selection."))
        input("\nPress ENTER to return...")
        return
    
    if new_theme == current_theme:
        print(f"\nTheme already set to {current_theme}.")
        input("\nPress ENTER to return...")
        return
    
    cfg["appearance"]["theme"] = new_theme
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
