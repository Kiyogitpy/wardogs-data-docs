/* Weapon loadout evaluator: the browser twin of `python -I _tools/weapon_attributes.py --weapon ...`.
   Pure logic, no DOM, no dependencies. UMD: a browser global `window.WDLoadout`, or
   `require("./assets/js/loadout-eval.js")` in node. Data: assets/data/weapon-loadouts.json
   (python -I _tools/weapon_attributes.py --json). `python -I _tools/weapon_attributes.py --check`
   runs the same loadouts through this file and through the Python and requires 0 mismatches.

   Rules (Wardogs_WeaponAttributes_v1.md "Rules"; Effects §7.1, §4.2, §4.4): base = the weapon's
   DefaultAttributes as f32; one application per equipped attachment's AppliedEffects, the selected
   sight's effects, the bipod's unfolded or mounted lists, and the stance preset (with its stacks);
   stack scaling m' = (m - I) * n + I (not for Override); the first Override wins, otherwise
   ((Base + ΣAdd) * (1 + Σ(Mul - 1)) / D) * ΠMulCompound + ΣAddFinal. Sums are CPython 3.12+ sum()
   (Neumaier-compensated), magnitudes are Math.fround'ed like the Python's f32(). Character-side
   lists are listed, never evaluated.

   ----------------------------------------------------------------------------------- API
   Strings that come from the game data (display names, tags, ids, effect names, notes) are data:
   set them as text, never as HTML. Notes use `backticks` around ids, as the Python prints them.

   WDLoadout.model(json) -> model
       Prepares the parsed weapon-loadouts.json. The model is read-only; keep one per page.
       model.meta                  the JSON's meta (data tree id, generator, doc anchors, notes)
       model.weapons               [{id, display, archetype}] in the Python's order (archetype, name)
       model.items[id]             {id, itemId, display, attachmentType, archetype, isWeapon,
                                    isAttachment, hasSights, isBipod, sights: [name]}
                                   id = asset name, e.g. "ID_WEPN_037" (also every `itemId` below)
       model.stances               ["Stand", "Crouch", "Prone"]
       model.bipodStates           ["folded", "unfolded", "mounted"]
       model.defaultSight          "S_Aim01"

   A loadout is a plain object (JSON-safe, fine for a permalink):
       {weapon: id, items: {<slot key>: itemId|null}, sight: name|null,
        stance: "Stand"|"Crouch"|"Prone", bipod: "folded"|"unfolded"|"mounted"}
       - slot key: the sub-slot's label path from the weapon down, joined by "/", e.g. "Barrel",
         "Barrel/Muzzle", "Handguard/Underbarrel" (label = tag without "Item.Attachment.").
       - a key missing from `items` means the slot's default item; null means empty. Keys of slots
         that are not open are ignored. Choosing "none" never adds a slot's missing-default note
         back or drops it: only placing an item drops it (as in the Python).
       - sight null means the default: every sight-bearing attachment uses `S_Aim01`, or no sight
         effects if it has no `S_Aim01`. A name applies to every attachment that has that entry;
         the others fall back to `S_Aim01` with a note (the Python's --sight).

   WDLoadout.defaultLoadout(model, weaponId) -> loadout
       The weapon's default loadout with every open slot written out explicitly (DefaultContainerItems,
       or DefaultItems only when that is empty), sight null, Stand, folded.

   WDLoadout.slots(model, loadout) -> [slot]
       The open sub-slots in walk order (each slot followed by the sub-slots its item brings):
       {key, tag, label, parent: key|null, depth (0 = on the weapon), owner: itemId (weapon or the
        attachment that brings the slot), accepts: [itemId] (attachments the filter admits, in data
        order), default: itemId|null, choice: itemId|null (what the loadout puts there),
        isDefault: bool, flag: string|null (missing default item note)}
       Slots that accept no attachment (chamber, magazine ammo) are included with accepts [].

   WDLoadout.setItem(model, loadout, key, itemId|null) -> new loadout
       Puts the item into the slot (it must be in that slot's `accepts`, or null), drops the keys of
       the slot's old sub-slots and writes out the defaults of the sub-slots the new item brings.

   WDLoadout.normalize(model, loadout) -> {loadout, dropped: [string]}
       For a loadout from a permalink: drops an unknown weapon (falls back to the first weapon),
       keys of slots that are not open, items the slot does not accept, an unknown stance or bipod
       state, and a sight no equipped item has; `dropped` says what went.

   WDLoadout.sights(model, loadout) -> [{name, items: [itemId], isDefault}]
       The SightsData entries of the equipped attachments, in walk order then data order, deduped by
       name. isDefault marks `S_Aim01`. Empty when nothing equipped has sights.

   WDLoadout.hasBipod(model, loadout) -> bool
       True when an equipped item carries the bipod lists (enable the bipod control only then).
       Evaluating a loadout with bipod unfolded/mounted and no bipod gives a note, no error.

   WDLoadout.evaluate(model, loadout) -> result
       {weapon: [{tag, label, base: number|null,
                  steps: [{source, effect, op, symbol, kind, stacks, magnitude: number|null,
                           backing: tag|null, flag: string|null}],
                  final: number|null, notes: [string]}],
        character: [{effect, source, modifiers: [modifier]|null}],
        applications: [{effect, stacks, source}],       weapon-side, in Override order
        attachments: [{key, tag, item}],                 equipped items in walk order
        hasBipod: bool,
        notes: [string]}                                  loadout flags, application notes, eval flags
       `weapon` lists every attribute the weapon has a base for (data order), then any other
       attribute a weapon-side modifier reaches. magnitude = the stack-scaled value the formula used,
       null when it was not evaluated (flag says why). `op` is the EBHAttributeModOp name, `symbol`
       its sign (+ × ÷ ×c +f =). `source` is the attachment id, "<id> sight <name>",
       "<id> bipod unfolded|mounted" or "stance <Stance>". Throws on an unknown weapon or an item a
       slot does not accept (normalize() first for untrusted input).

   WDLoadout.cli(model, loadout) -> {args, exact, reason}
       The weapon_attributes.py arguments for the loadout, e.g.
       "--weapon ID_WEPN_037 --with ID_FGRP_006 ID_SGHT_009 --sight S_Aim02 --stance Prone --mounted".
       exact = true when those arguments give exactly this loadout (checked by replaying the
       --with placement); otherwise false with a plain-text reason (e.g. the CLI cannot empty a slot
       that has a default item, or its first-free-slot rule would put an item elsewhere).

   WDLoadout.withItems(model, weaponId, ids, opts?) -> loadout
       The CLI's --with placement: each item goes into the first free sub-slot (walk order, sub-slots
       opened by earlier items included) that accepts it, replacing the default there. opts may give
       sight, stance, bipod. Throws when no free sub-slot accepts an item (the CLI's error).

   WDLoadout.effect(model, name) -> [modifier]|null
       An effect's modifiers: {attribute, op, symbol, kind, value?, backing?, mode?, channel?,
       curve?, indexing?, fallback?}.
   WDLoadout.attrLabel(tag) -> tag without "Attribute.Gameplay.Weapon." (or "Attribute.Gameplay.")
   WDLoadout.slotLabel(tag) -> tag without "Item.Attachment."
   WDLoadout.OPS             {Add: "+", Multiply: "×", Divide: "÷", MultiplyCompound: "×c",
                              AddFinal: "+f", Override: "="}
   WDLoadout.fmt(x, digits=6) -> Python f"{x:.{digits}g}" ("—" for null): the tables' rounding.
   ------------------------------------------------------------------------------------------ */
(function (root, factory) {
  "use strict";
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.WDLoadout = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var OPS = {Add: "+", Multiply: "×", Divide: "÷", MultiplyCompound: "×c", AddFinal: "+f", Override: "="};
  var OP_NAMES = ["Add", "Multiply", "Divide", "MultiplyCompound", "AddFinal", "Override"];
  var STANCES = ["Stand", "Crouch", "Prone"];
  var BIPOD_STATES = ["folded", "unfolded", "mounted"];
  var fround = Math.fround;
  var has = function (o, k) { return Object.prototype.hasOwnProperty.call(o, k); };

  // ------------------------------------------------------------------ helpers (Python twins)

  function replaceAll(s, a, b) { return s.split(a).join(b); }
  // ge_values.short(): every "Attribute.Gameplay." removed, "?" for an empty tag.
  function pyShort(tag) { return tag ? replaceAll(tag, "Attribute.Gameplay.", "") : "?"; }
  function slotLabel(tag) { return replaceAll(tag, "Item.Attachment.", ""); }
  function attrLabel(tag) {
    if (!tag) return "?";
    var w = "Attribute.Gameplay.Weapon.";
    return tag.indexOf(w) === 0 ? tag.slice(w.length) : pyShort(tag);
  }
  function pyStr(x) { return x === null || x === undefined ? "None" : String(x); }

  // CPython 3.12+ sum() of floats with start 0 (Neumaier); weapon_attributes.nsum().
  function nsum(xs) {
    if (!xs.length) return 0;
    var hi = 0 + xs[0], lo = 0.0;
    for (var i = 1; i < xs.length; i++) {
      var x = xs[i], t = hi + x;
      if (Math.abs(hi) >= Math.abs(x)) lo += (hi - t) + x;
      else lo += (x - t) + hi;
      hi = t;
    }
    return lo && isFinite(lo) ? hi + lo : hi;
  }

  // Python f"{x:.{digits}g}", rounding half to even on the exact value of the double.
  function fmt(x, digits) {
    if (x === null || x === undefined) return "—";
    digits = digits === undefined ? 6 : Math.max(1, digits);
    if (x !== x) return "nan";
    if (x === Infinity) return "inf";
    if (x === -Infinity) return "-inf";
    var sign = x < 0 || (x === 0 && 1 / x < 0) ? "-" : "";
    if (x === 0) return sign + "0";
    var e = Math.abs(x).toExponential(100).split("e");      // exact enough: 101 significant digits
    var all = e[0].replace(".", ""), exp = parseInt(e[1], 10);
    var d = all.slice(0, digits).split("").map(Number), rest = all.slice(digits);
    var up = rest[0] > "5" || (rest[0] === "5" && (/[1-9]/.test(rest.slice(1)) || d[d.length - 1] % 2 === 1));
    if (up) {
      var i = d.length - 1;
      while (i >= 0 && d[i] === 9) { d[i] = 0; i--; }
      if (i < 0) { d.unshift(1); d.pop(); exp++; } else d[i]++;
    }
    var ds = d.join(""), out;
    if (exp < -4 || exp >= digits) {
      var m = ds.length > 1 ? ds[0] + "." + ds.slice(1) : ds;
      m = m.indexOf(".") >= 0 ? m.replace(/0+$/, "").replace(/\.$/, "") : m;
      var ae = Math.abs(exp);
      out = m + "e" + (exp < 0 ? "-" : "+") + (ae < 10 ? "0" : "") + ae;
    } else if (exp >= 0) {
      out = ds.slice(0, exp + 1) + (ds.length > exp + 1 ? "." + ds.slice(exp + 1) : "");
      out = out.indexOf(".") >= 0 ? out.replace(/0+$/, "").replace(/\.$/, "") : out;
    } else {
      out = ("0." + new Array(-exp).join("0") + ds).replace(/0+$/, "").replace(/\.$/, "");
    }
    return sign + out;
  }

  function tagMatch(tag, wanted) {  // tag is lower case already
    wanted = wanted.toLowerCase();
    return tag === wanted || tag.indexOf(wanted + ".") === 0;
  }

  // weapon_attributes.accepts(): a sub-slot filter (native 0x67A2B40).
  function accepts(f, item) {
    var lower = function (xs) { return (xs || []).map(function (x) { return x.toLowerCase(); }); };
    var anyCtx = function (wanted) {
      return item.ctx.some(function (t) { return (wanted || []).some(function (a) { return tagMatch(t, a); }); });
    };
    var allowed = lower(f.allowItems).indexOf(item.key) >= 0 || anyCtx(f.allowContext);
    var blocked = lower(f.blockItems).indexOf(item.key) >= 0 || anyCtx(f.blockContext);
    if (f.mode === "AllowList") return allowed;
    if (f.mode === "BlockList") return !blocked;
    if (f.mode === "AllowPriority") return allowed || !blocked;
    return allowed && !blocked;  // BlockPriority
  }

  // ------------------------------------------------------------------------- model

  function model(json) {
    var attrs = json.attributes;
    var M = {
      meta: json.meta, defaultSight: json.defaultSight, stances: json.stances.slice(),
      bipodStates: BIPOD_STATES.slice(), eps: json.eps, items: {}, weapons: [], attachments: [], effects: {}
    };
    Object.keys(json.effects).forEach(function (name) {
      M.effects[name] = json.effects[name].map(function (m) {
        var x = {attribute: attrs[m.attr], op: m.op, kind: m.kind};
        ["value", "channel", "curve", "indexing", "mode", "fallback"].forEach(function (k) {
          if (has(m, k)) x[k] = m[k];
        });
        if (has(m, "backing")) x.backing = m.backing === null ? null : attrs[m.backing];
        return x;
      });
    });
    var isAtt = {};
    json.attachments.forEach(function (id) { isAtt[id] = true; });
    Object.keys(json.items).forEach(function (id) {
      var r = json.items[id], b = r.bipod;
      var it = {
        id: id, itemId: r.itemId, key: r.itemId.toLowerCase(), display: r.display || "",
        archetype: r.archetype || null, attachmentType: r.type || null,
        isWeapon: has(r, "base"), isAttachment: !!isAtt[id],
        ctx: (r.context || []).map(function (t) { return t.toLowerCase(); }), context: r.context || [],
        applied: r.applied || [], character: r.character || [],
        sightList: r.sights || [], sights: (r.sights || []).map(function (s) { return s[0]; }),
        hasSights: !!(r.sights && r.sights.length), isBipod: !!b,
        bipodWeapon: b ? b.weapon : [], bipodCharacter: b ? b.character : [],
        mountedWeapon: b ? b.mountedWeapon : [], mountedCharacter: b ? b.mountedCharacter : [],
        base: (r.base || []).map(function (p) { return [attrs[p[0]], p[1]]; }),
        stance: has(r, "stance") ? json.stancePresets[r.stance] : {},
        slots: (r.slots || []).map(function (c) {
          return {tag: c.tag, label: slotLabel(c.tag), filter: json.filters[c.filter],
                  "default": c["default"] || null, flag: c.flag || null, accepts: null};
        })
      };
      M.items[id] = it;
    });
    json.attachments.forEach(function (id) { M.attachments.push(M.items[id]); });
    Object.keys(M.items).forEach(function (id) {
      M.items[id].slots.forEach(function (c) {
        c.accepts = M.attachments.filter(function (a) { return accepts(c.filter, a); }).map(function (a) { return a.id; });
      });
    });
    json.weapons.forEach(function (id) {
      var w = M.items[id];
      M.weapons.push({id: id, display: w.display, archetype: w.archetype});
    });
    return M;
  }

  function weaponOf(M, id) {
    var w = M.items[id];
    if (!w || !w.isWeapon) throw new Error("no weapon " + id);
    return w;
  }

  // ------------------------------------------------------------- sub-slot trees (Slot)

  function makeSlot(M, owner, c, parent) {
    var s = {key: parent ? parent + "/" + c.label : c.label, tag: c.tag, parent: parent || null, owner: owner.id,
             cont: c, item: null, children: [], flag: c.flag, user: false};
    if (c["default"]) place(M, s, M.items[c["default"]]);
    return s;
  }
  function place(M, s, item) {
    s.item = item;
    s.flag = null;
    s.children = item.slots.map(function (c) { return makeSlot(M, item, c, s.key); });
  }
  function walk(slots, out) {
    out = out || [];
    slots.forEach(function (s) { out.push(s); walk(s.children, out); });
    return out;
  }
  function slotAccepts(s, item) { return !!item && item.isAttachment && s.cont.accepts.indexOf(item.id) >= 0; }

  // Loadout(data, weapon) then Loadout.choose(items); onBad(slot, id) handles a bad choice.
  function tree(M, lo, onBad) {
    var w = weaponOf(M, lo.weapon), items = lo.items || {};
    var roots = w.slots.map(function (c) { return makeSlot(M, w, c, null); });
    (function visit(slots) {
      slots.forEach(function (s) {
        if (has(items, s.key)) {
          var id = items[s.key];
          if (id === null) {
            s.item = null;
            s.children = [];
            s.user = true;
          } else if (!slotAccepts(s, M.items[id])) {
            if (!onBad) throw new Error(id + " is not allowed in sub-slot " + s.key + " of " + w.id);
            onBad(s, id);
          } else {
            place(M, s, M.items[id]);
            s.user = true;
          }
        }
        visit(s.children);
      });
    })(roots);
    return {weapon: w, roots: roots, all: walk(roots)};
  }
  function explicit(t) {
    var items = {};
    t.all.forEach(function (s) { items[s.key] = s.item ? s.item.id : null; });
    return items;
  }
  function make(weapon, items, o) {
    o = o || {};
    return {weapon: weapon, items: items, sight: o.sight === undefined ? null : o.sight,
            stance: o.stance || "Stand", bipod: o.bipod || "folded"};
  }

  function defaultLoadout(M, weaponId) {
    return make(weaponId, explicit(tree(M, {weapon: weaponId, items: {}})));
  }

  function slots(M, lo) {
    return tree(M, lo).all.map(function (s) {
      var choice = s.item ? s.item.id : null;
      return {key: s.key, tag: s.tag, label: s.cont.label, parent: s.parent, depth: s.key.split("/").length - 1,
              owner: s.owner, accepts: s.cont.accepts.slice(), "default": s.cont["default"], choice: choice,
              isDefault: choice === s.cont["default"], flag: s.flag};
    });
  }

  function setItem(M, lo, key, itemId) {
    var t = tree(M, lo), s = t.all.filter(function (x) { return x.key === key; })[0];
    if (!s) throw new Error("no open sub-slot " + key);
    if (itemId !== null && !slotAccepts(s, M.items[itemId])) throw new Error(itemId + " is not allowed in " + key);
    var items = {};
    Object.keys(lo.items || {}).forEach(function (k) {
      if (k.indexOf(key + "/") !== 0) items[k] = lo.items[k];
    });
    items[key] = itemId;
    return make(lo.weapon, explicit(tree(M, {weapon: lo.weapon, items: items})), lo);
  }

  function sightsOf(t, defaultSight) {
    var out = [], ix = {};
    t.all.forEach(function (s) {
      if (!s.item) return;
      s.item.sights.forEach(function (n) {
        if (!has(ix, n)) { ix[n] = out.length; out.push({name: n, items: [], isDefault: n === defaultSight}); }
        if (out[ix[n]].items.indexOf(s.item.id) < 0) out[ix[n]].items.push(s.item.id);
      });
    });
    return out;
  }
  function sights(M, lo) { return sightsOf(tree(M, lo), M.defaultSight); }
  function bipodIn(t) { return t.all.some(function (s) { return s.item && s.item.isBipod; }); }
  function hasBipod(M, lo) { return bipodIn(tree(M, lo)); }

  function normalize(M, lo) {
    var dropped = [];
    lo = lo || {};
    var weapon = lo.weapon;
    if (!M.items[weapon] || !M.items[weapon].isWeapon) {
      dropped.push("weapon " + pyStr(weapon) + " (unknown; using " + M.weapons[0].id + ")");
      weapon = M.weapons[0].id;
    }
    var given = (lo.items && typeof lo.items === "object") ? lo.items : {};
    var t = tree(M, {weapon: weapon, items: given}, function (s, id) {
      dropped.push(s.key + ": " + id + " (not accepted there; default kept)");
    });
    var open = {};
    t.all.forEach(function (s) { open[s.key] = true; });
    Object.keys(given).forEach(function (k) { if (!open[k]) dropped.push(k + " (no such open sub-slot)"); });
    var sight = lo.sight === undefined ? null : lo.sight;
    if (sight !== null && !sightsOf(t, M.defaultSight).some(function (x) { return x.name === sight; })) {
      dropped.push("sight " + sight + " (no equipped item has it)");
      sight = null;
    }
    var stance = lo.stance, bipod = lo.bipod;
    if (STANCES.indexOf(stance) < 0) { if (stance !== undefined) dropped.push("stance " + stance); stance = "Stand"; }
    if (BIPOD_STATES.indexOf(bipod) < 0) { if (bipod !== undefined) dropped.push("bipod " + bipod); bipod = "folded"; }
    return {loadout: make(weapon, explicit(t), {sight: sight, stance: stance, bipod: bipod}), dropped: dropped};
  }

  // ---------------------------------------------------------- evaluation (applications/evaluate)

  function applications(M, t, lo) {
    var weapon = [], character = [], notes = [], sight = lo.sight === undefined ? null : lo.sight;
    var mounted = lo.bipod === "mounted", bipod = lo.bipod === "unfolded" || mounted;
    var DS = M.defaultSight;
    var att = t.all.filter(function (s) { return s.item; }).map(function (s) { return s.item; });
    att.forEach(function (it) {
      it.applied.forEach(function (e) { weapon.push({effect: e, stacks: 1, source: it.id}); });
      if (it.sights.length) {
        var hasS = !!sight && it.sights.indexOf(sight) >= 0;
        var name = hasS ? sight : (it.sights.indexOf(DS) >= 0 ? DS : null);
        if (sight && !hasS) {
          notes.push("`" + it.id + "` has no sight `" + sight + "`; used " + (name ? "`" + name + "`" : "no sight effects"));
        } else if (name === null) {
          notes.push("`" + it.id + "` has no `" + DS + "` sight; no sight effects applied (natively no first-entry fallback)");
        }
        it.sightList.forEach(function (p) {
          if (p[0] === name) p[1].forEach(function (e) { weapon.push({effect: e, stacks: 1, source: it.id + " sight " + name}); });
        });
      }
      if (mounted && it.isBipod) {
        it.mountedWeapon.forEach(function (e) { weapon.push({effect: e, stacks: 1, source: it.id + " bipod mounted"}); });
        it.mountedCharacter.forEach(function (e) { character.push({effect: e, source: it.id + " bipod mounted"}); });
      } else if (bipod && it.isBipod) {
        it.bipodWeapon.forEach(function (e) { weapon.push({effect: e, stacks: 1, source: it.id + " bipod unfolded"}); });
        it.bipodCharacter.forEach(function (e) { character.push({effect: e, source: it.id + " bipod unfolded"}); });
      }
      it.character.forEach(function (e) { character.push({effect: e, source: it.id}); });
    });
    if (bipod && !att.some(function (it) { return it.isBipod; })) {
      notes.push("bipod " + (mounted ? "mounted" : "unfolded") + " but no bipod attachment is equipped");
    }
    var st = has(t.weapon.stance, lo.stance) ? t.weapon.stance[lo.stance] : [];
    st.forEach(function (p) {
      weapon.push({effect: p[0], stacks: p[1], source: "stance " + lo.stance});
      if (p[2]) notes.push("stance effect " + pyStr(p[0]) + " has CustomMagnitudes, not evaluated");
    });
    return {weapon: weapon, character: character, notes: notes};
  }

  function evaluateApps(M, w, apps) {
    var order = [], contrib = {}, flags = [];
    var baseMap = {};
    w.base.forEach(function (p) { if (!has(baseMap, p[0])) baseMap[p[0]] = p[1]; });
    w.base.forEach(function (p) { if (!has(contrib, p[0])) { contrib[p[0]] = []; order.push(p[0]); } });
    apps.forEach(function (app) {
      var eff = app.effect !== null && has(M.effects, app.effect) ? M.effects[app.effect] : null;
      if (eff === null) {
        flags.push("effect `" + pyStr(app.effect) + "` (" + app.source + ") is not in ge-values.json");
        return;
      }
      eff.forEach(function (m) {
        if (!has(contrib, m.attribute)) { contrib[m.attribute] = []; order.push(m.attribute); }
        contrib[m.attribute].push({app: app, mod: m, magnitude: null, flag: null});
      });
    });
    var result = {}, busy = {};
    var baseOf = function (a) { return a !== null && a !== undefined && has(baseMap, a) ? fround(baseMap[a]) : null; };

    function current(attr) {
      if (has(result, attr)) return result[attr].final;
      if (busy[attr]) { flags.push(pyShort(attr) + ": attribute-backed cycle"); return null; }
      busy[attr] = true;
      var base = baseOf(attr), notes = [], list = has(contrib, attr) ? contrib[attr] : [];
      list.forEach(function (c) {
        var m = c.mod, n = c.app.stacks, v, eff = pyStr(c.app.effect);
        if ((m.channel || "Default") !== "Default") c.flag = "channel " + m.channel;
        if (m.kind === "Scalar") {
          if (m.curve || (m.indexing || "Fixed") !== "Fixed") {
            c.flag = "curve row or non-Fixed indexing; curve not read";
            notes.push("`" + eff + "`: " + c.flag);
            return;
          }
          v = fround(m.value || 0);
        } else if (m.kind === "Attribute") {
          var backing = m.backing;
          if (m.curve) {
            c.flag = "attribute-backed with a curve; curve not read";
            notes.push("`" + eff + "`: " + c.flag);
            return;
          }
          v = (m.mode || "Current") === "Current" ? current(backing) : baseOf(backing);
          c.flag = "evaluated live (Effects §4.2)";
          notes.push("`" + eff + "` " + pyShort(attr) + " " + OPS[m.op] + " current " + pyShort(backing) +
                     ": evaluated against its final value; the game re-evaluates it live (Effects §4.2)");
          if (v === null) return;
        } else {
          c.flag = "SetByCaller; caller value not traced";
          notes.push("`" + eff + "`: " + c.flag);
          if (!has(m, "fallback")) return;
          v = fround(m.fallback);
        }
        if (n === 0) return;
        if (m.op !== "Override") {
          var ident = m.op === "Multiply" || m.op === "Divide" ? 1.0 : 0.0;
          v = (v - ident) * n + ident;
        }
        c.magnitude = v;
      });
      var live = list.filter(function (c) { return c.magnitude !== null && c.app.stacks !== 0; });
      var overrides = live.filter(function (c) { return c.mod.op === "Override"; });
      var final;
      if (overrides.length) {
        final = overrides[0].magnitude;
        var distinct = {};
        overrides.forEach(function (c) { distinct[fmt(c.magnitude)] = true; });
        var ds = Object.keys(distinct).sort();
        if (ds.length > 1) {
          notes.push(overrides.length + " Overrides with different values (" + ds.join(", ") + "); " +
                     "the native order depends on the equip history (not determinable from data); " +
                     "the tool used the first in its own order");
        }
      } else if (base === null) {
        final = null;
        if (live.length) notes.push(pyShort(attr) + " is modified but has no base value on this weapon; not evaluated");
      } else {
        var s = {};
        OP_NAMES.forEach(function (op) {
          s[op] = live.filter(function (c) { return c.mod.op === op; }).map(function (c) { return c.magnitude; });
        });
        var mul = 1.0 + nsum(s.Multiply.map(function (v) { return v - 1.0; }));
        var div = 1.0 + nsum(s.Divide.map(function (v) { return v - 1.0; }));
        if (Math.abs(div) <= M.eps) div = 1.0;
        var comp = 1.0;
        s.MultiplyCompound.forEach(function (v) { comp *= v; });
        final = ((base + nsum(s.Add)) * mul / div) * comp + nsum(s.AddFinal);
      }
      if (final !== null && list.some(function (c) { return c.magnitude === null; })) {
        notes.push(pyShort(attr) + ": some modifiers were not evaluated, so the final value is partial");
      }
      delete busy[attr];
      result[attr] = {base: base, contrib: list, final: final, notes: notes};
      return final;
    }

    order.forEach(current);
    return {order: order, result: result, flags: flags};
  }

  function effect(M, name) {
    if (name === null || !has(M.effects, name)) return null;
    return M.effects[name].map(function (m) {
      var x = {};
      Object.keys(m).forEach(function (k) { x[k] = m[k]; });
      x.symbol = OPS[m.op] || m.op;
      return x;
    });
  }

  function evaluate(M, lo) {
    var t = tree(M, lo), a = applications(M, t, lo), ev = evaluateApps(M, t.weapon, a.weapon);
    var lflags = {};
    t.all.forEach(function (s) { if (s.flag) lflags[s.flag] = true; });
    return {
      weapon: ev.order.map(function (attr) {
        var r = ev.result[attr];
        return {
          tag: attr, label: attrLabel(attr), base: r.base, final: r.final, notes: r.notes,
          steps: r.contrib.map(function (c) {
            return {source: c.app.source, effect: c.app.effect, op: c.mod.op, symbol: OPS[c.mod.op] || c.mod.op,
                    kind: c.mod.kind, stacks: c.app.stacks, magnitude: c.magnitude,
                    backing: c.mod.kind === "Attribute" ? c.mod.backing : null, flag: c.flag};
          })
        };
      }),
      character: a.character.map(function (c) { return {effect: c.effect, source: c.source, modifiers: effect(M, c.effect)}; }),
      applications: a.weapon.map(function (x) { return {effect: x.effect, stacks: x.stacks, source: x.source}; }),
      attachments: t.all.filter(function (s) { return s.item; }).map(function (s) {
        return {key: s.key, tag: s.tag, item: s.item.id};
      }),
      hasBipod: bipodIn(t),
      notes: Object.keys(lflags).sort().concat(a.notes, ev.flags)
    };
  }

  // ------------------------------------------------------------------- the CLI (--with)

  function withTree(M, weaponId, ids) {
    var w = weaponOf(M, weaponId);
    var roots = w.slots.map(function (c) { return makeSlot(M, w, c, null); });
    ids.forEach(function (id) {
      var it = M.items[id];
      if (!it || !it.isAttachment) throw new Error(pyStr(id) + " is not an attachment");
      var free = walk(roots).filter(function (s) { return !s.user && slotAccepts(s, it); })[0];
      if (!free) throw new Error(id + " is not allowed in any free sub-slot of " + weaponId);
      place(M, free, it);
      free.user = true;
    });
    return {weapon: w, roots: roots, all: walk(roots)};
  }

  function withItems(M, weaponId, ids, opts) {
    return make(weaponId, explicit(withTree(M, weaponId, ids || [])), opts);
  }

  function quote(s) { return /^[A-Za-z0-9_.:\-]+$/.test(s) ? s : '"' + s.replace(/(["\\])/g, "\\$1") + '"'; }

  function cli(M, lo) {
    var t = tree(M, lo), target = explicit(t);
    var minimal = [], full = [], reason = null;
    t.all.forEach(function (s) {
      var id = s.item ? s.item.id : null, def = s.cont["default"];
      if (id) full.push(id);
      if (id && id !== def) minimal.push(id);
      if (!id && def && !reason) {
        reason = "the CLI cannot empty the " + s.key + " sub-slot (its default is " + def + ")";
      }
    });
    var tryList = function (ids) {
      try {
        var got = explicit(withTree(M, lo.weapon, ids));
        var keys = Object.keys(target).concat(Object.keys(got));
        for (var i = 0; i < keys.length; i++) {
          var k = keys[i];
          if (!has(got, k) || !has(target, k) || got[k] !== target[k]) {
            return "the CLI's first-free-sub-slot rule gives " + k + " = " + (has(got, k) ? pyStr(got[k]) : "no sub-slot") +
                   " instead of " + (has(target, k) ? pyStr(target[k]) : "no sub-slot");
          }
        }
        return null;
      } catch (e) {
        return "the CLI's first-free-sub-slot rule rejects the list (" + e.message + ")";
      }
    };
    var ids = minimal;
    if (!reason) {
      var r1 = tryList(minimal);
      if (r1) {
        if (!tryList(full)) ids = full;
        else reason = r1;
      }
    }
    var args = "--weapon " + quote(lo.weapon);
    if (ids.length) args += " --with " + ids.map(quote).join(" ");
    if (lo.sight !== null && lo.sight !== undefined) args += " --sight " + quote(lo.sight);
    if (lo.stance && lo.stance !== "Stand") args += " --stance " + quote(lo.stance);
    if (lo.bipod === "unfolded") args += " --bipod";
    else if (lo.bipod === "mounted") args += " --mounted";
    return {args: args, exact: reason === null, reason: reason};
  }

  return {
    model: model, defaultLoadout: defaultLoadout, slots: slots, setItem: setItem, normalize: normalize,
    sights: sights, hasBipod: hasBipod, evaluate: evaluate, cli: cli, withItems: withItems, effect: effect,
    attrLabel: attrLabel, slotLabel: slotLabel, fmt: fmt, OPS: OPS
  };
});
