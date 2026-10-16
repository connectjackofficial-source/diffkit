"""Tests for diffkit.cli (subprocess-level smoke tests)."""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from diffkit.cli import main


def _run(*args):
    out = subprocess.run([sys.executable, "-m", "diffkit.cli", *args],
                         capture_output=True, text=True)
    return out.returncode, out.stdout, out.stderr


def test_diff_smoke():
    with tempfile.TemporaryDirectory() as td:
        a = Path(td) / "a.txt"
        b = Path(td) / "b.txt"
        a.write_text("one\ntwo\n")
        b.write_text("one\nTWO\n")
        rc, out, err = _run("diff", str(a), str(b))
        assert rc == 0
        assert "- two" in out and "+ TWO" in out and " one" in out
    print("test_diff_smoke: ok")


def test_sim_smoke():
    with tempfile.TemporaryDirectory() as td:
        a = Path(td) / "a.txt"
        b = Path(td) / "b.txt"
        a.write_text("same text here")
        b.write_text("same text here")
        rc, out, err = _run("sim", str(a), str(b))
        assert rc == 0 and out.strip() == "1.0000"
    print("test_sim_smoke: ok")


def test_hex_smoke():
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "bin.dat"
        f.write_bytes(b"\x00\xffabc")
        rc, out, err = _run("hex", str(f))
        assert rc == 0
        assert out.startswith("00000000")
        assert "00 ff" in out
    print("test_hex_smoke: ok")


def test_stats_smoke():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "p.diff"
        p.write_text("--- a/f\n+++ b/f\n@@ -1,1 +1,2 @@\n-x\n+x\n+y\n")
        rc, out, err = _run("stats", str(p))
        assert rc == 0
        assert "added:    2" in out and "removed:  1" in out
    print("test_stats_smoke: ok")


if __name__ == "__main__":
    test_diff_smoke()
    test_sim_smoke()
    test_hex_smoke()
    test_stats_smoke()
    print("diffkit cli tests passed")
