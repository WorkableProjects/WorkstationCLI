"""Unit tests for multi-series graphing, numerical derivative, numerical integral, and expanded presets."""

import math
from graphing.plotter import (
    parse_function_expression,
    generate_ascii_plot,
    PlotSeries,
    compute_numerical_derivative,
    compute_numerical_integral,
    PRESET_FUNCTIONS
)


def test_multi_series_symbol_and_legend():
    """Verify multiple functions render with distinct symbols and legend."""
    fn1 = parse_function_expression("sin(x)")
    fn2 = parse_function_expression("cos(x)")
    s1 = PlotSeries(fn=fn1, label="sin(x)", symbol="●")
    s2 = PlotSeries(fn=fn2, label="cos(x)", symbol="◆")

    plot_str = generate_ascii_plot([s1, s2], x_min=-3.14, x_max=3.14, title="Multi-Series Test")
    assert "[●] sin(x)" in plot_str
    assert "[◆] cos(x)" in plot_str
    assert "●" in plot_str
    assert "◆" in plot_str


def test_compute_numerical_derivative():
    """Verify numerical derivative accuracy for polynomials and trig functions."""
    fn_sq = parse_function_expression("x**2")
    deriv_sq = compute_numerical_derivative(fn_sq)
    # d/dx(x^2) = 2x -> at x=3, deriv = 6
    assert math.isclose(deriv_sq(3.0), 6.0, abs_tol=1e-3)

    fn_sin = parse_function_expression("sin(x)")
    deriv_sin = compute_numerical_derivative(fn_sin)
    # d/dx(sin(x)) = cos(x) -> at x=0, deriv = 1
    assert math.isclose(deriv_sin(0.0), 1.0, abs_tol=1e-3)


def test_compute_numerical_integral():
    """Verify numerical integral accuracy using Simpson's rule."""
    fn_constant = parse_function_expression("3")
    # ∫[0, 4] 3 dx = 12
    val_const = compute_numerical_integral(fn_constant, 0.0, 4.0)
    assert math.isclose(val_const, 12.0, abs_tol=1e-3)

    fn_x = parse_function_expression("x")
    # ∫[0, 2] x dx = [x^2 / 2] = 2
    val_x = compute_numerical_integral(fn_x, 0.0, 2.0)
    assert math.isclose(val_x, 2.0, abs_tol=1e-3)


def test_preset_categories():
    """Verify all 10+ preset functions have assigned categories and valid expressions."""
    assert len(PRESET_FUNCTIONS) >= 10
    categories = set()
    for name, info in PRESET_FUNCTIONS.items():
        assert "category" in info
        categories.add(info["category"])
        fn = parse_function_expression(info["expr"])
        assert callable(fn)

    assert "Polynomials" in categories
    assert "Trigonometric" in categories
    assert "Exponential & Logarithmic" in categories
    assert "Special Functions" in categories
