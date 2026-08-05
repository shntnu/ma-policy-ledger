#!/usr/bin/env python3
"""Goal 3 input: fetch the official history (DocumentHistoryActions) for every
bill included in the census, plus similar-bills data from the bill web page.

Runs only after the census checkpoint. Reads data/census.csv, fetches for
each included bill:
  - /api/GeneralCourts/193/Documents/{bill}/DocumentHistoryActions
  - the public bill page /Bills/193/{bill} (its "Similar Bills" block is an
    explicit companion/duplicate record not exposed by the API)

Output: data/histories.json - bill -> {actions: [...], similar: [...]}
"""

import json
import re
from pathlib import Path

import fetchlib

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"
API = "https://malegislature.gov/api"


def similar_bills(html: str) -> list[dict]:
    """Parse the Similar Bills table from a bill page."""
    out = []
    sec = re.search(r"[Ss]imilar [Bb]ills(.*?)</table>", html, re.S)
    if not sec:
        return out
    for m in re.finditer(
        r'href="/Bills/(\d+)/([A-Z]+\d+)"[^>]*>([^<]*)<', sec.group(1)
    ):
        out.append(
            {"general_court": int(m.group(1)), "bill": m.group(2), "label": m.group(3).strip()}
        )
    return out


def main() -> None:
    import csv

    rows = list(csv.DictReader((DATA / "census.csv").open()))
    bills = [r["bill_number"] for r in rows if r["decision"] == "include" and r["bill_number"]]
    result = {}
    for i, bn in enumerate(bills, 1):
        actions = fetchlib.get_json(
            f"{API}/GeneralCourts/193/Documents/{bn}/DocumentHistoryActions"
        )
        page = fetchlib.get(f"https://malegislature.gov/Bills/193/{bn}").decode(
            "utf-8", "replace"
        )
        result[bn] = {"actions": actions, "similar": similar_bills(page)}
        if i % 20 == 0:
            print(f"  {i}/{len(bills)}")
    (DATA / "histories.json").write_text(json.dumps(result, indent=1))
    print(f"wrote histories for {len(result)} bills")


if __name__ == "__main__":
    main()
