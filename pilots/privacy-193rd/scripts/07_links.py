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

import actions

import csvutil
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
# human review. Each entry carries side-by-side excerpts (verbatim from the
# cached official texts, as recorded in the memo/atomization/ notes).
# (prop_a, prop_b, rationale, excerpt_a, excerpt_b, sources)
K = "memo/atomization"
KINSHIPS = [
    ("P-016", "P-042", "Data broker registration: OCABR registry (MDPPA) vs AG registry with central opt-out (MIPSA)",
     "data brokers shall register with the OCABR in accordance with this subsection",
     "the controller shall register with the attorney general",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-042", "P-065", "Data-seller registration: AG privacy registry (MIPSA) vs DOR tax-base registration (S1896)",
     "the controller shall register with the attorney general",
     "must register with the department of revenue",
     f"{K}/family-mipsa-internet.md"),
    ("P-001", "P-031", "Data minimization: MDPPA duty-of-loyalty purposes vs GDPR-style principles (MIPSA/H1555)",
     "limited to what is reasonably necessary and proportionate to carry out one of the following purposes",
     "adequate, relevant and limited to what is reasonably necessary in relation to the purposes",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-004", "P-035", "Sensitive data: strict-necessity bar (MDPPA) vs consent-gate/prohibition (MIPSA/H1555)",
     "except where such collection or processing is strictly necessary to provide or maintain a specific product or service",
     "shall not otherwise process an individual's sensitive information without first obtaining the consent",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-271", "P-275", "Access right: MDPPA access (bundle section) vs GDPR-style access article",
     "access... correct any verifiable substantial inaccuracy... delete covered data... export to the individual",
     "the specific pieces of personal information that the controller has processed about the individual",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-273", "P-037", "Deletion right: MDPPA delete vs GDPR-style erasure",
     "delete covered data... export to the individual",
     "the right to request that a controller delete any personal information processed",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-272", "P-038", "Correction right: MDPPA correct vs GDPR-style rectification",
     "correct any verifiable substantial inaccuracy",
     "correct inaccurate personal information processed about the individual",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-274", "P-276", "Export/portability right: MDPPA export vs GDPR-style portability",
     "export to the individual or directly to another entity the covered data of the "
     "individual ... a portable, structured, interoperable, and machine-readable format",
     "in a structured, commonly used and machine-readable format",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-012", "P-034", "Opt-out of transfers/targeted ads: MDPPA vs MIPSA sale/ads opt-out with universal signal",
     "may not transfer or direct the transfer of the covered data of an individual to a third party if the individual objects",
     "the right to opt out of the processing of the individual's personal information",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-012", "P-053", "Opt-out vs GDPR objection right for direct marketing (H1555)",
     "may not transfer or direct the transfer of the covered data of an individual to a third party if the individual objects",
     "the right to object at any time to processing of personal data concerning the data subject for the marketing",
     f"{K}/family-mipsa-internet.md"),
    ("P-014", "P-019", "Universal opt-out signals (redraft) vs OCABR centralized opt-out mechanism (filed)",
     "an Internet link or a browser setting, browser extension or global device setting",
     "establish or recognize one or more acceptable privacy protective, centralized mechanisms",
     f"{K}/family-comprehensive-mdppa.md"),
    ("P-009", "P-040", "Anti-retaliation/nondiscrimination for exercising rights: MDPPA vs MIPSA",
     "may not retaliate against an individual for:- exercising any of the rights guaranteed by this chapter",
     "shall not discriminate against an individual for exercising in good faith any of the rights",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-017", "P-044", "Civil-rights processing ban: MDPPA vs MIPSA",
     "discriminates in or otherwise makes unavailable the equal enjoyment of goods or services",
     "discriminates in, or otherwise makes unavailable, the equal enjoyment of goods or services",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-018", "P-043", "Algorithmic/risk assessments: MDPPA impact assessments vs MIPSA/H1555 risk assessments-DPIA",
     "shall conduct an impact assessment of such algorithm in accordance with paragraph (1)",
     "carry out and document a risk assessment of the impact",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-022", "P-041", "Processor/service-provider contract duties: MDPPA vs GDPR-style",
     "shall adhere to the instructions of a covered entity and only collect, process, and transfer service provider data",
     "A contract between a controller and a processor shall govern the processor's procedures",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-023", "P-063", "General private right of action: MDPPA vs H1555 damages remedy",
     "liquidated damages of not less than 0.15% of the annual global revenue... or $15,000 per violation",
     "Any person who has suffered material or non-material damage as a result of an infringement",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-024", "P-045", "AG enforcement architecture: MDPPA 93A penalties vs MIPSA exclusive AG with cure",
     "not more than 4% of the annual global revenue... or $20,000,000, whichever is greater",
     "civil penalties of up to 7,500 dollars for each violation",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-024", "P-062", "AG enforcement: MDPPA vs H1555 GDPR-scale administrative fines",
     "not more than 4% of the annual global revenue... or $20,000,000, whichever is greater",
     "administrative fines up to $20,000,000, or in the case of an undertaking, up to 4 per cent of the total worldwide annual turnover",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-mipsa-internet.md"),
    ("P-046", "P-130", "Breach-limited PRA (MIPSA) vs location-chapter PRA (H357/S148): parallel architecture, different scopes",
     "damages from the controller in an amount up to 500 dollars per individual per incident",
     "actual damages, including damages for emotional distress, or $5,000 per violation, whichever is greater",
     f"{K}/family-mipsa-internet.md; {K}/family-location.md"),
    ("P-026", "P-128", "Legal-request transparency reports: MDPPA bi-monthly vs location-chapter annual AG reports",
     "provide the Attorney General and the general public a bi-monthly report",
     "report to the attorney general aggregate information pertaining to any warrants seeking location information",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-location.md"),
    ("P-087", "P-128", "Warrant transparency reports: biometric chapter vs location chapter (parallel drafting)",
     "on an annual basis, report to the attorney general aggregate information regarding any warrants for biometric information",
     "report to the attorney general aggregate information pertaining to any warrants seeking location information",
     f"{K}/family-biometric-breach.md; {K}/family-location.md"),
    ("P-125", "P-131", "Warrant gate over location/electronic data: duty on private holders (shield) vs bar on government acquisition (H1653/S27)",
     "serves the covered entity or service provider with a valid warrant or establishes the existence of exigent circumstances",
     "Except pursuant to a warrant issued by a justice of the superior court",
     f"{K}/family-location.md"),
    ("P-128", "P-134", "Warrant reporting: covered entities to AG vs courts to legislature",
     "report to the attorney general aggregate information pertaining to any warrants seeking location information",
     "shall transmit to the legislature a full and complete report concerning the number of applications for warrants",
     f"{K}/family-location.md"),
    ("P-139", "P-125", "Tension: compelled emergency carrier disclosure (H1519) vs warrant gate on the same holder class (shield bills)",
     "shall immediately provide location information concerning the telecommunications devices of the user to the requesting law enforcement agency",
     "serves the covered entity or service provider with a valid warrant or establishes the existence of exigent circumstances",
     f"{K}/family-location.md"),
    ("P-058", "P-097", "Breach notification: H1555 72-hour GDPR mechanism vs c.93H notice modernization",
     "not later than 72 hours after having become aware of it, notify the personal data breach to the attorney general",
     "the date, estimated date, or estimated date range of the breach of security",
     f"{K}/family-mipsa-internet.md; {K}/family-biometric-breach.md"),
    ("P-057", "P-085", "Security standards: H1555 general measures vs biometric-specific standard",
     "a level of security appropriate to the risk",
     "store, transmit, and protect from disclosure all biometric data using the reasonable standard of care",
     f"{K}/family-mipsa-internet.md; {K}/family-biometric-breach.md"),
    ("P-091", "P-081", "Biometric protection: 93H breach-law element vs standalone consent regime (different mechanism)",
     "any unique biological attribute or measurement that can be used to authenticate the identity of an individual",
     "shall not collect or process an individual's biometric information for identification purposes unless it first",
     f"{K}/family-biometric-breach.md"),
    ("P-068", "P-072", "ISP opt-in consent: private franchised ISPs (S218/H3179) vs public ISP (H3831)",
     "without express written approval from the customer",
     "not share data information with 3rd parties...or with opt-in consent of users",
     f"{K}/family-mipsa-internet.md"),
    ("P-076", "P-131", "Warrant for user data: public-ISP rule vs general stored-records regime",
     "shall not be provided to law enforcement without a warrant",
     "Except pursuant to a warrant issued by a justice of the superior court",
     f"{K}/family-mipsa-internet.md; {K}/family-location.md"),
    ("P-183", "P-171", "Biometric analysis of drone data (S1557) vs LE biometric surveillance ban (FR bills); S1557 cross-references c.6 s.220",
     "Facial recognition and other biometric matching technology shall not be used to analyze data produced by an unmanned",
     "unlawful for a law enforcement agency or officer to acquire, possess, access, use, assist with the use of",
     f"{K}/family-facial-recognition.md"),
    # eighth-pass finding 9: P-213 was split; the retention prong (P-383) is
    # the half this kinship was about. H3404's disclosure prong is no longer a
    # kinship at all - it is now a P-196 identity edge.
    ("P-383", "P-196", "ALPR restrictions: c.90K retention cap (H3404) vs comprehensive access regime (H3431)",
     "retain ALPR data longer than 14 days except in connection with a specific criminal investigation",
     "a governmental entity may not access, search, review, disclose, or exchange ALPR data from any source",
     f"{K}/family-driver-commercial.md; {K}/family-facial-recognition.md"),
    ("P-211", "P-194", "120-day retention/destruction: tolling data (H3434/H3404) vs ALPR data at EOPSS (H3431)",
     "permanently erase or destroy ... not later than 120 days following the date on which the tolling data was created",
     "shall retain and store ALPR data transferred to it pursuant to section 4 for a period of 120 days",
     f"{K}/family-driver-commercial.md; {K}/family-facial-recognition.md"),
    ("P-141", "P-162", "Targeted ads to minors: edtech school-data ban vs product-category ban on minor-directed services",
     "shall not ... engage in targeted advertising on the operator's site, service or application",
     "shall not market or advertise a product or a service described in subsection (g)",
     f"{K}/family-student-education.md"),
    ("P-015", "P-162", "Minors and targeted advertising: comprehensive-bill ban vs H80 product-category ban",
     "may not engage in targeted advertising to any individual if the covered entity has knowledge that the individual is a covered minor",
     "shall not market or advertise a product or a service described in subsection (g)",
     f"{K}/family-comprehensive-mdppa.md; {K}/family-student-education.md"),
    ("P-226", "P-067", "Doxing: general civil action (H1707/S971) vs police-officer criminal posting ban (H1428)",
     "the person disseminated the personal information with the malicious intent to cause, aid, encourage or facilitate the harassment",
     "shall publicly post or publicly display on the internet or make publicly available in any manner the personal information",
     f"{K}/family-driver-commercial.md; {K}/family-mipsa-internet.md"),
    ("P-226", "P-266", "Interpersonal disclosure restrictions: doxing civil action vs NDII criminal offense (boundary-revision pairing)",
     "the person disseminated the personal information with the malicious intent to cause, aid, encourage or facilitate the harassment",
     "whoever knowingly distributes visual material depicting another person, either "
     "identifiable in the visual material or identified by the distributing person "
     "... nude, partially nude or engaged in sexual conduct",
     f"{K}/family-driver-commercial.md; data/link_targets.json"),
    ("P-238", "P-211", "Retention limits: ad-network 24-month vs tolling 120-day (same mechanism family, different targets)",
     "for duration of a maximum of twenty-four months from the time of collection",
     "permanently erase or destroy ... not later than 120 days following the date on which the tolling data was created",
     f"{K}/family-driver-commercial.md"),
    ("P-246", "P-284", "Sale bans: consumer health data vs location information",
     "It shall be unlawful for a Regulated Entity to sell Consumer Health Data.",
     "sell, rent, trade, or lease location information to third parties",
     f"{K}/family-health-govrecords.md; {K}/family-location.md"),
    ("P-035", "P-242", "Sensitive-data opt-in: comprehensive-bill gates vs consumer-health-data chapter",
     "shall not otherwise process an individual's sensitive information without first obtaining the consent",
     "shall not collect any Consumer Health Data except: (a) With consent from the consumer",
     f"{K}/family-mipsa-internet.md; {K}/family-health-govrecords.md"),
    ("P-234", "P-006", "Sensitive data in advertising: ad-network opt-in (H395) vs MDPPA flat ban",
     "shall not use information about sensitive medical or financial data, sexual behavior or sexual orientation ... without the affirmative consent",
     "process sensitive covered data for purposes of targeted advertising",
     f"{K}/family-driver-commercial.md; {K}/family-comprehensive-mdppa.md"),
]

# Judgment calls and anomalies for the same review queue.
FLAGS = [
    ("S2539", "P-101", "Borderline in-domain: insurance/contract protection for breach reporting (SECTION 17).", "memo/atomization/family-biometric-breach.md"),
    ("S2539", "P-287;P-288;P-289", "Boundary call: delegated AI-training-data rulemaking mandates atomized per the codebook AI carve-in.", "memo/atomization/family-biometric-breach.md"),
    ("H1455", "", "Title says 'tracking of certain electronic devices' but official text is verbatim S209 (tolling data). Census include stands on the text.", "memo/atomization/family-driver-commercial.md"),
    ("H3217", "", "Reclassified to exclude under the symmetric program-incident rule (was a marginal include); successor H4502 verified not to carry its privacy clauses.", "memo/codebook.md"),
    ("S1368", "P-260", "Marginal census include: physical-adjacent confidentiality mechanism.", "memo/codebook.md"),
    ("H1986", "P-165", "Marginal census include: study resolve with data-practice charges.", "memo/codebook.md"),
    ("H4744", "P-266", "Boundary revision: interpersonal disclosure restrictions (doxing, NDII) are in-domain regardless of civil/criminal mechanism; reversal of the initial criminal-harassment carve-out, recorded in the codebook.", "memo/codebook.md"),
    ("2024 c.166", "", "Judgment call: parentage-case impoundment (c.209C ss.28I, 28O) and surrogacy-record confidentiality (s.28B(a)(ix)) ruled EX-ADJACENT as procedure-incident, in tension with the IN verdict for c.118 s.43A(b)(5); reviewer should check the distinction (protects case papers vs protects the regulated material itself).", "data/enacted_adjudication.csv"),
    ("2024 c.221 / H3735", "", "Judgment call contested by external review: the Truro disability-proof nondisclosure clause is ruled program-incident (symmetric on filed and enacted sides); the reviewer reads the codebook's government-records subdomain as covering it. If reversed, both H3735 and 2024 c.221 enter and the enacted count rises by one.", "data/enacted_adjudication.csv"),
    ("2024 c.238/c.343/c.252/c.186/c.178", "", "Judgment call: program-incident data provisions (registries, compact data system, mortality reviews, TND board records, burn-pit registry) excluded SYMMETRICALLY from both filed and enacted sides; see codebook program-incident rule.", "data/enacted_adjudication.csv"),
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

    for bn in sorted(hist):
        d = hist[bn]
        hurl = f"https://malegislature.gov/Bills/193/{bn}"
        for a in d["actions"]:
            act = a["Action"].strip()
            p = actions.parents_of(act)
            if p:
                for parent in p[0]:
                    add(bn, parent, p[1], "verified-official-record", act, hurl)
            s = actions.successor_of(act)
            if s:
                add(bn, s[0], s[1], "verified-official-record", act, hurl)
            so = actions.study_order_of(act)
            if so:
                add(bn, so, "sent_to_study", "verified-official-record", act, hurl)
        for s in d.get("similar", []):
            add(bn, f"{s['general_court']}:{s['bill']}", "official_similar",
                "verified-official-record", "Similar Bills tab",
                f"https://malegislature.gov/Bills/193/{bn}/SimilarBills")

    # text-identity detection among included bills. This claims TEXTUAL
    # relationship only (review finding 9): whether a pair is a companion,
    # a refile, or a redraft is determined by the official-record links
    # above, not by similarity.
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
                typ = "text_identical"
            elif j >= 0.50:
                typ = "text_near_identical"
            else:
                continue
            add(a, b, typ, "verified-text-comparison",
                f"normalized 8-gram Jaccard {j:.3f} between official texts",
                f"https://malegislature.gov/Bills/193/{a}")

    # study-order terminal verification (review findings 7, 9, 11): each
    # study order's own terminal actions go to a status table, NOT the link
    # graph (they are unary evidence records, not edges). Anything a study
    # order "Reported (in part)" is followed into link_targets.json and its
    # relevance recorded.
    lt_path = DATA / "link_targets.json"
    study_rows = []
    if lt_path.exists():
        lt = json.loads(lt_path.read_text())
        study_targets = sorted({l["target"] for l in links if l["link_type"] == "sent_to_study"})
        for so in study_targets:
            if so not in lt:
                continue
            acts = [a["Action"].strip() for a in lt[so]["actions"] if not a.get("IsStricken")]
            reported = []
            for a in acts:
                # Eighth-pass review: this used an ad-hoc regex matching only
                # the parenthesised form, so H4675's "Reported, in part, by
                # H3107" was missed and its reported_out cell came out blank
                # even though 05c had already fetched H3107 - which made the
                # codebook's "relevance recorded" claim false. The shared
                # parser in actions.py knows both forms; there is no reason
                # for a second copy here.
                s_ref = actions.successor_of(a)
                if s_ref and s_ref[1] == "reported_in_part_by":
                    ref = s_ref[0]
                    refd = lt.get(ref)
                    if refd is None:
                        reported.append(f"{ref} (NOT FETCHED - incomplete)")
                    else:
                        reported.append(f"{ref}: {refd['Title'][:60]} "
                                        f"({len(refd['text'])} chars; terminal: "
                                        f"{[x['Action'][:40] for x in refd['actions'] if not x.get('IsStricken')][-1]})")
            study_rows.append({
                "study_order": so,
                "terminal_actions": "; ".join(acts[-2:]) if acts else "no actions recorded",
                "reported_out": " | ".join(reported),
                "url": f"https://malegislature.gov/Bills/193/{so}",
            })
    with (DATA / "study_order_status.csv").open("w", newline="") as f:
        w = csvutil.dict_writer(f, fieldnames=["study_order", "terminal_actions", "reported_out", "url"])
        w.writeheader()
        w.writerows(study_rows)

    # Absorption links: dead standalone carriers -> the enacted vehicle that
    # carried their proposition into law (third-pass review finding 2).
    # (standalone, vehicle, prop, confidence, note)
    ABSORPTIONS = [
        ("H1525", "H58", "P-291", "verified-text-comparison", "identical use/sale restriction, 2023 c.2 s.33"),
        ("S943", "H58", "P-291", "verified-text-comparison", "identical use/sale restriction, 2023 c.2 s.33"),
        ("H3003", "H4040", "P-297;P-298", "verified-text-comparison", "same mechanism enacted at 2023 c.28 s.7"),
        ("H1690", "H4977", "P-295;P-296", "verified-text-comparison", "HOMES regime enacted at 2024 c.150 ss.28,52"),
        ("S956", "H4977", "P-295;P-296", "verified-text-comparison", "HOMES regime enacted at 2024 c.150 ss.28,52"),
        ("H4356", "H4977", "P-295;P-296", "verified-text-comparison", "HOMES redraft regime enacted at 2024 c.150 ss.28,52"),
        ("H2991", "H5077", "P-294", "inferred-needs-review", "enacted 2024 c.248 s.27 is a broader variant of H2991's home-address mechanism"),
    ]
    for sb, veh, prop, conf, note in ABSORPTIONS:
        add(sb, veh, "absorbed_into_vehicle", conf, f"{prop}: {note}",
            f"https://malegislature.gov/Bills/193/{veh}")

    for pa, pb, why, ex_a, ex_b, src in KINSHIPS:
        add(pa, pb, "proposition_kinship", "inferred-needs-review", why, src)

    with (DATA / "links.csv").open("w", newline="") as f:
        w = csvutil.dict_writer(f, fieldnames=["source", "target", "link_type", "confidence", "evidence", "evidence_url"])
        w.writeheader()
        w.writerows(links)

    # verification queue: kinship links with side-by-side excerpts, analytic
    # identity merges from bill_propositions.csv, and judgment flags
    with (DATA / "verification_queue.csv").open("w", newline="") as f:
        w = csvutil.writer(f)
        w.writerow(["item_type", "a", "b", "question", "excerpt_a", "excerpt_b", "sources"])
        for pa, pb, why, ex_a, ex_b, src in KINSHIPS:
            w.writerow(["proposition_kinship", pa, pb, why, ex_a, ex_b, src])
        n_identity = 0
        import atoms
        bp_path = DATA / "bill_propositions.csv"
        if bp_path.exists():
            by_prop = {}
            for r in csv.DictReader(bp_path.open()):
                by_prop.setdefault(r["prop_id"], []).append(r)
            for pid in sorted(by_prop):
                rows = by_prop[pid]
                inferred = [r for r in rows if r["identity_basis"] == "inferred-analytic"]
                for r in sorted(inferred, key=lambda x: x["bill"]):
                    others = sorted(x["bill"] for x in rows if x["bill"] != r["bill"])
                    comparator = next((o for o in others if (o, pid) in atoms.QUOTES), others[0] if others else "")
                    w.writerow([
                        "proposition_identity", f"{pid}:{r['bill']}", f"{pid}:{comparator}",
                        f"Is {r['bill']} ({r['sections']}) the same smallest change as {comparator}'s version of {pid}? Analytic judgment, not companion/redraft verified.",
                        atoms.QUOTES.get((r["bill"], pid), f"[quote missing for {r['bill']}:{pid}]"),
                        atoms.QUOTES.get((comparator, pid), f"[quote missing for {comparator}:{pid}]"),
                        f"https://malegislature.gov/Bills/193/{r['bill']}; https://malegislature.gov/Bills/193/{comparator}",
                    ])
                    n_identity += 1
        for bill, prop, note, src in FLAGS:
            w.writerow(["judgment_flag", bill, prop, note, "", "", src])

    from collections import Counter
    print(Counter(l["link_type"] for l in links))
    print(f"{len(links)} links; queue: {len(KINSHIPS)} kinships + {n_identity} identity merges + {len(FLAGS)} flags")


if __name__ == "__main__":
    main()
