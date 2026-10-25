---
title: Enox
parent: "Equipment"
group: "Medical"
description: "A self-only item that gives 40 HP as decaying health, above your normal maximum, which fades over time."
---

# Enox

| Enox | |
|---|---|
| **General** | |
| Type | Medical, equipment |
| Uses | One use per item |
| **Effect** | |
| Heals | 40 HP as decaying health |
| Use time | 2.2 s |
| Effects while using | None listed in the data |
| **Availability** | |
| Price | 450 cash (marked hidden in the shop data) |
| Unlock level | 0 (shop data) |
| **Data** | |
| Internal name | `ID.Item.Enox.Standard` |
{: .wiki-infobox }

The Enox is a self-only item that gives 40 HP of decaying health. Decaying health is health above your normal 100 max that fades back over time, so the Enox does not give a permanent heal. The shop lists it as a consumable that grants decaying health.

## Overview

The Enox is in the Medical category but is listed under Equipment in the shop. The shop data marks its price as hidden. It can be used only on yourself.

## Effects

- **Healing:** +40 HP as decaying health. The decay pool holds up to 40 HP above the normal maximum. Healing is capped at the maximum plus the decay pool.
- **Fading:** the decaying health fades over time, and damage taken also lowers it (a static reading of the game code). Every 5 s the fade removes 5 HP, or what is left of the pool, until the pool is empty. A full 40 HP pool is therefore gone after 40 s (read from the game code).
- **Movement:** the data lists no movement slow for the Enox.
- **Bleeding:** the Enox does not stop bleeding. The game has no damage-over-time bleeding to cure.

### Medic skills

The "Self-healing speed" skill is described as applying to all medical items. No number for them exists in the game files, and no game code reads them, so its effect on the Enox is not known. The item-switch skill does not cover the Enox.

## Use and timing

The use animation lasts 2.2 s on yourself. You must be Injured and alive to use it. There is no teammate use in the data.

## Cost

The Item Shop lists the Enox at 450 cash. The shop data marks this item as hidden.

## Season 2 changes

No Season 2 change to the Enox is listed in the data.

## See also

- [Medical Items](medical-items.md)
- [Bandage](bandage.md), for a heal that stays as permanent health
- [Individual First Aid Kit](individual-first-aid-kit.md)

## Sources

- [Medical and Healing](../../game-features/Wardogs_Medical_v1.md): the decay pool, use time and healing amount
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, shop text, hidden flag
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the self-use action and its animation
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): checked for changes
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): the Medical category label
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay and armour values
