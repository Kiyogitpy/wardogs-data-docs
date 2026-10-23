# Round 24 weapon damage: independent verification

Verifier: teammate D. Subject: `assets/data/weapon-damage.json` (teammate A) and `assets/data/ammo-availability.json` (teammate B), checked at main 1e3ad86b.

## Method

`_tools/verify_weapon_damage.py` recomputes every published cell from the raw `data/` export. It does not import `weapon_damage_tables.py` or `damage_tables.py`, and shares no code with them. Inputs it reads itself:

- the 146 infantry rule entries in `DT_GlobalDamage_InfantryData.json` (selection by alignment, source tags, target tags and hit location as in DamagePipeline v2 section 4; entries with instigator requirements are skipped because none is supplied);
- the bone, archetype-caliber and ammo-effectiveness helper tables (sections 7.1 to 7.3);
- the armor reduction of each vest and helmet (`DamagePercentageReduction` of the first durability stage: 30, 40, 50, 60);
- each ammo item's `ItemId` tag, its projectile data asset (source tag, arms class context, `BaseDamage`, `NumberOfPellets`);
- each weapon's `DamageEntityData` tag and the `SupportedCaliber` list of its stats asset.

The modifier tag for each ammo item is rebuilt from the item tag with the fixed map of section 7.9. Arithmetic is the product of the matching factors, clamped at 0, in 64-bit floats.

Run it with `python _tools/verify_weapon_damage.py`. It prints PASS or FAIL per cell for a named sample, then runs the full sweep and the checks for claims (e), (g), (h) and the ammo file. Exit code 0 means everything passed.

## Result in one line

All 3072 published cells (33 weapons x their ammo rows x 6 locations + 5 torso armor classes + 5 head armor classes) agree with my recomputation. Maximum absolute difference on `damage_raw`: 1.14e-13 (floating point noise). Weapon tags, modifier tags, base damage and pellet counts also match. The circularity worry did not find a bug: A's shared logic is right for these cells.

## Compared cells (36 named, from the script)

Columns: my value, JSON `damage_raw`, difference, JSON rounded value.

| Weapon | Caliber | Ammo | Cell | Mine | JSON raw | Diff | JSON shown |
|---|---|---|---|---:|---:|---:|---:|
| M4 | 556mm | FMJ | Torso.Upper | 27.2580 | 27.2580 | 0 | 27.3 |
| M4 | 556mm | ArmorPiercing | Torso.Upper | 21.8064 | 21.8064 | 0 | 21.8 |
| M4 | 556mm | HollowPoint | Torso.Upper | 54.5160 | 54.5160 | 0 | 54.5 |
| M4 | 556mm | Tracer | Head | 65.8000 | 65.8000 | 0 | 65.8 |
| M4 | 556mm | HollowPoint | Torso, SuperHeavy | 1.4719 | 1.4719 | 2e-16 | 1.5 |
| M4 | 556mm | ArmorPiercing | Torso, Medium | 16.5729 | 16.5729 | 0 | 16.6 |
| M4 | 556mm | FMJ | Torso, Light | 19.0806 | 19.0806 | 4e-15 | 19.1 |
| M4 | 556mm | FMJ | Head, Heavy | 32.9000 | 32.9000 | 0 | 32.9 |
| M4 | 556mm | HollowPoint.Tracer | Head, SuperHeavy | 2.3688 | 2.3688 | 0 | 2.4 |
| M4 | 556mm | ArmorPiercing.Tracer | Head, Medium | 40.0064 | 40.0064 | 0 | 40.0 |
| AK74M | 545mm | FMJ | Neck | 45.8250 | 45.8250 | 0 | 45.8 |
| AK74M | 545mm | ArmorPiercing | Torso, Light | 16.6040 | 16.6040 | 0 | 16.6 |
| WEPN_030 | 308Win | FMJ | Torso.Upper | 32.8556 | 32.8556 | 0 | 32.9 |
| MK22 | 308Win | HollowPoint | Head | 384.0030 | 384.0030 | 0 | 384.0 |
| WEPN_037 | 762mm | ArmorPiercing | Torso, Medium | 18.6414 | 18.6414 | 0 | 18.6 |
| SKS | 762mm | HollowPoint | Head, Heavy | 7.4970 | 7.4970 | 0 | 7.5 |
| SVDM | 762x54mm | ArmorPiercing | Torso, Heavy | 24.8582 | 24.8582 | 4e-15 | 24.9 |
| WEPN_017 | 762x54mm | FMJ | Head, None | 187.7348 | 187.7348 | 0 | 187.7 |
| Glock17 | 9mm | FMJ | Arm.Upper | 17.1600 | 17.1600 | 0 | 17.2 |
| Glock17 | 9mm | ArmorPiercing | Torso, Medium | 14.6362 | 14.6362 | 2e-15 | 14.6 |
| Glock17 | 9mm | ArmorPiercing | Torso, Heavy | 13.2132 | 13.2132 | 4e-15 | 13.2 |
| WEPN_026 | 45ACP | FMJ | Torso.Upper | 45.0450 | 45.0450 | 0 | 45.0 |
| WEPN_026 | 45ACP | HollowPoint | Head, Light | 16.2162 | 16.2162 | 4e-15 | 16.2 |
| Judge | 45Colt | FMJ | Head | 94.5000 | 94.5000 | 0 | 94.5 |
| WEPN_027 | 50AE | ArmorPiercing | Torso, Heavy | 43.6590 | 43.6590 | 0 | 43.7 |
| WEPN_027 | 50AE | FMJ | Leg.Thigh | 49.1400 | 49.1400 | 0 | 49.1 |
| SR_04 | 50Cal | FMJ | Torso, Heavy | 93.5550 | 93.5550 | 1e-14 | 93.6 |
| SR_04 | 50Cal | ArmorPiercing | Torso, Heavy | 74.8440 | 74.8440 | 3e-14 | 74.8 |
| SR_04 | 50Cal | ArmorPiercing | Head, SuperHeavy | 66.3754 | 66.3754 | 0 | 66.4 |
| SR_04 | 50Cal | FMJ | Torso.Middle | 150.9633 | 150.9633 | 3e-14 | 151.0 |
| WEPN_035 | 556mm | FMJ | Torso.Upper | 73.9200 | 73.9200 | 0 | 73.9 |
| WEPN_035 | 556mm | ArmorPiercing | Head, Medium | 72.6363 | 72.6363 | 1e-14 | 72.6 |
| M500 | 12g / 7mmBuck pellet | Buckshot | Torso.Upper | 24.7500 | 24.7500 | 0 | 24.8 |
| M500 | 12g slug | Slug | Torso.Upper | 103.9500 | 103.9500 | 0 | 104.0 |
| M500 | 12g slug | Slug | Torso, Heavy | 36.3825 | 36.3825 | 0 | 36.4 |
| M500 | 7mmBuck pellet | Buckshot | Head, Medium | 15.7500 | 15.7500 | 4e-15 | 15.7 |

"Torso, X" means a Torso.Upper hit on a target wearing armor class X; "Head, X" means a Head hit with helmet class X. WEPN_035 torso value 73.92 is 28 x 2.64 as stated: 1.10 (universal Torso.Upper) x 2.4 (sniper row), unaffected by caliber because the sniper row holds 1.0 for 556mm.

## Claims

**(a) AP deals about 0.8x FMJ unarmored: CONFIRMED.** Entry 15 is a flat -20 percent on any bullet with the ArmorPiercing modifier. Ratio AP/FMJ unarmored is exactly 0.800 for all 31 weapons with AP rows (shotgun has none). M4: 21.8064 against 27.258.

**(b) AP overtakes FMJ at Medium and above for rifle and heavier calibers, at Heavy and above for pistol calibers: CONFIRMED with one exception that the claim should state.** From the full sweep, the first armor class where AP beats FMJ (torso and head identical):

| Group | First class where AP wins |
|---|---|
| 556mm, 545mm, 308Win, 762mm, 762x54mm | Medium (M4: 16.57 against 16.36, only 1.3 percent) |
| 50AE (Deagle, a pistol weapon) | Medium (ratio 1.067) |
| 9mm, 45ACP, 45Colt | Heavy (Glock17 Medium 0.96, Heavy 1.04) |
| 50Cal (SR_04) | never |

The wording "pistol calibers cross at Heavy" is wrong for the Deagle: its arms class is High (0.5), so it crosses at Medium like a rifle. The margin at Medium for rifles is tiny, so "overtakes at Medium" will read as a bigger effect than it is.

**(c) SR_04 AP never beats FMJ: CONFIRMED.** The 50Cal projectile carries `Meta.Damage.Arms.Special`, and the ArmorPiercing row maps Special to 1.0. The armor scalar is then identical to FMJ, so AP is FMJ x 0.8 in every cell (ratio 0.800 at None, Light, Medium, Heavy and SuperHeavy). SR_04 also gets entries 124 to 127 (50Cal head/neck -15.6, Torso.Upper -12.5, Torso.Middle/Lower -6.0 and -7.7 percent), which both A's engine and mine apply.

**(d) HollowPoint higher unarmored, collapses against armor: CONFIRMED.** M4 torso: 54.52 unarmored (x2.0 of FMJ, entry 18), 8.1 Light, 5.9 Medium, 3.7 Heavy, 1.47 SuperHeavy. HP is below FMJ at Light, Medium, Heavy and SuperHeavy for every weapon and on both torso and head. The cause is more than the 1.5 scalar: entries 21 and 133 (-55 and -40 percent against vests) and 20 and 134 (-70 and -40 percent against helmets) apply as well.

**(e) The `same_damage_as` groups: CONFIRMED, but the count is 21, not 22.** Groups: A91, KH2002, M249, M4, TAR21, WEPN_029, WEPN_033 (7); WEPN_030 and WEPN_036 (2); RFB and WEPN_034 (2); Glock17, MP9, SMG_03, WEPN_028, WEPN_031, WEPN_032 (6); M500 and MP43 (2); WEPN_017 and SV98 (2). That is 21 ids. Every `damage_raw` block, ammo row and base damage is identical inside each group, in every ammo row. The converse also holds: no two weapons have identical values without being listed together.

**(f) The 33-weapon set: CONFIRMED, one scope caveat.** I scanned every item definition that references a weapon stats asset: 40 items, 33 included, 7 excluded (ArtilleryBarrelTest 155mm, TankBarrelTest 120x570mm, CGM4 84mm, Launcher_04 72mm, MMGL 40mm, RPG7 93mm, CombatBow). The projectile source tags of the excluded calibers are `Meta.Damage.Explosive.Rocket.84mm/72mm/93mm/120mm/155mm` and `Meta.Damage.Explosive.Grenade.40mm`, so none is a bullet. CombatBow's caliber is `Item.Caliber.Arrow`, which has no bullet ammo. Fists, BuildTool and the three hammers have empty `SupportedCaliber`. GrenadeLauncher (40mm) and AT4 (84mm) stats assets are explosive. No weapon item fires a bullet caliber and is missing from the 33.

Caveat: the M2Browning stationary gun (762mm, stats asset only, no item definition), the MWSY_001 mounted gun (50Cal) and several vehicle machine guns (308Win in ROT_03, ROT_04, TNK_01, WHL_05) do fire bullet calibers that the engine could price against infantry. They are excluded as mounted weapons, which is a scope choice, not a data fact; the JSON states it.

**(g) .338 Norma AP carries no modifier, no weapon chambers .338: CONFIRMED.** The two AP items are `Id.Item.338Nor.ArmourPiercing` and `Id.Item.338Nor.ArmourPiercing.Tracer`. Neither resolves through the fixed map, so no modifier tag; HollowPoint, HollowPoint.Tracer and Tracer of the same caliber do resolve. None of the 82 `DA_*_Stats` assets lists `Item.Caliber.338Nor` in `SupportedCaliber`; the string appears elsewhere only in ammo items, the projectile asset, UI, audio and tag files. The map in section 7.9 is a native-code claim I cannot test from data (see "Could not verify").

**(h) Slug base 105 and buckshot 25 x 8: CONFIRMED.** `DA_12g_RifledSlug_ProjectileData`: `BaseDamage` 105, no pellet count. `DA_7mmBuckshot_ProjectileData`: `BaseDamage` 25, `NumberOfPellets` 8. JSON `pellets` is 8 on the Buckshot row and null on Slug. Both use arms class Small and neither resolves to an ammo modifier.

## Ammo availability (teammate B), end to end

The script checks every caliber: the set of ammo items, the modifier tag rebuilt from the item tag, and the projectile asset, base damage and arms context. Result: 35 caliber keys, 100 items, zero differences. Three examined by hand:

- `338Nor`: six items. `Id.Item.338Nor.ArmourPiercing` and `...ArmourPiercing.Tracer` give `modifierTag` null with a note about the spelling; the HollowPoint, HollowPoint.Tracer and Tracer items give the matching tags; plain `Id.Item.338Nor` gives null. Projectile `DA_338Norman_ProjectileData`, base 105, Arms.High. Matches the raw item files. B also reports the raw `ItemContext` type for the AP items as `FMJ.Tracer`, which is what the item says (it is a data copy-paste in the game files, and plays no part in damage).
- `9mm`: `Id.Item.9mm`, `.ArmorPiercing`, `.ArmorPiercing.Tracer`, `.HollowPoint` and the Tracer variants resolve to null, ArmorPiercing, ArmorPiercing.Tracer, HollowPoint and so on. Base 22, Arms.Small.
- `12g` and the `7mmBuck` alias: `Id.Item.12g`, `Id.Item.12g.7mmBuck` and `Id.Item.12g.RifledSlug` all carry `Item.Caliber.12g`; the two buckshot items fire the 7mmBuck projectile, the slug fires `Item.Caliber.12g.RifledSlug`. B files the first two under `12g` and again under an `alias` entry `7mmBuck`, and notes the slug is not in the M500 stats `SupportedCaliber`. All consistent with the files.

## Discrepancies, ranked by how misleading they are

1. **Armor coverage is understated in the JSON `meta` and in `docs/evidence/round24-weapon-damage-engine.md`.** Both say the other locations are unarmored. The armor items list `CoveredHitLocations`: all vests cover Torso.Lower, Torso.Middle and Torso.Upper; SuperHeavy armor also covers Pelvis and Arm.Upper; Heavy, SuperHeavy and Tank helmets also cover Neck. So a Torso.Middle shot into Heavy armor does 13.6, not 27.2 (M4, FMJ); a Neck shot into a Heavy helmet does 24.7, not 49.4; an Arm.Upper shot into SuperHeavy armor does 6.05, not 15.1. The tables are correct for what they label (a torso_armor group is Torso.Upper; `location` is unarmored), but the sentence "other locations are unarmored" describes the game wrongly, and a reader using the Torso.Middle or Neck column on an armored target will overstate damage by up to 2x or more.
2. **`meta.rules` understates when AP wins and omits the exception.** It says AP "wins against heavy armor and loses against none". The sweep shows rifle, 50AE and heavier calibers already win at Medium, and Light is a loss for all. It also says AP "removes most of the armor reduction", which is false for SR_04 (scalar 1.0, no reduction removed) and only partly true for Small arms (0.7). The base scalar 0.3 is never used by any of the 33 weapons (their arms classes are Small, Medium, High and Special, all of which are in the override table). The SR_04 case is not mentioned in `meta`.
3. **`meta.rules` credits the HollowPoint collapse to the 1.5 scalar alone.** Entries 20, 21, 133 and 134 (-70, -55, -40, -40 percent against helmets and vests) do most of it. Not wrong, incomplete.
4. **The 22 in the lead's brief is 21.** Nothing in the repo says 22; I found no file making that claim, so this affects only the brief.
5. **Rounding ties.** In 12 of 3072 cells the exact value ends in 5 at the second decimal (22.95, 66.15, 15.75) and the JSON rounds to a different last digit than round-half-up would: RFB and WEPN_034 AP and AP.Tracer Arm.Upper and Leg.Thigh show 22.9 (exact 22.95); Judge FMJ and Tracer Head/Light shows 66.2 (exact 66.15); M500 and MP43 Buckshot Head/Medium shows 15.7 (exact 15.75). The unrounded `damage_raw` agrees with my value, so the only effect is a 0.05 display difference. Negligible.
6. **Cosmetic: `meta.excluded` lists Launcher_04, RPG7, MMGL and CGM4 twice** (once as a group, once each with the "no loadable bullet projectile" reason).

## What I could not verify

- Native behaviour: that the game really builds the ammo tag the way section 7.9 describes (including the `ArmourPiercing` spelling falling through), that rule evaluation order does not matter, and that the first durability stage is the one used at full durability. These are static-analysis claims in the pipeline doc; my check confirms the data and the arithmetic, not the binary.
- Distance falloff, ricochet, penetration, and the 8 pellets spreading across body parts: out of scope for the table, not tested.
- Single-precision effects: the game uses 32-bit floats; mine and A's use 64-bit. The two tie cases above are exactly where this could flip a displayed digit in game.
- `rpm`: checked against `RoundsPerMinute` in each stats asset for 32 of 33 weapons (M500's stats asset has a different name, not matched): no mismatches; LMG_02 and Glock17 are null because the asset omits it, as the meta states.
- Fire modes, magazine data and the attachments-related fields were not examined.
- That Arms.Special's 1.0 in the AP row is intended (not a data-entry quirk). It is what the data says.
