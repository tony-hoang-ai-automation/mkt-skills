# Infographic B-Roll Design System

Hệ thống design cho b-roll talking-head video: dark glassmorphic + neon glow + UI mockup hero + floating data badges. Thay thế design "abstract decorative" (rings, light sweeps) cũ bằng "content-driven mockup" mỗi scene = 1 mockup truyền tải insight cụ thể.

**Reference**: [scaffold_infographic_v2.py](../scripts/scaffold_infographic_v2.py)

---

## Design tokens

```css
--bg-deep: #0a0815          /* deepest background */
--bg-mid: #161229           /* mid radial gradient */
--bg-card: #1f1a3d          /* card surface */
--border-glow: rgba(106, 155, 204, 0.3)

--accent-orange: #d97757    /* primary brand */
--accent-cyan: #4dd9d9      /* secondary, mockup highlights */
--accent-purple: #a774d9    /* tertiary, attribution */
--accent-green: #5dd97a     /* success, badges */

--ink: #faf9f5              /* primary text */
--ink-mute: #a8a4c4         /* secondary text */

--glow-cyan: 0 0 24px rgba(77, 217, 217, 0.55)
--glow-orange: 0 0 24px rgba(217, 119, 87, 0.55)
--glow-purple: 0 0 24px rgba(167, 116, 217, 0.55)
--glow-green: 0 0 24px rgba(93, 217, 122, 0.55)
```

**Font**: Be Vietnam Pro 400/500/600/700/800/900

---

## Scene shell (always present)

Every infographic sub-comp wraps content in this shell:

1. **Radial gradient background** — `--bg-mid` center → `--bg-deep` edges
2. **Grid lines** — 60×60px cyan grid, opacity 0.25
3. **10 SVG particles** — drifting up-down loop (sine.inOut, repeat 4)
4. **Vignette** — radial dim around center, opacity 0.4
5. **Topic pill** — circle number + UPPERCASE label, orange border + glow, slides in from top with `back.out(1.8)`
6. **Brand title** — 110px font-weight 900, accent words gradient text-clip, words slam in `back.out(1.6)` stagger 0.08
7. **Hero mockup** (variant-specific, see below)
8. **Optional floating badges** (1-4 per scene, around mockup)

---

## 7 Mockup Variants

Each scene declares `mockup_variant` in `scenes.json`. Use the variant that matches the scene's content semantics.

### 1. `post-stack` — Social media case-study posts

**Use for**: Personal branding, content marketing, posting strategy, "đăng X ngày → có Y khách"

**Visual**: 3 Facebook/LinkedIn post cards stacked. Top card highlighted with orange border + engagement stats row. Bottom 2 cards rotated/dimmed to show "more cases" depth.

**Content schema**:
```json
{
  "mockup_variant": "post-stack",
  "content": {
    "posts": [
      { "name": "Hoàng · Tư vấn AI", "time": "30 ngày trước", "body": "Case #15 — ...", "stats": ["❤️ 1.2K", "💬 87", "📨 24 inbox"] },
      { "name": "...", "time": "...", "body": "..." },
      { "name": "...", "time": "...", "body": "..." }
    ]
  }
}
```

### 2. `ai-window` — ChatGPT/Gemini mockup

**Use for**: GEO, AI search optimization, "khi khách hỏi AI thay vì Google", search-result placement

**Visual**: Chrome window with traffic-light dots + title bar. User message + AI response with recommendation card highlighted in orange glow.

**Content schema**:
```json
{
  "mockup_variant": "ai-window",
  "content": {
    "window_title": "💬 ChatGPT · Hỏi AI",
    "user_query": "Phòng khám nha khoa tốt nhất TP.HCM?",
    "ai_intro": "Một số phòng khám được đánh giá cao:",
    "rec_name": "Phòng khám của bạn",
    "rec_tag": "⭐ Top recommended · AI mentioned"
  }
}
```

### 3. `phone-call` — iPhone call screen

**Use for**: Voice AI, customer service AI, appointment booking, "lễ tân AI"

**Visual**: iPhone mockup with notch + bezel. Call status + name + 12-bar pulsing waveform + agent speech bubble + 4-slot booking grid (booked + active + open).

**Content schema**:
```json
{
  "mockup_variant": "phone-call",
  "content": {
    "call_status": "📞 Cuộc gọi đến",
    "call_name": "Nha khoa Smile · 14:32",
    "agent_tag": "🤖 AI Agent",
    "agent_text": "\"Em đặt lịch cho anh ngày mai 2pm nhé\""
  }
}
```

### 4. `dashboard` — Analytics/Ads Manager mockup

**Use for**: Performance dashboards, ad campaigns, analytics platforms, "100 mẫu/tuần", any "show the numbers"

**Visual**: Glass card with header + live status dot + 3 stat cells (one with animated count-up) + 12-creative grid (rapid pop-in + flip) + green chart line drawing.

**Content schema**:
```json
{
  "mockup_variant": "dashboard",
  "content": {
    "dashboard_title": "📊 Ads Manager · Tuần 18",
    "stats": [
      { "label": "CREATIVES", "value": "0", "color": "orange" },
      { "label": "CTR", "value": "4.2%", "color": "cyan" },
      { "label": "CPM", "value": "$3.80", "color": "green" }
    ],
    "creatives": ["💪", "🏠", "💆", "🚗", "🍕", "👗", "📱", "💎", "⚽", "📚", "🎮", "🌿"],
    "counter_target": 100
  }
}
```

The first stat cell auto-animates count-up to `counter_target` (use this for the "wow number").

### 5. `app-card` — Product / SaaS app card

**Use for**: Vertical AI products, GPT wrappers, SaaS launches, "build cuối tuần", any product-as-business

**Visual**: App card with gradient icon (rotates in 360°) + name + desc + 3 stat badges. Optional metaphor row below (source → 3 wrappers). Build pill at bottom.

**Content schema**:
```json
{
  "mockup_variant": "app-card",
  "content": {
    "app_icon": "⚡",
    "app_name": "YourNicheAI",
    "app_desc": "Wrap AI · 1 ngách · UX riêng",
    "app_stats": ["⭐ 4.9", "📈 $5M ARR", "👥 1.2K users"],
    "metaphor": {
      "source": { "icon": "⚡", "label": "AI / Điện" },
      "products": [
        { "icon": "🍞", "label": "Toaster" },
        { "icon": "☕", "label": "Ấm đun" },
        { "icon": "💡", "label": "Bóng đèn" }
      ]
    },
    "build_text": "Build trên <strong>Lovable</strong> · cuối tuần này"
  }
}
```

### 6. `team-grid` — Headcount visualization (recap default)

**Use for**: Recap "before vs after", team morphing, count-down animation. Default for `kind: recap`.

**Visual**: Headcount board with header `<from> → <to>`. 40-dot grid (5×8) pops in random stagger. Count animates 0→from, then from→to while 75% of dots fade grey (cuts). Multiplier pill drops in.

**Content schema**:
```json
{
  "mockup_variant": "team-grid",
  "content": {
    "header_label": "Headcount",
    "from_value": 160,
    "to_value": 40,
    "unit": "nhân viên",
    "multiplier": 10,
    "mult_text": "Hiệu suất tăng gấp <strong>10 lần</strong>",
    "tag": "⚡ Không phải tương lai · đang xảy ra rồi"
  }
}
```

### 7. `comment-box` — CTA Facebook/IG comment mockup (cta default)

**Use for**: CTA scenes asking viewer to comment a keyword. Default for `kind: cta`.

**Visual**: Comment box with avatar + input field (typing keyword in orange highlight) + send button. 2 gift cards stack with thumbnails + FREE green badges. Big orange CTA pill pulsing.

**Content schema**:
```json
{
  "mockup_variant": "comment-box",
  "content": {
    "avatar_letter": "B",
    "keyword": "Claude",
    "gifts": [
      { "thumb": "🎬", "tag": "VIDEO #1 · 5 TIẾNG", "title": "Claude AI cho cá nhân", "badge": "FREE" },
      { "thumb": "🎬", "tag": "VIDEO #2 · 5 TIẾNG", "title": "Claude AI cho doanh nghiệp", "badge": "FREE" }
    ],
    "cta_text": "👇 Comment ngay 👇"
  }
}
```

---

## Floating badges (optional, all variants)

Add 1-4 circular badges around the hero mockup for extra data points. Each badge auto-positions, animates entrance from off-screen, and bobs on loop.

```json
{
  "badges": [
    { "pos": "tr", "color": "orange", "icon": "📅", "num": "30", "label": "Ngày" },
    { "pos": "ml", "color": "purple", "icon": "🎯", "num": "3", "label": "Ngành" },
    { "pos": "br", "color": "green", "icon": "📨", "num": "+24", "label": "Inbox" }
  ]
}
```

- `pos`: `tl | tr | bl | br | ml | mr` (top-left, top-right, etc.)
- `color`: `cyan | purple | orange | green`
- `icon`: emoji 26px
- `num`: bold number 30px
- `label`: small UPPERCASE 14px

---

## Scene → variant mapping cheat sheet

| Scene content type | Variant | Why |
|---|---|---|
| Personal branding / posting strategy | `post-stack` | Shows the act of posting + social proof |
| AI search / SEO / GEO | `ai-window` | Shows the search interface user is replacing |
| Voice / phone / call automation | `phone-call` | Shows the actual phone interface |
| Analytics / dashboards / metrics | `dashboard` | Shows the numbers in their native UI |
| Product launch / SaaS / app | `app-card` | Shows the product as a card |
| Recap before-after / team change | `team-grid` | Shows the magnitude of change visually |
| CTA "comment X to receive Y" | `comment-box` | Shows the action user should take |

---

## Captions (critical fix)

Captions sub-comp **MUST** mount with highest `data-track-index` to render above lesson sub-comps (which have full-screen dark backgrounds):

```html
<!-- All lesson/recap/cta mounts: track-index 40-47 -->
<div class="clip" data-composition-src="compositions/fs-lesson-1.html" data-start="..." data-track-index="40"></div>
<!-- ... -->
<!-- Captions LAST with track 60 + inline z-index -->
<div class="clip captions-mount" data-composition-src="compositions/captions.html" data-start="0" data-duration="..." data-track-index="60" style="z-index: 100;"></div>
```

Without this, captions are hidden behind the dark backgrounds of lesson sub-comps.
