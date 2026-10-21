#!/usr/bin/env node
'use strict';
const fs = require('fs');
const assert = require('assert');
const { meshSphere } = require('./vehicle_native_overlap');
const receipt = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
function cross(a, b) {
  return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];
}
function inverseRotate(q, v) {
  const xyz = q.slice(0, 3).map(x => -x);
  const t = cross(xyz, v).map(x => 2*x);
  const c = cross(xyz, t);
  return v.map((x, i) => (x+q[3]*t[i])+c[i]);
}
function multiply(a, b) {
  const c = cross(a, b);
  return [0, 1, 2].map(i => a[3]*b[i]+a[i]*b[3]+c[i])
    .concat(a[3]*b[3]-a[0]*b[0]-a[1]*b[1]-a[2]*b[2]);
}
for (const [index, row] of receipt.rows.entries()) {
  assert.equal(row.dispatches.length, 1, `dispatch ${index}`);
  const query = row.dispatches[0];
  const q = row.shape_rotation ? multiply(row.rotation, row.shape_rotation) : row.rotation;
  const shapeOffset = row.shape_translation ? inverseRotate(
    row.rotation.map((x, i) => i < 3 ? -x : x), row.shape_translation) : [0, 0, 0];
  const local = inverseRotate(q, row.world_center.map((x, i) => x-(row.translation[i]+shapeOffset[i])));
  for (let i = 0; i < 3; i++) {
    assert(Math.abs(query.center[i]-local[i]) <= 1e-10*Math.max(1, Math.abs(local[i])), `pose ${index}/${i}`);
  }
  assert.deepStrictEqual(query.scale, [1, 1, 1]);
  const result = meshSphere(receipt.mesh, query.center, row.radius, query.scale);
  assert.equal(result.overlap, row.overlap, `overlap ${index}`);
  assert.deepStrictEqual(result.faceOrder, row.face_order, `traversal ${index}`);
  assert.equal(row.continued, true);
}
console.log(JSON.stringify({ passed: true, cases: receipt.rows.length,
  scope: 'Single-shape actor unscaled/transformed no-MTD dispatch, supplied admission/poses; local transform checked numerically, geometry/traversal exact' }));
