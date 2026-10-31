# Round 24: ammo availability per caliber and weapon

Built by `_tools/ammo_availability.py` from `data/`; the result is `assets/data/ammo-availability.json`. `--check` prints counts and flags.

## How an ammo item resolves

The modifier tag comes from the ammo item's `ItemId` tag, not from its `Item.Ammo.Type.*` context (DamagePipeline section 7.9, native 0x6C98496). The type is the tag's last name, or its last two names for a five-level tag such as `Id.Item.308Win.ArmorPiercing.Tracer`. It resolves only through the fixed map of five `DA_AmmoModifier_*` assets: Tracer, HollowPoint, HollowPoint.Tracer, ArmorPiercing, ArmorPiercing.Tracer. Everything else gets no tag. A plain round is `Id.Item.<caliber>` and carries none, so it is FMJ. A cell below says "no tag" where the item exists but carries no modifier, and "-" where the data has no such item.

The context tag `Item.Ammo.Type.FMJ.Tracer` sits on most plain and Tracer items and on the .338 AP items, regardless of the ItemId. It has no effect on the resolved tag in the native rule above, so it was ignored.

## Caliber by ammo type

Weapons are the items whose stats asset lists the caliber in `SupportedCaliber`, as `_tools/damage_tables.py` reads them. "alias" marks a projectile caliber that no ammo item names in its context (see 7mmBuck below).

| Caliber | Weapons | FMJ | Tracer | HollowPoint | HollowPoint.Tracer | ArmorPiercing | ArmorPiercing.Tracer | Other types |
|---|---|---|---|---|---|---|---|---|
| 120x570mm | none | no tag | - | - | - | - | - | - |
| 120x800mm | none | no tag | - | - | - | - | - | - |
| 122mm | none | no tag | - | - | - | - | - | - |
| 125x570mm | none | no tag | - | - | - | - | - | - |
| 12g | M500, MP43 | no tag | - | - | - | - | - | Buckshot, Slug |
| 155mm | none | no tag | - | - | - | - | - | Sandbox |
| 155mm.Expensive | none | - | - | - | - | - | - | Expensive, Expensive.Sandbox |
| 155mm.Standard | none | - | - | - | - | - | - | Standard, Standard.Sandbox |
| 20x102mm | none | no tag | - | - | - | - | - | - |
| 308Win | RFB, WEPN_030, WEPN_034, WEPN_036, MK22 | no tag | `Tracer` | `HollowPoint` | `HollowPoint.Tracer` | `ArmorPiercing` | `ArmorPiercing.Tracer` | - |
| 30mm | none | no tag | - | - | - | - | - | - |
| 338Nor | none | no tag | `Tracer` | `HollowPoint` | `HollowPoint.Tracer` | - | - | ArmourPiercing, ArmourPiercing.Tracer |
| 35x228mm | none | no tag | - | - | - | - | - | - |
| 40mm | MMGL | no tag | - | - | - | - | - | - |
| 45ACP | Vector, WEPN_026 | no tag | `Tracer` | `HollowPoint` | `HollowPoint.Tracer` | `ArmorPiercing` | `ArmorPiercing.Tracer` | - |
| 45Colt | Judge | no tag | `Tracer` | `HollowPoint` | `HollowPoint.Tracer` | `ArmorPiercing` | `ArmorPiercing.Tracer` | - |
| 50AE | WEPN_027 | no tag | `Tracer` | `HollowPoint` | `HollowPoint.Tracer` | `ArmorPiercing` | `ArmorPiercing.Tracer` | - |
| 50Cal | SR_04 | no tag | `Tracer` | `HollowPoint` | `HollowPoint.Tracer` | `ArmorPiercing` | `ArmorPiercing.Tracer` | - |
| 545mm | AK74M | no tag | `Tracer` | `HollowPoint` | `HollowPoint.Tracer` | `ArmorPiercing` | `ArmorPiercing.Tracer` | - |
| 556mm | M4, KH2002, A91, TAR21, M249, WEPN_029, WEPN_033, WEPN_035 | no tag | `Tracer` | `HollowPoint` | `HollowPoint.Tracer` | `ArmorPiercing` | `ArmorPiercing.Tracer` | - |
| 70mm | none | no tag | - | - | - | - | - | - |
| 72mm | Launcher_04 | no tag | - | - | - | - | - | - |
| 762mm | SKS, WEPN_037 | no tag | `Tracer` | `HollowPoint` | `HollowPoint.Tracer` | `ArmorPiercing` | `ArmorPiercing.Tracer` | - |
| 762x51mm | none | no tag | `Tracer` | `HollowPoint` | `HollowPoint.Tracer` | `ArmorPiercing` | `ArmorPiercing.Tracer` | - |
| 762x54mm | SVDM, LMG_02, SV98, WEPN_017 | no tag | `Tracer` | `HollowPoint` | `HollowPoint.Tracer` | `ArmorPiercing` | `ArmorPiercing.Tracer` | - |
| 84mm | CGM4 | no tag | - | - | - | - | - | - |
| 93mm | RPG7 | no tag | - | - | - | - | - | - |
| 9mm | Glock17, MP9, WEPN_028, WEPN_031, WEPN_032, SMG_03 | no tag | `Tracer` | `HollowPoint` | `HollowPoint.Tracer` | `ArmorPiercing` | `ArmorPiercing.Tracer` | - |
| BatteryCharge | none | no tag | - | - | - | - | - | - |
| C4Charge | none | no tag | - | - | - | - | - | - |
| Arrow | none | no tag | - | - | - | - | - | - |
| Arrow.Explosive | none | - | - | - | - | - | - | Explosive |
| IEDCharge | none | - | - | - | - | - | - | Explosive |
| DroneProjectile | none | no tag | - | - | - | - | - | - |
| 7mmBuck (alias) | M500, MP43 | no tag | - | - | - | - | - | Buckshot |

Counts: 102 ammo item definitions (100 with a caliber context), 35 caliber entries, 37 weapons.

## Quirks

- .338 Norma AP: the items are `Id.Item.338Nor.ArmourPiercing` and `Id.Item.338Nor.ArmourPiercing.Tracer`. "ArmourPiercing" is not in the fixed map, so neither carries a modifier. The tracer one does not even get the Tracer modifier (the type resolves to the two-name string ArmourPiercing.Tracer). Both behave as FMJ. Plain, HollowPoint, HollowPoint.Tracer and Tracer .338 resolve normally.
- No weapon item in `data/` lists .338 Norma or 7.62x51mm as supported, and no magazine or chamber filter references them. Their ammo items and projectile assets exist. 7.62x51mm ammo has weapon-market rows only for plain, Tracer and AP.Tracer, all under `Vendor.Category.Vehicle.Ammo`, so the vendor treats it as vehicle ammo. Whether a vehicle weapon uses it is not determined here. The .338 items have no vendor row.
- Shotgun: M500 and MP43 chambers allow caliber context `Item.Caliber.12g` and block 556mm; the stats asset lists 12g and 7mmBuck. The ammo items are three: plain `Id.Item.12g`, `Id.Item.12g.7mmBuck` (display "7mm Buckshot") and `Id.Item.12g.RifledSlug`. Plain 12g and the buckshot item both point to [`DA_7mmBuckshot_ProjectileData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/7mm_Buckshot/DA_7mmBuckshot_ProjectileData.json) (projectile caliber 7mmBuck, base damage 25). The slug points to [`DA_12g_RifledSlug_ProjectileData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/7mm_Buckshot/DA_12g_RifledSlug_ProjectileData.json) (projectile id `Item.Caliber.12g.RifledSlug`, base damage 105), which is not in either shotgun's `SupportedCaliber`. A damage engine that picks the first listed caliber with a projectile gets the 7mmBuck pellet only. No shotgun type resolves a modifier: "7mmBuck" and "RifledSlug" are not in the fixed map, and plain 12g has no type name. So shotgun shells are always without a modifier tag.
- Calibers with only FMJ: 120x570mm, 120x800mm, 122mm, 125x570mm, 155mm (Standard/Expensive, plus Sandbox variants), 20x102mm, 30mm, 35x228mm, 40mm, 70mm, 72mm, 84mm, 93mm, and the charge or projectile items (BatteryCharge, C4Charge, Arrow, DroneProjectile). Of these, 40mm, 72mm, 84mm and 93mm are launcher calibers used by MMGL, Launcher_04, CGM4 and RPG7. Their "FMJ" label only means no type name in the ItemId; they are explosive or cannon rounds, so a bullet ammo modifier does not describe them.
- Non-bullet ammo: `Id.Item.Arrow.Explosive` and `Id.Item.IED.Explosive` (type Explosive, no tag), `Id.Item.BatteryCharge`, `Id.Item.C4Explosive`, `Id.Item.DroneProjectile`, `Id.Item.Arrow`, and `Id.Item.DebugHomingRocketAmmo` (84mm, a debug item whose projectile asset has no caliber ProjectileId). `Id.Item.C4Trigger` and `Id.Item.IED.Trigger` have the `Item.Ammo` context but no caliber. `Id.Item.C4Explosive` and `Id.Item.IED.Explosive` have no projectile fragment.
- 155mm items use three-level IDs (`ID.Item.155mm.Standard`, `.Expensive`) and `.Sandbox` variants. None resolve to a tag. No weapon lists 155mm.
- Tracer-only variants: none. Each bullet caliber with variants has all six items. Only `Id.Item.545mm.Tracer` lacks the `Item.Ammo` context (it keeps the caliber context). Whether that stops it loading is not determined; the JSON note flags it.
- Every bullet variant of a caliber points to the same projectile data asset as the plain round (checked for 308Win, 45ACP, 45Colt, 50AE, 50Cal, 545mm, 762x51mm, 9mm, 338Nor), so the base damage and context are identical across variants and only the added modifier tag differs.
- Loading rule found in the files: magazines and weapon chambers use an AllowList on `Item.Caliber.<x>` item context (for example the M4 standard magazine allows `Item.Caliber.556mm`, the MP43 chamber allows `Item.Caliber.12g` and blocks `Item.Caliber.556mm`). So every ammo item with that caliber context is loadable by weapons with that caliber. No per-type restriction was found.
- Several weapons share one damage tag (for example TAR21 and A91, Launcher_04 and the other launchers); this is the damage tag the existing tool reads, not an ammo question.

## Availability (vendor rows)

Each ammo item lists its weapon-market row when one exists: table, categories, price, amount, `bShowInVendor`, `LevelToUnlock`. Many rows have `bShowInVendor` false (for example plain 9mm and the .308 AP). What false means in play is not determined. Calibers with no vendor row for any item: 120x800mm, .338 Norma, 72mm, the charge items. The JSON never claims an item is obtainable; it reports the row.

## Not determined

- Which vehicle weapons load 7.62x51mm, .338 Norma, 20x102mm, 30mm, 35x228mm and the tank calibers (vehicle weapon item mapping was not traced).
- Whether items lacking the `Item.Ammo` context load into a magazine.
- What `bShowInVendor` false and `LevelToUnlock` mean for obtaining a given ammo variant.
- Loot or world-spawn sources of ammo.
