/* Compare the browser's blast amount with a private frozen-native replay receipt. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const impact = require('../assets/js/vehicle-impact.js');

if (!process.argv[2]) throw new Error('Usage: node _tools/vehicle_blast_falloff_check.js <native-receipt.json>');
const receipt = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
assert.ok(receipt.cases.length > 0, 'Native falloff cases are required');
const bits = Buffer.alloc(4);
for (const row of receipt.cases) {
  const amount = impact.blastAmount(row.source, row.distance);
  assert.equal(amount, row.native_amount, `${row.source.id}: ${row.distance} cm`);
  bits.writeFloatLE(amount);
  assert.equal(bits.readUInt32LE().toString(16).padStart(8, '0'), row.native_amount_bits);
}
console.log(JSON.stringify({passed: true, cases: receipt.cases.length,
  scope: 'Per-hit blast amount only; no scene gathering, damage rules or health routing invocation'}));
