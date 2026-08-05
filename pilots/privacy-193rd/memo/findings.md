# Findings memo: consumer data privacy in the 193rd General Court (2023-2024)

## The question

Does "the legislature passes almost nothing" survive when you count ideas instead of bills?
For this domain and session: yes, and counting ideas makes the finding sharper, not softer.

## What was measured

From the 10,156 documents filed in the 193rd General Court, a documented multi-net census identified 67 in-domain filings (66 bills and 1 resolve) touching consumer data privacy.
Each was atomized into its smallest standalone policy propositions: 208 distinct propositions, carried on 435 bill-proposition assignments, every one citing the bill section that grounds it.
A link graph of 446 edges connects companions (verified by programmatic text comparison), redrafts and consolidations (from the official histories), study orders, and one budget carve-out.
All 464 session laws enacted in 2023-2024 were full-text scanned, so budget outside sections are covered.
Every claim below can be checked from the cited malegislature.gov page; the dataset is in `data/`.

## The answer

**Zero of 208 propositions became law - as filed, or through any other vehicle.** The signature-phrase sweep of every enacted chapter (`data/enacted_probe.csv`) produced 22 candidate matches; all are false positives (budget line items, an RMV identity-verification authorization, physical-security language).
The bill-level rate is likewise 0 of 67.
So the claim survives both ways of counting: for this domain-session, the passage rate is 0% at any granularity.

What idea-level counting adds is a precise anatomy of how the ideas died:

1. **Nothing was rejected on the record.** No proposition - none of 208 - was defeated by a recorded vote.
   The only roll call anywhere in the census is a unanimous one in favor: H4844, the narrowed care-location-privacy bill carved out of a supplemental budget (H4496), passed the House 159-0 on July 10, 2024 (Y&N No. 133), was referred to Senate Ways and Means on August 5, and had no further action (https://malegislature.gov/Bills/193/H4844).
2. **The modal fate is silence.** 128 propositions (62%) died with no recorded action; 80 (38%) were sent to study through twelve study orders, none of which produced any further recorded action.
   For every one of the 208, the record offers no public explanation.
3. **The process did real work, then discarded it.** 46% of propositions (95 of 208) cleared a policy committee in at least one vehicle - "reported favorably" or beyond.
   The official histories record substantial consolidation: H4632 is a new draft of five bills (both comprehensive privacy regimes plus the biometric and children's-privacy bills), S2539 absorbed thirteen cyber and breach bills, and the H4632/S2770 redraft absorbed nine-tenths of the location-shield chapter.
   All of these consolidated vehicles then died in Ways and Means without a vote.
4. **Consolidation was also where ideas quietly vanished.** 39 propositions (19%) were dropped during consolidations - present in the parent bills, absent from the official redraft - including workplace-surveillance limits, algorithmic impact assessments, and the centralized opt-out mechanism.
   The record documents the merger but never the drops.

Where ideas stall, in one line: 7 propositions never got a hearing, 106 stalled in policy committee (55 heard only, 51 with repeated reporting extensions), 93 cleared committee and stalled afterward - overwhelmingly in Ways and Means - and 2 got further (one to a second reading, one through a full House vote), and none became law.

## Limitations, honestly

- One domain, one session.
  Consumer data privacy may be atypically unproductive; the method cannot say whether 0% generalizes.
- The census recall net is documented but not perfect: a bill with no domain or broad term in its title, never referred to the Advanced IT committee, and never enacted, would be invisible.
  The enacted-vehicle sweep closes this gap for anything that became law.
- Atomization granularity is a judgment; the codebook's severability tests and the per-family notes in `memo/atomization/` make it reproducible, and 47 inferred links and judgment calls sit in `data/verification_queue.csv` for human check.
- 140 docket-book-only filings have no retrievable text through the bill API and are accounted for but not atomized.
- "Sent to study" is treated as terminal because no study order here produced further recorded action; a longer horizon could in principle revive one.

## Scaling to all 8,000+ bills

The mechanical layers scale now: the JSON API yields every document, full text, history, and committee list; terminal-action parsing (validated here against 67 histories with zero indeterminate results) would give a bill-level fate dataset for the whole session in roughly a day of throttled fetching.
The expensive layers are judgment: domain boundaries, atomization, and proposition identity across bills - here they consumed most of the effort, at roughly 3 propositions per bill and one reading pass per bill family.
A realistic full-court design: (1) publish the bill-level fate ledger for all 8,000+ filings computed mechanically; (2) atomize by domain, prioritized by stakes, with two-reader verification queues like this pilot's; (3) reuse the explicit link graph, which is fully automatable because the histories themselves record redrafts, consolidations, and study orders.
Nothing about the method requires anything beyond the public record.

Dataset: `data/propositions.csv`, `data/bill_propositions.csv`, `data/links.csv`, `data/proposition_fates.csv`, `data/bill_fates.csv`, `data/census.csv`.
Definitions: `memo/codebook.md`.
Review queue: `data/verification_queue.csv`.
