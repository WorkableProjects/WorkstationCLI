"""Centralized prompt templates for Ollama-backed AI commands."""

from enum import Enum


class ReasoningLevel(str, Enum):
    """Universal CLI reasoning levels supported for every Ollama model."""

    MINIMAL = "Minimal"
    LOW = "Low"
    MEDIUM = "Medium"
    MAX = "Max"


REASONING_INSTRUCTIONS: dict[ReasoningLevel, str] = {
    ReasoningLevel.MINIMAL: "Answer directly. Avoid unnecessary explanation and optimize for speed.",
    ReasoningLevel.LOW: "Use light planning, briefly verify important facts, and stay concise.",
    ReasoningLevel.MEDIUM: "Plan before answering, explain key decisions, and verify important conclusions.",
    ReasoningLevel.MAX: "Use extensive planning, consider alternatives, self-check for errors, and provide a complete answer.",
}


def build_system_prompt(feature: str, reasoning_level: ReasoningLevel) -> str:
    """Build a system prompt that emulates the selected reasoning level for any model."""
    return (
        "You are Workstation CLI's educational AI assistant. "
        f"Feature: {feature}. "
        "Help students learn while being accurate, clear, and safe. "
        f"Reasoning mode ({reasoning_level.value}): {REASONING_INSTRUCTIONS[reasoning_level]}"
    )


def ai_chat_prompt(reasoning_level: ReasoningLevel) -> str:
    """Return the reusable AI chat system prompt."""
    return build_system_prompt("AI Chat", reasoning_level)


def quiz_generator_prompt(topic: str, reasoning_level: ReasoningLevel) -> str:
    """Return a prompt for generating a structured quiz."""
    return build_system_prompt("Quiz Generator", reasoning_level) + f" Create a quiz about: {topic}."


def study_planner_prompt(goal: str, reasoning_level: ReasoningLevel) -> str:
    """Return a prompt for generating a structured study plan."""
    return build_system_prompt("Study Planner", reasoning_level) + f" Build a study plan for: {goal}."


def essay_helper_prompt(topic: str, reasoning_level: ReasoningLevel) -> str:
    """Return a prompt for essay outlining and writing support."""
    return build_system_prompt("Essay Helper", reasoning_level) + f" Help outline an essay about: {topic}."


def socratic_tutor_prompt(topic: str, reasoning_level: ReasoningLevel) -> str:
    """Return a prompt for Socratic tutoring."""
    return build_system_prompt("Socratic Tutor", reasoning_level) + f" Tutor with questions about: {topic}."
