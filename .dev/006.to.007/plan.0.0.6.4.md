# v0.0.6.4 — Graphing Enhancements & Polish

## Graphing Overhauls

### 0.0.6.4.a Advanced Multi-Series Plotting

Expand graphing to support **plotting multiple functions simultaneously** on the same axes.

- **User Interface**:
  - Add an option: `"5. Compare Multiple Functions"` to the Graphing menu.
  - Allow users to input 2–5 functions (e.g., `sin(x)` and `cos(x)`) with distinct symbols/colors.
  - Each function uses different Unicode symbols: `●`, `○`, `×`, `+`, `◆`.

- **Implementation**:
  - Extend `PlotSeries` to maintain individual series metadata (expression, label, symbol).
  - `generate_ascii_plot()` already supports `List[PlotSeries]`; expose this in the UI.
  - Share X/Y domain and plot size across all series.

### 0.0.6.4.b Preset Function Expansion

Add more mathematical functions and visualization templates.

**New Presets to Consider**:
- Polynomial families: quartic, quintic
- Trigonometric compositions: `sin(x) + cos(x)`, `sin(x*x)`
- Exponential decay: `exp(-x)`
- Damped oscillation: `exp(-x/10) * sin(x)`
- Piecewise functions: `abs(x)`, `|x - 2|`
- Rational functions: `(x^2 - 1) / (x^2 + 1)`

**Preset Organization**:
- Group presets by category: "Polynomial", "Trigonometric", "Exponential", "Special Functions"
- Add a **Preset Browser** that shows descriptions and thumbnail previews.

### 0.0.6.4.c Plot Export & Sharing

Allow users to export plots as **plain-text ASCII** or **image files** (if optional dependency available).

- **Minimal (v0.0.6.4)**:
  - Export to `.txt` with full plot and domain/range metadata.
  
- **Extended (future)**:
  - PNG export (optional; require `matplotlib` or similar).
  - SVG export for precise vector graphics.

### 0.0.6.4.d Derivative & Integral Visualization

Add visualization tools for calculus concepts.

- **Numerical Derivative Plot**: Display `f(x)` and `f'(x)` (numerical approximation) on the same graph.
- **Integral Visualization**: Shade area under the curve for a given domain range.

**Simple Implementation**:
```python
def plot_with_derivative(expr_str: str, x_min, x_max, dx=0.1):
    """Plot both f(x) and its numerical derivative."""
    fn = parse_function_expression(expr_str)
    
    def derivative(x):
        return (fn(x + dx/2) - fn(x - dx/2)) / dx
    
    series_fn = PlotSeries(fn, label=f"f(x) = {expr_str}", symbol="●")
    series_deriv = PlotSeries(derivative, label="f'(x)", symbol="◆")
    
    return generate_ascii_plot([series_fn, series_deriv], x_min, x_max)
```

### 0.0.6.4.e Graphing Help & Documentation Expansion

Enhance the `run_graph_help_menu()` with more detailed guidance.

- **Common Errors**: Explain asymptotes, discontinuities, and how the tool handles them.
- **Tips & Tricks**: Domain selection, Y-scaling for better visualization.
- **Interactive Tutorial**: Walk new users through plotting a simple function step-by-step.
