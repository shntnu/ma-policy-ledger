"""Shared text-similarity helpers for cross-bill comparisons.

Used by 06_compile_atoms.py (identity basis of shared-proposition claims)
and 07_links.py (text-identity links). Reads only cached official texts.
"""

import hashlib
import json
import re
from pathlib import Path

PILOT = Path(__file__).resolve().parent.parent
API = "https://malegislature.gov/api"


def bill_text(bn: str) -> str:
    url = f"{API}/GeneralCourts/193/Documents/{bn}"
    p = PILOT / "raw" / "cache" / (hashlib.sha1(url.encode()).hexdigest() + ".bin")
    doc = json.loads(p.read_text(encoding="utf-8-sig"))
    t = re.sub(r"<[^>]+>", " ", doc.get("DocumentText") or "")
    return re.sub(r"\s+", " ", t).lower()


def shingles(text: str, k: int = 8) -> set:
    words = re.findall(r"[a-z0-9]+", text)
    return {" ".join(words[i : i + k]) for i in range(max(1, len(words) - k + 1))}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)
