"""Formatters for CLI output: headers, tables, with theme support."""

from typing import List, Dict, Any

def format_header(title: str, width: int = 50) -> str:
    """Format a header section with theme colors."""
    from core import theme_manager
    line = "=" * width
    colored_line = theme_manager.colorize(line, "header")
    colored_title = theme_manager.colorize(title, "header")
    return f"\n{colored_line}\n {colored_title.center(width - 2)} \n{colored_line}"

def format_table(headers: List[str], rows: List[List[Any]]) -> str:
    """Format a table with theme colors."""
    from core import theme_manager
    if not rows:
        return ""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    header_str = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    colored_header = theme_manager.colorize(header_str, "header")
    separator = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    
    row_strs = []
    for row in rows:
        row_strs.append(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))

    return f"{colored_header}\n{separator}\n" + "\n".join(row_strs)
