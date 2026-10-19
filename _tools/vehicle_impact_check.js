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

function verifyShot(vehicle, source, result) {
  const context = `${vehicle.id}: ${source.id}`;
  const tags = result.applications.map(hit => hit.hitLocation).filter(Boolean);
  assert.equal(tags.length, new Set(tags).size, `Repeated damage tag: ${context}`);
  assert.equal(result.incomplete, 0, `Missing component metadata: ${context}`);
  const ledger = {};
  for (const transfer of result.transfers) {
    assert.ok(vehicle.sections[transfer.section], `Unknown route target: ${context}`);
    assert.ok(Number.isFinite(transfer.amount) && transfer.amount > 0, context);
    if (transfer.via) assert.ok(vehicle.sections[transfer.via.section], context);
    ledger[transfer.section] = (ledger[transfer.section] || 0) + transfer.amount;
  }
  for (const [key, section] of Object.entries(vehicle.sections)) {
    assert.ok(Number.isFinite(result.health[key]) && result.health[key] >= 0 &&
      result.health[key] <= section.max_health, `Invalid section health: ${context}: ${key}`);
    near(result.sectionDamage[key], ledger[key] || 0);
    near(result.sectionDamage[key] + result.health[key], section.max_health);
  }
  for (const hit of result.hits) {
    assert.ok(hit.slotIndex >= 0, `Unresolved slot ${hit.material.name}: ${context}`);
    assert.ok(Number.isFinite(hit.factor), `Missing explosive rule factor: ${context}`);
    near(hit.amount, hit.base * hit.factor);
  }
}

function placements(mesh) {
  const b = mesh.bounds, result = [];
  for (let axis = 0; axis < 3; axis++) for (const sign of [-1, 1]) {
    const origin = b.center.slice(), direction = [0, 0, 0];
    origin[axis] = (sign < 0 ? b.min[axis] : b.max[axis]) + sign * 2;
    direction[axis] = -sign;
    const hit = mesh.ray(origin, direction);
    if (hit) result.push({kind: `surface-${axis}-${sign}`, point: hit.position});
  }
  for (const sign of [-1, 1]) result.push({kind: `ground-${sign}`,
    point: [b.center[0], b.min[1], (sign < 0 ? b.min[2] : b.max[2]) + sign]});
  return result;
}

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
  const offsetCaliber = {blast: {impact_backoff_cm: 12.7}};
  assert.deepEqual(impact.detonationOrigin(offsetCaliber, [1, 2, 3], [0, 0, -10]), [1, 2, 3.127]);
  assert.deepEqual(impact.detonationOrigin(offsetCaliber, [1, 2, 3], [0, 0, 0]), [1, 2, 3]);
  assert.deepEqual(impact.detonationOrigin(offsetCaliber, [1, 2, 3], [0, 0, 1e-7]), [1, 2, 3]);
  assert.deepEqual(impact.detonationOrigin({blast: {}}, [1, 2, 3], [0, 0, -10]), [1, 2, 3]);
  const dedupVehicle = {slots: [
    {section: "One", hit_location: "Vehicle.Main"},
    {section: "Two", hit_location: "Vehicle.Main"},
    {section: "One", hit_location: "Vehicle.Wheel"},
    {section: "Unknown", hit_location: null}
  ]};
  const dedup = impact.damageApplications(dedupVehicle, [0, 1, 2, 3, 3].map(slotIndex => ({slotIndex})));
  assert.deepEqual(dedup.map(hit => hit.slotIndex), [0, 2, 3, 3]); // Key is the tag, not section or component.

  let sectionChecks = 0;
  for (const vehicle of data.vehicles) for (const [key, section] of Object.entries(vehicle.sections)) {
    for (const amount of [1, section.max_health / 2, section.max_health * 2]) {
      const health = impact.freshHealth(vehicle), transfers = [], sectionDamage = {};
      impact.applyRadial(vehicle.sections, health, key, amount, 0, transfers);
      for (const [target, targetSection] of Object.entries(vehicle.sections))
        sectionDamage[target] = targetSection.max_health - health[target];
      verifyShot(vehicle, {id: `section-${key}-${amount}`}, {
        applications: [], incomplete: 0, health, transfers, sectionDamage, hits: []
      });
      sectionChecks++;
    }
  }
  console.log(`routing verification: ${data.vehicles.length} profiles, ${sectionChecks} fresh section applications passed`);
  if (process.argv.includes("--routing-only")) return;

  let models = 0, nodes = 0, triangles = 0, shots = 0, catalogShots = 0;
  let sources = data.meta.calibers.filter(c => c.blast).concat(data.meta.explosives);
  const sourceIndex = process.argv.indexOf("--source");
  if (sourceIndex >= 0) {
    sources = sources.filter(source => source.id === process.argv[sourceIndex + 1]);
    assert.equal(sources.length, 1, "--source must name one exported explosive source");
  }
  const coverage = [];
  const vehicleIndex = process.argv.indexOf("--vehicle-prefix");
  const vehicles = vehicleIndex < 0 ? data.vehicles
    : data.vehicles.filter(vehicle => vehicle.id.startsWith(process.argv[vehicleIndex + 1] || "__missing__"));
  assert.ok(vehicles.length, "--vehicle-prefix must match an exported vehicle");
  const source = data.meta.calibers.find(c => c.id === "Item.Caliber.84mm");
  assert.ok(source && source.blast, "Reviewed MAAWS projectile missing");
  near(source.blast.impact_backoff_cm, 12.7);
  const before = JSON.stringify(data);
  for (const vehicle of vehicles) {
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
      const points = placements(mesh);
      const row = {vehicle: vehicle.id, model: model.path, sources: sources.length,
        surfacePlacements: points.filter(p => p.kind.startsWith("surface")).length,
        groundPlacements: 2, shots: 0, damagingShots: 0};
      assert.ok(row.surfacePlacements > 0, `No surface placement: ${model.path}`);
      for (const explosive of sources) {
        for (const placement of points) {
          const result = impact.simulate(mesh, vehicle, explosive, placement.point, mapping);
          verifyShot(vehicle, explosive, result);
          row.shots++; catalogShots++;
          if (Object.values(result.sectionDamage).some(amount => amount > 0)) row.damagingShots++;
        }
        const outside = [mesh.bounds.max[0] + explosive.blast.radius / 100 + 5,
          mesh.bounds.center[1], mesh.bounds.center[2]];
        const miss = impact.simulate(mesh, vehicle, explosive, outside, mapping);
        verifyShot(vehicle, explosive, miss);
        assert.equal(miss.hits.length, 0, `Out-of-range contact: ${model.path}: ${explosive.id}`);
        assert.ok(Object.values(miss.sectionDamage).every(amount => amount === 0));
        row.shots++; catalogShots++;
      }
      coverage.push(row);
      if (vehicle.damage_row.endsWith(".TNK_01.AntiAir")) {
        assert.equal(Object.values(mapping).reduce((sum, node) => sum + node.point_sampling.points.length, 0), 89);
        const front = mesh.ray([0, 1, 8], [0, 0, -1]);
        assert.ok(front && front.material.name === "CC_MainBody");
        const result = impact.simulate(mesh, vehicle, source, front.position, mapping);
        assert.equal(result.samplingMode, "native-sockets");
        assert.equal(result.hits.length, 5, "Retain exposed component contacts for inspection");
        assert.equal(result.applications.length, 1, "Main-hit contacts must not multiply blast damage");
        near(result.mainDamage, 267.9);
        const fuel = MAIN + ".FuelTank";
        near(result.sectionDamage[fuel], 14.1);
        assert.ok(result.hits.every(hit => hit.material.name !== "CC_FuelTank"), "Fuel surface must stay occluded");
        const fuelTransfer = result.transfers.filter(entry => entry.section === fuel);
        assert.ok(fuelTransfer.every(entry => entry.via && entry.via.section === MAIN));
        near(fuelTransfer.reduce((sum, entry) => sum + entry.amount, 0), 14.1);
        const backed = impact.simulate(mesh, vehicle, source,
          impact.detonationOrigin(source, front.position, [0, 0, -1]), mapping);
        // Stopping at the first accepted socket gives 31.8 cm and 193.7 cm respectively.
        assert.ok(backed.hits.find(hit => hit.nativeComponent.endsWith(":MainBody")).distance < 11);
        assert.ok(backed.hits.find(hit => hit.nativeComponent.endsWith(":TurretSpin")).distance < 174);
        near(backed.mainDamage, 267.9);
      }
      if (vehicle.id.startsWith("land-tracked-leopard-spawn-")) {
        const front = mesh.ray([0, 1, mesh.bounds.max[2] + 2], [0, 0, -1]);
        assert.ok(front && front.material.name === "CC_MainBody");
        for (const backoff of [0, 0.127]) {
          const origin = front.position.map((value, i) => value + (i === 2 ? backoff : 0));
          const result = impact.simulate(mesh, vehicle, source, origin, mapping);
          assert.equal(result.samplingMode, "native-bounds");
          assert.equal(result.applications.length, 1, "SPW front hit must not acquire a false radar application");
          assert.ok(result.hits.every(hit => hit.material.name !== "CC_Radar"), "SPW radar bounds target is occluded");
          near(result.mainDamage, 361);
          near(result.sectionDamage[MAIN + ".FuelTank"], 19);
          near(result.health[MAIN + ".Radar"], 100);
        }
        const side = mesh.ray([mesh.bounds.max[0] + 2, 0.5, 0], [-1, 0, 0]);
        assert.ok(side && side.material.name === "CC_Tracks_L");
        const track = impact.simulate(mesh, vehicle, source,
          impact.detonationOrigin(source, side.position, [-1, 0, 0]), mapping);
        assert.equal(track.firstSection, MAIN + ".Tracks.Left");
        assert.equal(track.applications.length, 1);
        near(track.sectionDamage[MAIN + ".Tracks.Left"], 125);
        near(track.mainDamage, 121.125);
        near(track.sectionDamage[MAIN + ".FuelTank"], 6.375);
        // Conditional fixed-contact sequence; collision/deployment changes are not simulated.
        const running = impact.freshHealth(vehicle);
        for (const section of [MAIN + ".Tracks.Left", MAIN, MAIN])
          impact.applyRadial(vehicle.sections, running, section, 380);
        near(running[MAIN], 156.875);
        impact.applyRadial(vehicle.sections, running, MAIN, 380);
        near(running[MAIN], 0);
      }
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
  const expectedModels = vehicles.reduce((sum, vehicle) => sum + vehicle.models.reduce((count, model) =>
    count + 1 + (model.wheels_destroyed ? 1 : 0), 0), 0);
  assert.equal(models, expectedModels);
  console.log(`impact preview: ${models} models, ${nodes} nodes, ${triangles} triangles, ${shots} fresh/out-of-range shots passed`);
  console.log(`catalog verification: ${vehicles.length} vehicle profiles, ${sources.length} explosive sources, ${catalogShots} shots passed`);
  const reportIndex = process.argv.indexOf("--report");
  if (reportIndex >= 0) {
    assert.ok(process.argv[reportIndex + 1], "--report requires a path");
    fs.writeFileSync(process.argv[reportIndex + 1], JSON.stringify({
      scope: "Offline reference-pose software checks; no runtime collision parity established",
      vehicleProfiles: vehicles.length, models, sectionChecks,
      profilesWithoutGeometry: vehicles.filter(v => !v.models.length).map(v => v.id),
      sources: sources.map(s => s.id), shots: catalogShots, coverage
    }, null, 2) + "\n", {flag: "wx"});
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
