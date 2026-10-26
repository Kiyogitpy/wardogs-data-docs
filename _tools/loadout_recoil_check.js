/* Offline check for the Loadout Builder recoil panel's model (assets/js/loadout-recoil.js).
   AK74M Season 2, standing default loadout (vertical = horizontal = 1): 30 shots climb 35.705 degrees (round 81).
   Run: node _tools/loadout_recoil_check.js */
"use strict";
const fs = require("fs");
const path = require("path");
const assert = require("assert/strict");
const root = path.join(__dirname, "..");
const R = require(path.join(root, "assets/js/loadout-recoil.js"));
const SV = require(path.join(root, "assets/js/spray-viewer.js"));
const data = JSON.parse(fs.readFileSync(path.join(root, "assets/data/spray-patterns.json"), "utf8"));
const near = (a, b, e, m) => assert.ok(Math.abs(a - b) <= e, `${m}: ${a} vs ${b}`);

const f = R.findSeason(data, "ID_AK74M");
assert.ok(f, "AK74M s2 found");
const s = f.season;
const base = { vertical: 1, horizontal: 1, stance: "Stand", focus: false };
const p = R.path(s, base, 30);
near(p[29].y, 35.705, 0.01, "AK74M 30-shot climb");
// same as the spray viewer's cumulative path times the view kick magnitude
near(p[29].y, SV.cumulativePath(s, 30)[29].y * s.viewKickMagnitudeMultiplier, 1e-9, "matches spray viewer core");
// stance is only a label: the data's crouch/prone ratios must not be applied again
const crouch = R.path(s, { vertical: 1, horizontal: 1, stance: "Crouch", focus: false }, 30);
near(crouch[29].y, p[29].y, 1e-12, "stance not applied twice");
// the final multipliers scale linearly
const v = R.path(s, { vertical: 0.85, horizontal: 0.5, stance: "Crouch" }, 30);
near(v[29].y, p[29].y * 0.85, 1e-9, "vertical multiplier");
near(v[29].x, p[29].x * 0.5, 1e-9, "horizontal multiplier");
// default-loadout multipliers from the data are not applied either
const sm = JSON.parse(JSON.stringify(s)); sm.multipliers.vertical = 0.3; sm.multipliers.horizontal = 0.3;
near(R.path(sm, base, 30)[29].y, p[29].y, 1e-12, "data default multipliers ignored");
// focus cut
near(R.path(s, { vertical: 1, horizontal: 1, focus: true }, 30)[29].y, p[29].y * (1 - s.focusReductionPct / 100), 1e-9, "focus cut");
// band scaled, sample statistics
const b = R.band(s, base, 30);
near(b.p10[29].y, s.band.p10[29].y * s.viewKickMagnitudeMultiplier, 1e-9, "band scale");
let seed = 12345; const rnd = () => (seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296;
let sum = 0; const N = 4000;
for (let i = 0; i < N; i++) sum += R.sample(s, base, 30, rnd)[29].y;
near(sum / N, p[29].y, 0.5, "mean of sampled magazines (the rotation shrinks the mean slightly, ~1%)");
// distance conversion: 1 degree at 100 m
near(R.offsetM(1, 100), 1.7455, 1e-3, "offset");
assert.equal(R.findSeason(data, "ID_Nope"), null);
console.log(`loadout recoil: AK74M 30 shots climb ${p[29].y.toFixed(3)} deg, drift ${p[29].x.toFixed(3)} deg; crouch label unchanged; sample mean ${(sum / N).toFixed(2)}`);
