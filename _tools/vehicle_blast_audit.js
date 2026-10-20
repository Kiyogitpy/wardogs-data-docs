/* Cross-catalog explosion diagnostics. Changing contacts can change total damage with distance. */
"use strict";
const assert = require("node:assert/strict"), fs = require("node:fs"), path = require("node:path"), crypto = require("node:crypto");
const G = require("../assets/js/vehicle-impact-geometry.js"), impact = require("../assets/js/vehicle-impact.js");
const decoder = require("../assets/js/vendor/meshopt_decoder-1.2.0.js"), index = require("./vehicle_query_index.js");
const root = path.join(__dirname, ".."), data = JSON.parse(fs.readFileSync(path.join(root, "assets/data/vehicle-hitboxes.json")));
const metadata = JSON.parse(fs.readFileSync(path.join(root, "assets/data/vehicle-impact-components.json")));
const MAIN = "Attribute.Gameplay.Health";
const inputs = Object.fromEntries(["assets/js/vehicle-impact.js", "assets/js/vehicle-impact-geometry.js",
  "assets/data/vehicle-hitboxes.json", "assets/data/vehicle-impact-components.json", "_tools/vehicle-impact-sampling.json",
  "_tools/vehicle_query_index.js", "_tools/vehicle_blast_audit.js"].map(p =>
  [p, crypto.createHash("sha256").update(fs.readFileSync(path.join(root, p))).digest("hex")]));
function option(name) { const i = process.argv.indexOf(name); return i < 0 ? null : process.argv[i + 1]; }
function near(a, b) { assert.ok(Math.abs(a - b) < 1e-7, `${a} != ${b}`); }
function identity(hit) { return hit && [hit.component.nodeIndex, hit.primitiveIndex, hit.triangle.index]; }
function compare(a, b) {
  assert.deepEqual(identity(a), identity(b), "Indexed query changed the selected triangle");
  if (a) { near(a.distance, b.distance); a.position.forEach((v, i) => near(v, b.position[i])); }
}
function validateIndex(mesh, original) {
  const b = mesh.bounds; let count = 0;
  for (const c of mesh.components) {
    const middle = c.bounds.min.map((v, i) => (v + c.bounds.max[i]) / 2);
    compare(original.closestPoint(middle, c), mesh.closestPoint(middle, c)); count++;
  }
  for (let i = 0; i < 20; i++) {
    const p = b.center.map((v, axis) => v + (Math.sin(i * 7.37 + axis * 2.13) * 1.5) * (b.max[axis] - b.min[axis] + 1));
    compare(original.closestPoint(p), mesh.closestPoint(p));
    const direction = G.sub(b.center, p);
    for (const limit of [Infinity, G.length(direction) / 2]) compare(original.ray(p, direction, limit), mesh.ray(p, direction, limit));
    count += 3;
  }
  return count;
}
function checkShot(vehicle, source, result) {
  assert.equal(result.incomplete, 0);
  const tags = result.applications.map(h => h.hitLocation).filter(Boolean);
  assert.equal(tags.length, new Set(tags).size);
  for (const hit of result.hits) {
    assert.ok(Number.isFinite(hit.factor) && hit.slotIndex >= 0);
    near(hit.amount, hit.base * hit.factor);
    near(hit.base, impact.blastAmount(source, hit.distance));
  }
  for (const [key, section] of Object.entries(vehicle.sections)) {
    assert.ok(result.health[key] >= 0 && result.health[key] <= section.max_health);
    near(result.sectionDamage[key], result.transfers.filter(t => t.section === key).reduce((s, t) => s + t.amount, 0));
  }
}
function snapshot(result, vehicle) {
  const health = impact.freshHealth(vehicle), routingPhases = [];
  for (const hit of result.applications) {
    const transfers = [];
    impact.applyRadial(vehicle.sections, health, result.firstSection, hit.amount, 0, transfers);
    routingPhases.push([...new Set(transfers.map(t => t.via ? t.via.phase + ":" + t.section : "own:" + t.section))]);
  }
  return {mainDamage: result.mainDamage, firstSection: result.firstSection, contacts: result.hits.length,
    applications: result.applications.map(h => ({tag: h.hitLocation, nativeComponent: h.nativeComponent,
      material: h.material.name, distance: h.distance, base: h.base, factor: h.factor, amount: h.amount})),
    samplingMode: result.samplingMode, health: result.health, routingPhases};
}
function scalarCheck(source) {
  const {radius: r, effective_radius: e = 0, falloff: f = 0, minimum: m = 0} = source.blast;
  const distances = [...new Set([0, e, e + 0.001, r / 4, r / 2, r * 3 / 4, r - 0.001, r])].filter(d => d >= 0).sort((a, b) => a - b);
  const samples = distances.map(cm => ({cm, amount: impact.blastAmount(source, cm)}));
  // Independent piecewise linear reference, including nonzero slope endpoints and floors.
  for (const {cm, amount} of samples) {
    let expected = cm <= e ? source.base_damage : cm >= r ? 0
      : source.base_damage * (1 - f * ((cm - e) / (r - e)));
    near(amount, Math.max(expected, m));
  }
  if (r >= e && f >= 0 && f <= 1) for (let i = 1; i < samples.length; i++) assert.ok(samples[i].amount <= samples[i - 1].amount + 1e-7);
  return {id: source.id, blast: source.blast, samples};
}
function explainIncrease(nearer, farther) {
  const reasons = [], before = nearer.applications, after = farther.applications;
  if (nearer.firstSection !== farther.firstSection) reasons.push("first-section-changed");
  const key = h => h.tag || h.nativeComponent;
  const previous = new Map(before.map(h => [key(h), h]));
  if (after.some(h => !previous.has(key(h)))) reasons.push("additional-hit-location");
  if (before.some(h => !after.some(n => key(n) === key(h)))) reasons.push("lost-hit-location");
  if (after.some(h => previous.has(key(h)) && h.factor > previous.get(key(h)).factor + 1e-7)) reasons.push("higher-rule-factor");
  if (after.some(h => previous.has(key(h)) && h.base > previous.get(key(h)).base + 1e-7)) reasons.push("nearer-accepted-contact");
  if (JSON.stringify(nearer.routingPhases) !== JSON.stringify(farther.routingPhases)) reasons.push("routing-phases-changed");
  // If all routed inputs are identical/decreasing, an increased output needs investigation.
  if (!reasons.length) reasons.push("unexplained-routing-or-contact-change");
  return reasons;
}
async function main() {
  assert.ok(option("--report"), "--report requires a new output path");
  let sources = data.meta.calibers.filter(c => c.blast).concat(data.meta.explosives);
  if (option("--source")) sources = sources.filter(s => s.id === option("--source"));
  assert.ok(sources.length);
  const scalars = sources.map(scalarCheck), rows = [], increases = [], excluded = [];
  let shots = 0, indexChecks = 0, models = 0;
  const vehicles = data.vehicles.filter(v => !option("--vehicle-prefix") || v.id.startsWith(option("--vehicle-prefix")));
  for (const vehicle of vehicles) {
    if (!vehicle.models.length) { excluded.push({vehicle: vehicle.id, reason: "No published collision geometry"}); continue; }
    for (const base of vehicle.models) for (const model of [base, base.wheels_destroyed].filter(Boolean)) {
      const buffer = fs.readFileSync(path.join(root, model.path));
      const mesh = await G.load(buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength), decoder);
      indexChecks += validateIndex(mesh, index.attach(mesh)); models++;
      const mapping = metadata.models[model.path], row = {vehicle: vehicle.id, model: model.path, shots: 0,
        strongerSplashPairs: 0, moreDamageOutward: 0, samplingMode: null, sources: []};
      for (const source of sources) {
        const sourceRow = {id: source.id, shots: 0, rays: [], strongerSplashPairs: 0, moreDamageOutward: 0};
        // Four sides at two heights: rear/front and left/right, including low engine/track contact.
        for (const axis of [0, 2]) for (const sign of [-1, 1]) for (const height of [0.25, 0.6]) {
          const start = mesh.bounds.center.slice(), direction = [0, 0, 0];
          start[1] = mesh.bounds.min[1] + height * (mesh.bounds.max[1] - mesh.bounds.min[1]);
          start[axis] = (sign < 0 ? mesh.bounds.min[axis] : mesh.bounds.max[axis]) + sign * 2;
          direction[axis] = -sign;
          const surface = mesh.ray(start, direction);
          if (!surface) continue;
          const detonation = impact.detonationOrigin(source, surface.position, direction);
          const direct = impact.simulate(mesh, vehicle, source, detonation, mapping);
          checkShot(vehicle, source, direct); shots++; row.shots++; sourceRow.shots++;
          row.samplingMode = direct.samplingMode;
          const ray = {axis, sign, height, impact: surface.position, detonation, direct: snapshot(direct, vehicle), splash: []};
          const e = (source.blast.effective_radius || 0) / 100, r = source.blast.radius / 100;
          const offsets = [...new Set([0.25, Math.max(0.25, e), (Math.max(0, Math.min(e, r)) + r) / 2, r + 1])].sort((a, b) => a - b);
          let previous = null;
          for (const offset of offsets) {
            const origin = surface.position.slice(); origin[1] = mesh.bounds.min[1]; origin[axis] += sign * offset;
            const result = impact.simulate(mesh, vehicle, source, origin, mapping);
            checkShot(vehicle, source, result); shots++; row.shots++; sourceRow.shots++;
            const sample = {offset, origin, result: snapshot(result, vehicle)};
            ray.splash.push(sample);
            if (result.mainDamage > direct.mainDamage + 1e-7) { sourceRow.strongerSplashPairs++; row.strongerSplashPairs++; }
            if (previous && result.mainDamage > previous.result.mainDamage + 1e-7) {
              sourceRow.moreDamageOutward++; row.moreDamageOutward++;
              increases.push({vehicle: vehicle.id, model: model.path, source: source.id, axis, sign, height,
                reasons: explainIncrease(previous.result, sample.result), nearer: previous, farther: sample});
            }
            previous = sample;
          }
          sourceRow.rays.push(ray);
        }
        row.sources.push(sourceRow);
      }
      rows.push(row);
      console.log(`${model.path}: ${row.shots} shots, ${row.strongerSplashPairs} stronger splash pairs, ${row.moreDamageOutward} outward increases`);
    }
  }
  const report = {scope: "Offline reference-pose contact/routing diagnostics; no live collision parity established",
    inputs, models, sources: sources.length, shots, indexChecks, scalars, excluded, rows, increases};
  fs.writeFileSync(option("--report"), JSON.stringify(report, null, 2) + "\n", {flag: "wx"});
  console.log(JSON.stringify({models, sources: sources.length, shots, indexChecks, outwardIncreases: increases.length, excluded}));
}
main().catch(e => {console.error(e); process.exitCode = 1;});
