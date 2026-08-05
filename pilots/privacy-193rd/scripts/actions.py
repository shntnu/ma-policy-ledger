"""Single shared parser for official bill-history actions.

Used by 06 (identity lineage), 07 (link graph), and 08 (terminal classes,
successor chains) so every consumer sees the same vocabulary
(fourth-pass review finding 6).
"""

import re

# (pattern, link_type) - forward pointers from a bill to its successor
SUCCESSOR_PATTERNS = [
    (r"Accompanied a new draft, see ([HS]\d+)", "superseded_by"),
    (r"New draft substituted, see ([HS]\d+)", "superseded_by"),
    (r"Reprinted as amended, see ([HS]\d+)", "superseded_by"),
    (r"Substituted (?:as a new text )?for ([HS]\d+)", "substituted_for"),
    (r"Reported \(in part\) by ([HS]\d+)", "reported_in_part_by"),
    (r"Reported by ([HS]\d+)", "reported_by"),
    (r"^See ([HS]\d+)$", "see"),
]
# backward pointers (successor names its parents)
PARENT_PATTERNS = [
    (r"New draft of (.+)", "redraft_of"),
    (r"Reported on a part of ([HS]\d+)", "reported_from_part_of"),
    (r"Reported on ([HS]\d+)", "reported_on"),
    (r"new text of (.+)", "new_text_of"),
    (r"inserting in place thereof the text of ([HS]\d+)", "text_adopted_from"),
]
STUDY_PATTERN = r"Accompanied a study order, see ([HS]\d+)"


def successor_of(action: str):
    """Return (successor_bill, link_type) or None."""
    act = action.strip()
    for pat, typ in SUCCESSOR_PATTERNS:
        m = re.search(pat, act)
        if m:
            return m.group(1), typ
    return None


def parents_of(action: str):
    """Return (list_of_parent_bills, link_type) or None."""
    act = action.strip()
    for pat, typ in PARENT_PATTERNS:
        m = re.search(pat, act)
        if m:
            return re.findall(r"[HS]\d+", m.group(1)), typ
    return None


def study_order_of(action: str):
    m = re.search(STUDY_PATTERN, action.strip())
    return m.group(1) if m else None


def successor_map(histories: dict) -> dict:
    """bill -> successor bill, from all successor patterns, sorted iteration."""
    out = {}
    for bn in sorted(histories):
        for a in histories[bn]["actions"]:
            s = successor_of(a["Action"])
            if s:
                out[bn] = s[0]
    return out


def lineage_pairs(histories: dict) -> set:
    """Unordered official-lineage pairs from successor AND parent records."""
    pairs = set()
    for bn in sorted(histories):
        for a in histories[bn]["actions"]:
            s = successor_of(a["Action"])
            if s:
                pairs.add(frozenset((bn, s[0])))
            p = parents_of(a["Action"])
            if p:
                for parent in p[0]:
                    pairs.add(frozenset((bn, parent)))
    return pairs
