# Atomization working notes: comprehensive MDPPA family

Reading pass over cached bill texts (scripts/billtext.py); companion diffs
verified programmatically. Consolidated into scripts/atoms.py after
cross-checking. Quotes are verbatim from cached text.

All four texts read in full. Companion verification and atomization below.

## COMPANION VERIFICATION

- H83 vs S25: substantively identical word-for-word (whole-text diff after normalization). Only differences: cited Official Edition (2018 vs 2020) and S25 uses numbered subsection format ((1), (i)...) where H83 uses unnumbered lists. Same section numbering throughout, including duplicate "Section 11" (Data Brokers and Civil Rights both numbered 11).
- H4632 vs S2770: substantively identical word-for-word. Only differences: chapter title (H4632 "Chapter 93M. Massachusetts Data Privacy Act"; S2770 "Chapter 93M. Massachusetts Data Privacy Protection Act") and one stray numbering artifact.
- Structural relationship: H83/S25 = proposed c.93L (MDPPA) + c.149 s.204 (workplace surveillance). H4632/S2770 = proposed c.93M (comprehensive privacy) + NEW proposed c.93N (location information chapter, near-verbatim from the filed location bills H357/S148 lineage). The redrafts drop workplace surveillance, algorithmic impact assessments, the OCABR centralized opt-out, privacy/security officers, large-data-holder PIAs, legal-request transparency reports, and the s.230 carve-out; they add profiling opt-out, authorized agents/opt-out preference signals, and the c.93N location chapter.

---

## BILL H83 (= S25) — "Massachusetts Data Privacy Protection Act": comprehensive consumer data privacy regime plus workplace surveillance limits

(Section cites are to proposed c.93L unless noted. S25 is identical; same section numbers.)

1. `data-minimization-duty-of-loyalty` — Covered entities may collect/process/transfer covered data only as reasonably necessary and proportionate to 14 enumerated permissible purposes (incl. a civic-engagement/democratic-governance purpose), with limited secondary-processing purposes incl. first-party ads and targeted ads. — Sec. 2. — "limited to what is reasonably necessary and proportionate to carry out one of the following purposes"
2. `dark-pattern-ban` — Prohibits deceptive statements and manipulated user interfaces to induce sign-up, obtain consent, or condition exercise of rights. — Secs. 2(c), 4(c), 8(b), 9(e). — "manipulation of any user interface with the purpose or substantial effect of obscuring, subverting, or impairing"
3. `ssn-restrictions` — Bars collection/processing/transfer of Social Security numbers except for credit, authentication, fraud, tax, contract-enforcement uses. — Sec. 3(1). — "collect, process, or transfer a Social Security number, except when necessary"
4. `sensitive-data-strict-necessity` — Sensitive covered data (broadly defined: location, biometric, genetic, health, minors' data, browsing across sites, etc.) may be collected/processed only when strictly necessary for a requested product or enumerated purposes. — Secs. 1 (definition), 3(2). — "except where such collection or processing is strictly necessary to provide or maintain a specific product or service"
5. `sensitive-data-transfer-consent` — Third-party transfer of sensitive data requires prior affirmative express consent per transfer, with narrow exceptions (legal obligation, imminent injury, password managers, genetic-medical, mergers). — Sec. 3(3). — "pursuant to the affirmative express consent of the individual, given before each specific transfer"
6. `sensitive-data-targeted-ads-ban` — Flat ban on processing sensitive covered data for targeted advertising. — Sec. 3(4). — "process sensitive covered data for purposes of targeted advertising"
7. `consent-request-standards` — Standalone, understandable, accessible consent requests; symmetry (refusal as easy as acceptance); no consent from inaction or continued use; new consent for new purposes. — Sec. 4. — "shall not infer that an individual has provided affirmative express consent... from the inaction of the individual"
8. `privacy-by-design` — Duty to maintain reasonable policies/practices mitigating privacy risks (incl. minors), scaled to entity size, data sensitivity, and volume. — Sec. 5. — "establish, implement, and maintain reasonable policies, practices, and procedures"
9. `anti-retaliation-pricing` — No retaliation (denial, price/quality differences) for exercising rights or refusing collection; bona fide loyalty-program exception with data-sale limits; no unjust/coercive pricing. — Sec. 6. — "may not retaliate against an individual for:— exercising any of the rights guaranteed by this chapter"
10. `privacy-policy-transparency` — Public, accessible privacy policy with categories, purposes, transferees, data brokers by name, retention; material-change notice; large data holders: 10-year policy archive/change log and 500-word short-form notice. — Sec. 7. — "a detailed and accurate representation of the data collection, processing, and transfer activities"
11. `individual-data-rights` — Rights to access (24-month lookback), correct, delete, and export (portable, machine-readable), 30-day response +20-day extension, two free requests/year, verification and enumerated denial grounds (incl. private schools exception). — Sec. 8. — "access... correct any verifiable substantial inaccuracy... delete covered data... export to the individual"
12. `opt-out-rights-transfers-ads` — Rights to withdraw consent (as easy as giving it), opt out of third-party data transfers, opt out of targeted advertising; third parties must honor forwarded opt-outs. — Sec. 9. — "may not transfer or direct the transfer of the covered data of an individual to a third party if the individual objects"
13. `minors-targeted-ads-ban` — No targeted advertising with knowledge (tiered knowledge standard) the individual is under 18. — Sec. 10; knowledge def. Sec. 1. — "may not engage in targeted advertising to any individual if the covered entity has knowledge that the individual is a covered minor"
14. `data-broker-registration` — Data broker website notice, annual OCABR registration ($100 fee), public searchable registry; dedicated penalties ($100/day to $10,000/yr plus back fees). — Sec. 11 (Data Brokers). — "data brokers shall register with the OCABR in accordance with this subsection"
15. `civil-rights-nondiscrimination` — Ban on collecting/processing/transferring data in a manner that discriminates (disparate impact) on race, color, religion, national origin, sex, sexual orientation, gender identity, disability; AG enforcement plus annual legislative report. — Sec. 11 (Civil rights) (a)-(c). — "discriminates in or otherwise makes unavailable the equal enjoyment of goods or services"
16. `algorithm-impact-assessments` — Large data holders using covered algorithms posing consequential risk must conduct annual impact assessments; developers must conduct pre-deployment design evaluations; filed with AG within 30 days; public summaries. — Sec. 11 (Civil rights) (d). — "shall conduct an impact assessment of such algorithm in accordance with paragraph (1)"
17. `centralized-opt-out-mechanism` — OCABR must establish or recognize centralized privacy-protective opt-out mechanisms within 18 months (universal opt-out infrastructure). — Sec. 12(a)-(b). — "establish or recognize one or more acceptable privacy protective, centralized mechanisms"
18. `privacy-security-officers` — Non-small-business entities must designate privacy officer(s) and data security officer(s) implementing privacy/security programs. — Sec. 12(c)-(d). — "1 or more qualified employees as privacy officers; and 1 or more qualified employees as data security officers"
19. `large-holder-privacy-impact-assessment` — Large data holders: biennial privacy impact assessment weighing benefits vs. adverse consequences, approved by privacy officer. — Sec. 12(e)-(g). — "shall conduct a privacy impact assessment that weighs the benefits"
20. `service-provider-third-party-duties` — Service providers bound to covered-entity instructions via mandatory contracts; assistance with rights requests; deletion/return at end of service; 93H safeguards; third parties limited to consented/disclosed purposes. — Sec. 13. — "shall adhere to the instructions of a covered entity and only collect, process, and transfer service provider data"
21. `private-right-of-action` — PRA against covered entities that are not small businesses; liquidated damages >= 0.15% global revenue or $15,000/violation, punitive damages, fees; anti-arbitration/anti-waiver. — Secs. 14(a)-(e), 15(a). — "liquidated damages of not less than 0.15% of the annual global revenue... or $15,000 per violation"
22. `ag-enforcement-penalties` — AG action under c.93A s.4; penalties >= 0.15%/$15,000 per violation up to 4% global revenue/$20,000,000 per action; awards earmarked to affected individuals; multi-factor penalty calculus. — Sec. 14. — "not more than 4% of the annual global revenue... or $20,000,000, whichever is greater"
23. `complaint-retaliation-ban` — Unlawful to retaliate against an individual for a good-faith compliance complaint; separate civil action. — Sec. 14 (final paragraphs). — "to retaliate against an individual who makes a good-faith complaint"
24. `legal-request-transparency-reports` — Covered entities receiving legal requests (warrants, orders, subpoenas) must publish bi-monthly aggregate reports to AG and public, incl. location/biometric request counts. — Sec. 16. — "provide the Attorney General and the general public a bi-monthly report"
25. `interactive-computer-service-carveout` — s.230-style: interactive computer services not treated as publisher/speaker of user-provided personal information; hosting alone is not processing. — Sec. 15(b). — "shall be treated as the publisher or speaker of any personal information provided by another"
26. `workplace-surveillance-limits` — c.149 s.204: employer electronic monitoring only for enumerated purposes, least-invasive/fewest-employees/least-data; prohibits off-duty, private-area monitoring and facial recognition except identity verification; specific advance notice (filed with DLS); employment decisions cannot rest solely on monitoring data (access, correction, corroboration required); no compelled apps/wearables. — SECTION 2 (c.149 s.204). — "shall not electronically monitor an employee unless... the least invasive means that could reasonably be used"

(Effective date: 12 months post-enactment, enforcement delayed further 6 months — SECTION 3; attaches to all. Non-applicability: HIPAA-treatment data, interpersonal contact info — Sec. 17; attaches to scope.)

## BILL S25 — "Massachusetts Data Privacy Protection Act" (Senate companion)

Same subject; propositions 1-26 identical to H83, same section numbers (SECTION 1 c.93L Secs. 1-20; SECTION 2 c.149 s.204; SECTION 3 effective date). No substantive deltas found.

## BILL H4632 (= S2770) — "Massachusetts Data Privacy Act" (House committee redraft): comprehensive consumer privacy regime (c.93M) plus location-information privacy chapter (c.93N)

(Cites to proposed c.93M unless noted.)

1. `data-minimization-duty-of-loyalty` — Same mechanism; 13 permissible purposes — civic-engagement purpose DROPPED; secondary-processing list drops explicit "targeted advertising" item, keeping first-party advertising to non-minors. — Sec. 2. — "limited to what is reasonably necessary and proportionate to carry out one of the following purposes"
2. `dark-pattern-ban` — Same mechanism, now with defined term "dark pattern or deceptive design" (incl. anything FTC calls a dark pattern); applied to sign-up, consent, rights, opt-outs. — Secs. 1(a)(10), 2(c), 4(b), 5(c), 10(f). — "any practice the Federal Trade Commission refers to as a 'dark pattern'"
3. `ssn-restrictions` — Identical. — Sec. 3(a)(1). — "collect, process, or transfer a Social Security number, except when necessary"
4. `sensitive-data-strict-necessity` — Same mechanism; "sensitive covered data" definition expanded (adds military service, crime-victim status, pregnancy incl. lactation, reproductive-health purchases incl. contraceptives/abortifacients, philosophical beliefs); "consent" replaces "affirmative express consent". — Secs. 1(a)(29), 3(a)(2). — "strictly necessary to provide or maintain a specific product or service requested by the individual"
5. `sensitive-data-transfer-consent` — Same mechanism, per-transfer consent. — Sec. 3(a)(3). — "pursuant to the consent of the individual, given before each specific transfer takes place"
6. `sensitive-data-targeted-ads-ban` — Identical. — Sec. 3(a)(4). — "process sensitive covered data for the purposes of targeted advertising"
7. `consent-request-standards` — Same mechanism plus additions: request displayed at/before point of collection; must be accompanied by privacy policy (and LDH short form); cannot condition/limit account access. — Sec. 5. — "The request for consent must be displayed at or before the point of collection"
8. `privacy-by-design` — Same mechanism plus explicit retention-schedule evaluation duty. — Sec. 6(a)(4). — "evaluate the length of time that covered data shall be retained"
9. `anti-retaliation-pricing` — Essentially identical to filed. — Sec. 7. — "may not retaliate against an individual for: exercising any of the rights guaranteed"
10. `privacy-policy-transparency` — Same mechanism plus: must be on "homepage"; SEPARATE stand-alone biometric-data privacy policy; SEPARATE precise-geolocation privacy policy. — Sec. 9, esp. (i)-(j). — "shall provide a separate privacy policy detailing the collection, processing, and transfer of such biometric data"
11. `individual-data-rights` — Same rights; lookback cut 24 to 12 months; response window 30 to 45 days; private-school deletion exception replaced by FCRA consumer-reporting-agency exception; request mechanisms co-located with privacy policy. — Sec. 4. — "each request under subsection (a) shall be completed within 45 days"
12. `opt-out-rights-transfers-ads` — Same mechanism (withdraw consent, opt out of transfers and targeted ads, third-party pass-through); adds commercially-reasonable-timeframe compliance, good-faith liability shield for forwarding entity, loyalty-program conflict/opt-back-in procedure, no forced account creation. — Sec. 10(a)-(c), (e)-(j). — "may not transfer or direct the transfer of the covered data of an individual to a third party if the individual... objects"
13. `profiling-opt-out` — NEW: right to opt out of profiling in furtherance of automated decisions producing legal or similarly significant effects. — Secs. 1(a)(26), 10(d). — "profiling in furtherance of automated decisions that produce legal or similarly significant effects"
14. `authorized-agents-opt-out-signals` — NEW: rights exercisable through authorized agents designated by technological means incl. browser setting/extension or global device setting (opt-out preference signals); parents/guardians act for children; guardians/conservators for protected persons. — Sec. 15. — "an Internet link or a browser setting, browser extension or global device setting"
15. `minors-targeted-ads-ban` — Identical mechanism (minor = under 18; same tiered knowledge standard). — Secs. 1(a)(18), 16. — "may not engage in targeted advertising to any individual if the covered entity has knowledge that the individual is a minor"
16. `data-broker-registration` — Same notice + OCABR registration ($100) + public registry; dedicated dollar penalties replaced by general Sec. 12 enforcement; AG rulemaking to further define data brokers. — Secs. 17, 14(a)(4). — "data brokers shall register with the OCABR in accordance with this subsection"
17. `civil-rights-nondiscrimination` — Same mechanism; protected classes expanded to add genetic information, pregnancy/lactation, ancestry, veteran status, and "any other basis protected by chapter 151B"; AG report to named joint committees. — Sec. 8. — "genetic information, pregnancy... ancestry or status as a veteran, or any other basis protected by chapter 151B"
18. `service-provider-third-party-duties` — Essentially identical to filed. — Sec. 11. — "shall adhere to the instructions of a covered entity and only collect, process, and transfer service provider data"
19. `private-right-of-action` — PRA narrowed to defendants that are LARGE DATA HOLDERS (was: any non-small-business); adds 93A UDAP deeming with recovery of actual damages or $5,000; same liquidated damages (0.15%/$15,000), punitives, fees, anti-arbitration, anti-waiver. — Sec. 12(a)-(f), (j). — "by a covered entity, service provider, or third party that is a large data holder may bring a civil action"
20. `ag-enforcement-penalties` — Same penalty structure (0.15%/$15,000 per violation; 4%/$20,000,000 per action); ADDS court power to suspend/prohibit operating in the commonwealth for flagrant, willful, repeat violations, plus investigation/litigation cost recovery; drops earmarking of awards to individuals; AG complaint website with enforcement statistics. — Secs. 12(g)-(h), 14. — "suspend or prohibit a covered entity, service provider, or third party from operating in the commonwealth"
21. `complaint-retaliation-ban` — Identical. — Sec. 12(i). — "to retaliate against an individual who makes a good-faith complaint"
22. `location-consent-regime` — NEW c.93N (near-verbatim from filed location bills H357/S148): location information collectible only for permissible purposes with opt-in consent per purpose; consent expires at 1 year/purpose completion/revocation with mandatory destruction; precision/retention/inference minimization; Location Privacy Policy with 20-day change notice; partial retroactive application. — SECTION 2, c.93N Secs. 1, 2(a)-(e),(g),(h); SECTION 3. — "unlawful for a covered entity to collect or process an individual's location information except for a permissible purpose"
23. `location-sale-ban` — NEW: flat ban on selling, renting, trading, or leasing location information to third parties (applies retroactively to previously collected data). — c.93N Sec. 2(e)(3); SECTION 3. — "sell, rent, trade, or lease location information to third parties"
24. `location-govt-warrant-requirement` — NEW: no disclosure of location information to government absent valid warrant, exigent circumstances, legal mandate (incl. court order/subpoena/CID — an exception broadened vs. the filed H357 lineage), or data-subject request; plus ban on government monetizing location information. — c.93N Sec. 2(f), (i). — "serves the covered entity or service provider with a valid warrant"
25. `location-targeted-ads-opt-out` — NEW: opt-out of processing location information for targeted-ad selection/delivery. — c.93N Sec. 2(c). — "opt out of the processing of their location information for purposes of selecting and delivering targeted advertisements"
26. `location-anti-retaliation-enforcement` — NEW: no adverse action for exercising location rights; chapter-specific PRA (actual damages or $5,000/violation, punitives, fees, per-instance violations), 93A UDAP deeming, AG action, anti-waiver/anti-arbitration. — c.93N Secs. 3, 4. — "actual damages, including damages for emotional distress, or $5,000 per violation, whichever is greater"

(Scope: non-applicability expanded to add GLBA financial data and FERPA education records as data-level exemptions, with burden of proof on the party claiming exemption — Sec. 13; attaches to the regime. "Covered entity" small-entity exclusion tightened 75,000 to 25,000 individuals; "large data holder" thresholds lowered $250M/5M to $200M/2M individuals — Sec. 1; attaches. Effective date 1 year — SECTION 4.)

## BILL S2770 — "Massachusetts Data Privacy Protection Act" (Senate Ways & Means redraft)

Same subject; propositions 1-26 identical to H4632, same section numbers. Only delta: c.93M chapter title retains "Protection" ("Massachusetts Data Privacy Protection Act").

---

## CROSS-BILL MATRIX

I = present, substantively identical across bills holding it; V = present as variant (delta noted); A = absent. Filed pair (H83/S25) is baseline for shared propositions.

| # | Proposition | H83 | S25 | H4632 | S2770 | Redraft delta vs filed |
|---|---|---|---|---|---|---|
| 1 | data-minimization-duty-of-loyalty | I | I | V | V | drops civic-engagement purpose (14 to 13); drops explicit targeted-ads secondary purpose |
| 2 | dark-pattern-ban | I | I | V | V | codifies "dark pattern" definition incl. FTC reference |
| 3 | ssn-restrictions | I | I | I | I | none |
| 4 | sensitive-data-strict-necessity | I | I | V | V | sensitive-data definition broadened (reproductive health, pregnancy, victim status, veteran, philosophical beliefs) |
| 5 | sensitive-data-transfer-consent | I | I | V | V | "affirmative express consent" replaced by defined "consent" |
| 6 | sensitive-data-targeted-ads-ban | I | I | I | I | none |
| 7 | consent-request-standards | I | I | V | V | adds point-of-collection display, policy attachment, account-conditioning ban |
| 8 | privacy-by-design | I | I | V | V | adds retention-evaluation duty; drops "substantial privacy risk" framing |
| 9 | anti-retaliation-pricing | I | I | I | I | none material |
| 10 | privacy-policy-transparency | I | I | V | V | adds homepage placement + separate biometric and geolocation policies |
| 11 | individual-data-rights | I | I | V | V | 24 to 12-mo lookback; 30 to 45-day response; school exception to FCRA exception |
| 12 | opt-out-rights-transfers-ads | I | I | V | V | adds forwarding liability shield, loyalty conflict procedure, no-forced-account rule |
| 13 | profiling-opt-out | A | A | I | I | added by redraft |
| 14 | authorized-agents-opt-out-signals | A | A | I | I | added by redraft (browser/device opt-out preference signals) |
| 15 | minors-targeted-ads-ban | I | I | I | I | none |
| 16 | data-broker-registration | I | I | V | V | dedicated $100/day penalties replaced by general enforcement; AG rulemaking on brokers |
| 17 | civil-rights-nondiscrimination | I | I | V | V | protected classes expanded to c.151B universe |
| 18 | algorithm-impact-assessments | I | I | A | A | dropped by redraft |
| 19 | centralized-opt-out-mechanism (OCABR) | I | I | A | A | dropped; nearest successor is #14 (different mechanism) |
| 20 | privacy-security-officers | I | I | A | A | dropped by redraft |
| 21 | large-holder-privacy-impact-assessment | I | I | A | A | dropped as standalone duty (residual mention in service-provider section) |
| 22 | service-provider-third-party-duties | I | I | I | I | none material |
| 23 | private-right-of-action | I | I | V | V | defendant class narrowed non-small-business to large-data-holder only; adds 93A UDAP/$5,000 floor |
| 24 | ag-enforcement-penalties | I | I | V | V | adds operating-suspension remedy + cost recovery; drops earmarking awards to individuals |
| 25 | complaint-retaliation-ban | I | I | I | I | none |
| 26 | legal-request-transparency-reports | I | I | A | A | dropped by redraft |
| 27 | interactive-computer-service-carveout | I | I | A | A | dropped by redraft |
| 28 | workplace-surveillance-limits (c.149 s.204) | I | I | A | A | dropped by redraft (employee-data exclusion from covered data also removed) |
| 29 | location-consent-regime (c.93N) | A | A | I | I | added by redraft (location covered only as sensitive data in filed bills) |
| 30 | location-sale-ban | A | A | I | I | added by redraft |
| 31 | location-govt-warrant-requirement (+govt monetization ban) | A | A | I | I | added by redraft; legal-mandate exception broadened to court orders/subpoenas/CIDs vs H357/S148 lineage |
| 32 | location-targeted-ads-opt-out | A | A | I | I | added by redraft |
| 33 | location-anti-retaliation-enforcement | A | A | I | I | added by redraft (PRA $5,000/actual, 93A UDAP) |

Cross-pilot note for proposition matching: c.93N in H4632/S2770 is near-verbatim the filed H357/S148 location chapter (93L) with three deltas: drops the annual warrant-transparency reporting section (93L Sec. 3), broadens the government-disclosure exception to include subpoenas/CIDs, softens AG regulations from mandatory to permissive, and replaces H357's retroactive consent-or-destroy rule with retroactive application of only 2(e)(3), 2(e)(5), 2(f). Propositions 29-33 should share IDs with the corresponding H357/S148 propositions (variant edges), and H83/S25 proposition 26 (legal-request transparency) is the same mechanism family as H357/S148 Sec. 3 reporting.

Source files (full texts): /private/tmp/claude-501/-Users-shsingh-Documents-GitHub-misc-ma-policy-ledger/474925a5-d5bb-490b-b655-e4cf902211d4/scratchpad/mdppa-agent/{H83,S25,H4632,S2770}.txt
