/* Offline contracts for the reference-pose blast preview and its published geometry. */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const geometryAPI = require("../assets/js/vehicle-impact-geometry.js");
const impact = require("../assets/js/vehicle-impact.js");
const decoder = require("../assets/js/vendor/meshopt_decoder-1.2.0.js");
const queryIndex = require("./vehicle_query_index.js");
const root = path.join(__dirname, "..");
const data = JSON.parse(fs.readFileSync(path.join(root, "assets/data/vehicle-hitboxes.json")));
const metadata = JSON.parse(fs.readFileSync(path.join(root, "assets/data/vehicle-impact-components.json")));
const samplingFixture = JSON.parse(fs.readFileSync(path.join(root, "_tools/vehicle-impact-sampling.json")));
const MAIN = "Attribute.Gameplay.Health";
const near = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-7, `${actual} != ${expected}`);

function verifyShot(vehicle, source, result) {
  const context = `${vehicle.id}: ${source.id}`;
  const tags = result.applications.map(hit => hit.hitLocation).filter(Boolean);
  assert.equal(tags.length, new Set(tags).size, `Repeated damage tag: ${context}`);
  assert.equal(result.incomplete, 0, `Missing component metadata: ${context}`);
  const components = result.hits.map(hit => hit.nativeComponent);
  assert.equal(components.length, new Set(components).size, `Repeated native component: ${context}`);
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
    assert.ok(Number.isFinite(hit.amount) && hit.amount >= 0, `Invalid modified amount: ${context}`);
    if (vehicle.blast_rule_recipes)
      assert.equal(hit.amount, Math.fround(hit.amount), `Modified amount must be float32: ${context}`);
    else near(hit.amount, hit.base * hit.factor);
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
  const havoc = data.vehicles.find(vehicle => vehicle.id === "air-rotary-havoc");
  const rocket72 = data.meta.calibers.find(source => source.id === "Item.Caliber.72mm");
  assert.equal(impact.blastDamage(havoc, 0, rocket72, 0, 200), 400.0000305175781);
  assert.equal(impact.blastDamage(havoc, 0, rocket72, 1, 200), 80.00000762939453);
  assert.equal(impact.evaluateBlastRecipe({clamp: true, operations: [[3, 10], [2, 100]]}, 100), 220);
  assert.equal(impact.evaluateBlastRecipe({clamp: true, operations: [[2, 100], [3, 10]]}, 100), 210);
  assert.throws(() => impact.blastDamage({...havoc, blast_rule_recipes: []}, 0, rocket72, 0, 200),
    /Missing native blast rule recipe/);
  assert.equal(impact.blastDamage({slots: [{blast_factor: {legacy: [0.3, 0.3]}}]},
    0, {id: "legacy"}, 0, 0.1), 0.03, "Preserve factor-only vehicle inputs");
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
  const cycling = {A: {max_health: 100, pre: [["B", 1, false]]},
    B: {max_health: 100, pre: [["A", 1, false]]}};
  health = impact.freshHealth({sections: cycling});
  assert.equal(impact.applyRadial(cycling, health, "A", 40), 0);
  assert.deepEqual(health, {A: 100, B: 100}, "Native visit-limit abort must propagate through pre routing");
  const chain = Object.fromEntries(Array.from({length: 12}, (_, i) => ["S" + i,
    {max_health: 1, post: i < 11 ? [["S" + (i + 1), 1, true]] : []}]));
  health = impact.freshHealth({sections: chain});
  assert.equal(impact.applyRadial(chain, health, "S0", 20), 12);
  assert.ok(Object.values(health).every(value => value === 0), "Distinct sections have separate native visit counts");
  const mainCopy = {[MAIN]: {max_health: 100, simultaneous: [["Fuel", 0.5, false]]},
    Fuel: {max_health: 100}};
  health = impact.freshHealth({sections: mainCopy});
  assert.equal(impact.applyRadial(mainCopy, health, MAIN, 100), 100);
  assert.equal(health.Fuel, 50, "Simultaneous routing precedes the depleted-main post-route gate");
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
  const contacts = ["A0", "A1", "A2", "B0", "B1", "C0"].map((id, i) =>
    ({id, nativeComponent: id[0], distance: i + 1}));
  assert.deepEqual(impact.vehicleContacts(contacts).map(h => h.id), ["A0", "C0", "B1"]);
  assert.equal(contacts.length, 6, "Component filtering must not mutate gathered input");
  assert.deepEqual(impact.vehicleContacts([contacts[5], contacts[0]]).map(h => h.id), ["A0", "C0"]);
  // Raw native-sort replay: even the short-array path swaps equal keys.
  const tied = ["A", "B", "C"].map(id => ({id, nativeComponent: id, distance: 1}));
  assert.deepEqual(impact.vehicleContacts(tied.slice(0, 2)).map(h => h.id), ["B", "A"]);
  assert.deepEqual(impact.vehicleContacts(tied).map(h => h.id), ["B", "C", "A"]);
  const roundedTie = [{id: "A", nativeComponent: "A", distance: 1},
    {id: "B", nativeComponent: "B", distance: 1 + 1e-8}];
  assert.deepEqual(impact.vehicleContacts(roundedTie).map(h => h.id), ["B", "A"]);
  assert.deepEqual(tied.map(h => h.id), ["A", "B", "C"]);
  const targetTie = [[1,0,0],[-1,0,0],[0,1,0]];
  assert.deepEqual(impact.targetPoints(targetTie,[0,0,0]).map(t => targetTie.indexOf(t.position)),[1,2,0]);
  const targetRoundedTie = [[1,0,0],[1+1e-8,0,0]];
  assert.deepEqual(impact.targetPoints(targetRoundedTie,[0,0,0]).map(t => targetRoundedTie.indexOf(t.position)),[1,0]);
  assert.deepEqual(targetTie,[[1,0,0],[-1,0,0],[0,1,0]],"Target sorting must preserve supplied point order");
  const gateComponent = {nodeIndex: 0};
  const gateVehicle = {sections: {[MAIN]: {max_health: 1000, pre: [], post: [], simultaneous: []}}, slots: [
    {slot: "CC_MainBody", group: "ComplexSurface.Group.Default", section: MAIN,
      hit_location: "Vehicle.Main", blast_factor: {gate: [1, 1]}}
  ]};
  const gateSource = {id: "gate", base_damage: 100,
    blast: {radius: 2000, effective_radius: 1500, falloff: 1, prefer_upwards: false}};
  function angleShot(sphere, acceptedStart) {
    const geometry = {components: [gateComponent], closestPoint: () => ({distance: 1}),
      ray: start => start.every((v, i) => v === acceptedStart[i])
        ? {position: [10, 0, 0], component: gateComponent, material: {name: "CC_MainBody"}} : null};
    return impact.simulate(geometry, gateVehicle, gateSource, [0, 0, 0], {0: {component: "Fixture:Body",
      point_sampling: {method: "native-bounds", bounds_origin: [10, 0, 0], bounds_sphere_radius: sphere, points: [[10, 0, 0]]}}});
  }
  assert.equal(angleShot(0.1, [0, 0, 0.5]).hits[0].cloudIndex, 2, "Outside sphere accepts the 90-degree start");
  assert.equal(angleShot(0.1, [-0.5, 0, 0]).hits.length, 0, "Outside sphere rejects the opposite hemisphere");
  assert.equal(angleShot(20, [-0.5, 0, 0]).hits[0].cloudIndex, 3, "Inside sphere accepts 180-degree starts");

  const exactTarget = [10+1e-13, 2-1e-13, 3], segmentCalls = [], exactOrigin = [0,0,0];
  const segmentGeometry = {components: [gateComponent], closestPoint: () => ({distance: 1}),
    ray: () => { throw new Error("Segment backend must receive original endpoints"); },
    traceSegment: (start,end) => {
      segmentCalls.push({start: start.slice(), end: end.slice()});
      if (end === exactTarget && start[2] === .5) return {position: exactTarget,component: gateComponent,material: {name: "CC_MainBody"}};
      return null;
    }};
  const exactShot = impact.simulate(segmentGeometry, gateVehicle, gateSource, exactOrigin,
    {0: {component: "Fixture:Body",point_sampling: {method: "native-bounds",bounds_origin: exactTarget,
      bounds_sphere_radius: 20,points: [exactTarget]}}});
  assert.equal(exactShot.hits[0].cloudIndex, 2);
  assert.ok(segmentCalls.some(call => call.start.every((v,i) => v === exactOrigin[i]) && call.end[2] === .5),
    "Origin-to-cloud pretrace uses the segment backend");
  assert.deepEqual(segmentCalls[segmentCalls.length-1].end, exactTarget, "Target coordinates must survive without endpoint reconstruction");
  segmentGeometry.closestPoint = () => { throw new Error("Sphere backend supplies overlap membership"); };
  segmentGeometry.overlapSphere = (origin,radius) => {
    assert.deepEqual(origin,exactOrigin);assert.equal(radius,20);
    return [gateComponent];
  };
  const sphereMetadata = {0: {component: "Fixture:Body",point_sampling: {method: "native-bounds",bounds_origin: exactTarget,
    bounds_sphere_radius: 20,points: [exactTarget]}}};
  assert.equal(impact.simulate(segmentGeometry,gateVehicle,gateSource,exactOrigin,sphereMetadata).hits.length,1);
  segmentGeometry.overlapSphere = () => [];
  const tracedBeforeMiss = segmentCalls.length;
  assert.equal(impact.simulate(segmentGeometry,gateVehicle,gateSource,exactOrigin,sphereMetadata).hits.length,0);
  assert.equal(segmentCalls.length,tracedBeforeMiss,"An empty sphere result must skip contact traces");

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
  const upwards = new Set(["Item.Caliber.120x800mm.Standard", "Item.Caliber.155mm.Expensive",
    "Item.Caliber.155mm.Expensive.Sandbox", "Item.Caliber.155mm.Standard", "Item.Caliber.155mm.Standard.Sandbox",
    "Actor.m67-frag-grenade", "Actor.at-mine", "Actor.claymore", "Actor.molotov"]);
  for (const source of sources) assert.equal(source.blast.prefer_upwards, upwards.has(source.id), `Trace preference: ${source.id}`);
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
  // Frozen native 6F06792–6F06837 results, including float-rounded boundary inputs.
  for (const [cm, expected] of [[0, 100], [100, 100], [399.99, 100], [400, 100],
    [400.01, 99.99832916259766], [500, 83.33332824707031], [700, 50],
    [900, 16.666667938232422], [999.99, 0.0016682943096384406], [1000, 0]])
    assert.equal(impact.blastAmount(source, cm), expected);
  const tiny = {base_damage: 333.3,
    blast: {radius: 2e-9, effective_radius: 1e-9, minimum: 0.01, falloff: 0.1}};
  assert.equal(impact.blastAmount(tiny, 1.5e-9), 333.29998779296875);
  assert.equal(impact.blastAmount(tiny, 2e-9), 0.009999999776482582);
  const before = JSON.stringify(data);
  for (const vehicle of vehicles) {
    for (const base of vehicle.models) for (const model of [base, base.wheels_destroyed].filter(Boolean)) {
      const buffer = fs.readFileSync(path.join(root, model.path));
      const mesh = await geometryAPI.load(buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength), decoder);
      queryIndex.attach(mesh);
      assert.ok(mesh.bounds.min.concat(mesh.bounds.max).every(Number.isFinite));
      const mapping = metadata.models[model.path];
      assert.ok(mapping, model.path);
      const sampling = samplingFixture.models[model.path];
      assert.ok(sampling, `Missing authored sampling fixture: ${model.path}`);
      const expectedSamplingMode = Object.values(sampling.components).some(c => /sockets$/.test(c.method)) ? "native-sockets" : "native-bounds";
      for (const component of mesh.components) {
        assert.ok(mapping[component.nodeIndex]?.component, `Missing component: ${model.path}:${component.nodeIndex}`);
        if (sampling) assert.ok(mapping[component.nodeIndex].point_sampling, `Missing authored sampling: ${model.path}`);
      }
      models++; nodes += mesh.components.length; triangles += mesh.triangles.length;
      const points = placements(mesh);
      const row = {vehicle: vehicle.id, model: model.path, sources: sources.length,
        surfacePlacements: points.filter(p => p.kind.startsWith("surface")).length,
        groundPlacements: 2, samplingMode: expectedSamplingMode, shots: 0, damagingShots: 0};
      assert.ok(row.surfacePlacements > 0, `No surface placement: ${model.path}`);
      for (const explosive of sources) {
        for (const placement of points) {
          const result = impact.simulate(mesh, vehicle, explosive, placement.point, mapping);
          assert.equal(result.samplingMode, expectedSamplingMode, `Sampling fallback changed: ${model.path}`);
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
      if (vehicle.id === "land-tracked-tnk-04-default") {
        assert.equal(Object.values(mapping).reduce((sum, node) => sum + node.point_sampling.points.length, 0), 147);
        const partial = {...mapping};
        const firstIndex = mesh.components[0].nodeIndex;
        partial[firstIndex] = {...partial[firstIndex]};
        delete partial[firstIndex].point_sampling;
        assert.throws(() => impact.simulate(mesh, vehicle, source, mesh.bounds.center, partial),
          /Incomplete authored component sampling inputs/);
        assert.throws(() => impact.simulate(mesh, vehicle, source, mesh.bounds.center, {}),
          /Incomplete authored component sampling inputs/);
      }
      if (vehicle.damage_row.endsWith(".TNK_01.AntiAir")) {
        assert.equal(Object.values(mapping).reduce((sum, node) => sum + node.point_sampling.points.length, 0), 89);
        const front = mesh.ray([0, 1, 8], [0, 0, -1]);
        assert.ok(front && front.material.name === "CC_MainBody");
        const result = impact.simulate(mesh, vehicle, source, front.position, mapping);
        assert.equal(result.samplingMode, "native-sockets");
        assert.equal(result.hits.length, 5, "Retain exposed component contacts for inspection");
        assert.equal(result.applications.length, 1, "Main-hit contacts must not multiply blast damage");
        assert.equal(result.mainDamage, 267.9000244140625);
        const fuel = MAIN + ".FuelTank";
        assert.equal(result.sectionDamage[fuel], 14.100006103515625);
        assert.ok(result.hits.every(hit => hit.material.name !== "CC_FuelTank"), "Fuel surface must stay occluded");
        const fuelTransfer = result.transfers.filter(entry => entry.section === fuel);
        assert.ok(fuelTransfer.every(entry => entry.via && entry.via.section === MAIN));
        assert.equal(fuelTransfer.reduce((sum, entry) => sum + entry.amount, 0), 14.100006103515625);
        const backed = impact.simulate(mesh, vehicle, source,
          impact.detonationOrigin(source, front.position, [0, 0, -1]), mapping);
        // Global sorting retains the nearest first hit; swap removal can retain a farther later component.
        assert.ok(backed.hits.find(hit => hit.nativeComponent.endsWith(":MainBody")).distance < 11);
        const spinDistance = backed.hits.find(hit => hit.nativeComponent.endsWith(":TurretSpin")).distance;
        assert.ok(spinDistance > 280 && spinDistance < 285, "Preserve native swap-filter ordering");
        assert.equal(backed.mainDamage, 267.9000244140625);
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
          assert.equal(hit.amount, Math.fround(hit.amount));
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
