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


def diff_lines_ws(old: list, new: list) -> list:
    """Line diff with whitespace normalization.

    Each line is compared after collapsing runs of internal whitespace
    to a single space (leading/trailing stripped). The reported line
    text is the original, so the output stays true to the input files.
    """
    def norm(s: str) -> str:
        return " ".join(s.split())

    a = [norm(s) for s in old]
    b = [norm(s) for s in new]
    dp = _lcs_table(a, b)
    ops = []
    i = j = 0
    m, n = len(a), len(b)
    while i < m and j < n:
        if a[i] == b[j]:
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


def _lcs_table(a: list, b: list):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = dp[i + 1][j + 1] + 1
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
    return dp


def diff_linear(old: list, new: list) -> list:
    """Linear-space LCS diff (Hirschberg divide-and-conquer).

    Same op schema and optimality as :func:`diff_lines` but only
    O(N+M) memory — the right tool for large files where the O(N*M)
    DP table of diff_lines would blow up. Ties may resolve to a
    different-but-equally-optimal edit script than diff_lines.
    """
    idx = set(_lcs_indices(old, new))
    ops = []
    i = j = 0
    n, m = len(old), len(new)
    while i < n or j < m:
        if i < n and i in idx:
            while j < m and new[j] != old[i]:
                ops.append({"op": "add", "line": new[j], "old": None,
                            "new": j})
                j += 1
            ops.append({"op": "eq", "line": old[i], "old": i, "new": j})
            i += 1
            j += 1
        elif i < n:
            ops.append({"op": "del", "line": old[i], "old": i, "new": None})
            i += 1
        else:
            ops.append({"op": "add", "line": new[j], "old": None, "new": j})
            j += 1
    return ops


def _lcs_rows(a: list, b: list) -> list:
    """Last row of the LCS DP table, computed with O(N) space."""
    n = len(b)
    prev = [0] * (n + 1)
    for ai in a:
        cur = [0] * (n + 1)
        for j in range(n):
            if ai == b[j]:
                cur[j + 1] = prev[j] + 1
            else:
                cur[j + 1] = max(prev[j + 1], cur[j])
        prev = cur
    return prev


def _lcs_indices(a: list, b: list) -> list:
    """Hirschberg: indices into *a* forming an LCS with *b*."""
    if not a or not b:
        return []
    m, n = len(a), len(b)
    if m == 1:
        return [0] if a[0] in b else []
    mid = m // 2
    left = _lcs_rows(a[:mid], b)
    right = _lcs_rows(list(reversed(a[mid:])), list(reversed(b)))
    best_k, best = 0, -1
    for k in range(n + 1):
        s = left[k] + right[n - k]
        if s > best:
            best = s
            best_k = k
    lo = _lcs_indices(a[:mid], b[:best_k])
    hi = [mid + x for x in _lcs_indices(a[mid:], b[best_k:])]
    return lo + hi


def diff_text(old_text: str, new_text: str) -> list:
    """Convenience wrapper: split strings into lines, diff them."""
    return diff_lines(old_text.splitlines(), new_text.splitlines())
