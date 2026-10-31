'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const E=require('../assets/js/loadout-eval.js');

test('player-facing class is Assault while unlock and legacy permalink key remains Infantry',()=>{
 assert.equal(typeof E.roleLabel,'function');
 assert.equal(E.roleLabel('Infantry'),'Assault');
 for(const role of ['Medic','Recon','Support','Wardog','']) assert.equal(E.roleLabel(role),role);
 assert.equal(E.roleKey('Assault'),'Infantry');
 assert.equal(E.roleKey('Infantry'),'Infantry');
 assert.equal(E.roleKey('Support'),'Support');
});

test('Spear groups with assault rifles without rewriting its internal DMR archetype or recoil',()=>{
 assert.equal(typeof E.weaponGroup,'function');
 const model=E.model(require('../assets/data/weapon-loadouts.json'));
 const id='ID_WEPN_037',lo=E.defaultLoadout(model,id);
 const before=JSON.stringify(E.evaluate(model,lo));
 assert.equal(model.items[id].archetype,'DMR');
 assert.equal(E.weaponGroup(id,model.items[id].archetype),'AR');
 assert.equal(E.weaponGroup('ID_SKS','DMR'),'DMR');
 assert.equal(E.weaponGroup('ID_M4','AR'),'AR');
 assert.equal(E.weaponGroup('unknown',null),'Other');
 assert.equal(model.items[id].archetype,'DMR');
 assert.equal(JSON.stringify(E.evaluate(model,lo)),before);
});
