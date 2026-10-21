/* Native target-sort permutations and float squared-distance key comparison. */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const impact=require('../assets/js/vehicle-impact.js');
assert.ok(process.argv[2],'Usage: node _tools/vehicle_target_sort_check.js <native-target-sort-replay-v1.json>');
const sortBytes=fs.readFileSync(process.argv[2]),sort=JSON.parse(sortBytes);
const keyBytes=fs.readFileSync(path.join(path.dirname(process.argv[2]),'target-distance-key-replay-v1.json')),keys=JSON.parse(keyBytes);
const binary='a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37';
assert.equal(sort.passed,true);assert.equal(keys.passed,true);
assert.equal(sort.input_sha256,binary);assert.equal(keys.binary_sha256,binary);
for(const[i,row]of sort.cases.entries()){
  const points=row.values.map(v=>[Math.sqrt(v)/100,0,0]),before=JSON.stringify(points);
  const sorted=impact.targetPoints(points,[0,0,0]);
  assert.deepEqual(sorted.map(t=>points.indexOf(t.position)),row.native_order,`Target permutation ${i}`);
  assert.equal(JSON.stringify(points),before);
}
for(const[i,row]of keys.rows.entries())assert.equal(impact.targetPoints([row.point],row.origin)[0].key,row.key,`Distance key ${i}`);
assert.equal(sort.cases.length,783);assert.equal(keys.cases,1029);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
console.log(JSON.stringify({passed:true,sort_cases:sort.cases.length,key_cases:keys.cases,
  heap_calls:sort.helper_calls.native_heap_fallback,sort_receipt_sha256:sha(sortBytes),key_receipt_sha256:sha(keyBytes),
  scope:'Native target float-key construction and introsort/heap permutations; supplied point/order inputs, no scene/overlap parity'}));
