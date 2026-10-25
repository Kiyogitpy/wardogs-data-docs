---
title: Medical Items
parent: "Equipment"
group: "Medical"
description: "Healing and revive items: use time, healing amounts, the effects each one applies, and the downed and revive rules."
---

# Medical Items

| Medical items | |
|---|---|
| Items | 8 |
| Heal | Bandage, Individual First Aid Kit, Medical Bag, Enox, Adrenaline Pen |
| Revive | Defibrillator, Emergency Resuscitator, Field Resuscitator, Medical Bag |
| Max HP | 100 |
{: .wiki-infobox }

Medical items heal the player who uses them, a teammate, or both, and some bring a downed teammate back to their feet. Most healing is a fixed amount added in one use. The Medical Bag is the exception, because it heals over time. The data shows no medical item that stops bleeding or does damage over time. In this game, "bleed" refers to the bleed-out timer of a downed player, described below.

## Individual items

- [Bandage](bandage.md)
- [Individual First Aid Kit](individual-first-aid-kit.md)
- [Medical Bag](medical-bag.md)
- [Enox](enox.md)
- [Adrenaline Pen](adrenaline-pen.md)
- [Defibrillator](defibrillator.md)
- [Emergency Resuscitator](emergency-resuscitator.md)
- [Field Resuscitator](field-resuscitator.md)

## Overview

| Item | Heals | Revives | Price (cash) |
|---|---|---|---:|
| Bandage | 35 HP | no | 200 |
| Individual First Aid Kit | 100 HP, back to full from any health at 100 max | no | 800 |
| Medical Bag | 35 HP self over 5 s; 15 HP teammate over 1.5 s | yes, to 50 HP | 1,800 |
| Enox | 40 HP as decaying health | no | 450 (hidden in the shop) |
| Adrenaline Pen | no heal; unlimited tactical sprint for 60 s | no | 250 |
| Defibrillator | no | yes, to 35 HP | 1,600 |
| Emergency Resuscitator | no | yes, to 10 HP | 0 in the shop data |
| Field Resuscitator | no | yes, to 10 HP | 425 |

## Effects

**Bandage.** Adds 35 HP per use. A player can carry up to 5, and the bandage can be used on yourself or a teammate.

**Individual First Aid Kit.** Adds 100 HP per use, which returns a player at 100 max HP to full from any health. The data gives one heal value for the item, so the same amount applies whether it is used on yourself or a teammate.

**Medical Bag.** Uses durability rather than single items. The bag has 150 durability, and each action spends some of it:

| Action | Amount | Time | Durability cost |
|---|---:|---:|---:|
| Heal self | 35 HP | 5 s (7 HP per second) | 25 |
| Heal teammate | 15 HP | 1.5 s (10 HP per second) | 2 |
| Revive teammate | 50 HP after the revive | - | 10 |

Healing stops if the user moves away, according to the in-game tutorial text. The game charges the durability once per action, as a fixed amount (read from the game code), so the uses per bag below assume one cost per use.

**Enox.** Gives 40 HP as decaying health, which is health above the normal 100 that fades over time. The pool holds 40 HP. It fades 5 HP every 5 s until the pool is empty, so a full pool is gone after 40 s (read from the game code).

**Adrenaline Pen.** Gives no healing. It gives unlimited tactical sprint stamina for 60 seconds and reduces the equipment weight class of what you carry. The item can be used on yourself in 2 s, and a teammate use takes 1.3 s. A teammate who is alive gets the same 60 s unlimited tactical sprint.

**Defibrillator.** Revives a downed teammate to 35 HP at once. It needs a battery: one discharge uses 25 battery charges, and the charge-up takes 4 s. It cannot be used while you yourself are downed. Batteries are in [Utility Items](utility-items.md).

**Emergency Resuscitator and Field Resuscitator.** Revive a downed teammate to 10 HP. The shop text says each is a single-use item, and the Emergency Resuscitator is limited to one per life. The use animation is 2.2 s, and the revive is applied once at its end, so the use takes about 4 s (derived).

### Downed and revive

When a player's health reaches zero, they go critical. If nobody revives them, they bleed out and respawn at headquarters.

- The bleed-out timer starts at 360 s. In the normal critical state it drains at half speed, so a full timer lasts about 720 s (derived from the player defaults).
- A player who gives up drains the timer at 240 times speed, so it ends in about 1.5 s.
- A player who was revived and goes down again starts with at least 30 s.
- A base revive with bare hands holds for 20 s and gives the teammate 10 HP. Medic skills can shorten it.
- A critical player can be dragged by a friend, according to the tutorial text.

Max health is 100 HP. No natural health regeneration for infantry was found in the game code outside the Deathmatch mode, so healing comes from these items and from revives.

### Medic skills

The Medic skill tree changes some of these numbers. Four skills have values in the data, covering three effects:

- **Medkits have more uses.** The bag's usage rate multiplier drops from 1.0 to 0.6 as the skill levels up. The game code never reads it, so it does not appear to change the bag's durability cost.
- **Medical item swap speed.** Switching to a medical item gets faster, with the equip speed multiplied by 1.2 or 1.4 at the higher levels. It covers the items tagged as medical, all of the list above except the Enox.
- **Revive sprint boost.** After a revive, the reviver and the revived teammate each get a sprint and tactical sprint boost, at 1.2 or 1.4 times speed, for 5 s.

The other Medic skills, such as faster healing and a longer bleed-out timer, have a description in the skill tree but no number in the game files, and no game code reads them, so their effect is not known.

With the fixed durability costs, the bag gives the same counts at every skill level: 6 self heals, 75 teammate heals or 15 revives (derived from the 150 durability and the cost per action).

## Use and timing

Times are the length of each item's use animation, taken from the data.

| Item | On yourself | On a teammate | Notes |
|---|---:|---:|---|
| Bandage | 5.2 s | 4.8 s | |
| Individual First Aid Kit | 5.2 s (heals at 4.7 s) | 5.2 s (heals at 5.2 s) | Heal lands near the end of the use |
| Medical Bag | 5 s heal | 1.5 s heal | Runs until the target is full or the bag is empty |
| Enox | 2.2 s | not used on teammates | |
| Adrenaline Pen | 2.0 s | 1.3 s | |
| Defibrillator | 4 s charge | used to revive | Needs a battery |
| Emergency and Field Resuscitator | 2.2 s animation, one revive | | About 4 s in total, derived |

While a bandage, First Aid Kit, Medical Bag, Adrenaline Pen or resuscitator is in use, maximum movement speed is halved, according to the data.

## Cost

The shop price of each item is in the Overview table. The Season 2 Item Shop changed two of them, as listed below. The Emergency Resuscitator has a shop price of 0 in the data, and its item text says it is limited to one per life.

## Season 2 changes

| Item | Season 1 | Season 2 |
|---|---:|---:|
| Medical Bag price | 2,000 | 1,800 |
| Field Resuscitator price | 500 | 425 |

No change to healing amounts, use times or the downed rules is listed in the Season 2 Items data.

## See also

- [Body Armor](body-armor.md)
- [Utility Items](utility-items.md), for the batteries that power the Defibrillator
- [Progression and Economy](../../game-features/Wardogs_Progression_v1.md), for the Medic skill tables
- [Downed and Revive](../game-mechanics/downed-and-revive.md)

## Sources

- [Medical and Healing](../../game-features/Wardogs_Medical_v1.md): use times, amounts, durability, downed and revive values
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, shop text and unlock limits
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the use actions each item has
- [GameplayEffect values](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/ge-values.json): what the use effects change
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): prices
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay and armour values
