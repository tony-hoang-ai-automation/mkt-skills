#!/usr/bin/env python3
"""Scaffold a HyperFrames project from templates + scenes.json.

Reads:
- assets/templates/*.html.template
- scenes.json (with N lessons + optional recap + cta)
- caption-groups.json
- source.mp4 (already in output dir)

Writes:
- index.html (root composition with timeline)
- compositions/captions.html
- compositions/fs-lesson-{1..N}.html (cycling variants 1/2/3)
- compositions/recap-card.html (if scene of kind=recap)
- compositions/fs-cta.html (if scene of kind=cta)
- broll-map.json (if --broll-map provided)

Usage:
  python3 scaffold_project.py \
    --output workspace/content/YYYY-MM-DD/<slug>/ \
    --slug <slug> \
    --footer-handle "@tranvanhoang.com" \
    --header-label "<topic-summary>"
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL_DIR / 'assets' / 'templates'

# Reference SFX library
SFX_SRC = Path('/Users/tonyhoang/Documents/GitHub/hoang-ai-marketing/workspace/assets/reels/sfx')
SFX_FILES = [
    'camera-flash.mp3',
    'búng tay.mp3',
    'Whoosh sound effect (1).mp3',
    'Laser.mp3',
    'ting.mp3',
    'Discord Notification - Sound Effect.mp3',
]


def words_with_accent(title, accent_indices=None):
    """Wrap title words in <span class='word'>; mark some as accent."""
    accent_indices = accent_indices or []
    words = title.split()
    out = []
    for i, w in enumerate(words):
        cls = 'word accent' if i in accent_indices else 'word'
        out.append(f'<span class="{cls}">{w}</span>')
    return '\n        '.join(out)


def render_lesson(template_path, scene, num_str):
    """Substitute lesson template content for one scene."""
    html = template_path.read_text()
    # Replace eyebrow
    html = re.sub(
        r'<div class="fs-eyebrow">[^<]*</div>',
        f'<div class="fs-eyebrow">{scene["kicker"]}</div>',
        html, count=1
    )
    # Replace fs-num content (the displayed number)
    html = re.sub(
        r'<div class="fs-num">[^<]*</div>',
        f'<div class="fs-num">{num_str}</div>',
        html, count=1
    )
    # Replace fs-title — find the first <div class="fs-title"> ... </div>
    title_words = words_with_accent(scene['heading'])
    html = re.sub(
        r'<div class="fs-title">[\s\S]*?</div>',
        f'<div class="fs-title">\n        {title_words}\n      </div>',
        html, count=1
    )
    # Replace fs-sub
    sub = scene.get('sub', '')
    html = re.sub(
        r'<div class="fs-sub">[^<]*</div>',
        f'<div class="fs-sub">{sub}</div>',
        html, count=1
    )
    return html


def render_recap(template_path, scene):
    html = template_path.read_text()
    html = re.sub(
        r'<div class="fs-eyebrow">[^<]*</div>',
        f'<div class="fs-eyebrow">{scene.get("kicker","Recap")}</div>',
        html, count=1
    )
    # Many recap templates have 3 small cards or text — for our case, replace big title only
    html = re.sub(
        r'<div class="recap-title">[^<]*</div>',
        f'<div class="recap-title">{scene["heading"]}</div>',
        html, count=1
    )
    # Fallback: replace any fs-title
    html = re.sub(
        r'<div class="fs-title">[\s\S]*?</div>',
        f'<div class="fs-title">\n        {words_with_accent(scene["heading"])}\n      </div>',
        html, count=1
    )
    return html


def render_cta(template_path, scene, footer_handle):
    html = template_path.read_text()
    html = re.sub(
        r'<div class="fs-eyebrow">[^<]*</div>',
        f'<div class="fs-eyebrow">{scene.get("kicker","Comment để nhận")}</div>',
        html, count=1
    )
    html = re.sub(
        r'<div class="fs-title">[\s\S]*?</div>',
        f'<div class="fs-title">\n        {words_with_accent(scene["heading"])}\n      </div>',
        html, count=1
    )
    html = re.sub(
        r'<div class="fs-sub">[^<]*</div>',
        f'<div class="fs-sub">{scene.get("sub","")}</div>',
        html, count=1
    )
    return html


def render_captions_template(template_path):
    """Captions sub-comp — the inject_captions.py script will fill the array later."""
    return template_path.read_text()


def render_index(template_path, scenes, total_duration, header_label, footer_handle, slug, lesson_filenames):
    """Generate root index.html with timeline mounting all scenes."""
    html = template_path.read_text()

    # Replace title
    html = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{header_label} — Hoàng AI</title>',
        html, count=1
    )
    # Replace header pill label
    html = re.sub(
        r'(<div class="header-pill"[^>]*>)([\s\S]*?)(</div>\s*<!-- end header-pill)',
        lambda m: m.group(1) + (
            '\n      <div class="dot"></div>\n'
            f'      <div class="label">{header_label}</div>\n    '
        ) + m.group(3),
        html
    )
    # Simpler: just replace the .label text
    html = re.sub(
        r'<div class="label">[^<]*</div>',
        f'<div class="label">{header_label}</div>',
        html, count=1
    )
    # Replace footer handle
    html = re.sub(
        r'<div class="footer-handle">[^<]*</div>',
        f'<div class="footer-handle">{footer_handle}</div>',
        html, count=1
    )

    # Build the list of scene mount divs (insertion before <!-- SCENES_END -->)
    scene_mounts = []
    for i, sc in enumerate(scenes):
        if sc['kind'] == 'lesson':
            comp_id = f"fs-lesson-{sc['num']}"
            comp_src = f"compositions/{lesson_filenames[i]}"
            duration = sc['end'] - sc['start']
            scene_mounts.append(
                f'    <div data-composition-src="{comp_src}" '
                f'data-start="{sc["start"]:.2f}" '
                f'data-duration="{duration:.2f}" '
                f'data-composition-id="{comp_id}"></div>'
            )
        elif sc['kind'] == 'recap':
            duration = sc['end'] - sc['start']
            scene_mounts.append(
                f'    <div data-composition-src="compositions/recap-card.html" '
                f'data-start="{sc["start"]:.2f}" '
                f'data-duration="{duration:.2f}" '
                f'data-composition-id="recap-card"></div>'
            )
        elif sc['kind'] == 'cta':
            duration = sc['end'] - sc['start']
            scene_mounts.append(
                f'    <div data-composition-src="compositions/fs-cta.html" '
                f'data-start="{sc["start"]:.2f}" '
                f'data-duration="{duration:.2f}" '
                f'data-composition-id="fs-cta"></div>'
            )

    # Captions mount (always-on)
    captions_mount = (
        '    <div data-composition-src="compositions/captions.html" '
        f'data-start="0" data-duration="{total_duration:.2f}" '
        'data-composition-id="captions"></div>'
    )

    scene_block = '\n'.join([captions_mount] + scene_mounts)

    # Inject before </div> closing root composition
    # Find last </div> before </body>
    html = re.sub(
        r'(<div data-composition-src="compositions/captions\.html"[\s\S]*?</div>)',
        scene_block,
        html
    )
    # If no existing captions mount, insert before the </script> </div> </body> block
    if scene_block not in html:
        html = html.replace(
            '    </script>\n  </div>\n</body>',
            f'{scene_block}\n    </script>\n  </div>\n</body>'
        )

    # Compute SOURCE_PUNCHES (1 entry per lesson start)
    punches = []
    punches.append({'t': 0.0, 'scale': 1.10, 'dur': 0.6})  # entry
    for sc in scenes:
        if sc['kind'] == 'lesson':
            t = max(0.0, sc['end'] - 0.05)
            punches.append({'t': round(t, 2), 'scale': 1.10, 'dur': 0.55})
    # Limit to 5 punches max (avoid over-zoom)
    punches = punches[:5]

    punch_js = ',\n        '.join([
        f'{{ t: {p["t"]:.2f}, scale: {p["scale"]:.2f}, dur: {p["dur"]:.2f} }}'
        for p in punches
    ])

    html = re.sub(
        r'const SOURCE_PUNCHES = \[[\s\S]*?\];',
        f'const SOURCE_PUNCHES = [\n        {punch_js}\n      ];',
        html
    )

    # Compute AMBIENT_DRIFTS — drift during each scene (from start+0.5 to end-0.3)
    drifts = []
    # Intro drift before first lesson
    first_lesson = next((s for s in scenes if s['kind'] == 'lesson'), None)
    if first_lesson and first_lesson['start'] > 1.0:
        drifts.append({'start': 0.7, 'end': first_lesson['start'] - 0.3, 'from': 1.0, 'to': 1.03})

    drift_js = ',\n        '.join([
        f'{{ start: {d["start"]:.2f}, end: {d["end"]:.2f}, from: {d["from"]:.2f}, to: {d["to"]:.2f} }}'
        for d in drifts
    ])
    if drift_js:
        html = re.sub(
            r'const AMBIENT_DRIFTS = \[[\s\S]*?\];',
            f'const AMBIENT_DRIFTS = [\n        {drift_js}\n      ];',
            html
        )

    # Compute SFX timing — 6 SFX max
    sfx_lessons = [sc for sc in scenes if sc['kind'] == 'lesson']
    recap = next((sc for sc in scenes if sc['kind'] == 'recap'), None)
    cta = next((sc for sc in scenes if sc['kind'] == 'cta'), None)

    sfx_entries = []
    sfx_entries.append({'time': 0.0, 'file': 'camera-flash.mp3', 'volume': 0.32})
    # First lesson — snap
    if len(sfx_lessons) >= 1:
        sfx_entries.append({'time': max(0.0, sfx_lessons[0]['start'] - 0.05), 'file': 'búng tay.mp3', 'volume': 0.30})
    # 3rd lesson — whoosh
    if len(sfx_lessons) >= 3:
        sfx_entries.append({'time': max(0.0, sfx_lessons[2]['start'] - 0.05), 'file': 'Whoosh sound effect (1).mp3', 'volume': 0.22})
    # 5th lesson — laser
    if len(sfx_lessons) >= 5:
        sfx_entries.append({'time': max(0.0, sfx_lessons[4]['start'] - 0.05), 'file': 'Laser.mp3', 'volume': 0.28})
    # Recap — ting
    if recap:
        sfx_entries.append({'time': max(0.0, recap['start'] - 0.05), 'file': 'ting.mp3', 'volume': 0.20})
    # CTA — discord
    if cta:
        sfx_entries.append({'time': cta['start'], 'file': 'Discord Notification - Sound Effect.mp3', 'volume': 0.28})

    # Save sfx mapping next to project (for reference) — root composition will use <audio> elements
    return html, sfx_entries


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True)
    p.add_argument('--slug', required=True)
    p.add_argument('--footer-handle', default='@tranvanhoang.com')
    p.add_argument('--header-label', default='Hoàng AI')
    p.add_argument('--scenes', default=None, help='Path to scenes.json (default: <output>/scenes.json)')
    p.add_argument('--captions', default=None, help='Path to caption-groups.json (default: <output>/caption-groups.json)')
    p.add_argument('--broll-map', default=None)
    args = p.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'compositions').mkdir(exist_ok=True)
    (out / 'sfx').mkdir(exist_ok=True)

    scenes_path = Path(args.scenes) if args.scenes else out / 'scenes.json'
    captions_path = Path(args.captions) if args.captions else out / 'caption-groups.json'

    scenes_data = json.loads(scenes_path.read_text())
    scenes = scenes_data['scenes']
    total_duration = scenes_data.get('total_duration') or scenes_data.get('duration') or scenes[-1]['end']

    # Render lesson sub-comps with cycling variants
    lesson_filenames = []
    lesson_idx = 0
    for sc in scenes:
        if sc['kind'] == 'lesson':
            variant = sc.get('variant') or ((lesson_idx % 3) + 1)
            tmpl = TEMPLATES / f'fs-lesson-{variant}.html.template'
            html = render_lesson(tmpl, sc, num_str=str(sc['num']).zfill(2))
            # Each lesson gets its own filename to allow 6 lessons reusing 3 templates
            fname = f'fs-lesson-{sc["num"]}.html'
            (out / 'compositions' / fname).write_text(html)
            lesson_filenames.append(fname)
            lesson_idx += 1
        else:
            lesson_filenames.append(None)

    # Recap
    recap_scene = next((sc for sc in scenes if sc['kind'] == 'recap'), None)
    if recap_scene:
        html = render_recap(TEMPLATES / 'recap-card.html.template', recap_scene)
        (out / 'compositions' / 'recap-card.html').write_text(html)

    # CTA
    cta_scene = next((sc for sc in scenes if sc['kind'] == 'cta'), None)
    if cta_scene:
        html = render_cta(TEMPLATES / 'fs-cta.html.template', cta_scene, args.footer_handle)
        (out / 'compositions' / 'fs-cta.html').write_text(html)

    # Captions sub-comp
    captions_html = render_captions_template(TEMPLATES / 'captions.html.template')
    (out / 'compositions' / 'captions.html').write_text(captions_html)

    # Inject caption groups
    import subprocess
    inject_script = SKILL_DIR / 'scripts' / 'inject_captions.py'
    subprocess.run([
        'python3', str(inject_script),
        str(out / 'compositions' / 'captions.html'),
        str(captions_path),
    ], check=True)

    # Render root index
    index_html, sfx_entries = render_index(
        TEMPLATES / 'index.html.template',
        scenes, total_duration,
        args.header_label, args.footer_handle, args.slug,
        lesson_filenames,
    )

    # Inject SFX <audio> elements + scheduling
    sfx_audio_html = '\n'.join([
        f'    <audio id="sfx-{i}" src="sfx/{e["file"]}" preload="auto"></audio>'
        for i, e in enumerate(sfx_entries)
    ])
    sfx_js = ',\n        '.join([
        f'{{ t: {e["time"]:.2f}, id: "#sfx-{i}", vol: {e["volume"]:.2f} }}'
        for i, e in enumerate(sfx_entries)
    ])

    # Inject SFX before captions mount
    if '<audio id="sfx-0"' not in index_html:
        # Find first <div data-composition-src
        index_html = re.sub(
            r'(\s*<div data-composition-src=)',
            f'\n{sfx_audio_html}\n\\1',
            index_html, count=1
        )

    # Inject SFX trigger script before window.__timelines["root"] = tl
    sfx_trigger = f'''
      // -------- SFX trigger (volume-controlled play) --------
      const SFX_CUES = [
        {sfx_js}
      ];
      SFX_CUES.forEach((cue) => {{
        tl.call(() => {{
          const a = document.querySelector(cue.id);
          if (a) {{ a.volume = cue.vol; a.currentTime = 0; a.play().catch(()=>{{}}); }}
        }}, null, cue.t);
      }});
'''
    if 'SFX_CUES' not in index_html:
        index_html = index_html.replace(
            'window.__timelines["root"] = tl;',
            sfx_trigger + '\n      window.__timelines["root"] = tl;'
        )

    (out / 'index.html').write_text(index_html)

    # Copy SFX
    for f in SFX_FILES:
        src = SFX_SRC / f
        dst = out / 'sfx' / f
        if src.exists() and not dst.exists():
            shutil.copy(src, dst)

    print(f'Scaffold complete → {out}')
    print(f'  Lessons:   {sum(1 for s in scenes if s["kind"]=="lesson")}')
    print(f'  Recap:     {"yes" if recap_scene else "no"}')
    print(f'  CTA:       {"yes" if cta_scene else "no"}')
    print(f'  SFX cues:  {len(sfx_entries)}')
    print(f'  Duration:  {total_duration:.2f}s')


if __name__ == '__main__':
    main()
