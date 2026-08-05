# Codebook: consumer data privacy, 193rd General Court (2023-2024)

Status: complete through fate classification (Goals 1-4); revised 2026-08-05 in response to external review (see "Revision log" at the end).

## Fate rules (Goal 4)

Bill-level terminal classes (`data/bill_fates.csv`), parsed from official histories by `scripts/08_fates.py`:

- `superseded_by_redraft`: history ends in "Accompanied a new draft, see X", "New draft substituted, see X", or "Reported by X" (conference)
- `sent_to_study`: history ends in "Accompanied a study order, see X"
- `died_no_further_action`: history ends in "No further action taken"
- `enacted`: "Signed by the Governor, Chapter N of the Acts of YYYY" (one bill: H4744)
- (recorded-vote rejection is parsed for but did not occur)

Furthest-stage ladder: referred < heard < reporting_extended < reported_favorably < second_reading < engrossed_one_branch < in_second_branch < conference < passed_both < enacted.

Proposition-level fate (`data/proposition_fates.csv`): a proposition's final vehicles are its carrier bills excluding any bill superseded by a redraft that still carries the proposition (the chain is followed through redrafts).
Fate is the most informative terminal across final vehicles:

- `enacted_as_filed`: an enacted final vehicle carries the proposition through its official chain.
  One occurred: P-266 (NDII distribution ban) via H4744, enacted unanimously (House Y&N No. 119/121, Senate Roll Call #179) and signed as 2024 c.118.
- `enacted_other_vehicle`: proposition text found in an enacted chapter without an official chain connection.
  The sweep runs BEFORE fate assignment (review finding 2); reviewed matches live in `ENACTED_MATCHES` in `scripts/08_fates.py` and feed the classification.
  All other probe hits were reviewed as false positives; the review verdicts are recorded in `PROBE_FALSE_POSITIVES` in the same script.
- `rejected_by_recorded_vote`: none occurred; every roll call recorded in the census was in favor (H4844's 159-0 House passage; H4744's unanimous enactment votes)
- `sent_to_study`: a final vehicle was accompanied by a study order
- `died_no_recorded_action`: final vehicles ended with no further action, or every carrier was consolidated into a redraft that dropped the proposition (`dropped_in_consolidation` = yes, always with "no public explanation" in the detail, since the record never explains drops)
- `indeterminate`: reserved for unparseable records; none occurred

The fate citation is the vehicle that establishes the fate (review finding 6); the furthest-stage vehicle is cited in its own column.
All selections are sorted, and `scripts/09_checks.py` asserts byte-identical output on rerun.

"Sent to study" is recorded as its own fate because it is an explicit recorded disposition, but no study order in this census led to any further recorded action; functionally it is a terminal outcome.

## Link rules (Goal 3)

Link types in `data/links.csv`, with the confidence vocabulary:

- `redraft_of` (verified-official-record): the bill's official history says "New draft of X, Y and Z"; the successor bill points at every named parent.
- `superseded_by` (verified-official-record): the parent's history says "Accompanied a new draft, see X."
- `sent_to_study` (verified-official-record): "Accompanied a study order, see X" - the standard death-by-study mechanism; X is the study order.
- `reported_from_part_of` (verified-official-record): "Reported on a part of X" - a committee carved this bill out of vehicle X.
- `official_similar` (verified-official-record): a listing on the bill's Similar Bills tab; includes cross-session entries (refilings) where the site records them.
- `text_identical` (verified-text-comparison): normalized 8-gram Jaccard similarity >= 0.85 between the two official texts.
  RENAMED from `companion_identical` (review finding 9): similarity claims a TEXTUAL relationship only; whether a pair is companions, a refile, or a redraft is established by the official-record links, not by similarity.
- `text_near_identical` (verified-text-comparison): Jaccard in [0.50, 0.85) - substantially the same text with drafting variations (for example H83 vs S25, where one chamber's numbering style shreds 8-grams; the atomization notes verified them substantively identical).
- `study_order_terminal` (verified-official-record): each study order's own terminal actions, fetched and recorded so the claim that no study order produced further action rests on the orders' histories, not on assumption (review finding 7).
- `proposition_kinship` (inferred-needs-review): hand-proposed link between two DIFFERENT propositions sharing a goal but not a mechanism.
  Every kinship link sits in `data/verification_queue.csv` with verbatim side-by-side excerpts from the official texts.
- Study-order terminal records live in `data/study_order_status.csv`, not in the link graph (they are unary evidence, not edges); anything a study order "Reported (in part)" is fetched and its relevance recorded there (S2612 reported S2538, a jury-clerk bill with no privacy content).

Proposition identity across bills (the same P-NNN appearing on several bills in `data/bill_propositions.csv`) is itself a link claim.
Every edge now carries an `identity_basis` (review finding 10): `sole-carrier` (no cross-bill claim), `verified-text-identical` (Jaccard >= 0.85 with another carrier), `verified-official-lineage` (connected by an official redraft/supersession/conference record), `verified-text-near-identical` (Jaccard in [0.50, 0.85), i.e. the same text under different drafting conventions, with the manual diff recorded in the atomization notes), or `inferred-analytic` (same-mechanism judgment only).
Empty or sub-8-word texts yield an empty shingle set and can never be "identical" (H4241/H4744, whose API text is empty, rest on official lineage).
All `inferred-analytic` edges are queued in `data/verification_queue.csv` as `proposition_identity` items with verbatim side-by-side quotes (`QUOTES` in `scripts/atoms.py`).

## Atomization rules (Goal 2)

A proposition is the smallest change in law that could stand alone: it could be enacted by itself as a coherent, self-contained policy.
Operational tests, applied in order:

1. SEVERABILITY: if the provision were struck from the bill, would the rest still function?
   If striking it breaks other provisions, it is part of a larger proposition.
2. STANDALONE SENSE: could a one-sentence description of the provision be understood as a policy on its own ("data brokers must register with the AG annually")?
   Definitions, effective dates, severability clauses, and appropriations that merely fund another provision fail this test and attach to the substantive proposition they serve.
3. GRAIN LIMIT: enforcement provisions (penalties, AG authority, private rights of action) are separate propositions only when the bill treats them separately or when companion bills differ on exactly that point; otherwise they attach to the duty they enforce.

Propositions are identified across bills, not within one bill: two bills proposing the same smallest change carry the same proposition ID.
Whether two provisions are "the same" proposition: same legal mechanism aimed at the same target (not merely the same goal).
A stricter and a weaker version of the same mechanism are the same proposition (the difference is recorded on the bill-proposition edge); a different mechanism for the same goal is a different proposition.

IDs are `P-NNN` (persistent, never reused; retired IDs stay retired - P-011, P-036, P-244, P-265 are retired, see `RETIRED` in `scripts/atoms.py`).
Rights granted in one bill section but severable as policies (access, correction, deletion, portability) are separate propositions; the initial bundling of H83 s.8 violated this and was split (review finding 4).
The proposition table is hand-authored analysis stored as data in `scripts/atoms.py`, compiled and validated by `scripts/06_compile_atoms.py`; every bill-proposition assignment cites the section(s) of the bill text that ground it.

## Domain definition

A filing is IN the domain of consumer data privacy when at least one of its provisions would change Massachusetts law governing the collection, use, retention, disclosure, sale, or protection of information about an identified or identifiable natural person, where that information is held or handled by a party other than that person (a business, a data broker, a platform, a government agency acting as a data holder, or another individual).

Included subdomains:

- comprehensive consumer data privacy regimes (controller/processor duties, consumer rights, opt-outs, private rights of action)
- data broker registration and regulation
- biometric identifiers and facial recognition
- location information, including location shields and geofencing
- genetic and health data privacy, including reproductive-health data
- children's and students' online data and social media data practices
- browsing, search, and telematics data
- data security and breach notification obligations
- government acquisition of personal data held by commercial parties (location shield acts, warrant standards for stored communications and browsing data, carrier location disclosure)
- interpersonal disclosure restrictions on identifiable personal information or images, regardless of civil or criminal mechanism: doxing civil actions AND nonconsensual distribution of identifiable intimate imagery (NDII).
  REVISED 2026-08-05: the original text excluded "criminal harassment provisions without a data-handling rule," which was inconsistent with the inclusion of the doxing bills (same mechanism, civil remedy) and would have excluded the one enacted disclosure restriction in the domain (2024 c.118 s.6).
  Conduct-regulation without a disclosure element stays OUT: coercive-control definitions, protective-order law, harassment penalties, and minor-sexting diversion programs
- government surveillance of individuals through data-generating technology (facial recognition, ALPR data, police drone data rules)
- restrictions on disclosure of personal information held in government records (911 recordings, lottery winners, victim compensation records, firearm licensee information)

PROGRAM-INCIDENT RULE (added 2026-08-05, second-pass review): a confidentiality, de-identification, or data-system clause that is incident to a program a provision creates (a disease registry, review committee, licensure compact, labor board, benefit program) does NOT bring the filing or provision into the census.
The rule is applied SYMMETRICALLY: the filed-bill census never swept the hundreds of filed program bills for incidental confidentiality clauses, so counting such clauses only on the enacted side would bias the passage rate upward.
In-census when the data handling is the provision's primary object: rights or disclosure restrictions over an existing record class (eviction sealing, 911 recordings), duties on data holders as such (notary personal-info use restrictions), or filings whose primary subject IS a personal-data system (the education-to-career data center bills).
Applying this rule symmetrically reclassified H3217 (energy-scorecard bill with two incidental privacy clauses) to excluded, and keeps enacted program-incident provisions (Parkinson's registry, nurse-compact data system, mortality-review data rules, burn-pit registry, TND board records) out of the proposition universe; every such verdict is recorded row-level in data/enacted_adjudication.csv.

Excluded, with the boundary rationale:

- wiretap/interception statutes (c.272 s.99 amendments, warrant length, recording defenses): real-time interception authority is treated as criminal procedure, a separate domain.
  The line drawn: access to STORED commercial data about a person is IN (location shield, H1653/S27); authority to INTERCEPT communications in real time is OUT.
  Excluded bills: H73, H1722, H1786, S1075, S1093, S1128, S1141.
- forensic DNA (database expansion, familial search, DNA exceptions to limitation periods): criminal-procedure use of biometric material, not data-handling rules for consumers
- consumer reporting regulation (credit reports in housing or employment): consumer-finance domain; the mechanism is anti-discrimination or credit regulation, not data privacy (mortgage trigger-lead bills stay IN because their mechanism is the sale of application data)
- right-to-repair telematics: expands data ACCESS for repair-market competition rather than protecting personal data
- physical or visual privacy without a data-handling rule (video surveillance of neighbors, drone peeping offenses, nursing-home dignity)

- pure cybersecurity of state systems with no individual-rights provision (infrastructure hardening, IT funding)
- artificial intelligence regulation UNLESS the provision governs personal data as defined above
- open-meeting or public-records law (transparency of government, not privacy of individuals' data), except provisions restricting disclosure of personal information held in public records
- financial reporting, "data" in the sense of statistics or program metrics
- identity-document rules (licenses, IDs) without a data-handling provision
- sick-leave banks, land takings, and other named-individual acts

## Census universe

- Source: `/api/GeneralCourts/193/Documents` on malegislature.gov, fetched 2026-08-04; 10,156 documents, of which 8,183 carry a bill number (bills, resolves, orders) and 1,973 are docket-book-only entries.
- Enacted-vehicle universe: `/api/SessionLaws/2023` and `/2024`, 464 chapters, full text scanned, so budget outside sections are covered.
- FEEDBACK LOOP (added 2026-08-05, review finding 1): every enacted chapter with confirmed in-domain content is traced to its origin bill via the chapter's `OriginBill` field, and that bill plus its official lineage ("New draft of", "New draft substituted", "Reported by/on") is admitted to the census with reason `IN-ENACTED-FEEDBACK` (`scripts/04_inclusion.py` ADDITIONS; lineage fetched by `scripts/05c_link_targets.py`).
  This is how the NDII family (H1745/S1012/S1139 -> H4115 -> H4241 -> H4744 -> 2024 c.118) entered the census despite its generic title ("An Act to prevent abuse and exploitation") evading every title and committee net.

## Candidate-generation rules (recall net)

A document enters the candidate pool if any of:

1. Title matches a DOMAIN term regex (see `scripts/01_census.py`, `DOMAIN_TERMS`).
2. Title matches a BROAD term regex (`BROAD_TERMS`); these are kept only if full-text scan (`scripts/02_textscan.py`) finds domain text terms.
3. The document appears in the reported-out or before-committee list of the Joint Committee on Advanced Information Technology, the Internet and Cybersecurity (J33), regardless of title.

Known recall limitation: a bill whose title contains none of the broad terms, that was never referred to J33, and whose privacy content appears only in its text, is invisible to this net.
The enacted-vehicle sweep closes this gap for anything that became law; for bills that died, the gap is real and is reported in the memo's limitations.

## Inclusion decision

Every candidate receives an explicit decision (include / exclude) with a reason code, produced by `scripts/04_inclusion.py` and reviewed at the census checkpoint.
Reason codes:

- `IN-TITLE`: domain title term plus confirming text evidence
- `IN-TEXT`: broad-net title, domain confirmed in full text
- `IN-COMMITTEE`: J33 referral plus confirming text evidence
- `EX-FALSEPOS`: matched term used in a non-domain sense (for example "tracking" of prescription drug prices, "data" as program statistics)
- `EX-ADJACENT`: genuinely about information/technology but outside the domain definition above (with subcategory noted)
- `EX-NOBILL`: docket-book-only entry that never received a bill number; counted separately, text unavailable through the bill API
- `EX-PROCEDURAL`: committee extension orders and statutory annual reports (for example the district attorneys' wiretap reports), which are filings but not proposed legislation
- `EX-PROGRAM-INCIDENT`: filings whose only in-domain content is a confidentiality/data clause incident to a program they create (symmetric with the enacted-side rule above)
- `IN-ENACTED-FEEDBACK`: filings admitted by tracing enacted in-domain provisions to their origin bills and filed lineages

After the first pass, a vocabulary audit of all 10,156 titles added five speculative term groups (license plate reader, drone/unmanned, credit report, right to repair, deepfake) to the broad net so their relevance could be settled from bill text rather than assumption; the resulting decisions are recorded in `scripts/04_inclusion.py` OVERRIDES with per-bill notes.
Every override entry names its reason code and a one-line justification; the auto rule handled the unambiguous cases (38 includes, all strong-term, and the no-evidence excludes).

## Revision log

2026-08-05, in response to an external review of PR #1 (all twelve findings accepted):

1. Domain boundary revised: interpersonal disclosure restrictions (doxing, NDII) are in-domain regardless of civil/criminal mechanism.
   This reverses the original criminal-harassment carve-out, which was inconsistent with the doxing inclusion and would have excluded the domain's only enactment (2024 c.118 s.6).
2. Enacted-vehicle feedback loop added to the census (IN-ENACTED-FEEDBACK); the NDII lineage admitted (six bills).
3. H4844 re-atomized from the official PDF onto the location-family propositions as narrowed variants (P-265 retired); its extraction script rewritten to read the cached PDF deterministically.
4. Bundled rights split (P-011 -> P-271..P-274; P-036 -> P-275/P-276; P-244 -> P-277/P-278); S2539's AI-training-data consent rulemaking atomized (P-267).
5. Fate pipeline restructured: probe before fates, ENACTED_MATCHES feeds classification, fate-vehicle citations, deterministic output.
6. Similarity links renamed to text_identical/text_near_identical; identity_basis added to every bill-proposition edge; verification queue rebuilt with side-by-side excerpts and valid paths; study-order and redraft-successor records fetched before terminal claims; `scripts/09_checks.py` added.

2026-08-05, second pass, in response to a follow-up external review (all thirteen findings accepted):

1. Row-level enacted adjudication: every chapter flagged by the probe or the session-law scan carries per-provision verdicts in `data/enacted_adjudication.csv` (enforced exhaustive by the pipeline); the probe CSV now carries verdicts per hit.
2. Three more enacted vehicles admitted with their filed lineages: 2023 c.2 s.33 (notary personal-info restriction; H1525/S943), 2024 c.150 ss.28/52 (eviction-record sealing; H1690/S956/H4356), and c.118 s.6's court-record confidentiality atomized separately (P-280).
   P-266's description corrected: distribution is required, threat is an intent element, the repeat-offender penalty attaches.
3. Program-incident rule added (symmetric exclusion of confidentiality clauses incident to programs) and applied both ways: H3217 reclassified to excluded; enacted registry/compact/review-board provisions recorded as EX-PROGRAM-INCIDENT rather than silently ignored.
4. H4844 fully split with corrected subsection cites (s.2(b)(i)-(v), s.2(c), s.4 rulemaking topics); location-family minimization and sale/disclosure bundles split (P-123/P-124 retired into P-281..P-285); S2539 rulemaking split (P-267 retired into P-287..P-289).
5. Text-identity requires >= 8 words (empty texts can no longer be "identical"); H4241/H4744 identity rests on official lineage.
   A verified-text-near-identical basis tier records same-text-different-drafting pairs.
6. Study-order statuses moved out of the link graph into `data/study_order_status.csv`; S2612's reported-out bill (S2538) fetched and verified irrelevant.
7. All analytic identity merges queued with verbatim side-by-side quotes (`QUOTES` in `scripts/atoms.py`).
8. The findings memo is written as a current-state snapshot; revision history lives here and in the pull-request discussion.
