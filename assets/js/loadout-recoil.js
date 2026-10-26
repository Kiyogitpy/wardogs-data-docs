/* Recoil panel of the Loadout Builder (styles in _sass/custom/loadout-recoil.scss).
   window.WDRecoil.mount(el, sprayJson) -> panel; panel.update({ itemAsset, vertical, horizontal, stance, focus, magazine? }).
   Model (round 81, docs/evidence/round81-view-kick-curve.md): per shot v = Rot(theta) * P[i] * (H, V) * focusCut * ViewKickMagnitudeMultiplier,
   theta uniform in +-RandomDeviationDegree; past the pattern a uniform draw from the post-pattern ranges (path: their mean);
   no recovery on firearms; not scaled by field of view or sensitivity.
   vertical / horizontal are the evaluator's FINAL Vertical/HorizontalRecoilMultiplier. They already contain the stance effect and the
   attachments, so neither the data's stance ratios nor its default-loadout multipliers are applied here; stance is only a label.
   Pure functions (WDRecoilCore) are exported for _tools/loadout_recoil_check.js. Strings from the data are set as text only. */
(function () {
  "use strict";

  /* ---------- pure model ---------- */

  var SV = (typeof globalThis !== "undefined" && globalThis.SprayViewerCore) || null;
  if (!SV && typeof require !== "undefined") { try { SV = require("./spray-viewer.js"); } catch (e) { SV = null; } }

  function kickAt(season, i) {
    if (SV && SV.kickAt) return SV.kickAt(season, i);
    var p = season.pattern || [];
    if (i < p.length) return { x: p[i].x, y: p[i].y, random: false };
    var pp = season.postPattern || { yaw: [0, 0], pitch: [0, 0] };
    return { x: (pp.yaw[0] + pp.yaw[1]) / 2, y: (pp.pitch[0] + pp.pitch[1]) / 2, random: true };
  }
  function niceStep(span, target) {
    if (SV && SV.niceStep) return SV.niceStep(span, target);
    var raw = span / target, mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), r = raw / mag;
    return (r < 1.5 ? 1 : r < 3.5 ? 2 : r < 7.5 ? 5 : 10) * mag;
  }
  function num(v, d) { return typeof v === "number" && isFinite(v) ? v : d; }

  // Scale applied to the data's authored kick: loadout multipliers (final, stance included), focus cut, view kick magnitude.
  function scaleOf(season, o) {
    var f = num(season.viewKickMagnitudeMultiplier, 1);
    if (o.focus) f *= 1 - num(season.focusReductionPct, 0) / 100;
    return { x: f * num(o.horizontal, 1), y: f * num(o.vertical, 1) };
  }

  // Expected running sum of the scaled kicks, shot 1 first (no recovery).
  function path(season, o, n) {
    var s = scaleOf(season, o), out = [], cx = 0, cy = 0;
    for (var i = 0; i < n; i++) {
      var k = kickAt(season, i);
      cx += k.x * s.x; cy += k.y * s.y;
      out.push({ shot: i + 1, x: cx, y: cy });
    }
    return out;
  }

  // The data's Monte Carlo p10/p90 of the cumulative path (unscaled), scaled for this loadout.
  function band(season, o, n) {
    if (!season.band || !season.band.p10) return null;
    var s = scaleOf(season, o);
    function sc(a) { return a.slice(0, n).map(function (p) { return { shot: p.shot, x: p.x * s.x, y: p.y * s.y }; }); }
    return { p10: sc(season.band.p10), p90: sc(season.band.p90) };
  }

  // One random run: theta uniform in +-deviation per pattern kick, uniform post-pattern draws afterwards.
  function sample(season, o, n, rnd) {
    rnd = rnd || Math.random;
    var s = scaleOf(season, o), dev = num(season.randomDeviationDeg, 0) * Math.PI / 180, pl = (season.pattern || []).length;
    var pp = season.postPattern || { yaw: [0, 0], pitch: [0, 0] }, out = [], cx = 0, cy = 0;
    for (var i = 0; i < n; i++) {
      var kx, ky;
      if (i < pl) {
        var t = (rnd() * 2 - 1) * dev, c = Math.cos(t), sn = Math.sin(t), p = season.pattern[i];
        kx = p.x * c - p.y * sn; ky = p.x * sn + p.y * c;
      } else {
        kx = pp.yaw[0] + rnd() * (pp.yaw[1] - pp.yaw[0]); ky = pp.pitch[0] + rnd() * (pp.pitch[1] - pp.pitch[0]);
      }
      cx += kx * s.x; cy += ky * s.y;
      out.push({ shot: i + 1, x: cx, y: cy });
    }
    return out;
  }

  function offsetM(deg, distM) { return distM * Math.tan(deg * Math.PI / 180); }

  function findSeason(spray, itemAsset) {
    var ws = (spray && spray.weapons) || [];
    for (var i = 0; i < ws.length; i++) {
      if (ws[i].itemAsset === itemAsset) {
        var s = ws[i].seasons && ws[i].seasons.s2;
        return s && s.present !== false ? { weapon: ws[i], season: s } : null;
      }
    }
    return null;
  }

  function fmt(v, d) {
    if (v == null || !isFinite(v)) return "n/a";
    var dd = d == null ? 2 : d, t = Math.abs(v) < Math.pow(10, -dd) / 2 ? 0 : v;
    return t.toFixed(dd);
  }
  function fmtLen(m) { // metres to a readable length
    var a = Math.abs(m);
    if (a >= 100) return fmt(m, 0) + " m";
    if (a >= 10) return fmt(m, 1) + " m";
    if (a >= 1) return fmt(m, 2) + " m";
    return fmt(m * 100, 0) + " cm";
  }

  var core = { kickAt: kickAt, scaleOf: scaleOf, path: path, band: band, sample: sample, offsetM: offsetM, findSeason: findSeason, niceStep: niceStep, fmt: fmt, fmtLen: fmtLen };
  var api = {};
  if (typeof module !== "undefined" && module.exports) module.exports = core;
  if (typeof globalThis !== "undefined") globalThis.WDRecoilCore = core;
  if (typeof document === "undefined") return;

  /* ---------- view ---------- */

  var NS = "http://www.w3.org/2000/svg", AIM_H = 1.4, PERSON_H = 1.8, MAXSHOTS = 40;
  function el(tag, cls, text, parent) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function svg(tag, attrs, parent, text) {
    var e = document.createElementNS(NS, tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function clear(n) { while (n.firstChild) n.removeChild(n.firstChild); }
  function reduced() { try { return window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) { return false; } }
  function pt(sc, p) { return sc.X(p.x).toFixed(1) + "," + sc.Y(p.y).toFixed(1); }

  function mount(host, spray) {
    var st = { spray: spray, in: null, found: null, shots: 30, dist: 50, run: null, timer: null };
    clear(host);
    host.classList.add("wdr");
    var head = el("div", "wdr-head", null, host);
    el("h3", "wdr-title", "Recoil", head);
    var sub = el("p", "wdr-sub", "", head);
    var empty = el("p", "wdr-empty", "", host);
    empty.hidden = true;
    var body = el("div", "wdr-body", null, host);
    body.hidden = true;

    var ctr = el("div", "wdr-controls", null, body);
    var fire = el("button", "wdr-fire", "Fire", ctr);
    fire.type = "button";
    function slider(label, min, max, step) {
      var w = el("label", "wdr-field", null, ctr), t = el("span", "wdr-label", label + " ", w);
      var out = el("output", "wdr-out", "", t), r = el("input", null, null, w);
      r.type = "range"; r.min = min; r.max = max; r.step = step;
      return { r: r, out: out };
    }
    var sShots = slider("Shots fired", 1, MAXSHOTS, 1), sDist = slider("Target distance", 5, 300, 5);
    sShots.r.value = st.shots; sDist.r.value = st.dist;

    var figs = el("div", "wdr-figs", null, body);
    var fa = el("figure", "wdr-fig wdr-fig-plot", null, figs), fb = el("figure", "wdr-fig wdr-fig-target", null, figs);
    el("figcaption", null, "Cumulative view offset", fa);
    var plot = el("div", "wdr-plot", null, fa);
    var cap2 = el("figcaption", null, "", fb), targ = el("div", "wdr-target", null, fb);
    var live = el("p", "wdr-live", "", body);
    live.setAttribute("role", "status");
    var dl = el("dl", "wdr-summary", null, body);
    function stat(label) { var d = el("div", "wdr-stat", null, dl); el("dt", null, label, d); return el("dd", null, "", d); }
    var vClimb = stat("Climb"), vDrift = stat("Drift"), vDev = stat("Deviation"), vReset = stat("Pattern reset");
    var note = el("p", "wdr-note", "", body);

    function render() {
      var f = st.found, o = st.in;
      if (!o) { body.hidden = true; return; }
      if (!f) {
        empty.textContent = "No recoil data for this weapon.";
        empty.hidden = false; body.hidden = true; sub.textContent = ""; stopFire(); return;
      }
      empty.hidden = true; body.hidden = false;
      var season = f.season, n = st.shots;
      var c = { season: season, p: path(season, o, MAXSHOTS), b: band(season, o, MAXSHOTS) };
      var stance = o.stance || "Stand";
      sub.textContent = f.weapon.name + " | " + stance.toLowerCase() + (o.focus ? ", focused" : "") +
        " | vertical x" + fmt(num(o.vertical, 1), 2) + ", horizontal x" + fmt(num(o.horizontal, 1), 2);
      sShots.out.textContent = n; sDist.out.textContent = st.dist + " m";
      sShots.r.value = n; sDist.r.value = st.dist;

      var shown = st.run ? Math.min(st.run.shown, n) : n;
      var last = c.p[n - 1], sd = st.dist;
      drawPlot(c, n, shown);
      drawTarget(c, n, shown);
      vClimb.textContent = fmt(last.y, 2) + "° pitch";
      vDrift.textContent = fmt(last.x, 2) + "° yaw";
      vDev.textContent = "±" + fmt(num(season.randomDeviationDeg, 0), 1) + "° per shot";
      vReset.textContent = season.recoilPatternResetTime_s == null ? "n/a" : fmt(season.recoilPatternResetTime_s, 2) + " s";
      live.textContent = n + " shots: the view climbs " + fmt(last.y, 2) + " degrees and drifts " + fmt(last.x, 2) +
        " degrees; at " + sd + " m that is " + fmtLen(offsetM(last.y, sd)) + " up and " + fmtLen(offsetM(last.x, sd)) + " sideways.";
      cap2.textContent = "On a target " + sd + " m away";
      note.textContent = "Expected path (mean of the random section); the band is the 10th to 90th percentile of 2000 simulated magazines. " +
        "Multipliers are the loadout's final values (stance and attachments included). No recovery between shots; independent of field of view and sensitivity.";
    }

    /* degrees plot */
    var PW = 330, PH = 420, PM = { l: 44, r: 10, t: 12, b: 34 };
    function drawPlot(c, n, shown) {
      clear(plot);
      var root = svg("svg", { viewBox: "0 0 " + PW + " " + PH, class: "wdr-svg", role: "img", focusable: "false" }, plot);
      var xs = [0], ys = [0];
      c.p.forEach(function (p) { xs.push(p.x); ys.push(p.y); });
      if (c.b) c.b.p10.concat(c.b.p90).forEach(function (p) { xs.push(p.x); ys.push(p.y); });
      var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
      var spanY = (y1 - y0) || 1;
      if (x1 - x0 < spanY * 0.35) { var mid = (x0 + x1) / 2; x0 = mid - spanY * 0.175; x1 = mid + spanY * 0.175; }
      var px = (x1 - x0) * 0.06, py = spanY * 0.05; x0 -= px; x1 += px; y0 -= py; y1 += py;
      var w = PW - PM.l - PM.r, h = PH - PM.t - PM.b, s = Math.min(w / (x1 - x0), h / (y1 - y0));
      var cx = PM.l + w / 2 - s * (x0 + x1) / 2, cy = PM.t + h / 2 + s * (y0 + y1) / 2;
      var sc = { X: function (x) { return cx + s * x; }, Y: function (y) { return cy - s * y; } };
      var L = sc.X(x0), R = sc.X(x1), T = sc.Y(y1), B = sc.Y(y0), step = niceStep(Math.max(x1 - x0, y1 - y0), 7), v, t;
      var g = svg("g", null, root);
      var dec = step < 0.1 ? 2 : step < 1 ? 1 : 0;
      for (v = Math.ceil(x0 / step) * step; v <= x1 + 1e-9; v += step) {
        t = Math.round(v / step) * step;
        svg("line", { x1: sc.X(t), x2: sc.X(t), y1: T, y2: B, class: Math.abs(t) < 1e-9 ? "wdr-zero" : "wdr-grid" }, g);
        svg("text", { x: sc.X(t), y: B + 14, class: "wdr-tick", "text-anchor": "middle" }, g, fmt(t, dec));
      }
      for (v = Math.ceil(y0 / step) * step; v <= y1 + 1e-9; v += step) {
        t = Math.round(v / step) * step;
        svg("line", { x1: L, x2: R, y1: sc.Y(t), y2: sc.Y(t), class: Math.abs(t) < 1e-9 ? "wdr-zero" : "wdr-grid" }, g);
        svg("text", { x: L - 5, y: sc.Y(t) + 4, class: "wdr-tick", "text-anchor": "end" }, g, fmt(t, dec));
      }
      svg("text", { x: (L + R) / 2, y: PH - 4, class: "wdr-axis", "text-anchor": "middle" }, g, "Yaw, degrees (right +)");
      svg("text", { x: 11, y: (T + B) / 2, class: "wdr-axis", "text-anchor": "middle", transform: "rotate(-90 11 " + (T + B) / 2 + ")" }, g, "Pitch, degrees (up +)");
      svg("rect", { x: L, y: T, width: R - L, height: B - T, class: "wdr-frame" }, g);
      var i;
      if (c.b) for (i = 0; i < n; i++) {
        var a = c.b.p10[i], b = c.b.p90[i];
        svg("rect", { x: Math.min(sc.X(a.x), sc.X(b.x)), y: Math.min(sc.Y(a.y), sc.Y(b.y)), width: Math.max(1.5, Math.abs(sc.X(b.x) - sc.X(a.x))),
          height: Math.max(1.5, Math.abs(sc.Y(a.y) - sc.Y(b.y))), class: "wdr-band" }, g);
      }
      var pts = [{ x: 0, y: 0 }].concat(c.p.slice(0, n));
      svg("polyline", { points: pts.map(function (p) { return pt(sc, p); }).join(" "), class: "wdr-line" }, g);
      var pl = (c.season.pattern || []).length;
      c.p.slice(0, n).forEach(function (p, j) {
        var k = j + 1;
        svg("circle", { cx: sc.X(p.x), cy: sc.Y(p.y), r: k === n ? 3.5 : 2.4, class: "wdr-dot" + (j >= pl ? " is-random" : "") }, g);
        if (k % 10 === 0) svg("text", { x: sc.X(p.x) + 6, y: sc.Y(p.y) + 3, class: "wdr-num" }, g, k);
      });
      if (st.run) {
        var rp = st.run.pts.slice(0, shown);
        if (rp.length) {
          svg("polyline", { points: [{ x: 0, y: 0 }].concat(rp).map(function (p) { return pt(sc, p); }).join(" "), class: "wdr-run" }, g);
          var q = rp[rp.length - 1];
          svg("circle", { cx: sc.X(q.x), cy: sc.Y(q.y), r: 4.5, class: "wdr-run-dot" }, g);
        }
      }
      var o = svg("g", { class: "wdr-aim" }, g);
      svg("circle", { cx: sc.X(0), cy: sc.Y(0), r: 5, class: "wdr-aim-c" }, o);
      svg("line", { x1: sc.X(0) - 8, x2: sc.X(0) + 8, y1: sc.Y(0), y2: sc.Y(0), class: "wdr-aim-l" }, o);
      svg("line", { x1: sc.X(0), x2: sc.X(0), y1: sc.Y(0) - 8, y2: sc.Y(0) + 8, class: "wdr-aim-l" }, o);
      root.setAttribute("aria-label", "Spray plot: view offset in degrees for " + n + " shots, ending " + fmt(c.p[n - 1].y, 2) + " degrees up and " + fmt(c.p[n - 1].x, 2) + " degrees sideways.");
    }

    /* target at distance, metres, person drawn to scale */
    var TW = 300, TH = 420, TM = { l: 40, r: 8, t: 12, b: 24 };
    function drawTarget(c, n, shown) {
      clear(targ);
      var root = svg("svg", { viewBox: "0 0 " + TW + " " + TH, class: "wdr-svg", role: "img", focusable: "false" }, targ), d = st.dist;
      var X = [0], Y = [AIM_H], i;
      for (i = 0; i < n; i++) { X.push(offsetM(c.p[i].x, d)); Y.push(AIM_H + offsetM(c.p[i].y, d)); }
      if (c.b) for (i = 0; i < n; i++) [c.b.p10[i], c.b.p90[i]].forEach(function (p) { X.push(offsetM(p.x, d)); Y.push(AIM_H + offsetM(p.y, d)); });
      var xh = Math.max(0.6, Math.max.apply(null, X.map(Math.abs)) * 1.1);
      var y0 = Math.min(0, Math.min.apply(null, Y)) - 0.1, y1 = Math.max(PERSON_H + 0.15, Math.max.apply(null, Y)) + 0.1;
      var w = TW - TM.l - TM.r, h = TH - TM.t - TM.b, s = Math.min(w / (2 * xh), h / (y1 - y0));
      var ox = TM.l + w / 2, base = TM.t + h / 2 + s * (y0 + y1) / 2;
      function PX(m) { return ox + s * m; }
      function PY(m) { return base - s * m; }
      var g = svg("g", null, root), step = niceStep(y1 - y0, 6), v;
      for (v = Math.ceil(y0 / step) * step; v <= y1 + 1e-9; v += step) {
        var tv = Math.round(v / step) * step;
        svg("line", { x1: TM.l, x2: TW - TM.r, y1: PY(tv), y2: PY(tv), class: Math.abs(tv) < 1e-9 ? "wdr-ground" : "wdr-grid" }, g);
        svg("text", { x: TM.l - 5, y: PY(tv) + 4, class: "wdr-tick", "text-anchor": "end" }, g, fmt(tv, step < 1 ? 1 : 0));
      }
      svg("text", { x: 11, y: TM.t + h / 2, class: "wdr-axis", "text-anchor": "middle", transform: "rotate(-90 11 " + (TM.t + h / 2) + ")" }, g, "Height above ground, m");
      // standing player, 1.8 m, drawn to scale
      var p = svg("g", { class: "wdr-person" }, g);
      svg("rect", { x: PX(-0.2), y: PY(0.85), width: s * 0.17, height: s * 0.85, rx: 1 }, p);
      svg("rect", { x: PX(0.03), y: PY(0.85), width: s * 0.17, height: s * 0.85, rx: 1 }, p);
      svg("rect", { x: PX(-0.23), y: PY(1.5), width: s * 0.46, height: s * 0.7, rx: 2 }, p);
      svg("rect", { x: PX(-0.33), y: PY(1.48), width: s * 0.1, height: s * 0.6, rx: 2 }, p);
      svg("rect", { x: PX(0.23), y: PY(1.48), width: s * 0.1, height: s * 0.6, rx: 2 }, p);
      svg("circle", { cx: PX(0), cy: PY(PERSON_H - 0.11), r: s * 0.11 }, p);
      svg("text", { x: PX(0.42), y: PY(PERSON_H) + 4, class: "wdr-tick" }, g, "1.8 m");
      if (c.b) for (i = 0; i < n; i++) {
        var a = c.b.p10[i], b = c.b.p90[i], ax = PX(offsetM(a.x, d)), bx = PX(offsetM(b.x, d)), ay = PY(AIM_H + offsetM(a.y, d)), by = PY(AIM_H + offsetM(b.y, d));
        svg("rect", { x: Math.min(ax, bx), y: Math.min(ay, by), width: Math.max(1.5, Math.abs(bx - ax)), height: Math.max(1.5, Math.abs(ay - by)), class: "wdr-band" }, g);
      }
      var pts = [{ x: 0, y: AIM_H }].concat(c.p.slice(0, n).map(function (q) { return { x: offsetM(q.x, d), y: AIM_H + offsetM(q.y, d) }; }));
      svg("polyline", { points: pts.map(function (q) { return PX(q.x).toFixed(1) + "," + PY(q.y).toFixed(1); }).join(" "), class: "wdr-line" }, g);
      var pl = (c.season.pattern || []).length;
      pts.slice(1).forEach(function (q, k) { svg("circle", { cx: PX(q.x), cy: PY(q.y), r: k + 1 === n ? 3.2 : 2, class: "wdr-dot" + (k >= pl ? " is-random" : "") }, g); });
      if (st.run) {
        var rp = st.run.pts.slice(0, shown).map(function (q) { return { x: offsetM(q.x, d), y: AIM_H + offsetM(q.y, d) }; });
        if (rp.length) {
          svg("polyline", { points: [{ x: 0, y: AIM_H }].concat(rp).map(function (q) { return PX(q.x).toFixed(1) + "," + PY(q.y).toFixed(1); }).join(" "), class: "wdr-run" }, g);
          svg("circle", { cx: PX(rp[rp.length - 1].x), cy: PY(rp[rp.length - 1].y), r: 4, class: "wdr-run-dot" }, g);
        }
      }
      svg("circle", { cx: PX(0), cy: PY(AIM_H), r: 4.5, class: "wdr-aim-c" }, g);
      svg("text", { x: PX(0) + 8, y: PY(AIM_H) + 14, class: "wdr-tick" }, g, "aim, 1.4 m");
      var last = c.p[n - 1];
      root.setAttribute("aria-label", "Spray on a target " + d + " metres away, next to a 1.8 metre player: " + fmtLen(offsetM(last.y, d)) + " up and " + fmtLen(offsetM(last.x, d)) + " sideways after " + n + " shots.");
    }

    /* fire animation: one random magazine, shot by shot at the weapon's rate of fire */
    function stopFire(keep) {
      if (st.timer) { clearTimeout(st.timer); st.timer = null; }
      if (!keep) st.run = null;
      fire.textContent = "Fire"; fire.classList.remove("is-on");
    }
    function startFire() {
      var f = st.found; if (!f) return;
      stopFire();
      var n = st.shots, rpm = num(f.season.rpm, 600), gap = Math.max(30, 60000 / rpm);
      st.run = { pts: sample(f.season, st.in, n), shown: 0 };
      if (reduced()) { st.run.shown = n; fire.textContent = "Fire again"; render(); return; }
      fire.textContent = "Stop"; fire.classList.add("is-on");
      (function tick() {
        st.run.shown++;
        render();
        if (st.run.shown >= n) { st.timer = null; fire.textContent = "Fire again"; fire.classList.remove("is-on"); return; }
        st.timer = setTimeout(tick, gap);
      })();
    }
    fire.addEventListener("click", function () {
      if (st.timer) { stopFire(true); fire.textContent = "Fire again"; render(); } else startFire();
    });
    sShots.r.addEventListener("input", function () { st.shots = +sShots.r.value; stopFire(); render(); });
    sDist.r.addEventListener("input", function () { st.dist = +sDist.r.value; render(); });

    return {
      update: function (o) {
        if (!o) return;
        var prev = st.in && st.in.itemAsset;
        st.in = { itemAsset: o.itemAsset, vertical: o.vertical, horizontal: o.horizontal, stance: o.stance, focus: !!o.focus };
        st.found = findSeason(st.spray, o.itemAsset);
        if (o.magazine != null && o.itemAsset !== prev) st.shots = Math.max(1, Math.min(MAXSHOTS, o.magazine | 0));
        if (o.itemAsset !== prev) stopFire(); else { if (st.timer) clearTimeout(st.timer); st.timer = null; st.run = null; fire.textContent = "Fire"; fire.classList.remove("is-on"); }
        render();
      },
      destroy: function () { stopFire(); clear(host); }
    };
  }

  api.mount = mount;
  api.core = core;
  if (typeof globalThis !== "undefined") globalThis.WDRecoil = api;
})();
