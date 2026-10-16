# Contributing

Keep it zero-dependency and stdlib-only: no new imports beyond the
standard library. Tests are plain scripts (no pytest):

```bash
python tests/test_<module>.py
```

Every feature lands as two commits: the implementation and its test
coverage. Run the full suite before opening a PR:

```bash
for t in tests/test_*.py; do python "$t"; done
```
