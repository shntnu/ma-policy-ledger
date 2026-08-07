# Atomization working notes: driver-commercial family

Reading pass over cached bill texts (scripts/billtext.py); companion diffs verified programmatically.
Consolidated into scripts/atoms.py after cross-checking.
Quotes are verbatim from cached text.

Data verification note applied below: H1455's cached full text is verbatim identical to S209 (toll data amendments to c.6C s.13), despite its title "An Act relative to the tracking of certain electronic devices" — the "electronic devices" are toll transponders.
H1455 is NOT a companion of H1572/H1809.

## Per-bill atomization

### S209 — warrant requirement and remedies for electronic tolling data (amends c.6C s.13, adding subsecs (d)-(j); no (g) in text)
1. `toll-tech-purpose-limitation` — toll collection technology may not be used to locate vehicles for any purpose other than tolling.
   Subsec (d). "shall not be used to identify the location of any vehicle for purposes other than charging and collecting"
2. `toll-data-le-warrant` — no tolling-derived data to law enforcement without a c.276 warrant; emergency exception with 48-hour sworn statement filed with court attaches.
   Subsecs (e), (j). "shall be shared with or provided to any law enforcement entity ... without a valid warrant"
3. `toll-data-exclusionary-rule` — data obtained in violation is inadmissible in any criminal or civil proceeding (victim may still use it).
   Subsec (f). "shall be inadmissible in any criminal or civil proceeding"
4. `toll-data-private-action` — aggrieved person civil action; willful violations: exemplary damages $100-$1,000 per violation plus fees.
   Subsec (h). "liable for exemplary damages of not less than $100 and not more than $1,000 for each violation"
5. `toll-data-93a-hook` — any use of violation-obtained data is itself a c.93A violation.
   Subsec (i). "shall be a violation of Chapter 93A"

### H1455 — same subject; text verbatim identical to S209
Propositions 1-5 identical to S209, same subsection numbers, same quotes (only difference: lowercase "sections"/"chapter" in (e), (i)).
Carries all five S209 propositions with no substantive variance.

### H3434 — MassDOT tolling data privacy (standalone act, Sections 1-4)
1. `dot-tolling-access-restriction` — MassDOT barred from accessing/searching/disclosing/exchanging tolling data except four enumerated purposes (toll collection, system maintenance, emergency, legal process).
   Sec 2. "shall not access, search, review, disclose, or exchange tolling data in its possession"
2. `toll-data-le-warrant` (variant) — law-enforcement access only via search warrant, production order, or preservation request tied to a felony; emergency access with 48-hour written notice to AG (not court).
   Sec 2(c)-(d) plus Sec 1 definitions. "comply with a search warrant, production order, or preservation request ... prosecution of a felony"
3. `tolling-data-120-day-destruction` — mandatory permanent erasure of tolling data 120 days after creation, with legal-process and unpaid-toll retention exceptions.
   Sec 3. "permanently erase or destroy ... not later than 120 days following the date on which the tolling data was created"
4. `toll-data-private-action` (variant) — aggrieved person civil action; willful: treble damages OR exemplary $100-$1,000 plus fees.
   Sec 4. "liable for treble damages, or, in the alternative, exemplary damages"

### H3404 — driver privacy protections (new c.90K, Sections 1-6)
1. `alpr-government-use-restrictions` — persons under color of state law: no ALPR tracking of protected activity; 14-day ALPR data retention cap absent a specific investigation; no disclosure/sale except judicial proceeding; no access to others' ALPR data without warrant.
   Sec 2 (four prongs, one section; splittable). "retain ALPR data longer than 14 days except in connection with a specific criminal investigation" SPLIT (eighth pass): the note above answered the severability question and was not acted on for six passes, so one proposition (P-213) stood for four duties and its published description named only three of them.
   Prong (a) is now P-382, (b) is P-383, (d) is P-384, and prong (c) — no disclosure, sale or permitted access except in a judicial proceeding — is H3431's P-196 mechanism at a single exception rather than several, so it is recorded as a P-196 edge rather than a fifth ID.
   P-213 is retired.
2. `toll-tech-purpose-limitation` — toll tech only for tolling under c.6C s.13.
   Sec 3(a). "toll collection technologies shall only be used to identify the location of any vehicle for tolling purposes"
3. `dot-tolling-access-restriction` — same four-purpose department access bar as H3434 Sec 2.
   Sec 3(b). "shall not access, search, review, disclose, or exchange tolling data"
4. `tolling-data-120-day-destruction` — same 120-day erasure as H3434 Sec 3.
   Sec 3(c). "permanently erase or destroy all tolling data ... not later than 120 days"
5. `toll-data-le-warrant` — no toll collection data to law enforcement without search warrant or production order; emergency exception, 48-hour notice to AG.
   Sec 4. "shall be shared with or provided to any law enforcement entity ... without a search warrant, or production order"
6. `vehicle-telematics-le-warrant` — extends the warrant requirement to "vehicle data" (OEM/telematics/aftermarket GPS location data held by private parties); distinct target, so distinct proposition.
   Sec 1 (definition), Sec 4. "'Vehicle data', GPS information revealing the location of vehicles that is created by the hardware or software"
7. `toll-data-exclusionary-rule` (variant) — ALPR, tolling, and vehicle data obtained in violation barred from use by any governmental entity in any criminal, civil, or administrative proceeding.
   Sec 5. "shall not be admitted, offered or cited by any governmental entity for any purpose"
8. `toll-data-private-action` (variant) — civil action; willful: treble or exemplary $100-$1,000.
   Sec 6(a)-(b). "liable for treble damages, or, in the alternative, exemplary damages"
9. `toll-data-ag-enforcement` — AG enforcement power with injunctive relief; separate because companions lack it.
   Sec 6(c). "The attorney general shall enforce this chapter"

### H1572 — criminal ban on motor-vehicle tracking devices (new c.265 s.43B)
1. `vehicle-tracking-device-criminal-ban` — knowing installation of an electronic mobile tracking device on a motor vehicle without operator/occupant consent is criminal harassment (punished per c.265 s.43A); exceptions for law enforcement, parent/guardian monitoring a minor child operator, stolen-vehicle recovery, business fleet vehicles; OEM/rental/insurance telematics excluded.
   SECTION 1 (subsecs (a)-(d) all attach). "installs, conceals, or otherwise places for use an electronic mobile tracking device in or on a motor vehicle without the consent"

### H1809 — criminal ban on electronic tracking of motor vehicles (new c.272 s.108)
1. `vehicle-tracking-device-criminal-ban` (variant) — same mechanism: knowing nonconsensual installation/use of a tracking device on a motor vehicle for monitoring occupants; standalone penalty (up to 1 year house of correction and/or $1,000); exceptions for law enforcement, parent/guardian (child as occupant, voided if installer has restraining/no-contact order), stolen goods/theft-recovery devices, dealer starter-interrupt devices with written consent, business fleets including contractors; OEM/telematics/rental/insurance carve-out.
   Whole section (a)-(d) attaches. "knowingly installs, conceals or otherwise places or uses an electronic tracking device in or on a motor vehicle without the consent"

### H3217 — residential energy scorecard program (only personal-data clauses in-domain; SECTIONS 1-5, 7-8, 10-16 out of domain: RGGI funding, program design, building code, effective dates)
1. `scorecard-personal-data-content-limit` — energy scorecards may not contain personal data (c.66A definition) beyond address and rating.
   SECTION 6. "shall not contain any other personal data as defined in section 1 of chapter 66A"
2. `scorecard-nondisclosure-consent` — department/third-party-held scorecards not disclosable without owner consent; exempt from public records law; aggregate release allowed.
   SECTION 9 (new c.25A s.17(e)). "individual energy scorecards shall not be disclosed ... without the consent of the owner"

### H1049 — mortgage trigger lead privacy (new c.183 s.70)
1. `trigger-lead-solicitation-93a` — enumerated solicitation practices based on mortgage trigger leads (failure to disclose non-affiliation, failure to disclose the lead was purchased from a CRA, FCRA prescreen noncompliance, soliciting opt-out/Do-Not-Call consumers) declared unfair/deceptive under c.93A; definition 70(a) and AG-regulations clause 70(c) attach.
   SECTION 1, s.70(a)-(c). "the solicitation is based on personal information about the consumer that was purchased ... from a consumer reporting agency"

### H326 — trial offers / negative options plus financial-information nondisclosure (new c.93 ss.115-117)
1. `trial-offer-disclosure-consent-regime` — sellers must give clear pre-acceptance disclosure of trial-offer terms, easy cancellation, affirmative consent before charging, renewal notice 5-10 days before charge; seller bears burden of proof; violation is 93A.
   Sec 116(a)-(e),(g) (definitions in s.115 attach).
   Out of privacy domain (consumer-protection mechanism). "may not impose a financial obligation on a consumer ... unless the seller has obtained the consumer's affirmative consent"
2. `billing-data-pass-prohibition` — seller may not pass consumer billing information to another seller (causing a charge) without the consumer's affirmative consent at acceptance.
   Sec 116(f).
   IN domain. "allowing the seller to provide the consumer's billing information to a seller other than the seller making the trial offer"
3. `financial-institution-nondisclosure` — financial institutions barred from disclosing any customer financial or personal information except to the identified customer or with customer authorization limited to authorized scope; violation is 93A.
   Sec 117.
   IN domain. "shall not disclose any financial or personal information relating to a customer"

### H395 — Online Advertising Act (third-party ad networks; standalone act, Sections 1-8)
1. `ad-network-notice` — ad network must post clear notice of collection/use/retention practices, OPM profiling, opt-out and consent-revocation procedures; material-change notice with retroactivity limit.
   Sec 3(A). "shall post clear and conspicuous notice on its own website about its data collection and use practices"
2. `publisher-privacy-policy-requirement` — networks must contractually require client publishers to post privacy policies disclosing network use and opt-out link.
   Sec 3(B). "shall require that the publisher post a privacy policy"
3. `opm-opt-out` — consumer right to opt out of online preference marketing via designated page.
   Sec 4(A). "must provide a means for consumers to opt-out of online preference marketing"
4. `sensitive-data-opt-in` — affirmative consent (revocable) required before using sensitive medical/financial/sexual data for OPM.
   Sec 4(B). "shall not use information about sensitive medical or financial data, sexual behavior or sexual orientation ... without the affirmative consent"
5. `pii-merger-consent` — merging non-PII with PII requires consent (opt-out notice for prospective mergers, opt-in for previously collected data); Sec 5(B) technical safeguards against unconsented merger attach.
   Sec 4(C), 5(B). "shall not merge non-personally identifiable information ... with personally identifiable information without the consumer's prior consent"
6. `ad-network-data-security` — reasonable efforts to protect collected data from loss/misuse/improper access.
   Sec 5(A). "reasonable efforts to protect the data they collect or log ... from loss, misuse, alteration, destruction or improper access"
7. `ad-network-consumer-access` — consumer access right to retained PII, with identity-verification/burden/proprietary exceptions and cost-based fees.
   Sec 6. "shall provide consumers with reasonable access to personally identifiable information"
8. `ad-data-24-month-retention-limit` — non-PII collected via ad delivery must be deleted within 24 months.
   Sec 7. "for duration of a maximum of twenty-four months from the time of collection"
9. `ad-network-ag-enforcement` — act-wide AG action, $1,000 statutory penalty per violation, treble for pattern-and-practice; separate section enforcing all duties, so listed separately.
   Sec 8. "subject to a statutory penalty of not more than one thousand dollars for each instance"

### H1707 — malicious doxing civil action (new c.214 s.3C)
1. `malicious-doxing-civil-action` — civil action for knowing, nonconsensual dissemination of personal information (home address, phone, SSN, email, school/work location) with malicious intent to facilitate harassment/stalking/death/injury plus threat-or-result element; actual and punitive damages, sensitive-info (race, health, gender-affirming/reproductive care) damages enhancement, joint and several liability, platform/carrier immunity, unlawful-conduct/speech/petition exemptions, 2-year limitation.
   SECTIONS 1-2 (definitions, remedies, effective date all attach; not severable as standalone policies). "the person disseminated the personal information with the malicious intent to cause, aid, encourage or facilitate the harassment"

### S971 — malicious doxing civil action
1. `malicious-doxing-civil-action` — identical proposition, SECTIONS 1-2.
   Same quote applies verbatim.

## Cross-bill

**S209 vs H1455**: verbatim-identical texts (trivial capitalization differences).
All five propositions shared 1:1.
H1455's title mislabels the family; it belongs with S209, not with the tracking-device bills.

**S209/H1455 vs H3434 vs H3404** (tolling family):
- `toll-data-le-warrant`: all four bills.
  Variants: S209/H1455 = any-crime warrant, emergency statement filed with court; H3434 = felony-only, adds production order/preservation request channels for defendants, emergency notice to AG; H3404 = warrant or production order, emergency notice to AG, and extends to "vehicle data".
- `toll-tech-purpose-limitation`: S209/H1455 subsec (d) and H3404 Sec 3(a) only.
  H3434 approximates the goal through the department access restriction, a different mechanism (restriction on department conduct, not on the technology's use), so not the same proposition.
- `dot-tolling-access-restriction` and `tolling-data-120-day-destruction`: H3434 Secs 2-3 and H3404 Sec 3(b)-(c) only; near-verbatim shared text.
  Absent from S209/H1455.
- `toll-data-exclusionary-rule`: S209/H1455 (f) and H3404 Sec 5 only; H3404 variant broader (covers ALPR/tolling/vehicle data, bars governmental use in administrative proceedings too).
  Absent from H3434.
- `toll-data-private-action`: all four.
  Variant: S209/H1455 exemplary only; H3434/H3404 treble-or-exemplary.
- `toll-data-93a-hook`: S209/H1455 only.
- `toll-data-ag-enforcement`: H3404 only.
- `alpr-government-use-restrictions` and `vehicle-telematics-le-warrant`: H3404 only.
- Net: H3404 is a consolidation superset of S209/H1455 plus H3434, adding ALPR, vehicle telematics, and AG enforcement.

**H1572 vs H1809 vs H1455**: H1572 and H1809 share one proposition, `vehicle-tracking-device-criminal-ban` (same mechanism: criminal prohibition on nonconsensual vehicle tracking device installation; stricter/weaker variants).
Differences recorded on the edge: statutory placement (c.265 s.43B vs c.272 s.108); penalty (criminal-harassment penalties by reference vs standalone 1 year/$1,000); parent exception (child as operator vs child as occupant, H1809 adds restraining-order disqualifier); theft exception (stolen vehicle only vs stolen goods generally plus theft-recovery devices); H1809 adds dealer starter-interrupt exception and extends the fleet exception to contractors.
H1455 shares nothing with them; it carries the S209 tolling propositions.

**H1707 vs S971**: verbatim companions; single shared proposition `malicious-doxing-civil-action` with no substantive differences (three trivial wording variants: "such individual family member's" vs "such family member's" in the personal-information definition; "the dissemination" vs "such dissemination" in element (ii); S971 adds "pursuant to this section" in subsec (d)).

**Other cross-links within this set**: none.
H3217's scorecard clauses, H1049's trigger-lead mechanism, H326's data-pass and financial-institution nondisclosure, and H395's ad-network regime each stand alone in this twelve-bill set.
Adjacent-mechanism notes for the linking stage: H326 Sec 117 (financial-institution nondisclosure) and H1707/S971 (doxing) both restrict disclosure of personal information but by different mechanisms (institutional duty vs tort for malicious dissemination); H395 Sec 7 (24-month retention limit) and H3434/H3404 (120-day destruction) are both retention-limit mechanisms but at different targets (ad networks vs MassDOT).

**Domain flags**: H3217 SECTIONS 1-5, 7-8, 10-16 out of domain (energy program funding/design); H326 proposition 1 (trial-offer regime) out of domain (no data-handling rule); everything else in-domain per memo/codebook.md.
