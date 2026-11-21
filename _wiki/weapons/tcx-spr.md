---
title: "TCX-SPR"
parent: "Weapons"
group: "Assault rifles"
description: "The TCX-SPR assault rifle: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# TCX-SPR

| TCX-SPR | |
|---|---|
| ![TCX-SPR]({{ '/assets/img/icons/vendor-weapons/T_UI_Weapons_WEPN_037.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** |  |
| Class | Assault rifle |
| Caliber | [7.62x39mm](../ammunition/7-62x39mm.md) |
| Fire modes | Fully automatic and semi-automatic |
| **Performance** |  |
| Fire rate | 800 rounds/min |
| Muzzle velocity | 700 m/s |
| Effective range | 400 m |
| Standard magazine | TCX-SPR 28 RND Magazine |
| **Availability** |  |
| Vendor price | 3200 |
| Vendor level field | 1 |
| Stored role levels | Wardog 20 |
| Internal name | WEPN_037 |
{: .wiki-infobox }

The TCX-SPR is an [assault rifle](../weapons.md#assault-rifles) in Wardogs, chambered in 7.62x39mm. It fires fully automatic and semi-automatic at 800 rounds/min. Its standard magazine is the TCX-SPR 28 RND Magazine.

It takes the bullet types described on the [Ammunition](../ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Damage

These are S3-input model results using the earlier damage formula. Current native damage behavior has not been verified.

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 70.3 |
| Neck | 52.7 |
| Upper torso | 32.9 |
| Middle torso | 29.9 |
| Upper arm | 16.2 |
| Thigh | 16.2 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 32.9 | 70.3 |
| Light | 23.0 | 49.2 |
| Medium | 19.7 | 42.2 |
| Heavy | 16.5 | 35.2 |
| Super heavy | 13.2 | 28.1 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 32.9 |
| 50 m | 32.9 |
| 100 m | 32.9 |
| 200 m | 32.9 |
| 300 m | 32.9 |
| 400 m | 32.9 |
| 600 m | 22.3 |
| 800 m | 14.9 |
| 1000 m | 8.9 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 32.9 |
| Flesh Damage (HP) | 65.8 |
| Armor Piercing (AP) | 26.3 |

See [Ammunition](../ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Time to kill

Shots and time to kill (TTK) against a character with 100 HP. TTK runs from the first shot to the killing shot, so it is (shots - 1) x 60 / fire rate: one shot kills in 0 s.

**Upper torso hits, Standard (FMJ)**

| Vest | 10 m | 100 m | 300 m |
|---|---|---|---|
| No armor | 4 shots, 0.23 s | 4 shots, 0.23 s | 4 shots, 0.23 s |
| [Level 1 vest](../equipment/level-1-armor.md) | 5 shots, 0.30 s | 5 shots, 0.30 s | 5 shots, 0.30 s |
| [Level 2 vest](../equipment/level-2-armor.md) | 6 shots, 0.38 s | 6 shots, 0.38 s | 6 shots, 0.38 s |
| [Level 3 vest](../equipment/level-3-armor.md) | 7 shots, 0.45 s | 7 shots, 0.45 s | 7 shots, 0.45 s |
| [Level 4 vest](../equipment/level-4-armor.md) | 8 shots, 0.53 s | 8 shots, 0.53 s | 8 shots, 0.53 s |

**Head hits, Standard (FMJ)**

- At 10 m, no helmet: 2 shots, 0.07 s; Level 1 helmet: 3 shots, 0.15 s; Level 2 helmet: 3 shots, 0.15 s; Level 3 helmet: 3 shots, 0.15 s; Level 4 helmet: 4 shots, 0.23 s.
- At 100 m, no helmet: 2 shots, 0.07 s; Level 1 helmet: 3 shots, 0.15 s; Level 2 helmet: 3 shots, 0.15 s; Level 3 helmet: 3 shots, 0.15 s; Level 4 helmet: 4 shots, 0.23 s.

**Upper torso hits, Armor Piercing (AP)**

| Vest | 10 m | 100 m | 300 m |
|---|---|---|---|
| No armor | 4 shots, 0.23 s | 4 shots, 0.23 s | 4 shots, 0.23 s |
| [Level 1 vest](../equipment/level-1-armor.md) | 5 shots, 0.30 s | 5 shots, 0.30 s | 5 shots, 0.30 s |
| [Level 2 vest](../equipment/level-2-armor.md) | 5 shots, 0.30 s | 5 shots, 0.30 s | 5 shots, 0.30 s |
| [Level 3 vest](../equipment/level-3-armor.md) | 6 shots, 0.38 s | 6 shots, 0.38 s | 6 shots, 0.38 s |
| [Level 4 vest](../equipment/level-4-armor.md) | 6 shots, 0.38 s | 6 shots, 0.38 s | 6 shots, 0.38 s |

**Head hits, Armor Piercing (AP)**

- At 10 m, no helmet: 2 shots, 0.07 s; Level 1 helmet: 3 shots, 0.15 s; Level 2 helmet: 3 shots, 0.15 s; Level 3 helmet: 3 shots, 0.15 s; Level 4 helmet: 3 shots, 0.15 s.
- At 100 m, no helmet: 2 shots, 0.07 s; Level 1 helmet: 3 shots, 0.15 s; Level 2 helmet: 3 shots, 0.15 s; Level 3 helmet: 3 shots, 0.15 s; Level 4 helmet: 3 shots, 0.15 s.

Derived from the game data, not from play testing. It assumes every shot hits the stated part and that armor stays intact, and it ignores reload time, spread and recoil, so real fights take longer. Damage after the first 10 m comes from the range falloff curve. A * marks a distance beyond the effective-range model setting of 400 m, which may use a historical default when omitted. Damage falloff is calculated separately from its curve; the marker is not a damage cutoff.

## Recoil and spread

The recoil figures below use current S3 source settings with the historical calculation and omitted-field defaults; current native equivalence is unverified. Spread figures use the exported settings and historical calculation/default assumptions; current native spread behavior remains unverified.

Each bullet leaves the barrel in a random direction inside a cone around the point you aim at. Hip fire uses a wide cone that grows when you move. Aiming down the sights uses a very narrow one. Every shot also pushes the view up and to the side, following the weapon's recoil pattern.

**Spread**

| Situation | Still | Moving at full speed |
|---|---|---|
| Standing, hip fire | 3.0° | 6.0° |
| Crouching, hip fire | 2.0° | 4.0° |
| Prone, hip fire | 1.5° | 3.0° |
| In the air, hip fire | 10.0° | 10.0° |
| Aimed down sights | 0.0166° | 0.0166° |

Cone half-angles in degrees: a bullet can land up to that far from the aim point. At 100 m, standing hip fire has a radius of 5.2 m when still and 10.5 m at full speed; aimed, it is 0.03 m. Half of the shots land within half that radius.

Accuracy is 0.58 mrad, a full cone angle; the aimed row is half of it, in degrees.

- The historical spread model has no per-shot bloom or recovery timer. The earlier reader search does not establish their absence from S3.
- The model assumes the historical hip-spread easing time constant of about 0.04 s; the S3 default and consumer are unverified.
- The 10° in-air row uses the historical native default. An omitted S3 field does not verify that default.
- The historical model uses only aimed spread at full aim (blend exactly 1.0) and hip spread while partly aimed. The current branch has not been verified.
- In that model, "full speed" means 4 m/s standing, 2.5 m/s crouching and 0.5 m/s prone; interpolation is linear. These are historical model assumptions.
- The figures are before attachments, which can change spread (see [Attachments](../attachments.md)).

**S3-input recoil model**

| Measure | Value |
|---|---|
| Shots in the recoil pattern | 30 |
| Kick on the first shot | 0.85° up |
| Climb after 10 shots | 12.6° up |
| Climb after 30 shots | 36.2° up |
| Average climb per shot over 30 shots | 1.21° up |
| Sideways drift after 30 shots | 0.1° right |
| Pattern resets after | 0.5 s without firing |
| Vertical kick crouching / prone, compared with standing | 0.85× / 0.70× |
| Default-loadout recoil multiplier, vertical / horizontal | 1 / 1 |

Climb and drift figures are computed from the pattern points, before the recoil multiplier. The model turns each authored kick by up to 14° per shot, so its sideways drift varies from burst to burst. After shot 30 each kick is random inside the post-pattern range.

[Current recoil settings](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_037/Content/Data/DA_WEPN_037_Stats.json).

Archived Season 1 → 2 history (separate from the S3 model above): The Season 1 data has no entry for this weapon, so there is nothing to compare.

The [historical Weapon Spray Viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/spray-viewer.html) retains Season 1/2 data; it does not show this S3 snapshot.

The [official S3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) announce reduced TCX-SPR climb and drift, plus a fix for standing recoil being used while prone. These are developer-reported changes, distinct from the source-derived model above.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](../ammunition.md).

## Attachments

Slots on this weapon: Barrel, Grip, Handguard, Magazine, Sight, Stock, Underbarrel. See [Attachments](../attachments.md) for what each part changes.

Default parts: magazine (SIG Spear Standard Mag), grip (Sig Spear Standard Pistol Grip), stock (Sig Spear Standard Stock), barrel (Sig Spear Standard Barrel).

## Cost and unlocking

- Vendor price: 3200. The data pages do not decode the currency, so the price is shown as a plain number.
- Vendor level field: 1; this is distinct from role unlocking.
- Stored role levels: Wardog 20. These listed prerequisites do not establish every active mode/vendor gate.

## Season 2 changes

The Season 2 changes page lists no changes for this weapon.

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
- [Current role unlock nodes](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json): stored tree levels, separate from vendor level fields
- [Round 39 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-weapons.md): launcher speeds and ranges, magazines, default rate
