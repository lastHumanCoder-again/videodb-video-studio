#!/usr/bin/env python3
"""Analyze a reference video so its style can be replicated (the `replicate` pipeline).

Two layers:
  1. ffmpeg (always, local, free): format, scene cuts + pacing, sampled frames,
     color palette, extracted audio track.
  2. VideoDB (optional, BYO key): uploads the reference, indexes spoken words
     (transcript) and scenes (per-shot visual descriptions) — the vision layer.
     Uses your VideoDB account credits: get the user's explicit go-ahead first.

Usage: python3 analyze_reference.py <video.mp4 | http(s) URL> [--out DIR] [--no-videodb]
                                    [--scene-threshold 0.3] [--max-frames 24]

Output (default ./reference-analysis/):
  analysis.json     mechanical facts: dims, fps, duration, cut times, pacing stats
  frames/           one jpg per scene cut (agent reads these for style analysis)
  palette.png       dominant-color palette strip
  audio.mp3         extracted audio (transcribe with: npx hyperframes transcribe audio.mp3)
  transcript.txt    (VideoDB) spoken-word transcript
  videodb_scenes.json  (VideoDB) per-shot visual descriptions
Next step: write REPLICATION.md from these artifacts using references/pipelines/replicate.md.

A URL source requires the VideoDB layer (ffmpeg needs a local file) — either
download the video first, or provide VIDEO_DB_API_KEY.
"""
import json
import pathlib
import re
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _common import get_env

STYLE_PROMPT = (
    "Describe this scene's visual design so it can be replicated with different content: "
    "layout and composition, typography (case, weight, approximate size), color palette "
    "(background, text, accent), motion and animation, graphic elements (cards, charts, "
    "captions, logos), and overall energy. Ignore the specific subject matter."
)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def ffmpeg_layer(src, out, threshold, max_frames):
    probe = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height,r_frame_rate:format=duration",
                 "-of", "json", src])
    if probe.returncode != 0:
        sys.exit(f"ffprobe failed: {probe.stderr[:300]}")
    meta = json.loads(probe.stdout)
    stream = meta["streams"][0]
    w, h = stream["width"], stream["height"]
    num, den = stream["r_frame_rate"].split("/")
    fps = round(int(num) / int(den), 2)
    duration = round(float(meta["format"]["duration"]), 2)

    print(f"[ffmpeg] {w}x{h} @ {fps}fps, {duration}s — detecting scene cuts...")
    det = run(["ffmpeg", "-i", src, "-vf", f"select='gt(scene,{threshold})',showinfo",
               "-f", "null", "-"])
    cuts = [round(float(m), 2) for m in re.findall(r"pts_time:([0-9.]+)", det.stderr)]
    intervals = [round(b - a, 2) for a, b in zip([0.0] + cuts, cuts + [duration])]
    avg_cut = round(sum(intervals) / len(intervals), 2) if intervals else duration

    frames_dir = out / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    sample_times = [0.0] + cuts
    # Animated compositions crossfade instead of hard-cutting; if detection is
    # sparse, add a uniform time grid so the style is still fully sampled.
    if len(cuts) < duration / 8:
        grid = [round(t * 2.5, 2) for t in range(1, int(duration / 2.5))]
        sample_times = sorted(set(sample_times + grid))
        print(f"[ffmpeg] sparse cuts — added {len(grid)} time-grid samples (soft transitions?)")
    if len(sample_times) > max_frames:  # even subsample, keep first + last
        step = len(sample_times) / max_frames
        sample_times = [sample_times[int(i * step)] for i in range(max_frames)]
    for t in sample_times:
        run(["ffmpeg", "-loglevel", "error", "-ss", str(min(t + 0.05, duration - 0.1)),
             "-i", src, "-frames:v", "1", "-vf", "scale=640:-2",
             str(frames_dir / f"t{t:07.2f}.jpg"), "-y"])
    print(f"[ffmpeg] {len(cuts)} cuts (avg {avg_cut}s/cut), {len(sample_times)} frames -> {frames_dir}")

    run(["ffmpeg", "-loglevel", "error", "-i", src,
         "-vf", "fps=1,scale=160:-2,palettegen=max_colors=8",
         str(out / "palette.png"), "-y"])

    has_audio = run(["ffprobe", "-v", "error", "-select_streams", "a:0",
                     "-show_entries", "stream=codec_name", "-of", "csv=p=0", src]).stdout.strip() != ""
    if has_audio:
        run(["ffmpeg", "-loglevel", "error", "-i", src, "-vn", "-q:a", "4",
             str(out / "audio.mp3"), "-y"])

    analysis = {
        "source": src, "width": w, "height": h, "fps": fps, "duration": duration,
        "aspect": "9:16" if h > w else "16:9" if w > h else "1:1",
        "scene_threshold": threshold, "n_cuts": len(cuts), "cut_times": cuts,
        "avg_seconds_per_cut": avg_cut,
        "cuts_in_first_3s": sum(1 for c in cuts if c <= 3.0),
        "has_audio": has_audio,
    }
    (out / "analysis.json").write_text(json.dumps(analysis, indent=2))
    print(f"[ffmpeg] wrote {out / 'analysis.json'}")
    return analysis


def videodb_layer(src, out):
    key = get_env("VIDEO_DB_API_KEY") or get_env("VIDEODB_API_KEY")
    if not key:
        print("\n[videodb] VIDEO_DB_API_KEY not set — skipping the vision layer (optional).\n"
              "          With a key this uploads the reference and returns per-shot visual\n"
              "          descriptions + a transcript. Add to workspace/.env to enable.")
        return False
    try:
        import videodb
    except ImportError:
        print("\n[videodb] key found but the SDK is missing — run: pip install videodb")
        return False

    print("[videodb] connecting (note: indexing uses your VideoDB account credits)")
    conn = videodb.connect(api_key=key)
    if re.match(r"https?://", src):
        video = conn.upload(url=src)
    else:
        video = conn.upload(file_path=src)
    print(f"[videodb] uploaded, video id: {video.id}")

    try:
        video.index_spoken_words()
        transcript = video.get_transcript_text()
        (out / "transcript.txt").write_text(transcript or "")
        print(f"[videodb] transcript -> {out / 'transcript.txt'} ({len(transcript or '')} chars)")
    except Exception as e:
        print(f"[videodb] spoken-word indexing failed (video may have no speech): {e}")

    # time-based extraction: uniform coverage; shot-based misses the soft
    # crossfades that motion-graphics videos use instead of hard cuts
    index_id = video.index_scenes(extraction_type="time",
                                  extraction_config={"time": 5},
                                  prompt=STYLE_PROMPT)
    print(f"[videodb] scene index {index_id} building...")
    scenes = None
    for _ in range(60):
        time.sleep(5)
        try:
            scenes = video.get_scene_index(index_id)
            if scenes:
                break
        except Exception:
            pass
    if not scenes:
        sys.exit("[videodb] scene index did not become ready — retry later with get_scene_index()")
    (out / "videodb_scenes.json").write_text(json.dumps(
        {"video_id": video.id, "scene_index_id": index_id, "scenes": scenes}, indent=2))
    print(f"[videodb] {len(scenes)} scene descriptions -> {out / 'videodb_scenes.json'}")
    return True


def main():
    args = sys.argv[1:]
    def flag(name, default=None):
        if name in args:
            i = args.index(name)
            v = args[i + 1]
            del args[i:i + 2]
            return v
        return default

    out = pathlib.Path(flag("--out", "reference-analysis"))
    threshold = float(flag("--scene-threshold", "0.3"))
    max_frames = int(flag("--max-frames", "24"))
    no_videodb = "--no-videodb" in args
    if no_videodb:
        args.remove("--no-videodb")
    if len(args) != 1:
        sys.exit(__doc__)
    src = args[0]
    out.mkdir(parents=True, exist_ok=True)

    is_url = bool(re.match(r"https?://", src))
    if is_url and no_videodb:
        sys.exit("A URL source needs the VideoDB layer — download the file first or drop --no-videodb.")
    if not is_url and not pathlib.Path(src).is_file():
        sys.exit(f"Not found: {src}")

    if not is_url:
        ffmpeg_layer(src, out, threshold, max_frames)
    used_vdb = False if no_videodb else videodb_layer(src, out)
    if is_url and not used_vdb:
        sys.exit("URL source and no usable VideoDB layer — nothing analyzed.")

    print("\nDone. Next: read frames/ (+ videodb_scenes.json if present) and write "
          "REPLICATION.md per references/pipelines/replicate.md")


if __name__ == "__main__":
    main()
