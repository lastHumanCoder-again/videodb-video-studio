#!/usr/bin/env python3
"""Extract scene cue times from word-level VO transcripts. No API key needed.

Reads cues_spec.json + <segment>.transcript.json files from a voiceover dir,
writes cues.json one level up (project root). Run AFTER transcribing every
VO clip with `npx hyperframes transcribe <seg>.mp3`.

Usage: python3 extract_cues.py [voiceover_dir]   # default: ./voiceover, else ./

cues_spec.json:
  {
    "seg1_hook": {"s_open": 0.0, "s_question": "here's a photo", ...},
    ...
  }
Each value is either 0.0 (segment start) or a phrase; the cue time is the
start of the first word of that phrase in the transcript. NEVER estimate
these times by hand — a visual leading the voice is the amateur tell.
"""
import json
import pathlib
import re
import sys


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def cue(here, seg, phrase):
    w = json.load(open(here / f"{seg}.transcript.json"))
    toks = [norm(x["text"]) for x in w]
    pt = [norm(t) for t in phrase.split() if norm(t)]
    for i in range(len(toks) - len(pt) + 1):
        if toks[i:i + len(pt)] == pt:
            return round(w[i]["start"], 2)
    return None


def main():
    if len(sys.argv) > 1:
        here = pathlib.Path(sys.argv[1])
    elif pathlib.Path("voiceover/cues_spec.json").is_file():
        here = pathlib.Path("voiceover")
    else:
        here = pathlib.Path(".")
    spec_path = here / "cues_spec.json"
    if not spec_path.is_file():
        sys.exit(f"No cues_spec.json in {here} — write one (see script docstring).")
    CUES = json.loads(spec_path.read_text())

    missing = [s for s in CUES if not (here / f"{s}.transcript.json").is_file()]
    if missing:
        sys.exit("Missing transcripts for: " + ", ".join(missing) +
                 "\nRun: npx hyperframes transcribe <seg>.mp3   (for each segment)")

    out, not_found = {}, 0
    print(f"{'segment':<18}{'beat':<16}{'cue':<26}{'time'}")
    print("-" * 66)
    for seg, beats in CUES.items():
        w = json.load(open(here / f"{seg}.transcript.json"))
        out[seg] = {"_dur": round(w[-1]["end"], 2)}
        for label, ph in beats.items():
            t = 0.0 if ph == 0.0 else cue(here, seg, ph)
            out[seg][label] = t
            if t is None:
                not_found += 1
            print(f"{seg:<18}{label:<16}{str(ph):<26}{t}{'   <<< NOT FOUND' if t is None else ''}")

    dest = here.parent / "cues.json" if here.name == "voiceover" else here / "cues.json"
    json.dump(out, open(dest, "w"), indent=2)
    print(f"\nwrote {dest}")
    if not_found:
        sys.exit(f"{not_found} cue(s) NOT FOUND — fix the phrases in cues_spec.json and rerun.")


if __name__ == "__main__":
    main()
