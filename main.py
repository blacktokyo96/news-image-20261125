"""Copy the supplied front page to /output/entry.png.

Standard library only. No network. The program reads entry.png from
its own directory, checks it is a JPEG, copies its bytes unchanged to
the output directory, and verifies the written file against the source
SHA-256 before reporting success.
"""

import hashlib
import os
import sys


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except FileNotFoundError:
        print("Source entry.png is missing: " + source, file=sys.stderr)
        return 1
    if data[:3] != b"\xff\xd8\xff":
        print("Source entry.png is not a JPEG: expected FF D8 FF magic bytes",
              file=sys.stderr)
        return 1
    source_hash = sha256(data)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    os.chmod(output_dir, 0o755)
    destination = os.path.join(output_dir, "entry.png")
    with open(destination, "wb") as handle:
        handle.write(data)
    os.chmod(destination, 0o644)
    with open(destination, "rb") as handle:
        written = handle.read()
    if len(written) != len(data):
        print("Written entry.png size does not match source",
              file=sys.stderr)
        return 1
    if sha256(written) != source_hash:
        print("Written entry.png SHA-256 does not match source",
              file=sys.stderr)
        return 1
    print("Wrote %d bytes to %s; SHA-256 %s"
          % (len(written), destination, source_hash))
    return 0


if __name__ == "__main__":
    sys.exit(main())
