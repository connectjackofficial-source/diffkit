"""Three-way line merge on top of the LCS diff.

Takes a common base and two edited versions (ours/theirs) and produces
a merged text. When both sides edit the same base lines differently,
git-style conflict markers are emitted:

    <<<<<<< ours
    ...
    =======
    ...
    >>>>>>> theirs

Resolution is left to the caller; the markers make the ambiguity
explicit instead of silently picking a side.
"""
from __future__ import annotations

from .lcs import diff_lines


def _side_map(base: list, edited: list) -> dict:
    """Map each base line index to its replacement in *edited*.

    Returns {base_index: [output_lines]}; base_index -1 holds lines
    appended after the end of the base.
    """
    mapping: dict = {}
    ctx = -1
    mapping.setdefault(ctx, [])
    for op in diff_lines(base, edited):
        if op["op"] == "eq":
            ctx = op["old"]
            mapping.setdefault(ctx, [])
            mapping[ctx].append(op["line"])
        elif op["op"] == "del":
            ctx = op["old"]
            mapping.setdefault(ctx, [])
            mapping[ctx] = []  # base line removed on this side
        else:  # add: belongs to the current context line
            mapping[ctx].append(op["line"])
    return mapping


_MARKER_OURS = "<<<<<<< ours"
_MARKER_SEP = "======="
_MARKER_THEIRS = ">>>>>>> theirs"


def merge_3way(base: str, ours: str, theirs: str,
               conflict_markers: bool = True) -> str:
    """Merge *ours* and *theirs* against *base*.

    Lines both sides kept are kept; a change on one side is taken;
    conflicting changes produce conflict markers (or, with
    conflict_markers=False, raise MergeConflict on the first one).
    """
    base_l = base.splitlines()
    ours_map = _side_map(base_l, ours.splitlines())
    theirs_map = _side_map(base_l, theirs.splitlines())

    def _unchanged(side_lines: list, base_idx: int) -> bool:
        # a side "didn't touch" this base line when its replacement is
        # exactly the original line (or it has no replacement at all)
        return side_lines == [base_l[base_idx]] if base_idx >= 0 \
            else side_lines == []

    out: list[str] = []
    conflicts = 0
    for i in sorted(set(ours_map) | set(theirs_map)):
        om = ours_map.get(i, [])
        tm = theirs_map.get(i, [])
        if om == tm:
            out.extend(om)
        elif _unchanged(om, i):
            out.extend(tm)      # ours untouched -> take theirs
        elif _unchanged(tm, i):
            out.extend(om)      # theirs untouched -> take ours
        elif om and tm:
            conflicts += 1
            if not conflict_markers:
                raise MergeConflict(f"conflict at base line {i}")
            out.append(_MARKER_OURS)
            out.extend(om)
            out.append(_MARKER_SEP)
            out.extend(tm)
            out.append(_MARKER_THEIRS)
        else:
            out.extend(om or tm)
    return "\n".join(out) + ("\n" if base_l else "")


class MergeConflict(Exception):
    """Raised by merge_3way(conflict_markers=False) on a conflict."""


def has_conflicts(merged: str) -> bool:
    """True if the merged text still contains conflict markers."""
    return _MARKER_OURS in merged
