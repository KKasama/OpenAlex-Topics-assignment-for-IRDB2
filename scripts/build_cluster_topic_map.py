#!/usr/bin/env python3
"""
Build the CWTS micro-cluster -> OpenAlex Topic mapping table.

Why this is needed
------------------
The official OpenAlex classifier
(``OpenAlex/bert-base-multilingual-cased-finetuned-openalex-topic-classification-title-abstract``)
emits labels of the form ``"{cwts_micro_cluster_id}: {cwts_long_label}"``.
OpenAlex Works, however, carry Topic ids (``T10001`` …) whose ``display_name``
is the CWTS *short* label — a different string. To compare the official
model's output against v1–v5 output we need cluster_id -> T-id.

There is no published crosswalk, so we join two public sources on the
``summary`` / ``keywords`` / ``wikipedia_url`` fields, which both carry
verbatim:

  1. CWTS ``micro_cluster.tsv`` (cluster_id, short_label, long_label, keywords,
     summary, wikipedia_url) — inside the 1 GB zip at Zenodo 10560276 (CC0).
     Only that one 900 KB member is fetched, via HTTP range requests.
  2. OpenAlex's published topic sheet (topic_id, topic_name, subfield, field,
     domain, keywords, summary, wikipedia_url), linked from
     github.com/ourresearch/openalex-topic-classification.

Coverage is 4,511 / 4,521 clusters. The 10 misses are clusters that were
dropped when OpenAlex consolidated 4,521 clusters into 4,516 Topics.

Usage
-----
    python scripts/build_cluster_topic_map.py --out data/cluster_to_topic.json
"""

from __future__ import annotations

import argparse
import collections
import csv
import io
import json
import re
import struct
import urllib.request
import zlib

ZENODO_ZIP = "https://zenodo.org/records/10560276/files/classification_openalex_2023nov.zip"
TOPIC_SHEET = (
    "https://docs.google.com/spreadsheets/d/"
    "1v-MAq64x4YjhO7RWcB-yrKV5D_2vOOsxl4u6GBKEXY8/export?format=csv"
)
MEMBER = "micro_cluster.tsv"


# ── minimal remote-zip reader (range requests) ──────────────────────────

class RemoteZip:
    def __init__(self, url: str):
        self.url = url
        self.size = self._size()

    def _get(self, start: int, length: int) -> bytes:
        req = urllib.request.Request(
            self.url, headers={"Range": f"bytes={start}-{start + length - 1}"}
        )
        with urllib.request.urlopen(req) as f:
            return f.read()

    def _size(self) -> int:
        req = urllib.request.Request(self.url, headers={"Range": "bytes=0-0"})
        with urllib.request.urlopen(req) as f:
            cr = f.headers.get("Content-Range")
            return int(cr.split("/")[-1]) if cr else int(f.headers["Content-Length"])

    def entries(self) -> list[dict]:
        tail = self._get(max(0, self.size - 66000), min(66000, self.size))
        i = tail.rfind(b"PK\x05\x06")
        if i < 0:
            raise RuntimeError("no end-of-central-directory record")
        cd_size, cd_off = struct.unpack("<II", tail[i + 12 : i + 20])
        if 0xFFFFFFFF in (cd_size, cd_off):
            j = tail.rfind(b"PK\x06\x06")
            cd_size, cd_off = struct.unpack("<QQ", tail[j + 40 : j + 56])
        cd = self._get(cd_off, cd_size)

        out, p = [], 0
        while p < len(cd) and cd[p : p + 4] == b"PK\x01\x02":
            method = struct.unpack("<H", cd[p + 10 : p + 12])[0]
            csize = struct.unpack("<I", cd[p + 20 : p + 24])[0]
            usize = struct.unpack("<I", cd[p + 24 : p + 28])[0]
            nlen, elen, clen = struct.unpack("<HHH", cd[p + 28 : p + 34])
            lho = struct.unpack("<I", cd[p + 42 : p + 46])[0]
            name = cd[p + 46 : p + 46 + nlen].decode("utf-8", "replace")
            extra = cd[p + 46 + nlen : p + 46 + nlen + elen]

            q = 0  # walk the zip64 extra field
            while q + 4 <= len(extra):
                hid, hsz = struct.unpack("<HH", extra[q : q + 4])
                if hid == 0x0001:
                    body, k = extra[q + 4 : q + 4 + hsz], 0
                    if usize == 0xFFFFFFFF:
                        usize = struct.unpack("<Q", body[k : k + 8])[0]; k += 8
                    if csize == 0xFFFFFFFF:
                        csize = struct.unpack("<Q", body[k : k + 8])[0]; k += 8
                    if lho == 0xFFFFFFFF:
                        lho = struct.unpack("<Q", body[k : k + 8])[0]
                q += 4 + hsz

            out.append(dict(name=name, method=method, csize=csize, usize=usize, lho=lho))
            p += 46 + nlen + elen + clen
        return out

    def read(self, e: dict) -> bytes:
        hdr = self._get(e["lho"], 30)
        nlen, elen = struct.unpack("<HH", hdr[26:30])
        data = self._get(e["lho"] + 30 + nlen + elen, e["csize"])
        return data if e["method"] == 0 else zlib.decompress(data, -15)


# ── join ────────────────────────────────────────────────────────────────

def _norm(s: str | None) -> str:
    return re.sub(r"\s+", " ", s or "").strip().lower()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/cluster_to_topic.json")
    args = ap.parse_args()

    print(f"[1/3] fetching {MEMBER} from Zenodo (range requests) …")
    rz = RemoteZip(ZENODO_ZIP)
    entry = next(e for e in rz.entries() if e["name"] == MEMBER)
    raw = rz.read(entry).decode("utf-8", "replace")
    clusters = list(csv.DictReader(io.StringIO(raw), delimiter="\t"))
    print(f"      {len(clusters)} CWTS micro clusters")

    print("[2/3] fetching OpenAlex topic sheet …")
    with urllib.request.urlopen(TOPIC_SHEET) as f:
        sheet_raw = f.read().decode("utf-8", "replace")
    topics = list(csv.DictReader(io.StringIO(sheet_raw)))
    print(f"      {len(topics)} OpenAlex Topics")

    print("[3/3] joining on summary -> keywords -> wikipedia_url …")
    indexes = {}
    for key in ("summary", "keywords", "wikipedia_url"):
        buckets = collections.defaultdict(list)
        for row in topics:
            buckets[_norm(row[key])].append(row)
        indexes[key] = {k: v[0] for k, v in buckets.items() if len(v) == 1 and k}

    mapping: dict[str, dict] = {}
    how: collections.Counter = collections.Counter()
    for c in clusters:
        for key in ("summary", "keywords", "wikipedia_url"):
            t = indexes[key].get(_norm(c[key]))
            if t:
                mapping[c["micro_cluster_id"]] = {
                    "topic_id": "https://openalex.org/T" + t["topic_id"],
                    "display_name": t["topic_name"],
                    "subfield": t["subfield_name"],
                    "field": t["field_name"],
                    "domain": t["domain_name"],
                    "cwts_short_label": c["short_label"],
                    "cwts_long_label": c["long_label"],
                }
                how[key] += 1
                break
        else:
            how["unmapped"] += 1

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=0)

    print(f"\nmapped {len(mapping)}/{len(clusters)} clusters -> {args.out}")
    for k, v in how.most_common():
        print(f"  via {k}: {v}")


if __name__ == "__main__":
    main()
