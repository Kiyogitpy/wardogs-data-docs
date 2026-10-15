---
title: "UnderbarrelGrenadeLauncher (feature)"
parent: "Game Features"
---

# Wardogs — UnderbarrelGrenadeLauncher Game Feature Reference (v2)
*Extracted from cooked game data ([`Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher), 4 JSON files, all parsed). Build `++Wardogs+Live-CL-516586`, UE 5.7.*

> **Naming flag:** the launcher item is **`Id.Item.TestGrenadeLauncher`**, with display name **"TEST Grenade Launcher"**. It reads as a test or placeholder build, not a shipping item. The stats below are exported as-is, but the name and the magazine-audio reference suggest the item has not been finished.

---

## 1. Plugin Inventory

| Asset | Type | Role |
|---|---|---|
| [`Content/UnderbarrelGrenadeLauncher`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/UnderbarrelGrenadeLauncher.json) | `GameFeatureData` | Plugin root. Scans `/UnderbarrelGrenadeLauncher/Data` for `BH.Item` assets |
| [`Content/Data/GrenadeLauncher`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/GrenadeLauncher.json) | `BHInventoryItemDefinition` (7 exports) | The attachment item (`Id.Item.TestGrenadeLauncher`) |
| [`Content/Data/DA_GrenadeLauncher_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/DA_GrenadeLauncher_Stats.json) | `WDWeaponStatsData` | Firing, recoil and ballistic stats |
| [`Content/Data/DA_GrenadeLauncher_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/DA_GrenadeLauncher_Audio.json) | `WDAudioData` | Audio data asset. **Exported with no properties** |

---

## 2. Attachment Item ([`GrenadeLauncher`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/GrenadeLauncher.json))

| Field | Value |
|---|---|
| `ItemId` | `Id.Item.TestGrenadeLauncher` |
| `DisplayName` | "TEST Grenade Launcher" |
| `ItemContext` | `Item.Attachment.Underbarrel` |

### Fragments (6)

| Fragment | Purpose |
|---|---|
| `BHInventoryFragment_UserInterface` | UI hook (no properties) |
| `WDInventoryFragment_Attachment` | Weapon stats, ammo requirement, animations (section 3) |
| `WDInventoryFragment_Gunsmith` | `ItemType` = `EWDGunsmithItemType::Attachment` |
| `BHInventoryFragment_SubSlotSupport` | Ammo container (section 4) |
| `WDItemsmithDataFragment_CameraData` | Gunsmith camera parameters (section 5) |
| `WDInventoryFragment_Audio` | Audio asset [`ID_Magazine_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Magazine_Audio.json) (see note in section 6) |

---

## 3. Attachment Fragment: Weapon Setup

### 3a. Ammo requirement

| Field | Value |
|---|---|
| Required resource | `Id.Item.40mm` |
| Resources used | **1** per use |
| Resource type | `Item.Resource.AncillaryAmmo` |
| Limit search to item | true |
| Optional required sub-slot category | `None` |

### 3b. Reload animation

| Field | Value |
|---|---|
| First-person player montage | `AM_FP_UniTool_Reload` |
| Third-person player montage | `AM_TP_UniTool_Reload` |
| Override length | false (length 1.0 if used) |
| Item blend-out time | 0.1 s |
| Player blend-out time | 0.1 s |

Both montages come from the **Universal Tool** animation set, not a grenade-launcher-specific one.

### 3c. Firing animation
All four firing montage slots are `null`. Firing relies on the weapon's own animation.

### 3d. Spread
`SpreadValues` is keyed by stance and uses curve table [`CT_Weapon_Spread`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Curves/CT_Weapon_Spread.json). The `Stand` entry has value 1.0.

### 3e. Weapon stats reference
Stats come from `WDWeaponStatsData` [`DA_GrenadeLauncher_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/DA_GrenadeLauncher_Stats.json) (section 6), and audio from [`DA_GrenadeLauncher_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/DA_GrenadeLauncher_Audio.json).

---

## 4. Ammo Container (`BHInventoryFragment_SubSlotSupport`)

| Field | Value |
|---|---|
| Container identifier | `Item.Ammo` |
| Support filter | `EBHSupportFilterMethod::BlockList` (allow and block lists both empty) |
| Size type | `EBHContainerType::Item` |
| Grid size | 1 x 1 |
| List size | -2 (exported value) |
| Max slot stack size | **1** |
| Stacked packing | false |
| Hidden container | false |
| Default items | `Id.Item.40mm` (default amount null) |

Effect: the launcher holds one 40mm round in a single-slot container, with no stacking.

---

## 5. Gunsmith Camera (`WDItemsmithDataFragment_CameraData`)

Keyed on `Item.Attachment.Underbarrel`:

| Field | Value |
|---|---|
| Focus position offset | (0, 15, -5.20) |
| Focus position | (0, 0, 0) |
| Default angle (pitch, yaw, roll) | (0, 180, 0) |
| Center angle | (0, 180, 0) |
| Angle offset limit | 75 |
| Desired distance | 60 |
| Distance limits (min, max) | 10 to 200 |
| Camera speed | 1.0 |
| Zoom speed | 40 |
| Flair pan limit min / max | (-100, -50) / (100, 50) |
| Item-select view offset | (0, 0) |

---

## 6. Weapon Stats ([`DA_GrenadeLauncher_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/DA_GrenadeLauncher_Stats.json))

| Stat | Value | Notes |
|---|---|---|
| Rounds per minute | **75** | |
| Supported fire modes | `EWDFireMode::SemiAutomatic` | Only mode listed |
| Rounds per burst | 1 | |
| First focal plane | false | |
| Spawn projectile from camera when ADS | false | |
| Supported caliber | `Item.Caliber.40mm` | |
| Initial bullet speed | **7,600** | Unit not stated |
| Effective range | **300** | Unit not stated |

### Recoil curves
Both `ViewKickCurve` and `RecoveryKickCurve` are two-key linear-to-cubic ramps:

| Curve | Key 0 (time, value) | Key 1 (time, value) | Interp |
|---|---|---|---|
| View kick | (0, 0) | (1, 1) | Cubic, auto tangents |
| Recovery kick | (0, 0) | (1, 1) | Cubic, auto tangents |

Both are normalised 0-to-1 ramps (time 0 to 1, value 0 to 1). The export does not show what scales them.

### Audio
[`DA_GrenadeLauncher_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/DA_GrenadeLauncher_Audio.json) (`WDAudioData`) is exported with **no properties**. The launcher's sound therefore comes from the defaults or from whatever references it. The item's `WDInventoryFragment_Audio` points at [`ID_Magazine_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Magazine_Audio.json), a magazine asset, which suggests the item reuses magazine audio.

---

## 7. Plugin Root ([`UnderbarrelGrenadeLauncher`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/UnderbarrelGrenadeLauncher.json))

| Field | Value |
|---|---|
| Primary asset type | `BH.Item` |
| Base class | `BHInventoryItemDefinition` |
| Directory scanned | `/UnderbarrelGrenadeLauncher/Data` |
| Specific assets | none |
| Apply recursively | true |
| Priority | -1 |
| Cook rule | `AlwaysCook` |

---

## 8. How Values Combine

- **Ammo:** each shot uses 1 round of `Id.Item.40mm` (`ResourcesUsed` = 1). The container holds 1 round at a time (`MaxSlotAmountStackSize` = 1), so the launcher is effectively a single-shot magazine.
- **Fire rate:** 75 RPM is about **0.8 s** between shots (60 / 75). Semi-automatic means one shot per trigger pull.
- **Ballistics:** a 7,600 initial speed over an effective range of 300. Units are not stated, so the range-to-speed relation cannot be checked from this folder.
- **Damage:** no damage value is in this plugin. Damage is presumably on the 40mm projectile, which is outside this dump.

---

## 9. Still Not Pulled / Limitations

- **Damage and splash.** The 40mm round's damage and explosion data are not in this plugin.
- **Unit for bullet speed and effective range** is not stated.
- **[`CT_Weapon_Spread`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Curves/CT_Weapon_Spread.json) values** are referenced by name only. The curve table is outside this plugin.
- **Reload and firing montages** are referenced by path. Their timing is not in this dump.
- **[`DA_GrenadeLauncher_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/DA_GrenadeLauncher_Audio.json) is empty** in the export. Whether that is intentional or a missing asset needs checking.
- **Test naming:** whether `TestGrenadeLauncher` is shipped or only a test build cannot be confirmed from the dump. The name and magazine-audio reference are the evidence.
