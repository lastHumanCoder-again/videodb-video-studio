# -*- coding: utf-8 -*-
"""Generate index.html for the VideoDB auto-highlights reel (9:16).
Branded analysis UI: 3 highlight clips in a windowed player, a draw-on detection
circle over the action, "event detected" tags, a scanned-match timeline with moment
markers, a persistent 'Made with VideoDB' badge, and a VideoDB end card.
Edit CLIPS / timings below and run `python3 build.py`."""

W, H = 1080, 1920
# BRAND:START
DARK = "#0A0B0D"        # brand:canvas
PANEL = "#15161a"       # brand:card
ORANGE = "#E8551F"      # brand:accent
INK = "#0E0D0B"
# BRAND:END

# section timing -------------------------------------------------------------
INTRO_S, INTRO_E = 0.0, 2.60
END_S,   END_E   = 19.60, 24.20
ANALYSIS_S, ANALYSIS_E = 2.60, 19.60

LAND = dict(l=40, t=560, w=1000, h=563)          # landscape clip window (16:9)
VERT = dict(l=250, t=470, w=580, h=1031)         # vertical clip window (9:16)

# each highlight: src, start, dur, media in-point, framing, window rect,
# detection circle (center x/y, radius, pop time), tag, moment label, match-minute
CLIPS = [
    dict(src="clip2.mp4", ds=2.60, dur=6.00, min=1.7, pos="50% 50%", rect=LAND,
         cx=540, cy=890, r=118, pop=6.6, tag="GOAL DETECTED", conf="0.98",
         label="GOAL", time="23'", mark=23),
    dict(src="clip1.mp4", ds=8.60, dur=5.50, min=3.0, pos="50% 28%", rect=VERT,
         cx=552, cy=792, r=132, pop=11.8, tag="GOAL DETECTED", conf="0.97",
         label="GOAL", time="67'", mark=67),
    dict(src="clip3.mp4", ds=14.10, dur=5.50, min=4.0, pos="50% 50%", rect=LAND,
         cx=602, cy=856, r=118, pop=17.9, tag="BIG CHANCE", conf="0.95",
         label="BIG CHANCE", time="81'", mark=81),
]

MATCH = "Australia 2 – 0 Türkiye"
COMP = "FIFA World Cup 2026"
TOTAL = "1:56:26"
MATCH_MIN = 118.0
TL_L, TL_R = 70, 1010   # timeline track x-range
def mark_x(m): return round(TL_L + (m / MATCH_MIN) * (TL_R - TL_L))

WHOOSH = [c["ds"] for c in CLIPS] + [END_S]
BLIPS = [c["pop"] for c in CLIPS]

# ---- markup ----------------------------------------------------------------
clip_els = []
for i, c in enumerate(CLIPS, 1):
    r = c["rect"]
    clip_els.append(
        f'    <video id="cv{i}" class="clip hvid" src="{c["src"]}" data-start="{c["ds"]}" '
        f'data-duration="{c["dur"]}" data-track-index="{i-1}" data-media-start="{c["min"]}" muted playsinline '
        f'style="left:{r["l"]}px;top:{r["t"]}px;width:{r["w"]}px;height:{r["h"]}px;object-position:{c["pos"]}"></video>')
    # detection circle (ring + scanning dashed ring)
    cl = c["cx"]-c["r"]; ct = c["cy"]-c["r"]; d = c["r"]*2
    clip_els.append(
        f'    <div id="circ{i}" class="clip det-circ" data-start="{round(c["pop"]-0.05,3)}" data-duration="{round(c["ds"]+c["dur"]-c["pop"]+0.05,3)}" '
        f'data-track-index="{i+2}" style="left:{cl}px;top:{ct}px;width:{d}px;height:{d}px">'
        f'<div class="ring-dash"></div><div class="ring-solid"></div></div>')
    # detection tag chip near the circle
    tagl = c["cx"] + int(c["r"]*0.55); tagt = c["cy"] - c["r"] - 96
    clip_els.append(
        f'    <div id="tag{i}" class="clip det-tag" data-start="{round(c["pop"],3)}" data-duration="{round(c["ds"]+c["dur"]-c["pop"],3)}" '
        f'data-track-index="{i+5}" style="left:{tagl}px;top:{tagt}px"><span class="dot"></span>{c["tag"]}<span class="conf">{c["conf"]}</span></div>')
    # big moment label (lower-left of its window)
    labt = r["t"] + r["h"] + 22
    labl = r["l"]
    clip_els.append(
        f'    <div id="lab{i}" class="clip mom-label" data-start="{round(c["ds"]+0.15,3)}" data-duration="{round(c["dur"]-0.15,3)}" '
        f'data-track-index="{i+8}" style="left:{labl}px;top:{labt}px"><span class="mt">{c["time"]}</span><span class="ml">{c["label"]}</span></div>')

clips_markup = "\n".join(clip_els)

markers = "".join(
    f'<div class="tl-mark" style="left:{mark_x(c["mark"])}px"></div>'
    f'<div class="tl-mlabel" style="left:{mark_x(c["mark"])}px">{c["time"]}</div>' for c in CLIPS)

an_dur = round(ANALYSIS_E - ANALYSIS_S, 3)

# clicks / audio
audio_els = []
for j, t in enumerate(WHOOSH):
    audio_els.append(f'  <audio id="wh{j}" class="clip" src="whoosh.mp3" data-start="{round(t,3)}" data-duration="0.45" data-track-index="30" data-volume="0.5"></audio>')
for j, t in enumerate(BLIPS):
    audio_els.append(f'  <audio id="bl{j}" class="clip" src="blip.mp3" data-start="{round(t,3)}" data-duration="0.3" data-track-index="31" data-volume="0.5"></audio>')
audio_markup = "\n".join(audio_els)

# ---- timeline (GSAP) -------------------------------------------------------
tweens = []
def tw(s): tweens.append(s)

# intro
tw(f'tl.from("#intro-logo", {{opacity:0, y:-30, duration:0.5, ease:"power3.out"}}, 0.1);')
tw(f'tl.from("#intro-title .mask > span", {{yPercent:115, opacity:0, duration:0.55, ease:"power4.out"}}, 0.35);')
tw(f'tl.from("#intro-sub", {{opacity:0, y:20, duration:0.5, ease:"power3.out"}}, 0.7);')
tw(f'tl.from("#intro-scan", {{opacity:0, duration:0.3}}, 0.5);')
tw(f'tl.fromTo("#intro-scan", {{y:-160}}, {{y:170, duration:1.5, ease:"power1.inOut"}}, 0.7);')
tw(f'tl.to("#intro-scan", {{opacity:0, duration:0.3}}, {round(INTRO_E-0.4,3)});')

# persistent chrome appears with first clip
tw(f'tl.from("#topbar", {{opacity:0, y:-24, duration:0.45, ease:"power3.out"}}, {ANALYSIS_S});')
tw(f'tl.from("#timeline", {{opacity:0, y:30, duration:0.45, ease:"power3.out"}}, {round(ANALYSIS_S+0.1,3)});')
tw(f'tl.from("#badge", {{opacity:0, x:-24, duration:0.45, ease:"power3.out"}}, {round(ANALYSIS_S+0.2,3)});')
# analyzing dot pulse
tw(f'tl.to("#rec-dot", {{opacity:0.25, duration:0.5, yoyo:true, repeat:14, ease:"power1.inOut"}}, {ANALYSIS_S});')
# playhead jumps to each moment marker
for c in CLIPS:
    tw(f'tl.to("#playhead", {{left:{mark_x(c["mark"])}, duration:0.35, ease:"power2.inOut"}}, {round(c["ds"]+0.02,3)});')

# per-clip entrances + detection
for i, c in enumerate(CLIPS, 1):
    tw(f'tl.from("#cv{i}", {{opacity:0, duration:0.2, ease:"power2.out"}}, {c["ds"]});')
    tw(f'tl.fromTo("#cv{i}", {{scale:1.08}}, {{scale:1.0, duration:{c["dur"]}, ease:"power2.out"}}, {c["ds"]});')
    tw(f'tl.from("#lab{i}", {{x:-26, opacity:0, duration:0.4, ease:"back.out(1.7)"}}, {round(c["ds"]+0.15,3)});')
    # circle draw-on + pulse, dashed ring rotates (scanning)
    tw(f'tl.from("#circ{i}", {{scale:1.6, opacity:0, duration:0.4, ease:"back.out(2)"}}, {round(c["pop"]-0.05,3)});')
    tw(f'tl.to("#circ{i} .ring-solid", {{scale:1.08, duration:0.4, yoyo:true, repeat:5, ease:"power1.inOut"}}, {round(c["pop"]+0.35,3)});')
    tw(f'tl.fromTo("#circ{i} .ring-dash", {{rotation:0}}, {{rotation:360, duration:{round(c["ds"]+c["dur"]-c["pop"],3)}, ease:"none"}}, {round(c["pop"],3)});')
    tw(f'tl.from("#tag{i}", {{scale:0.5, opacity:0, duration:0.34, ease:"back.out(2.2)"}}, {round(c["pop"]+0.05,3)});')

# end screen
tw(f'tl.from("#end-logo", {{opacity:0, scale:0.8, duration:0.6, ease:"back.out(1.6)"}}, {round(END_S+0.05,3)});')
tw(f'tl.from("#end-tag", {{opacity:0, y:26, duration:0.5, ease:"power3.out"}}, {round(END_S+0.55,3)});')
tw(f'tl.from("#end-sub", {{opacity:0, y:20, duration:0.5, ease:"power3.out"}}, {round(END_S+0.8,3)});')
tw(f'tl.from("#end-cta", {{opacity:0, scale:0.8, duration:0.5, ease:"back.out(2)"}}, {round(END_S+1.1,3)});')
tw(f'tl.to("#end-cta", {{scale:1.05, duration:0.5, yoyo:true, repeat:3, ease:"power1.inOut"}}, {round(END_S+1.7,3)});')

tween_js = "\n    ".join(tweens)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>videodb-highlights</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
[data-composition-id="videodb-highlights"] {{
  position:relative; width:{W}px; height:{H}px; overflow:hidden;
  background:
    radial-gradient(120% 80% at 50% 0%, #16181d 0%, {DARK} 55%),
    {DARK};
  font-family:"Inter","Helvetica Neue",Arial,sans-serif; color:#fff;
}}
.bg-grid {{ position:absolute; inset:0; z-index:0; opacity:0.5;
  background-image:linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px),
                   linear-gradient(90deg, rgba(255,255,255,0.045) 1px, transparent 1px);
  background-size:90px 90px;
  -webkit-mask-image:radial-gradient(110% 80% at 50% 42%, #000 60%, transparent 100%);
          mask-image:radial-gradient(110% 80% at 50% 42%, #000 60%, transparent 100%); }}

/* highlight clips ---------------------------------------------------------- */
.hvid {{ position:absolute; object-fit:cover; border-radius:26px; z-index:5;
  border:3px solid rgba(232,85,31,0.55); background:#000;
  box-shadow:0 26px 70px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.04); }}

/* detection circle --------------------------------------------------------- */
.det-circ {{ position:absolute; z-index:7; }}
.ring-solid {{ position:absolute; inset:0; border-radius:50%; border:6px solid {ORANGE};
  box-shadow:0 0 26px rgba(232,85,31,0.65), inset 0 0 18px rgba(232,85,31,0.35); }}
.ring-dash {{ position:absolute; inset:-16px; border-radius:50%; border:4px dashed rgba(255,255,255,0.65); }}
.det-tag {{ position:absolute; z-index:8; display:inline-flex; align-items:center; gap:14px;
  background:rgba(10,11,13,0.92); border:2px solid {ORANGE}; border-radius:14px;
  padding:12px 22px; font-weight:900; font-size:34px; letter-spacing:0.01em; white-space:nowrap;
  box-shadow:0 10px 30px rgba(0,0,0,0.5); }}
.det-tag .dot {{ width:18px; height:18px; border-radius:50%; background:{ORANGE}; box-shadow:0 0 14px {ORANGE}; }}
.det-tag .conf {{ font-weight:700; font-size:28px; color:#9aa0aa; }}

/* moment label ------------------------------------------------------------- */
.mom-label {{ position:absolute; z-index:8; display:flex; align-items:baseline; gap:20px; }}
.mom-label .mt {{ font-weight:800; font-size:48px; color:{ORANGE}; font-variant-numeric:tabular-nums; }}
.mom-label .ml {{ font-weight:900; font-size:72px; letter-spacing:-0.02em;
  text-shadow:0 3px 18px rgba(0,0,0,0.7); }}

/* top bar ------------------------------------------------------------------ */
#topbar {{ position:absolute; left:40px; right:40px; top:64px; height:80px; z-index:9;
  display:flex; align-items:center; justify-content:space-between; }}
.tb-logo {{ height:42px; width:auto; }}
.tb-right {{ display:flex; align-items:center; gap:16px; background:rgba(255,255,255,0.06);
  border:1px solid rgba(255,255,255,0.12); border-radius:40px; padding:12px 24px;
  font-weight:800; font-size:30px; letter-spacing:0.04em; }}
#rec-dot {{ width:18px; height:18px; border-radius:50%; background:{ORANGE}; box-shadow:0 0 14px {ORANGE}; }}

/* timeline ----------------------------------------------------------------- */
#timeline {{ position:absolute; left:40px; right:40px; top:1640px; z-index:9; }}
.tl-cap {{ font-weight:700; font-size:30px; color:#aeb4bd; margin-bottom:26px; letter-spacing:0.01em; }}
.tl-cap b {{ color:#fff; font-weight:900; }}
.tl-track {{ position:relative; height:8px; border-radius:8px; background:rgba(255,255,255,0.14); margin:0 30px; }}
.tl-fill {{ position:absolute; left:0; top:0; height:100%; width:100%; border-radius:8px;
  background:linear-gradient(90deg, rgba(232,85,31,0.25), rgba(232,85,31,0.6)); }}
.tl-mark {{ position:absolute; top:50%; width:26px; height:26px; margin-left:-13px; margin-top:-13px;
  border-radius:50%; background:{ORANGE}; box-shadow:0 0 18px rgba(232,85,31,0.8); border:3px solid #0A0B0D; }}
.tl-mlabel {{ position:absolute; top:30px; transform:translateX(-50%); font-weight:800; font-size:26px; color:#cfd3da; }}
#playhead {{ position:absolute; top:50%; left:70px; width:6px; height:46px; margin-top:-23px; margin-left:-3px;
  background:#fff; border-radius:4px; box-shadow:0 0 16px rgba(255,255,255,0.8); z-index:2; }}

/* made-with badge ---------------------------------------------------------- */
#badge {{ position:absolute; left:40px; bottom:60px; z-index:10; display:inline-flex; align-items:center; gap:14px;
  background:rgba(10,11,13,0.85); border:1px solid rgba(255,255,255,0.14); border-radius:40px; padding:14px 26px;
  font-weight:700; font-size:32px; color:#cfd3da; box-shadow:0 8px 24px rgba(0,0,0,0.5); }}
#badge .play {{ width:0; height:0; border-left:20px solid {ORANGE}; border-top:13px solid transparent; border-bottom:13px solid transparent; }}
#badge .vdb {{ font-weight:900; color:#fff; }}
#badge .vdb i {{ font-style:normal; color:{ORANGE}; }}

/* intro -------------------------------------------------------------------- */
#intro {{ position:absolute; inset:0; z-index:20; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:30px; padding:0 80px; }}
#intro-logo {{ height:70px; width:auto; margin-bottom:20px; }}
#intro-title {{ text-align:center; }}
#intro-title .mask {{ overflow:hidden; display:block; }}
#intro-title .mask > span {{ display:inline-block; font-weight:900; font-size:128px; letter-spacing:-0.03em; line-height:0.95; }}
#intro-sub {{ text-align:center; font-weight:700; font-size:46px; color:#cfd3da; }}
#intro-sub b {{ color:{ORANGE}; }}
#intro-meta {{ font-weight:600; font-size:34px; color:#8b919b; margin-top:6px; }}
#intro-scan {{ position:absolute; left:120px; right:120px; height:4px; background:linear-gradient(90deg, transparent, {ORANGE}, transparent); box-shadow:0 0 24px {ORANGE}; top:50%; }}

/* end screen --------------------------------------------------------------- */
#end {{ position:absolute; inset:0; z-index:20; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:34px; padding:0 90px; background:radial-gradient(120% 80% at 50% 40%, #16181d 0%, {DARK} 60%); }}
#end-logo {{ width:72%; max-width:760px; height:auto; filter:drop-shadow(0 10px 50px rgba(232,85,31,0.45)); }}
#end-tag {{ text-align:center; font-weight:900; font-size:66px; letter-spacing:-0.02em; line-height:1.05; }}
#end-tag i {{ font-style:normal; color:{ORANGE}; }}
#end-sub {{ text-align:center; font-weight:600; font-size:40px; color:#aeb4bd; max-width:820px; line-height:1.25; }}
#end-cta {{ margin-top:14px; background:{ORANGE}; color:#fff; font-weight:900; font-size:46px; letter-spacing:0.01em;
  padding:22px 56px; border-radius:18px; box-shadow:0 14px 40px rgba(232,85,31,0.5); }}
</style>
</head>
<body>
<div data-composition-id="videodb-highlights" data-start="0" data-width="{W}" data-height="{H}">
  <div class="bg-grid"></div>

{clips_markup}

  <!-- persistent chrome -->
  <div id="topbar" class="clip" data-start="{ANALYSIS_S}" data-duration="{an_dur}" data-track-index="12">
    <img class="tb-logo" src="videodb-logo.png" />
    <div class="tb-right"><span id="rec-dot"></span>AUTO-HIGHLIGHTS</div>
  </div>

  <div id="timeline" class="clip" data-start="{ANALYSIS_S}" data-duration="{an_dur}" data-track-index="13">
    <div class="tl-cap">Scanned <b>{TOTAL}</b> broadcast · <b>3</b> key moments found</div>
    <div class="tl-track">
      <div class="tl-fill"></div>
      {markers}
      <div id="playhead"></div>
    </div>
  </div>

  <div id="badge" class="clip" data-start="{ANALYSIS_S}" data-duration="{an_dur}" data-track-index="14">
    <span class="play"></span>Made with <span class="vdb">Video<i>DB</i></span>
  </div>

  <!-- intro -->
  <div id="intro" class="clip" data-start="{INTRO_S}" data-duration="{round(INTRO_E,3)}" data-track-index="16">
    <img id="intro-logo" src="videodb-logo.png" />
    <div id="intro-title"><span class="mask"><span>AUTO-HIGHLIGHTS</span></span></div>
    <div id="intro-sub">{MATCH} · <b>{COMP}</b></div>
    <div id="intro-meta">Analyzing {TOTAL} broadcast…</div>
    <div id="intro-scan"></div>
  </div>

  <!-- end screen -->
  <div id="end" class="clip" data-start="{END_S}" data-duration="{round(END_E-END_S,3)}" data-track-index="17">
    <img id="end-logo" src="videodb-logo.png" />
    <div id="end-tag">See, search & <i>act</i> on any video</div>
    <div id="end-sub">Turn any match — any footage — into highlights, automatically.</div>
    <div id="end-cta">videodb.io</div>
  </div>

{audio_markup}

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused:true }});
    {tween_js}
    window.__timelines["videodb-highlights"] = tl;
  </script>
</div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote index.html  ({} clips, {} whooshes, {} blips)".format(len(CLIPS), len(WHOOSH), len(BLIPS)))
