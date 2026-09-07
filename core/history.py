"""Session command/calculation history.

Stores a small list of recent calculation entries. Each entry is a dict with keys:
- type: e.g., 'molar_mass'
- params: dict of parameters used (e.g., {'formula': 'H2O'})
- result: human-readable result text
"""
from collections import deque
from typing import Optional, Dict, Any

_HISTORY_MAX = 50
_history = deque(maxlen=_HISTORY_MAX)
_session_context: Dict[str, Any] = {}


def add(entry: Dict[str, Any]) -> None:
    _history.appendleft(entry)


def set_session_data(key: str, value: Any) -> None:
    """Store temporary session state."""
    _session_context[key] = value


def get_session_data(key: str, default: Any = None) -> Any:
    """Retrieve temporary session state."""
    return _session_context.get(key, default)


def clear_session() -> None:
    """Clear session data and calculation history."""
    _history.clear()
    _session_context.clear()


def get_recent(n: int = 1) -> Optional[Dict[str, Any]]:
    if n < 1 or n > len(_history):
        return None
    return list(_history)[n-1]


def list_history(limit: int = 10):
    return list(_history)[:limit]


def clear_history() -> None:
    _history.clear()
