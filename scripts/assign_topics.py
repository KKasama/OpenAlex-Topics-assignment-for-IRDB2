#!/usr/bin/env python3
"""
Assign OpenAlex Topics to IRDB records using an Ensemble approach.

Ensemble: multilingual-e5-base (embedding) + BM25 (keyword matching)

Fusion: final_score = w_emb * emb_score + w_bm25 * bm25_score
Default weights: embedding=0.75, BM25=0.25

Output is OpenAlex Work schema-aligned:
    primary_topic  : {id, display_name, score}
    topics         : [{id, display_name, score}, ...]  (top-n, default 3)
    method         : "ensemble" | "embedding_only" | "skipped"
    emb_score      : raw embedding cosine similarity
    bm25_score     : normalised BM25 score

Usage
-----
    python scripts/assign_topics.py \\
        --index-dir ./index-base \\
        --input  data/works-irdb-ja.jsonl \\
        --output data/topics-irdb-ja-ensemble.jsonl \\
        --minimal --top-n 3

    # Adjust ensemble weights
    python scripts/assign_topics.py \\
        --index-dir ./index-base \\
        --input  data/works-irdb-ja.jsonl \\
        --output data/topics-irdb-ja-ensemble.jsonl \\
        --minimal --top-n 3 --w-emb 0.6 --w-bm25 0.4
"""

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.embeddings       import ModelType
from src.ensemble_matcher import EnsembleMatcher

CHUNK_SIZE    = 256
PROGRESS_EVERY = 1000


# ────────────────────────────────────────────────────────────────────────
# Row builders
# ────────────────────────────────────────────────────────────────────────

def _work_id(record: dict) -> str:
    for key in ("id", "work_id", "openalex_id", "url"):
        v = record.get(key)
        if v:
            return str(v)
    return ""


def _topic_obj(c: dict, score_key: str = "final_score") -> dict:
    return {
        "id":           c.get("topic_id", ""),
        "display_name": c.get("display_name", ""),
        "score":        round(c.get(score_key, 0.0), 4),
    }


def _build_row(record: dict, result, top_n: int) -> dict:
    """Build OpenAlex-aligned output row."""
    cands = list(result.candidates or [])

    if not cands:
        pt = {"id": result.topic_id, "display_name": result.topic_name,
              "score": round(result.confidence, 4)}
        return {
            "work_id":       _work_id(record),
            "primary_topic": pt,
            "topics":        [pt],
            "method":        result.method,
            "emb_score":     round(result.emb_score, 4),
            "bm25_score":    round(result.bm25_score, 4),
        }

    # Ensure primary is first in candidates list
    if cands[0]["topic_id"] != result.topic_id:
        for i, c in enumerate(cands):
            if c["topic_id"] == result.topic_id:
                cands.insert(0, cands.pop(i))
                break

    topics = [
        {"id": c["topic_id"], "display_name": c["display_name"],
         "score": round(c["final_score"], 4)}
        for c in cands[:max(top_n, 1)]
    ]

    return {
        "work_id":       _work_id(record),
        "primary_topic": topics[0] if topics else None,
        "topics":        topics,
        "method":        result.method,
        "emb_score":     round(result.emb_score, 4),
        "bm25_score":    round(result.bm25_score, 4),
    }


# ────────────────────────────────────────────────────────────────────────
# I/O
# ────────────────────────────────────────────────────────────────────────

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


def _flush_chunk(chunk, matcher, out_stream, *, japanese_only, top_n):
    results = matcher.match_many(chunk, japanese_only=japanese_only)
    written = skipped = 0
    for record, result in zip(chunk, results):
        if result.method == "skipped":
            skipped += 1
            continue
        row = _build_row(record, result, top_n)
        out_stream.write(json.dumps(row, ensure_ascii=False) + "\n")
        written += 1
    return written, skipped


# ────────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Assign OpenAlex Topics via embedding + BM25 ensemble"
    )
    ap.add_argument("--index-dir", default="./index-base")
    ap.add_argument("--input",  default=None)
    ap.add_argument("--output", default=None)
    ap.add_argument("--model",  default=ModelType.MULTILINGUAL_E5_BASE.value)
    ap.add_argument("--top-k",  type=int, default=10,
                    help="Candidates retrieved per ranker (default 10)")
    ap.add_argument("--top-n",  type=int, default=3,
                    help="Topics emitted per work in output (default 3)")
    ap.add_argument("--w-emb",  type=float, default=0.75,
                    help="Weight for embedding score (default 0.75)")
    ap.add_argument("--w-bm25", type=float, default=0.25,
                    help="Weight for BM25 score (default 0.25)")
    ap.add_argument(
        "--japanese-only", dest="japanese_only",
        action="store_true", default=True,
    )
    ap.add_argument(
        "--no-japanese-only", dest="japanese_only",
        action="store_false",
    )
    ap.add_argument("--minimal", action="store_true",
                    help="Minimal output (work_id + topics only)")
    args = ap.parse_args()

    # Validate weights
    if abs(args.w_emb + args.w_bm25 - 1.0) > 1e-4:
        print("Error: --w-emb + --w-bm25 must equal 1.0", file=sys.stderr)
        sys.exit(1)

    print(
        f"Loading ensemble matcher (emb={args.w_emb}, bm25={args.w_bm25}) ...",
        file=sys.stderr
    )
    matcher = EnsembleMatcher.load(
        index_dir  = args.index_dir,
        model_type = args.model,
        w_emb      = args.w_emb,
        w_bm25     = args.w_bm25,
        top_k      = max(args.top_k, args.top_n),
    )
    print("Matcher ready. Starting processing ...", file=sys.stderr)

    out_stream = (
        open(args.output, "w", encoding="utf-8") if args.output else sys.stdout
    )

    written = skipped = processed = 0
    chunk: list[dict] = []
    start = time.time()
    next_log_at = PROGRESS_EVERY

    try:
        for _, record in _iter_jsonl(args.input):
            chunk.append(record)
            processed += 1
            if len(chunk) >= CHUNK_SIZE:
                w, s = _flush_chunk(
                    chunk, matcher, out_stream,
                    japanese_only=args.japanese_only,
                    top_n=args.top_n,
                )
                written += w; skipped += s; chunk = []
                if processed >= next_log_at and args.output:
                    elapsed = time.time() - start
                    rate = processed / elapsed if elapsed else 0
                    print(
                        f"  processed {processed:,} "
                        f"({rate:,.1f}/s, {elapsed/60:.1f} min)",
                        file=sys.stderr, flush=True,
                    )
                    next_log_at = (
                        (processed // PROGRESS_EVERY) + 1
                    ) * PROGRESS_EVERY
        if chunk:
            w, s = _flush_chunk(
                chunk, matcher, out_stream,
                japanese_only=args.japanese_only,
                top_n=args.top_n,
            )
            written += w; skipped += s
    finally:
        if args.output:
            out_stream.close()

    if args.output:
        elapsed = time.time() - start
        print(
            f"Wrote {written:,} lines to {args.output} "
            f"(reassigned {written:,}, skipped {skipped:,} non-Japanese) "
            f"in {elapsed/60:.1f} min",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
