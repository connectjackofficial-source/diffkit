"""Character n-gram similarity (Jaccard of n-gram sets).

Useful for fuzzy de-duplication of strings, "how close are these two
snippets" questions and heuristic malware-config matching. Pure Python,
works on any text without language-specific tokenizers.
"""
from __future__ import annotations


def ngram_similarity(a: str, b: str, n: int = 3) -> float:
    """Jaccard similarity of the character n-gram sets of a and b.

    Returns 1.0 when both inputs are empty, 0.0 when one is empty,
    otherwise |G(a) & G(b)| / |G(a) | G(b)| in [0.0, 1.0].
    """
    if n <= 0:
        raise ValueError("n must be >= 1")

    def grams(s: str) -> set:
        return {s[i:i + n] for i in range(max(0, len(s) - n + 1))}

    ga, gb = grams(a), grams(b)
    if not ga and not gb:
        return 1.0
    if not ga or not gb:
        return 0.0
    return len(ga & gb) / len(ga | gb)
