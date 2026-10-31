# Round 24: weapon damage engine

Generator: `python _tools/weapon_damage_tables.py --json` writes `assets/data/weapon-damage.json`. Schema is in the module docstring and in the JSON `meta`.

## Inputs

- `_tools/damage_tables.py`: `weapons()`, `projectiles()`, `evaluate()`, `HIT`, `LOCATIONS`, `CLASSES`, `ammo_table()`. Reused unchanged; no existing output was touched.
- Ammo items under `data/Wardogs/Content/Items/Resources/Ammo/**/ID_*.json`: ItemId tag, `Item.Caliber.*` context tag, projectile fragment (data asset name).
- Caliber data assets under [`Content/GameMechanics/Inventory/Equipment/Caliber/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber): asset name to ProjectileId, `NumberOfPellets`.
- Weapon ID files and stats assets under [`Plugins/GameFeatures/Weapons/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Weapons): display name, archetype (`Item.Archetype.*`), `RoundsPerMinute`, `SupportedFireModes`.
- Rules: DamagePipeline v2 section 7.3 (ammo scalar), 7.7 (damage event), 7.9 (item tag to modifier tag).
- `E:/r24/shared/ammo-availability.json` (teammate B), used only as a cross-check in `--check`. The engine derives availability itself, so the generator does not depend on that file.

## How ammo is chosen

A weapon loads every ammo item whose `Item.Caliber.*` tag is in the weapon's stats `SupportedCaliber`. The modifier tag follows 7.9: last name of the item tag, or the last two for a five-level tag, looked up in `Tracer, HollowPoint, HollowPoint.Tracer, ArmorPiercing, ArmorPiercing.Tracer`. Anything else gets no modifier (FMJ behaviour). Damage uses the projectile the item points at, not the weapon's first supported caliber, so the rifled slug uses its own base 105.

## Assumptions

Hostile, direct hit, point blank (no distance falloff), no ricochet or penetration, target outside a vehicle, no instigator tags, one hit. Armor classes are evaluated for Torso.Upper (vests) and Head (helmets) only, as in `--ammo`; the other four locations are unarmored. Values are rounded to one decimal; unrounded values are in `damage_raw`. Shotgun values are per pellet (8 pellets for the buckshot).

## Excluded

- Launcher_04, RPG7, MMGL, CGM4, AT4 asset, underbarrel GrenadeLauncher: rockets or grenades (`Meta.Damage.Explosive.*`).
- Fists: melee, no bullet.
- BuildTool and the three hammers: build tools.
- ArtilleryBarrelTest, TankBarrelTest: test and artillery barrels.
- M2Browning and MWSY_001 Heavy_MountedMachineGun (and other vehicle weapons): mounted.
- CombatBow: arrows, not bullets.

`damage_tables.weapons()` returns 37 weapons; 4 launchers drop out, leaving 33 in the JSON.

## Guesses and open points

- RPM: taken from `RoundsPerMinute` where the stats asset sets it. LMG_02 and Glock17 omit it, so `rpm` is null (the Infantry Weapons Stats page lists a class default of 600 for LMG_02; not applied).
- Shotguns: `Id.Item.12g` (generic) and `Id.Item.12g.7mmBuck` fire the same buckshot projectile; they are merged into one option `Buckshot`. `Id.Item.12g.RifledSlug` is option `Slug`. Both shotguns' stats list 12g and 7mmBuck, while the chamber filter allows 12g (B's note); the JSON reports caliber `12g`.
- Option ids: `FMJ` is the plain item; `Tracer` and the HP/AP tracer variants are kept as separate options even though their damage equals the non-tracer variant.
- .338 Norma AP (spelled ArmourPiercing in the item tag) resolves to no modifier and would behave as FMJ. No weapon in the table chambers .338, so the case produces no row; the code marks it with a note if a weapon ever does.
- Whether items without the `Item.Ammo` context load (B's open point) did not matter: `Id.Item.545mm.Tracer` has the caliber tag and projectile fragment, so the engine includes it. B's file now lists it too.
- Vendor `bShowInVendor=false` was not used to filter anything.
- Armor coverage by hit location (`CoveredHitLocations`) is not modeled; Torso.Upper and Head follow `damage_tables.py --ammo`.
- `entries_applied` lists every rule entry that changed any cell of the round, including Neck, Torso.Middle, Arm and Leg, so it can be longer than the `--ammo` column.

## Identical rows (same damage for every ammo option)

- A91, KH2002, M249, M4, TAR21, WEPN_029, WEPN_033 (5.56 mm; weapon tags AR.A91, AR.KH2002, AR.M4, AR.Galil, LMG.M249 all resolve to the same factors)
- Glock17, MP9, SMG_03, WEPN_028, WEPN_031, WEPN_032 (9 mm)
- RFB, WEPN_034 (.308)
- WEPN_030, WEPN_036 (.308, lower location factors than RFB)
- SV98, WEPN_017 (7.62x54)
- M500, MP43 (12g)

Singletons: AK74M, SKS, SVDM, LMG_02, WEPN_037, WEPN_027, Judge, WEPN_026, Vector, MK22, SR_04, WEPN_035.

## Surprising numbers

- AP is not a damage boost. Against no armor it deals 0.8 times FMJ. It wins only when armor reduction outweighs that: Medium torso vest for rifle and heavier calibers (ratio 1.28 to 1.4 at SuperHeavy), Heavy for pistol calibers (1.16 at SuperHeavy).
- SR_04 (.50 Cal, arms class Special) gets an armor scalar of 1.0 for AP, the same as FMJ, so AP is worse than FMJ at every armor class (58.2 against 72.8 at SuperHeavy). It still ranks first for AP at Medium torso (99.8) because of its base 90.
- Hollow point doubles unarmored damage and collapses against armor (M4: 54.5 unarmored, 1.5 at SuperHeavy).
- WEPN_035 is a 5.56 sniper: 73.9 at Torso.Upper from its sniper weapon factor (x2.64), well above other 5.56 weapons.
- SR_04 and the bolt snipers have RPM 41.5 and 46; M500 has 120 while MP43 has 900.
