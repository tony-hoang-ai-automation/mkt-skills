# Known Pitfalls + Fixes

Bugs encountered while building the reference project (3-bai-hoc). All are fixed in the templates already — but if you hit a similar issue when customizing, this is the playbook.

## 1. Captions don't appear in Studio

**Symptom:** Studio plays the video but captions never show up.

**Root cause:** GSAP `y` transform conflicts with CSS `transform: translate(-50%, 0)` used for centering. When GSAP animates `y`, it overwrites the existing transform, removing the `-50%` X offset → captions render at `left: 50%` with no centering correction → off-screen to the right.

**Fix:** Use full-width container + `text-align: center` instead of transform centering.

```css
/* WRONG — transform centering breaks GSAP y */
.caption-group {
  position: absolute;
  left: 50%;
  transform: translate(-50%, 0);
}

/* RIGHT — full-width + text-align */
.caption-group {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  text-align: center;
}
.caption-group .text {
  display: inline-block;  /* centered by parent's text-align */
}
```

Templates already use the right pattern. Watch out if customizing.

## 2. Captions sync drift (5+ seconds off mid-video)

**Symptom:** Caption groups start in sync at the beginning, drift further off as video progresses.

**Root cause:** Hand-edited captions text and accidentally changed timestamps. Common when cleaning Whisper output manually — typing new text and altering `start`/`end` values.

**Fix:** Never hand-edit timing. Run `clean_transcript.py` for text fixes (preserves timing), and use `inject_captions.py` to write the JS array. If user wants to tweak text, edit only the `text` field in `caption-groups.json` then re-inject.

## 3. Lint error: `gsap_animates_clip_element`

**Symptom:**
```
✗ GSAP animation sets visibility on a clip element. Selector "#fs-hook" resolves to <div class="clip ...">.
The framework manages clip visibility via visibility — do not animate these properties on clip elements.
```

**Root cause:** Used `tl.set(selector, { visibility: "hidden" })` on an element with `class="clip"`. Framework reserves `visibility` for itself.

**Fix:** Animate only `opacity` (and transforms). Drop `visibility` from `tl.set()` calls on clip elements.

```js
// WRONG
tl.set("#fs-hook", { opacity: 0, visibility: "hidden" }, 4.0);

// RIGHT — opacity only
tl.set("#fs-hook", { opacity: 0 }, 4.0);
```

## 4. Sub-composition timeline doesn't run

**Symptom:** Sub-comp loads but animations never play.

**Root cause:** Forgot to register the timeline in `window.__timelines`, OR inner `<div data-composition-id>` missing `data-start="0"`.

**Fix:**
```js
window.__timelines["fs-lesson-1"] = tl;  // last line of script
```

```html
<div data-composition-id="fs-lesson-1" data-start="0" data-width="1080" data-height="1920">
```

## 5. Sub-comp content not visible (renders blank)

**Symptom:** Sub-comp mount fires at the right time, but inside is blank.

**Root cause:** Standalone `index.html` does NOT use `<template>` wrapper. Sub-comps loaded via `data-composition-src` MUST use `<template>` wrapper. Mixing this up hides content.

**Fix:**
- Root `index.html`: `<div data-composition-id="root">...content...</div>` (no template)
- Sub-comp file: `<template id="..."><div data-composition-id="...">...content...</div></template>`

## 6. Hook shows full-screen for first 3s, hiding face

**Symptom:** First 3 seconds are entirely a text card with no face visible.

**Root cause:** Hook scene uses `position: absolute; inset: 0` (full-frame). User feedback: "3s đầu LUÔN hiện face."

**Fix:** Hook is a small overlay at top, NOT full-screen.

```css
.hook-overlay {
  position: absolute;
  top: 170px;        /* upper third */
  left: 50%;
  transform: translateX(-50%);
  width: 880px;      /* leaves face area visible */
  /* NOT inset: 0 */
}
```

The hook's bottom edge sits ~520px from the frame bottom, leaving 1400px of face area visible.

## 7. Source video punch zoom causes visible jump

**Symptom:** At lesson scene boundaries (when face video re-appears after b-roll), there's a visible "snap" before the zoom-in animation starts.

**Root cause:** Used `tl.fromTo()` which sets the `from` value INSTANTLY at the time position. Zoom from 1.10 → 1.0 starts with a sudden jump to 1.10.

**Fix:** This is actually intentional and works well — the b-roll covers the face during the moment of jump, so user sees a smooth "zoom-in reveal" when face emerges. The pattern is correct as-is in templates.

If unwanted, replace `fromTo` with two separate `set` + `to`:
```js
tl.set("#v-source", { scale: 1.10 }, t - 0.001);  // hidden by b-roll
tl.to("#v-source", { scale: 1.0, duration: 0.55, ease: "power3.out" }, t);
```

## 8. SFX not playing in preview Studio

**Symptom:** Preview Studio plays video + voice but SFX silent.

**Root cause:** SFX file path wrong, OR file missing in `<project>/sfx/`, OR `data-volume` set to 0.

**Fix:**
1. Verify file exists: `ls workspace/video-projects/<slug>/sfx/`
2. Verify `<audio src="sfx/<file>.mp3">` path (relative to project root, NOT absolute)
3. Verify `data-volume` is between 0.15 and 0.35

## 9. Lint: `caption_exit_missing_hard_kill`

**Symptom:** Warning about caption exit animations without `tl.set` kill.

**Root cause:** Each caption group needs a deterministic kill at `group.end` to ensure framework correctly hides at scrub.

**Fix:** Templates already include the hard kill:
```js
tl.set(id, { opacity: 0, visibility: "hidden" }, g.end);
```

If lint complains, check the captions.html sub-comp has this set call inside the `forEach` loop.

## 10. Whisper translates instead of transcribing

**Symptom:** Vietnamese audio transcribed in English.

**Root cause:** Used `--model medium.en` (or any `.en` variant) on Vietnamese audio. `.en` models translate non-English to English.

**Fix:** Always use non-`.en` model + `--language vi`:
```bash
npx hyperframes transcribe source.mp4 --model medium --language vi
```

## 11. Render fails with "Asset load failure: 404"

**Symptom:** Render starts then warns about 404 on `caption-overrides.json` or other assets.

**Root cause:** Non-blocking warning. Hyperframes optionally checks for these files; if absent, warns but proceeds.

**Fix:** Ignore. Render still produces correct MP4. If concerned, create empty `caption-overrides.json` file.

## 12. Background music too loud / drowns voice

Not yet seen but possible if user adds BGM. Standard rule:
- Voiceover: 1.0
- BGM: 0.10–0.15 max
- SFX: 0.15–0.32

If voice unclear, lower BGM volume by 50% and re-test.
