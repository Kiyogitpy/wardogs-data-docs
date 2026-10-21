'use strict';
const fs = require('fs');
const assert = require('assert');
const { multiplyPositive } = require('./vehicle_native_transform');
const receipt = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
let calls = 0, bones = 0;
for (const mesh of receipt.meshes) {
  const components = [];
  for (const bone of mesh.bones) {
    const result = bone.parent_index < 0 ? bone.local : multiplyPositive(bone.local, components[bone.parent_index]);
    const bytes = Buffer.alloc(96);
    result.forEach((v, i) => bytes.writeDoubleLE(v, i * 8));
    assert.strictEqual(bytes.toString('hex'), bone.component_bytes_hex, `${mesh.package}: ${bone.name}`);
    components.push(result);
    calls += Number(bone.native_call);
    bones++;
  }
}
assert.strictEqual(calls, receipt.native_calls);
assert.strictEqual(bones, receipt.bones);
assert.throws(() => multiplyPositive([0, 0, 0, 1, 0, 0, 0, 0, -1, 1, 1, 0], Array(12).fill(0)));
let worldCases = 0, validWorldCases = 0;
if (process.argv[3]) {
  const world = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
  const byPackage = new Map(receipt.meshes.map(m => [m.package, m.bones]));
  const identity = [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0];
  for (const row of world.rows) {
    const selected = byPackage.get(row.package);
    assert(selected);
    const valid = row.enabled && row.index >= 0 && row.index < selected.length;
    assert.strictEqual(valid, row.valid);
    assert.strictEqual(row.multiply_calls, Number(valid));
    assert.strictEqual(row.weak_calls, Number(row.enabled));
    const result = valid ? multiplyPositive(selected[row.index].component, world.worlds[row.world]) : identity;
    const bytes = Buffer.alloc(96);
    result.forEach((v, i) => bytes.writeDoubleLE(v, i * 8));
    assert.strictEqual(bytes.toString('hex'), row.output_bytes_hex, `${row.package}: ${row.index}, buffer ${row.selector}`);
    worldCases++;
    validWorldCases += Number(valid);
  }
  assert.strictEqual(worldCases, world.cases);
  assert.strictEqual(validWorldCases, world.valid_cases);
}
let socketCases = 0;
if (process.argv[4]) {
  const sockets = JSON.parse(fs.readFileSync(process.argv[4], 'utf8'));
  const byPackage = new Map(receipt.meshes.map(m => [m.package, new Map(m.bones.map(b => [b.name, b.component]))]));
  for (const mesh of sockets.meshes) {
    const boneMap = byPackage.get(mesh.package);
    assert(boneMap);
    for (const socket of mesh.sockets) {
      assert.strictEqual(boneMap.has(socket.bone), socket.bone_found);
      const parent = boneMap.get(socket.bone) || [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0];
      const result = multiplyPositive(socket.local, parent);
      const bytes = Buffer.alloc(96);
      result.forEach((v, i) => bytes.writeDoubleLE(v, i * 8));
      assert.strictEqual(bytes.toString('hex'), socket.component_bytes_hex, `${mesh.package}: ${socket.name}`);
      socketCases++;
    }
  }
  assert.strictEqual(socketCases, sockets.composition_calls);
}
console.log(JSON.stringify({ passed: true, bones, native_calls: calls, exact_scalar_bits: (bones + worldCases + socketCases) * 12,
  world_cases: worldCases, valid_world_cases: validWorldCases, socket_cases: socketCases }));
