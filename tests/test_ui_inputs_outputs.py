"""Tests for standardized input system primitives and universal output actions."""

from core.ui import prompt_input, prompt_float, prompt_int, prompt_yes_no, handle_output_actions

def test_prompt_input_with_default(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "")
    res = prompt_input("Enter value", default="default_val")
    assert res == "default_val"

def test_prompt_float_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "12.34")
    res = prompt_float("Enter float", min_val=0.0)
    assert res == 12.34

def test_prompt_int_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "42")
    res = prompt_int("Enter int", min_val=1)
    assert res == 42

def test_prompt_yes_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "y")
    assert prompt_yes_no("Proceed?") is True

    monkeypatch.setattr("builtins.input", lambda prompt: "n")
    assert prompt_yes_no("Proceed?") is False

    monkeypatch.setattr("builtins.input", lambda prompt: "")
    assert prompt_yes_no("Proceed?", default=True) is True

def test_handle_output_actions_back(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "b")
    # Should cleanly exit back without error
    handle_output_actions("Test Output", "Sample result content", actions=["copy", "save", "back"])
