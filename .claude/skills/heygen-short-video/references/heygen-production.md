# HeyGen Production — Parallel Tracks

After user provides Grok videos (or skips if all-avatar), run these **3 tracks in parallel** (no dependencies between them).

## Track A: Verify & Trim Grok/Custom Videos

Verify files exist (`1.mp4`, `2.mp4`...). Trim if needed:
```bash
ffmpeg -i "<grok_video>" -t <segment_duration> -c copy "<output_path>"
```

For custom b-roll media, see [custom-broll.md](custom-broll.md) for image/video handling.

## Track B: Render PromptTyping Segments

For each `prompt-typing` segment:

1. Create props JSON:
```json
{
  "text": "The prompt text to display...",
  "durationSeconds": 12,
  "title": "Prompt"
}
```
Optional: `startDelaySec` (default 0.5), `endPauseSec` (default 1.0)

2. Render:
```bash
cd workspace/video-projects/remotion-studio
npx remotion render src/index.ts PromptTyping out/prompt-1.mp4 --props=props/prompt-typing.json
```

## Track C: Split Audio & Generate Avatar Clips

### C1: Split Audio

```bash
uv run .claude/skills/heygen-short-video/scripts/split_audio.py "<mp3_path>" "<srt_path>" \
  --avatars "7ebc6e135f574dcdb943d309cb97806a:talking-head micro,2e8a789bfbf847d38a03470efbe64f69:laptop desk,27776380b32d4b4aa4c5824571fc7117:dual monitor office,b6b2968fadf5432cb7ebc104da63808f:micro simple bg" \
  --min-chunk-duration 8 --max-chunk-duration 20 \
  --output-dir "<working_dir>/chunks"
```

Only include avatar segments. Replace avatar IDs if user provided custom ones.

### C2: Upload & Submit to HeyGen (parallel per chunk)

**IMPORTANT: Use audioAssetId for lip-sync — NOT script+voiceId (TTS).**

Upload each chunk MP3 **in parallel** (v3 assets endpoint — the old
`upload.heygen.com/v1/asset` is legacy and sunsets 2026-10-31):
```bash
curl -X POST "https://api.heygen.com/v3/assets" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -F "file=@<chunk_path>;type=audio/mpeg"
# → data.asset_id
```

Create video with `audioAssetId` **in parallel** (submit all chunks concurrently):
```
mcp__heygen__create_video_from_avatar:
  avatarId: chunk.avatar_id
  audioAssetId: <uploaded_asset_id>
  aspectRatio: "9:16"
  resolution: "720p"
  title: "chunk_{index}"
```

### C3: Poll & Download (parallel per video)

```
For each video_id (poll all concurrently):
  mcp__heygen__get_video(videoId) → wait until status="completed"
  Download video_url to <working_dir>/heygen_clips/chunk_XXX.mp4
```
