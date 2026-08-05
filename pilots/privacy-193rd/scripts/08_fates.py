#!/usr/bin/env python3
"""Goal 4: classify the fate of every bill and every proposition.

Bill level (data/bill_fates.csv): terminal class from the official history -
superseded_by_redraft / sent_to_study / died_no_further_action - plus the
furthest procedural stage reached, the point of stall, and any roll calls.

Proposition level (data/proposition_fates.csv): each proposition's chain is
followed through redrafts (a successor counts only if it carries the same
proposition). Fate vocabulary, from the mission:
  enacted_as_filed / enacted_other_vehicle / rejected_by_recorded_vote /
  sent_to_study / died_no_recorded_action / indeterminate
plus a detail field. Where the record gives no reason, detail says
"no public explanation".

Enacted-vehicle sweep (data/enacted_probe.csv): targeted signature-phrase
search of all 464 enacted 2023-2024 chapters for each proposition family,
so "enacted through another vehicle" is checked against the full session-law
corpus, not assumed.
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
    "passed_both", "enacted",
]

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
}


def bill_status(actions):
    stage = "referred"
    order = {s: i for i, s in enumerate(STAGES)}
    def bump(s):
        nonlocal stage
        if order[s] > order[stage]:
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
        if "passed to be enacted" in low:
            bump("passed_both")
        if "signed by the governor" in low or re.search(r"chapter \d+ of the acts", low):
            bump("enacted")
        m = re.search(r"(\d+)\s*YEAS?\s*to\s*(\d+)\s*NAYS?\s*\(See YEA and NAY No\. (\d+)\)", act)
        if m:
            roll_calls.append(f"{d} {m.group(1)}-{m.group(2)} (Y&N No. {m.group(3)}): {act.splitlines()[0][:60]}")
        m = re.search(r"Accompanied a new draft, see ([HS]\d+)", act)
        if m:
            terminal, terminal_ref = "superseded_by_redraft", m.group(1)
        m = re.search(r"Accompanied a study order, see ([HS]\d+)", act)
        if m:
            terminal, terminal_ref = "sent_to_study", m.group(1)
        if "no further action taken" not in low:
            last_real = f"{d} {act[:100]}"
    return stage, terminal, terminal_ref, roll_calls, last_real


def main() -> None:
    hist = json.loads((DATA / "histories.json").read_text())
    props = {r["prop_id"]: r for r in csv.DictReader((DATA / "propositions.csv").open())}
    bp = list(csv.DictReader((DATA / "bill_propositions.csv").open()))
    carriers = {}
    for r in bp:
        carriers.setdefault(r["prop_id"], set()).add(r["bill"])

    statuses = {}
    for bn, d in hist.items():
        statuses[bn] = bill_status(d["actions"])
    with (DATA / "bill_fates.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bill", "furthest_stage", "terminal_class", "terminal_ref", "roll_calls", "last_recorded_action", "history_url"])
        for bn in sorted(statuses):
            st = statuses[bn]
            w.writerow([bn, st[0], st[1], st[2], "; ".join(st[3]), st[4],
                        f"https://malegislature.gov/Bills/193/{bn}"])

    # proposition-level: final vehicles are carriers with no successor that
    # also carries the proposition
    successor = {}
    for bn, d in hist.items():
        for a in d["actions"]:
            m = re.search(r"Accompanied a new draft, see ([HS]\d+)", a["Action"])
            if m:
                successor[bn] = m.group(1)

    order = {s: i for i, s in enumerate(STAGES)}
    out = []
    for pid, bills in sorted(carriers.items()):
        finals = set()
        for b in bills:
            succ = successor.get(b)
            if succ and succ in bills:
                continue  # superseded by a vehicle that still carries it
            finals.add(b)
        # fate precedence across final vehicles: enacted > rejected-by-vote >
        # sent_to_study > died-no-action > dropped-in-consolidation
        terms = {b: statuses[b][1] for b in finals}
        stage = max((statuses[b][0] for b in finals), key=lambda s: order[s])
        best = max(finals, key=lambda b: order[statuses[b][0]])
        dropped = sorted(b for b in bills if successor.get(b) and successor[b] not in bills)
        all_dropped = all(t == "superseded_by_redraft" for t in terms.values())
        if any(statuses[b][0] == "enacted" for b in finals):
            fate = "enacted_as_filed"
            detail = "enacted"
        elif "sent_to_study" in terms.values():
            sb = next(b for b in finals if terms[b] == "sent_to_study")
            fate = "sent_to_study"
            detail = (f"final vehicle {sb} accompanied study order {statuses[sb][2]}; "
                      "no public explanation of substance")
        elif "died_no_further_action" in terms.values():
            fate = "died_no_recorded_action"
            detail = f"final vehicle {best} ended with no further action; no public explanation"
        elif all_dropped:
            fate = "died_no_recorded_action"
            detail = (f"dropped in consolidation: {','.join(dropped)} superseded by "
                      f"{','.join(sorted({successor[b] for b in dropped}))} which does not carry "
                      "this proposition; no public explanation")
        else:
            fate = "indeterminate"
            detail = "terminal record unclear"
        if dropped and not all_dropped:
            detail += f"; also dropped in consolidation from {','.join(dropped)} (no public explanation)"
        out.append({
            "prop_id": pid,
            "slug": props[pid]["slug"],
            "fate": fate,
            "furthest_stage": stage,
            "dropped_in_consolidation": "yes" if dropped else "no",
            "final_vehicles": ";".join(sorted(finals)),
            "all_vehicles": ";".join(sorted(bills)),
            "roll_calls": "; ".join(statuses[best][3]),
            "detail": detail,
            "citation": f"https://malegislature.gov/Bills/193/{best}",
        })
    with (DATA / "proposition_fates.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    # enacted-vehicle sweep over all session laws
    probe_rows = []
    for year in (2023, 2024):
        laws = fetchlib.get_json(f"{API}/SessionLaws/{year}")
        for law in laws:
            plain = re.sub(r"<[^>]+>", " ", law.get("ChapterText") or "")
            plain = re.sub(r"\s+", " ", plain)
            low = plain.lower()
            for fam, phrases in PROBES.items():
                for ph in phrases:
                    for m in re.finditer(re.escape(ph), low):
                        probe_rows.append({
                            "family": fam, "phrase": ph, "year": year,
                            "chapter": law["ChapterNumber"],
                            "title": (law.get("Title") or "")[:80],
                            "snippet": plain[max(0, m.start() - 100): m.end() + 150],
                            "url": f"https://malegislature.gov/Laws/SessionLaws/Acts/{year}/Chapter{law['ChapterNumber']}",
                        })
                        break  # one hit per phrase per chapter
    with (DATA / "enacted_probe.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["family", "phrase", "year", "chapter", "title", "snippet", "url"])
        w.writeheader()
        w.writerows(probe_rows)

    from collections import Counter
    print("bill terminal classes:", Counter(s[1] for s in statuses.values()))
    print("bill furthest stages:", Counter(s[0] for s in statuses.values()))
    print("prop fates:", Counter(r["fate"] for r in out))
    print("prop furthest stages:", Counter(r["furthest_stage"] for r in out))
    print(f"enacted-vehicle probe hits: {len(probe_rows)} (review data/enacted_probe.csv)")


if __name__ == "__main__":
    main()
