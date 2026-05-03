---
name: mkt-hyperframe-talking-head-video
description: Build a TikTok/Reels 9:16 short video from a pre-recorded talking-head MP4 using HyperFrames — transcribe Vietnamese audio, auto-clean Whisper errors, generate synced caption groups, scaffold a complete preview-ready project with face-cam + 6 sound effects + 4 zoom hooks + ambient ken-burns drifts + full-screen b-roll scenes (each with rich GSAP effects: pulse rings, corner marks, word-slam titles, count-up numbers, light sweeps, scribble underlines, sparkles, particles) + caption track + CTA finale, then open the HyperFrames preview Studio for user review (NEVER auto-render MP4). USE WHEN user says "tạo video tiktok từ footage", "build hyperframe talking head", "tạo 9:16 video từ mp4 quay sẵn", "make tiktok video from face footage", "hyperframe video từ video quay", "tạo short video có caption + b-roll", "video chia sẻ kiến thức từ footage", "đóng gói video ngắn", or provides a 9:16 talking-head MP4 (with optional b-roll images/videos and stated purposes) asking to turn it into a finished short-form video. ALSO trigger when user has face-cam footage and wants captions + visual hooks + sound effects added to make it shareable on TikTok/Reels/Shorts/Facebook Reels.
---

# mkt-hyperframe-talking-head-video

Pipeline đóng gói: từ MP4 quay sẵn (talking head 9:16) tới HyperFrames preview project hoàn chỉnh có captions, SFX, zoom hooks, b-roll toàn cảnh có hiệu ứng rich, và CTA finale.

## When to use

- User đã quay xong 1 video face-cam 9:16 (TikTok/Reels/Shorts) và muốn add captions + visual hooks + SFX
- User có thêm 1 số ảnh hoặc video b-roll muốn chèn vào (kèm mục đích sử dụng)
- User muốn output preview Studio để duyệt visual trước khi render MP4

Đừng dùng skill này nếu:
- User chưa quay video — dùng `mkt-create-script-short-video` để viết script trước, hoặc skill khác để tạo voiceover + avatar AI
- User đã có HyperFrames project và chỉ muốn chỉnh tweaks nhỏ — sửa trực tiếp file thay vì re-scaffold
- User muốn render MP4 từ project đã có — chạy `npx hyperframes render` thẳng

## Pipeline overview

```
MP4 9:16 talking-head + (optional) b-roll files
    │
    ▼
1. Inspect MP4 ───────── ffprobe → duration, resolution, FPS
    │
    ▼
2. Plan structure ────── auto-detect lesson markers từ user input HOẶC từ transcript
    │
    ▼
3. Transcribe ────────── npx hyperframes transcribe --model medium --language vi
    │
    ▼
4. Clean transcript ──── apply VN Whisper error dict (alphabit→Alphabet, etc.)
    │
    ▼
5. Group captions ────── 3-5 words/group, break on >0.45s gap, preserve timing
    │
    ▼
6. Map b-roll ────────── ask user mục đích → assign to lesson scenes
    │
    ▼
7. Scaffold project ──── workspace/video-projects/<slug>/
    ├── index.html (root)
    ├── source.mp4
    ├── transcript.json + caption-groups.json
    ├── compositions/
    │   ├── captions.html
    │   ├── fs-lesson-N.html (one per lesson, varied effects)
    │   ├── recap-card.html (if applicable)
    │   └── fs-cta.html
    └── sfx/ (6 sound effects)
    │
    ▼
8. Lint ──────────────── npx hyperframes lint → fix any errors
    │
    ▼
9. Open preview ──────── npx hyperframes preview (background) → URL Studio
    │
    ▼
10. Hand off to user ─── KHÔNG auto-render MP4
```

**Preview-first rule (non-negotiable):** Skill kết thúc ở Step 9 với URL Studio. Render MP4 chỉ chạy khi user explicit confirm sau preview.

## Step 1: Verify input + plan

User sẽ cung cấp:

| Input | Required | Format |
|---|---|---|
| MP4 face-cam 9:16 | Yes | File path |
| Slug / tên project | No | Auto-derive from filename if missing |
| List b-roll | No | `[{path: "screenshot.png", purpose: "Bài học 1 — minh họa thử nghiệm"}, ...]` |
| Cấu trúc video | No | "3 bài học + intro + CTA" / "5 tips" / etc. — auto-detect if missing |

**Inspect MP4** trước khi làm gì:

```bash
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate \
  -of json "<mp4_path>"
```

Verify:
- Resolution là 9:16 (e.g., 1080x1920, 1440x2560) — nếu landscape, cảnh báo nhưng vẫn proceed (object-fit:cover sẽ crop)
- Duration < 180s ideal; > 180s vẫn được nhưng warn user TikTok algo prefer ≤90s
- FPS 24/25/30/60 đều OK — output sẽ default 30fps

**Slug**: derive từ filename, lowercase, dấu Việt → ASCII, space → dash. VD `"3 bài học .mp4"` → `3-bai-hoc`. User có thể override.

**Output dir**: `workspace/video-projects/<slug>/`

## Step 2: Transcribe + clean

```bash
cd workspace/video-projects/<slug>/
cp <user_mp4> source.mp4
npx hyperframes transcribe source.mp4 --model medium --language vi
```

**KHÔNG bao giờ** dùng `--model medium.en` hay `small.en` cho audio Việt — `.en` model TRANSLATE sang English thay vì transcribe. Luôn dùng `--language vi` cho audio Vietnamese.

Sau khi xong, clean transcript:

```bash
python3 .claude/skills/mkt-hyperframe-talking-head-video/scripts/clean_transcript.py \
  transcript.json
# writes: transcript.json (in-place clean) + caption-groups.json (auto-grouped)
```

Script đã apply VN Whisper error replacements (`alphabit→Alphabet`, `Cod→Code`, `dụng/dùng` context-aware, `đ��ng→đắc`, etc.) và auto-group thành 3-5 word caption phrases với break on >0.45s gap.

**Critical caption sync rule:** Timing PHẢI giữ y nguyên từ word-level transcript. KHÔNG hand-edit timing. Nếu cần sửa text, sửa text only — script `clean_transcript.py` đã handle. Bug điển hình: hand-edit text rồi accidentally sửa timing → captions lệch 5s ở giữa video.

## Step 3: Detect scene structure

```bash
python3 .claude/skills/mkt-hyperframe-talking-head-video/scripts/detect_scenes.py \
  transcript.json
# outputs: scenes.json
```

Script tìm trong transcript các marker:
- "Bài học đầu tiên / thứ 2 / thứ 3 / thứ N" → lesson scenes
- "Tips số 1 / Tip 1 / Số 1" → tip scenes
- "Tổng kết lại / Recap / Kết luận" → recap moment
- "Comment / Đăng ký / Like / Theo dõi" → CTA moment

Output `scenes.json`:
```json
{
  "type": "lessons",
  "scenes": [
    { "kind": "lesson", "num": 1, "start": 9.4, "end": 13.0, "kicker": "Bài học #1", "heading": "..." },
    { "kind": "lesson", "num": 2, "start": 34.5, "end": 38.0, ... },
    { "kind": "lesson", "num": 3, "start": 61.5, "end": 65.5, ... },
    { "kind": "recap", "start": 84.9, "end": 99.0 },
    { "kind": "cta", "start": 99.0, "end": 106.94 }
  ]
}
```

Nếu auto-detect không tìm ra structure rõ ràng (vd vlog free-form), present results cho user và xin confirm. User có thể override timestamps.

## Step 4: Map b-roll

Nếu user cung cấp b-roll files với mục đích:

```
[
  { path: "alphabet-screenshot.png", purpose: "Bài học 1 — Alphabet ship beta" },
  { path: "clock-icon.mp4",         purpose: "Bài học 2 — minh họa 24h" },
  { path: "team-meeting.png",       purpose: "Bài học 3 — bỏ rào cản team" }
]
```

**Mapping logic:**
- Mỗi b-roll match với 1 scene dựa trên text "Bài học N" trong purpose
- Image → use as full-screen background của scene đó (replace text-only generated scene)
- Video → use as full-screen scene background OR picture-in-picture overlay (default: full-screen)
- Default scene effects (pulse rings, corner marks, etc.) vẫn được layer ON TOP của b-roll image/video

Nếu user không cung cấp b-roll, dùng text-only scenes (như reference project `3-bai-hoc/`) — generated text card với title + giant number + sub.

## Step 5: Generate project files (infographic style — DEFAULT)

**Use the infographic v2 generator** for content-driven mockup b-rolls (Hostinger-inspired style: dark glassmorphic + neon glow + UI mockups + floating data badges):

```bash
python3 .claude/skills/mkt-hyperframe-talking-head-video/scripts/scaffold_infographic_v2.py \
  --output workspace/content/YYYY-MM-DD/<slug>/compositions/ \
  --scenes scenes.json
```

**scenes.json schema** (per scene, including `mockup_variant` + `content`):

```json
{
  "scenes": [
    {
      "kind": "lesson",
      "num": 1,
      "start": 12.71,
      "end": 26.40,
      "kicker": "Tư vấn AI",
      "heading": "Tư vấn AI cho 1 ngành",
      "accent_words": [2],
      "mockup_variant": "post-stack",
      "content": { "posts": [...] },
      "badges": [
        { "pos": "tr", "color": "orange", "icon": "📅", "num": "30", "label": "Ngày" }
      ]
    },
    { "kind": "recap", "mockup_variant": "team-grid", "content": {...} },
    { "kind": "cta", "mockup_variant": "comment-box", "content": {...} }
  ]
}
```

**7 mockup variants** — pick the one matching scene semantics:

| Scene type | Variant | Use for |
|---|---|---|
| Personal branding / posting | `post-stack` | Stack of 3 social cards, top highlighted with engagement |
| AI search / GEO | `ai-window` | ChatGPT-style window with rec card highlighted |
| Voice / phone / call | `phone-call` | iPhone mockup with waveform + agent bubble + slot grid |
| Analytics / dashboards | `dashboard` | Glass card with stats + creative grid + chart line |
| Product / SaaS launch | `app-card` | App card with icon + stats + optional metaphor row |
| Recap before-after | `team-grid` | 40-dot grid morph with animated count-down + multiplier |
| CTA "comment X" | `comment-box` | Comment box mockup + 2 gift cards + CTA pill |

**Full content schemas + design tokens**: see [references/infographic-design-system.md](references/infographic-design-system.md).

**Common shell elements** (auto-applied to every scene): radial gradient background + cyan grid lines + 10 SVG particles (drift loop) + vignette + topic pill (orange glow) + brand title 110px (slam-in word-by-word, accent gradient).

**Floating badges** (optional 1-4 per scene): circular 130px badges around the hero mockup with icon + number + label, color-coded (cyan/purple/orange/green) with matching glow, animate from off-screen + bob loop.

### Legacy generator (deprecated)

`scaffold_project.py` (rings/corners/light-sweep abstract decorative) — kept for backward compat but not recommended. Use `scaffold_infographic_v2.py` for new videos.

**Mỗi scene có:**
- Punch-zoom entrance trên `.scene-content` (alternating zoom-in 1.12 / zoom-out 0.92)
- Element entrances: eyebrow → num → title (word-by-word slam) → sub
- Ambient effects during scene (pulse rings, breath, drift, etc.)
- NO exit animation — clip ends, framework hides

Sub-composition rule: **internal timeline RELATIVE 0 → data-duration**, không phải absolute. Mount trong root với `data-composition-src="compositions/<name>.html"` data-start = scene.start.

## Step 6: Copy SFX

```bash
mkdir -p workspace/video-projects/<slug>/sfx
cp /Users/tonyhoang/Documents/GitHub/hoang-ai-marketing/workspace/assets/reels/sfx/{camera-flash.mp3,"búng tay.mp3","Whoosh sound effect (1).mp3",Laser.mp3,ting.mp3,"Discord Notification - Sound Effect.mp3"} workspace/video-projects/<slug>/sfx/
```

6 SFX standard mapping:
| Time | File | Volume | Moment |
|---|---|---|---|
| 0.0s | `camera-flash.mp3` | 0.32 | Hook opener — sync với source video punch zoom @0s |
| Lesson 1 start − 0.05s | `búng tay.mp3` (snap) | 0.30 | Lesson 1 reveal |
| Lesson 2 start − 0.05s | `Whoosh sound effect (1).mp3` | 0.22 | Lesson 2 transition |
| Lesson 3 start − 0.05s | `Laser.mp3` | 0.28 | Lesson 3 punch |
| Recap start − 0.05s | `ting.mp3` | 0.20 | Recap reveal |
| CTA start | `Discord Notification - Sound Effect.mp3` | 0.28 | CTA notification feel |

**SFX volume rule (per `references/sfx-library.md`):** hook 0.25-0.35, transition 0.15-0.2, CTA 0.25. Max 5-6 SFX, spaced ≥1.5s apart.

## Step 7: Lint + open preview

```bash
cd workspace/content/YYYY-MM-DD/<slug>/
npx hyperframes lint
```

Accept warnings:
- `composition_file_too_large` — informational only, OK to ignore on root
- `composition_self_attribute_selector` — info-only, infographic mockups use scoped `[data-composition-id="..."]` selectors

Reject errors:
- `gsap_animates_clip_element` — KHÔNG animate visibility/display trên clip — chỉ animate opacity
- `root_composition_missing_data_start` — sub-comps phải có `data-start="0"` trên inner div
- `media_missing_data_start` — `<audio>` SFX phải có `data-start` attribute (HF native scheduling, không dùng JS trigger)
- Caption sync issues — re-run script clean_transcript.py

### Critical: Caption z-order

Captions sub-comp **MUST** mount with **highest `data-track-index`** to render above lesson sub-comps (which have full-screen dark backgrounds). Otherwise captions are hidden behind the b-roll.

```html
<!-- Lesson/recap/cta mounts: track-index 40-47 -->
<div class="clip split-mount" data-composition-src="compositions/fs-lesson-1.html" data-start="..." data-track-index="40"></div>
<!-- ... -->
<!-- Captions LAST with track 60 + inline z-index -->
<div class="clip captions-mount"
     data-composition-src="compositions/captions.html"
     data-start="0" data-duration="..." data-track-index="60"
     style="z-index: 100;"></div>
```

## Step 7.5: Split-screen + full-face breath layout (RECOMMENDED for talking-head + b-roll)

**Use this for any video where face talking + b-roll mockups need both visible** — instead of fullscreen b-roll covering the face.

Architecture:
- Face video defaults full-screen during intro
- When b-roll appears: face shrinks to **bottom half** (1080x960), b-roll renders in **top half** (scaled 0.5)
- At end of each b-roll (1.5s before next scene): face expands back to full-screen ("breath" moment) → captures emotional punchlines
- Captions auto-animate between **center** (split mode) and **bottom** (full-face mode)

**Generate root index.html with split-screen pre-baked:**

```bash
python3 .claude/skills/mkt-hyperframe-talking-head-video/scripts/generate_root_index.py \
  --output workspace/content/YYYY-MM-DD/<slug>/index.html \
  --scenes scenes.json \
  --total-duration 108.92 \
  --header-label "6 AI BUSINESS 2026" \
  --footer-handle "@tranvanhoang.com"
```

scenes.json must include `brollEnd` + `hasBreath` per scene. See [references/split-screen-pacing.md](references/split-screen-pacing.md) for editorial rules (when full vs split), CSS specifics, and JS animation template.

**Editorial cheat sheet:**

| Moment | Layout |
|---|---|
| Hook intro 0-12s | **Full face** |
| Each Idea (data/mockup heavy) | **Split** (b-roll top, face bottom) |
| End of each Idea (punchline 1.4s) | **Full face breath** |
| Recap counter visualization | **Split first**, then **full face** for rally line |
| CTA | **Split first 2s** (show comment box), then **full face** for direct ask |

## Step 7.6: Caption typo correction (after Whisper transcription)

Whisper makes consistent Vietnamese errors (clipped accents, brand misspellings, missing spaces). Run the auto-fix:

```bash
python3 .claude/skills/mkt-hyperframe-talking-head-video/scripts/fix_caption_typos.py \
  caption-groups.json \
  script.txt    # source spoken script for additional diff check
```

The script applies a curated correction map (~25 known errors from past videos: `vừa dọt → vừa rót`, `Cửa số → Cửa sổ`, `Lê tân → Lễ tân`, `Common Cloud → Comment Claude`, `Cloud AI → Claude AI`, `Vice → Vise`, `level bổ → Lovable`, etc.) and flags suspicious tokens not present in the source script.

After fixing, re-inject:
```bash
python3 .claude/skills/mkt-hyperframe-talking-head-video/scripts/inject_captions.py \
  compositions/captions.html caption-groups.json
```

Open preview:
```bash
npx hyperframes preview
# Outputs Studio URL — typically http://localhost:3002
```

Run trong background (don't block conversation), output URL cho user.

## Step 8: Hand off to user

Báo cho user:
> **Preview Studio đã sẵn sàng!**
> URL: http://localhost:3002
>
> Mở browser scrub timeline xem:
> - Captions sync với giọng
> - 3 b-roll toàn cảnh có hiệu ứng đầy đủ (pulse rings / speed lines / light sweep)
> - Source video zoom punches sync với SFX
> - CTA finale với typing cursor + sparkles + particles
>
> Khi OK rồi nói "render" — tôi sẽ chạy `npx hyperframes render` xuất MP4 1080x1920 30fps.
> Nếu cần chỉnh visual nào, báo cụ thể (vd "lesson 2 thiếu hiệu ứng", "caption font lớn quá", "thay SFX laser bằng ting").

**Stop here.** KHÔNG render MP4 cho tới khi user xác nhận. Lý do: render mất 5-10 phút burn CPU/GPU, và preview cho phép user catch issues sớm.

## Critical rules (non-negotiable)

1. **3 giây đầu LUÔN hiện face** — Hook là overlay nhỏ ở top (180px from top, 880px wide cream card), KHÔNG full-screen. User feedback: "ko đc hiện b-roll toàn cảnh lúc đầu". Templates đã handle.

2. **Preview FIRST** — Chạy `npx hyperframes preview` mở Studio. KHÔNG `render` cho tới khi user xác nhận. Lưu trong memory `feedback_hyperframes_workflow.md`.

3. **Caption sync** — Timing lấy từ word-level transcript JSON. Script `clean_transcript.py` chỉ clean text, KHÔNG sửa timing. Hand-edit timing là common bug.

4. **GSAP `y` xung đột với `transform: translate(-50%, 0)`** — Captions container phải dùng `left: 0; right: 0; text-align: center` + inner inline-block `.text`. KHÔNG dùng transform centering. See `references/pitfalls.md`.

5. **Sub-comp internal timeline RELATIVE** — Trong sub-comp HTML, `tl.from(...)` dùng times 0 → data-duration, không phải absolute video time. Framework auto-nests timeline tại scene's data-start.

6. **No exit animations** trừ scene cuối — Clip variant tự ẩn khi data-duration end. Animating opacity:0 trước transition là anti-pattern.

7. **No visibility tween trên clip element** — Lint reject. Chỉ animate opacity. Framework manages visibility.

8. **Be Vietnam Pro mặc định**, KHÔNG Poppins/Inter/Roboto/Helvetica — font Việt-first per memory `feedback_vietnamese_typography.md`. Templates đã hardcode.

9. **SFX max 5-6, spaced ≥1.5s, volume 0.15-0.32** — Per `references/sfx-library.md`. Không front-load quá nhiều SFX.

10. **Source video zoom punch sync SFX** — Punch t=0s sync camera-flash; punches sau lesson b-roll exits sync với scene reveal. Pattern: scale 1.10→1.0 với power3.out 0.55s.

## References

- **`references/effects-catalog.md`** — Full GSAP effects list per scene type với code snippets. Đọc khi cần thêm/đổi hiệu ứng cho sub-comp.
- **`references/sfx-library.md`** — Mapping SFX file → moment + volume. Đọc khi đổi SFX hoặc add custom moment.
- **`references/design-tokens.md`** — Brand palette + typography defaults. Đọc khi user request brand alternative.
- **`references/pitfalls.md`** — Known bugs gặp trong reference project + cách fix. Đọc khi lint/preview báo lỗi lạ.

## Reference project

Sample đầy đủ tại `workspace/video-projects/3-bai-hoc/` — cấu trúc folder + tất cả file đều là output mong muốn của skill này. Khi viết template hoặc gặp edge case, scan reference project trước khi cố nhớ.

## Output handoff template

Sau Step 8, dùng exactly format này:

```markdown
## Video preview sẵn sàng

**Studio URL:** http://localhost:3002

**Project structure:**
- Root: `<slug>/index.html` (~430 dòng)
- Sub-comps: `<slug>/compositions/` (captions + N lesson + recap + cta)
- SFX: `<slug>/sfx/` (6 files)

**Đã apply:**
- 89 caption groups synced với word-level transcript
- 6 SFX (camera-flash @ 0s, snap/whoosh/laser cho 3 lesson, ting recap, discord CTA)
- 4 source video punch zooms + N ambient ken-burns drifts
- Hook overlay 0-4s (face vẫn hiện)
- 3 full-screen lesson b-rolls với rich effects (variants per lesson)
- Recap card overlay + CTA finale

**Refresh Studio để xem.** Nói "render" khi OK, hoặc báo cụ thể chỗ cần chỉnh.
```
