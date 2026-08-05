# Codebook: consumer data privacy, 193rd General Court (2023-2024)

Status: draft, link-graph stage.
Fate classification will extend this file.

## Link rules (Goal 3)

Link types in `data/links.csv`, with the confidence vocabulary:

- `redraft_of` (verified-official-record): the bill's official history says
  "New draft of X, Y and Z"; the successor bill points at every named parent.
- `superseded_by` (verified-official-record): the parent's history says
  "Accompanied a new draft, see X."
- `sent_to_study` (verified-official-record): "Accompanied a study order,
  see X" - the standard death-by-study mechanism; X is the study order.
- `reported_from_part_of` (verified-official-record): "Reported on a part
  of X" - a committee carved this bill out of vehicle X.
- `official_similar` (verified-official-record): a listing on the bill's
  Similar Bills tab; includes cross-session entries (refilings) where the
  site records them.
- `companion_identical` (verified-text-comparison): normalized 8-gram
  Jaccard similarity >= 0.85 between the two official texts, computed by
  `scripts/07_links.py` from the cached texts.
- `companion_near_identical` (verified-text-comparison): Jaccard in
  [0.50, 0.85) - substantially the same text with drafting variations
  (for example H83 vs S25, where one chamber's numbering style shreds
  8-grams; the atomization notes verified them substantively identical).
- `proposition_kinship` (inferred-needs-review): hand-proposed link between
  two DIFFERENT propositions sharing a goal but not a mechanism.
  Every kinship link sits in `data/verification_queue.csv` with a pointer
  to the side-by-side excerpts in `memo/atomization/`.

Proposition identity across bills (the same P-NNN appearing on several
bills in `data/bill_propositions.csv`) is itself a link claim; its
confidence is verified-text-comparison when the bills are companions or
redrafts confirmed by diff, and the variant notes on each edge record
stricter/weaker deltas.

## Atomization rules (Goal 2)

A proposition is the smallest change in law that could stand alone: it could
be enacted by itself as a coherent, self-contained policy.
Operational tests, applied in order:

1. SEVERABILITY: if the provision were struck from the bill, would the rest
   still function? If striking it breaks other provisions, it is part of a
   larger proposition.
2. STANDALONE SENSE: could a one-sentence description of the provision be
   understood as a policy on its own ("data brokers must register with the
   AG annually")? Definitions, effective dates, severability clauses, and
   appropriations that merely fund another provision fail this test and
   attach to the substantive proposition they serve.
3. GRAIN LIMIT: enforcement provisions (penalties, AG authority, private
   rights of action) are separate propositions only when the bill treats
   them separately or when companion bills differ on exactly that point;
   otherwise they attach to the duty they enforce.

Propositions are identified across bills, not within one bill: two bills
proposing the same smallest change carry the same proposition ID.
Whether two provisions are "the same" proposition: same legal mechanism
aimed at the same target (not merely the same goal).
A stricter and a weaker version of the same mechanism are the same
proposition (the difference is recorded on the bill-proposition edge);
a different mechanism for the same goal is a different proposition.

IDs are `P-NNN` (persistent, never reused; retired IDs stay retired).
The proposition table is hand-authored analysis stored as data in
`scripts/atoms.py`, compiled and validated by `scripts/06_compile_atoms.py`;
every bill-proposition assignment cites the section(s) of the bill text
that ground it.

## Domain definition

A filing is IN the domain of consumer data privacy when at least one of its
provisions would change Massachusetts law governing the collection, use,
retention, disclosure, sale, or protection of information about an identified
or identifiable natural person, where that information is held or handled by
a party other than that person (a business, a data broker, a platform, a
government agency acting as a data holder, or another individual).

Included subdomains:

- comprehensive consumer data privacy regimes (controller/processor duties,
  consumer rights, opt-outs, private rights of action)
- data broker registration and regulation
- biometric identifiers and facial recognition
- location information, including location shields and geofencing
- genetic and health data privacy, including reproductive-health data
- children's and students' online data and social media data practices
- browsing, search, and telematics data
- data security and breach notification obligations
- government acquisition of personal data held by commercial parties
  (location shield acts, warrant standards for stored communications and
  browsing data, carrier location disclosure)
- privacy of images of a person (nonconsensual image distribution) ONLY when
  the mechanism is a data-handling rule; criminal harassment provisions
  without a data-handling rule are excluded
- government surveillance of individuals through data-generating technology
  (facial recognition, ALPR data, police drone data rules)
- restrictions on disclosure of personal information held in government
  records (911 recordings, lottery winners, victim compensation records,
  firearm licensee information)

Excluded, with the boundary rationale:

- wiretap/interception statutes (c.272 s.99 amendments, warrant length,
  recording defenses): real-time interception authority is treated as
  criminal procedure, a separate domain.
  The line drawn: access to STORED commercial data about a person is IN
  (location shield, H1653/S27); authority to INTERCEPT communications in
  real time is OUT.
  Excluded bills: H73, H1722, H1786, S1075, S1093, S1128, S1141.
- forensic DNA (database expansion, familial search, DNA exceptions to
  limitation periods): criminal-procedure use of biometric material, not
  data-handling rules for consumers
- consumer reporting regulation (credit reports in housing or employment):
  consumer-finance domain; the mechanism is anti-discrimination or credit
  regulation, not data privacy (mortgage trigger-lead bills stay IN because
  their mechanism is the sale of application data)
- right-to-repair telematics: expands data ACCESS for repair-market
  competition rather than protecting personal data
- physical or visual privacy without a data-handling rule (video
  surveillance of neighbors, drone peeping offenses, nursing-home dignity)

- pure cybersecurity of state systems with no individual-rights provision
  (infrastructure hardening, IT funding)
- artificial intelligence regulation UNLESS the provision governs personal
  data as defined above
- open-meeting or public-records law (transparency of government, not
  privacy of individuals' data), except provisions restricting disclosure of
  personal information held in public records
- financial reporting, "data" in the sense of statistics or program metrics
- identity-document rules (licenses, IDs) without a data-handling provision
- sick-leave banks, land takings, and other named-individual acts

## Census universe

- Source: `/api/GeneralCourts/193/Documents` on malegislature.gov,
  fetched 2026-08-04; 10,156 documents, of which 8,183 carry a bill number
  (bills, resolves, orders) and 1,973 are docket-book-only entries.
- Enacted-vehicle universe: `/api/SessionLaws/2023` and `/2024`,
  464 chapters, full text scanned, so budget outside sections are covered.

## Candidate-generation rules (recall net)

A document enters the candidate pool if any of:

1. Title matches a DOMAIN term regex (see `scripts/01_census.py`,
   `DOMAIN_TERMS`).
2. Title matches a BROAD term regex (`BROAD_TERMS`); these are kept only if
   full-text scan (`scripts/02_textscan.py`) finds domain text terms.
3. The document appears in the reported-out or before-committee list of the
   Joint Committee on Advanced Information Technology, the Internet and
   Cybersecurity (J33), regardless of title.

Known recall limitation: a bill whose title contains none of the broad terms,
that was never referred to J33, and whose privacy content appears only in its
text, is invisible to this net.
The enacted-vehicle sweep closes this gap for anything that became law; for
bills that died, the gap is real and is reported in the memo's limitations.

## Inclusion decision

Every candidate receives an explicit decision (include / exclude) with a
reason code, produced by `scripts/04_inclusion.py` and reviewed at the
census checkpoint. Reason codes:

- `IN-TITLE`: domain title term plus confirming text evidence
- `IN-TEXT`: broad-net title, domain confirmed in full text
- `IN-COMMITTEE`: J33 referral plus confirming text evidence
- `EX-FALSEPOS`: matched term used in a non-domain sense (for example
  "tracking" of prescription drug prices, "data" as program statistics)
- `EX-ADJACENT`: genuinely about information/technology but outside the
  domain definition above (with subcategory noted)
- `EX-NOBILL`: docket-book-only entry that never received a bill number;
  counted separately, text unavailable through the bill API
- `EX-PROCEDURAL`: committee extension orders and statutory annual reports
  (for example the district attorneys' wiretap reports), which are filings
  but not proposed legislation

After the first pass, a vocabulary audit of all 10,156 titles added five
speculative term groups (license plate reader, drone/unmanned, credit
report, right to repair, deepfake) to the broad net so their relevance could
be settled from bill text rather than assumption; the resulting decisions
are recorded in `scripts/04_inclusion.py` OVERRIDES with per-bill notes.
Every override entry names its reason code and a one-line justification;
the auto rule handled the unambiguous cases (38 includes, all strong-term,
and the no-evidence excludes).
