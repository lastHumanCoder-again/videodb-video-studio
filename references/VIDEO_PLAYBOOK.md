# The Explainer-Video Playbook
### A hand-off to whoever builds these next (and a challenge to do it better than I did)

Hey — welcome. You're inheriting a pipeline that produces long-form, narrated explainer videos (2–7 min) as **code**, not in an editor. Everything is HTML + GSAP rendered by [HyperFrames](https://www.npmjs.com/package/hyperframes), narrated by ElevenLabs, illustrated with AI images, and stitched together deterministically. This doc is everything I figured out the hard way. Read it once end-to-end, then keep it open as a checklist.

The single most important sentence in here: **the visual must show what's being said, at the moment it's said, and it must never stop moving.** Almost every rule below serves that sentence.

I've marked my own screw-ups with **⚠️ I got this wrong** and ideas I didn't get to with **💡 You should try**. Beat me.

---

## 0. The mental model

A finished video = one **root** HTML file that places N **segment** sub-compositions back-to-back on a video track, with N voiceover clips on an audio track. Each segment is one narration paragraph (~20–70s) and contains several internal **scenes** that crossfade. You build segments in parallel, sync each to its own voice track, then assemble.

```
root index.html
├── video track:  [seg1][seg2][seg3]...        (sub-compositions, back-to-back)
├── audio track:  [vo1] gap [vo2] gap [vo3]...  (narration + breathing gaps)
└── (optional) music bed track
```

Why segments? Because (a) you can fan them out to parallel workers, (b) each syncs to a short audio file you can transcribe precisely, and (c) one broken segment doesn't sink the render.

---

## 1. The workflow loop (memorize this order)

1. **Script** → break into logical segments (one idea per segment).
2. **Voiceover** → generate each segment with ElevenLabs (`eleven_v3`) + delivery tags.
3. **Transcribe** every VO clip to **word-level timestamps**. ← do NOT skip this.
4. **Extract cue times** — when does the narrator actually say each scene's trigger phrase?
5. **Design gate** → lock a `DESIGN.md` (palette, fonts, motion) before writing any HTML.
6. **Build** each segment's HTML, anchoring scene transitions to the real cue times.
7. **Generate AI images** for anything photographic; wire them in.
8. **Assemble** the root (gaps, track alternation).
9. **Lint → validate → inspect.** Fix every error. Extract frames to actually *look*.
10. **Render** draft/standard → spot-check → **render HQ**.

Do them in this order. The expensive mistake (which I made) is building visuals before you know the real audio timing — you'll redo all of it.

---

## 2. Script & segmentation

- One segment = one paragraph = one idea. Hooks and resolutions can be longer (60–80s); tips/points 25–40s.
- Write the **on-screen text separately from the VO.** On-screen is short labels, numbers, stamps — never the full sentence. The VO carries the words; the screen carries the *proof*.
- For every sentence, ask: *what object/motion shows this?* If your answer is "text of the sentence," you haven't designed the beat yet.
- Storyboard a **beat sheet** first (timecode → VO fragment → visual → on-screen text → asset source). Building the beat sheet before animating saved me every time I did it and bit me every time I didn't.

**💡 You should try:** keep a one-line "visual verb" for each beat ("fill", "wipe", "stack", "tick", "draw a line", "flip ✗→✓"). If two adjacent beats share a verb, vary one.

---

## 3. Voiceover — ElevenLabs `eleven_v3`

The narrator is the spine. We use a single consistent voice across a series for brand recall. **Always confirm the voice/model with the client before spending on generation** — it's a paid call and the choice doesn't carry across jobs by default.

### The canonical script (don't rewrite this per project)

Write your lines into `voiceover/segments.json` and run the skill's `scripts/tts.py` from the project root:

```json
{
  "voice_id": "YOUR_VOICE_ID",
  "model": "eleven_v3",
  "settings": {"stability": 0.5, "similarity_boost": 0.75, "use_speaker_boost": true},
  "segments": {
    "seg1_hook": "[conversational] Your opening line... [knowing] the turn... [confident] the payoff."
  }
}
```

```bash
python3 "$SKILL_DIR/scripts/tts.py"            # all segments (skips existing mp3s)
python3 "$SKILL_DIR/scripts/tts.py" seg1_hook  # regenerate one by name
```

The regenerate-by-name filter is essential — you'll re-cut single lines constantly. **No `ELEVENLABS_API_KEY`?** The script prints every segment's text as a paste-ready block; generate the VO anywhere and drop the MP3s into `voiceover/`. Either way, TTS with a key is a **paid call — get explicit approval before running it, every time.**

### Delivery tags (the human-ness)

`eleven_v3` reads inline tags. Sprinkle, don't carpet-bomb. The ones I leaned on:
`[conversational] [warm] [confident] [knowing] [thoughtful] [intriguing] [emphatic] [matter-of-fact] [reassuring] [curious] [satisfied] [wry] [light] [serious] [measured] [inviting]`

Also use `...` for a real pause beat ("And even after all that... nobody finds you.").

### ⚠️ Gotchas I hit (these will bite you)

- **Numbers/prices get misread.** `$9.99` was spoken as "nine hundred ninety-nine." **Spell prices as words**: "nine dollars and ninety nine cents." Even "nine ninety-nine" is ambiguous — write it out fully.
- **Ambiguous abbreviations** — `'St'` reads as "Saint" or "Street." Rephrase: "writing out the word Street vs shortening it."
- **Fix typos in the source transcript before generating** — the model will faithfully pronounce "it Iinstead."
- **Verify a regeneration actually happened** — diff the file's md5/size. I once "regenerated" and got a cached file.
- Keep one segment per logical beat. A 70s+ single generation is fine but a 3-minute one risks drift; splitting also gives finer sync control.

---

## 4. Sync — the lesson that cost me a re-render

**You cannot guess intra-segment timing.** I gave builders estimated scene times ("DIY card at 5s, freelancer at 22s") and the visuals ran *ahead* of the voice — the freelancer card appeared while the narrator was still on DIY. It looked broken. The fix is mechanical and bulletproof:

**Transcribe every VO clip to word-level timestamps, then anchor each scene's transition to the real time the narrator says its cue word.**

```bash
# word-level transcript per segment (HyperFrames ships whisper)
npx hyperframes transcribe seg1_hook.mp3   # writes transcript.json
cp transcript.json seg1_hook.transcript.json
```

Then declare each scene's trigger phrase in `voiceover/cues_spec.json` and run the skill's extractor:

```json
{
  "seg1_hook": {"s_open": 0.0, "s_question": "here's a photo", "s_pivot": "even see"}
}
```

```bash
python3 "$SKILL_DIR/scripts/extract_cues.py"   # reads voiceover/, writes cues.json + a cue table
```

Each value is `0.0` (segment start) or a phrase; the cue is the start time of that phrase's first word in the transcript. The script fails loudly on phrases it can't find — fix the phrase, never guess the number. No API key involved; this always works.

Rule: **scene's crossfade fires AT the cue time; its entrance animations start 0.2–0.3s after.** A visual landing a beat *after* the word feels natural; landing *before* feels broken. Never let a scene appear before its cue.

**💡 You should try:** also pull per-word times for on-screen **karaoke captions** (HyperFrames has a captions reference). I never added captions; short-form retention loves them.

---

## 5. The design gate (do this before any HTML)

Never write a composition with default colors. Lock a `DESIGN.md` first:

- **Palette**: a near-black canvas, **one** accent color that carries all energy, a warm off-white for text, a muted gray for secondary, plus a red (problem/✗) and a green (confirm/✓). That's it. One accent. Resist a second.
- **Typography**: one heavy display face + one clean body face. Extreme weight contrast (300 vs 900, not 400 vs 700).
- **Motion**: smooth eases (`power3.out`, `expo.out`); the accent only appears when the "good" thing enters; pre-resolution states are desaturated.
- **"What NOT to do"**: list the anti-patterns (no generic blue `#3b82f6`, no `#333`, no two-sans pairing, no static holds).

### ⚠️ Fonts: verify in the *render*, not the lint

- The renderer auto-embeds only a **curated** font set. `Inter` and `Archivo Black` embed automatically; **`Anton` does NOT** and silently falls back to a generic sans — even with a base64 `@font-face` inside a `<template>` sub-composition (the template's `@font-face` doesn't register during headless capture).
- So: pick a display font that `npx hyperframes lint` does **not** flag with `font_family_without_font_face`, and **confirm typography by extracting a frame from the actual MP4** — lint passing is not proof.

---

## 6. Building in HyperFrames

### Structure

- **Root** (`index.html`): a standalone doc. The `data-composition-id` div sits directly in `<body>` (NOT in a `<template>`). It holds the segment clip divs + `<audio>` clips, and registers an empty `window.__timelines['root']`.
- **Segment** (`compositions/segN.html`): a `<template>`-wrapped sub-composition with `data-composition-id="segN"`, scoped `<style>` (`[data-composition-id="segN"] ...`), and one paused GSAP timeline registered as `window.__timelines['segN']`.

### Gaps between segments (so the VO can breathe)

Put a **0.6s silent gap** between segments. The narrator jumping straight into the next line sounds rushed. Implementation: each segment's **video clip** holds its last scene through the gap (clip duration = audio duration + 0.6), while the **audio clip** is just the natural VO length placed at the segment start.

### ⚠️ Track alternation (a floating-point trap)

Back-to-back clips on the **same track** can trip a `overlapping_clips_same_track` error because `30.36 + 30.76` computes to `61.120000000000005` and reads as overlapping the next clip at `61.12`. **Fix: alternate adjacent video clips between `data-track-index="1"` and `"2"`.** Track index doesn't affect visual layering (use `z-index` for that), so this is free. Put all audio on its own track (e.g. `3`).

### Transitions & entrances (non-negotiable)

- Every scene change uses a transition — no jump cuts. Primary = **blur-crossfade** (warm, forgiving). Reserve a punchier one for the hero reveal.
- **Every element animates IN** (`gsap.from`). Vary ≥3 eases per scene; offset the first entrance 0.1–0.3s.
- **No exit animations except on the final scene.** The crossfade *is* the exit; the outgoing scene must be fully visible when it starts.

Reusable blur-crossfade helpers:

```js
var tl = gsap.timeline({paused:true});
var XF = 0.55, R = '[data-composition-id="segN"] ';
function fadeIn(s,t){ tl.fromTo(R+s,{opacity:0,filter:'blur(18px)'},{opacity:1,filter:'blur(0px)',duration:XF,ease:'sine.inOut'},t); }
function fadeOut(s,t){ tl.to(R+s,{opacity:0,filter:'blur(18px)',duration:XF,ease:'sine.inOut'},t); }
// at a cue time T: fadeOut('#sceneA',T); fadeIn('#sceneB',T);
```

### Continuous motion (the client's #1 note — internalize it)

**Do not build a visual once and hold it static for 25 seconds.** Even within one tip, something visible must change every ~2–3s, *mimicking the action being described*:

- "Fill out your profile" → name **types in**, rating **ticks up 0.0→4.9**, photos **upload one by one**, boxes **expand**, sections **tick green** as completed.
- "Reviews stream in" → cards **slide in one at a time**, stars **fill ★ by ★**, the count **increments**.
- "It's a wall of complaints" → cards **stack/accumulate**.

"Entrance then hold" is the failure mode. If a scene must linger, give it ambient life (a finite pulse, a counter, a slow drift) — never a frozen frame.

Typewriter, done deterministically:

```js
var s = "I'm a mobile dog groomer in Austin.";
tl.to({n:0},{n:s.length,duration:1.9,ease:'none',onUpdate:function(){
  var el = document.querySelector(R+'#typed');
  if (el) el.textContent = s.slice(0, Math.round(this.targets()[0].n));
}}, START);
```

### Hard rules (these cause real bugs)

- **Deterministic only.** No `Math.random()`, no `Date.now()`, no `new Date()`. Need randomness? Seed a mulberry32 or stagger by index. Need a loop? **Finite** `repeat: N` — `repeat:-1` breaks the capture engine.
- Build the timeline **synchronously** (no `async`/`setTimeout`/Promises) — the engine reads `window.__timelines` right after load.
- Only animate visual props (opacity, transforms, color, filter). Never animate `display`/`visibility`, never call `video.play()`.
- `.scene{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden}`. The content container is `.wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:Npx;box-sizing:border-box}` — **use padding to position, never `position:absolute;top:Npx` on a content container** (it overflows when content grows).
- Headlines 60px+, body 20px+, data labels 16px+. `font-variant-numeric:tabular-nums` on number columns.
- **Emojis don't render reliably** in the capture engine. Use CSS/SVG shapes or safe glyphs (`✓ ✗ ★ ▲ → ☏`) instead of `📅 🎉 🛒`.

---

## 7. AI images (Kie.ai · nano-banana-pro)

Use AI images for **photographs** — people, places, real-world scenes (e.g. "a real photo of the business owner"). Do **not** use them for UI mockups, charts, or diagrams — those look sharper and stay on-brand as CSS/SVG you control.

### The canonical script (async create → poll → download)

```bash
python3 "$SKILL_DIR/scripts/gen_image.py" assets/owner.png 16:9 "candid documentary-style photograph of ..."
```

**No `KIE_API_KEY`?** The script prints the prompt + aspect as a paste-ready block — generate the image in any tool and save it to the given path. With a key it's a **paid call — get explicit approval before running it, every time.** The gotchas below are baked into the script, but they explain its odd shape.

### ⚠️ Gotchas that wasted my time

- **The params are nested under `input`** — `{"model":"nano-banana-pro","input":{"prompt":...,"aspectRatio":"4:5"}}`. Top-level `prompt` → `422 input cannot be null`.
- **No `resolution` field** here (it 500s). Valid `aspectRatio`: `16:9 9:16 4:5 1:1 2.39:1`.
- **Kie's WAF blocks Python `urllib`'s TLS fingerprint** → `403 Forbidden`, even though a browser UA header doesn't help. **Shell out to `curl`** (which passes). The `GET /credit` check works either way; the `POST` is what gets blocked.
- It's **async** — `200` means "queued," not "done." Always poll `recordInfo`.
- **Moderation/transient failures happen** — retry once with a slightly reworded prompt before giving up.

### Prompt craft for photoreal

- Ask for "**candid documentary-style photograph**," "warm natural light," "authentic, slightly imperfect, **not a polished stock photo**," "shallow depth of field." This consistently beat the sterile stock look.
- nano-banana-pro renders **text well** — you can put a brand name on a polo/van and it stays coherent. Use that.
- Generate the *contrast* too when the script needs it (I made both a warm real owner **and** a generic stock-photo worker for a "real vs stock" beat).
- Lock a `seed` if you need to iterate on the same composition.
- Keep characters consistent across a video by theming around one (I reused one fictional business, "Miller HVAC," across an entire video so the owner photo, the reviews, and the phone number all matched).

**💡 You should try:** image-to-image with `referenceImages` (up to 8 URLs) to keep a character identical across multiple shots. I only did text-to-image.

---

## 8. QA & verification — trust nothing until you've looked

Run all three, fix every **error** (warnings/info: judge):

```bash
npx hyperframes lint                 # structure, fonts, overlaps
npx hyperframes validate             # WCAG contrast in headless Chrome
npx hyperframes inspect --samples 60 # layout overflow/occlusion across the timeline
```

Then **extract frames and actually look** — lint/inspect can't see "ugly":

```bash
ffmpeg -loglevel error -ss 72 -i out.mp4 -frames:v 1 /tmp/frames/t72.png -y
```

### ⚠️ Inspect/validate quirks to know

- **Contrast warnings are often false positives.** `validate` samples ~5 fixed timestamps across the whole video, so it measures one segment's hidden elements while another segment is on screen → "1:1 contrast." Check whether the element is actually *visible* at that time before chasing it.
- **`--samples 9` (default) misses things.** On a 6-minute video use `--samples 60–72`. An agent told me "0 issues" at 9 samples; 70 samples found 11.
- **`data-layout-allow-overflow`** silences intentional `container_overflow`/`canvas_overflow` (e.g. a badge straddling a phone's edge, content scrolling inside a clipping screen). **`data-layout-allow-occlusion`** silences intentional layering (a pinned bar covering a header). But **`clipped_text` is NOT silenced by allow-overflow** — if text is getting cut by its own box, you must actually resize/wrap/shorten it.
- **The tall-scrolling-phone trap:** a phone mockup that scrolls a tall page or slides pages horizontally *will* overflow and clip text the inspector flags as errors. Simpler is better — make the page fit the screen and **crossfade** page-swaps (opacity) instead of sliding content off-screen.
- `/tmp` gets cleaned between steps — `mkdir -p` your frame dir each time.

---

## 9. Render & deliver

```bash
npx hyperframes render -o out.mp4 --quality draft      # fast preview while iterating
npx hyperframes render -o out_HQ.mp4 --quality high    # final master
```

- Iterate in **draft**, deliver in **high**. Don't HQ-render until frames look right — HQ is slow.
- Render in the **background** and verify frames while it runs.
- Confirm the master with `ffprobe` (duration, 1920×1080, h264+aac).
- A standard 1080p explainer lands ~25–45 MB; that's normal.

---

## 10. Attention & retention craft (the part that actually matters)

The pipeline is plumbing. This is the product.

- **Hook in the first 3 seconds.** Cold-open your strongest, most concrete line — a real quote, a shocking number — *before* the narrator's wind-up. Don't open on a static logo or an empty UI ("it's blank because it's only showing a website" was a real, fair complaint I got).
- **Real social proof beats claims.** Recreate genuine forum/review posts as clean cards (real text, real attribution, legible at video scale). A faithful recreation reads as authentic and stays sharp where a tiny raw screenshot wouldn't. **Never fabricate fake posts with invented usernames presented as real** — sourced/real or clearly representative only.
- **A recurring visual motif gives a through-line.** I used a red-✗ → accent-✓ "flip" 4+ times so the whole video felt like one argument. Pick one motif and repeat it.
- **The comparison table is a citation magnet.** A clean N-column "us vs them" grid (rows: who does the work / what it costs / the catch) is the single most screenshot-able, memorable frame. Spend your best layout here.
- **Show the dream, then the gap.** Build something vibrant and alive (a storefront assembling, a profile filling) — motion *is* the hook.
- **Numbered spines** ("TIP 3 OF 7", chapter cards) orient the viewer and create small completion dopamine. Keep the badge/number consistent across the series.
- **Pattern interrupts** before the key turn ("here's the part that's different 👉") reset attention.
- **End = the citable definition + one CTA.** Recap in a single sentence that doubles as the thing you want quoted, then one clear action. Not five.

**💡 You should try (I didn't):**
- **A light music bed** under the VO, ducking up at chapter cards and the close. Every brief asked for it; I never added it. Low effort, big lift.
- **Karaoke captions** synced to the word timestamps you already have.
- **B-roll variety** — I leaned heavily on UI mockups; mix in more AI photography and abstract motion so it's not all cards.
- **Trim discipline** — my tip-list videos ran 6–7 min vs a ~4:30 target. Long = drop-off. Cut the resolution and tighten each tip; respect the target length.

---

## 11. Working with parallel build-agents

Segments are independent, so fan them out. What makes delegation work:

- Give each agent **(a)** the exact composition id + duration, **(b)** a known-good file to mirror as the structural/motion exemplar, **(c)** the **exact cue timestamps** for its scenes, **(d)** the asset paths, and **(e)** the hard rules (palette, fonts, determinism, continuous-motion mandate).
- Then **you** own assembly, QA, and fixes centrally. Agents drift on consistency and timing — your central `inspect` + frame checks are the backstop.

**⚠️ My biggest process mistake:** I kept launching build-agents **one per message** and waiting for each. They're independent — **fire all of them in a single message** so they run concurrently. I wasted a lot of wall-clock doing this serially. Don't.

**💡 You should try:** a small **reusable component library** (the tip-card shell, the reddit-card, the founder-credential card, the phone frame, the comparison grid) as copy-paste partials, so agents start from proven, on-brand pieces instead of re-deriving them. I rebuilt these from memory each video.

---

## 12. Quick-start checklist

```
[ ] Script written, split into segments (1 idea each), on-screen text separated from VO
[ ] Voice/model confirmed with client (paid generation)
[ ] VO generated (prices spelled out, tags added, typos fixed); regen verified by file diff
[ ] Every VO transcribed → cue times extracted per scene
[ ] DESIGN.md locked (palette, fonts that auto-embed, motion, anti-patterns)
[ ] Segments built: synced to cues, continuous motion, entrances-in/no-exits, deterministic
[ ] AI images generated for photographic beats (curl, input{}, aspectRatio); wired in
[ ] Root assembled: 0.6s gaps, alternating video tracks, audio on its own track
[ ] lint 0 errors · validate (ignore false-positive contrast) · inspect --samples 60 = 0 errors
[ ] Frames extracted and eyeballed (fonts, layout, the photo beats, the hero frames)
[ ] Draft render reviewed → HQ render → ffprobe confirms specs
[ ] (Don't forget) music bed? captions? runtime within target?
```

---

## 13. The standards I'd hold you to

1. **Sync is sacred.** Anchor to transcripts. A visual that leads the voice is the most amateur tell.
2. **Never let the screen go static.** Every ~2–3s, something moves and means something.
3. **Look at the render.** Not the lint. Frames don't lie.
4. **One accent color. One display font. One CTA.** Restraint reads as premium.
5. **Sourced or representative proof — never faked.**
6. **Respect the runtime.** Shorter and tighter beats longer and complete.

You have the whole pipeline and every trap I stepped in. Go make them tighter, faster, and better-looking than mine. That's the job.

— handed off with everything I know
