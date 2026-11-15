---
title: Field Resuscitator
parent: "Equipment"
group: "Medical"
description: "A single-use revive item that revives a downed teammate faster than bare hands, priced at 425 cash in Season 2."
---

# Field Resuscitator

| Field Resuscitator | |
|---|---|
| ![Field Resuscitator]({{ '/assets/img/icons/utility-3d/t_ui_icon_enox_512x512.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Medical, quick slot |
| Inventory size | 1 by 2 slots |
| Uses | Single use |
| **Effect** | |
| Revives | A downed teammate, to 10 HP |
| Use time | Historical 2.2 s montage; separate 4 s interaction model (S3 consumer unresolved) |
| Effects while using | Maximum movement speed halved |
| **Availability** | |
| Price | 425 cash (500 in Season 1) |
| Unlock level | 0 (shop) |
| **Data** | |
| Internal name | `Id.Item.Resuscitator.Standard` |
{: .wiki-infobox }

The Field Resuscitator revives a downed teammate. It is a single-use item, and the shop describes it as a field revive that revives teammates faster than bare hands.

## Overview

The shop describes the Field Resuscitator as a field revive item that revives teammates faster and is single use. It works like the [Emergency Resuscitator](emergency-resuscitator.md), with the same use animation and container. The main difference is the price, and the shop text does not limit it to one per life.

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
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay and armour values
