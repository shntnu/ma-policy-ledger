# Atomization working notes: student/education data family

Produced by a reading pass over cached bill texts (billtext.py); consolidated
into scripts/atoms.py after cross-checking. Section cites refer to bill
sections; quotes are verbatim from the cached text.

BILL-BY-BILL ATOMIZATION

=== H532 -- An Act relative to student and educator data privacy (K-12 edtech operator regulation; inserts G.L. c.71 ss.34I-34L) ===

1. edtech-operator-targeted-ad-ban -- Prohibits K-12 edtech operators from targeted advertising based on information acquired through school use of their service. SECTION 1 (new c.71 s.34J(a)(1)). "shall not ... engage in targeted advertising on the operator's site, service or application"
2. edtech-operator-profiling-ban -- Prohibits operators from using covered information to amass a profile of a student or educator except for K-12 school purposes. SECTION 1 (s.34J(a)(2)). "to amass a profile about a student or a teacher, principal or administrator"
3. edtech-operator-sale-ban -- Prohibits sale or rental of student information, with merger and national-assessment-consent exceptions. SECTION 1 (s.34J(a)(3)). "sell or rent a student's information, including covered information"
4. edtech-operator-disclosure-limits -- Prohibits disclosure of covered information except under legal compulsion, approved de-identified research, or to educational entities. SECTION 1 (s.34J(a)(4)). "an operator may disclose covered information of a student so long as clauses (1) through (3) ... are not violated"
5. edtech-operator-reasonable-security -- Requires operators to maintain reasonable security procedures for covered information per board regulations. SECTION 1 (s.34J(b)(1)). "implement and maintain reasonable security procedures and practices appropriate to the nature of the covered information"
6. edtech-operator-return-destroy -- Requires operators to return or destroy covered information on educational-entity request or when no longer needed. SECTION 1 (s.34J(b)(2)). "immediately return or destroy covered information if requested by the educational entity"
   [Enforcement attaches to props 1-6 as a bundle, per grain limit: private right of action for aggrieved student or educational entity, $10,000 per disclosure/adverse action, punitive damages, fees (s.34J(e)); plus commissioner may bar violating operator from evaluation records for 5+ years (s.34J(f), process in s.34L(a)). Companions identical, so not split out. "may recover: (1) up to $10,000 for each disclosure that violates this section"]
7. edtech-contract-mandatory-terms -- Requires every educational-entity/operator contract touching covered information to contain eight enumerated data-protection clauses; noncompliant contracts voidable and data returned/destroyed. SECTION 1 (s.34K). "Any contract that fails to comply with the requirements of this section shall be voidable"
8. dese-data-governance-cpo -- Board must promulgate data security/privacy regulations and minimum operator security standards; commissioner appoints a chief privacy officer to develop policy, model contracts, training, oversight; educator-prep programs must include data-privacy curricula. SECTION 1 (s.34L(a)-(b)). "The commissioner shall appoint a chief privacy officer with experience in data privacy and security."
9. dese-data-inventory-transparency -- Department must publish a list of categories of covered information it collects with source, reason, and use. SECTION 1 (s.34L(c)). "make publicly available a list of categories of covered information collected by the department"
10. district-privacy-policy-breach-reporting -- Each district must adopt a privacy/security policy including 10-business-day breach reporting to the commissioner and designate a student data manager. SECTION 1 (s.34L(d)). "report all significant data breaches of student data ... within ten business days"
11. district-data-inventory-operator-list -- Each district must publish on its website categories of student PII collected and its current and 10-year historical operator contracts. SECTION 1 (s.34L(e)). "a list of the operators with which the district has a contract or agreement"
12. district-staff-privacy-training -- Districts must annually train employees with data access; training is a condition of educator certification. SECTION 1 (s.34L(f)). "annual training regarding the confidentiality of student data to any employee with access to covered information"

=== S280 -- An Act relative to student and educator data privacy ===

Identical text to H532 (verified: normalized diff empty). Carries propositions 1-12 above with identical section cites and quotes. Exact companion.

=== H1283 -- Public higher-ed student records exempt from public records law ===

1. public-records-ferpa-exemption -- Exempts public colleges/universities from producing FERPA education records, including directory information, under the public records law. Single unnumbered SECTION (new c.66 s.22). "shall not be required to produce records defined as education records in the Family Education Rights and Privacy Act"

=== S844 -- Public higher-ed student records exempt from public records law ===

1. public-records-ferpa-exemption -- Same mechanism (new c.66 s.22); variant: extends to "municipally owned institutions of higher education" and adds a government-requester carve-out. SECTION 1. "This section shall not apply to requests from federal, state, or municipal agencies."
   (Carve-out fails standalone-sense test; attaches to the exemption as a variant, not a separate proposition.)

=== H4266 -- Public higher-ed student records exempt from public records law (redraft of H1283) ===

1. public-records-ferpa-exemption -- Text is H1283 verbatim plus S844's government-agency carve-out sentence appended; does NOT pick up S844's municipal-institution extension. Single unnumbered SECTION (new c.66 s.22). "This section shall not apply to requests from federal, state, or municipal agencies."

=== H530 -- Establishing the Massachusetts Education-to-Career Data Center (new G.L. c.7E) ===

1. e2c-center-system-board -- Establishes the Education-to-Career Data Center within EOTSS with an executive director, the longitudinal Data System, and a 15-member governing board with privacy/security, de-identification, data-request-process, and transparency duties. SECTION 1 (c.7E ss.1, 2(a)-(d), 3(a)-(b),(f), 4). "The Massachusetts Education-to-Career Data Center is hereby established within the Executive Office of Technology Services and Security."
2. e2c-agency-data-mandate -- Requires EEC, DESE, DHE, and DUA (plus board-approved others) to provide data to the system at least annually; providers retain ownership. SECTION 1 (c.7E s.3(c)-(e)). "At least once per year, the following public agencies shall provide data to the data system"
3. e2c-ferpa-authorized-rep -- Deems the center a FERPA authorized representative of DESE, DHE, and DUA to access and compile student record and wage data for research. SECTION 1 (c.7E s.2(e)). "the center shall be considered an authorized representative of the state department of elementary and secondary education"
4. e2c-strategic-initiative-evaluation -- Board may designate strategic initiatives for enhanced data collection/evaluation via special committees with statistical expertise. SECTION 1 (c.7E s.5). "may determine that a strategic initiative of the commonwealth merits enhanced data collection or evaluation"
5. e2c-local-rpp-linking -- Authorizes municipal research-practice partnerships with center support for linking local data to the system. SECTION 1 (c.7E s.6). "developing policies and procedures to link local data to the data system"
   (SECTION 2 effective-upon-passage attaches to prop 1.)

=== S343 -- Education-to-Career Data Center ===

Identical text to H530 (verified: normalized diff empty). Propositions 1-5 as H530. Exact companion.

=== H4421 -- Education-to-Career Data Center (redraft of H530/S343) ===

Propositions 1-5 as H530 with same cites. Redraft changes (verified by diff), all within prop 3 e2c-ferpa-authorized-rep plus cosmetics:
- s.2(e): adds sentence requiring UI-data disclosures to comply with federal confidentiality regs: "shall adhere to the requirements of 20 C.F.R. Part 603 and state law concerning the confidentiality"
- s.2(e): drops "state" before each department name (cosmetic).
- s.5(c): "said agencies" -> "the agencies" (cosmetic).
Same proposition set; prop 3 recorded as stricter variant (added UI-confidentiality condition) on the H4421/S2666 edges.

=== S2666 -- Education-to-Career Data Center (redraft) ===

Identical to H4421 except two curly-quote glyphs (verified). Propositions 1-5 with the H4421 variant of prop 3. Exact companion of H4421.

=== H1893 -- Social media account privacy (students and employees) ===

1. student-social-media-password-ban-highered -- Prohibits higher-ed institutions (including UMass via parallel c.75 codification) from requiring disclosure of or access to a student's or applicant's personal social media account, compelling contact-adds, or retaliating; private right of action ($1,000 per violation) attaches; investigation exception. SECTIONS 1 (new c.15A s.45), 3 (new c.75 s.48, same mechanism restated for UMass). "shall not ... require, request or cause a student or applicant to disclose a user name, password"
2. student-social-media-password-ban-k12 -- Same mechanism aimed at elementary/secondary institutions; PRA attaches. SECTION 2 (new c.71 s.97). "a public or private institution providing elementary or secondary education located in the commonwealth"
3. employee-social-media-password-ban -- Same mechanism aimed at employers (interns included); enforcement via c.149 s.150 attaches. SECTIONS 4-5 (c.149 s.150 amendment; new c.149 s.192). "An employer shall not ... require, request or cause an employee or applicant to disclose a user name, password"
   (Note: prop 3 is employee privacy, outside the student/children subdomain but in the bill; same legal mechanism as props 1-2 at a different target, hence a separate proposition.)

=== H80 -- An Act relative to internet privacy protection for minors (new G.L. c.93 s.115) ===

1. minor-directed-prohibited-product-ads -- Bans operators from marketing 19 enumerated adult products (alcohol, firearms, tobacco, cannabis, obscene matter, etc.) on minor-directed sites or targeted to known minors, with advertising-service notification safe harbor. SECTION 1 (s.115(b),(c),(f),(g),(h)). "shall not market or advertise a product or a service described in subsection (g)"
2. minor-info-marketing-use-ban -- Bans operators from using, disclosing, or compiling (or letting third parties compile) a minor's personal information for marketing the prohibited products. SECTION 1 (s.115(d)). "shall not knowingly use, disclose, compile, or allow a third party to use, disclose or compile, the personal information of a minor"
3. minor-eraser-right -- Requires operators to let registered minor users remove (or request removal of) content they posted, with notice, instructions, and enumerated exceptions; anonymization/invisibility compliance options. SECTION 1 (s.115(i),(k),(m)). "permit a minor who is a registered user ... to remove or ... request and obtain removal of, content"
   (Enforcement attaches to props 1-3 as a bundle: $2,500 civil penalty per violation, AG action, s.115(j); no-age-collection disclaimers (e),(n) and SECTION 2 effective date Jan 1, 2024 attach. "civil penalty of not more than $2,500 per violation")

=== H1986 -- Resolve: special commission on children's mental health and social media ===

1. children-social-media-commission -- Creates a special commission to study social media harms to children and recommend a legal framework, reporting with draft legislation by Dec 31, 2024. Single resolve (unsectioned). "there shall be a special commission on children's mental health and social media"
   In-domain (data-practice) scope within the charge: independent algorithm-audit framework including transparency audits and risk assessments (clause (ii)); "methods to ensure privacy in age verification" (iii)(2); "data management best practices to mitigate the unauthorized access of a child's personal information" (iii)(3); privacy-ensuring tools for ages 13-18 (iii)(4). Remaining charges (mental-health harms, parent guidance, awareness campaigns) are out-of-domain content of the same single proposition; a study commission does not atomize by charge.

CROSS-BILL

- H532 = S280: exact companions, byte-identical after whitespace normalization. All 12 propositions shared 1:1.
- H1283 / S844 / H4266: one shared proposition (public-records-ferpa-exemption), same mechanism (new c.66 s.22 public-records exemption), variants: H1283 broadest (no carve-out, public colleges/universities only); S844 = + municipally owned institutions, + federal/state/municipal-agency requester carve-out; H4266 (redraft of H1283) = H1283 text + the agency carve-out only, no municipal-institution extension. Weaker/stricter variants of the same proposition, differences on the edges.
- H530 = S343 (exact companions) and H4421 = S2666 (exact companions, redrafts of the former). All five e2c propositions shared across all four bills. Redraft delta is confined to e2c-ferpa-authorized-rep: H4421/S2666 add the 20 C.F.R. Part 603 UI-confidentiality compliance sentence (stricter variant); other diffs cosmetic.
- H1893: no companion in this set. Its three propositions are one mechanism (compelled social-media-access ban + PRA) at three targets; no overlap with H532/S280, which regulate operator data handling, not institutional demands for account access (different mechanism, different regulated party).
- H80: standalone. Its targeted-marketing restriction is a different proposition from H532/S280 prop 1 (edtech-operator-targeted-ad-ban): different mechanism scope (product-category ad ban on minor-directed services vs total targeted-ad ban tied to school-purpose data) and different target (general operators re minors vs contracted K-12 operators).
- H1986: standalone; different mechanism (study commission) from every direct-regulation proposition above, so no shared propositions even where goals overlap H80 (children's online safety).
- No proposition is shared across bill families; sharing occurs only within the four companion/redraft clusters: {H532,S280}, {H1283,S844,H4266}, {H530,S343,H4421,S2666}, and the singletons {H1893},{H80},{H1986}.
