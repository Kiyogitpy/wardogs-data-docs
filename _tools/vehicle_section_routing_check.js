/* Compare the preview with private native section-routing fixtures. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const impact = require('../assets/js/vehicle-impact.js');

if (!process.argv[2]) throw new Error('Usage: node _tools/vehicle_section_routing_check.js <native-receipt.json>');
const receipt = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
assert.ok(receipt.cases.length > 0, 'Native routing cases are required');
for (const row of receipt.cases) {
  const health = {...row.initial_health}, transfers = [];
  const handled = impact.applyRadial(row.sections, health, row.section, row.amount, 0, transfers);
  assert.deepEqual(health, row.result.health, `${row.name}: ${row.section} health`);
  assert.equal(handled, row.result.handled, `${row.name}: ${row.section} handled`);
  assert.deepEqual(transfers.map(({section, amount}) => ({section, amount})), row.result.events,
    `${row.name}: ordered health changes`);
}
console.log(JSON.stringify({passed: true, cases: receipt.cases.length,
  scope: 'Native routing and clamp with owned attribute services; no live modifiers, replication or destroy callback'}));
