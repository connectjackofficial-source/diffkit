# diffkit

Zero-dependency binary and text diff toolkit. Pure Python — no difflib
shortcuts, no third-party deps — built for reversible inspection of code
diffs, patch files and binary blobs.

## Why

Most diff tooling hides the algorithm behind a fat dependency tree or a
GUI. `diffkit` keeps the classic algorithms readable and testable so you
can drop it into scripts, CI and RE toolchains without installing
anything:

- LCS line diff and fixed-block byte diff for binaries
- Unified diff parser, applier **and** generator (render/apply round-trip)
- Character n-gram Jaccard similarity for fuzzy matching
- Whole-directory comparison by relative path and sha256
- Hexdump with side-by-side visual diff
- Patch statistics from unified hunks

## Install

```bash
pip install .
```

or run straight from a checkout:

```bash
python -m diffkit.cli diff old.txt new.txt
```

## Usage

```python
from diffkit import diff_lines, render_unified, apply_patch

ops = diff_lines(old_lines, new_lines)
patch = render_unified(ops, "a/f", "b/f")
assert apply_patch(old_text, patch) == new_text
```

CLI subcommands: `diff`, `bytes`, `apply`, `sim`, `tree`, `hex`, `stats`.

## Test

```bash
python tests/test_lcs.py
python tests/test_unified.py
python tests/test_render_unified.py
python tests/test_similarity_tree.py
python tests/test_hexdump_patchstats.py
python tests/test_cli.py
```

## License

MIT
