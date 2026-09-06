"""Graphing menu router for function plotting and visual options."""

from typing import Optional
from core.menu import display_menu
from core import navigation, theme_manager
from graphing.plotter import parse_function_expression, generate_ascii_plot, PRESET_FUNCTIONS


def run_custom_function_plot() -> None:
    """Prompt user for custom mathematical function and plot it."""
    print("\n" + theme_manager.header("--- Custom Function Plotter ---"))
    print("Examples: x^2, sin(x), 2*x + 1, exp(-x^2), x^3 - 3*x")
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

    # Domain settings
    x_min_str = input("Enter x min [-10.0]: ").strip()
    x_max_str = input("Enter x max [10.0]: ").strip()

    try:
        x_min = float(x_min_str) if x_min_str else -10.0
        x_max = float(x_max_str) if x_max_str else 10.0
    except ValueError:
        print(theme_manager.error("[Error] Invalid numeric value for domain bounds."))
        input("\nPress ENTER to continue...")
        return

    if x_min >= x_max:
        print(theme_manager.error("[Error] Minimum x must be less than maximum x."))
        input("\nPress ENTER to continue...")
        return

    try:
        plot_str = generate_ascii_plot(fn, x_min=x_min, x_max=x_max, title=f"f(x) = {expr_str}")
        print("\n" + plot_str)
    except Exception as e:
        print(theme_manager.error(f"[Error] Failed to render plot: {e}"))

    input("\nPress ENTER to return to Graphing Menu...")


def run_preset_functions_menu() -> None:
    """Select and visualize preset common mathematical functions."""
    preset_names = list(PRESET_FUNCTIONS.keys())
    options = [(str(i + 1), name) for i, name in enumerate(preset_names)]
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
                plot_str = generate_ascii_plot(
                    fn,
                    x_min=info["x_min"],
                    x_max=info["x_max"],
                    title=info["title"]
                )
                print("\n" + plot_str)
                input("\nPress ENTER to continue...")
                continue

        print("\n" + theme_manager.error("[Error] Invalid choice."))


def run_graphing_menu() -> None:
    """Display the top-tier Graphing submenu."""
    navigation.push("Graphing")
    try:
        options = [
            ("1", "Plot Custom Function f(x)"),
            ("2", "Preset Common Functions"),
            ("0", "Return to Main Menu"),
        ]
        handlers = {
            "1": run_custom_function_plot,
            "2": run_preset_functions_menu,
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
