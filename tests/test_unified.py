"""Tests for diffkit.unified."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from diffkit.unified import parse_unified, apply_patch


PATCH = """--- a/notes.txt
+++ b/notes.txt
@@ -1,3 +1,4 @@
 alpha
-beta
+beta v2
 gamma
+delta
"""


def test_parse():
    p = parse_unified(PATCH)
    assert p["old"] == "a/notes.txt"
    assert p["new"] == "b/notes.txt"
    assert len(p["hunks"]) == 1
    h = p["hunks"][0]
    assert h["old_start"] == 1 and h["old_count"] == 3
    assert h["new_start"] == 1 and h["new_count"] == 4
    ops = [op for op, _ in h["lines"]]
    assert ops == [" ", "-", "+", " ", "+"]
    print("test_parse: ok")


def test_apply():
    old = "alpha\nbeta\ngamma\n"
    out = apply_patch(old, PATCH)
    assert out == "alpha\nbeta v2\ngamma\ndelta\n"
    print("test_apply: ok")


def test_insert_at_top():
    patch = "--- a\n+++ b\n@@ -0,0 +1,2 @@\n+head\n+second\n"
    assert apply_patch("x\ny\n", patch) == "head\nsecond\nx\ny\n"
    print("test_insert_at_top: ok")


def test_delete_hunk():
    patch = "--- a\n+++ b\n@@ -1,2 +1,1 @@\n-aaa\n bbb\n"
    assert apply_patch("aaa\nbbb\n", patch) == "bbb\n"
    print("test_delete_hunk: ok")


if __name__ == "__main__":
    test_parse()
    test_apply()
    test_insert_at_top()
    test_delete_hunk()
    print("diffkit unified tests passed")
