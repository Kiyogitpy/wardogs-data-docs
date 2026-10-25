---
title: "AH-6R [Rockets]"
parent: "Vehicles"
group: "Helicopters"
description: "Small attack helicopter of the Little Bird family with two B-13 rocket pods."
---

# AH-6R [Rockets]

| AH-6R [Rockets] | |
|---|---|
| Type | Combat helicopter (rockets) |
| Seats | 2 |
| Price | 18,800 cash |
| Unlock level | 1 |
| Main health | 400 HP |
| Top speed | 350 (as stored) |
| Mass | 722 kg |
| Rifle damage taken (derived) | 7.5% |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#air-rotary-littlebird/ROT_03_RocketPods) |
| Internal name | ROT_03 (rocket pods variant) |
{: .wiki-infobox }

The AH-6R [Rockets] is the rocket pod version of the small MH-6 helicopter. It carries two B-13 rocket pods for attacks on ground targets.

## Overview

The AH-6R [Rockets] is sold in the vehicle vendor under air combat, for 18,800 cash, and unlocks at level 1. It has the same airframe and health as the [MH-6](mh-6.md), with two seats instead of six.

## Stats

| Stat | Value |
|---|---|
| Max speed | 350 (as stored) |
| Fuel capacity | 105 (as stored) |
| Fuel economy | 4.4 (as stored) |
| Seats | 2 |
| Mass | 722 kg |
| Countermeasures | Flares |

## Armor and damage

Main health is 400 HP. The engine has 200 HP, the fuel tank 200 HP, the main rotor 400 HP and the tail rotor 300 HP.

Rifle rounds do 7.5% of their damage against the hull. Bullets that hit the fuel tank take an extra 200%. Rockets that hit the tail or tail rotor take an extra 200%.

Hits needed to destroy the main health. These counts are derived by simulating the damage rules with full-power, point-blank, standard (FMJ) hits; they are estimates from the data, not measured in game:

| Ammunition | Hits to destroy |
|---|---:|
| 5.56 mm rifle | 191 |
| 7.62×54 mm rifle | 122 |
| .308 Win | 264 |
| .50 cal | 60 |
| 20×102 mm cannon | 71 |
| 30 mm cannon | 7 |

## Weapons and seats

| Weapon | Type | Rate | Effective range | Reload | Starting ammunition |
|---|---|---:|---:|---:|---:|
| B-13 Rocket Pods (two, 122 mm) | Rockets | 350 rounds/min | 1,000 m | 6.0 s | 0 |

The pod reloads in 6.0 s and starts with no rockets loaded, according to the weapon data. The seats are a driver and one active passenger, as listed for the attack variants.

## Handling

- Driving assists: the climb rate is limited to 36 km/h and the collective holds a hover when released; the collective resets to minus 1 on the ground. See [Vehicle handling](vehicle-handling.md#driving-and-flight-assists).

- Maximum angular velocity 83 deg/s. Translational lift of 16% between 20 and 28 m/s.
- Ground effect falloff 12 m, with no strength stored.

## Season 2 changes

- Price rose from 12,500 to 18,800 cash.
- The 35×228 mm cannon rule changed from -40% to -69.5%.
- A new 125 mm rocket rule adds +100%.
- The flares button is renamed Fire Countermeasures. The key is the same (V on keyboard).

## Vehicle spawns

The AH-6R [Rockets] is covered by the air vehicle yards (inferred). Each side normally has one air yard, and every yard allows any helicopter by a general air tag, so it can be placed on all four main maps (three air yards per match). The Little Bird family (MH-6, AH-6M [Miniguns] and AH-6R [Rockets]) is named directly in one Zestafona yard, the extra air yard of the Lonestar side. The airframe is not named in those yards, so which helicopter appears in a slot is not in the data. See [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md).

## See also

- [MH-6](mh-6.md), the base transport model
- [AH-6M [Miniguns]](ah-6m-miniguns.md), the miniguns version
- [Vehicle damage](vehicle-damage.md)

## Sources

- [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md): which maps place this vehicle
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 42 weapons evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-weapons.md): the body mass of this aircraft, in kilograms
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the airplane and helicopter mass override values
