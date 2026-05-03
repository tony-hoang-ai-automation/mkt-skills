# 8-Driver Comparison Rubric (1-5 scoring)

## 1. First 3 Seconds

- **1**: "Xin chào" intro, logo full screen, no hook
- **2**: Generic title card, chào mừng, brand reveal
- **3**: Question hook OR data hook, nhưng slow build
- **4**: Counter-intuitive statement OR teaser @1-2s
- **5**: Teaser final reveal + bold statement + visual stop-scroll combined

## 2. Generalist Approach

- **1**: Pure niche jargon, nói với expert (vd: "Hooks in Claude Code")
- **3**: Niche topic có explain qua analogy
- **5**: Niche topic reframed qua universal angle (vd: "Làm sao tôi tiết kiệm $10K/năm với Claude Code")

Benchmark: Graham Stephan "How I Bought Tesla for $78/month" (niche finance + mass appeal).

## 3. Viewer Connection

- **1**: "Các bạn" / "quý vị", talking at audience
- **2**: Đôi khi "bạn" nhưng generic
- **3**: "Bạn" consistent, eye contact, nhưng không predict thoughts
- **4**: Predict viewer thoughts ("Bạn có thể đang nghĩ..."), actionable value
- **5**: Full I-you connection, 1-person addressing, educational + actionable insight

## 4. Tension Building

- **1**: Linear explanation, zero tension
- **2**: 1 setup, generic payoff ở cuối
- **3**: 1 main Q resolved ở cuối, không có mini-Q
- **4**: Main Q + 2-3 mini-Qs stacked
- **5**: Teaser @0s + main Q + 4+ mini-Qs + satisfying resolution (Jenga full)

## 5. Cleverness

- **1**: Bland, expected concepts, zero creative link
- **3**: 1 analogy nhẹ, không memorable
- **5**: 2 concept không liên quan được link theo cách "tại sao mình không nghĩ ra?"

Benchmark: Grace Wells "A Very Crummy Commercial" (22M views) — spoon as cinematic commercial.

## 6. Absurdity / Novelty

- **1**: Expected script, không có gì bất ngờ
- **3**: 1 visual twist nhẹ
- **5**: Setup khiến người xem "ủa gì vậy?" trong 3s đầu, commit them to watch

Note: Absurdity không phù hợp mọi format. Fact-heavy tutorial score 3 OK.

## 7. EOV (Effect on Viewer)

- **1**: Không clear emotion mục tiêu, "chỉ là chia sẻ"
- **3**: EOV identifiable (clarity / curiosity) nhưng không mạnh
- **5**: EOV khắc sâu (aha / gut-punch / satisfaction / belonging) — viewer share vì feel mạnh

Test: Sau khi xem, viewer có thể gọi tên emotion không?

## 8. Call to Action

- **1**: Autocratic ("Mua ngay!"), reach 5%
- **2**: Mild autocratic ("Đăng ký!")
- **3**: Generic non-autocratic ("Follow nếu thích")
- **4**: Democratic hoặc Benevolent rõ ràng
- **5**: CTA organic, emerges tự nhiên sau value delivery + non-autocratic + specific next step

---

## Scoring examples

### Example A — Gold video (Tanner Leatherstein "Is it Worth It? Louis Vuitton")
- First 3s: **5** — teaser tiền + bold "Có đáng $4,500 không?"
- Generalist: **5** — niche leather + mass appeal "luxury value"
- Viewer Connection: **4** — "you" xuyên suốt, predict thoughts
- Tension Building: **5** — main Q + 3 deconstruct phases
- Cleverness: **4** — link quality craftsmanship với price philosophy
- Absurdity: **3** — deconstruct luxury là mild novelty
- EOV: **5** — aha + validation strong
- CTA: **4** — "Check our own brand if curious" benevolent
**Total: 35/40**

### Example B — Typical Bronze AI tutorial
- First 3s: **2** — "Xin chào, hôm nay..."
- Generalist: **2** — "Hooks in Claude Code" niche jargon
- Viewer Connection: **3** — "bạn" nhưng generic
- Tension: **1** — linear tutorial
- Cleverness: **2** — 0 analogy
- Absurdity: **1** — expected
- EOV: **2** — vague clarity
- CTA: **2** — "Subscribe ngay!"
**Total: 15/40**

**Gap = 35-15 = 20** → Not ready, need major rework.

---

## When to call which fix skill

| Gap location | Recommended skill |
|-------------|-------------------|
| First 3s low | `mkt-hook-kallaway` hoặc `mkt-desire-hook-for-video` |
| Generalist low | `mkt-kane-generalist-repackager` |
| Viewer Connection low | `mkt-kane-triple-f-boost` (add Feelings) |
| Tension low | `mkt-kane-reels-jenga-tension` hoặc `mkt-kane-youtube-jenga-longform` |
| Cleverness low | `mkt-kane-cross-industry-viral-scout` (tìm pattern clever từ ngành khác) |
| Absurdity low | (add manually, không có skill dedicated) |
| EOV low | `mkt-kane-eov-reverse-engineer` |
| CTA low | `mkt-kane-cta-non-autocratic-rewriter` |
| Over-brand/prod | `mkt-kane-anti-pattern-auditor` |

## Review mode differences

### Pre-production review
- Draft chưa post — fix trước khi commit production
- Focus: block critical issues
- Success criteria: score ≥28/40

### Post-mortem review
- Video đã post và underperform
- Compare thêm: actual views vs Gold views
- Output thêm: "What to change for next video" learnings
- Feed learnings vào `mkt-content-knowledge-compiler`
