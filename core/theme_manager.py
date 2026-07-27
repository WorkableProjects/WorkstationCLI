"""Theme manager: loads and applies CLI theme preferences."""

from core.theme import get_palette
from services.config import load_config

_current_theme = "blue"


def load_theme() -> None:
    global _current_theme
    cfg = load_config()
    appearance = cfg.get("appearance", {})
    _current_theme = appearance.get("theme", "blue")


def get_current_theme() -> str:
    return _current_theme


def apply_theme() -> None:
    """Load theme on startup."""
    load_theme()


def colorize(text: str, style: str = "reset") -> str:
    """Apply color to text using current theme.
    
    Styles: header, ok, warn, error, reset
    """
    palette = get_palette(_current_theme)
    code = palette.get(style, "")
    reset = palette.get("reset", "")
    return f"{code}{text}{reset}" if code else text


# Colors for common elements
def header(text: str) -> str:
    return colorize(text, "header")


def ok(text: str) -> str:
    return colorize(text, "ok")


def warn(text: str) -> str:
    return colorize(text, "warn")


def error(text: str) -> str:
    return colorize(text, "error")
