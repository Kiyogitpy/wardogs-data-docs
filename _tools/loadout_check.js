/* Node runner for `python -I _tools/weapon_attributes.py --check`: reads {json, cases, with} on stdin,
   runs assets/js/loadout-eval.js and writes the results (numbers as the hex of their double) to stdout.
   Offline, no dependencies. */
"use strict";
const fs = require("fs");
const path = require("path");
const W = require(path.join(__dirname, "..", "assets", "js", "loadout-eval.js"));

const buf = new DataView(new ArrayBuffer(8));
function hexf(x) {
  if (x === null || x === undefined) return null;
  buf.setFloat64(0, Number(x), false);
  let s = "";
  for (let i = 0; i < 8; i++) s += buf.getUint8(i).toString(16).padStart(2, "0");
  return s;
}

function canonical(r) {
  return {
    weapon: r.weapon.map((a) => ({
      tag: a.tag, base: hexf(a.base), final: hexf(a.final), notes: a.notes,
      steps: a.steps.map((c) => ({source: c.source, effect: c.effect, op: c.op, kind: c.kind,
                                  stacks: hexf(c.stacks), magnitude: hexf(c.magnitude), flag: c.flag})),
    })),
    character: r.character.map((c) => ({effect: c.effect, source: c.source})),
    applications: r.applications.map((a) => ({effect: a.effect, stacks: hexf(a.stacks), source: a.source})),
    attachments: r.attachments.map((a) => ({key: a.key, tag: a.tag, item: a.item})),
    hasBipod: r.hasBipod,
    notes: r.notes,
  };
}

const input = JSON.parse(fs.readFileSync(0, "utf-8"));
const M = W.model(JSON.parse(fs.readFileSync(input.json, "utf-8")));
const out = {results: [], cli: [], normalized: [], with: [], accepts: {}, defaults: {}};

for (const c of input.cases) {
  const lo = {weapon: c.weapon, items: c.items, sight: c.sight, stance: c.stance, bipod: c.bipod};
  out.results.push(canonical(W.evaluate(M, lo)));
  out.cli.push(W.cli(M, lo));
  out.normalized.push(W.normalize(M, lo).dropped.length === 0);
}
for (const c of input.with) {
  try {
    out.with.push(W.withItems(M, c.weapon, c.ids).items);
  } catch (e) {
    out.with.push("error");
  }
}
Object.keys(M.items).forEach((id) => {
  M.items[id].slots.forEach((s, i) => { out.accepts[id + "#" + i] = s.accepts.slice(); });
});
M.weapons.forEach((w) => { out.defaults[w.id] = W.defaultLoadout(M, w.id).items; });
process.stdout.write(JSON.stringify(out));
