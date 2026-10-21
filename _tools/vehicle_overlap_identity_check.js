#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict');
const receipt=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
for(const [index,row]of receipt.rows.entries()){
  let expected;
  if(row.pattern){
    const selected=row.pattern==='first'?3:['second','hole'].includes(row.pattern)?4:row.welded?2:1;
    const weak=[selected,100+selected];
    expected={handle_component:weak,handle_item:10*selected,handle_kind:2,component:weak,item:10*selected,
      owner_component:row.mode==='direct'?weak:row.mode==='wrapper-owner'?[5,105]:[0,0],
      physics_owner:'0x'+(0x8000000+16*selected).toString(16)};
    assert.equal(row.selected_component,selected);
    assert.equal(row.callback_calls,['wrapper-null','wrapper-owner'].includes(row.mode)?1:0);
  }else if(row.pair){
    const found=row.metadata_type===2&&row.key_mode===(row.storage<2?'null':'actor');
    let item=-1;
    if(found){
      if(row.pair[1]===-1){if(row.pair[0]>=0)item=row.pair[0];}
      else if(row.pair[1]>=0)item=(row.pair[1]+0x80000000)|0;
    }
    expected={handle_component:[1,101],handle_item:-1,handle_kind:2,component:[1,101],item,
      owner_component:[0,0],physics_owner:'0x0'};
  }else{
    const component=row.selected_component,valid=row.weak_state==='valid';
    const weak=valid?[component,100+component]:[0,0];
    expected={handle_component:weak,handle_item:valid?row.item:0,handle_kind:valid?2:0,
      component:weak,item:valid?row.item:0,
      owner_component:row.physics===2&&row.userdata!==8?weak:[0,0],
      physics_owner:row.physics===2?'0x'+(0x8000000+16*component).toString(16):'0x0'};
  }
  assert.deepEqual(row.output,expected,`identity ${index}`);
}
console.log(JSON.stringify({passed:true,cases:receipt.rows.length,
  scope:'Native overlap body/direct-component identity fields and ISM item encoding on owned object/physics records; no captured identity provenance'}));
