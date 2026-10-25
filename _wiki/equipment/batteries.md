---
title: Batteries
parent: "Equipment"
group: "Utility"
description: "The Battery and High Capacity Battery: the power for the drills and the Defibrillator, with a 5 AH and a 15 AH size."
---

# Batteries

| Batteries | |
|---|---|
| **General** | |
| Type | Resource, power cell |
| Used by | Light and Heavy Drills, Defibrillator |
| **Use** | |
| Battery sizes | Medium (20 V, 5 AH), large (20 V, 15 AH) |
| **Availability** | |
| Price | 150 (Battery), 300 cash (High Capacity Battery) |
| Unlock level | 1 (shop data) |
| **Data** | |
| Internal name | `Id.Item.Battery`, `Id.Item.LargeBattery` |
{: .wiki-infobox }

Batteries are the power cells for the [Drills](drills.md) and the Defibrillator. The High Capacity Battery holds three times the rated amp-hours of the standard Battery and costs twice as much.

## Overview

The shop text lists two sizes. The Battery is a medium 20 V, 5 AH cell. The High Capacity Battery is a large 20 V, 15 AH cell. Both are bought one at a time.

## How it works

| Battery | Price (cash) | Weight (kg) | Capacity |
|---|---:|---:|---|
| Battery | 150 | 0.63 | 20 V, 5 AH |
| High Capacity Battery | 300 | 2 | 20 V, 15 AH |

The weights are in kilograms. The game stores item weight as a whole number 1,000 times the kilogram figure, so the kilogram value here is derived from it.

- The drills use battery power while they work, at 1.25 per second in the item data.
- The Defibrillator needs a battery to charge and to use, according to its shop text. See [Medical Items](medical-items.md).
- A battery is a small magazine of charges. The Battery holds 100 charges and the High Capacity Battery holds 250, and a new one is full. Tools spend charges, and the Defibrillator uses 25 per discharge, so a Battery covers four discharges and a High Capacity Battery ten.
- Each tool and the Defibrillator have one battery slot. Their reload action swaps in a new battery from your inventory, the same way a gun swaps a magazine, and a new tool comes with a battery loaded.
- The drills spend 1 charge for each repair swing that lands (inferred). If every swing is a repair step, that is about 2 charges a second on the Heavy Drill (a step every 0.5 s) and about 1.3 a second on the Light Drill (every 0.75 s), so a Battery lasts about 50 s and 75 s of steady repair and a High Capacity Battery about 125 s and 190 s. These times were worked out from the data, not timed in play.
- The [Infrared Range Finder](infrared-range-finder.md) also drains a battery while its scope is up: 3 charges when you raise it, then 1 charge every 0.8 s.

## Season 2 changes

No Season 2 change to the batteries is listed in the data.

## See also

- [Drills](drills.md)
- [Defibrillator](defibrillator.md)
- [Utility Items](utility-items.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, unlock levels, shop text, weights and capacities
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the battery use of the drills
- [Round 43 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round43-econ-buildables.md)
