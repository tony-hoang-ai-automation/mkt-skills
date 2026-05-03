# Split-Screen Pacing System

Layout 50/50 dọc — **top half: b-roll mockup** · **bottom half: face talking** — với **full-face breath moments** xen kẽ tại punchlines, rallying lines, và CTAs.

Đã validate trên video `6-ai-business-models-vn` (108.92s).

---

## Editorial rules — khi nào dùng full face vs split?

**🔥 GOLDEN RULE: Mỗi full-face window phải đủ dài để nói TRỌN ÍT NHẤT 1 CÂU QUAN TRỌNG.**

Không tạo "1.4s breath" làm pacing transition — full face moments phải carry meaning. Nếu chỉ có 1.4s thì hoặc giữ split, hoặc kéo dài full face đến hết câu (3-5s là phổ biến).

| Loại moment | Layout | Vì sao |
|---|---|---|
| Hook 0-3s đầu video | **Full face** | Build attention với personality |
| Liệt kê / data / mockup / so sánh số | **Split** | Cần visual để truyền tin |
| Quote ngoài đọc lên (Reid Hoffman, Daniel Priestley...) | **Full face khi đọc quote** | Audience cần thấy emotion khi quote được delivered |
| Punchline cuối mỗi ý ("dễ dàng", "thấy được") | **Full face cho NGUYÊN câu chứa punchline** (3-5s) | Câu chốt cần emotional weight |
| Rallying / emotional climax ("người Việt mình không thua") | **Full face cho NGUYÊN câu** (3-4s) | Cao trào, audience cần thấy mặt |
| CTA trực tiếp ("comment X mình tặng Y") | **Full face cho NGUYÊN câu CTA** (3+s) | Direct ask, look in the eye |
| Recap visualization (counter, comparison) | **Split** đầu, **full face** cuối | Show data → close emotional |

### How to set `brollEnd` correctly

For each scene, **identify the last important sentence** (usually the punchline, payoff line, or CTA). Set `brollEnd` to the **timestamp where that sentence STARTS** in the transcript.

Example workflow:
```bash
# Inspect caption-groups.json to find sentence boundaries
python3 -c "
import json
with open('caption-groups.json') as f: groups = json.load(f)
# Find captions in last 6s before scene end
SCENE_END = 26.40
for g in groups:
    if SCENE_END - 6 <= g['start'] <= SCENE_END:
        print(f'{g[\"start\"]:6.2f}  {g[\"text\"]}')
"
```

Look for sentence starts (capital letter after ., or natural breaths) and pick that timestamp as `brollEnd`. Common patterns:
- "Reid Hoffman nói thẳng:" → 21.30s = brollEnd for that scene
- "Vũ khí mới là PR..." → 34.08s = brollEnd
- "Mỗi khách 2 triệu một tháng" → 49.40s
- "Tìm ra mẫu thắng rồi mới đầu tư lớn" → 73.25s

**Don't pick brollEnd just by "1.5s before next scene"** — that's mechanical and creates meaningless visual breaks. Pick by SENTENCE BOUNDARY.

### Default cho 6-ý lesson video format

```
0-12s:    Full face (intro hook + stat badges floating)
For each Idea:
  - Split for first ~60-70% (mockup carries the data/visual)
  - Full face for last 30-40% — covering the FULL final sentence
    (punchline, conviction line, mini-CTA per idea)
Recap:    Split first ~60% (counter visual) → Full face last 40% (rally line)
CTA:      Split first 30% (show comment box) → Full face last 70% (direct ask)
```

**Validated example (6-ai-business-models-vn, 108.92s):**

| Scene | Split window | Full-face window | Sentence carried |
|---|---|---|---|
| Idea 1 | 12.71→21.00 (8.3s) | 21.00→26.63 (5.6s) | "Reid Hoffman nói thẳng: chọn 1 mảng, làm chủ, làm cho người ta thấy được" |
| Idea 2 | 26.63→33.80 (7.2s) | 33.80→39.57 (5.8s) | "Vũ khí mới là PR, LinkedIn, Reddit, YouTube" |
| Idea 3 | 39.57→46.50 (6.9s) | 46.50→51.93 (5.4s) | "Bao nhiêu phòng khám lỡ cuộc gọi giờ ăn trưa? Mỗi khách 2 triệu một tháng, dễ dàng" |
| Idea 4 | 51.93→59.50 (7.6s) | 59.50→64.18 (4.7s) | "Agency cũ làm vài cái 1 tháng, bạn làm 100 cái 1 tuần" |
| Idea 5 | 64.18→73.00 (8.8s) | 73.00→76.87 (3.9s) | "Tìm ra mẫu thắng rồi mới đầu tư lớn" |
| Idea 6 | 76.87→88.00 (11.1s) | 88.00→92.59 (4.6s) | "Business triệu đô. Build trên Lovable cuối tuần này" |
| Recap | 92.59→99.00 (6.4s) | 99.00→103.40 (4.4s) | "Người Việt mình không thua, chỉ là chưa biết bắt đầu" |
| CTA | 103.40→105.40 (2.0s) | 105.40→108.92 (3.5s) | "Mình gửi tặng bạn 2 video dài 5 tiếng về Claude AI cho cá nhân và doanh nghiệp" |

---

## Technical implementation

### 1. CSS (root index.html)

```css
/* Source video — full screen default, animates to bottom half during split */
#v-source {
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 25%;  /* full face mode: focus mid-upper */
  z-index: 1;
  transform-origin: center 38%;
  will-change: transform, height, top, object-position;
}

/* Split mount — scales 1080x1920 sub-comp into 1080x960 top half */
.split-mount {
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  width: 1080px !important;
  height: 960px !important;
  overflow: hidden !important;
  background: var(--bg-deep, #0a0815);
  z-index: 40;
}
.split-mount > [data-composition-id] {
  transform: scale(0.5);
  transform-origin: top center;
  width: 1080px !important;
  height: 1920px !important;
  position: absolute !important;
  left: 50%;
  margin-left: -540px;
}

/* Horizontal divider line at 50% */
#split-divider {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(217, 119, 87, 0.8) 20%,
    rgba(77, 217, 217, 0.9) 50%,
    rgba(217, 119, 87, 0.8) 80%,
    transparent 100%);
  box-shadow: 0 0 12px rgba(217, 119, 87, 0.5);
  z-index: 50;
  opacity: 0;
  will-change: opacity, transform;
}
```

### 2. HTML structure

All lesson/recap/cta mounts get `.split-mount` class:

```html
<!-- Each scene mount has split-mount class -->
<div class="clip split-mount"
     data-composition-src="compositions/fs-lesson-1.html"
     data-start="12.71" data-duration="12.19"
     data-composition-id="fs-lesson-1"
     data-track-index="40"></div>
<!-- ... -->

<!-- Divider line (positioned via CSS, animated via JS) -->
<div id="split-divider"></div>

<!-- Captions LAST with track-index 60 + z-index 100 -->
<div class="clip captions-mount"
     data-composition-src="compositions/captions.html"
     data-start="0" data-duration="108.92"
     data-composition-id="captions"
     data-track-index="60"
     style="z-index: 100;"></div>
```

### 3. Sub-comp duration shortening (critical)

For each lesson scene, **shorten data-duration by ~1.5s** so the b-roll unmounts before the next scene starts → creates a "full-face breath" window.

| Scene | Original duration | Shortened duration | Breath window |
|---|---|---|---|
| Lesson 1: 12.71→26.40 (13.69s) | 13.69 | **12.19** | 24.90→26.63 (1.73s) |
| Lesson 2: 26.63→39.30 (12.67s) | 12.67 | **11.17** | 37.80→39.57 (1.77s) |
| Lesson 3-6 | similar | each -1.5s | similar |

For **recap + CTA** that need full-face climax at END, shorten data-duration to match the split portion only:

| Scene | Original | Shortened | Why |
|---|---|---|---|
| Recap: 92.59→103.20 (10.61s) | 10.61 | **6.41** | Split for counter/×10, then 4.2s full face for rally line |
| CTA: 103.40→108.92 (5.52s) | 5.52 | **2.00** | Split shows comment box for 2s, then 3.5s full face direct ask |

### 4. JS animation system

Drop this into root index.html `<script>` after main timeline setup:

```js
const SCENES = [
  { id: "fs-lesson-1", start: 12.71, brollEnd: 24.90, hasBreath: true },
  { id: "fs-lesson-2", start: 26.63, brollEnd: 37.80, hasBreath: true },
  { id: "fs-lesson-3", start: 39.57, brollEnd: 50.20, hasBreath: true },
  { id: "fs-lesson-4", start: 51.93, brollEnd: 62.45, hasBreath: true },
  { id: "fs-lesson-5", start: 64.18, brollEnd: 75.15, hasBreath: true },
  { id: "fs-lesson-6", start: 76.87, brollEnd: 90.90, hasBreath: true },
  // Recap: split first ~60% then full face for rally line
  { id: "recap-card",  start: 92.59, brollEnd: 99.00, hasBreath: true },
  // CTA: split first ~30% (show what to do) then full face for direct ask
  { id: "fs-cta",      start: 103.40, brollEnd: 105.40, hasBreath: true },
];
const TRANSITION_DUR = 0.45;
const PRE_SHRINK = 0.3;  // shrink starts 0.3s before scene begins

// Helper: shrink face → bottom half · show divider · move captions to center
function goSplit(t) {
  tl.to("#v-source", {
    height: "50%", top: "50%",
    objectPosition: "center 15%",  // shift focus up so face stays visible
    duration: TRANSITION_DUR, ease: "power2.inOut",
  }, t);
  tl.to("#split-divider", { opacity: 1, duration: 0.35 }, t + 0.1);
  tl.to('[data-composition-id="captions"] .caption-stage', {
    bottom: 920, duration: TRANSITION_DUR, ease: "power2.inOut",
  }, t);
}

// Helper: expand face → fullscreen · hide divider · captions back to bottom
function goFull(t) {
  tl.to("#v-source", {
    height: "100%", top: "0%",
    objectPosition: "center 25%",
    duration: TRANSITION_DUR, ease: "power2.inOut",
  }, t);
  tl.to("#split-divider", { opacity: 0, duration: 0.3 }, t);
  tl.to('[data-composition-id="captions"] .caption-stage', {
    bottom: 160, duration: TRANSITION_DUR, ease: "power2.inOut",
  }, t);
}

// Initial caption position
tl.set('[data-composition-id="captions"] .caption-stage', { bottom: 160 }, 0);

// Walk all scenes — split at start, full at brollEnd if hasBreath
SCENES.forEach((sc) => {
  goSplit(sc.start - PRE_SHRINK);
  if (sc.hasBreath) {
    goFull(sc.brollEnd);
  }
});

// Divider pulse loop while visible (subtle)
tl.to("#split-divider", {
  scaleY: 1.4, duration: 1.2, ease: "sine.inOut",
  yoyo: true, repeat: 60, transformOrigin: "center center",
}, 13.0);
```

---

## Caption position values

```
bottom: 160px  → captions at bottom area (full-face mode)
bottom: 920px  → captions vertically centered on screen (split mode)
```

`bottom: 920px` puts the caption text right around y=960 (frame center) — at the divider line area, visible to viewer regardless of where the face is.

---

## Source video object-position values

```
object-position: center 25%   → full-face mode (mid-upper focus, default)
object-position: center 15%   → split mode (more head visible in shorter frame)
```

Tweak by ±5% if face crops too tight at top/bottom.

---

## Hard rules

1. **Sub-comp data-duration MUST be shortened** by ~1.5s for lessons that have breath. Otherwise b-roll covers the face during fullscreen moment.
2. **Captions sub-comp track-index 60+ with `style="z-index: 100"`** — otherwise hidden behind .split-mount (which has z-index 40).
3. **`.split-mount` background must match the sub-comp's gradient bg** (`var(--bg-deep, #0a0815)`) — otherwise side bars from `transform: scale(0.5)` show as jarring black.
4. **Recap + CTA always need breath at end** — they're emotional/action moments, never full-split through end.
5. **First lesson PRE_SHRINK = 0.3s** — too long and intro feels rushed; too short and split appears jarringly mid-sentence.
