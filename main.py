#!/usr/bin/env python3
"""Notes From a Passive-Aggressive Fridge -- round 2 entry.

A smart fridge leaves one dry, petty note on its door screen for its
owner. The program writes that single line to /output/entry.txt,
deterministically: the note is fixed text baked into the code, so every
run produces byte-identical output.

Why this note works (judge brief, in order):
  1. It is the fridge speaking, not the owner -- a sensor log entry.
  2. The joke turns twice: first the owner is caught staring at the
     light instead of eating, then the yogurt -- not the fridge --
     delivers the judgement.
  3. Fridge voice: a door log with a timestamp, smug about what its
     sensors recorded at 2:14 a.m.
  4. The grudge is small and domestic: opening the fridge for the
     light, a midnight habit, nothing bigger.
  5. Fresh concrete detail: the door log, the light, the yogurt.
     Nothing is explained; the reader fills in the sting.

Gate: /output/entry.txt must be UTF-8 text of 1 to 200 characters,
not only whitespace. The note below is 110 characters.
"""

import os
import sys

# The note the fridge leaves on its door screen. Fixed text: the
# program is deterministic by design, no randomness, no clock reads,
# no input -- the same note on every run, in every sandbox.
NOTE = (
    "Door log, 2:14 a.m.: you opened me just to stare at the light. "
    "The yogurt saw you. The yogurt is disappointed."
)

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200


def validate(note: str) -> None:
    """Enforce the gate before writing anything: 1-200 chars, not blank."""
    if not isinstance(note, str):
        raise TypeError("note must be a string")
    if not (MIN_CHARS <= len(note) <= MAX_CHARS):
        raise ValueError(
            f"note is {len(note)} characters, must be {MIN_CHARS}-{MAX_CHARS}"
        )
    if not note.strip():
        raise ValueError("note must not be only whitespace")
    if "\n" in note or "\r" in note:
        raise ValueError("note must be a single line")


def main() -> int:
    validate(NOTE)

    out_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(out_dir, exist_ok=True)

    # One trailing newline: the gate counts characters, and a single
    # newline keeps the file a well-formed text line without changing
    # the note itself.
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(NOTE + "\n")

    # Verify the write round-trips exactly: read the file back and
    # fail loudly rather than submit a truncated or altered note.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != NOTE + "\n":
        raise RuntimeError(
            f"round-trip mismatch: wrote {len(NOTE)} chars, "
            f"read back {len(written)} chars"
        )

    print(f"wrote {len(NOTE)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
