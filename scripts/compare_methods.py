#!/usr/bin/env python3
"""
Quantitative comparison of v1 / v2 / v3 topic assignments against gold labels.

Metrics
-------
  Primary topic accuracy : gold_topic_id == primary_topic.id
  Top-3 hit rate         : gold_topic_id appears anywhere in topics[]
  Avg confidence score   : mean of primary_topic.score

Usage
-----
    python scripts/compare_methods.py \\
        --gold   data/gold-labels-100.jsonl \\
        --v1     /path/to/irdb-topic-matcher/data/topics-1k-multi.jsonl \\
        --v2     data/topics-1k-ensemble.jsonl \\
        --v3     data/topics-1k-v3.jsonl \\
        --out-md docs/comparison-v1-v2-v3.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# ────────────────────────────────────────────────────────────────────────
# Loaders
# ────────────────────────────────────────────────────────────────────────

def load_jsonl(path: str | Path) -> dict[str, dict]:
    """Return dict keyed by work_id."""
    out: dict[str, dict] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            wid = row.get("work_id") or row.get("id") or ""
            if wid:
                out[wid] = row
    return out


def load_gold(path: str | Path) -> dict[str, dict]:
    return load_jsonl(path)


# ────────────────────────────────────────────────────────────────────────
# Metrics
# ────────────────────────────────────────────────────────────────────────

def _primary_id(row: dict) -> str:
    pt = row.get("primary_topic") or {}
    return pt.get("id", "")


def _primary_score(row: dict) -> float:
    pt = row.get("primary_topic") or {}
    return float(pt.get("score", 0.0))


def _top3_ids(row: dict) -> list[str]:
    return [t.get("id", "") for t in (row.get("topics") or [])]


def evaluate(
    gold: dict[str, dict],
    preds: dict[str, dict],
    label: str,
) -> dict:
    common = set(gold) & set(preds)
    if not common:
        return {"label": label, "n": 0, "primary_acc": 0.0, "top3_hit": 0.0, "avg_score": 0.0}

    primary_correct = 0
    top3_hit        = 0
    score_sum       = 0.0
    details         = []

    for wid in sorted(common):
        g = gold[wid]
        p = preds[wid]
        gold_id = g.get("gold_topic_id", "")
        pred_id = _primary_id(p)
        in_top3 = gold_id in _top3_ids(p)
        score   = _primary_score(p)

        if pred_id == gold_id:
            primary_correct += 1
        if in_top3:
            top3_hit += 1
        score_sum += score

        details.append({
            "work_id":       wid,
            "title":         g.get("title", ""),
            "gold_topic":    g.get("gold_topic_name", ""),
            "pred_topic":    (p.get("primary_topic") or {}).get("display_name", ""),
            "primary_match": pred_id == gold_id,
            "top3_hit":      in_top3,
            "score":         round(score, 4),
        })

    n = len(common)
    return {
        "label":       label,
        "n":           n,
        "primary_acc": round(primary_correct / n * 100, 1),
        "top3_hit":    round(top3_hit        / n * 100, 1),
        "avg_score":   round(score_sum       / n, 4),
        "details":     details,
    }


# ────────────────────────────────────────────────────────────────────────
# Report builder
# ────────────────────────────────────────────────────────────────────────

def build_report(results: list[dict], gold: dict[str, dict]) -> str:
    lines = [
        "# v1 / v2 / v3 手法比較レポート（正解ラベル対照）",
        "",
        f"**正解ラベル件数:** {len(gold)} 件  ",
        "",
        "---",
        "",
        "## 1. サマリ",
        "",
        "| 手法 | 対照件数 | Primary一致率 | Top-3 Hit率 | 平均スコア |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(
            f"| {r['label']} | {r['n']} 件 "
            f"| **{r['primary_acc']}%** "
            f"| {r['top3_hit']}% "
            f"| {r['avg_score']} |"
        )

    lines += ["", "---", "", "## 2. 詳細結果（全件）", ""]

    for r in results:
        lines += [
            f"### {r['label']}",
            "",
            "| # | タイトル（抜粋） | 正解 Topic | 本手法 Topic | Primary一致 | Top-3 |",
            "|---|---|---|---|---|---|",
        ]
        for i, d in enumerate(r.get("details", []), 1):
            ok_mark = "✅" if d["primary_match"] else "❌"
            t3_mark = "✅" if d["top3_hit"]      else "❌"
            title   = d["title"][:35].replace("|", "｜")
            gold_t  = d["gold_topic"][:30].replace("|", "｜")
            pred_t  = d["pred_topic"][:30].replace("|", "｜")
            lines.append(
                f"| {i} | {title} | {gold_t} | {pred_t} | {ok_mark} | {t3_mark} |"
            )
        lines.append("")

    lines += [
        "---",
        "",
        "## 3. 考察",
        "",
        "- **Primary一致率**: 正解 Topic と primary_topic が完全一致した割合",
        "- **Top-3 Hit率**: 正解 Topic が topics[] の上位 3 件に含まれた割合",
        "- 正解ラベルは Claude が候補 20 件の中から選択したもの（上位候補外の正解は含まない）",
        "",
        "*本レポートは `scripts/compare_methods.py` により自動生成されました。*",
    ]
    return "\n".join(lines)


# ────────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Compare v1/v2/v3/v4 against gold labels")
    ap.add_argument("--gold",   required=True, help="Gold labels JSONL")
    ap.add_argument("--v1",     default=None,  help="v1 output JSONL")
    ap.add_argument("--v2",     default=None,  help="v2 output JSONL")
    ap.add_argument("--v3",     default=None,  help="v3 output JSONL")
    ap.add_argument("--extra",  action="append", default=[],
                    metavar="LABEL:PATH",
                    help="Additional method as 'label:path' (repeatable)")
    ap.add_argument("--out-md", default=None,  help="Output markdown report path")
    args = ap.parse_args()

    gold = load_gold(args.gold)
    print(f"Gold labels loaded: {len(gold)} works", file=sys.stderr)

    results = []
    specs = [
        ("v1（embedding）",    args.v1),
        ("v2（ensemble）",     args.v2),
        ("v3（翻訳+階層+BM25）", args.v3),
    ]
    for lbl, sep, path in (s.partition(":") for s in args.extra):
        specs.append((lbl, path if sep else None))

    for label, path in specs:
        if not path:
            continue
        preds = load_jsonl(path)
        r = evaluate(gold, preds, label)
        results.append(r)
        print(
            f"{label}: n={r['n']}  primary={r['primary_acc']}%  "
            f"top3={r['top3_hit']}%  avg_score={r['avg_score']}",
            file=sys.stderr,
        )

    if not results:
        print("No prediction files provided.", file=sys.stderr)
        sys.exit(1)

    report = build_report(results, gold)

    if args.out_md:
        Path(args.out_md).write_text(report, encoding="utf-8")
        print(f"Report written → {args.out_md}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
