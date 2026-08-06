#!/usr/bin/env python3
"""Goal 1, step 3: scan every session law enacted in 2023 and 2024 (the 193rd
General Court) for consumer-data-privacy content, including budget outside
sections.

The universe comes from sessionlaws.py - the OFFICIAL year indexes, not
/api/SessionLaws/{year}, which omits 33 of the 407 Acts chapters the 2024
index lists (seventh-pass review finding 1). 03b_acts_index.py runs first and
caches the index pages and the API-omitted chapter pages.

Output: data/sessionlaw_scan.csv - one row per enacted chapter that matches
any text term, with hit counts and a snippet. The chapter key follows
sessionlaws.adj_key: Acts keep the bare number, Resolves are prefixed "R".
"""

import csvutil
import importlib
import re
from pathlib import Path

import sessionlaws

textscan = importlib.import_module("02_textscan")

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"


def main() -> None:
    laws = sessionlaws.universe()
    rows = []
    for law in laws:
        plain = law["text"]
        low = plain.lower()
        hits = {}
        snippet = ""
        for k, rx in textscan.TEXT_TERMS.items():
            found = list(re.finditer(rx, low))
            if found:
                hits[k] = len(found)
                if not snippet:
                    m = found[0]
                    snippet = plain[max(0, m.start() - 120): m.end() + 120].strip()
        if not hits:
            continue
        rows.append({
            "year": law["year"],
            "chapter": law["key"],
            "type": law["series"],
            "text_source": law["source"],
            "title": law["title"],
            "text_chars": len(plain),
            "text_terms": ";".join(f"{k}:{v}" for k, v in hits.items()),
            "snippet": snippet,
            "url": law["url"],
        })
    rows.sort(key=lambda r: (r["year"], r["type"], int(r["chapter"].lstrip("R"))))
    with (DATA / "sessionlaw_scan.csv").open("w", newline="") as f:
        w = csvutil.dict_writer(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    from_pages = sum(1 for law in laws if law["source"] == "chapter_page")
    print(f"{len(laws)} officially indexed session laws scanned "
          f"({from_pages} obtained from chapter pages the API feed omits), "
          f"{len(rows)} match at least one term")


if __name__ == "__main__":
    main()
