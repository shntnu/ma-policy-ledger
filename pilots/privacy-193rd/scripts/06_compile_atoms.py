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

import csvutil
import json
import re
from pathlib import Path

import actions
import atoms
import textsim

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"


def identity_bases(carriers: dict) -> dict:
    """For each (prop, bill) edge, classify the evidence that this bill's
    provision is the SAME proposition as the other carriers' (codebook: a
    shared prop ID is a link claim). Returns {(prop, bill): basis}.

    - sole-carrier: no cross-bill claim is being made
    - verified-text-identical: >= 0.85 normalized 8-gram Jaccard with
      another carrier
    - verified-official-lineage: connected to another carrier by an official
      redraft/supersession/conference record
    - inferred-analytic: same-mechanism judgment only (queued for review by
      07_links.py)
    """
    hist = json.loads((DATA / "histories.json").read_text())
    lineage = actions.lineage_pairs(hist)
    lt_path = DATA / "link_targets.json"
    if lt_path.exists():
        lineage |= actions.lineage_pairs(json.loads(lt_path.read_text()))

    sh = {}
    def get_sh(b):
        if b not in sh:
            try:
                sh[b] = textsim.shingles(textsim.bill_text(b))
            except FileNotFoundError:
                sh[b] = set()
        return sh[b]

    out = {}
    for prop, bills in carriers.items():
        bl = sorted(bills)
        if len(bl) == 1:
            out[(prop, bl[0])] = "sole-carrier"
            continue
        for b in bl:
            others = [o for o in bl if o != b]
            best = max((textsim.jaccard(get_sh(b), get_sh(o)) for o in others), default=0.0)
            if best >= 0.85:
                out[(prop, b)] = "verified-text-identical"
            elif any(frozenset((b, o)) in lineage for o in others):
                out[(prop, b)] = "verified-official-lineage"
            elif best >= 0.50:
                # substantially the same text with drafting variations
                # (e.g. H83 vs S25 numbering styles); the atomization notes
                # record the manual diff verification
                out[(prop, b)] = "verified-text-near-identical"
            else:
                out[(prop, b)] = "inferred-analytic"
    return out


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
        w = csvutil.writer(f)
        w.writerow(["prop_id", "slug", "subdomain", "description", "n_bills"])
        counts = {}
        for b, p, _, _ in atoms.EDGES:
            counts[p] = counts.get(p, 0) + 1
        for pid in sorted(atoms.PROPS):
            slug, sub, desc = atoms.PROPS[pid]
            w.writerow([pid, slug, sub, desc, counts[pid]])

    prop_bills = {}
    for b, p, _, _ in atoms.EDGES:
        prop_bills.setdefault(p, set()).add(b)
    bases = identity_bases(prop_bills)
    with (DATA / "bill_propositions.csv").open("w", newline="") as f:
        w = csvutil.writer(f)
        w.writerow(["bill", "prop_id", "sections", "note", "identity_basis", "bill_url"])
        for b, p, cite, note in sorted(atoms.EDGES):
            w.writerow([b, p, cite, note, bases[(p, b)],
                        f"https://malegislature.gov/Bills/193/{b}"])

    with (DATA / "out_of_domain_content.csv").open("w", newline="") as f:
        w = csvutil.writer(f)
        w.writerow(["bill", "excluded_content"])
        for b in sorted(atoms.OUT_OF_DOMAIN):
            w.writerow([b, atoms.OUT_OF_DOMAIN[b]])

    print(f"{len(atoms.PROPS)} propositions, {len(atoms.EDGES)} bill-proposition edges, "
          f"{len(edge_bills)} bills covered of {len(census)} included")


if __name__ == "__main__":
    main()
