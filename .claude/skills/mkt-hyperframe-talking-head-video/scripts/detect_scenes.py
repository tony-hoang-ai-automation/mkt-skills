#!/usr/bin/env python3
"""Detect scene structure from a Vietnamese transcript.

Looks for canonical markers (Bài học N, Tip N, Tổng kết, Comment) and
returns timestamps + suggested kicker/heading for each scene.

When markers are absent, falls back to a single-section structure
(intro + CTA only).

Usage:
    python3 detect_scenes.py path/to/transcript.json [--output scenes.json]
"""
import json, re, sys, os, argparse


# Vietnamese scene markers — ordered by priority. The first matching
# marker per "lesson slot" wins. Patterns are case-insensitive.
LESSON_MARKERS = [
    (r'\bbài học (đầu tiên|thứ nhất|số một|số 1)\b', 1),
    (r'\bbài học thứ (hai|2)\b', 2),
    (r'\bbài học thứ (ba|3)\b', 3),
    (r'\bbài học thứ (tư|bốn|4)\b', 4),
    (r'\bbài học thứ (năm|5)\b', 5),
    (r'\btip (số một|số 1|đầu tiên|1)\b', 1),
    (r'\btip (số hai|số 2|2)\b', 2),
    (r'\btip (số ba|số 3|3)\b', 3),
]

RECAP_MARKERS = [
    r'\btổng kết (lại|lại nhé)?\b',
    r'\bkết luận\b',
    r'\btóm lại\b',
]

CTA_MARKERS = [
    r'\bcomment\b',
    r'\b(đăng ký|like|theo dõi|follow)\b',
    r'\bhãy\s+(comment|like|share|đăng ký)\b',
    r'\b(nhấn|bấm)\s+(theo dõi|follow|like)\b',
]


def find_first_match(text, patterns):
    """Return (match_obj, pattern_idx) of the first regex that hits, or None."""
    for i, p in enumerate(patterns):
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m, i
    return None


def find_marker_in_words(words, pattern):
    """Find the first window of consecutive words whose joined text matches
    the pattern. Returns the start time of the first matching word, or None.
    """
    n = len(words)
    for window in (4, 5, 6, 3):
        for i in range(n - window + 1):
            snippet = ' '.join(words[i + j]['text'] for j in range(window))
            if re.search(pattern, snippet, re.IGNORECASE):
                return words[i]['start']
    return None


def detect_lesson_starts(words):
    """Return ordered list of (lesson_num, start_time)."""
    found = {}
    for pat, num in LESSON_MARKERS:
        if num in found:
            continue
        t = find_marker_in_words(words, pat)
        if t is not None:
            found[num] = t
    return sorted(found.items())  # [(1, 9.4), (2, 34.5), ...]


def detect_recap_start(words):
    for pat in RECAP_MARKERS:
        t = find_marker_in_words(words, pat)
        if t is not None:
            return t
    return None


def detect_cta_start(words):
    """Find the latest CTA marker (CTA usually near end)."""
    last_t = None
    for pat in CTA_MARKERS:
        for i in range(len(words) - 3):
            snippet = ' '.join(words[i + j]['text'] for j in range(min(4, len(words) - i)))
            if re.search(pat, snippet, re.IGNORECASE):
                t = words[i]['start']
                if last_t is None or t > last_t:
                    last_t = t
    return last_t


def build_scenes(words, total_duration):
    lesson_starts = detect_lesson_starts(words)
    recap_start = detect_recap_start(words)
    cta_start = detect_cta_start(words)

    scenes = []
    if lesson_starts:
        # Each lesson scene shows the b-roll for ~3.5-4s starting at the
        # lesson marker word.
        for idx, (num, start) in enumerate(lesson_starts):
            duration = 3.6 if num != lesson_starts[-1][0] else 4.0
            scenes.append({
                'kind': 'lesson',
                'num': num,
                'start': round(start, 2),
                'end': round(start + duration, 2),
                'kicker': f'Bài học #{num}',
                'heading': '',  # caller fills based on context
            })

    if recap_start is not None:
        # Recap card is an OVERLAY (z-24), runs from recap marker to CTA
        # start (or end of video if no CTA).
        end = cta_start if cta_start else total_duration
        scenes.append({
            'kind': 'recap',
            'start': round(recap_start, 2),
            'end': round(end, 2),
        })

    if cta_start is not None:
        scenes.append({
            'kind': 'cta',
            'start': round(cta_start, 2),
            'end': round(total_duration, 2),
        })

    return {
        'type': 'lessons' if lesson_starts else ('cta-only' if cta_start else 'free-form'),
        'total_duration': round(total_duration, 2),
        'scenes': scenes,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('transcript', help='Path to transcript.json (word-level)')
    ap.add_argument('--output', '-o', default=None, help='Output scenes.json path')
    args = ap.parse_args()

    if not os.path.exists(args.transcript):
        print(f'Error: {args.transcript} not found', file=sys.stderr)
        sys.exit(1)

    with open(args.transcript) as f:
        words = json.load(f)

    if not words:
        print('Error: empty transcript', file=sys.stderr)
        sys.exit(1)

    total_duration = words[-1]['end']
    scenes = build_scenes(words, total_duration)

    output = args.output or os.path.join(
        os.path.dirname(os.path.abspath(args.transcript)) or '.',
        'scenes.json',
    )
    with open(output, 'w') as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)

    print(f'Detected: type={scenes["type"]}, scenes={len(scenes["scenes"])}')
    for s in scenes['scenes']:
        if s['kind'] == 'lesson':
            print(f'  Lesson #{s["num"]}: {s["start"]:.2f}-{s["end"]:.2f}s')
        else:
            print(f'  {s["kind"]}: {s["start"]:.2f}-{s["end"]:.2f}s')
    print(f'→ {output}')


if __name__ == '__main__':
    main()
