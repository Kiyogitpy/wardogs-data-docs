/* Offline GLB triangle queries. Coordinates retain the assembly's metre/+Y-up frame. */
(function (root, factory) {
  'use strict';
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.VehicleImpactGeometry = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  function fail(message) { throw new Error('Vehicle impact geometry: ' + message); }
  function integer(n, label) {
    if (!Number.isSafeInteger(n) || n < 0) fail(label + ' must be a nonnegative integer');
    return n;
  }
  function vector(v, label) {
    if (!v || v.length !== 3 || !Array.from(v).every(Number.isFinite)) fail(label + ' must have three finite coordinates');
    return v;
  }
  function add(a, b) { return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]; }
  function sub(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
  function scale(a, s) { return [a[0] * s, a[1] * s, a[2] * s]; }
  function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function cross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  function length(a) { return Math.hypot(a[0], a[1], a[2]); }
  function normalize(a) { var n = length(a); return n ? scale(a, 1 / n) : [0, 0, 0]; }
  function emptyBounds() { return { min: [Infinity, Infinity, Infinity], max: [-Infinity, -Infinity, -Infinity] }; }
  function expandBounds(b, p) {
    for (var i = 0; i < 3; i++) { b.min[i] = Math.min(b.min[i], p[i]); b.max[i] = Math.max(b.max[i], p[i]); }
    return b;
  }
  function boundsDistanceSquared(p, b) {
    var sum = 0;
    for (var i = 0; i < 3; i++) { var d = Math.max(b.min[i] - p[i], 0, p[i] - b.max[i]); sum += d * d; }
    return sum;
  }
  function rayBounds(origin, direction, b, maxDistance) {
    var lo = 0, hi = maxDistance;
    for (var i = 0; i < 3; i++) {
      if (direction[i] === 0) { if (origin[i] < b.min[i] || origin[i] > b.max[i]) return false; }
      else {
        var a = (b.min[i] - origin[i]) / direction[i], c = (b.max[i] - origin[i]) / direction[i];
        lo = Math.max(lo, Math.min(a, c)); hi = Math.min(hi, Math.max(a, c));
        if (lo > hi) return false;
      }
    }
    return true;
  }
  function closestSegment(p, a, b) {
    var ab = sub(b, a), denom = dot(ab, ab);
    return add(a, scale(ab, denom ? Math.max(0, Math.min(1, dot(sub(p, a), ab) / denom)) : 0));
  }
  // Region tests from Real-Time Collision Detection, with a degenerate-triangle fallback.
  function closestTriangle(p, a, b, c) {
    var ab = sub(b, a), ac = sub(c, a), n = cross(ab, ac);
    if (dot(n, n) === 0) {
      var choices = [closestSegment(p, a, b), closestSegment(p, b, c), closestSegment(p, c, a)];
      return choices.reduce(function (best, q) { return dot(sub(q, p), sub(q, p)) < dot(sub(best, p), sub(best, p)) ? q : best; });
    }
    var ap = sub(p, a), d1 = dot(ab, ap), d2 = dot(ac, ap);
    if (d1 <= 0 && d2 <= 0) return a.slice();
    var bp = sub(p, b), d3 = dot(ab, bp), d4 = dot(ac, bp);
    if (d3 >= 0 && d4 <= d3) return b.slice();
    var vc = d1 * d4 - d3 * d2;
    if (vc <= 0 && d1 >= 0 && d3 <= 0) return add(a, scale(ab, d1 / (d1 - d3)));
    var cp = sub(p, c), d5 = dot(ab, cp), d6 = dot(ac, cp);
    if (d6 >= 0 && d5 <= d6) return c.slice();
    var vb = d5 * d2 - d1 * d6;
    if (vb <= 0 && d2 >= 0 && d6 <= 0) return add(a, scale(ac, d2 / (d2 - d6)));
    var va = d3 * d6 - d5 * d4;
    if (va <= 0 && d4 - d3 >= 0 && d5 - d6 >= 0) return add(b, scale(sub(c, b), (d4 - d3) / ((d4 - d3) + (d5 - d6))));
    var inverse = 1 / (va + vb + vc);
    return add(a, add(scale(ab, vb * inverse), scale(ac, vc * inverse)));
  }
  function rayTriangle(origin, direction, triangle, maxDistance) {
    var e1 = sub(triangle.b, triangle.a), e2 = sub(triangle.c, triangle.a);
    var p = cross(direction, e2), determinant = dot(e1, p);
    // A relative tolerance rejects parallel rays without rejecting small triangles.
    if (Math.abs(determinant) <= 1e-12 * length(e1) * length(e2)) return null;
    var inverse = 1 / determinant, t = sub(origin, triangle.a), u = dot(t, p) * inverse;
    if (u < -1e-10 || u > 1 + 1e-10) return null;
    var q = cross(t, e1), v = dot(direction, q) * inverse;
    if (v < -1e-10 || u + v > 1 + 1e-10) return null;
    var distance = dot(e2, q) * inverse;
    if (distance < 0 || distance > maxDistance) return null;
    return distance;
  }
  function result(triangle, position, distance) {
    return { position: position, distance: distance, normal: triangle.normal, component: triangle.component,
      material: triangle.material, primitiveIndex: triangle.primitiveIndex, triangle: triangle };
  }
  function matches(component, selector) {
    return selector === component || selector === component.id || selector === component.nodeIndex;
  }
  function createGeometry(components, nodes, materials, extras) {
    var triangles = [], bounds = emptyBounds();
    components.forEach(function (component) {
      component.triangles.forEach(function (triangle) {
        triangle.component = component;
        triangle.normal = normalize(cross(sub(triangle.b, triangle.a), sub(triangle.c, triangle.a)));
        triangles.push(triangle);
        [triangle.a, triangle.b, triangle.c].forEach(function (p) { expandBounds(component.bounds, p); expandBounds(bounds, p); });
      });
    });
    if (!triangles.length) fail('selected scene has no triangles');
    bounds.center = scale(add(bounds.min, bounds.max), 0.5);
    bounds.radius = length(sub(bounds.max, bounds.center));
    var geometry = { components: components, nodes: nodes, materials: materials, triangles: triangles, bounds: bounds, extras: extras };
    geometry.ray = function (origin, direction, maxDistance, predicate) {
      vector(origin, 'ray origin'); vector(direction, 'ray direction');
      var magnitude = length(direction);
      if (!magnitude || !Number.isFinite(magnitude)) fail('ray direction must have finite, nonzero length');
      direction = scale(direction, 1 / magnitude);
      if (maxDistance === undefined) maxDistance = Infinity;
      if (typeof maxDistance !== 'number' || !(maxDistance >= 0)) fail('ray maximum distance must be nonnegative');
      var nearest = null, limit = maxDistance;
      components.forEach(function (component) {
        if (!rayBounds(origin, direction, component.bounds, limit)) return;
        component.triangles.forEach(function (triangle) {
          if (predicate && !predicate(triangle, component)) return;
          var distance = rayTriangle(origin, direction, triangle, limit);
          if (distance !== null && (!nearest || distance < limit)) {
            nearest = result(triangle, add(origin, scale(direction, distance)), distance); limit = distance;
          }
        });
      });
      return nearest;
    };
    geometry.closestPoint = function (point, selectedComponent) {
      vector(point, 'query point');
      var nearest = null, bestSquared = Infinity;
      components.forEach(function (component) {
        if (selectedComponent !== undefined && selectedComponent !== null && !matches(component, selectedComponent)) return;
        if (boundsDistanceSquared(point, component.bounds) > bestSquared) return;
        component.triangles.forEach(function (triangle) {
          var position = closestTriangle(point, triangle.a, triangle.b, triangle.c), delta = sub(point, position), squared = dot(delta, delta);
          if (squared < bestSquared) { bestSquared = squared; nearest = result(triangle, position, Math.sqrt(squared)); }
        });
      });
      return nearest;
    };
    // Closed segment, including both endpoints; callers choose which components to ignore.
    geometry.segmentLOS = function (start, end, ignoreComponents) {
      vector(start, 'segment start'); vector(end, 'segment end');
      var delta = sub(end, start), distance = length(delta), ignored = ignoreComponents || [];
      if (!Array.isArray(ignored) && !(ignored instanceof Set)) ignored = [ignored];
      var hit = distance ? geometry.ray(start, delta, distance, function (_, component) {
        return !Array.from(ignored).some(function (selector) { return matches(component, selector); });
      }) : null;
      return { clear: hit === null, hit: hit, distance: distance };
    };
    return geometry;
  }

  function identity() { return [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]; }
  function multiply(a, b) {
    var out = new Array(16).fill(0);
    for (var c = 0; c < 4; c++) for (var r = 0; r < 4; r++) for (var k = 0; k < 4; k++) out[c * 4 + r] += a[k * 4 + r] * b[c * 4 + k];
    return out;
  }
  function localMatrix(node) {
    if (node.matrix) {
      if (node.translation || node.rotation || node.scale) fail('node cannot combine matrix and TRS');
      if (node.matrix.length !== 16 || !node.matrix.every(Number.isFinite)) fail('node matrix must contain 16 finite numbers');
      if (node.matrix[3] !== 0 || node.matrix[7] !== 0 || node.matrix[11] !== 0 || node.matrix[15] !== 1) fail('node matrix must be affine');
      return node.matrix.slice();
    }
    var t = node.translation || [0, 0, 0], s = node.scale || [1, 1, 1], q = node.rotation || [0, 0, 0, 1];
    vector(t, 'node translation'); vector(s, 'node scale');
    if (q.length !== 4 || !q.every(Number.isFinite)) fail('node rotation must contain four finite numbers');
    var norm = Math.hypot.apply(null, q);
    if (!norm) fail('node rotation quaternion must be nonzero');
    var x = q[0] / norm, y = q[1] / norm, z = q[2] / norm, w = q[3] / norm;
    return [(1 - 2 * (y*y + z*z))*s[0], 2*(x*y + z*w)*s[0], 2*(x*z - y*w)*s[0], 0,
      2*(x*y - z*w)*s[1], (1 - 2*(x*x + z*z))*s[1], 2*(y*z + x*w)*s[1], 0,
      2*(x*z + y*w)*s[2], 2*(y*z - x*w)*s[2], (1 - 2*(x*x + y*y))*s[2], 0, t[0], t[1], t[2], 1];
  }
  function transformPoint(m, p) {
    return [m[0]*p[0] + m[4]*p[1] + m[8]*p[2] + m[12], m[1]*p[0] + m[5]*p[1] + m[9]*p[2] + m[13], m[2]*p[0] + m[6]*p[1] + m[10]*p[2] + m[14]];
  }
  function byteRange(buffer, offset, count, label) {
    integer(offset, label + ' offset'); integer(count, label + ' length');
    if (!buffer || offset + count > buffer.byteLength) fail(label + ' exceeds its buffer');
    return new Uint8Array(buffer.buffer, buffer.byteOffset + offset, count);
  }
  async function load(arrayBuffer, decoder) {
    if (!(arrayBuffer instanceof ArrayBuffer)) fail('load expects an ArrayBuffer');
    if (arrayBuffer.byteLength < 20) fail('truncated GLB header');
    var header = new DataView(arrayBuffer);
    if (header.getUint32(0, true) !== 0x46546c67 || header.getUint32(4, true) !== 2) fail('expected a version 2 GLB');
    if (header.getUint32(8, true) !== arrayBuffer.byteLength) fail('GLB declared length does not match the input');
    var json = null, binary = null, offset = 12;
    while (offset < arrayBuffer.byteLength) {
      if (offset + 8 > arrayBuffer.byteLength) fail('truncated GLB chunk header');
      var size = header.getUint32(offset, true), kind = header.getUint32(offset + 4, true);
      if (size % 4 || offset + 8 + size > arrayBuffer.byteLength) fail('invalid GLB chunk bounds');
      var bytes = new Uint8Array(arrayBuffer, offset + 8, size);
      if (kind === 0x4e4f534a) {
        if (json || offset !== 12) fail('GLB must start with one JSON chunk');
        try { json = JSON.parse(new TextDecoder().decode(bytes)); } catch (error) { fail('invalid GLB JSON: ' + error.message); }
      } else if (kind === 0x004e4942) { if (binary) fail('multiple binary chunks are unsupported'); binary = bytes; }
      offset += 8 + size;
    }
    if (!json || !json.asset || json.asset.version !== '2.0') fail('missing glTF 2.0 asset');
    (json.extensionsRequired || []).forEach(function (extension) {
      if (extension !== 'EXT_meshopt_compression' && extension !== 'KHR_mesh_quantization') fail('unsupported required extension ' + extension);
    });
    function sourceBuffer(index) {
      var buffer = (json.buffers || [])[index];
      if (index !== 0 || !buffer || buffer.uri || !binary) fail('only the embedded GLB buffer is supported');
      integer(buffer.byteLength, 'buffer length');
      if (buffer.byteLength > binary.byteLength) fail('embedded buffer is truncated');
      return binary.subarray(0, buffer.byteLength);
    }
    var views = [];
    for (var vi = 0; vi < (json.bufferViews || []).length; vi++) {
      var view = json.bufferViews[vi], compressed = (view.extensions || {}).EXT_meshopt_compression;
      integer(view.byteLength, 'bufferView length');
      if (compressed) {
        if (!decoder || typeof decoder.decodeGltfBuffer !== 'function' || decoder.supported === false) fail('MeshoptDecoder is required for compressed geometry');
        await decoder.ready;
        integer(compressed.count, 'meshopt count'); integer(compressed.byteStride, 'meshopt stride');
        if (!compressed.byteStride || compressed.count * compressed.byteStride !== view.byteLength) fail('meshopt decoded length does not match bufferView');
        if (!['ATTRIBUTES', 'TRIANGLES', 'INDICES'].includes(compressed.mode)) fail('unsupported meshopt mode');
        if (!['NONE', 'OCTAHEDRAL', 'QUATERNION', 'EXPONENTIAL'].includes(compressed.filter || 'NONE')) fail('unsupported meshopt filter');
        var source = byteRange(sourceBuffer(compressed.buffer), compressed.byteOffset || 0, compressed.byteLength, 'meshopt source');
        var decoded = new Uint8Array(view.byteLength);
        decoder.decodeGltfBuffer(decoded, compressed.count, compressed.byteStride, source, compressed.mode, compressed.filter || 'NONE');
        views.push(decoded);
      } else views.push(byteRange(sourceBuffer(view.buffer), view.byteOffset || 0, view.byteLength, 'bufferView'));
    }
    var accessors = new Map();
    function accessor(index, expectedType, indexData) {
      if (accessors.has(index)) {
        var cached = accessors.get(index);
        if (cached.type !== expectedType || cached.indexData !== indexData) fail('accessor used with incompatible semantics');
        return cached.values;
      }
      var a = (json.accessors || [])[index];
      if (!a || a.type !== expectedType) fail('missing accessor or unexpected type for accessor ' + index);
      if (a.sparse) fail('sparse accessors are unsupported');
      var formats = { 5120: [1, 'getInt8'], 5121: [1, 'getUint8'], 5122: [2, 'getInt16'], 5123: [2, 'getUint16'], 5125: [4, 'getUint32'], 5126: [4, 'getFloat32'] };
      var format = formats[a.componentType], width = expectedType === 'VEC3' ? 3 : 1;
      if (!format) fail('unsupported accessor component type ' + a.componentType);
      if (indexData && (![5121, 5123, 5125].includes(a.componentType) || a.normalized)) fail('indices must be unsigned, unnormalized integers');
      if (a.normalized && (a.componentType === 5125 || a.componentType === 5126)) fail('unsupported normalized accessor type');
      integer(a.count, 'accessor count');
      var bytes = views[a.bufferView], descriptor = (json.bufferViews || [])[a.bufferView];
      if (!bytes || !descriptor) fail('accessor bufferView is missing');
      var stride = descriptor.byteStride || width * format[0], start = a.byteOffset || 0;
      integer(stride, 'accessor stride'); integer(start, 'accessor offset');
      if (stride < width * format[0] || stride % format[0] || start % format[0]) fail('invalid accessor stride or alignment');
      if (a.count && start + (a.count - 1) * stride + width * format[0] > bytes.byteLength) fail('accessor exceeds bufferView');
      var dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength), values = [];
      for (var i = 0; i < a.count; i++) {
        var entry = [];
        for (var j = 0; j < width; j++) {
          var value = dv[format[1]](start + i * stride + j * format[0], true);
          if (a.normalized) {
            var divisor = { 5120: 127, 5121: 255, 5122: 32767, 5123: 65535 }[a.componentType];
            value = Math.max(-1, value / divisor);
          }
          if (!Number.isFinite(value)) fail('non-finite accessor value');
          entry.push(value);
        }
        values.push(width === 1 ? entry[0] : entry);
      }
      accessors.set(index, { values: values, type: expectedType, indexData: indexData });
      return values;
    }
    var materials = (json.materials || []).map(function (material, index) {
      return { index: index, name: material.name || 'Material ' + index, extras: material.extras || {} };
    });
    var nodes = [], components = [], visited = new Set(), active = new Set();
    function visit(index, parentMatrix, parentIndex) {
      integer(index, 'node index');
      if (active.has(index)) fail('node hierarchy contains a cycle');
      if (visited.has(index)) fail('node has multiple parents in the selected scene');
      var node = (json.nodes || [])[index];
      if (!node) fail('missing node ' + index);
      if (node.skin !== undefined || node.weights) fail('skinned or morphed meshes are unsupported');
      if ((node.extensions || {}).EXT_mesh_gpu_instancing) fail('GPU-instanced nodes are unsupported');
      active.add(index); visited.add(index);
      var matrix = multiply(parentMatrix, localMatrix(node));
      if (!matrix.every(Number.isFinite)) fail('non-finite composed node transform');
      var placed = { nodeIndex: index, name: node.name || 'Node ' + index, parentIndex: parentIndex, matrix: matrix,
        extras: node.extras || {}, component: null, bounds: null, triangles: [] };
      nodes.push(placed);
      if (node.mesh !== undefined) {
        var mesh = (json.meshes || [])[node.mesh];
        if (!mesh) fail('missing node mesh');
        var component = { id: 'node:' + index, nodeIndex: index, name: placed.name, extras: placed.extras,
          wheel: placed.extras.wheel || null, nativeComponentKey: placed.extras.native_component_key || null,
          bounds: emptyBounds(), primitives: [], triangles: [] };
        placed.component = component; placed.bounds = component.bounds; placed.triangles = component.triangles;
        components.push(component);
        (mesh.primitives || []).forEach(function (primitive, primitiveIndex) {
          if (primitive.mode !== undefined && primitive.mode !== 4) fail('only TRIANGLES primitives are supported');
          if (primitive.targets || (primitive.extensions || {}).KHR_draco_mesh_compression) fail('morph targets and Draco geometry are unsupported');
          var positions = accessor((primitive.attributes || {}).POSITION, 'VEC3', false).map(function (p) {
            return vector(transformPoint(matrix, p), 'transformed position');
          });
          var indices = primitive.indices === undefined ? positions.map(function (_, i) { return i; }) : accessor(primitive.indices, 'SCALAR', true);
          if (indices.length % 3) fail('triangle index count is not divisible by three');
          var material = primitive.material === undefined ? null : materials[primitive.material];
          if (primitive.material !== undefined && !material) fail('missing primitive material');
          var record = { index: primitiveIndex, material: material, positions: positions, indices: indices, triangles: [] };
          component.primitives.push(record);
          for (var i = 0; i < indices.length; i += 3) {
            var corners = indices.slice(i, i + 3);
            if (corners.some(function (v) { return !Number.isInteger(v) || v < 0 || v >= positions.length; })) fail('triangle index exceeds positions');
            var triangle = { a: positions[corners[0]], b: positions[corners[1]], c: positions[corners[2]], material: material, primitiveIndex: primitiveIndex, index: i / 3 };
            record.triangles.push(triangle); component.triangles.push(triangle);
          }
        });
      }
      (node.children || []).forEach(function (child) { visit(child, matrix, index); });
      active.delete(index);
    }
    var scene = (json.scenes || [])[json.scene === undefined ? 0 : json.scene];
    if (!scene || !Array.isArray(scene.nodes)) fail('missing default scene');
    scene.nodes.forEach(function (index) { visit(index, identity(), null); });
    return createGeometry(components, nodes, materials, json.asset.extras || {});
  }
  return { load: load, add: add, sub: sub, scale: scale, dot: dot, cross: cross, length: length, normalize: normalize,
    emptyBounds: emptyBounds, expandBounds: expandBounds, boundsDistanceSquared: boundsDistanceSquared,
    rayBounds: rayBounds, closestTriangle: closestTriangle, rayTriangle: rayTriangle, multiply: multiply, transformPoint: transformPoint };
}));
