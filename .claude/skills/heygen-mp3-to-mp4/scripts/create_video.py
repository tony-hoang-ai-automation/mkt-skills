#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.31"]
# ///
"""
REST fallback for HeyGen avatar-video creation + status polling — **v3 only**.

Primary path stays the HeyGen MCP (`mcp__heygen__create_video_from_avatar` +
`mcp__heygen__get_video`). Use this script when the MCP is unauthenticated,
unavailable, or its tool surface changed under you.

Endpoints (current, non-legacy):
    POST https://api.heygen.com/v3/videos          → {"data": {"video_id", "status"}}
    GET  https://api.heygen.com/v3/videos/<id>     → {"data": {"status", "video_url", ...}}

Never call `POST /v2/video/generate` or `POST /v1/video.generate`: those carry
`deprecation: true` + `sunset: Sat, 31 Oct 2026 00:00:00 GMT` headers and stop
working after 2026-10-31.

Usage:
    # create (audio lip-sync from an uploaded asset)
    uv run create_video.py --avatar-id <id> --audio-asset-id <id> \
        [--aspect-ratio 9:16] [--resolution 720p] [--engine avatar_v] \
        [--title "slug-timestamp"] [--wait] [--timeout 900]

    # poll an existing video
    uv run create_video.py --status <video_id>

Outputs (stdout, one line):
    OK <video_id>                 (create without --wait)
    OK <video_id> <video_url>     (create --wait, or --status once completed)
    PENDING <video_id> <status>   (--status while still rendering)

Exit codes: 0 ok · 1 api/credit/render error · 2 still pending (--status) · 4 timeout
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import requests

BASE = "https://api.heygen.com/v3/videos"
DEFAULT_KEY_FILES = [
    Path(".env.local"),
    Path(".env"),
    Path.home() / "Documents" / "GitHub" / "hoang-ai-marketing" / ".env",
]
TERMINAL_OK = {"completed", "success", "done"}
TERMINAL_BAD = {"failed", "error", "canceled", "cancelled"}


def _read_key_from_env_file(path: Path) -> str | None:
    if not path.exists():
        return None
    for line in path.read_text().splitlines():
        m = re.match(r'^\s*HEYGEN_API_KEY\s*=\s*"?([^"\s#]+)"?\s*$', line)
        if not m:
            continue
        val = m.group(1).strip()
        if val.startswith("your_") or "placeholder" in val.lower() or val == "":
            continue
        return val
    return None


def resolve_api_key(explicit: str | None) -> str | None:
    if explicit:
        return _read_key_from_env_file(Path(explicit)) or explicit
    if env := os.environ.get("HEYGEN_API_KEY", "").strip():
        if not env.startswith("your_") and "placeholder" not in env.lower():
            return env
    for p in DEFAULT_KEY_FILES:
        if val := _read_key_from_env_file(p):
            return val
    return None


def _fail(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    sys.exit(code)


def _json(resp: requests.Response) -> dict:
    try:
        return resp.json()
    except Exception:
        return {"raw": resp.text[:500]}


def create(args: argparse.Namespace, api_key: str) -> str:
    payload: dict = {
        "type": "avatar",
        "avatar_id": args.avatar_id,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
    }
    if args.audio_asset_id:
        payload["audio_asset_id"] = args.audio_asset_id
    elif args.audio_url:
        payload["audio_url"] = args.audio_url
    else:
        _fail("ERROR need --audio-asset-id or --audio-url (this skill never uses TTS)")
    if args.engine != "default":
        # Avatar V rejects expressiveness / motionPrompt — we never send them.
        payload["engine"] = {"type": args.engine}
    if args.title:
        payload["title"] = args.title
    if args.callback_url:
        payload["callback_url"] = args.callback_url

    if not args.quiet:
        print(f"[create] POST {BASE} {json.dumps(payload)}", file=sys.stderr)
    resp = requests.post(
        BASE,
        headers={"X-Api-Key": api_key, "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    body = _json(resp)
    if resp.status_code >= 400:
        err = body.get("error") or body
        _fail(f"ERROR status={resp.status_code} body={err}")
    video_id = (body.get("data") or {}).get("video_id") or (body.get("data") or {}).get("id")
    if not video_id:
        _fail(f"ERROR missing video_id in response: {body}")
    return video_id


def fetch(video_id: str, api_key: str) -> dict:
    resp = requests.get(
        f"{BASE}/{video_id}", headers={"X-Api-Key": api_key}, timeout=60
    )
    body = _json(resp)
    if resp.status_code >= 400:
        _fail(f"ERROR status={resp.status_code} body={body.get('error') or body}")
    return body.get("data") or {}


def wait(video_id: str, api_key: str, timeout: int, interval: int, quiet: bool) -> str:
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = fetch(video_id, api_key)
        state = str(data.get("status", "")).lower()
        if state in TERMINAL_OK:
            url = data.get("video_url") or data.get("url")
            if not url:
                _fail(f"ERROR completed but no video_url: {data}")
            return url
        if state in TERMINAL_BAD:
            _fail(f"ERROR render {state}: {data.get('failure_message') or data}")
        if not quiet:
            print(f"[poll] {video_id} → {state or 'unknown'}", file=sys.stderr)
        time.sleep(interval)
    _fail(f"TIMEOUT {video_id} still rendering after {timeout}s", 4)
    return ""  # unreachable


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--status", metavar="VIDEO_ID", help="Poll one video and exit")
    ap.add_argument("--avatar-id")
    ap.add_argument("--audio-asset-id")
    ap.add_argument("--audio-url")
    ap.add_argument("--aspect-ratio", default="9:16",
                    choices=["9:16", "16:9", "4:5", "5:4", "1:1", "auto"])
    ap.add_argument("--resolution", default="720p", choices=["720p", "1080p", "4k"])
    ap.add_argument("--engine", default="avatar_v",
                    choices=["avatar_v", "avatar_iv", "avatar_iii", "default"],
                    help="'default' omits the engine field (HeyGen picks Avatar IV)")
    ap.add_argument("--title")
    ap.add_argument("--callback-url")
    ap.add_argument("--wait", action="store_true", help="Poll until completed")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--interval", type=int, default=15)
    ap.add_argument("--key-file")
    ap.add_argument("--quiet", "-q", action="store_true")
    args = ap.parse_args()

    api_key = resolve_api_key(args.key_file)
    if not api_key:
        _fail("ERROR HEYGEN_API_KEY not found (env / --key-file / .env.local / .env).")

    if args.status:
        data = fetch(args.status, api_key)
        state = str(data.get("status", "")).lower()
        if state in TERMINAL_OK:
            print(f"OK {args.status} {data.get('video_url') or data.get('url')}")
            return
        if state in TERMINAL_BAD:
            _fail(f"ERROR render {state}: {data.get('failure_message') or data}")
        print(f"PENDING {args.status} {state or 'unknown'}")
        sys.exit(2)

    if not args.avatar_id:
        _fail("ERROR --avatar-id required (or use --status <video_id>)")
    video_id = create(args, api_key)
    if not args.wait:
        print(f"OK {video_id}")
        return
    url = wait(video_id, api_key, args.timeout, args.interval, args.quiet)
    print(f"OK {video_id} {url}")


if __name__ == "__main__":
    main()
