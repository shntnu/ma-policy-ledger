# Findings memo: consumer data privacy in the 193rd General Court (2023-2024)

## The question

Does "the legislature passes almost nothing" survive when you count policy ideas instead of bills?
For this domain and session: yes.
The proposition-level passage rate is 6 in 223 (2.7%), the bill-level rate is 1 in 79, and every idea that passed did so inside a vehicle from outside the privacy-committee pipeline.

## What was measured

From the 10,156 documents filed in the 193rd General Court (https://malegislature.gov/api/GeneralCourts/193/Documents), a documented multi-net census identified 79 in-domain filings: title and committee nets over all filings, full-text confirmation of 325 broad-net candidates, and an enacted-vehicle feedback loop that adjudicates every enacted chapter flagged by a full-text scan of all 464 session laws of 2023-2024 (budget outside sections included) and traces in-domain provisions to their origin bills and filed lineages (`data/census.csv`, `data/enacted_adjudication.csv`).
Each filing was atomized into its smallest standalone policy propositions: 223 propositions on 494 bill-proposition edges, each citing its bill section and carrying an identity-basis label (`data/propositions.csv`, `data/bill_propositions.csv`).
A 528-edge link graph connects redrafts, consolidations, study orders, text-identical filings, and budget carve-outs (`data/links.csv`); 97 inferred links and judgment calls sit in `data/verification_queue.csv` with verbatim side-by-side excerpts.

## The answer

**Six of 223 propositions became law, in five enacted vehicles - none of them a privacy bill.**

1. The ban on nonconsensual distribution of identifiable intimate imagery, including deepfake "digitization" (P-266), and its companion court-record confidentiality rule (P-280), enacted unanimously as section 6 of 2024 c.118 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter118) after the filed bills H1745/S1012/S1139 were consolidated through H4115 and H4241 into the abuse-prevention conference vehicle H4744 (https://malegislature.gov/Bills/193/H4744).
2. Eviction-record sealing (P-290), filed as the HOMES bills H1690/S956 and their Judiciary redraft H4356, which died - and enacted anyway as sections 28 and 52 of the Affordable Homes Act, 2024 c.150 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter150).
3. The notary personal-information use/sale restriction (P-291), filed as H1525/S943, which died in committee - and enacted anyway as section 33 of the FY23 supplemental budget, 2023 c.2 (https://malegislature.gov/Laws/SessionLaws/Acts/2023/Chapter2).
4. The government-wide demographic-data collection standard with personal-information confidentiality (P-292), filed as H3003, which died - and enacted as section 7 of the FY24 budget, 2023 c.28 (https://malegislature.gov/Laws/SessionLaws/Acts/2023/Chapter28).
5. The expansion of personal contact and family information withheld from public statements of financial interests (P-294), filed in weaker form as H2991, which died - and enacted as section 27 of a December 2024 supplemental budget, 2024 c.248 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter248).

One further in-domain rule was enacted with NO filed antecedent in the domain: the TNC trip-level geolocation reporting regime with confidentiality and destruction rules (2024 c.206 s.15, https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter206). It is recorded in `data/enacted_adjudication.csv` but sits outside the filed-idea passage rate, since no filed bill proposed it.

The other 217 propositions died, and the anatomy of those deaths is the finding:

1. **Nothing was rejected on the record.** No proposition was defeated by any recorded vote.
   Every roll call in the census was *in favor*: H4744's unanimous passage and enactment votes, and H4844's 159-0 House passage (Y&N No. 133, https://malegislature.gov/Bills/193/H4844) - after which that care-location-privacy bill, itself carved out of supplemental budget H4496, died in Senate Ways and Means with no further action.
2. **The modal fate is silence.** 136 propositions (61%) died with no recorded action; 81 (36%) were sent to study through twelve study orders whose own histories (`data/study_order_status.csv`) end discharged to Rules with no further action (the one order that reported anything out, S2612, reported a jury-clerk bill with no privacy content).
   For all 217, the official record offers no public explanation.
3. **The process did real work, then discarded most of it.** 108 propositions (48%) cleared a policy committee in at least one vehicle.
   The histories record heavy consolidation - H4632 is officially a new draft of five bills spanning both comprehensive privacy regimes (https://malegislature.gov/Bills/193/H4632), and S2539 absorbed thirteen cyber and breach bills (https://malegislature.gov/Bills/193/S2539) - and every consolidated privacy vehicle died in Ways and Means without a vote.
4. **Consolidation was also where ideas quietly vanished.** 38 propositions (17%) were dropped during consolidations - present in parent bills, absent from the official redraft - including workplace-surveillance limits, algorithmic impact assessments, and the centralized opt-out mechanism.
   The record documents each merger but never explains the drops.
5. **What passed traveled around the privacy pipeline, not through it.** All five enacted vehicles were omnibus, budget, or conference acts (abuse prevention, housing, and three budget bills).
   The standalone filed versions of four of the six enacted ideas died in committee; every comprehensive privacy regime referred to the privacy-focused committees died without a floor vote.

Where ideas stall: 7 propositions never got a hearing; 108 stalled in policy committee (55 heard only, 53 with repeated reporting extensions); 93 cleared committee and stalled afterward, overwhelmingly in Ways and Means; 13 got further (second readings, one House passage, one conference); 2 were enacted through their own chain and 4 more through unrelated vehicles.

## Limitations

- One domain, one session; the 2.7% rate may not generalize.
- Opaque titles are the method's largest recall risk: the enacted-side feedback loop guarantees recall for ideas that became law, but a filed bill with a generic title that died outside the swept committees would be invisible.
  The three enacted vehicles were all found this way; dead bills have no equivalent guarantee.
- The domain boundary excludes program-incident data clauses (confidentiality boilerplate attached to registries, compacts, review boards) SYMMETRICALLY on the filed and enacted sides, because the filed census never swept program bills for such clauses; counting them on one side only would bias the rate.
  Every enacted-side exclusion under this rule is recorded row-level in `data/enacted_adjudication.csv`, and the closest judgment calls are queued for review.
- 48 cross-bill proposition-identity claims rest on analytic judgment rather than text-identity or official lineage; each is queued with verbatim side-by-side quotes.
- 140 docket-book-only filings are accounted for but have no retrievable text through the bill API.
- "Sent to study" is treated as terminal because every study order's fetched history ends without further action on any privacy matter.

## Scaling to all 8,000+ bills

The mechanical layers scale now: the JSON API yields every document, full text, history, committee list, and each chapter's origin bill; terminal-action parsing (validated against 77 histories, zero indeterminate, deterministic by `scripts/09_checks.py`) would give a whole-session bill-level fate ledger in about a day of throttled fetching.
The judgment layers are the cost: domain boundaries, atomization (~3 propositions per bill), cross-bill identity, and - the step this pilot shows is indispensable - row-level adjudication of every enacted chapter against the domain, since enacted privacy provisions travel in vehicles whose titles say nothing about privacy.
A full-court design should ship (1) the mechanical bill-level ledger for all filings, (2) domain-by-domain atomization with two-reader verification queues, and (3) the enacted-origin feedback loop as a standing recall guarantee for whatever becomes law.

Dataset: `data/propositions.csv`, `data/bill_propositions.csv`, `data/links.csv`, `data/proposition_fates.csv`, `data/bill_fates.csv`, `data/census.csv`, `data/enacted_adjudication.csv`.
Definitions and revision log: `memo/codebook.md`.
Review queue: `data/verification_queue.csv`.
Checks: `scripts/09_checks.py`.
