---
name: heygen-script-to-mp4
description: Convert a script (Vietnamese or English text) directly into a single HeyGen avatar video — HeyGen handles TTS using the locked ElevenLabs voice, then lip-syncs the avatar. Single-purpose — no MP3 generation, no SRT, no chunking, no Remotion. Uses HeyGen MCP tools exclusively (no direct REST API calls). Avatar look and voice ID are fixed allowlists. USE WHEN user says "tạo video heygen từ script", "script to heygen", "heygen mp4 từ text", "convert script sang heygen video", "tạo avatar video từ script", "heygen text to video", "biến script thành video heygen", or any time the user has script text (not an MP3) and wants exactly one HeyGen avatar MP4 out.
---

# HeyGen Script → MP4 (Single-Purpose, TTS path)

Take a script, return a HeyGen avatar MP4 with HeyGen-synthesized audio. Nothing else.

This is the **TTS sister** of `heygen-mp3-to-mp4`:

| Skill | Input | Voice path |
|---|---|---|
| `heygen-mp3-to-mp4` | pre-recorded MP3 | `voice.type = audio` + `audio_asset_id` |
| `heygen-script-to-mp4` (this) | script text | `voice.type = text` + `voice_id` |

The two paths are mutually exclusive — picking this skill means **no MP3 step at all**; HeyGen runs TTS internally using the locked voice ID.

## Hard constraints

| Constraint | Allowed values |
|---|---|
| HeyGen video creation | **HeyGen MCP only.** Never call HeyGen REST API directly via curl/requests. |
| Avatar look ID | One of: `ff800d7f76aa48f5a23eb6a742ed5365`, `66e75e22e6584bbdaa56a19088286dc8` |
| Voice ID | **Exactly** `fe3f902be2884d1b86ec49c255b3a287`. No other voice ID is permitted under any circumstance. |
| Script length | ≤ 1500 characters per video (HeyGen TTS soft cap). Fail fast if longer. |
| Aspect ratio | 9:16 default (TikTok / Reels) |

The voice ID lock is the whole reason this skill exists — every video produced through it sounds identical to past content.

## Inputs

1. **Script** (required) — either:
   - inline text passed in the conversation, OR
   - path to a `.txt` / `.md` file (skill reads its content; if markdown, strip headings and bullet markers before sending).
2. **Avatar look ID** (optional) — one of the two allowed IDs. If omitted, **pick randomly** from the allowed set so visual variety emerges across runs.
3. **Output path** (optional) — defaults to `workspace/heygen-clips/<script-slug>/<script-slug>_<YYYYMMDD-HHMMSS>.mp4` relative to project root. The slug is derived from the first ~6 words of the script (lowercase, ASCII-folded for Vietnamese, dashes for spaces).

## Workflow

### 1. Resolve and validate the script

If the user gave a file path, read it. Strip markdown formatting (`#`, `*`, `>`, list bullets, link syntax) so HeyGen reads only the spoken words. Trim leading/trailing whitespace.

Validate:
- Non-empty after stripping → otherwise stop and ask user for content.
- `len(script) ≤ 1500` characters → if longer, tell the user the count and that HeyGen TTS works best per-segment under 1500 chars. Suggest splitting into multiple videos manually, or using `mkt-video-script-to-mp3` + `heygen-mp3-to-mp4` for a long-form pipeline. Do not auto-split.

Show the user the cleaned script (first ~200 chars + `...` if longer) before continuing — they should catch typos here, not after the render.

### 2. Pick the avatar look

```python
import random
AVATAR_LOOKS = ["ff800d7f76aa48f5a23eb6a742ed5365", "66e75e22e6584bbdaa56a19088286dc8"]
avatar_id = random.choice(AVATAR_LOOKS)
```

If user named a look, validate it is in the allowlist. Tell the user which look you picked before continuing.

### 3. Generate the avatar video

Call the HeyGen MCP video-creation tool — canonical name **`generate_avatar_video`** (exposed as `mcp__heygen__generate_avatar_video` in the session). Required shape:

```
character:
  type: avatar
  avatar_id: <picked from allowlist>
  scale: 1.0
voice:
  type: text
  input_text: <cleaned script>
  voice_id: fe3f902be2884d1b86ec49c255b3a287
dimension:
  width: 720
  height: 1280     # 9:16
title: "<slug>-<timestamp>"
```

Capture the returned `video_id`.

**Why voice type = text (not audio):** TTS happens inside HeyGen using the locked voice. Sending an `audio_asset_id` here would tell HeyGen to use pre-recorded audio instead, defeating the purpose of this skill.

**Why voice_id is locked:** all videos from this account need to sound like the same person. The constraint is the contract.

### 4. Poll until completed

Call **`get_avatar_video_status`** every ~10 seconds with the `video_id`:

- `processing` / `pending` → keep polling
- `completed` → grab `video_url` from the response and proceed
- `failed` → stop, show the error to the user

Cap the wait at ~10 minutes; if still processing, tell the user and let them decide.

### 5. Download the MP4

Resolve the output path (default: `workspace/heygen-clips/<slug>/<slug>_<timestamp>.mp4` — create parent dirs if needed).

Download via the helper:

```bash
uv run .claude/skills/heygen-script-to-mp4/scripts/download_video.py "<video_url>" "<output_path>"
```

This is a plain HTTPS download of the URL HeyGen returned — not an API call to create or modify a video — so it does not violate the MCP-only constraint.

### 6. Report back

Tell the user in one short reply:

- output path of the MP4
- which avatar look was used
- script char count + estimated speaking duration (rough rule: ~150 chars/15s for Vietnamese TTS at normal pace)
- file size

## Helper scripts

- `scripts/check_script.py` — validate script length and produce a slug. Usage: `uv run .claude/skills/heygen-script-to-mp4/scripts/check_script.py "<script_or_path>"` — prints `OK <chars> <slug>` or `TOO_LONG <chars>` or `EMPTY`.
- `scripts/download_video.py` — same role as in `heygen-mp3-to-mp4`: HTTPS download of the finished MP4 URL.

## Example

User: `tạo video heygen từ script: "Hôm nay mình chia sẻ 3 cách dùng Claude Code để tự động hóa công việc..."`

You:
1. `check_script.py` → `OK 86 hom-nay-minh-chia-se-3`
2. Random pick: `ff800d7f76aa48f5a23eb6a742ed5365`. Say so.
3. `mcp__heygen__generate_avatar_video` (avatar + text + locked voice_id, 720×1280) → `video_id: v_yyy`
4. Poll `mcp__heygen__get_avatar_video_status` every 10s until `completed` → `video_url`
5. `download_video.py <url> workspace/heygen-clips/hom-nay-minh-chia-se-3/hom-nay-minh-chia-se-3_20260429-143022.mp4`
6. Report path, look, char count + ~9s estimated duration, size.

## What this skill deliberately does NOT do

- Does not generate MP3 separately (HeyGen does TTS internally).
- Does not write/transcribe SRT.
- Does not plan visuals, b-roll, segments.
- Does not chunk long scripts.
- Does not compose with Remotion.
- Does not let user pick a different voice — voice ID is locked.

For a long script that needs chunking, suggest: `mkt-video-script-to-mp3` (TTS to MP3) → `heygen-mp3-to-mp4` (per chunk) → manual concat. Or use the multi-segment skill `heygen-short-video`.

## Failure modes & messages

| Symptom | What to tell the user |
|---|---|
| Script empty after cleaning | `Script trống. Cần ít nhất 1 câu để TTS.` |
| Script > 1500 chars | `Script <X> ký tự, vượt ~1500 ký tự khuyến nghị cho 1 video HeyGen TTS. Tách nhỏ hoặc dùng pipeline mp3.` |
| HeyGen MCP not connected | `HeyGen MCP chưa kết nối. Chạy: claude mcp list để kiểm tra.` |
| HeyGen returns failed | `HeyGen render failed: <error>. Có thể voice_id sai hoặc script chứa ký tự HeyGen không xử lý được.` |
| Out of credits | `Hết credit HeyGen. Check qua mcp__heygen__get_remaining_credits.` |
| User asks for a different voice | `Skill này khoá voice_id. Nếu cần voice khác, dùng heygen-mp3-to-mp4 với MP3 đã được TTS bằng voice mong muốn từ trước.` |
