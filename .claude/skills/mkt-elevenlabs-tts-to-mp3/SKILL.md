---
name: mkt-elevenlabs-tts-to-mp3
description: Convert Vietnamese/English script text to MP3 voiceover using ElevenLabs TTS API. Calls POST /v1/text-to-speech/{voice_id}, streams audio bytes, writes MP3 directly. Locked to Hoang's brand voice ID by default. USE WHEN user says 'tạo mp3 elevenlabs', 'elevenlabs tts', 'eleven labs voice', 'text to speech elevenlabs', 'tạo voiceover elevenlabs', 'đọc text bằng elevenlabs', 'tts elevenlabs to mp3', 'eleven labs script to mp3', 'voiceover bằng elevenlabs', 'giọng elevenlabs'.
---

# ElevenLabs TTS to MP3

Convert script text to MP3 voiceover via ElevenLabs Text-to-Speech API.

## Defaults

- **Voice ID**: `K7ewtjKRNtwwt3lKQ6M0` (Hoang's brand voice — locked) — overridable via `ELEVENLABS_VOICE_ID` env or `--voice_id`
- **Model**: `eleven_v3` (most expressive, supports audio tags like [excited], [whisper], [laugh]; best for storytelling content) — overridable via `--model_id`. Alternatives: `eleven_multilingual_v2` (high quality, slower), `eleven_turbo_v2_5` (fast, slightly flat), `eleven_flash_v2_5` (fastest)
- **Output format**: `mp3_44100_128` (44.1 kHz / 128 kbps) — overridable via `--output_format`
- **Voice settings**: `stability=0.5`, `similarity_boost=0.75`, `style=0`, `use_speaker_boost=true` (ElevenLabs defaults)
- **Pronunciation map**: auto-loaded from `assets/vn-pronunciation-map.json` — disable with `--no-pronounce-map`, or point at a different file with `--pronounce-map path.json`
- **Char limit**: 5000 per request (ElevenLabs hard limit). Text > 5000 chars → script exits with error and asks user to split manually.

## Quick Usage

### From file
```bash
uv run .claude/skills/mkt-elevenlabs-tts-to-mp3/scripts/text_to_mp3.py \
  --file path/to/script.txt \
  -o workspace/content/YYYY-MM-DD/voiceover.mp3
```

### From inline text
```bash
uv run .claude/skills/mkt-elevenlabs-tts-to-mp3/scripts/text_to_mp3.py \
  "Xin chào các bạn, hôm nay mình chia sẻ về AI Agent" \
  -o workspace/assets/elevenlabs/sample.mp3
```

### Custom voice / model
```bash
uv run .claude/skills/mkt-elevenlabs-tts-to-mp3/scripts/text_to_mp3.py \
  --file script.txt \
  --voice_id K7ewtjKRNtwwt3lKQ6M0 \
  --model_id eleven_turbo_v2_5 \
  -o output.mp3
```

### Tweak voice expressiveness
```bash
uv run .claude/skills/mkt-elevenlabs-tts-to-mp3/scripts/text_to_mp3.py \
  --file script.txt \
  --stability 0.4 \
  --similarity_boost 0.8 \
  --style 0.2 \
  -o output.mp3
```

## Voice settings — when to tweak

| Setting | Range | Effect |
|---------|-------|--------|
| `stability` | 0.0–1.0 | Higher = more monotone/predictable; lower = more emotional/variable. **0.5 is the sweet spot** for narration. Drop to 0.3–0.4 for casual hooks; raise to 0.7+ for formal explainers. |
| `similarity_boost` | 0.0–1.0 | How closely to clone the reference voice. **0.75 default**. Raise toward 0.9 if voice sounds "off" from the original. |
| `style` | 0.0–1.0 | Style exaggeration. **0 default**. Adds latency when > 0. Useful (0.1–0.3) for expressive content. |
| `use_speaker_boost` | bool | Sharpens speaker similarity. Keep `true` for brand voice consistency. |

## Pronunciation Map (English-word fix)

ElevenLabs multilingual models try to read the *whole* text in the dominant language. In a Vietnamese script, English words like `doc`, `chat`, `git` get pronounced as Vietnamese syllables and sound wrong. To fix this without hand-editing every script, the skill auto-loads a **whole-word case-insensitive substitution map** from `assets/vn-pronunciation-map.json` and applies it before sending text to the API.

Default mapping:
```json
{
  "doc": "đóc",
  "chat": "chát",
  "git": "gít"
}
```

**How it works**: each key is matched case-insensitively with `\b...\b` boundaries, then replaced with the Vietnamese-phonetic value. The model sees "đóc" instead of "doc" and pronounces it close to /dɒk/. This only affects audio — your source script stays clean.

**Curating the dictionary** — listen first, add second:
- Run the skill on a short test script containing the candidate word
- If the model already reads it correctly, **don't add it** (overfitting will break things)
- Watch out for collisions: adding `"code"` would also rewrite the `Code` in `Claude Code` (brand name) → never do that
- For brand names that need protecting, leave them out entirely

**Override / disable**:
```bash
# Use a custom map for a specific project
uv run scripts/text_to_mp3.py --file s.txt --pronounce-map workspace/.../map.json -o out.mp3

# Skip the substitution entirely
uv run scripts/text_to_mp3.py --file s.txt --no-pronounce-map -o out.mp3
```

The script prints every applied substitution to stderr (e.g. `'doc' -> 'đóc' (4x)`) so you can verify what changed.

## Workflow

1. Load `ELEVENLABS_API_KEY` from project `.env`
2. Read text from `--file` or positional arg, strip whitespace
3. Apply pronunciation map (unless `--no-pronounce-map`) — whole-word case-insensitive replacement
4. Validate `len(text) <= 5000`
5. `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128`
   - Header: `xi-api-key: <key>`, `Content-Type: application/json`, `Accept: audio/mpeg`
   - Body:
     ```json
     {
       "text": "...",
       "model_id": "eleven_v3",
       "voice_settings": {
         "stability": 0.5,
         "similarity_boost": 0.75,
         "style": 0,
         "use_speaker_boost": true
       }
     }
     ```
4. Stream audio bytes directly to output MP3 (no transcoding needed — server returns MP3)
5. Print `output_path`, `size_mb`, `char_count`, `voice_id`, `model_id`

## Output Convention

- Short/test: `workspace/assets/elevenlabs/<name>.mp3`
- Video production: `workspace/content/YYYY-MM-DD/video-short/<project>/voiceover.mp3`

## Requirements

- `ELEVENLABS_API_KEY` in project `.env` (header auth: `xi-api-key`)
- Optional `ELEVENLABS_VOICE_ID` in `.env` to lock a different default voice
- Python deps managed via PEP 723 inline metadata (auto-installed by `uv run`): `requests`, `python-dotenv`
- No `ffmpeg` needed — ElevenLabs returns MP3 directly

## Why no chunking

ElevenLabs limits requests to 5000 characters. The skill **fails fast** above that limit instead of auto-splitting because:
- A single voiceover should be a coherent chunk — splitting mid-script causes prosody jumps at concat boundaries
- The user's content (hooks, short scripts, video segments) typically fits well under 5000 chars
- If the user genuinely needs longer audio, they should split the script semantically (paragraph breaks) and call this skill per chunk, then concat with ffmpeg in their own pipeline

## API Reference

- Endpoint: `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`
- Auth: `xi-api-key: <api_key>` header
- Model catalog: https://elevenlabs.io/docs/models
- Voice catalog (browse / get voice IDs): https://elevenlabs.io/app/voice-library
- API docs: https://elevenlabs.io/docs/api-reference/text-to-speech/convert
- Rate limits: depend on subscription tier — see https://elevenlabs.io/pricing
- Output formats: `mp3_44100_128` (default), `mp3_44100_192` (higher quality, paid only), `pcm_44100`, `ulaw_8000` (telephony)
