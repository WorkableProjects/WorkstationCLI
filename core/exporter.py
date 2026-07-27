"""Export utilities for saving calculation results to disk or clipboard."""
from pathlib import Path
import datetime
import os

EXPORT_DIR = Path.home() / ".workstation_cli" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def save_text(text: str, prefix: str = "calculation") -> Path:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = EXPORT_DIR / f"{prefix}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
        f.write("\n")
    return filename


def copy_to_clipboard(text: str) -> bool:
    try:
        import pyperclip
    except Exception:
        return False
    try:
        pyperclip.copy(text)
        return True
    except Exception:
        return False
