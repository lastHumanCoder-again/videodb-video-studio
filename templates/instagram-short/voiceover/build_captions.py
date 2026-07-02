#!/usr/bin/env python3
"""Karaoke caption data (assets/captions.js) from the VO transcript."""
import json, pathlib
HERE = pathlib.Path(__file__).parent
ASSETS = HERE.parent / "assets"
w = json.load(open(HERE / "vo.transcript.json"))
MERGES = {}; SKIP = set()
# words 24-31 ("show me the referee's call at minute 67") are typed in the search bar -> not captioned
# words 74-76 ("VideoDB with TinyFish") shown as the closing lockup -> not captioned
CHUNKS = [
    (0, 6), (7, 11),            # hook
    (12, 17), (18, 23),         # 90% problem
    (32, 36), (37, 42),         # link vs moment
    (43, 48),                   # collab
    (49, 53), (54, 61), (62, 63),  # how / stitch / already edited
    (64, 70), (71, 73),         # thesis
]
words, chunks = [], []
for ci, (a, b) in enumerate(CHUNKS):
    chunks.append({"i": ci, "start": round(w[a]["start"], 3), "end": None})
    i = a
    while i <= b:
        if i in SKIP: i += 1; continue
        text, end = w[i]["text"], w[i]["end"]
        if i in MERGES:
            j, disp = MERGES[i]; text, end = disp, w[j]["end"]
        words.append({"id": f"cw{i}", "text": text.upper(), "start": round(w[i]["start"], 3), "end": round(end, 3), "chunk": ci})
        i += 1
for k in range(len(chunks)):
    nxt = chunks[k + 1]["start"] if k + 1 < len(chunks) else 1e9
    last_word_end = max(x["end"] for x in words if x["chunk"] == k)
    # don't let a caption linger across a gap (e.g. the typed query / closing lockup)
    chunks[k]["end"] = round(min(nxt, last_word_end + 0.7), 3)
ASSETS.mkdir(exist_ok=True)
(ASSETS / "captions.js").write_text("window.WW_CAPS = " + json.dumps({"chunks": chunks, "words": words}) + ";\n")
print("wrote captions.js ·", len(chunks), "chunks ·", len(words), "words")
for c in chunks:
    print(f"  {c['i']:2d}  {c['start']:6.2f}-{c['end']:6.2f}  " + " ".join(x["text"] for x in words if x["chunk"] == c["i"]))
