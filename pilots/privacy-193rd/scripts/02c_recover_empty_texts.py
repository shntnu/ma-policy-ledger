#!/usr/bin/env -S uv run --with pypdf python3
"""Recover official text for every numbered bill whose API DocumentText is
empty (fourth-pass review finding 3): fetch the official PDF via the cache
and extract text to data/pdf_texts/BILL.txt. Bills with neither API text nor
a recoverable PDF are listed in data/unscanned_bills.csv.
"""

import io
import json
import re
from pathlib import Path

from pypdf import PdfReader

import csvutil
import fetchlib
import textsim

PILOT = Path(__file__).resolve().parent.parent
DATA = PILOT / "data"
OUT = DATA / "pdf_texts"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    docs = json.loads((DATA / "documents_193.json").read_text())
    bills = sorted({d["BillNumber"] for d in docs if d.get("BillNumber")})
    empty = [bn for bn in bills if len(textsim.bill_text(bn).strip()) < 50]
    print(f"{len(empty)} bills with empty API text")
    unrecovered = []
    for i, bn in enumerate(sorted(empty), 1):
        dest = OUT / (bn + ".txt")
        if dest.exists() and len(dest.read_text().strip()) >= 50:
            continue
        try:
            pdf = fetchlib.get(f"https://malegislature.gov/Bills/193/{bn}.pdf")
            reader = PdfReader(io.BytesIO(pdf))
            text = "\n".join((p.extract_text() or "") for p in reader.pages)
            text = re.sub(r"[ \t]+", " ", text).strip()
        except Exception as e:
            unrecovered.append((bn, str(e)[:80]))
            continue
        if len(text) < 50:
            unrecovered.append((bn, "PDF extracted to empty text"))
            continue
        dest.write_text(text + "\n")
        if i % 50 == 0:
            print(f"  {i}/{len(empty)}")
    with (DATA / "unscanned_bills.csv").open("w", newline="") as f:
        w = csvutil.writer(f)
        w.writerow(["bill", "reason"])
        for bn, why in unrecovered:
            w.writerow([bn, why])
    print(f"recovered {len(empty) - len(unrecovered)}; unrecovered {len(unrecovered)}")


if __name__ == "__main__":
    main()
