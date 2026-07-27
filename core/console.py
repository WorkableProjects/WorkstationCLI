"""Console utilities: smart screen clearing and preserved output buffer.

Provides:
- preserve_output(text): store and display important calculation output that should persist
- clear_navigation(): clear menu/navigation text while re-rendering preserved output
- clear_all(): full clear (no preserved output)
"""
from typing import List

_preserved_buffer: List[str] = []


def preserve_output(text: str) -> None:
    """Save and render text that should persist across menu navigations.

    The text is appended to an in-memory buffer and printed immediately so callers
    can use it as before. Subsequent menu clears will keep this buffer on-screen.
    """
    global _preserved_buffer
    _preserved_buffer.append(text)
    print(text)


def clear_navigation() -> None:
    """Clear the terminal navigation/menu area but reprint preserved outputs.

    Uses a full-screen clear then renders preserved calculation outputs for
    user reference.
    """
    # ANSI full clear + move cursor home
    print("\033[2J\033[H", end="")
    if _preserved_buffer:
        print("""
--- Preserved Output (previous calculations) ---
""")
        for item in _preserved_buffer:
            print(item)
        print("\n" + "-" * 50 + "\n")


def clear_all() -> None:
    """Clear everything and reset preserved buffer."""
    global _preserved_buffer
    _preserved_buffer = []
    print("\033[2J\033[H", end="")
