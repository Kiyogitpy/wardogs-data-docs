#!/usr/bin/env node
'use strict';
const fs = require('fs');
const assert = require('assert');
const { meshSphereQuery } = require('./vehicle_native_overlap');
const receipt = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
for (const [index, row] of receipt.rows.entries()) {
  assert.equal(row.queries.length, 1, `query ${index}`);
  const query = row.queries[0];
  assert.deepStrictEqual(query.scale, row.scale, `scale ${index}`);
  const factor = Math.fround(Math.fround(1/row.scale[0])*row.scale[0]);
  assert.equal(query.radius, Math.fround(row.radius*factor), `radius ${index}`);
  const result = meshSphereQuery(receipt.mesh, query.center, query.radius, query.scale,
    { min: query.bounds.slice(0, 3), max: query.bounds.slice(3) });
  assert.equal(result.overlap, row.overlap, `overlap ${index}`);
  assert.deepStrictEqual(result.faceOrder, row.face_order, `traversal ${index}`);
  assert.equal(row.continued, true);
}
console.log(JSON.stringify({ passed: true, cases: receipt.rows.length,
  scope: 'Scaled/transformed actor sphere dispatch; native query bounds/center supplied, exact local overlap/traversal and radius' }));
