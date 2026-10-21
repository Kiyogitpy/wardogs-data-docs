#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict');
const {scaledActorSphereInput,meshSphereQuery}=require('./vehicle_native_overlap');
const receipt=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
let differences=0,centerMismatches=0,boundsMismatches=0,maxInputError=0;
for(const [i,row]of receipt.rows.entries()){
  const input=scaledActorSphereInput(row.rotation,row.translation,row.shape_rotation,row.shape_translation,
    row.scale,row.world_center,row.radius);
  const expected=row.queries[0];
  assert.equal(input.radius,expected.radius,`radius ${i}`);
  assert.deepEqual(input.scale,expected.scale,`scale ${i}`);
  input.center.forEach((x,j)=>{if(x!==expected.center[j])centerMismatches++;});
  input.bounds.min.concat(input.bounds.max).forEach((x,j)=>{if(Math.fround(x)!==Math.fround(expected.bounds[j]))boundsMismatches++;});
  for(const [actual,want]of [[input.center,expected.center],
      [input.bounds.min.concat(input.bounds.max),expected.bounds]]){
    actual.forEach((x,j)=>{
      maxInputError=Math.max(maxInputError,Math.abs(x-want[j]));
      assert(Math.abs(x-want[j])<=1e-9*Math.max(1,Math.abs(want[j])),`input ${i}/${j}: ${x} != ${want[j]}`);
    });
  }
  const actual=meshSphereQuery(receipt.mesh,input.center,input.radius,input.scale,input.bounds);
  if(actual.overlap!==row.overlap||JSON.stringify(actual.faceOrder)!==JSON.stringify(row.face_order))differences++;
}
assert.equal(differences,0,`${differences} geometry/traversal differences`);
assert.equal(centerMismatches,0);
assert.equal(boundsMismatches,0);
console.log(JSON.stringify({passed:true,cases:receipt.rows.length,
  center_float_mismatches:centerMismatches,bounds_float_mismatches:boundsMismatches,max_input_error:maxInputError,
  scope:'Computed scaled actor sphere input; numerical input comparison plus exact overlap/traversal on owned fixtures'}));
