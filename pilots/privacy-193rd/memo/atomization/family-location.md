# Atomization working notes: location family

Reading pass over cached bill texts (scripts/billtext.py); companion diffs
verified programmatically. Consolidated into scripts/atoms.py after
cross-checking. Quotes are verbatim from cached text.

Companion diffs verified programmatically (normalized whitespace). Findings below.

## H357
Subject: New G.L. c.93L regulating collection, processing, sale, and disclosure of device-derived location information by private entities ("location shield act").

Cached text note: the as-filed text contains NO reproductive- or gender-affirming-care-specific language; it is a general location-privacy chapter. The care-specific framing belongs to the later H4844 redraft (not covered here).

1. `location-consent-regime` -- Ban on collecting/processing device location information except for enumerated permissible purposes, with prior privacy-policy disclosure and opt-in consent per purpose, one-year consent expiry with mandatory destruction; extends retroactively to pre-existing data. SECTION 1 (c.93L s.1 definitions, s.2(a),(b),(d), s.6 HIPAA carve-out), SECTION 2, SECTION 3. Quote: "unlawful for a covered entity to collect or process an individual's location information except for a permissible purpose"
2. `targeted-ad-optout` -- Entities delivering targeted ads must offer a clear means to opt out of location processing for ad targeting. SECTION 1 (s.2(c)). Quote: "a clear, conspicuous, and simple means to opt out of the processing of their location information"
3. `location-minimization` -- Prohibits collecting more precise data, retaining longer, or deriving inferences beyond what the permissible purpose requires. SECTION 1 (s.2(e)(1),(2),(4)). Quote: "collect more precise location information than necessary to carry out the permissible purpose"
4. `location-sale-disclosure-ban` -- Prohibits sale/rent/trade/lease of location information to third parties and any third-party disclosure not necessary to the purpose or requested by the individual. SECTION 1 (s.2(e)(3),(5)). Quote: "sell, rent, trade, or lease location information to third parties"
5. `govt-access-warrant-gate` -- Prohibits covered entities/service providers from disclosing location information to any government agency absent a valid warrant, exigent circumstances, legal mandate, or subject request. SECTION 1 (s.2(f)). Quote: "serves the covered entity or service provider with a valid warrant or establishes the existence of exigent circumstances"
6. `govt-monetization-ban` -- Prohibits government entities from monetizing location information. SECTION 1 (s.2(i)). Quote: "unlawful for a government entity to monetize location information"
7. `location-privacy-policy-duty` -- Requires maintaining and providing a Location Privacy Policy with seven enumerated contents, plus 20-business-day advance notice and re-consent on changes. SECTION 1 (s.2(g),(h)). Quote: "shall maintain and make available to the data subject a Location Privacy Policy" (coupled to prop 1: the policy is a consent prerequisite in s.2(a))
8. `warrant-transparency-reports` -- Annual aggregate reporting by covered entities to the AG of location-information warrants and legally mandated disclosures, published on standardized public forms. SECTION 1 (s.3(a)-(c)). Quote: "report to the attorney general aggregate information pertaining to any warrants seeking location information"
9. `anti-retaliation` -- Bars adverse action (refusal of service, differential pricing or quality) against individuals exercising chapter rights. SECTION 1 (s.4). Quote: "shall not take adverse action against an individual because the individual exercised or refused to waive"
10. `private-enforcement` -- Private right of action with greater of actual damages or $5,000 per violation plus punitive damages and fees, no mandatory arbitration, waivers void, plus AG c.93A enforcement and AG rulemaking. SECTION 1 (s.5, s.7). Quote: "actual damages, including damages for emotional distress, or $5,000 per violation, whichever is greater" (treated as separate per grain rule: bill segregates enforcement into own sections)

## S148
Subject: identical companion to H357.
Propositions: 1-10 exactly as H357, same section cites. Text is verbatim identical to H357 line-for-line (diff after whitespace normalization: zero differences, including the shared typos "executution" and duplicated "(iii)" absence).

## H1653
Subject: Rewrites G.L. c.276 s.1B (adds 1B-1E, 2A1/2) to require superior-court warrants for government access to stored electronic communication, subscriber, device, and location records; bans reverse warrants; regulates cell site simulators; shields library records.

1. `stored-records-warrant-requirement` -- Government/law enforcement may not obtain electronic information, subscriber information, or device data except by superior-court probable-cause warrant, with service/production procedures (14 days), particularity, warrant forms, and consent/emergency/lost-device exceptions. SECTION 1 (s.1B(a)-(e),(g),(k),(m)), SECTION 2 (s.2A1/2(a)), SECTION 3. Quote: "Except pursuant to a warrant issued by a justice of the superior court" 
2. `subject-notice-of-warrant` -- Requires notice to the data subject within 7 days of execution, with court-ordered delay up to 90 days (renewable) and gag orders on providers only on adverse-result findings. SECTION 1 (s.1B(h)-(j)). Quote: "Not later than 7 days after information is obtained" (attaches closely to prop 1; listed separately because it is a distinct duty on government that could be severed while the warrant gate still functions)
3. `out-of-state-warrant-comity` -- Massachusetts service providers must comply with other states' warrants/subpoenas for customer records as if issued under commonwealth law. SECTION 1 (s.1B(f)). Quote: "shall produce those records as if that warrant or subpoena had been issued under the law of the commonwealth"
4. `warrant-court-reporting` -- Courts report each warrant grant/denial to trial-court office of court management; annual public statistical report to the legislature. SECTION 1 (s.1B(l)). Quote: "shall transmit to the legislature a full and complete report concerning the number of applications for warrants"
5. `reverse-warrant-ban` -- Categorical ban on seeking, issuing, complying with, or laundering through other agencies any reverse-location or reverse-keyword court order or voluntary request. SECTION 1 (s.1C). Quote: "seek, from any court, a reverse-location court order or a reverse-keyword court order"
6. `cell-site-simulator-limits` -- Cell site simulator use limited to locating a specific device under a heightened warrant (felony nexus, least-invasive showing, 15-day term) with mandatory non-target data deletion within 24 hours and target data within 30 days. SECTION 1 (s.1D), SECTION 2 (s.2A1/2(b)). Quote: "unlawful ... to use a cell site simulator device for any purpose other than to locate or track"
7. `violation-remedies` -- For violations of 1B-1D: written notice to victims, exclusionary rule barring derived evidence, private right of action against government (greater of actual damages or $1,000/violation, punitives, fees), no arbitration, waivers void, c.258 inapplicable. SECTION 1 (s.1E). Quote: "no information acquired in violation of said sections, and no evidence derived therefrom, may be received in evidence" (separate per grain rule: own section, exclusionary rule is a distinct mechanism from the duties)
8. `library-records-shield` -- Library user private data excluded from the public-records definition and given the warrant/reverse-warrant/remedy protections of 1B, 1C, 1E. SECTIONS 4, 5 (c.78 s.7, new s.7A). Quote: "Library user private data shall not be a public record"

## S27
Subject: identical companion to H1653.
Propositions: 1-8 exactly as H1653, same section cites. Diff after whitespace normalization: only quote-mark glyphs, one trailing period on the "Location information" definition, and line-break joins in the model warrant forms. No substantive difference; identical propositions with no stricter/weaker variation.

## H1519
Subject: "Kelsey's Bill" -- new G.L. c.6A s.18M compelling wireless carriers and in-vehicle service providers to disclose device location to law enforcement in emergencies and missing-person investigations.

1. `carrier-emergency-location-disclosure` -- Carriers and in-vehicle providers must immediately provide device location information on law enforcement request for 911 response, missing person investigations, or death/serious-harm emergencies, with good-faith civil immunity; carriers must register emergency contacts annually with EOPSS, which maintains a database for public safety answering points and issues regulations. SECTION 1 (s.18M(b)-(e)). Quote: "shall immediately provide location information concerning the telecommunications devices of the user to the requesting law enforcement agency" (contact-registry and database subsections (c),(e) attach as machinery facilitating (b); immunity (d) attaches to the duty it serves; whole bill is one proposition)

## CROSS-BILL

- H357 vs S148: verbatim identical (zero normalized-diff lines). One proposition set, two filings.
- H1653 vs S27: substantively identical; differences are typographic only (quote glyphs, one period, warrant-form line breaks). One proposition set, two filings.
- OVERLAP FLAG (do not merge) - warrant gate on government access to location data: H357/S148 s.2(f) prohibits PRIVATE ENTITIES from disclosing location data to government without a warrant; H1653/S27 s.1B(b) prohibits GOVERNMENT from obtaining it without a warrant. Same goal, different mechanism and regulated party; different propositions under the codebook rule.
- OVERLAP FLAG - warrant transparency reporting: H357/S148 s.3 (covered entities report warrants to the AG, public forms) vs H1653/S27 s.1B(l) (courts report to legislature via trial-court administrator). Same goal, different mechanism and reporter; different propositions.
- OVERLAP FLAG - definitions of "location information": near-shared drafting lineage, but H357/S148 adds a precision threshold ("within a range of 1,850 feet or less") that H1653/S27 omits; H1653/S27 protects location data regardless of precision.
- TENSION FLAG - H1519 mandates warrantless emergency disclosure by carriers; H357/S148 s.2(f)(2) ("mandated under federal or state law") and exigent-circumstances clause, and H1653/S27 s.1B(k)(iii) emergency exception, would accommodate it, but H1519's mechanism (compelled disclosure) runs opposite to the shield bills' mechanism (restricted disclosure) over the same data type and holder class. Different propositions; flag the interaction.
- Enforcement architecture (PRA + no-arbitration + anti-waiver + per-violation statutory damages) is textually parallel between H357/S148 s.5 and H1653/S27 s.1E but targets private entities in one and government agencies in the other, with different damages floors ($5,000 vs $1,000) and an exclusionary rule only in H1653/S27. Different propositions.
- PROMPT DISCREPANCY: the cached H357/S148 texts contain no reproductive-health or gender-affirming-care-specific provisions; that shielding is presumably the H4844 redraft, handled separately by the researcher.
