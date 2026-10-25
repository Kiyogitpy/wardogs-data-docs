---
title: "Fixed-wing airplane"
parent: "Vehicles"
group: "Aircraft"
description: "Fixed-wing airplane with a driver seat and one passenger seat; the data has its flight model but no shop listing or display name."
---

# Fixed-wing airplane

| Fixed-wing airplane | |
|---|---|
| Type | Airplane |
| Seats | 2 (driver and one passenger seat) |
| Price | Not sold (no shop listing in the data) |
| Unlock level | Not applicable |
| Main health | 150 HP at start |
| Top speed | Not stored (see Handling) |
| Rifle damage taken (derived) | 7.5% |
| Internal name | FWG_01 |
{: .wiki-infobox }

The fixed-wing airplane is the only fixed-wing aircraft in the data. It has a full flight model with control surfaces, flaps, an airbrake and retractable landing gear. The data does not give it a display name, a shop row or a spawn rule, so this article describes it by what it is.

## Overview

The airplane has two seats, a driver and one passenger. Its damage rules are copied from the Little Bird helicopter family, and its health and fuel setup are its own. The data does not show how players get one in a match.

## Stats

| Stat | Value |
|---|---|
| Max speed | Not stored (see Handling) |
| Fuel | Fuel tank and fuel-leak effects (see below) |
| Seats | 2 |
| Mass override | 10,000 (as stored, unit not stated) |
| Max engine thrust | 226,800 N |
| Countermeasures | Flares, 3 starting, active for 3.5 s |

## Armor and damage

The airplane starts with 150 HP. The data gives threshold triggers on its main health at 90% and on its fuel tank at 90%, 50% and 0%. The fuel tank has three fuel-leak effects of 0.1, 0.4 and 0.5 per second. The data does not say which threshold drives which leak.

Its damage rules are those of the Little Bird family, so rifle rounds do 7.5% of their damage against the hull. The data does not simulate hits to destroy this airplane, so no hit counts are listed.

## Weapons and seats

The airplane has no weapons. It has two seats: a driver seat and an active passenger seat.

## Handling

- The data stores no top speed. The airplane's speed comes from its engine thrust (226,800 N), its mass (10,000) and drag, not from a speed limit.

- Control surfaces: elevators up to 40 degrees each, ailerons and rudders up to 20 degrees, flaps up to 18 degrees, and an airbrake that can extend.
- Retractable landing gear, with a nose wheel that steers up to 45 degrees.
- Main lift multiplier 0.4.
- Translational lift of 20% between 24 and 34 m/s.
- Max angular velocity limit is switched off in the data. The 83 deg/s value is stored but inactive.
- Ground effect strength is 0%, so it has no effect.

## Season 2 changes

- One health-threshold flag in its gameplay settings changed from true to false, and the export does not say what that flag controls.
- The flares button is renamed Fire Countermeasures. The key is the same (V on keyboard).

## See also

- [Vehicle damage](vehicle-damage.md)
- [MH-6](mh-6.md), which shares its damage rules
- [Vehicles](../vehicles.md)

## Sources

- [Vehicles (reference)](../../content/Wardogs_Vehicles_v2.md)
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
