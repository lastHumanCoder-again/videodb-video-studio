# BUILD_KIT — vlms-not-llms (shared components & rules)

Every segment `compositions/segN.html` is a standalone HTML doc that mirrors the structure and
components below. `compositions/seg1.html` is the canonical exemplar — mirror it. Brand/motion
spec: `DESIGN.md`. Canvas is **1920×1080**.

## 1. Segment file skeleton (copy verbatim, swap `segN`)

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  [data-composition-id="segN"]{
    position:relative; width:1920px; height:1080px; overflow:hidden;
    background:#0B0B0C; color:#F4F2EE;
    font-family:"Inter","Helvetica Neue",Arial,sans-serif;
    --orange:#E85810; --canvas:#0B0B0C; --card:#141416; --txt:#F4F2EE;
    --muted:#8C8C94; --line:#2A2A2E; --red:#E5484D; --green:#3DD68C;
  }
  [data-composition-id="segN"] .scene{ position:absolute; inset:0; width:1920px; height:1080px; overflow:hidden; }
  /* a subtle vignette/glow is OK; NO full-screen linear gradients (H.264 banding) */
  [data-composition-id="segN"] .glow{ position:absolute; inset:0;
    background:radial-gradient(60% 50% at 50% 42%, rgba(232,88,16,0.10), transparent 70%); }
  /* ... component styles (section 3) ... */
</style>
</head>
<body>
  <div data-composition-id="segN" data-start="0" data-duration="DUR" data-width="1920" data-height="1080">
    <!-- scenes: each a full-frame .scene .clip, crossfaded; see exemplar -->
    <img class="bug" src="../assets/videodb-logo.png" />   <!-- persistent corner logo, see CSS -->
    <script>
      window.__timelines = window.__timelines || {};
      var R = '[data-composition-id="segN"] ';
      var tl = gsap.timeline({ paused:true });
      var XF = 0.55;
      function fadeIn(s,t){ tl.fromTo(R+s,{opacity:0,filter:'blur(18px)'},{opacity:1,filter:'blur(0px)',duration:XF,ease:'sine.inOut'},t); }
      function fadeOut(s,t){ tl.to(R+s,{opacity:0,filter:'blur(18px)',duration:XF,ease:'sine.inOut'},t); }
      /* build timeline here, anchored to the cue times in the brief */
      window.__timelines["segN"] = tl;
    </script>
  </div>
</body>
</html>
```

> The root mounts each segment as `<div data-composition-src="compositions/segN.html" ...>`; the
> root owns the `<audio>`. Segments are **silent, full-frame, opaque** (`background:#0B0B0C`).
> The segment's internal timeline is **0-based** — cue times in the brief map directly onto it.

## 2. Hard rules (cause real bugs if broken)

- **Determinism only** — no `Math.random()`, `Date.now()`, `new Date()`. Loops use finite `repeat:N` (never `repeat:-1`).
- Build the timeline **synchronously** — no `async`/`setTimeout`/Promise.
- Every `.scene` is `.clip` with no `data-start/duration` needed (it's inside a sub-comp; the sub-comp clip is timed by the root). All scenes exist from t=0; **visibility is controlled by opacity in the timeline** (start scenes after scene-1 at `opacity:0` via CSS, fade in at cue).
- **Crossfade, don't jump.** At a scene's cue T: `fadeOut(prevScene,T); fadeIn(newScene,T);`. Entrance animations of the new scene start at `T+0.25`.
- **No exit animations except the final scene.** The crossfade IS the exit.
- **Continuous motion:** something moves every ~2–3s within every scene (count-up, typewriter, stagger, arrow draw, pulse with finite repeat). No frozen holds.
- Only animate opacity/transform/color/filter. Never animate `display`/`visibility`/width/height of a `<video>`.
- Headlines 60px+, body 20px+, labels 16px+. `font-variant-numeric:tabular-nums` on numbers.
- **No emojis** — use CSS/SVG shapes or `✓ ✗ ★ ▲ → ☏`.
- Fonts: only `"Archivo Black"` (display) and `"Inter"` (body) — they auto-embed. Do NOT use Anton/other (silent fallback). No `@font-face`/`@import` (won't apply in sub-comp at render).
- One accent: `var(--orange)`. No second loud color. No purple/blue gradient, no neon, no glassmorphism.

## 3. Components (copy the CSS you need)

```css
/* Persistent corner logo bug — every segment */
[data-composition-id="segN"] .bug{ position:absolute; right:46px; bottom:40px; height:34px; width:auto;
  opacity:0.5; z-index:50; }

/* Callout box — the signature stamp. Default = off-white box / near-black text. */
[data-composition-id="segN"] .box{ display:inline-block; background:#F4F2EE; color:#0B0B0C;
  font-family:"Archivo Black",sans-serif; text-transform:uppercase; letter-spacing:0.01em;
  line-height:0.98; padding:14px 22px; border-radius:12px; font-size:54px;
  box-shadow:0 14px 40px rgba(0,0,0,0.5); }
/* Orange payoff box — the "this is the point" stamp. Use ONCE per segment for the punchline. */
[data-composition-id="segN"] .box.pay{ background:var(--orange); color:#fff;
  box-shadow:0 16px 50px rgba(232,88,16,0.45); }
[data-composition-id="segN"] .box.sm{ font-size:34px; padding:10px 16px; border-radius:10px; }

/* Name label (lower-third, talking-head) */
[data-composition-id="segN"] .namelabel{ font-family:"Archivo Black",sans-serif; text-transform:uppercase;
  background:#F4F2EE; color:#0B0B0C; padding:12px 20px; font-size:44px; letter-spacing:0.02em; border-radius:8px; }

/* Card / surface */
[data-composition-id="segN"] .card{ background:var(--card); border:1px solid var(--line);
  border-radius:16px; padding:28px 32px; }

/* Chip (dataset tags etc.) */
[data-composition-id="segN"] .chip{ display:inline-flex; align-items:center; gap:12px; background:var(--card);
  border:1px solid var(--line); border-radius:999px; padding:12px 22px; font-size:26px; font-weight:600; color:var(--txt); }
[data-composition-id="segN"] .chip .dot{ width:12px; height:12px; border-radius:50%; background:var(--orange); }

/* Pipeline node (architecture spine) */
[data-composition-id="segN"] .node{ display:inline-flex; align-items:center; justify-content:center;
  background:var(--card); border:1px solid var(--line); border-radius:14px; padding:20px 26px;
  font-family:"Archivo Black",sans-serif; text-transform:uppercase; font-size:30px; letter-spacing:0.02em; }
[data-composition-id="segN"] .node.on{ border-color:var(--orange); box-shadow:0 0 0 2px rgba(232,88,16,0.35), 0 0 30px rgba(232,88,16,0.35); }
[data-composition-id="segN"] .arrowh{ color:var(--muted); font-size:30px; } /* use → between nodes */

/* Big number / counter */
[data-composition-id="segN"] .bignum{ font-family:"Archivo Black",sans-serif; color:var(--orange);
  font-size:240px; line-height:0.9; font-variant-numeric:tabular-nums; }

/* Hand-drawn marker arrow — inline SVG, draw-on. Loose/imperfect stroke. */
/* <svg class="marker" viewBox="0 0 300 160"><path class="mk" d="M10,20 C120,10 160,90 250,120" /></svg> + arrowhead path */
[data-composition-id="segN"] .marker .mk{ fill:none; stroke:var(--orange); stroke-width:7;
  stroke-linecap:round; stroke-linejoin:round; }
```

## 4. Reusable JS helpers (paste into the segment script)

```js
// count a number up:  countUp('#stat', 0, 82, 1.2, T, v=>v+'%')
function countUp(sel,from,to,dur,at,fmt){ var o={n:from};
  tl.to(o,{n:to,duration:dur,ease:'power2.out',onUpdate:function(){
    var el=document.querySelector(R+sel); if(el) el.textContent=(fmt?fmt(Math.round(o.n)):Math.round(o.n)); }},at); }

// typewriter:  typewrite('#t', "I'm a string.", 1.6, T)
function typewrite(sel,str,dur,at){ var o={n:0};
  tl.to(o,{n:str.length,duration:dur,ease:'none',onUpdate:function(){
    var el=document.querySelector(R+sel); if(el) el.textContent=str.slice(0,Math.round(o.n)); }},at); }

// stamp a box in (pop with slight overshoot)
function stamp(sel,at){ tl.from(R+sel,{opacity:0,scale:0.7,duration:0.34,ease:'back.out(1.6)'},at); }

// draw a marker arrow on (set pathLength via JS so dash works regardless of length)
function drawArrow(sel,dur,at){ var p=document.querySelector(R+sel); if(!p) return;
  var L=p.getTotalLength(); p.style.strokeDasharray=L; p.style.strokeDashoffset=L;
  tl.to(p,{strokeDashoffset:0,duration:dur,ease:'power2.inOut'},at); }
```

## 5. Crossfade pattern (the spine of every segment)

```js
// scene-1 visible at t=0 (CSS opacity:1). Later scenes CSS opacity:0.
// At each cue from the brief:
fadeOut('#s1', T1); fadeIn('#s2', T1);
//  ...entrances of #s2 children start at T1+0.25, staggered, varied eases.
```

The brief for each segment gives the exact cue times (seconds, 0-based) and what each scene
shows. **Anchor every transition to those cues. Never let a visual lead the voice.**
