/* Native single-shape actor visitor, with supplied broadphase admission. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const native = require('./vehicle_native_ray.js');
assert.ok(process.argv[2], 'Usage: node _tools/vehicle_actor_ray_check.js <actor-ray-visitor-replay-v1.json>');
const bytes = fs.readFileSync(process.argv[2]), receipt = JSON.parse(bytes);
assert.equal(receipt.passed, true);
assert.equal(receipt.binary_sha256, 'a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37');
const near = (a, b) => assert.ok(Math.abs(a-b) <= 1e-9*Math.max(1, Math.abs(b)), `${a} != ${b}`);
let cases = 0, invalidOutputs = 0;
for (const row of receipt.rows) {
  const actual = native.raycastActorMesh(receipt.mesh, row.rotation, row.translation,
    row.shape_rotation, row.shape_translation, row.scale, row.start, row.direction, row.length, row.cull);
  assert.deepEqual(actual.faceOrder, row.face_order, `Traversal case ${cases}`);
  assert.equal(actual.hit, row.result.hit, `Hit case ${cases}`);
  assert.equal(actual.continued, row.result.continued, `Continuation case ${cases}`);
  near(actual.fastLength, row.result.fast_length);
  if (actual.hit) {
    assert.equal(actual.face, row.result.face);
    assert.equal(actual.flags, row.result.flags);
    assert.equal(actual.distance, row.result.distance);
    if (actual.geometryOutputsWritten) {
      actual.position.forEach((v, i) => near(v, row.result.position[i]));
      actual.normal.forEach((v, i) => near(v, row.result.normal[i]));
    } else {
      assert.equal(actual.position, null);
      assert.equal(actual.normal, null);
      invalidOutputs++;
    }
  }
  cases++;
}
assert.equal(cases, 1728);
assert.equal(cases, receipt.cases);
console.log(JSON.stringify({passed: true, cases, unspecified_geometry_output_cases: invalidOutputs,
  receipt_sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
  scope: 'Single-shape actor transform/block handling, filters disabled and broadphase admission supplied; unspecified inner outputs are not compared'}));
