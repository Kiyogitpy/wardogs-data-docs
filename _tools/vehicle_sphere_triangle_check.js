'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),crypto=require('node:crypto');
const native=require('./vehicle_native_overlap.js');
assert.ok(process.argv[2],'Usage: node _tools/vehicle_sphere_triangle_check.js <sphere-triangle-overlap-replay-v1.json>');
const bytes=fs.readFileSync(process.argv[2]),receipt=JSON.parse(bytes);
assert.equal(receipt.passed,true);
assert.equal(receipt.binary_sha256,'a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37');
for(const[i,row]of receipt.rows.entries())assert.equal(native.sphereTriangle(row.triangle,row.center,row.radius),row.overlap,`Overlap case ${i}`);
assert.equal(receipt.cases,1696);
console.log(JSON.stringify({passed:true,cases:receipt.cases,receipt_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),
  scope:'Pure float32 sphere/triangle overlap kernel; excludes BVH/transform/query admission'}));
