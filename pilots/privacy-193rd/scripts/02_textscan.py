#!/usr/bin/env python3
"""Goal 1, step 2: fetch full text of every census candidate and scan it for
consumer-data-privacy terms.

Reads data/census_candidates.csv, fetches each bill's API document (cached),
and writes data/text_scan.csv with per-term hit counts and a context snippet
for the strongest match. Bills whose titles matched only BROAD terms are
confirmed or dropped based on this scan; bills whose titles matched DOMAIN
terms keep their text evidence for the codebook.
"""

import csv

import csvutil
import re
from pathlib import Path

import fetchlib
import textsim

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"
API = "https://malegislature.gov/api"

# Text-level domain terms: tighter than the title net, aimed at consumer data
# privacy specifically.
TEXT_TERMS = {
    # widened 2026-08-05 (third-pass review finding 1): the original pattern
    # missed "personal identifying information" (e.g. 2024 c.363)
    # widened 2026-08-07 (eighth-pass review finding 7): "individually
    # identifying information" (H3524) matched none of the earlier forms
    "personal_information": r"personal(?:ly)?(?: identif(?:iable|ying))? (?:information|data)|identif(?:iable|ying) personal information|individually identif(?:iable|ying) (?:information|data)",
    "consumer_privacy": r"consumer['s]{0,2}\s+(data\s+)?privacy|privacy of consumers",
    "data_privacy": r"data privacy|information privacy|privacy protection",
    "data_broker": r"data broker",
    "biometric": r"biometric",
    "geolocation": r"geolocation|location (information|data)|location shield|geofen",
    "facial_recognition": r"facial recognition|face recognition|faceprint",
    "genetic_privacy": r"genetic (information|data|privacy|test)",
    "browsing_history": r"browsing history|internet history|search history",
    "sale_of_data": r"(sale|sell|selling|sold) [^.]{0,60}(personal|consumer|location|health) (information|data)",
    "opt_out_privacy": r"opt[ -]?out [^.]{0,60}(sale|collection|processing|targeted advertising)",
    "data_protection": r"data protection",
    "security_breach": r"(security|data) breach|breach of security",
    "surveillance": r"surveillance",
    "wiretap_interception": r"wiretap|intercept(ion|ing)? of (wire|oral|electronic)",
    "electronic_monitoring": r"electronic(ally)? monitor",
    "right_to_privacy": r"right (to|of) privacy",
    "privacy_generic": r"privac(y|ies)",
    # widened 2026-08-05 (fourth-pass review finding 1): confidentiality,
    # nondisclosure, and public-record-exclusion language
    "record_nondisclosure": r"shall not be (?:a )?public record|not be deemed (?:a )?public record|(?:are|is) not (?:a )?public records?|not be open to (?:the )?public inspection|exempt(?:ed)? from (?:the )?(?:provisions of )?(?:chapter 66|section 10 of chapter 66|the public records law)|shall (?:be|remain) confidential|shall not be (?:disclosed|made public|published|released)|shall be kept confidential|may not be compelled to disclose|not (?:be )?subject to (?:public )?disclosure",
}


def scan_terms(text: str, before: int = 120, after: int = 120) -> tuple[dict, str]:
    """Apply TEXT_TERMS to text; return ({term: hit_count}, snippet).

    The single implementation of the domain term scan, shared by the filed
    side (this script, 01b_full_corpus_screen.py) and the enacted side
    (03_sessionlaws.py, 03b_acts_index.py) so the four cannot drift. The
    snippet surrounds the first match of the first term that hits, cut from
    `text` as given; callers format the hit counts themselves because they
    differ on ordering.
    """
    low = text.lower()
    hits = {}
    snippet = ""
    for k, rx in TEXT_TERMS.items():
        found = list(re.finditer(rx, low))
        if found:
            hits[k] = len(found)
            if not snippet:
                m = found[0]
                snippet = text[max(0, m.start() - before): m.end() + after].strip()
    return hits, snippet


def main() -> None:
    rows = list(csv.DictReader((DATA / "census_candidates.csv").open()))
    out = []
    n = sum(1 for r in rows if r["bill_number"])
    done = 0
    for r in rows:
        bn = r["bill_number"]
        if not bn:
            out.append({**base(r), "fetch_status": "docket_only_no_text"})
            continue
        done += 1
        try:
            doc = fetchlib.get_json(f"{API}/GeneralCourts/193/Documents/{bn}")
        except Exception as e:
            out.append({**base(r), "fetch_status": f"error: {e}"})
            print(f"  {bn}: ERROR {e}")
            continue
        text = (doc.get("DocumentText") or "")
        plain = re.sub(r"<[^>]+>", " ", text)
        plain = re.sub(r"\s+", " ", plain)
        # Eighth-pass review: this scan stopped at the API text while
        # 01b_full_corpus_screen.py already fell back to recovered PDF text, so
        # seven candidates whose API text is empty reached auto_decision() with
        # NO evidence and were excluded as EX-ADJACENT on that emptiness.
        # H4844 (geolocation:38, a core location-privacy bill) was in the
        # census only because a hand-written OVERRIDE rescued it. Both scans
        # now read the same best-available official text.
        if len(plain.strip()) < 50:
            recovered = textsim.full_text(bn)
            if recovered:
                plain = recovered
        hits, snippet = scan_terms(plain)
        out.append(
            {
                **base(r),
                "fetch_status": "ok",
                "legislation_type": doc.get("LegislationTypeName") or "",
                "text_chars": len(plain),
                "text_terms": ";".join(f"{k}:{v}" for k, v in hits.items()),
                "snippet": snippet,
            }
        )
        if done % 25 == 0:
            print(f"  {done}/{n} scanned")

    fields = [
        "bill_number", "title", "domain_title_terms", "broad_title_terms",
        "committee_net", "fetch_status", "legislation_type", "text_chars",
        "text_terms", "snippet",
    ]
    with (DATA / "text_scan.csv").open("w", newline="") as f:
        w = csvutil.dict_writer(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(out)
    print(f"wrote {len(out)} rows to data/text_scan.csv")


def base(r: dict) -> dict:
    return {
        "bill_number": r["bill_number"],
        "title": r["title"],
        "domain_title_terms": r["domain_title_terms"],
        "broad_title_terms": r["broad_title_terms"],
        "committee_net": r["committee_net"],
        "legislation_type": "",
        "text_chars": "",
        "text_terms": "",
        "snippet": "",
    }


if __name__ == "__main__":
    main()
