---
title: Halligan Bar
parent: "Equipment"
group: "Utility"
description: "The Halligan Bar: a quick-slot tool that pries open doors and locked vehicles, with limited durability and no effect on gates."
---

# Halligan Bar

| Halligan Bar | |
|---|---|
| **General** | |
| Type | Equipment, quick slot |
| Weight | 2.8 (unit not stated) |
| Durability | 7,000 (Season 2); 7 uses, 1,000 per door or vehicle unlock |
| **Use** | |
| Pries open | Doors (not gates) |
| Also | Forces open a locked vehicle |
| Melee damage | 100 in the item data |
| **Availability** | |
| Price | 885 cash |
| Unlock level | 0 |
| **Data** | |
| Internal name | `Id.Item.Crowbar` |
{: .wiki-infobox }

The Halligan Bar is a quick-slot tool. Its main job is to pry open doors. It has limited durability, and it does nothing to gates.

## Overview

The shop text says the Halligan Bar pries open doors but is ineffective against gates, and that it has limited durability. Its durability was 5,000 in Season 1 and is 7,000 in Season 2. When its durability reaches 0 the bar is used up and removed from the inventory (read from the game's action data).

## How it works

- Using it on a door forces the door open. The item data names this as a separate action. Each door opened costs 1,000 durability.
- The item data also gives the bar a vehicle unlock action, which forces open a locked vehicle. Each unlock also costs 1,000 durability. With 7,000 durability that is 7 uses in total, whatever mix of doors and vehicles.
- It can also be swung as a melee weapon. The item data gives the hit 100 damage.
- The bar cannot be used while the player is critically injured or dead.
- Inspecting the item interrupts a use.

## Season 2 changes

| Item | Season 1 | Season 2 |
|---|---:|---:|
| Halligan Bar price (cash) | 1,100 | 885 |
| Halligan Bar durability | 5,000 | 7,000 |

## See also

- [Utility Items](utility-items.md)
- [Hammers](hammers.md), for the other build tools

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, unlock level, shop text, weight, durability and the melee value
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the door and vehicle actions and the blocking rules
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): price and durability changes
- [Round 40 medical, armour and movement evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): the durability cost of the door and vehicle actions
