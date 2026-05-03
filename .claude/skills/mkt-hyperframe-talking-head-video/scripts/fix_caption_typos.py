#!/usr/bin/env python3
"""Auto-fix Whisper transcription typos against original script.

Compares caption-groups.json against script.txt (the source spoken text) and:
1. Detects common Vietnamese Whisper errors (clipped accent marks, brand misspellings)
2. Applies a known correction map (from past videos)
3. Reports unmatched suspicious patterns for manual review

Usage:
  python3 fix_caption_typos.py caption-groups.json script.txt
  # Writes corrected caption-groups.json in place

Common Whisper errors fixed:
  - vừa dọt → vừa rót, Cửa số → Cửa sổ, Chọn mạng → Chọn mảng
  - nói thng → nói thẳng, làm ch → làm chủ, Lê tân → Lễ tân
  - Tốiưu → Tối ưu (missing space)
  - chat GBT → ChatGPT, Cloud AI → Claude AI, Common Cloud → Comment Claude
  - Vụ khí → Vũ khí, level bổ → Lovable, Vice → Vise
  - triệu lý → trợ lý, nhà khoa → nha khoa
  - business triệu đâu → business triệu đô, gói điện và toaster → gói điện vào toaster
"""
import argparse
import json
import re
import sys
from pathlib import Path

# Curated correction map — append new errors here when discovered
KNOWN_FIXES = [
    # Format: (wrong, right) — applied in order
    ("vừa dọt", "vừa rót"),
    ("Cửa số đang", "Cửa sổ đang"),
    ("Cửa số ", "Cửa sổ "),  # standalone
    ("số đang mở", "sổ đang mở"),  # cross-group "Cửa | số đang mở"
    ("Chọn mạng bạn", "Chọn mảng bạn"),
    ("Chọn mạng", "Chọn mảng"),  # standalone
    ("một mạng,", "một mảng,"),
    ("nói thng", "nói thẳng"),
    ("làm ch ", "làm chủ "),
    ("làm ch.", "làm chủ."),
    ("làm ch,", "làm chủ,"),
    ("Tốiưu", "Tối ưu"),
    ("chat GBT", "ChatGPT"),
    ("Vụ khí", "Vũ khí"),
    ("Lê tân", "Lễ tân"),
    ("triệu lý", "trợ lý"),
    ("nhà khoa", "nha khoa"),
    ("phòng khám l c gọi", "phòng khám lỡ cuộc gọi"),
    ("Agency c ", "Agency cũ "),
    ("gói điện và toaster", "gói điện vào toaster"),
    ("toaster,ấm", "toaster, ấm"),
    ("business triệu đâu", "business triệu đô"),
    ("level bổ", "Lovable"),
    ("tốt cấp 10", "tốt gấp 10"),
    ("Vice nói thng", "Vise nói thẳng"),
    ("Vice ", "Vise "),
    ("Vice.", "Vise."),
    ("Common Cloud", "Comment Claude"),
    ("Cloud AI", "Claude AI"),
    ("video giải 5", "video dài 5"),
]


def apply_fixes(groups, fixes):
    changed = []
    for g in groups:
        orig = g["text"]
        new = orig
        for wrong, right in fixes:
            if wrong in new:
                new = new.replace(wrong, right)
        if new != orig:
            g["text"] = new
            changed.append((g["start"], orig, new))
    return changed


def find_suspicious(groups, script_text):
    """Heuristic — find caption tokens not present in script."""
    if not script_text:
        return []
    script_words = set(re.findall(r"[\w'-]+", script_text.lower()))
    suspicious = []
    for g in groups:
        # Strip punctuation, lowercase
        for tok in re.findall(r"[\w'-]+", g["text"].lower()):
            # Skip short tokens, brand-style ALLCAPS, numbers
            if len(tok) < 3 or tok.isdigit():
                continue
            if tok not in script_words:
                suspicious.append((g["start"], tok, g["text"]))
                break  # one per group
    return suspicious


def main():
    p = argparse.ArgumentParser()
    p.add_argument("caption_groups", help="Path to caption-groups.json")
    p.add_argument("script", nargs="?", help="Optional path to script.txt for additional diff check")
    p.add_argument("--dry-run", action="store_true", help="Print fixes without writing")
    args = p.parse_args()

    cap_path = Path(args.caption_groups)
    if not cap_path.exists():
        print(f"Error: {cap_path} not found", file=sys.stderr)
        sys.exit(1)

    groups = json.loads(cap_path.read_text())
    script_text = Path(args.script).read_text() if args.script else ""

    # Apply known fixes
    changed = apply_fixes(groups, KNOWN_FIXES)
    print(f"Applied fixes: {len(changed)} caption groups changed")
    for start, orig, new in changed:
        print(f"  {start:6.2f}s  '{orig}'  →  '{new}'")

    # Find remaining suspicious tokens (heuristic)
    if script_text:
        suspicious = find_suspicious(groups, script_text)
        if suspicious:
            print(f"\nSuspicious tokens (not in script — review manually):")
            for start, tok, text in suspicious[:15]:
                print(f"  {start:6.2f}s  token='{tok}'  in '{text}'")

    if not args.dry_run:
        cap_path.write_text(json.dumps(groups, ensure_ascii=False, indent=2))
        print(f"\nSaved → {cap_path}")
    else:
        print("\n[dry-run] No changes written")


if __name__ == "__main__":
    main()
