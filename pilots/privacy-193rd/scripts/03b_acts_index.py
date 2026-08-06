#!/usr/bin/env python3
"""Goal 1, step 3a: enumerate the enacted universe from the OFFICIAL session-law
year indexes, not from /api/SessionLaws/{year}.

Seventh-pass review finding 1: the API feed is incomplete. For 2024 it returns
374 Acts chapters while the official index lists 1-407 with no gaps; the 33
missing chapters include Chapter 399, which is in-domain and had been found
only through H4940's bill history. Treating the feed as the universe made the
memo's "all 464 session laws were scanned" claim false and left the
enacted-origin recall guarantee unsupported.

This script fetches and caches the official index for every (series, year),
enumerates every chapter it lists, obtains each chapter's official text (from
the API where the feed has it, from the official chapter page otherwise), and
scans it with the same widened TEXT_TERMS used on the filed side.

Outputs:
  data/acts_index_sources.csv - one row per official index page, with the
      chapter count it lists (or its absence, for 2023 Resolves)
  data/acts_index.csv - one row per officially indexed chapter: where its text
      came from, how many characters were obtained, and which domain terms hit

09_checks.py asserts that these rows are exactly the official index and that
every chapter was obtained, so no chapter can be silently unscanned again.
"""

import csvutil
import importlib
import re
from pathlib import Path

import sessionlaws

textscan = importlib.import_module("02_textscan")

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"

FIELDS = [
    "year", "series", "chapter", "key", "title", "origin_bill", "source",
    "text_chars", "obtained", "unobtainable_reason", "text_terms", "snippet",
    "url",
]


def main() -> None:
    with (DATA / "acts_index_sources.csv").open("w", newline="") as f:
        w = csvutil.writer(f)
        w.writerow(["year", "series", "index_present", "chapters_listed", "url"])
        for s in sessionlaws.index_status():
            w.writerow([s["year"], s["series"], s["present"],
                        s["chapters_listed"], s["url"]])

    rows = []
    for rec in sessionlaws.universe():
        hits, snippet = textscan.scan_terms(rec["text"])
        rows.append({
            "year": rec["year"], "series": rec["series"],
            "chapter": rec["chapter"], "key": rec["key"],
            "title": rec["title"],
            "origin_bill": rec["origin_bill"], "source": rec["source"],
            "text_chars": len(rec["text"]),
            "obtained": "yes" if rec["text"] else "no",
            "unobtainable_reason": rec["problem"],
            "text_terms": ";".join(f"{k}:{v}" for k, v in hits.items()),
            "snippet": snippet,
            "url": rec["url"],
        })
    rows.sort(key=lambda r: (r["year"], r["series"], int(r["chapter"])))
    with (DATA / "acts_index.csv").open("w", newline="") as f:
        w = csvutil.dict_writer(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    gap = [r for r in rows if r["source"] == "chapter_page"]
    hit = [r for r in rows if r["text_terms"]]
    print(f"{len(rows)} officially indexed chapters; {len(gap)} obtained from "
          f"chapter pages because the API feed omits them; "
          f"{len(hit)} match at least one domain term")
    gap_hits = sorted((r["year"], r["chapter"]) for r in gap if r["text_terms"])
    print(f"term hits among API-omitted chapters: {gap_hits}")


if __name__ == "__main__":
    main()
