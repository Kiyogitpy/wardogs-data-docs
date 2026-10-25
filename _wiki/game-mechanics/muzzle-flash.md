---
title: "Muzzle Flash"
parent: "Game Mechanics"
description: "How big each weapon's muzzle flash is for you and for other players, and how suppressors and muzzle devices shrink it."
---

# Muzzle Flash

| Muzzle flash | |
|---|---|
| **General** | |
| Flash sizes stored | Per weapon: size for you (first person), size for other players (third person), lifetime, distant flash |
| Muzzle device assets | 47 |
| Weapon flash recipes | 32 infantry weapons, 16 vehicle guns |
| Typical flash lifetime | 0.05 s (0.06 s for sniper rifles) |
{: .wiki-infobox }

The muzzle flash is the burst of light at the end of a barrel. The game stores one flash recipe for each weapon, a multiplier set for each muzzle device, and a colour override for some ammunition. The flash size is purely visual data: nothing here says how visible a shooter is to the AI or whether the flash counts for detection.

## Overview

Each weapon has two flash sizes. One is what you see on your own screen. The other is what other players see when you fire. For nearly every weapon the other players' flash is larger, because the first person flash is kept small so it does not hide your sights.

## Flash size by weapon

The sizes below are in the game's own units, which are not given in metres or pixels. Compare them with each other.

| Weapon | Your view | Other players' view |
|---|---|---|
| M4 | 10 | 35 |
| AK74 | 15 | 35 |
| A-91 | 15 | 30 |
| KH-2002 | 15 | 30 |
| Galil | 15 | 52.5 |
| FAL | 18 | 57 |
| M500 | 30 | 50 |
| MP43 | 30 | 50 |
| Judge | 25 | 35 |
| Deagle | 25 | 35 |
| M1911 | 10 | 20 |
| MP5, Bizon and other submachine guns | 15 | 25 |
| M14, SVD, SKS (marksman rifles) | not set | 35 |
| MK22, Mosin Nagant, SV98 | 25 | 37 to 40 |

What this means in play: the FAL and Galil throw the largest rifle flash at other players, shotguns (tied with one sniper rifle) the largest at your own screen, and pistols such as the M1911 and the GGX 17 the smallest. Marksman rifles and sniper rifles have a long distant flash (300 for most, 350 for one sniper rifle), so they are the easiest to spot from far away.

## Suppressors and muzzle devices

A weapon's factory muzzle multiplies the first person flash by 1.5 and uses a light strength of 0.1. The suppressor and flash hider assets cut this sharply:

- First person flash: x0.3 to x0.7 (most are x0.35 to x0.5).
- Other players' flash: x0.5 to x0.7.
- Distant flash: x0.75 to x0.85.
- Muzzle light: 0.05, half of the factory value.

So fitting one of these devices both shrinks the flash on your own screen and dims it for people watching you. The game files do not say which shop muzzle device uses which of these assets, so the table above cannot be broken down device by device. See [Muzzle Devices](../attachments/muzzle-devices.md) for what each device does to recoil, spread and aim time.

## Ammunition colour

Every ammunition type uses the same orange flash. Only the 7.62x54mm rimmed round also changes the sparks to a red-orange and uses 2 to 3 of them.

## Vehicle guns

Vehicle guns have their own recipes. Rocket launchers, the tank main guns and artillery spawn a separate flash effect. The tank coaxial gun and some mounted machine guns reuse the M249 SAW muzzle. The numbers for these are on the data page below.

## See also

- [Muzzle Devices](../attachments/muzzle-devices.md)
- [Spread and Recoil](spread-and-recoil.md)
- [Vehicle Weapons](../vehicles/vehicle-weapons.md)

## Sources

- [Muzzle Flashes (data page)](../../content/Wardogs_MuzzleFlashes_v1.md): every ammo, muzzle device, weapon and vehicle gun value
- [VFX](../../content/Wardogs_VFX_v2.md)
- [MuzzleFlashes folder](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes)
