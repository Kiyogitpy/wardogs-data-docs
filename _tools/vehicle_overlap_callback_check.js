#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict');
const receipt=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
for(const row of receipt.rows){
  assert.deepEqual(row.constructor_flags.slice(0,3),[0,row.ignore_touches,row.ignore_blocks]);
  assert.deepEqual(row.world_flags.slice(0,3),[1,row.ignore_touches,row.ignore_blocks]);
  assert.equal(row.query_flags,row.skip_narrow?36:4);
}
assert.equal(receipt.rows.length,32);
console.log(JSON.stringify({passed:true,cases:receipt.rows.length,
  scope:'Callback constructor and actual overlap callsite setup: Block demotion, ignore flags and skip-narrow query flag; no world execution'}));
