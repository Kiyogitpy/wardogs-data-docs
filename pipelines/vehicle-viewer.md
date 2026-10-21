---
title: "Vehicle Hitbox Viewer"
parent: "Pipelines"
nav_order: 2.5
redirect_from: ["/vehicle-viewer.html", "/vehicle-viewer"]
---

# Vehicle Hitbox Viewer

*Data: [`assets/data/vehicle-hitboxes.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-hitboxes.json), built by `python _tools/damage_tables.py --json`*

Every vehicle's collision mesh, coloured by the health section each collision slot feeds. Pick a slot on the model or in the list to see its section, how it passes damage to the main health, and how many hits of a caliber destroy the vehicle through it. How slots and routing work: [Vehicle Damage Pipeline](Wardogs_VehicleDamagePipeline_v1.md#31-hitboxes) §3.1 (hitboxes), [§4.2](Wardogs_VehicleDamagePipeline_v1.md#42-routing-semantics) (routing) and [§5.4](Wardogs_VehicleDamagePipeline_v1.md#54-hits-to-destroy) (hits to destroy).

For soldiers, the [Infantry Hitbox Viewer](infantry-viewer.md) shows the player's physics bodies by hit location.

<div class="vv" id="vv" markdown="0" data-json="{{ '/assets/data/vehicle-hitboxes.json' | relative_url }}?v={{ site.time | date: '%s' }}" data-base="{{ '/' | relative_url }}">
  <div class="vv-controls">
    <div class="vv-field">
      <label for="vv-vehicle">Vehicle</label>
      <select id="vv-vehicle" disabled><option>Loading vehicles…</option></select>
    </div>
    <div class="vv-field" id="vv-variant-field" hidden>
      <label for="vv-variant">Variant</label>
      <select id="vv-variant"></select>
    </div>
    <div class="vv-field" id="vv-wheels-field" hidden>
      <label for="vv-wheels">Wheels (damage state)</label>
      <select id="vv-wheels"><option value="intact">Intact</option><option value="destroyed">Deflated or destroyed</option></select>
    </div>
    <div class="vv-field">
      <label for="vv-caliber">Projectile / explosive</label>
      <select id="vv-caliber" disabled><option>…</option></select>
    </div>
    <div class="vv-field" id="vv-blastField" hidden>
      <label for="vv-interaction">Interaction</label>
      <select id="vv-interaction"><option value="inspect">Inspect slots</option><option value="impact">Place impact</option></select>
    </div>
    <div class="vv-field vv-field-mode">
      <span class="vv-label" id="vv-mode-label">Colour by</span>
      <div class="wd-segmented vv-mode" id="vv-mode" role="radiogroup" aria-labelledby="vv-mode-label">
        <button type="button" role="radio" value="section" aria-checked="true">Section</button>
        <button type="button" role="radio" value="hits" aria-checked="false" tabindex="-1">Hits to destroy</button>
        <button type="button" role="radio" value="factor" aria-checked="false" tabindex="-1">Rule factor</button>
      </div>
    </div>
  </div>
  <details class="vv-reference">
    <summary>Local reference geometry</summary>
    <p>Load a private cooked-reference pack to use its collision meshes and query model. Files stay in this browser. Activation, pose and component order are supplied reference inputs, not a captured game scene.</p>
    <div class="vv-reference-actions">
      <label for="vv-referenceFile">Load reference pack (.json or .json.gz)<input id="vv-referenceFile" type="file" accept=".json,.gz,application/json,application/gzip"></label>
      <button type="button" id="vv-referenceReset" disabled>Use published geometry</button>
    </div>
    <p id="vv-referenceStatus" role="status" aria-live="polite">Published geometry in use.</p>
  </details>
  <div class="vv-layout">
    <div class="vv-stage" id="vv-stage">
      <div class="vv-box">
        <model-viewer id="vv-model" class="vv-model" loading="lazy" reveal="auto" poster="{{ '/assets/images/vehicle-viewer-poster.svg' | relative_url }}" camera-controls touch-action="pan-y" interaction-prompt="none" shadow-intensity="0" exposure="1.1" camera-orbit="-35deg 70deg auto" alt="Collision mesh of the selected vehicle, coloured by health section"></model-viewer>
        <svg id="vv-impactOverlay" class="vv-impact-overlay" aria-hidden="true" hidden></svg>
        <p class="vv-status" id="vv-status" role="status"></p>
        <div class="vv-fallback" id="vv-fallback" hidden></div>
      </div>
      <div class="vv-notes" id="vv-notes" role="note" hidden></div>
      <div class="vv-impact-controls" id="vv-impactControls" hidden>
        <p id="vv-impactHelp" role="status">Choose an explosive caliber, then place an impact on the vehicle or nearby ground.</p>
        <form id="vv-groundForm" class="vv-ground-form">
          <label for="vv-impactX">Ground X (m)<input id="vv-impactX" type="number" step="0.1" value="0" required></label>
          <label for="vv-impactZ">Ground Z (m)<input id="vv-impactZ" type="number" step="0.1" value="0" required></label>
          <button type="submit" id="vv-placeGround" disabled>Place on ground</button>
          <button type="button" id="vv-clearImpact" disabled>Clear impact</button>
        </form>
        <p class="vv-impact-key">Solid ring: outer radius. Dashed ring: full damage radius. Rings show a sphere's three planes.</p>
      </div>
      <div class="vv-stage-bar">
        <span class="vv-checks"><label class="vv-check"><input type="checkbox" id="vv-labels" checked> Show labels</label>
        <label class="vv-check"><input type="checkbox" id="vv-xray" checked> See-through selection</label></span>
        <span class="vv-hint" id="vv-hint">Drag to turn, scroll or pinch to zoom, click a part to inspect it. While a part is selected, the rest turns see-through: click the model or press Esc to clear, and pick inner parts from the labels or the list.</span>
      </div>
    </div>
    <aside class="vv-panel" id="vv-panel" aria-label="Selected slot">
      <div id="vv-impactSummary" class="vv-impact-summary" aria-live="polite" hidden></div>
      <div id="vv-panel-body" aria-live="polite">
        <h2 class="vv-panel-title no_anchor is-empty">No slot selected</h2>
        <p class="vv-panel-empty">Click a part of the model, or pick a slot from the list below.</p>
      </div>
    </aside>
  </div>
  <div class="vv-legend" id="vv-legend"></div>
  <h2 class="vv-slots-title no_anchor">Collision slots</h2>
  <ul class="vv-slots" id="vv-slots" aria-label="Collision slots"></ul>
</div>

<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@4.3.1/dist/model-viewer.min.js" integrity="sha384-cprcVQt7wbUl0xngF3PGP6yBB7n4/t+4AoAMG9biiMCGFiWOdzUH10Ie2COTqFNW" crossorigin="anonymous" onerror="document.documentElement.classList.add('vv-mv-failed')"></script>
<script src="{{ '/assets/js/vendor/meshopt_decoder-1.2.0.js' | relative_url }}" defer></script>
<script src="{{ '/assets/js/vehicle-impact-geometry.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
<script src="{{ '/assets/js/vehicle-impact.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
<script src="{{ '/assets/js/vehicle-cooked-queries.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
<script src="{{ '/assets/js/vehicle-reference-pack.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
<script src="{{ '/assets/js/vehicle-viewer.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>

For explosives, choose **Place impact** and click the vehicle (**Direct hit**) or nearby ground (**Splash**). You can also enter ground X/Z coordinates in metres. Each placement starts with full health. Projectile shots travel from the current view toward that point; the blast centre moves back by half the authored projectile length, as in the traced impact path. Placed explosive actors use the selected point. The result is a **reference-pose estimate** from exported collision triangles and traced damage routing: component order, moving parts and the live scene can change the result. Gepard uses its authored damage-query sockets and SPW spawn variants use their authored component bounds; other models retain sampled display surfaces. Inspect slots retains the direct-hit rule and repeated-hit comparison for individual slots.

**Local reference packs** also replace the displayed mesh and component sampling metadata. They use the frozen build's cooked triangle/BVH query model and retain their supplied scene order. They do not provide terrain, moving poses, active physics state or other players, and are released when you return to published geometry or close the page.

Blast amounts apply the selected rules in native order with single-precision rounding, then follow the traced section routing. Displayed rule factors remain summaries. The calculation uses the exported source context and declared target assumptions; runtime registry overrides and extra actor context are not captured. The [Round 11 verification](../docs/ROUND11_STATUS.md) records the native comparisons and their limits.

## How the models are built

The models come from [`_tools/vehicle_models.py`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/vehicle_models.py), using meshes decoded with [`tools/cue4parse_extractor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/tools/cue4parse_extractor/README.md).

- **Collision meshes only.** Each part is the low-poly, untextured mesh that its render mesh names in `ComplexCollisionMesh`, not the render model. Its materials are the collision slots.
- **Placed in the reference pose.** Each part sits on the bone or socket it attaches to; doors and landing gear are shown in the reference pose too.
- **One model per distinct variant geometry.** Variants that share a damage map but differ in turrets, rear boxes or mounts each get their own model (the Variant list).
- **Left wheels are mirrored copies** of the right-side wheel mesh. The mirroring flag isn't in the export, so this is assumed.
- **Slots resolve as the game resolves them** ([Vehicle §3.2](Wardogs_VehicleDamagePipeline_v1.md#32-from-a-hit-triangle-to-a-section)). Only registered static meshes count. Instanced wheels are in the Wheel surface group and add the wheel's DataIndex (`CC_Wheel` becomes `CC_Wheel_2`), which runs axle by axle. Every other mesh is in the Default group and keeps its slot name as is. A slot missing from its group's map takes that group's default section. Projectile hits resolve their own triangle's section. For an explosion, the vehicle's first component hit selects the section for every radial application on that vehicle; each component hit still supplies its own location tag to the damage rules.
- **Wheels are shown intact unless you pick a damage state.** Destroyed (state 2 in [Vehicle §3.2](Wardogs_VehicleDamagePipeline_v1.md#32-from-a-hit-triangle-to-a-section)'s wheel mesh swap) shows every wheel's destroyed-mesh collision, which has no tyre slot. Deflated (state 1) keeps the intact look and traces the destruction mesh's hull. The slot name still comes from the intact wheel's collision mesh and the hull's triangles all give index 0, so a deflated hit gives `CC_Wheel`, the same hitbox; a wheel deflates at tyre health / max ≤ 0.55 and is destroyed at 0. The Wheels control appears only on the Humvee (WHL_05) and WHL_08, the vehicles whose destroyed wheels have their own collision mesh; on the others both states keep the intact hitbox.
- **Rotor blades are hitboxes like the hubs.** They register and resolve by their slot (`CC_MainRotor` / `CC_TailRotor`). Their `WDRotorCollision` profile blocks bullet traces; projectile sweeps ignore it.
- **Parts that can't be placed are left out**, with a note on the model. The MG nest's gun proxy attaches to a `receiver_J` bone that its skeleton doesn't have, so it is likely never attached.
- **Meshes without a collision mesh of their own aren't shown**, such as the MG nest's sandbags. Their collision profile isn't traced, and showing them would mean publishing render geometry.
- **The SPW radar is shown stowed.** No exported data creates its deployed pivot.
- **Blast sampling is partly reconstructed.** [Gepard uses authored sockets](../docs/evidence/round8-gepard-sampling-viewer.md) and SPW uses authored bounds; other models still sample display surfaces. The [fresh input census](../docs/evidence/round8-vehicle-sampling-census.md) covers all 33 source variants and distinguishes available damage-query sockets from verified viewer behavior.

<div class="vv-nojs" markdown="1">

## Hitbox table

The viewer needs JavaScript; this is the same data as a table. Every vehicle's collision slots, the section each one feeds (with its maximum health), how that section passes damage to the main health, and the rule factor at that slot for three calibers (the viewer itself offers every caliber in the data, grouped; [Vehicle Damage Pipeline](Wardogs_VehicleDamagePipeline_v1.md#31-hitboxes) §3.1).

<!-- damage_tables --hitboxes -->
| Vehicle (variants) | Collision slot | Section (max health) | Routing to main health | `556mm` | `50Cal` | `30mm` |
|---|---|---|---|---:|---:|---:|
| `Air.Rotary.Havoc` (Attack_ROT_02) | `CC_Engine` | Health.Engine (200) | none | ×0.05 | ×0.05 | ×0.195 |
|  | `CC_FuelTank` | Health.FuelTank (200) | none | ×0.2 | ×0.2 | ×0.195 |
|  | `CC_MainRotor` | Health.Rotor.Main (400) | post 1 when depleted, simultaneous 0.5 | ×0.025 | ×0.025 | ×0.195 |
|  | `CC_TailRotor` | Health.Rotor.Tail (300) | post 1 when depleted, simultaneous 1 | ×0.025 | ×0.025 | ×0.195 |
|  | `CC_Wheel_0` (unreachable: an indexed name, but no instanced wheel indexes this slot) | Health.Wheel.Left.Front (100) | post 1 when depleted | ×0.05 | ×0.05 | ×0.195 |
|  | `CC_Wheel_1` (unreachable: an indexed name, but no instanced wheel indexes this slot) | Health.Wheel.Right.Front (100) | post 1 when depleted | ×0.05 | ×0.05 | ×0.195 |
|  | `(default)` | Health (800) | is the main health | ×0.025 | ×0.025 | ×0.195 |
| `Air.Rotary.LittleBird` (ROT_03_Default, ROT_03_MachineGuns, ROT_03_RocketPods) | `CC_Engine` | Health.Engine (200) | none | ×0.075 | ×0.075 | ×0.595 |
|  | `CC_FuelTank` | Health.FuelTank (200) | none | ×0.075 | ×0.075 | ×0.595 |
|  | `CC_MainRotor` | Health.Rotor.Main (400) | post 1 when depleted, simultaneous 0.5 | ×0.075 | ×0.075 | ×0.595 |
|  | `CC_TailRotor` | Health.Rotor.Tail (300) | post 1 when depleted, simultaneous 1 | ×0.075 | ×0.075 | ×0.595 |
|  | `(default)` | Health (400) | is the main health | ×0.075 | ×0.075 | ×0.595 |
| `Air.Rotary.ROT_04` (ROT_04_Default, ROT_04_MountedMachineGuns) | `CC_Engine` | Health.Engine (200) | none | ×0.05 | ×0.05 | ×0.255 |
|  | `CC_FuelTank` | Health.FuelTank (200) | none | ×0.225 | ×0.225 | ×0.255 |
|  | `CC_MainRotor` | Health.Rotor.Main (400) | post 1 when depleted, simultaneous 0.5 | ×0.05 | ×0.05 | ×0.255 |
|  | `CC_TailRotor` | Health.Rotor.Tail (300) | post 1 when depleted, simultaneous 1 | ×0.05 | ×0.05 | ×0.255 |
|  | `(default)` | Health (600) | is the main health | ×0.025 | ×0.025 | ×0.255 |
| `Land.Tracked.Leopard.Spawn` (SPW_01) | `CC_FuelTank` | Health.FuelTank (100) | none | ×0 | ×0 | ×0.21 |
|  | `CC_MainBody` | Health (1000) | is the main health | ×0 | ×0 | ×0.21 |
|  | `CC_Radar` | Health.Radar (100) | none | ×0.05 | ×0.05 | ×0.21 |
|  | `CC_Tracks_L` | Health.Tracks.Left (125) | post 0.5 when depleted, simultaneous 1 | ×0 | ×0 | ×0.21 |
|  | `CC_Tracks_R` | Health.Tracks.Right (125) | post 0.5 when depleted, simultaneous 1 | ×0 | ×0 | ×0.21 |
|  | `CC_Radar` [Radar] (unreachable: no component registers this group) | Health.Radar (100) | none | ×0.05 | ×0.05 | ×0.21 |
|  | `(default)` | Health (1000) | is the main health | ×0 | ×0 | ×0.21 |
| `Land.Tracked.Leopard.Spawn` (SPW_02, SPW_03) | `CC_FuelTank` | Health.FuelTank (100) | none | ×0 | ×0 | ×0.21 |
|  | `CC_MainBody` | Health (1000) | is the main health | ×0 | ×0 | ×0.21 |
|  | `CC_Radar` | Health.Radar (100) | none | ×0.05 | ×0.05 | ×0.21 |
|  | `CC_Tracks_L` | Health.Tracks.Left (125) | post 0.5 when depleted, simultaneous 1 | ×0 | ×0 | ×0.21 |
|  | `CC_Tracks_R` | Health.Tracks.Right (125) | post 0.5 when depleted, simultaneous 1 | ×0 | ×0 | ×0.21 |
|  | `CC_Radar` [Radar] (unreachable: no component registers this group) | Health.Radar (100) | none | ×0.05 | ×0.05 | ×0.21 |
|  | `(default)` | Health (1000) | is the main health | ×0 | ×0 | ×0.21 |
|  | `(default)` [Radar] (unreachable: no component registers this group) | Health.Radar (100) | none | ×0.05 | ×0.05 | ×0.21 |
| `Stationary.Mistral` (STN_01) | `CC_Main` | Health (3000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
|  | `(default)` | Health (3000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
| `Stationary.Phalanx` (STN_02) | `CC_Main` | Health (5000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
|  | `(default)` | Health (5000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
| `Stationary.Mortar` (STN_03) | `CC_Main` | Health (3000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
|  | `(default)` | Health (3000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
| `Stationary.RadioTower` (STN_04) | `CC_Main` | Health (1000) | is the main health | ×0.05 | ×0.05 | ×0.85 |
|  | `(default)` | Health (1000) | is the main health | ×0.05 | ×0.05 | ×0.85 |
| `Stationary.STN_05` (STN_05) | `CC_Main` | Health (3000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
|  | `(default)` | Health (3000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
| `Stationary.MGNest` (STN_06, no row of its own) | `CC_Main` | Health (1800) | is the main health | ×1 | ×1 | ×1 |
|  | `(default)` | Health (1800) | is the main health | ×1 | ×1 | ×1 |
| `Land.Tracked.TNK_01.AntiAir` (TNK_01_AntiAir) | `CC_Engine` | Health.Engine (150) | post 1 when depleted, simultaneous 1 | ×0 | ×0 | ×0.18 |
|  | `CC_FuelTank` | Health.FuelTank (150) | none | ×0 | ×0 | ×0.18 |
|  | `CC_MainBody` | Health (800) | is the main health | ×0 | ×0 | ×0.18 |
|  | `CC_Tracks_L` | Health.Tracks.Left (125) | post 0.5 when depleted, simultaneous 1 | ×0 | ×0 | ×0.18 |
|  | `CC_Tracks_R` | Health.Tracks.Right (125) | post 0.5 when depleted, simultaneous 1 | ×0 | ×0 | ×0.18 |
|  | `(default)` | Health (800) | is the main health | ×0 | ×0 | ×0.18 |
| `Land.Tracked.TNK_01.Artillery` (TNK_01_Artillery) | `CC_Engine` | Health.Engine (150) | post 1 when depleted, simultaneous 1 | ×0 | ×0 | ×0.18 |
|  | `CC_FuelTank` | Health.FuelTank (100) | none | ×0 | ×0 | ×0.18 |
|  | `CC_MainBody` | Health (650) | is the main health | ×0 | ×0 | ×0.18 |
|  | `CC_Tracks_L` | Health.Tracks.Left (125) | post 0.5 when depleted, simultaneous 1 | ×0 | ×0 | ×0.18 |
|  | `CC_Tracks_R` | Health.Tracks.Right (125) | post 0.5 when depleted, simultaneous 1 | ×0 | ×0 | ×0.18 |
|  | `(default)` | Health (650) | is the main health | ×0 | ×0 | ×0.18 |
| `Land.Tracked.TNK_01.Heavy` (TNK_01_Heavy) | `CC_Engine` | Health.Engine (150) | post 1 when depleted, simultaneous 1 | ×0 | ×0 | ×0.18 |
|  | `CC_FuelTank` | Health.FuelTank (150) | none | ×0 | ×0 | ×0.18 |
|  | `CC_MainBody` | Health (800) | is the main health | ×0 | ×0 | ×0.18 |
|  | `CC_StrongArea` | Health.Body.StrongArea (350) | pre 0.4, post 1 when depleted | ×0 | ×0 | ×0.18 |
|  | `CC_Tracks_L` | Health.Tracks.Left (125) | post 0.5 when depleted, simultaneous 1 | ×0 | ×0 | ×0.18 |
|  | `CC_Tracks_R` | Health.Tracks.Right (125) | post 0.5 when depleted, simultaneous 1 | ×0 | ×0 | ×0.18 |
|  | `(default)` | Health (800) | is the main health | ×0 | ×0 | ×0.18 |
| `Land.Tracked.TNK_04.Default` (TNK_04) | `CC_Engine` | Health.Engine (150) | post 1 when depleted, simultaneous 1 | ×0 | ×0 | ×0.21 |
|  | `CC_FuelTank` | Health.FuelTank (150) | none | ×0 | ×0 | ×0.21 |
|  | `CC_MainBody` | Health (750) | is the main health | ×0 | ×0 | ×0.21 |
|  | `CC_Tracks_L` | Health.Tracks.Left (125) | post 0.85 when depleted, simultaneous 1 | ×0 | ×0 | ×0.21 |
|  | `CC_Tracks_R` | Health.Tracks.Right (125) | post 0.85 when depleted, simultaneous 1 | ×0 | ×0 | ×0.21 |
|  | `(default)` | Health (750) | is the main health | ×0 | ×0 | ×0.21 |
| `Land.Wheeled.Bobcat` (WHL_01_Default) | `CC_Engine` | Health (200) | is the main health | ×0.075 | ×0.075 | ×1 |
|  | `CC_FuelTank` | Health.FuelTank (100) | none | ×0.075 | ×0.075 | ×1 |
|  | `CC_Wheel_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.45 | ×0.45 | ×1 |
|  | `CC_Wheel_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.45 | ×0.45 | ×1 |
|  | `CC_Wheel_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.45 | ×0.45 | ×1 |
|  | `CC_Wheel_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.45 | ×0.45 | ×1 |
|  | `(default)` | Health (200) | is the main health | ×0.075 | ×0.075 | ×1 |
| `Land.Wheeled.Patriot.Kodiak` (WHL_02_Default, WHL_02_Pickup, WHL_02_SUV_RingTurret) | `CC_Engine` | Health (400) | is the main health | ×0.025 | ×0.025 | ×0.5 |
|  | `CC_FuelTank` | Health.FuelTank (400) | none | ×0.15 | ×0.15 | ×0.5 |
|  | `CC_Wheel_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.4 | ×0.4 | ×0.5 |
|  | `CC_Wheel_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.4 | ×0.4 | ×0.5 |
|  | `CC_Wheel_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.4 | ×0.4 | ×0.5 |
|  | `CC_Wheel_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.4 | ×0.4 | ×0.5 |
|  | `(default)` | Health (400) | is the main health | ×0.025 | ×0.025 | ×0.5 |
| `Land.Wheeled.Humvee.Default` (WHL_05_Humvee_Default) | `CC_Engine` | Health (500) | is the main health | ×0.025 | ×0.025 | ×0.3 |
|  | `CC_FuelTank` | Health.FuelTank (400) | pre 0.25, post 1 when depleted | ×0.25 | ×0.25 | ×0.3 |
|  | `CC_Tyre_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.3 |
|  | `CC_Tyre_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.3 |
|  | `CC_Tyre_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.3 |
|  | `CC_Tyre_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.3 |
|  | `CC_Wheel_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.3 |
|  | `CC_Wheel_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.3 |
|  | `CC_Wheel_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.3 |
|  | `CC_Wheel_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.3 |
|  | `(default)` | Health (500) | is the main health | ×0.025 | ×0.025 | ×0.3 |
| `Land.Wheeled.Humvee.Minigun` (WHL_05_Humvee_RingMinigun) | `CC_Engine` | Health (500) | is the main health | ×0.0125 | ×0.0125 | ×0.25 |
|  | `CC_FuelTank` | Health.FuelTank (400) | pre 0.25, post 1 when depleted | ×0.125 | ×0.125 | ×0.25 |
|  | `CC_Tyre_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.25 |
|  | `CC_Tyre_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.25 |
|  | `CC_Tyre_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.25 |
|  | `CC_Tyre_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.25 |
|  | `CC_Wheel_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.25 |
|  | `CC_Wheel_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.25 |
|  | `CC_Wheel_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.25 |
|  | `CC_Wheel_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.25 |
|  | `(default)` | Health (500) | is the main health | ×0.0125 | ×0.0125 | ×0.25 |
| `Land.Wheeled.Humvee.MachineGun` (WHL_05_Humvee_RingTurret) | `CC_Engine` | Health (500) | is the main health | ×0.02 | ×0.02 | ×0.225 |
|  | `CC_FuelTank` | Health.FuelTank (400) | pre 0.25, post 1 when depleted | ×0.2 | ×0.2 | ×0.225 |
|  | `CC_Tyre_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.225 |
|  | `CC_Tyre_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.225 |
|  | `CC_Tyre_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.225 |
|  | `CC_Tyre_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.225 |
|  | `CC_Wheel_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.225 |
|  | `CC_Wheel_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.225 |
|  | `CC_Wheel_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.225 |
|  | `CC_Wheel_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.3 | ×0.3 | ×0.225 |
|  | `(default)` | Health (500) | is the main health | ×0.02 | ×0.02 | ×0.225 |
| `Land.Wheeled.DuneBuggy` (WHL_06_DuneBuggy_Default) | `CC_Engine` | Health (400) | is the main health | ×0.05 | ×0.05 | ×0.4 |
|  | `CC_FuelTank` | Health.FuelTank (300) | post 1 when depleted | ×0.3 | ×0.3 | ×0.4 |
|  | `CC_Tyre_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.375 | ×0.375 | ×0.4 |
|  | `CC_Tyre_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.375 | ×0.375 | ×0.4 |
|  | `CC_Tyre_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.375 | ×0.375 | ×0.4 |
|  | `CC_Tyre_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.375 | ×0.375 | ×0.4 |
|  | `CC_Wheel_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.375 | ×0.375 | ×0.4 |
|  | `CC_Wheel_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.375 | ×0.375 | ×0.4 |
|  | `CC_Wheel_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.375 | ×0.375 | ×0.4 |
|  | `CC_Wheel_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.375 | ×0.375 | ×0.4 |
|  | `(default)` | Health (400) | is the main health | ×0.05 | ×0.05 | ×0.4 |
| `Land.Wheeled.Ural` (WHL_07_Battle, WHL_07_Default, WHL_07_ArmouredBattle) | `CC_Engine` | Health (700) | is the main health | ×0.025 | ×0.025 | ×0.6 |
|  | `CC_Flatbed` | Health.Body.ModerateArea (1) | pre 0.25, post 0.35 when depleted | ×0.05 | ×0.05 | ×0.6 |
|  | `CC_FuelTank` | Health.FuelTank (400) | pre 0.25, post 1 when depleted | ×0.225 | ×0.225 | ×0.6 |
|  | `CC_Tyre_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.6 |
|  | `CC_Tyre_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.6 |
|  | `CC_Tyre_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.6 |
|  | `CC_Tyre_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.6 |
|  | `CC_Tyre_4` [Wheel] | Health.Wheel.Left.Middle (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.6 |
|  | `CC_Tyre_5` [Wheel] | Health.Wheel.Right.Middle (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.6 |
|  | `CC_Wheel_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.6 |
|  | `CC_Wheel_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.6 |
|  | `CC_Wheel_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.6 |
|  | `CC_Wheel_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.6 |
|  | `CC_Wheel_4` [Wheel] | Health.Wheel.Left.Middle (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.6 |
|  | `CC_Wheel_5` [Wheel] | Health.Wheel.Right.Middle (75) | pre 0.25, post 0.25 when depleted | ×0.225 | ×0.225 | ×0.6 |
|  | `(default)` | Health (700) | is the main health | ×0.025 | ×0.025 | ×0.6 |
| `Land.Wheeled.WHL_08.Default` (WHL_08_Default, WHL_08_RingTurret) | `CC_Engine` | Health (500) | is the main health | ×0.025 | ×0.025 | ×0.4 |
|  | `CC_FuelTank` | Health.FuelTank (400) | none | ×0.2 | ×0.2 | ×0.4 |
|  | `CC_Tyre_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.35 | ×0.35 | ×0.4 |
|  | `CC_Tyre_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.35 | ×0.35 | ×0.4 |
|  | `CC_Tyre_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.35 | ×0.35 | ×0.4 |
|  | `CC_Tyre_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.35 | ×0.35 | ×0.4 |
|  | `CC_Wheel_0` [Wheel] | Health.Wheel.Left.Front (75) | pre 0.25, post 0.25 when depleted | ×0.35 | ×0.35 | ×0.4 |
|  | `CC_Wheel_1` [Wheel] | Health.Wheel.Right.Front (75) | pre 0.25, post 0.25 when depleted | ×0.35 | ×0.35 | ×0.4 |
|  | `CC_Wheel_2` [Wheel] | Health.Wheel.Left.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.35 | ×0.35 | ×0.4 |
|  | `CC_Wheel_3` [Wheel] | Health.Wheel.Right.Rear (75) | pre 0.25, post 0.25 when depleted | ×0.35 | ×0.35 | ×0.4 |
|  | `(default)` | Health (500) | is the main health | ×0.025 | ×0.025 | ×0.4 |
<!-- /damage_tables -->

</div>
