#!/usr/bin/env python3
"""Full-corpus census screen: scan the best available official text of EVERY
numbered bill against the domain term set.

Stable inputs only (fourth-pass review finding 4): the document list, the
cached texts (API or recovered PDF), and the term set. This script does NOT
read the generated census; 04_inclusion.py builds the census from this
scan plus the versioned verdict tables.

Outputs:
  data/corpus_scan.csv      every bill with at least one domain-term hit
  data/unscanned_bills.csv  is produced by 02c (bills with no recoverable
                            text); this script re-verifies and appends any
                            bill whose text is still unavailable
"""

import csv

import csvutil
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
    titles = {d["BillNumber"]: re.sub(r"\s+", " ", (d.get("Title") or "")).strip() for d in docs if d.get("BillNumber")}
    rows = []
    unscanned = []
    for i, bn in enumerate(sorted(titles), 1):
        text = textsim.full_text(bn)
        if text is None:
            unscanned.append(bn)
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
        rows.append({
            "bill": bn,
            "title": titles[bn][:110],
            "text_terms": ";".join(f"{k}:{v}" for k, v in sorted(hits.items())),
            "snippet": snippet[:280],
            "url": f"https://malegislature.gov/Bills/193/{bn}",
        })
        if i % 2000 == 0:
            print(f"  {i} scanned, {len(rows)} hits so far")

    with (DATA / "corpus_scan.csv").open("w", newline="") as f:
        w = csvutil.dict_writer(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with (DATA / "unscanned_bills.csv").open("w", newline="") as f:
        w = csvutil.writer(f)
        w.writerow(["bill", "reason"])
        for bn in unscanned:
            w.writerow([bn, "no API text and no recoverable PDF text"])
    print(f"{len(rows)} bills with domain-term hits; {len(unscanned)} unscanned "
          f"(recorded in data/unscanned_bills.csv)")


if __name__ == "__main__":
    main()
