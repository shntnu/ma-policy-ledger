#!/usr/bin/env python3
"""Fetch every document the link graph points at but the census did not
include, so no terminal claim rests on an unfetched record (review finding 7):

  - redraft successors outside the census (H4502)
  - all study orders named by "Accompanied a study order, see X"
  - budget vehicles named by "Reported on a part of X" (H4496)
  - origin bills of enacted chapters with in-domain content (H4744, from the
    /api/SessionLaws OriginBill field), plus the parents named in their
    histories (the standalone filings consolidated into them)

Output: data/link_targets.json - document metadata, text, and history for
each target.
"""

import json
import re
from pathlib import Path

import fetchlib

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"
API = "https://malegislature.gov/api"

# Origin bills of enacted chapters confirmed in-domain during probe review.
ENACTED_ORIGINS = ["H4744"]


def fetch_doc(bn: str) -> dict:
    doc = fetchlib.get_json(f"{API}/GeneralCourts/193/Documents/{bn}")
    hist = fetchlib.get_json(
        f"{API}/GeneralCourts/193/Documents/{bn}/DocumentHistoryActions"
    )
    text = re.sub(r"<[^>]+>", " ", doc.get("DocumentText") or "")
    return {
        "BillNumber": bn,
        "Title": (doc.get("Title") or "").strip(),
        "LegislationTypeName": doc.get("LegislationTypeName"),
        "text_chars": len(text),
        "text": re.sub(r"\s+", " ", text),
        "actions": hist,
    }


def main() -> None:
    hist = json.loads((DATA / "histories.json").read_text())
    census_bills = set(hist)
    targets = set()
    for bn, d in hist.items():
        for a in d["actions"]:
            for pat in (
                r"Accompanied a study order, see ([HS]\d+)",
                r"Accompanied a new draft, see ([HS]\d+)",
                r"Reported on a part of ([HS]\d+)",
            ):
                m = re.search(pat, a["Action"])
                if m and m.group(1) not in census_bills:
                    targets.add(m.group(1))
    targets.update(ENACTED_ORIGINS)

    out = {}
    for bn in sorted(targets):
        out[bn] = fetch_doc(bn)
        print(f"  {bn}: {out[bn]['Title'][:70]}")
    # follow enacted-origin lineage: "Reported on X" (conference), "New draft
    # of ..." parents, and any "Accompanied a new draft" pointers, until the
    # frontier is exhausted (bounded by the session's own records)
    frontier = list(ENACTED_ORIGINS)
    seen = set(out) | census_bills
    while frontier:
        bn = frontier.pop()
        doc = out.get(bn) or fetch_doc(bn)
        out.setdefault(bn, doc)
        found = set()
        for a in doc["actions"]:
            act = a["Action"].strip()
            m = re.match(r"New draft of (.+)", act)
            if m:
                found.update(re.findall(r"[HS]\d+", m.group(1)))
            m = re.search(r"Reported on ([HS]\d+)", act)
            if m:
                found.add(m.group(1))
            m = re.search(r"(?:in part )?[Bb]y ([HS]\d+)", act)
            if m:
                found.add(m.group(1))
        for p in sorted(found - seen):
            seen.add(p)
            out[p] = fetch_doc(p)
            print(f"  lineage {p}: {out[p]['Title'][:70]}")
            frontier.append(p)

    (DATA / "link_targets.json").write_text(json.dumps(out, indent=1))
    print(f"wrote {len(out)} link-target documents")


if __name__ == "__main__":
    main()
