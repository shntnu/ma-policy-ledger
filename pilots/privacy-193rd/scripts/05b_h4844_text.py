#!/usr/bin/env python3
"""Recover the text of H4844, whose API DocumentText is empty.

The public BillText tab serves the House-reported text as HTML; cache it and
extract plain text to data/h4844_text.txt for atomization verification.
"""

import re
from pathlib import Path

import fetchlib

PILOT = Path(__file__).resolve().parent.parent


def main() -> None:
    html = fetchlib.get("https://malegislature.gov/Bills/193/H4844/BillText").decode(
        "utf-8", "replace"
    )
    m = re.search(r'(?s)<div[^>]*class="[^"]*modalTargetPrint[^"]*"[^>]*>(.*?)</div>\s*</div>', html)
    body = m.group(1) if m else html
    text = re.sub(r"<[^>]+>", " ", body)
    text = re.sub(r"&nbsp;?", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    # keep only from the first SECTION onward if identifiable
    i = text.find("SECTION 1")
    if i > 0:
        text = text[i:]
    (PILOT / "data" / "h4844_text.txt").write_text(text.strip())
    print(len(text), "chars;", text[:300])


if __name__ == "__main__":
    main()
