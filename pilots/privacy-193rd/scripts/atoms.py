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
    "P-123": ("location-minimization", "location", "No more precise, longer-retained, or further-inferred location data than the purpose requires"),
    "P-124": ("location-sale-disclosure-ban", "location", "Ban on sale/rent/trade/lease of location information and unnecessary third-party disclosure"),
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
    "P-221": ("scorecard-personal-data-content-limit", "commercial", "Energy scorecards may not contain personal data beyond address and rating"),
    "P-222": ("scorecard-nondisclosure-consent", "commercial", "Energy scorecards not disclosable without owner consent; public-records exempt"),
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
    "P-266": ("ndii-distribution-ban", "interpersonal", "Criminal offense to distribute (or threaten to distribute) identifiable nude or sexual visual material without consent, with intent to harm or reckless disregard; enacted version adds deepfake 'digitization' coverage"),
    # --- S2539 delegated data-governance rulemaking (review finding 8) ---
    "P-267": ("ai-training-data-consent-rulemaking", "comprehensive", "Directs regulations requiring informed consent before collecting, using, sharing, or disclosing individuals' data for AI training, plus deletion or de-identification on request"),
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
}

# Retired proposition IDs (never reused). Kept for the audit trail.
RETIRED = {
    "P-011": "split into P-271..P-274 (severability, review finding 4)",
    "P-036": "split into P-275/P-276 (severability consistency)",
    "P-244": "split into P-277/P-278 (severability consistency)",
    "P-265": "H4844 re-atomized onto P-121/P-123/P-124/P-125 as narrowed variants (review finding 3)",
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
    ("P-123", "c.93N s.2(e)(1),(2),(4)", ""),
    ("P-124", "c.93N s.2(e)(3),(5)", "retroactive application of sale ban"),
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
    ("P-123", "c.93L s.2(e)(1),(2),(4)", ""),
    ("P-124", "c.93L s.2(e)(3),(5)", ""),
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

edges("H3217",
    ("P-221", "SECTION 6", ""),
    ("P-222", "SECTION 9 (c.25A s.17(e))", ""),
)
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
# shield. Weaker-scope variants of the same mechanisms per the codebook rule.
_H4844_NOTE = "narrowed to reproductive/gender-affirming-care location information; enforcement is 93A/AG only (no private right of action)"
edges("H4844",
    ("P-121", "c.93M ss.1,2(a); SECTIONS 2-3", _H4844_NOTE),
    ("P-123", "c.93M s.2(b)-(d) (precision, retention, inference minimization)", _H4844_NOTE),
    ("P-124", "c.93M s.2(e) (sale/rent/trade/gift/lease ban; third-party disclosure restriction)", _H4844_NOTE),
    ("P-125", "c.93M s.2(f) (government warrant gate)", _H4844_NOTE),
)

# NDII lineage: standalone filings, Judiciary redraft, engrossed and
# conference vehicles. H4241/H4744 have no API text; the enacted text is
# 2024 c.118 (https://malegislature.gov/Laws/SessionLaws/Acts/2024/Chapter118).
for b in ("H1745", "S1012", "S1139"):
    edges(b, ("P-266", "SECTION 5 (c.265 s.43A(b) rewrite)",
              "as-filed version; no digitization (deepfake) coverage"))
edges("H4115", ("P-266", "SECTION 6 (c.265 s.43A(b) rewrite)", "Judiciary redraft; no digitization coverage"))
edges("H4241", ("P-266", "engrossed text of H4115 SECTION 6 lineage (API text empty; see c.118 s.6)", "House-engrossed vehicle"))
edges("H4744", ("P-266", "2024 c.118 s.6 (c.265 s.43A(b)-(c))", "ENACTED; conference text adds 'digitization' (deepfake) coverage"))
edges("S2539",
    ("P-267", "SECTION 1 (c.7D s.17(f)(iv))", "delegated rulemaking over personal data in AI training; boundary call recorded in codebook"))

EDGES = E

OUT_OF_DOMAIN = {
    "S1896": "Municipal Broadband Fund (c.65D s.4; c.29 s.2RRRRR): broadband finance",
    "H3217": "Energy scorecard program design and funding (SECTIONS 1-5, 7-8, 10-16)",
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
