#!/usr/bin/env python3
"""
Assign OpenAlex Topics with the *official* OpenAlex classifier.

This is not our own method — it runs OpenAlex's own published model,
``OpenAlex/bert-base-multilingual-cased-finetuned-openalex-topic-classification-title-abstract``
(mBERT fine-tuned on CWTS labels, 4,521 classes, Apache-2.0), so that v1–v5
can be compared against the production baseline on identical input.

Two preprocessing modes
-----------------------
``--preprocess openalex``  Faithful port of OpenAlex's production preprocessing
    (``v1/003_Deployment/model_to_api/container/topic_classifier/predictor.py``).
    Note what it does: ``check_for_non_latin_characters`` rejects any text whose
    script groups include HIRAGANA / KATAKANA / CJK unless the text also holds
    more than 20 Latin characters, and ``remove_non_latin_characters`` strips
    those code points from whatever survives. For a Japanese-language paper the
    title and abstract are therefore reduced to the empty string before the
    model ever sees them — which is what production does to IRDB records.

``--preprocess keep-ja``  Identical in every other respect, but the Japanese
    text is passed through to the multilingual model untouched.

Running both modes over the same 1,000 works isolates the cost of the
Japanese-stripping step from every other difference.

Usage
-----
    python scripts/assign_topics_official.py \
        --input  data/works-1k.jsonl \
        --output data/topics-1k-official-openalex.jsonl \
        --map    data/cluster_to_topic.json \
        --preprocess openalex --top-n 3

    python scripts/assign_topics_official.py \
        --input  data/works-1k.jsonl \
        --output data/topics-1k-official-keepja.jsonl \
        --map    data/cluster_to_topic.json \
        --preprocess keep-ja --top-n 3
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = (
    "OpenAlex/bert-base-multilingual-cased-finetuned-openalex-topic-classification-title-abstract"
)

# Script groups OpenAlex's predictor.py rejects, verbatim from that file.
GROUPS_TO_SKIP = [
    "HIRAGANA", "CJK", "KATAKANA", "ARABIC", "HANGUL", "THAI",
    "DEVANAGARI", "BENGALI", "THAANA", "GUJARATI", "CYRILLIC",
]

_TAG_RE = re.compile(
    r"</?(?:i|b|em|strong|sub|sup|inf|scp|sc|p|br|title|subtitle|bold|italic|"
    r"formula|roman|font|mml:math|math|mi|mtext|msub|mrow|inline-formula)\s*/?>",
    re.IGNORECASE,
)


# ── OpenAlex production preprocessing (ported from predictor.py) ─────────

def group_non_latin_characters(text: str) -> tuple[list[str], int]:
    groups: list[str] = []
    latin = 0
    text = text.replace(".", "").replace(" ", "")
    for char in text:
        try:
            script = unicodedata.name(char).split(" ")[0]
            if script == "LATIN":
                latin += 1
            elif script not in groups:
                groups.append(script)
        except ValueError:
            if "UNK" not in groups:
                groups.append("UNK")
    return groups, latin


def check_for_non_latin_characters(text: str) -> int:
    """1 = keep the text, 0 = discard it. OpenAlex's gate."""
    groups, latin = group_non_latin_characters(str(text))
    if not any(g in GROUPS_TO_SKIP for g in groups):
        return 1
    return 1 if latin > 20 else 0


def remove_non_latin_characters(text: str) -> str:
    out = []
    for char in text:
        try:
            if unicodedata.name(char).split(" ")[0] not in GROUPS_TO_SKIP:
                out.append(char)
        except ValueError:
            pass
    return "".join(out)


def clean_text(text: str, strip_non_latin: bool) -> str:
    """Strip markup; optionally apply OpenAlex's non-Latin gate and removal."""
    if not isinstance(text, str):
        return ""
    text = _TAG_RE.sub("", text)
    text = re.sub(r"<[^>]{1,80}>", "", text)
    if strip_non_latin:
        if check_for_non_latin_characters(text) == 0:
            return ""
        text = remove_non_latin_characters(text)
    return re.sub(r"\s+", " ", text).strip()


def merge_title_and_abstract(title: str, abstract: str) -> str:
    """Exact input format the model was trained on."""
    if title:
        if abstract and len(abstract) >= 30:
            return f"<TITLE> {title}\n<ABSTRACT> {abstract[:2500]}"
        return f"<TITLE> {title}"
    if abstract and len(abstract) >= 30:
        return f"<TITLE> NONE\n<ABSTRACT> {abstract[:2500]}"
    return ""


# ── main ────────────────────────────────────────────────────────────────

def pick_device(arg: str) -> torch.device:
    if arg != "auto":
        return torch.device(arg)
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--map", default="data/cluster_to_topic.json")
    ap.add_argument("--preprocess", choices=["openalex", "keep-ja"], default="openalex")
    ap.add_argument("--top-n", type=int, default=3)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--device", default="auto")
    ap.add_argument(
        "--strip-boilerplate",
        action="store_true",
        help="drop repository-boilerplate / garbled abstracts via src.text_cleaner "
             "(off by default so the two --preprocess modes differ in one thing only)",
    )
    args = ap.parse_args()

    strip_non_latin = args.preprocess == "openalex"

    clean_abstract_extra = None
    if args.strip_boilerplate:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from src.text_cleaner import clean_abstract as clean_abstract_extra  # noqa

    cluster_map: dict[str, dict] = json.load(open(args.map, encoding="utf-8"))

    device = pick_device(args.device)
    print(f"model      : {MODEL_NAME}")
    print(f"device     : {device}")
    print(f"preprocess : {args.preprocess} "
          f"({'OpenAlex non-Latin gate ON' if strip_non_latin else 'Japanese text kept'})")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(device).eval()
    id2label = model.config.id2label

    records = []
    with open(args.input, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    if args.limit:
        records = records[: args.limit]
    print(f"works      : {len(records)}\n")

    n_empty = 0
    t0 = time.time()
    out = open(args.output, "w", encoding="utf-8")

    for start in range(0, len(records), args.batch_size):
        batch = records[start : start + args.batch_size]
        texts = []
        for rec in batch:
            abstract = rec.get("abstract") or ""
            if clean_abstract_extra is not None:
                abstract = clean_abstract_extra(abstract)
            title = clean_text(rec.get("title") or "", strip_non_latin)
            abstract = clean_text(abstract, strip_non_latin)
            merged = merge_title_and_abstract(title, abstract)
            if not merged:
                n_empty += 1
            texts.append(merged)

        enc = tokenizer(
            texts, max_length=512, truncation=True, padding="max_length", return_tensors="pt"
        ).to(device)
        with torch.no_grad():
            probs = torch.softmax(model(**enc).logits, dim=-1)

        k = min(args.top_n + 10, probs.shape[-1])
        top_p, top_i = torch.topk(probs, k, dim=-1)

        for row, rec, text in zip(range(len(batch)), batch, texts):
            topics = []
            for p, i in zip(top_p[row].tolist(), top_i[row].tolist()):
                cluster_id = id2label[i].split(":", 1)[0].strip()
                m = cluster_map.get(cluster_id)
                if not m:            # one of the 10 retired clusters
                    continue
                topics.append({
                    "id": m["topic_id"],
                    "display_name": m["display_name"],
                    "score": round(p, 4),
                    "subfield": m["subfield"],
                    "field": m["field"],
                    "domain": m["domain"],
                })
                if len(topics) == args.top_n:
                    break
            out.write(json.dumps({
                "work_id": rec.get("id") or rec.get("work_id"),
                "model_input": text,
                "input_empty": not text,
                "primary_topic": topics[0] if topics else None,
                "topics": topics,
                "method": f"official-mbert-{args.preprocess}",
            }, ensure_ascii=False) + "\n")

        done = start + len(batch)
        if done % (args.batch_size * 10) == 0 or done == len(records):
            rate = done / max(time.time() - t0, 1e-9)
            print(f"  {done}/{len(records)}  ({rate:.1f} works/s)", flush=True)

    out.close()
    print(f"\nwrote {args.output}")
    print(f"empty model input: {n_empty}/{len(records)} "
          f"({n_empty / max(len(records), 1) * 100:.1f}%)")
    print(f"elapsed: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
