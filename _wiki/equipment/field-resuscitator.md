---
title: Field Resuscitator
parent: "Equipment"
group: "Medical"
description: "A single-use revive item that revives a downed teammate faster than bare hands, priced at 425 cash in Season 2."
---

# Field Resuscitator

| Field Resuscitator | |
|---|---|
| **General** | |
| Type | Medical, quick slot |
| Inventory size | 1 by 2 slots |
| Uses | Single use |
| **Effect** | |
| Revives | A downed teammate; health after the revive not yet known |
| Use time | 2.2 s animation; runs until its container is empty or the target is full |
| Effects while using | Maximum movement speed halved |
| **Availability** | |
| Price | 425 cash (500 in Season 1) |
| Unlock level | 0 (shop data) |
| **Data** | |
| Internal name | `Id.Item.Resuscitator.Standard` |
{: .wiki-infobox }

The Field Resuscitator revives a downed teammate. It is a single-use item, and the shop describes it as a field revive that revives teammates faster than bare hands.

## Overview

The shop describes the Field Resuscitator as a field revive item that revives teammates faster and is single use. It works like the [Emergency Resuscitator](emergency-resuscitator.md), with the same use animation and container. The main difference in the data is the price, and the shop text does not limit it to one per life.

## Effects

- **Revive:** brings a downed teammate back. The health the teammate has after the revive is not yet known.
- **Container:** the item holds 10 units, emptied at 1 unit every 4 s. The data gives 44 s to empty it (derived). Whether a revive needs all 10 units, or ends earlier, is not yet known.
- **Movement:** maximum movement speed is halved while the item is in use.
- **Bleeding:** the item does not stop bleeding. The game has no damage-over-time bleeding to cure.

### Medic skills

The Medic skill for base revive speed covers only the bare-hands revive, not this item, and it has no number in the data. The post-revive sprint boost applies after you revive a teammate, and it gives both you and the revived teammate 1.2 or 1.4 times sprint speed for 5 s.

## Use and timing

The use animation is 2.2 s. The use keeps going until the container is empty or the teammate is full, so the total time is not yet known in full. The item can be used only on a teammate who is downed.

## Cost

The Item Shop lists the Field Resuscitator at 425 cash.

## Season 2 changes

The price fell from 500 cash in Season 1 to 425 cash in Season 2.

## See also

- [Emergency Resuscitator](emergency-resuscitator.md), the one-per-life revive item
- [Defibrillator](defibrillator.md), a battery-powered revive
- [Medical Items](medical-items.md)
- [Downed and Revive](../game-mechanics/downed-and-revive.md)

## Sources

- [Medical and Healing](../../game-features/Wardogs_Medical_v1.md): container, use time, movement effect and open revive questions
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): shop text, price, size
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the shared resuscitator action and its animation
- [Progression Tables](../../game-features/Wardogs_Progression_v1.md): Medic skills
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): price change
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): the Medical category label
