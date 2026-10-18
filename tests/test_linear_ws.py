"""Tests for diffkit diff_linear + whitespace-normalized diff.

diff_linear (Hirschberg) may pick a different-but-equally-optimal edit
script than diff_lines, so correctness is asserted mathematically:
the op script must replay to the new sequence, and its edit cost must
equal n + m - 2*LCS.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from diffkit.lcs import diff_lines, diff_linear, diff_lines_ws


def _lcs_len(a, b):
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
    return prev[n]


def _replay(old, ops):
    out = []
    for op in ops:
        if op["op"] == "eq" or op["op"] == "del":
            pass  # consumed from old by index
        if op["op"] in ("eq", "add"):
            out.append(op["line"])
    return out


def _check_optimal(old, new, ops):
    # replay gives new
    assert _replay(old, ops) == new, (old, new, ops)
    # edit cost is minimal
    cost = sum(1 for o in ops if o["op"] in ("del", "add"))
    assert cost == len(old) + len(new) - 2 * _lcs_len(old, new), \
        (old, new, cost)


def test_linear_simple():
    cases = [
        (["a", "b", "c"], ["a", "b", "c"]),
        (["a", "b"], ["a", "x", "b"]),
        ([], ["x", "y"]),
        (["x", "y"], []),
        (["one", "two"], ["one", "TWO", "three"]),
        (["a", "b"], ["b", "a"]),
    ]
    for old, new in cases:
        _check_optimal(old, new, diff_linear(old, new))
    print("test_linear_simple: ok")


def test_linear_random_optimal():
    rng = random.Random(7)
    pool = ["alpha", "beta", "gamma", "delta"]
    for _ in range(200):
        old = [rng.choice(pool) for _ in range(rng.randint(0, 12))]
        new = [rng.choice(pool) for _ in range(rng.randint(0, 12))]
        _check_optimal(old, new, diff_linear(old, new))
    print("test_linear_random_optimal: ok")


def test_ws_ignores_spacing():
    old = ["def f():", "    return 1"]
    new = ["def f():", "\treturn  1"]
    ops = diff_lines_ws(old, new)
    assert [o["op"] for o in ops] == ["eq", "eq"]
    # reported text stays original
    assert ops[1]["line"] == "    return 1"
    print("test_ws_ignores_spacing: ok")


def test_ws_still_catches_real_change():
    old = ["a = 1"]
    new = ["a = 2"]
    ops = diff_lines_ws(old, new)
    assert [o["op"] for o in ops] == ["del", "add"]
    print("test_ws_still_catches_real_change: ok")


if __name__ == "__main__":
    test_linear_simple()
    test_linear_random_optimal()
    test_ws_ignores_spacing()
    test_ws_still_catches_real_change()
    print("diffkit linear+ws tests passed")
