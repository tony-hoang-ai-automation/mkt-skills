# Final Message Skill Would Show User (had fail-fast triggered)

## Context

For THIS specific test input (`/tmp/long_script.txt` = 5500 bytes / **4776 characters**), the skill would **NOT** show a fail-fast error message — because `len(text) = 4776 <= 5000`, the validation passes and the pipeline proceeds to Phase 1.

No fail-fast message was emitted by the skill for this input.

---

## What the skill WOULD say if a script truly exceeded 5000 characters

### Verbatim error from sub-skill `text_to_mp3.py`

Per `.claude/skills/mkt-elevenlabs-tts-to-mp3/scripts/text_to_mp3.py:176-181` — written to stderr before `sys.exit(1)`:

```
Error: text is <N> chars, exceeds ElevenLabs limit of 5000.
Split the script semantically (paragraph breaks) and call this script per chunk,
then concat the resulting MP3s with ffmpeg.
```

Where `<N>` is the actual character count.

### Skill-level enforcement

Per `.claude/skills/mkt-full-video-with-11-hyperframe-heygen/SKILL.md` (Failure modes table, line 277):

> | Script > 5000 ký tự | Stop, yêu cầu user split semantic và gọi pipeline cho từng đoạn |

And per the orchestrator's "What this skill does NOT do" section (line 313):

> KHÔNG handle script > 5000 ký tự (fail fast — user split semantic).

---

## Reconstructed user-facing message (orchestrator-level, brand voice)

If the orchestrator surfaced the fail to the user, the expected output (per skill conventions) would be:

```markdown
## Script vượt 5000 ký tự — fail fast

**Script length:** <N> ký tự (limit 5000)
**Vượt:** <N - 5000> ký tự

ElevenLabs hard-cap 5000 ký tự / request. Auto-split sẽ gây prosody jumps tại boundary → output kém chất lượng.

**Hành động cần làm:**
1. Split script theo paragraph/semantic boundary (mỗi đoạn <= 5000 ký tự).
2. Gọi pipeline cho từng đoạn riêng — mỗi đoạn ra 1 MP3.
3. Concat các MP3 bằng ffmpeg sau Phase 1, hoặc gộp ở Phase 3 (HyperFrames composition).

**KHÔNG:** workspace folder chưa tạo, ElevenLabs API chưa gọi, $0 credit burned.

Reply với script đã split (hoặc 1 đoạn ngắn hơn) để mình tiếp tục pipeline.
```

---

## Actual behavior for THIS test input (4776 chars)

**No fail-fast message was triggered.** Validation passed at Step 0.4. The pipeline (had it been executed) would have proceeded to Phase 1 (ElevenLabs TTS).

I did **not** execute the pipeline because the eval intent (verify fail-fast) does not match the input (which does not exceed the limit). Running it would have burned ElevenLabs credits for a case the eval was not designed to measure.

See `validation-result.md` for the test-input bug analysis and recommendations.
