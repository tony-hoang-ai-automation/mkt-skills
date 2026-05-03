#!/usr/bin/env python3
"""Generate root index.html with split-screen + full-face breath layout baked in.

Reads scenes.json (with brollEnd + hasBreath fields) and emits a complete root
index.html that includes:
- Source video (full → bottom half during b-roll)
- 6 SFX with HF native scheduling
- Header pill + brand mark always-on
- Split-mount divs for each scene (lesson/recap/cta) with track-index 40-47
- Captions mount LAST with track-index 60 + z-index 100
- Split divider line at 50%
- GSAP timeline with goSplit() / goFull() helpers cycling through scenes

Usage:
  python3 generate_root_index.py \
    --output workspace/content/YYYY-MM-DD/<slug>/index.html \
    --scenes scenes.json \
    --total-duration 108.92 \
    --header-label "6 AI BUSINESS 2026" \
    --footer-handle "@tranvanhoang.com"

scenes.json schema (minimum):
{
  "total_duration": 108.92,
  "scenes": [
    {
      "kind": "lesson", "num": 1, "start": 12.71, "end": 26.40,
      "brollEnd": 24.90,         # When b-roll unmounts (1.5s before next scene)
      "hasBreath": true          # true → full-face breath at brollEnd
    },
    { "kind": "recap", "start": 92.59, "end": 103.20, "brollEnd": 99.00, "hasBreath": true },
    { "kind": "cta",   "start": 103.40, "end": 108.92, "brollEnd": 105.40, "hasBreath": true }
  ]
}
"""
import argparse
import json
import sys
from pathlib import Path


def render(scenes, total_duration, header_label, footer_handle):
    # Build mount divs
    mounts = []
    track = 40
    for sc in scenes:
        kind = sc.get("kind", "lesson")
        if kind == "lesson":
            comp_id = f"fs-lesson-{sc.get('num', 1)}"
            src = f"compositions/fs-lesson-{sc.get('num', 1)}.html"
        elif kind == "recap":
            comp_id = "recap-card"
            src = "compositions/recap-card.html"
        elif kind == "cta":
            comp_id = "fs-cta"
            src = "compositions/fs-cta.html"
        else:
            continue
        # Use brollEnd to compute shortened data-duration
        broll_end = sc.get("brollEnd", sc["end"])
        duration = broll_end - sc["start"]
        mounts.append(
            f'    <div class="clip split-mount" '
            f'data-composition-src="{src}" '
            f'data-start="{sc["start"]:.2f}" '
            f'data-duration="{duration:.2f}" '
            f'data-composition-id="{comp_id}" '
            f'data-track-index="{track}"></div>'
        )
        track += 1

    mounts_html = "\n".join(mounts)

    # Build SCENES JS array for animation timeline
    scenes_js = []
    for sc in scenes:
        kind = sc.get("kind", "lesson")
        if kind == "lesson":
            comp_id = f"fs-lesson-{sc.get('num', 1)}"
        elif kind == "recap":
            comp_id = "recap-card"
        elif kind == "cta":
            comp_id = "fs-cta"
        else:
            continue
        broll_end = sc.get("brollEnd", sc["end"])
        has_breath = "true" if sc.get("hasBreath", False) else "false"
        scenes_js.append(
            f'        {{ id: "{comp_id}", start: {sc["start"]:.2f}, '
            f'brollEnd: {broll_end:.2f}, hasBreath: {has_breath} }}'
        )
    scenes_js_str = ",\n".join(scenes_js)

    # First scene start for divider pulse start time
    first_scene_start = scenes[0]["start"] if scenes else 12.0

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <title>{header_label} — Hoàng AI</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg-deep: #0a0815;
      --brand-bg: #faf9f5;
      --brand-ink: #141413;
      --brand-accent: #d97757;
    }}
    html, body {{
      margin: 0; padding: 0;
      background: var(--brand-ink);
      font-family: 'Be Vietnam Pro', sans-serif;
    }}
    [data-composition-id="root"] {{
      position: relative; width: 1080px; height: 1920px;
      overflow: hidden; background: #000;
    }}
    /* SOURCE VIDEO */
    #v-source {{
      position: absolute; top: 0; left: 0;
      width: 100%; height: 100%;
      object-fit: cover;
      object-position: center 25%;
      z-index: 1;
      will-change: transform, height, top, object-position;
    }}
    /* SPLIT MOUNT */
    .split-mount {{
      position: absolute !important;
      top: 0 !important; left: 0 !important;
      width: 1080px !important; height: 960px !important;
      overflow: hidden !important;
      background: var(--bg-deep);
      z-index: 40;
    }}
    .split-mount > [data-composition-id] {{
      transform: scale(0.5);
      transform-origin: top center;
      width: 1080px !important; height: 1920px !important;
      position: absolute !important;
      left: 50%; margin-left: -540px;
    }}
    /* DIVIDER */
    #split-divider {{
      position: absolute; top: 50%; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, transparent 0%, rgba(217,119,87,0.8) 20%, rgba(77,217,217,0.9) 50%, rgba(217,119,87,0.8) 80%, transparent 100%);
      box-shadow: 0 0 12px rgba(217,119,87,0.5);
      z-index: 50; opacity: 0;
      will-change: opacity, transform;
    }}
    /* HEADER PILL */
    .header-pill {{
      position: absolute; top: 64px; left: 50%;
      transform: translateX(-50%);
      z-index: 30;
      display: flex; align-items: center; gap: 14px;
      padding: 16px 30px;
      background: rgba(20,20,19,0.78);
      border: 1.5px solid rgba(250,249,245,0.18);
      border-radius: 999px;
      backdrop-filter: blur(8px);
    }}
    .header-pill .dot {{
      width: 12px; height: 12px; border-radius: 50%;
      background: var(--brand-accent);
      box-shadow: 0 0 0 4px rgba(217,119,87,0.18);
    }}
    .header-pill .label {{
      font-weight: 600; font-size: 30px;
      letter-spacing: 0.04em;
      color: var(--brand-bg);
      text-transform: uppercase;
    }}
    /* FOOTER */
    .brand-mark {{
      position: absolute; left: 50%; bottom: 70px;
      transform: translateX(-50%);
      z-index: 45;
      font-weight: 600; font-size: 30px;
      letter-spacing: 0.04em;
      color: var(--brand-bg);
      opacity: 0.92;
      padding: 10px 22px;
      background: rgba(20,20,19,0.55);
      border-radius: 999px;
      backdrop-filter: blur(6px);
    }}
    .brand-mark .at {{ color: var(--brand-accent); margin-right: 2px; }}
  </style>
</head>
<body>
  <div data-composition-id="root" data-start="0" data-width="1080" data-height="1920">
    <video id="v-source" data-start="0" data-duration="{total_duration:.2f}"
           data-track-index="0" src="source.mp4" muted playsinline></video>
    <audio id="a-source" data-start="0" data-duration="{total_duration:.2f}"
           data-track-index="1" data-volume="1" src="source.mp4"></audio>

    <!-- 6 SFX (timing customize per video) -->
    <audio id="sfx-hook"  data-start="0"      data-duration="0.6" data-track-index="20" data-volume="0.32" src="sfx/camera-flash.mp3"></audio>

    <div id="split-divider"></div>

    <div id="brand-mark" class="clip brand-mark"
         data-start="0" data-duration="{total_duration:.2f}" data-track-index="2">
      <span class="at">@</span>{footer_handle.lstrip('@')}
    </div>

    <div id="header-pill" class="clip header-pill"
         data-start="0" data-duration="{total_duration:.2f}" data-track-index="3">
      <div class="dot"></div>
      <div class="label">{header_label}</div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});

      // --- Header pill entrance ---
      tl.from("#header-pill", {{ y: -40, opacity: 0, duration: 0.6, ease: "power3.out" }}, 0.15);
      tl.from("#brand-mark", {{ opacity: 0, duration: 0.7, ease: "power2.out" }}, 0.6);

      // --- SPLIT-SCREEN ↔ FULL-FACE TRANSITIONS ---
      const SCENES = [
{scenes_js_str}
      ];
      const TRANSITION_DUR = 0.45;
      const PRE_SHRINK = 0.3;

      function goSplit(t) {{
        tl.to("#v-source", {{
          height: "50%", top: "50%",
          objectPosition: "center 15%",
          duration: TRANSITION_DUR, ease: "power2.inOut",
        }}, t);
        tl.to("#split-divider", {{ opacity: 1, duration: 0.35 }}, t + 0.1);
        tl.to('[data-composition-id="captions"] .caption-stage', {{
          bottom: 920, duration: TRANSITION_DUR, ease: "power2.inOut",
        }}, t);
      }}

      function goFull(t) {{
        tl.to("#v-source", {{
          height: "100%", top: "0%",
          objectPosition: "center 25%",
          duration: TRANSITION_DUR, ease: "power2.inOut",
        }}, t);
        tl.to("#split-divider", {{ opacity: 0, duration: 0.3 }}, t);
        tl.to('[data-composition-id="captions"] .caption-stage', {{
          bottom: 160, duration: TRANSITION_DUR, ease: "power2.inOut",
        }}, t);
      }}

      tl.set('[data-composition-id="captions"] .caption-stage', {{ bottom: 160 }}, 0);

      SCENES.forEach((sc) => {{
        goSplit(sc.start - PRE_SHRINK);
        if (sc.hasBreath) {{
          goFull(sc.brollEnd);
        }}
      }});

      // Divider pulse loop
      tl.to("#split-divider", {{
        scaleY: 1.4, duration: 1.2, ease: "sine.inOut",
        yoyo: true, repeat: 60, transformOrigin: "center center",
      }}, {first_scene_start - 0.2:.2f});

      window.__timelines["root"] = tl;
    </script>

    <!-- ============ SCENE MOUNTS (split-screen, track 40-47) ============ -->
{mounts_html}

    <!-- ============ CAPTIONS LAST (track 60 + z-index 100) ============ -->
    <div class="clip captions-mount"
         data-composition-src="compositions/captions.html"
         data-start="0" data-duration="{total_duration:.2f}"
         data-composition-id="captions"
         data-track-index="60"
         style="z-index: 100;"></div>
  </div>
</body>
</html>
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    p.add_argument("--scenes", required=True)
    p.add_argument("--total-duration", type=float, required=True)
    p.add_argument("--header-label", default="VIDEO")
    p.add_argument("--footer-handle", default="@tranvanhoang.com")
    args = p.parse_args()

    scenes_data = json.loads(Path(args.scenes).read_text())
    scenes = scenes_data["scenes"]

    html = render(scenes, args.total_duration, args.header_label, args.footer_handle)
    Path(args.output).write_text(html)
    print(f"Generated → {args.output}")
    print(f"  Scenes: {len(scenes)}  ·  Duration: {args.total_duration}s")
    print(f"  Split-screen baked in · captions z-100 · breath transitions")


if __name__ == "__main__":
    main()
