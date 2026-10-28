---
title: Infrared Range Finder
parent: "Equipment"
group: "Utility"
description: "The Infrared Range Finder: the most expensive recon optic, with infrared variable magnification, an accurate distance readout and a reload action."
---

# Infrared Range Finder

| Infrared Range Finder | |
|---|---|
| ![Infrared Range Finder]({{ '/assets/img/icons/utility-3d/t_ui_icon_rangefinderIR.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Recon, specialist item |
| Use | Spot enemy infantry and vehicles, with an accurate distance |
| Weight | 0.43 kg |
| **Use** | |
| Magnification | Infrared, variable |
| Distance readout | Accurate |
| Battery use | 0 per second |
| Movement while in use | Maximum speed halved |
| **Availability** | |
| Price | 3,200 cash |
| Unlock level | 0 |
| **Data** | |
| Internal name | `ID.Item.InfraredRangeFinder` |
{: .wiki-infobox }

The Infrared Range Finder is the most expensive optic in the shop. It uses infrared magnification and shows an accurate distance. The Ghillie suit and headwear hide a player from infrared range finders, according to their shop text.

## Overview

The shop text lists the Infrared Range Finder as a variable infrared magnification optic with an accurate distance indicator. It is the most expensive recon item sold. There is no spotting range. Spotting works by timing instead of a range: a spot registers in 0.5 s on infantry and 0.75 s to 1.25 s on vehicles, and fades over 30 s on infantry (see [Spotting](../game-mechanics/spotting.md)).

## How it works

- It is used by aiming, with the item's secondary input.
- Its reload action swaps in a new [Battery](batteries.md). The range finder has one battery slot and comes with a Battery loaded.
- The item's own battery line says 0 per second, but the scope has its own drain rule. Raising the scope costs 3 charges, and then it costs 1 charge every 0.8 s (1.25 a second) while the scope stays up. A full Battery (100 charges) lasts about 78 s of use and a full High Capacity Battery (250 charges) about 198 s. These times come from the game's default settings and were not timed in play.
- The low battery warning sound plays once, when 20 charges or fewer are left while the scope is up. That is about 16 s before the battery runs out. When the charges reach 0 the scope loses power (inferred).
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
