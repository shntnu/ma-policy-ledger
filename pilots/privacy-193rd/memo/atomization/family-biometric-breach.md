# Atomization working notes: biometric/breach family

Reading pass over cached bill texts (scripts/billtext.py); companion diffs
verified programmatically. Consolidated into scripts/atoms.py after
cross-checking. Quotes are verbatim from cached text.

H63 text, S195, S140, H76, S30, S198, S2539, and H281 all read in full. Output follows.

## Per-bill atomization

### H63 — standalone biometric privacy chapter (new c.93M "Privacy Protections for Biometric Information"): consent regime, monetization ban, warrant notice, private right of action

Bill structure: SECTION 1 inserts c.93M (internal Sections 1-6); SECTION 2 = retroactive consent + AG regs; SECTION 3 = effective date. Internal Section 1 (definitions), Section 6 (non-applicability: HIPAA, GLBA, government contractors), SECTION 2 (6-month retroactive consent/destruction), and SECTION 3 (effective date) attach to the substantive propositions; they fail standalone sense.

1. **biometric-collection-consent** — prohibit collection/processing of biometric info without prior written notice, delivery of privacy policy, and opt-in consent, with H63-specific handwritten non-electronic consent for identification uses and 3-year consent expiry. Sections: SECTION 1 (c.93M s.2(a)-(c)); SECTION 2 attaches (retroactive consent). Evidence: "shall not collect or process an individual's biometric information for identification purposes unless it first".
2. **biometric-privacy-policy-retention** — mandatory public Biometric Privacy Policy stating use models, security policies, disclosure practices, and retention/deletion schedule, with 20-business-day change notice and re-consent; destruction on consent expiry. Sections: SECTION 1 (c.93M s.2(c)-(e)). Evidence: "shall always maintain and make available to the individual a Biometric Privacy Policy".
3. **biometric-disclosure-limits** — ban disclosure of biometric info except enumerated exceptions (consented service provision, consented transaction, separate handwritten per-disclosure consent, legal requirement, warrant, 911 emergency). Sections: SECTION 1 (c.93M s.2(g)). Evidence: "shall not disclose, cause to disclose, or otherwise disseminate or cause to disseminate an individual's biometric information".
4. **biometric-monetization-ban** — flat prohibition on disclosing biometric info for profit or consideration (sell, rent, trade, lease). Sections: SECTION 1 (c.93M s.1 def. 10, s.2(h)). Evidence: "It is unlawful for a covered entity, data processor, or third party to monetize an individual's biometric information."
5. **biometric-security-standard** — duty to store/transmit/protect biometric data with industry reasonable standard of care and at least as protectively as other sensitive data. Sections: SECTION 1 (c.93M s.2(f)). Evidence: "store, transmit, and protect from disclosure all biometric data using the reasonable standard of care".
6. **biometric-warrant-notice** — entity receiving a warrant for biometric info must immediately notify the individual (copy of warrant, inventory, requester identity), subject to court-ordered 30-day renewable delay; duty to contest invalid warrants. Sections: SECTION 1 (c.93M s.3). Evidence: "shall serve or deliver the following information to the individual to which the warrant request biometric information refers".
7. **biometric-warrant-transparency-reports** — annual aggregate reporting to the AG of warrants received and legally mandated disclosures; AG publishes standardized reports online. Sections: SECTION 1 (c.93M s.4). Evidence: "on an annual basis, report to the attorney general aggregate information regarding any warrants for biometric information".
8. **biometric-enforcement-pra** — private right of action (no exhaustion, no forced arbitration) with revenue-scaled liquidated damages, punitive damages, fees; AG action via c.93A s.4; rebuttable presumption of harm; anti-waiver. Sections: SECTION 1 (c.93M s.5). Evidence: "liquidated damages of not less than 0.5% of the annual global revenue of the covered entity or $5,000".

### S195 — standalone Biometric Information Privacy Act (new c.93M), Illinois-BIPA-style, single unnumbered enacting section

Section cites below are to internal c.93M sections (the bill has one enacting section). Section 1 (definitions) and Section 4 (construction) attach.

1. **biometric-collection-consent** — no collection/purchase/receipt of biometric identifiers without written notice of collection, purpose and term, and written (electronic-permitted) consent. Sections: c.93M s.2(b). Evidence: "receives written consent executed by the subject of the biometric identifier or biometric information".
2. **biometric-privacy-policy-retention** — mandatory written retention-schedule/destruction policy; destruction when purpose satisfied or within 1 year of last interaction, whichever first. Sections: c.93M s.2(a). Evidence: "establishing a retention schedule and guidelines for permanently destroying biometric identifiers and biometric information".
3. **biometric-monetization-ban** — ban on selling, leasing, trading, or otherwise profiting from biometric identifiers. Sections: c.93M s.2(c). Evidence: "sell, lease, trade, or otherwise profit from a person's or a customer's biometric identifier".
4. **biometric-disclosure-limits** — ban disclosure/redisclosure except consent, consumer-requested financial transaction, state/federal law or municipal ordinance, or warrant/subpoena. Sections: c.93M s.2(d). Evidence: "disclose, redisclose, or otherwise disseminate a person's or a customer's biometric identifier or biometric information unless".
5. **biometric-security-standard** — same dual security duty as H63, verbatim mechanism. Sections: c.93M s.2(e). Evidence: "in a manner that is the same as or more protective than the manner in which the private entity stores".
6. **commercial-establishment-biometric-id-ban** — flat use ban: places of entertainment, retail stores, food/drink establishments may not use biometrics to identify a person. Sections: c.93M s.2(f), s.1 (def. "Commercial Establishment" attaches). Evidence: "No commercial establishment shall use a person's or a customer's biometric identifier or biometric information to identify them."
7. **biometric-enforcement-pra** — aggrieved-person cause of action and AG action, both via c.93A procedures; $5,000 minimum or actual damages, double-to-treble for willful/knowing. Sections: c.93M s.3. Evidence: "Damages pursuant to any said action shall be no less than $5,000 per violation or actual damages suffered".

### S140 — adds biometric indicators to the c.93H breach-notification "personal information" definition

1. **93h-personal-info-biometric** — extend c.93H personal information to a new "(d) biometric indicator" element; SECTION 1's definition attaches (note: the S140 definition includes "genetic information" and has no photograph/recording exclusions). Sections: SECTIONS 1, 2, 3. Evidence: "any unique biological attribute or measurement that can be used to authenticate the identity of an individual".

That is the whole bill: one proposition, three formal sections.

### H76 — comprehensive modernization of c.93H (definitions, breach trigger, notice contents)

SECTION 6 (regs updated to reflect definition changes) attaches to the definitional propositions; it fails standalone sense.

1. **93h-personal-info-biometric** — add "(E) biometric information" element plus its definition (excludes photographs, audio/video recordings, and derived data unless generated to identify). Sections: SECTIONS 1, 4(i)(E). Evidence: "data generated from the specific technical processing of an individual's unique biological or physiological patterns or characteristics".
2. **93h-personal-info-dob** — add "(F) date of birth" element. Sections: SECTION 4(i)(F). Evidence: "(F) date of birth;".
3. **93h-personal-info-expanded-categories** — add taxpayer ID, passport/military/other government ID numbers, genetic information, health insurance information, medical information, and specific geolocation information as elements, with their definitions. Sections: SECTIONS 3, 4(i)(B),(C),(G)-(J), 5. Evidence: "(G) genetic information; (H) health insurance information; (I) medical information; or (J) specific geolocation information".
4. **93h-login-credentials-breach** — extend the breach law to standalone online-account credentials (no name required) with credential-specific notice mechanics (password-change direction; no notice to the breached email account itself). Sections: SECTIONS 4(ii), 10 (last two paragraphs). Evidence: "a username or electronic mail address, in combination with a password or security question and answer that would permit access".
5. **93h-breach-definition-modernization** — restate "breach of security" around electronic data: unencrypted electronic data, or encrypted data when the "encryption key or security credential" has been acquired. Sections: SECTION 2. Evidence: "encrypted electronic data when the encryption key or security credential has been acquired".
6. **93h-breach-harm-threshold** — condition the notification trigger on a foreseeable-risk-of-harm test added to c.93H s.3(b). Sections: SECTION 7. Evidence: "presents a reasonably foreseeable risk of financial, physical, reputational or other cognizable harm to the resident".
7. **93h-notice-content-modernization** — rewrite required consumer-notice contents (date range, data types, description, contact, police report, free security freeze, mitigation services, FTC info), require sample copy to AG/OCABR, bar delay pending headcount, and rework the credit-monitoring certification report; medical/geolocation breaches exempted from freeze and certification items. Sections: SECTIONS 8, 9, 10. Evidence: "the date, estimated date, or estimated date range of the breach of security". Note: as drafted this proposition cross-references "subclauses (A) through (J)", so it is not severable from proposition 3 without redrafting.

### S30 — exact companion of H76 (same 10 sections)

Propositions identical to H76 items 1-7, with the same section numbers (SECTIONS 1-10). Textual differences from H76, both trivial: (a) SECTION 1, biometric exclusion clause (iii): S30 reads "generated to authenticate or identify a specific individual" where H76 reads only "to identify"; (b) SECTION 10: S30 "shall not be required to include" vs H76 "shall not need to include". Evidence (SECTION 1): "unless such data is generated to authenticate or identify a specific individual".

### S198 — adds date of birth to c.93H personal information (single-section bill)

1. **93h-personal-info-dob** — add "(d) date of birth" to the existing personal information definition. Sections: the bill's sole unnumbered section. Evidence: "adding to the definition of 'personal information' the following subsection:- (d) date of birth". Note: drafting collides with S140, which also proposes a "(d)" element.

### S2539 — Senate omnibus, "cybersecurity resilience + AI"; consumer-data content is SECTIONS 5-15 (c.93H), embedding the H76/S30 package plus one addition

In-domain propositions (SECTIONS 5-15 track S30's SECTIONS 1-10 nearly verbatim, with SECTION 13 inserted):

1. **93h-personal-info-biometric** — SECTIONS 5, 8(i)(E). Evidence: "generated to authenticate or identify a specific individual" (matches S30 wording, not H76's).
2. **93h-personal-info-dob** — SECTION 8(i)(F). Evidence: "(F) date of birth;".
3. **93h-personal-info-expanded-categories** — SECTIONS 7, 8(i)(B),(C),(G)-(J), 9. Evidence: "(J) specific geolocation information".
4. **93h-login-credentials-breach** — SECTIONS 8(ii), 15 (last two paragraphs). Evidence: "a username or electronic mail address, in combination with a password or security question and answer".
5. **93h-breach-definition-modernization** — SECTION 6. Evidence: "when the encryption key or security credential has been acquired".
6. **93h-breach-harm-threshold** — SECTION 11. Evidence: "reasonably foreseeable risk of financial, physical, reputational or other cognizable harm".
7. **93h-notice-content-modernization** — SECTIONS 12, 14, 15 (trivial variant: "toll-free number" singular vs H76/S30 "numbers"). Evidence: "mitigation services to be provided pursuant to this chapter". SECTION 10 (regs update) attaches to the definitional propositions.
8. **93h-notify-fbi** — S2539-unique: adds the FBI as a mandatory breach-notification recipient alongside the AG in c.93H s.3(b). Sections: SECTION 13. Evidence: "the following words each time so appearing:- , Federal Bureau of Investigation".

Borderline (flag, arguably in-domain):
- SECTION 17 (new c.175 s.231): contracts and cyber-insurance policies may not prohibit/limit/delay reporting a cybersecurity incident or 93H breach of security to government; insurer anti-discrimination. Mechanism protects breach reporting, so it touches the breach-notification subdomain. Evidence: "No insurer shall discriminate against an insured party for reporting a cybersecurity incident".
- SECTION 1, c.7D s.17(f)(iv): the Automated Decision Making Control Board is directed to regulate AI training data including "informed consent... from individuals before collecting, using, sharing or disclosing their data" and deletion/de-identification. This is delegated rulemaking over personal data inside an otherwise out-of-domain AI section; per the codebook's AI carve-in ("UNLESS the provision governs personal data") it is a candidate proposition.
- SECTION 16(i): warrant requirement before police deploy a robotic device for "surveillance or location tracking" — matches the codebook's government-surveillance-through-data-generating-technology subdomain (drone/robot data rules); likely belongs to a different cluster, flagged rather than atomized here.

Out-of-domain content (no consumer-data propositions): SECTION 1's c.7D s.12 (state-employee cybersecurity training), s.13 (definitions), s.14 (cybersecurity control board / state cybersecurity code with $10k fines), s.15 (Cyber Incident Response Team), s.16 (critical-infrastructure incident reporting to fusion center — explicitly disclaims 93H effect: "Nothing in this section shall be construed to... fulfill any regulatory data breach reporting requirements pursuant to chapter 93H"), s.17 generally (ADM board); SECTION 2 (Massachusetts Innovation Fund / IT modernization loans); SECTIONS 3-4 (civil defense act, cyber-attack emergency powers); SECTION 16 generally (weaponized robotics ban); SECTION 18 (cybersecurity workforce fund); SECTIONS 19-22 (board transition, standards deadline, effective date).

### H281 — c.93H rewrite: statutory information-security-program mandate, breach redefined with identity-theft-risk threshold, financial-account biometric element (drafted against the 2016 Official Edition; several provisions are older-generation text refiled)

1. **93h-security-program-mandate** — DCABR shall adopt regulations requiring a comprehensive written information security program with enumerated elements (coordinator, risk assessment, safeguards, third-party-provider oversight), plus GLBA/HIPAA/HITECH deemed-compliance safe harbor. Sections: SECTION 2. Evidence: "develop, implement, and maintain a comprehensive information security program that contains administrative, technical, and physical safeguards".
2. **93h-breach-harm-threshold** — narrow the breach definition itself to acquisitions creating an identity-theft/fraud risk. Sections: SECTION 1 ("Breach of security" definition). Evidence: "that creates an identifiable risk of identity theft or fraud".
3. **93h-personal-info-biometric** — add a biometric element to personal information, narrowest variant: only biometrics used to access financial accounts. Sections: SECTION 1 (personal information clause (d)). Evidence: "biometric indicator of the consumer used to gain access to financial accounts of the consumer".
4. **93h-personal-info-public-records-exclusion** — exclude lawfully obtained publicly available / government-record information from personal information (H281-only narrowing). Sections: SECTION 1. Evidence: "shall not include information that is lawfully obtained from publicly available information".
5. **93h-notice-content-modernization** — rewrite the same third paragraph of s.3(b) notice contents (police report, security-freeze process, "any fees required to be paid" — weaker than current law's free-freeze rule). Sections: SECTION 3. Evidence: "and any fees required to be paid to any of the consumer reporting agencies".

Attachments/orphans: SECTION 1's definitions of "Encrypted" (128-bit floor plus DCABR revision power under s.1(b)), "Notice", "Substitute notice", "Data" attach to the package. "Access device", "Financial institution", and "Service provider" are defined but no operative section in the printed text uses them — orphaned definitions, suggesting the filing is a truncated refile of a longer prior-session bill (SECTION numbering even switches between "SECTION 1:" and "SECTION 2.").

## Cross-bill analysis

**H63 vs S195 (both new c.93M standalone biometric acts).** Not exact companions — different drafts of the same architecture. Shared propositions, with variants on the edges:
- biometric-collection-consent: shared; H63 stricter (handwritten non-electronic consent for identification uses, 3-year consent expiry with renewal, retroactive 6-month re-consent for pre-existing data via bill SECTION 2); S195 weaker (written consent, electronic permitted, no expiry).
- biometric-privacy-policy-retention: shared; H63's policy is richer (use models, 20-day change notice + re-consent), S195 has the harder retention backstop (destruction within 1 year of last interaction).
- biometric-monetization-ban: shared; H63 flat ban on any disclosure for consideration; S195 ban on sell/lease/trade/profit. Same mechanism, H63 stricter.
- biometric-disclosure-limits: shared; exception lists nearly parallel; H63 adds 911-emergency exception, separate handwritten per-disclosure consent, and warrant-validity duty; S195 additionally allows subpoena and municipal ordinance.
- biometric-security-standard: shared, essentially verbatim identical dual-standard language in both (H63 c.93M s.2(f); S195 s.2(e)).
- biometric-enforcement-pra: both bills treat enforcement in a separate internal section and differ on exactly this point, so it is carried as its own proposition per the grain rule. H63: liquidated damages of 0.5%/0.1% of annual global revenue or $5,000/$1,000 per violation, punitive damages, anti-arbitration, anti-waiver, rebuttable presumption of harm. S195: c.93A procedures, $5,000 or actual damages, double-to-treble for willful/knowing.
- H63-only propositions: biometric-warrant-notice (c.93M s.3), biometric-warrant-transparency-reports (c.93M s.4). No S195 counterpart.
- S195-only proposition: commercial-establishment-biometric-id-ban (c.93M s.2(f)) — a sectoral use ban, a different mechanism from the consent regime; no H63 counterpart.

**S140 vs H63/S195.** Different mechanism for the same broad goal: S140 folds biometrics into the existing c.93H breach-notification/security regime (protection = security-program + breach notice), while H63/S195 create new collection/consent/use duties in a standalone chapter. Different propositions; S140 shares nothing with H63/S195.

**H76 vs S30.** Exact companions, section-for-section (SECTIONS 1-10), sharing all seven propositions. Only two wording differences, both noted above (SECTION 1 clause (iii) "identify" vs "authenticate or identify" — H76's biometric exclusion is marginally broader, i.e., its biometric coverage marginally narrower; SECTION 10 "need"/"required" phrasing).

**S2539 vs H76/S30.** S2539 SECTIONS 5-12 and 14-15 reproduce S30 SECTIONS 1-10 essentially verbatim (S2539 matches S30, not H76, on the "authenticate or identify" wording). S2539 inserts one extra proposition into the package: SECTION 13, FBI notification (93h-notify-fbi), found in no other bill here. So on the 93H package: H76 = S30 = S2539(93H portion), plus S2539's FBI add-on.

**93h-personal-info-biometric proposition membership** (same mechanism — add a biometric data element to c.93H personal information — five bills): S140 (SS.1-3; own "biometric indicator" definition that sweeps in genetic information, no photo/recording exclusions); H76 (SS.1, 4(i)(E)); S30 (SS.1, 4(i)(E)); S2539 (SS.5, 8(i)(E)); H281 (S.1, weakest: only financial-account-access biometrics, and no separate biometric definition). Rough strength ordering: H76/S30/S2539 and S140 comparable (different definitional boundaries), H281 far narrower.

**93h-personal-info-dob proposition membership**: S198 (entire bill), H76 S.4(i)(F), S30 S.4(i)(F), S2539 S.8(i)(F). Identical mechanism; S198 is the standalone minimal version.

**93h-breach-harm-threshold membership**: H76 S.7, S30 S.7, S2539 S.11 (threshold added to the s.3(b) trigger; harm categories broad: financial, physical, reputational, other cognizable) vs H281 S.1 (threshold embedded in the breach definition; limited to identity theft or fraud). Same mechanism (risk-of-harm gate on the notification duty), different statutory placement and scope; H281 is the weaker variant.

**93h-notice-content-modernization membership**: H76 SS.8-10, S30 SS.8-10, S2539 SS.12, 14, 15, and H281 S.3 — all rewrite the same third-paragraph notice-content provision of c.93H s.3(b). H281 is the weak/legacy variant (short list, permits security-freeze fees, no medical/geolocation carve-outs, no mitigation-services or FTC items); note H281's fee language conflicts with current law and with the other three bills' "no charge" clause.

**Singletons**: 93h-security-program-mandate (H281 S.2 only); 93h-personal-info-public-records-exclusion (H281 S.1 only); 93h-notify-fbi (S2539 S.13 only); commercial-establishment-biometric-id-ban (S195 only); biometric-warrant-notice and biometric-warrant-transparency-reports (H63 only); breach-reporting-insurance-protection (S2539 S.17 only, flagged borderline).

**Grain caveats for atoms.py authoring**: (1) In H76/S30/S2539 the notice-content proposition cross-references subclauses (A)-(J) of the new personal-information definition, so its edge should record a dependency on the expansion propositions. (2) S198's "(d) date of birth" and S140's "(d) a biometric indicator" both claim clause (d) of the current definition — mutually incompatible drafting, same amendment site, different propositions. (3) H63's SECTION 2 (retroactive consent) and SECTION 3 (effective date) are attached to biometric-collection-consent, not standalone. (4) The bills-file scratchpad path shared with other agents got clobbered mid-run; the verified text dump used for this analysis is at /private/tmp/claude-501/-Users-shsingh-Documents-GitHub-misc-ma-policy-ledger/474925a5-d5bb-490b-b655-e4cf902211d4/scratchpad/bills-biom-8271.txt, generated by /Users/shsingh/Documents/GitHub/misc/ma-policy-ledger/pilots/privacy-193rd/scripts/billtext.py.
