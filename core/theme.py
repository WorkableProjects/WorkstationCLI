"""Simple UI theme helpers using ANSI color palettes.

Current implementation only exposes a color wrapper and a saved preference
in the config file. Full application of theme to all outputs is iterative.
"""

PALETTES = {
    "dark": {
        "header": "\033[95m",      # Bright magenta
        "ok": "\033[92m",          # Bright green
        "warn": "\033[93m",        # Bright yellow
        "error": "\033[91m",       # Bright red
        "reset": "\033[0m",
    },
    "light": {
        "header": "\033[34m",      # Dark blue
        "ok": "\033[32m",          # Dark green
        "warn": "\033[33m",        # Dark yellow
        "error": "\033[31m",       # Dark red
        "reset": "\033[0m",
        "bg": "\033[47m",          # White background (optional)
    },
}


def get_palette(theme: str = "dark") -> dict:
    return PALETTES.get(theme, PALETTES["dark"])
