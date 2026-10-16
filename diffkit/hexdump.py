"""Classic hexdump rendering for binary inspection."""
from __future__ import annotations


def hexdump(data: bytes, width: int = 16, offset: int = 0) -> str:
    """Render bytes as an offset + hex + ASCII table.

    >>> print(hexdump(b"hello\\x00\\xffworld"))
    00000000  68 65 6c 6c 6f 00 ff 77 6f 72 6c 64              |hello..world|
    """
    out = []
    for i in range(0, len(data), width):
        chunk = data[i:i + width]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        hex_part = hex_part.ljust(width * 3 - 1)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        out.append(f"{offset + i:08x}  {hex_part}  |{ascii_part}|")
    return "\n".join(out)


def hexdiff(old: bytes, new: bytes, width: int = 16) -> str:
    """Hexdump both buffers side by side for visual comparison."""
    a = hexdump(old, width).splitlines()
    b = hexdump(new, width).splitlines()
    n = max(len(a), len(b))
    out = []
    for i in range(n):
        la = a[i] if i < len(a) else ""
        lb = b[i] if i < len(b) else ""
        out.append(f"{la:<60}  |  {lb}")
    return "\n".join(out)
