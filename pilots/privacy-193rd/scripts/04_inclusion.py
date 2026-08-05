#!/usr/bin/env python3
"""Goal 1, step 4: produce an explicit include/exclude decision for every
census candidate, applying the codebook rules to the full-text scan results.

The automatic rule (auto_decision) is deliberately conservative in both
directions; ambiguous cases fall to "review". Final decisions for reviewed
cases are encoded in the OVERRIDES table below - in the script, not in the
data - so the census is reproducible from scratch and every judgment call is
version-controlled and visible in diffs. Reason codes are defined in
memo/codebook.md.

Output: data/census.csv - the reviewed census with decision + reason per row.
"""

import csv

import csvutil
from pathlib import Path

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"

# Text terms that alone establish domain relevance when present.
STRONG_TERMS = {
    "personal_information",
    "consumer_privacy",
    "data_broker",
    "biometric",
    "facial_recognition",
    "genetic_privacy",
    "browsing_history",
    "sale_of_data",
    "opt_out_privacy",
}
# Terms that support relevance but need a domain title term or a strong term.
SUPPORT_TERMS = {
    "data_privacy",
    "geolocation",
    "data_protection",
    "security_breach",
    "surveillance",
    "wiretap_interception",
    "electronic_monitoring",
    "right_to_privacy",
    "privacy_generic",
}

# Final decisions for cases the auto rule left at "review", plus corrections
# where the auto rule is wrong. Filled during census review; every entry
# must carry a reason code from the codebook and a short note.
# bill_number -> (decision, reason_code, note)
OVERRIDES: dict[str, tuple[str, str, str]] = {
    # --- includes: consumer/individual data handling rules confirmed in text
    "H1442": ("include", "IN-TITLE", "911 recording disclosure restriction (gov-held personal info)"),
    "H4323": ("include", "IN-TITLE", "911 caller privacy; same subject as H1442"),
    "S1022": ("include", "IN-TITLE", "911 caller privacy companion"),
    "S194": ("include", "IN-TITLE", "lottery winner identity: public-record disclosure restriction"),
    "S938": ("include", "IN-TITLE", "crime victim compensation records confidentiality"),
    "H1283": ("include", "IN-TEXT", "public higher-ed student information protection"),
    "H4266": ("include", "IN-TEXT", "same title as H1283, later filing"),
    "S844": ("include", "IN-TEXT", "companion of H1283"),
    "H1455": ("include", "IN-TITLE", "tolling data privacy; text is verbatim S209 despite the title"),
    "H1519": ("include", "IN-TEXT", "carrier disclosure of location data for missing persons"),
    "H1572": ("include", "IN-TITLE", "motor vehicle tracking device consent"),
    "H1809": ("include", "IN-TITLE", "motor vehicle electronic tracking prohibition"),
    "H1653": ("include", "IN-TEXT", "warrant standard for stored electronic communications/browsing data"),
    "S27": ("include", "IN-COMMITTEE", "companion of H1653"),
    "H357": ("include", "IN-TITLE", "location shield: geolocation data sale/disclosure limits"),
    "S148": ("include", "IN-TITLE", "location shield companion of H357"),
    "H4844": ("include", "IN-TITLE", "location-information protections; text in attachment (redraft)"),
    "H1893": ("include", "IN-TITLE", "social media account privacy vs educational institutions"),
    "S1368": ("include", "IN-TITLE", "patient identity confidentiality in waiting rooms; marginal"),
    "H80": ("include", "IN-COMMITTEE", "children's internet privacy rights"),
    "S198": ("include", "IN-COMMITTEE", "adds date of birth to c.93H personal information"),
    "H3404": ("include", "IN-TITLE", "driver data privacy protections"),
    "H3434": ("include", "IN-TITLE", "electronic tolling data privacy"),
    "S209": ("include", "IN-TITLE", "electronic tolling driver privacy"),
    "H3831": ("include", "IN-TEXT", "municipal ISP data-minimization duty"),
    "H1986": ("include", "IN-TEXT", "children's social media commission incl. data practices; marginal"),
    "H3863": ("include", "IN-TEXT", "firearm-license personal info release restriction"),
    # H3217 reclassified 2026-08-05 (second-pass review): its two privacy
    # clauses are program-incident components of an energy-program bill.
    # Program-incident data provisions are excluded SYMMETRICALLY (filed and
    # enacted sides) per the codebook's program-incident rule.
    "H3217": ("exclude", "EX-PROGRAM-INCIDENT", "energy-scorecard bill; privacy clauses are program-incident"),
    "H1728": ("include", "IN-TITLE", "facial recognition commission recommendations"),
    "H4359": ("include", "IN-TITLE", "facial recognition; same subject as H1728"),
    "S927": ("include", "IN-TITLE", "facial recognition companion"),
    # H4832 was provisionally included on its surveillance/location-warrant
    # text; full reading plus its official history (new draft of S2483, H1488
    # and H4103, all robotic-device/drone bills) shows a robotic-device
    # regime with no personal-data handling rule, so it is out per the
    # physical-surveillance boundary.
    "H4832": ("exclude", "EX-ADJACENT", "robotic-device regulation; no personal-data handling rule"),
    "H3431": ("include", "IN-TEXT", "ALPR data regulation (retention, access, GPS coordinates)"),
    "S1557": ("include", "IN-TEXT", "police drone data minimization; biometric analysis ban"),
    # --- excludes: false positives of the term net
    "H2814": ("exclude", "EX-FALSEPOS", "biometric refers to gun-lock hardware, not data handling"),
    "H131": ("exclude", "EX-FALSEPOS", "fast-tracking = expediting adoptions"),
    "S1123": ("exclude", "EX-FALSEPOS", "tracking of malpractice case statistics"),
    "S560": ("exclude", "EX-FALSEPOS", "transportation funding reporting"),
    "H2334": ("exclude", "EX-FALSEPOS", "firearm tracing, not personal-data handling"),
    "H1556": ("exclude", "EX-FALSEPOS", "protest buffer at residences; no data provision"),
    "H2792": ("exclude", "EX-FALSEPOS", "biometric/surveillance = physical security of data centers"),
    "S1958": ("exclude", "EX-FALSEPOS", "companion of H2792"),
    "H4456": ("exclude", "EX-FALSEPOS", "incidental reference to complying with privacy laws"),
    "H3780": ("exclude", "EX-FALSEPOS", "ISP privacy policies as one reporting item"),
    # --- excludes: adjacent domains per codebook boundary
    "H1722": ("exclude", "EX-ADJACENT", "wiretap/interception statute (criminal procedure boundary)"),
    "H1786": ("exclude", "EX-ADJACENT", "wiretap modernization (criminal procedure boundary)"),
    "S1075": ("exclude", "EX-ADJACENT", "wiretap statutes update"),
    "S1093": ("exclude", "EX-ADJACENT", "wiretap defense for police recordings"),
    "S1128": ("exclude", "EX-ADJACENT", "wiretap statutes update"),
    "S1141": ("exclude", "EX-ADJACENT", "wiretap warrant length"),
    "H73": ("exclude", "EX-ADJACENT", "interception of wire and oral communications"),
    "H1760": ("exclude", "EX-ADJACENT", "forensic DNA (criminal procedure)"),
    "H4836": ("exclude", "EX-ADJACENT", "forensic DNA (criminal procedure)"),
    "S1060": ("exclude", "EX-ADJACENT", "forensic DNA (criminal procedure)"),
    "H2336": ("exclude", "EX-ADJACENT", "state DNA database expansion"),
    "H2342": ("exclude", "EX-ADJACENT", "lawfully owed DNA collection"),
    "S1554": ("exclude", "EX-ADJACENT", "lawfully owed DNA collection"),
    "S1528": ("exclude", "EX-ADJACENT", "familial DNA searching"),
    "S1587": ("exclude", "EX-ADJACENT", "state DNA database expansion"),
    "S961": ("exclude", "EX-ADJACENT", "identity theft criminal penalties; no data-handling rule"),
    "H1672": ("exclude", "EX-ADJACENT", "physical/video privacy of property"),
    "H1488": ("exclude", "EX-ADJACENT", "drone peeping offense; physical surveillance"),
    "H3429": ("exclude", "EX-ADJACENT", "drone surveillance offense; physical surveillance"),
    "H3256": ("exclude", "EX-ADJACENT", "drone airspace regulation"),
    "H3325": ("exclude", "EX-ADJACENT", "drone operation safety"),
    "S2308": ("exclude", "EX-ADJACENT", "drone operation regulation"),
    "S877": ("exclude", "EX-ADJACENT", "credit reporting in housing (consumer-finance domain)"),
    "H1308": ("exclude", "EX-ADJACENT", "credit reporting in housing (consumer-finance domain)"),
    "S1144": ("exclude", "EX-ADJACENT", "employer use of credit reports (consumer-finance domain)"),
    "S142": ("exclude", "EX-ADJACENT", "right to repair: data access, not privacy protection"),
    "H360": ("exclude", "EX-ADJACENT", "right to repair"),
    "S2478": ("exclude", "EX-ADJACENT", "right to repair"),
    "H290": ("exclude", "EX-ADJACENT", "right to repair motor vehicle data law"),
    "H329": ("exclude", "EX-ADJACENT", "right to repair disclosure notice"),
    "H1238": ("exclude", "EX-ADJACENT", "health IT integration"),
    "H986": ("exclude", "EX-ADJACENT", "telehealth access"),
    "S655": ("exclude", "EX-ADJACENT", "telehealth access"),
    "H1976": ("exclude", "EX-ADJACENT", "mental health patient rights"),
    "H655": ("exclude", "EX-ADJACENT", "physical dignity/privacy in nursing homes"),
    "H1762": ("exclude", "EX-ADJACENT", "asset forfeiture transparency reporting"),
    "S1111": ("exclude", "EX-ADJACENT", "asset forfeiture transparency reporting"),
    "H1802": ("exclude", "EX-ADJACENT", "juvenile justice statistics"),
    "S931": ("exclude", "EX-ADJACENT", "juvenile justice statistics"),
    "H1862": ("exclude", "EX-ADJACENT", "workforce statistics"),
    "S1187": ("exclude", "EX-ADJACENT", "workforce statistics"),
    "S1567": ("exclude", "EX-ADJACENT", "in-custody monitoring technology study"),
    "S1892": ("exclude", "EX-ADJACENT", "social media excise tax"),
    "H3082": ("exclude", "EX-ADJACENT", "municipal records management"),
    "S2060": ("exclude", "EX-ADJACENT", "municipal records management"),
    "H4802": ("exclude", "EX-ADJACENT", "library study; patron privacy one item of broader scope"),
    "H62": ("exclude", "EX-ADJACENT", "open data standard (government transparency)"),
    "H64": ("exclude", "EX-ADJACENT", "government automated-decision commission (AI governance)"),
    "H4024": ("exclude", "EX-ADJACENT", "government automated-decision commission (AI governance)"),
    "S33": ("exclude", "EX-ADJACENT", "government automated-decision commission (AI governance)"),
    "H77": ("exclude", "EX-ADJACENT", "state IT cloud procurement"),
    "H69": ("exclude", "EX-ADJACENT", "blockchain commission"),
    "S29": ("exclude", "EX-ADJACENT", "blockchain commission"),
    "S31": ("exclude", "EX-ADJACENT", "generative AI regulation without personal-data provisions"),
    "S26": ("exclude", "EX-ADJACENT", "state agency IT modernization"),
    "S32": ("exclude", "EX-ADJACENT", "government cyber incident response"),
    "S36": ("exclude", "EX-ADJACENT", "cybersecurity commission (state systems)"),
    "S2811": ("exclude", "EX-ADJACENT", "state cybersecurity code; references c.93H, does not amend it"),
    "H4406": ("exclude", "EX-ADJACENT", "deepfake task force (content forgery, not personal data)"),
    "H72": ("exclude", "EX-ADJACENT", "deepfake criminal offense"),
    "H3818": ("exclude", "EX-ADJACENT", "online exploitation criminal offense"),
    "H81": ("exclude", "EX-ADJACENT", "broadband in public housing"),
    # --- excludes: procedural filings, not legislation
    "H4299": ("exclude", "EX-PROCEDURAL", "committee extension order"),
    "H4536": ("exclude", "EX-PROCEDURAL", "committee extension order"),
}

# Bills admitted through the enacted-vehicle feedback loop (codebook,
# "Census universe" and reason code IN-ENACTED-FEEDBACK): 2024 c.118's
# OriginBill is H4744; its official lineage (05c_link_targets.py) runs
# H1745/S1012/S1139 (+ coercive-control bills, which stay excluded) ->
# H4115 -> H4241 -> H4744. Each carries the NDII disclosure-restriction
# mechanism, in-domain under the revised interpersonal-disclosure boundary.
# bill -> (title, reason_code, note)
ADDITIONS = {
    "H1745": ("An Act relative to transmitting indecent visual depictions by teens and the unlawful distribution of explicit images", "IN-ENACTED-FEEDBACK", "NDII offense, SECTION 5"),
    "S1012": ("An Act relative to transmitting indecent visual depictions by teens and the unlawful distribution of explicit images", "IN-ENACTED-FEEDBACK", "NDII offense, SECTION 5"),
    "S1139": ("An Act relative to transmitting indecent visual depictions by teens and the unlawful distribution of explicit images", "IN-ENACTED-FEEDBACK", "NDII offense, SECTION 5"),
    "H4115": ("An Act to prevent abuse and exploitation", "IN-ENACTED-FEEDBACK", "Judiciary redraft carrying the NDII offense, SECTION 6"),
    "H4241": ("An Act to prevent abuse and exploitation", "IN-ENACTED-FEEDBACK", "House-engrossed vehicle of the NDII offense"),
    "H4744": ("An Act to prevent abuse and exploitation", "IN-ENACTED-FEEDBACK", "conference vehicle; enacted as 2024 c.118 (NDII at s.6)"),
    # Eviction-record sealing (HOMES) lineage: enacted as 2024 c.150 ss.28,52
    # inside the Affordable Homes Act; filed parents found by the c.150
    # adjudication (see data/enacted_adjudication.csv).
    "H1690": ("An Act promoting housing opportunity and mobility through eviction sealing (HOMES)", "IN-ENACTED-FEEDBACK", "eviction-record sealing regime"),
    "S956": ("An Act promoting housing opportunity and mobility through eviction sealing (HOMES)", "IN-ENACTED-FEEDBACK", "companion of H1690"),
    "H4356": ("An Act promoting housing opportunity and mobility through eviction sealing (HOMES)", "IN-ENACTED-FEEDBACK", "Judiciary redraft of the HOMES bills"),
    # Notary personal-information restriction: enacted as 2023 c.2 s.33
    # (new c.222 s.29); filed companions carry the identical restriction.
    "H1525": ("An Act modernizing notary services", "IN-ENACTED-FEEDBACK", "notary personal-info use/sale restriction"),
    "S943": ("An Act modernizing notary services", "IN-ENACTED-FEEDBACK", "companion of H1525"),
    # Demographic-data collection standard: enacted as 2023 c.28 s.7 (c.6A s.109)
    "H3003": ("An Act ensuring equitable representation in the Commonwealth", "IN-ENACTED-FEEDBACK", "agency demographic-data collection with PII confidentiality"),
    # SFI personal-info withholding: enacted (expanded) as 2024 c.248 s.27
    "H2991": ("An Act relative to access to statements of financial interest", "IN-ENACTED-FEEDBACK", "SFI home-address withholding; enacted version broader"),
    # Enacted origin vehicles of in-domain provisions (chapter OriginBill
    # records; third-pass review finding 2). Budget outside-sections are
    # census units per the brief; the vehicle carries them.
    "H58": ("An Act making appropriations for fiscal year 2023 (supplemental)", "IN-ENACTED-VEHICLE", "enacted as 2023 c.2; carries the notary provision (s.33)"),
    "H4040": ("An Act making appropriations for fiscal year 2024 (GAA)", "IN-ENACTED-VEHICLE", "enacted as 2023 c.28; carries the demographic-data standard (s.7)"),
    "H4977": ("An Act relative to the Affordable Homes Act", "IN-ENACTED-VEHICLE", "enacted as 2024 c.150; carries eviction sealing (ss.28,52)"),
    "H5077": ("An Act making appropriations for fiscal year 2024 (supplemental-closeout)", "IN-ENACTED-VEHICLE", "enacted as 2024 c.248; carries the SFI withholding expansion (s.27)"),
    "H4799": ("An Act making appropriations for fiscal year 2024 (closeout supplemental)", "IN-ENACTED-VEHICLE", "enacted as 2024 c.206; carries the TNC trip-data regime (s.15)"),
    "S2884": ("An Act relative to bus lane enforcement", "IN-ENACTED-VEHICLE", "enacted as 2024 c.363; bus-camera data rules (found by the widened enacted-side scan)"),
}


def parse_terms(s: str) -> dict[str, int]:
    out = {}
    for part in (s or "").split(";"):
        if ":" in part:
            k, v = part.rsplit(":", 1)
            out[k] = int(v)
    return out


def auto_decision(row: dict) -> tuple[str, str]:
    terms = parse_terms(row["text_terms"])
    strong = {k: v for k, v in terms.items() if k in STRONG_TERMS}
    has_title = bool(row["domain_title_terms"])
    if row["fetch_status"] == "docket_only_no_text":
        return "exclude", "EX-NOBILL"
    if strong and sum(strong.values()) >= 2:
        if has_title:
            return "include", "IN-TITLE"
        if row["committee_net"]:
            return "include", "IN-COMMITTEE"
        return "include", "IN-TEXT"
    if not terms and not has_title:
        return "exclude", "EX-ADJACENT"
    return "review", ""


# Verdicts for full-corpus-screen hits with no prior census decision
# (third-pass review finding 3), from five documented triage reading passes
# over the complete corpus. Stored in scripts/corpus_triage_verdicts.csv
# (bill, verdict, reason, mechanisms); 04 fails if any corpus hit lacks a
# verdict, so the census is an enforced-complete full-text screen.
def _load_triage():
    out = {}
    path = Path(__file__).resolve().parent / "corpus_triage_verdicts.csv"
    for r in csv.DictReader(path.open()):
        if r["verdict"] == "IN-CORE":
            out[r["bill"]] = ("include", "IN-CORPUS-SCREEN", r["reason"])
        else:
            out[r["bill"]] = ("exclude", r["verdict"], r["reason"])
    return out


TRIAGE: dict[str, tuple[str, str, str]] = _load_triage()


def main() -> None:
    rows = list(csv.DictReader((DATA / "text_scan.csv").open()))
    out = []
    counts = {}
    for r in rows:
        dec, reason = auto_decision(r)
        note = "auto"
        key = r["bill_number"] or r["title"]
        if key in OVERRIDES:
            dec, reason, note = OVERRIDES[key]
        out.append({**r, "decision": dec, "reason": reason, "note": note})
        counts[dec] = counts.get(dec, 0) + 1
    corpus_path = DATA / "corpus_scan.csv"
    if corpus_path.exists():
        already = {r["bill_number"] for r in out if r.get("bill_number")}
        missing = []
        for r in csv.DictReader(corpus_path.open()):
            bn = r["bill"]
            if bn in already or bn in ADDITIONS:
                continue  # decided by the legacy candidate path or ADDITIONS
            if bn not in TRIAGE:
                missing.append(bn)
                continue
            dec, reason, note = TRIAGE[bn]
            out.append({
                "bill_number": bn, "title": r["title"], "domain_title_terms": "",
                "broad_title_terms": "", "committee_net": "",
                "fetch_status": "corpus_screen", "legislation_type": "",
                "text_chars": "", "text_terms": r["text_terms"],
                "snippet": r["snippet"],
                "decision": dec, "reason": reason, "note": note,
            })
            counts[dec] = counts.get(dec, 0) + 1
        if missing:
            with (DATA / "corpus_triage_needed.csv").open("w", newline="") as f:
                w = csvutil.writer(f)
                w.writerow(["bill"])
                for bn in sorted(missing):
                    w.writerow([bn])
            raise SystemExit(
                f"corpus-screen hits without triage verdicts: {len(missing)} "
                f"(worklist written to data/corpus_triage_needed.csv): {sorted(missing)[:10]}")
    for bn, (title, reason, note) in ADDITIONS.items():
        out.append({
            "bill_number": bn, "title": title, "domain_title_terms": "",
            "broad_title_terms": "", "committee_net": "",
            "fetch_status": "added_by_feedback", "legislation_type": "Bill",
            "text_chars": "", "text_terms": "", "snippet": "",
            "decision": "include", "reason": reason, "note": note,
        })
        counts["include"] = counts.get("include", 0) + 1
    with (DATA / "census.csv").open("w", newline="") as f:
        w = csvutil.dict_writer(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(counts)


if __name__ == "__main__":
    main()
