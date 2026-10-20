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

  // Native actor-hit sort precedes the vehicle's swap-removal of repeated components.
  function vehicleContacts(contacts) {
    var hits = contacts.slice().sort(function (a, b) { return Math.fround(a.distance) - Math.fround(b.distance); });
    var seen = new Set(), index = 0;
    while (index < hits.length) {
      var hit = hits[index];
      if (seen.has(hit.nativeComponent)) {
        hits[index] = hits[hits.length - 1];
        hits.pop();
      } else {
        seen.add(hit.nativeComponent);
        index++;
      }
    }
    return hits;
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

  function simulate(geometry, vehicle, caliber, origin, metadata) {
    if (!caliber.blast || !(caliber.blast.radius > 0)) throw new Error("Choose an explosive projectile.");
    if (!Array.isArray(origin) || origin.length !== 3 || !origin.every(Number.isFinite)) throw new Error("Invalid impact position.");
    var radius = caliber.blast.radius / 100, hits = [], eligible = new Set();
    var starts = cloud(origin, caliber.blast.prefer_upwards === true), incomplete = 0;
    var supplied = geometry.components.filter(function (component) {
      return metadata && metadata[String(component.nodeIndex)] && metadata[String(component.nodeIndex)].point_sampling;
    });
    var hasSockets = supplied.some(function (component) {
      return /sockets$/.test(metadata[String(component.nodeIndex)].point_sampling.method);
    });
    if (!supplied.length || supplied.length !== geometry.components.length)
      throw new Error("Incomplete authored component sampling inputs.");
    var tested = new Set(), blocked = new Set();
    geometry.components.forEach(function (component) {
      var mapped = metadata && metadata[String(component.nodeIndex)];
      if (!mapped || !mapped.component) { incomplete++; return; }
      var closest = geometry.closestPoint(origin, component);
      if (!closest || closest.distance > radius + 1e-7) return;
      eligible.add(mapped.component);
      var sampling = mapped.point_sampling;
      if (["native-bounds", "native-sockets", "native-instance-bounds", "native-instance-sockets"].indexOf(sampling.method) < 0 ||
          !Array.isArray(sampling.points) || !sampling.points.length ||
          !finiteVector(sampling.bounds_origin) || !sampling.points.every(finiteVector) ||
          !Number.isFinite(sampling.bounds_sphere_radius) || sampling.bounds_sphere_radius < 0)
        throw new Error("Invalid authored component sampling inputs.");
      var angle = distance(origin, sampling.bounds_origin) <= sampling.bounds_sphere_radius + 1e-6 ? 180 : 90;
      var targets = sampling.points.map(function (point) { return {position: point}; }).sort(function (a, b) {
        return distance(origin, a.position) - distance(origin, b.position);
      });
      for (var t = 0; t < targets.length; t++) {
        if (distance(origin, targets[t].position) > radius + 1) continue;
        var accepted = null;
        for (var s = 0; s < starts.length && !accepted; s++) {
          var start = starts[s], target = targets[t], delta = sub(target.position, start), length = Math.hypot.apply(Math, delta);
          if (s >= 2 && angleRejected(origin, start, sampling.bounds_origin, angle)) continue;
          // Native 0x6F0341D exempts cloud index 1 from the origin-to-start pretrace.
          // Tested-clear starts still run each component callback; only the pretrace is cached.
          if (s !== 1 && !tested.has(s)) {
            tested.add(s);
            var pretraceLength = distance(origin, start);
            if (pretraceLength > 0 && geometry.ray(origin, sub(start, origin), pretraceLength)) blocked.add(s);
          }
          if (blocked.has(s) || length < 1e-7) continue;
          // Authored traces retain their exact starts; moving inside a surface can bypass the hull.
          var direction = mul(delta, 1 / length), trace = geometry.ray(start, direction, length);
          if (trace && trace.component === component && distance(origin, trace.position) <= radius + 1e-7)
            accepted = Object.assign({}, trace, {traceStart: start.slice(), cloudIndex: s});
        }
        if (!accepted) continue;
        var slotIndex = slotOf(vehicle, accepted.material), slot = vehicle.slots[slotIndex];
        var cm = Math.fround(distance(origin, accepted.position) * 100);
        var ring = cm <= (caliber.blast.effective_radius || 0) ? 0 : 1;
        var table = slot && (caliber.source_type === "actor" ? slot.explosion_factor : slot.blast_factor);
        var factors = table && table[caliber.id];
        var factor = factors ? factors[ring] : null;
        hits.push({position: accepted.position, component: component, material: accepted.material,
          traceStart: accepted.traceStart, cloudIndex: accepted.cloudIndex,
          nativeComponent: mapped.component, slotIndex: slotIndex, distance: cm,
          factor: factor, base: blastAmount(caliber, cm), amount: factor === null ? 0 : blastAmount(caliber, cm) * factor});
      }
    });
    hits = vehicleContacts(hits);
    var occluded = eligible.size - new Set(hits.map(function (hit) { return hit.nativeComponent; })).size;
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
      samplingMode: hasSockets ? "native-sockets" : "native-bounds",
      baseAmount: applications.reduce(function (sum, hit) { return sum + hit.base; }, 0),
      orderingNote: "Reference-pose estimate: authored sampling, native cloud gate/cache, actor-hit distance sorting and component filtering; visibility uses display geometry. Live collision bodies, terrain, active instances and equal-distance ordering can change the result."};
  }
  return {simulate: simulate, detonationOrigin: detonationOrigin, blastAmount: blastAmount, applyRadial: applyRadial,
    freshHealth: freshHealth, slotOf: slotOf, cloud: cloud, damageApplications: damageApplications,
    vehicleContacts: vehicleContacts};
}));
