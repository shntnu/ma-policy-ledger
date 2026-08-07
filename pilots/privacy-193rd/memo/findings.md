# Findings memo: consumer data privacy in the 193rd General Court (2023-2024)

## The question

Does "the legislature passes almost nothing" survive when you count policy ideas instead of bills?
For this domain and session: yes.
Of 295 distinct policy propositions, 17 became law (5.8%); of 143 in-domain filings, 8 were enacted, and none of those eight was a standalone privacy bill: six were omnibus, budget, or conference vehicles and two were transportation acts carrying camera-data rules.

## What was measured

The census is a full-text screen of the complete corpus: 8,178 of the 8,183 numbered filings of the 193rd General Court were full-text screened (the five with no recoverable text are recorded in `data/unscanned_bills.csv`) (https://malegislature.gov/api/GeneralCourts/193/Documents), and every filing with a domain-term hit received an explicit decision with a reason code (`data/census.csv` accounts for 1,001 candidate filings).
On the enacted side the universe is the official session-law index rather than the API feed: 497 chapters (2023 Acts 1-89, 2024 Acts 1-407, and the single 2024 Resolve, https://malegislature.gov/Laws/SessionLaws/Acts/2024), every one of them obtained and full-text scanned, and every flagged chapter carries row-level verdicts (`data/acts_index.csv` is the chapter-by-chapter coverage record; `data/enacted_adjudication.csv` carries 54 row-level verdicts across 25 chapters).
This matters because `/api/SessionLaws/2024` returns only 374 of the 407 Acts chapters the official index lists, and one of the 33 it omits - Chapter 399 - is in-domain.
Enacted chapters' origin bills, including budget vehicles carrying outside sections, are census units, so ideas that entered law without a standalone filing are counted.
The 143 in-domain filings were atomized into 295 propositions on 689 bill-proposition edges, each citing its bill section and carrying an identity-basis label; a 901-edge link graph connects redrafts, consolidations, study orders, text-identical filings, and absorptions into enacted vehicles; 134 items sit in `data/verification_queue.csv` (124 inferred links with verbatim side-by-side excerpts, plus 10 judgment flags).
Every excerpt in that queue, and every quote in the analyst's quote table, is checked by `scripts/09_checks.py` against the cached text of the bill it is attributed to.

## The answer

**Seventeen of 295 propositions became law, through eight enacted vehicles - none a standalone privacy bill.** Fifteen passed through their own official chains (`enacted_as_filed`):

1. The ban on nonconsensual distribution of identifiable intimate imagery, including deepfakes, and its court-record confidentiality rule (P-266, P-280), via the abuse-prevention conference vehicle H4744, 2024 c.118 s.6 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter118).
2. The notary personal-information use/sale restriction (P-291), carried through the FY23 supplemental budget chain (H57/S24/H3548/S23 -> H58), 2023 c.2 s.33 (https://malegislature.gov/Laws/SessionLaws/Acts/2023/Chapter2); the standalone bills H1525/S943 died in committee.
3. Eviction-record sealing and the sealed-record consumer-reporting duties (P-295, P-296), filed as the HOMES bills and carried by the Affordable Homes lineage H4138 -> H4707 -> H4726 -> H4977, 2024 c.150 ss.28/52 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter150). The House prints struck the sealing regime and the Senate text (S2834 SECTION 48) restored it before enactment; the independent HOMES filings H1690, S956 and their redraft H4356 died with no chain to H4977.
4. Four bus-camera data rules - public-records exemption, litigation limits, the occupant-identification limit, and vendor confidentiality (P-299, P-300, P-380, P-302) - plus the duty to redact occupants from a photograph before a notice of violation issues (P-381), via S2884, 2024 c.363 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter363).
5. Four school-bus-camera data rules - the occupant-identification limit, the municipal-ownership/vendor-use restriction, the 30-day/1-year destruction regime with annual attestation, and the court-order-only access rule (P-380, P-302, P-379, P-371) - via the H3306/H3336/H3375/H3440 -> H4450 -> H4940 chain, whose text the Senate replaced with S3005 before enactment as 2024 c.399 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter399). P-380 and P-302 are the two propositions that reached the statute book through two independent vehicles, c.363 and c.399.
6. The TNC trip-data reporting mandate and its confidentiality rules (P-303, P-304), enacted through the FY24 closeout supplemental chain (S2888 -> S2891 -> H4799), 2024 c.206 s.15 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter206); four standalone filings carrying the same regime (S666, H1099, H1158, S627) died in committee.
7. The SFI personal-contact withholding expansion (P-294), carried through the December 2024 supplemental chain (H5049/H5132 -> H5077), 2024 c.248 s.27 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter248); the weaker standalone H2991 died in committee.

Two were absorbed into an unrelated enacted vehicle after their filed carrier died (`enacted_other_vehicle`):

8. The agency demographic-data standard and its PII-confidentiality rule (P-297, P-298), filed as H3003, enacted in the FY24 budget, 2023 c.28 s.7 (https://malegislature.gov/Laws/SessionLaws/Acts/2023/Chapter28).

The other 278 propositions died, and the anatomy of those deaths is the finding:

1. **No proposition was rejected on the record.** No proposition was defeated by any recorded vote; every roll call recorded on a census proposition was favorable.
   The census bills' histories contain two adverse roll calls, and neither fell on a bill's own question: a procedural motion in the FY24 budget vehicle H4040, "Motion to suspend Rule 40 rejected - 25 YEAS to 132 NAYS (See YEA and NAY No. 31)" (https://malegislature.gov/Bills/193/H4040), and S2834 Amendment 25, titled in its official record "MBTA Communities Act - Zoning Appeal", rejected 6-34 (Roll Call #194, https://malegislature.gov/api/GeneralCourts/193/Documents/S2834/Branches/Senate/Amendments/25/), which carried no privacy proposition.
2. **The modal fate is silence.** 144 propositions (49%) died with no recorded action; 134 (45%) were sent to study through study orders whose own fetched histories (`data/study_order_status.csv`) end discharged to Rules with no further action.
   For all 278, the record offers no public explanation.
3. **The process did real work, then discarded most of it.** 126 propositions (43%) cleared a policy committee in at least one vehicle; 49 (17%) were dropped during official consolidations - present in parent bills, absent from the redraft - with the merger recorded but the drops never explained.
   The two omnibus consumer-privacy consolidations died in Ways and Means without a vote: H4632, absorbing five bills, in House Ways and Means, and S2539, absorbing thirteen, in Senate Ways and Means (https://malegislature.gov/Bills/193/H4632). Consolidation as such was not fatal, and the memo's own enacted list shows why: of the nine census redrafts absorbing two or more parents, H4115 (eight parents) became 2024 c.118 and H4450 (five parents) became 2024 c.399, while H4266 and H4356 never reached Ways and Means at all and died after a second reading.
4. **What passed traveled around the privacy pipeline, not through it.** The dedicated privacy regimes - comprehensive consumer-data acts, biometric acts, location shields, breach modernization - all died.
   What reached the Governor rode in an abuse-prevention conference report, a housing act, two camera-enforcement transportation acts, and four budget bills; every enacted proposition has filed carriers, and for thirteen of the seventeen a standalone filing of the same proposition had already died when the idea passed inside a vehicle.

Where ideas stall: 0 propositions never got a hearing; 169 stalled in policy committee (83 heard only, 86 with repeated reporting extensions); 97 cleared committee and stalled afterward, overwhelmingly in Ways and Means; 12 got further (a second reading, eleven in a second branch incl. one full House passage at 159-0); 17 were enacted.

## Limitations

- One domain, one session; the 5.8% rate may not generalize.
- The census is a full-text term screen (privacy, data, confidentiality, nondisclosure, and public-record-exclusion language): a filing touching the domain only in language outside that set would still be missed.
  The enacted side does not rely on that screen alone - Chapter 399 regulates camera images without using a single screen term, and is in the ledger because the signature probe and the enacted-origin feedback loop found it independently - but the same blind spot on the filed side is real, and each widening of the term set has so far admitted at least one more filing (H3524 this pass).
  Five bills have no recoverable text and are recorded in `data/unscanned_bills.csv`.
- The domain boundary excludes program-incident data clauses (confidentiality boilerplate attached to registries, compacts, review boards, benefit programs) symmetrically on both the filed and enacted sides; every such verdict is recorded row-level (511 filed-side triage verdicts in `scripts/corpus_triage_verdicts.csv`, enacted-side in `data/enacted_adjudication.csv`), and the closest calls are queued.
- 84 cross-bill proposition-identity claims rest on analytic judgment rather than text-identity or official lineage; each is queued with verbatim side-by-side quotes.
- `enacted_as_filed` follows an official successor chain even where an intermediate print does not carry the proposition, which is how the eviction-sealing regime is classified; the codebook states the rule and the alternative reading.
- 1,973 docket-book-only filings have no retrievable text through the bill API and are accounted for but not atomizable.
- "Sent to study" is treated as terminal because every study order's fetched history ends without further action on any privacy matter.

## Scaling to all 8,000+ bills

This pilot ended up fetching and screening the full corpus anyway, so the marginal cost of whole-court coverage is now the judgment layers only: domain boundaries, atomization (~2.1 propositions per in-domain bill), cross-bill identity, and row-level adjudication of every enacted chapter - the step that repeatedly proved indispensable, since enacted privacy provisions travel in vehicles whose titles say nothing about privacy (an abuse-prevention act, a housing act, two camera-enforcement acts, four budgets).
The enacted side also needs its universe enumerated from the official index rather than the API, which silently omits 33 of 2024's 407 chapters.
A full-court design: (1) the mechanical bill-level fate ledger for all 8,183 filings, nearly free from the cached corpus; (2) domain-by-domain atomization with two-reader verification queues; (3) the full-text screen, the signature probe, and the enacted-origin feedback loop as three independent recall guarantees.

Dataset: `data/propositions.csv`, `data/bill_propositions.csv`, `data/links.csv`, `data/proposition_fates.csv`, `data/bill_fates.csv`, `data/census.csv`, `data/acts_index.csv`, `data/enacted_adjudication.csv`, `data/study_order_status.csv`.
Definitions and revision log: `memo/codebook.md`.
Review queue: `data/verification_queue.csv`.
Checks: `scripts/09_checks.py`.
