# STYLE — The VideoDB video-essay look

This is the single most important doc for *appearance*. We are replicating the style of the
reference video (`videoplayback (34).mp4`, 16:9, ~5:26, 24fps) — a **polished tech
video-essay / documentary explainer**. See `reference/REFERENCE-VIDEO.md` and the frames in
`reference/frames/` for the receipts.

> One sentence: **a black-canvas explainer where every claim is stamped on screen in a bold
> caps callout, pointed at with a hand-drawn marker arrow, while real B-roll, 3D renders, and
> annotated diagrams carry the visuals — and one orange accent (VideoDB `#E85810`) ties it to
> the brand.**

---

## The five visual signatures (these ARE the style)

1. **The bold caps callout box.** Short keyword phrases in a **heavy condensed/mono caps**
   face, stacked one per line, each in its own pill/rounded rectangle. In the reference these
   are white box / black text (e.g. `SOUNDWAVES` · `WATER` · `60 SECONDS`) and lower-third
   name labels (`DAVID HOLZ`). **For us: invert to brand —** off-white box with near-black
   text for neutral facts, and a **VideoDB-orange box with white text** for the punchline of
   each beat (the orange box is the "this is the point" stamp). They pop in, never just appear.

2. **Hand-drawn marker annotations.** A rough white/orange **marker arrow** curving from a
   label to the thing it names; occasionally a hand-drawn circle or underline. This is the
   glue that says "look here." Draw it ON (animate the stroke), don't fade it in. In
   HyperFrames: an inline SVG `<path>` with `stroke-dasharray`/`stroke-dashoffset` animated to
   0 (a marker-sweep). Keep it loose and imperfect — not a clean vector arrow.

3. **Talking-head / B-roll with a name label.** Real or AI footage of a person, with a bold
   caps lower-third label set off to the side. Documentary, slightly imperfect, warm grade.
   For VideoDB: founders, engineers, customers, or representative operators (label them
   truthfully — see PLAYBOOK §10, never fabricate a named source).

4. **3D renders + annotated technical diagrams.** The reference leans hard on CGI machine
   renders and labeled schematics (callout lines to parts). For VideoDB this is our natural
   home turf: **render the architecture** — the frankenstack vs the one backend, the six
   primitives, ingest→index→memory→search→edit→stream as a pipeline diagram, a query hitting a
   petabyte archive and a clip materialising. Build these as **CSS/SVG you control**, not AI
   images (sharper, on-brand, editable). Animate the data moving through them.

5. **AI / abstract imagery for the "big idea" beats.** Atmospheric AI shots (the glowing head,
   cosmic fields) for conceptual moments — "machines as a second viewer," "video as memory."
   Use sparingly, for the hook and the turn, not as wallpaper.

---

## Pacing & motion (matches §6 of the playbook)

- **Black/near-black background** dominant. Content floats on it; let it breathe.
- **Cut/transition rhythm is brisk** — a new visual idea every few seconds; within a held shot,
  something still moves (a counter ticks, the arrow draws, a label stamps in, a diagram fills).
  *Entrance-then-hold is the failure mode.*
- **Blur-crossfade** between scenes (warm, forgiving); reserve a punchier transition for the
  hero reveal. No jump cuts.
- **Callouts stamp, they don't slide far.** Pop-in with a slight overshoot (`back.out(1.4)`),
  ~0.25–0.4s. The orange "point" box can land a beat harder than neutral boxes.
- **Numbers count up.** `10×`, `100×`, `~120ms`, `82%`, `5 min` — animate from 0/blur to value.
  `font-variant-numeric: tabular-nums`.
- **Marker arrows draw on** over ~0.4–0.6s, landing AT the cue word, never before.

---

## Typography

- **Display (callout boxes, labels, big numbers):** a **heavy caps** face. The reference reads
  as a bold mono/condensed grotesque. Use **Archivo Black** — it auto-embeds in HyperFrames and
  gives the chunky, confident stamp we want. For the mono-flavoured label variant, a mono is
  attractive but **verify embedding in the render** (see playbook §5; Anton silently falls
  back). Default to Archivo Black until a mono is proven in an extracted frame.
- **Body / captions / annotations:** **Inter** (300 vs 700 for weight contrast). Auto-embeds.
- All callout text **UPPERCASE**, tight letter-spacing, tight line-height (~0.95).

## Color (full kit in BRAND.md)

- Canvas near-black `#0B0B0C`; text off-white `#F4F2EE`; secondary gray `#8C8C94`.
- **One accent: VideoDB orange `#E85810`** — the "point" box, key numbers, the active node in a
  diagram, the marker arrow when it underlines the payoff. **Resist a second accent.**
- Utility only: red `#E5484D` for ✗/problem (the frankenstack), green `#3DD68C` for ✓/resolved.
- The brand logo bug (orange ▼ + Video + DB) sits as a small persistent corner mark, or stamps
  in full at the open and the close.

## What NOT to do

- No generic tech-startup gradient (purple/blue), no neon, no glassmorphism. VideoDB reads
  **calm + technical**; the energy comes from motion and the orange, not from effects.
- No two-sans pairing, no `#333`, no generic `#3b82f6` blue.
- No static holds; no full-screen linear gradients on dark (H.264 banding — use solid + a
  localized radial glow).
- No emojis in the capture engine — use CSS/SVG shapes or safe glyphs (`✓ ✗ ★ ▲ → ☏`).
- Don't fabricate named talking-head sources or fake review posts. Sourced or clearly
  representative only.
- Don't let a callout/diagram lead the voice. It lands AT or just after the cue word.
