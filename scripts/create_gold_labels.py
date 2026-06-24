#!/usr/bin/env python3
"""
Create gold-label Topics for N Japanese papers using Claude (Anthropic API).

For each paper:
1. Retrieve top-20 candidate topics via embedding search.
2. Send paper + candidates to Claude and ask it to pick the best topic.
3. Save the gold label (work_id, title, chosen topic, reasoning).

Usage
-----
    export ANTHROPIC_API_KEY="sk-ant-..."

    python scripts/create_gold_labels.py \\
        --index-dir ./index-base \\
        --works     data/works-1k.jsonl \\
        --output    data/gold-labels-100.jsonl \\
        --n         100

    # Re-run failed items only (skips already-written work_ids)
    python scripts/create_gold_labels.py \\
        --index-dir ./index-base \\
        --works     data/works-1k.jsonl \\
        --output    data/gold-labels-100.jsonl \\
        --n         100 --resume
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.embeddings  import EmbeddingModel, ModelType
from src.topic_index import TopicIndex

_JP_RE = re.compile(r"[ぁ-ゟ゠-ヿ一-鿿]")


# ────────────────────────────────────────────────────────────────────────
# Claude prompt
# ────────────────────────────────────────────────────────────────────────

def _build_prompt(title: str, candidates: list[dict]) -> str:
    lines = [
        "You are an expert academic librarian who specialises in classifying "
        "Japanese research papers according to the OpenAlex topic taxonomy.",
        "",
        f'Paper title: "{title}"',
        "",
        "Below are the top candidate topics retrieved by a semantic search. "
        "Select the ONE topic that best describes the main research theme of this paper.",
        "Return ONLY a JSON object with these fields:",
        '  { "topic_id": "https://openalex.org/T...", "topic_name": "...", "confidence": 0.0-1.0, "reasoning": "..." }',
        "",
        "Candidate topics:",
    ]
    for i, c in enumerate(candidates, 1):
        keywords = ", ".join(c.get("keywords", [])[:6])
        lines.append(
            f'{i:2d}. [{c["id"]}] {c["display_name"]}  '
            f'(Field: {c.get("field","")}, Domain: {c.get("domain","")})'
        )
        if keywords:
            lines.append(f'      Keywords: {keywords}')
    lines += [
        "",
        "Important: if none of the candidates fits well, still choose the closest one.",
        "Respond with the JSON object only — no markdown fences, no extra text.",
    ]
    return "\n".join(lines)


# ────────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Create gold topic labels via Claude")
    ap.add_argument("--index-dir", default="./index-base")
    ap.add_argument("--works",  required=True, help="JSONL of works to label")
    ap.add_argument("--output", required=True, help="Output gold-labels JSONL")
    ap.add_argument("--n",      type=int, default=100, help="How many papers to label")
    ap.add_argument("--top-k",  type=int, default=20,  help="Candidates shown to Claude")
    ap.add_argument("--model-claude", default="claude-sonnet-4-6",
                    help="Claude model to use (default claude-sonnet-4-6)")
    ap.add_argument("--resume", action="store_true",
                    help="Skip work_ids already in output file")
    ap.add_argument("--delay",  type=float, default=0.5,
                    help="Seconds between API calls (default 0.5)")
    args = ap.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        sys.exit("Error: set ANTHROPIC_API_KEY environment variable")

    try:
        import anthropic
    except ImportError:
        sys.exit("Error: pip install anthropic")

    client = anthropic.Anthropic(api_key=api_key)

    # ── load already-done ids (resume mode) ──────────────────────────
    done_ids: set[str] = set()
    if args.resume and Path(args.output).exists():
        with open(args.output, encoding="utf-8") as f:
            for line in f:
                try:
                    done_ids.add(json.loads(line)["work_id"])
                except Exception:
                    pass
        print(f"Resume: skipping {len(done_ids)} already-labelled works.", file=sys.stderr)

    # ── load embedding model + topic index ──────────────────────────
    print("Loading topic index …", file=sys.stderr)
    d = Path(args.index_dir)
    index     = TopicIndex.load(d)
    emb_model = EmbeddingModel(ModelType.MULTILINGUAL_E5_BASE)

    # build a lookup: topic_id → full metadata (for keywords etc.)
    with open(d / "topics_meta.json", encoding="utf-8") as f:
        topics_meta = json.load(f)
    topic_lookup = {t["id"]: t for t in topics_meta}

    # ── collect papers ───────────────────────────────────────────────
    papers: list[dict] = []
    with open(args.works, encoding="utf-8") as f:
        for line in f:
            try:
                w = json.loads(line)
            except json.JSONDecodeError:
                continue
            title = w.get("title", "") or ""
            if not _JP_RE.search(title):
                continue
            wid = w.get("id") or w.get("work_id") or ""
            if wid in done_ids:
                continue
            papers.append({"work_id": wid, "title": title})
            if len(papers) >= args.n:
                break

    if not papers:
        print("No papers to label (all done or none with Japanese titles).", file=sys.stderr)
        return

    print(f"Labelling {len(papers)} papers with {args.model_claude} …", file=sys.stderr)

    out_f = open(args.output, "a", encoding="utf-8")
    success = skipped = 0

    for idx, paper in enumerate(papers, 1):
        work_id = paper["work_id"]
        title   = paper["title"]

        # ── 1. embedding search for top-k candidates ─────────────────
        query_vec = emb_model.encode([title], is_query=True)
        candidates_raw = index.query(query_vec[0], top_k=args.top_k)

        candidates = []
        for c in candidates_raw:
            meta = topic_lookup.get(c.topic_id, {})
            field_name = ""
            if isinstance(meta.get("field"), dict):
                field_name = meta["field"].get("display_name", "")
            domain_name = ""
            if isinstance(meta.get("domain"), dict):
                domain_name = meta["domain"].get("display_name", "")
            candidates.append({
                "id":           c.topic_id,
                "display_name": c.display_name,
                "field":        field_name,
                "domain":       domain_name,
                "keywords":     meta.get("keywords", []),
                "emb_score":    round(c.score, 4),
            })

        # ── 2. call Claude ────────────────────────────────────────────
        prompt = _build_prompt(title, candidates)
        try:
            response = client.messages.create(
                model=args.model_claude,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}],
            )
            raw_text = response.content[0].text.strip()

            # Parse JSON response
            # Handle cases where Claude adds minor whitespace or trailing chars
            clean = re.sub(r"^```(?:json)?|```$", "", raw_text, flags=re.MULTILINE).strip()
            result = json.loads(clean)

            label = {
                "work_id":       work_id,
                "title":         title,
                "gold_topic_id":   result.get("topic_id", ""),
                "gold_topic_name": result.get("topic_name", ""),
                "confidence":    result.get("confidence", 0.0),
                "reasoning":     result.get("reasoning", ""),
                "candidates":    candidates,
            }
            out_f.write(json.dumps(label, ensure_ascii=False) + "\n")
            out_f.flush()
            success += 1
            print(
                f"[{idx:3d}/{len(papers)}] {title[:60]:60s} → {result.get('topic_name','?')[:40]}",
                file=sys.stderr,
            )

        except Exception as e:
            print(f"[{idx:3d}/{len(papers)}] ERROR for {work_id}: {e}", file=sys.stderr)
            skipped += 1

        if args.delay > 0 and idx < len(papers):
            time.sleep(args.delay)

    out_f.close()
    print(
        f"\nDone. Labelled {success} papers, {skipped} errors → {args.output}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
