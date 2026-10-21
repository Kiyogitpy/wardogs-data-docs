#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const receipt=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const wheels=JSON.parse(fs.readFileSync(path.join(path.dirname(process.argv[2]),'wheel-manager-replay-v2.json'),'utf8'));
assert.equal(receipt.binary_sha256,wheels.binary_sha256);
let accepted=0,joins=0;
for(const row of receipt.rows){
  const effective=row.multi_body?row.raw_item:-1;
  assert.equal(row.effective_item,effective);
  const valid=effective>=0&&effective<row.count;
  assert.equal(row.accepted,valid);assert.equal(row.output_untouched,true);
  assert.equal(row.matrix_index,valid?effective:null);
  if(effective<0)assert.equal(row.slot_name_unchanged,true);
  else assert.equal(row.slot_name_unchanged,null);
  if(valid){
    accepted++;
    for(const trial of wheels.rows)for(const event of trial.events){
      if(effective>=event.after.length)continue;
      assert.equal(event.indexed_slot_suffixes[effective],event.after[effective]);
      const remap=event.item_to_data_index;
      assert.equal(remap.length?remap[effective]:effective,event.after[effective]);
      joins++;
    }
  }
}
console.log(JSON.stringify({passed:true,cases:receipt.rows.length,accepted,prior_wheel_state_joins:joins,
  scope:'Native overlap item getter and instance admission/negative slot-name guard; cross-receipt physical-item joins to prior wheel remap, no full pipeline or captured state claim'}));
