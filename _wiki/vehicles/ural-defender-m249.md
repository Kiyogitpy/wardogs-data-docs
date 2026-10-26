---
title: "Ural Defender [M249]"
parent: "Vehicles"
group: "Cars and trucks"
description: "Armored Ural Defender with a mounted M249 machine gun, sold for 9,500 cash."
---

# Ural Defender [M249]

| Ural Defender [M249] | |
|---|---|
| ![Ural Defender M249](../../assets/img/icons/vehicles-3d/T_UI_Vendor_URAL_3.png){: .wiki-infobox-img } | |
| Type | Heavy truck with machine gun |
| Seats | 3 on the stats sheet (5 seat setups in the seat data) |
| Price | 9,500 cash |
| Unlock level | 0 |
| Main health | 700 HP |
| Top speed | 79 (as stored) |
| Rifle damage taken (derived) | 5% |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#land-wheeled-ural/WHL_07_ArmouredBattle) |
| Internal name | WHL_07 (armored battle variant) |
{: .wiki-infobox }

The Ural Defender [M249] is the armored version of the [Ural Defender](ural-defender.md) with an M249 machine gun mounted on it. It is the most expensive of the Ural family.

## Overview

The Ural Defender [M249] is sold in the vehicle vendor under land transport, for 9,500 cash, and unlocks at level 0. Its Season 2 price went up from 6,750. Its stats sheet and health match the Ural family.

## Stats

| Stat | Value |
|---|---|
| Max speed | 79 (as stored) |
| Fuel capacity | 85 (as stored) |
| Fuel economy | 4.0 (as stored) |
| Seats | 3 (stats sheet) |
| Mass | 10,000 (as stored, unit not stated) |
| Countermeasures | Not stated |

The seat data has 5 setups, but the stats sheet gives 3 seats. The data does not show why they differ.

## Armor and damage

Main health is 700 HP. Its engine, fuel tank and wheels match the [Ural](ural.md). The data uses the Ural damage table for this variant:

| Ammunition | Hits to destroy | Faster route |
|---|---:|---|
| 5.56 mm rifle | 1,000 | 175 through the fuel tank |
| 7.62×54 mm rifle | 637 | 112 through the fuel tank |
| .308 Win | 1,778 | 311 through the fuel tank |
| .50 cal | 312 | 55 through the fuel tank |
| 20×102 mm cannon | 94 | None found |
| 30 mm cannon | 12 | None found |

## Weapons and seats

| Weapon | Type | Rate | Effective range | Reload | Starting ammunition |
|---|---|---:|---:|---:|---:|
| M249 Machine Gun (mounted) | Machine gun | 850 rounds/min | 700 m | 4.25 s | 0 (tracer) |

The gun fires 850 rounds/min out to 700 m. The data gives the reload time and the starting ammunition too (none loaded at the start, tracer rounds).

## Handling

Handling matches the Ural: mass 10,000, hand brake 50, and front steering of 30 degrees.

- **Tyre states.** Each tyre has three states: intact; damaged (deflated), at or below 55% of the wheel's health; and destroyed, at 0. The wheel data stores a radius, friction and brake value for each state. [Repair and vehicle parts](repair-and-vehicle-parts.md) covers what each state does.

## Season 2 changes

- Price rose from 6,750 to 9,500 cash.
- The wheel deflation threshold rose from 0.5 to 0.55 on the axles that apply to this variant.

## Vehicle spawns

The Ural Defender [M249] is placed by the ground vehicle yards of all four main maps: [Bakurani](../game-modes-and-maps/bakurani.md), [Ozeti](../game-modes-and-maps/ozeti.md), [Zestafona](../game-modes-and-maps/zestafona.md) and [Saburtulo](../game-modes-and-maps/saburtulo.md). The yards list the vehicle family (Ural, Ural Defender and Ural Defender [M249]), not each variant, so which variant appears in a slot is not in the data (inferred). A match offers it in 7 of the 7 ground yards on Ozeti, 5 or 6 of the 7 or 6 on Bakurani, 7 of 7 on Zestafona and 6 of 6 on Saburtulo. The data gives no vehicle count or respawn timer per yard. See [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md).

## See also

- [Ural](ural.md) and [Ural Defender](ural-defender.md), the other Ural variants
- [Kodiak [M249]](kodiak-m249.md), a machine gun SUV
- [Vehicle damage](vehicle-damage.md)

## Sources

- [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md): which maps place this vehicle
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
