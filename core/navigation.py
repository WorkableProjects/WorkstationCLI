"""Navigation stack utilities for breadcrumb display.

Usage:
  from core import navigation
  navigation.push("Chemistry")
  ... display_menu(...) will show breadcrumb
  navigation.pop()
"""

_stack: list[str] = []


def push(name: str) -> None:
    _stack.append(name)


def pop() -> None:
    if _stack:
        _stack.pop()


def current_path() -> list[str]:
    return list(_stack)


def breadcrumb(separator: str = " --> ") -> str:
    if not _stack:
        return "HOME"
    return separator.join(["HOME"] + _stack)
