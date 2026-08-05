#!/usr/bin/env python3
"""Goal 2 compiler: validate atoms.py against the census and emit
data/propositions.csv and data/bill_propositions.csv.

Checks:
  - every proposition ID referenced by an edge exists in PROPS
  - every proposition in PROPS has at least one edge
  - every census-included bill has at least one edge (or is listed in
    OUT_OF_DOMAIN with no in-domain content - none currently)
  - no duplicate (bill, prop) pairs
"""

import csv
from pathlib import Path

import atoms

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"


def main() -> None:
    census = {
        r["bill_number"]
        for r in csv.DictReader((DATA / "census.csv").open())
        if r["decision"] == "include"
    }
    edge_bills = {e[0] for e in atoms.EDGES}
    edge_props = {e[1] for e in atoms.EDGES}

    problems = []
    for e in atoms.EDGES:
        if e[1] not in atoms.PROPS:
            problems.append(f"edge references unknown prop: {e}")
    for p in atoms.PROPS:
        if p not in edge_props:
            problems.append(f"prop {p} has no edges")
    for b in sorted(census - edge_bills):
        problems.append(f"included bill {b} has no propositions")
    for b in sorted(edge_bills - census):
        problems.append(f"edge bill {b} is not census-included")
    seen = set()
    for e in atoms.EDGES:
        key = (e[0], e[1])
        if key in seen:
            problems.append(f"duplicate edge {key}")
        seen.add(key)
    if problems:
        for p in problems:
            print("PROBLEM:", p)
        raise SystemExit(1)

    with (DATA / "propositions.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["prop_id", "slug", "subdomain", "description", "n_bills"])
        counts = {}
        for b, p, _, _ in atoms.EDGES:
            counts[p] = counts.get(p, 0) + 1
        for pid in sorted(atoms.PROPS):
            slug, sub, desc = atoms.PROPS[pid]
            w.writerow([pid, slug, sub, desc, counts[pid]])

    with (DATA / "bill_propositions.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bill", "prop_id", "sections", "note", "bill_url"])
        for b, p, cite, note in sorted(atoms.EDGES):
            w.writerow([b, p, cite, note, f"https://malegislature.gov/Bills/193/{b}"])

    with (DATA / "out_of_domain_content.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bill", "excluded_content"])
        for b in sorted(atoms.OUT_OF_DOMAIN):
            w.writerow([b, atoms.OUT_OF_DOMAIN[b]])

    print(f"{len(atoms.PROPS)} propositions, {len(atoms.EDGES)} bill-proposition edges, "
          f"{len(edge_bills)} bills covered of {len(census)} included")


if __name__ == "__main__":
    main()
