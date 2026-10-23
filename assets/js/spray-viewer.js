/* Weapon spray (recoil) viewer (pipelines/spray-viewer.md; styles in _sass/custom/spray-viewer.scss, on
   top of the vehicle viewer's .vv-* styles). Data: assets/data/spray-patterns.json.
   - x is yaw in degrees (right +), y is pitch in degrees (up +). A shot's kick is added to the view and
     firearms do not recover by themselves, so the plotted spray is the running sum of the kicks;
   - kick n is pattern[n] while the pattern lasts, then the middle of the post-pattern yaw/pitch ranges
     (the random section's expected value); expectedPath in the data is that running sum;
   - the p10/p90 band covers the random section, the fan shows the +-randomDeviationDeg turn of each
     pattern kick;
   - factors (stance, focus, default-attachment multipliers) scale the whole path.
   Pure functions are exported (module.exports / globalThis.SprayViewerCore) for _tools/spray_viewer_check.js.
   Strings from the data are set as text only. */
(function () {
  "use strict";

  /* ---------- pure model ---------- */

  var EPS = 1e-9;

  function kickAt(season, i) {
    var p = season.pattern || [];
    if (i < p.length) return { x: p[i].x, y: p[i].y, random: false };
    var pp = season.postPattern || { yaw: [0, 0], pitch: [0, 0] };
    return { x: (pp.yaw[0] + pp.yaw[1]) / 2, y: (pp.pitch[0] + pp.pitch[1]) / 2, random: true };
  }

  // Running sum of the kicks, shot 1 first. n defaults to the length of the data's expectedPath.
  function cumulativePath(season, n) {
    if (n == null) n = season.expectedPath ? season.expectedPath.length : Math.max(30, (season.pattern || []).length);
    var out = [], cx = 0, cy = 0;
    for (var i = 0; i < n; i++) {
      var k = kickAt(season, i);
      cx += k.x; cy += k.y;
      out.push({ shot: i + 1, x: cx, y: cy });
    }
    return out;
  }

  // Scale factors for the chosen stance / focus / attachment toggles.
  function factors(season, opt) {
    var m = season.multipliers || {};
    var st = (m.stance && m.stance[opt.stance || "stand"]);
    if (st == null) st = 1;
    var f = st * (season.viewKickMagnitudeMultiplier == null ? 1 : season.viewKickMagnitudeMultiplier);
    if (opt.focus) f *= 1 - (season.focusReductionPct || 0) / 100;
    var h = opt.attachments && m.horizontal != null ? m.horizontal : 1;
    var v = opt.attachments && m.vertical != null ? m.vertical : 1;
    return { x: f * h, y: f * v };
  }

  function scalePoints(pts, f) {
    return pts.map(function (p) { var q = { x: p.x * f.x, y: p.y * f.y }; if (p.shot != null) q.shot = p.shot; return q; });
  }

  function climbAfter(path, n) {
    if (!path.length) return null;
    return path[Math.min(n, path.length) - 1].y;
  }

  function xExtent(path, band) {
    var lo = Infinity, hi = -Infinity;
    function add(p) { if (p.x < lo) lo = p.x; if (p.x > hi) hi = p.x; }
    path.forEach(add);
    if (band) { band.p10.forEach(add); band.p90.forEach(add); }
    return path.length ? hi - lo : null;
  }

  function targetOffset(deg, distM) { return distM * Math.tan(deg * Math.PI / 180); }
  function degForOffset(m, distM) { return Math.atan(m / distM) * 180 / Math.PI; }

  function shotsChanged(a, b) {
    var n = Math.max(a.expectedPath.length, b.expectedPath.length), c = 0;
    for (var i = 0; i < n; i++) {
      var ka = i < a.expectedPath.length ? kickAt(a, i) : null, kb = i < b.expectedPath.length ? kickAt(b, i) : null;
      if (!ka || !kb || Math.abs(ka.x - kb.x) > 1e-6 || Math.abs(ka.y - kb.y) > 1e-6) c++;
    }
    return c;
  }

  function niceStep(span, target) {
    var raw = span / target, mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), r = raw / mag;
    return (r < 1.5 ? 1 : r < 3.5 ? 2 : r < 7.5 ? 5 : 10) * mag;
  }

  function fmt(v, d) {
    if (v == null || !isFinite(v)) return "n/a";
    return (Math.abs(v) < 5e-5 ? 0 : v).toFixed(d == null ? 2 : d).replace("-0.00", "0.00");
  }

  var core = {
    kickAt: kickAt, cumulativePath: cumulativePath, factors: factors, scalePoints: scalePoints,
    climbAfter: climbAfter, xExtent: xExtent, targetOffset: targetOffset, degForOffset: degForOffset,
    shotsChanged: shotsChanged, niceStep: niceStep
  };
  if (typeof module !== "undefined" && module.exports) module.exports = core;
  if (typeof globalThis !== "undefined") globalThis.SprayViewerCore = core;
  if (typeof document === "undefined" || !document.getElementById || !document.getElementById("sv")) return;

  /* ---------- view ---------- */

  var NS = "http://www.w3.org/2000/svg";
  var CATEGORY_LABEL = { infantry: "Infantry", vehicle: "Vehicle", stationary: "Stationary", test: "Test", tool: "Tools", other: "Other" };
  var root = document.getElementById("sv");
  var state = { data: null, weapon: null, season: "s2", stance: "stand", focus: false, attachments: false,
                fan: true, band: true, metres: false, dist: 100, nShots: 30, inspect: 1, category: "infantry", sameScale: true };
  var els = {};

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function svg(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(e);
    return e;
  }
  function clear(n) { while (n.firstChild) n.removeChild(n.firstChild); }

  function seasonOf(w, k) { var s = w.seasons[k]; return s && s.present !== false ? s : null; }

  // Which seasons the control shows for this weapon, plus a note when the choice falls back.
  function visibleSeasons(w) {
    var s1 = seasonOf(w, "s1"), s2 = seasonOf(w, "s2"), want = state.season, note = "";
    var list = [];
    if (want === "compare") {
      if (s1 && s2) list = ["s1", "s2"];
      else if (s2) { list = ["s2"]; note = "Season 1 has no data for this weapon: showing Season 2 only."; }
      else if (s1) { list = ["s1"]; note = "Season 2 has no data for this weapon: showing Season 1 only."; }
    } else if (want === "s1") {
      if (s1) list = ["s1"];
      else if (s2) { list = ["s2"]; note = "Season 1 has no data for this weapon: showing Season 2."; }
    } else {
      if (s2) list = ["s2"];
      else if (s1) { list = ["s1"]; note = "Season 2 has no data for this weapon: showing Season 1."; }
    }
    return { list: list, note: note, s1: s1, s2: s2 };
  }

  function opts() { return { stance: state.stance, focus: state.focus, attachments: state.attachments }; }

  // Everything one season draws, already scaled by the toggles.
  function seriesFor(season, n) {
    var nn = Math.min(n, season.expectedPath.length), f = factors(season, opts());
    var path = scalePoints(cumulativePath(season, nn), f);
    var band = null, fan = [];
    if (season.band && season.band.p10) {
      band = { p10: scalePoints(season.band.p10.slice(0, nn), f), p90: scalePoints(season.band.p90.slice(0, nn), f) };
    }
    var dev = (season.randomDeviationDeg || 0) * Math.PI / 180, plen = (season.pattern || []).length;
    for (var i = 0; i < Math.min(nn, plen); i++) {
      var k = { x: season.pattern[i].x * f.x, y: season.pattern[i].y * f.y };
      var from = i ? path[i - 1] : { x: 0, y: 0 };
      [-dev, dev].forEach(function (a, j) {
        var c = Math.cos(a), s = Math.sin(a);
        fan[i] = fan[i] || { from: from, ends: [] };
        fan[i].ends[j] = { x: from.x + k.x * c - k.y * s, y: from.y + k.x * s + k.y * c };
      });
    }
    return { season: season, path: path, band: band, fan: fan, plen: plen };
  }

  /* ---------- main plot ---------- */

  var VW = 760, VH = 620, M = { l: 62, r: 62, t: 44, b: 52 };

  function domain(all, withFan) {
    var xs = [0], ys = [0];
    all.forEach(function (s) {
      s.path.forEach(function (p) { xs.push(p.x); ys.push(p.y); });
      if (s.band && state.band) s.band.p10.concat(s.band.p90).forEach(function (p) { xs.push(p.x); ys.push(p.y); });
      if (withFan && s.fan) s.fan.forEach(function (f) { f.ends.forEach(function (p) { xs.push(p.x); ys.push(p.y); }); });
    });
    var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
    var ys2 = (y1 - y0) || 1, xs2 = x1 - x0;
    if (xs2 < ys2 * 0.6) { var mid = (x0 + x1) / 2; x0 = mid - ys2 * 0.3; x1 = mid + ys2 * 0.3; xs2 = x1 - x0; }
    var padX = xs2 * 0.08, padY = ys2 * 0.08;
    return { x0: x0 - padX, x1: x1 + padX, y0: y0 - padY, y1: y1 + padY };
  }

  function makeScale(d, w, h, ox, oy) {
    var sx = w / (d.x1 - d.x0), sy = h / (d.y1 - d.y0), s = Math.min(sx, sy);
    var cx = ox + w / 2 - s * (d.x0 + d.x1) / 2, cy = oy + h / 2 + s * (d.y0 + d.y1) / 2;
    return { s: s, X: function (x) { return cx + s * x; }, Y: function (y) { return cy - s * y; } };
  }

  function marker(parent, kind, x, y, r, cls) {
    if (kind === "square") return svg("rect", { x: x - r, y: y - r, width: 2 * r, height: 2 * r, class: cls }, parent);
    return svg("circle", { cx: x, cy: y, r: r, class: cls }, parent);
  }

  function drawPlot() {
    var host = els.plot, vis = visibleSeasons(state.weapon);
    clear(host);
    var all = vis.list.map(function (k) { var s = seriesFor(k === "s1" ? vis.s1 : vis.s2, state.nShots); s.key = k; return s; });
    var root2 = svg("svg", { viewBox: "0 0 " + VW + " " + VH, class: "sv-svg", role: "img", tabindex: "0",
      "aria-label": "Spray plot of " + state.weapon.name + ": cumulative view offset in degrees by shot. Arrow keys step the inspected shot." }, host);
    els.svg = root2;
    if (!all.length) { svg("text", { x: VW / 2, y: VH / 2, class: "sv-text", "text-anchor": "middle" }, root2).textContent = "No data for this weapon."; return all; }
    var d = domain(all, state.fan), pw = VW - M.l - M.r, ph = VH - M.t - M.b, sc = makeScale(d, pw, ph, M.l, M.t);
    var left = (M.l + pw / 2) - sc.s * (d.x1 - d.x0) / 2, right = left + sc.s * (d.x1 - d.x0);
    var top = (M.t + ph / 2) - sc.s * (d.y1 - d.y0) / 2, bottom = top + sc.s * (d.y1 - d.y0);
    var step = niceStep(Math.max(d.x1 - d.x0, d.y1 - d.y0), 7), g = svg("g", null, root2), dist = state.dist;

    function tick(v, axis) {
      var t = Math.round(v / step) * step;
      return t;
    }
    // grid + degree axes
    var i, v;
    for (v = Math.ceil(d.x0 / step) * step; v <= d.x1 + EPS; v += step) {
      v = tick(v);
      var xp = sc.X(v); if (xp < left - 0.5 || xp > right + 0.5) continue;
      svg("line", { x1: xp, x2: xp, y1: top, y2: bottom, class: v === 0 ? "sv-zero" : "sv-grid" }, g);
      svg("text", { x: xp, y: bottom + 18, class: "sv-text", "text-anchor": "middle" }, g).textContent = fmt(v, step < 0.1 ? 2 : 1);
    }
    for (v = Math.ceil(d.y0 / step) * step; v <= d.y1 + EPS; v += step) {
      v = tick(v);
      var yp = sc.Y(v); if (yp < top - 0.5 || yp > bottom + 0.5) continue;
      svg("line", { x1: left, x2: right, y1: yp, y2: yp, class: v === 0 ? "sv-zero" : "sv-grid" }, g);
      svg("text", { x: left - 8, y: yp + 4, class: "sv-text", "text-anchor": "end" }, g).textContent = fmt(v, step < 0.1 ? 2 : 1);
    }
    svg("text", { x: (left + right) / 2, y: VH - 8, class: "sv-axis-title", "text-anchor": "middle" }, g).textContent = "Yaw, degrees (right +)";
    svg("text", { x: 14, y: (top + bottom) / 2, class: "sv-axis-title", "text-anchor": "middle", transform: "rotate(-90 14 " + (top + bottom) / 2 + ")" }, g).textContent = "Pitch, degrees (up +)";
    // metres at the chosen distance: second scale on the top (yaw) and right (pitch) edges
    if (state.metres && dist > 0) {
      var spanX = targetOffset(d.x1, dist) - targetOffset(d.x0, dist), spanY = targetOffset(d.y1, dist) - targetOffset(d.y0, dist);
      var mstep = niceStep(Math.max(spanX, spanY), 7), m;
      for (m = Math.ceil(targetOffset(d.x0, dist) / mstep) * mstep; m <= targetOffset(d.x1, dist) + EPS; m += mstep) {
        var mx = sc.X(degForOffset(m, dist)); if (mx < left - 0.5 || mx > right + 0.5) continue;
        svg("line", { x1: mx, x2: mx, y1: top, y2: top - 5, class: "sv-tick2" }, g);
        svg("text", { x: mx, y: top - 9, class: "sv-text2", "text-anchor": "middle" }, g).textContent = fmt(m, mstep < 0.1 ? 2 : mstep < 1 ? 1 : 0);
      }
      for (m = Math.ceil(targetOffset(d.y0, dist) / mstep) * mstep; m <= targetOffset(d.y1, dist) + EPS; m += mstep) {
        var my = sc.Y(degForOffset(m, dist)); if (my < top - 0.5 || my > bottom + 0.5) continue;
        svg("line", { x1: right, x2: right + 5, y1: my, y2: my, class: "sv-tick2" }, g);
        svg("text", { x: right + 9, y: my + 4, class: "sv-text2" }, g).textContent = fmt(m, mstep < 0.1 ? 2 : mstep < 1 ? 1 : 0);
      }
      svg("text", { x: right, y: 14, class: "sv-axis-title2", "text-anchor": "end" }, g).textContent = "Metres on a target " + dist + " m away";
    }
    svg("rect", { x: left, y: top, width: right - left, height: bottom - top, class: "sv-frame" }, g);

    // series
    all.forEach(function (s) {
      var cls = "sv-" + s.key, grp = svg("g", { class: cls }, g);
      if (state.fan) s.fan.forEach(function (f) {
        if (!f) return;
        svg("polygon", { points: [f.from, f.ends[0], f.ends[1]].map(function (p) { return sc.X(p.x).toFixed(1) + "," + sc.Y(p.y).toFixed(1); }).join(" "), class: "sv-fan" }, grp);
      });
      if (state.band && s.band) for (i = Math.max(0, s.plen - 1); i < s.path.length; i++) {
        var a = s.band.p10[i], b = s.band.p90[i], w = Math.max(1, Math.abs(sc.X(b.x) - sc.X(a.x))), h = Math.max(1, Math.abs(sc.Y(a.y) - sc.Y(b.y)));
        svg("rect", { x: Math.min(sc.X(a.x), sc.X(b.x)), y: Math.min(sc.Y(a.y), sc.Y(b.y)), width: w, height: h, class: "sv-band" }, grp);
      }
      var pts = [{ x: 0, y: 0 }].concat(s.path).map(function (p) { return sc.X(p.x).toFixed(1) + "," + sc.Y(p.y).toFixed(1); }).join(" ");
      svg("polyline", { points: pts, class: "sv-line" }, grp);
      var every = s.path.length > 36 ? 5 : s.path.length > 18 && all.length > 1 ? 2 : 1;
      s.path.forEach(function (p, j) {
        var inPat = j < s.plen, mk = marker(grp, s.key === "s1" ? "circle" : "square", sc.X(p.x), sc.Y(p.y), j + 1 === state.inspect ? 6 : 4, "sv-dot" + (inPat ? "" : " is-random"));
        if ((j + 1) % every === 0 || j === 0 || j === s.path.length - 1) {
          var t = svg("text", { x: sc.X(p.x) + (s.key === "s1" ? -7 : 7), y: sc.Y(p.y) + 3, class: "sv-num", "text-anchor": s.key === "s1" ? "end" : "start" }, grp);
          t.textContent = String(j + 1);
        }
      });
    });
    var o = marker(g, "circle", sc.X(0), sc.Y(0), 4, "sv-origin");
    svg("title", null, o).textContent = "Aim point before the first shot";
    // inspected shot cross-hair
    all.forEach(function (s) {
      var p = s.path[Math.min(state.inspect, s.path.length) - 1];
      if (p) svg("circle", { cx: sc.X(p.x), cy: sc.Y(p.y), r: 10, class: "sv-pick sv-pick-" + s.key }, g);
    });
    els.scale = sc; els.shown = all;
    return all;
  }

  /* ---------- timeline ---------- */

  function drawTimeline(all) {
    var host = els.timeline; clear(host);
    var W = 760, rowH = 56, H = 40 + all.length * rowH + 28, L = 62, R = 24;
    var sv = svg("svg", { viewBox: "0 0 " + W + " " + H, class: "sv-svg sv-tl", role: "img",
      "aria-label": "Fire-rate timeline: when each shot happens at the weapon's rounds per minute, with the pattern reset time marked" }, host);
    var tmax = 0, noRpm = [];
    all.forEach(function (s) {
      var r = s.season.rpm;
      if (!r) { noRpm.push(s.key); return; }
      var T = (s.path.length - 1) * 60 / r + (s.season.recoilPatternResetTime_s || 0);
      if (T > tmax) tmax = T;
    });
    if (!tmax) {
      svg("text", { x: W / 2, y: H / 2, class: "sv-text", "text-anchor": "middle" }, sv).textContent = "No fire rate in the data for this weapon.";
      return;
    }
    var sx = function (t) { return L + (W - L - R) * t / tmax; }, step = niceStep(tmax, 8), v;
    for (v = 0; v <= tmax + EPS; v += step) {
      svg("line", { x1: sx(v), x2: sx(v), y1: 24, y2: H - 28, class: "sv-grid" }, sv);
      svg("text", { x: sx(v), y: H - 12, class: "sv-text", "text-anchor": "middle" }, sv).textContent = fmt(v, step < 0.1 ? 2 : step < 1 ? 1 : 0) + " s";
    }
    all.forEach(function (s, ri) {
      var r = s.season.rpm, y = 40 + ri * rowH + 16, cls = "sv-" + s.key;
      var g = svg("g", { class: cls }, sv);
      svg("text", { x: 6, y: y + 4, class: "sv-text sv-rowname" }, g).textContent = s.key === "s1" ? "S1" : "S2";
      if (!r) { svg("text", { x: L + 6, y: y + 4, class: "sv-text" }, g).textContent = "No RPM in the data"; return; }
      var iv = 60 / r, last = (s.path.length - 1) * iv, reset = s.season.recoilPatternResetTime_s || 0;
      svg("rect", { x: sx(last), y: y - 14, width: Math.max(1, sx(last + reset) - sx(last)), height: 28, class: "sv-reset" }, g);
      svg("text", { x: sx(last) + 4, y: y - 17, class: "sv-text2" }, g).textContent = "reset " + fmt(reset, 2) + " s";
      svg("line", { x1: L, x2: sx(last + reset), y1: y, y2: y, class: "sv-line" }, g);
      for (var j = 0; j < s.path.length; j++) {
        var mk = marker(g, s.key === "s1" ? "circle" : "square", sx(j * iv), y, j < s.plen ? 4 : 3, "sv-dot" + (j < s.plen ? "" : " is-random"));
        svg("title", null, mk).textContent = "Shot " + (j + 1) + " at " + fmt(j * iv, 2) + " s";
      }
      if (s.plen > 0 && s.plen < s.path.length) {
        svg("line", { x1: sx(s.plen * iv - iv / 2), x2: sx(s.plen * iv - iv / 2), y1: y - 14, y2: y + 14, class: "sv-end" }, g);
      }
      if (iv >= reset && reset > 0) svg("text", { x: W - R, y: y + 24, class: "sv-text2", "text-anchor": "end" }, g).textContent = "Shots " + fmt(iv, 2) + " s apart exceed the " + fmt(reset, 2) + " s reset: every shot starts the pattern again.";
    });
  }

  /* ---------- panel: readout + diff ---------- */

  function row(tr, cells, th) {
    cells.forEach(function (c, i) { var td = el(th || i === 0 ? "th" : "td", null, c); if (th || i === 0) td.scope = th ? "col" : "row"; tr.appendChild(td); });
  }

  function drawPanel(all, vis) {
    var p = els.panel; clear(p);
    var t = el("h2", "vv-panel-title no_anchor", state.weapon.name); p.appendChild(t);
    var meta = [state.weapon.class, CATEGORY_LABEL[state.weapon.category] || state.weapon.category].filter(Boolean).join(", ");
    p.appendChild(el("p", "sv-meta", meta));
    if (vis.note) p.appendChild(el("p", "sv-note", vis.note));
    if (state.season === "compare" && vis.s1 && vis.s2) p.appendChild(diffTable(vis.s1, vis.s2));
    else if (state.season === "compare" && all.length === 1) { /* the note says it */ }
    // readout of the inspected shot
    var h = el("h3", "sv-h3 no_anchor", "Shot " + state.inspect); p.appendChild(h);
    var tb = el("table", "sv-table"), th = el("thead"), tr0 = el("tr");
    row(tr0, ["Season", "Yaw, deg", "Pitch, deg", "Kick (yaw, pitch)"], true); th.appendChild(tr0); tb.appendChild(th);
    var body = el("tbody");
    all.forEach(function (s) {
      var i = Math.min(state.inspect, s.path.length) - 1, pt = s.path[i], f = factors(s.season, opts()), k = kickAt(s.season, i);
      var tr = el("tr");
      var name = s.key === "s1" ? "Season 1" : "Season 2";
      var cells = [name, fmt(pt.x, 3), fmt(pt.y, 3), fmt(k.x * f.x, 3) + ", " + fmt(k.y * f.y, 3) + (k.random ? " (random section, mid)" : "")];
      if (state.metres && state.dist > 0) cells[1] += " (" + fmt(targetOffset(pt.x, state.dist), 2) + " m)", cells[2] += " (" + fmt(targetOffset(pt.y, state.dist), 2) + " m)";
      row(tr, cells); tr.firstChild.className = "sv-key-" + s.key; body.appendChild(tr);
    });
    tb.appendChild(body); p.appendChild(tb);
    // facts per visible season
    all.forEach(function (s) {
      var se = s.season, f = factors(se, opts());
      var l = el("p", "sv-facts");
      l.textContent = (all.length > 1 ? (s.key === "s1" ? "Season 1: " : "Season 2: ") : "") +
        (se.rpm ? fmt(se.rpm, 0) + " RPM, " : "RPM n/a, ") + (se.pattern || []).length + " pattern shots, random-turn up to " + fmt(se.randomDeviationDeg, 1) +
        " deg, pattern restarts after " + fmt(se.recoilPatternResetTime_s, 2) + " s. Applied factors: yaw x" + fmt(f.x, 3) + ", pitch x" + fmt(f.y, 3) + ".";
      p.appendChild(l);
      if (se.sourceNote) p.appendChild(el("p", "sv-src", se.sourceNote));
    });
  }

  function diffTable(a, b) {
    var wrap = el("div", "sv-diff");
    wrap.appendChild(el("h3", "sv-h3 no_anchor", "Season 1 to Season 2"));
    var tb = el("table", "sv-table"), th = el("thead"), tr0 = el("tr");
    row(tr0, ["", "S1", "S2", "Change"], true); th.appendChild(tr0); tb.appendChild(th);
    var body = el("tbody"), n1 = Math.min(state.nShots, a.expectedPath.length), n2 = Math.min(state.nShots, b.expectedPath.length);
    var pa = scalePoints(cumulativePath(a, n1), factors(a, opts())), pb = scalePoints(cumulativePath(b, n2), factors(b, opts()));
    function add(label, x, y, unit, d) {
      var tr = el("tr"), delta = (x == null || y == null) ? "n/a" : (y - x >= 0 ? "+" : "") + fmt(y - x, d == null ? 2 : d) + (unit || "");
      row(tr, [label, x == null ? "n/a" : fmt(x, d == null ? 2 : d) + (unit || ""), y == null ? "n/a" : fmt(y, d == null ? 2 : d) + (unit || ""), delta]);
      body.appendChild(tr);
    }
    var tr = el("tr"); row(tr, ["Shots with a different kick", "", "", String(shotsChanged(a, b)) + " of " + Math.max(a.expectedPath.length, b.expectedPath.length)]); body.appendChild(tr);
    [10, 20, 30].forEach(function (n) {
      var ya = a.expectedPath.length >= n ? climbAfter(pa, n) : null, yb = b.expectedPath.length >= n ? climbAfter(pb, n) : null;
      add("Climb after " + n + " shots", ya, yb, " deg");
    });
    add("Spread width (yaw)", xExtent(pa, state.band ? scalePoints2(a.band, factors(a, opts()), n1) : null), xExtent(pb, state.band ? scalePoints2(b.band, factors(b, opts()), n2) : null), " deg");
    add("Fire rate", a.rpm, b.rpm, " RPM", 0);
    add("Pattern reset time", a.recoilPatternResetTime_s, b.recoilPatternResetTime_s, " s");
    tb.appendChild(body); wrap.appendChild(tb);
    return wrap;
  }
  function scalePoints2(band, f, n) {
    if (!band) return null;
    return { p10: scalePoints(band.p10.slice(0, n), f), p90: scalePoints(band.p90.slice(0, n), f) };
  }

  /* ---------- legend ---------- */

  function key(parent, kind, cls, text, dashed) {
    var k = el("span", "vv-key sv-legend-key");
    var s = svg("svg", { width: 34, height: 14, viewBox: "0 0 34 14", "aria-hidden": "true", class: cls }, k);
    svg("line", { x1: 2, x2: 32, y1: 7, y2: 7, class: "sv-line" + (dashed ? " is-dashed" : "") }, s);
    marker(s, kind, 17, 7, 4, "sv-dot");
    k.appendChild(el("span", null, text));
    parent.appendChild(k);
  }
  function drawLegend(vis) {
    var lg = els.legend; clear(lg);
    lg.appendChild(el("span", "vv-legend-title", "Season"));
    vis.list.forEach(function (k) {
      if (k === "s1") key(lg, "circle", "sv-s1", "Season 1 (blue, circles, dashed line)", true);
      else key(lg, "square", "sv-s2", "Season 2 (green, squares, solid line)", false);
    });
    var note = "Numbers are the shot. Hollow markers are the random section (middle of the ranges).";
    if (state.band) note += " Shaded boxes: 10th to 90th percentile of the random section.";
    if (state.fan) note += " Wedges: the random turn of each pattern kick.";
    lg.appendChild(el("span", "vv-legend-note", note));
  }

  /* ---------- overview grid ---------- */

  function drawOverview() {
    var host = els.grid; clear(host);
    var ws = state.data.weapons.filter(function (w) { return w.category === state.category; });
    var groups = {};
    ws.forEach(function (w) { (groups[w.class] = groups[w.class] || []).push(w); });
    var tiles = [];
    ws.forEach(function (w) {
      var vs = visibleSeasonsFor(w), series = vs.list.map(function (k) { var s = seriesFor(k === "s1" ? vs.s1 : vs.s2, 1e9); s.key = k; return s; });
      tiles.push({ w: w, series: series });
    });
    var shared = null;
    if (state.sameScale) {
      var all = []; tiles.forEach(function (t) { t.series.forEach(function (s) { all.push(s); }); });
      shared = { lo: 0, hi: 0, lx: 0, hx: 0 };
      all.forEach(function (s) { s.path.forEach(function (p) { shared.hi = Math.max(shared.hi, p.y); shared.lo = Math.min(shared.lo, p.y); shared.hx = Math.max(shared.hx, p.x); shared.lx = Math.min(shared.lx, p.x); }); });
    }
    var order = Object.keys(groups).sort();
    order.forEach(function (cls) {
      host.appendChild(el("h3", "sv-grid-title no_anchor", cls));
      var ul = el("ul", "sv-tiles");
      groups[cls].forEach(function (w) {
        var t = tiles.filter(function (x) { return x.w === w; })[0];
        var li = el("li", "sv-tile-li"), b = el("button", "sv-tile" + (w === state.weapon ? " is-current" : ""));
        b.type = "button"; b.setAttribute("aria-label", "Open " + w.name);
        var s0 = t.series.length ? t.series[0] : null;
        var sv = svg("svg", { viewBox: "0 0 100 110", class: "sv-svg sv-mini", "aria-hidden": "true" }, b);
        if (s0) {
          var d;
          if (shared) d = { x0: Math.min(shared.lx, -1) , x1: Math.max(shared.hx, 1), y0: shared.lo, y1: shared.hi };
          else { d = domain(t.series, false); }
          var cx = (d.x0 + d.x1) / 2; var span = Math.max(d.y1 - d.y0, (d.x1 - d.x0) * 1.1) * 1.08 || 1;
          var scl = 96 / span, ox = 50 - scl * cx;
          var X = function (x) { return ox + scl * x; }, Y = function (y) { return 104 - scl * (y - d.y0) ; };
          t.series.forEach(function (s) {
            var grp = svg("g", { class: "sv-" + s.key }, sv);
            svg("polyline", { points: [{ x: 0, y: 0 }].concat(s.path).map(function (p) { return X(p.x).toFixed(1) + "," + Y(p.y).toFixed(1); }).join(" "), class: "sv-line" + (s.key === "s1" ? " is-dashed" : "") }, grp);
            var last = s.path[s.path.length - 1];
            if (last) marker(grp, s.key === "s1" ? "circle" : "square", X(last.x), Y(last.y), 2.2, "sv-dot");
          });
          svg("circle", { cx: X(0), cy: Y(0), r: 1.8, class: "sv-origin" }, sv);
        }
        li.appendChild(b);
        b.appendChild(el("span", "sv-tile-name", w.name));
        b.addEventListener("click", function () { selectWeapon(w.id, true); });
        ul.appendChild(li);
      });
      host.appendChild(ul);
    });
  }
  function visibleSeasonsFor(w) { return visibleSeasons(w); }

  /* ---------- wiring ---------- */

  function render(skipOverview) {
    if (!state.weapon) return;
    var vis = visibleSeasons(state.weapon);
    var maxN = Math.max.apply(null, vis.list.map(function (k) { return (k === "s1" ? vis.s1 : vis.s2).expectedPath.length; }).concat([1]));
    els.shots.max = String(maxN); els.shots.min = "1";
    if (state.nShots > maxN) state.nShots = maxN;
    els.shots.value = String(state.nShots);
    els.shotsOut.textContent = String(state.nShots);
    if (state.inspect > state.nShots) state.inspect = state.nShots;
    els.inspect.max = String(state.nShots); els.inspect.value = String(state.inspect);
    var all = drawPlot();
    drawTimeline(all); drawPanel(all, vis); drawLegend(vis);
    // season buttons: say when a season has nothing for this weapon
    Array.prototype.forEach.call(els.season.querySelectorAll("button"), function (b) {
      var on = b.value === state.season; b.setAttribute("aria-checked", on ? "true" : "false"); b.tabIndex = on ? 0 : -1;
    });
    Array.prototype.forEach.call(els.stance.querySelectorAll("button"), function (b) {
      var on = b.value === state.stance; b.setAttribute("aria-checked", on ? "true" : "false"); b.tabIndex = on ? 0 : -1;
    });
    els.dist.disabled = !state.metres;
    if (!skipOverview) drawOverview();
  }

  function fillWeapons() {
    var sel = els.weapon, cur = state.weapon && state.weapon.id;
    clear(sel);
    var ws = state.data.weapons.filter(function (w) { return w.category === state.category; });
    var by = {}; ws.forEach(function (w) { (by[w.class] = by[w.class] || []).push(w); });
    Object.keys(by).sort().forEach(function (c) {
      var og = document.createElement("optgroup"); og.label = c;
      by[c].sort(function (a, b) { return a.name.localeCompare(b.name); }).forEach(function (w) {
        var o = el("option", null, w.name); o.value = w.id; og.appendChild(o);
      });
      sel.appendChild(og);
    });
    sel.disabled = !ws.length;
    var keep = ws.filter(function (w) { return w.id === cur; })[0] || ws[0];
    if (keep) { sel.value = keep.id; state.weapon = keep; }
  }

  function selectWeapon(id, scroll) {
    var w = state.data.weapons.filter(function (x) { return x.id === id; })[0];
    if (!w) return;
    state.weapon = w; els.weapon.value = id; state.inspect = 1;
    state.nShots = 1e9;
    render();
    if (scroll && els.stage.scrollIntoView) els.stage.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  function radioGroup(group, onPick) {
    var btns = Array.prototype.slice.call(group.querySelectorAll("button"));
    btns.forEach(function (b, i) {
      b.addEventListener("click", function () { onPick(b.value); });
      b.addEventListener("keydown", function (e) {
        var j = e.key === "ArrowRight" || e.key === "ArrowDown" ? i + 1 : e.key === "ArrowLeft" || e.key === "ArrowUp" ? i - 1 : null;
        if (j == null) return;
        e.preventDefault();
        var t = btns[(j + btns.length) % btns.length]; t.focus(); onPick(t.value);
      });
    });
  }

  function init(data) {
    state.data = data;
    state.data.weapons.forEach(function (w) { w.category = w.category || "infantry"; });
    var cats = Array.from(new Set(data.weapons.map(function (w) { return w.category; })));
    clear(els.category);
    cats.sort(function (a, b) { return a === "infantry" ? -1 : b === "infantry" ? 1 : a.localeCompare(b); }).forEach(function (c) {
      var o = el("option", null, CATEGORY_LABEL[c] || c); o.value = c; els.category.appendChild(o);
    });
    state.category = cats.indexOf("infantry") >= 0 ? "infantry" : cats[0];
    els.category.value = state.category; els.category.disabled = false;
    if (data.meta && data.meta.PROVISIONAL) {
      els.prov.hidden = false;
    }
    fillWeapons();
    state.nShots = 1e9;
    els.weapon.addEventListener("change", function () { selectWeapon(els.weapon.value); });
    els.category.addEventListener("change", function () { state.category = els.category.value; state.weapon = null; fillWeapons(); state.nShots = 1e9; state.inspect = 1; render(); });
    radioGroup(els.season, function (v) { state.season = v; state.nShots = 1e9; render(); });
    radioGroup(els.stance, function (v) { state.stance = v; render(); });
    [["focus", "focus"], ["attachments", "attachments"], ["fan", "fan"], ["band", "band"], ["metres", "metres"], ["sameScale", "sameScale"]].forEach(function (p) {
      els["c_" + p[0]].addEventListener("change", function () { state[p[1]] = this.checked; render(); });
    });
    els.dist.addEventListener("input", function () { var v = parseFloat(this.value); if (v > 0) { state.dist = v; render(); } });
    els.shots.addEventListener("input", function () { state.nShots = parseInt(this.value, 10); render(); });
    els.inspect.addEventListener("input", function () { state.inspect = parseInt(this.value, 10); render(true); });
    els.plot.addEventListener("keydown", function (e) {
      var d = e.key === "ArrowRight" || e.key === "ArrowUp" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowDown" ? -1 : 0;
      if (e.key === "Home") d = -1e9; else if (e.key === "End") d = 1e9;
      if (!d) return;
      e.preventDefault();
      state.inspect = Math.max(1, Math.min(state.nShots, state.inspect + d)); render(true);
      var s = els.plot.querySelector("svg"); if (s) s.focus();
    });
    els.plot.addEventListener("mousemove", function (e) {
      if (!els.scale || !els.shown || !els.shown.length || !els.svg) return;
      var r = els.svg.getBoundingClientRect(), k = VW / r.width, mx = (e.clientX - r.left) * k, my = (e.clientY - r.top) * k, best = 0, bd = Infinity;
      els.shown[els.shown.length - 1].path.forEach(function (p, i) {
        var dx = els.scale.X(p.x) - mx, dy = els.scale.Y(p.y) - my, dd = dx * dx + dy * dy;
        if (dd < bd) { bd = dd; best = i; }
      });
      if (best + 1 !== state.inspect && bd < 40 * 40) { state.inspect = best + 1; render(true); }
    });
    els.status.textContent = "";
    ["weapon", "category"].forEach(function (k) { els[k].disabled = false; });
    render();
  }

  function boot() {
    ["weapon", "category", "season", "stance", "plot", "timeline", "panel", "legend", "grid", "shots", "shotsOut", "inspect", "dist", "status", "stage", "prov"].forEach(function (k) {
      els[k] = document.getElementById("sv-" + (k === "shotsOut" ? "shots-out" : k));
    });
    ["focus", "attachments", "fan", "band", "metres", "sameScale"].forEach(function (k) { els["c_" + k] = document.getElementById("sv-c-" + k); });
    els.status.textContent = "Loading weapons…";
    fetch(root.getAttribute("data-json")).then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(init)
      .catch(function (e) { els.status.textContent = "Could not load the spray data (" + e.message + ")."; });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
