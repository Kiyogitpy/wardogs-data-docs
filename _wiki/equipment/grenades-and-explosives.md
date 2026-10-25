---
title: Grenades and Explosives
parent: "Equipment"
group: "Explosives and throwables"
description: "Frag grenade, C4, placed mines, Improvised Explosive Device and launcher rounds: blast damage, the distance it reaches, and the fuse or trigger."
---

# Grenades and Explosives

| Grenades and explosives | |
|---|---|
| Hand grenade | M67 Frag Grenade |
| Remote | C4 Charge with Remote Detonator; Improvised Explosive Device with its trigger |
| Placed | Claymore, AT Mine |
| Launcher and bow rounds | 40mm, 84mm, 93mm, 72mm rounds; Explosive Arrow |
| Largest blast at centre | 300 HP (AT Mine and Improvised Explosive Device) |
{: .wiki-infobox }

Grenades and explosives deal damage in a blast around the point where they go off. A thrown grenade or placed charge does its damage at its centre and less further out, and it reaches no further than its outer radius. Molotovs and smoke are covered on [Fire, Smoke and Flash](fire-smoke-and-flash.md).

## Overview

The table lists the blast numbers in the data. These are the starting amounts before armor and before the game's rules for each body part, so they are not the final damage a player takes. Armor reduction is explained on [Body Armor](body-armor.md).

Blast damage falls evenly from the full amount at the inner radius to zero at the outer radius. Where a value is shown as "full to", the blast does its full amount out to that distance.

## Individual items

- [M67 Frag Grenade](m67-frag-grenade.md)
- [C4 Charge](c4-charge.md), with the Remote Detonator
- [Claymore](claymore.md)
- [AT Mine](at-mine.md)
- [Improvised Explosive Device](improvised-explosive-device.md)

## Effects

### Thrown and placed explosives

| Item | Blast at centre | Full damage out to | No damage beyond | Thrown contact |
|---|---:|---:|---:|---|
| M67 Frag Grenade | 100 HP | 5 m | 10 m | 10 HP on thrown contact |
| C4 Charge | 250 HP | 2.5 m | 6 m | 10 HP |
| AT Mine | 300 HP | 3.8 m | 7.5 m | placed, not thrown |
| Claymore | 150 HP | 1.5 m | 3 m | placed, not thrown |
| Improvised Explosive Device | 300 HP | 4 m | 8 m | 10 HP |

Examples from the frag grenade: 100 HP at 5 m, 50 HP at 7.5 m, and nothing from 10 m on.

The gold variant of the M67 Frag Grenade is in the item data, but it has no shop listing, so it is not described further.

### Launcher and bow rounds

These rounds are fired by weapons. The figures are the explosion at the centre of each round. A direct hit before the round arms does the direct-hit damage shown instead of the blast.

| Round | Fired by | Blast at centre | Full damage out to | No damage beyond | Direct hit before arming |
|---|---|---:|---:|---:|---:|
| 40mm grenade | MGL-40 | 100 HP | 2.5 m | 10 m | 80 HP |
| 84mm rocket | MAAWS | 100 HP | 4 m | 10 m | 120 HP |
| 93mm rocket | RPG-7 | 110 HP | 2.5 m | 12 m | 120 HP |
| 72mm rocket | 9K333 Verba | 200 HP | 2 m | 10.8 m | 120 HP |
| Explosive Arrow | Combat bow | 150 HP | 2 m | 4 m | not listed |

The vehicle cannons, artillery and drone shells are on the [Explosives](../../game-features/Wardogs_Explosives_v1.md) data page. They are used by vehicles, not infantry.

**Guidance.** The game data stores guidance settings for two rocket projectiles: the 72 mm rocket has a proportional-navigation (steering) constant of 30, a maximum turn of 10 and a lock-on time of 2 s, and the 70 mm projectile a maximum turn of 1.0 (units as stored). In the game code, guidance only acts while a rocket's motor is thrusting, and only for a projectile marked as guided that has a target: each step it turns toward the target by the steering constant times the angle off, capped at the maximum turn in degrees. The lock-on time is not read by the projectile code (from the game code, not tested in play; whether the 72 mm and 70 mm assets are marked as guided is not confirmed). No weapon item lists the 70 mm projectile, and whether the Talon 9K-SAM's 72 mm rounds use these settings is not confirmed.

**Friendly fire.** The damage tables reduce friendly fire only for infantry bullets (-50 %) and large hammers (-70 %). Explosives and fire have no friendly-fire reduction in the tables. Any limit on hitting teammates with this item would have to come from the item itself or from native code, which the data does not show.

## Use and timing

| Item | Fuse or trigger | Arming | How it is used |
|---|---|---|---|
| M67 Frag Grenade | 4 s after the throw | none | Thrown. Can be cooked (held before throwing). Throwing it back never applies as shipped (from the game code, not tested in play) |
| C4 Charge | Set off by the Remote Detonator; the charge adds a 0.2 s delay | sticks to what it hits | Thrown, then detonated remotely |
| Improvised Explosive Device | 3 s after the trigger is pressed | none | Placed, then detonated remotely; no range limit |
| AT Mine | when a vehicle moves over the trigger area | 1 s after placement | Placed; see [Fire, Smoke and Flash](fire-smoke-and-flash.md) for trigger details |
| Claymore | when a player or vehicle enters the trigger area | 2 s after placement | Placed; see [Fire, Smoke and Flash](fire-smoke-and-flash.md) for trigger details |

### Throwing

The M67 Frag Grenade has three throws: an overarm throw at 2,500 cm/s (25 m/s), an underarm throw at 1,400 cm/s, and a back throw at 1,800 cm/s. From the game code, not tested in play, the back throw never applies as shipped, and molotovs and smoke grenades cannot be thrown back. The C4 trigger and Improvised Explosive Device trigger are thrown at 900 cm/s and 1,200 cm/s. Speeds in the data are in centimetres per second. The throw speed is scaled by a curve of how high you aim, and part of your own movement speed is added to it (a static reading of the throw code, not checked in play).

### Remote detonators

The Remote Detonator sets off placed C4 charges. The data sets the detonator's range to 20,000 units. Units are centimetres in this game, so that is 200 m. A Support skill raises the range to 240 m and then 280 m. The Improvised Explosive Device trigger has no range limit.

## Cost

| Item | Price (cash) |
|---|---:|
| M67 Frag Grenade | 200 |
| C4 Charge | 250 |
| Remote Detonator | 650 |
| Improvised Explosive Device trigger | 300 |
| Claymore | 900 |
| AT Mine | 650 |

Launcher and bow rounds are priced with their weapons. See the [Weapon Shop](../../game-features/Wardogs_WeaponShop_v1.md) data page.

## Season 2 changes

The Season 2 items data lists no change to the blast damage, radius or fuse of any grenade, C4 charge, mine, Improvised Explosive Device or launcher round. It lists no price change for these items either.

## See also

- [Fire, Smoke and Flash](fire-smoke-and-flash.md), for the Molotov, smoke grenades and mine triggers
- [Buildables](buildables.md), which take damage from grenades and explosives
- [Body Armor](body-armor.md)
- [Vehicle damage](../vehicles/vehicle-damage.md)

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the throw speed and friendly-fire readings, and the M67 throw-back caveat
- [Explosives Reference](../../game-features/Wardogs_Explosives_v1.md): blast damage, radius, falloff, fuse and arming values
- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): throw speeds, detonator range and placement
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices and shop text
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): thrown and placed actor values
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
- [Round 42 weapons evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-weapons.md): the throw-back gate for the M67, and the molotov and smoke rule
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the throw-back gate data for grenades, molotovs and smoke
- [Round 46 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-b.md): wiki update notes for gear order, the Drill Rig zone speed, the lock and flare search, rocket guidance and placement rewards
- [Round 47 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round47.md): how guidance is applied in flight
- [Guided projectile data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/r46-guidance.json): the guidance fields for the 72 mm and 70 mm projectiles
