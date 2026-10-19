/* Offline contracts for the reference-pose blast preview and its published geometry. */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const geometryAPI = require("../assets/js/vehicle-impact-geometry.js");
const impact = require("../assets/js/vehicle-impact.js");
const decoder = require("../assets/js/vendor/meshopt_decoder-1.2.0.js");
const root = path.join(__dirname, "..");
const data = JSON.parse(fs.readFileSync(path.join(root, "assets/data/vehicle-hitboxes.json")));
const metadata = JSON.parse(fs.readFileSync(path.join(root, "assets/data/vehicle-impact-components.json")));
const MAIN = "Attribute.Gameplay.Health";
const near = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-7, `${actual} != ${expected}`);

async function main() {
  const cal = {base_damage: 100, blast: {radius: 1000, effective_radius: 500, minimum: 10, falloff: 1}};
  near(impact.blastAmount(cal, 0), 100);
  near(impact.blastAmount(cal, 500), 100);
  near(impact.blastAmount(cal, 750), 50);
  near(impact.blastAmount(cal, 1000), 10); // Native minimum still applies to an accepted boundary hit.
  near(impact.blastAmount({...cal, blast: {...cal.blast, radius: 300, effective_radius: 600}}, 400), 100);
  const sections = {
    [MAIN]: {max_health: 1000, pre: [], post: [], simultaneous: []},
    Track: {max_health: 100, pre: [], post: [[MAIN, 1, true]], simultaneous: [[MAIN, 1, false]],
      radial_routing_skips: {simultaneous: true}}
  };
  let health = impact.freshHealth({sections});
  impact.applyRadial(sections, health, "Track", 150);
  near(health.Track, 0); near(health[MAIN], 950); // No simultaneous copy from a radial-skipping track.
  sections.Track.radial_routing_skips.simultaneous = false;
  health = impact.freshHealth({sections});
  impact.applyRadial(sections, health, "Track", 150);
  near(health[MAIN], 850);
  const starts = impact.cloud([0, 0, 0], false);
  assert.equal(starts.length, 15);
  assert.deepEqual(starts[1], [0, 0.5, 0]); // UE up -> displayed +Y.
  starts.slice(1).forEach(p => near(Math.hypot(...p), 0.5));
  assert.deepEqual(impact.cloud([0, 0, 0], true)[0], starts[1]);

  let models = 0, nodes = 0, triangles = 0, shots = 0;
  const source = data.meta.calibers.find(c => c.id === "Item.Caliber.84mm");
  assert.ok(source && source.blast, "Reviewed MAAWS projectile missing");
  const before = JSON.stringify(data);
  for (const vehicle of data.vehicles) {
    for (const base of vehicle.models) for (const model of [base, base.wheels_destroyed].filter(Boolean)) {
      const buffer = fs.readFileSync(path.join(root, model.path));
      const mesh = await geometryAPI.load(buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength), decoder);
      assert.ok(mesh.bounds.min.concat(mesh.bounds.max).every(Number.isFinite));
      const mapping = metadata.models[model.path];
      assert.ok(mapping, model.path);
      for (const component of mesh.components) {
        assert.ok(mapping[component.nodeIndex]?.component, `Missing component: ${model.path}:${component.nodeIndex}`);
      }
      models++; nodes += mesh.components.length; triangles += mesh.triangles.length;
      if (!model.path.endsWith("--wheels-destroyed.glb")) {
        const bounds = mesh.bounds;
        const origin = [bounds.max[0] + 1, bounds.min[1], bounds.center[2]];
        const result = impact.simulate(mesh, vehicle, source, origin, mapping);
        assert.ok(Number.isFinite(result.mainDamage) && result.mainDamage >= 0 && result.mainDamage <= vehicle.main_health);
        const ids = result.hits.map(hit => hit.nativeComponent);
        assert.equal(ids.length, new Set(ids).size, "A native component was counted twice");
        result.hits.forEach(hit => {
          assert.ok(hit.distance <= source.blast.radius + 1e-5);
          near(hit.amount, hit.base * hit.factor);
        });
        if (result.hits.length) {
          const first = vehicle.slots[result.hits[0].slotIndex];
          assert.equal(result.firstSection, first ? first.section : null);
        }
        const outside = impact.simulate(mesh, vehicle, source, [bounds.max[0] + source.blast.radius / 100 + 5, 0, 0], mapping);
        assert.equal(outside.hits.length, 0); near(outside.mainDamage, 0);
        shots += 2;
      }
    }
  }
  assert.equal(JSON.stringify(data), before, "Shots must not mutate exported health/data");
  assert.equal(models, 36);
  console.log(`impact preview: ${models} models, ${nodes} nodes, ${triangles} triangles, ${shots} fresh/out-of-range shots passed`);
}
main().catch(error => { console.error(error); process.exitCode = 1; });
