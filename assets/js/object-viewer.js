/* Object collision viewer (pipelines/object-viewer.md). Data: assets/data/object-collision.json, built by
   _tools/object_models.py; models: assets/models/objects/<id>.glb (collision primitives only, one material per
   stage and mesh, named "S<n>|<mesh>"; props: one per body). Styles are the vehicle viewer's .vv-* classes
   (_sass/custom/vehicle-viewer.scss), so this file holds only the page logic.
   Strings from the data are set as text only. */
(function () {
  "use strict";

  var MESHOPT = "assets/js/vendor/meshopt_decoder-1.2.0.js";
  var MV_TIMEOUT = 15000;
  var HIGHLIGHT = [0.35, 0.35, 0.35];
  
  var root, data, base, viewer, els = {};
  var state = { id: null, stage: 0, selected: null };
  var mvState = "pending", materials = [], loadToken = 0, fallbackText = null;

  function $(id) { return document.getElementById(id); }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }
  function num(x) {
    if (x == null) return "-";
    return Math.abs(x) >= 100 ? Math.round(x).toLocaleString("en-US") : String(Math.round(x * 100) / 100);
  }
  function status(text) { els.status.textContent = text || ""; els.status.hidden = !text; }

  function current() { return data.objects.filter(function (o) { return o.id === state.id; })[0]; }
  /* the finished stage: the first "Complete" stage, else the last one that is not a foundation or a destroyed state */
  function finishedStage(o) {
    var i, last = o.stages.length - 1;
    for (i = 0; i < o.stages.length; i++) if (/^Complete/.test(o.stages[i].name || "")) return i;
    for (i = o.stages.length - 1; i >= 0; i--) if (!/^(Foundation|Destroyed)/.test(o.stages[i].name || "")) return i;
    return last;
  }
  function stage() { var o = current(); return o && o.stages[state.stage]; }

  /* ---------- text ---------- */

  function shapeText(s) {
    if (s.size_m) return s.type + " " + s.size_m.map(num).join(" x ") + " m";
    if (s.type === "sphere") return "sphere radius " + num(s.radius_m) + " m";
    if (s.type === "sphyl") return "capsule radius " + num(s.radius_m) + " m, cylinder " + num(s.cylinder_length_m) + " m";
    return "convex hull, " + s.triangles + " triangles, extent " + (s.extent_m || []).map(num).join(" x ") + " m";
  }

  function shortMesh(m) { return m.replace(/^SM_/, ""); }

  function row(dl, term, value) {
    dl.appendChild(el("dt", null, term));
    var dd = el("dd");
    if (value && value.nodeType) dd.appendChild(value); else dd.textContent = value;
    dl.appendChild(dd);
  }
  function code(t) { return el("code", null, t); }
  function link(href, text) {
    var a = el("a", null, text);
    a.href = /^https?:/.test(href) ? href : base + href;
    return a;
  }

  /* ---------- panel ---------- */

  function summary(o, body) {
    body.appendChild(el("h2", "vv-panel-title no_anchor", o.name));
    var dl = el("dl", "vv-facts");
    row(dl, "Definition", code(o.asset));
    if (o.max_health != null) row(dl, "Max health", num(o.max_health));
    if (o.cost != null) row(dl, "Supply cost", num(o.cost));
    if (o.damage_row) row(dl, "Damage row", code(o.damage_row));
    if (o.modifiers) {
      var t = Object.keys(o.modifiers).map(function (k) { return k + " " + o.modifiers[k]; }).join(", ");
      row(dl, "Damage changes", t);
    }
    if (o.blast) {
      var b = o.blast;
      row(dl, "Explosion", num(b.BaseDamage) + " damage, radius " + num(b.ExplosiveRadius / 100) + " m (full damage inside " +
        num(b.EffectiveExplosiveRadius / 100) + " m), minimum " + num(b.MinimumExplosiveDamage));
    }
    (o.facts || []).forEach(function (f) { row(dl, f[0], f[1]); });
    body.appendChild(dl);
    (o.notes || []).forEach(function (n) { body.appendChild(el("p", "vv-note", n)); });
    var links = el("p", "vv-links");
    if (o.group === "buildables") {
      links.appendChild(link("Wardogs_Buildables_v1.html#4-health-and-damage-rules", "Buildables: health and damage"));
      links.appendChild(document.createTextNode(" · "));
    }
    if (o.group === "doors") {
      links.appendChild(link("Wardogs_HitRegistration_v1.html", "Hit registration"));
      links.appendChild(document.createTextNode(" · "));
    }
    if (o.group === "deployables" || o.group === "projectiles") {
      links.appendChild(link("Wardogs_Explosives_v1.html", "Explosives"));
      links.appendChild(document.createTextNode(" · "));
    }
    if (o.vehicle_viewer) {
      links.appendChild(link("vehicle-viewer.html#" + o.vehicle_viewer, "The vehicle hitbox model"));
      links.appendChild(document.createTextNode(" · "));
    }
    links.appendChild(link(data.meta.evidence, "How the models were extracted"));
    body.appendChild(links);
  }

  function pieceDetail(o, p, body) {
    body.appendChild(el("h2", "vv-panel-title no_anchor", shortMesh(p.mesh)));
    var dl = el("dl", "vv-facts");
    row(dl, o.group === "props" ? "Body (bone)" : "Static mesh", code(p.mesh));
    if (p.placements != null) row(dl, "Placements", String(p.placements));
    if (p.profile) row(dl, "Collision profile", code(p.profile) );
    if (p.component_profile) row(dl, "Component profile in the Blueprint", code(p.component_profile));
    if (p.visible === false) row(dl, "Visible in game", "no (collision proxy)");
    if (p.object_type) row(dl, "Object type", p.object_type);
    if (p.physics_type) row(dl, "Physics type", p.physics_type);
    if (p.trace_flag) row(dl, "Trace collision", p.trace_flag);
    if (p.phys_material) row(dl, "Physical material", code(p.phys_material));
    body.appendChild(dl);
    if (p.shapes && p.shapes.length) {
      body.appendChild(el("p", "vv-label", "Collision primitives"));
      var ul = el("ul");
      p.shapes.forEach(function (s) { ul.appendChild(el("li", null, shapeText(s))); });
      body.appendChild(ul);
    } else {
      body.appendChild(el("p", "vv-note", p.status));
    }
    if (p.spawns_actor) body.appendChild(el("p", "vv-note", "This stage also spawns " + p.spawns_actor + "."));
  }

  function updatePanel() {
    var o = current(), body = els.panelBody;
    body.textContent = "";
    if (!o) return;
    var p = state.selected && stage().pieces.filter(function (x) { return x.mesh === state.selected; })[0];
    if (p) pieceDetail(o, p, body); else summary(o, body);
  }

  /* ---------- lists and controls ---------- */

  function fillObjects() {
    els.object.textContent = "";
    data.groups.forEach(function (g) {
      var og = document.createElement("optgroup");
      og.label = g.label;
      data.objects.filter(function (o) { return o.group === g.id; }).forEach(function (o) {
        var opt = el("option", null, o.name);
        opt.value = o.id;
        og.appendChild(opt);
      });
      els.object.appendChild(og);
    });
    els.object.disabled = false;
  }

  function fillStages() {
    var o = current();
    els.stage.textContent = "";
    o.stages.forEach(function (s, i) {
      var opt = el("option", null, s.name || ("Stage " + (i + 1)));
      opt.value = String(i);
      els.stage.appendChild(opt);
    });
    els.stage.value = String(state.stage);
    els.stageField.hidden = o.stages.length < 2;
  }

  function buildList() {
    var o = current(), ul = els.slots;
    ul.textContent = "";
    stage().pieces.forEach(function (p) {
      var li = el("li");
      var b = el("button", "vv-slot", shortMesh(p.mesh) + (p.placements > 1 ? " x" + p.placements : ""));
      b.type = "button";
      b.setAttribute("aria-pressed", String(state.selected === p.mesh));
      if (p.status !== "ok") { b.appendChild(el("span", "vv-slot-note", " (no geometry)")); }
      b.addEventListener("click", function () { select(state.selected === p.mesh ? null : p.mesh); });
      li.appendChild(b);
      ul.appendChild(li);
    });
    els.slotsTitle.textContent = o.group === "props" ? "Bodies" : "Meshes in this stage";
  }

  function select(mesh) {
    state.selected = mesh;
    buildList();
    updatePanel();
    paint();
    writeHash();
  }

  /* ---------- model ---------- */

  function webgl() {
    try {
      var c = document.createElement("canvas");
      return !!(window.WebGLRenderingContext && (c.getContext("webgl2") || c.getContext("webgl")));
    } catch (e) { return false; }
  }

  function whenModelViewer() {
    return new Promise(function (resolve, reject) {
      if (!webgl()) { reject(new Error("WebGL is not available in this browser")); return; }
      if (!window.customElements) { reject(new Error("this browser has no custom elements")); return; }
      var started = Date.now();
      var poll = setInterval(function () {
        if (document.documentElement.classList.contains("vv-mv-failed")) {
          clearInterval(poll); reject(new Error("the 3D viewer script did not load"));
        } else if (Date.now() - started > MV_TIMEOUT) {
          clearInterval(poll); reject(new Error("the 3D viewer script took too long to load"));
        }
      }, 250);
      customElements.whenDefined("model-viewer").then(function () { clearInterval(poll); resolve(); });
    });
  }

  function showFallback(reason) {
    fallbackText = reason;
    els.stageBox.classList.add("is-fallback");
    els.fallback.hidden = false;
    els.fallback.textContent = "";
    els.fallback.appendChild(el("p", "vv-fallback-note", reason));
    var wrap = el("div", "table-wrapper"), t = el("table");
    var head = t.createTHead().insertRow();
    ["Mesh", "Collision primitives"].forEach(function (h) { var th = el("th", null, h); th.scope = "col"; head.appendChild(th); });
    var tb = t.createTBody();
    stage().pieces.forEach(function (p) {
      var r = tb.insertRow();
      r.insertCell().appendChild(code(p.mesh));
      r.insertCell().textContent = p.shapes && p.shapes.length ? p.shapes.map(shapeText).join("; ") : p.status;
    });
    wrap.appendChild(t);
    els.fallback.appendChild(wrap);
  }

  function hideFallback() {
    fallbackText = null;
    els.stageBox.classList.remove("is-fallback");
    els.fallback.hidden = true;
    els.fallback.textContent = "";
  }

  function loadModel() {
    var o = current();
    materials = [];
    if (mvState === "pending") { status("Loading the 3D viewer…"); return; }
    if (mvState !== "ok" || !o.glb) {
      status("");
      showFallback(mvState !== "ok" ? "The 3D view is unavailable (" + mvState + "). The collision geometry of this object:"
        : "No collision primitives are published for this object. Its meshes:");
      return;
    }
    hideFallback();
    status("Loading the collision shapes…");
    var token = ++loadToken;
    viewer.dataset.token = String(token);
    var src = base + o.glb;
    if (viewer.getAttribute("src") === src) onLoad(); else viewer.setAttribute("src", src);
  }

  function stageOfMaterial(name) {
    var m = /^S(\d+)\|/.exec(name);
    return m ? +m[1] - 1 : 0;
  }
  function meshOfMaterial(name) { return name.indexOf("|") >= 0 ? name.split("|").slice(1).join("|") : name; }

  function onLoad() {
    if (+viewer.dataset.token !== loadToken || !viewer.model) return;
    materials = viewer.model.materials.map(function (m) {
      return { material: m, stage: stageOfMaterial(m.name), mesh: meshOfMaterial(m.name),
               colour: m.pbrMetallicRoughness.baseColorFactor.slice(0, 3) };
    });
    status("");
    paint();
  }

  function paint() {
    materials.forEach(function (m) {
      var shown = m.stage === state.stage, sel = state.selected === m.mesh && shown;
      try {
        m.material.setAlphaMode(shown ? "OPAQUE" : "BLEND");
        m.material.pbrMetallicRoughness.setBaseColorFactor(m.colour.concat([shown ? 1 : 0]));
        m.material.setEmissiveFactor(sel ? HIGHLIGHT : [0, 0, 0]);
      } catch (e) { /* the viewer keeps the file's values */ }
    });
  }

  function setupPicking() {
    var down = null;
    viewer.addEventListener("pointerdown", function (e) { down = [e.clientX, e.clientY]; });
    viewer.addEventListener("click", function (e) {
      if (down && Math.abs(e.clientX - down[0]) + Math.abs(e.clientY - down[1]) > 6) return;   // a drag, not a click
      var r = viewer.getBoundingClientRect();
      var m = viewer.materialFromPoint(e.clientX - r.left, e.clientY - r.top);
      if (!m) { select(null); return; }
      var hit = materials.filter(function (x) { return x.material === m || x.material.index === m.index; })[0];
      if (!hit || hit.stage !== state.stage) return;
      select(state.selected === hit.mesh ? null : hit.mesh);
    });
  }

  /* ---------- state ---------- */

  function setObject(id, stageIdx, fromHash) {
    var o = data.objects.filter(function (x) { return x.id === id; })[0] || data.objects[0];
    state.id = o.id;
    state.stage = Math.max(0, Math.min(o.stages.length - 1, stageIdx == null ? finishedStage(o) : stageIdx));
    state.selected = null;
    els.object.value = o.id;
    fillStages();
    buildList();
    updatePanel();
    loadModel();
    paint();
    if (!fromHash) writeHash();
  }

  function setStage(i) {
    state.stage = i;
    state.selected = null;
    buildList();
    updatePanel();
    if (fallbackText) { hideFallback(); loadModel(); }
    paint();
    writeHash();
  }

  function writeHash() {
    try { history.replaceState(null, "", "#" + state.id + "/" + (state.stage + 1)); } catch (e) { /* ignore */ }
  }

  function parseHash() {
    var m = /^#([a-z0-9-]+)(?:\/(\d+))?$/.exec(location.hash);
    return m ? { id: m[1], stage: m[2] ? +m[2] - 1 : null } : { id: null, stage: null };
  }

  ready(function () {
    root = $("ov");
    if (!root) return;
    base = root.getAttribute("data-base") || "/";
    ["object", "stage", "stageField", "status", "fallback", "slots", "slotsTitle"].forEach(function (k) { els[k] = $("ov-" + k); });
    els.panelBody = $("ov-panel-body");
    els.stageBox = $("ov-stage-box");
    viewer = $("ov-model");
    status("Loading the object data…");
    fetch(root.getAttribute("data-json"))
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (json) {
        data = json;
        fillObjects();
        els.object.addEventListener("change", function () { setObject(els.object.value, null, false); });
        els.stage.addEventListener("change", function () { setStage(+els.stage.value); });
        document.addEventListener("keydown", function (e) {
          if (e.key === "Escape" && state.selected && e.target.tagName !== "SELECT") select(null);
        });
        window.addEventListener("hashchange", function () { var h = parseHash(); setObject(h.id, h.stage, true); });
        viewer.addEventListener("load", onLoad);
        viewer.addEventListener("error", function () { status("The model could not be loaded."); });
        setupPicking();
        var h = parseHash();
        setObject(h.id, h.stage, true);
        whenModelViewer().then(function () {
          customElements.get("model-viewer").meshoptDecoderLocation = new URL(base + MESHOPT, location.href).href;
          mvState = "ok";
        }, function (err) { mvState = err.message; }).then(function () {
          root.classList.toggle("vv-no-3d", mvState !== "ok");
          loadModel();
          paint();
        });
      })
      .catch(function (err) {
        status("The object data could not be loaded (" + err.message + ").");
        root.classList.add("vv-no-data");
      });
  });
})();
