# Pipeline: youtube-longform

**Makes:** a long-form narrated explainer / tech video-essay — 1920×1080, 16:9, 24fps, target 3–5 min.
**When:** "youtube video", "explainer", "video essay", "long-form" — a multi-segment argument carried by one narrator.
**Master rules:** `references/VIDEO_PLAYBOOK.md` — sync, determinism, QA, VO/image scripts, retention craft all apply. This doc is only the format deltas.

## Worked example anatomy (`templates/youtube-longform/` — 8-segment "chess-vision" episode)

```
SCRIPT.md                     # episode script: per-segment VO + on-screen text + visual + cue→next phrase
DESIGN.md                     # the LOCKED design gate (palette/type/motion below) — copied into every episode
BUILD_KIT.md                  # segment skeleton + component CSS + JS helpers (countUp/typewrite/stamp/drawArrow)
LOGOS.md                      # inline-SVG marks for third-party logos (rendered white, never their brand color)
index.html                    # ROOT: 8 segment clips back-to-back on tracks 1/2, 8 <audio> VO clips on track 3
compositions/seg1..seg8.html  # one <template> sub-composition per narration paragraph; seg1 = canonical exemplar
voiceover/segments.json       # TTS input (voice_id, model, per-segment tagged lines) — read by $SKILL_DIR/scripts/tts.py
voiceover/segN_*.mp3          # one VO clip per segment
voiceover/segN_*.transcript.json  # word-level whisper transcript per clip (never skip)
voiceover/cues_spec.json      # per-segment {scene_id: trigger phrase | 0.0}
cues.json                     # OUTPUT of extract_cues.py — real scene times; the build brief for each segment
assets/                       # AI/real photos, logo files, brand bug (videodb-logo.png)
meta.json · hyperframes.json · package.json · template.json (workflow steps)
```

## Format rules

**Episode structure.** One segment = one paragraph = one idea (~20–70s; hook/close can run longer, tips 25–40s). A 3–5 min episode is 6–9 segments. Each segment holds several internal scenes that blur-crossfade at real cue times.

**Root assembly** (mirror `index.html`): segment video clips back-to-back, `data-track-index` alternating `1`/`2` (float trap); all VO `<audio>` on track `3`; each video clip = its audio duration + a **0.6s gap** (clip holds the last scene; audio is natural length at segment start).

**The locked design system** (`DESIGN.md` — brand tokens rewritten from `brand.json` via the `BRAND:START/END` blocks in each segment's CSS variables):
- Palette: `#0B0B0C` canvas · `#141416` cards · **`#E85810` orange, THE one accent** · `#F4F2EE` text · `#8C8C94` muted · `#2A2A2E` hairlines · `#E5484D` ✗-red · `#3DD68C` ✓-green.
- Type: **Archivo Black** display (UPPERCASE, tracking ~0.01em, line-height ~0.95) + **Inter** 300/500/700 body — both auto-embed; do NOT use Anton or unverified fonts (silent fallback — confirm any new font from an MP4 frame, not lint). Headlines 60px+, body 20px+, labels 16px+, `tabular-nums` on numbers.
- Motion: eases `power3.out`/`expo.out` (headlines), `power2.out` (cards), one-shot `back.out` pops on small elements. **Blur-crossfade 0.55s** between scenes — no jump cuts. Callout boxes stamp in 0.25–0.4s; numbers count up; marker arrows draw on (`stroke-dashoffset`→0, 0.4–0.6s) landing AT the cue word. Slow intentional push-ins (scale 1.0→1.08 over the scene) are encouraged; aimless wobble is not.
- Continuous motion: something meaningful changes every ~2–3s. Every element animates IN; no exits except the final scene.

**Signature motifs** (pick, then repeat for a through-line):
- **✗→✓ flip** (red frankenstack → green/orange one-backend) — the most screenshot-able comparison frame.
- **Orange payoff box** (`.box.pay`) — the "this is the point" stamp, ONCE per segment.
- An animated pipeline spine of nodes (`.node` → `.node.on` in orange).
- Persistent low-opacity corner logo bug every segment; full logo stamps only after the hook and on the end/CTA card. Dark backgrounds only.

**Real images:** AI-generate photographic beats (people, places, real-world scenes) via `$SKILL_DIR/scripts/gen_image.py out.png 16:9 "prompt"`; keep UI mockups, charts, diagrams as CSS/SVG. When naming a real model/product, show its logo from `LOGOS.md`, rendered white. Sourced or clearly representative only — never fabricated posts.

## Build workflow (deltas on the master loop)

1. Scaffold: `python3 "$SKILL_DIR/scripts/new_project.py" youtube-longform <slug>` — then study the worked example before touching anything (`npm install && npx hyperframes preview`).
2. Write `SCRIPT.md` in the example's shape: per segment — VO (with eleven_v3 delivery tags), on-screen text (short stamps, never the sentence), visual description, and the **cue → next** phrase. Get the script approved.
3. Confirm `DESIGN.md` with the user (design gate) — the scaffold copied it; adapt only with a written reason.
4. VO: edit `voiceover/segments.json` → `python3 "$SKILL_DIR/scripts/tts.py"` (BYO-key; no key → paste-ready prompt blocks, drop MP3s into `voiceover/`).
5. Transcribe every MP3: `npx hyperframes transcribe voiceover/<seg>.mp3` → save as `voiceover/<seg>.transcript.json`.
6. Cues: fill `voiceover/cues_spec.json` (one entry per scene; `0.0` or a trigger phrase) → `python3 "$SKILL_DIR/scripts/extract_cues.py"` → `cues.json`. Anchor every crossfade AT the cue; entrances start cue+0.25.
7. Build `compositions/segN.html` by **mirroring `compositions/seg1.html` and `BUILD_KIT.md`**: same skeleton (scoped styles under `[data-composition-id="segN"]`, paused timeline in `window.__timelines`, 0-based times), same components (`.box`, `.box.pay`, `.namelabel`, `.card`, `.chip`, `.node`, `.bignum`, `.marker`), same helpers (`fadeIn/fadeOut`, `countUp`, `typewrite`, `stamp`, `drawArrow`). Segments are silent, opaque, full-frame; the root owns all audio. Fan segments out to parallel agents — give each the composition id, duration, exact cues, asset paths, and seg1 as exemplar; you own assembly + QA.
8. Assemble the root exactly like the example (gaps, alternating tracks, audio track 3), then QA + render per the master playbook (`inspect --samples 60` for a 4–6 min timeline; extract frames and eyeball the hero frames and fonts).

## Format-specific gotchas

- Building visuals before transcribing is the expensive mistake — estimated cue times always drift and you redo everything.
- The `@font-face` inside a `<template>` sub-composition does NOT apply at render — stick to auto-embed fonts (Inter, Archivo Black).
- No full-screen linear gradients on the dark canvas (H.264 banding) — solid + localized radial glow (`.glow`) only.
- No emojis in the capture engine — CSS/SVG shapes or `✓ ✗ ★ ▲ → ☏`.
- Never put the logo on a light surface (the white part of the mark vanishes).
- Respect the runtime: 3–5 min. Tip-list scripts balloon to 6–7 min if you don't cut — long = drop-off.
