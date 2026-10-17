---
title: "Vehicle Damage Pipeline"
parent: "Pipelines"
nav_order: 2
---

# Wardogs — Vehicle Damage Pipeline

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

How damage resolves against vehicles. Vehicles use **the same rule
pipeline as infantry**: the same `ModifyDamage` call, collector,
sorting and arithmetic described in
[`Wardogs_DamagePipeline_v2.md`](Wardogs_DamagePipeline_v2.md) §1–6.
There are two differences. Vehicle rows contain no custom operations,
and the modified amount goes to a section-based health model instead of
`TakeDamage`.

Build: `++Wardogs+Live-CL-516586` · Engine: UE 5.7 · Native addresses are
file RVAs in the restored executable (see the damage doc §11). Labels as in
the damage doc: **Native** (code, RVA cited, unreviewed decompiler
output), **Data** (export), **Derived** (arithmetic on both), **Open**.

---

## At a glance

| Stage | Status | Section |
|---|---|---|
| Rules: same evaluator; target tag = the vehicle's `VehicleDamageTag`; parent walk reaches the generic `Meta.Damage.Vehicle` row | **Native** + **Data** | §1 |
| Rule data: 21 vehicle files, 23 rows, 665 entries (581 selectable), no custom operations, 5 `Add` entries | **Data** | §2 |
| Hit location: the hit section's `Meta.Damage.HitLocation.*` tag; hitboxes are collision-mesh slots mapped to sections | **Native** + **Data** | §3 |
| Section application: pick section → Pre routing → own health → section-damaged handling → Simultaneous → Post | **Native** | §4 |
| Worked examples: ROT_02 profile, TNK_01 125 mm hit, caliber factors, hits to destroy | **Derived** | §5 |

## 1. Same evaluator, different target

**Native.** A vehicle hit reaches `UWDDamageSubsystem::ModifyDamage`
(`0x6F02EC0`) and the global evaluator (`0x6BB6FB0`) exactly as an
infantry hit does. The projectile path (`0x6B725B0`, at `0x6B733AC`) and
the radial paths (`0x6F06540`, `0x6F042A0`, `0x76740F0`) fetch the
vehicle hit tag through `0x6B80230` before the call. The result is
dispatched through `IWDDamageable` (`0x6C2A5F0`) to the vehicle class's
interface slot (Rotary slot 370 at `0x76B7E80`; Wheeled 375, Tracked 367,
Stationary 366, Airplane 367), which calls `ApplyWDDamage` (`0x6B7FE50`)
with the modified amount as `FWDDamageContext.CurrentDamage`.

`UWDVehicleOperatorComponent` slots 160/161 (`0x7692B60`, `0x768ED20`)
are a different path: they build events whose *source* is the vehicle
(`Meta.Damage.Explosive.VehicleExplosion` / `DamageType.Explosive`, and
`Meta.Damage.Vehicle` / `DamageType.Enviroment`), most likely for damage
to occupants.

**The target tag.** The vehicle pawn constructor (`0x76B5560`) creates a
damage entity component with the default tag `Meta.Damage.Vehicle`.
`UWDVehicleGameplaySystemsComponent` slot 161 (`0x767BC40`) overwrites it
(`0x6B18E70`) with `DA_GameplaySystems_*.DamageEntitySettings.VehicleDamageTag`.
For 20 of the 21 vehicles that tag equals the vehicle row key exactly
(STN_06 is the exception, §2.2).

**The walk** (damage doc §5). The collector evaluates every level of the
target tag's parent chain that has a registry row, most specific first,
stopping at `RootDamageTag`. Vehicle tables use the same
`FWDDamageableEntityTableRow` and are added to the `GlobalDamageData`
registry by each vehicle's GameFeature (for example
`Vehicles/ROT_02/Content/ROT_02.json`, `RegistryToAddTo: GlobalDamageData`).
So a Havoc hit evaluates its own row (`…Air.Rotary.Havoc`), then any
parent rows, then the generic `Meta.Damage.Vehicle` row, unless
`RootDamageTag` is `Meta.Damage.Vehicle` itself (**Open**). The generic
row is a parent level evaluated after each vehicle's own row, **not a
fallback**. Its live entries are two HollowPoint rules, −40 and +40,
which together give ×0.84; the Bullet (`None`) and Ricochet (0) entries
change nothing. Supply crates use several levels:
`…SupplyCrate.Large.Armoured` → `.Large` (empty) → `.SupplyCrate` →
`Meta.Damage.Vehicle`.

**Arithmetic** (damage doc §6). `Percentage_Ongoing` multiplies the
running amount by `1 + Amount/100`: −95 leaves 5 %, +400 gives ×5. Within
a level, entries sort by category index (`DA_GlobalDamage_Categories`,
no tie-breaker; `PriorityIndex` is overwritten, so array order decides
nothing). Because five vehicle entries use `Add` (§2.1), **order
matters for those rows**: entries sorting after the `Add` scale the flat
+1000, entries before it do not. The clamp `max(C, 0)` happens once, at
the end.

## 2. Rule data

### 2.1 Inventory

**Data.** 21 files under `Plugins/GameFeatures/Vehicles/<CODE>/Content/DataTables/`
(`DataTable/` for STN_03 and STN_05), plus the generic
[`DT_GlobalDamage_VehicleData`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_VehicleData.json).
"Selectable" excludes entries the collector skips (no requirements and
amount 0, damage doc §4).

| File (`DT_GlobalDamage_VehicleData_…`) | Row key (`Meta.Damage.Vehicle.` omitted) | Entries | Selectable | Ongoing amount range | Other ops |
|---|---|---:|---:|---|---|
| `ROT_02` | `Air.Rotary.Havoc` | 35 | 31 | −95 … +450 | — |
| `ROT_03` | `Air.Rotary.LittleBird` | 33 | 30 | −95 … +500 | — |
| `ROT_04` | `Air.Rotary.ROT_04` | 33 | 29 | −95 … +450 | — |
| `SPW_01` | `Land.Tracked.Leopard.Spawn` | 32 | 27 | −100 … +500 | — |
| `STN_01` | `Stationary.Mistral` | 26 | 22 | −100 … +1500 | 1 Add |
| `STN_02` | `Stationary.Phalanx` | 26 | 22 | −100 … +2000 | 1 Add |
| `STN_03` | `Stationary.Mortar` | 24 | 20 | −100 … +650 | 1 Add |
| `STN_04` | `Stationary.RadioTower` | 27 | 24 | −95 … +250 | — |
| `STN_05` | `Stationary.STN_05` | 24 | 20 | −100 … +650 | 1 Add |
| `STN_06` | `Stationary.STN_05` | 24 | 20 | −100 … +650 | 1 Add |
| `TNK_01` | `Land.Tracked.TNK_01.AntiAir` | 29 | 24 | −100 … +450 | — |
| `TNK_01` | `Land.Tracked.TNK_01.Artillery` | 29 | 24 | −100 … +500 | — |
| `TNK_01` | `Land.Tracked.TNK_01.Heavy` | 29 | 24 | −100 … +450 | — |
| `TNK_04` | `Land.Tracked.TNK_04.Default` | 30 | 25 | −100 … +450 | — |
| `WHL_01` | `Land.Wheeled.Bobcat` | 20 | 19 | −95 … +500 | — |
| `WHL_02` | `Land.Wheeled.Patriot.Kodiak` | 29 | 26 | −95 … +700 | — |
| `WHL_05_Humvee` | `Land.Wheeled.Humvee.Default` | 31 | 28 | −95 … +500 | — |
| `WHL_05_Minigun` | `Land.Wheeled.Humvee.Minigun` | 31 | 28 | −97.5 … +800 | — |
| `WHL_05_RingTurret` | `Land.Wheeled.Humvee.MachineGun` | 31 | 28 | −96 … +650 | — |
| `WHL_06_DuneBuggy` | `Land.Wheeled.DuneBuggy` | 30 | 27 | −95 … +500 | — |
| `WHL_07_Ural` | `Land.Wheeled.Ural` | 30 | 27 | −95 … +500 | — |
| `WHL_08` | `Land.Wheeled.WHL_08.Default` | 31 | 28 | −95 … +600 | — |
| `WHL_08_RingTurret` | `Land.Wheeled.WHL_08.MachineGun` | 31 | 28 | −95.5 … +600 | — |

Totals: 665 entries, 581 selectable. Operations: 576 `Percentage_Ongoing`,
84 `None`, **5 `Add` +1000** (STN_01, 02, 03, 05, 06; source
`Meta.Damage.Vehicle.Land.Tracked`, category Bone). No custom operations.

Selectable entries by category: Calibre 328, Armor 108, Bone 45, CaliberEffectiveness 44, AmmoModifier 23, Ricochet 18, Melee 10, None 5. The five
category-`None` entries are the stationary Melee −80 rules; a missing
category sorts first (index −1).

### 2.2 Data issues

- **STN_06 is probably wrongly keyed.** Its table is a byte-identical copy
  of STN_05's (row `…Stationary.STN_05`), but its `VehicleDamageTag` is
  `Meta.Damage.Vehicle.Stationary.MGNest`
  (`DA_GameplaySystems_STN_06.json`). That tag appears neither in the
  exported tag config nor among the native tag globals, and two sources
  register the same STN_05 row. STN_06 most likely never reaches its own
  rules.
- **`Land.Wheeled.WHL_08.MachineGun` is never used.** No gameplay-systems
  asset assigns that tag; the WHL_08 ring-turret variant carries the
  `WHL_08.Default` tag through its config, so the MachineGun row's rules
  are unreachable.
- **Nine entries can never match.** Their `PossibleHitLocations` list only
  `Attribute.Gameplay.Health.*` tags, but the event's hit location is a
  `Meta.Damage.HitLocation.*` tag (§3). Affected: ROT_03 #4 and #5,
  SPW_01 #16, STN_04 #16 and #18, TNK_01 #14 (all three rows), TNK_04 #14.

## 3. Hit location

**Native** (`0x6B80230`). The event's hit location is the first
`Meta.Damage.HitLocation.*` tag in the hit section's `Tags`. Rules with
`PossibleHitLocations` such as `…Vehicle.MainRotor` match against it.

### 3.1 Hitboxes

**Native.** A point hit picks its section through the vehicle's complex
surface, not physics bodies. The zone query `0x5338730` (used by
`ApplyDamageEvent` and by the projectile hit-tag fetch `0x6B80230`) and
the reflected `QueryDamageZoneForComplexHit` thunk `0x5345EA0`, which
inlines the same three calls, do the lookup. Every triangle of the vehicle's
collision mesh belongs to a named **collision slot**. The
`BHComplexSurfaceComponent` (vehicle pawn `+0x340`, reached through the
interface at `+0x338`) resolves the hit to its slot (`0x50BF880`), and the
damage model looks the slot up in its slot-to-section table (component
`+0x180`). When the query misses on a point or radial hit, the section tag
is empty (§4.1). The vehicle's physics asset (for example `PA_ROT_02`, one
body with collision disabled) plays no part.

**Data.** The table comes from `MVF_HealthSections.ComplexSurfaceMappings`
in the platform and part files: per surface group, a slot map
(`CC_FuelTank` → `Attribute.Gameplay.Health.FuelTank`, …), and a default
section (usually the main health) for every slot not listed. Which code
fills the component's table from this struct is not traced; the struct is
the only slot-to-section data in the export.

**Data, collision meshes.** The slots live on dedicated low-poly
collision meshes, separate from the render models. Each render static mesh
names its collision mesh in `UStaticMesh.ComplexCollisionMesh`. For the
Havoc: `SM_ROT_02_Body` → `CC_ROT_02_Body_01a`, plus the wheels, doors,
main and rear rotor hubs and blades (9 collision meshes, under
`Meshes/ComplexCollision/`); the missile pods and reticle have none. The
rotors are placed by an `MVF_DestructibleMeshes` fragment
(`Vehicle.DestructibleMesh.Rotor.Main` / `.Tail`), attached to the chassis
skeleton's `mainRotorSpin_J` and `rearRotorSpin_J` bones. A
collision mesh's material slots are the `CC_*` names, each with a
collision material (for example `CC_FuelTank` → `MI_VehicleCC_FuelTank`,
`CC_Main` → `MI_VehicleCC_Metal_ReinforcedArmored`, `CC_TailRotor` →
`MI_VehicleCC_Metal_Weak`), and its render data holds the triangles per
slot (`CC_ROT_02_Body_01a`: about 1,450 triangles over 7 slots). Slots not
in the map, such as `CC_Main`, `CC_Glass` and `CC_Fabric`, take the
default section. Stationary vehicles place such proxies directly as mesh
fragments (`Meshes/ComplexCollisions/ComplexProxy/`). Decoding these
meshes needs the static-mesh usmap fixes in
[`tools/cue4parse_extractor`](tools/cue4parse_extractor/README.md).

**Derived**, `_tools/damage_tables.py --hitboxes`: every vehicle's map,
with the section's maximum health, how the section passes damage to the
main health (§4.2), and the rule factor at that hitbox for an FMJ direct
hit (§1–2; the section's hit-location tag selects location rules).
Variants that share a damage row and map are listed together. "none"
means hits there never reach the main health.

<!-- damage_tables --hitboxes -->
| Vehicle (variants) | Collision slot | Section (max health) | Routing to main health | `556mm` | `50Cal` | `30mm` |
|---|---|---|---|---:|---:|---:|
| `Air.Rotary.Havoc` (Attack_ROT_02) | `CC_Engine` | Health.Engine (200) | none | ×0.05 | ×0.05 | ×0.195 |
|  | `CC_FuelTank` | Health.FuelTank (200) | none | ×0.2 | ×0.2 | ×0.195 |
|  | `CC_MainRotor` | Health.Rotor.Main (400) | post 1 when depleted, simultaneous 0.5 | ×0.025 | ×0.025 | ×0.195 |
|  | `CC_TailRotor` | Health.Rotor.Tail (300) | post 1 when depleted, simultaneous 1 | ×0.025 | ×0.025 | ×0.195 |
|  | `CC_Wheel_0` | Health.Wheel.Left.Front (100) | post 1 when depleted | ×0.05 | ×0.05 | ×0.195 |
|  | `CC_Wheel_1` | Health.Wheel.Right.Front (100) | post 1 when depleted | ×0.05 | ×0.05 | ×0.195 |
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
|  | `CC_Radar` [Radar] | Health.Radar (100) | none | ×0.05 | ×0.05 | ×0.21 |
|  | `(default)` | Health (1000) | is the main health | ×0 | ×0 | ×0.21 |
| `Land.Tracked.Leopard.Spawn` (SPW_02, SPW_03) | `CC_FuelTank` | Health.FuelTank (100) | none | ×0 | ×0 | ×0.21 |
|  | `CC_MainBody` | Health (1000) | is the main health | ×0 | ×0 | ×0.21 |
|  | `CC_Radar` | Health.Radar (100) | none | ×0.05 | ×0.05 | ×0.21 |
|  | `CC_Tracks_L` | Health.Tracks.Left (125) | post 0.5 when depleted, simultaneous 1 | ×0 | ×0 | ×0.21 |
|  | `CC_Tracks_R` | Health.Tracks.Right (125) | post 0.5 when depleted, simultaneous 1 | ×0 | ×0 | ×0.21 |
|  | `CC_Radar` [Radar] | Health.Radar (100) | none | ×0.05 | ×0.05 | ×0.21 |
|  | `(default)` | Health (1000) | is the main health | ×0 | ×0 | ×0.21 |
|  | `(default)` [Radar] | Health.Radar (100) | none | ×0.05 | ×0.05 | ×0.21 |
| `Stationary.Mistral` (STN_01) | `CC_Main` | Health (3000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
|  | `(default)` | Health (3000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
| `Stationary.Phalanx` (STN_02) | `CC_Main` | Health (5000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
|  | `(default)` | Health (5000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
| `Stationary.Mortar` (STN_03) | `CC_Main` | Health (3000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
|  | `(default)` | Health (3000) | is the main health | ×0.15 | ×0.15 | ×0.5 |
| `Stationary.RadioTower` (STN_04) | `CC_Main` | Health (1000) | is the main health | ×0.05 | ×0.05 | ×0.85 |
|  | `(default)` | Health (1000) | is the main health | ×0.05 | ×0.05 | ×0.85 |
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

## 4. Section application

### 4.1 Order

**Native.** After the rules, `ApplyWDDamage` hands the amount to the
vehicle damage model:

1. **Pick the section** (`ApplyDamageEvent`, `0x53202B0`; the exec thunk
   `0x5341430` reaches it through `0x5320400`). A pre-gate requires the
   authority role, an amount above `1e-8` and two owner checks. Point
   damage uses the zone query `0x5338730` on the hit info; radial damage
   uses the first component hit; any other event falls back to
   `Attribute.Gameplay.Health`. When the zone query misses on a point or
   radial hit, the section tag is empty rather than the main health.
2. **PreDamageRouting.**
3. The section-requirement filter.
4. **The section's own attribute** is reduced by the remainder
   (`0x52311D0`).
5. **Section-damaged handling** (vtable `+0x510`; base `0x532F730`, WD
   override `0x6B802D0`). It broadcasts the section-damaged delegate,
   then:
   - section still alive: returns 1;
   - main `Attribute.Gameplay.Health` depleted: calls the owning
     `BHBaseVehiclePawn`'s destroy routine (`0x53D8E20`, unnamed; not the
     reflected `DestroyVehicle` UFunction, whose native body is
     `0x53288B0`) and returns 0, so no post routing;
   - any other section depleted: broadcasts
     `MVehicleSectionDestroyedMessage` (`0x5307ED0`) and returns 1.
6. **SimultaneousDamageRouting.**
7. **PostDamageRouting.** Skipped if step 5 returned 0, or if pre routing
   (step 2) returned 0 (amount used up, or the loop guard tripped). It
   still runs when step 3 rejects the section or step 4 absorbs nothing;
   steps 4–6 are skipped in that case.

So the destroyed-section message goes out **before** post routing.
Sections are keyed by attribute tags (`Attribute.Gameplay.Health.*`).

### 4.2 Routing semantics

**Native** (`0x53205D0` ApplyDamageToSection, `0x5339DD0`
RerouteDamageInternal). Structures:
[`FVehicleHealthSection`](sdk/raw/Mechanized_structs.hpp#L523) and
[`FVehicleDamageRouting`](sdk/raw/Mechanized_structs.hpp#L511).

```cpp
struct FVehicleHealthSection final {       // 0x140
    float MaxHealth;                                    // 0x00
    FGameplayTagContainer Tags;                         // 0x08 — includes the hit-location tag (§3)
    bool  _aaachkphmgcampdlhdkkf;                       // 0x28 — skip Pre routing for radial events
    TMap<FGameplayTag, FVehicleDamageRouting> PreDamageRouting;          // 0x30
    bool  _aaacikmpjffpcggjhonpl;                       // 0x80 — skip Post routing for radial events
    TMap<FGameplayTag, FVehicleDamageRouting> PostDamageRouting;         // 0x88
    bool  _aaadafjbjhkkggmmjaeba;                       // 0xD8 — skip Simultaneous routing for radial events
    TMap<FGameplayTag, FVehicleDamageRouting> SimultaneousDamageRouting; // 0xE0
    FGameplayTag RepairInteractionContextTag;           // 0x130
    FGameplayTag RepairInteractionTrackerPointTag;      // 0x138
};

struct FVehicleDamageRouting final {       // 0x30
    FBHScalableFloat Scalar;               // 0x00
    bool bUseAbsoluteHealth;               // 0x28 — scalar input is absolute health, not a fraction
    bool bOnlyWhenDepleted;                // 0x29
};
```

- **Pre/Post routing:** each target section receives
  `(D − amount already handled) × clamp(Scalar(h), 0, 1)`, where `h` is
  the section's health as a fraction of `MaxHealth`, or its absolute
  health when `bUseAbsoluteHealth` is set. The flag picks the scalar's
  input; it does not route "to absolute health".
- **`bOnlyWhenDepleted`:** set routes only when the section's health is
  ≤ 0. When clear, pre and post routes fire only while health is > 0, but
  simultaneous routes fire at any health, including on the hit that
  depletes the section.
- **Simultaneous routing copies, it does not split:** the target gets
  `clamp(Scalar) ×` the amount this section actually absorbed, in a fresh
  context, and its return value is ignored.
- **Radial flags:** the three unnamed bools skip the Pre, Post or
  Simultaneous map when the event is radial (`FDamageEvent` class ID 2).
- **Loop guard:** routing aborts once a section has been re-entered 10
  times.

**Data**, across 96 sections: 35 Pre routes, 54 Post routes (all
depleted-only), 20 Simultaneous routes. No scalar uses a curve and none
uses absolute health. The radial skip-simultaneous flag is set on 10
sections (the tracks).

## 5. Worked examples

### 5.1 ROT_02 Havoc profile

**Data**, row `Meta.Damage.Vehicle.Air.Rotary.Havoc`, selectable entries
(zero-based index; hit locations omit `Meta.Damage.HitLocation.Vehicle.`):

| # | Category | Op | Amount | Source requires (`Meta.Damage.` omitted) | Hit locations |
|---:|---|---|---:|---|---|
| 1 | Armor | Ongoing | −95 | `Bullet` | any |
| 2 | Armor | Ongoing | −70 | `Cannon` | any |
| 3 | Ricochet | Ongoing | +0 | `Kinetic.Impact.Ricochet` | any |
| 4 | Calibre | Ongoing | +400 | `Explosive.Rocket`, `Explosive.Radius.Inner` | any |
| 5 | Calibre | Ongoing | −20 | `Explosive.Grenade`, `Explosive.Radius.Inner` | any |
| 6 | Armor | Ongoing | −70 | `Bullet.308Win` | any |
| 7 | Calibre | Ongoing | +200 | `Explosive.Utility.ATMine` | any |
| 8 | Armor | Ongoing | −15 | `Explosive.Utility.C4` | any |
| 9 | Armor | Ongoing | +45 | `Explosive.Utility.IED` | any |
| 10 | Armor | Ongoing | −75 | `Explosive.Utility.Claymore` | any |
| 11 | Calibre | Ongoing | −35 | `Cannon.30mm` | any |
| 12 | Calibre | Ongoing | −46 | `Cannon.35x228mm` | any |
| 13 | Calibre | Ongoing | −60 | `Explosive.Rocket.72mm` | any |
| 14 | Calibre | Ongoing | −30 | `Explosive.Rocket.93mm` | any |
| 15 | Calibre | Ongoing | −45 | `Explosive.Rocket.93mm` | MainRotor, TailRotor, Tail |
| 16 | Calibre | Ongoing | −10 | `Explosive.Rocket.120x800mm` | any |
| 17 | Calibre | Ongoing | +30 | `Explosive.Rocket.84mm` | any |
| 18 | Calibre | Ongoing | −5 | `Explosive.Rocket.84mm` | MainRotor, TailRotor, Tail |
| 19 | Calibre | Ongoing | +150 | `Explosive.Rocket.120mm` | any |
| 20 | Calibre | Ongoing | −75.5 | `Cannon.20x102mm` | any |
| 21 | Calibre | Ongoing | −85 | `Explosive.Rocket.122mm` | any |
| 22 | Calibre | Ongoing | −30 | `Explosive.Grenade.40mm` | any |
| 23 | Calibre | Ongoing | +0 | `Explosive.Rocket.155mm` | any |
| 26 | Calibre | Ongoing | +50 | `Explosive.Rocket` | TailRotor |
| 27 | Calibre | Ongoing | +0 | `Explosive.Rocket` | MainRotor |
| 28 | Calibre | Ongoing | +0 | `Explosive.Rocket` | Tail |
| 29 | Calibre | Ongoing | +0 | `Explosive.Rocket` | Engine |
| 31 | Bone | Ongoing | +300 | `Bullet` | FuelTank |
| 32 | Bone | Ongoing | −50 | `Bullet` | Attribute.Gameplay.Health, Attribute.Gameplay.Health.Skids, Attribute.Gameplay.Health.Tail, MainBody, MainRotor, Skids, Tail, TailRotor |
| 33 | Calibre | Ongoing | +450 | `Explosive.Drone` | any |
| 34 | Calibre | Ongoing | +150 | `Explosive.Rocket.125mm` | any |

**Derived.** Every matching entry applies, so entries with the same source
stack:

- a 93 mm rocket hit on a rotor or the tail gets 0.70 (#14) × 0.55 (#15);
  elsewhere only 0.70;
- an 84 mm rocket on a rotor or the tail gets 1.30 (#17) × 0.95 (#18);
- the generic rocket +50 % (#26) applies to tail-rotor hits only;
- bullets: −95 % armor (#1), then +300 % on the FuelTank (#31) or −50 %
  on the body, rotors, tail and skids (#32).

### 5.2 TNK_01 Heavy, inner-radius 125 mm rocket

**Derived.** TNK_01 has three rows (AntiAir, Artillery, Heavy). Its 125 mm
rule is +40, +15 or +31.5 respectively. An inner-radius 125 mm event
also matches Rocket + Inner (+17.5) and #12 (Rocket, `HitLocation.Vehicle`,
0). Result: Heavy 1.315 × 1.175 ≈ **×1.545**; AntiAir ×1.645;
Artillery ×1.351. The generic row adds nothing for a non-HollowPoint
rocket.

The amount then goes to a section. For example, TNK_01's
`Body.StrongArea` first pre-routes 0.4 × D to the main health, takes the
rest itself, and once depleted overflows ×1.0 to the main health
(`VP_TNK_01_Heavy.json`).

### 5.3 Caliber factors by vehicle

**Derived**, `_tools/damage_tables.py --vehicles`: the rule factor for an
FMJ direct hit by each caliber, from the vehicle's own row plus the
generic row. No vehicle rule references a weapon tag, so the caliber
alone decides. Only entries **without** a hit-location filter are
applied: location rules (for example ROT_02's FuelTank +300 % or the
−50 % body rule, §5.1) multiply on top for the section that was hit.
Section routing (§4) then decides where the amount lands. The second
`Stationary.STN_05` row is STN_06's copy (§2.2).

<!-- damage_tables --vehicles -->
| Vehicle row (`Meta.Damage.Vehicle.` omitted) | `556mm` | `762mm` | `762x54mm` | `308Win` | `50Cal` | `20x102mm` | `30mm` | `35x228mm` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `Air.Rotary.Havoc` | ×0.05 | ×0.05 | ×0.05 | ×0.015 | ×0.05 | ×0.0735 | ×0.195 | ×0.162 |
| `Air.Rotary.LittleBird` | ×0.075 | ×0.075 | ×0.075 | ×0.0337 | ×0.075 | ×0.0945 | ×0.595 | ×0.214 |
| `Air.Rotary.ROT_04` | ×0.05 | ×0.05 | ×0.05 | ×0.02 | ×0.05 | ×0.06 | ×0.255 | ×0.128 |
| `Land.Tracked.Leopard.Spawn` | ×1 | ×1 | ×1 | ×1 | ×1 | ×0.048 | ×0.21 | ×0.048 |
| `Stationary.Mistral` | ×0.15 | ×0.15 | ×0.15 | ×0.15 | ×0.15 | ×0.3 | ×0.5 | ×0.3 |
| `Stationary.Phalanx` | ×0.15 | ×0.15 | ×0.15 | ×0.15 | ×0.15 | ×0.3 | ×0.5 | ×0.3 |
| `Stationary.Mortar` | ×0.15 | ×0.15 | ×0.15 | ×0.15 | ×0.15 | ×0.3 | ×0.5 | ×0.3 |
| `Stationary.RadioTower` | ×0.05 | ×0.05 | ×0.05 | ×0.05 | ×0.05 | ×0.3 | ×0.85 | ×0.3 |
| `Stationary.STN_05` | ×0.15 | ×0.15 | ×0.15 | ×0.15 | ×0.15 | ×0.3 | ×0.5 | ×0.3 |
| `Stationary.STN_05` | ×0.15 | ×0.15 | ×0.15 | ×0.15 | ×0.15 | ×0.3 | ×0.5 | ×0.3 |
| `Land.Tracked.TNK_01.AntiAir` | ×0 | ×0 | ×0 | ×0 | ×0 | ×0.045 | ×0.18 | ×0.036 |
| `Land.Tracked.TNK_01.Artillery` | ×0 | ×0 | ×0 | ×0 | ×0 | ×0.045 | ×0.18 | ×0.027 |
| `Land.Tracked.TNK_01.Heavy` | ×0 | ×0 | ×0 | ×0 | ×0 | ×0.045 | ×0.18 | ×0.036 |
| `Land.Tracked.TNK_04.Default` | ×0 | ×0 | ×0 | ×0 | ×0 | ×0.075 | ×0.21 | ×0.048 |
| `Land.Wheeled.Bobcat` | ×0.075 | ×0.075 | ×0.075 | ×0.0262 | ×0.075 | ×0.25 | ×1 | ×0.6 |
| `Land.Wheeled.Patriot.Kodiak` | ×0.05 | ×0.05 | ×0.05 | ×0.025 | ×0.05 | ×0.175 | ×0.5 | ×0.3 |
| `Land.Wheeled.Humvee.Default` | ×0.05 | ×0.05 | ×0.05 | ×0.025 | ×0.05 | ×0.15 | ×0.3 | ×0.15 |
| `Land.Wheeled.Humvee.Minigun` | ×0.025 | ×0.025 | ×0.025 | ×0.0125 | ×0.025 | ×0.12 | ×0.25 | ×0.12 |
| `Land.Wheeled.Humvee.MachineGun` | ×0.04 | ×0.04 | ×0.04 | ×0.02 | ×0.04 | ×0.135 | ×0.225 | ×0.135 |
| `Land.Wheeled.DuneBuggy` | ×0.1 | ×0.1 | ×0.1 | ×0.055 | ×0.1 | ×0.25 | ×0.4 | ×0.35 |
| `Land.Wheeled.Ural` | ×0.05 | ×0.05 | ×0.05 | ×0.0175 | ×0.05 | ×0.125 | ×0.6 | ×0.125 |
| `Land.Wheeled.WHL_08.Default` | ×0.05 | ×0.05 | ×0.05 | ×0.025 | ×0.05 | ×0.16 | ×0.4 | ×0.315 |
| `Land.Wheeled.WHL_08.MachineGun` | ×0.045 | ×0.045 | ×0.045 | ×0.0225 | ×0.045 | ×0.15 | ×0.36 | ×0.305 |
<!-- /damage_tables -->

Every rule that matches applies, so caliber-specific rules stack with the
general ones: on most rows `.308Win` gets both the general bullet rule
and its own −70 %, which is why it scores below 5.56 mm. Tanks take ×0
from small arms.

### 5.4 Hits to destroy

**Derived**, `_tools/damage_tables.py --survive`: for every vehicle
variant, how many direct hits destroy it (main `Attribute.Gameplay.Health`
reaching 0), simulating the rules (§1–2, including the hit section's
hit-location rules) and the section order and routing of §4. Base damage
at point blank, FMJ. Each cell gives the hits on the main body, then,
when some other section is faster, the fewest hits through any one
section and which section. "—" means that section can never destroy the
vehicle: the rules reduce the damage to 0, or it does not route to the
main health.

**Data, assembly.** Each variant (`Variants/VV_*`) names a platform
(`AssemblyData.VehicleBase`). Every enabled slot of the platform, and of
each part placed in it, holds the variant's `SlotOverrides` part for that
dotted slot path (for example `Body`, `Rearback.Chassis`), otherwise the
slot's `DefaultPart`. Health sections come from every enabled
`MVF_HealthSections` fragment of the assembled modules. The damage row is
the `VehicleDamageTag` in the variant's `*GameplaySystems*` asset, reached
through the modules' `DA_*Config` references. STN_06 is left out: its tag
has no row (§2.2).

Assumptions:

- **Health stops at 0:** a section absorbs at most its remaining health,
  and the rest is left for post routing. The attribute hook that would
  clamp it is not traced, but the depleted-only post routes in the data
  only carry damage this way.
- Point hits only (radial flags do not apply); the section-requirement
  filter, repair and regeneration are ignored.

<!-- damage_tables --survive -->
| Variant | Damage row (`Meta.Damage.Vehicle.` omitted) | Main health | `556mm` | `50Cal` | `20x102mm` | `30mm` |
|---|---|---:|---|---|---|---|
| `Attack_ROT_02` | `Air.Rotary.Havoc` | 800 | 1143 / 643 (Wheel.Left.Front) | 356 / 200 (Wheel.Left.Front) | 182 | 42 |
| `ROT_03_Default` | `Air.Rotary.LittleBird` | 400 | 191 | 60 | 71 | 7 |
| `ROT_03_MachineGuns` | `Air.Rotary.LittleBird` | 400 | 191 | 60 | 71 | 7 |
| `ROT_03_RocketPods` | `Air.Rotary.LittleBird` | 400 | 191 | 60 | 71 | 7 |
| `ROT_04_Default` | `Air.Rotary.ROT_04` | 600 | 858 / 429 (Rotor.Tail) | 267 / 134 (Rotor.Tail) | 167 | 24 |
| `ROT_04_MountedMachineGuns` | `Air.Rotary.ROT_04` | 600 | 858 / 429 (Rotor.Tail) | 267 / 134 (Rotor.Tail) | 167 | 24 |
| `SPW_01` | `Land.Tracked.Leopard.Spawn` | 1000 | — | — | 366 | 51 |
| `SPW_02` | `Land.Tracked.Leopard.Spawn` | 1000 | — | — | 366 | 51 |
| `SPW_03` | `Land.Tracked.Leopard.Spawn` | 1000 | — | — | 366 | 51 |
| `STN_01` | `Stationary.Mistral` | 3000 | 715 | 223 | 167 | 60 |
| `STN_02` | `Stationary.Phalanx` | 5000 | 1191 | 371 | 278 | 100 |
| `STN_03` | `Stationary.Mortar` | 3000 | 715 | 223 | 167 | 60 |
| `STN_04` | `Stationary.RadioTower` | 1000 | 715 | 223 | 56 | 12 |
| `TNK_01_AntiAir` | `Land.Tracked.TNK_01.AntiAir` | 800 | — | — | 312 | 47 |
| `TNK_01_Artillery` | `Land.Tracked.TNK_01.Artillery` | 650 | — | — | 254 | 39 |
| `TNK_01_Heavy` | `Land.Tracked.TNK_01.Heavy` | 800 | — | — | 312 | 47 |
| `TNK_04` | `Land.Tracked.TNK_04.Default` | 750 | — | — | 176 | 38 |
| `WHL_01_Default` | `Land.Wheeled.Bobcat` | 200 | 96 / 64 (Wheel.Left.Front) | 30 / 20 (Wheel.Left.Front) | 14 | 2 |
| `WHL_02_Default` | `Land.Wheeled.Patriot.Kodiak` | 400 | 572 / 143 (Wheel.Left.Front) | 178 / 45 (Wheel.Left.Front) | 39 | 8 |
| `WHL_02_Pickup` | `Land.Wheeled.Patriot.Kodiak` | 400 | 572 / 143 (Wheel.Left.Front) | 178 / 45 (Wheel.Left.Front) | 39 | 8 |
| `WHL_02_SUV_RingTurret` | `Land.Wheeled.Patriot.Kodiak` | 400 | 572 / 143 (Wheel.Left.Front) | 178 / 45 (Wheel.Left.Front) | 39 | 8 |
| `WHL_05_Humvee_Default` | `Land.Wheeled.Humvee.Default` | 500 | 715 / 129 (FuelTank) | 223 / 40 (FuelTank) | 56 | 17 |
| `WHL_05_Humvee_RingMinigun` | `Land.Wheeled.Humvee.Minigun` | 500 | 1429 / 258 (FuelTank) | 445 / 80 (FuelTank) | 70 | 20 |
| `WHL_05_Humvee_RingTurret` | `Land.Wheeled.Humvee.MachineGun` | 500 | 893 / 161 (FuelTank) | 278 / 50 (FuelTank) | 62 | 23 |
| `WHL_06_DuneBuggy_Default` | `Land.Wheeled.DuneBuggy` | 400 | 286 / 84 (FuelTank) | 89 / 26 (FuelTank) | 27 | 10 |
| `WHL_07_Battle` | `Land.Wheeled.Ural` | 700 | 1000 / 175 (FuelTank) | 312 / 55 (FuelTank) | 94 | 12 |
| `WHL_07_Default` | `Land.Wheeled.Ural` | 700 | 1000 / 175 (FuelTank) | 312 / 55 (FuelTank) | 94 | 12 |
| `WHL_07_ArmouredBattle` | `Land.Wheeled.Ural` | 700 | 1000 / 175 (FuelTank) | 312 / 55 (FuelTank) | 94 | 12 |
| `WHL_08_Default` | `Land.Wheeled.WHL_08.Default` | 500 | 715 / 204 (Wheel.Left.Front) | 223 / 63 (Wheel.Left.Front) | 53 | 13 |
| `WHL_08_RingTurret` | `Land.Wheeled.WHL_08.Default` | 500 | 715 / 204 (Wheel.Left.Front) | 223 / 63 (Wheel.Left.Front) | 53 | 13 |
<!-- /damage_tables -->

## 6. Top damage source tags

**Data**, counted over selectable entries in all 23 rows:

| Source tag | Entries |
|---|---:|
| `Meta.Damage.Bullet` | 95 |
| `Meta.Damage.Explosive.Rocket` | 57 |
| `Meta.Damage.Explosive.Radius.Inner` | 36 |
| `Meta.Damage.Cannon.20x102mm` | 24 |
| `Meta.Damage.Explosive.Grenade` | 23 |
| `Meta.Damage.Explosive.Utility.IED` | 23 |
| `Meta.Damage.Cannon.30mm` | 23 |
| `Meta.Damage.Cannon.35x228mm` | 23 |
| `Meta.Damage.Explosive.Rocket.120mm` | 23 |
| `Meta.Damage.Explosive.Rocket.125mm` | 23 |
| `Meta.Damage.Explosive.Utility.C4` | 22 |
| `Meta.Damage.Explosive.Rocket.120x800mm` | 22 |

Every row has a `Meta.Damage.Bullet` rule.

## 7. Open questions

| # | Question | What closes it |
|---|---|---|
| V-1 | `RootDamageTag`'s value, which decides whether the generic `Meta.Damage.Vehicle` row is evaluated | The `UWDGlobalDamageSystem` instance's config (not in the export) |
| V-2 | How `ModifyDamage` copies the entity component's tag into the target tag | `0x6EF8DE0` / `0x6F01BB0`, which did not decompile; disassembly |
| V-3 | What happens when the zone query resolves to no section | `0x5338730` and the section lookup |
| V-4 | Which source tags a vehicle collision event carries, which the stationary `Add` entries depend on | The collision damage caller |
| V-5 | Whether a HollowPoint tag ever reaches a vehicle event | Projectile path with ammo variants against vehicles |
| V-6 | Network authority | Not observable statically; security questions go through [`SECURITY.md`](SECURITY.md) |

## 8. Cross-references

- [`Wardogs_DamagePipeline_v2.md`](Wardogs_DamagePipeline_v2.md): the shared rule pipeline (§1–6)
- [`Wardogs_AllVehicles_Stats_Damage_v1.md`](Wardogs_AllVehicles_Stats_Damage_v1.md): per-vehicle stats and the damage tables entry by entry
- [`Wardogs_GameFeatures_Vehicles_v2.md`](Wardogs_GameFeatures_Vehicles_v2.md): vehicle game-feature loadouts
- [`sdk/raw/Mechanized_structs.hpp`](sdk/raw/Mechanized_structs.hpp): `FVehicleDamageRouting` (L511), `FVehicleHealthSection` (L523)

## Change log

| Date | Change |
|---|---|
| 2026-10-16 | v1: first trace of the per-vehicle tables, ROT_02 profile and section structures. |
| 2026-10-17 | Rewritten against the decompilation corpus and the damage doc. Vehicles use the same rule pipeline as infantry (the "fundamentally different" claim is withdrawn); target tag from `VehicleDamageTag`; the generic row is a parent level, not a fallback; `PriorityIndex` is overwritten (array order decides nothing); 5 `Add` entries; corrected counts (21 files, 23 rows, 665 entries) and row keys; ROT_02 duplicates explained by hit locations; section order and routing semantics traced; STN_06 keying and nine unreachable entries flagged. |
| 2026-10-17 | Added caliber factors for every vehicle row (§5.3), generated by `_tools/damage_tables.py --vehicles`. |
| 2026-10-17 | Added hits to destroy for six vehicles (§5.4): rules plus section routing, simulated by `--survive`. |
| 2026-10-17 | §5.4 now covers all 30 variants with a damage row, assembled from the variant data (platform, slots, overrides) instead of hand-picked modules; flagged the unreachable `WHL_08.MachineGun` row. |
| 2026-10-17 | Independent verifier pass: the destroy routine is not the reflected `DestroyVehicle`; when post routing runs; simultaneous routing fires at any health when `bOnlyWhenDepleted` is clear; the section pick's pre-gate, zone-miss case and thunk path. |
| 2026-10-17 | Added §3.1 Hitboxes: hits resolve through the complex-surface collision slots, mapped to sections by `ComplexSurfaceMappings`; per-vehicle slot map with section health, routing and rule factors (`--hitboxes`). |
