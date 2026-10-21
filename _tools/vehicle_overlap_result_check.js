#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict');
const {deduplicateOverlapResults}=require('./vehicle_native_overlap');
const receipt=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
for(const [index,row]of receipt.rows.entries()){
  function converted(r){return {marker:r.marker,
    component:{index:r.component,serial:r.component?100+r.component:0,valid:r.component!==0,instanced:row.instanced},
    itemIndex:r.item,physicsOwner:r.owner?0x8000000+16*r.owner:0,blocking:r.response===2};}
  const initial=row.initial.map(converted),incoming=row.input.map(converted);
  const actual=deduplicateOverlapResults(initial,incoming);
  const output=actual.results.map(r=>({marker:r.marker,component:r.component.index,item:r.itemIndex,
    owner:r.physicsOwner?(r.physicsOwner-0x8000000)/16:0,blocking:r.blocking}));
  assert.deepEqual(output,row.output,`dedup ${index}`);
  assert.equal(actual.anyBlocking,row.any_blocking,`blocking ${index}`);
}
console.log(JSON.stringify({passed:true,cases:receipt.rows.length,
  scope:'Native overlap result classification/dedup ordering and block upgrades; supplied converted identity records, owned native weak-pointer registry, no allocation growth'}));
