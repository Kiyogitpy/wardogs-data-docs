'use strict';
const fs = require('fs');
const assert = require('assert');
const { buildComponentPose } = require('./vehicle_native_transform');
const native = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const source = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const poses = new Map(source.meshes.map(mesh => [mesh.package, buildComponentPose(mesh.bones.map(b => ({
  parent_index: b.parent_index,
  local: [...b.rotation_xyzw.values, ...b.translation_cm.values, 0, ...b.scale.values, 0]
})))]));
let records = 0;
for (const row of native.rows) {
  const expected = poses.get(row.package);
  assert.strictEqual(expected.length, row.bones.length);
  row.bones.forEach((bone, i) => {
    const bytes = Buffer.alloc(96);
    expected[i].forEach((v, j) => bytes.writeDoubleLE(v, j * 8));
    assert.strictEqual(bytes.toString('hex'), bone.component_bytes_hex, `${row.package}: ${bone.name}, ${row.mode}`);
    records++;
  });
}
console.log(JSON.stringify({ passed: true, cases: native.cases, bone_records: records, exact_scalar_bits: records * 12 }));
