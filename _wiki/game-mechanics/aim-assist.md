---
title: "Aim Assist"
parent: "Game Mechanics"
description: "How aim assist pulls your aim toward enemies, the four pull modes it can use, and the one weapon class with assist switched off."
---

# Aim Assist

| Aim assist | |
|---|---|
| **General** | |
| Pull modes | All, movement only, look only, off |
| Set separately for | Hip fire and aiming down sights |
| **Performance** | |
| Targets counted at once | 8 |
| Switched off | RPG-7 (both hip fire and aiming down sights) |
{: .wiki-infobox }

Aim assist helps you keep your aim on an enemy by pulling your aim toward a target inside the assist reticle. Each weapon class has its own settings, and each one picks a pull mode for hip fire and another for aiming down sights. The settings are stored in the game data. The figures below are the values as stored, not values checked in play.

## Overview

Aim assist is a pull, not an automatic aim. The game looks at the enemies in a set area in front of you and nudges your aim toward them. How strong the nudge is depends on the settings for the weapon class.

## How it works

- **Pull modes.** The mode decides when the pull happens. **All** pulls when you move or look. **Movement only** pulls only when you move. **Look only** pulls only when you move the camera. **Off** never pulls.
- **Input.** Unless a setting says otherwise, the pull needs input from you, either movement or looking (derived from the game's default for this setting).
- **Targets.** Up to 8 targets are counted at once for every class. A minimum weight of 0.125 is stored for every class.
- **Slow-down.** The settings also hold a slow-down part, with its own rates. The data stores the rates, but the feel in play has not been measured.
- **Smoke.** The cloud from an [M18 Smoke Grenade](../equipment/m18-smoke-grenade.md) appears to block aim assist on targets inside it (a static reading of the code; not tested in play).
- **Season 2.** Season 2 set the pull and slow rates to 10 in and 8 out for every class except the RPG-7 (see [Season 2 changes](../patch-notes/season-2.md)).

## Numbers

Stored settings by weapon class. The data gives no units for the target range.

| Setting | Assault rifle | LMG | SMG | Shotgun | Sniper | Pistol | Melee | RPG-7 |
|---|---|---|---|---|---|---|---|---|
| Pull, hip fire | All | All | All | All | All | All | All | Off |
| Pull, aiming down sights | All | All | All | All | All | All | All | Off |
| Target range | 30,000 | 30,000 | 20,000 | 20,000 | 40,000 | not set | 800 | 0 |

A class with no stored pull mode takes the game's default, which is All in both modes. Only the RPG-7 stores an Off pull mode in the data.

## Tips that follow from the numbers

- **The RPG-7 gets no help.** Its pull is off in both modes, so aiming it is entirely up to you.
- **Smoke may block the assist.** A target inside an M18 cloud probably gets no pull (static reading), so do not count on help against enemies in smoke.

## What is not yet known

- The units of the target range and the reticle sizes. The data gives none.
- How strong the pull feels in play. The settings are stored, but the feel was not measured.
- Whether the RPG-7 has assist off on purpose. The data cannot say.

## See also

- [Controls and Settings](controls-and-settings.md)
- [Spread and Recoil](spread-and-recoil.md)
- [Hit Registration](hit-registration.md)
- [M18 Smoke Grenade](../equipment/m18-smoke-grenade.md)
- [RPG-7](../weapons/rpg-7.md)

## Sources

- [Items: aim assist settings](../../content/Wardogs_Items_v2.md): section 9, the stored values for each weapon class
- [Round 41 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-weapons.md): the four pull modes, the default modes and the RPG-7 setting
