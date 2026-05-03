---
name: mkt-kane-cross-industry-viral-scout
description: "Tìm viral pattern ở ngành khác (bác sĩ, luật sư, tài chính, bất động sản, thủ công) có thể apply cho niche AI/automation của Hoang. Ngách AI educator VN còn ít format được khai thác — cross-industry adaptation là blue ocean. USE WHEN user says 'tìm format ngành khác', 'cross industry research', 'học format từ ngành khác', 'blue ocean format', 'tìm format chưa ai làm', 'adapt format từ niche khác', 'cross industry viral'."
pillar: P1 + P2 + P3 (Research + Ideation)
---

# Cross-Industry Viral Scout

Brendan Kane nhấn mạnh: "Study các format từ ngành có LITTLE SUCCESSFUL EXAMPLES trong niche của bạn — thường là blue ocean." Ngách AI educator tiếng Việt còn ít creator khai thác format khó, nên copy từ ngành khác là shortcut hiệu quả.

## Logic đằng sau

Audience AI không chỉ xem AI content. Họ xem doctor reacts (Dr. Mike), leather crafting (Leatherstein), challenge videos (d'Avella), finance (Graham Stephan). Format các ngành đó đã được test với audience đa dạng → bạn copy structure, đổi topic thành AI → content không đụng hàng.

## Input

1. **Topic AI** (vd: "Claude Code hooks", "MCP server", "AI agent workflow")
2. **Industries to scout** — default list (có thể customize):
   - Medicine (bác sĩ — surgery, mental health)
   - Law (luật sư — contract review)
   - Finance (money tips — Graham Stephan, Ramit)
   - Real estate (deconstruct deal)
   - Craftsmanship (leather, woodwork — Leatherstein, Malecki)
   - Food/cooking
   - Fitness
   - Comedy / prank
3. Optional: **target platform** (FB / Reels / YouTube) — ảnh hưởng lựa chọn format

## Process

### Step 1 — Scout top creators trong mỗi industry

Với mỗi industry, tìm 2-3 creator nhiều followers + engagement rate cao (không chỉ celebrity). Ví dụ default list:
- Medicine: Dr. Erin Nance (hand surgeon, 700K), Dr. Mike (12M), Dr. Julie Smith (psychology)
- Law: Erika Kullberg, LegalEagle
- Finance: Graham Stephan, Humphrey Yang, Ramit Sethi
- Real estate: Ryan Serhant
- Craftsmanship: Tanner Leatherstein, John Malecki
- Food: Joshua Weissman, BabishCulinary
- Prank/Street: Hunter Prosper, School of Hard Knocks, ThatWasEpic

### Step 2 — Identify format core của mỗi creator

Với mỗi creator, note:
- Signature format (dùng ≥5 lần)
- Core performance driver (1-2 key drivers)
- Hook pattern
- Visual/audio signature
- Length

### Step 3 — Pattern matching với AI topic

Cho mỗi format, trả lời: **"Pattern này áp dụng cho Claude Code / AI agent / automation thế nào?"**

Ví dụ:
- **Dr. Nance — dramatized medical stories** → Hoang có thể làm "dramatized AI agent mishaps" (kể câu chuyện AI agent làm sai + giải pháp)
- **Leatherstein — deconstruct luxury product** → "deconstruct AI course $500 — đáng không"
- **Graham Stephan — generalist framing** → "Làm sao tôi dùng Claude Code tiết kiệm $10K/năm" (thay vì "Claude Code Hooks Tutorial")
- **Dr. Julie Smith — visual metaphor** → "Xô nước = stress → Drill = AI agent tự drain" (minh hoạ workflow automation bằng vật lý)

### Step 4 — Score adaptation viability

Mỗi format × AI topic → score:
- **Audience overlap** (1-5): audience của creator có match persona Hoang không?
- **Structure transferability** (1-5): structure có copy được không? (VD: ASMR leather → khó copy vì AI không physical)
- **Platform fit** (1-5): hợp platform nào của Hoang?
- **Competitive advantage** (1-5): ngách AI VN đã có ai làm chưa? (càng ít càng tốt)

Total score ≥15/20 = high potential adaptation.

### Step 5 — Output top 5-10 adaptation prompts

Cho mỗi adaptation cao điểm, viết brief:

```markdown
## Adaptation #N: [Source creator] → [AI topic]

**Source format**: [name + structure tóm tắt]
**Original creator**: @handle (links)
**AI topic**: [specific]
**Core driver copied**: [1-2 drivers]
**Platform recommendation**: [Reels / YouTube / FB]
**Score**: XX/20

**Adapted hook**: "[hook mẫu VN]"
**Adapted structure**:
1. ...
2. ...

**Risk**: [cảnh báo locale / persona mismatch nếu có]
**Next skill**: `mkt-[relevant-skill]`
```

## Output Format

File: `research/cross-industry/[topic-slug]-scout.md`

## Mandatory Rules

- [ ] Scout ít nhất 5 industries, không chỉ tech-adjacent
- [ ] Mỗi format liệt kê 2+ creator reference (không 1 creator)
- [ ] Score ≥4 cross-industry ideas cuối cùng
- [ ] Cảnh báo locale issue (humor Mỹ, pacing nhanh) khi adapt cho audience VN
- [ ] Không copy content — chỉ copy STRUCTURE
- [ ] Link reference `mkt-kane-viral-format-identifier` nếu user cần deep-analyze 1 format

## References

- `references/cross-industry-adaptation-framework.md` — Framework 4 dimensions + scoring
- `references/adaptation-examples.md` — Case studies từ sách + Hoàng-specific examples
