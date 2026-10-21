/* Native receipt comparison; cooked resources and receipts remain private. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const native = require('./vehicle_native_ray.js');
assert.ok(process.argv[2], 'Usage: node _tools/vehicle_cooked_ray_check.js <cooked-bvh-ray-replay-v1.json>');
const bytes = fs.readFileSync(process.argv[2]), receipt = JSON.parse(bytes);
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
assert.equal(receipt.passed, true);
assert.equal(receipt.binary_sha256, 'a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37');
const cache = new Map();
for (const [file, expected] of Object.entries(receipt.source_hashes)) {
  const bytes = fs.readFileSync(file);
  assert.equal(sha(bytes), expected, file);
  const decoded = JSON.parse(bytes);
  decoded.complexImplicits = decoded.complexImplicits.map(native.prepareMesh);
  cache.set(file, decoded);
}
let cases = 0, visits = 0;
const near = (a, b) => assert.ok(Math.abs(a-b) <= 1e-9*Math.max(1, Math.abs(b)), `${a} != ${b}`);
for (const row of receipt.rows) {
  const mesh = cache.get(row.decoded_file).complexImplicits[row.implicit];
  const actual = native.raycastMesh(mesh, row.start, row.direction, row.length, row.cull);
  assert.deepEqual(actual.faceOrder, row.face_order, `BVH traversal case ${cases}`);
  assert.equal(actual.hit, row.result.hit, `Hit case ${cases}`);
  assert.equal(actual.face, row.result.face, `Face case ${cases}`);
  if (actual.hit) {
    near(actual.time, row.result.time);
    actual.position.forEach((v, i) => near(v, row.result.position[i]));
    actual.normal.forEach((v, i) => near(v, row.result.normal[i]));
  }
  visits += actual.faceOrder.length;
  cases++;
}
assert.equal(cases, receipt.cases);
assert.equal(visits, receipt.face_visits);
assert.equal(cases, 6720);
console.log(JSON.stringify({passed: true, cases, face_visits: visits, payloads: cache.size,
  receipt_sha256: sha(bytes), scope: 'Local cooked BVH traversal and triangle results; no scene/instance-transform parity'}));
