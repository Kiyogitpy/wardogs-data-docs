/* Infantry hitbox viewer (infantry-viewer.md; styles in _sass/custom/infantry-viewer.scss, on top of
   the vehicle viewer's .vv-* styles). Data: assets/data/infantry-hitboxes.json
   (python _tools/infantry_tables.py --json).
   - the model is the baseline PA_TPCharacter_Simplified asset: one GLB node and one material per body, both named
     after the body's bone;
   - a bone gives a hit location (bones[].hit_location), the hit location gives the selected source's
     multiplier (sources[].zone_multiplier; null: the source doesn't use hit locations and is uniform);
   - bodies are coloured by hit location or by multiplier; an armor or helmet dims the hit locations
     it doesn't cover; a click on the model or the bone list selects a bone and the panel explains it;
   - everything the data marks as not traced (meta.not_traced, sources[].not_traced, bone_rule.runtime)
     is shown with a "Not traced" tag;
   - without WebGL, model-viewer or the model, a table takes the model's place. With JavaScript off
     the page shows the static table under .vv-nojs. Strings from the data are set as text only. */
(function () {
  "use strict";

  // Same vendored meshopt decoder as the vehicle viewer (see the note in vehicle-viewer.js).
  var MESHOPT = "assets/js/vendor/meshopt_decoder-1.2.0.js";
  var MODEL = "assets/models/infantry/player.glb";   // when the JSON has no model.path
  var MV_TIMEOUT = 15000;
  var HL = "Meta.Damage.HitLocation.Infantry.";

  // Hit locations: the dataviz reference palette's dark categorical steps and their light-mode
  // siblings that sit inside the dark band, placed so every pair of zones that touch on the body
  // clears CVD ΔE 8 and normal-vision ΔE 15 against the panel surface #18181c (checked by
  // palette_check.mjs in the preview tools). Zones that share a hue family are far apart on the
  // body, and every zone is also named in the legend, the list and the panel.
  var ZONE_COLOURS = {
    "Head": "#9085e9",
    "Neck": "#c98500",
    "Torso.Upper": "#d55181",
    "Torso.Middle": "#008300",
    "Torso.Lower": "#3987e5",
    "Pelvis": "#d95926",
    "Arm.Upper": "#256abf",
    "Arm.Lower": "#1baf7a",
    "Arm.Hand": "#6250d6",
    "Leg.Thigh": "#199e70",
    "Leg.Calf": "#2a78d6",
    "Leg.Foot": "#e34948"
  };
  var NO_ZONE = "#6c6c75";           // a body whose bone has no hit location (hatched in the legend)
  var NONE_COLOUR = "#3b3b42";       // multiplier 0: no damage (hatched)
  // Sequential blue, dark mode, as in the vehicle viewer's rule-factor mode: brighter = more damage.
  var RAMP = ["#184f95", "#1c5cab", "#256abf", "#2a78d6", "#3987e5", "#5598e7",
              "#6da7ec", "#86b6ef", "#9ec5f4", "#b7d3f6", "#cde2fb"];
  var HIGHLIGHT = "#5a5a5a";         // emissive on the selected body
  var GHOST = 0.13;                  // alpha of the other bodies while one is selected (see-through)
  var DIM_TO = "#202024", DIM = 0.85; // bodies an armor item doesn't cover: mixed this far towards the stage

  var DP = "Wardogs_DamagePipeline_v2.html";
  var SEC = {
    bone: DP + "#71-b_bonedamagemodifiers_c-entries-5-7-10",
    ammo: DP + "#73-b_ammotypeeffectiveness_c-entries-138141",
    armor: DP + "#75-wddamagemodificationoperation_playerarmordurability-entries-142144",
    perWeapon: DP + "#77-per-weapon-damage-per-bullet",
    distance: DP + "#78-damage-over-distance",
    ammoArmor: DP + "#79-ammo-type-against-armor",
    table: DP + "#81-bonedamagemodifiers-hit-location-table"
  };
  // How each category deals damage; [text, link, text, link, ...] so links stay links.
  var CATEGORIES = [
    { id: "bullets", label: "Bullets", note: [
      "A bullet's damage comes from its weapon ", ["§7.7", SEC.perWeapon], " and falls off with distance ", ["§7.8", SEC.distance],
      ". The hit-location rule then multiplies it by the Universal value for the hit location times the weapon-type row's value ",
      ["§7.1", SEC.bone], ". Armor and helmets act on bullets through ammo-type effectiveness ", ["§7.3", SEC.ammo], ", ",
      ["§7.9", SEC.ammoArmor], "."] },
    { id: "explosives", label: "Explosives and launchers", note: [
      "An explosive projectile uses its direct-hit path when it is not exploding. A blast evaluates each kept component hit separately (values below). " +
      "Whether the hit-location rule applies depends on the tags the hit carries ", ["§7.1", SEC.bone],
      "; armor and helmets cut explosive blunt damage by their reduction ", ["§7.5", SEC.armor], "."] },
    { id: "other", label: "Other (melee, impact)", note: [
      "Melee and impact damage. A source that carries a hit location uses the bone table's row for its tag ", ["§7.1", SEC.bone],
      "; one that doesn't is the same on every body part. Armor cuts melee hits by its reduction ", ["§7.5", SEC.armor], "."] }
  ];

  var HELMET_FACT = "The compiled Mutable model selects tagged physics assets by helmet, faction and view conditions. " +
    "It deduplicates selected assets, reuses a sole asset when generated bodies are unmodified, and otherwise builds " +
    "a combined asset with at most one body setup per bone. Combined-body geometry comes from the generated Mutable body; " +
    "the source setup used to create each result bone supplies selected body properties. The normal CharacterMesh override defaults to null, so its getter " +
    "uses the assigned mesh's physics asset. Runtime parameter values and later mutations are unknown. This viewer " +
    "shows PA_TPCharacter_Simplified only.";
  var TAPERED_NOTE = "The model shows the authored tapered shape. Native simple collision uses a straight capsule " +
    "with the mean of its two scaled radii; query/channel filters still apply.";
  var REMAP_NOTE = "animation and ragdoll only; not used for damage (0x6BB8D40)";

  var REPO = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/";   // data/ and sdk/ are local only, not on GitHub

  var root, data, base, els = {};
  var zones = {}, zoneOrder = {}, bonesBy = {}, entries = [], ntById = {};
  var state = { source: null, armor: null, mode: "zone", selected: null, picked: false, xray: true };
  var viewer = null, mvState = "pending", materials = [], loaded = false, fallbackText = null, range = null;

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

  function num(x) {
    if (x == null || isNaN(x)) return "?";
    var a = Math.abs(x);
    var s = a >= 100 ? x.toFixed(0) : a >= 10 ? x.toFixed(1) : a >= 1 ? x.toFixed(3) : a === 0 ? "0" : x.toPrecision(3);
    s = s.indexOf(".") >= 0 ? s.replace(/0+$/, "").replace(/\.$/, "") : s;
    return Number(s).toLocaleString("en-US", { maximumFractionDigits: 4 });
  }

  function code(text) { return el("code", null, String(text)); }

  // A dotted tag in <code> that may wrap after each dot instead of mid-word.
  function breakable(tag) {
    var c = el("code");
    String(tag).split(".").forEach(function (part, i, all) {
      c.appendChild(document.createTextNode(part + (i < all.length - 1 ? "." : "")));
      if (i < all.length - 1) c.appendChild(el("wbr"));
    });
    return c;
  }

  function docLink(href, text) {
    var a = el("a", null, text);
    a.href = /^https?:/.test(href) ? href : base + href;
    return a;
  }

  function richText(parent, parts) {
    parts.forEach(function (p) {
      if (typeof p === "string") parent.appendChild(document.createTextNode(p));
      else parent.appendChild(docLink(p[1], p[0]));
    });
    return parent;
  }

  function humanKey(k) {
    var s = String(k).replace(/_m$/, " (m)").replace(/_pct$/, " (%)").replace(/_/g, " ");
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

  // A rule entry as the data gives it: a number, a string, or an object naming one.
  function entryText(e) {
    if (e == null) return "?";
    if (typeof e !== "object") return String(e);
    var id = e.entry != null ? e.entry : e.index != null ? e.index : e.id != null ? e.id : e.row;
    var what = e.what || e.label || e.text || e.op || e.operation;
    return (id != null ? String(id) : "") + (what ? (id != null ? " " : "") + "(" + what + ")" : "");
  }

  function entryKey(e) {
    if (e == null || typeof e !== "object") return String(e);
    var id = e.entry != null ? e.entry : e.index != null ? e.index : e.id != null ? e.id : e.row;
    return String(id);
  }

  function entriesText(list) {
    return list && list.length ? list.map(entryText).join(", ") : "none";
  }

  function compact(v) {
    if (v == null) return "";
    if (typeof v === "object") { try { return JSON.stringify(v); } catch (e) { return String(v); } }
    return String(v);
  }

  /* ---------- data model ---------- */

  function zoneOf(bone) {
    var b = bonesBy[bone];
    return b && b.hit_location ? zones[b.hit_location] || { tag: b.hit_location, short: b.hit_location.replace(HL, ""), label: b.hit_location.replace(HL, "") } : null;
  }

  // model.bodies: bone names (or {bone, shapes, phys_material} records); shapes and physical
  // materials may also come as model.body_shapes / model.phys_materials maps.
  function bodyList() {
    return ((data.model && data.model.bodies) || []).map(function (b) { return typeof b === "string" ? b : b && b.bone; }).filter(Boolean);
  }

  function bodyInfo(bone) {
    var m = data.model || {}, rec = (m.bodies || []).filter(function (b) { return b && b.bone === bone; })[0] || {};
    var shapes = (m.body_shapes || {})[bone] || rec.shapes, pm = (m.phys_materials || {})[bone] || rec.phys_material;
    return shapes != null || pm ? { shapes: shapes, phys_material: pm } : null;
  }

  // sources[].not_traced: ids into meta.not_traced (or whole {id, text, data} items).
  function notTracedOf(s) {
    return (s.not_traced || []).map(function (x) { return typeof x === "string" ? ntById[x] || { id: x, text: x } : x; });
  }

  function isTapered(bone) {
    var info = bodyInfo(bone), sh = info && info.shapes;
    return /tapered/i.test(Array.isArray(sh) ? sh.join(" ") : String(sh || ""));
  }

  // bone_rule.runtime is a traced rule unless the data says otherwise (traced: false, or "not traced").
  function boneRuleTraced() {
    var r = data.bone_rule || {};
    return r.traced != null ? !!r.traced : !!r.runtime && !/not traced/i.test(r.runtime);
  }

  function categoryLabel(c) {
    var dc = (((data.meta && data.meta.categories) || []).filter(function (x) { return x.id === c.id; })[0]) || {};
    return dc.label || c.label;
  }

  function zoneLabel(z) { return z ? z.label || z.short : "no hit location"; }

  function categoryOf(s) {
    for (var i = 0; i < CATEGORIES.length; i++) if (CATEGORIES[i].id === s.category) return CATEGORIES[i];
    return CATEGORIES[CATEGORIES.length - 1];
  }

  function uniform(s) { return !s || s.zone_multiplier == null; }

  // { value, uniform, missing } for a hit location under the current source.
  function multiplier(z, s) {
    s = s || state.source;
    if (uniform(s)) return { value: 1, uniform: true, missing: false };
    if (!z) return { value: null, uniform: false, missing: true };
    var v = s.zone_multiplier[z.tag];
    return v == null ? { value: null, uniform: false, missing: true } : { value: +v, uniform: false, missing: false };
  }

  // §7.1's row lookup, to show where a multiplier comes from: the first source tag that names a row,
  // directly or by its parent; null when no tag does (then only the Universal row applies).
  function boneRowFor(s) {
    if (s.bone_row !== undefined) return s.bone_row;
    var rows = data.bone_rows || {};
    var tags = s.damage_tags || [];
    for (var i = 0; i < tags.length; i++) {
      var t = tags[i];
      if (rows[t]) return t;
      var parent = t.slice(0, t.lastIndexOf("."));
      if (parent && rows[parent]) return parent;
    }
    return null;
  }

  function breakdown(z, s) {
    var m = multiplier(z, s);
    if (m.uniform || m.missing || !z) return null;
    var u = z.universal != null ? z.universal : ((data.bone_rows || {}).Universal || {})[z.tag];
    var row = boneRowFor(s), w = row ? ((data.bone_rows[row] || {})[z.tag]) : 1;
    if (u == null || w == null || Math.abs(u * w - m.value) > 1e-3 * Math.max(1, m.value)) return null;
    return { u: u, row: row, w: w };
  }

  function covers(item, z) {
    return !!(item && z && (item.covers || []).indexOf(z.tag) >= 0);
  }

  function shared(item, s) {
    if (!item || !s) return [];
    var keys = (s.armor_entries || []).map(entryKey);
    return (item.entries || []).filter(function (e) { return keys.indexOf(entryKey(e)) >= 0; });
  }

  /* ---------- the JSON's compact encoding ---------- */

  // meta.encoding: zone_multiplier {row: R} stands for Universal × row R per hit location; factors are
  // {k} (k × that) or {zones: [12 values]}; armor {k} multiplies the unarmored factor on covered hit
  // locations; file references are an index into meta.files or [index, field]; doc and case are keys
  // of meta.docs and meta.cases. Expanded here into per-hit-location records once, on load. Data in
  // the expanded form (zone_multiplier {tag: n}, direct[].zones) passes through unchanged.
  var FILE_KEYS = { weapon: 1, stats: 1, projectile: 1, item: 1, items: 1, config: 1, src: 1, S_src: 1, fields_src: 1, path: 1 };

  function fileRef(v) {
    var files = (data.meta && data.meta.files) || [];
    if (typeof v === "number" && files[v] != null) return files[v];
    if (Array.isArray(v) && v.length === 2 && typeof v[0] === "number" && typeof v[1] === "string" && files[v[0]] != null) return files[v[0]] + ": " + v[1];
    if (Array.isArray(v)) return v.map(function (x) { if (x && typeof x === "object" && !Array.isArray(x)) { fileRefs(x); return x; } return fileRef(x); });
    if (v && typeof v === "object") fileRefs(v);
    return v;
  }

  function fileRefs(o) {
    if (Array.isArray(o)) { o.forEach(fileRefs); return; }
    if (!o || typeof o !== "object") return;
    Object.keys(o).forEach(function (k) {
      if (FILE_KEYS[k] || /_src$/.test(k)) o[k] = fileRef(o[k]);
      else fileRefs(o[k]);
    });
  }

  // B[tag] for a zone_multiplier {row: R}; null for a uniform source.
  function boneFactors(zm) {
    if (!zm || typeof zm !== "object" || !("row" in zm)) return null;
    var rows = data.bone_rows || {}, U = rows.Universal || {}, W = zm.row ? rows[zm.row] || {} : {}, out = {};
    data.hit_locations.forEach(function (z) {
      var u = U[z.tag] != null ? U[z.tag] : z.universal != null ? z.universal : 1, w = zm.row ? W[z.tag] : 1;
      out[z.tag] = +(u * (w != null ? w : 1)).toPrecision(6);
    });
    return out;
  }

  // A factor spec as {tag: factor}: {k} × B, or {zones} in hit_locations order.
  function zoneFactors(spec, B) {
    var out = {};
    data.hit_locations.forEach(function (z, i) {
      if (spec && Array.isArray(spec.zones)) out[z.tag] = spec.zones[i];
      else out[z.tag] = (spec && spec.k != null ? spec.k : 1) * (B ? B[z.tag] : 1);
    });
    return out;
  }

  function zoneEntries(ze, z) {
    if (!ze) return [];
    return ze[z.short] || ze[z.tag] || (Array.isArray(ze) ? ze[zoneOrder[z.tag]] || [] : []);
  }

  function expandArmor(armor, base, entries, ze) {
    var out = {};
    Object.keys(armor || {}).forEach(function (item) {
      var a = armor[item] || {}, it = armorById(item), per = {}, covered = data.hit_locations.filter(function (z) { return covers(it, z); });
      covered.forEach(function (z, i) {
        var f = Array.isArray(a.zones) ? (a.zones.length === data.hit_locations.length ? a.zones[zoneOrder[z.tag]] : a.zones[i])
          : base[z.tag] * (a.k != null ? a.k : 1);
        per[z.tag] = { factor: f, entries: (entries || []).concat(zoneEntries(ze, z), a.entries || []) };
      });
      out[item] = per;
    });
    return out;
  }

  function expand() {
    var cases = (data.meta && data.meta.cases) || {}, docs = (data.meta && data.meta.docs) || {};
    data.sources.forEach(function (s) {
      var v = s.values || {};
      fileRefs(v);
      if (s.doc && !/[#.\/]/.test(s.doc) && docs[s.doc]) s.doc = docs[s.doc];
      var B = boneFactors(s.zone_multiplier);
      if (s.zone_multiplier && "row" in s.zone_multiplier) {
        if (s.bone_row === undefined) s.bone_row = s.zone_multiplier.row;
        s.zone_multiplier = B;
      }
      var dz = v.direct_zones;
      if (dz && Array.isArray(v.direct)) {
        var f = zoneFactors(dz.factor, s.zone_multiplier), arm = expandArmor(dz.armor, f, dz.entries, dz.zone_entries);
        v.direct.forEach(function (c) {
          if (c.zones) return;
          c.label = c.label || cases[c.case] || c.case;
          if (c.S_src != null && !c.S_path) c.S_path = c.S_src;
          c.zones = {};
          data.hit_locations.forEach(function (z) {
            c.zones[z.tag] = { damage: c.S * f[z.tag], factor: f[z.tag], entries: (dz.entries || []).concat(zoneEntries(dz.zone_entries, z)) };
          });
          c.armor = {};
          Object.keys(arm).forEach(function (item) {
            c.armor[item] = {};
            Object.keys(arm[item]).forEach(function (t) {
              c.armor[item][t] = { damage: c.S * arm[item][t].factor, factor: arm[item][t].factor, entries: arm[item][t].entries };
            });
          });
        });
        delete v.direct_zones;
      }
      if (v.falloff && v.falloff.src !== undefined && v.falloff.path === undefined) { v.falloff.path = v.falloff.src; delete v.falloff.src; }
      var r = v.radial;
      if (r) {
        if (r.fields && r.fields_src !== undefined) {
          var fields = {};
          Object.keys(r.fields).forEach(function (k) {
            var x = r.fields[k];
            fields[k] = x && typeof x === "object" ? x : { value: x, path: r.fields_src ? r.fields_src + "." + k : null };
          });
          r.fields = fields;
          delete r.fields_src;
        }
        var RB = boneFactors(r.zone_multiplier);
        Object.keys(r.rings || {}).forEach(function (k) {
          var g = r.rings[k];
          if (!g || !g.factor || typeof g.factor !== "object") return;
          var spec = g.factor;
          var simple = !RB && spec.k != null;
          g.factor = simple ? spec.k : "varies by hit location";
          if (g.zone_entries) { g.entries_by_hit_location = g.zone_entries; delete g.zone_entries; }
          if (g.armor) {
            g.factor_with_armor_tag = {};
            Object.keys(g.armor).forEach(function (item) {
              var a = g.armor[item] || {};
              g.factor_with_armor_tag[item] = simple && a.k != null ? spec.k * a.k : a.k != null ? "×" + num(a.k) + " with this tag" : "varies by hit location";
            });
            delete g.armor;
          }
        });
        if (r.zone_multiplier && "row" in r.zone_multiplier) r.bone_row = r.zone_multiplier.row || "Universal only";
        delete r.zone_multiplier;
      }
    });
  }

  /* ---------- colours ---------- */

  function hexToRgb(h) { return [1, 3, 5].map(function (i) { return parseInt(h.substr(i, 2), 16); }); }
  function rgbToHex(c) { return "#" + c.map(function (x) { return ("0" + Math.round(x).toString(16)).slice(-2); }).join(""); }
  function mix(a, b, f) { var x = hexToRgb(a), y = hexToRgb(b); return rgbToHex(x.map(function (v, i) { return v + (y[i] - v) * f; })); }

  function ramp(t) {
    t = Math.max(0, Math.min(1, t)) * (RAMP.length - 1);
    var i = Math.min(Math.floor(t), RAMP.length - 2), f = t - i;
    var a = hexToRgb(RAMP[i]), b = hexToRgb(RAMP[i + 1]);
    return rgbToHex(a.map(function (x, k) { return x + (b[k] - x) * f; }));
  }

  // One log scale for every source, so a colour means the same multiplier whichever source is picked.
  function computeRange() {
    var vals = [1];
    data.sources.forEach(function (s) {
      if (!s.zone_multiplier) return;
      Object.keys(s.zone_multiplier).forEach(function (k) { var v = +s.zone_multiplier[k]; if (v > 0) vals.push(v); });
    });
    range = { min: Math.min.apply(null, vals), max: Math.max.apply(null, vals) };
  }

  function rampT(x) {
    if (range.max === range.min) return 1;
    return (Math.log(x) - Math.log(range.min)) / (Math.log(range.max) - Math.log(range.min));
  }

  // { colour, hatch: "" | "none" | "nozone", dim } for a bone in the current mode.
  function paint(bone) {
    var z = zoneOf(bone), dim = !!state.armor && !covers(state.armor, z);
    if (state.mode === "zone") {
      if (!z) return { colour: NO_ZONE, hatch: "nozone", dim: dim };
      return { colour: ZONE_COLOURS[z.short] || NO_ZONE, hatch: "", dim: dim };
    }
    var m = multiplier(z);
    if (m.uniform) return { colour: ramp(rampT(1)), hatch: "", dim: dim };
    if (m.missing) return { colour: NO_ZONE, hatch: "nozone", dim: dim };
    if (!(m.value > 0)) return { colour: NONE_COLOUR, hatch: "none", dim: dim };
    return { colour: ramp(rampT(m.value)), hatch: "", dim: dim };
  }

  function swatch(p) {
    var i = el("i", "vv-swatch" + (p.hatch === "none" ? " is-none" : p.hatch === "nozone" ? " is-nozone" : "") + (p.dim ? " is-dim" : ""));
    i.setAttribute("aria-hidden", "true");
    if (!p.hatch) i.style.background = p.colour;
    return i;
  }

  function multText(z, s) {
    var m = multiplier(z, s);
    if (m.uniform) return "×1 (uniform)";
    if (m.missing) return z ? "no value" : "no hit location";
    return m.value > 0 ? "×" + num(m.value) : "no damage (×0)";
  }

  /* ---------- controls ---------- */

  function fillSources() {
    var sel = els.source;
    sel.textContent = "";
    CATEGORIES.forEach(function (c) {
      var list = data.sources.filter(function (s) { return categoryOf(s) === c; });
      if (!list.length) return;
      var g = el("optgroup");
      g.label = categoryLabel(c);
      list.forEach(function (s) {
        var o = el("option", null, s.label + (s.group ? " (" + s.group + ")" : "") + (uniform(s) ? ", uniform" : ""));
        o.value = s.id;
        g.appendChild(o);
      });
      sel.appendChild(g);
    });
    sel.disabled = false;
  }

  function fillArmor() {
    var sel = els.armor;
    sel.textContent = "";
    var none = el("option", null, "None");
    none.value = "";
    sel.appendChild(none);
    [["armor", "Armor"], ["helmet", "Helmets"]].forEach(function (k) {
      var list = (data.armor || []).filter(function (a) { return a.kind === k[0]; });
      if (!list.length) return;
      var g = el("optgroup");
      g.label = k[1];
      list.forEach(function (a) {
        var o = el("option", null, a.item.replace(/^ID_/, "") + " (" + (a.reduction_pct != null ? "−" + num(a.reduction_pct) + "%" : "?") + ")");
        o.value = a.item;
        g.appendChild(o);
      });
      sel.appendChild(g);
    });
    sel.disabled = false;
  }

  function setMode(mode, focus) {
    state.mode = mode;
    Array.prototype.forEach.call(els.mode.querySelectorAll("button"), function (x) {
      x.setAttribute("aria-checked", String(x.value === mode));
      x.tabIndex = x.value === mode ? 0 : -1;
      if (focus && x.value === mode) x.focus();
    });
  }

  function setupMode() {
    var buttons = els.mode.querySelectorAll("button");
    Array.prototype.forEach.call(buttons, function (b) {
      b.addEventListener("click", function () { setMode(b.value, false); repaint(); });
    });
    els.mode.addEventListener("keydown", function (e) {
      var step = e.key === "ArrowRight" || e.key === "ArrowDown" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowUp" ? -1 : 0;
      if (!step) return;
      e.preventDefault();
      var list = Array.prototype.slice.call(buttons);
      var at = list.indexOf(els.mode.querySelector('[aria-checked="true"]'));
      setMode(list[(at + step + list.length) % list.length].value, true);
      repaint();
    });
  }

  /* ---------- bone list ---------- */

  function sortEntries() {
    entries.sort(function (a, b) {
      var za = zoneOf(a.bone), zb = zoneOf(b.bone);
      var oa = za && zoneOrder[za.tag] != null ? zoneOrder[za.tag] : 99, ob = zb && zoneOrder[zb.tag] != null ? zoneOrder[zb.tag] : 99;
      return oa - ob || a.order - b.order;
    });
  }

  function buildList() {
    var list = els.bones;
    list.textContent = "";
    sortEntries();
    entries.forEach(function (it) {
      var li = el("li"), b = el("button", "vv-slot iv-bone");
      b.type = "button";
      b.setAttribute("aria-pressed", "false");
      b.dataset.bone = it.bone;
      var name = el("span", "vv-slot-name", it.bone);
      name.appendChild(el("small", "vv-slot-group iv-bone-zone"));
      var absent = el("small", "vv-slot-absent");
      absent.hidden = true;
      name.appendChild(absent);
      b.appendChild(el("i", "vv-swatch"));
      b.appendChild(name);
      b.appendChild(el("span", "vv-slot-value"));
      b.addEventListener("click", function () { select(state.selected === it.bone ? null : it.bone, false); });
      li.appendChild(b);
      list.appendChild(li);
    });
  }

  function onModel(bone) { return materials.some(function (m) { return m.bone === bone; }); }

  // Why a listed bone has nothing to click on the model, or "" when it has a body there.
  function absence(it) {
    var e = bonesBy[it.bone];
    if (e && e.has_body === false) return "no body";
    if (loaded && !onModel(it.bone)) return "not on the model";
    return "";
  }

  function updateList() {
    Array.prototype.forEach.call(els.bones.querySelectorAll(".iv-bone"), function (b) {
      var bone = b.dataset.bone, z = zoneOf(bone), p = paint(bone);
      b.replaceChild(swatch(p), b.firstChild);
      b.querySelector(".iv-bone-zone").textContent = zoneLabel(z) + (state.armor && covers(state.armor, z) ? " · covered" : "");
      b.querySelector(".vv-slot-value").textContent = state.mode === "zone" ? (z ? z.short : "not in the hit-location map") : multText(z);
      b.setAttribute("aria-pressed", String(bone === state.selected));
      var why = absence({ bone: bone });
      b.classList.toggle("is-absent", !!why);
      var tag = b.querySelector(".vv-slot-absent");
      tag.textContent = why;
      tag.hidden = !why;
    });
  }

  /* ---------- legend ---------- */

  function key(p, label) {
    var k = el("span", "vv-key");
    k.appendChild(swatch(p));
    k.appendChild(document.createTextNode(label));
    return k;
  }

  function updateLegend() {
    var lg = els.legend, s = state.source, anyNoZone = entries.some(function (it) { return !zoneOf(it.bone); });
    lg.textContent = "";
    if (state.mode === "zone") {
      lg.appendChild(el("span", "vv-legend-title", "Hit location"));
      data.hit_locations.forEach(function (z) {
        lg.appendChild(key({ colour: ZONE_COLOURS[z.short] || NO_ZONE, hatch: "" }, zoneLabel(z)));
      });
    } else {
      lg.appendChild(el("span", "vv-legend-title", "Multiplier, " + s.label));
      if (uniform(s)) {
        lg.appendChild(key({ colour: ramp(rampT(1)), hatch: "" }, "×1 on every body part: this source doesn't use the hit location"));
      } else {
        var bar = el("span", "vv-ramp"), stops = [];
        for (var i = 0; i <= 10; i++) stops.push(ramp(i / 10));
        var track = el("span", "vv-ramp-bar iv-ramp-bar");
        track.style.background = "linear-gradient(90deg, " + stops.join(", ") + ")";
        track.setAttribute("aria-hidden", "true");
        var one = el("span", "iv-ramp-one");
        one.style.left = (rampT(1) * 100).toFixed(1) + "%";
        track.appendChild(one);
        bar.appendChild(el("span", "vv-tick", "×" + num(range.min)));
        bar.appendChild(track);
        bar.appendChild(el("span", "vv-tick", "×" + num(range.max)));
        lg.appendChild(bar);
        lg.appendChild(el("span", "vv-legend-note", "log scale, same for every source; the mark is ×1; brighter = more damage"));
        var anyZero = data.hit_locations.some(function (z) { var m = multiplier(z); return !m.missing && !(m.value > 0); });
        if (anyZero) lg.appendChild(key({ colour: NONE_COLOUR, hatch: "none" }, "no damage (×0)"));
      }
    }
    if (anyNoZone) lg.appendChild(key({ colour: NO_ZONE, hatch: "nozone" }, "no hit location"));
    if (state.armor) {
      var a = key({ colour: "#8e8e96", hatch: "", dim: true }, "dimmed: not covered by " + state.armor.item);
      lg.appendChild(a);
    }
  }

  /* ---------- panel ---------- */

  function row(dl, term, value) {
    dl.appendChild(el("dt", null, term));
    var dd = el("dd");
    if (value instanceof Node) dd.appendChild(value); else dd.textContent = value;
    dl.appendChild(dd);
  }

  // The tag already says "Not traced"; drop the same words at the start of the text.
  function untracedText(n) {
    var t = String(n.text || n.id || "").replace(/^\s*not traced\s*[:.,;-]?\s*/i, "");
    return t.charAt(0).toUpperCase() + t.slice(1);
  }

  function badge() { return el("span", "iv-badge", "Not traced"); }

  // meta.verified: facts traced since the docs were written, each with its RVAs.
  function verified(re) {
    var v = (data.meta && data.meta.verified && data.meta.verified.items) || [];
    return v.filter(function (x) { return re.test(x.id || ""); });
  }

  function tracedNote(x) {
    var p = el("p", "vv-note iv-traced-note");
    p.appendChild(el("span", "iv-badge iv-badge-traced", "Traced"));
    p.appendChild(document.createTextNode(" " + (x.text || x.id) + " "));
    (x.rvas || []).forEach(function (r, i) { if (i) p.appendChild(document.createTextNode(", ")); p.appendChild(code(r)); });
    var st = data.meta.verified.status;
    if (st) p.appendChild(el("small", "iv-untraced-users", st.charAt(0).toUpperCase() + st.slice(1) + "."));
    return p;
  }

  // One not-traced item ({id, text, data}) as a note with its tag.
  function untracedNote(n) {
    var p = el("p", "vv-note iv-untraced-note");
    p.appendChild(badge());
    p.appendChild(document.createTextNode(" " + untracedText(n)));
    if (n.data != null && n.data !== "") {
      p.appendChild(document.createTextNode(" Data: "));
      p.appendChild(inlineValue(n.data));
    }
    return p;
  }

  function meaning(m, s) {
    if (m.uniform) return "the same factor on every body part: " + s.label + " doesn't use the hit location";
    if (m.missing) return "the data gives no multiplier for this hit location";
    if (!(m.value > 0)) return "a hit here deals no damage";
    if (Math.abs(m.value - 1) < 1e-9) return "a hit here deals the damage unchanged";
    return "a hit here deals " + num(m.value) + " times the damage that reaches the hit-location rule (" +
      (m.value > 1 ? "more" : "less") + " than a ×1 location)";
  }

  // values.direct: one case per way the projectile can hit, each with per-hit-location damage.
  function directCases(s) {
    var d = s && s.values && s.values.direct;
    return Array.isArray(d) ? d.filter(function (c) { return c && c.zones; }) : [];
  }

  function caseName(c, all) { return all.length > 1 ? humanKey(c.case || "") : "Direct hit"; }

  // Built off-document and swapped in only when it changed, so the live region speaks once.
  function updatePanel() {
    var live = els.panelBody, body = el("div");
    fillPanel(body);
    if (body.innerHTML !== live.innerHTML) live.innerHTML = body.innerHTML;
  }

  function fillPanel(body) {
    var title = el("h2", "vv-panel-title no_anchor");
    body.appendChild(title);
    if (!state.selected) {
      title.className += " is-empty";
      title.textContent = "No body part selected";
      body.appendChild(el("p", "vv-panel-empty", "Click a part of the model, or pick a bone from the list below."));
      return;
    }
    var bone = state.selected, e = bonesBy[bone], z = zoneOf(bone), s = state.source, m = multiplier(z, s);
    title.textContent = bone;
    title.insertBefore(swatch(paint(bone)), title.firstChild);

    var dl = el("dl", "vv-facts");
    if (z) {
      var hl = el("span");
      hl.appendChild(document.createTextNode(zoneLabel(z) + " "));
      hl.appendChild(breakable(z.tag));
      row(dl, "Hit location", hl);
    } else {
      row(dl, "Hit location", (e ? "none: the hit-location asset gives this bone none" : "none: this bone isn't in the hit-location asset") +
        (data.bone_rule && data.bone_rule.unmapped ? ". " + data.bone_rule.unmapped.charAt(0).toUpperCase() + data.bone_rule.unmapped.slice(1) : ""));
    }
    var why = absence({ bone: bone });
    row(dl, "Body", why === "no body" ? "none in the viewer's baseline physics asset; generated runtime assets can differ"
      : why ? "listed in the data but not in this model" : loaded ? "on the model" : "…");
    var info = bodyInfo(bone);
    if (info) {
      var sh = Array.isArray(info.shapes) ? info.shapes.join(", ") : info.shapes != null ? String(info.shapes) : "";
      row(dl, "Shapes", (sh || "?") + (info.phys_material ? " · " + info.phys_material : ""));
    }
    if (e && e.impact_remap) {
      var r = el("span");
      r.appendChild(code(e.impact_remap));
      r.appendChild(document.createTextNode(": " + REMAP_NOTE));
      row(dl, "Impact remap", r);
    }
    var rule = data.bone_rule && data.bone_rule.runtime;
    if (rule && boneRuleTraced()) row(dl, "Bone match", rule);
    body.appendChild(dl);
    if (rule && !boneRuleTraced()) body.appendChild(untracedNote({ text: rule }));
    if (isTapered(bone)) body.appendChild(el("p", "vv-note", TAPERED_NOTE));

    dl = el("dl", "vv-facts");
    row(dl, "Source", s.label + (s.group ? " (" + s.group + ")" : ""));
    var mv = el("span");
    mv.appendChild(document.createTextNode(multText(z, s)));
    var bd = breakdown(z, s);
    if (bd) {
      var small = el("small", "iv-breakdown");
      small.appendChild(document.createTextNode("Universal ×" + num(bd.u) + (bd.row ? " × " : "")));
      if (bd.row) { small.appendChild(breakable(bd.row)); small.appendChild(document.createTextNode(" ×" + num(bd.w))); }
      mv.appendChild(small);
    }
    row(dl, "Hit-location multiplier", mv);
    row(dl, "What it means", meaning(m, s));
    var cases = directCases(s);
    cases.forEach(function (c) {
      var hit = z && c.zones[z.tag];
      if (!hit) return;
      var v = el("span");
      v.appendChild(document.createTextNode(num(c.S) + " × " + num(hit.factor) + " = " + num(hit.damage)));
      v.appendChild(el("small", "iv-breakdown", "entries " + entriesText(hit.entries)));
      var armored = state.armor && c.armor && c.armor[state.armor.item] && c.armor[state.armor.item][z.tag];
      if (armored) {
        v.appendChild(el("small", "iv-breakdown", "with " + state.armor.item + ": " + num(armored.damage) +
          " (×" + num(armored.factor) + ", entries " + entriesText(armored.entries) + ")"));
      }
      row(dl, "Damage per hit, " + caseName(c, cases).toLowerCase(), v);
    });
    if (state.armor) {
      var a = state.armor, cv = covers(a, z);
      row(dl, a.item, !cv ? "doesn't cover this hit location"
        : "covers it: −" + num(a.reduction_pct) + "% in the item data; the entries that apply depend on the source (armor card below)");
    }
    body.appendChild(dl);
    if (m.uniform && s.why) body.appendChild(el("p", "vv-note", s.why));

    var docs = (data.meta && data.meta.docs) || {}, links = el("p", "vv-panel-links"), first = true;
    ["bone_operation", "bone_table", "hit_locations", "armor_durability"].concat(Object.keys(docs)).filter(function (k, i, all) {
      return docs[k] && all.indexOf(k) === i;
    }).slice(0, 4).forEach(function (k) {
      if (!first) links.appendChild(document.createTextNode(" · "));
      links.appendChild(docLink(docs[k], humanKey(k)));
      first = false;
    });
    if (!first) body.appendChild(links);
  }

  /* ---------- source and armor cards ---------- */

  function isPath(v) { return typeof v === "string" && /^(data|assets|sdk|mappings|_tools)\//.test(v); }

  // "data/....json: Field.Path" -> the file, then the field. Files outside data/ and sdk/ link to GitHub.
  function pathNode(v) {
    var cut = v.indexOf(": "), file = cut < 0 ? v : v.slice(0, cut), span = el("span", "iv-path");
    var a = el(/^(data|sdk)\//.test(file) ? "code" : "a");
    if (a.tagName === "A") a.href = REPO + file;
    a.appendChild(breakable(file.replace(/^data\/Wardogs\//, "").split("/").join(".").replace(/\.json$/, "")));
    a.setAttribute("aria-label", file);
    span.appendChild(a);
    if (cut >= 0) span.appendChild(document.createTextNode(" " + v.slice(cut + 2)));
    return span;
  }

  // A value inside running text or a table cell.
  function inlineValue(v) {
    if (v == null) return document.createTextNode("—");
    if (typeof v === "number") return document.createTextNode(num(v));
    if (typeof v === "boolean") return document.createTextNode(v ? "yes" : "no");
    if (isPath(v)) return pathNode(v);
    if (typeof v === "string") return document.createTextNode(v);
    var span = el("span");
    if (Array.isArray(v)) {
      if (!v.length) span.textContent = "none";
      v.forEach(function (x, i) { if (i) span.appendChild(document.createTextNode(", ")); span.appendChild(inlineValue(x)); });
      return span;
    }
    Object.keys(v).forEach(function (k, i) {
      if (i) span.appendChild(document.createTextNode(" · "));
      span.appendChild(document.createTextNode(humanKey(k) + " "));
      span.appendChild(inlineValue(v[k]));
    });
    return span;
  }

  function table(cols, rows, numeric) {
    var wrap = el("div", "table-wrapper iv-values-table"), t = el("table"), head = t.createTHead().insertRow();
    cols.forEach(function (c, i) {
      var th = el("th", numeric && numeric[i] ? "num" : null, c);
      th.scope = "col";
      head.appendChild(th);
    });
    var tb = t.createTBody();
    rows.forEach(function (r) {
      var tr = tb.insertRow();
      if (r.cls) tr.className = r.cls;
      r.cells.forEach(function (c, i) {
        var td = tr.insertCell();
        if (numeric && numeric[i]) td.className = "num";
        td.appendChild(c instanceof Node ? c : inlineValue(c));
      });
    });
    wrap.appendChild(t);
    return wrap;
  }

  // Any other value: arrays of records as tables, records as facts, the rest inline.
  function renderValue(v) {
    if (Array.isArray(v) && v.length && v.every(function (x) { return x && typeof x === "object" && !Array.isArray(x); })) {
      var cols = [];
      v.forEach(function (x) { Object.keys(x).forEach(function (k) { if (cols.indexOf(k) < 0) cols.push(k); }); });
      return table(cols.map(humanKey), v.map(function (x) { return { cells: cols.map(function (k) { return x[k]; }) }; }),
        cols.map(function (k) { return typeof v[0][k] === "number"; }));
    }
    if (v && typeof v === "object" && !Array.isArray(v)) {
      var dl = el("dl", "vv-facts iv-facts-grid iv-values");
      Object.keys(v).forEach(function (k) { row(dl, humanKey(k), inlineValue(v[k])); });
      return dl;
    }
    return inlineValue(v);
  }

  function sub(body, text) { body.appendChild(el("h3", "iv-card-sub no_anchor", text)); }

  // values{}: the direct-hit damage per hit location, the distance falloff and the radial data get
  // their own tables; every other field is listed as it is.
  function renderValues(body, s) {
    var v = s.values || {}, special = { direct: 1, falloff: 1, radial: 1 }, rest = {};
    Object.keys(v).forEach(function (k) { if (!special[k] && v[k] != null && !(Array.isArray(v[k]) && !v[k].length)) rest[k] = v[k]; });
    if (Object.keys(rest).length) {
      var dl = el("dl", "vv-facts iv-facts-grid iv-values");
      Object.keys(rest).forEach(function (k) { row(dl, humanKey(k), Array.isArray(rest[k]) && typeof rest[k][0] === "object" ? renderValue(rest[k]) : inlineValue(rest[k])); });
      sub(body, "Values");
      body.appendChild(dl);
    }
    var cases = directCases(s);
    if (cases.length) {
      sub(body, "Damage per hit, by hit location");
      var ul = el("ul", "iv-cases");
      cases.forEach(function (c) {
        var li = el("li");
        var name = caseName(c, cases), label = String(c.label || "");
        if (label.toLowerCase().indexOf(name.toLowerCase() + ":") === 0) label = label.slice(name.length + 1).trim();
        li.appendChild(el("strong", null, name + ": "));
        li.appendChild(document.createTextNode(label + (c.S != null ? " (S = " + num(c.S) + ")" : "")));
        if (c.S_path) { li.appendChild(document.createTextNode(" ")); li.appendChild(pathNode(c.S_path)); }
        ul.appendChild(li);
      });
      body.appendChild(ul);
      var item = state.armor, cols = ["Hit location"], numeric = [false];
      cases.forEach(function (c) {
        cols.push(caseName(c, cases) + " (×factor)"); numeric.push(true);
        if (item) { cols.push("with " + item.item.replace(/^ID_/, "")); numeric.push(true); }
      });
      cols.push("Entries"); numeric.push(false);
      var sel = zoneOf(state.selected);
      var rows = data.hit_locations.map(function (z) {
        var cells = [zoneLabel(z)], ents = [];
        cases.forEach(function (c) {
          var h = c.zones[z.tag];
          cells.push(h ? num(h.damage) + " (×" + num(h.factor) + ")" : "—");
          if (h) ents.push(entriesText(h.entries));
          if (item) {
            var a = c.armor && c.armor[item.item] && c.armor[item.item][z.tag];
            cells.push(a ? num(a.damage) + " (" + entriesText(a.entries) + ")" : covers(item, z) ? "?" : "not covered");
          }
        });
        cells.push(ents.filter(function (x, i) { return ents.indexOf(x) === i; }).join(" / "));
        return { cells: cells, cls: sel && sel.tag === z.tag ? "is-selected" : "" };
      });
      body.appendChild(table(cols, rows, numeric));
    }
    var f = v.falloff;
    if (f && ((f.points && f.points.length) || (f.keys_m && f.keys_m.length))) {
      sub(body, "Damage over distance");
      var lead = el("p", "iv-card-lead");
      if (f.keys_m && f.keys_m.length) {
        lead.appendChild(document.createTextNode("Curve keys (m → factor): " + f.keys_m.map(function (k) { return num(k[0]) + " → " + num(k[1]); }).join(", ") +
          (f.cubic ? " (cubic)" : " (linear)") + ". "));
      } else lead.appendChild(document.createTextNode("No distance curve: the factor stays 1. "));
      if (f.path) lead.appendChild(pathNode(f.path));
      body.appendChild(lead);
      if (f.points && f.points.length) body.appendChild(renderValue(f.points));
      else if (f.keys_m && f.keys_m.length && !f.cubic) body.appendChild(falloffTable(f.keys_m, s));
    }
    var r = v.radial;
    if (r && typeof r === "object") {
      sub(body, "Blast (radial path)");
      if (r.fields) {
        body.appendChild(table(["Field", "Value", "From"], Object.keys(r.fields).map(function (k) {
          var x = r.fields[k] || {};
          return { cells: [k, x.value, x.path ? pathNode(x.path) : "—"] };
        }), [false, true, false]));
      }
      if (r.rings) {
        var item2 = state.armor;
        body.appendChild(table(["Ring", "Tag", "Factor", "Entries"].concat(item2 ? ["with " + item2.item.replace(/^ID_/, "")] : []),
          Object.keys(r.rings).map(function (k) {
            var g = r.rings[k] || {}, cells = [humanKey(k), g.tag ? breakable(g.tag) : "—", typeof g.factor === "number" ? "×" + num(g.factor) : g.factor, entriesText(g.entries)];
            var fa = g.factor_with_armor_tag && g.factor_with_armor_tag[item2 && item2.item];
            if (item2) cells.push(typeof fa === "number" ? "×" + num(fa) : fa != null ? String(fa) : "—");
            return { cells: cells };
          }), [false, false, true, false, true]));
      }
      var other = {};
      Object.keys(r).forEach(function (k) { if (k !== "fields" && k !== "rings" && r[k] != null && !(Array.isArray(r[k]) && !r[k].length)) other[k] = r[k]; });
      Object.keys(r.rings || {}).forEach(function (k) { if (r.rings[k] && r.rings[k].entries_by_hit_location) other[humanKey(k) + " ring, extra entries by hit location"] = r.rings[k].entries_by_hit_location; });
      if (Object.keys(other).length) body.appendChild(renderValue(other));
    }
  }

  // The distance curve read between its keys (linear), with the first direct case's damage on the
  // selected body's hit location (else the upper torso).
  function falloffAt(keys, m) {
    if (m <= keys[0][0]) return keys[0][1];
    for (var i = 1; i < keys.length; i++) {
      if (m <= keys[i][0]) {
        var a = keys[i - 1], b = keys[i];
        return b[0] === a[0] ? b[1] : a[1] + (b[1] - a[1]) * (m - a[0]) / (b[0] - a[0]);
      }
    }
    return keys[keys.length - 1][1];
  }

  function falloffTable(keys, s) {
    var ms = [50, 100, 200, 400, 800, 1200];
    keys.forEach(function (k) { if (k[0] > 0 && ms.indexOf(k[0]) < 0) ms.push(k[0]); });
    ms.sort(function (a, b) { return a - b; });
    var c = directCases(s)[0], z = zoneOf(state.selected) || zones[HL + "Torso.Upper"] || data.hit_locations[0];
    var hit = c && z && c.zones[z.tag];
    var cols = ["Distance (m)", "Factor"].concat(hit ? ["Damage, " + zoneLabel(z).toLowerCase()] : []);
    return table(cols, ms.map(function (m) {
      var f = falloffAt(keys, m);
      return { cells: [m, f].concat(hit ? [hit.damage * f] : []) };
    }), [true, true, true]);
  }

  function tagList(tags) {
    var span = el("span", "iv-tags");
    (tags || []).forEach(function (t, i) {
      if (i) span.appendChild(document.createTextNode(", "));
      span.appendChild(breakable(t));
    });
    if (!tags || !tags.length) span.textContent = "none";
    return span;
  }

  // meta.entries: what each rule entry of DT_GlobalDamage_InfantryData requires and does.
  function entryDetails(list, summary) {
    var all = (data.meta && data.meta.entries) || {};
    var known = (list || []).filter(function (e) { return all[entryKey(e)]; });
    if (!known.length) return null;
    var d = el("details", "iv-entries");
    d.appendChild(el("summary", null, summary));
    var ul = el("ul");
    known.forEach(function (e) {
      var x = all[entryKey(e)], li = el("li");
      li.appendChild(el("strong", null, entryKey(e) + ": "));
      var parts = [];
      ["source", "target", "hit", "alignment"].forEach(function (k) { if (x[k] && x[k] !== "—" && x[k] !== "None") parts.push(k + " " + x[k]); });
      li.appendChild(document.createTextNode((parts.length ? parts.join(", ") + " → " : "") + (x.change || "")));
      ul.appendChild(li);
    });
    d.appendChild(ul);
    return d;
  }

  function categoryNote(c) {
    var cats = (data.meta && data.meta.categories) || [];
    var dc = cats.filter(function (x) { return x.id === c.id; })[0];
    return dc && dc.note ? el("p", "iv-card-lead", dc.note) : richText(el("p", "iv-card-lead"), c.note);
  }

  function updateSourceCard() {
    var body = els.sourceBody, s = state.source, c = categoryOf(s);
    body.textContent = "";
    var head = el("p", "iv-card-name");
    head.appendChild(el("strong", null, s.label));
    head.appendChild(el("span", "iv-card-kind", categoryLabel(c) + (s.group ? " · " + s.group : "")));
    body.appendChild(head);
    body.appendChild(categoryNote(c));
    if (uniform(s)) body.appendChild(el("p", "vv-note", "Same factor on every body part. " + (s.why || "The data gives no reason.")));
    else if (s.why) body.appendChild(el("p", "iv-card-lead", s.why));
    var v = s.values || {}, key = s.id + " " + (s.group || "") + " " + s.label;
    var ids = [];
    if (v.radial || (s.radial_entries && s.radial_entries.length)) ids.push(/^radial-hits$/, /^blunt-direct-only$/);
    if (/back.?blast/i.test(key)) ids.push(/back/);
    if (/thrown/i.test(key)) ids.push(/thrown/);
    ids.forEach(function (re) { verified(re).forEach(function (x) { body.appendChild(tracedNote(x)); }); });
    var dl = el("dl", "vv-facts iv-facts-grid");
    row(dl, "Damage tags", tagList(s.damage_tags));
    row(dl, "Uses the hit location", s.uses_hit_location ? "yes" : "no");
    var br = boneRowFor(s);
    if (!uniform(s)) row(dl, "Bone table row", br ? breakable(br) : "none: Universal only");
    row(dl, "Rule entries", entriesText(s.rule_entries));
    row(dl, "Armor entries", entriesText(s.armor_entries));
    if (s.radial_uses_hit_location != null) row(dl, "Blast uses the hit location", s.radial_uses_hit_location ? "yes" : "no");
    if (s.radial_entries && s.radial_entries.length) row(dl, "Blast entries", entriesText(s.radial_entries));
    if (s.friendly_entries && s.friendly_entries.length) row(dl, "Friendly-fire entries", entriesText(s.friendly_entries));
    body.appendChild(dl);
    var det = entryDetails((s.rule_entries || []).concat(s.armor_entries || [], s.radial_entries || [], s.friendly_entries || []).filter(function (x, i, all) {
      return all.map(entryKey).indexOf(entryKey(x)) === i;
    }), "What these entries do");
    if (det) body.appendChild(det);
    renderValues(body, s);
    var nts = notTracedOf(s);
    if (nts.length) {
      sub(body, "Not traced for this source");
      nts.forEach(function (n) { body.appendChild(untracedNote(n)); });
    }
    if (s.doc) {
      var p = el("p", "vv-panel-links");
      p.appendChild(docLink(s.doc, "How this source is traced"));
      body.appendChild(p);
    }
  }

  function updateArmorCard() {
    var body = els.armorBody, a = state.armor, s = state.source;
    body.textContent = "";
    if (!a) {
      body.appendChild(el("p", "iv-card-lead", "None selected. Pick an armor or helmet to see the hit locations it covers; the model dims the rest."));
      return;
    }
    var head = el("p", "iv-card-name");
    head.appendChild(el("strong", null, a.item));
    head.appendChild(el("span", "iv-card-kind", a.kind === "helmet" ? "Helmet" : "Armor"));
    body.appendChild(head);
    var dl = el("dl", "vv-facts iv-facts-grid");
    row(dl, "Context tag", breakable(a.tag));
    var cov = (a.covers || []).map(function (t) { return zoneLabel(zones[t] || { short: t.replace(HL, "") }); });
    row(dl, "Covers", cov.length ? cov.join(", ") : "nothing");
    row(dl, "Reduction", a.reduction_pct != null ? "−" + num(a.reduction_pct) + "% (×" + num(1 - a.reduction_pct / 100) + ")" : "?");
    if (a.stage_reductions && a.stage_reductions.length) row(dl, "Per durability stage", a.stage_reductions.map(function (x) { return "−" + num(x) + "%"; }).join(", "));
    row(dl, "Max durability", a.max_durability != null ? num(a.max_durability) : "none");
    row(dl, "Rule entries", entriesText(a.entries));
    if (a.custom_entries && a.custom_entries.length) row(dl, "Custom operations", entriesText(a.custom_entries));
    body.appendChild(dl);
    var det = entryDetails(a.entries, "What these entries do");
    if (det) body.appendChild(det);

    // With the selected source: the covered hit locations' damage per hit with and without the item.
    sub(body, "With " + s.label);
    var cases = directCases(s), covered = data.hit_locations.filter(function (z) { return covers(a, z); });
    if (!covered.length) {
      body.appendChild(el("p", "iv-card-lead", "This item covers no hit location, so no armor rule reaches the hit."));
    } else if (cases.length) {
      var c = cases[0], rows = covered.map(function (z) {
        var h = c.zones[z.tag], w = c.armor && c.armor[a.item] && c.armor[a.item][z.tag];
        return { cells: [zoneLabel(z), h ? h.damage : null, w ? w.damage : null, w ? entriesText(w.entries) : "?"] };
      });
      body.appendChild(table(["Hit location", "Without", "With", "Entries"], rows, [false, true, true, false]));
      body.appendChild(el("p", "iv-card-lead", caseName(c, cases) + (c.S != null ? ", S = " + num(c.S) : "") + "."));
    } else {
      var sh = shared(a, s);
      body.appendChild(el("p", "iv-card-lead", sh.length ? "Entries shared with this source's armor entries: " + entriesText(sh) + "."
        : "None of this item's entries are among this source's armor entries (" + entriesText(s.armor_entries) + ")."));
    }
    if (a.kind === "helmet") {
      body.appendChild(el("p", "iv-card-lead", HELMET_FACT));
    }
    if (a.path) {
      var p = el("p", "vv-panel-links");
      p.appendChild(document.createTextNode("Item data: "));
      p.appendChild(isPath(a.path) ? pathNode(a.path) : breakable(a.path));
      body.appendChild(p);
    }
  }

  // Every not-traced item once: meta.not_traced, the bone rule's runtime, and source-only items.
  function updateUntraced() {
    var list = els.untracedList, items = [];
    list.textContent = "";
    ((data.meta && data.meta.not_traced) || []).forEach(function (n) { items.push({ n: n, title: null }); });
    if (data.bone_rule && data.bone_rule.runtime && !boneRuleTraced()) items.push({ n: { text: data.bone_rule.runtime, data: data.bone_rule.data }, title: "Bone to hit location" });
    data.sources.forEach(function (s) {
      (s.not_traced || []).forEach(function (x) { if (typeof x === "object" && !(x.id && ntById[x.id])) items.push({ n: x, title: s.label }); });
    });
    items.forEach(function (it) {
      var li = el("li"), n = it.n;
      li.appendChild(badge());
      li.appendChild(document.createTextNode(" "));
      if (it.title) li.appendChild(el("strong", null, it.title + ": "));
      li.appendChild(document.createTextNode(untracedText(n)));
      if (n.data != null && n.data !== "") {
        li.appendChild(document.createTextNode(" Data: "));
        li.appendChild(inlineValue(n.data));
      }
      if (n.id) {
        var users = data.sources.filter(function (s) { return (s.not_traced || []).some(function (x) { return (typeof x === "string" ? x : x.id) === n.id; }); });
        if (users.length) li.appendChild(el("small", "iv-untraced-users", "Affects " + users.length + (users.length === 1 ? " source: " : " sources: ") +
          users.slice(0, 6).map(function (s) { return s.label; }).join(", ") + (users.length > 6 ? " and " + (users.length - 6) + " more" : "") + "."));
      }
      list.appendChild(li);
    });
    var as = (data.meta && data.meta.assumptions) || [], ver = (data.meta && data.meta.verified) || null;
    els.assumptions.textContent = "";
    if (ver && ver.items && ver.items.length) {
      els.assumptions.appendChild(el("h3", "iv-card-sub no_anchor", "Traced" + (ver.status ? " (" + ver.status + ")" : "")));
      var vl = el("ul", "iv-assumptions iv-verified");
      ver.items.forEach(function (x) {
        var li = el("li", null, (x.text || x.id || "") + " ");
        (x.rvas || []).forEach(function (r, i) { if (i) li.appendChild(document.createTextNode(", ")); li.appendChild(code(r)); });
        vl.appendChild(li);
      });
      els.assumptions.appendChild(vl);
    }
    if (as.length) {
      els.assumptions.appendChild(el("h3", "iv-card-sub no_anchor", "Assumptions"));
      var ul = el("ul", "iv-assumptions");
      as.forEach(function (x) { ul.appendChild(el("li", null, compact(x))); });
      els.assumptions.appendChild(ul);
    }
    els.untraced.hidden = !items.length && !as.length;
  }

  /* ---------- model ---------- */

  function webgl() {
    try {
      var c = document.createElement("canvas");
      return !!(window.WebGLRenderingContext && (c.getContext("webgl2") || c.getContext("webgl")));
    } catch (e) { return false; }
  }

  function whenModelViewer() {
    return new Promise(function (resolve, reject) {
      if (!webgl()) { reject(new Error("WebGL is not available in this browser")); return; }
      if (!window.customElements) { reject(new Error("this browser has no custom elements")); return; }
      var started = Date.now();
      var poll = setInterval(function () {
        if (document.documentElement.classList.contains("iv-mv-failed")) {
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

  function updateNotes() {
    var box = els.notes, m = data.model;
    box.textContent = "";
    if (m) {
      var p = el("p");
      p.appendChild(document.createTextNode("Physics asset "));
      p.appendChild(code(m.physics_asset || "?"));
      p.appendChild(document.createTextNode(" · " + bodyList().length + " bodies"));
      box.appendChild(p);
      // The model's notes (how it was built, what it leaves out) fold away: they are long.
      var notes = (m.notes || []).filter(Boolean);
      if (notes.length) {
        var d = el("details", "iv-model-notes");
        d.appendChild(el("summary", null, "About this model (" + notes.length + (notes.length === 1 ? " note)" : " notes)")));
        notes.forEach(function (n) { d.appendChild(el("p", null, compact(n))); });
        box.appendChild(d);
      }
    }
    box.hidden = !box.childNodes.length;
  }

  function showFallback(reason) {
    fallbackText = reason;
    els.stage.classList.add("is-fallback");
    els.fallback.hidden = false;
    els.fallback.textContent = "";
    els.fallback.appendChild(el("p", "vv-fallback-note", reason));
    var wrap = el("div", "table-wrapper"), t = el("table"), s = state.source;
    var cols = ["Bone", "Hit location", "Multiplier (" + s.label + ")"];
    if (state.armor) cols.push(state.armor.item);
    var head = t.createTHead().insertRow();
    cols.forEach(function (h, i) {
      var th = el("th", i === 2 ? "num" : null, h);
      th.scope = "col";
      head.appendChild(th);
    });
    var tb = t.createTBody();
    entries.forEach(function (it) {
      var r = tb.insertRow(), z = zoneOf(it.bone), why = absence(it);
      var c0 = r.insertCell();
      c0.appendChild(code(it.bone));
      if (why) c0.appendChild(document.createTextNode(" (" + why + ")"));
      r.insertCell().textContent = z ? zoneLabel(z) + " (" + z.short + ")" : "none";
      var c2 = r.insertCell();
      c2.className = "num";
      c2.textContent = multText(z, s);
      if (state.armor) r.insertCell().textContent = covers(state.armor, z) ? "covered, −" + num(state.armor.reduction_pct) + "%" : "not covered";
    });
    wrap.appendChild(t);
    els.fallback.appendChild(wrap);
    if (uniform(s) && s.why) els.fallback.appendChild(el("p", "vv-note", s.why));
  }

  function hideFallback() {
    fallbackText = null;
    els.stage.classList.remove("is-fallback");
    els.fallback.hidden = true;
    els.fallback.textContent = "";
  }

  function loadModel() {
    materials = [];
    loaded = false;
    if (mvState === "pending") { status("Loading the 3D viewer…"); return; }
    if (mvState !== "ok" || !data.model) {
      status("");
      showFallback(mvState !== "ok" ? "The 3D view is unavailable (" + mvState + "). The bones and their hit locations:"
        : "No physics-asset model has been exported yet. The bones and their hit locations:");
      return;
    }
    hideFallback();
    status("Loading the physics bodies…");
    var src = base + (data.model.path || MODEL);
    if (viewer.getAttribute("src") === src && viewer.loaded) onLoad();
    else viewer.setAttribute("src", src);
  }

  function onLoad() {
    if (!viewer.model) return;
    materials = viewer.model.materials.map(function (m) {
      try {
        m.pbrMetallicRoughness.setMetallicFactor(0);
        m.pbrMetallicRoughness.setRoughnessFactor(0.85);
      } catch (e) { /* keep the file's values */ }
      return { material: m, bone: m.name };
    });
    loaded = true;
    // Bodies whose bone the data doesn't list still get an entry (no hit location).
    var known = {};
    entries.forEach(function (it) { known[it.bone] = true; });
    var added = false;
    materials.forEach(function (m) {
      if (!known[m.bone]) { known[m.bone] = true; entries.push({ bone: m.bone, order: 1000 + entries.length }); added = true; }
    });
    if (added) buildList();
    frame();
    repaint();
    status("");
  }

  // Fit the model's bounding box to the stage from the default view angle (as the vehicle viewer).
  var THETA = 25, PHI = 80, MARGIN = 1.08;
  function frame() {
    try {
      var size = viewer.getDimensions(), w = viewer.clientWidth, h = viewer.clientHeight;
      var fov = viewer.getFieldOfView() * Math.PI / 180;
      if (!size || !w || !h || !(fov > 0)) return;
      var t = THETA * Math.PI / 180, ph = PHI * Math.PI / 180;
      var d = [Math.sin(ph) * Math.sin(t), Math.cos(ph), Math.sin(ph) * Math.cos(t)];
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
    showFallback("The physics-asset model could not be loaded. The bones and their hit locations:");
  }

  function linear(hex) {
    return hexToRgb(hex).map(function (c) {
      c /= 255;
      return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
  }

  function ghosting() { return state.xray && !!state.selected && materials.some(function (m) { return m.bone === state.selected; }); }

  function updateMaterials() {
    var ghost = ghosting();
    materials.forEach(function (m) {
      var selected = m.bone === state.selected, faded = ghost && !selected, p = paint(m.bone);
      var colour = p.dim ? mix(p.colour, DIM_TO, DIM) : p.colour;
      try {
        m.material.setAlphaMode(faded ? "BLEND" : "OPAQUE");
        m.material.pbrMetallicRoughness.setBaseColorFactor(linear(colour).concat([faded ? GHOST : 1]));
        m.material.setEmissiveFactor(selected ? HIGHLIGHT : "#000000");
      } catch (e) { /* material not ready */ }
    });
  }

  /* ---------- state changes ---------- */

  function repaint() {
    if (!data) return;
    updateMaterials();
    updateList();
    updateLegend();
    updatePanel();
    updateSourceCard();
    updateArmorCard();
    if (fallbackText) showFallback(fallbackText);
    if (viewer) {
      viewer.alt = "Physics-asset bodies of the player character, coloured by " +
        (state.mode === "zone" ? "hit location" : state.source.label + " multiplier") +
        (state.armor ? ", " + state.armor.item + " coverage highlighted" : "") +
        (state.selected ? ", " + state.selected + " selected" : "");
    }
  }

  function select(bone, picked) {
    state.selected = bone;
    state.picked = !!bone && picked;
    repaint();
  }

  function sourceById(id) { return data.sources.filter(function (s) { return s.id === id; })[0] || null; }
  function armorById(id) { return (data.armor || []).filter(function (a) { return a.item === id; })[0] || null; }

  // "#<source id>" or "#<source id>/<armor item>".
  function parseHash() {
    var h = decodeURIComponent(location.hash.slice(1)), cut = h.indexOf("/");
    return cut < 0 ? { source: h, armor: null } : { source: h.slice(0, cut), armor: h.slice(cut + 1) };
  }

  function writeHash() {
    var h = "#" + state.source.id + (state.armor ? "/" + state.armor.item : "");
    if (location.hash === h || decodeURIComponent(location.hash) === h) return;
    try { history.replaceState(null, "", h); } catch (e) { location.hash = h; }
  }

  function applyHash(fromLoad) {
    var h = parseHash(), s = sourceById(h.source);
    if (!s) return false;
    state.source = s;
    state.armor = armorById(h.armor);
    els.source.value = s.id;
    els.armor.value = state.armor ? state.armor.item : "";
    if (!fromLoad) setMode("mult", false);
    return true;
  }

  /* ---------- picking ---------- */

  function setupPicking() {
    var down = null;
    function at(e) { var r = viewer.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; }
    viewer.addEventListener("pointerdown", function (e) { down = at(e); });
    viewer.addEventListener("click", function (e) {
      if (!materials.length) return;
      var up = at(e);
      if (down && Math.abs(up[0] - down[0]) + Math.abs(up[1] - down[1]) > 6) return;   // a drag
      var r = viewer.getBoundingClientRect(), p = down || up;
      var m = viewer.materialFromPoint(r.left + p[0], r.top + p[1]);
      if (!m) { if (state.selected) select(null, false); return; }
      var hit = materials.filter(function (x) { return x.material === m || x.material.index === m.index; })[0];
      if (!hit) return;
      // Bodies don't enclose each other, so a click on a see-through body selects it.
      select(hit.bone === state.selected ? null : hit.bone, true);
    });
  }

  /* ---------- start ---------- */

  function index() {
    zones = {}; zoneOrder = {}; bonesBy = {}; entries = [];
    data.hit_locations.forEach(function (z, i) { zones[z.tag] = z; zoneOrder[z.tag] = i; });
    (data.bones || []).forEach(function (b, i) {
      bonesBy[b.bone] = b;
      entries.push({ bone: b.bone, order: i });
    });
    bodyList().forEach(function (b) {
      if (!bonesBy[b] && !entries.some(function (x) { return x.bone === b; })) entries.push({ bone: b, order: 500 + entries.length });
    });
    ntById = {};
    ((data.meta && data.meta.not_traced) || []).forEach(function (n) { if (n && n.id) ntById[n.id] = n; });
  }

  ready(function () {
    root = $("iv");
    if (!root) return;
    base = root.getAttribute("data-base") || "/";
    ["source", "armor", "mode", "stage", "status", "fallback", "legend", "bones", "xray", "notes", "untraced"].forEach(function (k) {
      els[k] = $("iv-" + k);
    });
    els.panelBody = $("iv-panel-body");
    els.sourceBody = $("iv-source-body");
    els.armorBody = $("iv-armor-body");
    els.untracedList = $("iv-untraced-list");
    els.assumptions = $("iv-assumptions");
    viewer = $("iv-model");
    status("Loading the hitbox data…");

    fetch(root.getAttribute("data-json"))
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (json) {
        data = json;
        if (!data.sources || !data.sources.length || !data.hit_locations) throw new Error("no sources in the data");
        index();
        expand();
        computeRange();
        fillSources();
        fillArmor();
        setupMode();
        if (!applyHash(false)) {   // a linked source opens coloured by its multiplier
          state.source = data.sources[0];
          els.source.value = state.source.id;
        }
        els.source.addEventListener("change", function () {
          state.source = sourceById(els.source.value) || state.source;
          setMode("mult", false);
          writeHash();
          repaint();
        });
        els.armor.addEventListener("change", function () {
          state.armor = armorById(els.armor.value);
          writeHash();
          repaint();
        });
        els.xray.addEventListener("change", function () { state.xray = els.xray.checked; repaint(); });
        document.addEventListener("keydown", function (e) {
          if (e.key !== "Escape" || !state.selected || e.target.tagName === "SELECT") return;
          select(null, false);
        });
        window.addEventListener("hashchange", function () { if (applyHash(false)) repaint(); });
        viewer.addEventListener("load", onLoad);
        viewer.addEventListener("error", onError);
        setupPicking();
        buildList();
        updateNotes();
        updateUntraced();
        loadModel();
        repaint();
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
