/* Offline regression checks for the viewer's compact radial-data decoder. */
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert/strict");
const root = path.join(__dirname, "..");
const script = fs.readFileSync(path.join(root, "assets/js/infantry-viewer.js"), "utf8");
const seam = `
  globalThis.decode = function (input) {
    data = input;
    input.hit_locations.forEach(function (z, i) { zoneOrder[z.tag] = i; });
    expand();
    return input;
  };
})();`;
assert.ok(script.trimEnd().endsWith("})();"), "viewer wrapper changed");
const context = { document: { readyState: "loading", addEventListener() {} } };
vm.createContext(context);
vm.runInContext(script.trimEnd().slice(0, -5) + seam, context);
const raw = JSON.parse(fs.readFileSync(path.join(root, "assets/data/infantry-hitboxes.json"), "utf8"));
const decoded = context.decode(structuredClone(raw));
let rings = 0, armor = 0;
raw.sources.forEach((source, i) => {
  const radial = source.values.radial;
  if (!radial) return;
  Object.entries(radial.rings || {}).forEach(([key, ring]) => {
    const actual = decoded.sources[i].values.radial.rings[key];
    const uniform = !radial.zone_multiplier && ring.factor.k != null;
    assert.equal(actual.factor, uniform ? ring.factor.k : "varies by hit location", source.id + " " + key);
    rings++;
    Object.entries(ring.armor || {}).forEach(([item, spec]) => {
      const expected = uniform && spec.k != null ? ring.factor.k * spec.k
        : spec.k != null ? "×" + Number(spec.k.toPrecision(3)) + " with this tag" : "varies by hit location";
      // Uniform rings must expose numeric armor factors rather than raw compact objects.
      if (uniform) assert.equal(actual.factor_with_armor_tag?.[item], expected, source.id + " " + item);
      else assert.ok(actual.factor_with_armor_tag?.[item] != null, source.id + " " + item);
      armor++;
    });
  });
});
assert.ok(rings >= 12 && armor > 0, "radial fixtures missing");
console.log(`radial decoder: ${rings} rings, ${armor} armor factors passed`);
