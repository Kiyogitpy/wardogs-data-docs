---
title: Adrenaline Pen
parent: "Equipment"
group: "Medical"
description: "A non-healing item that gives unlimited tactical sprint for 60 s and makes your carried equipment lighter to carry."
---

# Adrenaline Pen

| Adrenaline Pen | |
|---|---|
| ![Adrenaline Pen]({{ '/assets/img/icons/utility-3d/T_UI_Item_Stim_BC.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Medical, quick slot |
| Carry limit | 3 |
| Uses | One use per pen |
| **Effect** | |
| Heals | None |
| Effect | 60 s of unlimited tactical sprint stamina and focus energy; equipment weight class one step lighter |
| Use time | 2.0 s on yourself; 1.3 s on a teammate |
| Effects while using | Maximum movement speed halved |
| **Availability** | |
| Price | 250 cash |
| Unlock level | 1 (shop data) |
| **Data** | |
| Internal name | `Id.Item.StimPen` |
{: .wiki-infobox }

The Adrenaline Pen does not heal. It gives a player unlimited tactical sprint for a short time and makes carried equipment count as one weight class lighter.

## Overview

The shop describes the pen as unlimited tactical sprint for a short time, with a reduced equipment weight class. Up to 3 can be carried. The pen can be used on yourself or on a teammate, and each use has its own use time.

## Effects

- **Tactical sprint:** for 60 s, tactical sprint stamina use is zero, so the player can keep tactical sprinting.
- **Focus energy:** for the same 60 s, focus energy use is zero.
- **Equipment weight:** the item reduces the equipment weight class by one step while the effect lasts.
- **Camera:** the field of view widens by 5% while the effect is held. The widening is ignored while you are downed.
- **Movement:** maximum movement speed is halved while the pen is in use.
- **Stacking:** a second pen used during the 60 s does not add a second stack. The effect keeps one stack, and the second pen restarts the 60 s (derived from the effect's default settings in the game code).

### Medic skills

The "Item-switch speed (Medical Archetype)" skill makes switching to the medical items faster, with an equip speed multiplier of 1.2 at skill level 2 and 1.4 at level 4. It covers the items tagged as medical: the Medical Bag, Bandage, Individual First Aid Kit, Defibrillator, both Resuscitators and this pen. It does not cover the Enox.

## Use and timing

| Use | Time |
|---|---:|
| On yourself | 2.0 s |
| On a teammate | 1.3 s |

The times are the length of each use animation. The self use requires you to be alive. The teammate use requires the teammate to be alive. A teammate who is alive gets the same 60 s of unlimited tactical sprint, and nothing more. The self and teammate pen uses block each other.

## Cost

The Item Shop lists the pen at 250 cash.

## Season 2 changes

No Season 2 change to the pen is listed.

## See also

- [Medical Items](medical-items.md)
- [Medical Bag](medical-bag.md), for a heal over time
- [Downed and Revive](../game-mechanics/downed-and-revive.md)

## Sources

- [Medical and Healing](../../game-features/Wardogs_Medical_v1.md): use times, the tactical sprint and weight effects, and the camera change
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, shop text, carry limit
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): use actions, animation times and blocking rules
- [GameplayEffect values](../../pipelines/Wardogs_GameplayEffect_Values_v1.md): the tactical sprint and focus effect and the movement effect
- [Progression Tables](../../game-features/Wardogs_Progression_v1.md): Medic skills
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): the Medical category label
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): checked for changes
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay and armour values
