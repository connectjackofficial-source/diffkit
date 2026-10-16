"""Longest-common-subsequence diff: lines for text, blocks for bytes.

A readable LCS implementation (DP table + backtrack) — the classic
algorithm, no difflib shortcuts, so the tradeoffs are explicit: O(n*m)
memory, exact matches only, no fuzz.
"""
from __future__ import annotations


def diff_lines(old: list, new: list) -> list:
    """LCS line diff between two sequences.

    Returns [{"op": "eq"|"del"|"add", "line": str,
    "old": int|None, "new": int|None}] in forward order.
    """
    m, n = len(old), len(new)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if old[i] == new[j]:
                dp[i][j] = dp[i + 1][j + 1] + 1
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])

    ops = []
    i = j = 0
    while i < m and j < n:
        if old[i] == new[j]:
            ops.append({"op": "eq", "line": old[i], "old": i, "new": j})
            i += 1
            j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            ops.append({"op": "del", "line": old[i], "old": i, "new": None})
            i += 1
        else:
            ops.append({"op": "add", "line": new[j], "old": None, "new": j})
            j += 1
    while i < m:
        ops.append({"op": "del", "line": old[i], "old": i, "new": None})
        i += 1
    while j < n:
        ops.append({"op": "add", "line": new[j], "old": None, "new": j})
        j += 1
    return ops


def diff_bytes(old: bytes, new: bytes, block: int = 16) -> list:
    """Byte-level diff at fixed-block granularity.

    Binary files rarely line up line-by-line, so we diff fixed-size
    blocks (default 16 bytes) and report which blocks were inserted,
    removed or unchanged.
    """
    a = [old[i:i + block] for i in range(0, len(old), block)]
    b = [new[i:i + block] for i in range(0, len(new), block)]
    return diff_lines(a, b)


def diff_text(old_text: str, new_text: str) -> list:
    """Convenience wrapper: split strings into lines, diff them."""
    return diff_lines(old_text.splitlines(), new_text.splitlines())
