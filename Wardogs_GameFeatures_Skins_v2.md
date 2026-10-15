---
title: "Skins (feature)"
parent: "Game Features"
---

# Wardogs: GameFeatures Skins Reference (v2)
*Source: exported JSON under [`Wardogs/Plugins/GameFeatures/Skins`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Skins) (16 files, 5 folders). Numbers and tags are read from the export. Meanings of fields that are not named in the export are marked as unconfirmed.*

---

## Season 02 update (2026-10-15)

- **New skin asset:** [`Skin_ChocolateChip`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/Skin_ChocolateChip.json) (in [`Season01_SkinsData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Season01_SkinsData.json)), pattern `T_Pattern_ChocolateChip`, LUT `T_LUT_Brown_001`, with 56 overrides, the largest set.
- **New folder [`Season02_SkinsData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season02_SkinsData/Content/Season02_SkinsData.json):** cosmetic table [`DT_Cosmetics_Season02_Skins`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season02_SkinsData/Content/Data/DT_Cosmetics_Season02_Skins.json) with 8 rows (3 of them ChocolateChip), registered to `CosmeticData` through the new feature file.
- **[`Skin_DigitalWood`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/Skin_DigitalWood.json):** overrides 43 → 46 (added [`WEPN_034`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/WEPN_034.json), `Vehicle.Variant.Air.Rotary.Havoc.Default` and `Vehicle.Variant.Air.Rotary.Littlebird`). `WearThreshold` on 10 existing overrides 0.8 → 1.0.
- **[`Skin_TwoTone_Desert`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/Skin_TwoTone_Desert.json):** overrides 3 → 8 (added [`WEPN_036`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_036/Content/WEPN_036.json), `KH2002`, [`WEPN_033`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_033/Content/WEPN_033.json), [`WEPN_034`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/WEPN_034.json) and `Vehicle.Variant.Air.Rotary.Havoc.Default`).
- **[`Skin_BlackAndGold`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/Skin_BlackAndGold.json):** overrides 1 → 3 (added [`WEPN_033`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_033/Content/WEPN_033.json) and `Vehicle.Variant.Air.Rotary.Havoc.Default`). Default accent UV Y 1.35187 → 0.1.
- No skin assets or cosmetic rows were removed.

---

## 1. Layout

| Folder | Files | Contents |
|---|---|---|
| FactionLogo_SkinsData | 5 | 1 cosmetic table (3 rows), 3 `WDSkinDataAsset`, 1 registry source |
| Season01_SkinsData | 6 | 1 cosmetic table (17 rows), 4 `WDSkinDataAsset`, 1 registry source |
| Season01_SkinsAssets | 1 | `GameFeatureData` shell, no properties exported |
| Season02_SkinsData | 2 | 1 cosmetic table (8 rows), 1 registry source |
| SkinsInSession | 2 | `SkinDisplayBadgeData` and a component-add action |

---

## 2. Cosmetic Rows

Each `WDCosmeticData` row links a cosmetic tag to the item or vehicle it applies to (`EntityID`) and to a skin asset (`SkinDefinition`). Table tags are shown without the `Meta.Cosmetic.` prefix.

| Table | Row | Applies to (EntityID) | Archetype | Skin asset |
|---|---|---|---|---|
| FactionLogo | FactionLogo.WEPN_033 | Id.Item.WEPN_033 | Item.Archetype.AR | Skin_Supporter_Lonestar |
| FactionLogo | FactionLogo.KH2002 | Id.Item.KH2002 | Item.Archetype.AR | Skin_Supporter_Manticore |
| FactionLogo | FactionLogo.A91 | Id.Item.A91 | Item.Archetype.AR | Skin_Supporter_Valkyra |
| Season01_Skins | BlackAndGold.AK74 | Id.Item.AK74M | Item.Archetype.AR | Skin_BlackAndGold |
| Season01_Skins | DigitalWood.GGX17 | Id.Item.Glock17 | Item.Archetype.Pistol | Skin_DigitalWood |
| Season01_Skins | DigitalWood.SportsParachute | Id.Item.Parachute.Sport | Item.Archetype.Parachute | Skin_DigitalWood |
| Season01_Skins | DigitalWood.SV98 | Id.Item.SV98 | Item.Archetype.Sniper | Skin_DigitalWood |
| Season01_Skins | DigitalWood.M4 | Id.Item.M4 | Item.Archetype.AR | Skin_DigitalWood |
| Season01_Skins | TwoToneDesert.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.Default | Vehicle.Archetype.Land.Wheeled | Skin_TwoTone_Desert |
| Season01_Skins | TwoToneDesert.Bobcat | Vehicle.Variant.Land.Wheeled.Bobcat.Default | Vehicle.Archetype.Land.Wheeled | Skin_TwoTone_Desert |
| Season01_Skins | TwoToneDesert.Littlebird | Vehicle.Variant.Air.Rotary.Littlebird.Default | Vehicle.Archetype.Air.Rotary | Skin_TwoTone_Desert |
| Season01_Skins | TwoToneDesert.DuneBuggy | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default | Vehicle.Archetype.Land.Wheeled | Skin_TwoTone_Desert |
| Season01_Skins | TwoToneDesert.A91 | Id.Item.A91 | Item.Archetype.AR | Skin_TwoTone_Desert |
| Season01_Skins | TwoToneDesert.Bushmaster | Id.Item.WEPN_033 | Item.Archetype.AR | Skin_TwoTone_Desert |
| Season01_Skins | TwoToneDesert.KH2002 | Id.Item.KH2002 | Item.Archetype.AR | Skin_TwoTone_Desert |
| Season01_Skins | TwoToneDesert.M4 | Id.Item.M4 | Item.Archetype.AR | Skin_TwoTone_Desert |
| Season01_Skins | TwoToneDesert.M249 | Id.Item.M249 | Item.Archetype.LMG | Skin_TwoTone_Desert |
| Season01_Skins | TwoToneDesert.AX50 | Id.Item.SR_04 | Item.Archetype.Sniper | Skin_TwoTone_Desert |
| Season01_Skins | TwoToneDesert.MP9 | Id.Item.MP9 | Item.Archetype.SMG | Skin_TwoTone_Desert |
| Season01_Skins | TwoToneDesert.M500 | Id.Item.M500 | Item.Archetype.Shotgun | Skin_TwoTone_Desert |
| Season02_Skins | BlackAndGold.Littlebird | Vehicle.Variant.Air.Rotary.Littlebird.Default | Vehicle.Archetype.Air.Rotary | Skin_BlackAndGold |
| Season02_Skins | TwoToneDesert.Mosin | Id.Item.Mosin | Item.Archetype.Sniper | Skin_TwoTone_Desert |
| Season02_Skins | TwoToneDesert.Galil | Id.Item.WEPN_029 | Item.Archetype.AR | Skin_TwoTone_Desert |
| Season02_Skins | TwoToneDesert.Havoc | Vehicle.Variant.Air.Rotary.Havoc.Default | Vehicle.Archetype.Air.Rotary | Skin_TwoTone_Desert |
| Season02_Skins | DigitalWood.M500 | Id.Item.M500 | Item.Archetype.Shotgun | Skin_DigitalWood |
| Season02_Skins | ChocolateChip.M14 | Id.Item.WEPN_034 | Item.Archetype.DMR | Skin_ChocolateChip |
| Season02_Skins | ChocolateChip.Evolys | Id.Item.WEPN_036 | Item.Archetype.LMG | Skin_ChocolateChip |
| Season02_Skins | ChocolateChip.TCXSPR | Id.Item.WEPN_037 | Item.Archetype.AR | Skin_ChocolateChip |

Faction logos: each of the three `FactionLogo` rows points at a `Skin_Supporter_*` asset, and each of those assets has one `CPD_Overrides` entry for the same item (section 3).

---

## 3. Skin Data Assets

Each `WDSkinDataAsset` holds one `Skin` struct with four fields: `Pattern_ID_Mask` (pattern texture), `PossibleLUTs` (colour lookup textures), `DefaultCPD` (a parameter block with UV placement, wear threshold and feather, and mastery colour), and `CPD_Overrides` (per-item overrides of the same parameter block, keyed by item tag). The name `CPD` is not expanded in the export; the reading here is a guess.

| Asset | Folder | Pattern mask | LUT(s) | Overrides | Override target tags |
|---|---|---|---|---|---|
| Skin_Supporter_Lonestar | FactionLogo_SkinsData | T_Pattern_Lonestar | T_LUT_Lonestar | 1 | WEPN_033 |
| Skin_Supporter_Manticore | FactionLogo_SkinsData | T_Pattern_Manticore | T_LUT_Manticore | 1 | KH2002 |
| Skin_Supporter_Valkyra | FactionLogo_SkinsData | T_Pattern_Valkyra | T_LUT_Valkyra | 1 | A91 |
| Skin_BlackAndGold | Season01_SkinsData | T_Pattern_Solid_001 | T_LUT_Gold_001 | 3 | RPG7, WEPN_033, Vehicle.Variant.Air.Rotary.Havoc.Default |
| Skin_DigitalWood | Season01_SkinsData | T_Pattern_Digital_002 | T_LUT_Green_001 | 46 | Glock17, CGM4, Parachute.Sport, M4, KH2002, A91, AK74M, RFB, M249, WEPN_027, M500, SR_04, WEPN_033, WEPN_029, WEPN_030, MMGL, Vector, WEPN_026, SKS, SMG_03, Judge, LMG_02, MK22, WEPN_028, Vehicle.Variant.Land.Wheeled.Bobcat.Default, Vehicle.Variant.Land.Wheeled.DuneBuggy.Default, Vehicle.Variant.Land.Wheeled.Kodiak.Pickup, Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun, Vehicle.Variant.Land.Wheeled.Humvee.Default, Vehicle.Variant.Land.Wheeled.Humvee.MachineGun, Vehicle.Variant.Land.Wheeled.Ural.Default, Vehicle.Variant.Land.Wheeled.Ural.Battle, Vehicle.Variant.Land.Wheeled.Ural.Attack, Vehicle.Variant.Land.Tracked.TNK_01.Heavy, Vehicle.Variant.Land.Tracked.TNK_01.AntiAir, Vehicle.Variant.Land.Tracked.TNK_01.Artillery, SVDM, SV98, RPG7, CombatBow, TAR21, Mosin, Vehicle.Variant.Land.Wheeled.Kodiak.Default, WEPN_034, Vehicle.Variant.Air.Rotary.Havoc.Default, Vehicle.Variant.Air.Rotary.Littlebird |
| Skin_TwoTone_Desert | Season01_SkinsData | T_Pattern_Solid_001 | T_LUT_Desert_002 | 8 | M4, Judge, Mosin, WEPN_036, KH2002, WEPN_033, WEPN_034, Vehicle.Variant.Air.Rotary.Havoc.Default |
| Skin_ChocolateChip | Season01_SkinsData | T_Pattern_ChocolateChip | T_LUT_Brown_001 | 56 | WEPN_037, WEPN_029, MMGL, Defibrillator, M67Grenade, Vehicle.Variant.Land.Wheeled.Ural.Default, Vehicle.Variant.Land.Wheeled.Ural.Battle, Vehicle.Variant.Land.Wheeled.Ural.Attack, Vehicle.Variant.Land.Wheeled.Bobcat.Default, WEPN_030, M4, AK74M, TAR21, A91, KH2002, CombatBow, SKS, SVDM, M249, LMG_02, Judge, Glock17, WEPN_032, WEPN_026, WEPN_027, M500, MP43, SMG_03, WEPN_028, SV98, MK22, SR_04, CGM4, RPG7, Launcher_04, WEPN_036, Mosin, Vehicle.Variant.Land.Wheeled.Humvee.MachineGun, Vehicle.Variant.Land.Wheeled.DuneBuggy, Vehicle.Variant.Air.Rotary.ROT_01.Default, Vehicle.Variant.Land.Wheeled.Humvee.Minigun, Vehicle.Variant.Land.Wheeled.Kodiak.Default, Vehicle.Variant.Land.Tracked.TNK_01.Artillery, Vehicle.Variant.Land.Tracked.TNK_01.AntiAir, Vehicle.Variant.Land.Wheeled.Kodiak.Pickup, Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun, Vehicle.Variant.Land.Tracked.TNK_01.Heavy, Vehicle.Variant.Air.Rotary.Littlebird.Default, Vehicle.Variant.Land.Wheeled.DuneBuggy.Default, Vehicle.Variant.Land.Wheeled.Humvee.Default, WEPN_033, MP9, RFB, Vector, WEPN_034, Vehicle.Variant.Air.Rotary.ROT_02 |

Override targets for [`Skin_ChocolateChip`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/Skin_ChocolateChip.json) cover 56 items, the largest set. [`Skin_DigitalWood`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/Skin_DigitalWood.json) covers 46. The other five assets override 1 to 8 items each. Each override sets its own `DisplaySkin`, `WearThreshold`, `DisplayMastery` and `MasteryColour`, so one skin can look different on each item.

---

## 4. Wiring

| Feature file | Action | Effect |
|---|---|---|
| FactionLogo_SkinsData | DataRegistrySource | Adds [`DT_Cosmetics_FactionLogo`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/FactionLogo_SkinsData/Content/Data/DT_Cosmetics_FactionLogo.json) to registry `CosmeticData` (priority 0, client and server) |
| Season01_SkinsData | DataRegistrySource | Adds [`DT_Cosmetics_Season01_Skins`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/DT_Cosmetics_Season01_Skins.json) to registry `CosmeticData` (priority 0, client and server) |
| Season02_SkinsData | DataRegistrySource | Adds [`DT_Cosmetics_Season02_Skins`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season02_SkinsData/Content/Data/DT_Cosmetics_Season02_Skins.json) to registry `CosmeticData` (priority 0, client and server) |
| Season01_SkinsAssets | GameFeatureData | No properties exported; its role is not confirmed |
| SkinsInSession | AddComponents | Adds `WDActorSkinComponent` to `BHItem`, `BHBaseVehiclePawn`, `WDDroppedItem` (client and server, one entry per actor class) |
| SkinsInSession | SkinDisplayBadgeData | Preview material: `MM_SkinsPreview` |

---

## 5. How the Values Combine

- Equipping a cosmetic: the row's `EntityID` gives the item; the row's `SkinDefinition` gives the skin asset.
- Applying the skin to a specific item: the `DefaultCPD` block applies, and a matching `CPD_Overrides` entry for that item replaces the fields it sets.
- Cosmetic rows are read through the `CosmeticData` registry, which the two DataRegistrySource actions add to.

---

## 6. Still Not Pulled / Limitations

- **Prices, unlock conditions and rarity** for cosmetics are not in this folder.
- **Texture and material contents** (what `T_Pattern_*`, `T_LUT_*` and `MM_SkinsPreview` look like) are not decoded.
- **`CPD` field meanings.** The UV, wear and mastery field names are as exported. Their effect on rendering is not confirmed.
- **Component class** `WDActorSkinComponent` and the [`SkinsInSession`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/SkinsInSession/Content/SkinsInSession.json) runtime are only named here, not decoded.

