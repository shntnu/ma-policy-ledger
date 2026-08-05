#!/usr/bin/env python3
"""Full-corpus census screen (third-pass review finding 3): scan the cached
full text of EVERY numbered bill in the 193rd General Court with the widened
domain term set, so the census is a complete full-text screen rather than a
title/committee-gated sample.

Outputs:
  data/corpus_scan.csv   every bill with at least one domain-term hit:
                         terms, counts, snippet, current census status
  data/corpus_triage.csv the subset with no census decision yet - the
                         adjudication worklist
"""

import csv
import importlib
import json
import re
from pathlib import Path

import textsim

textscan = importlib.import_module("02_textscan")

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"


def main() -> None:
    docs = json.loads((DATA / "documents_193.json").read_text())
    census = {r["bill_number"]: r for r in csv.DictReader((DATA / "census.csv").open())}
    titles = {d["BillNumber"]: (d.get("Title") or "").strip() for d in docs if d.get("BillNumber")}
    rows = []
    missing = []
    for i, bn in enumerate(sorted(titles), 1):
        try:
            text = textsim.bill_text(bn)
        except FileNotFoundError:
            missing.append(bn)
            continue
        hits = {}
        snippet = ""
        for k, rx in textscan.TEXT_TERMS.items():
            found = list(re.finditer(rx, text))
            if found:
                hits[k] = len(found)
                if not snippet:
                    m = found[0]
                    snippet = text[max(0, m.start() - 100): m.end() + 150].strip()
        if not hits:
            continue
        c = census.get(bn)
        rows.append({
            "bill": bn,
            "title": titles[bn][:110],
            "text_terms": ";".join(f"{k}:{v}" for k, v in sorted(hits.items())),
            "snippet": snippet[:280],
            "census_decision": c["decision"] if c else "",
            "census_reason": c["reason"] if c else "",
            "url": f"https://malegislature.gov/Bills/193/{bn}",
        })
        if i % 1000 == 0:
            print(f"  {i} scanned, {len(rows)} hits so far")

    with (DATA / "corpus_scan.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    triage = [r for r in rows if not r["census_decision"]]
    with (DATA / "corpus_triage.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(triage)
    print(f"{len(rows)} bills with domain-term hits; {len(triage)} need triage; "
          f"{len(missing)} texts missing from cache")


if __name__ == "__main__":
    main()
