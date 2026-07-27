"""Simple UI theme helpers using ANSI color palettes.

Current implementation only exposes a color wrapper and a saved preference
in the config file. Full application of theme to all outputs is iterative.
"""

PALETTES = {
    "dark": {
        "header": "\033[95m",
        "ok": "\033[92m",
        "warn": "\033[93m",
        "error": "\033[91m",
        "reset": "\033[0m",
    },
    "light": {
        "header": "\033[94m",
        "ok": "\033[32m",
        "warn": "\033[33m",
        "error": "\033[31m",
        "reset": "\033[0m",
    },
}


def get_palette(theme: str = "dark") -> dict:
    return PALETTES.get(theme, PALETTES["dark"])
