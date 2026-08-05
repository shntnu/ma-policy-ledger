#!/usr/bin/env python3
"""Goal 4: classify the fate of every bill and every proposition.

Order of operations (review finding 2): the enacted-vehicle sweep runs
FIRST; its reviewed verdicts live in ADJUDICATIONS (data-as-code), and the
enacted origin vehicles named there are census carriers of the propositions
their chapters contain, so enactment flows structurally into fate
assignment.

enacted_as_filed vs enacted_other_vehicle: a proposition is enacted AS FILED
when the enacted carrier is connected to the proposition's filed lineage by
official successor records (redraft/substitution/conference), or is the
proposition's only carrier (outside-section-born ideas). It is enacted
THROUGH ANOTHER VEHICLE when its filed carriers have no official chain to
the enacted vehicle (absorption established by text adjudication instead).

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

# Enactment is established structurally: enacted origin vehicles are census
# carriers of the propositions their chapters contain (scripts/atoms.py),
# so the fate logic below needs no side table. ADJUDICATIONS remains the
# row-level verdict record for every flagged chapter.
# Row-level adjudication of every chapter flagged by the probe or the
# session-law scan (second-pass review finding 8). Verdicts:
#   IN-CORE            in-domain under the primary-object test; propositions
#                      and filed lineage admitted
#   EX-PROGRAM-INCIDENT confidentiality/data clause incident to a program
#                      the provision creates (symmetric rule, see codebook)
#   EX-ADJACENT        adjacent domain per codebook boundary
#   EX-FALSEPOS        matched term used in a non-domain sense
# (year, chapter) -> list of (sections, verdict, note)
ADJUDICATIONS = {
    (2023, "2"): [
        ("s.33 (new c.222 s.29)", "IN-CORE", "notary personal-info restriction (P-291); filed parents H1525/S943; enacted vehicle H58"),
        ("s.33 (c.222 s.28: AV-recording retention, access limits, security standards)", "EX-PROGRAM-INCIDENT", "recordkeeping/access mechanics incident to the remote-notarization program; s.29's use/sale ban is the data-primary rule"),
        ("ss.23, 31-32 (definitions, journal rules)", "EX-PROGRAM-INCIDENT", "notarial act-integrity recordkeeping; identity-proofing definitions attach"),
        ("ss.8-11 (sports-wagering license CORI/fingerprints)", "EX-ADJACENT", "licensing background checks (criminal-records mechanism)"),
        ("appropriation line items", "EX-FALSEPOS", "lottery/victim-comp/biometric term matches in budget lines"),
    ],
    (2023, "10"): [("ballot-order lottery", "EX-FALSEPOS", "town-clerk candidate-order drawing; no personal data")],
    (2024, "139"): [("IT bond act line items", "EX-FALSEPOS", "'digitization' = municipal records digitization funding; no handling rule")],
    (2024, "135"): [("DCJIS firearms dashboard", "EX-FALSEPOS", "publishes non-personally-identifying aggregate statistics; no handling rule")],
    (2023, "28"): [
        ("s.7 (new c.6A s.109)", "IN-CORE", "demographic-data collection standard (P-297) and PII confidentiality (P-298); filed parent H3003; enacted vehicle H4040"),
        ("s.2 items 3000-1000, 7010-0005, 4120-1000, 4800-0015, 7004-0099/0108/9024 (c.66A overrides, SSN eligibility, fair-hearing redaction)", "EX-PROGRAM-INCIDENT", "recurring benefit/education program-administration data provisos"),
        ("s.43 (c.111 s.24O maternal mortality committee)", "EX-PROGRAM-INCIDENT", "confidentiality incident to the review committee (same verdict as 2024 c.186 s.15)"),
        ("s.2 item 7061-9611 and other line items", "EX-FALSEPOS", "'alpr'='malpractice'; student-data pilot proviso 'to the extent allowed by law' creates no new rule"),
    ],
    (2023, "77"): [
        ("s.5 (c.19A s.4G(c) CDC-worker list)", "EX-PROGRAM-INCIDENT", "worker-list disclosure/opt-out incident to the workforce-council program"),
        ("supplemental budget line items", "EX-FALSEPOS", "term matches in appropriation text"),
    ],
    (2024, "140"): [
        ("s.2 items 3000-1000, 7010-0005, 4120-1000, 4800-0015, 7004-0099/0108/9024", "EX-PROGRAM-INCIDENT", "same recurring program-administration data provisos as 2023 c.28 (FY25 EEC version adds 'investigations')"),
        ("s.7 (c.10 s.24 online lottery data rules)", "EX-PROGRAM-INCIDENT", "player-data nondisclosure, anonymized tracking, ad-targeting ban incident to the online-lottery program; kinship with P-254 (S194 winner anonymity) noted - different target (player transaction data vs winner identity), and winner-publicity carve-outs retained"),
        ("s.22 (tuition-equity information protection)", "EX-PROGRAM-INCIDENT", "disclosure-protection clause incident to tuition-eligibility administration; partly declaratory of existing exemptions"),
        ("other line items", "EX-FALSEPOS", "term matches without new handling rules"),
    ],
    (2024, "206"): [
        ("s.15 (c.159A1/2 s.12 TNC trip-data regime)", "IN-CORE", "trip-data reporting mandate (P-303) and confidentiality rules (P-304); outside section carried by enacted vehicle H4799; no standalone filed antecedent"),
        ("collective bargaining agreement funding", "EX-FALSEPOS", "lottery commission labor agreement"),
    ],
    (2024, "248"): [
        ("s.27 (c.268B s.3 SFI withholding expansion)", "IN-CORE", "SFI withholding (P-294); filed parent H2991; enacted vehicle H5077"),
        ("ss.17-18 (interagency data sharing)", "EX-PROGRAM-INCIDENT", "c.66A-override sharing authorizations for student/incarcerated-person data incident to special-education administration"),
        ("supplemental budget line items", "EX-FALSEPOS", "term matches in appropriation text"),
    ],
    (2024, "118"): [
        ("s.6 (c.265 s.43A(b))", "IN-CORE", "NDII distribution offense (P-266); court-record confidentiality (P-280)"),
        ("s.4 (c.209A coercive control)", "EX-ADJACENT", "abuse-prevention-order law incl. threatening to publish sensitive personal information"),
        ("ss.2-3, 5, 7-9 (penalties, diversion, education)", "EX-ADJACENT", "criminal penalties, juvenile diversion (s.7's de-identified reporting attaches to diversion program)"),
    ],
    (2024, "150"): [
        ("ss.28, 52 (new c.239 s.16; c.93 s.52(a)(7))", "IN-CORE", "eviction-sealing regime (P-295) and CRA duties (P-296); HOMES lineage; enacted vehicle H4977"),
        ("ss.2A, 35, 121", "EX-FALSEPOS", "eviction/privacy/sealed-bid term matches without data-handling rules"),
    ],
    (2024, "166"): [
        ("ss.62, 65 (genetic-testing rules)", "EX-ADJACENT", "family-law evidentiary/parentage procedure; no handling rule on genetic information itself"),
        ("s.65 (c.209C s.28B(a)(ix) surrogacy records)", "EX-ADJACENT", "records-availability condition of surrogacy-agreement enforceability (contract formation), confidentiality incident to it; judgment call queued"),
        ("s.65 (c.209C ss.28I, 28O impoundment)", "EX-ADJACENT", "impoundment incident to family-law status proceedings, protecting case papers rather than regulating a data class; contrast c.118 s.43A(b)(5), which protects the very material whose distribution is the offense; judgment call queued"),
    ],
    (2024, "178"): [
        ("s.139 (burn-pit registry)", "EX-PROGRAM-INCIDENT", "confidentiality/purpose limits incident to a registry the section creates"),
        ("s.147 (51A military sharing)", "EX-PROGRAM-INCIDENT", "sharing protocol incident to family-advocacy program coordination"),
        ("s.136 (genetic term)", "EX-FALSEPOS", "discharge-upgrade eligibility criterion"),
    ],
    (2024, "186"): [
        ("ss.15, 16, 21 (mortality reviews, pregnancy-loss data)", "EX-PROGRAM-INCIDENT", "collection/confidentiality rules incident to review programs the sections create"),
    ],
    (2024, "197"): [
        ("assisted-living oversight confidentiality", "EX-PROGRAM-INCIDENT", "inspection-report and business-information confidentiality incident to the licensure program"),
        ("s.17 (LGBTQI+ resident protections)", "EX-ADJACENT", "dignity/anti-discrimination and physical privacy without a data-handling rule"),
    ],
    (2024, "238"): [
        ("s.225 (Parkinson's registry)", "EX-PROGRAM-INCIDENT", "confidentiality/de-identification incident to a registry the section creates"),
        ("s.229 (nurse licensure compact data system)", "EX-PROGRAM-INCIDENT", "PII sharing/expungement rules incident to the compact's licensure system; fingerprint checks are licensure procedure"),
        ("s.224 (public-health reporting de-identification)", "EX-PROGRAM-INCIDENT", "de-identification clause on program reporting"),
        ("ss.112, 214, 249, 297", "EX-FALSEPOS", "hearing-privacy discretion; data-center physical security; ticket fees; election deepfake (adjacent per H72/H4406 precedent)"),
    ],
    (2024, "252"): [
        ("c.150F s.5(A) and related", "EX-PROGRAM-INCIDENT", "driver-record public-records exemption and list-sharing incident to the bargaining board the act creates"),
    ],
    (2024, "363"): [
        ("s.1 (c.4 s.7 cl.26(w)); c.90K s.5", "IN-CORE", "bus-camera records exemption (P-299), litigation limits (P-300), occupant-ID ban (P-301), vendor confidentiality (P-302); enacted vehicle S2884 (found by the widened scan)"),
    ],
    (2024, "343"): [
        ("s.48 (patient-safety data transmission)", "EX-PROGRAM-INCIDENT", "transmission-with-safeguards rule incident to the Lehman center program"),
        ("ss.24, 42, 49, 64", "EX-FALSEPOS", "business/trade-secret regulatory confidentiality, not personal data"),
    ],
    (2024, "389"): [
        ("ss.1, 3", "EX-FALSEPOS", "cybersecurity-insurance definition; insurer financial confidentiality"),
    ],
}


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
    adjudicated = {(r["year"], r["chapter"]) for r in rows} & set()
    for r in rows:
        key = (r["year"], r["chapter"])
        if key in ADJUDICATIONS:
            r["verdict"] = "; ".join(f"{s}: {v}" for s, v, _ in ADJUDICATIONS[key])
        else:
            r["verdict"] = "UNADJUDICATED"
    with (DATA / "enacted_probe.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["family", "phrase", "year", "chapter", "title", "snippet", "verdict", "url"])
        w.writeheader()
        w.writerows(rows)
    with (DATA / "enacted_adjudication.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "chapter", "sections", "verdict", "note", "url"])
        for (year, ch) in sorted(ADJUDICATIONS):
            for sec, verdict, note in ADJUDICATIONS[(year, ch)]:
                w.writerow([year, ch, sec, verdict, note,
                            f"https://malegislature.gov/Laws/SessionLaws/Acts/{year}/Chapter{ch}"])
    un = sorted({(r["year"], r["chapter"]) for r in rows if r["verdict"] == "UNADJUDICATED"})
    if un:
        raise SystemExit(f"unadjudicated probe chapters: {un}")
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
                        r"Reprinted as amended, see ([HS]\d+)",
                        r"Reported \(in part\) by ([HS]\d+)",
                        r"Substituted (?:as a new text )?for ([HS]\d+)",
                        r"^See ([HS]\d+)$",
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

        def chains_to(start, target):
            seen_chain = set()
            b = start
            while b in successor and b not in seen_chain:
                seen_chain.add(b)
                b = successor[b]
                if b == target:
                    return True
            return b == target

        enacted_finals = sorted(b for b in finals if statuses[b][0] == "enacted")
        if enacted_finals:
            fb = enacted_finals[0]
            others = [b for b in bills if b != fb]
            chained = sorted(b for b in others if chains_to(b, fb))
            unchained = sorted(b for b in others if b not in chained)
            if not others or chained:
                fate = "enacted_as_filed"
                detail = f"enacted via {fb}: {statuses[fb][2]}"
                if unchained:
                    detail += (f"; independent filings of the same proposition "
                               f"({','.join(unchained)}) died without an official chain to {fb}")
            else:
                fate = "enacted_other_vehicle"
                detail = (f"enacted via vehicle {fb} ({statuses[fb][2]}); filed carriers "
                          f"{','.join(unchained)} have no official chain to it (absorption "
                          "established by text adjudication, see data/enacted_adjudication.csv "
                          "and the absorbed_into_vehicle links)")
            cite = f"https://malegislature.gov/Bills/193/{fb}"
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
    enacted_props = sorted(r["prop_id"] for r in out if r["fate"].startswith("enacted"))
    print(f"enacted-probe hits: {len(probe_rows)}; enacted propositions: {enacted_props}")


if __name__ == "__main__":
    main()
