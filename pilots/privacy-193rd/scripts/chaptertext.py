#!/usr/bin/env python3
"""Print the cached plain text of a session law: chaptertext.py 2024 118.
Reads only the fetchlib cache; never hits the network."""

import re
import sys

import fetchlib

year, chapter = sys.argv[1], sys.argv[2]
laws = fetchlib.get_json(f"https://malegislature.gov/api/SessionLaws/{year}")
law = next(l for l in laws if l["ChapterNumber"] == chapter)
text = re.sub(r"<[^>]+>", " ", law.get("ChapterText") or "")
text = re.sub(r"&nbsp;?", " ", text)
print(re.sub(r"[ \t]+", " ", text))
