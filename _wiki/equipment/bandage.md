---
title: Bandage
parent: "Equipment"
group: "Medical"
description: "The basic healing item: 35 HP per use on yourself or a teammate, its use times and the movement slow it applies."
---

# Bandage

| Bandage | |
|---|---|
| ![Bandage]({{ '/assets/img/icons/utility-3d/T_UI_Vendor_Bandage.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Medical, quick slot |
| Carry limit | 5 |
| Uses | One heal per item |
| **Effect** | |
| Heals | 35 HP |
| Use time | 5.2 s on yourself, 4.8 s on a teammate |
| Effects while using | Maximum movement speed halved |
| **Availability** | |
| Price | 200 cash |
| Unlock level | 1 (shop data) |
| **Data** | |
| Internal name | `Id.Item.Bandage` |
{: .wiki-infobox }

The Bandage is the basic healing item of the Medical category. Each use adds 35 HP, which is a small heal next to the [Individual First Aid Kit](individual-first-aid-kit.md). It can be used on yourself or on an injured teammate.

## Overview

The Bandage is the cheap, everyday heal. The shop describes it as healing a small amount for yourself or a teammate. Up to 5 can be carried, and it is listed in the quick-slot group of the shop.

## Effects

- **Healing:** +35 HP per use, added to current health. The heal is applied once, when the use animation ends: about 5.2 s on yourself and 4.8 s on a teammate.
- **Movement:** while a bandage is in use, maximum movement speed is halved. The same applies to the other medical items except the Enox.
- **Bleeding:** the Bandage does not stop bleeding. The game has no damage-over-time bleeding to cure. The "bleed" in the game is the downed timer, described in [Downed and Revive](../game-mechanics/downed-and-revive.md).

### Medic skills

The Medic skill "Self-healing speed" and "Teammate healing speed" are described as applying to all medical items. No number for them exists in the game files, and no game code reads them, so how much faster the Bandage heals is not known.

The "Item-switch speed (Medical Archetype)" skill makes switching to a medical item faster. Its equip speed multiplier is 1.2 at skill level 2 and 1.4 at level 4.

## Use and timing

| Use | Time |
|---|---:|
| On yourself | 5.2 s |
| On a teammate | 4.8 s |

The times are the length of each use animation in the data. You must be alive. On yourself you must also be Injured, and a teammate must be Injured too. Starting a bandage use cancels sprint and tactical sprint. A bandage use and a First Aid Kit use block each other, so only one can run at a time.

## Cost

The Item Shop lists the Bandage at 200 cash. No Season 2 change to its price is listed.

## Season 2 changes

No Season 2 change to the Bandage is listed in the data.

## See also

- [Medical Items](medical-items.md)
- [Individual First Aid Kit](individual-first-aid-kit.md)
- [Downed and Revive](../game-mechanics/downed-and-revive.md)

## Sources

- [Medical and Healing](../../game-features/Wardogs_Medical_v1.md): heal amount, use times, movement effect and the bleeding note
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, shop text, unlock level, carry limit
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): use actions, blocking and interrupt rules
- [GameplayEffect values](../../pipelines/Wardogs_GameplayEffect_Values_v1.md): the movement effect
- [Progression Tables](../../game-features/Wardogs_Progression_v1.md): Medic skills
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): the Medical category label
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): checked for changes
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay and armour values
