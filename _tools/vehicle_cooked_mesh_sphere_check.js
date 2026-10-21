'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),crypto=require('node:crypto');
const native=require('./vehicle_native_overlap.js');
assert.ok(process.argv[2],'Usage: node _tools/vehicle_cooked_mesh_sphere_check.js <cooked-mesh-sphere-overlap-replay-v1.json>');
const bytes=fs.readFileSync(process.argv[2]),receipt=JSON.parse(bytes),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(receipt.passed,true);
assert.equal(receipt.binary_sha256,'a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37');
const cache=new Map();
for(const[p,digest]of Object.entries(receipt.source_hashes)){
  const bytes=fs.readFileSync(p);assert.equal(sha(bytes),digest);cache.set(p,JSON.parse(bytes).complexImplicits);
}
let count=0,visits=0;
for(const row of receipt.rows){
  const mesh=cache.get(row.decoded_file)[row.implicit_index];
  const actual=native.meshSphere(mesh,row.center,row.radius,row.scale);
  assert.deepEqual(actual,{overlap:row.overlap,faceOrder:row.face_order},`Cooked sphere case ${count}`);
  visits+=actual.faceOrder.length;count++;
}
assert.equal(count,7560);assert.equal(count,receipt.cases);assert.equal(visits,receipt.face_visits);
console.log(JSON.stringify({passed:true,cases:count,meshes:receipt.meshes,face_visits:visits,receipt_sha256:sha(bytes),
  scope:'Native no-MTD overlap on original cooked local geometry/BVH; supplied query transform/scale, no world admission'}));
