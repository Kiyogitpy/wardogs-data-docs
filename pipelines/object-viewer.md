---
title: "Object Collision Viewer"
redirect_from: ["/object-viewer.html", "/object-viewer"]
parent: "Damage & Combat Systems"
description: "Collision shapes of buildables, fortifications, placed explosives and crates, with their health and damage data"
---

# Object Collision Viewer

*Data: [`assets/data/object-collision.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/object-collision.json), built by `python _tools/object_models.py`*

The collision shapes of the things players build, place and drop, drawn as they are cooked in the game's files: boxes, spheres, capsules and convex hulls. Pick an object, then a build stage, and click a piece to see its shapes, collision profile and trace setting. The panel's summary shows the object's max health, its damage row, how bullets, melee, grenades, rockets, C4 and IEDs change the damage it takes, and, for placed explosives, the blast values.

Vehicles and stationary weapons are in the [Vehicle Hitbox Viewer](vehicle-viewer.md); soldiers are in the [Infantry Hitbox Viewer](infantry-viewer.md). Health and damage rows: [Buildables §4](../game-features/Wardogs_Buildables_v1.md#4-health-and-damage-rules); blast values: [Explosives](../game-features/Wardogs_Explosives_v1.md).

<div class="vv ov" id="ov" markdown="0" data-json="{{ '/assets/data/object-collision.json' | relative_url }}?v={{ site.time | date: '%s' }}" data-base="{{ '/' | relative_url }}">
  <div class="vv-controls">
    <div class="vv-field">
      <label for="ov-object">Object</label>
      <select id="ov-object" disabled><option>Loading objects…</option></select>
    </div>
    <div class="vv-field" id="ov-stageField" hidden>
      <label for="ov-stage">Build stage</label>
      <select id="ov-stage"></select>
    </div>
  </div>
  <div class="vv-layout">
    <div class="vv-stage" id="ov-stage-box">
      <div class="vv-box">
        <model-viewer id="ov-model" class="vv-model" loading="lazy" reveal="auto" poster="{{ '/assets/images/vehicle-viewer-poster.svg' | relative_url }}" camera-controls touch-action="pan-y" interaction-prompt="none" shadow-intensity="0" exposure="1.1" camera-orbit="-35deg 70deg auto" alt="Collision shapes of the selected object"></model-viewer>
        <p class="vv-status" id="ov-status" role="status"></p>
        <div class="vv-fallback" id="ov-fallback" hidden></div>
      </div>
      <div class="vv-stage-bar">
        <span class="vv-hint">Drag to turn, scroll or pinch to zoom, click a piece to inspect it. Press Esc or click empty space to clear.</span>
      </div>
    </div>
    <aside class="vv-panel" id="ov-panel" aria-label="Selected object">
      <div id="ov-panel-body" aria-live="polite"></div>
    </aside>
  </div>
  <h2 class="vv-slots-title no_anchor" id="ov-slotsTitle">Meshes in this stage</h2>
  <ul class="vv-slots" id="ov-slots" aria-label="Pieces"></ul>
</div>

<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@4.3.1/dist/model-viewer.min.js" integrity="sha384-cprcVQt7wbUl0xngF3PGP6yBB7n4/t+4AoAMG9biiMCGFiWOdzUH10Ie2COTqFNW" crossorigin="anonymous" onerror="document.documentElement.classList.add('vv-mv-failed')"></script>
<script src="{{ '/assets/js/vendor/meshopt_decoder-1.2.0.js' | relative_url }}" defer></script>
<script src="{{ '/assets/js/object-viewer.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>

## What is shown

- **Collision shapes only.** A buildable's stage meshes have no separate collision mesh; their collision is a set of simple shapes stored with the mesh. Those shapes are what the viewer draws, in the mesh's own frame, placed where the build stage places the mesh. No render geometry, texture or image is used.
- **One stage at a time.** Each build stage swaps in its own meshes, so the stage selector shows that stage's shapes. A stage's decorative meshes (planks, crates, cables) are listed too; those without simple shapes are marked "no geometry".
- **Missing geometry.** A mesh with no simple shapes would collide on its render triangles, which are not published here. The FOB's finished-stage meshes are in that group; its foundation and its destroyed-state hulls are shown. The FOB's meshes are placed at the origin, because their relative placement is not in the exported data.
- **Props and aircraft** show the bodies of a physics asset on the skeletal mesh's reference pose, the way the infantry model is built.
- **Placed explosives** show the item's static mesh. The Claymore's box is also its trace collision; the other meshes use the default trace setting.
- **Other characters.** The one non-player combat mesh in the files, SK_Western_Mid, uses the player's physics asset (PA_TPCharacter_Simplified), so the [infantry model](infantry-viewer.md) covers it; the vendor, pilot and Rusalka NPC meshes name no physics asset.
