# Deck template — HTML slides → PDF / PNG

Hand-drawn-doodle slide deck (16:9 by default, any dimension via `--slide-w` / `--slide-h`).

1. Edit `slides.html` — one `.slide` div per slide (`dark` or `light` theme). Doodles are drawn by `doodles.js` into any `.art[data-art="<scene>"]` div; compose new scenes from the helpers in its registry.
2. `npm install`
3. Playwright launches your **system Chrome** (`channel: 'chrome'`). If Chrome isn't installed, run `npx playwright install chrome` (or change `channel` in render.js/shots.js to plain chromium after `npx playwright install chromium`).
4. `npm run render` → `out/deck.pdf` (one page per slide, size auto-detected). Custom I/O: `node render.js <input.html> <output.pdf>`.
5. `npm run shots` → `out/shots/slide-01.png …` at 2x. Custom: `node shots.js <input.html> <outDir> [prefix]`.

Brand palette lives in `deck.css` between `/* BRAND:START */ … /* BRAND:END */` — retarget the annotated `brand:*` tokens to reskin. Fonts are local woff2 (Archivo, Caveat, Space Mono); rough.js is vendored in `vendor/`.
