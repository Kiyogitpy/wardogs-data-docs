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

  // Stable colours keyed by full health-section tag, so sections keep their identity across vehicles.
  var SECTION_COLOURS = {
    "Attribute.Gameplay.Health": "#8b8b96",
    "Attribute.Gameplay.Health.FuelTank": "#c98500",
    "Attribute.Gameplay.Health.Engine": "#d55181",
    "Attribute.Gameplay.Health.Rotor.Main": "#b56ed8",
    "Attribute.Gameplay.Health.Rotor.Tail": "#8f2eef",
    "Attribute.Gameplay.Health.Wheel.Left.Front": "#e41111",
    "Attribute.Gameplay.Health.Wheel.Right.Front": "#2eefbf",
    "Attribute.Gameplay.Health.Wheel.Left.Middle": "#dfef2e",
    "Attribute.Gameplay.Health.Wheel.Right.Middle": "#e411c1",
    "Attribute.Gameplay.Health.Wheel.Left.Rear": "#2eef2e",
    "Attribute.Gameplay.Health.Wheel.Right.Rear": "#9ad86e",
    "Attribute.Gameplay.Health.Tracks.Left": "#2e7fef",
    "Attribute.Gameplay.Health.Tracks.Right": "#d8896e",
    "Attribute.Gameplay.Health.Radar": "#2ecfef",
    "Attribute.Gameplay.Health.Body.StrongArea": "#d8be6e",
    "Attribute.Gameplay.Health.Body.ModerateArea": "#3386c1"
  };
  var UNKNOWN_SECTION_COLOURS = ["#8f2eef", "#2eefbf", "#2e7fef", "#e41111", "#dfef2e", "#2ecfef"];
  var NONE_COLOUR = "#3b3b42";       // "can't destroy" (hatched in the legend and list)
  // Sequential blue, dark mode: step 600 (dimmest allowed on dark) up to step 100.
  var RAMP = ["#184f95", "#1c5cab", "#256abf", "#2a78d6", "#3987e5", "#5598e7",
              "#6da7ec", "#86b6ef", "#9ec5f4", "#b7d3f6", "#cde2fb"];
  var HIGHLIGHT = "#5a5a5a";         // emissive added to the selected slot's materials
  var GHOST = 0.13;                  // alpha of the other slots while one is selected (see-through)

  var root, data, mainSection, base, els = {};
  var state = { vehicle: null, model: -1, caliber: null, interaction: "inspect", shot: null,
                mode: "section", selected: -1, picked: null, labels: true, xray: true, wheels: "intact" };
  var viewer = null, mvState = "pending", materials = [], loadToken = 0, fallbackText = null;
  var geometryCache = new Map(), impactGeometry = null, impactMetadata = null, metadataPromise = null;
  var impactToken = 0, impactLoading = false, impactError = null;
  var inspectHint = "";

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

  function unknownSectionColour(section) {
    var hash = 2166136261;
    for (var i = 0; i < section.length; i++) hash = Math.imul(hash ^ section.charCodeAt(i), 16777619);
    return UNKNOWN_SECTION_COLOURS[(hash >>> 0) % UNKNOWN_SECTION_COLOURS.length];
  }

  function sectionOf(section) {
    if (!section || section === mainSection) {
      return { tag: mainSection, label: "Main health", colour: SECTION_COLOURS[mainSection] || "#8b8b96" };
    }
    return { tag: section, label: shortSection(section),
             colour: SECTION_COLOURS[section] || unknownSectionColour(section) };
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

  /* ---------- per-slot direct-hit inspection ---------- */

  function perHit(cal) { return cal.base_damage; }
  function factorOf(s, cal) {
    var factors = cal.source_type === "actor" && s.explosion_factor && s.explosion_factor[cal.id];
    return factors ? factors[0] : (s.rule_factor || {})[cal.id];
  }

  // Rule-factor-scaled damage and hits to destroy for a slot; the direct view reads the precomputed values.
  function hitsOf(s, cal) {
    return cal.source_type === "actor" ? null : s.hits_to_destroy[cal.id];
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
    if (state.mode === "section") return { colour: sectionOf(s.section).colour, none: false };
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
    sources().forEach(function (c) {
      var g = c.group || "Calibers";
      if (!groups[g]) { groups[g] = document.createElement("optgroup"); groups[g].label = g; sel.appendChild(groups[g]); }
      var o = el("option", null, c.label + (c.unused ? " [not hand-held]" : "") + " (base " + num(c.base_damage) + ")");
      o.value = c.id;
      groups[g].appendChild(o);
    });
    sel.disabled = false;
  }

  function sources() { return data.meta.calibers.concat(data.meta.explosives || []); }

  function setupMode() {
    var group = els.mode, buttons = group.querySelectorAll("button");
    function choose(b, focus) {
      if (b.disabled) return;
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
      var next = (at + step + list.length) % list.length;
      while (list[next].disabled && next !== at) next = (next + step + list.length) % list.length;
      choose(list[next], true);
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
      var seen = Object.create(null);
      Object.keys(v.sections || {}).forEach(function (section) { if (section) seen[section] = true; });
      v.slots.forEach(function (s) { if (s.section && s.section !== "None") seen[s.section] = true; });
      if (mainSection) seen[mainSection] = true;
      Object.keys(seen).sort(function (a, b) {
        if (a === mainSection) return -1;
        if (b === mainSection) return 1;
        var left = shortSection(a), right = shortSection(b);
        return left < right ? -1 : left > right ? 1 : 0;
      }).forEach(function (section) {
        var entry = sectionOf(section);
        lg.appendChild(key(entry.colour, entry.label));
      });
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
    if (cal.source_type === "actor") {
      row(dl, "Explosion factor (full damage radius)", "×" + num(f));
      body.appendChild(el("p", "vv-note", "This source has no projectile impact. Place its explosion to estimate damage across the model."));
    } else {
      row(dl, "Rule factor (" + cal.label + ", direct)", "×" + num(f));
      row(dl, "Damage per direct hit", num(amt) + " × " + num(f) + " = " + num(amt * f));
      row(dl, "Hits to destroy", h == null ? "can't destroy the vehicle through this slot" : num(h));
      if (cal.blast) body.appendChild(el("p", "vv-note", "These are independent direct projectile hits through this slot. Place impact estimates one armed shot's blast separately."));
    }
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
    clearImpact();
    els.stage.classList.add("is-fallback");
    els.fallback.hidden = false;
    els.fallback.textContent = "";
    els.fallback.appendChild(el("p", "vv-fallback-note", reason));
    var wrap = el("div", "table-wrapper"), t = el("table"), cal = state.caliber;
    var head = t.createTHead().insertRow();
    ["Collision slot", "Section (max health)", "Routing", "Rule factor (" + cal.label + (cal.source_type === "actor" ? ", inner radius" : "") + ")",
     cal.source_type === "actor" ? "Explosion" : "Damage per hit", "Hits to destroy"].forEach(function (h, i) {
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
      [["×" + num(f)], [cal.source_type === "actor" ? "place explosion" : num(perHit(cal) * f)],
       [cal.source_type === "actor" ? "not a projectile" : h == null ? "can't destroy" : num(h)]].forEach(function (x) {
        var c = r.insertCell();
        c.className = "num";
        c.textContent = x[0];
      });
    });
    wrap.appendChild(t);
    els.fallback.appendChild(wrap);
    syncImpactControls();
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
    impactToken++;
    impactGeometry = null;
    impactMetadata = null;
    impactLoading = false;
    impactError = null;
    clearImpact();
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
    prepareImpact();
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
    requestAnimationFrame(function () { requestAnimationFrame(function () { declutterQueued = false; declutter(); drawImpact(); }); });
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
    viewer.classList.toggle("vv-no-labels", !state.labels || placingImpact());
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

  function ghosting() { return !placingImpact() && state.xray && state.selected >= 0 && materials.length > 0; }

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

  /* ---------- one-shot impact placement ---------- */

  function placingImpact() { return !!(state.caliber && state.caliber.blast && state.interaction === "impact"); }

  function syncImpactControls() {
    var active = placingImpact(), available = active && !!impactGeometry && !fallbackText;
    els.impactControls.hidden = !active;
    els.placeGround.disabled = !available;
    els.impactX.disabled = !available;
    els.impactZ.disabled = !available;
    els.clearImpact.disabled = !state.shot;
    els.panelBody.hidden = active;
    els.impactSummary.hidden = !active;
    if (active && !state.shot) renderImpactSummary();
    root.classList.toggle("vv-is-placing", active && !fallbackText);
    els.hint.textContent = active ? "Drag to turn, scroll or pinch to zoom. Click a surface to place a Direct hit or nearby ground for Splash; press Esc to clear the impact." : inspectHint;
    if (!active) return;
    els.impactHelp.textContent = fallbackText ? "Impact placement needs the 3D model. The inspection table is available below."
      : impactError ? "Impact geometry could not be loaded: " + impactError + ". Switch to Inspect slots to continue."
      : !available ? "Loading collision triangles for impact placement…"
      : "Click the vehicle for a Direct hit, or nearby ground for Splash. Each shot starts at full health. Ground is the model's lowest point; X is left/right and Z is front/back.";
  }

  function clearImpact() {
    state.shot = null;
    if (els.impactSummary) { els.impactSummary.hidden = true; els.impactSummary.textContent = ""; }
    if (els.impactOverlay) { els.impactOverlay.toggleAttribute("hidden", true); els.impactOverlay.textContent = ""; }
    if (els.clearImpact) els.clearImpact.disabled = true;
  }

  function prepareImpact() {
    if (!placingImpact() || mvState !== "ok" || !materials.length || fallbackText || impactGeometry || impactLoading) {
      syncImpactControls(); return;
    }
    var model = currentModel();
    if (!model) return;
    var path = model.path, token = ++impactToken;
    impactLoading = true;
    impactError = null;
    syncImpactControls();
    if (!metadataPromise) {
      metadataPromise = fetch(base + "assets/data/vehicle-impact-components.json").then(function (r) {
        if (!r.ok) throw new Error("component metadata HTTP " + r.status);
        return r.json();
      }).catch(function (error) { metadataPromise = null; throw error; });
    }
    if (!geometryCache.has(path)) {
      geometryCache.set(path, fetch(base + path).then(function (r) {
        if (!r.ok) throw new Error("collision mesh HTTP " + r.status);
        return r.arrayBuffer();
      }).then(function (buffer) {
        if (!window.VehicleImpactGeometry || !window.VehicleImpact || !window.MeshoptDecoder) throw new Error("impact scripts are unavailable");
        return window.VehicleImpactGeometry.load(buffer, window.MeshoptDecoder);
      }).catch(function (error) { geometryCache.delete(path); throw error; }));
    }
    Promise.all([geometryCache.get(path), metadataPromise]).then(function (loaded) {
      if (token !== impactToken || !currentModel() || currentModel().path !== path) return;
      var metadata = loaded[1].models && loaded[1].models[path];
      if (!metadata) throw new Error("no native component map for this assembly");
      impactGeometry = loaded[0];
      impactMetadata = metadata;
      impactLoading = false;
      els.impactX.value = String(Math.round(impactGeometry.bounds.center[0] * 10) / 10);
      els.impactZ.value = String(Math.round(impactGeometry.bounds.center[2] * 10) / 10);
      syncImpactControls();
    }).catch(function (error) {
      if (token !== impactToken) return;
      impactLoading = false;
      impactError = error.message;
      syncImpactControls();
    });
  }

  // Public model-viewer APIs expose the orbit in radians and the target in model metres.
  function impactCamera() {
    var G = window.VehicleImpactGeometry, orbit = viewer.getCameraOrbit(), target = viewer.getCameraTarget();
    var back = [Math.sin(orbit.phi) * Math.sin(orbit.theta), Math.cos(orbit.phi), Math.sin(orbit.phi) * Math.cos(orbit.theta)];
    var right = [Math.cos(orbit.theta), 0, -Math.sin(orbit.theta)], up = G.cross(back, right);
    return { position: G.add([target.x, target.y, target.z], G.scale(back, orbit.radius)), back: back, right: right, up: up,
      width: viewer.clientWidth, height: viewer.clientHeight, tan: Math.tan(viewer.getFieldOfView() * Math.PI / 360) };
  }

  function groundFromPixel(pixel) {
    var G = window.VehicleImpactGeometry, camera = impactCamera();
    var x = (2 * pixel[0] / camera.width - 1) * camera.tan * camera.width / camera.height;
    var y = (1 - 2 * pixel[1] / camera.height) * camera.tan;
    var direction = G.normalize(G.add(G.scale(camera.back, -1), G.add(G.scale(camera.right, x), G.scale(camera.up, y))));
    if (Math.abs(direction[1]) < 1e-9) return null;
    var distance = (impactGeometry.bounds.min[1] - camera.position[1]) / direction[1];
    return distance >= 0 && distance < 1000 ? G.add(camera.position, G.scale(direction, distance)) : null;
  }

  function placeImpact(position, label) {
    if (!placingImpact() || !impactGeometry || fallbackText) return;
    if (!position || !position.every(Number.isFinite)) {
      els.impactHelp.textContent = "That point does not meet the ground plane. Turn the camera downward or use ground X/Z.";
      return;
    }
    try {
      var incoming = window.VehicleImpactGeometry.sub(position, impactCamera().position);
      var origin = window.VehicleImpact.detonationOrigin(state.caliber, position, incoming);
      var result = window.VehicleImpact.simulate(impactGeometry, state.vehicle, state.caliber, origin, impactMetadata);
      state.shot = { origin: origin, impactPosition: position, label: label, result: result };
      syncImpactControls();
      renderImpactSummary();
      drawImpact();
    } catch (error) {
      clearImpact();
      els.impactHelp.textContent = "This impact could not be estimated: " + error.message;
    }
  }

  function renderImpactSummary() {
    var box = els.impactSummary, shot = state.shot;
    box.textContent = "";
    box.hidden = !placingImpact();
    if (!shot) {
      box.appendChild(el("h2", "vv-panel-title no_anchor", "Place an impact"));
      box.appendChild(el("p", "vv-panel-empty", fallbackText ? "Use Inspect slots to explore the available hitbox data." : "Click the vehicle or ground, or enter ground X/Z to preview one explosion."));
      return;
    }
    var result = shot.result, dl = el("dl", "vv-facts");
    box.appendChild(el("h2", "vv-panel-title no_anchor", shot.label));
    box.appendChild(el("p", "vv-note", (result.samplingMode === "native-bounds"
      ? "Reference-pose estimate using authored component bounds. "
      : "Reference-pose estimate from sampled display surfaces. ") +
      "Live collision and order can differ. Full health per shot."));
    if (state.caliber.blast.impact_backoff_cm > 0)
      box.appendChild(el("p", "vv-note", "Shot direction follows the view. Detonation is " +
        num(state.caliber.blast.impact_backoff_cm) + " cm back from the impact along that path."));
    row(dl, "Main health damage", num(result.mainDamage));
    row(dl, "Main health remaining", num(result.mainRemaining) + " / " + num(state.vehicle.sections[mainSection].max_health));
    row(dl, "Blast contacts", result.hits.length + " reached; " + result.occluded + " not reached");
    row(dl, "Damage applications", result.applications.length + " unique hit locations; " +
      (result.hits.length - result.applications.length) + " repeat contacts skipped");
    if (result.firstSection) row(dl, "Preview first section", shortSection(result.firstSection));
    if (result.scenarioMainDamage && result.scenarioMainDamage.min !== result.scenarioMainDamage.max) {
      row(dl, "First-choice examples", num(result.scenarioMainDamage.min) + "–" + num(result.scenarioMainDamage.max) + " main damage");
    }
    box.appendChild(dl);
    var changed = Object.keys(result.health).filter(function (key) {
      return key !== mainSection && result.health[key] < state.vehicle.sections[key].max_health;
    });
    if (changed.length) {
      var list = el("ul", "vv-routes");
      changed.forEach(function (key) {
        var routed = (result.transfers || []).filter(function (entry) { return entry.section === key && entry.via; });
        var note = routed.length ? " (" + num(routed.reduce(function (sum, entry) { return sum + entry.amount; }, 0)) +
          " damage routed from " + Array.from(new Set(routed.map(function (entry) { return shortSection(entry.via.section); }))).join(", ") + ")" : "";
        list.appendChild(el("li", null, shortSection(key) + ": " + num(result.health[key]) + " / " +
          num(state.vehicle.sections[key].max_health) + " HP" + note));
      });
      box.appendChild(list);
    }
    if (!result.hits.length) box.appendChild(el("p", "vv-note", "No visible collision component is reached by this blast."));
    var assumptions = el("details", "vv-impact-assumptions");
    assumptions.appendChild(el("summary", null, "Model assumptions"));
    assumptions.appendChild(el("p", "vv-note", result.orderingNote || "The first component selects the blast's health section. Native overlap order is unknown; this preview uses GLB component order."));
    assumptions.appendChild(el("p", "vv-note", "Impact point (m): " + shot.impactPosition.map(num).join(", ") + ". " +
      (shot.label === "Direct hit" ? "Selected collision surface." : "Selected isolated ground plane.")));
    assumptions.appendChild(el("p", "vv-note", "Detonation centre (m): " + shot.origin.map(num).join(", ") + "."));
    if (result.scenarioMainDamage && result.scenarioMainDamage.min !== result.scenarioMainDamage.max) {
      assumptions.appendChild(el("p", "vv-note", "First-choice examples reuse the same sampled hits. They are not exhaustive and do not bound the game's results."));
    }
    if (result.firstSectionAlternatives && result.firstSectionAlternatives.length > 1) {
      assumptions.appendChild(el("p", "vv-note", "Sampled first-hit sections: " + result.firstSectionAlternatives.map(shortSection).join(", ") + "."));
    }
    var actorNote = state.caliber.source_note || state.caliber.note;
    if (state.caliber.source_type === "actor" && actorNote) assumptions.appendChild(el("p", "vv-note", actorNote));
    if (result.tracePreferenceUnknown) {
      assumptions.appendChild(el("p", "vv-note", "This source's upward trace preference is unknown; the preview uses the ordinary cloud order."));
    }
    box.appendChild(assumptions);
  }

  function svgElement(tag, attributes) {
    var node = document.createElementNS("http://www.w3.org/2000/svg", tag);
    Object.keys(attributes).forEach(function (key) { node.setAttribute(key, attributes[key]); });
    return node;
  }

  function drawImpact() {
    var svg = els.impactOverlay, shot = state.shot;
    svg.textContent = "";
    var hidden = !shot || !placingImpact() || !!fallbackText;
    svg.toggleAttribute("hidden", hidden);
    if (hidden || !viewer.clientWidth || !viewer.clientHeight) return;
    var G = window.VehicleImpactGeometry, camera = impactCamera();
    svg.setAttribute("viewBox", "0 0 " + camera.width + " " + camera.height);
    function project(position) {
      var delta = G.sub(position, camera.position), depth = -G.dot(delta, camera.back);
      if (depth <= 0.01) return null;
      var f = camera.height / (2 * camera.tan * depth);
      return [camera.width / 2 + G.dot(delta, camera.right) * f, camera.height / 2 - G.dot(delta, camera.up) * f];
    }
    function ring(radius, plane, cls) {
      if (!(radius > 0)) return;
      var path = "", connected = false;
      for (var i = 0; i <= 80; i++) {
        var angle = i * Math.PI / 40, offset = [0, 0, 0];
        offset[plane[0]] = Math.cos(angle) * radius; offset[plane[1]] = Math.sin(angle) * radius;
        var p = project(G.add(shot.origin, offset));
        if (!p) { connected = false; continue; }
        path += (connected ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1); connected = true;
      }
      svg.appendChild(svgElement("path", { d: path, class: cls }));
    }
    [[0, 2], [0, 1], [1, 2]].forEach(function (plane) {
      ring((state.caliber.blast.radius || 0) / 100, plane, "vv-blast-outer");
      ring((state.caliber.blast.effective_radius || 0) / 100, plane, "vv-blast-effective");
    });
    shot.result.hits.forEach(function (hit) {
      var p = project(hit.position);
      if (p) svg.appendChild(svgElement("circle", { cx: p[0], cy: p[1], r: 3, class: "vv-blast-contact" }));
    });
    var origin = project(shot.origin);
    if (origin) {
      svg.appendChild(svgElement("circle", { cx: origin[0], cy: origin[1], r: 7, class: "vv-blast-origin" }));
      var label = svgElement("text", { x: origin[0] + 12, y: origin[1] - 12, class: "vv-blast-label" });
      label.textContent = "Detonation"; svg.appendChild(label);
    }
  }

  /* ---------- state changes ---------- */

  function syncBlast() {
    var explosive = !!(state.caliber && state.caliber.blast);
    els.blastField.hidden = !explosive;
    if (!explosive) state.interaction = "inspect";
    els.interaction.value = state.interaction;
    var actor = state.caliber && state.caliber.source_type === "actor";
    if (actor && state.mode === "hits") state.mode = "section";
    Array.prototype.forEach.call(els.mode.querySelectorAll("button"), function (button) {
      button.disabled = !!(actor && button.value === "hits");
      button.setAttribute("aria-checked", String(button.value === state.mode));
      button.tabIndex = button.value === state.mode ? 0 : -1;
    });
    syncImpactControls();
    prepareImpact();
  }

  function repaint() {
    if (!state.vehicle) return;
    var sc = scale();
    updateMaterials(sc);
    updateHotspots(sc);
    updateList(sc);
    updateLegend(sc);
    updatePanel();
    syncImpactControls();
    drawImpact();
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
    // Cancel browser autoscroll without blocking model-viewer's pointer controls.
    viewer.addEventListener("mousedown", function (event) {
      if (event.button === 1) event.preventDefault();
    }, true);
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
      if (placingImpact()) {
        if (!impactGeometry) return;
        // In pinned 4.3.1 getNDC subtracts the element rect despite the API's relative-pixel comment.
        var surface = viewer.positionAndNormalFromPoint(r.left + p[0], r.top + p[1]);
        var origin = surface ? [surface.position.x, surface.position.y, surface.position.z] : groundFromPixel(p);
        placeImpact(origin, surface ? "Direct hit" : "Splash");
        return;
      }
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
    ["vehicle", "caliber", "mode", "stage", "status", "fallback", "legend", "slots", "labels", "xray", "hint", "variant", "wheels", "notes", "blastField", "interaction", "impactControls", "impactHelp", "impactX", "impactZ", "groundForm", "placeGround", "clearImpact", "impactSummary", "impactOverlay"].forEach(function (k) {
      els[k] = $("vv-" + k);
    });
    els.panelBody = $("vv-panel-body");
    els.variantField = $("vv-variant-field");
    els.wheelsField = $("vv-wheels-field");
    viewer = $("vv-model");
    inspectHint = els.hint.textContent;
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
          state.caliber = sources().filter(function (c) { return c.id === els.caliber.value; })[0];
          clearImpact();
          state.interaction = state.caliber.blast ? "impact" : "inspect";
          syncBlast();
          repaint();
        });
        els.interaction.addEventListener("change", function () {
          state.interaction = els.interaction.value;
          clearImpact(); syncBlast(); repaint();
        });
        els.clearImpact.addEventListener("click", function () { clearImpact(); syncImpactControls(); });
        els.groundForm.addEventListener("submit", function (event) {
          event.preventDefault();
          if (!impactGeometry) return;
          placeImpact([els.impactX.valueAsNumber, impactGeometry.bounds.min[1], els.impactZ.valueAsNumber], "Splash");
        });
        els.labels.addEventListener("change", function () { state.labels = els.labels.checked; repaint(); });
        els.xray.addEventListener("change", function () { state.xray = els.xray.checked; repaint(); });
        document.addEventListener("keydown", function (e) {
          if (e.key === "Escape" && state.shot && !/^(INPUT|SELECT|TEXTAREA)$/.test(e.target.tagName)) {
            clearImpact(); syncImpactControls(); return;
          }
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
