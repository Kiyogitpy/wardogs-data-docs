/* Compare native transformed wrapper dispatch and output contracts. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const native = require('./vehicle_native_ray.js');
assert.ok(process.argv[2], 'Usage: node _tools/vehicle_transformed_ray_check.js <transformed-mesh-ray-replay-v1.json>');
const bytes = fs.readFileSync(process.argv[2]), receipt = JSON.parse(bytes);
assert.equal(receipt.passed, true);
assert.equal(receipt.binary_sha256, 'a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37');
const near = (a, b) => assert.ok(Math.abs(a-b) <= 1e-9*Math.max(1, Math.abs(b)), `${a} != ${b}`);
let cases = 0, zeroTime = 0;
for (const row of receipt.rows) {
  const actual = native.raycastTransformedMesh(receipt.meshes[row.mesh_index], row.rotation, row.translation,
    row.scale, row.start, row.direction, row.length, row.cull);
  assert.deepEqual(actual.faceOrder, row.face_order, `Traversal case ${cases}`);
  assert.equal(actual.hit, row.result.hit, `Hit case ${cases}`);
  assert.equal(actual.face, row.result.face, `Face case ${cases}`);
  if (actual.hit) {
    near(actual.time, row.result.time);
    assert.equal(actual.outputsWritten, row.result.outputs_written);
    if (actual.outputsWritten) {
      actual.position.forEach((v, i) => near(v, row.result.position[i]));
      actual.normal.forEach((v, i) => near(v, row.result.normal[i]));
    } else {
      assert.equal(actual.position, null);
      assert.equal(actual.normal, null);
      assert.deepEqual(row.result.position, [999,999,999]);
      assert.deepEqual(row.result.normal, [999,999,999]);
      zeroTime++;
    }
  }
  cases++;
}
assert.equal(cases, 4608);
assert.equal(cases, receipt.cases);
assert.equal(zeroTime, receipt.zero_time_hits);
console.log(JSON.stringify({passed: true, cases, zero_time_hits: zeroTime,
  receipt_sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
  scope: 'Rigid transformed wrapper and optional mesh scale; no world scene membership'}));
