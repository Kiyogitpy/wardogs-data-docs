#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {actorSphere,scaledActorSphereInput}=require('./vehicle_native_overlap');
const {prepareMesh}=require('./vehicle_native_ray');
const receipt=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const manifest=JSON.parse(fs.readFileSync(process.argv[3]||path.join(path.dirname(process.argv[2]),'conditional-native-scenes-v1/manifest.json'),'utf8'));
const scenes=new Map(manifest.scenes.map(s=>[s.id,s])),cache=new Map();
let candidates=0,scaled=0;
for(const [index,row]of receipt.rows.entries()){
  const scene=scenes.get(row.scene),nodes=[];
  const center=[row.center[2]*100,-row.center[0]*100,row.center[1]*100],radius=Math.fround(row.radius*100);
  for(const candidate of row.candidates){
    const component=scene.native_components.find(c=>c.node_index===candidate.node_index),p=component.query;
    const resource=p.resources[0];
    if(!cache.has(resource.decoded_file))cache.set(resource.decoded_file,JSON.parse(fs.readFileSync(resource.decoded_file,'utf8')).complexImplicits.map(prepareMesh));
    const mesh=cache.get(resource.decoded_file)[resource.implicit_index];
    const actual=actorSphere(mesh,p.rotation,p.translation,null,null,p.scale,center,radius);
    assert.equal(actual.overlap,candidate.overlap,`overlap ${index}/${candidate.node_index}`);
    assert.deepEqual(actual.faceOrder,candidate.face_order,`faces ${index}/${candidate.node_index}`);
    if(p.scale){
      const input=scaledActorSphereInput(p.rotation,p.translation,null,null,p.scale,center,radius),expected=candidate.queries[0];
      assert.deepEqual(input.center,expected.center,`scaled center ${index}/${candidate.node_index}`);
      assert.deepEqual(input.bounds.min.concat(input.bounds.max).map(Math.fround),expected.bounds.map(Math.fround),`scaled bounds ${index}/${candidate.node_index}`);
      assert.equal(input.radius,expected.radius);
      scaled++;
    }
    if(actual.overlap)nodes.push(candidate.node_index);
    candidates++;
  }
  assert.deepEqual(nodes,row.nodes,`membership ${index}`);
}
console.log(JSON.stringify({passed:true,cases:receipt.rows.length,candidate_calls:candidates,scaled_candidates:scaled,
  scope:'Computed reference-pose overlap membership/traversal; supplied scene candidates/eligibility/order, no world acceleration or identity conversion'}));
