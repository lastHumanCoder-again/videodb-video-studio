# REPLICATION.md — "read the game" (from the Iniesta editorial concept short)

Reference: 14.0s · 1080×1920 · 30fps · NO audio track · 2 hard cuts (avg 4.7s/scene).
Compiled from ffmpeg analysis + VideoDB scene index (video m-z-019f239c-4f09-7ae3-b3c2-e58a3cf79ad6).

## 1. Format
- 1080×1920 · 30fps · exactly 14.0s · 3 scenes: ~0–4.7 / 4.7–9.3 / 9.3–14.0
- HARD CUTS between scenes (no crossfades) — this reference cuts, unlike our house style
- Inside each scene: one slow continuous camera move (gentle push-in / drift), objects settle with tiny physical easing

## 2. Palette (monochrome — deliberate exception to house orange-on-dark)
- Scene 1: paper gray canvas `#C9C6C0` with mottled texture, vignette darker at edges
- Scene 2: pale bone surface `#D6D3CE`, near-white; soft contact shadow under object
- Scene 3: near-black felt `#111110` with film grain, pale spotlight `#E5E2DC`
- Text: near-black `#1A1A1A` on light scenes; off-white `#EDEBE6` on dark
- Single brand accent (`#E85810`) appears ONCE: the VideoDB lockup at the very end

## 3. Typography
- Editorial mixed-scale pairing: small light UPPERCASE kicker ("not only his") directly above a huge bold lowercase word ("space") — weight contrast ~300 vs 900, scale contrast ~1:4
- Centered, tight leading, sits inside/above the spotlight beam

## 4. Motion grammar
- Museum-display staging: ONE object per scene, dead center, huge negative space
- Slow zoom/push (scale 1.0→1.06 over full scene), object micro-rotation or settle
- Scene 3: spotlight beam (narrow trapezoid from top-right) REVEALS the type, then the beam narrows onto the object
- Film grain + vignette on every scene (CSS noise overlay, finite animation)
- Focus-pull feel on cuts: incoming scene starts 8px blurred for 0.3s

## 5. Structural skeleton (function per beat)
| Ref beat | Ref content | Our content |
|---|---|---|
| S1: the surface subject | player photo in halftone octagon card | match frame in halftone octagon card — "everyone sees the game" |
| S2: the organ of perception | eyeball on pale pedestal | eye macro — "watching is easy" |
| S3: the real instrument + payoff | brain under spotlight on pitch, "not only his space" | brain on pitch under beam, "not only the pixels" / "moments" → VideoDB lockup |

## 6. Graphic system
- Halftone/engraving filter on the S1 photo card (CSS: grayscale + contrast + dot pattern overlay), octagonal clip-path, hairline border
- S3 background: ghosted top-down football-pitch line graphics (SVG, ~8% opacity)
- Circular pale platform under the hero object; faint diagonal hairline through frame
- End lockup: VideoDB logo + "agents that read the game" — the only color in the video

## 7. Routing
Pipeline `instagram-short` (9:16 · 30fps), custom monochrome styling per this spec.
Assets (rights-clean): assets/brain-bw.jpg (Wikimedia Commons, B/W lateral brain), assets/eye-bw.jpg (Commons macro eye, desaturated; credit: "Eye (11774111985).jpg"), assets/match-bw.jpg (own asset). No reference footage or assets reused.
No VO (reference has none) — silent, caption-carried, like the reference.
