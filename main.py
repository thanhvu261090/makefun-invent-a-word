#!/usr/bin/env python3
"""Invent a Word We Need — make.fun bounty entry.

Holds one fixed entry line: a new word, "snugret", plus its
one-line definition. Writes it exactly as-is, with no trailing
newline, to /output/entry.txt. Python 3, standard library only.
"""

import os
import sys

ENTRY = "Snugret (n.) — the cosy guilt of cancelling plans to stay home, relieved and a little ashamed at once."

OUTPUT_PATH = "/output/entry.txt"


def validate(entry: str) -> None:
    """Validate the entry against the bounty gate."""
    if not isinstance(entry, str):
        raise ValueError("entry must be a string")
    # Must be valid UTF-8 (round-trip check).
    entry.encode("utf-8").decode("utf-8")
    if not (1 <= len(entry) <= 140):
        raise ValueError(f"entry must be 1-140 characters, got {len(entry)}")
    if entry != entry.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    if not entry.strip():
        raise ValueError("entry must not be only whitespace")


def main() -> int:
    validate(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # Write exactly as-is, no trailing newline.
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    print(f"Wrote {len(ENTRY)} characters to {OUTPUT_PATH}")
    return 0


def self_test() -> None:
    """Small self-test: validate, write, re-read, compare byte-for-byte."""
    validate(ENTRY)
    main()
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    assert raw == ENTRY.encode("utf-8"), "output bytes differ from ENTRY"
    assert not raw.endswith(b"\n"), "output must not end with a newline"
    assert len(raw.decode("utf-8")) == len(ENTRY) <= 140
    print("self-test passed: output is byte-identical to ENTRY, "
          f"{len(ENTRY)} chars, no trailing newline")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        raise SystemExit(main())
