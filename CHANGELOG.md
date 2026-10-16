# Changelog

All notable changes to diffkit.

## 0.2.0 - 2026-10-16

- `render_unified` — generate unified patch text from diff ops
  (render/apply round-trip verified by tests)
- CLI subcommands: `diff`, `bytes`, `apply`, `sim`, `tree`, `hex`, `stats`
- `patch_stats` — hunk/added/removed/context tallies from a patch file

## 0.1.0 - 2026-10-16

- `diff_lines` / `diff_bytes` — LCS line diff and byte-block diff
- `parse_unified` / `apply_patch` — unified patch parsing and application
- `ngram_similarity` — character n-gram Jaccard similarity
- `tree_diff` — directory comparison by relative path and sha256
- `hexdump` / `hexdiff` — hex rendering for binary inspection
- Package scaffold: pyproject, MIT license, console script `diffkit`
