#!/usr/bin/env python3
"""
Fetch what OpenAlex currently holds for a set of works: its assigned Topics
plus the two production features that IRDB records tend to lack
(``referenced_works_count`` and ``primary_location.source``).

The second part matters as much as the first: OpenAlex's classifier takes
title, abstract, source name and citations. If a record has no references and
its source is the generic "Institutional Repositories DataBase (IRDB)", two of
those four inputs carry no signal — and the production preprocessing discards
Japanese title/abstract text, leaving effectively none.

Usage
-----
    python scripts/fetch_openalex_current.py \
        --input  data/works-1k.jsonl \
        --output data/openalex-current-1k.jsonl \
        --mailto you@example.org
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request

API = "https://api.openalex.org/works"
SELECT = ",".join([
    "id", "title", "language", "type",
    "topics", "primary_topic",
    "referenced_works_count", "cited_by_count",
    "primary_location", "abstract_inverted_index",
])


def fetch(ids: list[str], mailto: str, retries: int = 4) -> list[dict]:
    params = {
        "filter": "openalex_id:" + "|".join(ids),
        "select": SELECT,
        "per-page": str(len(ids)),
        "mailto": mailto,
    }
    url = f"{API}?{urllib.parse.urlencode(params)}"
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as f:
                return json.load(f)["results"]
        except Exception as exc:                                  # noqa: BLE001
            if attempt == retries - 1:
                print(f"  ! giving up on a batch: {exc}")
                return []
            time.sleep(2 ** attempt)
    return []


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--mailto", required=True)
    ap.add_argument("--batch-size", type=int, default=50)
    args = ap.parse_args()

    ids = []
    with open(args.input, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                wid = json.loads(line).get("id") or ""
                if wid:
                    ids.append(wid.rsplit("/", 1)[-1])
    print(f"works: {len(ids)}")

    n = 0
    with open(args.output, "w", encoding="utf-8") as out:
        for start in range(0, len(ids), args.batch_size):
            batch = ids[start : start + args.batch_size]
            for row in fetch(batch, args.mailto):
                # keep the payload small: drop the inverted index, keep its length
                ab = row.pop("abstract_inverted_index", None) or {}
                row["abstract_word_count"] = sum(len(v) for v in ab.values())
                loc = row.pop("primary_location", None) or {}
                src = loc.get("source") or {}
                row["source_id"] = src.get("id")
                row["source_name"] = src.get("display_name")
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                n += 1
            print(f"  {min(start + args.batch_size, len(ids))}/{len(ids)}", flush=True)
            time.sleep(0.12)

    print(f"wrote {n} records -> {args.output}")


if __name__ == "__main__":
    main()
