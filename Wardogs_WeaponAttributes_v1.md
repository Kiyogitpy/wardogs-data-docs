---
title: "Weapon Attributes"
parent: "Content"
---

# Wardogs — Weapon Attributes

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Each weapon's final `Attribute.Gameplay.Weapon.*` values with its default attachments, and what every
attachment changes on the weapon. The values are computed from the cooked data with the rules of the
[Gameplay Effects Pipeline](Wardogs_GameplayEffectsPipeline_v1.md); nothing here was measured in the game.
Effect modifiers come from [Gameplay Effect Values](Wardogs_GameplayEffect_Values_v1.md). Labels: **Data**
for what the export says, **Native** for what the traced code does, **Assumption** for a choice this page
makes where the code is not traced.
To try any other loadout (attachments, sight, stance, bipod), use the [Weapon Loadout Calculator](loadout-calculator.md).

## Rules

From [Effects §7.1](Wardogs_GameplayEffectsPipeline_v1.md#71-what-applies-to-a-weapon) (what applies to a
weapon), [§4.2](Wardogs_GameplayEffectsPipeline_v1.md#42-modifiers) (stack scaling) and
[§4.4](Wardogs_GameplayEffectsPipeline_v1.md#44-current-value) (current value):

- **Base.** The weapon item's `WDItemExtensionData_GameplayEffects.DefaultAttributes`. The `AimTime` in
  `WDItemExtensionData_RangedWeapon.DefaultAttributes` never changes it, so it is not used.
- **On the weapon,** one application each: every equipped attachment's `AppliedEffects`; the selected
  sight's `SightsData[name].AppliedEffects`, where the name starts as `S_Aim01` and changes only through
  `CycleSights`; the bipod's unfolded list (`+0x138`) only with the bipod unfolded and not mounted, and
  its `MountedAppliedEffects` (`+0x158`, applied by the Blueprint action `B_Action_MountBipod`) instead
  of the unfolded lists while mounted (the tables use folded); and `StanceGameplayEffects[stance]` with
  the preset's stack count (1 in all data; the tables use Stand).
- **Not on the weapon.** `AppliedCharacterEffects`, the bipod's unfolded `+0x148` list and its mounted
  `MountedAppliedCharacterEffects` (`+0x168`) go to the character. They are listed as character effects
  and never enter a weapon value.
- **Evaluation.** Each application is its own instance with `n = 1` (so an effect applied twice counts
  twice), every `Filter` is empty and no weapon attribute has a hook. Magnitudes are read as the asset's
  floats, so 0.7 enters as 0.699999988. If an Override is active, the first one in the attribute's
  Override list wins. Otherwise
  `Current = ((Base + ΣAdd) × (1 + Σ(Multiply − 1)) / D) × ΠMultiplyCompound + ΣAddFinal`, with
  `D = 1 + Σ(Divide − 1)`, or 1 when |D| ≤ 1e-8. Only the `Default` channel exists.
- **Attribute-backed modifiers** (seven sight effects override `MaxZeroingRange` with the current
  `MinZeroingRange`) are evaluated against the final value of the backing attribute and marked †. The
  game does the same: such magnitudes are re-evaluated whenever the backing attribute's current value
  changes ([Effects §4.2](Wardogs_GameplayEffectsPipeline_v1.md#42-modifiers)).
  No weapon-side modifier has a curve row, non-`Fixed` indexing or a set-by-caller magnitude; the tool
  marks one if it appears.

## Choices this page makes

- **Data: Override order does not matter.** No two attachments that fit one weapon at the same time
  override the same attribute with different values, and stance effects have no Override. Native order
  (append on apply, swap on removal, [Effects §4.4](Wardogs_GameplayEffectsPipeline_v1.md#44-current-value))
  depends on the equip history, so the tool flags any future conflict rather than trust its choice (it
  uses the first Override in its own order and marks the value †). That order is the weapon's sub-slots in data order, each attachment
  followed by the sub-slots it brings (a barrel's muzzle slot, a handguard's underbarrel slot); per
  attachment its `AppliedEffects`, then the selected sight's effects, then the unfolded or mounted bipod
  list; and the stance effect (applied at registration and re-appended on every stance change; it has no
  Override modifier, so its place does not matter). On the authority the equip path follows the sub-slot
  update messages (`WDItemSubslotUpdated`, `0x6C99030`), slot by slot; the attachment array is replayed in
  array order at registration and on replication (`0x6C9A330`), which changes only slots whose item
  differs. The order across the weapon and its attachments is not traced.
- **Data: initial sight.** §1 and §2 use the `SightsData` entry `S_Aim01`, per
  [Effects §7.1](Wardogs_GameplayEffectsPipeline_v1.md#71-what-applies-to-a-weapon); §3 lists every entry.
  `ID_CantedIrons`, whose only entry is `S_AimCanted1`, has no `S_Aim01`. Natively there is no first-entry
  fallback: its `AppliedEffects` apply only when it replaces another attachment in the slot (`0x6C9D170`),
  and its sight effects come from the weapon's sight table entry for `S_Aim01` (`+0x438`, left by another
  sight), or none (`0x6C9E190`). The tool applies no sight effects for it; no weapon accepts the item, so
  this affects no table.
- **Native (`0x6784010`): default loadout.** Each sub-slot's `DefaultContainerItems`, or `DefaultItems` only
  when `DefaultContainerItems` is empty, and the defaults of the sub-slots that item brings. `None` leaves
  the slot empty. The tool takes the first real item; natively every entry is added, and no weapon or
  attachment sub-slot lists more than one. Ammunition in chamber and magazine slots carries no effects and
  is left out. Among attachment sub-slots the lists differ only in `ID_CGM4`'s sight (`DefaultItems`
  `BasicRedDot` = `ID_RedDot`; `DefaultContainerItems` `ID_SGHT_033`), whose `AllowList` admits only `SGHT_033`;
  with `ID_RedDot` the MAAWS AimTime would be 0.45. Sixteen magazine ammo slots also differ (the plain round in
  `DefaultItems`, its `.Tracer` round in `DefaultContainerItems`), which changes no attribute.
- **Native: sub-slot filters** (`0x67A2B40`, run per container by `0x67A2790`). `ItemId` is matched exactly
  against the item lists; context tags hierarchically (`HasAny`, `0x395BE30`: the item's tag or a child of
  it). `AllowList` = allowed (block lists ignored; one weapon's default chamber round is on both lists);
  `BlockList` = not blocked; `BlockPriority` = allowed and not blocked; `AllowPriority` = allowed or not
  blocked.

## Using the tool

```
python _tools/weapon_attributes.py --weapon ID_WEPN_037 --with ID_FGRP_006 ID_SGHT_009 --stance Prone
python _tools/weapon_attributes.py --write
```

`--with` puts each attachment into the first free sub-slot that accepts it, replacing the default item
there, and stops with an error when no free sub-slot accepts it. `--sight NAME` picks a `SightsData`
entry (default `S_Aim01`), `--bipod` unfolds a bipod and `--mounted` mounts it (implying unfolded),
which replaces the unfolded lists with the mounted ones. The command prints the loadout, the applications in Override order, the
character effects, and each attribute's modifiers and final value at full precision.

**Reading the tables.** Attribute names drop `Attribute.Gameplay.Weapon.`. Operations: `+` Add, `×`
Multiply, `÷` Divide, `×c` MultiplyCompound, `+f` AddFinal, `=` Override. Values are rounded to six
significant digits.

<!-- BEGIN weapon_attributes -->
Generated by [`_tools/weapon_attributes.py`](_tools/weapon_attributes.py) from `data/` and [`assets/data/ge-values.json`](assets/data/ge-values.json): 38 weapons, 298 attachment items, 11 weapon attributes.

## 1. Final values

Default loadout, Stand stance, bipod folded. A cell shows `base → final` where the two differ. Attributes a weapon has no base value for are blank.

| Weapon | VRecoil | HRecoil | Spread | Accuracy | AimTime | ADS zoom | Zero min | Zero max | Equip | Holster | Length |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| [A-91](#a-91-id_a91) | 1 → **0.588** | 1 → **0.595** | 1 | 1 | 0.525 → **0.44625** | 1.2 | 100 | 100 | 0.92 → **1.0672** | 1 | 80 |
| [AK74](#ak74-id_ak74m) | 1 | 1 | 1 | 1 | 0.45 | 1.2 | 100 | 1000 | 1 | 1.05 | 80 |
| [Bushmaster M17S](#bushmaster-m17s-id_wepn_033) | 1 → **0.84** | 1 → **0.85** | 1 | 1 | 0.525 → **0.44625** | 1.2 | 100 | 100 | 0.95 → **1.102** | 1 | 80 |
| [FAL](#fal-id_wepn_030) | 1 | 1 | 1 | 1 | 0.5 | 1.2 | 100 | 600 | 0.95 | 1 | 80 |
| [Galil](#galil-id_wepn_029) | 1 | 1 | 1 | 1 | 0.49 | 1.2 | 100 | 400 | 0.95 | 1 | 80 |
| [KH-2002](#kh-2002-id_kh2002) | 1 → **0.84** | 1 → **0.85** | 1 | 1 | 0.525 → **0.44625** | 1.2 | 100 | 100 | 0.95 → **1.102** | 1 | 80 |
| [M4](#m4-id_m4) | 1 | 1 | 1 | 1 | 0.49 | 1.2 | 100 | 500 | 0.95 → **0.931** | 1.1 | 80 |
| [T-21](#t-21-id_tar21) | 1 → **0.84** | 1 → **0.85** | 1 | 1 | 0.525 → **0.44625** | 1.2 | 100 | 300 | 0.95 → **1.102** | 1 | 80 |
| [Compound Bow](#compound-bow-id_combatbow) | 1 | 1 | 1 | 1 | 0.285 | 1.2 | 100 | 100 |  |  | 80 |
| [BMR-308](#bmr-308-id_rfb) | 1 → **0.84** | 1 → **0.85** | 1 | 1 | 0.52 → **0.442** | 1.2 | 100 | 300 | 0.92 → **1.1408** | 1 | 80 |
| [M14](#m14-id_wepn_034) | 1 | 1 | 1 | 1 | 0.53 | 1.2 | 100 | 500 | 0.97 | 1 | 80 |
| [SKS](#sks-id_sks) | 1 | 1 | 1 | 1 | 0.53 | 1.2 | 100 | 1000 | 1.15 | 1.1 | 80 |
| [SVD](#svd-id_svdm) | 1 | 1 | 1 | 1 | 0.53 → **0.5618** | 1.2 | 100 | 1100 | 0.97 → **0.873** | 1 | 80 |
| [TCX-SPR](#tcx-spr-id_wepn_037) | 1 | 1 | 1 | 1 | 0.48 | 1.2 | 100 | 200 | 1 | 0.95 | 80 |
| [Evo-3 Ultra](#evo-3-ultra-id_wepn_036) | 1 | 1 | 1 | 1 | 0.64 | 1.2 | 100 | 500 | 1 | 1 | 80 |
| [M249 SAW](#m249-saw-id_m249) | 1 → **1.17** | 1 → **1.17** | 1 | 1 | 0.68 → **0.816** | 1.2 | 200 | 1200 | 0.95 → **0.8835** | 0.95 | 80 |
| [PKM](#pkm-id_lmg_02) | 1 | 1 | 1 | 1 | 0.73 → **0.803** | 1.2 | 100 | 1500 | 0.95 | 1 | 80 |
| [9K333 Verba](#9k333-verba-id_launcher_04) | 1 | 1 | 1 | 1 | 0.5 | 1.2 | 100 | 1000 |  | 1.15 | 100 |
| [MAAWS](#maaws-id_cgm4) | 1 | 1 | 1 | 1 | 0.5 | 1.2 | 100 | 100 | 0.95 | 1 | 80 |
| [MGL-40](#mgl-40-id_mmgl) | 1 | 1 | 1 | 1 | 0.4 | 1.2 | 50 | 400 | 0.95 | 1 | 80 |
| [RPG-7](#rpg-7-id_rpg7) | 1 | 1 | 1 | 1 | 0.5 | 1.2 | 100 | 500 | 0.95 | 1 | 80 |
| [Deagle](#deagle-id_wepn_027) | 1 | 1 | 1 | 1 | 0.25 | 1.2 | 50 | 50 | 0.9 | 0.85 | 80 |
| [GGX 17](#ggx-17-id_glock17) | 1 | 1 | 1 | 1 | 0.2 | 1.2 | 50 | 50 | 1.2 | 1.1 | 80 |
| [GGX 18](#ggx-18-id_wepn_032) | 1 | 1 | 1 | 1 | 0.2 | 1.2 | 50 | 50 | 1.2 | 1.15 | 80 |
| [Judge](#judge-id_judge) | 1 | 1 | 1 | 1 | 0.35 | 1.2 | 25 | 25 | 0.95 | 1.15 | 80 |
| [M1911](#m1911-id_wepn_026) | 1 | 1 | 1 | 1 | 0.2 | 1.2 | 25 | 25 | 0.92 | 1 | 80 |
| [AMP-9](#amp-9-id_mp9) | 1 → **1.12** | 1 → **1.14** | 1 | 1 | 0.25 → **0.2775** | 1.2 | 50 | 100 | 1.12 → **1.0416** | 1.2 | 80 |
| [MP5](#mp5-id_wepn_028) | 1 | 1 | 1 | 1 | 0.285 | 1.2 | 25 | 100 | 1.05 | 0.9 | 80 |
| [PP-19 Bizon](#pp-19-bizon-id_wepn_031) | 1 | 1 | 1 | 1 | 0.285 | 1.2 | 50 | 200 | 0.94 | 1.15 | 80 |
| [PP-19 Vityaz](#pp-19-vityaz-id_smg_03) | 1 | 1 | 1 | 1 | 0.285 | 1.2 | 50 | 200 | 0.94 | 1.15 | 80 |
| [Super-45](#super-45-id_vector) | 1 | 1 | 1 | 1 | 0.25 | 1.2 | 50 | 100 | 1 | 1 | 80 |
| [M500](#m500-id_m500) | 1 | 1 | 1 | 1 | 0.365 | 1.2 | 100 | 100 | 0.95 | 1 | 80 |
| [MP43](#mp43-id_mp43) | 1 | 1 | 1 | 1 | 0.35 | 1.2 | 70 | 70 | 1.25 | 0.95 | 80 |
| [AMR 50](#amr-50-id_sr_04) | 1 | 1 | 1 | 1 | 0.68 | 1.2 | 100 | 300 | 0.9 | 1.15 | 80 |
| [MK22](#mk22-id_mk22) | 1 | 1 | 1 | 1 | 0.675 → **0.7155** | 1.2 | 100 | 300 | 1.05 → **0.945** | 1.17 | 80 |
| [Mosin Nagant](#mosin-nagant-id_wepn_017) | 1 | 1 | 1 | 1 | 0.65 | 1.2 | 200 | 800 | 0.94 | 1 | 80 |
| [Scout Rifle TD](#scout-rifle-td-id_wepn_035) | 1 | 1 | 1 | 1 | 0.5 | 1.2 | 100 | 100 | 1 | 1 | 80 |
| [SV98](#sv98-id_sv98) | 1 | 1 | 1 | 1 | 0.6 | 1.2 | 100 | 100 | 0.95 | 1 | 80 |

## 2. Weapons

Each weapon's default loadout (sub-slot: item), the effects applied to it in the order this page uses for Override lists, and per attribute the base, the modifiers that reach it and the final value. Modifier magnitudes are the stack-scaled values.

### AR

#### A-91 (ID_A91)

Item `Id.Item.A91`, [`ID_A91.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_004/Content/Data/ID_A91.json).

- **Loadout:** Magazine: `ID_STANAG_Mag_20rd`; Barrel: `ID_A91Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_AR_Prone`.
- **Character effects:** `GE_MAGZ_053_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 0.84 `GE_MAGZ_053`<br>×c 0.7 `GE_Weapon_StanceRecoil_AR_Prone` | 0.588 |
| HorizontalRecoilMultiplier | 1 | ×c 0.85 `GE_MAGZ_053`<br>×c 0.7 `GE_Weapon_StanceRecoil_AR_Prone` | 0.595 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.525 | ×c 0.85 `GE_MAGZ_053` | 0.44625 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 100 | — | 100 |
| EquipSpeedMultiplier | 0.92 | ×c 1.16 `GE_MAGZ_053` | 1.0672 |
| HolsterSpeedMultiplier | 1 | — | 1 |

#### AK74 (ID_AK74M)

Item `Id.Item.AK74M`, [`ID_AK74M.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_001/Content/Data/ID_AK74M.json).

- **Loadout:** Magazine: `ID_AK74M_Mag_Standard`; Stock: `ID_AK74MStock`; Grip: `ID_AK74MPistolGrip`; Barrel: `ID_AK74MBarrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_AR_Standing`.
- **Character effects:** `GE_AK74_Mag_30rd_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_AK74_Mag_30rd`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_AK74_Mag_30rd`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.45 | ×c 1 `GE_AK74_Mag_30rd` | 0.45 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 1000 | — | 1000 |
| EquipSpeedMultiplier | 1 | — | 1 |
| HolsterSpeedMultiplier | 1.05 | — | 1.05 |

#### Bushmaster M17S (ID_WEPN_033)

Item `Id.Item.WEPN_033`, [`ID_WEPN_033.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_033/Content/Data/ID_WEPN_033.json).

- **Loadout:** Magazine: `ID_STANAG_Mag_20rd`; Barrel: `ID_BARL_044`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_AR_Standing`.
- **Character effects:** `GE_MAGZ_053_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 0.84 `GE_MAGZ_053`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 0.84 |
| HorizontalRecoilMultiplier | 1 | ×c 0.85 `GE_MAGZ_053`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 0.85 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.525 | ×c 0.85 `GE_MAGZ_053` | 0.44625 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 100 | — | 100 |
| EquipSpeedMultiplier | 0.95 | ×c 1.16 `GE_MAGZ_053` | 1.102 |
| HolsterSpeedMultiplier | 1 | — | 1 |

#### FAL (ID_WEPN_030)

Item `Id.Item.WEPN_030`, [`ID_WEPN_030.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_030/Content/Data/ID_WEPN_030.json).

- **Loadout:** Magazine: `ID_MAGZ_006`; Barrel: `ID_BARL_007`; Grip: `ID_PGRP_003`; Stock: `ID_STOK_005`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_AR_Standing`.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_006`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_006`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.5 | ×c 1 `GE_MAGZ_006` | 0.5 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 600 | — | 600 |
| EquipSpeedMultiplier | 0.95 | — | 0.95 |
| HolsterSpeedMultiplier | 1 | — | 1 |

† Sight default `Id.Item.IRNS_002` (on `ID_WEPN_030`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.

#### Galil (ID_WEPN_029)

Item `Id.Item.WEPN_029`, [`ID_WEPN_029.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_029/Content/Data/ID_WEPN_029.json).

- **Loadout:** Magazine: `ID_MAGZ_005`; Stock: `ID_STOK_013`; Grip: `ID_PGRP_010`; Barrel: `ID_BARL_006`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_AR_Standing`.
- **Character effects:** `GE_MAGZ_005_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_005`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_005`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.49 | ×c 1 `GE_MAGZ_005` | 0.49 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 400 | — | 400 |
| EquipSpeedMultiplier | 0.95 | — | 0.95 |
| HolsterSpeedMultiplier | 1 | — | 1 |

#### KH-2002 (ID_KH2002)

Item `Id.Item.KH2002`, [`ID_KH2002.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_003/Content/Data/ID_KH2002.json).

- **Loadout:** Magazine: `ID_STANAG_Mag_20rd`; Barrel: `ID_KH2002Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_AR_Standing`.
- **Character effects:** `GE_MAGZ_053_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 0.84 `GE_MAGZ_053`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 0.84 |
| HorizontalRecoilMultiplier | 1 | ×c 0.85 `GE_MAGZ_053`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 0.85 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.525 | ×c 0.85 `GE_MAGZ_053` | 0.44625 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 100 | — | 100 |
| EquipSpeedMultiplier | 0.95 | ×c 1.16 `GE_MAGZ_053` | 1.102 |
| HolsterSpeedMultiplier | 1 | — | 1 |

#### M4 (ID_M4)

Item `Id.Item.M4`, [`ID_M4.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_002/Content/Data/ID_M4.json).

- **Loadout:** Magazine: `ID_556STANAG_Mag_Standard`; Grip: `ID_M4Grip`; Stock: `ID_M4Stock`; Barrel: `ID_M4Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_AR_Standing`.
- **Character effects:** `GE_Stanag_30Rounds_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_Stanag_30Rounds`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_Stanag_30Rounds`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.49 | ×c 1 `GE_Stanag_30Rounds` | 0.49 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 500 | — | 500 |
| EquipSpeedMultiplier | 0.95 | ×c 0.98 `GE_Stanag_30Rounds` | 0.931 |
| HolsterSpeedMultiplier | 1.1 | — | 1.1 |

† Sight default `Id.Item.IRNS_006` (on `ID_M4`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.

#### T-21 (ID_TAR21)

Item `Id.Item.TAR21`, [`ID_TAR21.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_005/Content/Data/ID_TAR21.json).

- **Loadout:** Magazine: `ID_STANAG_Mag_20rd`; Barrel: `ID_Tar21Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_AR_Standing`.
- **Character effects:** `GE_MAGZ_053_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 0.84 `GE_MAGZ_053`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 0.84 |
| HorizontalRecoilMultiplier | 1 | ×c 0.85 `GE_MAGZ_053`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 0.85 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.525 | ×c 0.85 `GE_MAGZ_053` | 0.44625 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 300 | — | 300 |
| EquipSpeedMultiplier | 0.95 | ×c 1.16 `GE_MAGZ_053` | 1.102 |
| HolsterSpeedMultiplier | 1 | — | 1 |

### Bow

#### Compound Bow (ID_CombatBow)

Item `Id.Item.CombatBow`, [`ID_CombatBow.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/Data/DataAssets/ID_CombatBow.json).

- **Loadout:** no attachments.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_SR_Standing`.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_Weapon_StanceRecoil_SR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_Weapon_StanceRecoil_SR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.285 | — | 0.285 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 100 | — | 100 |

### DMR

#### BMR-308 (ID_RFB)

Item `Id.Item.RFB`, [`ID_RFB.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/DMR/RFB/Content/Data/ID_RFB.json).

- **Loadout:** Magazine: `ID_RFB_Mag_Standard`; Barrel: `ID_RFBBarrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_DMR_Standing`.
- **Character effects:** `GE_MAG_FAL_10rd_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 0.84 `GE_MAG_FAL_10rd`<br>×c 1 `GE_Weapon_StanceRecoil_DMR_Standing` | 0.84 |
| HorizontalRecoilMultiplier | 1 | ×c 0.85 `GE_MAG_FAL_10rd`<br>×c 1 `GE_Weapon_StanceRecoil_DMR_Standing` | 0.85 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.52 | ×c 0.85 `GE_MAG_FAL_10rd` | 0.442 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 300 | — | 300 |
| EquipSpeedMultiplier | 0.92 | ×c 1.24 `GE_MAG_FAL_10rd` | 1.1408 |
| HolsterSpeedMultiplier | 1 | — | 1 |

† Sight default `Id.Item.ARMIrons` (on `ID_RFB`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.

#### M14 (ID_WEPN_034)

Item `Id.Item.WEPN_034`, [`ID_WEPN_034.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/Data/ID_WEPN_034.json).

- **Loadout:** Magazine: `ID_MAGZ_068`; Stock: `ID_STOK_059`; Barrel: `ID_BARL_047`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_DMR_Standing`.
- **Character effects:** `GE_MAGZ_068_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_068`<br>×c 1 `GE_Weapon_StanceRecoil_DMR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_068`<br>×c 1 `GE_Weapon_StanceRecoil_DMR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.53 | ×c 1 `GE_MAGZ_068` | 0.53 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 500 | — | 500 |
| EquipSpeedMultiplier | 0.97 | ×c 1 `GE_MAGZ_068` | 0.97 |
| HolsterSpeedMultiplier | 1 | — | 1 |

#### SKS (ID_SKS)

Item `Id.Item.SKS`, [`ID_SKS.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_007/Content/Data/ID_SKS.json).

- **Loadout:** Magazine: `ID_SKS_Mag_Internal`; Handguard: `ID_SKSHandguard`; Barrel: `ID_SKSBarrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_DMR_Standing`.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_Weapon_StanceRecoil_DMR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_Weapon_StanceRecoil_DMR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.53 | — | 0.53 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 1000 | — | 1000 |
| EquipSpeedMultiplier | 1.15 | — | 1.15 |
| HolsterSpeedMultiplier | 1.1 | — | 1.1 |

† Grip default `Id.Item.SKSPistolGrip` (on `ID_SKS`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.

#### SVD (ID_SVDM)

Item `Id.Item.SVDM`, [`ID_SVDM.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/DMR/SVDM/Content/Data/ID_SVDM.json).

- **Loadout:** Magazine: `ID_SVDM_Mag_Standard`; Handguard: `ID_SVDMHandguard`; Stock: `ID_SVDMStock`; Barrel: `ID_SVDMBarrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_DMR_Standing`.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAG_SVDM`<br>×c 1 `GE_Weapon_StanceRecoil_DMR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAG_SVDM`<br>×c 1 `GE_Weapon_StanceRecoil_DMR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.53 | ×c 1.06 `GE_MAG_SVDM` | 0.5618 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 1100 | — | 1100 |
| EquipSpeedMultiplier | 0.97 | ×c 0.9 `GE_MAG_SVDM` | 0.873 |
| HolsterSpeedMultiplier | 1 | — | 1 |

#### TCX-SPR (ID_WEPN_037)

Item `Id.Item.WEPN_037`, [`ID_WEPN_037.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_037/Content/Data/ID_WEPN_037.json).

- **Loadout:** Magazine: `ID_MAGZ_069`; Handguard: `ID_HNDG_054`; Grip: `ID_PGRP_043`; Stock: `ID_STOK_060`; Barrel: `ID_BARL_048`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_AR_Standing`.
- **Character effects:** `GE_MAGZ_069_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_069`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_069`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.48 | ×c 1 `GE_MAGZ_069` | 0.48 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 200 | — | 200 |
| EquipSpeedMultiplier | 1 | ×c 1 `GE_MAGZ_069` | 1 |
| HolsterSpeedMultiplier | 0.95 | — | 0.95 |

### LMG

#### Evo-3 Ultra (ID_WEPN_036)

Item `Id.Item.WEPN_036`, [`ID_WEPN_036.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_036/Content/Data/ID_WEPN_036.json).

- **Loadout:** Magazine: `ID_MAGZ_067`; Grip: `ID_PGRP_042`; Stock: `ID_STOK_058`; Barrel: `ID_BARL_046`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_AR_Standing`.
- **Character effects:** `GE_MAGZ_067_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_067`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_067`<br>×c 1 `GE_Weapon_StanceRecoil_AR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.64 | ×c 1 `GE_MAGZ_067` | 0.64 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 500 | — | 500 |
| EquipSpeedMultiplier | 1 | ×c 1 `GE_MAGZ_067` | 1 |
| HolsterSpeedMultiplier | 1 | — | 1 |

#### M249 SAW (ID_M249)

Item `Id.Item.M249`, [`ID_M249.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_009/Content/Data/ID_M249.json).

- **Loadout:** Magazine: `ID_M249_Mag_Standard`; Stock: `ID_M249Stock`; Barrel: `ID_M249Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_LMG_Standing`.
- **Character effects:** `GE_MAG_M249_200rd_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1.17 `GE_MAG_M249_200rd`<br>×c 1 `GE_Weapon_StanceRecoil_LMG_Standing` | 1.17 |
| HorizontalRecoilMultiplier | 1 | ×c 1.17 `GE_MAG_M249_200rd`<br>×c 1 `GE_Weapon_StanceRecoil_LMG_Standing` | 1.17 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.68 | ×c 1.2 `GE_MAG_M249_200rd` | 0.816 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 200 | — | 200 |
| MaxZeroingRange | 1200 | — | 1200 |
| EquipSpeedMultiplier | 0.95 | ×c 0.93 `GE_MAG_M249_200rd` | 0.8835 |
| HolsterSpeedMultiplier | 0.95 | — | 0.95 |

† Grip default `Id.Item.RK3PistolGrip` (on `ID_M249`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.

#### PKM (ID_LMG_02)

Item `Id.Item.LMG_02`, [`ID_LMG_02.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/LMG/LMG_02/Content/Data/ID_LMG_02.json).

- **Loadout:** Magazine: `ID_LMG_02_Magazine_Standard`; Grip: `ID_LMG_02PistolGrip`; Stock: `ID_LMG_02Stock`; Barrel: `ID_LMG_02Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_LMG_Standing`.
- **Character effects:** `GE_MAG_LMG_02_100rd_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAG_LMG_02_100rd`<br>×c 1 `GE_Weapon_StanceRecoil_LMG_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAG_LMG_02_100rd`<br>×c 1 `GE_Weapon_StanceRecoil_LMG_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.73 | ×c 1.1 `GE_MAG_LMG_02_100rd` | 0.803 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 1500 | — | 1500 |
| EquipSpeedMultiplier | 0.95 | — | 0.95 |
| HolsterSpeedMultiplier | 1 | — | 1 |

### Launcher

#### 9K333 Verba (ID_Launcher_04)

Item `Id.Item.Launcher_04`, [`ID_Launcher_04.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/Launcher_04/Content/Data/ID_Launcher_04.json).

- **Loadout:** no attachments.
- **Stance (Stand):** no stance effect.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | — | 1 |
| HorizontalRecoilMultiplier | 1 | — | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.5 | — | 0.5 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 100 | — | 100 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 1000 | — | 1000 |
| HolsterSpeedMultiplier | 1.15 | — | 1.15 |

#### MAAWS (ID_CGM4)

Item `Id.Item.CGM4`, [`ID_CGM4.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_013/Content/Data/ID_CGM4.json).

- **Loadout:** Sight: `ID_SGHT_033`.
- **Sight:** `ID_SGHT_033` `S_Aim01`.
- **Stance (Stand):** no stance effect.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | — | 1 |
| HorizontalRecoilMultiplier | 1 | — | 1 |
| AdsZoomMultiplier | 1.2 | = 1.2 `GE_SGHT_033` | 1.2 |
| AimTime | 0.5 | ×c 1 `GE_SGHT_033` | 0.5 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 100 | — | 100 |
| EquipSpeedMultiplier | 0.95 | — | 0.95 |
| HolsterSpeedMultiplier | 1 | — | 1 |

#### MGL-40 (ID_MMGL)

Item `Id.Item.MMGL`, [`ID_MMGL.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_012/Content/Data/ID_MMGL.json).

- **Loadout:** Sight: `ID_SGHT_037`; Magazine: `ID_MMGL_Mag_Internal`; Barrel: `ID_MMGLBarrel`; Handguard: `ID_MMGLHandguard`; Grip: `ID_MMGLGrip`; Stock: `ID_MMGLStock`.
- **Sight:** `ID_SGHT_037` `S_Aim01`.
- **Stance (Stand):** no stance effect.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | — | 1 |
| HorizontalRecoilMultiplier | 1 | — | 1 |
| AdsZoomMultiplier | 1.2 | = 1.2 `GE_SGHT_037` | 1.2 |
| AimTime | 0.4 | ×c 1 `GE_SGHT_037` | 0.4 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 50 | — | 50 |
| MaxZeroingRange | 400 | — | 400 |
| EquipSpeedMultiplier | 0.95 | — | 0.95 |
| HolsterSpeedMultiplier | 1 | — | 1 |

#### RPG-7 (ID_RPG7)

Item `Id.Item.RPG7`, [`ID_RPG7.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/RPG7/Content/Data/ID_RPG7.json).

- **Loadout:** no attachments.
- **Stance (Stand):** no stance effect.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | — | 1 |
| HorizontalRecoilMultiplier | 1 | — | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.5 | — | 0.5 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 500 | — | 500 |
| EquipSpeedMultiplier | 0.95 | — | 0.95 |
| HolsterSpeedMultiplier | 1 | — | 1 |

### Pistol

#### Deagle (ID_WEPN_027)

Item `Id.Item.WEPN_027`, [`ID_WEPN_027.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_027/Content/Data/ID_WEPN_027.json).

- **Loadout:** Magazine: `ID_MAGZ_003`; Barrel: `ID_BARL_004`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_Pistol_Standing`.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_003`<br>×c 1 `GE_Weapon_StanceRecoil_Pistol_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_003`<br>×c 1 `GE_Weapon_StanceRecoil_Pistol_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.25 | ×c 1 `GE_MAGZ_003` | 0.25 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 50 | — | 50 |
| MaxZeroingRange | 50 | — | 50 |
| EquipSpeedMultiplier | 0.9 | — | 0.9 |
| HolsterSpeedMultiplier | 0.85 | — | 0.85 |

#### GGX 17 (ID_Glock17)

Item `Id.Item.Glock17`, [`ID_Glock17.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_010/Content/Data/ID_Glock17.json).

- **Loadout:** Magazine: `ID_Glock17_Mag_Standard`; Barrel: `ID_Glock17Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_Pistol_Standing`.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAG_Glock_17rd`<br>×c 1 `GE_Weapon_StanceRecoil_Pistol_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAG_Glock_17rd`<br>×c 1 `GE_Weapon_StanceRecoil_Pistol_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.2 | ×c 1 `GE_MAG_Glock_17rd` | 0.2 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 50 | — | 50 |
| MaxZeroingRange | 50 | — | 50 |
| EquipSpeedMultiplier | 1.2 | — | 1.2 |
| HolsterSpeedMultiplier | 1.1 | — | 1.1 |

#### GGX 18 (ID_WEPN_032)

Item `Id.Item.WEPN_032`, [`ID_WEPN_032.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_032/Content/Data/ID_WEPN_032.json).

- **Loadout:** Magazine: `ID_Glock17_Mag_Standard`; Barrel: `ID_Glock17Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_Pistol_Standing`.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAG_Glock_17rd`<br>×c 1 `GE_Weapon_StanceRecoil_Pistol_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAG_Glock_17rd`<br>×c 1 `GE_Weapon_StanceRecoil_Pistol_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.2 | ×c 1 `GE_MAG_Glock_17rd` | 0.2 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 50 | — | 50 |
| MaxZeroingRange | 50 | — | 50 |
| EquipSpeedMultiplier | 1.2 | — | 1.2 |
| HolsterSpeedMultiplier | 1.15 | — | 1.15 |

#### Judge (ID_Judge)

Item `Id.Item.Judge`, [`ID_Judge.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Pistols/Pistol_02/Content/Data/ID_Judge.json).

- **Loadout:** Magazine: `ID_Judge_Mag_Internal`; Grip: `ID_JudgePistolgrip`; Barrel: `ID_JudgeBarrel`.
- **Stance (Stand):** no stance effect.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | — | 1 |
| HorizontalRecoilMultiplier | 1 | — | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.35 | — | 0.35 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 25 | — | 25 |
| MaxZeroingRange | 25 | — | 25 |
| EquipSpeedMultiplier | 0.95 | — | 0.95 |
| HolsterSpeedMultiplier | 1.15 | — | 1.15 |

#### M1911 (ID_WEPN_026)

Item `Id.Item.WEPN_026`, [`ID_WEPN_026.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_026/Content/Data/ID_WEPN_026.json).

- **Loadout:** Magazine: `ID_MAGZ_002`; Barrel: `ID_BARL_003`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_Pistol_Standing`.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_002`<br>×c 1 `GE_Weapon_StanceRecoil_Pistol_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_002`<br>×c 1 `GE_Weapon_StanceRecoil_Pistol_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.2 | ×c 1 `GE_MAGZ_002` | 0.2 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 25 | — | 25 |
| MaxZeroingRange | 25 | — | 25 |
| EquipSpeedMultiplier | 0.92 | — | 0.92 |
| HolsterSpeedMultiplier | 1 | — | 1 |

### SMG

#### AMP-9 (ID_MP9)

Item `Id.Item.MP9`, [`ID_MP9.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_014/Content/Data/ID_MP9.json).

- **Loadout:** Magazine: `ID_MP9_Mag_Standard`; Barrel: `ID_MP9Barrel`; Stock: `ID_MP9Stock`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_SMG_Standing`.
- **Character effects:** `GE_MAGZ_043_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1.12 `GE_MAGZ_043`<br>×c 1 `GE_Weapon_StanceRecoil_SMG_Standing` | 1.12 |
| HorizontalRecoilMultiplier | 1 | ×c 1.14 `GE_MAGZ_043`<br>×c 1 `GE_Weapon_StanceRecoil_SMG_Standing` | 1.14 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.25 | ×c 1.11 `GE_MAGZ_043` | 0.2775 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 50 | — | 50 |
| MaxZeroingRange | 100 | — | 100 |
| EquipSpeedMultiplier | 1.12 | ×c 0.93 `GE_MAGZ_043` | 1.0416 |
| HolsterSpeedMultiplier | 1.2 | — | 1.2 |

#### MP5 (ID_WEPN_028)

Item `Id.Item.WEPN_028`, [`ID_WEPN_028.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_028/Content/Data/ID_WEPN_028.json).

- **Loadout:** Magazine: `ID_MAGZ_004`; Stock: `ID_STOK_003`; Barrel: `ID_BARL_005`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_SMG_Standing`.
- **Character effects:** `GE_MAGZ_004_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_004`<br>×c 1 `GE_Weapon_StanceRecoil_SMG_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_004`<br>×c 1 `GE_Weapon_StanceRecoil_SMG_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.285 | ×c 1 `GE_MAGZ_004` | 0.285 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 25 | — | 25 |
| MaxZeroingRange | 100 | — | 100 |
| EquipSpeedMultiplier | 1.05 | — | 1.05 |
| HolsterSpeedMultiplier | 0.9 | — | 0.9 |

#### PP-19 Bizon (ID_WEPN_031)

Item `Id.Item.WEPN_031`, [`ID_WEPN_031.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_031/Content/Data/ID_WEPN_031.json).

- **Loadout:** Handguard: `ID_HNDG_055`; Magazine: `ID_MAGZ_051`; Grip: `ID_SMG_03PistolGrip`; Stock: `ID_SMG_03Stock`; Barrel: `ID_BARL_049`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_SMG_Standing`.
- **Character effects:** `GE_MAGZ_051_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_051`<br>×c 1 `GE_Weapon_StanceRecoil_SMG_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_051`<br>×c 1 `GE_Weapon_StanceRecoil_SMG_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.285 | ×c 1 `GE_MAGZ_051` | 0.285 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 50 | — | 50 |
| MaxZeroingRange | 200 | — | 200 |
| EquipSpeedMultiplier | 0.94 | ×c 1 `GE_MAGZ_051` | 0.94 |
| HolsterSpeedMultiplier | 1.15 | — | 1.15 |

#### PP-19 Vityaz (ID_SMG_03)

Item `Id.Item.SMG_03`, [`ID_SMG_03.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/SMG/SMG_03/Content/Data/ID_SMG_03.json).

- **Loadout:** Magazine: `ID_SMG_03_Mag_Standard`; Grip: `ID_SMG_03PistolGrip`; Stock: `ID_SMG_03Stock`; Barrel: `ID_SMG_03Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_SMG_Standing`.
- **Character effects:** `GE_MAG_SMG_03_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAG_SMG_03`<br>×c 1 `GE_Weapon_StanceRecoil_SMG_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAG_SMG_03`<br>×c 1 `GE_Weapon_StanceRecoil_SMG_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.285 | ×c 1 `GE_MAG_SMG_03` | 0.285 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 50 | — | 50 |
| MaxZeroingRange | 200 | — | 200 |
| EquipSpeedMultiplier | 0.94 | — | 0.94 |
| HolsterSpeedMultiplier | 1.15 | — | 1.15 |

#### Super-45 (ID_Vector)

Item `Id.Item.Vector`, [`ID_Vector.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_006/Content/Data/ID_Vector.json).

- **Loadout:** Magazine: `ID_Vector_Mag_Standard`; Stock: `ID_VectorStock`; Barrel: `ID_VectorBarrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_SMG_Standing`.
- **Character effects:** `GE_MAGZ_008_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_008`<br>×c 1 `GE_Weapon_StanceRecoil_SMG_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAGZ_008`<br>×c 1 `GE_Weapon_StanceRecoil_SMG_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.25 | ×c 1 `GE_MAGZ_008` | 0.25 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 50 | — | 50 |
| MaxZeroingRange | 100 | — | 100 |
| EquipSpeedMultiplier | 1 | — | 1 |
| HolsterSpeedMultiplier | 1 | — | 1 |

### Shotgun

#### M500 (ID_M500)

Item `Id.Item.M500`, [`ID_M500.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_011/Content/Data/ID_M500.json).

- **Loadout:** Magazine: `ID_M12G_Mag_Internal`; Stock: `ID_M500Stock`; Barrel: `ID_M500Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_Shotgun_Standing`.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_Weapon_StanceRecoil_Shotgun_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_Weapon_StanceRecoil_Shotgun_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.365 | — | 0.365 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 100 | — | 100 |
| EquipSpeedMultiplier | 0.95 | — | 0.95 |
| HolsterSpeedMultiplier | 1 | — | 1 |

#### MP43 (ID_MP43)

Item `Id.Item.MP43`, [`ID_MP43.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Shotgun/MP43/Content/Data/ID_MP43.json).

- **Loadout:** Handguard: `ID_MP43Handguard`; Stock: `ID_MP43Stock`; Barrel: `ID_MP43Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_Shotgun_Standing`.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_Weapon_StanceRecoil_Shotgun_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_Weapon_StanceRecoil_Shotgun_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.35 | — | 0.35 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 70 | — | 70 |
| MaxZeroingRange | 70 | — | 70 |
| EquipSpeedMultiplier | 1.25 | — | 1.25 |
| HolsterSpeedMultiplier | 0.95 | — | 0.95 |

### Sniper

#### AMR 50 (ID_SR_04)

Item `Id.Item.SR_04`, [`ID_SR_04.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Sniper/SR_04/Content/Data/ID_SR_04.json).

- **Loadout:** Magazine: `ID_SR_04_Mag_Standard`; Handguard: `ID_SR_04Handguard`; Stock: `ID_SR_04Stock`; Barrel: `ID_SR_04Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_SR_Standing`.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAG_SR_04_5rd`<br>×c 1 `GE_Weapon_StanceRecoil_SR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAG_SR_04_5rd`<br>×c 1 `GE_Weapon_StanceRecoil_SR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.68 | ×c 1 `GE_MAG_SR_04_5rd` | 0.68 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 300 | — | 300 |
| EquipSpeedMultiplier | 0.9 | — | 0.9 |
| HolsterSpeedMultiplier | 1.15 | — | 1.15 |

† Sight default `Id.Item.ARMIrons` (on `ID_SR_04`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.

#### MK22 (ID_MK22)

Item `Id.Item.MK22`, [`ID_MK22.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Sniper/MK22/Content/Data/ID_MK22.json).

- **Loadout:** Magazine: `ID_MK22_Mag_Standard`; Grip: `ID_MK22Grip`; Stock: `ID_MK22Stock`; Barrel: `ID_MK22Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_SR_Standing`.
- **Character effects:** `GE_MAG_MK22_10rd_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAG_MK22_10rd`<br>×c 1 `GE_Weapon_StanceRecoil_SR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAG_MK22_10rd`<br>×c 1 `GE_Weapon_StanceRecoil_SR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.675 | ×c 1.06 `GE_MAG_MK22_10rd` | 0.7155 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 300 | — | 300 |
| EquipSpeedMultiplier | 1.05 | ×c 0.9 `GE_MAG_MK22_10rd` | 0.945 |
| HolsterSpeedMultiplier | 1.17 | — | 1.17 |

† Sight default `Id.Item.ARMIrons` (on `ID_MK22`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.

#### Mosin Nagant (ID_WEPN_017)

Item `Id.Item.Mosin`, [`ID_WEPN_017.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/ID_WEPN_017.json).

- **Loadout:** Magazine: `ID_Mosin_MagInternal`; Barrel: `ID_MosinBarrel`; Stock: `ID_MosinStock`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_SR_Standing`.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_Weapon_StanceRecoil_SR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_Weapon_StanceRecoil_SR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.65 | — | 0.65 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 200 | — | 200 |
| MaxZeroingRange | 800 | — | 800 |
| EquipSpeedMultiplier | 0.94 | — | 0.94 |
| HolsterSpeedMultiplier | 1 | — | 1 |

#### Scout Rifle TD (ID_WEPN_035)

Item `Id.Item.WEPN_035`, [`ID_WEPN_035.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_035/Content/Data/ID_WEPN_035.json).

- **Loadout:** Stock: `ID_STOK_057`; Barrel: `ID_BARL_045`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_SR_Standing`.
- **Character effects:** none.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_Weapon_StanceRecoil_SR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_Weapon_StanceRecoil_SR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.5 | — | 0.5 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 100 | — | 100 |
| EquipSpeedMultiplier | 1 | — | 1 |
| HolsterSpeedMultiplier | 1 | — | 1 |

† Sight default `Id.Item.IRNS_008` (on `ID_WEPN_035`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.

#### SV98 (ID_SV98)

Item `Id.Item.SV98`, [`ID_SV98.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_008/Content/Data/ID_SV98.json).

- **Loadout:** Magazine: `ID_SV98_Mag_Standard`; Stock: `ID_SV98Stock`; Barrel: `ID_SV98Barrel`.
- **Stance (Stand):** `GE_Weapon_StanceRecoil_SR_Standing`.
- **Character effects:** `GE_MAG_SV98_10rd_CharacterEffects`.

| Attribute | Base | Modifiers | Final |
|---|---:|---|---:|
| VerticalRecoilMultiplier | 1 | ×c 1 `GE_MAG_SV98_10rd`<br>×c 1 `GE_Weapon_StanceRecoil_SR_Standing` | 1 |
| HorizontalRecoilMultiplier | 1 | ×c 1 `GE_MAG_SV98_10rd`<br>×c 1 `GE_Weapon_StanceRecoil_SR_Standing` | 1 |
| AdsZoomMultiplier | 1.2 | — | 1.2 |
| AimTime | 0.6 | ×c 1 `GE_MAG_SV98_10rd` | 0.6 |
| SpreadMultiplier | 1 | — | 1 |
| AccuracyMultiplier | 1 | — | 1 |
| Length | 80 | — | 80 |
| MinZeroingRange | 100 | — | 100 |
| MaxZeroingRange | 100 | — | 100 |
| EquipSpeedMultiplier | 0.95 | — | 0.95 |
| HolsterSpeedMultiplier | 1 | — | 1 |

## 3. Attachments

The 246 attachment items at least one weapon accepts, grouped by `AttachmentType`. **On the weapon** lists the modifiers of `AppliedEffects`; **Sight** those of each `SightsData` entry in data order; **Bipod unfolded** those of the unfolded list (`+0x138`); **Bipod mounted** those of `MountedAppliedEffects` (`+0x158`), which replace the unfolded lists while mounted. **Character** names the effects that go to the character instead (`AppliedCharacterEffects`, the bipod's unfolded `+0x148` list and its mounted `MountedAppliedCharacterEffects`, `+0x168`). **Accepted by** lists the weapons with a sub-slot that accepts the item, on the weapon itself or on an attachment it accepts (a muzzle on a barrel, an underbarrel on a handguard).

### Barrel (36)

| Attachment | Weapon-side modifiers | Character | Accepted by |
|---|---|---|---|
| `ID_A91Barrel` | — | — | A91 |
| `ID_AK74MBarrel` | — | — | AK74M |
| `ID_AR_01_BRL_02` | — | — | AK74M |
| `ID_AR_02_BRL_01` | — | — | M4 |
| M1911 Barrel (`ID_BARL_003`) | — | — | WEPN_026 |
| Deagle Barrel (`ID_BARL_004`) | — | — | WEPN_027 |
| MP5 Barrel (`ID_BARL_005`) | — | — | WEPN_028 |
| Galil Barrel (`ID_BARL_006`) | — | — | WEPN_029 |
| `ID_BARL_007` | — | — | WEPN_030 |
| `ID_BARL_044` | — | — | WEPN_033 |
| Scout Rifle Standard Barrel (`ID_BARL_045`) | — | — | WEPN_035 |
| WEPN_036 Evoly Standard Barrel (`ID_BARL_046`) | — | — | WEPN_036 |
| WEPN_034 M14 Standard Barrel (`ID_BARL_047`) | — | — | WEPN_034 |
| Sig Spear (WEPN_037) Standard Barrel (`ID_BARL_048`) | — | — | WEPN_037 |
| WEPN_031 Bizon Standard Barrel (`ID_BARL_049`) | — | — | WEPN_031 |
| `ID_Glock17Barrel` | — | — | Glock17, WEPN_032 |
| `ID_JudgeBarrel` | — | — | Judge |
| `ID_KH2002Barrel` | — | — | KH2002 |
| `ID_LMG_02Barrel` | — | — | LMG_02 |
| `ID_M249Barrel` | — | — | M249 |
| M4 Barrel (`ID_M4Barrel`) | — | — | M4 |
| `ID_M500Barrel` | — | — | M500 |
| `ID_MK22Barrel` | — | — | MK22 |
| `ID_MMGLBarrel` | — | — | MMGL |
| `ID_MosinBarrel` | — | — | WEPN_017 |
| `ID_MP43Barrel` | — | — | MP43 |
| `ID_MP9Barrel` | — | — | MP9 |
| `ID_Pistol_01_BRL_07` | — | — | Glock17, WEPN_032 |
| `ID_RFBBarrel` | — | — | RFB |
| `ID_SKSBarrel` | — | — | SKS |
| `ID_SMG_03Barrel` | — | — | SMG_03 |
| `ID_SR_04Barrel` | — | — | SR_04 |
| `ID_SV98Barrel` | — | — | SV98 |
| `ID_SVDMBarrel` | — | — | SVDM |
| `ID_Tar21Barrel` | — | — | TAR21 |
| `ID_VectorBarrel` | — | — | Vector |

### Bipod (9)

| Attachment | Weapon-side modifiers | Character | Accepted by |
|---|---|---|---|
| Grip Pod (`ID_FGP_04`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.88, HorizontalRecoilMultiplier ×c 0.9, SpreadMultiplier ×c 0.94, AimTime ×c 1.1, EquipSpeedMultiplier ×c 0.98<br>**Bipod unfolded:** VerticalRecoilMultiplier ×c 1.15, HorizontalRecoilMultiplier ×c 1.15, SpreadMultiplier ×c 1.15, AimTime ×c 1.05<br>**Bipod mounted:** VerticalRecoilMultiplier ×c 0.25, HorizontalRecoilMultiplier ×c 0.28, SpreadMultiplier ×c 0.45, AimTime ×c 0.92 | `GE_FGP_04_NonBipodState_CharacterEffects`, `GE_FGP_04_UnfoldedBipodState_CharacterEffects`, `GE_FGP_04_BipodState_CharacterEffects` | AK74M, M249, M4, MP9, SMG_03, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_036, WEPN_037 |
| PKM Bipod (`ID_FGRP_008`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 1, AimTime ×c 1<br>**Bipod unfolded:** VerticalRecoilMultiplier ×c 1.15, HorizontalRecoilMultiplier ×c 1.15, SpreadMultiplier ×c 1.15, AimTime ×c 1.05<br>**Bipod mounted:** VerticalRecoilMultiplier ×c 0.2, HorizontalRecoilMultiplier ×c 0.22, SpreadMultiplier ×c 1, AimTime ×c 0.88 | `GE_FGRP_008_UnfoldedBipodState_CharacterEffects`, `GE_FGRP_008_BipodState_CharacterEffects` | LMG_02 |
| SV98 Bipod (`ID_FGRP_009`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 1, AimTime ×c 1<br>**Bipod unfolded:** VerticalRecoilMultiplier ×c 1.15, HorizontalRecoilMultiplier ×c 1.15, SpreadMultiplier ×c 1.15, AimTime ×c 1.05<br>**Bipod mounted:** VerticalRecoilMultiplier ×c 0.45, HorizontalRecoilMultiplier ×c 0.35, SpreadMultiplier ×c 0.45, AimTime ×c 0.84 | `GE_FGRP_009_UnfoldedBipodState_CharacterEffects`, `GE_FGRP_009_BipodState_CharacterEffects` | SV98 |
| SKS Bipod (`ID_FGRP_010`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 1, AimTime ×c 1<br>**Bipod unfolded:** VerticalRecoilMultiplier ×c 1.15, HorizontalRecoilMultiplier ×c 1.15, SpreadMultiplier ×c 1.15, AimTime ×c 1.05<br>**Bipod mounted:** VerticalRecoilMultiplier ×c 0.65, HorizontalRecoilMultiplier ×c 0.4, SpreadMultiplier ×c 0.45, AimTime ×c 0.86 | `GE_FGRP_010_UnfoldedBipodState_CharacterEffects`, `GE_FGRP_010_BipodState_CharacterEffects` | SKS |
| SVD Bipod (`ID_FGRP_011`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 1, AimTime ×c 1<br>**Bipod unfolded:** VerticalRecoilMultiplier ×c 1.15, HorizontalRecoilMultiplier ×c 1.15, SpreadMultiplier ×c 1.15, AimTime ×c 1.05<br>**Bipod mounted:** VerticalRecoilMultiplier ×c 0.65, HorizontalRecoilMultiplier ×c 0.35, SpreadMultiplier ×c 0.45, AimTime ×c 0.86 | `GE_FGRP_011_UnfoldedBipodState_CharacterEffects`, `GE_FGRP_011_BipodState_CharacterEffects` | SVDM |
| M249 Bipod (`ID_FGRP_012`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 1, AimTime ×c 1<br>**Bipod unfolded:** VerticalRecoilMultiplier ×c 1.15, HorizontalRecoilMultiplier ×c 1.15, SpreadMultiplier ×c 1.15, AimTime ×c 1.05<br>**Bipod mounted:** VerticalRecoilMultiplier ×c 0.2, HorizontalRecoilMultiplier ×c 0.25, SpreadMultiplier ×c 1, AimTime ×c 0.88 | `GE_FGRP_012_UnfoldedBipodState_CharacterEffects`, `GE_FGRP_012_BipodState_CharacterEffects` | M249 |
| Pro Tilt Bipod (`ID_FGRP_013`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 1, AimTime ×c 1<br>**Bipod unfolded:** VerticalRecoilMultiplier ×c 1.15, HorizontalRecoilMultiplier ×c 1.15, SpreadMultiplier ×c 1.15, AimTime ×c 1.05<br>**Bipod mounted:** VerticalRecoilMultiplier ×c 0.65, HorizontalRecoilMultiplier ×c 0.5, SpreadMultiplier ×c 0.45, AimTime ×c 0.83 | `GE_FGRP_013_UnfoldedBipodState_CharacterEffects`, `GE_FGRP_013_BipodState_CharacterEffects` | MK22, RFB, SR_04 |
| Evo-3 Ultra Bipod (`ID_FGRP_019`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 1, AimTime ×c 1<br>**Bipod unfolded:** VerticalRecoilMultiplier ×c 1.15, HorizontalRecoilMultiplier ×c 1.15, SpreadMultiplier ×c 1.15, AimTime ×c 1.05<br>**Bipod mounted:** VerticalRecoilMultiplier ×c 0.4, HorizontalRecoilMultiplier ×c 0.3, SpreadMultiplier ×c 1, AimTime ×c 0.88 | `GE_FGRP_019_UnfoldedBipodState_CharacterEffects`, `GE_FGRP_019_BipodState_CharacterEffects` | WEPN_036 |
| M14 Bipod (`ID_FGRP_020`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 1, AimTime ×c 1<br>**Bipod unfolded:** VerticalRecoilMultiplier ×c 1.15, HorizontalRecoilMultiplier ×c 1.15, SpreadMultiplier ×c 1.15, AimTime ×c 1.05<br>**Bipod mounted:** VerticalRecoilMultiplier ×c 0.6, HorizontalRecoilMultiplier ×c 0.35, SpreadMultiplier ×c 1, AimTime ×c 0.88 | `GE_FGRP_020_UnfoldedBipodState_CharacterEffects`, `GE_FGRP_020_BipodState_CharacterEffects` | WEPN_034 |

### Grip (26)

| Attachment | Weapon-side modifiers | Character | Accepted by |
|---|---|---|---|
| `ID_AK74MIMIEGGrip` | — | — | AK74M |
| AK74M Grip (`ID_AK74MPistolGrip`) | — | — | AK74M |
| `ID_AR_02_GRP_05` | **On the weapon:** HorizontalRecoilMultiplier = 0, VerticalRecoilMultiplier = 0 | — | M4 |
| TDG Vertical Foregrip (`ID_FGP_02`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.7, HorizontalRecoilMultiplier ×c 0.85, SpreadMultiplier ×c 0.83, AimTime ×c 1.1, EquipSpeedMultiplier ×c 0.92 | `GE_FGP_02_CharacterEffects` | AK74M, M249, M4, M500, MP9, RFB, SMG_03, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_036, WEPN_037 |
| AFG Angled Foregrip (`ID_FGP_03`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.94, HorizontalRecoilMultiplier ×c 0.75, SpreadMultiplier ×c 0.78, AimTime ×c 0.85, EquipSpeedMultiplier ×c 1.1 | `GE_FGP_03_CharacterEffects` | AK74M, M249, M4, M500, MP9, RFB, SMG_03, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_036, WEPN_037 |
| RVG Vertical Foregrip (`ID_FGRP_006`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.75, HorizontalRecoilMultiplier ×c 0.87, SpreadMultiplier ×c 0.81, AimTime ×c 0.9, EquipSpeedMultiplier ×c 1.07 | `GE_FGRP_006_CharacterEffects` | AK74M, M249, M4, M500, MP9, RFB, SMG_03, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_036, WEPN_037 |
| Shift Foregrip (`ID_FGRP_007`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.92, HorizontalRecoilMultiplier ×c 0.71, SpreadMultiplier ×c 0.76, AimTime ×c 0.87, EquipSpeedMultiplier ×c 1.15 | `GE_FGRP_007_CharacterEffects` | AK74M, M249, M4, M500, MP9, RFB, SMG_03, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_036, WEPN_037 |
| CQR Tactical Front Rail Grip (`ID_FGRP_014`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.7, HorizontalRecoilMultiplier ×c 0.97, SpreadMultiplier ×c 0.91, AimTime ×c 1.15, EquipSpeedMultiplier ×c 1.09 | `GE_FGRP_014_CharacterEffects` | AK74M, M249, M4, M500, WEPN_029, WEPN_030, WEPN_036 |
| Rubberized Ergonomic Foregrip (`ID_FGRP_015`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.82, HorizontalRecoilMultiplier ×c 0.93, SpreadMultiplier ×c 0.84, AimTime ×c 1.02, EquipSpeedMultiplier ×c 0.98 | `GE_FGRP_015_CharacterEffects` | AK74M, M249, M4, M500, MP9, RFB, SMG_03, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_036, WEPN_037 |
| 45° Angled Foregrip (`ID_FGRP_016`) | **On the weapon:** VerticalRecoilMultiplier ×c 1.05, HorizontalRecoilMultiplier ×c 0.82, SpreadMultiplier ×c 0.82, AimTime ×c 0.83, EquipSpeedMultiplier ×c 1.13 | `GE_FGRP_016_CharacterEffects` | AK74M, M249, M4, M500, MP9, RFB, SMG_03, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_036, WEPN_037 |
| Angled Tactical Foregrip (`ID_FGRP_017`) | **On the weapon:** VerticalRecoilMultiplier ×c 1.02, HorizontalRecoilMultiplier ×c 0.84, SpreadMultiplier ×c 0.84, AimTime ×c 0.88, EquipSpeedMultiplier ×c 1.09 | `GE_FGRP_017_CharacterEffects` | AK74M, M249, M4, M500, MP9, RFB, SMG_03, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_036, WEPN_037 |
| Mini Angled Foregrip (`ID_FGRP_018`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.95, HorizontalRecoilMultiplier ×c 0.77, SpreadMultiplier ×c 0.8, AimTime ×c 0.86, EquipSpeedMultiplier ×c 1.1 | `GE_FGRP_018_CharacterEffects` | AK74M, M249, M4, M500, MP9, RFB, SMG_03, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_036, WEPN_037 |
| `ID_JudgePistolgrip` | — | — | Judge |
| `ID_LMG_02PistolGrip` | — | — | LMG_02 |
| M4 Pistol Grip (`ID_M4Grip`) | — | — | M4 |
| `ID_MK22Grip` | — | — | MK22 |
| `ID_MMGLGrip` | — | — | MMGL |
| FAL Pistol Grip (`ID_PGRP_003`) | — | — | WEPN_030 |
| Galil Pistol Grip (`ID_PGRP_010`) | — | — | WEPN_029 |
| `ID_PGRP_041` | — | — | WEPN_035 |
| WEPN_36 Evoly Grip (`ID_PGRP_042`) | — | — | WEPN_036 |
| Sig Spear (WEPN_037) Standard Pistol Grip (`ID_PGRP_043`) | — | — | WEPN_037 |
| Kungfu (`ID_PGRP_044`) | — | — | WEPN_037 |
| `ID_Pistol_01_GRP_01` | — | — | Glock17, WEPN_032 |
| RK6 Tactical Foregrip (`ID_RK6_Grip`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.85, HorizontalRecoilMultiplier ×c 0.92, SpreadMultiplier ×c 0.85, AimTime ×c 1.1, EquipSpeedMultiplier ×c 1 | `GE_RK6_CharacterEffects` | AK74M, M249, M4, M500, MP9, RFB, SMG_03, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_036, WEPN_037 |
| `ID_SMG_03PistolGrip` | — | — | SMG_03, WEPN_031 |

### Handguard (6)

| Attachment | Weapon-side modifiers | Character | Accepted by |
|---|---|---|---|
| `ID_MMGLHandguard` | — | — | MMGL |
| `ID_MP43Handguard` | — | — | MP43 |
| `ID_SKSHandguard` | — | — | SKS |
| `ID_SMG_01_HGD_01` | — | — | Vector |
| `ID_SR_04Handguard` | — | — | SR_04 |
| `ID_SVDMHandguard` | — | — | SVDM |

### Magazine (57)

| Attachment | Weapon-side modifiers | Character | Accepted by |
|---|---|---|---|
| STANAG 30 RND Magazine (`ID_556STANAG_Mag_Standard`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, EquipSpeedMultiplier ×c 0.98 | `GE_Stanag_30Rounds_CharacterEffects` | A91, KH2002, M249, M4, TAR21, WEPN_033 |
| AK74 75 RND Drum Magazine (`ID_AK74M_Mag_75rnd`) | **On the weapon:** AimTime ×c 1.26, VerticalRecoilMultiplier ×c 1.22, HorizontalRecoilMultiplier ×c 1.24, EquipSpeedMultiplier ×c 0.93 | `GE_AK74_Mag_Drum75rd_CharacterEffects` | AK74M |
| AK74 60 RND Magazine (`ID_AK74M_Mag_Extended`) | **On the weapon:** AimTime ×c 1.19, VerticalRecoilMultiplier ×c 1.19, HorizontalRecoilMultiplier ×c 1.21, EquipSpeedMultiplier ×c 0.93 | `GE_AK74_Mag_Ext60rd_CharacterEffects` | AK74M |
| AK74 30 RND Magazine (`ID_AK74M_Mag_Standard`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | `GE_AK74_Mag_30rd_CharacterEffects` | AK74M |
| AR Extended Mag (`ID_AR_Mag_Extended`) | — | — | A91, KH2002, M4, TAR21, WEPN_033 |
| Glock 17 Extended Mag (`ID_Glock17_Mag_Extended`) | — | — | Glock17, WEPN_032 |
| GGX 17 RND Magazine (`ID_Glock17_Mag_Standard`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | — | Glock17, WEPN_032 |
| Judge Bullet Cylinder (`ID_Judge_Mag_Internal`) | — | — | Judge |
| PKM 100 RND Box  (`ID_LMG_02_Magazine_Standard`) | **On the weapon:** AimTime ×c 1.1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | `GE_MAG_LMG_02_100rd_CharacterEffects` | LMG_02 |
| M500 Internal Mag (`ID_M12G_Mag_Internal`) | — | — | M500 |
| M249 200 RND Box (`ID_M249_Mag_Standard`) | **On the weapon:** AimTime ×c 1.2, VerticalRecoilMultiplier ×c 1.17, HorizontalRecoilMultiplier ×c 1.17, EquipSpeedMultiplier ×c 0.93 | `GE_MAG_M249_200rd_CharacterEffects` | M249 |
| M4 Standard Mag (`ID_M4_Mag_Standard`) | — | — | A91, KH2002, M4, TAR21, WEPN_033 |
| M1911 7 RND Magazine (`ID_MAGZ_002`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | — | WEPN_026 |
| Deagle 7 RND Magazine (`ID_MAGZ_003`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | — | WEPN_027 |
| MP5 30 RND Magazine (`ID_MAGZ_004`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | `GE_MAGZ_004_CharacterEffects` | WEPN_028 |
| Galil 35 RND Magazine (`ID_MAGZ_005`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | `GE_MAGZ_005_CharacterEffects` | WEPN_029 |
| FAL 20 RND Magazine (`ID_MAGZ_006`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | — | RFB, WEPN_030 |
| GGX 50 RND Drum Magazine (`ID_MAGZ_011`) | **On the weapon:** AimTime ×c 1.1, VerticalRecoilMultiplier ×c 1.04, HorizontalRecoilMultiplier ×c 1.07, EquipSpeedMultiplier ×c 0.95 | `GE_MAGZ_011_CharacterEffects` | Glock17, WEPN_032 |
| GGX 33 RND Magazine (`ID_MAGZ_012`) | **On the weapon:** AimTime ×c 1.06, VerticalRecoilMultiplier ×c 1.02, HorizontalRecoilMultiplier ×c 1.04, EquipSpeedMultiplier ×c 0.98 | `GE_MAGZ_012_CharacterEffects` | Glock17, WEPN_032 |
| FAL 30 RND Magazine (`ID_MAGZ_024`) | **On the weapon:** AimTime ×c 1.26, VerticalRecoilMultiplier ×c 1.22, HorizontalRecoilMultiplier ×c 1.24, EquipSpeedMultiplier ×c 0.93 | `GE_MAGZ_024_CharacterEffects` | RFB, WEPN_030 |
| AMR 50 10 RND Magazine (`ID_MAGZ_026`) | **On the weapon:** AimTime ×c 1.06, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, EquipSpeedMultiplier ×c 0.9 | `GE_MAGZ_026_CharacterEffects` | SR_04 |
| MK22 5 RND Magazine (`ID_MAGZ_034`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | `GE_MAGZ_034_CharacterEffects` | MK22 |
| PP-19 50 RND Vityaz Drum Magazine (`ID_MAGZ_046`) | **On the weapon:** AimTime ×c 1.2, VerticalRecoilMultiplier ×c 1.2, HorizontalRecoilMultiplier ×c 1.18, EquipSpeedMultiplier ×c 0.93 | `GE_MAGZ_046_CharacterEffects` | SMG_03 |
| PP-19 Bizon 53 RND Magazine (`ID_MAGZ_051`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, EquipSpeedMultiplier ×c 1 | `GE_MAGZ_051_CharacterEffects` | WEPN_031 |
| AMP-9 20 RND Magazine (`ID_MAGZ_052`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | `GE_MAGZ_052_CharacterEffects` | MP9 |
| Super-45 40 RND Drum Magazine (`ID_MAGZ_055`) | **On the weapon:** AimTime ×c 1.2, VerticalRecoilMultiplier ×c 1.2, HorizontalRecoilMultiplier ×c 1.18, EquipSpeedMultiplier ×c 0.93 | `GE_MAGZ_055_CharacterEffects` | Vector |
| MP5 50 RND Drum Magazine (`ID_MAGZ_056`) | **On the weapon:** AimTime ×c 1.2, VerticalRecoilMultiplier ×c 1.2, HorizontalRecoilMultiplier ×c 1.18, EquipSpeedMultiplier ×c 0.93 | `GE_MAGZ_056_CharacterEffects` | WEPN_028 |
| Super-45 13 RND Magazine (`ID_MAGZ_057`) | **On the weapon:** AimTime ×c 0.83, VerticalRecoilMultiplier ×c 0.83, HorizontalRecoilMultiplier ×c 0.83, EquipSpeedMultiplier ×c 1.21 | `GE_MAGZ_057_CharacterEffects` | Vector |
| PP-19 Vityaz 10 RND Magazine (`ID_MAGZ_059`) | **On the weapon:** AimTime ×c 0.86, VerticalRecoilMultiplier ×c 0.83, HorizontalRecoilMultiplier ×c 0.83, EquipSpeedMultiplier ×c 1.2 | `GE_MAGZ_059_CharacterEffects` | SMG_03 |
| Galil 50 RND Magazine (`ID_MAGZ_060`) | **On the weapon:** AimTime ×c 1.19, VerticalRecoilMultiplier ×c 1.19, HorizontalRecoilMultiplier ×c 1.21, EquipSpeedMultiplier ×c 0.93 | `GE_MAGZ_060_CharacterEffects` | WEPN_029 |
| AMP-9 15 RND Magazine (`ID_MAGZ_061`) | **On the weapon:** AimTime ×c 0.86, VerticalRecoilMultiplier ×c 0.83, HorizontalRecoilMultiplier ×c 0.83, EquipSpeedMultiplier ×c 1.2 | — | MP9 |
| M249 100 RND Fabric Magazine (`ID_MAGZ_062`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, EquipSpeedMultiplier ×c 1 | `GE_MAGZ_062_CharacterEffects` | M249 |
| M1911 10 RND Magazine (`ID_MAGZ_063`) | **On the weapon:** AimTime ×c 1.06, VerticalRecoilMultiplier ×c 1.02, HorizontalRecoilMultiplier ×c 1.04, EquipSpeedMultiplier ×c 0.98 | `GE_MAGZ_063_CharacterEffects` | WEPN_026 |
| MP5 20 RND Magazine (`ID_MAGZ_064`) | **On the weapon:** AimTime ×c 0.87, VerticalRecoilMultiplier ×c 0.87, HorizontalRecoilMultiplier ×c 0.88, EquipSpeedMultiplier ×c 1.1 | `GE_MAGZ_064_CharacterEffects` | WEPN_028 |
| SVD 5 RND Magazine (`ID_MAGZ_065`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | `GE_MAGZ_065` | SVDM |
| AMP-9 50 RND Drum Magazine (`ID_MAGZ_066`) | **On the weapon:** AimTime ×c 1.2, VerticalRecoilMultiplier ×c 1.2, HorizontalRecoilMultiplier ×c 1.18, EquipSpeedMultiplier ×c 0.93 | `GE_MAGZ_066` | MP9 |
| Evo-3 Ultra 50 RND Box (`ID_MAGZ_067`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, EquipSpeedMultiplier ×c 1 | `GE_MAGZ_067_CharacterEffects` | WEPN_036 |
| M14 10 RND Magazine (`ID_MAGZ_068`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, EquipSpeedMultiplier ×c 1 | `GE_MAGZ_068_CharacterEffects` | WEPN_034 |
| SIG Spear (WEPN_037) Standard Mag (`ID_MAGZ_069`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, EquipSpeedMultiplier ×c 1 | `GE_MAGZ_069_CharacterEffects` | WEPN_037 |
| M14 30 RND Magazine (`ID_MAGZ_070`) | **On the weapon:** AimTime ×c 1.2, VerticalRecoilMultiplier ×c 1.22, HorizontalRecoilMultiplier ×c 1.24, EquipSpeedMultiplier ×c 0.93 | `GE_MAGZ_070_CharacterEffects` | WEPN_034 |
| M14 20 RND Magazine (`ID_MAGZ_071`) | **On the weapon:** AimTime ×c 1.08, VerticalRecoilMultiplier ×c 1.07, HorizontalRecoilMultiplier ×c 1.05, EquipSpeedMultiplier ×c 0.95 | `GE_MAGZ_071_CharacterEffects` | WEPN_034 |
| MK22 Standard Mag (`ID_MK22_Mag_Standard`) | **On the weapon:** AimTime ×c 1.06, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, EquipSpeedMultiplier ×c 0.9 | `GE_MAG_MK22_10rd_CharacterEffects` | MK22 |
| MMGL Internal Mag (`ID_MMGL_Mag_Internal`) | — | — | MMGL |
| Mosin Standard Mag (`ID_Mosin_MagInternal`) | — | — | WEPN_017 |
| MP9 Extended Mag (`ID_MP9_Mag_Extended`) | — | — | MP9 |
| AMP-9 30 RND Magazine (`ID_MP9_Mag_Standard`) | **On the weapon:** AimTime ×c 1.11, VerticalRecoilMultiplier ×c 1.12, HorizontalRecoilMultiplier ×c 1.14, EquipSpeedMultiplier ×c 0.93 | `GE_MAGZ_043_CharacterEffects` | MP9 |
| FAL 10 RND Magazine (`ID_RFB_Mag_Standard`) | **On the weapon:** AimTime ×c 0.85, VerticalRecoilMultiplier ×c 0.84, HorizontalRecoilMultiplier ×c 0.85, EquipSpeedMultiplier ×c 1.24 | `GE_MAG_FAL_10rd_CharacterEffects` | RFB, WEPN_030 |
| SKS Extended Mag (`ID_SKS_Mag_Extended`) | — | — | SKS |
| SKS Internal Mag (`ID_SKS_Mag_Internal`) | — | — | SKS |
| PP-19 Vityaz 30 RND Magazine (`ID_SMG_03_Mag_Standard`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | `GE_MAG_SMG_03_CharacterEffects` | SMG_03 |
| AMR 50 5 RND Magazine (`ID_SR_04_Mag_Standard`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | — | SR_04 |
| STANAG 20 RND Magazine (`ID_STANAG_Mag_20rd`) | **On the weapon:** AimTime ×c 0.85, VerticalRecoilMultiplier ×c 0.84, HorizontalRecoilMultiplier ×c 0.85, EquipSpeedMultiplier ×c 1.16 | `GE_MAGZ_053_CharacterEffects` | A91, KH2002, M249, M4, TAR21, WEPN_033 |
| STANAG 60 RND Magazine (`ID_STANAG_Mag_Extended_60rd`) | **On the weapon:** AimTime ×c 1.19, VerticalRecoilMultiplier ×c 1.19, HorizontalRecoilMultiplier ×c 1.21, EquipSpeedMultiplier ×c 0.93 | `GE_MAGZ_054_CharacterEffects` | A91, KH2002, M249, M4, TAR21, WEPN_033 |
| SV98 Extended Mag (`ID_SV98_Mag_Extended`) | — | — | SV98 |
| SV98 10 RND Magazine (`ID_SV98_Mag_Standard`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | `GE_MAG_SV98_10rd_CharacterEffects` | SV98 |
| SVDM Standard Magazine (`ID_SVDM_Mag_Standard`) | **On the weapon:** AimTime ×c 1.06, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, EquipSpeedMultiplier ×c 0.9 | — | SVDM |
| Super-45 30 RND Magazine (`ID_Vector_Mag_Standard`) | **On the weapon:** AimTime ×c 1, VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1 | `GE_MAGZ_008_CharacterEffects` | Vector |

### Muzzle (56)

| Attachment | Weapon-side modifiers | Character | Accepted by |
|---|---|---|---|
| 3 Prong Flash Hider (`ID_MUZL_013`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 0.99, AimTime ×c 0.98 | — | M249, M4, TAR21, WEPN_029 |
| TopComp Brake (`ID_MUZL_014`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.82, HorizontalRecoilMultiplier ×c 0.98, SpreadMultiplier ×c 0.96, AimTime × 1.05 | — | M249, M4, TAR21, WEPN_029 |
| Dual Port Brake (`ID_MUZL_019`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.82, HorizontalRecoilMultiplier ×c 0.96, SpreadMultiplier ×c 0.95, AimTime ×c 1.05 | — | Glock17, MP9, SMG_03, WEPN_028, WEPN_031, WEPN_032 |
| Ballista Brake (`ID_MUZL_020`) | **On the weapon:** VerticalRecoilMultiplier ×c 1.02, HorizontalRecoilMultiplier ×c 0.8, SpreadMultiplier ×c 0.95, AimTime ×c 1.04 | — | AK74M, Glock17, M4, MP9, SMG_03, TAR21, WEPN_028, WEPN_029, WEPN_031, WEPN_032 |
| Constrictor Brake (`ID_MUZL_022`) | **On the weapon:** VerticalRecoilMultiplier ×c 1.01, HorizontalRecoilMultiplier ×c 0.83, SpreadMultiplier ×c 0.97, AimTime ×c 1.03 | — | LMG_02, MK22, RFB, SKS, SV98, WEPN_017, WEPN_030, WEPN_036, WEPN_037 |
| Tread Brake (`ID_MUZL_023`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.86, HorizontalRecoilMultiplier ×c 0.98, SpreadMultiplier ×c 0.97, AimTime ×c 1.03 | — | M249 |
| Hexagon Brake (`ID_MUZL_024`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.99, HorizontalRecoilMultiplier ×c 0.78, SpreadMultiplier ×c 0.96, AimTime ×c 1.05 | — | M4, TAR21, WEPN_029 |
| Slicktap Brake (`ID_MUZL_025`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.8, HorizontalRecoilMultiplier ×c 1.03, SpreadMultiplier ×c 0.96, AimTime ×c 1.08 | — | SKS |
| 3-Chamber Brake (`ID_MUZL_027`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.8, HorizontalRecoilMultiplier ×c 0.98, SpreadMultiplier ×c 0.96, AimTime ×c 1.06 | — | M249, M4, TAR21, WEPN_029 |
| DTK-1 Brake (`ID_MUZL_028`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.8, HorizontalRecoilMultiplier ×c 0.9, SpreadMultiplier ×c 0.95, AimTime ×c 1.06 | — | SKS |
| Orpheus Max Brake (`ID_MUZL_029`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.74, HorizontalRecoilMultiplier ×c 0.9, SpreadMultiplier ×c 0.98, AimTime ×c 1.07 | — | LMG_02, M249 |
| Three Port Brake (`ID_MUZL_030`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.78, HorizontalRecoilMultiplier ×c 0.96, SpreadMultiplier ×c 0.96, AimTime ×c 1.06 | — | MK22, RFB, WEPN_030, WEPN_036, WEPN_037 |
| M500 Sabre Brake (`ID_MUZL_031`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.8, HorizontalRecoilMultiplier ×c 1.02, SpreadMultiplier ×c 0.95, AimTime ×c 1.07 | — | M500 |
| RC-556 Suppressor (`ID_MUZL_032`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.88, HorizontalRecoilMultiplier ×c 0.92, SpreadMultiplier ×c 0.88, AimTime ×c 1.12 | — | M249, M4, TAR21, WEPN_029 |
| Eclipse Flash Hider (`ID_MUZL_037`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 0.99, AimTime ×c 0.98 | — | Glock17, MP9, SMG_03, WEPN_028, WEPN_031, WEPN_032 |
| Slotted Flash Hider (`ID_MUZL_038`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 0.99, AimTime ×c 0.98 | — | LMG_02 |
| Birdcage Flash Hider (`ID_MUZL_039`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 0.99, AimTime ×c 0.98 | — | AK74M |
| SVD 7.62x54R Brake (`ID_MUZL_040`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.82, HorizontalRecoilMultiplier ×c 0.98, SpreadMultiplier ×c 0.97, AimTime ×c 1.03 | — | SVDM |
| SRVV Brake (`ID_MUZL_041`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.88, HorizontalRecoilMultiplier ×c 0.82, SpreadMultiplier ×c 0.95, AimTime ×c 1.05 | — | LMG_02, SV98, SVDM, WEPN_017 |
| Deadeye Flash Hider (`ID_MUZL_042`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 1, AimTime ×c 1 | — | LMG_02, MK22, RFB, SKS, SV98, SVDM, WEPN_017, WEPN_030, WEPN_035, WEPN_036, WEPN_037 |
| Improved Cylinder Choke (`ID_MUZL_044`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 1, AimTime ×c 1.02 | — | M500 |
| Full Choke (`ID_MUZL_045`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 1, AimTime ×c 1.02 | — | M500 |
| Super-45 Flash Hider (`ID_MUZL_046`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 0.99, AimTime ×c 0.98 | — | Vector |
| Ghost LITE Muzzle Brake (`ID_MUZL_047`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.78, HorizontalRecoilMultiplier ×c 0.88, SpreadMultiplier ×c 0.98, AimTime ×c 1.04 | — | Vector |
| AMR 50 Cal Muzzle Brake (`ID_MUZL_048`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.8, HorizontalRecoilMultiplier ×c 0.92, SpreadMultiplier ×c 0.99, AimTime ×c 1.05 | — | SR_04 |
| .50 Cal Heavy Suppressor (`ID_MUZL_049`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.9, HorizontalRecoilMultiplier ×c 0.94, SpreadMultiplier ×c 0.9, AimTime ×c 1.12 | — | SR_04 |
| .45 ACP Pistol Compensator (`ID_MUZL_050`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.86, HorizontalRecoilMultiplier ×c 0.98, SpreadMultiplier ×c 0.98, AimTime ×c 1.03 | — | WEPN_026 |
| AMP-9 9x19 Suppressor (`ID_MUZL_051`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.94, HorizontalRecoilMultiplier ×c 0.95, SpreadMultiplier ×c 0.92, AimTime ×c 1.08 | — | MP9 |
| AMP-9 Tactical Flash Hider (`ID_MUZL_052`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 0.99, AimTime ×c 0.98 | — | MP9 |
| PP-19-01 Vityaz 9x19 Suppressor (`ID_MUZL_053`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.97, HorizontalRecoilMultiplier ×c 0.97, SpreadMultiplier ×c 0.95, AimTime ×c 1.1 | — | SMG_03 |
| PP-19 Vityaz Flash Hider (`ID_MUZL_054`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 0.99, AimTime ×c 0.98 | — | SMG_03 |
| BMR-308 Flash Hider (`ID_MUZL_055`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 0.99, AimTime ×c 0.98 | — | RFB |
| BMR-308 Suppressor (`ID_MUZL_056`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.95, HorizontalRecoilMultiplier ×c 0.96, SpreadMultiplier ×c 0.92, AimTime ×c 1.08 | — | RFB |
| Flow-Through .308 Suppressor (`ID_MUZL_057`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.96, HorizontalRecoilMultiplier ×c 0.97, SpreadMultiplier ×c 0.9, AimTime ×c 1.05 | — | MK22 |
| QD-5 Suppressor (`ID_MUZL_058`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.94, HorizontalRecoilMultiplier ×c 0.95, SpreadMultiplier ×c 0.9, AimTime ×c 1.08 | — | WEPN_028 |
| MP5 Flash Hider (`ID_MUZL_059`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 0.92, AimTime ×c 0.98 | — | WEPN_028 |
| Suppressor T8L1 Scout (`ID_MUZL_060`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.96, HorizontalRecoilMultiplier ×c 0.96, SpreadMultiplier ×c 0.93, AimTime ×c 1.07 | — | WEPN_030 |
| FAL Flash Hider (`ID_MUZL_061`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 0.97, AimTime ×c 0.98 | — | WEPN_030 |
| STRELIX Suppressor (`ID_MUZL_062`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.96, HorizontalRecoilMultiplier ×c 0.96, SpreadMultiplier ×c 0.93, AimTime ×c 1.04 | — | WEPN_035 |
| WEPN_033 (M14) standard muzzle (`ID_MUZL_064`) | — | — | WEPN_034 |
| QD-5 Suppressor (`ID_MUZL_065`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.94, HorizontalRecoilMultiplier ×c 0.95, SpreadMultiplier ×c 0.9, AimTime ×c 1.08 | — | WEPN_036 |
| Sig Default (`ID_MUZL_066`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.94, HorizontalRecoilMultiplier ×c 0.95, SpreadMultiplier ×c 0.9, AimTime ×c 1.08 | — | WEPN_037 |
| Cross Rifle Muzzle Brake (`ID_MUZL_067`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.92, HorizontalRecoilMultiplier ×c 0.94, SpreadMultiplier ×c 0.9, AimTime ×c 1.08 | — | WEPN_037 |
| Clutch Lok Muzzle Brake (`ID_MUZL_068`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.9, HorizontalRecoilMultiplier ×c 1.05, SpreadMultiplier ×c 0.9, AimTime ×c 1.02 | — | WEPN_037 |
| SRD762TI-QD (`ID_MUZL_069`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.93, HorizontalRecoilMultiplier ×c 0.94, SpreadMultiplier ×c 0.9, AimTime ×c 1.1 | — | WEPN_037 |
| SL7i-BL Suppressor (`ID_MUZL_070`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.95, HorizontalRecoilMultiplier ×c 0.94, SpreadMultiplier ×c 0.9, AimTime ×c 1.1 | — | WEPN_036 |
| .30 Cal SS Phosphate Muzzle Brake (`ID_MUZL_071`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.85, HorizontalRecoilMultiplier ×c 1.05, SpreadMultiplier ×c 0.88, AimTime ×c 1.05 | — | WEPN_034 |
| .30 Cal Steel Black Flash Hider  (`ID_MUZL_072`) | **On the weapon:** VerticalRecoilMultiplier ×c 1, HorizontalRecoilMultiplier ×c 1, SpreadMultiplier ×c 1, AimTime ×c 0.97 | — | WEPN_034 |
| GOL Multi-Caliber Suppressor (`ID_MZL_04`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.84, HorizontalRecoilMultiplier ×c 0.9, SpreadMultiplier ×c 0.88, AimTime ×c 1.15 | — | MK22, RFB, SKS, SR_04, SV98, SVDM, WEPN_017 |
| SG Multi-Caliber Suppressor (`ID_MZL_05`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.9, HorizontalRecoilMultiplier ×c 0.94, SpreadMultiplier ×c 0.91, AimTime ×c 1.08 | — | Glock17, MP9, SMG_03, Vector, WEPN_026, WEPN_028, WEPN_031, WEPN_032 |
| 12 Gauge Suppressor (`ID_MZL_06`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.88, HorizontalRecoilMultiplier ×c 0.95, SpreadMultiplier ×c 0.92, AimTime ×c 1.1 | — | M500 |
| AR Multi-Caliber Suppressor (`ID_MZL_07`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.88, HorizontalRecoilMultiplier ×c 0.93, SpreadMultiplier ×c 0.9, AimTime ×c 1.1 | — | M249, M4, TAR21, WEPN_029, WEPN_030 |
| Hexagon 762 Suppressor (`ID_MZL_08`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.82, HorizontalRecoilMultiplier ×c 0.9, SpreadMultiplier ×c 0.89, AimTime ×c 1.12 | — | LMG_02, SKS, SV98, SVDM, WEPN_017 |
| PBS-4 Suppressor (`ID_MZL_09`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.86, HorizontalRecoilMultiplier ×c 0.92, SpreadMultiplier ×c 0.88, AimTime ×c 1.12 | — | AK74M |
| TGP-A Suppressor 5.45 (`ID_MZL_10`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.9, HorizontalRecoilMultiplier ×c 0.94, SpreadMultiplier ×c 0.91, AimTime ×c 1.1 | — | AK74M |
| CQB 74 Brake (`ID_PWSCQB74`) | **On the weapon:** VerticalRecoilMultiplier ×c 0.8, HorizontalRecoilMultiplier ×c 0.97, SpreadMultiplier ×c 0.96, AimTime ×c 1.04 | — | AK74M |

### Sight (28)

| Attachment | Weapon-side modifiers | Character | Accepted by |
|---|---|---|---|
| 6-10x Scope MRAD (`ID_10xScope`) | **On the weapon:** AimTime × 1.15, AdsZoomMultiplier = 6, MaxZeroingRange = 1000, MinZeroingRange = 100<br>**Sight `S_Aim01`:** no effects | `GE_10xScope_CharacterEffects` | MK22, SKS, SR_04, SV98, SVDM, WEPN_034, WEPN_035 |
| 6-10x Scope MOA (`ID_10xScopeMoa`) | **On the weapon:** AimTime × 1.15, AdsZoomMultiplier = 6, MaxZeroingRange = 1000, MinZeroingRange = 100<br>**Sight `S_Aim01`:** no effects | `GE_10xScope_CharacterEffects` | MK22, SKS, SR_04, SV98, SVDM, WEPN_034, WEPN_035 |
| Spitfire 3X (`ID_3xScope`) | **On the weapon:** AdsZoomMultiplier = 3, MinZeroingRange = 100, MaxZeroingRange = 300, AimTime ×c 1.1<br>**Sight `S_Aim01`:** no effects | `GE_3xScope_CharacterEffects` | AK74M, LMG_02, M249, M4, M500, MK22, RFB, SKS, SR_04, SV98, SVDM, TAR21, WEPN_029, WEPN_030, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| 4x Elcan Spectr (`ID_4xElcanSpectr`) | **On the weapon:** MaxZeroingRange = 400, MinZeroingRange = 100<br>**Sight `S_Aim01`:** AimTime ×c 1.1, AdsZoomMultiplier = 4<br>**Sight `S_Aim02`:** AimTime ×c 1.05, AdsZoomMultiplier = 1.2 | `GE_4xElcanSpectr_CharacterEffects` | AK74M, LMG_02, M249, M4, M500, MK22, RFB, SKS, SR_04, SV98, SVDM, TAR21, WEPN_029, WEPN_030, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| 4x Hybrid (`ID_4xHybrid`) | **On the weapon:** AdsZoomMultiplier = 4, AimTime + 0.35<br>**Sight `S_Aim01`:** no effects | — | MK22, SKS, SR_04, SV98, SVDM, WEPN_034, WEPN_035 |
| 3-6x Scope (`ID_6xScope`) | **On the weapon:** AdsZoomMultiplier = 3, AimTime + 0.2, MaxZeroingRange = 500, MinZeroingRange = 100<br>**Sight `S_Aim01`:** AdsZoomMultiplier = 3 | — | MK22, RFB, SKS, SR_04, SV98, SVDM, WEPN_034, WEPN_035 |
| Holographic Sight (`ID_EotechHoloSight`) | **On the weapon:** AdsZoomMultiplier = 1.2, AimTime ×c 0.9, MinZeroingRange = 100, MaxZeroingRange = 100<br>**Sight `S_Aim01`:** no effects | — | AK74M, LMG_02, M249, M4, M500, MK22, MP9, RFB, SKS, SMG_03, SR_04, SV98, SVDM, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_031, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| 2.5x Combat Optic (`ID_OPT_08`) | **On the weapon:** AimTime ×c 1.05, AdsZoomMultiplier = 2.5, MinZeroingRange = 100, MaxZeroingRange = 300<br>**Sight `S_Aim01`:** no effects | — | AK74M, LMG_02, M249, M4, M500, MK22, MP9, RFB, SKS, SMG_03, SR_04, SV98, SVDM, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_031, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| Compact T-2 Red Dot (`ID_RedDot`) | **On the weapon:** AdsZoomMultiplier = 1.2, AimTime ×c 0.9, MaxZeroingRange = current MinZeroingRange<br>**Sight `S_Aim01`:** no effects | — | AK74M, LMG_02, M249, M4, M500, MK22, MP9, RFB, SKS, SMG_03, SR_04, SV98, SVDM, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_031, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| Kobra Reflex (`ID_SGHT_009`) | **On the weapon:** AdsZoomMultiplier = 1.2, AimTime ×c 0.85, MaxZeroingRange = current MinZeroingRange<br>**Sight `S_Aim01`:** no effects | — | AK74M, LMG_02, M249, M4, M500, MK22, MP9, RFB, SKS, SMG_03, SR_04, SV98, SVDM, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_031, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| 1x-6x LPVO Short Dot (`ID_SGHT_011`) | **On the weapon:** AdsZoomMultiplier = 3, AimTime ×c 1.12, MaxZeroingRange = 600, MinZeroingRange = 100<br>**Sight `S_Aim01`:** AdsZoomMultiplier = 3 | `GE_SGHT_011_CharacterEffects` | MK22, SKS, SR_04, SV98, SVDM, WEPN_034, WEPN_035 |
| Four Reticle Reflex (`ID_SGHT_016`) | **On the weapon:** AdsZoomMultiplier = 1.2, AimTime ×c 0.85, MaxZeroingRange = current MinZeroingRange<br>**Sight `S_Aim01`:** no effects | — | AK74M, LMG_02, M249, M4, M500, MK22, MP9, RFB, SKS, SMG_03, SR_04, SV98, SVDM, TAR21, Vector, WEPN_027, WEPN_028, WEPN_029, WEPN_030, WEPN_031, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| OKP 7 Reflex (`ID_SGHT_023`) | **On the weapon:** AdsZoomMultiplier = 1.2, AimTime ×c 0.85, MaxZeroingRange = current MinZeroingRange<br>**Sight `S_Aim01`:** no effects | — | AK74M, LMG_02, M4, M500, MK22, MP9, RFB, SKS, SMG_03, SR_04, SV98, SVDM, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_031, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| Mini Reflex Sight (`ID_SGHT_025`) | **On the weapon:** AdsZoomMultiplier = 1.2, AimTime ×c 1.02, MaxZeroingRange = current MinZeroingRange<br>**Sight `S_Aim01`:** no effects | — | WEPN_032 |
| Tricon 1.5x Compact Prism Scope (`ID_SGHT_026`) | **On the weapon:** AimTime ×c 0.97, AdsZoomMultiplier = 1.5, MinZeroingRange = 100, MaxZeroingRange = 200<br>**Sight `S_Aim01`:** no effects | — | AK74M, LMG_02, M249, M4, M500, MK22, MP9, RFB, SKS, SMG_03, SR_04, SV98, SVDM, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_031, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| Vektor Frenix-X Micro Reflex Sight (`ID_SGHT_027`) | **On the weapon:** AdsZoomMultiplier = 1.2, AimTime ×c 0.87, MaxZeroingRange = current MinZeroingRange<br>**Sight `S_Aim01`:** no effects | — | AK74M, LMG_02, M4, M500, MK22, MP9, RFB, SKS, SMG_03, SR_04, SV98, SVDM, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_031, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| CQ-2x Prism Combat Scope (`ID_SGHT_028`) | **On the weapon:** AimTime ×c 1.05, AdsZoomMultiplier = 2, MinZeroingRange = 100, MaxZeroingRange = 300<br>**Sight `S_Aim01`:** no effects | — | AK74M, LMG_02, M249, M4, M500, MK22, MP9, RFB, SKS, SMG_03, SR_04, SV98, SVDM, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_031, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| 3x Tactical Prism Scope (`ID_SGHT_029`) | **On the weapon:** AdsZoomMultiplier = 3, MinZeroingRange = 100, MaxZeroingRange = 300, AimTime ×c 1.1<br>**Sight `S_Aim01`:** no effects | `GE_SGHT_029_CharacterEffects` | AK74M, LMG_02, M249, M4, M500, MK22, RFB, SKS, SR_04, SV98, SVDM, TAR21, WEPN_029, WEPN_030, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| 4x Combat Prism Scope with Reflex (`ID_SGHT_030`) | **On the weapon:** MaxZeroingRange = 400, MinZeroingRange = 100<br>**Sight `S_Aim01`:** AimTime ×c 1.1, AdsZoomMultiplier = 4<br>**Sight `S_Aim02`:** AimTime ×c 1.05, AdsZoomMultiplier = 1.2 | `GE_SGHT_030_CharacterEffects` | AK74M, LMG_02, M249, M4, M500, MK22, RFB, SKS, SR_04, SV98, SVDM, TAR21, WEPN_029, WEPN_030, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| 6x Precision Rifle Scope (`ID_SGHT_031`) | **On the weapon:** AdsZoomMultiplier = 6, AimTime ×c 1.15, MaxZeroingRange = 600, MinZeroingRange = 100<br>**Sight `S_Aim01`:** AdsZoomMultiplier = 6 | `GE_SGHT_031_CharacterEffects` | MK22, SKS, SR_04, SV98, SVDM, WEPN_034, WEPN_035 |
| Frontier 2.5x-10x Precision Scope (`ID_SGHT_032`) | **On the weapon:** AimTime × 1.2, AdsZoomMultiplier = 2.5, MaxZeroingRange = 1000, MinZeroingRange = 100<br>**Sight `S_Aim01`:** no effects | `GE_SGHT_032_CharacterEffects` | MK22, SKS, SR_04, SV98, SVDM, WEPN_034, WEPN_035 |
| CGM4 Scope (`ID_SGHT_033`) | **On the weapon:** AdsZoomMultiplier = 1.2, AimTime ×c 1<br>**Sight `S_Aim01`:** no effects | — | AK74M, CGM4, LMG_02, M249, M4, M500, MK22, MP9, RFB, SKS, SMG_03, SR_04, SV98, SVDM, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_031, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| PGO-7 (`ID_SGHT_034`) | **On the weapon:** AdsZoomMultiplier = 2.8, AimTime ×c 1.15, MinZeroingRange = 10, MaxZeroingRange = 10<br>**Sight `S_Aim01`:** no effects | `GE_SGHT_034_CharacterEffects` | RPG7 |
| 6x Marksman Scope + Reflex (`ID_SGHT_036`) | **On the weapon:** AimTime × 1<br>**Sight `S_Aim01`:** AdsZoomMultiplier = 6, AimTime ×c 1.12, MaxZeroingRange = 600, MinZeroingRange = 100<br>**Sight `S_Aim02`:** AimTime ×c 1.05, AdsZoomMultiplier = 1.2 | `GE_SGHT_036_CharacterEffects` | MK22, SKS, SR_04, SV98, SVDM, WEPN_034, WEPN_035 |
| MMGL Sight (`ID_SGHT_037`) | **On the weapon:** AdsZoomMultiplier = 1.2, AimTime ×c 1<br>**Sight `S_Aim01`:** no effects | — | AK74M, LMG_02, M249, M4, M500, MK22, MMGL, MP9, RFB, SKS, SMG_03, SR_04, SV98, SVDM, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_031, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| Compact P-1 Red Dot (`ID_SGHT_038`) | **On the weapon:** AdsZoomMultiplier = 1.2, AimTime ×c 1, MaxZeroingRange = current MinZeroingRange<br>**Sight `S_Aim01`:** no effects | — | AK74M, LMG_02, M4, M500, MK22, MP9, RFB, SKS, SMG_03, SR_04, SV98, SVDM, TAR21, Vector, WEPN_028, WEPN_029, WEPN_030, WEPN_031, WEPN_034, WEPN_035, WEPN_036, WEPN_037 |
| Leatherwood ART II (`ID_SGHT_039`) | **On the weapon:** AdsZoomMultiplier = 3, AimTime ×c 1.15, MaxZeroingRange = 800, MinZeroingRange = 100<br>**Sight `S_Aim01`:** no effects | `GE_SGHT_039_CharacterEffects` | WEPN_034 |
| PU 91/30 Scope (`ID_SGHT_040`) | **On the weapon:** AdsZoomMultiplier = 3.5, AimTime ×c 1.15, MaxZeroingRange = 800, MinZeroingRange = 100<br>**Sight `S_Aim01`:** no effects | `GE_SGHT_040_CharacterEffects` | WEPN_017 |

### Stock (28)

| Attachment | Weapon-side modifiers | Character | Accepted by |
|---|---|---|---|
| AK74M Stock (`ID_AK74MStock`) | — | — | AK74M |
| `ID_AR_02_STK_04` | — | — | M4 |
| `ID_HNDG_053` | — | — | WEPN_034 |
| `ID_HNDG_054` | — | — | WEPN_037 |
| `ID_HNDG_055` | — | — | WEPN_031 |
| `ID_LMG_02Stock` | — | — | LMG_02 |
| `ID_M249Stock` | — | — | M249 |
| M4 Stock (`ID_M4Stock`) | — | — | M4 |
| `ID_M500Stock` | — | — | M500 |
| `ID_MK22Stock` | — | — | MK22 |
| `ID_MMGLStock` | — | — | MMGL |
| `ID_MosinStock` | — | — | WEPN_017 |
| `ID_MP43Stock` | — | — | MP43 |
| `ID_MP9Stock` | — | — | MP9 |
| `ID_Pistol_01_STK_01` | — | — | Glock17, WEPN_032 |
| `ID_SMG_03Stock` | — | — | SMG_03, WEPN_031 |
| `ID_SR_04Stock` | — | — | SR_04 |
| MP5 Stock (`ID_STOK_003`) | — | — | WEPN_028 |
| FAL Stock (`ID_STOK_005`) | — | — | WEPN_030 |
| Galil Stock (`ID_STOK_013`) | — | — | WEPN_029 |
| Scout Rifle Stock (`ID_STOK_057`) | — | — | WEPN_035 |
| Evoly stock (`ID_STOK_058`) | — | — | WEPN_036 |
| M14 Stock (`ID_STOK_059`) | — | — | WEPN_034 |
| Sig Spear Standard Stock (`ID_STOK_060`) | — | — | WEPN_037 |
| `ID_SV98Stock` | — | — | SV98 |
| `ID_SVDMStock` | — | — | SVDM |
| `ID_VectorStock` | — | — | Vector |
| `ID_ZenitStock` | — | — | AK74M |

## 4. Flagged cases

Results above that rest on something not traced or on an odd piece of data.

- **Several sights.** `ID_4xElcanSpectr` (S_Aim01, S_Aim02); `ID_SGHT_030` (S_Aim01, S_Aim02); `ID_SGHT_036` (S_Aim01, S_Aim02). §1 and §2 use `S_Aim01`, per Effects §7.1; §3 lists each.
- **No `S_Aim01` sight** (natively no first-entry fallback; the tool applies no sight effects): `ID_CantedIrons` (S_AimCanted1).
- **No weapon accepts these attachments** that carry effects: `ID_CantedIrons`.
- **Same effect on the weapon and the character:** `ID_MAGZ_065` lists `GE_MAGZ_065` in both `AppliedEffects` and `AppliedCharacterEffects`; `ID_MAGZ_066` lists `GE_MAGZ_066` in both `AppliedEffects` and `AppliedCharacterEffects`.
- **Attribute-backed** (7 effects, evaluated live, Effects §4.2): `GE_RedDot` on `ID_RedDot`; `GE_SGHT_009` on `ID_SGHT_009`; `GE_SGHT_016` on `ID_SGHT_016`; `GE_SGHT_023` on `ID_SGHT_023`; `GE_SGHT_025` on `ID_SGHT_025`; `GE_SGHT_027` on `ID_SGHT_027`; `GE_SGHT_038` on `ID_SGHT_038`. Each overrides `MaxZeroingRange` with the current `MinZeroingRange`; the tool uses the final `MinZeroingRange`. None is in a default loadout.
- **Repeated `DefaultAttributes` keys** on 9K333 Verba (`ID_Launcher_04`): 9 keys appear twice, with different values for `Length` 100 then 80. The map load keeps both pairs (`FMapProperty::SerializeItem` adds each entry without a lookup when the archetype's map is empty), and `OnRegister` (`0x6C692E0`) installs them in order with overwrite off (`0x522F8F0`), so the first value is used: `Length` 100.
- **Empty effect references** (skipped): `ID_MUZL_064`.
- **Stance map** of A-91 (`ID_A91`): Stand → `GE_Weapon_StanceRecoil_AR_Prone`, Crouch → `GE_Weapon_StanceRecoil_AR_Standing`, Prone → `GE_Weapon_StanceRecoil_AR_Standing` (taken as in data).
- **Stance map** of TCX-SPR (`ID_WEPN_037`): Prone → `GE_Weapon_StanceRecoil_AR_Standing` (taken as in data).
- FAL (`ID_WEPN_030`): Sight default `Id.Item.IRNS_002` (on `ID_WEPN_030`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.
- M4 (`ID_M4`): Sight default `Id.Item.IRNS_006` (on `ID_M4`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.
- BMR-308 (`ID_RFB`): Sight default `Id.Item.ARMIrons` (on `ID_RFB`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.
- SKS (`ID_SKS`): Grip default `Id.Item.SKSPistolGrip` (on `ID_SKS`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.
- M249 SAW (`ID_M249`): Grip default `Id.Item.RK3PistolGrip` (on `ID_M249`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.
- AMR 50 (`ID_SR_04`): Sight default `Id.Item.ARMIrons` (on `ID_SR_04`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.
- MK22 (`ID_MK22`): Sight default `Id.Item.ARMIrons` (on `ID_MK22`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.
- Scout Rifle TD (`ID_WEPN_035`): Sight default `Id.Item.IRNS_008` (on `ID_WEPN_035`) has no item definition in data/ or in the game's paks (WdExtract `findname`), so the slot stays empty and adds no effects.
<!-- END weapon_attributes -->

## 5. Not traced

- The order of the sub-slot update messages across the weapon and its attachments (no value depends on
  it, see Override order above).
- Which caller grants the default loadout at spawn, and whether a saved preset replaces the defaults
  (`0x6784010` adds them only when the create-defaults flag is set; `0x6BD5860` sets it).
- Attachment `AppliedEffects` that never reach a weapon value because no weapon accepts the attachment.

## Change log

| Date | Change |
|---|---|
| 2026-10-17 | v1: generated per-weapon base and final values with the default loadout, per-attachment weapon-side modifiers and accepting weapons, from the §7.1 rules; `_tools/weapon_attributes.py` added. |
| 2026-10-17 | Round-5 verifier pass: the initial sight is `S_Aim01` (Effects §7.1), with a fallback to the first entry for `ID_CantedIrons`; `--mounted` models a mounted bipod (`MountedAppliedEffects` on the weapon, `MountedAppliedCharacterEffects` on the character, unfolded lists removed), and §3 lists the mounted lists. No §1 value changed. |
| 2026-10-18 | Round-6 verifier corrections: a repeated `DefaultAttributes` key keeps its first value (`OnRegister` installs with overwrite off), so the 9K333 Verba `Length` is 100, not 80 (the only §1 change); no native first-entry sight fallback, so the tool applies no sight effects for `ID_CantedIrons`; Override order, default loadout (`0x6784010`, `DefaultItems` only when `DefaultContainerItems` is empty) and sub-slot filters (`0x67A2B40`) are now traced and labelled Data / Native; stance effect and equip path wording; attribute-backed magnitudes are evaluated live (Effects §4.2); missing default items are absent from the paks too; the tool detects the bipod struct by `MountedAppliedEffects` and drops a missing-default flag when `--with` replaces that slot. |
| 2026-10-18 | Round-7 correction: 16 magazine ammo slots also differ between the two default lists (no attribute change). |
| 2026-10-18 | Interactive loadout calculator page added (`loadout-calculator.md`): choose a weapon, attachments, sight, stance and bipod state and see base, modifiers and final for every `Attribute.Gameplay.Weapon.*` value. It runs `assets/js/loadout-eval.js`, a port of this tool's evaluation over `assets/data/weapon-loadouts.json` (`--json`); `--check` compares the two on every default loadout and 400 seeded random loadouts. No §1 value changed. |
