---
title: "Health and Damage"
parent: "Game Mechanics"
description: "How much health a player has, which body parts count for more, and how many hits it takes to go down."
---

# Health and Damage

| Health and damage | |
|---|---|
| Max health | 100 HP |
| Hit locations | 12 body parts |
| Friendly fire | Bullet damage to a teammate or to yourself is halved |
| Health regeneration | No natural regeneration found in the data (see [Downed and Revive](downed-and-revive.md)) |
{: .wiki-infobox }

Every infantry player starts with 100 HP. A hit takes health off that total, and the amount depends on the weapon and ammo, the part of the body that was hit, any armor covering that part, and how far the bullet travelled. This article covers the body parts. [Armor](armor.md), [Ballistics](ballistics.md) and [Penetration and Ricochet](penetration-and-ricochet.md) cover the other factors.

## Overview

A player can be hit in twelve places: the head, neck, three parts of the torso (upper, middle and lower), the pelvis, the upper and lower arm, the hand, the thigh, the calf and the foot. The head is the most dangerous place to be hit, and the hands and feet are the least. Damage is worked out per hit, so every bullet is its own calculation.

## How it works

1. The game finds which body part the bullet touched. A hit on the chest counts as an upper-torso hit, a hit on the forearm as a lower-arm hit, and so on.
2. Each body part has a base multiplier, and each weapon class adds its own multiplier for that part. The two multiply together.
3. Armor covering that body part reduces the result (see [Armor](armor.md)).
4. The remaining damage comes off health. When health reaches zero the player is downed (see [Downed and Revive](downed-and-revive.md)).

Friendly fire is part of the same system. A bullet that hits a teammate, or the shooter, does half the damage it would otherwise do.

## Numbers

Base multiplier per body part, before the weapon class is added:

| Body part | Multiplier |
|---|---:|
| Head | 1.00 |
| Neck | 0.75 |
| Upper torso | 1.10 |
| Middle torso | 1.00 |
| Lower torso | 0.95 |
| Pelvis | 0.90 |
| Upper arm | 0.60 |
| Lower arm | 0.50 |
| Hand | 0.30 |
| Thigh | 0.60 |
| Calf | 0.50 |
| Foot | 0.30 |

Head multiplier added by each weapon class: assault rifles 2.35, SMGs 2.1, LMGs 2.35, shotguns 1.5, DMRs 2.45 and sniper rifles about 4.27.

Damage per hit with the M4 (full metal jacket ammo, no armor) and the number of hits that kill an unarmored player:

| Body part | Damage per hit | Hits to kill |
|---|---:|---:|
| Head | 65.8 | 2 |
| Neck | 49.4 | 3 |
| Upper torso | 27.3 | 4 |
| Middle torso | 27.2 | 4 |
| Lower torso | 25.8 | 4 |
| Pelvis | 25.2 | 4 |
| Upper arm | 15.1 | 7 |
| Lower arm | 12.6 | 8 |
| Hand | 7.6 | 14 |
| Thigh | 15.1 | 7 |
| Calf | 12.6 | 8 |
| Foot | 7.6 | 14 |

These values are calculated from the game's multipliers and the M4's base damage. The full table for every weapon and ammo type is on [Damage by Weapon and Ammo](../../game-features/Wardogs_WeaponDamage_v1.md).

The same bullet does different damage to different weapons. A sniper rifle such as the MK22 does 118.8 to the upper torso and 192.0 to the head, so one hit kills an unarmored player in either place. A pistol such as the GGX 17 does 25.4 to the upper torso and 46.2 to the head, so it takes four body shots or three headshots.

## Tips that follow from the numbers

- **Aim high.** With the M4, two headshots kill an unarmored player, while four torso hits are needed. Head and neck hits matter most.
- **Limbs are a poor target.** Hands and feet take 14 hits from an M4, and arms and legs 7 to 8 hits.
- **Armor changes the count.** Covering the torso with heavy armor raises the M4 torso hits to kill from 4 to 8. See [Armor](armor.md) for the full effect.
- **Teammates are not a safe target.** Bullets that hit a teammate do half damage, so friendly fire still hurts, just less.

## See also

- [Armor](armor.md)
- [Ballistics](ballistics.md)
- [Penetration and Ricochet](penetration-and-ricochet.md)
- [Downed and Revive](downed-and-revive.md)
- [Hit Registration](hit-registration.md)

## Sources

- [Damage by Weapon and Ammo](../../game-features/Wardogs_WeaponDamage_v1.md)
- [Damage rules](../../pipelines/Wardogs_DamagePipeline_v2.md) (body-part multipliers and friendly fire)
- [Game Mechanics Reference](../../content/Wardogs_GameMechanics_v2.md) (hit-location table)
- [Weapon damage by location (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json)
- [Infantry hitboxes (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/infantry-hitboxes.json)
