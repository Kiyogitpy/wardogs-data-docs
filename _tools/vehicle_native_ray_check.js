/* Compare the portable visitor model with private raw-native replay receipts. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const native = require('./vehicle_native_ray.js');
const receiptPath = process.argv[2];
assert.ok(receiptPath, 'Usage: node _tools/vehicle_native_ray_check.js <native-triangle-ray-replay-v3.json>');
const bytes = fs.readFileSync(receiptPath), receipt = JSON.parse(bytes);
assert.equal(receipt.passed, true);
assert.equal(receipt.binary_sha256, 'a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37');
let count = 0;
function check(vertices, triangles, start, direction, length, cull, expected) {
  const actual = native.raycast(vertices, triangles, start, direction, length, cull);
  assert.equal(actual.hit, expected.hit);
  assert.equal(actual.face, expected.face);
  if (actual.hit) assert.ok(Math.abs(actual.time-expected.time) <= 1e-12*Math.max(1, Math.abs(expected.time)));
  count++;
}
for (const row of receipt.rows) {
  check(row.vertices, row.triangles, row.start, row.direction, row.length, row.cull, row.result);
}
const triangle = [[0,0,0],[100,0,0],[0,100,0]];
for (const row of receipt.order_cases) {
  const height = 10 + (row.scenario === 'round_down' ? 2e-7 : 7e-7);
  const z = row.scenario === 'round_down' ? 1e-7 : row.scenario === 'round_up' ? -1e-7 : 0;
  const vertices = triangle.concat(triangle.map(([x,y]) => [x,y,z]));
  const faces = [[0,1,2],[3,4,5]];
  if (row.reverse) faces.reverse();
  check(vertices, faces, [25,25,height], [0,0,-1], 11, false, row.result);
}
for (const row of receipt.degenerate_cases) {
  const s = row.scale;
  check([[0,0,0],[s,0,0],[0,s,0]], [[0,1,2]], [s/4,s/4,10], [0,0,-1], 11, row.cull, row.result);
}
assert.equal(count, receipt.cases);
assert.equal(count, 1184);
console.log(JSON.stringify({passed: true, cases: count,
  receipt_sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
  scope: 'Both native index-width fixtures; supplied face order, no BVH or world-transform parity'}));
