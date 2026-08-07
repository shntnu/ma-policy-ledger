#!/usr/bin/env -S uv run --with pypdf python3
"""Recover the text of H4844, whose API DocumentText is empty.

Reads the official PDF (cached by fetchlib; the BillText HTML tab serves
only page chrome for this bill) and extracts plain text deterministically
to data/h4844_text.txt. Review finding 5: an earlier version of this script
read the HTML shell and would have overwritten the good text on a rerun.
"""

import io
import re
from pathlib import Path

from pypdf import PdfReader

import fetchlib

PILOT = Path(__file__).resolve().parent.parent


def main() -> None:
    pdf = fetchlib.get("https://malegislature.gov/Bills/193/H4844.pdf")
    reader = PdfReader(io.BytesIO(pdf))
    pages = [p.extract_text() or "" for p in reader.pages]
    text = "\n".join(pages)
    text = re.sub(r"[ \t]+", " ", text)
    if "SECTION 1" not in text or "93M" not in text:
        raise SystemExit("H4844 PDF extraction failed sanity check")
    (PILOT / "data" / "h4844_text.txt").write_text(text.strip() + "\n")
    print(f"wrote data/h4844_text.txt ({len(text)} chars, {len(pages)} pages)")


if __name__ == "__main__":
    main()
