#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Check an MP3 file exists and is ≤ 300 seconds.

Prints one line:
  OK <seconds>          → file fine, exit 0
  TOO_LONG <seconds>    → file > 300s, exit 2
  MISSING               → file not found, exit 3
  PROBE_FAILED <reason> → ffprobe could not read it, exit 4

Used by the heygen-mp3-to-mp4 skill before uploading to HeyGen.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HEYGEN_MAX_SECONDS = 300.0


def probe_duration(path: Path) -> float:
    if not shutil.which("ffprobe"):
        raise RuntimeError("ffprobe not found on PATH (install ffmpeg)")
    out = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(out.stdout.strip())


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_duration.py <mp3_path>", file=sys.stderr)
        return 64
    path = Path(sys.argv[1]).expanduser()
    if not path.is_file():
        print("MISSING")
        return 3
    try:
        seconds = probe_duration(path)
    except Exception as exc:
        print(f"PROBE_FAILED {exc}")
        return 4
    if seconds > HEYGEN_MAX_SECONDS:
        print(f"TOO_LONG {seconds:.1f}")
        return 2
    print(f"OK {seconds:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
