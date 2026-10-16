"""Tests for diffkit.hexdump and diffkit.patchstats."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from diffkit.hexdump import hexdump, hexdiff
from diffkit.patchstats import patch_stats


def test_hexdump_shape():
    out = hexdump(b"hello\x00\xffworld")
    lines = out.splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("00000000")
    assert "68 65 6c 6c 6f 00 ff 77 6f 72 6c 64" in lines[0]
    assert "|hello..world|" in lines[0]
    print("test_hexdump_shape: ok")


def test_hexdump_multirow():
    out = hexdump(bytes(range(20)))
    assert len(out.splitlines()) == 2
    assert out.splitlines()[1].startswith("00000010")
    print("test_hexdump_multirow: ok")


def test_hexdump_empty():
    assert hexdump(b"") == ""
    print("test_hexdump_empty: ok")


def test_hexdiff_aligns():
    out = hexdiff(b"abc", b"abcd")
    lines = out.splitlines()
    assert len(lines) == 1
    assert lines[0].count("|") >= 2
    print("test_hexdiff_aligns: ok")


def test_stats():
    patch = "--- a/f\n+++ b/f\n@@ -1,3 +1,4 @@\n a\n-b\n+b2\n c\n+d\n"
    s = patch_stats(patch)
    assert s["hunks"] == 1
    assert s["added"] == 2
    assert s["removed"] == 1
    assert s["context"] == 2
    assert s["files"] == [{"old": "a/f", "new": "b/f"}]
    print("test_stats: ok")


def test_stats_empty():
    s = patch_stats("")
    assert s == {"hunks": 0, "added": 0, "removed": 0,
                 "context": 0, "files": []}
    print("test_stats_empty: ok")


if __name__ == "__main__":
    test_hexdump_shape()
    test_hexdump_multirow()
    test_hexdump_empty()
    test_hexdiff_aligns()
    test_stats()
    test_stats_empty()
    print("diffkit hexdump+patchstats tests passed")
