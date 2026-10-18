/* Weapon Loadout Calculator (loadout-calculator.md; styles in _sass/custom/loadout-calculator.scss, on top
   of the vehicle viewer's .vv-* styles). UI only: every rule (which sub-slots a choice opens, what a
   slot accepts, the sight entries, the bipod lists, the evaluation and the command-line equivalent)
   comes from window.WDLoadout (assets/js/loadout-eval.js, loaded before this file), the browser twin of
   _tools/weapon_attributes.py. Data: assets/data/weapon-loadouts.json (weapon_attributes.py --json).
   - one select per open sub-slot, listing what the slot accepts plus "Empty";
   - sight, stance and bipod (the bipod switch is enabled only while a bipod is equipped);
   - the attribute table (base, each modifier, final; changed values highlighted), the character
     effects and the notes; a deep link in the hash; the equivalent command line.
   With JavaScript off the page shows the .vv-nojs note instead. Strings from the data are set as text. */
(function () {
  "use strict";

  var CMD = "python -I _tools/weapon_attributes.py ";
  var OP_NAMES = { Add: "Add", Multiply: "Multiply", Divide: "Divide", MultiplyCompound: "MultiplyCompound",
                   AddFinal: "AddFinal", Override: "Override" };

  var L, model, root, els = {}, lo = null, defEval = null, dropped = [], copyTimer = null;

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

  var RESERVED = { w: 1, sight: 1, stance: 1, bipod: 1 };

  function writeHash() {
    var p = ["w=" + encodeURIComponent(lo.weapon)];
    L.slots(model, lo).forEach(function (s) {
      if (!s.isDefault) p.push(encodeURIComponent(s.key) + "=" + encodeURIComponent(s.choice == null ? "none" : s.choice));
    });
    if (lo.sight != null) p.push("sight=" + encodeURIComponent(lo.sight));
    if (lo.stance !== stances()[0]) p.push("stance=" + encodeURIComponent(lo.stance));
    if (lo.bipod !== bipodStates()[0]) p.push("bipod=" + encodeURIComponent(lo.bipod));
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
    return true;
  }

  /* ---------- controls ---------- */

  function fillWeapons() {
    var sel = els.weapon, groups = {}, order = [];
    sel.textContent = "";
    weapons().forEach(function (w) {
      var g = w.archetype || "Other";
      if (!groups[g]) { groups[g] = el("optgroup"); groups[g].label = g; order.push(g); }
      var o = el("option", null, weaponLabel(w));
      o.value = w.id;
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
        var o = el("option", null, itemLabel(a) + (a === dflt ? " (default)" : ""));
        o.value = a;
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
    L = window.WDLoadout;
    if (!L || typeof L.model !== "function") { fail("The calculator's evaluator (loadout-eval.js) did not load."); return; }
    status("Loading the weapon data…");
    fetch(root.getAttribute("data-json"))
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (json) {
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
