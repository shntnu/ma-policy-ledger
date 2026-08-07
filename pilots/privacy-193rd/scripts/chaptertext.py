#!/usr/bin/env python3
"""Print the official text of a session law: `chaptertext.py 2024 399`.
Add `Resolves` for the resolve series: `chaptertext.py 2024 1 Resolves`.

Reads through sessionlaws.py, so it sees the whole official universe rather
than the /api/SessionLaws feed, which omits 33 of 2024's 407 Acts chapters -
including c.399, the in-domain one. Reads only the fetchlib cache.
"""

import sys

import sessionlaws

if len(sys.argv) < 3:
    raise SystemExit(__doc__)
year, ch = int(sys.argv[1]), sys.argv[2]
series = sys.argv[3] if len(sys.argv) > 3 else "Acts"

known = {(r["year"], r["series"], r["chapter"]) for r in sessionlaws.official_index()}
if (year, series, ch) not in known:
    raise SystemExit(
        f"{series} {year} c.{ch} is not in the official index "
        f"({sessionlaws.index_url(series, year)})")

rec = sessionlaws.chapter(year, ch, series)
if not rec["text"]:
    raise SystemExit(f"{rec['url']}: {rec['problem']}")
print(f"===== {series} {year} c.{ch} ({rec['source']}) =====")
print(rec["title"])
print(rec["url"])
print()
print(rec["text"])
