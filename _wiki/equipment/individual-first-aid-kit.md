---
title: Individual First Aid Kit
parent: "Equipment"
group: "Medical"
description: "The largest single heal of the basic items: 100 HP per use, which returns a player on 100 max HP to full from any health."
---

# Individual First Aid Kit

| Individual First Aid Kit | |
|---|---|
| **General** | |
| Type | Medical, quick slot |
| Uses | One heal per item |
| **Effect** | |
| Heals | 100 HP (back to full from any health at 100 max HP) |
| Use time | 5.2 s on yourself (heal at 4.7 s); 5.2 s on a teammate (heal at 5.2 s) |
| Effects while using | Maximum movement speed halved |
| **Availability** | |
| Price | 800 cash |
| Unlock level | 1 (shop data) |
| **Data** | |
| Internal name | `Id.Item.SuperBandage` |
{: .wiki-infobox }

The Individual First Aid Kit is the strongest single heal among the basic medical items. It adds 100 HP in one use, so a player on 100 max HP is healed to full from any health. It can be used on yourself or on a teammate.

## Overview

The shop describes the kit as healing a teammate or yourself back to full health. The data gives it a heal of +100 HP, which reaches full from any health at 100 max HP.
## Effects

- **Healing:** +100 HP per use, added to current health and capped at the maximum. The data gives one heal per use. The game's own heal timing is shown in the use table below.
- **Movement:** while the kit is in use, maximum movement speed is halved, as with the Bandage.
- **Bleeding:** the kit does not stop bleeding. There is no damage-over-time bleeding in the game to cure, see [Medical Items](medical-items.md).

### Medic skills

The "Self-healing speed" and "Teammate healing speed" skills are described as applying to all medical items. No number for them exists in the game files, and no game code reads them, so the effect on the kit's use time is not known.

The "Item-switch speed (Medical Archetype)" skill makes switching to a medical item faster, with an equip speed multiplier of 1.2 at skill level 2 and 1.4 at level 4.

## Use and timing

| Use | Use animation | Heal lands |
|---|---:|---:|
| On yourself | 5.2 s | at 4.7 s |
| On a teammate | 5.2 s | at 5.2 s |

The times come from the use animation in the data. The heal lands near the end of the animation. For yourself you must be Injured and alive. For a teammate, the teammate must be Injured and alive. The kit blocks and is blocked by the Bandage use, and starting a use cancels sprint and tactical sprint.

## Cost

The Item Shop lists the kit at 800 cash. No Season 2 change to its price is listed.

## Season 2 changes

No Season 2 change to the kit is listed in the data.

## See also

- [Bandage](bandage.md), the cheaper heal of 35 HP
- [Medical Items](medical-items.md)
- [Downed and Revive](../game-mechanics/downed-and-revive.md)

## Sources

- [Medical and Healing](../../game-features/Wardogs_Medical_v1.md): heal amount, heal timing, movement effect
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, shop text, unlock level
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): use actions and animation times
- [GameplayEffect values](../../pipelines/Wardogs_GameplayEffect_Values_v1.md): the movement effect
- [Progression Tables](../../game-features/Wardogs_Progression_v1.md): Medic skills
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): the Medical category label
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): checked for changes
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay and armour values
