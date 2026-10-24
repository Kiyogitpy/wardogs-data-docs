---
title: "Stingray"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A buildable stationary emplacement whose ammunition is listed as UAV, built with a Large Hammer from 650 Build Supplies."
---

# Stingray

| Stingray | |
|---|---|
| **General** | |
| Type | Stationary emplacement |
| **Weapon** | |
| Gun | Main barrel |
| Ammunition | UAV (drone projectile) |
| Fire mode | Semi-automatic |
| Rate | 50 rounds/min |
| Effective range | 10,000 m |
| Reload | Not yet known |
| Starting ammunition | 0 |
| Restock | 900 Ammo Supplies |
| **Building** | |
| Build cost | 650 Build Supplies |
| Health | 3,000 HP |
| Hammer | Large Hammer |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#stationary-stn-05) |
| Internal name | STN_05 |
{: .wiki-infobox }

The Stingray is a buildable stationary emplacement with a main barrel that fires UAV projectiles. The game lists its ammunition as "UAV", so it appears to be a drone launcher, though the data does not describe the projectile in plain words. It is built with a Large Hammer from 650 Build Supplies and has 3,000 HP.

## Overview

The Stingray starts with no ammunition and needs a restock before it can fire. The restock takes 900 Ammo Supplies, the largest restock of the stationary weapons in the data. The match interface has a drone reload screen for this emplacement.

## Effects

### Weapon

The barrel is listed at 50 rounds/min in semi-automatic mode, with an effective range of 10,000 m. The data gives a reload value of 0.0 s, which may mean that the barrel has no reload step, but the export does not confirm this, so the reload is shown as not yet known.

The data does not give a windup time or a bullet speed that this article can check against play.

## Use and timing

The Stingray uses the same placement rules as the other stationary weapons: it is built with a Large Hammer, and its placement conditions check the Forward Operating Base bounds, a ladder-bounds rule and a safe-zone rule. The [Buildables](buildables.md) page describes these rules.

Because the emplacement starts with no ammunition, the first use in a match depends on a restock. How quickly a restock takes effect in play is not yet known.

## Cost

| Item | Value |
|---|---|
| Build Supplies | 650 |
| Health | 3,000 HP |
| Hammer | Large Hammer |

The Build Supplies cost is not a cash price. Build Supplies are bought in the shop, as the [Buildables](buildables.md) page explains.

## Season 2 changes

- Build cost went from 150 to 650 Build Supplies, the largest change of any stationary weapon.
- One damage entry was added to the emplacement's damage table for 125 mm rocket hits (amount -50), and another for 20x102 mm cannon hits (amount -70). The amounts use the same units as the other entries in the [vehicle damage](../vehicles/vehicle-damage.md) table.

## See also

- [Buildables](buildables.md): Build Supplies costs, health and hammers for every structure and stationary weapon
- [Talon 9K-SAM](talon-9k-sam.md), [Vanguard CIWS](vanguard-ciws.md), [MG Nest](mg-nest.md), [Loudspeaker](loudspeaker.md) and [L81 Mortar](l81-mortar.md): the other stationary emplacements

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): Build Supplies cost, health, hammer and placement conditions
- [All vehicles stat and damage sheet](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md): the barrel's rate, fire mode, effective range and damage table
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): the UAV ammunition name
- [Vehicles changes, Season 2](../../season-2-changes/vehicles.md): cost and damage table changes
- [Stingray weapon data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/Weapons/WeaponExtensions/WE_STN_05_Heavy_MainBarrel.json): restock and ammunition
- [Vehicle hitboxes](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-hitboxes.json): the 3D hitbox set used by the viewer link
