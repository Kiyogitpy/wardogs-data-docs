#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict');
const {overlapActorShapes}=require('./vehicle_native_overlap');
const receipt=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
for(const [i,row]of receipt.rows.entries()){
  const shapes=row.shapes.map(shape=>({...shape,component_id:17}));
  const result=overlapActorShapes(receipt.mesh,row.rotation,row.translation,shapes,row.order,
    row.query,row.ignore_actors,row.ignore_components,row.world_center,row.radius,
    {demote:row.demote,anyHit:row.any_hit,ignoreTouches:row.scenario==='ignore_touches',ignoreBlocks:row.scenario==='ignore_blocks'});
  assert.deepEqual(result.filterCalls,row.filter_calls,`filter ${i}`);
  assert.deepEqual(result.shapeVisits,row.shape_visits,`faces ${i}`);
  assert.deepEqual(result.result,row.result,`collection ${i}`);
}
console.log(JSON.stringify({passed:true,cases:receipt.rows.length,
  scope:'Conditional two-shape sphere bounds/filter/Touch-Block collection and finalization; supplied world admission/state/order, no postfilter'}));
