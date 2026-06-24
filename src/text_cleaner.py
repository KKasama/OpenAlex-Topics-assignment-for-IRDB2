"""
Preprocessing utilities for IRDB paper texts before translation/embedding.

Key problems found in the data:
  1. Repository boilerplate abstracts ("UTokyo Repository は本学で生産された…")
  2. Inverted-index-decoded abstracts with spaces ("H i g u c h i 2 0 0 4")
  3. English titles with Japanese abstracts (need separate handling)
"""

from __future__ import annotations

import re

_JP_RE = re.compile(r"[ぁ-ゟ゠-ヿ一-鿿]")

# Patterns that indicate a boilerplate / metadata abstract
_BOILERPLATE_RE = re.compile(
    r"UTokyo Repository|リポジトリ.{0,20}本学|本学.{0,20}生産|"
    r"機関リポジトリ|本リポジトリ|学術機関リポジトリ|JAIRO|"
    r"DSpace|学術成果を電子的"
)

# Inverted-index decoded: single chars separated by spaces, e.g. "H i g u c h i"
_SPACED_CHARS_RE = re.compile(r"(?<!\w)([a-zA-Z0-9]) (?=[a-zA-Z0-9] )")


def is_boilerplate(text: str) -> bool:
    """Return True if the text is repository metadata, not a real abstract."""
    if not text:
        return False
    return bool(_BOILERPLATE_RE.search(text))


def is_spaced_inverted_index(text: str) -> bool:
    """Return True if text looks like a decoded inverted index (chars with spaces)."""
    if not text or len(text) < 10:
        return False
    # Count space-separated single-character sequences
    single_chars = re.findall(r"(?<!\w)[a-zA-Z0-9](?!\w)", text)
    return len(single_chars) > len(text.split()) * 0.5


def clean_abstract(text: str) -> str:
    """Return a cleaned abstract, or empty string if it should be discarded."""
    if not text:
        return ""
    if is_boilerplate(text):
        return ""
    if is_spaced_inverted_index(text):
        return ""
    return text.strip()


def paper_texts(record: dict) -> tuple[str, str]:
    """
    Return (title, abstract) with abstract cleaned.
    If abstract is boilerplate or garbled, returns ("", "").
    """
    title    = (record.get("title") or "").strip()
    abstract = clean_abstract(record.get("abstract") or "")
    return title, abstract


def combined_text(title: str, abstract: str) -> str:
    """Combine title and abstract for embedding (no [SEP] if abstract empty)."""
    if abstract:
        return f"{title} {abstract}"
    return title
