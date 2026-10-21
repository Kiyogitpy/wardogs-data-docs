/* Bounds + native query gate/filter + blocking iteration comparison. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const native = require('./vehicle_native_ray.js');
assert.ok(process.argv[2], 'Usage: node _tools/vehicle_multi_shape_ray_check.js <multi-shape-ray-replay-v1.json>');
const bytes = fs.readFileSync(process.argv[2]), receipt = JSON.parse(bytes);
assert.equal(receipt.passed, true);
assert.equal(receipt.binary_sha256, 'a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37');
const near = (a, b) => assert.ok(Math.abs(a-b) <= 1e-9*Math.max(1, Math.abs(b)), `${a} != ${b}`);
let cases = 0, unspecified = 0;
for (const row of receipt.rows) {
  // The native fixture's component-ID adapter returns 17 for this actor.
  const shapes = row.shapes.map(shape => ({...shape, component_id: 17}));
  const actual = native.raycastActorShapes(receipt.mesh, row.rotation, row.translation, shapes,
    row.order, row.query, row.ignore_actors, row.ignore_components, row.start, row.direction, row.length, row.cull);
  assert.deepEqual(actual.filterCalls, row.filter_calls, `Filter case ${cases}`);
  assert.deepEqual(actual.shapeVisits, row.shape_visits, `Geometry visits case ${cases}`);
  assert.equal(actual.hit, row.result.hit, `Hit case ${cases}`);
  assert.equal(actual.continued, row.result.continued, `Continuation case ${cases}`);
  near(actual.fastLength, row.result.fast_length);
  if (actual.hit) {
    assert.equal(actual.shape, row.result.shape);
    assert.equal(actual.face, row.result.face);
    assert.equal(actual.flags, row.result.flags);
    assert.equal(actual.distance, row.result.distance);
    if (actual.geometryOutputsWritten) {
      actual.position.forEach((v, i) => near(v, row.result.position[i]));
      actual.normal.forEach((v, i) => near(v, row.result.normal[i]));
    } else {
      assert.equal(actual.distance, 0);
      unspecified++;
    }
  }
  cases++;
}
assert.equal(cases, 3328);
assert.equal(cases, receipt.cases);
console.log(JSON.stringify({passed: true, cases, unspecified_geometry_output_cases: unspecified,
  receipt_sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
  scope: 'Two-shape bounds/gate/filter/blocking loop; supplied bounds/filter records and fast-ray flags, ignore touches, postfilter disabled'}));
