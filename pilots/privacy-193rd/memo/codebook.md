# Codebook: consumer data privacy, 193rd General Court (2023-2024)

Status: draft, census stage.
Later stages (atomization, linking, fate classification) will extend this file.

## Domain definition

A filing is IN the domain of consumer data privacy when at least one of its
provisions would change Massachusetts law governing the collection, use,
retention, disclosure, sale, or protection of information about an identified
or identifiable natural person, where that information is held or handled by
a party other than that person (a business, a data broker, a platform, a
government agency acting as a data holder, or another individual).

Included subdomains:

- comprehensive consumer data privacy regimes (controller/processor duties,
  consumer rights, opt-outs, private rights of action)
- data broker registration and regulation
- biometric identifiers and facial recognition
- location information, including location shields and geofencing
- genetic and health data privacy, including reproductive-health data
- children's and students' online data and social media data practices
- browsing, search, and telematics data
- data security and breach notification obligations
- interception of wire and electronic communications when the object is
  personal communications content (the modern wiretap boundary)
- privacy of images of a person (nonconsensual image distribution) ONLY when
  the mechanism is a data-handling rule; criminal harassment provisions
  without a data-handling rule are excluded
- government surveillance of individuals through commercial data or
  technology (for example, purchase of location data, ALPR databases)

Excluded, with the boundary rationale:

- pure cybersecurity of state systems with no individual-rights provision
  (infrastructure hardening, IT funding)
- artificial intelligence regulation UNLESS the provision governs personal
  data as defined above
- open-meeting or public-records law (transparency of government, not
  privacy of individuals' data), except provisions restricting disclosure of
  personal information held in public records
- financial reporting, "data" in the sense of statistics or program metrics
- identity-document rules (licenses, IDs) without a data-handling provision
- sick-leave banks, land takings, and other named-individual acts

## Census universe

- Source: `/api/GeneralCourts/193/Documents` on malegislature.gov,
  fetched 2026-08-04; 10,156 documents, of which 8,183 carry a bill number
  (bills, resolves, orders) and 1,973 are docket-book-only entries.
- Enacted-vehicle universe: `/api/SessionLaws/2023` and `/2024`,
  464 chapters, full text scanned, so budget outside sections are covered.

## Candidate-generation rules (recall net)

A document enters the candidate pool if any of:

1. Title matches a DOMAIN term regex (see `scripts/01_census.py`,
   `DOMAIN_TERMS`).
2. Title matches a BROAD term regex (`BROAD_TERMS`); these are kept only if
   full-text scan (`scripts/02_textscan.py`) finds domain text terms.
3. The document appears in the reported-out or before-committee list of the
   Joint Committee on Advanced Information Technology, the Internet and
   Cybersecurity (J33), regardless of title.

Known recall limitation: a bill whose title contains none of the broad terms,
that was never referred to J33, and whose privacy content appears only in its
text, is invisible to this net.
The enacted-vehicle sweep closes this gap for anything that became law; for
bills that died, the gap is real and is reported in the memo's limitations.

## Inclusion decision

Every candidate receives an explicit decision (include / exclude) with a
reason code, produced by `scripts/04_inclusion.py` and reviewed at the
census checkpoint. Reason codes:

- `IN-TITLE`: domain title term plus confirming text evidence
- `IN-TEXT`: broad-net title, domain confirmed in full text
- `IN-COMMITTEE`: J33 referral plus confirming text evidence
- `EX-FALSEPOS`: matched term used in a non-domain sense (for example
  "tracking" of prescription drug prices, "data" as program statistics)
- `EX-ADJACENT`: genuinely about information/technology but outside the
  domain definition above (with subcategory noted)
- `EX-NOBILL`: docket-book-only entry that never received a bill number;
  counted separately, text unavailable through the bill API
