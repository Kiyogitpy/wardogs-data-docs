---
title: Binoculars
parent: "Equipment"
group: "Utility"
description: "The Binoculars: the cheapest recon optic, a low magnification view for spotting enemy infantry and vehicles, and its movement slow while in use."
---

# Binoculars

| Binoculars | |
|---|---|
| **General** | |
| Type | Recon, specialist item |
| Use | Spot enemy infantry and vehicles |
| Weight | 0.3 kg |
| **Use** | |
| Magnification | Low |
| Movement while in use | Maximum speed halved |
| **Availability** | |
| Price | 180 cash |
| Unlock level | 0 |
| **Data** | |
| Internal name | `ID.Item.Binoculars` |
{: .wiki-infobox }

The Binoculars are the simplest of the recon optics. They give a low magnification view to spot enemy infantry and vehicles at a distance. They are the cheapest of the four optics sold in the shop.

## Overview

The shop describes the Binoculars as a way to spot enemy infantry and vehicles with low magnification. Unlike the [Range Finder](range-finder.md), they show no distance. The data gives no spotting range, so how far they reveal targets is not yet known.

## How it works

- The Binoculars are held and used by aiming, which uses the item's secondary input.
- While they are in use, maximum movement speed is halved, the same effect the medical items apply.
- Starting a sprint or a tactical sprint interrupts the use. So does inspecting the item.

**How interrupts work in general.** Each action names one response type, and the type decides what happens to the actions already running. Interrupt cancels the listed active actions. Interrupt and buffer cancels them and queues them to run again. Interrupt buffered clears queued copies. Interrupt categories cancels every active action that shares a listed category. Reactivate stops the listed actions and restarts them, with their saved context, once the new action is in place. Interrupt on complete cancels the listed actions when the new action ends. This comes from the action system's code; the individual actions that use each type were not all mapped.

The other recon optics are the [Monocular](monocular.md), the [Range Finder](range-finder.md) and the [Infrared Range Finder](infrared-range-finder.md).

## Season 2 changes

| Item | Season 1 | Season 2 |
|---|---:|---:|
| Binoculars price (cash) | 75 | 180 |

## See also

- [Monocular](monocular.md)
- [Range Finder](range-finder.md)
- [Infrared Range Finder](infrared-range-finder.md)
- [Utility Items](utility-items.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, unlock level, shop text, weight
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the aim use, movement effect and interrupt rules
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): price change
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
- [Round 46 A evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-a.md): wiki update notes and data findings for this article
