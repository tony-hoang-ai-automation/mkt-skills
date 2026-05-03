#!/usr/bin/env python3
"""Generate 8 infographic-style sub-comps for the 6-AI-business video.

Style: Hostinger-inspired infographic — hero mockup (phone/browser/dashboard) +
floating circular badges with icons + neon glow + glassmorphism + particle decoration.
"""
import sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else 'compositions')
OUT.mkdir(exist_ok=True)

GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'

SHARED_CSS = """
:root {
  --bg-deep: #0a0815;
  --bg-mid: #161229;
  --bg-card: #1f1a3d;
  --border-glow: rgba(106, 155, 204, 0.3);
  --accent-orange: #d97757;
  --accent-cyan: #4dd9d9;
  --accent-purple: #a774d9;
  --accent-green: #5dd97a;
  --ink: #faf9f5;
  --ink-mute: #a8a4c4;
  --glow-cyan: 0 0 24px rgba(77, 217, 217, 0.55);
  --glow-orange: 0 0 24px rgba(217, 119, 87, 0.55);
  --glow-purple: 0 0 24px rgba(167, 116, 217, 0.55);
  --glow-green: 0 0 24px rgba(93, 217, 122, 0.55);
}
"""

PARTICLE_SVG = """
<svg class="particles" viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid slice">
  <circle cx="120" cy="280" r="4" fill="#4dd9d9" opacity="0.6"/>
  <circle cx="980" cy="380" r="6" fill="#a774d9" opacity="0.5"/>
  <circle cx="200" cy="1450" r="5" fill="#d97757" opacity="0.55"/>
  <circle cx="900" cy="1620" r="4" fill="#5dd97a" opacity="0.6"/>
  <circle cx="540" cy="320" r="3" fill="#4dd9d9" opacity="0.4"/>
  <circle cx="380" cy="780" r="3" fill="#a774d9" opacity="0.5"/>
  <circle cx="700" cy="900" r="4" fill="#d97757" opacity="0.45"/>
  <circle cx="160" cy="1100" r="5" fill="#5dd97a" opacity="0.55"/>
  <circle cx="850" cy="1200" r="3" fill="#4dd9d9" opacity="0.5"/>
  <circle cx="450" cy="1700" r="4" fill="#a774d9" opacity="0.4"/>
</svg>
"""


def write(filename, comp_id, body, css, js):
    html = f'''<template id="{comp_id}-template">
  <div data-composition-id="{comp_id}" data-start="0" data-width="1080" data-height="1920">
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800;900&family=Space+Mono:wght@700&display=swap" rel="stylesheet" />

    <style>
      {SHARED_CSS}
      [data-composition-id="{comp_id}"] {{
        width: 100%; height: 100%;
        background: radial-gradient(ellipse 1200px 800px at 50% 30%, var(--bg-mid) 0%, var(--bg-deep) 70%);
        color: var(--ink);
        position: relative; overflow: hidden;
        font-family: 'Be Vietnam Pro', sans-serif;
      }}
      [data-composition-id="{comp_id}"] .particles {{
        position: absolute; inset: 0; z-index: 1; pointer-events: none;
        will-change: transform, opacity;
      }}
      [data-composition-id="{comp_id}"] .particles circle {{
        will-change: transform, opacity;
      }}
      [data-composition-id="{comp_id}"] .grid-bg {{
        position: absolute; inset: 0; z-index: 0; opacity: 0.25;
        background-image:
          linear-gradient(rgba(106, 155, 204, 0.12) 1px, transparent 1px),
          linear-gradient(90deg, rgba(106, 155, 204, 0.12) 1px, transparent 1px);
        background-size: 60px 60px; pointer-events: none;
      }}
      [data-composition-id="{comp_id}"] .vignette {{
        position: absolute; inset: 0; z-index: 2; pointer-events: none;
        background: radial-gradient(ellipse 800px 600px at 50% 50%, transparent 30%, var(--bg-deep) 100%);
        opacity: 0.4;
      }}
      [data-composition-id="{comp_id}"] .scene-content {{
        position: relative; z-index: 5;
        width: 100%; height: 100%;
        padding: 200px 50px 320px;
        box-sizing: border-box;
        display: flex; flex-direction: column;
        align-items: center; justify-content: flex-start;
      }}
      [data-composition-id="{comp_id}"] .topic-pill {{
        display: inline-flex; align-items: center; gap: 10px;
        padding: 12px 24px;
        background: rgba(31, 26, 61, 0.85);
        border: 1.5px solid var(--accent-orange);
        border-radius: 999px;
        font-weight: 700; font-size: 22px; letter-spacing: 0.18em;
        text-transform: uppercase; color: var(--accent-orange);
        margin-bottom: 18px;
        backdrop-filter: blur(10px);
        will-change: transform, opacity;
        box-shadow: var(--glow-orange);
      }}
      [data-composition-id="{comp_id}"] .topic-pill .num {{
        display: inline-flex; align-items: center; justify-content: center;
        width: 32px; height: 32px;
        background: var(--accent-orange); color: var(--bg-deep);
        border-radius: 50%; font-weight: 900; font-size: 20px;
      }}
      [data-composition-id="{comp_id}"] .brand-title {{
        font-family: 'Be Vietnam Pro', sans-serif;
        font-weight: 900; font-size: 110px; line-height: 0.92;
        letter-spacing: -0.04em; text-transform: uppercase;
        margin: 0 0 28px;
        text-shadow: 0 0 40px rgba(217, 119, 87, 0.4);
        will-change: transform, opacity;
      }}
      [data-composition-id="{comp_id}"] .brand-title .accent {{
        background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%);
        -webkit-background-clip: text; background-clip: text; color: transparent;
      }}
      [data-composition-id="{comp_id}"] .brand-title .word {{
        display: inline-block; will-change: transform, opacity;
      }}
      {css}
    </style>

    <div class="grid-bg"></div>
    {PARTICLE_SVG}
    <div class="vignette"></div>
    <div class="scene-content">
      {body}
    </div>

    {GSAP}
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const ROOT = '[data-composition-id="{comp_id}"]';

      // Particles drift
      tl.fromTo(ROOT + ' .particles circle',
        {{ scale: 0, opacity: 0 }},
        {{ scale: 1, opacity: 0.6, duration: 1.2, ease: "power2.out", stagger: 0.05 }},
        0
      );
      tl.to(ROOT + ' .particles circle', {{
        y: -20, duration: 2.5, ease: "sine.inOut",
        yoyo: true, repeat: 4, stagger: {{ each: 0.1, yoyo: true }},
      }}, 1.0);

      // Topic pill enter
      tl.from(ROOT + ' .topic-pill', {{
        y: -30, scale: 0.8, opacity: 0, duration: 0.5, ease: "back.out(1.8)",
      }}, 0.2);

      // Brand title — word by word slam
      tl.from(ROOT + ' .brand-title .word', {{
        y: 80, opacity: 0, scale: 0.7, duration: 0.55,
        ease: "back.out(1.6)", stagger: 0.08,
      }}, 0.45);

      {js}

      window.__timelines["{comp_id}"] = tl;
    </script>
  </div>
</template>
'''
    (OUT / filename).write_text(html)
    print(f'  → {filename}')


# ============================================================
# IDEA 1 — Tư vấn AI ngành (Facebook case-study posts mockup)
# ============================================================
write('fs-lesson-1.html', 'fs-lesson-1',
      body='''
        <div class="topic-pill"><span class="num">1</span>Tư vấn AI</div>
        <h1 class="brand-title">
          <span class="word">Tư</span>
          <span class="word">vấn</span>
          <span class="word accent">AI</span>
        </h1>

        <!-- Facebook case-study post stack mockup -->
        <div class="post-stack">
          <div class="post-card pc-3">
            <div class="post-head">
              <div class="post-avatar"></div>
              <div class="post-meta">
                <div class="post-name">Hoàng · Tư vấn AI</div>
                <div class="post-time">15 ngày trước · 🌐</div>
              </div>
            </div>
            <div class="post-body">Case study #28 — Chatbot CSKH cho 1 spa, save 24h/tuần</div>
          </div>
          <div class="post-card pc-2">
            <div class="post-head">
              <div class="post-avatar"></div>
              <div class="post-meta">
                <div class="post-name">Hoàng · Tư vấn AI</div>
                <div class="post-time">22 ngày trước · 🌐</div>
              </div>
            </div>
            <div class="post-body">Case #22 — AI workflow cho phòng marketing</div>
          </div>
          <div class="post-card pc-1">
            <div class="post-head">
              <div class="post-avatar"></div>
              <div class="post-meta">
                <div class="post-name">Hoàng · Tư vấn AI</div>
                <div class="post-time">30 ngày trước · 🌐</div>
              </div>
            </div>
            <div class="post-body">Case #15 — Tự động kế toán cho 1 SME · save 18h/tuần</div>
            <div class="post-stats">
              <span>❤️ 1.2K</span><span>💬 87</span><span>📨 24 inbox</span>
            </div>
          </div>
        </div>

        <!-- Floating badges -->
        <div class="float-badge fb-calendar">
          <div class="fb-ico">📅</div>
          <div class="fb-num"><span id="day-count">30</span></div>
          <div class="fb-label">Ngày</div>
        </div>
        <div class="float-badge fb-industries">
          <div class="fb-ico">🎯</div>
          <div class="fb-num">3</div>
          <div class="fb-label">Ngành</div>
        </div>
        <div class="float-badge fb-inbox">
          <div class="fb-ico">📨</div>
          <div class="fb-num">+24</div>
          <div class="fb-label">Inbox</div>
        </div>
      ''',
      css='''
        [data-composition-id="fs-lesson-1"] .post-stack {
          position: relative; width: 720px; height: 500px;
          margin: 12px auto;
        }
        [data-composition-id="fs-lesson-1"] .post-card {
          position: absolute; left: 0; right: 0;
          background: rgba(31, 26, 61, 0.92);
          border: 1.5px solid var(--border-glow);
          border-radius: 18px;
          padding: 18px 22px;
          backdrop-filter: blur(12px);
          box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5);
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-1"] .pc-3 { top: 0; transform: rotate(-3deg) scale(0.92); opacity: 0.5; }
        [data-composition-id="fs-lesson-1"] .pc-2 { top: 80px; transform: rotate(2deg) scale(0.96); opacity: 0.75; }
        [data-composition-id="fs-lesson-1"] .pc-1 {
          top: 180px; box-shadow: 0 16px 48px rgba(217, 119, 87, 0.4);
          border-color: var(--accent-orange);
        }
        [data-composition-id="fs-lesson-1"] .post-head {
          display: flex; align-items: center; gap: 12px; margin-bottom: 10px;
        }
        [data-composition-id="fs-lesson-1"] .post-avatar {
          width: 44px; height: 44px; border-radius: 50%;
          background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%);
        }
        [data-composition-id="fs-lesson-1"] .post-meta { text-align: left; }
        [data-composition-id="fs-lesson-1"] .post-name {
          font-weight: 700; font-size: 22px; color: var(--ink);
        }
        [data-composition-id="fs-lesson-1"] .post-time {
          font-size: 16px; color: var(--ink-mute); margin-top: 2px;
        }
        [data-composition-id="fs-lesson-1"] .post-body {
          font-size: 24px; font-weight: 600; color: var(--ink);
          line-height: 1.3; text-align: left;
        }
        [data-composition-id="fs-lesson-1"] .post-stats {
          display: flex; gap: 18px; margin-top: 12px;
          padding-top: 12px;
          border-top: 1px solid rgba(106, 155, 204, 0.2);
          font-size: 18px; font-weight: 600; color: var(--accent-cyan);
        }
        [data-composition-id="fs-lesson-1"] .float-badge {
          position: absolute; z-index: 8;
          width: 130px; height: 130px; border-radius: 50%;
          display: flex; flex-direction: column; align-items: center; justify-content: center;
          background: rgba(31, 26, 61, 0.92);
          border: 2.5px solid var(--accent-cyan);
          box-shadow: var(--glow-cyan);
          backdrop-filter: blur(10px);
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-1"] .fb-calendar {
          top: 180px; right: 30px;
          border-color: var(--accent-orange); box-shadow: var(--glow-orange);
        }
        [data-composition-id="fs-lesson-1"] .fb-industries {
          top: 380px; left: 20px;
          border-color: var(--accent-purple); box-shadow: var(--glow-purple);
        }
        [data-composition-id="fs-lesson-1"] .fb-inbox {
          top: 580px; right: 40px;
          border-color: var(--accent-green); box-shadow: var(--glow-green);
        }
        [data-composition-id="fs-lesson-1"] .fb-ico { font-size: 26px; line-height: 1; }
        [data-composition-id="fs-lesson-1"] .fb-num {
          font-weight: 900; font-size: 32px; line-height: 1;
          margin-top: 2px; color: var(--ink);
          font-variant-numeric: tabular-nums;
        }
        [data-composition-id="fs-lesson-1"] .fb-calendar .fb-num { color: var(--accent-orange); }
        [data-composition-id="fs-lesson-1"] .fb-industries .fb-num { color: var(--accent-purple); }
        [data-composition-id="fs-lesson-1"] .fb-inbox .fb-num { color: var(--accent-green); }
        [data-composition-id="fs-lesson-1"] .fb-label {
          font-weight: 600; font-size: 14px; color: var(--ink-mute);
          letter-spacing: 0.1em; text-transform: uppercase; margin-top: 2px;
        }
      ''',
      js='''
        // Post cards stack-in
        tl.from(ROOT + ' .pc-3', { y: 60, opacity: 0, duration: 0.5, ease: "power3.out" }, 1.2);
        tl.from(ROOT + ' .pc-2', { y: 60, opacity: 0, duration: 0.5, ease: "power3.out" }, 1.4);
        tl.from(ROOT + ' .pc-1', { y: 60, opacity: 0, duration: 0.55, ease: "back.out(1.4)" }, 1.6);
        tl.from(ROOT + ' .post-stats', { opacity: 0, y: 10, duration: 0.4 }, 2.1);

        // Floating badges enter from corners
        tl.from(ROOT + ' .fb-calendar', { x: 80, y: -40, scale: 0, opacity: 0, duration: 0.55, ease: "back.out(2.2)" }, 2.0);
        tl.from(ROOT + ' .fb-industries', { x: -80, y: 30, scale: 0, opacity: 0, duration: 0.55, ease: "back.out(2.2)" }, 2.3);
        tl.from(ROOT + ' .fb-inbox', { x: 80, y: 40, scale: 0, opacity: 0, duration: 0.55, ease: "back.out(2.2)" }, 2.6);

        // Badges float bob
        tl.to(ROOT + ' .float-badge', {
          y: -12, duration: 1.2, ease: "sine.inOut",
          yoyo: true, repeat: 3, stagger: { each: 0.2, yoyo: true },
        }, 3.2);

        // Day counter tick 1 → 30
        const dayObj = { v: 1 };
        tl.set(ROOT + ' #day-count', { textContent: '1' }, 2.0);
        tl.to(dayObj, {
          v: 30, duration: 3.5, ease: "power2.out",
          onUpdate: () => {
            const el = document.querySelector(ROOT + ' #day-count');
            if (el) el.textContent = Math.round(dayObj.v);
          }
        }, 2.0);
      '''
)

# ============================================================
# IDEA 2 — GEO (ChatGPT search result mockup)
# ============================================================
write('fs-lesson-2.html', 'fs-lesson-2',
      body='''
        <div class="topic-pill"><span class="num">2</span>GEO</div>
        <h1 class="brand-title">
          <span class="word accent">AI</span>
          <span class="word">Search</span>
        </h1>

        <!-- ChatGPT-style mockup window -->
        <div class="ai-window">
          <div class="window-bar">
            <div class="dot dot-r"></div>
            <div class="dot dot-y"></div>
            <div class="dot dot-g"></div>
            <div class="window-title">💬 ChatGPT · Hỏi AI</div>
          </div>
          <div class="window-body">
            <div class="user-msg">
              <div class="msg-icon">👤</div>
              <div class="msg-text">Phòng khám nha khoa tốt nhất TP.HCM?</div>
            </div>
            <div class="ai-msg">
              <div class="msg-icon">✨</div>
              <div class="msg-text">
                Một số phòng khám được đánh giá cao:
                <div class="rec-card">
                  <div class="rec-trophy">🏆</div>
                  <div class="rec-meta">
                    <div class="rec-name">Phòng khám của bạn</div>
                    <div class="rec-tag">⭐ Top recommended · AI mentioned</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Source pills row -->
        <div class="source-row">
          <div class="src-pill">📰 PR</div>
          <div class="src-pill">💼 LinkedIn</div>
          <div class="src-pill">🔥 Reddit</div>
          <div class="src-pill">🎬 YouTube</div>
        </div>

        <!-- Floating AI logo orbits -->
        <div class="orbit-badge ob-chatgpt">💬<div class="ob-name">ChatGPT</div></div>
        <div class="orbit-badge ob-gemini">✨<div class="ob-name">Gemini</div></div>
        <div class="orbit-badge ob-perplexity">🌀<div class="ob-name">Perplexity</div></div>
      ''',
      css='''
        [data-composition-id="fs-lesson-2"] .ai-window {
          width: 760px; margin: 8px auto 14px;
          background: rgba(31, 26, 61, 0.92);
          border: 1.5px solid var(--border-glow);
          border-radius: 22px;
          backdrop-filter: blur(14px);
          box-shadow: 0 20px 60px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.08);
          overflow: hidden;
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-2"] .window-bar {
          display: flex; align-items: center; gap: 10px;
          padding: 14px 20px;
          background: rgba(10, 8, 21, 0.6);
          border-bottom: 1px solid rgba(106, 155, 204, 0.15);
        }
        [data-composition-id="fs-lesson-2"] .dot { width: 14px; height: 14px; border-radius: 50%; }
        [data-composition-id="fs-lesson-2"] .dot-r { background: #ff5f57; }
        [data-composition-id="fs-lesson-2"] .dot-y { background: #ffbd2e; }
        [data-composition-id="fs-lesson-2"] .dot-g { background: #28ca42; }
        [data-composition-id="fs-lesson-2"] .window-title {
          margin-left: auto; font-size: 16px; color: var(--ink-mute); font-weight: 600;
        }
        [data-composition-id="fs-lesson-2"] .window-body {
          padding: 22px 24px;
          display: flex; flex-direction: column; gap: 16px;
          text-align: left;
        }
        [data-composition-id="fs-lesson-2"] .user-msg, .ai-msg {
          display: flex; gap: 14px; align-items: flex-start;
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-2"] .msg-icon {
          width: 38px; height: 38px; border-radius: 50%;
          background: var(--bg-deep); border: 2px solid var(--accent-cyan);
          display: flex; align-items: center; justify-content: center;
          font-size: 20px; flex-shrink: 0;
          box-shadow: var(--glow-cyan);
        }
        [data-composition-id="fs-lesson-2"] .ai-msg .msg-icon {
          border-color: var(--accent-orange); box-shadow: var(--glow-orange);
        }
        [data-composition-id="fs-lesson-2"] .msg-text {
          flex: 1; font-size: 24px; line-height: 1.4; color: var(--ink); font-weight: 600;
        }
        [data-composition-id="fs-lesson-2"] .rec-card {
          margin-top: 14px;
          display: flex; align-items: center; gap: 14px;
          padding: 16px 18px;
          background: linear-gradient(135deg, rgba(217, 119, 87, 0.18) 0%, rgba(217, 119, 87, 0.05) 100%);
          border: 1.5px solid var(--accent-orange);
          border-radius: 14px;
          will-change: transform, opacity;
          box-shadow: var(--glow-orange);
        }
        [data-composition-id="fs-lesson-2"] .rec-trophy { font-size: 36px; line-height: 1; }
        [data-composition-id="fs-lesson-2"] .rec-name {
          font-weight: 800; font-size: 22px; color: var(--accent-orange);
        }
        [data-composition-id="fs-lesson-2"] .rec-tag {
          font-size: 16px; color: var(--ink-mute); margin-top: 2px;
        }
        [data-composition-id="fs-lesson-2"] .source-row {
          display: flex; gap: 12px; flex-wrap: wrap; justify-content: center;
          margin-top: 14px;
        }
        [data-composition-id="fs-lesson-2"] .src-pill {
          padding: 12px 22px;
          background: rgba(167, 116, 217, 0.18);
          border: 1.5px solid var(--accent-purple);
          color: var(--ink); font-weight: 700; font-size: 22px;
          border-radius: 999px;
          box-shadow: var(--glow-purple);
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-2"] .orbit-badge {
          position: absolute; z-index: 9;
          width: 110px; height: 110px; border-radius: 50%;
          background: rgba(31, 26, 61, 0.95);
          border: 2.5px solid var(--accent-cyan);
          display: flex; flex-direction: column; align-items: center; justify-content: center;
          font-size: 38px; line-height: 1;
          box-shadow: var(--glow-cyan);
          backdrop-filter: blur(10px);
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-2"] .ob-chatgpt { top: 220px; left: 30px; }
        [data-composition-id="fs-lesson-2"] .ob-gemini { top: 480px; left: 20px; border-color: var(--accent-purple); box-shadow: var(--glow-purple); }
        [data-composition-id="fs-lesson-2"] .ob-perplexity { top: 320px; right: 30px; border-color: var(--accent-orange); box-shadow: var(--glow-orange); }
        [data-composition-id="fs-lesson-2"] .ob-name {
          font-size: 13px; font-weight: 700; color: var(--ink); margin-top: 4px;
          letter-spacing: 0.05em;
        }
      ''',
      js='''
        // Window slide down
        tl.from(ROOT + ' .ai-window', { y: -40, opacity: 0, scale: 0.95, duration: 0.55, ease: "back.out(1.5)" }, 1.2);

        // User message types in
        tl.from(ROOT + ' .user-msg', { x: -40, opacity: 0, duration: 0.4, ease: "power3.out" }, 1.7);
        // AI response slide
        tl.from(ROOT + ' .ai-msg', { x: 40, opacity: 0, duration: 0.45, ease: "power3.out" }, 2.2);
        // Recommendation card highlight
        tl.from(ROOT + ' .rec-card', { y: 20, scale: 0.85, opacity: 0, duration: 0.55, ease: "back.out(2)" }, 2.7);
        tl.to(ROOT + ' .rec-card', {
          scale: 1.04, duration: 0.5, ease: "sine.inOut",
          yoyo: true, repeat: 4,
        }, 3.2);

        // Source pills cascade
        tl.from(ROOT + ' .src-pill', { y: 30, opacity: 0, duration: 0.4, ease: "back.out(1.6)", stagger: 0.1 }, 3.0);

        // Orbit badges enter from off-screen
        tl.from(ROOT + ' .ob-chatgpt', { x: -150, scale: 0, opacity: 0, duration: 0.55, ease: "back.out(2)" }, 1.5);
        tl.from(ROOT + ' .ob-perplexity', { x: 150, scale: 0, opacity: 0, duration: 0.55, ease: "back.out(2)" }, 1.7);
        tl.from(ROOT + ' .ob-gemini', { x: -150, scale: 0, opacity: 0, duration: 0.55, ease: "back.out(2)" }, 1.9);
        tl.to(ROOT + ' .orbit-badge', {
          y: -10, duration: 1.4, ease: "sine.inOut",
          yoyo: true, repeat: 3, stagger: { each: 0.2, yoyo: true },
        }, 2.8);
      '''
)

# ============================================================
# IDEA 3 — Voice AI Receptionist (iPhone call mockup)
# ============================================================
write('fs-lesson-3.html', 'fs-lesson-3',
      body='''
        <div class="topic-pill"><span class="num">3</span>Voice AI</div>
        <h1 class="brand-title">
          <span class="word">Lễ</span>
          <span class="word">tân</span>
          <span class="word accent">AI</span>
        </h1>

        <!-- iPhone call screen mockup -->
        <div class="phone-frame">
          <div class="phone-notch"></div>
          <div class="phone-screen">
            <div class="call-status">📞 Cuộc gọi đến</div>
            <div class="call-name">Nha khoa Smile · 14:32</div>
            <div class="waveform">
              <div class="wf-bar"></div><div class="wf-bar"></div><div class="wf-bar"></div>
              <div class="wf-bar"></div><div class="wf-bar"></div><div class="wf-bar"></div>
              <div class="wf-bar"></div><div class="wf-bar"></div><div class="wf-bar"></div>
              <div class="wf-bar"></div><div class="wf-bar"></div><div class="wf-bar"></div>
            </div>
            <div class="agent-bubble">
              <div class="bubble-tag">🤖 AI Agent</div>
              <div class="bubble-text">"Em đặt lịch cho anh ngày mai 2pm nhé"</div>
            </div>
            <div class="slot-grid">
              <div class="slot s-booked">9:00 ✓</div>
              <div class="slot s-booked">10:30 ✓</div>
              <div class="slot s-now">14:00 ●</div>
              <div class="slot s-open">15:30</div>
            </div>
          </div>
        </div>

        <!-- Floating badges -->
        <div class="float-badge fb-vendor">
          <div class="fb-ico">🎙️</div>
          <div class="fb-name">Eleven Labs</div>
        </div>
        <div class="float-badge fb-247">
          <div class="fb-ico">⏰</div>
          <div class="fb-num">24/7</div>
        </div>
        <div class="float-badge fb-price">
          <div class="fb-ico">💰</div>
          <div class="fb-num">2tr</div>
          <div class="fb-name">/tháng</div>
        </div>
      ''',
      css='''
        [data-composition-id="fs-lesson-3"] .phone-frame {
          width: 380px; height: 560px;
          margin: 8px auto;
          background: var(--bg-deep);
          border: 4px solid #2a2545;
          border-radius: 48px;
          padding: 18px;
          box-shadow: 0 24px 60px rgba(0,0,0,0.7), inset 0 0 30px rgba(0,0,0,0.5);
          position: relative;
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-3"] .phone-notch {
          position: absolute; top: 6px; left: 50%; transform: translateX(-50%);
          width: 120px; height: 22px;
          background: #000; border-radius: 0 0 16px 16px;
        }
        [data-composition-id="fs-lesson-3"] .phone-screen {
          width: 100%; height: 100%;
          background: linear-gradient(180deg, #1a1432 0%, #0f0a26 100%);
          border-radius: 32px;
          padding: 28px 20px 20px;
          box-sizing: border-box;
          display: flex; flex-direction: column; gap: 12px;
          text-align: center;
        }
        [data-composition-id="fs-lesson-3"] .call-status {
          font-weight: 700; font-size: 18px; color: var(--accent-green);
          letter-spacing: 0.1em; text-transform: uppercase;
        }
        [data-composition-id="fs-lesson-3"] .call-name {
          font-weight: 700; font-size: 22px; color: var(--ink);
        }
        [data-composition-id="fs-lesson-3"] .waveform {
          display: flex; align-items: flex-end; justify-content: center;
          gap: 4px; height: 40px; margin: 6px 0;
        }
        [data-composition-id="fs-lesson-3"] .wf-bar {
          width: 6px; background: var(--accent-cyan);
          border-radius: 3px;
          box-shadow: 0 0 8px rgba(77, 217, 217, 0.6);
          will-change: transform;
        }
        [data-composition-id="fs-lesson-3"] .wf-bar:nth-child(1) { height: 30%; }
        [data-composition-id="fs-lesson-3"] .wf-bar:nth-child(2) { height: 60%; }
        [data-composition-id="fs-lesson-3"] .wf-bar:nth-child(3) { height: 80%; }
        [data-composition-id="fs-lesson-3"] .wf-bar:nth-child(4) { height: 50%; }
        [data-composition-id="fs-lesson-3"] .wf-bar:nth-child(5) { height: 90%; }
        [data-composition-id="fs-lesson-3"] .wf-bar:nth-child(6) { height: 40%; }
        [data-composition-id="fs-lesson-3"] .wf-bar:nth-child(7) { height: 70%; }
        [data-composition-id="fs-lesson-3"] .wf-bar:nth-child(8) { height: 95%; }
        [data-composition-id="fs-lesson-3"] .wf-bar:nth-child(9) { height: 55%; }
        [data-composition-id="fs-lesson-3"] .wf-bar:nth-child(10) { height: 75%; }
        [data-composition-id="fs-lesson-3"] .wf-bar:nth-child(11) { height: 35%; }
        [data-composition-id="fs-lesson-3"] .wf-bar:nth-child(12) { height: 65%; }
        [data-composition-id="fs-lesson-3"] .agent-bubble {
          background: rgba(217, 119, 87, 0.18);
          border: 1.5px solid var(--accent-orange);
          border-radius: 14px;
          padding: 12px 14px;
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-3"] .bubble-tag {
          font-size: 14px; font-weight: 700; color: var(--accent-orange);
          margin-bottom: 4px;
        }
        [data-composition-id="fs-lesson-3"] .bubble-text {
          font-size: 18px; font-weight: 600; color: var(--ink);
          font-style: italic;
        }
        [data-composition-id="fs-lesson-3"] .slot-grid {
          display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
          margin-top: auto;
        }
        [data-composition-id="fs-lesson-3"] .slot {
          padding: 10px;
          border-radius: 10px;
          font-weight: 700; font-size: 15px;
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-3"] .s-booked {
          background: rgba(93, 217, 122, 0.18);
          border: 1px solid var(--accent-green);
          color: var(--accent-green);
        }
        [data-composition-id="fs-lesson-3"] .s-now {
          background: var(--accent-orange);
          color: var(--bg-deep);
          box-shadow: var(--glow-orange);
        }
        [data-composition-id="fs-lesson-3"] .s-open {
          background: rgba(168, 164, 196, 0.1);
          border: 1px solid var(--ink-mute);
          color: var(--ink-mute);
        }
        [data-composition-id="fs-lesson-3"] .float-badge {
          position: absolute; z-index: 9;
          width: 130px; height: 130px; border-radius: 50%;
          display: flex; flex-direction: column; align-items: center; justify-content: center;
          background: rgba(31, 26, 61, 0.92);
          backdrop-filter: blur(10px);
          will-change: transform, opacity;
          padding: 8px; box-sizing: border-box; text-align: center;
        }
        [data-composition-id="fs-lesson-3"] .fb-vendor {
          top: 220px; left: 30px;
          border: 2.5px solid var(--accent-cyan); box-shadow: var(--glow-cyan);
        }
        [data-composition-id="fs-lesson-3"] .fb-247 {
          top: 460px; left: 25px;
          border: 2.5px solid var(--accent-purple); box-shadow: var(--glow-purple);
        }
        [data-composition-id="fs-lesson-3"] .fb-price {
          top: 360px; right: 25px;
          width: 150px; height: 150px;
          border: 3px solid var(--accent-orange); box-shadow: var(--glow-orange);
        }
        [data-composition-id="fs-lesson-3"] .fb-ico { font-size: 26px; line-height: 1; }
        [data-composition-id="fs-lesson-3"] .fb-num {
          font-weight: 900; font-size: 32px; line-height: 1; margin-top: 4px;
          color: var(--ink); font-variant-numeric: tabular-nums;
        }
        [data-composition-id="fs-lesson-3"] .fb-price .fb-num {
          font-size: 40px; color: var(--accent-orange);
        }
        [data-composition-id="fs-lesson-3"] .fb-247 .fb-num { color: var(--accent-purple); }
        [data-composition-id="fs-lesson-3"] .fb-name {
          font-size: 13px; font-weight: 700; color: var(--ink-mute);
          letter-spacing: 0.05em; margin-top: 2px;
        }
        [data-composition-id="fs-lesson-3"] .fb-vendor .fb-name {
          font-size: 14px; color: var(--accent-cyan);
        }
      ''',
      js='''
        // Phone slide up
        tl.from(ROOT + ' .phone-frame', { y: 80, opacity: 0, scale: 0.85, duration: 0.6, ease: "back.out(1.6)" }, 1.2);

        // Waveform bars pulse continuously
        tl.fromTo(ROOT + ' .wf-bar',
          { scaleY: 0.3 },
          { scaleY: 1, duration: 0.4, ease: "sine.inOut", stagger: { each: 0.05, repeat: 8, yoyo: true } },
          1.7
        );

        // Agent bubble pop in
        tl.from(ROOT + ' .agent-bubble', { y: 20, scale: 0.7, opacity: 0, duration: 0.5, ease: "back.out(2)" }, 2.2);

        // Slot grid stagger
        tl.from(ROOT + ' .slot', { y: 20, opacity: 0, duration: 0.35, ease: "back.out(1.6)", stagger: 0.1 }, 2.6);
        tl.to(ROOT + ' .s-now', {
          scale: 1.08, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 4,
        }, 3.1);

        // Floating badges enter
        tl.from(ROOT + ' .fb-vendor', { x: -100, scale: 0, opacity: 0, duration: 0.55, ease: "back.out(2)" }, 1.7);
        tl.from(ROOT + ' .fb-247', { x: -100, scale: 0, opacity: 0, duration: 0.55, ease: "back.out(2)" }, 2.0);
        tl.from(ROOT + ' .fb-price', { x: 120, scale: 0, opacity: 0, duration: 0.6, ease: "back.out(2.2)" }, 2.3);
        tl.to(ROOT + ' .fb-price', {
          scale: 1.06, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 4,
        }, 3.0);
        tl.to(ROOT + ' .float-badge', {
          y: -10, duration: 1.4, ease: "sine.inOut",
          yoyo: true, repeat: 3, stagger: { each: 0.2, yoyo: true },
        }, 3.5);
      '''
)

# ============================================================
# IDEA 4 — Ad Agency AI (Facebook Ads dashboard mockup)
# ============================================================
write('fs-lesson-4.html', 'fs-lesson-4',
      body='''
        <div class="topic-pill"><span class="num">4</span>Ad Agency AI</div>
        <h1 class="brand-title">
          <span class="word">Quảng cáo</span>
          <span class="word accent">100×</span>
        </h1>

        <!-- Ads Manager dashboard mockup -->
        <div class="ads-dashboard">
          <div class="dash-header">
            <div class="dash-title">📊 Ads Manager · Tuần 18</div>
            <div class="dash-status">● Live</div>
          </div>
          <div class="dash-stats">
            <div class="stat-cell">
              <div class="stat-label">CREATIVES</div>
              <div class="stat-num"><span id="ad-count">0</span></div>
            </div>
            <div class="stat-cell">
              <div class="stat-label">CTR</div>
              <div class="stat-num stat-cyan">4.2%</div>
            </div>
            <div class="stat-cell">
              <div class="stat-label">CPM</div>
              <div class="stat-num stat-green">$3.80</div>
            </div>
          </div>
          <div class="creative-grid">
            <div class="creative">💪</div><div class="creative">🏠</div><div class="creative">💆</div><div class="creative">🚗</div>
            <div class="creative">🍕</div><div class="creative">👗</div><div class="creative">📱</div><div class="creative">💎</div>
            <div class="creative">⚽</div><div class="creative">📚</div><div class="creative">🎮</div><div class="creative">🌿</div>
          </div>
          <div class="chart-line">
            <svg viewBox="0 0 400 60" preserveAspectRatio="none">
              <polyline class="chart-path" points="0,55 50,50 100,40 150,38 200,30 250,20 300,18 350,8 400,5"
                fill="none" stroke="#5dd97a" stroke-width="3" stroke-linecap="round"/>
              <polyline class="chart-path-fill" points="0,55 50,50 100,40 150,38 200,30 250,20 300,18 350,8 400,5 400,60 0,60"
                fill="rgba(93, 217, 122, 0.15)" stroke="none"/>
            </svg>
          </div>
        </div>

        <!-- VS comparison -->
        <div class="vs-row">
          <div class="vs-cell vs-old">
            <div class="vs-label">Agency cũ</div>
            <div class="vs-num">5</div>
            <div class="vs-unit">/tháng</div>
          </div>
          <div class="vs-arrow">→</div>
          <div class="vs-cell vs-new">
            <div class="vs-label">AI Native</div>
            <div class="vs-num">100</div>
            <div class="vs-unit">/tuần</div>
          </div>
        </div>
      ''',
      css='''
        [data-composition-id="fs-lesson-4"] .ads-dashboard {
          width: 720px; margin: 8px auto 14px;
          background: rgba(31, 26, 61, 0.92);
          border: 1.5px solid var(--border-glow);
          border-radius: 22px;
          padding: 18px;
          backdrop-filter: blur(12px);
          box-shadow: 0 20px 50px rgba(0,0,0,0.5);
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-4"] .dash-header {
          display: flex; justify-content: space-between; align-items: center;
          padding-bottom: 12px;
          border-bottom: 1px solid rgba(106, 155, 204, 0.15);
        }
        [data-composition-id="fs-lesson-4"] .dash-title { font-weight: 700; font-size: 20px; color: var(--ink); }
        [data-composition-id="fs-lesson-4"] .dash-status {
          font-size: 16px; font-weight: 700; color: var(--accent-green);
        }
        [data-composition-id="fs-lesson-4"] .dash-stats {
          display: flex; gap: 12px; margin: 14px 0;
        }
        [data-composition-id="fs-lesson-4"] .stat-cell {
          flex: 1; padding: 12px;
          background: rgba(10, 8, 21, 0.6); border-radius: 12px;
          text-align: left;
        }
        [data-composition-id="fs-lesson-4"] .stat-label {
          font-size: 13px; font-weight: 700; color: var(--ink-mute);
          letter-spacing: 0.1em; text-transform: uppercase;
        }
        [data-composition-id="fs-lesson-4"] .stat-num {
          font-weight: 800; font-size: 36px; line-height: 1;
          color: var(--accent-orange); margin-top: 4px;
          font-variant-numeric: tabular-nums;
        }
        [data-composition-id="fs-lesson-4"] .stat-cyan { color: var(--accent-cyan); }
        [data-composition-id="fs-lesson-4"] .stat-green { color: var(--accent-green); }
        [data-composition-id="fs-lesson-4"] .creative-grid {
          display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px;
          margin-bottom: 14px;
        }
        [data-composition-id="fs-lesson-4"] .creative {
          aspect-ratio: 1;
          background: rgba(167, 116, 217, 0.15);
          border: 1.5px solid var(--accent-purple);
          border-radius: 10px;
          display: flex; align-items: center; justify-content: center;
          font-size: 28px;
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-4"] .chart-line {
          height: 60px; padding: 0 4px;
        }
        [data-composition-id="fs-lesson-4"] .chart-path {
          stroke-dasharray: 1000; stroke-dashoffset: 1000;
        }
        [data-composition-id="fs-lesson-4"] .vs-row {
          display: flex; gap: 12px; align-items: stretch;
          width: 100%; max-width: 720px;
        }
        [data-composition-id="fs-lesson-4"] .vs-cell {
          flex: 1; padding: 18px 14px;
          border-radius: 18px;
          display: flex; flex-direction: column; align-items: center;
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-4"] .vs-old {
          background: rgba(168, 164, 196, 0.1);
          border: 2px solid rgba(168, 164, 196, 0.3);
          opacity: 0.7;
        }
        [data-composition-id="fs-lesson-4"] .vs-new {
          background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%);
          box-shadow: var(--glow-orange);
        }
        [data-composition-id="fs-lesson-4"] .vs-label {
          font-size: 16px; font-weight: 700; color: var(--ink-mute);
          letter-spacing: 0.1em; text-transform: uppercase;
        }
        [data-composition-id="fs-lesson-4"] .vs-new .vs-label { color: var(--bg-deep); opacity: 0.8; }
        [data-composition-id="fs-lesson-4"] .vs-num {
          font-weight: 900; font-size: 80px; line-height: 0.9;
          letter-spacing: -0.04em; color: var(--ink); margin-top: 4px;
          font-variant-numeric: tabular-nums;
        }
        [data-composition-id="fs-lesson-4"] .vs-new .vs-num { color: var(--bg-deep); }
        [data-composition-id="fs-lesson-4"] .vs-unit {
          font-size: 18px; font-weight: 700; color: var(--ink-mute);
        }
        [data-composition-id="fs-lesson-4"] .vs-new .vs-unit { color: var(--bg-deep); opacity: 0.8; }
        [data-composition-id="fs-lesson-4"] .vs-arrow {
          align-self: center; font-size: 36px; font-weight: 800; color: var(--accent-orange);
        }
      ''',
      js='''
        // Dashboard slide in
        tl.from(ROOT + ' .ads-dashboard', { y: -30, opacity: 0, scale: 0.95, duration: 0.55, ease: "back.out(1.4)" }, 1.2);

        // Creative thumbnails rapid pop
        tl.from(ROOT + ' .creative', { scale: 0, opacity: 0, rotation: 180, duration: 0.35, ease: "back.out(2)", stagger: 0.04 }, 1.8);
        tl.to(ROOT + ' .creative', { rotationY: 360, duration: 0.5, stagger: 0.03 }, 2.5);

        // Ad count tick 0 → 100
        const adObj = { v: 0 };
        tl.to(adObj, {
          v: 100, duration: 1.6, ease: "power2.out",
          onUpdate: () => {
            const el = document.querySelector(ROOT + ' #ad-count');
            if (el) el.textContent = Math.round(adObj.v);
          }
        }, 1.9);

        // Chart line draw
        tl.to(ROOT + ' .chart-path', { strokeDashoffset: 0, duration: 1.5, ease: "power2.inOut" }, 2.5);

        // VS row slide
        tl.from(ROOT + ' .vs-old', { x: -80, opacity: 0, duration: 0.5, ease: "power3.out" }, 3.5);
        tl.from(ROOT + ' .vs-new', { x: 80, opacity: 0, duration: 0.5, ease: "power3.out" }, 3.5);
        tl.from(ROOT + ' .vs-arrow', { scale: 0, opacity: 0, duration: 0.4, ease: "back.out(2.4)" }, 3.8);
        tl.to(ROOT + ' .vs-new .vs-num', {
          scale: 1.1, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 3,
        }, 4.0);
      '''
)

# ============================================================
# IDEA 5 — UGC AI (TikTok Reels mockup)
# ============================================================
write('fs-lesson-5.html', 'fs-lesson-5',
      body='''
        <div class="topic-pill"><span class="num">5</span>UGC AI</div>
        <h1 class="brand-title">
          <span class="word accent">1000</span>
          <span class="word">mẫu test</span>
        </h1>

        <!-- TikTok phone mockup with engagement -->
        <div class="tiktok-row">
          <div class="tiktok-phone">
            <div class="tt-screen">
              <div class="tt-thumb">▶</div>
              <div class="tt-overlay">
                <div class="tt-creator">@hoang.ai</div>
                <div class="tt-caption">"Skincare routine 10s 🧴"</div>
              </div>
              <div class="tt-engage">
                <div class="eng-row"><span class="eng-ico">❤️</span><span class="eng-num">89K</span></div>
                <div class="eng-row"><span class="eng-ico">💬</span><span class="eng-num">2.1K</span></div>
                <div class="eng-row"><span class="eng-ico">🔁</span><span class="eng-num">5.4K</span></div>
              </div>
            </div>
          </div>
          <div class="tiktok-phone tp-2">
            <div class="tt-screen">
              <div class="tt-thumb">▶</div>
              <div class="tt-overlay">
                <div class="tt-creator">@hoang.ai</div>
                <div class="tt-caption">"Pet food unboxing 🐶"</div>
              </div>
            </div>
          </div>
          <div class="tiktok-phone tp-3">
            <div class="tt-screen">
              <div class="tt-thumb">▶</div>
            </div>
          </div>
        </div>

        <!-- Counter card -->
        <div class="counter-card">
          <div class="counter-side cs-old">
            <div class="cs-label">UGC creator</div>
            <div class="cs-num">20</div>
            <div class="cs-unit">video / tháng</div>
          </div>
          <div class="cs-arrow">→</div>
          <div class="counter-side cs-new">
            <div class="cs-label">AI generated</div>
            <div class="cs-num"><span id="ugc-num">0</span></div>
            <div class="cs-unit">video / tuần</div>
          </div>
        </div>

        <!-- Product chips floating -->
        <div class="float-prod fp-skincare"><span class="fp-ico">🧴</span><span>Skincare</span></div>
        <div class="float-prod fp-pet"><span class="fp-ico">🐶</span><span>Thú cưng</span></div>
        <div class="float-prod fp-food"><span class="fp-ico">💊</span><span>TPCN</span></div>
      ''',
      css='''
        [data-composition-id="fs-lesson-5"] .tiktok-row {
          display: flex; gap: 14px; margin: 8px 0; justify-content: center;
        }
        [data-composition-id="fs-lesson-5"] .tiktok-phone {
          width: 200px; height: 360px;
          background: var(--bg-deep);
          border: 4px solid #2a2545;
          border-radius: 28px;
          padding: 12px;
          will-change: transform, opacity;
          box-shadow: 0 16px 40px rgba(0,0,0,0.6);
        }
        [data-composition-id="fs-lesson-5"] .tp-2 { transform: rotate(4deg) scale(0.9); opacity: 0.85; }
        [data-composition-id="fs-lesson-5"] .tp-3 { transform: rotate(-4deg) scale(0.85); opacity: 0.7; }
        [data-composition-id="fs-lesson-5"] .tt-screen {
          width: 100%; height: 100%;
          background: linear-gradient(180deg, #1a1432 0%, #0f0a26 100%);
          border-radius: 16px;
          position: relative; overflow: hidden;
          display: flex; align-items: center; justify-content: center;
        }
        [data-composition-id="fs-lesson-5"] .tt-thumb {
          font-size: 48px; color: var(--accent-orange);
          filter: drop-shadow(0 0 20px var(--accent-orange));
        }
        [data-composition-id="fs-lesson-5"] .tt-overlay {
          position: absolute; bottom: 50px; left: 8px; right: 50px;
          text-align: left;
        }
        [data-composition-id="fs-lesson-5"] .tt-creator {
          font-weight: 800; font-size: 14px; color: var(--ink);
        }
        [data-composition-id="fs-lesson-5"] .tt-caption {
          font-size: 12px; color: var(--ink); margin-top: 4px;
          line-height: 1.3;
        }
        [data-composition-id="fs-lesson-5"] .tt-engage {
          position: absolute; right: 8px; bottom: 16px;
          display: flex; flex-direction: column; gap: 12px;
        }
        [data-composition-id="fs-lesson-5"] .eng-row {
          display: flex; flex-direction: column; align-items: center;
        }
        [data-composition-id="fs-lesson-5"] .eng-ico { font-size: 18px; }
        [data-composition-id="fs-lesson-5"] .eng-num {
          font-size: 11px; font-weight: 700; color: var(--ink); margin-top: 2px;
        }
        [data-composition-id="fs-lesson-5"] .counter-card {
          margin: 14px 0; padding: 18px 24px;
          background: rgba(31, 26, 61, 0.92);
          border: 1.5px solid var(--border-glow);
          border-radius: 22px;
          backdrop-filter: blur(10px);
          display: flex; align-items: center; gap: 20px;
          will-change: transform, opacity;
          box-shadow: 0 12px 32px rgba(0,0,0,0.4);
        }
        [data-composition-id="fs-lesson-5"] .counter-side {
          display: flex; flex-direction: column; align-items: center;
        }
        [data-composition-id="fs-lesson-5"] .cs-label {
          font-size: 14px; font-weight: 700; color: var(--ink-mute);
          letter-spacing: 0.08em; text-transform: uppercase;
        }
        [data-composition-id="fs-lesson-5"] .cs-num {
          font-weight: 900; font-size: 70px; line-height: 0.9;
          letter-spacing: -0.04em; color: var(--ink);
          font-variant-numeric: tabular-nums;
        }
        [data-composition-id="fs-lesson-5"] .cs-new .cs-num {
          background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%);
          -webkit-background-clip: text; background-clip: text; color: transparent;
        }
        [data-composition-id="fs-lesson-5"] .cs-unit {
          font-size: 14px; font-weight: 600; color: var(--ink-mute); margin-top: 2px;
        }
        [data-composition-id="fs-lesson-5"] .cs-arrow {
          font-size: 40px; font-weight: 800; color: var(--accent-orange);
        }
        [data-composition-id="fs-lesson-5"] .float-prod {
          position: absolute; z-index: 9;
          display: inline-flex; align-items: center; gap: 8px;
          padding: 10px 18px;
          background: rgba(31, 26, 61, 0.92);
          border: 2px solid var(--accent-cyan);
          border-radius: 999px;
          font-weight: 700; font-size: 18px; color: var(--ink);
          box-shadow: var(--glow-cyan);
          backdrop-filter: blur(10px);
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-5"] .fp-ico { font-size: 22px; }
        [data-composition-id="fs-lesson-5"] .fp-skincare {
          top: 280px; left: 30px;
          border-color: var(--accent-cyan); box-shadow: var(--glow-cyan);
        }
        [data-composition-id="fs-lesson-5"] .fp-pet {
          top: 380px; right: 40px;
          border-color: var(--accent-purple); box-shadow: var(--glow-purple);
        }
        [data-composition-id="fs-lesson-5"] .fp-food {
          top: 480px; left: 40px;
          border-color: var(--accent-green); box-shadow: var(--glow-green);
        }
      ''',
      js='''
        // Phones cascade
        tl.from(ROOT + ' .tiktok-phone', { y: 50, scale: 0.6, opacity: 0, duration: 0.5, ease: "back.out(1.8)", stagger: 0.12 }, 1.2);
        tl.to(ROOT + ' .tt-thumb', {
          scale: 1.15, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 5,
        }, 1.8);

        // Counter card slide
        tl.from(ROOT + ' .counter-card', { y: 30, opacity: 0, duration: 0.5, ease: "power3.out" }, 2.2);
        const ugcObj = { v: 0 };
        tl.to(ugcObj, {
          v: 1000, duration: 1.8, ease: "power2.out",
          onUpdate: () => {
            const el = document.querySelector(ROOT + ' #ugc-num');
            if (el) el.textContent = Math.round(ugcObj.v).toLocaleString('vi-VN');
          }
        }, 2.6);
        tl.to(ROOT + ' .cs-new .cs-num', {
          scale: 1.1, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 2,
        }, 4.4);

        // Floating product chips
        tl.from(ROOT + ' .fp-skincare', { x: -100, scale: 0, opacity: 0, duration: 0.5, ease: "back.out(2)" }, 1.8);
        tl.from(ROOT + ' .fp-pet', { x: 100, scale: 0, opacity: 0, duration: 0.5, ease: "back.out(2)" }, 2.1);
        tl.from(ROOT + ' .fp-food', { x: -100, scale: 0, opacity: 0, duration: 0.5, ease: "back.out(2)" }, 2.4);
        tl.to(ROOT + ' .float-prod', {
          y: -10, duration: 1.4, ease: "sine.inOut",
          yoyo: true, repeat: 3, stagger: { each: 0.2, yoyo: true },
        }, 3.0);
      '''
)

# ============================================================
# IDEA 6 — Vertical AI (App icon + metaphor + Lovable preview)
# ============================================================
write('fs-lesson-6.html', 'fs-lesson-6',
      body='''
        <div class="topic-pill"><span class="num">6</span>Vertical AI</div>
        <h1 class="brand-title">
          <span class="word accent">$5M</span>
          <span class="word">/ năm</span>
        </h1>

        <!-- App card mockup -->
        <div class="app-card">
          <div class="app-icon">⚡</div>
          <div class="app-meta">
            <div class="app-name">YourNicheAI</div>
            <div class="app-desc">Wrap AI · 1 ngách · UX riêng</div>
            <div class="app-stats">
              <span class="badge-stat">⭐ 4.9</span>
              <span class="badge-stat">📈 $5M ARR</span>
              <span class="badge-stat">👥 1.2K users</span>
            </div>
          </div>
        </div>

        <!-- Electricity metaphor row -->
        <div class="meta-stage">
          <div class="meta-cell ms-source">
            <div class="ms-ico">⚡</div>
            <div class="ms-label">AI / Điện</div>
          </div>
          <div class="ms-flow">→</div>
          <div class="meta-products">
            <div class="meta-cell"><div class="ms-ico">🍞</div><div class="ms-label">Toaster</div></div>
            <div class="meta-cell"><div class="ms-ico">☕</div><div class="ms-label">Ấm đun</div></div>
            <div class="meta-cell"><div class="ms-ico">💡</div><div class="ms-label">Bóng đèn</div></div>
          </div>
        </div>

        <!-- Lovable build pill -->
        <div class="build-pill">
          <span class="bp-ico">🚀</span>
          <span>Build trên <strong>Lovable</strong> · cuối tuần này</span>
        </div>

        <!-- Quote attribution -->
        <div class="quote-attrib">
          <div class="qa-line">— <strong>Daniel Priestley</strong></div>
        </div>
      ''',
      css='''
        [data-composition-id="fs-lesson-6"] .app-card {
          width: 720px; margin: 6px auto 14px;
          background: rgba(31, 26, 61, 0.92);
          border: 1.5px solid var(--accent-orange);
          border-radius: 22px;
          padding: 18px 22px;
          display: flex; align-items: center; gap: 18px;
          box-shadow: var(--glow-orange);
          backdrop-filter: blur(12px);
          will-change: transform, opacity;
        }
        [data-composition-id="fs-lesson-6"] .app-icon {
          width: 90px; height: 90px;
          background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%);
          border-radius: 22px;
          display: flex; align-items: center; justify-content: center;
          font-size: 56px;
          box-shadow: var(--glow-orange), inset 0 -4px 0 rgba(0,0,0,0.2);
          flex-shrink: 0;
        }
        [data-composition-id="fs-lesson-6"] .app-meta { flex: 1; text-align: left; }
        [data-composition-id="fs-lesson-6"] .app-name {
          font-weight: 800; font-size: 30px; color: var(--ink);
          letter-spacing: -0.02em;
        }
        [data-composition-id="fs-lesson-6"] .app-desc {
          font-size: 18px; color: var(--ink-mute); margin-top: 2px;
        }
        [data-composition-id="fs-lesson-6"] .app-stats {
          display: flex; gap: 8px; margin-top: 10px;
        }
        [data-composition-id="fs-lesson-6"] .badge-stat {
          font-size: 14px; font-weight: 700;
          padding: 6px 12px;
          background: rgba(77, 217, 217, 0.12);
          border: 1px solid rgba(77, 217, 217, 0.3);
          color: var(--accent-cyan);
          border-radius: 999px;
        }
        [data-composition-id="fs-lesson-6"] .meta-stage {
          display: flex; align-items: center; gap: 16px;
          margin: 12px 0; flex-wrap: wrap; justify-content: center;
        }
        [data-composition-id="fs-lesson-6"] .meta-cell {
          display: flex; flex-direction: column; align-items: center;
          padding: 14px 16px; min-width: 100px;
          background: rgba(31, 26, 61, 0.92);
          border: 2px solid var(--border-glow);
          border-radius: 16px;
          will-change: transform, opacity;
          backdrop-filter: blur(8px);
        }
        [data-composition-id="fs-lesson-6"] .ms-source {
          background: var(--accent-orange); border-color: var(--accent-orange);
          box-shadow: var(--glow-orange);
        }
        [data-composition-id="fs-lesson-6"] .ms-source .ms-label { color: var(--bg-deep); font-weight: 800; }
        [data-composition-id="fs-lesson-6"] .ms-ico { font-size: 44px; line-height: 1; }
        [data-composition-id="fs-lesson-6"] .ms-label {
          font-weight: 700; font-size: 16px; color: var(--ink); margin-top: 6px;
        }
        [data-composition-id="fs-lesson-6"] .ms-flow {
          font-size: 40px; font-weight: 800; color: var(--accent-orange);
        }
        [data-composition-id="fs-lesson-6"] .meta-products { display: flex; gap: 10px; }
        [data-composition-id="fs-lesson-6"] .build-pill {
          display: inline-flex; align-items: center; gap: 10px;
          padding: 14px 24px;
          background: rgba(93, 217, 122, 0.18);
          border: 2px solid var(--accent-green);
          color: var(--ink);
          font-weight: 700; font-size: 22px;
          border-radius: 999px;
          box-shadow: var(--glow-green);
          margin-top: 8px;
          will-change: transform, opacity;
          backdrop-filter: blur(10px);
        }
        [data-composition-id="fs-lesson-6"] .build-pill strong { color: var(--accent-green); font-weight: 900; }
        [data-composition-id="fs-lesson-6"] .quote-attrib {
          margin-top: 12px;
          font-style: italic; font-size: 18px; color: var(--ink-mute);
        }
        [data-composition-id="fs-lesson-6"] .quote-attrib strong { color: var(--accent-purple); font-style: normal; }
      ''',
      js='''
        // App card slide in
        tl.from(ROOT + ' .app-card', { y: 30, opacity: 0, scale: 0.92, duration: 0.55, ease: "back.out(1.6)" }, 1.2);
        tl.from(ROOT + ' .app-icon', { rotation: -180, scale: 0, duration: 0.5, ease: "back.out(2.2)" }, 1.4);
        tl.from(ROOT + ' .badge-stat', { y: 10, opacity: 0, duration: 0.35, ease: "power3.out", stagger: 0.1 }, 1.8);

        // Source punch
        tl.from(ROOT + ' .ms-source', { scale: 0, opacity: 0, rotation: -90, duration: 0.55, ease: "back.out(2.2)" }, 2.2);
        tl.to(ROOT + ' .ms-source .ms-ico', {
          scale: 1.2, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 5,
        }, 2.7);
        tl.from(ROOT + ' .ms-flow', { x: -30, opacity: 0, duration: 0.4, ease: "power3.out" }, 2.7);
        tl.from(ROOT + ' .meta-products .meta-cell', {
          y: 30, scale: 0.5, opacity: 0,
          duration: 0.5, ease: "back.out(2)", stagger: 0.15,
        }, 2.9);
        tl.to(ROOT + ' .meta-products .ms-ico', {
          y: -8, duration: 0.6, ease: "sine.inOut",
          yoyo: true, repeat: 3, stagger: { each: 0.12, yoyo: true },
        }, 3.7);

        // Build pill bounce
        tl.from(ROOT + ' .build-pill', { y: 30, scale: 0.6, opacity: 0, duration: 0.5, ease: "back.out(2)" }, 3.4);

        // Quote attrib
        tl.from(ROOT + ' .quote-attrib', { y: 10, opacity: 0, duration: 0.4 }, 3.8);
      '''
)

# ============================================================
# RECAP — 160 → 40 with team grid morph
# ============================================================
def gen_team_dots():
    """Generate 40 visible person dots in a 8x5 grid."""
    out = []
    for row in range(5):
        for col in range(8):
            x = col * 18 + 10
            y = row * 18 + 10
            out.append(f'<div class="team-dot td-r{row}c{col}" style="left:{x}%; top:{y}%;"></div>')
    return '\n        '.join(out)

write('recap-card.html', 'recap-card',
      body=f'''
        <div class="topic-pill"><span class="num">▼</span>Vise · CEO nói thẳng</div>
        <h1 class="brand-title">
          <span class="word">160 →</span>
          <span class="word accent">40</span>
        </h1>

        <!-- Team morph visualization: 160 dots → 40 dots remaining -->
        <div class="team-board">
          <div class="board-header">
            <div class="bh-label">Headcount</div>
            <div class="bh-stat"><span id="team-num">160</span> nhân viên</div>
          </div>
          <div class="team-grid">
            {gen_team_dots()}
          </div>
        </div>

        <!-- Multiplier callout -->
        <div class="mult-stage">
          <div class="mult-pill">
            <span class="mult-x">×</span>
            <span class="mult-num">10</span>
          </div>
          <div class="mult-text">Hiệu suất<br/><strong>tăng gấp 10 lần</strong></div>
        </div>

        <!-- Tag -->
        <div class="recap-tag">⚡ Không phải tương lai · đang xảy ra rồi</div>
      ''',
      css='''
        [data-composition-id="recap-card"] .team-board {
          width: 720px; margin: 6px auto 14px;
          background: rgba(31, 26, 61, 0.92);
          border: 1.5px solid var(--border-glow);
          border-radius: 22px;
          padding: 18px;
          backdrop-filter: blur(12px);
          box-shadow: 0 12px 32px rgba(0,0,0,0.4);
          will-change: transform, opacity;
        }
        [data-composition-id="recap-card"] .board-header {
          display: flex; justify-content: space-between; align-items: center;
          padding-bottom: 14px;
          border-bottom: 1px solid rgba(106, 155, 204, 0.15);
        }
        [data-composition-id="recap-card"] .bh-label {
          font-size: 16px; font-weight: 700; color: var(--ink-mute);
          letter-spacing: 0.1em; text-transform: uppercase;
        }
        [data-composition-id="recap-card"] .bh-stat {
          font-weight: 800; font-size: 28px; color: var(--accent-orange);
          font-variant-numeric: tabular-nums;
        }
        [data-composition-id="recap-card"] .team-grid {
          position: relative; height: 170px; margin-top: 14px;
        }
        [data-composition-id="recap-card"] .team-dot {
          position: absolute;
          width: 22px; height: 22px;
          border-radius: 50%;
          background: var(--accent-cyan);
          box-shadow: 0 0 8px rgba(77, 217, 217, 0.5);
          will-change: transform, opacity;
        }
        [data-composition-id="recap-card"] .team-dot.dot-cut {
          background: rgba(168, 164, 196, 0.2); box-shadow: none;
        }
        [data-composition-id="recap-card"] .mult-stage {
          display: flex; align-items: center; gap: 18px;
          margin: 8px 0;
          will-change: transform, opacity;
        }
        [data-composition-id="recap-card"] .mult-pill {
          display: inline-flex; align-items: baseline; gap: 4px;
          padding: 16px 28px;
          background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%);
          color: var(--bg-deep);
          border-radius: 22px;
          box-shadow: var(--glow-orange);
        }
        [data-composition-id="recap-card"] .mult-x {
          font-size: 36px; font-weight: 800;
        }
        [data-composition-id="recap-card"] .mult-num {
          font-size: 80px; line-height: 0.85;
          font-weight: 900; letter-spacing: -0.04em;
          font-variant-numeric: tabular-nums;
        }
        [data-composition-id="recap-card"] .mult-text {
          font-size: 22px; font-weight: 600; color: var(--ink); text-align: left;
          line-height: 1.3;
        }
        [data-composition-id="recap-card"] .mult-text strong {
          color: var(--accent-orange); font-weight: 800;
        }
        [data-composition-id="recap-card"] .recap-tag {
          margin-top: 14px;
          font-style: italic; font-weight: 600; font-size: 24px;
          color: var(--accent-cyan);
          will-change: transform, opacity;
        }
      ''',
      js='''
        // Team board enter
        tl.from(ROOT + ' .team-board', { y: 30, opacity: 0, scale: 0.95, duration: 0.55, ease: "back.out(1.5)" }, 1.0);

        // Dots pop in (40 dots, fast stagger)
        tl.from(ROOT + ' .team-dot', {
          scale: 0, opacity: 0, duration: 0.3, ease: "back.out(1.6)",
          stagger: { each: 0.012, from: "random" },
        }, 1.4);

        // Header counter 0 → 160 fast
        const upObj = { v: 0 };
        tl.to(upObj, {
          v: 160, duration: 1.0, ease: "power2.out",
          onUpdate: () => {
            const el = document.querySelector(ROOT + ' #team-num');
            if (el) el.textContent = Math.round(upObj.v);
          }
        }, 1.4);

        // Then countdown 160 → 40, while dots fade to grey
        const dnObj = { v: 160 };
        tl.to(dnObj, {
          v: 40, duration: 1.6, ease: "power3.inOut",
          onUpdate: () => {
            const el = document.querySelector(ROOT + ' #team-num');
            if (el) el.textContent = Math.round(dnObj.v);
          }
        }, 2.6);
        // Cut 30 dots (75%) — fade them grey
        tl.to(ROOT + ' .team-dot:nth-child(n+11)', {
          backgroundColor: 'rgba(168, 164, 196, 0.2)',
          boxShadow: 'none', scale: 0.6,
          duration: 1.4, ease: "power2.inOut", stagger: 0.025,
        }, 2.6);

        // Multiplier punch
        tl.from(ROOT + ' .mult-pill', { scale: 0.4, opacity: 0, rotation: -10, duration: 0.6, ease: "back.out(2.2)" }, 4.2);
        tl.to(ROOT + ' .mult-pill', {
          scale: 1.06, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 3,
        }, 4.85);
        tl.from(ROOT + ' .mult-text', { x: -30, opacity: 0, duration: 0.45, ease: "power3.out" }, 4.5);

        // Tag fade
        tl.from(ROOT + ' .recap-tag', { y: 14, opacity: 0, duration: 0.5 }, 5.0);
      '''
)

# ============================================================
# CTA — Comment Claude (Facebook comment box mockup)
# ============================================================
write('fs-cta.html', 'fs-cta',
      body='''
        <div class="topic-pill"><span class="num">▼</span>Comment để nhận</div>
        <h1 class="brand-title">
          <span class="word">Comment</span>
          <span class="word accent">"Claude"</span>
        </h1>

        <!-- Facebook comment box mockup -->
        <div class="comment-box">
          <div class="cb-avatar">B</div>
          <div class="cb-input">
            <span class="cb-text">Claude</span><span class="cb-cursor">|</span>
          </div>
          <div class="cb-send">▶</div>
        </div>

        <!-- Gift cards stack -->
        <div class="gift-stack">
          <div class="gift-card">
            <div class="gc-thumb">🎬</div>
            <div class="gc-meta">
              <div class="gc-tag">VIDEO #1 · 5 TIẾNG</div>
              <div class="gc-title">Claude AI cho cá nhân</div>
            </div>
            <div class="gc-badge">FREE</div>
          </div>
          <div class="gift-card">
            <div class="gc-thumb">🎬</div>
            <div class="gc-meta">
              <div class="gc-tag">VIDEO #2 · 5 TIẾNG</div>
              <div class="gc-title">Claude AI cho doanh nghiệp</div>
            </div>
            <div class="gc-badge">FREE</div>
          </div>
        </div>

        <!-- Hand pointing down -->
        <div class="hand-cta">👇 Comment ngay 👇</div>
      ''',
      css='''
        [data-composition-id="fs-cta"] .comment-box {
          width: 720px; margin: 6px auto 14px;
          display: flex; align-items: center; gap: 12px;
          padding: 18px;
          background: rgba(31, 26, 61, 0.92);
          border: 2px solid var(--accent-orange);
          border-radius: 18px;
          box-shadow: var(--glow-orange);
          backdrop-filter: blur(12px);
          will-change: transform, opacity;
        }
        [data-composition-id="fs-cta"] .cb-avatar {
          width: 48px; height: 48px; border-radius: 50%;
          background: var(--accent-cyan); color: var(--bg-deep);
          display: flex; align-items: center; justify-content: center;
          font-weight: 800; font-size: 22px;
          flex-shrink: 0;
        }
        [data-composition-id="fs-cta"] .cb-input {
          flex: 1; text-align: left;
          padding: 12px 16px;
          background: rgba(10, 8, 21, 0.6);
          border-radius: 999px;
          font-size: 26px; font-weight: 700; color: var(--ink);
        }
        [data-composition-id="fs-cta"] .cb-text {
          color: var(--accent-orange);
          background: rgba(217, 119, 87, 0.15);
          padding: 2px 10px; border-radius: 6px;
        }
        [data-composition-id="fs-cta"] .cb-cursor {
          color: var(--accent-orange);
          animation: caret 0.6s steps(1) infinite;
        }
        @keyframes caret { 50% { opacity: 0; } }
        [data-composition-id="fs-cta"] .cb-send {
          width: 48px; height: 48px; border-radius: 50%;
          background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%);
          color: var(--bg-deep);
          display: flex; align-items: center; justify-content: center;
          font-size: 22px; font-weight: 800;
          box-shadow: var(--glow-orange);
          flex-shrink: 0;
        }
        [data-composition-id="fs-cta"] .gift-stack {
          display: flex; flex-direction: column; gap: 12px;
          width: 720px;
        }
        [data-composition-id="fs-cta"] .gift-card {
          display: flex; align-items: center; gap: 14px;
          padding: 16px 18px;
          background: rgba(31, 26, 61, 0.92);
          border: 1.5px solid var(--border-glow);
          border-radius: 18px;
          backdrop-filter: blur(10px);
          box-shadow: 0 12px 28px rgba(0,0,0,0.4);
          will-change: transform, opacity;
        }
        [data-composition-id="fs-cta"] .gc-thumb {
          width: 70px; height: 70px;
          background: linear-gradient(135deg, var(--accent-purple) 0%, #c498e0 100%);
          border-radius: 14px;
          display: flex; align-items: center; justify-content: center;
          font-size: 38px;
          box-shadow: var(--glow-purple);
          flex-shrink: 0;
        }
        [data-composition-id="fs-cta"] .gc-meta { flex: 1; text-align: left; }
        [data-composition-id="fs-cta"] .gc-tag {
          font-size: 13px; font-weight: 800; color: var(--accent-cyan);
          letter-spacing: 0.12em; text-transform: uppercase;
        }
        [data-composition-id="fs-cta"] .gc-title {
          font-size: 24px; font-weight: 800; color: var(--ink); margin-top: 4px;
          letter-spacing: -0.01em;
        }
        [data-composition-id="fs-cta"] .gc-badge {
          padding: 6px 12px;
          background: var(--accent-green); color: var(--bg-deep);
          border-radius: 999px;
          font-weight: 800; font-size: 14px;
          box-shadow: var(--glow-green);
          flex-shrink: 0;
        }
        [data-composition-id="fs-cta"] .hand-cta {
          margin-top: 14px;
          padding: 16px 32px;
          background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%);
          color: var(--bg-deep);
          font-weight: 800; font-size: 26px; border-radius: 999px;
          box-shadow: var(--glow-orange);
          will-change: transform, opacity;
        }
      ''',
      js='''
        // Comment box drop in
        tl.from(ROOT + ' .comment-box', { y: -30, opacity: 0, scale: 0.92, duration: 0.5, ease: "back.out(1.6)" }, 1.0);
        tl.from(ROOT + ' .cb-text', { scale: 0, opacity: 0, duration: 0.4, ease: "back.out(2)" }, 1.4);

        // Gift cards stack drop
        tl.from(ROOT + ' .gift-card', { y: 40, opacity: 0, scale: 0.9, duration: 0.5, ease: "back.out(1.6)", stagger: 0.18 }, 1.6);
        tl.from(ROOT + ' .gc-badge', { scale: 0, opacity: 0, rotation: -30, duration: 0.45, ease: "back.out(2.4)", stagger: 0.18 }, 2.0);

        // Pulse gift cards
        tl.to(ROOT + ' .gift-card', {
          scale: 1.02, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 3, stagger: { each: 0.15, yoyo: true },
        }, 2.4);

        // Hand CTA punch
        tl.from(ROOT + ' .hand-cta', { y: 30, scale: 0.5, opacity: 0, duration: 0.5, ease: "back.out(2.2)" }, 2.6);
        tl.to(ROOT + ' .hand-cta', {
          scale: 1.06, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 4,
        }, 3.2);
      '''
)

print(f'\nGenerated 8 infographic-style sub-comps in {OUT}')
