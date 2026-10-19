/* Reference-pose explosion preview. Native damage arithmetic; sampled display geometry, not live physics. */
(function (root, factory) {
  "use strict";
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.VehicleImpact = api;
}(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  var MAIN = "Attribute.Gameplay.Health", GROUP = "ComplexSurface.Group.";
  function sub(a, b) { return a.map(function (v, i) { return v - b[i]; }); }
  function add(a, b) { return a.map(function (v, i) { return v + b[i]; }); }
  function mul(a, k) { return a.map(function (v) { return v * k; }); }
  function distance(a, b) { return Math.hypot.apply(Math, sub(a, b)); }
  function clearSegment(geometry, start, end) {
    var delta = sub(end, start), length = Math.hypot.apply(Math, delta);
    if (length < 2e-5) return true;
    return !geometry.ray(add(start, mul(delta, 1e-5 / length)), delta, length - 2e-5);
  }

  function blastAmount(caliber, centimetres) {
    var b = caliber.blast || {}, r = b.radius || 0, e = b.effective_radius || 0;
    var base = caliber.base_damage || 0, amount;
    if (centimetres <= e) amount = base;
    else if (centimetres >= r) amount = 0;
    else {
      var t = Math.abs(e - r) <= 1e-8 ? (centimetres >= e ? 1 : 0)
        : Math.max(0, Math.min(1, (centimetres - r) / (e - r)));
      amount = base * (1 - (b.falloff || 0) + (b.falloff || 0) * t);
    }
    return Math.max(amount, b.minimum || 0);
  }

  // Match the existing slot resolver's exact-group, default-slot and parent-group walk.
  function slotOf(vehicle, material) {
    var parts = material.name.split("|"), slot = parts[0], group = GROUP + (parts[1] || "Default");
    while (group.indexOf(GROUP) === 0) {
      var exact = vehicle.slots.findIndex(function (s) { return s.group === group && s.slot === slot; });
      if (exact >= 0) return exact;
      var fallback = vehicle.slots.findIndex(function (s) { return s.group === group && s.slot === "(default)"; });
      if (fallback >= 0) return fallback;
      group = group.slice(0, group.lastIndexOf("."));
    }
    return -1;
  }

  function freshHealth(vehicle) {
    var health = {};
    Object.keys(vehicle.sections).forEach(function (key) { health[key] = vehicle.sections[key].max_health; });
    return health;
  }

  // Radial event routing differs from the viewer's point-hit inspection calculation.
  function applyRadial(sections, health, key, amount, depth, transfers, via) {
    var section = sections[key];
    if (!section || !(amount > 0) || (depth || 0) > 10) return 0;
    var handled = 0, skips = section.radial_routing_skips || {};
    function reroute(routes, phase) {
      (routes || []).forEach(function (route) {
        if ((health[key] <= 0) === !!route[2] && amount > handled) {
          handled += applyRadial(sections, health, route[0],
            (amount - handled) * Math.max(0, Math.min(1, route[1])), (depth || 0) + 1,
            transfers, {section: key, phase: phase});
        }
      });
    }
    if (!skips.pre) reroute(section.pre, "pre");
    var own = Math.min(Math.max(amount - handled, 0), Math.max(health[key], 0));
    health[key] -= own;
    handled += own;
    if (transfers && own > 0) transfers.push({section: key, amount: own, via: via || null});
    if (key === MAIN && health[key] <= 0) return handled;
    if (!skips.simultaneous) (section.simultaneous || []).forEach(function (route) {
      if (!route[2] || health[key] <= 0)
        applyRadial(sections, health, route[0], own * Math.max(0, Math.min(1, route[1])), (depth || 0) + 1,
          transfers, {section: key, phase: "simultaneous"});
    });
    if (!skips.post) reroute(section.post, "post");
    return handled;
  }

  // Native 0x6F06B10–13 skips a previously processed nonempty vehicle hit-location tag.
  // This preview contains one target actor; contact collection and damage application are separate.
  function damageApplications(vehicle, contacts) {
    var seen = new Set();
    return contacts.filter(function (hit) {
      var slot = vehicle.slots[hit.slotIndex], tag = slot && slot.hit_location;
      hit.hitLocation = tag || null;
      hit.suppressed = !!tag && seen.has(tag);
      if (tag) seen.add(tag);
      return !hit.suppressed;
    });
  }

  // Native cloud order, converted UE (X,Y,Z) -> displayed (-Y,Z,X), metres.
  function cloud(origin, preferUpwards) {
    var d = [[0, 0, 1], [1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, -1], [-1, 0, 0]];
    [[1, 1, 1], [1, -1, 1], [1, 1, -1], [1, -1, -1],
      [-1, 1, 1], [-1, -1, 1], [-1, 1, -1], [-1, -1, -1]].forEach(function (v) {
      d.push(mul(v, 1 / Math.sqrt(3)));
    });
    var starts = [origin].concat(d.map(function (v) { return add(origin, mul([-v[1], v[2], v[0]], 0.5)); }));
    if (preferUpwards) { var first = starts[0]; starts[0] = starts[1]; starts[1] = first; }
    return starts;
  }

  // The live game samples loaded collision bodies. Here candidate targets are sampled
  // from the published triangle surface and its bounds; the UI labels this approximation.
  function candidates(geometry, component, origin) {
    var b = component.bounds, middle = b.min.map(function (v, i) { return (v + b.max[i]) / 2; });
    var points = [origin, middle];
    [0, 1].forEach(function (x) { [0, 1].forEach(function (y) { [0, 1].forEach(function (z) {
      points.push([b[x ? "max" : "min"][0], b[y ? "max" : "min"][1], b[z ? "max" : "min"][2]]);
    }); }); });
    var seen = new Set();
    return points.map(function (p) { return geometry.closestPoint(p, component); }).filter(function (hit) {
      if (!hit) return false;
      var key = hit.position.map(function (v) { return v.toFixed(6); }).join(",");
      if (seen.has(key)) return false;
      seen.add(key); return true;
    }).sort(function (a, b) { return distance(a.position, origin) - distance(b.position, origin); });
  }

  function simulate(geometry, vehicle, caliber, origin, metadata) {
    if (!caliber.blast || !(caliber.blast.radius > 0)) throw new Error("Choose an explosive projectile.");
    if (!Array.isArray(origin) || origin.length !== 3 || !origin.every(Number.isFinite)) throw new Error("Invalid impact position.");
    var radius = caliber.blast.radius / 100, hits = [], occluded = 0, retained = new Set();
    var starts = cloud(origin, caliber.blast.prefer_upwards === true), incomplete = 0;
    geometry.components.forEach(function (component) {
      var mapped = metadata && metadata[String(component.nodeIndex)];
      if (!mapped || !mapped.component) { incomplete++; return; }
      if (retained.has(mapped.component)) return;
      var closest = geometry.closestPoint(origin, component);
      if (!closest || closest.distance > radius + 1e-7) return;
      var found = null, targets = candidates(geometry, component, origin);
      for (var t = 0; t < targets.length && !found; t++) {
        for (var s = 0; s < starts.length && !found; s++) {
          var start = starts[s], target = targets[t], delta = sub(target.position, start), length = Math.hypot.apply(Math, delta);
          // Native 0x6F0341D exempts cloud index 1 from the origin-to-start pretrace.
          if (s !== 1 && distance(origin, start) > 1e-7 && !clearSegment(geometry, origin, start)) continue;
          if (length < 1e-7) { found = target; break; }
          // Step inward from the trace start by a numerical epsilon, never add it to damage distance.
          var direction = mul(delta, 1 / length), epsilon = Math.min(1e-5, length / 100);
          var trace = geometry.ray(add(start, mul(direction, epsilon)), direction, length + epsilon);
          if (trace && trace.component === component && distance(origin, trace.position) <= radius + 1e-7) found = trace;
        }
      }
      if (!found) { occluded++; return; }
      retained.add(mapped.component);
      var slotIndex = slotOf(vehicle, found.material), slot = vehicle.slots[slotIndex];
      var cm = distance(origin, found.position) * 100;
      var ring = cm <= (caliber.blast.effective_radius || 0) ? 0 : 1;
      var table = slot && (caliber.source_type === "actor" ? slot.explosion_factor : slot.blast_factor);
      var factors = table && table[caliber.id];
      var factor = factors ? factors[ring] : null;
      hits.push({position: found.position, component: component, material: found.material,
        nativeComponent: mapped.component, slotIndex: slotIndex, distance: cm,
        factor: factor, base: blastAmount(caliber, cm), amount: factor === null ? 0 : blastAmount(caliber, cm) * factor});
    });
    var first = hits[0], firstSlot = first && vehicle.slots[first.slotIndex];
    var firstSection = firstSlot ? firstSlot.section : null, health = freshHealth(vehicle);
    var applications = damageApplications(vehicle, hits), transfers = [];
    // Native radial section choice is ComponentHits[0], even for subsequent per-hit rule locations.
    applications.forEach(function (hit) { applyRadial(vehicle.sections, health, firstSection, hit.amount, 0, transfers); });
    var alternatives = Array.from(new Set(hits.map(function (hit) {
      var slot = vehicle.slots[hit.slotIndex]; return slot ? slot.section : null;
    })));
    var damage = {};
    Object.keys(health).forEach(function (key) { damage[key] = vehicle.sections[key].max_health - health[key]; });
    var scenarios = hits.map(function (first, index) {
      var slot = vehicle.slots[first.slotIndex], next = freshHealth(vehicle);
      var sequence = [first].concat(hits.filter(function (_, i) { return i !== index; }));
      damageApplications(vehicle, sequence.map(function (hit) { return Object.assign({}, hit); })).forEach(function (hit) {
        applyRadial(vehicle.sections, next, slot ? slot.section : null, hit.amount);
      });
      return (vehicle.sections[MAIN] ? vehicle.sections[MAIN].max_health : 0) - (next[MAIN] || 0);
    });
    return {hits: hits, applications: applications, transfers: transfers, occluded: occluded, incomplete: incomplete,
      health: health, sectionDamage: damage,
      firstSection: firstSection, firstSectionAlternatives: alternatives, orderSensitive: alternatives.length > 1,
      mainDamage: damage[MAIN] || 0, mainRemaining: health[MAIN] || 0,
      scenarioMainDamage: {min: scenarios.length ? Math.min.apply(Math, scenarios) : 0,
        max: scenarios.length ? Math.max.apply(Math, scenarios) : 0},
      tracePreferenceUnknown: caliber.blast.prefer_upwards == null,
      baseAmount: applications.reduce(function (sum, hit) { return sum + hit.base; }, 0),
      orderingNote: "Reference-pose estimate: sampled display surfaces and GLB component order; live collision bodies, terrain and query order can change the result."};
  }
  return {simulate: simulate, blastAmount: blastAmount, applyRadial: applyRadial,
    freshHealth: freshHealth, slotOf: slotOf, cloud: cloud, damageApplications: damageApplications};
}));
