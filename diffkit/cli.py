"""Command-line interface for diffkit.

Subcommands: diff (text), bytes (block diff), apply (patch), sim
(n-gram similarity), tree (directory compare), hex (hexdump), stats.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .lcs import diff_lines, diff_bytes
from .unified import apply_patch, parse_unified
from .similarity import ngram_similarity
from .tree import tree_diff
from .hexdump import hexdump
from .patchstats import patch_stats


def _print_diff(ops) -> None:
    for op in ops:
        mark = {"eq": " ", "del": "-", "add": "+"}[op["op"]]
        sys.stdout.write(f"{mark} {op['line']}\n")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="diffkit", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("diff", help="text line diff of two files")
    d.add_argument("old")
    d.add_argument("new")

    b = sub.add_parser("bytes", help="fixed-block byte diff of two files")
    b.add_argument("old")
    b.add_argument("new")
    b.add_argument("--block", type=int, default=16)

    a = sub.add_parser("apply", help="apply a unified patch to a file")
    a.add_argument("file")
    a.add_argument("patch")

    s = sub.add_parser("sim", help="n-gram similarity of two files")
    s.add_argument("a")
    s.add_argument("b")
    s.add_argument("-n", type=int, default=3)

    t = sub.add_parser("tree", help="compare two directory trees")
    t.add_argument("old")
    t.add_argument("new")

    h = sub.add_parser("hex", help="hexdump a file")
    h.add_argument("file")
    h.add_argument("--width", type=int, default=16)

    st = sub.add_parser("stats", help="summarize a unified patch file")
    st.add_argument("patch")
    return p


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)
    if args.cmd == "diff":
        _print_diff(diff_lines(
            Path(args.old).read_text(encoding="utf-8", errors="replace").splitlines(),
            Path(args.new).read_text(encoding="utf-8", errors="replace").splitlines(),
        ))
    elif args.cmd == "bytes":
        _print_diff(diff_bytes(
            Path(args.old).read_bytes(), Path(args.new).read_bytes(), args.block))
    elif args.cmd == "apply":
        old = Path(args.file).read_text(encoding="utf-8", errors="replace")
        patch = Path(args.patch).read_text(encoding="utf-8", errors="replace")
        sys.stdout.write(apply_patch(old, patch))
    elif args.cmd == "sim":
        a = Path(args.a).read_text(encoding="utf-8", errors="replace")
        b = Path(args.b).read_text(encoding="utf-8", errors="replace")
        print(f"{ngram_similarity(a, b, args.n):.4f}")
    elif args.cmd == "tree":
        r = tree_diff(args.old, args.new)
        for kind in ("added", "removed", "modified"):
            for path in r[kind]:
                print(f"{kind:>8}  {path}")
    elif args.cmd == "hex":
        print(hexdump(Path(args.file).read_bytes(), args.width))
    elif args.cmd == "stats":
        s = patch_stats(Path(args.patch).read_text(encoding="utf-8", errors="replace"))
        print(f"hunks:    {s['hunks']}")
        print(f"added:    {s['added']}")
        print(f"removed:  {s['removed']}")
        print(f"context:  {s['context']}")
        for f in s["files"]:
            print(f"file:     {f['old']} -> {f['new']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
