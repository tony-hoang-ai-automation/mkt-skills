# Effects Catalog — Per Scene Type

Each lesson sub-comp gets a different set of effects to keep the video visually fresh. Don't repeat the same effect across multiple lessons — viewer fatigue.

## Source video (face-cam) effects

| Effect | When | How |
|---|---|---|
| Entry punch zoom | t=0s, sync camera-flash SFX | `tl.fromTo("#v-source", { scale: 1.10 }, { scale: 1.0, duration: 0.6, ease: "power3.out" }, 0)` |
| Reveal punch zoom | After each full-screen b-roll exits | Same pattern, scale 1.10–1.12 → 1.0, duration 0.55–0.6 |
| Ambient ken-burns drift | During long talking sections (15s+) | `tl.fromTo("#v-source", { scale: 1.0 }, { scale: 1.04, duration: <stretch>, ease: "sine.inOut" }, <start>)` |

CSS prerequisite: `#v-source { transform-origin: center 38%; }` — anchor to face area for natural zoom feel.

## Lesson 1 (foundational) — recommended effects

- **Background radial glow** behind NUM (warm halo, opacity 0.18, fades in)
- **3 pulse rings** expanding outward from NUM (1.5s cycles, scale 0.5→2.4, opacity 0.6→0)
- **4 corner accent marks** (L-shapes burnt sienna, draw in with stagger 0.06s)
- **Word-by-word slam title** (each `.word` falls from y=-50, scale 1.6→1.0, back.out 1.8, stagger 0.07)
- **NUM entry rotation** (rotation -8° → 0°, back.out 1.6)
- **NUM ambient breath** (scale 1.0 ↔ 1.05 sine.inOut yoyo)
- **Sub gentle drift** (y -6 sine.inOut)

Background: dark `#141413`. Color: `#faf9f5`. Accents: `#d97757`.

## Lesson 2 (urgency / speed) — recommended effects

- **Speed lines** (8 thin lines streak across frame, alternating sides, opacity 0→0.7→0)
- **Background dotted pattern** (radial dots subtle, fades in)
- **Corner ticks** (text "⏱ FAST" top-left, "SHIP NOW ›" bottom-right blinking)
- **Count-up number** (e.g., "0 → 24" tick over 0.7s, snap: { innerText: 1 })
- **Word-by-word slam title**
- **NUM entry rotation +8°** (opposite direction from Lesson 1)
- **24 number scale pulse** after count-up settles
- **Corner tick blinking** opacity 0.5↔1.0 yoyo

Background: cream `#faf9f5`. Color: `#141413`.

## Lesson 3 (most important / "tâm đắc nhất") — recommended effects

- **Radial light sweep** (1400px halo, slow rotate 60° over 4s)
- **8 diagonal rays** burst out from center (stagger 0.04s, opacity 0→0.9 then fade to 0.15)
- **"★ Bài học vàng" badge** at top (slam-in from above, scale 1.4→1.0)
- **Scribble underline** SVG path under accent word (`stroke-dasharray` draw-in)
- **Word-by-word slam title**
- **NUM stronger pulse** scale 1.0 ↔ 1.06
- **Badge subtle bounce** scale 1.0 ↔ 1.06
- **Light sweep opacity breath**

Background: dark `#141413`. Stronger punch entrance (scale 1.15 → 1.0).

## Lesson 4+ — rotate variants

For videos with 4+ lessons, cycle Lesson 1/2/3 variants. Don't introduce a 4th variant — viewer attention is already taxed; reuse what works.

## CTA scene — recommended effects

- **Background radial pulse** (1200px halo, continuous breath)
- **Typing cursor** blink before pill appears (~2Hz, 4 cycles)
- **Pill slam-in** (scale 0.4 → 1.0, rotation -6°, back.out 1.8)
- **8 sparkle dots** burst around pill, twinkle random opacity
- **3 ripple rings** expanding from pill outward (1.2s each, 3 cycles)
- **6 floating particles** rise from bottom to top (2.5s travel, looping)
- **Bouncing arrow** y 0 ↔ 18 sine.inOut yoyo
- **Pill scale pulse** scale 1.0 ↔ 1.06 sine.inOut yoyo

Background: dark `#141413`. Pill: `#d97757`. Arrow: `#d97757`.

## Recap card (overlay, NOT full-screen) — recommended effects

- **Card slide-up + scale soft entrance** (y 50, scale 0.96 → 1.0, power3.out)
- **Eyebrow x slide-in**
- **3 row stagger** (x 60 → 0, opacity 0 → 1, stagger 0.18s)

Keep recap minimal — it's a quiet moment between lesson energy and CTA finale.

## Caption effects

Default: simple fade + y rise (y 18 → 0, opacity 0 → 1, duration 0.18). Hard kill at `group.end` via `tl.set(id, { opacity: 0, visibility: "hidden" }, end)`.

Don't add per-word effects on captions for talking-head videos — viewer is already watching the speaker; complex caption animation is distracting. Keep captions clean and synced.

## Hook overlay (top, 0–4s) — recommended effects

- **Card scale + opacity entrance** (scale 0.94, opacity 0 → 1, back.out 1.5)
- **Eyebrow slide-down**
- **Title slide-up with back.out**
- **Rule line draw-in** (scaleX 0 → 1, transformOrigin left center)
- **Sub fade-up**
- **Soft fade-out at 3.55–4.0s** before clip ends

NOT full-screen. Sits at top:170px so face stays visible underneath.

## Effects to AVOID

- **Glitch / VHS effects** — feels low-quality on cream/burnt-sienna brand
- **Neon glow** — clashes with Anthropic-style flat paper aesthetic
- **Strobing / flicker** above 4Hz — accessibility (epilepsy) concern
- **Particle systems with >10 elements** — looks busy, render slow
- **Full-screen color flashes** — distracting from talking head focus
- **Continuous infinite loops** with `repeat: -1` — breaks HyperFrames capture engine, always use finite repeats: `Math.ceil(duration / cycle) - 1`

## Performance notes

- Each sub-comp adds ~120–180 lines of code. Keep total project under 6 sub-comps for fast lint/preview.
- GSAP timelines with 30+ tweens render fine; 100+ may slow Studio scrubbing.
- SVG `stroke-dashoffset` animations are cheap. CSS `box-shadow` animation is expensive — avoid animating shadow on >5 elements simultaneously.
