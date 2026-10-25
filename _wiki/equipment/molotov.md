---
title: Molotov
parent: "Equipment"
group: "Explosives and throwables"
description: "The Molotov: a thrown incendiary that bursts for 40 HP and leaves a fire area for 45 s that burns players and vehicles."
---

# Molotov

| Molotov | |
|---|---|
| **General** | |
| Type | Lethal, thrown incendiary (quick slot) |
| How it is used | Thrown. Bursts and leaves a fire area |
| Fuse | Bursts on first impact; 5 s backstop |
| Cookable | No |
| **Blast and fire** | |
| Burst damage at centre | 40 HP |
| Burst full damage out to | 2.5 m |
| Burst no damage beyond | 5 m |
| Burst minimum damage | 10 HP |
| Fire area life | 45 s |
| Fire patches | 15 per throw, each 2 m x 2 m and 0.5 m tall |
| Fire damage to players | 15 HP every 0.4 s (37.5 HP per second) |
| Fire damage to vehicles | 2 HP every 0.4 s (5 HP per second) |
| **Availability** | |
| Price | 340 cash |
| Shop unlock level | 1 |
| Required items | None |
| Internal name | `Id.Item.Molotov` |
{: .wiki-infobox }

The Molotov is a thrown incendiary. It does a small burst when it goes off, then leaves a fire area that keeps burning for 45 s. Anyone who stands in the fire takes damage every 0.4 s, which is far more than the burst does.

## Overview

The Molotov is sold as a Lethal, Quick Slot item for 340 cash, and it needs unlock level 1 in the shop data. Its burst is small, so most of its value is the fire. The Season 2 item data adds the Molotov to the item list of each of the 24 emotes, but it does not say what that does in play.

For the other explosives, see [Grenades and Explosives](grenades-and-explosives.md). For the smoke and signal throwables, see [Fire, Smoke and Flash](fire-smoke-and-flash.md).

## How it works

**Throwing.** The Molotov has two throws. An overarm throw sends it at 20 m/s (2,000 cm/s). An underarm throw sends it at 12 m/s (1,200 cm/s). Thrown contact adds 10 HP of impact damage.

**Burst on impact.** A thrown Molotov bursts on its first impact. It is the only throwable set to do so. The 5 s fuse is only a backstop, for a Molotov that does not hit anything. It cannot be cooked.

**Burst.** On detonation the Molotov does its burst damage, then starts a fire area.

**Fire area.** The fire is laid as patches: each throw makes 15, and each patch is a box 2 m by 2 m and 0.5 m tall. The patches last 45 s. Anyone or any vehicle inside a patch takes damage every 0.4 s. The 15 patches lie on a spiral out to about 2.5 m from the impact point. The spiral's centre is pushed up to 3.75 m further along the throw, so the fire spreads forward from where it lands.

**Burning status.** A player in the fire gets a "burning" status. It darkens and blurs the screen, with a vignette effect. The data does not give a timer for the status. It ends when the player leaves the patch: a static reading of the game code finds the status removed on leaving the fire volume (not checked in play).

Armor reduces the burst but not the fire: no armor rule in the data applies to fire damage (derived). The damage tables reduce friendly fire only for infantry bullets (-50 %) and large hammers (-70 %), so fire from a teammate's Molotov has no reduction in the tables. Whether the game mode turns off friendly damage elsewhere is not in these tables.

## Damage

### To players

The burst does 40 HP at its centre, out to 2.5 m. Beyond 2.5 m it falls to zero at 5 m. Standing in the fire is the main threat:

- 15 HP every 0.4 s, which is 37.5 HP per second while in the fire
- The status applies only while the player is in the fire

### To vehicles

The burst does 40 HP at the centre, which is small against vehicles. The data gives the number of burst hits a vehicle needs to lose its main health. This assumes one burst on the main section, and it does not count the fire.

| Vehicle | Main health | Burst hits to destroy |
|---|---:|---:|
| [MH-6](../vehicles/mh-6.md) | 400 HP | 10 |
| [Humvee](../vehicles/humvee.md) | 500 HP | 13 |
| [T-72B3](../vehicles/t-72b3.md) | 750 HP | 20 |
| [M113 APC SV](../vehicles/m113-apc-sv.md) | 1000 HP | 27 |

The fire adds 2 HP every 0.4 s, which is 5 HP per second while a vehicle stays in the area. See [Vehicle damage](../vehicles/vehicle-damage.md) for how vehicles take damage in general.

## Season 2 changes

The Season 2 items data adds the Molotov, along with four other items, to the item list of each of the 24 emotes. The data does not say what this changes in play. The Season 2 items data lists no change to the Molotov's damage, fire, fuse or price.

## See also

- [Fire, Smoke and Flash](fire-smoke-and-flash.md), the overview of fire, smoke and signal throwables
- [Grenades and Explosives](grenades-and-explosives.md), for the blast explosives
- [M18 Smoke Grenade](m18-smoke-grenade.md)
- [Buildables](buildables.md), for structures that fire can affect
- [Vehicle damage](../vehicles/vehicle-damage.md)

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the fire field's 45 s life and the burning status ending on leaving the patch
- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): fire area, burning status, throws and fuse
- [Explosives Reference](../../game-features/Wardogs_Explosives_v1.md): burst damage, radius, falloff and vehicle hit counts
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price and unlock level
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): Molotov burst and fire values
- [Vehicle damage pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md): how explosives are scaled against vehicles
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): Molotov fire patches, fuse and damage rules.
- [Round 39 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-vehicles-explosives.md): Impact burst and patch spiral.
- [Round 40 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-vehicles-explosives.md): the same topics, with the round 40 values where they differ.
