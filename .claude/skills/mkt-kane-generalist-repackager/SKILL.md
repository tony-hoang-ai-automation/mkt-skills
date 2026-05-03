---
name: mkt-kane-generalist-repackager
description: "Áp dụng Generalist Approach: take niche AI topic (Claude Code hooks, MCP server, AI agent) → repackage thành hook có mass appeal (universal-interest framing). Ngược với niche-jargon hook. Reach 10x wider audience mà vẫn giữ nội dung niche. USE WHEN user says 'repackage niche topic', 'generalist approach', 'hook mass appeal', 'làm topic tech thành mass', 'đổi góc nhìn niche sang universal', 'expand audience', 'generalist hook', 'không muốn chỉ expert xem'."
pillar: P1 + P2 + P3 (Ideation — widen reach)
---

# Generalist Repackager

Brendan Kane case study:
- Technical title: "Car Financing Strategies for Millennials"
- Generalist title: "How I Bought a Tesla for $78 per Month" (Graham Stephan, 8.5M views)

Content **giống nhau** nhưng framing khác → 8,500× reach.

Lý do: Algorithm show video từ pool 150K+ post cho feed 15 slot. Content pure niche không compete được với entertainment. Generalist framing bridge niche insight + universal interest → lọt vào feed của cả non-niche user.

## Input

1. **Niche topic** (vd: "Claude Code hooks", "MCP server setup", "AI agent memory")
2. **Core insight** (1-2 câu về điểm chính bạn muốn dạy)
3. **Optional**: target platform (ảnh hưởng length hook)

## Process

### Step 1 — Identify universal interest hooks

Topic AI niche có thể map vào 5 universal interests:
1. **Money** (save, earn, invest)
2. **Time** (save, optimize, freedom)
3. **Status** (recognition, career, skill)
4. **Fear** (miss out, lose job, fall behind)
5. **Curiosity** (secret, hidden, nobody-knows)

Mỗi topic AI có thể framed qua 2-3 universal angle.

VD: "Claude Code hooks"
- Money: "Làm sao Claude Code hooks tiết kiệm $5K/năm setup tool"
- Time: "1 file Claude Code hook = 20 giờ/tuần thời gian rảnh"
- Status: "Senior dev dùng Claude Code hooks — junior không biết cái này"
- Fear: "Nếu không dùng hooks, Claude Code của bạn đang chạy kém 70%"
- Curiosity: "Anthropic giấu feature này khỏi tutorial chính thức"

### Step 2 — Generate 5 repackaged hook options

1 cho mỗi universal angle.

Template pattern:
- **Money**: "Làm sao [action] tiết kiệm $X / kiếm $X"
- **Time**: "1 [thing] = X giờ rảnh"
- **Status**: "Người [persona top] dùng [X] — bạn không biết"
- **Fear**: "Nếu không [action], bạn đang [bad outcome]"
- **Curiosity**: "[Authority] giấu [X] / ít ai nói về [X]"

### Step 3 — Add niche entry point trong body

Hook mass → body đi sâu niche. Quan trọng: viewer xem hook mass vào → body niche mà vẫn kept interest vì hook đã bật expectation.

Body template:
1. Payoff hook (1-2 câu delivery promise của hook)
2. Niche explanation (context + technical detail)
3. Return to universal outcome (tie lại money/time/status)

### Step 4 — Score audience reach

Estimate reach mass vs niche:
- Niche hook: ~1-5% population interested
- Generalist hook: ~20-40% population interested (nếu hit universal well)
- Content sâu niche body → lose non-niche ở middle, nhưng đã bought 3s attention

### Step 5 — Recommend format + next skill

Match format với hook:
- Money/Time → "Is it Worth It?" format → `mkt-kane-reels-is-it-worth-it`
- Status/Fear → Myth-bust → `mkt-kane-reels-untold-stories`
- Curiosity → Teaser-first → `mkt-kane-youtube-jenga-longform`

## Output Format

```markdown
# Generalist Repackage: [Niche Topic]

**Niche Topic**: [original]
**Core Insight**: [1-2 sentences]
**Persona**: [target]

## 5 Repackaged Hook Options

### 💰 Money Angle
"[Hook]"
**Expected reach**: ~25% broader than niche
**Risk**: nếu không deliver financial specific → viewer drop

### ⏰ Time Angle
"[Hook]"
...

### 🏆 Status Angle
"[Hook]"
...

### 😰 Fear Angle
"[Hook]"
**Caveat**: use carefully — không scare cheap

### 🔍 Curiosity Angle
"[Hook]"
...

## Recommended Pick
[1 hook best fit brand voice Hoàng + EOV target]

## Body Bridge (how to transition from mass hook → niche content)
1. Payoff hook: [1-2 câu]
2. Niche explanation: [outline]
3. Universal outcome return: [tie back]

## Recommended next skills
- [skill tương ứng format]
- `mkt-hook-kallaway` để polish hook thêm
- `mkt-kane-gold-comparison-reviewer` để benchmark với Graham Stephan / similar
```

## Mandatory Rules

- [ ] Generate đủ 5 hook cho 5 universal angles (không skip)
- [ ] Hook phải DELIVER trong body — không clickbait bán rẻ
- [ ] Universal number phải specific (vd: "$10,000/năm" không "a lot of money")
- [ ] Brand voice Hoàng: không dùng hype words ("INSANE", "SHOCK", "MUST")
- [ ] Fear angle dùng khi có data backing, không scare cheap
- [ ] Niche content body không dilute — vẫn deep technical

## Case studies cho AI niche

### "MCP Server" repackaged
- Money: "Mỗi MCP server mới = $200/tháng saving API cost"
- Time: "Cái MCP này thay thế 3 tool tôi trả $99/tháng"
- Status: "Claude power user dùng MCP — còn ChatGPT user thì không"
- Fear: "Không dùng MCP = bạn đang dùng Claude ở 30% capability"
- Curiosity: "Feature của Claude mà Anthropic không promote"

### "AI Agent Memory" repackaged
- Money: "AI agent nhớ = không trả tiền prompt lại"
- Time: "Nhớ context = không retype 50 tin nhắn mỗi sáng"
- Status: "Agent có memory là junior. Không memory là intern."
- Fear: "AI agent quên = bạn mất productivity đã đạt được"
- Curiosity: "Cách Anthropic làm memory khác OpenAI — và tại sao quan trọng"

## References

- `references/generalist-examples.md` — Case studies + thêm 20 repackage examples
