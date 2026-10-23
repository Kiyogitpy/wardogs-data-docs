/* Offline check for the spray viewer: its cumulative path must equal every weapon's expectedPath in
   assets/data/spray-patterns.json (within 1e-3 (the file stores 5 decimals; paths accumulate rounding)), and the helpers must behave. Run: node _tools/spray_viewer_check.js */
"use strict";
const fs = require("fs");
const path = require("path");
const assert = require("assert/strict");
const root = path.join(__dirname, "..");
const core = require(path.join(root, "assets/js/spray-viewer.js"));
const data = JSON.parse(fs.readFileSync(path.join(root, "assets/data/spray-patterns.json"), "utf8"));
assert.ok(Array.isArray(data.weapons) && data.weapons.length > 0, "no weapons");
let seasons = 0, shots = 0;
const bad = [];
for (const w of data.weapons) {
  assert.ok(w.name && !/^(WEPN_|DA_|ID_)/.test(w.name), "code name shown as weapon name: " + w.id);
  for (const k of ["s1", "s2"]) {
    const s = w.seasons[k];
    if (!s || s.present === false) continue;
    const got = core.cumulativePath(s);
    assert.equal(got.length, s.expectedPath.length, w.id + " " + k + " length");
    got.forEach((p, i) => {
      const e = s.expectedPath[i];
      if (e.shot !== p.shot || Math.abs(e.x - p.x) > 1e-3 || Math.abs(e.y - p.y) > 1e-3) bad.push(w.id + " " + k + " shot " + (i + 1));
    });
    if (s.band) assert.ok(s.band.p10.length === s.band.p90.length && s.band.p10.length >= 1, w.id + " band");
    shots += got.length; seasons++;
  }
}
assert.deepEqual(bad, [], "cumulative path differs from expectedPath: " + bad.slice(0, 5).join("; "));
// helpers
const s = {
  pattern: [{ x: 1, y: 2 }, { x: -1, y: 1 }], postPattern: { yaw: [-1, 3], pitch: [0, 2] },
  multipliers: { horizontal: 2, vertical: 0.5, stance: { stand: 1, crouch: 0.5, prone: 0.25 } },
  focusReductionPct: 20, viewKickMagnitudeMultiplier: 1
};
const p = core.cumulativePath(s, 4);
assert.deepEqual(p.map(q => [q.x, q.y]), [[1, 2], [0, 3], [1, 4], [2, 5]]);
assert.deepEqual(core.factors(s, { stance: "crouch", focus: true, attachments: true }), { x: 0.5 * 0.8 * 2, y: 0.5 * 0.8 * 0.5 });
assert.deepEqual(core.factors(s, {}), { x: 1, y: 1 });
assert.ok(Math.abs(core.targetOffset(1, 100) - 100 * Math.tan(Math.PI / 180)) < 1e-12);
assert.ok(Math.abs(core.degForOffset(core.targetOffset(2.5, 80), 80) - 2.5) < 1e-9);
assert.equal(core.climbAfter(p, 3), 4);
console.log(`spray viewer: ${data.weapons.length} weapons, ${seasons} seasons, ${shots} shots match expectedPath`);
