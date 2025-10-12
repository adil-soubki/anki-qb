"""Formatting utilities for QBReader data and markdown tables."""

import re
import pandas as pd

from anki_qb.parsing import parse_ygk_page_dl


def format_qa(df: pd.DataFrame) -> list[str]:
    """
    Format a tossup or bonus DataFrame into a list of readable strings
    containing the question(s) and answer(s).

    Works with:
      - Tossups: uses `question_sanitized` and `answer_sanitized`
      - Bonuses: uses `leadin_sanitized`, `parts_sanitized`, and `answers_sanitized`

    Args:
        df: DataFrame containing tossup or bonus data

    Returns:
        List of strings, one per row
    """
    formatted = []

    for _, row in df.iterrows():
        # Detect bonus vs tossup
        if {'leadin_sanitized', 'parts_sanitized', 'answers_sanitized'}.issubset(row.index):
            leadin = row.get('leadin_sanitized', '')
            parts = row.get('parts_sanitized', [])
            answers = row.get('answers_sanitized', [])

            # Make sure parts and answers are lists
            parts = parts if isinstance(parts, (list, tuple)) else [parts]
            answers = answers if isinstance(answers, (list, tuple)) else [answers]

            qa_text = f"Leadin: {leadin.strip() if isinstance(leadin, str) else ''}\n"
            for i, (p, a) in enumerate(zip(parts, answers), start=1):
                p_str = p.strip() if isinstance(p, str) else ""
                a_str = a.strip() if isinstance(a, str) else ""
                qa_text += f"  Part {i}: {p_str}\n  Answer: {a_str}\n"

            formatted.append(qa_text.strip())

        elif {'question_sanitized', 'answer_sanitized'}.issubset(row.index):
            question = row.get('question_sanitized', '')
            answer = row.get('answer_sanitized', '')
            q_str = question.strip() if isinstance(question, str) else ""
            a_str = answer.strip() if isinstance(answer, str) else ""
            formatted.append(f"Question: {q_str}\nAnswer: {a_str}")

        else:
            # Unknown schema — skip row
            continue

    return formatted


def format_ygk_prompt(data: dict[str, str], prompt_template: str, qbr_data: dict[str, str]) -> str:
    """
    Format a YGK article data dict into a prompt using the given template.

    Args:
        data: Dictionary with article, label, text, and terms
        prompt_template: Prompt template string with format placeholders
        qbr_data: Dictionary with QBReader data (tossups, bonuses)

    Returns:
        Formatted prompt string
    """
    # From YGK article
    category = data["article"].lower().replace("You Gotta Know These ", "")
    topic = data["label"]
    text = data["text"]
    for term in data["terms"]:
        text = text.replace(term, f"**{term}**")

    return prompt_template.format(
        category=category,
        topic=topic,
        text=text,
        num_related_tossups=qbr_data["num_related_tossups"],
        tossups=qbr_data["tossups"],
        num_related_bonuses=qbr_data["num_related_bonuses"],
        bonuses=qbr_data["bonuses"],
    )


def format_ygk_prompts(path: str, prompt_template: str, get_qbr_data_fn) -> list[str]:
    """
    Parse a YGK page and format all topics into prompts.

    Args:
        path: Path to the HTML file or category name
        prompt_template: Prompt template string with format placeholders
        get_qbr_data_fn: Function to get QBReader data for a given YGK data dict

    Returns:
        List of formatted prompt strings
    """
    ret = []
    for data in parse_ygk_page_dl(path):
        qbr_data = get_qbr_data_fn(data)
        ret.append(format_ygk_prompt(data, prompt_template, qbr_data))
    return ret


def read_markdown(markdown_text: str) -> pd.DataFrame:
    """
    Reads a Markdown-formatted table into a pandas DataFrame.

    Args:
        markdown_text: The Markdown table as a string

    Returns:
        DataFrame containing the parsed table
    """
    lines = [l.strip() for l in markdown_text.strip().splitlines() if l.strip()]
    lines = [re.sub(r'^\||\|$', '', l) for l in lines]  # remove outer pipes
    lines = [re.split(r'\s*\|\s*', l) for l in lines if not re.match(r'^\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\s*$', l)]
    header, *rows = lines
    rows = [[r.strip() for r in row] for row in rows]
    return pd.DataFrame(rows, columns=[h.strip() for h in header])
