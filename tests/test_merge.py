"""Tests for diffkit batch 3: 3-way merge."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from diffkit.merge import merge_3way, has_conflicts, MergeConflict


def test_non_overlapping_changes_merge_clean():
    base = "a\nb\nc\n"
    ours = "a\nB\nc\n"      # edit line 2
    theirs = "a\nb\nC\n"    # edit line 3
    merged = merge_3way(base, ours, theirs)
    assert merged == "a\nB\nC\n", merged
    assert not has_conflicts(merged)
    print("test_non_overlapping_changes_merge_clean: ok")


def test_same_side_change_taken():
    base = "a\nb\nc\n"
    ours = "a\nb\nc\n"      # untouched
    theirs = "a\nb\nx\n"    # one-side edit
    assert merge_3way(base, ours, theirs) == "a\nb\nx\n"
    print("test_same_side_change_taken: ok")


def test_conflict_markers_and_flag():
    base = "a\nb\nc\n"
    ours = "a\nX\nc\n"
    theirs = "a\nY\nc\n"
    merged = merge_3way(base, ours, theirs)
    assert has_conflicts(merged)
    assert "<<<<<<< ours" in merged and ">>>>>>> theirs" in merged
    try:
        merge_3way(base, ours, theirs, conflict_markers=False)
        raise AssertionError("expected MergeConflict")
    except MergeConflict:
        pass
    print("test_conflict_markers_and_flag: ok")


def test_insertions_on_both_sides():
    base = "a\nb\n"
    ours = "a\nins-ours\nb\n"
    theirs = "a\nb\nins-theirs\n"
    merged = merge_3way(base, ours, theirs)
    assert merged == "a\nins-ours\nb\nins-theirs\n", merged
    assert not has_conflicts(merged)
    print("test_insertions_on_both_sides: ok")


if __name__ == "__main__":
    test_non_overlapping_changes_merge_clean()
    test_same_side_change_taken()
    test_conflict_markers_and_flag()
    test_insertions_on_both_sides()
    print("diffkit batch3 tests passed")
