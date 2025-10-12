"""Parsing functions for NAQT 'You Gotta Know' articles."""

import lxml.html
from more_itertools import first, one

from anki_qb.text_utils import normalize_text


def ygk_path(category_or_path: str, base_dir: str = "data/ygk") -> str:
    """
    Maps article category to HTML file path.

    Args:
        category_or_path: Either a category name or a direct path to HTML file
        base_dir: Base directory where HTML files are stored

    Returns:
        Path to the HTML file
    """
    if category_or_path.endswith(".html"):
        return category_or_path
    category = category_or_path.lower().replace(" ", "_")
    filename = f"https___www_naqt_com_you_gotta_know_{category}_html.html"
    return f"{base_dir}/{filename}"


def read_html(path: str) -> lxml.html.HtmlElement:
    """
    Read an HTML file and parse it into an lxml element tree.

    Args:
        path: Path to the HTML file

    Returns:
        Parsed HTML element tree
    """
    with open(path, "r") as f:
        text = f.read()
    return lxml.html.fromstring(text)


def parse_ygk_page_ul(path: str) -> list[dict[str, str]]:
    """
    Parse a 'You Gotta Know' page that uses <ul> structure.

    Args:
        path: Path to the HTML file or category name

    Returns:
        List of dictionaries containing article, label, terms, html, and text
    """
    ret = []
    tree = read_html(path)
    article = normalize_text(first(tree.xpath("//h1")).text)
    assert article.lower().startswith("you gotta know")

    for li in tree.xpath("//ul[@class='ygk']/li"):
        ret.append({
            "article": article,
            "label": normalize_text(one(li.xpath("./span[@class='label']")).text),
            "terms": [normalize_text(t.text) for t in li.xpath("./span[@class='ygk-term']")],
            "html": normalize_text(lxml.html.tostring(li).decode("ascii").strip()),
            "text": normalize_text(li.text_content())
        })
    return ret


def parse_ygk_page_dl(path: str) -> list[dict[str, str]]:
    """
    Parse a 'You Gotta Know' page that uses <dl> structure.
    Some pages have a dl instead of ul.

    Args:
        path: Path to the HTML file or category name

    Returns:
        List of dictionaries containing article, label, terms, html, and text
    """
    ret = []
    tree = read_html(path)
    article = normalize_text(first(tree.xpath("//h1")).text)
    assert article.lower().startswith("you gotta know")

    labels = tree.xpath("//dl[@class='ygk']/dt")
    assert len(tree.xpath("//dl[@class='ygk']/dd")) == len(labels)

    for label, dd in zip(labels, tree.xpath("//dl[@class='ygk']/dd")):
        ret.append({
            "article": article,
            "label": normalize_text(label.text),
            "terms": [normalize_text(t.text) for t in dd.xpath("./span[@class='ygk-term']")],
            "html": normalize_text(lxml.html.tostring(dd).decode("ascii").strip()),
            "text": normalize_text(dd.text_content())
        })
    return ret


def parse_ygk_page(path: str) -> list[dict[str, str]]:
    """
    Parse a 'You Gotta Know' page, automatically detecting structure type.

    Args:
        path: Path to the HTML file or category name

    Returns:
        List of dictionaries containing article, label, terms, html, and text
    """
    ret = parse_ygk_page_ul(path)
    if not ret:
        ret = parse_ygk_page_dl(path)
    return ret
