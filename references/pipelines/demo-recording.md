# Pipeline: demo-recording — product launch video + screen-capture stack

**Makes:** a 1920×1080 · 24fps · ~2min product launch/reveal video (hook → reveal → demo → value → use cases → CTA), optionally built around real screen recordings captured with the bundled Playwright stack. **Use when:** the user asks for a launch video, product demo video, feature reveal, or screen-recording-driven promo.

Master rules: `references/VIDEO_PLAYBOOK.md` — sync, determinism, design gate, QA all apply in full.

## Worked example anatomy (`templates/demo-recording/`)

```
index.html            root: 6 segment clips + 6 VO clips (alternating tracks, 0.6s gaps)
compositions/seg1-6   one <template> sub-composition per narrative beat (~125s total)
BUILD_KIT.md          THE build spec — read before touching any segment:
                      segment skeleton, shared component CSS (● REC dot, RECORD→COMPILE→REPLAY
                      spine, callout boxes, code/app windows, tiles), helper functions
                      (fadeIn/fadeOut/countUp/typewrite/stamp), per-segment cue specs
DESIGN.md, SCRIPT.md  visual/motion spec + full narration script
cues.json             extracted cue times (regenerate per new VO)
voiceover/            6 mp3s + word-level transcripts + segments.json + cues_spec.json
repo/                 the capture stack (below) — reusable, independent of the video
```

## The capture stack (`repo/`)

A Playwright-driven recorder that captures a product demo as both a **screen stream** and an **accessibility action log** (every click/type/press):

- `run_demo.py` — orchestrates the demo flow (drives the app, triggers capture)
- `server.py` — FastAPI server the demo talks to
- `capture/recorder.py`, `capture_client.py`, `ax_client.py` — screen recording + AX log capture (+ `native/` per-OS hooks)
- Setup: `cd repo && pip install -e .` (or `uv sync`), then `python run_demo.py --help`

Use it to record real product footage, then embed the clips in segments (framework-owned media playback, alternating tracks). For a different product, rewrite the flow in `run_demo.py` against your own app/server.

## Build workflow

1. Scaffold: `python3 "$SKILL_DIR/scripts/new_project.py" demo-recording <slug>` → `npm install`.
2. Read `BUILD_KIT.md` end-to-end. New launch videos keep its skeleton and shared components — that's what makes segments consistent.
3. Write `SCRIPT.md`: one segment per narrative beat (hook / product reveal / demo beat(s) / value / CTA). Keep a through-line motif (the worked example uses the ● REC dot + a 3-node progress spine — invent an equivalent for your product).
4. (Optional) capture real product footage with `repo/`.
5. VO: `voiceover/segments.json` → `"$SKILL_DIR/scripts/tts.py"` (BYO key / prompt-only fallback) → `npx hyperframes transcribe` each mp3 → `voiceover/cues_spec.json` → `"$SKILL_DIR/scripts/extract_cues.py"`.
6. Rebuild `compositions/segN.html` from the BUILD_KIT skeleton, anchored to your cues. One orange payoff box per segment; no exit animations except the final scene.
7. Assemble root, QA (`inspect --samples 60`), draft render, frame eyeball, HQ.

## Format-specific gotchas

- Segment durations = VO duration + 0.6s gap; the video clip holds through the gap, the audio clip is natural length.
- The BUILD_KIT's shared CSS is duplicated into each segN.html (sub-compositions are scoped) — change a shared component in ALL segments or drift shows.
- `repo/.env.example` lists the capture stack's own config (placeholders only) — it is unrelated to the skill's workspace/.env keys.
- Real screen recordings: trim/speed-ramp with ffmpeg BEFORE embedding; don't try to retime video inside the composition.
