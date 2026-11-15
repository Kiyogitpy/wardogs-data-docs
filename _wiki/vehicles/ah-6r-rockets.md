---
title: "AH-6R [Rockets]"
parent: "Vehicles"
group: "Helicopters"
description: "Small attack helicopter of the Little Bird family with two 70 mm rocket pods."
---

# AH-6R [Rockets]

| AH-6R [Rockets] | |
|---|---|
| ![AH-6R Rockets]({{ '/assets/img/icons/vehicles-3d/T_UI_Vendor_Littlebird_3.png' | relative_url }}){: .wiki-infobox-img } | |
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

The AH-6R [Rockets] is the rocket pod version of the small MH-6 helicopter. It carries two 70 mm rocket pods for attacks on ground targets.

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

Rifle rounds do 7.5% of their damage against the hull. The saved +200% fuel-tank bullet rule names Attribute.Gameplay.Health.FuelTank, whereas the current hitbox model uses Meta.Damage.HitLocation.Vehicle.FuelTank. That model does not apply this bonus (5.56 mm remains at 7.5%); whether S3 native code bridges those tags is unresolved. Rockets that hit the tail or tail rotor take an extra 200%.

Hits needed to destroy the main health. These counts are derived by simulating the damage rules with full-power, point-blank, standard (FMJ) hits; they are estimates worked out from the damage rules, not measured in game:

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
| Rocket Pods (two, 70 mm; S3 announced) | Rockets | 350 rounds/min | 1,000 m | 6.0 s | 0 |

The pod reloads in 6.0 s and starts with no rockets loaded, according to the weapon's own settings. The seats are a driver and one active passenger, as listed for the attack variants.

## Handling

- Driving assists: the climb rate is limited to 36 km/h and the collective holds a hover when released; the collective resets to minus 1 on the ground. See [Vehicle handling](vehicle-handling.md#driving-and-flight-assists).

- Maximum angular velocity 83 deg/s. Translational lift of 16% between 20 and 28 m/s.
- Ground effect falloff 12 m, with no strength set.

## Season 2 changes

- Price rose from 12,500 to 18,800 cash.
- The 35×228 mm cannon rule changed from -40% to -69.5%.
- A new 125 mm rocket rule adds +100%.
- The flares button is renamed Fire Countermeasures. The key is the same (V on keyboard).

## Vehicle spawns

The AH-6R [Rockets] is covered by the air vehicle yards (inferred). Each side normally has one air yard, and every yard allows any helicopter by a general air tag, so it can be placed on all four main maps (three air yards per match). The Little Bird family (MH-6, AH-6M [Miniguns] and AH-6R [Rockets]) is named directly in one Zestafona yard, the extra air yard of the Lonestar side. The airframe is not named in those yards, so which helicopter appears in a slot is not known. See [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md).

## See also

- [MH-6](mh-6.md), the base transport model
- [AH-6M [Miniguns]](ah-6m-miniguns.md), the miniguns version
- [Vehicle damage](vehicle-damage.md)

## Season 3 update

The [official Season 3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) replace the AH-6R's shared 122 mm rocket with a dedicated 70 mm rocket. Announced damage to infantry and vehicles is unchanged, but thrust instability makes its flight wobble and reduces its practical effectiveness against infantry. The other pod settings below remain saved settings, not a newly measured firing test.

The [official Season 3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) announce stronger ballistic protection for Littlebird pilots and co-pilots. This concerns occupants, not the hull percentages above. They also fix body repair on the armed Littlebird variants and make their repair points reachable.

The [official Season 3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) lower the spotted-target kill reward for this vehicle from 1,000 to 850 cash. This is a spotting reward, not the purchase price or a direct destruction reward.

The [official Season 3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) also retune 20×102 mm damage: each round hits a vehicle section once, and this helicopter takes slightly less damage than in Season 2. Retained hit-count tables are conditional calculations, not a new verification of that section-contact behavior.

## Sources

- [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md): which maps place this vehicle
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles Game Feature](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle Parts and Handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 42 weapons evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-weapons.md): the body mass of this aircraft, in kilograms
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the airplane and helicopter mass override values
