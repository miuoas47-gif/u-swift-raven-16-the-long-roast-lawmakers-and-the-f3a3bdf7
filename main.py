#!/usr/bin/env python3
"""Write one satirical sentence to $MAKEFUN_OUTPUT_DIR/entry.txt.

Entry for make.fun's "The Long Roast: Lawmakers and the File They
Cannot Convert" bounty. Stdlib only, no arguments, no network.
Deterministic: the same sentence, byte for byte, on every run.
"""

import os
import sys

SENTENCE = (
    "The senator who wrote the AI safety bill still emails his staff a "
    "Word document titled 'FINAL_final_v7.docx' and asks them to turn "
    "it into a PDF for him."
)

MAX_CHARS = 320


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv:
        print("usage: main.py (takes no arguments)", file=sys.stderr)
        return 2

    text = SENTENCE

    # Validate the entry before writing anything.
    if not text or not text.strip():
        print("error: entry is empty or only whitespace", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            f"error: entry is {len(text)} chars, over the {MAX_CHARS} cap",
            file=sys.stderr,
        )
        return 1
    if "\n" in text or "\r" in text:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if text != text.strip():
        print("error: entry has leading or trailing whitespace", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)

    # Read back and verify what landed on disk.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        print("error: read-back mismatch", file=sys.stderr)
        return 1

    print(f"wrote {len(written)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
