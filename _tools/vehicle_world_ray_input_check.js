/* World-ray input arithmetic, independent of scene admission/filtering. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const native = require('./vehicle_native_ray.js');
assert.ok(process.argv[2], 'Usage: node _tools/vehicle_world_ray_input_check.js <world-ray-input-replay-v1.json>');
const bytes = fs.readFileSync(process.argv[2]), receipt = JSON.parse(bytes);
assert.equal(receipt.passed, true);
assert.equal(receipt.binary_sha256, 'a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37');
let cases = 0;
for (const row of receipt.rows) {
  assert.deepEqual(native.worldRayInput(row.start, row.end),
    {length: row.length, admitted: row.admitted, direction: row.direction}, `Input case ${cases}`);
  cases++;
}
assert.equal(cases, 1051);
assert.equal(cases, receipt.cases);
console.log(JSON.stringify({passed: true, cases,
  receipt_sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
  scope: 'Selected world-ray arithmetic/threshold blocks; engine setup and scene traversal excluded'}));
