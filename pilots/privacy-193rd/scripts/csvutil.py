"""LF-only CSV writers so generated tables match git-stored bytes on any
platform (fourth-pass review finding 7)."""

import csv


def writer(f, **kw):
    kw.setdefault("lineterminator", "\n")
    return csv.writer(f, **kw)


def dict_writer(f, fieldnames, **kw):
    kw.setdefault("lineterminator", "\n")
    return csv.DictWriter(f, fieldnames=fieldnames, **kw)
