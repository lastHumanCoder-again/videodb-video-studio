#!/usr/bin/env python3
"""ElevenLabs voiceover from a segments.json spec (BYO key, optional).

Looks for segments.json in ./voiceover/ then ./ (or pass a path). MP3s are
written next to the spec, one per segment.

Usage: python3 tts.py                      # all segments (skips existing mp3s)
       python3 tts.py seg1_hook            # regenerate named segment(s)
       python3 tts.py path/to/segments.json [seg ...]

segments.json:
  {
    "voice_id": "...",                  # required for API generation
    "model": "eleven_v3",
    "settings": {"stability": 0.5, "similarity_boost": 0.75, "use_speaker_boost": true},
    "segments": {"seg1_hook": "[confident] Line one...", ...}
  }

No ELEVENLABS_API_KEY? The script prints every segment's text as a paste-ready
block — generate the VO in any tool and save as <segment>.mp3 beside the spec.
Never call this with a key present without the user's explicit go-ahead: TTS
generation is a paid API call.
"""
import hashlib
import json
import pathlib
import sys
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _common import get_env, no_key_banner


def find_spec(argv):
    if argv and argv[0].endswith(".json"):
        return pathlib.Path(argv[0]), argv[1:]
    for cand in (pathlib.Path("voiceover/segments.json"), pathlib.Path("segments.json")):
        if cand.is_file():
            return cand, argv
    sys.exit("No segments.json found in ./voiceover/ or ./ — pass a path explicitly.")


def main():
    spec_path, rest = find_spec(sys.argv[1:])
    spec = json.loads(spec_path.read_text())
    segments = spec["segments"]
    out_dir = spec_path.parent
    only = set(rest)

    api_key = get_env("ELEVENLABS_API_KEY")
    if not api_key:
        print(no_key_banner("ELEVENLABS_API_KEY", "generate these voiceover MP3s via ElevenLabs"))
        todo = [n for n in segments if (not only or n in only) and not (out_dir / f"{n}.mp3").exists()]
        if not todo:
            print("All segment MP3s already exist — nothing to generate.")
            return
        print(f"Generate {len(todo)} segment(s) and save each as {out_dir}/<name>.mp3:\n")
        for name in todo:
            print(f"--- {name}.mp3 ---\n{segments[name]}\n")
        print("Then continue with: npx hyperframes transcribe <each mp3> and extract_cues.py")
        return

    voice_id = spec.get("voice_id") or get_env("ELEVENLABS_VOICE_ID")
    if not voice_id:
        sys.exit("segments.json has no voice_id and ELEVENLABS_VOICE_ID is not set.")
    model = spec.get("model", "eleven_v3")
    settings = spec.get("settings", {"stability": 0.5, "similarity_boost": 0.75, "use_speaker_boost": True})

    for name, text in segments.items():
        if only and name not in only:
            continue
        dest = out_dir / f"{name}.mp3"
        if not only and dest.exists():
            print("skip", name)
            continue
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128"
        body = json.dumps({"text": text, "model_id": model, "voice_settings": settings}).encode()
        req = urllib.request.Request(url, data=body, method="POST",
            headers={"xi-api-key": api_key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
        except urllib.error.HTTPError as e:
            print("ERR", name, e.code, e.read().decode()[:300])
            sys.exit(1)
        dest.write_bytes(data)
        print("OK", name, len(data), "md5", hashlib.md5(data).hexdigest()[:8])


if __name__ == "__main__":
    main()
