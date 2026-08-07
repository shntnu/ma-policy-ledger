#!/usr/bin/env python3
"""Print the cached plain text of a bill: `python3 billtext.py H83 [S25 ...]`.

Reads only from the fetch cache; exits with an error if a bill is not cached
(nothing is fetched here, so this can never hit the network).
"""

import json
import re
import sys

import fetchlib

API = "https://malegislature.gov/api"


def plain_text(bill: str) -> str:
    url = f"{API}/GeneralCourts/193/Documents/{bill}"
    rec = fetchlib._index.get(url)
    if rec is None:
        raise SystemExit(f"{bill}: not in cache; run 02_textscan.py first")
    doc = json.loads((fetchlib.PILOT / rec["path"]).read_text(encoding="utf-8-sig"))
    text = re.sub(r"<[^>]+>", " ", doc.get("DocumentText") or "")
    return re.sub(r"[ \t]+", " ", text)


if __name__ == "__main__":
    for bn in sys.argv[1:]:
        print(f"===== {bn} =====")
        print(plain_text(bn))
