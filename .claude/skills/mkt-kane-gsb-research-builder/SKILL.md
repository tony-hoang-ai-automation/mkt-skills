---
name: mkt-kane-gsb-research-builder
description: "Build Gold-Silver-Bronze (GSB) comparative research sheet cho 1 creator hoặc 1 Viral Format — so sánh video top (Gold, ~10x baseline) / trung bình (Silver, mode views) / thấp (Bronze, dưới median) để rút hypothesis về performance drivers. USE WHEN user says 'tạo gsb sheet', 'gsb research', 'phân tích gold silver bronze', 'so sánh top video và low video', 'research performance driver', 'phân tích creator theo gsb', 'build gsb sheet', 'nghiên cứu format gsb'."
pillar: P1 (AI Demo & Tutorials) + P3 (AI News & Trends)
---

# GSB Research Builder (Brendan Kane — Hook Point)

Tạo bảng nghiên cứu **Gold-Silver-Bronze** để tìm ra performance drivers đứng sau video viral. Thay vì đoán, bạn sẽ so sánh video top vs video trung bình vs video flop của **cùng 1 creator** hoặc **cùng 1 format** — pattern nổi lên từ so sánh chính là hypothesis để apply cho content của Hoang.

**Ngôn ngữ output**: Tiếng Việt, giọng tự nhiên. Metric table vẫn giữ English column header.

## Khi nào dùng

- Muốn phân tích 1 creator AI/tech để học format (vd: Matt Wolfe, AI Jason, MrBeast)
- Muốn validate 1 format trước khi Hoang áp dụng (vd: "Is it Worth It?" có phù hợp niche AI không)
- Trước khi làm video mới — cần reference Gold để so sánh sau khi viết
- Research cross-industry (vd: format bác sĩ có thể áp cho AI educator)

## Input

User cung cấp 1 trong 3:
1. **Creator URL** (YouTube channel / TikTok / Instagram) — skill tự suggest top/mid/bottom videos
2. **Format name + niche** — vd: "Walking Listicle trong ngách AI tools"
3. **Danh sách 10-30 video URLs** đã tự chọn sẵn

Nếu chưa có videos, yêu cầu user chạy skill `youtube-trend-finder` / `mkt-youtube-topic-researcher` / `youtube-transcript` trước.

## Process

### Step 1 — Xác định baseline view count của creator/format

Trước khi gán nhãn Gold/Silver/Bronze, phải biết baseline. Cách tính:
- **Creator-based**: Tính **mode** (giá trị xuất hiện nhiều nhất) của views trong 30 video gần nhất. Đây là Silver baseline.
- **Format-based**: Tính mode của 20+ video cùng format từ 3-5 creators khác nhau.

Dùng **mode** thay vì mean vì 1-2 video cực viral sẽ skew mean.

### Step 2 — Phân tier Gold / Silver / Bronze

Theo định nghĩa Brendan Kane (chi tiết trong `references/gsb-framework.md`):
- **Gold** = views ≥ 5-10× baseline (breakthrough)
- **Silver** = views gần mode (baseline đa số đạt được)
- **Bronze** = views < median (dưới baseline)

Target lấy tối thiểu **3 Gold + 3 Silver + 3 Bronze** (9 video). Tốt hơn: 5+5+5.

### Step 3 — Fill bảng GSB

Cho mỗi video, ghi đủ các cột (xem `references/gsb-sheet-template.md`):

| Video | Views | Tier | Page | Notes | EOV | Tactics | Hypothesis |
|-------|-------|------|------|-------|-----|---------|------------|

- **Notes**: 1-2 câu mô tả nội dung + câu chuyện
- **EOV** (Effect on Viewer): clarity / curiosity / aha / satisfaction / gut-punch / absurdity reaction / ...
- **Tactics**: visual/audio/storytelling elements quan sát được (teaser at start, asmr, contrast, meme card, jumpcut, music contrast, ...)
- **Hypothesis**: pattern bạn nghi là driver

### Step 4 — Extract Performance Drivers (5 upward + 4 downward)

Theo `references/performance-drivers-rubric.md`:

**5 Upward Drivers** (có mặt ở Gold, thiếu ở Bronze):
1. Cleverness — link 2 concept không liên quan thông minh
2. Absurdity — tình huống bất ngờ/phi lý
3. Perspective Shift — debunk misconception, aha moment
4. Viewer Connection — eye contact, "bạn" (singular), actionable value, educational insight
5. Tension Building — setup + payoff, stacked mini-questions

**4 Downward Drivers** (có mặt ở Bronze, thiếu ở Gold):
1. Over-branding — logo to, color brand cứng nhắc → drop 75% performance
2. Over-production — cinematic polish khi không cần
3. Stock imagery — cảm giác corporate, thiếu authenticity
4. Standardized aesthetic — feed grid đẹp nhưng mỗi post riêng lẻ yếu

Đánh dấu ✅ (present) / ❌ (absent) / ⚠️ (partial) cho từng driver ở từng video.

### Step 5 — Viết Hypothesis section

Sau khi fill bảng, viết 5-10 hypothesis cụ thể:

> **H1**: "Video nào mở đầu bằng câu hỏi counter-intuitive trong 2s đầu → đạt Gold (4/4 Gold có, 0/4 Bronze có). Hypothesis: First-2s counter-intuitive hook là driver chính cho format này."
>
> **H2**: "Tất cả Bronze dùng stock B-roll còn Gold dùng footage iPhone self-shot. Hypothesis: stock footage làm giảm performance trong niche AI tutorial."

### Step 6 — Next-step Ideation prompts

Cuối file, list 3-5 idea cụ thể cho Hoang apply vào content sắp tới, format:

> **Idea cho Reels**: [Hook theo pattern H1] + [Topic AI relevant] + [Tactic từ Gold video X]
>
> **Idea cho YouTube**: [30-Day-Challenge theo format Gold] + [Topic AI relevant]

## Output Format

File Markdown lưu tại `research/gsb/[creator-or-format-slug]/gsb-sheet.md`:

```markdown
# GSB Research: [Creator Name / Format Name]

**Ngày research**: YYYY-MM-DD
**Baseline (Silver mode)**: XXX,XXX views
**Gold threshold**: ≥ Y,YYY,YYY views
**Bronze threshold**: < ZZ,ZZZ views

## Bảng GSB

| Video | Views | Tier | Page | Notes | EOV | Tactics | Upward Drivers (5) | Downward Drivers (4) |
|-------|-------|------|------|-------|-----|---------|--------------------|--------------------|
| [URL] | 2.3M | Gold | @creator | ... | aha | teaser@0s, ASMR | ✅✅⚠️✅✅ | ❌❌❌❌ |

## Hypothesis

- **H1**: ...
- **H2**: ...

## Next-step Ideation

- Idea 1 cho Reels: ...
- Idea 2 cho YouTube: ...
```

## Mandatory Rules

- [ ] Tối thiểu 3 Gold + 3 Silver + 3 Bronze trước khi viết hypothesis (N<9 = chưa đủ data)
- [ ] Mode views, không dùng mean — 1-2 outlier sẽ skew kết quả
- [ ] Mỗi hypothesis phải nêu rõ evidence (X/Y Gold có driver Z)
- [ ] Không ghi hypothesis dựa trên cảm tính ("tôi thấy video này hay") — chỉ ghi khi có pattern count rõ ràng
- [ ] Link tất cả video URL (để tự re-verify khi cần)
- [ ] Khi research creator nước ngoài → note locale differences (vd: humor Mỹ có thể không work với audience VN)

## References

- `references/gsb-framework.md` — Định nghĩa Gold/Silver/Bronze + cách tính baseline
- `references/performance-drivers-rubric.md` — Chi tiết 5 upward + 4 downward drivers với examples
- `references/gsb-sheet-template.md` — Blank sheet template với column descriptions

## Reference skills trong repo

- `youtube-trend-finder` — lấy video list từ channel
- `youtube-transcript` — extract transcript để phân tích deeper
- `mkt-kane-viral-format-identifier` — xác định format trước khi GSB
- `mkt-competitor-video-strategy-analyzer` — phân tích strategy chi tiết hơn
- `mkt-content-knowledge-compiler` — compile hypothesis vào knowledge base lâu dài
