/* Pure, synchronous recoil optimizer. Requires loadout-eval.js first in a browser;
   Node: require('./loadout-optimize.js'). Browser/Worker: WDLoadoutOptimizer.

   optimize(model, loadout, {allowed: id => boolean} = {}) returns:
     {vertical, horizontal, overall, count, evaluated, rejected, baseline, notes,
      locked?, noRecoil?, normalizationUnavailable?}
   Goals are candidate objects or null. A candidate is:
     {loadout, vertical, horizontal, score, changes, changedSlots, nonDefaults}.
   count is the number of reliable recoil-distinct representatives scored, NOT all
   cosmetic/effect-equivalent permutations. evaluated includes rejected representatives.
   changes counts equipment differences at the union of current/candidate slot paths
   (including removed children; an absent empty slot is not an equipment change).

   Axis goals minimize their axis, then the other axis. Overall is exactly
     sqrt(((V / defaultV)^2 + (H / defaultH)^2) / 2),
   where default means factory equipment at the CURRENT stance and bipod setting.
   No handling/speed stats enter the objective. Ties preserve equipment, then prefer
   slot defaults. Zero default axes disable only overall; unreliable default recoil
   disables all goals. Unknown effects are conservatively considered unreliable.

   Compatible parent and child combinations are searched together. Ordered relevant
   effect sequences (including all transitive attribute backing dependencies) are
   exact equivalence classes; only the least-change/default-preferred representative
   of each is kept. No independent-per-slot greedy picks or approximate beam limits.
   Current optic/sight slot paths and sight entry are fixed. Empty choices are allowed
   only for default-empty or currently empty slots; default mechanical parts cannot
   be stripped to manufacture a better result. All equipped parts, including nested
   defaults, must pass allowed(), as must the weapon. Neither argument is mutated. */
(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./loadout-eval.js'));
  else root.WDLoadoutOptimizer = factory(root.WDLoadout);
})(typeof self !== 'undefined' ? self : this, function (E) {
  'use strict';
  var V = 'Attribute.Gameplay.Weapon.VerticalRecoilMultiplier';
  var H = 'Attribute.Gameplay.Weapon.HorizontalRecoilMultiplier';
  function recoil(model, lo) {
    var evaluation = E.evaluate(model, lo), rows = evaluation.weapon, byTag = {}, checked = {}, busy = {};
    rows.forEach(function (r) { byTag[r.tag] = r; });
    // Unknown effects can target anything; do not present a partial number as an optimum.
    if (evaluation.applications.some(function (a) { return !E.effect(model, a.effect); })) return null;
    function reliable(tag) {
      if (busy[tag]) return false;
      if (checked[tag] !== undefined) return checked[tag];
      var r = byTag[tag];
      if (!r || !Number.isFinite(r.final)) return false;
      busy[tag] = true;
      var overrides = new Set();
      var valid = !evaluation.applications.some(function (a) {
        return (E.effect(model, a.effect) || []).some(function (m) {
          return m.attribute === tag && (m.channel || 'Default') !== 'Default';
        });
      }) && r.steps.every(function (s) {
        if (s.stacks === 0) return true;
        if (!Number.isFinite(s.magnitude) || !E.OPS[s.op] || s.kind === 'SetByCaller') return false;
        if (s.flag && s.flag !== 'evaluated live (Effects §4.2)') return false;
        if (s.op === 'Override') overrides.add(s.magnitude);
        return s.kind !== 'Attribute' || reliable(s.backing);
      });
      var stance = model.items[lo.weapon].stance[lo.stance] || [];
      if (stance.some(function (p) {
        return p[2] && (E.effect(model, p[0]) || []).some(function (m) { return m.attribute === tag; });
      })) valid = false;
      delete busy[tag];
      checked[tag] = valid && overrides.size <= 1;
      return checked[tag];
    }
    if (!reliable(V) || !reliable(H) || byTag[V].final < 0 || byTag[H].final < 0) return null;
    return {vertical: byTag[V].final, horizontal: byTag[H].final};
  }
  function optimize(model, loadout, options) {
    var allowed = options && options.allowed || function () { return true; };
    var current = E.normalize(model, loadout).loadout;
    var result = {vertical: null, horizontal: null, overall: null, count: 0, evaluated: 0, rejected: 0, baseline: null, notes: []};
    if (!allowed(current.weapon)) { result.locked = true; result.notes.push('The weapon is not allowed.'); return result; }
    var baseline = E.defaultLoadout(model, current.weapon);
    baseline.stance = current.stance; baseline.bipod = current.bipod;
    var defaults = recoil(model, baseline);
    result.baseline = defaults;
    if (!defaults) {
      result.noRecoil = true;
      result.notes.push('Default recoil is missing, non-finite, negative or unresolved; no reliable normalized comparison is available.');
      return result;
    }
    result.normalizationUnavailable = defaults.vertical === 0 || defaults.horizontal === 0;
    if (result.normalizationUnavailable) result.notes.push('Normalized overall recoil requires positive default recoil on both axes.');
    var fixed = {};
    E.slots(model, current).forEach(function (s) {
      if (/sight|optic/i.test(s.label) || (s.choice && model.items[s.choice].hasSights)) fixed[s.key] = s.choice;
    });
    function score(items, nonDefaults) {
      if (Object.keys(fixed).some(function (k) { return items[k] !== fixed[k]; })) return;
      var lo = Object.assign({}, current, {items: items}), r = recoil(model, lo);
      result.evaluated++;
      if (!r) { result.rejected++; return; }
      var changedSlots = Array.from(new Set(Object.keys(items).concat(Object.keys(current.items)))).filter(function (k) {
        return (items[k] || null) !== (current.items[k] || null);
      });
      var candidate = Object.assign({loadout: lo, changes: changedSlots.length, changedSlots: changedSlots, nonDefaults: nonDefaults}, r);
      candidate.score = result.normalizationUnavailable ? null : Math.sqrt((Math.pow(r.vertical / defaults.vertical, 2) + Math.pow(r.horizontal / defaults.horizontal, 2)) / 2);
      result.count++;
      function better(previous, keys) {
        if (!previous) return true;
        for (var i = 0; i < keys.length; i++) {
          var k = keys[i];
          if (candidate[k] !== previous[k]) return candidate[k] < previous[k];
        }
        return false;
      }
      if (better(result.vertical, ['vertical', 'horizontal', 'changes', 'nonDefaults'])) result.vertical = candidate;
      if (better(result.horizontal, ['horizontal', 'vertical', 'changes', 'nonDefaults'])) result.horizontal = candidate;
      if (candidate.score !== null && better(result.overall, ['score', 'changes', 'nonDefaults'])) result.overall = candidate;
    }
    // Only erase distinctions proven irrelevant to recoil (including transitive backing attributes).
    // Keep effect order and multiplicity: Override order and compensated sums must remain exact.
    var relevant = new Set([V, H]), changed = true;
    while (changed) {
      changed = false;
      Object.keys(model.effects).forEach(function (name) {
        model.effects[name].forEach(function (m) {
          if (relevant.has(m.attribute) && m.kind === 'Attribute' && m.backing && !relevant.has(m.backing)) {
            relevant.add(m.backing); changed = true;
          }
        });
      });
    }
    var effectRelevant = {}, itemEffects = {};
    Object.keys(model.effects).forEach(function (name) {
      effectRelevant[name] = model.effects[name].some(function (m) { return relevant.has(m.attribute); });
    });
    function effectsFor(id) {
      if (!id) return [];
      if (itemEffects[id]) return itemEffects[id];
      var it = model.items[id], effects = it.applied.slice();
      var sight = current.sight && it.sights.indexOf(current.sight) >= 0 ? current.sight : model.defaultSight;
      it.sightList.forEach(function (p) { if (p[0] === sight) effects = effects.concat(p[1]); });
      if (it.isBipod && current.bipod === 'mounted') effects = effects.concat(it.mountedWeapon);
      else if (it.isBipod && current.bipod === 'unfolded') effects = effects.concat(it.bipodWeapon);
      itemEffects[id] = effects.filter(function (name) { return effectRelevant[name] !== false; });
      return itemEffects[id];
    }
    function changeCount(items) {
      return Array.from(new Set(Object.keys(items).concat(Object.keys(current.items)))).filter(function (k) {
        return (items[k] || null) !== (current.items[k] || null);
      }).length;
    }
    function reduce(options) {
      var groups = new Map();
      options.forEach(function (o) {
        var signature = JSON.stringify(o.effects), previous = groups.get(signature);
        if (!previous || changeCount(o.items) < changeCount(previous.items) ||
            (changeCount(o.items) === changeCount(previous.items) && o.nonDefaults < previous.nonDefaults)) groups.set(signature, o);
      });
      return Array.from(groups.values());
    }
    function combine(left, right) {
      var out = [];
      left.forEach(function (a) { right.forEach(function (b) {
        out.push({items: Object.assign({}, a.items, b.items), effects: a.effects.concat(b.effects), nonDefaults: a.nonDefaults + b.nonDefaults});
      }); });
      return reduce(out);
    }
    function branch(c, key) {
      var choices = c.accepts.length ? c.accepts.slice() : [c.default];
      if ((!c.default || current.items[key] === null) && choices.indexOf(null) < 0) choices.unshift(null);
      var out = [];
      choices.filter(function (id) {
        return (id === null || allowed(id)) && (!Object.prototype.hasOwnProperty.call(fixed, key) || fixed[key] === id);
      }).forEach(function (id) {
        var items = {}; items[key] = id;
        var variants = [{items: items, effects: effectsFor(id), nonDefaults: id === c.default ? 0 : 1}];
        if (id) model.items[id].slots.forEach(function (child) {
          variants = combine(variants, branch(child, key + '/' + child.label));
        });
        variants.forEach(function (o) {
          if (!Object.keys(fixed).some(function (k) {
            return k.indexOf(key + '/') === 0 && o.items[k] !== fixed[k];
          })) out.push(o);
        });
      });
      return reduce(out);
    }
    var variants = [{items: {}, effects: [], nonDefaults: 0}];
    model.items[current.weapon].slots.forEach(function (c) { variants = combine(variants, branch(c, c.label)); });
    variants.forEach(function (o) { score(o.items, o.nonDefaults); });
    if (result.rejected) result.notes.push(result.rejected + ' recoil-distinct candidates were excluded for missing or unresolved recoil.');
    if (!result.count) result.notes.push('No legal, reliable loadout preserves the chosen sight and required parts.');
    return result;
  }
  return {optimize: optimize};
});
