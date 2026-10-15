---
title: "Demolition"
parent: "Content"
---

# Wardogs — Demolition Reference (v2)
*Extracted from cooked game data (JSON export, [`Wardogs/Content/Demolition/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Demolition), 86 source files: 39 demolition assets, 9 component settings, 19 remnant-mesh assets, 19 rulesets). Parsed with a Python script. The 19 ruleset files each contain several `--- export:` blocks and were split on those headers. Values are the raw exported values.*

> **How the parts link:** each `BHDemolitionDataAsset` (one per destructible prop) points at one **component settings** asset (rendering/collision), one **ruleset** (which damage sources or vehicles may demolish it), one or more **remnant mesh** assets (what is left behind), plus VFX, a crosstalk audio tag, and fragment physics.

---

## Season 02 update (2026-10-15)

- **New asset:** `Fences_Metal_03` (4 meshes, `Default_Tank` settings, `LargeAndMediumVehiclesAndExplosions` ruleset, remnant set `RM_Fence_Metal_Residential_03_01_A`).
- **Counts:** demolition assets 38 → 39, remnant sets 16 → 19, rulesets 15 → 19. No demolition assets were removed.
- **New remnant sets:** `RM_Fence_Metal_Residential_03_01_A`, `RM_Fences_Plaster_Residential_01_A`, `RM_Fences_Plaster_Residential_Pillar_01_A`.
- **Mesh counts:** `Bollard_Metal_01` 1 → 2; `Fences_Concrete_01` 4 → 6 (the two plaster remnant sets are added to it).
- **Bushes_Flora and Saplings:** ruleset `Everything` → `EverythingAndMolotov` (adds `Meta.Damage.Molotov`, minimum distance 300).
- **Fences_Wood_01_A and Fences_Wood_01_B:** ruleset `LargeAndMediumVehiclesAndExplosions` → `LargeAndMediumVehiclesExplosionsAndBuildables`.
- **Rulesets:** `Everything` now also includes [`Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Buildables.json); new [`Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Buildables.json) ruleset (single buildable rule).
- **Vehicle rules:** AirVehicles 6 → 8 entries (ROT_04), TrackedVehicles 7 → 8 (TNK_04.Default), WheeledVehicles 11 → 13 (WHL_08), LargeWheeledVehicles 9 → 11 (WHL_08), LargeAndMediumWheeledVehicles 10 → 12 (WHL_08).

## 1. Asset Families

| Family | Count | Type | Path |
|---|---|---|---|
| Demolition assets | 39 | `BHDemolitionDataAsset` | `Demolition/` |
| Component settings | 9 | `BHDemolitionComponentSettings` | [`Demolition/ComponentSettings/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Demolition/ComponentSettings) |
| Remnant mesh sets | 19 | `BHDemolitionRemnantMeshesAsset` | [`Demolition/Remnants/DA/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Demolition/Remnants/DA) |
| Rulesets | 19 | `BHDemolitionRuleset` plus rule sub-objects | [`Demolition/RuleSets/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Demolition/RuleSets) (`Explosions/`, `Vehicles/`) |

---

## 2. Demolition Assets (all 39)

Prefix `DA_Demolition_` removed from names. "Zones" are the `PermittedZones` tags (`Important` and `Distant`), presumably level-of-detail or distance zones (not confirmed). "Restitution" is the first fragment's `RestitutionImpulseMultiplier`. Where a second fragment exists it is listed after a slash, with `-` meaning the field is absent.

| Asset | Meshes | Component settings | Ruleset | Zones | VFX (`NS_`) | Restitution | Remnant set(s) | Remnant actor | Crosstalk tag (`Audio.Event.Prop.Demolition.*`) |
|---|---|---|---|---|---|---|---|---|---|
| BarbedWire_01 | 2 | Default | Everything | Important, Distant | MetalGeneralSmash | 0.175 / - | - | - | FenceMetalChainlink |
| Bollard_Metal_01 | 2 | Default | Everything | Important, Distant | MetalGeneralSmash | 0.3 | - | - | Sign |
| BrickWall_01_A | 2 | ConcreteWalls_01 | TanksAndLargeExplosions | Important, Distant | BrickSmash | 0.4 | RM_BrickWall_01_A | - | FenceConcrete |
| BrickWall_01_B | 8 | ConcreteWalls_01 | TanksAndLargeExplosions | Important, Distant | BrickSmash | 0.4 | RM_BrickWall_01_B | - | FenceConcrete |
| BrickWall_01_C | 5 | ConcreteWalls_01 | TanksAndLargeExplosions | Important, Distant | BrickPillarSmash | 0.4 | - | - | FenceConcrete |
| Bushes_Flora | 2 | Default_Bushes | EverythingAndMolotov | Important | BushSmash_01 | 0.05 | - | - | Bush |
| ConcreteBarrier_01 | 1 | ConcreteWalls_01 | TanksAndMedLargeExplosions | Important, Distant | ConcreteSmash | 0.2 | RM_ConcreteBarrier_01 | - | FenceConcrete |
| ConcreteBarrier_02 | 1 | ConcreteWalls_01 | TanksAndMedLargeExplosions | Important, Distant | ConcreteSmash | 0.4 | RM_ConcreteBarrier_02 | - | FenceConcrete |
| Corrugated_Metal_01a | 1 | ShadowCacheStatic | Everything | Important, Distant | MetalGeneralSmash | 0.2 | - | - | FenceMetalSheet |
| Fences_ChainlinkTarp_01 | 2 | Default | Everything | Important, Distant | MetalGeneralSmash | 0.2 | - | - | FenceMetalChainlink |
| Fences_ChainlinkWire_01 | 3 | Default | Everything | Important, Distant | MetalGeneralSmash | 0.2 | - | - | FenceMetalChainlink |
| Fences_Chainlink_01 | 6 | Default_ChainLink | Everything | Important, Distant | MetalGeneralSmash | 0.2 | - | - | FenceMetalChainlink |
| Fences_Concrete_01 | 6 | ConcreteWalls_01 | TanksAndMedLargeExplosions | Important, Distant | ConcreteSmash | 0.4 | RM_Fence_Concrete_01_A, RM_Fence_FlowerBed_Concrete_WallSection_01, RM_Fences_Plaster_Residential_01_A, RM_Fences_Plaster_Residential_Pillar_01_A | - | FenceConcrete |
| Fences_Concrete_01_B | 3 | ConcreteWalls_01 | TanksAndMedLargeExplosions | Important, Distant | ConcretePillarSmash | 0.4 | RM_Fence_Concrete_01_B | - | FenceConcrete |
| Fences_Concrete_01_C | 4 | ConcreteWalls_01 | TanksAndMedLargeExplosions | Important, Distant | ConcreteSmash | 0.4 | - | - | FenceConcrete |
| Fences_Concrete_03_A | 4 | Default_Tank | TanksAndLargeExplosions | Distant, Important | ConcreteSmash | 0.4 | RM_Fence_Concrete_03_A | - | FenceConcrete |
| Fences_Concrete_03_B | 2 | Default_Tank | TanksAndLargeExplosions | Important, Distant | ConcreteSmash | 0.4 | RM_Fence_Concrete_03_B | - | FenceConcrete |
| Fences_Concrete_03_C | 7 | Default_Tank | TanksAndLargeExplosions | Important, Distant | ConcretePillarSmash | 0.4 | RM_Fence_Concrete_03_C | - | FenceConcrete |
| Fences_Metal_01 | 9 | Default_Tank | TanksAndMedLargeExplosions | Important, Distant | MetalGeneralSmash | 0.3 | - | - | FenceMetalSheet |
| Fences_Metal_02 | 4 | Default_Tank | TanksAndMedLargeExplosions | Important, Distant | MetalConcreteSmash | 0.4 | - | - | FenceMetalSheet |
| Fences_Metal_03 | 4 | Default_Tank | LargeAndMediumVehiclesAndExplosions | Important, Distant | MetalConcreteSmash | 0.4 | RM_Fence_Metal_Residential_03_01_A | - | FenceMetalSheet |
| Fences_Ornamental_01 | 2 | Default_Tank | TanksAndMedLargeExplosions | Important, Distant | MetalConcreteSmash | 0.4 | RM_Fences_Ornamental_01_A, RM_Fences_Ornamental_01_B | - | FenceMetalSheet |
| Fences_SmallConcrete_01_A | 1 | Default_Tank | TanksAndLargeExplosions | Important, Distant | ConcreteSmash | 0.4 | RM_Fences_SmallConcrete_01_A | - | FenceConcrete |
| Fences_SmallConcrete_01_B | 1 | Default_Tank | TanksAndLargeExplosions | Important, Distant | ConcreteSmash | 0.4 | RM_Fences_SmallConcrete_01_B | - | FenceConcrete |
| Fences_SmallConcrete_01_C | 1 | Default_Tank | TanksAndLargeExplosions | Important, Distant | ConcreteSmash | 0.4 | RM_Fences_SmallConcrete_01_C | - | FenceConcrete |
| Fences_Wood_01_A | 7 | Fences | LargeAndMediumVehiclesExplosionsAndBuildables | Important, Distant | WoodSmash_Fence | 0.125 / - | RM_Fences_Wood_01_A (`DA_RM_` prefix) | - | FenceWood |
| Fences_Wood_01_B | 4 | Fences | LargeAndMediumVehiclesExplosionsAndBuildables | Important, Distant | WoodSmash_Fence | 0.125 | RM_Fences_Wood_01_A | - | FenceWood |
| Fences_Wood_02 | 4 | Fences | Everything | Important, Distant | WoodSmash_Fence_NoPlanks | 0.125 | - | - | FenceWood |
| LampPost_01 | 2 | Default (developer copy) | LargeVehiclesAndExplosions | Important, Distant | LampPostSmash | 0.3 | - | - | Sign |
| MetalFence_01 | 1 | ShadowCacheStatic | TanksAndMedLargeExplosions | Important, Distant | MetalGeneralSmash | 0.3 | - | - | FenceMetalSheet |
| MetalFence_Support_01 | 0 | Default | TanksAndMedLargeExplosions | Important, Distant | MetalConcreteSmash | 0.2 | - | - | FenceConcrete |
| Saplings | 10 | CS_Saplings | EverythingAndMolotov | Important | SaplingSmash_01 | 0.1 | - | - | Tree |
| Signage_Large_Metal_01 | 3 | Default_Tank | TanksAndLargeExplosions | Important, Distant | MetalGeneralSmash | 0.4 | - | BP_Remnant_RoadSigns_C | FenceMetalSheet |
| Signage_Metal_01 | 12 | Signage_Metal | Everything | Important, Distant | MetalGeneralSmash | 0.2 | - | BP_Remnant_RoadSigns_C | Sign |
| SmallMetalFence_1m_01 | 2 | Default | Everything | Important, Distant | MetalGeneralSmash | 0.3 | - | - | FenceMetalSheet |
| SmallMetalFence_2m_01 | 5 | Default | Everything | Important, Distant | MetalGeneralSmash | 0.3 | - | - | FenceMetalSheet |
| Structures_Metal_01 | 3 | Default | Everything | Important, Distant | MetalGeneralSmash | 0.4 | - | - | FenceMetalSheet |
| TelephonePole_Concrete_01 | 1 | Default (developer copy) | LargeAndMediumVehiclesAndExplosions | Important, Distant | LampPostSmash | 0.3 | - | - | FenceConcrete |
| TelephoneWireCable_40M_01_A | 1 | ShadowCacheStatic | LargeAndMediumVehiclesAndExplosions | Important, Distant | MetalGeneralSmash | 0.3 | - | - | Sign |

Totals across the 39 assets:
- **Rulesets used:** Everything 11, EverythingAndMolotov 2, TanksAndLargeExplosions 10, TanksAndMedLargeExplosions 10, LargeAndMediumVehiclesAndExplosions 3, LargeAndMediumVehiclesExplosionsAndBuildables 2, LargeVehiclesAndExplosions 1.
- **Zones:** Important + Distant 36; Important only 2 (Bushes_Flora, Saplings); Distant + Important 1 (Fences_Concrete_03_A).
- **VFX:** MetalGeneralSmash 14, ConcreteSmash 9, MetalConcreteSmash 4, BrickSmash 2, ConcretePillarSmash 2, WoodSmash_Fence 2, LampPostSmash 2, and one each of BrickPillarSmash, BushSmash_01, WoodSmash_Fence_NoPlanks, SaplingSmash_01.
- **Crosstalk tags:** FenceConcrete 16, FenceMetalSheet 10, Sign 4, FenceMetalChainlink 4, FenceWood 3, Bush 1, Tree 1.
- **Remnant sets:** 16 of the 39 assets reference one or more remnant sets. All 19 remnant assets are referenced by at least one asset.
- **Remnant actor:** only the two signage assets (`Signage_Large_Metal_01`, `Signage_Metal_01`) set `DemolitionRemnantActor` (`BP_Remnant_RoadSigns_C`).
- **Far-representation collision:** `bEnableCollisionWhenInFarRepresentation` appears only on `Bushes_Flora` and `Saplings`, and it is `false` on both.

---

## 3. Component Settings (9)

Each setting sets instance culling, Nanite and shadow-cache behaviour, plus a collision profile. Blank cells mean the field is not set in the export (engine default).

| Setting | Instance start / end cull | Ray tracing | WPO disable dist | Nanite pixel-prog dist / screen size | Shadow cache | bGenerateHitEvents | Collision profile |
|---|---|---|---|---|---|---|---|
| `DA_Demolition_CS_Default` | 201,000 / 201,100 | true | - | - | - | - | BHDemolition |
| [`DA_Demolition_CS_ConcreteWalls_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Demolition/ComponentSettings/DA_Demolition_CS_ConcreteWalls_01.json) | 201,000 / 201,100 | true | - | - | - | **true** | BHDemolition |
| [`DA_Demolition_CS_Default_Tank`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Demolition/ComponentSettings/DA_Demolition_CS_Default_Tank.json) | 201,000 / 201,100 | true | - | - | - | **true** | BHDemolition |
| [`DA_Demolition_CS_Default_ChainLink`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Demolition/ComponentSettings/DA_Demolition_CS_Default_ChainLink.json) | 201,000 / 201,100 | true | - | - | - | - | BHDemolitionChainlinkFence |
| [`DA_Demolition_CS_Default_Bushes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Demolition/ComponentSettings/DA_Demolition_CS_Default_Bushes.json) | 201,000 / 201,100 | - | 2,000 | 2,000 / 1.0 | Static | - | BHDemolitionBushes |
| [`DA_CS_Saplings`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Demolition/ComponentSettings/DA_CS_Saplings.json) | 201,000 / 201,100 | - | 2,000 | 2,000 / 1.0 | Static | - | BHDemolitionFlora |
| [`DA_Demolition_CS_Fences`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Demolition/ComponentSettings/DA_Demolition_CS_Fences.json) | 201,000 / 201,100 | true | 10,000 | 10,000 / 0.5 | Static | **true** | BHDemolition |
| [`DA_Demolition_CS_ShadowCacheStatic`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Demolition/ComponentSettings/DA_Demolition_CS_ShadowCacheStatic.json) | 201,000 / 201,100 | true | - | - | Static | - | BHDemolition |
| [`DA_Demolition_CS_Signage_Metal`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Demolition/ComponentSettings/DA_Demolition_CS_Signage_Metal.json) | 201,000 / 201,100 | true | - | - | - | - | BHDemolition |

Cull distances are in the same engine units as the rest of the export (probably cm, so about 2 km; not confirmed).

---

## 4. Remnant Meshes (19)

Each remnant set holds `RemnantMeshes` entries, each with a `NearMesh` and a `FarMesh`. In all 19 sets, `NearMesh` and `FarMesh` name the same asset, except the ornamental fences. Offset and far-rep override are null in every entry.

| Remnant set | Entries | Near/far mesh |
|---|---|---|
| RM_BrickWall_01_A | 1 | SM_RemnantNear_Brick_Wall_01a |
| RM_BrickWall_01_B | 1 | SM_RemnantNear_Brick_Wall_01b |
| RM_ConcreteBarrier_01 | 1 | S_RemnantNear_Old_Concrete_Barrier_vkurdfd |
| RM_ConcreteBarrier_02 | 1 | S_RemnantNear_Concrete_Barrier_tlisbicfa |
| RM_Fence_Concrete_01_A | 1 | SM_RemnantNear_Fence_Concrete_Wall_01b |
| RM_Fence_Concrete_01_B | 1 | SM_Fence_Concrete_Generic_01_Pillar_01c |
| RM_Fence_Concrete_03_A | 1 | SM_Wall_Concrete_Industrial_01e |
| RM_Fence_Concrete_03_B | 1 | SM_Wall_Concrete_Industrial_01f |
| RM_Fence_Concrete_03_C | 1 | SM_Wall_Concrete_Industrial_01_Pillar_01e |
| RM_Fence_FlowerBed_Concrete_WallSection_01 | 1 | SM_FlowerBed_Concrete_WallSection_dst_01a |
| RM_Fence_Metal_Residential_03_01_A | 1 | SM_Fence_Metal_Residential_dst_03a |
| RM_Fences_Ornamental_01_A | 1 | near: SM_RemnantNear_OrnamentalFence_A_Mid_01a / far: SM_RemnantFar_OrnamentalFence_A_Mid_01a |
| RM_Fences_Ornamental_01_B | 1 | near: SM_RemnantNear_OrnamentalFence_A_Corner_01a / far: SM_RemnantFar_OrnamentalFence_A_Corner_01a |
| RM_Fences_Plaster_Residential_01_A | 1 | SM_Wall_Plaster_Residential_dst_01a |
| RM_Fences_Plaster_Residential_Pillar_01_A | 1 | SM_Wall_Plaster_Residential_01_Pillar_dst_01a |
| RM_Fences_SmallConcrete_01_A | 1 | SM_RemnantNear_Low_Wall_Left_01 |
| RM_Fences_SmallConcrete_01_B | 1 | SM_RemnantNear_Low_Wall_Middle_0 |
| RM_Fences_SmallConcrete_01_C | 1 | SM_RemnantNear_Low_Wall_Right_01 |
| DA_RM_Fences_Wood_01_A | 3 | SM_RemnantNear_Fence_Wood_Wall_01a, _01b, _01c |

(Remnant asset names keep the `DA_Demolition_RM_` prefix except the wood set, which is [`DA_RM_Fences_Wood_01_A`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Demolition/Remnants/DA/DA_RM_Fences_Wood_01_A.json).)

---

## 5. Rulesets

Every ruleset except [`BH_Demolition_RS_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Demolition/RuleSets/BH_Demolition_RS_Buildables.json) is an OR of its children. No `And` or `Not` rule types appear in the export. Ruleset names reference other rulesets, so the composed trees are shown below.

### 5a. Composition

| Ruleset | Composed as OR of |
|---|---|
| BH_Demolition_RS_Buildables | A single buildable rule (`WDDemolitionRule_Buildable`, no properties exported) |
| BH_Demolition_RS_Everything | AllVehicles, AllExplosions, Buildables |
| BH_Demolition_RS_EverythingAndMolotov | AllVehicles, AllExplosions, Buildables, Molotov |
| BH_Demolition_RS_AllVehicles | AirVehicles, TrackedVehicles, WheeledVehicles |
| BH_Demolition_RS_AllExplosions | LargeExplosives, MediumExplosives, SmallExplosions |
| BH_Demolition_RS_TanksAndLargeExplosions | LargeExplosives, TrackedVehicles |
| BH_Demolition_RS_TanksAndMedLargeExplosions | LargeExplosives, MediumExplosives, TrackedVehicles |
| BH_Demolition_RS_LargeAndMediumVehiclesAndExplosions | AllExplosions, TrackedVehicles, AirVehicles, LargeAndMediumWheeledVehicles |
| BH_Demolition_RS_LargeVehiclesAndExplosions | AllExplosions, TrackedVehicles, AirVehicles, LargeWheeledVehicles |
| BH_Demolition_RS_LargeAndMediumVehiclesExplosionsAndBuildables | LargeAndMediumVehiclesAndExplosions, Buildables |

### 5b. Explosion rules (`WDDemolitionRule_Explosion`)

| Ruleset | Permitted damage source tags | MinimumDistanceFromExplosionSource |
|---|---|---|
| SmallExplosions | `Meta.Damage.C4`, `Meta.Damage.Grenade`, `Meta.Damage.Explosive.Grenade.40mm`, `Meta.Damage.Explosive.Utility.C4`, `Meta.Damage.Explosive.Utility.Claymore`, `Meta.Damage.Explosive.Utility.IED` | 300 |
| MediumExplosives | `Meta.Damage.Explosive.Rocket` | 400 |
| LargeExplosives | `Meta.Damage.Explosive.Utility.ATMine`, `Meta.Damage.Explosive.VehicleExplosion`, `Meta.Damage.Landmine`, `Meta.Damage.Cannon.30mm`, `Meta.Damage.Explosive.Rocket.120mm` | 500 |
| Molotov | `Meta.Damage.Molotov` | 300 |

### 5c. Vehicle rules (`BHDemolitionRule_Vehicle`)

Every vehicle rule sets `bPermitOverlaps = true` and `bPermitBlockingHits = true`.

| Ruleset | Permitted vehicle variants |
|---|---|
| AirVehicles | Airplane.FWG.Default, Rotary.Littlebird.Default, Rotary.Littlebird.MountedMachineGuns, Rotary.Havoc.Default, Rotary.ROT_01.Default, Rotary.ROT_01.MountedMachineGuns, Rotary.ROT_04.MountedMachineGuns, Rotary.ROT_04.Default |
| TrackedVehicles | SpawnVehicle.Valkyra, SpawnVehicle.Manticore, SpawnVehicle.Lonestar, TNK_01.AntiAir, TNK_01.Artillery, TNK_01.Light, TNK_01.Heavy, TNK_04.Default |
| WheeledVehicles (13) | Bobcat.Default, DuneBuggy.Default, Humvee.Default, Humvee.MachineGun, Humvee.Minigun, Kodiak.Default, Kodiak.Pickup, Kodiak.MachineGun, Ural.Default, Ural.Attack, Ural.Battle, WHL_08.Default, WHL_08.MachineGun |
| LargeWheeledVehicles (11) | Humvee.Default, Humvee.MachineGun, Humvee.Minigun, Kodiak.Default, Kodiak.Pickup, Kodiak.MachineGun, Ural.Default, Ural.Attack, Ural.Battle, WHL_08.Default, WHL_08.MachineGun |
| LargeAndMediumWheeledVehicles (12) | the eleven LargeWheeled entries plus DuneBuggy.Default |

Vehicle paths are `Vehicle.Variant.<Air|Land>.<Type>.<Model>.<Variant>` tags.

---

## 6. How Values Combine

- **Which hits can demolish (likely):** a demolition asset's ruleset is tested against the incoming damage source (explosion rules) or the colliding vehicle (vehicle rules). A match appears to permit demolition. The export does not state the trigger logic.
- **Minimum distance** (300 / 400 / 500) is attached to explosion rules. Its unit and effect are not confirmed. Probably the minimum distance from the blast at which the rule counts.
- **Fragment restitution** (0.05 to 0.4 across assets) multiplies the impulse that fragments receive. Two-fragment assets have a second fragment with no restitution override.
- **Which VFX plays** is set per asset by `DemolitionVFX` (a Niagara system). The crosstalk tag is the audio event for the same break.

---

## 7. Observations

- The ruleset names suggest a tiering: `Everything` is the broadest, and the `Tanks…` and `LargeAndMedium…` sets cover a narrower range of sources. The export does not say which tier is meant to be harder to demolish.
- `LampPost_01` and `TelephonePole_Concrete_01` use component settings from [`/Game/Developers/Celesteneukirchen/Demolition/Settings/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Developers/Celesteneukirchen/Demolition/Settings) (a developer folder), not the main `ComponentSettings` path. Their values may differ from the main copies. This was not compared.
- `Fences_Wood_01_A` and `Fences_Wood_01_B` share one remnant asset, [`DA_RM_Fences_Wood_01_A`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Demolition/Remnants/DA/DA_RM_Fences_Wood_01_A.json), which uses the `DA_RM_` prefix rather than `DA_Demolition_RM_` like the other remnant sets.

---

## 8. Still Not Pulled / Limitations

- **Demolition behaviour is not in this folder.** The data shows what can demolish an asset and what it leaves, but not the impulse, mass, damage-to-break threshold, or fragment counts (only restitution is exported).
- **Units are not stated.** Minimum distance, cull distances and fragment physics are used as exported. The cm assumption is an inference.
- **Remnant `Offset` and `FarRepresentationData_Override`** are null in every entry, so their use cannot be documented.
- **Mesh-level data** (`SourceMeshes` entries' `FarRepresentationData`, custom primitive colours) is not summarised beyond the mesh name.
- **Zones** (`Important`, `Distant`) are not defined in this folder. Their meaning is an inference from the names.
- **Crosstalk and VFX asset paths** are referenced by name only. The audio and Niagara assets themselves are outside this category.
