#!/bin/bash
# Turnkey live demo runner. Run this from Terminal.app (which has Screen
# Recording + Accessibility + Input Monitoring granted).
set -e
cd "$(dirname "$0")"
set -a; . ./.env; set +a
echo "== VideoDB Record & Replay — live demo =="
echo "Do not touch the mouse/keyboard once STEP 3 starts (it drives TextEdit)."
echo
exec uv run python run_demo.py
