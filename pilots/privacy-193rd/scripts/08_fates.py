#!/usr/bin/env python3
"""Goal 4: classify the fate of every bill and every proposition.

Order of operations (review finding 2): the enacted-vehicle sweep runs
FIRST; its reviewed verdicts live in ENACTED_MATCHES (data-as-code, like the
census OVERRIDES) and feed proposition fate assignment, so a genuine enacted
match can and does change a fate.

Bill level (data/bill_fates.csv): terminal class from the official history.
Proposition level (data/proposition_fates.csv): the chain is followed
through redrafts, engrossments, and conference reports (successor patterns:
"Accompanied a new draft, see X", "New draft substituted, see X",
"Reported by X"); a successor counts only if it carries the proposition.
Fate vocabulary: enacted_as_filed / enacted_other_vehicle /
rejected_by_recorded_vote / sent_to_study / died_no_recorded_action /
indeterminate. The citation is the vehicle that ESTABLISHES the fate
(review finding 6); the furthest-stage vehicle is cited separately.
All selections iterate in sorted order (deterministic output).
"""

import csv
import json
import re
from pathlib import Path

import fetchlib

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"
API = "https://malegislature.gov/api"

STAGES = [
    "referred", "heard", "reporting_extended", "reported_favorably",
    "second_reading", "engrossed_one_branch", "in_second_branch",
    "conference", "passed_both", "enacted",
]
ORDER = {s: i for i, s in enumerate(STAGES)}

# Signature phrases per proposition family for the enacted-vehicle sweep.
PROBES = {
    "education-to-career": ["education-to-career"],
    "comprehensive-privacy": ["data privacy protection act", "information privacy and security act", "covered data", "targeted advertising"],
    "location": ["location information", "location shield", "geofen"],
    "biometric": ["biometric"],
    "breach-93H": ["chapter 93h", "93h"],
    "facial-recognition": ["facial recognition"],
    "alpr": ["license plate reader", "alpr"],
    "data-broker": ["data broker"],
    "student-data": ["student data", "education records", "34i"],
    "social-media": ["social media"],
    "911": ["911 call", "audio recording of a 911", "public safety answering point"],
    "lottery": ["lottery"],
    "victim-comp": ["victim compensation"],
    "tolling": ["tolling data", "toll collection technolog"],
    "trigger-lead": ["trigger lead", "mortgage trigger"],
    "isp": ["internet service provider"],
    "health-data": ["consumer health data"],
    "drone": ["unmanned aerial"],
    "scorecard": ["scorecard"],
    "doxing": ["doxing", "personal information with the intent"],
    "ndii": ["visual material", "digitization"],
}

# Reviewed verdicts from data/enacted_probe.csv. Every probe hit is either
# matched to a proposition here or dismissed as a false positive (the
# codebook records the review).
# prop_id -> (year, chapter, section, url, note)
ENACTED_MATCHES = {
    "P-266": (2024, "118", "s.6 (c.265 s.43A(b)-(c))",
              "https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter118",
              "NDII distribution/threat offense incl. digitization; origin bill H4744 per the chapter's OriginBill record"),
}
PROBE_FALSE_POSITIVES = (
    "All other probe hits reviewed 2026-08-05: 'alpr' matches 'malpractice'; "
    "lottery/victim-comp hits are appropriation line items; biometric/"
    "facial-recognition hits in 2023 c.2 authorize RMV identity verification "
    "(government use, not a census proposition); 2024 c.238 biometric hits "
    "are data-center physical security and nurse-licensure fingerprinting; "
    "93H hits are compliance cross-references; student-data hit is a grant "
    "proviso; 'visual material' hits outside c.118 are obscenity-statute "
    "cross-references."
)


def bill_status(actions):
    stage = "referred"
    def bump(s):
        nonlocal stage
        if ORDER[s] > ORDER[stage]:
            stage = s
    roll_calls = []
    terminal = "died_no_further_action"
    terminal_ref = ""
    last_real = None
    for a in actions:
        if a.get("IsStricken"):
            continue
        act = a["Action"].strip()
        d = a["Date"][:10]
        low = act.lower()
        if "hearing scheduled" in low:
            bump("heard")
        if "reporting date extended" in low:
            bump("reporting_extended")
        if "reported favorably" in low or re.search(r"reported.*ought to pass", low) or "reported from the committee" in low:
            bump("reported_favorably")
        if "ordered to a third reading" in low or "read second" in low:
            bump("second_reading")
        if "passed to be engrossed" in low:
            bump("engrossed_one_branch")
        if re.search(r"read; and referred to the committee on senate|referred to the committee on senate ways and means", low) and stage == "engrossed_one_branch":
            bump("in_second_branch")
        if "committee of conference" in low:
            bump("conference")
        if re.match(r"enacted", low) or "passed to be enacted" in low:
            bump("passed_both")
        if "signed by the governor" in low or re.search(r"chapter \d+ of the acts", low):
            bump("enacted")
            terminal, terminal_ref = "enacted", act
        for rx in (r"\d+\s*YEAS?\s*to\s*\d+\s*NAYS?\s*\(See YEA and NAY No\. \d+\)",
                   r"Roll Call #\d+ \(Yeas \d+ to Nays \d+\)"):
            if re.search(rx, act):
                roll_calls.append(f"{d} {act.splitlines()[0][:80]}")
                break
        m = re.search(r"Accompanied a new draft, see ([HS]\d+)", act)
        if m:
            terminal, terminal_ref = "superseded_by_redraft", m.group(1)
        m = re.search(r"New draft substituted, see ([HS]\d+)", act)
        if m:
            terminal, terminal_ref = "superseded_by_redraft", m.group(1)
        m = re.search(r"Reported by ([HS]\d+)", act)
        if m:
            terminal, terminal_ref = "superseded_by_redraft", m.group(1)
        m = re.search(r"Accompanied a study order, see ([HS]\d+)", act)
        if m:
            terminal, terminal_ref = "sent_to_study", m.group(1)
        if "no further action taken" not in low:
            last_real = f"{d} {act[:100]}"
    return stage, terminal, terminal_ref, roll_calls, last_real


def run_probe():
    rows = []
    for year in (2023, 2024):
        laws = fetchlib.get_json(f"{API}/SessionLaws/{year}")
        for law in laws:
            plain = re.sub(r"<[^>]+>", " ", law.get("ChapterText") or "")
            plain = re.sub(r"\s+", " ", plain)
            low = plain.lower()
            for fam in sorted(PROBES):
                for ph in PROBES[fam]:
                    m = re.search(re.escape(ph), low)
                    if m:
                        rows.append({
                            "family": fam, "phrase": ph, "year": year,
                            "chapter": law["ChapterNumber"],
                            "title": (law.get("Title") or "")[:80],
                            "snippet": plain[max(0, m.start() - 100): m.end() + 150],
                            "url": f"https://malegislature.gov/Laws/SessionLaws/Acts/{year}/Chapter{law['ChapterNumber']}",
                        })
    with (DATA / "enacted_probe.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["family", "phrase", "year", "chapter", "title", "snippet", "url"])
        w.writeheader()
        w.writerows(rows)
    return rows


def main() -> None:
    probe_rows = run_probe()

    hist = json.loads((DATA / "histories.json").read_text())
    props = {r["prop_id"]: r for r in csv.DictReader((DATA / "propositions.csv").open())}
    bp = list(csv.DictReader((DATA / "bill_propositions.csv").open()))
    carriers = {}
    for r in bp:
        carriers.setdefault(r["prop_id"], set()).add(r["bill"])

    statuses = {bn: bill_status(hist[bn]["actions"]) for bn in sorted(hist)}
    with (DATA / "bill_fates.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bill", "furthest_stage", "terminal_class", "terminal_ref", "roll_calls", "last_recorded_action", "history_url"])
        for bn in sorted(statuses):
            st = statuses[bn]
            w.writerow([bn, st[0], st[1], st[2], "; ".join(st[3]), st[4],
                        f"https://malegislature.gov/Bills/193/{bn}"])

    successor = {}
    for bn in sorted(hist):
        for a in hist[bn]["actions"]:
            for pat in (r"Accompanied a new draft, see ([HS]\d+)",
                        r"New draft substituted, see ([HS]\d+)",
                        r"Reported by ([HS]\d+)"):
                m = re.search(pat, a["Action"])
                if m:
                    successor[bn] = m.group(1)

    out = []
    for pid in sorted(carriers):
        bills = sorted(carriers[pid])
        finals = sorted(
            b for b in bills
            if not (successor.get(b) and successor[b] in bills)
        )
        terms = {b: statuses[b][1] for b in finals}
        stage = max((statuses[b][0] for b in finals), key=lambda s: ORDER[s])
        stage_bill = min(b for b in finals if statuses[b][0] == stage)
        dropped = sorted(b for b in bills if successor.get(b) and successor[b] not in bills)
        all_dropped = bool(finals) and all(t == "superseded_by_redraft" for t in terms.values())

        enacted_finals = sorted(b for b in finals if statuses[b][0] == "enacted")
        if enacted_finals:
            fb = enacted_finals[0]
            fate = "enacted_as_filed"
            detail = f"enacted via {fb}: {statuses[fb][2]}"
            cite = f"https://malegislature.gov/Bills/193/{fb}"
        elif pid in ENACTED_MATCHES:
            year, ch, sec, url, note = ENACTED_MATCHES[pid]
            fb = stage_bill
            fate = "enacted_other_vehicle"
            detail = f"text enacted at {year} c.{ch} {sec}: {note}"
            cite = url
        elif "sent_to_study" in terms.values():
            fb = min(b for b in finals if terms[b] == "sent_to_study")
            fate = "sent_to_study"
            detail = (f"final vehicle {fb} accompanied study order {statuses[fb][2]}; "
                      "no public explanation of substance")
            cite = f"https://malegislature.gov/Bills/193/{fb}"
        elif "died_no_further_action" in terms.values():
            fb = min(b for b in finals if terms[b] == "died_no_further_action")
            fate = "died_no_recorded_action"
            detail = f"final vehicle {fb} ended with no further action; no public explanation"
            cite = f"https://malegislature.gov/Bills/193/{fb}"
        elif all_dropped:
            fb = min(finals)
            fate = "died_no_recorded_action"
            detail = (f"dropped in consolidation: {','.join(dropped)} superseded by "
                      f"{','.join(sorted({successor[b] for b in dropped}))} which does not carry "
                      "this proposition; no public explanation")
            cite = f"https://malegislature.gov/Bills/193/{fb}"
        else:
            fb = min(finals) if finals else min(bills)
            fate = "indeterminate"
            detail = "terminal record unclear"
            cite = f"https://malegislature.gov/Bills/193/{fb}"
        if dropped and fate not in ("enacted_as_filed", "enacted_other_vehicle") and not all_dropped:
            detail += f"; also dropped in consolidation from {','.join(dropped)} (no public explanation)"
        out.append({
            "prop_id": pid,
            "slug": props[pid]["slug"],
            "fate": fate,
            "fate_vehicle": fb,
            "furthest_stage": stage,
            "furthest_stage_vehicle": stage_bill,
            "dropped_in_consolidation": "yes" if dropped else "no",
            "final_vehicles": ";".join(finals),
            "all_vehicles": ";".join(bills),
            "roll_calls": "; ".join(statuses[stage_bill][3]),
            "detail": detail,
            "fate_citation": cite,
            "stage_citation": f"https://malegislature.gov/Bills/193/{stage_bill}",
        })
    with (DATA / "proposition_fates.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    from collections import Counter
    print("bill terminal classes:", dict(sorted(Counter(s[1] for s in statuses.values()).items())))
    print("bill furthest stages:", dict(sorted(Counter(s[0] for s in statuses.values()).items())))
    print("prop fates:", dict(sorted(Counter(r["fate"] for r in out).items())))
    print("prop furthest stages:", dict(sorted(Counter(r["furthest_stage"] for r in out).items())))
    print(f"enacted-probe hits: {len(probe_rows)}; matched: {sorted(ENACTED_MATCHES)}")


if __name__ == "__main__":
    main()
