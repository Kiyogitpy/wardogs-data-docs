/* Verify exported recipes and the browser calculation against private native receipts. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const impact = require('../assets/js/vehicle-impact.js');

if (!process.argv[2]) throw new Error('Usage: node _tools/vehicle_blast_rules_check.js <native-receipt.json> [owned-receipt.json]');
const receipt = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const data = JSON.parse(fs.readFileSync(path.join(__dirname, '../assets/data/vehicle-hitboxes.json'), 'utf8'));
assert.equal(data.meta.blast_rule_recipe_format, 1);
const vehicles = new Map(data.vehicles.map(vehicle => [vehicle.id, vehicle]));
const sources = new Map(data.meta.calibers.concat(data.meta.explosives).map(source => [source.id, source]));
function recipe(row) {
  return {clamp: !!row.native.groups.length,
    operations: row.native.groups.flatMap(group => group.operations.map(op => [op.operation, op.amount]))};
}
assert.ok(receipt.cases.length > 0);
for (const row of receipt.cases) {
  const vehicle = vehicles.get(row.vehicle), slot = vehicle.slots[row.slot_index];
  const ring = row.radius === 'Inner' ? 0 : 1;
  const exported = vehicle.blast_rule_recipes[slot.blast_rule_recipe_ids[row.source][ring]];
  assert.deepEqual(exported, recipe(row), `${row.vehicle}:${row.slot_index}:${row.source}:${row.radius}`);
  assert.equal(impact.blastDamage(vehicle, row.slot_index, sources.get(row.source), ring, row.starting_amount), row.native.amount);
}
let ownedCases = 0;
if (process.argv[3]) {
  const owned = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
  for (const row of owned.cases)
    assert.equal(impact.evaluateBlastRecipe(recipe(row), row.starting_amount), row.native.amount, row.vehicle);
  ownedCases = owned.cases.length;
}
console.log(JSON.stringify({passed: true, catalog_cases: receipt.cases.length, owned_cases: ownedCases,
  scope: 'Native ordered vehicle blast rules under the declared registry/context assumptions'}));
