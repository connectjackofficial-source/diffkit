# Roadmap

- `--stat` flag on `diff` / `bytes` to print patch stats inline
- Myers O(ND) diff for large-file performance (LCS DP is O(n*m))
- `diff` with configurable context in `render_unified` (done: `context=` param)
- Patch fuzz: tolerate misplaced context lines on apply (currently exact)
- Byte diff with variable-length anchor search instead of fixed blocks
- `pipx`-style single-file distribution
