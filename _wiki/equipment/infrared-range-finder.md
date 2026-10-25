---
title: Infrared Range Finder
parent: "Equipment"
group: "Utility"
description: "The Infrared Range Finder: the most expensive recon optic, with infrared variable magnification, an accurate distance readout and a reload action."
---

# Infrared Range Finder

| Infrared Range Finder | |
|---|---|
| **General** | |
| Type | Recon, specialist item |
| Use | Spot enemy infantry and vehicles, with an accurate distance |
| Weight | 0.43 kg |
| **Use** | |
| Magnification | Infrared, variable |
| Distance readout | Accurate |
| Battery use | 0 per second in the item data |
| Movement while in use | Maximum speed halved |
| **Availability** | |
| Price | 3,200 cash |
| Unlock level | 0 |
| **Data** | |
| Internal name | `ID.Item.InfraredRangeFinder` |
{: .wiki-infobox }

The Infrared Range Finder is the most expensive optic in the shop. It uses infrared magnification and shows an accurate distance. The Ghillie suit and headwear hide a player from infrared range finders, according to their shop text.

## Overview

The shop text lists the Infrared Range Finder as a variable infrared magnification optic with an accurate distance indicator. It is the most expensive recon item sold. The data gives no spotting range. The data gives spot timing instead of a range: a spot registers in 0.5 s on infantry and 0.75 s to 1.25 s on vehicles, and fades over 30 s on infantry (see [Spotting](../game-mechanics/spotting.md)).

## How it works

- It is used by aiming, with the item's secondary input.
- It has its own reload action in the data. The sources do not say what it reloads, so that is not yet known.
- The item data sets its battery use to 0 per second, so the sources do not show it draining a battery. The audio data includes a low battery warning. What triggers it is not yet known.
- While it is in use, maximum movement speed is halved.
- The [Ghillie Body Suit](ghillie-body-suit.md) and [Ghillie Headwear](ghillie-headwear.md) hide the player from infrared range finders, according to their shop text.

## Season 2 changes

| Item | Season 1 | Season 2 |
|---|---:|---:|
| Infrared Range Finder price (cash) | 1,200 | 3,200 |

## See also

- [Range Finder](range-finder.md)
- [Monocular](monocular.md)
- [Binoculars](binoculars.md)
- [Utility Items](utility-items.md)
- [Optics Comparison](optics-comparison.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, unlock level, shop text, weight, battery use
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the aim and reload actions and the movement effect
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): price change
