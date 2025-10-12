"""LLM interaction functions for flashcard generation."""

import functools
from typing import Optional

from google import genai

from anki_qb.prompts import PROMPT_SANITIZE_TERM
from anki_qb.search import search_bonuses, search_tossups
from anki_qb.formatters import format_qa


# Global client that will be initialized with API key
_client: Optional[genai.Client] = None


def initialize_client(api_key: str) -> None:
    """
    Initialize the global Gemini client with an API key.

    Args:
        api_key: Google Gemini API key
    """
    global _client
    _client = genai.Client(api_key=api_key)


def get_client() -> genai.Client:
    """
    Get the global Gemini client.

    Returns:
        Initialized Gemini client

    Raises:
        RuntimeError: If client hasn't been initialized
    """
    if _client is None:
        raise RuntimeError(
            "Gemini client not initialized. Call initialize_client() first "
            "or set the GEMINI_API_KEY environment variable."
        )
    return _client


@functools.cache
def sanitize_term(term: str) -> str:
    """
    Sanitize a search term using LLM to increase likelihood of matching in database.

    Args:
        term: Original search term (may include dates, etc.)

    Returns:
        Sanitized search term
    """
    client = get_client()
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=PROMPT_SANITIZE_TERM.format(term=term),
    ).text.strip()


def ask_llm(prompt: str, model: str = "gemini-2.5-flash", thinking_budget: int = -1) -> str:
    """
    Ask the LLM a question using the specified model.

    Args:
        prompt: The prompt to send to the LLM
        model: Model name to use (default: gemini-2.5-flash)
        thinking_budget: Thinking budget (-1 for dynamic, 0 to turn off, >0 for specific budget)

    Returns:
        LLM response text
    """
    client = get_client()
    result = client.models.generate_content(
        model=model,
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            thinking_config=genai.types.ThinkingConfig(thinking_budget=thinking_budget)
        ),
    )
    return result.text


def get_qbr_data(ygk_data: dict[str, str], bonuses_df, tossups_df) -> dict[str, str]:
    """
    Get QBReader data (tossups and bonuses) for a given YGK article data.

    Args:
        ygk_data: Dictionary with YGK article data including 'label' field
        bonuses_df: DataFrame with bonus questions
        tossups_df: DataFrame with tossup questions

    Returns:
        Dictionary with num_related_bonuses, num_related_tossups, bonuses, and tossups
    """
    term = sanitize_term(ygk_data["label"])
    bonuses = search_bonuses(term, bonuses_df)
    tossups = search_tossups(term, tossups_df)
    return {
        "num_related_bonuses": len(bonuses),
        "num_related_tossups": len(tossups),
        "bonuses": "\n\n".join(format_qa(bonuses)),
        "tossups": "\n\n".join(format_qa(tossups)),
    }
