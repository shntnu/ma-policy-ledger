"""Proposition table for the privacy-193rd pilot (Goal 2 output).

Hand-authored analysis-as-data, consolidated from the per-family reading
notes in memo/atomization/ (which carry verbatim quotes for every
assignment). Validated and compiled to CSV by 06_compile_atoms.py.

PROPS: prop_id -> (slug, subdomain, description)
  IDs are persistent and never reused. Numbering is grouped by family with
  gaps left for later insertions.

EDGES: (bill, prop_id, section_cite, note)
  note records variant status relative to the other bills carrying the same
  proposition ("identical companion", "stricter: ...", "weaker: ...").

OUT_OF_DOMAIN: bill -> description of that bill's content that falls outside
  the domain definition and is therefore not atomized (accounting record).
"""

PROPS = {
    # --- Comprehensive regime, MDPPA lineage (H83/S25 -> H4632/S2770) ---
    "P-001": ("data-minimization-duty-of-loyalty", "comprehensive", "Covered entities may collect/process/transfer covered data only as reasonably necessary for enumerated permissible purposes"),
    "P-002": ("dark-pattern-ban", "comprehensive", "Ban on deceptive statements and manipulative interfaces to induce consent or impair rights"),
    "P-003": ("ssn-restrictions", "comprehensive", "Bar on collecting/processing/transferring Social Security numbers except enumerated uses"),
    "P-004": ("sensitive-data-strict-necessity", "comprehensive", "Sensitive covered data collectible/processable only when strictly necessary for a requested product or enumerated purpose"),
    "P-005": ("sensitive-data-transfer-consent", "comprehensive", "Third-party transfer of sensitive data requires prior consent per transfer"),
    "P-006": ("sensitive-data-targeted-ads-ban", "comprehensive", "Flat ban on processing sensitive covered data for targeted advertising"),
    "P-007": ("consent-request-standards", "comprehensive", "Standalone, symmetric, non-inferable consent requests; new consent for new purposes"),
    "P-008": ("privacy-by-design", "comprehensive", "Duty to maintain reasonable risk-mitigating policies scaled to size and sensitivity"),
    "P-009": ("anti-retaliation-pricing", "comprehensive", "No retaliation or price/quality difference for exercising rights; loyalty-program exception"),
    "P-010": ("privacy-policy-transparency", "comprehensive", "Public privacy policy with categories, purposes, transferees, brokers, retention; change notice"),
    # P-011 retired 2026-08-05: bundled four severable rights, violating the
    # codebook severability test (review finding 4); split into P-271..P-274.
    "P-012": ("opt-out-rights-transfers-ads", "comprehensive", "Rights to withdraw consent and opt out of third-party transfers and targeted advertising"),
    "P-013": ("profiling-opt-out", "comprehensive", "Right to opt out of profiling in furtherance of decisions with legal or similarly significant effects"),
    "P-014": ("authorized-agents-opt-out-signals", "comprehensive", "Rights exercisable through authorized agents and browser/device opt-out preference signals"),
    "P-015": ("minors-targeted-ads-ban", "comprehensive", "No targeted advertising to individuals known (tiered standard) to be under 18"),
    "P-016": ("data-broker-registration-ocabr", "comprehensive", "Data broker website notice plus annual OCABR registration and public registry"),
    "P-017": ("civil-rights-nondiscrimination", "comprehensive", "Ban on data practices that discriminate (disparate impact) on protected characteristics"),
    "P-018": ("algorithm-impact-assessments", "comprehensive", "Annual covered-algorithm impact assessments by large holders; pre-deployment design evaluations filed with AG"),
    "P-019": ("centralized-opt-out-mechanism", "comprehensive", "OCABR must establish or recognize centralized privacy-protective opt-out mechanisms"),
    "P-020": ("privacy-security-officers", "comprehensive", "Mandatory designated privacy officers and data security officers"),
    "P-021": ("large-holder-privacy-impact-assessment", "comprehensive", "Biennial privacy impact assessment by large data holders"),
    "P-022": ("service-provider-third-party-duties", "comprehensive", "Service providers bound to instructions by contract; third parties limited to disclosed purposes"),
    "P-023": ("comprehensive-private-right-of-action", "comprehensive", "Private action with liquidated damages (0.15% global revenue or $15,000/violation), anti-arbitration"),
    "P-024": ("comprehensive-ag-enforcement", "comprehensive", "AG enforcement via c.93A with penalties up to 4% global revenue or $20M per action"),
    "P-025": ("complaint-retaliation-ban", "comprehensive", "Unlawful to retaliate for good-faith compliance complaints"),
    "P-026": ("legal-request-transparency-reports", "comprehensive", "Bi-monthly aggregate public reports of legal requests received (warrants, orders, subpoenas)"),
    "P-027": ("interactive-computer-service-carveout", "comprehensive", "s.230-style carve-out: hosting user-provided personal information is not processing"),
    "P-028": ("workplace-surveillance-limits", "workplace", "Employer electronic monitoring limited to enumerated purposes, least-invasive means, advance notice"),
    # --- Comprehensive regime, MIPSA lineage (H60/S227); GDPR-style props shared with H1555 where same mechanism ---
    "P-031": ("gdpr-processing-principles", "comprehensive", "Fair, purpose-limited, minimized, accurate, storage-limited, secure processing principles (GDPR art.5 style)"),
    "P-032": ("gdpr-lawful-basis", "comprehensive", "Processing lawful only on enumerated bases (consent, contract, legal obligation, vital/legitimate interests)"),
    "P-033": ("gdpr-privacy-notice", "comprehensive", "Mandatory point-of-collection privacy notice of categories, purposes, sales, retention"),
    "P-034": ("mipsa-optout-sale-ads", "comprehensive", "Opt-out of sale, targeted cross-contextual and first-party advertising, honored via universal opt-out signal"),
    "P-035": ("gdpr-sensitive-info-gate", "comprehensive", "Sensitive/special-category information processable only with opt-in consent or enumerated exceptions"),
    # P-036 retired 2026-08-05: bundled access and portability; split into
    # P-275/P-276 for consistency with the severability test.
    "P-037": ("gdpr-right-delete", "comprehensive", "Right to deletion/erasure with downstream notification and retention exceptions"),
    "P-038": ("gdpr-right-correct", "comprehensive", "Right to correction/rectification of inaccurate personal information"),
    "P-039": ("mipsa-right-revoke-consent", "comprehensive", "Right to revoke previously given consent via easy conspicuous mechanism"),
    "P-040": ("mipsa-nondiscrimination", "comprehensive", "No denying, degrading, or repricing service for exercising rights; loyalty exception; waivers void"),
    "P-041": ("gdpr-processor-contracts", "comprehensive", "Mandatory controller-processor contracts (instructions, confidentiality, audits, deletion)"),
    "P-042": ("mipsa-databroker-registration-ag", "comprehensive", "Annual data broker registration with the AG, public registry, centralized broker opt-out"),
    "P-043": ("gdpr-risk-assessments", "comprehensive", "Documented pre-processing risk assessments for high-risk processing (DPIA family)"),
    "P-044": ("mipsa-antidiscrimination-processing", "comprehensive", "Ban on processing that discriminates in equal enjoyment of goods/services by protected class"),
    "P-045": ("mipsa-ag-enforcement", "comprehensive", "Exclusive AG enforcement with CIDs, 30-day cure, civil penalties to $7,500/violation"),
    "P-046": ("mipsa-breach-private-action", "comprehensive", "Private action limited to security breaches from unreasonable controls; NIST safe harbor"),
    "P-047": ("mipsa-privacy-fund", "comprehensive", "Dedicated Massachusetts Privacy Fund from penalties and fees"),
    "P-048": ("mipsa-reciprocity", "comprehensive", "Deemed compliance for entities under AG-certified equally protective laws"),
    "P-049": ("mipsa-nonprofit-highered-scope", "comprehensive", "Extension of the chapter to nonprofits and higher education (delayed)"),
    # --- Internet bill of rights (H1555) unique mechanisms ---
    "P-051": ("ibor-child16-parental-consent", "children", "Parental consent required for information-society services to children under 16"),
    "P-052": ("ibor-right-restriction", "comprehensive", "Right to obtain restriction of processing (freeze pending disputes)"),
    "P-053": ("ibor-right-object-marketing", "comprehensive", "Right to object to processing; absolute objection right for direct marketing/profiling"),
    "P-054": ("ibor-automated-decisions", "comprehensive", "Right not to be subject to solely automated decisions with legal effects; human intervention"),
    "P-055": ("ibor-design-default-records", "comprehensive", "Data protection by design/default plus records-of-processing duty"),
    "P-056": ("ibor-instate-representative", "comprehensive", "Out-of-state controllers targeting MA must designate an in-commonwealth representative"),
    "P-057": ("ibor-security-measures", "data-security", "Risk-appropriate technical/organizational security including pseudonymization and encryption"),
    "P-058": ("ibor-breach-notification-72h", "data-security", "Breach notification to AG within 72 hours and to subjects when high-risk"),
    "P-059": ("ibor-data-protection-officer", "comprehensive", "Mandatory data protection officer for public bodies and large-scale processors"),
    "P-060": ("ibor-codes-certification", "comprehensive", "AG-approved codes of conduct and voluntary certification seals"),
    "P-061": ("ibor-cross-border-transfers", "comprehensive", "Out-of-state transfers only under AG adequacy decisions, safeguards, or derogations"),
    "P-062": ("ibor-ag-supervision-fines", "comprehensive", "AG as supervisory authority with GDPR-scale administrative fines (to $20M/4% turnover)"),
    "P-063": ("ibor-general-damages-pra", "comprehensive", "Judicial remedy and compensation for material and non-material damage; representative actions"),
    # --- Data sale, ISP, and municipal internet ---
    "P-065": ("data-seller-dor-registration", "data-brokers", "Annual DOR registration by sellers of residents' personal data, disclosing buyers and income; tax design report"),
    "P-066": ("ice-data-sale-ban", "data-brokers", "Ban on selling personal information to ICE or intermediaries"),
    "P-067": ("police-officer-pii-posting-ban", "govt-records", "Criminal penalty for publicly posting police officers' or family's personal information without consent"),
    "P-068": ("isp-optin-consent", "isp", "Franchised ISPs/telecoms may not collect/use/disclose customer personal information without express written approval; no surcharge or denial"),
    "P-069": ("isp-sale-written-authorization", "isp", "ISP sale of customer PII requires express written revocable authorization"),
    "P-070": ("muni-isp-data-minimization", "isp", "Public broadband may not collect/use/retain usage data beyond service necessity; de-identify and drop"),
    "P-071": ("muni-isp-collection-notice", "isp", "Public, accessible, translated notice of public-ISP data collection and retention"),
    "P-072": ("muni-isp-thirdparty-optin", "isp", "No public-ISP data sharing with third parties except contractors or with opt-in consent"),
    "P-073": ("muni-isp-anonymous-wifi", "isp", "No identification requirement to access public wifi"),
    "P-074": ("muni-isp-data-profile-access", "isp", "Public-ISP users may request their data profile and a report of information collected or shared"),
    "P-075": ("muni-isp-breach-notice", "isp", "Public-ISP reasonable security, encryption, and prompt user breach notification"),
    "P-076": ("muni-isp-warrant-requirement", "isp", "Public-ISP user data released to law enforcement only with warrant; user notified of requests"),
    # --- Biometric standalone acts ---
    "P-081": ("biometric-collection-consent", "biometric", "No collection/processing of biometric information without notice and opt-in written consent"),
    "P-082": ("biometric-privacy-policy-retention", "biometric", "Mandatory public biometric privacy/retention-destruction policy"),
    "P-083": ("biometric-disclosure-limits", "biometric", "Ban on disclosing biometric information except enumerated consent/legal exceptions"),
    "P-084": ("biometric-monetization-ban", "biometric", "Ban on selling, leasing, trading, or profiting from biometric information"),
    "P-085": ("biometric-security-standard", "biometric", "Duty to protect biometric data at industry standard and as protectively as other sensitive data"),
    "P-086": ("biometric-warrant-notice", "biometric", "Entity receiving a biometric warrant must notify the individual, subject to court delay"),
    "P-087": ("biometric-warrant-transparency-reports", "biometric", "Annual aggregate reporting to AG of biometric warrants and mandated disclosures"),
    "P-088": ("biometric-enforcement-pra", "biometric", "Private right of action and AG enforcement for biometric violations"),
    "P-089": ("commercial-establishment-biometric-id-ban", "biometric", "Entertainment/retail/food establishments may not use biometrics to identify persons"),
    # --- c.93H breach-law amendments ---
    "P-091": ("93h-personal-info-biometric", "data-security", "Add a biometric element to the c.93H personal information definition"),
    "P-092": ("93h-personal-info-dob", "data-security", "Add date of birth to the c.93H personal information definition"),
    "P-093": ("93h-personal-info-expanded-categories", "data-security", "Add taxpayer/passport/government IDs, genetic, health insurance, medical, geolocation to c.93H personal information"),
    "P-094": ("93h-login-credentials-breach", "data-security", "Extend breach law to standalone online-account credentials with credential-specific notice"),
    "P-095": ("93h-breach-definition-modernization", "data-security", "Restate breach of security around electronic data and acquired encryption keys"),
    "P-096": ("93h-breach-harm-threshold", "data-security", "Condition breach notification on a risk-of-harm test"),
    "P-097": ("93h-notice-content-modernization", "data-security", "Rewrite required breach-notice contents (dates, data types, freeze, mitigation services)"),
    "P-098": ("93h-notify-fbi", "data-security", "Add the FBI as a mandatory breach-notification recipient"),
    "P-099": ("93h-security-program-mandate", "data-security", "Statutory comprehensive written information security program requirement via OCABR regulations"),
    "P-100": ("93h-personal-info-public-records-exclusion", "data-security", "Exclude lawfully obtained public information from c.93H personal information"),
    "P-101": ("breach-reporting-insurance-protection", "data-security", "Contracts and cyber-insurance may not prohibit/limit reporting incidents or breaches to government"),
    # --- Location shield (H357/S148 c.93L; absorbed as c.93N in H4632/S2770) ---
    "P-121": ("location-consent-regime", "location", "Device location information collectible only for permissible purposes with per-purpose opt-in consent and expiry"),
    "P-122": ("location-targeted-ad-optout", "location", "Opt-out of location processing for targeted advertising"),
    # P-123 and P-124 retired 2026-08-05: each bundled separately severable
    # clauses (second-pass review finding 4); split into P-281..P-285.
    "P-125": ("location-govt-access-warrant-gate", "location", "No disclosure of location information to government absent warrant, exigency, legal mandate, or subject request"),
    "P-126": ("location-govt-monetization-ban", "location", "Government entities may not monetize location information"),
    "P-127": ("location-privacy-policy-duty", "location", "Mandatory Location Privacy Policy with enumerated contents and change re-consent"),
    "P-128": ("location-warrant-transparency-reports", "location", "Annual aggregate reporting to AG of location warrants and mandated disclosures"),
    "P-129": ("location-anti-retaliation", "location", "No adverse action for exercising location-privacy rights"),
    "P-130": ("location-private-enforcement", "location", "Private right of action ($5,000/violation or actual damages), anti-arbitration, AG c.93A enforcement"),
    # --- Stored-records warrant regime (H1653/S27) ---
    "P-131": ("stored-records-warrant-requirement", "electronic-privacy", "Government access to stored electronic/subscriber/device/location records only by superior-court warrant"),
    "P-132": ("warrant-subject-notice", "electronic-privacy", "Notice to the data subject within 7 days of warrant execution, with court-ordered delay"),
    "P-133": ("out-of-state-warrant-comity", "electronic-privacy", "MA providers comply with other states' warrants as if issued under commonwealth law"),
    "P-134": ("warrant-court-reporting", "electronic-privacy", "Courts report warrant grants/denials; annual public statistical report to the legislature"),
    "P-135": ("reverse-warrant-ban", "electronic-privacy", "Ban on reverse-location and reverse-keyword court orders and voluntary requests"),
    "P-136": ("cell-site-simulator-limits", "electronic-privacy", "Cell site simulators only under heightened warrant with mandatory data deletion"),
    "P-137": ("stored-records-violation-remedies", "electronic-privacy", "Exclusionary rule plus private action against government for stored-records violations"),
    "P-138": ("library-records-shield", "electronic-privacy", "Library user data excluded from public records and given warrant protections"),
    "P-139": ("carrier-emergency-location-disclosure", "location", "Carriers must provide device location to law enforcement for 911/missing-person emergencies with immunity"),
    # --- Student and education data ---
    "P-141": ("edtech-operator-targeted-ad-ban", "student", "K-12 edtech operators may not target advertising based on school-acquired information"),
    "P-142": ("edtech-operator-profiling-ban", "student", "Operators may not amass student/educator profiles except for school purposes"),
    "P-143": ("edtech-operator-sale-ban", "student", "Ban on sale or rental of student information"),
    "P-144": ("edtech-operator-disclosure-limits", "student", "Operator disclosure of covered information limited to legal compulsion, research, educational entities"),
    "P-145": ("edtech-operator-reasonable-security", "student", "Operators must maintain reasonable security procedures for covered information"),
    "P-146": ("edtech-operator-return-destroy", "student", "Operators must return or destroy covered information on request or when no longer needed"),
    "P-147": ("edtech-contract-mandatory-terms", "student", "Mandatory data-protection clauses in every educational-entity/operator contract; noncompliant contracts voidable"),
    "P-148": ("dese-data-governance-cpo", "student", "Board data-privacy regulations plus a DESE chief privacy officer and educator-prep curricula"),
    "P-149": ("dese-data-inventory-transparency", "student", "DESE must publish categories of covered information it collects with source and purpose"),
    "P-150": ("district-privacy-policy-breach-reporting", "student", "District privacy policies with 10-day breach reporting and student data managers"),
    "P-151": ("district-data-inventory-operator-list", "student", "Districts publish collected-data categories and operator contracts (current and 10-year)"),
    "P-152": ("district-staff-privacy-training", "student", "Annual district staff data-privacy training tied to certification"),
    "P-153": ("public-records-ferpa-exemption", "student", "Public higher-ed FERPA education records exempt from the public records law"),
    "P-154": ("e2c-center-system-board", "govt-data", "Education-to-Career Data Center, longitudinal data system, and governing board with privacy duties"),
    "P-155": ("e2c-agency-data-mandate", "govt-data", "EEC/DESE/DHE/DUA must provide data to the system at least annually"),
    "P-156": ("e2c-ferpa-authorized-rep", "govt-data", "Center deemed FERPA authorized representative to access student record and wage data"),
    "P-157": ("e2c-strategic-initiative-evaluation", "govt-data", "Board may designate strategic initiatives for enhanced data collection/evaluation"),
    "P-158": ("e2c-local-rpp-linking", "govt-data", "Municipal research-practice partnerships linking local data to the system"),
    "P-159": ("student-social-media-password-ban-highered", "student", "Higher-ed institutions may not demand access to students' personal social media accounts"),
    "P-160": ("student-social-media-password-ban-k12", "student", "K-12 institutions may not demand access to students' personal social media accounts"),
    "P-161": ("employee-social-media-password-ban", "workplace", "Employers may not demand access to employees'/applicants' personal social media accounts"),
    "P-162": ("minor-directed-prohibited-product-ads", "children", "Ban on marketing enumerated adult products on minor-directed sites or to known minors"),
    "P-163": ("minor-info-marketing-use-ban", "children", "Ban on using/compiling minors' personal information to market prohibited products"),
    "P-164": ("minor-eraser-right", "children", "Registered minors may remove or obtain removal of content they posted"),
    "P-165": ("children-social-media-commission", "children", "Special commission on children's mental health and social media incl. algorithm audits, age-verification privacy, data practices"),
    # --- Facial recognition and surveillance-technology data ---
    "P-171": ("le-biometric-surveillance-ban", "surveillance-tech", "Default ban on law enforcement acquiring or using biometric surveillance technology"),
    "P-172": ("rmv-fr-identity-verification", "surveillance-tech", "RMV may use facial recognition to verify identity when issuing licenses"),
    "P-173": ("state-police-fr-gateway", "surveillance-tech", "All FR searches centralized in one state police unit for enumerated purposes with vetted technology"),
    "P-174": ("emergency-fr-court-filing", "surveillance-tech", "Emergency FR searches documented in sworn statement filed with superior court within 48 hours"),
    "P-175": ("fr-defendant-notice-discovery", "surveillance-tech", "Defendants identified via FR get notice and discovery of search records and algorithm"),
    "P-176": ("le-fr-search-transparency", "surveillance-tech", "Public records of each FR search, quarterly reports, annual disaggregated statistics"),
    "P-177": ("nonle-agency-fr-transparency", "surveillance-tech", "Non-LE public agencies record and report their FR searches"),
    "P-178": ("emotion-video-analysis-ban", "surveillance-tech", "Absolute ban on LE biometric emotion inference and moving-image analysis"),
    "P-179": ("rmv-fr-search-public-notice", "surveillance-tech", "RMV must post and distribute public notice of FR searches of license photos"),
    "P-181": ("drone-operation-gateway", "surveillance-tech", "Government drones operable only under warrant, non-LE purposes, or documented emergency"),
    "P-182": ("drone-data-minimization", "surveillance-tech", "Drone warrant flights collect data only on the subject; non-target data deleted within 24 hours"),
    "P-183": ("drone-biometric-analysis-ban", "surveillance-tech", "No facial recognition or biometric matching of drone data except as judicially authorized"),
    "P-184": ("drone-first-amendment-shield", "surveillance-tech", "No drone collection on political/religious/social views absent probable-cause investigation"),
    "P-185": ("drone-exclusionary-rule", "surveillance-tech", "Unlawfully acquired drone information inadmissible in any proceeding"),
    "P-186": ("drone-warrant-subject-notice", "surveillance-tech", "Drone warrant subject served notice within 7 days, with court-ordered delay"),
    "P-187": ("drone-warrant-judicial-reporting", "surveillance-tech", "Judges annually report drone warrants; annual public report to the legislature"),
    "P-191": ("alpr-use-restriction", "surveillance-tech", "Government ALPR use limited to law-enforcement purposes and DOT tolls/parking"),
    "P-192": ("alpr-accuracy-verification", "surveillance-tech", "24-hour hot-list updates and human confirmation before acting on ALPR alerts"),
    "P-193": ("alpr-le-48h-destruction", "surveillance-tech", "Law enforcement must destroy ALPR data within 48 hours (optional transfer to EOPSS)"),
    "P-194": ("alpr-eopss-120day-retention", "surveillance-tech", "EOPSS retains transferred ALPR data 120 days then destroys, absent legal process"),
    "P-195": ("alpr-vendor-retention-parity", "surveillance-tech", "No government contracts with private ALPR vendors exceeding the 120-day retention standard"),
    "P-196": ("alpr-access-limits", "surveillance-tech", "Default ban on government access/search/disclosure of ALPR data with enumerated exceptions"),
    "P-197": ("alpr-secondary-use-ban", "surveillance-tech", "No ALPR data use for credit, insurance, employment, or marketing decisions"),
    "P-198": ("alpr-admissibility-limits", "surveillance-tech", "Suppression of unlawfully obtained ALPR data; civil/administrative inadmissibility"),
    "P-199": ("alpr-private-right-of-action", "surveillance-tech", "Civil action with treble or exemplary damages for ALPR violations"),
    "P-200": ("alpr-ag-enforcement", "surveillance-tech", "AG enforcement of the ALPR chapter"),
    "P-201": ("alpr-annual-reporting", "surveillance-tech", "EOPSS annual report to the legislature on ALPR systems and volumes"),
    # --- Vehicle, tolling, and tracking ---
    "P-205": ("toll-tech-purpose-limitation", "location", "Toll collection technology usable only for tolling purposes"),
    "P-206": ("toll-data-le-warrant", "location", "No tolling-derived data to law enforcement without warrant/production order; emergency procedure"),
    "P-207": ("toll-data-exclusionary-rule", "location", "Data obtained in violation inadmissible in proceedings"),
    "P-208": ("toll-data-private-action", "location", "Civil action with exemplary or treble damages for tolling-data violations"),
    "P-209": ("toll-data-93a-hook", "location", "Use of violation-obtained tolling data is itself a c.93A violation"),
    "P-210": ("dot-tolling-access-restriction", "location", "MassDOT barred from accessing/disclosing tolling data except four enumerated purposes"),
    "P-211": ("tolling-data-120day-destruction", "location", "Mandatory permanent erasure of tolling data 120 days after creation"),
    "P-212": ("toll-data-ag-enforcement", "location", "AG enforcement of the driver-privacy chapter"),
    "P-213": ("alpr-14day-retention-90K", "surveillance-tech", "ALPR restrictions under proposed c.90K: no protected-activity tracking, 14-day retention cap, warrant for access"),
    "P-214": ("vehicle-telematics-le-warrant", "location", "Warrant requirement extended to OEM/telematics/aftermarket GPS vehicle data held by private parties"),
    "P-215": ("vehicle-tracking-device-criminal-ban", "location", "Criminal ban on nonconsensual installation of tracking devices on motor vehicles"),
    # --- Commercial data practices ---
    # P-221/P-222 retired 2026-08-05: H3217 excluded under the symmetric
    # program-incident rule (see codebook revision log).
    "P-223": ("trigger-lead-solicitation-93a", "commercial", "Mortgage trigger-lead solicitation practices declared unfair/deceptive under c.93A"),
    "P-224": ("billing-data-pass-prohibition", "commercial", "Seller may not pass consumer billing information to another seller without affirmative consent"),
    "P-225": ("financial-institution-nondisclosure", "commercial", "Financial institutions barred from disclosing customer financial/personal information without authorization"),
    "P-226": ("malicious-doxing-civil-action", "interpersonal", "Civil action for malicious nonconsensual dissemination of personal information to facilitate harassment"),
    # --- Online advertising (H395) ---
    "P-231": ("ad-network-notice", "advertising", "Ad networks must post notice of collection/use/retention and profiling practices"),
    "P-232": ("publisher-privacy-policy-requirement", "advertising", "Networks must contractually require publisher privacy policies with opt-out link"),
    "P-233": ("opm-opt-out", "advertising", "Consumer right to opt out of online preference marketing"),
    "P-234": ("sensitive-data-opm-opt-in", "advertising", "Affirmative consent before using sensitive medical/financial/sexual data for preference marketing"),
    "P-235": ("pii-merger-consent", "advertising", "Consent required before merging non-PII with PII"),
    "P-236": ("ad-network-data-security", "advertising", "Reasonable efforts to protect collected ad data"),
    "P-237": ("ad-network-consumer-access", "advertising", "Consumer access right to retained PII held by ad networks"),
    "P-238": ("ad-data-24month-retention-limit", "advertising", "Ad-delivery data deleted within 24 months of collection"),
    "P-239": ("ad-network-ag-enforcement", "advertising", "AG enforcement with $1,000 statutory penalties, treble for pattern-and-practice"),
    # --- Consumer health data ---
    "P-241": ("chd-privacy-policy", "health", "Consumer Health Data Privacy Policy published on homepage; no collection beyond it without fresh consent"),
    "P-242": ("chd-optin-consent", "health", "Opt-in consent (separate for collection and sharing) before handling consumer health data"),
    "P-243": ("chd-nonretaliation", "health", "No discrimination against consumers exercising health-data rights"),
    # P-244 retired 2026-08-05: bundled severable rights; split into
    # P-277/P-278 (consent withdrawal attaches to P-242's consent mechanism).
    "P-245": ("chd-security-minimization", "health", "Need-based access restriction and reasonable security for consumer health data"),
    "P-246": ("chd-sale-ban", "health", "Flat ban on selling consumer health data"),
    "P-247": ("psc-data-processing-standards", "health", "Pregnancy services centers may process personal information only with consent under fair-processing principles"),
    # --- Government-held records disclosure restrictions ---
    "P-251": ("e911-audio-confidential", "govt-records", "911 call audio confidential; release restricted to consent, court order, or enumerated recipients"),
    "P-252": ("e911-transcript-public", "govt-records", "Written 911 transcript remains public, prepared at requester's cost"),
    "P-253": ("e911-retention-1yr", "govt-records", "PSAPs must retain 911 recordings at least one year"),
    "P-254": ("lottery-winner-anonymity", "govt-records", "Lottery winner identity not a public record; nondisclosure on winner request"),
    "P-255": ("victim-comp-records-confidential", "govt-records", "Victim-compensation claim records confidential and privileged"),
    "P-256": ("firearm-records-maintenance-ban", "govt-records", "Government may not maintain firearm-transfer records containing personal information"),
    "P-257": ("firearm-records-disclosure-ban", "govt-records", "No government disclosure of firearm licensee personal information except enumerated purposes"),
    "P-258": ("firearm-records-destruction", "govt-records", "Mandate to destroy existing firearm transfer/possession records"),
    "P-259": ("firearm-records-harm-relief", "govt-records", "Relief mechanism for persons harmed by prior release of firearm records"),
    "P-260": ("waiting-room-confidentiality-right", "health", "Patient confidentiality guarantee extended to common areas and waiting rooms"),
    "P-261": ("waiting-room-anonymity-system", "health", "No announcing patient names; numbering or pager systems required"),
    # P-265 retired 2026-08-05: H4844 is re-atomized as narrowed variants of
    # the location-family propositions P-121/P-123/P-124/P-125 (review
    # finding 3: the single edge omitted severable mechanisms and misstated
    # the official PDF, which does contain a sale/rent/trade/gift/lease ban).
    # --- NDII / abuse-prevention lineage (H1745/S1012/S1139 -> H4115 ->
    # H4241 -> H4744 -> 2024 c.118), admitted after the enacted-vehicle
    # feedback loop and the boundary revision recorded in the codebook ---
    "P-266": ("ndii-distribution-ban", "interpersonal", "Criminal offense to distribute identifiable nude or sexual visual material without consent, with intent to harm/harass/threaten or reckless disregard; enacted version adds deepfake 'digitization' coverage (threat appears as an intent element, not a standalone offense; repeat-offender penalty attaches)"),
    "P-280": ("ndii-court-record-confidentiality", "govt-records", "Visual material in court records of an NDII prosecution is closed to public inspection; inspection limited to enumerated persons absent court order"),
    # P-267 retired 2026-08-05: bundled three severable rulemaking mandates
    # and misstated the deletion trigger; split into P-287..P-289.
    # --- splits of retired P-011 (H83/S25 lineage individual rights) ---
    "P-271": ("comp-right-access", "comprehensive", "Right to access covered data collected about the individual (24-month lookback as filed)"),
    "P-272": ("comp-right-correct", "comprehensive", "Right to correct verifiable substantial inaccuracies in covered data"),
    "P-273": ("comp-right-delete", "comprehensive", "Right to delete covered data about the individual"),
    "P-274": ("comp-right-export", "comprehensive", "Right to export covered data in a portable, machine-readable format"),
    # --- splits of retired P-036 (MIPSA/H1555 GDPR-style rights) ---
    "P-275": ("gdpr-right-access", "comprehensive", "Right to obtain the specific pieces of personal information processed about the individual"),
    "P-276": ("gdpr-right-portability", "comprehensive", "Right to receive personal information in a structured machine-readable format and transmit it"),
    # --- splits of retired P-244 (consumer health data rights) ---
    "P-277": ("chd-right-know", "health", "Consumer right to know what consumer health data is collected and shared"),
    "P-278": ("chd-right-delete", "health", "Consumer right to 30-day deletion of consumer health data with third-party flow-down"),
    # --- splits of retired P-123/P-124 (location minimization and sale/disclosure) ---
    "P-281": ("location-precision-limit", "location", "No collecting more precise location information than the permissible purpose requires"),
    "P-282": ("location-retention-limit", "location", "No retaining location information longer than the permissible purpose requires"),
    "P-283": ("location-inference-limit", "location", "No deriving or inferring beyond the permissible purpose from location information"),
    "P-284": ("location-sale-ban", "location", "Ban on selling, renting, trading, gifting, or leasing location information to third parties"),
    "P-285": ("location-thirdparty-disclosure-limit", "location", "No third-party disclosure of location information unless necessary to the purpose or requested"),
    "P-286": ("location-govt-disclosure-notice-rulemaking", "location", "Directs AG regulations requiring notice to the individual of any government disclosure of care-location information"),
    # --- splits of retired P-267 (S2539 AI-training-data rulemaking) ---
    "P-287": ("ai-training-data-security-rulemaking", "comprehensive", "Directs regulations requiring security measures for individuals' data used in AI training"),
    "P-288": ("ai-training-data-consent-rulemaking", "comprehensive", "Directs regulations requiring informed consent before collecting, using, sharing, or disclosing individuals' data for AI training"),
    "P-289": ("ai-training-data-deletion-rulemaking", "comprehensive", "Directs regulations requiring deletion or de-identification of AI training data when no longer needed"),
    # P-290 retired 2026-08-05: bundled the sealing regime with independently
    # operative consumer-reporting-agency duties (third-pass review finding
    # 4); split into P-295/P-296.
    # --- notary personal information (H1525/S943; enacted 2023 c.2 s.33) ---
    "P-291": ("notary-personal-info-use-restriction", "commercial", "Notaries may not use, sell, or transfer identifying personal information acquired in a notarial act except for enumerated purposes"),
    # P-292 retired 2026-08-05: bundled the collection standard with the
    # PII-confidentiality/publication restriction; split into P-297/P-298.
    # --- SFI withholding (H2991; enacted expanded at 2024 c.248 s.27) ---
    "P-294": ("sfi-personal-info-withholding", "govt-records", "Ethics commission must withhold filers' personal contact information (home address; enacted version adds email, phone, family member identity) from public statements of financial interests"),
    # --- splits of retired P-290 (eviction sealing, HOMES lineage; enacted 2024 c.150) ---
    "P-295": ("eviction-record-sealing-regime", "govt-records", "Petition-based sealing of eviction court records with tiered waiting periods; sealed records closed to public inspection with limited re-access purposes"),
    "P-296": ("sealed-eviction-cra-duties", "commercial", "Consumer reporting agencies may not disclose or use sealed eviction records and must remove them within 30 days of sealing"),
    # --- splits of retired P-292 (demographic data, H3003; enacted 2023 c.28 s.7) ---
    "P-297": ("demographic-data-collection-standard", "govt-data", "Government agencies collecting race/ethnicity data must use separate, voluntarily self-identified categories"),
    "P-298": ("demographic-pii-confidentiality", "govt-data", "Personal identifying information in agency demographic data is confidential; only aggregated data preventing identification may be published"),
    # --- bus-camera data rules (S2884; enacted 2024 c.363) ---
    "P-299": ("bus-camera-records-exemption", "surveillance-tech", "Bus-camera photographs and personal identifying information exempt from the public records law"),
    "P-300": ("bus-camera-litigation-limits", "surveillance-tech", "Bus-camera evidence not discoverable or admissible outside enforcement proceedings absent a court order with materiality findings"),
    "P-301": ("bus-camera-occupant-id-ban", "surveillance-tech", "Bus-camera photographs may not be used to identify vehicle occupants or contents; mandatory redaction before notices issue"),
    "P-302": ("bus-camera-vendor-confidentiality", "surveillance-tech", "Enforcing authorities and camera vendors must keep camera data confidential; no use, disclosure, sale, or access beyond violation processing"),
    # --- TNC trip-data regime (outside section; enacted 2024 c.206 s.15 via H4799) ---
    "P-303": ("tnc-trip-data-reporting-mandate", "location", "TNCs must report trip-level data monthly, including continuous 60-second in-ride geolocation, driver identifier, and vehicle plate, to the DPU division"),
    "P-304": ("tnc-trip-data-confidentiality", "location", "Reported TNC trip data is not a public record; sharing only de-identified under confidentiality agreements with listed agencies; breach triggers destruction and notification"),
}

# Retired proposition IDs (never reused). Kept for the audit trail.
RETIRED = {
    "P-011": "split into P-271..P-274 (severability, review finding 4)",
    "P-036": "split into P-275/P-276 (severability consistency)",
    "P-244": "split into P-277/P-278 (severability consistency)",
    "P-265": "H4844 re-atomized onto location-family propositions as narrowed variants (review finding 3)",
    "P-123": "split into P-281/P-282/P-283 (second-pass review finding 4)",
    "P-124": "split into P-284/P-285 (second-pass review finding 4)",
    "P-267": "split into P-287/P-288/P-289 with corrected descriptions (second-pass review finding 6)",
    "P-221": "H3217 excluded under the symmetric program-incident rule",
    "P-222": "H3217 excluded under the symmetric program-incident rule",
    "P-290": "split into P-295/P-296 (third-pass review finding 4)",
    "P-292": "split into P-297/P-298 (third-pass review finding 4)",
    "P-318": "split into P-350/P-351 (fourth-pass review finding 5)",
    "P-319": "split into P-352/P-353 (fourth-pass review finding 5)",
    "P-345": "split into P-354/P-355/P-356 (fourth-pass review finding 5)",
    "P-347": "split into P-357/P-358/P-359 (fourth-pass review finding 5)",
}

# (bill, prop_id, section_cite, note)
E = []
def edges(bill, *pairs):
    for prop, cite, note in pairs:
        E.append((bill, prop, cite, note))

_C93L = [  # H83/S25 filed comprehensive: prop -> section
    ("P-001", "c.93L s.2", ""), ("P-002", "c.93L ss.2(c),4(c),8(b),9(e)", ""),
    ("P-003", "c.93L s.3(1)", ""), ("P-004", "c.93L ss.1,3(2)", ""),
    ("P-005", "c.93L s.3(3)", ""), ("P-006", "c.93L s.3(4)", ""),
    ("P-007", "c.93L s.4", ""), ("P-008", "c.93L s.5", ""),
    ("P-009", "c.93L s.6", ""), ("P-010", "c.93L s.7", ""),
    ("P-271", "c.93L s.8", "24-month lookback; 30-day response"),
    ("P-272", "c.93L s.8", ""), ("P-273", "c.93L s.8", ""),
    ("P-274", "c.93L s.8", ""),
    ("P-012", "c.93L s.9", ""), ("P-015", "c.93L s.10", ""),
    ("P-016", "c.93L s.11 (Data Brokers)", "dedicated $100/day penalties"),
    ("P-017", "c.93L s.11 (Civil rights)(a)-(c)", ""),
    ("P-018", "c.93L s.11 (Civil rights)(d)", ""),
    ("P-019", "c.93L s.12(a)-(b)", ""), ("P-020", "c.93L s.12(c)-(d)", ""),
    ("P-021", "c.93L s.12(e)-(g)", ""), ("P-022", "c.93L s.13", ""),
    ("P-023", "c.93L ss.14(a)-(e),15(a)", "defendants: any non-small-business"),
    ("P-024", "c.93L s.14", "awards earmarked to individuals"),
    ("P-025", "c.93L s.14 (final)", ""), ("P-026", "c.93L s.16", ""),
    ("P-027", "c.93L s.15(b)", ""), ("P-028", "SECTION 2 (c.149 s.204)", ""),
]
for b in ("H83", "S25"):
    edges(b, *[(p, c, ("identical companion; " + n).rstrip("; ")) for p, c, n in _C93L])

_C93M_REDRAFT = [  # H4632/S2770 redraft
    ("P-001", "c.93M s.2", "variant: drops civic-engagement purpose and explicit targeted-ads secondary purpose"),
    ("P-002", "c.93M ss.1(a)(10),2(c),4(b),5(c),10(f)", "variant: codifies dark-pattern definition incl. FTC reference"),
    ("P-003", "c.93M s.3(a)(1)", ""),
    ("P-004", "c.93M ss.1(a)(29),3(a)(2)", "stricter: sensitive-data definition broadened (reproductive health, pregnancy, victim status)"),
    ("P-005", "c.93M s.3(a)(3)", "variant: defined consent replaces affirmative express consent"),
    ("P-006", "c.93M s.3(a)(4)", ""),
    ("P-007", "c.93M s.5", "stricter: point-of-collection display, no account conditioning"),
    ("P-008", "c.93M s.6(a)(4)", "variant: adds retention-evaluation duty"),
    ("P-009", "c.93M s.7", ""),
    ("P-010", "c.93M s.9(i)-(j)", "stricter: homepage placement plus separate biometric and geolocation policies"),
    ("P-271", "c.93M s.4", "weaker: 12-month lookback, 45-day response"),
    ("P-272", "c.93M s.4", ""), ("P-273", "c.93M s.4", "FCRA exception replaces school exception"),
    ("P-274", "c.93M s.4", ""),
    ("P-012", "c.93M s.10(a)-(c),(e)-(j)", "variant: forwarding liability shield, loyalty conflict procedure"),
    ("P-013", "c.93M ss.1(a)(26),10(d)", "added by redraft"),
    ("P-014", "c.93M s.15", "added by redraft"),
    ("P-015", "c.93M ss.1(a)(18),16", ""),
    ("P-016", "c.93M ss.17,14(a)(4)", "variant: dedicated penalties replaced by general enforcement; AG broker rulemaking"),
    ("P-017", "c.93M s.8", "stricter: protected classes expanded to c.151B universe"),
    ("P-022", "c.93M s.11", ""),
    ("P-023", "c.93M s.12(a)-(f),(j)", "weaker: defendant class narrowed to large data holders; adds 93A $5,000 floor"),
    ("P-024", "c.93M ss.12(g)-(h),14", "variant: adds operating-suspension remedy; drops earmarking"),
    ("P-025", "c.93M s.12(i)", ""),
    ("P-121", "c.93N ss.1,2(a)-(b),(d)", "variant of H357/S148 chapter: softened AG regs, altered retroactivity"),
    ("P-122", "c.93N s.2(c)", ""),
    ("P-281", "c.93N s.2(e)(1)", ""),
    ("P-282", "c.93N s.2(e)(2)", ""),
    ("P-283", "c.93N s.2(e)(4)", ""),
    ("P-284", "c.93N s.2(e)(3)", "retroactive application"),
    ("P-285", "c.93N s.2(e)(5)", "retroactive application"),
    ("P-125", "c.93N s.2(f)", "weaker: legal-mandate exception broadened to court orders/subpoenas/CIDs"),
    ("P-126", "c.93N s.2(i)", ""),
    ("P-127", "c.93N s.2(g)-(h)", ""),
    ("P-129", "c.93N s.3", ""),
    ("P-130", "c.93N s.4", "variant: $5,000/actual damages, 93A UDAP deeming"),
]
edges("H4632", *_C93M_REDRAFT)
edges("S2770", *[(p, c, ("identical companion of H4632; " + n).rstrip("; ")) for p, c, n in _C93M_REDRAFT])

_MIPSA = [
    ("P-031", "c.93M s.5", ""), ("P-032", "c.93M s.6", ""),
    ("P-033", "c.93M s.7", "10-year archive for large holders"),
    ("P-034", "c.93M ss.8,17(b)-(d),25(u)(3)", ""),
    ("P-035", "c.93M s.9", "consent-gate mechanism; 12-month re-request cooldown"),
    ("P-275", "c.93M s.10", ""), ("P-276", "c.93M s.10", ""),
    ("P-037", "c.93M s.11", ""),
    ("P-038", "c.93M s.12", ""), ("P-039", "c.93M s.13", ""),
    ("P-040", "c.93M ss.16,18", ""), ("P-041", "c.93M s.19", ""),
    ("P-042", "c.93M ss.20,25(p)(2)-(3),25(f)", ""),
    ("P-043", "c.93M s.21", "risk assessments; algorithmic detail for large holders"),
    ("P-044", "c.93M s.22", ""), ("P-045", "c.93M s.25", ""),
    ("P-046", "c.93M s.26", ""), ("P-047", "c.93M s.27", ""),
    ("P-048", "c.93M s.28", ""), ("P-049", "c.93M s.30; SECTION 2", ""),
]
for b in ("H60", "S227"):
    edges(b, *[(p, c, ("identical companion; " + n).rstrip("; ")) for p, c, n in _MIPSA])

edges("H1555",
    ("P-031", "c.93M s.3", "stricter: no size thresholds"),
    ("P-032", "c.93M s.4", "variant: adds public-task basis"),
    ("P-033", "c.93M ss.7-9", "variant: 1-month deadline"),
    ("P-035", "c.93M s.6", "stricter: prohibition-with-exceptions for special categories"),
    ("P-275", "c.93M s.10", "separate GDPR access article"),
    ("P-276", "c.93M s.15", "separate GDPR portability article"),
    ("P-037", "c.93M ss.12,14", "stricter: right to be forgotten with downstream notification"),
    ("P-038", "c.93M s.11", ""),
    ("P-041", "c.93M ss.20,22", ""),
    ("P-043", "c.93M ss.29-30", "stricter: adds mandatory AG prior consultation"),
    ("P-051", "c.93M s.5", ""), ("P-052", "c.93M s.13", ""),
    ("P-053", "c.93M s.16", ""), ("P-054", "c.93M s.17", ""),
    ("P-055", "c.93M ss.18-19,23-24", ""), ("P-056", "c.93M s.21", ""),
    ("P-057", "c.93M s.26", ""), ("P-058", "c.93M ss.27-28", ""),
    ("P-059", "c.93M ss.31-33", ""), ("P-060", "c.93M ss.34-37", ""),
    ("P-061", "c.93M ss.38-44", ""), ("P-062", "c.93M ss.45-52,56-57", ""),
    ("P-063", "c.93M ss.53-55", ""),
)

edges("S1896",
    ("P-065", "c.65D ss.1-2,6", ""),
    ("P-066", "c.65D s.5", ""),
)
edges("H1428", ("P-067", "c.41 s.98H (SECTION 1)", ""))
edges("S218", ("P-068", "c.93 s.115", ""))
edges("H3179",
    ("P-068", "c.93 s.115 para.1", "identical first paragraph to S218"),
    ("P-069", "c.93 s.115 para.2", "H3179-only addition"),
)
edges("H3831",
    ("P-070", "c.7D s.14(1)(a)-(b)", ""), ("P-071", "c.7D s.14(1)(c)", ""),
    ("P-072", "c.7D s.14(1)(d)", ""), ("P-073", "c.7D s.14(1)(e)", ""),
    ("P-074", "c.7D s.13(e)", ""), ("P-075", "c.7D s.14(1)(f)-(h)", ""),
    ("P-076", "c.7D s.14(3)", ""),
)

edges("H63",
    ("P-081", "c.93M s.2(a)-(c); bill SECTION 2", "stricter: handwritten consent for identification, 3-year expiry, retroactive re-consent"),
    ("P-082", "c.93M s.2(c)-(e)", "richer policy; 20-day change notice"),
    ("P-083", "c.93M s.2(g)", "adds 911 exception and per-disclosure handwritten consent"),
    ("P-084", "c.93M ss.1,2(h)", "stricter: any disclosure for consideration"),
    ("P-085", "c.93M s.2(f)", ""),
    ("P-086", "c.93M s.3", "H63 only"),
    ("P-087", "c.93M s.4", "H63 only"),
    ("P-088", "c.93M s.5", "revenue-scaled liquidated damages, anti-arbitration, presumption of harm"),
)
edges("S195",
    ("P-081", "c.93M s.2(b)", "weaker: written consent, electronic permitted, no expiry"),
    ("P-082", "c.93M s.2(a)", "harder retention backstop: destruction within 1 year of last interaction"),
    ("P-083", "c.93M s.2(d)", "adds subpoena and municipal-ordinance exceptions"),
    ("P-084", "c.93M s.2(c)", "sell/lease/trade/profit formulation"),
    ("P-085", "c.93M s.2(e)", ""),
    ("P-088", "c.93M s.3", "c.93A procedures; $5,000 or actual; double-treble willful"),
    ("P-089", "c.93M s.2(f)", "S195 only"),
)
edges("S140", ("P-091", "SECTIONS 1-3", "own biometric-indicator definition incl. genetic information; no photo exclusions"))
_93H_PKG = [
    ("P-091", "SECTIONS 1,4(i)(E)", ""),
    ("P-092", "SECTION 4(i)(F)", ""),
    ("P-093", "SECTIONS 3,4(i)(B),(C),(G)-(J),5", ""),
    ("P-094", "SECTIONS 4(ii),10", ""),
    ("P-095", "SECTION 2", ""),
    ("P-096", "SECTION 7", "broad harm categories"),
    ("P-097", "SECTIONS 8-10", "depends on P-093 subclause references"),
]
edges("H76", *[(p, c, ("identical companion of S30; " + n).rstrip("; ")) for p, c, n in _93H_PKG])
edges("S30", *[(p, c, ("identical companion of H76; " + n).rstrip("; ")) for p, c, n in _93H_PKG])
edges("S2539",
    ("P-091", "SECTIONS 5,8(i)(E)", "matches S30 wording"),
    ("P-092", "SECTION 8(i)(F)", ""),
    ("P-093", "SECTIONS 7,8(i)(B),(C),(G)-(J),9", ""),
    ("P-094", "SECTIONS 8(ii),15", ""),
    ("P-095", "SECTION 6", ""),
    ("P-096", "SECTION 11", ""),
    ("P-097", "SECTIONS 12,14,15", ""),
    ("P-098", "SECTION 13", "S2539 only"),
    ("P-101", "SECTION 17 (c.175 s.231)", "S2539 only; borderline in-domain"),
)
edges("S198", ("P-092", "sole section", "standalone minimal version; clause (d) collides with S140 drafting"))
edges("H281",
    ("P-091", "SECTION 1 cl.(d)", "weakest variant: financial-account-access biometrics only"),
    ("P-096", "SECTION 1 (breach definition)", "weaker: identity-theft/fraud risk only, embedded in definition"),
    ("P-097", "SECTION 3", "weak/legacy variant; permits security-freeze fees"),
    ("P-099", "SECTION 2", "H281 only"),
    ("P-100", "SECTION 1", "H281 only"),
)

_LOCATION = [
    ("P-121", "c.93L ss.1,2(a),(b),(d),6; SECTIONS 2-3", ""),
    ("P-122", "c.93L s.2(c)", ""),
    ("P-281", "c.93L s.2(e)(1)", ""),
    ("P-282", "c.93L s.2(e)(2)", ""),
    ("P-283", "c.93L s.2(e)(4)", ""),
    ("P-284", "c.93L s.2(e)(3)", ""),
    ("P-285", "c.93L s.2(e)(5)", ""),
    ("P-125", "c.93L s.2(f)", ""),
    ("P-126", "c.93L s.2(i)", ""),
    ("P-127", "c.93L s.2(g),(h)", ""),
    ("P-128", "c.93L s.3(a)-(c)", ""),
    ("P-129", "c.93L s.4", ""),
    ("P-130", "c.93L ss.5,7", ""),
]
for b in ("H357", "S148"):
    edges(b, *[(p, c, ("identical companion; " + n).rstrip("; ")) for p, c, n in _LOCATION])

_STORED = [
    ("P-131", "c.276 s.1B(a)-(e),(g),(k),(m); s.2A1/2(a); SECTION 3", ""),
    ("P-132", "c.276 s.1B(h)-(j)", ""),
    ("P-133", "c.276 s.1B(f)", ""),
    ("P-134", "c.276 s.1B(l)", ""),
    ("P-135", "c.276 s.1C", ""),
    ("P-136", "c.276 s.1D; s.2A1/2(b)", ""),
    ("P-137", "c.276 s.1E", ""),
    ("P-138", "SECTIONS 4-5 (c.78 s.7, s.7A)", ""),
]
for b in ("H1653", "S27"):
    edges(b, *[(p, c, ("identical companion; " + n).rstrip("; ")) for p, c, n in _STORED])
edges("H1519", ("P-139", "c.6A s.18M(b)-(e)", "single-proposition bill"))

_EDTECH = [
    ("P-141", "c.71 s.34J(a)(1)", ""), ("P-142", "c.71 s.34J(a)(2)", ""),
    ("P-143", "c.71 s.34J(a)(3)", ""), ("P-144", "c.71 s.34J(a)(4)", ""),
    ("P-145", "c.71 s.34J(b)(1)", ""), ("P-146", "c.71 s.34J(b)(2)", ""),
    ("P-147", "c.71 s.34K", ""), ("P-148", "c.71 s.34L(a)-(b)", ""),
    ("P-149", "c.71 s.34L(c)", ""), ("P-150", "c.71 s.34L(d)", ""),
    ("P-151", "c.71 s.34L(e)", ""), ("P-152", "c.71 s.34L(f)", ""),
]
for b in ("H532", "S280"):
    edges(b, *[(p, c, ("identical companion; " + n).rstrip("; ")) for p, c, n in _EDTECH])
edges("H1283", ("P-153", "new c.66 s.22", "broadest: no carve-out"))
edges("S844", ("P-153", "SECTION 1 (c.66 s.22)", "variant: adds municipal institutions and agency-requester carve-out"))
edges("H4266", ("P-153", "new c.66 s.22", "redraft: H1283 text plus agency carve-out only"))
_E2C = [
    ("P-154", "c.7E ss.1,2(a)-(d),3(a)-(b),(f),4", ""),
    ("P-155", "c.7E s.3(c)-(e)", ""),
    ("P-156", "c.7E s.2(e)", ""),
    ("P-157", "c.7E s.5", ""),
    ("P-158", "c.7E s.6", ""),
]
for b in ("H530", "S343"):
    edges(b, *[(p, c, ("identical companion; " + n).rstrip("; ")) for p, c, n in _E2C])
for b in ("H4421", "S2666"):
    edges(b, *[(p, c,
        "redraft; stricter: adds 20 C.F.R. Part 603 UI-confidentiality condition" if p == "P-156"
        else "redraft of H530/S343; identical") for p, c, n in _E2C])
edges("H1893",
    ("P-159", "SECTIONS 1,3 (c.15A s.45; c.75 s.48)", ""),
    ("P-160", "SECTION 2 (c.71 s.97)", ""),
    ("P-161", "SECTIONS 4-5 (c.149 ss.150,192)", ""),
)
edges("H80",
    ("P-162", "c.93 s.115(b),(c),(f),(g),(h)", ""),
    ("P-163", "c.93 s.115(d)", ""),
    ("P-164", "c.93 s.115(i),(k),(m)", ""),
)
edges("H1986", ("P-165", "sole resolve", "study commission; data-practice charges in clauses (ii)-(iii)"))

_FR = [
    ("P-171", "c.6 s.220(b),(l)", ""),
    ("P-172", "c.6 s.220(c)", ""),
    ("P-173", "c.6 s.220(d)", ""),
    ("P-174", "c.6 s.220(e)", ""),
    ("P-175", "c.6 s.220(f)", ""),
    ("P-176", "c.6 s.220(g),(h)", ""),
    ("P-177", "c.6 s.220(i),(j)", ""),
    ("P-178", "c.6 s.220(k)", ""),
]
for b in ("H1728", "S927"):
    edges(b, *[(p, c, ("identical companion; " + n).rstrip("; ")) for p, c, n in _FR])
edges("H4359",
    ("P-171", "c.6 s.220(b),(l)", "redraft; unchanged"),
    ("P-172", "c.6 s.220(c)", "redraft; broader: investigate and verify, state police may assist"),
    ("P-173", "c.6 s.220(d)", "redraft; adds RMV-assist purpose; documentation duty narrowed to FBI requests"),
    ("P-174", "c.6 s.220(e)", "redraft; unchanged"),
    ("P-175", "c.6 s.220(f)", "redraft; unchanged"),
    ("P-176", "c.6 s.220(g),(h)", "redraft; FBI searches counted by requesting agency"),
    ("P-177", "c.6 s.220(i),(j)", "redraft; unchanged"),
    ("P-178", "c.6 s.220(k)", "redraft; unchanged"),
)
edges("S1551", ("P-179", "c.90 s.8N", "single-proposition bill"))
edges("S1557",
    ("P-181", "c.6 s.221(c)", ""),
    ("P-182", "c.6 s.221(d)(1),(e)", ""),
    ("P-183", "c.6 s.221(d)(2)", ""),
    ("P-184", "c.6 s.221(d)(3)", ""),
    ("P-185", "c.6 s.221(f)", ""),
    ("P-186", "c.6 s.221(g),(h)", ""),
    ("P-187", "c.6 s.221(i)", ""),
)
edges("H3431",
    ("P-191", "c.90J s.2", ""), ("P-192", "c.90J s.3", ""),
    ("P-193", "c.90J s.4", ""), ("P-194", "c.90J s.5", ""),
    ("P-195", "c.90J s.6", ""), ("P-196", "c.90J s.7", ""),
    ("P-197", "c.90J ss.8,10(b)", ""), ("P-198", "c.90J s.9", ""),
    ("P-199", "c.90J s.10(a)", ""), ("P-200", "c.90J s.14", ""),
    ("P-201", "c.90J s.12", ""),
)

_TOLL_S209 = [
    ("P-205", "c.6C s.13(d)", ""),
    ("P-206", "c.6C s.13(e),(j)", "any-crime warrant; emergency statement to court"),
    ("P-207", "c.6C s.13(f)", ""),
    ("P-208", "c.6C s.13(h)", "exemplary damages only"),
    ("P-209", "c.6C s.13(i)", ""),
]
edges("S209", *[(p, c, ("identical to H1455; " + n).rstrip("; ")) for p, c, n in _TOLL_S209])
edges("H1455", *[(p, c, ("identical to S209; " + n).rstrip("; ")) for p, c, n in _TOLL_S209])
edges("H3434",
    ("P-210", "Sec.2", ""),
    ("P-206", "Sec.2(c)-(d)", "variant: felony-only; production order/preservation request; emergency notice to AG"),
    ("P-211", "Sec.3", ""),
    ("P-208", "Sec.4", "variant: treble or exemplary"),
)
edges("H3404",
    ("P-213", "c.90K Sec.2", ""),
    ("P-205", "c.90K Sec.3(a)", ""),
    ("P-210", "c.90K Sec.3(b)", ""),
    ("P-211", "c.90K Sec.3(c)", ""),
    ("P-206", "c.90K Sec.4", "variant: warrant or production order; extends to vehicle data"),
    ("P-214", "c.90K Secs.1,4", ""),
    ("P-207", "c.90K Sec.5", "variant: broader (ALPR/tolling/vehicle data; administrative proceedings)"),
    ("P-208", "c.90K Sec.6(a)-(b)", "variant: treble or exemplary"),
    ("P-212", "c.90K Sec.6(c)", ""),
)
edges("H1572", ("P-215", "c.265 s.43B", "criminal-harassment penalties by reference; child-as-operator parent exception"))
edges("H1809", ("P-215", "c.272 s.108", "variant: standalone penalty; child-as-occupant exception with restraining-order disqualifier; dealer and fleet carve-outs"))

edges("H1049", ("P-223", "c.183 s.70 (SECTION 1)", ""))
edges("H326",
    ("P-224", "c.93 s.116(f)", ""),
    ("P-225", "c.93 s.117", ""),
)
for b in ("H1707", "S971"):
    edges(b, ("P-226", "SECTIONS 1-2 (c.214 s.3C)", "identical companion"))
edges("H395",
    ("P-231", "Sec.3(A)", ""), ("P-232", "Sec.3(B)", ""),
    ("P-233", "Sec.4(A)", ""), ("P-234", "Sec.4(B)", ""),
    ("P-235", "Secs.4(C),5(B)", ""), ("P-236", "Sec.5(A)", ""),
    ("P-237", "Sec.6", ""), ("P-238", "Sec.7", ""),
    ("P-239", "Sec.8", ""),
)

_CHD = [
    ("P-241", "c.93M s.2", ""), ("P-242", "c.93M s.3(1)-(3)", "consent withdrawal right (s.4) attaches to this consent mechanism"),
    ("P-243", "c.93M s.3(4)", ""),
    ("P-277", "c.93M s.4", ""), ("P-278", "c.93M s.4", ""),
    ("P-245", "c.93M s.5", ""), ("P-246", "c.93M s.6", ""),
]
for b in ("H386", "S184"):
    edges(b, *[(p, c, ("identical companion; " + n).rstrip("; ")) for p, c, n in _CHD])
edges("H377", ("P-247", "c.93A1/2 ss.3-4", "notice-only for incompatible-purpose processing"))
edges("S174", ("P-247", "c.93A1/2 ss.3-4", "stricter: consent plus notice for incompatible-purpose processing"))

for b, note in (("H1442", "identical to S1022"), ("S1022", "identical to H1442")):
    edges(b,
        ("P-251", "c.6A s.18M", note + "; private-data framing, consent-or-court-order rule"),
        ("P-252", "c.6A s.18M para.1", note),
    )
edges("H4323",
    ("P-251", "c.6A s.18G(b)", "redraft: public-records-exemption mechanism, broader access list, $1,000 fine"),
    ("P-252", "c.6A s.18G(c)", "weaker public access: PII redactable"),
    ("P-253", "c.6A s.18G(a)", "H4323 only"),
)
edges("S194", ("P-254", "c.10 s.24 (sole section)", ""))
edges("S938", ("P-255", "c.258C s.15 (sole section)", ""))
edges("H3863",
    ("P-256", "SECTION 1 para.1", ""),
    ("P-257", "SECTION 1 para.1", ""),
    ("P-258", "SECTION 1 para.2", ""),
    ("P-259", "SECTION 1 para.3", ""),
)
edges("S1368",
    ("P-260", "SECTION 1 (c.111 s.70E)", ""),
    ("P-261", "SECTION 2", ""),
)
# H4844 (official text: data/h4844_text.txt, extracted from the cached
# malegislature.gov PDF): a care-location-scoped version of the location
# shield. Weaker-scope variants of the same mechanisms per the codebook rule;
# section 4's rulemaking directives are recorded as rulemaking variants of
# the corresponding operative duties.
_H4844_NOTE = "narrowed to reproductive/gender-affirming-care location information; enforcement is 93A/AG only (no private right of action)"
edges("H4844",
    ("P-121", "c.93M ss.1,2(a); s.4(iii) consent rulemaking; bill SECTIONS 2-3", _H4844_NOTE),
    ("P-281", "c.93M s.2(b)(i)", _H4844_NOTE),
    ("P-282", "c.93M s.2(b)(ii); s.4(iv) destruction rulemaking", _H4844_NOTE),
    ("P-283", "c.93M s.2(b)(iv)", _H4844_NOTE),
    ("P-284", "c.93M s.2(b)(iii)", _H4844_NOTE + "; adds 'gift' to the sale ban"),
    ("P-285", "c.93M s.2(b)(v)", _H4844_NOTE),
    ("P-125", "c.93M s.2(c)", _H4844_NOTE),
    ("P-127", "c.93M s.2(a)(i); s.4(i) policy-content rulemaking", _H4844_NOTE),
    ("P-122", "c.93M s.4(ii)", _H4844_NOTE + "; rulemaking variant (AG to set targeted-ad limits)"),
    ("P-129", "c.93M s.4(v)", _H4844_NOTE + "; rulemaking variant (AG to prohibit adverse actions)"),
    ("P-286", "c.93M s.4(vi)", "H4844 only"),
)

# NDII lineage: standalone filings, Judiciary redraft, engrossed and
# conference vehicles. H4241/H4744 have no API text; the enacted text is
# 2024 c.118 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter118).
for b in ("H1745", "S1012", "S1139"):
    edges(b,
        ("P-266", "SECTION 5 (c.265 s.43A(b) rewrite)", "as-filed version; no digitization (deepfake) coverage"),
        ("P-280", "SECTION 5 (c.265 s.43A(b)(5))", ""))
edges("H4115",
    ("P-266", "SECTION 6 (c.265 s.43A(b) rewrite)", "Judiciary redraft; no digitization coverage"),
    ("P-280", "SECTION 6 (c.265 s.43A(b)(5))", ""))
edges("H4241",
    ("P-266", "engrossed text of H4115 SECTION 6 lineage (API text empty; see c.118 s.6)", "House-engrossed vehicle"),
    ("P-280", "engrossed text (see c.118 s.6, s.43A(b)(5))", ""))
edges("H4744",
    ("P-266", "2024 c.118 s.6 (c.265 s.43A(b))", "ENACTED; conference text adds 'digitization'; (c) repeat-offender penalty attaches"),
    ("P-280", "2024 c.118 s.6 (c.265 s.43A(b)(5))", "ENACTED"))
edges("S2539",
    ("P-287", "SECTION 1 (c.7D s.17(f)(iv))", "delegated rulemaking; boundary call in codebook"),
    ("P-288", "SECTION 1 (c.7D s.17(f)(iv))", "delegated rulemaking; boundary call in codebook"),
    ("P-289", "SECTION 1 (c.7D s.17(f)(iv))", "deletion/de-identification when data no longer needed"))

# HOMES eviction-record sealing lineage (enacted at 2024 c.150 ss.28,52:
# https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter150)
for b in ("H1690", "S956"):
    edges(b,
        ("P-295", "new c.239 s.16(a)-(h),(j)-(k)", "identical companion"),
        ("P-296", "new c.239 s.16(i); c.93 s.52 amendment", "identical companion"))
edges("H4356",
    ("P-295", "new c.239 s.16(a)-(h),(j)-(k)", "Judiciary redraft of H1690/S956"),
    ("P-296", "new c.239 s.16(i); c.93 s.52 amendment", "Judiciary redraft of H1690/S956"))
for b in ("H1525", "S943"):
    edges(b, ("P-291", "new c.222 s.29 (within the notary-modernization act)", "identical companion"))
edges("H3003",
    ("P-297", "sole section (demographic collection categories)", "enacted as 2023 c.28 s.7"),
    ("P-298", "sole section (PII confidentiality, aggregate publication)", "enacted as 2023 c.28 s.7"))
edges("H2991", ("P-294", "sole section (SFI home-address restriction)", "weaker than enacted 2024 c.248 s.27, which adds email/phone/family"))

# Enacted origin vehicles (chapter OriginBill records). Each carries the
# in-domain propositions its enacted chapter contains; provisions may have
# entered the vehicle by amendment or conference, so the cite is to the
# enacted chapter section (third-pass review finding 2).
edges("H58", ("P-291", "2023 c.2 s.33 (new c.222 s.29)", "enacted vehicle (FY23 supplemental budget)"))
edges("H4040",
    ("P-297", "2023 c.28 s.7 (new c.6A s.109)", "enacted vehicle (FY24 GAA)"),
    ("P-298", "2023 c.28 s.7 (new c.6A s.109)", "enacted vehicle (FY24 GAA)"))
edges("H4977",
    ("P-295", "2024 c.150 s.52 (new c.239 s.16)", "enacted vehicle (Affordable Homes Act)"),
    ("P-296", "2024 c.150 ss.28,52 (c.93 s.52(a)(7); c.239 s.16(i))", "enacted vehicle (Affordable Homes Act)"))
edges("H5077", ("P-294", "2024 c.248 s.27 (c.268B s.3)", "enacted vehicle (December 2024 supplemental)"))
edges("H4799",
    ("P-303", "2024 c.206 s.15 (c.159A1/2 s.12(a)-(c))", "enacted vehicle (FY24 closeout supplemental); outside section, no filed antecedent"),
    ("P-304", "2024 c.206 s.15 (c.159A1/2 s.12(d)-(e))", "enacted vehicle (FY24 closeout supplemental); outside section, no filed antecedent"))
edges("S2884",
    ("P-299", "SECTION 1 (c.4 s.7 cl.26(w)); c.90K s.5(b)", "enacted as 2024 c.363"),
    ("P-300", "c.90K s.5(a)", "enacted as 2024 c.363"),
    ("P-301", "c.90K s.5(c)", "enacted as 2024 c.363"),
    ("P-302", "c.90K s.5(d)", "enacted as 2024 c.363"))

EDGES = E

OUT_OF_DOMAIN = {
    "S1896": "Municipal Broadband Fund (c.65D s.4; c.29 s.2RRRRR): broadband finance",
    "H326": "Trial-offer/negative-option disclosure and consent regime (c.93 s.116(a)-(e),(g)): consumer protection without a data-handling rule",
    "H3831": "Municipal broadband build-out, net neutrality, anti-censorship, governance (c.7D ss.12, 13(a)-(d),(f), 14(1)(i)-(k), 14(2))",
    "S2539": "State cybersecurity code, incident response, AI/ADM board, robotics, funds (SECTIONS 1-4, 16, 18-22); SECTION 1 c.7D s.17(f)(iv) AI training-data consent rulemaking flagged borderline",
    "S1557": "Drone weaponization ban, acquisition approval, critical-infrastructure airspace, hunting ban (c.6 s.221(b); SECTION 2)",
    "H377": "Deceptive pregnancy-services advertising ban (c.93A1/2 s.2): advertising regulation without a data-handling rule",
    "S174": "Deceptive pregnancy-services advertising ban (c.93A1/2 s.2): same as H377",
    "H1745": "Minor-sexting diversion program (SECTION 3, c.119 s.39N) and criminal-harassment penalty changes (SECTION 4): juvenile-diversion and penalty mechanisms, not disclosure restrictions",
    "S1012": "Same out-of-domain content as H1745 (diversion program, penalties)",
    "S1139": "Same out-of-domain content as H1745 (diversion program, penalties)",
    "H4115": "Diversion program, penalty changes, and coercive-control provisions (abuse-prevention-order law)",
    "H4241": "Same as H4115 (engrossed vehicle)",
    "H4744": "2024 c.118 out-of-domain content: coercive-control definitions (abuse-order law, incl. threatening to publish sensitive personal information as an abuse element), minor-sexting diversion (c.119 s.39N), penalty increases, related procedural sections",
}

# Verbatim quotes (from the cached official texts, as recorded in the
# memo/atomization/ notes and data/h4844_text.txt) grounding the cross-bill
# identity claims that rest on analytic judgment, plus the comparator
# carriers' quotes, so the verification queue can show them side by side.
# (bill, prop_id) -> quote
QUOTES = {
    ("H1555", "P-031"): "adequate, relevant and limited to what is necessary in relation to the purposes",
    ("H60", "P-031"): "adequate, relevant and limited to what is reasonably necessary in relation to the purposes",
    ("H1555", "P-032"): "Processing shall be legal only if and to the extent that at least 1 of the following applies",
    ("H60", "P-032"): "Processing shall be lawful and in compliance with this chapter only if",
    ("H1555", "P-033"): "the controller shall, at the time when personal data is obtained, provide the data subject with all of the following",
    ("H60", "P-033"): "a reasonably accessible, clear and meaningful privacy notice",
    ("H1555", "P-035"): "Processing of personal data revealing racial or ethnic origin, political opinions, religious or philosophical beliefs",
    ("H60", "P-035"): "shall not otherwise process an individual's sensitive information without first obtaining the consent",
    ("H1555", "P-037"): "the erasure of personal data concerning the data subject without undue delay",
    ("H60", "P-037"): "the right to request that a controller delete any personal information processed",
    ("H1555", "P-038"): "the rectification of inaccurate personal data concerning the data subject",
    ("H60", "P-038"): "correct inaccurate personal information processed about the individual",
    ("H1555", "P-041"): "Processing by a processor shall be governed by a contract or other legal act",
    ("H60", "P-041"): "A contract between a controller and a processor shall govern the processor's procedures",
    ("H1555", "P-043"): "an assessment of the impact of the envisaged processing operations on the protection of personal data",
    ("H60", "P-043"): "carry out and document a risk assessment of the impact",
    ("H1555", "P-275"): "confirmation as to whether or not personal data concerning the data subject is being processed",
    ("H60", "P-275"): "the specific pieces of personal information that the controller has processed about the individual",
    ("H1555", "P-276"): "in a structured, commonly used and machine-readable format",
    ("H60", "P-276"): "the specific pieces of personal information ... in a portable ... format",
    ("H1572", "P-215"): "installs, conceals, or otherwise places for use an electronic mobile tracking device in or on a motor vehicle without the consent",
    ("H1809", "P-215"): "knowingly installs, conceals or otherwise places or uses an electronic tracking device in or on a motor vehicle without the consent",
    ("H281", "P-091"): "biometric indicator of the consumer used to gain access to financial accounts of the consumer",
    ("H76", "P-091"): "data generated from the specific technical processing of an individual's unique biological or physiological patterns or characteristics",
    ("H281", "P-096"): "that creates an identifiable risk of identity theft or fraud",
    ("H76", "P-096"): "presents a reasonably foreseeable risk of financial, physical, reputational or other cognizable harm to the resident",
    ("H281", "P-097"): "and any fees required to be paid to any of the consumer reporting agencies",
    ("H76", "P-097"): "the date, estimated date, or estimated date range of the breach of security",
    ("S140", "P-091"): "any unique biological attribute or measurement that can be used to authenticate the identity of an individual",
    ("H3404", "P-205"): "toll collection technologies shall only be used to identify the location of any vehicle for tolling purposes",
    ("S209", "P-205"): "shall not be used to identify the location of any vehicle for purposes other than charging and collecting",
    ("H3404", "P-206"): "shall be shared with or provided to any law enforcement entity ... without a search warrant, or production order",
    ("S209", "P-206"): "shall be shared with or provided to any law enforcement entity ... without a valid warrant",
    ("H3404", "P-207"): "shall not be admitted, offered or cited by any governmental entity for any purpose",
    ("S209", "P-207"): "shall be inadmissible in any criminal or civil proceeding",
    ("H3404", "P-208"): "liable for treble damages, or, in the alternative, exemplary damages",
    ("S209", "P-208"): "liable for exemplary damages of not less than $100 and not more than $1,000 for each violation",
    ("H3404", "P-210"): "shall not access, search, review, disclose, or exchange tolling data",
    ("H3434", "P-210"): "shall not access, search, review, disclose, or exchange tolling data in its possession",
    ("H3404", "P-211"): "permanently erase or destroy all tolling data ... not later than 120 days",
    ("H3434", "P-211"): "permanently erase or destroy ... not later than 120 days following the date on which the tolling data was created",
    ("H3434", "P-206"): "comply with a search warrant, production order, or preservation request ... prosecution of a felony",
    ("H3434", "P-208"): "liable for treble damages, or, in the alternative, exemplary damages",
    ("H4844", "P-121"): "shall collect or process an individual's reproductive or gender-affirming care location information if: (i) ... location privacy policy; (ii) obtains consent",
    ("H357", "P-121"): "unlawful for a covered entity to collect or process an individual's location information except for a permissible purpose",
    ("H4844", "P-122"): "any limitations or restrictions on the use of targeted advertisements by a covered entity or service provider",
    ("H357", "P-122"): "a clear, conspicuous, and simple means to opt out of the processing of their location information",
    ("H4844", "P-125"): "the agency or official serves the covered entity or service provider with a valid warrant",
    ("H357", "P-125"): "serves the covered entity or service provider with a valid warrant or establishes the existence of exigent circumstances",
    ("H4844", "P-127"): "determining minimum requirements for inclusion in a location privacy policy",
    ("H357", "P-127"): "shall maintain and make available to the data subject a Location Privacy Policy",
    ("H4844", "P-129"): "prohibitions on adverse actions by a covered entity or service provider against an individual because the individual exercised",
    ("H357", "P-129"): "shall not take adverse action against an individual because the individual exercised or refused to waive",
    ("H4844", "P-281"): "collect more precise reproductive or gender-affirming care location information than",
    ("H357", "P-281"): "collect more precise location information than necessary to carry out the permissible purpose",
    ("H4844", "P-282"): "retain reproductive or gender-affirming care location information longer than necessary",
    ("H357", "P-282"): "retain location information longer than necessary to carry out the permissible purpose",
    ("H4844", "P-283"): "derive or infer from reproductive or gender-affirming care location information any",
    ("H357", "P-283"): "derive or infer ... beyond ... the permissible purpose",
    ("H4844", "P-284"): "sell, rent, trade, gift or lease reproductive or gender-affirming care location information",
    ("H357", "P-284"): "sell, rent, trade, or lease location information to third parties",
    ("H4844", "P-285"): "disclose, cause to disclose or assist with or facilitate the disclosure of an individual's",
    ("H357", "P-285"): "disclose ... to a third party unless ... necessary ... or requested by the individual",
    ("H63", "P-081"): "shall not collect or process an individual's biometric information for identification purposes unless it first",
    ("S195", "P-081"): "receives written consent executed by the subject of the biometric identifier or biometric information",
    ("H63", "P-082"): "shall always maintain and make available to the individual a Biometric Privacy Policy",
    ("S195", "P-082"): "establishing a retention schedule and guidelines for permanently destroying biometric identifiers and biometric information",
    ("H63", "P-083"): "shall not disclose, cause to disclose, or otherwise disseminate or cause to disseminate an individual's biometric information",
    ("S195", "P-083"): "disclose, redisclose, or otherwise disseminate a person's or a customer's biometric identifier or biometric information unless",
    ("H63", "P-084"): "It is unlawful for a covered entity, data processor, or third party to monetize an individual's biometric information.",
    ("S195", "P-084"): "sell, lease, trade, or otherwise profit from a person's or a customer's biometric identifier",
    ("H63", "P-085"): "store, transmit, and protect from disclosure all biometric data using the reasonable standard of care",
    ("S195", "P-085"): "in a manner that is the same as or more protective than the manner in which the private entity stores",
    ("H63", "P-088"): "liquidated damages of not less than 0.5% of the annual global revenue of the covered entity or $5,000",
    ("S195", "P-088"): "Damages pursuant to any said action shall be no less than $5,000 per violation or actual damages suffered",
    ("S218", "P-068"): "without express written approval from the customer",
    ("H3179", "P-068"): "without express written approval from the customer",
}
QUOTES.update({
    ("H1690", "P-290"): "may petition the court to seal the court record",
    ("H4356", "P-290"): "may petition the court to seal the court record",
})
QUOTES.update({
    ("H1525", "P-291"): "shall not use, sell, or offer to sell to another person, or transfer to another person for use or sale, any personal inf[ormation]",
})
QUOTES.update({
    ("H3003", "P-292"): "except for personal identifying information, which shall be deemed confidential, each government agency shall make the data available",
    ("H2991", "P-294"): "statements of financial interest filed pursuant to section 5, which contain the home address of the filer",
})
QUOTES.update({
    ("H1690", "P-295"): "may petition the court to seal the court record",
    ("H4356", "P-295"): "may petition the court to seal the court record",
    ("H1690", "P-296"): "a consumer reporting agency shall not disclose the existence of, or information regarding, an eviction record sealed under this section",
    ("H4356", "P-296"): "a consumer reporting agency shall not disclose the existence of, or information regarding, an eviction record sealed under this section",
    ("H4977", "P-295"): "may petition the court to seal the court record (2024 c.150 s.52)",
    ("H4977", "P-296"): "a consumer reporting agency shall not disclose the existence of, or information regarding, an eviction record sealed (2024 c.150 s.52)",
    ("H3003", "P-297"): "every government agency that collects demographic data as to the race or ethnicity of residents ... shall use separate collection categories",
    ("H3003", "P-298"): "except for personal identifying information, which shall be deemed confidential, each government agency shall make the data available",
    ("H4040", "P-297"): "shall use separate collection categories and tabulations (2023 c.28 s.7)",
    ("H4040", "P-298"): "except for personal identifying information, which shall be deemed confidential (2023 c.28 s.7)",
    ("H58", "P-291"): "shall not use, sell or offer to sell to another person or transfer to another person for use or sale any personal information (2023 c.2 s.33)",
    ("H5077", "P-294"): "home address, personal email address and personal and home telephone number of the filer and the name and home address of a family member (2024 c.248 s.27)",
})

# ---------------------------------------------------------------------------
# Full-corpus-screen admissions (third-pass review finding 3): 31 bills
# found by full-text screening all 8,183 numbered filings. Mechanism notes
# and cites from the five triage reading passes
# (scripts/corpus_triage_verdicts.csv).
PROPS.update({
    "P-305": ("judicial-pii-agency-posting-ban", "govt-records", "State/county/municipal agencies barred from posting protected judicial officers' personal information online without written consent, with confidential-marking and 72-hour removal"),
    "P-306": ("judicial-pii-databroker-sale-ban", "data-brokers", "Data brokers barred from selling, licensing, or trading judges' personal information"),
    "P-307": ("judicial-pii-takedown-right", "interpersonal", "Post-request duty on any person or business to remove and not transfer judges' personal information (72-hour takedown), with private action"),
    "P-308": ("election-worker-pii-posting-ban", "interpersonal", "Unlawful to knowingly post election workers' or family members' personal information online where dissemination promotes harassment or threatens safety"),
    "P-310": ("worker-data-collection-notice", "workplace", "Employer notice of worker-data collection including vendor/third-party disclosure notice"),
    "P-311": ("worker-data-access-right", "workplace", "Worker right to access worker data in portable format on verifiable request"),
    "P-312": ("worker-data-correction-right", "workplace", "Accuracy duty and worker correction right with downstream third-party correction"),
    "P-313": ("worker-data-minimization", "workplace", "Worker-data collection limited to strictly necessary purposes"),
    "P-314": ("worker-data-sale-ban", "workplace", "Ban on sale or license of worker data, including de-identified worker data"),
    "P-315": ("worker-data-disclosure-limits", "workplace", "Worker-data disclosure only by contract with security duties; biometric/health third-party transfer ban; government-sharing limits"),
    "P-316": ("worker-biometric-health-destruction", "workplace", "Mandatory destruction of worker biometric and health data"),
    "P-317": ("worker-data-employment-use-bans", "workplace", "Bans on using worker data for enumerated employment decisions"),
    # P-318/P-319 retired 2026-08-05 (fourth-pass review finding 5): split.
    "P-350": ("worker-data-security-safeguards", "workplace", "Employer duty to maintain security safeguards for worker data"),
    "P-351": ("worker-data-breach-notice", "workplace", "Breach notification to affected workers and the department"),
    "P-352": ("worker-vendor-compliance-liability", "workplace", "Vendor compliance duties and joint employer-vendor liability for worker data and ADS"),
    "P-353": ("worker-vendor-return-delete", "workplace", "Vendor duty to return and delete worker data at contract termination"),
    "P-361": ("worker-vendor-information-supply", "workplace", "Vendor duty to supply the employer all information necessary for chapter compliance"),
    "P-320": ("workplace-monitoring-notice", "workplace", "Notice regimes for workplace electronic monitoring (advance, change, and inventory notices)"),
    "P-321": ("workplace-monitoring-limits", "workplace", "Allowable-purpose, strictly-necessary, least-invasive limits on electronic monitoring with prohibited practices (off-duty, private areas, facial/gait/emotion recognition)"),
    "P-322": ("workplace-monitoring-data-use-limits", "workplace", "Limits on using monitoring data for employment decisions; no sole reliance"),
    "P-323": ("workplace-monitoring-data-access", "workplace", "Employee right to review and copy electronic monitoring data about them"),
    "P-324": ("workplace-ads-notice-inventory", "workplace", "Notice and annual inventory duties for automated decision systems affecting workers"),
    "P-325": ("workplace-ads-use-prohibitions", "workplace", "Prohibited ADS uses (profiling rights-exercise, facial/gait/emotion recognition, customer-rating reliance) and human-oversight requirements"),
    "P-326": ("workplace-algorithmic-impact-assessments", "workplace", "Algorithmic impact assessments for workplace ADS with worker dispute rights"),
    "P-328": ("monitoring-data-disclosure-limits", "workplace", "Disclosure restrictions on collected monitoring data with consent/warrant exceptions"),
    "P-332": ("camera-capture-limit-destruction", "surveillance-tech", "Camera systems may capture images only upon violation; destruction within 48 hours of final disposition (variant: 30-day/1-year schedules)"),
    "P-333": ("buscam-vendor-rmv-access-security", "surveillance-tech", "Camera vendor access to RMV owner data limited to enforcement purpose with security protocol, background checks, encryption, and annual independent audit"),
    "P-335": ("ltc-sogi-nondisclosure", "health", "Long-term care facilities barred from disclosing residents' sexual orientation, gender identity/transition, intersex, or HIV status, with a duty to minimize inadvertent disclosure"),
    "P-336": ("rmv-federal-access-warrant-gate", "govt-records", "RMV files and data closed to federal civil immigration enforcement absent a judge-signed probable-cause warrant, with AG quash authority"),
    "P-337": ("cori-noncriminal-access-ban", "govt-records", "CORI may not be accessed or disclosed for non-criminal-justice purposes including civil enforcement"),
    "P-338": ("court-personnel-disclosure-limits", "govt-records", "Court personnel may share case information with federal agents only as publicly available; orders limiting disclosure of immigration-status information"),
    "P-340": ("dealer-customer-data-restrictions", "commercial", "Manufacturers may require dealer customer information only for enumerated purposes and may not share, sell, or transfer it to third parties without dealer consent"),
    "P-341": ("dealer-data-breach-indemnification", "commercial", "Mandatory manufacturer/third-party indemnification of dealers for data security breaches and unlawful use of customer data"),
    "P-342": ("pi-rmv-data-access-grant", "govt-records", "Licensed private investigators added to authorized users of RMV computer data, with misuse prohibitions and license revocation"),
    "P-343": ("pi-facial-recognition-access-ban", "surveillance-tech", "Private investigators barred from accessing the RMV facial recognition system, on pain of license revocation"),
    "P-344": ("fusion-collection-dissemination-limits", "surveillance-tech", "Ban on collecting or disseminating protected information absent criminal nexus, with accuracy vetting, dissemination logs, five-year file review and destruction; private right of action attaches"),
    # P-345 retired 2026-08-05: split into P-354/P-355/P-356.
    "P-354": ("fusion-internal-data-audits", "surveillance-tech", "Annual internal audits of each fusion-center database (users, access levels, data quantities, sources)"),
    "P-355": ("fusion-ig-oversight", "surveillance-tech", "Inspector General access to criminal intelligence systems with biennial compliance reports"),
    "P-356": ("fusion-sar-audit-purge", "surveillance-tech", "Independent audit of suspicious-activity reports with purge of noncompliant records"),
    "P-346": ("fusion-subject-access", "surveillance-tech", "Subject right of access to personal data held in criminal intelligence systems"),
    # P-347 retired 2026-08-05: split into P-357/P-358/P-359.
    "P-357": ("client-data-bank-system", "govt-data", "State-run centralized client data bank with standardized application, client ID-card issuance, and provider-acceptance duties"),
    "P-362": ("client-data-bank-membership-conditions", "govt-data", "Nonprofit providers' state grant/loan eligibility conditioned on data-bank participation, with an application fee set by the secretary"),
    "P-358": ("client-data-bank-consent-gate", "govt-data", "Written informed client consent required before the data bank discloses client personal data, with c.66A protection duties"),
    "P-359": ("client-data-bank-records-exclusion", "govt-data", "Data-bank client information excluded from the public-records definition"),
})

edges("H1566",
    ("P-305", "new c.221D s.2", "companion of S1133"),
    ("P-306", "new c.221D s.3(a)", "companion of S1133"),
    ("P-307", "new c.221D s.3(b)-(f)", "companion of S1133; private action attaches"))
edges("S1133",
    ("P-305", "SECTION 2 (c.221D s.2)", "companion of H1566"),
    ("P-306", "SECTION 3(a)", "companion of H1566"),
    ("P-307", "SECTION 3(b)-(f)", "companion of H1566"))
edges("S1013", ("P-308", "new c.56 s.48A(c)", "penalties attach"))
edges("S1116", ("P-226", "SECTION 2 (new c.214 s.3C); SECTION 1 (c.12 s.11H)", "stricter variant: adds AG civil-rights enforcement and treble bias damages"))
edges("H1873",
    ("P-310", "c.149B s.2", ""), ("P-311", "c.149B s.2A", ""),
    ("P-312", "c.149B s.2B", ""), ("P-313", "c.149B s.2C(a)-(d)", ""),
    ("P-314", "c.149B s.2C(e)", "includes de-identified worker data"),
    ("P-315", "c.149B s.2C(f)-(h)", ""), ("P-316", "c.149B s.2C(i)", ""),
    ("P-317", "c.149B s.2C(j)-(k)", ""),
    ("P-350", "c.149B s.2D(a)", ""), ("P-351", "c.149B s.2D(b)", ""),
    ("P-352", "c.149B ss.2E(a),4E(a)", ""), ("P-361", "c.149B ss.2E(b),4E(b)", ""),
    ("P-353", "c.149B ss.2E(c),4E(c)", ""),
    ("P-320", "c.149B ss.3-3B", ""),
    ("P-321", "c.149B s.3C", ""), ("P-322", "c.149B s.3D", ""),
    ("P-324", "c.149B ss.4-4B", ""), ("P-325", "c.149B ss.4C-4D", ""),
    ("P-326", "c.149B s.5, s.5C", ""))
edges("S1228",
    ("P-321", "SECTIONS 2, 7, 12", "monitoring-only act; collection/private-area/First Amendment limits"),
    ("P-320", "SECTIONS 3-6", "general/specific/simultaneous notice regimes"),
    ("P-323", "SECTION 8", ""),
    ("P-322", "SECTION 9", "no adverse action without compliance; no sole-basis quotas"),
    ("P-328", "SECTIONS 10, 12(d)-(e)", "enforcement (SECTION 13) and non-waiver attach"))
edges("H3597",
    ("P-322", "new c.149 s.105E(i)", "practical-necessity and least-invasive test within just-cause bill"),
    ("P-320", "c.149 s.105E(i) notice provisions", ""),
    ("P-323", "c.149 s.105E(j)", "work-speed data copy every 7 days; correction rights"))
_CAM90J = [
    ("P-299", "c.4 s.7 cl.26(w); c.90J s.8(c)", ""),
    ("P-300", "c.90J s.8(b)", ""),
    ("P-301", "c.90J s.8(d)", ""),
    ("P-302", "c.90J s.8(e)", ""),
    ("P-332", "c.90J s.8(a)", ""),
]
for b in ("H3393", "S1483", "S2275"):
    edges(b, *[(pp, cc, "road-safety/bus-camera c.90J regime") for pp, cc, nn in _CAM90J])
edges("H3375", *[(pp, cc, "school-bus camera authorization, same regime") for pp, cc, nn in _CAM90J])
for b, note in (("H4166", "Cambridge home-rule petition, same regime"), ("H4287", "Salem home-rule petition, same regime")):
    edges(b,
        ("P-299", "s.8(c)", note), ("P-300", "s.8(b)", note),
        ("P-302", "s.8(e)", note), ("P-332", "s.8(a)", note))
edges("H3336",
    ("P-333", "new c.90 s.14C(c)(1)", ""),
    ("P-332", "c.90 s.14C(c)(2)", "variant: 30-day non-violation/1-year violation destruction with attestation"),
    ("P-302", "c.90 s.14C(c)(2)", "variant: recordings municipal property; vendor use ban"))
edges("S2600",
    ("P-299", "SECTION 6 (c.4 s.7 cl.26(w)); SECTION 8 (c.90K s.5(b))", "parent vehicle of S2884 (Reported on a part of)"),
    ("P-300", "c.90K s.5(a)", ""),
    ("P-301", "c.90K s.5(c)", ""),
    ("P-302", "c.90K s.5(d)", ""))
for b in ("H637", "S381"):
    edges(b, ("P-335", "new c.111 s.72CC(f)", "companions; DPH penalties attach"))
edges("S2604", ("P-335", "new c.111 s.72CC(f)", "Senate redraft; clause dropped from enacted 2024 c.197 s.17 (see adjudication)"))
for b in ("H1438", "S941"):
    edges(b,
        ("P-336", "SECTION 1 (c.6 s.167A(j))", "companions; AG quash authority attaches"),
        ("P-337", "SECTIONS 2-3 (c.6 s.172)", "companions"),
        ("P-338", "SECTIONS 5-6 (c.147 s.63; c.258B s.3(x))", "companions; interview-subject PII carve-out attaches"))
for b in ("H331", "S151"):
    edges(b,
        ("P-340", "c.93B s.4(c)(14)", "companions"),
        ("P-341", "c.93B s.4(c)(14) indemnification clause", "companions"))
for b in ("H3289", "S2250"):
    edges(b,
        ("P-342", "SECTIONS 1-2 (c.90 s.30A; c.147 s.30 para 12)", "companions"),
        ("P-343", "c.147 s.30 para 13", "companions; license revocation attaches"))
edges("H3637",
    ("P-344", "new c.66A s.2C", "private right of action (s.2C(b)(6)) attaches"),
    ("P-354", "new c.66A s.2A", ""),
    ("P-355", "new c.66A s.2B", "s.2E transparency attaches"),
    ("P-356", "new c.66A s.2D", ""),
    ("P-346", "new c.66A s.2F", ""))
edges("H219",
    ("P-357", "new c.6A s.16DD(d)", "system, standardized application, ID card"),
    ("P-362", "new c.6A s.16DD(b)-(c)", "application fee (b); provider eligibility conditioning (c)"),
    ("P-358", "new c.6A s.16DD(e)", ""),
    ("P-359", "new c.6A s.16DD(a)", ""))
edges("S23", ("P-291", "SECTION 30 (new c.222 s.29)", "Senate supplemental-budget vehicle carrying the notary restriction"))
edges("S2703",
    ("P-266", "SECTION 6 (c.265 s.43A(b))", "Senate redraft in the NDII lineage"),
    ("P-280", "SECTION 6 (c.265 s.43A(b)(5))", ""))
edges("S2710",
    ("P-266", "SECTION 7 (c.265 s.43A(b))", "later Senate redraft in the NDII lineage"),
    ("P-280", "SECTION 7 (c.265 s.43A(b)(5))", ""))
for b in ("S2834", "S2850"):
    edges(b,
        ("P-295", "new c.239 s.16(b)-(h),(j)", "Senate Affordable Homes vehicle"),
        ("P-296", "new c.239 s.16(i); c.93 s.52(a)(7)", "Senate Affordable Homes vehicle"))
QUOTES.update({
    ("S1116", "P-226"): "a person may bring a civil action ... doxing ... disclosure of personally identifying information with intent to harass",
    ("H1707", "P-226"): "the person disseminated the personal information with the malicious intent to cause, aid, encourage or facilitate the harassment",
    ("S23", "P-291"): "notary shall not use, sell, offer for sale, or transfer personal information obtained from remote notarization (SECTION 30)",
    ("H3375", "P-299"): "photographs ... and personal identifying information ... shall not be a public record",
    ("H4166", "P-299"): "photographs and personal identifying information not a public record (s.8(c))",
    ("H4287", "P-299"): "photographs and personal identifying information not a public record (s.8(c))",
    ("H3375", "P-300"): "shall not be discoverable in any judicial or administrative proceeding ... without a court order",
    ("H4166", "P-300"): "non-discoverability absent court order (s.8(b))",
    ("H4287", "P-300"): "non-discoverability absent court order (s.8(b))",
    ("H3375", "P-302"): "may not use, disclose, sell or permit access to camera data except to process violations",
    ("H3336", "P-302"): "recordings property of the municipality; vendor use for any other purpose banned",
    ("H4166", "P-302"): "city/manufacturer/vendor use/disclosure/sale/access ban beyond violation processing (s.8(e))",
    ("H4287", "P-302"): "use-limitation on camera operation and data (s.8(d)-(e))",
    ("H3375", "P-332"): "capture only on violation; destruction within 48 hours of final disposition",
    ("H3336", "P-332"): "non-violation footage destroyed in 30 days; violation records destroyed 1 year after final disposition",
    ("H4166", "P-332"): "capture only on violation + destruction within 48h of final disposition (s.8(a))",
    ("H4287", "P-332"): "capture only on violation + destruction within 48h of final disposition (s.8(a))",
    ("H1873", "P-320"): "electronic monitoring notice, notice of change, annual systems inventory (c.149B ss.3-3B)",
    ("S1228", "P-320"): "general/director's/specific/simultaneous notice regimes with reasonable-suspicion exception (SS.3-6)",
    ("H3597", "P-320"): "pre-monitoring notice regime incl. vendors, dates/times, right-to-access notice (s.105E(i))",
    ("H1873", "P-321"): "allowable-purpose/strictly-necessary/least-invasive limits; prohibited practices: off-duty, private areas, facial/gait/emotion recognition (s.3C)",
    ("S1228", "P-321"): "collection limited to employer premises and work-related data; private-area monitoring ban (SS.2,7,12)",
    ("H1873", "P-322"): "use limits and no sole reliance on monitoring data for decisions (s.3D)",
    ("S1228", "P-322"): "no adverse action without compliance; no sole-basis quotas (SECTION 9)",
    ("H3597", "P-322"): "practical-necessity plus least-invasive test; ban on relying on biometric/in-home/personal-device/geofencing data (s.105E(i))",
    ("S1228", "P-323"): "employee right to review/copy monitoring data (SECTION 8)",
    ("H3597", "P-323"): "employee right to copy work-speed data every 7 days, correction rights (s.105E(j))",
    ("H3289", "P-342"): "adds licensed private detectives/investigators to c.90 s.30A; prohibits use of RMV computer data inconsistent with c.147 s.22(2)",
    ("S2250", "P-342"): "adds PIs to authorized RMV computer-data users; prohibition on use of RMV data inconsistent with c.147 s.22",
    ("H3289", "P-343"): "prohibits accessing the RMV facial recognition system, with mandatory license revocation",
    ("S2250", "P-343"): "prohibition on accessing the RMV facial recognition system; mandatory license revocation",
})

# Fourth-pass review corrections: filed carriers of the TNC trip-data regime
# (section-level comparison against 2024 c.206 s.15) and the H1791 companion
# of S938.
for b in ("S666", "H1099", "H1158", "S627"):
    edges(b,
        ("P-303", "c.159A1/2 s.12(a)-(c) (within the bill's TNC/TND provisions)", "filed carrier of the regime enacted at 2024 c.206 s.15"),
        ("P-304", "c.159A1/2 s.12(d)-(e)", "filed carrier of the regime enacted at 2024 c.206 s.15"))
edges("H1791", ("P-255", "c.258C s.15 (sole section)", "companion-grade match to S938 (Jaccard 0.827)"))
QUOTES.update({
    ("S666", "P-303"): "the geographic position of the vehicle during the entire duration of the pre-arranged ride, provided at intervals of not less than every 60 seconds",
    ("H4799", "P-303"): "the geographic position of the vehicle during the entire duration of the pre-arranged ride, provided at intervals of not less than every 60 seconds (2024 c.206 s.15)",
    ("S666", "P-304"): "shall not be considered a public record ... shall not be disclosed to any person or entity other than those listed",
    ("H4799", "P-304"): "shall not be considered a public record ... de-identified trip data (2024 c.206 s.15)",
    ("H1099", "P-303"): "trip-level data ... at intervals of not less than every 60 seconds",
    ("H1158", "P-303"): "trip-level data ... at intervals of not less than every 60 seconds",
    ("S627", "P-303"): "trip-level data ... at intervals of not less than every 60 seconds",
    ("H1099", "P-304"): "shall not be considered a public record; de-identified sharing under agreements",
    ("H1158", "P-304"): "shall not be considered a public record; de-identified sharing under agreements",
    ("S627", "P-304"): "shall not be considered a public record; de-identified sharing under agreements",
    ("H1791", "P-255"): "shall be confidential and privileged, and shall not be disclosed by the division",
    ("S938", "P-255"): "shall be confidential and privileged, and shall not be disclosed by the division",
})

# Second corpus-triage pass (widened confidentiality screen + recovered PDF
# texts): nine vehicle-stage carriers of existing enacted propositions and
# one new record-class protection.
PROPS.update({
    "P-360": ("immunization-exemption-record-confidentiality", "health", "Medical immunization-exemption certifications confidential; no disclosure outside the school health program"),
    "P-363": ("immunization-exemption-inadmissibility", "health", "Immunization-exemption certifications inadmissible in proceedings absent written parental consent"),
    "P-364": ("immunization-exemption-physician-shield", "health", "Certifications may not be used against the certifying physician's rating or standing with employers, insurers, or affiliations"),
    "P-370": ("immunization-certifier-disciplinary-immunity", "health", "Certifying physicians immune from licensing or disciplinary action absent manifest bad faith"),
    # camera lineage successors (fixed-point traversal; H4940 enacted as 2024 c.399)
    "P-368": ("dv-report-confidentiality-study", "govt-records", "Task force to review domestic-violence report confidentiality laws and recommend survivor protections"),
    "P-369": ("victim-notice-protected-report-access", "govt-records", "Victim must be notified when an advocate or counselor not specifically authorized requests access to a protected police report"),
})
edges("H582",
    ("P-360", "SECTION 1 (rewritten c.76 s.15, confidentiality clause)", ""),
    ("P-363", "SECTION 1 (admissibility clause)", ""),
    ("P-364", "SECTION 1 (rating/standing clause)", ""),
    ("P-370", "SECTION 1 (manifest-bad-faith immunity clause)", ""))
for b, cite, note in (
    ("H57", "inserted c.222 s.29 (bill lines 673-677)", "Governor's FY23 supplemental filing carrying the notary restriction"),
    ("S24", "s.19 (new c.222 s.29)", "Senate Ways and Means FY23 supplemental stage"),
    ("H3548", "inserted c.222 s.29 (amendment lines 740-744)", "House further-amendment stage of the FY23 supplemental"),
):
    edges(b, ("P-291", cite, note))
for b, note in (("S2888", "Senate supplemental stage; pre-geolocation drafting variant"),
                ("S2891", "Senate supplemental reprint (text adopted by H4799)")):
    edges(b,
        ("P-303", "s.14/s.15 (c.159A1/2 s.12(a)-(b))", note),
        ("P-304", "s.14/s.15 (c.159A1/2 s.12(d))", note))
edges("H4138",
    ("P-295", "SECTION 47 (new c.239 s.15(a)-(d))", "Affordable Homes filing stage; sealing regime variant"),
    ("P-296", "SECTION 47 (c.239 s.15 consumer-report provisions)", "Affordable Homes filing stage"))
for b, sec in (("H5049", "SECTION 70"), ("H5132", "SECTION 27")):
    edges(b, ("P-294", f"{sec} (amending c.268B s.3)", "closeout-supplemental stage carrying the withholding expansion"))
edges("H5154",
    ("P-299", "SECTION 1 (c.4 s.7 cl.26(w)); c.90K s.5(b)", "House redraft of S2884"),
    ("P-300", "c.90K s.5(a)", "House redraft of S2884"),
    ("P-301", "c.90K s.5(c)", "House redraft of S2884"),
    ("P-302", "c.90K s.5(d)", "House redraft of S2884"))
QUOTES.update({
    ("H57", "P-291"): "prohibition on notary use, sale, or transfer of personal information obtained in remote notarization (c.222 s.29)",
    ("S24", "P-291"): "notary may not use, sell, or transfer personal information identifying a remotely-located individual (s.19, c.222 s.29)",
    ("H3548", "P-291"): "prohibition on notary use, sale, or transfer of personal information obtained in remote notarization (c.222 s.29)",
    ("S2888", "P-303"): "mandatory trip-level data reporting to the DPU division incl. driver universally-unique identifier",
    ("S2888", "P-304"): "sharing only of de-identified trip-level data under confidential data-sharing agreements; not a public record",
    ("S2891", "P-303"): "trip-level data reporting mandate incl. driver UUID and residence (s.15)",
    ("S2891", "P-304"): "de-identified sharing under confidential data-sharing agreements only; not a public record (s.15)",
    ("H4138", "P-295"): "eviction-record sealing with petition right (SECTION 47, new c.239 s.15)",
    ("H4138", "P-296"): "consumer-report inquiry duties with AG warning enforcement (SECTION 47)",
    ("H5049", "P-294"): "personal email, personal/home telephone, and family-member name and home address withheld (SECTION 70)",
    ("H5132", "P-294"): "personal email, personal/home telephone, and family-member name and home address withheld (SECTION 27)",
    ("H5154", "P-299"): "public-records exemption for photographs/PII collected under new c.90K",
    ("H5154", "P-302"): "confidentiality and no use/disclosure/sale of camera data by enforcing authorities and vendors",
})
QUOTES.update({
    ("H5154", "P-300"): "non-discoverability/non-admissibility of camera evidence absent court order (c.90K s.5(a))",
    ("H5154", "P-301"): "ban on using photographs to identify operator/passengers/contents plus redaction duty (c.90K s.5(c))",
})
QUOTES.update({
    ("H3375", "P-301"): "no frontal photographs; avoid identifying operator, passengers or contents (s.8(d))",
})

# Fifth-pass grammar-screen admissions.
PROPS.update({
    "P-365": ("taxpayer-examination-records-shield", "govt-records", "Identities of persons under municipal tax examination and records disclosed to the treasurer excluded from public-records disclosure"),
    "P-366": ("railroad-fatality-report-confidentiality", "govt-records", "Police reports of railroad fatalities and officer-crew communications non-public, with access limited to enumerated parties"),
    "P-367": ("union-communications-privilege", "workplace", "Labor organizations may not be compelled to disclose communications received in confidence from employees, with enumerated exceptions"),
})
edges("H1062", ("P-365", "SECTION 1 (c.60 amendment)", "sole section"))
for b in ("H4731", "S2809"):
    edges(b, ("P-366", "new c.160 s.253", "identical companion"))
edges("H1939", ("P-367", "new section (b)-(d)", "privilege with subsection (c)-(d) exceptions attaching"))
QUOTES.update({
    ("H4731", "P-366"): "shall not be made public and shall be maintained by the police department that responds to such fatality",
    ("S2809", "P-366"): "shall not be made public and shall be maintained by the police department that responds to such fatality",
})


# Sixth-pass admissions: camera-lineage successor stages (H4450 redraft of
# H3336/H3375; H4940 enacted as 2024 c.399 per its official history - the
# SessionLaws API list omits this chapter, see the adjudication note) and
# two term-form-independent primary-object filings.
edges("H4450",
    ("P-302", "school-bus camera section (municipal ownership; vendor no-other-use)", "redraft of H3336/H3375; RMV-vendor security regime (P-333) not carried"),
    ("P-332", "destruction clauses (30-day non-violation / 1-year post-disposition)", "redraft of H3336/H3375"))
edges("H4940",
    ("P-301", "notice-of-liability clause (no frontal images; no operator/passenger/contents identification)", "ENACTED as 2024 c.399"),
    ("P-302", "ownership/vendor clause (images property of municipality; vendor no-other-use)", "ENACTED as 2024 c.399"),
    ("P-332", "destruction clauses (30-day / 1-year with annual attestation to the state secretary)", "ENACTED as 2024 c.399"))
edges("S1136", ("P-368", "new c.41 s.97D1/2", "sole section"))
edges("S1503", ("P-369", "c.41 s.97D amendment (sole section)", ""))
QUOTES.update({
    ("H4450", "P-302"): "shall be the property of the municipality under agreement with a vendor and shall not be used by a vendor for any other purpose",
    ("H4940", "P-302"): "shall be the property of the municipality under agreement with a vendor and shall not be used by a vendor for any other purpose",
    ("H4450", "P-332"): "destroyed ... within 30 days of the date the image was recorded ... destroyed within 1 year of final disposition",
    ("H4940", "P-332"): "destroyed ... within 30 days of the date the image was recorded ... destroyed within 1 year of final disposition",
    ("H4940", "P-301"): "shall not include a frontal view photograph or video image ... or images that identify the operator, passengers or contents of the vehicle",
})
