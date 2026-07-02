# Environment & optional API keys

**Nothing in this skill requires an API key.** Every template is a finished worked example that renders locally, and every generation step has a prompt-only fallback. Keys just remove manual steps.

## The env chain

Scripts resolve keys in this order (first hit wins):

1. `<skill>/workspace/.env` — your global keys (`chmod 600`, gitignored)
2. `./.env` in the project you're running from — per-project override
3. The process environment

## The keys

| Key | Script it enables | What happens without it |
|---|---|---|
| `ELEVENLABS_API_KEY` | `scripts/tts.py` — voiceover from `voiceover/segments.json` | Prints each segment's text as a paste-ready block; generate the VO in any tool, save as `voiceover/<segment>.mp3` |
| `ELEVENLABS_VOICE_ID` | default voice when `segments.json` has no `voice_id` | — |
| `KIE_API_KEY` | `scripts/gen_image.py` — AI images (Kie.ai nano-banana-pro) | Prints the prompt + aspect ratio as a paste-ready block; save the image to the target path |
| `VIDEO_DB_API_KEY` | `scripts/analyze_reference.py` — the vision layer for the `replicate` pipeline (upload reference, per-scene visual descriptions + transcript; needs `pip install videodb`) | ffmpeg layer still runs on local files (format, pacing, frames, palette); only URL sources and scene descriptions need the key |

Everything else — scaffolding, transcription (`npx hyperframes transcribe`, local Whisper), cue extraction, building, lint/validate/inspect, rendering — is fully local and keyless.

## Adding a key

```bash
echo 'ELEVENLABS_API_KEY=...' >> ~/.claude/skills/videodb-video-studio/workspace/.env
chmod 600 ~/.claude/skills/videodb-video-studio/workspace/.env
python3 scripts/check_env.py   # confirm
```

## The paid-generation rule (for agents)

With keys present, `tts.py` and `gen_image.py` make **paid API calls**. Never run them without the user's explicit go-ahead **in the current conversation turn**. Approval for one job does not carry to the next. When in doubt, default to the prompt-only fallback.

## Prerequisites (all pipelines)

- Node.js ≥ 18 — HyperFrames CLI runs via each project's `npx hyperframes`
- Python 3.9+ — scaffolder + generation scripts
- ffmpeg — QA frame extraction
- The `deck` template additionally needs Playwright's Chromium: `npx playwright install chromium`

`scripts/setup.py` checks these and prints install hints (non-blocking).
