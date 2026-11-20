#!/usr/bin/env python3
"""Ship the finished front page for news-image-20261120.

The entry's program: take entry.png — the 1024x1024 front page for
Friday 20 November 2026 sitting next to this script — and write it
to the output directory the harness provides.

Before anything is written the artwork is gated:
  * it must be a real PNG (8-byte signature + IHDR chunk) or a real
    JPEG (SOI marker);
  * it must be at most 1 MiB;
  * neither side may exceed 1024 px.
The copy goes out in 32 KiB pieces, is read back, and must match the
source byte for byte (size and SHA-256). A failed gate writes
nothing and exits non-zero. Two runs produce identical bytes.

Standard library only. No network. No randomness. No clock.
"""
import hashlib
import os
import struct
import sys

BYTE_LIMIT = 1024 * 1024
SIDE_LIMIT = 1024
PIECE = 32 * 1024

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def refuse(msg):
    print("main.py: " + msg, file=sys.stderr)
    return 1


def read_png_dims(blob):
    """(width, height) from a PNG IHDR, else None."""
    if len(blob) < 33 or blob[:8] != PNG_MAGIC:
        return None
    if blob[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", blob[16:24])


def read_jpeg_dims(blob):
    """(width, height) from a JPEG SOF marker, else None."""
    if len(blob) < 4 or blob[:3] != JPEG_MAGIC:
        return None
    pos = 2
    while pos + 9 < len(blob):
        if blob[pos] != 0xFF:
            pos += 1
            continue
        marker = blob[pos + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if pos + 4 > len(blob):
            return None
        seg = struct.unpack(">H", blob[pos + 2:pos + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2):
            if pos + 9 > len(blob):
                return None
            h, w = struct.unpack(">HH", blob[pos + 5:pos + 9])
            return w, h
        pos += 2 + seg
    return None


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        return refuse("entry.png missing next to main.py")
    with open(src, "rb") as handle:
        blob = handle.read()
    if len(blob) > BYTE_LIMIT:
        return refuse("entry.png is %d bytes, over the 1 MiB limit"
                      % len(blob))
    dims = read_png_dims(blob) or read_jpeg_dims(blob)
    if dims is None:
        return refuse("entry.png is neither a valid PNG nor a valid JPEG")
    width, height = dims
    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        return refuse("entry.png is %dx%d, over the 1024 px limit"
                      % (width, height))

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    digest = hashlib.sha256(blob).hexdigest()
    if os.path.abspath(dst) == os.path.abspath(src):
        # The output directory is the artwork's own directory: there
        # is nothing to copy, the file is already in place.
        print("main.py: entry.png already in place (%dx%d, %d bytes)"
              % (width, height, len(blob)))
        return 0
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            piece = fin.read(PIECE)
            if not piece:
                break
            fout.write(piece)
    with open(dst, "rb") as handle:
        copied = handle.read()
    if len(copied) != len(blob):
        return refuse("size mismatch after copy (%d vs %d)"
                      % (len(copied), len(blob)))
    if hashlib.sha256(copied).hexdigest() != digest:
        return refuse("SHA-256 mismatch after copy")
    print("main.py: wrote entry.png (%dx%d, %d bytes, sha256 %s)"
          % (width, height, len(blob), digest[:12]))
    return 0


if __name__ == "__main__":
    sys.exit(run())
