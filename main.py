#!/usr/bin/env python3
"""Front-page entry for make.fun bounty news-image-20261123.

What this program does is deliberately small: it takes the front page
that was rendered in advance and bundled next to this file
(``entry.png``) and copies it, byte for byte, into the output
directory the grader expects. Nothing is drawn here, nothing is
downloaded, and nothing depends on the time of day, on chance, or on
anything outside the standard library, so every run produces exactly
the same file.

Usage, exactly as the grader runs it::

    python3 -P -s main.py

The image lands at ``$MAKEFUN_OUTPUT_DIR/entry.png``; when that
variable is unset the fallback is ``/output/entry.png``. After the
copy the program checks the result twice — once by file size and once
by SHA-256 digest — and only then reports success.
"""

import hashlib
import os
import shutil
import sys

IMAGE_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
READ_CHUNK = 65536


def file_sha256(path):
    """Return the hex SHA-256 digest of the file at *path*."""
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(READ_CHUNK)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def run():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    bundled = os.path.join(script_dir, IMAGE_NAME)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, IMAGE_NAME)

    shutil.copyfile(bundled, destination)

    copied_size = os.path.getsize(destination)
    if copied_size != os.path.getsize(bundled):
        print("error: copied file size does not match the bundled image",
              file=sys.stderr)
        return 1

    copied_hash = file_sha256(destination)
    if copied_hash != file_sha256(bundled):
        print("error: copied file hash does not match the bundled image",
              file=sys.stderr)
        return 1

    print("wrote %s (%d bytes, sha256 %s)"
          % (destination, copied_size, copied_hash))
    return 0


if __name__ == "__main__":
    sys.exit(run())
