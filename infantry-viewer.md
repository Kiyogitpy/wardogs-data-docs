---
title: "Infantry Hitbox Viewer"
parent: "Pipelines"
nav_order: 2.75
---

# Infantry Hitbox Viewer

*Data: [`assets/data/infantry-hitboxes.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/infantry-hitboxes.json), built by `python _tools/infantry_tables.py --json`*

The player's physics-asset bodies, coloured by the hit location each body's bone maps to. Pick a damage source to recolour the body by that source's hit-location multiplier, and an armor or helmet to see the hit locations it covers. Pick a body on the model or in the list to see its bone, hit location and multiplier. How it works: [Damage Pipeline](Wardogs_DamagePipeline_v2.md#71-b_bonedamagemodifiers_c-entries-5-7-10) §7.1 (the hit-location rule), [§8.1](Wardogs_DamagePipeline_v2.md#81-bonedamagemodifiers-hit-location-table) (its table) and [§7.5](Wardogs_DamagePipeline_v2.md#75-wddamagemodificationoperation_playerarmordurability-entries-142144) (armor), and [Game Mechanics](Wardogs_GameMechanics_v2.md#2b-hit-locations-da_globaldamage_hitlocations_player) §2b (bones to hit locations).

<div class="vv iv" id="iv" markdown="0" data-json="{{ '/assets/data/infantry-hitboxes.json' | relative_url }}?v={{ site.time | date: '%s' }}" data-base="{{ '/' | relative_url }}">
  <div class="vv-controls iv-controls">
    <div class="vv-field iv-field-source">
      <label for="iv-source">Damage source</label>
      <select id="iv-source" disabled><option>Loading sources…</option></select>
    </div>
    <div class="vv-field iv-field-armor">
      <label for="iv-armor">Armor or helmet</label>
      <select id="iv-armor" disabled><option>…</option></select>
    </div>
    <div class="vv-field vv-field-mode iv-field-mode">
      <span class="vv-label" id="iv-mode-label">Colour by</span>
      <div class="wd-segmented vv-mode iv-mode" id="iv-mode" role="radiogroup" aria-labelledby="iv-mode-label">
        <button type="button" role="radio" value="zone" aria-checked="true">Hit location</button>
        <button type="button" role="radio" value="mult" aria-checked="false" tabindex="-1">Source multiplier</button>
      </div>
    </div>
  </div>
  <div class="vv-layout">
    <div class="vv-stage" id="iv-stage">
      <div class="vv-box iv-box">
        <model-viewer id="iv-model" class="vv-model" loading="lazy" reveal="auto" poster="{{ '/assets/images/vehicle-viewer-poster.svg' | relative_url }}" camera-controls touch-action="pan-y" interaction-prompt="none" shadow-intensity="0" exposure="1.1" camera-orbit="25deg 80deg auto" alt="Physics-asset bodies of the player character, coloured by hit location"></model-viewer>
        <p class="vv-status" id="iv-status" role="status"></p>
        <div class="vv-fallback" id="iv-fallback" hidden></div>
      </div>
      <div class="vv-notes" id="iv-notes" role="note" hidden></div>
      <div class="vv-stage-bar">
        <span class="vv-checks"><label class="vv-check"><input type="checkbox" id="iv-xray" checked> See-through selection</label></span>
        <span class="vv-hint">Drag to turn, scroll or pinch to zoom, click a body part to inspect it. While a part is selected, the rest turns see-through: click empty space or press Esc to clear. Every part is also in the list below.</span>
      </div>
    </div>
    <aside class="vv-panel" id="iv-panel" aria-label="Selected body part">
      <div id="iv-panel-body" aria-live="polite">
        <h2 class="vv-panel-title no_anchor is-empty">No body part selected</h2>
        <p class="vv-panel-empty">Click a part of the model, or pick a bone from the list below.</p>
      </div>
    </aside>
  </div>
  <div class="vv-legend" id="iv-legend"></div>
  <div class="iv-cards">
    <section class="iv-card" id="iv-source-card" aria-labelledby="iv-source-title">
      <h2 class="iv-card-title no_anchor" id="iv-source-title">Damage source</h2>
      <div id="iv-source-body"></div>
    </section>
    <section class="iv-card" id="iv-armor-card" aria-labelledby="iv-armor-title">
      <h2 class="iv-card-title no_anchor" id="iv-armor-title">Armor or helmet</h2>
      <div id="iv-armor-body"></div>
    </section>
  </div>
  <h2 class="vv-slots-title no_anchor">Bones</h2>
  <ul class="vv-slots iv-bones" id="iv-bones" aria-label="Bones"></ul>
  <section class="iv-card iv-untraced" id="iv-untraced" aria-labelledby="iv-untraced-title" hidden>
    <h2 class="iv-card-title no_anchor" id="iv-untraced-title">Not traced</h2>
    <p class="iv-card-lead">What this page shows but the game code behind it hasn't been followed, so it rests on the data alone:</p>
    <ul class="iv-untraced-list" id="iv-untraced-list"></ul>
    <div id="iv-assumptions"></div>
  </section>
</div>

<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@4.3.1/dist/model-viewer.min.js" integrity="sha384-cprcVQt7wbUl0xngF3PGP6yBB7n4/t+4AoAMG9biiMCGFiWOdzUH10Ie2COTqFNW" crossorigin="anonymous" onerror="document.documentElement.classList.add('iv-mv-failed')"></script>
<script src="{{ '/assets/js/infantry-viewer.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>

## How this works

- **Bodies, not the render mesh.** The model is the player's physics asset: one untextured collision body per bone, placed in the reference pose. Each body is named, and its material named, after its bone. Six bodies (lower arms, calves and thighs) are tapered capsules; whether Chaos builds query shapes from tapered capsules is unverified, so how closely hits follow those six shapes is too.
- **A bone picks a hit location.** The hit-location asset maps 22 skeleton bones to 12 hit locations ([Game Mechanics](Wardogs_GameMechanics_v2.md#2b-hit-locations-da_globaldamage_hitlocations_player) §2b). The game matches the hit bone's name exactly (`0x6BB8D00`): no walk up to parent bones, and a bone that isn't in the map gives no hit location. `spine_01` and `spine_02` are mapped but have no body, so a live player is never hit there. The asset's `DamageImpactRemap` (`spine_01` to `pelvis`, `spine_05` to `spine_04`) is read for animation and ragdoll only (`0x6BB8D40`), not for damage: `spine_05` counts as the upper torso.
- **The hit location picks a multiplier.** The hit-location rule multiplies the running damage by the `Universal` row's value for the hit location times the value in the row named by the hit's weapon or damage-type tag, or by that tag's parent ([Damage Pipeline](Wardogs_DamagePipeline_v2.md#71-b_bonedamagemodifiers_c-entries-5-7-10) §7.1). The values are in [§8.1](Wardogs_DamagePipeline_v2.md#81-bonedamagemodifiers-hit-location-table). An assault-rifle headshot gets 1.0 × 2.35 = ×2.35.
- **Not every source uses it.** A source that no hit-location entry selects, or one the rule exempts (drone explosives), has the same factor on every body part. An explosion's damage is worked out for each body it hits, with that body's hit location, so a blast varies by hit location wherever its data does. The viewer follows each source's data, shows the uniform ones as uniform and says why.
- **Armor and helmets cover hit locations.** An item takes part only in hits on the hit locations it covers ([Damage Pipeline](Wardogs_DamagePipeline_v2.md#76-the-bullet-event) §7.6). Bullets then meet it through ammo-type effectiveness ([§7.3](Wardogs_DamagePipeline_v2.md#73-b_ammotypeeffectiveness_c-entries-138141)); explosive blunt and melee hits through armor durability, a cut by its reduction percentage ([§7.5](Wardogs_DamagePipeline_v2.md#75-wddamagemodificationoperation_playerarmordurability-entries-142144)). The armor card lists the entries for the selected source. A helmet adds its own single body on `head` (Mutable merges it into the character), which is still the Head hit location; the merge rule isn't traced, and the model shows the character's bodies only.
- **What isn't traced is labelled.** Steps the data shows but whose game code hasn't been followed carry a "not traced" tag, on the model's panel and in the list under the viewer.

<div class="vv-nojs" markdown="1">

## Hitbox tables

The viewer needs JavaScript; these are the same data as tables, from `python _tools/infantry_tables.py` ([Damage Pipeline](Wardogs_DamagePipeline_v2.md#81-bonedamagemodifiers-hit-location-table) §8.1, [Game Mechanics](Wardogs_GameMechanics_v2.md#2b-hit-locations-da_globaldamage_hitlocations_player) §2b).

### Hit locations

Each hit location, the bones that map to it, its `Universal` multiplier and the items that cover it.

<!-- infantry_tables --zones -->
| Hit location (`Meta.Damage.HitLocation.Infantry.*`) | Bones | `Universal` | Covered by |
|---|---|---:|---|
| `Head` | `head` | 1 | HeavyHelmet, LightHelmet, MediumHelmet, PilotHelmet, SuperHeavyHelmet, TankHelmet |
| `Neck` | `neck_01` | 0.75 | HeavyHelmet, SuperHeavyHelmet, TankHelmet |
| `Torso.Upper` | `clavicle_l`, `clavicle_r`, `spine_05` | 1.1 | HeavyArmor, LightArmor, MediumArmor, SuperHeavyArmor |
| `Torso.Middle` | `spine_04` | 1 | HeavyArmor, LightArmor, MediumArmor, SuperHeavyArmor |
| `Torso.Lower` | `spine_03`, `spine_02`, `spine_01` | 0.95 | HeavyArmor, LightArmor, MediumArmor, SuperHeavyArmor |
| `Pelvis` | `pelvis` | 0.9 | SuperHeavyArmor |
| `Arm.Upper` | `upperarm_l`, `upperarm_r` | 0.6 | SuperHeavyArmor |
| `Arm.Lower` | `lowerarm_l`, `lowerarm_r` | 0.5 | — |
| `Arm.Hand` | `hand_l`, `hand_r` | 0.3 | — |
| `Leg.Thigh` | `thigh_l`, `thigh_r` | 0.6 | — |
| `Leg.Calf` | `calf_l`, `calf_r` | 0.5 | — |
| `Leg.Foot` | `foot_l`, `foot_r` | 0.3 | — |
<!-- /infantry_tables -->

### Bones

Each mapped bone, its hit location, its `DamageImpactRemap` target and whether the physics asset gives it a body.

<!-- infantry_tables --bones -->
| Bone | Hit location | `DamageImpactRemap` (animation and ragdoll only) | Physics body |
|---|---|---|---|
| `head` | `Head` | — | yes |
| `neck_01` | `Neck` | — | yes |
| `clavicle_l` | `Torso.Upper` | — | yes |
| `clavicle_r` | `Torso.Upper` | — | yes |
| `spine_05` | `Torso.Upper` | `spine_04` | yes |
| `spine_04` | `Torso.Middle` | — | yes |
| `spine_03` | `Torso.Lower` | — | yes |
| `spine_02` | `Torso.Lower` | — | **no** |
| `spine_01` | `Torso.Lower` | `pelvis` | **no** |
| `upperarm_l` | `Arm.Upper` | — | yes |
| `upperarm_r` | `Arm.Upper` | — | yes |
| `lowerarm_l` | `Arm.Lower` | — | yes |
| `lowerarm_r` | `Arm.Lower` | — | yes |
| `hand_l` | `Arm.Hand` | — | yes |
| `hand_r` | `Arm.Hand` | — | yes |
| `pelvis` | `Pelvis` | — | yes |
| `thigh_l` | `Leg.Thigh` | — | yes |
| `thigh_r` | `Leg.Thigh` | — | yes |
| `calf_l` | `Leg.Calf` | — | yes |
| `calf_r` | `Leg.Calf` | — | yes |
| `foot_l` | `Leg.Foot` | — | yes |
| `foot_r` | `Leg.Foot` | — | yes |
<!-- /infantry_tables -->

### Multipliers by row

The hit-location factor (`Universal` × row) for every row of the bone table.

<!-- infantry_tables --multipliers -->
| Row (`Meta.Damage.` omitted) | Head | Neck | Torso.Upper | Torso.Middle | Torso.Lower | Pelvis | Arm.Upper | Arm.Lower | Arm.Hand | Leg.Thigh | Leg.Calf | Leg.Foot |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `Universal` | 1 | 0.75 | 1.1 | 1 | 0.95 | 0.9 | 0.6 | 0.5 | 0.3 | 0.6 | 0.5 | 0.3 |
| `Weapon.AR` | 2.35 | 1.76 | 0.974 | 0.97 | 0.921 | 0.9 | 0.54 | 0.45 | 0.27 | 0.54 | 0.45 | 0.27 |
| `Weapon.SMG` | 2.1 | 1.58 | 1.16 | 1.05 | 0.997 | 0.945 | 0.78 | 0.65 | 0.39 | 0.78 | 0.65 | 0.39 |
| `Weapon.LMG` | 2.35 | 1.76 | 0.974 | 0.97 | 0.921 | 0.9 | 0.54 | 0.45 | 0.27 | 0.54 | 0.45 | 0.27 |
| `Weapon.Shotgun` | 1.5 | 1.12 | 0.99 | 0.9 | 0.855 | 0.81 | 0.63 | 0.525 | 0.315 | 0.63 | 0.525 | 0.315 |
| `Weapon.DMR` | 2.45 | 1.84 | 1.18 | 1.18 | 1.18 | 1.12 | 0.75 | 0.625 | 0.375 | 0.75 | 0.625 | 0.375 |
| `Weapon.Sniper` | 4.27 | 3.2 | 2.64 | 1.93 | 1.84 | 1.56 | 0.9 | 0.75 | 0.45 | 0.9 | 0.75 | 0.45 |
| `Weapon.Pistol` | 2.1 | 1.58 | 1.16 | 1.05 | 0.997 | 0.945 | 0.78 | 0.65 | 0.39 | 0.78 | 0.65 | 0.39 |
| `DamageType.Melee` | 1.5 | 1.12 | 1.1 | 1 | 0.95 | 0.9 | 0.72 | 0.6 | 0.36 | 0.72 | 0.6 | 0.36 |
| `Weapon.CombatBow` | 2.3 | 1.72 | 2.28 | 1.96 | 1.42 | 0.9 | 0.48 | 0.4 | 0.24 | 0.48 | 0.4 | 0.24 |
| `Weapon.Launcher` | 1.5 | 1.12 | 1.1 | 0.6 | 0.57 | 0.54 | 0.48 | 0.4 | 0.24 | 0.48 | 0.4 | 0.24 |
| `Weapon.Vehicle.Turret.Minigun` | 1.25 | 0.735 | 0.627 | 0.62 | 0.617 | 0.423 | 0.282 | 0.235 | 0.141 | 0.282 | 0.235 | 0.141 |
| `Weapon.Vehicle.Turret.MachineGun` | 2.35 | 1.76 | 1.1 | 1 | 0.95 | 0.9 | 0.54 | 0.45 | 0.27 | 0.54 | 0.45 | 0.27 |
| `Weapon.Vehicle.Cannon` | 1 | 0.75 | 0.66 | 0.6 | 0.57 | 0.54 | 0.18 | 0.15 | 0.09 | 0.18 | 0.15 | 0.09 |
| `Weapon.Vehicle.Turret.Artillery` | 2.35 | 1.76 | 0.974 | 0.97 | 0.921 | 0.9 | 0.54 | 0.45 | 0.27 | 0.54 | 0.45 | 0.27 |
| `Weapon.Vehicle.Turret.Heavy` | 2.35 | 1.76 | 0.974 | 0.97 | 0.921 | 0.9 | 0.54 | 0.45 | 0.27 | 0.54 | 0.45 | 0.27 |
| `Weapon.Vehicle.HelicopterCannon` | 3.2 | 2.4 | 1.98 | 1.8 | 1.71 | 1.17 | 0.72 | 0.6 | 0.36 | 0.72 | 0.6 | 0.36 |
| `Weapon.Vehicle.HelicopterRocket` | 1.5 | 1.12 | 1.1 | 0.6 | 0.57 | 0.54 | 0.48 | 0.4 | 0.24 | 0.48 | 0.4 | 0.24 |
| `Weapon.Vehicle.Turret.STN_06` | 2.2 | 1.65 | 1.32 | 1 | 0.95 | 0.9 | 0.6 | 0.5 | 0.3 | 0.6 | 0.5 | 0.3 |
| `Weapon.HMG.MWSY_001` | 2.2 | 1.65 | 1.32 | 1 | 0.95 | 0.9 | 0.6 | 0.5 | 0.3 | 0.6 | 0.5 | 0.3 |
<!-- /infantry_tables -->

### Damage sources

Every source of character damage: the rule entries it meets, whether the hit location applies, and the armor entries.

<!-- infantry_tables --sources -->
| Category | Source | Damage tags | Hit location matters (direct) | Rule entries | Armor entries | Blast entries | Not traced |
|---|---|---|---|---|---|---|---|
| Bullets | A91 | `Bullet.556mm` | yes (`Weapon.AR` row) | 5, 6, 38, 145 | 138, 140 | — | — |
| Bullets | TAR21 | `Bullet.556mm` | yes (`Weapon.AR` row) | 5, 6, 38, 145 | 138, 140 | — | — |
| Bullets | WEPN_033 | `Bullet.556mm` | yes (`Weapon.AR` row) | 5, 6, 38, 145 | 138, 140 | — | — |
| Bullets | AK74M | `Bullet.545mm` | yes (`Weapon.AR` row) | 5, 6, 46, 145 | 138, 140 | — | — |
| Bullets | WEPN_030 | `Bullet.308Win` | yes (`Weapon.AR` row) | 5, 6, 76, 145 | 138, 140 | — | — |
| Bullets | WEPN_029 | `Bullet.556mm` | yes (`Weapon.AR` row) | 5, 6, 145 | 138, 140 | — | — |
| Bullets | KH2002 | `Bullet.556mm` | yes (`Weapon.AR` row) | 5, 6, 36, 145 | 138, 140 | — | — |
| Bullets | M4 | `Bullet.556mm` | yes (`Weapon.AR` row) | 5, 6, 39, 145 | 138, 140 | — | — |
| Bullets | WEPN_037 | `Bullet.762mm` | yes (`Weapon.AR` row) | 5, 6, 145 | 138, 140 | — | — |
| Bullets | RFB | `Bullet.308Win` | yes (`Weapon.DMR` row) | 5, 6, 74, 145 | 138, 140 | — | — |
| Bullets | SKS | `Bullet.762mm` | yes (`Weapon.DMR` row) | 5, 6, 61, 145 | 138, 140 | — | — |
| Bullets | SVDM | `Bullet.762x54mm` | yes (`Weapon.DMR` row) | 5, 6, 69, 145 | 138, 140 | — | — |
| Bullets | WEPN_034 | `Bullet.308Win` | yes (`Weapon.DMR` row) | 5, 6, 145 | 138, 140 | — | — |
| Bullets | LMG_02 | `Bullet.762x54mm` | yes (`Weapon.LMG` row) | 5, 6, 68, 145 | 138, 140 | — | — |
| Bullets | M249 | `Bullet.556mm` | yes (`Weapon.LMG` row) | 5, 6, 40, 145 | 138, 140 | — | — |
| Bullets | WEPN_036 | `Bullet.308Win` | yes (`Weapon.LMG` row) | 5, 6, 145 | 138, 140 | — | — |
| Bullets | WEPN_027 | `Bullet.50AE` | yes (`Weapon.Pistol` row) | 5, 6, 145 | 138, 140 | — | — |
| Bullets | Glock17 | `Bullet.9mm` | yes (`Weapon.Pistol` row) | 5, 6, 51, 145 | 138, 140 | — | — |
| Bullets | WEPN_032 | `Bullet.9mm` | yes (`Weapon.Pistol` row) | 5, 6, 51, 145 | 138, 140 | — | — |
| Bullets | Judge | `Bullet.45Colt` | yes (`Weapon.Pistol` row) | 5, 6, 57, 145 | 138, 140 | — | — |
| Bullets | WEPN_026 | `Bullet.45ACP` | yes (`Weapon.Pistol` row) | 5, 6, 97, 145 | 138, 140 | — | — |
| Bullets | WEPN_028 | `Bullet.9mm` | yes (`Weapon.SMG` row) | 5, 6, 145 | 138, 140 | — | — |
| Bullets | MP9 | `Bullet.9mm` | yes (`Weapon.SMG` row) | 5, 6, 52, 145 | 138, 140 | — | — |
| Bullets | SMG_03 | `Bullet.9mm` | yes (`Weapon.SMG` row) | 5, 6, 53, 145 | 138, 140 | — | — |
| Bullets | Vector | `Bullet.45ACP` | yes (`Weapon.SMG` row) | 5, 6, 96, 145 | 138, 140 | — | — |
| Bullets | WEPN_031 | `Bullet.9mm` | yes (`Weapon.SMG` row) | 5, 6, 145 | 138, 140 | — | — |
| Bullets | M500 | `Bullet.12g.7mmBuckshot` | yes (`Weapon.Shotgun` row) | 5, 6, 81, 91, 145 | 82, 83, 84, 138, 140 | — | — |
| Bullets | M500 (12g.RifledSlug) | `Bullet.12g.RifledSlug` | yes (`Weapon.Shotgun` row) | 5, 6, 86, 91, 145 | 87, 88, 89, 138, 140 | — | caliber-parent-match |
| Bullets | MP43 | `Bullet.12g.7mmBuckshot` | yes (`Weapon.Shotgun` row) | 5, 6, 81, 91, 145 | 82, 83, 84, 138, 140 | — | — |
| Bullets | MP43 (12g.RifledSlug) | `Bullet.12g.RifledSlug` | yes (`Weapon.Shotgun` row) | 5, 6, 86, 91, 145 | 87, 88, 89, 138, 140 | — | caliber-parent-match |
| Bullets | MK22 | `Bullet.308Win` | yes (`Weapon.Sniper` row) | 5, 6, 75, 145 | 138, 140 | — | — |
| Bullets | SR_04 | `Bullet.50Cal` | yes (`Weapon.Sniper` row) | 5, 6, 124, 125, 126, 127, 145 | 128, 129, 130, 131, 138, 140 | — | — |
| Bullets | WEPN_017 | `Bullet.762x54mm` | yes (`Weapon.Sniper` row) | 5, 6, 67, 145 | 138, 140 | — | — |
| Bullets | SV98 | `Bullet.762x54mm` | yes (`Weapon.Sniper` row) | 5, 6, 66, 145 | 138, 140 | — | — |
| Bullets | WEPN_035 | `Bullet.556mm` | yes (`Weapon.Sniper` row) | 5, 6, 41, 145 | 138, 140 | — | — |
| Bullets | TNK 01 MachineGun (308Win) | `Bullet.308Win` | yes (`Weapon.Vehicle.Turret.MachineGun` row) | 5, 6, 145 | 138, 140 | — | vehicle-weapon-tag |
| Bullets | ROT 03 AttachedMachineGuns (308Win) | `Bullet.308Win` | yes (`Weapon.Vehicle.Turret.Minigun` row) | 5, 6, 145 | 138, 140 | — | vehicle-weapon-tag |
| Bullets | ROT 04 MountedMachineGun (308Win) +1 more | `Bullet.308Win` | yes (`Weapon.Vehicle.Turret.Minigun` row) | 5, 6, 145 | 138, 140 | — | vehicle-weapon-tag |
| Bullets | WHL 05 RingMinigun (308Win) | `Bullet.308Win` | yes (`Weapon.Vehicle.Turret.Minigun` row) | 5, 6, 145 | 138, 140 | — | vehicle-weapon-tag |
| Bullets | TNK 04 MountedMachineGun (50Cal) +1 more | `Bullet.50Cal` | yes (`Weapon.HMG.MWSY_001` row) | 5, 6, 124, 125, 126, 127, 145 | 128, 129, 130, 131, 138, 140 | — | vehicle-weapon-tag |
| Bullets | STN 06 MountedMachineGun (50Cal) | `Bullet.50Cal` | yes (`Weapon.Vehicle.Turret.STN_06` row) | 5, 6, 124, 125, 126, 127, 145 | 128, 129, 130, 131, 138, 140 | — | vehicle-weapon-tag |
| Bullets | TNK 01 Heavy MountedMachineGun (556mm) +3 more | `Bullet.556mm` | yes (`Weapon.LMG` row) | 5, 6, 40, 145 | 138, 140 | — | vehicle-weapon-tag |
| Bullets | TNK 04 MachineGun (762x54mm) | `Bullet.762x54mm` | yes (`Weapon.Vehicle.Turret.MachineGun` row) | 5, 6, 145 | 138, 140 | — | vehicle-weapon-tag |
| Bullets | CombatBow (Arrow) | `Bullet.Arrow` | yes (`Weapon.CombatBow` row) | 5, 6, 25, 145 | 26, 27, 28, 29, 30, 31, 138, 140 | — | — |
| Explosives and launchers | CGM4 | `Explosive.Rocket.84mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (`Weapon.Launcher` row) | 7 | 102, 103, 104, 105, 142, 143 | 102, 103, 104, 105, 113, 114 | armor-hook-paths, exploding-hit, radial-amount, radial-context, radial-split |
| Explosives and launchers | CGM4 (84mm.TVGuided) | `Explosive.Rocket.60mm` | no | — | 102, 103, 104, 105 | 102, 103, 104, 105 | armor-hook-paths, caliber-parent-match, exploding-hit, radial-amount, radial-context, radial-split |
| Explosives and launchers | Launcher_04 | `Explosive.Rocket.72mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (`Weapon.Launcher` row) | 7 | 102, 103, 104, 105, 142, 143 | 102, 103, 104, 105 | armor-hook-paths, exploding-hit, radial-amount, radial-context, radial-split |
| Explosives and launchers | MMGL | `Explosive.Grenade.40mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (`Weapon.Launcher` row) | 7 | 105, 142, 143 | 105, 115 | armor-hook-paths, exploding-hit, radial-amount, radial-context, radial-split |
| Explosives and launchers | RPG7 | `Explosive.Rocket.93mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (`Weapon.Launcher` row) | 7 | 102, 103, 104, 105, 142, 143 | 102, 103, 104, 105, 112 | armor-hook-paths, exploding-hit, radial-amount, radial-context, radial-split |
| Explosives and launchers | TNK 01 Heavy (120x570mm) | `Explosive.Rocket.120mm` | no | — | 102, 103, 104, 105 | 102, 103, 104, 105, 111 | armor-hook-paths, exploding-hit, radial-amount, radial-context, radial-split, vehicle-weapon-tag |
| Explosives and launchers | STN 03 Heavy MainBarrel (120x800mm.Standard) | `Explosive.Rocket.120x800mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (W = 1) | 7 | 102, 103, 104, 105, 142, 143 | 102, 103, 104, 105 | armor-hook-paths, caliber-parent-match, exploding-hit, radial-amount, radial-context, radial-split, vehicle-weapon-tag |
| Explosives and launchers | ROT 02 Weapon 122mm (122mm) | `Explosive.Rocket.122mm` | no | 110 | 102, 103, 104, 105 | 102, 103, 104, 105, 110 | armor-hook-paths, exploding-hit, radial-amount, radial-context, radial-split, vehicle-weapon-tag |
| Explosives and launchers | ROT 03 Weapon 122mm (122mm) | `Explosive.Rocket.122mm` | no | 110 | 102, 103, 104, 105 | 102, 103, 104, 105, 110 | armor-hook-paths, exploding-hit, radial-amount, radial-context, radial-split, vehicle-weapon-tag |
| Explosives and launchers | ROT 02 Weapon 122mm (122mm.Havoc) | `Explosive.Rocket.122mm` | no | 110 | 102, 103, 104, 105 | 102, 103, 104, 105, 110 | armor-hook-paths, caliber-parent-match, exploding-hit, radial-amount, radial-context, radial-split, vehicle-weapon-tag |
| Explosives and launchers | ROT 03 Weapon 122mm (122mm.Havoc) | `Explosive.Rocket.122mm` | no | 110 | 102, 103, 104, 105 | 102, 103, 104, 105, 110 | armor-hook-paths, caliber-parent-match, exploding-hit, radial-amount, radial-context, radial-split, vehicle-weapon-tag |
| Explosives and launchers | TNK 04 (125x570mm) | `Explosive.Rocket.125mm` | no | — | 102, 103, 104, 105 | 102, 103, 104, 105, 109 | armor-hook-paths, exploding-hit, radial-amount, radial-context, radial-split, vehicle-weapon-tag |
| Explosives and launchers | TNK 01 Artillery (155mm.Expensive) | `Explosive.Rocket.155mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (`Weapon.Vehicle.Turret.Artillery` row) | 7 | 102, 103, 104, 105, 142, 143 | 102, 103, 104, 105, 108 | armor-hook-paths, caliber-parent-match, exploding-hit, radial-amount, radial-context, radial-split, vehicle-weapon-tag |
| Explosives and launchers | TNK 01 Artillery (155mm.Standard) | `Explosive.Rocket.155mm` | no | — | 102, 103, 104, 105 | 102, 103, 104, 105, 108 | armor-hook-paths, caliber-parent-match, exploding-hit, radial-amount, radial-context, radial-split, vehicle-weapon-tag |
| Explosives and launchers | STN 02 Heavy MainCannon (20x102mm) | `Cannon.20x102mm` | yes (W = 1) | 10, 119 | 139, 141 | — | vehicle-weapon-tag |
| Explosives and launchers | ROT 02 Weapon 30mmCannon (30mm) | `Cannon.30mm` | yes (`Weapon.Vehicle.HelicopterCannon` row) | 10 | 139, 141 | 10, 105, 139, 141 | armor-hook-paths, exploding-hit, radial-amount, radial-context, radial-split, vehicle-weapon-tag |
| Explosives and launchers | TNK 03 (35x228mm) | `Cannon.35x228mm` | yes (`Weapon.Vehicle.Cannon` row) | 10, 118 | 139, 141 | — | vehicle-weapon-tag |
| Explosives and launchers | GrenadeLauncher (40mm) | `Explosive.Grenade.40mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (W = 1) | 7 | 105, 142, 143 | 105, 115 | armor-hook-paths, exploding-hit, radial-amount, radial-context, radial-split, underbarrel-weapon-tag |
| Explosives and launchers | STN 01 Heavy MountedMachineGun (72mm) | `Explosive.Rocket.72mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (W = 1) | 7 | 102, 103, 104, 105, 142, 143 | 102, 103, 104, 105 | armor-hook-paths, exploding-hit, radial-amount, radial-context, radial-split, vehicle-weapon-tag |
| Explosives and launchers | CombatBow (Arrow.Explosive) | `Bullet.Arrow.Explosive` | yes (`Weapon.CombatBow` row) | 5, 6, 25, 145 | 26, 27, 28, 29, 30, 31, 138, 140 | 5, 6, 25, 26, 27, 28, 29, 30, 31, 105, 138, 140, 145 | armor-hook-paths, caliber-parent-match, exploding-hit, radial-amount, radial-context, radial-split |
| Explosives and launchers | STN 05 Heavy MainBarrel (DroneProjectile) | `Explosive.Drone`, `Kinetic.Impact.ExplosiveBlunt` | no | 7, 117 | 105, 142, 143 | 105 | armor-hook-paths, exploding-hit, radial-amount, radial-context, radial-split, vehicle-weapon-tag |
| Explosives and launchers | M67 frag grenade | `Explosive.Grenade` | no | — | 105 | — | explosive-actors, armor-hook-paths |
| Explosives and launchers | C4 | `Explosive.Utility.C4` | no | 116 | 105 | — | explosive-actors, armor-hook-paths |
| Explosives and launchers | AT mine | `Explosive.Utility.ATMine` | no | — | 105 | — | explosive-actors, armor-hook-paths |
| Explosives and launchers | Claymore | `Explosive.Utility.Claymore` | no | — | 105 | — | explosive-actors, armor-hook-paths |
| Explosives and launchers | IED | `Explosive.Utility.IED` | no | — | 105 | — | explosive-actors, armor-hook-paths |
| Explosives and launchers | Molotov | `Explosive.Utility.Molotov` | no | — | 105, 106 | — | explosive-actors, armor-hook-paths |
| Explosives and launchers | CGM4 back-blast | `DamageType.BackBlast` | no | — | — | — | backblast, armor-hook-paths |
| Explosives and launchers | Launcher_04 back-blast | `DamageType.BackBlast` | no | — | — | — | backblast, armor-hook-paths |
| Explosives and launchers | RPG7 back-blast | `DamageType.BackBlast` | no | — | — | — | backblast, armor-hook-paths |
| Explosives and launchers | Vehicle explosion (occupants) | `Explosive.VehicleExplosion`, `DamageType.Explosive` | no | — | 105 | — | occupant-damage, armor-hook-paths |
| Other | Fists | `Utility.Fists`, `DamageType.Melee` | no | — | 144 | — | melee-path, armor-hook-paths |
| Other | LargeHammer | `Utility.LargeHammer`, `DamageType.Melee` | no | — | 144 | — | melee-path, armor-hook-paths |
| Other | MediumHammer | `Utility.MediumHammer`, `DamageType.Melee` | no | — | 144 | — | melee-path, armor-hook-paths |
| Other | SmallHammer | `Utility.SmallHammer`, `DamageType.Melee` | no | — | 144 | — | melee-path, armor-hook-paths |
| Other | Crowbar | `Utility.Crowbar`, `DamageType.Melee` | no | — | 144 | — | melee-path, armor-hook-paths |
| Other | HeavyDrill_RepairTool | `Utility.LargeDrill`, `DamageType.Melee` | no | — | 144 | — | melee-path, armor-hook-paths |
| Other | LightDrill_RepairTool | `Utility.MediumDrill`, `DamageType.Melee` | no | — | 144 | — | melee-path, armor-hook-paths |
| Other | Thrown object contact | `Kinetic.Impact.Throwable`, `DamageType.Impact` | no | — | — | — | impact-amount, armor-hook-paths |
| Other | Actor or vehicle impact | `DamageType.Impact` | no | — | — | — | impact-amount, armor-hook-paths |
<!-- /infantry_tables -->

### Explosive rounds

Launcher, cannon and shell rounds: direct-hit and blast data.

<!-- infantry_tables --explosives -->
| Source | Projectile | Source tag | Blunt S (before arming) | Direct S | Arming delay (s) | `ExplosiveRadius` | `EffectiveExplosiveRadius` | `ExplosiveDamageFallOff` | `MinimumExplosiveDamage` | Blast bone factor | Inner: factor (entries) | Outer: factor (entries) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| CGM4 | `84mm` | `Explosive.Rocket.84mm` | 120 | 100 | 0.03 | 1000 | 400 | 1 | — | no | ×1.01 (114) | ×0.5 (113) |
| CGM4 (84mm.TVGuided) | `84mm.TVGuided` | `Explosive.Rocket.60mm` | — | 100 | — | 1000 | 400 | 0.5 | — | no | ×1 (—) | ×1 (—) |
| Launcher_04 | `72mm` | `Explosive.Rocket.72mm` | 120 | 200 | 0.13 | 1080 | 200 | 0.8 | — | no | ×1 (—) | ×1 (—) |
| MMGL | `40mm` | `Explosive.Grenade.40mm` | 80 | 100 | 0.07 | 1000 | 250 | 1 | — | no | ×1 (—) | ×0.5 (115) |
| RPG7 | `93mm` | `Explosive.Rocket.93mm` | 120 | 110 | 0.099 | 1200 | 250 | 0.9 | — | no | ×1 (—) | ×0.5 (112) |
| TNK 01 Heavy (120x570mm) | `120x570mm` | `Explosive.Rocket.120mm` | — | 150 | — | 750 | 420 | 0.3 | 30 | no | ×1 (—) | ×0.5 (111) |
| STN 03 Heavy MainBarrel (120x800mm.Standard) | `120x800mm.Standard` | `Explosive.Rocket.120x800mm` | 120 | 120 | 0.1 | 1000 | 500 | 0.45 | 15 | no | ×1 (—) | ×1 (—) |
| ROT 02 Weapon 122mm (122mm) | `122mm` | `Explosive.Rocket.122mm` | — | 100 | — | 600 | 200 | 1 | 10 | no | ×0.55 (110) | ×0.55 (110) |
| ROT 03 Weapon 122mm (122mm) | `122mm` | `Explosive.Rocket.122mm` | — | 100 | — | 600 | 200 | 1 | 10 | no | ×0.55 (110) | ×0.55 (110) |
| ROT 02 Weapon 122mm (122mm.Havoc) | `122mm.Havoc` | `Explosive.Rocket.122mm` | — | 300 | — | 300 | 600 | 0.6 | — | no | ×0.55 (110) | ×0.55 (110) |
| ROT 03 Weapon 122mm (122mm.Havoc) | `122mm.Havoc` | `Explosive.Rocket.122mm` | — | 300 | — | 300 | 600 | 0.6 | — | no | ×0.55 (110) | ×0.55 (110) |
| TNK 04 (125x570mm) | `125x570mm` | `Explosive.Rocket.125mm` | — | 150 | — | 750 | 420 | 0.3 | 30 | no | ×1 (—) | ×0.5 (109) |
| TNK 01 Artillery (155mm.Expensive) | `155mm.Expensive` | `Explosive.Rocket.155mm` | 100 | 450 | 1.3 | 2000 | 1000 | 0.93 | — | no | ×1 (—) | ×0.45 (108) |
| TNK 01 Artillery (155mm.Standard) | `155mm.Standard` | `Explosive.Rocket.155mm` | — | 450 | — | 2000 | 750 | 0.5 | — | no | ×1 (—) | ×0.45 (108) |
| STN 02 Heavy MainCannon (20x102mm) | `20x102mm` | `Cannon.20x102mm` | — | 60 | — | — | 375 | 0.7 | — | — | — | — |
| ROT 02 Weapon 30mmCannon (30mm) | `30mm` | `Cannon.30mm` | — | 100 | — | 300 | 100 | 1 | 20 | yes (W = 1) | ×1 (10) | ×1 (10) |
| TNK 03 (35x228mm) | `35x228mm` | `Cannon.35x228mm` | — | 60 | — | — | 375 | 0.7 | — | — | — | — |
| GrenadeLauncher (40mm) | `40mm` | `Explosive.Grenade.40mm` | 80 | 100 | 0.07 | 1000 | 250 | 1 | — | no | ×1 (—) | ×0.5 (115) |
| STN 01 Heavy MountedMachineGun (72mm) | `72mm` | `Explosive.Rocket.72mm` | 120 | 200 | 0.13 | 1080 | 200 | 0.8 | — | no | ×1 (—) | ×1 (—) |
| CombatBow (Arrow.Explosive) | `Arrow.Explosive` | `Bullet.Arrow.Explosive` | — | 150 | — | 400 | 200 | 1 | — | yes (W = 1) | ×1 (5) | ×1 (5) |
| STN 05 Heavy MainBarrel (DroneProjectile) | `DroneProjectile` | `Explosive.Drone` | 100 | 120 | 0.1 | 1000 | 500 | 0.45 | 15 | no | ×1 (—) | ×1 (—) |
<!-- /infantry_tables -->

### Armor and helmets

Each item's context tag, durability, reduction and the hit locations it covers.

<!-- infantry_tables --armor -->
| Item | Context tag | Kind | Max durability | `R` (%) | Covered hit locations | Entries (custom in bold) |
|---|---|---|---:|---:|---|---|
| `ID_GhillieArmor` | `Meta.Damage.Armor.Ghillie` | armor | — | 0 (no stages) | — | 21, 83, 89, 133, **138**, **139**, **143**, **144** |
| `ID_GhillieArmorDry` | `Meta.Damage.Armor.Ghillie` | armor | — | 0 (no stages) | — | 21, 83, 89, 133, **138**, **139**, **143**, **144** |
| `ID_GhillieHelmet` | `Meta.Damage.Helmet.Ghillie` | helmet | — | 0 (no stages) | — | 20, 28, 82, 87, 134, **140**, **141**, **142** |
| `ID_GhillieHelmetDry` | `Meta.Damage.Helmet.Ghillie` | helmet | — | 0 (no stages) | — | 20, 28, 82, 87, 134, **140**, **141**, **142** |
| `ID_HeavyArmor` | `Meta.Damage.Armor.Heavy` | armor | 250 | 50 | Torso.Upper, Torso.Middle, Torso.Lower | 21, 26, 83, 89, 104, 128, 133, **138**, **139**, **143**, **144** |
| `ID_HeavyHelmet` | `Meta.Damage.Helmet.Heavy` | helmet | 180 | 50 | Head, Neck | 20, 28, 30, 82, 87, 130, 134, **140**, **141**, **142** |
| `ID_LightArmor` | `Meta.Damage.Armor.Light` | armor | 200 | 30 | Torso.Upper, Torso.Middle, Torso.Lower | 21, 83, 89, 102, 133, **138**, **139**, **143**, **144** |
| `ID_LightHelmet` | `Meta.Damage.Helmet.Light` | helmet | 80 | 30 | Head | 20, 28, 29, 82, 87, 134, **140**, **141**, **142** |
| `ID_MediumArmor` | `Meta.Damage.Armor.Medium` | armor | 220 | 40 | Torso.Upper, Torso.Middle, Torso.Lower | 21, 83, 89, 103, 133, **138**, **139**, **143**, **144** |
| `ID_MediumHelmet` | `Meta.Damage.Helmet.Medium` | helmet | 100 | 40 | Head | 20, 28, 82, 87, 134, **140**, **141**, **142** |
| `ID_PilotHelmet` | `Meta.Damage.Helmet.Pilot` | helmet | 180 | 30 | Head | 20, 28, 82, 87, 134, **140**, **141**, **142** |
| `ID_SuperHeavyArmor` | `Meta.Damage.Armor.SuperHeavy` | armor | 300 | 60 | Torso.Upper, Torso.Middle, Torso.Lower, Pelvis, Arm.Upper | 21, 27, 83, 84, 89, 105, 106, 129, 133, **138**, **139**, **143**, **144** |
| `ID_SuperHeavyHelmet` | `Meta.Damage.Helmet.SuperHeavy` | helmet | 200 | 60 | Head, Neck | 20, 28, 31, 82, 87, 88, 131, 134, 136, **140**, **141**, **142** |
| `ID_TankHelmet` | `Meta.Damage.Helmet.Tank` | helmet | 180 | 55 | Head, Neck | 20, 28, 82, 87, 134, **140**, **141**, **142** |
<!-- /infantry_tables -->

### Traced since the docs

Facts the verifier has traced but the reference pages don't yet state, each with its RVAs.

<!-- infantry_tables --verified -->
| Id | Fact (verifier round 6 (doc text pending)) | RVAs |
|---|---|---|
| `hit-location-asset` | The hit-location asset is picked by the target actor's class (ClassToHitLocations). | `0x6F01BB0` |
| `bone-lookup` | The hit location is an exact FName match of the raw FHitResult.BoneName in DamageHitLocations: no parent walk, and an unmapped bone gives an empty tag (no hit location). | `0x6BB8D00` |
| `impact-remap` | DamageImpactRemap is never applied for damage: its reader has 3 callers, all animation or ragdoll. spine_05 is Torso.Upper for damage. | `0x6BB8D40` |
| `physics-asset` | The hit bodies are PA_TPCharacter_Simplified's; all 20 map to a hit location. spine_01 and spine_02 have no body, so a live player never produces them. Mutable adds each helmet's single head body, which maps to Head. | — |
| `radial-hits` | Radial damage: the gathered hits pass the character's IWDDamageable filter (dropped in one seat state, otherwise one hit per component). Each kept hit is its own evaluation, tagged Radius.Inner or .Outer, with that hit's bone as the hit location. | `0x6F06540`, `0x6E6DCC0` |
| `blunt-direct-only` | Kinetic.Impact.ExplosiveBlunt is added only on a projectile's direct-impact path, so entries 7, 117, 142 and 143 never apply to blast damage; entries 102–116 do. | `0x6B725B0` |
| `thrown-contact` | Against a character, the explosive-actor path is the thrown object's contact damage (source Kinetic.Impact.Throwable, DamageType.Impact), applied once per contact on the contacted bone. | `0x6CA8730` |
| `backblast-paths` | On foot, 0x6F042A0 traces the back-blast cone. In a seat, 0x6F06EB0 hits the occupants of the shooter's vehicle with synthetic hits, the shooter included. Only Launcher_04, RPG7 and CGM4 enable back-blast. | `0x6F042A0`, `0x6F06EB0` |
<!-- /infantry_tables -->

### Not traced

What the docs leave open, with what the data shows.

<!-- infantry_tables --not-traced -->
| Id | Open question | What the data says |
|---|---|---|
| `radial-amount` | Blast damage: which DamageValues field is the starting amount, the falloff arithmetic, and which radius separates Meta.Damage.Explosive.Radius.Inner from .Outer. GameMechanics §14 says BaseDamage and ExplosiveRadius feed the Calibre rules and falloff is ExplosiveDamageFallOff, without a formula. | Projectile assets carry BaseDamage, ExplosiveRadius, EffectiveExplosiveRadius, ExplosiveDamageFallOff and on some MinimumExplosiveDamage (values per source). |
| `radial-split` | Which of the character's components the radial gather hits. Known (verifier round 6 (doc text pending)): one hit per component after the IWDDamageable filter 0x6E6DCC0, each hit its own evaluation with its bone's hit location. | No data field describes the gather. |
| `radial-context` | Which tags a blast hit's source context carries besides the source tag and the radius tag (weapon tag, caliber id). The blast factors here use the projectile's source tag, its DamageEntityData.Context and the radius tag, so the bone factor's W is 1 on blast hits. | Entries 108–116 need only the source tag and a radius tag. |
| `exploding-hit` | When a projectile hit is bExploding. §7.6: an exploding hit skips both scales, the armor hook and ModifyDamage on the projectile path; what sets bExploding is not stated, so whether an armed launcher, shell or cannon round ever deals the direct-hit amount is open. | Projectile assets carry bHasArmingDelay and ArmingDelay (seconds of flight time, §7.6). |
| `explosive-actors` | Detonation damage of grenades, C4, mines, claymores, IEDs and the Molotov. Against a character 0x6CA8730 is only the thrown object's contact damage (verifier round 6 (doc text pending)); the detonation's path, amount and tags are not traced. | The items reference actor Blueprints (B_FragGrenade, B_ThrowableC4, B_AT_Mine, B_Claymore, B_Molotov) that are not in the data export, so no damage value is in data/. |
| `armor-hook-paths` | Whether the target hook Auth_GetArmorDamageEvent (§7.6) runs on paths other than the projectile's direct impact (blast, back-blast, melee, actor impact, thrown contact). It decides whether an armor tag reaches entries 102–106 and 138–144. | Armor items list CoveredHitLocations (see armor). |
| `armor-data-rows` | Whether DT_GlobalDamage_ArmorData's rows are evaluated for a character hit. §5's walk for a character starts at Meta.Damage.Infantry and gives one group; the armor rows are keyed by armor tags. | DT_GlobalDamage_ArmorData has rows Meta.Damage.Armor, Meta.Damage.Helmet and the two Ghillie rows. |
| `vehicle-weapon-tag` | Whether a vehicle weapon extension (WE_*) puts its DamageEntityData.Tag into the source context as a weapon item does. §7.6 identifies the weapon tag by value for weapon items; the vehicle rows of BoneDamageModifiers are only reached if it does. | Every WE_* file carries a Meta.Damage.Weapon.* tag (values per source). |
| `underbarrel-weapon-tag` | Which weapon tag an underbarrel grenade launcher shot carries. | GrenadeLauncher.json has no Meta.Damage.Weapon tag; its stats are DA_GrenadeLauncher_Stats. |
| `melee-path` | The melee caller: §1.1 names no melee path, so the event's source (the item's Utility tag, whether Meta.Damage.DamageType.Melee is added), its hit location and the armor hook are not traced. | Melee items carry WDItemExtensionData_CharacterMelee.MeleeActions[].Damage and DamageEntityData.Tag; entry 144 requires Meta.Damage.DamageType.Melee; BoneDamageModifiers has a Meta.Damage.DamageType.Melee row that no bone entry (5, 7, 10) selects for a melee-only source. |
| `impact-amount` | The starting amount of actor impact (0x6E72D90, §1.1) and of a thrown object's contact (0x6CA8730), and what the hitting actor's entity data holds. | No infantry rule entry requires Meta.Damage.DamageType.Impact or Kinetic.Impact.Throwable. |
| `backblast` | Back-blast: the event's source tag and amount, and the hit location of the seated path's synthetic hits. The two paths are known (verifier round 6 (doc text pending)). | Launcher stats carry a BackBlast config (FWDBackBlastConfig) whose field names are hashed in the export and the SDK; no infantry rule entry requires Meta.Damage.DamageType.BackBlast. |
| `occupant-damage` | Damage to vehicle occupants from UWDVehicleOperatorComponent slots 160/161 (§1.1; VehicleDamagePipeline §1): the amount and hit location. | Source tags Meta.Damage.Explosive.VehicleExplosion + DamageType.Explosive, and Meta.Damage.Vehicle + DamageType.Enviroment. |
| `helmet-merge` | The rule by which Mutable merges a helmet's physics asset into the character's. Known (verifier round 6 (doc text pending)): each helmet adds its single head body, which maps to Head. The model shows PA_TPCharacter_Simplified without helmet bodies. | MUT_TP_Character lists five helmet physics assets (PA_Helmet_*), one Sphyl body on head each (assets/models/infantry/player.glb asset.extras.notes; MUT_TP_Character is not in the data/ JSON export). |
| `tapered-capsule-query` | Whether Chaos builds query shapes from tapered-capsule bodies, i.e. whether these six bodies can be hit by a trace at all. | calf_l, calf_r, lowerarm_l, lowerarm_r, thigh_l and thigh_r are TaperedCapsule bodies (QueryAndPhysics) in PA_TPCharacter_Simplified (assets/models/infantry/player.glb asset.extras.bodies[].shapes). |
| `collision-channels` | Which trace channels hit the character's bodies. The CharacterMesh component uses collision profile Custom, whose per-channel responses are native class defaults, not stored in the cooked Blueprint. | CharacterMesh.BodyInstance.CollisionEnabled is QueryOnly (profile Custom); every body is QueryAndPhysics with BodyCollision_Enabled (assets/models/infantry/player.glb asset.extras.notes and node extras). |
| `physical-material` | Data only, no documented use: no doc uses a body's physical material or surface type for infantry damage (VFX uses physical materials for impact effects; VehicleDamagePipeline §3.2 says vehicle hits read neither physical materials nor bone names). | The head body uses PM_Head, the other 19 bodies PM_Body (assets/models/infantry/player.glb asset.extras.bodies[].phys_material; the body export gives SurfaceType17 and SurfaceType3; the PM_* assets are not in the data/ JSON export). |
| `caliber-parent-match` | Whether a weapon whose SupportedCaliber is a parent tag fires the child projectiles: the bow lists Item.Caliber.Arrow (child Arrow.Explosive), the M500 / MP43 Item.Caliber.12g (child 12g.RifledSlug), the artillery Item.Caliber.155mm (155mm.Standard, .Expensive), STN_03 Item.Caliber.120x800mm (120x800mm.Standard), CGM4 Item.Caliber.84mm (child 84mm.TVGuided). How SupportedCaliber is matched is not traced. | No WDProjectileData asset has ProjectileId Item.Caliber.12g, .155mm or .120x800mm; the child ids each have one (Sandbox copies left out). |
<!-- /infantry_tables -->

</div>
