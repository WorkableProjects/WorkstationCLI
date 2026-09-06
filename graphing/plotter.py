"""Graphing module evaluator and ASCII/Unicode plot renderer."""

import math
import re
from typing import Callable, Tuple, List, Optional, Dict, Any

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
    "Quadratic": {"expr": "x**2", "title": "f(x) = x²", "x_min": -5.0, "x_max": 5.0},
    "Cubic": {"expr": "x**3 - 3*x", "title": "f(x) = x³ - 3x", "x_min": -3.0, "x_max": 3.0},
    "Sine Wave": {"expr": "sin(x)", "title": "f(x) = sin(x)", "x_min": -6.28, "x_max": 6.28},
    "Cosine Wave": {"expr": "cos(x)", "title": "f(x) = cos(x)", "x_min": -6.28, "x_max": 6.28},
    "Gaussian": {"expr": "exp(-x**2)", "title": "f(x) = e^(-x²)", "x_min": -3.0, "x_max": 3.0},
    "Logarithmic": {"expr": "log(x)", "title": "f(x) = ln(x)", "x_min": 0.1, "x_max": 10.0},
    "Reciprocal": {"expr": "1/x", "title": "f(x) = 1/x", "x_min": -5.0, "x_max": 5.0},
}


def parse_function_expression(expression: str) -> Callable[[float], float]:
    """
    Parse a mathematical string expression into a single-variable callable f(x).
    Supports common math functions and syntax like x^2, 2x, sin(x), etc.
    """
    expr = expression.strip()
    if expr.lower().startswith("f(x)"):
        expr = expr.split("=", 1)[-1].strip()

    # Replace '^' with '**'
    expr = expr.replace('^', '**')

    # Support implicit multiplication like 2x -> 2*x, 3sin(x) -> 3*sin(x), x(x+1) -> x*(x+1)
    # Number followed by x or letter/parenthesis
    expr = re.sub(r'(\d)\s*([a-zA-Z\(])', r'\1*\2', expr)
    # x followed by number or (
    expr = re.sub(r'([xX])\s*(\d|\()', r'\1*\2', expr)

    # Validate characters safely
    # Allow math identifiers, numbers, spaces, operators, parentheses
    allowed_pattern = re.compile(r'^[0-9a-zA-Z\s\+\-\*\/\%\.\,\(\)]+$')
    if not allowed_pattern.match(expr):
        raise ValueError("Invalid characters in expression.")

    def fn(x: float) -> float:
        context = dict(SAFE_MATH_GLOBALS)
        context['x'] = float(x)
        context['X'] = float(x)
        try:
            val = eval(expr, {"__builtins__": None}, context)
            if isinstance(val, (int, float)):
                return float(val)
            raise ValueError("Expression did not return a numerical value.")
        except ZeroDivisionError:
            return float('nan')
        except ValueError:
            return float('nan')
        except Exception as e:
            raise ValueError(f"Evaluation error: {e}")

    # Test evaluation at x=1.0 to check syntax errors early
    fn(1.0)

    return fn


def generate_ascii_plot(
    fn: Callable[[float], float],
    x_min: float = -10.0,
    x_max: float = 10.0,
    y_min: Optional[float] = None,
    y_max: Optional[float] = None,
    width: int = 50,
    height: int = 20,
    title: str = "Function Plot"
) -> str:
    """
    Generates a terminal ASCII/Unicode graph for f(x).
    """
    if x_min >= x_max:
        raise ValueError("x_min must be less than x_max.")

    dx = (x_max - x_min) / float(width - 1)
    x_vals = [x_min + i * dx for i in range(width)]
    y_vals = []

    for x in x_vals:
        try:
            y = fn(x)
            if math.isnan(y) or math.isinf(y):
                y_vals.append(None)
            else:
                y_vals.append(y)
        except Exception:
            y_vals.append(None)

    valid_y = [y for y in y_vals if y is not None]
    if not valid_y:
        return "Cannot plot function: No valid values in the specified domain."

    if y_min is None:
        computed_y_min = min(valid_y)
    else:
        computed_y_min = float(y_min)

    if y_max is None:
        computed_y_max = max(valid_y)
    else:
        computed_y_max = float(y_max)

    if computed_y_min == computed_y_max:
        computed_y_min -= 1.0
        computed_y_max += 1.0

    dy = (computed_y_max - computed_y_min) / float(height - 1)

    # Canvas initialization with spaces
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    # Draw Axes
    # y-axis (x = 0)
    y_axis_col = None
    if x_min <= 0 <= x_max:
        y_axis_col = int(round((0.0 - x_min) / dx))
        if 0 <= y_axis_col < width:
            for r in range(height):
                grid[r][y_axis_col] = '│'

    # x-axis (y = 0)
    x_axis_row = None
    if computed_y_min <= 0 <= computed_y_max:
        x_axis_row = height - 1 - int(round((0.0 - computed_y_min) / dy))
        if 0 <= x_axis_row < height:
            for c in range(width):
                if grid[x_axis_row][c] == '│':
                    grid[x_axis_row][c] = '┼'
                else:
                    grid[x_axis_row][c] = '─'

    # Plot curve points
    for c in range(width):
        y = y_vals[c]
        if y is None:
            continue
        if computed_y_min <= y <= computed_y_max:
            r = height - 1 - int(round((y - computed_y_min) / dy))
            if 0 <= r < height:
                grid[r][c] = '•'

    # Build output string
    lines = []
    header_str = f"┌{'─' * (width + 2)}┐"
    lines.append(header_str)
    title_line = f"│ {title[:width].center(width)} │"
    lines.append(title_line)
    lines.append(f"├{'─' * (width + 2)}┤")

    for r in range(height):
        # Y label on top and bottom rows
        if r == 0:
            lbl = f"{computed_y_max:7.2f} │"
        elif r == height - 1:
            lbl = f"{computed_y_min:7.2f} │"
        else:
            lbl = "        │"
        row_str = "".join(grid[r])
        lines.append(f"{lbl}{row_str}│")

    lines.append(f"└{'─' * 8}┴{'─' * width}┘")
    x_lbl_str = f" x: {x_min:<8.2f}" + f"0.0".center(width - 20) + f"{x_max:>8.2f} "
    lines.append(f"         {x_lbl_str}")

    return "\n".join(lines)
