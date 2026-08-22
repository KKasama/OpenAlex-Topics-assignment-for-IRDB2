#!/usr/bin/env python3
"""
Comprehensive comparison of all topic assignment methods against gold labels.

Adds hierarchy-level accuracy (Subfield / Field / Domain) and the two official
model runs (openalex / keep-ja preprocessing).

Usage
-----
    python scripts/compare_all_methods.py \
        --gold data/gold-labels-100.jsonl \
        --meta index-e5-large/topics_meta.json \
        --oa-current data/openalex-current-1k.jsonl \
        --methods \
            "OpenAlex current"=data/openalex-current-1k.jsonl \
            "Official mBERT (openalex)"=data/topics-1k-official-openalex.jsonl \
            "Official mBERT (keep-ja)"=data/topics-1k-official-keepja.jsonl \
            "v1 embedding"=../irdb-topic-matcher/data/topics-1k-multi.jsonl \
            "v2 ensemble"=data/topics-1k-ensemble.jsonl \
            "v5 e5-large"=data/topics-1k-v5-e5-large.jsonl \
        --out-md docs/comparison-all-methods.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# ── helpers ──────────────────────────────────────────────────────────────

def load_jsonl(path: str) -> dict[str, dict]:
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            wid = row.get("work_id") or row.get("id") or ""
            if wid:
                out[wid] = row
    return out


def build_topic_hierarchy(meta_path: str) -> dict[str, dict]:
    """topic_id -> {display_name, subfield, field, domain}"""
    records = json.load(open(meta_path, encoding="utf-8"))
    out = {}
    for r in records:
        tid = r["id"]
        out[tid] = dict(
            display_name=r["display_name"],
            subfield=r.get("subfield", {}).get("display_name", ""),
            field=r.get("field", {}).get("display_name", ""),
            domain=r.get("domain", {}).get("display_name", ""),
        )
    return out


def get_primary(row: dict) -> dict | None:
    """Extract the primary topic from any of our output formats or OpenAlex API format."""
    pt = row.get("primary_topic")
    if pt:
        return pt
    topics = row.get("topics")
    if topics and isinstance(topics, list) and len(topics) > 0:
        return topics[0]
    return None


def get_primary_id(row: dict) -> str:
    pt = get_primary(row)
    return (pt.get("id") or "") if pt else ""


def get_top3_ids(row: dict) -> list[str]:
    topics = row.get("topics") or []
    return [t.get("id", "") for t in topics[:3]]


def get_hierarchy(row: dict, meta: dict[str, dict]) -> dict[str, str]:
    """Return {subfield, field, domain} for a row, from the row itself or from meta."""
    pt = get_primary(row)
    if not pt:
        return {"subfield": "", "field": "", "domain": ""}
    tid = pt.get("id", "")
    # Some outputs embed subfield/field/domain directly
    sf = pt.get("subfield", {})
    if isinstance(sf, dict):
        sf = sf.get("display_name", "")
    fi = pt.get("field", {})
    if isinstance(fi, dict):
        fi = fi.get("display_name", "")
    do = pt.get("domain", {})
    if isinstance(do, dict):
        do = do.get("display_name", "")
    # fill in from meta if missing
    m = meta.get(tid, {})
    return {
        "subfield": sf or m.get("subfield", ""),
        "field": fi or m.get("field", ""),
        "domain": do or m.get("domain", ""),
    }


def evaluate(
    gold: dict[str, dict],
    preds: dict[str, dict],
    meta: dict[str, dict],
    label: str,
) -> dict:
    common = sorted(set(gold) & set(preds))
    n = len(common)
    if n == 0:
        return {"label": label, "n": 0}
    primary_match = 0
    top3_hit = 0
    subfield_match = 0
    field_match = 0
    domain_match = 0
    scores = []
    details = []

    for wid in common:
        g, p = gold[wid], preds[wid]
        gold_id = g["gold_topic_id"]
        pred_id = get_primary_id(p)
        p_match = pred_id == gold_id
        in_top3 = gold_id in get_top3_ids(p)

        # hierarchy: compare via the gold topic's hierarchy
        gold_hier = meta.get(gold_id, {})
        pred_hier = get_hierarchy(p, meta)
        sf = gold_hier.get("subfield", "") and gold_hier["subfield"] == pred_hier["subfield"]
        fi = gold_hier.get("field", "") and gold_hier["field"] == pred_hier["field"]
        do = gold_hier.get("domain", "") and gold_hier["domain"] == pred_hier["domain"]

        if p_match:
            primary_match += 1
        if in_top3:
            top3_hit += 1
        if sf:
            subfield_match += 1
        if fi:
            field_match += 1
        if do:
            domain_match += 1

        pt = get_primary(p) or {}
        scores.append(float(pt.get("score", 0.0)))
        details.append({
            "wid": wid,
            "title": g.get("title", "")[:80],
            "gold_topic": g.get("gold_topic_name", ""),
            "pred_topic": (get_primary(p) or {}).get("display_name", ""),
            "primary_match": p_match,
            "top3_hit": in_top3,
            "subfield_match": sf,
            "field_match": fi,
            "domain_match": do,
        })

    return {
        "label": label,
        "n": n,
        "primary_acc": round(primary_match / n * 100, 1),
        "top3_hit": round(top3_hit / n * 100, 1),
        "subfield_acc": round(subfield_match / n * 100, 1),
        "field_acc": round(field_match / n * 100, 1),
        "domain_acc": round(domain_match / n * 100, 1),
        "avg_score": round(sum(scores) / n, 4) if scores else 0,
        "details": details,
    }


# ── report ───────────────────────────────────────────────────────────────

def generate_report(results: list[dict]) -> str:
    lines = [
        "# 全手法比較レポート（正解ラベル対照・階層別）",
        "",
        f"**正解ラベル件数:** {results[0]['n']} 件  ",
        "",
        "---",
        "",
        "## 1. サマリ",
        "",
        "| 手法 | n | Primary一致 | Top-3 Hit | Subfield一致 | Field一致 | Domain一致 | Avg Score |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(
            f"| {r['label']} | {r['n']} | "
            f"**{r['primary_acc']}%** | {r['top3_hit']}% | "
            f"{r['subfield_acc']}% | {r['field_acc']}% | {r['domain_acc']}% | "
            f"{r['avg_score']} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. 詳細（Primary Topic 比較 — 先頭 30 件）")
    lines.append("")
    lines.append("| # | 正解 Topic | 手法 | 付与 Topic | P | T3 | SF | F | D |")
    lines.append("|---|---|---|---|---|---|---|---|---|")

    details_by_wid = {}
    for r in results:
        for d in r.get("details", []):
            details_by_wid.setdefault(d["wid"], {})["gold"] = d["gold_topic"]
            details_by_wid.setdefault(d["wid"], {})[r["label"]] = d

    i = 0
    for wid in sorted(details_by_wid)[:30]:
        i += 1
        group = details_by_wid[wid]
        gold = group.get("gold", "")[:35]
        for r in results:
            d = group.get(r["label"])
            if not d:
                continue
            ok = lambda v: "✅" if v else "❌"
            pred = d["pred_topic"][:35]
            lines.append(
                f"| {i} | {gold} | {r['label'][:20]} | {pred} | "
                f"{ok(d['primary_match'])} | {ok(d['top3_hit'])} | "
                f"{ok(d['subfield_match'])} | {ok(d['field_match'])} | "
                f"{ok(d['domain_match'])} |"
            )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*作成：笠間和喜（iGroup Japan）/ {__import__('datetime').date.today().isoformat()}*")
    return "\n".join(lines)


# ── main ─────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--methods", nargs="+", required=True, metavar="LABEL=PATH")
    ap.add_argument("--out-md", required=True)
    args = ap.parse_args()

    gold = load_jsonl(args.gold)
    meta = build_topic_hierarchy(args.meta)
    print(f"gold labels : {len(gold)}")

    results = []
    for spec in args.methods:
        label, path = spec.split("=", 1)
        preds = load_jsonl(path)
        r = evaluate(gold, preds, meta, label)
        print(f"{r['label']:<30} n={r['n']:>3}  "
              f"primary={r.get('primary_acc','-'):>5}%  top3={r.get('top3_hit','-'):>5}%  "
              f"field={r.get('field_acc','-'):>5}%  domain={r.get('domain_acc','-'):>5}%")
        results.append(r)

    report = generate_report(results)
    with open(args.out_md, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nwrote {args.out_md}")


if __name__ == "__main__":
    main()
