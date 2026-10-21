/* Ray-hit math only; object identity/physical-material filling is excluded. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const native = require('./vehicle_native_ray.js');
assert.ok(process.argv[2], 'Usage: node _tools/vehicle_ray_conversion_check.js <ray-hit-conversion-replay-v1.json>');
const bytes = fs.readFileSync(process.argv[2]), receipt = JSON.parse(bytes);
assert.equal(receipt.passed, true);
assert.equal(receipt.binary_sha256, 'a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37');
const decode = bits => bits.map(x => Buffer.from(x, 'hex').readDoubleLE());
const near = (a, b) => assert.ok(Math.abs(a-b) <= 1e-9*Math.max(1, Math.abs(b)), `${a} != ${b}`);
let cases = 0, accepted = 0;
for (const row of receipt.rows) {
  const x = row.input, expected = row.result;
  const actual = native.convertRayHitMath(x.start, x.end, x.length, x.distance, x.flags,
    decode(x.position_bits), decode(x.normal_bits));
  assert.equal(actual.accepted, expected.accepted, `Acceptance case ${cases}`);
  if (actual.accepted) {
    assert.equal(actual.time, expected.time);
    assert.equal(actual.distance, expected.distance);
    assert.equal(actual.flags, expected.flags);
    for (const [a, b] of [['location','location'],['impactPoint','impact_point'],['normal','normal'],['impactNormal','impact_normal']]) {
      actual[a].forEach((v, i) => near(v, expected[b][i]));
    }
    accepted++;
  }
  cases++;
}
assert.equal(cases, 1016);
assert.equal(accepted, receipt.accepted);
console.log(JSON.stringify({passed: true, cases, accepted,
  receipt_sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
  scope: 'Native ray-hit math with null query geometry and supplied Block response; object/face/material outputs excluded'}));
