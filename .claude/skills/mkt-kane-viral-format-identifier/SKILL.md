---
name: mkt-kane-viral-format-identifier
description: "Phân biệt Viral Format (storytelling structure lâu dài) vs Trend (nhất thời) từ 1 video/post. Xác định 5-10 video cùng format của creator để confirm đây là format thật. USE WHEN user says 'video này dùng format gì', 'đây là trend hay format', 'xác định format viral', 'identify viral format', 'phân biệt format và trend', 'format recognition', 'video này có format lặp lại không'."
pillar: P1 + P3 (Research giai đoạn Discover)
---

# Viral Format Identifier

Skill này giúp bạn trả lời câu hỏi **"Video này thành công nhờ TREND hay nhờ FORMAT?"** — phân biệt cực kỳ quan trọng vì trend chết nhanh, format dùng lại được nhiều lần.

## Định nghĩa cốt lõi (Brendan Kane)

- **Format** = storytelling structure tái sử dụng được nhiều lần. Ví dụ: "Is it Worth It?" của Tanner Leatherstein (phân rã sản phẩm để tìm giá trị thật) — dùng được với hàng trăm sản phẩm khác nhau.
- **Trend** = fleeting phenomenon (music, meme, challenge) — chết sau 2-4 tuần.

**Quy tắc vàng**: Nếu creator dùng cấu trúc đó **≥5-10 lần** và đều có engagement rate cao → đó là **format**. Nếu chỉ 1-2 video dùng và không lặp lại → có thể là **trend/luck**.

## Input

User cung cấp 1 trong:
1. **1 video URL** — skill sẽ tìm creator's channel và check các video khác
2. **Transcript + creator name** — skill hỏi thêm 5-10 video khác của creator để compare
3. **Post text + creator** — cho Facebook/X posts

## Process

### Step 1 — Decompose video/post thành structure

List các element:
- Hook structure (opening 3-10s nói gì)
- Narrative arc (câu chuyện đi theo thứ tự nào)
- Visual pattern (shot types, transitions)
- Audio pattern (voiceover style, music, ASMR, silence)
- Payoff/ending pattern

### Step 2 — Kiểm tra repetition trong creator's account

- Visit creator profile, list 20-30 video gần nhất
- Đếm bao nhiêu video dùng CÙNG structure từ Step 1
- Engagement rate của những video đó

Threshold:
- **≥5 video lặp structure + engagement tốt** → CONFIRMED FORMAT
- **2-4 video lặp** → POSSIBLE FORMAT (cần thêm data)
- **0-1 video lặp** → TREND / LUCK / ONE-OFF

### Step 3 — Match với format có tên sẵn

Check `references/known-viral-formats.md` — có phải format đã được name như:
- Untold Stories (Daniel Wall)
- Visual Metaphor (Dr. Julie Smith)
- Is it Worth It? (Tanner Leatherstein)
- 30-Day-Challenge (Matt d'Avella)
- Walking Listicle (Robert Croak)
- Thought-Provoking Questions (Hunter Prosper)
- Progressive Reveal / Teaser-First (Mark Rober)
- Street Interview (School of Hard Knocks)
- 5-Levels-of-Difficulty (Wired)
- ASMR Deconstruction (Leatherstein)
- Meme Card + Talking Head (Dr. Mike)
- Expert Reacts
- Challenge + Expert Interview
- 1 Concept / 5 Perspectives
- Contrast Tale (2 lives, 2 outcomes)

Nếu match → đặt tên format đó. Nếu không match → đặt tên mới cho format (theo pattern "Noun + Verb-ing" vd: "Deep-Cut Revealing").

### Step 4 — List performance drivers nhận ra

Theo 5 upward drivers (Cleverness / Absurdity / Perspective Shift / Viewer Connection / Tension Building) — driver nào là CORE của format này?

VD: "Is it Worth It?" format core drivers = Perspective Shift + Cleverness (reveal giá trị thật ≠ giá bán).

### Step 5 — Recommend 3 skill trong repo để áp dụng

Format đã identified → gợi ý user nên dùng skill nào tiếp theo:
- Untold Stories → `mkt-kane-reels-untold-stories`
- Visual Metaphor → `mkt-kane-reels-visual-metaphor`
- Is it Worth It? → `mkt-kane-reels-is-it-worth-it`
- 30-Day-Challenge → `mkt-kane-youtube-30-day-challenge`
- Teaser-First longform → `mkt-kane-youtube-jenga-longform`
- Jenga tension short → `mkt-kane-reels-jenga-tension`
- Any format + GSB → `mkt-kane-gsb-research-builder` để research deeper

## Output Format

```markdown
# Format Analysis: [Creator] — [Video Title]

**Video URL**: [link]
**Creator**: @handle
**Views/Engagement**: ...
**Analyzed date**: YYYY-MM-DD

## Structure Breakdown
- **Hook**: [opening pattern]
- **Narrative arc**: [flow]
- **Visual**: [shot types]
- **Audio**: [voice/music]
- **Payoff**: [ending]

## Verdict: FORMAT / POSSIBLE FORMAT / TREND-LUCK

**Evidence**: 7/20 video gần nhất của creator dùng cùng structure → CONFIRMED FORMAT

## Format name: [Đặt tên]
Match với known format: [Untold Stories / Visual Metaphor / ... / None — brand new format]

## Core Performance Drivers
1. [Driver] — why
2. [Driver] — why

## Recommended next skills
1. `mkt-[skill-name]` — lý do
2. `mkt-[skill-name]` — lý do
3. `mkt-kane-gsb-research-builder` — để research deeper
```

## Mandatory Rules

- [ ] Không kết luận "format" nếu chưa check ≥5 video khác của creator
- [ ] Phân biệt rõ: format = structure (reusable), trend = content/sound (perishable)
- [ ] Khi match known format → dùng đúng tên trong `known-viral-formats.md`, không tự đặt tên mới
- [ ] Khi tạo tên format mới → format: "Noun + Verb-ing" hoặc "Adjective + Noun"
- [ ] Luôn recommend ≥3 skill để user có đường đi tiếp

## References

- `references/format-vs-trend-rubric.md` — Bảng phân biệt + red flags
- `references/known-viral-formats.md` — 20+ named formats với examples
