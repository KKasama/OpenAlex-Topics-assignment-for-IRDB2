"""
BM25-based Topic index using topic keywords / display_name / description.

Tokenisation strategy
---------------------
Topics are in English; papers are in Japanese (with occasional English
terms). We bridge the gap with two signals:

1. **English token overlap** — many Japanese academic papers contain
   English technical terms, acronyms, or English abstracts/keywords.
   BM25 on simple word tokens catches these matches.

2. **CJK character bigrams** — when topic descriptions or paper text
   contain CJK characters, bigram overlap gives a language-agnostic
   similarity signal without needing a full morphological analyser.

Together these provide a lightweight complementary signal to the dense
embedding similarity used as the primary ranker.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

try:
    from rank_bm25 import BM25Okapi  # type: ignore
except ImportError as e:
    raise ImportError(
        "rank_bm25 is required for BM25 matching: pip install rank-bm25"
    ) from e


_WS_RE  = re.compile(r'[^\w぀-ゟ゠-ヿ一-鿿]+')
_CJK_RE = re.compile(r'[一-鿿぀-ゟ゠-ヿ]')


def tokenize(text: str) -> list[str]:
    """Tokenise text into English word-tokens + CJK character bigrams."""
    # English/ASCII tokens
    tokens = [t.lower() for t in _WS_RE.split(text) if t and len(t) > 1]
    # CJK bigrams
    cjk = _CJK_RE.findall(text)
    bigrams = [cjk[i] + cjk[i + 1] for i in range(len(cjk) - 1)]
    return tokens + bigrams


@dataclass
class BM25Match:
    topic_id: str
    display_name: str
    field: str
    subfield: str
    domain: str
    score: float   # normalised BM25 score in [0, 1]


def _safe_name(topic: dict, key: str) -> str:
    v = topic.get(key)
    return (v.get("display_name", "") if isinstance(v, dict) else v) or ""


class BM25TopicIndex:
    """BM25 index over topic keyword / description corpora."""

    def __init__(self, topics: list[dict], bm25: "BM25Okapi") -> None:
        self._topics = topics
        self._bm25   = bm25

    # ------------------------------------------------------------------ #
    # Factory                                                              #
    # ------------------------------------------------------------------ #

    @classmethod
    def load(cls, meta_path: str | Path) -> "BM25TopicIndex":
        """Build a BM25 index from the topics_meta.json file.

        The corpus for each topic is:
            display_name  +  keywords (joined)  +  description (first 300 chars)
        """
        topics: list[dict] = json.loads(Path(meta_path).read_text(encoding="utf-8"))
        corpus: list[list[str]] = []
        for t in topics:
            parts = [t.get("display_name", "")]
            parts += t.get("keywords", [])
            desc = t.get("description", "") or ""
            parts.append(desc[:300])
            corpus.append(tokenize(" ".join(parts)))

        bm25 = BM25Okapi(corpus)
        return cls(topics, bm25)

    # ------------------------------------------------------------------ #
    # Query                                                                #
    # ------------------------------------------------------------------ #

    def query(self, text: str, top_k: int = 5) -> list[BM25Match]:
        return self.query_batch([text], top_k=top_k)[0]

    def query_batch(
        self, texts: list[str], top_k: int = 5
    ) -> list[list[BM25Match]]:
        """Return top-k BM25 matches for each text.

        Scores are normalised per-query to [0, 1] so they are
        comparable with cosine similarity values from the embedding index.
        """
        results: list[list[BM25Match]] = []
        for text in texts:
            tokens = tokenize(text)
            raw_scores: np.ndarray = self._bm25.get_scores(tokens)

            # Normalise to [0, 1] relative to the query's max score.
            max_s = float(raw_scores.max())
            norm  = raw_scores / max_s if max_s > 0 else raw_scores

            top_idx = np.argpartition(norm, -top_k)[-top_k:]
            top_idx = top_idx[np.argsort(norm[top_idx])[::-1]]

            matches: list[BM25Match] = []
            for idx in top_idx:
                t = self._topics[idx]
                matches.append(
                    BM25Match(
                        topic_id    = t.get("id", ""),
                        display_name= t.get("display_name", ""),
                        field       = _safe_name(t, "field"),
                        subfield    = _safe_name(t, "subfield"),
                        domain      = _safe_name(t, "domain"),
                        score       = float(norm[idx]),
                    )
                )
            results.append(matches)
        return results
