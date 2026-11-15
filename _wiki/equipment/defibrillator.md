---
title: Defibrillator
parent: "Equipment"
group: "Medical"
description: "The revive item that brings a downed teammate back at 35 HP powered by a battery; its historical charge model uses 4 s."
---

# Defibrillator

| Defibrillator | |
|---|---|
| ![Defibrillator]({{ '/assets/img/icons/utility-3d/T_UI_Icon_Utility_Defib_512x512.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Medical, quick slot |
| Inventory size | 2 by 2 slots |
| Power | A battery, which is its magazine |
| **Effect** | |
| Revives | A downed teammate, to 35 HP, instantly once charged |
| Historical charge time | 4 s; S3 consumer unverified |
| Historical battery cost | 25 charges per discharge; S3 consumer unverified |
| Historical montage length | 9.2 s |
| **Availability** | |
| Price | 1,600 cash |
| Unlock level | 0 (shop) |
| **Data** | |
| Internal name | `Id.Item.Defibrillator.Standard` |
{: .wiki-infobox }

The Defibrillator is the revive item for teammates. It needs a battery to charge and to use, and it brings a downed teammate back to 35 HP. It cannot be used while you are downed yourself.

## Overview

The shop describes the Defibrillator as reviving a teammate instantly, and says it needs a battery to charge and use. A new one starts with one battery in it. Batteries are sold as [Utility Items](utility-items.md).

## Effects

- **Revive:** a downed teammate is revived to 35 HP at once when the discharge completes.
- **Charge:** the historical Blueprint/default trace uses 4 s; current S3 charge timing is unresolved.
- **Battery:** the historical discharge trace spends 25 charges. The saved battery capacities are 100 and 250 charges. Four standard-battery discharges assumes the historical 25-charge discharge cost and no other consumption; current charge/discharge consumers remain unverified.
- **Blocking:** the item cannot be used while you are downed.
- **Movement and bleeding:** no movement-slow effect is listed in the reviewed item data; that is not a complete S3 consumer search. No bleeding-cure effect is listed on this item. The cited CL516586-era search found the downed bleed-out timer, not a damage-over-time bleeding system; that negative search does not establish absence in S3.

### Medic skills

The "Defib charge speed" skill is described as reducing the charge time. The "Increased charges per battery" skill is also described. No number for either skill is known, so the new charge time and battery use are not known.

The revive speed boost skills apply after you revive a teammate. Your sprint and tactical sprint speed are multiplied by 1.2 at skill level 2 and 1.4 at level 4, and the revived teammate gets the same boost. Both last 5 s.

## Use and timing

| Step | Time |
|---|---:|
| Charge (historical Blueprint/default model) | 4 s |
| Use animation (historical montage) | 9.2 s |

The historical montage is 9.15 s long and loops in its middle part. The 4 s charge and 25-charge discharge cost come from historical Blueprint defaults and their consumer trace, not an S3 timing measurement. You need a teammate who is downed for it to revive, and you must be alive and not downed. It has its own reload action, and its magazine is a battery.

## Default controls

Held, the Defibrillator uses the left mouse button (right trigger on a gamepad) for its main use and the right mouse button (left trigger) for its secondary use. Inspect is I. The reload key, R (the left face button on a gamepad), is also bound while it is held. These are defaults and can be rebound in the control settings.

## Cost

The Item Shop lists the Defibrillator at 1,600 cash.

## Season 2 changes

No Season 2 change to the Defibrillator is listed.

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
- [Misc Gameplay Assets: item inputs](../../content/Wardogs_MiscGameplayAssets_v1.md): section 7a, the default keys
