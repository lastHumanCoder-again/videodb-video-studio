---
name: videodb-video-studio
description: "Umbrella video-production studio packaging 6 HyperFrames pipelines, VideoDB-branded by default: (1) YouTube long-form explainer / video essay 3-5min 1920x1080, (2) Instagram short / reel 15-60s 1080x1920 with karaoke captions, (3) split-screen UGC talking-head 9:16 with animated cards, (4) HTML slide deck to PDF/PNG with hand-drawn art, (5) product demo / launch video with Playwright screen capture, (6) highlights reel repurposing. Router skill: state your intent and it loads the matching playbook and scaffolds a full worked example. BYO-key optional (ElevenLabs TTS, Kie.ai images) — everything scaffolds and renders with zero keys. Triggers: make a short, instagram reel, vertical video, youtube explainer, long-form video, video essay, split screen, ugc video, talking head video, slide deck, carousel, launch video, demo recording, product demo video, highlights reel, karaoke captions, VideoDB video, rebrand a video template."
---

# VideoDB Video Studio

Six production-tested video pipelines behind one router. Each template is a **full worked example** — a real finished video that renders as-is with zero API keys — plus a playbook that tells you exactly how to build a new one like it.

## STEP -1 — HARD RULES (these override everything else)

1. **Sync is sacred.** NEVER estimate intra-segment timings. Always: `npx hyperframes transcribe <seg>.mp3` for every VO clip → `extract_cues.py` → anchor every scene transition to real cue times. A visual that leads the voice is the amateur tell.
2. **Design gate.** Never write composition HTML before the project's `DESIGN.md` exists and is confirmed with the user. The scaffold copies one — adapt it first.
3. **Never auto-run paid generation.** `tts.py` and `gen_image.py` with keys present are paid API calls. Explicit user confirmation required in the current turn, every time; approval does not carry across jobs.
4. **No-key is not an error.** Missing key → the scripts print a paste-ready prompt-only fallback and exit 0. Relay the fallback to the user and continue; never block, never invent keys.
5. **Determinism.** No `Math.random()`, `Date.now()`, `new Date()`. Finite repeats only. Build timelines synchronously. `class="clip"` + `data-*` timing attributes on every timed element. Alternate adjacent video clips between track indices; audio on its own track.
6. **Continuous motion.** Something visible changes every 2–3s, depicting what's being spoken. "Entrance then hold" is the failure mode.
7. **Look at the render, not the lint.** Extract frames with ffmpeg and eyeball fonts/layout before declaring anything done.
8. **Scaffold only via `new_project.py`.** Hand-copied templates drift (stale slugs, stale brand blocks).

## Script locations

Set once per session: `SKILL_DIR="$HOME/.claude/skills/videodb-video-studio"` (adjust if installed elsewhere — this file's directory).

| Action | Command |
|---|---|
| First-time setup | `python3 "$SKILL_DIR/scripts/setup.py"` |
| Key/prereq status | `python3 "$SKILL_DIR/scripts/check_env.py"` |
| New project | `python3 "$SKILL_DIR/scripts/new_project.py" <pipeline> <slug> [--dir …] [--brand …]` |
| Voiceover (BYO key) | `python3 "$SKILL_DIR/scripts/tts.py"` (run in project root; reads `voiceover/segments.json`) |
| Cue extraction | `python3 "$SKILL_DIR/scripts/extract_cues.py"` (run in project root) |
| AI image (BYO key) | `python3 "$SKILL_DIR/scripts/gen_image.py" out.png 16:9 "prompt"` |

## STEP 0 — Setup gate

Before the first scaffold, check `"$SKILL_DIR/workspace/config.json"`. Missing → run `setup.py` (interactive; or `--projects-dir <path> --brand <path> --yes`). It records the projects directory and brand config, reports optional-key status, and checks prerequisites (node ≥ 18, python3, ffmpeg) without blocking. Never edit `config.json` by hand — re-run setup.

## STEP 1 — Route the intent

| User says (any of) | Pipeline | Canvas · fps | Typical length |
|---|---|---|---|
| youtube video, explainer, video essay, long-form | `youtube-longform` | 1920×1080 · 24 | 3–5 min |
| instagram short, reel, vertical short, tiktok, karaoke captions | `instagram-short` | 1080×1920 · 30 | 15–60 s |
| split screen, ugc, talking head + cards, creator video | `split-ugc` | 1080×1920 · 30 | ~40 s |
| deck, slides, pdf, carousel, presentation | `deck` | 16:9 slides | n/a |
| launch video, demo video, screen recording, product demo | `demo-recording` | 1920×1080 · 24 | ~2 min |
| highlights, repurpose, clips reel | `highlights` | 1080×1920 · 30 | ~25 s |

Then read **only** `references/pipelines/<pipeline>.md` plus `references/VIDEO_PLAYBOOK.md` (the master methodology). Do not load the other five pipeline docs. Ambiguous intent → ask ONE question (e.g. "vertical for IG or horizontal for YouTube?").

## STEP 2 — Scaffold

```bash
python3 "$SKILL_DIR/scripts/new_project.py" <pipeline> <slug>
```

Copies the full worked example, re-slugs the composition id (grep-verified), rewrites BRAND-annotated colors from the configured `brand.json`, prints the pipeline's next steps. The worked example is the exemplar: study its structure, then replace its content with the new video's — don't start from a blank file.

**Rebranding:** all brand tokens live in `brand.json` (colors, fonts, logo). A custom brand: `--brand path/to/other-brand.json`. Templates carry `BRAND:START/END` annotated blocks; only annotated values are rewritten.

## STEP 3 — The build loop (per project)

Follow `references/VIDEO_PLAYBOOK.md` §1 in order: script → voiceover → **transcribe** → **extract cues** → design gate → build segments → images → assemble → QA → render. The pipeline reference doc holds the format-specific rules (safe zones, caption bands, card schemas, capture stack usage).

VO and images honor the BYO-key contract (Hard Rules 3–4): with keys, confirm then generate; without, deliver the printed prompt blocks to the user and tell them where to drop the files.

## STEP 4 — QA & render

```bash
npx hyperframes lint && npx hyperframes validate && npx hyperframes inspect --samples 60
npx hyperframes render -o out.mp4 --quality draft     # iterate on draft
ffmpeg -ss <t> -i out.mp4 -frames:v 1 frame.png -y    # eyeball frames (Hard Rule 7)
npx hyperframes render -o out_HQ.mp4 --quality high   # final master only when frames look right
```

Contrast warnings from `validate` are often false positives (it samples fixed timestamps) — verify the element is actually visible at that time before chasing it.

## Error handling

| Symptom | Fix |
|---|---|
| `new_project.py` "RE-SLUG INCOMPLETE" | Report the leftover files; likely a binary/renamed file — fix template, don't hand-patch the project |
| `extract_cues.py` "NOT FOUND" cues | The phrase isn't in the transcript verbatim — reword the phrase in `cues_spec.json`; never type a number by hand |
| Font renders as generic sans in MP4 | Font isn't in HyperFrames' auto-embed set (Inter/Archivo Black are; Anton is NOT). Switch fonts; verify with a frame extract |
| `overlapping_clips_same_track` | Floating-point trap — alternate `data-track-index` between adjacent clips |
| tts/gen_image prints "[no key]" | Working as designed — hand the printed prompts to the user, files go in the stated paths |
| Kie API 403 on POST | Expected with urllib — the script already shells out to curl; if it still 403s, key is invalid |

## Example session

> **User:** make me an instagram short about semantic video search
> 1. Check `workspace/config.json` → missing → run `setup.py` (user skips keys — fine).
> 2. Route: "instagram short" → `instagram-short`. Read `references/pipelines/instagram-short.md` + `references/VIDEO_PLAYBOOK.md`.
> 3. `new_project.py instagram-short semantic-search` → project scaffolded, brand applied.
> 4. Confirm DESIGN.md + script beats with the user (design gate).
> 5. Write `voiceover/segments.json`; no key → `tts.py` prints the VO lines; user drops MP3s in.
> 6. `npx hyperframes transcribe` each MP3 → `extract_cues.py` → build scenes on real cues.
> 7. lint/validate/inspect → draft render → extract frames, eyeball → HQ render.
