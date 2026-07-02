# -*- coding: utf-8 -*-
"""Generate index.html for the split-screen UGC composition (VideoDB / soccer-clips).
Talking head docks from full-screen into the bottom split; top zone runs image cards,
kinetic-type cards, a built VideoDB demo (copy link -> paste -> 3 clips), and a clip
montage. White word-captions ride the seam; the click SFX fires on every top change.
Timings come from transcript.json. Edit below and run `python3 build.py`."""

DURATION = 40.2
DOCK = 3.6          # full-screen avatar docks into the split here

# layout (px in 1080x1920) --------------------------------------------------
SEAM = 812
VIDEO_TOP = 760
CAP_TOP = 828
VIDEO_OBJ_POS = "50% 14%"

# BRAND:START
CARD = "#F6F3EC"        # brand:card
GRID = "#DCD8CE"        # brand:hairline
INK = "#141414"         # brand:text
CORAL = "#C75C3C"       # brand:accent
RED = "#D6452F"         # brand:bad
DARK = "#0E0D0B"
VDB_ORANGE = "#E8551F"  # secondary literal brand color (VideoDB orange) — not a theme token
# BRAND:END

MATCH = "Australia 2-0 Türkiye | FIFA World Cup 2026"

# in-points for the soccer clips (seconds into each source) ------------------
C1_IN, C2_IN, C3_IN = 5.3, 5.0, 7.0

# top cards ------------------------------------------------------------------
CARDS = [
    dict(s=3.60,  e=5.00,  kind="image", img="soccer-shorts-clip.jpg",  pos="50% 42%"),
    dict(s=5.00,  e=6.00,  kind="image", img="soccer-channel-money.jpg", pos="50% 46%"),
    dict(s=6.00,  e=7.78,  kind="statement", top="But",     acc="how?", color=CORAL),
    dict(s=7.78,  e=9.79,  kind="image", img="watching-match.jpg",  pos="50% 40%"),
    dict(s=9.79,  e=12.43, kind="image", img="editing-manual.jpg",  pos="50% 30%"),
    dict(s=12.43, e=13.95, kind="statement", top="They're", acc="not.", color=RED),
    dict(s=13.95, e=16.65, kind="logo",  img="videodb-logo.png"),
    dict(s=16.65, e=20.20, kind="paste"),
    dict(s=20.20, e=23.27, kind="results"),
    dict(s=23.27, e=23.85, kind="word", acc="Goals",       color=CORAL),
    dict(s=23.85, e=24.82, kind="word", acc="Assists",     color=CORAL),
    dict(s=24.82, e=25.18, kind="word", acc="Cards",       color=CORAL),
    dict(s=25.18, e=25.85, kind="word", acc="Big chances", color=CORAL),
    dict(s=25.85, e=28.00, kind="word", acc="Everything",  color=INK),
    dict(s=28.00, e=31.40, kind="price", label="The old way",  big="90 MIN",  color=RED),
    dict(s=31.40, e=33.84, kind="price", label="With VideoDB", big="SECONDS", color=CORAL),
    dict(s=33.84, e=35.37, kind="clip", src="clip2.mp4", min=C2_IN, label="GOAL · 23'", trk=10),
    dict(s=35.37, e=36.90, kind="clip", src="clip1.mp4", min=C1_IN, label="GOAL · 67'", trk=11),
    dict(s=36.90, e=38.42, kind="clip", src="clip3.mp4", min=C3_IN, label="BIG CHANCE · 81'", trk=12),
    dict(s=38.42, e=40.20, kind="cta", top="Comment", acc="“workflow”", sub="for the full breakdown", color=CORAL),
]

# seam captions (start, text) — extend each until the next ------------------
CAPTIONS = [
    (0.14,"People are"),(0.90,"hundreds of dollars"),(1.95,"a month"),(2.36,"posting soccer clips"),
    (3.60,"and I just found out"),(5.98,"how they’re creating them"),(7.37,"so fast"),
    (7.85,"I thought they were"),(8.87,"watching full matches"),(10.17,"and clipping everything"),(11.58,"manually"),
    (12.43,"They’re not"),(13.61,"They use tools like"),(16.02,"VideoDB"),
    (16.65,"You paste in"),(17.60,"a match link"),(18.81,"and it"),
    (20.20,"automatically finds"),(21.00,"all the key moments"),(22.23,"from the game"),
    (23.27,"Goals"),(23.77,"Assists"),(24.82,"Cards"),(25.18,"Big chances"),(25.85,"Everything"),
    (28.00,"instead of spending hours"),(29.47,"watching a 90-min match"),
    (31.40,"you can find"),(32.28,"the best moments"),(33.19,"in seconds"),
    (33.98,"if you want my"),(34.73,"complete workflow"),(36.29,"for creating these"),(37.37,"soccer clips"),
    (38.42,"comment “WORKFLOW”"),(39.57,"below"),
]

EASES = ["back.out(1.5)", "power4.out", "expo.out", "back.out(1.7)"]


def card_markup(i, c):
    cid = f"card-{i}"; trk = 2 if i % 2 == 0 else 5
    head = f'    <div id="{cid}" class="clip card {c["kind"]}" data-start="{c["s"]}" data-duration="{round(c["e"]-c["s"],3)}" data-track-index="{trk}">'
    k = c["kind"]
    if k == "image":
        return head + f'\n      <div class="img-wrap"><img class="kb" src="{c["img"]}" style="object-position:{c["pos"]}" /></div>\n    </div>'
    if k == "logo":
        return head + f'\n      <div class="grid dark-grid"></div>\n      <div class="logo-wrap"><img class="logo-img" src="{c["img"]}" /></div>\n    </div>'
    if k == "clip":
        # top-level (NOT nested in a timed card) so the framework can play it
        d = round(c["e"]-c["s"],3)
        return (f'    <video id="mv-{i}" class="clip mvid" src="{c["src"]}" data-start="{c["s"]}" data-duration="{d}" '
                f'data-track-index="{c["trk"]}" data-media-start="{c["min"]}" muted playsinline></video>\n'
                f'    <div id="mtag-{i}" class="clip mtag" data-start="{c["s"]}" data-duration="{d}" data-track-index="{c["trk"]+3}">{c["label"]}</div>')
    if k == "paste":
        return head + PASTE_INNER
    if k == "results":
        s = c["s"]; dur = round(c["e"]-c["s"],3)
        return head + results_inner(s, dur)
    if k == "statement":
        inner = (f'<div class="mask"><span class="bold">{c["top"]}</span></div>'
                 f'<div class="mask"><span class="serif" style="color:{c["color"]}">{c["acc"]}</span></div>')
    elif k == "word":
        inner = f'<div class="mask"><span class="serif word-acc" style="color:{c["color"]}">{c["acc"]}</span></div>'
    elif k == "price":
        inner = (f'<div class="mask"><span class="label">{c["label"]}</span></div>'
                 f'<div class="mask"><span class="big" style="color:{c["color"]}">{c["big"]}</span></div>')
    else:  # cta
        inner = (f'<div class="mask"><span class="bold">{c["top"]}</span></div>'
                 f'<div class="mask"><span class="serif" style="color:{c["color"]}">{c["acc"]}</span></div>'
                 f'<div class="mask"><span class="sub">{c["sub"]}</span></div>')
    return head + f'\n      <div class="grid"></div>\n      <div class="card-body">{inner}</div>\n    </div>'


# --- BESPOKE SCENES (VideoDB product UI — replace per product) ---
# The "paste" and "results" card kinds below (PASTE_INNER + results_inner)
# render VideoDB-specific product UI. Swap their markup for your product.

# ---- VideoDB "paste" scene (static markup, animated by GSAP) ----------------
PASTE_INNER = f'''
      <div class="grid"></div>
      <div class="paste-stage">
        <div id="pst-bar" class="yt-bar"><span class="yt-ico"></span><span class="yt-q">{MATCH}</span></div>
        <div id="pst-thumb" class="yt-result">
          <img src="match-thumb.jpg" />
          <span class="yt-dur">1:56:26</span>
          <div id="pst-copied" class="copied-chip">Link copied</div>
        </div>
        <div id="pst-arrow" class="pst-arrow"></div>
        <div id="pst-panel" class="vdb-panel">
          <img class="vdb-logo" src="videodb-logo.png" />
          <div class="vdb-input"><span id="pst-url" class="vdb-url">youtu.be/aus-tur-2026</span><span class="caret"></span></div>
          <div id="pst-btn" class="vdb-btn">Analyze</div>
        </div>
      </div>
    </div>'''


def results_inner(s, dur):
    clips = [("res-1.jpg", "GOAL · 23'"), ("res-2.jpg", "GOAL · 67'"), ("res-3.jpg", "BIG CHANCE · 81'")]
    cards = ""
    for n, (poster, lbl) in enumerate(clips, 1):
        cards += (f'\n          <div id="res-c{n}" class="res-card">'
                  f'<img class="res-poster" src="{poster}" />'
                  f'<span class="res-play"></span>'
                  f'<span class="res-tag">{lbl}</span></div>')
    return f'''
      <div class="grid dark-grid"></div>
      <div class="res-stage">
        <div id="res-head" class="res-head"><img class="res-logo" src="videodb-logo.png" /><span class="res-found">3 key moments found</span></div>
        <div class="res-row">{cards}
        </div>
      </div>
    </div>'''


def caption_markup(i):
    s, text = CAPTIONS[i]
    e = CAPTIONS[i + 1][0] if i < len(CAPTIONS) - 1 else DURATION
    trk = 3 if i % 2 == 0 else 6
    return (f'    <div id="cap-{i}" class="clip caption" data-start="{round(s,3)}" '
            f'data-duration="{round(e-s,3)}" data-track-index="{trk}"><span>{text}</span></div>')


def click_markup(i, c):
    return (f'  <audio id="click-{i}" class="clip" src="click-sfx.mp3" data-start="{c["s"]}" '
            f'data-duration="0.3" data-track-index="4" data-volume="0.5"></audio>')


def card_tweens(i, c):
    cid = f"#card-{i}"; s = c["s"]; dur = round(c["e"]-c["s"],3); k = c["kind"]
    e1 = EASES[i % len(EASES)]; e2 = EASES[(i+2) % len(EASES)]
    if k == "image":
        return (f'  tl.from("{cid} .img-wrap", {{opacity:0, scale:1.08, duration:0.42, ease:"power3.out"}}, {s});\n'
                f'  tl.fromTo("{cid} .kb", {{scale:1.0}}, {{scale:1.06, duration:{dur}, ease:"none"}}, {s});')
    if k == "clip":
        return (f'  tl.from("#mv-{i}", {{opacity:0, duration:0.16, ease:"power2.out"}}, {s});\n'
                f'  tl.fromTo("#mv-{i}", {{scale:1.12}}, {{scale:1.0, duration:{dur}, ease:"power2.out"}}, {s});\n'
                f'  tl.from("#mtag-{i}", {{x:-30, opacity:0, duration:0.4, ease:"back.out(1.7)"}}, {round(s+0.1,3)});')
    if k == "logo":
        return (f'  tl.from("{cid} .grid", {{opacity:0, duration:0.5, ease:"power2.out"}}, {s});\n'
                f'  tl.from("{cid} .logo-img", {{opacity:0, scale:0.78, duration:0.5, ease:"back.out(1.7)"}}, {s});')
    # --- BESPOKE SCENES (VideoDB product UI — replace per product) ---
    # tweens for the "paste" and "results" product-demo cards
    if k == "paste":
        return (f'  tl.from("{cid} .grid", {{opacity:0, duration:0.4}}, {s});\n'
                f'  tl.from("#pst-bar", {{y:-40, opacity:0, duration:0.4, ease:"power3.out"}}, {s});\n'
                f'  tl.from("#pst-thumb", {{scale:0.92, opacity:0, duration:0.45, ease:"back.out(1.6)"}}, {round(s+0.2,3)});\n'
                f'  tl.from("#pst-copied", {{scale:0.5, opacity:0, duration:0.34, ease:"back.out(2.4)"}}, {round(s+0.7,3)});\n'
                f'  tl.from("#pst-panel", {{y:70, opacity:0, duration:0.5, ease:"power3.out"}}, {round(s+1.55,3)});\n'
                f'  tl.from("#pst-arrow", {{opacity:0, scale:0.4, duration:0.3, ease:"back.out(2)"}}, {round(s+1.7,3)});\n'
                f'  tl.from("#pst-url", {{opacity:0, x:-26, duration:0.32, ease:"power2.out"}}, {round(s+2.0,3)});\n'
                f'  tl.from("#pst-btn", {{scale:0.8, opacity:0, duration:0.36, ease:"back.out(2)"}}, {round(s+2.35,3)});\n'
                f'  tl.to("#pst-btn", {{scale:1.07, duration:0.16, yoyo:true, repeat:1, ease:"power1.inOut"}}, {round(s+2.85,3)});')
    if k == "results":
        return (f'  tl.from("{cid} .grid", {{opacity:0, duration:0.4}}, {s});\n'
                f'  tl.from("#res-head", {{y:-26, opacity:0, duration:0.4, ease:"power3.out"}}, {s});\n'
                f'  tl.from("#res-c1", {{scale:0.55, opacity:0, duration:0.46, ease:"back.out(1.8)"}}, {round(s+0.25,3)});\n'
                f'  tl.from("#res-c2", {{scale:0.55, opacity:0, duration:0.46, ease:"back.out(1.8)"}}, {round(s+0.5,3)});\n'
                f'  tl.from("#res-c3", {{scale:0.55, opacity:0, duration:0.46, ease:"back.out(1.8)"}}, {round(s+0.75,3)});')
    # text-based cards
    t = [f'  tl.from("{cid} .mask:nth-child(1) > span", {{yPercent:115, opacity:0, duration:0.42, ease:"{e1}"}}, {s});']
    if k != "word":
        t.append(f'  tl.from("{cid} .mask:nth-child(2) > span", {{yPercent:115, opacity:0, duration:0.46, ease:"{e2}"}}, {round(s+0.06,3)});')
    if k == "price":
        t.append(f'  tl.from("{cid} .big", {{scale:0.6, duration:0.5, ease:"back.out(1.8)"}}, {round(s+0.06,3)});')
    if k == "cta":
        t.append(f'  tl.from("{cid} .mask:nth-child(3) > span", {{yPercent:115, opacity:0, duration:0.4, ease:"power3.out"}}, {round(s+0.15,3)});')
    if k == "word":
        t.append(f'  tl.from("{cid} .word-acc", {{scale:0.72, duration:0.34, ease:"back.out(2.2)"}}, {s});')
    t.append(f'  tl.from("{cid} .grid", {{opacity:0, duration:0.5, ease:"power2.out"}}, {s});')
    return "\n".join(t)


def caption_tween(i):
    return f'  tl.from("#cap-{i}", {{scale:0.7, opacity:0, duration:0.18, ease:"back.out(2.6)"}}, {round(CAPTIONS[i][0],3)});'


cards_markup = "\n".join(card_markup(i, c) for i, c in enumerate(CARDS))
caps_markup = "\n".join(caption_markup(i) for i in range(len(CAPTIONS)))
clicks_markup = "\n".join(click_markup(i, c) for i, c in enumerate(CARDS))
card_tween_js = "\n".join(card_tweens(i, c) for i, c in enumerate(CARDS))
cap_tween_js = "\n".join(caption_tween(i) for i in range(len(CAPTIONS)))

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>split-ugc-videodb</title>
<style>
/* Fonts auto-embed from family names (Inter, Playfair Display). */
* {{ margin:0; padding:0; box-sizing:border-box; }}

[data-composition-id="split-ugc-videodb"] {{
  position:relative; width:1080px; height:1920px; overflow:hidden;
  background:{DARK}; font-family:"Inter","Helvetica Neue",Arial,sans-serif;
  --seam:{SEAM}px;
}}
.bg {{ position:absolute; inset:0; background:{DARK}; z-index:0; }}

/* talking head — full-frame, docks into the split at DOCK ------------------ */
.video-wrap {{ position:absolute; left:0; right:0; top:0; bottom:0; overflow:hidden; z-index:1; }}
.video-wrap video {{ width:100%; height:100%; object-fit:cover; object-position:{VIDEO_OBJ_POS}; transform-origin:50% 38%; }}
.seam-fade {{ position:absolute; left:0; right:0; top:{VIDEO_TOP}px; height:240px; z-index:2;
  background:linear-gradient(180deg,{DARK} 0%, rgba(14,13,11,0.65) 38%, rgba(14,13,11,0) 100%); pointer-events:none; }}

/* top cards ---------------------------------------------------------------- */
.topzone {{ position:absolute; left:0; right:0; top:0; height:var(--seam); z-index:5; }}
.card {{ position:absolute; inset:0; background:{CARD}; overflow:hidden; display:flex; align-items:center; justify-content:center; }}
.card .grid {{ position:absolute; inset:0;
  background-image:linear-gradient(to right, {GRID} 1px, transparent 1px), linear-gradient(to bottom, {GRID} 1px, transparent 1px);
  background-size:96px 96px; opacity:0.9;
  -webkit-mask-image:radial-gradient(120% 100% at 50% 45%, #000 60%, transparent 100%);
          mask-image:radial-gradient(120% 100% at 50% 45%, #000 60%, transparent 100%); }}
.card .grid.dark-grid {{ background-image:linear-gradient(to right, rgba(255,255,255,0.06) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,0.06) 1px, transparent 1px); }}
.card-body {{ position:relative; z-index:1; width:100%; padding:0 90px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px; text-align:center; }}
.mask {{ overflow:hidden; display:block; padding:6px 0; }}
.mask > span {{ display:inline-block; }}

.card.image {{ background:#EDEEF0; }}
.card.image .img-wrap {{ position:absolute; inset:0; overflow:hidden; }}
.card.image .kb {{ width:100%; height:100%; object-fit:cover; transform-origin:50% 50%; }}

.card.logo {{ background:{DARK}; }}
.logo-wrap {{ position:relative; z-index:1; width:100%; display:flex; align-items:center; justify-content:center; }}
.logo-img {{ width:60%; max-width:640px; height:auto; filter:drop-shadow(0 8px 40px rgba(232,85,31,0.4)); }}

/* clip montage (top-level video clips filling the top zone) ----------------- */
.mvid {{ position:absolute; left:0; top:0; width:1080px; height:{SEAM}px; object-fit:cover; object-position:50% 45%;
  transform-origin:50% 50%; z-index:5; background:#000; }}
.mtag {{ position:absolute; z-index:6; left:34px; top:{SEAM-90}px; background:{VDB_ORANGE}; color:#fff;
  font-weight:900; font-size:46px; letter-spacing:-0.01em; padding:12px 26px; border-radius:14px; box-shadow:0 6px 26px rgba(0,0,0,0.5); }}

/* text card type scale ----------------------------------------------------- */
.bold {{ font-weight:900; font-size:168px; line-height:0.92; letter-spacing:-0.03em; color:{INK}; }}
.serif {{ font-family:"Playfair Display", Georgia, serif; font-style:italic; font-weight:700; font-size:172px; line-height:0.96; letter-spacing:-0.01em; }}
.statement .bold {{ font-size:150px; }}
.statement .serif {{ font-size:158px; }}
.word .serif {{ font-size:208px; }}
.label {{ font-weight:800; font-size:72px; letter-spacing:-0.02em; color:{INK}; opacity:0.78; }}
.big {{ font-weight:900; font-size:228px; line-height:0.9; letter-spacing:-0.04em; font-variant-numeric:tabular-nums; }}
.cta .bold {{ font-size:132px; }}
.cta .serif {{ font-size:176px; }}
.cta .sub {{ font-weight:700; font-size:58px; color:{INK}; opacity:0.7; letter-spacing:-0.01em; }}

/* VideoDB paste scene ------------------------------------------------------ */
.paste {{ background:{CARD}; }}
.paste-stage {{ position:relative; z-index:1; width:100%; height:100%; padding:54px 80px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:22px; }}
.yt-bar {{ display:flex; align-items:center; gap:20px; width:840px; max-width:100%; background:#fff; border:2px solid #e2ded3; border-radius:60px;
  padding:22px 34px; box-shadow:0 8px 28px rgba(0,0,0,0.08); }}
.yt-ico {{ width:40px; height:40px; border-radius:50%; background:{RED}; flex:0 0 auto; position:relative; }}
.yt-ico::after {{ content:""; position:absolute; left:15px; top:11px; border-left:16px solid #fff; border-top:9px solid transparent; border-bottom:9px solid transparent; }}
.yt-q {{ font-weight:700; font-size:34px; color:#222; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.yt-result {{ position:relative; width:520px; border-radius:22px; overflow:hidden; box-shadow:0 18px 50px rgba(0,0,0,0.22); }}
.yt-result img {{ display:block; width:100%; height:auto; }}
.yt-dur {{ position:absolute; right:14px; bottom:14px; background:rgba(0,0,0,0.85); color:#fff; font-weight:800; font-size:30px; padding:6px 14px; border-radius:10px; }}
.copied-chip {{ position:absolute; right:14px; top:14px; background:#1faa59; color:#fff; font-weight:900; font-size:30px; padding:10px 22px; border-radius:14px; box-shadow:0 8px 22px rgba(31,170,89,0.5); }}
.copied-chip::before {{ content:"✓  "; }}
.pst-arrow {{ width:0; height:0; border-left:26px solid transparent; border-right:26px solid transparent; border-top:34px solid {VDB_ORANGE}; }}
.vdb-panel {{ width:760px; max-width:100%; background:#15161a; border:2px solid rgba(232,85,31,0.35); border-radius:30px; padding:30px 34px;
  display:flex; flex-direction:column; align-items:center; gap:24px; box-shadow:0 22px 60px rgba(0,0,0,0.4); }}
.vdb-logo {{ height:54px; width:auto; }}
.vdb-input {{ width:100%; display:flex; align-items:center; gap:4px; background:#0e0f12; border:2px solid #2a2c33; border-radius:16px; padding:22px 26px; }}
.vdb-url {{ font-weight:600; font-size:34px; color:#cfd2d8; font-family:"Inter",monospace; }}
.caret {{ width:3px; height:38px; background:{VDB_ORANGE}; margin-left:2px; }}
.vdb-btn {{ background:{VDB_ORANGE}; color:#fff; font-weight:900; font-size:38px; letter-spacing:0.01em; padding:18px 56px; border-radius:16px; box-shadow:0 10px 30px rgba(232,85,31,0.45); }}

/* VideoDB results scene ---------------------------------------------------- */
.results {{ background:{DARK}; }}
.res-stage {{ position:relative; z-index:1; width:100%; height:100%; padding:60px 70px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:34px; }}
.res-head {{ display:flex; align-items:center; gap:26px; }}
.res-logo {{ height:50px; width:auto; }}
.res-found {{ font-weight:900; font-size:46px; color:#fff; letter-spacing:-0.01em; }}
.res-found::before {{ content:"✓ "; color:#1faa59; }}
.res-row {{ display:flex; gap:26px; align-items:stretch; justify-content:center; width:100%; }}
.res-card {{ position:relative; width:300px; height:430px; border-radius:22px; overflow:hidden; background:#000; border:3px solid rgba(232,85,31,0.55); box-shadow:0 16px 44px rgba(0,0,0,0.55); }}
.res-poster {{ width:100%; height:100%; object-fit:cover; object-position:50% 45%; }}
.res-play {{ position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:88px; height:88px; border-radius:50%;
  background:rgba(0,0,0,0.45); border:3px solid rgba(255,255,255,0.9); }}
.res-play::after {{ content:""; position:absolute; left:36px; top:28px; border-left:30px solid #fff; border-top:17px solid transparent; border-bottom:17px solid transparent; }}
.res-tag {{ position:absolute; left:16px; bottom:16px; background:{VDB_ORANGE}; color:#fff; font-weight:900; font-size:30px; padding:8px 16px; border-radius:11px; }}

/* seam captions ------------------------------------------------------------ */
.capzone {{ position:absolute; left:0; right:0; top:{CAP_TOP}px; height:200px; z-index:8; display:flex; align-items:flex-start; justify-content:center; pointer-events:none; }}
.caption {{ position:absolute; left:50%; top:0; transform-origin:center top; width:960px; margin-left:-480px; text-align:center; }}
.caption span {{ display:inline-block; color:#fff; font-weight:900; font-size:96px; line-height:1.0; letter-spacing:-0.02em;
  text-shadow:0 4px 22px rgba(0,0,0,0.9), 0 1px 3px rgba(0,0,0,0.95); }}
</style>
</head>
<body>
<div data-composition-id="split-ugc-videodb" data-start="0" data-width="1080" data-height="1920">
  <div class="bg"></div>

  <div class="video-wrap">
    <video id="vid" class="clip" data-start="0" data-duration="{DURATION}" data-track-index="0" src="Video1.mp4" muted playsinline></video>
  </div>
  <div class="seam-fade"></div>
  <audio id="voice" class="clip" src="Video1.mp4" data-start="0" data-duration="{DURATION}" data-track-index="1" data-volume="1"></audio>

  <div class="topzone">
{cards_markup}
  </div>

  <div class="capzone">
{caps_markup}
  </div>

{clicks_markup}

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused:true }});

    // full-screen hook -> dock into the split
    gsap.set(".video-wrap", {{ top:0 }});
    gsap.set(".seam-fade", {{ opacity:0 }});
    tl.fromTo("#vid", {{scale:1.0}}, {{scale:1.10, duration:{round(DOCK-0.05,3)}, ease:"none"}}, 0);
    tl.to(".video-wrap", {{top:{VIDEO_TOP}, duration:0.55, ease:"power3.inOut"}}, {round(DOCK-0.05,3)});
    tl.to("#vid", {{scale:1.0, duration:0.55, ease:"power3.inOut"}}, {round(DOCK-0.05,3)});
    tl.to(".seam-fade", {{opacity:1, duration:0.4, ease:"power2.out"}}, {round(DOCK-0.2,3)});

    // top card entrances
{card_tween_js}

    // caption pops
{cap_tween_js}

    window.__timelines["split-ugc-videodb"] = tl;
  </script>
</div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote index.html  ({} cards, {} captions, {} clicks)".format(len(CARDS), len(CAPTIONS), len(CARDS)))
