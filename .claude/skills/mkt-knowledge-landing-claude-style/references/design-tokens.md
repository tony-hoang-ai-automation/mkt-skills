# Design tokens & Brand color reference

Tham chiếu nhanh khi outline. Tất cả token đã định nghĩa sẵn trong `assets/template.html` — cần chỉ wrap class.

## Background & ink (body)

| Token | Hex | Dùng cho |
|---|---|---|
| `bg` body | `#07070a` | Page background |
| `ink-950` | `#07070a` | Deepest panel |
| `ink-900` | `#0b0b10` | Panel base |
| `ink-800` | `#111119` | Card hover bg |
| `ink-700` | `#1a1a25` | Border accent |
| Body text | `#ECECEF` | Default text |
| White/95 | rgba(255,255,255,0.95) | Heading |
| White/65 | rgba(255,255,255,0.65) | Body lead |
| White/45 | rgba(255,255,255,0.45) | Footnote |

## Typography

| Stack | Font | Tailwind alias | Dùng |
|---|---|---|---|
| Sans | Inter | `font-sans` | Body, headings, UI |
| Mono | JetBrains Mono | `font-mono` | Code, badge, label |
| Serif (deco) | Instrument Serif italic | `font-serif italic` | Step number, image caption |

Heading sizes:
- Hero h1: `text-[44px] sm:text-7xl md:text-8xl lg:text-[120px]`
- Section h2: `text-5xl sm:text-7xl md:text-[88px]`
- Sub-headline: `text-3xl sm:text-5xl md:text-6xl`
- Stat number: `text-7xl` (display) hoặc `text-4xl` (mini)

`display` class = `font-weight: 700; letter-spacing: -0.04em; line-height: 0.98;`

## Brand color lookup

Pick brand chính từ topic của user → dùng accent đó cho gradient + dot + pill.

| Brand / Tool | Primary hex | Tailwind alias | Gradient class |
|---|---|---|---|
| **Claude / Anthropic** | `#DA7756` | `claude` | `grad-claude` |
| **DeepSeek** | `#4D6BFE` | `deepseek` | `grad-deepseek` |
| **OpenAI / ChatGPT** | `#10A37F` | `openai` | `grad-openai` |
| **Google / Gemini** | `#4285F4` | `google` | `grad-google` |
| **Mistral** | `#FF6B35` | `mistral` | `grad-mistral` |
| **Perplexity** | `#20808D` | `perplexity` | (custom) |
| **xAI / Grok** | `#1DA1F2` | `xai` | (custom) |
| **Meta / Llama** | `#0467DF` | `meta` | (custom) |
| **Microsoft / Copilot** | `#0078D4` | `msft` | (custom) |
| **Cohere** | `#FF7759` | — | (use custom) |
| **NVIDIA** | `#76B900` | — | (use custom) |
| **HuggingFace** | `#FFD21E` | — | (use custom) |

## Generic accent colors (cho stat / chip / badge)

| Accent | Hex | Khi dùng |
|---|---|---|
| Green | `#3FCF8E` | Saving, success, "code", positive |
| Amber | `#F4B860` | Highlight, warning, money, ×N |
| Purple | `#A78BFA` | AI, premium, intelligence, magic |
| Pink | `#F472B6` | Creative, design, marketing |
| Cyan | `#22D3EE` | Speed, throughput, tech infra |
| Red | `#F87171` | Bad, wrong, anti-pattern |

## Section connector

Default đường gradient dọc giữa Claude orange ↔ DeepSeek blue. Nếu page không liên quan 2 brand này, override 2 stop màu trong CSS:

```css
.connector::before {
  background: linear-gradient(to bottom,
    rgba(255,255,255,0) 0%,
    rgba({{BRAND_1_RGB}},0.55) 25%,
    rgba({{BRAND_2_RGB}},0.55) 75%,
    rgba(255,255,255,0) 100%);
  box-shadow: 0 0 18px rgba({{BRAND_1_RGB}},0.25);
}
```

## Spacing rhythm

- Section vertical padding: `pt-24 pb-24` (default), `pt-40 pb-32` (hero)
- Connector height: `180px`
- Card padding: `p-6` (mini) / `p-8` (default) / `p-10` (chart)
- Heading ↔ paragraph gap: `mt-8`
- Paragraph ↔ stats grid gap: `mt-16`
- Inline gap small: `gap-2.5` (pills), `gap-3` (icons), `gap-5` (cards)

## Icon set

**Lucide icons** (qua CDN). KHÔNG dùng emoji. Tên icon thường gặp:

- Brand: `github`, `terminal`, `cpu`, `code-2`
- Action: `arrow-right`, `arrow-up`, `copy`, `check`, `key`
- Stat: `bar-chart-3`, `trending-up`, `zap`, `sparkles`
- Concept: `git-merge`, `layers`, `unlock`, `book-open`, `image`
- UI: `chevron-down`, `external-link`

Init cuối page:
```html
<script>if (window.lucide) lucide.createIcons();</script>
```

## Responsive breakpoints

Dùng default Tailwind:
- `sm:` 640px
- `md:` 768px
- `lg:` 1024px
- `xl:` 1280px

Test: 375px (mobile), 768px (tablet), 1024px (desktop), 1440px (wide). KHÔNG cho horizontal scroll.

## Accessibility checklist

- `cursor-pointer` trên mọi clickable element
- `prefers-reduced-motion` respect (đã include trong template)
- `aria-hidden="true"` trên prompt sr-only (vì là content cho copy, không cho screen reader đọc)
- Focus state visible (default Tailwind đủ)
- Alt text cho `<img>` khi thay placeholder bằng ảnh thật
