#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const G=require('../assets/js/vehicle-impact-geometry');
const decoder=require('../assets/js/vendor/meshopt_decoder-1.2.0');
const {attach}=require('./vehicle_cooked_backend');
const receipt=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const manifest=JSON.parse(fs.readFileSync(process.argv[3]||path.join(path.dirname(process.argv[2]),'conditional-native-scenes-v1/manifest.json'),'utf8'));
async function main(){
  let cases=0,membershipChanges=0,added=0,removed=0;
  for(const scene of manifest.scenes){
    const b=fs.readFileSync(scene.scene_path);
    const geometry=attach(await G.load(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),decoder),scene);
    for(const row of receipt.rows.filter(r=>r.scene===scene.id)){
      assert.deepEqual(geometry.overlapSphere(row.center,row.radius).map(c=>c.nodeIndex),row.nodes,`membership ${cases}`);
      const legacy=geometry.components.filter(c=>{
        const closest=geometry.closestPoint(row.center,c);
        return closest&&closest.distance<=row.radius+1e-7;
      }).map(c=>c.nodeIndex);
      const nativeOnly=row.nodes.filter(id=>!legacy.includes(id)),legacyOnly=legacy.filter(id=>!row.nodes.includes(id));
      if(nativeOnly.length||legacyOnly.length)membershipChanges++;
      added+=nativeOnly.length;removed+=legacyOnly.length;
      cases++;
    }
    for(const [origin,radius]of [[[0,0,0],-1],[[0,0,0],Infinity],[[NaN,0,0],1]]){
      assert.throws(()=>geometry.overlapSphere(origin,radius),/Invalid reference overlap sphere/);
    }
  }
  console.log(JSON.stringify({passed:true,cases,scenes:manifest.scenes.length,
    membership_changes_vs_closest_point:membershipChanges,native_only_memberships:added,closest_point_only_memberships:removed,
    scope:'Attached private cooked backend sphere membership/order over native oracle; supplied source poses and candidate membership/eligibility'}));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
