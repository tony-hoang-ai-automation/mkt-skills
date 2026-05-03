---
name: heygen-mp3-to-mp4
description: Convert a single MP3 voiceover file into a single HeyGen avatar lip-sync MP4 video. Single-purpose — no planning, no SRT, no chunking, no Remotion compositing. Uses HeyGen MCP tools exclusively (no direct REST API calls). Locks avatar look and voice ID to a fixed allowlist. USE WHEN user says "tạo video heygen từ mp3", "mp3 to heygen", "heygen mp4 từ audio", "convert mp3 sang heygen video", "tạo avatar video từ file mp3", "lip sync mp3 heygen", "biến mp3 thành video heygen", or any time the user has exactly one MP3 file and wants exactly one HeyGen avatar MP4 out.
---

# HeyGen MP3 → MP4 (Single-Purpose)

Take one MP3 voiceover, return one HeyGen avatar lip-sync MP4. Nothing else.

This skill exists because the existing `heygen-short-video` skill requires a full production plan + SRT + chunked segments — overkill when the user just has a finished voiceover and wants a talking-head video.

## Hard constraints

These are non-negotiable. Reject the request if any cannot be honored.

| Constraint | Allowed values |
|---|---|
| HeyGen video creation | **HeyGen MCP only.** Never call `https://api.heygen.com/...` via curl/requests for video generation. |
| Avatar look ID | One of: `ff800d7f76aa48f5a23eb6a742ed5365`, `66e75e22e6584bbdaa56a19088286dc8` |
| Voice ID (only if MCP path forces TTS) | `fe3f902be2884d1b86ec49c255b3a287` (no other voice ID is permitted) |
| MP3 duration | ≤ 300 seconds (5 minutes). Fail fast if longer; do **not** auto-split. |
| Aspect ratio | 9:16 default (TikTok / Reels) |

For MP3 lip-sync the voice type is `audio` and `audio_asset_id` is provided — voice_id is **not** sent. The voice_id allowlist above only matters if a future MCP signature requires one.

## Inputs

1. **MP3 path** (required) — absolute path to the voiceover file.
2. **Avatar look ID** (optional) — one of the two allowed IDs. If omitted, **pick randomly** from the allowed set so visual variety emerges across runs.
3. **Output path** (optional) — defaults to `workspace/heygen-clips/<mp3-stem>/<mp3-stem>_<YYYYMMDD-HHMMSS>.mp4` relative to the project root.

## Workflow

Follow these steps in order. Each step has a stop condition; do not proceed past a failed step.

### 1. Validate the MP3

Run the duration check helper:

```bash
uv run .claude/skills/heygen-mp3-to-mp4/scripts/check_duration.py "<mp3_path>"
```

The script prints one line: `OK <seconds>` or `TOO_LONG <seconds>` or `MISSING`. Exit code 0 = OK, non-zero = stop.

If `TOO_LONG`: tell the user the duration and that HeyGen caps a single video at ~5 min, and suggest the existing `heygen-short-video` skill (which chunks). Do not proceed.

### 2. Pick the avatar look

If the user named a look, validate it is in the allowlist. If not (or none specified), pick randomly:

```python
import random
AVATAR_LOOKS = ["ff800d7f76aa48f5a23eb6a742ed5365", "66e75e22e6584bbdaa56a19088286dc8"]
avatar_id = random.choice(AVATAR_LOOKS)
```

Tell the user which look you picked before continuing — they may want to override.

### 3. Upload the MP3 as a HeyGen asset

Use the HeyGen MCP upload tool. The exact tool name in the current session will appear under the `mcp__heygen__*` namespace; the canonical name is **`upload_asset`**.

Pass the MP3 file path (or its bytes if the MCP requires inline content) and asset type `audio`. Capture the returned `asset_id` (sometimes `id` or `audio_asset_id` depending on schema).

If the upload tool is not exposed in the current MCP session, stop and tell the user — do **not** fall back to `curl https://upload.heygen.com/v1/asset`.

### 4. Generate the avatar video

Call the HeyGen MCP video-creation tool — canonical name **`generate_avatar_video`**. Required shape (the MCP wrapper translates this into the v3 API):

```
character:
  type: avatar
  avatar_id: <picked from allowlist>
  scale: 1.0
voice:
  type: audio
  audio_asset_id: <from step 3>
dimension:
  width: 720
  height: 1280     # 9:16
title: "<mp3-stem>-<timestamp>"
```

Capture the returned `video_id`.

**Why voice type = audio (not text):** lip-sync from an existing MP3 requires HeyGen to consume the audio directly. Sending a `voice_id` here would switch HeyGen into TTS mode and ignore the uploaded MP3.

### 5. Poll until completed

Call the MCP status tool — canonical name **`get_avatar_video_status`** — every ~10 seconds with the `video_id`. Statuses:

- `processing` / `pending` → keep polling
- `completed` → grab `video_url` from the response and proceed
- `failed` → stop, show the error to the user

Cap the wait at ~10 minutes; if still processing, tell the user and let them decide.

### 6. Download the MP4

Resolve the output path (default: `workspace/heygen-clips/<mp3-stem>/<mp3-stem>_<timestamp>.mp4` — create parent dirs if needed).

Download via the helper:

```bash
uv run .claude/skills/heygen-mp3-to-mp4/scripts/download_video.py "<video_url>" "<output_path>"
```

This is a plain HTTPS download of the URL HeyGen returned — not an API call to create or modify a video — so it does not violate the MCP-only constraint.

### 7. Report back

Tell the user three things in one short reply:

- output path of the MP4
- which avatar look was used
- duration & file size of the result

## Example

User: `tạo video heygen từ mp3 workspace/audio/episode-3.mp3`

You:
1. `check_duration.py workspace/audio/episode-3.mp3` → `OK 87.4`
2. Random pick: `66e75e22e6584bbdaa56a19088286dc8`. Say so.
3. `mcp__heygen__upload_asset` → `asset_id: a_xxx`
4. `mcp__heygen__generate_avatar_video` (avatar + audio asset, 720×1280) → `video_id: v_yyy`
5. Poll `mcp__heygen__get_avatar_video_status` every 10s until `completed` → `video_url`
6. `download_video.py <url> workspace/heygen-clips/episode-3/episode-3_20260429-143022.mp4`
7. Report path, look ID, duration.

## What this skill deliberately does NOT do

- Does not write/transcribe SRT (that's `mkt-ai-video-extract-srt-segment`).
- Does not plan visuals, b-roll, segments (that's `plan-short-video-edit`).
- Does not chunk MP3 (that's `heygen-short-video` with `split_audio.py`).
- Does not compose with Remotion (that's `heygen-remotion-short-video-editor`).

If the user wants any of the above, point them at the right skill instead of expanding this one.

## Failure modes & messages

| Symptom | What to tell the user |
|---|---|
| MP3 file missing | `MP3 không tìm thấy ở <path>. Kiểm tra lại đường dẫn.` |
| MP3 > 300s | `MP3 dài <X>s, vượt giới hạn 5 phút của HeyGen. Dùng skill heygen-short-video (có chunking) thay thế.` |
| HeyGen MCP not connected | `HeyGen MCP chưa kết nối. Chạy: claude mcp list để kiểm tra.` |
| Upload tool missing in MCP | `MCP HeyGen phiên bản này không expose upload_asset. Skill này yêu cầu MCP-only — không fallback REST.` |
| HeyGen returns failed | `HeyGen render failed: <error>. Có thể avatar look bị xoá hoặc audio asset không hợp lệ.` |
| Out of credits | `Hết credit HeyGen. Check qua mcp__heygen__get_remaining_credits.` |
