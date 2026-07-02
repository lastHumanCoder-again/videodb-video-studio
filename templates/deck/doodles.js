/* ============================================================
   VideoDB doodle toolkit — hand-drawn art via rough.js
   Each .art[data-art] div gets an <svg>; a registry fn draws into it.
   Reusable across decks: compose from the helpers below.
   ============================================================ */
(function () {
  let ORANGE = '#E85810';        // per-deck: overridden from the slide's --orange at draw time
  const SEED = 42; // deterministic sketchiness

  // theme-aware neutral ink (boxes/arrows that aren't the orange accent)
  function neutral(theme) { return theme === 'light' ? '#A39C90' : '#6E6E76'; }
  function ink(theme)     { return theme === 'light' ? '#16161A' : '#F4F2EE'; }

  // ---- low-level helpers (return SVG nodes to append) ----
  const H = {
    rect(rc, x, y, w, h, o = {}) {
      return rc.rectangle(x, y, w, h, { roughness: 1.5, bowing: 1.4, seed: SEED, strokeWidth: 2, ...o });
    },
    ell(rc, cx, cy, w, h, o = {}) {
      return rc.ellipse(cx, cy, w, h, { roughness: 1.4, bowing: 1.2, seed: SEED, strokeWidth: 2, ...o });
    },
    line(rc, x1, y1, x2, y2, o = {}) {
      return rc.line(x1, y1, x2, y2, { roughness: 1.4, bowing: 1.5, seed: SEED, strokeWidth: 2, ...o });
    },
    path(rc, d, o = {}) {
      return rc.path(d, { roughness: 1.3, bowing: 1.2, seed: SEED, strokeWidth: 2, ...o });
    },
    // curved arrow from (x1,y1) to (x2,y2) with a control offset + arrowhead
    arrow(rc, x1, y1, x2, y2, o = {}) {
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      const curve = o.curve ?? 0.3;
      const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
      const dx = x2 - x1, dy = y2 - y1;
      const cx = mx - dy * curve, cy = my + dx * curve;
      g.appendChild(H.path(rc, `M${x1},${y1} Q${cx},${cy} ${x2},${y2}`, o));
      // arrowhead
      const ang = Math.atan2(y2 - cy, x2 - cx);
      const a = 0.42, len = o.head ?? 16;
      g.appendChild(H.line(rc, x2, y2, x2 - len * Math.cos(ang - a), y2 - len * Math.sin(ang - a), o));
      g.appendChild(H.line(rc, x2, y2, x2 - len * Math.cos(ang + a), y2 - len * Math.sin(ang + a), o));
      return g;
    },
    // text via SVG (handwriting)
    text(svg, x, y, str, o = {}) {
      const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      t.setAttribute('x', x); t.setAttribute('y', y);
      t.setAttribute('fill', o.fill || ORANGE);
      t.setAttribute('font-family', o.font || "'Caveat',cursive");
      t.setAttribute('font-size', o.size || 26);
      t.setAttribute('font-weight', o.weight || 600);
      t.setAttribute('text-anchor', o.anchor || 'start');
      if (o.spacing) t.setAttribute('letter-spacing', o.spacing);
      t.textContent = str;
      svg.appendChild(t);
      return t;
    },
    // mono label box (used for chat/search/prompts/settings, RECIPE etc.)
    labelBox(rc, svg, x, y, w, h, str, o = {}) {
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.appendChild(H.rect(rc, x, y, w, h, { stroke: o.stroke || '#FFFFFF', strokeWidth: 2, roughness: 1.6 }));
      svg.appendChild(g);
      H.text(svg, x + w / 2, y + h / 2 + 6, str, {
        fill: o.color || '#F4F2EE', font: "'Space Mono',monospace", size: o.size || 17, weight: 400, anchor: 'middle'
      });
      return g;
    },
    // a sketchy video frame with play triangle + corner tab + progress bar
    videoFrame(rc, svg, x, y, w, h, o = {}) {
      const stroke = o.stroke || ink(o.theme);
      svg.appendChild(H.rect(rc, x, y, w, h, { stroke, strokeWidth: 2.4, roughness: 1.4 }));
      // corner tab
      svg.appendChild(H.rect(rc, x + w - 26, y + 10, 16, 12, { stroke: ORANGE, fill: ORANGE, fillStyle: 'solid', strokeWidth: 1 }));
      // play triangle
      const cx = x + w / 2, cy = y + h / 2, s = Math.min(w, h) * 0.18;
      svg.appendChild(H.path(rc, `M${cx - s * 0.7},${cy - s} L${cx + s},${cy} L${cx - s * 0.7},${cy + s} Z`,
        { stroke: ORANGE, strokeWidth: 2.4, roughness: 1.1 }));
      // progress bar
      svg.appendChild(H.rect(rc, x + w * 0.28, y + h - 22, w * 0.34, 9,
        { stroke: ORANGE, fill: ORANGE, fillStyle: 'solid', strokeWidth: 1 }));
    },
    heart(rc, svg, cx, cy, s, o = {}) {
      const d = `M${cx},${cy + s * 0.7}
        C${cx - s},${cy - s * 0.2} ${cx - s * 0.5},${cy - s} ${cx},${cy - s * 0.35}
        C${cx + s * 0.5},${cy - s} ${cx + s},${cy - s * 0.2} ${cx},${cy + s * 0.7} Z`;
      svg.appendChild(H.path(rc, d, { stroke: ORANGE, fill: ORANGE, fillStyle: 'solid', strokeWidth: 1.5, roughness: 1.2, ...o }));
    },
    // pill/tag with a centered mono or handwriting label
    tag(rc, svg, x, y, w, h, str, o = {}) {
      const fill = o.fill ? { fill: o.fill, fillStyle: 'solid' } : {};
      svg.appendChild(H.rect(rc, x, y, w, h, { stroke: o.stroke || ORANGE, strokeWidth: 2, roughness: 1.5, ...fill }));
      H.text(svg, x + w / 2, y + h / 2 + 7, str, {
        fill: o.color || ORANGE, font: o.font || "'Space Mono',monospace", size: o.size || 18,
        weight: o.weight || 700, anchor: 'middle',
      });
    },
    // magnifying glass
    magnifier(rc, svg, cx, cy, r, o = {}) {
      const c = o.stroke || ORANGE;
      svg.appendChild(H.ell(rc, cx, cy, r * 2, r * 2, { stroke: c, strokeWidth: 2.6 }));
      const a = Math.PI / 4;
      svg.appendChild(H.line(rc, cx + Math.cos(a) * r, cy + Math.sin(a) * r,
        cx + Math.cos(a) * (r + 18), cy + Math.sin(a) * (r + 18), { stroke: c, strokeWidth: 4 }));
    },
    // notification bell
    bell(rc, svg, cx, cy, s, o = {}) {
      const c = o.stroke || ORANGE;
      svg.appendChild(H.path(rc, `M${cx - s},${cy + s * 0.7}
        C${cx - s},${cy - s * 0.3} ${cx - s * 0.5},${cy - s} ${cx},${cy - s}
        C${cx + s * 0.5},${cy - s} ${cx + s},${cy - s * 0.3} ${cx + s},${cy + s * 0.7} Z`,
        { stroke: c, strokeWidth: 2.4 }));
      svg.appendChild(H.line(rc, cx - s * 1.25, cy + s * 0.7, cx + s * 1.25, cy + s * 0.7, { stroke: c, strokeWidth: 2.2 }));
      svg.appendChild(H.ell(rc, cx, cy + s * 1.05, s * 0.45, s * 0.45, { stroke: c, strokeWidth: 2 }));
      svg.appendChild(H.line(rc, cx, cy - s, cx, cy - s * 1.3, { stroke: c, strokeWidth: 2 }));
    },
    // ECG / vitals line with one critical spike, left->right
    ecg(rc, svg, x, y, w, o = {}) {
      const c = o.stroke || ORANGE, m = y; // baseline
      const sx = x + w * 0.45;
      const pts = [[x, m], [sx, m], [sx + 14, m - 6], [sx + 26, m + 46],
        [sx + 40, m - 60], [sx + 54, m + 16], [sx + 66, m], [x + w, m]];
      svg.appendChild(H.path(rc, 'M' + pts.map(p => p.join(',')).join(' L'),
        { stroke: c, strokeWidth: 2.6, roughness: 0.8, bowing: 0.4 }));
    },
    // simple robot/agent head with X or O eyes
    robot(rc, svg, x, y, w, h, o = {}) {
      const c = o.stroke || ink(o.theme);
      svg.appendChild(H.rect(rc, x, y, w, h, { stroke: c, strokeWidth: 2.6 }));
      svg.appendChild(H.line(rc, x + w / 2, y, x + w / 2, y - 16, { stroke: c, strokeWidth: 2 }));
      svg.appendChild(H.ell(rc, x + w / 2, y - 20, 9, 9, { stroke: ORANGE, fill: ORANGE, fillStyle: 'solid', strokeWidth: 1 }));
      const ex = [x + w * 0.32, x + w * 0.68], ey = y + h * 0.42, r = w * 0.1;
      ex.forEach((e) => {
        if (o.xEyes) {
          svg.appendChild(H.line(rc, e - r, ey - r, e + r, ey + r, { stroke: ORANGE, strokeWidth: 3 }));
          svg.appendChild(H.line(rc, e + r, ey - r, e - r, ey + r, { stroke: ORANGE, strokeWidth: 3 }));
        } else {
          svg.appendChild(H.ell(rc, e, ey, r * 1.6, r * 1.6, { stroke: ORANGE, strokeWidth: 2.4 }));
        }
      });
      svg.appendChild(H.line(rc, x + w * 0.3, y + h * 0.74, x + w * 0.7, y + h * 0.74, { stroke: c, strokeWidth: 2 }));
    },
    // small camera feed cell: frame + lens + REC dot
    camera(rc, svg, x, y, w, h, o = {}) {
      const c = o.stroke || ink(o.theme);
      svg.appendChild(H.rect(rc, x, y, w, h, { stroke: o.hot ? ORANGE : c, strokeWidth: o.hot ? 2.6 : 1.8, roughness: 1.6 }));
      svg.appendChild(H.ell(rc, x + w / 2, y + h / 2, w * 0.32, w * 0.32, { stroke: o.hot ? ORANGE : c, strokeWidth: 1.8 }));
      // REC dot
      svg.appendChild(H.ell(rc, x + 10, y + 10, 7, 7, { stroke: ORANGE, fill: ORANGE, fillStyle: 'solid', strokeWidth: 1 }));
    },
    // database cylinder
    cylinder(rc, svg, cx, top, w, h, o = {}) {
      const c = o.stroke || ORANGE;
      svg.appendChild(H.ell(rc, cx, top, w, w * 0.28, { stroke: c, strokeWidth: 2 }));
      svg.appendChild(H.line(rc, cx - w / 2, top, cx - w / 2, top + h, { stroke: c }));
      svg.appendChild(H.line(rc, cx + w / 2, top, cx + w / 2, top + h, { stroke: c }));
      svg.appendChild(H.path(rc, `M${cx - w / 2},${top + h} Q${cx},${top + h + w * 0.28} ${cx + w / 2},${top + h}`, { stroke: c }));
    },
  };

  // ---- per-slide art registry ----
  const ART = {
    // 01 problem: three "?" cards + stick figure + curved arrow
    problem(rc, svg, W, Hh, theme) {
      const n = neutral(theme);
      const cw = 120, ch = 150, gap = 22, y = 40;
      for (let i = 0; i < 3; i++) {
        const x = i * (cw + gap) + 10;
        svg.appendChild(H.rect(rc, x, y, cw, ch, { stroke: n, strokeWidth: 2.2 }));
        svg.appendChild(H.line(rc, x + 8, y + 34, x + cw - 8, y + 34, { stroke: n, strokeWidth: 1.6 }));
        H.text(svg, x + cw / 2, y + ch / 2 + 22, '?', { fill: n, font: "'Caveat',cursive", size: 60, anchor: 'middle' });
      }
      // stick figure
      const sx = 3 * (cw + gap) + 24, sy = y + 60;
      svg.appendChild(H.ell(rc, sx, sy, 20, 20, { stroke: ink(theme), strokeWidth: 2 }));
      svg.appendChild(H.line(rc, sx, sy + 10, sx, sy + 48, { stroke: ink(theme) }));
      svg.appendChild(H.line(rc, sx - 16, sy + 24, sx + 16, sy + 24, { stroke: ink(theme) }));
      svg.appendChild(H.line(rc, sx, sy + 48, sx - 14, sy + 72, { stroke: ink(theme) }));
      svg.appendChild(H.line(rc, sx, sy + 48, sx + 14, sy + 72, { stroke: ink(theme) }));
      // curved arrow under cards
      svg.appendChild(H.arrow(rc, 3 * (cw + gap), y + ch + 70, 20, y + ch + 50, { stroke: ORANGE, strokeWidth: 2.4, curve: 0.18 }));
      H.text(svg, 110, y + ch + 96, 're-specify it every time…', { fill: ORANGE, size: 24 });
    },

    // 02 insight: 4 label boxes -> arrows -> hatched funnel -> cylinder "taste"
    insight(rc, svg, W, Hh, theme) {
      const labels = ['chat', 'search', 'prompts', 'settings'];
      const bx = 0, bw = 150, bh = 42, gap = 18, by = 20;
      labels.forEach((l, i) => {
        const y = by + i * (bh + gap);
        H.labelBox(rc, svg, bx, y, bw, bh, l, {});
        svg.appendChild(H.arrow(rc, bx + bw + 6, y + bh / 2, 300, 150, { stroke: neutral(theme), strokeWidth: 1.6, curve: 0.05, head: 12 }));
      });
      // funnel (hatched, orange)
      const fx = 300, fy = 96;
      svg.appendChild(H.path(rc, `M${fx},${fy} L${fx + 130},${fy} L${fx + 92},${fy + 78} L${fx + 38},${fy + 78} Z`,
        { stroke: ORANGE, fill: ORANGE, fillStyle: 'hachure', hachureGap: 7, fillWeight: 1.5, strokeWidth: 2.2 }));
      // cylinder "taste"
      const cx = fx + 65, cyl = fy + 110, cw = 96, chh = 66;
      svg.appendChild(H.ell(rc, cx, cyl, cw, 24, { stroke: ORANGE, strokeWidth: 2 }));
      svg.appendChild(H.line(rc, cx - cw / 2, cyl, cx - cw / 2, cyl + chh, { stroke: ORANGE }));
      svg.appendChild(H.line(rc, cx + cw / 2, cyl, cx + cw / 2, cyl + chh, { stroke: ORANGE }));
      svg.appendChild(H.path(rc, `M${cx - cw / 2},${cyl + chh} Q${cx},${cyl + chh + 22} ${cx + cw / 2},${cyl + chh}`, { stroke: ORANGE }));
      H.text(svg, cx, cyl + chh - 6, 'taste', { fill: ORANGE, size: 22, anchor: 'middle' });
    },

    // 03 soul.md document with orange hatched header + heart + rows
    soulmd(rc, svg, W, Hh, theme) {
      const x = 18, y = 56, w = 300, h = 250;
      H.text(svg, x + w - 8, y - 18, 'auto-named ↓', { fill: ORANGE, size: 22, anchor: 'end' });
      svg.appendChild(H.rect(rc, x, y, w, h, { stroke: ink(theme), strokeWidth: 2.6 }));
      // header band hatched
      svg.appendChild(H.rect(rc, x, y, w, 46, { stroke: ORANGE, fill: ORANGE, fillStyle: 'hachure', hachureGap: 6, fillWeight: 1.4, strokeWidth: 2.4 }));
      H.text(svg, x + 18, y + 31, 'SOUL.MD', { fill: ORANGE, font: "'Space Mono',monospace", size: 18, weight: 700 });
      H.heart(rc, svg, x + w - 24, y + 22, 10);
      const rows = ['# intro', '# subtitles', '# logo', '# music', '# pacing'];
      rows.forEach((r, i) => {
        const ry = y + 84 + i * 36;
        H.text(svg, x + 22, ry, r, { fill: ink(theme), size: 24 });
        svg.appendChild(H.line(rc, x + 150, ry - 7, x + w - 22, ry - 7, { stroke: neutral(theme), strokeWidth: 1.4 }));
      });
    },

    // 04 driver: soul.md box -> arrow -> gear -> arrow -> video frame; "your style ✓"
    driver(rc, svg, W, Hh, theme) {
      // soul.md box w/ hatched header
      const bx = 0, by = 30, bw = 130, bh = 150;
      svg.appendChild(H.rect(rc, bx, by, bw, bh, { stroke: ink(theme), strokeWidth: 2.4 }));
      svg.appendChild(H.rect(rc, bx, by, bw, 30, { stroke: ORANGE, fill: ORANGE, fillStyle: 'hachure', hachureGap: 6, strokeWidth: 2 }));
      H.text(svg, bx + bw / 2, by + bh + 24, 'soul.md', { fill: neutral(theme), font: "'Space Mono',monospace", size: 15, anchor: 'middle' });
      svg.appendChild(H.arrow(rc, bx + bw + 8, by + bh / 2, bx + bw + 78, by + bh / 2, { stroke: ORANGE, strokeWidth: 2.4, curve: 0 }));
      // gear
      gear(rc, svg, bx + bw + 120, by + bh / 2, 28);
      H.text(svg, bx + bw + 120, by + bh + 24, 'agent', { fill: neutral(theme), font: "'Space Mono',monospace", size: 15, anchor: 'middle' });
      svg.appendChild(H.arrow(rc, bx + bw + 160, by + bh / 2, bx + bw + 230, by + bh / 2, { stroke: ORANGE, strokeWidth: 2.4, curve: 0 }));
      // video frame
      H.videoFrame(rc, svg, bx + bw + 250, by + 30, 150, 96, { theme });
      H.text(svg, bx + bw + 325, by + 158, 'your style ✓', { fill: ORANGE, size: 24, anchor: 'middle' });
    },

    // 05 payoff: speech box -> arrow -> big video frame; "...done."
    payoff(rc, svg, W, Hh, theme) {
      svg.appendChild(H.rect(rc, 0, 20, 250, 64, { stroke: ink(theme), strokeWidth: 2.4 }));
      H.text(svg, 125, 58, '"30s reel, Q3 launch"', { fill: ink(theme), font: "'Caveat',cursive", size: 24, anchor: 'middle' });
      svg.appendChild(H.path(rc, `M70,84 L60,140`, { stroke: ink(theme), strokeWidth: 2 }));
      svg.appendChild(H.arrow(rc, 250, 120, 320, 150, { stroke: ORANGE, strokeWidth: 2.6, curve: 0.1 }));
      H.videoFrame(rc, svg, 330, 90, 230, 150, { theme });
      H.text(svg, 445, 268, '…done.', { fill: ORANGE, size: 26, anchor: 'middle' });
    },

    // 06 record->replay: stack (one orange) -> gear -> RECIPE box
    recipe(rc, svg, W, Hh, theme) {
      const n = neutral(theme);
      svg.appendChild(H.rect(rc, 0, 30, 170, 22, { stroke: n, strokeWidth: 2 }));
      svg.appendChild(H.rect(rc, 4, 56, 170, 22, { stroke: n, strokeWidth: 2 }));
      svg.appendChild(H.rect(rc, 8, 82, 170, 24, { stroke: ORANGE, fill: ORANGE, fillStyle: 'solid', strokeWidth: 2 }));
      H.text(svg, 90, 132, 'one edit', { fill: n, font: "'Caveat',cursive", size: 20, anchor: 'middle' });
      svg.appendChild(H.arrow(rc, 184, 70, 250, 70, { stroke: ORANGE, strokeWidth: 2.4, curve: 0 }));
      gear(rc, svg, 290, 70, 26);
      H.text(svg, 290, 132, 'generalize', { fill: n, font: "'Caveat',cursive", size: 20, anchor: 'middle' });
      svg.appendChild(H.arrow(rc, 330, 70, 396, 70, { stroke: ORANGE, strokeWidth: 2.4, curve: 0 }));
      // RECIPE box
      const rx = 410, ry = 16, rw = 180, rh = 150;
      svg.appendChild(H.rect(rc, rx, ry, rw, rh, { stroke: ink(theme), strokeWidth: 2.6 }));
      H.text(svg, rx + rw / 2, ry + 30, 'RECIPE', { fill: ORANGE, font: "'Space Mono',monospace", size: 17, weight: 700, anchor: 'middle' });
      svg.appendChild(H.line(rc, rx + 16, ry + 44, rx + rw - 16, ry + 44, { stroke: neutral(theme), strokeWidth: 1.4 }));
      ['{topic}', '{brand}', '{collection}'].forEach((t, i) =>
        H.text(svg, rx + 20, ry + 78 + i * 32, t, { fill: ORANGE, size: 24 }));
    },

    // 07 at scale: RECIPE -> fan of arrows -> 2x3 grid of video frames
    scale(rc, svg, W, Hh, theme) {
      const rx = 0, ry = 90, rw = 150, rh = 90;
      svg.appendChild(H.rect(rc, rx, ry, rw, rh, { stroke: ink(theme), strokeWidth: 2.6 }));
      H.text(svg, rx + rw / 2, ry + rh / 2 + 7, 'RECIPE', { fill: ORANGE, font: "'Space Mono',monospace", size: 17, weight: 700, anchor: 'middle' });
      const gx = 230, gy = 0, fw = 116, fh = 74, gpx = 24, gpy = 22;
      for (let r = 0; r < 3; r++) for (let c = 0; c < 2; c++) {
        const x = gx + c * (fw + gpx), y = gy + r * (fh + gpy);
        H.videoFrame(rc, svg, x, y, fw, fh, { theme });
        svg.appendChild(H.arrow(rc, rx + rw + 4, ry + rh / 2, x - 6, y + fh / 2, { stroke: neutral(theme), strokeWidth: 1.3, curve: 0.04, head: 10 }));
      }
      H.text(svg, gx + 2 * fw + gpx, gy + 3 * fh + 2 * gpy + 8, 'N outputs →', { fill: neutral(theme), font: "'Caveat',cursive", size: 22, anchor: 'end' });
    },

    // 08 loop: circle with clarify/do/verify/ship + center "loop"
    loop(rc, svg, W, Hh, theme) {
      const cx = 150, cy = 150, r = 110, n = neutral(theme);
      // 4 arcs forming the loop
      svg.appendChild(H.ell(rc, cx, cy, r * 2, r * 2, { stroke: n, strokeWidth: 2, roughness: 1.6 }));
      // arrowheads at top/right/bottom/left tangents
      [[cx, cy - r, 1], [cx + r, cy, 1]].forEach(([x, y]) => {});
      svg.appendChild(H.ell(rc, cx, cy, 86, 50, { stroke: ORANGE, strokeWidth: 2.4 }));
      H.text(svg, cx, cy + 8, 'loop', { fill: ORANGE, size: 26, anchor: 'middle' });
      H.text(svg, cx, cy - r - 12, 'clarify', { fill: n, font: "'Caveat',cursive", size: 22, anchor: 'middle' });
      H.text(svg, cx + r + 8, cy + 6, 'do', { fill: n, font: "'Caveat',cursive", size: 22 });
      H.text(svg, cx, cy + r + 26, 'verify', { fill: n, font: "'Caveat',cursive", size: 22, anchor: 'middle' });
      H.text(svg, cx - r - 8, cy + 6, 'ship', { fill: n, font: "'Caveat',cursive", size: 22, anchor: 'end' });
      H.text(svg, cx, cy + r + 50, 'until it passes', { fill: n, size: 19, anchor: 'middle' });
    },

    // hero reticle (title slide): target circle + heart center
    reticle(rc, svg, W, Hh, theme) {
      const cx = W / 2, cy = Hh / 2 - 10, r = 46, n = neutral(theme);
      svg.appendChild(H.ell(rc, cx, cy, r * 2, r * 2, { stroke: n, strokeWidth: 2 }));
      // tick marks
      [[0, -1], [1, 0], [0, 1], [-1, 0]].forEach(([dx, dy]) => {
        svg.appendChild(H.line(rc, cx + dx * r, cy + dy * r, cx + dx * (r + 12), cy + dy * (r + 12), { stroke: n, strokeWidth: 1.6 }));
      });
      H.heart(rc, svg, cx, cy, 14);
      H.text(svg, cx, cy + r + 34, 'the soul engine', { fill: n, size: 22, anchor: 'middle' });
    },

    // chess-lens: 8x8 hand-drawn board, piece glyphs, one piece ringed w/ arrow one square over
    board(rc, svg, W, Hh, theme) {
      const n = neutral(theme), k = ink(theme);
      const B = Math.min(W, Hh) - 46;               // room for file/rank labels
      const x0 = (W - B) / 2 + 8, y0 = 6, c = B / 8;
      svg.appendChild(H.rect(rc, x0, y0, B, B, { stroke: k, strokeWidth: 2.6 }));
      for (let i = 1; i < 8; i++) {
        svg.appendChild(H.line(rc, x0 + i * c, y0, x0 + i * c, y0 + B, { stroke: n, strokeWidth: 1.2, roughness: 1.7 }));
        svg.appendChild(H.line(rc, x0, y0 + i * c, x0 + B, y0 + i * c, { stroke: n, strokeWidth: 1.2, roughness: 1.7 }));
      }
      // file / rank labels
      'abcdefgh'.split('').forEach((f, i) =>
        H.text(svg, x0 + i * c + c / 2, y0 + B + 19, f, { fill: n, font: "'Space Mono',monospace", size: 12, weight: 400, anchor: 'middle' }));
      for (let i = 0; i < 8; i++)
        H.text(svg, x0 - 11, y0 + i * c + c / 2 + 4, String(8 - i), { fill: n, font: "'Space Mono',monospace", size: 12, weight: 400, anchor: 'end' });
      // piece glyphs: a few circles + crosses
      [[1, 1], [4, 2], [6, 5], [2, 6], [5, 7]].forEach(([cc, rr]) =>
        svg.appendChild(H.ell(rc, x0 + cc * c + c / 2, y0 + rr * c + c / 2, c * 0.5, c * 0.5, { stroke: k, strokeWidth: 2 })));
      [[6, 1], [1, 4], [3, 6]].forEach(([cc, rr]) => {
        const px = x0 + cc * c + c / 2, py = y0 + rr * c + c / 2, r = c * 0.2;
        svg.appendChild(H.line(rc, px - r, py - r, px + r, py + r, { stroke: k, strokeWidth: 2 }));
        svg.appendChild(H.line(rc, px + r, py - r, px - r, py + r, { stroke: k, strokeWidth: 2 }));
      });
      // the misplaced piece: solid dot + hand-drawn ring + arrow one square over
      const tx = x0 + 3 * c + c / 2, ty = y0 + 3 * c + c / 2;
      svg.appendChild(H.ell(rc, tx, ty, c * 0.5, c * 0.5, { stroke: ORANGE, fill: ORANGE, fillStyle: 'solid', strokeWidth: 1.6 }));
      svg.appendChild(H.ell(rc, tx, ty, c * 1.02, c * 1.02, { stroke: ORANGE, strokeWidth: 2.4, roughness: 2 }));
      svg.appendChild(H.arrow(rc, tx + c * 0.6, ty - c * 0.66, tx + c, ty - c * 0.28, { stroke: ORANGE, strokeWidth: 2.2, curve: 0.3, head: 11 }));
      H.text(svg, tx + c * 1.35, ty - c * 0.95, 'off by one', { fill: ORANGE, size: 20 });
    },

    // chess-lens: one rank of 8 squares — piece in square 3, dashed ghost in square 4
    shifted(rc, svg, W, Hh, theme) {
      const n = neutral(theme), k = ink(theme);
      const c = Math.min(W / 8.6, Hh - 96);
      const x0 = (W - c * 8) / 2, y0 = (Hh - c) / 2 + 8;
      for (let i = 0; i < 8; i++)
        svg.appendChild(H.rect(rc, x0 + i * c, y0, c, c,
          { stroke: (i === 2 || i === 3) ? k : n, strokeWidth: (i === 2 || i === 3) ? 2.4 : 1.5 }));
      'abcdefgh'.split('').forEach((f, i) =>
        H.text(svg, x0 + i * c + c / 2, y0 + c + 20, f, { fill: n, font: "'Space Mono',monospace", size: 12, weight: 400, anchor: 'middle' }));
      const p1x = x0 + 2 * c + c / 2, p2x = x0 + 3 * c + c / 2, py = y0 + c / 2;
      // the real piece
      svg.appendChild(H.ell(rc, p1x, py, c * 0.52, c * 0.52, { stroke: k, strokeWidth: 2.6 }));
      svg.appendChild(H.ell(rc, p1x, py, c * 0.18, c * 0.18, { stroke: k, fill: k, fillStyle: 'solid', strokeWidth: 1 }));
      // the ghost copy, one file over
      svg.appendChild(H.ell(rc, p2x, py, c * 0.52, c * 0.52, { stroke: ORANGE, strokeWidth: 2.2, strokeLineDash: [7, 6] }));
      // sketchy arrow between them
      svg.appendChild(H.arrow(rc, p1x + c * 0.2, y0 - 16, p2x - c * 0.05, y0 - 8, { stroke: ORANGE, strokeWidth: 2.2, curve: -0.5, head: 11 }));
      H.text(svg, (p1x + p2x) / 2, y0 - 38, 'one file over', { fill: ORANGE, size: 22, anchor: 'middle' });
      H.text(svg, p1x + c * 0.1, y0 + c + 46, 'the board', { fill: n, size: 20, anchor: 'end' });
      H.text(svg, p2x - c * 0.1, y0 + c + 46, 'the model', { fill: ORANGE, size: 20, anchor: 'start' });
    },

    // chess-lens: two robots head-to-head, each at multiple thinking budgets
    contenders(rc, svg, W, Hh, theme) {
      const n = neutral(theme), k = ink(theme);
      const rw = 120, rh = 108, y = 34;
      const x1 = W * 0.18 - rw / 2, x2 = W * 0.82 - rw / 2;
      H.robot(rc, svg, x1, y, rw, rh, { theme });
      H.robot(rc, svg, x2, y, rw, rh, { theme });
      H.text(svg, x1 + rw / 2, y + rh + 32, 'GPT-5.4', { fill: k, font: "'Space Mono',monospace", size: 16, weight: 700, anchor: 'middle' });
      H.text(svg, x2 + rw / 2, y + rh + 32, 'CLAUDE OPUS 4.7', { fill: k, font: "'Space Mono',monospace", size: 16, weight: 700, anchor: 'middle' });
      H.text(svg, W / 2, y + rh / 2 + 12, 'vs', { fill: ORANGE, size: 46, anchor: 'middle' });
      // bracket underneath: both swept across thinking budgets
      const by = y + rh + 52;
      svg.appendChild(H.path(rc, `M${x1},${by} L${x1},${by + 13} L${x2 + rw},${by + 13} L${x2 + rw},${by}`, { stroke: n, strokeWidth: 1.7 }));
      H.text(svg, W / 2, by + 42, 'MIN → MAX THINKING', { fill: n, font: "'Space Mono',monospace", size: 14, weight: 700, anchor: 'middle', spacing: '.2em' });
      H.text(svg, W / 2, by + 70, 'each swept across thinking budgets', { fill: n, size: 21, anchor: 'middle' });
    },

    // chess-lens: photo of a board -> arrow -> exact FEN box
    photo2fen(rc, svg, W, Hh, theme) {
      const n = neutral(theme), k = ink(theme);
      const bx = 4, by = 24, bs = 150, cc = bs / 4;
      svg.appendChild(H.rect(rc, bx, by, bs, bs, { stroke: k, strokeWidth: 2.4 }));
      for (let i = 1; i < 4; i++) {
        svg.appendChild(H.line(rc, bx + i * cc, by, bx + i * cc, by + bs, { stroke: n, strokeWidth: 1.2 }));
        svg.appendChild(H.line(rc, bx, by + i * cc, bx + bs, by + i * cc, { stroke: n, strokeWidth: 1.2 }));
      }
      [[0, 1], [2, 2], [3, 0], [1, 3]].forEach(([ccx, rr]) =>
        svg.appendChild(H.ell(rc, bx + ccx * cc + cc / 2, by + rr * cc + cc / 2, cc * 0.5, cc * 0.5, { stroke: k, strokeWidth: 2 })));
      H.text(svg, bx + bs / 2, by + bs + 28, 'one photo', { fill: n, size: 21, anchor: 'middle' });
      svg.appendChild(H.arrow(rc, bx + bs + 16, by + bs / 2, bx + bs + 92, by + bs / 2, { stroke: ORANGE, strokeWidth: 2.4, curve: 0.12 }));
      H.labelBox(rc, svg, bx + bs + 106, by + bs / 2 - 26, 150, 52, 'EXACT FEN', { stroke: k, color: k, size: 16 });
      H.text(svg, bx + bs + 181, by + bs / 2 + 56, 'every square, exactly', { fill: ORANGE, size: 21, anchor: 'middle' });
    },

    // chess-lens: two ways of seeing — row-by-row scan vs one holistic ring
    seeing(rc, svg, W, Hh, theme) {
      const n = neutral(theme), k = ink(theme);
      const bs = Math.min(Hh - 96, W / 2 - 70), cell = bs / 4, gy = 40;
      const gx1 = W * 0.25 - bs / 2, gx2 = W * 0.75 - bs / 2;
      H.text(svg, gx1 + bs / 2, 16, 'GPT-5.4', { fill: k, font: "'Space Mono',monospace", size: 14, weight: 700, anchor: 'middle' });
      H.text(svg, gx2 + bs / 2, 16, 'CLAUDE OPUS 4.7', { fill: k, font: "'Space Mono',monospace", size: 14, weight: 700, anchor: 'middle' });
      [gx1, gx2].forEach((gx) => {
        svg.appendChild(H.rect(rc, gx, gy, bs, bs, { stroke: k, strokeWidth: 2.2 }));
        for (let i = 1; i < 4; i++) {
          svg.appendChild(H.line(rc, gx + i * cell, gy, gx + i * cell, gy + bs, { stroke: n, strokeWidth: 1.1 }));
          svg.appendChild(H.line(rc, gx, gy + i * cell, gx + bs, gy + i * cell, { stroke: n, strokeWidth: 1.1 }));
        }
      });
      // left: procedural row-by-row scan arrows
      for (let r = 0; r < 4; r++)
        svg.appendChild(H.arrow(rc, gx1 + 8, gy + r * cell + cell / 2, gx1 + bs - 10, gy + r * cell + cell / 2,
          { stroke: ORANGE, strokeWidth: 1.7, curve: 0, head: 9 }));
      // right: one big holistic ring
      svg.appendChild(H.ell(rc, gx2 + bs / 2, gy + bs / 2, bs * 1.2, bs * 1.08, { stroke: ORANGE, strokeWidth: 2.4, roughness: 1.9 }));
      H.text(svg, gx1 + bs / 2, gy + bs + 32, 'row by row', { fill: n, size: 21, anchor: 'middle' });
      H.text(svg, gx2 + bs / 2, gy + bs + 32, 'the whole position', { fill: n, size: 21, anchor: 'middle' });
    },

  };

  // gear helper used by several slides
  function gear(rc, svg, cx, cy, r) {
    svg.appendChild(H.ell(rc, cx, cy, r * 2, r * 2, { stroke: ORANGE, strokeWidth: 2.2 }));
    svg.appendChild(H.ell(rc, cx, cy, r * 0.8, r * 0.8, { stroke: ORANGE, strokeWidth: 2 }));
    for (let i = 0; i < 8; i++) {
      const a = (i / 8) * Math.PI * 2;
      svg.appendChild(H.line(rc, cx + Math.cos(a) * r, cy + Math.sin(a) * r,
        cx + Math.cos(a) * (r + 9), cy + Math.sin(a) * (r + 9), { stroke: ORANGE, strokeWidth: 2 }));
    }
  }

  // ---- boot: fill every .art[data-art] ----
  function draw() {
    document.querySelectorAll('.art[data-art]').forEach((div) => {
      const name = div.dataset.art;
      const fn = ART[name];
      if (!fn) return;
      const W = +div.dataset.w || div.clientWidth || 480;
      const Hh = +div.dataset.h || div.clientHeight || 360;
      const slide = div.closest('.slide');
      const cssOrange = getComputedStyle(slide).getPropertyValue('--orange').trim();
      if (cssOrange) ORANGE = cssOrange;   // honor per-deck accent
      const theme = slide.classList.contains('light') ? 'light' : 'dark';
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      // responsive: drawing coords are W×Hh (viewBox); the svg fills the div and scales
      svg.setAttribute('viewBox', `0 0 ${W} ${Hh}`);
      svg.setAttribute('width', '100%'); svg.setAttribute('height', '100%');
      svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
      svg.style.overflow = 'visible'; svg.style.display = 'block';
      div.appendChild(svg);
      const rc = rough.svg(svg);
      fn(rc, svg, W, Hh, theme);
    });
    document.body.setAttribute('data-doodles-ready', '1');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', draw);
  else draw();
})();
