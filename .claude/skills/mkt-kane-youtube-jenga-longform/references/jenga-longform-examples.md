# Jenga Longform — 3 Ví Dụ Đầy Đủ (AI / Claude Code topic)

3 full example bám sát cấu trúc 8 section Jenga. Dùng tham chiếu khi viết script mới.

---

## Ví dụ 1 — "Tôi thử build AI agent thay thế cả team marketing trong 7 ngày — đây là ngày cuối"

**Pillar**: P1 AI Demo | **Duration**: 17 phút

### Last Dab (viết trước)
"7 ngày trước mình tin AI agent chỉ là hype. Giờ mình không thể làm marketing theo cách cũ nữa."

### Final Reveal Lock
- Cảnh: Dashboard analytics ngày 7 — 42 bài đăng, 3 campaign chạy, 11 lead, CPA giảm 60%
- Cảm xúc viewer: Impressed + tò mò "làm sao?"

### [0-10s] TEASER
Voice-over: "Đây là ngày thứ 7. Con số bạn đang thấy, mình cũng không tin lần đầu."
Visual: 4s clip dashboard analytics (ẩn context).

### [10s-1min] MAIN QUESTION SETUP
"Team marketing của mình 4 người. Mình đặt câu hỏi: liệu AI agent thay được bao nhiêu công việc trong 7 ngày? Stakes là 2 triệu cafe tháng này. Mình không phải dev chuyên."

### [1-4min] ATTEMPT 1 + OBSTACLE
- Setup: build 1 agent duy nhất làm tất cả (content + ads + email).
- Execute: Claude Code spin up agent "do-everything".
- Obstacle: agent confuse context, viết caption FB bằng giọng cold email. Rối ren sau 40 prompt.
- Consequence: 3 ngày đầu zero output usable.

### [4-5min] PIVOT
"Mình học: 1 agent làm mọi thứ = không agent nào. Cần chia nhỏ theo vai trò — giống team thật."

### [5-9min] ATTEMPT 2 + OBSTACLE MỚI
- Setup: 4 sub-agent (content, ads, email, analytics) + 1 orchestrator.
- Execute: Framework sub-agent + MCP server cho Notion / Meta Ads.
- Obstacle escalated: sub-agent ghi đè output nhau — orchestrator không biết ai làm gì.
- Stakes tăng: còn 2 ngày, chưa có 1 campaign chạy.

### [9-13min] BREAKTHROUGH
Research reference: Anthropic "Building effective agents" (Dec 2024) — pattern "orchestrator-workers" với shared state file.
Insight: mỗi sub-agent ghi vào file riêng, orchestrator đọc trước khi giao task. Workflow rõ ràng trong 90 phút.

### [13-17min] FINAL REVEAL PAYOFF
"Đây là dashboard bạn đã thấy ở giây 0." Replay clip + thêm 20s: 42 bài, 3 campaign, 11 lead, CPA $1.8 (giảm từ $4.5).

### [17-20min] TAKEAWAY + CTA
Takeaway: (1) 1 agent làm mọi thứ = fail; (2) Framework orchestrator-workers có sẵn, không tự nghĩ ra; (3) shared state là chìa khóa.
CTA: "Toàn bộ System + Prompt Template mình chia sẻ trong cộng đồng AI Freedom Builders. Nếu bạn muốn thử, link ở description."

### Expert/Research citation
- [x] Research paper: Anthropic "Building effective agents"

### B-roll key assets
- Dashboard screenshot trước/sau
- Terminal recording Claude Code
- Sticky note board "vai trò mỗi agent"
- Cafe cup (metaphor cho stakes)

---

## Ví dụ 2 — "Claude Code có ship được production app trong 4 giờ? Tôi đã test"

**Pillar**: P1 AI Demo | **Duration**: 14 phút

### Last Dab
"4 giờ không đủ để build perfect app. Nhưng đủ để ship app khách trả tiền."

### Final Reveal Lock
- Cảnh: Browser mở app production URL + Stripe dashboard show 1 payment
- Cảm xúc viewer: Shock + "wait, thật á?"

### [0-10s] TEASER
Voice-over: "Đây là giây thứ 3 sau khi mình push deploy. Timer nói 3 giờ 47 phút."
Visual: 3s split screen — app live + timer 03:47:xx.

### [10s-1min] MAIN QUESTION SETUP
"Khách yêu cầu mini-CRM cho spa 5 nhân viên. Báo giá thị trường 15 triệu, 3 tuần. Mình đặt cược: Claude Code ship được trong 4 giờ và khách chịu trả 3 triệu? Không được thì mình miễn phí."

### [1-4min] ATTEMPT 1 + OBSTACLE
- Setup: Next.js + Supabase, 1 prompt duy nhất cho toàn bộ feature.
- Execute: Claude Code scaffold 3 components trong 25 phút.
- Obstacle: auth flow vô hạn redirect, Supabase RLS policy block request.
- Consequence: mất 45 phút debug, còn 2h15 — stakes chặt.

### [4-5min] PIVOT
"Mình nhận ra: không prompt duy nhất ship được app. Cần chia feature thành phase + spec rõ ràng."

### [5-9min] ATTEMPT 2 + OBSTACLE MỚI
- Setup: viết spec.md 1 trang, breakdown 7 task, Claude Code làm từng task.
- Execute: task 1-5 xong trong 90 phút.
- Obstacle escalated: task 6 (gửi SMS notif qua Twilio) — API key khách chưa có, rate limit sandbox block flow.
- Stakes tăng: còn 30 phút, chưa test end-to-end.

### [9-13min] BREAKTHROUGH
Expert interview slot: [anh Minh — CTO startup SaaS VN] — 1 câu hỏi: "Khi API block, ship stub hay delay?"
Insight: ship với SMS stub + flag "coming soon", khách approve. App live 3h47min.

### [13-17min] FINAL REVEAL PAYOFF
Replay split screen + thêm 25s: browser thao tác app real (tạo khách, lên lịch), Stripe dashboard 1 payment 3tr đã nhận.

### [17-20min] TAKEAWAY + CTA
Takeaway: (1) No-code mindset sai — spec.md quan trọng hơn prompt; (2) ship stub + communicate, không chờ perfect; (3) khách mua kết quả, không mua tech stack.
CTA: "Mình share file spec.md Template trong AI Freedom Builders. Link description nếu bạn muốn clone."

### Expert/Research citation
- [x] Expert interview: anh Minh, CTO startup SaaS VN

### B-roll key assets
- Timer overlay
- Terminal + IDE split screen
- Stripe dashboard screenshot
- Anh Minh interview (cutaway)

---

## Ví dụ 3 — "Tôi gọi AI agent thay cho 12 freelancer — và đây là những gì xảy ra"

**Pillar**: P1 AI Demo + P2 One Person Business | **Duration**: 19 phút

### Last Dab
"12 freelancer không biến mất — họ chuyển vai. AI agent không thay thế con người, nó thay thế task."

### Final Reveal Lock
- Cảnh: 2 bảng P&L side-by-side — Q4 2025 (12 freelancer, lãi 23tr) vs Q1 2026 (AI agent + 3 freelancer chuyên sâu, lãi 67tr)
- Cảm xúc viewer: Impressed + reflective

### [0-10s] TEASER
Voice-over: "Đây là P&L quý vừa rồi. Lãi 67 triệu. Trước đó 23. Khác biệt duy nhất: mình thay 9 freelancer bằng AI agent."
Visual: 4s P&L side-by-side (blur numbers).

### [10s-1min] MAIN QUESTION SETUP
"Mình chạy agency content 2 năm. 12 freelancer, lãi mỏng, mình stress quản lý. Câu hỏi: nếu AI agent làm được 80% task freelancer, giữ ai, bỏ ai, và lãi đi đâu?"

### [1-4min] ATTEMPT 1 + OBSTACLE
- Setup: replace freelancer content writer bằng Claude + Template.
- Execute: 1 tuần đầu output tăng 3x.
- Obstacle: client phàn nàn "bài giống nhau, mất giọng brand".
- Consequence: 2 client rời, doanh thu giảm 8tr/tháng.

### [4-5min] PIVOT
"Mình sai ở chỗ replace CON NGƯỜI thay vì replace TASK. Freelancer writer làm 5 việc — mình automate hết 5 việc, mất cả người giữ brand voice."

### [5-9min] ATTEMPT 2 + OBSTACLE MỚI
- Setup: breakdown 12 freelancer thành ~60 task. Gán từng task vào AI agent HOẶC người.
- Execute: AI agent làm research, draft, QA, scheduling. Người làm brand voice, client call, strategy.
- Obstacle escalated: 3 freelancer nghỉ vì thu nhập giảm (task của họ bị AI thay), team morale xuống.
- Stakes tăng: Q1 deadline cho 4 client, team căng.

### [9-13min] BREAKTHROUGH
Research reference: MIT Sloan 2025 survey "AI adoption outcomes" — companies tăng lãi khi re-hire freelancer vào vai trò higher-leverage thay vì cắt.
Insight: mời 3 freelancer quay lại với contract "strategy + brand voice advisor" — trả cao hơn, ít giờ hơn. Win-win.

### [13-17min] FINAL REVEAL PAYOFF
Replay P&L side-by-side + thêm 30s breakdown: Q4 lãi 23tr (12 freelancer), Q1 lãi 67tr (3 advisor + AI agent). Cost giảm 45%, output tăng 2.2x.

### [17-20min] TAKEAWAY + CTA
Takeaway: (1) Replace task, không replace người; (2) AI agent freed up vốn để trả cao hơn cho người giữ lại; (3) One Person Business không nghĩa là solo — nghĩa là leverage.
CTA: "Framework phân loại task mình dùng có trong AI Freedom Builders. Nếu bạn đang cân nhắc AI cho team, ghé qua xem."

### Expert/Research citation
- [x] Research paper: MIT Sloan 2025 "AI adoption outcomes"

### B-roll key assets
- P&L Q4 vs Q1 side-by-side
- Slack/Notion screenshot workflow
- Freelancer zoom call (blur face)
- Task-gán-matrix whiteboard

---

## Điểm chung 3 ví dụ (pattern quan trọng)

1. **Teaser luôn là 3-5s CLIP thực từ final reveal** — không voice-over mô tả, mà show thẳng cảnh cuối.
2. **Obstacle 2 luôn khó hơn obstacle 1** — không flat.
3. **Pivot section là energy low** — cho viewer "thở" trước Attempt 2.
4. **Breakthrough có expert HOẶC paper** — không chỉ self-insight.
5. **Final reveal REPLAY đúng clip teaser** + thêm 15-25s context.
6. **Last Dab xuất hiện cuối** — nhưng viết đầu tiên.
7. **CTA gợi mời** (Benevolent / Laissez-faire), không autocratic.
