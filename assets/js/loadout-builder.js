/* Loadout Builder (content/loadout-builder.md; styles in _sass/custom/loadout-builder.scss). UI only:
   every rule (which sub-slots a choice opens, what a slot accepts, sights, evaluation) comes from
   window.WDLoadout (assets/js/loadout-eval.js); the recoil spray plot comes from window.WDRecoil
   (assets/js/loadout-recoil.js, optional: the panel shows only when it is loaded).
   Data (all fetched; the extras and the recoil data are optional):
     weapon-loadouts.json   attributes and attachments        loadout-extras.json   unlocks, reticles, ballistics
     loadout-builder.json   slot lists, names, prices, icons  spray-patterns.json   recoil spray model
   The whole build is in the URL hash (see writeHash). Strings from the data are set as text. */
(function () {
  "use strict";

  var L, model, X = null, B = null, spray = null, panel = null, base = "/", els = {};
  var S = null;                         // the build, see fresh()
  var pickerFid = null, pickerOnPick = null, pickerCfg = null, copyTimer = null, lastRes = null;

  // Weapon sub-slots shown as tiles: [order, player label].
  var SHOWN_SLOTS = { "Item.Attachment.Muzzle": [0, "Muzzle"], "Item.Attachment.Magazine": [1, "Magazine"],
                      "Item.Attachment.Sight": [2, "Scope"], "Item.Attachment.Underbarrel": [3, "Foregrip"] };
  var WSLOTS = [["primary", "Primary", "1", "p"], ["sidearm", "Sidearm", "2", "s"], ["special", "Special item", "3", "x"]];
  var GEAR = [["helmet", "Helmet", "h"], ["armor", "Armor", "a"], ["vest", "Tac vest", "v"], ["backpack", "Backpack", "b"]];
  var PART_NAMES = { "Head": "Head", "Neck": "Neck", "Torso.Upper": "Upper torso", "Torso.Middle": "Middle torso",
                     "Torso.Lower": "Lower torso", "Pelvis": "Pelvis", "Arm.Upper": "Upper arm", "Arm.Lower": "Forearm",
                     "Arm.Hand": "Hand", "Leg.Thigh": "Thigh", "Leg.Calf": "Calf", "Leg.Foot": "Foot" };
  var VESTS = [["None", "No armor"], ["Light", "Level 1 armor"], ["Medium", "Level 2 armor"], ["Heavy", "Level 3 armor"],
               ["SuperHeavy", "Level 4 armor"]];
  var HELMETS = [["None", "No helmet"], ["Light", "Level 1 helmet"], ["Medium", "Level 2 helmet"], ["Heavy", "Level 3 helmet"],
                 ["SuperHeavy", "Level 4 helmet"], ["Pilot", "Pilot helmet"], ["Tank", "Tank crew helmet"]];
  var DROP_PARTS = ["Head", "Torso.Upper", "Arm.Upper", "Leg.Thigh"];
  // Weapon attribute: [player label, unit, which way is better (-1 lower, 1 higher, 0 neither)], in display order.
  var HANDLING = [
    ["AimTime", "ADS time", " s", -1], ["VerticalRecoilMultiplier", "Vertical recoil", "×", -1],
    ["HorizontalRecoilMultiplier", "Horizontal recoil", "×", -1], ["SpreadMultiplier", "Spread", "×", -1],
    ["AccuracyMultiplier", "Accuracy", "×", 1], ["EquipSpeedMultiplier", "Equip speed", "×", 1],
    ["HolsterSpeedMultiplier", "Holster speed", "×", 1], ["AdsZoomMultiplier", "ADS zoom", "×", 0],
    ["MinZeroingRange", "Min zeroing", " m", 0], ["MaxZeroingRange", "Max zeroing", " m", 0], ["Length", "Length", "", 0]
  ];

  function $(id) { return document.getElementById(id); }
  function ready(fn) { if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn); else fn(); }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function fmt(x, d) { return L.fmt(x, d); }
  function clear(n) { n.textContent = ""; }
  function cssEscape(s) { return window.CSS && CSS.escape ? CSS.escape(s) : String(s).replace(/["\\]/g, "\\$&"); }

  /* ---------- data access ---------- */

  function weaponById(id) { return (model.weapons || []).filter(function (w) { return w.id === id; })[0] || null; }
  // Sight entries are socket names (S_Aim01, S_Aim02, S_AimCanted1): shown as the sight they aim through.
  function sightLabel(s) {
    var m = /^S_Aim(Canted)?0*(\d+)$/.exec(String(s));
    if (!m) return String(s);
    if (m[1]) return m[2] === "1" ? "Canted sight" : "Canted sight " + m[2];
    return m[2] === "1" ? "Main sight" : m[2] === "2" ? "Second sight" : "Sight " + m[2];
  }
  function bi(id) { return (B && B.items && B.items[id]) || null; }
  function mi(id) { return (model.items && model.items[id]) || null; }
  function nameOf(id) { var b = bi(id), m = mi(id); return (b && b.name) || (m && m.display) || String(id); }
  function iconOf(id) { var b = bi(id); return (b && b.icon) || (X && X.icons && X.icons[id]) || null; }
  function stances() { return model.stances || ["Stand", "Crouch", "Prone"]; }
  function bipodStates() { return model.bipodStates || ["folded", "unfolded", "mounted"]; }
  function roles() { return (X && X.meta.roles) || []; }
  function distances() { return (X && X.meta.distances) || [0]; }
  function hp() { return (X && X.meta.hp) || 100; }
  // "Ghillie (Dead)" variants are not equipment a player picks.
  var HIDE = { ID_GhillieArmorDry: 1, ID_GhillieHelmetDry: 1 };
  function slotIds(key) { return ((B && B.slots && B.slots[key]) || []).filter(function (id) { return !HIDE[id]; }); }

  /* ---------- level gates ---------- */

  // DT_MetaTree_Roles has one tree per class plus the Wardog tree, which gates on the Wardog (career) level.
  var WARDOG = "Wardog";
  function classRoles() { return roles().filter(function (r) { return r !== WARDOG; }); }

  function unlockText(id) {
    var u = X && X.unlocks[id];
    if (!u) return "";
    return Object.keys(u).sort().map(function (r) { return r + " level " + u[r][0]; }).join(", ");
  }
  // Items in no tree are always allowed. A Wardog tree item needs the Wardog level; a class tree item needs the
  // class level, in that class's tree when a class is chosen, in any tree with "Any class". An unset level allows all.
  function allowed(id) {
    var u = X && X.unlocks[id];
    if (!u) return true;
    return Object.keys(u).some(function (r) {
      if (r === WARDOG) return S.wardog == null || u[r][0] <= S.wardog;
      if (S.level == null) return true;
      return (!S.role || r === S.role) && u[r][0] <= S.level;
    });
  }
  function gated() { return S.wardog != null || S.level != null; }

  /* ---------- build state ---------- */

  function fresh() {
    var s = { slots: {}, gear: {}, active: "primary", stance: stances()[0], focus: false,
              role: S ? S.role : "", level: S ? S.level : null, wardog: S ? S.wardog : null,
              best: S ? S.best : { goal: "overall", skip: { "Item.Attachment.Sight": true } },
              bal: { ammo: null, helmet: "None", vest: "None", range: 0 } };
    WSLOTS.forEach(function (w) { s.slots[w[0]] = { id: null, lo: null }; });
    GEAR.forEach(function (g) { s.gear[g[0]] = null; });
    return s;
  }

  function makeLoadout(id) {
    if (!id || !weaponById(id)) return null;
    var lo = L.defaultLoadout(model, id);
    return lo;
  }

  function setWeapon(slot, id) {
    S.slots[slot] = { id: id || null, lo: makeLoadout(id) };
    if (S.slots[slot].lo) S.active = slot;
  }

  function defaultBuild() {
    S = fresh();
    var ids = slotIds("primary"), pick = ids.indexOf("ID_AK74M") >= 0 ? "ID_AK74M" : ids[0];
    if (pick) setWeapon("primary", pick);
  }

  // The bipod lists apply only with a bipod equipped; an unavailable sight entry goes back to the default.
  function settle(lo) {
    if (!lo) return;
    if (!L.hasBipod(model, lo)) lo.bipod = bipodStates()[0];
    if (lo.sight != null && !L.sights(model, lo).some(function (s) { return s.name === lo.sight; })) lo.sight = null;
  }

  function current() {
    var s = S.slots[S.active];
    if (s && s.lo) return s;
    for (var i = 0; i < WSLOTS.length; i++) if (S.slots[WSLOTS[i][0]].lo) { S.active = WSLOTS[i][0]; return S.slots[S.active]; }
    return null;
  }

  function isDefaultBuild() {
    var d = ids0();
    return WSLOTS.every(function (w) {
      var s = S.slots[w[0]];
      if (w[0] === "primary") {
        if (s.id !== d) return false;
        if (!s.lo) return true;
        return s.lo.sight == null && s.lo.bipod === bipodStates()[0] && L.slots(model, s.lo).every(function (x) { return x.isDefault; });
      }
      return !s.id;
    }) && GEAR.every(function (g) { return !S.gear[g[0]]; }) && S.stance === stances()[0] && !S.focus &&
      S.bal.helmet === "None" && S.bal.vest === "None" && S.bal.range === 0 && !S.bal.ammo;
  }
  function ids0() { var ids = slotIds("primary"); return ids.indexOf("ID_AK74M") >= 0 ? "ID_AK74M" : ids[0] || null; }

  /* ---------- hash ----------
     #p=<weapon|none>&s=…&x=…  primary, sidearm, special item (asset ids)
     &p@<slot key>=<item|none>   a non-default attachment in that weapon's open sub-slot (s@…, x@… likewise)
     &p#sight=<entry>&p#bipod=<unfolded|mounted>   per weapon
     &h=&a=&v=&b=<id>   helmet, armor, tac vest, backpack
     &on=<primary|sidearm|special>&stance=<Crouch|Prone>&focus=1&wd=<Wardog level>&cls=<class>&lvl=<class level>
     &ammo=<id>&th=<target helmet class>&ta=<target armor class>&range=<metres>
     Only what differs from the default build is written. */

  function enc(s) { return encodeURIComponent(s); }
  function levelOf(v) { var n = parseInt(v, 10); return n >= 1 ? Math.min(n, 150) : null; }

  function writeHash() {
    var p = [];
    WSLOTS.forEach(function (w) {
      var s = S.slots[w[0]], k = w[3];
      if (w[0] === "primary") { if (s.id !== ids0()) p.push("p=" + enc(s.id || "none")); }
      else if (s.id) p.push(k + "=" + enc(s.id));
      if (!s.lo) return;
      L.slots(model, s.lo).forEach(function (x) {
        if (!x.isDefault) p.push(enc(k + "@" + x.key) + "=" + enc(x.choice == null ? "none" : x.choice));
      });
      if (s.lo.sight != null) p.push(enc(k + "#sight") + "=" + enc(s.lo.sight));
      if (s.lo.bipod !== bipodStates()[0]) p.push(enc(k + "#bipod") + "=" + enc(s.lo.bipod));
    });
    GEAR.forEach(function (g) { if (S.gear[g[0]]) p.push(g[2] + "=" + enc(S.gear[g[0]])); });
    if (S.active !== "primary") p.push("on=" + S.active);
    if (S.stance !== stances()[0]) p.push("stance=" + enc(S.stance));
    if (S.focus) p.push("focus=1");
    if (S.wardog != null) p.push("wd=" + S.wardog);
    if (S.role) p.push("cls=" + enc(S.role));
    if (S.level != null) p.push("lvl=" + S.level);
    var ba = ballistics();
    if (ba && S.bal.ammo && ba.ammo.length && S.bal.ammo !== ba.ammo[0].id) p.push("ammo=" + enc(S.bal.ammo));
    if (S.bal.helmet !== "None") p.push("th=" + enc(S.bal.helmet));
    if (S.bal.vest !== "None") p.push("ta=" + enc(S.bal.vest));
    if (S.bal.range) p.push("range=" + distances()[S.bal.range]);
    var h = p.length ? "#" + p.join("&") : "";
    if (location.hash === h || (!h && !location.hash)) return;
    try { history.replaceState(null, "", h || location.pathname + location.search); } catch (e) { location.hash = h; }
  }

  function applyHash() {
    var h = location.hash.slice(1);
    if (!h) return false;
    var kv = {}, pend = {};
    WSLOTS.forEach(function (w) { pend[w[3]] = { items: {}, sight: null, bipod: bipodStates()[0] }; });
    h.split("&").forEach(function (x) {
      var i = x.indexOf("="), k, v;
      try { k = decodeURIComponent(i < 0 ? x : x.slice(0, i)); v = i < 0 ? "" : decodeURIComponent(x.slice(i + 1)); } catch (e) { return; }
      var m = /^([psx])([@#])(.+)$/.exec(k);
      if (m) {
        if (m[2] === "@") pend[m[1]].items[m[3]] = v === "none" ? null : v;
        else if (m[3] === "sight") pend[m[1]].sight = v || null;
        else if (m[3] === "bipod") pend[m[1]].bipod = v;
      } else if (k) kv[k] = v;
    });
    S = fresh();
    WSLOTS.forEach(function (w) {
      var k = w[3], id;
      if (w[0] === "primary") id = kv.p === undefined ? ids0() : kv.p === "none" ? null : kv.p;
      else id = kv[k] || null;
      if (id && slotIds(w[0]).indexOf(id) < 0) id = w[0] === "primary" ? ids0() : null;   // unknown id: the default primary
      S.slots[w[0]] = { id: id, lo: null };
      if (id && weaponById(id)) {
        var n = L.normalize(model, { weapon: id, items: pend[k].items, sight: pend[k].sight, stance: stances()[0], bipod: pend[k].bipod });
        S.slots[w[0]].lo = n.loadout;
        settle(n.loadout);
      }
    });
    GEAR.forEach(function (g) { var v = kv[g[2]]; if (v && slotIds(g[0]).indexOf(v) >= 0) S.gear[g[0]] = v; });
    if (WSLOTS.some(function (w) { return w[0] === kv.on; })) S.active = kv.on;
    if (stances().indexOf(kv.stance) >= 0) S.stance = kv.stance;
    S.focus = kv.focus === "1";
    S.role = kv.cls && classRoles().indexOf(kv.cls) >= 0 ? kv.cls : "";
    S.level = levelOf(kv.lvl);
    S.wardog = levelOf(kv.wd);
    if (kv.cls === WARDOG && S.wardog == null) { S.wardog = S.level; S.level = null; }   // links from before the Wardog level box
    S.bal.ammo = kv.ammo || null;
    S.bal.helmet = HELMETS.some(function (v) { return v[0] === kv.th; }) ? kv.th : "None";
    S.bal.vest = VESTS.some(function (v) { return v[0] === kv.ta; }) ? kv.ta : "None";
    S.bal.range = Math.max(0, distances().indexOf(Number(kv.range)));
    return true;
  }

  /* ---------- small widgets ---------- */

  function img(path, cls) {
    var i = el("img", cls);
    i.src = base + path;
    i.alt = "";
    i.decoding = "async";
    i.loading = "lazy";
    return i;
  }

  // An icon box: the picture, or the first letters of the name when there is none (or it fails to load).
  function iconBox(id, cls, name) {
    var b = el("span", "lb-icon" + (cls ? " " + cls : "")), p = id ? iconOf(id) : null;
    b.setAttribute("aria-hidden", "true");
    function letters() { clear(b); b.classList.add("lb-icon-none"); b.textContent = name ? String(name).replace(/[^A-Za-z0-9]/g, "").slice(0, 2).toUpperCase() : ""; }
    if (p) {
      var i = img(p);
      i.addEventListener("error", letters);
      b.appendChild(i);
    } else letters();
    return b;
  }

  function priceText(id) {
    var b = bi(id);
    if (!b) return "";
    if (b.price == null) return "—";
    var t = b.price === 0 ? "Free" : "$" + b.price.toLocaleString("en-US");
    return b.priceHidden ? t + " · not on sale" : t;
  }

  function status(t) { els.status.textContent = t || ""; els.status.hidden = !t; }

  function focusFid(fid) {
    if (!fid) return;
    var e = els.root.querySelector('[data-fid="' + cssEscape(fid) + '"]');
    if (e) e.focus();
  }

  /* ---------- picker ---------- */

  function openPicker(cfg, opener) {
    pickerCfg = cfg;
    pickerFid = opener ? opener.getAttribute("data-fid") : null;
    els.pickerTitle.textContent = cfg.title;
    els.pickerQ.value = "";
    renderPicker();
    if (typeof els.picker.showModal === "function") els.picker.showModal(); else els.picker.setAttribute("open", "");
    els.pickerQ.focus();
  }

  function closePicker() {
    if (els.picker.open) { if (els.picker.close) els.picker.close(); else els.picker.removeAttribute("open"); }
  }

  function renderPicker() {
    var cfg = pickerCfg, q = els.pickerQ.value.trim().toLowerCase(), box = els.pickerList, shown = 0, groups = {}, order = [];
    clear(box);
    function card(o) {
      var li = el("li"), b = el("button", "lb-opt"), locked = o.id != null && !allowed(o.id) && o.id !== cfg.current;
      b.type = "button";
      if (o.id === cfg.current) b.setAttribute("aria-pressed", "true"); else b.setAttribute("aria-pressed", "false");
      if (locked) { b.setAttribute("aria-disabled", "true"); b.classList.add("lb-locked"); }
      b.appendChild(iconBox(o.id, "lb-opt-icon", o.name));
      var t = el("span", "lb-opt-text");
      t.appendChild(el("span", "lb-opt-name", o.name));
      if (o.meta) t.appendChild(el("span", "lb-opt-meta", o.meta));
      b.appendChild(t);
      var badges = el("span", "lb-badges");
      if (o.isDefault) badges.appendChild(el("span", "lb-badge", "Default"));
      if (o.id === cfg.current) badges.appendChild(el("span", "lb-badge lb-badge-on", "Equipped"));
      var ut = o.id ? unlockText(o.id) : "";
      if (ut) badges.appendChild(el("span", "lb-badge" + (locked ? " lb-badge-lock" : ""), (locked ? "Locked · " : "Unlocks ") + ut));
      if (badges.children.length) t.appendChild(badges);
      b.addEventListener("click", function () {
        if (b.getAttribute("aria-disabled") === "true") { els.pickerCount.textContent = o.name + " is locked at your level (" + ut + ")."; return; }
        closePicker();
        cfg.onPick(o.id);
        focusFid(pickerFid);
      });
      li.appendChild(b);
      return li;
    }
    var list = el("ul", "lb-opt-list");
    if (cfg.empty != null && (!q || cfg.empty.toLowerCase().indexOf(q) >= 0)) {
      list.appendChild(card({ id: null, name: cfg.empty, meta: cfg.emptyMeta || "", isDefault: false }));
      if (cfg.current == null) list.lastChild.firstChild.setAttribute("aria-pressed", "true");
    }
    cfg.options.forEach(function (o) {
      var hay = (o.name + " " + (o.group || "") + " " + (o.meta || "")).toLowerCase();
      if (q && hay.indexOf(q) < 0) return;
      shown++;
      var g = o.group || "";
      if (!groups[g]) { groups[g] = []; order.push(g); }
      groups[g].push(o);
    });
    if (order.length === 1 && !order[0]) list.appendChild(document.createDocumentFragment());
    order.forEach(function (g) {
      var ul = order.length === 1 && !g ? list : el("ul", "lb-opt-list");
      groups[g].forEach(function (o) { ul.appendChild(card(o)); });
      if (ul !== list) {
        var sec = el("section", "lb-opt-group"), h = el("h3", "lb-opt-group-title no_anchor", g);
        sec.appendChild(h);
        sec.appendChild(ul);
        box.appendChild(sec);
      }
    });
    box.insertBefore(list, box.firstChild);
    if (!list.children.length) box.removeChild(list);
    els.pickerCount.textContent = shown + (shown === 1 ? " item" : " items") + (q ? " match" : "") +
      (gated() ? ". " + gateText() + ": locked items are greyed out." : "");
    if (!shown && !(cfg.empty != null)) box.appendChild(el("p", "lb-none", "Nothing matches."));
  }

  function optionsFor(ids, withClass) {
    return ids.map(function (id) {
      var b = bi(id), m = mi(id);
      var meta = priceText(id);
      return { id: id, name: nameOf(id), meta: meta, group: withClass ? ((b && b.class) || (m && m.archetype) || "Other") : "" };
    }).sort(function (a, b) { return a.group === b.group ? 0 : a.group.localeCompare(b.group); });
  }

  /* ---------- equipment column ---------- */

  function tile(fid, o) {
    var b = el("button", "lb-tile" + (o.cls ? " " + o.cls : ""));
    b.type = "button";
    b.setAttribute("data-fid", fid);
    var locked = o.id && !allowed(o.id);
    b.setAttribute("aria-label", locked ? o.aria.replace(/\. Change$/, ", locked at your level. Change") : o.aria);
    b.appendChild(iconBox(o.id, "lb-tile-icon", o.name));
    var t = el("span", "lb-tile-text");
    t.appendChild(el("span", "lb-tile-slot", o.slot));
    t.appendChild(el("span", "lb-tile-name", o.name || "Empty"));
    if (o.id) t.appendChild(el("span", "lb-tile-price", priceText(o.id)));
    b.appendChild(t);
    if (o.num) b.appendChild(el("span", "lb-tile-num", o.num));
    if (o.id && !allowed(o.id)) { b.classList.add("lb-tile-locked"); b.appendChild(el("span", "lb-tile-warn", "Locked")); }
    if (!o.id) b.classList.add("lb-tile-empty");
    b.addEventListener("click", function () { o.open(b); });
    return b;
  }

  function renderEquip() {
    var box = els.equip, fid = document.activeElement && box.contains(document.activeElement) ? document.activeElement.getAttribute("data-fid") : null;
    clear(box);
    WSLOTS.forEach(function (w) {
      var slot = w[0], s = S.slots[slot], row = el("div", "lb-slotrow" + (S.active === slot && s.lo ? " lb-slotrow-on" : ""));
      row.appendChild(tile("w:" + slot, {
        id: s.id, name: s.id ? nameOf(s.id) : "", slot: w[1], num: w[2], cls: "lb-tile-main",
        aria: w[1] + ": " + (s.id ? nameOf(s.id) : "empty") + ". Change",
        open: function (opener) {
          openPicker({
            title: w[1], current: s.id, empty: "Empty", options: optionsFor(slotIds(slot), true),
            onPick: function (id) { setWeapon(slot, id); if (!id && S.active === slot) S.active = "primary"; update(true); }
          }, opener);
        }
      }));
      if (s.lo) {
        var subs = el("div", "lb-subs");
        subs.setAttribute("role", "group");
        subs.setAttribute("aria-label", w[1] + " attachments");
        // Only the four slots players change are shown; barrel, stock, pistol grip and handguard keep their
        // defaults (still evaluated). The muzzle sits on the barrel, so it is a nested slot.
        L.slots(model, s.lo).filter(function (x) { return SHOWN_SLOTS[x.tag] && x.accepts && x.accepts.length; })
          .sort(function (a, b) { return SHOWN_SLOTS[a.tag][0] - SHOWN_SLOTS[b.tag][0]; })
          .forEach(function (x) {
          var label = SHOWN_SLOTS[x.tag][1], t = tile("a:" + slot + ":" + x.key, {
            id: x.choice, name: x.choice ? nameOf(x.choice) : "", slot: label, cls: "lb-mini",
            aria: label + ": " + (x.choice ? nameOf(x.choice) : "empty") + ". Change",
            open: function (opener) {
              openPicker({
                title: w[1] + ": " + label, current: x.choice, empty: "Empty", emptyMeta: x["default"] == null ? "Default" : "",
                options: optionsFor(x.accepts, false).map(function (o) { o.isDefault = o.id === x["default"]; return o; }),
                onPick: function (id) {
                  s.lo = L.setItem(model, s.lo, x.key, id);
                  settle(s.lo);
                  S.active = slot;
                  update(true);
                }
              }, opener);
            }
          });
          t.title = label + (x.choice ? ": " + nameOf(x.choice) : ": empty");
          subs.appendChild(t);
          });
        row.appendChild(subs);
      }
      box.appendChild(row);
    });
    var gear = el("div", "lb-gear");
    GEAR.forEach(function (g) {
      var id = S.gear[g[0]];
      gear.appendChild(tile("g:" + g[0], {
        id: id, name: id ? nameOf(id) : "", slot: g[1], cls: "lb-tile-gear",
        aria: g[1] + ": " + (id ? nameOf(id) : "empty") + ". Change",
        open: function (opener) {
          openPicker({
            title: g[1], current: id, empty: "Empty", options: optionsFor(slotIds(g[0]), false),
            onPick: function (nid) { S.gear[g[0]] = nid; update(true); }
          }, opener);
        }
      }));
    });
    box.appendChild(gear);
    if (fid) focusFid(fid);
  }

  /* ---------- summary ---------- */

  function renderSummary() {
    var box = els.summary, lines = [], total = 0, unknown = 0, weight = 0, wUnknown = 0, wKnown = 0;
    function add(label, id, sub) {
      var b = bi(id), p = b ? b.price : null;
      if (p == null) unknown++; else total += p;
      if (b && b.weightKg != null) { weight += b.weightKg; wKnown++; } else wUnknown++;
      lines.push({ label: label, name: nameOf(id), price: priceText(id), sub: sub, id: id });
    }
    WSLOTS.forEach(function (w) {
      var s = S.slots[w[0]];
      if (!s.id) return;
      add(w[1], s.id, false);
      if (s.lo) L.slots(model, s.lo).forEach(function (x) { if (x.choice != null && !x.isDefault) add(x.label || L.slotLabel(x.tag), x.choice, true); });
    });
    GEAR.forEach(function (g) { if (S.gear[g[0]]) add(g[1], S.gear[g[0]], false); });
    clear(box);
    var dl = el("dl", "lb-facts");
    function fact(k, v, cls) {
      dl.appendChild(el("dt", null, k));
      dl.appendChild(el("dd", cls, v));
    }
    fact("Total cost", lines.length ? "$" + total.toLocaleString("en-US") + (unknown ? " + " + unknown + " without a price" : "") : "$0", "lb-total");
    if (wKnown) fact("Weight", (wUnknown ? "at least " : "") + fmt(Math.round(weight * 100) / 100) + " kg");
    var vest = S.gear.vest && bi(S.gear.vest), bp = S.gear.backpack && bi(S.gear.backpack);
    fact("Quick slots", vest && vest.quickSlots != null ? String(vest.quickSlots) : S.gear.vest ? "not known" : "none (no tac vest)");
    fact("Bag cells", bp && bp.grid ? bp.grid[0] * bp.grid[1] + " (" + bp.grid[0] + " × " + bp.grid[1] + ")" : S.gear.backpack ? "not known" : "none (no backpack)");
    box.appendChild(dl);
    var locked = lines.filter(function (l) { return !allowed(l.id); });
    if (locked.length) box.appendChild(el("p", "lb-hint lb-warn", "Locked at your level: " + locked.map(function (l) { return l.name; }).join(", ") + "."));
    if (lines.length) {
      var ul = el("ul", "lb-break");
      lines.forEach(function (l) {
        var li = el("li", l.sub ? "lb-break-sub" : "");
        li.appendChild(el("span", "lb-break-slot", l.label));
        li.appendChild(el("span", "lb-break-name", l.name));
        li.appendChild(el("span", "lb-break-price", l.price));
        ul.appendChild(li);
      });
      box.appendChild(ul);
      box.appendChild(el("p", "lb-hint", "Attachments that come with a weapon by default are not charged separately; only the ones you change are listed."));
    } else box.appendChild(el("p", "lb-none", "Nothing equipped yet."));
  }

  /* ---------- weapon card ---------- */

  function setSeg(group, value) {
    var off = group.getAttribute("aria-disabled") === "true";
    Array.prototype.forEach.call(group.querySelectorAll("button"), function (b) {
      var on = b.value === value;
      b.setAttribute("aria-checked", String(on));
      b.tabIndex = on && !off ? 0 : -1;
    });
  }

  function seg(label, items, value, onPick, disabled) {
    var g = el("div", "lb-seg");
    g.setAttribute("role", "radiogroup");
    g.setAttribute("aria-label", label);
    if (disabled) g.setAttribute("aria-disabled", "true");
    var buttons = items.map(function (it) {
      var b = el("button", null, it[1]);
      b.type = "button";
      b.value = it[0];
      b.setAttribute("role", "radio");
      b.disabled = !!disabled;
      b.addEventListener("click", function () { if (!disabled) onPick(it[0]); });
      g.appendChild(b);
      return b;
    });
    g.addEventListener("keydown", function (e) {
      var step = e.key === "ArrowRight" || e.key === "ArrowDown" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowUp" ? -1 : 0;
      if (!step || disabled) return;
      e.preventDefault();
      var at = buttons.map(function (b) { return b.getAttribute("aria-checked") === "true"; }).indexOf(true);
      onPick(buttons[(at + step + buttons.length) % buttons.length].value);
      var again = els.weapon.querySelector('.lb-seg[aria-label="' + label + '"] [aria-checked="true"]');
      if (again) again.focus();
    });
    setSeg(g, value);
    return g;
  }

  function field(label, control) {
    var f = el("div", "lb-field lb-field-inline"), l = el("span", "lb-label", label);
    f.appendChild(l);
    f.appendChild(control);
    return f;
  }

  function ballistics() { var c = current(); return (X && c && X.ballistics[c.id]) || null; }

  function chip(k, v) {
    var c = el("div", "lb-chip");
    c.appendChild(el("span", "lb-chip-k", k));
    c.appendChild(el("span", "lb-chip-v", v));
    return c;
  }

  function renderWeapon(res) {
    var box = els.weapon, c = current();
    clear(box);
    if (!c) { box.appendChild(el("p", "lb-none", "Choose a primary weapon, sidearm or special item in the equipment column to see its values.")); return; }
    var lo = c.lo, b = bi(c.id), m = mi(c.id), ba = ballistics();
    var head = el("div", "lb-whead");
    head.appendChild(iconBox(c.id, "lb-whead-icon", nameOf(c.id)));
    var ht = el("div", "lb-whead-text");
    ht.appendChild(el("p", "lb-whead-name", nameOf(c.id)));
    ht.appendChild(el("p", "lb-whead-class", (b && b.class) || (m && m.archetype) || ""));
    if (b && b.text) ht.appendChild(el("p", "lb-whead-sub", b.text));
    head.appendChild(ht);
    box.appendChild(head);

    var chips = el("div", "lb-chips");
    if (ba && ba.rpm != null) chips.appendChild(chip("Rate of fire", fmt(ba.rpm) + " rpm"));
    if (ba && ba.effectiveRange != null) chips.appendChild(chip("Effective range", fmt(ba.effectiveRange) + " m"));
    if (ba && ba.ammo && ba.ammo.length) {
      var am = ba.ammo.filter(function (a) { return a.id === S.bal.ammo; })[0] || ba.ammo[0];
      chips.appendChild(chip("Caliber", am.label));
    }
    if (b && b.weightKg != null) chips.appendChild(chip("Weight", fmt(b.weightKg) + " kg"));
    if (chips.children.length) box.appendChild(chips);

    var controls = el("div", "lb-wcontrols");
    var avail = WSLOTS.filter(function (w) { return S.slots[w[0]].lo; });
    if (avail.length > 1) {
      controls.appendChild(field("Show", seg("Weapon shown", avail.map(function (w) { return [w[0], w[1] + ": " + nameOf(S.slots[w[0]].id)]; }), S.active,
        function (v) { S.active = v; update(true); })));
    }
    controls.appendChild(field("Stance", seg("Stance", stances().map(function (x) { return [x, x]; }), S.stance, function (v) { S.stance = v; update(true); })));
    var focusWrap = el("label", "lb-check"), cb = el("input");
    cb.type = "checkbox";
    cb.checked = S.focus;
    cb.addEventListener("change", function () { S.focus = cb.checked; update(true); });
    focusWrap.appendChild(cb);
    focusWrap.appendChild(el("span", null, "Focus"));
    focusWrap.title = "Steady aim: applied to the recoil plot below";
    if (panel) controls.appendChild(field("Recoil", focusWrap));
    var bip = res.hasBipod != null ? !!res.hasBipod : L.hasBipod(model, lo);
    controls.appendChild(field("Bipod", seg("Bipod", bipodStates().map(function (x) { return [x, x.charAt(0).toUpperCase() + x.slice(1)]; }), lo.bipod,
      function (v) { lo.bipod = v; update(true); }, !bip)));
    var sights = L.sights(model, lo);
    if (sights.length > 1) {
      var sel = el("select"), dflt = model.defaultSight || "S_Aim01";
      sel.id = "lb-sight-entry";
      var o0 = el("option", null, sightLabel(dflt) + " (initial)");
      o0.value = "";
      sel.appendChild(o0);
      sights.forEach(function (x) { if (x.isDefault) return; var o = el("option", null, sightLabel(x.name)); o.value = x.name; sel.appendChild(o); });
      sel.value = lo.sight == null ? "" : lo.sight;
      sel.setAttribute("aria-label", "Aiming sight");
      sel.addEventListener("change", function () { lo.sight = sel.value || null; update(true); });
      controls.appendChild(field("Aiming sight", sel));
    }
    box.appendChild(controls);
  }

  /* ---------- handling ---------- */

  function finalOf(res, tag) {
    var r = res.weapon.filter(function (x) { return x.tag === tag; })[0];
    return r ? r.final : null;
  }

  function signed(d) { return (d > 0 ? "+" : d < 0 ? "−" : "") + fmt(Math.abs(d)); }

  function renderHandling(res) {
    var tb = els.handlingRows, byTag = {}, rows = [], better = 0, worse = 0;
    clear(tb);
    res.weapon.forEach(function (r) { byTag[r.tag.split(".").pop()] = r; });
    HANDLING.forEach(function (h) { if (byTag[h[0]]) rows.push([h, byTag[h[0]]]); });
    res.weapon.forEach(function (r) {
      var k = r.tag.split(".").pop();
      if (!HANDLING.some(function (h) { return h[0] === k; })) rows.push([[k, r.label || L.attrLabel(r.tag), "", 0], r]);
    });
    rows.forEach(function (p) {
      var h = p[0], r = p[1], tr = el("tr"), th = el("th", null, h[1]);
      th.scope = "row";
      th.title = r.tag;
      tr.appendChild(th);
      function val(v) { return v == null ? "—" : (h[2] === "×" ? "×" + fmt(v) : fmt(v) + h[2]); }
      tr.appendChild(el("td", "lb-num", val(r.base)));
      tr.appendChild(el("td", "lb-num lb-strong", val(r.final)));
      var ch = el("td", "lb-num");
      if (r.base != null && r.final != null && fmt(r.base) !== fmt(r.final)) {
        var d = r.final - r.base, dir = h[3] === 0 ? 0 : (d < 0) === (h[3] < 0) ? 1 : -1;
        var txt = signed(d) + (h[2] === "×" ? "" : h[2]);
        var s = el("span", dir > 0 ? "lb-good" : dir < 0 ? "lb-bad" : "lb-flat", txt);
        ch.appendChild(s);
        if (r.base) ch.appendChild(el("span", "lb-pct", " (" + (d > 0 ? "+" : "−") + Math.abs(Math.round(d / r.base * 1000) / 10) + "%)"));
        ch.appendChild(el("span", "lb-sr", dir > 0 ? " better" : dir < 0 ? " worse" : " changed"));
        tr.className = dir > 0 ? "lb-row-good" : dir < 0 ? "lb-row-bad" : "lb-row-flat";
        if (dir > 0) better++; else if (dir < 0) worse++;
      } else ch.appendChild(el("span", "lb-none", "—"));
      tr.appendChild(ch);
      if (r.notes && r.notes.length) th.appendChild(el("span", "lb-dagger", " †"));
      tb.appendChild(tr);
    });
    els.handlingSum.textContent = "Base is the weapon on its own; Fitted includes every attachment, the sight, the bipod state and the stance. " +
      better + " better, " + worse + " worse than base.";
  }

  function modValue(m) {
    if (m.kind === "Attribute") return "current " + L.attrLabel(m.backing);
    if (m.kind === "SetByCaller") return "SetByCaller";
    return m.value;
  }

  // Combined effect of a list of modifiers on a multiplier that starts at 1, by the evaluator's rule
  // (first Override wins; else ((1 + ΣAdd) * (1 + Σ(Mul - 1)) / D) * ΠMulCompound + ΣAddFinal).
  function combine(mods) {
    var ov = null, add = 0, mul = 0, div = 1, comp = 1, fin = 0, ok = true;
    mods.forEach(function (m) {
      if (typeof m.value !== "number") { ok = false; return; }
      switch (m.op) {
        case "Override": if (ov == null) ov = m.value; break;
        case "Add": add += m.value; break;
        case "Multiply": mul += m.value - 1; break;
        case "Divide": div *= m.value; break;
        case "MultiplyCompound": comp *= m.value; break;
        case "AddFinal": fin += m.value; break;
        default: ok = false;
      }
    });
    if (!ok) return null;
    return ov != null ? ov : ((1 + add) * (1 + mul) / div) * comp + fin;
  }

  function humanize(attr) {
    var s = attr.split(".").pop().replace(/Multiplier$/, "").replace(/Scale$/, "");
    s = s.replace(/([a-z])([A-Z])/g, "$1 $2").toLowerCase();
    return s.charAt(0).toUpperCase() + s.slice(1);
  }
  function lowerBetter(attr) {
    if (/Stabili[sz]ation(?!Time)/.test(attr)) return false;
    if (/Sway|Time|Recoil|Spread/.test(attr)) return true;
    return null;
  }

  function renderCharacter(res) {
    var tb = els.charRows, groups = {}, order = [], hidden = 0;
    clear(tb);
    (res.character || []).forEach(function (c) {
      (c.modifiers || []).forEach(function (m) {
        if (!groups[m.attribute]) { groups[m.attribute] = []; order.push(m.attribute); }
        groups[m.attribute].push({ m: m, source: c.source, effect: c.effect });
      });
    });
    // sway first
    order.sort(function (a, b) { return (/Sway/.test(b) ? 1 : 0) - (/Sway/.test(a) ? 1 : 0) || humanize(a).localeCompare(humanize(b)); });
    order.forEach(function (attr) {
      var g = groups[attr], comb = combine(g.map(function (x) { return x.m; }));
      var active = g.filter(function (x) { return typeof x.m.value !== "number" || x.m.value !== 1 || x.m.op === "Override"; });
      if (comb != null && Math.abs(comb - 1) < 1e-9) { hidden++; return; }
      var tr = el("tr"), th = el("th", null, humanize(attr));
      th.scope = "row";
      th.title = attr;
      tr.appendChild(th);
      var td = el("td", "lb-num lb-strong");
      if (comb == null) td.textContent = "—";
      else {
        var lb = lowerBetter(attr), cls = lb == null ? "lb-flat" : (comb < 1) === lb ? "lb-good" : "lb-bad";
        td.appendChild(el("span", cls, "×" + fmt(comb)));
        td.appendChild(el("span", "lb-sr", cls === "lb-good" ? " better" : cls === "lb-bad" ? " worse" : " changed"));
      }
      tr.appendChild(td);
      var from = el("td", "lb-from");
      active.forEach(function (x, i) {
        var v = typeof x.m.value === "number" ? x.m.symbol || "" + " " : "";
        var line = el("span", "lb-from-item");
        line.appendChild(el("span", "lb-from-name", mi(x.source) ? nameOf(x.source) : x.source || x.effect));
        line.appendChild(el("span", "lb-from-val", " " + (x.m.symbol || x.m.op) + " " + (typeof x.m.value === "number" ? fmt(x.m.value) : modValue(x.m))));
        from.appendChild(line);
      });
      tr.appendChild(from);
      tb.appendChild(tr);
    });
    if (!tb.children.length) {
      var tr0 = el("tr"), t0 = el("td", "lb-none", "No sway or character effect differs from the default for this loadout.");
      t0.colSpan = 3;
      tr0.appendChild(t0);
      tb.appendChild(tr0);
    } else if (hidden) {
      var tr1 = el("tr"), t1 = el("td", "lb-none", hidden + " more effect" + (hidden === 1 ? " is" : "s are") + " listed by the game but leave the value at ×1.");
      t1.colSpan = 3;
      tr1.appendChild(t1);
      tb.appendChild(tr1);
    }
  }

  function richText(parent, text) {
    String(text).split(/(`[^`]*`)/).forEach(function (part) {
      if (part.length > 1 && part.charAt(0) === "`" && part.charAt(part.length - 1) === "`") parent.appendChild(el("code", null, part.slice(1, -1)));
      else if (part) parent.appendChild(document.createTextNode(part));
    });
  }

  function renderNotes(res) {
    var ul = els.notes;
    clear(ul);
    (res.notes || []).forEach(function (n) { var li = el("li"); richText(li, n); ul.appendChild(li); });
    L.slots(model, current().lo).forEach(function (s) {
      if (s.flag) { var li = el("li"); richText(li, s.flag); ul.appendChild(li); }
    });
  }

  /* ---------- recoil ---------- */

  function renderRecoil(res) {
    var card = els.recoilCard;
    // Launchers and the bow have no bullet model here (single shots, no ballistics): no spray panel either.
    if (!panel || !(X && X.ballistics[current().id])) { card.hidden = true; return; }
    var v = finalOf(res, "Attribute.Gameplay.Weapon.VerticalRecoilMultiplier"), h = finalOf(res, "Attribute.Gameplay.Weapon.HorizontalRecoilMultiplier");
    card.hidden = false;
    els.recoilLead.textContent = "Spray pattern of " + nameOf(current().id) + " with this loadout: vertical recoil ×" + (v == null ? "?" : fmt(v)) +
      ", horizontal ×" + (h == null ? "?" : fmt(h)) + " (attachments, bipod and " + S.stance.toLowerCase() + " stance included).";
    try {
      var mag = L.slots(model, current().lo).filter(function (x) { return x.tag === "Item.Attachment.Magazine" && x.choice != null; })[0];
      var cap = mag && bi(mag.choice) ? bi(mag.choice).capacity : null;
      panel.update({ itemAsset: current().id, vertical: v == null ? 1 : v, horizontal: h == null ? 1 : h, stance: S.stance, focus: S.focus,
                     magazine: cap == null ? undefined : cap });
    } catch (e) { els.recoilLead.textContent = "The recoil plot could not be drawn (" + e.message + ")."; }
  }

  /* ---------- sight and reticle ---------- */

  function figure(path, caption, alt, cls) {
    var f = el("figure", "lb-reticle" + (cls ? " " + cls : "")), pane = el("div", "lb-reticle-pane"), i = img(path);
    i.alt = alt;
    pane.appendChild(i);
    f.appendChild(pane);
    f.appendChild(el("figcaption", null, caption));
    return f;
  }

  function renderOptics(res) {
    var box = els.optics, c = current(), lo = c.lo, entry = lo.sight || model.defaultSight || "S_Aim01";
    clear(box);
    els.opticsCard.hidden = !X;
    if (!X) return;
    var zoom = finalOf(res, "Attribute.Gameplay.Weapon.AdsZoomMultiplier"), aim = finalOf(res, "Attribute.Gameplay.Weapon.AimTime");
    box.appendChild(el("p", "lb-lead", "Aiming zoom ×" + (zoom == null ? "?" : fmt(zoom)) + ", ADS time " + (aim == null ? "?" : fmt(aim) + " s") +
      ". Aiming with: " + sightLabel(entry).toLowerCase() + "."));
    var ids = [c.id];
    L.slots(model, lo).forEach(function (s) { if (s.choice != null) ids.push(s.choice); });
    var sights = ids.filter(function (id) { var it = mi(id); return it && it.sights && it.sights.length; });
    if (!sights.length) { box.appendChild(el("p", "lb-none", "No sight attachment equipped: the weapon aims with its own sights.")); return; }
    sights.forEach(function (id) {
      var wrap = el("div", "lb-sight"), head = el("div", "lb-sight-head");
      head.appendChild(iconBox(id, "lb-sight-icon", nameOf(id)));
      head.appendChild(el("strong", null, nameOf(id)));
      wrap.appendChild(head);
      var r = (X.reticles && X.reticles[id]) || {}, row = el("div", "lb-reticles");
      if (r.scope) row.appendChild(figure(r.scope, "Through the scope", nameOf(id) + " reticle through the scope"));
      var lens = r.entries && r.entries[entry];
      if (lens) row.appendChild(figure(lens, "Lens reticle (" + sightLabel(entry).toLowerCase() + ")", nameOf(id) + " lens reticle", "lb-reticle-lens"));
      if (row.children.length) wrap.appendChild(row);
      else wrap.appendChild(el("p", "lb-hint", "No reticle image: this sight's reticle is built inside the game's material, with no texture to show."));
      box.appendChild(wrap);
    });
  }

  /* ---------- ammunition, body parts, drop-off (ported from loadout-calculator.js) ---------- */

  function lab(list, key) { var x = list.filter(function (v) { return v[0] === key; })[0]; return x ? x[1] : key; }
  function n1(v) { return v == null ? "—" : (Math.round(v * 10) / 10).toFixed(1); }

  function shot(a, part, i) {
    var row = a.damage[part] || {}, kind = X.meta.armorKind[part] === "helmet" ? "helmet" : "vest";
    var cls = kind === "helmet" ? S.bal.helmet : S.bal.vest;
    var covered = cls !== "None" && row[cls] != null;
    var f = a.factor ? a.factor[i] : (i === 0 ? 1 : null);
    if (f == null || row.None == null) return null;
    return { dmg: (covered ? row[cls] : row.None) * f * a.pellets, armor: covered ? lab(kind === "helmet" ? HELMETS : VESTS, cls) : "" };
  }
  function kill(b, s) {
    if (!s || s.dmg <= 0) return null;
    var n = Math.ceil(hp() / s.dmg - 1e-9);
    return { shots: n, ttk: b.rpm ? (n - 1) * 60 / b.rpm : null };
  }
  function td(text, cls) { return el("td", cls, text); }

  function renderBallistics() {
    var b = ballistics(), card = els.balCard;
    card.hidden = !X;
    if (!X) return;
    if (!b || !b.ammo.length) {
      els.balControls.hidden = true;
      els.balSummary.textContent = "No bullet damage data for this weapon: launchers and the bow are not modelled here.";
      [els.partsRows, els.dropHead, els.dropRows].forEach(clear);
      els.balNote.textContent = "";
      return;
    }
    els.balControls.hidden = false;
    if (!b.ammo.some(function (a) { return a.id === S.bal.ammo; })) S.bal.ammo = b.ammo[0].id;
    clear(els.ammo);
    b.ammo.forEach(function (a) { var o = el("option", null, a.label); o.value = a.id; els.ammo.appendChild(o); });
    els.ammo.value = S.bal.ammo;
    els.thelmet.value = S.bal.helmet;
    els.tarmor.value = S.bal.vest;
    els.range.value = String(S.bal.range);
    var a = b.ammo.filter(function (x) { return x.id === S.bal.ammo; })[0], dist = distances(), i = S.bal.range, er = b.effectiveRange, pel = a.pellets > 1;
    els.balSummary.textContent = nameOf(current().id) + " with " + a.label + ": " + (b.rpm ? fmt(b.rpm) + " rounds per minute" : "rate of fire not known") +
      (pel ? ", " + a.pellets + " pellets per shot (all assumed to hit)" : "") + (er != null ? ", full damage out to " + fmt(er) + " m" : "") +
      ". At " + dist[i] + " m against a " + hp() + " HP target:";
    clear(els.partsRows);
    X.meta.locations.forEach(function (part) {
      var s = shot(a, part, i), k = kill(b, s), tr = el("tr"), th = el("th", null, PART_NAMES[part] || part);
      th.scope = "row";
      tr.appendChild(th);
      tr.appendChild(td(s ? s.armor || "—" : "—"));
      tr.appendChild(td(s ? n1(s.dmg) : "not reached", "lb-num"));
      tr.appendChild(td(k ? String(k.shots) : "—", "lb-num"));
      tr.appendChild(td(k && k.ttk != null ? k.ttk.toFixed(2) + " s" : "—", "lb-num"));
      els.partsRows.appendChild(tr);
    });
    clear(els.dropHead);
    var hr = el("tr");
    ["Distance", "Damage factor"].concat(DROP_PARTS.map(function (p) { return PART_NAMES[p]; }), ["Shots to kill, upper torso", "Time to kill, upper torso"])
      .forEach(function (t, c) { var th = el("th", c ? "lb-num" : null, t); th.scope = "col"; hr.appendChild(th); });
    els.dropHead.appendChild(hr);
    clear(els.dropRows);
    dist.forEach(function (d, j) {
      var tr = el("tr"), f = a.factor ? a.factor[j] : (j === 0 ? 1 : null);
      if (j === i) tr.className = "lb-row-on";
      var th = el("th", null, d + " m" + (er != null && d > er ? " *" : ""));
      th.scope = "row";
      tr.appendChild(th);
      tr.appendChild(td(f == null ? "not reached" : (f * 100).toFixed(1) + "%", "lb-num"));
      DROP_PARTS.forEach(function (p) { var s = shot(a, p, j); tr.appendChild(td(s ? n1(s.dmg) : "—", "lb-num")); });
      var k = kill(b, shot(a, "Torso.Upper", j));
      tr.appendChild(td(k ? String(k.shots) : "—", "lb-num"));
      tr.appendChild(td(k && k.ttk != null ? k.ttk.toFixed(2) + " s" : "—", "lb-num"));
      els.dropRows.appendChild(tr);
    });
    els.balNote.textContent = "Target helmet and armor are the enemy's, not yours. Every shot hits the named part; no reload, spread or recoil. " +
      "Damage per shot comes from the weapon and the ammunition; attachments do not change it. Damage at a distance is the point-blank damage × the weapon's falloff curve × the bullet's speed loss to drag. " +
      (er != null ? "* beyond the full-damage range. " : "") + "Armor covers the torso (level 4 also the pelvis and upper arm); a helmet covers the head (level 3, level 4 and tank crew helmets also the neck).";
  }

  /* ---------- best attachments ---------- */

  // [goal, label, the Fitted value it lowers, or null for the overall score]
  var GOALS = [["vertical", "Vertical recoil", "VerticalRecoilMultiplier"], ["horizontal", "Horizontal recoil", "HorizontalRecoilMultiplier"],
               ["overall", "Overall", null]];
  // Overall score: sum over the HANDLING values with a better direction of direction × weight × ln(Fitted / Base);
  // weight 1, except equip and holster speed 0.25. Higher is better.
  var OVERALL_W = { EquipSpeedMultiplier: 0.25, HolsterSpeedMultiplier: 0.25 };
  var bestCache = { key: null, val: null };

  function handlingOf(lo) {
    var out = {};
    L.evaluate(model, lo).weapon.forEach(function (r) { out[r.tag.split(".").pop()] = r; });
    return out;
  }
  function overallScore(h) {
    var s = 0;
    HANDLING.forEach(function (d) {
      var r = h[d[0]];
      if (d[3] && r && r.base > 0 && r.final > 0) s += d[3] * (OVERALL_W[d[0]] || 1) * Math.log(r.final / r.base);
    });
    return s;
  }
  function goalScore(h) {
    var attr = GOALS.filter(function (g) { return g[0] === S.best.goal; })[0][2];
    if (!attr) return overallScore(h);
    return h[attr] && h[attr].final != null ? -h[attr].final : -Infinity;
  }
  function better(a, b) {
    for (var i = 0; i < a.length; i++) if (Math.abs(a[i] - b[i]) > 1e-9) return a[i] > b[i];
    return false;
  }
  function bestSlots(lo) {
    return L.slots(model, lo).filter(function (x) { return SHOWN_SLOTS[x.tag] && x.accepts && x.accepts.length; })
      .sort(function (a, b) { return SHOWN_SLOTS[a.tag][0] - SHOWN_SLOTS[b.tag][0]; });
  }

  // Every combination of unlocked parts in the ticked slots (at most ~8,000, the M4), scored by the goal; ties go
  // to the overall score, then fewer changes from what is equipped, then the lower price of the changed parts.
  function searchBest(lo) {
    var now = {}, keys = [], best = null, n = 0, picks = [];
    bestSlots(lo).forEach(function (x) { now[x.key] = x.choice; if (!S.best.skip[x.tag]) keys.push(x.key); });
    (function rec(l, i) {
      if (i === keys.length) {
        settle(l);
        var h;
        try { h = handlingOf(l); } catch (e) { return; }
        n++;
        var changes = 0, price = 0;
        keys.forEach(function (k, j) {
          if (picks[j] === now[k]) return;
          changes++;
          var b = picks[j] && bi(picks[j]);
          if (b && b.price) price += b.price;
        });
        var sc = [goalScore(h), overallScore(h), -changes, -price];
        if (!best || better(sc, best.sc)) best = { sc: sc, lo: l, h: h, picks: picks.slice() };
        return;
      }
      var x = L.slots(model, l).filter(function (y) { return y.key === keys[i]; })[0];
      if (!x) { picks[i] = null; rec(l, i + 1); return; }
      var ids = x.accepts.filter(function (id) { return allowed(id) || id === x["default"]; });
      if (x.tag !== "Item.Attachment.Magazine") ids.push(null);
      ids.forEach(function (id) {
        var nl;
        try { nl = id === x.choice ? l : L.setItem(model, l, x.key, id); } catch (e) { return; }
        picks[i] = id;
        rec(nl, i + 1);
      });
    })(lo, 0);
    return best && { lo: best.lo, h: best.h, n: n, keys: keys, now: now, picks: best.picks };
  }

  function renderBest(res) {
    var box = els.best, slot = S.active, c = current(), lo = c.lo, shown = bestSlots(lo);
    clear(box);
    var controls = el("div", "lb-wcontrols");
    controls.appendChild(field("Best for", seg("Best for", GOALS.map(function (g) { return [g[0], g[1]]; }), S.best.goal,
      function (v) { S.best.goal = v; update(false); })));
    var checks = el("div", "lb-best-slots");
    checks.setAttribute("role", "group");
    checks.setAttribute("aria-label", "Slots to choose");
    shown.forEach(function (x) {
      var lab = el("label", "lb-check"), cb = el("input");
      cb.type = "checkbox";
      cb.checked = !S.best.skip[x.tag];
      cb.setAttribute("data-fid", "best:" + x.tag);
      cb.addEventListener("change", function () { S.best.skip[x.tag] = !cb.checked; update(false); focusFid("best:" + x.tag); });
      lab.appendChild(cb);
      lab.appendChild(document.createTextNode(SHOWN_SLOTS[x.tag][1]));
      checks.appendChild(lab);
    });
    controls.appendChild(field("Slots to choose", checks));
    box.appendChild(controls);

    var key = JSON.stringify([slot, lo.weapon, lo.items, lo.sight, lo.bipod, lo.stance, S.best, S.wardog, S.level, S.role]);
    if (bestCache.key !== key) bestCache = { key: key, val: searchBest(lo) };
    var r = bestCache.val;
    if (!r || !r.keys.length) { box.appendChild(el("p", "lb-none", "Tick at least one slot to choose.")); return; }

    var diff = r.keys.filter(function (k, j) { return r.picks[j] !== r.now[k]; }).length;
    box.appendChild(el("p", "lb-lead", "Tried " + r.n.toLocaleString("en-US") + (r.n === 1 ? " combination" : " combinations") + " of the parts unlocked at " +
      (gated() ? gateText() : "any level (set your levels above to limit it)") + ". " +
      (diff ? diff + (diff === 1 ? " part differs" : " parts differ") + " from what is equipped." : "What is equipped is already the best for this goal.")));

    var t1 = el("table", "lb-table lb-best-table"), tb1 = el("tbody");
    t1.appendChild(el("caption", "lb-sr", "Equipped and best part for each chosen slot"));
    var hr = el("tr");
    ["Slot", "Equipped", "Best"].forEach(function (h) { var th = el("th", null, h); th.scope = "col"; hr.appendChild(th); });
    var th1 = el("thead"); th1.appendChild(hr); t1.appendChild(th1);
    r.keys.forEach(function (k, j) {
      var x = shown.filter(function (y) { return y.key === k; })[0], same = r.picks[j] === r.now[k];
      var tr = el("tr", same ? "" : "lb-row-good"), th = el("th", null, x ? SHOWN_SLOTS[x.tag][1] : k);
      th.scope = "row";
      tr.appendChild(th);
      tr.appendChild(el("td", null, r.now[k] ? nameOf(r.now[k]) : "Empty"));
      var td = el("td", same ? null : "lb-strong", r.picks[j] ? nameOf(r.picks[j]) : "Empty");
      if (!same) td.appendChild(el("span", "lb-sr", " (change)"));
      tr.appendChild(td);
      tb1.appendChild(tr);
    });
    t1.appendChild(tb1);
    var w1 = el("div", "lb-scroll"); w1.appendChild(t1); box.appendChild(w1);

    var now = {}, t2 = el("table", "lb-table lb-best-table"), tb2 = el("tbody");
    res.weapon.forEach(function (x) { now[x.tag.split(".").pop()] = x; });
    t2.appendChild(el("caption", "lb-sr", "Handling values with what is equipped and with the best parts"));
    hr = el("tr");
    [["Value", ""], ["Equipped", "lb-num"], ["Best", "lb-num"]].forEach(function (h) { var th = el("th", h[1], h[0]); th.scope = "col"; hr.appendChild(th); });
    var th2 = el("thead"); th2.appendChild(hr); t2.appendChild(th2);
    HANDLING.forEach(function (d) {
      var a = now[d[0]], b = r.h[d[0]];
      if (!d[3] || !a || !b) return;
      function val(v) { return v == null ? "—" : (d[2] === "×" ? "×" + fmt(v) : fmt(v) + d[2]); }
      var tr = el("tr"), th = el("th", null, d[1]);
      th.scope = "row";
      tr.appendChild(th);
      tr.appendChild(el("td", "lb-num", val(a.final)));
      var td = el("td", "lb-num"), dv = b.final - a.final;
      if (a.final != null && b.final != null && fmt(a.final) !== fmt(b.final)) {
        var good = (dv < 0) === (d[3] < 0);
        td.appendChild(el("span", good ? "lb-good" : "lb-bad", val(b.final)));
        td.appendChild(el("span", "lb-sr", good ? " better" : " worse"));
      } else td.appendChild(el("span", "lb-strong", val(b.final)));
      tr.appendChild(td);
      tb2.appendChild(tr);
    });
    t2.appendChild(tb2);
    var w2 = el("div", "lb-scroll"); w2.appendChild(t2); box.appendChild(w2);

    var go = el("button", "lb-btn lb-btn-primary", diff ? "Equip these" : "Already equipped");
    go.type = "button";
    go.disabled = !diff;
    go.setAttribute("data-fid", "best:go");
    go.addEventListener("click", function () {
      S.slots[slot].lo = r.lo;
      settle(r.lo);
      update(true);
      focusFid("best:go");
    });
    box.appendChild(go);
    box.appendChild(el("p", "lb-hint", "Values use the stance and bipod chosen above. Overall adds up how much each value with a better direction " +
      "improves on the weapon's base, in proportion (ln Fitted / Base): ADS time, vertical and horizontal recoil, spread and accuracy count fully, " +
      "equip and holster speed a quarter. Barrel, stock, pistol grip and handguard stay as they are. Magazine capacity is not scored; " +
      "ties go to fewer changes, then the cheaper parts."));
  }

  /* ---------- gate bar and update ---------- */

  function renderGate() {
    var lockedAny = [];
    WSLOTS.forEach(function (w) {
      var s = S.slots[w[0]];
      if (s.id && !allowed(s.id)) lockedAny.push(nameOf(s.id));
      if (s.lo) L.slots(model, s.lo).forEach(function (x) { if (x.choice != null && !x.isDefault && !allowed(x.choice)) lockedAny.push(nameOf(x.choice)); });
    });
    GEAR.forEach(function (g) { if (S.gear[g[0]] && !allowed(S.gear[g[0]])) lockedAny.push(nameOf(S.gear[g[0]])); });
    els.gateHint.textContent = !X ? "" : !gated()
      ? "Set your Wardog level and class level to grey out what you have not unlocked yet. Some items unlock with the Wardog level, " +
        "the rest in a class tree; items that no tree lists are always available."
      : gateText() + ": locked items are greyed out in the pickers." +
        (lockedAny.length ? " Equipped but locked: " + lockedAny.join(", ") + "." : "");
    els.gateHint.classList.toggle("lb-warn", lockedAny.length > 0);
    els.role.value = S.role;
    els.level.value = S.level == null ? "" : String(S.level);
    els.wardog.value = S.wardog == null ? "" : String(S.wardog);
  }
  function gateText() {
    var p = [];
    if (S.wardog != null) p.push("Wardog level " + S.wardog);
    if (S.level != null) p.push((S.role || "any class") + " level " + S.level);
    return p.join(", ");
  }

  function update(hash) {
    var c = current();
    renderGate();
    renderEquip();
    renderSummary();
    var res = null;
    if (c) {
      c.lo.stance = S.stance;
      WSLOTS.forEach(function (w) { var s = S.slots[w[0]]; if (s.lo) { s.lo.stance = S.stance; settle(s.lo); } });
      try { res = L.evaluate(model, c.lo); } catch (err) { status("This loadout could not be evaluated (" + err.message + ")."); res = null; }
    }
    lastRes = res;
    renderWeapon(res || { weapon: [] });
    els.bestCard.hidden = !res || !bestSlots(c.lo).length;
    if (!els.bestCard.hidden) renderBest(res);
    els.handlingCard.hidden = !res;
    els.recoilCard.hidden = !res || !panel;
    els.opticsCard.hidden = !res || !X;
    els.balCard.hidden = !res || !X;
    if (res) {
      renderHandling(res);
      renderCharacter(res);
      renderNotes(res);
      renderRecoil(res);
      renderOptics(res);
      renderBallistics();
    }
    els.reset.disabled = isDefaultBuild();
    if (hash) writeHash();
  }

  function copyLink() {
    writeHash();
    var text = location.href;
    function done(ok) {
      els.copy.textContent = ok ? "Link copied" : "Press Ctrl+C to copy";
      clearTimeout(copyTimer);
      copyTimer = setTimeout(function () { els.copy.textContent = "Copy link"; }, 1800);
    }
    function fallback() {
      var ta = el("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.className = "lb-offscreen";
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      done(ok);
    }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(function () { done(true); }, fallback);
    else fallback();
  }

  function fillSelect(sel, list) {
    clear(sel);
    list.forEach(function (v) { var o = el("option", null, v[1]); o.value = v[0]; sel.appendChild(o); });
  }

  function init() {
    var root = els.root = $("lb");
    if (!root) return;
    ["status", "reset", "copy", "role", "level", "wardog", "equip", "summary", "weapon", "picker", "layout"].forEach(function (k) { els[k] = $("lb-" + k); });
    els.gateHint = $("lb-gate-hint");
    els.handlingCard = $("lb-handling-card"); els.handlingRows = $("lb-handling-rows"); els.handlingSum = $("lb-handling-sum");
    els.charRows = $("lb-char-rows"); els.notes = $("lb-notes");
    els.recoilCard = $("lb-recoil-card"); els.recoilLead = $("lb-recoil-lead"); els.recoil = $("lb-recoil");
    els.opticsCard = $("lb-optics-card"); els.optics = $("lb-optics");
    els.bestCard = $("lb-best-card"); els.best = $("lb-best");
    els.balCard = $("lb-ballistics-card"); els.balControls = root.querySelector("#lb-ballistics-card .lb-controls");
    ["ammo", "thelmet", "tarmor", "range"].forEach(function (k) { els[k] = $("lb-" + k); });
    els.balSummary = $("lb-bal-summary"); els.balNote = $("lb-bal-note");
    els.partsRows = $("lb-parts-rows"); els.dropHead = $("lb-drop-head"); els.dropRows = $("lb-drop-rows");
    els.pickerTitle = $("lb-picker-title"); els.pickerQ = $("lb-picker-q"); els.pickerList = $("lb-picker-list"); els.pickerCount = $("lb-picker-count");
    base = root.getAttribute("data-base") || "/";
    L = window.WDLoadout;
    if (!L || typeof L.model !== "function") { status("The evaluator (loadout-eval.js) did not load."); return; }

    function getJson(url) { return fetch(url).then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); }); }
    var optional = function (attr) { return getJson(root.getAttribute(attr)).catch(function () { return null; }); };
    var wantRecoil = !!(window.WDRecoil && typeof window.WDRecoil.mount === "function");
    Promise.all([getJson(root.getAttribute("data-json")), optional("data-extras"), getJson(root.getAttribute("data-builder"))])
      .then(function (all) {
        model = L.model(all[0]);
        X = all[1];
        B = all[2];
        if (!(model.weapons || []).length) throw new Error("no weapons in the data");
        fillSelect(els.thelmet, HELMETS);
        fillSelect(els.tarmor, VESTS);
        fillSelect(els.range, distances().map(function (d, j) { return [String(j), d + " m"]; }));
        var any = el("option", null, "Any class");
        any.value = "";
        clear(els.role);
        els.role.appendChild(any);
        classRoles().forEach(function (r) { var o = el("option", null, r); o.value = r; els.role.appendChild(o); });
        els.role.disabled = els.level.disabled = els.wardog.disabled = !X;
        els.copy.disabled = false;
        els.reset.disabled = false;

        els.role.addEventListener("change", function () { S.role = els.role.value; update(true); });
        els.level.addEventListener("change", function () { S.level = levelOf(els.level.value); update(true); });
        els.wardog.addEventListener("change", function () { S.wardog = levelOf(els.wardog.value); update(true); });
        els.ammo.addEventListener("change", function () { S.bal.ammo = els.ammo.value; update(true); });
        els.thelmet.addEventListener("change", function () { S.bal.helmet = els.thelmet.value; update(true); });
        els.tarmor.addEventListener("change", function () { S.bal.vest = els.tarmor.value; update(true); });
        els.range.addEventListener("change", function () { S.bal.range = parseInt(els.range.value, 10) || 0; update(true); });
        els.copy.addEventListener("click", copyLink);
        els.reset.addEventListener("click", function () {
          var role = S.role, level = S.level;
          defaultBuild();
          S.role = role;
          S.level = level;
          update(true);
          focusFid("w:primary");
        });
        els.pickerQ.addEventListener("input", renderPicker);
        $("lb-picker-close").addEventListener("click", closePicker);
        // A click on the backdrop (the dialog element itself) closes it; Escape closes it natively.
        els.picker.addEventListener("click", function (e) { if (e.target === els.picker) closePicker(); });
        els.picker.addEventListener("close", function () { focusFid(pickerFid); });
        window.addEventListener("hashchange", function () { if (applyHash()) update(false); });

        if (!applyHash()) defaultBuild();
        status("");
        els.layout.hidden = false;
        update(false);
        root.classList.add("lb-ready");
        // The spray data is 1.4 MB: fetched after the first paint, then the recoil panel appears.
        if (wantRecoil) setTimeout(function () {
          optional("data-spray").then(function (j) {
            if (!j) return;
            try { panel = window.WDRecoil.mount(els.recoil, j); } catch (e) { panel = null; }
            if (panel) update(false);
          });
        }, 50);
      })
      .catch(function (err) { status("The loadout data could not be loaded (" + err.message + ")."); });
  }

  ready(init);
})();
