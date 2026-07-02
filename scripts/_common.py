#!/usr/bin/env python3
"""Shared utilities for videodb-video-studio scripts.

Env chain (first hit wins per key):
  1. <skill>/workspace/.env
  2. ./.env (project-local, next to where you run the script)
  3. os.environ
Missing keys are NOT errors — callers print a prompt-only fallback and exit 0.
"""
import json
import os
import pathlib

SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
WORKSPACE = SKILL_DIR / "workspace"
DEFAULT_BRAND = SKILL_DIR / "assets" / "brand" / "brand.json"


def _parse_env_file(path):
    vals = {}
    if not path.is_file():
        return vals
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        vals[k.strip()] = v.strip().strip('"').strip("'")
    return vals


def get_env(key):
    """Resolve key through the env chain. Returns None if unset everywhere."""
    for source in (
        _parse_env_file(WORKSPACE / ".env"),
        _parse_env_file(pathlib.Path.cwd() / ".env"),
        os.environ,
    ):
        if source.get(key):
            return source[key]
    return None


def load_config():
    """workspace/config.json written by setup.py, or None if setup never ran."""
    cfg = WORKSPACE / "config.json"
    if cfg.is_file():
        return json.loads(cfg.read_text())
    return None


def load_brand(path=None):
    """Load brand.json (explicit path > config.json brand > VideoDB default)."""
    if path is None:
        cfg = load_config()
        if cfg and cfg.get("brand"):
            path = cfg["brand"]
    p = pathlib.Path(path) if path else DEFAULT_BRAND
    return json.loads(p.read_text()), p


def no_key_banner(key_name, enables):
    return (
        f"\n[no key] {key_name} is not set — that's fine, nothing is broken.\n"
        f"With a key this script would {enables}.\n"
        f"To add one later: echo '{key_name}=...' >> \"{WORKSPACE / '.env'}\"\n"
        f"Prompt-only fallback below — generate the assets yourself and drop them in place.\n"
    )
