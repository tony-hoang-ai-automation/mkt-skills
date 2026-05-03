# Hoàng AI Marketing — Visual Identity

Bộ ground truth visual cho mọi nội dung của Hoàng (YouTube, Facebook, TikTok). Mọi composition trong project — title card, thumbnail, video overlay, slide, ảnh chia sẻ — đều phải truy ngược màu sắc, typography, và motion về file này.

Brand identity được align theo **Anthropic / Claude AI brand system** — warm cream paper, burnt sienna accent, editorial typography. Không phải dark dashboard cyber, không phải startup tech khoe code — mà là cảm giác "studio nghiên cứu AI ấm cúng": chuyên gia mời bạn ngồi xuống đọc một bài viết tử tế, không phải bị quăng vào terminal.

Khán giả mục tiêu: **chủ doanh nghiệp SME Việt Nam, quản lý, dân văn phòng 28–45 tuổi (TP.HCM / Hà Nội)**, không có nền lập trình. Cần cảm giác premium-mà-gần-gũi: chuyên gia AI nói chuyện với bạn như đang ngồi cùng bàn cà phê.

## Style Prompt

Visual của Hoàng là **"phòng đọc của một researcher AI"** — ánh sáng ấm trên giấy kem, một điểm nhấn cam đất (burnt sienna) như con dấu trên bìa sách. Có sự bình tĩnh của trang sách, sự rõ ràng của một bài essay được biên tập kỹ, nhưng vẫn giữ tính hành động của một builder thực thụ.

Mood: **bình tĩnh, tự tin, có chiều sâu** — một người đã đọc, đã thử, và đang chia sẻ lại. Energy 7/10 — confident nhưng không hype. Gần Anthropic hơn OpenAI — gần The New Yorker hơn TechCrunch.

Tránh: nền navy/đen tuyền, neon cyan/tím/hồng, gradient sặc sỡ, font system mặc định, hiệu ứng vlog (glitch nặng, sticker, countdown timer), cute icon kiểu dashboard SaaS, dark-mode-mặc-định.

## Colors

Palette chính thức theo Anthropic brand system. **Light mode là default** — paper-warm, không phải dark-mode.

### Core palette

| Token | Hex | Vai trò |
|---|---|---|
| `--brand-bg` | `#faf9f5` | Background chính — kem ấm như giấy in cao cấp (Anthropic Light) |
| `--brand-surface` | `#e8e6dc` | Card, panel, surface — kem đậm hơn 1 nấc (Anthropic Light Gray) |
| `--brand-ink` | `#141413` | Text chính, heading — gần đen nhưng ấm (Anthropic Dark) |
| `--brand-ink-mute` | `#b0aea5` | Text phụ, meta, caption (Anthropic Mid Gray) |
| `--brand-border` | `#d6d3c7` | Border, divider, hairline — derived từ Light Gray, đậm hơn surface |

### Accent palette

| Token | Hex | Vai trò |
|---|---|---|
| `--brand-accent` | `#d97757` | **Burnt sienna** — accent chính, signature Claude. CTA, highlight, số liệu quan trọng |
| `--brand-accent-2` | `#6a9bcc` | Slate blue — accent phụ, link, info state |
| `--brand-accent-3` | `#788c5d` | Olive green — accent thứ ba, success/positive metric |

### Dark mode (chỉ dùng cho video overlay khi cần contrast cao)

| Token | Hex | Vai trò |
|---|---|---|
| `--brand-bg-dark` | `#141413` | Background tối — Anthropic Dark, dùng cho hero scene cuối / Last Dab |
| `--brand-text-dark` | `#faf9f5` | Text trên nền tối |

### Quy tắc dùng accent

- **Burnt sienna `#d97757`** là main accent — dùng cho CTA, số liệu hero, keyword tiếng Việt cần highlight, underline link. Một frame có thể có nhiều element cam, nhưng nên giới hạn 1 element là "loud" (full saturation), phần còn lại tint nhẹ.
- **Slate blue `#6a9bcc`** chỉ dùng khi cần thông tin phụ, link, hoặc state "info" — không bao giờ thay thế cam làm accent chính.
- **Olive green `#788c5d`** cực kỳ tiết kiệm — chỉ dùng cho metric tích cực ("+147% engagement"), check icon, success badge.
- **Không bao giờ dùng cả 3 accent trong cùng 1 frame** — tối đa 2.

## Typography

Typography là **Việt-first**: chính font phải được thiết kế cho tiếng Việt, không phải font quốc tế "có thêm subset Vietnamese". Pair chính thức của brand:

- **Be Vietnam Pro** (display + body + UI) — geometric sans, do Bê font foundry (Việt Nam) thiết kế chuyên cho tiếng Việt. Dấu thanh (sắc / huyền / hỏi / ngã / nặng) và dấu chữ (ă / â / ê / ô / ơ / ư) đều render chuẩn ở mọi weight và size, kể cả size lớn 100px+ trên TikTok.
- **Lora** (optional, chỉ cho blog editorial dài) — serif transitional, có Vietnamese subset. **Không dùng cho video / caption / asset social** vì serif + dấu thanh đọc khó ở size mobile.

### Quy tắc bắt buộc

- **Mọi visual asset cho audience Việt** (video, slide, ảnh, landing page, post) chỉ dùng **Be Vietnam Pro**. Single-font system — display + body + UI cùng family, khác weight.
- **Không dùng** Poppins / Inter / Roboto / Montserrat / Helvetica / Arial / system font làm display. Những font này có subset Vietnamese nhưng dấu thanh position không chuẩn ở size lớn.
- **Fallback chain:** `'Be Vietnam Pro', 'Inter', 'Arial', sans-serif`. Inter là font dự phòng tốt nhất nếu Be Vietnam Pro chưa load (Inter có Vietnamese coverage chấp nhận được, không phải tốt nhất).

### Weight scale

| Weight | Khi nào dùng |
|---|---|
| 400 Regular | Body paragraph, caption phụ |
| 500 Medium | UI label, button secondary, sub-title |
| 600 SemiBold | Section title, button primary, kicker |
| 700 Bold | Hero headline, hook lớn, accent quan trọng |
| 800 ExtraBold | Display siêu lớn (TikTok title, hero CTA) |
| 400 Italic | Quote, pull-out, tone "tâm sự" |

### Type scale (size chuẩn)

| Role | Weight | Size (web) | Size (TikTok 9:16) |
|---|---|---|---|
| Hero headline / display | 700–800 | 56–72px | 96–130px |
| Section title | 600–700 | 32–40px | 64–80px |
| Sub-headline | 500–600 | 20–24px | 44–52px |
| UI label / pill | 500–600 | 14–16px | 28–36px |
| Body paragraph | 400 | 18–20px | 44–52px |
| Quote / italic | 400 italic | 24–28px | 36–44px |
| Caption / meta | 500 | 13–14px | 24–32px |

### Tiếng Việt — quy tắc render

- **Google Fonts URL chính thức:**
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&display=swap"
    rel="stylesheet"
  />
  ```
- **Test render** với câu có đủ dấu khó: **"Xây dựng đội ngũ bot làm việc 24/7"** — kiểm `ư`, `ạ`, `ộ`, `ũ`, `ễ` không bị crop, không overlap dòng dưới.
- **Line-height tối thiểu:**
  - Display (heading 60px+): `1.08–1.15`
  - Body / paragraph: `1.45`
  - Caption TikTok (dấu nhiều, 60px): `1.2` để dấu mũ không chạm dòng trên
- **Letter-spacing:** `-0.01em` cho display, `0` cho body, `+0.04em` cho UI label uppercase.
- **TikTok caption stroke:** `-webkit-text-stroke: 0` (Be Vietnam Pro đã đủ độ contrast với weight 700; thêm stroke làm dấu thanh lem).
- **Tránh** `font-style: italic` trên Be Vietnam Pro size lớn 80px+ — dấu thanh nghiêng dễ chạm. Dùng italic chỉ cho quote/sub-headline ≤44px.

## Logo & Wordmark

- File chính: `assets/hoang-logo.png` *(placeholder — thay bằng logo thực khi có)*
- Wordmark text: **"Hoàng"** hoặc **"Hoàng AI"** — Be Vietnam Pro Bold 700 (KHÔNG italic — geometric thẳng).
- Trên nền sáng (`--brand-bg`): logo dùng `--brand-ink` (`#141413`).
- Trên nền tối (`--brand-bg-dark`): logo dùng `--brand-bg` (`#faf9f5`).
- **Nếu cần highlight**: dùng burnt sienna `#d97757` cho 1 ký tự hoặc dấu, không dùng cho toàn wordmark.
- Glow / drop-shadow: **không dùng**. Anthropic brand là flat-paper, không glow neon.
- Clearspace: nửa chiều cao logo margin 4 phía.
- **Không** đổi màu, kéo dãn, italic hóa, hay thêm hiệu ứng ngoài spec.

Tagline đi kèm (tùy ngữ cảnh):
- "AI Freedom Builders" — tên cộng đồng, giữ tiếng Anh (power word)
- "One Person Business powered by AI" — positioning, giữ tiếng Anh
- "Xây đội bot làm việc 24/7" — bản tiếng Việt cho audience SME

## Motion Rules

- **Chỉ animate vào (entrance)** — mọi element vào bằng `gsap.from()`. Transition giữa scene tự xử lý phần thoát.
- **Bộ easing:** `power3.out`, `expo.out`, `back.out(1.4)`, `power4.out` cho entrance; `power2.in` để hand-off vào transition; `sine.inOut` cho ambient loop.
- **Mỗi scene dùng ít nhất 3 ease khác nhau** — tránh cảm giác máy móc.
- **Duration band:** entrance nhanh 0.3–0.5s, headline 0.5–0.8s, ambient drift 2–4s.
- **Offset entrance đầu tiên** 0.1–0.3s sau khi scene bắt đầu.
- **Stagger text:** 0.04–0.08s/ký tự cho display, 0.12–0.18s/từ cho headline.
- **Số chạy:** GSAP `{innerText: N, snap: {innerText: 1}}` để đếm lên, kèm `font-variant-numeric: tabular-nums`.
- **Anthropic-style hint:** motion phải có chất "paper, ink" — entrance như mực thấm vào giấy (fade + slight rise), không phải scale-bounce kiểu SaaS.

## Transitions

CSS thuần (không shader) để scene đơn giản và dễ render.

| Đổi scene | Transition | Duration | Ease |
|---|---|---|---|
| 1 → 2 | Page-turn fade | 0.4s | `power3.inOut` (mở climax, cảm giác lật trang) |
| 2 → 3 | Push slide trái | 0.35s | `power2.inOut` |
| 3 → 4 | Push slide trái | 0.35s | `power2.inOut` |
| 4 → 5 | Cream-to-ink crossfade | 0.5s | `sine.inOut` (lắng xuống vào CTA, có thể đảo light → dark) |

Default = push slide (60%). Accent = page-turn (mở đầu) + cream-to-ink (kết, dùng để chuyển sang scene CTA dark).

## Buttons / CTA

- **Primary CTA**: Pill bo `border-radius: 999px`, fill `--brand-accent` (`#d97757`), text `--brand-bg` (`#faf9f5`).
- **Secondary CTA**: Outline pill, border 1.5px `--brand-ink`, text `--brand-ink`, fill trong suốt.
- Be Vietnam Pro SemiBold 600, **không UPPERCASE bắt buộc** — Sentence case OK theo Anthropic style. UPPERCASE chỉ cho label ngắn dạng pill (max 3 từ).
- Padding: 14–18px dọc + 28–36px ngang.
- Hover: primary chuyển sang `#c46847` (burnt sienna đậm hơn 8%); secondary fill thành `--brand-ink` 100%.

**Ví dụ CTA tiếng Việt:**
```
[ Tham gia AI Freedom Builders → ]      ← primary, fill cam
[ Xem khoá học AI Agent → ]              ← secondary, outline đen
[ Tải template ngay → ]                  ← primary, fill cam
```

**Ví dụ CTA tiếng Anh (cho LinkedIn / X.com):**
```
[ Join the community → ]
```

**Quy tắc copy CTA:**
- Động từ hành động đứng đầu: "Tham gia", "Tải", "Xem", "Đăng ký".
- Power word giữ tiếng Anh khi đã quen thuộc với audience: AI, Template, Workflow, Framework, Prompt.
- Không dùng kiểu autocratic "Mua ngay!" / "Đăng ký liền!" — viết kiểu mời gọi: "Tham gia cùng cộng đồng".

## Iconography

- Stroke mỏng 1.5–2px, màu `--brand-ink` (`#141413`) trên nền sáng, hoặc `--brand-accent` (`#d97757`) khi cần highlight.
- **Không fill mass color** — chỉ outline (Anthropic icon style là editorial line-art).
- Bộ icon ưu tiên: chevron mũi tên (`›`, `→`), document/page, biểu đồ, đèn ý tưởng, dấu hỏi, dấu ngoặc kép.
- Tránh: trái tim cute, emoji-style icon, illustration nhiều màu, gradient icon, neon glow icon.

## Channel-specific Notes

| Kênh | Tỷ lệ | Đặc thù visual |
|---|---|---|
| **YouTube** (chính) | 16:9 | Thumbnail dùng face-shot Hoàng + text overlay Poppins Bold 700, 1 keyword tiếng Việt + 1 power word tiếng Anh. Background `--brand-bg` (kem) hoặc `--brand-bg-dark` (đen ấm) tùy mood video. Burnt sienna cho keyword nhấn. |
| **Facebook** | 1:1 hoặc 4:5 | Carousel post 4:5: nền kem `--brand-bg`, body Lora 400 đọc dài được, accent burnt sienna cho keyword. Tránh full-dark Facebook làm "đứt" feed. |
| **TikTok / Reels** | 9:16 | Caption burned-in bottom-third, Be Vietnam Pro Bold 700 size 56–64px, pill nền `rgba(20,20,19,0.82)` để đọc trên mọi video. Nền có thể dark (`#141413`) khi face-shot quay studio sáng — tăng contrast. KHÔNG dùng Lora / serif cho TikTok (dấu thanh + compress mạnh = vỡ). |

## What NOT to Do

1. **Không dùng nền navy / cyan / dark blue.** Brand là cream + ink, không phải Vercel/Linear dashboard. Nền dark chỉ dùng `#141413` (Anthropic Dark) khi thực sự cần.
2. **Không neon, không glow drop-shadow.** Anthropic là flat paper. Bóng đổ nếu có thì soft & subtle (`0 2px 8px rgba(20,20,19,0.08)`), không phải glow màu.
3. **Không gradient sặc sỡ** — đặc biệt purple/pink/cyan. Nếu cần gradient, chỉ subtle cream-to-light-gray (`#faf9f5 → #e8e6dc`).
4. **Không Poppins, Inter, Roboto, Montserrat, Helvetica, Arial, Roboto Mono, font system.** Chỉ Be Vietnam Pro (Lora chỉ cho blog editorial dài, không cho video/social).
5. **Không icon cute / illustration vlog / emoji as decoration.** Brand là editorial-modern, không phải dashboard playful.
6. **Không dùng keyword `transparent` trong gradient** — không tương thích shader. Dùng `rgba(250,249,245,0)`.
7. **Không `Math.random()` hay `Date.now()`** — render phải deterministic. Dùng seeded PRNG nếu cần.
8. **Không exit animation** ở mọi scene trừ scene cuối — transition lo phần thoát.
9. **Không kéo dãn logo, không italic logo, không glow logo.** Giữ aspect ratio, tôn trọng clearspace.
10. **Không lạm dụng từ tiếng Anh trong content Việt.** Chỉ giữ 3 nhóm: power words (System, Automation, Framework, Workflow, Template, AI, Prompt), tên riêng (Claude, OpenAI, ChatGPT, Anthropic), viết tắt (AI, API, SME). Mọi từ khác dịch sang tiếng Việt — đích đến "lớp 5 hiểu được".
11. **Không text quá nhỏ trên TikTok/Reels.** Min 48px cho caption, 64px+ cho headline. Mobile first.
12. **Không dùng cả 3 accent (cam + xanh + olive) trong cùng frame.** Tối đa 2.

## Brand Voice Sync

Visual phải đồng bộ với brand voice trong `MY RESOURCES/BRANDVOICE.MD`:
- **Persona xưng hô**: "mình" / "Hoàng" với "bạn" / "các bạn" — visual cũng cần warmth giấy ấm, không cold-corporate dark mode.
- **Tone 7/10**: confident nhưng không hype — không nháy 60fps liên tục, không neon, không countdown timer căng thẳng. Burnt sienna là điểm nhấn ấm, không phải red-alert.
- **Hook patterns** (Data/Shock, One Person Power, Statistic + Counter-intuition, Bold Statement): khi có hook dạng số liệu, visual hóa số đó bằng `--brand-accent` `#d97757` + Poppins Bold cỡ lớn + count-up animation.

## File References

- `assets/hoang-logo.png` — logo chính *(cần thiết kế và bổ sung theo spec mới)*
- `assets/brand-tokens.css` — CSS `:root` vars import bởi mọi composition *(cần tạo, dùng palette mới)*
- `MY RESOURCES/BRANDVOICE.MD` — quy tắc giọng văn, hook patterns, last dab framework
- `MY RESOURCES/WHO10X TECH.MD` — chân dung khách hàng SME Việt
- `CLAUDE.md` — context tổng thể project & content pillars

### Reference brand tokens (để paste vào `brand-tokens.css`)

```css
:root {
  /* Core palette — Anthropic / Claude AI */
  --brand-bg: #faf9f5;
  --brand-surface: #e8e6dc;
  --brand-border: #d6d3c7;
  --brand-ink: #141413;
  --brand-ink-mute: #b0aea5;

  /* Accents */
  --brand-accent: #d97757;       /* Burnt sienna — primary */
  --brand-accent-hover: #c46847; /* -8% lightness for hover */
  --brand-accent-2: #6a9bcc;     /* Slate blue — info/link */
  --brand-accent-3: #788c5d;     /* Olive — success/metric */

  /* Dark mode (selective use) */
  --brand-bg-dark: #141413;
  --brand-text-dark: #faf9f5;

  /* Typography — Việt-first */
  --font-display: 'Be Vietnam Pro', 'Inter', Arial, sans-serif;
  --font-body: 'Be Vietnam Pro', 'Inter', Arial, sans-serif;
  --font-editorial: 'Lora', Georgia, serif;  /* chỉ cho blog editorial dài, KHÔNG cho video */
}
```

---

**Lưu ý cho creator/AI agent**: Trước khi tạo bất kỳ visual asset nào, đọc lại file này + `BRANDVOICE.MD`. Khi có conflict giữa visual đẹp và brand voice, **brand voice thắng** — vì khán giả Việt nhớ giọng nói trước khi nhớ màu sắc. Khi có conflict giữa visual đẹp và Anthropic brand spec, **brand spec thắng** — consistency cross-platform quan trọng hơn 1 frame đẹp.
