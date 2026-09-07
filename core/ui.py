"""Reusable interactive terminal UI primitives: grid selector, horizontal tab menu, navigation, and detail panel."""

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


class HorizontalTabMenu:
    """
    Horizontal tab-based interactive navigation menu.

    Structure:
    tabs = [
        {
            "name": "Chemistry",
            "options": [
                ("Molar Mass Calculator", handler_fn),
                ...
            ]
        },
        ...
    ]
    """

    def __init__(self, title: str, tabs: List[Dict[str, Any]], palette_commands: Optional[List[Dict[str, Any]]] = None):
        self.title = title
        self.tabs = tabs
        self.active_tab_idx = 0
        self.active_option_idx = 0
        self.palette_commands = palette_commands

    def run(self) -> None:
        """Run the interactive horizontal tab menu loop."""
        navigation.push(self.title)
        try:
            while True:
                term_w = get_terminal_width()
                clear_navigation()
                print(f"{navigation.breadcrumb()}\n")

                # Banner header line
                line = "=" * min(term_w, 80)
                print(theme_manager.colorize(line, "header"))
                print(f" {theme_manager.colorize(self.title, 'header').center(min(term_w, 78))} ")
                print(theme_manager.colorize(line, "header"))

                # Render Tab Bar
                tab_parts = []
                for idx, tab in enumerate(self.tabs):
                    tab_name = tab["name"]
                    if idx == self.active_tab_idx:
                        rendered = theme_manager.colorize(f"[ {tab_name} ]", "header")
                    else:
                        rendered = f"  {tab_name}  "
                    tab_parts.append(rendered)
                print("\n  " + "  ".join(tab_parts) + "\n")
                print(theme_manager.colorize("-" * min(term_w, 80), "header"))

                current_tab = self.tabs[self.active_tab_idx]
                raw_options = current_tab.get("options", [])
                if callable(raw_options):
                    options = raw_options()
                else:
                    options = raw_options

                if options and self.active_option_idx >= len(options):
                    self.active_option_idx = max(0, len(options) - 1)

                # Render active tab's options
                print(f"\n {theme_manager.colorize(current_tab['name'].upper(), 'header')} OPTIONS:\n")
                if not options:
                    print("  (No options available)")
                else:
                    for opt_idx, option in enumerate(options):
                        opt_label = option[0]
                        if callable(opt_label):
                            label = opt_label()
                        else:
                            label = str(opt_label)
                        if opt_idx == self.active_option_idx:
                            print(theme_manager.colorize(f"  > {opt_idx + 1}. {label} <", "ok"))
                        else:
                            print(f"    {opt_idx + 1}. {label}")

                print("\n" + theme_manager.colorize("-" * min(term_w, 80), "header"))
                palette_hint = " | Ctrl+K / '/' = Command Palette" if self.palette_commands else ""
                print(f" Controls: ←/→ (a/d) = Switch Tabs | ↑/↓ (w/s) = Navigate Options | Enter = Run{palette_hint} | q = Exit")

                if _HAS_TERMIOS:
                    key = _get_key()
                    if key in ("\x0b", "/") and self.palette_commands:  # Ctrl+K or /
                        from core.command_palette import CommandPalette
                        cp = CommandPalette(self.palette_commands)
                        cp.run()
                    elif key in ("\x1b[D", "\x1bOD", "a", "A", "h", "H"):  # Left
                        self.active_tab_idx = (self.active_tab_idx - 1) % len(self.tabs)
                        self.active_option_idx = 0
                    elif key in ("\x1b[C", "\x1bOC", "d", "D", "l", "L"):  # Right
                        self.active_tab_idx = (self.active_tab_idx + 1) % len(self.tabs)
                        self.active_option_idx = 0
                    elif key in ("\x1b[A", "\x1bOA", "w", "W", "k", "K"):  # Up
                        if options:
                            self.active_option_idx = (self.active_option_idx - 1) % len(options)
                    elif key in ("\x1b[B", "\x1bOB", "s", "S", "j", "J"):  # Down
                        if options:
                            self.active_option_idx = (self.active_option_idx + 1) % len(options)
                    elif key in ("\r", "\n"):  # Enter
                        if options and 0 <= self.active_option_idx < len(options):
                            handler = options[self.active_option_idx][1]
                            if handler:
                                handler()
                    elif key in ("q", "Q", "\x1b", "0"):
                        break
                else:
                    cmd = input("\nEnter command (left/right/up/down/enter/q or option #): ").strip().lower()
                    if cmd in ("q", "exit", "0"):
                        break
                    elif cmd in ("a", "left", "h"):
                        self.active_tab_idx = (self.active_tab_idx - 1) % len(self.tabs)
                        self.active_option_idx = 0
                    elif cmd in ("d", "right", "l"):
                        self.active_tab_idx = (self.active_tab_idx + 1) % len(self.tabs)
                        self.active_option_idx = 0
                    elif cmd in ("w", "up", "k"):
                        if options:
                            self.active_option_idx = (self.active_option_idx - 1) % len(options)
                    elif cmd in ("s", "down", "j"):
                        if options:
                            self.active_option_idx = (self.active_option_idx + 1) % len(options)
                    elif cmd in ("", "enter"):
                        if options and 0 <= self.active_option_idx < len(options):
                            handler = options[self.active_option_idx][1]
                            if handler:
                                handler()
                    elif cmd.isdigit():
                        idx = int(cmd) - 1
                        if 0 <= idx < len(options):
                            self.active_option_idx = idx
                            handler = options[idx][1]
                            if handler:
                                handler()
        finally:
            navigation.pop()


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


# Standardized Input System Primitives
def prompt_input(
    prompt_text: str,
    default: Optional[str] = None,
    validator: Optional[Callable[[str], Any]] = None,
    allow_cancel: bool = True
) -> Optional[str]:
    """
    Standardized interactive input prompt with optional default, validation, and cancel support.
    Returns None if user cancels (by entering 'q', 'cancel', or Esc when empty).
    """
    default_str = f" [{default}]" if default is not None else ""
    full_prompt = f"{prompt_text}{default_str}: "

    while True:
        try:
            val = input(full_prompt).strip()
        except (KeyboardInterrupt, EOFError):
            return None

        if not val:
            if default is not None:
                return str(default)
            if allow_cancel:
                return None

        if allow_cancel and val.lower() in ("q", "cancel", ":q"):
            return None

        if validator:
            try:
                validated_val = validator(val)
                return str(validated_val) if not isinstance(validated_val, str) else validated_val
            except Exception as e:
                print(theme_manager.error(f"  [Validation Error] {e}"))
                continue

        return val


def prompt_float(
    prompt_text: str,
    default: Optional[float] = None,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    allow_blank: bool = False
) -> Optional[float]:
    """Standardized numeric float input prompt with min/max validation."""
    def _validate(s: str) -> float:
        f = float(s)
        if min_val is not None and f < min_val:
            raise ValueError(f"Value must be >= {min_val}")
        if max_val is not None and f > max_val:
            raise ValueError(f"Value must be <= {max_val}")
        return f

    default_str = str(default) if default is not None else None
    res = prompt_input(prompt_text, default=default_str, validator=_validate, allow_cancel=True)
    if res is None:
        return None if allow_blank else default
    try:
        return float(res)
    except Exception:
        return default


def prompt_int(
    prompt_text: str,
    default: Optional[int] = None,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None,
    allow_blank: bool = False
) -> Optional[int]:
    """Standardized integer input prompt with min/max validation."""
    def _validate(s: str) -> int:
        i = int(s)
        if min_val is not None and i < min_val:
            raise ValueError(f"Value must be >= {min_val}")
        if max_val is not None and i > max_val:
            raise ValueError(f"Value must be <= {max_val}")
        return i

    default_str = str(default) if default is not None else None
    res = prompt_input(prompt_text, default=default_str, validator=_validate, allow_cancel=True)
    if res is None:
        return None if allow_blank else default
    try:
        return int(res)
    except Exception:
        return default


def prompt_yes_no(prompt_text: str, default: bool = False) -> bool:
    """Standardized Yes/No boolean prompt."""
    hint = "[Y/n]" if default else "[y/N]"
    full_prompt = f"{prompt_text} {hint}: "
    try:
        res = input(full_prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        return default

    if not res:
        return default
    return res.startswith("y")


# Universal Output Actions Primitive
def handle_output_actions(
    title: str,
    text_content: str,
    actions: Optional[List[str]] = None,
    ai_callback: Optional[Callable[[str], None]] = None
) -> None:
    """
    Standardized output action bar handler: [Copy], [Save], [Export], [Send to AI], [Back].
    """
    from core import exporter
    if actions is None:
        actions = ["copy", "save", "back"]

    term_w = get_terminal_width()
    print("\n" + theme_manager.colorize("-" * min(term_w, 80), "header"))
    action_btns = []
    if "copy" in actions:
        action_btns.append("[C]opy")
    if "save" in actions or "export" in actions:
        action_btns.append("[S]ave")
    if "send_to_ai" in actions and ai_callback:
        action_btns.append("[A]I Chat")
    action_btns.append("[B]ack")

    print(" Actions: " + "  ".join(action_btns))

    while True:
        try:
            choice = input("\nSelect action (or press Enter to return): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break

        if choice in ("", "b", "back", "q", "exit"):
            break
        elif choice in ("c", "copy") and "copy" in actions:
            ok = exporter.copy_to_clipboard(text_content)
            if ok:
                print(theme_manager.colorize("✓ Copied to clipboard.", "ok"))
            else:
                print(theme_manager.error("[Info] Clipboard not available. Output text is printed above."))
        elif choice in ("s", "save", "e", "export") and ("save" in actions or "export" in actions):
            prefix = title.lower().replace(" ", "_").replace("/", "_")
            path = exporter.save_text(text_content, prefix=prefix)
            print(theme_manager.colorize(f"✓ Saved output to: {path}", "ok"))
        elif choice in ("a", "ai") and "send_to_ai" in actions and ai_callback:
            print(theme_manager.colorize("Sending output context to AI Chat...", "header"))
            ai_callback(text_content)
            break
        else:
            print(theme_manager.error("Invalid choice. Press Enter to return."))
