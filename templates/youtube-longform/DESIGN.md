# DESIGN — VideoDB YouTube (LOCKED design gate)

Copy this file into each episode folder before writing any composition HTML. It fuses the
VideoDB brand (`knowledge-base/BRAND.md`) with the video-essay look (`knowledge-base/STYLE.md`).
Do not deviate without a reason written here.

## Format
- **1920×1080, 16:9, 24fps** (author/render HQ at this; reference is a downscaled copy).
- Long-form narrated explainer, target **3–5 min** (respect the runtime — tighter wins).

## Style Prompt (one paragraph)
A calm, technical tech video-essay on a near-black canvas. Real B-roll, 3D-style renders, and
crisp CSS/SVG architecture diagrams carry the visuals; every claim is stamped on screen in a
bold caps callout box; a single VideoDB-orange box marks the payoff of each beat; hand-drawn
marker arrows point at what's named; talking-head moments wear a heavy caps name label. One
accent color, confident motion, nothing static. Premium and restrained — energy comes from
movement and the orange, never from gradients or neon.

## Colors (one accent — orange)
- `#0B0B0C` — canvas (near-black, dominant)
- `#141416` — raised cards / surfaces
- `#E85810` — **VideoDB orange, THE accent**: payoff box, key numbers, active diagram node, marker underline, logo
- `#F4F2EE` — primary text (warm off-white)
- `#8C8C94` — secondary text / labels (AA on canvas)
- `#2A2A2E` — hairlines / borders / grid
- `#E5484D` — utility red (✗ / problem / frankenstack)
- `#3DD68C` — utility green (✓ / resolved)

## Typography
- **Archivo Black** — display: callout boxes, name labels, big numbers. UPPERCASE, tracking ~0.01em, line-height ~0.95. **Auto-embeds.**
- **Inter** (300/500/700) — body, captions, annotations, diagram labels. **Auto-embeds.**
- `font-variant-numeric: tabular-nums` on all numbers/counters.
- Headlines 60px+, body 20px+, data labels 16px+.
- ⚠️ Do NOT use Anton or an unverified mono — they silently fall back at render. Confirm any new
  font by extracting a frame from the actual MP4 (playbook §5), not by lint passing.

## Motion
- Smooth eases: `power3.out` / `expo.out` (headlines), `power2.out` (cards). Brief one-shot entrance pops OK (`back.out`) on small elements.
- **Callout boxes stamp in** ~0.25–0.4s; the orange payoff box lands a beat harder.
- **Numbers count up** to value (no blur-zoom).
- **Marker arrows draw on** (animate `stroke-dashoffset`→0) over ~0.4–0.6s, landing AT the cue word.
- Scene transitions: **blur-crossfade** ~0.55s. No jump cuts.
- **Continuous motion mandate:** something meaningful changes every ~2–3s — a value updates, an element reveals, a row populates, the board changes, a glow shifts. Entrance-then-hold is a bug.
- Every element animates IN (`gsap.from`); no exit animations except the final scene.

### Zoom & cinematic movement (use it — make it engaging)
- **Zoom is a tool, not banned.** A slow **push-in** (or pull-back) on a photo/hero shot adds energy and draws the eye — use it. Keep it **smooth and slow** (long ease, e.g. scale 1.0→1.08 over the whole scene) so it reads cinematic, not jittery. Pair big reveals with a confident **scale-in** (card/board/number punches in).
- The thing to avoid is **aimless** motion — a constant tiny wobble that means nothing, or a hold where nothing moves. Every move should have intent: reveal, emphasis, or following the narration.
- Still keep the **continuous-motion** rule: something meaningful changes every ~2–3s (a push-in + a count + a reveal can all run together). Combine zoom with content motion, glow, and position for a lively, premium feel.

## Real images (for beats, not just logos)
- **Use real images to ground narrative beats** — not only logos. When the script references a real event, person, place, or product ("in 1997 AI beat the world champion" → a real photo of the defeated grandmaster; "a camera on a shelf" → a real retail/CCTV shot; a real product UI, a real archive), **show a real photo**. It's far more credible and engaging than an abstract.
- Source via the **TinyFish API** (`TINYFISH_API_KEY` in the project `.env`): `GET https://api.search.tinyfish.ai?query=...` with header `X-API-Key` to find the source page (favor `commons.wikimedia.org` for reuse rights), then download via `Special:FilePath/<file>`. Frame on the dark canvas (dark border/vignette/veil for legibility), add a small credit when the licence needs it, and feel free to push-in for life.
- **When you name a real model/product, show its logo** — inline-SVG marks in the episode's `LOGOS.md` (OpenAI, Claude), rendered **white** next to the name; never the model's own brand color (orange stays VideoDB's).

## Brand bug
- Persistent small `videodb-logo.png` corner mark (low opacity) throughout.
- Full logo stamps in after the hook (open) and on the end/CTA card. Dark backgrounds only.

## Recurring motifs (pick and repeat for a through-line)
- **✗-frankenstack → ✓-one-backend flip** (the comparison-table / before-after — our most screenshot-able frame).
- Orange "payoff box" as the consistent "this is the point" stamp.
- The six-primitive pipeline as an animated spine.

## What NOT to do
- No second accent color. No purple/blue tech gradient, no neon, no glassmorphism.
- No two-sans pairing, no `#333`, no generic blue `#3b82f6`.
- No full-screen linear gradients on dark (H.264 banding) — solid + localized radial glow only.
- No static holds. No emojis in the capture engine (use CSS/SVG or `✓ ✗ ★ ▲ → ☏`).
- No fabricated named sources or fake posts — sourced or clearly representative only.
- Never place the logo on a light surface (the white "Video" vanishes).
- Determinism only: no `Math.random()` / `Date.now()` / `new Date()`; finite `repeat:N`.
