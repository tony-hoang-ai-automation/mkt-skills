---
name: mkt-kane-gold-comparison-reviewer
description: "So sánh side-by-side draft của Hoang (script/post/video) vs 1 Gold reference theo 8 performance drivers. Dùng trước khi post (pre-production review) HOẶC sau khi post underperform (post-mortem). Output scorecard + top 3 priority fixes. USE WHEN user says 'so sánh với gold', 'compare draft với video top', 'gold comparison', 'benchmark content', 'pre post review', 'post mortem video', 'draft đã đủ mạnh chưa', 'compare với reference'."
pillar: Cross-pillar (quality assurance)
---

# Gold Comparison Reviewer

Brendan Kane: "Trước khi post, so sánh video của bạn side-by-side với Gold reference. Nếu có gap → fix trước khi post. Nếu post underperform → dùng lại comparison để debug."

## 8 Performance Drivers được score

1. **First 3 Seconds** — hook mạnh ngay 3s đầu không?
2. **Generalist Approach** — niche + mass appeal balanced?
3. **Viewer Connection** — eye contact, "bạn", actionable?
4. **Tension Building** — setup-payoff, stacked tensions?
5. **Cleverness** — link 2 concept không liên quan?
6. **Absurdity / Novelty** — unexpected element?
7. **EOV (Effect on Viewer)** — emotion mục tiêu rõ?
8. **Call to Action** — non-autocratic, clear?

## Input

- **Draft**: script / post text / video URL của Hoang
- **Gold reference**: URL / transcript / post link của creator top (>1M views cùng format)
- **Optional**: Views của draft (nếu đã post) để compute actual vs expected

## Process

### Step 1 — Decompose Gold reference

Analyze Gold theo 8 drivers → score mỗi driver 1-5 và note evidence/tactic cụ thể:
- First 3s: "Teaser @0:02 + bold statement @0:05"
- Generalist: "Topic niche X framed qua universal Y"
- ...

### Step 2 — Decompose draft

Same 8-driver analysis cho draft của Hoang.

### Step 3 — Compute gap

Cho mỗi driver: `Gap = Gold_score - Your_score`
- Gap ≥2 = critical fix priority
- Gap = 1 = nice-to-have
- Gap ≤0 = bạn bằng hoặc vượt Gold

### Step 4 — Fix suggestions (concrete, not vague)

Mỗi driver có gap ≥1 → viết 1-2 câu rewrite cụ thể hoặc action.

### Step 5 — Top 3 priorities

Rank fix theo:
1. Gap size (2+ > 1)
2. Impact (First 3s & EOV > CTA refinement)
3. Effort (easy wins ưu tiên trước)

## Output Format

```markdown
# Gold Comparison: [Your Draft] vs [Gold Reference]

**Draft**: [Title / URL / ID]
**Gold**: @creator — [Title] ([Views])
**Review mode**: Pre-production / Post-mortem
**Review date**: YYYY-MM-DD

## Scorecard

| # | Driver | Gold | Your | Gap | Priority |
|---|--------|------|------|-----|----------|
| 1 | First 3 Seconds | 5 | 2 | 3 | 🔴 Critical |
| 2 | Generalist Approach | 4 | 4 | 0 | ✅ OK |
| 3 | Viewer Connection | 5 | 3 | 2 | 🟡 High |
| 4 | Tension Building | 5 | 2 | 3 | 🔴 Critical |
| 5 | Cleverness | 3 | 3 | 0 | ✅ OK |
| 6 | Absurdity | 4 | 1 | 3 | 🟡 High |
| 7 | EOV Clarity | 5 | 3 | 2 | 🟡 High |
| 8 | CTA | 4 | 3 | 1 | 🟢 Low |

**Total Gap**: 14 (out of 40)
**Readiness**: 26/40 = 65% → cần fix Critical trước khi post

## Detailed Gap Analysis

### 🔴 1. First 3 Seconds (Gap 3)
- **Gold tactic**: Teaser final reveal + bold counter-intuitive statement
- **Your draft**: "Xin chào, hôm nay mình sẽ nói về..."
- **Fix**: Thay intro bằng "Khóa AI $500 — đáng hay không? Mình đã chi $12K và có câu trả lời."

### 🔴 4. Tension Building (Gap 3)
- **Gold tactic**: 1 main Q + 4 mini-Qs stacked
- **Your draft**: linear explanation, 0 tension
- **Fix**: Reframe sang Jenga: Main Q "AI agent có thay junior dev?" → mini Qs debugging / context / maintenance / trust / cost

...

## Top 3 Priority Fixes (ranked)
1. **Rewrite intro 3s** — chuyển từ chào sang teaser + bold statement (30 min)
2. **Restructure body với Jenga** — add 4 mini-Qs (1h)
3. **Add 1 absurd element** — 1 metaphor / 1 unexpected visual (20 min)

## Verdict
- 🔴 Not ready to post — fix Top 3 trước
- 🟡 Can post but expect 30-50% of Gold performance
- 🟢 Ready — minor polish only
```

## Mandatory Rules

- [ ] Gold reference phải cùng FORMAT với draft (không so Listicle với Untold Stories)
- [ ] Gold reference phải có ≥1M views hoặc ≥10× baseline creator
- [ ] Mỗi gap phải có tactic cụ thể (không "cần tốt hơn" vague)
- [ ] Fix suggestion phải actionable trong <2h (không "reshoot toàn bộ")
- [ ] Nếu total gap ≥10/40 → recommend KHÔNG POST, quay lại ideation
- [ ] Recommend sau comparison: `mkt-kane-triple-f-boost` nếu thiếu Feelings/Facts/Fun, `mkt-kane-anti-pattern-auditor` nếu nghi over-branding

## References

- `references/comparison-rubric.md` — Chi tiết scoring 1-5 cho từng driver + examples
