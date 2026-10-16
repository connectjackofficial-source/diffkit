"""Tests for diffkit.unified.render_unified (round-trip with apply)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from diffkit.lcs import diff_lines
from diffkit.unified import render_unified, apply_patch, parse_unified


def _roundtrip(old: list, new: list):
    ops = diff_lines(old, new)
    patch = render_unified(ops, "a/f", "b/f")
    out = apply_patch("\n".join(old) + ("\n" if old else ""), patch)
    assert out == "\n".join(new) + ("\n" if new else ""), patch
    return patch


def test_roundtrip_simple():
    patch = _roundtrip(["a", "b", "c"], ["a", "B", "c", "d"])
    assert patch.startswith("--- a/f\n+++ b/f\n@@")
    print("test_roundtrip_simple: ok")


def test_roundtrip_insert_top():
    _roundtrip(["x", "y"], ["head", "x", "y"])  # insertion round-trips
    print("test_roundtrip_insert_top: ok")


def test_roundtrip_delete_all():
    _roundtrip(["a", "b"], [])
    print("test_roundtrip_delete_all: ok")


def test_roundtrip_identical():
    patch = _roundtrip(["a"], ["a"])
    assert patch == "--- a/f\n+++ b/f\n"  # no hunks when nothing changed
    print("test_roundtrip_identical: ok")


def test_parse_render_consistency():
    ops = diff_lines(["1", "2", "3"], ["1", "x", "3", "4"])
    patch = render_unified(ops)
    parsed = parse_unified(patch)
    assert parsed["hunks"][0]["old_count"] == 3
    assert parsed["hunks"][0]["new_count"] == 4
    print("test_parse_render_consistency: ok")


if __name__ == "__main__":
    test_roundtrip_simple()
    test_roundtrip_insert_top()
    test_roundtrip_delete_all()
    test_roundtrip_identical()
    test_parse_render_consistency()
    print("diffkit render_unified tests passed")
