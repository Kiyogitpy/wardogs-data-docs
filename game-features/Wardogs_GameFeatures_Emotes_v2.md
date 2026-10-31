---
title: "Emotes"
redirect_from: ["/Wardogs_GameFeatures_Emotes_v2.html", "/Wardogs_GameFeatures_Emotes_v2"]
parent: "Rewards & Unlocks"
description: "The emote package: emote entities, cosmetic rows and how they are wired into the game."
---

# Wardogs: GameFeatures Emotes Reference
*Source: exported JSON under [`Wardogs/Plugins/GameFeatures/Emotes`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Emotes) (3 files, 1 folder: [`Season01_EmotesData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Emotes/Season01_EmotesData/Content/Season01_EmotesData.json)). This is the full emote data set in the dump. Numbers and tags are read from the export.*

---

## 1. Files

| File | Type | Contents |
|---|---|---|
| [`DT_Cosmetics_Season01_Emotes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Emotes/Season01_EmotesData/Content/Data/DT_Cosmetics_Season01_Emotes.json) | DataTable (`WDCosmeticData`) | 3 cosmetic rows |
| [`DT_EntityData_Ext_Emotes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Emotes/Season01_EmotesData/Content/Data/DT_EntityData_Ext_Emotes.json) | DataTable (`BHEntityData_UI`) | 6 entity rows with display names and icons |
| [`Season01_EmotesData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Emotes/Season01_EmotesData/Content/Season01_EmotesData.json) | GameFeatureAction_DataRegistrySource | Registers the entity table |

---

## 2. Emote Entities

Six `BHEntityData_UI` rows. The `Action tag` is the action name each emote uses. All six point at the same placeholder icon (`T_UI_WorkInProgress`), so no emote has final art assigned in this build.

| Row tag | Action tag | Display name | Icon asset |
|---|---|---|---|
| Id.Emote.Shh | Action.Emote.Shh | Shh | T_UI_WorkInProgress |
| Id.Emote.Rock | Action.Emote.Rock | Rock | T_UI_WorkInProgress |
| Id.Emote.Paper | Action.Emote.Paper | Paper | T_UI_WorkInProgress |
| Id.Emote.Scissors | Action.Emote.Scissors | Scissors | T_UI_WorkInProgress |
| Id.Emote.RockPaperScissors | Action.Emote.RockPaperScissors | Rock Paper Scissors | T_UI_WorkInProgress |
| Id.Emote.Middle_Finger | Action.Emote.Middle_Finger | Middle Finger | T_UI_WorkInProgress |

Entity rows `Rock`, `Paper` and `Scissors` exist as separate emotes. They are not cosmetic rows in this folder. The `RockPaperScissors` row is the combined emote; its link to the three single-hand rows is an inference, not confirmed.

---

## 3. Cosmetic Rows

Cosmetic rows are the purchasable or unlockable side. Three exist, one per emote that has a cosmetic entry. None of them has a `SkinDefinition`.

| Row | Entity (EntityId) | Category | Archetype |
|---|---|---|---|
| Emote.Shh | Id.Emote.Shh | Meta.Cosmetic.Emote | None |
| Emote.RockPaperScissors | Id.Emote.RockPaperScissors | Meta.Cosmetic.Emote | None |
| Emote.Middle_Finger | Id.Emote.Middle_Finger | Meta.Cosmetic.Emote | None |

The cosmetic rows cover `Shh`, `RockPaperScissors` and `Middle_Finger`. `Rock`, `Paper` and `Scissors` have no cosmetic row here.

---

## 4. Wiring

| Registry | Table added | Priority |
|---|---|---|
| EntityData_UI | DT_EntityData_Ext_Emotes | 0 |
| CosmeticData | DT_Cosmetics_Season01_Emotes | 0 |

The one registry source adds both tables: the entity table to `EntityData_UI` and the cosmetic table to `CosmeticData`, the same registry the Skins folder uses.

---

## 5. Still Not Pulled / Limitations

- **Animations, audio and VFX** for the emotes are not in this folder.
- **Prices and unlock rules** for emote cosmetics are not in this folder.
- **Emote trigger and playback logic** (what runs when an emote is used) is not decoded.

## Change log

| Date | Change |
|---|---|
| 2026-10-18 | `data/` re-exported with the v2 usmap (names only; values unchanged): the row key is spelled `EntityId`. |
