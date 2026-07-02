#!/usr/bin/env python3
"""Scaffold a new video project from a pipeline template.

Usage: python3 new_project.py <pipeline> <slug> [--dir PATH] [--brand PATH] [--install]

  <pipeline>   one of the dirs in templates/ (youtube-longform, instagram-short,
               split-ugc, deck, demo-recording, highlights)
  <slug>       kebab-case project name, becomes the directory + composition id
  --dir        where to create the project (default: config.json projects_dir, else cwd)
  --brand      brand.json to apply (default: config.json brand, else bundled VideoDB)
  --install    run `npm install` in the new project (default: just print the command)

What it does: copies the full worked example, re-slugs the composition id
(verified by grep — zero leftovers), rewrites BRAND-annotated color values
from brand.json, copies the brand logo, prints pipeline next steps.
Always scaffold with this script — hand-copied templates drift.
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _common import SKILL_DIR, load_brand, load_config

TEXT_EXT = {".html", ".css", ".js", ".json", ".py", ".md", ".mjs", ".txt", ".toml", ".yaml", ".yml"}
SKIP_DIRS = {"node_modules", "renders", "out", "__pycache__", ".git"}

HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
ANNOT_RE = re.compile(r"brand:([a-z]+)")


def iter_text_files(root):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_EXT and not (set(p.parts) & SKIP_DIRS):
            yield p


def reslug(root, old, new):
    changed = 0
    for p in iter_text_files(root):
        try:
            text = p.read_text()
        except UnicodeDecodeError:
            continue
        if old in text:
            p.write_text(text.replace(old, new))
            changed += 1
    leftovers = [str(p.relative_to(root)) for p in iter_text_files(root)
                 if old in p.read_text(errors="ignore")]
    return changed, leftovers


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def apply_brand(root, colors):
    """Two passes. (1) Inside BRAND:START/END blocks, rewrite hex values on
    brand:<token> annotated lines — collecting each token's ORIGINAL value.
    (2) Globally replace those original values everywhere (hex, and rgba/rgb
    triples), so accent literals in inline JS / gradients / box-shadow glows
    follow the token too. Colors NOT annotated in any BRAND block are never
    touched (that's how a template keeps a deliberate secondary literal)."""
    rewritten = 0
    originals = {}  # original hex (lowercase) -> token
    for p in iter_text_files(root):
        try:
            lines = p.read_text().splitlines(keepends=True)
        except UnicodeDecodeError:
            continue
        in_block, dirty = False, False
        for i, line in enumerate(lines):
            if "BRAND:START" in line:
                in_block = True
                continue
            if "BRAND:END" in line:
                in_block = False
                continue
            if not in_block:
                continue
            m = ANNOT_RE.search(line)
            if not m:
                continue
            token = m.group(1)
            if token not in colors:
                continue
            old = HEX_RE.search(line)
            if not old:
                continue
            if originals.setdefault(old.group(0).lower(), token) != token:
                originals[old.group(0).lower()] = None  # ambiguous: two tokens share a value
            new_line, n = HEX_RE.subn(colors[token], line, count=1)
            if n:
                lines[i] = new_line
                rewritten += 1
                dirty = True
        if dirty:
            p.write_text("".join(lines))

    # Pass 2: chase the original values through the whole project.
    subs = []
    for old_hex, token in originals.items():
        if token is None or colors[token].lower() == old_hex:
            continue
        subs.append((re.compile(re.escape(old_hex), re.IGNORECASE), colors[token]))
        r, g, b = hex_to_rgb(old_hex)
        nr, ng, nb = hex_to_rgb(colors[token])
        subs.append((re.compile(rf"(rgba?\()\s*{r}\s*,\s*{g}\s*,\s*{b}\b"), rf"\g<1>{nr},{ng},{nb}"))
    if subs:
        for p in iter_text_files(root):
            try:
                text = p.read_text()
            except UnicodeDecodeError:
                continue
            new_text = text
            for pat, repl in subs:
                new_text = pat.sub(repl, new_text)
            if new_text != text:
                p.write_text(new_text)
                rewritten += 1
    return rewritten


def main():
    args = [a for a in sys.argv[1:]]
    def flag(name):
        if name in args:
            i = args.index(name)
            val = args[i + 1]
            del args[i:i + 2]
            return val
        return None

    out_dir = flag("--dir")
    brand_arg = flag("--brand")
    install = "--install" in args
    if install:
        args.remove("--install")
    if len(args) != 2:
        templates = sorted(p.name for p in (SKILL_DIR / "templates").iterdir() if p.is_dir())
        sys.exit(f"Usage: new_project.py <pipeline> <slug> [--dir PATH] [--brand PATH] [--install]\n"
                 f"Pipelines: {', '.join(templates)}")
    pipeline, slug = args
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        sys.exit(f"Slug must be kebab-case (got: {slug})")

    template = SKILL_DIR / "templates" / pipeline
    if not template.is_dir():
        sys.exit(f"Unknown pipeline '{pipeline}'. Available: "
                 + ", ".join(sorted(p.name for p in (SKILL_DIR / 'templates').iterdir() if p.is_dir())))
    manifest = json.loads((template / "template.json").read_text())

    cfg = load_config()
    if out_dir is None:
        out_dir = (cfg or {}).get("projects_dir") or "."
    root = (pathlib.Path.cwd() if out_dir == "." else pathlib.Path(out_dir).expanduser()) / slug
    if root.exists():
        sys.exit(f"{root} already exists — pick another slug or remove it.")

    brand, brand_path = load_brand(brand_arg)
    print(f"Scaffolding {pipeline} -> {root}")
    shutil.copytree(template, root, ignore=shutil.ignore_patterns(*SKIP_DIRS, ".DS_Store"))

    old_slug = manifest["slug"]
    changed, leftovers = reslug(root, old_slug, slug)
    print(f"Re-slugged '{old_slug}' -> '{slug}' in {changed} file(s)")
    if leftovers:
        sys.exit("RE-SLUG INCOMPLETE, leftovers in: " + ", ".join(leftovers))

    n = apply_brand(root, brand.get("colors", {}))
    print(f"Applied brand '{brand.get('name')}' ({brand_path.name}): {n} color value(s) rewritten")
    shutil.copy(brand_path, root / "brand.json")
    logo = brand_path.parent / brand.get("logo", "")
    if brand.get("logo") and logo.is_file():
        shutil.copy(logo, root / logo.name)

    if (root / "package.json").is_file():
        if install:
            subprocess.run(["npm", "install"], cwd=root, check=False)
        else:
            print(f"\nNow run: cd {root} && npm install")

    print("\nNext steps:")
    for i, step in enumerate(manifest.get("next_steps", []), 1):
        print(f"  {i}. {step}")


if __name__ == "__main__":
    main()
