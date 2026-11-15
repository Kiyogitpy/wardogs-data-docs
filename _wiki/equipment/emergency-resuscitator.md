---
title: Emergency Resuscitator
parent: "Equipment"
group: "Medical"
description: "A single-use revive item, limited to one per life, that revives a downed teammate faster than bare hands."
---

# Emergency Resuscitator

| Emergency Resuscitator | |
|---|---|
| ![Emergency Resuscitator]({{ '/assets/img/icons/utility-3d/t_ui_icon_enox_512x512.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Medical, quick slot |
| Inventory size | 1 by 2 slots |
| Uses | Single use |
| Buy limit | One per life (shop data) |
| **Effect** | |
| Revives | A downed teammate, to 10 HP |
| Use time | Historical 2.2 s montage; separate 4 s interaction model (S3 consumer unresolved) |
| Effects while using | Maximum movement speed halved |
| **Availability** | |
| Price | Listed as 0 in the shop data |
| Unlock level | 0 (shop data) |
| **Data** | |
| Internal name | `Id.Item.Resuscitator.Cheap` |
{: .wiki-infobox }

The Emergency Resuscitator revives a downed teammate. It is a single-use item, and the shop text says it is limited to one per life. It revives faster than a bare-hands revive.

## Overview

The shop describes the item as a one-per-life emergency revive that revives teammates faster and is single use. The S3 vendor export lists price 0, `LifeTimeBuyLimit` 1 and `bShowInVendor` true; actual match availability and loot placement are not established by that row. The Field Resuscitator is the other item of this type, with the same use behavior.

## Effects

- **Revive:** brings a downed teammate back to 10 HP. One revive is applied and the item is used up. On a player from the other faction, the revived player also gets a 60 s effect (see [Status Effects](../game-mechanics/status-effects.md)).
- **Container:** the item holds 10 units, emptied at 1 unit every 4 s. The historical round 39 action trace applies one revive after a derived 4 s interaction, rather than stepping through all 10 units (which would give 44 s in that formula). This is a historical consumer model using the unchanged S3 container values.
- **Movement:** maximum movement speed is halved while the item is in use.
- **Bleeding:** No bleeding-cure effect is listed on this item. The cited CL516586-era search found the downed bleed-out timer, not a damage-over-time bleeding system; that negative search does not establish absence in S3.

### Medic skills

The Medic skill for base revive speed covers only the bare-hands revive, not this item, and no number is known for it. The post-revive sprint boost applies after you revive a teammate, and it gives both you and the revived teammate 1.2 or 1.4 times sprint speed for 5 s.

## Use and timing

The historical montage is about 2.2 s long. The four-second estimate instead comes from the round 39 container-action trace: `(0 / 1 + 1) × 4 s`, followed by one revive and consumption. It is not the montage length, and the current S3 action consumer has not been reverified. The historical action targets a downed player; its other-faction branch means this should not be read as a universal teammate-only restriction.

## Cost

The shop lists a price of 0 for this item, and a buy limit of 1, shown in the shop text as one per life.

## Season 2 changes

No Season 2 change to this item is listed.

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
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay and armour values
- [Round 42 economy and buildables evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): no vendor, loot or unlock row (P38)
