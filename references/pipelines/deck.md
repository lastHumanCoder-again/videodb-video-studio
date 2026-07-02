# Pipeline: deck — HTML slides → PDF + PNGs with hand-drawn art

**Makes:** a designed slide deck (16:9 by default) rendered from HTML to PDF and per-slide PNGs, with procedural hand-drawn illustrations (rough.js). **Use when:** the user asks for a deck, slides, presentation, PDF, or social carousel. This is the one pipeline that outputs documents, not video.

## Worked example anatomy (`templates/deck/`)

```
slides.html        the VideoDB deck — each <section class="slide"> is one slide
deck.css           all styling; BRAND:START/END block carries the brand tokens
doodles.js         rough.js scene library — <div class="art" data-art="<scene>" data-w data-h>
render.js          Playwright: node render.js [input.html] [output.pdf]
shots.js           Playwright: node shots.js <input.html> <outDir> [prefix] — one PNG per slide
fonts/             Archivo 800/900, Caveat 500/600, SpaceMono 400/700 (woff2, local)
vendor/rough.js    hand-drawn rendering lib
TEMPLATE_NOTES.md  quick usage notes
```

## Workflow

1. Scaffold: `python3 "$SKILL_DIR/scripts/new_project.py" deck <slug>`
2. `npm install && npx playwright install chrome` — the scripts launch **system Chrome** (`channel:'chrome'`), so install the `chrome` channel, not chromium, if launch fails.
3. Edit `slides.html`: duplicate a `<section class="slide">`, keep the grid/typography classes from existing slides. Doodle art: point `data-art` at a scene name defined in `doodles.js` (generic scenes: problem, insight, driver, payoff, recipe, scale, loop, reticle...). Scenes draw on page load and signal `data-doodles-ready` — the render scripts wait for it.
4. `npm run render` → `out/deck.pdf`; `npm run shots` → `out/shots/slide-N.png`.
5. New illustration: add a scene case to `doodles.js` reusing its helpers (gear, robot, arrows, boxes). Keep the sketchy single-color style — the hand-drawn look IS the brand.

## Format-specific gotchas

- Different aspect (e.g. IG 4:5 carousel): change the slide dimensions in `deck.css`; `render.js`/`shots.js` auto-detect slide size.
- Fonts are local woff2 loaded via `@font-face` in deck.css — this works here (Playwright page render), unlike HyperFrames video renders which only embed their curated font list.
- PNGs export at 2x for legibility; that's intended for social carousels.
- No voiceover, no cues, no HyperFrames — the master VIDEO_PLAYBOOK loop does not apply to this pipeline; only the design-gate and brand rules do.
