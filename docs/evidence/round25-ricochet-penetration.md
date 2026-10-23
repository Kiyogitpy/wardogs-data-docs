---
title: Round 25 ricochet and penetration, what the files determine
nav_exclude: true
---

# Ricochet and penetration: what is determinable

Round 25, teammate H. Question from the damage page: can ricochet and
penetration be modeled for the infantry weapons? Short answer: the
per-surface, per-ammo physics constants are fully in the files and are
tabulated in [`assets/data/weapon-penetration.json`](../../assets/data/weapon-penetration.json)
(generator and checks: [`_tools/weapon_penetration.py`](../../_tools/weapon_penetration.py)).
What is not in the files is the other half of every wall calculation: which
surface type, density and thickness a given wall or prop has. So the page can
state how an ammo type behaves against each surface type, and cannot yet say
what happens against "a concrete wall in Bakurani".

Two corrections to the shorthand used elsewhere in the docs:

- "Ricochet chances are zero" is true only for SurfaceType3 (Body) and
  SurfaceType17 (Head). In the packed config 57 of the 63 surface types have a
  nonzero ricochet probability, and 36 of the 63 (every named type except Body
  and Head, plus none of the unnamed 39-62) have a nonzero exit-speed modifier. The zeros for Body and Head are the exception, and they matter only
  for flesh. They say nothing about walls.
- "Ricochet and penetration are not modeled" on the damage page is a statement
  about scope, not about the game. The game models both, with the constants
  below.

Evidence tags: **Data** (read from the export or the packed config), **Native**
(traced in code, address given), **Derived** (arithmetic on Data and Native),
**New** (decoded this round from the unreviewed corpus pseudocode; not
independently verified), **Not determined**.

Sources of the packed values: `Wardogs/Config/DefaultGame.ini` line 303
(`ProjectileSystemSettings`) and `DefaultEngine.ini` `[PhysicalSurfaces]` in the
offline round 8 config extraction, which is not part of `data/`. The values are
copied into the JSON's `config` block so the script runs from a clone.

## 1. Determinability table

| Question | Status | What the files give |
|---|---|---|
| Which surfaces allow penetration? | Native for the rule, Not determined per world material | There is no per-surface "can penetrate" flag. A pass needs `capacity > thickness / cos(angle)` and thickness at least 0.01 (`0x6F36190`, [downstream trace](round8-physical-material-downstream.md) section 2). Capacity depends on projectile mass, diameter, speed, effectiveness and the material **density**. Projectile side: `bShouldPenetrate` is true by default (every infantry bullet asset omits it) and explicitly false on the launcher and cannon rounds (70, 72, 84, 93, 120, 122, 125, 155 mm); `bForcePenetrateThinSurfaces` is set on 122 mm, HAVOC, 40, 72, 84, 93 mm and the arrows. Per-material side: `BallisticResponse` Disabled rejects the exit query, Planar synthesizes thickness (`0x6F2F740`, `0x6F2FC20`); the response, density and thickness of any world material other than PM_Head and PM_Body are not in the export. |
| What is the ricochet chance per surface and ammo? | Data for the inputs, New for the combination, Derived for ammo | Surface table (`PhysMatRicochetProbabilities`, 63 entries), angle table (nine 10-degree bins, 0.08 at 0-10 up to 0.92 at 80-90), and `PenetrationEffectivenessRicochetProbabilities (2, 1)` are Data. Minimum angle `MinImpactAngleForRicochet`: 10 degrees by default (`+0x214`), 91 on the 155 mm assets (never). The way they combine (product of surface and angle terms times a ramp on penetration effectiveness, one random draw) is **New**, from `0x6F36600`, section 3. Ammo enters only through penetration effectiveness (AP x1.8, HP x0.1, section 4). |
| What fraction of speed and damage survives a pass through each surface? | Derived formula, Data coefficients, Not determined for walls | Speed after = speed x (1 - f) x clamp(1 - 0.5 (p + s), 0, 1), with `f = thickness x density / (K x cos)`, p the ammo variant's exit-speed multiplier, s the surface's exit-speed modifier (Data, 63 entries). `K` per weapon and ammo is in the JSON. `s`, `p` and `K` are known; thickness and density are not, except density for Head (0.2) and Body (1.0). Damage is not scaled at the pass itself (next row). |
| How many hits does the bitmap allow? | Derived (width), Not determined (cap) | `RicochetBitMap` and `PenetrationBitMap` are `uint32` (SDK `WDGame_structs.hpp`, `+0x44`, `+0x48`); bit `HitCount - 2` is read, so the history tags can mark hits 2 through 33. The first hit never carries the tags. Whether the projectile is removed after some number of hits, and what bit 32 and beyond do, is Not determined; `MaxConsecutiveFullRefundedSubsteps = 10` is a simulation-substep limit, not a hit cap. |
| Is damage after penetration scaled by the remaining speed? | Native | Yes, at the **next** impact. The current impact keeps its pre-exit `ImpactVelocity` (`0x6F36FE1`-`0x6F36FF1`); the amount builder takes that vector's length into the speed scale `clamp(speed / reference, 0, 1)` (`0x6B72A7F`-`0x6B72ACB`, `0x6C255B0`). The updated velocity reaches the later hit. Data: no infantry damage rule keys on `Kinetic.Impact.Ricochet` or `.Penetration` (0 of 146 entries), so the history tags add no factor of their own; the vehicle table has one such entry and its Amount is 0. Reference speed: weapon `TypicalSpeed` when overridden, else the projectile's. |
| Does a ricochet cost speed? | New | After a successful draw the velocity is scaled by a random factor between the surface's restitution Min and Max (`PhysMatRicochetRestitutionCoefficient`, Data), after a reflection and a random deflection. Ricochet is tried before penetration; a hit that ricochets is not also penetrated (`0x6F36F40`). Details in section 3. |
| Which physical materials do world props and walls use? | Not determined | The export has no mesh-to-physical-material table and no `WDPhysicalMaterial` assets except the two flesh materials. 156 data files carry a `PhysicalMaterialOverride`; 9,076 entries are `null` (mesh default, not exported) and only 125 name a material: PM_Metal 90, PM_Concrete 24, PM_Plaster 9, PM_Brick 1, PM_Glass 1. Which SurfaceType, density, thickness scale and BallisticResponse each PM_* has is not exported. The engine names SurfaceType4 Brick, 8 Concrete, 14 Glass, 23 Metal, 28 Plaster; mapping PM_Concrete to SurfaceType8 is an assumption by name, not data. |
| Does the ammo type change penetration? | Data | Five `DA_AmmoModifier_*` assets multiply PenetrationEffectiveness, EffectiveRange, PenetrationExitSpeed and TracerChance (table in section 4). They touch no damage value. |
| Is there a per-surface health multiplier? | Native, bounded | None found in the traced bullet amount chain ([downstream trace](round8-physical-material-downstream.md), conclusion). Not a claim about every actor override. |

## 2. Formulas and where they come from

All speeds in cm/s, as stored. `T` thickness along the ray (engine unit), `c`
the cosine of the impact angle (angle from the surface normal), `rho` the larger
of the entry and exit materials' density, `d` and `m` the projectile Diameter and
Mass, `E` the ammo variant's penetration effectiveness (base multiplier times
the modifier), `p` its exit-speed multiplier, `s` the surface's exit-speed
modifier.

| Step | Formula | Source |
|---|---|---|
| Capacity | `capacity = v x 0.01 x m x c x E / (max(rho, 0.001) x 0.099999994 x d^2)` | Native, `0x6F2FB77`-`0x6F2FC07` (downstream trace section 1) |
| Effectiveness | `capacity / T` | Native, `0x6F2FC03` |
| Pass condition | `capacity > T / c` and `T >= 0.01` (unless the actor override flag is set) | Native, `0x6F361B2`-`0x6F361F3` |
| Speed after pass | `v x (1 - T / capacity) x clamp(1 - 0.5 (p + s), 0, 1)`, then a random exit deflection | Native, `0x6F36294`-`0x6F36359` |
| Next-impact damage factor | `clamp(v_after / reference, 0, 1)` | Native, `0x6B72AB9` to `0x6C255B0`; reference per Damage Pipeline section 7.6 |
| Capacity coefficient | `K = v x 0.01 x m x E / (0.099999994 x d^2)`, so `capacity = K c / rho`, `f = T / capacity = T rho / (K c)`, pass iff `f < c`, effectiveness `= K c / (rho T)` | Derived (this round) |
| Variant stats | base stat x modifier multiplier; omitted base `E` = 1.0, omitted base `p` = 0.0, omitted min angle = 10 | Native constructor defaults `0x699DEE0` (`+0x208`, `+0x20C`, `+0x214`, read from the corpus this round; the 10-degree default is also in Projectile Flight section 10); multiplication per Damage Pipeline section 7.9 |

The units of `T` are not established. The collision trace gives no unit for
thickness, and `Diameter` and `Mass` carry no real-world unit either (the
downstream trace says so). The JSON therefore expresses loads as the
dimensionless `f`, and `K` is "thickness times density per unit cosine" in
whatever unit the engine's `T` uses. Planar surfaces multiply the material's
`PlanarThickness` by `PlanarSurfaceThicknessScale = 10` (Data).

A consequence worth stating: an ammo variant with a larger `E` has a
proportionally larger `K`, so AP (E x1.8) passes through 1.8 times the
thickness-density load of FMJ at the same speed, and HP (E x0.1) one tenth.
HP, with `E` 0.1, has effectiveness at or below 1 for any load above `0.1 K`,
which makes it the ammo most likely to ricochet and the one that stops first.

## 3. Ricochet decision, decoded this round (New, unverified)

`0x6F36600` is called from `0x6F36F40` before the penetration step; penetration
(`0x6F36190`) runs only when the ricochet draw fails. The pseudocode in the local
corpus (read-only, marked UNREVIEWED DECOMPILER OUTPUT) reads, in order:

1. Return false if the result is not usable (first call on `a3 + 176`).
2. Return false if the ratio of two projectile vectors' lengths (instance `+0x20`
   over `+0x88`, current velocity over a stored launch-like velocity; the second
   field is not named) is below 0.1.
3. Angle `= result.angle` in degrees. Return false if it is below stats
   `+0x214` (`MinImpactAngleForRicochet`).
4. `P = PhysMatRicochetProbabilities[SurfaceType]` (1.0 if the surface is not in
   the map), then multiply by the third element of **every** angle-table row
   whose closed interval contains the angle (an angle of exactly 10, 20, ... hits
   two bins and multiplies both).
5. `t = clamp((effectiveness - 2) / (1 - 2), 0, 1)` using subsystem `+0x3C0` and
   `+0x3C4`, which hold `PenetrationEffectivenessRicochetProbabilities (2, 1)`
   (the field identification by offset is inferred). With effectiveness
   `= K c / (rho T)`: `t = 1` at effectiveness 1 or below, `0` at 2 or above.
6. Ricochet iff `t x P > r`, with `r` from an LCG (`196314165 x seed + 907633515`)
   in `[0, 1)`, seed at projectile `+0xD0`.
7. On success: reflect the velocity about the normal, add a random deflection
   (`MaxDeflectionPercentageShallowAngle` / `SharpAngle` blended by angle), look up the
   surface's restitution Min/Max and scale the velocity by a random value in
   between, then record the event.

Reading: a bullet that is clearly able to penetrate (effectiveness 2 or more,
i.e. `f <= 0.5`) cannot ricochet at all, whatever the surface and angle. Ricochet
needs a struggling bullet, and the surface and angle tables then scale the
chance. This is also why a flesh hit never ricochets (Body and Head have `P = 0`).
It follows that high-effectiveness ammo (AP) ricochets less than FMJ against the
same wall, HP more.

Not decoded: the exact reflection geometry, the deflection distribution, the
meaning of the ratio gate in item 2, and what sets the usability flag in item 1
(`v60` in `0x6F36F40`, written by `0x6F2F740`).

## 4. Ammo variants and what the files give per surface type

Ammo modifier assets ([`AmmoModifiers/`](../../data/Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers)):

| Modifier | E (penetration effectiveness) | p (exit-speed) | Effective range | Tracer |
|---|---:|---:|---:|---:|
| FMJ (no asset) | x1 | x1 | x1 | none |
| Tracer | x1.0 | x0.075 | x1.0 | 1.0 |
| HollowPoint | x0.1 | x0.15 | x0.8 | none |
| HollowPoint.Tracer | x0.1 | x0.15 | x0.8 | 1.0 |
| ArmorPiercing | x1.8 | x0.0 | x1.2 | none |
| ArmorPiercing.Tracer | x1.76 | x0.0 | x1.2 | 1.0 |

Base `p` per caliber is in the projectile assets (5.56: 0.18, .308: 0.13,
7.62x54: 0.14, 7.62x39 mm: 0.15, 9 mm: 0.35, .45 ACP: 0.32, .50 Cal: 0.05; 5.45, 7.62x51 and .338 omit it, so 0.0); `E` is 1.0 unless
the asset sets it (.50 Cal 3.5, 20x102 1.8, 35x228 0.75, arrow 0.5). Multiplying by
the modifier: AP always gives `p = 0` (0 times anything), HP gives `0.15 p`, Tracer
`0.075 p`. Because of the clamp the exit-speed term only ever protects speed:
`clamp(1 - 0.5 (p + s), 0, 1)` is 1 only when both are 0.

Per-surface values (SurfaceType, engine name, exit-speed modifier `s`, ricochet
probability `P`, restitution Min-Max) are in the JSON `config.surfaces`. A
selection (full list in the JSON):

| Type | Name | s | P | Restitution |
|---:|---|---:|---:|---|
| 3 | Body | 0 | 0 | 1.0-1.0 |
| 17 | Head | 0 | 0 | 1.0-1.0 |
| 4 | Brick | 0.30 | 0.25 | 0.15-0.35 |
| 8 | Concrete | 0.40 | 0.35 | 0.25-0.50 |
| 14 | Glass | 0.05 | 0.10 | 0.15-0.40 |
| 23 | Metal | 0.40 | 0.45 | 0.35-0.65 |
| 28 | Plaster | 0.25 | 0.20 | 0.15-0.35 |
| 35 | Wood | 0.15 | 0.30 | 0.15-0.35 |
| 38 | BulletProofGlass | 1.00 | 0.10 | 0.15-0.40 |
| 18 | Ice | 0.15 | 0.80 | 0.50-0.85 |
| 0 | Default | 0 | 0.30 | 0.25-0.45 |

Surface types 39-62 have no engine name; they share `s = 0`, `P = 0.5` and
restitution 0.4-0.6. SurfaceType19 (Lava) has an empty restitution entry.

Implication for the damage page: no surface type is a hard stop on speed alone,
because `p + s` at most reaches 1.55 (arrow on BulletProofGlass) and the factor
bottoms out at 0.225. Whether a wall stops the bullet is decided by `f < c`, that
is by thickness and density, which the files do not give for any wall.

## 5. Worked examples

These are grounded in the formulas and the Data above, with one free input: the
load `X = T rho / c` (a number in the engine's thickness unit times density), which the
game files do not supply for any wall. The surface values are the SurfaceType8
(Concrete) entry; whether a given wall resolves to it is not determined. Both rounds
are fired from the A-91 at point blank (`InitialBulletSpeed` 71500 cm/s, speed-scale
reference 40400 cm/s from the 5.56 projectile; 71500 above 40400, so the speed scale
is 1 at the muzzle). Drag between the two impacts is ignored.

Chosen load `X = 45`.

| | FMJ 5.56 | AP 5.56 |
|---|---:|---:|
| `E` | 1 | 1.8 |
| `p` | 0.18 | 0 |
| `K` | 90.23 | 162.41 |
| `f = X / K` | 0.499 | 0.277 |
| Surface factor `clamp(1 - 0.5 (p + 0.4))` | 0.710 | 0.800 |
| Speed after (cm/s) | 71500 x 0.501 x 0.710 = 25447 | 71500 x 0.723 x 0.800 = 41351 |
| Next-impact damage fraction `min(1, v / 40400)` | **0.630** | **1.000** |
| Ricochet at 35 degrees (effectiveness `K / X`) | 2.005, `t = 0`, chance 0 | 3.61, `t = 0`, chance 0 |

The damage page's per-bullet numbers stay as they are for the first impact. The
difference shows in what is left for a target behind the wall: 63 percent of a fresh
hit for FMJ, a full hit for AP. The AP figure is not extra damage: the speed scale is
capped at 1, and AP leaves the round above the reference speed.

A struggling round, `X = 70` at 35 degrees (cos 0.819), FMJ:
effectiveness `K / X = 1.289`, `t = 0.711`; with Concrete `P = 0.35` and the angle bin
30-40 at 0.42, chance `= 0.35 x 0.42 x 0.711 = 0.104`. If it does not ricochet,
`f = 0.776 < c = 0.819`, so it penetrates, with speed `71500 x 0.224 x 0.710 = 11366`
and a next-impact damage fraction of 0.281. The same wall load against AP gives
effectiveness 2.32, ricochet chance 0, `f = 0.431`, next-impact fraction 0.806.

The JSON's `reference` block tabulates the same for A91, AK74M, SV98, SR_04 and
Glock17, every ammo variant, seven surface types and loads `f` of 0, 0.25, 0.5, 0.75.
The `f` there is the speed-loss fraction directly, to avoid asserting a thickness unit.

## 6. What remains not determined, ranked

1. **Physical material per world mesh, with density, thickness and BallisticResponse.**
   This is the blocker for any wall or prop number. The export holds 125 explicit
   `PhysicalMaterialOverride` names (PM_Metal 90, PM_Concrete 24, PM_Plaster 9,
   PM_Brick 1, PM_Glass 1) and 9,076 nulls that fall back to the mesh's own
   material. Settling it needs the cooked `WDPhysicalMaterial` assets (SurfaceType,
   Density, PlanarThickness, BallisticResponse; same extraction as PM_Head and
   PM_Body in round 8) and the static mesh or material physical-material assignments for
   the map meshes, or a runtime trace printing the `FHitResult` physical material and
   the result block (`+0` thickness, `+0xC` capacity) for shots at tagged props. The
   exported `PlanarThickness` on the flesh assets is subnormal and was not trusted in
   round 8.
2. **Units and live values of thickness, and the speed at the first wall.** Without
   the thickness unit the loads are dimensionless. A runtime shot of known weapon at a
   known plate gives `T` and `capacity` directly from `0x6F2FC20` / `0x6F2FB30`. The
   speed at the wall also needs the drag integration from
   [Projectile Flight](../../pipelines/Wardogs_ProjectileFlight_v1.md); `InitialBulletSpeedModifier`
   and attachment effects on launch speed are still open there.
3. **The ricochet reflection and the ratio gate (`0x6F36600` items 1, 2, 7).** The
   decision formula is decoded but unreviewed. Cheap to settle statically: two to three
   short IDA sessions to confirm the offsets `+0x3C0/+0x3C4` are the effectiveness range,
   to name the vector at `+0x88`, and to read the reflection and deflection terms. After that
   the angle, restitution and deflection of a ricocheted round can be modeled in full.
4. Hit-count cap per projectile and what happens past hit 33 (bitmap width).
5. Exit deflection distribution after a pass (`ExitDeflection*` ranges are Data,
   `(5, 0.5)` effectiveness and `(0, 7.5)` degrees; their use is not re-derived), and
   its consequence for hitting a target behind a wall.
6. Pellet rounds (12 gauge): `MaxPelletCount = 16` is Data, and the per-pellet
   diameter and mass are in the assets, but the pellet spread behind a pass is not
   modeled. The shotgun rows of the JSON use the same formulas per pellet.
7. Armor interaction after a pass: the rule for armor uses ammo-type effectiveness
   from the damage tables, independent of this speed loss. No coupling was found.

## 7. Files

- [`_tools/weapon_penetration.py`](../../_tools/weapon_penetration.py): `--write`,
  `--check`.
- [`assets/data/weapon-penetration.json`](../../assets/data/weapon-penetration.json).
- This page. Not touched: damage page, damage JSON, config, `assets/js`, `worker/`,
  round 24 files.
