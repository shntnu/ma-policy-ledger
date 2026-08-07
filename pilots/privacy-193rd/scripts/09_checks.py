#!/usr/bin/env python3
"""Validation suite: referential integrity, path validity, determinism,
and headline-number assertions. Exits nonzero on any failure."""

import csv
import re as _re
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
# eighth-pass review: eight rows carried hand-written prose in `title` instead
# of the official title. 04 now always prefers the official one.
_official_titles = {
    d["BillNumber"]: _re.sub(r"\s+", " ", (d.get("Title") or "")).strip()
    for d in __import__("json").loads((DATA / "documents_193.json").read_text())
    if d.get("BillNumber")
}
# The corpus-screen path truncates long titles to 110 characters, so a census
# title must be the official title or a leading slice of it - never a
# hand-written paraphrase, which is what the eighth pass found.
for r in census:
    _bn = r["bill_number"]
    _off = _official_titles.get(_bn)
    if _bn and _off:
        check(_off.startswith(_re.sub(r"\s+", " ", r["title"]).strip()),
              f"census title for {_bn} is the official title (or a prefix of it): "
              f"got {r['title'][:60]!r}, official {_off[:60]!r}")
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

# --- eighth-pass finding 5: the excerpts must actually BE verbatim.
# The codebook, the memo and atoms.py all promise verbatim excerpts from the
# official texts, and nothing tested it: 58 of 155 QUOTES entries were analyst
# prose, and one attributed to S1116 an intent element ("with intent to
# harass") that the bill does not contain - manufacturing agreement on the
# exact axis where it and its comparator differ. This is the load-bearing
# check of that finding; it is what prevents recurrence.
import importlib as _il
import verbatim
import actions as _actions_mod
# every module with fixtures self-tests here, so one command certifies them
_actions_mod.self_test()
verbatim.self_test()
_il.import_module("08_fates")._self_test()
_atoms = _il.import_module("atoms")
for (bill, pid), quote in sorted(_atoms.QUOTES.items()):
    try:
        miss = verbatim.missing_fragments(bill, quote)
    except ValueError as e:
        check(False, f"QUOTES: {e}")
        continue
    check(not miss, f"QUOTES[{bill},{pid}] is not verbatim from {bill}: {miss}")
# and the same over what actually reaches the reviewer.
# Identity rows name a bill-proposition pair, so the excerpt is checked against
# that bill. Kinship rows name bare propositions; before this the loop skipped
# them, leaving 80 of 248 excerpt sides untested while the memo and codebook
# claimed every queue excerpt was checked - and two of the skipped excerpts
# were analyst paraphrase. A kinship excerpt is checked against the
# proposition's carrier bills and must be verbatim from at least one of them.
_QROW = _re.compile(r"^(P-\d+):([HS]\d+)$")
_carriers = {}
for _r in bp:
    _carriers.setdefault(_r["prop_id"], []).append(_r["bill"])
for r in queue:
    if r["item_type"] not in ("proposition_kinship", "proposition_identity"):
        continue
    for side, excerpt in (("a", r["excerpt_a"]), ("b", r["excerpt_b"])):
        m = _QROW.match(r[side])
        if m:
            bills = [m.group(2)]
        elif _re.fullmatch(r"P-\d+", r[side]):
            bills = sorted(_carriers.get(r[side], []))
            check(bool(bills), f"queue {r[side]} has carrier bills to quote from")
        else:
            check(False, f"queue row side {side} is not a proposition or pair: {r[side]!r}")
            continue
        best, quotable = None, False
        for bill in bills:
            try:
                miss = verbatim.missing_fragments(bill, excerpt)
            except ValueError:
                continue  # this carrier has no recoverable text; try the next
            quotable = True
            if best is None or len(miss) < len(best[1]):
                best = (bill, miss)
            if not miss:
                break
        if not quotable:
            check(False, f"queue excerpt_{side} ({r[side]}): no carrier has recoverable text")
            continue
        check(best is not None and not best[1],
              f"queue {r['item_type']} excerpt_{side} ({r[side]}) is not verbatim "
              f"from any carrier (closest {best[0]}: {best[1]})")

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
             "propositions.csv", "acts_index.csv", "acts_index_sources.csv",
             "text_scan.csv"):
    snap[name] = (DATA / name).read_bytes()
snap["histories.json"] = (DATA / "histories.json").read_bytes()
# eighth pass: 02_textscan.py and 05_histories.py were absent from this list,
# so text_scan.csv and histories.json were never re-derived from the raw cache
# and a count-neutral edit already propagated into them survived a green suite.
# Both rerun offline in under a second.
for script in ("02_textscan.py", "05_histories.py",
               "03b_acts_index.py", "03_sessionlaws.py",
               "01b_full_corpus_screen.py", "04_inclusion.py",
               "06_compile_atoms.py", "07_links.py", "08_fates.py"):
    subprocess.run([sys.executable, script], cwd=PILOT / "scripts",
                   check=True, capture_output=True)
for name, before in snap.items():
    check((DATA / name).read_bytes() == before, f"deterministic rerun: {name}")

# headline assertions
from collections import Counter
fate_counts = Counter(r["fate"] for r in fates)
check(fate_counts.get("indeterminate", 0) == 0, "no indeterminate fates")
# P-295/P-296 moved from enacted_other_vehicle to enacted_as_filed in the
# eighth pass: the official chain H4138 -> H4707 -> H4726 -> H4977 is one bill
# lineage, published in links.csv as verified-official-record, and the fate
# stage now follows it (see 08_fates.successor_universe and the codebook).
for pid, expected in (("P-266", "enacted_as_filed"), ("P-280", "enacted_as_filed"),
                      ("P-291", "enacted_as_filed"), ("P-294", "enacted_as_filed"),
                      ("P-295", "enacted_as_filed"), ("P-296", "enacted_as_filed"),
                      ("P-297", "enacted_other_vehicle"), ("P-298", "enacted_other_vehicle"),
                      ("P-299", "enacted_as_filed"), ("P-302", "enacted_as_filed"),
                      ("P-303", "enacted_as_filed"), ("P-304", "enacted_as_filed"),
                      ("P-371", "enacted_as_filed"),
                      # eighth-pass finding 4 splits: the capture limit was
                      # never enacted, the destruction schedule was; the
                      # redaction duty reached only 2024 c.363
                      ("P-378", "sent_to_study"), ("P-379", "enacted_as_filed"),
                      ("P-380", "enacted_as_filed"), ("P-381", "enacted_as_filed")):
    check(sum(1 for r in fates if r["prop_id"] == pid and r["fate"] == expected) == 1,
          f"{pid} fate is {expected}")

# --- enacted universe: the official index is the denominator (finding 1)
import importlib
import sessionlaws
ORDER_STAGE = importlib.import_module("08_fates").ORDER
acts = rows("acts_index.csv")
official = {(str(r["year"]), r["series"], r["chapter"]) for r in sessionlaws.official_index()}
indexed = {(r["year"], r["series"], r["chapter"]) for r in acts}
check(indexed == official,
      f"acts_index.csv is exactly the official index "
      f"(missing {sorted(official - indexed)[:5]}, extra {sorted(indexed - official)[:5]})")
# the substantive coverage claim: every officially indexed chapter yielded
# text. (Asserting "obtained or a reason recorded" would be vacuous - 03b
# derives both fields from the same emptiness test.)
for r in acts:
    check(int(r["text_chars"]) > 0,
          f"chapter {r['year']} c.{r['chapter']} yielded no text: "
          f"{r['unobtainable_reason'] or 'no reason recorded'}")
# every term-flagged chapter of that universe reaches the adjudication table.
# Both sides are compared in adj_key space (Acts bare, Resolves "R"-prefixed),
# or an Acts chapter and a Resolve of the same number would collide.
scan_keys = {(r["year"], r["chapter"]) for r in scan}
flagged_from_index = {(r["year"], r["key"]) for r in acts if r["text_terms"]}
check(scan_keys == flagged_from_index,
      "sessionlaw_scan.csv flags exactly the term-hit chapters of the official index")

# --- finding 4: a bill that was itself enacted may never be counted among a
# proposition's dead carriers, and every enacted carrier must be represented.
# Both are checked against the structured columns; the prose detail is
# generated from the same lists, so there is nothing to re-parse.
enacted_bills = {r["bill"] for r in rows("bill_fates.csv") if r["terminal_class"] == "enacted"}
for r in fates:
    died = set(filter(None, r["died_carriers"].split(";")))
    check(not (died & enacted_bills),
          f"{r['prop_id']}: enacted vehicle counted as a dead carrier "
          f"({sorted(died & enacted_bills)})")
    carried_and_enacted = set(r["all_vehicles"].split(";")) & enacted_bills
    check(carried_and_enacted == set(filter(None, r["enacted_vehicles"].split(";"))),
          f"{r['prop_id']}: enacted carriers {sorted(carried_and_enacted)} "
          f"vs enacted_vehicles {r['enacted_vehicles']!r}")
    for bn in died:
        check(bn in r["detail"], f"{r['prop_id']}: died carrier {bn} absent from the detail")
    if r["fate"].startswith("enacted"):
        check(r["enacted_vehicles"], f"{r['prop_id']}: enacted fate names its vehicles")
        check(all(v in r["final_vehicles"].split(";") for v in r["enacted_vehicles"].split(";")),
              f"{r['prop_id']}: every enacted vehicle is a final vehicle")
for pid in ("P-380", "P-302"):
    row = next(r for r in fates if r["prop_id"] == pid)
    check(row["enacted_vehicles"] == "H4940;S2884",
          f"{pid} records both enacted vehicles (got {row['enacted_vehicles']!r})")

# --- eighth-pass finding 2: the adverse-roll-call count is a prose claim in
# both the memo and the codebook and was wrong ("exactly one" against two).
# Assert it against the same regexes 08_fates uses, so it cannot go stale.
import json as _json
_hist = _json.loads((DATA / "histories.json").read_text())
_TALLY = (r"(\d+)\s*YEAS?\s*to\s*(\d+)\s*NAYS?\s*\(See YEA and NAY No\. \d+\)",
          r"Roll Call #\d+ \(Yeas (\d+) to Nays (\d+)\)")
_adverse = []
for _bn in sorted(_hist):
    for _a in _hist[_bn]["actions"]:
        if _a.get("IsStricken"):
            continue
        for _rx in _TALLY:
            _m = _re.search(_rx, _a["Action"])
            if _m:
                if int(_m.group(2)) > int(_m.group(1)):
                    _adverse.append((_bn, _a["Action"].splitlines()[0][:60]))
                break
check(len(_adverse) == 2,
      f"census histories contain exactly two adverse roll calls (got {len(_adverse)}: {_adverse})")
check({b for b, _ in _adverse} == {"H4040", "S2834"},
      f"the two adverse roll calls are H4040's Rule 40 motion and S2834 Amendment 25 (got {sorted({b for b, _ in _adverse})})")
# neither is a proposition defeat: no proposition's fate is a recorded-vote
# rejection, which is the claim that actually matters
check(fate_counts.get("rejected_by_recorded_vote", 0) == 0,
      "no proposition was rejected by recorded vote")

# --- eighth-pass finding 6: "every consolidated privacy vehicle died in Ways
# and Means" was a false universal. Assert the shape of the fan-in directly so
# the memo sentence has a table behind it.
_fanin = Counter(r["source"] for r in links if r["link_type"] == "redraft_of")
_consol = {b for b, n in _fanin.items() if n >= 2}
_bf = {r["bill"]: r for r in rows("bill_fates.csv")}
_consol_enacted_chain = sorted(
    b for b in _consol if _bf.get(b, {}).get("terminal_class") == "superseded_by_redraft")
check(len(_consol) >= 9,
      f"at least nine consolidation redrafts with two or more parents (got {len(_consol)})")
check({"H4115", "H4450"} <= set(_consol_enacted_chain),
      "H4115 and H4450 are consolidation redrafts that were superseded onward rather than "
      f"dying in committee (got {_consol_enacted_chain})")
check({"H4632", "S2539"} <= _consol,
      "H4632 and S2539 are the two omnibus consumer-privacy consolidations")

# --- eighth-pass finding 3: widening the successor universe to the committed
# link targets must not change any CENSUS bill's own successor; it may only
# let a chain continue through a non-census stage.
_fates_mod = importlib.import_module("08_fates")
import actions as _actions
_sm_census = _actions.successor_map(_hist)
_sm_union = _actions.successor_map(_fates_mod.successor_universe(_hist))
_moved = {k for k in set(_sm_census) | set(_sm_union)
          if k in _hist and _sm_census.get(k) != _sm_union.get(k)}
check(not _moved,
      f"link-target union leaves every census bill's own successor unchanged (moved: {sorted(_moved)})")

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
    (r"an? ([\d,]+)-edge link graph", len(links)),
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
    (r"([A-Za-z]+) were absorbed into an unrelated enacted vehicle",
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
    # remaining counts the memo asserts
    (r"of [\d,]+ in-domain filings, ([\d,]+) were enacted", len(enacted_bills)),
    (r"([\d,]+) stalled in policy committee",
     sum(1 for r in fates if r["furthest_stage"] in ("heard", "reporting_extended"))),
    (r"\(([\d,]+) heard only", sum(1 for r in fates if r["furthest_stage"] == "heard")),
    (r"([\d,]+) with repeated reporting extensions",
     sum(1 for r in fates if r["furthest_stage"] == "reporting_extended")),
    (r"([\d,]+) cleared committee and stalled afterward",
     sum(1 for r in fates if r["furthest_stage"] == "reported_favorably")),
    (r"([\d,]+) got further \(a second reading",
     sum(1 for r in fates if r["furthest_stage"] in ("second_reading", "in_second_branch"))),
    (r"([\d,]+) filed-side triage verdicts",
     sum(1 for _ in csv.DictReader((PILOT / "scripts" / "corpus_triage_verdicts.csv").open()))),
    (r"\(([\d,]+) inferred links", sum(1 for r in queue if r["item_type"] != "judgment_flag")),
    (r"plus ([\d,]+) judgment flags",
     sum(1 for r in queue if r["item_type"] == "judgment_flag")),
    (r"for ([a-z]+) of the [a-z]+ a standalone filing",
     sum(1 for r in enacted_props if r["died_carriers"])),
    (r"for [a-z]+ of the ([a-z]+) a standalone filing", len(enacted_props)),
    (r"([\d,]+) of the [\d,]+ numbered filings .{0,40}were full-text screened",
     len(rows("corpus_scan.csv")) and 8183 - len(rows("unscanned_bills.csv"))),
    (r"([\d,]+) chapters \(2023 Acts", len(acts)),
]
WORDS = {"two": 2, "four": 4, "eight": 8, "twelve": 12, "thirteen": 13,
         "fifteen": 15, "sixteen": 16, "seventeen": 17}
for pattern, expected in HEADLINES:
    found = _re.findall(pattern, memo, _re.IGNORECASE)
    check(bool(found), f"memo headline present: /{pattern}/")
    for raw in found:
        if raw.replace(",", "").isdigit():
            val = raw.replace(",", "")
            val = int(val)
        elif raw.lower() in WORDS:
            val = WORDS[raw.lower()]
        else:
            # an unmapped number word must be a reported failure, not a crash
            check(False, f"memo headline /{pattern}/ says {raw!r}, which "
                         f"09_checks.WORDS cannot read (tables say {expected})")
            continue
        check(val == expected,
              f"memo headline /{pattern}/ says {raw}, tables say {expected}")
pct = round(100 * len(enacted_props) / len(props), 1)
for raw in _re.findall(r"(\d+\.\d)%", memo):
    check(float(raw) == pct, f"memo passage rate says {raw}%, tables say {pct}%")

if fails:
    print(f"\n{len(fails)} check(s) failed")
    sys.exit(1)
print(f"all checks passed: {len(census)} census rows, {len(props)} propositions, "
      f"{len(bp)} edges, {len(fates)} fates, {len(queue)} queue items, {len(links)} links")
