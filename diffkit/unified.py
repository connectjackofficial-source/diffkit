"""Unified diff parsing and patch application.

Implements the classic unified diff format:
    --- old
    +++ new
    @@ -l,s +l,s @@ context
with no dependency on difflib's patch machinery — we hand-roll the
hunk parser and the line-number arithmetic.
"""
from __future__ import annotations

_HUNK_RE = r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@"


def parse_unified(text: str) -> dict:
    """Parse a unified diff string.

    Returns {"old": name, "new": name, "hunks": [
      {"old_start": int, "old_count": int, "new_start": int,
       "new_count": int, "lines": [(op, line), ...]}]} where op is
    one of " ", "+", "-" (and "\\" no-newline markers are skipped).
    """
    lines = text.splitlines()
    old_name = new_name = None
    hunks = []
    cur = None
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("--- ") and old_name is None:
            old_name = ln[4:].lstrip()
        elif ln.startswith("+++ ") and new_name is None:
            new_name = ln[4:].lstrip()
        elif ln.startswith("@@"):
            import re
            m = re.match(_HUNK_RE, ln)
            if not m:
                i += 1
                continue
            old_s, old_c, new_s, new_c = (int(g or 1) for g in m.groups())
            cur = {"old_start": old_s, "old_count": old_c,
                   "new_start": new_s, "new_count": new_c, "lines": []}
            hunks.append(cur)
        elif cur is not None and ln[:1] in (" ", "+", "-"):
            cur["lines"].append((ln[:1], ln[1:]))
        elif cur is not None and ln[:1] == "\\":
            pass  # "\ No newline at end of file"
        i += 1
    return {"old": old_name, "new": new_name, "hunks": hunks}


def render_unified(ops, old_name: str = "a", new_name: str = "b",
                   context: int = 3) -> str:
    """Render diff ops (from :func:`diffkit.lcs.diff_lines`) as unified text.

    Groups change runs with surrounding context lines into hunks; a
    pure insertion at the top of the file becomes ``@@ -0,0 +1,k @@``.
    """
    seq = []
    old_no = new_no = 0
    for op in ops:
        if op["op"] == "eq":
            old_no += 1
            new_no += 1
            seq.append((" ", op["line"], old_no, new_no))
        elif op["op"] == "del":
            old_no += 1
            seq.append(("-", op["line"], old_no, None))
        else:
            new_no += 1
            seq.append(("+", op["line"], None, new_no))

    out = [f"--- {old_name}", f"+++ {new_name}"]
    i, n = 0, len(seq)
    while i < n:
        if seq[i][0] not in ("+", "-"):
            i += 1
            continue
        j = i
        while j < n and seq[j][0] in ("+", "-"):
            j += 1
        s = max(0, i - context)
        e = min(n, j + context)
        win = seq[s:e]
        old_start = next((x[2] for x in win if x[2] is not None), 0)
        new_start = next((x[3] for x in win if x[3] is not None), 1)
        old_count = sum(1 for x in win if x[0] in (" ", "-"))
        new_count = sum(1 for x in win if x[0] in (" ", "+"))
        out.append(f"@@ -{old_start},{old_count} +{new_start},{new_count} @@")
        for op, line, _, _ in win:
            out.append(f"{op}{line}")
        i = e
    return "\n".join(out) + "\n"


def apply_patch(old_text: str, patch_text: str) -> str:
    """Apply a unified patch to text and return the patched text.

    Positions are 1-based; a hunk with old_start == 0 means a pure
    insertion at the top of the file.
    """
    parsed = parse_unified(patch_text)
    lines = old_text.splitlines(keepends=True)
    for hunk in parsed["hunks"]:
        read = max(hunk["old_start"] - 1, 0)  # 0-based read position
        out = []
        for op, ln in hunk["lines"]:
            if op == " ":
                if read < len(lines) and lines[read].rstrip("\n") == ln:
                    out.append(lines[read])
                    read += 1
                else:
                    out.append(ln + "\n")
            elif op == "-":
                read += 1
            else:  # "+"
                out.append(ln + "\n")
        prefix = lines[: hunk["old_start"] - 1] if hunk["old_start"] > 1 else []
        lines = prefix + out + lines[read:]
    return "".join(lines)
