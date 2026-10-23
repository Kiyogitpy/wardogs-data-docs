---
title: "Humvee"
parent: "Vehicles"
group: "Cars and trucks"
description: "Four-seat light armored SUV with no weapons, built for off-road travel and the base model of the Humvee family."
---

# Humvee

| Humvee | |
|---|---|
| Type | Light armored SUV |
| Seats | 4 |
| Price | 3,000 cash |
| Unlock level | 0 |
| Main health | 500 HP |
| Top speed | 113.2 (as stored) |
| Rifle damage taken (derived) | 5% |
| Internal name | WHL_05 (default variant) |
{: .wiki-infobox }

The Humvee is a four-seat light armored SUV with no weapons. Its shop description says it is best suited to off-road travel. It is the base model of the Humvee family, which also includes the [Humvee [Minigun]](humvee-minigun.md) and the [Humvee [M249]](humvee-m249.md).

## Overview

The Humvee is sold in the vehicle vendor under land transport, for 3,000 cash, and unlocks at level 0.

## Stats

| Stat | Value |
|---|---|
| Max speed | 113.2 (as stored) |
| Fuel capacity | 65 (as stored) |
| Fuel economy | 3.3 (as stored) |
| Seats | 4 |
| Mass | 7,250 (as stored, unit not stated) |
| Countermeasures | Not stated |

## Armor and damage

Main health is 500 HP. The Humvee has separate health for its engine (400 HP), fuel tank (400 HP) and each wheel (75 HP).

Rifle rounds do 5% of their damage against the hull. The fuel tank takes an extra 400% from bullets, so it is the fastest route to destroy the vehicle.

Hits needed to destroy the main health. These counts are derived by simulating the damage rules with full-power, point-blank, standard (FMJ) hits; they are estimates from the data, not measured in game:

| Ammunition | Hits to destroy | Faster route |
|---|---:|---|
| 5.56 mm rifle | 715 | 129 through the fuel tank |
| 7.62×54 mm rifle | 455 | 82 through the fuel tank |
| .308 Win | 889 | 160 through the fuel tank |
| .50 cal | 223 | 40 through the fuel tank |
| 20×102 mm cannon | 56 | None found |
| 30 mm cannon | 17 | None found |

## Weapons and seats

The Humvee has no weapons. Its four seats are a driver and three passengers.

## Handling

- Mass 7,250, hand brake 80, ABS 50 and traction control 45, as stored.
- Front steering of 35 degrees.
- Torque split of 0.4 to the front and 0.6 to the rear.
- Engine idle 700 RPM, rev limit 4,000 RPM.

## Season 2 changes

- Torque split moved toward the rear wheels: the front share fell from 0.7 to 0.4, and the rear share rose from 0.3 to 0.6.
- The rear suspension was re-tuned, with the compression damper lowered from 9,000 to 8,250 and the rebound damper from 12,000 to 6,250. The front suspension damper also changed.
- The wheel deflation threshold rose from 0.5 to 0.55 on all axles.
- The 35×228 mm cannon rule changed from -67% to -85%, so cannon hits from that calibre now do less damage.
- A new 125 mm rocket rule adds +250%.
- The vehicle item changed size in inventory (height 4 to 3).
- Price is unchanged at 3,000.

## See also

- [Humvee [Minigun]](humvee-minigun.md) and [Humvee [M249]](humvee-m249.md), the armed variants
- [Kodiak](kodiak.md), a smaller SUV
- [Vehicle damage](vehicle-damage.md)

## Sources

- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
