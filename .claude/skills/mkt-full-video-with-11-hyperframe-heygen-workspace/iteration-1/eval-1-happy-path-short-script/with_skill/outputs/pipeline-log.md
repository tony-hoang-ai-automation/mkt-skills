# Pipeline Log - eval-1-happy-path-short-script

Skill: mkt-full-video-with-11-hyperframe-heygen
Date: 2026-04-29
Slug: smoke-test-claude-code
Workspace: workspace/content/2026-04-29/smoke-test-claude-code/
Test mode: Automated (no user checkpoint stop, stop before final render)

## Phase 0 - Setup - DONE

- Validated script length (232 chars, <= 5000) - PASS
- Slug from task input: smoke-test-claude-code
- Date folder: 2026-04-29 (today, UTC+7)
- Workspace folder: /Users/tonyhoang/Documents/GitHub/hoang-ai-marketing/workspace/content/2026-04-29/smoke-test-claude-code/
- Script saved at workspace/content/2026-04-29/smoke-test-claude-code/script.txt
- B-roll: NONE (per task spec - skip Step 4 b-roll mapping)

## Phase 1 (ElevenLabs TTS) - DONE

Command: uv run .claude/skills/mkt-elevenlabs-tts-to-mp3/scripts/text_to_mp3.py --file workspace/content/2026-04-29/smoke-test-claude-code/script.txt -o workspace/content/2026-04-29/smoke-test-claude-code/voiceover.mp3

Output:
- voiceover.mp3 - 0.2 MB (210,695 bytes)
- Char count: 232
- Voice: K7ewtjKRNtwwt3lKQ6M0 (Hoang brand voice, default)
- Model: eleven_multilingual_v2
- Format: mp3_44100_128
- Pronunciation substitutions: none

Duration check (heygen-mp3-to-mp4/scripts/check_duration.py):
- Result: OK 13.1 - well within 300s HeyGen cap

## Phase 2 - CHECKPOINT (auto-bypassed per test mode)

Per test harness rules, the user MP3-review checkpoint was auto-bypassed (treated as OK). No user prompt issued.

## Phase 2 (HeyGen MP3 -> MP4) - FAILED (BLOCKED on MCP auth)

Avatar pick (random from allowlist):
- Picked: ff800d7f76aa48f5a23eb6a742ed5365
- Allowlist: ff800d7f76aa48f5a23eb6a742ed5365, 66e75e22e6584bbdaa56a19088286dc8

MCP precheck (mcp__heygen__get_current_user):
- Result: MCP server heygen requires re-authorization (token expired)

claude mcp list confirmation:
heygen: https://mcp.heygen.com/mcp/v1/ (HTTP) - ! Needs authentication

Failure mode (per skill SKILL.md table):
- HeyGen MCP not connected -> Stop, bao user claude mcp list de verify MCP HeyGen connected.

Hard constraint enforcement (per heygen-mp3-to-mp4 SKILL.md):
- Never call https://api.heygen.com/... via curl/requests for video generation. (HeyGen MCP only.)
- If the upload tool is not exposed in the current MCP session, stop and tell the user - do NOT fall back to curl https://upload.heygen.com/v1/asset.

Action taken: Pipeline halted at start of Phase 2 (Step 3, before any HeyGen API call). No retry attempted (per task instruction). No fallback to REST.

Deviation from happy path: The eval-1 happy-path test cannot complete past Phase 1 in the current environment. The task description stated .env had ELEVENLABS_API_KEY + HeyGen MCP connected, but at runtime the HeyGen MCP token is expired. To unblock, run HeyGen MCP re-auth and retry the eval.

## Phase 3 (HyperFrames packaging) - NOT STARTED

Phase 3 depends on source.mp4 from Phase 2. Skipped because Phase 2 did not produce the file.

Expected (had Phase 2 succeeded):
- Transcribe source.mp4 with npx hyperframes transcribe --model medium --language vi
- Clean transcript + group captions (clean_transcript.py)
- Detect scenes (detect_scenes.py) - for ~13s/50-word script with no Bai hoc N / Tip N / Tong ket markers, the detector likely returns an empty/single-scene structure. The script DOES contain dang ky kenh -> CTA marker should fire. Per task spec: scenes.json empty/single-scene - acceptable for short script.
- Scaffold project (root index.html, compositions/captions.html, compositions/fs-cta.html, possibly default scene)
- Copy 6 SFX from workspace/assets/reels/sfx/
- Lint (npx hyperframes lint)
- Open preview (npx hyperframes preview &) - capture URL - kill bg process per test rule

## Phase 5 - Hand off - NOT REACHED

## Summary table

| Phase | Status | Output |
|---|---|---|
| 0 Setup | DONE | script.txt |
| 1 ElevenLabs | DONE | voiceover.mp3 (13.1s, 0.2 MB) |
| 2 HeyGen | BLOCKED | source.mp4 MISSING - MCP token expired |
| 3 HyperFrames | NOT STARTED | (depends on Phase 2) |
| 5 Hand off | NOT REACHED | - |

## Files actually present in workspace

script.txt 294
voiceover.mp3 210695

## Files expected per skill but missing (downstream of Phase 2 failure)

- source.mp4 (Phase 2 output)
- transcript.json (Phase 3 - Whisper)
- caption-groups.json (Phase 3)
- scenes.json (Phase 3) - would likely be near-empty for ~50-word script (acceptable per task spec)
- index.html (Phase 3 root)
- compositions/ folder
- sfx/ folder

## Resolution to retry this eval

1. Re-authenticate HeyGen MCP (host login flow).
2. Verify claude mcp list shows heygen Connected.
3. Re-run this eval - the existing voiceover.mp3 can be reused to skip Phase 1.

## Cost actually spent

- ElevenLabs: ~232 chars synthesized (mp3_44100_128) - minimal credit usage.
- HeyGen: 0 USD (no API calls made).
- Total estimated: ~0.005 USD (ElevenLabs only).
