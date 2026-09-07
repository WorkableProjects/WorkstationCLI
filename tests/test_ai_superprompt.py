"""Unit tests for AI superprompt generation and reasoning levels."""

from services.ollama_prompts import ReasoningLevel, build_system_prompt, ai_chat_prompt


def test_reasoning_level_enum():
    """Verify all reasoning levels exist."""
    assert ReasoningLevel.MINIMAL.value == "Minimal"
    assert ReasoningLevel.LOW.value == "Low"
    assert ReasoningLevel.MEDIUM.value == "Medium"
    assert ReasoningLevel.MAX.value == "Max"


def test_build_system_prompt_contains_superprompt():
    """Verify system prompt includes universal superprompt instructions."""
    prompt = build_system_prompt("Test Feature", ReasoningLevel.HIGH if hasattr(ReasoningLevel, "HIGH") else ReasoningLevel.MAX)
    assert "You are Workstation CLI's versatile AI assistant" in prompt
    assert "Tutor Mode:" in prompt
    assert "Quiz Generator:" in prompt
    assert "Study Planner:" in prompt
    assert "Problem Solver:" in prompt


def test_ai_chat_prompt_reasoning_levels():
    """Verify reasoning level instructions are injected correctly."""
    prompt_min = ai_chat_prompt(ReasoningLevel.MINIMAL)
    assert "Answer directly" in prompt_min

    prompt_max = ai_chat_prompt(ReasoningLevel.MAX)
    assert "Use extensive planning" in prompt_max
