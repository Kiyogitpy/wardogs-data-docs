/* Vehicle hitbox viewer (vehicle-viewer.md; styles in _sass/custom/vehicle-viewer.scss).
   Data: assets/data/vehicle-hitboxes.json (python _tools/damage_tables.py --json).
   - each vehicle's collision mesh is a GLB with one material per collision slot, named as the
     slot ("CC_FuelTank"), or "<slot>|<Group>" outside the Default surface group ("CC_Main|Radar");
   - a material resolves to a slot entry as the game does (resolve below): (group, slot), else the
     group's "(default)", else the parent group's, else no section (painted grey, clickable);
   - slots are coloured by section family, hits to destroy (log scale) or rule factor; a click on
     the model, a label or the slot list selects a slot and the side panel explains it;
   - without WebGL, model-viewer or an exported model, the selected vehicle's hitbox table is
     shown instead. With JavaScript off the page shows the static table under .vv-nojs. */
(function () {
  "use strict";

  // The GLBs are meshopt-compressed. model-viewer loads this script, then decodes with its own
  // bundled decoder; the file is meshoptimizer 1.2.0's UMD build (meshopt_decoder.cjs), vendored
  // because a CDN copy can't carry SRI on that dynamic load (and jsDelivr serves .cjs as
  // application/node, which browsers refuse to run). Site-relative, under base.
  var MESHOPT = "assets/js/vendor/meshopt_decoder-1.2.0.js";
  var MV_TIMEOUT = 15000;            // ms to wait for <model-viewer> to be defined
  var DEFAULT_GROUP = "ComplexSurface.Group.Default";
  var GROUP = "ComplexSurface.Group.";
  var ROW = "Meta.Damage.Vehicle.";
  var PILOT = "air-rotary-havoc";

  // Section families: the dataviz reference palette's dark categorical steps, assigned so the
  // families that share a vehicle stay apart (validated against the panel surface #18181c).
  // Body areas and the main health stay neutral: no further hue clears every vehicle's pairs.
  var FAMILIES = [
    { key: "FuelTank", label: "Fuel tank", colour: "#c98500" },
    { key: "Engine", label: "Engine", colour: "#d55181" },
    { key: "Rotor", label: "Rotors", colour: "#008300" },
    { key: "Wheel", label: "Wheels", colour: "#3987e5" },
    { key: "Tracks", label: "Tracks", colour: "#9085e9" },
    { key: "Radar", label: "Radar", colour: "#199e70" },
    { key: "Body", label: "Body areas", colour: "#a9a9b2" }
  ];
  var MAIN = { key: "Main", label: "Main health", colour: "#6c6c75" };
  var NONE_COLOUR = "#3b3b42";       // "can't destroy" (hatched in the legend and list)
  // Sequential blue, dark mode: step 600 (dimmest allowed on dark) up to step 100.
  var RAMP = ["#184f95", "#1c5cab", "#256abf", "#2a78d6", "#3987e5", "#5598e7",
              "#6da7ec", "#86b6ef", "#9ec5f4", "#b7d3f6", "#cde2fb"];
  var HIGHLIGHT = "#5a5a5a";         // emissive added to the selected slot's materials
  var GHOST = 0.13;                  // alpha of the other slots while one is selected (see-through)

  var root, data, mainSection, base, els = {};
  var state = { vehicle: null, model: -1, caliber: null, blast: true, dist: 0, mode: "section", selected: -1, picked: null, labels: true, xray: true,
                wheels: "intact" };
  var viewer = null, mvState = "pending", materials = [], loadToken = 0, fallbackText = null;

  function $(id) { return document.getElementById(id); }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  /* ---------- formatting ---------- */

  function shortSection(tag) {
    if (!tag) return "?";
    return tag === mainSection ? "Main health" : tag.replace(mainSection + ".", "");
  }

  function shortGroup(group) { return (group || DEFAULT_GROUP).replace(GROUP, ""); }

  function slotName(s) { return s.slot === "(default)" ? "(default)" : s.slot; }

  function num(x) {
    if (x == null) return "?";
    var a = Math.abs(x);
    var s = a >= 100 ? x.toFixed(0) : a >= 10 ? x.toFixed(1) : a >= 1 ? x.toFixed(2) : x.toPrecision(3);
    s = s.indexOf(".") >= 0 ? s.replace(/0+$/, "").replace(/\.$/, "") : s;
    return Number(s).toLocaleString("en-US", { maximumFractionDigits: 4 });
  }

  function pct(scalar) { return num(scalar * 100) + "%"; }

  function familyOf(section) {
    if (!section || section === mainSection) return MAIN;
    var head = section.replace(mainSection + ".", "").split(".")[0];
    for (var i = 0; i < FAMILIES.length; i++) if (FAMILIES[i].key === head) return FAMILIES[i];
    return MAIN;
  }

  function vehicleLabel(v) {
    return v.damage_row.replace(ROW, "") + " (" + v.variants.join(", ") + ")";
  }

  // vehicles[].models: one GLB per distinct variant geometry, its slot centres aligned with
  // vehicles[].slots. An older file (vehicles[].model, slots[].centre) reads as one model.
  function normalise(v) {
    if (Array.isArray(v.models)) return;
    v.models = v.model ? [{ variants: v.variants, path: v.model,
                            centres: v.slots.map(function (s) { return s.centre || null; }) }] : [];
  }

  // models[].wheels_destroyed: the same model with every wheel destroyed (damage state 2), shown by the
  // Wheels control; same variants and slots, its own GLB, centres and notes.
  function currentModel() {
    var v = state.vehicle, m = v && state.model >= 0 ? v.models[state.model] || null : null;
    return m && state.wheels === "destroyed" && m.wheels_destroyed ? m.wheels_destroyed : m;
  }

  function modelLabel(m) { return m.variants.join(", "); }

  /* ---------- colour scales ---------- */

  function hexToRgb(h) { return [1, 3, 5].map(function (i) { return parseInt(h.substr(i, 2), 16); }); }
  function rgbToHex(c) { return "#" + c.map(function (x) { return ("0" + Math.round(x).toString(16)).slice(-2); }).join(""); }

  function ramp(t) {
    t = Math.max(0, Math.min(1, t)) * (RAMP.length - 1);
    var i = Math.min(Math.floor(t), RAMP.length - 2), f = t - i;
    var a = hexToRgb(RAMP[i]), b = hexToRgb(RAMP[i + 1]);
    return rgbToHex(a.map(function (x, k) { return x + (b[k] - x) * f; }));
  }

  /* ---------- blast falloff (Damage pipeline §1.1: 0x6F06540) ---------- */

  // Radial amount at distance d (cm): Base inside E, 0 at R and beyond, else Base * ((1 - F) + F * t) with t = 1 at E
  // and 0 at R; never below MinimumExplosiveDamage. Missing fields are 0. What d is measured between is not traced.
  function blastAmount(cal, d) {
    var b = cal.blast || {}, R = b.radius || 0, E = b.effective_radius || 0, F = b.falloff || 0, mn = b.minimum || 0;
    var base = cal.base_damage || 0, a;
    if (d <= E) a = base;
    else if (d >= R) a = 0;
    else {
      var t = Math.abs(E - R) <= 1e-8 ? (d >= E ? 1 : 0) : Math.min(Math.max((d - R) / (E - R), 0), 1);
      a = base * ((1 - F) + F * t);
    }
    return Math.max(a, mn);
  }

  function useBlast() { return state.blast && state.caliber && !!state.caliber.blast; }
  function perHit(cal) { return useBlast() ? blastAmount(cal, state.dist) : cal.base_damage; }

  // Port of apply_section in damage_tables.py (Vehicle §4): one point application to a section.
  function applySection(secs, health, key, amount, depth) {
    var sec = secs[key], handled = 0;
    if (!sec || depth > 10 || !(amount > 0)) return 0;
    function clamp01(x) { return Math.min(Math.max(x, 0), 1); }
    function reroute(routes) {
      routes.forEach(function (r) {
        if ((health[key] <= 0) === !!r[2] && amount - handled > 0)
          handled += applySection(secs, health, r[0], (amount - handled) * clamp01(r[1]), depth + 1);
      });
    }
    reroute(sec.pre);
    var own = Math.min(Math.max(amount - handled, 0), Math.max(health[key], 0));
    health[key] -= own;
    handled += own;
    if (key === data.meta.main_section && health[key] <= 0) return handled;
    sec.simultaneous.forEach(function (r) {
      if (!r[2] || health[key] <= 0) applySection(secs, health, r[0], own * clamp01(r[1]), depth + 1);
    });
    reroute(sec.post);
    return handled;
  }

  // Hits of `dmg` on the slot's section until the main health reaches 0, or null.
  function simHits(v, s, dmg) {
    var secs = v.sections, main = data.meta.main_section, health = {}, hits = 0;
    if (!secs || !secs[s.section] || !(dmg > 0)) return null;
    Object.keys(secs).forEach(function (k) { health[k] = secs[k].max_health; });
    while (health[main] > 0 && hits < 5000) { applySection(secs, health, s.section, dmg, 0); hits++; }
    return hits < 5000 ? hits : null;
  }

  // The slot's rule factor: a blast hit is tagged Radius.Inner within E, else Radius.Outer (Damage §1.1),
  // and meets different rules than the direct impact.
  function factorOf(s, cal) {
    var b = useBlast() && s.blast_factor && s.blast_factor[cal.id];
    if (!b) return s.rule_factor[cal.id];
    return state.dist <= ((cal.blast && cal.blast.effective_radius) || 0) ? b[0] : b[1];
  }

  // Rule-factor-scaled damage and hits to destroy for a slot; the direct view reads the precomputed values.
  function dmgOf(s, cal) { return perHit(cal) * factorOf(s, cal); }
  function hitsOf(s, cal) {
    return useBlast() ? simHits(state.vehicle, s, dmgOf(s, cal)) : s.hits_to_destroy[cal.id];
  }

  // The selected vehicle's value range for the current caliber, ignoring nulls.
  function range(values) {
    var known = values.filter(function (x) { return x != null && x > 0; });
    if (!known.length) return null;
    return { min: Math.min.apply(null, known), max: Math.max.apply(null, known) };
  }

  function scale() {
    var v = state.vehicle;
    if (state.mode === "hits") {
      var r = range(v.slots.map(function (s) { return hitsOf(s, state.caliber); }));
      return { range: r, t: function (x) {     // fewer hits: brighter
        if (!r || r.max === r.min) return 1;
        return 1 - (Math.log(x) - Math.log(r.min)) / (Math.log(r.max) - Math.log(r.min));
      } };
    }
    var f = range(v.slots.map(function (s) { return factorOf(s, state.caliber); }));
    return { range: f, t: function (x) {       // more damage let through: brighter
      if (!f || f.max === f.min) return 1;
      return (x - f.min) / (f.max - f.min);
    } };
  }

  // { colour, none } for a slot entry in the current mode; none: can't destroy / no damage.
  function paint(s, sc) {
    if (!s) return { colour: NONE_COLOUR, none: true };   // a material with no section
    if (state.mode === "section") return { colour: familyOf(s.section).colour, none: false };
    var x = state.mode === "hits" ? hitsOf(s, state.caliber) : factorOf(s, state.caliber);
    if (x == null || !(x > 0)) return { colour: NONE_COLOUR, none: true };
    return { colour: ramp(sc.t(x)), none: false };
  }

  function valueText(s) {
    if (state.mode === "hits") {
      var h = hitsOf(s, state.caliber);
      return h == null ? "can't destroy" : num(h) + (h === 1 ? " hit" : " hits");
    }
    if (state.mode === "factor") return "×" + num(factorOf(s, state.caliber));
    return shortSection(s.section) + (s.max_health != null ? " · " + num(s.max_health) + " HP" : "");
  }

  /* ---------- slot resolution ---------- */

  // The game's lookup (Vehicle §3.1): (group, slot), else the group's default, else the same in the parent
  // group while it is under ComplexSurface.Group, else no section. Default is Wheel's sibling, not its parent.
  function resolve(name, v) {
    var parts = String(name || "").split("|");
    var slot = parts[0], group = parts[1] ? GROUP + parts[1] : DEFAULT_GROUP;
    var s = v.slots, i, g;
    for (g = group; g; g = g === GROUP.slice(0, -1) ? null : g.slice(0, g.lastIndexOf("."))) {
      for (i = 0; i < s.length; i++) if (s[i].slot === slot && s[i].group === g) return { index: i, how: g === group ? "exact" : "parent" };
      for (i = 0; i < s.length; i++) {
        if (s[i].slot === "(default)" && s[i].group === g && s[i].section && s[i].section !== "None") return { index: i, how: "default" };
      }
    }
    return { index: -1, how: "none" };
  }

  // Mapped slots that look like indexed copies of a material's slot (CC_Wheel -> CC_Wheel_0, CC_Wheel_1).
  function similar(name, v) {
    var slot = String(name || "").split("|")[0];
    return v.slots.filter(function (s) { return s.slot.indexOf(slot + "_") === 0; }).map(function (s) { return s.slot; });
  }

  /* ---------- plain-words routing ---------- */

  function target(tag) { return tag === mainSection ? "the main health" : "the " + shortSection(tag) + " section"; }

  function routing(s) {
    if (s.section === mainSection) return ["is the main health: the vehicle is destroyed when it reaches 0"];
    var r = s.routing || {}, out = [], toMain = false;
    (r.pre || []).forEach(function (x) {
      toMain = toMain || x.to === mainSection;
      out.push((x.only_when_depleted ? "once destroyed, passes " : "passes ") + pct(x.scalar) +
               " of each hit to " + target(x.to) + " first");
    });
    (r.simultaneous || []).forEach(function (x) {
      toMain = toMain || x.to === mainSection;
      out.push("copies " + pct(x.scalar) + " of the damage it absorbs to " + target(x.to) +
               (x.only_when_depleted ? " once destroyed" : ""));
    });
    (r.post || []).forEach(function (x) {
      toMain = toMain || x.to === mainSection;
      out.push(x.only_when_depleted
        ? "passes " + pct(x.scalar) + " of further damage to " + target(x.to) + " once destroyed"
        : "passes " + pct(x.scalar) + " of the damage it doesn't absorb to " + target(x.to));
    });
    if (!out.length) out.push("never passes damage to the main health");
    else if (!toMain) out.push("does not pass damage to the main health directly");
    return out;
  }

  /* ---------- controls ---------- */

  function fillVehicles() {
    var sel = els.vehicle, groups = {};
    sel.textContent = "";
    data.vehicles.forEach(function (v, i) {
      var kind = v.damage_row.replace(ROW, "").split(".")[0];
      if (!groups[kind]) { groups[kind] = el("optgroup"); groups[kind].label = kind; sel.appendChild(groups[kind]); }
      var label = v.models.length > 1 ? v.damage_row.replace(ROW, "") : vehicleLabel(v);   // variants: in the Variant list
      var o = el("option", null, label + (v.models.length ? "" : " (no model yet)"));
      o.value = v.id;
      groups[kind].appendChild(o);
    });
    sel.disabled = false;
  }

  function fillCalibers() {
    var sel = els.caliber;
    sel.textContent = "";
    var groups = {};
    data.meta.calibers.forEach(function (c) {
      var g = c.group || "Calibers";
      if (!groups[g]) { groups[g] = document.createElement("optgroup"); groups[g].label = g; sel.appendChild(groups[g]); }
      var o = el("option", null, c.label + (c.unused ? " [not hand-held]" : "") + " (base " + num(c.base_damage) + ")");
      o.value = c.id;
      groups[g].appendChild(o);
    });
    sel.disabled = false;
  }

  function setupMode() {
    var group = els.mode, buttons = group.querySelectorAll("button");
    function choose(b, focus) {
      state.mode = b.value;
      Array.prototype.forEach.call(buttons, function (x) {
        x.setAttribute("aria-checked", String(x === b));
        x.tabIndex = x === b ? 0 : -1;
      });
      if (focus) b.focus();
      repaint();
    }
    Array.prototype.forEach.call(buttons, function (b) {
      b.addEventListener("click", function () { choose(b, false); });
    });
    group.addEventListener("keydown", function (e) {
      var step = e.key === "ArrowRight" || e.key === "ArrowDown" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowUp" ? -1 : 0;
      if (!step) return;
      e.preventDefault();
      var list = Array.prototype.slice.call(buttons);
      var at = list.indexOf(group.querySelector('[aria-checked="true"]'));
      choose(list[(at + step + list.length) % list.length], true);
    });
  }

  /* ---------- slot list, legend, panel ---------- */

  function swatch(p) {
    var i = el("i", "vv-swatch" + (p.none ? " is-none" : ""));
    i.setAttribute("aria-hidden", "true");
    if (!p.none) i.style.background = p.colour;
    return i;
  }

  function buildList() {
    var list = els.slots, v = state.vehicle;
    list.textContent = "";
    v.slots.forEach(function (s, i) {
      var li = el("li"), b = el("button", "vv-slot");
      b.type = "button";
      b.setAttribute("aria-pressed", "false");
      b.dataset.slot = i;
      var name = el("span", "vv-slot-name", slotName(s));
      if (s.group !== DEFAULT_GROUP) name.appendChild(el("small", "vv-slot-group", shortGroup(s.group) + " group"));
      var absent = el("small", "vv-slot-absent", "unreachable");
      absent.hidden = true;
      name.appendChild(absent);
      b.appendChild(el("i", "vv-swatch"));
      b.appendChild(name);
      b.appendChild(el("span", "vv-slot-value"));
      b.addEventListener("click", function () { select(state.selected === i ? -1 : i, null); });
      li.appendChild(b);
      list.appendChild(li);
    });
  }

  function updateList(sc) {
    var onModel = {};
    materials.forEach(function (m) { if (m.index >= 0) onModel[m.index] = true; });
    Array.prototype.forEach.call(els.slots.querySelectorAll(".vv-slot"), function (b) {
      var i = +b.dataset.slot, s = state.vehicle.slots[i], p = paint(s, sc);
      b.replaceChild(swatch(p), b.firstChild);
      b.querySelector(".vv-slot-value").textContent = valueText(s);
      b.setAttribute("aria-pressed", String(i === state.selected));
      var absent = !!s.unreachable || (materials.length > 0 && !onModel[i]);
      b.classList.toggle("is-absent", absent);
      b.querySelector(".vv-slot-absent").hidden = !absent;
    });
  }

  function key(colour, label, none) {
    var k = el("span", "vv-key");
    k.appendChild(swatch({ colour: colour, none: !!none }));
    k.appendChild(document.createTextNode(label));
    return k;
  }

  function updateLegend(sc) {
    var lg = els.legend, v = state.vehicle, cal = state.caliber;
    lg.textContent = "";
    if (state.mode === "section") {
      lg.appendChild(el("span", "vv-legend-title", "Section"));
      var seen = {};
      FAMILIES.concat([MAIN]).forEach(function (f) { seen[f.key] = false; });
      v.slots.forEach(function (s) { seen[familyOf(s.section).key] = true; });
      seen.Main = true;
      FAMILIES.concat([MAIN]).forEach(function (f) { if (seen[f.key]) lg.appendChild(key(f.colour, f.label)); });
      if (noSection()) lg.appendChild(key(NONE_COLOUR, "no section: hits do nothing", true));
      return;
    }
    var hits = state.mode === "hits";
    lg.appendChild(el("span", "vv-legend-title", (hits ? "Hits to destroy" : "Rule factor") + ", " + cal.label));
    var anyNone = v.slots.some(function (s) { return paint(s, sc).none; });
    if (sc.range) {
      var bar = el("span", "vv-ramp"), stops = [];
      for (var i = 0; i <= 10; i++) stops.push(ramp(hits ? 1 - i / 10 : i / 10));
      var track = el("span", "vv-ramp-bar");
      track.style.background = "linear-gradient(90deg, " + stops.join(", ") + ")";
      track.setAttribute("aria-hidden", "true");
      var lo = hits ? num(sc.range.min) + " (fewest)" : "×" + num(sc.range.min);
      var hi = hits ? num(sc.range.max) + " (most)" : "×" + num(sc.range.max);
      bar.appendChild(el("span", "vv-tick", lo));
      bar.appendChild(track);
      bar.appendChild(el("span", "vv-tick", hi));
      lg.appendChild(bar);
      lg.appendChild(el("span", "vv-legend-note", hits ? "log scale; brighter = fewer hits" : "brighter = more damage gets through"));
    }
    if (anyNone || !sc.range) lg.appendChild(key(NONE_COLOUR, hits ? "can't destroy the vehicle" : "no damage", true));
    if (noSection()) lg.appendChild(key(NONE_COLOUR, "no section: hits do nothing", true));
  }

  function noSection() { return materials.some(function (m) { return m.index < 0; }); }

  function row(dl, term, value) {
    dl.appendChild(el("dt", null, term));
    var dd = el("dd");
    if (value instanceof Node) dd.appendChild(value); else dd.textContent = value;
    dl.appendChild(dd);
  }

  function code(text) { return el("code", null, text); }

  // A dotted tag in <code> that may wrap after each dot instead of mid-word.
  function breakable(tag) {
    var c = el("code");
    tag.split(".").forEach(function (part, i, all) {
      c.appendChild(document.createTextNode(part + (i < all.length - 1 ? "." : "")));
      if (i < all.length - 1) c.appendChild(el("wbr"));
    });
    return c;
  }

  function docLink(href, text) {
    var a = el("a", null, text);
    a.href = base + href;
    return a;
  }

  // Built off-document and swapped in only when it changed, so the live region speaks once.
  function updatePanel() {
    var live = els.panelBody, body = el("div"), v = state.vehicle;
    fillPanel(body, v);
    if (body.innerHTML !== live.innerHTML) live.innerHTML = body.innerHTML;
  }

  function fillPanel(body, v) {
    var title = el("h2", "vv-panel-title no_anchor");
    body.appendChild(title);
    if (state.selected < 0 && state.picked) {   // a material that resolves to no section
      title.textContent = state.picked;
      title.insertBefore(swatch({ colour: NONE_COLOUR, none: true }), title.firstChild);
      body.appendChild(el("p", "vv-note", "This surface resolves to no health section, so a hit on it does nothing " +
        "to the vehicle. The note under the model says why."));
      return;
    }
    if (state.selected < 0) {
      title.className += " is-empty";
      title.textContent = "No slot selected";
      body.appendChild(el("p", "vv-panel-empty", "Click a part of the model, or pick a slot from the list below."));
      return;
    }
    var s = v.slots[state.selected], cal = state.caliber, sc = scale();
    title.textContent = state.picked || slotName(s);
    title.insertBefore(swatch(paint(s, sc)), title.firstChild);

    var dl = el("dl", "vv-facts");
    var mats = materials.filter(function (m) { return m.index === state.selected; }).map(function (m) { return m.name; });
    if (state.picked) {
      var how = resolve(state.picked, v).how;
      row(dl, "Material", code(state.picked));
      if (how !== "exact") {
        row(dl, "Slot entry", how === "default"
          ? "not in the slot map: takes the " + shortGroup(s.group) + " group's default section"
          : "not in its own group's map: found in the parent " + shortGroup(s.group) + " group");
      }
      var near = how === "default" ? similar(state.picked, v) : [];
      if (near.length) {
        body.appendChild(dl);
        dl = el("dl", "vv-facts");
        body.appendChild(el("p", "vv-note", "The slot map lists " + near.join(" / ") + " but this mesh's slot is " +
          state.picked.split("|")[0] + ". Only instanced wheels get a wheel index; this is a static mesh, so the " +
          "game uses the default section and those listed slots can't be hit."));
      }
    } else if (materials.length) {
      row(dl, "Materials", mats.length ? mats.join(", ") : "none on this model");
      if (!mats.length) {
        body.appendChild(dl);
        dl = el("dl", "vv-facts");
        body.appendChild(el("p", "vv-note", "No collision geometry carries this slot on this model, so direct hits " +
          "can't select it. Damage can still arrive through routing from other sections."));
      }
    }
    if (s.unreachable) {
      body.appendChild(dl);
      dl = el("dl", "vv-facts");
      body.appendChild(el("p", "vv-note", "No hit in the game can produce this slot key: " + s.unreachable + "."));
    }
    if (!state.picked || state.picked !== s.slot) {
      var entry = el("span");
      entry.appendChild(code(slotName(s)));
      entry.appendChild(document.createTextNode(" in the " + shortGroup(s.group) + " group"));
      row(dl, "Slot map", entry);
    }
    row(dl, "Section", breakable(s.section || "?"));
    row(dl, "Max health", s.max_health != null ? num(s.max_health) : "?");
    var ul = el("ul", "vv-routes");
    routing(s).forEach(function (line) { ul.appendChild(el("li", null, line)); });
    row(dl, "Routing", ul);
    var f = factorOf(s, cal), h = hitsOf(s, cal), amt = perHit(cal);
    row(dl, "Rule factor (" + cal.label + (useBlast() ? ", blast" : "") + ")", "×" + num(f));
    row(dl, useBlast() ? "Blast amount (" + num(state.dist / 100) + " m)" : "Damage per hit", num(amt) + " × " + num(f) + " = " + num(amt * f));
    row(dl, "Hits to destroy", h == null ? "can't destroy the vehicle through this slot" : num(h));
    body.appendChild(dl);
    if (cal.note) body.appendChild(el("p", "vv-caliber-note", cal.note));

    var links = el("p", "vv-panel-links");
    links.appendChild(docLink(data.meta.docs.hitboxes, "Hitboxes (§3.1)"));
    links.appendChild(document.createTextNode(" · "));
    links.appendChild(docLink(data.meta.docs.routing, "Routing (§4.2)"));
    links.appendChild(document.createTextNode(" · "));
    links.appendChild(docLink(data.meta.docs.hits_to_destroy, "Hits to destroy (§5.4)"));
    body.appendChild(links);
  }

  /* ---------- model ---------- */

  function webgl() {
    try {
      var c = document.createElement("canvas");
      return !!(window.WebGLRenderingContext && (c.getContext("webgl2") || c.getContext("webgl")));
    } catch (e) { return false; }
  }

  // Resolves once <model-viewer> is defined; rejects if its module fails or takes too long.
  function whenModelViewer() {
    return new Promise(function (resolve, reject) {
      if (!webgl()) { reject(new Error("WebGL is not available in this browser")); return; }
      if (!window.customElements) { reject(new Error("this browser has no custom elements")); return; }
      var started = Date.now();
      var poll = setInterval(function () {
        if (document.documentElement.classList.contains("vv-mv-failed")) {
          clearInterval(poll); reject(new Error("the 3D viewer script did not load"));
        } else if (Date.now() - started > MV_TIMEOUT) {
          clearInterval(poll); reject(new Error("the 3D viewer script took too long to load"));
        }
      }, 250);
      customElements.whenDefined("model-viewer").then(function () { clearInterval(poll); resolve(); });
    });
  }

  function status(text) {
    els.status.textContent = text || "";
    els.status.hidden = !text;
  }

  // models[].notes (GLB asset.extras.notes): shown under the stage, in 3D and table view alike.
  function updateNotes() {
    var notes = ((currentModel() || {}).notes || []).filter(Boolean), box = els.notes;
    box.textContent = "";
    notes.forEach(function (n) { box.appendChild(el("p", null, n)); });
    box.hidden = !notes.length;
  }

  function showFallback(reason) {
    fallbackText = reason;
    els.stage.classList.add("is-fallback");
    els.fallback.hidden = false;
    els.fallback.textContent = "";
    els.fallback.appendChild(el("p", "vv-fallback-note", reason));
    var wrap = el("div", "table-wrapper"), t = el("table"), cal = state.caliber;
    var head = t.createTHead().insertRow();
    ["Collision slot", "Section (max health)", "Routing", "Rule factor (" + cal.label + ")",
     "Damage per hit", "Hits to destroy"].forEach(function (h, i) {
      var th = el("th", i >= 3 ? "num" : null, h);
      th.scope = "col";
      head.appendChild(th);
    });
    var tb = t.createTBody();
    state.vehicle.slots.forEach(function (s) {
      var r = tb.insertRow(), f = factorOf(s, cal), h = hitsOf(s, cal);
      var c0 = r.insertCell();
      c0.appendChild(code(slotName(s)));
      if (s.group !== DEFAULT_GROUP) c0.appendChild(document.createTextNode(" [" + shortGroup(s.group) + "]"));
      r.insertCell().textContent = shortSection(s.section) + " (" + num(s.max_health) + ")";
      r.insertCell().textContent = routing(s).join("; ");
      [["×" + num(f)], [num(perHit(cal) * f)], [h == null ? "can't destroy" : num(h)]].forEach(function (x) {
        var c = r.insertCell();
        c.className = "num";
        c.textContent = x[0];
      });
    });
    wrap.appendChild(t);
    els.fallback.appendChild(wrap);
  }

  function hideFallback() {
    fallbackText = null;
    els.stage.classList.remove("is-fallback");
    els.fallback.hidden = true;
    els.fallback.textContent = "";
  }

  function fallbackReason() {
    if (mvState !== "ok") return "The 3D view is unavailable (" + mvState + "). The hitboxes of this vehicle:";
    return "No collision mesh has been exported for this vehicle yet. Its hitboxes:";
  }

  function loadModel() {
    var v = state.vehicle;
    materials = [];
    clearHotspots();
    if (mvState === "pending") { status("Loading the 3D viewer…"); return; }   // whenModelViewer() calls back
    var model = currentModel();
    if (mvState !== "ok" || !model) {
      status("");
      showFallback(fallbackReason());
      return;
    }
    hideFallback();
    status("Loading the collision mesh…");
    var token = ++loadToken;
    viewer.dataset.token = token;
    var src = base + model.path;
    if (viewer.getAttribute("src") === src) onLoad();
    else viewer.setAttribute("src", src);
  }

  function onLoad() {
    if (+viewer.dataset.token !== loadToken || !viewer.model) return;
    var v = state.vehicle;
    materials = viewer.model.materials.map(function (m) {
      var r = resolve(m.name, v);
      try {
        m.pbrMetallicRoughness.setMetallicFactor(0);
        m.pbrMetallicRoughness.setRoughnessFactor(0.85);
      } catch (e) { /* keep the file's values */ }
      return { material: m, name: m.name, index: r.index };
    });
    frame();
    buildHotspots();
    repaint();
    status("");
  }

  // Fit the model's bounding box to the stage from the default view angle: for each box corner,
  // the camera distance that keeps it inside the vertical and horizontal field of view, plus a
  // margin for labels. (model-viewer's own "auto" fits a bounding sphere, which leaves long
  // vehicles small.) The user can still zoom out to model-viewer's limit.
  var THETA = -35, PHI = 70, MARGIN = 1.12;
  function frame() {
    try {
      var size = viewer.getDimensions(), w = viewer.clientWidth, h = viewer.clientHeight;
      var fov = viewer.getFieldOfView() * Math.PI / 180;
      if (!size || !w || !h || !(fov > 0)) return;
      var t = THETA * Math.PI / 180, ph = PHI * Math.PI / 180;
      var d = [Math.sin(ph) * Math.sin(t), Math.cos(ph), Math.sin(ph) * Math.cos(t)];   // towards the camera
      var right = [Math.cos(t), 0, -Math.sin(t)];
      var up = [d[1] * right[2] - d[2] * right[1], d[2] * right[0] - d[0] * right[2], d[0] * right[1] - d[1] * right[0]];
      var tanV = Math.tan(fov / 2), tanH = tanV * w / h, dist = 0;
      [-0.5, 0.5].forEach(function (a) { [-0.5, 0.5].forEach(function (b) { [-0.5, 0.5].forEach(function (c) {
        var p = [a * size.x, b * size.y, c * size.z];
        var dot = function (v) { return p[0] * v[0] + p[1] * v[1] + p[2] * v[2]; };
        var z = dot(d);
        dist = Math.max(dist, z + Math.abs(dot(up)) / tanV, z + Math.abs(dot(right)) / tanH);
      }); }); });
      if (dist > 0) {
        viewer.cameraOrbit = THETA + "deg " + PHI + "deg " + (dist * MARGIN).toFixed(3) + "m";
        viewer.jumpCameraToGoal();
      }
    } catch (e) { /* keep model-viewer's framing */ }
  }

  function onError() {
    status("");
    showFallback("The collision mesh for this vehicle could not be loaded. Its hitboxes:");
  }

  function clearHotspots() {
    if (!viewer) return;
    Array.prototype.forEach.call(viewer.querySelectorAll(".vv-hotspot"), function (h) { h.remove(); });
  }

  function buildHotspots() {
    clearHotspots();
    var centres = (currentModel() || {}).centres || [];
    state.vehicle.slots.forEach(function (s, i) {
      var centre = centres[i];
      if (!centre || s.slot === "(default)") return;
      var b = el("button", "vv-hotspot");
      b.type = "button";
      b.slot = "hotspot-" + i;
      b.dataset.position = centre.join(" ");
      b.dataset.visibilityAttribute = "visible";
      b.dataset.slot = i;
      b.tabIndex = -1;                       // the slot list is the keyboard route
      b.setAttribute("aria-hidden", "true");
      b.appendChild(el("i", "vv-swatch"));
      b.appendChild(el("span", null, s.slot.replace(/^CC_/, "")));
      b.addEventListener("click", function (e) {
        e.stopPropagation();
        select(state.selected === i ? -1 : i, null);
      });
      viewer.appendChild(b);
    });
  }

  // Labels that would overlap are pushed down (a leader line keeps them tied to their point).
  // Runs a frame after model-viewer has moved them: on camera change, load and resize.
  var declutterQueued = false;
  function queueDeclutter() {
    if (declutterQueued) return;
    declutterQueued = true;
    requestAnimationFrame(function () { requestAnimationFrame(function () { declutterQueued = false; declutter(); }); });
  }

  function declutter() {
    if (!viewer || !state.labels) return;
    var items = Array.prototype.map.call(viewer.querySelectorAll(".vv-hotspot"), function (h) {
      var dy = parseFloat(h.style.getPropertyValue("--vv-dy")) || 0, r = h.getBoundingClientRect();
      return { h: h, left: r.left, right: r.right, top: r.top - dy, bottom: r.bottom - dy };
    }).filter(function (it) { return it.right > it.left; });
    items.sort(function (a, b) { return a.top - b.top || a.left - b.left; });
    var placed = [];
    items.forEach(function (it) {
      var dy = 0, moved = true, guard = 0;
      while (moved && guard++ < items.length + 1) {
        moved = false;
        placed.forEach(function (p) {
          if (it.left < p.right + 3 && it.right > p.left - 3 && it.top + dy < p.bottom + 3 && it.bottom + dy > p.top - 3) {
            dy = p.bottom + 3 - it.top;
            moved = true;
          }
        });
      }
      placed.push({ left: it.left, right: it.right, top: it.top + dy, bottom: it.bottom + dy });
      it.h.style.setProperty("--vv-dy", Math.round(dy) + "px");
      it.h.classList.toggle("is-moved", dy > 0);
    });
  }

  function updateHotspots(sc) {
    if (!viewer) return;
    viewer.classList.toggle("vv-no-labels", !state.labels);
    Array.prototype.forEach.call(viewer.querySelectorAll(".vv-hotspot"), function (b) {
      var i = +b.dataset.slot, p = paint(state.vehicle.slots[i], sc);
      b.replaceChild(swatch(p), b.firstChild);
      b.classList.toggle("is-selected", i === state.selected);
    });
    queueDeclutter();
  }

  function linear(hex) {
    return hexToRgb(hex).map(function (c) {
      c /= 255;
      return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
  }

  function ghosting() { return state.xray && state.selected >= 0 && materials.length > 0; }

  // Colour every material; with a slot selected and "See-through selection" on, the others fade
  // to a faint tint of their colour so parts inside the body (fuel tank, engine) show through.
  function updateMaterials(sc) {
    var ghost = ghosting();
    materials.forEach(function (m) {
      var s = m.index >= 0 ? state.vehicle.slots[m.index] : null;
      var selected = m.index >= 0 && m.index === state.selected;
      var faded = ghost && !selected;
      try {
        m.material.setAlphaMode(faded ? "BLEND" : "OPAQUE");
        m.material.pbrMetallicRoughness.setBaseColorFactor(linear(paint(s, sc).colour).concat([faded ? GHOST : 1]));
        m.material.setEmissiveFactor(selected ? HIGHLIGHT : "#000000");
      } catch (e) { /* material not ready */ }
    });
  }

  /* ---------- state changes ---------- */

  // Show the blast controls for a caliber with blast data; the slider runs 0 to its ExplosiveRadius.
  function syncBlast() {
    var b = state.caliber && state.caliber.blast;
    els.blastField.hidden = !b;
    if (!b) return;
    var max = (b.radius || 0) / 100;
    els.dist.max = max;
    els.dist.step = 0.5;
    if (state.dist > max * 100) state.dist = max * 100;
    els.dist.value = state.dist / 100;
    els.dist.disabled = !state.blast;
    els.distOut.textContent = num(state.dist / 100) + " m";
    els.blastNote.textContent = state.blast
      ? "Falloff: full damage within " + num((b.effective_radius || 0) / 100) + " m, none at " + num(max) + " m (Damage pipeline §1.1). " +
        "Amount at this distance: " + num(blastAmount(state.caliber, state.dist)) + ". What the distance is measured between is not traced."
      : "";
  }

  function repaint() {
    if (!state.vehicle) return;
    var sc = scale();
    updateMaterials(sc);
    updateHotspots(sc);
    updateList(sc);
    updateLegend(sc);
    updatePanel();
    if (fallbackText) showFallback(fallbackText);
    if (viewer && state.vehicle) {
      var m = currentModel();
      viewer.alt = "Collision mesh of " + vehicleLabel(state.vehicle) + (m && state.vehicle.models.length > 1 ? ", " + modelLabel(m) : "") +
        (m && m.path.indexOf("--wheels-destroyed") >= 0 ? ", wheels destroyed" : "") + ", coloured by " +
        (state.mode === "section" ? "health section" : state.mode === "hits" ? "hits to destroy" : "rule factor");
    }
  }

  function select(i, picked) {
    state.selected = i;
    state.picked = i >= 0 ? picked : null;
    repaint();
  }

  // "#<id>" or "#<id>/<variant>" (any variant name of that model).
  function parseHash() {
    var h = decodeURIComponent(location.hash.slice(1)), cut = h.indexOf("/");
    return cut < 0 ? { id: h, variant: null } : { id: h.slice(0, cut), variant: h.slice(cut + 1) };
  }

  function modelFor(v, variant) {
    if (!v.models.length) return -1;
    for (var i = 0; variant && i < v.models.length; i++) if (v.models[i].variants.indexOf(variant) >= 0) return i;
    return 0;
  }

  function writeHash() {
    var v = state.vehicle, m = currentModel();
    var h = "#" + v.id + (m && v.models.length > 1 && state.model > 0 ? "/" + m.variants[0] : "");
    if (location.hash === h || decodeURIComponent(location.hash) === h) return;
    try { history.replaceState(null, "", h); } catch (e) { location.hash = h; }
  }

  function fillVariants() {
    var v = state.vehicle, sel = els.variant;
    sel.textContent = "";
    v.models.forEach(function (m, i) {
      var o = el("option", null, modelLabel(m));
      o.value = String(i);
      sel.appendChild(o);
    });
    sel.value = String(state.model);
    els.variantField.hidden = v.models.length < 2;
    var m = v.models[state.model], damaged = !!(m && m.wheels_destroyed);
    if (!damaged) state.wheels = "intact";
    els.wheels.value = state.wheels;
    els.wheelsField.hidden = !damaged;
  }

  function setVehicle(id, variant, fromHash) {
    var v = data.vehicles.filter(function (x) { return x.id === id; })[0];
    if (!v) return;
    var model = modelFor(v, variant);
    if (v === state.vehicle && model === state.model) return;
    var sameVehicle = v === state.vehicle;
    state.vehicle = v;
    state.model = model;
    if (!sameVehicle) {
      state.selected = -1;
      state.picked = null;
      buildList();
    } else {
      state.picked = null;           // the slot stays selected across variants
    }
    els.vehicle.value = v.id;
    fillVariants();
    updateNotes();
    if (!fromHash) writeHash();
    loadModel();
    repaint();
  }

  function initialVehicle() {
    var want = parseHash();
    var ids = data.vehicles.map(function (v) { return v.id; });
    if (ids.indexOf(want.id) >= 0) return want;
    var withModel = data.vehicles.filter(function (v) { return v.models.length; })[0];
    if (ids.indexOf(PILOT) >= 0 && (!withModel || data.vehicles[ids.indexOf(PILOT)].models.length)) return { id: PILOT, variant: null };
    return { id: withModel ? withModel.id : ids[0], variant: null };
  }

  /* ---------- picking ---------- */

  function setupPicking() {
    // Pointer position relative to the viewer: focusing the viewer on press can scroll the page,
    // so the click's client coordinates may no longer be over the part that was pressed.
    var down = null;
    function at(e) { var r = viewer.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; }
    viewer.addEventListener("pointerdown", function (e) { down = at(e); });
    viewer.addEventListener("click", function (e) {
      if (!materials.length) return;
      var up = at(e);
      if (down && Math.abs(up[0] - down[0]) + Math.abs(up[1] - down[1]) > 6) return;   // a drag
      var r = viewer.getBoundingClientRect(), p = down || up;
      var m = viewer.materialFromPoint(r.left + p[0], r.top + p[1]);
      if (!m) { if (state.selected >= 0) select(-1, null); return; }
      var hit = materials.filter(function (x) { return x.material === m || x.material.index === m.index; })[0];
      if (!hit) return;
      if (hit.index < 0) {   // no section: explain it in the panel, nothing to select
        state.selected = -1;
        state.picked = ghosting() ? null : hit.name;
        repaint();
        return;
      }
      // See-through: clicks still land on the faded outer shell first, so a click on a faded
      // part clears the selection; inner parts are picked from the labels or the list.
      if (ghosting()) {
        if (hit.index !== state.selected) select(-1, null);
        return;
      }
      select(hit.index, hit.name);
    });
  }

  /* ---------- start ---------- */

  ready(function () {
    root = $("vv");
    if (!root) return;
    base = root.getAttribute("data-base") || "/";
    ["vehicle", "caliber", "mode", "stage", "status", "fallback", "legend", "slots", "labels", "xray", "variant", "wheels", "notes", "blastField", "blastMode", "dist", "distOut", "blastNote"].forEach(function (k) {
      els[k] = $("vv-" + k);
    });
    els.panelBody = $("vv-panel-body");
    els.variantField = $("vv-variant-field");
    els.wheelsField = $("vv-wheels-field");
    viewer = $("vv-model");
    status("Loading the hitbox data…");

    fetch(root.getAttribute("data-json"))
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (json) {
        data = json;
        mainSection = data.meta.main_section;
        data.vehicles.forEach(normalise);
        state.caliber = data.meta.calibers[0];
        fillVehicles();
        fillCalibers();
        syncBlast();
        setupMode();
        els.vehicle.addEventListener("change", function () { setVehicle(els.vehicle.value, null, false); });
        els.variant.addEventListener("change", function () {
          var m = state.vehicle.models[+els.variant.value];
          setVehicle(state.vehicle.id, m ? m.variants[0] : null, false);
        });
        els.wheels.addEventListener("change", function () {
          state.wheels = els.wheels.value;
          state.picked = null;
          updateNotes();
          loadModel();
          repaint();
        });
        els.caliber.addEventListener("change", function () {
          state.caliber = data.meta.calibers.filter(function (c) { return c.id === els.caliber.value; })[0];
          syncBlast();
          repaint();
        });
        els.blastMode.addEventListener("change", function () { state.blast = els.blastMode.value === "blast"; syncBlast(); repaint(); });
        els.dist.addEventListener("input", function () { state.dist = +els.dist.value * 100; syncBlast(); repaint(); });
        els.labels.addEventListener("change", function () { state.labels = els.labels.checked; repaint(); });
        els.xray.addEventListener("change", function () { state.xray = els.xray.checked; repaint(); });
        document.addEventListener("keydown", function (e) {
          if (e.key !== "Escape" || state.selected < 0 || e.target.tagName === "SELECT") return;
          select(-1, null);
        });
        window.addEventListener("hashchange", function () { var h = parseHash(); setVehicle(h.id, h.variant, true); });
        viewer.addEventListener("load", onLoad);
        viewer.addEventListener("camera-change", queueDeclutter);
        window.addEventListener("resize", queueDeclutter);
        viewer.addEventListener("error", onError);
        setupPicking();
        var start = initialVehicle();
        setVehicle(start.id, start.variant, false);
        whenModelViewer().then(function () {
          var MV = customElements.get("model-viewer");
          MV.meshoptDecoderLocation = new URL(base + MESHOPT, location.href).href;
          mvState = "ok";
        }, function (err) {
          mvState = err.message;
        }).then(function () {
          root.classList.toggle("vv-no-3d", mvState !== "ok");
          loadModel();
          repaint();
        });
      })
      .catch(function (err) {
        status("The hitbox data could not be loaded (" + err.message + ").");
        root.classList.add("vv-no-data");
      });
  });
})();
