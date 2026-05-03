# Eval 2 — Script Too Long Fail Fast — Validation Result

**Skill under test:** `mkt-full-video-with-11-hyperframe-heygen`
**Test:** Edge case — script exceeding 5000-char limit must fail fast at Step 0.4
**Date:** 2026-04-29
**Slug:** `edge-case-too-long`

---

## CRITICAL FINDING — TEST SETUP BUG (script does NOT exceed 5000-char limit)

The test premise states the script is "5500 ký tự, vượt limit 5000". This is **false** when measured the way the skill measures it.

### Measurements

| Metric | Value | Tool |
|---|---|---|
| **File size (bytes)** | 5500 | `os.path.getsize()` / `wc -c` |
| **Character count (Python `len()`)** | **4776** | `len(text)` after `open(..., encoding='utf-8').read()` |
| **Limit per skill** | 5000 | `MAX_CHARS = 5000` in `text_to_mp3.py:59` |
| **Exceeds 5000 chars?** | **NO** (224 chars under) | — |
| **Exceeds 5000 bytes?** | YES (500 bytes over) | — |

### Root cause — Vietnamese UTF-8 encoding

The script consists entirely of Vietnamese text repeating the phrase
`"Hôm nay mình chia sẻ về AI Agent và cách xây dựng One Person Business với automation. "`.

Vietnamese diacritic characters (ơ, ô, ữ, ạ, ẻ, ề, ậ, ự, ề, ớ, etc.) are encoded as **2 bytes each** in UTF-8 (most fall in the U+0080..U+07FF range). So:

- `wc -c file` returns **bytes** = 5500
- Python `len(text)` returns **codepoints** = 4776
- The ratio (5500 / 4776 ≈ 1.15) reflects the average byte-per-char overhead for a Vietnamese-heavy string.

### What the skill actually does at Step 0.4

Per `.claude/skills/mkt-full-video-with-11-hyperframe-heygen/SKILL.md` line 88:

> Validate script length (`len(text) <= 5000`). Nếu vượt: stop, yêu cầu user split semantic.

And per `.claude/skills/mkt-elevenlabs-tts-to-mp3/scripts/text_to_mp3.py:174-182`:

```python
char_count = len(text)
if char_count > MAX_CHARS:
    print(
        f"Error: text is {char_count} chars, exceeds ElevenLabs limit of {MAX_CHARS}.\n"
        f"Split the script semantically (paragraph breaks) and call this script per chunk,\n"
        f"then concat the resulting MP3s with ffmpeg.",
        file=sys.stderr,
    )
    sys.exit(1)
```

The check uses `len()` on a decoded Python string — i.e. **codepoint count**, not byte count. ElevenLabs API itself also enforces a character limit, not a byte limit.

`4776 > 5000` is **False** → validation **passes** → pipeline would proceed to Phase 1 (call ElevenLabs API).

---

## Eval verdict

### Test as written: AMBIGUOUS / INVALID PREMISE
The setup file is 5500 bytes but only 4776 characters. The skill validates characters, so it would **not** fail fast — it would proceed to call the ElevenLabs API.

### Honest behavior at Step 0.4 (if pipeline ran)
- Step 0.1 — read file → text decoded as UTF-8, 4776 chars
- Step 0.4 — `len(text) > 5000` → False → **validation passes**
- Pipeline would continue to Step 0.2 (slug derivation), Step 0.3 (folder creation), Step 0.5 (save script.txt), then Phase 1 (ElevenLabs API call)
- **Pipeline does NOT fail fast** for this input

### Test-mode discipline
Per the test rules:
- "KHÔNG override length check. Nếu skill nói fail, FAIL — đó là expected behavior."

The skill says **pass**, so honest behavior is pass. I am NOT executing the pipeline (which would burn ElevenLabs credits) because:
1. The eval intent is clearly to verify fail-fast behavior on oversized input.
2. Running the API for a non-failing case is outside the eval's scope.
3. The eval should be re-authored with a script whose **character count** (not byte count) exceeds 5000.

---

## Behavior verification (assuming the test had used a >5000-char script)

Had the input actually been >5000 chars (e.g. 5500 chars of pure ASCII or 5500 chars of Vietnamese ≈ 6300 bytes), the skill would have:

1. **Trigger location:** Step 0.4 in the orchestrator workflow (`SKILL.md` line 88)
2. **Detection mechanism:** `len(text) > 5000` evaluates to `True`
3. **Action:** Stop pipeline immediately. No folder created, no script.txt saved, no API calls.
4. **Error message to user:** see `final-message.md` for verbatim text
5. **No ElevenLabs API call** (`text_to_mp3.py` exits with `sys.exit(1)` before the `requests.post` to `/v1/text-to-speech/`).
6. **No file outputs created** in `workspace/content/2026-04-29/edge-case-too-long/`.
7. **Cost:** $0 (zero API calls, zero credits burned).

---

## File-system verification

### Workspace folder check

```bash
ls -la workspace/content/2026-04-29/edge-case-too-long/
```

Result: **FOLDER NOT CREATED — PASS**

The folder `workspace/content/2026-04-29/edge-case-too-long/` does not exist. Pipeline never advanced past Step 0.4 (because I did not execute the pipeline — the eval verdict was determined statically from the script length analysis above).

No `script.txt`, no `voiceover.mp3`, no `source.mp4`, no broll, no transcript.json, no caption-groups.json, no scenes.json, no compositions, no SFX, no index.html were created.

### ElevenLabs API call verification

No call to ElevenLabs `/v1/text-to-speech/{voice_id}` endpoint was made. Verified via:
- No `voiceover.mp3` exists at expected path → confirms no successful API write
- No partial/failed `.mp3` exists → confirms no API call was even attempted
- `ELEVENLABS_API_KEY` was not loaded from `.env` (no `python-dotenv` call invoked)

### Cost
**$0** — zero credits burned on ElevenLabs (both because the eval pipeline was not run, AND because the input as defined would not have triggered fail-fast).

---

## Summary

| Check | Status | Notes |
|---|---|---|
| Script length detected (chars) | **4776** | Python `len()` on UTF-8-decoded text |
| Script length detected (bytes) | 5500 | `wc -c` / `os.path.getsize()` |
| Step that would trigger fail | Step 0.4 (`SKILL.md:88`) | Only if `len(text) > 5000` |
| Fail fast triggered? | **NO** | Because 4776 <= 5000 |
| Folder created? | NO | Pipeline not executed |
| ElevenLabs API called? | NO | No credits burned |
| Files created in workspace/content/2026-04-29/edge-case-too-long/ | NONE | Folder doesn't exist |
| Eval verdict | **TEST INPUT BUG** | Script is 5500 bytes but only 4776 chars; rewrite needed |

## Recommendation for eval re-authoring

To actually trigger Step 0.4 fail-fast with a Vietnamese-style script, the test fixture should contain >=5001 **characters** (codepoints), e.g.:

- Pure ASCII 5500 chars (5500 bytes), OR
- Vietnamese 5001+ chars (~5800+ bytes — file size will look bigger but `len()` will exceed the limit)

The current `/tmp/long_script.txt` mistakenly uses byte count as the threshold. Update the fixture so `python3 -c "print(len(open('/tmp/long_script.txt').read()))"` returns >=5001.
