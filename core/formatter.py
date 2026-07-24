from typing import List, Dict, Any

def format_header(title: str, width: int = 50) -> str:
    line = "=" * width
    return f"\n{line}\n {title.center(width - 2)} \n{line}"

def format_table(headers: List[str], rows: List[List[Any]]) -> str:
    if not rows:
        return ""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    header_str = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    separator = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    
    row_strs = []
    for row in rows:
        row_strs.append(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))

    return f"{header_str}\n{separator}\n" + "\n".join(row_strs)
