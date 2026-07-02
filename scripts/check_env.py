#!/usr/bin/env python3
"""Print status of optional API keys and setup state. Always safe to run."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _common import WORKSPACE, get_env, load_config

KEYS = {
    "ELEVENLABS_API_KEY": "voiceover generation (scripts/tts.py)",
    "KIE_API_KEY": "AI image generation (scripts/gen_image.py)",
}

cfg = load_config()
print("Setup:", "config.json OK" if cfg else "NOT RUN — run scripts/setup.py first")
if cfg:
    print("  projects_dir:", cfg.get("projects_dir"))
    print("  brand:", cfg.get("brand"))

print("\nOptional API keys (everything works without them):")
for key, enables in KEYS.items():
    val = get_env(key)
    print(f"  {'set     ' if val else 'not set (optional)'}  {key:<22} -> {enables}")
print(f"\nKeys are read from {WORKSPACE / '.env'}, then ./.env, then the environment.")
