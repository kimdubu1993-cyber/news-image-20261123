#!/usr/bin/env python3
"""Copy the pre-rendered news image into the output directory.

Standard library only. No network, no clock, no randomness: the output
bytes are exactly the bytes of news.png shipped beside this script.
"""
import hashlib
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SOURCE_NAME = "news.png"
OUTPUT_NAME = "entry.png"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    os.chmod(out_dir, 0o755)
    dest = os.path.join(out_dir, OUTPUT_NAME)

    with open(source, "rb") as fh:
        header = fh.read(8)
    if header != PNG_MAGIC:
        print("news.png is not a PNG file", file=sys.stderr)
        return 1

    shutil.copyfile(source, dest)
    os.chmod(dest, 0o644)

    with open(source, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print("wrote %s sha256=%s" % (dest, digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
