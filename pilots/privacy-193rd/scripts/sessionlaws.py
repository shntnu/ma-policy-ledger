"""The complete official enacted universe for the 193rd General Court.

`/api/SessionLaws/{year}` is NOT the enacted universe. For 2024 it returns 375
rows covering 374 Acts chapters plus 1 Resolve, while the official year index
(https://malegislature.gov/Laws/SessionLaws/Acts/2024) lists Acts chapters 1
through 407 with no gaps - 33 chapters missing from the feed, among them
Chapter 399, which is in-domain and was found only through H4940's history
(seventh-pass review finding 1). 2023 has no such defect (index and feed both
list Acts 1-89) and has no Resolves index at all.

This module enumerates the universe from the official year indexes and
supplies each chapter's official text, preferring the API's ChapterText where
the feed carries it and falling back to the official chapter page otherwise.
Chapter-page extraction is validated against the API text of 2024 c.363 in the
self-test below: the act body is word-identical, so the two sources are
interchangeable for scanning.

Every consumer of the enacted side (03_sessionlaws.py's term scan,
03b_acts_index.py's coverage record, 08_fates.py's signature probe) reads the
universe from here, so the numerator and the recall guarantee rest on the same
enumerated set.
"""

import html as _html
import re

import fetchlib

API = "https://malegislature.gov/api"
SITE = "https://malegislature.gov"
YEARS = (2023, 2024)
SERIES = ("Acts", "Resolves")


def index_url(series: str, year: int) -> str:
    return f"{SITE}/Laws/SessionLaws/{series}/{year}"


def chapter_url(series: str, year: int, chapter: str) -> str:
    return f"{SITE}/Laws/SessionLaws/{series}/{year}/Chapter{chapter}"


def adj_key(series: str, chapter: str) -> str:
    """Adjudication/scan key for a chapter. Acts keep the bare number (the
    established key in 08_fates.ADJUDICATIONS); Resolves are prefixed "R" so
    an Acts chapter and a Resolve of the same number can never collide."""
    return chapter if series == "Acts" else "R" + chapter


def official_index() -> list[dict]:
    """Every chapter the official year indexes list, as
    {year, series, chapter, url}. A series with no index page for a year
    (2023 Resolves returns 404) contributes nothing and is recorded by
    03b_acts_index.py as absent."""
    out = []
    for year in YEARS:
        for series in SERIES:
            body = _index_body(series, year)
            if body is None:
                continue
            rx = rf"/Laws/SessionLaws/{series}/{year}/Chapter(\d+)"
            for ch in sorted({int(m) for m in re.findall(rx, body)}):
                out.append({
                    "year": year, "series": series, "chapter": str(ch),
                    "url": chapter_url(series, year, str(ch)),
                })
    return out


def index_status() -> list[dict]:
    """One row per (year, series) saying whether the official index exists."""
    out = []
    for year in YEARS:
        for series in SERIES:
            body = _index_body(series, year)
            out.append({
                "year": year, "series": series,
                "present": "yes" if body is not None else "no",
                "url": index_url(series, year),
            })
    return out


def _index_body(series: str, year: int):
    """The official index page, or None when the series has no chapters that
    year (2023 has no Resolves, and that page 404s). Any other non-200 is a
    real failure and must not be swallowed."""
    url = index_url(series, year)
    st = fetchlib.status(url)
    if st == 404:
        return None
    if st != 200:
        raise RuntimeError(f"HTTP {st} for {url}")
    return fetchlib.get(url).decode("utf-8", "replace")


def _api_rows() -> dict:
    from pathlib import Path
    fetchlib.seed(
        f"{API}/SessionLaws/2023",
        Path(__file__).resolve().parent.parent / "raw" / "probe" / "api_sessionlaws_2023.json",
    )
    rows = {}
    for year in YEARS:
        for law in fetchlib.get_json(f"{API}/SessionLaws/{year}"):
            series = law.get("Type") or "Acts"
            rows[(year, series, law["ChapterNumber"])] = law
    return rows


def _strip(markup: str) -> str:
    txt = re.sub(r"(?s)<script.*?</script>", " ", markup)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = _html.unescape(txt)
    return re.sub(r"\s+", " ", txt).strip()


def page_parts(body: str) -> tuple[str, str]:
    """(title, act text) from an official session-law chapter page. The body
    is the block between the chapterTitle heading and the sidebar column."""
    i = body.find('class="h3 chapterTitle"')
    if i < 0:
        return "", ""
    head_end = body.find("</h2>", i)
    title = _strip(body[body.find(">", i) + 1:head_end])
    j = body.find('<div class="col-xs-12 col-md-4', head_end)
    if j < 0:
        j = len(body)
    return title, _strip(body[head_end + 5:j])


def universe() -> list[dict]:
    """Every officially indexed chapter with its official text.

    Each record: year, series, chapter, key, title, origin_bill, text,
    source ("api" or "chapter_page"), url. `text` is "" only when the
    chapter page could not be parsed, which 09_checks.py treats as a
    coverage failure unless a reason is recorded."""
    api = _api_rows()
    out = []
    for rec in official_index():
        year, series, ch = rec["year"], rec["series"], rec["chapter"]
        law = api.get((year, series, ch))
        if law is not None:
            text = _strip(law.get("ChapterText") or "")
            title = (law.get("Title") or "").strip()
            origin = (law.get("OriginBill") or {}) if isinstance(law.get("OriginBill"), dict) else {}
            source = "api"
        else:
            body = fetchlib.get(rec["url"]).decode("utf-8", "replace")
            title, text = page_parts(body)
            origin = {}
            source = "chapter_page"
        out.append({
            "year": year, "series": series, "chapter": ch,
            "key": adj_key(series, ch),
            "title": re.sub(r"\s+", " ", title).strip(),
            "origin_bill": (origin.get("BillNumber") or "") if origin else "",
            "text": text, "source": source, "url": rec["url"],
        })
    return out


def _selftest() -> None:
    """Chapter-page extraction must reproduce the API's act text. 2024 c.363
    is in both sources, so it is the fixture."""
    law = _api_rows()[(2024, "Acts", "363")]
    api_words = re.findall(r"[a-z0-9]+", _strip(law["ChapterText"]).lower())
    body = fetchlib.get(chapter_url("Acts", 2024, "363")).decode("utf-8", "replace")
    _, page = page_parts(body)
    page_words = re.findall(r"[a-z0-9]+", page.lower())
    assert api_words == page_words, (
        f"chapter-page extraction diverges from the API text for 2024 c.363: "
        f"{len(api_words)} vs {len(page_words)} words")
    idx = official_index()
    assert sum(1 for r in idx if r["year"] == 2023 and r["series"] == "Acts") == 89
    assert sum(1 for r in idx if r["year"] == 2024 and r["series"] == "Acts") == 407
    print(f"sessionlaws self-test ok: {len(idx)} officially indexed chapters; "
          "chapter-page extraction is word-identical to the API text (2024 c.363)")


if __name__ == "__main__":
    _selftest()
