"""Single shared test for "is this excerpt verbatim from that bill's text?"

Eighth-pass review finding 5. `memo/codebook.md` and `memo/findings.md` both
promise the verification queue shows VERBATIM side-by-side excerpts from the
official texts, and `scripts/atoms.py` labels its QUOTES table the same way.
Nothing enforced it: 58 of 155 QUOTES entries were analyst descriptions, and
one (S1116) asserted a legal element the bill does not contain. The check
lives here so `09_checks.py` and any future consumer share one definition.

The matcher is deliberately generous - it must never fail a quote that IS in
the text, because a false alarm would push an author toward paraphrase:

  - case- and punctuation-insensitive (curly quotes, commas, hyphens)
  - " ... " splits a quote into fragments, each of which must occur; this is
    how an author elides intervening words
  - standalone digit tokens are dropped from both sides, so the line numbers
    interleaved through recovered PDF text ("the 182 vehicle") cannot cause a
    false negative
  - a trailing pinpoint cite - "(s.8(c))", "(SECTION 30)", "(2024 c.206 s.15)"
    - is stripped before matching; it locates the quote rather than quoting

What it does NOT tolerate is a fragment that simply is not there. Reads only
cached official texts through textsim.full_text, so it runs offline.
"""

import re

import textsim

# a trailing parenthetical that locates rather than quotes
# one level of nesting, because pinpoint cites look like "(s.8(c))"
_TRAILING_CITE = re.compile(
    r"\s*\((?:SECTION|SS\.|s\.|ss\.|new\s|c\.|ch\.|\d{4}\s+c\.)"
    r"(?:[^()]|\([^()]*\))*\)\s*$",
    re.IGNORECASE,
)


def normalize(s: str) -> str:
    """Lowercase word tokens, digits dropped, space-delimited and -padded."""
    toks = [t for t in re.findall(r"[a-z0-9]+", s.lower()) if not t.isdigit()]
    return " " + " ".join(toks) + " "


def fragments(quote: str) -> list:
    """Quote -> the fragments that must each occur, cite stripped."""
    prev = None
    while prev != quote:
        prev = quote
        quote = _TRAILING_CITE.sub("", quote).strip()
    parts = re.split(r"\s*\.\.\.\s*", quote)
    return [p for p in (x.strip() for x in parts) if normalize(p).strip()]


_TEXT_CACHE = {}


def bill_text(bill: str):
    """Normalized best-available official text, or None if there is none."""
    if bill not in _TEXT_CACHE:
        t = textsim.full_text(bill)
        _TEXT_CACHE[bill] = normalize(t) if t else None
    return _TEXT_CACHE[bill]


def missing_fragments(bill: str, quote: str) -> list:
    """Fragments of `quote` absent from `bill`'s text.

    Raises if the bill has no recoverable text at all: a quote can never be
    attributed to a document the repository cannot show, so that is a defect
    rather than a pass.
    """
    text = bill_text(bill)
    if text is None:
        raise ValueError(f"{bill}: no recoverable official text to quote from")
    return [f for f in fragments(quote) if normalize(f)[1:-1] not in text]


def is_verbatim(bill: str, quote: str) -> bool:
    return not missing_fragments(bill, quote)


_FIXTURES = [
    # real H3375 text, with an elision and a trailing pinpoint cite
    ("H3375", "photographs and other personal identifying information collected "
              "by a city or town pursuant to this chapter shall not be a public record", True),
    ("H3375", "shall only take photographs when a camera enforceable violation "
              "occurs ... destroyed not more than 48 hours after the final disposition", True),
    ("H3375", "photographs and other personal identifying information collected "
              "by a city or town pursuant to this chapter shall not be a public record (s.8(c))", True),
    # H5154's text is recovered PDF with line numbers interleaved through it
    ("H5154", "the enforcing authority shall redact the photograph to remove or "
              "obscure the vehicle operator, passengers or contents of the vehicle", True),
    # the failure the check exists to catch: an element S1116 does not contain
    ("S1116", "disclosure of personally identifying information with intent to harass", False),
    ("S1116", "may pursue a cause of action for doxing", True),
]


def self_test() -> None:
    for bill, quote, expected in _FIXTURES:
        got = is_verbatim(bill, quote)
        assert got is expected, (
            f"{bill}: expected verbatim={expected}, got {got}; "
            f"missing {missing_fragments(bill, quote)}"
        )


if __name__ == "__main__":
    self_test()
    print("verbatim.py fixtures pass")
