---
title: Utility Items
parent: "Equipment"
group: "Utility"
description: "Parachutes, backpacks, tactical vests, recon optics, vehicle and build tools, batteries and supplies: what each one does and what it costs."
---

# Utility Items

| Utility items | |
|---|---|
| Groups | Parachutes, backpacks, tactical vests, recon optics, tools, batteries and supplies |
| Price range | 0 (Pouch) to 3,200 cash (Infrared Range Finder) |
| Unlock level | 0 or 1 for everything listed |
{: .wiki-infobox }

Utility items are the gear that is neither armor, medical, explosive nor buildable. This article covers the parachutes used for dropping in, the backpacks and tactical vests that set how much a player can carry, the optics used for spotting, and the tools used to repair vehicles and open doors.

## Overview

Most of these items have a short description in the shop and few numbers in the data. Where a number is missing, the article says so.

## Effects

### Parachutes

A parachute is a single-use item. It must be deployed by hand, and opening takes 2.0 s according to the data.

| Item | Weight | Price (cash) | Can steer | Notes |
|---|---:|---:|---|---|
| Basic Parachute | 2.5 | 500 | no | No glide; no pull-up |
| Sport Parachute | 9 | 700 | yes | Glide, pull-up and speed caps; pull-up uses stamina |

The Sport Parachute has more features in the data:

- Horizontal speed is capped at 2,200 and vertical speed at 3,000. The data does not give units for these; they are probably centimetres per second.
- Glide acceleration is 1,000.
- A pull-up stamina bar drains at 50 per second and refills at 30 per second.

A player can deploy either parachute only after falling at least 400 units. The data does not give the unit, which is probably centimetres, so that is about 4 m. The parachute also needs at least 1,000 units of clearance above the ground to open.

### Backpacks

A backpack adds a grid of storage slots. The Pouch is free, and the other backpacks cost from 350 to 1,600 cash.

| Backpack | Price (cash) | Grid | Slots |
|---|---:|---|---:|
| Pouch | 0 | 3 x 2 (vertical placement only) | 6 |
| Scout Backpack | 350 | 4 x 2 | 8 |
| Field Backpack | 650 | 6 x 2 | 12 |
| Operator Backpack | 800 | 5 x 3 | 15 |
| Assault Backpack | 1,200 | 5 x 5 | 21 |
| Ruck Backpack | 1,600 | 6 x 4 | 24 |
| Medium Backpack and Sling | 1,400 (hidden in the shop) | not listed | not listed |

The Medium Backpack and Sling adds a sling for one extra weapon or special item, according to the shop text.

### Tactical vests

Tactical vests are not body armor. They give no damage reduction in the data. Each one unlocks more quick slots and speeds up reloading and switching to utility items. None adds storage.

| Vest | Price (cash) | Quick slots unlocked | Reload and utility speed |
|---|---:|---|---|
| Small Tac Vest | 100 | 5 and 6 | minor increase |
| Medium Tac Vest | 250 | 5 to 8 | moderate increase |
| Large Tac Vest | 400 | all | strong increase |

For armor, see [Body Armor](body-armor.md).

### Recon optics

These optics spot enemy infantry and vehicles at a distance. The shop text describes what they show; the data does not give a spotting range.

| Item | Price (cash) | Magnification |
|---|---:|---|
| Binoculars | 180 | low |
| Monocular | 350 | medium, variable |
| Range Finder | 1,450 | high, variable; shows an accurate distance |
| Infrared Range Finder | 3,200 | infrared, variable; shows an accurate distance |

### Tools

| Item | Price (cash) | What it does |
|---|---:|---|
| Halligan Bar | 885 | Pries open doors, but not gates. Limited durability (7,000 in Season 2) |
| Wrench | 180 | Repairs all vehicles, slowly |
| Light Drill | 600 | Repairs vehicles at a moderate speed. Needs batteries |
| Heavy Drill | 1,300 | Repairs vehicles at the fastest speed. Needs batteries |

The Light and Heavy Drills use Batteries, and Batteries also charge the Defibrillator. Two sizes exist:

| Item | Price (cash) | Capacity |
|---|---:|---|
| Battery | 150 | Medium (20V, 5AH) |
| High Capacity Battery | 300 | Large (20V, 15AH) |

### Vehicle fuel

The 40 L Fuel Canister costs 150 cash. It refuels vehicles and has 40 durability. Each use adds 25 fuel, according to the item data.

### Supplies

Supplies are used up by structures and the Forward Operating Base, and all need a Forward Operating Base radius to use.

| Supply | Price (cash, lot of 50) | Use |
|---|---:|---|
| Ammo Supplies | 10 | Reloads buildable weapons |
| Fuel Supplies | 10 | Refuels vehicles at a Refuel Station |
| Mechanical Supplies | 10 | Repairs vehicles at a Repair Station |

The Build Supplies that hammers use are listed on the [Buildables](buildables.md) page.

## Cost

Prices are listed in each table above.

## Season 2 changes

| Item | Season 1 | Season 2 |
|---|---:|---:|
| Basic Parachute price | 100 | 500 |
| Sport Parachute price | 1,000 | 700 |
| Basic and Sport parachute minimum fall height | 100 | 400 |
| Sport pull-up drag | 825 | 400 |
| Halligan Bar price | 1,100 | 885 |
| Halligan Bar durability | 5,000 | 7,000 |
| Wrench price | 150 | 180 |
| Binoculars price | 75 | 180 |
| Monocular price | 150 | 350 |
| Range Finder price | 400 | 1,450 |
| Infrared Range Finder price | 1,200 | 3,200 |

Both parachutes also gained new values in Season 2: a vertical drag coefficient of 1.75, an open time of 2.0 s, and a minimum height above the ground to open of 1,000.

## See also

- [Buildables](buildables.md), for the hammers and Build Supplies
- [Medical Items](medical-items.md), for the Defibrillator that uses Batteries
- [Body Armor](body-armor.md), for armor that protects against damage

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, backpack grids, tactical vest and tool text, and supply prices
- [Parachutes](../../game-features/Wardogs_GameFeatures_Parachutes_v2.md): movement values and the Season 2 update
- [Utility](../../game-features/Wardogs_GameFeatures_Utility_v2.md): the world content packs for consumables, deployables, throwables and tools; the pack files carry no numbers
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): price and durability changes
