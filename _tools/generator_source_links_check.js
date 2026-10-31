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
const season = load("season-diff", "globalThis.assetPathNode = assetPathNode;");
let linked = 0, removed = 0;
for (const file of fs.readdirSync(path.join(root, "assets/data/season-diff"))) {
  const data = JSON.parse(fs.readFileSync(path.join(root, "assets/data/season-diff", file), "utf8"));
  for (const asset of data.assets || []) {
    const node = season.assetPathNode(asset);
    if (asset.status === "removed") { assert.equal(node.tagName, "CODE"); removed++; }
    else { checkLink(node, "data/" + asset.path); linked++; }
    assert.equal(node.textContent, asset.path);
  }
}
for (const asset of [
  { status: "added", path: "Wardogs/Config/DefaultGame.ini" },
  { status: "modified", path: "sdk/raw/WDGame_classes.hpp" }
]) assert.equal(season.assetPathNode(asset).tagName, "CODE");
assert.ok(paths.size > 0 && linked > 0 && removed > 0);
console.log(`source links: ${paths.size} infantry JSON paths, ${linked} current season paths; ${removed} removed paths kept unlinked`);
