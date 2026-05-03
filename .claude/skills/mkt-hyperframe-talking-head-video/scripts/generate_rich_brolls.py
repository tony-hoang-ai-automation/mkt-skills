#!/usr/bin/env python3
"""Generate 8 rich animated b-roll sub-comps for the 6-AI-business video.

Each sub-comp is content-specific with multiple animated elements
(icons, count-ups, comparison cards, brand pills, etc.)
"""
import sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else 'compositions')
OUT.mkdir(exist_ok=True)

# Shared CSS tokens
CSS_TOKENS = """
:root {
  --bg-dark: #141413;
  --bg-cream: #faf9f5;
  --surface: #1f1f1d;
  --border: #2a2a27;
  --accent: #d97757;
  --accent-soft: rgba(217, 119, 87, 0.18);
  --accent-glow: rgba(217, 119, 87, 0.45);
  --blue: #6a9bcc;
  --green: #788c5d;
  --ink: #faf9f5;
  --ink-mute: #b0aea5;
}
"""

GSAP_SRC = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'

def write_subcomp(filename, comp_id, body_html, css_extra, timeline_js):
    """Write a sub-composition file."""
    html = f'''<template id="{comp_id}-template">
  <div data-composition-id="{comp_id}" data-start="0" data-width="1080" data-height="1920">
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800;900&display=swap"
      rel="stylesheet"
    />

    <style>
      {CSS_TOKENS}
      [data-composition-id="{comp_id}"] {{
        width: 100%; height: 100%;
        background: linear-gradient(160deg, #1a1a18 0%, #141413 50%, #0f0f0e 100%);
        color: var(--ink);
        position: relative;
        overflow: hidden;
        font-family: 'Be Vietnam Pro', 'Inter', Arial, sans-serif;
      }}
      [data-composition-id="{comp_id}"] .scene-bg-mesh {{
        position: absolute; inset: 0; z-index: 0;
        background:
          radial-gradient(ellipse 600px 400px at 20% 30%, var(--accent-soft) 0%, transparent 60%),
          radial-gradient(ellipse 500px 600px at 85% 75%, rgba(106,155,204,0.08) 0%, transparent 65%);
        opacity: 0.85; pointer-events: none;
      }}
      [data-composition-id="{comp_id}"] .scene-grid {{
        position: absolute; inset: 0; z-index: 0;
        background-image:
          linear-gradient(rgba(217,119,87,0.05) 1px, transparent 1px),
          linear-gradient(90deg, rgba(217,119,87,0.05) 1px, transparent 1px);
        background-size: 80px 80px; opacity: 0.6; pointer-events: none;
      }}
      [data-composition-id="{comp_id}"] .scene-content {{
        position: relative; z-index: 2;
        width: 100%; height: 100%;
        padding: 220px 80px 360px;
        box-sizing: border-box;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        text-align: center;
      }}
      [data-composition-id="{comp_id}"] .kicker {{
        display: inline-flex; align-items: center; gap: 10px;
        padding: 10px 20px;
        background: var(--accent-soft);
        border: 1.5px solid var(--accent);
        border-radius: 999px;
        font-weight: 700; font-size: 22px;
        letter-spacing: 0.2em; text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 24px;
        will-change: transform, opacity;
      }}
      [data-composition-id="{comp_id}"] .kicker .dot {{
        width: 10px; height: 10px; border-radius: 50%;
        background: var(--accent);
        box-shadow: 0 0 12px var(--accent-glow);
      }}
      [data-composition-id="{comp_id}"] .big-num {{
        font-weight: 900; font-size: 200px; line-height: 0.85;
        letter-spacing: -0.06em;
        background: linear-gradient(135deg, var(--accent) 0%, #f4a384 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        margin-bottom: 8px;
        font-variant-numeric: tabular-nums;
        will-change: transform, opacity;
      }}
      [data-composition-id="{comp_id}"] .title-line {{
        font-weight: 800; font-size: 92px; line-height: 1.05;
        letter-spacing: -0.025em;
        margin: 0 0 18px;
      }}
      [data-composition-id="{comp_id}"] .title-line .word {{
        display: inline-block; will-change: transform, opacity;
      }}
      [data-composition-id="{comp_id}"] .title-line .accent {{ color: var(--accent); }}
      {css_extra}
    </style>

    <div class="scene-bg-mesh"></div>
    <div class="scene-grid"></div>
    <div class="scene-content">
      {body_html}
    </div>

    {GSAP_SRC}
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const ROOT = '[data-composition-id="{comp_id}"]';

      // BG mesh slow drift
      tl.fromTo(ROOT + ' .scene-bg-mesh',
        {{ scale: 1.0, opacity: 0.0 }},
        {{ scale: 1.08, opacity: 0.85, duration: 1.6, ease: "sine.out" }},
        0
      );
      // Grid fade in
      tl.from(ROOT + ' .scene-grid', {{
        opacity: 0, duration: 0.8, ease: "power2.out",
      }}, 0.1);

      // Kicker pop in
      tl.from(ROOT + ' .kicker', {{
        y: -20, opacity: 0, scale: 0.85, duration: 0.5, ease: "back.out(1.8)",
      }}, 0.15);

      // Big num zoom in
      tl.from(ROOT + ' .big-num', {{
        scale: 0.4, opacity: 0, duration: 0.6, ease: "back.out(2)",
      }}, 0.35);

      // Title words slam in (word-by-word)
      tl.from(ROOT + ' .title-line .word', {{
        y: 50, opacity: 0, scale: 0.85, duration: 0.45,
        ease: "back.out(1.5)", stagger: 0.06,
      }}, 0.6);

      {timeline_js}

      window.__timelines["{comp_id}"] = tl;
    </script>
  </div>
</template>
'''
    (OUT / filename).write_text(html)
    print(f'  → {filename}')


# ============================================================
# IDEA 1 — Tư vấn AI cho 1 ngành (12.71 → 26.4s)
# ============================================================
write_subcomp(
    'fs-lesson-1.html', 'fs-lesson-1',
    body_html='''
      <div class="kicker"><div class="dot"></div>Mô hình #1 · Tư vấn AI</div>
      <div class="big-num">01</div>
      <h1 class="title-line">
        <span class="word">Tư</span>
        <span class="word">vấn</span>
        <span class="word accent">AI</span>
        <span class="word">cho</span>
        <span class="word">1</span>
        <span class="word">ngành</span>
      </h1>

      <div class="industry-pills">
        <div class="pill"><span class="ico">📊</span>Marketing</div>
        <div class="pill"><span class="ico">💼</span>Kế toán</div>
        <div class="pill"><span class="ico">👥</span>Nhân sự</div>
      </div>

      <div class="cadence-row">
        <div class="cadence-icon">📅</div>
        <div class="cadence-text">Đăng case study lên Facebook · <strong><span id="day-counter">1</span> ngày</strong></div>
      </div>
    ''',
    css_extra='''
      [data-composition-id="fs-lesson-1"] .industry-pills {
        display: flex; gap: 18px; margin: 24px 0;
        flex-wrap: wrap; justify-content: center;
      }
      [data-composition-id="fs-lesson-1"] .pill {
        display: inline-flex; align-items: center; gap: 12px;
        padding: 18px 28px; border-radius: 999px;
        background: var(--surface); border: 2px solid var(--border);
        font-weight: 700; font-size: 30px; color: var(--ink);
        will-change: transform, opacity;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
      }
      [data-composition-id="fs-lesson-1"] .pill .ico { font-size: 36px; }
      [data-composition-id="fs-lesson-1"] .cadence-row {
        margin-top: 32px;
        display: inline-flex; align-items: center; gap: 18px;
        padding: 22px 32px;
        background: var(--accent); border-radius: 22px;
        font-weight: 700; font-size: 30px; color: var(--bg-cream);
        box-shadow: 0 12px 32px var(--accent-glow);
      }
      [data-composition-id="fs-lesson-1"] .cadence-row strong {
        font-weight: 900; font-size: 38px;
      }
      [data-composition-id="fs-lesson-1"] .cadence-icon { font-size: 48px; }
    ''',
    timeline_js='''
      // Industry pills bounce in (staggered)
      tl.from(ROOT + ' .pill', {
        y: 40, scale: 0.4, opacity: 0,
        duration: 0.55, ease: "back.out(2.2)", stagger: 0.18,
      }, 1.0);
      // Pills wiggle loop
      tl.to(ROOT + ' .pill', {
        rotation: 2, duration: 0.6, ease: "sine.inOut",
        yoyo: true, repeat: 4, stagger: { each: 0.1, yoyo: true },
        transformOrigin: "50% 50%",
      }, 2.2);

      // Cadence row slide in
      tl.from(ROOT + ' .cadence-row', {
        y: 30, opacity: 0, scale: 0.92,
        duration: 0.5, ease: "back.out(1.6)",
      }, 1.8);

      // Day counter 1 → 30 ticking
      const dayObj = { v: 1 };
      tl.to(dayObj, {
        v: 30, duration: 4.5, ease: "power2.out",
        onUpdate: () => {
          const el = document.querySelector(ROOT + ' #day-counter');
          if (el) el.textContent = Math.round(dayObj.v);
        }
      }, 2.2);
    '''
)

# ============================================================
# IDEA 2 — GEO / Tối ưu xuất hiện trên ChatGPT, Gemini (26.6 → 39.3s)
# ============================================================
write_subcomp(
    'fs-lesson-2.html', 'fs-lesson-2',
    body_html='''
      <div class="kicker"><div class="dot"></div>Mô hình #2 · GEO</div>
      <div class="big-num">02</div>
      <h1 class="title-line">
        <span class="word">Xuất</span>
        <span class="word">hiện</span>
        <span class="word">trên</span>
        <span class="word accent">AI search</span>
      </h1>

      <div class="search-mockup">
        <div class="search-bar">
          <span class="search-ico">🔍</span>
          <span class="search-text" id="search-typing"></span><span class="caret">|</span>
        </div>
      </div>

      <div class="ai-logos">
        <div class="logo-cell" data-name="ChatGPT">💬<div class="logo-name">ChatGPT</div></div>
        <div class="logo-cell" data-name="Gemini">✨<div class="logo-name">Gemini</div></div>
        <div class="logo-cell" data-name="Perplexity">🌀<div class="logo-name">Perplexity</div></div>
        <div class="logo-cell" data-name="Grok">⚡<div class="logo-name">Grok</div></div>
      </div>

      <div class="source-row">
        <div class="source-pill">PR</div>
        <div class="source-pill">LinkedIn</div>
        <div class="source-pill">Reddit</div>
        <div class="source-pill">YouTube</div>
      </div>
    ''',
    css_extra='''
      [data-composition-id="fs-lesson-2"] .search-mockup {
        width: 100%; max-width: 880px; margin: 18px 0;
        will-change: transform, opacity;
      }
      [data-composition-id="fs-lesson-2"] .search-bar {
        display: flex; align-items: center; gap: 16px;
        padding: 22px 28px;
        background: var(--bg-cream); color: var(--bg-dark);
        border-radius: 18px; box-shadow: 0 12px 32px rgba(0,0,0,0.4);
        font-size: 30px; font-weight: 600; letter-spacing: -0.01em;
        text-align: left;
      }
      [data-composition-id="fs-lesson-2"] .search-ico { font-size: 36px; }
      [data-composition-id="fs-lesson-2"] .search-text { color: var(--bg-dark); }
      [data-composition-id="fs-lesson-2"] .caret {
        color: var(--accent); font-weight: 800;
        animation: caret-blink 0.6s steps(1) infinite;
      }
      @keyframes caret-blink { 50% { opacity: 0; } }
      [data-composition-id="fs-lesson-2"] .ai-logos {
        display: flex; gap: 16px; margin: 22px 0; flex-wrap: wrap; justify-content: center;
      }
      [data-composition-id="fs-lesson-2"] .logo-cell {
        display: flex; flex-direction: column; align-items: center;
        padding: 18px 22px; min-width: 140px;
        background: var(--surface); border: 2px solid var(--border);
        border-radius: 18px; font-size: 56px; line-height: 1;
        will-change: transform, opacity;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
      }
      [data-composition-id="fs-lesson-2"] .logo-name {
        font-size: 22px; font-weight: 700; color: var(--ink); margin-top: 8px;
      }
      [data-composition-id="fs-lesson-2"] .source-row {
        display: flex; gap: 14px; margin-top: 18px; flex-wrap: wrap; justify-content: center;
      }
      [data-composition-id="fs-lesson-2"] .source-pill {
        padding: 14px 26px;
        background: var(--accent); color: var(--bg-cream);
        font-weight: 700; font-size: 26px; border-radius: 999px;
        box-shadow: 0 6px 18px var(--accent-glow);
        will-change: transform, opacity;
      }
    ''',
    timeline_js='''
      // Search bar slide down
      tl.from(ROOT + ' .search-mockup', {
        y: -30, opacity: 0, duration: 0.5, ease: "back.out(1.5)",
      }, 1.0);

      // Type "phòng khám tốt nhất TP.HCM" char by char
      const SEARCH_QUERY = "phòng khám tốt nhất TP.HCM";
      let typeProg = { i: 0 };
      tl.to(typeProg, {
        i: SEARCH_QUERY.length, duration: 1.6, ease: "none",
        onUpdate: () => {
          const el = document.querySelector(ROOT + ' #search-typing');
          if (el) el.textContent = SEARCH_QUERY.substring(0, Math.floor(typeProg.i));
        }
      }, 1.3);

      // AI logos pop in (staggered grid)
      tl.from(ROOT + ' .logo-cell', {
        y: 50, scale: 0.3, opacity: 0,
        duration: 0.5, ease: "back.out(2.4)", stagger: 0.12,
      }, 3.2);

      // Logos pulse loop
      tl.to(ROOT + ' .logo-cell', {
        scale: 1.05, duration: 0.5, ease: "sine.inOut",
        yoyo: true, repeat: 5, stagger: { each: 0.08, yoyo: true },
      }, 4.0);

      // Source pills cascade in
      tl.from(ROOT + ' .source-pill', {
        x: -60, opacity: 0, duration: 0.4, ease: "power3.out", stagger: 0.1,
      }, 4.5);
    '''
)

# ============================================================
# IDEA 3 — Voice AI Receptionist (39.6 → 51.7s)
# ============================================================
write_subcomp(
    'fs-lesson-3.html', 'fs-lesson-3',
    body_html='''
      <div class="kicker"><div class="dot"></div>Mô hình #3 · Voice AI</div>
      <div class="big-num">03</div>
      <h1 class="title-line">
        <span class="word">Lễ</span>
        <span class="word">tân</span>
        <span class="word accent">AI</span>
        <span class="word">giọng</span>
        <span class="word">nói</span>
      </h1>

      <div class="phone-stage">
        <div class="ring ring-1"></div>
        <div class="ring ring-2"></div>
        <div class="ring ring-3"></div>
        <div class="phone-icon">📞</div>
      </div>

      <div class="vendor-pill">
        <span class="vendor-dot"></span>Eleven Labs · Voice Agent
      </div>

      <div class="industry-row">
        <div class="ind-cell"><span class="ind-ico">🦷</span>Nha khoa</div>
        <div class="ind-cell"><span class="ind-ico">💆</span>Spa</div>
        <div class="ind-cell"><span class="ind-ico">🩺</span>Bác sĩ</div>
      </div>

      <div class="price-card">
        <div class="price-from">Mỗi khách</div>
        <div class="price-num">2 triệu</div>
        <div class="price-from">/ tháng</div>
      </div>
    ''',
    css_extra='''
      [data-composition-id="fs-lesson-3"] .phone-stage {
        position: relative; width: 200px; height: 200px;
        margin: 12px auto 16px;
        display: flex; align-items: center; justify-content: center;
      }
      [data-composition-id="fs-lesson-3"] .phone-icon {
        font-size: 110px; line-height: 1; z-index: 5; position: relative;
        will-change: transform;
        filter: drop-shadow(0 8px 20px var(--accent-glow));
      }
      [data-composition-id="fs-lesson-3"] .ring {
        position: absolute; top: 50%; left: 50%;
        border-radius: 50%; border: 3px solid var(--accent);
        opacity: 0; will-change: transform, opacity;
      }
      [data-composition-id="fs-lesson-3"] .ring-1 {
        width: 200px; height: 200px; margin: -100px 0 0 -100px;
      }
      [data-composition-id="fs-lesson-3"] .ring-2 {
        width: 280px; height: 280px; margin: -140px 0 0 -140px;
      }
      [data-composition-id="fs-lesson-3"] .ring-3 {
        width: 360px; height: 360px; margin: -180px 0 0 -180px;
      }
      [data-composition-id="fs-lesson-3"] .vendor-pill {
        display: inline-flex; align-items: center; gap: 10px;
        padding: 12px 22px;
        background: var(--surface); border: 2px solid var(--accent);
        border-radius: 999px;
        font-weight: 700; font-size: 24px; color: var(--ink);
        margin-bottom: 18px;
        will-change: transform, opacity;
      }
      [data-composition-id="fs-lesson-3"] .vendor-dot {
        width: 12px; height: 12px; border-radius: 50%;
        background: var(--accent);
        box-shadow: 0 0 10px var(--accent-glow);
      }
      [data-composition-id="fs-lesson-3"] .industry-row {
        display: flex; gap: 14px; margin-bottom: 22px; flex-wrap: wrap; justify-content: center;
      }
      [data-composition-id="fs-lesson-3"] .ind-cell {
        display: inline-flex; align-items: center; gap: 10px;
        padding: 14px 22px;
        background: var(--surface); border-radius: 16px;
        font-weight: 700; font-size: 26px; color: var(--ink);
        will-change: transform, opacity;
      }
      [data-composition-id="fs-lesson-3"] .ind-ico { font-size: 36px; }
      [data-composition-id="fs-lesson-3"] .price-card {
        display: inline-flex; align-items: baseline; gap: 14px;
        padding: 24px 38px;
        background: linear-gradient(135deg, var(--accent) 0%, #f4a384 100%);
        color: var(--bg-cream); border-radius: 24px;
        font-weight: 800;
        box-shadow: 0 16px 40px var(--accent-glow);
        will-change: transform, opacity;
      }
      [data-composition-id="fs-lesson-3"] .price-from {
        font-size: 28px; font-weight: 600; opacity: 0.92;
      }
      [data-composition-id="fs-lesson-3"] .price-num {
        font-size: 88px; line-height: 0.9; letter-spacing: -0.04em;
        font-weight: 900;
      }
    ''',
    timeline_js='''
      // Phone shake/ring
      tl.from(ROOT + ' .phone-icon', {
        scale: 0, rotation: -45, opacity: 0,
        duration: 0.55, ease: "back.out(2.2)",
      }, 1.0);
      tl.to(ROOT + ' .phone-icon', {
        rotation: 12, duration: 0.12, ease: "power2.inOut",
        yoyo: true, repeat: 7, transformOrigin: "50% 80%",
      }, 1.55);

      // Pulse rings expanding outward
      tl.fromTo(ROOT + ' .ring',
        { scale: 0.3, opacity: 0.8 },
        { scale: 1.4, opacity: 0, duration: 1.6, ease: "power2.out", stagger: 0.5, repeat: 2 },
        1.4
      );

      // Vendor pill slide in
      tl.from(ROOT + ' .vendor-pill', {
        y: 20, opacity: 0, duration: 0.45, ease: "power3.out",
      }, 2.0);

      // Industry cells stagger in
      tl.from(ROOT + ' .ind-cell', {
        x: -40, opacity: 0, scale: 0.8,
        duration: 0.4, ease: "back.out(1.6)", stagger: 0.12,
      }, 2.4);

      // Price card big punch
      tl.from(ROOT + ' .price-card', {
        scale: 0.5, opacity: 0, rotation: -5,
        duration: 0.6, ease: "back.out(2)",
      }, 3.2);
      tl.to(ROOT + ' .price-card', {
        scale: 1.04, duration: 0.5, ease: "sine.inOut",
        yoyo: true, repeat: 4,
      }, 3.9);
    '''
)

# ============================================================
# IDEA 4 — AI Native Ad Agency (51.9 → 63.95s)
# ============================================================
write_subcomp(
    'fs-lesson-4.html', 'fs-lesson-4',
    body_html='''
      <div class="kicker"><div class="dot"></div>Mô hình #4 · Ad Agency AI</div>
      <div class="big-num">04</div>
      <h1 class="title-line">
        <span class="word">Quảng</span>
        <span class="word">cáo</span>
        <span class="word accent">100×</span>
        <span class="word">tốc</span>
        <span class="word">độ</span>
      </h1>

      <div class="ad-grid">
        <div class="ad-cell">💪</div>
        <div class="ad-cell">🏠</div>
        <div class="ad-cell">💆</div>
        <div class="ad-cell">🚗</div>
        <div class="ad-cell">🍕</div>
        <div class="ad-cell">👗</div>
        <div class="ad-cell">📱</div>
        <div class="ad-cell">💎</div>
      </div>

      <div class="vs-row">
        <div class="vs-cell vs-old">
          <div class="vs-label">Agency cũ</div>
          <div class="vs-num">5</div>
          <div class="vs-unit">ads / tháng</div>
        </div>
        <div class="vs-divider">vs</div>
        <div class="vs-cell vs-new">
          <div class="vs-label">AI Native</div>
          <div class="vs-num">100</div>
          <div class="vs-unit">ads / tuần</div>
        </div>
      </div>
    ''',
    css_extra='''
      [data-composition-id="fs-lesson-4"] .ad-grid {
        display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;
        max-width: 700px; margin: 16px auto;
      }
      [data-composition-id="fs-lesson-4"] .ad-cell {
        aspect-ratio: 1;
        background: var(--surface); border: 2px solid var(--border);
        border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        font-size: 48px;
        will-change: transform, opacity;
        box-shadow: 0 6px 16px rgba(0,0,0,0.3);
      }
      [data-composition-id="fs-lesson-4"] .vs-row {
        display: flex; align-items: stretch; gap: 16px;
        margin-top: 22px; width: 100%; max-width: 720px;
      }
      [data-composition-id="fs-lesson-4"] .vs-cell {
        flex: 1; padding: 22px 18px; border-radius: 22px;
        display: flex; flex-direction: column; align-items: center;
        will-change: transform, opacity;
      }
      [data-composition-id="fs-lesson-4"] .vs-old {
        background: var(--surface); border: 2px solid var(--border);
        opacity: 0.7;
      }
      [data-composition-id="fs-lesson-4"] .vs-new {
        background: linear-gradient(135deg, var(--accent) 0%, #f4a384 100%);
        box-shadow: 0 12px 32px var(--accent-glow);
      }
      [data-composition-id="fs-lesson-4"] .vs-label {
        font-weight: 700; font-size: 22px; letter-spacing: 0.1em;
        color: var(--ink-mute); text-transform: uppercase; margin-bottom: 8px;
      }
      [data-composition-id="fs-lesson-4"] .vs-new .vs-label { color: var(--bg-cream); opacity: 0.92; }
      [data-composition-id="fs-lesson-4"] .vs-num {
        font-weight: 900; font-size: 110px; line-height: 0.9;
        letter-spacing: -0.05em;
        font-variant-numeric: tabular-nums;
        color: var(--ink); will-change: transform;
      }
      [data-composition-id="fs-lesson-4"] .vs-new .vs-num { color: var(--bg-cream); }
      [data-composition-id="fs-lesson-4"] .vs-unit {
        font-weight: 600; font-size: 22px; color: var(--ink-mute); margin-top: 6px;
      }
      [data-composition-id="fs-lesson-4"] .vs-new .vs-unit { color: var(--bg-cream); opacity: 0.85; }
      [data-composition-id="fs-lesson-4"] .vs-divider {
        align-self: center; font-weight: 800; font-size: 36px; color: var(--accent);
      }
    ''',
    timeline_js='''
      // Ad grid cells pop in rapid-fire (one per 50ms)
      tl.from(ROOT + ' .ad-cell', {
        scale: 0, opacity: 0, rotation: 180,
        duration: 0.4, ease: "back.out(2)", stagger: 0.06,
      }, 1.0);
      // Cells flip-shuffle (rotate quickly)
      tl.to(ROOT + ' .ad-cell', {
        rotationY: 360, duration: 0.6, ease: "power2.inOut",
        stagger: 0.04,
      }, 1.7);

      // VS row slide up
      tl.from(ROOT + ' .vs-old', {
        x: -80, opacity: 0, duration: 0.5, ease: "power3.out",
      }, 2.4);
      tl.from(ROOT + ' .vs-new', {
        x: 80, opacity: 0, duration: 0.5, ease: "power3.out",
      }, 2.4);
      tl.from(ROOT + ' .vs-divider', {
        scale: 0, opacity: 0, duration: 0.4, ease: "back.out(2.4)",
      }, 2.7);

      // Big number "100" punch
      tl.from(ROOT + ' .vs-new .vs-num', {
        scale: 0.5, opacity: 0, duration: 0.5, ease: "back.out(2.2)",
      }, 2.85);
      tl.to(ROOT + ' .vs-new .vs-num', {
        scale: 1.1, duration: 0.4, ease: "sine.inOut",
        yoyo: true, repeat: 4,
      }, 3.4);
    '''
)

# ============================================================
# IDEA 5 — UGC AI cho thương mại điện tử (64.2 → 76.65s)
# ============================================================
write_subcomp(
    'fs-lesson-5.html', 'fs-lesson-5',
    body_html='''
      <div class="kicker"><div class="dot"></div>Mô hình #5 · UGC AI</div>
      <div class="big-num">05</div>
      <h1 class="title-line">
        <span class="word">Test</span>
        <span class="word accent">1000 mẫu</span>
        <span class="word">video</span>
      </h1>

      <div class="phones-row">
        <div class="phone phone-1">▶</div>
        <div class="phone phone-2">▶</div>
        <div class="phone phone-3">▶</div>
        <div class="phone phone-4">▶</div>
      </div>

      <div class="counter-card">
        <div class="counter-track">
          <div class="counter-step counter-old">
            <div class="counter-num"><span id="ugc-old">20</span></div>
            <div class="counter-meta">người thật</div>
          </div>
          <div class="counter-arrow">→</div>
          <div class="counter-step counter-new">
            <div class="counter-num"><span id="ugc-new">0</span></div>
            <div class="counter-meta">AI generated</div>
          </div>
        </div>
      </div>

      <div class="product-row">
        <div class="prod">🧴 Skincare</div>
        <div class="prod">🐶 Thú cưng</div>
        <div class="prod">💊 Thực phẩm CN</div>
      </div>
    ''',
    css_extra='''
      [data-composition-id="fs-lesson-5"] .phones-row {
        display: flex; gap: 14px; margin: 16px 0; justify-content: center;
      }
      [data-composition-id="fs-lesson-5"] .phone {
        width: 100px; height: 180px;
        background: var(--surface); border: 3px solid var(--accent);
        border-radius: 18px;
        display: flex; align-items: center; justify-content: center;
        font-size: 40px; color: var(--accent);
        will-change: transform, opacity;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
      }
      [data-composition-id="fs-lesson-5"] .counter-card {
        margin: 18px 0;
        padding: 24px 30px;
        background: var(--surface); border: 2px solid var(--border);
        border-radius: 22px;
        will-change: transform, opacity;
      }
      [data-composition-id="fs-lesson-5"] .counter-track {
        display: flex; align-items: center; gap: 24px;
      }
      [data-composition-id="fs-lesson-5"] .counter-step {
        display: flex; flex-direction: column; align-items: center;
      }
      [data-composition-id="fs-lesson-5"] .counter-num {
        font-weight: 900; font-size: 96px; line-height: 0.85;
        letter-spacing: -0.04em; color: var(--ink);
        font-variant-numeric: tabular-nums;
      }
      [data-composition-id="fs-lesson-5"] .counter-new .counter-num {
        background: linear-gradient(135deg, var(--accent) 0%, #f4a384 100%);
        -webkit-background-clip: text; background-clip: text;
        color: transparent;
      }
      [data-composition-id="fs-lesson-5"] .counter-meta {
        font-weight: 600; font-size: 22px; color: var(--ink-mute); margin-top: 4px;
      }
      [data-composition-id="fs-lesson-5"] .counter-arrow {
        font-size: 56px; color: var(--accent); font-weight: 800;
      }
      [data-composition-id="fs-lesson-5"] .product-row {
        display: flex; gap: 14px; margin-top: 14px; flex-wrap: wrap; justify-content: center;
      }
      [data-composition-id="fs-lesson-5"] .prod {
        padding: 12px 22px;
        background: var(--accent); color: var(--bg-cream);
        font-weight: 700; font-size: 24px; border-radius: 999px;
        will-change: transform, opacity;
      }
    ''',
    timeline_js='''
      // Phones cascade in
      tl.from(ROOT + ' .phone', {
        y: 50, scale: 0, opacity: 0, rotation: -15,
        duration: 0.4, ease: "back.out(2)", stagger: 0.08,
      }, 1.0);
      // Phones bob
      tl.to(ROOT + ' .phone', {
        y: -10, duration: 0.5, ease: "sine.inOut",
        yoyo: true, repeat: 5, stagger: { each: 0.08, yoyo: true },
      }, 1.5);

      // Counter card slide
      tl.from(ROOT + ' .counter-card', {
        y: 30, opacity: 0, duration: 0.5, ease: "power3.out",
      }, 1.8);
      // Animated count: 0 → 1000 (fast)
      const ugcObj = { v: 0 };
      tl.to(ugcObj, {
        v: 1000, duration: 1.8, ease: "power2.out",
        onUpdate: () => {
          const el = document.querySelector(ROOT + ' #ugc-new');
          if (el) el.textContent = Math.round(ugcObj.v).toLocaleString('vi-VN');
        }
      }, 2.2);

      // Product pills slide in
      tl.from(ROOT + ' .prod', {
        x: -40, opacity: 0, duration: 0.4, ease: "power3.out", stagger: 0.12,
      }, 4.0);
    '''
)

# ============================================================
# IDEA 6 — Vertical AI / GPT Wrapper (76.9 → 92.4s)
# ============================================================
write_subcomp(
    'fs-lesson-6.html', 'fs-lesson-6',
    body_html='''
      <div class="kicker"><div class="dot"></div>Mô hình #6 · Vertical AI</div>
      <div class="big-num">06</div>
      <h1 class="title-line">
        <span class="word">Sản</span>
        <span class="word">phẩm</span>
        <span class="word accent">AI ngách</span>
      </h1>

      <div class="metaphor-stage">
        <div class="meta-cell meta-source">
          <div class="meta-ico">⚡</div>
          <div class="meta-name">Điện</div>
        </div>
        <div class="meta-flow">→</div>
        <div class="meta-products">
          <div class="meta-cell"><div class="meta-ico">🍞</div><div class="meta-name">Toaster</div></div>
          <div class="meta-cell"><div class="meta-ico">☕</div><div class="meta-name">Ấm đun</div></div>
          <div class="meta-cell"><div class="meta-ico">💡</div><div class="meta-name">Bóng đèn</div></div>
        </div>
      </div>

      <div class="quote-card">
        <div class="quote-author">— Daniel Priestley</div>
        <div class="quote-text">"AI = điện. Wrap nó vào 1 ngách, thành business <strong>$5M/năm</strong>"</div>
      </div>

      <div class="build-pill">
        🚀 Build trên <strong>Lovable</strong> · cuối tuần này
      </div>
    ''',
    css_extra='''
      [data-composition-id="fs-lesson-6"] .metaphor-stage {
        display: flex; align-items: center; gap: 22px;
        margin: 18px 0; flex-wrap: wrap; justify-content: center;
      }
      [data-composition-id="fs-lesson-6"] .meta-cell {
        display: flex; flex-direction: column; align-items: center; gap: 6px;
        padding: 16px 20px; min-width: 110px;
        background: var(--surface); border: 2px solid var(--border);
        border-radius: 18px;
        will-change: transform, opacity;
        box-shadow: 0 8px 18px rgba(0,0,0,0.3);
      }
      [data-composition-id="fs-lesson-6"] .meta-source {
        background: var(--accent); border-color: var(--accent);
        box-shadow: 0 12px 32px var(--accent-glow);
      }
      [data-composition-id="fs-lesson-6"] .meta-source .meta-name { color: var(--bg-cream); }
      [data-composition-id="fs-lesson-6"] .meta-ico { font-size: 56px; line-height: 1; }
      [data-composition-id="fs-lesson-6"] .meta-name {
        font-weight: 700; font-size: 22px; color: var(--ink);
      }
      [data-composition-id="fs-lesson-6"] .meta-flow {
        font-size: 56px; font-weight: 800; color: var(--accent);
      }
      [data-composition-id="fs-lesson-6"] .meta-products {
        display: flex; gap: 14px;
      }
      [data-composition-id="fs-lesson-6"] .quote-card {
        margin: 18px 0;
        padding: 22px 28px; max-width: 800px;
        background: rgba(217,119,87,0.1);
        border-left: 6px solid var(--accent);
        border-radius: 0 18px 18px 0;
        text-align: left;
        will-change: transform, opacity;
      }
      [data-composition-id="fs-lesson-6"] .quote-author {
        font-weight: 700; font-size: 20px; color: var(--accent);
        text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;
      }
      [data-composition-id="fs-lesson-6"] .quote-text {
        font-style: italic; font-weight: 600; font-size: 28px;
        line-height: 1.3; color: var(--ink);
      }
      [data-composition-id="fs-lesson-6"] .quote-text strong {
        color: var(--accent); font-weight: 800; font-style: normal;
      }
      [data-composition-id="fs-lesson-6"] .build-pill {
        display: inline-flex; align-items: center; gap: 10px;
        padding: 16px 30px;
        background: var(--bg-cream); color: var(--bg-dark);
        font-weight: 700; font-size: 26px; border-radius: 999px;
        margin-top: 6px; will-change: transform, opacity;
        box-shadow: 0 10px 24px rgba(0,0,0,0.4);
      }
      [data-composition-id="fs-lesson-6"] .build-pill strong {
        color: var(--accent); font-weight: 900;
      }
    ''',
    timeline_js='''
      // Source (electricity) bolt punch
      tl.from(ROOT + ' .meta-source', {
        scale: 0, opacity: 0, rotation: -90,
        duration: 0.55, ease: "back.out(2.2)",
      }, 1.0);
      tl.to(ROOT + ' .meta-source .meta-ico', {
        scale: 1.2, duration: 0.3, ease: "sine.inOut",
        yoyo: true, repeat: 5,
      }, 1.5);

      // Flow arrow
      tl.from(ROOT + ' .meta-flow', {
        x: -30, opacity: 0, duration: 0.4, ease: "power3.out",
      }, 1.5);

      // Products cascade
      tl.from(ROOT + ' .meta-products .meta-cell', {
        y: 40, scale: 0.4, opacity: 0,
        duration: 0.5, ease: "back.out(2)", stagger: 0.18,
      }, 1.8);
      tl.to(ROOT + ' .meta-products .meta-ico', {
        y: -8, duration: 0.6, ease: "sine.inOut",
        yoyo: true, repeat: 4, stagger: { each: 0.12, yoyo: true },
      }, 2.7);

      // Quote card slide in from left
      tl.from(ROOT + ' .quote-card', {
        x: -60, opacity: 0, duration: 0.55, ease: "power3.out",
      }, 3.0);

      // Build pill bounce in
      tl.from(ROOT + ' .build-pill', {
        scale: 0.4, opacity: 0, y: 20,
        duration: 0.5, ease: "back.out(2.2)",
      }, 3.7);
    '''
)

# ============================================================
# RECAP — 160 → 40 với x10 multiplier (92.6 → 103.2s)
# ============================================================
write_subcomp(
    'recap-card.html', 'recap-card',
    body_html='''
      <div class="kicker"><div class="dot"></div>Vise · CEO nói thẳng</div>
      <div class="big-num">×10</div>
      <h1 class="title-line">
        <span class="word">160</span>
        <span class="word accent">→</span>
        <span class="word">40</span>
      </h1>

      <div class="counter-stage">
        <div class="counter-side side-from">
          <div class="side-label">Trước</div>
          <div class="side-num" id="recap-from">160</div>
          <div class="side-unit">nhân viên</div>
        </div>
        <div class="counter-arrow">→</div>
        <div class="counter-side side-to">
          <div class="side-label">Sau</div>
          <div class="side-num" id="recap-to">40</div>
          <div class="side-unit">nhân viên</div>
        </div>
      </div>

      <div class="multiplier-pill">
        <span class="x">×</span><span class="mult-num">10</span>
        <span class="mult-text">hiệu suất</span>
      </div>

      <div class="recap-tag">⚡ Không phải tương lai · đang xảy ra rồi</div>
    ''',
    css_extra='''
      [data-composition-id="recap-card"] .counter-stage {
        display: flex; align-items: center; gap: 24px; margin: 20px 0;
        will-change: transform, opacity;
      }
      [data-composition-id="recap-card"] .counter-side {
        flex: 1; padding: 22px 18px; border-radius: 22px;
        display: flex; flex-direction: column; align-items: center;
        will-change: transform, opacity;
      }
      [data-composition-id="recap-card"] .side-from {
        background: var(--surface); border: 2px solid var(--border); opacity: 0.7;
      }
      [data-composition-id="recap-card"] .side-to {
        background: linear-gradient(135deg, var(--accent) 0%, #f4a384 100%);
        box-shadow: 0 16px 40px var(--accent-glow);
      }
      [data-composition-id="recap-card"] .side-label {
        font-weight: 700; font-size: 22px; letter-spacing: 0.1em;
        text-transform: uppercase; color: var(--ink-mute); margin-bottom: 6px;
      }
      [data-composition-id="recap-card"] .side-to .side-label { color: var(--bg-cream); opacity: 0.92; }
      [data-composition-id="recap-card"] .side-num {
        font-weight: 900; font-size: 130px; line-height: 0.85;
        letter-spacing: -0.05em; color: var(--ink);
        font-variant-numeric: tabular-nums;
      }
      [data-composition-id="recap-card"] .side-to .side-num { color: var(--bg-cream); }
      [data-composition-id="recap-card"] .side-unit {
        font-weight: 600; font-size: 22px; color: var(--ink-mute); margin-top: 6px;
      }
      [data-composition-id="recap-card"] .side-to .side-unit { color: var(--bg-cream); opacity: 0.85; }
      [data-composition-id="recap-card"] .counter-arrow {
        font-size: 64px; font-weight: 800; color: var(--accent);
      }
      [data-composition-id="recap-card"] .multiplier-pill {
        display: inline-flex; align-items: baseline; gap: 6px;
        padding: 16px 32px; margin-top: 8px;
        background: var(--bg-dark); border: 2px solid var(--accent);
        border-radius: 999px;
        font-weight: 800; color: var(--ink);
        box-shadow: 0 12px 32px rgba(0,0,0,0.5);
        will-change: transform, opacity;
      }
      [data-composition-id="recap-card"] .multiplier-pill .x {
        font-size: 36px; color: var(--accent);
      }
      [data-composition-id="recap-card"] .multiplier-pill .mult-num {
        font-size: 64px; line-height: 1; font-variant-numeric: tabular-nums;
        color: var(--accent);
      }
      [data-composition-id="recap-card"] .multiplier-pill .mult-text {
        font-size: 22px; font-weight: 600; margin-left: 6px; color: var(--ink);
      }
      [data-composition-id="recap-card"] .recap-tag {
        margin-top: 18px;
        font-style: italic; font-weight: 600; font-size: 26px;
        color: var(--accent);
        will-change: transform, opacity;
      }
    ''',
    timeline_js='''
      // Counter sides slide in opposing
      tl.from(ROOT + ' .side-from', {
        x: -100, opacity: 0, duration: 0.55, ease: "power3.out",
      }, 1.0);
      tl.from(ROOT + ' .side-to', {
        x: 100, opacity: 0, duration: 0.55, ease: "power3.out",
      }, 1.0);
      tl.from(ROOT + ' .counter-arrow', {
        scale: 0, rotation: -90, opacity: 0, duration: 0.5, ease: "back.out(2.4)",
      }, 1.3);

      // Animated count from-side: 0→160 (fast)
      const fromObj = { v: 0 };
      tl.to(fromObj, {
        v: 160, duration: 1.0, ease: "power2.out",
        onUpdate: () => {
          const el = document.querySelector(ROOT + ' #recap-from');
          if (el) el.textContent = Math.round(fromObj.v);
        }
      }, 1.2);
      // Then to-side counts down 160→40
      const toObj = { v: 160 };
      tl.to(toObj, {
        v: 40, duration: 1.4, ease: "power3.inOut",
        onUpdate: () => {
          const el = document.querySelector(ROOT + ' #recap-to');
          if (el) el.textContent = Math.round(toObj.v);
        }
      }, 2.4);
      // Punch the to-side number when it lands
      tl.to(ROOT + ' .side-to .side-num', {
        scale: 1.2, duration: 0.3, ease: "back.out(3)",
        yoyo: true, repeat: 1,
      }, 3.7);

      // Multiplier pill drop + bounce
      tl.from(ROOT + ' .multiplier-pill', {
        y: -50, scale: 0.4, opacity: 0,
        duration: 0.6, ease: "back.out(2.2)",
      }, 4.2);
      tl.to(ROOT + ' .multiplier-pill', {
        scale: 1.08, duration: 0.4, ease: "sine.inOut",
        yoyo: true, repeat: 3,
      }, 4.85);

      // Tag fade up
      tl.from(ROOT + ' .recap-tag', {
        y: 20, opacity: 0, duration: 0.5, ease: "power2.out",
      }, 5.0);
    '''
)

# ============================================================
# CTA — Comment Claude (103.4 → 108.92s)
# ============================================================
write_subcomp(
    'fs-cta.html', 'fs-cta',
    body_html='''
      <div class="kicker"><div class="dot"></div>Comment để nhận</div>
      <div class="big-num">⌨</div>
      <h1 class="title-line">
        <span class="word">Comment</span>
        <span class="word accent">"Claude"</span>
      </h1>

      <div class="gift-stack">
        <div class="gift-card gc-1">
          <div class="gift-ico">🎬</div>
          <div class="gift-meta">
            <div class="gift-title">Video #1 · 5 tiếng</div>
            <div class="gift-sub">Claude AI cho cá nhân</div>
          </div>
        </div>
        <div class="gift-card gc-2">
          <div class="gift-ico">🎬</div>
          <div class="gift-meta">
            <div class="gift-title">Video #2 · 5 tiếng</div>
            <div class="gift-sub">Claude AI cho doanh nghiệp</div>
          </div>
        </div>
      </div>

      <div class="bubble-row">
        <div class="bubble">💬</div>
        <div class="bubble">💬</div>
        <div class="bubble">💬</div>
      </div>

      <div class="hand-down">👇 Comment ngay 👇</div>
    ''',
    css_extra='''
      [data-composition-id="fs-cta"] .gift-stack {
        display: flex; flex-direction: column; gap: 14px;
        margin: 20px 0; width: 100%; max-width: 720px;
      }
      [data-composition-id="fs-cta"] .gift-card {
        display: flex; align-items: center; gap: 18px;
        padding: 20px 24px;
        background: var(--surface); border: 2px solid var(--accent);
        border-radius: 22px;
        will-change: transform, opacity;
        box-shadow: 0 12px 32px rgba(0,0,0,0.4);
      }
      [data-composition-id="fs-cta"] .gc-2 {
        background: linear-gradient(135deg, rgba(217,119,87,0.2) 0%, var(--surface) 100%);
      }
      [data-composition-id="fs-cta"] .gift-ico {
        font-size: 56px; line-height: 1;
        flex-shrink: 0;
      }
      [data-composition-id="fs-cta"] .gift-meta { text-align: left; flex: 1; }
      [data-composition-id="fs-cta"] .gift-title {
        font-weight: 800; font-size: 30px; color: var(--accent);
        letter-spacing: -0.01em;
      }
      [data-composition-id="fs-cta"] .gift-sub {
        font-weight: 500; font-size: 22px; color: var(--ink); margin-top: 2px;
      }
      [data-composition-id="fs-cta"] .bubble-row {
        display: flex; gap: 18px; margin: 14px 0;
      }
      [data-composition-id="fs-cta"] .bubble {
        font-size: 56px;
        will-change: transform, opacity;
        filter: drop-shadow(0 4px 12px var(--accent-glow));
      }
      [data-composition-id="fs-cta"] .hand-down {
        margin-top: 8px;
        padding: 16px 32px;
        background: var(--accent); color: var(--bg-cream);
        font-weight: 800; font-size: 28px; border-radius: 999px;
        box-shadow: 0 12px 30px var(--accent-glow);
        will-change: transform, opacity;
      }
    ''',
    timeline_js='''
      // Gift cards drop in
      tl.from(ROOT + ' .gift-card', {
        y: 40, scale: 0.85, opacity: 0,
        duration: 0.5, ease: "back.out(1.8)", stagger: 0.18,
      }, 1.0);
      // Cards subtle pulse
      tl.to(ROOT + ' .gift-card', {
        scale: 1.02, duration: 0.7, ease: "sine.inOut",
        yoyo: true, repeat: 3, stagger: { each: 0.15, yoyo: true },
      }, 1.8);

      // Bubbles bounce
      tl.from(ROOT + ' .bubble', {
        y: -40, scale: 0, opacity: 0,
        duration: 0.45, ease: "back.out(2.4)", stagger: 0.1,
      }, 1.6);
      tl.to(ROOT + ' .bubble', {
        y: -15, duration: 0.4, ease: "sine.inOut",
        yoyo: true, repeat: 5, stagger: { each: 0.08, yoyo: true },
      }, 2.2);

      // Hand-down CTA drop + wiggle
      tl.from(ROOT + ' .hand-down', {
        y: 30, scale: 0.5, opacity: 0,
        duration: 0.5, ease: "back.out(2)",
      }, 2.0);
      tl.to(ROOT + ' .hand-down', {
        scale: 1.06, duration: 0.4, ease: "sine.inOut",
        yoyo: true, repeat: 4,
      }, 2.6);
    '''
)

print(f'\nGenerated 8 rich animated sub-comps in {OUT}')
