"""Graphing menu router, preset library, and plot configuration manager."""

from typing import Optional, Dict, Any
from core.menu import display_menu
from core import navigation, theme_manager, help as helpmod
from graphing.plotter import (
    parse_function_expression,
    generate_ascii_plot,
    PRESET_FUNCTIONS,
    PlotSeries
)

# Global plot settings
DEFAULT_PLOT_SETTINGS: Dict[str, Any] = {
    "x_min": -10.0,
    "x_max": 10.0,
    "y_min": None,
    "y_max": None,
    "width": 50,
    "height": 20,
}


def run_custom_function_plot() -> None:
    """Prompt user for custom function f(x) and plot with domain, range, and size controls."""
    print("\n" + theme_manager.header("--- Custom Function Plotter ---"))
    print("Examples: x^2, sin(x), 2*x + 1, exp(-x^2), x^3 - 3*x, 1/x, log(x)")
    expr_str = input("\nEnter function f(x): ").strip()
    if not expr_str:
        print(theme_manager.warn("No expression entered. Returning..."))
        return

    try:
        fn = parse_function_expression(expr_str)
    except Exception as e:
        print(theme_manager.error(f"\n[Error] Invalid expression: {e}"))
        input("\nPress ENTER to continue...")
        return

    # Domain Controls with explicit left/right edge wording and inline hint
    print("\n" + theme_manager.colorize("--- Domain Configuration (X Range) ---", "header"))
    print("Hint: Controls the visible X range from left → right.")
    def_x_min = DEFAULT_PLOT_SETTINGS["x_min"]
    def_x_max = DEFAULT_PLOT_SETTINGS["x_max"]

    x_min_str = input(f"X-axis minimum (left edge) [{def_x_min}]: ").strip()
    x_max_str = input(f"X-axis maximum (right edge) [{def_x_max}]: ").strip()

    try:
        x_min = float(x_min_str) if x_min_str else float(def_x_min)
        x_max = float(x_max_str) if x_max_str else float(def_x_max)
    except ValueError:
        print(theme_manager.error("[Error] Invalid numeric value for domain bounds."))
        input("\nPress ENTER to continue...")
        return

    if x_min >= x_max:
        print(theme_manager.error("[Error] Left edge (x_min) must be strictly less than right edge (x_max)."))
        input("\nPress ENTER to continue...")
        return

    # Y Range configuration (Auto vs Custom)
    print("\n" + theme_manager.colorize("--- Vertical Scaling (Y Range) ---", "header"))
    print("1. Automatic Y scaling (recommended)")
    print("2. Custom Y min & max bounds")
    y_choice = input("Select Y scaling option [1]: ").strip() or "1"

    y_min, y_max = None, None
    if y_choice == "2":
        y_min_str = input("Y-axis minimum (bottom edge): ").strip()
        y_max_str = input("Y-axis maximum (top edge): ").strip()
        try:
            if y_min_str:
                y_min = float(y_min_str)
            if y_max_str:
                y_max = float(y_max_str)
            if y_min is not None and y_max is not None and y_min >= y_max:
                print(theme_manager.error("[Error] Bottom edge (y_min) must be strictly less than top edge (y_max)."))
                input("\nPress ENTER to continue...")
                return
        except ValueError:
            print(theme_manager.error("[Error] Invalid numeric value for Y range."))
            input("\nPress ENTER to continue...")
            return

    # Render plot
    try:
        series = PlotSeries(fn=fn, label=f"f(x) = {expr_str}", symbol="•", expr=expr_str)
        plot_str = generate_ascii_plot(
            series_input=series,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
            width=DEFAULT_PLOT_SETTINGS["width"],
            height=DEFAULT_PLOT_SETTINGS["height"],
            title=f"f(x) = {expr_str}"
        )
        print("\n" + plot_str)
    except Exception as e:
        print(theme_manager.error(f"[Error] Failed to render plot: {e}"))

    input("\nPress ENTER to return to Graphing Menu...")


def run_preset_functions_menu() -> None:
    """Select and plot preset common mathematical functions."""
    preset_names = list(PRESET_FUNCTIONS.keys())
    options = [(str(i + 1), f"{name} — {PRESET_FUNCTIONS[name]['title']}") for i, name in enumerate(preset_names)]
    options.append(("0", "Return to Graphing Menu"))

    while True:
        choice = display_menu("PRESET FUNCTIONS", options)
        if choice == "0":
            return

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(preset_names):
                name = preset_names[idx]
                info = PRESET_FUNCTIONS[name]
                fn = parse_function_expression(info["expr"])

                print(f"\nPreset: {name} ({info['title']})")
                print(f"Description: {info['description']}")
                override = input(f"Use preset domain [{info['x_min']}, {info['x_max']}]? (Y/n): ").strip().lower()

                if override == "n":
                    x_min_str = input(f"X-axis minimum (left edge) [{info['x_min']}]: ").strip()
                    x_max_str = input(f"X-axis maximum (right edge) [{info['x_max']}]: ").strip()
                    try:
                        x_min = float(x_min_str) if x_min_str else float(info["x_min"])
                        x_max = float(x_max_str) if x_max_str else float(info["x_max"])
                    except ValueError:
                        print(theme_manager.error("[Error] Invalid numeric value."))
                        input("\nPress ENTER to continue...")
                        continue
                else:
                    x_min, x_max = info["x_min"], info["x_max"]

                series = PlotSeries(fn=fn, label=info["title"], symbol="•", expr=info["expr"])
                plot_str = generate_ascii_plot(
                    series_input=series,
                    x_min=x_min,
                    x_max=x_max,
                    width=DEFAULT_PLOT_SETTINGS["width"],
                    height=DEFAULT_PLOT_SETTINGS["height"],
                    title=info["title"]
                )
                print("\n" + plot_str)
                input("\nPress ENTER to continue...")
                continue

        print("\n" + theme_manager.error("[Error] Invalid choice."))


def run_plot_settings_menu() -> None:
    """View and adjust default plot settings (domain, Y scaling, dimensions)."""
    while True:
        print("\n" + theme_manager.header("--- PLOT SETTINGS & DEFAULTS ---"))
        y_str = "Auto" if DEFAULT_PLOT_SETTINGS['y_min'] is None else f"[{DEFAULT_PLOT_SETTINGS['y_min']}, {DEFAULT_PLOT_SETTINGS['y_max']}]"
        print(f"1. Default X Domain : [{DEFAULT_PLOT_SETTINGS['x_min']}, {DEFAULT_PLOT_SETTINGS['x_max']}]")
        print(f"2. Default Y Range  : {y_str}")
        print(f"3. Plot Dimensions : {DEFAULT_PLOT_SETTINGS['width']} cols x {DEFAULT_PLOT_SETTINGS['height']} rows")
        print("0. Return to Graphing Menu")

        choice = input("\nSelect setting to modify (0-3): ").strip()
        if choice == "0":
            return
        elif choice == "1":
            try:
                xmin_s = input(f"Default X min [{DEFAULT_PLOT_SETTINGS['x_min']}]: ").strip()
                xmax_s = input(f"Default X max [{DEFAULT_PLOT_SETTINGS['x_max']}]: ").strip()
                if xmin_s:
                    DEFAULT_PLOT_SETTINGS["x_min"] = float(xmin_s)
                if xmax_s:
                    DEFAULT_PLOT_SETTINGS["x_max"] = float(xmax_s)
                print(theme_manager.ok("X domain updated."))
            except ValueError:
                print(theme_manager.error("[Error] Invalid numeric entry."))
        elif choice == "2":
            mode = input("Use (1) Automatic Y scaling or (2) Fixed Y range [1]: ").strip() or "1"
            if mode == "1":
                DEFAULT_PLOT_SETTINGS["y_min"] = None
                DEFAULT_PLOT_SETTINGS["y_max"] = None
                print(theme_manager.ok("Set Y range to automatic scaling."))
            else:
                try:
                    ymin_s = input("Enter default Y min: ").strip()
                    ymax_s = input("Enter default Y max: ").strip()
                    if ymin_s and ymax_s and float(ymin_s) < float(ymax_s):
                        DEFAULT_PLOT_SETTINGS["y_min"] = float(ymin_s)
                        DEFAULT_PLOT_SETTINGS["y_max"] = float(ymax_s)
                        print(theme_manager.ok("Fixed Y range updated."))
                    else:
                        print(theme_manager.error("[Error] Y min must be less than Y max."))
                except ValueError:
                    print(theme_manager.error("[Error] Invalid numeric entry."))
        elif choice == "3":
            try:
                w_s = input(f"Plot width (10-120) [{DEFAULT_PLOT_SETTINGS['width']}]: ").strip()
                h_s = input(f"Plot height (5-40) [{DEFAULT_PLOT_SETTINGS['height']}]: ").strip()
                if w_s:
                    DEFAULT_PLOT_SETTINGS["width"] = max(10, min(120, int(w_s)))
                if h_s:
                    DEFAULT_PLOT_SETTINGS["height"] = max(5, min(40, int(h_s)))
                print(theme_manager.ok("Plot dimensions updated."))
            except ValueError:
                print(theme_manager.error("[Error] Invalid integer entry."))
        else:
            print(theme_manager.error("[Error] Invalid choice."))


def run_graph_help_menu() -> None:
    """Display comprehensive graphing help and controls instructions."""
    print("\n" + theme_manager.header("--- GRAPH HELP & CONTROLS ---"))
    print("""
WORKSTATION CLI GRAPHING TOOL HELP:

1. Syntax & Expressions:
   - Variable: x (case-insensitive)
   - Powers: x^2 or x**2
   - Implicit Multiplication: 2x, 3sin(x), x(x+1)
   - Functions: sin, cos, tan, exp, log (ln), log10, sqrt, abs

2. Controls & Scaling:
   - X Domain: Controls visible left → right horizontal range sampled.
   - Y Range: Automatic scaling auto-detects min/max while filtering
     extreme asymptote spikes (e.g. 1/x). Custom Y range lets you fix
     vertical bounds.
   - Plot Size: Width and Height can be adjusted under Plot Settings.

3. Features:
   - Multi-series plotting support.
   - Asymptote and discontinuity handling (undefined points render blank).
   - Zero-axis markers ('┼', '│', '─').
""")
    input("Press ENTER to return to Graphing Menu...")


def run_graphing_menu() -> None:
    """Display the top-tier Graphing submenu per v0.0.6 specification."""
    navigation.push("Graphing")
    try:
        options = [
            ("1", "Plot Custom Function"),
            ("2", "Preset Functions"),
            ("3", "Plot Settings"),
            ("4", "Graph Help / Controls"),
            ("0", "Return to Main Menu"),
        ]
        handlers = {
            "1": run_custom_function_plot,
            "2": run_preset_functions_menu,
            "3": run_plot_settings_menu,
            "4": run_graph_help_menu,
        }

        while True:
            choice = display_menu("GRAPHING TOOL", options)
            if choice == "0":
                return
            handler = handlers.get(choice)
            if handler is None:
                print("\n" + theme_manager.error("[Error] Invalid selection. Please choose an option from the menu."))
                continue
            handler()
    finally:
        navigation.pop()
