#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["opencv-python>=4.8"]
# ///
"""
Detect speaker face in a stationary talking-head video and compute
BOTTOM / FULLSCREEN / HIDDEN transform constants for face-mode choreography.

Why this exists: hardcoded constants assume the speaker is centered in a
1920x1080 frame. Real recordings drift — speaker sits left of center, sits
lower, the camera is angled. Hardcoding produces visible dead space and
crops in BOTTOM mode and off-center crops in FULLSCREEN.

Assumptions:
- Speaker is mostly stationary (sit/stand still) — 1 sample frame is
  enough to fix BOTTOM and FULLSCREEN for the entire short.
- Source video can be any landscape resolution (read with ffprobe).
- Output composition is 1080x1920.
- face-wrapper uses transform-origin: 0 0 (top-left). The translate(x,y)
  values in the output are post-scale absolute pixel offsets. If your
  index.html sets a different origin, recompute manually or change this
  script.

Usage:
  uv run scripts/detect_face.py <edit.mp4>
  uv run scripts/detect_face.py <edit.mp4> --timestamp 2.5 --output assets/face-modes.json
  uv run scripts/detect_face.py <edit.mp4> --bottom-face-h 520 --fullscreen-face-h 700

Output: JSON with face bbox + computed BOTTOM/FULLSCREEN/HIDDEN.
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def ffprobe_dims(video: Path) -> tuple[int, int]:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=p=0:s=x", str(video),
        ],
        capture_output=True, text=True, check=True,
    )
    w, h = r.stdout.strip().split("x")
    return int(w), int(h)


def extract_frame(video: Path, t: float, out_png: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-ss", str(t), "-i", str(video),
            "-frames:v", "1", "-q:v", "2", str(out_png),
        ],
        check=True, capture_output=True,
    )


def detect_face(png_path: Path) -> dict:
    import cv2

    img = cv2.imread(str(png_path))
    if img is None:
        sys.exit(f"ERROR: cannot read {png_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = cascade.detectMultiScale(gray, 1.1, 5, minSize=(80, 80))

    if len(faces) == 0:
        sys.exit(
            "ERROR: no face detected. Try --timestamp at a moment when the speaker "
            "is facing the camera with normal lighting. Avoid hand-on-chin / profile shots."
        )

    fx, fy, fw, fh = max(faces, key=lambda f: f[2] * f[3])  # largest = closest
    return {"x": int(fx), "y": int(fy), "w": int(fw), "h": int(fh)}


def compute_modes(
    src_w: int,
    src_h: int,
    face: dict,
    bottom_face_h: float = 480,
    fullscreen_face_h: float = 640,
    bottom_face_center_y: float = 1440,
    fullscreen_face_center_y: float = 600,
    out_w: int = 1080,
    out_h: int = 1920,
) -> dict:
    """
    Compute transforms assuming transform-origin: 0 0.

    For each mode we want: face_center_in_source * scale + translate = face_center_in_output.
    So:  translate = face_center_in_output - scale * face_center_in_source

    BOTTOM:     face center lands at (out_w/2, bottom_face_center_y) — bottom half of frame.
                Default 480px face → ~25% of vertical frame, leaves room above for scenes.
    FULLSCREEN: face center lands at (out_w/2, fullscreen_face_center_y) — upper third.
                Default 640px face → ~33% of frame; upper-third position gives good headroom.
                Scale is force-bumped if needed so wrapper fully covers 1080x1920 (no gaps).
    HIDDEN:     same geometry as BOTTOM (so opacity-fade doesn't drift hình học).
    """
    fcx = face["x"] + face["w"] / 2
    fcy = face["y"] + face["h"] / 2
    fh = face["h"]

    s_b = bottom_face_h / fh
    x_b = out_w / 2 - s_b * fcx
    y_b = bottom_face_center_y - s_b * fcy

    s_f = fullscreen_face_h / fh
    # Guarantee fullscreen mode actually fills the portrait frame (no edge gap)
    min_s_f_w = out_w / src_w
    min_s_f_h = out_h / src_h
    min_s_f = max(min_s_f_w, min_s_f_h)
    if s_f < min_s_f * 1.02:
        s_f = min_s_f * 1.05
    x_f = out_w / 2 - s_f * fcx
    y_f = fullscreen_face_center_y - s_f * fcy

    return {
        "BOTTOM":     {"x": round(x_b, 1), "y": round(y_b, 1), "scale": round(s_b, 4)},
        "FULLSCREEN": {"x": round(x_f, 1), "y": round(y_f, 1), "scale": round(s_f, 4)},
        "HIDDEN":     {"x": round(x_b, 1), "y": round(y_b, 1), "scale": round(s_b, 4), "opacity": 0},
    }


def emit_js_snippet(modes: dict) -> str:
    """Pretty JS lines you can paste into index.html."""
    def fmt(name, m):
        opa = f", opacity: {m['opacity']}" if "opacity" in m else ""
        return f"const {name:<10} = {{ x: {m['x']:>8}, y: {m['y']:>6}, scale: {m['scale']:.4f}{opa} }};"
    return "\n".join([
        fmt("BOTTOM",     modes["BOTTOM"]),
        fmt("FULLSCREEN", modes["FULLSCREEN"]),
        fmt("HIDDEN",     modes["HIDDEN"]),
    ])


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video", help="Path to the edited talking-head video (e.g. assets/<name>-edit.mp4)")
    p.add_argument("--timestamp", type=float, default=1.0,
                   help="Seconds into the video to sample for face detection (default 1.0).")
    p.add_argument("--bottom-face-h", type=float, default=480,
                   help="Target face height in BOTTOM mode, output pixels (default 480 = 25%% of 1920).")
    p.add_argument("--fullscreen-face-h", type=float, default=640,
                   help="Target face height in FULLSCREEN mode, output pixels (default 640 = 33%% of 1920).")
    p.add_argument("--bottom-face-y", type=float, default=1440,
                   help="Y of face center in BOTTOM mode, output pixels (default 1440 = mid bottom-half).")
    p.add_argument("--fullscreen-face-y", type=float, default=600,
                   help="Y of face center in FULLSCREEN mode, output pixels (default 600 = upper third).")
    p.add_argument("--output", default=None, help="Write JSON to this path (default: stdout only).")
    args = p.parse_args()

    video = Path(args.video).resolve()
    if not video.exists():
        sys.exit(f"ERROR: {video} not found")

    src_w, src_h = ffprobe_dims(video)

    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "sample.png"
        extract_frame(video, args.timestamp, png)
        face = detect_face(png)

    modes = compute_modes(
        src_w, src_h, face,
        bottom_face_h=args.bottom_face_h,
        fullscreen_face_h=args.fullscreen_face_h,
        bottom_face_center_y=args.bottom_face_y,
        fullscreen_face_center_y=args.fullscreen_face_y,
    )

    result = {
        "source_video": str(video),
        "source_dims":  [src_w, src_h],
        "sample_timestamp": args.timestamp,
        "face_bbox":    face,
        "face_modes":   modes,
        "js_snippet":   emit_js_snippet(modes),
        "transform_origin_assumed": "0 0",
        "note": (
            "Calibrated for THIS recording's actual face position. Paste js_snippet into "
            "index.html. Verify with a 1-frame preview before committing scenes."
        ),
    }

    out = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}\n")
    print(out)


if __name__ == "__main__":
    main()
