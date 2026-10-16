"""Tests for diffkit.lcs."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from diffkit.lcs import diff_lines, diff_bytes, diff_text


def test_identical():
    ops = diff_lines(["a", "b", "c"], ["a", "b", "c"])
    assert [o["op"] for o in ops] == ["eq", "eq", "eq"]
    print("test_identical: ok")


def test_insert_delete():
    ops = diff_lines(["a", "b"], ["a", "x", "b"])
    assert [o["op"] for o in ops] == ["eq", "add", "eq"]
    assert ops[1]["line"] == "x"
    ops = diff_lines(["a", "b"], ["a"])
    assert [o["op"] for o in ops] == ["eq", "del"]
    print("test_insert_delete: ok")


def test_rewrite():
    ops = diff_lines(["one", "two"], ["one", "TWO"])
    assert [o["op"] for o in ops] == ["eq", "del", "add"]
    print("test_rewrite: ok")


def test_bytes_diff():
    old = b"\x00\x01" * 8          # exactly one 16-byte block
    new = old + b"\xde\xad"        # one full block + one 2-byte block
    ops = diff_bytes(old, new)
    assert [o["op"] for o in ops] == ["eq", "add"]
    assert ops[-1]["line"] == b"\xde\xad"
    print("test_bytes_diff: ok")


def test_diff_text():
    ops = diff_text("hello\nworld", "hello\nearth")
    assert [o["op"] for o in ops] == ["eq", "del", "add"]
    print("test_diff_text: ok")


def test_empty():
    assert diff_lines([], []) == []
    ops = diff_lines([], ["a"])
    assert ops == [{"op": "add", "line": "a", "old": None, "new": 0}]
    print("test_empty: ok")


if __name__ == "__main__":
    test_identical()
    test_insert_delete()
    test_rewrite()
    test_bytes_diff()
    test_diff_text()
    test_empty()
    print("diffkit lcs tests passed")
