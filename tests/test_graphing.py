"""Unit tests for the Graphing module plotter and expression parser."""

import math
import pytest
from graphing.plotter import parse_function_expression, generate_ascii_plot, PRESET_FUNCTIONS


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


def test_preset_functions():
    assert "Quadratic" in PRESET_FUNCTIONS
    for name, info in PRESET_FUNCTIONS.items():
        fn = parse_function_expression(info["expr"])
        plot_output = generate_ascii_plot(fn, x_min=info["x_min"], x_max=info["x_max"])
        assert len(plot_output) > 0
