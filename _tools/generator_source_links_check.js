/* Offline DOM/source-target regressions; no browser, network or npm packages. */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { execFileSync } = require("node:child_process");
const root = path.join(__dirname, "..");
const tracked = new Set(execFileSync("git", ["ls-files", "-z", "data"], { cwd: root, encoding: "utf8" }).split("\0"));
const BLOB = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/";
class Node {
  constructor(tag, text = "") { this.tagName = tag.toUpperCase(); this.textContent = text; this.children = []; this.attrs = {}; }
  appendChild(child) { this.children.push(child); return child; }
  setAttribute(name, value) { this.attrs[name] = value; if (name === "href") this.href = value; }
  addEventListener() {}
  remove() {}
}
const document = {
  readyState: "loading", addEventListener() {},
  createElement: tag => new Node(tag),
  createTextNode: text => new Node("#text", text),
  createDocumentFragment: () => new Node("#fragment")
};
function load(name, expose) {
  const source = fs.readFileSync(path.join(root, "assets/js", name + ".js"), "utf8").trimEnd();
  assert.ok(source.endsWith("})();"));
  const context = { document };
  vm.createContext(context);
  vm.runInContext(source.slice(0, -5) + expose + "\n})();", context);
  return context;
}
function checkLink(node, file) {
  assert.equal(node.tagName, "A", file);
  assert.equal(node.href, BLOB + file.split("/").map(encodeURIComponent).join("/"));
  assert.ok(tracked.has(file), "unpublished target: " + file);
  assert.ok(fs.statSync(path.join(root, file)).isFile());
  assert.ok(file.startsWith("data/") && file.endsWith(".json"));
}
const infantry = load("infantry-viewer", "globalThis.pathNode = pathNode;");
const paths = new Set();
function scan(value) {
  if (typeof value === "string" && /^(data|sdk)\//.test(value)) paths.add(value.split(": ")[0]);
  else if (Array.isArray(value)) value.forEach(scan);
  else if (value && typeof value === "object") Object.values(value).forEach(scan);
}
scan(JSON.parse(fs.readFileSync(path.join(root, "assets/data/infantry-hitboxes.json"), "utf8")));
for (const file of paths) {
  const span = infantry.pathNode(file + ": Field.Path");
  checkLink(span.children[0], file);
  assert.equal(span.children[1].textContent, " Field.Path");
}
for (const file of ["sdk/raw/WDGame_classes.hpp", "data/Wardogs/Config/DefaultGame.ini"])
  assert.equal(infantry.pathNode(file).children[0].tagName, "CODE");
const season = load("season-diff", "globalThis.assetPathNode = assetPathNode; globalThis.changesTable = changesTable; globalThis.valueCell = valueCell; globalThis.changeCell = changeCell;");
const s2Revision = "8d0d6a9a0a3a0a0170e7ff3929202a92a5b9c12b";
const s2Paths = new Set(execFileSync("git", ["ls-tree", "-r", "--name-only", "-z", s2Revision, "data"],
  { cwd: root, encoding: "utf8", maxBuffer: 8 * 1024 * 1024 }).split("\0"));
let linked = 0, removed = 0;
for (const file of fs.readdirSync(path.join(root, "assets/data/season-diff"))) {
  const data = JSON.parse(fs.readFileSync(path.join(root, "assets/data/season-diff", file), "utf8"));
  for (const asset of data.assets || []) {
    const node = season.assetPathNode(asset, s2Revision);
    if (asset.status === "removed") { assert.equal(node.tagName, "CODE"); removed++; }
    else {
      const target = "data/" + asset.path;
      assert.equal(node.tagName, "A");
      assert.equal(node.href, BLOB.replace("/main/", "/" + s2Revision + "/") + target.split("/").map(encodeURIComponent).join("/"));
      assert.ok(s2Paths.has(target), "Missing historical S2 target: " + target);
      linked++;
    }
    assert.equal(node.textContent, asset.path);
  }
}
for (const asset of [
  { status: "added", path: "Wardogs/Config/DefaultGame.ini" },
  { status: "modified", path: "sdk/raw/WDGame_classes.hpp" }
]) assert.equal(season.assetPathNode(asset).tagName, "CODE");
assert.ok(paths.size > 0 && linked > 0 && removed > 0);
for (const labels of [["Season 1", "Season 2"], ["Season 2", "Season 3"]]) {
  const table = season.changesTable([{path: "Amount", op: "changed", before: 13.6, after: 14}], ...labels);
  const headers = table.children[0].children[0].children[0].children[0].children.map(n => n.textContent);
  assert.deepEqual(headers, ["Property", ...labels, "Change"]);
}
let currentLinked = 0;
for (const file of fs.readdirSync(path.join(root, "assets/data/season3-diff"))) {
  if (!file.endsWith(".json")) continue;
  const data = JSON.parse(fs.readFileSync(path.join(root, "assets/data/season3-diff", file), "utf8"));
  for (const asset of data.assets || []) {
    const node = season.assetPathNode(asset);
    if (asset.status === "removed") assert.equal(node.tagName, "CODE");
    else { checkLink(node, "data/" + asset.path); currentLinked++; }
  }
}
assert.ok(currentLinked > 0);
const exact = season.valueCell(9007199254740992, false, "9007199254740993");
assert.equal(exact.children[0].textContent, "9007199254740993");
const nested = season.changesTable([{path: "Container", op: "added", after: {n: 9007199254740992, zero: 0},
  after_literal: '{"n":9007199254740993,"zero":-0.0}'}], "Season 2", "Season 3");
const nestedValue = nested.children[0].children[0].children[1].children[0].children[0].children[2].children[0];
assert.equal(nestedValue.textContent, '{"n":9007199254740993,"zero":-0.0}');
const change = season.changeCell({before: 1, after: 1, before_type: "integer", after_type: "decimal"});
assert.equal(change.children[0].textContent, "integer → decimal");
const source = season.valueCell({$saved_export: {side: "s2", file: "Wardogs/Example.json", type: "array", count: 2000, export: ["Example", 1], pointer: "/Rows"}}, false);
assert.ok(source.children[1].href.includes("/" + s2Revision + "/data/Wardogs/Example.json"));
console.log(`source links: ${paths.size} current infantry, ${linked} pinned S2, ${currentLinked} current S3; both season headers, exact literals and source references pass`);
