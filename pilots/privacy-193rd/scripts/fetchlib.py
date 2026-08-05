"""Cached, throttled fetcher for malegislature.gov.

Every fetched page is cached under raw/cache/ keyed by the SHA-1 of the URL,
with a JSONL index (raw/cache_index.jsonl) recording url, path, timestamp, and
HTTP status. A URL is never fetched twice: if it is in the cache, the cached
bytes are returned. Network fetches are throttled to at least MIN_INTERVAL
seconds apart.

seed(url, path) registers an existing file (for example an exploratory probe
fetch) as the cached copy of a URL, so the same content is never re-downloaded.
"""

import hashlib
import json
import shutil
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PILOT = Path(__file__).resolve().parent.parent
CACHE = PILOT / "raw" / "cache"
INDEX = PILOT / "raw" / "cache_index.jsonl"
USER_AGENT = (
    "ma-policy-ledger research scraper (nonpartisan measurement research; "
    "contact: eklavyaa@gmail.com)"
)
MIN_INTERVAL = 2.5  # seconds between network requests
_last_fetch = [0.0]


def _key(url: str) -> str:
    return hashlib.sha1(url.encode()).hexdigest()


def _load_index() -> dict:
    idx = {}
    if INDEX.exists():
        with INDEX.open() as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    idx[rec["url"]] = rec
    return idx


def _append_index(rec: dict) -> None:
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    with INDEX.open("a") as f:
        f.write(json.dumps(rec) + "\n")


_index = _load_index()


def seed(url: str, path: str) -> None:
    """Register an existing file as the cached copy of url."""
    if url in _index:
        return
    src = Path(path)
    if not src.exists():
        raise FileNotFoundError(path)
    CACHE.mkdir(parents=True, exist_ok=True)
    dest = CACHE / (_key(url) + ".bin")
    shutil.copyfile(src, dest)
    rec = {
        "url": url,
        "path": str(dest.relative_to(PILOT)),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "status": 200,
        "seeded_from": str(src),
    }
    _append_index(rec)
    _index[url] = rec


def get(url: str, max_retries: int = 3) -> bytes:
    """Return the body for url, from cache if present, else fetch and cache.
    With FETCHLIB_OFFLINE=1 in the environment, a cache miss raises instead
    of fetching (used to assert committed-cache completeness)."""
    if url in _index:
        return (PILOT / _index[url]["path"]).read_bytes()
    import os
    if os.environ.get("FETCHLIB_OFFLINE"):
        raise RuntimeError(f"offline mode: {url} not in cache")
    CACHE.mkdir(parents=True, exist_ok=True)
    body = None
    status = None
    for attempt in range(max_retries):
        wait = MIN_INTERVAL - (time.time() - _last_fetch[0])
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            _last_fetch[0] = time.time()
            with urllib.request.urlopen(req, timeout=60) as resp:
                status = resp.status
                body = resp.read()
            break
        except urllib.error.HTTPError as e:
            status = e.code
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                time.sleep(10 * (attempt + 1))
                continue
            body = e.read()
            break
        except (urllib.error.URLError, TimeoutError):
            if attempt < max_retries - 1:
                time.sleep(10 * (attempt + 1))
                continue
            raise
    dest = CACHE / (_key(url) + ".bin")
    dest.write_bytes(body)
    rec = {
        "url": url,
        "path": str(dest.relative_to(PILOT)),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
    }
    _append_index(rec)
    _index[url] = rec
    if status != 200:
        raise RuntimeError(f"HTTP {status} for {url} (cached)")
    return body


def get_json(url: str):
    return json.loads(get(url).decode("utf-8-sig"))
