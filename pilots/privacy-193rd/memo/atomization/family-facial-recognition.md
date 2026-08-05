# Atomization working notes: facial-recognition family

Reading pass over cached bill texts (scripts/billtext.py); companion diffs
verified programmatically. Consolidated into scripts/atoms.py after
cross-checking. Quotes are verbatim from cached text.

H1728

Bill: H1728 - Implements the facial recognition special commission's recommendations by rewriting G.L. c.6 s.220 (all propositions in SECTION 1, cited by inserted-s.220 subsection).

1. le-biometric-surveillance-ban - Default prohibition on law enforcement acquiring, possessing, or using biometric surveillance technology, with exclusionary rule and narrow carve-outs (personal-device authentication, redaction software, unsolicited evidence) attached. SECTION 1, s.220(b),(l). "unlawful for a law enforcement agency or officer to acquire, possess, access, use, assist with the use of"
2. rmv-fr-identity-verification - Authorizes the registrar of motor vehicles to use facial recognition solely to verify identity when issuing licenses. SECTION 1, s.220(c). "may acquire, possess, or use facial recognition technology to verify an individual's identity when issuing licenses"
3. state-police-fr-gateway - Centralizes all FR searches in one state police operations group (or FBI on request), limited to felony warrant, emergency, deceased-identification, and on-behalf-of-agency purposes, using only approved technology vetted at public hearing. SECTION 1, s.220(d). "may perform a facial recognition search, or request the federal bureau of investigation to perform such a search"
4. emergency-fr-court-filing - Emergency FR searches must be immediately documented and justified in a sworn supervisory statement filed with superior court within 48 hours. SECTION 1, s.220(e). "file with the superior court in the relevant jurisdiction a signed, sworn statement"
5. fr-defendant-notice-discovery - Criminal defendants identified via FR search get notice plus discovery of all search records, algorithm, accuracy, and match-selection process. SECTION 1, s.220(f). "shall be provided notice that they were subject to such search, pursuant to rule 14"
6. le-fr-search-transparency - State police must record each search/request as a public record, report quarterly to EOPSS, and EOPSS publishes annual disaggregated statistics including race and gender of subjects. SECTION 1, s.220(g),(h). "shall document, as a public record, each facial recognition search request and each facial recognition search performed"
7. nonle-agency-fr-transparency - Non-law-enforcement public agencies must record and quarterly report their FR searches to EOPSS, with annual public publication. SECTION 1, s.220(i),(j). "Each non-law enforcement public agency shall document, as a public record, each facial recognition search requested"
8. emotion-video-analysis-ban - Absolute ban (no exceptions) on law enforcement using biometric systems to infer emotions or to analyze moving images/video; still frames allowed only under the (d) gateway. SECTION 1, s.220(k). "unlawful for a law enforcement agency of officer to use a biometric surveillance system to infer a person's emotions"

S927

Bill: S927 - Senate companion of H1728; text verbatim identical (only the SECTION 1 codification preamble wording differs).

Propositions 1-8 identical to H1728, same subsection cites, same quotes. No proposition-level differences.

H4359

Bill: H4359 - Judiciary redraft of H1728/S927, same rewrite of G.L. c.6 s.220.

1. le-biometric-surveillance-ban - unchanged. SECTION 1, s.220(b),(l).
2. rmv-fr-identity-verification - Same mechanism, broadened: registrar may use FR to "investigate and verify" identity, and state police may access/use FR to assist the registrar. SECTION 1, s.220(c). "the department of state police may access or use facial recognition technology to assist the registrar"
3. state-police-fr-gateway - Same mechanism with an added purpose (1) (assist the RMV under (c)); old purposes renumbered (2)-(5); written-documentation duty narrowed from "any search performed or search request made to the FBI" to FBI requests only. SECTION 1, s.220(d). "to assist the registrar of motor vehicles in investigating and verifying an individual's identity"
4. emergency-fr-court-filing - unchanged (now keyed to (d)(3)). SECTION 1, s.220(e).
5. fr-defendant-notice-discovery - unchanged. SECTION 1, s.220(f).
6. le-fr-search-transparency - unchanged except (h)(ii) counts FBI searches "requested to be performed," disaggregated by requesting agency. SECTION 1, s.220(g),(h).
7. nonle-agency-fr-transparency - unchanged. SECTION 1, s.220(i),(j).
8. emotion-video-analysis-ban - unchanged. SECTION 1, s.220(k).

H4832

Bill: H4832 - "Civil rights and technology": inserts G.L. c.140 s.131Z regulating robotic devices; contains NO facial recognition content (all cites are SECTION 1, inserted-s.131Z subsections).

1. weaponized-robot-ban - Criminal ban on manufacturing, modifying, selling, transferring, possessing, or operating a weapon-equipped robotic device (including UAVs), with escalating prison terms; DoD/defense-contractor/AG-waiver exemptions and a law-enforcement carve-out (explosives disposal, imminent-threat property destruction, training) attach, as do AG waiver regulations. s.131Z(b),(d),(e),(j). "unlawful for any person, whether or not acting under color of law, to manufacture, modify, sell, transfer, possess"
2. robot-misuse-crimes - Criminal offense to use a robotic device to threaten a crime, criminally harass, or physically restrain a person. s.131Z(c). "to use a robotic device to: (A) threaten to commit a crime"
3. robot-deployment-warrant - Law enforcement must obtain a warrant before deploying a robotic device onto private property or for surveillance/location tracking where an officer would need one. s.131Z(f). "shall be required to obtain a warrant, or other legally required judicial authorization, prior to deploying a robotic device"
4. robot-use-reporting - Each LE robotic-device use documented as a public record and reported quarterly to EOPSS; EOPSS publishes annually by March 31 (mechanism-shape mirrors s.220(g)-(h)). s.131Z(h). "shall document, as a public record, each time it uses a robotic device quarterly"
5. robot-private-right-of-action - Any individual may sue for damages and injunctive relief for violations, with attorneys' fees; treated in its own subsection covering the whole section. s.131Z(g). "Any individual may bring a civil action for damages and equitable relief, including injunctive relief"

(EOPSS rulemaking, s.131Z(i), attaches to propositions 1 and 4.)

S1551

Bill: S1551 - RMV transparency about facial recognition searches of driver's license/ID photos.

1. rmv-fr-search-public-notice - Registrar must post notices at licensing offices, hand out written information, and post web information explaining how officers use and access targeted face recognition of license/ID photos in criminal investigations. Single unnumbered SECTION (inserted c.90 s.8N). "post notices in conspicuous locations at all department driver licensing offices"

S1557

Bill: S1557 - Government drone (unmanned aerial vehicle) use rules: acquisition approval, warrant regime, data minimization, biometric-analysis ban.

1. drone-weapon-ban - Prohibits equipping UAVs with weapons. SECTION 1, s.221(b). "Unmanned aerial vehicles may not be equipped with weapons."
2. drone-acquisition-approval - Government UAV acquisition requires Secretary of Public Safety authorization (municipal purchases also need governing-body approval). SECTION 1, s.221(b). "shall be authorized, in the case of a unit of state or county government, by the Secretary of Public Safety"
3. critical-infrastructure-airspace-ban - Offense for any person to knowingly operate a drone in violation of critical-infrastructure airspace restrictions. SECTION 1, s.221(b). "No person shall knowingly operate an unmanned aircraft in violation of airspace restrictions"
4. drone-operation-gateway - Government may operate a UAV only under a c.276 warrant, for non-law-enforcement purposes (with evidence/intelligence-use bar), or in a documented emergency with a 48-hour supervisory affidavit. SECTION 1, s.221(c). "unlawful for a government entity or official to operate an unmanned aerial vehicle except as follows"
5. drone-data-minimization - Warrant flights collect data only on the warrant subject; non-target data may not be used or disclosed without consent and must be deleted within 24 hours. SECTION 1, s.221(d)(1),(e). "Such data shall be deleted as soon as practical, and in no event later than 24 hours"
6. drone-biometric-analysis-ban - Facial recognition and other biometric matching may not be applied to drone data except as judicially authorized under c.6 s.220. SECTION 1, s.221(d)(2). "Facial recognition and other biometric matching technology shall not be used to analyze data produced by an unmanned"
7. drone-first-amendment-shield - No drone tracking/collection of political, religious, or social views/associations absent a specific criminal investigation with probable cause. SECTION 1, s.221(d)(3). "used to track, collect, or maintain information about the political, religious, or social views"
8. drone-exclusionary-rule - Unlawfully acquired drone information inadmissible in any judicial, regulatory, or government proceeding. SECTION 1, s.221(f). "shall not be received in evidence in any judicial, regulatory, or other government proceeding"
9. drone-warrant-subject-notice - Warrant subject must be served the warrant and a notice within 7 days, with court-ordered delay up to 90 days. SECTION 1, s.221(g),(h). "Not later than seven days after information is collected by an unmanned aerial vehicle"
10. drone-warrant-judicial-reporting - Judges annually report each drone warrant to court management; court administrator files an annual public report with the legislature. SECTION 1, s.221(i). "any judge issuing or denying a warrant under subsection (c)(1) during the preceding calendar year shall report"
11. drone-hunting-ban - Adds UAVs to the c.131 s.65 prohibition on using aircraft for hunting/wildlife purposes. SECTION 2. "inserting after the word 'helicopter', in line 3, the following words:- , unmanned aerial vehicle"

H3431

Bill: H3431 - Comprehensive ALPR (automatic license plate reader) regime: new G.L. c.90J (all cites are SECTION 1, inserted chapter 90J section numbers).

1. alpr-use-restriction - Government ALPR use unlawful except law enforcement for legitimate law-enforcement purposes and DOT for tolls/parking fees. c.90J s.2. "unlawful for any governmental entity to use an ALPR system; provided, however"
2. alpr-accuracy-verification - Hot-list databases must be updated every 24 hours and a human must confirm plate and state match before acting on an alert. c.90J s.3. "shall confirm that the license plate number and state of issuance of the targeted vehicle matches"
3. alpr-le-48h-destruction - Law enforcement must permanently destroy ALPR data within 48 hours of capture, optionally transferring it to EOPSS first. c.90J s.4. "shall permanently erase or destroy any such data in its possession, custody or control"
4. alpr-eopss-120day-retention - EOPSS stores transferred ALPR data 120 days then destroys it, with extensions only for warrant, production order, or preservation request. c.90J s.5. "shall retain and store ALPR data transferred to it pursuant to section 4 for a period of 120 days"
5. alpr-vendor-retention-parity - Government may not contract with or access data from private entities that retain in-state ALPR data longer than the 120-day standard. c.90J s.6. "shall not enter into a business agreement with, or access ALPR data from, a non-governmental entity"
6. alpr-access-limits - Default ban on government accessing/searching/disclosing ALPR data from any source, excepting alert-compliance, system maintenance, documented emergencies (48-hour AG notice), felony warrants/production orders/preservation requests, and tolls; case-linked retention until prosecution ends. c.90J s.7. "a governmental entity may not access, search, review, disclose, or exchange ALPR data from any source"
7. alpr-secondary-use-ban - Bars any person from using ALPR data for credit, lending, insurance, employment, or marketing decisions (93A hook in s.10(b) attaches). c.90J s.8, s.10(b). "to determine a person's numerical or other credit rating"
8. alpr-admissibility-limits - Suppression of data obtained in knowing violation, plus general inadmissibility in civil/administrative proceedings except tolls, parking, insurance-fraud, theft, repossession matters. c.90J s.9. "shall not be admitted, offered or cited by any governmental entity for any purpose"
9. alpr-private-right-of-action - Aggrieved persons may sue for damages or injunctions, with treble or exemplary damages plus fees for willful violations. c.90J s.10(a). "shall, in addition to any liability for such actual damages as may be shown, be liable for treble damages"
10. alpr-ag-enforcement - Attorney general enforces ss.2-8 with injunctive and 93A relief. c.90J s.14. "The attorney general shall enforce sections 2 through 8, inclusive"
11. alpr-annual-reporting - EOPSS annual report to the legislature on system counts, participating municipalities, scan volumes, and warrants served. c.90J s.12. "the executive office shall file a report with the clerks of the senate and house of representatives"

(s.11 stricter-local-rules savings, s.13 rulemaking/audit, s.15 severability fail the standalone test and attach; s.13's audit process attaches to props 1-6.)

CROSS-BILL

H1728 = S927: verbatim companions; only the codification preamble in SECTION 1 differs. All 8 propositions identical.

H1728/S927 -> H4359: all 8 propositions survive. Three edits, all within existing propositions: (1) RMV authorization broadened from "verify" to "investigate and verify," with state police authorized to assist the registrar (s.220(c)); (2) corresponding new gateway purpose (d)(1) "to assist the registrar of motor vehicles," renumbering the rest; (3) written-documentation duty narrowed from all searches performed or requested to FBI requests only, and (h)(ii) recast to count FBI searches "requested," disaggregated by requesting agency. Nothing dropped, nothing else added.

H4359 -> H4832: complete subject replacement, not a redraft of the FR text. H4832 contains zero facial recognition, biometric surveillance, or RMV provisions; every H4359 proposition (1-8) is absent. Its content is a new robotic-device regime (weaponization ban, robot-misuse crimes, deployment warrant, use reporting, private right of action) in c.140 s.131Z rather than c.6 s.220. Structural echoes only: the quarterly-public-record-plus-March-31-EOPSS-publication reporting mechanism (s.131Z(h)) copies the shape of s.220(g)-(h), and the warrant-before-surveillance requirement (s.131Z(f)) parallels the FR/drone warrant gateways - but the mechanism targets differ (robotic devices, not biometric searches), so under the codebook these are different propositions. Cross-family overlap: H4832's weaponized-robot ban (s.131Z(b), covering UAVs) and S1557's drone-weapon ban (s.221(b)) are the same mechanism at overlapping targets - same proposition, H4832 the stricter variant (criminal penalties, broader device class); likewise H4832 s.131Z(f) and S1557 s.221(c)(1) are candidate same-proposition warrant requirements at overlapping targets (H4832 broader: any robotic device).

S1551 inside the others: no. S1551's mechanism is point-of-service public notice (posted notices, handouts, website text at RMV licensing offices about FR searches of license photos). H1728/S927/H4359 regulate the same target (FR searches against RMV photos) but through different mechanisms: search authorization limits (d), after-the-fact statistical reporting/publication (g)-(j), and individualized defendant notice (f). No posting/general-public-notice duty appears in H1728, S927, H4359, or H4832, so S1551 remains a distinct proposition with no bill-edge to the redraft line. S1557 (d)(2) cross-references c.6 s.220 but does not carry S1551's mechanism either.
