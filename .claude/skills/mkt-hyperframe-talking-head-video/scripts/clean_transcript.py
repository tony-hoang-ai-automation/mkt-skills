#!/usr/bin/env python3
"""Clean Whisper Vietnamese transcript + auto-group caption phrases.

Input:  transcript.json (whisper.cpp word-level format)
Output: transcript-cleaned.json (same structure, fixed text per word) +
        caption-groups.json (3-5 word phrases with start/end timing)

Usage:
    python3 clean_transcript.py path/to/transcript.json
"""
import json, re, sys, os

# Word-level replacements — apply when a single word matches exactly.
# Keep this list conservative; ambiguous words go in PHRASE_REPLACEMENTS instead.
WORD_REPLACEMENTS = {
    'alphabit': 'Alphabet', 'Alphabit': 'Alphabet',
    'kĩ': 'kỹ',
    'gián': 'gắn',          # "gián nhãn" → "gắn nhãn"
    'cốt': 'code',          # "viết cốt" → "viết code"
    'cod': 'Code', 'Cod': 'Code',
    'cán': 'cá',            # "cán nhân" → "cá nhân"
    'dưi': 'dưới',          # post-strip artifact
    'đng': 'đắc',           # "đng nhất" → "đắc nhất" post-strip
}

# Phrase-level replacements (handle context-sensitive cases including
# words that should stay unchanged in other contexts, e.g. "dụng" only
# becomes "dùng" in "bản dụng thử" / "dụng thử nghiệm").
PHRASE_REPLACEMENTS = [
    (r'\bbản dụng thử\b',      'bản dùng thử'),
    (r'\bnhãn dụng thử\b',     'nhãn dùng thử'),
    (r'\bgắn nhãn dụng\b',     'gắn nhãn dùng'),
    (r'\bthay đựng\b',         'tham vọng'),
    (r'\bđã nạp\b',            'đã làm'),
    (r'\btự xin khép\b',       'đợi xin phép'),
    (r'\bxin khép\b',          'xin phép'),
    (r'\btâm đ\S{1,3}ng\b',    'tâm đắc'),
    (r'\bđ\S{1,3}ng nhất\b',   'đắc nhất'),
    (r'\bh\S{1,2}n các\b',     'hẳn các'),
    (r'\bbỏ h\S{1,2}n\b',      'bỏ hẳn'),
    (r'cáchứng',               'cách ứng'),
    (r'\bứng dùng\b',          'ứng dụng'),
    (r'\báp dùng\b',           'áp dụng'),  # safety net if a word-level
                                              # replacement leaks into 'áp dụng'
    (r'doanh nghi[\S]{0,2}p',  'doanh nghiệp'),
    (r'\s+,', ','),
    (r'\s+', ' '),
]

# Unicode replacement char - strip silently. Whisper sometimes emits
# U+FFFD when it can't decode certain Vietnamese tone marks.
REPL_CHARS = ['�', '�']


def strip_repl_chars(text):
    for ch in REPL_CHARS:
        text = text.replace(ch, '')
    return text


def clean_word_text(word_text):
    """Clean a single word string: strip replacement chars, apply
    word-level dictionary if exact match. Preserve punctuation around the
    word so 'họ,' still becomes 'họ,'.
    """
    text = strip_repl_chars(word_text)
    # Match leading punctuation, core word, trailing punctuation.
    m = re.match(r'^([^\wÀ-ỹ]*)([\wÀ-ỹ]+)([^\wÀ-ỹ]*)$', text)
    if m:
        pre, core, post = m.groups()
        if core in WORD_REPLACEMENTS:
            core = WORD_REPLACEMENTS[core]
        return pre + core + post
    return text


def apply_phrase_replacements(text):
    for pat, repl in PHRASE_REPLACEMENTS:
        text = re.sub(pat, repl, text)
    return text


def clean_words(words):
    """Return new list of words with cleaned text. Timing untouched."""
    out = []
    for w in words:
        if not w.get('text'):
            continue
        new_text = clean_word_text(w['text'])
        if not new_text.strip():
            continue
        out.append({**w, 'text': new_text})
    return out


def group_captions(words, max_words=5, min_words=2, gap_break=0.45):
    """Auto-group word-level transcript into 3-5 word caption phrases.

    Break on:
    - silence gap > gap_break seconds between consecutive words
    - max_words reached

    Don't drop words; preserve full coverage.
    """
    groups = []
    cur = []
    for i, w in enumerate(words):
        if cur:
            gap = w['start'] - cur[-1]['end']
            if gap > gap_break or len(cur) >= max_words:
                if len(cur) >= min_words:
                    groups.append(cur)
                    cur = []
                # else: keep filling current group (under min)
        cur.append(w)
    if cur:
        groups.append(cur)

    # Convert to caption groups + apply phrase-level cleanup on full
    # text so context-sensitive replacements work across word boundaries.
    captions = []
    for g in groups:
        text = ' '.join(w['text'] for w in g).strip().rstrip(',')
        text = apply_phrase_replacements(text)
        captions.append({
            'text': text,
            'start': round(g[0]['start'], 2),
            'end': round(g[-1]['end'], 2),
        })
    return captions


def main():
    if len(sys.argv) < 2:
        print('Usage: clean_transcript.py path/to/transcript.json', file=sys.stderr)
        sys.exit(1)

    transcript_path = sys.argv[1]
    if not os.path.exists(transcript_path):
        print(f'Error: {transcript_path} not found', file=sys.stderr)
        sys.exit(1)

    with open(transcript_path) as f:
        words = json.load(f)

    cleaned_words = clean_words(words)
    captions = group_captions(cleaned_words)

    # Write cleaned word-level transcript next to the original.
    base_dir = os.path.dirname(os.path.abspath(transcript_path)) or '.'
    cleaned_path = os.path.join(base_dir, 'transcript-cleaned.json')
    captions_path = os.path.join(base_dir, 'caption-groups.json')

    with open(cleaned_path, 'w') as f:
        json.dump(cleaned_words, f, ensure_ascii=False, indent=2)
    with open(captions_path, 'w') as f:
        json.dump(captions, f, ensure_ascii=False, indent=2)

    print(f'Cleaned words: {len(cleaned_words)} → {cleaned_path}')
    print(f'Caption groups: {len(captions)} → {captions_path}')
    if captions:
        print(f'Last end: {captions[-1]["end"]:.2f}s')


if __name__ == '__main__':
    main()
