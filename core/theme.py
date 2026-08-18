"""Simple UI theme helpers using ANSI color palettes.

Current implementation only exposes a color wrapper and a saved preference
in the config file. Full application of theme to all outputs is iterative.
"""

PALETTES = {
    "blue": {
        "header": "\033[34m",      # Dark Blue (replaced bright blue)
        "ok": "\033[36m",          # Cyan
        "warn": "\033[33m",        # Yellow
        "error": "\033[31m",       # Red
        "reset": "\033[0m",
    },
    "pink": {
        "header": "\033[38;5;205m", # Refined Pink (replaced bright magenta/pink)
        "ok": "\033[92m",          # Bright green
        "warn": "\033[93m",        # Bright yellow
        "error": "\033[91m",       # Bright red
        "reset": "\033[0m",
    },
    "red": {
        "header": "\033[31m",      # Red
        "ok": "\033[32m",          # Green
        "warn": "\033[33m",        # Yellow
        "error": "\033[91m",       # Bright Red
        "reset": "\033[0m",
    },
    "orange": {
        "header": "\033[38;5;208m", # Orange
        "ok": "\033[32m",          # Green
        "warn": "\033[33m",        # Yellow
        "error": "\033[31m",       # Red
        "reset": "\033[0m",
    },
    "green": {
        "header": "\033[32m",      # Green
        "ok": "\033[36m",          # Cyan
        "warn": "\033[33m",        # Yellow
        "error": "\033[31m",       # Red
        "reset": "\033[0m",
    },
    "cyan": {
        "header": "\033[36m",      # Cyan
        "ok": "\033[32m",          # Green
        "warn": "\033[33m",        # Yellow
        "error": "\033[31m",       # Red
        "reset": "\033[0m",
    },
    "black": {
        "header": "\033[38;2;0;0;0;48;2;0;0;0m", # Black on black
        "ok": "\033[38;2;0;0;0;48;2;0;0;0m",     # Black on black
        "warn": "\033[38;2;0;0;0;48;2;0;0;0m",   # Black on black
        "error": "\033[38;2;0;0;0;48;2;0;0;0m",  # Black on black
        "reset": "\033[0m",
    },
}


def get_palette(theme: str = "blue") -> dict:
    return PALETTES.get(theme, PALETTES["blue"])
