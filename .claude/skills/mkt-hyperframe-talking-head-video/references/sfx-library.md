# Sound Effects Library

Library at `workspace/assets/reels/sfx/` (full library) — copy 6 needed files into project's `sfx/` folder.

## 6 SFX standard mapping (use these by default)

Use these for any video with the lesson + recap + CTA pattern. Each SFX
plays at a specific moment with carefully tuned volume so it doesn't
drown out the voiceover.

| Time | File | Volume | Moment |
|---|---|---|---|
| 0.0s | `camera-flash.mp3` | 0.32 | Hook opener — sync với source video punch zoom @0s |
| (lesson 1 start − 0.05s) | `búng tay.mp3` | 0.30 | Snap reveal cho lesson 1 |
| (lesson 2 start − 0.05s) | `Whoosh sound effect (1).mp3` | 0.22 | Whoosh transition cho lesson 2 |
| (lesson 3 start − 0.05s) | `Laser.mp3` | 0.28 | Laser punch cho lesson 3 (most important) |
| (recap start − 0.05s) | `ting.mp3` | 0.20 | Light bulb cho recap reveal |
| (cta start) | `Discord Notification - Sound Effect.mp3` | 0.28 | Notification feel cho CTA |

## Volume rule

- **Hook SFX**: 0.25–0.35 (loudest — needs attention grab)
- **Transition SFX**: 0.15–0.20 (gentle — not competing with voice)
- **CTA SFX**: 0.25–0.30 (clear but not jarring)

Anything above 0.35 will drown the voiceover. Anything below 0.15 won't be heard on phone speakers.

## Spacing rule

- **Max 5–6 SFX** per video (more = noisy, audience tunes out)
- **Minimum 1.5s gap** between consecutive SFX (overlap = muddy mix)
- **Front-load**: 60% of SFX in first 10s if hook is critical

## Alternative SFX (when standard mapping doesn't fit)

For videos that aren't the lesson pattern (vlog, story, demo), pick from:

### Reaction (surprise/shock — for hook moments)
- `SUDDEN SUSPENSE.mp3` (1.3s) — quick suspense, dramatic opener
- `DUN DUN DUNNN.mp3` (4.0s) — dramatic reveal (use first 1.5s)
- `Wow.mp3` (2.3s) — impressive result

### Positive / success (for solution / aha moment)
- `tada.mp3` (0.6s) — quick win
- `tada tada.mp3` (1.9s) — bigger celebration
- `lung linh.mp3` (1.7s) — magical/sparkle
- `ting.mp3` (0.9s) — light bulb (used for recap by default)

### Transition / emphasis
- `Whoosh sound effect (1).mp3` (1.1s) — fast scene change
- `búng tay.mp3` (0.3s) — finger snap, "just like that"
- `Laser.mp3` (0.4s) — tech/futuristic punch
- `boom.mp3` — heavy impact

### CTA / notification
- `Discord Notification - Sound Effect.mp3` (0.9s) — soft notif
- `tada tada.mp3` — celebratory ending

## Custom SFX

User can drop new MP3 files into project's `sfx/` folder, then add
`<audio>` clip in root index.html with appropriate `data-start`,
`data-duration`, `data-volume`.

Verify file exists before referencing:
```bash
[ -f "workspace/video-projects/<slug>/sfx/<file>.mp3" ] && echo OK || echo MISSING
```

## Why these specific SFX?

The 6 default SFX cover the full emotional arc of a 3-lesson + CTA video:
1. **Hook** (camera-flash): "Pay attention! Something starts now."
2. **Lesson 1** (snap): "Quick fact. Listen up."
3. **Lesson 2** (whoosh): "Moving on to the next."
4. **Lesson 3** (laser): "This is the important one."
5. **Recap** (ting): "Let me summarize."
6. **CTA** (notification): "Take action now."

Each SFX matches the energy of its moment. Camera-flash is sharp and immediate; whoosh suggests forward motion; laser feels precise/important; notification mimics a phone alert (familiar dopamine cue).
