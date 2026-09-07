"""Unit tests for the Graphing module plotter, multi-series support, and expression parser."""

import math
import pytest
from graphing.plotter import (
    parse_function_expression,
    generate_ascii_plot,
    PRESET_FUNCTIONS,
    PlotSeries
)


def test_parse_function_expression_polynomial():
    fn = parse_function_expression("x^2 + 2*x + 1")
    assert fn(0) == 1.0
    assert fn(2) == 9.0
    assert fn(-1) == 0.0


def test_parse_function_expression_implicit_mult():
    fn = parse_function_expression("2x - 3")
    assert fn(4) == 5.0

    fn2 = parse_function_expression("3sin(x)")
    assert math.isclose(fn2(math.pi / 2), 3.0)


def test_parse_function_expression_f_of_x():
    fn = parse_function_expression("f(x) = x^3 - 3*x")
    assert fn(0) == 0.0
    assert fn(2) == 2.0


def test_parse_function_expression_invalid_syntax():
    with pytest.raises(Exception):
        parse_function_expression("import os; os.system('ls')")


def test_generate_ascii_plot():
    fn = parse_function_expression("x^2")
    plot_output = generate_ascii_plot(fn, x_min=-2.0, x_max=2.0, width=40, height=15, title="f(x) = x^2")

    assert "f(x) = x^2" in plot_output
    assert "│" in plot_output
    assert "─" in plot_output
    assert "•" in plot_output
    assert "Domain:" in plot_output


def test_preset_functions():
    assert "Quadratic" in PRESET_FUNCTIONS
    for name, info in PRESET_FUNCTIONS.items():
        fn = parse_function_expression(info["expr"])
        plot_output = generate_ascii_plot(fn, x_min=info["x_min"], x_max=info["x_max"])
        assert len(plot_output) > 0


def test_multi_series_plotting():
    fn1 = parse_function_expression("sin(x)")
    fn2 = parse_function_expression("cos(x)")
    s1 = PlotSeries(fn=fn1, label="sin", symbol="S")
    s2 = PlotSeries(fn=fn2, label="cos", symbol="C")

    plot_output = generate_ascii_plot([s1, s2], x_min=-3.14, x_max=3.14, title="Trig Comparison")
    assert "Trig Comparison" in plot_output
    assert "[S] sin" in plot_output
    assert "[C] cos" in plot_output
    assert "S" in plot_output
    assert "C" in plot_output


def test_discontinuity_and_asymptote_handling():
    fn_reciprocal = parse_function_expression("1/x")
    # Should not crash on division by zero at x=0
    plot_output = generate_ascii_plot(fn_reciprocal, x_min=-5.0, x_max=5.0)
    assert "Domain:" in plot_output

    fn_log = parse_function_expression("log(x)")
    # x <= 0 returns nan/undefined, should render available positive domain
    plot_output_log = generate_ascii_plot(fn_log, x_min=-2.0, x_max=5.0)
    assert "Domain:" in plot_output_log


def test_custom_y_scaling_bounds():
    fn = parse_function_expression("x")
    plot_output = generate_ascii_plot(fn, x_min=-5.0, x_max=5.0, y_min=-10.0, y_max=10.0)
    assert "10.00" in plot_output
    assert "-10.00" in plot_output
