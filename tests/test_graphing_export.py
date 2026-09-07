"""Unit tests for plot text file export functionality."""

import os
import tempfile
from pathlib import Path
from graphing.plotter import export_plot_to_file, generate_ascii_plot, parse_function_expression


def test_export_plot_to_file(tmp_path):
    """Verify plot ASCII text is exported accurately to a text file."""
    fn = parse_function_expression("x**2")
    plot_str = generate_ascii_plot(fn, x_min=-2.0, x_max=2.0, title="Test Export Plot")

    export_path = tmp_path / "test_export.txt"
    saved_file = export_plot_to_file(plot_str, str(export_path))

    assert os.path.exists(saved_file)
    content = Path(saved_file).read_text(encoding="utf-8")
    assert "Test Export Plot" in content
    assert "Domain:" in content
    assert "Range:" in content
