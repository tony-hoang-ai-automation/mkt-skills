#!/usr/bin/env python3
"""Generic infographic-style sub-comp scaffolder.

Reads scenes.json with `mockup_variant` + `content` per scene and generates
8 polished infographic mockups: post-stack, ai-window, phone-call, dashboard,
tiktok-grid, app-card, team-grid, comment-box.

Each scene type renders a dedicated UI mockup (not abstract decoration) with
floating data badges, animated entrances, and brand-style typography.

Usage:
  python3 scaffold_infographic_v2.py \
    --output workspace/content/YYYY-MM-DD/<slug>/compositions/ \
    --scenes scenes.json \
    --captions caption-groups.json
"""
import argparse
import json
import sys
from pathlib import Path

GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'

# ====== DESIGN TOKENS — same palette as Hostinger-style ======
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


def shell(comp_id: str, body: str, css: str, js: str) -> str:
    """Wrap a sub-comp body with shared shell (background, particles, header pill, brand title, scripts)."""
    return f'''<template id="{comp_id}-template">
  <div data-composition-id="{comp_id}" data-start="0" data-width="1080" data-height="1920">
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />

    <style>
      {SHARED_CSS}
      [data-composition-id="{comp_id}"] {{
        width: 100%; height: 100%;
        background: radial-gradient(ellipse 1200px 800px at 50% 30%, var(--bg-mid) 0%, var(--bg-deep) 70%);
        color: var(--ink);
        position: relative; overflow: hidden;
        font-family: 'Be Vietnam Pro', sans-serif;
      }}
      [data-composition-id="{comp_id}"] .particles {{ position: absolute; inset: 0; z-index: 1; pointer-events: none; will-change: transform, opacity; }}
      [data-composition-id="{comp_id}"] .particles circle {{ will-change: transform, opacity; }}
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
        margin: 0 0 28px; text-align: center;
        text-shadow: 0 0 40px rgba(217, 119, 87, 0.4);
        will-change: transform, opacity;
      }}
      [data-composition-id="{comp_id}"] .brand-title .accent {{
        background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%);
        -webkit-background-clip: text; background-clip: text; color: transparent;
      }}
      [data-composition-id="{comp_id}"] .brand-title .word {{
        display: inline-block; will-change: transform, opacity; margin-right: 0.18em;
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

      // Topic pill
      tl.from(ROOT + ' .topic-pill', {{
        y: -30, scale: 0.8, opacity: 0, duration: 0.5, ease: "back.out(1.8)",
      }}, 0.2);

      // Brand title slam
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


def title_words(title: str, accent_words: list[int] = None) -> str:
    """Wrap each word in span.word; mark accent words."""
    accent_words = accent_words or []
    parts = title.split()
    out = []
    for i, w in enumerate(parts):
        cls = 'word accent' if i in accent_words else 'word'
        out.append(f'<span class="{cls}">{w}</span>')
    return '\n          '.join(out)


def floating_badges(badges: list[dict]) -> tuple[str, str, str]:
    """Render N floating badges. Each badge: {pos: "tl|tr|bl|br|ml|mr", color: "cyan|purple|orange|green", icon: "📅", num: "30", label: "ngày"}.
    Returns (html, css, js)."""
    pos_map = {
        'tl': 'top: 220px; left: 30px;',
        'tr': 'top: 220px; right: 30px;',
        'bl': 'top: 580px; left: 30px;',
        'br': 'top: 580px; right: 30px;',
        'ml': 'top: 400px; left: 25px;',
        'mr': 'top: 400px; right: 25px;',
    }
    enter_map = {'tl': '-100, -40', 'tr': '100, -40', 'bl': '-100, 40', 'br': '100, 40', 'ml': '-100, 0', 'mr': '100, 0'}
    color_var = {'cyan': '--accent-cyan', 'purple': '--accent-purple', 'orange': '--accent-orange', 'green': '--accent-green'}
    glow_var = {'cyan': '--glow-cyan', 'purple': '--glow-purple', 'orange': '--glow-orange', 'green': '--glow-green'}

    html_parts, css_parts, js_parts = [], [], []
    for i, b in enumerate(badges):
        pos = b.get('pos', 'tr')
        color = b.get('color', 'cyan')
        cls = f'flb-{i}'
        html_parts.append(f'''<div class="float-badge {cls}">
          <div class="fb-ico">{b.get('icon', '★')}</div>
          <div class="fb-num">{b.get('num', '')}</div>
          <div class="fb-label">{b.get('label', '')}</div>
        </div>''')
        css_parts.append(f'''[data-composition-id="COMP_ID"] .{cls} {{
          {pos_map[pos]}
          border-color: var({color_var[color]}); box-shadow: var({glow_var[color]});
        }}
        [data-composition-id="COMP_ID"] .{cls} .fb-num {{ color: var({color_var[color]}); }}''')
        x, y = enter_map[pos].split(', ')
        js_parts.append(f'''tl.from(ROOT + ' .{cls}', {{ x: {x}, y: {y}, scale: 0, opacity: 0, duration: 0.55, ease: "back.out(2.2)" }}, {1.8 + i * 0.2});''')

    base_css = '''
        [data-composition-id="COMP_ID"] .float-badge {
          position: absolute; z-index: 9;
          width: 130px; height: 130px; border-radius: 50%;
          display: flex; flex-direction: column; align-items: center; justify-content: center;
          background: rgba(31, 26, 61, 0.92);
          backdrop-filter: blur(10px);
          border: 2.5px solid var(--accent-cyan);
          box-shadow: var(--glow-cyan);
          will-change: transform, opacity;
          padding: 8px; box-sizing: border-box; text-align: center;
        }
        [data-composition-id="COMP_ID"] .fb-ico { font-size: 26px; line-height: 1; }
        [data-composition-id="COMP_ID"] .fb-num {
          font-weight: 900; font-size: 30px; line-height: 1; margin-top: 2px;
          color: var(--ink); font-variant-numeric: tabular-nums;
        }
        [data-composition-id="COMP_ID"] .fb-label {
          font-weight: 600; font-size: 14px; color: var(--ink-mute);
          letter-spacing: 0.1em; text-transform: uppercase; margin-top: 2px;
        }'''
    bob_js = '''tl.to(ROOT + ' .float-badge', { y: -10, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: 3, stagger: { each: 0.2, yoyo: true } }, 3.5);'''

    return ('\n        '.join(html_parts), base_css + '\n' + '\n'.join(css_parts), '\n        '.join(js_parts) + '\n        ' + bob_js)


# ====== 8 MOCKUP VARIANT TEMPLATES ======

def variant_post_stack(content: dict) -> tuple[str, str, str]:
    """Mockup: 3 social media post cards stacked, top card highlighted."""
    posts = content.get('posts', [])
    while len(posts) < 3:
        posts.append({'name': 'User', 'time': 'now', 'body': 'Sample post', 'stats': []})

    cards_html = ''
    for i, p in enumerate(reversed(posts[:3])):
        idx = 3 - i  # 3, 2, 1 (1 is top/highlighted)
        stats_html = ''
        if idx == 1 and p.get('stats'):
            stats_html = f'<div class="post-stats">' + ''.join(f'<span>{s}</span>' for s in p['stats']) + '</div>'
        cards_html += f'''
        <div class="post-card pc-{idx}">
          <div class="post-head">
            <div class="post-avatar"></div>
            <div class="post-meta">
              <div class="post-name">{p.get('name', 'User')}</div>
              <div class="post-time">{p.get('time', 'now')}</div>
            </div>
          </div>
          <div class="post-body">{p.get('body', '')}</div>
          {stats_html}
        </div>'''

    body = f'<div class="post-stack">{cards_html}</div>'
    css = '''
        [data-composition-id="COMP_ID"] .post-stack { position: relative; width: 720px; height: 500px; margin: 12px auto; }
        [data-composition-id="COMP_ID"] .post-card {
          position: absolute; left: 0; right: 0;
          background: rgba(31, 26, 61, 0.92);
          border: 1.5px solid var(--border-glow);
          border-radius: 18px; padding: 18px 22px;
          backdrop-filter: blur(12px);
          box-shadow: 0 12px 32px rgba(0,0,0,0.5);
          will-change: transform, opacity;
        }
        [data-composition-id="COMP_ID"] .pc-3 { top: 0; transform: rotate(-3deg) scale(0.92); opacity: 0.5; }
        [data-composition-id="COMP_ID"] .pc-2 { top: 80px; transform: rotate(2deg) scale(0.96); opacity: 0.75; }
        [data-composition-id="COMP_ID"] .pc-1 { top: 180px; box-shadow: 0 16px 48px rgba(217, 119, 87, 0.4); border-color: var(--accent-orange); }
        [data-composition-id="COMP_ID"] .post-head { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
        [data-composition-id="COMP_ID"] .post-avatar { width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%); }
        [data-composition-id="COMP_ID"] .post-meta { text-align: left; }
        [data-composition-id="COMP_ID"] .post-name { font-weight: 700; font-size: 22px; color: var(--ink); }
        [data-composition-id="COMP_ID"] .post-time { font-size: 16px; color: var(--ink-mute); margin-top: 2px; }
        [data-composition-id="COMP_ID"] .post-body { font-size: 24px; font-weight: 600; color: var(--ink); line-height: 1.3; text-align: left; }
        [data-composition-id="COMP_ID"] .post-stats { display: flex; gap: 18px; margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(106, 155, 204, 0.2); font-size: 18px; font-weight: 600; color: var(--accent-cyan); }'''
    js = '''tl.from(ROOT + ' .pc-3', { y: 60, opacity: 0, duration: 0.5, ease: "power3.out" }, 1.2);
        tl.from(ROOT + ' .pc-2', { y: 60, opacity: 0, duration: 0.5, ease: "power3.out" }, 1.4);
        tl.from(ROOT + ' .pc-1', { y: 60, opacity: 0, duration: 0.55, ease: "back.out(1.4)" }, 1.6);
        tl.from(ROOT + ' .post-stats', { opacity: 0, y: 10, duration: 0.4 }, 2.1);'''
    return body, css, js


def variant_ai_window(content: dict) -> tuple[str, str, str]:
    """Mockup: ChatGPT-style window with user message + AI response + recommendation card."""
    body = f'''
        <div class="ai-window">
          <div class="window-bar">
            <div class="dot dot-r"></div>
            <div class="dot dot-y"></div>
            <div class="dot dot-g"></div>
            <div class="window-title">{content.get('window_title', '💬 AI Chat')}</div>
          </div>
          <div class="window-body">
            <div class="user-msg">
              <div class="msg-icon">👤</div>
              <div class="msg-text">{content.get('user_query', 'Sample question?')}</div>
            </div>
            <div class="ai-msg">
              <div class="msg-icon">✨</div>
              <div class="msg-text">
                {content.get('ai_intro', 'Here is the answer:')}
                <div class="rec-card">
                  <div class="rec-trophy">🏆</div>
                  <div class="rec-meta">
                    <div class="rec-name">{content.get('rec_name', 'Top recommendation')}</div>
                    <div class="rec-tag">{content.get('rec_tag', '⭐ AI mentioned')}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>'''
    css = '''
        [data-composition-id="COMP_ID"] .ai-window {
          width: 760px; margin: 8px auto 14px;
          background: rgba(31, 26, 61, 0.92);
          border: 1.5px solid var(--border-glow);
          border-radius: 22px;
          backdrop-filter: blur(14px);
          box-shadow: 0 20px 60px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.08);
          overflow: hidden; will-change: transform, opacity;
        }
        [data-composition-id="COMP_ID"] .window-bar {
          display: flex; align-items: center; gap: 10px; padding: 14px 20px;
          background: rgba(10, 8, 21, 0.6);
          border-bottom: 1px solid rgba(106, 155, 204, 0.15);
        }
        [data-composition-id="COMP_ID"] .dot { width: 14px; height: 14px; border-radius: 50%; }
        [data-composition-id="COMP_ID"] .dot-r { background: #ff5f57; }
        [data-composition-id="COMP_ID"] .dot-y { background: #ffbd2e; }
        [data-composition-id="COMP_ID"] .dot-g { background: #28ca42; }
        [data-composition-id="COMP_ID"] .window-title { margin-left: auto; font-size: 16px; color: var(--ink-mute); font-weight: 600; }
        [data-composition-id="COMP_ID"] .window-body { padding: 22px 24px; display: flex; flex-direction: column; gap: 16px; text-align: left; }
        [data-composition-id="COMP_ID"] .user-msg, [data-composition-id="COMP_ID"] .ai-msg { display: flex; gap: 14px; align-items: flex-start; will-change: transform, opacity; }
        [data-composition-id="COMP_ID"] .msg-icon { width: 38px; height: 38px; border-radius: 50%; background: var(--bg-deep); border: 2px solid var(--accent-cyan); display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; box-shadow: var(--glow-cyan); }
        [data-composition-id="COMP_ID"] .ai-msg .msg-icon { border-color: var(--accent-orange); box-shadow: var(--glow-orange); }
        [data-composition-id="COMP_ID"] .msg-text { flex: 1; font-size: 24px; line-height: 1.4; color: var(--ink); font-weight: 600; }
        [data-composition-id="COMP_ID"] .rec-card { margin-top: 14px; display: flex; align-items: center; gap: 14px; padding: 16px 18px; background: linear-gradient(135deg, rgba(217, 119, 87, 0.18) 0%, rgba(217, 119, 87, 0.05) 100%); border: 1.5px solid var(--accent-orange); border-radius: 14px; will-change: transform, opacity; box-shadow: var(--glow-orange); }
        [data-composition-id="COMP_ID"] .rec-trophy { font-size: 36px; line-height: 1; }
        [data-composition-id="COMP_ID"] .rec-name { font-weight: 800; font-size: 22px; color: var(--accent-orange); }
        [data-composition-id="COMP_ID"] .rec-tag { font-size: 16px; color: var(--ink-mute); margin-top: 2px; }'''
    js = '''tl.from(ROOT + ' .ai-window', { y: -40, opacity: 0, scale: 0.95, duration: 0.55, ease: "back.out(1.5)" }, 1.2);
        tl.from(ROOT + ' .user-msg', { x: -40, opacity: 0, duration: 0.4, ease: "power3.out" }, 1.7);
        tl.from(ROOT + ' .ai-msg', { x: 40, opacity: 0, duration: 0.45, ease: "power3.out" }, 2.2);
        tl.from(ROOT + ' .rec-card', { y: 20, scale: 0.85, opacity: 0, duration: 0.55, ease: "back.out(2)" }, 2.7);
        tl.to(ROOT + ' .rec-card', { scale: 1.04, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 4 }, 3.2);'''
    return body, css, js


def variant_phone_call(content: dict) -> tuple[str, str, str]:
    """Mockup: iPhone call screen with waveform + agent bubble + slot grid."""
    body = f'''
        <div class="phone-frame">
          <div class="phone-notch"></div>
          <div class="phone-screen">
            <div class="call-status">{content.get('call_status', '📞 Cuộc gọi đến')}</div>
            <div class="call-name">{content.get('call_name', 'Caller · 14:32')}</div>
            <div class="waveform">
              <div class="wf-bar"></div><div class="wf-bar"></div><div class="wf-bar"></div>
              <div class="wf-bar"></div><div class="wf-bar"></div><div class="wf-bar"></div>
              <div class="wf-bar"></div><div class="wf-bar"></div><div class="wf-bar"></div>
              <div class="wf-bar"></div><div class="wf-bar"></div><div class="wf-bar"></div>
            </div>
            <div class="agent-bubble">
              <div class="bubble-tag">{content.get('agent_tag', '🤖 AI Agent')}</div>
              <div class="bubble-text">{content.get('agent_text', '"Sample agent response"')}</div>
            </div>
            <div class="slot-grid">
              <div class="slot s-booked">9:00 ✓</div>
              <div class="slot s-booked">10:30 ✓</div>
              <div class="slot s-now">14:00 ●</div>
              <div class="slot s-open">15:30</div>
            </div>
          </div>
        </div>'''
    css = '''
        [data-composition-id="COMP_ID"] .phone-frame {
          width: 380px; height: 560px; margin: 8px auto;
          background: var(--bg-deep); border: 4px solid #2a2545;
          border-radius: 48px; padding: 18px;
          box-shadow: 0 24px 60px rgba(0,0,0,0.7), inset 0 0 30px rgba(0,0,0,0.5);
          position: relative; will-change: transform, opacity;
        }
        [data-composition-id="COMP_ID"] .phone-notch { position: absolute; top: 6px; left: 50%; transform: translateX(-50%); width: 120px; height: 22px; background: #000; border-radius: 0 0 16px 16px; }
        [data-composition-id="COMP_ID"] .phone-screen {
          width: 100%; height: 100%;
          background: linear-gradient(180deg, #1a1432 0%, #0f0a26 100%);
          border-radius: 32px; padding: 28px 20px 20px; box-sizing: border-box;
          display: flex; flex-direction: column; gap: 12px; text-align: center;
        }
        [data-composition-id="COMP_ID"] .call-status { font-weight: 700; font-size: 18px; color: var(--accent-green); letter-spacing: 0.1em; text-transform: uppercase; }
        [data-composition-id="COMP_ID"] .call-name { font-weight: 700; font-size: 22px; color: var(--ink); }
        [data-composition-id="COMP_ID"] .waveform { display: flex; align-items: flex-end; justify-content: center; gap: 4px; height: 40px; margin: 6px 0; }
        [data-composition-id="COMP_ID"] .wf-bar { width: 6px; background: var(--accent-cyan); border-radius: 3px; box-shadow: 0 0 8px rgba(77, 217, 217, 0.6); will-change: transform; }
        [data-composition-id="COMP_ID"] .wf-bar:nth-child(1) { height: 30%; } [data-composition-id="COMP_ID"] .wf-bar:nth-child(2) { height: 60%; } [data-composition-id="COMP_ID"] .wf-bar:nth-child(3) { height: 80%; } [data-composition-id="COMP_ID"] .wf-bar:nth-child(4) { height: 50%; } [data-composition-id="COMP_ID"] .wf-bar:nth-child(5) { height: 90%; } [data-composition-id="COMP_ID"] .wf-bar:nth-child(6) { height: 40%; } [data-composition-id="COMP_ID"] .wf-bar:nth-child(7) { height: 70%; } [data-composition-id="COMP_ID"] .wf-bar:nth-child(8) { height: 95%; } [data-composition-id="COMP_ID"] .wf-bar:nth-child(9) { height: 55%; } [data-composition-id="COMP_ID"] .wf-bar:nth-child(10) { height: 75%; } [data-composition-id="COMP_ID"] .wf-bar:nth-child(11) { height: 35%; } [data-composition-id="COMP_ID"] .wf-bar:nth-child(12) { height: 65%; }
        [data-composition-id="COMP_ID"] .agent-bubble { background: rgba(217, 119, 87, 0.18); border: 1.5px solid var(--accent-orange); border-radius: 14px; padding: 12px 14px; will-change: transform, opacity; }
        [data-composition-id="COMP_ID"] .bubble-tag { font-size: 14px; font-weight: 700; color: var(--accent-orange); margin-bottom: 4px; }
        [data-composition-id="COMP_ID"] .bubble-text { font-size: 18px; font-weight: 600; color: var(--ink); font-style: italic; }
        [data-composition-id="COMP_ID"] .slot-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: auto; }
        [data-composition-id="COMP_ID"] .slot { padding: 10px; border-radius: 10px; font-weight: 700; font-size: 15px; will-change: transform, opacity; }
        [data-composition-id="COMP_ID"] .s-booked { background: rgba(93, 217, 122, 0.18); border: 1px solid var(--accent-green); color: var(--accent-green); }
        [data-composition-id="COMP_ID"] .s-now { background: var(--accent-orange); color: var(--bg-deep); box-shadow: var(--glow-orange); }
        [data-composition-id="COMP_ID"] .s-open { background: rgba(168, 164, 196, 0.1); border: 1px solid var(--ink-mute); color: var(--ink-mute); }'''
    js = '''tl.from(ROOT + ' .phone-frame', { y: 80, opacity: 0, scale: 0.85, duration: 0.6, ease: "back.out(1.6)" }, 1.2);
        tl.fromTo(ROOT + ' .wf-bar', { scaleY: 0.3 }, { scaleY: 1, duration: 0.4, ease: "sine.inOut", stagger: { each: 0.05, repeat: 8, yoyo: true } }, 1.7);
        tl.from(ROOT + ' .agent-bubble', { y: 20, scale: 0.7, opacity: 0, duration: 0.5, ease: "back.out(2)" }, 2.2);
        tl.from(ROOT + ' .slot', { y: 20, opacity: 0, duration: 0.35, ease: "back.out(1.6)", stagger: 0.1 }, 2.6);
        tl.to(ROOT + ' .s-now', { scale: 1.08, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 4 }, 3.1);'''
    return body, css, js


def variant_dashboard(content: dict) -> tuple[str, str, str]:
    """Mockup: Analytics dashboard with stats + creative grid + chart line."""
    creatives = content.get('creatives', ['💪', '🏠', '💆', '🚗', '🍕', '👗', '📱', '💎', '⚽', '📚', '🎮', '🌿'])
    creatives_html = ''.join(f'<div class="creative">{c}</div>' for c in creatives[:12])
    stats = content.get('stats', [
        {'label': 'TOTAL', 'value': '0', 'color': 'orange'},
        {'label': 'CTR', 'value': '4.2%', 'color': 'cyan'},
        {'label': 'CPM', 'value': '$3.80', 'color': 'green'},
    ])
    stats_html = ''.join(f'<div class="stat-cell"><div class="stat-label">{s["label"]}</div><div class="stat-num stat-{s["color"]}">{"<span id=ds-num>" + s["value"] + "</span>" if i == 0 else s["value"]}</div></div>' for i, s in enumerate(stats))

    body = f'''
        <div class="ads-dashboard">
          <div class="dash-header">
            <div class="dash-title">{content.get('dashboard_title', '📊 Dashboard · Live')}</div>
            <div class="dash-status">● Live</div>
          </div>
          <div class="dash-stats">{stats_html}</div>
          <div class="creative-grid">{creatives_html}</div>
          <div class="chart-line">
            <svg viewBox="0 0 400 60" preserveAspectRatio="none">
              <polyline class="chart-path" points="0,55 50,50 100,40 150,38 200,30 250,20 300,18 350,8 400,5" fill="none" stroke="#5dd97a" stroke-width="3" stroke-linecap="round"/>
            </svg>
          </div>
        </div>'''
    css = '''
        [data-composition-id="COMP_ID"] .ads-dashboard { width: 720px; margin: 8px auto 14px; background: rgba(31, 26, 61, 0.92); border: 1.5px solid var(--border-glow); border-radius: 22px; padding: 18px; backdrop-filter: blur(12px); box-shadow: 0 20px 50px rgba(0,0,0,0.5); will-change: transform, opacity; }
        [data-composition-id="COMP_ID"] .dash-header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 12px; border-bottom: 1px solid rgba(106, 155, 204, 0.15); }
        [data-composition-id="COMP_ID"] .dash-title { font-weight: 700; font-size: 20px; color: var(--ink); }
        [data-composition-id="COMP_ID"] .dash-status { font-size: 16px; font-weight: 700; color: var(--accent-green); }
        [data-composition-id="COMP_ID"] .dash-stats { display: flex; gap: 12px; margin: 14px 0; }
        [data-composition-id="COMP_ID"] .stat-cell { flex: 1; padding: 12px; background: rgba(10, 8, 21, 0.6); border-radius: 12px; text-align: left; }
        [data-composition-id="COMP_ID"] .stat-label { font-size: 13px; font-weight: 700; color: var(--ink-mute); letter-spacing: 0.1em; text-transform: uppercase; }
        [data-composition-id="COMP_ID"] .stat-num { font-weight: 800; font-size: 36px; line-height: 1; margin-top: 4px; font-variant-numeric: tabular-nums; }
        [data-composition-id="COMP_ID"] .stat-orange { color: var(--accent-orange); }
        [data-composition-id="COMP_ID"] .stat-cyan { color: var(--accent-cyan); }
        [data-composition-id="COMP_ID"] .stat-green { color: var(--accent-green); }
        [data-composition-id="COMP_ID"] .creative-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px; margin-bottom: 14px; }
        [data-composition-id="COMP_ID"] .creative { aspect-ratio: 1; background: rgba(167, 116, 217, 0.15); border: 1.5px solid var(--accent-purple); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 28px; will-change: transform, opacity; }
        [data-composition-id="COMP_ID"] .chart-line { height: 60px; padding: 0 4px; }
        [data-composition-id="COMP_ID"] .chart-path { stroke-dasharray: 1000; stroke-dashoffset: 1000; }'''
    target = content.get('counter_target', 100)
    js = f'''tl.from(ROOT + ' .ads-dashboard', {{ y: -30, opacity: 0, scale: 0.95, duration: 0.55, ease: "back.out(1.4)" }}, 1.2);
        tl.from(ROOT + ' .creative', {{ scale: 0, opacity: 0, rotation: 180, duration: 0.35, ease: "back.out(2)", stagger: 0.04 }}, 1.8);
        tl.to(ROOT + ' .creative', {{ rotationY: 360, duration: 0.5, stagger: 0.03 }}, 2.5);
        const cnt = {{ v: 0 }};
        tl.to(cnt, {{ v: {target}, duration: 1.6, ease: "power2.out", onUpdate: () => {{ const el = document.querySelector(ROOT + ' #ds-num'); if (el) el.textContent = Math.round(cnt.v); }} }}, 1.9);
        tl.to(ROOT + ' .chart-path', {{ strokeDashoffset: 0, duration: 1.5, ease: "power2.inOut" }}, 2.5);'''
    return body, css, js


def variant_app_card(content: dict) -> tuple[str, str, str]:
    """Mockup: App card with icon + stats badges + optional metaphor row."""
    stats_html = ''.join(f'<span class="badge-stat">{s}</span>' for s in content.get('app_stats', ['⭐ 4.9', '📈 $5M ARR', '👥 1.2K']))
    metaphor_html = ''
    if content.get('metaphor'):
        m = content['metaphor']
        metaphor_html = f'''<div class="meta-stage">
          <div class="meta-cell ms-source"><div class="ms-ico">{m['source']['icon']}</div><div class="ms-label">{m['source']['label']}</div></div>
          <div class="ms-flow">→</div>
          <div class="meta-products">''' + ''.join(f'<div class="meta-cell"><div class="ms-ico">{p["icon"]}</div><div class="ms-label">{p["label"]}</div></div>' for p in m['products']) + '</div></div>'

    body = f'''
        <div class="app-card">
          <div class="app-icon">{content.get('app_icon', '⚡')}</div>
          <div class="app-meta">
            <div class="app-name">{content.get('app_name', 'YourApp')}</div>
            <div class="app-desc">{content.get('app_desc', 'Description')}</div>
            <div class="app-stats">{stats_html}</div>
          </div>
        </div>
        {metaphor_html}
        <div class="build-pill">
          <span class="bp-ico">🚀</span>
          <span>{content.get('build_text', 'Build trên <strong>Lovable</strong>')}</span>
        </div>'''
    css = '''
        [data-composition-id="COMP_ID"] .app-card { width: 720px; margin: 6px auto 14px; background: rgba(31, 26, 61, 0.92); border: 1.5px solid var(--accent-orange); border-radius: 22px; padding: 18px 22px; display: flex; align-items: center; gap: 18px; box-shadow: var(--glow-orange); backdrop-filter: blur(12px); will-change: transform, opacity; }
        [data-composition-id="COMP_ID"] .app-icon { width: 90px; height: 90px; background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%); border-radius: 22px; display: flex; align-items: center; justify-content: center; font-size: 56px; box-shadow: var(--glow-orange), inset 0 -4px 0 rgba(0,0,0,0.2); flex-shrink: 0; }
        [data-composition-id="COMP_ID"] .app-meta { flex: 1; text-align: left; }
        [data-composition-id="COMP_ID"] .app-name { font-weight: 800; font-size: 30px; color: var(--ink); letter-spacing: -0.02em; }
        [data-composition-id="COMP_ID"] .app-desc { font-size: 18px; color: var(--ink-mute); margin-top: 2px; }
        [data-composition-id="COMP_ID"] .app-stats { display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }
        [data-composition-id="COMP_ID"] .badge-stat { font-size: 14px; font-weight: 700; padding: 6px 12px; background: rgba(77, 217, 217, 0.12); border: 1px solid rgba(77, 217, 217, 0.3); color: var(--accent-cyan); border-radius: 999px; }
        [data-composition-id="COMP_ID"] .meta-stage { display: flex; align-items: center; gap: 16px; margin: 12px 0; flex-wrap: wrap; justify-content: center; }
        [data-composition-id="COMP_ID"] .meta-cell { display: flex; flex-direction: column; align-items: center; padding: 14px 16px; min-width: 100px; background: rgba(31, 26, 61, 0.92); border: 2px solid var(--border-glow); border-radius: 16px; will-change: transform, opacity; backdrop-filter: blur(8px); }
        [data-composition-id="COMP_ID"] .ms-source { background: var(--accent-orange); border-color: var(--accent-orange); box-shadow: var(--glow-orange); }
        [data-composition-id="COMP_ID"] .ms-source .ms-label { color: var(--bg-deep); font-weight: 800; }
        [data-composition-id="COMP_ID"] .ms-ico { font-size: 44px; line-height: 1; }
        [data-composition-id="COMP_ID"] .ms-label { font-weight: 700; font-size: 16px; color: var(--ink); margin-top: 6px; }
        [data-composition-id="COMP_ID"] .ms-flow { font-size: 40px; font-weight: 800; color: var(--accent-orange); }
        [data-composition-id="COMP_ID"] .meta-products { display: flex; gap: 10px; }
        [data-composition-id="COMP_ID"] .build-pill { display: inline-flex; align-items: center; gap: 10px; padding: 14px 24px; background: rgba(93, 217, 122, 0.18); border: 2px solid var(--accent-green); color: var(--ink); font-weight: 700; font-size: 22px; border-radius: 999px; box-shadow: var(--glow-green); margin-top: 8px; will-change: transform, opacity; backdrop-filter: blur(10px); }
        [data-composition-id="COMP_ID"] .build-pill strong { color: var(--accent-green); font-weight: 900; }'''
    js = '''tl.from(ROOT + ' .app-card', { y: 30, opacity: 0, scale: 0.92, duration: 0.55, ease: "back.out(1.6)" }, 1.2);
        tl.from(ROOT + ' .app-icon', { rotation: -180, scale: 0, duration: 0.5, ease: "back.out(2.2)" }, 1.4);
        tl.from(ROOT + ' .badge-stat', { y: 10, opacity: 0, duration: 0.35, ease: "power3.out", stagger: 0.1 }, 1.8);
        tl.from(ROOT + ' .ms-source', { scale: 0, opacity: 0, rotation: -90, duration: 0.55, ease: "back.out(2.2)" }, 2.2);
        tl.from(ROOT + ' .meta-products .meta-cell', { y: 30, scale: 0.5, opacity: 0, duration: 0.5, ease: "back.out(2)", stagger: 0.15 }, 2.7);
        tl.to(ROOT + ' .meta-products .ms-ico', { y: -8, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 3, stagger: { each: 0.12, yoyo: true } }, 3.5);
        tl.from(ROOT + ' .build-pill', { y: 30, scale: 0.6, opacity: 0, duration: 0.5, ease: "back.out(2)" }, 3.2);'''
    return body, css, js


def variant_team_grid(content: dict) -> tuple[str, str, str]:
    """Mockup: Headcount board with dot grid morphing 160→40."""
    dots_html = ''
    for row in range(5):
        for col in range(8):
            x = col * 18 + 10; y = row * 18 + 10
            dots_html += f'<div class="team-dot" style="left:{x}%; top:{y}%;"></div>\n'

    body = f'''
        <div class="team-board">
          <div class="board-header">
            <div class="bh-label">{content.get('header_label', 'Headcount')}</div>
            <div class="bh-stat"><span id="team-num">{content.get('from_value', 160)}</span> {content.get('unit', 'nhân viên')}</div>
          </div>
          <div class="team-grid">{dots_html}</div>
        </div>
        <div class="mult-stage">
          <div class="mult-pill">
            <span class="mult-x">×</span>
            <span class="mult-num">{content.get('multiplier', 10)}</span>
          </div>
          <div class="mult-text">{content.get('mult_text', 'Hiệu suất tăng gấp <strong>10 lần</strong>')}</div>
        </div>
        <div class="recap-tag">{content.get('tag', '⚡ Đang xảy ra rồi')}</div>'''
    css = '''
        [data-composition-id="COMP_ID"] .team-board { width: 720px; margin: 6px auto 14px; background: rgba(31, 26, 61, 0.92); border: 1.5px solid var(--border-glow); border-radius: 22px; padding: 18px; backdrop-filter: blur(12px); box-shadow: 0 12px 32px rgba(0,0,0,0.4); will-change: transform, opacity; }
        [data-composition-id="COMP_ID"] .board-header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 14px; border-bottom: 1px solid rgba(106, 155, 204, 0.15); }
        [data-composition-id="COMP_ID"] .bh-label { font-size: 16px; font-weight: 700; color: var(--ink-mute); letter-spacing: 0.1em; text-transform: uppercase; }
        [data-composition-id="COMP_ID"] .bh-stat { font-weight: 800; font-size: 28px; color: var(--accent-orange); font-variant-numeric: tabular-nums; }
        [data-composition-id="COMP_ID"] .team-grid { position: relative; height: 170px; margin-top: 14px; }
        [data-composition-id="COMP_ID"] .team-dot { position: absolute; width: 22px; height: 22px; border-radius: 50%; background: var(--accent-cyan); box-shadow: 0 0 8px rgba(77, 217, 217, 0.5); will-change: transform, opacity; }
        [data-composition-id="COMP_ID"] .mult-stage { display: flex; align-items: center; gap: 18px; margin: 8px 0; }
        [data-composition-id="COMP_ID"] .mult-pill { display: inline-flex; align-items: baseline; gap: 4px; padding: 16px 28px; background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%); color: var(--bg-deep); border-radius: 22px; box-shadow: var(--glow-orange); }
        [data-composition-id="COMP_ID"] .mult-x { font-size: 36px; font-weight: 800; }
        [data-composition-id="COMP_ID"] .mult-num { font-size: 80px; line-height: 0.85; font-weight: 900; letter-spacing: -0.04em; font-variant-numeric: tabular-nums; }
        [data-composition-id="COMP_ID"] .mult-text { font-size: 22px; font-weight: 600; color: var(--ink); text-align: left; line-height: 1.3; }
        [data-composition-id="COMP_ID"] .mult-text strong { color: var(--accent-orange); font-weight: 800; }
        [data-composition-id="COMP_ID"] .recap-tag { margin-top: 14px; font-style: italic; font-weight: 600; font-size: 24px; color: var(--accent-cyan); will-change: transform, opacity; }'''
    fr = content.get('from_value', 160); to = content.get('to_value', 40)
    js = f'''tl.from(ROOT + ' .team-board', {{ y: 30, opacity: 0, scale: 0.95, duration: 0.55, ease: "back.out(1.5)" }}, 1.0);
        tl.from(ROOT + ' .team-dot', {{ scale: 0, opacity: 0, duration: 0.3, ease: "back.out(1.6)", stagger: {{ each: 0.012, from: "random" }} }}, 1.4);
        const upObj = {{ v: 0 }};
        tl.to(upObj, {{ v: {fr}, duration: 1.0, ease: "power2.out", onUpdate: () => {{ const el = document.querySelector(ROOT + ' #team-num'); if (el) el.textContent = Math.round(upObj.v); }} }}, 1.4);
        const dnObj = {{ v: {fr} }};
        tl.to(dnObj, {{ v: {to}, duration: 1.6, ease: "power3.inOut", onUpdate: () => {{ const el = document.querySelector(ROOT + ' #team-num'); if (el) el.textContent = Math.round(dnObj.v); }} }}, 2.6);
        tl.to(ROOT + ' .team-dot:nth-child(n+11)', {{ backgroundColor: 'rgba(168, 164, 196, 0.2)', boxShadow: 'none', scale: 0.6, duration: 1.4, ease: "power2.inOut", stagger: 0.025 }}, 2.6);
        tl.from(ROOT + ' .mult-pill', {{ scale: 0.4, opacity: 0, rotation: -10, duration: 0.6, ease: "back.out(2.2)" }}, 4.2);
        tl.to(ROOT + ' .mult-pill', {{ scale: 1.06, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 3 }}, 4.85);
        tl.from(ROOT + ' .mult-text', {{ x: -30, opacity: 0, duration: 0.45, ease: "power3.out" }}, 4.5);
        tl.from(ROOT + ' .recap-tag', {{ y: 14, opacity: 0, duration: 0.5 }}, 5.0);'''
    return body, css, js


def variant_comment_box(content: dict) -> tuple[str, str, str]:
    """Mockup: Comment input box + 2 gift cards stack + CTA pill."""
    gifts_html = ''
    for g in content.get('gifts', [{'thumb': '🎬', 'tag': 'GIFT', 'title': 'Title'}, {'thumb': '🎬', 'tag': 'GIFT 2', 'title': 'Title 2'}]):
        gifts_html += f'''<div class="gift-card">
          <div class="gc-thumb">{g['thumb']}</div>
          <div class="gc-meta">
            <div class="gc-tag">{g['tag']}</div>
            <div class="gc-title">{g['title']}</div>
          </div>
          <div class="gc-badge">{g.get('badge', 'FREE')}</div>
        </div>'''

    body = f'''
        <div class="comment-box">
          <div class="cb-avatar">{content.get('avatar_letter', 'B')}</div>
          <div class="cb-input">
            <span class="cb-text">{content.get('keyword', 'KEYWORD')}</span><span class="cb-cursor">|</span>
          </div>
          <div class="cb-send">▶</div>
        </div>
        <div class="gift-stack">{gifts_html}</div>
        <div class="hand-cta">{content.get('cta_text', '👇 Comment ngay 👇')}</div>'''
    css = '''
        [data-composition-id="COMP_ID"] .comment-box { width: 720px; margin: 6px auto 14px; display: flex; align-items: center; gap: 12px; padding: 18px; background: rgba(31, 26, 61, 0.92); border: 2px solid var(--accent-orange); border-radius: 18px; box-shadow: var(--glow-orange); backdrop-filter: blur(12px); will-change: transform, opacity; }
        [data-composition-id="COMP_ID"] .cb-avatar { width: 48px; height: 48px; border-radius: 50%; background: var(--accent-cyan); color: var(--bg-deep); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 22px; flex-shrink: 0; }
        [data-composition-id="COMP_ID"] .cb-input { flex: 1; text-align: left; padding: 12px 16px; background: rgba(10, 8, 21, 0.6); border-radius: 999px; font-size: 26px; font-weight: 700; color: var(--ink); }
        [data-composition-id="COMP_ID"] .cb-text { color: var(--accent-orange); background: rgba(217, 119, 87, 0.15); padding: 2px 10px; border-radius: 6px; }
        [data-composition-id="COMP_ID"] .cb-cursor { color: var(--accent-orange); animation: caret 0.6s steps(1) infinite; }
        @keyframes caret { 50% { opacity: 0; } }
        [data-composition-id="COMP_ID"] .cb-send { width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%); color: var(--bg-deep); display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 800; box-shadow: var(--glow-orange); flex-shrink: 0; }
        [data-composition-id="COMP_ID"] .gift-stack { display: flex; flex-direction: column; gap: 12px; width: 720px; }
        [data-composition-id="COMP_ID"] .gift-card { display: flex; align-items: center; gap: 14px; padding: 16px 18px; background: rgba(31, 26, 61, 0.92); border: 1.5px solid var(--border-glow); border-radius: 18px; backdrop-filter: blur(10px); box-shadow: 0 12px 28px rgba(0,0,0,0.4); will-change: transform, opacity; }
        [data-composition-id="COMP_ID"] .gc-thumb { width: 70px; height: 70px; background: linear-gradient(135deg, var(--accent-purple) 0%, #c498e0 100%); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 38px; box-shadow: var(--glow-purple); flex-shrink: 0; }
        [data-composition-id="COMP_ID"] .gc-meta { flex: 1; text-align: left; }
        [data-composition-id="COMP_ID"] .gc-tag { font-size: 13px; font-weight: 800; color: var(--accent-cyan); letter-spacing: 0.12em; text-transform: uppercase; }
        [data-composition-id="COMP_ID"] .gc-title { font-size: 24px; font-weight: 800; color: var(--ink); margin-top: 4px; letter-spacing: -0.01em; }
        [data-composition-id="COMP_ID"] .gc-badge { padding: 6px 12px; background: var(--accent-green); color: var(--bg-deep); border-radius: 999px; font-weight: 800; font-size: 14px; box-shadow: var(--glow-green); flex-shrink: 0; }
        [data-composition-id="COMP_ID"] .hand-cta { margin-top: 14px; padding: 16px 32px; background: linear-gradient(135deg, var(--accent-orange) 0%, #f4a384 100%); color: var(--bg-deep); font-weight: 800; font-size: 26px; border-radius: 999px; box-shadow: var(--glow-orange); will-change: transform, opacity; }'''
    js = '''tl.from(ROOT + ' .comment-box', { y: -30, opacity: 0, scale: 0.92, duration: 0.5, ease: "back.out(1.6)" }, 1.0);
        tl.from(ROOT + ' .cb-text', { scale: 0, opacity: 0, duration: 0.4, ease: "back.out(2)" }, 1.4);
        tl.from(ROOT + ' .gift-card', { y: 40, opacity: 0, scale: 0.9, duration: 0.5, ease: "back.out(1.6)", stagger: 0.18 }, 1.6);
        tl.from(ROOT + ' .gc-badge', { scale: 0, opacity: 0, rotation: -30, duration: 0.45, ease: "back.out(2.4)", stagger: 0.18 }, 2.0);
        tl.from(ROOT + ' .hand-cta', { y: 30, scale: 0.5, opacity: 0, duration: 0.5, ease: "back.out(2.2)" }, 2.6);
        tl.to(ROOT + ' .hand-cta', { scale: 1.06, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 4 }, 3.2);'''
    return body, css, js


VARIANT_MAP = {
    'post-stack': variant_post_stack,
    'ai-window': variant_ai_window,
    'phone-call': variant_phone_call,
    'dashboard': variant_dashboard,
    'app-card': variant_app_card,
    'team-grid': variant_team_grid,
    'comment-box': variant_comment_box,
}


def render_scene(comp_id: str, scene: dict) -> str:
    """Render one sub-comp from scene data."""
    variant_name = scene.get('mockup_variant', 'app-card')
    variant_fn = VARIANT_MAP.get(variant_name)
    if not variant_fn:
        raise ValueError(f"Unknown mockup_variant: {variant_name}. Available: {list(VARIANT_MAP)}")

    content = scene.get('content', {})
    body, css, js = variant_fn(content)

    # Replace COMP_ID placeholder
    css = css.replace('COMP_ID', comp_id)

    # Build header pill + title
    pill_label = scene.get('kicker', 'Scene')
    pill_num = scene.get('num', '★')
    title_str = scene.get('heading', 'Title')
    accent_idx = scene.get('accent_words', [])
    title_html = title_words(title_str, accent_idx)

    # Optional floating badges
    badges = scene.get('badges', [])
    fb_html, fb_css, fb_js = ('', '', '')
    if badges:
        fb_html, fb_css, fb_js = floating_badges(badges)
        fb_css = fb_css.replace('COMP_ID', comp_id)

    full_body = f'''
        <div class="topic-pill"><span class="num">{pill_num}</span>{pill_label}</div>
        <h1 class="brand-title">
          {title_html}
        </h1>
        {body}
        {fb_html}
    '''
    full_css = css + '\n' + fb_css
    full_js = js + '\n        ' + fb_js

    return shell(comp_id, full_body, full_css, full_js)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True, help='Compositions directory to write into')
    p.add_argument('--scenes', required=True, help='scenes.json with mockup_variant + content per scene')
    p.add_argument('--captions', help='caption-groups.json (optional, for captions sub-comp injection)')
    p.add_argument('--captions-template', help='Path to captions.html.template (optional)')
    args = p.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    scenes_data = json.loads(Path(args.scenes).read_text())
    scenes = scenes_data['scenes']

    for sc in scenes:
        kind = sc.get('kind', 'lesson')
        if kind == 'lesson':
            comp_id = f"fs-lesson-{sc.get('num', 1)}"
            fname = f"{comp_id}.html"
        elif kind == 'recap':
            comp_id = 'recap-card'
            fname = 'recap-card.html'
        elif kind == 'cta':
            comp_id = 'fs-cta'
            fname = 'fs-cta.html'
        else:
            continue

        html = render_scene(comp_id, sc)
        (out / fname).write_text(html)
        print(f'  → {fname} (variant: {sc.get("mockup_variant")})')

    print(f'\nGenerated {len([s for s in scenes if s.get("kind") in ("lesson","recap","cta")])} infographic-style sub-comps in {out}')


if __name__ == '__main__':
    main()
