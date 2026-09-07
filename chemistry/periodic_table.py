"""Canonical Periodic Table domain model, lookup engine, grid layout, and interactive viewer."""

from typing import Dict, Any, Optional, Tuple, List
from utils.parser import load_periodic_table
from core.ui import GridSelector, DetailPanel
from core import theme_manager

# 18-Group x 10-Row Matrix Layout for 118 Elements
# Rows 0-6: Periods 1-7
# Row 7: Blank separator
# Rows 8-9: Lanthanides (57-71) and Actinides (89-103)

PERIODIC_TABLE_GRID: List[List[Optional[str]]] = [
    # Period 1
    ["H", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "He"],
    # Period 2
    ["Li", "Be", None, None, None, None, None, None, None, None, None, None, "B", "C", "N", "O", "F", "Ne"],
    # Period 3
    ["Na", "Mg", None, None, None, None, None, None, None, None, None, None, "Al", "Si", "P", "S", "Cl", "Ar"],
    # Period 4
    ["K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr"],
    # Period 5
    ["Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe"],
    # Period 6 (La-Lu detached below)
    ["Cs", "Ba", None, "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn"],
    # Period 7 (Ac-Lr detached below)
    ["Fr", "Ra", None, "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"],
    # Separator
    [None] * 18,
    # Lanthanides (57-71)
    [None, None, None, "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"],
    # Actinides (89-103)
    [None, None, None, "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr"],
]


def find_element(query: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    """
    Canonical element lookup.
    Searches by symbol (exact or case-insensitive), element name, or atomic number.
    Returns (symbol, element_data) or None.
    """
    if not query:
        return None
    pt = load_periodic_table()
    q = query.strip().lower()

    if query.strip() in pt:
        return query.strip(), pt[query.strip()]

    for symbol, data in pt.items():
        if (
            symbol.lower() == q
            or data.get("name", "").lower() == q
            or (q.isdigit() and int(q) == data.get("number"))
            or (str(data.get("number")) == q)
        ):
            return symbol, data

    return None


def find_grid_coordinates(query: str, items_dict: Dict[str, Any]) -> Optional[Tuple[int, int]]:
    """Locate grid row and column coordinates for a given search query."""
    res = find_element(query)
    if not res:
        return None
    target_symbol, _ = res

    for r_idx, row in enumerate(PERIODIC_TABLE_GRID):
        for c_idx, sym in enumerate(row):
            if sym == target_symbol:
                return r_idx, c_idx
    return None


def get_shell_summary(electron_config: str, atomic_number: int) -> Dict[int, int]:
    """Derive principal energy level (shell n=1..7) electron counts from configuration."""
    if not electron_config:
        return {}

    noble_cores = {
        "[He]": "1s2",
        "[Ne]": "1s2 2s2 2p6",
        "[Ar]": "1s2 2s2 2p6 3s2 3p6",
        "[Kr]": "1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6",
        "[Xe]": "1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6",
        "[Rn]": "1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6 6s2 4f14 5d10 6p6",
    }

    full_cfg = electron_config
    for core, expanded in noble_cores.items():
        if core in full_cfg:
            full_cfg = full_cfg.replace(core, expanded)

    shells: Dict[int, int] = {}
    tokens = full_cfg.split()
    for token in tokens:
        if len(token) >= 3 and token[0].isdigit():
            n = int(token[0])
            count_str = token[2:]
            if count_str.isdigit():
                shells[n] = shells.get(n, 0) + int(count_str)

    return shells


def format_subshell_display(subshell_str: str) -> str:
    """Format subshell notation e.g. 1s2 -> 1s²."""
    superscripts = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '10': '¹⁰',
        '11': '¹¹', '12': '¹²', '13': '¹³', '14': '¹⁴'
    }
    result = []
    tokens = subshell_str.split()
    for t in tokens:
        if t.startswith("[") and t.endswith("]"):
            result.append(t)
            continue
        for digits, sup in sorted(superscripts.items(), key=lambda x: -len(x[0])):
            if t.endswith(digits):
                base = t[:-len(digits)]
                result.append(f"{base}{sup}")
                break
        else:
            result.append(t)
    return " ".join(result)


def format_element_detail(symbol: str, data: Dict[str, Any]) -> str:
    """Format structured element detail view."""
    def val_or_na(val: Any) -> str:
        if val is None or val == "" or val == "N/A":
            return "N/A"
        return str(val)

    name = val_or_na(data.get("name"))
    number = val_or_na(data.get("number"))
    mass = f"{data.get('mass')} g/mol" if data.get("mass") is not None else "N/A"
    category = val_or_na(data.get("category")).title()
    period = val_or_na(data.get("period"))
    group = val_or_na(data.get("group"))
    block = val_or_na(data.get("block"))
    state = val_or_na(data.get("state"))
    phase = val_or_na(data.get("phase"))
    electronegativity = val_or_na(data.get("electronegativity"))
    valence = val_or_na(data.get("valence_electrons"))
    oxidation = val_or_na(data.get("oxidation_states"))
    ec_raw = val_or_na(data.get("electron_configuration"))
    ec_formatted = format_subshell_display(ec_raw) if ec_raw != "N/A" else "N/A"

    shells = get_shell_summary(data.get("electron_configuration", ""), data.get("number", 0))
    shell_str = " / ".join(f"n={n}: {count}e⁻" for n, count in sorted(shells.items())) if shells else "N/A"

    header_title = f"{name.upper()} ({symbol}) — ELEMENT DETAILS"
    line = "=" * 60
    colored_line = theme_manager.colorize(line, "header")
    colored_title = theme_manager.colorize(header_title, "header")

    lines = [
        colored_line,
        f" {colored_title.center(58)} ",
        colored_line,
        f"  Symbol             : {symbol}",
        f"  Name               : {name}",
        f"  Atomic Number      : {number}",
        f"  Atomic Mass        : {mass}",
        f"  Category           : {category}",
        f"  Period / Group     : Period {period}, Group {group}",
        f"  Block              : {block}-block",
        f"  State (Room Temp)  : {state} ({phase})",
        f"  Electronegativity  : {electronegativity}",
        f"  Valence Electrons  : {valence}",
        f"  Oxidation States   : {oxidation}",
        "-" * 60,
        "  ELECTRON CONFIGURATION:",
        f"    Shorthand / Full  : {ec_formatted}",
        f"    Shell Electrons   : {shell_str}",
        colored_line,
    ]

    return "\n".join(lines)


def render_element_tile(symbol: Optional[str], data: Optional[Dict[str, Any]], is_selected: bool, compact_mode: bool) -> str:
    """Render a single periodic table tile with consistent width."""
    if symbol is None:
        return "   " if compact_mode else "    "

    sym_str = symbol[:2]
    if compact_mode:
        if is_selected:
            return theme_manager.colorize(f"[{sym_str:^1}]", "header")
        return f" {sym_str:^2}"
    else:
        if is_selected:
            return theme_manager.colorize(f"[{sym_str:^2}]", "header")
        return f" {sym_str:^2} "


def run_interactive_periodic_table() -> None:
    """Launch the interactive 118-element periodic table UI."""
    pt_data = load_periodic_table()

    def on_element_select(symbol: str, data: Dict[str, Any]) -> bool:
        if data:
            detail_text = format_element_detail(symbol, data)
            DetailPanel.show(f"Element: {symbol}", detail_text)
        return True  # Stay in grid view loop

    selector = GridSelector(
        title="INTERACTIVE PERIODIC TABLE",
        grid_matrix=PERIODIC_TABLE_GRID,
        items_dict=pt_data,
        tile_renderer=render_element_tile,
        on_select=on_element_select,
        search_handler=find_grid_coordinates,
        min_width_full=76,
    )
    selector.run()
