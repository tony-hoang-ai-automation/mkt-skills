# Style Swaps for Communication Algorithm

Bank các câu swap khi balance blend Feelings / Facts / Fun trong FB post.

## Inject Feelings (F) — khi < 25%

Short injections (1-2 sentences):
- "Có những đêm mình thấy chơi vơi vì không biết bắt đầu từ đâu."
- "Moment đó mình sốc thực sự — không phải vì nó khó, mà vì mình đã phí 3 năm làm tay."
- "Bình an đôi khi đến từ việc biết mình không cô đơn trong chuyện này."
- "Thương anh em còn đang manual copy-paste từng ngày."
- "Mình nhớ cảm giác lần đầu AI agent chạy 1 phát đúng — tim đập như lần đầu ship app."
- "Cảm giác stuck 6 tháng ở 1 vấn đề là cảm giác mình hiểu."

## Inject Facts (Fx) — khi < 20%

- "Theo Anthropic Q4 2024: [data]"
- "GitHub Copilot Research 2024: dev dùng AI ship 55% faster"
- "Case cụ thể: mình test 12 SME client, trung bình giảm 68% manual work"
- "Gartner dự báo 75% enterprise dùng AI agent 2026"
- "Data 3 tháng của mình: $2,800 → $890 cost/month"
- "Harvard Business Review 2024: [finding]"
- "Trên 500 user survey, 87% stuck ở đúng bước này"

## Inject Fun (Fn) — khi < 15%

- "Yo, cái moment đó đỉnh thật sự."
- "Wow, mình cười ngu 5 phút khi thấy output."
- "Hài ở chỗ: tool này free mà xịn hơn cái $200/tháng."
- "Hơi phèo khi nhận ra: mình làm tay 3 năm cái này, AI xong trong 10 phút."
- "Tui biết nghe kì, nhưng thật sự là vậy."
- "Bất ngờ nhất là lúc client hỏi: 'Anh làm 1 mình thật à?'"
- "Anh em đoán xem mình tốn bao nhiêu để fix — $0. Nhờ Claude debug hộ."
- "Cười té ghế khi thấy AI agent tự reply email đúng giọng mình."

## Fix Values-based (V → 0%)

| ❌ Values | ✅ Replace with |
|-----------|----------------|
| "Tool X là tốt nhất" | Facts: "Tool X đạt 92% benchmark Y" |
| "Cách này đúng nhất" | Facts: "Nghiên cứu Z cho thấy cách này +73% kết quả" |
| "Bạn phải dùng Claude" | Feelings: "Mình cảm thấy Claude work tốt cho mình trong task này" |
| "Đây là best practice" | Facts: "7/10 team Fortune 500 dùng cách này (HBR)" |
| "AI là tương lai" | Facts: "Gartner: 75% enterprise dùng AI vào 2026" |
| "Không dùng AI là sai" | Feelings: "Mình từng resist AI 2 năm. Giờ nhìn lại thấy tiếc thời gian đó." |

## Fix Autocratic (A → 0%)

| ❌ Autocratic | ✅ Replace with |
|--------------|-----------------|
| "Mua ngay!" | Democratic: "Bạn muốn xem deal không?" |
| "Đăng ký liền!" | Benevolent: "Mình dành 5 slot cho anh em đang cần" |
| "Follow ngay!" | Laissez-faire: "Follow nếu hợp, chill nếu không" |
| "Share bài này!" | Democratic: "Bài này giúp được ai trong network bạn? Share nếu có" |
| "Click link bio!" | Laissez-faire: "Link bio — check khi rảnh" |
| "Đừng bỏ lỡ!" | Democratic: "Bạn muốn catch cái này trước deadline?" |

## When Facts are too dry

Chuyển Fx → Fx + Fn:
- ❌ "Anthropic report: SME dùng Claude tiết kiệm 14 giờ/tuần"
- ✅ "Anthropic report: SME dùng Claude tiết kiệm 14 giờ/tuần. Yo — đó là 1 full weekend. Mỗi tuần."

Chuyển Fx → Fx + F:
- ❌ "Cost giảm 68%"
- ✅ "Cost giảm 68%. Cảm giác thở phào khi thấy bill cuối tháng."

## Neutral sentence check

Neutral (N) là câu không carry emotion/data/fun rõ — OK có nhưng không count vào blend. Ví dụ:
- "Đây là cách mình làm."
- "Để giải thích rõ hơn..."
- "Bạn có thể nghĩ điều này..."

Cố gắng convert Neutral → F/Fx/Fn để raise blend %.

## Quality check: đa dạng open/close

Một bài Golden không chỉ blend giữa bài mà cả open và close:
- Hook (câu 1): F hoặc Fx hoặc Fn mạnh (không Neutral)
- Last Dab (câu cuối): F hoặc Fx hoặc wisdom

Không bài nào open bằng "Hôm nay mình muốn nói về..." (Neutral).

## Target blend matrix

| Topic type | Target F | Target Fx | Target Fn |
|-----------|----------|-----------|-----------|
| Tech/tool (dry) | 30% | 35% | 20% |
| Mindset/philosophy | 40% | 20% | 15% |
| Case study | 25% | 40% | 15% |
| BIP / journey | 45% | 15% | 20% |
| Tutorial | 20% | 45% | 15% |

Brand voice Hoàng 7/10 energy — Fun nên 15-20%, không ≥25% (sẽ swing sang entertainment).
