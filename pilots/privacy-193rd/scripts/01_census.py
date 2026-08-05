#!/usr/bin/env python3
"""Goal 1, step 1: build the candidate census for consumer data privacy,
193rd General Court (2023-2024).

Inputs (all fetched through the cache in fetchlib):
  - /api/GeneralCourts/193/Documents  (all 10,156 filed documents, titles)
  - /api/GeneralCourts/193/Committees and each committee's detail
    (reported-out document lists, used as a title-independent recall net)

Outputs:
  - data/documents_193.json      normalized document list
  - data/committees_193.json     committee code -> name, reported-out bills
  - data/census_candidates.csv   every candidate with match reasons

Candidate rules (cast wide; inclusion decisions happen later, documented in
the codebook):
  - DOMAIN title terms: privacy, personal information/data, biometric, data
    broker, consumer data, location data/shield, surveillance, facial
    recognition, genetic information/privacy, social media, tracking,
    wiretap/interception, data/security breach, identity theft, cybersecurity
  - BROAD title terms (full text fetched and scanned by 02_textscan.py):
    information, data, electronic, digital, internet, online, technology,
    telecommunications, consumer protection, artificial intelligence,
    algorithm
  - COMMITTEE net: every document reported out of J33 (Advanced Information
    Technology, the Internet and Cybersecurity)
"""

import csv
import json
import re
from pathlib import Path

import fetchlib

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"
API = "https://malegislature.gov/api"

DOMAIN_TERMS = {
    "privacy": r"\bprivacy\b",
    "personal_information": r"personal (information|data)",
    "data_privacy_protection": r"data (privacy|protection)",
    "biometric": r"\bbiometric",
    "data_broker": r"data broker",
    "consumer_data": r"consumer data",
    "location_data": r"location (shield|data|information|privacy)|\bgeofen",
    "surveillance": r"surveillance",
    "facial_recognition": r"facial recognition|face recognition",
    "genetic": r"\bgenetic (information|privacy|data|test)|\bdna\b",
    "social_media": r"social media",
    "cybersecurity": r"cyber ?security",
    "data_security_breach": r"(security|data) breach|breach of security|data security",
    "identity_theft": r"identity (theft|fraud)",
    "tracking": r"\btracking\b|\btracker",
    "wiretap_interception": r"wiretap|interception|eavesdrop",
}

BROAD_TERMS = {
    "information": r"\binformation\b",
    "data": r"\bdata\b",
    "electronic": r"\belectronic\b",
    "digital": r"\bdigital\b",
    "internet": r"\binternet\b",
    "online": r"\bonline\b",
    "technology": r"\btechnology\b",
    "telecommunications": r"\btelecommunications\b",
    "consumer_protection": r"\bconsumer protection\b",
    "artificial_intelligence": r"artificial intelligence|algorithm",
}

COMMITTEE_NET = ["J33"]


def matches(title: str, terms: dict) -> list[str]:
    t = title.lower()
    return [k for k, rx in terms.items() if re.search(rx, t)]


def main() -> None:
    DATA.mkdir(exist_ok=True)

    # Seed the cache from exploratory probe fetches so nothing is re-fetched.
    probes = PILOT / "raw" / "probe"
    fetchlib.seed(
        f"{API}/GeneralCourts/193/Documents?fields=BillNumber,Title,LegislationTypeName",
        probes / "api_docs_fields.json",
    )
    fetchlib.seed(f"{API}/GeneralCourts/193/Committees", probes / "api_committees.json")
    fetchlib.seed(f"{API}/GeneralCourts/193/Committees/J33", probes / "api_J33.json")
    fetchlib.seed(f"{API}/GeneralCourts/193/Documents/H83", probes / "api_H83.json")
    fetchlib.seed(
        f"{API}/GeneralCourts/193/Documents/H83/DocumentHistoryActions",
        probes / "api_H83_history.json",
    )

    docs = fetchlib.get_json(
        f"{API}/GeneralCourts/193/Documents?fields=BillNumber,Title,LegislationTypeName"
    )
    norm = [
        {
            "BillNumber": d.get("BillNumber"),
            "DocketNumber": d.get("DocketNumber"),
            "Title": (d.get("Title") or "").strip(),
            "IsDocketBookOnly": d.get("IsDocketBookOnly"),
            "PrimarySponsor": (d.get("PrimarySponsor") or {}).get("Name"),
        }
        for d in docs
    ]
    (DATA / "documents_193.json").write_text(json.dumps(norm, indent=1))
    print(f"{len(norm)} documents in 193rd General Court")

    committees = fetchlib.get_json(f"{API}/GeneralCourts/193/Committees")
    comm_out = {}
    for c in committees:
        code = c["CommitteeCode"]
        detail = fetchlib.get_json(f"{API}/GeneralCourts/193/Committees/{code}")
        comm_out[code] = {
            "FullName": detail.get("FullName"),
            "Branch": detail.get("Branch"),
            "ReportedOutDocuments": [
                {"BillNumber": r.get("BillNumber"), "Title": (r.get("Title") or "").strip()}
                for r in detail.get("ReportedOutDocuments") or []
            ],
            "DocumentsBeforeCommittee": [
                {"BillNumber": r.get("BillNumber"), "Title": (r.get("Title") or "").strip()}
                for r in detail.get("DocumentsBeforeCommittee") or []
            ],
        }
        print(f"  {code}: {len(comm_out[code]['ReportedOutDocuments'])} reported out")
    (DATA / "committees_193.json").write_text(json.dumps(comm_out, indent=1))

    net_bills = {}
    for code in COMMITTEE_NET:
        for r in comm_out[code]["ReportedOutDocuments"] + comm_out[code]["DocumentsBeforeCommittee"]:
            if r["BillNumber"]:
                net_bills.setdefault(r["BillNumber"], set()).add(code)

    rows = []
    seen = set()
    for d in norm:
        dom = matches(d["Title"], DOMAIN_TERMS)
        brd = matches(d["Title"], BROAD_TERMS)
        comm = sorted(net_bills.get(d["BillNumber"] or "", []))
        if not (dom or brd or comm):
            continue
        key = d["BillNumber"] or f"docket:{d['DocketNumber']}"
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            {
                "bill_number": d["BillNumber"] or "",
                "docket_number": d["DocketNumber"] or "",
                "title": d["Title"],
                "docket_only": "yes" if d["IsDocketBookOnly"] else "no",
                "primary_sponsor": d["PrimarySponsor"] or "",
                "domain_title_terms": ";".join(dom),
                "broad_title_terms": ";".join(brd),
                "committee_net": ";".join(comm),
                "url": (
                    f"https://malegislature.gov/Bills/193/{d['BillNumber']}"
                    if d["BillNumber"]
                    else ""
                ),
            }
        )

    rows.sort(key=lambda r: (r["domain_title_terms"] == "", r["bill_number"]))
    with (DATA / "census_candidates.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    n_dom = sum(1 for r in rows if r["domain_title_terms"])
    print(f"{len(rows)} candidates ({n_dom} matched domain terms in title)")


if __name__ == "__main__":
    main()
