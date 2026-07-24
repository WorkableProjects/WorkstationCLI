import json
import re
from pathlib import Path
from typing import Dict

DATA_DIR = Path(__file__).parent.parent / "data"

def load_periodic_table() -> Dict[str, dict]:
    file_path = DATA_DIR / "periodic_table.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_constants() -> dict:
    file_path = DATA_DIR / "constants.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_chemical_formula(formula: str) -> Dict[str, int]:
    """
    Parses a chemical formula string into a dictionary mapping element symbols to counts.
    Supports parentheses, nested groups, and hydrate notation with dot '·' or '*'.
    Examples:
        'H2O' -> {'H': 2, 'O': 1}
        'Ca(OH)2' -> {'Ca': 1, 'O': 2, 'H': 2}
        'Al2(SO4)3' -> {'Al': 2, 'S': 3, 'O': 12}
        'CuSO4·5H2O' -> {'Cu': 1, 'S': 1, 'O': 9, 'H': 10}
    """
    clean_formula = formula.replace(" ", "").replace("*", "·")
    if not clean_formula:
        raise ValueError("Formula cannot be empty.")

    # Check for hydrate (e.g. CuSO4·5H2O)
    if "·" in clean_formula:
        parts = clean_formula.split("·")
        main_part = parts[0]
        hydrate_part = parts[1]
        
        # Match multiplier in hydrate part (e.g., 5H2O -> multiplier 5, formula H2O)
        m = re.match(r"^(\d+)(.+)$", hydrate_part)
        if m:
            hydrate_mult = int(m.group(1))
            hydrate_sub_formula = m.group(2)
        else:
            hydrate_mult = 1
            hydrate_sub_formula = hydrate_part

        main_counts = _parse_simple_or_parentheses(main_part)
        hydrate_counts = _parse_simple_or_parentheses(hydrate_sub_formula)
        
        result = dict(main_counts)
        for elem, count in hydrate_counts.items():
            result[elem] = result.get(elem, 0) + count * hydrate_mult
        return result
    else:
        return _parse_simple_or_parentheses(clean_formula)

def _parse_simple_or_parentheses(formula: str) -> Dict[str, int]:
    periodic_table = load_periodic_table()

    # Recursive sub-parser using stack for nested parentheses
    def parse_group(s: str) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        i = 0
        n = len(s)

        while i < n:
            if s[i] == '(':
                # Find matching closing parenthesis
                open_bracket_count = 1
                j = i + 1
                while j < n and open_bracket_count > 0:
                    if s[j] == '(':
                        open_bracket_count += 1
                    elif s[j] == ')':
                        open_bracket_count -= 1
                    j += 1
                
                if open_bracket_count != 0:
                    raise ValueError(f"Unmatched parenthesis in formula: {formula}")
                
                inner_formula = s[i+1:j-1]
                sub_counts = parse_group(inner_formula)
                
                # Check multiplier after closing parenthesis
                k = j
                mult_str = ""
                while k < n and s[k].isdigit():
                    mult_str += s[k]
                    k += 1
                
                mult = int(mult_str) if mult_str else 1
                for elem, cnt in sub_counts.items():
                    counts[elem] = counts.get(elem, 0) + cnt * mult
                i = k
            else:
                # Match element symbol (Uppercase followed by optional lowercase)
                elem_match = re.match(r"^([A-Z][a-z]?)", s[i:])
                if not elem_match:
                    raise ValueError(f"Invalid element or symbol near character '{s[i]}' in formula: {formula}")
                
                elem = elem_match.group(1)
                if elem not in periodic_table:
                    raise ValueError(f"Unknown element symbol '{elem}' in formula: {formula}")

                i += len(elem)

                # Match count
                num_str = ""
                while i < n and s[i].isdigit():
                    num_str += s[i]
                    i += 1
                
                cnt = int(num_str) if num_str else 1
                counts[elem] = counts.get(elem, 0) + cnt

        return counts

    return parse_group(formula)
