"""Centralized prompt templates for Ollama-backed AI commands."""

from enum import Enum
from core.banner import VERSION


class ReasoningLevel(str, Enum):
    """Universal CLI reasoning levels supported for every Ollama model."""

    MINIMAL = "Minimal"
    LOW = "Low"
    MEDIUM = "Medium"
    MAX = "Max"


REASONING_INSTRUCTIONS: dict[ReasoningLevel, str] = {
    ReasoningLevel.MINIMAL: "Answer directly. Avoid unnecessary explanation.",
    ReasoningLevel.LOW: "Use light planning. Verify important facts. Stay concise.",
    ReasoningLevel.MEDIUM: "Plan before answering. Explain key decisions. Self-check conclusions.",
    ReasoningLevel.MAX: "Use extensive planning. Consider alternatives. Self-verify. Provide complete answer with reasoning.",
}


def build_system_prompt(feature: str, reasoning_level: ReasoningLevel) -> str:
    """Build a system prompt that emulates the selected reasoning level for any model.

    Injects runtime context so the AI knows it's operating inside Workstation CLI,
    what tools are available, and that a local model (Ollama) may be configured.
    """
    runtime_context = (
        "Running inside Workstation CLI (educational chemistry, study, and AI tools). "
        "Available CLI tools: chemistry calculators (molar mass, stoichiometry, periodic table), "
        "reference lookups, graphing utilities, and an interactive AI chat backed by Ollama. "
    )

    superprompt_instructions = (
        "You are Workstation CLI's versatile AI assistant, serving as an expert tutor, quiz generator, "
        "study planner, and problem solver. "
        "Capabilities & Role:\n"
        "- Tutor Mode: Explain concepts clearly, answer questions, provide step-by-step guidance, "
        "and encourage learning with Socratic questioning when appropriate.\n"
        "- Quiz Generator: Create practice problems, quizzes, and self-assessments with solutions when asked.\n"
        "- Study Planner: Help structure study schedules, recommend topic breakdowns, and suggest study strategies.\n"
        "- Problem Solver: Assist with chemistry, math, coding, and general scientific problem-solving.\n"
        "Behavior Guidelines:\n"
        "- Ensure responses are educational, accurate, clear, and structured.\n"
        "- For unsafe or out-of-scope requests, politely decline and steer back to educational topics.\n"
        "- Preserve conversation context for multi-turn interactions."
    )

    return (
        f"{superprompt_instructions}\n"
        f"Feature Context: {feature}. CLI Version: v1.0.0.\n"
        f"{runtime_context}\n"
        f"Reasoning Mode ({reasoning_level.value}): {REASONING_INSTRUCTIONS[reasoning_level]}"
    )


def ai_chat_prompt(reasoning_level: ReasoningLevel) -> str:
    """Return the reusable AI chat superprompt."""
    return build_system_prompt("AI Chat", reasoning_level)


def essay_helper_prompt(topic: str, reasoning_level: ReasoningLevel) -> str:
    """Return a prompt for essay outlining and writing support."""
    return build_system_prompt("Essay Helper", reasoning_level) + f"\nHelp outline an essay about: {topic}."


def socratic_tutor_prompt(topic: str, reasoning_level: ReasoningLevel) -> str:
    """Return a prompt for Socratic tutoring."""
    return build_system_prompt("Socratic Tutor", reasoning_level) + f"\nTutor with questions about: {topic}."
