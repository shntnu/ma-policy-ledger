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

# study-order terminal evidence: every sent_to_study target has a status row
so_targets = {r["target"] for r in links if r["link_type"] == "sent_to_study"}
so_status = {r["study_order"] for r in rows("study_order_status.csv")}
check(so_targets <= so_status, f"every study order has terminal evidence (missing: {sorted(so_targets - so_status)[:6]})")

# offline completeness: 05c reruns entirely from the committed cache
import os as _os
env = dict(_os.environ, FETCHLIB_OFFLINE="1")
r = subprocess.run([sys.executable, "05c_link_targets.py"], cwd=PILOT / "scripts",
                   env=env, capture_output=True, text=True)
check(r.returncode == 0, f"05c runs offline from committed cache ({r.stderr.strip().splitlines()[-1] if r.stderr else 'no stderr'})")

# determinism: rerunning 06/07/08 must not change outputs
snap = {}
for name in ("bill_propositions.csv", "links.csv", "verification_queue.csv",
             "proposition_fates.csv", "bill_fates.csv", "corpus_scan.csv",
             "census.csv", "sessionlaw_scan.csv", "enacted_probe.csv",
             "enacted_adjudication.csv", "study_order_status.csv",
             "propositions.csv"):
    snap[name] = (DATA / name).read_bytes()
for script in ("03_sessionlaws.py", "01b_full_corpus_screen.py",
               "04_inclusion.py", "06_compile_atoms.py", "07_links.py",
               "08_fates.py"):
    subprocess.run([sys.executable, script], cwd=PILOT / "scripts",
                   check=True, capture_output=True)
for name, before in snap.items():
    check((DATA / name).read_bytes() == before, f"deterministic rerun: {name}")

# headline assertions
from collections import Counter
fate_counts = Counter(r["fate"] for r in fates)
check(fate_counts.get("indeterminate", 0) == 0, "no indeterminate fates")
for pid, expected in (("P-266", "enacted_as_filed"), ("P-280", "enacted_as_filed"),
                      ("P-291", "enacted_as_filed"), ("P-294", "enacted_as_filed"),
                      ("P-295", "enacted_other_vehicle"), ("P-296", "enacted_other_vehicle"),
                      ("P-297", "enacted_other_vehicle"), ("P-298", "enacted_other_vehicle"),
                      ("P-299", "enacted_as_filed"), ("P-302", "enacted_as_filed"),
                      ("P-303", "enacted_as_filed"), ("P-304", "enacted_as_filed"),
                      ("P-371", "enacted_as_filed")):
    check(sum(1 for r in fates if r["prop_id"] == pid and r["fate"] == expected) == 1,
          f"{pid} fate is {expected}")

# --- enacted universe: the official index is the denominator (finding 1)
import sessionlaws
ORDER_STAGE = {s: i for i, s in enumerate([
    "referred", "heard", "reporting_extended", "reported_favorably",
    "second_reading", "engrossed_one_branch", "in_second_branch",
    "conference", "passed_both", "enacted"])}
acts = rows("acts_index.csv")
official = {(str(r["year"]), r["series"], r["chapter"]) for r in sessionlaws.official_index()}
indexed = {(r["year"], r["series"], r["chapter"]) for r in acts}
check(indexed == official,
      f"acts_index.csv is exactly the official index "
      f"(missing {sorted(official - indexed)[:5]}, extra {sorted(indexed - official)[:5]})")
for r in acts:
    check(r["obtained"] == "yes" or r["unobtainable_reason"],
          f"chapter {r['year']} c.{r['chapter']} is scanned or has an unobtainable reason")
check(all(int(r["text_chars"]) > 0 for r in acts if r["obtained"] == "yes"),
      "every obtained chapter has text")
# every term-flagged chapter of that universe reaches the adjudication table
scan_keys = {(r["year"], r["chapter"]) for r in scan}
flagged_from_index = {(r["year"], r["chapter"]) for r in acts if r["text_terms"]}
check(scan_keys == flagged_from_index,
      "sessionlaw_scan.csv flags exactly the term-hit chapters of the official index")

# --- finding 4: no enacted vehicle may be described as having died or as
# lacking a chain to the vehicle that carried the proposition into law
enacted_bills = {r["bill"] for r in rows("bill_fates.csv") if r["terminal_class"] == "enacted"}
for r in fates:
    narrated = set()
    for clause in (r"independent filings of the same proposition \(([^)]*)\) died without",
                   r"filed carriers ([HS\d,]+) have no official chain"):
        for m in _re.finditer(clause, r["detail"]):
            narrated |= set(_re.findall(r"[HS]\d+", m.group(1)))
    check(not (narrated & enacted_bills),
          f"{r['prop_id']}: enacted vehicle in the died narrative "
          f"({sorted(narrated & enacted_bills)})")
    if r["fate"].startswith("enacted"):
        check(r["enacted_vehicles"], f"{r['prop_id']}: enacted fate names its vehicles")
        check(all(v in r["final_vehicles"].split(";") for v in r["enacted_vehicles"].split(";")),
              f"{r['prop_id']}: every enacted vehicle is a final vehicle")
for pid in ("P-301", "P-302"):
    row = next(r for r in fates if r["prop_id"] == pid)
    check(row["enacted_vehicles"] == "H4940;S2884",
          f"{pid} records both enacted vehicles (got {row['enacted_vehicles']!r})")

# --- finding 6: the memo's headline arithmetic must match the tables, so a
# green check cannot coexist with stale prose
memo = (PILOT / "memo" / "findings.md").read_text()
enacted_props = [r for r in fates if r["fate"].startswith("enacted")]
enacted_vehicles = sorted({v for r in enacted_props for v in r["enacted_vehicles"].split(";")})
HEADLINES = [
    (r"Of ([\d,]+) distinct policy propositions", len(props)),
    (r"distinct policy propositions, ([\d,]+) became law", len(enacted_props)),
    (r"of ([\d,]+) in-domain filings", len(included)),
    (r"The ([\d,]+) in-domain filings were atomized", len(included)),
    (r"atomized into ([\d,]+) propositions", len(props)),
    (r"on ([\d,]+) bill-proposition edges", len(bp)),
    (r"an ([\d,]+)-edge link graph", len(links)),
    (r"([\d,]+) items sit in `data/verification_queue.csv`", len(queue)),
    (r"accounts for ([\d,]+) candidate filings", len(census)),
    (r"universe is the official session-law index[^.]*?: ([\d,]+) chapters", len(acts)),
    (r"([\d,]+) row-level verdicts", len(adj)),
    (r"verdicts across ([\d,]+) chapters", len({(r["year"], r["chapter"]) for r in adj})),
    (r"\*\*([A-Za-z]+) of [\d,]+ propositions became law", len(enacted_props)),
    (r"\*\*[A-Za-z]+ of ([\d,]+) propositions became law", len(props)),
    (r"through ([a-z]+) enacted vehicles", len(enacted_vehicles)),
    (r"([A-Za-z]+) passed through their own official chains",
     fate_counts.get("enacted_as_filed", 0)),
    (r"([A-Za-z]+) were absorbed into unrelated enacted vehicles",
     fate_counts.get("enacted_other_vehicle", 0)),
    (r"The other ([\d,]+) propositions died", len(fates) - len(enacted_props)),
    (r"([\d,]+) propositions \(\d+%\) died with no recorded action",
     fate_counts.get("died_no_recorded_action", 0)),
    (r"; ([\d,]+) \(\d+%\) were sent to study", fate_counts.get("sent_to_study", 0)),
    (r"For all ([\d,]+), the record offers", len(fates) - len(enacted_props)),
    (r"([\d,]+) propositions \(\d+%\) cleared a policy committee",
     sum(1 for r in fates if ORDER_STAGE[r["furthest_stage"]] >= ORDER_STAGE["reported_favorably"])),
    (r"([\d,]+) \(\d+%\) were dropped during official consolidations",
     sum(1 for r in fates if r["dropped_in_consolidation"] == "yes")),
    (r"([\d,]+) propositions never got a hearing",
     sum(1 for r in fates if r["furthest_stage"] == "referred")),
    (r"; ([\d,]+) were enacted\.", len(enacted_props)),
    (r"([\d,]+) cross-bill proposition-identity claims",
     sum(1 for r in bp if r["identity_basis"] == "inferred-analytic")),
]
WORDS = {"twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
         "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "four": 4}
for pattern, expected in HEADLINES:
    found = _re.findall(pattern, memo, _re.IGNORECASE)
    check(bool(found), f"memo headline present: /{pattern}/")
    for raw in found:
        val = WORDS.get(raw.lower(), None)
        if val is None:
            val = int(raw.replace(",", ""))
        check(val == expected,
              f"memo headline /{pattern}/ says {raw}, tables say {expected}")
pct = round(100 * len(enacted_props) / len(props), 1)
for hit in _re.findall(r"\((\d+\.\d)%\)|the (\d+\.\d)% rate", memo):
    got = float(hit[0] or hit[1])
    check(got == pct, f"memo passage rate says {got}%, tables say {pct}%")

if fails:
    print(f"\n{len(fails)} check(s) failed")
    sys.exit(1)
print(f"all checks passed: {len(census)} census rows, {len(props)} propositions, "
      f"{len(bp)} edges, {len(fates)} fates, {len(queue)} queue items, {len(links)} links")
