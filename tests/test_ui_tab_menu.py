"""Unit tests for HorizontalTabMenu in core.ui."""

from core.ui import HorizontalTabMenu


def test_tab_menu_initialization():
    """Verify HorizontalTabMenu initializes default active indices."""
    tabs = [
        {"name": "Chemistry", "options": [("Molar Mass", lambda: None)]},
        {"name": "AI", "options": [("AI Chat", lambda: None)]},
    ]
    menu = HorizontalTabMenu("Test Menu", tabs)
    assert menu.title == "Test Menu"
    assert menu.active_tab_idx == 0
    assert menu.active_option_idx == 0


def test_tab_menu_structure():
    """Verify tab structure and options retrieval."""
    tabs = [
        {"name": "Tab1", "options": [("Opt1", lambda: None), ("Opt2", lambda: None)]},
        {"name": "Tab2", "options": [("OptA", lambda: None)]},
    ]
    menu = HorizontalTabMenu("Test", tabs)
    assert len(menu.tabs) == 2
    assert len(menu.tabs[0]["options"]) == 2
    assert menu.tabs[1]["name"] == "Tab2"
