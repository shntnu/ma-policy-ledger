#!/usr/bin/env python3
"""Validation suite: referential integrity, path validity, determinism,
and headline-number assertions. Exits nonzero on any failure."""

import csv
import subprocess
import sys
from pathlib import Path

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"
fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)
        print("FAIL:", msg)


def rows(name):
    return list(csv.DictReader((DATA / name).open()))


census = rows("census.csv")
included = {r["bill_number"] for r in census if r["decision"] == "include"}
props = rows("propositions.csv")
bp = rows("bill_propositions.csv")
fates = rows("proposition_fates.csv")
queue = rows("verification_queue.csv")
links = rows("links.csv")

check(all(r["decision"] in ("include", "exclude") for r in census), "census decisions binary")
check({r["bill"] for r in bp} == included, "bill_propositions covers exactly the included bills")
pids = {r["prop_id"] for r in props}
check({r["prop_id"] for r in bp} == pids, "every proposition has edges and vice versa")
check({r["prop_id"] for r in fates} == pids, "every proposition has a fate")
check(all(r["identity_basis"] for r in bp), "every edge has an identity basis")
check(all(r["fate_citation"].startswith("https://malegislature.gov") for r in fates), "fate citations are official URLs")
for r in fates:
    check(r["fate_vehicle"] in r["final_vehicles"].split(";") or r["fate"] == "enacted_other_vehicle",
          f"{r['prop_id']}: fate vehicle among final vehicles")

# verification-queue source paths must exist
for r in queue:
    for path in (r["sources"] or "").split(";"):
        path = path.strip()
        if path and "/" in path and not path.startswith("http"):
            check((PILOT / path.split(" ")[0]).exists() or (PILOT.parent.parent / path).exists(),
                  f"queue path exists: {path}")

# kinship rows carry both excerpts
kin = [r for r in queue if r["item_type"] == "proposition_kinship"]
check(all(r["excerpt_a"] and r["excerpt_b"] for r in kin), "kinship rows have side-by-side excerpts")

# determinism: rerunning 06/07/08 must not change outputs
snap = {}
for name in ("bill_propositions.csv", "links.csv", "verification_queue.csv",
             "proposition_fates.csv", "bill_fates.csv"):
    snap[name] = (DATA / name).read_bytes()
for script in ("06_compile_atoms.py", "07_links.py", "08_fates.py"):
    subprocess.run([sys.executable, script], cwd=PILOT / "scripts",
                   check=True, capture_output=True)
for name, before in snap.items():
    check((DATA / name).read_bytes() == before, f"deterministic rerun: {name}")

# headline assertions
from collections import Counter
fate_counts = Counter(r["fate"] for r in fates)
check(fate_counts.get("indeterminate", 0) == 0, "no indeterminate fates")
check(fate_counts.get("enacted_as_filed", 0) + fate_counts.get("enacted_other_vehicle", 0) >= 1,
      "the NDII enactment is recorded")
check(sum(1 for r in fates if r["prop_id"] == "P-266" and r["fate"] == "enacted_as_filed") == 1,
      "P-266 enacted via its own chain (H4744)")

if fails:
    print(f"\n{len(fails)} check(s) failed")
    sys.exit(1)
print(f"all checks passed: {len(census)} census rows, {len(props)} propositions, "
      f"{len(bp)} edges, {len(fates)} fates, {len(queue)} queue items, {len(links)} links")
