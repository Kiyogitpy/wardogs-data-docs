---
title: "Huey"
parent: "Vehicles"
group: "Helicopters"
description: "A helicopter that is in the game's reward, targeting and spawn rules but not in the vehicle vendor: a 1,200 cash destroy reward, a mounted machine gun variant and Little Bird seat protection, with no stats of its own."
---

# Huey

| Huey | |
|---|---|
| **General** | |
| Type | Helicopter |
| Variants | Default and a mounted machine gun version |
| Seats | Not stored |
| Mass | Not stored |
| **Durability** | |
| Main health | Not stored |
| Seat protection (Season 2) | 25% against small and medium arms, 15% against high-calibre arms |
| Destroy reward | 1,200 cash |
| **Availability** | |
| Price | Not sold (no shop listing) |
| Unlock level | Not applicable |
| Internal name | ROT_01 |
{: .wiki-infobox }

The Huey is a helicopter that the game's rules name in many places, but whose vehicle entries are missing. It has a destroy reward, a seat-protection rule, a spotting target, a place on the Talon 9K-SAM and MG Nest target lists, and a mention in one air yard on the Zestafona map. It has no shop listing, so a player cannot buy it, and no health, speed, seats or fuel is known for it. This article collects what the rules say about it and states plainly what they do not.

## Overview

The Huey is a helicopter family in the game. It has two variants in the rules: a default one and one with mounted machine guns. The rules for the variants are identical wherever they are listed, so nothing separates one from the other except the name.

The other helicopters in the vehicle vendor have their own entries with a health total, seats, price, weapons and handling. The Huey has none of that. The entries that would hold it are missing, so it behaves like a vehicle that is half-listed: the systems that deal with vehicles after the fact (rewards, targeting, spotting and seat rules) know it, and the systems that define a vehicle do not. Whether a match ever places one is not shown. The one place that names it is a spawn yard, described below.

## Stats

| Stat | Value |
|---|---|
| Max speed | Not stored |
| Fuel | Not stored. The fuel and health display lists the Huey, so it has a fuel gauge, but no capacity |
| Seats | Not stored |
| Mass | Not stored |
| Countermeasures | Not stored |
| Weapons | A mounted machine gun on the second variant. Its stats are not in the data |

## Armor and damage

No main health, no engine, fuel tank or rotor health and no damage zones are known for the Huey. Hits to destroy it cannot be worked out, so this wiki gives no counts for it.

What is known is the protection its seated players get. A seat reduction of -25 means a seated player takes 75% of the damage from small and medium arms, and -15 means 85% of the damage from high-calibre arms (see [Seats and passengers](seats-and-passengers.md)). The Huey has the same two values as the Little Bird family ([MH-6](mh-6.md), [AH-6M [Miniguns]](ah-6m-miniguns.md) and [AH-6R [Rockets]](ah-6r-rockets.md)) and the [Z20 Lakota](z20-lakota.md) after Season 2. Both of its variants carry the same rule.

When a Huey is destroyed it plays the generic helicopter explosion, the same one as the Z20 Lakota. The Havoc and the Little Bird family each have their own. See [Destruction](../game-mechanics/destruction.md).

## Destroy reward

Destroying a Huey is worth 1,200 cash as a base reward. That sits between the MH-6 (800) and the Havoc (6,000) in the reward list. The entry is for all Huey variants. The same entry also holds the shared vehicle bonus values: it is worth 1.25 times the base in a Control Zone and 1.5 times in a Hot Zone (inferred from the column names; see [Cash and rewards](../progression-and-economy/cash-and-rewards.md)).

Destroying a Huey also has its own challenge reward tags, including tags for the assist rewards (fuel supplied, logistic and revive assists) and for the mounted machine gun variant. The amounts paid are set by the challenge tables, not by the vehicle.

## Weapons and seats

The game names a mounted machine gun on the Huey ("Machine Gun" is the only name it has). The Pilot role has three skills for mounted machine guns that list it by item: one for horizontal recoil, one for vertical recoil and one for aim-down-sights time. The gun also has a muzzle flash entry. See [Vehicle weapons](vehicle-weapons.md) for the mounted guns that do have stats.

No seat count, no list of seat roles and no ammunition for the gun are set. The Huey is not in the Pilot role's unlock list, which places the other helicopters. It has a node in the unlock tree layout, but no price is given for it.

## Targeting

Several anti-air weapons list the Huey as a valid target:

- the [Talon 9K-SAM](../building/talon-9k-sam.md), whose target list is the Little Bird family, the Havoc, the Huey, the Z20 Lakota family and the airplane;
- the [MG Nest](../building/mg-nest.md), whose list is the Little Bird family, the Havoc, the Huey and the airplane.

The Huey is also one of the 22 target types of the spotting system, with a separate spotting tag for each variant. See [Spotting](../game-mechanics/spotting.md).

## Vehicle spawns

The Huey is named directly in one air yard on the Zestafona map: the extra air yard of the Lonestar side, which allows the Havoc, the Little Bird family, the Huey and the Z20 Lakota family. The yard does not say which helicopter appears in a slot. The general air yards that allow any air vehicle could also place one (inferred). See [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md).

## Season 2 changes

- The Huey's seat protection was halved, from 50% to 25% against small and medium arms and from 20% to 15% against high-calibre arms. This is the same change the Little Bird family got.

## See also

- [Havoc](havoc.md), the most expensive helicopter in the shop
- [MH-6](mh-6.md), [Z20 Lakota](z20-lakota.md) and the other [helicopters](../vehicles.md)
- [Helicopter Guide](../guides/helicopter-guide.md)
- [Seats and passengers](seats-and-passengers.md)

## Sources

- [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md): the air yard that names the Huey
- [Game Mechanics](../../content/Wardogs_GameMechanics_v2.md): the seat-protection entries and the Season 2 change
- [Gameplay Tags](../../content/Wardogs_GameplayTags_v1.md): the Huey reward and platform tags
- [Spotting](../../game-features/Wardogs_GameFeatures_Spotting_v2.md): the Huey target types
- [VFX](../../content/Wardogs_VFX_v2.md): the mounted machine gun muzzle flash
- [Meta Progression](../../content/Wardogs_Meta_v2.md): the Pilot mounted-gun skills
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md): the destroy reward
- Vehicle destroy reward values: base 1,200 and the zone multipliers
- Seat damage reduction values: the -25 and -15 entries
- Air vehicle demolition rules: the Huey rule set
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md): the reserved platform XP tag
