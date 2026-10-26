---
title: "Aim Assist"
parent: "Game Mechanics"
description: "How aim assist pulls your aim toward enemies, the four pull modes it can use, and the launcher class that has assist switched off."
---

# Aim Assist

| Aim assist | |
|---|---|
| **General** | |
| Pull modes | All, movement only, look only, off |
| Set separately for | Hip fire and aiming down sights |
| **Performance** | |
| Targets counted at once | 8 |
| Switched off | Launchers: RPG-7, 9K333 Verba, MGL-40, MAAWS (both hip fire and aiming down sights) |
{: .wiki-infobox }

Aim assist helps you keep your aim on an enemy by pulling your aim toward a target inside the assist reticle. Each weapon class has its own settings, and each one picks a pull mode for hip fire and another for aiming down sights. The settings are stored in the game data. The figures below are the values as stored, not values checked in play.

## Overview

Aim assist is a pull, not an automatic aim. The game looks at the enemies in a set area in front of you and nudges your aim toward them. How strong the nudge is depends on the settings for the weapon class.

## How it works

- **Pull modes.** The mode decides when the pull happens. **All** pulls when you move or look. **Movement only** pulls only when you move. **Look only** pulls only when you move the camera. **Off** never pulls.
- **Input.** Unless a setting says otherwise, the pull needs input from you, either movement or looking (derived from the game's default for this setting).
- **Targets.** Up to 8 targets are counted at once for every class. A minimum weight of 0.125 is stored for every class.
- **Slow-down.** The settings also hold a slow-down part, with its own rates, that eases your look speed while a target is in the reticle. The data stores the rates, but the feel in play has not been measured.
- **Units.** The target range is in the game's world units, which are centimetres (inferred): 30,000 is 300 m for rifles and 800 is 8 m for melee. The reticle sizes are world units at a depth equal to the target range. Every class uses the same shape, an inner reticle 3% and an outer reticle 9% of that depth wide (and 2.4% and 7.2% high), so the outer reticle is about 5 degrees wide and 4 degrees high and the inner one about 1.7 degrees wide and 1.4 degrees high at any range (derived from the stored numbers). The pull and slow rates (10 in, 8 out) are speeds per second at which the assist fades in and out, so a higher number reaches full strength sooner (inferred; the game code that applies them was not found).
- **Smoke.** The cloud from an [M18 Smoke Grenade](../equipment/m18-smoke-grenade.md) appears to block aim assist on targets inside it (a static reading of the code; not tested in play).
- **Season 2.** Season 2 set the pull and slow rates to 10 in and 8 out for every class except the launchers (see [Season 2 changes](../patch-notes/season-2.md)).

## Numbers

Stored settings by weapon class. The target range is in world units (centimetres, inferred). The launcher column covers the RPG-7, 9K333 Verba, MGL-40 and MAAWS, which share one settings set.

| Setting | Assault rifle | LMG | SMG | Shotgun | Sniper | Pistol | Melee | Launchers |
|---|---|---|---|---|---|---|---|---|
| Pull, hip fire | All | All | All | All | All | All | All | Off |
| Pull, aiming down sights | All | All | All | All | All | All | All | Off |
| Target range | 30,000 | 30,000 | 20,000 | 20,000 | 40,000 | not set | 800 | 0 |

A class with no stored pull mode takes the game's default, which is All in both modes. Only the launcher settings store an Off pull mode in the data.

## Tips that follow from the numbers

- **Launchers get no help.** The RPG-7, 9K333 Verba, MGL-40 and MAAWS have the pull off in both modes, so aiming them is entirely up to you.
- **Smoke may block the assist.** A target inside an M18 cloud probably gets no pull (static reading), so do not count on help against enemies in smoke.

## What is not yet known

- How strong the pull feels in play. The settings are stored, but the feel was not measured.
- Why launchers have no aim assist. They use their own settings set with every strength, rate and range at 0 and the pull off; no file states a reason. Each of the four launchers simply points at that zeroed set.

## See also

- [Controls and Settings](controls-and-settings.md)
- [Spread and Recoil](spread-and-recoil.md)
- [Hit Registration](hit-registration.md)
- [M18 Smoke Grenade](../equipment/m18-smoke-grenade.md)
- [RPG-7](../weapons/rpg-7.md)
- [9K333 Verba](../weapons/9k333-verba.md)
- [MGL-40](../weapons/mgl-40.md)
- [MAAWS](../weapons/maaws.md)

## Sources

- [Items: aim assist settings](../../content/Wardogs_Items_v2.md): section 9, the stored values for each weapon class
- [Round 41 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-weapons.md): the four pull modes, the default modes and the RPG-7 setting
