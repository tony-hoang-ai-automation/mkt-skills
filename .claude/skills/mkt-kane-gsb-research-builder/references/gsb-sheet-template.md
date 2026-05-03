# GSB Sheet Template

Copy-paste template cho bảng GSB. Fill từng hàng khi phân tích video.

## Header meta

```markdown
# GSB Research: [Creator Name / Format Name]

**Ngày research**: YYYY-MM-DD
**Scope**: [Creator / Format]
**Niche**: [AI Tutorials / AI News / One Person Business / ...]
**Baseline (Silver mode)**: XXX,XXX views (từ 30 video gần nhất)
**Gold threshold**: ≥ X,XXX,XXX views (5-10× mode)
**Bronze threshold**: < XX,XXX views (dưới median)
**Total videos analyzed**: NN (G: n | S: n | B: n)
```

## Bảng chính

```markdown
| # | Video URL | Views | Tier | Page | Notes | EOV | Tactics | Upward (5) | Downward (4) |
|---|-----------|-------|------|------|-------|-----|---------|------------|--------------|
| 1 | [link] | 2.3M | Gold | @creator | Teaser final experiment ở 0s, sau đó explain process với 5 obstacle, kết thúc reveal record | aha + satisfaction | teaser@0s, jumpcut nhanh, music dynamic, voice energetic | ✅✅⚠️✅✅ | ❌❌❌❌ |
| 2 | [link] | 180K | Silver | @creator | Tutorial chuẩn nhưng không có hook surprise | clarity | voice calm, screen recording chính | ⚠️❌❌✅⚠️ | ⚠️❌❌✅ |
| 3 | [link] | 28K | Bronze | @creator | Intro dài 30s về creator, logo corner từ đầu, stock b-roll | (nothing notable) | logo persistent, stock footage, jargon đầu | ❌❌❌⚠️❌ | ✅⚠️✅✅ |
```

### Ký hiệu Upward Drivers (theo thứ tự)
1. Cleverness
2. Absurdity
3. Perspective Shift
4. Viewer Connection
5. Tension Building

### Ký hiệu Downward Drivers (theo thứ tự)
1. Over-branding
2. Over-production
3. Stock imagery
4. Standardized aesthetic

### Ký hiệu scoring
- ✅ = present rõ ràng
- ⚠️ = partial
- ❌ = absent

## Column descriptions (dán vào cuối file nếu muốn self-documenting)

- **Video URL**: Link full để tự verify sau này
- **Views**: Số views tại thời điểm research (ghi thêm ngày để biết video age)
- **Tier**: Gold / Silver / Bronze — gán theo threshold đã tính ở header
- **Page**: Tên creator/channel để tracking nếu research nhiều creator
- **Notes**: 1-2 câu mô tả narrative + key moments. Không copy title — viết bằng lời của bạn.
- **EOV** (Effect on Viewer): emotion mà viewer cảm nhận. Common: clarity, curiosity, aha, satisfaction, gut-punch, belonging, absurdity-reaction, urgency, validation, inspiration.
- **Tactics**: Tangible elements — teaser, jumpcut, asmr, meme card, captions bold, music contrast, split-screen, meta humor, slow reveal, etc.
- **Upward Drivers (5)**: Score 5-ô ✅/⚠️/❌ cho Cleverness / Absurdity / Perspective / Connection / Tension
- **Downward Drivers (4)**: Score 4-ô cho Over-brand / Over-prod / Stock / Standard

## Hypothesis template (sau khi fill 9+ rows)

```markdown
## Hypothesis

### H1 — [Tên pattern]
**Claim**: [Câu tuyên bố rõ ràng 1 câu]
**Evidence**: X/Y Gold có, W/Z Bronze có
**Confidence**: High / Medium / Low
**Apply to Hoang**: [Cách apply cụ thể cho content P1/P2/P3/P4/P5]

### H2 — ...
```

Ví dụ hypothesis tốt:
> **H1 — Teaser final scene ở 0-3s**
> **Claim**: Video mở đầu với teaser final reveal → drop rate 3s thấp hơn ~40%
> **Evidence**: 5/5 Gold có teaser @0s, 0/4 Bronze có
> **Confidence**: High
> **Apply to Hoang**: Mọi video YouTube dài >5 phút nên có 3-5s teaser cảnh cuối ở intro

## Next-step Ideation template

```markdown
## Next-step Ideation for Hoang

### Idea 1 — [Platform: Reels / YouTube / Facebook]
- **Pillar**: P1 AI Demo / P2 OPB / P3 News / P4 Mindset / P5 Behind-the-scenes
- **Format**: [Format nào từ bảng này]
- **Hook pattern**: [Pattern H1/H2...]
- **Topic AI**: [Topic relevant]
- **Tactics cần copy**: [List]
- **Expected EOV**: [Emotion mục tiêu]

### Idea 2 — ...
```
