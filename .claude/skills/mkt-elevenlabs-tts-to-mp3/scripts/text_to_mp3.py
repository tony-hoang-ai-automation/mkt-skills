# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "python-dotenv"]
# ///
"""Convert text to MP3 using ElevenLabs Text-to-Speech API.

Flow:
    1. Load ELEVENLABS_API_KEY from project .env
    2. (Optional) Apply pronunciation map — whole-word case-insensitive replacement
       of English terms with Vietnamese-phonetic spellings, so ElevenLabs reads
       them close to the original English instead of as Vietnamese syllables.
       Default map: assets/vn-pronunciation-map.json. Disable with --no-pronounce-map.
    3. POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128
       with xi-api-key header + JSON body { text, model_id, voice_settings }
    4. Stream MP3 bytes from response straight to output file
    5. Print metadata (path, size_mb, char_count, voice_id, model_id, applied substitutions)

Auth: xi-api-key header, key value from env var ELEVENLABS_API_KEY.

Usage:
    uv run scripts/text_to_mp3.py "Your text here" -o output.mp3
    uv run scripts/text_to_mp3.py --file script.txt -o output.mp3
    uv run scripts/text_to_mp3.py --file script.txt --voice_id <ID> --model_id eleven_turbo_v2_5 -o output.mp3
    uv run scripts/text_to_mp3.py --file script.txt --pronounce-map custom.json -o output.mp3
    uv run scripts/text_to_mp3.py --file script.txt --no-pronounce-map -o output.mp3

Default voice:
    Resolved from env var ELEVENLABS_VOICE_ID (set in .env) with fallback K7ewtjKRNtwwt3lKQ6M0
    (Hoang's brand voice). Override at call time with --voice_id.

Char limit:
    ElevenLabs hard-caps a single request at 5000 characters. Text longer than that
    causes an early exit — split semantically (paragraph breaks) and call this script
    per chunk, then concat externally.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parents[4]
load_dotenv(_project_root / ".env")

BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"
FALLBACK_VOICE = "K7ewtjKRNtwwt3lKQ6M0"
DEFAULT_VOICE = os.getenv("ELEVENLABS_VOICE_ID", FALLBACK_VOICE)
DEFAULT_MODEL = "eleven_v3"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"
DEFAULT_STABILITY = 0.5
DEFAULT_SIMILARITY_BOOST = 0.75
DEFAULT_STYLE = 0.0
DEFAULT_SPEAKER_BOOST = True
MAX_CHARS = 5000

DEFAULT_PRONOUNCE_MAP = (
    Path(__file__).resolve().parent.parent / "assets" / "vn-pronunciation-map.json"
)


def _api_key() -> str:
    key = os.getenv("ELEVENLABS_API_KEY")
    if not key:
        print("Error: ELEVENLABS_API_KEY not found in .env", file=sys.stderr)
        sys.exit(1)
    return key


def load_pronunciation_map(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Error: pronunciation map at {path} is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    # Drop comment / metadata keys (anything starting with _)
    return {k: v for k, v in raw.items() if not k.startswith("_") and isinstance(v, str)}


def apply_pronunciation_map(
    text: str, mapping: dict[str, str]
) -> tuple[str, list[tuple[str, str, int]]]:
    """Whole-word case-insensitive substitution. Returns (new_text, [(key, value, count), ...])."""
    if not mapping:
        return text, []
    applied: list[tuple[str, str, int]] = []
    # Process longer keys first so multi-word entries (e.g. "claude code") win over single words
    for key in sorted(mapping.keys(), key=len, reverse=True):
        value = mapping[key]
        pattern = re.compile(r"\b" + re.escape(key) + r"\b", re.IGNORECASE)
        text, count = pattern.subn(value, text)
        if count:
            applied.append((key, value, count))
    return text, applied


def synthesize(
    text: str,
    voice_id: str,
    model_id: str,
    output_format: str,
    stability: float,
    similarity_boost: float,
    style: float,
    use_speaker_boost: bool,
    output_path: Path,
    timeout_s: int = 180,
) -> None:
    url = f"{BASE_URL}/{voice_id}"
    headers = {
        "xi-api-key": _api_key(),
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": style,
            "use_speaker_boost": use_speaker_boost,
        },
    }
    params = {"output_format": output_format}

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with requests.post(
        url, headers=headers, json=payload, params=params, stream=True, timeout=timeout_s
    ) as r:
        if r.status_code >= 400:
            try:
                err_body = r.json()
            except Exception:
                err_body = r.text
            print(f"Error: ElevenLabs returned {r.status_code}: {err_body}", file=sys.stderr)
            sys.exit(1)

        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 15):
                if chunk:
                    f.write(chunk)


def text_to_mp3(
    text: str,
    output_path: str,
    voice_id: str = DEFAULT_VOICE,
    model_id: str = DEFAULT_MODEL,
    output_format: str = DEFAULT_OUTPUT_FORMAT,
    stability: float = DEFAULT_STABILITY,
    similarity_boost: float = DEFAULT_SIMILARITY_BOOST,
    style: float = DEFAULT_STYLE,
    use_speaker_boost: bool = DEFAULT_SPEAKER_BOOST,
    pronunciation_map: dict[str, str] | None = None,
) -> dict:
    out = Path(output_path).expanduser().resolve()

    applied: list[tuple[str, str, int]] = []
    if pronunciation_map:
        text, applied = apply_pronunciation_map(text, pronunciation_map)
        if applied:
            print("Applied pronunciation map:", file=sys.stderr)
            for key, value, count in applied:
                print(f"  {key!r} -> {value!r} ({count}x)", file=sys.stderr)

    char_count = len(text)
    if char_count > MAX_CHARS:
        print(
            f"Error: text is {char_count} chars, exceeds ElevenLabs limit of {MAX_CHARS}.\n"
            f"Split the script semantically (paragraph breaks) and call this script per chunk,\n"
            f"then concat the resulting MP3s with ffmpeg.",
            file=sys.stderr,
        )
        sys.exit(1)
    if char_count == 0:
        print("Error: empty text", file=sys.stderr)
        sys.exit(1)

    print(
        f"Synthesizing ({char_count} chars, voice={voice_id}, model={model_id}, format={output_format})...",
        file=sys.stderr,
    )
    synthesize(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
        stability=stability,
        similarity_boost=similarity_boost,
        style=style,
        use_speaker_boost=use_speaker_boost,
        output_path=out,
    )

    size_mb = out.stat().st_size / (1024 * 1024)
    return {
        "output_path": str(out),
        "size_mb": round(size_mb, 2),
        "char_count": char_count,
        "voice_id": voice_id,
        "model_id": model_id,
        "output_format": output_format,
        "pronunciation_substitutions": [
            {"key": k, "value": v, "count": c} for k, v, c in applied
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser(description="ElevenLabs TTS -> MP3")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("text", nargs="?", help="Text to synthesize")
    src.add_argument("--file", help="Path to .txt file containing text")
    p.add_argument("-o", "--output", required=True, help="Output MP3 path")
    p.add_argument(
        "--voice_id",
        default=DEFAULT_VOICE,
        help=f"ElevenLabs voice ID (default: {DEFAULT_VOICE})",
    )
    p.add_argument(
        "--model_id",
        default=DEFAULT_MODEL,
        help=f"Model ID (default: {DEFAULT_MODEL})",
    )
    p.add_argument(
        "--output_format",
        default=DEFAULT_OUTPUT_FORMAT,
        help=f"Output format (default: {DEFAULT_OUTPUT_FORMAT})",
    )
    p.add_argument(
        "--stability",
        type=float,
        default=DEFAULT_STABILITY,
        help=f"Voice stability 0..1 (default: {DEFAULT_STABILITY})",
    )
    p.add_argument(
        "--similarity_boost",
        type=float,
        default=DEFAULT_SIMILARITY_BOOST,
        help=f"Similarity boost 0..1 (default: {DEFAULT_SIMILARITY_BOOST})",
    )
    p.add_argument(
        "--style",
        type=float,
        default=DEFAULT_STYLE,
        help=f"Style exaggeration 0..1 (default: {DEFAULT_STYLE})",
    )
    p.add_argument(
        "--no_speaker_boost",
        action="store_true",
        help="Disable speaker boost (default: enabled)",
    )
    p.add_argument(
        "--pronounce-map",
        default=str(DEFAULT_PRONOUNCE_MAP),
        help=f"Path to pronunciation map JSON (default: {DEFAULT_PRONOUNCE_MAP})",
    )
    p.add_argument(
        "--no-pronounce-map",
        action="store_true",
        help="Disable pronunciation map substitution",
    )
    args = p.parse_args()

    if args.file:
        text = Path(args.file).expanduser().read_text(encoding="utf-8").strip()
    else:
        text = (args.text or "").strip()

    if args.no_pronounce_map:
        pmap: dict[str, str] = {}
    else:
        pmap = load_pronunciation_map(Path(args.pronounce_map).expanduser())

    result = text_to_mp3(
        text=text,
        output_path=args.output,
        voice_id=args.voice_id,
        model_id=args.model_id,
        output_format=args.output_format,
        stability=args.stability,
        similarity_boost=args.similarity_boost,
        style=args.style,
        use_speaker_boost=not args.no_speaker_boost,
        pronunciation_map=pmap,
    )
    print("OK")
    for k, v in result.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
