---
title: Defibrillator
parent: "Equipment"
group: "Medical"
description: "The revive item that brings a downed teammate back at 35 HP after a 4 s charge, powered by a battery."
---

# Defibrillator

| Defibrillator | |
|---|---|
| **General** | |
| Type | Medical, quick slot |
| Inventory size | 2 by 2 slots |
| Power | A battery, which is its magazine |
| **Effect** | |
| Revives | A downed teammate, to 35 HP, instantly once charged |
| Charge time | 4 s |
| Battery use | 25 battery charges per discharge |
| Use time | 9.2 s use animation |
| **Availability** | |
| Price | 1,600 cash |
| Unlock level | 0 (shop data) |
| **Data** | |
| Internal name | `Id.Item.Defibrillator.Standard` |
{: .wiki-infobox }

The Defibrillator is the revive item for teammates. It needs a battery to charge and to use, and it brings a downed teammate back to 35 HP. It cannot be used while you are downed yourself.

## Overview

The shop describes the Defibrillator as reviving a teammate instantly, and says it needs a battery to charge and use. A new one starts with one battery in it. Batteries are sold as [Utility Items](utility-items.md).

## Effects

- **Revive:** a downed teammate is revived to 35 HP at once when the discharge completes.
- **Charge:** the charge takes 4 s.
- **Battery:** each discharge uses 25 battery charges. A standard battery holds up to 100 charges and a large battery holds up to 250, so a standard battery covers four discharges.
- **Blocking:** the item cannot be used while you are downed.
- **Movement and bleeding:** the data gives no movement slow for this item. The Defibrillator does not cure bleeding, because the game has no damage-over-time bleeding.

### Medic skills

The "Defib charge speed" skill is described as reducing the charge time. The "Increased charges per battery" skill is also described. The game files give no number for either skill, so the new charge time and battery use are not in the data.

The revive speed boost skills apply after you revive a teammate. Your sprint and tactical sprint speed are multiplied by 1.2 at skill level 2 and 1.4 at level 4, and the revived teammate gets the same boost. Both last 5 s.

## Use and timing

| Step | Time |
|---|---:|
| Charge | 4 s |
| Use animation | 9.2 s |

The use animation in the data is 9.15 s long, and it loops in its middle part. The 4 s charge is the timer the item runs before the discharge. You need a teammate who is downed for it to revive, and you must be alive and not downed. It has its own reload action, and its magazine is a battery.

## Cost

The Item Shop lists the Defibrillator at 1,600 cash.

## Season 2 changes

No Season 2 change to the Defibrillator is listed in the data.

## See also

- [Utility Items](utility-items.md), for the batteries that power it
- [Emergency Resuscitator](emergency-resuscitator.md) and [Field Resuscitator](field-resuscitator.md), other revive items
- [Medical Items](medical-items.md)
- [Downed and Revive](../game-mechanics/downed-and-revive.md)

## Sources

- [Medical and Healing](../../game-features/Wardogs_Medical_v1.md): charge time, battery use, revive health and the blocking rule
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, shop text, battery requirement, size and weight
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): use and reload actions, blocking rules, animation time
- [GameplayEffect values](../../pipelines/Wardogs_GameplayEffect_Values_v1.md): the revive tag
- [Progression Tables](../../game-features/Wardogs_Progression_v1.md): Medic skills
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): the Medical category label
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): checked for changes
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay and armour values
- [Round 39 medical and movement evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): Medic skill magnitudes are absent from the data (M2)
