"""Tests for Command Palette functionality."""

from core.command_palette import CommandPalette

def test_command_palette_search():
    commands = [
        {"name": "Molar Mass Calculator", "category": "Chemistry", "keywords": "molar mass mole", "handler": None},
        {"name": "Gas Laws Calculator", "category": "Chemistry", "keywords": "gas pressure temp", "handler": None},
        {"name": "Plot Custom Function", "category": "Graphing", "keywords": "plot function graph", "handler": None},
        {"name": "AI Chat", "category": "AI", "keywords": "ai chat ollama", "handler": None},
    ]

    cp = CommandPalette(commands)

    # Empty query returns all commands
    assert len(cp.search("")) == 4

    # Search chemistry
    chem_matches = cp.search("chem")
    assert len(chem_matches) == 2

    # Search specific tool
    plot_matches = cp.search("plot")
    assert len(plot_matches) == 1
    assert plot_matches[0]["name"] == "Plot Custom Function"

    # Search non-matching
    no_matches = cp.search("nonexistent_tool_xyz")
    assert len(no_matches) == 0
