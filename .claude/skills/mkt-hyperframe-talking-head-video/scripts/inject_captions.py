#!/usr/bin/env python3
"""Inject CAPTION_GROUPS array literal into a captions.html sub-composition.

Replaces the existing `const CAPTION_GROUPS = [...]` block with one rebuilt
from caption-groups.json. Preserves everything else in the file (CSS,
DOM, timeline animation logic, etc.).

This is the most error-prone manual step (large JS array, easy to break
syntax with hand edits). Always run this script — never hand-edit the
array.

Usage:
    python3 inject_captions.py path/to/captions.html path/to/caption-groups.json
"""
import json, re, sys, os


def main():
    if len(sys.argv) < 3:
        print('Usage: inject_captions.py <captions.html> <caption-groups.json>',
              file=sys.stderr)
        sys.exit(1)

    captions_html = sys.argv[1]
    groups_json = sys.argv[2]

    if not os.path.exists(captions_html):
        print(f'Error: {captions_html} not found', file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(groups_json):
        print(f'Error: {groups_json} not found', file=sys.stderr)
        sys.exit(1)

    with open(captions_html) as f:
        html = f.read()
    with open(groups_json) as f:
        groups = json.load(f)

    # Build the JS array literal with consistent indentation.
    lines = []
    for g in groups:
        text_escaped = g['text'].replace('\\', '\\\\').replace('"', '\\"')
        lines.append(
            f'        {{ text: "{text_escaped}", '
            f'start: {g["start"]:.2f}, end: {g["end"]:.2f} }},'
        )
    new_array = 'const CAPTION_GROUPS = [\n' + '\n'.join(lines) + '\n      ];'

    # Replace whatever array currently exists. Pattern matches from
    # `const CAPTION_GROUPS = [` through the closing `];` at the same
    # indentation level. Non-greedy across lines.
    pat = re.compile(r'const CAPTION_GROUPS = \[\s*\n(.*?)\n\s*\];', re.DOTALL)
    m = pat.search(html)
    if not m:
        print('Error: could not find CAPTION_GROUPS array in captions.html',
              file=sys.stderr)
        sys.exit(1)

    new_html = html[:m.start()] + new_array + html[m.end():]
    with open(captions_html, 'w') as f:
        f.write(new_html)

    print(f'Injected {len(groups)} caption groups → {captions_html}')
    if groups:
        print(f'Range: {groups[0]["start"]:.2f}s → {groups[-1]["end"]:.2f}s')


if __name__ == '__main__':
    main()
