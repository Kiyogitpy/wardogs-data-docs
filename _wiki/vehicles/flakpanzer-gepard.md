---
title: "Flakpanzer Gepard"
parent: "Vehicles"
group: "Armored vehicles"
description: "Two-seat tracked anti-air tank with twin 35 mm Oerlikon cannons, sold for 14,000 cash."
---

# Flakpanzer Gepard

| Flakpanzer Gepard | |
|---|---|
| Type | Anti-air armored vehicle |
| Seats | 2 |
| Price | 14,000 cash |
| Unlock level | 1 |
| Main health | 800 HP |
| Top speed | 65 (as stored) |
| Rifle damage taken (derived) | 0% |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#land-tracked-tnk-01-antiair) |
| Internal name | TNK_01 (anti-air variant) |
{: .wiki-infobox }

The Flakpanzer Gepard is a two-seat tracked anti-air tank. Its twin Duel 35 mm Oerlikon GDF cannons fire at a very high rate, at 1,100 rounds per minute.

## Overview

The Gepard is sold in the vehicle vendor under land tank, for 14,000 cash, and unlocks at level 1. Its Season 2 price went up from 10,000. It has the same tracks and rifle protection as the other tanks in the family.

## Stats

| Stat | Value |
|---|---|
| Max speed | 65 (as stored) |
| Fuel capacity | 110 (as stored) |
| Fuel economy | 10.0 (as stored) |
| Seats | 2 |
| Max incline | 50 degrees |
| Countermeasures | Smoke (1 charge; screen active for 16 s, usable again after 90 s) |

## Armor and damage

Main health is 800 HP. The Gepard has separate health for its engine (150 HP), fuel tank (150 HP) and each track (125 HP).

While its main body stands, the body sends 5% of each hit to the fuel tank. Rifle rounds do no damage, so rifle fire cannot destroy it. Cannon rounds do work:

| Ammunition | Hits to destroy |
|---|---:|
| 5.56 mm, 7.62×54 mm, .308 Win, .50 cal | Cannot be destroyed |
| 20×102 mm cannon | 312 |
| 30 mm cannon | 47 |

## Weapons and seats

| Weapon | Type | Rate | Effective range | Reload | Starting ammunition |
|---|---|---:|---:|---:|---:|
| Duel 35 mm Oerlikon GDF cannons (twin) | Cannon | 1,100 rounds/min | 1,000 m | 4.0 s | None |

The seats are a driver and a gunner in the turret. The Gepard also carries a smoke countermeasure with one charge, like the L2A6. Its smoke screen stays active for 16 seconds, and the Gepard can use smoke again 90 seconds after the first use. The data lists one starting charge. Smoke charges follow the vehicle inventory in the same way as flares: the smoke item must be added to the vehicle. The data does not say what sells or gives smoke charges.

## Handling

- Tracked drive with a top speed of 65 and a maximum incline of 50 degrees.
- Fuel economy is listed as 10.0 (as stored), higher than the other tanks' 8.0 to 8.5. The data does not say which direction is better.

**Engine torque.** The torque curve is set against engine RPM up to 5,000 in the tracked drive data, and the torque values carry no unit label. See [Vehicle handling](vehicle-handling.md) for the other tracked numbers.

## Season 2 changes

- Price rose from 10,000 to 14,000 cash.
- A new 125 mm rocket rule adds +40%.
- Two interaction points on the sides of the vehicle moved outward, from an offset of 40 to 85 (units not stated).
- The vehicle item is wider in inventory (width 4 to 6).

## Vehicle spawns

The Flakpanzer Gepard is placed by the ground vehicle yards of all four main maps: [Bakurani](../game-modes-and-maps/bakurani.md), [Ozeti](../game-modes-and-maps/ozeti.md), [Zestafona](../game-modes-and-maps/zestafona.md) and [Saburtulo](../game-modes-and-maps/saburtulo.md). The yards list the vehicle family (L2A6, Flakpanzer Gepard and SPH-2 share one tank tag), not each variant, so which variant appears in a slot is not in the data (inferred). A match offers it in 7 of the 7 ground yards on Ozeti, 5 or 6 of the 7 or 6 on Bakurani, 7 of 7 on Zestafona and 6 of 6 on Saburtulo. The data gives no vehicle count or respawn timer per yard. See [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md).

## See also

- [SPH-2](sph-2.md) and [L2A6](l2a6.md), the other tanks of this family
- [T-72B3](t-72b3.md), a separate tank
- [Vehicle damage](vehicle-damage.md)

## Sources

- [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md): which maps place this vehicle
- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the smoke screen's 16 s active window and 90 s cooldown, and the other round 41 vehicle readings
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
