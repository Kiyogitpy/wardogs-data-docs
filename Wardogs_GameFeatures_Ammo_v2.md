---
title: "Ammo (feature)"
parent: "Game Features"
---

# Wardogs — GameFeature: Ammo Reference (v2)
*Extracted from cooked game data via CUE4Parse (build `++Wardogs+Live-CL-509546`, UE 5.7.4). Source: [`Wardogs/Plugins/GameFeatures/Ammo/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Ammo) (23 JSON files). Scripted pass over every file, then checked the one real export type in full.*

> **Key finding:** this folder does **not** define ammo. It holds 23 GameFeature bundles, and each one does a single thing: it adds one **External Data Layer** (a world-partition streaming layer) to the world. No damage, count, magazine, or per-round values are stored here. Those values are elsewhere (section 5).

---

## 1. Package Contents

Every file has the same structure. Nothing differs between them except the names.

| Export | Count | Role |
|---|---|---|
| `GameFeatureData` (one per file) | 23 | Bundle root. One action in each. |
| `GameFeatureAction_AddWorldPartitionContent` | 23 | Adds one `ExternalDataLayerAsset` to the world. |

Each bundle's `Actions[0]` points at its own `GameFeatureAction_AddWorldPartitionContent_2`. That action's only property is `ExternalDataLayerAsset`.

---

## 2. Bundle-to-Layer Map

| Bundle | External Data Layer added |
|---|---|
| [`AMMO_001`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_001/Content/AMMO_001.json) | `EDL_AMMO_001` |
| [`AMMO_002`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_002/Content/AMMO_002.json) | `EDL_AMMO_002` |
| [`AMMO_003`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_003/Content/AMMO_003.json) | `EDL_AMMO_003` |
| [`AMMO_004`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_004/Content/AMMO_004.json) | `EDL_AMMO_004` |
| [`AMMO_005`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_005/Content/AMMO_005.json) | `EDL_AMMO_005` |
| [`AMMO_006`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_006/Content/AMMO_006.json) | `EDL_AMMO_006` |
| [`AMMO_007`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_007/Content/AMMO_007.json) | `EDL_AMMO_007` |
| [`AMMO_008`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_008/Content/AMMO_008.json) | `EDL_AMMO_008` |
| [`AMMO_009`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_009/Content/AMMO_009.json) | `EDL_AMMO_009` |
| [`AMMO_010`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_010/Content/AMMO_010.json) | `EDL_AMMO_010` |
| [`AMMO_011`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_011/Content/AMMO_011.json) | `EDL_AMMO_011` |
| [`AMMO_012`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_012/Content/AMMO_012.json) | `EDL_AMMO_012` |
| [`AMMO_013`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_013/Content/AMMO_013.json) | `EDL_AMMO_013` |
| [`AMMO_014`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_014/Content/AMMO_014.json) | `EDL_AMMO_014` |
| [`AMMO_015`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_015/Content/AMMO_015.json) | `EDL_AMMO_015` |
| [`AMMO_016`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_016/Content/AMMO_016.json) | `EDL_AMMO_016` |
| [`AMMO_017`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_017/Content/AMMO_017.json) | `EDL_AMMO_017` |
| [`AMMO_018`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_018/Content/AMMO_018.json) | `EDL_AMMO_018` |
| [`AMMO_019`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_019/Content/AMMO_019.json) | `EDL_AMMO_019` |
| [`AMMO_020`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_020/Content/AMMO_020.json) | `EDL_AMMO_020` |
| [`AMMO_021`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_021/Content/AMMO_021.json) | `EDL_AMMO_021` |
| [`AMMO_022`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_022/Content/AMMO_022.json) | `EDL_AMMO_022` |
| [`AMMO_GLOBAL`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_GLOBAL/Content/AMMO_GLOBAL.json) | `EDL_AMMO_GLOBAL` |

The bundles are numbered 001 to 022, plus a `GLOBAL` one. That numbering suggests 22 numbered groups plus a shared layer. Which content lives in each layer is not stored in these files.

---

## 3. What Each Bundle Does

When a GameFeature is activated, its action runs. For these bundles the action is "add world partition content", which loads the named External Data Layer into the level's streaming. Inferred from the action type: the content placed inside `EDL_AMMO_xxx` is brought in or out as the feature is enabled.

That is the only behaviour stored here. The layer's **contents** are not in this dump, so the actual ammo placed in each layer cannot be listed.

---

## 4. Relationship to the Other GameFeatures

A grep of the whole dump finds no other export that names an `AMMO_0xx` or [`AMMO_GLOBAL`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_GLOBAL/Content/AMMO_GLOBAL.json) bundle, so nothing else in the dump references them by name. They appear to be standalone world-streaming switches. Their link to gameplay would be through the External Data Layers, which are not in the dump.

---

## 5. Where the Actual Ammo Data Is

Ammo-related data assets exist elsewhere in the dump. Found in this pass:

| Location | Contents |
|---|---|
| [`Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers) | 5 data assets: [`DA_AmmoModifier_ArmorPiercing`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers/DA_AmmoModifier_ArmorPiercing.json), [`DA_AmmoModifier_ArmorPiercing_Tracer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers/DA_AmmoModifier_ArmorPiercing_Tracer.json), [`DA_AmmoModifier_HollowPoint`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers/DA_AmmoModifier_HollowPoint.json), [`DA_AmmoModifier_HollowPoint_Tracer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers/DA_AmmoModifier_HollowPoint_Tracer.json), [`DA_AmmoModifier_Tracer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers/DA_AmmoModifier_Tracer.json). |
| [`Wardogs/Content/Audio/Events/UI/Inventory/AE_UI_Inventory_ExtractAmmo`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/UI/Inventory/AE_UI_Inventory_ExtractAmmo.json) and related | Ammo audio, including [`AE_UI_Request_Ammo`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/UI/Request/AE_UI_Request_Ammo.json), [`AE_Comms_Request_Ammo`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Comms/AssistanceRequests/AE_Comms_Request_Ammo.json), [`ID_LooseAmmoBox_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_LooseAmmoBox_Audio.json) |

The `AmmoModifiers` assets are the most likely source of ammo *types* (armour-piercing, hollow-point, tracer). Their damage and behaviour values were not checked in this pass, since they sit outside the scope of this folder.

---

## 6. Limitations

- **No ammo values are in this folder.** There are no damage, count, capacity, or type numbers.
- **The EDL contents are not in the dump.** Which actors, pickups, or spawn points each layer contains cannot be listed from here.
- **The purpose of the numbered groups** (001 to 022) is not stated in the data. The numbering suggests separate zones or loot groups, but that is an inference.
- **[`AMMO_GLOBAL`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Ammo/AMMO_GLOBAL/Content/AMMO_GLOBAL.json)** is named like a shared layer. Its contents are not visible here.
- The `AmmoModifiers` data assets are identified by name only in this doc. Their contents were not decoded here; a dedicated pass over [`Content/GameMechanics/DamageSystem/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/DamageSystem) would be needed for ammo values.
