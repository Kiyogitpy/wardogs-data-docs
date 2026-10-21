/* Compare the complete conditional backend with composed raw-native results. */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const G=require('../assets/js/vehicle-impact-geometry.js');
const decoder=require('../assets/js/vendor/meshopt_decoder-1.2.0.js');
const backend=require('./vehicle_cooked_backend.js');
assert.ok(process.argv[2],'Usage: node _tools/vehicle_reference_scene_ray_check.js <reference-scene-native-oracle-v1.json>');
const oraclePath=process.argv[2],root=path.dirname(oraclePath),bytes=fs.readFileSync(oraclePath),oracle=JSON.parse(bytes);
const manifestPath=process.argv[3]||path.join(root,'conditional-native-scenes-v1/manifest.json');
const fixturePath=process.argv[4]||path.join(root,'scene-ray-fixtures-v1.json');
const fixtures=JSON.parse(fs.readFileSync(fixturePath));
const manifest=JSON.parse(fs.readFileSync(manifestPath));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(oracle.passed,true);
assert.equal(oracle.binary_sha256,'a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37');
for(const[p,digest]of Object.entries(oracle.source_hashes))assert.equal(sha(fs.readFileSync(p)),digest,p);
const boundSources=new Map(Object.entries(oracle.source_hashes).map(([p,digest])=>[path.resolve(p),digest]));
for(const p of[manifestPath,fixturePath])assert.equal(sha(fs.readFileSync(p)),boundSources.get(path.resolve(p)),p+' is not bound by oracle');
const near=(a,b)=>assert.ok(Math.abs(a-b)<=1e-8*Math.max(1,Math.abs(b)),`${a} != ${b}`);
async function main(){const cache=new Map();let cases=0,hits=0;
  for(const row of oracle.rows){
    const input=fixtures.rows[row.fixture_index];
    if(!cache.has(input.scene)){
      const scene=manifest.scenes.find(s=>s.id===input.scene),buffer=fs.readFileSync(scene.scene_path);
      assert.equal(sha(buffer),scene.scene_sha256);
      const geometry=await G.load(buffer.buffer.slice(buffer.byteOffset,buffer.byteOffset+buffer.byteLength),decoder);
      backend.attach(geometry,scene);cache.set(input.scene,geometry);
    }
    const geometry=cache.get(input.scene);
    const actual=input.ignore.length?geometry.segmentLOS(input.start,input.end,input.ignore).hit:geometry.traceSegment(input.start,input.end);
    assert.equal(!!actual,row.result.hit,`Hit case ${row.fixture_index} ${input.scene} ${input.kind}`);
    if(actual){
      const expected=row.result;
      assert.equal(actual.component.nodeIndex,expected.node_index);
      assert.equal(actual.nativeFace.face,expected.face);
      assert.equal(actual.material.name,expected.material);
      assert.equal(actual.distance,expected.distance);
      assert.equal(actual.nativeFlags,expected.native_flags);
      for(const field of['position','location','normal'])actual[field].forEach((v,i)=>near(v,expected[field][i]));
      hits++;
    }
    cases++;
  }
  assert.equal(cases,fixtures.cases);assert.equal(cases,oracle.cases);assert.equal(hits,oracle.hit_cases);
  assert.equal(cache.size,new Set(fixtures.rows.map(row=>row.scene)).size);
  console.log(JSON.stringify({passed:true,cases,hits,scenes:cache.size,native_candidate_calls:oracle.native_candidate_calls,
    oracle_sha256:sha(bytes),scope:'Complete conditional backend vs composed native routines; supplied candidate set/order/poses/Block eligibility; no acceleration/overlap/runtime state'}));
}
main().catch(error=>{console.error(error);process.exitCode=1;});
