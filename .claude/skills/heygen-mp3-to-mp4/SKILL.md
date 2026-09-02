---
name: heygen-mp3-to-mp4
description: Convert a single MP3 voiceover file into a single HeyGen avatar lip-sync MP4 video. Defaults to **Avatar V engine** (higher-quality cross-reference animation) with automatic fallback to Avatar IV when the avatar look is not eligible. Single-purpose — no planning, no SRT, no chunking, no Remotion compositing. Hybrid path — REST asset upload (`POST /v3/assets` helper script) + HeyGen MCP for video creation, because the post-2026 MCP no longer exposes an asset-upload tool. Reads avatar look pool (`HEYGEN_AVATAR_LOOKS`) from `.env` and HeyGen API key (`HEYGEN_API_KEY`) for the upload step. USE WHEN user says "tạo video heygen từ mp3", "mp3 to heygen", "heygen mp4 từ audio", "convert mp3 sang heygen video", "tạo avatar video từ file mp3", "lip sync mp3 heygen", "biến mp3 thành video heygen", or any time the user has exactly one MP3 file and wants exactly one HeyGen avatar MP4 out.
---

# HeyGen MP3 → MP4 (Single-Purpose)

Take one MP3 voiceover, return one HeyGen avatar lip-sync MP4. Nothing else.

This skill exists because `heygen-short-video` requires a full production plan + SRT + chunked segments — overkill when the user just has a finished voiceover and wants a talking-head video.

## API version policy (read first)

**v3 only.** HeyGen's v1/v2 endpoints are legacy: they answer with `deprecation: true` +
`sunset: Sat, 31 Oct 2026 00:00:00 GMT` and are retired on **2026-11-01**.

- Never call `POST /v2/video/generate`, `POST /v1/video/generate`, `GET /v1/video_status.get`,
  `GET /v2/avatars`, or `POST https://upload.heygen.com/v1/asset`.
- Current endpoints: `POST /v3/assets` (upload) · `POST /v3/videos` (create) ·
  `GET /v3/videos/{id}` (poll) · `GET /v3/users/me` (account + wallet balance).
- The MCP tools (`create_video_from_avatar`, `get_video`) already route to v3 — the sunset
  does not affect the MCP path. Only direct REST calls need care.

Full mapping table, billing-lane gotcha, and re-verification commands: [references/api-versions.md](references/api-versions.md).

## Why hybrid REST + MCP (not MCP-only)

Earlier versions of this skill enforced "MCP only — never call REST." That rule is **no longer feasible** as of the 2026 HeyGen MCP reshape: the MCP server exposes `create_video_from_avatar`, `get_video`, `create_lipsync`, `list_avatar_looks`, etc. — there is **no asset-upload tool**. To lip-sync from a local MP3 the API still requires either an `audioAssetId` (uploaded asset) or an `audioUrl` (public HTTPS URL). Hosting a public URL is fragile (link rot, leakage), so we upload via `POST /v3/assets` through a thin helper, then continue through MCP for video creation, polling, and download.

## Hard constraints

| Constraint | Allowed values |
|---|---|
| Asset upload | REST `POST https://api.heygen.com/v3/assets` via `scripts/upload_asset.py` (uses `HEYGEN_API_KEY`) |
| Video creation / status | **HeyGen MCP** (`mcp__heygen__create_video_from_avatar`, `mcp__heygen__get_video`). REST fallback = `scripts/create_video.py` (v3), never raw v2 |
| Avatar look ID | One of the IDs in `HEYGEN_AVATAR_LOOKS` env var (comma-separated allowlist) |
| **Engine** | **Avatar V default** (`engine={"type":"avatar_v"}`). Fallback to Avatar IV (`{"type":"avatar_iv"}` or omit) ONLY when `get_avatar_look.supported_api_engines` does not contain `avatar_v` |
| Voice ID (only if MCP path forces TTS) | `HEYGEN_VOICE_ID` from `.env` (no other voice ID is permitted) |
| MP3 duration | ≤ 300 seconds (5 minutes). Fail fast if longer; do **not** auto-split |
| Aspect ratio | `9:16` default (TikTok / Reels). `16:9` only when parent orchestrator overrides |
| Resolution | `720p` default (yields 720×1280 for 9:16, 1280×720 for 16:9) |

For MP3 lip-sync the voice type is `audio` and `audioAssetId`/`audioUrl` is provided — `voiceId` is **not** sent. The voice_id allowlist above only matters if a future MCP signature requires one.

**Avatar V vs Avatar IV** — Avatar V uses cross-reference-driven animation for noticeably better lip-sync + subtle body motion, at the cost of longer render time (~1.5-2× IV). Default is Avatar V. The engine selector is per-call (`engine={"type":"avatar_v"}`), and HeyGen rejects `expressiveness` + `motionPrompt` params when Avatar V is selected (those are IV-only). If the picked avatar look does not list `avatar_v` in `supported_api_engines`, transparently fall back to Avatar IV and tell the user which engine was used.

## Inputs

1. **MP3 path** (required) — absolute path to the voiceover file.
2. **Avatar look ID** (optional) — one of the allowed IDs. If omitted, **pick randomly** from the allowed set so visual variety emerges across runs.
3. **Output path** (optional) — defaults to `workspace/heygen-clips/<mp3-stem>/<mp3-stem>_<YYYYMMDD-HHMMSS>.mp4` relative to the project root.
4. **Aspect ratio** (optional) — `9:16` (default) or `16:9`.

## Workflow

Follow these steps in order. Each step has a stop condition; do not proceed past a failed step.

### 0. Auth check (first call only)

The HeyGen MCP server uses OAuth. On a fresh session only `mcp__heygen__authenticate` and `mcp__heygen__complete_authentication` are exposed; the real tools (`create_video_from_avatar`, `get_video`, …) appear **after** auth completes. If the session has none of those tools loaded, call `mcp__heygen__authenticate` and surface the returned authorize URL to the user. They click → the browser may show "connection error" on the localhost callback (expected) → they paste the full callback URL back, you call `mcp__heygen__complete_authentication`. Once the post-auth tools surface in the deferred-tool list, continue.

If OAuth cannot be completed in this session (non-interactive run), use the REST fallback in Step 4b — it needs only `HEYGEN_API_KEY` plus a funded API wallet.

### 1. Validate the MP3

```bash
uv run .claude/skills/heygen-mp3-to-mp4/scripts/check_duration.py "<mp3_path>"
```

Prints `OK <seconds>` / `TOO_LONG <seconds>` / `MISSING`. Exit code 0 = OK, non-zero = stop.

If `TOO_LONG`: tell the user the duration and that HeyGen caps a single video at ~5 min, and suggest `heygen-short-video` (which chunks). Do not proceed.

### 2. Pick the avatar look

```bash
HEYGEN_AVATAR_LOOKS=$(
  grep -h '^HEYGEN_AVATAR_LOOKS=' .env.local .env 2>/dev/null \
  | head -1 | cut -d'=' -f2- | tr -d '"' | tr -d "'"
)
echo "$HEYGEN_AVATAR_LOOKS" | tr ',' '\n' | awk 'BEGIN{srand()} {a[NR]=$0} END{print a[int(rand()*NR)+1]}'
```

**Placeholder pitfall** — some repos ship `.env.local` with stubs (`avatar_look_id_1,avatar_look_id_2`). Real values often live in `~/Documents/GitHub/hoang-ai-marketing/.env`:

```bash
grep '^HEYGEN_AVATAR_LOOKS=' ~/Documents/GitHub/hoang-ai-marketing/.env
```

If the value matches `^(your_|avatar_look_id_|placeholder)`, treat it as missing and fall back to the marketing-repo `.env`. If both are placeholder/missing, stop and ask the user to fill in real IDs.

Tell the user which avatar look you picked before continuing — they may want to override.

### 2.5. Check engine eligibility (Avatar V vs Avatar IV)

Call **`mcp__heygen__get_avatar_look`** with the picked `lookId` and inspect `supported_api_engines`:

```yaml
supported_api_engines: ["avatar_v", "avatar_iv"]   # → use Avatar V (default)
supported_api_engines: ["avatar_iv"]               # → use Avatar IV (fallback)
```

- If `"avatar_v"` is present → `engine = {"type": "avatar_v"}`
- Otherwise → omit `engine` (HeyGen defaults to Avatar IV)

Tell the user which engine will be used. Accept an override (`--engine iv` or natural language) — Avatar IV renders faster and accepts `expressiveness` + `motionPrompt`.

### 3. Upload the MP3 as a HeyGen asset (REST, v3)

```bash
uv run .claude/skills/heygen-mp3-to-mp4/scripts/upload_asset.py "<mp3_path>"
# → prints "OK <asset_id>" on success
```

The helper POSTs multipart to `https://api.heygen.com/v3/assets`, picks the right MIME type for the extension, and resolves `HEYGEN_API_KEY` in this order: `--key-file` flag → `HEYGEN_API_KEY` env → `.env.local` → `.env` → `~/Documents/GitHub/hoang-ai-marketing/.env`. Placeholder stubs (`your_*`) are skipped automatically.

`--legacy` still exists for the retired-in-2026 `upload.heygen.com/v1/asset` path. Do not use it unless v3 is failing for a specific account, and never after 2026-10-31.

Capture the asset_id printed on stdout.

### 4. Generate the avatar video (MCP)

Call **`mcp__heygen__create_video_from_avatar`** (the old `dimension: {width, height}` shape is gone — the tool takes `aspectRatio` + `resolution` enums) with the engine chosen in Step 2.5:

```yaml
avatarId:       <picked from allowlist>
audioAssetId:   <from step 3>             # OR audioUrl when cross-workspace upload
aspectRatio:    "9:16"                    # or "16:9" when parent orchestrator overrides
resolution:     "720p"                    # 720p · 1080p · 4k
engine:         {"type": "avatar_v"}      # DEFAULT — omit only when Step 2.5 chose IV fallback
title:          "<mp3-stem>-<timestamp>"
```

Capture the returned `video_id` (status starts as `waiting`).

**Avatar V constraint:** when `engine.type == "avatar_v"`, do NOT send `expressiveness` or `motionPrompt` — HeyGen rejects them. Those are Avatar IV only.

**Why audio (not text):** lip-sync from an existing MP3 requires HeyGen to consume the audio directly. Sending `script` + `voiceId` switches HeyGen into TTS mode and ignores the uploaded MP3 entirely.

### 4b. REST fallback (only when MCP is unavailable)

```bash
uv run .claude/skills/heygen-mp3-to-mp4/scripts/create_video.py \
  --avatar-id "<look_id>" --audio-asset-id "<asset_id>" \
  --aspect-ratio 9:16 --resolution 720p --engine avatar_v \
  --title "<slug>-<timestamp>" --wait
# → "OK <video_id> <video_url>"
```

This hits `POST /v3/videos` + `GET /v3/videos/{id}` — never v2. It bills the **API-key wallet**, not the subscription credits the MCP/OAuth path uses; a `402 insufficient_credit` here means the wallet is empty even though MCP would still render. Check with `curl -s https://api.heygen.com/v3/users/me -H "X-Api-Key: $HEYGEN_API_KEY"`.

### 5. Poll until completed

Call **`mcp__heygen__get_video`** with the `video_id` every ~10–15 seconds:

- `waiting` / `processing` / `pending` → keep polling
- `completed` → grab `video_url` and proceed
- `failed` → stop, surface `failure_message`

Cap the wait at ~10 minutes; if still processing, tell the user and let them decide. REST equivalent: `create_video.py --status <video_id>`.

**zsh quirk for poll loops** — the variable name `status` is read-only in zsh. `status=$(…)` in a polling loop crashes with `read-only variable: status`. Use `vstate`, `phase`, or `ready`.

### 6. Download the MP4

```bash
uv run .claude/skills/heygen-mp3-to-mp4/scripts/download_video.py "<video_url>" "<output_path>"
```

Plain HTTPS download of the URL HeyGen returned — not an API call.

### 7. Report back

One short reply with: output path of the MP4, which avatar look + engine were used, duration & file size.

## Example

User: `tạo video heygen từ mp3 workspace/audio/episode-3.mp3`

1. Auth check → if HeyGen tools present, skip; else `mcp__heygen__authenticate` + complete OAuth.
2. `check_duration.py workspace/audio/episode-3.mp3` → `OK 87.4`
3. Random pick from `HEYGEN_AVATAR_LOOKS` (e.g. `66e75e22e6584bbdaa56a19088286dc8`). Say so.
4. `mcp__heygen__get_avatar_look(lookId="66e75e22…")` → `supported_api_engines: ["avatar_v","avatar_iv"]` → Avatar V. Say so.
5. `upload_asset.py workspace/audio/episode-3.mp3` → `OK 36922ca92326480f8dbb0f57fae1a144`
6. `mcp__heygen__create_video_from_avatar(avatarId=…, audioAssetId=…, aspectRatio="9:16", resolution="720p", engine={"type":"avatar_v"}, title="episode-3-…")` → `video_id: 874793a8…`
7. Poll `mcp__heygen__get_video` every ~15s until `completed` → `video_url` (Avatar V renders ~1.5-2× longer than IV)
8. `download_video.py <url> workspace/heygen-clips/episode-3/episode-3_20260902-143022.mp4`
9. Report path, look ID, engine, duration.

## What this skill deliberately does NOT do

- Does not write/transcribe SRT (that's `mkt-ai-video-extract-srt-segment`).
- Does not plan visuals, b-roll, segments (that's `mkt-plan-short-video-edit-16-9`).
- Does not chunk MP3 (that's `heygen-short-video` with `split_audio.py`).
- Does not compose with Remotion or HyperFrames (that's the parent orchestrator).

If the user wants any of the above, point them at the right skill instead of expanding this one.

## Failure modes & messages

| Symptom | What to tell the user |
|---|---|
| MP3 file missing | `MP3 không tìm thấy ở <path>. Kiểm tra lại đường dẫn.` |
| MP3 > 300s | `MP3 dài <X>s, vượt giới hạn 5 phút của HeyGen. Dùng skill heygen-short-video (có chunking) thay thế.` |
| HeyGen MCP not authenticated | Surface `mcp__heygen__authenticate` URL, ask user to authorize, then `mcp__heygen__complete_authentication`. |
| `HEYGEN_API_KEY` not found / placeholder | `Không tìm thấy HEYGEN_API_KEY. Helper đã thử .env.local, .env, và ~/Documents/GitHub/hoang-ai-marketing/.env. Cần key thật (không phải stub your_*).` |
| `HEYGEN_AVATAR_LOOKS` is placeholder (`avatar_look_id_1,…`) | Same fallback as the API key — read from marketing repo, or ask user to fill in real avatar IDs. |
| HeyGen returns failed | `HeyGen render failed: <failure_message>. Có thể avatar look bị xoá hoặc audio asset không hợp lệ.` |
| `402 insufficient_credit` on REST fallback | API wallet ở `$0` (khác với subscription credits của MCP). Check `GET /v3/users/me`, nạp tại https://app.heygen.com/billing, hoặc quay lại đường MCP. |
| Tool name not found (`upload_asset` / `generate_avatar_video` / `get_avatar_video_status`) | Old MCP names — replaced by REST upload + `create_video_from_avatar` + `get_video`. Update any caller still using the old names. |
| Any code path calling `/v2/video/generate` or `upload.heygen.com/v1/asset` | Legacy, sunset 2026-10-31 → switch to `POST /v3/videos` / `POST /v3/assets`. See [references/api-versions.md](references/api-versions.md). |
| Avatar look does not support Avatar V | Transparent fallback: omit `engine` → Avatar IV. Tell user "Avatar V không khả dụng cho look này, dùng Avatar IV". |
| HeyGen rejects `expressiveness` / `motionPrompt` with Avatar V | Those params are Avatar IV only. Drop them when `engine.type == "avatar_v"`. |
| User passes `--engine iv` override | Skip Step 2.5 selection, omit `engine`. Avatar IV (faster, accepts expressiveness/motionPrompt). |
