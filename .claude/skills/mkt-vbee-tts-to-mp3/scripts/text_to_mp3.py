# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "python-dotenv"]
# ///
"""Convert text to MP3 using VBee TTS API.

Flow:
    1. POST https://vbee.vn/api/v1/tts with Bearer JWT + app_id + input_text -> returns request_id
    2. Poll GET https://vbee.vn/api/v1/tts/{request_id} until status == "SUCCESS"
    3. Download audio from audio_link
    4. If server returned WAV (fallback), transcode to MP3 via ffmpeg

Auth: Bearer JWT (VBEE_API env) in Authorization header + app_id UUID (VBEE_APP_ID env)
      in request body. Both required.

Usage:
    uv run scripts/text_to_mp3.py "Your text here" -o output.mp3
    uv run scripts/text_to_mp3.py --file script.txt -o output.mp3
    uv run scripts/text_to_mp3.py "Text" --voice_code n_hanoi_male_tuananhnews_news_vc -o output.mp3

Default voice:
    Resolved from env var VOICE_CODE (set in .env) with fallback n_hanoi_male_tuananhnews_news_vc.
    Override at call time with --voice_code.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parents[4]
load_dotenv(_project_root / ".env")

BASE_URL = "https://vbee.vn/api/v1/tts"
# Resolved at CLI-parse time: env var VOICE_CODE wins, else hardcoded fallback.
FALLBACK_VOICE = "n_hanoi_male_tuananhnews_news_vc"
DEFAULT_VOICE = os.getenv("VOICE_CODE", FALLBACK_VOICE)
DEFAULT_BITRATE = 128
DEFAULT_SPEED = "1.0"
DEFAULT_AUDIO_TYPE = "mp3"
# VBee requires callback_url; we use response_type=indirect + polling so a placeholder is fine.
PLACEHOLDER_CALLBACK = "https://example.com/vbee/callback"


def _creds() -> tuple[str, str]:
    jwt = os.getenv("VBEE_API")
    app_id = os.getenv("VBEE_APP_ID")
    if not jwt:
        print("Error: VBEE_API (Bearer JWT) not found in .env", file=sys.stderr)
        sys.exit(1)
    if not app_id:
        print("Error: VBEE_APP_ID (app UUID) not found in .env", file=sys.stderr)
        sys.exit(1)
    return jwt, app_id


def _headers() -> dict:
    jwt, _ = _creds()
    return {"Authorization": f"Bearer {jwt}", "Content-Type": "application/json"}


def submit_tts(
    text: str,
    voice_code: str,
    audio_type: str,
    bitrate: int,
    speed_rate: str,
    callback_url: str,
) -> str:
    _, app_id = _creds()
    payload = {
        "app_id": app_id,
        "response_type": "indirect",
        "callback_url": callback_url,
        "input_text": text,
        "voice_code": voice_code,
        "audio_type": audio_type,
        "bitrate": bitrate,
        "speed_rate": speed_rate,
    }
    r = requests.post(BASE_URL, headers=_headers(), json=payload, timeout=60)
    if r.status_code >= 400:
        print(f"Error submitting TTS ({r.status_code}): {r.text}", file=sys.stderr)
        sys.exit(1)
    data = r.json()
    result = data.get("result") or {}
    request_id = result.get("request_id")
    if not request_id:
        print(f"Error: no request_id in response: {data}", file=sys.stderr)
        sys.exit(1)
    return request_id


def poll_until_ready(request_id: str, timeout_s: int = 600, interval_s: float = 3.0) -> tuple[str, str]:
    """Return (audio_link, audio_type_actual)."""
    deadline = time.time() + timeout_s
    last_status = None
    while time.time() < deadline:
        r = requests.get(f"{BASE_URL}/{request_id}", headers=_headers(), timeout=30)
        if r.status_code >= 400:
            print(f"Poll error ({r.status_code}): {r.text}", file=sys.stderr)
            sys.exit(1)
        result = r.json().get("result") or {}
        status = (result.get("status") or "").upper()
        if status != last_status:
            print(f"  status: {status or 'PENDING'}", file=sys.stderr)
            last_status = status
        if status == "SUCCESS":
            link = result.get("audio_link")
            if not link:
                print(f"Error: SUCCESS but no audio_link: {result}", file=sys.stderr)
                sys.exit(1)
            return link, (result.get("audio_type") or "").lower()
        if status in ("FAILED", "ERROR", "FAILURE"):
            print(f"Error: TTS job failed: {result}", file=sys.stderr)
            sys.exit(1)
        time.sleep(interval_s)
    print(f"Error: polling timed out after {timeout_s}s", file=sys.stderr)
    sys.exit(1)


def download(url: str, dest: Path) -> None:
    with requests.get(url, stream=True, timeout=180) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 15):
                if chunk:
                    f.write(chunk)


def transcode_to_mp3(src: Path, mp3_path: Path, bitrate_kbps: int = 192) -> None:
    if not shutil.which("ffmpeg"):
        print("Error: ffmpeg not found on PATH. Install via `brew install ffmpeg`.", file=sys.stderr)
        sys.exit(1)
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(src),
        "-codec:a", "libmp3lame", "-b:a", f"{bitrate_kbps}k",
        str(mp3_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)


def text_to_mp3(
    text: str,
    output_path: str,
    voice_code: str = DEFAULT_VOICE,
    bitrate: int = DEFAULT_BITRATE,
    speed_rate: str = DEFAULT_SPEED,
    audio_type: str = DEFAULT_AUDIO_TYPE,
    callback_url: str = PLACEHOLDER_CALLBACK,
    keep_source: bool = False,
) -> dict:
    out = Path(output_path).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    print(f"Submitting VBee TTS ({len(text)} chars, voice={voice_code}, type={audio_type})...", file=sys.stderr)
    request_id = submit_tts(text, voice_code, audio_type, bitrate, speed_rate, callback_url)
    print(f"request_id = {request_id}", file=sys.stderr)

    print("Polling for completion...", file=sys.stderr)
    audio_link, actual_type = poll_until_ready(request_id)
    print(f"audio_link = {audio_link}", file=sys.stderr)
    print(f"actual audio_type = {actual_type}", file=sys.stderr)

    with tempfile.TemporaryDirectory() as tmp:
        src_ext = actual_type or Path(audio_link).suffix.lstrip(".") or "mp3"
        src_path = Path(tmp) / f"vbee-{request_id}.{src_ext}"
        print(f"Downloading {src_ext.upper()}...", file=sys.stderr)
        download(audio_link, src_path)

        if src_ext == "mp3" and out.suffix.lower() == ".mp3":
            shutil.copy2(src_path, out)
        else:
            print(f"Transcoding {src_ext.upper()} -> MP3 (192k)...", file=sys.stderr)
            transcode_to_mp3(src_path, out)

        if keep_source and src_ext != "mp3":
            kept = out.with_suffix(f".{src_ext}")
            shutil.copy2(src_path, kept)
            print(f"Kept source {src_ext.upper()} at {kept}", file=sys.stderr)

    size_mb = out.stat().st_size / (1024 * 1024)
    return {
        "request_id": request_id,
        "audio_link": audio_link,
        "output_path": str(out),
        "size_mb": round(size_mb, 2),
        "char_count": len(text),
        "voice_code": voice_code,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="VBee TTS -> MP3")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("text", nargs="?", help="Text to synthesize")
    src.add_argument("--file", help="Path to .txt file containing text")
    p.add_argument("-o", "--output", required=True, help="Output MP3 path")
    p.add_argument("--voice_code", default=DEFAULT_VOICE, help=f"VBee voice code (default: {DEFAULT_VOICE})")
    p.add_argument("--bitrate", type=int, default=DEFAULT_BITRATE, help="Bitrate (kbps). VBee supports 128.")
    p.add_argument("--speed_rate", default=DEFAULT_SPEED, help="Speech speed rate (default: 1.0)")
    p.add_argument("--audio_type", default=DEFAULT_AUDIO_TYPE, choices=["mp3", "wav"])
    p.add_argument("--callback_url", default=PLACEHOLDER_CALLBACK)
    p.add_argument("--keep_source", action="store_true", help="Keep original file when server returns non-MP3")
    args = p.parse_args()

    if args.file:
        text = Path(args.file).expanduser().read_text(encoding="utf-8").strip()
    else:
        text = args.text.strip()
    if not text:
        print("Error: empty text", file=sys.stderr)
        sys.exit(1)

    result = text_to_mp3(
        text=text,
        output_path=args.output,
        voice_code=args.voice_code,
        bitrate=args.bitrate,
        speed_rate=args.speed_rate,
        audio_type=args.audio_type,
        callback_url=args.callback_url,
        keep_source=args.keep_source,
    )
    print("OK")
    for k, v in result.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
