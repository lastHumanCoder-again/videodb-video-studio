#!/usr/bin/env python3
"""
Turnkey live demo of open-record-replay: record -> compile -> SKILL.

Runs the REAL repo pipeline end-to-end and performs a simple, reliable UI
workflow (typing a note into TextEdit) via pyautogui so the AX hook + VideoDB
screen capture record it. Then compiles the recording into SKILL.json / SKILL.md.

MUST be run from a host with macOS Screen Recording + Accessibility + Input
Monitoring granted (e.g. Terminal.app). Reads creds from ./.env.

    ./run_demo.sh          # wrapper sources .env then runs this
"""
import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO))

SKILL_NAME = "textedit-note"
LEAD_IN = 3.0
TRIM_END = 2.0


def workflow_sync():
    """The demonstrated workflow — typing a note into a fresh TextEdit document.
    Pure keyboard after launch, so it's robust (no pixel coordinates)."""
    import pyautogui
    pyautogui.FAILSAFE = False
    # fresh TextEdit state
    subprocess.run(["killall", "TextEdit"], capture_output=True)
    time.sleep(0.6)
    subprocess.run(["osascript", "-e", 'tell application "TextEdit" to activate'], capture_output=True)
    subprocess.run(["osascript", "-e", 'tell application "TextEdit" to make new document'], capture_output=True)
    time.sleep(1.6)
    pyautogui.typewrite("Record once. Replay anywhere.", interval=0.06)
    pyautogui.press("enter")
    time.sleep(0.3)
    pyautogui.typewrite("This note was typed during a VideoDB Record & Replay capture.", interval=0.045)
    time.sleep(1.2)


async def main():
    import server
    from capture import recorder
    from compiler import compiler as C
    from registry import save_skill_md

    print(">>> STEP 1  connecting to VideoDB ...", flush=True)
    await server._ensure_connected()
    print("    connected. collection:", getattr(server.state.coll, "name", "?"), flush=True)

    print(f">>> STEP 2  record_skill('{SKILL_NAME}', lead_in={LEAD_IN}) ...", flush=True)
    rec = await recorder.record_skill(SKILL_NAME, lead_in_seconds=LEAD_IN)
    print("    mode:", rec.get("mode"), "| session:", rec.get("session_dir"), flush=True)
    if rec.get("ax_permission_warning"):
        print("    !! AX WARNING:", rec["ax_permission_warning"], flush=True)

    print(f">>> STEP 3  performing workflow after {LEAD_IN}s lead-in (typing into TextEdit) ...", flush=True)
    await asyncio.sleep(LEAD_IN)
    await asyncio.to_thread(workflow_sync)
    print("    workflow done.", flush=True)

    print(f">>> STEP 4  stop_recording(trim_end={TRIM_END}) ...", flush=True)
    stop = await recorder.stop_recording(trim_end_seconds=TRIM_END)
    vid = stop.get("video_id") or ""
    print("    events:", stop.get("event_count"), "| has_video:", stop.get("has_video"),
          "| video_id:", vid or "(none)", "| dur:", round(stop.get("duration_seconds", 0), 1), "s", flush=True)

    print(">>> STEP 5  compile_skill ...", flush=True)
    if vid and vid.lower() != "none":
        skill = await C.compile_skill(vid, SKILL_NAME)
    else:
        print("    (events-only compile — no video_id)", flush=True)
        skill = await C.compile_skill_events_only(SKILL_NAME)
    md_path = await save_skill_md(skill)
    skill["skill_md_path"] = str(md_path)

    steps = skill.get("steps", [])
    print("\n=========== RESULT ===========", flush=True)
    print("skill name :", skill.get("name"), flush=True)
    print("steps      :", len(steps), flush=True)
    print("strategy   :", skill.get("execution_strategy"), flush=True)
    print("video_id   :", vid or "(none)", flush=True)
    print("SKILL.md   :", md_path, flush=True)
    json_path = Path(md_path).parent / "SKILL.json"
    print("SKILL.json :", json_path, flush=True)

    # write a compact summary the orchestrator can read back
    summary = {
        "skill_name": SKILL_NAME,
        "video_id": vid,
        "mode": rec.get("mode"),
        "event_count": stop.get("event_count"),
        "duration_seconds": stop.get("duration_seconds"),
        "step_count": len(steps),
        "execution_strategy": skill.get("execution_strategy"),
        "skill_md_path": str(md_path),
        "skill_json_path": str(json_path),
        "session_dir": rec.get("session_dir"),
    }
    (REPO / "demo_result.json").write_text(json.dumps(summary, indent=2))
    print("\nwrote", REPO / "demo_result.json", flush=True)
    print("==============================", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
