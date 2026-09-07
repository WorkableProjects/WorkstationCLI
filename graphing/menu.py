"""Graphing menu router, preset library, and plot configuration manager."""

import math
from typing import Optional, Dict, Any, List, Tuple
from core.menu import display_menu
from core import navigation, theme_manager, help as helpmod
from graphing.plotter import (
    parse_function_expression,
    generate_ascii_plot,
    PRESET_FUNCTIONS,
    PlotSeries,
    export_plot_to_file,
    compute_numerical_derivative,
    compute_numerical_integral
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
        _prompt_plot_export(plot_str)
    except Exception as e:
        print(theme_manager.error(f"[Error] Failed to render plot: {e}"))

    input("\nPress ENTER to return to Graphing Menu...")


def _prompt_plot_export(plot_str: str) -> None:
    """Prompt user if they want to export the rendered plot to a text file."""
    exp_choice = input("\nExport plot to plain text file? (y/N): ").strip().lower()
    if exp_choice in ("y", "yes"):
        filename = input("Enter filename [auto-generated]: ").strip() or None
        try:
            saved_path = export_plot_to_file(plot_str, filename)
            print(theme_manager.ok(f"✓ Plot saved successfully to: {saved_path}"))
        except Exception as err:
            print(theme_manager.error(f"[Error] Failed to export plot: {err}"))


MULTI_SERIES_SYMBOLS = ["●", "○", "×", "+", "◆"]


def run_multi_series_plot() -> None:
    """Prompt user for 2-5 functions and plot them simultaneously on shared axes."""
    print("\n" + theme_manager.header("--- Multi-Series Function Plotter ---"))
    print("Enter between 2 and 5 functions to plot on the same axes.")
    print("Examples: f1(x) = sin(x), f2(x) = cos(x)")

    count_str = input("\nHow many functions to compare (2-5) [2]: ").strip() or "2"
    try:
        count = int(count_str)
        if count < 2 or count > 5:
            print(theme_manager.error("[Error] Number of functions must be between 2 and 5."))
            input("\nPress ENTER to continue...")
            return
    except ValueError:
        print(theme_manager.error("[Error] Invalid integer choice."))
        input("\nPress ENTER to continue...")
        return

    series_list: List[PlotSeries] = []
    for i in range(count):
        sym = MULTI_SERIES_SYMBOLS[i % len(MULTI_SERIES_SYMBOLS)]
        expr_str = input(f"Enter expression for function #{i+1} [{sym}]: ").strip()
        if not expr_str:
            print(theme_manager.warn("Expression skipped or cancelled."))
            return
        try:
            fn = parse_function_expression(expr_str)
            series_list.append(PlotSeries(fn=fn, label=f"f{i+1}(x) = {expr_str}", symbol=sym, expr=expr_str))
        except Exception as e:
            print(theme_manager.error(f"[Error] Invalid expression for function #{i+1}: {e}"))
            input("\nPress ENTER to continue...")
            return

    # Domain Controls
    print("\n" + theme_manager.colorize("--- Domain Configuration (X Range) ---", "header"))
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

    try:
        plot_str = generate_ascii_plot(
            series_input=series_list,
            x_min=x_min,
            x_max=x_max,
            width=DEFAULT_PLOT_SETTINGS["width"],
            height=DEFAULT_PLOT_SETTINGS["height"],
            title="Multi-Series Function Comparison"
        )
        print("\n" + plot_str)
        _prompt_plot_export(plot_str)
    except Exception as e:
        print(theme_manager.error(f"[Error] Failed to render multi-series plot: {e}"))

    input("\nPress ENTER to return to Graphing Menu...")


def run_derivative_plot() -> None:
    """Plot function f(x) and its numerical derivative f'(x) together."""
    print("\n" + theme_manager.header("--- Numerical Derivative Plotter ---"))
    print("Displays f(x) [●] and its numerical derivative f'(x) [◆] on the same axes.")
    expr_str = input("\nEnter function f(x): ").strip()
    if not expr_str:
        print(theme_manager.warn("No expression entered. Returning..."))
        return

    try:
        fn = parse_function_expression(expr_str)
        deriv_fn = compute_numerical_derivative(fn)
    except Exception as e:
        print(theme_manager.error(f"\n[Error] Invalid expression: {e}"))
        input("\nPress ENTER to continue...")
        return

    print("\n" + theme_manager.colorize("--- Domain Configuration (X Range) ---", "header"))
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

    series_fn = PlotSeries(fn=fn, label=f"f(x) = {expr_str}", symbol="●", expr=expr_str)
    series_deriv = PlotSeries(fn=deriv_fn, label="f'(x) [Derivative]", symbol="◆")

    try:
        plot_str = generate_ascii_plot(
            series_input=[series_fn, series_deriv],
            x_min=x_min,
            x_max=x_max,
            width=DEFAULT_PLOT_SETTINGS["width"],
            height=DEFAULT_PLOT_SETTINGS["height"],
            title=f"f(x) = {expr_str} and Derivative f'(x)"
        )
        print("\n" + plot_str)
        _prompt_plot_export(plot_str)
    except Exception as e:
        print(theme_manager.error(f"[Error] Failed to render derivative plot: {e}"))

    input("\nPress ENTER to return to Graphing Menu...")


def run_integral_plot() -> None:
    """Compute numerical definite integral of f(x) over [a, b] and display with plot."""
    print("\n" + theme_manager.header("--- Definite Integral Calculator & Visualizer ---"))
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

    print("\n" + theme_manager.colorize("--- Integration Bounds ---", "header"))
    a_str = input("Lower bound (a) [0]: ").strip() or "0"
    b_str = input("Upper bound (b) [5]: ").strip() or "5"

    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError:
        print(theme_manager.error("[Error] Invalid numeric value for bounds."))
        input("\nPress ENTER to continue...")
        return

    integral_val = compute_numerical_integral(fn, a, b)

    if math.isnan(integral_val):
        print(theme_manager.error(f"\nCould not compute integral: Function has undefined values in interval [{a}, {b}]."))
    else:
        print("\n" + "=" * 50)
        print(theme_manager.ok("  Definite Integral Result:"))
        print(f"  ∫[{a:.2f}, {b:.2f}] ({expr_str}) dx ≈ {integral_val:.6f}")
        print("=" * 50)

    # Plot on bounds
    x_min = min(a, b) - 1.0 if a != b else a - 5.0
    x_max = max(a, b) + 1.0 if a != b else a + 5.0

    try:
        series = PlotSeries(fn=fn, label=f"f(x) = {expr_str}", symbol="•", expr=expr_str)
        title_str = f"∫[{a:.2f}, {b:.2f}] f(x) dx ≈ {integral_val:.4f}" if not math.isnan(integral_val) else f"f(x) = {expr_str}"
        plot_str = generate_ascii_plot(
            series_input=series,
            x_min=x_min,
            x_max=x_max,
            width=DEFAULT_PLOT_SETTINGS["width"],
            height=DEFAULT_PLOT_SETTINGS["height"],
            title=title_str
        )
        print("\n" + plot_str)
        _prompt_plot_export(plot_str)
    except Exception as e:
        print(theme_manager.error(f"[Error] Failed to render plot: {e}"))

    input("\nPress ENTER to return to Graphing Menu...")


def run_preset_functions_menu() -> None:
    """Select and plot preset common mathematical functions grouped by category."""
    categories: Dict[str, List[Tuple[str, Dict[str, Any]]]] = {}
    for name, info in PRESET_FUNCTIONS.items():
        cat = info.get("category", "General")
        categories.setdefault(cat, []).append((name, info))

    while True:
        cat_list = list(categories.keys())
        options = [(str(i + 1), cat_name) for i, cat_name in enumerate(cat_list)]
        options.append(("0", "Return to Graphing Menu"))

        choice = display_menu("PRESET CATEGORIES", options)
        if choice == "0":
            return

        if choice.isdigit():
            c_idx = int(choice) - 1
            if 0 <= c_idx < len(cat_list):
                selected_cat = cat_list[c_idx]
                preset_items = categories[selected_cat]

                sub_options = [(str(j + 1), f"{p_name} — {p_info['title']}") for j, (p_name, p_info) in enumerate(preset_items)]
                sub_options.append(("0", "Back to Preset Categories"))

                while True:
                    sub_choice = display_menu(f"PRESETS: {selected_cat.upper()}", sub_options)
                    if sub_choice == "0":
                        break

                    if sub_choice.isdigit():
                        p_idx = int(sub_choice) - 1
                        if 0 <= p_idx < len(preset_items):
                            name, info = preset_items[p_idx]
                            fn = parse_function_expression(info["expr"])

                            print(f"\nPreset: {name} ({info['title']})")
                            print(f"Category: {selected_cat}")
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
    """Display comprehensive graphing help, calculus tools, and export instructions."""
    print("\n" + theme_manager.header("--- GRAPH HELP & DOCUMENTATION ---"))
    print("""
WORKSTATION CLI GRAPHING TOOL HELP:

1. Syntax & Expressions:
   - Variable: x (case-insensitive)
   - Powers: x^2 or x**2
   - Implicit Multiplication: 2x, 3sin(x), x(x+1)
   - Functions: sin, cos, tan, exp, log (ln), log10, sqrt, abs

2. Multi-Series Plotting:
   - Compare 2 to 5 functions simultaneously on shared axes.
   - Distinct symbols (●, ○, ×, +, ◆) with formatted legend.

3. Calculus Tools:
   - Numerical Derivative Plot: Displays f(x) and f'(x) together on graph.
   - Definite Integral: Computes ∫[a, b] f(x) dx via Simpson's rule.

4. Exporting Plots:
   - Save rendered plots to plain-text (.txt) files.
   - Includes title, expressions, domain, range, and size metadata.

5. Domain & Asymptotes:
   - Automatic outlier filtering prevents extreme asymptote spikes (e.g. 1/x).
   - Undefined domain points (NaN / Inf) render as clean blank spaces.
""")
    input("Press ENTER to return to Graphing Menu...")


def run_graphing_menu() -> None:
    """Display the top-tier Graphing submenu per v0.0.6 specification."""
    navigation.push("Graphing")
    try:
        options = [
            ("1", "Plot Custom Function"),
            ("2", "Compare Multiple Functions"),
            ("3", "Numerical Derivative Plot"),
            ("4", "Definite Integral Calculation"),
            ("5", "Preset Functions Library"),
            ("6", "Plot Settings"),
            ("7", "Graph Help / Documentation"),
            ("0", "Return to Main Menu"),
        ]
        handlers = {
            "1": run_custom_function_plot,
            "2": run_multi_series_plot,
            "3": run_derivative_plot,
            "4": run_integral_plot,
            "5": run_preset_functions_menu,
            "6": run_plot_settings_menu,
            "7": run_graph_help_menu,
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
