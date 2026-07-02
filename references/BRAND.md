# BRAND — VideoDB

Source: [videodb.io](https://www.videodb.io/) (dark-mode site, confirmed June 2026) + the
brand logo. This is the brand layer; the *motion/appearance* spec is in `STYLE.md`.

## The logo

`assets/videodb-logo.png` — wordmark: an **orange downward triangle ▼** (a play-mark tipped
down) + **"Video"** in white + **"DB"** in orange. Designed for **dark backgrounds** — the
white "Video" disappears on white, so **never place it on a light surface.**

- Persistent small **corner bug** (bottom-right or top-left), low opacity, throughout.
- Full-size **stamp-in** at the open (after the hook) and on the end/CTA card.
- Keep clear space ≥ the triangle's width around it. Don't recolor, stretch, or add effects.

## Color

| Role | Hex | Use |
|------|-----|-----|
| Accent (THE color) | `#E85810` | VideoDB orange. The "point" box, key numbers, active diagram node, marker underline, logo. **The only loud color.** |
| Canvas | `#0B0B0C` | Near-black background (dominant). |
| Canvas alt | `#141416` | Cards / raised surfaces on the canvas. |
| Text primary | `#F4F2EE` | Warm off-white — body, captions. |
| Text secondary | `#8C8C94` | Muted gray — labels, secondary data (passes AA on canvas). |
| Hairline | `#2A2A2E` | Borders, grid lines, dividers. |
| ✗ / problem | `#E5484D` | Utility red — the frankenstack, "before," failure. |
| ✓ / resolved | `#3DD68C` | Utility green — "after," confirmation. |

> Orange is the whole energy budget. If you feel the urge to add a second brand color, add
> motion instead.

## Typography

- **Display:** **Archivo Black** — heavy caps for callout boxes, name labels, big numbers.
  Auto-embeds in HyperFrames (Anton does NOT — see playbook §5). Uppercase, tight tracking.
- **Body:** **Inter** (300 / 500 / 700) — captions, annotations, diagram labels. Auto-embeds.
- `font-variant-numeric: tabular-nums` on every number column / counter.

## Voice & copy (for scripts and on-screen text)

VideoDB is **calm, technical, partnership-first** — confident, not hypey. Mirror that:

- **Tagline / sign-off:** **"To see is to know."** (from Sanskrit *vid* — to see, to know.)
- **Headline positioning:** *"Data infrastructure for video, built for machines and agents."*
- **The hook idea:** *"Video has a second user now: machines."*
- **On-screen text is short stamps** — the keyword, the number, the verdict — never the full
  narrated sentence (the VO carries the words; the screen carries the proof). See PLAYBOOK §2.
- Lowercase, precise, declarative. Avoid exclamation marks, "revolutionary," "game-changer,"
  emoji. Let the numbers and the architecture do the talking.

## The numbers that are on-brand to stamp (verify current before use)

- `82%` of internet traffic is video
- `10×` lower total cost (replaces 10+ vendors)
- `100×` faster video retrieval (~`120ms` across petabyte archives)
- `5 min` to first query / to production
- `1` API across cloud, VPC, edge · `∞` agent queries per video

> These move. Re-check against videodb.io / PRODUCT.md before putting a figure on screen, and
> spell prices/numbers out in the VO script so ElevenLabs reads them correctly (playbook §3).
