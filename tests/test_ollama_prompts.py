"""Unit tests for Ollama prompts and superprompt architecture."""

from services.ollama_prompts import ReasoningLevel, REASONING_INSTRUCTIONS, build_system_prompt, ai_chat_prompt, essay_helper_prompt, socratic_tutor_prompt


def test_reasoning_instructions_mapping():
    """Verify reasoning level instructions match expected strings."""
    assert REASONING_INSTRUCTIONS[ReasoningLevel.MINIMAL] == "Answer directly. Avoid unnecessary explanation."
    assert REASONING_INSTRUCTIONS[ReasoningLevel.LOW] == "Use light planning. Verify important facts. Stay concise."
    assert REASONING_INSTRUCTIONS[ReasoningLevel.MEDIUM] == "Plan before answering. Explain key decisions. Self-check conclusions."
    assert REASONING_INSTRUCTIONS[ReasoningLevel.MAX] == "Use extensive planning. Consider alternatives. Self-verify. Provide complete answer with reasoning."


def test_build_system_prompt_content():
    """Verify system prompt includes superprompt capabilities, feature, version, and reasoning level."""
    prompt = build_system_prompt("AI Chat", ReasoningLevel.MEDIUM)
    assert "Tutor Mode" in prompt
    assert "Quiz Generator" in prompt
    assert "Study Planner" in prompt
    assert "Problem Solver" in prompt
    assert "Feature Context: AI Chat" in prompt
    assert "v0.0.6.2" in prompt
    assert "Reasoning Mode (Medium): Plan before answering. Explain key decisions. Self-check conclusions." in prompt


def test_ai_chat_prompt():
    """Verify ai_chat_prompt uses build_system_prompt properly across reasoning levels."""
    for level in ReasoningLevel:
        prompt = ai_chat_prompt(level)
        assert f"Reasoning Mode ({level.value}): {REASONING_INSTRUCTIONS[level]}" in prompt


def test_other_prompts():
    """Verify helper prompts append topic specific instructions."""
    essay_p = essay_helper_prompt("photosynthesis", ReasoningLevel.LOW)
    assert "Help outline an essay about: photosynthesis." in essay_p

    socratic_p = socratic_tutor_prompt("thermodynamics", ReasoningLevel.MINIMAL)
    assert "Tutor with questions about: thermodynamics." in socratic_p
