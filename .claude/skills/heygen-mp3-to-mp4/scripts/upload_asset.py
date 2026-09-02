#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.31"]
# ///
"""
Upload an audio file to HeyGen as an asset and return the asset_id.

API version: **v3** — `POST https://api.heygen.com/v3/assets` (multipart, field
`file`) → `{"data": {"asset_id": "...", "url": "...", ...}}`.

The legacy endpoint `POST https://upload.heygen.com/v1/asset` (raw binary body,
response `data.id`) still works but sits in HeyGen's v1/v2 legacy bucket, which
carries `deprecation: true` + `sunset: Sat, 31 Oct 2026 00:00:00 GMT` response
headers. Pass `--legacy` to force it only if v3 is unavailable for your account.

The HeyGen MCP server exposes no asset-upload tool (`create_video_from_avatar`,
`get_video`, … only), so this REST helper is the supported upload path.

Usage:
    uv run upload_asset.py <mp3_path> [--key-file PATH] [--legacy] [--quiet]

Outputs (stdout, one line):
    OK <asset_id>

Exit codes:
    0 — upload succeeded
    1 — file missing / api error / no api key

The API key is read from (in order):
    1. --key-file flag
    2. HEYGEN_API_KEY env var
    3. .env.local / .env in current dir
    4. ~/Documents/GitHub/hoang-ai-marketing/.env (canonical fallback for the
       Hoang marketing setup — placeholder keys like `your_*` are skipped)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import requests

V3_ENDPOINT = "https://api.heygen.com/v3/assets"
LEGACY_ENDPOINT = "https://upload.heygen.com/v1/asset"
DEFAULT_KEY_FILES = [
    Path(".env.local"),
    Path(".env"),
    Path.home() / "Documents" / "GitHub" / "hoang-ai-marketing" / ".env",
]


def _read_key_from_env_file(path: Path) -> str | None:
    if not path.exists():
        return None
    for line in path.read_text().splitlines():
        m = re.match(r'^\s*HEYGEN_API_KEY\s*=\s*"?([^"\s#]+)"?\s*$', line)
        if not m:
            continue
        val = m.group(1).strip()
        # Skip placeholder stubs
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


def content_type_for(path: Path) -> str:
    ext = path.suffix.lower()
    return {
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".m4a": "audio/mp4",
        ".aac": "audio/aac",
        ".ogg": "audio/ogg",
        ".mp4": "video/mp4",
        ".mov": "video/quicktime",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }.get(ext, "application/octet-stream")


def _fail(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)


def upload_v3(path: Path, api_key: str, quiet: bool) -> str:
    ctype = content_type_for(path)
    if not quiet:
        print(f"[upload] POST {V3_ENDPOINT} ({path.name}, {ctype})", file=sys.stderr)
    with path.open("rb") as fh:
        resp = requests.post(
            V3_ENDPOINT,
            headers={"X-Api-Key": api_key},
            files={"file": (path.name, fh, ctype)},
            timeout=180,
        )
    try:
        body = resp.json()
    except Exception:
        body = {"raw": resp.text[:500]}
    if resp.status_code >= 400:
        _fail(f"ERROR status={resp.status_code} body={body}")
    asset_id = (body.get("data") or {}).get("asset_id") or (body.get("data") or {}).get("id")
    if not asset_id:
        _fail(f"ERROR missing asset id in v3 response: {body}")
    return asset_id


def upload_legacy(path: Path, api_key: str, quiet: bool) -> str:
    ctype = content_type_for(path)
    if not quiet:
        print(
            f"[upload] POST {LEGACY_ENDPOINT} ({path.name}, {ctype}) "
            "— legacy v1 endpoint, sunset 2026-10-31",
            file=sys.stderr,
        )
    resp = requests.post(
        LEGACY_ENDPOINT,
        headers={"X-Api-Key": api_key, "Content-Type": ctype},
        data=path.read_bytes(),
        timeout=180,
    )
    try:
        body = resp.json()
    except Exception:
        body = {"raw": resp.text[:500]}
    if resp.status_code >= 400 or body.get("code", 100) != 100:
        _fail(f"ERROR status={resp.status_code} body={body}")
    asset_id = (body.get("data") or {}).get("id")
    if not asset_id:
        _fail(f"ERROR missing asset id in legacy response: {body}")
    return asset_id


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mp3_path", help="Path to the audio file to upload")
    ap.add_argument(
        "--key-file",
        help="Path to a .env-format file containing HEYGEN_API_KEY",
        default=None,
    )
    ap.add_argument(
        "--legacy",
        action="store_true",
        help="Force the deprecated v1 upload endpoint (sunset 2026-10-31)",
    )
    ap.add_argument("--quiet", "-q", action="store_true")
    args = ap.parse_args()

    api_key = resolve_api_key(args.key_file)
    if not api_key:
        _fail(
            "ERROR HEYGEN_API_KEY not found. Set env var, --key-file, or add a real "
            "key to .env.local / .env / ~/Documents/GitHub/hoang-ai-marketing/.env "
            "(placeholder stubs starting with 'your_' are skipped)."
        )

    mp3_path = Path(args.mp3_path).expanduser().resolve()
    if not mp3_path.exists():
        _fail(f"MISSING {mp3_path}")

    if args.legacy:
        asset_id = upload_legacy(mp3_path, api_key, args.quiet)
    else:
        asset_id = upload_v3(mp3_path, api_key, args.quiet)
    print(f"OK {asset_id}")


if __name__ == "__main__":
    main()
