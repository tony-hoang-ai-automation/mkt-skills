---
name: mkt-kane-anti-pattern-auditor
description: "Audit bài Facebook / Reels / YouTube để phát hiện 4 downward drivers (over-branding, over-production, stock imagery, standardized aesthetic) + frequency-over-quality. Mỗi anti-pattern bị drop ~75% performance nếu hiện diện. USE WHEN user says 'audit content', 'check anti pattern', 'content có lỗi gì không', 'kiểm tra over branding', 'vì sao video bị chết', 'vì sao post không ai xem', 'content audit', 'kiểm tra chất lượng content'."
pillar: Cross-pillar (quality guardrail)
---

# Anti-Pattern Auditor (Brendan Kane)

Skill này quét content (bài FB / script Reels / video YouTube) tìm 4 downward drivers đã được chứng minh làm **drop 75% performance**. Nếu post/video của bạn underperform — audit đây trước khi nghi ngờ content idea.

## 4 Anti-patterns (downward drivers)

1. **Over-branding** — logo persistent, color cứng nhắc, intro "Xin chào tôi là Brand X"
2. **Over-production** — cinematic quá mức, polish thay thế substance
3. **Stock imagery** — generic B-roll, sunset timelapse, business handshake
4. **Standardized aesthetic** — feed grid đồng nhất, mỗi post không đứng riêng được

Thêm bonus: **Frequency-over-quality** (đăng dày mà quality yếu) khi input là 7-30 ngày post history.

## Input

- Single piece (bài FB / script / video URL)
- HOẶC content calendar / post history 7-30 ngày (để audit frequency)
- Optional: benchmark Gold reference để so sánh

## Process

### Step 1 — Scan from 3-second perspective

Đọc/xem trong 3 giây đầu → note mọi branding element:
- Logo xuất hiện ở đâu, có persistent không?
- Intro có bắt đầu bằng "Tôi là X" / brand name không?
- Color scheme có cứng nhắc theo brand guideline không?

### Step 2 — Check production level

- Production ≈ cinematic ad? → over-production risk
- Lighting studio 3-point? → over-production
- Music bản quyền xịn đồng bộ? → over-production
- Transitions CGI / polish? → over-production
- Voice-over ấm như TV commercial? → over-production

Với FB post text: check có "marketing speak" quá polished không — nếu đọc như email corporate = fail.

### Step 3 — Spot stock imagery

- B-roll generic (sunset, city, people walking)? → ❌
- Business handshake, laptop on desk? → ❌
- Screen recording own workflow? → ✅ (authentic)
- Selfie iPhone quay? → ✅ (authentic)

Exception: stock imagery dùng ironic / self-aware → OK

### Step 4 — Aesthetic standardization check

Nếu input là multiple pieces:
- Tất cả đều cùng font / layout / filter? → ❌
- Feed IG grid như 1 bức tranh? → ❌
- Mỗi post đứng riêng có stand out không khi xuất hiện pool 150K post? → test

### Step 5 — Frequency-over-quality audit (nếu có history)

- Post >3/tuần mà engagement rate <1%? → fail
- Post 1-2/tuần với engagement cao? → good
- Inconsistent pattern? → cần refocus

### Step 6 — Viết report với priority rewrite

Mỗi anti-pattern:
- **Score**: ✅ (clean) / ⚠️ (partial) / ❌ (problem)
- **Evidence**: quote cụ thể từ content (VD: "Logo hiện từ 0:00 đến 1:30 liên tục")
- **Impact estimate**: % performance drop nghi ngờ
- **Fix suggestion**: câu rewrite hoặc action cụ thể

Cuối report: **Top 3 Priority Fixes** (ranked by impact).

## Output Format

```markdown
# Anti-Pattern Audit: [Content Title / ID]

**Audit date**: YYYY-MM-DD
**Content type**: FB post / Reels / YouTube / Calendar
**Platform**: ...
**Content length/duration**: ...

## 1. Over-branding — ❌/⚠️/✅
**Evidence**: [quote / timestamp / screenshot reference]
**Impact**: ~XX% performance drop risk
**Fix**: [specific rewrite]

## 2. Over-production — ❌/⚠️/✅
...

## 3. Stock Imagery — ❌/⚠️/✅
...

## 4. Standardized Aesthetic — ❌/⚠️/✅
...

## 5. Frequency-over-Quality — ❌/⚠️/✅ (optional)
...

## Top 3 Priority Fixes
1. [Highest impact fix với action cụ thể]
2. [Second]
3. [Third]

## Clean-up to keep
[Elements đang OK, không động vào]
```

## Mandatory Rules

- [ ] Mỗi anti-pattern phải có evidence cụ thể (quote hoặc timestamp), không vague
- [ ] Fix suggestion phải actionable (VD: "Xoá logo từ 0:00-0:15, chỉ giữ watermark cuối 0:58-1:00")
- [ ] Không judgment — nói nguyên nhân data-driven, không "quá xấu" chung chung
- [ ] Bonus: nếu audit calendar → suggest schedule optimize (vd: giảm 5→2 post/tuần, spend thời gian cho quality)
- [ ] Khi content clean tất cả anti-pattern mà vẫn flop → recommend chuyển sang `mkt-kane-gold-comparison-reviewer`

## References

- `references/anti-pattern-rubric.md` — Chi tiết 4 drivers với examples Adidas vs Harrison Nevel
