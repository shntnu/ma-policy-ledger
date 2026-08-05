#!/usr/bin/env python3
"""Goal 1, step 3: scan every session law enacted in 2023 and 2024 (the 193rd
General Court) for consumer-data-privacy content, including budget outside
sections, using the full ChapterText returned by /api/SessionLaws/{year}.

Output: data/sessionlaw_scan.csv - one row per enacted chapter that matches
any text term, with hit counts and a snippet.
"""

import csv
import importlib
import re
from pathlib import Path

import fetchlib

textscan = importlib.import_module("02_textscan")

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"
API = "https://malegislature.gov/api"


def main() -> None:
    fetchlib.seed(
        f"{API}/SessionLaws/2023", PILOT / "raw" / "probe" / "api_sessionlaws_2023.json"
    )
    rows = []
    total = 0
    for year in (2023, 2024):
        laws = fetchlib.get_json(f"{API}/SessionLaws/{year}")
        total += len(laws)
        for law in laws:
            plain = re.sub(r"<[^>]+>", " ", law.get("ChapterText") or "")
            plain = re.sub(r"\s+", " ", plain)
            low = plain.lower()
            hits = {}
            snippet = ""
            for k, rx in textscan.TEXT_TERMS.items():
                found = list(re.finditer(rx, low))
                if found:
                    hits[k] = len(found)
                    if not snippet:
                        m = found[0]
                        snippet = plain[max(0, m.start() - 120) : m.end() + 120].strip()
            if not hits:
                continue
            rows.append(
                {
                    "year": year,
                    "chapter": law["ChapterNumber"],
                    "type": law.get("Type"),
                    "title": (law.get("Title") or "").strip(),
                    "text_chars": len(plain),
                    "text_terms": ";".join(f"{k}:{v}" for k, v in hits.items()),
                    "snippet": snippet,
                    "url": f"https://malegislature.gov/Laws/SessionLaws/Acts/{year}/Chapter{law['ChapterNumber']}",
                }
            )
    with (DATA / "sessionlaw_scan.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{total} session laws scanned, {len(rows)} match at least one term")


if __name__ == "__main__":
    main()
