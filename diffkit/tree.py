"""Whole-directory comparison by relative path and content hash."""
from __future__ import annotations

import hashlib
from pathlib import Path


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _scan(root) -> dict:
    """Map relative POSIX paths to sha256 for every file under root."""
    out = {}
    for p in sorted(Path(root).rglob("*")):
        if p.is_file():
            out[p.relative_to(root).as_posix()] = _sha256(p)
    return out


def tree_diff(old_root, new_root) -> dict:
    """Compare two directory trees.

    Returns {"added": [...], "removed": [...], "modified": [...]} —
    relative paths only; content equality is decided by sha256.
    """
    a = _scan(old_root)
    b = _scan(new_root)
    added = sorted(set(b) - set(a))
    removed = sorted(set(a) - set(b))
    modified = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    return {"added": added, "removed": removed, "modified": modified}
