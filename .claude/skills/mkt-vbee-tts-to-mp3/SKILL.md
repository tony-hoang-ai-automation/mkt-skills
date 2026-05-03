---
name: mkt-vbee-tts-to-mp3
description: Convert Vietnamese/English text to MP3 voiceover using VBee TTS API. Submits text-to-speech job, polls until done, downloads audio, auto-transcodes to MP3 via ffmpeg if server returns WAV. USE WHEN user says 'tạo mp3 vbee', 'vbee tts', 'text to speech vbee', 'tạo voiceover vbee', 'đọc text bằng vbee', 'tts vbee to mp3', 'giọng ngọc huyền', 'giọng mai phương', 'giọng minh hoàng vbee', 'giọng tuấn anh vbee'.
---

# VBee TTS to MP3

Convert text to MP3 voiceover using VBee TTS (https://vbee.vn/api/v1/tts).

## Defaults

- **Voice code**: `n_hanoi_male_tuananhnews_news_vc` (Hà Nội nam — Tuấn Anh, news) — overridable via `VOICE_CODE` env in `.env`, or `--voice_code` at call time
- **Audio type**: `mp3` (server also supports `wav`)
- **Bitrate**: `128`
- **Speed rate**: `1.0` (string)
- **Language**: auto (VN/EN via voice code)

## Quick Usage

### From file
```bash
uv run .claude/skills/mkt-vbee-tts-to-mp3/scripts/text_to_mp3.py \
  --file path/to/script.txt \
  -o workspace/content/YYYY-MM-DD/voiceover.mp3
```

### From inline text
```bash
uv run .claude/skills/mkt-vbee-tts-to-mp3/scripts/text_to_mp3.py \
  "Xin chào các bạn, hôm nay mình chia sẻ về AI Agent" \
  -o workspace/assets/vbee/sample.mp3
```

### Custom voice / speed
```bash
uv run .claude/skills/mkt-vbee-tts-to-mp3/scripts/text_to_mp3.py \
  --file script.txt \
  --voice_code sg_male_minhhoang_news_48k-thg \
  --speed_rate 1.1 \
  -o output.mp3
```

### Keep source file when API returns WAV
```bash
uv run .claude/skills/mkt-vbee-tts-to-mp3/scripts/text_to_mp3.py \
  --file script.txt --keep_source -o output.mp3
```

## Workflow

1. `POST https://vbee.vn/api/v1/tts` with body:
   ```json
   {
     "app_id": "<VBEE_API from .env>",
     "response_type": "indirect",
     "callback_url": "https://example.com/vbee/callback",
     "input_text": "...",
     "voice_code": "n_hanoi_male_tuananhnews_news_vc",
     "audio_type": "mp3",
     "bitrate": 128,
     "speed_rate": "1.0"
   }
   ```
   → returns `request_id` with `status: IN_PROGRESS`
2. Poll `GET https://vbee.vn/api/v1/tts/{request_id}` every 3s until `status == "SUCCESS"` (timeout 600s)
3. Download audio from `audio_link`
4. If server returns MP3 → copy to output path directly
5. If server returns WAV → transcode to MP3 via ffmpeg (`libmp3lame`, `-b:a 192k`)
6. Print `request_id`, `audio_link`, `output_path`, `size_mb`, `char_count`, `voice_code`

**Note**: VBee requires `callback_url` field in the body. We set `response_type: "indirect"` and rely on polling, so a placeholder URL is fine — no callback server needed.

## Common Voice Codes

| Code | Region / Voice |
|------|----------------|
| `n_hanoi_male_tuananhnews_news_vc` | Hà Nội — nam (Tuấn Anh, news) ← default |
| `hn_female_ngochuyen_full_48k-fhg` | Hà Nội — nữ (Ngọc Huyền, full) |
| `hn_female_ngochuyen_news_48k-thg` | Hà Nội — nữ (Ngọc Huyền, news) |
| `hn_female_maiphuong_vdts_48k-fhg` | Hà Nội — nữ (Mai Phương) |
| `hue_female_huonggiang_news_48k-thg` | Huế — nữ (Hương Giang) |
| `sg_male_minhhoang_news_48k-thg` | Sài Gòn — nam (Minh Hoàng) |

Full voice catalog: https://studio.vbee.vn

## Output Convention

- Short/test: `workspace/assets/vbee/<name>.mp3`
- Video production: `workspace/content/YYYY-MM-DD/video-short/<project>/voiceover.mp3`

## Requirements

- `VBEE_API` in project `.env` (app_id UUID; sent inside request body — **not** as header)
- `ffmpeg` on PATH — only needed when API returns WAV (macOS: `brew install ffmpeg`)
- Python deps managed via PEP 723 inline metadata (auto-installed by `uv run`)

## API Reference

- Postman docs: https://documenter.getpostman.com/view/12951168/Uz5FHbSd
- Submit endpoint: `POST https://vbee.vn/api/v1/tts`
- Status endpoint: `GET https://vbee.vn/api/v1/tts/{request_id}`
- Auth: `app_id` in JSON body (no Authorization header)
- Status values: `IN_PROGRESS` → `SUCCESS` | `FAILED`
- Response modes: `indirect` (async + polling) | `direct` (sync wait)
