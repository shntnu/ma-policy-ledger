# Findings memo: consumer data privacy in the 193rd General Court (2023-2024)

## The question

Does "the legislature passes almost nothing" survive when you count policy ideas instead of bills?
For this domain and session: yes.
Of 274 distinct policy propositions, 14 became law (5.1%); of 131 in-domain filings, 7 were enacted, and every one of those seven was an omnibus, budget, or conference vehicle rather than a standalone privacy bill.

## What was measured

The census is a full-text screen of the complete corpus: all 8,183 numbered filings of the 193rd General Court were fetched and scanned (https://malegislature.gov/api/GeneralCourts/193/Documents), every filing with a domain-term hit received an explicit decision with a reason code, and all 464 session laws of 2023-2024 were full-text scanned, and every flagged chapter was adjudicated provision-by-provision (`data/census.csv` accounts for 977 candidate filings; `data/enacted_adjudication.csv` carries the row-level verdicts for every chapter flagged by either enacted-side search).
Enacted chapters' origin bills - including budget vehicles carrying outside sections - are census units, so ideas that entered law without a standalone filing are counted.
The 131 in-domain filings were atomized into 274 propositions on 638 bill-proposition edges, each citing its bill section and carrying an identity-basis label; an 813-edge link graph connects redrafts, consolidations, study orders, text-identical filings, and absorptions into enacted vehicles; 138 items sit in `data/verification_queue.csv` (128 inferred links with verbatim side-by-side excerpts, plus 10 judgment flags).

## The answer

**Fourteen of 274 propositions became law, through seven enacted vehicles - none a standalone privacy bill.** Ten passed through their own official chains (`enacted_as_filed`):

1. The ban on nonconsensual distribution of identifiable intimate imagery, including deepfakes, and its court-record confidentiality rule (P-266, P-280), via the abuse-prevention conference vehicle H4744, 2024 c.118 s.6 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter118).
2. The notary personal-information use/sale restriction (P-291), carried through the FY23 supplemental budget chain (H57/S24/H3548/S23 -> H58), 2023 c.2 s.33 (https://malegislature.gov/Laws/SessionLaws/Acts/2023/Chapter2); the standalone bills H1525/S943 died in committee.
3. Four bus-camera data rules - public-records exemption, litigation limits, occupant-identification ban with mandatory redaction, vendor confidentiality (P-299..P-302) - via S2884, 2024 c.363 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter363); six other filings proposing the same camera-data regime died.
4. The TNC trip-data reporting mandate and its confidentiality rules (P-303, P-304), enacted through the FY24 closeout supplemental chain (S2888 -> S2891 -> H4799), 2024 c.206 s.15 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter206); four standalone filings carrying the same regime (S666, H1099, H1158, S627) died in committee.
5. The SFI personal-contact withholding expansion (P-294), carried through the December 2024 supplemental chain (H5049/H5132 -> H5077), 2024 c.248 s.27 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter248); the weaker standalone H2991 died in committee.

Four were absorbed into unrelated enacted vehicles after their filed carriers died (`enacted_other_vehicle`):

6. Eviction-record sealing and the sealed-record consumer-reporting duties (P-295, P-296), filed as the HOMES bills, enacted inside the Affordable Homes Act, 2024 c.150 ss.28/52 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter150).
7. The agency demographic-data standard and its PII-confidentiality rule (P-297, P-298), filed as H3003, enacted in the FY24 budget, 2023 c.28 s.7 (https://malegislature.gov/Laws/SessionLaws/Acts/2023/Chapter28).

The other 260 propositions died, and the anatomy of those deaths is the finding:

1. **Nothing was rejected on the record.** No proposition was defeated by any recorded vote; every roll call in the census was in favor.
2. **The modal fate is silence.** 141 propositions (51%) died with no recorded action; 119 (43%) were sent to study through study orders whose own fetched histories (`data/study_order_status.csv`) end discharged to Rules with no further action.
   For all 260, the record offers no public explanation.
3. **The process did real work, then discarded most of it.** 119 propositions (43%) cleared a policy committee in at least one vehicle; 50 (18%) were dropped during official consolidations - present in parent bills, absent from the redraft - with the merger recorded but the drops never explained.
   Every consolidated privacy vehicle (H4632 absorbing five bills, S2539 absorbing thirteen) died in Ways and Means without a vote (https://malegislature.gov/Bills/193/H4632).
4. **What passed traveled around the privacy pipeline, not through it.** The dedicated privacy regimes - comprehensive consumer-data acts, biometric acts, location shields, breach modernization - all died.
   What reached the Governor rode in an abuse-prevention conference report, a housing act, a bus-lane act, and four budget bills; several of those vehicles enacted ideas whose standalone filings had already died in committee, and one enacted an idea never filed at all.

Where ideas stall: 11 propositions never got a hearing; 144 stalled in policy committee (62 heard only, 82 with repeated reporting extensions); 93 cleared committee and stalled afterward, overwhelmingly in Ways and Means; 12 got further (a second reading, eleven in a second branch incl. one full House passage at 159-0); 14 were enacted.

## Limitations

- One domain, one session; the 5.1% rate may not generalize.
- The census is a full-text term screen (privacy, data, confidentiality, nondisclosure, and public-record-exclusion language): a filing touching the domain only in language outside that set would still be missed, though the enacted-origin loop guarantees recall for anything that became law.
  Five bills have no recoverable text and are recorded in `data/unscanned_bills.csv`.
- The domain boundary excludes program-incident data clauses (confidentiality boilerplate attached to registries, compacts, review boards, benefit programs) symmetrically on both the filed and enacted sides; every such verdict is recorded row-level (493 filed-side triage verdicts in `scripts/corpus_triage_verdicts.csv`, enacted-side in `data/enacted_adjudication.csv`), and the closest calls are queued.
- 88 cross-bill proposition-identity claims rest on analytic judgment rather than text-identity or official lineage; each is queued with verbatim side-by-side quotes.
- 1,973 docket-book-only filings have no retrievable text through the bill API and are accounted for but not atomizable.
- "Sent to study" is treated as terminal because every study order's fetched history ends without further action on any privacy matter.

## Scaling to all 8,000+ bills

This pilot ended up fetching and screening the full corpus anyway, so the marginal cost of whole-court coverage is now the judgment layers only: domain boundaries, atomization (~2.1 propositions per in-domain bill), cross-bill identity, and row-level adjudication of every enacted chapter - the step that repeatedly proved indispensable, since enacted privacy provisions travel in vehicles whose titles say nothing about privacy (an abuse-prevention act, a housing act, a bus-lane act, four budgets).
A full-court design: (1) the mechanical bill-level fate ledger for all 8,183 filings, nearly free from the cached corpus; (2) domain-by-domain atomization with two-reader verification queues; (3) the full-text screen plus enacted-origin feedback loop as standing recall guarantees.

Dataset: `data/propositions.csv`, `data/bill_propositions.csv`, `data/links.csv`, `data/proposition_fates.csv`, `data/bill_fates.csv`, `data/census.csv`, `data/enacted_adjudication.csv`, `data/study_order_status.csv`.
Definitions and revision log: `memo/codebook.md`.
Review queue: `data/verification_queue.csv`.
Checks: `scripts/09_checks.py`.
