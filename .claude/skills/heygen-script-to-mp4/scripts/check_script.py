#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Validate a script for HeyGen TTS and produce a filesystem slug.

Input: either inline script text, or a path to a .txt/.md file.
If the argument resolves to an existing file, its contents are read;
otherwise the argument is treated as the script text itself.

Markdown formatting (#, *, >, -, [text](url), ``code``) is stripped so
HeyGen TTS only sees spoken words.

Output: one line on stdout, exit code:
  OK <chars> <slug>  → script fits, exit 0
  TOO_LONG <chars>   → > 1500 chars, exit 2
  EMPTY              → nothing left after cleaning, exit 3

Slug is derived from the first ~6 words of the cleaned script:
ASCII-folded for Vietnamese, lowercase, dashes for spaces.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

MAX_CHARS = 1500
SLUG_WORDS = 6
SLUG_MAX_LEN = 60


def strip_markdown(text: str) -> str:
    # links: [label](url) → label
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # inline code, bold, italic markers
    text = re.sub(r"[`*_~]", "", text)
    # headings & blockquotes & list markers at line start
    text = re.sub(r"^[ \t]*[#>\-+*][ \t]+", "", text, flags=re.MULTILINE)
    # numbered list markers
    text = re.sub(r"^[ \t]*\d+\.[ \t]+", "", text, flags=re.MULTILINE)
    # collapse internal whitespace runs (but keep single newlines as spaces)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slugify(text: str) -> str:
    words = text.split()[:SLUG_WORDS]
    joined = " ".join(words)
    folded = unicodedata.normalize("NFKD", joined)
    ascii_only = folded.encode("ascii", "ignore").decode("ascii")
    ascii_only = re.sub(r"[^a-zA-Z0-9\s-]", "", ascii_only)
    slug = re.sub(r"\s+", "-", ascii_only.strip().lower())
    slug = re.sub(r"-+", "-", slug)
    return slug[:SLUG_MAX_LEN] or "script"


def resolve_input(arg: str) -> str:
    candidate = Path(arg).expanduser()
    if candidate.is_file():
        return candidate.read_text(encoding="utf-8")
    return arg


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_script.py <script_text_or_path>", file=sys.stderr)
        return 64
    raw = resolve_input(sys.argv[1])
    cleaned = strip_markdown(raw)
    if not cleaned:
        print("EMPTY")
        return 3
    char_count = len(cleaned)
    if char_count > MAX_CHARS:
        print(f"TOO_LONG {char_count}")
        return 2
    print(f"OK {char_count} {slugify(cleaned)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
