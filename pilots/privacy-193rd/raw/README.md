# raw/

Cached copies of every source page fetched from malegislature.gov.

- `probe/` - exploratory fetches made while discovering the site's API and
  search interface (bill search HTML, API endpoint tests).
  Where a probe fetched the same URL a script later needs, the script seeds
  the cache from the probe file so the URL is never fetched twice.
- `cache/` - the canonical cache used by `scripts/fetchlib.py`.
  Files are named by the SHA-1 of the source URL.
- `cache_index.jsonl` - one JSON record per cached URL: url, path, fetch
  timestamp (UTC), HTTP status, and `seeded_from` when the content came from
  a probe file.

Nothing in this directory is ever edited by hand; `cache/` and
`cache_index.jsonl` are written only by `fetchlib.py`.

Findings from probing (2026-08-04): malegislature.gov's site search
(`/Bills/Search`, `/Search`) only indexes the current (194th) General Court,
so the census of the 193rd is built from the JSON API instead:
`/api/GeneralCourts/193/Documents` (all filed documents),
`/api/GeneralCourts/193/Committees/{code}` (reported-out lists),
`/api/GeneralCourts/193/Documents/{bill}` (full text and history links), and
`/api/SessionLaws/{year}` (full text of every enacted chapter).
