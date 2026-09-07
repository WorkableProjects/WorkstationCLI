"""Command Palette module for fast searching and running CLI actions/tools."""

import sys
import shutil
from typing import List, Dict, Callable, Any, Optional
from core import theme_manager, navigation
from core.console import clear_navigation

try:
    import termios
    import tty
    _HAS_TERMIOS = True
except Exception:
    _HAS_TERMIOS = False


def _get_key() -> str:
    if not _HAS_TERMIOS:
        return input().strip()
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            import select
            r, _, _ = select.select([sys.stdin], [], [], 0.05)
            if r:
                seq = sys.stdin.read(2)
                return ch + seq
            return "\x1b"
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


class CommandPalette:
    """
    Searchable palette for launching any tool across categories.
    """

    def __init__(self, commands: List[Dict[str, Any]]):
        """
        commands list structure:
        [
            {
                "name": "Molar Mass Calculator",
                "category": "Chemistry",
                "keywords": "mass mole chemistry weight",
                "handler": callable
            }, ...
        ]
        """
        self.commands = commands

    def search(self, query: str) -> List[Dict[str, Any]]:
        if not query.strip():
            return self.commands

        q = query.lower().strip()
        results = []
        for cmd in self.commands:
            name = cmd["name"].lower()
            cat = cmd["category"].lower()
            kw = cmd.get("keywords", "").lower()
            if q in name or q in cat or q in kw:
                results.append(cmd)
        return results

    def run(self) -> None:
        """Run the interactive Command Palette prompt."""
        navigation.push("Command Palette")
        try:
            query = ""
            selected_idx = 0

            while True:
                term_w = shutil.get_terminal_size((80, 24)).columns
                clear_navigation()
                print(f"{navigation.breadcrumb()}\n")

                line = "=" * min(term_w, 80)
                print(theme_manager.colorize(line, "header"))
                print(f" {theme_manager.colorize('COMMAND PALETTE', 'header').center(min(term_w, 78))} ")
                print(theme_manager.colorize(line, "header"))

                print(f"\n Search: [ {query}█ ]")
                print(theme_manager.colorize("-" * min(term_w, 80), "header"))

                matches = self.search(query)
                if not matches:
                    print("\n  (No matching commands found)")
                else:
                    if selected_idx >= len(matches):
                        selected_idx = max(0, len(matches) - 1)

                    print("\n Matching Commands:\n")
                    # Display top matches
                    display_matches = matches[:10]
                    for idx, cmd in enumerate(display_matches):
                        cat_tag = theme_manager.colorize(f"[{cmd['category']}]", "header")
                        if idx == selected_idx:
                            print(theme_manager.colorize(f"  > {idx + 1}. {cmd['name']} {cat_tag} <", "ok"))
                        else:
                            print(f"    {idx + 1}. {cmd['name']} {cat_tag}")

                print("\n" + theme_manager.colorize("-" * min(term_w, 80), "header"))
                print(" Controls: Type to filter | ↑/↓ = Select | Enter = Launch | Esc/Ctrl+C = Exit Palette")

                if _HAS_TERMIOS:
                    key = _get_key()
                    if key in ("\x1b[A", "\x1bOA"):  # Up arrow
                        if matches:
                            selected_idx = (selected_idx - 1) % len(matches)
                    elif key in ("\x1b[B", "\x1bOB"):  # Down arrow
                        if matches:
                            selected_idx = (selected_idx + 1) % len(matches)
                    elif key in ("\r", "\n"):  # Enter
                        if matches and 0 <= selected_idx < len(matches):
                            handler = matches[selected_idx]["handler"]
                            if handler:
                                handler()
                                break
                    elif key in ("\x1b", "\x03"):  # Esc or Ctrl+C
                        break
                    elif key in ("\x7f", "\x08"):  # Backspace
                        query = query[:-1]
                        selected_idx = 0
                    elif len(key) == 1 and ord(key) >= 32:  # Printable character
                        query += key
                        selected_idx = 0
                else:
                    inp = input("\nType search query, 'launch #', or 'q' to return: ").strip()
                    if inp.lower() in ("q", "cancel", "exit"):
                        break
                    elif inp.isdigit():
                        idx = int(inp) - 1
                        if matches and 0 <= idx < len(matches):
                            handler = matches[idx]["handler"]
                            if handler:
                                handler()
                                break
                    else:
                        query = inp
                        selected_idx = 0
        finally:
            navigation.pop()
