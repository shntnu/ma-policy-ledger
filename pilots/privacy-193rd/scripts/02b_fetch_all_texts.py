#!/usr/bin/env python3
"""Fetch the full text of EVERY numbered bill in the 193rd General Court, so
the census can be a full-text screen of the complete corpus rather than a
title/committee-gated sample (third-pass review finding 3).

Uses the standard cache (never re-fetches ~700 already-cached documents) at
a 1.2s interval - a deliberate, documented bulk-mode politeness setting for
this one job (~7,850 requests, ~2.6 hours).
"""

import json
from pathlib import Path

import fetchlib

fetchlib.MIN_INTERVAL = 1.2

PILOT = Path(__file__).resolve().parent.parent
API = "https://malegislature.gov/api"


def main() -> None:
    docs = json.loads((PILOT / "data" / "documents_193.json").read_text())
    bills = sorted({d["BillNumber"] for d in docs if d.get("BillNumber")})
    print(f"{len(bills)} numbered documents")
    done = 0
    errors = []
    for bn in bills:
        try:
            fetchlib.get_json(f"{API}/GeneralCourts/193/Documents/{bn}")
        except Exception as e:
            errors.append((bn, str(e)[:60]))
        done += 1
        if done % 250 == 0:
            print(f"  {done}/{len(bills)} ({len(errors)} errors)")
    print(f"complete: {done} fetched/cached, {len(errors)} errors")
    for bn, e in errors[:20]:
        print("  ERROR", bn, e)


if __name__ == "__main__":
    main()
