"""Tests for diffkit.similarity and diffkit.tree."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from diffkit.similarity import ngram_similarity
from diffkit.tree import tree_diff


def test_identical():
    assert ngram_similarity("hello world", "hello world") == 1.0
    print("test_identical: ok")


def test_completely_different():
    assert ngram_similarity("aaaa", "bbbb") == 0.0
    print("test_completely_different: ok")


def test_partial():
    s = ngram_similarity("the quick brown fox", "the quick brown dog")
    assert 0.0 < s < 1.0
    print("test_partial: ok")


def test_empty():
    assert ngram_similarity("", "") == 1.0
    assert ngram_similarity("", "abc") == 0.0
    print("test_empty: ok")


def test_tree_diff():
    with tempfile.TemporaryDirectory() as td:
        old = Path(td) / "old"
        new = Path(td) / "new"
        (old / "src").mkdir(parents=True)
        (new / "src").mkdir(parents=True)
        (old / "src" / "a.py").write_text("print(1)\n")
        (old / "src" / "gone.py").write_text("x")
        (old / "keep.txt").write_text("same")
        (new / "src" / "a.py").write_text("print(2)\n")
        (new / "src" / "fresh.py").write_text("y")
        (new / "keep.txt").write_text("same")
        r = tree_diff(old, new)
        assert r["added"] == ["src/fresh.py"]
        assert r["removed"] == ["src/gone.py"]
        assert r["modified"] == ["src/a.py"]
    print("test_tree_diff: ok")


if __name__ == "__main__":
    test_identical()
    test_completely_different()
    test_partial()
    test_empty()
    test_tree_diff()
    print("diffkit similarity+tree tests passed")
