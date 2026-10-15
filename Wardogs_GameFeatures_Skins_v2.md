# Wardogs: GameFeatures Skins Reference (v2)
*Source: exported JSON under `Wardogs/Plugins/GameFeatures/Skins` (13 files, 4 folders). Numbers and tags are read from the export. Meanings of fields that are not named in the export are marked as unconfirmed.*

---

## 1. Layout

| Folder | Files | Contents |
|---|---|---|
| FactionLogo_SkinsData | 5 | 1 cosmetic table (3 rows), 3 `WDSkinDataAsset`, 1 registry source |
| Season01_SkinsData | 5 | 1 cosmetic table (17 rows), 3 `WDSkinDataAsset`, 1 registry source |
| Season01_SkinsAssets | 1 | `GameFeatureData` shell, no properties exported |
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

Faction logos: each of the three `FactionLogo` rows points at a `Skin_Supporter_*` asset, and each of those assets has one `CPD_Overrides` entry for the same item (section 3).

---

## 3. Skin Data Assets

Each `WDSkinDataAsset` holds one `Skin` struct with four fields: `Pattern_ID_Mask` (pattern texture), `PossibleLUTs` (colour lookup textures), `DefaultCPD` (a parameter block with UV placement, wear threshold and feather, and mastery colour), and `CPD_Overrides` (per-item overrides of the same parameter block, keyed by item tag). The name `CPD` is not expanded in the export; the reading here is a guess.

| Asset | Folder | Pattern mask | LUT(s) | Overrides | Override target tags |
|---|---|---|---|---|---|
| Skin_Supporter_Lonestar | FactionLogo_SkinsData | T_Pattern_Lonestar | T_LUT_Lonestar | 1 | WEPN_033 |
| Skin_Supporter_Manticore | FactionLogo_SkinsData | T_Pattern_Manticore | T_LUT_Manticore | 1 | KH2002 |
| Skin_Supporter_Valkyra | FactionLogo_SkinsData | T_Pattern_Valkyra | T_LUT_Valkyra | 1 | A91 |
| Skin_BlackAndGold | Season01_SkinsData | T_Pattern_Solid_001 | T_LUT_Gold_001 | 1 | RPG7 |
| Skin_DigitalWood | Season01_SkinsData | T_Pattern_Digital_002 | T_LUT_Green_001 | 43 | Glock17, CGM4, Parachute.Sport, M4, KH2002, A91, AK74M, RFB, M249, WEPN_027, M500, SR_04, WEPN_033, WEPN_029, WEPN_030, MMGL, Vector, WEPN_026, SKS, SMG_03, Judge, LMG_02, MK22, WEPN_028, Vehicle.Variant.Land.Wheeled.Bobcat.Default, Vehicle.Variant.Land.Wheeled.DuneBuggy.Default, Vehicle.Variant.Land.Wheeled.Kodiak.Pickup, Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun, Vehicle.Variant.Land.Wheeled.Humvee.Default, Vehicle.Variant.Land.Wheeled.Humvee.MachineGun, Vehicle.Variant.Land.Wheeled.Ural.Default, Vehicle.Variant.Land.Wheeled.Ural.Battle, Vehicle.Variant.Land.Wheeled.Ural.Attack, Vehicle.Variant.Land.Tracked.TNK_01.Heavy, Vehicle.Variant.Land.Tracked.TNK_01.AntiAir, Vehicle.Variant.Land.Tracked.TNK_01.Artillery, SVDM, SV98, RPG7, CombatBow, TAR21, Mosin, Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| Skin_TwoTone_Desert | Season01_SkinsData | T_Pattern_Solid_001 | T_LUT_Desert_002 | 3 | M4, Judge, Mosin |

Override targets for `Skin_DigitalWood` cover 43 items, the largest set. The other five assets override 1 to 3 items each. Each override sets its own `DisplaySkin`, `WearThreshold`, `DisplayMastery` and `MasteryColour`, so one skin can look different on each item.

---

## 4. Wiring

| Feature file | Action | Effect |
|---|---|---|
| FactionLogo_SkinsData | DataRegistrySource | Adds `DT_Cosmetics_FactionLogo` to registry `CosmeticData` (priority 0, client and server) |
| Season01_SkinsData | DataRegistrySource | Adds `DT_Cosmetics_Season01_Skins` to registry `CosmeticData` (priority 0, client and server) |
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
- **Component class** `WDActorSkinComponent` and the `SkinsInSession` runtime are only named here, not decoded.

