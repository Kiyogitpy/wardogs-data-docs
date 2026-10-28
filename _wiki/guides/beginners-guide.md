---
title: "Beginner's Guide"
parent: "Guides"
description: "The basics every new player needs: health, where hits count most, which ammo to load for each armor class, how healing and reviving work, and how to aim and move."
---

# Beginner's Guide

This guide covers the basics of combat in Wardogs, with every number taken from the game. It is a starting point. Each section links to the article that explains the rule in full.

## 1. Health

Every player starts with 100 HP. The health you lose depends on the part of the body you are hit in, the weapon, the ammo and the armor. Hits to kill an unarmored player with the M4 rifle:

| Body part | Hits to kill |
|---|---:|
| Head | 2 |
| Neck | 3 |
| Upper, middle or lower torso, pelvis | 4 |
| Upper arm, thigh | 7 |
| Lower arm, calf | 8 |
| Hand, foot | 14 |

A headshot is the fastest kill, and limb hits are the slowest. Full details are in [Health and Damage](../game-mechanics/health-and-damage.md).

## 2. Where damage counts

- **The head is the most dangerous place to be hit.** The M4 does 65.8 to the head and 27.3 to the upper torso.
- **Sniper rifles can kill in one shot.** The MK22 does 118.8 to the upper torso and 192.0 to the head, which is enough to kill an unarmored player in either place.
- **Arms and legs count the least.** An M4 hit to a hand does 7.6.

## 3. Armor and which ammo to load

Vests cover the torso and helmets cover the head. Only the top-tier vest also covers the pelvis and upper arm, and only the heavier helmets cover the neck. Lower arms, hands, thighs, calves and feet are never covered by armor.

| Vest or helmet | Reduction | Damage reduced at |
|---|---:|---|
| Light | 30% | Vest: torso. Helmet: head |
| Medium | 40% | Vest: torso. Helmet: head |
| Heavy | 50% | Vest: torso. Helmet: head and neck |
| Super heavy | 60% | Vest: torso, pelvis, upper arm. Helmet: head and neck |

Choose ammo to match what the enemy wears:

- **No armor:** hollow point. It does about twice the damage of full metal jacket.
- **Light armor:** full metal jacket. Hollow point loses most of its damage.
- **Heavy or Super heavy armor:** armor-piercing does clearly more damage than full metal jacket with rifles. Against Medium armor the gap is small (16.6 against 16.4 on a Medium vest).

The full comparison is in [Choosing Ammo](choosing-ammo.md) and [Armor](../game-mechanics/armor.md).

## 4. Healing and reviving

- **Bandage:** +35 HP, about 5 seconds to use.
- **Individual First Aid Kit:** +100 HP, about 5 seconds to use.
- **Medical Bag:** heals 35 HP over 5 seconds on yourself, or 15 HP over 1.5 seconds on a teammate.
- **Health does not regenerate on its own.** No natural healing for infantry was found in the game code outside the Deathmatch mode.
- **At 0 HP you are downed.** You have 360 seconds on the bleed-out timer, which drains at half speed, so about 12 minutes in total (derived from the player defaults). A teammate can revive you by holding for 20 seconds with no equipment, and you come back at 10 HP.
- **Defibrillator:** revives a teammate to 35 HP after a 4 second charge, once it has a battery. You cannot use it while you are downed yourself.
- **Giving up** ends the wait in 1.5 seconds. Use it only when no help is coming.

See [Downed and Revive](../game-mechanics/downed-and-revive.md) for every item and its numbers.

## 5. Aiming and moving

- **Aiming down the sights removes hip spread completely.** Shots fired from the hip are spread at random. An assault rifle's hip spread runs from 3 degrees standing still to 6 degrees at full speed, 2 to 4 crouched and 1.5 to 3 prone. Sniper rifles spread 4 to 7 degrees standing.
- **Stand still and crouch to shoot more accurately.** Standing still reduces hip spread compared with moving, and crouching or going prone reduces it further.
- **Aiming down the sights halves your movement speed.** Plan to aim when you have stopped.
- **Walking speed:** 4.3 m/s standing, 2.7 m/s crouched, and 0.8 m/s prone. A standing sprint is 6.1 m/s.
- **Using a medical item also halves your speed** while you use it.

For the full spread and movement rules, see [Spread and Recoil](../game-mechanics/spread-and-recoil.md) and [Movement](../game-mechanics/movement.md).

## 6. Teammates

Bullets that hit a teammate do half damage. Friendly fire still costs health, so take care with your line of fire.

## 7. Where to go next

- **Money:** [Making Money](making-money.md) explains how cash comes in and what it buys.
- **Base:** [Building a Base](building-guide.md) covers the Forward Operating Base and the buildables you place in it.
- **Vehicles:** the [Vehicle Guide](vehicle-guide.md) compares every vehicle by role and shows how to keep one alive and fuelled.
- **Missions against AI:** the [PvE Guide](pve-guide.md) covers the three PvE missions and the soldiers you fight in them.

## What is not yet known

- How the game settles a hit when the shooter and target see it differently.
- The payout for each kind of spotted target is in the spotting challenge rows.
- The real revive time of a resuscitator, which is about 4 s by derivation from the item stats.

## See also

- [Health and Damage](../game-mechanics/health-and-damage.md)
- [Armor](../game-mechanics/armor.md)
- [Choosing Ammo](choosing-ammo.md)
- [Downed and Revive](../game-mechanics/downed-and-revive.md)
- [Medical Items](../equipment/medical-items.md)
- [Weapons](../weapons.md)
- [Body armor](../equipment/body-armor.md)
- [Vehicles](../vehicles.md)
- [Vehicle Guide](vehicle-guide.md)
- [PvE Guide](pve-guide.md)

## Sources

- [Damage by Weapon and Ammo](../../game-features/Wardogs_WeaponDamage_v1.md)
- [Medical and Healing](../../game-features/Wardogs_Medical_v1.md)
- [Player Movement Numbers](../../content/Wardogs_PlayerMovement_v1.md)
- [Weapon Spread, Accuracy and Shot Direction](../../pipelines/Wardogs_WeaponSpread_v1.md)
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay, armour and critical state values
- [Round 42 economy and buildables evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): spotting reward rows (P29, P30)
