"""
Ensemble Topic matcher: embedding (multilingual-e5-base) + BM25.

Fusion strategy
---------------
For each paper we collect top-K candidates from both rankers, merge
the candidate pools, and compute a weighted final score:

    final_score(topic) = w_emb * emb_score + w_bm25 * bm25_score

where missing scores default to 0.  The topic with the highest
``final_score`` becomes ``primary_topic``; the next two become
``topics[1]`` and ``topics[2]``.

Default weights: embedding=0.75, BM25=0.25.
BM25 acts as a "tiebreaker / keyword boost" rather than the primary signal.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .bm25_index   import BM25TopicIndex, BM25Match
from .embeddings   import EmbeddingModel, ModelType
from .language     import is_japanese
from .ndc_mapping  import NDCMapper, NDCMatch
from .topic_index  import TopicIndex, TopicMatch


# ────────────────────────────────────────────────────────────────────────
# Result dataclass
# ────────────────────────────────────────────────────────────────────────

@dataclass
class EnsembleResult:
    topic_id:    str
    topic_name:  str
    field:       str
    subfield:    str
    domain:      str
    confidence:  float   # weighted ensemble score [0, 1]
    emb_score:   float   # raw embedding cosine similarity
    bm25_score:  float   # normalised BM25 score
    method:      str     # "ensemble" | "embedding_only" | "skipped"

    candidates: list[dict] = field(default_factory=list)
    # Each dict: {topic_id, display_name, emb_score, bm25_score, final_score}


# ────────────────────────────────────────────────────────────────────────
# EnsembleMatcher
# ────────────────────────────────────────────────────────────────────────

class EnsembleMatcher:
    """Combine FAISS embedding search + BM25 keyword matching."""

    def __init__(
        self,
        emb_index:   TopicIndex,
        bm25_index:  BM25TopicIndex,
        emb_model:   EmbeddingModel,
        ndc_mapper:  NDCMapper | None = None,
        w_emb:       float = 0.75,
        w_bm25:      float = 0.25,
        top_k:       int   = 10,
    ) -> None:
        assert abs(w_emb + w_bm25 - 1.0) < 1e-6, "weights must sum to 1"
        self.emb_index  = emb_index
        self.bm25_index = bm25_index
        self.emb_model  = emb_model
        self.ndc_mapper = ndc_mapper or NDCMapper()
        self.w_emb      = w_emb
        self.w_bm25     = w_bm25
        self.top_k      = top_k

    # ------------------------------------------------------------------ #
    # Factory                                                              #
    # ------------------------------------------------------------------ #

    @classmethod
    def load(
        cls,
        index_dir:  str | Path,
        model_type: ModelType | str = ModelType.MULTILINGUAL_E5_BASE,
        w_emb:      float = 0.75,
        w_bm25:     float = 0.25,
        top_k:      int   = 10,
    ) -> "EnsembleMatcher":
        d = Path(index_dir)
        emb_index  = TopicIndex.load(d)
        bm25_index = BM25TopicIndex.load(d / "topics_meta.json")
        emb_model  = EmbeddingModel(model_type)
        return cls(emb_index, bm25_index, emb_model,
                   w_emb=w_emb, w_bm25=w_bm25, top_k=top_k)

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def match(
        self,
        title:    str,
        abstract: str = "",
        japanese_only: bool = False,
    ) -> EnsembleResult:
        return self.match_many(
            [{"title": title, "abstract": abstract}],
            japanese_only=japanese_only,
        )[0]

    def match_many(
        self,
        papers: list[dict],
        japanese_only: bool = False,
    ) -> list[EnsembleResult]:
        """Batch-encode + batch-BM25 + fuse."""
        n = len(papers)
        out: list[EnsembleResult] = [None] * n  # type: ignore

        to_encode_idx: list[int] = []
        texts: list[str] = []

        for i, paper in enumerate(papers):
            title    = paper.get("title", "") or ""
            abstract = paper.get("abstract", "") or ""
            language = paper.get("language")
            if japanese_only and not is_japanese(title, abstract, language):
                out[i] = _skipped_result()
                continue
            to_encode_idx.append(i)
            texts.append(title if not abstract else f"{title} [SEP] {abstract}")

        if not texts:
            return out

        # ── 1. Embedding batch encode + FAISS search ──────────────────
        query_matrix = self.emb_model.encode(texts, is_query=True)
        emb_candidates = self.emb_index.query_batch(query_matrix, top_k=self.top_k)

        # ── 2. BM25 batch search ──────────────────────────────────────
        bm25_candidates = self.bm25_index.query_batch(texts, top_k=self.top_k)

        # ── 3. Fuse per paper ─────────────────────────────────────────
        for j, i in enumerate(to_encode_idx):
            out[i] = self._fuse(emb_candidates[j], bm25_candidates[j])

        return out

    def match_batch(
        self,
        papers:        list[dict],
        japanese_only: bool = False,
        chunk_size:    int  = 256,
    ) -> list[EnsembleResult]:
        """Process papers in memory-bounded chunks."""
        results: list[EnsembleResult] = []
        for start in range(0, len(papers), chunk_size):
            chunk = papers[start : start + chunk_size]
            results.extend(self.match_many(chunk, japanese_only=japanese_only))
        return results

    # ------------------------------------------------------------------ #
    # Internals                                                            #
    # ------------------------------------------------------------------ #

    def _fuse(
        self,
        emb_cands:  list[TopicMatch],
        bm25_cands: list[BM25Match],
    ) -> EnsembleResult:
        """Merge embedding + BM25 candidates and pick the best."""
        # Build score dicts keyed by topic_id
        emb_scores:  dict[str, float] = {c.topic_id: c.score for c in emb_cands}
        bm25_scores: dict[str, float] = {c.topic_id: c.score for c in bm25_cands}

        # Union of all candidate topic IDs
        all_ids = set(emb_scores) | set(bm25_scores)

        # Build a lookup for topic metadata from embedding candidates
        meta: dict[str, TopicMatch] = {c.topic_id: c for c in emb_cands}
        for c in bm25_cands:
            if c.topic_id not in meta:
                # Create a compatible stub from BM25 result
                meta[c.topic_id] = TopicMatch(
                    topic_id    = c.topic_id,
                    display_name= c.display_name,
                    field       = c.field,
                    subfield    = c.subfield,
                    domain      = c.domain,
                    score       = 0.0,
                )

        # Compute final weighted scores
        scored: list[dict] = []
        for tid in all_ids:
            e = emb_scores.get(tid, 0.0)
            b = bm25_scores.get(tid, 0.0)
            f = self.w_emb * e + self.w_bm25 * b
            scored.append({
                "topic_id":    tid,
                "display_name": meta[tid].display_name,
                "field":        meta[tid].field,
                "subfield":     meta[tid].subfield,
                "domain":       meta[tid].domain,
                "emb_score":   e,
                "bm25_score":  b,
                "final_score": f,
            })

        scored.sort(key=lambda x: x["final_score"], reverse=True)
        best = scored[0]

        # Determine method label
        if bm25_scores.get(best["topic_id"], 0.0) > 0:
            method = "ensemble"
        else:
            method = "embedding_only"

        return EnsembleResult(
            topic_id   = best["topic_id"],
            topic_name = best["display_name"],
            field      = best["field"],
            subfield   = best["subfield"],
            domain     = best["domain"],
            confidence = best["final_score"],
            emb_score  = best["emb_score"],
            bm25_score = best["bm25_score"],
            method     = method,
            candidates = scored[:self.top_k],
        )


# ────────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────────

def _skipped_result() -> EnsembleResult:
    return EnsembleResult(
        topic_id="", topic_name="", field="", subfield="", domain="",
        confidence=0.0, emb_score=0.0, bm25_score=0.0, method="skipped",
    )
