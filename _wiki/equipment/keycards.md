---
title: "Keycards"
parent: "Equipment"
group: "Utility"
description: "The six faction Keycards (Alpha, Bravo and Charlie, two of each): quick-slot items with a use action, no shop price and no door in the data that takes them."
---

# Keycards

| Keycards | |
|---|---|
| ![Keycards]({{ '/assets/img/icons/other-itemcard-textures/T_UI_Icon_Vendor_PurchaseTag_Icon.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Quick-slot item |
| Cards | 6: Alpha Card 1, Alpha Card 2, Bravo Card 1, Bravo Card 2, Charlie Card 1, Charlie Card 2 |
| Use | A one-handed use action, blocked while you are critically hurt or dead |
| **Availability** | |
| Price | Not sold (no shop row) |
| Unlock level | Not applicable |
| Internal name | `Id.Item.KeyCard.Alpha.1` to `Id.Item.KeyCard.Charlie.2` |
{: .wiki-infobox }

Keycards are six quick-slot items, two for each of the three factions. Each has a use action, but the data names no door, reader or objective that accepts one. They look like a feature that is set up on the item side only.

## Overview

The six cards are Alpha Card 1, Alpha Card 2, Bravo Card 1, Bravo Card 2, Charlie Card 1 and Charlie Card 2. Each card carries a faction and a card number (1 or 2). The faction tags Alpha, Bravo and Charlie are the three team slots. In the spawn data they pair with Lonestar, Valkyra and Manticore (inferred; see [Factions](../game-modes-and-maps/factions.md)).

All six use the same held model, a generic universal tool, and the same one-handed use animation. They can be dropped as a world item. The use action cannot start while the player is critically hurt or dead.

## Effects

The item data records only the faction and the card number. It does not record what a card opens, what a reader checks, or what the use action changes. No door, building or mission file in the data names a keycard.

## Use and timing

Using a card plays a short one-handed animation. The data stores no use time and no durability for it.

## Cost

Keycards are not sold and have no unlock. They have no vendor row and appear in no role or mastery tree.

## Season 2 changes

None found.

## See also

- [Halligan Bar](halligan-bar.md), the tool that opens doors and locked vehicles
- [Utility items](utility-items.md)
- [Factions](../game-modes-and-maps/factions.md)

## Sources

- [Items (feature)](../../game-features/Wardogs_GameFeatures_Items_v2.md): the six keycard rows and the use action
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md): the keycard names in the entity text table
- [Weapon Miscellany](../../game-features/Wardogs_WeaponMisc_v1.md): the keycard animation sets
- [Keycard item folder](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Items/Keycard/Content/Data/Keycards)
