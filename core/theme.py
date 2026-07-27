"""Simple UI theme helpers using ANSI color palettes.

Current implementation only exposes a color wrapper and a saved preference
in the config file. Full application of theme to all outputs is iterative.
"""

PALETTES = {
    "blue": {
        "header": "\033[94m",      # Bright blue
        "ok": "\033[36m",          # Cyan
        "warn": "\033[33m",        # Yellow
        "error": "\033[31m",       # Red
        "reset": "\033[0m",
    },
    "pink": {
        "header": "\033[95m",      # Bright magenta/pink
        "ok": "\033[92m",          # Bright green
        "warn": "\033[93m",        # Bright yellow
        "error": "\033[91m",       # Bright red
        "reset": "\033[0m",
    },
}


def get_palette(theme: str = "blue") -> dict:
    return PALETTES.get(theme, PALETTES["blue"])
