---
name: mkt-kane-triple-f-boost
description: "Retrofit (viết lại) bài Facebook / script Reels / script YouTube có sẵn để đạt blend Feelings (30%) + Facts (25%) + Fun (20%) — tổng ≥75% theo Communication Algorithm của Brendan Kane. Đồng thời loại bỏ Values-based và Autocratic phrasing. Dùng khi audit thấy content đang heavy 1 style. USE WHEN user says 'triple f boost', 'viết lại theo feelings facts fun', 'enhance content', 'content thiếu cảm xúc', 'content khô quá', 'thêm fun vào bài', 'rewrite content đa dạng', 'cân bằng feelings facts fun'."
pillar: Cross-pillar (retrofit tool)
---

# Triple F Boost — Communication Algorithm Rewrite

Brendan Kane: **75% dân số** giao tiếp qua Feelings (30%) + Facts (25%) + Fun (20%). Nếu content của bạn chỉ heavy 1 style, bạn đang alienate 45-70% audience. Skill này rewrite để blend đủ 3.

## Vocabulary cue cho từng style

### Feelings (30% population)
- "Tôi cảm thấy..." / "Mình thấy..."
- "Mình quan tâm..." / "Mình lo..."
- "Tôi yêu..." / "Mình ghét..."
- "Bình an" / "Ấm áp" / "Lo lắng" / "An toàn"
- Tone: gentle, empathetic, connecting

### Facts (25% population)
- "Theo dữ liệu X..."
- "Nghiên cứu Y cho thấy..."
- Số cụ thể: 87%, 3 ngày, $500
- Who / what / when / where / how much
- "Based on...", "So sánh giữa A và B..."
- Tone: neutral, clear, non-biased

### Fun (20% population)
- "Wow!" / "Tuyệt!" / "Hài quá"
- "Yo, cái này..." / "Đỉnh thật"
- Exclamation marks, dynamic pacing
- Playful analogies, unexpected twist
- Tone: high-energy, enthusiastic, spontaneous

### TRÁNH (alienate 85%)
- **Values-based** (Opinions 10%): "Cách này là đúng nhất", "Bạn PHẢI làm vậy"
- **Autocratic** (Actions 5% only): "Mua ngay!", "Làm đi!", "Đừng bỏ lỡ!"

## Input

Content có sẵn (post text / script):
- Độ dài bất kỳ
- Platform: FB / Reels / YouTube
- Original state

## Process

### Step 1 — Score content hiện tại

Đếm câu từng style:
- Feelings phrases: _/total
- Facts phrases: _/total
- Fun phrases: _/total
- Values-based: _/total (target 0)
- Autocratic: _/total (target 0)

Compute % each. Identify imbalance.

### Step 2 — Diagnose imbalance

Common patterns:
- **Fact-heavy** (engineer/tech content): thiếu Feelings + Fun → khô, lose 50% audience
- **Fun-only** (entertainment): thiếu Facts → audience không trust → lose 25%
- **Values-heavy** ("tốt nhất", "phải làm"): alienate 90% → fail
- **Autocratic-heavy** (sales page): chỉ reach 5%

### Step 3 — Rewrite với target blend

Target: Feelings ≥25% + Facts ≥20% + Fun ≥15% → tổng ≥60% minimum. Tốt nhất ≥75%.

**Swap rules**:
- Câu Values-based → câu Fact-based tương đương
  - ❌ "Claude là tool tốt nhất cho developer"
  - ✅ "Theo Anthropic, Claude Opus 4.7 đạt 92% trên SWE-bench"
  
- Câu Autocratic → câu Democratic / Benevolent / Laissez-faire
  - ❌ "Đăng ký ngay kẻo lỡ!"
  - ✅ "Bạn có muốn thử một approach khác không?" (Democratic)
  - ✅ "Mình viết khóa này cho anh em đang stuck ở đây" (Benevolent)
  - ✅ "Yo, cái này work cho mình, check xem sao" (Laissez-faire)

- Thêm Feelings: inject 2-3 câu về emotion
  - "Hôm qua mình mất 4 tiếng debug cái này — cảm giác như đập đầu vào tường"

- Thêm Facts: inject 2-3 stat/number cụ thể
  - "Cụ thể là 87% các bạn trong group stuck ở đúng bước này"

- Thêm Fun: inject 1-2 moment high-energy
  - "Wow, lúc đó mình thấy cái result ra màn hình, đúng kiểu 'đỉnh thật sự'!"

### Step 4 — Output diff table

Show before/after với lý do swap.

## Output Format

```markdown
# Triple F Boost: [Content ID / Title]

## Original Score
- Feelings: X% (Y/Z sentences)
- Facts: X%
- Fun: X%
- Values-based: X% (target 0)
- Autocratic: X% (target 0)

**Diagnosis**: [Ví dụ: "Fact-heavy (45% Facts, 5% Feelings, 3% Fun) → mất 50% audience Feelings-based"]

## Rewrite (full version)

[Full rewritten content]

## Target Score (after rewrite)
- Feelings: X% ✅
- Facts: X% ✅
- Fun: X% ✅
- Values-based: 0% ✅
- Autocratic: 0% ✅
- Total F+F+F: ≥75%

## Diff Table

| # | Before | After | Style swap | Reason |
|---|--------|-------|-----------|--------|
| 1 | "Claude là tool tốt nhất" | "Claude Opus 4.7 đạt 92% SWE-bench (nguồn Anthropic)" | Values → Facts | Avoid alienation |
| 2 | "Đăng ký ngay kẻo lỡ!" | "Bạn muốn thử không?" | Autocratic → Democratic | Inclusive |
| 3 | (add) | "Hôm qua mình debug 4 tiếng — đập đầu vào tường" | Added Feelings | Balance blend |
```

## Mandatory Rules

- [ ] Không thay đổi message core / thesis của bài
- [ ] Giữ brand voice 7/10 energy (không swing sang giọng khác)
- [ ] Giữ power words English: System, Automation, One Person, AI, Framework, Workflow, No-code, Template
- [ ] Giữ nhân xưng "mình/bạn" consistent
- [ ] Target blend F+F+F ≥75% nhưng không cần chính xác 30/25/20 — blend tự nhiên quan trọng hơn
- [ ] Values-based và Autocratic phải về 0%, không compromise

## References

- `references/vocabulary-swap-bank.md` — Bank các câu swap sẵn cho tiếng Việt
