# BUILD_KIT — record-replay LAUNCH (shared components & exact specs)

Each `compositions/segN.html` is a standalone HTML doc mirroring the structure of the exemplar
(the `youtube-longform` template's `compositions/seg1.html`). Brand/motion spec: `./DESIGN.md`. Canvas
**1920×1080**. Launch pace — **denser than the essay: a beat every ~1.5–2.5s.**

## 0. The through-line motifs (MUST be pixel-identical across every segment that uses them)
- **● REC dot** — pulsing orange dot + "REC" label. The signature. Appears seg1 (ignites), seg3 (arms).
- **RECORD → COMPILE → REPLAY spine** — a 3-node row; the *active* node lights orange. Introduced in
  seg2 (all draw on), then in seg3 node 1 is `.on`, seg4 node 2 is `.on`, seg5 node 3 is `.on`,
  seg6 all three `.on`. Copy the `.spine/.snode/.sarrow` CSS verbatim.
- **Orange payoff box** — one per segment, the "this is the point" stamp.

## 1. Segment skeleton (copy verbatim, swap `segN` + `DUR`)
```html
<!doctype html><html lang="en"><head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1920, height=1080" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  [data-composition-id="segN"]{ position:relative; width:1920px; height:1080px; overflow:hidden;
    font-family:"Inter","Helvetica Neue",Arial,sans-serif;
    /* BRAND:START */
    background:#0B0B0C; /* brand:canvas */
    color:#F4F2EE;      /* brand:text */
    --orange:#E85810;   /* brand:accent */
    --card:#141416;     /* brand:card */
    --muted:#8C8C94;    /* brand:muted */
    --line:#2A2A2E;     /* brand:hairline */
    --red:#E5484D;      /* brand:bad */
    --green:#3DD68C;    /* brand:good */
    /* BRAND:END */
  }
  [data-composition-id="segN"] .scene{ position:absolute; inset:0; width:1920px; height:1080px; overflow:hidden; opacity:0; }
  [data-composition-id="segN"] #FIRSTSCENE{ opacity:1; }   /* the t=0 scene is visible */
  [data-composition-id="segN"] .glow{ position:absolute; inset:0; background:radial-gradient(60% 50% at 50% 42%, rgba(232,88,16,0.10), transparent 70%); }
  [data-composition-id="segN"] .wrap{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:90px; }
  /* ...paste the component CSS you need from §3... */
  [data-composition-id="segN"] .bug{ position:absolute; right:46px; bottom:40px; height:34px; width:auto; opacity:0.55; z-index:50; }
</style></head><body>
  <div data-composition-id="segN" data-start="0" data-duration="DUR" data-width="1920" data-height="1080">
    <!-- scenes: each a full-frame .scene; first scene has the visible id -->
    <img class="bug" src="assets/videodb-logo.png" />
    <script>
      window.__timelines = window.__timelines || {};
      var R = '[data-composition-id="segN"] ';
      var tl = gsap.timeline({ paused:true });
      var XF = 0.5;
      function fadeIn(s,t){ tl.fromTo(R+s,{opacity:0,filter:'blur(16px)'},{opacity:1,filter:'blur(0px)',duration:XF,ease:'sine.inOut'},t); }
      function fadeOut(s,t){ tl.to(R+s,{opacity:0,filter:'blur(16px)',duration:XF,ease:'sine.inOut'},t); }
      function countUp(sel,from,to,dur,at,fmt){ var o={n:from};
        tl.to(o,{n:to,duration:dur,ease:'power2.out',onUpdate:function(){ var el=document.querySelector(R+sel); if(el) el.textContent=(fmt?fmt(Math.round(o.n)):Math.round(o.n)); }},at); }
      function typewrite(sel,str,dur,at){ var o={n:0};
        tl.to(o,{n:str.length,duration:dur,ease:'none',onUpdate:function(){ var el=document.querySelector(R+sel); if(el) el.textContent=str.slice(0,Math.round(o.n)); }},at); }
      function stamp(sel,at){ tl.from(R+sel,{opacity:0,scale:0.72,duration:0.36,ease:'back.out(1.6)'},at); }
      tl.from(R+'.bug',{opacity:0,duration:0.6},0.8);
      /* build timeline, anchored to the cue times in §4 */
      window.__timelines["segN"] = tl;
    </script>
  </div></body></html>
```

## 2. Hard rules (break these = real bugs)
- **Determinism only** — no `Math.random()`/`Date.now()`/`new Date()`. Loops use finite `repeat:N` (never `-1`).
- Build timeline **synchronously** — no `async`/`setTimeout`/Promise.
- All `.scene`s exist at t=0; the first scene is CSS `opacity:1`, the rest `opacity:0`. Reveal via `fadeIn` at the cue.
- **Crossfade, don't jump.** At cue T: `fadeOut(prevScene,T); fadeIn(newScene,T);` — new scene's child entrances start at `T+0.25`.
- **No exit animations except seg6's final scene.** The crossfade IS the exit.
- **Continuous motion:** something moves every ~2–3s in every scene (count-up, typewriter, row populate, pulse w/ finite repeat, slow push). No frozen holds.
- Only animate opacity/transform/color/filter. No emojis — use `✓ ✗ ● → ▸` or CSS/SVG.
- Fonts: only **"Archivo Black"** (display) + **"Inter"** (body) — they auto-embed. No `@font-face`/`@import`.
- One accent: `var(--orange)`. Never a second loud color. Headlines 60px+, body 22px+, labels 16px+. `font-variant-numeric:tabular-nums` on numbers/code.
- Position content with `.wrap` padding/flex — never `position:absolute;top:Npx` on a growing content container.

## 3. Shared components (COPY VERBATIM — these guarantee the through-line)
```css
/* ● REC dot + label */
[data-composition-id="segN"] .rec{ display:inline-flex; align-items:center; gap:16px; font-family:"Archivo Black",sans-serif;
  color:var(--orange); font-size:40px; letter-spacing:0.14em; text-shadow:0 2px 14px rgba(0,0,0,0.8); }
[data-composition-id="segN"] .rec .dot{ width:26px; height:26px; border-radius:50%; background:var(--orange); box-shadow:0 0 22px var(--orange); }

/* RECORD→COMPILE→REPLAY spine */
[data-composition-id="segN"] .spine{ display:inline-flex; align-items:center; gap:26px; }
[data-composition-id="segN"] .snode{ font-family:"Archivo Black",sans-serif; text-transform:uppercase; letter-spacing:0.03em;
  font-size:34px; padding:20px 30px; border-radius:14px; background:var(--card); border:1px solid var(--line); color:var(--muted); }
[data-composition-id="segN"] .snode.on{ color:#fff; border-color:var(--orange);
  box-shadow:0 0 0 2px rgba(232,88,16,0.4), 0 0 34px rgba(232,88,16,0.4); background:#1a1310; }
[data-composition-id="segN"] .sarrow{ color:var(--muted); font-size:40px; }

/* Callout boxes */
[data-composition-id="segN"] .box{ display:inline-block; background:#F4F2EE; color:#0B0B0C; font-family:"Archivo Black",sans-serif;
  text-transform:uppercase; letter-spacing:0.01em; line-height:0.98; padding:16px 26px; border-radius:12px; font-size:60px; box-shadow:0 14px 40px rgba(0,0,0,0.6); }
[data-composition-id="segN"] .box.pay{ background:var(--orange); color:#fff; box-shadow:0 16px 50px rgba(232,88,16,0.5); }
[data-composition-id="segN"] .box.red{ background:var(--red); color:#fff; }
[data-composition-id="segN"] .box.sm{ font-size:38px; padding:12px 18px; }

/* Card / chip */
[data-composition-id="segN"] .card{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:26px 30px; }
[data-composition-id="segN"] .chip{ display:inline-flex; align-items:center; gap:12px; background:var(--card); border:1px solid var(--line);
  border-radius:999px; padding:12px 24px; font-size:28px; font-weight:600; color:var(--txt,#F4F2EE); }
[data-composition-id="segN"] .chip .cd{ width:12px; height:12px; border-radius:50%; background:var(--orange); }

/* Big number */
[data-composition-id="segN"] .bignum{ font-family:"Archivo Black",sans-serif; color:var(--orange); font-size:200px; line-height:0.9; font-variant-numeric:tabular-nums; }

/* Code / log window (accessibility log, SKILL files) — monospace via ui-monospace stack (renders fine) */
[data-composition-id="segN"] .win{ background:#0e0e10; border:1px solid var(--line); border-radius:14px; overflow:hidden; box-shadow:0 24px 60px rgba(0,0,0,0.6); }
[data-composition-id="segN"] .win .bar{ display:flex; align-items:center; gap:10px; padding:14px 18px; background:#141416; border-bottom:1px solid var(--line); }
[data-composition-id="segN"] .win .bar .d{ width:13px; height:13px; border-radius:50%; background:#3a3a40; }
[data-composition-id="segN"] .win .bar .t{ margin-left:12px; font-size:20px; color:var(--muted); font-weight:600; }
[data-composition-id="segN"] .win .body{ padding:22px 26px; font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace; font-size:26px; line-height:1.7; }
[data-composition-id="segN"] .logrow{ display:flex; gap:14px; align-items:center; color:#cfcfd6; }
[data-composition-id="segN"] .logrow .k{ color:var(--orange); font-weight:700; } /* verb */
[data-composition-id="segN"] .var{ background:rgba(232,88,16,0.18); border:1px solid var(--orange); color:#ffd3b0; border-radius:8px; padding:2px 10px; }

/* self-heal UI button (seg5) */
[data-composition-id="segN"] .appwin{ width:760px; }
[data-composition-id="segN"] .btn{ display:inline-block; font-family:"Archivo Black",sans-serif; text-transform:uppercase; font-size:26px;
  padding:16px 30px; border-radius:10px; background:var(--orange); color:#fff; }
[data-composition-id="segN"] .ring{ position:absolute; border:3px solid var(--green); border-radius:12px; box-shadow:0 0 26px rgba(61,214,140,0.6); }

/* use-case tile (seg6) */
[data-composition-id="segN"] .tile{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:30px 28px; width:410px; }
[data-composition-id="segN"] .tile .h{ font-family:"Archivo Black",sans-serif; text-transform:uppercase; font-size:30px; letter-spacing:0.01em; }
[data-composition-id="segN"] .tile .g{ width:56px; height:56px; border-radius:12px; background:#1a1310; border:1px solid var(--orange);
  display:flex; align-items:center; justify-content:center; color:var(--orange); font-size:30px; margin-bottom:18px; }

/* marker underline (draw-on): <svg class="mk" viewBox="0 0 400 40"><path d="M8,26 C120,10 280,10 392,22"/></svg> */
[data-composition-id="segN"] .mk path{ fill:none; stroke:var(--orange); stroke-width:7; stroke-linecap:round; }
```
Helper to draw a marker/line: set pathLength then animate strokeDashoffset→0 (see chess exemplar `drawArrow`).

## 4. EXACT per-segment specs (durations + cue times, 0-based, from cues.json)

### seg1 — HOOK · DUR 19.16 (VO 18.56)
Scenes: **#s1a** fumble/fail (t0) → **#s1b** REC ignites (14.90) → **#s1c** pivot box (16.71).
- s1a (0.0): a mock app window (`.win`) with a form; a cursor (● or an SVG arrow) clicks the wrong
  field twice; a red `.box.red` "AGENT FAILED" stamps in ~2.5s; keep motion (cursor jitter/retry,
  a red ✗ pulse) through ~14s. This is the "agents fumble/forget" beat — it holds a while, so give
  it ambient life (cursor retries, a small "attempt 1… 2… 3…" counter ticking).
- s1b (14.90): fadeOut s1a; fadeIn s1b — the big **● REC** dot ignites center (scale-in + glow pulse, finite repeat).
- s1c (16.71): fadeOut s1b; fadeIn s1c — orange `.box.pay` **"JUST SHOW IT. ONCE."** punches in (stamp), small tag "the fix" above.

### seg2 — REVEAL · DUR 15.64 (VO 15.04)
Scenes: **#s2a** name reveal (t0) → **#s2b** spine draws on (11.41).
- s2a (0.0): center — small **● REC** dot, then product lockup **"RECORD & REPLAY"** (Archivo Black, ~120px)
  stamps in; a subline chip row "OPEN SOURCE" + "VIDEODB" fades in ~2s; hold with a soft glow pulse.
- s2b (11.41): fadeOut s2a; fadeIn s2b — the **RECORD → COMPILE → REPLAY** `.spine` draws in node by
  node (stagger ~0.25s each, arrows fade between). All nodes default (not `.on`) — this introduces the spine.

### seg3 — RECORD · DUR 19.08 (VO 18.48) · spine node 1 = RECORD `.on`
Scenes: **#s3a** rec arms (t0) → **#s3b** dual-capture split (4.59) → OS chips within s3b at (16.68).
- Put the spine at the TOP of every scene here with **RECORD `.on`** (small, `transform:scale(.62)` row).
- s3a (0.0): **● REC** dot arms (pulse); caption chip "do the task" ; a tiny cursor performs a click.
- s3b (4.59): fadeOut s3a; fadeIn s3b — two panels side by side:
  LEFT `.win` titled "ACCESSIBILITY LOG" — `.logrow`s TYPE IN one at a time (typewrite / staggered):
  `click ▸ Search`, `type ▸ "invoice"`, `press ▸ Enter` (verb in `.k` orange).
  RIGHT `.win` titled "SCREEN → VIDEODB" — a video-frame placeholder (a dark rect w/ a faux UI + a
  small pulsing ● REC in its corner) "streaming" (a scanline sweeps top→bottom, finite repeat).
  At ~11s stamp orange `.box.pay` **"PRECISION + PICTURE"** below.
- OS chips (16.68): three `.chip`s "Windows · macOS · Linux" stagger in at the bottom.

### seg4 — COMPILE · DUR 21.72 (VO 21.12) · spine node 2 = COMPILE `.on`
Scenes: **#s4a** log→compile→skill files (t0) → **#s4b** variable morph (16.54) → payoff (19.36).
- Spine at top, **COMPILE `.on`**.
- s4a (0.0): left a compact event-log `.win`; an orange arrow labeled "COMPILE" draws to the right;
  two artifact `.card`s appear: **`SKILL.json`** (show 3–4 structured lines: `"action":"click"`,
  `"target":"Search"`, …) and **`SKILL.md`** (show a readable step list "1. Open search  2. Type query …").
  Stagger the json lines populating. Small version tag `v2 ▸ v1 archived` fades in ~13s.
- s4b (16.54): a value inside the json (`"invoice"`) HIGHLIGHTS then morphs into an orange `.var`
  chip **`{{ query }}`** (scale/color tween). Keep both cards visible (don't fadeOut) — this is an
  in-scene change, so animate the value in place rather than a full crossfade.
- payoff (19.36): orange `.box.pay` **"ONE DEMO → A REUSABLE SKILL"** stamps in at the bottom.

### seg5 — REPLAY + SELF-HEAL · DUR 24.92 (VO 24.32) · spine node 3 = REPLAY `.on` (HERO)
Scenes: **#s5a** replay running (t0) → **#s5b** UI changes (7.84) → **#s5c** brittle ✗ (13.65) →
**#s5d** self-heal ✓ + payoff (19.80, payoff stamp at 23.35).
- Spine at top, **REPLAY `.on`**.
- s5a (0.0): an `.appwin` `.win` "CUSTOMER PORTAL"; replay steps check off ✓ one at a time (stagger),
  a `{{ query }}` field fills live via typewrite with "invoice".
- s5b (7.84): fadeOut s5a; fadeIn s5b — SAME app; narrate "a button moves": the **Submit `.btn`**
  visibly SLIDES from bottom-right to top-left (tween ~0.8s), a small "UI UPDATED" tag flashes.
- s5c (13.65): fadeOut s5b; fadeIn s5c — split: LEFT "BRITTLE SCRIPT" a `.win` that snaps a red
  `.box.red` **"✗ NOT FOUND"** (the button is gone from its coords); a red ✗ pulses.
- s5d (19.80): fadeOut s5c; fadeIn s5d — the app again; a green scanning `.ring` sweeps, LANDS on
  the moved Submit button, ✓ green check pops "MATCHED BY APPEARANCE". At **23.35** orange `.box.pay`
  **"THE UI CHANGED. IT DIDN'T CARE."** stamps. This is THE money frame — make it land hard.

### seg6 — USE CASES + CTA · DUR 25.16 (VO 24.56)
Scenes: **#s6a** 4-tile montage (t0) → **#s6b** payoff (15.85) → **#s6c** CTA (19.13, "to see" 23.13).
- s6a (0.0): a 2×2 grid of `.tile`s staggering in (~every 1.2s, matching the VO list), each with a
  `.g` glyph + `.h` title: **"AUTOMATE THE BORING"** (▸), **"DOCS THAT RUN"** (→), **"DRIVE LEGACY APPS"**
  (●), **"SURVIVES REDESIGNS"** (✓). Give each a tiny live motion (a mini progress bar / tick).
- s6b (15.85): fadeOut s6a; fadeIn s6b — orange `.box.pay` **"RECORD ONCE. REPLAY ANYWHERE."** big center;
  behind/above it the full **RECORD → COMPILE → REPLAY** spine with ALL THREE nodes `.on` (completing the motif).
- s6c (19.13): fadeOut s6b; fadeIn s6c — full VideoDB logo (use `assets/videodb-logo.png` at ~64px,
  NOT the small corner bug) + the ● REC dot; a single CTA line **"OPEN SOURCE · github.com/video-db/open-record-replay"**;
  at 23.13 the tagline **"TO SEE IS TO KNOW"** fades up under it. **This is the ONLY scene allowed an exit** (a gentle final fade is optional; holding is fine).

## 5. QA gate (I run centrally)
`npx hyperframes lint` (0 errors) · `validate` (ignore false-positive contrast on hidden scenes) ·
`inspect --samples 60` (0 errors) · extract frames at each cue and eyeball. Then draft render → HQ.
