# Mission

This is the normalized restatement of the commissioning prompt that started the project; the verbatim original is in BRIEF.md.

You are conducting independent, nonpartisan measurement research on the Massachusetts legislature.
Reconstruct the complete fate of every distinct policy idea in ONE domain - consumer data privacy - for the 2023-2024 session (193rd General Court), the most recent completed session, so every outcome is final.
If an initial census shows this domain is too thin (under ~30 filings, no merger chains), choose a better domain of 50-150 bills and justify the switch.

## Goals, in order

1. Census: find every bill, resolve, and budget outside-section in the session touching the domain.
   Account for 100% of them.
2. Atomize: split each into distinct policy propositions - the smallest change in law that could stand alone.
   Give each proposition a persistent ID.
3. Link: build the graph connecting duplicates, House/Senate companions, refilings from prior sessions, successive redrafts, and provisions absorbed into omnibus or budget acts.
   Chase explicit links first (official bill-history pages record redrafts and consolidations), then propose implicit links via text comparison.
4. Classify every proposition's fate: enacted as filed / enacted through another vehicle / rejected by recorded vote / sent to study / died with no recorded action / indeterminate from the public record.
5. Answer the question: within this domain, does "the legislature passes almost nothing" survive when you count ideas instead of bills?
   Report the proposition-level passage rate, where ideas stall, and what share died with no recorded vote or explanation.

## Rules of evidence

- Primary sources only: malegislature.gov bill pages, histories, journals, session laws; Open States bulk data as backup.
  Cite an official URL for every factual claim.
- Mark every link and label with confidence: verified from explicit record, or inferred and needing human check.
  Queue all inferred links for review with side-by-side excerpts.
- Where the record is silent, write "no public explanation."
  Never infer motive, blame, or intent.
- Strict neutrality: no reference to any candidate, campaign, or election.
  This is measurement, not advocacy.

## Deliverables

1. Machine-readable dataset (CSV or JSON): propositions, bills, links, dispositions, citations.
2. A codebook documenting every definition and judgment call, precise enough that a second researcher could reproduce the classifications.
3. A verification queue of every uncertain link.
4. A findings memo, two pages max: the domain-level answer, honest limitations, and what it would take to scale this to all 8,000+ bills.

## Definition of done

A skeptical stranger can pick any proposition, click its citations, and confirm its entire story in under a minute.

## Working rules

- Cache every fetched page into /raw before parsing; never re-fetch.
  Throttle requests to malegislature.gov.
- Everything must be reproducible by re-running /scripts.
  No manual one-off data edits.
- Checkpoints: stop after Goal 1 (census) for review before atomizing, and stop again after Goal 3 (link graph) before classifying fates.
