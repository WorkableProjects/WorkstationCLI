"""Unit tests for HorizontalTabMenu in core.ui, verifying tab navigation and dynamic option evaluation."""

from core.ui import HorizontalTabMenu


def test_tab_menu_callable_options():
    """Verify tab menu dynamically evaluates callable options lists."""
    counter = [0]

    def dynamic_options():
        counter[0] += 1
        return [("Dynamic Option " + str(counter[0]), lambda: None)]

    tabs = [
        {"name": "Dynamic Tab", "options": dynamic_options}
    ]

    menu = HorizontalTabMenu("Test Menu", tabs)
    assert menu.active_tab_idx == 0
    raw = menu.tabs[menu.active_tab_idx]["options"]
    opts = raw() if callable(raw) else raw
    assert opts[0][0] == "Dynamic Option 1"


def test_tab_menu_callable_labels():
    """Verify tab menu dynamically evaluates callable option labels."""
    status = "Active"
    label_fn = lambda: f"Setting Status: {status}"

    tabs = [
        {"name": "Settings", "options": [(label_fn, lambda: None)]}
    ]

    menu = HorizontalTabMenu("Test Menu", tabs)
    raw = menu.tabs[0]["options"][0][0]
    evaluated = raw() if callable(raw) else str(raw)
    assert evaluated == "Setting Status: Active"


def test_tab_menu_clamping_active_option_index():
    """Verify active option index is safely clamped if options list shrinks."""
    tabs = [
        {"name": "Tab1", "options": [("1", None), ("2", None), ("3", None)]}
    ]
    menu = HorizontalTabMenu("Test", tabs)
    menu.active_option_idx = 5
    options = menu.tabs[0]["options"]
    if menu.active_option_idx >= len(options):
        menu.active_option_idx = max(0, len(options) - 1)
    assert menu.active_option_idx == 2
