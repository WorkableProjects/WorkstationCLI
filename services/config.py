"""Local configuration file helpers for Workstation CLI."""

import json
import os
import subprocess
from pathlib import Path
from typing import Any

from services.ollama_prompts import ReasoningLevel

CONFIG_DIR = Path.home() / ".workstation_cli"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_MODEL = "llama3.2:3b-instruct-q4_K_M"
DEFAULT_CONFIG: dict[str, Any] = {
    "ai": {
        "model": DEFAULT_MODEL,
        "base_url": "http://localhost:11434/api",
        "timeout": 60.0,
        "reasoning_level": ReasoningLevel.MEDIUM.value,
    },
    "appearance": {
        "theme": "blue"
    }
}


def ensure_config_file() -> Path:
    """Create the local config file if needed and return its path."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
    return CONFIG_FILE


def load_config() -> dict[str, Any]:
    """Load configuration, recreating defaults when the local file is invalid."""
    ensure_config_file()
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            config = json.load(file)
    except (OSError, json.JSONDecodeError):
        config = DEFAULT_CONFIG.copy()
        save_config(config)
    return merge_defaults(config)


def save_config(config: dict[str, Any]) -> None:
    """Persist configuration to the local config file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2)
        file.write("\n")


def merge_defaults(config: dict[str, Any]) -> dict[str, Any]:
    """Return a config dictionary with missing default keys filled in."""
    merged = json.loads(json.dumps(DEFAULT_CONFIG))
    ai_config = config.get("ai", {}) if isinstance(config, dict) else {}
    if isinstance(ai_config, dict):
        merged["ai"].update(ai_config)
    appearance_config = config.get("appearance", {}) if isinstance(config, dict) else {}
    if isinstance(appearance_config, dict):
        merged["appearance"].update(appearance_config)
    return merged


def open_config_in_editor() -> bool:
    """Open the local config file in the user's editor and return success."""
    config_path = ensure_config_file()
    editor = os.environ.get("EDITOR") or os.environ.get("VISUAL")
    if not editor:
        return False
    try:
        subprocess.run([editor, str(config_path)], check=False)
    except OSError:
        return False
    return True
