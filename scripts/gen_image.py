#!/usr/bin/env python3
"""Kie.ai nano-banana-pro image generation (BYO key, optional).

Usage: python3 gen_image.py out.png 16:9 "prompt"
Valid aspect ratios: 16:9, 9:16, 4:5, 1:1, 2.39:1

Uses curl (not urllib) deliberately — Kie's WAF blocks Python's urllib.

No KIE_API_KEY? Prints the prompt as a paste-ready block: generate the image
in any tool and save it to the output path. Never call this with a key present
without the user's explicit go-ahead: image generation is a paid API call.
"""
import json
import pathlib
import re
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _common import get_env, no_key_banner

out, aspect, prompt = sys.argv[1], sys.argv[2], sys.argv[3]

KEY = get_env("KIE_API_KEY")
if not KEY:
    print(no_key_banner("KIE_API_KEY", "generate this image via Kie.ai nano-banana-pro"))
    print(f"--- image prompt (aspect {aspect}) ---\n{prompt}\n")
    print(f"Save the generated image to: {out}")
    sys.exit(0)


def curl(args):
    raw = subprocess.check_output(
        ["curl", "-s", "-H", f"Authorization: Bearer {KEY}"] + args, timeout=90)
    return json.loads(raw)


res = curl(["-X", "POST", "https://api.kie.ai/api/v1/jobs/createTask",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({"model": "nano-banana-pro",
                              "input": {"prompt": prompt, "aspectRatio": aspect}})])
task = res.get("data", {}).get("taskId") or res.get("data", {}).get("task_id")
if not task:
    print("CREATE FAIL", json.dumps(res)[:400]); sys.exit(1)
print("task", task)


def find_url(obj):
    urls = []
    def walk(o):
        if isinstance(o, str):
            for m in re.findall(r"https?://[^\s\"']+\.(?:png|jpg|jpeg|webp)", o):
                urls.append(m)
        elif isinstance(o, dict):
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(obj)
    return urls


for _ in range(60):
    time.sleep(4)
    info = curl(["https://api.kie.ai/api/v1/jobs/recordInfo?taskId=" + task])
    d = info.get("data", {})
    st = str(d.get("state", d.get("status", ""))).lower()
    rj = d.get("resultJson")
    if isinstance(rj, str):
        try: d["_rj"] = json.loads(rj)
        except Exception: pass
    if st in ("success", "completed", "succeeded"):
        urls = find_url(d)
        if not urls:
            print("DONE but no url:", json.dumps(d)[:500]); sys.exit(1)
        url = urls[0]
        subprocess.check_call(["curl", "-s", "-L", "-o", out, url])
        print("OK", out, "<-", url); sys.exit(0)
    if st in ("fail", "failed", "error"):
        print("GEN FAIL", json.dumps(d)[:400]); sys.exit(1)
    print("...", st or "queued")
print("TIMEOUT"); sys.exit(1)
