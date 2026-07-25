"""Lightweight schema helpers for validating Ollama structured output."""

from typing import Any, Tuple, Type, Union

Schema = dict[str, Union[Type[Any], Tuple[Type[Any], ...]]]

QUIZ_SCHEMA: Schema = {"questions": list}
STUDY_PLAN_SCHEMA: Schema = {"title": str, "sessions": list}
ESSAY_OUTLINE_SCHEMA: Schema = {"thesis": str, "outline": list}
FLASHCARDS_SCHEMA: Schema = {"flashcards": list}


def validate_schema(payload: dict[str, Any], schema: Schema) -> bool:
    """Return True when all required keys exist and match expected Python types."""
    return all(key in payload and isinstance(payload[key], expected) for key, expected in schema.items())
