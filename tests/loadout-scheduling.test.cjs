'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const code = fs.readFileSync(path.join(__dirname, '../assets/js/loadout-calculator.js'), 'utf8');
const scheduling = code.slice(code.indexOf('  function scheduleRecommendations()'), code.indexOf('  function update(hash)'));
function harness(useWorker) {
  const jobs = [], workers = [], rendered = [];
  let calls = 0;
  const section = { attributes: {}, setAttribute(k, v) { this.attributes[k] = v; } };
  const context = {
    lo: { weapon: 'test', items: {} }, gate: { role: 'Support', level: 21 },
    model: { items: { test: {} } }, X: {}, optimizerJson: {},
    optimizerWorker: null, optimizerTimer: null, optimizerKey: null, optimizerJob: 0,
    els: { recommendations: section, recommendationStatus: { textContent: '' }, recoilCompare: { textContent: 'old results' }, recoilCurrent: { textContent: '' } },
    root: { getAttribute() { return '/worker.js'; } },
    allowed() { return true; }, recommendationScope() { return 'scope'; },
    renderRecommendations(result) { rendered.push(result); },
    setTimeout(fn) { jobs.push(fn); return jobs.length; }, clearTimeout() {},
    window: { WDLoadoutOptimizer: { optimize() { calls++; return {}; } } }
  };
  if (useWorker) {
    function Worker() { workers.push(this); }
    Worker.prototype.postMessage = function (payload) { this.payload = payload; };
    Worker.prototype.terminate = function () { this.terminated = true; };
    context.Worker = context.window.Worker = Worker;
  }
  vm.createContext(context); vm.runInContext(scheduling, context);
  return { context, workers, rendered, section, get calls() { return calls; }, flush() { while (jobs.length) jobs.shift()(); } };
}

test('missing Workers never runs a blocking optimizer on the UI thread', () => {
  const h = harness(false);
  h.context.scheduleRecommendations(); h.flush();
  assert.equal(h.calls, 0, 'must not run synchronous optimization on the main thread');
  assert.equal(h.section.attributes['aria-busy'], 'false');
  assert.match(h.context.els.recommendationStatus.textContent, /worker|background/i);
});

test('progression changes clear old results and reject out-of-order worker replies', () => {
  const h = harness(true);
  h.context.scheduleRecommendations(); h.flush();
  const old = h.workers[0];
  h.context.gate.level = 5;
  h.context.scheduleRecommendations();
  assert.equal(h.context.els.recoilCompare.textContent, '');
  assert.equal(old.terminated, true);
  h.flush();
  old.onmessage({ data: { id: old.payload.id, result: { stale: true } } });
  assert.equal(h.rendered.length, 0);
  const current = h.workers[1];
  current.onmessage({ data: { id: current.payload.id, result: { current: true } } });
  assert.equal(h.rendered.length, 1);
  assert.equal(h.rendered[0].current, true);
});

test('worker loading failure leaves the editor usable without a synchronous fallback', () => {
  const h = harness(true);
  h.context.scheduleRecommendations(); h.flush();
  h.workers[0].onerror({ preventDefault() {} }); h.flush();
  assert.equal(h.calls, 0);
  assert.equal(h.section.attributes['aria-busy'], 'false');
  assert.match(h.context.els.recommendationStatus.textContent, /manual editor/i);
});

test('worker constructor and postMessage errors do not block manual editing', () => {
  for (const failure of ['constructor', 'postMessage']) {
    const h = harness(true);
    function BrokenWorker() { if (failure === 'constructor') throw new Error('unavailable'); }
    BrokenWorker.prototype.postMessage = function () { throw new Error('clone failed'); };
    BrokenWorker.prototype.terminate = function () {};
    h.context.Worker = h.context.window.Worker = BrokenWorker;
    h.context.scheduleRecommendations(); h.flush();
    assert.equal(h.calls, 0);
    assert.equal(h.section.attributes['aria-busy'], 'false');
    assert.match(h.context.els.recommendationStatus.textContent, /manual editor/i);
  }
});

test('stale worker errors cannot clear a newer worker', () => {
  const h = harness(true);
  h.context.scheduleRecommendations(); h.flush();
  const old = h.workers[0];
  h.context.gate.level = 3; h.context.scheduleRecommendations(); h.flush();
  const current = h.workers[1];
  old.onerror({ preventDefault() {} });
  assert.notEqual(current.terminated, true);
  current.onmessage({ data: { id: current.payload.id, result: { current: true } } });
  assert.equal(h.rendered.length, 1);
});

test('superseded debounce callbacks cannot start stale searches', () => {
  const h = harness(true);
  h.context.scheduleRecommendations();
  h.context.gate.level = 3; h.context.scheduleRecommendations();
  h.flush();
  assert.equal(h.workers.length, 1);
  assert.equal(h.workers[0].payload.id, 2);
});
