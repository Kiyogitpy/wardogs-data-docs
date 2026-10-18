---
title: "Vehicle Damage Pipeline"
parent: "Pipelines"
nav_order: 2
redirect_from: ["/Wardogs_VehicleDamagePipeline_v1.html", "/Wardogs_VehicleDamagePipeline_v1"]
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
infantry hit does. The projectile path (`0x6B725B0`, at `0x6B733AC`),
the radial path (`0x6F06540`), the back-blast path `0x6F042A0` and the
collision path `0x76740F0` (V-4) fetch the vehicle hit tag through
`0x6B80230` before the call. The result is
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
(`0x6B18E70`) with `DA_GameplaySystems_*.DamageEntitySettings.VehicleDamageTag`,
only when that tag is not None.
For 20 of the 21 vehicles that tag equals the vehicle row key exactly
(STN_06 is the exception, §2.2).

**The walk** (damage doc §5). The collector evaluates every level of the
target tag's parent chain that has a registry row, most specific first,
stopping before `RootDamageTag`, which is `Meta.Damage` (set in the
system's constructor `0x6BB6160`). Vehicle tables use the same
`FWDDamageableEntityTableRow` and are added to the `GlobalDamageData`
registry by each vehicle's GameFeature (for example
`Vehicles/ROT_02/Content/ROT_02.json`, `RegistryToAddTo: GlobalDamageData`).
So a Havoc hit evaluates its own row (`…Air.Rotary.Havoc`), then any
parent rows, then the generic `Meta.Damage.Vehicle` row, since the walk
runs up to the root `Meta.Damage` above it. The generic
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
[`DT_GlobalDamage_VehicleData`](../data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_VehicleData.json).
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

- **STN_06 is wrongly keyed.** Its table is a byte-identical copy of
  STN_05's (row `…Stationary.STN_05`), but its `VehicleDamageTag` is
  `Meta.Damage.Vehicle.Stationary.MGNest`
  (`DA_GameplaySystems_STN_06.json`). The tag is registered: the shipped
  `DefaultGameplayTags.ini` (in the paks) lists it, together with
  `…WHL_08.Default` and `…TNK_04.Default`. The exported copy under
  `data/Wardogs/Config/` is a different version of that file (3622 lines
  against 3897) and lacks all three. No table has a `…Stationary` or
  `…MGNest` row, so STN_06's walk is `…Stationary.MGNest` →
  `…Stationary` → `Meta.Damage.Vehicle`. It never reaches the STN_05
  rows; only the generic row applies: ×0.84 for HollowPoint ammo,
  otherwise no change.
- **STN_05's row is registered twice.** Both GameFeatures add their table
  to `GlobalDamageData` at priority 0. Sources are kept in descending
  priority by a stable sort, so ties stay in insertion order
  (`0x46EC5B0` → `0x46EDC20` → `0x46E3930`), and the lookup takes the
  first source that has the row (`0x46ED100`). The two rows are
  byte-identical, so the load order does not matter.
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
interface at `+0x338`) resolves the hit to its slot (`0x50BF880`). The
damage model then looks up the pair (surface group, slot) in its table
(component `+0x180`, `0x53952A0`): the slot's section if the group maps
it, else the group's default section, else the same lookup in the parent
group (while it is under `ComplexSurface.Group`), else no section. When
the query misses on a point or radial hit, the section tag is empty
(§4.1). The vehicle's physics asset (for example `PA_ROT_02`: one body,
`body_J`, with 22 collision shapes) plays no part, because the slot
lookup needs a static-mesh component. The exact rule is in §3.2.

**Data.** The table comes from `MVF_HealthSections.ComplexSurfaceMappings`
in the platform and part files: per surface group, a slot map
(`CC_FuelTank` → `Attribute.Gameplay.Health.FuelTank`, …), and a default
section (usually the main health) for every slot not listed. The section
registration (`0x53214A0`, run for each `MVF_HealthSections` fragment)
merges this struct (fragment `+0x90`) into the component's table
(`+0x180`, `0x538ABD0`), and `PhysicsGroupMappings` (`+0xE0`) into
`+0x1D0` (`0x53167B0`). Per surface group, slot pairs are added (only
values under `Attribute.Gameplay.Health`), and the group's default is overwritten, so
the last fragment's default wins. The zone query never reads `+0x1D0`.
`ApplyCollisionDamage` (slot 160, `0x531FC20`) and `0x532D4C0`, on the
component-hit path (`0x767E640`), read it: they resolve a physics-group
tag from the hit body (`0x50F41D0`) and walk parent tags.

**Data, collision meshes.** The slots live on dedicated low-poly
collision meshes, separate from the render models. Each render static mesh
names its collision mesh in `UStaticMesh.ComplexCollisionMesh`. For the
Havoc: `SM_ROT_02_Body` → `CC_ROT_02_Body_01a`, plus the wheels, doors,
main and rear rotor hubs and blades (9 collision meshes, under
`Meshes/ComplexCollision/`); the missile pods and reticle have none. The
rotors are placed by an `MVF_DestructibleMeshes` fragment
(`Vehicle.DestructibleMesh.Rotor.Main` / `.Tail`), attached to the chassis
skeleton's `mainRotorSpin_J` and `rearRotorSpin_J` bones. The rotor hub
and blade meshes register in `ComplexSurface.Group.Default`, so
`CC_MainRotor` / `CC_TailRotor` use the same map; the spinning meshes do
not register (`VP_ROT_02.json`, `bRegisterComplexSurface`). The hubs
use `MVCT_QueryProxy`, which always applies the `VehicleQueryProxy`
profile (`0x50EEE90`; the entry's `NoCollision` name is ignored):
query-only, blocking Visibility and projectile traces. So hub hits
resolve to `CC_MainRotor` / `CC_TailRotor`. The blades use
`WDRotorCollision`. That profile (query-only, object type `WDRotor`) does
not override Visibility or `WDProjectile`, so both block. Projectile hits
trace the Visibility channel with every response set to Block
(`0x6F3C75A`, response params from `0x6B8E100`), so bullets hit the
blades. Sweeps using the `ProjectileSweep` profile (the projectile actor,
`0x76D40A0`) ignore `WDRotor` objects and would pass through. The rotor
component's own `DefaultCollisionProfile` (`+0x670`) is `MVCT_Physics` /
`NoCollision` from the constructor (`0x5304690` → `0x50E0AD0`), and no
native code applies it, so the hubs keep the registration's
`VehicleQueryProxy`. The only native later switch found is the
destructible-group toggle (`0x53BC420`, bound by `0x53C1490`). When the
component's damage-model group is destroyed, or the vehicle is
(`bIsVehicleDestroyed`), it hides the component and sets `NoCollision`;
when shown again it re-applies the stored profile. Whether the rotor hubs
belong to such a group is not traced. A collision mesh's material slots are the `CC_*` names, each
with a collision material (for example `CC_FuelTank` → `MI_VehicleCC_FuelTank`,
`CC_Main` → `MI_VehicleCC_Metal_ReinforcedArmored`, `CC_TailRotor` →
`MI_VehicleCC_Metal_Weak`), and its render data holds the triangles per
slot (`CC_ROT_02_Body_01a`: about 1,450 triangles over 7 slots). Slots not
in the map, such as `CC_Main`, `CC_Glass` and `CC_Fabric`, take the
default section. Stationary vehicles place such proxies directly as mesh
fragments (`Meshes/ComplexCollisions/ComplexProxy/`). STN_06's gun proxy
(`Browning_Gun_Proxy`, `CC_Gun`) asks for socket `receiver_J` on
`TurretSkeleton`, but `SK_Browning_Mounted` has no bone or socket of that
name. The attach code (`0x50EE770`) then reports a partial match
(`0x50EBDE0`). That attaches at the skeleton component's origin only if
the vehicle allows partial attachments (`bEnablePartialAttachments`,
`0x50EF920`); otherwise the proxy is never attached. Nothing in `data/`
sets that flag, so the proxy is probably never attached; the flag's
runtime value is unverified. The proxy is query-only `VehicleQueryProxy`
and registers, so it is hittable wherever it ends up; that position is
not traced. Decoding these
meshes needs the static-mesh usmap fixes in
[`tools/cue4parse_extractor`](../tools/cue4parse_extractor/README.md).

**Derived**, `_tools/damage_tables.py --hitboxes`: every vehicle's map,
with the section's maximum health, how the section passes damage to the
main health (§4.2), and the rule factor at that hitbox for an FMJ direct
hit (§1–2; the section's hit-location tag selects location rules).
Variants that share a damage row and map are listed together. "none"
means hits there never reach the main health. Rows marked "unreachable"
are map keys that no registered component can produce (§3.2).

Interactive: the [Vehicle Hitbox Viewer](vehicle-viewer.md) shows these slots on each vehicle's collision mesh.

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

### 3.2 From a hit triangle to a section

**Native** (`0x50BF880`, `0x53952A0`, the component registrations
`0x50F06E7` and `0x53A00C6`). For one hit, the inputs are the vehicle's
registered static-mesh components, the component that was hit, the
triangle index within that component's collision mesh and, for instanced
wheels, the instance.

1. **Component.** A hit on anything but a static-mesh component gives no
   section: skeletal meshes, physics-asset bodies, weapons on skeletal
   meshes. So does an unregistered component (`MVF_StaticMesh` with
   `bRegisterComplexSurface` off, destructible entries with it off such as
   the rotor spin meshes, a disabled fragment). `MVF_StaticMesh` and
   `MVF_InstancedWheels` register by default; destructible entries use
   their own flag.
2. **Collision mesh.** The mesh's `ComplexCollisionMesh` if set, otherwise
   the mesh itself.
3. **Slot.** The material slot name of the hit triangle's material index:
   `StaticMaterials[MyItem].MaterialSlotName`. The engine fills `MyItem`
   from the triangle when the trace asks for face indices and the hit
   shape is a triangle mesh; projectile traces are complex and ask for
   face indices (`0x6B8E2F4`, `0x6F30F70`). Physical materials and bone
   names are not read.
4. **Group.** The component's `SurfaceGroup`: `ComplexSurface.Group.Default`
   for `MVF_StaticMesh` and `ComplexSurface.Group.Wheel` for
   `MVF_InstancedWheels` unless set, the explicit value for destructible
   entries, and an instanced wheel's per-instance override when set.
5. **Indexed names, instanced wheels only.** A slot listed in the wheel
   fragment's `IndexedSlotNames` (and not already numbered) gets the
   wheel's `DataIndex`, held in the instance's remap entry, not the
   instance's position in the instanced mesh, which changes when wheels
   are deactivated: `CC_Wheel` → `CC_Wheel_2` (`0x50BF500`). Static meshes
   never get a suffix.
6. **Lookup.** In the merged map (§3.1), starting with the component's
   group: the slot's section if the group maps the slot; else the group's
   default section if it has one; else repeat in the parent group, while
   that is still under `ComplexSurface.Group`; else no section, an empty
   section tag, which is not the main health (§4.1).
   `ComplexSurface.Group.Default` is not a parent of
   `ComplexSurface.Group.Wheel`, so unmapped wheel slots do not take the
   default group's default.

This holds for projectile hits, radial hits and the back-blast path
`0x6F042A0`. The radial gather (`0x6EFFDC0`) line-traces each overlapped
component on the Visibility channel with complex collision and face
indices (`0x6F0005A`), and a vehicle keeps only hits that block on the
traced component itself, for an instanced wheel on the same instance
(`0x6F03720`). So radial hits fill `MyItem` and resolve by the same rule.
A component whose trace is blocked by something else gets no hit. Only
`WDC4` and `WDDestructionBuilding` targets get synthetic hits (`FaceIndex`
0, `MyItem` 0), per `DamageSystemSettings`. The other back-blast path
(`0x6F06EB0`) runs only when the shooter sits in a vehicle seat. It does
not trace: it builds a synthetic hit (`0x3EAF060`: face index 0, material
index 0) on the first primitive component of each occupant of that
vehicle, so no vehicle section is involved; the vehicle itself takes the
back-blast self-damage effects directly in `0x6B92900`. The branch
depends on the shooter: on foot `0x6F042A0`; seated in a vehicle
`0x6F06EB0`, whose targets are that vehicle's occupants, so its synthetic
hit lands on characters, not on a vehicle
([DamagePipeline §1.1](Wardogs_DamagePipeline_v2.md#11-callers-and-where-the-result-goes)).

The collision path (`0x76740F0`) and explosive impacts (`0x6CA8730`) use
an `OnComponentHit` hit. For physics contacts the engine builds it in
`0x3A90520`: zeroed (`FaceIndex` 0), `Component` = the damaged component,
and `MyItem` = the hitting body's `InstanceBodyIndex` (`0x42D9EF0`), not a
material index. A single-body hitter (a thrown explosive's mesh) gives −1,
which fails the slot lookup (`0x50BF9FD`): no section. A skeletal vehicle
body gives its body index, read as a material slot of the damaged mesh.
Hits from movement sweeps (`0x3A902D0`) are not traced.

In the data, ROT_02's wheels are static meshes, so their slots (`CC_Wheel`
on the right wheel, `CC_Tyre` on the left, `CC_Main` on both) resolve to
the main health and the map keys `CC_Wheel_0` / `CC_Wheel_1` never match.
That assumes no static mesh has a slot literally named `CC_Wheel_0`; the
decoded ROT_02 wheel meshes do not, and the other meshes are not checked
(V-9). WHL_* wheel slots `CC_Wheel` (and `CC_Tyre` on WHL_05 to WHL_08)
become `CC_Wheel_n` and `CC_Tyre_n`. No component registers
`ComplexSurface.Group.Radar`, so the SPW radar rows cannot be hit.

**Wheel index.** The wheel index is the movement component's order: axle
by axle, then the axle's own wheel order (`0x5370A40`). The
instanced-wheel setup assigns each wheel's `DataIndex` from the same
axle-major enumeration (`0x5365660`, `0x539ABB9`), so the `_n` suffix is
that wheel index. The lists line up: the movement component builds each
axle's runtime wheels from its `WheelSetup` list, one per entry and in
order (`0x53999B0`), but only for an axle with exactly two setup wheels
(`0x53999CF`). Every shipped axle asset has two (left, then right). An
axle with any other count would get no runtime wheels, and the two
numberings would diverge.
`GetWheelAxleSideFromIndex` (`0x76AB5F0`) reads index i as axle 'rear'
when i ≥ 2 and side i & 1; this matches the four-wheel maps (`_0` left
front … `_3` right rear). WHL_07 has three axles, and its indices 2-5 all
read as rear.

**Wheel mesh swap.** The movement component keeps a state byte per wheel
(`+0x9B0`: 0 intact, 1 deflated, 2 destroyed). When one changes,
`0x5370A40` broadcasts (wheel index, old, new). Each wheel ISM's handler
`0x5336DD0`, bound by `0x53303F0`, then calls `SetWheelActive`
(`0x533B6F0`), `SetWheelUseAlternativeCollision` (`0x533BAE0`) and
`SetWheelMaterialParams` (`0x533BA20`) for that wheel. With
`bSupportTyreDestruction` and a mode set to `All`, the wheel is
deactivated on the intact ISM and activated on the destroyed ISM at state
2, or at state 1 when `DeflatedMeshMode` is `All` (`0x539B6E7`).
`CollisionOnly` switches the intact ISM to the alternative collision hull
instead. That hull is the `DestructionMesh`'s `BodySetup` (`0x5389A46`): its
simple shapes plus the complex trimesh cooked from its
`ComplexCollisionMesh` (inferred from cooked sizes; the blob is not parsed).
A hit on it takes the slot name from the hit component's own collision
mesh and the index from the hull triangle, which is 0 on WHL_05 and WHL_08
(`0x50BF880`), so a deflated wheel there gives `CC_Wheel_n`. `SetupWheels` receives it for the intact ISM
when `bSupportTyreDestruction` is set and either mode is `CollisionOnly`
(`0x5389990`); the destroyed ISM gets none, and no asset names the hull
separately. Every wheeled vehicle uses the defaults (deflated
`CollisionOnly`, destroyed `All`). So at state 1 the wheel keeps its
intact mesh and collides with the destruction mesh's hull (WHL_05:
`SM_Humvee_Wheel_RearRight_Destroyed`), and at state 2 it swaps to the
destruction mesh. WHL_05: destroyed mesh at state 2, alternative
collision from state 1.

The state byte is written only by `0x537C580`, an attribute-change
handler. At set-up (`0x5356B00`, end of the movement component's vtable
slot 202) the component binds one handler per wheel on the vehicle's
`GameplayEffectComponent` (`0x5229630`), keyed by that wheel's
`TyreHealthAttribute` (`Attribute.Gameplay.Health.Wheel.<side>.<axle>`).
On a change to value v the state becomes 2 if v ≤ 0, 1 if
v / max(MaxHealth, 1) ≤ `DeflateThreshold` (0.55 on every axle asset;
MaxHealth comes from the damage model's section map at `+0x130`), and 0
otherwise. `0x5370A40`, called on every update from slot 206
(`0x537C260`), compares the bytes with its cache (`+0x9D8`) and
broadcasts the changes. So a wheel deflates at 55% of its section health
and is destroyed at 0. The rule is checked in the executable; the
single-writer scan, the binding chain (`0x5356B00` → `0x5229630` →
`0x5229EAF`) and MaxHealth being the section's maximum were not
re-derived by the verifier.

## 4. Section application

### 4.1 Order

**Native.** After the rules, `ApplyWDDamage` hands the amount to the
vehicle damage model:

1. **Pick the section** (`ApplyDamageEvent`, `0x53202B0`, which then
   calls `0x5320400`; the reflected exec thunk `0x5341430` repeats the
   pick inline and calls `0x5320400` directly, without passing through
   `0x53202B0`). A pre-gate requires the
   authority role, an amount above `1e-8` and two owner checks. Point
   damage uses the zone query `0x5338730` on the hit info. Radial damage
   uses it on `ComponentHits[0]` (`0x5320394`). Before that, the vehicle's
   `IWDDamageable` slot 8 (`0x6C2A790`) keeps one hit per component, so an
   instanced-wheel component contributes one wheel. Every application from
   one explosion on one vehicle takes its section from that first hit,
   while the rule's hit-location tag comes from each hit (`0x6F06540`).
   Each radial amount is the falloff amount of the round's radii, not
   `BaseDamage` ([Damage pipeline §1.1](Wardogs_DamagePipeline_v2.html#11-callers-and-where-the-result-goes)).
   Any other event falls back to `Attribute.Gameplay.Health`.
   When the zone query misses on a point or radial hit, the section tag is
   empty rather than the main health. That application then does nothing:
   `0x53205D0` returns 0 before routing (V-3).
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
[`FVehicleHealthSection`](../sdk/raw/Mechanized_structs.hpp#L523) and
[`FVehicleDamageRouting`](../sdk/raw/Mechanized_structs.hpp#L511).

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
through the modules' `DA_*Config` references, together with the rows on
that tag's parent walk. STN_06 has no row of its own, so only the generic
row applies (§2.2).

**Native, assembly** (`0x50E7200`, `0x50E7140`; disassembly only, no
corpus bodies). The game follows the same chain, with three points that
no data exercises:

- Two more override layers: a variant can be built on another variant
  (`0x50E7140` recurses into it), and the vehicle actor's own
  `AssemblyData` (`+0x3A0`) is applied last.
- When two health sections share a key, the first one registered wins
  (`0x53214A0`). No variant repeats a key.
- A variant's `CustomFragmentData` can replace the vehicle config
  (`0x53B6190`). The 10 variants that have any only override meshes and
  materials.

**Health stops at 0** (native): a section absorbs at most its remaining
health, and the rest is left for post routing. Each section attribute
gets a base-value and a current-value hook (registered in `0x53214A0`
through `0x5236990` / `0x5236C70`, map at the attribute component's
`+0x378`), both bound to `0x533A750`, which clamps the new value to
`[0, MaxHealth]`. The reduction helper `0x52311D0` returns the change
actually applied, so the absorbed amount never exceeds the remaining
health.

Assumption: point hits only (radial flags do not apply); the
section-requirement filter, repair and regeneration are ignored.

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
| `STN_06` | `Stationary.MGNest` | 1800 | 65 | 20 | 30 | 18 |
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
| V-1 | **Closed** (§1): `RootDamageTag` is `Meta.Damage` and is never evaluated, so the walk reaches the generic `Meta.Damage.Vehicle` row | Constructor `0x6BB6160`; the walk in `0x6BB6A60` |
| V-2 | **Closed**: `0x6EF8DE0` keeps the event's `TargetEntityData` when its tag is set. Only when the tag is None does it resolve the target actor (`TargetEventData.Actor`, else the controller's pawn), find its `UWDDamageEntityComponent` (`0x6F01820`) and copy that component's `DamageEntityData` (`+0xE0`: tag, context and cause tag) into the target data. Inside the same branch, an empty hit-location tag is filled from `ClassToHitLocations` by bone name (`0x6F01BB0`). The instigator data always comes from the instigator's component, and the source data is copied from the event | `0x6EF8DE0` (disassembly), `0x6F01820` (disassembly), `0x6F01BB0` |
| V-3 | **Closed**: a zone-query miss gives an empty section tag (§3.1, §4.1), and `ApplyDamageToSection` (`0x53205D0`) finds no section for it in the component's section map (`+0x130`, `0x532B660`) and returns 0 at once (`0x5320670`), before PreDamageRouting. So such a hit does nothing to the vehicle | `0x53205D0`, `0x532B660` |
| V-4 | **Closed**: the collision path (`OnMeshHitEvent` `0x768A280` → `0x767E640` → `0x76736C0` → `0x76740F0`) uses the ramming vehicle's own `DamageEntityData` as the source (tag = its `VehicleDamageTag`, or `Meta.Damage.Landscape` when empty) and adds `Meta.Damage.DamageType.Impact` to the source context. So the stationary `Add +1000` entries (source `Meta.Damage.Vehicle.Land.Tracked`) fire when a tracked vehicle rams the stationary | `0x76740F0` (`0x7674428`, `0x7674435`) |
| V-5 | **Closed** (static): the projectile path copies the ammo-variant stats' context, which holds the ammo-modifier tag ([DamagePipeline §7.9](Wardogs_DamagePipeline_v2.md#79-ammo-type-against-armor)), into the source context before the vehicle branch, and no vehicle class has a pre-`ModifyDamage` hook that strips it. So HollowPoint rounds meet the generic ×0.84 pair and the per-vehicle Bullet+HollowPoint entries. The ammo tag (instance `+0xF0`, empty from the constructor `0x6B8E100`) is set by `0x6F30E50` from the spawn parameters. On the fire path the weapon owner (`IWDWeaponOwner` `+0x90`, `0x6C98290`) builds `Meta.Damage.AmmoModifier.<type>` from the loaded round's item tag; predicted simulations use `FWDProjectileSimulationSetup.AmmoModifierTag` (`0x6F2C450`). The `<type>` rule is in [DamagePipeline §7.9](Wardogs_DamagePipeline_v2.md#79-ammo-type-against-armor) | `0x6B725B0`; `0x6F30E50`; `0x6C98290` |
| V-6 | Network authority | Not observable statically; security questions go through [`SECURITY.md`](../SECURITY.md) |
| V-7 | **Closed** for physics contacts (§3.2): `0x3A90520` builds the `OnComponentHit` hit with `FaceIndex` 0 and `MyItem` = the hitting body's `InstanceBodyIndex` (`0x42D9EF0`), so a single-body hitter gives −1 and no section. Open: sweep-sourced hits (`0x3A902D0`) | Engine code that builds sweep hits (`0x3A902D0`) |
| V-8 | **Closed** (§3.2): the shooter's seat picks the branch of `0x6B92900`. `0x6E6EBA0` returns the vehicle whose seat the shooter occupies (`VehicleOperatorComponent.CurrentSeat`, owner a `BHBaseVehiclePawn`). On foot, `0x6F042A0` traces the cone; seated, `0x6F06EB0` hits only that vehicle's occupants, and `0x6B92900` applies the self-damage map straight to the vehicle ([DamagePipeline §1.1](Wardogs_DamagePipeline_v2.md#11-callers-and-where-the-result-goes)) | `0x6E6EBA0`, `0x532DD70`, `0x6F06EB0` |
| V-9 | Whether a literally numbered material slot (such as `CC_Wheel_0`) ever exists on a static mesh. The generator assumes not, which holds for the decoded ROT_02 wheel meshes | Decode every registered static mesh's collision mesh |
| V-10 | **Closed** (§3.2): the wheel index order, the `DataIndex` assignment and the mesh swap are traced. The state byte (`+0x9B0`) is written only by `0x537C580` from the wheel's `TyreHealthAttribute` (2 at ≤ 0, 1 at ≤ `DeflateThreshold` 0.55 of max), and the runtime wheels are built one per setup entry, in order, for two-wheel axles (`0x53999B0`, `0x53999CF`); every shipped axle has two | `0x537C580`, `0x53999B0` |

## 8. Cross-references

- [`Wardogs_DamagePipeline_v2.md`](Wardogs_DamagePipeline_v2.md): the shared rule pipeline (§1–6)
- [`Wardogs_AllVehicles_Stats_Damage_v1.md`](../content/Wardogs_AllVehicles_Stats_Damage_v1.md): per-vehicle stats and the damage tables entry by entry
- [`Wardogs_GameFeatures_Vehicles_v2.md`](../game-features/Wardogs_GameFeatures_Vehicles_v2.md): vehicle game-feature loadouts
- [`sdk/raw/Mechanized_structs.hpp`](../sdk/raw/Mechanized_structs.hpp): `FVehicleDamageRouting` (L511), `FVehicleHealthSection` (L523)
- [`docs/evidence/vehicles.md`](../docs/evidence/vehicles.md): evidence behind the native addresses, with a verification status for every RVA this page cites

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
| 2026-10-17 | Another independent verifier pass: closed V-1 (`RootDamageTag` is `Meta.Damage`); the exec thunk does not pass through `0x53202B0`; the health clamp is traced (`0x533A750`), so "health stops at 0" is native, not an assumption; native assembly adds two unused override layers, first-registered section wins and config replacement (§5.4); the STN_06 tag-absence argument is softened; the code that fills the slot-to-section table is `0x53214A0` (§3.1). The §5.4 chain for all variants and the Main health column were confirmed. |
| 2026-10-17 | Round-4 verifier pass: STN_06's tag is registered (shipped `DefaultGameplayTags.ini`), so only the generic row applies; it is now in §3.1 and §5.4. STN_05's duplicate row resolved. The slot lookup is keyed by (surface group, slot) with defaults and a parent-group walk; new §3.2 gives the exact face-to-section rule; `--hitboxes` marks unreachable keys (ROT_02 `CC_Wheel_0`/`_1`, the SPW radar group). V-2, V-4 and V-5 closed; physics-group table readers and rotor registration added. |
| 2026-10-17 | Round-5 verifier pass: the wheel suffix is the wheel's `DataIndex`, not the instance's position (§3.2 step 5); ROT_02's left wheel has `CC_Tyre`; the `+0x180` / `+0x1D0` merge citations were swapped (§3.1). Radial and `0x6F042A0` back-blast hits carry face indices; the `0x6F06EB0` back-blast uses a synthetic hit on material slot 0. Radial damage takes its section from `ComponentHits[0]` after one hit per component (§4.1). Added the wheel index order, the wheel mesh swap, the rotor hub profile and the ammo-tag writer (V-5). New open rows V-7 to V-10. |
| 2026-10-18 | Round-6 verifier pass: the `0x6F06EB0` back-blast runs only for a seated shooter and hits that vehicle's occupants, not the vehicle (corrects round 5); the branch is the shooter's seat (V-8 closed). Physics-contact hits carry the hitter's body index in `MyItem`, so a single-body hitter finds no section (V-7 closed for contacts). A hit with no section does nothing (V-3 closed). Wheels: the state-byte writer and rule (deflated at 55%, destroyed at 0), the setup / runtime lists line up for two-wheel axles, WHL_07's index caveat and the deflated hull (V-10 closed). Rotors: blades block bullet traces; the rotor default profile is never applied. STN_06's gun proxy is probably never attached. V-5 points to DamagePipeline §7.9. |
| 2026-10-18 | Radial amount is the verified falloff (Damage pipeline §1.1); the vehicle viewer has a "Blast at distance" view. |
| 2026-10-18 | Round-7 BA-2/BA-3: the deflated hull is the destruction mesh's `BodySetup` with its trimesh; slot name from the hit component's mesh, index from the hull (`0x50BF880`). |
