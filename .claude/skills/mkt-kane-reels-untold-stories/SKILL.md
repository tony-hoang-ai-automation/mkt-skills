---
name: mkt-kane-reels-untold-stories
description: "Viết Reels 30-90s theo format Untold Stories của Daniel Wall: behind-the-scenes của chủ đề ai cũng biết → reveal 'Oh wait, what?!' moment. Phù hợp topic AI/tech đang hot nhưng viewer chưa biết deep-cut. USE WHEN user says 'viết reels untold stories', 'behind the scenes reels', 'deep cut story reels', 'reveal ít người biết', 'reels format daniel wall', 'viết reels chủ đề hot có twist', 'oh wait what reels'."
pillar: P3 AI News & Trends (re-angle hot topic) + P1 AI Demo
---

# Reels — Untold Stories Format (Daniel Wall style)

Brendan Kane case study: Daniel Wall (YouTube/TikTok @danielswall) dùng format này gain 1M+ follower, signature video "It's Corn" (21M views), "Netflix-Wednesday?" (11M views).

**Core insight**: Viewer đã biết surface của topic. Video của bạn mở curtain cho deep-cut ít ai biết → "Oh wait, what?!" payoff.

## Structure (6 sections, ~45-75s total)

1. **Hook one-liner** (0-3s) — promise hidden story
2. **Context** (3-10s) — confirm cái ai cũng biết
3. **Deep-cut reveal** (10-30s) — thông tin ít người biết
4. **Layered micro-tensions** (30-50s) — 2-3 micro-reveal stacked
5. **Insider-feel payoff** (50-65s) — "now you're in the know"
6. **Soft CTA** (65-75s) — non-autocratic

## Input

1. **Topic/object/person ai cũng biết** (vd: "Claude", "ChatGPT", "MrBeast", "AI viral tool trên GitHub")
2. **Deep-cut research** (optional — skill sẽ prompt)
3. **Duration** (default 60s)

## Process

### Step 1 — Research deep-cuts

Hỏi 3 câu về topic:
1. Origin/history ít ai biết (backstory)
2. Creator/team behind (con người thật)
3. Connection unexpected (cross-industry link, viral moment khác)

Nếu chưa có data — recommend skill `mkt-xcom-viral-knowledge-finder` hoặc `mkt-kane-gsb-research-builder` trước.

### Step 2 — Hook promising story

Hook pattern (chọn 1):
- "Có thể bạn chưa biết: [X]..."
- "Tôi tình cờ khám phá [X]. Đây là cách..."
- "Ai cũng biết [X]. Nhưng đằng sau là..."
- "[X] có 1 câu chuyện chưa ai kể."
- "Bạn nghĩ bạn biết [X]? Đây là 3 điều ẩn..."

Viết 3 hook variations cho user chọn.

### Step 3 — Context (3-10s)

Confirm cái phổ biến — tạo base để build deeper. Viewer nghĩ "OK mình biết cái này".

VD Claude: "Claude là AI chatbot của Anthropic. Bạn dùng rồi. Ai cũng nghe rồi."

### Step 4 — Deep-cut reveal (10-30s)

Dump thông tin ít biết. Viewer phản ứng "ủa thật á?". Ít nhất 1 data point specific + 1 context shift.

VD Claude:
> "Nhưng Anthropic không build Claude để làm chatbot. Dario Amodei founder rời OpenAI vì nghĩ alignment research quan trọng hơn — và Claude là testing ground cho alignment technique họ sợ OpenAI không làm đủ nhanh."

### Step 5 — Layered micro-tensions (30-50s)

2-3 mini-reveals stack lên. Mỗi reveal mở câu hỏi mới.

VD Claude:
> "Và đây mới lạ: Claude được train với Constitutional AI — không phải RLHF thuần. Anthropic viết 'constitution' rules AI tự judge chính mình. Open nguyên paper cho cộng đồng. Nhưng constitution ấy chứa — you guessed — principles từ UN Declaration of Human Rights và Apple Terms of Service."

### Step 6 — Insider-feel payoff (50-65s)

Giúp viewer cảm thấy "now I know something others don't". Close loop hook.

VD: "Next time bạn chat Claude, bạn đang chat với AI được dạy theo 30 điều khoản của Apple. Bây giờ bạn biết."

### Step 7 — Soft CTA (65-75s)

Benevolent hoặc Laissez-faire (KHÔNG autocratic):
- "Follow mình cho thêm deep-cut AI như vầy."
- "AI Freedom Builders có thread về constitution — link bio."

### Step 8 — Visual + audio direction

Cho mỗi section, note:
- Camera: talking head / screen recording / b-roll
- Caption style: bold stroke với highlight word key
- Music: silent khi drop info / rising khi transition micro-tension
- Pacing: medium cut, không jumpy

## Output Format

```markdown
# Reels Script — Untold Stories: [Topic]

**Duration**: ~60s
**Format**: Untold Stories (Daniel Wall style)
**Pillar**: P3 AI News & Trends

## 3 Hook Variations
1. "[Hook A — discovery angle]"
2. "[Hook B — promise hidden]"
3. "[Hook C — challenge assumption]"

**Recommended**: Hook [N] — reason

## Full Script

### [0-3s] HOOK
"[Hook chọn]"
📹 Visual: [note]
🎵 Audio: [note]

### [3-10s] CONTEXT
"[Confirm common knowledge]"
📹 Visual: [note]

### [10-30s] DEEP-CUT REVEAL
"[Hidden info with 1 data point + context shift]"
📹 Visual: [note]
🎵 Audio: silent / drop

### [30-50s] LAYERED MICRO-TENSIONS
"[Reveal 1]"
"[Reveal 2]"
"[Reveal 3]"
📹 Visual: [note]

### [50-65s] INSIDER-FEEL PAYOFF
"[Close loop]"
📹 Visual: [direct camera]

### [65-75s] SOFT CTA
"[Benevolent or Laissez-faire]"
📹 Visual: [note]

## Last Dab (memorable closer)
"[1-liner stick]"

## Next Skills
- `mkt-hook-kallaway` — polish hook nếu cần
- `mkt-video-script-to-mp3` → `mkt-full-ai-video` — produce video
- `mkt-kane-gold-comparison-reviewer` — benchmark với Daniel Wall video
```

## Mandatory Rules

- [ ] Duration 30-90s (default 60s)
- [ ] Hook ≤3s, promising story
- [ ] Deep-cut phải có data specific + surprise element
- [ ] Mỗi micro-tension mở câu hỏi mới (không flat info dump)
- [ ] Payoff close loop back to hook
- [ ] CTA non-autocratic
- [ ] Brand voice 7/10 — không sensational
- [ ] Power words English giữ
- [ ] Nhân xưng "mình/bạn"

## References

- `references/untold-stories-examples.md` — 3 ví dụ đầy đủ cho topic AI
