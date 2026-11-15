---
title: Enox
parent: "Equipment"
group: "Medical"
description: "A self-only item that gives 40 HP as decaying health, above your normal maximum, which fades over time."
---

# Enox

| Enox | |
|---|---|
| ![Enox]({{ '/assets/img/icons/utility-3d/t_ui_icon_enox_512x512.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Medical, equipment |
| Uses | One use per item |
| **Effect** | |
| Heals | 40 HP as decaying health |
| Use time | 2.2 s |
| Effects while using | None listed |
| **Availability** | |
| Price | 450 cash (marked hidden in the shop data) |
| Unlock level | 0 (shop data) |
| **Data** | |
| Internal name | `ID.Item.Enox.Standard` |
{: .wiki-infobox }

The Enox stores a self-use amount of 40. In the historical vitality model this becomes decaying health above a normal 100 HP maximum, rather than a permanent heal; the S3 vitality consumer has not been reverified. The shop lists it as a consumable that grants decaying health.

## Overview

The Enox is in the Medical category but is listed under Equipment in the shop. The shop marks its price as hidden. It can be used only on yourself.

## Effects

- **Healing:** +40 HP as decaying health. The historical vitality model caps the extra pool at 40 HP and healing at maximum health plus that pool; current S3 vitality limits are unverified.
- **Fading:** the decaying health fades over time, and damage taken also lowers it (a static reading of the game code). The CL516586-era round 40 trace removes up to 5 HP every 5 s, giving 40 s for a full 40 HP pool. That decay rate and pool limit are historical defaults, not reverified S3 native behavior.
- **Movement:** The current Enox appliable export lists no movement effect; that absence does not prove every S3 consumer leaves movement unchanged.
- **Bleeding:** No bleeding-cure effect is listed on this item. The cited CL516586-era search found the downed bleed-out timer, not a damage-over-time bleeding system; that negative search does not establish absence in S3.

### Medic skills

The "Self-healing speed" skill is described as applying to all medical items. The historical round 39 search found no magnitude or consumer for this skill; its S3 effect on Enox is unresolved. The item-switch skill does not cover the Enox.

## Use and timing

The historical use montage lasts about 2.2 s on yourself; current completion timing is unverified. You must be Injured and alive to use it. There is no teammate use.

## Cost

The Item Shop lists the Enox at 450 cash. The shop marks this item as hidden.

## Season 2 changes

No Season 2 change to the Enox is listed.

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
