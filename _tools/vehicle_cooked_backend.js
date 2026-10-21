/* Conditional native-query backend for private offline reference scenes.
 * Rendering retains supplied GLB geometry; queries use original cooked data.
 * Poses and component encounter order are supplied, not captured scene state.
 */
'use strict';
const native = require('./vehicle_native_ray.js');
const overlap = require('./vehicle_native_overlap.js');
const cache = new Map();
const uePoint = p => [p[2]*100, -p[0]*100, p[1]*100];
const gltfPoint = p => [-p[1]/100, p[2]/100, p[0]/100];
const gltfVector = p => [-p[1], p[2], p[0]];
function load(resource) {
  const fs = require('node:fs');
  const crypto = require('node:crypto');
  if (!cache.has(resource.decoded_file)) {
    const bytes = fs.readFileSync(resource.decoded_file);
    const sha = crypto.createHash('sha256').update(bytes).digest('hex');
    if (sha !== resource.sha256) throw new Error('Cooked resource hash mismatch: '+resource.decoded_file);
    cache.set(resource.decoded_file, {sha, meshes: JSON.parse(bytes).complexImplicits.map(native.prepareMesh)});
  }
  const decoded = cache.get(resource.decoded_file);
  if (decoded.sha !== resource.sha256) throw new Error('Conflicting cooked resource identity');
  const mesh = decoded.meshes[resource.implicit_index];
  if (!mesh || mesh.triangles.length !== resource.surface_slots.length) throw new Error('Cooked material/face count mismatch');
  return mesh;
}
function attach(geometry, scene, loadResource = load) {
  const bindings = scene.native_components.map(row => {
    const component = geometry.components.find(c => c.nodeIndex === row.node_index);
    if (!component) throw new Error('Missing reference component '+row.node_index);
    if (row.query.resources.length !== 1) throw new Error('Expected the current one-complex-implicit own-body layout');
    const resource = row.query.resources[0], mesh = loadResource(resource);
    const materials = new Map(component.triangles.map(t => [t.material.name, t.material]));
    for (const slot of resource.surface_slots) if (!materials.has(slot)) throw new Error('Missing cooked slot '+slot);
    const primitives = new Map(component.triangles.map(t => [t.material.name, t.primitiveIndex]));
    return {component, pose: row.query, resource, mesh, materials, primitives};
  });
  if (bindings.length !== geometry.components.length) throw new Error('Reference component coverage mismatch');
  function ray(origin, direction, maxDistance, ignore) {
    if (![origin,direction].every(v => v && v.length === 3 && v.every(Number.isFinite))) throw new Error('Invalid reference ray');
    const magnitude = Math.hypot(...direction);
    if (!(magnitude > 0)) throw new Error('Zero reference ray direction');
    if (maxDistance === undefined || maxDistance === Infinity) {
      maxDistance = Math.hypot(...origin.map((v,i) => v-geometry.bounds.center[i]))+geometry.bounds.radius*2+1;
    }
    if (!Number.isFinite(maxDistance) || maxDistance < 0) throw new Error('Invalid reference ray length');
    const end = origin.map((x,i) => x+direction[i]/magnitude*maxDistance);
    return segment(origin,end,ignore);
  }
  function segment(origin,end,ignore) {
    if (![origin,end].every(v => v && v.length === 3 && v.every(Number.isFinite))) throw new Error('Invalid reference segment');
    const startUE = uePoint(origin), endUE = uePoint(end), query = native.worldRayInput(startUE,endUE);
    if (!query.admitted) return null;
    let selected = null, limit = query.length;
    for (const binding of bindings) {
      const c = binding.component;
      if (ignore && ignore.some(x => x === c || x === c.id || x === c.nodeIndex)) continue;
      const p = binding.pose;
      const hit = native.raycastActorMesh(binding.mesh,p.rotation,p.translation,null,null,p.scale,
        startUE,query.direction,limit,p.cull_backface);
      if (!hit.hit) continue;
      selected = {binding,hit};
      limit = hit.fastLength;
      if (!hit.continued) break;
    }
    if (!selected) return null;
    const {binding,hit} = selected;
    const converted = native.convertRayHitMath(startUE,endUE,query.length,hit.distance,hit.flags,hit.position,hit.normal);
    if (!converted.accepted) return null;
    const slot = binding.resource.surface_slots[hit.face], material = binding.materials.get(slot);
    const primitive = binding.primitives.get(slot);
    return {position: gltfPoint(converted.impactPoint), location: gltfPoint(converted.location),
      normal: gltfVector(converted.impactNormal), distance: converted.distance/100,
      component: binding.component, material, primitiveIndex: primitive,
      nativeFace: {decodedFile: binding.resource.decoded_file, implicitIndex: binding.resource.implicit_index, face: hit.face},
      nativeFlags: converted.flags};
  }
  geometry.ray = function(origin,direction,maxDistance,predicate) {
    if (predicate) throw new Error('Conditional cooked backend uses component exclusions through segmentLOS, not per-triangle predicates');
    return ray(origin,direction,maxDistance);
  };
  geometry.traceSegment = function(start,end) { return segment(start,end); };
  geometry.overlapSphere = function(origin,radius) {
    if (!Array.isArray(origin) || origin.length !== 3 || !origin.every(Number.isFinite) ||
        !Number.isFinite(radius) || radius < 0) throw new Error('Invalid reference overlap sphere');
    const center = uePoint(origin), radiusUE = Math.fround(radius*100);
    if (!center.every(Number.isFinite) || !Number.isFinite(radiusUE)) throw new Error('Reference overlap sphere exceeds finite UE input');
    return bindings.filter(binding => {
      const p = binding.pose;
      return overlap.actorSphere(binding.mesh,p.rotation,p.translation,null,null,p.scale,center,radiusUE).overlap;
    }).map(binding => binding.component);
  };
  geometry.segmentLOS = function(start,end,ignoreComponents) {
    const delta = end.map((x,i) => x-start[i]), distance = Math.hypot(...delta);
    let ignore = ignoreComponents || [];
    if (ignore instanceof Set) ignore = [...ignore];
    else if (!Array.isArray(ignore)) ignore = [ignore];
    const hit = distance ? segment(start,end,ignore) : null;
    return {clear: !hit, hit, distance};
  };
  geometry.nativeReferenceScope = 'Cooked ray/sphere overlap geometry/BVH with computed query inputs; supplied source poses, candidate eligibility and encounter order, no captured world state';
  return geometry;
}
module.exports = {attach};
