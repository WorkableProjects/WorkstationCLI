"""Reusable interactive terminal UI primitives: grid selector, navigation, and detail panel."""

import sys
import shutil
from typing import List, Dict, Any, Optional, Callable, Tuple
from core.console import clear_navigation
from core import theme_manager, navigation, help as helpmod

try:
    import termios
    import tty
    _HAS_TERMIOS = True
except Exception:
    _HAS_TERMIOS = False


def get_terminal_width() -> int:
    """Get current terminal width or fallback to 80."""
    try:
        return shutil.get_terminal_size((80, 24)).columns
    except Exception:
        return 80


def _get_key() -> str:
    """Read a single keypress or ANSI escape sequence from stdin."""
    if not _HAS_TERMIOS:
        return input().strip()
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            # Direct read for arrow key escape sequence [A, [B, [C, [D
            import select
            r, _, _ = select.select([sys.stdin], [], [], 0.05)
            if r:
                seq = sys.stdin.read(2)
                return ch + seq
            # Non-blocking fallback try if select didn't catch buffered bytes
            try:
                import fcntl, os
                fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
                try:
                    seq = sys.stdin.read(2)
                    return ch + seq
                except Exception:
                    pass
                finally:
                    fcntl.fcntl(fd, fcntl.F_SETFL, fl)
            except Exception:
                pass
            return "\x1b"
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


class GridSelector:
    """
    Reusable 2D interactive grid selection component.

    Parameters:
        title: Header title for the UI
        grid_matrix: List[List[Optional[str]]] representing rows and columns of keys
        items_dict: Dict[str, Any] mapping key to data object
        tile_renderer: Callable[(key, data, is_selected, compact_mode) -> str]
        on_select: Callable[(key, data) -> bool] called on Enter. Return True to stay in loop, False to exit.
        search_handler: Optional Callable[(query, items_dict) -> Optional[Tuple[int, int]]] returns (r, c) or None
    """

    def __init__(
        self,
        title: str,
        grid_matrix: List[List[Optional[str]]],
        items_dict: Dict[str, Any],
        tile_renderer: Callable[[str, Any, bool, bool], str],
        on_select: Optional[Callable[[str, Any], bool]] = None,
        search_handler: Optional[Callable[[str, Dict[str, Any]], Optional[Tuple[int, int]]]] = None,
        min_width_full: int = 76
    ):
        self.title = title
        self.grid_matrix = grid_matrix
        self.items_dict = items_dict
        self.tile_renderer = tile_renderer
        self.on_select = on_select
        self.search_handler = search_handler
        self.min_width_full = min_width_full

        # Initial cursor position: find first non-None key
        self.r = 0
        self.c = 0
        self._find_first_valid()

    def _find_first_valid(self) -> None:
        for r_idx, row in enumerate(self.grid_matrix):
            for c_idx, key in enumerate(row):
                if key is not None:
                    self.r = r_idx
                    self.c = c_idx
                    return

    def get_selected_key(self) -> Optional[str]:
        if 0 <= self.r < len(self.grid_matrix):
            row = self.grid_matrix[self.r]
            if 0 <= self.c < len(row):
                return row[self.c]
        return None

    def move_cursor(self, dr: int, dc: int) -> None:
        """Move cursor by delta (dr, dc) skipping None slots if possible."""
        max_r = len(self.grid_matrix) - 1
        if max_r < 0:
            return

        new_r = max(0, min(max_r, self.r + dr))
        row = self.grid_matrix[new_r]
        max_c = len(row) - 1
        if max_c < 0:
            return

        new_c = max(0, min(max_c, self.c + dc))

        # If landed on None slot, search along direction
        if row[new_c] is None:
            # Check horizontally
            found = False
            if dc != 0:
                step = 1 if dc > 0 else -1
                curr = new_c
                while 0 <= curr <= max_c:
                    if row[curr] is not None:
                        new_c = curr
                        found = True
                        break
                    curr += step
            elif dr != 0:
                # Vertical move onto None: find nearest valid col in row
                best_c = None
                best_dist = 999
                for c_idx, val in enumerate(row):
                    if val is not None:
                        dist = abs(c_idx - self.c)
                        if dist < best_dist:
                            best_dist = dist
                            best_c = c_idx
                if best_c is not None:
                    new_c = best_c
                    found = True

            if not found and row[new_c] is None:
                return  # Cannot move to empty region

        self.r = new_r
        self.c = new_c

    def run(self) -> None:
        """Run the interactive UI loop."""
        navigation.push(self.title)
        try:
            while True:
                term_w = get_terminal_width()
                compact_mode = term_w < self.min_width_full

                clear_navigation()
                print(f"{navigation.breadcrumb()}\n")

                line = "=" * min(term_w, 80)
                print(theme_manager.colorize(line, "header"))
                print(f" {theme_manager.colorize(self.title, 'header').center(min(term_w, 78))} ")
                print(theme_manager.colorize(line, "header"))

                selected_key = self.get_selected_key()

                # Render Grid
                for r_idx, row in enumerate(self.grid_matrix):
                    row_str_parts = []
                    for c_idx, key in enumerate(row):
                        is_sel = (r_idx == self.r and c_idx == self.c)
                        data = self.items_dict.get(key) if key else None
                        tile_str = self.tile_renderer(key, data, is_sel, compact_mode)
                        row_str_parts.append(tile_str)
                    print("".join(row_str_parts))

                # Footer
                print("\n" + theme_manager.colorize("-" * min(term_w, 80), "header"))
                if selected_key and selected_key in self.items_dict:
                    item_info = self.items_dict[selected_key]
                    name = item_info.get("name", selected_key)
                    print(f" Highlighted: [ {selected_key} ] {name}")

                print(" Controls: Arrow Keys = Navigate | Enter = View Details | [/] or [s] = Search | [q] = Return")

                if _HAS_TERMIOS:
                    key = _get_key()
                    if key in ("\x1b[A", "\x1bOA", "w", "W", "k", "K"):  # Up
                        self.move_cursor(-1, 0)
                        continue
                    elif key in ("\x1b[B", "\x1bOB", "j", "J"):  # Down
                        self.move_cursor(1, 0)
                        continue
                    elif key in ("\x1b[D", "\x1bOD", "a", "A", "h", "H"):  # Left
                        self.move_cursor(0, -1)
                        continue
                    elif key in ("\x1b[C", "\x1bOC", "d", "D", "l", "L"):  # Right
                        self.move_cursor(0, 1)
                        continue
                    elif key in ("\r", "\n"):  # Enter
                        sel_key = self.get_selected_key()
                        if sel_key and self.on_select:
                            stay = self.on_select(sel_key, self.items_dict.get(sel_key))
                            if not stay:
                                break
                        continue
                    elif key in ("/", "s", "S"):  # Search
                        self._handle_search()
                        continue
                    elif key in ("q", "Q", "0"):
                        break
                    continue
                else:
                    cmd = input("\nEnter command (arrow/s/enter/q): ").strip().lower()
                    if cmd in ("q", "0", "exit"):
                        break
                    elif cmd in ("s", "search", "/"):
                        self._handle_search()
                    elif cmd in ("v", "view", "") and selected_key:
                        if self.on_select:
                            self.on_select(selected_key, self.items_dict.get(selected_key))
        finally:
            navigation.pop()

    def _handle_search(self) -> None:
        query = input("\nSearch element by Symbol, Name, or Number: ").strip()
        if not query:
            return
        if self.search_handler:
            pos = self.search_handler(query, self.items_dict)
            if pos:
                r, c = pos
                self.r = r
                self.c = c
            else:
                print(theme_manager.error(f"[Info] No matching element for '{query}'."))
                input("Press ENTER to continue...")


class DetailPanel:
    """Reusable detail panel display."""

    @staticmethod
    def show(title: str, content: str) -> None:
        from core.navigation import push, pop
        push(title)
        try:
            clear_navigation()
            print(content)
            input("\nPress ENTER to return...")
        finally:
            pop()
