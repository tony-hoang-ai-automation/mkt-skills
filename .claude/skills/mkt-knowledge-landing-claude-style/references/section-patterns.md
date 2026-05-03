# Section patterns — HTML snippets ready-to-paste

Copy snippet, paste vào template, fill `{{PLACEHOLDER}}`. Nhớ chèn `<div class="connector"></div>` giữa 2 section.

## Table of contents
1. [Hero](#1-hero)
2. [Stats 3-column](#2-stats-3-column)
3. [Image placeholder + Copy button](#3-image-placeholder--copy-button)
4. [Chart.js bar chart](#4-chartjs-bar-chart)
5. [Comparison 2-column](#5-comparison-2-column)
6. [Step cards (4-col)](#6-step-cards-4-col)
7. [Code block / CTA installation](#7-code-block--cta-installation)
8. [Link cards (3-col outbound)](#8-link-cards-3-col-outbound)
9. [Section badge variants](#9-section-badge-variants)

---

## 1. Hero

```html
<section id="hero" class="relative pt-40 pb-24 sm:pt-48 sm:pb-32 px-6">
  <div class="orbit w-[520px] h-[520px] left-[-120px] top-[80px]"></div>
  <div class="orbit w-[520px] h-[520px] right-[-120px] top-[160px]"></div>

  <div class="max-w-6xl mx-auto text-center">

    <!-- Pills row (3-5 pills, brand + ref + tag) -->
    <div class="flex flex-wrap items-center justify-center gap-2.5 mb-12">
      <span class="pill">
        <span class="w-4 h-4 rounded-md bg-deepseek/20 border border-deepseek/50 flex items-center justify-center">
          <span class="w-1.5 h-1.5 rounded-full bg-deepseek"></span>
        </span>
        <span class="text-deepseek-200">{{BRAND_1}}</span>
      </span>
      <span class="pill">
        <span class="w-4 h-4 rounded-md bg-claude/20 border border-claude/50 flex items-center justify-center">
          <span class="w-1.5 h-1.5 rounded-full bg-claude"></span>
        </span>
        <span class="text-claude-100">{{BRAND_2}}</span>
      </span>
      <span class="pill">
        <i data-lucide="github" class="w-4 h-4 text-white/70"></i>
        <span>{{REPO_OR_REF}}</span>
      </span>
    </div>

    <!-- Big display headline với gradient highlight -->
    <h1 class="display text-white text-[44px] sm:text-7xl md:text-8xl lg:text-[120px]">
      <span class="grad-deepseek">{{KEYWORD_1}}</span><span class="text-white/40">  +  </span><br class="sm:hidden"/>
      <span class="grad-claude">{{KEYWORD_2}}</span>
    </h1>

    <!-- Sub-headline -->
    <p class="mt-10 display text-3xl sm:text-5xl md:text-6xl text-white/95">
      {{SUB_LINE_1}}
      <br/>
      <span class="grad-amber">{{HIGHLIGHT}}</span> {{SUB_LINE_2}}
    </p>

    <!-- Description -->
    <p class="mt-8 max-w-2xl mx-auto text-base sm:text-lg text-white/65 leading-relaxed">
      {{DESCRIPTION_VIETNAMESE}}
    </p>

    <!-- Dual CTA -->
    <div class="mt-10 flex flex-col sm:flex-row items-center justify-center gap-3">
      <a href="#start" class="cursor-pointer inline-flex items-center gap-2 px-6 py-3.5 rounded-full bg-white text-ink-900 font-semibold hover:bg-white/90 transition-colors">
        {{PRIMARY_CTA}}
        <i data-lucide="arrow-right" class="w-4 h-4"></i>
      </a>
      <a href="#secondary" class="cursor-pointer inline-flex items-center gap-2 px-6 py-3.5 rounded-full border border-white/15 hover:border-white/30 transition-colors text-white/90">
        <i data-lucide="bar-chart-3" class="w-4 h-4"></i>
        {{SECONDARY_CTA}}
      </a>
    </div>

    <!-- Meta row (3 micro-checks) -->
    <div class="mt-8 flex items-center justify-center gap-5 text-[13px] text-white/45 font-mono">
      <span class="inline-flex items-center gap-1.5"><i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400"></i> {{META_1}}</span>
      <span class="inline-flex items-center gap-1.5"><i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400"></i> {{META_2}}</span>
      <span class="inline-flex items-center gap-1.5"><i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400"></i> {{META_3}}</span>
    </div>
  </div>
</section>
```

---

## 2. Stats 3-column

Dùng cho "WHAT IS X" — show 3 đặc tính số chính.

```html
<section id="{{ID}}" class="px-6">
  <div class="max-w-6xl mx-auto text-center">

    <span class="badge"><span class="dot bg-deepseek"></span> 0N · {{SECTION_MARKER}}</span>

    <h2 class="mt-8 display text-white text-5xl sm:text-7xl md:text-[88px]">
      What <span class="grad-deepseek">{{SUBJECT}}</span> is
    </h2>

    <p class="mt-8 max-w-2xl mx-auto text-lg text-white/65 leading-relaxed">
      {{SUBJECT_DESCRIPTION_VI}}
    </p>

    <div class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-5">
      <div class="card card-hover p-8 text-left">
        <div class="font-mono text-[11px] tracking-[.18em] text-deepseek-200 mb-6">// {{STAT_1_LABEL}}</div>
        <div class="display text-7xl grad-deepseek">{{STAT_1_VALUE}}</div>
        <div class="mt-4 text-white font-semibold">{{STAT_1_TITLE}}</div>
        <div class="mt-1.5 text-sm text-white/55 font-mono">{{STAT_1_SUB}}</div>
      </div>

      <div class="card card-hover p-8 text-left">
        <div class="font-mono text-[11px] tracking-[.18em] text-emerald-300 mb-6">// {{STAT_2_LABEL}}</div>
        <div class="display text-7xl grad-green">{{STAT_2_VALUE}}</div>
        <div class="mt-4 text-white font-semibold">{{STAT_2_TITLE}}</div>
        <div class="mt-1.5 text-sm text-white/55 font-mono">{{STAT_2_SUB}}</div>
      </div>

      <div class="card card-hover p-8 text-left">
        <div class="font-mono text-[11px] tracking-[.18em] text-amber-300 mb-6">// {{STAT_3_LABEL}}</div>
        <div class="display text-7xl grad-amber">{{STAT_3_VALUE}}</div>
        <div class="mt-4 text-white font-semibold">{{STAT_3_TITLE}}</div>
        <div class="mt-1.5 text-sm text-white/55 font-mono">{{STAT_3_SUB}}</div>
      </div>
    </div>

    <!-- Optional: 3 supporting bullets -->
    <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-x-8 gap-y-4 text-left max-w-5xl mx-auto">
      <div class="flex gap-3">
        <i data-lucide="cpu" class="w-5 h-5 text-deepseek-300 mt-0.5 shrink-0"></i>
        <p class="text-sm text-white/70 leading-relaxed">{{BULLET_1}}</p>
      </div>
      <div class="flex gap-3">
        <i data-lucide="layers" class="w-5 h-5 text-emerald-400 mt-0.5 shrink-0"></i>
        <p class="text-sm text-white/70 leading-relaxed">{{BULLET_2}}</p>
      </div>
      <div class="flex gap-3">
        <i data-lucide="unlock" class="w-5 h-5 text-amber-300 mt-0.5 shrink-0"></i>
        <p class="text-sm text-white/70 leading-relaxed">{{BULLET_3}}</p>
      </div>
    </div>
  </div>
</section>
```

---

## 3. Image slot + auto fallback

**N** = số thứ tự ảnh trong page (1, 2, 3, ...). Filename luôn là `N.png`. Prompt nằm trong `prompts.md` cùng folder, KHÔNG nhúng vào HTML nữa.

Behavior: HTML chứa cả `<img>` lẫn placeholder content. Khi user thêm `N.png` vào folder → `onload` thêm class `.img-loaded` → ẩn placeholder, hiện ảnh. Khi không có file → `onerror` xoá `<img>` → placeholder hiện ra.

```html
<section id="{{ID}}" class="px-6">
  <div class="max-w-6xl mx-auto text-center">

    <span class="badge"><span class="dot bg-claude"></span> 0N · {{SECTION_MARKER}}</span>

    <h2 class="mt-8 display text-white text-5xl sm:text-7xl md:text-[88px] reveal">
      {{HEADLINE_LINE_1}}<br/>
      <span class="grad-claude">{{HIGHLIGHT}}</span> {{HEADLINE_LINE_2}}
    </h2>

    <p class="mt-8 max-w-2xl mx-auto text-lg text-white/65 leading-relaxed reveal">
      {{LEAD_PARAGRAPH_VI}}
    </p>

    <!-- Image slot: <img> auto-detect, fallback to placeholder -->
    <div class="mt-14 ph aspect-[16/9] max-w-5xl mx-auto reveal" id="img-slot-{N}">
      <img src="{N}.png" alt="{{ALT_TEXT_VI}}"
           class="w-full h-full object-cover rounded-[20px]"
           onload="this.parentElement.classList.add('img-loaded')"
           onerror="this.remove()" />
      <span class="ph-tag">▮ {N}.png — chưa có ảnh</span>
      <span class="ph-aspect">16 : 9</span>
      <div class="ph-center">
        <div class="icon-box"><i data-lucide="image" class="w-7 h-7 text-claude"></i></div>
        <div class="font-serif italic text-2xl text-white/80 mb-2">{{IMAGE_TITLE_VI}}</div>
        <div class="font-mono text-xs text-white/40 max-w-md">
          Xem prompt #{N} trong <code>prompts.md</code>
        </div>
      </div>
    </div>

    <!-- Optional: 3 mini stats below -->
    <div class="mt-10 grid grid-cols-1 sm:grid-cols-3 gap-5 max-w-4xl mx-auto text-left">
      <div class="card p-6 reveal">
        <div class="font-mono text-[11px] tracking-[.18em] text-claude-200 mb-3">// {{LBL_A}}</div>
        <div class="display text-4xl text-white">{{VAL_A}}</div>
        <div class="text-sm text-white/55 mt-2">{{SUB_A}}</div>
      </div>
      <div class="card p-6 reveal">
        <div class="font-mono text-[11px] tracking-[.18em] text-deepseek-200 mb-3">// {{LBL_B}}</div>
        <div class="display text-4xl text-white">{{VAL_B}}</div>
        <div class="text-sm text-white/55 mt-2">{{SUB_B}}</div>
      </div>
      <div class="card p-6 reveal">
        <div class="font-mono text-[11px] tracking-[.18em] text-amber-300 mb-3">// {{LBL_C}}</div>
        <div class="display text-4xl grad-amber">{{VAL_C}}</div>
        <div class="text-sm text-white/55 mt-2">{{SUB_C}}</div>
      </div>
    </div>
  </div>
</section>
```

**Aspect ratio**: dùng `aspect-[16/9]` mặc định (vì AI33 chỉ hỗ trợ 16:9 — không có 16:10). Có thể đổi sang `aspect-[4/3]` nếu diagram vuông hơn, hoặc `aspect-[1/1]` cho icon-style.

---

## 4. Chart.js bar chart

Dùng cho "BENCHMARKS / COMPARISON". Container có legend custom + canvas.

```html
<section id="{{ID}}" class="px-6">
  <div class="max-w-6xl mx-auto text-center">
    <span class="badge"><span class="dot bg-emerald-400"></span> 0N · {{SECTION_MARKER}}</span>

    <h2 class="mt-8 display text-white text-5xl sm:text-7xl md:text-[88px]">
      {{HEADLINE}} <span class="grad-green">{{HIGHLIGHT}}</span>?
    </h2>

    <p class="mt-8 max-w-2xl mx-auto text-lg text-white/65 leading-relaxed">
      {{LEAD_VI}}
    </p>

    <div class="mt-14 card p-6 sm:p-10">
      <div class="flex flex-wrap items-center justify-center gap-6 mb-8 text-sm">
        <div class="flex items-center gap-2"><span class="inline-block w-4 h-2.5 rounded-sm bg-deepseek"></span><span class="text-white/85">{{LEGEND_1}}</span></div>
        <div class="flex items-center gap-2"><span class="inline-block w-4 h-2.5 rounded-sm" style="background:#F2A07A"></span><span class="text-white/85">{{LEGEND_2}}</span></div>
        <div class="flex items-center gap-2"><span class="inline-block w-4 h-2.5 rounded-sm bg-claude"></span><span class="text-white/85">{{LEGEND_3}}</span></div>
      </div>
      <div class="relative h-[420px]">
        <canvas id="chartCanvas"></canvas>
      </div>
    </div>

    <div class="mt-10 max-w-3xl mx-auto text-center">
      <p class="text-base text-white/70 leading-relaxed">
        <span class="text-white font-semibold">Caveat:</span> {{CAVEAT_VI}}
      </p>
    </div>
  </div>
</section>
```

JS init (gắn vào `<script>` block ở cuối page):

```js
(function(){
  const ctx = document.getElementById('chartCanvas');
  if (!ctx) return;
  const c1 = '#4D6BFE';   // brand 1
  const c2 = '#F2A07A';   // brand 2 light
  const c3 = '#DA7756';   // brand 3 / Claude
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['{{BENCH_1}}', '{{BENCH_2}}', '{{BENCH_3}}', '{{BENCH_4}}'],
      datasets: [
        { label: '{{LEGEND_1}}', data: [80,92,68,73], backgroundColor: c1, borderRadius: 6, barThickness: 28 },
        { label: '{{LEGEND_2}}', data: [78,0,0,60],   backgroundColor: c2, borderRadius: 6, barThickness: 28 },
        { label: '{{LEGEND_3}}', data: [82,0,59,79],  backgroundColor: c3, borderRadius: 6, barThickness: 28 },
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      animation: { duration: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 800 },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(7,7,10,0.95)',
          borderColor: 'rgba(255,255,255,0.12)', borderWidth: 1,
          titleFont: { family: 'Inter', weight: '600' },
          bodyFont: { family: 'JetBrains Mono', size: 12 },
          padding: 12, displayColors: true, boxWidth: 8, boxHeight: 8, boxPadding: 4,
          callbacks: { label: (c) => ` ${c.dataset.label}: ${c.parsed.y}%` }
        }
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: 'rgba(255,255,255,0.7)', font: { family: 'JetBrains Mono', size: 12 } } },
        y: { beginAtZero: true, max: 100,
             grid: { color: 'rgba(255,255,255,0.06)' },
             ticks: { color: 'rgba(255,255,255,0.45)', font: { family: 'JetBrains Mono', size: 11 }, callback: (v) => v + '%' } }
      }
    }
  });
})();
```

---

## 5. Comparison 2-column

Dùng cho "WHEN TO USE WHICH" — 2 cột song song với chip Yes/Yes (không phải Yes/No — hiếm khi 1 phía là 100% sai).

```html
<section id="{{ID}}" class="px-6">
  <div class="max-w-6xl mx-auto text-center">
    <span class="badge"><span class="dot bg-purple-400"></span> 0N · {{SECTION_MARKER}}</span>

    <h2 class="mt-8 display text-white text-5xl sm:text-7xl md:text-[88px]">
      {{HEADLINE_1}}<br/>
      <span class="grad-purple">{{HIGHLIGHT}}</span>
    </h2>

    <p class="mt-8 max-w-2xl mx-auto text-lg text-white/65 leading-relaxed">{{LEAD_VI}}</p>

    <div class="mt-16 grid grid-cols-1 md:grid-cols-2 gap-5 text-left">
      <!-- Column A -->
      <div class="card p-8">
        <div class="flex items-center gap-3 mb-6">
          <span class="w-10 h-10 rounded-xl bg-deepseek/15 border border-deepseek/40 flex items-center justify-center">
            <i data-lucide="zap" class="w-5 h-5 text-deepseek-300"></i>
          </span>
          <div>
            <div class="font-mono text-[11px] tracking-[.18em] text-deepseek-200">// {{COL_A_LABEL}}</div>
            <div class="text-2xl font-semibold text-white">{{COL_A_TITLE}}</div>
          </div>
        </div>
        <ul class="space-y-3.5">
          <li class="flex gap-3">
            <span class="chip-good shrink-0 px-1.5 py-0.5 rounded-md text-[11px] font-mono mt-0.5">YES</span>
            <span class="text-white/80 text-[15px]"><span class="font-medium text-white">{{ITEM_TITLE}}</span> — {{ITEM_DESC_VI}}</span>
          </li>
          <!-- ... 3-4 items ... -->
        </ul>
      </div>

      <!-- Column B -->
      <div class="card p-8">
        <div class="flex items-center gap-3 mb-6">
          <span class="w-10 h-10 rounded-xl bg-claude/15 border border-claude/40 flex items-center justify-center">
            <i data-lucide="sparkles" class="w-5 h-5 text-claude"></i>
          </span>
          <div>
            <div class="font-mono text-[11px] tracking-[.18em] text-claude-200">// {{COL_B_LABEL}}</div>
            <div class="text-2xl font-semibold text-white">{{COL_B_TITLE}}</div>
          </div>
        </div>
        <ul class="space-y-3.5">
          <li class="flex gap-3">
            <span class="chip-good shrink-0 px-1.5 py-0.5 rounded-md text-[11px] font-mono mt-0.5">YES</span>
            <span class="text-white/80 text-[15px]"><span class="font-medium text-white">{{ITEM_TITLE}}</span> — {{ITEM_DESC_VI}}</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- Combined verdict -->
    <div class="mt-10 card p-7 max-w-3xl mx-auto text-center">
      <div class="flex items-center justify-center gap-3 mb-3 text-white/85">
        <i data-lucide="git-merge" class="w-5 h-5 text-amber-300"></i>
        <span class="font-mono text-[11px] tracking-[.18em] text-amber-300">// THE COMBO</span>
      </div>
      <p class="text-lg text-white/80 leading-relaxed">{{COMBO_VERDICT_VI}}</p>
    </div>
  </div>
</section>
```

---

## 6. Step cards (4-col)

Dùng cho "HOW IT WORKS" — 3-4 step cards, mỗi card có serif italic step number + body + code snippet.

```html
<section id="{{ID}}" class="px-6">
  <div class="max-w-6xl mx-auto text-center">
    <span class="badge"><span class="dot bg-emerald-400"></span> 0N · {{SECTION_MARKER}}</span>

    <h2 class="mt-8 display text-white text-5xl sm:text-7xl md:text-[88px]">
      {{HEADLINE}} <span class="grad-green">{{HIGHLIGHT}}</span>
    </h2>

    <p class="mt-8 max-w-2xl mx-auto text-lg text-white/65 leading-relaxed">{{LEAD_VI}}</p>

    <div class="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 text-left">

      <div class="card card-hover p-7">
        <div class="step-num">01</div>
        <div class="mt-3 text-white font-semibold text-lg">{{STEP_1_TITLE}}</div>
        <p class="mt-2 text-sm text-white/60 leading-relaxed">{{STEP_1_DESC_VI}}</p>
        <div class="mt-5 code p-3.5">
          <span class="c-prompt">$</span> <span class="c-cmd">{{CMD}}</span>
        </div>
      </div>

      <!-- repeat for 02, 03, 04 -->

    </div>

    <p class="mt-10 text-sm text-white/45 font-mono">{{TIP_LINE_VI}}</p>
  </div>
</section>
```

---

## 7. Code block / CTA installation

Dùng cho "GET STARTED" — terminal-style frame với traffic-light dots + Copy all.

```html
<section id="start" class="px-6 pb-24">
  <div class="max-w-5xl mx-auto">

    <div class="text-center">
      <span class="badge"><span class="dot bg-claude"></span> 0N · GET STARTED</span>
      <h2 class="mt-8 display text-white text-5xl sm:text-7xl md:text-[80px]">
        {{HEADLINE_LINE_1}}<br/>
        <span class="grad-claude">{{HIGHLIGHT}}</span>
      </h2>
      <p class="mt-8 max-w-2xl mx-auto text-lg text-white/65 leading-relaxed">{{LEAD_VI}}</p>
    </div>

    <div class="mt-12 card p-2">
      <div class="flex items-center gap-2 px-4 py-3 border-b border-white/10">
        <span class="w-3 h-3 rounded-full bg-red-400/80"></span>
        <span class="w-3 h-3 rounded-full bg-amber-400/80"></span>
        <span class="w-3 h-3 rounded-full bg-emerald-400/80"></span>
        <span class="ml-3 font-mono text-[12px] text-white/45">{{TERMINAL_PATH_LABEL}}</span>
        <button onclick="copyText('cmd', event)" class="cursor-pointer ml-auto inline-flex items-center gap-1.5 text-[11px] text-white/60 hover:text-white border border-white/15 hover:border-white/30 px-2.5 py-1 rounded-full transition-colors">
          <i data-lucide="copy" class="w-3 h-3"></i> Copy all
        </button>
      </div>
      <pre id="cmd" class="code rounded-none border-0 p-6 text-[14px] leading-[1.9] whitespace-pre overflow-x-auto"><span class="c-com"># {{COMMENT_1}}</span>
<span class="c-prompt">$</span> <span class="c-cmd">{{CMD_1}}</span>

<span class="c-com"># {{COMMENT_2}}</span>
<span class="c-prompt">$</span> <span class="c-cmd">{{CMD_2}}</span></pre>
    </div>

  </div>
</section>
```

---

## 8. Link cards (3-col outbound)

Đặt sau code block — 3 card link tới repo / docs / API.

```html
<div class="mt-10 grid grid-cols-1 md:grid-cols-3 gap-4">
  <a target="_blank" rel="noopener" href="{{URL_1}}" class="card card-hover p-6 cursor-pointer flex items-center justify-between">
    <div>
      <div class="font-mono text-[11px] tracking-[.18em] text-white/45 mb-1">// {{LBL_1}}</div>
      <div class="text-white font-semibold">{{TITLE_1}}</div>
      <div class="text-sm text-white/50">{{SUB_1}}</div>
    </div>
    <i data-lucide="github" class="w-6 h-6 text-white/70"></i>
  </a>
  <!-- repeat 2 more cards -->
</div>
```

---

## 9. Section badge variants

Dot color theo brand chính của section đó:

```html
<span class="badge"><span class="dot bg-deepseek"></span>  01 · THE MODEL</span>
<span class="badge"><span class="dot bg-claude"></span>    02 · THE SAVINGS</span>
<span class="badge"><span class="dot bg-emerald-400"></span> 03 · BENCHMARKS</span>
<span class="badge"><span class="dot bg-amber-400"></span>   04 · DUAL TERMINAL</span>
<span class="badge"><span class="dot bg-purple-400"></span>  05 · WHEN TO USE WHICH</span>
```

Marker text **luôn tiếng Anh viết hoa** — đó là signature của design này.
