# Security

- `apply_patch` only mutates an in-memory string; it never writes files
  or touches the filesystem on its own. Feed it untrusted patches freely.
- `tree_diff` reads files recursively; pass only directories you trust.
- No network access, no eval, no subprocess in library code.
- If you find a vulnerability, open an issue privately with a minimal
  reproducer before any disclosure.
