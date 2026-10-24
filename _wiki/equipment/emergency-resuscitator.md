---
title: Emergency Resuscitator
parent: "Equipment"
group: "Medical"
description: "A single-use revive item, limited to one per life, that revives a downed teammate faster than bare hands."
---

# Emergency Resuscitator

| Emergency Resuscitator | |
|---|---|
| **General** | |
| Type | Medical, quick slot |
| Inventory size | 1 by 2 slots |
| Uses | Single use |
| Buy limit | One per life (shop data) |
| **Effect** | |
| Revives | A downed teammate; health after the revive not yet known |
| Use time | 2.2 s animation; runs until its container is empty or the target is full |
| Effects while using | Maximum movement speed halved |
| **Availability** | |
| Price | Listed as 0 in the shop data |
| Unlock level | 0 (shop data) |
| **Data** | |
| Internal name | `Id.Item.Resuscitator.Cheap` |
{: .wiki-infobox }

The Emergency Resuscitator revives a downed teammate. It is a single-use item, and the shop text says it is limited to one per life. It revives faster than a bare-hands revive.

## Overview

The shop describes the item as a one-per-life emergency revive that revives teammates faster and is single use. The shop data lists its price as 0, so how a player obtains it is not yet known from the data. The Field Resuscitator is the other item of this type, with the same use behavior.

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

The shop data lists a price of 0 for this item, and a buy limit of 1, shown in the shop text as one per life.

## Season 2 changes

No Season 2 change to this item is listed in the data.

## See also

- [Field Resuscitator](field-resuscitator.md), the other single-use revive item
- [Defibrillator](defibrillator.md), a battery-powered revive
- [Medical Items](medical-items.md)
- [Downed and Revive](../game-mechanics/downed-and-revive.md)

## Sources

- [Medical and Healing](../../game-features/Wardogs_Medical_v1.md): container, use time, movement effect and open revive questions
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): shop text, price, buy limit and size
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the shared resuscitator action and its animation
- [Progression Tables](../../game-features/Wardogs_Progression_v1.md): Medic skills
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): the Medical category label
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): checked for changes
