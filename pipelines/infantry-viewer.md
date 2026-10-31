---
title: "Infantry Hitbox Viewer"
redirect_from: ["/infantry-viewer.html", "/infantry-viewer"]
parent: "Interactive Tools"
description: "The player's physics bodies coloured by hit location, multipliers per damage source, armor and helmet coverage"
---

# Infantry Hitbox Viewer

*Data: [`assets/data/infantry-hitboxes.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/infantry-hitboxes.json), built by `python _tools/infantry_tables.py --json`*

The player's physics-asset bodies, coloured by the hit location each body's bone maps to. Pick a damage source to recolour the body by that source's hit-location multiplier, and an armor or helmet to see the hit locations it covers. Pick a body on the model or in the list to see its bone, hit location and multiplier. How it works: [Damage Pipeline](Wardogs_DamagePipeline_v2.md#71-b_bonedamagemodifiers_c-entries-5-7-10) §7.1 (the hit-location rule), [§8.1](Wardogs_DamagePipeline_v2.md#81-bonedamagemodifiers-hit-location-table) (its table) and [§7.5](Wardogs_DamagePipeline_v2.md#75-wddamagemodificationoperation_playerarmordurability-entries-142144) (armor), and [Game Mechanics](../content/Wardogs_GameMechanics_v2.md#2b-hit-locations-da_globaldamage_hitlocations_player) §2b (bones to hit locations).

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

Baseline weapon/projectile pairs use the first supported caliber with projectile data as a modelling choice; not every baseline loading path has been audited. Extra child-caliber pairings are restricted to the [reviewed item/filter associations](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round8-weapon-context.md). A damage calculation for a pair does not by itself prove that a loadout can fire it.

- **Bodies, not the render mesh.** The model shows the baseline `PA_TPCharacter_Simplified` asset: one untextured collision body per bone, placed in the reference pose. Each body is named, and its material named, after its bone. Six bodies (lower arms, calves and thighs) show authored tapered capsules. The native simple-geometry builder instead registers straight capsules with the mean of the scaled/clamped end radii; body/element modes permit queries, while geometry selection and channel filters still apply. See the [native construction trace](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round8-tapered-query.md). This supersedes the model's older embedded unverified-query note.
- **A bone picks a hit location.** The hit-location asset maps 22 skeleton bones to 12 hit locations ([Game Mechanics](../content/Wardogs_GameMechanics_v2.md#2b-hit-locations-da_globaldamage_hitlocations_player) §2b). The game matches the hit bone's name exactly (`0x6BB8D00`): no walk up to parent bones, and a bone that isn't in the map gives no hit location. `spine_01` and `spine_02` are mapped but have no body in this baseline asset; generated runtime assets can differ. The asset's `DamageImpactRemap` (`spine_01` to `pelvis`, `spine_05` to `spine_04`) is read for animation and ragdoll only (`0x6BB8D40`), not for damage: `spine_05` counts as the upper torso.
- **The hit location picks a multiplier.** The hit-location rule multiplies the running damage by the `Universal` row's value for the hit location times the value in the row named by the hit's weapon or damage-type tag, or by that tag's parent ([Damage Pipeline](Wardogs_DamagePipeline_v2.md#71-b_bonedamagemodifiers_c-entries-5-7-10) §7.1). The values are in [§8.1](Wardogs_DamagePipeline_v2.md#81-bonedamagemodifiers-hit-location-table). An assault-rifle headshot gets 1.0 × 2.35 = ×2.35.
- **Not every source uses it.** A source that no hit-location entry selects, or one the rule exempts (drone explosives), has the same factor on every body part. A character explosion normally keeps one hit per component and evaluates it separately. Projectile blasts retain the weapon and caliber context, so a mapped hit bone can use that weapon's row. This assumes valid equipment and the converter's bone-lookup fallback; invalid armor tags can suppress it. The normal setup has one eligible TP mesh component; sampling, visibility, protected-seat rejection and later mutations still determine acceptance. The viewer models one mapped hit, not a guaranteed blast total.
- **Armor coverage depends on the path.** Direct projectiles keep the first covering piece ([Damage Pipeline](Wardogs_DamagePipeline_v2.md#76-the-bullet-event) §7.6). Radial and back-blast armor hooks accept every valid piece without coverage tests. The blast table evaluates each retained armor tag alone at every hit location; combined equipment needs joint evaluation. Melee Blueprints queue Torso armor events but discard the returned copy before health evaluation, leaving no health hit-location tag ([§1.2](Wardogs_DamagePipeline_v2.md#12-blueprint-melee-and-occupant-events)). Mutable selects tagged physics assets by compiled helmet/faction/view conditions, deduplicates them, reuses a sole asset when generated bodies are unmodified, and otherwise builds a combined asset with at most one body setup per bone. Combined-body geometry comes from generated Mutable bodies; the source setup used to create each result bone supplies selected body properties. The normal `CharacterMesh` override defaults to null and its getter uses the assigned mesh's physics asset. Runtime values and later mutations remain unknown; this model shows only `PA_TPCharacter_Simplified`.
- **Blast amount is traced.** Inner hits use `BaseDamage` through `EffectiveExplosiveRadius`; Outer hits fall linearly toward `BaseDamage × (1 − ExplosiveDamageFallOff)` just inside `ExplosiveRadius`, then 0, all floored at `MinimumExplosiveDamage`. Inner takes priority if E > R. Center, Disc and native-default Points modes use distance from the original blast origin to the accepted `ImpactPoint` or synthetic candidate point ([Damage §1.1](Wardogs_DamagePipeline_v2.md#11-callers-and-where-the-result-goes)).
- **What isn't traced is labelled.** Steps the data shows but whose game code hasn't been followed carry a "not traced" tag, on the model's panel and in the list under the viewer.

<div class="vv-nojs" markdown="1">

## Hitbox tables

The viewer needs JavaScript; these are the same data as tables, from `python _tools/infantry_tables.py` ([Damage Pipeline](Wardogs_DamagePipeline_v2.md#81-bonedamagemodifiers-hit-location-table) §8.1, [Game Mechanics](../content/Wardogs_GameMechanics_v2.md#2b-hit-locations-da_globaldamage_hitlocations_player) §2b).

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
| Bullets | M500 (12g.RifledSlug) | `Bullet.12g.RifledSlug` | yes (`Weapon.Shotgun` row) | 5, 6, 86, 91, 145 | 87, 88, 89, 138, 140 | — | — |
| Bullets | MP43 | `Bullet.12g.7mmBuckshot` | yes (`Weapon.Shotgun` row) | 5, 6, 81, 91, 145 | 82, 83, 84, 138, 140 | — | — |
| Bullets | MP43 (12g.RifledSlug) | `Bullet.12g.RifledSlug` | yes (`Weapon.Shotgun` row) | 5, 6, 86, 91, 145 | 87, 88, 89, 138, 140 | — | — |
| Bullets | MK22 | `Bullet.308Win` | yes (`Weapon.Sniper` row) | 5, 6, 75, 145 | 138, 140 | — | — |
| Bullets | SR_04 | `Bullet.50Cal` | yes (`Weapon.Sniper` row) | 5, 6, 124, 125, 126, 127, 145 | 128, 129, 130, 131, 138, 140 | — | — |
| Bullets | WEPN_017 | `Bullet.762x54mm` | yes (`Weapon.Sniper` row) | 5, 6, 67, 145 | 138, 140 | — | — |
| Bullets | SV98 | `Bullet.762x54mm` | yes (`Weapon.Sniper` row) | 5, 6, 66, 145 | 138, 140 | — | — |
| Bullets | WEPN_035 | `Bullet.556mm` | yes (`Weapon.Sniper` row) | 5, 6, 41, 145 | 138, 140 | — | — |
| Bullets | TNK 01 MachineGun (308Win) | `Bullet.308Win` | yes (`Weapon.Vehicle.Turret.MachineGun` row) | 5, 6, 145 | 138, 140 | — | — |
| Bullets | ROT 03 AttachedMachineGuns (308Win) | `Bullet.308Win` | yes (`Weapon.Vehicle.Turret.Minigun` row) | 5, 6, 145 | 138, 140 | — | — |
| Bullets | ROT 04 MountedMachineGun (308Win) +1 more | `Bullet.308Win` | yes (`Weapon.Vehicle.Turret.Minigun` row) | 5, 6, 145 | 138, 140 | — | — |
| Bullets | WHL 05 RingMinigun (308Win) | `Bullet.308Win` | yes (`Weapon.Vehicle.Turret.Minigun` row) | 5, 6, 145 | 138, 140 | — | — |
| Bullets | TNK 04 MountedMachineGun (50Cal) +1 more | `Bullet.50Cal` | yes (`Weapon.HMG.MWSY_001` row) | 5, 6, 124, 125, 126, 127, 145 | 128, 129, 130, 131, 138, 140 | — | — |
| Bullets | STN 06 MountedMachineGun (50Cal) | `Bullet.50Cal` | yes (`Weapon.Vehicle.Turret.STN_06` row) | 5, 6, 124, 125, 126, 127, 145 | 128, 129, 130, 131, 138, 140 | — | — |
| Bullets | TNK 01 Heavy MountedMachineGun (556mm) +3 more | `Bullet.556mm` | yes (`Weapon.LMG` row) | 5, 6, 40, 145 | 138, 140 | — | — |
| Bullets | TNK 04 MachineGun (762x54mm) | `Bullet.762x54mm` | yes (`Weapon.Vehicle.Turret.MachineGun` row) | 5, 6, 145 | 138, 140 | — | — |
| Bullets | CombatBow (Arrow) | `Bullet.Arrow` | yes (`Weapon.CombatBow` row) | 5, 6, 25, 145 | 26, 27, 28, 29, 30, 31, 138, 140 | — | — |
| Explosives and launchers | CGM4 | `Explosive.Rocket.84mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (`Weapon.Launcher` row) | 7 | 102, 103, 104, 105, 142, 143 | 102, 103, 104, 105, 113, 114 | — |
| Explosives and launchers | Launcher_04 | `Explosive.Rocket.72mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (`Weapon.Launcher` row) | 7 | 102, 103, 104, 105, 142, 143 | 102, 103, 104, 105 | — |
| Explosives and launchers | MMGL | `Explosive.Grenade.40mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (`Weapon.Launcher` row) | 7 | 105, 142, 143 | 105, 115 | — |
| Explosives and launchers | RPG7 | `Explosive.Rocket.93mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (`Weapon.Launcher` row) | 7 | 102, 103, 104, 105, 142, 143 | 102, 103, 104, 105, 112 | — |
| Explosives and launchers | TNK 01 Heavy (120x570mm) | `Explosive.Rocket.120mm` | no | — | 102, 103, 104, 105 | 102, 103, 104, 105, 111 | — |
| Explosives and launchers | STN 03 Heavy MainBarrel (120x800mm.Standard) | `Explosive.Rocket.120x800mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (W = 1) | 7 | 102, 103, 104, 105, 142, 143 | 102, 103, 104, 105 | — |
| Explosives and launchers | ROT 02 Weapon 122mm (122mm) | `Explosive.Rocket.122mm` | no | 110 | 102, 103, 104, 105 | 102, 103, 104, 105, 110 | — |
| Explosives and launchers | ROT 03 Weapon 122mm (122mm) | `Explosive.Rocket.122mm` | no | 110 | 102, 103, 104, 105 | 102, 103, 104, 105, 110 | — |
| Explosives and launchers | TNK 04 (125x570mm) | `Explosive.Rocket.125mm` | no | — | 102, 103, 104, 105 | 102, 103, 104, 105, 109 | — |
| Explosives and launchers | TNK 01 Artillery (155mm.Expensive) | `Explosive.Rocket.155mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (`Weapon.Vehicle.Turret.Artillery` row) | 7 | 102, 103, 104, 105, 142, 143 | 102, 103, 104, 105, 108 | — |
| Explosives and launchers | TNK 01 Artillery (155mm.Standard) | `Explosive.Rocket.155mm` | no | — | 102, 103, 104, 105 | 102, 103, 104, 105, 108 | — |
| Explosives and launchers | STN 02 Heavy MainCannon (20x102mm) | `Cannon.20x102mm` | yes (W = 1) | 10, 119 | 139, 141 | — | — |
| Explosives and launchers | ROT 02 Weapon 30mmCannon (30mm) | `Cannon.30mm` | yes (`Weapon.Vehicle.HelicopterCannon` row) | 10 | 139, 141 | 10, 105, 139, 141 | — |
| Explosives and launchers | TNK 03 (35x228mm) | `Cannon.35x228mm` | yes (`Weapon.Vehicle.Cannon` row) | 10, 118 | 139, 141 | — | — |
| Explosives and launchers | GrenadeLauncher (40mm) | `Explosive.Grenade.40mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (W = 1) | 7 | 105, 142, 143 | 105, 115 | underbarrel-weapon-tag |
| Explosives and launchers | STN 01 Heavy MountedMachineGun (72mm) | `Explosive.Rocket.72mm`, `Kinetic.Impact.ExplosiveBlunt` | yes (W = 1) | 7 | 102, 103, 104, 105, 142, 143 | 102, 103, 104, 105 | — |
| Explosives and launchers | STN 05 Heavy MainBarrel (DroneProjectile) | `Explosive.Drone`, `Kinetic.Impact.ExplosiveBlunt` | no | 7, 117 | 105, 142, 143 | 105 | — |
| Explosives and launchers | M67 frag grenade | `Grenade`, `Explosive.Rocket.60mm`, `DamageType.Explosive` | no | — | 102, 103, 104, 105 | 102, 103, 104, 105 | — |
| Explosives and launchers | C4 | `Explosive.Utility.C4`, `Explosive.Utility.C4`, `DamageType.Explosive` | no | 116 | 105 | 105, 116 | — |
| Explosives and launchers | AT mine | `Explosive.Utility.ATMine`, `Explosive.Utility.ATMine` | no | — | 105 | 105 | — |
| Explosives and launchers | Claymore | `Explosive.Utility.Claymore`, `DamageType.Explosive` | no | — | 105 | 105 | — |
| Explosives and launchers | IED | `Explosive.Utility.IED`, `Explosive.Utility.IED`, `DamageType.Explosive` | no | — | 105 | 105 | — |
| Explosives and launchers | Molotov | [`Molotov`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Molotov.json), [`Molotov`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Molotov.json), `DamageType.Explosive` | no | — | 105 | 105 | — |
| Explosives and launchers | CGM4 back-blast | `Weapon.Launcher.AT4`, `DamageType.BackBlast` | no | — | — | — | — |
| Explosives and launchers | Launcher_04 back-blast | `Weapon.Launcher.AT4`, `DamageType.BackBlast` | no | — | — | — | — |
| Explosives and launchers | RPG7 back-blast | `Weapon.Launcher.AT4`, `DamageType.BackBlast` | no | — | — | — | — |
| Explosives and launchers | Vehicle explosion (occupants) | `Explosive.VehicleExplosion`, `DamageType.Explosive` | no | — | 105 | — | — |
| Other | Vehicle environment (occupants) | `Vehicle`, `DamageType.Enviroment` | no | — | — | — | — |
| Other | Fists | `Utility.Fists`, `DamageType.Melee` | no | — | 144 | — | — |
| Other | LargeHammer | `Utility.LargeHammer`, `DamageType.Melee` | no | — | 144 | — | — |
| Other | MediumHammer | `Utility.MediumHammer`, `DamageType.Melee` | no | — | 144 | — | — |
| Other | SmallHammer | `Utility.SmallHammer`, `DamageType.Melee` | no | — | 144 | — | — |
| Other | Crowbar | `Utility.Crowbar`, `DamageType.Melee` | no | — | 144 | — | — |
| Other | HeavyDrill_RepairTool | `Utility.LargeDrill`, `DamageType.Melee` | no | — | 144 | — | — |
| Other | LightDrill_RepairTool | `Utility.MediumDrill`, `DamageType.Melee` | no | — | 144 | — | — |
| Other | Thrown object contact | `Kinetic.Impact.Throwable`, `DamageType.Impact` | no | — | — | — | — |
| Other | Actor or vehicle impact | `DamageType.Impact` | no | — | — | — | — |
<!-- /infantry_tables -->

### Explosive rounds

Launcher, cannon and shell rounds: direct-hit and blast data.

<!-- infantry_tables --explosives -->
| Source | Projectile | Source tag | Blunt S (before arming) | Direct S | Arming delay (s) | `ExplosiveRadius` | `EffectiveExplosiveRadius` | `ExplosiveDamageFallOff` | `MinimumExplosiveDamage` | Blast bone factor | Inner: factor (entries) | Outer: factor (entries) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| CGM4 | `84mm` | `Explosive.Rocket.84mm` | 120 | 100 | 0.03 | 1000 | 400 | 1 | — | no | ×1.01 (114) | ×0.5 (113) |
| Launcher_04 | `72mm` | `Explosive.Rocket.72mm` | 120 | 200 | 0.13 | 1080 | 200 | 0.8 | — | no | ×1 (—) | ×1 (—) |
| MMGL | `40mm` | `Explosive.Grenade.40mm` | 80 | 100 | 0.07 | 1000 | 250 | 1 | — | no | ×1 (—) | ×0.5 (115) |
| RPG7 | `93mm` | `Explosive.Rocket.93mm` | 120 | 110 | 0.099 | 1200 | 250 | 0.9 | — | no | ×1 (—) | ×0.5 (112) |
| TNK 01 Heavy (120x570mm) | `120x570mm` | `Explosive.Rocket.120mm` | — | 150 | — | 750 | 420 | 0.3 | 30 | no | ×1 (—) | ×0.5 (111) |
| STN 03 Heavy MainBarrel (120x800mm.Standard) | `120x800mm.Standard` | `Explosive.Rocket.120x800mm` | 120 | 120 | 0.1 | 1000 | 500 | 0.45 | 15 | no | ×1 (—) | ×1 (—) |
| ROT 02 Weapon 122mm (122mm) | `122mm` | `Explosive.Rocket.122mm` | — | 100 | — | 600 | 200 | 1 | 10 | no | ×0.55 (110) | ×0.55 (110) |
| ROT 03 Weapon 122mm (122mm) | `122mm` | `Explosive.Rocket.122mm` | — | 100 | — | 600 | 200 | 1 | 10 | no | ×0.55 (110) | ×0.55 (110) |
| TNK 04 (125x570mm) | `125x570mm` | `Explosive.Rocket.125mm` | — | 150 | — | 750 | 420 | 0.3 | 30 | no | ×1 (—) | ×0.5 (109) |
| TNK 01 Artillery (155mm.Expensive) | `155mm.Expensive` | `Explosive.Rocket.155mm` | 100 | 450 | 1.3 | 2000 | 1000 | 0.93 | — | no | ×1 (—) | ×0.45 (108) |
| TNK 01 Artillery (155mm.Standard) | `155mm.Standard` | `Explosive.Rocket.155mm` | — | 450 | — | 2000 | 750 | 0.5 | — | no | ×1 (—) | ×0.45 (108) |
| STN 02 Heavy MainCannon (20x102mm) | `20x102mm` | `Cannon.20x102mm` | — | 60 | — | — | 375 | 0.7 | — | — | — | — |
| ROT 02 Weapon 30mmCannon (30mm) | `30mm` | `Cannon.30mm` | — | 100 | — | 300 | 100 | 1 | 20 | yes (`Weapon.Vehicle.HelicopterCannon` row) | ×1 (10) | ×1 (10) |
| TNK 03 (35x228mm) | `35x228mm` | `Cannon.35x228mm` | — | 60 | — | — | 375 | 0.7 | — | — | — | — |
| GrenadeLauncher (40mm) | `40mm` | `Explosive.Grenade.40mm` | 80 | 100 | 0.07 | 1000 | 250 | 1 | — | no | ×1 (—) | ×0.5 (115) |
| STN 01 Heavy MountedMachineGun (72mm) | `72mm` | `Explosive.Rocket.72mm` | 120 | 200 | 0.13 | 1080 | 200 | 0.8 | — | no | ×1 (—) | ×1 (—) |
| STN 05 Heavy MainBarrel (DroneProjectile) | `DroneProjectile` | `Explosive.Drone` | 100 | 120 | 0.1 | 1000 | 500 | 0.45 | 15 | no | ×1 (—) | ×1 (—) |
<!-- /infantry_tables -->

### Thrown and placed explosive defaults

These are starting blast values, including native inheritance, rather than
final health loss. The source root and appended context are distinct.
Each kept component hit is evaluated separately; trigger timing and the
complete Molotov fire-patch geometry/lifetime are not modelled.
See the [reviewed actor evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round8-explosive-actors.md).

<!-- infantry_tables --actor-explosives -->
| Actor | Source root | Base | Outer radius (cm) | Inner radius (cm) | Minimum | Falloff | Appended context (before radius) |
|---|---|---:|---:|---:|---:|---:|---|
| M67 frag grenade | `Meta.Damage.Grenade` | 100 | 1000 | 500 | 10 | 1 | `Meta.Damage.Explosive.Rocket.60mm`, `Meta.Damage.DamageType.Explosive` |
| C4 | `Meta.Damage.Explosive.Utility.C4` | 250 | 600 | 250 | 20 | 1 | `Meta.Damage.Explosive.Utility.C4`, `Meta.Damage.DamageType.Explosive` |
| AT mine | `Meta.Damage.Explosive.Utility.ATMine` | 300 | 750 | 375 | 50 | 0.5 | `Meta.Damage.Explosive.Utility.ATMine` |
| Claymore | `Meta.Damage.Explosive.Utility.Claymore` | 150 | 300 | 150 | 30 | 0.5 | `Meta.Damage.DamageType.Explosive` |
| IED | `Meta.Damage.Explosive.Utility.IED` | 300 | 800 | 400 | 60 | 1 | `Meta.Damage.Explosive.Utility.IED`, `Meta.Damage.DamageType.Explosive` |
| Molotov | `Meta.Damage.Molotov` | 40 | 500 | 250 | 10 | 1 | `Meta.Damage.Molotov`, `Meta.Damage.DamageType.Explosive` |
<!-- /infantry_tables -->

Molotov sustained fire separately attempts 15 starting player damage or
2 vehicle health per eligible 0.4-second loop. These are not unconditional
damage-per-second guarantees.

### Armor and helmets

Each item's context tag, durability, reduction and the hit locations it covers.

<!-- infantry_tables --armor -->
| Item | Context tag | Kind | Max durability | `R` (%) | Covered hit locations | Entries (custom in bold) |
|---|---|---|---:|---:|---|---|
| [`ID_GhillieArmor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_GhillieArmor.json) | `Meta.Damage.Armor.Ghillie` | armor | — | 0 (no stages) | — | 21, 83, 89, 133, **138**, **139**, **143**, **144** |
| [`ID_GhillieArmorDry`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_GhillieArmorDry.json) | `Meta.Damage.Armor.Ghillie` | armor | — | 0 (no stages) | — | 21, 83, 89, 133, **138**, **139**, **143**, **144** |
| [`ID_GhillieHelmet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_GhillieHelmet.json) | `Meta.Damage.Helmet.Ghillie` | helmet | — | 0 (no stages) | — | 20, 28, 82, 87, 134, **140**, **141**, **142** |
| [`ID_GhillieHelmetDry`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_GhillieHelmetDry.json) | `Meta.Damage.Helmet.Ghillie` | helmet | — | 0 (no stages) | — | 20, 28, 82, 87, 134, **140**, **141**, **142** |
| [`ID_HeavyArmor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_HeavyArmor.json) | `Meta.Damage.Armor.Heavy` | armor | 250 | 50 | Torso.Upper, Torso.Middle, Torso.Lower | 21, 26, 83, 89, 104, 128, 133, **138**, **139**, **143**, **144** |
| [`ID_HeavyHelmet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_HeavyHelmet.json) | `Meta.Damage.Helmet.Heavy` | helmet | 180 | 50 | Head, Neck | 20, 28, 30, 82, 87, 130, 134, **140**, **141**, **142** |
| [`ID_LightArmor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_LightArmor.json) | `Meta.Damage.Armor.Light` | armor | 200 | 30 | Torso.Upper, Torso.Middle, Torso.Lower | 21, 83, 89, 102, 133, **138**, **139**, **143**, **144** |
| [`ID_LightHelmet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_LightHelmet.json) | `Meta.Damage.Helmet.Light` | helmet | 80 | 30 | Head | 20, 28, 29, 82, 87, 134, **140**, **141**, **142** |
| [`ID_MediumArmor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_MediumArmor.json) | `Meta.Damage.Armor.Medium` | armor | 220 | 40 | Torso.Upper, Torso.Middle, Torso.Lower | 21, 83, 89, 103, 133, **138**, **139**, **143**, **144** |
| [`ID_MediumHelmet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_MediumHelmet.json) | `Meta.Damage.Helmet.Medium` | helmet | 100 | 40 | Head | 20, 28, 82, 87, 134, **140**, **141**, **142** |
| [`ID_PilotHelmet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_PilotHelmet.json) | `Meta.Damage.Helmet.Pilot` | helmet | 180 | 30 | Head | 20, 28, 82, 87, 134, **140**, **141**, **142** |
| [`ID_SuperHeavyArmor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_SuperHeavyArmor.json) | `Meta.Damage.Armor.SuperHeavy` | armor | 300 | 60 | Torso.Upper, Torso.Middle, Torso.Lower, Pelvis, Arm.Upper | 21, 27, 83, 84, 89, 105, 106, 129, 133, **138**, **139**, **143**, **144** |
| [`ID_SuperHeavyHelmet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_SuperHeavyHelmet.json) | `Meta.Damage.Helmet.SuperHeavy` | helmet | 200 | 60 | Head, Neck | 20, 28, 31, 82, 87, 88, 131, 134, 136, **140**, **141**, **142** |
| [`ID_TankHelmet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_TankHelmet.json) | `Meta.Damage.Helmet.Tank` | helmet | 180 | 55 | Head, Neck | 20, 28, 82, 87, 134, **140**, **141**, **142** |
<!-- /infantry_tables -->

### Traced since the docs

Facts the verifier has traced but the reference pages don't yet state, each with its RVAs.

<!-- infantry_tables --verified -->
| Id | Fact (verified native trace (rounds 6 and 8)) | RVAs |
|---|---|---|
| `hit-location-asset` | ClassToHitLocations maps BHMoverPawn and WDTargetDummy to DA_GlobalDamage_HitLocations_Player. The shipped keys have disjoint inheritance branches, so they cannot compete for one target. | `0x6F01BB0` |
| `bone-lookup` | The hit location is an exact FName match of the raw FHitResult.BoneName in DamageHitLocations: no parent walk, and an unmapped bone gives an empty tag (no hit location). | `0x6BB8D00` |
| `impact-remap` | DamageImpactRemap is never applied for damage: its reader has 3 callers, all animation or ragdoll. spine_05 is Torso.Upper for damage. | `0x6BB8D40` |
| `physics-asset` | The viewer model uses PA_TPCharacter_Simplified; all 20 bodies map to a hit location. spine_01 and spine_02 have no body. Mutable's compiled model selects tagged physics assets by helmet/faction/view branches; see helmet-merge for the verified normal merge and component-default policy. | — |
| `radial-hits` | Radial damage: the gathered hits pass the character's IWDDamageable filter (dropped in one seat state, otherwise one hit per component). Each kept hit is its own evaluation, tagged Radius.Inner or .Outer, with that hit's bone as the hit location. | `0x6F06540`, `0x6E6DCC0` |
| `blunt-direct-only` | Kinetic.Impact.ExplosiveBlunt is added only on a projectile's direct-impact path, so entries 7, 117, 142 and 143 never apply to blast damage; entries 102–116 do. | `0x6B725B0` |
| `thrown-contact` | Against a character, the explosive-actor path is the thrown object's contact damage (source Kinetic.Impact.Throwable, DamageType.Impact), applied once per contact on the contacted bone. | `0x6CA8730` |
| `backblast-paths` | On foot, 0x6F042A0 traces the back-blast cone. In a seat, 0x6F06EB0 hits the occupants of the shooter's vehicle with synthetic hits, the shooter included. Only Launcher_04, RPG7 and CGM4 enable back-blast. | `0x6F042A0`, `0x6F06EB0` |
| `radial-amount` | Blast starts at BaseDamage through EffectiveExplosiveRadius (Inner), then falls linearly toward BaseDamage × (1 − ExplosiveDamageFallOff) just inside ExplosiveRadius (Outer), with 0 at or beyond that radius, all floored at MinimumExplosiveDamage. The Inner branch takes priority if E > R. Center, Disc and Points gather distance is original blast origin to accepted ImpactPoint, or the candidate point for a synthetic hit. Native default is Points with first-unoccluded-point termination. | `0x6F06540`, `0x6F03720` |
| `radial-context` | Exploding projectiles retain stats context, the weapon damage tag and ProjectileId, then add DamageType.Explosive and Radius.Inner/Outer. They skip the direct path's Projectile/ExplosiveBlunt additions. A mapped hit bone can therefore use the weapon bone row; this assumes valid equipment and the converter's target-discovery path. | `0x6B725B0`, `0x6B70E20`, `0x6F06540` |
| `armor-data-rows` | Armor rows run in a separate armor-target event starting from the original event amount. They do not join the character health event's Infantry group. The trace establishes evaluation/queuing, not the final durability write. | `0x6B53000`, `0x6BB4EB0` |
| `occupant-damage` | Vehicle-operator slot 160 starts at 1000 and appends VehicleExplosion + DamageType.Explosive; slot 161 forwards its caller's float and appends Vehicle + DamageType.Enviroment. Both use a zeroed synthetic hit with no bone or explicit hit-location tag, then ModifyDamage. | `0x7692B60`, `0x768ED20` |
| `armor-hook-paths` | Radial/back-blast use the general armor hook with empty bone/location. Melee Blueprints call it with Torso for separate armor events, but ignore its returned copy and evaluate the original health event. Thrown-contact and actor-impact native bodies call neither armor hook. | `0x6B53580`, `0x6B67870` |
| `melee-path` | Cooked B_Action_Melee, MeleeBash and ItemMelee character paths evaluate the original event with DamageType.Melee (or extension override), no hit bone and no hit-location tag. Amount is selected MeleeAction.Damage, or WeaponStats.MeleeDamage for bash. The source root is ItemId on the actions and extension DamageEntityData.Tag on ItemMelee; source context is replaced by the singleton damage type. | `0x6B67870`, `0x6F07C10` |
| `explosive-actors` | Frag, C4, AT mine, Claymore, IED and Molotov burst defaults and detonation routes were extracted from cooked Blueprints and native constructor inheritance. Reviewed numerical inputs are in assets/data/explosive-actors.json. Molotov fire separately starts at 15 player damage or 2 vehicle health per eligible 0.4-second loop; full patch geometry/lifetime remains open. | `0x6CA8D20`, `0x6F06540` |
| `backblast` | Normal handheld back-blast copies the weapon extension entity and appends DamageType.BackBlast; all three enabled launchers use Weapon.Launcher.AT4 as root. On-foot health uses minimum/base and distance/angle curves. Seated health uses base × health scalar × clamped vehicle scalar × distance curve; synthetic hits have no bone/location. Vehicle attribute self-damage is separate. | `0x6B92900`, `0x76C3EB0`, `0x76C4120` |
| `vehicle-weapon-tag` | The vehicle weapon extension copies WeaponExtensionDataAsset.DamageEntityData into its damage component; IWDWeaponOwner supplies that component's root tag to projectile record +0x10, which the damage builder appends to source context. Thus configured WE weapon tags reach bone-row selection. | `0x76478D0`, `0x6B72030`, `0x6B725B0` |
| `collision-channels` | Packed CharacterMesh configuration blocks Visibility, WDProjectile, WDMeleeHit and WDExplosive; ignores Pawn, Vehicle and PhysicsBody; overlaps WDVehicleCamera, WDBuildablePlacement and WDRotor. The cooked player mesh is Custom/QueryOnly with no response-array override, inheriting those responses. This establishes static channel responses, not shape registration or later runtime changes. | — |
| `tapered-capsule-query` | The simple-geometry builder converts tapered elements to straight capsules using the mean of their scaled/clamped radii and registers query-capable shapes. QueryOnly body plus QueryAndPhysics element preserves queries. The viewer shows authored tapered geometry; simple-geometry selection and channel filters still govern actual hits. | `0x423A2C0`, `0x422A320`, `0x42333F0` |
| `physical-material` | Physical materials affect penetration geometry/capacity, exit velocity and history tags. The current hit uses pre-exit ImpactVelocity; later hits may lose starting damage through the speed scale. Head/Body surface speed modifiers and ricochet chances are zero; their densities differ (0.2/1). Their ignore-list entries suppress history marking, not velocity loss. No extra direct SurfaceType health scalar is established in the traced bullet calculation. | `0x6F2F740`, `0x6F36190`, `0x6F36F40` |
| `exploding-hit` | bExploding requires positive radius, arming eligibility, instance +0x101 and no ricochet/penetration. The instance gate defaults true; the camera-projectile path updates it from vehicle-candidate acquisition time/threshold and clears it outside that controller state. A positive threshold can retain eligibility through loss grace. This covers the concrete traced mutation, not every possible writer. | `0x6B721B0`, `0x6F391F0`, `0x76CFEB0` |
| `impact-amount` | Actor impact starts at abs(overlap volume in m³ × cached substep seconds × UnresolvedCollisionDamageMultiplier), with native float conversion order and invalid/empty guards. Ground/BodyDragging cache FMoverTimeStep.StepMs × 0.001. It bypasses rules. Thrown contact uses ImpactDamage, inherited as 10 by Frag, C4, IED and Molotov; the hitting actor supplies source entity data. | `0x6E6B670`, `0x529AB10`, `0x6CA8730` |
| `radial-split` | Normal player setup has one eligible third-person CharacterMesh component: capsule ignores Visibility and first-person meshes use NoCollision. Mutable associates with the existing mesh, changing its asset/bodies rather than adding a third-person query primitive. The filter keeps one valid hit per component, not one per body. LOS, sampling, body state and protected-seat rejection can still leave no hit; this is not an invariant for arbitrary runtime component mutations. | `0x6E6DCC0`, `0x6E6AFBE`, `0x6B44E60` |
| `helmet-merge` | Mutable resolves __PA tags to indexed physics assets and deduplicates selected pointers. It reuses a sole selected asset when generated bodies are unmodified; otherwise it builds a combined asset with at most one body setup per bone. In the combined path, AggGeom comes from the generated Mutable body record, while the source setup used when a result bone is first created supplies selected body properties; duplicate head setups do not duplicate the result body or append geometry. The compiled program has root-reachable base __PA:0 plus helmet tags selected by helmet/faction/view conditions. The normal CharacterMesh override defaults null and its getter falls back to the assigned mesh's physics asset. Runtime parameter values and later override/replacement mutations remain unknown; attached-parent replacement is a separate default-off flag. | `0x66C05F0`, `0x66BAD60`, `0x6699D70`, `0x66D20A0`, `0x3D5E200`, `0x3D71170` |
| `caliber-parent-match` | Normal reload filters compare exact item IDs or child item context against parent filters; firing uses the actual loaded item's projectile fragment. Reviewed child associations are M500/MP43 slug, STN03 Standard and artillery Standard/Expensive. SupportedCaliber is not a universal admission gate. Prefix-only bow Explosive, CGM4 TVGuided and ROT02/03 Havoc pairings are excluded: the reviewed default chamber/item mappings do not select those projectile assets. Other runtime actions remain conditional. | `0x67A2B40`, `0x6792CB0`, `0x6C98290`, `0x7645A30` |
<!-- /infantry_tables -->

### Not traced

What the docs leave open, with what the data shows.

<!-- infantry_tables --not-traced -->
| Id | Open question | What the data says |
|---|---|---|
| `underbarrel-weapon-tag` | The shipped test underbarrel launcher has no firing binding on the verified M4/default-input path; an alternate firing owner and shot tag remain unproved. | H maps to ToggleAncillaryFire, but the selected input maps supply no binding. GrenadeLauncher.json supplies stats, not a firing component or Meta.Damage.Weapon tag. This source is data-only. |
<!-- /infantry_tables -->

</div>
