# Design Tokens (Default Brand)

Default brand: Hoàng AI Marketing — Anthropic-inspired cream + burnt sienna + Be Vietnam Pro. Read `../DESIGN.md` at project root for full brand guidelines.

## Colors

```css
:root {
  /* Core palette */
  --brand-bg: #faf9f5;          /* cream paper background (light mode default) */
  --brand-surface: #e8e6dc;     /* card / surface (slightly darker cream) */
  --brand-border: #d6d3c7;      /* hairline divider */
  --brand-ink: #141413;         /* near-black text */
  --brand-ink-mute: #b0aea5;    /* secondary text */

  /* Accents */
  --brand-accent: #d97757;      /* burnt sienna — primary accent */
  --brand-accent-hover: #c46847;
  --brand-accent-2: #6a9bcc;    /* slate blue — info/link */
  --brand-accent-3: #788c5d;    /* olive — success/positive metric */

  /* Dark mode (selective use — full-screen scenes, CTA) */
  --brand-bg-dark: #141413;
  --brand-text-dark: #faf9f5;
}
```

### Per-scene background

| Scene | Background | Why |
|---|---|---|
| Hook overlay (top, 0-4s) | `rgba(250, 249, 245, 0.96)` | Cream card on top of face video |
| Lesson 1 b-roll | `#141413` (dark) | Foundational — strong contrast |
| Lesson 2 b-roll | `#faf9f5` (cream) | Alternates dark/light for visual rhythm |
| Lesson 3 b-roll | `#141413` (dark) | Most important — return to dark for emphasis |
| Recap card (overlay) | `rgba(250, 249, 245, 0.96)` | Quiet moment, cream paper feel |
| CTA b-roll | `#141413` (dark) | Conversion finale — high contrast |

### Accent rule

**Burnt sienna `#d97757`** — primary accent for all key elements:
- Lesson NUM giant text
- Title "accent" word (e.g., `<span class="accent">thử nghiệm</span>`)
- CTA pill background
- Header pill dot
- Scribble underline
- Pulse rings, light sweep
- Footer "@" character

Don't use slate blue or olive in scene b-rolls — too many accents = confused hierarchy. Reserve them for non-video assets (LinkedIn carousel, IG post).

## Typography

**Font: Be Vietnam Pro** (single-font system). Việt-first, render dấu chuẩn ở mọi size. NO Poppins/Inter/Roboto/Helvetica/Arial.

Google Fonts URL:
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&display=swap"
  rel="stylesheet"
/>
```

CSS:
```css
font-family: 'Be Vietnam Pro', 'Inter', Arial, sans-serif;
```

Inter is fallback if Be Vietnam Pro fails — has decent Vietnamese coverage. Arial last resort.

### Weight scale

| Weight | When to use |
|---|---|
| 400 Regular | Body, sub captions |
| 500 Medium | UI label, button secondary, sub |
| 600 SemiBold | Section title, kicker, button primary |
| 700 Bold | Captions on TikTok, mid-size title |
| 800 ExtraBold | Display: Lesson NUM (240px), title (130px), CTA pill |
| 400 Italic | Quote, "tâm sự" tone, sub headers ≤44px |

### Type scale (TikTok 9:16)

| Role | Weight | Size | Notes |
|---|---|---|---|
| Display NUM | 800 | 240px | line-height 0.86, tabular-nums |
| Display title | 800 | 130px | line-height 1.10, letter-spacing -0.02em |
| Hero overlay title | 800 | 78px | line-height 1.05 |
| Section / pill text | 600-700 | 60-72px | |
| Caption (TikTok) | 700 | 58-60px | line-height 1.25, padding 18px 28px |
| Eyebrow / kicker | 600 | 24-32px | letter-spacing 0.18em-0.22em, UPPERCASE |
| Sub italic | 500 italic | 26-38px | line-height 1.35 |
| Footer / meta | 600 | 28-30px | |

### Line-height for Vietnamese

- Display 60px+: `1.05–1.15` (need extra room for dấu mũ)
- Body / paragraph: `1.45`
- Caption: `1.25` (compromise — readable but compact)
- Pill / single-line: `1.0` (no wrapping)

### Letter-spacing

- Display 100px+: `-0.02em` (tight modernist look)
- Body 50px-: `0` (default)
- UI label UPPERCASE: `+0.04em` to `+0.22em` (eyebrow)

## Spacing tokens

| Token | Value | Use |
|---|---|---|
| Header pill top | `64px` | Distance from frame top |
| Hook overlay top | `170-200px` | Below header, leaves face area visible |
| Caption stage bottom | `280px` | Above footer, below face zone |
| Footer bottom | `70px` | Pill ~140px tall |
| Sub-comp content padding | `220px 80px 380px` | top, sides, bottom — keeps content centered with mobile-safe zones |

## Z-index stack

| Element | z-index | Notes |
|---|---|---|
| Source video | 1 | Background |
| Vignette | 2 | Decorative gradient |
| Recap overlay mount | 24 | Below b-roll, above source |
| Hook overlay | 28 | Above source, below header |
| Header pill | 30 | Always-on UI |
| Full-screen b-roll mount | 32 | Covers source during scene |
| Captions mount | 35 | Above b-roll for readability |
| Footer wordmark | 45 | Always on top |

## Brand voice in templates

- **Footer**: `@<handle>` (default `@tranvanhoang.com` for Hoàng) — burnt sienna `@`, ink text, cream pill bg
- **Header pill**: `<accent>N</accent> <topic>` (e.g., "3 Bài học · Alphabet") — UPPERCASE, weight 600
- **Hook eyebrow**: Một câu mô tả ngắn, UPPERCASE letter-spacing 0.18em
- **Hook title**: `<accent>N keyword</accent> mình học được` (or similar; user customizes)
- **Lesson kicker**: `Bài học #N`
- **Lesson title**: 2-3 dòng word-by-word, accent 1 keyword
- **Recap eyebrow**: `Tổng kết · N bài học`
- **CTA eyebrow**: Question that hints at value (e.g. "Muốn học Claude Code?")
- **CTA pill**: 1 word, UPPERCASE (e.g., `CODE`, `START`, `FREE`)
- **CTA sub**: 2 dòng — what user gets if they comment

## Customization

If user has different brand:
1. Replace `--brand-accent` color
2. Replace `--brand-bg` and `--brand-bg-dark`
3. Replace footer handle in templates
4. Optionally replace font (must support Vietnamese — see `feedback_vietnamese_typography.md` memory)

Don't replace fonts with Poppins/Inter/Roboto for Vietnamese audience — dấu thanh position issues.
