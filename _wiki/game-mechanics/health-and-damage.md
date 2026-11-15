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
| Friendly fire | Bullet damage to a teammate is halved; Large Hammer damage to a teammate is cut by 70 % |
| Health regeneration | None outside Deathmatch (none found in the game code; see [Downed and Revive](downed-and-revive.md)). Deathmatch: 5 health per tick after 10 s without damage |
{: .wiki-infobox }

Every infantry player starts with 100 HP. A hit takes health off that total, and the amount depends on the weapon and ammo, the part of the body that was hit, any armor covering that part, and how far the bullet travelled. This article covers the body parts. [Armor](armor.md), [Ballistics](ballistics.md) and [Penetration and Ricochet](penetration-and-ricochet.md) cover the other factors.

## Overview

A player can be hit in twelve places: the head, neck, three parts of the torso (upper, middle and lower), the pelvis, the upper and lower arm, the hand, the thigh, the calf and the foot. The head is the most dangerous place to be hit, and the hands and feet are the least. Damage is worked out per hit, so every bullet is its own calculation.

## How it works

1. The game finds which body parts the bullet's path passes through. A hit on the chest counts as an upper-torso hit, a hit on the forearm as a lower-arm hit, and so on. If the path crosses more than one part, the damage is worked out for each and the highest result counts (see [Hit Registration](hit-registration.md)).
2. Each body part has a base multiplier, and each weapon class adds its own multiplier for that part. The two multiply together.
3. Armor covering that body part reduces the result (see [Armor](armor.md)).
4. The remaining damage comes off health. When health reaches zero the player is downed (see [Downed and Revive](downed-and-revive.md)).

Friendly fire is part of the same system. A bullet that hits a teammate does half the damage it would otherwise do, and a Large Hammer hit on a teammate does 30 % of its damage. The damage tables give no friendly-fire reduction to explosives or fire, so a teammate's grenade, mine, C4 or Molotov fire is not reduced there.

A bullet also does less damage once it has slowed. Its speed is compared with a reference speed for the weapon, and the damage is scaled by the ratio (see [Ballistics](ballistics.md)).

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

Head multiplier added by each weapon class: assault rifles 2.35, SMGs 2.1, LMGs 2.35, shotguns 1.5, DMRs 3.00 and sniper rifles about 4.27.

**Arm damage class.** Each bullet also has an arm damage class, set by its caliber. It belongs to the bullet, not to the armour the target wears.

- **Small:** 9 mm, .45 ACP, .45 Colt, 7 mm buckshot and 12 gauge rifled slug.
- **Medium:** 5.45 mm and 5.56 mm.
- **High:** the 7.62 family (7.62x39, 7.62x51, 7.62x54R), .308, .338 Norma Magnum, .50 AE, 30 mm, and the combat and explosive arrows.
- **Special:** .50 Cal.

Damage per hit with the M4 (full metal jacket ammo, no armor) and the number of hits that kill an unarmored player:

| Body part | Damage per hit | Hits to kill |
|---|---:|---:|
| Head | 65.8 | 2 |
| Neck | 49.4 | 3 |
| Upper torso | 30.8 | 4 |
| Middle torso | 28.0 | 4 |
| Lower torso | 26.6 | 4 |
| Pelvis | 25.2 | 4 |
| Upper arm | 15.1 | 7 |
| Lower arm | 12.6 | 8 |
| Hand | 7.6 | 14 |
| Thigh | 15.1 | 7 |
| Calf | 12.6 | 8 |
| Foot | 7.6 | 14 |

These are point-blank model results using S3 multipliers and the M4's base damage with the historical damage formula: hostile target, outside a vehicle, no penetration or falloff. Current native damage behavior has not been verified. The full table for every weapon and ammo type is on [Damage by Weapon and Ammo](../../game-features/Wardogs_WeaponDamage_v1.md).

The same bullet does different damage to different weapons. A sniper rifle such as the MK22 does 118.8 to the upper torso and 192.0 to the head, so one hit kills an unarmored player in either place. A pistol such as the GGX 17 does 25.4 to the upper torso and 46.2 to the head, so it takes four body shots or three headshots.

## Rules that depend on the weapon or the round

Besides the body-part multiplier, the damage table has rules that match a weapon type, a round or an explosive. They multiply with everything else. The weapon/caliber factors below are current S3 stored values; the remaining rules describe the historical damage model.

- **Weapon type and round.** Assault rifles do x0.75 with .308 Winchester (FAL) and x0.88 with 7.62x39 mm (TCX-SPR). Marksman rifles do x0.91 with .308 Winchester (BMR-308, M14) and x0.90 with 7.62x54R (SVD), up from x0.85 and x0.80 respectively in Season 2. Machine guns do x0.75 with 7.62x54R (PKM) and .308 Winchester (Evo-3 Ultra). All other weapons are x1.00. The weapon articles already include this.
- **Autocannons.** The Flakpanzer Gepard's 35 mm and the 20 mm cannon of the Vanguard CIWS and other stationary guns do x0.70 to a player on any body part.
- **Outer blast ring.** An explosion's outer ring does x0.50 for the 84, 93, 120, 125 and 40 mm weapons (RPG-7, MAAWS, the L2A6 and T-72B3 guns, the MGL-40) and x0.45 for the 155 mm shell, on top of the distance falloff. The 40 mm grenade and the 125 mm shell gained this in Season 2. Inside the inner ring the rule does not apply. C4 has x0.60 in its outer ring.
- **Rifled slug and arrows.** The 12 gauge rifled slug does x0.70 on a body part covered by a vest. Compound Bow arrows do x0.90 against Heavy gear and x0.66 against Super heavy gear. See [Armor](armor.md).
- **.50 cal.** AMR 50 and M2 Browning hits do x0.84 to the head and neck, x0.875 to the upper torso and about x0.87 to the middle and lower torso, before armor.
- **Molotov.** Fire does x0.70 against a Super heavy vest.

## Tips that follow from the numbers

- **Aim high.** With the M4, two headshots kill an unarmored player, while four torso hits are needed. Head and neck hits matter most.
- **Limbs are a poor target.** Hands and feet take 14 hits from an M4, and arms and legs 7 to 8 hits.
- **Armor changes the count.** Covering the torso with heavy armor raises the modeled M4 upper-torso hits to kill from 4 to 7. See [Armor](armor.md) for the full effect.
- **Teammates are not a safe target.** Bullets that hit a teammate do half damage, so friendly fire still hurts, just less.

## See also

- [Armor](armor.md)
- [Ballistics](ballistics.md)
- [Penetration and Ricochet](penetration-and-ricochet.md)
- [Downed and Revive](downed-and-revive.md)
- [Hit Registration](hit-registration.md)
- [Body armor](../equipment/body-armor.md)
- [Medical Items](../equipment/medical-items.md)

## Season 3 announcement

Compared with Season 2, assault rifles and LMGs gain 13% upper-torso damage and 3% middle- and lower-torso damage. AR torso damage returns to Season 1 values; LMG torso damage matches ARs. The change applies to armored and unarmored targets, with the armor reduction percentage unchanged.

The announced DMR bounds are: unarmored body kills take 2 shots instead of 3; unhelmeted head kills take 1 instead of 2. SVD, BMR-308 and M14 require 1–2 fewer body shots at every armor level and 2 headshots instead of 3 through a level 3 helmet. SKS requires 1 fewer body shot against level 2 and level 4 armor. Neck damage increases but still takes 2 shots; arm and leg damage is unchanged. These are the announcement's bounds, not a guarantee for every ammunition, range, penetration or hit-location combination.

Source: [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221). These are developer-announced changes; saved fields and historical models below do not independently verify the current binary consumer.

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the friendly-fire rule in the damage tables (only bullets and the Large Hammer are reduced)
- [Damage by Weapon and Ammo](../../game-features/Wardogs_WeaponDamage_v1.md)
- [Damage rules](../../pipelines/Wardogs_DamagePipeline_v2.md) (body-part multipliers and friendly fire)
- [Round 41 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-weapons.md): the body parts crossed by one bullet and the faction rule
- [Game Mechanics Reference](../../content/Wardogs_GameMechanics_v2.md) (hit-location table)
- [Weapon damage by location (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json)
- [Infantry hitboxes (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/infantry-hitboxes.json)
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay, armour and critical state values
