# SCRIPT — Episode 2: "AI Mastered Chess. It Still Can't See the Board."

**Status:** DRAFT for approval (script stage — no VO/images generated yet).
**Source:** VideoDB Labs field note — *"Strong general-purpose VLMs can still fail on downstream
vision tasks"* (chessboard → FEN experiment / Chess Lens), S. Nagaonkar, May 19 2026.
labs.videodb.io/engineering/field-notes/claude-chessboard-spatial-reasoning · repo: github.com/video-db/chess-lens
**Format:** 16:9, 1920×1080, 24fps · target runtime **~3:40** · same tech video-essay style
(the skill's `references/STYLE.md` + this template's `DESIGN.md`; this worked example is itself the build reference).
**Thesis:** Playing chess is logic (solved). *Reading a board from an image* is vision — and even
the best models stumble at exact spatial localization. Which one wins depends on the task and the
setup, not the leaderboard. (Direct sequel to Ep1's "evaluate the setup, not the model.")

---

## Title options (YouTube)
1. **"AI Mastered Chess. It Still Can't See the Board."** ← recommended (the contradiction = the hook)
2. "Can AI Play Chess? That's the Wrong Question." (your bait-and-pivot instinct)
3. "We Showed the Best AIs a Chessboard. It Got Weird."
4. "Which AI Actually Sees Best? We Used Chess to Find Out."

**Recommended combo:** Title #1, with hook-overlay *"can AI play chess? wrong question."* in the first 3s.

## Recurring motifs
- **The one-wrong-square board.** A clean CSS chessboard; when a model errs, the offending square
  flashes **red** — repeated every time we show a failure. The whole video's visual signature.
- **Orange payoff box** for each beat's punchline (one per scene).
- **Callback to Ep1:** the closing lesson is the orange box *"BEST GENERAL MODEL ≠ BEST FOR YOUR TASK."*

## Reporting stance
- **Name the models. State the findings to the point. Do not tinker with the numbers.** These are
  observations from real research — not a downgrade or a dig at anyone. Report exactly what was
  found: GPT-5.4 and Claude Opus 4.7, the real accuracies, the real failure modes.
- Accuracy is still the goal: the ~2.78% run was an output-truncation/parse failure at max summary
  under the 1024-token cap, and it recovered to ~84.7% at 4096 tokens. State that mechanism plainly
  (the setup broke it) — that's the actual finding, reported straight, not spin. Re-verify every
  number against the source before VO.

---

## SEG 1 — HOOK  (~26s)
**VO:**
> [confident] Twenty-five years ago, a computer beat the world chess champion. [matter-of-fact]
> Today, a chess engine on your phone would crush every human who has ever lived. [knowing] So
> this should be the easiest question we could ask an AI: [curious] here's a photo of a
> chessboard... what's on it? [thoughtful] ...And some of the best models in the world get it
> wrong. [intriguing] We're not testing whether AI can play chess. We're testing whether it can
> even see the board.
**On-screen:** cinematic chessboard (AI hero) → "AI CAN PLAY CHESS." (off-white) → flip to orange
"CAN IT *SEE* THE BOARD?" · small "wrong question" tag.
**Visual:** moody chessboard image; a scanning reticle sweeps it; pivot stamp lands.
**Cue → next:** "see the board"

## SEG 2 — THE REAL QUESTION  (~26s)
**VO:**
> [measured] Because playing chess is logic. [emphatic] Reading a board from an image is vision.
> [conversational] Two completely different skills. [confident] A model has to find the board, get
> its orientation, and place every single piece on exactly the right square. [knowing] Miss one —
> by one square — and the whole position is wrong. [thoughtful] For anything real — an app that
> watches a board, a camera reading a shelf, an agent looking at a screen — that precision is the
> whole game. [curious] So which of today's top models actually gets it right?
**On-screen:** "LOGIC" vs orange "VISION" split · CSS board appears; one square flashes red →
"ONE SQUARE OFF = WRONG" · use-case chips: "board · shelf · screen".
**Visual:** the split; the board with a red square (motif established).
**Cue → next:** "gets it right"

## SEG 3 — THE EXPERIMENT  (~30s)
**VO:**
> [matter-of-fact] So the team at VideoDB Labs ran the test. [measured] Seventy-two real positions
> from a single game. [confident] Each one shown to the model as an image. The job: output the
> exact layout — every piece, every square — as one precise line of text. [serious] Scoring was
> brutal: exact match only. [knowing] One piece on the wrong square, one miscounted gap... and the
> entire board counts as wrong. [matter-of-fact] Two models in the ring: GPT five point four, and
> Claude Opus four point seven — each run at different thinking settings.
**On-screen:** "72 POSITIONS" (count) · board image → arrow → a FEN-style text line · "EXACT MATCH
ONLY" (orange) · two model chips: "GPT-5.4" · "CLAUDE OPUS 4.7".
**Visual:** board → text-map conversion; brutal-scoring stamp; the two contenders.
**Cue → next:** "thinking settings"

## SEG 4 — THE RESULTS  (~32s)
**VO:**
> [curious] And the spread was wild. [confident] The best run — GPT five point four — got a
> perfect score. Seventy-two out of seventy-two. [satisfied] A hundred percent. [measured] Claude
> Opus, at its best, topped out around eighty-five. [intriguing] But here's the part nobody
> expected. [knowing] Crank the thinking budget to maximum... and it didn't get smarter. It
> collapsed. [serious] Two point eight percent. [thoughtful] Same model. Same images. And a far
> worse result.
**On-screen:** leaderboard — `GPT-5.4 (low) 100%` (green, top) · `GPT-5.4 default 97%` ·
`Claude Opus max 85%` · then the twist: a bar crashing to `2.8%` labeled "MAX THINKING" with orange
"NOBODY EXPECTED THIS".
**Visual:** leaderboard counts up; the collapse bar drops hard (counter ticking down).
**Cue → next:** "worse result"

## SEG 5 — WHY IT FAILS  (~34s)
**VO:**
> [measured] So what went wrong? [knowing] The models weren't blind. They knew it was a chess
> position. They failed at the exact location. [matter-of-fact] A piece shifted one square over. An
> empty gap miscounted. The right piece... in the wrong place. [thoughtful] And at max thinking,
> the model spent so many words explaining itself that it ran out of room before it finished — so
> the answer got cut off. [confident] It wasn't the brain that failed. It was the setup around it.
> [knowing] And Anthropic's own documentation says it plainly: Claude's spatial reasoning is
> limited — reading a clock face, or placing chess pieces, is still hard.
**On-screen:** expected board vs model output, the wrong square flashing red (`1BNP1N1P` →
`1BNB1N1P`) · "TRUNCATED" tag on an overflowing text box · orange "IT WASN'T THE BRAIN. IT WAS THE
SETUP." · quoted line "spatial reasoning… is limited" — attributed **"— Anthropic docs"**.
**Visual:** the diff (motif payoff); the truncation; the payoff box.
**Cue → next:** "still hard"

## SEG 6 — THE LESSON  (~26s)  ← callback to Ep1
**VO:**
> [measured] And this is the lesson worth keeping. [emphatic] The best general model is not
> automatically the best model for your task. [confident] GPT didn't win because it's smarter. It
> won at this one specific job — reading a grid — with enough room to answer. [knowing] You'd never
> know that from a leaderboard. [satisfied] You only find it by testing on the exact thing you're
> trying to build.
**On-screen:** a generic "#1 MODEL" trophy crossed out (✗) → orange payoff **"BEST GENERAL MODEL ≠
BEST FOR YOUR TASK."** · small tie-in "(see: evaluate the setup, not the model)".
**Visual:** trophy ✗ → orange box; subtle Ep1 callback.
**Cue → next:** "trying to build"

## SEG 7 — VideoDB / Chess Lens  (~26s)
**VO:**
> [matter-of-fact] Which is exactly what this was built for. [confident] It's called Chess Lens —
> and it runs on VideoDB. [measured] VideoDB ingests the board visually, follows the position as
> the game moves, and turns every frame into structured data. [knowing] The evaluation, the traces,
> the score for every model and every setting — all in one place. [satisfied] So you can see, for
> your task, which model actually reads the world correctly.
**On-screen:** pipeline "BOARD → INGEST → TRACK POSITION → STRUCTURED DATA" (animated, orange) ·
a compare panel "model × setting → score" · VideoDB logo bug.
**Visual:** the Chess Lens pipeline spine; an eval grid; brand mark.
**Cue → next:** "reads the world correctly"

## SEG 8 — CLOSE + CTA  (~24s)
**VO:**
> [measured] A machine beating a grandmaster is old news. [emphatic] The real frontier is whether
> it can look at the world... and get it exactly right. [confident] And for your problem, knowing
> which model does — [knowing] that's not a guess. It's a test. [satisfied] Don't trust the
> leaderboard. Run it on your own board. [warm] To see... is to know.
**On-screen:** orange "DON'T TRUST THE LEADERBOARD. TEST IT." · "TO SEE IS TO KNOW." + full VideoDB
logo stamp · CTA "READ THE FIELD NOTE · github.com/video-db/chess-lens".
**Visual:** recap the one-square board; tagline + logo; one CTA.
**Cue → end.**

---

## Accuracy notes (verify before VO)
- 72 positions, single game, image→FEN, exact-match scoring. Models: GPT-5.4 + Claude Opus 4.7 at
  several thinking/summary settings. Best = GPT-5.4 (100%). Best Claude = ~84.7% (max, run 2).
  The ~2.8% collapse = parse/token-truncation at max summary under the 1024-token cap; recovered at
  4096 tokens. Failure modes: one-file shift, empty-square miscount, right-piece-wrong-square,
  wrong color/case. GPT reasoned row-by-row; Claude described globally. Anthropic docs cite limited
  spatial reasoning (clock face / chess piece positions). Chess Lens built on VideoDB.
- Keep it model-neutral and fair (this channel is BYO-model). It's a "test for your task" story.

## Next steps (gated on your OK)
1. Confirm title + script.
2. Generate VO (same channel voice `86SOy9VyOePcRbIneYDa`, eleven_v3) — **paid; needs your go-ahead.**
3. Transcribe → cues → build (reuse the chess-board/leaderboard components) → 1 AI hero image →
   assemble → QA → render. Pipeline is turnkey from Ep1.
