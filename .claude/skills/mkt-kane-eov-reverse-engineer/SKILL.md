---
name: mkt-kane-eov-reverse-engineer
description: "Bắt đầu ideation từ Effect on Viewer (emotion/reaction mong muốn) → reverse-engineer ra format + hook + tactic + Last Dab. Ngược với cách thường (có message → tìm cách truyền đạt). Áp dụng cho FB post / Reels / YouTube. USE WHEN user says 'ideation từ cảm xúc', 'start với eov', 'muốn viewer cảm thấy x', 'reverse engineer content', 'eov đi trước', 'thiết kế cảm xúc trước', 'design for emotion', 'eov first'."
pillar: Cross-pillar (ideation)
---

# EOV Reverse-Engineer

Brendan Kane: **"Start with the desired Effect on Viewer."** Thay vì "Tôi có message X, làm sao truyền đạt?", hỏi: "Tôi muốn viewer cảm thấy X — tactic nào tạo được X?"

Example từ sách:
- Music producer viết bài dance → bắt đầu với "muốn người nghe nhún nhảy" → chọn tempo + drum → sau đó viết melody
- MetLife *My Dad Is a Liar* → bắt đầu với "muốn viewer khóc" → chọn story of daughter POV → sau đó fit message insurance vào

## EOV Taxonomy

### Knowledge-based EOVs
- **Clarity** — "Giờ tôi hiểu rồi"
- **Curiosity** — "Muốn biết thêm"
- **Aha moment** — "Sao mình không nghĩ ra?"
- **Perspective shift** — "Mình đã nghĩ sai bấy lâu"

### Emotional EOVs
- **Inspiration** — "Muốn làm ngay"
- **Validation** — "Mình không cô đơn"
- **Belonging** — "Cộng đồng này cho mình"
- **Satisfaction** — "Đã xem xong thấy đầy đủ"
- **Gut-punch** — "Thay đổi cách tôi nhìn"
- **Calm** — "Bình an sau khi xem"

### Action-based EOVs
- **Urgency** — "Phải bắt đầu ngay" (careful with autocratic)
- **Excitement** — "Muốn thử liền"
- **Confidence** — "Tôi làm được"

## Input

1. **Desired EOV** (pick 1 primary, max 1 secondary)
2. **Platform**: FB post / Reels / YouTube
3. **Topic context** (nếu có — giúp chọn tactic relevant)
4. **Persona nhắm** (default SME 28-45 VN theo WHO10X TECH.MD)

## Process

### Step 1 — Clarify EOV

Hỏi user câu hoàn chỉnh: "Sau khi xem xong, viewer nên cảm thấy/nghĩ gì?"

VD output:
> EOV primary: Aha moment về AI agent
> EOV secondary: Belonging (cộng đồng AI Freedom Builders)

### Step 2 — Map EOV → Format candidates

Theo `references/eov-to-tactic-map.md`:

| EOV | Best formats |
|-----|-------------|
| Aha / Perspective Shift | Myth-bust, Is it Worth It?, Counter-intuitive |
| Curiosity | Teaser-first, Untold Stories, Jenga |
| Satisfaction | Visual Metaphor, ASMR Deconstruction |
| Inspiration | 30-Day-Challenge, Transformation |
| Validation | Personal story, "I used to think..." |
| Gut-punch | Contrast Tale, Two Lives |
| Clarity | Listicle, Progression, 5-Levels |
| Calm | Slow-pace vlog, Meditation-style |
| Belonging | Community story, BIP post |
| Urgency | Deadline + concrete stakes (non-autocratic) |

Pick 2-3 format candidate.

### Step 3 — Suggest 5 hook options

Cho mỗi format, write 1-2 hook cụ thể. Minimum 5 hooks total.

Hook must hint at EOV trong 3s đầu.

VD EOV = Aha + format Is it Worth It?:
- "Khóa AI $500 — tôi chi $12K rồi, đây là câu trả lời thật"
- "Hầu hết khóa AI VN bán đắt gấp 10 lần giá trị thật — đây là cách check"

### Step 4 — Suggest 3 tactics

Pick tactics match EOV target:
- **Music**: upbeat (excitement), silent (clarity), ambient (calm)
- **Visual**: fast cut (urgency), slow zoom (satisfaction), split-screen (contrast)
- **Pacing**: 1 second/shot (energy), 3-5 second/shot (reflection)
- **Cadence**: energetic (fun), measured (authority), conversational (connection)

### Step 5 — Suggest Last Dab (brand voice rule)

Last Dab = closing punchline memorable. Viết ngay câu này TRƯỚC — rồi mới fill middle.

VD cho EOV Aha:
- "Trả tiền cho tool, đừng trả tiền cho curse."
- "AI không magic — nó là leverage."

### Step 6 — Output ideation brief

Compile brief sẵn sàng để user feed vào skill writing.

## Output Format

```markdown
# EOV Reverse-Engineered Brief

**EOV Primary**: [emotion] — "Sau khi xem, viewer cảm thấy ..."
**EOV Secondary**: [optional]
**Platform**: FB / Reels / YouTube
**Topic**: [if given]

## Format Candidates (ranked)
1. **[Format name]** — why fit EOV
2. **[Format name]** — why fit EOV
3. **[Format name]** — why fit EOV

## 5 Hook Options
1. "[Hook 1]"
2. "[Hook 2]"
3. "[Hook 3]"
4. "[Hook 4]"
5. "[Hook 5]"

## 3 Tactic Suggestions
- **Music**: [specific]
- **Visual**: [specific]
- **Pacing/Cadence**: [specific]

## Last Dab (write this first)
"[Closing punchline]"

## Recommended next skill
- `mkt-reels-[format]` / `mkt-youtube-[format]` / `mkt-fb-post-[format]` — để viết full content
```

## Mandatory Rules

- [ ] Chỉ pick 1 primary EOV (tránh blur)
- [ ] Last Dab viết TRƯỚC hook (theo rule BRANDVOICE.MD)
- [ ] Hook phải hint EOV trong 3s đầu
- [ ] Không gợi Autocratic CTA cho bất kỳ EOV nào — kể cả "Urgency"
- [ ] Recommend skill writing chính xác theo format đã pick

## References

- `references/eov-to-tactic-map.md` — Mapping EOV → format + tactics
