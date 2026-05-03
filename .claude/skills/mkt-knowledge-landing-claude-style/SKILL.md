---
name: mkt-knowledge-landing-claude-style
description: Tạo single-page landing website (HTML đơn file dùng Tailwind CDN + Lucide icons + Chart.js) trình bày nội dung video chia sẻ kiến thức AI/tech theo design language của Claude AI. Body dark navy theme + accent màu thương hiệu (Claude orange, DeepSeek blue, OpenAI green, etc.); infographic placeholder dùng style cream hand-drawn editorial của Claude AI. Scroll-down dọc, vertical connector lines giữa section, big hero typography với gradient highlight cho keyword thương hiệu, 3-column stats cards, Chart.js benchmarks, image placeholder kèm prompt ẩn (chữ tiếng Việt có dấu, giữ tiếng Anh cho brand/tech) — chỉ hiện nút Copy. Khi user đưa transcript / topic / tài liệu, skill tự outline section, viết Vietnamese copy, viết image prompt Claude-AI-editorial-style, build HTML. Optional bước cuối — gọi mkt-broll-image để generate ảnh thật qua AI33 (Nano Banana Pro). USE WHEN user says 'tạo landing page kiến thức', 'website 1 trang scroll', 'tạo trang trình bày video AI/tech', 'Claude AI style landing', 'transcript thành landing page', 'one-page knowledge website', 'tạo website chia sẻ kiến thức scroll dọc', 'knowledge sharing landing page', 'website giới thiệu video chia sẻ'.
---

# mkt-knowledge-landing-claude-style

Tạo landing page 1 trang (scroll-down) trình bày 1 chủ đề kiến thức AI/tech, thiết kế theo design language Claude AI: dark navy body với accent màu thương hiệu, vertical connector lines, big hero typography, stats cards, Chart.js, image placeholder kèm prompt Claude-AI-editorial-style ẩn (chỉ hiện nút Copy).

## Khi nào dùng

User muốn turn 1 nội dung — video transcript, blog post, hoặc đơn giản là 1 topic + intent — thành **website 1 trang scroll** để chia sẻ kiến thức trên social/portfolio. Đây không phải slide deck (không dùng `marp` / `slidev`), không phải multi-page site, không phải lead-gen quiz (đã có `landing-page-content-creator` cho việc đó).

Ví dụ phù hợp:
- "Tạo landing page chia sẻ video về DeepSeek V4 + Claude Code"
- "Làm trang web 1 trang scroll giới thiệu agent N8n"
- "Convert transcript này thành knowledge landing"

## Inputs cần có từ user

Trước khi build, hỏi (hoặc parse từ message của user) những thứ sau. Nếu user không đưa, infer reasonable default rồi confirm.

| Input | Bắt buộc | Default |
|---|---|---|
| Topic / chủ đề | ✅ | — |
| Brand được nhắc đến (Claude / DeepSeek / OpenAI / ...) | ✅ | infer từ topic |
| Tài liệu nguồn (transcript / blog / key points) | optional | — |
| Target audience | optional | "Việt Nam, AI/tech learner" |
| Output folder | optional | `output/<slug>/` (folder, không phải file đơn) |
| Số section (ngoài hero) | optional | 5–7 |

## Output structure

Skill này luôn output 1 **folder** (không phải 1 file đơn lẻ). Cấu trúc:

```
output/<slug>/
├── <slug>.html       ← landing page chính, tên file = slug của topic
├── prompts.md        ← danh sách prompt cho từng ảnh, copy-paste để gen thủ công
├── 1.png             ← user tự gen rồi đặt vào (skill KHÔNG tự gen)
├── 2.png
└── ...
```

- **Folder name**: slug của topic (vd. `deepseek-v4-claude-code`, `n8n-ai-agent-vs-zapier`).
- **HTML filename**: trùng folder name + `.html`.
- **prompts.md**: file Markdown liệt kê toàn bộ prompt theo thứ tự `1.png`, `2.png`, ... User copy từng prompt → paste vào AI33 / Nano Banana Pro / Midjourney → save về cùng folder.
- **Image files**: HTML tự nhận khi user thêm vào folder (xem `<img>` + `onerror` fallback trong `assets/template.html`). Chưa có ảnh → hiện placeholder dashed border. Có ảnh → render full đẹp ngay không cần edit HTML.
- **Skill KHÔNG tự gọi AI gen ảnh** — chỉ output prompt. Nếu user muốn auto-gen, chạy `mkt-broll-image` riêng từng prompt (xem mục "Tích hợp mkt-broll-image").

## Workflow

### Bước 1 — Hiểu intent & outline

Đọc tài liệu (nếu có) hoặc bám topic. Identify **brand chính** (1–2 brand) → tra `references/design-tokens.md` để pick accent color. Outline 5–7 section ngoài hero:

| # | Section archetype | Khi nào dùng |
|---|---|---|
| 01 | **WHAT IS X** | giới thiệu chủ thể chính (model / tool / framework) — pattern: stats cards 3-column |
| 02 | **THE VALUE / SAVINGS** | lý do quan trọng (cost, time, quality) — pattern: image-placeholder + 3 mini-stats |
| 03 | **BENCHMARKS / DATA** | so sánh số liệu — pattern: Chart.js bar chart |
| 04 | **HOW IT WORKS** | mechanism, architecture — pattern: image-placeholder (visual thinking diagram) |
| 05 | **STEP BY STEP** | hướng dẫn dùng — pattern: 4 step cards với code snippet |
| 06 | **WHEN TO USE WHICH** | comparison decision — pattern: 2-column compare |
| 07 | **GET STARTED** | CTA — pattern: code block + 3 link cards |

Linh hoạt — bỏ section không phù hợp, đổi thứ tự nếu logic kể chuyện cần. Mỗi landing page nên có **ít nhất 1 image placeholder** và **ít nhất 1 stats hoặc chart section**.

### Bước 2 — Viết Vietnamese copy

Quy tắc copy:
- Headlines section: **mix Anh-Việt OK**, keyword brand giữ English (DeepSeek V4, Claude Code), từ chuyên ngành OK English. Sub-headline có thể tiếng Anh ngắn gọn (như "Same workflow. 3000× less money.").
- Body paragraph: **tiếng Việt có dấu đầy đủ**, brand/tech keyword giữ tiếng Anh. Tone: educational, professional, friendly. LLM xưng "tôi", gọi user là "anh" (theo CLAUDE.md ở `hoang_brain`).
- Section badge marker: `• 0N · TITLE_IN_ENGLISH` (như `• 02 · THE SAVINGS`).
- Annotation labels: tiếng Việt ngắn, có dấu.

### Bước 3 — Apply gradient highlight cho keyword

Trong heading lớn (h1, h2 hero và section), wrap keyword brand bằng class gradient tương ứng:

```html
<span class="grad-claude">Claude Code</span>
<span class="grad-deepseek">DeepSeek V4</span>
<span class="grad-green">code</span>
<span class="grad-amber">3000×</span>
<span class="grad-purple">AI</span>
```

Class gradient đã định nghĩa sẵn trong `assets/template.html`. Nếu brand chưa có sẵn, thêm vào `<style>` block theo pattern.

### Bước 4 — Generate image prompt

Mỗi image placeholder cần 1 prompt **theo Claude AI editorial signature style**. Đọc `references/infographic-prompt-template.md` để có rule chi tiết. Quy tắc cứng:

1. **Background**: warm cream `#F0EEE6` — KHÔNG vintage, KHÔNG parchment, KHÔNG aged texture.
2. **Style**: hand-drawn editorial line art với subtle warm color fills (như spot illustration trên claude.ai marketing pages).
3. **Visual thinking metaphor**: mỗi ảnh phải có ẩn dụ trực quan dễ hiểu (heo đất vỡ vs két sắt nhỏ; ống nước nối terminal qua proxy; gear-and-pipe cho mechanism; cầu thang cho progression...).
4. **Text trong ảnh**: TẤT CẢ tiếng Việt có dấu đầy đủ. CHỈ giữ tiếng Anh cho:
   - Brand names (CLAUDE OPUS, DEEPSEEK V4, OPENAI, ANTHROPIC, MIT…)
   - Technical keywords (TERMINAL, PROXY, API, MoE, SDK, CLI…)
   - Inline code (`$ claude`, `:8082`, `npm`…)
   - Currency / math symbols ($, %, ×, ₫…)
5. **Palette**: cream bg + dark slate text + Claude orange `#DA7756` + brand-color tương ứng + accent (green `#3FCF8E` cho saving / amber `#F4B860` cho highlight / etc.).
6. **Aspect ratio**: 16:10 (default) hoặc 16:9 cho diagram dài.

### Bước 5 — Đặt tên file ảnh theo số thứ tự

**Convention**: ảnh đánh số tăng dần — `1.png`, `2.png`, `3.png`, ... — KHÔNG đặt tên theo nội dung (không phải `phep-tinh-infographic.png` hay `dual-terminal-diagram.png`). Lý do: dễ tracking, dễ replace, dễ rename về sau.

Trong HTML placeholder tag: `▮ IMAGE PLACEHOLDER #N — N.png` (N là số thứ tự xuất hiện trong page, đếm từ 1).

### Bước 6 — Assemble HTML

Bắt đầu từ `assets/template.html` (skeleton có đủ Tailwind config + CSS tokens + script). Inject section bằng snippet trong `references/section-patterns.md`. Với mỗi snippet, copy-paste rồi điền nội dung — đừng tự viết lại CSS, dùng class có sẵn (`.card`, `.pill`, `.badge`, `.connector`, `.ph`, `.code`, `.step-num`, `.chip-good`, etc.).

**Section connector**: chèn `<div class="connector"></div>` giữa mỗi 2 section. Đường gradient dọc nối có **animated color flow** (gradient chạy + traveling pulse dot di chuyển xuống) — hiệu ứng mặc định đã có trong `template.html` qua CSS keyframes `@keyframes flow` + `@keyframes travel`. Tự động tắt khi `prefers-reduced-motion: reduce`.

#### 6a — Pro polish bằng `ui-ux-pro-max` (recommended)

Trước khi viết HTML, gọi `ui-ux-pro-max` skill để get extra design intelligence — animation patterns, hover micro-interactions, accessibility checks. Đặc biệt hữu ích khi:
- User yêu cầu "giao diện chuyên nghiệp", "có nhiều hiệu ứng", "polish hơn".
- Topic phức tạp cần multi-section logic flow.
- Muốn brand color mới chưa có trong design-tokens.

```bash
python3 /Users/tonyhoang/Documents/GitHub/hoang_brain/.claude/skills/ui-ux-pro-max/scripts/search.py \
  "<topic> <brand> AI dev tool dark futuristic" \
  --design-system -p "<Project Name>"
```

Lấy phần **KEY EFFECTS** + **PATTERN** + **PRE-DELIVERY CHECKLIST** từ output → áp dụng:
- Hover micro-interactions (scale, color-shift, shadow lift).
- Scroll-triggered animations (fade-up, slide-in) — dùng IntersectionObserver hoặc CSS-only (sticky + clip).
- Section transition cues (parallax orbs, gradient bleed giữa sections).
- Bổ sung CSS keyframes mới ngoài `flow`/`travel` đã có.

Tóm tắt brief từ ui-ux-pro-max cho user trước khi build, để confirm direction. KHÔNG override identity Claude AI dark theme — chỉ thêm polish lớp trên.

### Bước 7 — Image slot trong HTML + prompts.md riêng

Slot ảnh trong HTML dùng pattern `<img>` + `onerror` fallback. Khi file `N.png` chưa có trong folder → hiện placeholder dashed border. Khi user thêm ảnh vào → tự động render full.

```html
<div class="ph aspect-[16/9] max-w-5xl mx-auto" id="img-slot-{N}">
  <img src="{N}.png" alt="{ALT_TEXT_VI}"
       class="w-full h-full object-cover rounded-[20px]"
       onload="this.parentElement.classList.add('img-loaded')"
       onerror="this.remove()" />
  <span class="ph-tag">▮ {N}.png — chưa có ảnh</span>
  <span class="ph-aspect">16 : 9</span>
  <div class="ph-center">
    <div class="icon-box"><i data-lucide="image" class="w-7 h-7 text-claude"></i></div>
    <div class="font-serif italic text-2xl text-white/80 mb-2">{TIÊU ĐỀ TIẾNG VIỆT}</div>
    <div class="font-mono text-xs text-white/40 max-w-md">
      Xem prompt #{N} trong <code>prompts.md</code>
    </div>
  </div>
</div>
```

CSS `.img-loaded` ẩn các element placeholder khi `<img>` load thành công (đã có trong template.html).

Prompt **KHÔNG nhúng vào HTML** nữa — viết vào file riêng `prompts.md` cùng folder. Format:

```markdown
# Image prompts — {{TITLE}}

Tổng cộng N ảnh. Đặt tên `1.png`, `2.png`, ..., `N.png` cùng folder. HTML tự load.

## 1.png — {{TIÊU_ĐỀ_NGẮN}}

[Aspect: 16:9 · Provider gợi ý: AI33 / Nano Banana Pro · Resolution: 2K]

{{FULL_PROMPT_CLAUDE_AI_EDITORIAL_STYLE}}

---

## 2.png — ...
```

Template chi tiết: `assets/prompts-template.md`.

### Bước 8 — Save folder & confirm

Tạo folder `output/<slug>/` rồi save 2 file:
1. `<slug>.html` — landing page chính.
2. `prompts.md` — danh sách prompt cho từng ảnh, format theo `assets/prompts-template.md`.

Mở browser preview (`open output/<slug>/<slug>.html`). Báo cho user:
- Path tới folder.
- Số image placeholder cần gen (N).
- Hướng dẫn: "Anh copy từng prompt trong `prompts.md` rồi paste vào AI33/Nano Banana Pro, save ảnh về cùng folder, đặt tên `1.png`, `2.png`, ... HTML sẽ tự nhận khi anh refresh trang."

### Bước 9 — Optional: gọi mkt-broll-image gen ảnh

Nếu user muốn tự động hoá: hỏi "Anh muốn tôi gen luôn N ảnh placeholder bằng `mkt-broll-image` (AI33 / Nano Banana Pro) không?"

Nếu yes, **với mỗi prompt** trong `prompts.md`:
```bash
python3 .claude/skills/image-post-creator/scripts/generate.py \
  '<PROMPT_NGẮN_GỌN_<2K_CHARS>' \
  -o output/<slug>/N.png \
  -ar 16:9 \
  -p ai33 \
  --size 2K \
  -v
```

⚠️ **Cảnh báo prompt length**: AI33 dễ trả `temporary_model_error` khi prompt dài >2000 chars. Khi auto-gen, **rút ngắn prompt** xuống ~1500-2000 chars: giữ layout description + visual metaphor + brand colors, bỏ bớt text annotation thừa và mô tả style lặp. Bản đầy đủ vẫn lưu trong `prompts.md` cho user dùng tay.

⚠️ **Aspect ratio**: AI33 KHÔNG hỗ trợ 16:10 — phải dùng `16:9` (gần nhất). Ảnh ra 1344×768 (2K). Trong HTML đã set placeholder `aspect-[16/9]` mặc định.

## Files trong skill này

```
mkt-knowledge-landing-claude-style/
├── SKILL.md                          (file này)
├── assets/
│   ├── template.html                 (skeleton để fork — copy & fill)
│   ├── prompts-template.md           (template file prompts.md output)
│   └── examples/
│       └── deepseek-v4-claude-code.html  (case hoàn chỉnh tham khảo)
└── references/
    ├── design-tokens.md              (palette + typography + brand color lookup)
    ├── section-patterns.md           (HTML snippet cho mỗi loại section)
    └── infographic-prompt-template.md (rule viết prompt Claude AI editorial)
```

## Quick reference — Section archetypes

Khi outline section, chọn pattern phù hợp từ bảng dưới. Snippet HTML chi tiết xem `references/section-patterns.md`.

| Pattern | Dùng cho | Visual hook |
|---|---|---|
| **hero** | Mở đầu | Pills row + display heading + dual CTA + meta |
| **stats-3col** | What is X — đặc tính số | 3 cards với số to gradient |
| **image-placeholder** | Concept cần ẩn dụ | Cream infographic + Copy prompt button |
| **chart** | Benchmark / so sánh số | Chart.js bar chart |
| **comparison-2col** | When to use which | 2 cards Yes/Yes với chip |
| **step-cards** | How to use | 4-col cards với serif step number + code |
| **code-block** | CTA cài đặt | macOS-style terminal frame + copy all |
| **link-cards** | Outbound | 3-col card với icon + label |

## Quick reference — Brand color (đầy đủ trong `references/design-tokens.md`)

| Brand | Primary | Tailwind alias |
|---|---|---|
| Claude / Anthropic | `#DA7756` | `claude` |
| DeepSeek | `#4D6BFE` | `deepseek` |
| OpenAI / ChatGPT | `#10A37F` | `openai` |
| Google / Gemini | `#4285F4` | `google` |
| Mistral | `#FF6B35` | `mistral` |
| Perplexity | `#20808D` | `perplexity` |
| xAI / Grok | `#1DA1F2` | `xai` |
| Meta / Llama | `#0467DF` | `meta` |
| Microsoft / Copilot | `#0078D4` | `msft` |

## Anti-patterns

❌ Vintage parchment / Da Vinci style trong infographic — đã reject.
❌ Image filename theo nội dung (`savings.png`, `diagram.png`) — phải đánh số `1.png` `2.png`.
❌ Hiện prompt text dạng block visible — phải nằm trong `prompts.md` (file riêng), KHÔNG nhúng vào HTML.
❌ Output 1 file HTML đơn — phải là folder `output/<slug>/` chứa HTML + prompts.md + ảnh.
❌ Emoji icon — luôn dùng Lucide SVG.
❌ Light mode — landing này luôn dark navy (Claude AI dark theme).
❌ Slide-deck layout — đây là scroll-down web, không phải slide.
❌ Tự code CSS từ đầu — luôn fork `assets/template.html`.
❌ Tiếng Anh trong body Vietnamese — chỉ giữ Anh cho brand/tech keyword.
❌ Connector tĩnh — phải có animation (flow gradient + traveling dot).
❌ Auto-gen ảnh không hỏi user — user là người quyết định gen tay hay auto.

## Không làm

- Không tạo multi-page site — skill này chỉ cho 1 folder + 1 file HTML.
- Không generate ảnh tự động trừ khi user đồng ý.
- Không quên `<div class="connector"></div>` giữa các section — signature design.
- Không quên `prefers-reduced-motion` + `cursor-pointer` + Lucide initialization.
- Không gọi AI33 với prompt > 2000 chars — sẽ trả `temporary_model_error`.
