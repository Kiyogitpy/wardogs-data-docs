'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const E = require('../assets/js/loadout-eval.js');
const fs = require('node:fs');
const optimizerPath = require('node:path').join(__dirname, '../assets/js/loadout-optimize.js');
const O = fs.existsSync(optimizerPath) ? require(optimizerPath) : {};
const V = 'Attribute.Gameplay.Weapon.VerticalRecoilMultiplier';
const H = 'Attribute.Gameplay.Weapon.HorizontalRecoilMultiplier';
function fixture() {
  return E.model({meta: {}, eps: 1e-8, defaultSight: 'S_Aim01', stances: ['Stand', 'Crouch', 'Prone'],
    attributes: [V, H], stancePresets: [{}],
    filters: [{mode: 'AllowList', allowItems: ['a', 'b', 'c']}],
    effects: {a: [{attr: 0, op: 'Multiply', kind: 'Scalar', value: 0.5}],
      b: [{attr: 1, op: 'Multiply', kind: 'Scalar', value: 0.5}],
      c: [0, 1].map(attr => ({attr, op: 'Multiply', kind: 'Scalar', value: 0.7}))},
    weapons: ['w'], attachments: ['a', 'b', 'c'], items: {
      w: {itemId: 'w', base: [[0, 2], [1, 4]], stance: 0,
        slots: [{tag: 'Item.Attachment.Muzzle', filter: 0, default: null}]},
      a: {itemId: 'a', applied: ['a']}, b: {itemId: 'b', applied: ['b']}, c: {itemId: 'c', applied: ['c']}
    }});
}
test('chooses distinct vertical, horizontal and equal-weight normalized RMS optima without mutating input', () => {
  assert.equal(typeof O.optimize, 'function');
  const model = fixture(), lo = E.defaultLoadout(model, 'w');
  const before = JSON.stringify({model, lo});
  const result = O.optimize(model, lo);
  assert.equal(result.vertical.loadout.items.Muzzle, 'a');
  assert.equal(result.horizontal.loadout.items.Muzzle, 'b');
  assert.equal(result.overall.loadout.items.Muzzle, 'c');
  assert.equal(result.vertical.vertical, 1);
  assert.equal(result.horizontal.horizontal, 2);
  assert.equal(result.overall.score, Math.fround(0.7));
  assert.ok(result.count > 0);
  assert.equal(JSON.stringify({model, lo}), before);
});
test('ties preserve current equipment including children instead of stripping default mechanical parts', () => {
  const model = fixture();
  model.items.a.applied = model.items.b.applied = model.items.c.applied = [];
  model.items.w.slots[0].default = 'b';
  model.items.c.slots = [{label: 'Child', tag: 'Item.Attachment.Child', default: 'b', accepts: ['b'], flag: null}];
  const lo = E.setItem(model, E.defaultLoadout(model, 'w'), 'Muzzle', 'c');
  const result = O.optimize(model, lo);
  for (const goal of ['vertical', 'horizontal', 'overall']) {
    assert.deepEqual(result[goal].loadout, lo);
    assert.equal(result[goal].changes, 0);
  }
});
test('searches alternate parent branches while preserving chosen optic path, sight entry, stance and bipod', () => {
  const model = fixture();
  const sight = {label: 'Sight', tag: 'Item.Attachment.Sight', default: 'c', accepts: ['c'], flag: null};
  const grip = {label: 'Underbarrel', tag: 'Item.Attachment.Underbarrel', default: 'd', accepts: ['d'], flag: null};
  model.items.w.slots[0] = {label: 'Handguard', tag: 'Item.Attachment.Handguard', default: 'a', accepts: ['a', 'b', 'e'], flag: null};
  model.items.a.applied = [];
  model.items.a.slots = [sight];
  model.items.b.applied = ['a']; model.items.b.slots = [grip];
  model.items.c.applied = []; model.items.c.hasSights = true;
  model.items.c.sights = ['S_Aim01', 'S_Aim02'];
  model.items.c.sightList = [['S_Aim01', []], ['S_Aim02', ['b']]];
  model.items.d = {...model.items.a, id: 'd', itemId: 'd', key: 'd', slots: [], applied: ['a']};
  model.items.e = {...model.items.a, id: 'e', itemId: 'e', key: 'e', slots: [sight, grip]};
  model.items.w.stance = {Crouch: [['c', 1, 0]]};
  const lo = {...E.defaultLoadout(model, 'w'), sight: 'S_Aim02', stance: 'Crouch', bipod: 'mounted'};
  const result = O.optimize(model, lo);
  assert.equal(result.vertical.loadout.items.Handguard, 'e');
  for (const goal of ['vertical', 'horizontal', 'overall']) {
    const candidate = result[goal];
    assert.equal(candidate.loadout.items['Handguard/Sight'], 'c');
    assert.equal(candidate.loadout.sight, 'S_Aim02');
    assert.equal(candidate.loadout.stance, 'Crouch');
    assert.equal(candidate.loadout.bipod, 'mounted');
    assert.deepEqual(E.normalize(model, candidate.loadout).dropped, []);
    const baseline = {...E.defaultLoadout(model, 'w'), stance: lo.stance, bipod: lo.bipod};
    const rows = E.evaluate(model, baseline).weapon;
    const dv = rows.find(r => r.tag === V).final, dh = rows.find(r => r.tag === H).final;
    assert.equal(candidate.score, Math.sqrt(((candidate.vertical / dv) ** 2 + (candidate.horizontal / dh) ** 2) / 2));
  }
});
test('does not score missing or unreliable recoil data', () => {
  const corruptions = [
    m => { m.items.w.base = [[V, 2]]; },
    m => { m.items.w.base[0][1] = Infinity; },
    m => { m.items.w.base[0][1] = -1; },
    m => { m.items.w.stance = {Stand: [['unknown', 1, 0]]}; },
    m => { m.effects.bad = [{attribute: V, op: 'Multiply', kind: 'Scalar', value: 0.2, curve: 'unread'}];
      m.items.w.stance = {Stand: [['bad', 1, 0]]}; },
    m => { m.effects.bad = [{attribute: V, op: 'Multiply', kind: 'SetByCaller', fallback: 0.1}];
      m.items.w.stance = {Stand: [['bad', 1, 0]]}; },
    m => { m.effects.bad = [1, 2].map(value => ({attribute: V, op: 'Override', kind: 'Scalar', value}));
      m.items.w.stance = {Stand: [['bad', 1, 0]]}; }
  ];
  for (const corrupt of corruptions) {
    const model = fixture(); model.items.w.slots = []; corrupt(model);
    const result = O.optimize(model, E.defaultLoadout(model, 'w'));
    assert.deepEqual([result.vertical, result.horizontal, result.overall, result.count], [null, null, null, 0]);
    assert.ok(result.notes.length > 0);
  }
});
test('collapses recoil-neutral leaf combinations exactly instead of evaluating the Cartesian product', () => {
  const model = fixture();
  model.items.a.applied = model.items.b.applied = model.items.c.applied = [];
  for (let i = 0; i < 7; i++) {
    const id = 'neutral' + i;
    model.items[id] = {...model.items.a, id, itemId: id, key: id};
  }
  model.items.w.slots = Array.from({length: 4}, (_, i) => ({
    label: 'Leaf' + i, tag: 'Item.Attachment.Leaf' + i, default: 'a',
    accepts: ['a', 'b', 'c', ...Array.from({length: 7}, (_, j) => 'neutral' + j)], flag: null
  }));
  const lo = E.defaultLoadout(model, 'w');
  const result = O.optimize(model, lo);
  assert.equal(result.count, 1);
  assert.deepEqual(result.overall.loadout, lo);
});
test('equal-change ties prefer slot defaults over arbitrary replacement parts', () => {
  const model = fixture();
  model.items.a.applied = model.items.b.applied = model.items.c.applied = [];
  model.items.w.slots[0].default = 'b';
  const lo = E.setItem(model, E.defaultLoadout(model, 'w'), 'Muzzle', 'c');
  const result = O.optimize(model, lo, {allowed: id => id !== 'c'});
  assert.equal(result.overall.loadout.items.Muzzle, 'b');
});
test('zero default recoil keeps axis goals but reports normalized overall as unavailable', () => {
  const model = fixture(); model.items.w.base[0][1] = 0;
  const result = O.optimize(model, E.defaultLoadout(model, 'w'));
  assert.ok(result.vertical && result.horizontal);
  assert.equal(result.vertical.score, null);
  assert.equal(result.overall, null);
  assert.equal(result.normalizationUnavailable, true);
  assert.ok(result.notes.length > 0);
});
test('rejects recoil modifiers on unresolved channels even when attribute-backed values are numeric', () => {
  const model = fixture();
  model.items.w.base[1][1] = 0.1;
  model.effects.a = [{attribute: V, op: 'Override', kind: 'Attribute', backing: H, channel: 'Other'}];
  const result = O.optimize(model, E.defaultLoadout(model, 'w'));
  assert.equal(result.vertical.loadout.items.Muzzle, 'c');
});
test('reports rejected uncertain candidates without making them winners', () => {
  const model = fixture(); model.items.a.applied = ['unknown'];
  const result = O.optimize(model, E.defaultLoadout(model, 'w'));
  assert.equal(result.vertical.loadout.items.Muzzle, 'c');
  assert.equal(result.rejected, 1);
  assert.equal(result.evaluated, result.count + result.rejected);
  assert.ok(result.notes.length > 0);
});
test('can preserve an explicitly empty current slot without newly stripping default parts', () => {
  const model = fixture();
  model.items.w.slots[0].default = 'b';
  model.items.a.applied = model.items.b.applied = model.items.c.applied = [];
  const normal = E.defaultLoadout(model, 'w');
  assert.equal(O.optimize(model, normal).overall.loadout.items.Muzzle, 'b');
  const empty = E.setItem(model, normal, 'Muzzle', null);
  const result = O.optimize(model, empty);
  assert.deepEqual(result.overall.loadout, empty);
});
// Independent small-tree oracle: deliberately enumerates every compatible equipment combination.
function brute(model, input, allowed = () => true) {
  const current = E.normalize(model, input).loadout;
  const baseline = {...E.defaultLoadout(model, current.weapon), stance: current.stance, bipod: current.bipod};
  const values = lo => {
    const rows = E.evaluate(model, lo).weapon;
    return [rows.find(r => r.tag === V).final, rows.find(r => r.tag === H).final];
  };
  const [dv, dh] = values(baseline), candidates = [];
  const fixed = E.slots(model, current).filter(s => /sight|optic/i.test(s.label) || (s.choice && model.items[s.choice].hasSights));
  function visit(lo, index) {
    const slots = E.slots(model, lo);
    if (index === slots.length) {
      if (!allowed(lo.weapon) || slots.some(s => s.choice && !allowed(s.choice)) ||
          fixed.some(s => lo.items[s.key] !== s.choice)) return;
      const [vertical, horizontal] = values(lo);
      const changes = new Set([...Object.keys(current.items), ...Object.keys(lo.items)]);
      candidates.push({loadout: lo, vertical, horizontal,
        score: Math.sqrt(((vertical / dv) ** 2 + (horizontal / dh) ** 2) / 2),
        changes: [...changes].filter(k => (current.items[k] || null) !== (lo.items[k] || null)).length,
        nonDefaults: slots.filter(s => !s.isDefault).length});
      return;
    }
    const s = slots[index], choices = s.accepts.length ? [...s.accepts] : [s.default];
    if ((!s.default || current.items[s.key] === null) && !choices.includes(null)) choices.push(null);
    for (const id of choices) {
      if (id !== null && !allowed(id)) continue;
      visit(E.setItem(model, lo, s.key, id), index + 1);
    }
  }
  visit(current, 0);
  const goals = {vertical: ['vertical', 'horizontal', 'changes', 'nonDefaults'],
    horizontal: ['horizontal', 'vertical', 'changes', 'nonDefaults'], overall: ['score', 'changes', 'nonDefaults']};
  return Object.fromEntries(Object.entries(goals).map(([name, keys]) => {
    const sorted = [...candidates].sort((a, b) => {
      for (const k of keys) if (a[k] !== b[k]) return a[k] - b[k];
      return 0;
    });
    return [name, sorted[0] || null];
  }));
}
test('matches exhaustive brute force across nested branches, tradeoffs and transitive recoil backing attributes', () => {
  const model = fixture(), D = 'Attribute.Gameplay.Weapon.AimTime';
  model.items.w.base.push([D, 1]);
  for (const effects of Object.values(model.effects)) for (const m of effects) m.op = 'MultiplyCompound';
  model.effects.c.push({attribute: D, op: 'Multiply', kind: 'Scalar', value: 0.8});
  model.effects.live = [{attribute: V, op: 'MultiplyCompound', kind: 'Attribute', backing: D}];
  model.items.w.stance = {Crouch: [['live', 1, 0]]};
  const child = (label, defaultId) => ({label, tag: 'Item.Attachment.' + label,
    default: defaultId, accepts: ['a', 'b', 'c'], flag: null});
  model.items.p = {...model.items.a, id: 'p', itemId: 'p', key: 'p', applied: [], slots: [child('Muzzle', 'a')]};
  model.items.q = {...model.items.p, id: 'q', itemId: 'q', key: 'q',
    slots: [child('Muzzle', 'c'), child('Underbarrel', null)]};
  model.items.w.slots = [{...child('Barrel', 'p'), accepts: ['p', 'q']}, child('Stock', null)];
  const lo = {...E.defaultLoadout(model, 'w'), stance: 'Crouch', bipod: 'unfolded'};
  for (const blocked of [[], ['a'], ['p'], ['a', 'q']]) {
    const allowed = id => !blocked.includes(id);
    const expected = brute(model, lo, allowed), actual = O.optimize(model, lo, {allowed});
    for (const goal of ['vertical', 'horizontal', 'overall']) {
      for (const k of ['vertical', 'horizontal', 'score', 'changes', 'nonDefaults']) {
        assert.equal(actual[goal][k], expected[goal][k], `${goal}.${k}, blocked=${blocked}`);
      }
    }
  }
});
test('browser UMD export is usable without Node globals', () => {
  const vm = require('node:vm'), context = {WDLoadout: E};
  vm.createContext(context);
  vm.runInContext(fs.readFileSync(optimizerPath, 'utf8'), context);
  assert.equal(typeof context.WDLoadoutOptimizer.optimize, 'function');
  const model = fixture();
  assert.equal(context.WDLoadoutOptimizer.optimize(model, E.defaultLoadout(model, 'w')).overall.loadout.items.Muzzle, 'c');
});
test('all real weapons return normalized, fully eligible candidates at fixed stance and bipod', () => {
  const model = E.model(require('../assets/data/weapon-loadouts.json'));
  const unlocks = require('../assets/data/loadout-extras.json').unlocks;
  const allowed = id => !unlocks[id] || Object.entries(unlocks[id]).some(([cls, [level]]) => cls === 'Infantry' && level <= 40);
  for (const w of model.weapons) {
    for (const restriction of [undefined, {allowed}]) {
      const lo = {...E.defaultLoadout(model, w.id), stance: 'Prone', bipod: 'mounted'};
      const result = O.optimize(model, lo, restriction);
      if (restriction && !allowed(w.id)) { assert.equal(result.locked, true); continue; }
      for (const goal of ['vertical', 'horizontal', 'overall']) {
        if (!result[goal]) continue;
        const candidate = result[goal];
        assert.deepEqual(E.normalize(model, candidate.loadout).dropped, [], w.id);
        assert.equal(candidate.loadout.stance, 'Prone'); assert.equal(candidate.loadout.bipod, 'mounted');
        assert.ok(Number.isFinite(candidate.vertical) && candidate.vertical >= 0);
        assert.ok(Number.isFinite(candidate.horizontal) && candidate.horizontal >= 0);
        if (restriction) assert.ok(E.evaluate(model, candidate.loadout).attachments.every(a => allowed(a.item)));
      }
    }
  }
});
test('AK74M with RedDot and Crouch matches real-data exhaustive search and preserves optic', () => {
  const model = E.model(require('../assets/data/weapon-loadouts.json'));
  const lo = E.withItems(model, 'ID_AK74M', ['ID_RedDot'], {stance: 'Crouch'});
  const expected = brute(model, lo), actual = O.optimize(model, lo);
  assert.equal(actual.count, 216);
  for (const goal of ['vertical', 'horizontal', 'overall']) {
    assert.equal(actual[goal].loadout.items.Sight, 'ID_RedDot');
    assert.equal(actual[goal].loadout.stance, 'Crouch');
    for (const k of ['vertical', 'horizontal', 'score', 'changes', 'nonDefaults']) {
      assert.equal(actual[goal][k], expected[goal][k], `${goal}.${k}`);
    }
  }
  assert.equal(actual.overall.loadout.items['Barrel/Muzzle'], 'ID_MUZL_020');
  assert.equal(actual.overall.loadout.items.Underbarrel, 'ID_FGP_02');
});
test('locked weapons have no candidates', () => {
  const model = fixture();
  const result = O.optimize(model, E.defaultLoadout(model, 'w'), {allowed: id => id !== 'w'});
  assert.deepEqual([result.vertical, result.horizontal, result.overall, result.count], [null, null, null, 0]);
  assert.equal(result.locked, true);
});
test('allowed enforces class/level-style eligibility for every equipped nested default', () => {
  const model = fixture();
  model.items.c.slots = [{label: 'Child', tag: 'Item.Attachment.Child', default: 'a', accepts: ['a'], flag: null}];
  const result = O.optimize(model, E.defaultLoadout(model, 'w'), {allowed: id => id !== 'a'});
  assert.equal(result.vertical.loadout.items.Muzzle, 'b');
  for (const goal of ['vertical', 'horizontal', 'overall']) {
    assert.ok(E.evaluate(model, result[goal].loadout).attachments.every(a => a.item !== 'a'));
  }
});
