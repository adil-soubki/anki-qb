"""Search functions for QBReader database of tossups and bonuses."""

import re
import pandas as pd


def search_bonuses(term: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Search for a term (case-insensitive) in the following columns of a
    bonus DataFrame:
      - leadin_sanitized (string)
      - answers_sanitized (list of strings)
      - parts_sanitized (list of strings)

    Args:
        term: The search term
        df: Bonus DataFrame with sanitized columns

    Returns:
        Filtered DataFrame with rows where the term appears

    Raises:
        ValueError: If required columns are missing
    """
    required_cols = {'leadin_sanitized', 'answers_sanitized', 'parts_sanitized'}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame missing required columns: {missing}")

    # Compile regex pattern for robust, case-insensitive substring match
    pattern = re.compile(re.escape(term), re.IGNORECASE)

    def match_in_text(text):
        if isinstance(text, str):
            return bool(pattern.search(text))
        return False

    def match_in_list(lst):
        if isinstance(lst, (list, tuple)):
            return any(isinstance(item, str) and pattern.search(item) for item in lst)
        return False

    mask = (
        df['leadin_sanitized'].apply(match_in_text)
        | df['answers_sanitized'].apply(match_in_list)
        | df['parts_sanitized'].apply(match_in_list)
    )
    return df[mask]


def search_tossups(term: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Search for a term (case-insensitive) in both `question_sanitized`
    and `answer_sanitized` columns of a tossups DataFrame.

    Args:
        term: The search term
        df: Tossups DataFrame with sanitized columns

    Returns:
        Filtered DataFrame with rows where the term appears

    Raises:
        ValueError: If required columns are missing
    """
    required_cols = {'question_sanitized', 'answer_sanitized'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"DataFrame must have columns: {required_cols}")

    pattern = re.compile(re.escape(term), re.IGNORECASE)

    def match(text):
        if isinstance(text, str):
            return bool(pattern.search(text))
        return False

    mask = df['question_sanitized'].apply(match) | df['answer_sanitized'].apply(match)
    return df[mask]
