# Handoff: seventh-pass review fixes (PR #1)

Written 2026-08-05 for a fresh session.
The seventh-pass Codex review is PR #1 comment id 5198544063
(https://github.com/shntnu/ma-policy-ledger/pull/1#issuecomment-5198544063).
All six findings were verified plausible during digestion; none has been
implemented.
`BRIEF.md` at the repo root is the controlling standard; read it first,
then this note, then the review comment itself.

## Current state

- Branch `pilot/privacy-193rd`, head `c83af7f`, PR #1 open against `main`
  (main was rewound to the initial commit so the PR diff shows everything;
  merging restores it).
- Headline as committed: 15 of 284 propositions enacted (5.3%), 139
  in-domain filings, 989 filings accounted, 8 enacted vehicles.
  These numbers WILL change again after finding 1.
- The pipeline is `pilots/privacy-193rd/scripts/run_all.sh` (01 -> 09).
  A clean `git archive` rerun with `FETCHLIB_OFFLINE=1` passes
  `09_checks.py` and regenerates `data/` byte-for-byte; keep that true.

## The six findings, with implementation guidance

### 1 (P1) Enacted universe from the official Acts index, not the API

`/api/SessionLaws/2024` returns 375 rows / 374 unique chapters, ends at
c.392, and omits 33 chapters that the official index
(https://malegislature.gov/Laws/SessionLaws/Acts/2024, chapters 1-407)
lists - including c.393-407 and 18 earlier gaps.
c.399 (already in the census via H4940's history) proves the omissions can
be in-domain.
Check 2023 for the same defect.

Implementation: new script (suggest `03b_acts_index.py`) that fetches and
caches the official index pages for 2023 and 2024, enumerates every
chapter number, fetches each chapter page not covered by the API response
(the chapter pages under /Laws/SessionLaws/Acts/{year}/Chapter{n} are
JS-shell HTML - the usable text may need the print route or PDF; probe
one first; c.399's page is already cached and is a shell, so expect to
need `/Laws/SessionLaws/Acts/2024/Chapter399` print/PDF variants), scans
each with the widened `TEXT_TERMS` from `02_textscan.py`, and emits the
chapter list + hits.
Then: adjudicate every newly flagged chapter row-level in `ADJUDICATIONS`
(scripts/08_fates.py) exactly like the existing rows; trace any in-domain
provision to its origin bill (chapter pages/API rows carry OriginBill
where available; for index-only chapters the bill history search may be
needed); admit lineages per the established feedback-loop pattern.
Add a 09 check asserting exact index-to-scan coverage (every chapter on
the official index is either scanned or recorded as unobtainable with a
reason).
Update the memo sentence "all 464 session laws" - the real universe is
the official index count, and the current claim is false.

### 2 (P1) Carry the fixed-point lineage records into census and atoms

- H3306 and H3440: parents of H4450 (its history: "New draft of S2275,
  H3306, H3336, H3375, H3440"), already fetched in
  `data/link_targets.json`, texts carry the school-bus-camera rules.
  Admit both (`04_inclusion.py` ADDITIONS, reason IN-ENACTED-FEEDBACK)
  and give them atom edges (verify which of P-299..P-302/P-332/P-333
  each text carries before writing edges - read the texts, do not assume).
  Note S2275 is already in the census; H4450's parent list also updates
  the redraft story.
- S3005: the Senate struck H4940's text and inserted S3005 (link graph
  already has `text_adopted_from`); the S3005 PDF is cached
  (data/pdf_texts/ or raw cache - check `textsim.full_text('S3005')`).
  The cached H4940 PDF is the PRE-amendment House text, so S3005 +
  Chapter 399 are the correct evidence for the enacted version.
  Admit S3005 (IN-ENACTED-VEHICLE stage), atomize from its text, and
  re-cite H4940's edges to the enacted-version evidence (c.399 s.2).

### 3 (P1) Atomize the court-order access rule and H4450's full carriage

H4450 also carries P-301 (no-frontal/occupant-identification) - add the
edge.
The court-order-only access rule (images unusable outside
enforcement/defense except by court order) appears in H4450, H4940,
S3005, and c.399 s.2 (new c.90 s.14C(d)(1)).
Decide: documented variant of P-300 (litigation limits) or a new
proposition under the same-mechanism test - then assign every carrying
stage consistently.
Recommendation from digestion: treat as a P-300 variant (same
litigation-access mechanism, school-bus target) with variant notes; if
you split instead, retire nothing - just add the new ID (P-371 is next
free; check `atoms.py` PROPS/RETIRED for collisions first).

### 4 (P1) Fate logic: represent ALL enacted final vehicles

`08_fates.py` around the enacted branch: `fb = enacted_finals[0]` and the
"independent filings ... died" detail wrongly sweeps OTHER ENACTED
vehicles into the died list (P-301/P-302 rows currently say S2884 "died"
even though it is enacted as c.363).
Fix: when multiple enacted finals exist, list all of them in the fate
detail and a new column if needed (e.g. `enacted_vehicles`), cite all,
and restrict the died-narrative to carriers whose terminal class is
actually non-enacted.
Update the 09 assertions accordingly (P-301/P-302 have two enacted
vehicles; expected fates stay enacted_as_filed).

### 5 (P1) H219 smallest-change splits

Split P-357 into: data-bank creation/operation; standardized application;
ID-card issuance; provider card-acceptance duty (verify each clause
stands alone in the text - `textsim.full_text('H219')`, s.16DD(d)).
Split P-362 into: application fee (s.16DD(b)) vs grant/loan/contract
eligibility conditioning (s.16DD(c)).
Retire P-357/P-362 (never reuse IDs; add to RETIRED with reason), mint
new IDs, keep QUOTES coverage for any inferred-analytic edges (09 fails
on missing quotes).

### 6 (P2) One current snapshot everywhere + count assertions

Fix ALL of:
- memo/findings.md: the "six of the fourteen" sentence and any remaining
  "14 enacted" (generated table says 15; after finding 1 the number may
  move again - sync LAST, after the pipeline settles).
- memo/codebook.md: "seven bills" enacted list (it is eight+: add H4940;
  re-check after finding 1); the fate section must include the
  H4940/P-332 occurrence; the roll-call sentence must acknowledge the
  S2834 Amendment 25 rejection (cached record: "MBTA Communities Act -
  Zoning Appeal", Roll Call 194, 6-34 - unrelated to privacy, but
  "every roll call was favorable" is false as written); "all 8,183
  screened" -> 8,178 with five unscanned (data/unscanned_bills.csv).
- PR #1 body: one section still carries 267/607/715/14-267/112/53-era
  numbers; rewrite the whole body against the final tables rather than
  patching strings.
- The response comment you will post: note that S1503/P-369 is
  died_no_recorded_action after a favorable report (the prior response
  mislabeled it sent-to-study).
- NEW CHECK (the reviewer's ask): extend `09_checks.py` to parse the
  headline numbers out of memo/findings.md (propositions total, enacted
  count, filings, census rows) and assert they equal the generated
  tables, so checks cannot pass alongside stale prose.

## Conventions and gotchas (hard-won; do not relearn)

- Politeness: fetchlib throttles 2.5s (bulk jobs may use ~1.2s); cache
  everything; never refetch; `FETCHLIB_OFFLINE=1` makes cache misses
  fatal - the final verification depends on it.
- All CSV writers go through `csvutil` (LF); normalize whitespace in any
  text written to CSVs (embedded CRLF in API titles bit us once).
- Judgment calls live as data-in-scripts: census OVERRIDES/ADDITIONS/
  TRIAGE-verdicts (scripts/corpus_triage_verdicts.csv), atoms
  PROPS/EDGES/QUOTES/RETIRED, 08 ADJUDICATIONS.
  Never hand-edit generated data/ files.
- Proposition IDs are persistent; retired IDs stay retired.
- Every inferred-analytic identity edge needs a QUOTES entry for the
  bill AND a comparator carrier, or 09 fails.
- The program-incident rule (codebook) is applied symmetrically; the
  H3735/c.221 call is intentionally contested-and-queued - do not
  reopen it silently.
- Successor cycles exist (H4799 <-> S2891); enacted carriers are always
  final vehicles.
- `scripts/actions.py` is the ONLY action parser; extend it (with
  fixtures in its self-test) rather than adding regex anywhere else.
- Markdown prose uses semantic line breaks; reflow with
  `python3 ~/.claude/scripts/reflow-md.py FILE`.
- memo/findings.md is a clean current-state snapshot - no revision
  narration; history belongs in the codebook revision log (dated) and
  the PR thread.

## Verification recipe (must pass before pushing)

    cd pilots/privacy-193rd/scripts && python3 actions.py && python3 09_checks.py
    # clean-archive, fully offline, byte-identical:
    T=$(mktemp -d) && git archive HEAD | tar -x -C "$T" \
      && cd "$T/pilots/privacy-193rd/scripts" \
      && FETCHLIB_OFFLINE=1 sh -c 'python3 01_census.py && python3 02_textscan.py \
         && python3 03_sessionlaws.py && python3 01b_full_corpus_screen.py \
         && python3 04_inclusion.py && python3 05_histories.py \
         && python3 05c_link_targets.py && python3 06_compile_atoms.py \
         && python3 07_links.py && python3 08_fates.py && python3 09_checks.py' \
      && diff -rq "$T/pilots/privacy-193rd/data" <repo>/pilots/privacy-193rd/data

## Wrap-up steps after the fixes

1. Commit with a clear message (signed; Co-Authored-By trailer per
   local convention), push to `pilot/privacy-193rd`.
2. Update the PR #1 body wholesale to the final numbers.
3. Post a point-by-point response comment on PR #1 addressing findings
   1-6, ending with the standard Claude Code attribution line.
   Correct the S1503 fate mislabel from the sixth-pass response there.
4. Update the codebook revision log with a dated seventh-pass entry.
