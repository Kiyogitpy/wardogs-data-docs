---
title: Infrared Range Finder
parent: "Equipment"
group: "Utility"
description: "The Infrared Range Finder: a recon optic with a hidden S3 vendor row, infrared variable magnification, an accurate distance readout and a reload action."
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
| Listed price | 3,200 cash; hidden in the S3 vendor row |
| Unlock level | 0 |
| **Data** | |
| Internal name | `ID.Item.InfraredRangeFinder` |
{: .wiki-infobox }

The Infrared Range Finder has the highest listed recon-optic price, but its S3 vendor row sets `bShowInVendor` false; the official Season 3 notes confirm that it was removed from the vendor pending redesign. It uses infrared magnification and shows an accurate distance. The Ghillie suit and headwear hide a player from infrared range finders, according to their shop text.

## Overview

The shop text lists the Infrared Range Finder as a variable infrared magnification optic with an accurate distance indicator. Its vendor row is hidden. A maximum spotting range has not been established. The saved spotting extension supplies timing values: a spot registers in 0.5 s on infantry and 0.75 s to 1.25 s on vehicles, and fades over 30 s on infantry (see [Spotting](../game-mechanics/spotting.md)).

## How it works

- It is used by aiming, with the item's secondary input.
- Its reload action swaps in a new [Battery](batteries.md). The range finder has one battery slot and comes with a Battery loaded.
- The item's own battery line says 0 per second, but the scope has its own drain rule. The historical consumer model charges 3 on raising, then 1 every 0.8 s (1.25 per second) while scoped. A full Battery (100 charges) lasts about 78 s of use and a full High Capacity Battery (250 charges) about 198 s. These are historical round 58 consumer/default calculations, not verified S3 runtime lifetimes. The current scope export retains an obfuscated 0.8 value, but its S3 native field binding has not been established.
- In the historical round 58 model, the warning fires once at 20 or fewer positive charges while scoped, about 16 s before depletion under the stated drain. The historical path stops the scope at zero. Current S3 thresholds and stop behavior are unresolved.
- While it is in use, maximum movement speed is halved.
- The [Ghillie Body Suit](ghillie-body-suit.md) and [Ghillie Headwear](ghillie-headwear.md) hide the player from infrared range finders, according to their shop text.

## Season 3 announcement

The Infrared Range Finder was removed from the vendor pending a redesign. The retained 3,200-cash row and historical unlock information do not make it purchasable.

Source: [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221). These are developer-announced changes; saved fields and historical models below do not independently verify the current binary consumer.

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
