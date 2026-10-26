/* Weapon Loadout Calculator (loadout-calculator.md; styles in _sass/custom/loadout-calculator.scss, on top
   of the vehicle viewer's .vv-* styles). UI only: every rule (which sub-slots a choice opens, what a
   slot accepts, the sight entries, the bipod lists, the evaluation and the command-line equivalent)
   comes from window.WDLoadout (assets/js/loadout-eval.js, loaded before this file), the browser twin of
   _tools/weapon_attributes.py. Data: assets/data/weapon-loadouts.json (weapon_attributes.py --json).
   - one select per open sub-slot, listing what the slot accepts plus "Empty";
   - sight, stance and bipod (the bipod switch is enabled only while a bipod is equipped);
   - the attribute table (base, each modifier, final; changed values highlighted), the character
     effects and the notes; a deep link in the hash; the equivalent command line.
   Extras from assets/data/loadout-extras.json (_tools/loadout_extras.py; optional, the page works without it):
   - class and class level: items in a role unlock tree above the level (or only in another class's tree)
     are disabled in the pickers and marked with the class and level that unlock them;
   - the equipped sights' reticles (through the scope, and the lens reticle of the active sight entry);
   - ammunition, target vest and helmet, distance: damage per body part, shots and time to kill (100 HP),
     and the damage drop-off over distance.
   With JavaScript off the page shows the .vv-nojs note instead. Strings from the data are set as text. */
(function () {
  "use strict";

  var CMD = "python -I _tools/weapon_attributes.py ";
  var OP_NAMES = { Add: "Add", Multiply: "Multiply", Divide: "Divide", MultiplyCompound: "MultiplyCompound",
                   AddFinal: "AddFinal", Override: "Override" };

  var L, model, root, els = {}, lo = null, defEval = null, dropped = [], copyTimer = null;
  var X = null, base = "/", gate = { role: "", level: null }, bal = { ammo: null, vest: "None", helmet: "None", range: 0 };

  // Player-facing names for the extras.
  var PART_NAMES = { "Head": "Head", "Neck": "Neck", "Torso.Upper": "Upper torso", "Torso.Middle": "Middle torso",
                     "Torso.Lower": "Lower torso", "Pelvis": "Pelvis", "Arm.Upper": "Upper arm", "Arm.Lower": "Forearm",
                     "Arm.Hand": "Hand", "Leg.Thigh": "Thigh", "Leg.Calf": "Calf", "Leg.Foot": "Foot" };
  var VESTS = [["None", "No vest"], ["Light", "Level 1 vest"], ["Medium", "Level 2 vest"], ["Heavy", "Level 3 vest"],
               ["SuperHeavy", "Level 4 vest"]];
  var HELMETS = [["None", "No helmet"], ["Light", "Level 1 helmet"], ["Medium", "Level 2 helmet"], ["Heavy", "Level 3 helmet"],
                 ["SuperHeavy", "Level 4 helmet"], ["Pilot", "Pilot helmet"], ["Tank", "Tank crew helmet"]];
  var DROP_PARTS = ["Head", "Torso.Upper", "Arm.Upper", "Leg.Thigh"];

  function $(id) { return document.getElementById(id); }
  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function fmt(x, digits) { return L.fmt(x, digits); }

  // Text with `code` spans (the evaluator's notes use backticks) as text nodes and <code> elements.
  function richText(parent, text) {
    String(text).split(/(`[^`]*`)/).forEach(function (part) {
      if (part.length > 1 && part.charAt(0) === "`" && part.charAt(part.length - 1) === "`") parent.appendChild(el("code", null, part.slice(1, -1)));
      else if (part) parent.appendChild(document.createTextNode(part));
    });
  }

  /* ---------- model access ---------- */

  function weapons() { return model.weapons || []; }
  function weaponById(id) { return weapons().filter(function (w) { return w.id === id; })[0] || null; }
  function item(id) { return (model.items && model.items[id]) || null; }
  function display(id) { var it = item(id); return (it && it.display) || String(id); }
  function itemLabel(id) { var it = item(id); return it && it.display ? it.display + " (" + id + ")" : String(id); }
  function weaponLabel(w) { return w.display ? w.display + " (" + w.id + ")" : w.id; }
  function defaultSight() { return model.defaultSight || "S_Aim01"; }
  function stances() { return model.stances || ["Stand", "Crouch", "Prone"]; }
  function bipodStates() { return model.bipodStates || ["folded", "unfolded", "mounted"]; }

  /* ---------- loadout ---------- */

  function load(weaponId) {
    lo = L.defaultLoadout(model, weaponId);
    defEval = L.evaluate(model, L.defaultLoadout(model, weaponId));
    dropped = [];
  }

  function isDefault() {
    return lo.sight == null && lo.stance === stances()[0] && lo.bipod === bipodStates()[0] &&
      L.slots(model, lo).every(function (s) { return s.isDefault; });
  }

  // The bipod lists apply only with a bipod equipped: without one the switch goes back to folded.
  function settle() {
    if (!L.hasBipod(model, lo)) lo.bipod = bipodStates()[0];
    if (lo.sight != null && !L.sights(model, lo).some(function (s) { return s.name === lo.sight; })) lo.sight = null;
  }

  /* ---------- hash: #w=<weapon>&<slot key>=<item|none>&sight=…&stance=…&bipod=… ----------
     Only what differs from the defaults is written; a missing slot key means the slot's default. */

  var RESERVED = { w: 1, sight: 1, stance: 1, bipod: 1, cls: 1, lvl: 1, ammo: 1, vest: 1, helmet: 1, range: 1 };

  function writeHash() {
    var p = ["w=" + encodeURIComponent(lo.weapon)];
    L.slots(model, lo).forEach(function (s) {
      if (!s.isDefault) p.push(encodeURIComponent(s.key) + "=" + encodeURIComponent(s.choice == null ? "none" : s.choice));
    });
    if (lo.sight != null) p.push("sight=" + encodeURIComponent(lo.sight));
    if (lo.stance !== stances()[0]) p.push("stance=" + encodeURIComponent(lo.stance));
    if (lo.bipod !== bipodStates()[0]) p.push("bipod=" + encodeURIComponent(lo.bipod));
    if (gate.role) p.push("cls=" + encodeURIComponent(gate.role));
    if (gate.level != null) p.push("lvl=" + gate.level);
    var ba = ballistics();
    if (ba && bal.ammo && ba.ammo.length && bal.ammo !== ba.ammo[0].id) p.push("ammo=" + encodeURIComponent(bal.ammo));
    if (bal.vest !== "None") p.push("vest=" + encodeURIComponent(bal.vest));
    if (bal.helmet !== "None") p.push("helmet=" + encodeURIComponent(bal.helmet));
    if (bal.range) p.push("range=" + distances()[bal.range]);
    var h = "#" + p.join("&");
    if (location.hash === h) return;
    try { history.replaceState(null, "", h); } catch (e) { location.hash = h; }
  }

  function readHash() {
    var h = location.hash.slice(1), out = { items: {} };
    if (!h) return null;
    h.split("&").forEach(function (x) {
      var i = x.indexOf("="), k, v;
      try { k = decodeURIComponent(i < 0 ? x : x.slice(0, i)); v = i < 0 ? "" : decodeURIComponent(x.slice(i + 1)); }
      catch (e) { return; }
      if (!k) return;
      if (k === "w") out.weapon = v;
      else if (RESERVED[k]) out[k] = v;
      else out.items[k] = v === "none" ? null : v;
    });
    return out.weapon ? out : null;
  }

  function applyHash() {
    var h = readHash();
    if (!h || !weaponById(h.weapon)) return false;
    load(h.weapon);
    var n = L.normalize(model, {
      weapon: h.weapon, items: h.items, sight: h.sight || null,
      stance: h.stance || stances()[0], bipod: h.bipod || bipodStates()[0]
    });
    lo = n.loadout;
    dropped = n.dropped || [];
    var lv = parseInt(h.lvl, 10);
    gate.role = h.cls && roles().indexOf(h.cls) >= 0 ? h.cls : "";
    gate.level = lv >= 1 ? lv : null;
    bal.ammo = h.ammo || null;
    bal.vest = VESTS.some(function (v) { return v[0] === h.vest; }) ? h.vest : "None";
    bal.helmet = HELMETS.some(function (v) { return v[0] === h.helmet; }) ? h.helmet : "None";
    bal.range = Math.max(0, distances().indexOf(Number(h.range)));
    return true;
  }

  /* ---------- extras: class level gates ---------- */

  function roles() { return (X && X.meta.roles) || []; }
  function distances() { return (X && X.meta.distances) || [0]; }

  // "Recon L28" for each class tree that unlocks the item, or "" when no tree gates it.
  function unlockText(id) {
    var u = X && X.unlocks[id];
    if (!u) return "";
    return Object.keys(u).sort().map(function (r) { return r + " L" + u[r][0]; }).join(", ");
  }

  // Whether the class and level limit allows the item: items in no tree are always allowed; with a class
  // chosen, only that class's tree counts; with "Any class", the lowest level over the trees.
  function allowed(id) {
    var u = X && X.unlocks[id];
    if (!u || gate.level == null) return true;
    if (gate.role) return !!u[gate.role] && u[gate.role][0] <= gate.level;
    return Object.keys(u).some(function (r) { return u[r][0] <= gate.level; });
  }

  function gateSuffix(id) {
    var t = unlockText(id);
    if (!t) return "";
    return allowed(id) ? " · " + t : " · locked: " + t;
  }

  function renderGate() {
    var locked = equippedIds().filter(function (id) { return !allowed(id); });
    els.gateHint.textContent = !X ? "" : gate.level == null
      ? "Set a class level to grey out what that class has not unlocked yet. Items that no class tree lists are always available."
      : (gate.role || "Any class") + " at level " + gate.level + ": locked items are greyed out." +
        (locked.length ? " Equipped but locked: " + locked.map(display).join(", ") + "." : "");
    els.gateHint.classList.toggle("lc-warn", locked.length > 0);
  }

  function equippedIds() {
    var ids = [lo.weapon];
    L.slots(model, lo).forEach(function (s) { if (s.choice != null) ids.push(s.choice); });
    return ids;
  }

  /* ---------- controls ---------- */

  function fillWeapons() {
    var sel = els.weapon, groups = {}, order = [];
    sel.textContent = "";
    weapons().forEach(function (w) {
      var g = w.archetype || "Other";
      if (!groups[g]) { groups[g] = el("optgroup"); groups[g].label = g; order.push(g); }
      var o = el("option", null, weaponLabel(w) + gateSuffix(w.id));
      o.value = w.id;
      o.disabled = !allowed(w.id) && !(lo && lo.weapon === w.id);
      groups[g].appendChild(o);
    });
    order.forEach(function (g) { sel.appendChild(groups[g]); });
    sel.disabled = false;
  }

  function cssEscape(s) { return window.CSS && CSS.escape ? CSS.escape(s) : String(s).replace(/["\\]/g, "\\$&"); }

  function renderSlots() {
    var box = els.slots, list = L.slots(model, lo), active = document.activeElement;
    var focusKey = active && box.contains(active) ? active.getAttribute("data-key") : null;
    var none = list.filter(function (s) { return !(s.accepts && s.accepts.length); });
    box.textContent = "";
    list.forEach(function (s, i) {
      if (!(s.accepts && s.accepts.length)) return;   // chamber and magazine ammo: no attachment fits
      var f = el("div", "vv-field lc-slot" + (s.depth ? " lc-slot-child" : ""));
      f.style.setProperty("--lc-depth", s.depth || 0);
      f.setAttribute("data-key", s.key);
      var id = "lc-slot-" + i, lab = el("label");
      lab.htmlFor = id;
      lab.appendChild(document.createTextNode(s.label || L.slotLabel(s.tag)));
      if (s.depth && s.owner) lab.appendChild(el("span", "lc-slot-on", " on " + display(s.owner)));
      var sel = el("select");
      sel.id = id;
      sel.setAttribute("data-key", s.key);
      var dflt = s["default"] != null ? s["default"] : null;
      var empty = el("option", null, "Empty" + (dflt == null ? " (default)" : ""));
      empty.value = "";
      sel.appendChild(empty);
      s.accepts.forEach(function (a) {
        var o = el("option", null, itemLabel(a) + (a === dflt ? " (default)" : "") + gateSuffix(a));
        o.value = a;
        o.disabled = !allowed(a) && a !== s.choice;
        sel.appendChild(o);
      });
      sel.value = s.choice != null ? s.choice : "";
      sel.addEventListener("change", function () {
        lo = L.setItem(model, lo, s.key, sel.value || null);
        dropped = [];
        settle();
        update(true);
      });
      f.appendChild(lab);
      f.appendChild(sel);
      if (s.flag) { var fl = el("p", "lc-hint lc-warn"); richText(fl, s.flag); f.appendChild(fl); }
      if (s.choice != null && !allowed(s.choice)) {
        f.appendChild(el("p", "lc-hint lc-warn", "Locked at this class level (unlocks at " + unlockText(s.choice) + ")."));
      }
      box.appendChild(f);
    });
    if (!box.children.length) box.appendChild(el("p", "lc-empty", "No sub-slot of this weapon accepts an attachment."));
    if (none.length) {
      box.appendChild(el("p", "lc-hint", "Not shown (no attachment fits, ammunition only): " +
        none.map(function (s) { return s.key; }).join(", ") + "."));
    }
    if (focusKey) {
      var again = box.querySelector('select[data-key="' + cssEscape(focusKey) + '"]');
      if (again) again.focus();
    }
  }

  function renderSight() {
    var sel = els.sight, list = L.sights(model, lo), dflt = defaultSight();
    var hasDefault = list.some(function (s) { return s.isDefault; });
    sel.textContent = "";
    if (!list.length) {
      sel.appendChild(el("option", null, "No sight entries in this loadout"));
      sel.disabled = true;
      els.sightHint.textContent = "";
      return;
    }
    var first = el("option", null, hasDefault ? dflt + " (initial)" : dflt + " (initial; not on the equipped sights)");
    first.value = "";
    sel.appendChild(first);
    list.forEach(function (s) {
      if (s.isDefault) return;
      var o = el("option", null, s.name + (list.length > 1 && s.items && s.items.length && multiSight(list) ? " (" + s.items.map(display).join(", ") + ")" : ""));
      o.value = s.name;
      sel.appendChild(o);
    });
    sel.value = lo.sight == null ? "" : lo.sight;
    sel.disabled = false;
    els.sightHint.textContent = list.length > 1 || !hasDefault
      ? "The weapon starts on " + dflt + " and changes entry through CycleSights. A chosen entry applies to every equipped attachment that has it."
      : "";
  }
  // More than one attachment carries sight entries: name the attachment each entry belongs to.
  function multiSight(list) {
    var owners = {};
    list.forEach(function (s) { (s.items || []).forEach(function (i) { owners[i] = 1; }); });
    return Object.keys(owners).length > 1;
  }

  function setRadio(group, value, focus) {
    var off = group.getAttribute("aria-disabled") === "true";
    Array.prototype.forEach.call(group.querySelectorAll("button"), function (b) {
      var on = b.value === value;
      b.setAttribute("aria-checked", String(on));
      b.tabIndex = on && !off ? 0 : -1;
      if (focus && on) b.focus();
    });
  }

  function setupRadio(group, onPick) {
    var buttons = Array.prototype.slice.call(group.querySelectorAll("button"));
    function pick(v, focus) { onPick(v); dropped = []; setRadio(group, v, focus); update(true); }
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        if (group.getAttribute("aria-disabled") !== "true") pick(b.value, false);
      });
    });
    group.addEventListener("keydown", function (e) {
      var step = e.key === "ArrowRight" || e.key === "ArrowDown" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowUp" ? -1 : 0;
      if (!step || group.getAttribute("aria-disabled") === "true") return;
      e.preventDefault();
      var at = buttons.indexOf(group.querySelector('[aria-checked="true"]'));
      pick(buttons[(at + step + buttons.length) % buttons.length].value, true);
    });
  }

  function renderBipod(res) {
    var on = res.hasBipod != null ? !!res.hasBipod : L.hasBipod(model, lo), g = els.bipod;
    if (on) g.removeAttribute("aria-disabled"); else g.setAttribute("aria-disabled", "true");
    Array.prototype.forEach.call(g.querySelectorAll("button"), function (b) { b.disabled = !on; });
    setRadio(g, lo.bipod, false);
    els.bipodHint.textContent = on
      ? "Unfolded applies the bipod's unfolded lists; mounted removes them and applies its mounted lists instead."
      : "No bipod is equipped, so there are no bipod lists to apply.";
  }

  /* ---------- output ---------- */

  function stepItem(st) {
    var li = el("li");
    var op = el("span", "lc-op", st.symbol || L.OPS[st.op] || st.op || "?");
    op.title = OP_NAMES[st.op] || st.op || "";
    li.appendChild(op);
    var text = st.backing
      ? "current " + L.attrLabel(st.backing) + (st.magnitude != null ? " = " + fmt(st.magnitude) : "")
      : st.magnitude == null ? "?" : fmt(st.magnitude);
    var v = el("span", "lc-mag", text);
    if (st.magnitude != null) v.title = fmt(st.magnitude, 10);
    li.appendChild(v);
    if (st.stacks != null && st.stacks !== 1) li.appendChild(el("span", "lc-stacks", "×" + st.stacks + " stacks"));
    li.appendChild(el("code", "lc-effect", st.effect || ""));
    if (st.source) li.appendChild(el("span", "lc-src", st.source));
    if (st.flag) li.appendChild(el("span", "lc-flag", st.flag));
    return li;
  }

  function renderRows(res) {
    var tb = els.rows, changed = 0, vsDefault = 0, defBy = {};
    tb.textContent = "";
    ((defEval && defEval.weapon) || []).forEach(function (r) { defBy[r.tag] = r; });
    res.weapon.forEach(function (r) {
      var tr = el("tr"), name = r.label || L.attrLabel(r.tag);
      tr.setAttribute("data-attr", name);
      var th = el("th", "lc-attr", name);
      th.scope = "row";
      th.title = r.tag;
      tr.appendChild(th);

      var base = el("td", "lc-num lc-base", fmt(r.base));
      if (r.base != null) base.title = fmt(r.base, 10);
      tr.appendChild(base);

      var mods = el("td", "lc-mods-cell"), steps = r.steps || [];
      if (!steps.length) mods.appendChild(el("span", "lc-none", "—"));
      else {
        var ul = el("ul", "lc-steps");
        steps.forEach(function (st) { ul.appendChild(stepItem(st)); });
        mods.appendChild(ul);
      }
      (r.notes || []).forEach(function (n) { var p = el("p", "lc-row-note"); richText(p, n); mods.appendChild(p); });
      tr.appendChild(mods);

      var fin = el("td", "lc-num lc-final");
      var val = el("span", "lc-final-val", fmt(r.final) + ((r.notes && r.notes.length) ? " †" : ""));
      if (r.final != null) { val.title = fmt(r.final, 10); fin.setAttribute("data-full", fmt(r.final, 10)); }
      fin.appendChild(val);
      if (r.final != null && r.base != null && fmt(r.final) !== fmt(r.base)) {
        tr.classList.add("lc-changed");
        changed++;
        fin.appendChild(el("span", "lc-sr", " (changed from the base)"));
      }
      var d = defBy[r.tag];
      if (d && fmt(d.final) !== fmt(r.final)) {
        vsDefault++;
        tr.classList.add("lc-vs-default");
        fin.appendChild(el("span", "lc-was", "default " + fmt(d.final)));
      }
      tr.appendChild(fin);
      tb.appendChild(tr);
    });
    els.summary.textContent = res.weapon.length
      ? changed + " of " + res.weapon.length + " values differ from the weapon's base" +
        (vsDefault ? "; " + vsDefault + " differ from its default loadout." : "; none differs from its default loadout.")
      : "This weapon has no weapon attributes.";
  }

  function renderList(ul, makers, emptyText) {
    ul.textContent = "";
    if (!makers.length) { ul.appendChild(el("li", "lc-none", emptyText)); return; }
    makers.forEach(function (make) { var li = el("li"); make(li); ul.appendChild(li); });
  }

  function modText(m) {
    var v = m.kind === "Attribute" ? "current " + L.attrLabel(m.backing) : m.kind === "SetByCaller" ? "SetByCaller" : fmt(m.value);
    return L.attrLabel(m.attribute) + " " + (m.symbol || L.OPS[m.op] || m.op) + " " + v;
  }

  function renderCharacter(res) {
    renderList(els.character, (res.character || []).map(function (c) {
      return function (li) {
        li.appendChild(el("code", null, c.effect));
        if (c.source) li.appendChild(el("span", "lc-src", c.source));
        if (c.modifiers && c.modifiers.length) li.appendChild(el("span", "lc-char-mods", c.modifiers.map(modText).join(", ")));
        else if (c.modifiers === null) li.appendChild(el("span", "lc-char-mods", "not in the exported effect values"));
      };
    }), "None for this loadout.");
  }

  function renderNotes(res) {
    var notes = (res.notes || []).slice();
    if (dropped.length) notes.unshift("From the link, not applied: " + dropped.join("; "));
    renderList(els.notes, notes.map(function (n) { return function (li) { richText(li, n); }; }), "Nothing to flag for this loadout.");
  }

  function renderCli() {
    var c = L.cli(model, lo) || {};
    // One nowrap span per word, so a line never breaks inside "--stance" or an id.
    els.cli.textContent = "";
    (CMD + (c.args || "")).split(" ").forEach(function (w, i) {
      if (i) els.cli.appendChild(document.createTextNode(" "));
      els.cli.appendChild(el("span", "lc-arg", w));
    });
    els.copy.disabled = false;
    els.cliNote.classList.toggle("lc-warn", c.exact === false);
    els.cliNote.textContent = c.exact === false
      ? "Not the same loadout: " + (c.reason || "the command line can't express it") + "."
      : "Prints the same loadout, with every value at full precision.";
  }

  /* ---------- extras: sight and reticle ---------- */

  function img(path, alt, cls) {
    var i = el("img", cls);
    i.src = base + path;
    i.alt = alt;
    i.decoding = "async";
    return i;
  }

  // The scope reticles are black lines, the lens reticles white (greyscale emissive): "lc-reticle-lens" darkens the disc.
  function figure(path, caption, alt, cls) {
    var f = el("figure", "lc-reticle" + (cls ? " " + cls : ""));
    var pane = el("div", "lc-reticle-pane");
    pane.appendChild(img(path, alt));
    f.appendChild(pane);
    f.appendChild(el("figcaption", null, caption));
    return f;
  }

  function finalOf(res, tag) {
    var r = res.weapon.filter(function (x) { return x.tag === tag; })[0];
    return r ? r.final : null;
  }

  function renderOptics(res) {
    var box = els.optics, entry = lo.sight || defaultSight();
    box.textContent = "";
    var zoom = finalOf(res, "Attribute.Gameplay.Weapon.AdsZoomMultiplier");
    var aim = finalOf(res, "Attribute.Gameplay.Weapon.AimTime");
    var stats = el("p", "lc-card-lead");
    stats.textContent = "Aiming zoom ×" + (zoom == null ? "?" : fmt(zoom)) + ", aim time " + (aim == null ? "?" : fmt(aim) + " s") +
      " (weapon attributes of this loadout). Sight entry: " + entry + ".";
    box.appendChild(stats);
    var sights = equippedIds().filter(function (id) { var it = item(id); return it && it.sights && it.sights.length; });
    if (!sights.length) { box.appendChild(el("p", "lc-none", "No sight attachment equipped: the weapon aims with its own sights.")); return; }
    sights.forEach(function (id) {
      var wrap = el("div", "lc-sight"), head = el("div", "lc-sight-head");
      var icon = X.icons[id];
      if (icon) head.appendChild(img(icon, "", "lc-sight-icon"));
      head.appendChild(el("strong", null, display(id)));
      wrap.appendChild(head);
      var r = X.reticles[id] || {}, row = el("div", "lc-reticles");
      if (r.scope) row.appendChild(figure(r.scope, "Through the scope", display(id) + " reticle through the scope"));
      var lens = r.entries && r.entries[entry];
      if (lens) row.appendChild(figure(lens, "Lens reticle (" + entry + ")", display(id) + " lens reticle", "lc-reticle-lens"));
      if (row.children.length) wrap.appendChild(row);
      else wrap.appendChild(el("p", "lc-hint", "No reticle image: this sight's reticle is built inside the game's material, with no texture to show."));
      box.appendChild(wrap);
    });
  }

  /* ---------- extras: ammunition, body parts, drop-off ---------- */

  function ballistics() { return (X && lo && X.ballistics[lo.weapon]) || null; }
  function hp() { return (X && X.meta.hp) || 100; }
  function label(list, key) { var x = list.filter(function (v) { return v[0] === key; })[0]; return x ? x[1] : key; }
  function n1(v) { return v == null ? "—" : (Math.round(v * 10) / 10).toFixed(1); }

  // Damage of one shot (all pellets) at a body part and distance index, and the armor piece that applied.
  function shot(a, part, i) {
    var row = a.damage[part] || {}, kind = X.meta.armorKind[part] === "helmet" ? "helmet" : "vest";
    var cls = kind === "helmet" ? bal.helmet : bal.vest;
    var covered = cls !== "None" && row[cls] != null;
    var f = a.factor ? a.factor[i] : (i === 0 ? 1 : null);
    if (f == null || row.None == null) return null;
    return { dmg: (covered ? row[cls] : row.None) * f * a.pellets, armor: covered ? label(kind === "helmet" ? HELMETS : VESTS, cls) : "" };
  }

  function kill(b, s) {
    if (!s || s.dmg <= 0) return null;
    var n = Math.ceil(hp() / s.dmg - 1e-9);
    return { shots: n, ttk: b.rpm ? (n - 1) * 60 / b.rpm : null };
  }

  function td(text, cls) { return el("td", cls, text); }

  function renderBallistics() {
    var b = ballistics(), card = els.ballisticsCard;
    if (!b || !b.ammo.length) {
      card.hidden = !X;
      els.balSummary.textContent = "No bullet damage data for this weapon: launchers and the bow are not modelled here.";
      [els.partsRows, els.dropHead, els.dropRows].forEach(function (x) { x.textContent = ""; });
      card.classList.add("lc-bal-empty");
      els.balNote.textContent = "";
      return;
    }
    card.hidden = false;
    card.classList.remove("lc-bal-empty");
    if (!b.ammo.some(function (a) { return a.id === bal.ammo; })) bal.ammo = b.ammo[0].id;
    els.ammo.textContent = "";
    b.ammo.forEach(function (a) { var o = el("option", null, a.label); o.value = a.id; els.ammo.appendChild(o); });
    els.ammo.value = bal.ammo;
    var a = b.ammo.filter(function (x) { return x.id === bal.ammo; })[0], dist = distances(), i = bal.range;
    var er = b.effectiveRange, pel = a.pellets > 1;

    els.balSummary.textContent = display(lo.weapon) + " with " + a.label + ": " + (b.rpm ? fmt(b.rpm) + " rounds per minute" : "rate of fire not known") +
      (pel ? ", " + a.pellets + " pellets per shot (all assumed to hit)" : "") +
      (er != null ? ", full damage out to " + fmt(er) + " m" : "") + ". At " + dist[i] + " m against a " + hp() + " HP target:";

    els.partsRows.textContent = "";
    X.meta.locations.forEach(function (part) {
      var s = shot(a, part, i), k = kill(b, s), tr = el("tr");
      var th = el("th", null, PART_NAMES[part] || part);
      th.scope = "row";
      tr.appendChild(th);
      tr.appendChild(td(s ? s.armor || "—" : "—"));
      tr.appendChild(td(s ? n1(s.dmg) : "not reached", "lc-num"));
      tr.appendChild(td(k ? String(k.shots) : "—", "lc-num"));
      tr.appendChild(td(k && k.ttk != null ? k.ttk.toFixed(2) + " s" : "—", "lc-num"));
      els.partsRows.appendChild(tr);
    });

    els.dropHead.textContent = "";
    var hr = el("tr");
    ["Distance", "Damage factor"].concat(DROP_PARTS.map(function (p) { return PART_NAMES[p]; }), ["Shots to kill, upper torso", "Time to kill, upper torso"])
      .forEach(function (t, c) { var th = el("th", c ? "lc-num" : null, t); th.scope = "col"; hr.appendChild(th); });
    els.dropHead.appendChild(hr);
    els.dropRows.textContent = "";
    dist.forEach(function (d, j) {
      var tr = el("tr"), f = a.factor ? a.factor[j] : (j === 0 ? 1 : null);
      if (j === i) tr.className = "lc-row-on";
      var th = el("th", null, d + " m" + (er != null && d > er ? " *" : ""));
      th.scope = "row";
      tr.appendChild(th);
      tr.appendChild(td(f == null ? "not reached" : (f * 100).toFixed(1) + "%", "lc-num"));
      DROP_PARTS.forEach(function (p) { var s = shot(a, p, j); tr.appendChild(td(s ? n1(s.dmg) : "—", "lc-num")); });
      var k = kill(b, shot(a, "Torso.Upper", j));
      tr.appendChild(td(k ? String(k.shots) : "—", "lc-num"));
      tr.appendChild(td(k && k.ttk != null ? k.ttk.toFixed(2) + " s" : "—", "lc-num"));
      els.dropRows.appendChild(tr);
    });
    els.balNote.textContent = "Every shot hits the named part; no reload, spread or recoil. Damage per shot comes from the weapon and the ammunition, and attachments do not change it. " +
      "Damage at a distance is the point-blank damage × the weapon's falloff curve × the bullet's speed loss to drag (Weapon Damage Falloff). " +
      (er != null ? "* beyond the full-damage range. " : "") + "A vest covers the torso (level 4 also the pelvis and upper arm); a helmet covers the head (level 3, level 4 and tank crew helmets also the neck).";
  }

  function fillBalControls() {
    [[els.vest, VESTS], [els.helmet, HELMETS]].forEach(function (p) {
      p[0].textContent = "";
      p[1].forEach(function (v) { var o = el("option", null, v[1]); o.value = v[0]; p[0].appendChild(o); });
    });
    els.range.textContent = "";
    distances().forEach(function (d, j) { var o = el("option", null, d + " m"); o.value = String(j); els.range.appendChild(o); });
    els.role.textContent = "";
    var any = el("option", null, "Any class");
    any.value = "";
    els.role.appendChild(any);
    roles().forEach(function (r) { var o = el("option", null, r); o.value = r; els.role.appendChild(o); });
    els.role.disabled = els.level.disabled = false;
  }

  function syncBalControls() {
    els.vest.value = bal.vest;
    els.helmet.value = bal.helmet;
    els.range.value = String(bal.range);
    els.role.value = gate.role;
    els.level.value = gate.level == null ? "" : String(gate.level);
  }

  function renderExtras(res) {
    if (!X) return;
    els.opticsCard.hidden = false;
    fillWeapons();
    els.weapon.value = lo.weapon;
    syncBalControls();
    renderGate();
    renderOptics(res);
    renderBallistics();
  }

  function update(hash) {
    var res;
    try { res = L.evaluate(model, lo); }
    catch (err) {
      status("This loadout could not be evaluated (" + err.message + ").");
      return;
    }
    status("");
    els.weapon.value = lo.weapon;
    renderSlots();
    renderSight();
    setRadio(els.stance, lo.stance, false);
    renderBipod(res);
    renderRows(res);
    renderCharacter(res);
    renderNotes(res);
    renderCli();
    renderExtras(res);
    els.reset.disabled = isDefault();
    if (hash) writeHash();
  }

  function copy() {
    var text = els.cli.textContent;
    function done(ok) {
      els.copy.textContent = ok ? "Copied" : "Press Ctrl+C to copy";
      clearTimeout(copyTimer);
      copyTimer = setTimeout(function () { els.copy.textContent = "Copy command"; }, 1800);
    }
    function fallback() {
      var r = document.createRange(), s = window.getSelection();
      r.selectNodeContents(els.cli);
      s.removeAllRanges();
      s.addRange(r);
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
      done(ok);
    }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(function () { done(true); }, fallback);
    else fallback();
  }

  function status(text) { els.status.textContent = text || ""; els.status.hidden = !text; }

  function fail(text) {
    status(text + " The default loadouts are in the Weapon Attributes tables.");
    var a = el("a", null, "Weapon Attributes, final values");
    a.href = "Wardogs_WeaponAttributes_v1.html#1-final-values";
    els.status.appendChild(document.createTextNode(" "));
    els.status.appendChild(a);
    root.classList.add("lc-no-data");
  }

  ready(function () {
    root = $("lc");
    if (!root) return;
    ["weapon", "reset", "status", "slots", "sight", "stance", "bipod", "summary", "rows", "notes", "cli", "copy"].forEach(function (k) {
      els[k] = $("lc-" + k);
    });
    els.character = $("lc-char");
    els.sightHint = $("lc-sight-hint");
    els.bipodHint = $("lc-bipod-hint");
    els.cliNote = $("lc-cli-note");
    ["role", "level", "optics", "ammo", "vest", "helmet", "range"].forEach(function (k) { els[k] = $("lc-" + k); });
    els.gateHint = $("lc-gate-hint");
    els.opticsCard = $("lc-optics-card");
    els.ballisticsCard = $("lc-ballistics-card");
    els.balSummary = $("lc-bal-summary");
    els.balNote = $("lc-bal-note");
    els.partsRows = $("lc-parts-rows");
    els.dropHead = $("lc-drop-head");
    els.dropRows = $("lc-drop-rows");
    base = root.getAttribute("data-base") || "/";
    L = window.WDLoadout;
    if (!L || typeof L.model !== "function") { fail("The calculator's evaluator (loadout-eval.js) did not load."); return; }
    status("Loading the weapon data…");
    function getJson(url) { return fetch(url).then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); }); }
    // The extras are optional: without them the calculator still shows the attributes.
    var extras = getJson(root.getAttribute("data-extras")).catch(function () { return null; });
    Promise.all([getJson(root.getAttribute("data-json")), extras])
      .then(function (both) {
        var json = both[0];
        X = both[1];
        if (X) {
          fillBalControls();
          els.role.addEventListener("change", function () { gate.role = els.role.value; update(true); });
          els.level.addEventListener("change", function () {
            var v = parseInt(els.level.value, 10);
            gate.level = v >= 1 ? Math.min(v, 150) : null;
            update(true);
          });
          els.ammo.addEventListener("change", function () { bal.ammo = els.ammo.value; update(true); });
          els.vest.addEventListener("change", function () { bal.vest = els.vest.value; update(true); });
          els.helmet.addEventListener("change", function () { bal.helmet = els.helmet.value; update(true); });
          els.range.addEventListener("change", function () { bal.range = parseInt(els.range.value, 10) || 0; update(true); });
        }
        model = L.model(json);
        if (!weapons().length) throw new Error("no weapons in the data");
        fillWeapons();
        if (!applyHash()) load(weapons()[0].id);
        els.weapon.addEventListener("change", function () { load(els.weapon.value); update(true); });
        els.reset.addEventListener("click", function () { load(lo.weapon); update(true); els.weapon.focus(); });
        els.sight.addEventListener("change", function () { lo.sight = els.sight.value || null; dropped = []; update(true); });
        setupRadio(els.stance, function (v) { lo.stance = v; });
        setupRadio(els.bipod, function (v) { lo.bipod = v; });
        els.copy.addEventListener("click", copy);
        window.addEventListener("hashchange", function () { if (applyHash()) update(false); });
        update(!!location.hash);
        els.reset.disabled = isDefault();
        root.classList.add("lc-ready");
      })
      .catch(function (err) { fail("The weapon data could not be loaded (" + err.message + ")."); });
  });
})();
