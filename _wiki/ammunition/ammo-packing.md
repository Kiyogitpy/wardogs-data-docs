---
redirect_from: ["/wiki/game-mechanics/ammo-packing/"]
title: "Ammo Packing"
parent: "Ammunition"
description: "How long it takes to load rounds into a magazine, take them out and combine loose rounds, how the time grows with the round count, and which magazines are quicker."
---

# Ammo Packing

| Ammo packing | |
|---|---|
| **General** | |
| Operations | Load, extract (unload), combine loose rounds |
| Time set by | Caliber and round count |
| **Magazines** | |
| Quicker magazines | 3 of 69 (factor 0.6 to 0.8) |
| Time unit | Seconds (inferred) |
{: .wiki-infobox }

Filling a magazine, emptying one and combining loose rounds all take time. The time depends on the caliber and on how many rounds are moved, and a few magazines work faster.

## Overview

Each caliber has its own time curve for each operation. A curve lists a time for a few round counts, and the time between two listed counts is a straight line. A magazine can then change that time with its own factor.

## How it works

- **Caliber.** The game looks up the curve for the round's caliber. If the ammunition has no curve of its own, such as a tracer, it uses the curve of its parent caliber, so tracer rounds use the plain caliber's curve. Only when the whole chain has no curve does a default curve apply.
- **Round count.** The time is read at the number of rounds being moved.
- **Magazine factor.** Each magazine has a load factor and an extract factor, and the curve's time is multiplied by the factor. Most magazines use 1.0, which leaves the curve's time unchanged.
- **Combining.** Combining loose rounds adds two of these times together (derived from how the game calls the curves). In a static reading of the code, the magazine rounds are taken from (the source) supplies the extract factor and the magazine they go into (the target) supplies the load factor.
- **Unit.** The times are treated as seconds. This is inferred from how the game uses them as operation durations and has not been checked in play.

## Numbers

Curve points per caliber, as stored. Each entry is the time at the round count shown.

| Caliber | Load | Extract | Combine loose |
|---|---|---|---|
| 5.56 mm | 0.5 at 0 rounds, 60 at 200 | 0.3 at 0, 40 at 200 | 0.5 at 0, 14.25 at 200 |
| 9 mm | 0.4 at 0, 35 at 100 | 0.3 at 0, 20 at 100 | 0.4 at 0, 5.3 at 100 |
| 7.62×54 mm | 1 at 0, 45 at 100 | 0.7 at 0, 30 at 100 | 1 at 0, 19 at 100 |
| 12 gauge | 0.5 at 0, 20 at 30 | 0.3 at 0, 10 at 30 | 0.5 at 0, 8 at 48 |

Three magazines have a factor below 1.0, and all three are for machine guns. The factor applies to both load and extract. Examples at 100 rounds (derived, using the curves above and the factors):

| Magazine | Factor | Load | Extract |
|---|---:|---:|---:|
| 5.56 mm, M249 standard magazine | 0.6 | 18.2 | 12.1 |
| 5.56 mm, second M249 magazine | 0.8 | 24.2 | 16.1 |
| 7.62×54 mm, machine-gun magazine | 0.7 | 31.5 | 21.0 |
| 5.56 mm, plain magazine (factor 1.0) | 1.0 | 30.3 | 20.2 |

The round counts are examples. The magazine's capacity is not stored on the magazine item in the data, so the table does not say how many rounds each magazine holds.

## Tips that follow from the numbers

- **Loading is slower than extracting.** For the same round count, the load time is longer than the extract time in every caliber in the data (derived from the curve points).
- **Machine-gun magazines pack faster.** The M249 standard magazine takes 40 percent less time than a plain magazine (factor 0.6).

## What is not yet known

- Whether the times are seconds in play. The unit is inferred from how the game uses them.
- How many rounds each magazine holds is set by the weapon's magazine slot, not by the magazine item, so this page does not list capacities. Each weapon article gives its own.

## See also

- [Ammunition](../ammunition.md)
- [Magazines](../attachments/magazines.md)
- [Weapons](../weapons.md)

## Sources

- [Ammo Packing](../../game-features/Wardogs_AmmoPacking_v1.md): the curves, the magazine factors and the derived examples
- [Round 41 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-weapons.md): the curve lookup with the parent caliber, the factors and the round-count input
