# Cross-Reference Index

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Where to find things that are **referenced in one doc but defined in another**.
Bulk resolution for the CROSS_REF gap bucket (see
[`gap_resolution/CROSS_REF.md`](gap_resolution/CROSS_REF.md)).

Reading pattern: a data doc mentions `<Thing>` with a "not in this
category" / "referenced by path only" note. This index tells you the
canonical doc where `<Thing>` IS covered.

---

## By asset-name prefix

### `CRV_*` / `CT_*` — Curve assets and Curve Tables

| Referenced in | Example reference | Defined in |
|---|---|---|
| `Wardogs_GameFeatures_Parachutes_v2.md` | `CRV_ParachutePunishment_Damage` | Raw curve values: [`data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/`](data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/) — covered contextually in [`Wardogs_GameMechanics_v2.md`](../content/Wardogs_GameMechanics_v2.md) and [`Wardogs_Characters_v2.md`](../content/Wardogs_Characters_v2.md) |
| `Wardogs_GameFeatures_UnderbarrelGrenadeLauncher_v2.md` | `CT_Weapon_Spread` | Full curve-table values in [`data/Wardogs/Content/Items/Weapons/Curves/CT_Weapon_Spread.json`](data/Wardogs/Content/Items/Weapons/Curves/CT_Weapon_Spread.json); used by weapons documented in [`Wardogs_InfantryWeapons_Stats_v1.md`](../content/Wardogs_InfantryWeapons_Stats_v1.md), [`Wardogs_Weapons_v2.md`](../content/Wardogs_Weapons_v2.md), and the game-features weapon docs |

### `DA_*` — DataAssets

| Prefix | Doc |
|---|---|
| `DA_<Weapon>_Stats` | [`Wardogs_InfantryWeapons_Stats_v1.md`](../content/Wardogs_InfantryWeapons_Stats_v1.md) (infantry), [`Wardogs_Weapons_v2.md`](../content/Wardogs_Weapons_v2.md) (general) |
| `DA_<Vehicle>_Stats` (e.g., `DA_WHL_07_Stats`, `DA_TNK_01_Stats`) | [`Wardogs_AllVehicles_Stats_Damage_v1.md`](../content/Wardogs_AllVehicles_Stats_Damage_v1.md) |
| `DA_AmmoModifier_*` | [`Wardogs_DamagePipeline_v2.md`](../pipelines/Wardogs_DamagePipeline_v2.md) §7.9 |
| `DA_Explosion_*` | [`Wardogs_VFX_v2.md`](../content/Wardogs_VFX_v2.md) explosions section |
| `DA_MuzzleFlash_*`, `DA_MF_MUZL_*` | [`Wardogs_VFX_v2.md`](../content/Wardogs_VFX_v2.md) muzzle flashes section |
| `DA_<Vehicle>_Exhaust` | [`Wardogs_VFX_v2.md`](../content/Wardogs_VFX_v2.md) exhaust section |
| `DA_AmmoModifier_<Type>` | [`Wardogs_DamagePipeline_v2.md`](../pipelines/Wardogs_DamagePipeline_v2.md) |

### `DT_*` — DataTables

| Prefix | Doc |
|---|---|
| `DT_GlobalDamage_InfantryData` + helpers | [`Wardogs_DamagePipeline_v2.md`](../pipelines/Wardogs_DamagePipeline_v2.md) §3 |
| `DT_GlobalDamage_VehicleData_<CODE>` | [`Wardogs_VehicleDamagePipeline_v1.md`](../pipelines/Wardogs_VehicleDamagePipeline_v1.md) §2.1 |
| `DT_Challenges_*` | [`Wardogs_Meta_v2.md`](../content/Wardogs_Meta_v2.md) challenges section |
| `DT_RewardLookup_*` | [`Wardogs_GameFeatures_Rewards_v2.md`](../game-features/Wardogs_GameFeatures_Rewards_v2.md) |
| `DT_VehicleMarket` | [`Wardogs_GameFeatures_Vehicles_v2.md`](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) vendor section |
| `DT_RadialWheelSlotType_*` | [`Wardogs_UI_v2.md`](../content/Wardogs_UI_v2.md) radial wheel section |
| `DT_EntityData_UI_*` | [`Wardogs_UI_v2.md`](../content/Wardogs_UI_v2.md) entity data section |
| `DT_GunsmithPopupOptions` | [`Wardogs_GameFeatures_Gunsmith_v2.md`](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) popups section |
| `DT_VehiclePropList` | [`Wardogs_Environment_v2.md`](../content/Wardogs_Environment_v2.md) |

### `B_<Blueprint>_C` — Blueprint classes

| Prefix | Doc |
|---|---|
| `B_CameraShake_*` | Referenced in [`Wardogs_VFX_v2.md`](../content/Wardogs_VFX_v2.md); shake behaviour internals **not documented** (Blueprint bytecode not exported — SDK has only property offsets) |
| `B_Gunsmith*` | [`Wardogs_GameFeatures_Gunsmith_v2.md`](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) |
| `B_ArchetypeCaliberModifiers_C`, `B_BoneDamageModifiers_C`, `B_AmmoTypeEffectiveness_C`, `B_VehicleSeatDamageReduction_C` | [`Wardogs_DamagePipeline_v2.md`](../pipelines/Wardogs_DamagePipeline_v2.md) §7 — the 4 damage modifier blueprints |
| `CP_*_C` (prefab classes) | Referenced in [`Wardogs_Destruction_v2.md`](../content/Wardogs_Destruction_v2.md) and [`Wardogs_ExternalAssets_v2.md`](../content/Wardogs_ExternalAssets_v2.md); internals (debris/collision/thresholds) **not exported** in cooked data |

### `NS_*` — Niagara systems

Niagara internals are compiled graphs that don't export to JSON. The
NS references across docs are **references by path only**; no doc
covers Niagara internals exhaustively.

Niagara systems referenced in:
- [`Wardogs_VFX_v2.md`](../content/Wardogs_VFX_v2.md) — recipe rows
- [`Wardogs_Demolition_v2.md`](../content/Wardogs_Demolition_v2.md)
- [`Wardogs_ExternalAssets_v2.md`](../content/Wardogs_ExternalAssets_v2.md)
- [`Wardogs_GameFeatures_Utility_v2.md`](../game-features/Wardogs_GameFeatures_Utility_v2.md)
- [`Wardogs_Maps_v2.md`](../content/Wardogs_Maps_v2.md)

Resolution path: FModel visual inspection, not CUE4Parse JSON. Not
scheduled for this project (would require tool addition).

### `T_*` — Textures

Textures are binary assets with no JSON parse pass. References across
docs point to texture paths only. No dedicated texture doc exists.

- `T_Reticle_*` referenced in [`Wardogs_GameFeatures_Gunsmith_v2.md`](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md)
- See the `data/` tree for the actual `.uasset` files if you need to
  inspect in FModel.

### `W_*` / `DL_*` — Widgets and Data Layers

| Prefix | Doc |
|---|---|
| `W_*` widgets | Referenced in [`Wardogs_UI_v2.md`](../content/Wardogs_UI_v2.md), [`Wardogs_GameFeatures_Gunsmith_v2.md`](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md), [`Wardogs_GameFeatures_Vehiclesmith_v2.md`](../game-features/Wardogs_GameFeatures_Vehiclesmith_v2.md) — widget binaries not JSON-parsed |
| `DL_*` data layers | Referenced in Vehiclesmith; data layers are UE world-partition constructs, not JSON-exported |

### `ID_*` — Audio profile data assets

| Example | Doc |
|---|---|
| `ID_Backpack_Audio`, `ID_Vest_Audio` | [`Wardogs_Audio_v2.md`](../content/Wardogs_Audio_v2.md) player audio section |
| `ID_Vox_*` | [`Wardogs_Audio_v2.md`](../content/Wardogs_Audio_v2.md) vox section |

### `MirrorDataTable` (animation reference)

- Referenced in [`Wardogs_Animation_v2.md`](../content/Wardogs_Animation_v2.md)
- The field is `null` in every exported schema. **Confirmed: no
  MirrorDataTable is wired into any motion-matching schema in this
  dump.** May be used by a different system (control rig, first-person
  layer) not covered by current exports.

### `Id.Item.*` — GameplayTag item IDs

| Example | Doc |
|---|---|
| `Id.Item.OPT_08` (optic) | [`Wardogs_Items_v2.md`](../content/Wardogs_Items_v2.md) optic section |
| `Id.Item.MAG_*` (magazine) | [`Wardogs_Items_v2.md`](../content/Wardogs_Items_v2.md) magazine section |
| `Id.Item.SKN_*` (skin) | [`Wardogs_GameFeatures_Skins_v2.md`](../game-features/Wardogs_GameFeatures_Skins_v2.md) |

### `_mps`, `_kmh`, `_deg`, `_m` — unit suffixes

The game uses explicit unit suffixes on some vehicle stat fields:

- `_mps` → meters per second
- `_kmh` → kilometers per hour
- `_deg` → degrees
- `_m` → meters

Fields **without** a suffix (bare `Speed`, `Fuel`, `FuelEconomy`,
`MuzzleSpeed`, `DragArea`, `Mass`) are **not labelled** and should be
treated as relative values. See [`Wardogs_GameFeatures_Vehicles_v2.md`](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) and the project
[`UNITS reference`](gap_resolution/UNITS.md).

### `PostProcessEffect.DeathState.*` — Post-process GameplayTags

Referenced in [`Wardogs_GameFeatures_AlternativeCriticalCamera_v2.md`](../game-features/Wardogs_GameFeatures_AlternativeCriticalCamera_v2.md).
Tag family defined under:

- `data/Wardogs/Content/<...>/DT_AlternativeCriticalCamera.json` (empty in current export)
- Post-process tag catalog: see [`Wardogs_GameplayTags_v1.md`](../content/Wardogs_GameplayTags_v1.md)
  if indexed there; otherwise the live tag registry

### `AppliableActionData` / `ThrowActions` — Item action arrays

- Defined in [`Wardogs_Items_v2.md`](../content/Wardogs_Items_v2.md) — self-reference; partially decoded (required states, velocity curve references). Full decode is an EXPORT bucket item (not CROSS_REF).

### `Ural.Battle` / `DA_WHL_07_Stats` — Vehicle naming mapping

Resolved: `Ural.Battle` tag points at `DA_WHL_07_Stats` (not an
ArmouredBattle asset). Numbers identical across both references; this
is a legacy naming artifact, not a data divergence.

- Vehicle stats: [`Wardogs_AllVehicles_Stats_Damage_v1.md`](../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- Vehicle market loadout: [`Wardogs_GameFeatures_Vehicles_v2.md`](../game-features/Wardogs_GameFeatures_Vehicles_v2.md)

### `Vehiclesmith_Main_P` — Map asset

Map asset for the Vehiclesmith UI. Referenced in
[`Wardogs_GameFeatures_Vehiclesmith_v2.md`](../game-features/Wardogs_GameFeatures_Vehiclesmith_v2.md).
Live map file: `data/Wardogs/Plugins/GameFeatures/Vehiclesmith/Content/Maps/Vehiclesmith_Main_P.umap` — not JSON-exported (map files are binary).

## By doc

### [Wardogs_Animation_v2.md](../content/Wardogs_Animation_v2.md)
- `MirrorDataTable` → resolved: all null, confirmed not in dump

### [Wardogs_Destruction_v2.md](../content/Wardogs_Destruction_v2.md)
- `CP_*_C` → resolved: internals not exported (Blueprint bytecode)

### [Wardogs_GameFeatures_AlternativeCriticalCamera_v2.md](../game-features/Wardogs_GameFeatures_AlternativeCriticalCamera_v2.md)
- `DT_AlternativeCriticalCamera` → file exists, empty row (confirmed in-plugin)
- `PostProcessEffect.DeathState.Killcam` → GameplayTag, see tag catalog

### [Wardogs_GameFeatures_FactoryInvestment_01_v2.md](../game-features/Wardogs_GameFeatures_FactoryInvestment_01_v2.md)
- Display name + map icon → localised string + texture asset (binary, not JSON)

### [Wardogs_GameFeatures_Gunsmith_v2.md](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md)
- `T_Reticle_*`, `W_*`, `DL_*` → textures/widgets/data layers, binary
- `Id.Item.OPT_08` → [`Wardogs_Items_v2.md`](../content/Wardogs_Items_v2.md) optics section
- `DT_GunsmithPopupOptions` → self-reference, defined in this doc's Season 02 update

### [Wardogs_GameFeatures_Parachutes_v2.md](../game-features/Wardogs_GameFeatures_Parachutes_v2.md)
- `CRV_ParachutePunishment_Damage` → data file in GameMechanics tree
- `ID_Backpack_Audio`, `ID_Vest_Audio` → [`Wardogs_Audio_v2.md`](../content/Wardogs_Audio_v2.md)

### [Wardogs_GameFeatures_UnderbarrelGrenadeLauncher_v2.md](../game-features/Wardogs_GameFeatures_UnderbarrelGrenadeLauncher_v2.md)
- `CT_Weapon_Spread` → [`Wardogs_Items_v2.md`](../content/Wardogs_Items_v2.md) weapon curves section
- `TestGrenadeLauncher` → test-only asset, naming matches test-build convention

### [Wardogs_GameFeatures_Vehicles_v2.md](../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- `_mps`, `_kmh`, `_deg` suffixes → units reference above
- `Ural.Battle` / `DA_WHL_07_Stats` → [`Wardogs_AllVehicles_Stats_Damage_v1.md`](../content/Wardogs_AllVehicles_Stats_Damage_v1.md)

### [Wardogs_GameFeatures_Vehiclesmith_v2.md](../game-features/Wardogs_GameFeatures_Vehiclesmith_v2.md)
- Vehicle stats → [`Wardogs_AllVehicles_Stats_Damage_v1.md`](../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- `DL_Vehiclesmith_*`, `Vehiclesmith_Main_P` → binary assets, not JSON-exported

### [Wardogs_Items_v2.md](../content/Wardogs_Items_v2.md)
- `AppliableActionData` / `ThrowActions` → partially decoded; full decode is EXPORT bucket work

### [Wardogs_Maps_v2.md](../content/Wardogs_Maps_v2.md)
- Materials / vertex factories → binary assets (no dedicated doc)

### [Wardogs_VFX_v2.md](../content/Wardogs_VFX_v2.md)
- `B_CameraShake_*` → referenced only; Blueprint internals not exported
- `NS_*` Niagara systems → not JSON-exported (compiled graph format)

## Takeaway

Many "CROSS_REF" gaps are actually **"this is binary"** or
**"this is a Blueprint bytecode"** gaps — not resolvable without
either (a) FModel visual inspection (not scheduled), (b) IDA RE of the
compiled consumer, or (c) a GameplayTag catalog pass.

Resolvable-by-cross-link: the ones involving data assets and
cooked DataTables, which this index now resolves.

Non-resolvable from current pipeline:
- Niagara system internals (compiled graphs)
- Blueprint bytecode (not in Dumper-7 output)
- Binary textures / meshes / maps (umap/uasset binary)
- Widget visual trees (binary)
- Data layers (world-partition constructs)

For the non-resolvable, the honest resolution is "add a note in the
referring doc stating `<Thing> is binary, not covered by this project's
JSON-parse pipeline`" — which converts the gap from "where is this
defined" to "this isn't documentable from cooked data."
