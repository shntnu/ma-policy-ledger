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
    """Parse bill links out of a /Bills/193/{bill}/SimilarBills tab page."""
    out = []
    seen = set()
    for m in re.finditer(r'href="/Bills/(\d+)/([A-Z]+\.?\d+)"', html):
        key = (int(m.group(1)), m.group(2))
        if key not in seen:
            seen.add(key)
            out.append({"general_court": key[0], "bill": key[1]})
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
        fetchlib.get(f"https://malegislature.gov/Bills/193/{bn}")  # cached bill page
        sim = fetchlib.get(
            f"https://malegislature.gov/Bills/193/{bn}/SimilarBills"
        ).decode("utf-8", "replace")
        result[bn] = {"actions": actions, "similar": similar_bills(sim)}
        if i % 20 == 0:
            print(f"  {i}/{len(bills)}")
    (DATA / "histories.json").write_text(json.dumps(result, indent=1))
    print(f"wrote histories for {len(result)} bills")


if __name__ == "__main__":
    main()
