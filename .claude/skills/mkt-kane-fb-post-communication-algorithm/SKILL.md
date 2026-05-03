---
name: mkt-kane-fb-post-communication-algorithm
description: "Viết bài Facebook blend Feelings (30%) + Facts (25%) + Fun (20%) — tổng ≥75% — theo 5 Rules Communication Algorithm của Brendan Kane. Tự score % từng style sau khi viết + self-audit. Reach 85% audience thay vì chỉ 30% bài khô fact-only. USE WHEN user says 'viết fb post 5 rules', 'post feelings facts fun', 'viết fb blend cảm xúc data vui', 'communication algorithm post', 'fb post reach 85%', 'post có đủ 3 style', 'bài fb đa style'."
pillar: Cross-pillar (FB post format)
---

# Facebook Post — Communication Algorithm (5 Rules)

Brendan Kane: 5 Rules giúp reach **85%** dân số:
- Rule 1: Feelings (30%) — emotion, connection, empathy
- Rule 2: Facts (25%) — data, research, specific numbers
- Rule 3: Fun (20%) — playful, energy, unexpected
- Rule 4: KHÔNG Values-based ("tốt nhất", "phải") → loại Opinion 10%
- Rule 5: KHÔNG Autocratic ("Mua ngay!") → loại Action-forced 5%

Bài post target blend ≥25% Feelings + ≥20% Facts + ≥15% Fun = ≥60% minimum, ideal ≥75%.

## Input

1. **Topic** (AI / automation / OPB)
2. **Main message** (1-2 câu thesis)
3. **Data/number** (nếu có)
4. **Personal element** (optional)

## Process

### Step 1 — Draft v1 tự nhiên

Viết bản đầu không control style. Length 400-700 từ.

### Step 2 — Tag từng câu theo style

Highlight mỗi câu = F (Feelings) / Fx (Facts) / Fn (Fun) / V (Values — TRÁNH) / A (Autocratic — TRÁNH) / N (Neutral — không count).

### Step 3 — Count + compute %

Total câu = 100%. Compute:
- F% = (F count / total) × 100
- Fx% = ...
- Fn% = ...
- V% = ...
- A% = ...
- F+Fx+Fn = blend score (target ≥75%)

### Step 4 — Rewrite nếu không đạt

Nếu:
- **V > 0%**: swap sang Facts hoặc Feelings (xem `references/style-swaps.md`)
- **A > 0%**: swap sang Democratic/Benevolent/Laissez-faire
- **F+Fx+Fn < 75%**: thêm câu theo style thiếu
- **1 style >50%**: quá heavy → add câu style khác để balance

### Step 5 — Final audit

Output bài + breakdown % + verdict.

## Output Format

```markdown
# FB Post — Communication Algorithm

**Topic**: [topic]
**Target blend**: ≥75% (F+Fx+Fn)

## Post (final)

[Full post 400-700 words]

## Style Breakdown

| Style | Count | % | Target | Status |
|-------|-------|---|--------|--------|
| Feelings (F) | X | 28% | ≥25% | ✅ |
| Facts (Fx) | X | 23% | ≥20% | ✅ |
| Fun (Fn) | X | 17% | ≥15% | ✅ |
| Neutral (N) | X | 27% | — | ✅ |
| Values (V) | 0 | 0% | 0% | ✅ |
| Autocratic (A) | 0 | 0% | 0% | ✅ |

**F+Fx+Fn blend**: 68% — [Above 60% threshold / below threshold, rewrite needed]

## Audit Checklist
- [ ] V = 0% ✅
- [ ] A = 0% ✅
- [ ] F+Fx+Fn ≥ 60% ✅
- [ ] Brand voice 7/10 ✅
- [ ] Power words EN giữ ✅
- [ ] mình/bạn consistent ✅
- [ ] CTA non-autocratic ✅
- [ ] 400-700 words ✅
```

## Example

### Target: AI agent tiết kiệm thời gian

```
Sáng nay mình ngồi cà phê 2 tiếng. Không làm gì. Chỉ uống cà phê và nhìn ra cửa sổ. (F)

Nghe có vẻ lười. Nhưng đây là ngày 47 liên tiếp mình có 2 tiếng rảnh buổi sáng. (F) (Fx - data)

Lý do: tuần trước mình deploy 1 AI agent handle 80% daily task. (Fx) Report: email filtering, draft reply, schedule post, analytics digest — all automated by 7am. (Fx) Anthropic Customer Report Q4: SME dùng Claude agent average tiết kiệm 14 giờ/tuần. (Fx) Mình đúng median. (N)

Yo cái moment lần đầu thấy agent email reply đúng giọng mình, mình bật cười — như nhìn 1 người em họ copy mình. (Fn)

Có đêm mình còn nghĩ: 20 năm trước ông bà mình làm ruộng 12 tiếng/ngày để nuôi 5 đứa con. Giờ mình ngồi coffee 2 tiếng sáng nhờ AI agent. Progress là vậy. (F)

Không phải AI làm thay bạn. AI tạo thời gian bạn từng nghĩ là không có. Thời gian đó bạn dùng sao là quyết định cá nhân — coffee, family, đọc sách, hay start project tiếp. (N)

Bạn đang dùng AI để tạo thời gian hay tiêu thêm thời gian? (Democratic CTA) Mình mở AI Freedom Builders cho anh em đang build agent thực sự — link bio nếu muốn join chung conversation. (Benevolent)

AI không làm bạn giàu. AI làm bạn có thời gian để quyết định giàu là gì. (F + wisdom)
```

**Breakdown**:
- F: 4 câu (40%) ✅
- Fx: 4 câu (40%) ✅
- Fn: 1 câu (10%) — below target, add thêm
- V: 0 ✅
- A: 0 ✅

**Verdict**: Fun dưới target 15% → thêm 1 câu Fun giữa đoạn.

## Mandatory Rules

- [ ] Tag mỗi câu 1 style rõ ràng
- [ ] V = 0, A = 0 tuyệt đối
- [ ] Tối thiểu 1 câu mỗi Feelings/Facts/Fun (không zero)
- [ ] Nếu topic dry (tech/tool) → inject thêm Feelings qua personal moment + Fun qua playful analogy
- [ ] Nếu topic emotional (mindset) → thêm Facts qua specific number/research
- [ ] Brand voice 7/10 — not hype
- [ ] CTA non-autocratic default

## References

- `references/style-swaps.md` — Bank các swap khi rewrite
