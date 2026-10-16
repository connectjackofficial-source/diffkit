"""Patch statistics: hunk counts and line-change tallies."""
from __future__ import annotations

from .unified import parse_unified


def patch_stats(patch_text: str) -> dict:
    """Summarize a unified patch.

    Returns {"hunks": int, "added": int, "removed": int,
    "context": int, "files": [old -> new]}.
    """
    parsed = parse_unified(patch_text)
    added = removed = context = 0
    for hunk in parsed["hunks"]:
        for op, _ in hunk["lines"]:
            if op == "+":
                added += 1
            elif op == "-":
                removed += 1
            else:
                context += 1
    files = []
    if parsed["old"] or parsed["new"]:
        files.append({"old": parsed["old"], "new": parsed["new"]})
    return {"hunks": len(parsed["hunks"]), "added": added,
            "removed": removed, "context": context, "files": files}
