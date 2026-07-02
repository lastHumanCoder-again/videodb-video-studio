#!/usr/bin/env bash
# videodb-video-studio installer / verifier.
# Works whether you cloned into ~/.claude/skills/ or unzipped a release there.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"
TARGET="$SKILLS_DIR/videodb-video-studio"

echo "videodb-video-studio installer"
echo "------------------------------"

if [ "$HERE" != "$TARGET" ]; then
  echo "Note: this copy lives at $HERE"
  echo "For Claude Code to pick it up as a skill it should be at:"
  echo "  $TARGET"
  read -r -p "Copy it there now? [y/N] " ans
  if [ "${ans:-n}" = "y" ] || [ "${ans:-n}" = "Y" ]; then
    mkdir -p "$SKILLS_DIR"
    cp -R "$HERE" "$TARGET"
    echo "Copied. Continuing checks against $TARGET"
    HERE="$TARGET"
  else
    echo "Skipping copy — CLI-toolkit mode still works from here."
  fi
fi

chmod 600 "$HERE/workspace/.env" 2>/dev/null || true

echo
python3 "$HERE/scripts/check_env.py" || true

echo
echo "Next:"
echo "  1. python3 \"$HERE/scripts/setup.py\"        # one-time config (projects dir, brand)"
echo "  2. Restart Claude Code, then say e.g.:"
echo "       \"make me an instagram short about semantic video search\""
echo "     Or use it as a plain CLI:"
echo "       python3 \"$HERE/scripts/new_project.py\" instagram-short my-first-short"
