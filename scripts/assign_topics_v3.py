#!/usr/bin/env python3
"""
Assign OpenAlex Topics — v3: Translation + Hierarchical + BM25 Ensemble.

Pipeline per paper
------------------
1. Translate Japanese title/abstract → English (translator selectable).
2. Embed English text with multilingual-e5-base.
3. Fetch top-50 candidates from FAISS and filter to dominant domain
   (hierarchical classification).
4. Run BM25 on the translated English text against topic keywords.
5. Fuse: final_score = w_emb * emb_score + w_bm25 * bm25_score.

Output is OpenAlex Work schema-aligned (same format as v1/v2).

Usage
-----
    # Gemini 2.0 Flash（推奨）
    export GEMINI_API_KEY="AIza..."
    python scripts/assign_topics_v3.py \\
        --index-dir ./index-base \\
        --input     data/works-1k.jsonl \\
        --output    data/topics-1k-v3-gemini.jsonl \\
        --translator gemini --top-n 3

    # OPUS-MT（ローカル・無料・品質低）
    python scripts/assign_topics_v3.py \\
        --index-dir ./index-base \\
        --input     data/works-1k.jsonl \\
        --output    data/topics-1k-v3.jsonl \\
        --translator opus --top-n 3
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.bm25_index          import BM25TopicIndex
from src.embeddings          import EmbeddingModel, ModelType
from src.hierarchical_index  import HierarchicalTopicIndex
from src.translator          import translate_batch as opus_translate_batch, needs_translation

CHUNK_SIZE     = 64   # smaller chunks due to translation overhead
PROGRESS_EVERY = 500


# ────────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────────

def _work_id(record: dict) -> str:
    for key in ("id", "work_id", "openalex_id", "url"):
        v = record.get(key)
        if v:
            return str(v)
    return ""


def _paper_text(record: dict) -> str:
    title    = record.get("title", "") or ""
    abstract = record.get("abstract", "") or ""
    if abstract:
        return f"{title} [SEP] {abstract}"
    return title


def _fuse(
    emb_cands,
    bm25_cands,
    w_emb:  float,
    w_bm25: float,
    top_n:  int,
) -> dict:
    emb_scores  = {c.topic_id: (c.score, c) for c in emb_cands}
    bm25_scores = {c.topic_id: c.score     for c in bm25_cands}

    all_ids = set(emb_scores) | set(bm25_scores)

    # Build metadata lookup
    meta = {tid: c for tid, (_, c) in emb_scores.items()}
    for c in bm25_cands:
        if c.topic_id not in meta:
            meta[c.topic_id] = c

    scored = []
    for tid in all_ids:
        e = emb_scores.get(tid, (0.0, None))[0]
        b = bm25_scores.get(tid, 0.0)
        f = w_emb * e + w_bm25 * b
        m = meta[tid]
        scored.append({
            "topic_id":    tid,
            "display_name": m.display_name,
            "field":        m.field if hasattr(m, "field") else "",
            "subfield":     m.subfield if hasattr(m, "subfield") else "",
            "domain":       m.domain if hasattr(m, "domain") else "",
            "emb_score":   round(e, 4),
            "bm25_score":  round(b, 4),
            "final_score": round(f, 4),
        })

    scored.sort(key=lambda x: x["final_score"], reverse=True)
    best = scored[0]
    topics = [
        {"id": c["topic_id"], "display_name": c["display_name"],
         "score": c["final_score"]}
        for c in scored[:max(top_n, 1)]
    ]

    method = "v3_ensemble" if bm25_scores.get(best["topic_id"], 0.0) > 0 else "v3_hierarchical"

    return {
        "primary_topic": topics[0],
        "topics":        topics,
        "method":        method,
        "emb_score":     best["emb_score"],
        "bm25_score":    best["bm25_score"],
    }


def _iter_jsonl(path: str | None):
    if path is None:
        for i, line in enumerate(sys.stdin, 1):
            line = line.strip()
            if line:
                try:
                    yield i, json.loads(line)
                except json.JSONDecodeError:
                    pass
        return
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    yield i, json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"  [warn] line {i}: {e}", file=sys.stderr)


# ────────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description="v3: Translation + Hierarchical + BM25 topic assignment"
    )
    ap.add_argument("--index-dir", default="./index-base")
    ap.add_argument("--input",  default=None)
    ap.add_argument("--output", default=None)
    ap.add_argument("--model",  default=ModelType.MULTILINGUAL_E5_BASE.value)
    ap.add_argument("--top-k",  type=int, default=50,
                    help="Prefetch candidates before hierarchical filter (default 50)")
    ap.add_argument("--top-n",  type=int, default=3,
                    help="Topics emitted per work (default 3)")
    ap.add_argument("--w-emb",  type=float, default=0.75)
    ap.add_argument("--w-bm25", type=float, default=0.25)
    ap.add_argument("--translator", choices=["gemini", "opus"], default="gemini",
                    help="Translation backend: gemini (recommended) or opus (local)")
    args = ap.parse_args()

    if abs(args.w_emb + args.w_bm25 - 1.0) > 1e-4:
        sys.exit("Error: --w-emb + --w-bm25 must equal 1.0")

    # ── translation backend ──────────────────────────────────────────
    if args.translator == "gemini":
        from src.translator_gemini import GeminiTranslator
        _gemini = GeminiTranslator()
        def translate_batch(texts: list[str]) -> list[str]:
            return _gemini.translate_batch(texts)
        print("Translator: Gemini 2.0 Flash", file=sys.stderr)
    else:
        translate_batch = opus_translate_batch
        print("Translator: OPUS-MT (local)", file=sys.stderr)

    d = Path(args.index_dir)
    print("Loading hierarchical index …", file=sys.stderr)
    hier_index = HierarchicalTopicIndex.load(d, prefetch_k=args.top_k)
    bm25_index = BM25TopicIndex.load(d / "topics_meta.json")
    emb_model  = EmbeddingModel(args.model)
    print("Indices ready.", file=sys.stderr)

    out_stream = (
        open(args.output, "w", encoding="utf-8") if args.output else sys.stdout
    )

    written = processed = translated_count = 0
    chunk_records: list[dict] = []
    start = time.time()
    next_log = PROGRESS_EVERY

    def flush(chunk: list[dict]) -> int:
        nonlocal translated_count

        raw_texts = [_paper_text(r) for r in chunk]

        # Step 1: translate Japanese → English
        en_texts = translate_batch(raw_texts)
        translated_count += sum(
            1 for orig, en in zip(raw_texts, en_texts) if needs_translation(orig)
        )

        # Step 2: embed English texts
        query_matrix = emb_model.encode(en_texts, is_query=True)

        # Step 3: hierarchical (domain-filtered) FAISS search
        emb_cands_batch = hier_index.query_batch(query_matrix, top_k=args.top_k)

        # Step 4: BM25 on English text
        bm25_cands_batch = bm25_index.query_batch(en_texts, top_k=10)

        written_local = 0
        for record, emb_cands, bm25_cands, en_text in zip(
            chunk, emb_cands_batch, bm25_cands_batch, en_texts
        ):
            row = {
                "work_id": _work_id(record),
                "translated_title": en_text,
            }
            row.update(_fuse(emb_cands, bm25_cands, args.w_emb, args.w_bm25, args.top_n))
            out_stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            written_local += 1
        return written_local

    try:
        for _, record in _iter_jsonl(args.input):
            chunk_records.append(record)
            processed += 1
            if len(chunk_records) >= CHUNK_SIZE:
                written += flush(chunk_records)
                chunk_records = []
                if args.output and processed >= next_log:
                    elapsed = time.time() - start
                    rate = processed / elapsed if elapsed else 0
                    print(
                        f"  processed {processed:,} ({rate:.1f}/s, "
                        f"translated {translated_count:,}, {elapsed/60:.1f} min)",
                        file=sys.stderr, flush=True,
                    )
                    next_log = ((processed // PROGRESS_EVERY) + 1) * PROGRESS_EVERY
        if chunk_records:
            written += flush(chunk_records)
    finally:
        if args.output:
            out_stream.close()

    if args.output:
        elapsed = time.time() - start
        print(
            f"Wrote {written:,} lines → {args.output}  "
            f"(translated {translated_count:,} papers, {elapsed/60:.1f} min)",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
