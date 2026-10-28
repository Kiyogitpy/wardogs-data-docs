---
title: "Humvee [Minigun]"
parent: "Vehicles"
group: "Cars and trucks"
description: "Five-seat Humvee with a ring-mounted M134D minigun, the lowest rifle damage taken of any truck or SUV."
---

# Humvee [Minigun]

| Humvee [Minigun] | |
|---|---|
| ![Humvee Minigun]({{ '/assets/img/icons/vehicles-3d/T_UI_Icon_Vehicle_Humvee_Gun.png' | relative_url }}){: .wiki-infobox-img } | |
| Type | Light armored SUV with minigun |
| Seats | 5 (shop listing; one stats sheet lists 4) |
| Price | 10,000 cash |
| Unlock level | 0 |
| Main health | 500 HP |
| Top speed | 113.2 (as stored) |
| Rifle damage taken (derived) | 2.5% |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#land-wheeled-humvee-minigun) |
| Internal name | WHL_05 (minigun variant) |
{: .wiki-infobox }

The Humvee [Minigun] is the [Humvee](humvee.md) with an M134D minigun on a ring mount. It fires fast at close range, and its body takes the least rifle damage of any truck or SUV.

## Overview

The Humvee [Minigun] is sold in the vehicle vendor under land transport, for 10,000 cash, and unlocks at level 0. Its Season 2 price went up from 4,500. The shop describes it as a five-seat vehicle with a minigun attachment.

## Stats

| Stat | Value |
|---|---|
| Max speed | 113.2 (as stored) |
| Fuel capacity | 65 (as stored) |
| Fuel economy | 3.3 (as stored) |
| Seats | 5 (shop); 4 on one stats sheet |
| Mass | 7,250 (as stored, unit not stated) |
| Countermeasures | Not stated |

## Armor and damage

Main health is 500 HP, with the same engine, fuel tank and wheel health as the [Humvee](humvee.md). Rifle rounds do 2.5% of their damage against the hull.

The fuel tank takes an extra 400% from bullets, and the wheels take an extra 800%. Hits needed to destroy the main health. These counts are derived by simulating the damage rules with full-power, point-blank, standard (FMJ) hits; they are estimates worked out from the damage rules, not measured in game:

| Ammunition | Hits to destroy | Faster route |
|---|---:|---|
| 5.56 mm rifle | 1,429 | 258 through the fuel tank |
| 7.62×54 mm rifle | 910 | 164 through the fuel tank |
| .308 Win | 1,778 | 320 through the fuel tank |
| .50 cal | 445 | 80 through the fuel tank |
| 20×102 mm cannon | 70 | None found |
| 30 mm cannon | 20 | None found |

## Weapons and seats

| Weapon | Type | Rate | Effective range | Reload | Starting ammunition |
|---|---|---:|---:|---:|---:|
| M134D Minigun (ring mount) | Machine gun | 1,500 rounds/min | 800 m | 4.25 s | 150 (tracer) |

The five seats are the driver, one gunner and three passengers. The gunner seat is the second seat. It is an exterior standing seat at the ring mount, and the player who takes it is the one who fires the minigun. Taking that seat puts the player on the gun automatically. The driver and the three passengers do not fire it.

## Handling

Handling matches the base Humvee: mass 7,250, hand brake 80, front steering of 35 degrees, and the same torque split.

- **Tyre states.** Each tyre has three states: intact; damaged (deflated), at or below 55% of the wheel's health; and destroyed, at 0. Each state sets a wheel radius, friction and brake value. [Repair and vehicle parts](repair-and-vehicle-parts.md) covers what each state does.

## Season 2 changes

- Price rose from 4,500 to 10,000 cash.
- The gamepad aim sensitivity for the minigun turret rose from 75 to 100.
- The 35×228 mm cannon rule changed from -71% to -88%.
- The 20×102 mm cannon rule changed from -90% to -88%.
- A new 125 mm rocket rule adds +250%.
- The vehicle item changed size in inventory (height 4 to 3).
- The front and rear torque split and wheel deflation changes that apply to all Humvee variants are listed on the [Humvee](humvee.md) article.

## Vehicle spawns

The Humvee [Minigun] is placed by the ground vehicle yards of all four main maps: [Bakurani](../game-modes-and-maps/bakurani.md), [Ozeti](../game-modes-and-maps/ozeti.md), [Zestafona](../game-modes-and-maps/zestafona.md) and [Saburtulo](../game-modes-and-maps/saburtulo.md). The yards list the vehicle family (Humvee, Humvee [M249] and Humvee [Minigun]), not each variant, so which variant appears in a slot is not known (inferred). A match offers it in 7 of the 7 ground yards on Ozeti, 5 or 6 of the 7 or 6 on Bakurani, 7 of 7 on Zestafona and 6 of 6 on Saburtulo. No vehicle count or respawn timer per yard is known. See [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md).

## See also

- [Humvee](humvee.md), the base model
- [Humvee [M249]](humvee-m249.md), the machine gun variant
- [Vehicle damage](vehicle-damage.md)

## Sources

- [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md): which maps place this vehicle
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles Game Feature](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle Parts and Handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and findings for this article
