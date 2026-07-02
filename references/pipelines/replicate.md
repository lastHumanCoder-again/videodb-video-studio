# Pipeline: replicate — watch a reference video, compile its style, replay it with new content

**Makes:** a REPLICATION.md style spec compiled from any example video, then a new video in that style through one of the other pipelines. **Use when:** the user shows a video ("make one like this", "copy this style/format", "our next video should look like X"). Sibling concept to VideoDB's open-record-replay: they record *actions* once and replay them anywhere; this watches a *video* once and replays its *style* with new content.

**Legal line (hard rule):** replicate style and structure — pacing, palette, motion grammar, layout system. NEVER copy assets, footage, copyrighted music, or verbatim script from the reference.

## Step 1 — Analyze the reference

```bash
python3 "$SKILL_DIR/scripts/analyze_reference.py" <video.mp4 | URL> [--out DIR]
```

Two layers:
- **ffmpeg (always, local, free):** `analysis.json` (dims/fps/duration/cut times/pacing), `frames/` (sampled stills — READ THESE), `palette.png`, `audio.mp3`.
- **VideoDB (optional, BYO `VIDEO_DB_API_KEY` + `pip install videodb`):** the vision layer — uploads the reference, returns `transcript.txt` (spoken words) and `videodb_scenes.json` (a design-oriented visual description per 5s window). **Uses account credits — get the user's explicit go-ahead before running with a key present.** A URL source (e.g. YouTube) requires this layer; local files work with ffmpeg alone.

## Step 2 — Compile REPLICATION.md

Read `analysis.json`, the frames (all of them), and if present the VideoDB scene descriptions + transcript. Write `REPLICATION.md` in the project with exactly these sections:

1. **Format** — aspect, fps, target duration, pacing (avg s/cut; where it accelerates; cuts in first 3s).
2. **Palette** — canvas / text / accent (+ secondary) as hex, from frames + palette.png. Map to brand tokens: this becomes a generated `brand.json` if the user wants the reference's colors, or the user's own brand if they want theirs.
3. **Typography** — case, weight contrast, approximate scale hierarchy, serif/sans character.
4. **Motion grammar** — what animates and how (crossfades vs hard cuts, type entrances, counters, kens-burns, karaoke captions), transition style + duration.
5. **Structural skeleton** — the beat sheet of the reference with timestamps (hook device → beats → payoff → CTA), from transcript + scenes. Describe each beat's *function*, not its content.
6. **Graphic system** — recurring elements: cards, lower thirds, logos/bugs and their placement, caption treatment, charts.
7. **Pipeline routing** — which of the six pipelines fits (see table below) + what the worked example must be bent toward.

Routing heuristics: 9:16 + burned captions + <60s → `instagram-short` · talking head docked with graphics zone → `split-ugc` · 16:9 narrated multi-beat → `youtube-longform` · product UI + launch arc → `demo-recording` · gameplay/footage with analysis overlays → `highlights` · none of these → build custom on the closest template and say so.

**Gate:** show REPLICATION.md to the user and get sign-off before building (this is the design gate for this pipeline).

## Step 3 — Replay with new content

1. If the user wants the reference's look: write its palette/fonts into a new `ref-brand.json` and scaffold with `--brand ref-brand.json`. If they want their own brand in the reference's *structure*: scaffold with their brand and keep only sections 1, 4–6.
2. `python3 "$SKILL_DIR/scripts/new_project.py" <routed-pipeline> <slug> [--brand ...]`
3. Build per that pipeline's reference doc, substituting the user's content into the structural skeleton — same beats, same pacing budget, new message.
4. Verify the replica against the spec: render a draft, extract frames at the reference's beat timestamps, compare side by side with `frames/`. Master rules: references/VIDEO_PLAYBOOK.md.

## Format-specific gotchas

- Animated/motion-graphics references crossfade instead of hard-cutting — both layers handle this (ffmpeg falls back to a 2.5s time grid; VideoDB uses time-based extraction) — but treat `n_cuts: 0` as "soft-transition style", itself a style fact worth recording.
- `analyze_reference.py` needs the `videodb` pip package only for the vision layer; everything else is stdlib + ffmpeg.
- VideoDB scene descriptions are per-window design breakdowns — trust them for layout/type/motion language, but pull exact hex values from the frames, not the prose.
- Keep the uploaded reference's `video_id` (recorded in videodb_scenes.json) — re-indexing with a different prompt is cheaper than re-uploading.
