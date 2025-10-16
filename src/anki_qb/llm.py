"""LLM interaction functions for flashcard generation using the llm package."""

import functools
from typing import Optional

import llm

from anki_qb.prompts import PROMPT_SANITIZE_TERM
from anki_qb.search import search_bonuses, search_tossups
from anki_qb.formatters import format_qa


# Default model to use if not specified
DEFAULT_MODEL = "gpt-4o-mini"


@functools.cache
def sanitize_term(term: str, model: Optional[str] = None) -> str:
    """
    Sanitize a search term using LLM to increase likelihood of matching in database.

    Args:
        term: Original search term (may include dates, etc.)
        model: LLM model to use (defaults to DEFAULT_MODEL)

    Returns:
        Sanitized search term
    """
    model_obj = llm.get_model(model or DEFAULT_MODEL)
    response = model_obj.prompt(PROMPT_SANITIZE_TERM.format(term=term))
    return response.text().strip()


def ask_llm(prompt: str, model: Optional[str] = None) -> str:
    """
    Ask the LLM a question using the specified model.

    Args:
        prompt: The prompt to send to the LLM
        model: Model name to use (e.g., "gpt-4", "claude-3-5-sonnet", "gemini-2.0-flash")
               If None, uses DEFAULT_MODEL

    Returns:
        LLM response text
    """
    model_obj = llm.get_model(model or DEFAULT_MODEL)
    response = model_obj.prompt(prompt)
    return response.text()


def get_qbr_data(ygk_data: dict[str, str], bonuses_df, tossups_df, model: Optional[str] = None) -> dict[str, str]:
    """
    Get QBReader data (tossups and bonuses) for a given YGK article data.

    Args:
        ygk_data: Dictionary with YGK article data including 'label' field
        bonuses_df: DataFrame with bonus questions
        tossups_df: DataFrame with tossup questions
        model: LLM model to use for term sanitization

    Returns:
        Dictionary with num_related_bonuses, num_related_tossups, bonuses, tossups, and sanitized_term
    """
    term = sanitize_term(ygk_data["label"], model=model)
    bonuses = search_bonuses(term, bonuses_df)
    tossups = search_tossups(term, tossups_df)
    return {
        "num_related_bonuses": len(bonuses),
        "num_related_tossups": len(tossups),
        "bonuses": "\n\n".join(format_qa(bonuses)),
        "tossups": "\n\n".join(format_qa(tossups)),
        "sanitized_term": term,
    }
