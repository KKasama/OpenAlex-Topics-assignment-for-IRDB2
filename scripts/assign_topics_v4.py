#!/usr/bin/env python3
"""
Assign OpenAlex Topics — v4: Translator × Embedding model comparison.

Fixes vs v3
-----------
  - Boilerplate abstracts ("UTokyo Repository…") are detected and removed.
  - Title and abstract are translated SEPARATELY, then combined.
  - Supports two translators: fugumt (local) | gemini (API).
  - Supports two embedding models: e5 (multilingual-e5-base) | scibert.
  - No hierarchical filtering (removed — was hurting accuracy in tests).
  - BM25 still included at default weight 0.10 (validated in BM25 sweep).

Usage
-----
    # FuguMT + e5-base（ローカル・無料）
    python scripts/assign_topics_v4.py \\
        --translator fugumt --emb-model e5 \\
        --index-dir  ./index-base \\
        --input  data/works-1k.jsonl \\
        --output data/topics-1k-v4-fugumt-e5.jsonl

    # Gemini + e5-base
    export GEMINI_API_KEY="AIza..."
    python scripts/assign_topics_v4.py \\
        --translator gemini --emb-model e5 \\
        --index-dir  ./index-base \\
        --input  data/works-1k.jsonl \\
        --output data/topics-1k-v4-gemini-e5.jsonl

    # FuguMT + SciBERT（先にindex-scibertを構築すること）
    python scripts/assign_topics_v4.py \\
        --translator fugumt --emb-model scibert \\
        --index-dir  ./index-scibert \\
        --input  data/works-1k.jsonl \\
        --output data/topics-1k-v4-fugumt-scibert.jsonl

    # Gemini + SciBERT
    python scripts/assign_topics_v4.py \\
        --translator gemini --emb-model scibert \\
        --index-dir  ./index-scibert \\
        --input  data/works-1k.jsonl \\
        --output data/topics-1k-v4-gemini-scibert.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.bm25_index         import BM25TopicIndex
from src.embeddings         import EmbeddingModel, ModelType
from src.text_cleaner       import paper_texts, combined_text
from src.topic_index        import TopicIndex

CHUNK_SIZE     = 32   # smaller chunks for translation overhead
PROGRESS_EVERY = 200

EMB_MODEL_MAP = {
    "e5":       ModelType.MULTILINGUAL_E5_BASE,
    "e5-large": "intfloat/multilingual-e5-large",
    "scibert":  "allenai/scibert_scivocab_uncased",
}


# ────────────────────────────────────────────────────────────────────────
# Translation helpers
# ────────────────────────────────────────────────────────────────────────

def _make_translator(name: str):
    """Return a translate_batch(list[str]) -> list[str] function."""
    if name == "none":
        return lambda texts: list(texts)  # pass-through, no translation
    elif name == "fugumt":
        from src.translator_fugumt import translate_batch
        return translate_batch
    elif name == "gemini":
        from src.translator_gemini import GeminiTranslator
        tr = GeminiTranslator()
        return tr.translate_batch
    else:
        raise ValueError(f"Unknown translator: {name}")


def _translate_papers(records: list[dict], translate_batch) -> list[str]:
    """
    Translate title and abstract separately, clean boilerplate, combine.
    Returns one translated text string per record.
    """
    titles    = []
    abstracts = []
    for r in records:
        t, a = paper_texts(r)
        titles.append(t)
        abstracts.append(a)

    # Translate titles
    en_titles    = translate_batch(titles)
    # Translate abstracts (only non-empty ones)
    en_abstracts = translate_batch(abstracts)

    return [combined_text(t, a) for t, a in zip(en_titles, en_abstracts)]


# ────────────────────────────────────────────────────────────────────────
# Fusion
# ────────────────────────────────────────────────────────────────────────

def _fuse(emb_cands, bm25_cands, w_emb: float, w_bm25: float, top_n: int) -> dict:
    emb_map  = {c.topic_id: (c.score, c) for c in emb_cands}
    bm25_map = {c.topic_id: c.score      for c in bm25_cands}
    all_ids  = set(emb_map) | set(bm25_map)
    meta     = {tid: c for tid, (_, c) in emb_map.items()}
    for c in bm25_cands:
        if c.topic_id not in meta:
            meta[c.topic_id] = c

    scored = []
    for tid in all_ids:
        e = emb_map.get(tid,  (0.0, None))[0]
        b = bm25_map.get(tid, 0.0)
        scored.append({
            "topic_id":    tid,
            "display_name": meta[tid].display_name,
            "emb_score":   round(e, 4),
            "bm25_score":  round(b, 4),
            "final_score": round(w_emb * e + w_bm25 * b, 4),
        })
    scored.sort(key=lambda x: x["final_score"], reverse=True)
    best   = scored[0]
    topics = [{"id": c["topic_id"], "display_name": c["display_name"],
               "score": c["final_score"]} for c in scored[:max(top_n, 1)]]
    method = "v4_ensemble" if bm25_map.get(best["topic_id"], 0.0) > 0 else "v4_embedding"
    return {
        "primary_topic": topics[0],
        "topics":        topics,
        "method":        method,
        "emb_score":     best["emb_score"],
        "bm25_score":    best["bm25_score"],
    }


# ────────────────────────────────────────────────────────────────────────
# I/O
# ────────────────────────────────────────────────────────────────────────

def _work_id(r: dict) -> str:
    for k in ("id", "work_id", "openalex_id"):
        v = r.get(k)
        if v:
            return str(v)
    return ""


def _iter_jsonl(path):
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    pass


# ────────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description="v4: Translator × Embedding model comparison pipeline"
    )
    ap.add_argument("--translator", choices=["none", "fugumt", "gemini"], required=True)
    ap.add_argument("--emb-model",  choices=["e5", "e5-large", "scibert"], required=True)
    ap.add_argument("--index-dir",  required=True)
    ap.add_argument("--input",      required=True)
    ap.add_argument("--output",     required=True)
    ap.add_argument("--top-k",  type=int,   default=10)
    ap.add_argument("--top-n",  type=int,   default=3)
    ap.add_argument("--w-emb",  type=float, default=0.90)
    ap.add_argument("--w-bm25", type=float, default=0.10)
    args = ap.parse_args()

    if abs(args.w_emb + args.w_bm25 - 1.0) > 1e-4:
        sys.exit("Error: --w-emb + --w-bm25 must equal 1.0")

    d = Path(args.index_dir)
    print(f"Translator : {args.translator}", file=sys.stderr)
    print(f"Emb model  : {args.emb_model}",  file=sys.stderr)
    print(f"Index dir  : {d}",                file=sys.stderr)

    translate_batch = _make_translator(args.translator)

    emb_model_id = EMB_MODEL_MAP[args.emb_model]
    print(f"Loading embedding model {emb_model_id} …", file=sys.stderr)
    emb_model  = EmbeddingModel(emb_model_id)
    topic_idx  = TopicIndex.load(d)
    bm25_idx   = BM25TopicIndex.load(d / "topics_meta.json")
    print("Ready.", file=sys.stderr)

    out = open(args.output, "w", encoding="utf-8")
    written = processed = translated = 0
    chunk: list[dict] = []
    start = time.time()
    next_log = PROGRESS_EVERY

    def flush(chunk):
        nonlocal written, translated
        en_texts = _translate_papers(chunk, translate_batch)
        translated += sum(1 for t in en_texts if t)
        q_matrix   = emb_model.encode(en_texts, is_query=True)
        emb_batch  = topic_idx.query_batch(q_matrix, top_k=args.top_k)
        bm25_batch = bm25_idx.query_batch(en_texts, top_k=args.top_k)
        for record, emb_c, bm25_c, en_text in zip(chunk, emb_batch, bm25_batch, en_texts):
            row = {"work_id": _work_id(record), "translated_title": en_text[:120]}
            row.update(_fuse(emb_c, bm25_c, args.w_emb, args.w_bm25, args.top_n))
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            written += 1

    try:
        for record in _iter_jsonl(args.input):
            chunk.append(record)
            processed += 1
            if len(chunk) >= CHUNK_SIZE:
                flush(chunk); chunk = []
                if processed >= next_log:
                    elapsed = time.time() - start
                    print(f"  {processed:,} processed ({processed/elapsed:.1f}/s, "
                          f"{elapsed/60:.1f} min)", file=sys.stderr, flush=True)
                    next_log = ((processed // PROGRESS_EVERY) + 1) * PROGRESS_EVERY
        if chunk:
            flush(chunk)
    finally:
        out.close()

    elapsed = time.time() - start
    print(f"Wrote {written:,} → {args.output}  ({elapsed/60:.1f} min)", file=sys.stderr)


if __name__ == "__main__":
    main()
