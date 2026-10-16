"""diffkit: zero-dependency binary and text diff toolkit.

Line-level and byte-level diffs, unified patch parsing/applying, n-gram
similarity and whole-tree comparison — pure Python, no difflib shortcuts.
"""
from .lcs import diff_lines, diff_bytes

__version__ = "0.1.0"
__all__ = ["diff_lines", "diff_bytes"]
