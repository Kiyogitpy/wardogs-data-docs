'use strict';
const fs = require('fs');
const assert = require('assert');
const { cachedSocketTransform, buildSocketCache } = require('./vehicle_native_transform');
const read = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const receipt = read(process.argv[2]), sockets = read(process.argv[3]), poses = read(process.argv[4]);
const byPackage = new Map(sockets.meshes.map(m => [m.package, m.sockets]));
const bones = new Map(poses.meshes.map(m => [m.package, m.bones]));
let cases = 0, missing = 0;
for (const row of receipt.rows) {
  const socket = byPackage.get(row.package)[row.socket], pose = bones.get(row.package);
  assert.strictEqual(socket.name, row.name);
  const index = pose.findIndex(b => b.name === socket.bone);
  assert.strictEqual(index, row.bone_index);
  const result = cachedSocketTransform(socket.local, index < 0 ? null : pose[index].component,
    receipt.worlds[row.world], row.space, row.enabled);
  const bytes = Buffer.alloc(96);
  result.forEach((v, i) => bytes.writeDoubleLE(v, i * 8));
  assert.strictEqual(bytes.toString('hex'), row.output_bytes_hex, `${row.package}: ${row.name}, space ${row.space}`);
  assert.strictEqual(row.cache_calls, 1);
  assert.strictEqual(row.hash_calls, 1);
  const boneCall = Number(index >= 0 && row.space !== 3 && row.enabled);
  assert.strictEqual(row.bone_calls, boneCall);
  assert.strictEqual(row.weak_calls, boneCall);
  assert.strictEqual(row.multiply_calls, index >= 0 && row.space !== 3 ? 1 + Number(row.enabled) : 0);
  missing += Number(index < 0);
  cases++;
}
assert.strictEqual(cases, receipt.cases);
assert.strictEqual(missing, receipt.missing_bone_cases);
let builds = 0, entries = 0, predicates = 0;
if (process.argv[5]) {
  const construction = read(process.argv[5]);
  for (const mesh of construction.meshes) {
    const expected = buildSocketCache(mesh.inputs);
    assert.strictEqual(expected.size, mesh.entries.length);
    for (const entry of mesh.entries) {
      const item = expected.get(entry.name_id);
      for (const key of ['name', 'source', 'slot', 'bone_index', 'local_bytes_hex']) {
        assert.strictEqual(entry[key], item[key], `${mesh.package}: ${entry.name}, ${key}`);
      }
      if (entry.does_socket_exist !== undefined) {
        assert.strictEqual(entry.does_socket_exist, true);
        predicates++;
      }
      entries++;
    }
    assert.strictEqual(mesh.sparse_count - mesh.free_count, expected.size);
    builds++;
  }
  assert.strictEqual(builds, construction.cases);
  assert.strictEqual(entries, construction.cached_entries);
}
console.log(JSON.stringify({ passed: true, cases, missing_bone_cases: missing, exact_scalar_bits: cases * 12,
  cache_builds: builds, cache_entries: entries, socket_predicates: predicates }));
