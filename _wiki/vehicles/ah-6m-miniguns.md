---
title: "AH-6M [Miniguns]"
parent: "Vehicles"
group: "Helicopters"
description: "Small attack helicopter of the Little Bird family with two M134D miniguns."
---

# AH-6M [Miniguns]

| AH-6M [Miniguns] | |
|---|---|
| ![AH-6M Miniguns]({{ '/assets/img/icons/vehicles-3d/T_UI_Vehicle_LittleBird_GUNS_BC.png' | relative_url }}){: .wiki-infobox-img } | |
| Type | Combat helicopter (miniguns) |
| Seats | 2 |
| Price | 10,480 cash |
| Unlock level | 1 |
| Main health | 400 HP |
| Top speed | 350 (as stored) |
| Mass | 722 kg |
| Rifle damage taken (derived) | 7.5% |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#air-rotary-littlebird/ROT_03_MachineGuns) |
| Internal name | ROT_03 (miniguns variant) |
{: .wiki-infobox }

The AH-6M [Miniguns] is the miniguns version of the small MH-6 helicopter. It carries two M134D miniguns on the sides, for close-range fire support.

## Overview

The AH-6M [Miniguns] is sold in the vehicle vendor under air combat, for 10,480 cash, and unlocks at level 1. It has the same airframe and health as the [MH-6](mh-6.md), with two seats instead of six and a gun fit in place of the passenger seats.

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
| M134D Minigun (two) | Machine gun | 1,500 rounds/min | 800 m | 4.25 s | 300 (tracer) |

The pilot fires the miniguns. The two guns are grouped on one mount, and only the driver seat can use that weapon. The second seat is an active passenger seat with no gun. The mount can aim from 30 degrees down to 22 degrees up.

## Handling

- Driving assists: the climb rate is limited to 36 km/h and the collective holds a hover when released; the collective resets to minus 1 on the ground. See [Vehicle handling](vehicle-handling.md#driving-and-flight-assists).

- Maximum angular velocity 83 deg/s. Translational lift of 16% between 20 and 28 m/s.
- Ground effect falloff 12 m, with no strength set.

## Season 2 changes

- Price rose from 7,000 to 12,000 cash.
- The 35×228 mm cannon rule changed from -40% to -69.5%.
- A new 125 mm rocket rule adds +100%.
- The flares button is renamed Fire Countermeasures. The key is the same (V on keyboard).

## Vehicle spawns

The AH-6M [Miniguns] is covered by the air vehicle yards (inferred). Each side normally has one air yard, and every yard allows any helicopter by a general air tag, so it can be placed on all four main maps (three air yards per match). The Little Bird family (MH-6, AH-6M [Miniguns] and AH-6R [Rockets]) is named directly in one Zestafona yard, the extra air yard of the Lonestar side. The airframe is not named in those yards, so which helicopter appears in a slot is not known. See [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md).

## See also

- [MH-6](mh-6.md), the base transport model
- [AH-6R [Rockets]](ah-6r-rockets.md), the rocket version
- [Vehicle damage](vehicle-damage.md)

## Season 3 update

The [official Season 3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) reduce this variant from 12,000 to 10,480 cash. The saved vehicle market export agrees. This is the undiscounted price; mode restrictions and progression still affect availability.

The [official Season 3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) increase vehicle-mounted minigun infantry damage multipliers relative to Season 2: head +50%, neck +78%, upper torso +64%, middle torso +55%, lower torso +50%, and pelvis, arms and legs +56%. These are relative increases, not percentage-point additions or fresh hit-count measurements.

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
