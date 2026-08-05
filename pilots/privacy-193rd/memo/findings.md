# Findings memo: consumer data privacy in the 193rd General Court (2023-2024)

Revised 2026-08-05 after external review; the original memo claimed zero enactments, which the review showed was wrong.
The correction is described honestly below and in the codebook's revision log.

## The question

Does "the legislature passes almost nothing" survive when you count ideas instead of bills?
For this domain and session: yes - the proposition-level passage rate is 1 in 214 (0.5%) - and counting ideas shows precisely how the other 213 died.

## What was measured

From the 10,156 documents filed in the 193rd General Court (https://malegislature.gov/api/GeneralCourts/193/Documents), a documented multi-net census identified 73 in-domain filings, including six admitted through an enacted-vehicle feedback loop that traces every enacted chapter's `OriginBill` back into the census (`data/census.csv`, every candidate with an explicit decision and reason code).
Each filing was atomized into its smallest standalone policy propositions: 214 propositions on 462 bill-proposition edges, each citing its bill section and carrying an identity-basis label (`data/propositions.csv`, `data/bill_propositions.csv`).
A 502-edge link graph connects redrafts, consolidations, study orders, text-identical filings, and one budget carve-out (`data/links.csv`); all 464 session laws of 2023-2024 (https://malegislature.gov/api/SessionLaws/2024) were full-text scanned so budget outside sections are covered.

## The answer

**One of 214 propositions became law.** P-266, the ban on nonconsensual distribution of identifiable intimate imagery (NDII, including deepfake "digitization"), was enacted unanimously as section 6 of 2024 Chapter 118 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter118), after the standalone filings H1745/S1012/S1139 were consolidated through H4115 and H4241 into conference vehicle H4744 (https://malegislature.gov/Bills/193/H4744). Bill-level rate: 1 of 73.
Everything else - 213 propositions - died, and the anatomy of those deaths is the finding:

1. **Nothing was rejected on the record.** No proposition was defeated by any recorded vote.
   Every roll call in the census was *in favor*: H4744's unanimous enactment votes, and H4844's 159-0 House passage (Y&N No. 133, https://malegislature.gov/Bills/193/H4844) - after which that bill, a care-location-privacy act carved out of supplemental budget H4496, died in Senate Ways and Means with no further action.
2. **The modal fate is silence.** 132 propositions (62%) died with no recorded action; 81 (38%) were sent to study through twelve study orders whose own histories (fetched and recorded as `study_order_terminal` links) show they were discharged to Rules and never acted on again.
   For all 213, the official record offers no public explanation.
3. **The process did real work, then discarded most of it.** 46% of propositions (99 of 214) cleared a policy committee in at least one vehicle.
   The histories record heavy consolidation - H4632 is officially a new draft of five bills spanning both comprehensive privacy regimes (https://malegislature.gov/Bills/193/H4632), S2539 absorbed thirteen cyber and breach bills (https://malegislature.gov/Bills/193/S2539) - and every consolidated privacy vehicle except H4744 then died in Ways and Means without a vote.
4. **Consolidation was also where ideas quietly vanished.** 40 propositions (19%) were dropped during consolidations - present in parent bills, absent from the official redraft - including workplace-surveillance limits, algorithmic impact assessments, and the centralized opt-out mechanism.
   The record documents each merger but never explains the drops.
5. **The one success followed a different route than any privacy bill.** P-266 passed inside an abuse-prevention vehicle moved by Judiciary and a conference committee, not through the privacy committee whose consolidated vehicles all stalled.

Where ideas stall: 7 propositions never got a hearing; 108 stalled in policy committee (55 heard only, 53 with repeated reporting extensions); 93 cleared committee and stalled afterward, overwhelmingly in Ways and Means; 5 got further (one second reading, four through a full House vote via H4844); 1 was enacted.

## Limitations, honestly

- One domain, one session; the 0.5% rate may not generalize.
- The original census missed the enacted NDII family because its title ("An Act to prevent abuse and exploitation") evaded every net; the feedback loop that now catches enacted vehicles cannot rescue similarly opaque bills that *died* - that recall gap remains and is the method's largest known weakness.
- The domain boundary was revised mid-study (interpersonal disclosure restrictions in, reversing a carve-out that was inconsistent with the doxing inclusion); the codebook's revision log records the change and its rationale.
- 58 cross-bill proposition-identity claims rest on analytic judgment rather than companion-diff or official lineage; they are flagged `inferred-analytic` and queued in `data/verification_queue.csv` (105 items total) with side-by-side excerpts for the kinship links.
- 140 docket-book-only filings are accounted for but have no retrievable text through the bill API.
- "Sent to study" is treated as terminal because every study order's fetched history ends discharged to Rules with no further action.

## Scaling to all 8,000+ bills

The mechanical layers scale now: the JSON API yields every document, full text, history, committee list, and each chapter's origin bill; terminal-action parsing (validated against 73 histories, zero indeterminate, deterministic by `scripts/09_checks.py`) would give a whole-session bill-level fate ledger in about a day of throttled fetching.
The judgment layers are the cost: domain boundaries, atomization (~3 propositions per bill), and cross-bill identity - and the review of this pilot showed exactly where such judgment fails without adversarial checking (the NDII miss, the bundling inconsistencies).
A full-court design should therefore ship (1) the mechanical bill-level ledger for all filings, (2) domain-by-domain atomization with two-reader verification queues, and (3) the enacted-origin feedback loop as a standing recall guarantee, since it is the only net that catches opaque titles - for enacted ideas automatically, and for dead ones only via wider human reading.

Dataset: `data/propositions.csv`, `data/bill_propositions.csv`, `data/links.csv`, `data/proposition_fates.csv`, `data/bill_fates.csv`, `data/census.csv`.
Definitions and revision log: `memo/codebook.md`.
Review queue: `data/verification_queue.csv`.
Checks: `scripts/09_checks.py`.
