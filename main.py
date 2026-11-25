#!/usr/bin/env python3
"""Invent a Word We Need — make.fun bounty entry.

One fixed entry line: a new word, "snugret", with its one-line
definition. main() writes it exactly as-is, with no trailing
newline, to /output/entry.txt. Python 3, standard library only.

Validators check the entry is valid UTF-8, 1-140 characters, and
a single line. The self-test also checks the output is
deterministic across runs.
"""

import os
import sys

ENTRY = "Snugret (n.) — the cosy guilt of cancelling plans to stay home, relieved and a little ashamed at once."

OUTPUT_PATH = "/output/entry.txt"


def validate_utf8(entry: str) -> None:
    """Entry must round-trip through UTF-8 encoding."""
    if not isinstance(entry, str):
        raise ValueError("entry must be a string")
    entry.encode("utf-8").decode("utf-8")


def validate_length(entry: str) -> None:
    """Entry must be a non-empty string of 1-140 characters."""
    if not (1 <= len(entry) <= 140):
        raise ValueError(f"entry must be 1-140 characters, got {len(entry)}")
    if not entry.strip():
        raise ValueError("entry must not be only whitespace")


def validate_single_line(entry: str) -> None:
    """Entry must be one line with no leading/trailing whitespace."""
    if entry != entry.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")


def validate(entry: str) -> None:
    """Validate the entry against the bounty gate."""
    validate_utf8(entry)
    validate_length(entry)
    validate_single_line(entry)


def main() -> int:
    validate(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # Write exactly as-is, no trailing newline.
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    print(f"Wrote {len(ENTRY)} characters to {OUTPUT_PATH}")
    return 0


def self_test() -> None:
    """Self-test: validate, write twice, re-read, compare byte-for-byte.

    Checks entry length (102 chars, within 1-140), single-line
    shape, no trailing newline, byte-identical output, and that
    a second run reproduces the same bytes exactly.
    """
    validate(ENTRY)
    assert 1 <= len(ENTRY) <= 140, f"entry length {len(ENTRY)} out of range"
    assert "\n" not in ENTRY and "\r" not in ENTRY, "entry must be one line"
    main()
    with open(OUTPUT_PATH, "rb") as f:
        first_run = f.read()
    main()
    with open(OUTPUT_PATH, "rb") as f:
        second_run = f.read()
    assert first_run == second_run, "output is not deterministic across runs"
    raw = first_run
    assert raw == ENTRY.encode("utf-8"), "output bytes differ from ENTRY"
    assert not raw.endswith(b"\n"), "output must not end with a newline"
    assert len(raw.decode("utf-8")) == len(ENTRY) <= 140
    print("self-test passed: output is byte-identical to ENTRY, "
          f"{len(ENTRY)} chars, single line, no trailing newline, "
          "deterministic across runs")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        raise SystemExit(main())
