#!/bin/sh
# Reproduce every generated table from the committed raw/ cache.
# From a clean checkout, no network access is required (all sources cached);
# if the cache were empty, the same order performs the throttled fetching.
set -e
cd "$(dirname "$0")"
python3 01_census.py            # candidate nets (titles, committees)
python3 02_textscan.py          # full-text confirmation of net candidates
python3 02b_fetch_all_texts.py  # full corpus texts (cache no-op when present)
./02c_recover_empty_texts.py    # PDF recovery for empty API texts (uv+pypdf)
python3 03b_acts_index.py       # official Acts/Resolves index -> enacted universe
python3 03_sessionlaws.py       # enacted-chapter scan over that universe
python3 01b_full_corpus_screen.py  # full-corpus screen (stable inputs)
python3 04_inclusion.py         # census from nets + screen + verdict tables
python3 05_histories.py         # histories/similar-bills for included bills
./05b_h4844_text.py             # H4844 official PDF text (uv+pypdf)
python3 05c_link_targets.py     # study orders, redraft successors, lineages
python3 06_compile_atoms.py     # propositions + edges + identity bases
python3 07_links.py             # link graph + verification queue
python3 08_fates.py             # enacted adjudication + fates
python3 09_checks.py            # invariants + determinism
