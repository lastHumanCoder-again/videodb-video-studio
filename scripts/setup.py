#!/usr/bin/env python3
"""First-run setup gate. Writes workspace/config.json (never edit that by hand;
re-run this script to change settings).

Interactive: python3 setup.py
Flags (non-interactive, any subset):
  --projects-dir PATH    where new video projects are scaffolded (default ~/videos;
                         use "." to scaffold into the current directory each time)
  --brand PATH           custom brand.json (default: bundled VideoDB brand)
  --yes                  accept defaults for anything not passed

API keys are OPTIONAL and never requested by flags — add them to
workspace/.env yourself (see workspace/README.md). Everything works without.
"""
import json
import pathlib
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _common import SKILL_DIR, WORKSPACE, DEFAULT_BRAND, get_env


def check_prereqs():
    print("\nPrerequisites (non-blocking):")
    for cmd, hint in [
        ("node", "install Node.js >= 18: https://nodejs.org"),
        ("npx", "ships with Node.js"),
        ("python3", "you're running it, so OK"),
        ("ffmpeg", "brew install ffmpeg  (used for QA frame extraction)"),
    ]:
        path = shutil.which(cmd)
        print(f"  {'OK ' if path else 'MISSING'}  {cmd:<8}" + ("" if path else f"  -> {hint}"))
    try:
        v = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=10).stdout.strip()
        print(f"  node version: {v} (need >= 18)")
    except Exception:
        pass


def key_status():
    return {
        "ELEVENLABS_API_KEY": bool(get_env("ELEVENLABS_API_KEY")),
        "KIE_API_KEY": bool(get_env("KIE_API_KEY")),
    }


def main():
    args = sys.argv[1:]
    def flag(name):
        if name in args:
            i = args.index(name)
            return args[i + 1] if i + 1 < len(args) else None
        return None

    yes = "--yes" in args
    projects_dir = flag("--projects-dir")
    brand = flag("--brand")

    interactive = sys.stdin.isatty() and not yes and (projects_dir is None or brand is None)
    if interactive:
        if projects_dir is None:
            raw = input("Projects directory for new videos [~/videos, or '.' for cwd-mode]: ").strip()
            projects_dir = raw or "~/videos"
        if brand is None:
            raw = input(f"Brand config path [default: bundled VideoDB brand]: ").strip()
            brand = raw or None
    if projects_dir is None:
        projects_dir = "~/videos"

    if projects_dir != ".":
        projects_dir = str(pathlib.Path(projects_dir).expanduser())
        pathlib.Path(projects_dir).mkdir(parents=True, exist_ok=True)

    brand_path = str(pathlib.Path(brand).expanduser().resolve()) if brand else str(DEFAULT_BRAND)
    if not pathlib.Path(brand_path).is_file():
        sys.exit(f"Brand config not found: {brand_path}")

    WORKSPACE.mkdir(exist_ok=True)
    keys = key_status()
    config = {
        "version": 1,
        "projects_dir": projects_dir,
        "brand": brand_path,
        "keys": {k: ("set" if v else "not set (optional)") for k, v in keys.items()},
    }
    cfg_path = WORKSPACE / "config.json"
    cfg_path.write_text(json.dumps(config, indent=2) + "\n")
    env_path = WORKSPACE / ".env"
    if env_path.exists():
        env_path.chmod(0o600)

    print(f"\nWrote {cfg_path}")
    print(json.dumps(config, indent=2))
    print("\nOptional API keys:", ", ".join(f"{k}={'set' if v else 'not set'}" for k, v in keys.items()))
    if not any(keys.values()):
        print("No keys — that's fine. VO/images fall back to paste-ready prompts;")
        print(f"add keys later in {env_path} (see workspace/README.md).")
    check_prereqs()
    print("\nSetup complete. Scaffold your first project:")
    print('  python3 "' + str(SKILL_DIR / "scripts" / "new_project.py") + '" instagram-short my-first-short')


if __name__ == "__main__":
    main()
