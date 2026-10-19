---
title: Round 8 backblast damage evidence
nav_exclude: true
---

# Round 8: backblast source, health amount and seated hit

Research date: 2026-10-18; CL-516586. Static reads of the original restored executable and existing read-only corpus, with critical instructions checked independently using Capstone. No game process, service or IDA database was opened. Addresses below are RVAs. The corpus records executable SHA-256 `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.

## Closure

The normal on-foot and seated health amounts and source-context construction are resolved. Handheld backblast retains the weapon's own damage entity and adds `Meta.Damage.DamageType.BackBlast`; it does not obtain the projectile's damage entity. All three exported launcher item fragments use the same source tag, `Meta.Damage.Weapon.Launcher.AT4`. Seated damage uses a synthetic hit with no bone or explicit hit-location tag. Vehicle attribute self-damage is a separate caller path and must not be treated as occupant health damage.

The additional reflected/secondary on-foot branch and all target-gather conditions remain outside this bounded closure. The formulas below describe the native starting amount before `ModifyDamage`, target filters, and application; they are not unconditional gameplay damage guarantees.

## Source construction

`0x6B92900` initializes a fallback `FWDDamageEntityData` with the global BackBlast tag (`0x6B92AE8–0x6B92AFE`). The tag initializer is `0x1279F70`; its name argument at `0x1279F8B` is `Meta.Damage.DamageType.BackBlast`.

The caller then asks the `IWDWeaponOwner` interface for its damage-entity component through slot `+0x70` (`0x6B92B0C`). When present, `0x1C36300` returns component `+0xE0`; the caller replaces the fallback tag, context and cause with that entity (`0x6B92B17–0x6B92B45`). The following optional item-tag lookup can replace the cause tag. It does not replace the source tag or append projectile/caliber context.

For the normal ranged-weapon extension, constructor `0x6C91510` installs the owner interface at extension `+0xF0`, table `0xB389AB8`; its `+0x70` slot is `0x1812A60`, which returns `[interface+0x40]`, i.e. extension `+0x130`, the created damage-entity component. Initialization `0x6C9AFB0` passes ranged-weapon fragment `+0x1E0` to that component (`0x6C9B588–0x6C9B596`). Setter `0x6B18E30` copies its source tag, context and cause to component `+0xE0/+0xE8/+0x108` (`0x6B18E40`, `0x6B18E55`, `0x6B18E63`). This connects the cooked item fragment to the backblast source, rather than merely inferring it from the weapon name.

On-foot `0x6F042A0` copies the provided source and appends BackBlast if absent (`0x6F04571–0x6F04609`). Seated `0x6F06EB0` does the same (`0x6F06F67–0x6F06FD0`). Neither block adds `DamageType.Projectile`, `DamageType.Explosive`, a radius tag, or a projectile ID. Existing caller-provided context is preserved; this is not proof that every possible custom owner starts with empty context.

The exported `WDItemExtensionData_RangedWeapon.DamageEntityData` has tag `Meta.Damage.Weapon.Launcher.AT4` and no serialized context in each of:

| Item file | Source anchor |
|---|---|
| `data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/Launcher_04/Content/Data/ID_Launcher_04.json` | `DamageEntityData`, line 1270 |
| `data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/RPG7/Content/Data/ID_RPG7.json` | `DamageEntityData`, line 1297 |
| `data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_013/Content/Data/ID_CGM4.json` | `DamageEntityData`, line 1249 |

The fallback-only case instead starts with BackBlast as its source tag. Do not universally replace the normal handheld source with that fallback tag.

## Native field-to-formula mapping

Offsets are from `FWDBackBlastConfig`, `sdk/raw/WDGame_structs.hpp:19938`. Symbolic meanings below are defined by the actual reads and use, not guesses at the hashed names.

| Offset | Exported field | Verified use |
|---|---|---|
| `+0x0C` | `_aaabbilmgpjejlkjoeibh` | on-foot angle limit A, degrees |
| `+0x10` | `_aaaanghlhocankbgenpld` | on-foot distance limit D |
| `+0x14` | `_aaaaplhbefklkbekbplbj` | on-foot nominal base B; also seated base |
| `+0x18` | `_aaaaocboicpblkhflbiho` | on-foot minimum M |
| `+0x20` | `_aaabeflbnagdhkfoiahod` | on-foot distance curve Fd |
| `+0xA8` | `_aaabbnnpbcjpjbldiifog` | on-foot angle curve Fa |
| `+0x138` | `_aaabcbmocdkdakedpapbc` | seated distance divisor Dc |
| `+0x140` | `_aaabjjnlflmigemoolnjn` | seated health distance curve Fc |
| `+0x25C` | `_aaabhjchepijkbbnkmohg` | seated health scalar K |
| `+0x290` | `_aaabgpobchhagbhokmiba` | clamped seated/vehicle scalar C |
| `+0x2A8` | `_aaabemendcoeglbmnhbld` | separate vehicle attribute self-damage map |
| `+0x2F8` | `VehicleOverrides` | variant-keyed replacement of C, effects and attribute map |

Distances use the executable's FVector world coordinates, conventionally centimeters. `+0x13C` and the helper `0x76C4000` are part of the effects-strength route, not the health amount returned by `0x76C4120`.

## Normal on-foot starting amount

`0x6F042A0` passes distance d and angle theta to `0x76C3EB0` at `0x6F0501E`. Its returned float becomes the starting amount sent to generic event builder `0x6BB4D30` at `0x6F051F1`, then general armor hook `+0x18` (`0x6F0525B`), `ModifyDamage` (`0x6F0526C`) and application (`0x6F052DD`).

For ordinary finite inputs, `0x76C3EB0` implements:

```text
if D <= 0 or B <= 0 or d <= 0.0001 or d > D or theta > A: S = 0
otherwise:
  t = clamp(d / D, 0, 1)
  u = A > 0 ? clamp(theta / A, 0, 1) : 0
  fd = Fd(t), or 1-t when the runtime curve has no keys
  fa = Fa(u), or 1-u when the runtime curve has no keys
  S = M + (B-M) * clamp(fd * fa, 0, 1)
```

Machine anchors: guards `0x76C3ED3–0x76C3F0B`; normalization `0x76C3F11–0x76C3F49`; curve lookup/evaluation `0x76C3F4C–0x76C3F9E`; product, clamp and interpolation `0x76C3FB0–0x76C3FD8`. Consequently the angular/distance boundary can still yield M, with a discontinuity to zero beyond the guard. The exact origin d=0 returns zero, so B is a nominal limiting base, not the helper's result at exactly d=0.

In the ordinary accepted-hit path, d is the Euclidean distance from the supplied backblast origin to `FHitResult.ImpactPoint` (`0x6F04F00–0x6F04F67`); theta comes from the rear-direction dot product, clamped before inverse cosine and degree conversion (`0x6F04F47–0x6F04FB1`). A special target-geometry branch can substitute theta=0 and a clamped distance (`0x6F04FB9–0x6F05013`); do not generalize the simple geometry description to that branch. A later reflected/secondary path calls radial helper `0x6F062F0` near `0x6F05FA3`; its complete trigger and amount are not closed here.

## Seated starting amount and synthetic hit

Caller `0x6B92900` first makes a variant-adjusted config with `0x76C4200` (`0x6B92C9A`), then invokes seated `0x6F06EB0` (`0x6B92CD2`). The on-foot call is separate at `0x6B933E9`.

Seated function `0x6F06EB0` immediately exits its processing branch when `clamp(C,0,1) <= 0` (`0x6F06F2B–0x6F06F4A`). Per candidate occupant, it computes root-location distance from the source actor passed as a4, not distance from the rear cone origin to a skeletal hit (`0x6F070FF–0x6F07146`; source root read `0x6F06FD5–0x6F07007`). It calls health helper `0x76C4120` at `0x6F07208`:

```text
P = K * B * clamp(C, 0, 1)
if P <= 0 or Dc <= 0: S = 0
otherwise:
  t = clamp(actorRootDistance / Dc, 0, 1)
  f = Fc(t), or 1-t when the runtime curve has no keys
  S = max(P * f, 0)
```

Machine anchors: C clamp `0x76C4124–0x76C4164`; P `0x76C4155–0x76C4168`; guards `0x76C416D–0x76C417E`; normalization/curve `0x76C4180–0x76C41B0`; result `0x76C41B5–0x76C41D9`. There is no on-foot M term or angle curve in this helper. The separate effects-strength helper `0x76C4000` is called at `0x6F0714D`; its result must not be substituted for S.

The seated hit is constructed by `0x3EAF060` at `0x6F07386` and receives the computed distance at hit `+0x08` (`0x6F073A0`). This constructor zeroes 0x100 bytes (`0x3EAF08E`) and writes locations, normals, actor handle and component only (`0x3EAF093–0x3EAF192`). It never writes `BoneName +0xF0` or `MyBoneName +0xF8`; see `sdk/raw/Engine_structs.hpp:9537`. Builder call `0x6F075A1` passes S in xmm1 and the global empty explicit hit-location tag at stack `+0x38` (`0x6F0753A`, `0x6F07578`). The general armor hook also gets empty location and a pointer to zero bone (`0x6F0766B–0x6F07681`), followed by `ModifyDamage` at `0x6F07695`.

Thus this native seated path does not provide an anatomical bone/location for bone multipliers. The ordinary converter's conditional bone fallback cannot manufacture an anatomical name from this empty synthetic bone. General armor hook filtering still has the valid-equipment/removal-set conditions described in [round8-armor.md](round8-armor.md) and independently checked in [round8-radial.md](round8-radial.md).

## Cooked weapon values and vehicle overrides

These values are read from each `BackBlast` object, with bEnabled=true. B/M are starting-amount parameters; seated P is before downstream modifiers.

| Stats asset | A degrees | D | B | M | Dc | K | C | Seated P | Fc plateau ends at distance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `DA_Launcher_04_Stats` | 35 | 200 | 80 | 15 | 300 | 0.3 | 1 | 24 | 120 |
| `DA_RPG7_Stats` | 40 | 500 | 130 | 30 | 1000 | 0.7 | 0.8 | 72.8 | 250 |
| `DA_CGM4_Stats` | 45 | 600 | 150 | 40 | 1200 | 0.45 | 0.8 | 54 | 300 |

Stats sources are beside their respective ID files above: Launcher_04 `DA_Launcher_04_Stats.json:687`, RPG7 `DA_RPG7_Stats.json:699`, CGM4 `DA_CGM4_Stats.json:641`.

All three serialize the distance Fd as an unweighted cubic curve, keys `(0,1)`, `(tm,0.896613)`, `(1,0)`, with middle arrive/leave tangent -1 and first leave/final arrive tangent 0. `tm=0.37625` for Launcher_04 and CGM4, `0.19625` for RPG7. Their angle curve Fa is not serialized; the empty-curve branch gives `1-u`. Their seated Fc is piecewise linear: Launcher_04 keys `(0,1),(.4,1),(1,0)`; RPG7/CGM4 `(0,1),(.25,1),(1,0)`.

All three have exact variant overrides for `Vehicle.Variant.Land.Wheeled.Bobcat.Default` and `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default`, setting C=0, effects empty and attribute map empty. Native `0x76C4200` copies the config (`0x76C421B`), looks up the variant (`0x76C422C`), and replaces only C (`0x76C423F`), effects (`0x76C424C`) and attribute map (`0x76C425C`). It does not change B, M, curves or distances. These overrides therefore disable the seated function through its C gate; this does not establish that unrelated world backblast paths cannot hurt a nearby actor.

The default attribute map contains rotor-main/engine values 300/80 for Launcher_04 and 200/100 for RPG7/CGM4. This is separate vehicle self-damage: caller loads each positive map value into xmm2 (`0x6B9301E`) and passes its attribute tag to `0x5320280` (`0x6B9303C`). These map values are not the seated infantry S, and the seated health scalar K is not an armor multiplier.

## Suggested documentation/generator changes and limits

Replace the backblast source/amount unknowns with the two explicit formulas and the handheld source construction above. A data table can show nominal on-foot B/M and seated P, while keeping distance and angle dependent results explicit. Do not reuse explosive radial falloff, projectile source tags, caliber context, effects strength, or vehicle attribute-map amounts for this health path. Seated output should have no anatomical bone multiplier from its synthetic hit.

Still open: complete on-foot gather/occlusion and special geometry cases; the additional reflected/secondary on-foot radial branch; custom owner-provided context and runtime mutations; vehicle aliases beyond the two exact serialized variants; live collision/seat outcomes. No dynamic execution was used to close those questions.
