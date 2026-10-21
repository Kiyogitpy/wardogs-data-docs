/* Offline triangle visitor and cooked BVH model, CL-516586, local UE centimetres.
 * No scene membership, instance transform or world-query filtering is supplied.
 */
'use strict';
const EPS = Math.fround(1e-8);
const preparedVertices = new WeakSet();
const sub = (a, b) => a.map((x, i) => x - b[i]);
const dot = (a, b) => a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
const cross = (a, b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];

function rayState(vertices, start, direction, length, cull) {
  if (!preparedVertices.has(vertices)) vertices = vertices.map(p => p.map(Math.fround));
  let limit = Math.fround(length), selected = null;
  function visit(face, index) {
    const [a, b, c] = face.map(i => vertices[i]);
    const ab = sub(b, a), ac = sub(c, a), normal = cross(ab, ac);
    const nd = dot(normal, direction);
    if (cull && nd > 0) return;
    const determinant = -nd;
    if (Math.abs(determinant) < EPS) return;
    const inverse = 1 / determinant, delta = sub(start, a);
    const time = dot(delta, normal) * inverse;
    if (time < 0 || time > limit) return;
    const negativeDirection = direction.map(x => -x);
    const baryCross = cross(negativeDirection, delta);
    const u = dot(baryCross, ac) * inverse;
    if (u < -EPS || u > 1 + EPS) return;
    const negativeV = dot(baryCross, ab) * inverse;
    if (negativeV > EPS || u - negativeV > 1 + EPS) return;
    const squared = dot(normal, normal);
    const multiplier = squared >= EPS ? Math.sign(determinant) / Math.sqrt(squared) : 0;
    selected = {hit: true, face: index, time,
      position: start.map((x, i) => x + direction[i]*time), normal: normal.map(x => x*multiplier)};
    // A later face compares against the rounded traversal distance, not OutTime.
    limit = Math.fround(time);
  }
  return {visit, limit: () => limit,
    finish: () => selected && selected.time <= length ? selected : {hit: false, time: null, face: null}};
}

// Prepare immutable cooked geometry once; each query otherwise quantizes inputs.
function prepareMesh(mesh) {
  const vertices = mesh.vertices.map(p => Object.freeze(p.map(Math.fround)));
  Object.freeze(vertices);
  preparedVertices.add(vertices);
  return {...mesh, vertices};
}

function raycast(vertices, faces, start, direction, length, cull) {
  const state = rayState(vertices, start, direction, length, cull);
  faces.forEach(state.visit);
  return state.finish();
}

function raycastMesh(mesh, start, direction, length, cull) {
  const state = rayState(mesh.vertices, start, direction, length, cull);
  const f = Math.fround, origin = start.map(f), dir = direction.map(f);
  const parallel = dir.map(x => Math.abs(x) < EPS);
  const inverse = dir.map((x, i) => parallel[i] ? 0 : f(1 / x));
  function boundsHit(min, max) {
    let entry = 0, exit = state.limit();
    for (let i = 0; i < 3; i++) {
      if (parallel[i]) {
        if (origin[i] < min[i] || origin[i] > max[i]) return false;
      } else {
        const a = f(f(min[i]-origin[i])*inverse[i]);
        const b = f(f(max[i]-origin[i])*inverse[i]);
        entry = Math.max(entry, Math.min(a, b));
        exit = Math.min(exit, Math.max(a, b));
      }
    }
    return exit >= entry;
  }
  const stack = mesh.bvh.nodes.length ? [0] : [], faceOrder = [];
  while (stack.length) {
    const node = mesh.bvh.nodes[stack.pop()];
    // Internal children push in stored order; LIFO visits child 1 first.
    for (const child of node) {
      if (child.childOrFaceIndex === -1 || !boundsHit(child.bounds.min, child.bounds.max)) continue;
      if (!child.faceCount) stack.push(child.childOrFaceIndex);
      else for (let i = child.childOrFaceIndex; i < child.childOrFaceIndex+child.faceCount; i++) {
        const box = mesh.bvh.faceBounds[i];
        if (!boundsHit(box.slice(0, 3), box.slice(3))) continue;
        faceOrder.push(i);
        state.visit(mesh.triangles[i], i);
      }
    }
  }
  return {...state.finish(), faceOrder};
}

function raycastScaledMesh(mesh, suppliedScale, start, direction, length, cull) {
  const f = Math.fround, minimumScale = f(1e-6);
  const scale = suppliedScale.map(x => Math.abs(f(x)) < minimumScale ? minimumScale : f(x));
  const inverse = scale.map(x => f(1 / x));
  const localStart = start.map((x, i) => f(f(x)*inverse[i]));
  const denormal = direction.map((x, i) => f(f(x)*inverse[i]));
  const factor = Math.sqrt(denormal[1]*denormal[1]+denormal[0]*denormal[0]+denormal[2]*denormal[2]);
  const noHit = {hit: false, face: null, time: null};
  const metadata = {effectiveScale: scale, inverseScale: inverse};
  if (!(factor > 2.2250738585072014e-308)) return {...noHit, ...metadata, faceOrder: []};
  const factorInverse = 1 / factor;
  const localDirection = denormal.map(x => x*factorInverse);
  const local = raycastMesh(mesh, localStart, localDirection, length*factor, cull);
  if (!local.hit) return {...noHit, ...metadata, faceOrder: local.faceOrder};
  const time = local.time*factorInverse;
  if (time === 0) return {...local, ...metadata, time, position: start.slice(), normal: direction.map(x => -x)};
  // The scaled wrapper rejects its far endpoint after the local inclusive test.
  if (time >= length) return {...noHit, ...metadata, faceOrder: local.faceOrder};
  const position = local.position.map((x, i) => f(f(x)*scale[i]));
  let normal = local.normal.map((x, i) => f(f(x)*inverse[i]));
  const squared = f(f(f(normal[1]*normal[1])+f(normal[0]*normal[0]))+f(normal[2]*normal[2]));
  if (squared < 1.1754943508222875e-38) normal = [0, 0, 0];
  else if (squared !== 1) {
    const multiplier = f(1 / f(Math.sqrt(squared)));
    normal = normal.map(x => f(x*multiplier));
  }
  return {...local, ...metadata, time, position, normal};
}

function rotateQuaternion(q, v) {
  const twiceCross = cross(q, v).map(x => x*2);
  const correction = cross(q, twiceCross);
  return v.map((x, i) => (x+q[3]*twiceCross[i])+correction[i]);
}

function raycastTransformedMesh(mesh, rotation, translation, meshScale, start, direction, length, cull) {
  const inverse = [-rotation[0], -rotation[1], -rotation[2], rotation[3]];
  const localStart = rotateQuaternion(inverse, sub(start, translation));
  const localDirection = rotateQuaternion(inverse, direction);
  const local = meshScale === null ? raycastMesh(mesh, localStart, localDirection, length, cull) :
    raycastScaledMesh(mesh, meshScale, localStart, localDirection, length, cull);
  if (!local.hit) return local;
  // This wrapper leaves the caller's position/normal storage untouched at TOI 0.
  if (local.time === 0) return {...local, position: null, normal: null, outputsWritten: false};
  const position = rotateQuaternion(rotation, local.position).map((x, i) => x+translation[i]);
  return {...local, position, normal: rotateQuaternion(rotation, local.normal), outputsWritten: true};
}

function raycastActorMesh(mesh, rotation, translation, shapeRotation, shapeTranslation, meshScale,
  start, direction, length, cull) {
  const q = rotation.map(Math.fround), inverse = [-q[0], -q[1], -q[2], q[3]];
  const localStart = rotateQuaternion(inverse, sub(start, translation));
  const localDirection = rotateQuaternion(inverse, direction);
  const local = shapeRotation !== null ? raycastTransformedMesh(mesh, shapeRotation, shapeTranslation,
    meshScale, localStart, localDirection, length, cull) : meshScale !== null ?
    raycastScaledMesh(mesh, meshScale, localStart, localDirection, length, cull) :
    raycastMesh(mesh, localStart, localDirection, length, cull);
  if (!local.hit) return {...local, continued: true, fastLength: length};
  const fastLength = Math.max(local.time, 0), validOutputs = local.outputsWritten !== false;
  return {...local, distance: Math.fround(local.time), flags: 7,
    fastLength, continued: fastLength !== 0, geometryOutputsWritten: validOutputs,
    position: validOutputs ? rotateQuaternion(q, local.position).map((x, i) => x+translation[i]) : null,
    normal: validOutputs ? rotateQuaternion(q, local.normal) : null};
}

function worldRayInput(start, end) {
  const delta = sub(end, start);
  const length = Math.fround(Math.sqrt(delta[0]*delta[0]+delta[1]*delta[1]+delta[2]*delta[2]));
  const admitted = length > EPS;
  return {length, admitted, direction: admitted ? delta.map(x => x*(1 / length)) : null};
}

function safeNormal(v) {
  const squared = dot(v, v);
  if (squared === 1) return v.slice();
  if (squared < EPS) return [0, 0, 0];
  const inverse = 1 / Math.sqrt(squared);
  return v.map(x => x*inverse);
}

function convertRayHitMath(start, end, length, distance, flags, position, suppliedNormal) {
  distance = Math.fround(distance);
  const penetrating = distance <= 0, delta = sub(end, start);
  const usesPosition = !!(flags & 1) && !penetrating;
  const usesNormal = !!(flags & 2) && !penetrating;
  if ((usesPosition && !position.every(Number.isFinite)) || (usesNormal && !suppliedNormal.every(Number.isFinite))) {
    return {accepted: false};
  }
  const time = Math.fround(distance / Math.fround(length));
  let normal = safeNormal(usesNormal ? suppliedNormal : delta.map(x => -x));
  if (usesNormal && Math.abs(1-dot(normal, normal)) >= Math.fround(.01)) normal = safeNormal(delta.map(x => -x));
  return {accepted: true, time, distance, flags: penetrating ? 3 : 1,
    location: start.map((x, i) => x+delta[i]*time), impactPoint: usesPosition ? position.slice() : start.slice(),
    normal, impactNormal: normal.slice()};
}

function tracePrefilter(query, shape, component, actors, components) {
  if (!(query[3] & shape[3] & 3) || ((query[3] >>> 26) & (shape[3] >>> 26))) return 0;
  const qChannel = (query[3] >>> 21) & 31, sChannel = (shape[3] >>> 21) & 31;
  let result;
  if (query[0] === 0) result = query[1] & (1 << sChannel) ? (qChannel === 0 ? 2 : 1) : 0;
  else {
    const sResponse = shape[1] & (1 << qChannel) ? 2 : shape[2] & (1 << qChannel) ? 1 : 0;
    const qResponse = query[1] & (1 << sChannel) ? 2 : query[2] & (1 << sChannel) ? 1 : 0;
    result = Math.min(sResponse, qResponse);
  }
  // This entry models the LOS callback's ignore-touch configuration.
  if (result === 1 || (result && (actors.includes(shape[0]) || components.includes(component)))) return 0;
  return result;
}

function actorBoundsHit(start, direction, bounds, length) {
  let entry = 0, exit = Number.MAX_VALUE;
  for (let i = 0; i < 3; i++) {
    const lo = bounds.min[i]-start[i], hi = bounds.max[i]-start[i];
    if (Math.abs(direction[i]) < EPS) {
      if (lo > 0 || hi < 0) return false;
    } else {
      const inverse = 1 / direction[i], a = lo*inverse, b = hi*inverse;
      entry = Math.max(entry, Math.min(a, b));
      exit = Math.min(exit, Math.max(a, b));
      if (entry > exit) return false;
    }
  }
  return entry <= length && exit >= 0;
}

function raycastActorShapes(mesh, rotation, translation, shapes, order, query, actors, components,
  start, direction, length, cull) {
  let best = {hit: false}, limit = length, continued = true;
  const filterCalls = [], shapeVisits = [];
  for (const id of order) {
    const shape = shapes.find(s => s.id === id);
    if (shapes.length > 1 && !actorBoundsHit(start, direction, shape.bounds, limit)) continue;
    if (components.length && shape.component_id === undefined) throw new Error('Missing supplied component identity');
    const filter = shape.query_enabled ? tracePrefilter(query, shape.filter, shape.component_id, actors, components) : 0;
    filterCalls.push({shape: id, result: filter});
    if (!filter) continue;
    const hit = raycastActorMesh(shape.mesh || mesh, rotation, translation, shape.rotation, shape.translation,
      shape.scale || null, start, direction, limit, cull);
    hit.faceOrder.forEach(face => shapeVisits.push([id, face]));
    if (!hit.hit) continue;
    best = {...hit, shape: id};
    limit = hit.fastLength;
    if (!hit.continued) { continued = false; break; }
  }
  return {...best, fastLength: limit, continued, filterCalls, shapeVisits};
}

module.exports = {raycast, raycastMesh, raycastScaledMesh, raycastTransformedMesh, raycastActorMesh,
  worldRayInput, convertRayHitMath, raycastActorShapes, prepareMesh};
