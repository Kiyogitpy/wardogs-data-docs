---
title: "Kodiak [M249]"
parent: "Vehicles"
group: "Cars and trucks"
description: "Five-seat Kodiak SUV with a ring-mounted M249 machine gun, sold for 6,750 cash."
---

# Kodiak [M249]

| Kodiak [M249] | |
|---|---|
| ![Kodiak M249]({{ '/assets/img/icons/vehicles-3d/T_UI_Vehicle_Kodiak_MachineGun.png' | relative_url }}){: .wiki-infobox-img } | |
| Type | SUV with machine gun |
| Seats | 5 |
| Price | 6,750 cash |
| Unlock level | 0 |
| Main health | 400 HP |
| Top speed | 154 (as stored) |
| Rifle damage taken (derived) | 5% (from the Kodiak damage rules) |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#land-wheeled-patriot-kodiak/WHL_02_SUV_RingTurret) |
| Internal name | WHL_02 (machine gun variant) |
{: .wiki-infobox }

The Kodiak [M249] is the Kodiak SUV with an M249 machine gun on a ring turret. It seats five.

## Overview

The Kodiak [M249] is sold in the vehicle vendor under land transport, for 6,750 cash, and unlocks at level 0. Its Season 2 price went up from 3,750.

## Stats

| Stat | Value |
|---|---|
| Max speed | 154 (as stored) |
| Fuel capacity | 50 (as stored) |
| Fuel economy | 2.9 (as stored) |
| Seats | 5 |
| Countermeasures | Not stated |

## Armor and damage

Main health is 400 HP, with the same engine, fuel tank and wheel health as the [Kodiak](kodiak.md). The data simulates this variant with the same damage rules as the base Kodiak, so its destruction counts match:

| Ammunition | Hits to destroy | Faster route |
|---|---:|---|
| 5.56 mm rifle | 572 | 143 through the left front wheel |
| 7.62×54 mm rifle | 364 | 91 through the left front wheel |
| .308 Win | 712 | 178 through the left front wheel |
| .50 cal | 178 | 45 through the left front wheel |
| 20×102 mm cannon | 39 | None found |
| 30 mm cannon | 8 | None found |

## Weapons and seats

| Weapon | Type | Rate | Effective range | Reload | Starting ammunition |
|---|---|---:|---:|---:|---:|
| M249 Machine Gun (ring turret) | Machine gun | 850 rounds/min | 700 m | 4.25 s | 0 (tracer) |

The gun fires 850 rounds/min out to 700 m. The data gives the reload time and the starting ammunition too (none loaded at the start, tracer rounds).

## Handling

Handling matches the base Kodiak: mass 2,750, hand brake 50, and front steering of 30 degrees.

- **Tyre states.** Each tyre has three states: intact; damaged (deflated), at or below 55% of the wheel's health; and destroyed, at 0. The wheel data stores a radius, friction and brake value for each state. [Repair and vehicle parts](repair-and-vehicle-parts.md) covers what each state does.

## Season 2 changes

- Price rose from 3,750 to 6,750 cash.
- The vehicle item changed size in inventory (height 4 to 3).

## Vehicle spawns

The Kodiak [M249] is placed by the ground vehicle yards of all four main maps: [Bakurani](../game-modes-and-maps/bakurani.md), [Ozeti](../game-modes-and-maps/ozeti.md), [Zestafona](../game-modes-and-maps/zestafona.md) and [Saburtulo](../game-modes-and-maps/saburtulo.md). The yards list the vehicle family (Kodiak, Kodiak [M249] and Kodiak [Pickup]), not each variant, so which variant appears in a slot is not in the data (inferred). A match offers it in all 7 ground yards on Ozeti, 6 or 7 of the 6 or 7 on Bakurani, 7 of 7 on Zestafona and 6 of 6 on Saburtulo. The data gives no vehicle count or respawn timer per yard. See [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md).

## See also

- [Kodiak](kodiak.md) and [Kodiak [Pickup]](kodiak-pickup.md), the other Kodiak variants
- [Humvee [M249]](humvee-m249.md), a similar machine gun SUV
- [Vehicle damage](vehicle-damage.md)

## Sources

- [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md): which maps place this vehicle
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles Game Feature](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle Parts and Handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
