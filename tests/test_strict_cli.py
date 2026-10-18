"""Tests for strict patch application and the diff --ws/--stat CLI."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from diffkit.unified import apply_patch, PatchApplyError, render_unified
from diffkit.lcs import diff_lines, diff_lines_ws


def test_strict_ok_on_match():
    old = "a\nb\nc\n"
    patch = "--- x\n+++ y\n@@ -1,3 +1,3 @@\n a\n-b\n+d\n c\n"
    assert apply_patch(old, patch, strict=True) == "a\nd\nc\n"
    print("test_strict_ok_on_match: ok")


def test_strict_raises_on_mismatch():
    old = "a\nX\nc\n"
    patch = "--- x\n+++ y\n@@ -1,3 +1,3 @@\n a\n-b\n+d\n c\n"
    try:
        apply_patch(old, patch, strict=True)
        raise AssertionError("expected PatchApplyError")
    except PatchApplyError:
        pass
    # lenient mode still applies positionally
    assert apply_patch(old, patch) == "a\nd\nc\n"
    print("test_strict_raises_on_mismatch: ok")


def test_ws_cli_flag_makes_spacing_equal():
    old = ["x  =   1", "y   = 2"]
    new = ["x = 1", "y = 2"]
    assert [o["op"] for o in diff_lines(old, new)] != ["eq", "eq"]
    assert [o["op"] for o in diff_lines_ws(old, new)] == ["eq", "eq"]
    print("test_ws_cli_flag_makes_spacing_equal: ok")


def test_stat_renders_from_ops():
    ops = diff_lines(["a", "b"], ["a", "c", "d"])
    patch = render_unified(ops)
    assert "@@" in patch
    assert "+c" in patch
    print("test_stat_renders_from_ops: ok")


if __name__ == "__main__":
    test_strict_ok_on_match()
    test_strict_raises_on_mismatch()
    test_ws_cli_flag_makes_spacing_equal()
    test_stat_renders_from_ops()
    print("diffkit strict+cli tests passed")
