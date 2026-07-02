# SCRIPT — LAUNCH: "Record Once. Replay Anywhere." (open-record-replay)

**Status:** DRAFT for approval (script stage — no VO / images / compositions generated yet).
**Type:** **Launch / reveal video** (the open-source announcement) — NOT a numbered essay episode.
A longer YouTube deep-dive can follow later as its own episode.
**Source:** VideoDB open-source release — *Record & Replay* MCP server.
repo: github.com/video-db/open-record-replay · tagline: *"Record desktop workflows once. Replay them anywhere."*
**Format:** 16:9, 1920×1080, 24fps · target runtime **~1:45** (launch pace — tight, high-energy,
reveal → proof → CTA) · VideoDB brand look (the skill's `references/STYLE.md` + `./DESIGN.md`), build
reference: the `youtube-longform` template.
**Goal:** Announce the tool, make it *feel* magic in under two minutes, and drive to the repo.
Shareable on X / LinkedIn / YouTube; every beat is a screenshot.

---

## Title / thumbnail options
1. **"Record Once. Replay Anywhere."** ← recommended launch line (+ subline "open-source AI desktop automation")
2. "Stop Scripting Agents. Just Show Them." (provocation)
3. "We Open-Sourced the Tool That Teaches AI to Use Any App."
4. "Your AI Agent Can Finally Watch You Work."

**Recommended combo:** Title #1, hook-overlay *"just show it. once."* in the first 3s, product name
**Record & Replay** revealed by ~0:12.

## Launch tone (vs. the essay style)
- **Reveal energy, not lecture.** Faster cuts, bigger type, the product name lands early and hard.
- Still the VideoDB look: near-black canvas, one orange accent, Archivo Black stamps, continuous
  motion. Just **denser** — a beat every ~1.5–2.5s.
- Ends on a real launch CTA: **open source · on GitHub today.**

## Recurring motifs (the through-line)
- **The pulsing orange ● REC dot** — the signature; ignites in the hook, "arms" the demo, recap at close.
- **Record → Compile → Replay** three-node spine; the orange active node walks it once.
- **The "button moved — still worked" self-heal flash** — the money frame: brittle script ✗ red →
  self-healing replay ✓ green.

## Reporting stance
- Real, open-source, described honestly. MCP server (Python 3.10+). Dual capture (accessibility log +
  screen video → VideoDB) → LLM compiles `SKILL.json` + `SKILL.md` (with variable templating &
  versioning) → agent replays with native calls + visual self-healing. Cross-platform (Win UIA /
  macOS Accessibility / Linux AT-SPI). Model-neutral ("an LLM"). No fabricated benchmarks.

---

## SEG 1 — HOOK  (~15s)
**VO:**
> [confident] Show a person a task once — they've got it for life. [matter-of-fact] Show an AI agent
> the same task, and it starts from scratch every single time — [serious] fumbling through your apps,
> breaking the second a button moves. [curious] So we built the obvious fix: [intriguing] let it
> watch you do it... once.
**On-screen:** cursor fumbles a form → red ✗ "AGENT FAILED" → hard cut to pulsing orange **● REC** →
orange box "JUST SHOW IT. ONCE."
**Visual:** fumble → the REC dot ignites (motif set) → pivot stamp.
**Cue → next:** "do it... once"

## SEG 2 — THE REVEAL  (~14s)
**VO:**
> [confident] This is Record and Replay. [warm] Open source, from VideoDB. [emphatic] You record a
> desktop workflow one time — [confident] and any AI agent can replay it, anywhere. [knowing] Three
> steps. Record. Compile. Replay.
**On-screen:** product lockup **"RECORD & REPLAY"** stamps in under the REC dot · "OPEN SOURCE ·
VIDEODB" strip · the three-node spine **RECORD → COMPILE → REPLAY** draws on (nodes dim, awaiting).
**Visual:** name reveal; the spine is introduced (it structures the rest of the video).
**Cue → next:** "Record. Compile. Replay."

## SEG 3 — RECORD  (~20s)  ← spine node 1 lights
**VO:**
> [matter-of-fact] You hit record, and just do the task. [measured] Two things get captured at once:
> [knowing] a native accessibility log — every click and keystroke, exact to the field — [confident]
> and the screen itself, recorded as video, into VideoDB. [emphatic] Precision *and* picture.
> [warm] Windows, Mac, or Linux.
**On-screen:** ● REC arms; split capture — left "ACCESSIBILITY LOG" rows type in (`click ▸ Search`,
`type ▸ "invoice"`, `press ▸ Enter`) · right "SCREEN → VIDEODB" video frame streaming · orange payoff
"PRECISION + PICTURE, AT ONCE." · OS chips Windows · macOS · Linux.
**Visual:** dual-capture split (core mechanic), log types as video streams.
**Cue → next:** "Windows, Mac, or Linux"

## SEG 4 — COMPILE  (~18s)  ← spine node 2 lights
**VO:**
> [matter-of-fact] Then an LLM compiles it. [measured] Your one demo becomes a reusable skill — a
> `SKILL.json` an agent runs, and a `SKILL.md` a human can read. [intriguing] It even spots the parts
> that change — a name, a date, an amount — [emphatic] and turns them into variables. [satisfied]
> Record it once, reuse it a thousand ways.
**On-screen:** event log → orange arrow "COMPILE" → two artifact cards `SKILL.json` + `SKILL.md` · a
value highlights and morphs into `{{ query }}` orange chip · payoff box "ONE DEMO → A REUSABLE SKILL."
**Visual:** log → skill artifacts; the variable-templating morph.
**Cue → next:** "a thousand ways"

## SEG 5 — REPLAY + SELF-HEALING  (~24s)  ← spine node 3 lights (HERO beat)
**VO:**
> [confident] Now any agent replays it — real native clicks, no pixel guessing. [measured] But here's
> the moment that matters. [knowing] Real apps change. A button moves. A panel gets redesigned.
> [serious] A brittle script crashes right here. [intriguing] This doesn't. [emphatic] Because it
> remembers what the screen *looked like* — so it finds the button that matches, and keeps going.
> [satisfied] It heals itself.
**On-screen:** replay runs (steps ✓, `{{ query }}` filled live) → self-heal motif: "Submit" button
**slides** to a new spot → brittle script snaps ✗ red "NOT FOUND" → replay re-scans, matches by
appearance, lands ✓ green → orange payoff "THE UI CHANGED. IT DIDN'T CARE."
**Visual:** the button-moved self-heal flash — THE signature frame.
**Cue → next:** "heals itself"

## SEG 6 — USE CASES + CTA  (~22s)
**VO:**
> [curious] So — automate the boring desktop chore. [confident] Turn a workflow into docs that
> actually *run*. [matter-of-fact] Drive that legacy app with no API. [knowing] Ship automation that
> survives a redesign. [emphatic] One recording — all of it. [warm] It's open source, and it's live
> on GitHub today. [satisfied] Go teach an agent something. [confident] Because to see... is to know.
**On-screen:** fast 4-card montage "AUTOMATE THE BORING · DOCS THAT RUN · DRIVE LEGACY APPS ·
SURVIVES REDESIGNS" → orange payoff "RECORD ONCE. REPLAY ANYWHERE." → REC dot + full VideoDB logo
stamp → single CTA "OPEN SOURCE · github.com/video-db/open-record-replay" · "TO SEE IS TO KNOW."
**Visual:** rapid tile stagger → payoff → brand + one CTA. (Only segment with an exit.)
**Cue → end.**

---

## Accuracy notes (verify before VO)
- **MCP server**, Python 3.10+, `uv`, MCP 1.0+. Stages: **Record → Compile → Replay.**
- **Dual recording:** accessibility events (deterministic) + screen video → **VideoDB** (Capture SDK).
- **Compile:** an **LLM** → **`SKILL.json`** (executable) + **`SKILL.md`** (readable); **variable
  templating** (search terms/dates); **versioning** (auto-increment + archive).
- **Replay:** reads skill, substitutes variables, native system calls; **self-healing** via visual
  scene descriptions when UI shifts.
- **Cross-platform:** Windows UI Automation · macOS Accessibility · Linux AT-SPI.
- **Tools (if shown):** `record_skill_tool`, `stop_recording_tool`, `compile_skill_tool`,
  `list_skills_tool`, `request_capture_permissions_tool`. Model-neutral; no fabricated numbers.

## Next steps (gated on your OK)
1. Confirm **launch title + script** (and the self-heal motif as the signature frame).
2. Generate VO (channel voice `86SOy9VyOePcRbIneYDa`, eleven_v3) — **paid; needs your go-ahead.**
3. Transcribe → cues → build 6 compositions (spine/box/pipeline components reused) + 1 real legacy-app
   screenshot → assemble → QA → render HQ. Turnkey.
