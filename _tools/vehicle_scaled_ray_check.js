/* Native scale setup/wrapper parity on private owned-fixture receipts. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const native = require('./vehicle_native_ray.js');
assert.ok(process.argv[2], 'Usage: node _tools/vehicle_scaled_ray_check.js <scaled-mesh-ray-replay-v1-or-v2.json>');
const bytes = fs.readFileSync(process.argv[2]), receipt = JSON.parse(bytes);
assert.equal(receipt.passed, true);
assert.equal(receipt.binary_sha256, 'a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37');
const near = (a, b) => assert.ok(Math.abs(a-b) <= 1e-9*Math.max(1, Math.abs(b)), `${a} != ${b}`);
let cases = 0;
for (const row of receipt.rows) {
  const mesh = receipt.meshes ? receipt.meshes[row.mesh_index] : receipt.mesh;
  const actual = native.raycastScaledMesh(mesh, row.scale, row.start, row.direction, row.length, row.cull);
  assert.deepEqual(actual.effectiveScale, row.effective_scale);
  assert.deepEqual(actual.inverseScale, row.inverse_scale);
  assert.deepEqual(actual.faceOrder, row.face_order, `Traversal case ${cases}`);
  assert.equal(actual.hit, row.result.hit, `Hit case ${cases}`);
  assert.equal(actual.face, row.result.face, `Face case ${cases}`);
  if (actual.hit) {
    near(actual.time, row.result.time);
    actual.position.forEach((v, i) => near(v, row.result.position[i]));
    actual.normal.forEach((v, i) => near(v, row.result.normal[i]));
  }
  cases++;
}
assert.equal(cases, receipt.meshes ? 3456 : 576);
assert.equal(cases, receipt.cases);
console.log(JSON.stringify({passed: true, cases, receipt_sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
  scope: 'Native scale setter, scaled wrapper and local BVH fixtures; no rigid world transforms or live scene'}));
