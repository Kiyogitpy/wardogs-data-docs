---
title: "Weapon Mastery"
parent: "Progression & Economy"
group: "Roles and mastery"
description: "The mastery screen's lists: 8 weapon types with 25 weapons, and 2 vehicle types with 8 vehicles. The data has no XP, level or reward table for either, so how progress is earned is not in the game data."
---

# Weapon Mastery

| Weapon Mastery | |
|---|---|
| **General** | |
| Kind | Mastery track for each weapon type and vehicle type |
| Weapon types | 8, with 25 weapons on the screen |
| Vehicle types | 2, with 8 vehicles on the screen |
| XP per level | Not in the client data |
| Rewards per level | Not in the client data |
| **Rewards** | |
| Season 1 skins | 17 in total: 12 weapon skins (on 11 weapons, the M4 has two), 4 vehicle skins and 1 parachute skin |
| Internal name | DA_UI_PlatformMastery_SceneData |
{: .wiki-infobox }

Weapon mastery is the mastery track for each type of weapon. The game data calls it platform mastery. The mastery screen has two halves: Weapon Mastery, for eight weapon types, and Vehicle Mastery, for two vehicle types. The data gives the lists that the screen shows. It holds no XP, level or reward table for any of them, so how progress is earned and what each level gives is not in the game data.

## Overview

Each weapon type and vehicle type has its own mastery progress. The mastery screen shows an "All" view and one view for each type.

## How it works

- **Per type.** Progress is kept for each type, not for each weapon or vehicle. The screen lists which weapons and vehicles belong to each type.
- **Two tabs.** The platform mastery screen has a Progression tab and a Challenges tab.
- **XP.** The data gives no XP for any weapon or vehicle. No item in this build has a platform XP tag set (it is empty on all 628 item rows), so the data does not say how mastery XP is earned.
- **Separate from role mastery.** Role mastery is a different track for the six roles, with its own XP curve. See [Cash and Rewards](cash-and-rewards.md#role-mastery-xp).

## Weapon types

The lists below are the weapons on the mastery screen, as the screen groups them. Each name links to its wiki article.

| Weapon type | Weapons on the screen |
|---|---|
| Assault Rifle (5) | [AK74](../weapons/ak74.md), [M4](../weapons/m4.md), [KH-2002](../weapons/kh-2002.md), [T-21](../weapons/t-21.md), [A-91](../weapons/a-91.md) |
| Light Machine Gun (2) | [PKM](../weapons/pkm.md), [M249 SAW](../weapons/m249-saw.md) |
| Marksman Rifle (3) | [BMR-308](../weapons/bmr-308.md), [SKS](../weapons/sks.md), [SVD](../weapons/svd.md) |
| Shotgun (2) | [MP43](../weapons/mp43.md), [M500](../weapons/m500.md) |
| Submachine Gun (3) | [AMP-9](../weapons/amp-9.md), [Super-45](../weapons/super-45.md), [PP-19 Vityaz](../weapons/pp-19-vityaz.md) |
| Sniper Rifle (4) | [MK22](../weapons/mk22.md), [SV98](../weapons/sv98.md), [Mosin Nagant](../weapons/mosin-nagant.md), [AMR 50](../weapons/amr-50.md) |
| Pistol (2) | [GGX 17](../weapons/ggx-17.md), [Judge](../weapons/judge.md) |
| Launcher (4) | [RPG-7](../weapons/rpg-7.md), [MAAWS](../weapons/maaws.md), [9K333 Verba](../weapons/9k333-verba.md), [MGL-40](../weapons/mgl-40.md) |

These lists differ from the weapon classes used elsewhere on this wiki. The Galil, FAL, Bushmaster M17S, Evo-3 Ultra, TCX-SPR, MP5, GGX 18, Deagle and M1911 are not on the mastery screen, although some of them have skins. The mapping is by item ID.

## Vehicle types

| Vehicle type | Vehicles on the screen |
|---|---|
| Land Vehicle (5) | [SPH-2](../vehicles/sph-2.md) (artillery), [L2A6](../vehicles/l2a6.md) (heavy tank), [Kodiak](../vehicles/kodiak.md), [Bobcat](../vehicles/bobcat.md), Lonestar spawn vehicle |
| Air Vehicle (3) | [Havoc](../vehicles/havoc.md), [MH-6](../vehicles/mh-6.md) (Little Bird), and a third helicopter that has no wiki article yet |

The Season 1 skin table names three weapons differently from this wiki. Its AX50 row is the AMR 50, its MP9 row is the AMP-9, and its Glock 17 row is the GGX 17. The mapping here is by item ID.

## Rewards

### Skins

The Season 1 cosmetic data lists skins for weapons, vehicles and a parachute, in three sets: Black and Gold, Digital Wood and Two-Tone Desert.

| Item | Type | Skin set |
|---|---|---|
| AK74 | Assault Rifle | Black and Gold |
| M4 | Assault Rifle | Digital Wood and Two-Tone Desert |
| A-91 | Assault Rifle | Two-Tone Desert |
| Bushmaster M17S | Assault Rifle | Two-Tone Desert |
| KH-2002 | Assault Rifle | Two-Tone Desert |
| M249 SAW | Light Machine Gun | Two-Tone Desert |
| M500 | Shotgun | Two-Tone Desert |
| AMP-9 | Submachine Gun | Two-Tone Desert |
| AMR 50 | Sniper Rifle | Two-Tone Desert |
| SV98 | Sniper Rifle | Digital Wood |
| GGX 17 | Pistol | Digital Wood |
| Humvee, Bobcat, Littlebird and Dune Buggy | Vehicles | Two-Tone Desert |
| Sports parachute | Parachute | Digital Wood |

The data does not say how a skin is granted. The Season 1 skins are sold on the Gold Market, and the backend can grant items outside the shop (see [Cosmetics](cosmetics.md)). No mastery level is linked to a skin in the data. No skin is listed for the Marksman Rifle or Launcher types.

### Parts

The data has a mastery paint title and a mastery texture slot for paints, but it lists no mastery paint names and no weapon paint list. Which attachments or parts a weapon type unlocks is not in the data.

### XP and rewards per level

Not in the client data. The mastery data holds screen text, colours and icon settings. It has no XP figures and no reward for any level, and the backend has no platform mastery content type. The level and XP thresholds that would gate the track do not appear in the client.

## Season 2 changes

The Season 02 update changed the text strings for the reward track and its panel. The values did not change, and the sources list no change to weapon mastery rewards.

## See also

- [Cosmetics](cosmetics.md)
- [Cash and Rewards](cash-and-rewards.md)
- [Challenges](challenges.md)

## Sources

- [Reward track and platform mastery data](../../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md)
- [Season 1 cosmetic and item unlocks](../../content/Wardogs_Season01_CosmeticUnlocks_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Platform mastery screen data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Mastery/Platforms/Data/DA_UI_PlatformMastery_SceneData.json) (JSON)
- [Season 1 skin table](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/DT_Cosmetics_Season01_Skins.json) (JSON)
- [Mastery paint select data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Flair/PaintSelect/Data/Mastery/DA_Itemsmith_MasteryPaintSelect.json) (JSON)
- [Economy data: platform mastery](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json) (JSON)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
