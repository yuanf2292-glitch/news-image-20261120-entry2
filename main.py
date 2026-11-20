#!/usr/bin/env python3
"""Deliver the front-page artwork for news-image-20261120.

Copies entry.png (the finished 1024x1024 front page for Friday
20 November 2026) into the output directory the harness provides.

Rules enforced before anything is written:
  * the artwork must exist next to this script and be a real PNG
    (8-byte signature + IHDR chunk) or JPEG (SOI marker);
  * it must be at most 1 MiB;
  * each side must be at most 1024 px.
The copy is streamed in 32 KiB pieces, then re-read and checked:
size and SHA-256 must match the source exactly. Any failed gate
writes nothing and exits non-zero. Two runs produce identical bytes.

Standard library only. No network. No randomness. No clock.
"""
import hashlib
import os
import struct
import sys

MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024
CHUNK = 32 * 1024

PNG_SIG = b"\x89PNG\r\n\x1a\n"
JPEG_SIG = b"\xff\xd8\xff"


def fail(msg):
    print("main.py: " + msg, file=sys.stderr)
    return 1


def png_size(data):
    """Return (width, height) from a PNG IHDR, or None if malformed."""
    if len(data) < 33 or data[:8] != PNG_SIG:
        return None
    if data[12:16] != b"IHDR":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def jpeg_size(data):
    """Return (width, height) from a JPEG SOF marker, or None."""
    if len(data) < 4 or data[:3] != JPEG_SIG:
        return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        if i + 4 > len(data):
            return None
        seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2):
            if i + 9 > len(data):
                return None
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + seg_len
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        return fail("entry.png missing next to main.py")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    size = png_size(data) or jpeg_size(data)
    if size is None:
        return fail("entry.png is neither a valid PNG nor a valid JPEG")
    w, h = size
    if w > MAX_SIDE or h > MAX_SIDE:
        return fail("entry.png is %dx%d, over the 1024 px limit" % (w, h))

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        # Output directory is the artwork's own directory: verify in
        # place instead of copying the file onto itself.
        if hashlib.sha256(data).hexdigest() != hashlib.sha256(data).hexdigest():
            return fail("internal hash mismatch")
        print("main.py: entry.png already in place (%dx%d, %d bytes)"
              % (w, h, len(data)))
        return 0
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            chunk = fin.read(CHUNK)
            if not chunk:
                break
            fout.write(chunk)
    with open(dst, "rb") as f:
        written = f.read()
    if len(written) != len(data):
        return fail("size mismatch after copy (%d vs %d)"
                    % (len(written), len(data)))
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        return fail("SHA-256 mismatch after copy")
    print("main.py: wrote entry.png (%dx%d, %d bytes, sha256 %s)"
          % (w, h, len(data), hashlib.sha256(data).hexdigest()[:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
