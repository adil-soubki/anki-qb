"""Text processing and normalization utilities."""

import html
import unicodedata


def normalize_text(s: str) -> str:
    """
    Normalize a string by:
    - Unescaping HTML entities
    - Replacing non-breaking spaces with normal spaces
    - Converting fancy quotes and dashes to plain ASCII equivalents
    - Removing extra whitespace

    Args:
        s: The string to normalize

    Returns:
        The normalized string
    """
    if not s:
        return ""

    # 1. Unescape HTML entities
    s = html.unescape(s)

    # 2. Replace non-breaking spaces and other common unicode spaces
    s = s.replace("\xa0", " ").replace("\u200b", "").replace("\u202f", " ")

    # 3. Normalize unicode to NFKD form to separate accents
    s = unicodedata.normalize("NFKD", s)

    # 4. Replace fancy quotes and dashes with simple equivalents
    replacements = {
        """: '"',
        """: '"',
        "'": "'",
        "'": "'",
        "–": "-",
        "—": "-",
        "…": "...",
    }
    for k, v in replacements.items():
        s = s.replace(k, v)

    # 5. Collapse multiple spaces to a single space
    s = " ".join(s.split())

    return s
