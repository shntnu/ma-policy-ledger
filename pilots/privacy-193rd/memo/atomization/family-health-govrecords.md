# Atomization working notes: health-govrecords family

Reading pass over cached bill texts (scripts/billtext.py); companion diffs
verified programmatically. Consolidated into scripts/atoms.py after
cross-checking. Quotes are verbatim from cached text.

BILL-BY-BILL ATOMIZATION

=== H386 — Consumer Health Data Act (new c. 93M; regulates commercial collection/sharing/sale of consumer health data)
1. chd-privacy-policy — Regulated entities must maintain and publish on their homepage a Consumer Health Data Privacy Policy disclosing data types, sources, sharing, third parties, and rights, and may not collect/share beyond it without fresh affirmative consent. SECTION 1 (c.93M s.2). "shall maintain a Consumer Health Data Privacy Policy that clearly and conspicuously discloses"
2. chd-optin-consent — Opt-in consent (separate consents for collection and for sharing), or strict necessity for a requested product/service, required before any collection or sharing of consumer health data. SECTION 1 (c.93M s.3(1)-(3)). "shall not collect any Consumer Health Data except: (a) With consent from the consumer"
3. chd-nonretaliation — Ban on discriminating against a consumer (refusal to serve, higher price, lower quality) for exercising chapter rights. SECTION 1 (c.93M s.3(4)). "shall not discriminate against a consumer for exercising any rights included in this chapter"
4. chd-consumer-rights — Consumer rights to know, to withdraw consent, and to deletion within 30 days including flow-down deletion by all third parties notified. SECTION 1 (c.93M s.4). "right to have their Consumer Health Data deleted by informing the Regulated Entity"
5. chd-security-minimization — Need-based internal access restriction, reasonable administrative/technical/physical security practices, and publicly available compliance documentation. SECTION 1 (c.93M s.5). "restrict access to Consumer Health Data ... to only those employees ... for which access is necessary"
6. chd-sale-ban — Flat prohibition on selling consumer health data. SECTION 1 (c.93M s.6). "It shall be unlawful for a Regulated Entity to sell Consumer Health Data."
Attached (not standalone): definitions (s.1), c.93A/Consumer Protection Act enforcement hook declaring violations unfair or deceptive acts (s.7, chapter-wide, attaches to all of P1-P6; companions do not differ), HIPAA exemption and severability (s.8).

=== S184 — Consumer Health Data Act
Body text is character-for-character identical to H386 (verified by diff). Same propositions 1-6, same sections, same attachments.

=== H377 — Pregnancy services centers: deceptive advertising ban and personal-data processing standards (new c.93A 1/2)
1. lspc-deceptive-ad-ban — Limited services pregnancy centers prohibited from making deceptive statements about pregnancy-related services in any advertising medium. SECTION 1 (c.93A1/2 s.2), with corrective-advertising injunctive relief in s.5(b),(f). "any statement concerning any pregnancy-related service ... that: (i) is deceptive"
2. psc-data-processing-standards — Pregnancy services centers may process personal information only with consent, under fair-processing principles (purpose limitation, minimization, retention and security limits), after a privacy notice, with a 15-day consent-revocation mechanism and vendor due diligence. SECTION 1 (c.93A1/2 s.3; limitations/exemptions s.4). "shall not process an individual's personal information unless the center has obtained the individual's consent"
Attached: definitions (s.1); AG enforcement — civil investigative demand, 10-day cure, injunctions, civil penalties up to $1,000 per violation, fees (s.5) — is a single scheme enforcing both P1 and P2 and companions do not differ, so it attaches to each; effective date (bill SECTION 2, 6 months after passage).

=== S174 — Pregnancy services centers (companion to H377)
Same two propositions, same sections. Substantive section-level difference: c.93A1/2 s.3(d) — S174 requires "first: (i) obtaining the individual's consent; and (ii) providing the individual with notice" before incompatible-purpose processing, where H377 requires notice only. Stricter version of the same mechanism = same proposition (psc-data-processing-standards), difference recorded on edge. Remaining diffs are typographical (s.1 "Process" wording, s.4(a)(2) "and", s.5(d)(ii) "attorneys'").

=== S1368 — Health facility waiting-room and common-area patient confidentiality (amends c.111 s.70E)
1. waiting-room-confidentiality-right — Extends the patients-rights confidentiality guarantee to a facility's common areas and waiting rooms. SECTION 1. "confidentiality shall extend to a facility's common areas and waiting rooms"
2. waiting-room-anonymity-system — Providers must implement a facility-wide anonymity system: no announcing patient first/last names; patient numbering or electronic pagers. SECTION 2. "shall not be permitted to announce the first and or last name of patients"
(Split because P1 amends the patient-rights declaration and P2 imposes an operational duty on providers; each survives without the other.)

=== H1442 — 911 call audio privacy (adds c.6A s.18M)
1. e911-audio-confidential — 911 call audio classified as private data on the caller; release prohibited without the caller's express written consent, except court order (public interest balancing), law enforcement investigative dissemination, and public-safety/EMS training use. SECTION 1 (both paragraphs of s.18M). "release of the audio recording of a 911 telephone call without the express written consent of the caller ... shall be prohibited"
2. e911-transcript-public — Written transcript of the 911 audio remains public, prepared upon request at the requester's actual cost. SECTION 1 (s.18M para. 1). "a written transcript of the audio recording is public. A transcript shall be prepared upon request."

=== S1022 — 911 call audio privacy
Substantively identical to H1442 (diff shows only enacting-clause boilerplate and "18M:" vs "18M."). Same propositions e911-audio-confidential and e911-transcript-public, SECTION 1.

=== H4323 — 911 call audio confidentiality, redraft (strikes and replaces c.6A s.18G)
1. e911-audio-confidential — 911 audio not a public record under c.4 s.7; maintained confidentially; releasable only to enumerated recipients (caller/subject and their attorneys, law enforcement, criminal-case parties), with caller consent, for training, or by court order; $1,000 fine for violation. SECTION 1 (s.18G(b)). "shall not be deemed a public record under the provisions of section 7 of chapter 4"
2. e911-transcript-public — Transcript is a public record, prepared on request at requester's cost, with PII of the caller or involved persons redactable. SECTION 1 (s.18G(c)). "A written transcript of the audio recording of a 911 call is a public record."
3. e911-retention-1yr — PSAPs with enhanced 911 must retain 911 recordings at least 1 year. SECTION 1 (s.18G(a)). "shall retain 911 recordings for a period of not less than 1 year"

=== S194 — Lottery winner anonymity (amends c.10 s.24)
1. lottery-winner-anonymity — Winner name/address/identifying info deemed not public records and exempt from c.66 s.10; on the winner's written request the commission may not disclose it or require any public act; commission must notify winners of these refusal rights (notice duty attaches). Single unnumbered SECTION. "shall not be deemed public records of the commission and shall not be subject to section 10 of chapter 66"

=== S938 — Crime victim compensation record confidentiality (adds c.258C s.15)
1. victim-comp-records-confidential — All division records on victim-compensation claims made confidential and privileged, nondisclosable by the division or downstream recipients, with exceptions for claim processing, claimant written consent, criminal-justice purposes at AG discretion, mandatory discovery, and court order. Single unnumbered SECTION (s.15(a)-(b)). "shall be confidential and privileged, and shall not be disclosed by the division"

=== H3863 — Firearm license/transfer record privacy (replaces c.66 s.10B first paragraph; emergency preamble)
1. firearm-records-maintenance-ban — DCJIS, licensing authorities, and all government officials prohibited from maintaining firearm/ammunition transfer records containing personal information. SECTION 1 para. 1. "shall not maintain any records on the transfer of firearms ... that contains any personal information"
2. firearm-records-disclosure-ban — No government disclosure of such information except to criminal justice agencies, to the requester about themselves, or under a warrant for a criminal investigation. SECTION 1 para. 1. "no government official, employee, or agent shall disclose any such information to the general public"
3. firearm-records-destruction — Mandate to destroy all existing transfer/possession records, retract published records, and recover released data. SECTION 1 para. 2. "shall destroy all records regarding the transfer or possession of any firearms"
4. firearm-records-harm-relief — Relief mechanism against DCJIS/licensing authorities for persons harmed by prior release of this information. SECTION 1 para. 3. "demonstrate that they have been harmed or damaged by any prior release"

CROSS-BILL PROPOSITION SHARING

- chd-privacy-policy, chd-optin-consent, chd-nonretaliation, chd-consumer-rights, chd-security-minimization, chd-sale-ban: H386 = S184, exact companions, zero textual difference in the enacted chapter.
- lspc-deceptive-ad-ban: H377 = S174, identical.
- psc-data-processing-standards: H377 and S174; S174 stricter at c.93A1/2 s.3(d) (consent + notice vs notice only for incompatible-purpose processing) — same proposition, strictness noted on edge.
- e911-audio-confidential: H1442 = S1022 (identical text, "private data" framing, consent-or-court-order rule); H4323 same proposition, different drafting: (a) codified by replacing s.18G instead of adding s.18M; (b) mechanism restated as public-records exemption (c.4 s.7) plus confidentiality duty rather than "private data" classification; (c) access list broadened to caller/subject and attorneys and criminal-case parties (H1442/S1022 instead carve law enforcement investigations out of the section entirely); (d) H4323 court-order balancing adds "the victim(s)"; (e) H4323 adds a $1,000 fine (enforcement attaches here; absent from H1442/S1022). Same mechanism at same target; H1442/S1022 vs H4323 differences recorded on edges.
- e911-transcript-public: all of H1442, S1022, H4323; H4323 adds redaction of personally identifying information before release — same proposition, weaker public-access variant noted.
- e911-retention-1yr: H4323 only (no counterpart in H1442/S1022; s.18G retention duty carried over from the statute being replaced, but within this family it is unique to H4323).
- waiting-room propositions (S1368), lottery-winner-anonymity (S194), victim-comp-records-confidential (S938), and the four firearm-records propositions (H3863) are each unique to their single bill; no cross-bill matches within this set. Family-level note: e911-audio-confidential, victim-comp-records-confidential, firearm-records-disclosure-ban, and lottery-winner-anonymity all restrict disclosure of government-held personal information but target different record types via different statutes — different targets, so distinct propositions.

Source files: bill texts cached via /Users/shsingh/Documents/GitHub/misc/ma-policy-ledger/pilots/privacy-193rd/scripts/billtext.py; rules at /Users/shsingh/Documents/GitHub/misc/ma-policy-ledger/pilots/privacy-193rd/memo/codebook.md.
