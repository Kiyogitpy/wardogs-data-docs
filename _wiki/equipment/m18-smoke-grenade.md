---
title: M18 Smoke Grenade
parent: "Equipment"
group: "Explosives and throwables"
description: "The M18 Smoke Grenade in white and black: a thrown smoke cloud that lasts 120 s, with no direct effect on players in the data."
---

# M18 Smoke Grenade

| M18 Smoke Grenade | |
|---|---|
| **General** | |
| Type | Tactical, thrown smoke (quick slot) |
| Variants | M18 Smoke Grenade: White, M18 Smoke Grenade: Black |
| How it is used | Thrown. Releases a cloud of smoke |
| Fuse | 3 s |
| **Cloud** | |
| Cloud length | 120 s |
| Effect on players | None in the data |
| **Availability** | |
| Price, each | 100 cash |
| Shop unlock level | 0 |
| Required items | None |
| Internal name | `ID.Item.SmokeGrenade.White`, `ID.Item.SmokeGrenade.Black` |
{: .wiki-infobox }

The M18 Smoke Grenade makes a cloud of white or black smoke that lasts 120 s. It is the plain smoke throwable, and it is not a blast. In the code found, the only thing that reads the cloud is the aim-assist target picker, so smoke blocks aim assist. Spotting, lock-on and the minimap do not read it. Nothing in the data makes smoke block enemy soldiers' sight: the smoke has no collision or sight-blocker, so AI sight is not blocked as far as the data shows.

## Overview

There are two M18 Smoke Grenades in the item shop, White and Black. They are the same item apart from the colour of the smoke. Each costs 100 cash.

The coloured signal grenades use the same smoke but also place a marker on the map. See [M18 Signal Grenade](m18-signal-grenade.md).

## How it works

**Throwing.** The smoke grenade has the same two throws as the Molotov. An overarm throw sends it at 20 m/s (2,000 cm/s). An underarm throw sends it at 12 m/s (1,200 cm/s).

**Fuse.** It releases its smoke 3 s after it is thrown.

**Cloud.** The cloud lasts 120 s, then fades for 10 s before it is removed. A cloud that is already running when you arrive has lost the time it has already spent. The smoke stops at walls, so it does not pass through them. The smoke effect's default in the game files is 180 s with a 20 s fade in; the white grenade overrides that to 120 s. This is read from the files and was not seen in play.

**Players in the cloud.** The data does not apply any game effect through the smoke. It does not hurt, heal or slow anyone in the cloud. The only effect found is on aim assist, as described above.

## Damage

The M18 Smoke Grenade does no damage. It has no blast and no thrown-contact damage in the data.

## Season 2 changes

The Season 2 items data lists no change to the M18 Smoke Grenade, and no change to its price.

## See also

- [Fire, Smoke and Flash](fire-smoke-and-flash.md), the overview of fire, smoke and signal throwables
- [M18 Signal Grenade](m18-signal-grenade.md), the coloured smoke grenades that also mark the map
- [Molotov](molotov.md), the incendiary throwable

## Sources

- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): smoke asset durations, throws and the smoke volume
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): names, prices and shop text
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): throwable fuse values
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): what the smoke cloud affects in the code found.
- [Round 41 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-modes-ai-other.md): the smoke effect's default duration and fades.
