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

# kinship AND identity rows carry both excerpts
ev = [r for r in queue if r["item_type"] in ("proposition_kinship", "proposition_identity")]
check(all(r["excerpt_a"] and r["excerpt_b"] for r in ev), "kinship/identity rows have side-by-side excerpts")
check(all("quote missing" not in r["excerpt_a"] + r["excerpt_b"] for r in ev), "no missing quotes in queue")

# links are real edges (non-empty endpoints)
check(all(r["source"] and r["target"] for r in links), "all links have non-empty endpoints")

# adjudication coverage over the UNION of both enacted-search outputs
probe = rows("enacted_probe.csv")
check(all(r["verdict"] != "UNADJUDICATED" for r in probe), "every probe hit adjudicated")
adj = rows("enacted_adjudication.csv")
check(len(adj) > 0 and all(r["verdict"] in ("IN-CORE", "EX-PROGRAM-INCIDENT", "EX-ADJACENT", "EX-FALSEPOS") for r in adj), "adjudication verdicts use the fixed vocabulary")
adj_chapters = {(r["year"], r["chapter"]) for r in adj}
scan = rows("sessionlaw_scan.csv")
flagged = {(r["year"], r["chapter"]) for r in scan} | {(r["year"], r["chapter"]) for r in probe}
check(flagged <= adj_chapters, f"every scan/probe-flagged chapter adjudicated (missing: {sorted(flagged - adj_chapters)[:5]})")

# every IN-CORE adjudication maps to propositions with census carriers
import re as _re
carriers_by_prop = {}
for r in bp:
    carriers_by_prop.setdefault(r["prop_id"], set()).add(r["bill"])
for r in adj:
    if r["verdict"] == "IN-CORE":
        mapped = _re.findall(r"P-\d+", r["note"])
        check(bool(mapped), f"IN-CORE row maps to propositions: {r['year']} c.{r['chapter']} {r['sections'][:40]}")
        for pid_m in mapped:
            check(pid_m in carriers_by_prop and carriers_by_prop[pid_m], f"IN-CORE prop {pid_m} has census carriers")

# queue proposition IDs must reference live propositions
for r in queue:
    for field in ("a", "b"):
        for pid_m in _re.findall(r"P-\d+", r[field]):
            check(pid_m in pids, f"queue references live prop: {pid_m} in {r['item_type']}")

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
for pid, expected in (("P-266", "enacted_as_filed"), ("P-280", "enacted_as_filed"),
                      ("P-291", "enacted_other_vehicle"), ("P-294", "enacted_other_vehicle"),
                      ("P-295", "enacted_other_vehicle"), ("P-296", "enacted_other_vehicle"),
                      ("P-297", "enacted_other_vehicle"), ("P-298", "enacted_other_vehicle"),
                      ("P-299", "enacted_as_filed"), ("P-302", "enacted_as_filed"),
                      ("P-303", "enacted_as_filed"), ("P-304", "enacted_as_filed")):
    check(sum(1 for r in fates if r["prop_id"] == pid and r["fate"] == expected) == 1,
          f"{pid} fate is {expected}")

if fails:
    print(f"\n{len(fails)} check(s) failed")
    sys.exit(1)
print(f"all checks passed: {len(census)} census rows, {len(props)} propositions, "
      f"{len(bp)} edges, {len(fates)} fates, {len(queue)} queue items, {len(links)} links")
