'use strict';

// Frozen 0x16670B0 nonnegative-scale branch. UE layout: q4, translation4, scale4.
function multiplyPositive(a, b) {
  for (const input of [a, b]) {
    if (!Array.isArray(input) || input.length !== 12 || !input.every(Number.isFinite)) {
      throw new Error('Expected twelve finite transform scalars');
    }
    if (input[7] !== 0 || input[11] !== 0 || input.slice(8, 11).some(v => v < 0)) {
      throw new Error('Only zero padding and nonnegative scales are covered');
    }
  }
  const [ax, ay, az, aw] = a, [bx, by, bz, bw] = b;
  const q = [
    (((aw * bx) * 1 + bw * ax) + (by * az) * 1) + (ay * bz) * -1,
    (((az * bx) * -1 + bw * ay) + (by * aw) * 1) + (ax * bz) * 1,
    (((ay * bx) * 1 + bw * az) + (by * ax) * -1) + (aw * bz) * 1,
    (((ax * bx) * -1 + bw * aw) + (by * ay) * -1) + (az * bz) * -1
  ];
  const v = a.slice(4, 7).map((x, i) => x * b[8 + i]);
  const cross = v => [by * v[2] - bz * v[1], bz * v[0] - bx * v[2], bx * v[1] - by * v[0]];
  const c = cross(v), twice = c.map(x => x + x), again = cross(twice);
  const t = v.map((x, i) => ((bw * twice[i] + x) + again[i]) + b[4 + i]);
  return [...q, ...t, 0, ...a.slice(8, 11).map((x, i) => x * b[8 + i]), 0];
}

// Matching cache entry only. Other spaces and cache misses have separate callers.
function cachedSocketTransform(local, bone, componentWorld, space, enabled) {
  if (space === 3) return local.slice();
  if (space !== 0) throw new Error('Only world and parent-bone-local socket spaces are covered');
  if (bone === null) return componentWorld.slice();
  const identity = [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0];
  return multiplyPositive(local, enabled ? multiplyPositive(bone, componentWorld) : identity);
}

// Input FName identities and local transforms are supplied by the frozen-asset receipts.
function buildSocketCache(inputs) {
  const cache = new Map(), mesh = inputs.filter(x => x.source === 'mesh');
  const skeleton = inputs.filter(x => x.source === 'skeleton');
  mesh.forEach((input, slot) => cache.set(input.name_id, { ...input, slot }));
  skeleton.forEach((input, index) => {
    if (!cache.has(input.name_id)) cache.set(input.name_id, { ...input, slot: mesh.length + index });
  });
  return cache;
}

// Full parent-ordered hierarchy, matching scalar and dispatch-level-2 construction receipts.
function buildComponentPose(bones) {
  const components = [];
  bones.forEach((bone, index) => {
    if (index === 0) {
      if (bone.parent_index !== -1) throw new Error('Expected a root bone first');
      components.push(bone.local.slice());
      return;
    }
    if (bone.parent_index < 0 || bone.parent_index >= index) throw new Error('Expected parent-ordered bones');
    const result = multiplyPositive(bone.local, components[bone.parent_index]);
    const [x, y, z, w] = result;
    const squared = (y * y + w * w) + (x * x + z * z);
    const reciprocal = 1 / Math.sqrt(squared);
    const q = squared >= 1e-8 ? result.slice(0, 4).map(v => reciprocal * v) : [0, 0, 0, 1];
    components.push([...q, ...result.slice(4)]);
  });
  return components;
}

module.exports = { multiplyPositive, cachedSocketTransform, buildSocketCache, buildComponentPose };
