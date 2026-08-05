#!/usr/bin/env python3
"""Goal 3: build the link graph.

Explicit links (confidence=verified-official-record), parsed from official
bill histories and the Similar Bills tabs:
  - redraft_of:        "New draft of X, Y and Z" history entries
  - superseded_by:     "Accompanied a new draft, see X"
  - sent_to_study:     "Accompanied a study order, see X"
  - reported_from_part_of: "Reported on a part of X"
  - official_similar:  the malegislature.gov Similar Bills tab

Computed links (confidence=verified-text-comparison), from programmatic
comparison of cached official texts:
  - companion_identical: normalized-text Jaccard similarity >= 0.90
    between two included bills (House/Senate companions and duplicates)

Inferred links (confidence=inferred-needs-review), hand-proposed
proposition-level kinships between DIFFERENT propositions with the same
goal but different mechanisms; every one goes to the verification queue
with a pointer to the side-by-side excerpts in memo/atomization/.

Outputs: data/links.csv, data/verification_queue.csv
"""

import csv
import hashlib
import json
import re
from pathlib import Path

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"
API = "https://malegislature.gov/api"


def bill_text(bn: str) -> str:
    url = f"{API}/GeneralCourts/193/Documents/{bn}"
    p = PILOT / "raw" / "cache" / (hashlib.sha1(url.encode()).hexdigest() + ".bin")
    doc = json.loads(p.read_text(encoding="utf-8-sig"))
    t = re.sub(r"<[^>]+>", " ", doc.get("DocumentText") or "")
    return re.sub(r"\s+", " ", t).lower()


def shingles(text: str, k: int = 8) -> set:
    words = re.findall(r"[a-z0-9]+", text)
    return {" ".join(words[i : i + k]) for i in range(max(1, len(words) - k + 1))}


# Proposition-level kinships: same goal, different mechanism, proposed for
# human review. (prop_a, prop_b, rationale, excerpt_source)
KINSHIPS = [
    ("P-016", "P-042", "Data broker registration: OCABR registry (MDPPA) vs AG registry with central opt-out (MIPSA)", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-042", "P-065", "Data-seller registration: AG privacy registry (MIPSA) vs DOR tax-base registration (S1896)", "memo/atomization/family-mipsa-internet.md"),
    ("P-001", "P-031", "Data minimization: MDPPA duty-of-loyalty purposes vs GDPR-style principles (MIPSA/H1555)", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-004", "P-035", "Sensitive data: strict-necessity bar (MDPPA) vs consent-gate/prohibition (MIPSA/H1555)", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-011", "P-036", "Access/portability rights: MDPPA bundle vs GDPR-style articles", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-011", "P-037", "Deletion right: MDPPA bundle vs GDPR-style erasure", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-011", "P-038", "Correction right: MDPPA bundle vs GDPR-style rectification", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-012", "P-034", "Opt-out of transfers/targeted ads: MDPPA vs MIPSA sale/ads opt-out with universal signal", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-012", "P-053", "Opt-out vs GDPR objection right for direct marketing (H1555)", "memo/atomization/family-mipsa-internet.md"),
    ("P-014", "P-019", "Universal opt-out signals (redraft) vs OCABR centralized opt-out mechanism (filed)", "memo/atomization/family-comprehensive-mdppa.md"),
    ("P-009", "P-040", "Anti-retaliation/nondiscrimination for exercising rights: MDPPA vs MIPSA", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-017", "P-044", "Civil-rights processing ban: MDPPA vs MIPSA", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-018", "P-043", "Algorithmic/risk assessments: MDPPA impact assessments vs MIPSA/H1555 risk assessments-DPIA", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-022", "P-041", "Processor/service-provider contract duties: MDPPA vs GDPR-style", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-023", "P-063", "General private right of action: MDPPA vs H1555 damages remedy", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-024", "P-045", "AG enforcement architecture: MDPPA 93A penalties vs MIPSA exclusive AG with cure", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-024", "P-062", "AG enforcement: MDPPA vs H1555 GDPR-scale administrative fines", "memo/atomization/family-comprehensive-mdppa.md; family-mipsa-internet.md"),
    ("P-046", "P-130", "Breach-limited PRA (MIPSA) vs location-chapter PRA (H357/S148): different scopes, parallel architecture", "memo/atomization/family-mipsa-internet.md; family-location.md"),
    ("P-026", "P-128", "Legal-request transparency reports: MDPPA bi-monthly vs location-chapter annual AG reports", "memo/atomization/family-comprehensive-mdppa.md; family-location.md"),
    ("P-087", "P-128", "Warrant transparency reports: biometric chapter vs location chapter (parallel drafting)", "memo/atomization/family-biometric-breach.md; family-location.md"),
    ("P-125", "P-131", "Warrant gate over location/electronic data: duty on private holders (shield) vs bar on government acquisition (H1653/S27)", "memo/atomization/family-location.md"),
    ("P-128", "P-134", "Warrant reporting: covered entities to AG vs courts to legislature", "memo/atomization/family-location.md"),
    ("P-139", "P-125", "Tension: compelled emergency carrier disclosure (H1519) vs warrant gate on the same holder class (shield bills)", "memo/atomization/family-location.md"),
    ("P-058", "P-097", "Breach notification: H1555 72-hour GDPR mechanism vs c.93H notice modernization", "memo/atomization/family-mipsa-internet.md; family-biometric-breach.md"),
    ("P-057", "P-085", "Security standards: H1555 general measures vs biometric-specific standard", "memo/atomization/family-mipsa-internet.md; family-biometric-breach.md"),
    ("P-091", "P-081", "Biometric protection: 93H breach-law element vs standalone consent regime (different mechanism)", "memo/atomization/family-biometric-breach.md"),
    ("P-068", "P-072", "ISP opt-in consent: private franchised ISPs (S218/H3179) vs public ISP (H3831)", "memo/atomization/family-mipsa-internet.md"),
    ("P-076", "P-131", "Warrant for user data: public-ISP rule vs general stored-records regime", "memo/atomization/family-mipsa-internet.md; family-location.md"),
    ("P-183", "P-171", "Biometric analysis of drone data (S1557) vs LE biometric surveillance ban (FR bills): S1557 cross-references c.6 s.220", "memo/atomization/family-facial-recognition.md"),
    ("P-213", "P-196", "ALPR restrictions: c.90K summary regime (H3404) vs comprehensive c.90J regime (H3431)", "memo/atomization/family-driver-commercial.md; family-facial-recognition.md"),
    ("P-211", "P-194", "120-day retention/destruction: tolling data (H3434/H3404) vs ALPR data at EOPSS (H3431)", "memo/atomization/family-driver-commercial.md; family-facial-recognition.md"),
    ("P-141", "P-162", "Targeted ads to minors: edtech school-data ban vs product-category ban on minor-directed services", "memo/atomization/family-student-education.md"),
    ("P-015", "P-162", "Minors and targeted advertising: comprehensive-bill ban vs H80 product-category ban", "memo/atomization/family-comprehensive-mdppa.md; family-student-education.md"),
    ("P-226", "P-067", "Doxing: general civil action (H1707/S971) vs police-officer criminal posting ban (H1428)", "memo/atomization/family-driver-commercial.md; family-mipsa-internet.md"),
    ("P-238", "P-211", "Retention limits: ad-network 24-month vs tolling 120-day (same mechanism family, different targets)", "memo/atomization/family-driver-commercial.md"),
    ("P-246", "P-124", "Sale bans: consumer health data vs location information", "memo/atomization/family-health-govrecords.md; family-location.md"),
    ("P-035", "P-242", "Sensitive-data opt-in: comprehensive-bill gates vs consumer-health-data chapter", "memo/atomization/family-mipsa-internet.md; family-health-govrecords.md"),
    ("P-234", "P-006", "Sensitive data in advertising: ad-network opt-in (H395) vs MDPPA flat ban", "memo/atomization/family-driver-commercial.md; family-comprehensive-mdppa.md"),
    ("P-265", "P-121", "Care-location consent regime (H4844) is a narrowed variant of the general location-shield consent regime (H357/S148): same mechanism restricted to care-related location data; official lineage runs through budget bill H4496, not the shield bills", "data/h4844_text.txt; memo/atomization/family-location.md"),
]

# Judgment calls and anomalies for the same review queue.
FLAGS = [
    ("H4844", "", "H4844 text not in API or bill page; history says 'Reported on a part of H4496' (FY24 supplemental budget). P-265 pending text verification.", "data/histories.json"),
    ("S2539", "P-101", "Borderline in-domain: insurance/contract protection for breach reporting (SECTION 17).", "memo/atomization/family-biometric-breach.md"),
    ("S2539", "", "Borderline: c.7D s.17(f)(iv) AI training-data consent rulemaking not atomized (delegated rulemaking, not direct law change).", "memo/atomization/family-biometric-breach.md"),
    ("H1455", "", "Title says 'tracking of certain electronic devices' but official text is verbatim S209 (tolling data). Census include stands on the text.", "memo/atomization/family-driver-commercial.md"),
    ("H1555", "", "MIPSA/H1555 GDPR-mechanism propositions merged onto shared IDs (P-031..P-043 subset); merge is analytic, review recommended.", "memo/atomization/family-mipsa-internet.md"),
    ("H3217", "P-221", "Marginal census include: privacy clauses are two sections of an energy-program bill.", "memo/codebook.md"),
    ("S1368", "P-260", "Marginal census include: physical-adjacent confidentiality mechanism.", "memo/codebook.md"),
    ("H1986", "P-165", "Marginal census include: study resolve with data-practice charges.", "memo/codebook.md"),
]


def main() -> None:
    hist = json.loads((DATA / "histories.json").read_text())
    census = {
        r["bill_number"]
        for r in csv.DictReader((DATA / "census.csv").open())
        if r["decision"] == "include"
    }
    links = []

    def add(src, dst, typ, conf, evidence, url):
        links.append({
            "source": src, "target": dst, "link_type": typ, "confidence": conf,
            "evidence": evidence, "evidence_url": url,
        })

    for bn, d in hist.items():
        hurl = f"https://malegislature.gov/Bills/193/{bn}"
        for a in d["actions"]:
            act = a["Action"].strip()
            m = re.match(r"New draft of (.+)", act)
            if m:
                for parent in re.findall(r"[HS]\d+", m.group(1)):
                    add(bn, parent, "redraft_of", "verified-official-record", act, hurl)
            m = re.search(r"Accompanied a new draft, see ([HS]\d+)", act)
            if m:
                add(bn, m.group(1), "superseded_by", "verified-official-record", act, hurl)
            m = re.search(r"Accompanied a study order, see ([HS]\d+)", act)
            if m:
                add(bn, m.group(1), "sent_to_study", "verified-official-record", act, hurl)
            m = re.search(r"Reported on a part of ([HS]\d+)", act)
            if m:
                add(bn, m.group(1), "reported_from_part_of", "verified-official-record", act, hurl)
        for s in d.get("similar", []):
            add(bn, f"{s['general_court']}:{s['bill']}", "official_similar",
                "verified-official-record", "Similar Bills tab",
                f"https://malegislature.gov/Bills/193/{bn}/SimilarBills")

    # companion detection by text similarity among included bills
    texts = {}
    for bn in sorted(census):
        try:
            t = bill_text(bn)
        except FileNotFoundError:
            continue
        if len(t) > 200:
            texts[bn] = shingles(t)
    bills = sorted(texts)
    for i, a in enumerate(bills):
        for b in bills[i + 1:]:
            inter = len(texts[a] & texts[b])
            union = len(texts[a] | texts[b])
            if not union:
                continue
            j = inter / union
            if j >= 0.85:
                typ = "companion_identical"
            elif j >= 0.50:
                typ = "companion_near_identical"
            else:
                continue
            add(a, b, typ, "verified-text-comparison",
                f"normalized 8-gram Jaccard {j:.3f} between official texts",
                f"https://malegislature.gov/Bills/193/{a}")

    for pa, pb, why, src in KINSHIPS:
        add(pa, pb, "proposition_kinship", "inferred-needs-review", why, src)

    with (DATA / "links.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["source", "target", "link_type", "confidence", "evidence", "evidence_url"])
        w.writeheader()
        w.writerows(links)

    queue = [l for l in links if l["confidence"] == "inferred-needs-review"]
    with (DATA / "verification_queue.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_type", "a", "b", "question", "excerpts_at"])
        for l in queue:
            w.writerow(["proposition_kinship", l["source"], l["target"], l["evidence"], l["evidence_url"]])
        for bill, prop, note, src in FLAGS:
            w.writerow(["judgment_flag", bill, prop, note, src])

    from collections import Counter
    print(Counter(l["link_type"] for l in links))
    print(f"{len(links)} links; {len(queue) + len(FLAGS)} verification-queue items")


if __name__ == "__main__":
    main()
