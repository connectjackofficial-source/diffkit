"""diffkit: zero-dependency binary and text diff toolkit.

Line-level and byte-level diffs, unified patch parsing/applying, n-gram
similarity and whole-tree comparison — pure Python, no difflib shortcuts.
"""
from .lcs import diff_lines, diff_bytes
from .unified import parse_unified, apply_patch
from .similarity import ngram_similarity
from .tree import tree_diff
from .hexdump import hexdump

__version__ = "0.1.0"
__all__ = ["diff_lines", "diff_bytes", "parse_unified", "apply_patch",
           "ngram_similarity", "tree_diff", "hexdump"]
