/* Spatial index for offline audits. Uses the viewer's exact triangle query functions. */
"use strict";
const G = require("../assets/js/vehicle-impact-geometry.js");

function attach(mesh) {
  const original = {ray: mesh.ray, closestPoint: mesh.closestPoint};
  const order = new Map(mesh.triangles.map((triangle, index) => [triangle, index]));
  function build(triangles) {
    const bounds = G.emptyBounds();
    for (const triangle of triangles) for (const p of [triangle.a, triangle.b, triangle.c]) G.expandBounds(bounds, p);
    // Triangle queries tolerate edge rounding; internal boxes must not trim those hits.
    const padding = Math.max(1, ...G.sub(bounds.max, bounds.min)) * 1e-9;
    for (let i = 0; i < 3; i++) { bounds.min[i] -= padding; bounds.max[i] += padding; }
    if (triangles.length <= 12) return {bounds, triangles};
    const span = G.sub(bounds.max, bounds.min), axis = span.indexOf(Math.max(...span));
    triangles.sort((a, b) => (a.a[axis] + a.b[axis] + a.c[axis]) -
      (b.a[axis] + b.b[axis] + b.c[axis]) || order.get(a) - order.get(b));
    const half = Math.floor(triangles.length / 2);
    return {bounds, children: [build(triangles.slice(0, half)), build(triangles.slice(half))]};
  }
  const trees = new Map(mesh.components.map(c => [c, build(c.triangles.slice())]));
  function result(triangle, position, distance) {
    return {position, distance, normal: triangle.normal, component: triangle.component,
      material: triangle.material, primitiveIndex: triangle.primitiveIndex, triangle};
  }
  function valid(v) { return v && v.length === 3 && Array.from(v).every(Number.isFinite); }
  mesh.ray = function (origin, direction, maxDistance, predicate) {
    const magnitude = valid(direction) ? G.length(direction) : 0;
    if (!valid(origin) || !magnitude || !Number.isFinite(magnitude) ||
        (maxDistance !== undefined && !(typeof maxDistance === "number" && maxDistance >= 0)))
      return original.ray(origin, direction, maxDistance, predicate);
    direction = G.scale(direction, 1 / magnitude);
    let nearest = null, limit = maxDistance === undefined ? Infinity : maxDistance;
    function visit(node) {
      if (!G.rayBounds(origin, direction, node.bounds, limit)) return;
      if (node.children) { node.children.forEach(visit); return; }
      for (const triangle of node.triangles) {
        if (predicate && !predicate(triangle, triangle.component)) continue;
        const distance = G.rayTriangle(origin, direction, triangle, limit);
        if (distance !== null && (!nearest || distance < limit ||
            (distance === limit && order.get(triangle) < order.get(nearest.triangle)))) {
          nearest = result(triangle, G.add(origin, G.scale(direction, distance)), distance);
          limit = distance;
        }
      }
    }
    mesh.components.forEach(c => {
      if (G.rayBounds(origin, direction, c.bounds, limit)) visit(trees.get(c));
    });
    return nearest;
  };
  mesh.closestPoint = function (point, selectedComponent) {
    if (!valid(point)) return original.closestPoint(point, selectedComponent);
    let nearest = null, bestSquared = Infinity;
    function visit(node) {
      if (G.boundsDistanceSquared(point, node.bounds) > bestSquared) return;
      if (node.children) {
        node.children.slice().sort((a, b) => G.boundsDistanceSquared(point, a.bounds) -
          G.boundsDistanceSquared(point, b.bounds)).forEach(visit);
        return;
      }
      for (const triangle of node.triangles) {
        const position = G.closestTriangle(point, triangle.a, triangle.b, triangle.c);
        const delta = G.sub(point, position), squared = G.dot(delta, delta);
        if (squared < bestSquared || (squared === bestSquared && nearest &&
            order.get(triangle) < order.get(nearest.triangle))) {
          bestSquared = squared; nearest = result(triangle, position, Math.sqrt(squared));
        }
      }
    }
    for (const c of mesh.components) if (selectedComponent == null || selectedComponent === c ||
      selectedComponent === c.id || selectedComponent === c.nodeIndex) visit(trees.get(c));
    return nearest;
  };
  return original;
}

module.exports = {attach};
