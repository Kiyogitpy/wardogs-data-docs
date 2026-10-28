---
title: "M249 SAW"
parent: "Weapons"
group: "Light machine guns"
description: "The M249 SAW light machine gun: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# M249 SAW

| M249 SAW | |
|---|---|
| ![M249 SAW]({{ '/assets/img/icons/vendor-weapons/T_UI_Vendor_WEPN_009.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** |  |
| Class | Light machine gun |
| Caliber | [5.56x45mm](../ammunition/5-56x45mm.md) |
| Fire modes | Fully automatic and semi-automatic |
| **Performance** |  |
| Fire rate | 850 rounds/min |
| Muzzle velocity | 915 m/s |
| Effective range | 700 m |
| Standard magazine | M249 200 RND Box |
| **Availability** |  |
| Vendor price | 3200 |
| Unlock level | 1 |
| Internal name | M249 |
{: .wiki-infobox }

The M249 SAW is a [light machine gun](../weapons.md#light-machine-guns) in Wardogs, chambered in 5.56x45mm. It fires fully automatic and semi-automatic at 850 rounds/min. Its standard magazine is the M249 200 RND Box.

It takes the bullet types described on the [Ammunition](../ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 65.8 |
| Neck | 49.4 |
| Upper torso | 27.3 |
| Middle torso | 27.2 |
| Upper arm | 15.1 |
| Thigh | 15.1 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 27.3 | 65.8 |
| Light | 19.1 | 46.1 |
| Medium | 16.4 | 39.5 |
| Heavy | 13.6 | 32.9 |
| Super heavy | 10.9 | 26.3 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 27.3 |
| 50 m | 27.3 |
| 100 m | 27.3 |
| 200 m | 27.3 |
| 300 m | 27.3 |
| 400 m | 27.3 |
| 600 m | 27.3 |
| 800 m | 21.7 |
| 1000 m | 12.0 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 27.3 |
| Flesh Damage (HP) | 54.5 |
| Armor Piercing (AP) | 21.8 |

See [Ammunition](../ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Time to kill

Shots and time to kill (TTK) against a character with 100 HP. TTK runs from the first shot to the killing shot, so it is (shots - 1) x 60 / fire rate: one shot kills in 0 s.

**Upper torso hits, Standard (FMJ)**

| Vest | 10 m | 100 m | 300 m |
|---|---|---|---|
| No armor | 4 shots, 0.21 s | 4 shots, 0.21 s | 4 shots, 0.21 s |
| [Level 1 vest](../equipment/level-1-armor.md) | 6 shots, 0.35 s | 6 shots, 0.35 s | 6 shots, 0.35 s |
| [Level 2 vest](../equipment/level-2-armor.md) | 7 shots, 0.42 s | 7 shots, 0.42 s | 7 shots, 0.42 s |
| [Level 3 vest](../equipment/level-3-armor.md) | 8 shots, 0.49 s | 8 shots, 0.49 s | 8 shots, 0.49 s |
| [Level 4 vest](../equipment/level-4-armor.md) | 10 shots, 0.64 s | 10 shots, 0.64 s | 10 shots, 0.64 s |

**Head hits, Standard (FMJ)**

- At 10 m, no helmet: 2 shots, 0.07 s; Level 1 helmet: 3 shots, 0.14 s; Level 2 helmet: 3 shots, 0.14 s; Level 3 helmet: 4 shots, 0.21 s; Level 4 helmet: 4 shots, 0.21 s.
- At 100 m, no helmet: 2 shots, 0.07 s; Level 1 helmet: 3 shots, 0.14 s; Level 2 helmet: 3 shots, 0.14 s; Level 3 helmet: 4 shots, 0.21 s; Level 4 helmet: 4 shots, 0.21 s.

**Upper torso hits, Armor Piercing (AP)**

| Vest | 10 m | 100 m | 300 m |
|---|---|---|---|
| No armor | 5 shots, 0.28 s | 5 shots, 0.28 s | 5 shots, 0.28 s |
| [Level 1 vest](../equipment/level-1-armor.md) | 6 shots, 0.35 s | 6 shots, 0.35 s | 6 shots, 0.35 s |
| [Level 2 vest](../equipment/level-2-armor.md) | 7 shots, 0.42 s | 7 shots, 0.42 s | 7 shots, 0.42 s |
| [Level 3 vest](../equipment/level-3-armor.md) | 7 shots, 0.42 s | 7 shots, 0.42 s | 7 shots, 0.42 s |
| [Level 4 vest](../equipment/level-4-armor.md) | 8 shots, 0.49 s | 8 shots, 0.49 s | 8 shots, 0.49 s |

**Head hits, Armor Piercing (AP)**

- At 10 m, no helmet: 2 shots, 0.07 s; Level 1 helmet: 3 shots, 0.14 s; Level 2 helmet: 3 shots, 0.14 s; Level 3 helmet: 3 shots, 0.14 s; Level 4 helmet: 3 shots, 0.14 s.
- At 100 m, no helmet: 2 shots, 0.07 s; Level 1 helmet: 3 shots, 0.14 s; Level 2 helmet: 3 shots, 0.14 s; Level 3 helmet: 3 shots, 0.14 s; Level 4 helmet: 3 shots, 0.14 s.

Derived from the game data, not from play testing. It assumes every shot hits the stated part and that armor stays intact, and it ignores reload time, spread and recoil, so real fights take longer. Damage after the first 10 m comes from the range falloff curve. A * marks a distance beyond the weapon's effective range of 700 m, where damage falls with distance.

## Recoil and spread

Each bullet leaves the barrel in a random direction inside a cone around the point you aim at. Hip fire uses a wide cone that grows when you move. Aiming down the sights uses a very narrow one. Every shot also pushes the view up and to the side, following the weapon's recoil pattern.

**Spread**

| Situation | Still | Moving at full speed |
|---|---|---|
| Standing, hip fire | 3.0° | 6.0° |
| Crouching, hip fire | 2.0° | 4.0° |
| Prone, hip fire | 1.0° | 2.0° |
| In the air, hip fire | 10.0° | 10.0° |
| Aimed down sights | 0.1° | 0.1° |

Cone half-angles in degrees: a bullet can land up to that far from the aim point. At 100 m, standing hip fire has a radius of 5.2 m when still and 10.5 m at full speed; aimed, it is 0.22 m. Half of the shots land within half that radius.

Accuracy is 4.3 mrad, a full cone angle; the aimed row is half of it, in degrees.

- The data has no per-shot bloom and no recovery timer: nothing found in the spread data makes firing widen the spread, and spread changes only with speed, stance, being in the air and aiming. This comes from reading the game files, not from testing in game.
- Hip spread eases toward its new value with a time constant of about 0.04 s (a native default found by static reading).
- The 10° in-air figure is a native default found by static reading; only the grenade launcher's data sets it, to the same 10°.
- At full aim (aim blend exactly 1.0) hip spread is set to zero, so only the aimed row applies. A partly aimed weapon counts as hip fire.
- "Full speed" means 4 m/s standing, 2.5 m/s crouching and 0.5 m/s prone; between still and that speed the hip spread is a straight line.
- The figures are before attachments, which can change spread (see [Attachments](../attachments.md)).

**Recoil**

| Measure | Value |
|---|---|
| Shots in the recoil pattern | 7 |
| Kick on the first shot | 2.41° up |
| Climb after 10 shots | 16.1° up |
| Climb after 30 shots | 36.1° up |
| Average climb per shot over 30 shots | 1.20° up |
| Sideways drift after 30 shots | 1.5° left |
| Pattern resets after | 0.5 s without firing |
| Vertical kick crouching / prone, compared with standing | 0.60× / 0.35× |
| Default-loadout recoil multiplier, vertical / horizontal | 1.17 / 1.17 |

Climb and drift figures are computed from the pattern points, before the recoil multiplier. The game turns each authored kick by up to 20° per shot, so the real sideways drift varies from burst to burst. After shot 7 each kick is random inside the post-pattern range.

Season 2 did not change the recoil pattern.

To see the whole pattern as a picture, open the [Weapon Spray Viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/spray-viewer.html) and pick the M249 SAW in the viewer.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](../ammunition.md).

## Attachments

Slots on this weapon: Barrel, Grip, Magazine, Sight, Stock, Underbarrel. See [Attachments](../attachments.md) for what each part changes.

Default parts: magazine (M249 200 RND Box).

## Cost and unlocking

- Vendor price: 3200. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

- Suppression effect multiplier: none to 1.25

## See also

- [Weapons](../weapons.md)
- [Ammunition](../ammunition.md)
- [Attachments](../attachments.md)
- [Choosing Ammo](../guides/choosing-ammo.md)
- [Ballistics](../game-mechanics/ballistics.md)
- [Health and Damage](../game-mechanics/health-and-damage.md)
- [Spread and Recoil](../game-mechanics/spread-and-recoil.md)

## Sources

- [Weapon Shop and Parts](../../game-features/Wardogs_WeaponShop_v1.md): price, unlock level, default magazine
- [Infantry Weapon Stats](../../content/Wardogs_InfantryWeapons_Stats_v1.md): fire rate and fire modes
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): body-part, armor and falloff numbers
- [Weapon Spread and Recoil Data](../../content/Wardogs_WeaponSpreadRecoilData_v1.md): spread and recoil inputs
- [Weapon Spread pipeline](../../pipelines/Wardogs_WeaponSpread_v1.md): how the aim cone and hip spread are computed
- [Spray Patterns Gallery](../../game-features/Wardogs_SprayPatterns_v1.md): recoil patterns, Season 1 and Season 2
- [weapon-spread-recoil.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-spread-recoil.json): accuracy and hip spread curves
- [spray-patterns.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/spray-patterns.json): recoil pattern points, Season 1 and Season 2
- [Season 2 Changes: Weapons & Ammo](../../season-2-changes/weapons-ammo.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): caliber and ammo names
- [weapon-loadouts.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-loadouts.json): names, slots and effects
- [weapon-damage.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage.json): body-part and armor damage
- [weapon-damage-falloff.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-falloff.json): falloff curves, also used for the time to kill table
- [weapon-capacity.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-capacity.json): muzzle speed, effective range, chamber and magazine
- [Round 39 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-weapons.md): launcher speeds and ranges, magazines, default rate
