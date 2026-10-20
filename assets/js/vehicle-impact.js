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
  function finiteVector(value) { return Array.isArray(value) && value.length === 3 && value.every(Number.isFinite); }
  function detonationOrigin(caliber, position, incoming) {
    if (!finiteVector(position) || !finiteVector(incoming)) throw new Error("Invalid projectile impact direction.");
    var length = Math.hypot.apply(Math, incoming), backoff = caliber.blast && caliber.blast.impact_backoff_cm;
    if (!(length > 1e-6) || !(backoff > 0)) return position.slice();
    return sub(position, mul(incoming, backoff / 100 / length));
  }
  function angleRejected(origin, start, boundsOrigin, threshold) {
    var a = sub(boundsOrigin, origin), b = sub(start, origin);
    var magnitude = Math.hypot.apply(Math, a) * Math.hypot.apply(Math, b);
    var dot = magnitude > 0 ? a.reduce(function (sum, value, i) { return sum + value * b[i]; }, 0) / magnitude : 0;
    return Math.acos(Math.max(-1, Math.min(1, dot))) * 180 / Math.PI > threshold;
  }
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

  // Models without authored sampling metadata use this display-surface approximation.
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
    var supplied = geometry.components.filter(function (component) {
      return metadata && metadata[String(component.nodeIndex)] && metadata[String(component.nodeIndex)].point_sampling;
    });
    var authored = supplied.length > 0, hasSockets = supplied.some(function (component) {
      return metadata[String(component.nodeIndex)].point_sampling.method === "native-sockets";
    });
    if (authored && supplied.length !== geometry.components.length)
      throw new Error("Incomplete authored component sampling inputs.");
    var tested = new Set(), blocked = new Set();
    geometry.components.forEach(function (component) {
      var mapped = metadata && metadata[String(component.nodeIndex)];
      if (!mapped || !mapped.component) { incomplete++; return; }
      if (retained.has(mapped.component)) return;
      var closest = geometry.closestPoint(origin, component);
      if (!closest || closest.distance > radius + 1e-7) return;
      var sampling = mapped.point_sampling;
      if (authored && (["native-bounds", "native-sockets"].indexOf(sampling.method) < 0 ||
          !Array.isArray(sampling.points) || !sampling.points.length ||
          !finiteVector(sampling.bounds_origin) || !sampling.points.every(finiteVector) ||
          !Number.isFinite(sampling.angle_degrees))) throw new Error("Invalid authored component sampling inputs.");
      var found = null, targets = authored ? sampling.points.map(function (point) { return {position: point}; }).sort(function (a, b) {
        return distance(origin, a.position) - distance(origin, b.position);
      })
        : candidates(geometry, component, origin);
      for (var t = 0; t < targets.length && (!found || authored); t++) {
        if (authored && distance(origin, targets[t].position) > radius + 1) continue;
        var accepted = null;
        for (var s = 0; s < starts.length && !accepted; s++) {
          var start = starts[s], target = targets[t], delta = sub(target.position, start), length = Math.hypot.apply(Math, delta);
          if (authored && s >= 2 && angleRejected(origin, start, sampling.bounds_origin, sampling.angle_degrees)) continue;
          // Native 0x6F0341D exempts cloud index 1 from the origin-to-start pretrace.
          if (authored) {
            // Tested-clear starts still run each component callback; only the pretrace is cached.
            if (s !== 1 && !tested.has(s)) {
              tested.add(s);
              var pretraceLength = distance(origin, start);
              if (pretraceLength > 0 && geometry.ray(origin, sub(start, origin), pretraceLength)) blocked.add(s);
            }
            if (blocked.has(s)) continue;
          } else if (s !== 1 && distance(origin, start) > 1e-7 && !clearSegment(geometry, origin, start)) continue;
          if (length < 1e-7) { if (!authored) accepted = target; continue; }
          // Authored traces retain their exact starts; moving inside a surface can bypass the hull.
          var direction = mul(delta, 1 / length), epsilon = Math.min(1e-5, length / 100);
          var trace = authored ? geometry.ray(start, direction, length)
            : geometry.ray(add(start, mul(direction, epsilon)), direction, length + epsilon);
          if (trace && trace.component === component && distance(origin, trace.position) <= radius + 1e-7) accepted = trace;
        }
        // Reviewed native vehicle families continue through candidates and retain the nearest hit.
        if (accepted && (!found || distance(origin, accepted.position) < distance(origin, found.position))) found = accepted;
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
      samplingMode: authored ? (hasSockets ? "native-sockets" : "native-bounds") : "sampled-surfaces",
      baseAmount: applications.reduce(function (sum, hit) { return sum + hit.base; }, 0),
      orderingNote: authored
        ? "Reference-pose estimate: authored component sampling points, native angle gate and trace-cloud cache; visibility uses display geometry and GLB component order. Live collision bodies, terrain and query order can change the result."
        : "Reference-pose estimate: sampled display surfaces and GLB component order; live collision bodies, terrain and query order can change the result."};
  }
  return {simulate: simulate, detonationOrigin: detonationOrigin, blastAmount: blastAmount, applyRadial: applyRadial,
    freshHealth: freshHealth, slotOf: slotOf, cloud: cloud, damageApplications: damageApplications};
}));
