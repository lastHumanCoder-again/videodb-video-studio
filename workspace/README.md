# workspace/

Local state for the videodb-video-studio skill. Everything here except this README is gitignored.

- `config.json` — written by `scripts/setup.py`. Holds your projects directory, brand config path, and which optional API keys are configured. Never edit by hand; re-run setup to change it.
- `.env` — optional API keys, one per line (`chmod 600`):
  - `ELEVENLABS_API_KEY=...` — enables `scripts/tts.py` (voiceover generation)
  - `KIE_API_KEY=...` — enables `scripts/gen_image.py` (AI image generation)

No keys? Everything still works. Scripts print paste-ready prompts and tell you where to drop the files you generate yourself. See `references/env-setup.md`.
