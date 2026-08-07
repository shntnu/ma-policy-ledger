# MA Policy Ledger

This repository is a measurement-research project on the Massachusetts General Court.
It tests whether the common claim that "the legislature passes almost nothing" survives when legislative output is counted at the level of distinct policy ideas rather than bill numbers.
The method is to take one policy domain in one completed session, enumerate every filing that touches it, split each filing into its smallest standalone policy propositions, link duplicates, companions, refilings, and redrafts into a graph, and then classify the final fate of every proposition from the official public record.
The whole exercise started from a single commissioning prompt, reproduced verbatim in BRIEF.md; MISSION.md is its normalized restatement, committed first to timestamp the approach before any data was collected.

The first pilot, in `pilots/privacy-193rd/`, covers consumer data privacy in the 2023-2024 session (193rd General Court), chosen because the session is complete and every outcome is final.
Each pilot directory contains `raw/` (cached copies of every source page fetched, so no page is ever re-fetched), `scripts/` (all collection and analysis code, sufficient to reproduce every output from scratch), `data/` (machine-readable propositions, links, dispositions, and citations), and `memo/` (the findings memo, codebook, and verification queue for human review of inferred links).
All factual claims cite official malegislature.gov URLs; where the record is silent the dataset says "no public explanation" rather than inferring intent.
