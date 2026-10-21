#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict');
const receipt=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
for(const row of receipt.defaults){
  assert.equal(row.partial,0);assert.equal(row.source_mode,1);assert.equal(row.socket_mode,0);
}
for(const row of receipt.socket_cases){
  const named=BigInt(row.name)!==0n;
  assert.equal(row.matched,!named||row.exists);
  assert.equal(BigInt(row.output),!named?0n:row.exists?BigInt(row.name):BigInt(row.prior));
  assert.equal(row.callback_calls,named?1:0);
}
for(const row of receipt.gates){
  const attach=row.partial?row.resolution!==0:row.resolution===2;
  assert.equal(row.branch,attach?'attach':'unmatched');
}
assert.equal(receipt.browning.requested_name_absent,true);
console.log(JSON.stringify({passed:true,cases:receipt.cases,
  scope:'Native attachment defaults, explicit socket predicate and partial-match gate; supplied predicate responses, no engine attachment/runtime override claim'}));
