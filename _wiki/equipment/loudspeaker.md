---
title: "Loudspeaker"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A buildable stationary emplacement with no weapon in the game data, built with a Medium or Large Hammer from 200 Build Supplies."
---

# Loudspeaker

| Loudspeaker | |
|---|---|
| **General** | |
| Type | Stationary emplacement |
| Weapon | None in the data |
| **Building** | |
| Build cost | 200 Build Supplies |
| Health | 1,000 HP |
| Hammer | Medium Hammer or Large Hammer |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#stationary-radiotower) |
| Internal name | STN_04 |
{: .wiki-infobox }

The Loudspeaker is the one stationary emplacement in the game data with no weapon. It is built with a Medium or Large Hammer from 200 Build Supplies and has 1,000 HP. It is the only stationary emplacement that a Medium Hammer can build.

## Overview

The Loudspeaker is listed on the [Buildables](buildables.md) page with the other stationary emplacements, but the data gives no gun, ammunition, rate or range for it. The data does not say what it does in play, so that is not yet known.

## Effects

### Weapon

None. The game data has no weapon for this emplacement.

### Damage

The damage data files the Loudspeaker under the same table as the radio tower structure, with 1,000 HP. The [vehicle damage](../vehicles/vehicle-damage.md) page explains how these tables work.

## Use and timing

The Loudspeaker can be placed with a Medium Hammer as well as a Large Hammer, the only stationary emplacement that has this choice. Its placement conditions check the Forward Operating Base bounds, a ladder-bounds rule and a safe-zone rule, the same as the other stationary emplacements. The [Buildables](buildables.md) page describes these rules.

## Cost

| Item | Value |
|---|---|
| Build Supplies | 200 |
| Health | 1,000 HP |
| Hammer | Medium Hammer or Large Hammer |

The Build Supplies cost is not a cash price. Build Supplies are bought in the shop, as the [Buildables](buildables.md) page explains.

## Season 2 changes

- Build cost went from 100 to 200 Build Supplies.
- Two damage entries were added to the emplacement's damage table: one for 20x102 mm cannon hits (amount -70) and one for 125 mm rocket hits (amount +250). The amounts use the same units as the other entries in the [vehicle damage](../vehicles/vehicle-damage.md) table.

## See also

- [Buildables](buildables.md): Build Supplies costs, health and hammers for every structure and stationary weapon
- [Talon 9K-SAM](talon-9k-sam.md), [Vanguard CIWS](vanguard-ciws.md), [Stingray](stingray.md), [MG Nest](mg-nest.md) and [L81 Mortar](l81-mortar.md): the other stationary emplacements

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): Build Supplies cost, health, hammers and placement conditions
- [All vehicles stat and damage sheet](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md): the damage table for this emplacement
- [Vehicles changes, Season 2](../../season-2-changes/vehicles.md): cost and damage table changes
- [Vehicle hitboxes](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-hitboxes.json): the 3D hitbox set used by the viewer link
