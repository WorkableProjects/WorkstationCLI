from typing import List, Tuple, Optional
from core.console import clear_navigation
from core import navigation, help as helpmod

try:
    import termios
    import tty
    _HAS_TERMIOS = True
except Exception:
    _HAS_TERMIOS = False


def _get_single_key() -> str:
    if not _HAS_TERMIOS:
        # Fallback to normal input if termios not available
        return input()
    import sys
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        # Handle arrow sequences
        if ch == "\x1b":
            seq = sys.stdin.read(2)
            return ch + seq
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def display_menu(title: str, options: List[Tuple[str, str]]) -> str:
    """
    Interactive menu with breadcrumb, smart clearing, keyboard navigation, and help.

    - Arrow keys navigate (Up/Down)
    - Enter selects highlighted option
    - Typing a number selects that option immediately
    - Typing '?' or 'help' shows context help
    """
    # Render once then enter input loop
    selected_index = 0
    while True:
        clear_navigation()
        breadcrumb = navigation.breadcrumb()
        print(f"{breadcrumb}\n")
        print("\n" + "=" * 40)
        if title:
            print(f" {title.center(38)} ")
            print("=" * 40)
        for idx, (key, desc) in enumerate(options):
            prefix = "> " if idx == selected_index else "  "
            print(f"{prefix}{key}. {desc}")
        print("=" * 40)

        if _HAS_TERMIOS:
            print("\nUse Up/Down arrows to navigate, Enter to select, or type a number. Press '?' for help.")
            key = _get_single_key()
            if key == "\x1b[A":  # Up
                selected_index = (selected_index - 1) % len(options)
                continue
            if key == "\x1b[B":  # Down
                selected_index = (selected_index + 1) % len(options)
                continue
            if key in ("\r", "\n"):
                return options[selected_index][0]
            if key.isdigit():
                # consume the rest of the line if any
                rest = ''
                if key != '\n':
                    # read remainder of number
                    rest = sys.stdin.readline().strip()
                choice = key + rest
                return choice.strip()
            if key == '?':
                helpmod.show_help(title)
                continue
            # Otherwise ignore and loop
            continue
        else:
            raw = input("\nSelect an option: ").strip()
            if not raw:
                continue
            if raw.lower() in {"?", "help"}:
                helpmod.show_help(title)
                continue
            return raw
