# Pipeline: instagram-short

**Makes:** a vertical short / reel — 1080×1920, 9:16, 30fps, 15–60s (sweet spot 15–40s), sound-off-first with burned-in karaoke captions.
**When:** "instagram short", "reel", "vertical short", "tiktok", "karaoke captions" — one idea, one motif, landed hard.
**Master rules:** `references/VIDEO_PLAYBOOK.md` — sync, determinism, QA, VO/image scripts all apply. This doc is only the vertical deltas.

## Worked example anatomy (`templates/instagram-short/` — "tinyfish-collab", 39.5s single-segment)

```
DESIGN.md                     # the LOCKED vertical design gate (safe zones, sizes, motion below)
index.html                    # ROOT: one seg1 clip (track 1) + one vo.mp3 <audio> (track 3); local @font-face here
compositions/seg1.html        # the whole short as ONE sub-composition: 7 internal scenes + the caption engine
voiceover/segments.json       # TTS input — read by $SKILL_DIR/scripts/tts.py
voiceover/vo.mp3              # single VO clip (one clip per short is the norm)
voiceover/vo.transcript.json  # word-level transcript — captions AND scene cues both anchor to it
voiceover/build_captions.py   # transcript → assets/captions.js (chunk/word karaoke data); edit CHUNKS, rerun
assets/captions.js            # generated `window.WW_CAPS = {chunks, words}` — consumed by seg1's caption block
assets/*.png|svg              # hook/scene images (9:16-composed), partner + brand logos, videodb-logo.png
meta.json · hyperframes.json · package.json · template.json (workflow steps)
```

## Format rules

**Safe zones (non-negotiable — IG chrome covers the video):**
```
top    ~0–220px    risky: status bar / Reels tab — corner bug + ambient only
center ~220–1500px SAFE — all callouts, diagrams, numbers, payoff stamps
band   ~y1320–1460 caption band — karaoke captions ride here (worked example: .caps at top:1330)
bottom ~1500–1920  BLOCKED — username/caption/like rail; keep clear
```
Design readable content into the ~1080×1280 center band; treat top/bottom as bleed. Lint cannot see IG's UI — eyeball frames against the zones.

**Sound-off first (the biggest delta).** ~85% watch muted; the short must land with no audio. Karaoke captions are **mandatory** (long-form treats them as optional). Every claim is *also* stamped as a big on-screen callout — stamps carry the argument for a viewer who reads nothing else; VO is the polish layer.

**Karaoke captions (the canonical mechanism):** word-level transcript → edit the `CHUNKS` index ranges in `voiceover/build_captions.py` (group words into 2–6-word caption chunks; SKIP words that appear on-screen elsewhere, e.g. a typed query or the closing lockup) → `python3 voiceover/build_captions.py` writes `assets/captions.js`. `seg1.html` loads it and builds the DOM + GSAP tweens deterministically: chunk plate fades in at `start-0.06`, out at `end-0.22`; each word recolors to orange `#E85810` at its `start` and back to off-white after. Style: Inter 700 ~50–56px UPPERCASE on a dark plate (`rgba(11,11,12,.6)`, rounded), 2–4 words visible — never a full sentence block.

**Design system deltas** (same brand tokens as long-form, rewritten from `brand.json`):
- Same palette; orange `#E85810` is the entire energy budget (payoff stamp, key numbers, active caption word, active node).
- Type is bigger (phone at arm's length): **hero stamp 110–150px**, headline 72px+, caption 52–64px, data label 28px+. Archivo Black display / Inter body (auto-embed).
- Motion is snappier: stamps pop **0.2–0.35s**, blur-crossfade **~0.4s** (vs 0.55), marker arrows draw 0.35–0.5s. **Continuous-motion cadence tightens to ~1.5–2.5s** (vs 2–3s long-form). Slow push-ins (1.0→1.06) for life.
- Layouts stack **vertically**: visual on top, stamps below (or stamp punched center over a dimmed visual); pipelines run top→bottom; marker arrows point down or circle a number.

**Cold-open hook rule (first ~1 second):** frame 1 IS the hook — strongest number/quote/villain immediately. No logo open, no wind-up. The corner bug appears at once (**top-left**, out of the very top strip — the worked example puts it at left:46 top:150); the full logo stamp is reserved for the end/CTA card only. Frame 1 doubles as the grid thumbnail — export it: `ffmpeg -i out.mp4 -frames:v 1 cover.png -y`. **Loop-aware:** the last frame should sit comfortably next to the first (IG auto-loops).

## Build workflow (deltas on the master loop)

1. Scaffold: `python3 "$SKILL_DIR/scripts/new_project.py" instagram-short <slug>`; study the example (`npm install && npx hyperframes preview`).
2. Script ONE idea, hook first: ~40–110 words of VO for 15–40s. Beat sheet with three distinct short layers per beat — on-screen stamp ≠ caption ≠ VO. Confirm `DESIGN.md` (design gate).
3. VO: `voiceover/segments.json` → `python3 "$SKILL_DIR/scripts/tts.py"` (BYO-key / prompt fallback; drop your MP3 in as `voiceover/vo.mp3`).
4. Transcribe: `npx hyperframes transcribe voiceover/vo.mp3` → `voiceover/vo.transcript.json`.
5. Captions: edit `CHUNKS`/`SKIP`/`MERGES` in `voiceover/build_captions.py` → run it → check its printed chunk table reads naturally.
6. Cues: a single-segment short can anchor scene changes directly to transcript word times; multi-segment shorts use `voiceover/cues_spec.json` + `$SKILL_DIR/scripts/extract_cues.py` as usual (with ~0.3s gaps between segments, not 0.6 — shorts breathe less).
7. Build `compositions/seg1.html` mirroring the example: `.scene` is `width:1080px;height:1920px`, blur-crossfade helpers with `XF=0.4`, stamps/arrows on real cue times, captions block intact, content inside the center band.
8. Images (if any): `$SKILL_DIR/scripts/gen_image.py assets/x.png 9:16 "prompt"` — subject composed into the center safe band.
9. QA + render per master playbook (`inspect --samples 40` is enough for ≤60s; extract frames and check the safe zones + caption band specifically). Confirm the final: `ffprobe` → 1080×1920, 30fps, h264+aac (~8–20 MB for 30s).

## Format-specific gotchas

- Don't copy 1920×1080 scene CSS from an episode — everything is 1080×1920, and the render is **30fps not 24**.
- Don't slide tall content off-screen to transition (the overflow/clipped-text trap) — crossfade.
- Text in the top ~220px or bottom ~420px passes lint but gets eaten by IG chrome at playback.
- The worked example loads two extra local fonts (`Marker`, `Caveat`) via `@font-face` **in the root `index.html` head** with local woff2 files — that placement renders; `@font-face` inside the sub-composition `<template>` does NOT. Keep core type on auto-embed Inter/Archivo Black and verify any extra font from an MP4 frame.
- Rebuilding captions after re-cutting VO: re-transcribe first, then re-run `build_captions.py` — the CHUNKS word indices shift with any wording change.
- Track alternation still applies if you add clips; audio stays on its own track.
