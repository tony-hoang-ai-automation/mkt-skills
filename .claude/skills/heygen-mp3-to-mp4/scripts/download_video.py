#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Download a finished HeyGen video URL to a local MP4 path.

This is a plain HTTPS download of a URL HeyGen returned via its MCP
get_avatar_video_status response — it does NOT call any HeyGen REST
API to create or modify videos, so it does not violate the skill's
"MCP only for video creation" constraint.

Usage:
  python download_video.py <video_url> <output_path>

Exits non-zero if download fails or response is not a video file.
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

CHUNK = 1 << 16  # 64 KiB


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: download_video.py <video_url> <output_path>", file=sys.stderr)
        return 64

    url, out_str = sys.argv[1], sys.argv[2]
    out = Path(out_str).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    req = urllib.request.Request(url, headers={"User-Agent": "heygen-mp3-to-mp4/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            ctype = resp.headers.get("Content-Type", "")
            if "video" not in ctype and "octet-stream" not in ctype:
                print(f"unexpected content-type: {ctype}", file=sys.stderr)
                return 5
            total = 0
            with open(out, "wb") as fh:
                while True:
                    chunk = resp.read(CHUNK)
                    if not chunk:
                        break
                    fh.write(chunk)
                    total += len(chunk)
    except Exception as exc:
        print(f"download failed: {exc}", file=sys.stderr)
        return 6

    if total < 1024:
        print(f"file suspiciously small: {total} bytes", file=sys.stderr)
        return 7

    print(f"OK {out} {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
