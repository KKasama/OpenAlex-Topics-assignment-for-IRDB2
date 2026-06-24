"""
Hierarchical Topic search: select Domain first, then search within that Domain.

Instead of flat search across all 4,516 topics, this wrapper:
1. Fetches a large candidate pool (prefetch_k, default 50) from the full index.
2. Identifies the dominant domain via weighted plurality vote among top-20.
3. Returns only topics within that domain, reranked by embedding score.

This structurally prevents cross-domain confusion (e.g., medical → military).
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np

from .topic_index import TopicIndex, TopicMatch


class HierarchicalTopicIndex:
    """Domain-filtered wrapper around TopicIndex."""

    def __init__(self, index: TopicIndex, prefetch_k: int = 50) -> None:
        self._index = index
        self._prefetch_k = prefetch_k

    @classmethod
    def load(cls, dir_path, prefetch_k: int = 50) -> "HierarchicalTopicIndex":
        return cls(TopicIndex.load(dir_path), prefetch_k=prefetch_k)

    # ------------------------------------------------------------------
    # Public API  (mirrors TopicIndex)
    # ------------------------------------------------------------------

    def query(self, query_vec: np.ndarray, top_k: int = 5) -> list[TopicMatch]:
        return self.query_batch(query_vec, top_k=top_k)[0]

    def query_batch(
        self, query_matrix: np.ndarray, top_k: int = 5
    ) -> list[list[TopicMatch]]:
        q = np.atleast_2d(query_matrix)
        all_candidates = self._index.query_batch(q, top_k=self._prefetch_k)

        results: list[list[TopicMatch]] = []
        for candidates in all_candidates:
            domain = self._dominant_domain(candidates)
            filtered = [c for c in candidates if c.domain == domain]

            # Safety: if filtering leaves fewer than top_k, fall back to global
            if len(filtered) < min(top_k, 3):
                filtered = candidates

            results.append(filtered[:top_k])
        return results

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _dominant_domain(candidates: list[TopicMatch], vote_k: int = 20) -> str:
        """Plurality vote on domain using score-weighted sum over top vote_k."""
        if not candidates:
            return ""
        domain_scores: dict[str, float] = defaultdict(float)
        for c in candidates[:vote_k]:
            domain_scores[c.domain] += c.score
        return max(domain_scores, key=lambda d: domain_scores[d])
