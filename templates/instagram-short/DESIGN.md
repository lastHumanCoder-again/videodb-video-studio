# DESIGN — VideoDB Instagram Shorts (LOCKED design gate)

Copy this file into each short's folder before writing any composition HTML. It is the
**9:16 vertical** sibling of [`../DESIGN.md`](../DESIGN.md) — same brand, same motion language,
re-laid-out for a phone held vertically and watched **with the sound off**. Do not deviate
without a reason written here.

## Format
- **1080×1920, 9:16, 30fps.** (Long-form is 1920×1080 / 24fps — this track is vertical + a touch
  snappier.)
- Short-form, target **15–40s** (hard ceiling ~60s). One idea per short. Tighter always wins.
- **Loop-aware:** the last frame should sit comfortably next to the first (IG auto-loops).

## The safe zone (non-negotiable for vertical)
IG/Reels overlays chrome on top of the video. Keep anything that must be read inside the center.
```
1080 × 1920 canvas
├── top    ~0–220px   : risky (status bar / "Reels" tab) — bug + ambient only, no key text
├── center ~220–1500px: SAFE — all callouts, diagrams, numbers, the payoff stamp live here
└── bottom ~1500–1920 : BLOCKED — username, caption, like/share/comment rail sit here
                         → keep this clear; our burned-in captions ride ABOVE it (~1320–1460)
```
Design the readable content into a **~1080×1280 center band**. Treat top/bottom as bleed.

## Sound-off first (the biggest delta from long-form)
~85% watch muted. The video must land the whole point with **no audio**.
- **Burned-in karaoke captions are mandatory** (long-form treats them as optional — here they're
  the spine). Word-or-phrase level, synced to the VO transcript, riding the caption band
  (~y1320–1460), inside the safe zone, never over the bottom UI.
- Every claim is **also** stamped as an on-screen callout — the caption and the stamp reinforce
  each other. A viewer who reads nothing but the big stamps still gets the argument.
- VO is the polish layer, not the carrier. If muted, nothing essential is lost.

## Colors (identical to brand — one accent)
- `#0B0B0C` canvas · `#141416` cards · **`#E85810` VideoDB orange (THE accent)** ·
  `#F4F2EE` text · `#8C8C94` secondary · `#2A2A2E` hairline · `#E5484D` ✗ · `#3DD68C` ✓.
- Orange is the entire energy budget — payoff stamp, key numbers, active node, marker underline,
  active caption word, logo. Resist a second color; add motion instead.

## Typography (bigger — it's a phone)
- **Archivo Black** — display: callout stamps, big numbers, name labels. UPPERCASE, tracking
  ~0.01em, line-height ~0.92. **Auto-embeds.**
- **Inter** (400/700) — captions, annotations, diagram labels. **Auto-embeds.**
- Vertical sizes (read at arm's length on a 6" screen): **hero stamp 110–150px**, headline 72px+,
  caption 52–64px (700), data label 28px+. `font-variant-numeric: tabular-nums` on all numbers.
- ⚠️ No Anton / unverified mono — silent fallback at render. Confirm any new font by extracting an
  MP4 frame, not by lint.

## Motion (snappier than long-form, never static)
- Eases: `power3.out` / `expo.out` (hero/number), `power2.out` (cards), `back.out(1.6)` on stamp pops.
- **Callout stamps pop ~0.2–0.35s** (faster than the 0.25–0.4 of long-form); the orange payoff box
  lands a beat harder with a small overshoot.
- **Numbers count up** to value. **Marker arrows draw on** (`stroke-dashoffset`→0) ~0.35–0.5s,
  landing AT the cue word.
- Scene transitions: **blur-crossfade ~0.4s** (tighter). No jump cuts.
- **Continuous-motion mandate is stricter for shorts:** something meaningful changes every
  **~1.5–2.5s** (in long-form it's 2–3s). The thumb is on the scroll — earn every frame.
- A slow **push-in** on a hero/photo is encouraged (scale 1.0→1.06 over the scene) for life — but
  intentional, never aimless wobble.

## The hook (first ~1 second — even harder than long-form's 3s)
- Cold-open the strongest concrete thing: a shocking number, a real quote, the villain. **No logo
  open, no slow wind-up.** The first frame must already be the hook.
- The bug appears immediately (small corner); the full logo stamp is reserved for the **end/CTA**
  card only (vertical has no time for an open stamp).

## Brand bug & CTA
- Persistent small `videodb-logo.png` corner mark, low opacity, top-left (top-left is safer than
  bottom in vertical — bottom is the UI rail). Keep it out of the very top status-bar strip.
- End card: full logo stamp + **one** CTA + house line **"To see is to know."** Dark bg only.

## Recurring motifs (pick one, repeat — gives the short a spine in 30s)
- **✗-frankenstack → ✓-one-backend flip** — compresses beautifully into a vertical before/after.
- Orange "payoff box" as the consistent "this is the point" stamp.
- The six-primitive pipeline as a **vertical** animated spine (stack top→bottom, not left→right).

## What NOT to do
- No second accent. No purple/blue tech gradient, neon, or glassmorphism.
- No key text in the top ~220px or bottom ~420px (IG chrome eats it).
- No two-sans pairing, no `#333`, no generic blue `#3b82f6`.
- No full-screen linear gradients on dark (H.264 banding) — solid + localized radial glow only.
- No static holds. No emojis in the capture engine (use CSS/SVG or `✓ ✗ ★ ▲ → ☏`).
- No fabricated named sources or fake posts — sourced or clearly representative only.
- Never place the logo on a light surface (white "Video" vanishes).
- Determinism only: no `Math.random()` / `Date.now()` / `new Date()`; finite `repeat:N`.
