---
title: Hammers
parent: "Equipment"
group: "Utility"
description: "The Small, Medium and Large Hammers: the build tools that place and build structures, with their build speed, the structures each one can place and its build amount per hit."
---

# Hammers

| Hammers | |
|---|---|
| ![Hammers]({{ '/assets/img/icons/utility-3d/T_UI_Item_Hammer_1_BC.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Build tool |
| Build speed | Slow (Small), moderate (Medium), fast (Large) |
| Structures | 7 (Small), 12 (Medium), 19 (Large) |
| Weight | 0.32, 1.23, 3.18 kg |
| **Use** | |
| Build amount per hit | 0.5 (Small), 1 (Medium), 1.5 (Large) |
| Build amount on a weak spot | 3 (Small), 5 (Medium), 8 (Large) |
| **Availability** | |
| Price | 100 (Small), 800 (Medium), 2,400 cash (Large) |
| Unlock level | 0 |
| **Data** | |
| Internal name | `ID.Item.BuildTool.Hammer.Small`, `ID.Item.BuildTool.Hammer.Medium`, `ID.Item.BuildTool.Hammer.Large` |
{: .wiki-infobox }

A hammer is the build tool for placing and building structures. Using it places a see-through schematic of the structure, and each hit adds progress until the structure is finished. Every hammer needs [Build Supplies](supplies.md) to build.

## Overview

There are three hammers, each for a different size of structure. The Small Hammer builds small structures only. The Medium Hammer builds large and basic structures. The Large Hammer can build every structure. The shop text calls it fast, but by the swing timing below it adds build progress per second at about the same rate as the Medium, so that is not confirmed.

## How it works

| Hammer | Build amount per hit | Weak-spot amount | Blow time (s) | Dismantle per hit | Durability |
|---|---:|---:|---:|---:|---:|
| Small Hammer | 0.5 | 3 | 0.24 | 150 | 800 |
| Medium Hammer | 1 | 5 | 0.25 | 200 | 1,500 |
| Large Hammer | 1.5 | 8 | 0.45 | 250 | 3,000 |

- A hit adds the build amount divided by the structure's Build Supplies cost to its progress. A bigger hammer therefore needs fewer hits for the same structure, and the same total Build Supplies. The hit counts for each structure are in its article.
- A weak-spot hit adds the larger amount in the table, which is 6, 5 and 5.3 times the normal hit. Weak spots are explained in the [Buildables](../building.md#weak-spots) article.
- The Small Hammer's build amount is 0.5. Barbed Wire and Recon Tent count each hit 3.5 times as much, so a Small Hammer builds them in 4 hits.
- Blow time is the point in the swing when the hit lands, from the first-person animation. It is not the time a build takes.
- The hammers also repair finished structures and dismantle your own. A repair hit restores health at the build amount times the structure's repair multiplier, and a dismantle hit does the damage in the Dismantle column to the structure.
- The hammers have a melee value of 20 (Small), 35 (Medium) and 150 (Large). Each hammer's melee action passes that value as the damage of a swing hit, in a melee damage event tagged with the hammer (read from the melee Blueprint; not tested in play).
- One hit per swing takes 0.567 s with the Small and Medium hammers and 0.883 s with the Large. These come from the use animation (one hit per pass of the swing loop) and are estimates, not times measured in play. The articles use them to give build time in seconds.

The hammer's actions let the player rotate the structure being placed, toggle snapping and toggle placement mode.

## Season 2 changes

| Item | Season 1 | Season 2 |
|---|---:|---:|
| Large Hammer weak-spot build amount | 10 | 8 |
| Medium Hammer weak-spot build amount | 6 | 5 |

The Small Hammer's build amounts did not change in Season 2.

## See also

- [Supplies](supplies.md), for Build Supplies
- [Buildables](../../game-features/Wardogs_Buildables_v1.md), for the structures each hammer can place
- [Utility Items](utility-items.md)

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): build amounts, blow timing, dismantle amounts, and the structures each hammer can place
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, shop text, weights, durability and melee values
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the rotate, snapping and placement actions
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): weak-spot build amount changes
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots and placement checks
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the swing timing (one hit per loop) and build time estimates
