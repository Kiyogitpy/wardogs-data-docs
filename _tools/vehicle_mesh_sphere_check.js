'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),crypto=require('node:crypto');
const native=require('./vehicle_native_overlap.js');
assert.ok(process.argv[2],'Usage: node _tools/vehicle_mesh_sphere_check.js <mesh-sphere-overlap-replay-v1.json>');
const bytes=fs.readFileSync(process.argv[2]),receipt=JSON.parse(bytes);
assert.equal(receipt.passed,true);
assert.equal(receipt.binary_sha256,'a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37');
for(const[i,row]of receipt.rows.entries()){
  const min=[0,1,2].map(axis=>Math.min(...row.triangle.map(p=>p[axis])));
  const max=[0,1,2].map(axis=>Math.max(...row.triangle.map(p=>p[axis])));
  const mesh={vertices:row.triangle,triangles:[[0,1,2]],bvh:{nodes:[[
    {bounds:{min,max},childOrFaceIndex:0,faceCount:1},
    {bounds:{min:[0,0,0],max:[0,0,0]},childOrFaceIndex:-1,faceCount:0}]],faceBounds:[min.concat(max)]}};
  assert.deepEqual(native.meshSphere(mesh,row.center,row.radius,row.scale),
    {overlap:row.overlap,faceOrder:row.face_order},`Mesh-sphere case ${i}`);
}
assert.equal(receipt.cases,4032);
console.log(JSON.stringify({passed:true,cases:receipt.cases,receipt_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),
  scope:'Native mesh/sphere no-MTD fixtures including query bounds and triangle visits; no world overlap admission'}));
