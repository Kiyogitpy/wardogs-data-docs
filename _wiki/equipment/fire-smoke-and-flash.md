---
title: Fire, Smoke and Flash
parent: "Equipment"
group: "Explosives and throwables"
description: "Molotov fire, smoke and signal grenades, mine and Claymore triggers, and throwing. Flash and stun grenades are not in this build."
---

# Fire, Smoke and Flash

| Fire, smoke and flash | |
|---|---|
| Fire | Molotov (burning area for 45 s) |
| Smoke | White and Black smoke; eight coloured signal grenades; vehicle smoke |
| Triggered | AT Mine, Claymore, C4 and Improvised Explosive Device (detail below) |
| Flash and stun | not in this build |
{: .wiki-infobox }

This article covers the throwables and placed gear that do something other than a direct blast: the Molotov's burning area, the smoke and signal grenades, the triggers of the mines and Claymore, and how throwables are thrown. Blast damage and radius for every explosive are on [Grenades and Explosives](grenades-and-explosives.md).

## Overview

Flash and stun grenades are not in the data for this build. There is no flashbang item, no shop listing and no effect. The only remnants are three sound effects and a Medic skill that reduces the effect of flash and stun, which has no number attached in the data.

Destroyed vehicles, the fixed guns and a destroyed forward operating base also set off explosions of their own. See [Destruction](../game-mechanics/destruction.md#wreck-explosions).

## Individual items

- [Molotov](molotov.md)
- [M18 Smoke Grenade](m18-smoke-grenade.md), white and black
- [M18 Signal Grenade](m18-signal-grenade.md), six colours

## Effects

### Molotov

The Molotov bursts on detonation, dealing 40 HP at its centre out to 2.5 m and nothing beyond 5 m. It then leaves a burning area.

- **Burning area.** The fire lasts up to 45 s. It is laid as 15 patches per throw, each a 2 m by 2 m box 0.5 m tall. It damages players and vehicles inside a patch every 0.4 s. The 15 patches spread on a spiral out to about 2.5 m from the impact point.
- **Players.** Each tick deals 15 HP, which is 37.5 HP per second while standing in the fire. Players without the Alive state take no damage.
- **Vehicles.** Each tick deals 2 health, which is 5 per second.
- **Burning status.** A player in the fire gets a "burning" status, shown with a screen effect that darkens and blurs the view. The status ends when the player leaves the patch (a static reading of the game code, not checked in play). The data gives no timer for it.

The Molotov bursts on its first impact. Its 5 s fuse is only a backstop, and it is the only throwable set to burst on impact. Burning damage from the fire counts as the thrower's damage, so kills and score from the fire go to the player who threw the Molotov (a static reading of the game code, not checked in play). Armor reduces the burst but not the fire, since no armor rule in the data applies to fire damage (derived). The damage tables reduce friendly fire only for infantry bullets (-50 %) and large hammers (-70 %), so a teammate's Molotov fire has no reduction in the tables.

### Smoke grenades

Smoke grenades make a cloud of smoke. The data gives the length of each cloud, but no effect on play. No item applies a game effect through smoke, so smoke does not hurt, heal or slow anyone in the data. In the code found, the only thing that reads a smoke cloud is the aim-assist target picker, so smoke blocks aim assist. Spotting, lock-on and the minimap do not read it. Nothing in the data makes smoke block enemy soldiers' sight: the smoke has no collision or sight-blocker, so the AI sight is not blocked as far as the data shows.

| Item | Cloud length | Cost (cash) |
|---|---:|---:|
| M18 Smoke Grenade: White | 120 s | 100 |
| M18 Smoke Grenade: Black | 120 s | 100 |
| Vehicle smoke (countermeasure) | 6 s | 750 |

Vehicle smoke is a countermeasure that trails smoke around a vehicle and then settles into a larger screen, according to the shop text. The screen lasts 6 s and then fades for 2 s before it is removed.

Each smoke stays for its full duration (white and black 120 s, blue signal 64 s, other signals 180 s, vehicle smoke 6 s). Then the plume fades out over the fade time (10 s for the grenades, 2 s for the vehicle screen) before it is removed. A smoke effect that is already running when you arrive has lost the time it has already spent, so less of it is left.

The smoke effect's own defaults in the game files are a 180 s total, a 20 s fade in and a 10 s fade out. The white grenade overrides the length to 120 s. These are read from the files and were not seen in play.

### Signal grenades

Signal grenades release a column of coloured smoke and place a marker on the map. The data gives 180 s of cloud length for most colours and 64 s for the blue one. Each costs 50 cash.

| Colour | Shop name | Map marker | Type |
|---|---|---|---|
| Yellow | Alert | Alert | Tactical |
| Red | Hostile | Hostile | Tactical |
| Blue | Friendly | Friendly | Tactical |
| Orange | Damaged Vehicle | Damaged vehicle | Tactical |
| Green | Supply Request | Supply Request | Logistics |
| Purple | Landing Zone | Landing Zone | Logistics |

Each colour adds its marker through the deployable map tracker, which places the marker on the map. The game names the smoke types "Covering" and "Signal". The data does not say who else can see the marker.

### Mines and placed explosives

The AT Mine, Claymore and Improvised Explosive Device are placed on the ground, and each has its own trigger. Placing them takes time, and the player moves at 40% speed while placing. A placed mine has 1 HP.

| | AT Mine | Claymore | C4 Charge | Improvised Explosive Device |
|---|---|---|---|---|
| Triggered by | Vehicles | Players and vehicles | Remote Detonator | Improvised Explosive Device trigger |
| Speed rule | Vehicle moving above 0.1 km/h | Vehicle moving above 0 km/h | none | none |
| Arming delay | 1 s after placement | 2 s after placement | none | none |
| Delay after trigger | none | none | none (charge 0.2 s) | 3 s |
| Team rule | Triggers on friendly vehicles | Triggers on teammates | none | none |
| Line of sight | not used | yes, to the target | none | none |
| Range | placed up to 4 m away | placed up to 4 m away | 200 m (remote) | no limit |
| Shot | any damage except thrown impacts sets it off | an explosion sets it off; other damage destroys it | a C4 or Improvised Explosive Device blast sets it off; it has 30 HP | same as C4 |

Notes from the data:

- The AT Mine checks for vehicles every 0.1 s, and ignores everything else.
- The Claymore's trigger area is in front of it. Players must have a matching tag to count as a target.
- The C4 charge and Improvised Explosive Device charge stick to the surface they hit. A charge whose owner is no longer valid is removed after a 5 s check, without a blast.
- Placement distance for the mines and Claymore is 400 units, which is about 4 m. The placement angle limit is 30, which the data reads as degrees; this is assumed.

### Throwing

The Molotov and smoke grenades use the same throw speeds:

| Throw | Speed (cm/s) | Speed (m/s) |
|---|---:|---:|
| Overarm (primary) | 2,000 | 20 |
| Underarm (secondary) | 1,200 | 12 |

Each throw also has a speed curve in the data. A static reading of the throw code (not checked in play) scales the flat speed by a curve of how high you aim, and then adds part of your own horizontal and vertical movement speed.

## Use and timing

| Item | Fuse | Notes |
|---|---|---|
| Molotov | 5 s | Cannot be cooked (held before throwing) or thrown back |
| Smoke grenades | 3 s | Cannot be thrown back. The cloud lasts for the length given above |
| C4 Charge | 0.2 s after the trigger | Set off by the Remote Detonator |
| Improvised Explosive Device | 3 s after the trigger | |

## Cost

| Item | Price (cash) |
|---|---:|
| Molotov | 340 |
| M18 Smoke Grenade: White or Black | 100 |
| Signal grenades (each colour) | 50 |
| Vehicle smoke | 750 |
| AT Mine | 650 |
| Claymore | 900 |
| Improvised Explosive Device trigger | 300 |

## Season 2 changes

The Season 2 items data lists no change to the Molotov, smoke grenades, mines or Claymore.

## See also

- [Grenades and Explosives](grenades-and-explosives.md), for blast damage and fuses of the frag grenade, C4 and launcher rounds
- [Buildables](buildables.md), for the structures that the Molotov fire damages

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the 45 s fire field and the burning status ending on leaving the patch, and the throw speed readings
- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): Molotov burst and fire, smoke assets, throws and mine triggers
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, shop text and signal grenade names
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): the Molotov fire field and mine values
- [Explosives Reference](../../game-features/Wardogs_Explosives_v1.md): Molotov blast damage and fuses
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): Molotov patches and fire rules, and what smoke affects in the code found.
- [Round 39 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-vehicles-explosives.md): Smoke duration and fade, signal markers and the Claymore and mine rules.
- [Round 40 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-vehicles-explosives.md): the same topics, with the round 40 values where they differ.
- [Round 41 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-modes-ai-other.md): the smoke effect's default durations and fades.
- [Round 42 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-modes-ai-other.md): which explosion sequence each destroyed item uses.
- [Round 42 weapons evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-weapons.md): fire damage is credited to the thrower, and smoke and Molotovs cannot be thrown back
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the Molotov fire instigator and the throw-back gate
