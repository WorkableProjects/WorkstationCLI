"""Graphing module evaluator, multi-series data model, and ASCII/Unicode plot renderer."""

import math
import re
from pathlib import Path
from typing import Callable, Tuple, List, Optional, Dict, Any, Union

SAFE_MATH_GLOBALS = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'sinh': math.sinh,
    'cosh': math.cosh,
    'tanh': math.tanh,
    'exp': math.exp,
    'log': math.log,
    'log10': math.log10,
    'sqrt': math.sqrt,
    'pi': math.pi,
    'e': math.e,
}

PRESET_FUNCTIONS: Dict[str, Dict[str, Any]] = {
    "Quadratic": {
        "category": "Polynomials",
        "expr": "x**2",
        "title": "f(x) = x²",
        "x_min": -5.0,
        "x_max": 5.0,
        "description": "Parabola opening upwards with vertex at origin."
    },
    "Cubic": {
        "category": "Polynomials",
        "expr": "x**3 - 3*x",
        "title": "f(x) = x³ - 3x",
        "x_min": -3.0,
        "x_max": 3.0,
        "description": "Polynomial with local maximum and minimum."
    },
    "Quartic": {
        "category": "Polynomials",
        "expr": "x**4 - 2*x**2",
        "title": "f(x) = x⁴ - 2x²",
        "x_min": -2.0,
        "x_max": 2.0,
        "description": "W-shaped polynomial with two local minima."
    },
    "Sine Wave": {
        "category": "Trigonometric",
        "expr": "sin(x)",
        "title": "f(x) = sin(x)",
        "x_min": -6.28,
        "x_max": 6.28,
        "description": "Periodic wave oscillating between -1 and 1."
    },
    "Cosine Wave": {
        "category": "Trigonometric",
        "expr": "cos(x)",
        "title": "f(x) = cos(x)",
        "x_min": -6.28,
        "x_max": 6.28,
        "description": "Periodic wave with peak at x = 0."
    },
    "Trig Superposition": {
        "category": "Trigonometric",
        "expr": "sin(x) + cos(x)",
        "title": "f(x) = sin(x) + cos(x)",
        "x_min": -6.28,
        "x_max": 6.28,
        "description": "Composite wave illustrating constructive/destructive interference."
    },
    "Damped Oscillation": {
        "category": "Trigonometric",
        "expr": "exp(-x/5) * sin(x)",
        "title": "f(x) = e^(-x/5) * sin(x)",
        "x_min": 0.0,
        "x_max": 20.0,
        "description": "Oscillating motion with exponential decay over time."
    },
    "Gaussian": {
        "category": "Exponential & Logarithmic",
        "expr": "exp(-x**2)",
        "title": "f(x) = e^(-x²)",
        "x_min": -3.0,
        "x_max": 3.0,
        "description": "Symmetric bell-shaped curve."
    },
    "Exponential Decay": {
        "category": "Exponential & Logarithmic",
        "expr": "exp(-x)",
        "title": "f(x) = e^(-x)",
        "x_min": -1.0,
        "x_max": 5.0,
        "description": "Standard exponential decay curve."
    },
    "Logarithmic": {
        "category": "Exponential & Logarithmic",
        "expr": "log(x)",
        "title": "f(x) = ln(x)",
        "x_min": 0.1,
        "x_max": 10.0,
        "description": "Natural logarithm defined for x > 0."
    },
    "Reciprocal": {
        "category": "Special Functions",
        "expr": "1/x",
        "title": "f(x) = 1/x",
        "x_min": -5.0,
        "x_max": 5.0,
        "description": "Hyperbola with vertical asymptote at x = 0."
    },
    "Absolute Value": {
        "category": "Special Functions",
        "expr": "abs(x)",
        "title": "f(x) = |x|",
        "x_min": -5.0,
        "x_max": 5.0,
        "description": "V-shaped continuous function with non-differentiable vertex at origin."
    },
    "Rational Function": {
        "category": "Special Functions",
        "expr": "(x**2 - 1) / (x**2 + 1)",
        "title": "f(x) = (x²-1)/(x²+1)",
        "x_min": -4.0,
        "x_max": 4.0,
        "description": "Smooth rational curve bounded between -1 and 1."
    }
}


class PlotSeries:
    """Represents a single mathematical function series for plotting."""

    def __init__(
        self,
        fn: Callable[[float], float],
        label: str = "f(x)",
        symbol: str = "•",
        expr: str = ""
    ):
        self.fn = fn
        self.label = label
        self.symbol = symbol
        self.expr = expr


def parse_function_expression(expression: str) -> Callable[[float], float]:
    """
    Parse a mathematical string expression into a single-variable callable f(x).
    Supports common math functions and syntax like x^2, 2x, sin(x), etc.
    """
    expr = expression.strip()
    if expr.lower().startswith("f(x)"):
        expr = expr.split("=", 1)[-1].strip()

    expr = expr.replace('^', '**')

    # Implicit multiplication like 2x -> 2*x, 3sin(x) -> 3*sin(x), x(x+1) -> x*(x+1)
    expr = re.sub(r'(\d)\s*([a-zA-Z\(])', r'\1*\2', expr)
    expr = re.sub(r'([xX])\s*(\d|\()', r'\1*\2', expr)

    allowed_pattern = re.compile(r'^[0-9a-zA-Z\s\+\-\*\/\%\.\,\(\)]+$')
    if not allowed_pattern.match(expr):
        raise ValueError("Invalid characters in expression.")

    def fn(x: float) -> float:
        context = dict(SAFE_MATH_GLOBALS)
        context['x'] = float(x)
        context['X'] = float(x)
        try:
            val = eval(expr, {"__builtins__": None}, context)
            if isinstance(val, (int, float, complex)):
                if isinstance(val, complex):
                    if abs(val.imag) < 1e-12:
                        val = val.real
                    else:
                        return float('nan')
                if math.isnan(val) or math.isinf(val):
                    return float('nan')
                return float(val)
            raise ValueError("Expression did not return a numerical value.")
        except (ZeroDivisionError, ValueError, OverflowError):
            return float('nan')
        except Exception as e:
            raise ValueError(f"Evaluation error: {e}")

    # Verify expression structure by evaluating at a test point
    try:
        fn(1.0)
    except Exception:
        # Retry test evaluation at x=2.0 (in case x=1 was domain boundary)
        try:
            fn(2.0)
        except Exception as err:
            raise ValueError(f"Expression evaluation failed: {err}")

    return fn


def generate_ascii_plot(
    series_input: Union[Callable[[float], float], PlotSeries, List[PlotSeries]],
    x_min: float = -10.0,
    x_max: float = 10.0,
    y_min: Optional[float] = None,
    y_max: Optional[float] = None,
    width: int = 50,
    height: int = 20,
    title: str = "Function Plot"
) -> str:
    """
    Generates a terminal ASCII/Unicode plot for one or more mathematical series.
    """
    if x_min >= x_max:
        raise ValueError("x_min (left edge) must be less than x_max (right edge).")
    if width < 10 or height < 5:
        raise ValueError("Plot size width must be >= 10 and height >= 5.")

    # Normalize series_input into List[PlotSeries]
    series_list: List[PlotSeries] = []
    if isinstance(series_input, list):
        series_list = series_input
    elif isinstance(series_input, PlotSeries):
        series_list = [series_input]
    elif callable(series_input):
        series_list = [PlotSeries(fn=series_input, label=title, symbol="•")]
    else:
        raise TypeError("Invalid series input provided to generate_ascii_plot.")

    dx = (x_max - x_min) / float(width - 1)
    x_vals = [x_min + i * dx for i in range(width)]

    # Sample each series
    sampled_data: List[List[Optional[float]]] = []
    all_valid_y: List[float] = []

    for series in series_list:
        y_vals: List[Optional[float]] = []
        for x in x_vals:
            try:
                y = series.fn(x)
                if y is None or math.isnan(y) or math.isinf(y):
                    y_vals.append(None)
                else:
                    y_vals.append(y)
                    all_valid_y.append(y)
            except Exception:
                y_vals.append(None)
        sampled_data.append(y_vals)

    if not all_valid_y:
        return f"Cannot plot function: No valid values in domain [{x_min:.2f}, {x_max:.2f}]."

    # Compute Y Range
    if y_min is None:
        # Outlier filtering for auto scaling near asymptotes (e.g. 1/x near 0)
        sorted_y = sorted(all_valid_y)
        if len(sorted_y) > 4:
            q1_idx = len(sorted_y) // 4
            q3_idx = (3 * len(sorted_y)) // 4
            q1, q3 = sorted_y[q1_idx], sorted_y[q3_idx]
            iqr = q3 - q1
            if iqr > 0:
                filtered = [y for y in sorted_y if (q1 - 3 * iqr) <= y <= (q3 + 3 * iqr)]
                computed_y_min = min(filtered) if filtered else min(all_valid_y)
            else:
                computed_y_min = min(all_valid_y)
        else:
            computed_y_min = min(all_valid_y)
    else:
        computed_y_min = float(y_min)

    if y_max is None:
        sorted_y = sorted(all_valid_y)
        if len(sorted_y) > 4:
            q1_idx = len(sorted_y) // 4
            q3_idx = (3 * len(sorted_y)) // 4
            q1, q3 = sorted_y[q1_idx], sorted_y[q3_idx]
            iqr = q3 - q1
            if iqr > 0:
                filtered = [y for y in sorted_y if (q1 - 3 * iqr) <= y <= (q3 + 3 * iqr)]
                computed_y_max = max(filtered) if filtered else max(all_valid_y)
            else:
                computed_y_max = max(all_valid_y)
        else:
            computed_y_max = max(all_valid_y)
    else:
        computed_y_max = float(y_max)

    if computed_y_min >= computed_y_max:
        computed_y_min -= 1.0
        computed_y_max += 1.0

    dy = (computed_y_max - computed_y_min) / float(height - 1)

    # Canvas initialization
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    # Draw Axes
    # y-axis (x = 0)
    if x_min <= 0 <= x_max:
        y_axis_col = int(round((0.0 - x_min) / dx))
        if 0 <= y_axis_col < width:
            for r in range(height):
                grid[r][y_axis_col] = '│'

    # x-axis (y = 0)
    if computed_y_min <= 0 <= computed_y_max:
        x_axis_row = height - 1 - int(round((0.0 - computed_y_min) / dy))
        if 0 <= x_axis_row < height:
            for c in range(width):
                if grid[x_axis_row][c] == '│':
                    grid[x_axis_row][c] = '┼'
                else:
                    grid[x_axis_row][c] = '─'

    # Plot curve points for each series
    for s_idx, series in enumerate(series_list):
        y_vals = sampled_data[s_idx]
        sym = series.symbol or "•"
        for c in range(width):
            y = y_vals[c]
            if y is None:
                continue
            if computed_y_min <= y <= computed_y_max:
                r = height - 1 - int(round((y - computed_y_min) / dy))
                if 0 <= r < height:
                    grid[r][c] = sym

    # Build formatted output
    lines = []
    box_width = width + 2
    lines.append(f"┌{'─' * box_width}┐")
    lines.append(f"│ {title[:width].center(width)} │")

    # Series Legend if multiple
    if len(series_list) > 1:
        legend_str = " ".join(f"[{s.symbol}] {s.label}" for s in series_list)
        lines.append(f"│ {legend_str[:width].center(width)} │")

    lines.append(f"├{'─' * box_width}┤")

    for r in range(height):
        if r == 0:
            lbl = f"{computed_y_max:7.2f} │"
        elif r == height - 1:
            lbl = f"{computed_y_min:7.2f} │"
        else:
            lbl = "        │"
        row_str = "".join(grid[r])
        lines.append(f"{lbl}{row_str}│")

    lines.append(f"└{'─' * 8}┴{'─' * width}┘")

    # X-axis label with endpoint values and center 0.0 marker
    if x_min <= 0 <= x_max:
        center_lbl = "0.0"
    else:
        center_lbl = f"{(x_min + x_max)/2.0:.1f}"

    x_lbl_str = f" x: {x_min:<8.2f}" + center_lbl.center(max(1, width - 20)) + f"{x_max:>8.2f} "
    lines.append(f"         {x_lbl_str}")

    # Domain & Range Summary Footer
    summary = f" Domain: x ∈ [{x_min:.2f}, {x_max:.2f}] | Range: y ∈ [{computed_y_min:.2f}, {computed_y_max:.2f}] | Size: {width}x{height}"
    lines.append(f" {summary}")

    return "\n".join(lines)


def export_plot_to_file(plot_str: str, filepath: Optional[str] = None) -> str:
    """Save plot ASCII text and metadata to a text file."""
    if not filepath:
        import time
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filepath = f"plot_export_{timestamp}.txt"
    path = Path(filepath)
    path.write_text(plot_str, encoding="utf-8")
    return str(path.resolve())


def compute_numerical_derivative(
    fn: Callable[[float], float],
    dx: float = 1e-5
) -> Callable[[float], float]:
    """Return a callable representing the numerical derivative f'(x) via central difference."""
    def derivative(x: float) -> float:
        try:
            f_plus = fn(x + dx / 2.0)
            f_minus = fn(x - dx / 2.0)
            if math.isnan(f_plus) or math.isnan(f_minus):
                return float('nan')
            return (f_plus - f_minus) / dx
        except Exception:
            return float('nan')
    return derivative


def compute_numerical_integral(
    fn: Callable[[float], float],
    a: float,
    b: float,
    n: int = 1000
) -> float:
    """Compute numerical definite integral of f(x) from a to b using Simpson's Rule."""
    if a == b:
        return 0.0
    if n % 2 != 0:
        n += 1  # Simpson's rule requires even n

    h = (b - a) / float(n)
    total = 0.0

    try:
        fa = fn(a)
        fb = fn(b)
        if math.isnan(fa) or math.isnan(fb):
            return float('nan')
        total = fa + fb

        for i in range(1, n):
            x = a + i * h
            val = fn(x)
            if math.isnan(val):
                return float('nan')
            coefficient = 4.0 if i % 2 != 0 else 2.0
            total += coefficient * val

        return (h / 3.0) * total
    except Exception:
        return float('nan')
