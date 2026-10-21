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

Offline native replay now covers event conversion, configured system
activation and ModifyDamage dispatch for all 63 retained critical blast
contacts, matching final float32 amounts and modification records. These
fixtures supply UObject, registry and lifecycle services; see the
[round 11 evidence boundaries](../docs/ROUND11_STATUS.md#native-event-conversion-activation-and-dispatch).
The later handoff replay also covers 20 complete retained health sequences
(46 applications), through native context copy, interface fallback and section
routing. Its supplied world/lifecycle and context-attachment boundaries are
recorded in the [handoff evidence](../docs/ROUND11_STATUS.md#native-damage-context-dispatch-through-vehicle-health).
The complete radial caller now also runs from entry to return with an owned
one-actor gather, including filtering and typed context assembly; see the
[radial caller scope](../docs/ROUND11_STATUS.md#complete-radial-caller-assembly-after-owned-gathering).

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
Native parent matching also accepts the exact `Meta.Damage.HitLocation`
root. Round 11 replay verifies all 154 exported slots and the root/default/
inheritance boundaries; the export compiler now includes that root case.

The replayed vehicle acceptance method (`0x76B63E0`) permits a target outside
`State.Location.SafeZone`, or inside `State.Location.SafeZone.Hostile`.
Its native cached-tag query follows explicit and parent tags. This is one
vehicle interface table with owned cached state, not captured runtime state
for every vehicle class; see the
[lookup and acceptance evidence](../docs/ROUND11_STATUS.md#native-hit-location-lookup-and-safe-zone-acceptance).

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
when shown again it re-applies the stored profile. Native setup registers
the cooked hub/base and blade entries in their Main/Tail groups; the health
callback selects that group and the visibility callback visits every member.
Thus hubs and blades toggle together, each restoring its own saved profile.
See [the registration/selector trace](../docs/evidence/round8-rotor-toggle.md).
A collision mesh's material slots are the `CC_*` names, each
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
`0x50EF920`); otherwise the proxy is not attached by this path. The native
attach-manager constructor explicitly initializes the flag **false**
(`0x50E08C5`), and the stationary-vehicle constructor chain and STN_06
platform do not override it. Thus the default rejects this partial match;
later runtime mutation remains untraced. See the
[constructor evidence](../docs/evidence/round8-stn06-attachments.md).
The proxy is query-only `VehicleQueryProxy`
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

#### T-72 armor (TNK_04)

**Data.** The T-72B3 has no explosive-reactive-armor (ERA) data. Case-sensitive
searches of `data/` for `ERA` (whole word), `Kontakt`, `Relikt` and
`ReactiveArmo` find nothing, and neither does the same search of the GObjects
dump (`GObjects-Dump-WithProperties.txt`: 0 hits for `ERA` as a whole word,
`Kontakt`, `Relikt`, `ReactiveArmor`). The only `Reactive` strings under the
vehicle plugin are a wheeled steering curve (`CRV_SteerSpeed_Reactive`) and a
dune-buggy input asset that names it. The tank has no armor-brick component,
attribute or section: its sections are the six in the TNK_04 rows of the table
above. So any ERA bricks on the model are cosmetic for damage.

**Data.** Collision mesh `assets/models/vehicles/land-tracked-tnk-04-default.glb`
(triangles per collision slot, summed from the glTF index counts):
`CC_MainBody` 3,872, `CC_Tracks_L` 574 and `CC_Tracks_R` 577 (1,151 together),
`CC_Engine` 56, `CC_FuelTank` 20, and `CC_Fabric` 166, `CC_Plastic` 142,
`CC_Glass` 10 (318 together). `CC_Fabric`, `CC_Plastic` and `CC_Glass` have no
entry in the slot-to-section map, so they fall to the default section, the main
health (750). There is no `Body.StrongArea` section: TNK_01 Heavy has
`CC_StrongArea` (378 triangles, 350 health, pre 0.4 to the main health) as a
tougher hull zone; TNK_04 has nothing like it. Armor thickness or angle is not
modelled either way (§3.2: a hit picks a section from its triangle).

**Data.** The tank's protection is the 30-entry row
`Meta.Damage.Vehicle.Land.Tracked.TNK_04.Default` in
`DT_GlobalDamage_VehicleData_TNK_04`, keyed by damage type, not by where the
tank is hit. Selected entries (percent amount, then the factor 1 + amount / 100):

| Source tag | Amount (%) | Factor |
|---|---:|---:|
| `Bullet` | −100 | ×0 |
| `Cannon` | −70 | ×0.3, then the caliber entry |
| `Cannon.35x228mm` / `.20x102mm` / `.30mm` | −84 / −75 / −30 | ×0.16 / ×0.25 / ×0.7 on top of the cannon entry |
| `Kinetic.Impact.Ricochet` | −95 | ×0.05 |
| `Explosive.Drone` | +450 | ×5.5 |
| `Explosive.Rocket.84mm` | +185 | ×2.85 |
| `Explosive.Rocket.155mm` | +80 | ×1.8 |
| `Explosive.Rocket.120mm` / `.125mm` / `.93mm` | +47.5 / +47.5 / +45.5 | ×1.475 / ×1.475 / ×1.455 |
| `Explosive.Rocket.122mm` / `.120x800mm` | −25 / −10 | ×0.75 / ×0.9 |
| `Explosive.Utility.ATMine` / `IED` / `C4` / `Claymore` | +145 / +30 / −25 / −95 | ×2.45 / ×1.3 / ×0.75 / ×0.05 |

The factors multiply (§4.1). The generated tables in §3.1 and §5.3 hold the
results per caliber.

**Data.** Three entries carry a hit-location requirement and only one changes a
result. `Explosive.Grenade.40mm` on `Meta.Damage.HitLocation.Vehicle.Engine` is
−95 % (×0.05, on top of the generic 40 mm entry +20 %). `Bullet` on
`Attribute.Gameplay.Health.FuelTank` is +200 %, but the plain `Bullet` entry
already makes the factor ×0, so it stays 0. `Explosive.Rocket` on
`Meta.Damage.HitLocation.Vehicle` is 0 %. Nothing in the row is keyed to a hull
front, turret or side, so reactive-looking bricks cannot change a hit: the rules
see the damage type and, for these three entries, the section hit.

**Derived.** The difference between the T-72 and TNK_01 is therefore the
damage-type numbers (§5.3), the 750 main health, and the missing `StrongArea`,
not a reactive layer. Not traced: the visual meshes (`SM_TNK_04_*`) were not
inspected for brick geometry; the claim is only that no damage data refers to
any.

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
For movement sweeps, native immediate/deferred dispatch reaches
`0x3A902D0` in both actor directions. The moving actor keeps the other
component in the hit; the struck actor receives swapped `MyItem`/`Item`
and bone names. Native scene-query conversion identifies sweep `Item` as
the struck body/instance index. The ordinary mesh move query leaves
face-return disabled, keeping `FaceIndex` and pre-reversal `MyItem` at −1;
the reversed single-body target therefore lacks a usable section index.
Nonnegative instance indices may select a slot by numerical coincidence,
not triangle material. This is the ordinary traced path; custom queries
that request faces are separate. See the [sweep investigation](../docs/evidence/round8-vehicle-sweep.md).

In the data, ROT_02's wheels are static meshes, so their slots (`CC_Wheel`
on the right wheel, `CC_Tyre` on the left, `CC_Main` on both) resolve to
the main health and the map keys `CC_Wheel_0` / `CC_Wheel_1` never match.
That assumes no static mesh has a slot literally named `CC_Wheel_0`; the
decoded ROT_02 wheel meshes do not, and the other meshes are not checked
(V-9). WHL_* wheel slots `CC_Wheel` (and `CC_Tyre` on WHL_05 to WHL_08)
become `CC_Wheel_n` and `CC_Tyre_n`. The inspected SPW radar proxies register
Default, leaving their part-level `ComplexSurface.Group.Radar` rows unused.
The platform's Default-group `CC_Radar` row still resolves Radar health;
this does not make the radar unhittable. See the
[SPW source settings](../docs/evidence/round8-spw-collision-inputs.md#sockets-placement-and-authored-settings).

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
   actor hit array is sorted by float Distance (`0x6B6FFD0`). The vehicle's
   `IWDDamageable` slot 8 (`0x6C2A790`) then keeps one hit per component by
   removing duplicates with a last-entry swap, so an instanced-wheel
   component contributes one wheel. Swaps can reorder later components and
   select a farther contact for one of them; this is not independent nearest
   selection for every component. See the
   [complete sampling trace](../docs/evidence/round10-native-vehicle-sampling.md).
   **A later gate also
   suppresses repeated nonempty hit-location tags on the same actor**
   (`0x6F06AE6`–`0x6F06B13`): the first encountered tag wins; subsequent
   same-tag contacts skip event creation and application. An empty tag is
   not deduplicated. Component contacts therefore do not each imply a
   separate health application. Every application from
   one explosion on one vehicle takes its section from that first hit,
   while the rule's hit-location tag comes from each hit (`0x6F06540`).
   Each radial amount is the falloff amount of the round's radii, not
   `BaseDamage` ([Damage pipeline §1.1](Wardogs_DamagePipeline_v2.html#11-callers-and-where-the-result-goes)).
   Each application is tagged `Explosive.Radius.Inner` or `.Outer` instead of
   `DamageType.Projectile`, so it meets different rules than the direct
   impact. **Derived:** the Kodiak row's Rocket + `Radius.Inner` entry (+400 %)
   makes an 84 mm blast within 4 m ×6.5 instead of the direct ×1.3: 650
   against 400 main health, one hit. The viewer's `blast_factor` holds both
   factors per slot.
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
  the **source section's** health as a fraction of `MaxHealth`, or its absolute
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

Routing targets are arbitrary registered health-section tags, not only
main health. For example, Gepard's MainBody routes 5% to FuelTank before
its own health loss while MainBody is alive. That transfer does not require
a FuelTank collision hit and does not establish blast penetration. See the
[explosive audit correction](../docs/evidence/round8-explosive-viewer-audit.md#correction-hit-location-deduplication-and-routed-fuel-damage).

**Data**, across the 23 exported damage profiles: 113 section instances,
46 Pre routes, 66 Post routes (all depleted-only), and 22 Simultaneous
routes. Shared source sections are counted again in each profile. No
scalar uses a curve and none uses absolute health. The radial
skip-simultaneous flag is set on 12 section instances (the tracks).

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
| Variant | Damage row (`Meta.Damage.Vehicle.` omitted) | Main health | `556mm` | `762x54mm` | `308Win` | `50Cal` | `20x102mm` | `30mm` |
|---|---|---:|---|---|---|---|---|---|
| `Attack_ROT_02` | `Air.Rotary.Havoc` | 800 | 1143 / 643 (Wheel.Left.Front) | 728 / 410 (Wheel.Left.Front) | 2371 / 1334 (Wheel.Left.Front) | 356 / 200 (Wheel.Left.Front) | 182 | 42 |
| `ROT_03_Default` | `Air.Rotary.LittleBird` | 400 | 191 | 122 | 264 | 60 | 71 | 7 |
| `ROT_03_MachineGuns` | `Air.Rotary.LittleBird` | 400 | 191 | 122 | 264 | 60 | 71 | 7 |
| `ROT_03_RocketPods` | `Air.Rotary.LittleBird` | 400 | 191 | 122 | 264 | 60 | 71 | 7 |
| `ROT_04_Default` | `Air.Rotary.ROT_04` | 600 | 858 / 429 (Rotor.Tail) | 546 / 273 (Rotor.Tail) | 1334 / 667 (Rotor.Tail) | 267 / 134 (Rotor.Tail) | 167 | 24 |
| `ROT_04_MountedMachineGuns` | `Air.Rotary.ROT_04` | 600 | 858 / 429 (Rotor.Tail) | 546 / 273 (Rotor.Tail) | 1334 / 667 (Rotor.Tail) | 267 / 134 (Rotor.Tail) | 167 | 24 |
| `SPW_01` | `Land.Tracked.Leopard.Spawn` | 1000 | — | — | — | — | 366 | 51 |
| `SPW_02` | `Land.Tracked.Leopard.Spawn` | 1000 | — | — | — | — | 366 | 51 |
| `SPW_03` | `Land.Tracked.Leopard.Spawn` | 1000 | — | — | — | — | 366 | 51 |
| `STN_01` | `Stationary.Mistral` | 3000 | 715 | 455 | 445 | 223 | 167 | 60 |
| `STN_02` | `Stationary.Phalanx` | 5000 | 1191 | 758 | 741 | 371 | 278 | 100 |
| `STN_03` | `Stationary.Mortar` | 3000 | 715 | 455 | 445 | 223 | 167 | 60 |
| `STN_04` | `Stationary.RadioTower` | 1000 | 715 | 455 | 445 | 223 | 56 | 12 |
| `STN_05` | `Stationary.STN_05` | 3000 | 715 | 455 | 445 | 223 | 167 | 60 |
| `STN_06` | `Stationary.MGNest` | 1800 | 65 | 41 | 40 | 20 | 30 | 18 |
| `TNK_01_AntiAir` | `Land.Tracked.TNK_01.AntiAir` | 800 | — | — | — | — | 312 | 47 |
| `TNK_01_Artillery` | `Land.Tracked.TNK_01.Artillery` | 650 | — | — | — | — | 254 | 39 |
| `TNK_01_Heavy` | `Land.Tracked.TNK_01.Heavy` | 800 | — | — | — | — | 312 | 47 |
| `TNK_04` | `Land.Tracked.TNK_04.Default` | 750 | — | — | — | — | 176 | 38 |
| `WHL_01_Default` | `Land.Wheeled.Bobcat` | 200 | 96 / 64 (Wheel.Left.Front) | 61 / 40 (Wheel.Left.Front) | 170 / 113 (Wheel.Left.Front) | 30 / 20 (Wheel.Left.Front) | 14 | 2 |
| `WHL_02_Default` | `Land.Wheeled.Patriot.Kodiak` | 400 | 572 / 143 (Wheel.Left.Front) | 364 / 91 (Wheel.Left.Front) | 712 / 178 (Wheel.Left.Front) | 178 / 45 (Wheel.Left.Front) | 39 | 8 |
| `WHL_02_Pickup` | `Land.Wheeled.Patriot.Kodiak` | 400 | 572 / 143 (Wheel.Left.Front) | 364 / 91 (Wheel.Left.Front) | 712 / 178 (Wheel.Left.Front) | 178 / 45 (Wheel.Left.Front) | 39 | 8 |
| `WHL_02_SUV_RingTurret` | `Land.Wheeled.Patriot.Kodiak` | 400 | 572 / 143 (Wheel.Left.Front) | 364 / 91 (Wheel.Left.Front) | 712 / 178 (Wheel.Left.Front) | 178 / 45 (Wheel.Left.Front) | 39 | 8 |
| `WHL_05_Humvee_Default` | `Land.Wheeled.Humvee.Default` | 500 | 715 / 129 (FuelTank) | 455 / 82 (FuelTank) | 889 / 160 (FuelTank) | 223 / 40 (FuelTank) | 56 | 17 |
| `WHL_05_Humvee_RingMinigun` | `Land.Wheeled.Humvee.Minigun` | 500 | 1429 / 258 (FuelTank) | 910 / 164 (FuelTank) | 1778 / 320 (FuelTank) | 445 / 80 (FuelTank) | 70 | 20 |
| `WHL_05_Humvee_RingTurret` | `Land.Wheeled.Humvee.MachineGun` | 500 | 893 / 161 (FuelTank) | 569 / 103 (FuelTank) | 1112 / 200 (FuelTank) | 278 / 50 (FuelTank) | 62 | 23 |
| `WHL_06_DuneBuggy_Default` | `Land.Wheeled.DuneBuggy` | 400 | 286 / 84 (FuelTank) | 182 / 54 (FuelTank) | 324 / 95 (FuelTank) | 89 / 26 (FuelTank) | 27 | 10 |
| `WHL_07_Battle` | `Land.Wheeled.Ural` | 700 | 1000 / 175 (FuelTank) | 637 / 112 (FuelTank) | 1778 / 311 (FuelTank) | 312 / 55 (FuelTank) | 94 | 12 |
| `WHL_07_Default` | `Land.Wheeled.Ural` | 700 | 1000 / 175 (FuelTank) | 637 / 112 (FuelTank) | 1778 / 311 (FuelTank) | 312 / 55 (FuelTank) | 94 | 12 |
| `WHL_07_ArmouredBattle` | `Land.Wheeled.Ural` | 700 | 1000 / 175 (FuelTank) | 637 / 112 (FuelTank) | 1778 / 311 (FuelTank) | 312 / 55 (FuelTank) | 94 | 12 |
| `WHL_08_Default` | `Land.Wheeled.WHL_08.Default` | 500 | 715 / 204 (Wheel.Left.Front) | 455 / 130 (Wheel.Left.Front) | 889 / 254 (Wheel.Left.Front) | 223 / 63 (Wheel.Left.Front) | 53 | 13 |
| `WHL_08_RingTurret` | `Land.Wheeled.WHL_08.Default` | 500 | 715 / 204 (Wheel.Left.Front) | 455 / 130 (Wheel.Left.Front) | 889 / 254 (Wheel.Left.Front) | 223 / 63 (Wheel.Left.Front) | 53 | 13 |
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
| V-7 | **Closed** for physics contacts and ordinary movement sweeps (§3.2): contacts use the hitter's body index; sweeps preserve body/instance indices with face-return disabled and reverse Item/MyItem for the struck actor. Ordinary single-body cases give −1 and no section. Custom face-return queries are distinct. | [Native sweep conversion](../docs/evidence/round8-vehicle-sweep.md) |
| V-8 | **Closed** (§3.2): the shooter's seat picks the branch of `0x6B92900`. `0x6E6EBA0` returns the vehicle whose seat the shooter occupies (`VehicleOperatorComponent.CurrentSeat`, owner a `BHBaseVehiclePawn`). On foot, `0x6F042A0` traces the cone; seated, `0x6F06EB0` hits only that vehicle's occupants, and `0x6B92900` applies the self-damage map straight to the vehicle ([DamagePipeline §1.1](Wardogs_DamagePipeline_v2.md#11-callers-and-where-the-result-goes)) | `0x6E6EBA0`, `0x532DD70`, `0x6F06EB0` |
| V-9 | **Closed for the frozen authored census**: all 276 registered static component/state rows resolve to 217 own/collision meshes. None has a literal numbered slot whose base is `CC_Wheel` or `CC_Tyre`. Runtime mesh/material overrides are outside this asset audit. | `numbered-material-slot-audit-v1.json`; [round 11 audit](../docs/ROUND11_STATUS.md#numbered-material-slots-and-native-collision-damage) |
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
| 2026-10-18 | Radial hits take the `Radius.Inner` / `.Outer` rule factor, not the direct-hit one (§4.1); the viewer defaults explosive calibers to the blast at 0 m. Fixes the Kodiak showing 4 MAAWS hits where the game one-shots it. |
| 2026-10-18 | Round-7 BA-2/BA-3: the deflated hull is the destruction mesh's `BodySetup` with its trimesh; slot name from the hit component's mesh, index from the hull (`0x50BF880`). |


### Shipped collision curves and omitted native defaults

`shipped-collision-curves-native-v1.json` executes the native settings and
data-asset constructors, runtime external/inline curve lookup, rich-curve
evaluator and unweighted interpolation, followed by the full collision
magnitude helper. **23 settings assets / 38 curves cover all 33 variants** by
authored reference reachability. **534 curve samples and 3,312 magnitude checks
pass**, including serialized keys, constant bounds and exact float32 composition.
There is no supplied curve-value callback. This compares native standalone
curve evaluation with native magnitude composition; it is not an independent
cubic oracle or a live-game comparison.

All 23 assets omit the relevant scalar properties. Native constructor defaults
are HighSpeedThreshold 30, bCrushDamageAtHighSpeed true, SpeedCrushFactor
float32(0.8), CrushPenetrationThreshold 20, CrushDamageMultiplier 1000 and
VehicleDamageCooldownTimer 0.5. SDK layout now binds these names to component
fields +0x5F8 through +0x60C. Empty inline curves use the native MAX_FLT default
sentinel and return the caller default. All 38 exported curves are unweighted.
The native rich-curve VFT points to the executed evaluator at slot 17.

A fresh read-only CUE4Parse export from the installed PAKs matches the exact
DamageEntitySettings / FloatCurve properties for all **61 packages**. All
**35** previously frozen skeletal-package identities also match. This binds
the data to the same installed asset set; it does not capture live overrides.
Serialized property overlay, base/unrelated targeting-constructor services,
native gameplay configuration copy/precedence and runtime loading remain
supplied or unverified. Component construction and contact callbacks are not
established by this receipt.

A second label correction applies to the radial fixture: `event_face` and
`typed_hit_faces` were owned opaque IDs stored in **FHitResult.MyItem +0xA4**,
not FaceIndex +0. `full-radial-hit-id-label-correction-v1.json` renames those
fields to `event_my_item` / `typed_hit_my_items`. The original receipt remains
preserved, and reversing all 144 label instances reproduces it exactly.
Filtering, order, hit-copy and numeric results are unchanged. This correction
is derived evidence, not another native execution.

`shipped-curves-checkpoint-validation-v1.json` binds the frozen EXE, native CFG
and constant bytes, producer/fixture identities, SDK/source inputs, fresh PAK
exports and the reversible label correction. `FIRST_TRACK_AUDIT_v3.md` records
the remaining first-track boundaries. Next: native contact admission at
0x76736C0 / 0x767E640, configuration precedence and class/caller attribution.
Track one remains incomplete; tracks two through five remain pending in order.
Calculator code/data are unchanged, so UI/arithmetic checks were not repeated.


### Native contact admission and mesh-hit vector derivation

`contact-admission-native-v2.json` executes the complete native 0x76736C0
helper with the shipped settings and native curve evaluator. **1,242 catalog
cases pass, with 894 forwarding positive amounts**, plus **17 boundary cases**.
Null/garbage targets, non-authority owner roles, missing class/interface,
existing cooldown and selected secondary-set/seat-list conditions suppress
contacts before magnitude evaluation. An admitted positive amount inserts a
cooldown entry and requests a non-looping **0.5-second** timer. The damage caller
receives the other actor as target and the owner as both source and instigator.
The final damage caller is supplied on this receipt; it has separate native
execution evidence and is not yet joined here.

Native class-registration arguments bind 0x53CAB60 to BHBaseVehiclePawn,
0x527B100 to BHMoverPawn and 0x6E65DE0 to WDMoverCharacter. The helper selects
component curve +0x460 for vehicle ancestry, +0x570 for mover-pawn ancestry,
and +0x4E8 otherwise. Only the mover-pawn branch requests crush scaling.
The native +0x758 getter executes and the SDK identifies VehicleSeatComponent;
the related-actor list acquisition remains supplied. V1 fixtures used misleading
`driver` object labels. V2 corrects those labels, executes the seat getter and
retains every prior numeric result; both versions remain preserved.

`mesh-hit-contact-native-v2.json` runs selected complete entry/return paths of
0x767E640 through vector derivation and the actual contact helper: **276 catalog
cases and 266 boundary cases pass**, with **536 contact-helper calls**. It tests
the owner velocity squared, converted to float32, against 100; values at or
below the threshold return before contact handling. WDMoverCharacter targets
also return early. Valid movable primitives that pass the supplied simulation
query contribute their supplied float32 mass. When their float32 mass sum is
at least 1, native code divides the impulse by that sum in double precision;
otherwise it keeps the impulse. The resulting vector drives actual native
curve/magnitude/contact handling.

These mesh-hit paths end naturally at a supplied positive duplicate-cache
gate after contact handling. Later self-damage, effects and propagation branches
remain unexecuted. Owner velocity, virtual physics queries/masses, reflection,
weak-object creation, set storage/lookup/removal, related-actor acquisition,
timer manager/scheduling, allocation and final damage dispatch remain supplied.
No actual world physics, cache lifecycle or server behavior is established.
`contact-admission-checkpoint-validation-v1.json` binds both current receipts,
the seat getter, static class names, native CFG/constants and their input chain.
`FIRST_TRACK_AUDIT_v4.md` keeps the whole first-track objective open. Next work
is later mesh-hit branches, native configuration copy/precedence and remaining
class/caller boundaries. Tracks two through five remain pending in order.
No calculator code/data changed; no UI/arithmetic rerun or push was performed.


### Native gameplay-config copy joined to contact handling

`gameplay-config-copy-native-v2.json` executes complete entry/return paths of
0x767BC40 with an owned vehicle owner at Role 0 and explicit setup services.
**46 shipped-settings cases and eight boundary/override cases pass**, including
**235 native runtime-curve copies** through 0x36269E0. Native code selects the
supplied candidate, writes GameplayConfig +0xF0, and transfers the damage tag,
all five curves and the six collision scalar fields into DamageEntitySettings
+0x3D0. The source data asset is populated by the fixture from verified native
defaults and shipped serialized collision properties. Unrelated source settings
remain at their native defaults.

A missing/garbage container preserves the earlier config pointer; a missing or
incompatible candidate clears it. A garbage candidate is assigned to +0xF0 but
its settings are not copied. Missing/garbage owners return before selection.
Owned non-default scalar values also copy exactly, so this behavior does not
rely on constructor values coincidentally matching in both objects. Both GC
flag states are covered with supplied barriers.

`config-contact-joined-native-v1.json` then runs native contact handling in
the same emulator state after each of **23 native configuration copies**.
All **1,242 contacts / 894 positive forwards** match the separate contact
receipt exactly in amount, curve choice, admission and timer requests. There
are no component damage-settings writes between native BeginPlay and native
contact handling. The fixture changes the supplied owner Role from 0 to 3
before contact handling; this does not establish authority BeginPlay behavior.
A null cached world pointer takes the native fallback lookup, whose result is
supplied, before scheduling a timer.

Contact receipt V3 corrects an aliasing bug in trace recording: later standalone
oracle evaluations could append to an earlier case's `curve_samples` list.
`contact-admission-native-v3.json` snapshots that list and proves exactly one
native curve sample per catalog contact. V1/V2 remain preserved; every amount,
curve selection, admission and timer result is unchanged. V3 is the current
contact receipt. Mesh-hit V2 results do not retain that sample list and are
unaffected. The correction changes fixture trace storage, not native code.

The native settings copy is now executed and joined. Module/asset acquisition,
class compatibility, source property deserialization, delegate/setup services,
optional components/subsystems, unrelated targeting/final continuations,
engine storage/timers and final damage dispatch remain supplied. Actual module
assembly/loading precedence, authority setup, complete BeginPlay effects and
later mesh-hit effects/self-damage/propagation remain unverified.
`config-contact-checkpoint-validation-v1.json` binds these results and verifies
that the V3 correction leaves prior numeric outcomes unchanged.
`FIRST_TRACK_AUDIT_v5.md` and `RESUME_CHECKPOINT_v32.md` preserve the next work.
Track one is still incomplete; tracks two through five remain pending in order.
No calculator changes, UI/arithmetic rerun, live access, commit or push occurred.


### Native settings/contact and mesh-hit joined through health (checkpoint v33)

`config-contact-damage-joined-native-v2.json` joins native BeginPlay collision
settings copy, contact admission, magnitude and curves to the complete native
0x76740F0 damage caller, point event/context construction, rule evaluation,
interface dispatch, baseline section health, cleanup and cooldown scheduling
in **one emulator and allocator**. **1,242 settings/contact cases, 414 cases
across all 23 catalog vehicle rows (22 distinct damage tags), and four suppression cases pass**, producing
**1,308 applications** checked against separate native rule/health runs.
Tracked, wheeled and empty source tags, both GC flag states and all three
contact-class branches are included. Health clipping is checked natively.

`config-mesh-damage-joined-native-v1.json` additionally connects the native
mesh-hit vector derivation to that damage path after native settings copy.
Its **276 catalog and 266 boundary cases pass**, with **479 applications**.
Vector, virtual-query selection, curve, incoming amount and timer results
match the isolated mesh/contact receipt. Component damage settings remain
unchanged between native setup and the mesh-hit callback.

There is no manual event/context/amount bridge on either joined path. Shared
engine-service PE code/global images switch at native caller boundaries;
fixture heap, call arguments and contexts are not copied at those switches.
Unicorn translation-cache flushing is required after these switches: without
it, an earlier translated stub can survive a byte restoration. The successful
fixtures flush the cache. `joined-service-image-code-audit-v1.json` separately
checks **57 protected native spans** against the frozen code across both
images and the return transition.

Source property population, module/class lookup, Role-0 setup followed by
supplied Role-3 contacts, reflection, hit/zone resolution, physics state and
virtual queries/masses, weak objects, set/cache/timer/allocation/typed cleanup,
and baseline no-modifier/lifecycle services remain supplied. The mesh callback
still returns naturally at a supplied positive duplicate-cache gate after the
contact path. Later self-damage/effects/propagation, actual cache semantics,
module loading precedence, authority setup and runtime class/world installation
remain open. The separate native final-damage-caller boundary is now joined;
this does not close those other boundaries.

`config-damage-joined-checkpoint-validation-v1.json`, `FIRST_TRACK_AUDIT_v6.md`
and `RESUME_CHECKPOINT_v33.md` bind the results and next work. Track one remains
incomplete; tracks two through five remain queued in order. No product code
changed, so UI checks were not repeated. No live access, commit or push occurred.


### Native mesh duplicate cache and component selection (checkpoint v34)

`mesh-duplicate-cache-native-v1.json` executes the native 273-byte key hash,
set lookup/insertion, weak-handle equality/validity and the expiry callback's
full hash unlink plus sparse-slot release. **1,024 uint32 hash-model cases,
54 weak-handle cases and 74 cache operations pass**. Owned chunked object slots
exercise index, serial and packed flag checks. Forced hash chains cover
duplicate insertion, deletion and free-slot reuse with four inline buckets or
64 external buckets. The key is an ordered pair of weak handles plus
**FHitResult.Item +0xA8**. This differs from the earlier radial fixture's opaque
IDs stored in MyItem +0xA4.

Sparse removal alone is not full set deletion: it leaves hash-chain links
behind. The actual expiry wrapper at 0x7677E80 enters 0x766C4B0, which unlinks
the hash chain before sparse release. The mesh callback constructs the matching
delegate VFT; slot 11 points to that wrapper. This executes native expiry logic
under owned invocation, not elapsed-time scheduling or timer-manager behavior.
Storage is preallocated for 32 elements; allocation/growth/rehash paths remain
unexecuted and memmove is supplied.

`mesh-native-cache-joined-v1.json` removes the supplied duplicate-gate result
from the shared settings/mesh/contact/damage/health fixture. **276 catalog and
266 boundary cases retain exact damage, health, vector and timer results**,
and **six seeded cache cases pass**, totaling **485 applications**. Native
hash/lookup now runs in the mesh callback. On misses, native 0x76696D0 selects
the damage-model class through its cached native getter; the optional virtual
component lookup is supplied as null and the callback returns naturally.
An exact cache hit skips that later selection. Changed Item, reversed handles
and a deliberately colliding valid handle miss; native expiry makes an exact
key eligible for selection again. Contact damage occurs before this gate, so
those cache choices do not undo the preceding contact damage.

Native registration arguments identify the requested class as
WDVehicleDamageModelComponent, bound by `contact-class-labels-v2.json`.
Its virtual receiver at 0x6B7FCD0 is now captured as 321 bytes despite the
corpus row having failed. Capture alone is not receiver execution or corpus
repair. Non-null receiver behavior, later own-damage/effects/secondary paths,
callback-driven cache insertion and actual timer execution remain next work.
Object/class tables, component discovery, property/setup/physics/reflection,
hit/engine/lifecycle services retain their declared owned boundaries.

`mesh-cache-checkpoint-validation-v1.json`, `FIRST_TRACK_AUDIT_v7.md` and
`RESUME_CHECKPOINT_v34.md` bind these results. Track one remains incomplete;
tracks two through five remain queued in order. No product code changed,
UI checks were not repeated, and no live access, commit or push occurred.


### Native WD collision receiver and constructor attribution (checkpoint v35)

`own-collision-receiver-native-v1.json` executes the recovered 321-byte
0x6B7FCD0 WD receiver, the 1,621-byte base 0x531FC20 receiver and native
0x53205D0 baseline section health. **720 finite cases and five owned boundary
cases pass**, checked against **17 separate native health oracles**. Inputs
cover negative/zero/epsilon/ordinary/clipped amounts, double factors followed
by float32 conversion, owner roles, damageability and stats/inventory branches.
The receiver is invoked directly; it is not yet the non-null component returned
to the mesh callback.

Native base code clamps the incoming float amount at zero, multiplies by the
native double attribute result and converts to float32 before its epsilon
check. Its Role-3, bCanBeDamaged and supplied enable predicate gates control
entry to section health. The WD wrapper optionally changes the temporary
`+0x2B8` cause through supplied stats/interface discovery and an inventory-cause
result, then restores the prior cause in every case. Positive handled damage
and vehicle ancestry control its notification call. A supplied garbage owner
with an accepting base enable predicate can still reach that notification;
the wrapper's cause-override garbage check is not a general notification gate.
This describes owned branch inputs, not actual object-lifetime behavior.

The native 187-byte WD object constructor also executes with its base constructor
and final lifecycle helper supplied. Guard canaries are preserved. It installs
primary VFT `0xB30DFF8`; the actual native pointer at `+0x500` (`0xB30E4F8`)
points to `0x6B7FCD0`. This strengthens receiver/table attribution beyond corpus
aliases. The class initializer at `0x6B80930` is distinct from the object
constructor at `0x6B7FB50`.

Surface resolution is supplied as a fallback to the main health section;
class/stats/inventory lookup, enable predicate, optional operator discovery,
attribute/requirement services, notifications and lifecycle remain supplied.
Owner non-null is an input precondition. Actual runtime class installation,
all surface-routing branches, non-null mesh integration and later mesh effects
remain unverified. No corpus row was rewritten: a failed decompiler row has
usable captured/executed native code, which is a different result.

`own-receiver-checkpoint-validation-v1.json`, `FIRST_TRACK_AUDIT_v8.md` and
`RESUME_CHECKPOINT_v35.md` bind this checkpoint. Next: return an owned non-null
model component to the mesh callback, execute the own-vehicle and rotation
curve paths into this receiver, then later effects/cache/timer boundaries.
Track one remains incomplete; tracks two through five remain queued. No product
code changed, UI checks were not repeated, and no live access or push occurred.


### Non-null mesh collision receiver joined (checkpoint v36)

`nonnull-mesh-receiver-native-v1.json` joins native settings copy, the mesh
callback, target contact/point/rules/health, and the separate owner's collision
curve/receiver/health path in one emulator. **621 catalog cases and four
boundary cases pass** across 23 settings assets, three contact classes, three
owner velocities and three impact normals. They include **622 owner receiver
calls, 177 positive owner-health changes and 495 target applications**, checked
against 37 separate native owner-health results. Target health/events remain
identical to the previously validated contact path while owner results vary
with the impact-normal projection.

Native code projects the owner velocity onto Hit.ImpactNormal, takes the
projected vector norm, multiplies by 0.036 and converts to float32 for
VehicleCollisionCurve at component +0x3D8. The selected ray-miss/no-secondary
branch supplies native multipliers of one; float32 composition agrees exactly
with the amount received by 0x6B7FCD0. Its base receiver and section health run
natively, with a separate owner model and health state. No gameplay event,
context or amount is rebuilt between these paths.

The callback now reaches native duplicate insertion and constructs its actual
64-byte expiry closure. Native 0x158B640 also builds populated three/four-unit
(48/64-byte) delegate descriptors; the low-level allocator and timer service
remain supplied. The service records and consumes the descriptor, not elapsed
time. Earlier fixture versions supplied allocation storage without populating
that descriptor; their timer calls established request arguments, not complete
delegate assembly. The current replay includes the populated descriptor.

A native repeat/expiry sequence uses the **actual constructed closure**, with
its full native VFT mapped. An exact repeated key skips owner damage after the
already-tested target contact. Invoking the closure through VFT +0x58 runs
native hash unlink/expiry; a following callback applies owner damage again.
The contact cooldown lookup is deliberately reset by the owned fixture between
calls, so this does not establish cumulative real-time cooldown behavior.
Health baselines are also reset between independent observations.

`nonnull-service-image-audit-v2.json` checks 22 protected native spans/data
across upstream, owner-receiver and return service images. Version 1 of that
image audit and its fixture remain preserved; V2 maps the whole expiry VFT
needed for the real indirect closure call. PE service-image switching flushes
Unicorn's translation cache and leaves gameplay heap/context state intact.

This path supplies a ray miss, nonmatching secondary class, base-vehicle
callback/filter results, physics/virtual state, source property/setup and
reflection/component discovery, attributes/notifications/lifecycle, allocation
and timer-manager services. Ray-hit/rotation, matching secondary propagation,
base effects, allocator growth, actual timing/world/authority and runtime class
installation remain open. `nonnull-mesh-checkpoint-validation-v1.json`,
`FIRST_TRACK_AUDIT_v9.md` and `RESUME_CHECKPOINT_v36.md` bind the checkpoint.
Track one remains incomplete; tracks two through five stay queued. No product
code changed, UI checks were not repeated, and no live access or push occurred.


### Native ray-hit rotation multiplier joined (checkpoint v37)

`mesh-rotation-native-v1.json` executes the selected ray-hit branch through
native root up-vector calculation, between-vector quaternion, quaternion-to-
rotator conversion, axis normalization and the actual rotation curve, followed
by the already-native owner receiver/health/cache/timer-descriptor path.
**621 catalog cases and two ray/root boundaries pass**: 23 settings assets and
27 orientations, including pitch/roll tilts, quarter turns, opposite up vectors,
rotated roots, a diagonal normal and mixed gimbal lock. There are **299 positive
owner-health changes and 434 target applications**, with **61 separate native
owner-health results**. Target health/events stay unchanged across orientations.

The caller normalizes each angle to its signed axis range and evaluates
RotationDamageMultiplier at component +0x648 using **abs(Pitch) + abs(Roll)**,
converted to float32. Yaw is excluded. The default curve value is one, including
empty inline curves. Native up vectors and quaternion mapping agree with a
unit-quaternion model; native Euler output agrees with an independent branch
model, including the singularity cases. Curve input and final float32 amount
composition agree exactly. For an identity owner and a ground normal tilted
30 degrees, the shipped example multiplier is approximately 1.35.

Ray result/normal and owner transform are owned inputs. Native helpers execute
around three supplied numeric library boundaries: atan2, fmod and asin use
Python math callbacks. Their PE import thunks are verified against the frozen
CRT import directory. This does not prove those library implementations or an
actual world trace. `rotation-service-image-audit-v1.json` checks 16 protected
native spans across upstream/owner/return service images.

`demolition-multiplier-static-labels-v1.json` identifies the next branch from
native registration arguments: BHDemolitionCellRepresentation,
InstancedStaticMeshComponent and BHDemolitionDataFragment_VehicleDamage.
The captured caller selects a matching fragment and uses its first float as
the XMM9 collision multiplier. The earlier generic description as a secondary
propagation branch was too broad; this is a demolition data-fragment multiplier
path. Its matching branch/query and authored data remain unexecuted/unbound.

Actual trace traversal, demolition-fragment/query behavior, base-vehicle
filter/effects, allocation growth, timer scheduling, module loading, authority,
class installation and runtime world/lifecycle state remain open.
`rotation-mesh-checkpoint-validation-v1.json`, `FIRST_TRACK_AUDIT_v10.md` and
`RESUME_CHECKPOINT_v37.md` bind the checkpoint. Track one remains incomplete;
tracks two through five remain queued. No product code changed, UI checks were
not repeated, and no live access, commit or push occurred.


### Checkpoint v38: native demolition lookup and typed fragment multiplier

The selected native 52FD760 read-only query now executes with its membership,
component-to-ID and ID-to-asset map lookups. The native 767E640 caller selects
the first matching VehicleDamage fragment (including derived types), composes
the multiplier and reaches native owner health in the same emulator.

Fresh PAK headers recover the dynamic FInstancedStruct types that ordinary
JSON exports omit: 39 VehicleImpulse fragments and four VehicleDamage fragments
across the 39 currently exported demolition assets. The mapping identifies
these as sibling types. RestitutionImpulseMultiplier is not a damage multiplier.
The four DamageMultiplier values are zero; 35 assets have no matching fragment.
For these lists, successful query/predicate selection yields multiplier zero;
query rejection falls back to one. These are conditional outcomes: every asset
references a ruleset and the ruleset predicate is still a supplied callback.

mesh-demolition-native-v1.json covers 23 settings x39 assets x2 predicate
outcomes (1,794 cases), plus25 owned guard/type/order/scalar cases. Separate
native owner-health results verify final amounts; target health/events remain
unchanged across asset/predicate choices. demolition-service-image-audit-v1.json
checks30 protected native spans across upstream/owner/return images.

World, class installation, representation maps, source loading, physics,
allocation/timing and engine services remain supplied. The read-only query
skips demolition mutation. Actual ruleset eligibility is next: authoring
reference closure finds19 packages, not yet freshly compared or executed.
Native base effects/filtering, growth/rehash, other caller integration and
runtime world/lifecycle boundaries also remain open. Track one is incomplete;
tracks two through five remain queued. No product code changed, UI checks were
not repeated, and no live access, commit or push occurred.

demolition-mesh-checkpoint-validation-v1.json binds this evidence closure;
FIRST_TRACK_AUDIT_v11.md and RESUME_CHECKPOINT_v38.md preserve the next work.


### Checkpoint v39: native vehicle-context demolition rules

Fresh installed PAK exports match all66 objects in19 referenced rule packages
by export index, name, type and properties. Native Or/Ruleset/Vehicle predicates,
class casts, cached class getters, actor variant getter and tag-container match
now execute in a separate owned vehicle-context fixture. Native explosion and
buildable predicates execute their missing-context rejection paths.

`demolition-rules-native-v1.json` passes2,574 catalog cases:39 demolition assets
x33 authored variant tags x2 supplied contact flags.1,254 permit and1,320 reject;
11 additional actor/class/variant/tag/cycle guard cases pass. The native match
checks the input tag against permitted explicit and parent entries. Parent
container construction and tag identities remain supplied. Do not infer a
standard tag direction from the names alone. Both authored contact bits are
true; individual-bit meaning is not established by this catalog replay.

The prior mesh demolition lookup/multiplier receipt still uses a supplied
predicate outcome. Joining actual rules into that same emulator is next.
Positive explosion/buildable context paths, class/variant installation,
property loading, actual world participation, growth and lifecycle remain
separate boundaries. No complete-track or live-parity claim is made.
`demolition-rules-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v12.md and
RESUME_CHECKPOINT_v39.md bind this increment. Track1 remains incomplete;2-5
remain queued in order. No product code, live access, commit or push.


### Checkpoint v40: native rules-to-damage join and positive metadata graphs

`rules-mesh-native-v2.json` joins actual authored native rules to the52FD760
query,767E640 typed fragment multiplier and native owner health in one emulator.
It passes3,003 catalog cases:39assets x33variant tags at one configuration, plus
22other configurations x39assets xone permitting/one rejecting variant. This is
not the full23x39x33matrix.1,485permit,1,518reject;1,050cases change owner health.
Seven independent native owner-health results check final amounts. Native
configuration copies and target health/events match the frozen conditional
baseline; the supplied predicate callback never executes.

V2 also passes184regressions across23configurations, four contact categories
(other/vehicle/pawn/special) and permitting/rejecting variants. The first joined
fixture installed a second owned vehicle-class identity and misclassified
vehicle contacts outside its selected-other catalog. V2 reuses the original
contact class. `rules-class-identity-correction-v1.json` retains eight direct
comparisons, including the two affected vehicle outcomes, and proves the fix.
Configuration setup retains its supplied class/config services; native code
is restored before mesh handling. The current image audit verifies50protected
spans after setup and across owner/return images.

`demolition-metadata-native-v1.json` proves270authored/boundary and44owned
positive/negative typed metadata cases. Native explosion code evaluates the
shipped ANY tag-query bytecode and accepts matching finite Distance<=the
configured threshold. Native buildable code checks explicit/parent blocklists
and inverts the match. Four native constructor cases additionally prove the
omitted buildable blocklist defaults to empty, initialize the explosion query
and bind both VFT+2B0 predicate slots. UObject/base initialization is supplied.
`demolition-metadata-graph-native-v1.json` then passes7,761cases over all39asset
rule graphs, including source tags/children, thresholds/nextfloatabove and
buildable metadata.3,081permit. These graphs are separate from an explosion
caller/world/damage join. The metadata code audit verifies36protected spans.

Correction to earlier boolean labels:SDK EBHDemolitionType is Blocking=0 and
Overlap=1; context byte+8 is the enum, not a blocking-hit boolean. Native200case
truth table verifies bit0 permitsOverlap andbit1 permitsBlocking. Existing
`blocking`/`blocking_hit` boolean fields storebool(rawtype), so true meansOverlap.
The mesh query supplies raw1Overlap. `demolition-type-label-correction-v1.json`
binds59,706legacy field occurrences across four frozen receipts without changing
numeric results. Both authored permit bits were true, so catalog outcomes stand.

Native graph/query/health execution uses supplied object/class/variant/map and
property population, tag identities/parent-container construction, world,
physics, CRT, allocator, registry/locks/reference lifetime and timer services.
The read-only query skips actual demolition mutation; graph growth is untested.
Base53C7AC0callback/effects and532D4C0filter remain supplied; their full selected
CFGs are now captured but unexecuted. Actual explosion caller/world integration,
loading/authority/class/runtime lifecycle, allocation growth and scheduling also
remain open. Track1 remains incomplete;2-5 remain queued. No live access, product
code change, commit or push.

`rules-mesh-metadata-checkpoint-validation-v2.json`, FIRST_TRACK_AUDIT_v13.md and
RESUME_CHECKPOINT_v40.md preserve this checkpoint and its next steps.


### Checkpoint v41: native collision physics lookup/gate and base callback

The former532D4C0filter shortcut is now a native hit-to-physics-group and
VehicleDamagePhysicsData lookup. Native50F41D0 checks component membership,
resolves body-setup weak pointers, selects one of nine geometry arrays, applies
optional shape-name overrides and chooses a group by body-result index. Native
532D4C0/48A9940 select exact or nearest-parent physics data, including the
bExecuteCollisionEffects byte. Native FName hashing and parent-manager wrapper
execute; object/map/geometry installation, registry lookup, locks and reference
lifetime remain supplied.

Fresh PAK exports match15explicit MVF_HealthSections objects and all40authored
PhysicsGroupMappings rows. One disables collision effects and39enable them.
These are explicit exports; inherited/omitted fragments and active module
applicability are not established. `collision-physics-native-v1.json` passes
220authored queries plus37weak-reference/index/geometry/override/parent cases.
The populated fields cover flag/modifier selection, not damage routing.

`filter-rules-mesh-native-v1.json` embeds that native lookup into767E640 without
a gameplay answer bridge.3,680cases cover23settings x40rows xexact/child query
xpermitting/rejecting demolition variants; four missing-map/nomatch cases also
pass. The false flag suppresses the callback in92catalog cases; the remaining
3,588reach it. Missing physics data also reaches it. Prior target/owner health
and events match. The base53C7AC0body remains a suppliednoop in this joined
receipt; the owner-receiver phase retains its previous supplied group fallback.
The service-image audit verifies70native spans after setup/upstream/owner/return.

Separately, `base-collision-callback-native-v1.json` executes the full selected
53C7AC0body, native impulse normalization/up-vector math, vehicle-class alias,
4C46730cue wrapper and the cached4C47EB0provider/TLS path.1,068finite arithmetic
cases and30guards/handoffs pass, producing735owned manager-receiver dispatches.
The pawn branch compares impulse squared length strictly above a supplied
character threshold and records impulse length as RawMagnitude. The general
branch uses float32(abs(relative velocity dot Hit.Normal)) strictly above a
supplied threshold. Native orientation gating and recursive two-vehicle handoff
are covered. Location, Normal, instigator/causer handles and physical material
are checked at the FWDGameplayCueParameters receiver boundary. Engine physics,
weak-key creation, class/config inputs and the already initialized provider/
manager receiver are supplied; actual cue rendering/replication is untested.
Authored base-config threshold/default acquisition remains open.

The separate filter/callback code audit checks124native spans; together with
the joined audit this is194checks. Side-selector clarification:
`collision-physics-side-labels-v1.json` binds the legacyown_side field to the
raw fifth50F41D0argument: false selects MyBoneName+F8/MyItem+A4, true selects
BoneName+F0/Item+A8.532D4C0usesfalse. Hit.ElementIndex+AC, notFaceIndex, selects
the geometry element. Earlier frozen numeric receipts are unchanged.

Next is replacing the mesh's supplied53C7AC0callback with the verified native
body. That integration must enlarge the owned actor allocation safely, preserve
component/stats/owner pointers and reconcile class identities and service
images. Physics routing under the owner receiver, actual base-config loading,
explosion caller/world integration, growth/scheduling and runtime class/world/
lifecycle inputs remain open. Track1is incomplete;2-5 remain queued. No live
access, product-code change, commit or push.

`filter-base-callback-checkpoint-validation-v2.json`, FIRST_TRACK_AUDIT_v14.md
and RESUME_CHECKPOINT_v41.md preserve the evidence and continuation.


### Checkpoint v42: native base callback joined through cue parameters

`full-callback-mesh-native-v1.json` removes the supplied53C7AC0callback from the
selected767E640path. Native complex-hit/physics-data lookup, base callback,
cue wrapper/cached provider path, demolition rules/fragment factor and owner/
target health now execute in the same emulator.3,680catalog cases and736contact
category/simulation/flag/demolition regressions pass. The catalog produces3,588
owned cue-manager dispatches; the category regressions produce276. Six separate
native callback results check the typed cue fields. Health, events and selected
source/context fields match the previous conditional-callback baseline.

Both owned actor objects were copied into guarded0xAD0allocations, with owner,
component, stats, controller and cache references updated. Guards hold in every
case. The joined class-marker views now use one pawn identity across contact,
query, point-event and callback services. The old contact/point/query pawn
indices were2/1/3; current pawn/vehicle/special markers are0/1/2. Callback and
contact classify vehicles as pawns consistently. This proves the supplied
marker profile, not actual runtime UClass installation or inheritance state.
The post-setup service-image audit verifies80protected native spans.

The callback receives the native mass-adjusted collision vector, not the
original mesh-hit impulse. With owned impulse(1000,2000,3000) and masses10/20,
the observed callback argument is(33.333333333333336,66.66666666666667,100).
The frozen input field remains namedimpulse. Cue position/normal, magnitude,
instigator/causer and physical-material copy are checked independently; padding
bytes are not treated as semantic fields.

`callback-config-defaults-native-v1.json` executes the native base constructor
and four derived config constructors, including null initializer guards. Nine
cases prove the common callback threshold+128defaults30, character threshold
+12Cdefaults10 and default cue tagNone. Native registration name/size/constructor
arguments bind all five classes. Base UObject and derived lifetime/delegate
services remain supplied. Fresh PAK exports match25complete config Properties
objects covering references to all23settings rows.19explicitly provide collision
cue tags; six retainNone. Two rotary configs override the separate public
CollisionEffectImpactThreshold+124to10; neither overrides callback+128.

`authored-callback-mesh-native-v1.json` replays these effective candidate fields
in300same-emulator cases: general20/30/31boundaries, pawn squared-vector9/16
boundaries, recursive vehicle handoff and two demolition outcomes. All pass,
with152cue dispatches and preserved health results. This is a reference-linked
candidate replay: active variant/config selection, native property loading,
runtime actor cue overrides and actual rendering/replication remain unproven.

Next is native physics-group routing in the owner collision receiver. Its
53C9A90/53CA690mesh discovery and50F41D0group fallback are still supplied, and
its populated routing-map branch has not been joined. Config/module loading
precedence, explosion caller/world integration, growth/scheduling and actual
runtime world/class/lifecycle state also remain open. Track1remains incomplete;
2-5remain queued in order. No live access, product-code change, commit or push.

`full-callback-config-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v15.md
and RESUME_CHECKPOINT_v42.md preserve this checkpoint.


### Checkpoint v43: native owner physics section routing joined

The full mesh callback now reaches native owner physics-group selection,
collision modifier, sequential and simultaneous health routing. The new
`full-routed-mesh-native-v1.json` passes 3,680 cases: 23 gameplay settings,
40 explicit physics rows, exact and child tags, and two demolition outcomes.
Target health, events, selected source/context fields and 3,588 cue dispatches
match the frozen callback baseline. Owner health and handled return match an
independent native receiver replay using the amount produced by mesh code.
The gameplay path shares one emulator; the replay is verification only.

`physics-routing-receiver-native-v1.json` passes 1,120 catalog cases and
26 owned guard/variant cases against a stateful native section-health oracle.
The source has 32 rows with one sequential route, six with one sequential and
two simultaneous routes, and two with two sequential routes. Sequential routes
multiply the remaining amount and accumulate handled damage. Simultaneous
routes multiply the original scaled amount and do not add their handled result
to the function return. Both can change health. Routing entries have a 20-byte
stride. Sparse inline/external allocation bits and holes are exercised.
Four health sections are declared owned inputs: main, fuel tank and both front
wheels. This does not establish installed runtime attribute sets or map order.

Correction to v42: 53C9A90 and 53CA690 resolve seat occupants/fallback pawns;
they are not mesh discovery. Missing occupants do not skip physics lookup.
Native 531FC20 still reaches 50F41D0 using MyBone/MyItem hit fields, resolves
the nearest parent physics row and applies native 53984A0 before routing.
The authored row with collision effects disabled still applies collision
damage; its coefficient is 18.5, so an admitted 100-unit input damages main
health by 1,850. The effect flag controls the cue callback, not damage admission.

`full-routed-driver-native-v1.json` passes 280 joined cases: 40 physics rows
and seven owned seat/pawn/controller states. The same pawn marker is used by
contact, callback, query and driver cast. Valid drivers supply causer/controller;
absent or non-pawn occupants supply neither. A garbage pawn pointer can remain
in the causer field while controller is zero. This records native output,
without asserting that such a pointer is valid. Positive historical-seat/world
fallback remains untested. Code bytes are checked in upstream, owner, restored
upstream and post-catalog phases; successful producers and fixtures are frozen.

Remaining track 1 work includes config/module selection and loading precedence,
inherited/omitted fragment application, explosion caller/world integration,
cache growth/rehash and timer scheduling, and actual world/class/lifecycle/
animation/history inputs. Engine attribute, registry, requirement and lifetime
services remain supplied. Track 1 is incomplete; tracks 2-5 remain queued in
order. No live access, product behavior change, commit or push.

`full-routed-mesh-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v16.md,
RESUME_CHECKPOINT_v43.md and checkpoint-integrity-v43.json preserve this result.


### Checkpoint v44: native config override/fallback selection

`vehicle-config-selection-native-v1.json` verifies native 53CBBC0 application
at UMVF_VehicleConfig VFT slot 89, with native typed-metadata helper 53B6190
and config/pawn class getters. Frozen VFT bytes bind that slot and metadata
slot 88 (53CE640). The helper's registration-name argument binds the label
MVFCustomData_VehicleConfig, matching the SDK OverrideVehicleConfig field;
the module's fallback VehicleConfig soft reference is at +40.

2,400 cases cover override and fallback resolution states, metadata presence
and exact/derived/unrelated types, target class/presence, GC mode and declared
cold/warm metadata registration. Sixteen further cases change the override
between its two resolution calls. Native selection prefers a typed override;
an absent, unresolved or unrelated override uses the module fallback. A typed
override whose object is marked garbage is selected first, then fails the
final validity guard without trying the fallback. A changed second resolution
also fails without falling back when null, unrelated or garbage. Only a valid
selected config and valid target class cause pawn+A78 installation and the
VFT+8E0 notification dispatch. Failure preserves the previous config pointer.

This proves native control flow for supplied soft-reference results, class
marker profiles and target context. The engine resolver, metadata registration,
target-context service and notification body remain supplied. It does not prove
PAK asset loading, module ordering, inherited fragment application or complete
config acquisition through the full mesh. Track 1 remains incomplete; tracks
2-5 remain queued in order. No live access, product-code change, commit or push.

Next native leads are metadata selection 53CE640 and the actual pawn config
notification 53C0080 (ABHBaseVehiclePawn VFT slot 284 / +8E0), followed by
linking selected config fields to the existing callback/routing path. Remaining
explosion caller/world, cache/timer and runtime input gaps stay separate.

`vehicle-config-selection-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v17.md,
RESUME_CHECKPOINT_v44.md and checkpoint-integrity-v44.json preserve this result.


### Checkpoint v45: native config metadata and base notification

`vehicle-config-metadata-native-v1.json` passes 600 metadata/path guard cases
and 75 source-linked request cases for 25 explicit MVF_VehicleConfig exports.
Native 53CE640 chooses a typed override with a non-empty package field or the
module fallback. Native 17A4E20 deep-copies the soft path, including UTF-8
subpaths, and 1603EE0 destroys temporary path strings. The request pair is
moved into the output, the temporary pair is zeroed and the valid flag is set.
That flag records a request handle, not proof that the asset exists or loaded.
48AC720 remains a recording asset-request engine boundary. Fresh PAK decoding
in `config-module-pak-v1/manifest.json` subsequently matches all 25 complete
module Properties objects at their names/types/export indices. No VehicleConfig
field was omitted in this explicit module set. Active module order and inherited
fragment application remain unproven.

`vehicle-config-notification-native-v1.json` replaces the selection fixture's
notification shortcut with actual base-pawn 53C0080. Native camera guards and
53A4630 install camera assets; 26CCE10 copies five arrays of 8-byte input names.
Native role-3 history arithmetic clamps rate/scale, allocates 44-byte entries,
moves the buffer and releases the old one. 324 camera/input/event-guard cases,
192 history cases and 400 selection/notification cases pass. Frozen base-pawn
VFT bytes bind slot 284/+8E0 to 53C0080 and slot 311/+9B8 to the native default
return. Engine camera transform/activation, allocation/copy/free, scale, lifecycle
and registration services are supplied. Positive event maps and new network
physics settings creation have not been exercised.

Correction to the v44 corpus lead: actor +788 is VehicleEventComponent, not
the operator component; config +60 is EventMappings. Actor +768/+770 are third-
and first-person spring arms. SDK offsets and native field accesses bind these
labels. The current notification fixture intentionally exercises missing or
garbage event components. It does not replace the event mapping body with a
successful result.

Derived notification overrides are distinct: airplane 53BFEE0, rotary 53C0540,
tracked 53C06E0 and wheeled/WD-wheeled 53C0B50. Their direct CFGs are captured
but not executed by this base-pawn suite. These overrides, positive event/
network branches and linking native selected config into the full mesh remain
next. Explosion caller/world integration, cache/timer behavior and genuine
runtime input gaps remain open. Track 1 is incomplete; tracks 2-5 remain queued
in order. No live access, product-code change, commit or push.

`config-metadata-notification-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v18.md,
RESUME_CHECKPOINT_v45.md and checkpoint-integrity-v45.json preserve this result.


### Checkpoint v46: native wheeled config notification and axle construction

`wheeled-config-notification-native-v1.json` joins native config selection and
installation to actual wheeled 53C0B50, the base notification and seven native
wheeled setter helpers. Frozen VFT entries bind both MWheeledVehiclePawn and
WDWheeledVehiclePawn slot 284 to this body. 486 component/asset guards, 216
rate/axle/wheel cases and 256 selection cases pass their expected outcomes.
The guard suite includes 54 explicitly expected native read faults, rather
than 486 successful applications: the input setter 536F090 does not guard a
null input asset. Garbage-marked input assets are also copied. Other individual
asset setters have their own guards. A fault can occur after earlier settings
have already changed; no rollback is asserted.

Native characteristics update rate clamps to 50..1000, with timestep 1/rate;
mass, engine/transmission fields and three gear ratios are installed. Native
axle construction uses 112-byte records and deep-copies 64-byte wheel
configuration records, preserving owned names, physics tags and indices.
Non-empty axle/wheel arrays, native temporary destructors and selected pointer
storage execute. Wheel tag containers and runtime wheel-state arrays are empty
in these owned profiles. Allocation/copy/free, weak-handle registration and
component/profile virtual activation remain supplied engine services.

The derived actor component lives at +AD0, so the old base fixture allocation
cannot contain it. The new fixture uses a separately guarded C00-byte actor
and a guarded 2000-byte physics allocation; both retain their end guards.
These capacities are fixture allocations, not claims about actual UClass size.
No actual asset loading, physics world registration or config-to-mesh join is
claimed. Air/rotary/tracked overrides, positive event/network branches, full
config acquisition, explosion caller/world and cache/timer gaps remain open.
Track 1 is incomplete; tracks 2-5 remain queued in order. No live access,
product-code change, commit or push.

`wheeled-notification-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v19.md,
RESUME_CHECKPOINT_v46.md and checkpoint-integrity-v46.json preserve this result.


### Checkpoint v47: native wheeled config-to-collision join

`configured-routed-mesh-native-v1.json` connects the native wheeled/base config
constructors, module selection, wheeled/base notification and axle construction,
gameplay settings copy, and full collision/cue/health path in one emulator.
Nine source-linked wheeled configs pass 2,880 catalog cases (40 physics rows,
exact/child tags, two demolition outcomes and override/fallback selection).
Their target/owner damage results match the frozen routed-mesh baseline.
2,808 catalog cue dispatches match independent native callback replays using
the selected config's actual cue tag and native 30/10 threshold defaults.
216 further cases verify equality/above-threshold, pawn-vector and recursive
vehicle behavior against the prior authored-config suite.

The settings-copy path now executes native 53CB340 to read the selected actor
+A78 pointer, native 188F5C0 to check the selected config's GameplayConfigDataAsset
reference, and native 767BC40/36269E0 to install settings. The old supplied
container/getter shortcuts are absent in this phase. The actor's config pointer,
its callback fields, its gameplay reference and copied component settings remain
unchanged through collision. The callback does not reinstall a substitute config
or rewrite its thresholds/tags. Native-copy preservation already present in the
mesh fixture remains enabled. The actor uses guarded C00 storage and an A00
owned VFT; previous owner/component/cue/controller/stats/cache references are
updated explicitly.

36 rejected-reference cases exercise null or unrelated gameplay assets through
both selection routes. Native setup clears component +F0 and does not copy
settings. Actor +A78 still holds the selected vehicle config. The harness does
not invoke collision for these cases; its ready_for_collision flag is an
orchestration decision, not a newly discovered native collision guard.

Source cue fields and the GameplayConfig reference are supplied property
overlays after native construction. UObject/delegate initialization, class
markers, soft resolution, physical world, movement/input profiles and engine
lifecycle services remain owned inputs. The movement profile used for setter/
axle activation is synthetic, distinct from each config's authored subassets;
primitive mass/pose queries are still supplied. This proves a native control-
and-data join, not actual UObject loading, active variant/module ordering or
physical installation in a game world. Air/rotary/tracked notifications,
positive event/network branches, explosion caller/world integration and cache/
timer gaps remain open. Track 1 is incomplete; tracks 2-5 remain queued in order.
No live access, product-code change, commit or push.

`configured-routed-mesh-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v20.md,
RESUME_CHECKPOINT_v47.md and checkpoint-integrity-v47.json preserve this result.


### Native throwable-contact impact caller checkpoint v48

The frozen build's native `6CA8730` throwable-contact caller now executes through
point-event assembly, source rules and target health in an owned fixture.
1,840 cases span 23 canonical targets, four declared source profiles, five damage
amounts, driver presence and GC variants. 1,380 nonempty-root cases match an
independent native collision point-caller replay with equivalent enriched source.
The 460 empty-root cases have no paired oracle: the throwable caller preserves
`None`, while the older collision caller substitutes `Landscape`.

Native source/controller getters execute. The caller uniquely adds Throwable
and Impact contexts and replaces source cause with actor EntityId. Hit location
remains `None`. 18 guards, 83 timing cases and two repeat sequences pass; 85 code
image checks preserve 17 captured functions. Positive handled damage sets the
repeat latch. A latched positive cooldown compares float32(double world time
minus stored float) with the cooldown; equality admits. This function leaves the
stored timestamp unchanged. External scheduling effects remain unproven.

World/mode/target/interface lookup and engine tag/lifetime services are supplied;
mode codes remain raw values. This is throwable contact impact, distinct from
radial detonation. Radial gather `6F01E50` and upstream `6EFFDC0` are CFG-captured
but unexecuted. Actual world/multi-actor/lifecycle integration, asset installation,
derived notification/event/network branches, cache growth and timers remain open.
Track 1 is incomplete; tracks 2-5 remain queued in order. No commit or push.

Private restart: `RESUME_CHECKPOINT_v48.md`, `FIRST_TRACK_AUDIT_v21.md`,
`explosive-impact-checkpoint-validation-v1.json`, `checkpoint-integrity-v48.json`
under `round11_collision_parity_20261020`.


### Native radial gather builder checkpoint v49

Native `6F01E50` now iterates supplied sparse world results and constructs actor/
radial-event records through native constructors and deep hit-array copies.
20 critical scenes (63 contacts) and 24 owned guard/filter cases preserve the
prior full-radial damage and health results. 102 standalone gather cases verify
multi-actor construction across 0–137 slots, inline/heap bitmaps, holes and
occupied null/garbage actors. Joined health cases still contain one valid actor.

Native event construction copies base damage into both leading damage fields;
the outer caller still computes per-contact falloff from the original inputs.
This replaces the prior shortcut's assumptions about constructed event fields.
3,818 native image checks pass. Upstream `6EFFDC0` additionally executes through
the radial caller for 16 empty-query/invalid-world cases with 16 image checks.
The engine query boundary observes shape 2/radius 2000; query results are supplied
empty. Nonempty native grouping, component geometry/LOS, actual world identity,
multi-actor health and lifecycle remain open. Engine setup and lifetime services
remain owned; empty-query options setup is a no-op, not a native-copy proof.

Track 1 remains incomplete; tracks 2–5 remain queued in order. Private restart:
`RESUME_CHECKPOINT_v49.md`, `FIRST_TRACK_AUDIT_v22.md`,
`native-radial-gather-checkpoint-validation-v1.json`, `checkpoint-integrity-v49.json`
under `round11_collision_parity_20261020`. No commit or push.


### Native nonempty overlap grouping checkpoint v50

A bounded native `6EFFDC0` window now processes supplied nonempty engine overlaps
into actor/component groups. 64 cases verify first-seen order, repeated item
append, invalid actor/component/interface handling, bone selection and native
transform copying, including growth to 20 actors, nine components, 11 items and
nine transforms. 1,792 native image checks pass; input overlap records stay intact.

Execution stops explicitly at `6F0088C`, before LOS, final contact/map construction,
cleanup, return or damage. Engine query/weak/class/config/bone/pose data and
allocation/rehash services remain supplied. The actual vehicle virtual disables
the special distance path, leaving its distance field at FLTMAX. This proves
native grouping/copy behavior, not actual geometry/LOS or complete world parity.

Track 1 remains incomplete; tracks 2–5 stay queued. Private restart:
`RESUME_CHECKPOINT_v50.md`, `FIRST_TRACK_AUDIT_v23.md`,
`nonempty-world-group-checkpoint-validation-v1.json`, `checkpoint-integrity-v50.json`
under `round11_collision_parity_20261020`. No commit or push.


### Native nonempty world gather return checkpoint v51

Native `6EFFDC0` now completes its nonempty world-gather return for declared
mode-0 pose-class and engine-trace inputs. 140 cases cover 440 supplied traces;
5,600 native code-image checks pass. Execution extends the prior grouping window
through native sampler/lazy initialization, LOS admission, contact insertion,
distance sorting, final sparse-map ownership transfer and intermediate cleanup.
The same UC frame is paused to install supplied class/owner views, then resumed.

Native sample initialization produces the 15-point pattern and later calls use
its cache. Range equality admits; misses, wrong components and far impacts reject.
Equal-distance contacts can reorder during native sorting; actual receipt order
is retained. Original overlap bytes remain intact and source hit arrays clear
after native ownership transfer. Distinct actor contacts are constructed, while
outer radial damage and independent actor health remain unjoined.

Mode 0 explicitly overrides the frozen default 2. Other modes/classes, real
physics, query-option copying and engine lifecycle remain unproven. Engine
queries/traces, class/weak/config/bone/pose, allocation/rehash/free and thread-guard
services remain supplied. Track 1 is incomplete; tracks 2–5 remain queued.
Private restart: `RESUME_CHECKPOINT_v51.md`, `FIRST_TRACK_AUDIT_v24.md`,
`complete-world-gather-checkpoint-validation-v2.json`, `checkpoint-integrity-v51.json`
under `round11_collision_parity_20261020`. No commit or push.


### Native world-to-radial independent health checkpoint v52

The nonempty native world gather now feeds native gather-event construction,
radial filtering/falloff, source rules, typed dispatch and independent actor
health in one UC. 288 mode-0 cases across 23 damage target tags match 1,104
separate per-actor native radial replays. Distinct model/interface/tag-owner/
attribute objects preserve per-actor health, events and damage causes. Owned
actor/component views are prepared before entry; no grouping pause or synthesized
gather output is used. Models here have one synthetic main health attribute.

The joined fixture now uses one shared settings object for world and damage,
and native query setup/copy replaces no-op options handling. Four direct audit
replays verify both fixes. Algorithm 1 additionally passes 32 comparison cases
across three damage tags against a separate mode-0 joined fixture. Together,
13,002 native code-image checks pass. Native query inputs use empty ignore lists.

Modes 0/1 override frozen default 2. Default-mode execution, other component
classes, authored multi-section health/config joins and actual engine geometry,
identity/lifecycle remain open. Physics queries/traces, class/weak/property/pose/
hit-location views and allocator/rehash/name/thread/free services remain supplied.
The 23 damage tags do not establish 23 native physics subclasses. Track 1 stays
incomplete; tracks 2–5 remain queued. Private restart: `RESUME_CHECKPOINT_v52.md`,
`FIRST_TRACK_AUDIT_v25.md`, `joined-world-radial-checkpoint-validation-v1.json`,
`checkpoint-integrity-v52.json` under `round11_collision_parity_20261020`.
No commit or push.


### Frozen-default world query checkpoint v53

Native selector 2, the frozen PE default, now runs the SkinnedMesh pose path
through visibility masks/callbacks, contact construction, radial rules and
independent actor health. All 288 cases match the frozen mode-0 joined dataset
across 23 damage tags. 552 visibility-cache reuses are directly observed.
32 additional cases cover blocked/clear misses, cache reuse, bounds variation,
radius equality/outside and GC/order. Together, 18,880 code-image checks pass.

The remaining branch getters are now statically name-bound to
SkeletalMeshComponent, InstancedStaticMeshComponent and ShapeComponent. Their
positive paths, authored multi-section health/config joins and actual engine
geometry/identity/lifecycle remain open. Engine bounds/queries, class/pose/weak/
property views and allocator/runtime services remain supplied. Static default
selection does not prove live config, and image counts are not branch coverage.

Track 1 remains incomplete; tracks 2–5 stay queued. Private restart:
`RESUME_CHECKPOINT_v53.md`, `FIRST_TRACK_AUDIT_v26.md`,
`default-world-checkpoint-validation-v1.json`, `checkpoint-integrity-v53.json`
under `round11_collision_parity_20261020`. No commit or push.

### Native component branches checkpoint v54

The frozen default selector 2 now has 64 owned component cases (16 scenarios,
GC on/off, trace hit/miss): Skinned pose/empty, generic center, Skeletal default
and indexed body handles, InstancedStaticMesh identity/translation/index bounds/
empty pose/item filtering, and Shape raw codes 1/2/3 candidate points. Analytic
world point sets and a separate native radial-to-health oracle match; 4,288
code-image checks and guarded component allocations pass. Skeletal sampling
passes no item filter, while the instanced route rejects a wrong Hit.Item.

Class metadata, body handles/poses, shape values, physics and runtime services
remain supplied. Unit component transforms and translated instances are tested;
rotation/scale breadth, real engine views and authored multi-section config joins
remain open. Code-image counts are not branch coverage. Track 1 is incomplete;
tracks 2-5 remain queued. Private restart: RESUME_CHECKPOINT_v54.md,
FIRST_TRACK_AUDIT_v27.md, component-branches-checkpoint-validation-v1.json,
checkpoint-integrity-v54.json under round11_collision_parity_20261020.
No live server access, commit or push.

### Authored section health checkpoint v55

226 native world-to-health cases passed across 23 vehicle damage-row groups:
113 exported section views with GC off/on, 452 independent actor health oracles,
and 15,142 code-image checks. Two actors retain distinct authored health limits
and routing state. Source checks bind 139 files and match enabled health
fragments for all 32 included variants. These prove config arithmetic under
supplied initialization and section resolution; native asset loading/module
order and actual physics remain open. Track 1 is incomplete; tracks 2-5 queued.

Private restart: RESUME_CHECKPOINT_v55.md, FIRST_TRACK_AUDIT_v28.md,
world-authored-sections-checkpoint-validation-v1.json, checkpoint-integrity-v55.json.
A separate 308-case native surface/section resolver run is pending and excluded
from this checkpoint's proof. No live access, commit or push.

### Native surface/section join checkpoint v56

All 154 catalog slots passed through native component-registry/face/item lookup,
surface group/slot resolution, section and hit-location selection, damage rules
and authored section health: 308 cases with GC off/on and two actors. Another
46 guard/item/numbered-slot cases passed. Across these, 662 separate native health
oracles match. The former supplied 6B80230/5338730/50BF880 answers now execute
natively. StaticMeshComponent is PE-name-bound; runtime metadata remains owned.

Eight empty-fragment cases also pass native discovery/dead-object gates and the
WD/base apply continuation. Total: 28,738 code-image checks. Populated fragment
installation, attribute/delegate creation, actual asset loading/registration,
geometry and remaining runtime/lifecycle gaps stay open. Catalog registry/face
views and engine services are supplied; counts do not imply branch coverage.
Track 1 remains incomplete; tracks 2-5 stay queued.

Private restart: RESUME_CHECKPOINT_v56.md, FIRST_TRACK_AUDIT_v29.md,
world-surface-resolver-checkpoint-validation-v1.json, checkpoint-integrity-v56.json.
All capture jobs are terminal. No live access, commit or push.

### Native fragment installation checkpoint v57

46 source-ordered installation setups and 308 downstream slot-damage cases passed.
Native insertion starts from empty preallocated section and complex-surface maps;
source config identities are preserved. Enabled fragments are applied separately,
and all 32 variant health/complex views match their 23 source templates. Native
world-to-health results match separate native health oracles. Total: 26,512
code-image checks, which do not imply branch coverage.

Attribute handles, registration/notification backends and engine runtime services
remain supplied. Physics-group maps are empty in this dataset; the next prototype
copies real source physics rows natively. Runtime module order, real attributes,
callback delivery, geometry and lifecycle remain open. Track 1 is incomplete;
tracks 2-5 queued. Private restart: RESUME_CHECKPOINT_v57.md, FIRST_TRACK_AUDIT_v30.md,
populated-fragment-checkpoint-validation-v1.json, checkpoint-integrity-v57.json.
No live access, commit or push.

### Corrected native physics installation checkpoint v58

All three source health-fragment maps now install natively: health sections,
complex-surface mappings and physics-group routing. The corrected run passed
46 setups and 308 downstream slot-damage cases, installing 92 physics groups
across 23 templates with GC off/on. Total: 26,834 code-image checks.

Physics tag/float entries are 20 bytes. The initial new fixture incorrectly used
24 bytes and its partial run was stopped before a success receipt. A native
consumer regression now rejects that malformed layout and matches independent
native health results after correction (two cases, 160 additional image checks).
The two labels select installation GC; they do not independently toggle consumer
GC. Historical physics-prototype claims are superseded by the private layout
correction. v57's health/complex validation is unaffected.

Geometry, real attribute/delegate/notification backends and runtime module order
remain open. Track 1 is incomplete; tracks 2-5 queued. Private restart:
RESUME_CHECKPOINT_v58.md, FIRST_TRACK_AUDIT_v31.md,
physics-fragment-checkpoint-validation-v1.json, checkpoint-integrity-v58.json.
No live access, commit or push.

### Installed physics to native collision health checkpoint v59

46 native source installations now feed native primitive/body group lookup,
parent-group selection, physics routing and authored section health. All 416
cases passed across 23 templates: exact/child group queries, small/depletion-sized
damage, and explicitly observed consumer GC off/on. No group or section-result
injection is used. Native health oracles match; 13,534 code-image checks pass.

Physics routes may reference globally named tags absent from a model's health
map. The independent oracle now preserves those names while keeping the health
sections absent; health/event behavior matches. Shape reachability remains an
owned input. Primitive/body/weak registration, real runtime backends and asset
loading remain open. Track 1 is incomplete; tracks 2-5 queued. Next is joining
native-installed maps to the full mesh/contact callback chain.

Private restart: RESUME_CHECKPOINT_v59.md, FIRST_TRACK_AUDIT_v32.md,
installed-geometry-checkpoint-validation-v1.json, checkpoint-integrity-v59.json.
All capture jobs are terminal. No live access, commit or push.

### Installed maps through native contact callback checkpoint v60

All 416 source-linked contact cases passed across 23 templates and 46 native
installations, with installation/contact GC off/on. Native-installed health,
complex and physics map identities survive the full owned mesh/contact/filter/
base-callback/cue/rules/owner-health chain; contact setup reads the physics map
without reseeding it. Owner health uses authored maxima. Separate native full
callback and section-health fixtures match upstream/target outputs and authored
owner health/events/returns/recursive calls. 5,860 image integrity checks pass.

Settings linkage is static; native active configuration selection remains the
next catalog join. A separate Humvee configuration prototype passes GC off/on,
but does not establish catalog completion. Owned geometry/registry, attribute/
delegate/notification/timer backends and actual engine lifecycle remain open.
Track 1 is incomplete; tracks 2-5 queued. Private restart: RESUME_CHECKPOINT_v60.md,
FIRST_TRACK_AUDIT_v33.md, installed-contact-checkpoint-validation-v1.json,
checkpoint-integrity-v60.json. All capture jobs terminal. No live access or push.

### Native selected configuration and installed contact checkpoint v61

All 576 cases passed: nine authored wheeled configurations/eight templates,
18 native source installations and 36 override/fallback selection setups. Native
configuration construction/selection/notification and linked settings copy now
precede the full owned contact chain and source-installed owner health/physics
maps in one emulator. Config/map identities and copied settings survive. Separate
configured callback and section-health fixtures match target/cue/config outputs
and authored owner health/events/returns/recursive requests. 7,290 code-image
integrity checks pass. Installation/contact GC is varied; configuration-stage GC
is not independently varied. First exact group adds low/high speed boundaries.

Real attribute/delegate/notification backends, auxiliary gameplay/module lifecycle,
actual geometry/loading/order and network/event/cache/timer delivery remain open.
Static backend leads and raw CFGs are saved privately, without execution claims.
Track 1 is incomplete; tracks 2-5 queued. Private restart: RESUME_CHECKPOINT_v61.md,
FIRST_TRACK_AUDIT_v34.md, ATTRIBUTE_BACKEND_NEXT_v1.md,
installed-configured-checkpoint-validation-v1.json, checkpoint-integrity-v61.json.
All capture jobs terminal. No live access, commit or push.

The v61 high-speed cases do not deplete owner sections under these authored
curve/routing outputs; they do not establish destruction behavior. The validator
records 308 nonpositive owner requests and zero depleted cases.
