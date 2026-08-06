# Handoff: eighth-pass review fixes (PR #1)

Written 2026-08-06 for a fresh session.
`BRIEF.md` at the repo root is the controlling standard; read it first, then this note, then `memo/review-eighth-pass.md`, which is the full review report.

## Provenance of this review

Unlike passes one through seven, this review was not external.
It was produced in-repo by a 31-agent adversarial workflow: six independent auditors (census completeness, atomization grain, evidence integrity, fate classification, checks efficacy, public claims), each finding then handed to a separate verifier instructed to REFUTE it and to default to refuted when uncertain. 22 findings survived; 2 were refuted and dropped.

Treat the surviving findings as credible but not sacred.
Two were already refined during verification, and finding 3 turns on a judgment the project has not yet made explicitly.
Reproduce before you fix.

## Current state

- Branch `pilot/privacy-193rd`, head `2b02165`, clean tree, PR #1 open.
- Headline as committed: 16 of 289 propositions enacted (5.5%), 142 in-domain filings, 992 filings accounted, 8 enacted vehicles, 497 officially indexed session-law chapters.
  Findings 1, 3, 4 and 7 all move published numbers.
- Pipeline is `scripts/run_all.sh` (01 -> 09, with 03b before 03).
  A clean `git archive` rerun with `FETCHLIB_OFFLINE=1` passes `09_checks.py` and regenerates `data/` byte-for-byte; keep that true.

## The findings, ranked, with implementation guidance

Findings 1, 2, 6 and 7 were reproduced directly at the main-loop level after the workflow returned; the rest rest on the auditors' and verifiers' work.

### 1 (P1) The stage parser misses "Hearing rescheduled to"

`08_fates.py` bumps the ladder to `heard` only on `"hearing scheduled" in low`.
Thirteen census bills carry ONLY an unstricken "Hearing rescheduled to" row (H76, S30, H3831, H3863, S198, S27, H1099, H1158, H219, H3637, H582, S627, S666).
All 19 propositions currently reported at `referred` sit on three of them (H219, H3831, H582), so "19 propositions never got a hearing" is false; the true figure is 0.

Fix: bump `heard` on "hearing rescheduled" as well, regenerate, and correct `memo/findings.md` (expect 0 never heard, 167 stalled in policy committee, 84 heard only, 83 reporting-extended - confirm against the regenerated table rather than trusting these numbers).
`09_checks.py` HEADLINES asserts the memo's "19" against the same parser, so today a green suite only certifies that the prose matches the bug; the assertions will follow the regenerated values automatically once the parser is fixed.
Document in the codebook what `heard` measures (a hearing scheduled OR rescheduled on the official history) - it currently never says.

### 2 (P1) Two adverse roll calls, not one

Scanning all 142 census histories with the pipeline's own two regexes gives 73 recorded tallies, of which two have nays exceeding yeas:

- S2834 Amendment 25, "MBTA Communities Act - Zoning Appeal", 6-34
- H4040, "Motion to suspend Rule 40 rejected - 25 YEAS to 132 NAYS (See YEA and NAY No. 31)"

The H4040 action is unstricken, sits in the cached official API response, is already published in `data/bill_fates.csv`, and propagates into the `roll_calls` column of P-297 and P-298.
So the memo's cited example attaches to no proposition while the one it omits attaches to two.
`memo/findings.md` and `memo/codebook.md` both say "exactly one" / "the single adverse roll call".

Fix: correct both documents to state both, and keep the substantive claim, which is still true and is the one that matters: no PROPOSITION was defeated on the record.
Consider a 09 assertion over the adverse-tally count so the sentence cannot go stale again.

Related, same finding: `rejected_by_recorded_vote` is documented as a fate in the `08_fates.py` docstring and `codebook.md` but no code path can emit it - `bill_status` collects roll-call strings and never compares yeas to nays.
Either implement it or say plainly in the codebook that the category is defined but unreachable, and why.

### 3 (P1) P-295/P-296 detail denies a chain the project publishes

The fate detail says six carriers "have no official chain" to H4977 and cites `absorbed_into_vehicle` links as the substitute basis.
Both halves are wrong: `data/links.csv` already publishes, as verified-official-record, S2834 -> H4726, S2850 -> H4726, H4138 -> H4707, and H4977 reported_on H4726; and `grep absorbed_into_vehicle data/links.csv` returns no row for H4138, S2834 or S2850 - exactly the three carriers that have chains.

The cause is mechanical: `successor_map` is built from `histories.json`, which holds census bills only, and H4707/H4726 were correctly excluded from the census for not carrying the sealing provision.

DO NOT relabel silently.
Relabeling P-295/P-296 to `enacted_as_filed` would make them the first chains running through non-carrier stages, which is a real methodological choice - the codebook's `enacted_as_filed` definition has no carrier-membership condition, but every existing instance happens to satisfy one.
Decide it explicitly, write the decision into the codebook, and note it in the PR response either way.

What is wrong regardless of that decision: the detail sentence asserts the absence of a chain the project itself publishes as verified, and offers evidence that does not exist.
At minimum, build the fate-stage successor map from `histories.json` union the history-bearing entries of `link_targets.json` and make the detail cite real evidence.
`memo/findings.md`'s "absorbed into unrelated enacted vehicles after their filed carriers died" is also wrong for H4138, whose terminal class is `superseded_by_redraft`, not death.

### 4 (P2) P-332 and P-301 claim mechanisms their chapters lack

P-332 bundles two severable mechanisms: capture-only-on-violation and a destruction schedule. 2024 c.399 contains the word "capture" ZERO times - only the destruction half was enacted - yet the whole proposition reads `enacted_as_filed`.
The project splits exactly this collection/retention pair everywhere else (P-281/P-282 in H4844, P-193/P-194 in the ALPR family), and `findings.md` already narrates c.399 as enacting only the destruction regime, so the prose knows what the dataset denies.
Split it, retire P-332 with a RETIRED entry, mint new IDs.
Expect the capture-limit proposition to come out `sent_to_study` with `dropped_in_consolidation = yes`.

P-301's description asserts "mandatory redaction before notices issue". "redact"/"obscure" appear in only 3 of its 12 carriers, and c.399 has zero redaction hits - what it has is the opposite savings clause.
Merging strictness variants is permitted, but the codebook requires the difference be recorded on the edge, and none of P-301's twelve edge notes does.
Either split the redaction duty or narrow the description to the shared rule and record the variant on the affected edges.

### 5 (P1) Evidence integrity: the queue's "verbatim" excerpts

58 of 155 `QUOTES` entries are not verbatim from the cited bill under a deliberately generous matcher (case- and punctuation-insensitive, splits on " ... ", drops standalone digit tokens so PDF line numbers cannot cause false negatives, strips trailing "(2024 c.206 s.15)" style cites).
In `data/verification_queue.csv`, 31 of 80 `proposition_identity` rows have at least one non-verbatim side and 23 have both - the reviewer is shown the analyst's own summary next to a link to the bill, which is the artifact the brief's evidence rule exists to prevent.

Most are honest analyst descriptions with pinpoint section cites, mislabeled rather than wrong.
One is not:

- `atoms.py` gives S1116 the excerpt "a person may bring a civil action ... doxing ... disclosure of personally identifying information with intent to harass".
  S1116 contains no "harass", no "civil action", no "personally identifying".
  Its operative clause is "may pursue a cause of action for doxing" and its intent element is intent to cause "stalking, physical harm to person, or serious property damage". "Intent to harass" is the comparator H1707's element.
  The row asks the reviewer to judge whether the two state the same smallest change, and the excerpt manufactures agreement on the exact axis where they differ.

Also flagged: H4356 attributed H1690's "an eviction record sealed under this section" where H4356 says "a court record"; H3003 and H4040 both attributed "separate collection categories", a phrase in neither bill nor in 2023 c.28 s.7 (both say "separate collection and tabulations").

This is the same failure class as the fanned-quote block removed in the cleanup pass, and it violates the rule written into `atoms.py` in response to it: a quote attributed to a bill must come from THAT bill's text.

Fix, in this order:
1. Add a verbatim assertion to `09_checks.py` over both `QUOTES` and the queue excerpts, with the tolerances above.
   This is the load-bearing change - it prevents recurrence.
2. Fix the S1116, H4356, H3003/H4040 entries against the actual texts.
   For S1116 let the difference SHOW; that is what the reviewer must weigh.
3. For the ~40 legitimate summaries, either replace them with real excerpts or move them to a separately labeled column so "verbatim" is true of what remains.
   Do not simply relax the word in the codebook - the brief asks for side-by-side excerpts.

### 6 (P2) "Every consolidated privacy vehicle died in Ways and Means"

False, and the memo refutes it four paragraphs earlier.
Nine census bills are consolidation redrafts with two or more `redraft_of` parents; H4115 (8 parents) became 2024 c.118 and H4450 (5 parents) became 2024 c.399 - the memo's own enacted items 1 and 4.
H4266 and H4356 never went to Ways and Means at all.
Git history shows the sentence originally carried an "except H4744" carve-out that was removed while later passes admitted the NDII and school-bus lineages.

Fix: scope the sentence to the two omnibus consumer-privacy consolidations (H4632, S2539) and name the counterexamples.
Add a 09 check over the `redraft_of` fan-in against `terminal_class`.

### 7 (P2) H3524 is accounted for nowhere

Absent from `census.csv`, `corpus_scan.csv` and `scripts/corpus_triage_verdicts.csv`, though present in `documents_193.json`.
Its entire 840-character text is two disclosure restrictions: no municipality may publish "the name, or other individually identifying information, of a veteran still owing a tax", and c.62C s.21 is amended so "the name and address of a veteran shall not be published as part of said list".
That is verbatim the codebook's included subdomain "restrictions on disclosure of personal information held in government records" - the same mechanism as S194, which is included as P-254.
It cannot be a program-incident exclusion; the nondisclosure rule is the bill's only content.

Cause: `record_nondisclosure`'s passive alternation lists "disclosed|made public" but not "published", and `personal_information` does not cover "individually identifying".
The auditors swept 14 other unscanned nondisclosure filings and found them all correctly out, so this is one filing rather than a class - but prior passes treated structurally identical misses as defects to fix (fifth pass admitted H1939; sixth admitted S1136/S1503), so consistency requires fixing it.

Fix: add "published|released" to the passive alternation and "individually identif(ying|iable) information" to `personal_information`, rerun 01b and 04, adjudicate whatever new hits surface (04 fails until every hit has a verdict), and atomize H3524.
Expect 143 in-domain filings and a new proposition; every headline regenerates.
Widening terms cascades - budget time for the new triage verdicts.

### 8 (P3) S2604's terminal record contradicts its citation

`actions.SUCCESSOR_PATTERNS` recognizes "Accompanied a new draft, see X" and "Accompanied a study order, see X" but not the bare "Accompanied X".
S2604's history ends "2024-07-22 Accompanied H4193" with no "No further action taken" anywhere, but `bill_status` initializes `terminal = "died_no_further_action"` and nothing overrides it, so the fate detail says "ended with no further action" while `fate_citation` points at a page whose last action says otherwise.
`codebook.md` defines that class as "history ends in 'No further action taken'", so the default violates the project's own definition.

Separately, `bill_propositions.csv` for (S2604, P-335) records "clause dropped from enacted 2024 c.197 s.17" while `proposition_fates.csv` sets `dropped_in_consolidation = no`.
The drop is real: 2024 c.197 contains zero occurrences of "minimize the likelihood", "inadvertent" or "personal identifying information".

Fix: add an anchored `^Accompanied ([HS]\d+)$` pattern with a fixture in `actions.py` (it cannot collide with the two existing forms), fetch H4193's history, and either make `bill_status` emit `indeterminate` on an unmatched terminal or state the default in the codebook.
Expect "47 dropped during official consolidations" to become 48 - a number `09_checks.py` asserts.

### 9 (P3) P-213 bundles four severable ALPR duties

H3404's proposed c.90K s.2 is a shared-stem prohibition list: (a) no tracking of constitutionally protected activity, (b) no retention beyond 14 days, (c) no disclosure/sale/access except in a judicial proceeding, (d) no access to others' ALPR data without a warrant.
All four are one P-213, whose description names only (a), (b) and (d) and whose slug names only (b).
The identically-formed list in H4844 s.2(b)(i)-(v) was split into P-281..P-285 by the second pass, and `memo/atomization/family-driver-commercial.md` annotates this very section "four prongs, one section; splittable".

The verifier refuted the larger impact claims: the mechanism is not missing (P-196 covers it and a kinship link exists) and the rate still rounds to 5.5%.
What remains real: a machine-readable description that misstates the content it is cited against, three uncounted duties, and a missing H3404 -> P-196 identity edge that would move P-196's furthest_stage from "heard" to "reported_favorably".

### Minor but confirmed (full detail in review-eighth-pass.md)

- `04_inclusion.py` skips corpus-screen evidence for any bill already in `text_scan.csv`, and `02_textscan.py` never falls back to recovered PDF text.
  Seven candidates have zero API characters and were decided on zero evidence; H4578 has a live corpus hit discarded with no triage verdict, so the "04 fails if any corpus hit lacks a verdict" guarantee is false on that path.
  H4844 is in the census only because of a hand-written OVERRIDE that this same hole would otherwise have excluded.
- `ADJUDICATIONS[(2024,"135")]` covers one of the two families the scan flags; the c.123 s.12 restraint-record sole-use limit has no verdict.
  `09_checks.py` asserts chapter-level coverage only, so "every flagged chapter adjudicated provision-by-provision" is false. 2024 c.252 has the same shape.
- Eight `census.csv` rows (H58, H4040, H5077, H4799, H3306, H3440, S1136, S1503) carry hand-written prose in `title` instead of the official title, while 18 of 26 ADDITIONS rows carry the official title - a slip, not a convention.
- The determinism check reruns seven scripts but not `02_textscan.py` or `05_histories.py`, so `text_scan.csv` and `histories.json` are never re-derived.
  A verifier got a fabricated roll call into `bill_fates.csv` with the suite green.
  The codebook's sixth-pass claim that the check "was extended to every generated output" is inaccurate.
  Both rerun offline in under a second.
- `07_links.py`'s ad-hoc reported-out regex matches only the rarer of the two forms, leaving H4675's `reported_out` blank when 05c had already fetched the answer, which makes the codebook's "relevance recorded" claim false.

## What the auditors verified as SOUND

Do not re-litigate these; they were checked hard and held.

- The enacted universe is complete and corroborated three ways, including approval-date monotonicity across all 497 chapters and a sweep with ~25 domain constructions deliberately outside `TEXT_TERMS` (six hits, all false positives).
  All 33 API-omitted chapters re-extracted from raw HTML start at the preamble and end at the approval line.
- Filed-universe arithmetic is exact: 8,183 numbered filings, 8,178 screened, and the five unscanned are genuinely unrecoverable (two HTTP 500 + PDF 404, three image-only PDFs yielding zero characters from both pypdf and pdftotext).
- All 675 identity-basis labels recomputed from cached texts and histories with ZERO mismatches.
  All 60 similarity links reproduce their Jaccard to three decimals.
  All 198 quoted strings in the atomization memos verify.
  Every section cite in all 675 edges resolves.
- Proposition ID discipline is clean: 289 live, 17 retired, empty intersection, and a replay of all ten committed versions of `propositions.csv` shows the 71 unallocated IDs were never allocated.
- The multi-vehicle fate chains hold; the dual-vehicle claim for P-301/P-302 through c.363 and c.399 is correct; the H4799/S2891 cycle is handled.
- Neutrality is absolute: a motive/blame/intent regex over all 289 detail strings returns zero hits; all 273 died propositions carry "no public explanation".
- The HEADLINES block is stronger than it looks: mutating all 201 numeric tokens in `findings.md` one at a time produced a failure for every token a pattern covers, with no coincidental matches and no silent non-matches.

## Conventions and gotchas (hard-won; do not relearn)

- Politeness: fetchlib throttles 2.5s; cache everything; never refetch; `FETCHLIB_OFFLINE=1` makes cache misses fatal - final verification depends on it.
  `fetchlib.status()` reports a recorded HTTP status without raising; `fetchlib.get()` still returns a cached non-200 body as content, so use `status()` when "does this exist" matters.
- All CSV writers go through `csvutil` (LF); normalize whitespace in any text written to CSVs.
- Judgment calls live as data-in-scripts: census OVERRIDES/ADDITIONS/TRIAGE verdicts, atoms PROPS/EDGES/QUOTES/RETIRED, 08 ADJUDICATIONS.
  Never hand-edit generated `data/` files.
- Proposition IDs are persistent; retired IDs stay retired.
  Next free is P-378.
- Every inferred-analytic identity edge needs a QUOTES entry for the bill AND a comparator carrier, or 09 fails.
- The term scan lives in ONE place: `02_textscan.scan_terms()`, shared by 02, 01b, 03 and 03b.
  Do not add a fifth copy.
- The session-law universe lives in `sessionlaws.py`; `adj_key`/`split_key` own the Acts/Resolves key convention.
  Do not decode the "R" prefix by hand.
- `scripts/actions.py` is the ONLY action parser; extend it with fixtures in its self-test rather than adding regex elsewhere.
- The program-incident rule is applied symmetrically; the H3735/c.221 call is intentionally contested-and-queued - do not reopen it silently.
- Markdown prose uses semantic line breaks; reflow with `python3 ~/.claude/scripts/reflow-md.py FILE`.
- `memo/findings.md` is a clean current-state snapshot - no revision narration; history belongs in the codebook revision log (dated) and the PR thread.

## Verification recipe (must pass before pushing)

cd pilots/privacy-193rd/scripts && python3 actions.py && python3 sessionlaws.py && python3 09_checks.py
    # clean-archive, fully offline, byte-identical:
T=$(mktemp -d) && git archive HEAD | tar -x -C "$T" \ && cd "$T/pilots/privacy-193rd/scripts" \ && FETCHLIB_OFFLINE=1 sh -c 'python3 01_census.py && python3 02_textscan.py \ && python3 03b_acts_index.py && python3 03_sessionlaws.py \ && python3 01b_full_corpus_screen.py && python3 04_inclusion.py \ && python3 05_histories.py && python3 05c_link_targets.py \ && python3 06_compile_atoms.py && python3 07_links.py \ && python3 08_fates.py && python3 09_checks.py' \ && diff -rq "$T/pilots/privacy-193rd/data" <repo>/pilots/privacy-193rd/data

## Suggested order of work

1. Findings 2, 5, 6 and 8 first: no cascade beyond regeneration, and 5's check is the one that prevents recurrence of the worst failure class.
2. Then finding 1 (regenerates stage counts).
3. Then decide finding 3 explicitly and write the decision into the codebook.
4. Then findings 4 and 7 together, since both regenerate the headline.
5. Finding 9 last.

## Wrap-up steps

1. Commit with clear messages (signed; Co-Authored-By trailer per local convention), push to `pilot/privacy-193rd`.
2. Update the PR #1 body wholesale to the final numbers.
3. Post a response comment on PR #1 covering these findings, noting that this pass was self-review rather than external, and ending with the standard Claude Code attribution line.
4. Update the codebook revision log with a dated eighth-pass entry.
