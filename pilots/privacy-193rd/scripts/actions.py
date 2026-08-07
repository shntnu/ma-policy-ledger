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
    (r"Reprinted,? as amended, see ([HS]\d+)", "superseded_by"),
    (r"Published as amended, see ([HS]\d+)", "superseded_by"),
    (r"Text of an amendment, see ([HS]\d+)", "amendment_stage_of"),
    (r"Substituted (?:as a new text )?for ([HS]\d+)", "substituted_for"),
    # "by" is optional: the two forms in this corpus are "Reported, in part,
    # by H3107" (H4675) and "Reported (in part) S2538" (S2612). 07_links.py
    # used to carry its own regex for the second one only, which left H4675's
    # reported_out cell blank (eighth-pass review).
    (r"Reported[,]? \(?in part\)?,? (?:by )?([HS]\d+)", "reported_in_part_by"),
    (r"Reported by ([HS]\d+)", "reported_by"),
    (r"^See ([HS]\d+)$", "see"),
    # Eighth-pass review finding 8: the bare form. S2604's history ends
    # "Accompanied H4193" and contains no "No further action taken", yet
    # bill_status defaulted it to died_no_further_action, so the fate detail
    # contradicted the last line of the page it cites. Anchored, so it cannot
    # swallow "Accompanied a new draft, see X" or "Accompanied a study order,
    # see X" - the only other two forms in this corpus.
    (r"^Accompanied ([HS]\d+)$", "accompanied"),
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


# Fixture tests over real action strings from the cached histories.
_FIXTURES = [
    ("Accompanied a new draft, see H4632", ("H4632", "superseded_by")),
    ("New draft substituted, see H4241", ("H4241", "superseded_by")),
    ("Reprinted as amended, see S2710", ("S2710", "superseded_by")),
    ("Reprinted, as amended, see S2891", ("S2891", "superseded_by")),
    ("Published as amended, see H58", ("H58", "superseded_by")),
    ("Text of an amendment, see H58", ("H58", "amendment_stage_of")),
    ("Text of an amendment, see S2884", ("S2884", "amendment_stage_of")),
    ("Substituted as a new text for H58", ("H58", "substituted_for")),
    ("Substituted for H4241", ("H4241", "substituted_for")),
    ("Reported (in part) by S2884", ("S2884", "reported_in_part_by")),
    ("Reported, in part, by H5077", ("H5077", "reported_in_part_by")),
    ("Reported, in part, by H3107", ("H3107", "reported_in_part_by")),
    ("Reported (in part) S2538", ("S2538", "reported_in_part_by")),
    ("See H58", ("H58", "see")),
    ("Reported by H4744", ("H4744", "reported_by")),
    ("Accompanied H4193", ("H4193", "accompanied")),
    # the anchor must keep the two longer forms on their own patterns
    ("Accompanied a new draft, see H4632", ("H4632", "superseded_by")),
    ("Accompanied a study order, see H4517", None),
]


def self_test() -> None:
    for act, expected in _FIXTURES:
        got = successor_of(act)
        assert got == expected, f"{act!r}: expected {expected}, got {got}"
    assert parents_of("New draft of S26, S30 and H76") == (["S26", "S30", "H76"], "redraft_of")
    assert parents_of("Reported on a part of H4496") == (["H4496"], "reported_from_part_of")
    assert parents_of("Amended by striking out all after the enacting clause and inserting in place thereof the text of S2888") == (["S2888"], "text_adopted_from")
    assert study_order_of("Accompanied a study order, see H4517") == "H4517"


if __name__ == "__main__":
    self_test()
    print("actions.py fixtures pass")
