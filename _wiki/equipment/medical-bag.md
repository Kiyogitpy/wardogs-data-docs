---
title: Medical Bag
parent: "Equipment"
group: "Medical"
description: "The only healing item that works over time: it heals yourself or a teammate and can revive a downed teammate, using durability from a 150 pool."
---

# Medical Bag

| Medical Bag | |
|---|---|
| **General** | |
| Type | Medical, specialist item |
| Inventory size | 2 by 2 slots |
| Uses | Durability pool of 150, spent by each action |
| **Effect** | |
| Heals | 35 HP on yourself over 5 s; 15 HP on a teammate over 1.5 s |
| Revives | A downed teammate, to 50 HP |
| Use time | 7.4 s use animation; runs until the target is full or the bag is empty |
| Effects while using | Maximum movement speed halved |
| **Availability** | |
| Price | 1,800 cash |
| Unlock level | 0 (shop data) |
| **Data** | |
| Internal name | `ID.Item.MedKit.Standard` |
{: .wiki-infobox }

The Medical Bag is the only medical item that heals over time. It heals a player continuously while the use lasts, and it can revive a downed teammate. Each action uses up part of the bag's 150 durability, so it lasts a number of heals rather than a number of items. The shop says it costs more to heal yourself with the bag than to heal a teammate.

## Overview

The bag is the item for teammate support. A teammate heal costs only 2 durability for 15 HP, and a revive costs 10 durability for 50 HP. Healing yourself with it is expensive, at 25 durability for 35 HP.

## Effects

| Action | Amount | Time | Rate | Durability cost |
|---|---:|---:|---:|---:|
| Heal yourself | 35 HP | 5 s | 7 HP/s | 25 |
| Heal a teammate | 15 HP | 1.5 s | 10 HP/s | 2 |
| Revive a teammate | 50 HP after the revive | not stated | not applicable | 10 |

The rate column is the amount divided by the time. The game charges the durability once per action, as a fixed amount, not per second or per step (read from the game code). The table below uses that cost.

- **Healing over time:** the tutorial text says the bag heals over time, and that healing stops if you move away.
- **Movement:** maximum movement speed is halved while the bag is in use.
- **Bleeding:** the bag does not stop bleeding. The game has no damage-over-time bleeding to cure.

### Medic skills

The "Medkits have more uses" skill has a usage multiplier in the data, which falls from 1 to 0.6 as the skill levels up. The data gives four values:

| Skill level | Usage multiplier |
|---|---:|
| 0 | 1 |
| 2 | 0.8 |
| 3 | 0.7 |
| 4 | 0.6 |

The game code never reads this multiplier, and it charges the same durability cost at every level. So the bag holds 6 self heals, 75 teammate heals or 15 revives at every level (derived from the fixed costs, 150 durability in total). Whether the server applies the skill is not known. The "Medic bag" skill, which the skill tree describes as adding slots for medical items, has no number in the game files and no code reads it, so its effect is not known.

## Use and timing

The use animation lasts 7.4 s in the data, and it loops between about 1.5 s and 5.7 s. The heal runs until the target is full or the bag is empty, so the total time depends on how much health is missing. The "Medical item switch speed" skill also speeds up switching to the bag, with an equip speed multiplier of 1.2 at skill level 2 and 1.4 at level 4.

The bag can heal yourself only while Injured and alive, and it can heal a teammate who is Injured and alive. A revive needs a downed teammate. A hand revive has a 20 s hold (see Downed and Revive); the data gives no separate hold time for the bag's revive.

## Cost

The Item Shop lists the bag at 1,800 cash.

## Season 2 changes

The price of the Medical Bag fell from 2,000 cash in Season 1 to 1,800 cash in Season 2. No other Season 2 change to the bag is listed.

## See also

- [Medical Items](medical-items.md)
- [Adrenaline Pen](adrenaline-pen.md), and the other healing items
- [Downed and Revive](../game-mechanics/downed-and-revive.md)
- [Progression and Economy](../../game-features/Wardogs_Progression_v1.md), for the Medic skill curve

## Sources

- [Medical and Healing](../../game-features/Wardogs_Medical_v1.md): heal amounts, durability, rates and the skill curve
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, shop text, size and weight
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): use actions and animation times
- [GameplayEffect values](../../pipelines/Wardogs_GameplayEffect_Values_v1.md): the movement effect and the usage multiplier
- [Progression Tables](../../game-features/Wardogs_Progression_v1.md): Medic skills and curves
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): price change
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): the Medical category label
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay and armour values
