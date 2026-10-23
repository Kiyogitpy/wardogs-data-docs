---
title: "Gameplay Effect Values"
parent: "Damage & Combat Systems"
description: "What all 341 effects do: every attachment, stance and movement modifier"
---

# Wardogs — Gameplay Effect Values

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

What every `GE_*` gameplay effect does: 341 effects, 1069 modifiers (962 fixed values, 82 set by the caller, 25 backed by another attribute). How effects and attributes work is in the [Gameplay Effects Pipeline](Wardogs_GameplayEffectsPipeline_v1.md).

**Source.** A static export of each effect's cooked class default object from the game's paks ([`tools/cue4parse_extractor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/tools/cue4parse_extractor/README.md): CUE4Parse with the 5.7.4 usmap; three usmap array types were corrected so the modifiers and tag queries decode). The data is in [`assets/data/ge-values.json`](assets/data/ge-values.json); this page is generated from it by [`_tools/ge_values.py`](_tools/ge_values.py).

**Reading the tables.** Attribute names drop `Attribute.Gameplay.`. Operations: `+` Add, `×` Multiply, `÷` Divide, `×c` MultiplyCompound, `+f` AddFinal, `=` Override. `@StackCount` and the like name the curve indexing ([pipeline §4.2](Wardogs_GameplayEffectsPipeline_v1.md#42-modifiers)). Cooked objects only store values that differ from the native default, so a blank duration or stack count means the native default, which is not in the paks. The tables give each modifier, not a combined result; how the operations combine into an attribute's current value is in [pipeline §4.4](Wardogs_GameplayEffectsPipeline_v1.md#44-current-value).

Three effects ship in the paks but not in the SDK headers: `GE_GrantSkill_Lockpicking`, `GE_Meta_ResourceChange` and `GE_MolotovBurning`.

## GE_MAGZ (60)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_MAGZ_002` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_003` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_004` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_004_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_005` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_005_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_006` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_008` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_008_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_011` | Weapon.AimTime ×c 1.1<br>Weapon.VerticalRecoilMultiplier ×c 1.04<br>Weapon.HorizontalRecoilMultiplier ×c 1.07<br>Weapon.EquipSpeedMultiplier ×c 0.95 |  |  |  |  |
| `GE_MAGZ_011_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.25 |  |  |  |  |
| `GE_MAGZ_012` | Weapon.AimTime ×c 1.06<br>Weapon.VerticalRecoilMultiplier ×c 1.02<br>Weapon.HorizontalRecoilMultiplier ×c 1.04<br>Weapon.EquipSpeedMultiplier ×c 0.98 |  |  |  |  |
| `GE_MAGZ_012_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.12 |  |  |  |  |
| `GE_MAGZ_024` | Weapon.AimTime ×c 1.26<br>Weapon.VerticalRecoilMultiplier ×c 1.22<br>Weapon.HorizontalRecoilMultiplier ×c 1.24<br>Weapon.EquipSpeedMultiplier ×c 0.93 |  |  |  |  |
| `GE_MAGZ_024_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.24 |  |  |  |  |
| `GE_MAGZ_026` | Weapon.AimTime ×c 1.06<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.EquipSpeedMultiplier ×c 0.9 |  |  |  |  |
| `GE_MAGZ_026_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_034` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_034_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_043` | Weapon.AimTime ×c 1.11<br>Weapon.VerticalRecoilMultiplier ×c 1.12<br>Weapon.HorizontalRecoilMultiplier ×c 1.14<br>Weapon.EquipSpeedMultiplier ×c 0.93 |  |  |  |  |
| `GE_MAGZ_043_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.23 |  |  |  |  |
| `GE_MAGZ_046` | Weapon.AimTime ×c 1.2<br>Weapon.VerticalRecoilMultiplier ×c 1.2<br>Weapon.HorizontalRecoilMultiplier ×c 1.18<br>Weapon.EquipSpeedMultiplier ×c 0.93 |  |  |  |  |
| `GE_MAGZ_046_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.25 |  |  |  |  |
| `GE_MAGZ_051` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.EquipSpeedMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_051_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_052` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_052_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_053` | Weapon.AimTime ×c 0.85<br>Weapon.VerticalRecoilMultiplier ×c 0.84<br>Weapon.HorizontalRecoilMultiplier ×c 0.85<br>Weapon.EquipSpeedMultiplier ×c 1.16 |  |  |  |  |
| `GE_MAGZ_053_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 0.78 |  |  |  |  |
| `GE_MAGZ_054` | Weapon.AimTime ×c 1.19<br>Weapon.VerticalRecoilMultiplier ×c 1.19<br>Weapon.HorizontalRecoilMultiplier ×c 1.21<br>Weapon.EquipSpeedMultiplier ×c 0.93 |  |  |  |  |
| `GE_MAGZ_054_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.21 |  |  |  |  |
| `GE_MAGZ_055` | Weapon.AimTime ×c 1.2<br>Weapon.VerticalRecoilMultiplier ×c 1.2<br>Weapon.HorizontalRecoilMultiplier ×c 1.18<br>Weapon.EquipSpeedMultiplier ×c 0.93 |  |  |  |  |
| `GE_MAGZ_055_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.25 |  |  |  |  |
| `GE_MAGZ_056` | Weapon.AimTime ×c 1.2<br>Weapon.VerticalRecoilMultiplier ×c 1.2<br>Weapon.HorizontalRecoilMultiplier ×c 1.18<br>Weapon.EquipSpeedMultiplier ×c 0.93 |  |  |  |  |
| `GE_MAGZ_056_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.25 |  |  |  |  |
| `GE_MAGZ_057` | Weapon.AimTime ×c 0.83<br>Weapon.VerticalRecoilMultiplier ×c 0.83<br>Weapon.HorizontalRecoilMultiplier ×c 0.83<br>Weapon.EquipSpeedMultiplier ×c 1.21 |  |  |  |  |
| `GE_MAGZ_057_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 0.77 |  |  |  |  |
| `GE_MAGZ_059` | Weapon.AimTime ×c 0.86<br>Weapon.VerticalRecoilMultiplier ×c 0.83<br>Weapon.HorizontalRecoilMultiplier ×c 0.83<br>Weapon.EquipSpeedMultiplier ×c 1.2 |  |  |  |  |
| `GE_MAGZ_059_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 0.78 |  |  |  |  |
| `GE_MAGZ_060` | Weapon.AimTime ×c 1.19<br>Weapon.VerticalRecoilMultiplier ×c 1.19<br>Weapon.HorizontalRecoilMultiplier ×c 1.21<br>Weapon.EquipSpeedMultiplier ×c 0.93 |  |  |  |  |
| `GE_MAGZ_060_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.21 |  |  |  |  |
| `GE_MAGZ_061` | Weapon.AimTime ×c 0.86<br>Weapon.VerticalRecoilMultiplier ×c 0.83<br>Weapon.HorizontalRecoilMultiplier ×c 0.83<br>Weapon.EquipSpeedMultiplier ×c 1.2 |  |  |  |  |
| `GE_MAGZ_062` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.EquipSpeedMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_062_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_063` | Weapon.AimTime ×c 1.06<br>Weapon.VerticalRecoilMultiplier ×c 1.02<br>Weapon.HorizontalRecoilMultiplier ×c 1.04<br>Weapon.EquipSpeedMultiplier ×c 0.98 |  |  |  |  |
| `GE_MAGZ_063_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.12 |  |  |  |  |
| `GE_MAGZ_064` | Weapon.AimTime ×c 0.87<br>Weapon.VerticalRecoilMultiplier ×c 0.87<br>Weapon.HorizontalRecoilMultiplier ×c 0.88<br>Weapon.EquipSpeedMultiplier ×c 1.1 |  |  |  |  |
| `GE_MAGZ_064_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 0.81 |  |  |  |  |
| `GE_MAGZ_065` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_066` | Weapon.AimTime ×c 1.2<br>Weapon.VerticalRecoilMultiplier ×c 1.2<br>Weapon.HorizontalRecoilMultiplier ×c 1.18<br>Weapon.EquipSpeedMultiplier ×c 0.93 |  |  |  |  |
| `GE_MAGZ_067` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.EquipSpeedMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_067_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_068` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.EquipSpeedMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_068_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_069` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.EquipSpeedMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_069_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAGZ_070` | Weapon.AimTime ×c 1.2<br>Weapon.VerticalRecoilMultiplier ×c 1.22<br>Weapon.HorizontalRecoilMultiplier ×c 1.24<br>Weapon.EquipSpeedMultiplier ×c 0.93 |  |  |  |  |
| `GE_MAGZ_070_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.24 |  |  |  |  |
| `GE_MAGZ_071` | Weapon.AimTime ×c 1.08<br>Weapon.VerticalRecoilMultiplier ×c 1.07<br>Weapon.HorizontalRecoilMultiplier ×c 1.05<br>Weapon.EquipSpeedMultiplier ×c 0.95 |  |  |  |  |
| `GE_MAGZ_071_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.08 |  |  |  |  |

## GE_FGRP (54)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_FGRP_006` | Weapon.VerticalRecoilMultiplier ×c 0.75<br>Weapon.HorizontalRecoilMultiplier ×c 0.87<br>Weapon.SpreadMultiplier ×c 0.81<br>Weapon.AimTime ×c 0.9<br>Weapon.EquipSpeedMultiplier ×c 1.07 |  |  |  |  |
| `GE_FGRP_006_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.93<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.95<br>Character.AimSwayVerticalMovementMultiplier ×c 0.78<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.85<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.75 |  |  |  |  |
| `GE_FGRP_007` | Weapon.VerticalRecoilMultiplier ×c 0.92<br>Weapon.HorizontalRecoilMultiplier ×c 0.71<br>Weapon.SpreadMultiplier ×c 0.76<br>Weapon.AimTime ×c 0.87<br>Weapon.EquipSpeedMultiplier ×c 1.15 |  |  |  |  |
| `GE_FGRP_007_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1<br>Character.AimSwaySpeedMultiplier ×c 0.88<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.92<br>Character.AimSwayVerticalMovementMultiplier ×c 0.88<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.86<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.78 |  |  |  |  |
| `GE_FGRP_008_BipodState` | Weapon.VerticalRecoilMultiplier ×c 0.2<br>Weapon.HorizontalRecoilMultiplier ×c 0.22<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 0.88 |  |  |  |  |
| `GE_FGRP_008_BipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.4<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.28<br>Character.AimSwayVerticalMovementMultiplier ×c 0.3<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.65<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.5 |  |  |  |  |
| `GE_FGRP_008_NonBipodState` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 1 |  |  |  |  |
| `GE_FGRP_008_UnfoldedBipodState` | Weapon.VerticalRecoilMultiplier ×c 1.15<br>Weapon.HorizontalRecoilMultiplier ×c 1.15<br>Weapon.SpreadMultiplier ×c 1.15<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_FGRP_008_UnfoldedBipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 1.05<br>Character.AimSwayHorizontalMovementMultiplier ×c 1.05<br>Character.AimSwayVerticalMovementMultiplier ×c 1.1<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.08<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.08 |  |  |  |  |
| `GE_FGRP_009_BipodState` | Weapon.VerticalRecoilMultiplier ×c 0.45<br>Weapon.HorizontalRecoilMultiplier ×c 0.35<br>Weapon.SpreadMultiplier ×c 0.45<br>Weapon.AimTime ×c 0.84 |  |  |  |  |
| `GE_FGRP_009_BipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.4<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.35<br>Character.AimSwayVerticalMovementMultiplier ×c 0.36<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.6<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.4 |  |  |  |  |
| `GE_FGRP_009_NonBipodState` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 1 |  |  |  |  |
| `GE_FGRP_009_UnfoldedBipodState` | Weapon.VerticalRecoilMultiplier ×c 1.15<br>Weapon.HorizontalRecoilMultiplier ×c 1.15<br>Weapon.SpreadMultiplier ×c 1.15<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_FGRP_009_UnfoldedBipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 1.05<br>Character.AimSwayHorizontalMovementMultiplier ×c 1.05<br>Character.AimSwayVerticalMovementMultiplier ×c 1.1<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.08<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.08 |  |  |  |  |
| `GE_FGRP_010_BipodState` | Weapon.VerticalRecoilMultiplier ×c 0.65<br>Weapon.HorizontalRecoilMultiplier ×c 0.4<br>Weapon.SpreadMultiplier ×c 0.45<br>Weapon.AimTime ×c 0.86 |  |  |  |  |
| `GE_FGRP_010_BipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.4<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.28<br>Character.AimSwayVerticalMovementMultiplier ×c 0.3<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.65<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.5 |  |  |  |  |
| `GE_FGRP_010_NonBipodState` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 1 |  |  |  |  |
| `GE_FGRP_010_UnfoldedBipodState` | Weapon.VerticalRecoilMultiplier ×c 1.15<br>Weapon.HorizontalRecoilMultiplier ×c 1.15<br>Weapon.SpreadMultiplier ×c 1.15<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_FGRP_010_UnfoldedBipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 1.05<br>Character.AimSwayHorizontalMovementMultiplier ×c 1.05<br>Character.AimSwayVerticalMovementMultiplier ×c 1.1<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.08<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.08 |  |  |  |  |
| `GE_FGRP_011_BipodState` | Weapon.VerticalRecoilMultiplier ×c 0.65<br>Weapon.HorizontalRecoilMultiplier ×c 0.35<br>Weapon.SpreadMultiplier ×c 0.45<br>Weapon.AimTime ×c 0.86 |  |  |  |  |
| `GE_FGRP_011_BipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.4<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.28<br>Character.AimSwayVerticalMovementMultiplier ×c 0.3<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.6<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.45 |  |  |  |  |
| `GE_FGRP_011_NonBipodState` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 1 |  |  |  |  |
| `GE_FGRP_011_UnfoldedBipodState` | Weapon.VerticalRecoilMultiplier ×c 1.15<br>Weapon.HorizontalRecoilMultiplier ×c 1.15<br>Weapon.SpreadMultiplier ×c 1.15<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_FGRP_011_UnfoldedBipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 1.05<br>Character.AimSwayHorizontalMovementMultiplier ×c 1.05<br>Character.AimSwayVerticalMovementMultiplier ×c 1.1<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.08<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.08 |  |  |  |  |
| `GE_FGRP_012_BipodState` | Weapon.VerticalRecoilMultiplier ×c 0.2<br>Weapon.HorizontalRecoilMultiplier ×c 0.25<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 0.88 |  |  |  |  |
| `GE_FGRP_012_BipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.4<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.28<br>Character.AimSwayVerticalMovementMultiplier ×c 0.3<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.6<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.45 |  |  |  |  |
| `GE_FGRP_012_NonBipodState` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 1 |  |  |  |  |
| `GE_FGRP_012_UnfoldedBipodState` | Weapon.VerticalRecoilMultiplier ×c 1.15<br>Weapon.HorizontalRecoilMultiplier ×c 1.15<br>Weapon.SpreadMultiplier ×c 1.15<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_FGRP_012_UnfoldedBipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 1.05<br>Character.AimSwayHorizontalMovementMultiplier ×c 1.05<br>Character.AimSwayVerticalMovementMultiplier ×c 1.1<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.08<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.08 |  |  |  |  |
| `GE_FGRP_013_BipodState` | Weapon.VerticalRecoilMultiplier ×c 0.65<br>Weapon.HorizontalRecoilMultiplier ×c 0.5<br>Weapon.SpreadMultiplier ×c 0.45<br>Weapon.AimTime ×c 0.83 |  |  |  |  |
| `GE_FGRP_013_BipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.4<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.28<br>Character.AimSwayVerticalMovementMultiplier ×c 0.3<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.55<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.4 |  |  |  |  |
| `GE_FGRP_013_NonBipodState` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 1 |  |  |  |  |
| `GE_FGRP_013_UnfoldedBipodState` | Weapon.VerticalRecoilMultiplier ×c 1.15<br>Weapon.HorizontalRecoilMultiplier ×c 1.15<br>Weapon.SpreadMultiplier ×c 1.15<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_FGRP_013_UnfoldedBipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 1.05<br>Character.AimSwayHorizontalMovementMultiplier ×c 1.05<br>Character.AimSwayVerticalMovementMultiplier ×c 1.1<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.08<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.08 |  |  |  |  |
| `GE_FGRP_014` | Weapon.VerticalRecoilMultiplier ×c 0.7<br>Weapon.HorizontalRecoilMultiplier ×c 0.97<br>Weapon.SpreadMultiplier ×c 0.91<br>Weapon.AimTime ×c 1.15<br>Weapon.EquipSpeedMultiplier ×c 1.09 |  |  |  |  |
| `GE_FGRP_014_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.95<br>Character.AimSwayHorizontalMovementMultiplier ×c 1.05<br>Character.AimSwayVerticalMovementMultiplier ×c 0.73<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.92<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.85 |  |  |  |  |
| `GE_FGRP_015` | Weapon.VerticalRecoilMultiplier ×c 0.82<br>Weapon.HorizontalRecoilMultiplier ×c 0.93<br>Weapon.SpreadMultiplier ×c 0.84<br>Weapon.AimTime ×c 1.02<br>Weapon.EquipSpeedMultiplier ×c 0.98 |  |  |  |  |
| `GE_FGRP_015_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.92<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.92<br>Character.AimSwayVerticalMovementMultiplier ×c 0.7<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.8<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.72 |  |  |  |  |
| `GE_FGRP_016` | Weapon.VerticalRecoilMultiplier ×c 1.05<br>Weapon.HorizontalRecoilMultiplier ×c 0.82<br>Weapon.SpreadMultiplier ×c 0.82<br>Weapon.AimTime ×c 0.83<br>Weapon.EquipSpeedMultiplier ×c 1.13 |  |  |  |  |
| `GE_FGRP_016_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.92<br>Character.AimSwayHorizontalMovementMultiplier ×c 1<br>Character.AimSwayVerticalMovementMultiplier ×c 0.96<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.92<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.84 |  |  |  |  |
| `GE_FGRP_017` | Weapon.VerticalRecoilMultiplier ×c 1.02<br>Weapon.HorizontalRecoilMultiplier ×c 0.84<br>Weapon.SpreadMultiplier ×c 0.84<br>Weapon.AimTime ×c 0.88<br>Weapon.EquipSpeedMultiplier ×c 1.09 |  |  |  |  |
| `GE_FGRP_017_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.92<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.98<br>Character.AimSwayVerticalMovementMultiplier ×c 0.9<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.9<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.82 |  |  |  |  |
| `GE_FGRP_018` | Weapon.VerticalRecoilMultiplier ×c 0.95<br>Weapon.HorizontalRecoilMultiplier ×c 0.77<br>Weapon.SpreadMultiplier ×c 0.8<br>Weapon.AimTime ×c 0.86<br>Weapon.EquipSpeedMultiplier ×c 1.1 |  |  |  |  |
| `GE_FGRP_018_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.92<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.96<br>Character.AimSwayVerticalMovementMultiplier ×c 0.92<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.9<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.82 |  |  |  |  |
| `GE_FGRP_019_BipodState` | Weapon.VerticalRecoilMultiplier ×c 0.4<br>Weapon.HorizontalRecoilMultiplier ×c 0.3<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 0.88 |  |  |  |  |
| `GE_FGRP_019_BipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.4<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.28<br>Character.AimSwayVerticalMovementMultiplier ×c 0.3<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.65<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.5 |  |  |  |  |
| `GE_FGRP_019_NonBipodState` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 1 |  |  |  |  |
| `GE_FGRP_019_UnfoldedBipodState` | Weapon.VerticalRecoilMultiplier ×c 1.15<br>Weapon.HorizontalRecoilMultiplier ×c 1.15<br>Weapon.SpreadMultiplier ×c 1.15<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_FGRP_019_UnfoldedBipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 1.05<br>Character.AimSwayHorizontalMovementMultiplier ×c 1.05<br>Character.AimSwayVerticalMovementMultiplier ×c 1.1<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.08<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.08 |  |  |  |  |
| `GE_FGRP_020_BipodState` | Weapon.VerticalRecoilMultiplier ×c 0.6<br>Weapon.HorizontalRecoilMultiplier ×c 0.35<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 0.88 |  |  |  |  |
| `GE_FGRP_020_BipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.4<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.28<br>Character.AimSwayVerticalMovementMultiplier ×c 0.3<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.65<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.5 |  |  |  |  |
| `GE_FGRP_020_NonBipodState` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 1 |  |  |  |  |
| `GE_FGRP_020_UnfoldedBipodState` | Weapon.VerticalRecoilMultiplier ×c 1.15<br>Weapon.HorizontalRecoilMultiplier ×c 1.15<br>Weapon.SpreadMultiplier ×c 1.15<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_FGRP_020_UnfoldedBipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 1.05<br>Character.AimSwayHorizontalMovementMultiplier ×c 1.05<br>Character.AimSwayVerticalMovementMultiplier ×c 1.1<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.08<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.08 |  |  |  |  |

## GE_MUZL (47)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_MUZL_013` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 0.99<br>Weapon.AimTime ×c 0.98 |  |  |  |  |
| `GE_MUZL_014` | Weapon.VerticalRecoilMultiplier ×c 0.82<br>Weapon.HorizontalRecoilMultiplier ×c 0.98<br>Weapon.SpreadMultiplier ×c 0.96<br>Weapon.AimTime × 1.05 |  |  |  |  |
| `GE_MUZL_019` | Weapon.VerticalRecoilMultiplier ×c 0.82<br>Weapon.HorizontalRecoilMultiplier ×c 0.96<br>Weapon.SpreadMultiplier ×c 0.95<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_MUZL_020` | Weapon.VerticalRecoilMultiplier ×c 1.02<br>Weapon.HorizontalRecoilMultiplier ×c 0.8<br>Weapon.SpreadMultiplier ×c 0.95<br>Weapon.AimTime ×c 1.04 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_022` | Weapon.VerticalRecoilMultiplier ×c 1.01<br>Weapon.HorizontalRecoilMultiplier ×c 0.83<br>Weapon.SpreadMultiplier ×c 0.97<br>Weapon.AimTime ×c 1.03 |  |  |  |  |
| `GE_MUZL_023` | Weapon.VerticalRecoilMultiplier ×c 0.86<br>Weapon.HorizontalRecoilMultiplier ×c 0.98<br>Weapon.SpreadMultiplier ×c 0.97<br>Weapon.AimTime ×c 1.03 |  |  |  |  |
| `GE_MUZL_024` | Weapon.VerticalRecoilMultiplier ×c 0.99<br>Weapon.HorizontalRecoilMultiplier ×c 0.78<br>Weapon.SpreadMultiplier ×c 0.96<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_MUZL_025` | Weapon.VerticalRecoilMultiplier ×c 0.8<br>Weapon.HorizontalRecoilMultiplier ×c 1.03<br>Weapon.SpreadMultiplier ×c 0.96<br>Weapon.AimTime ×c 1.08 |  |  |  |  |
| `GE_MUZL_027` | Weapon.VerticalRecoilMultiplier ×c 0.8<br>Weapon.HorizontalRecoilMultiplier ×c 0.98<br>Weapon.SpreadMultiplier ×c 0.96<br>Weapon.AimTime ×c 1.06 |  |  |  |  |
| `GE_MUZL_028` | Weapon.VerticalRecoilMultiplier ×c 0.8<br>Weapon.HorizontalRecoilMultiplier ×c 0.9<br>Weapon.SpreadMultiplier ×c 0.95<br>Weapon.AimTime ×c 1.06 |  |  |  |  |
| `GE_MUZL_029` | Weapon.VerticalRecoilMultiplier ×c 0.74<br>Weapon.HorizontalRecoilMultiplier ×c 0.9<br>Weapon.SpreadMultiplier ×c 0.98<br>Weapon.AimTime ×c 1.07 |  |  |  |  |
| `GE_MUZL_030` | Weapon.VerticalRecoilMultiplier ×c 0.78<br>Weapon.HorizontalRecoilMultiplier ×c 0.96<br>Weapon.SpreadMultiplier ×c 0.96<br>Weapon.AimTime ×c 1.06 |  |  |  |  |
| `GE_MUZL_031` | Weapon.VerticalRecoilMultiplier ×c 0.8<br>Weapon.HorizontalRecoilMultiplier ×c 1.02<br>Weapon.SpreadMultiplier ×c 0.95<br>Weapon.AimTime ×c 1.07 |  |  |  |  |
| `GE_MUZL_032` | Weapon.VerticalRecoilMultiplier ×c 0.88<br>Weapon.HorizontalRecoilMultiplier ×c 0.92<br>Weapon.SpreadMultiplier ×c 0.88<br>Weapon.AimTime ×c 1.12 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_037` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 0.99<br>Weapon.AimTime ×c 0.98 |  |  |  |  |
| `GE_MUZL_038` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 0.99<br>Weapon.AimTime ×c 0.98 |  |  |  |  |
| `GE_MUZL_039` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 0.99<br>Weapon.AimTime ×c 0.98 |  |  |  |  |
| `GE_MUZL_040` | Weapon.VerticalRecoilMultiplier ×c 0.82<br>Weapon.HorizontalRecoilMultiplier ×c 0.98<br>Weapon.SpreadMultiplier ×c 0.97<br>Weapon.AimTime ×c 1.03 |  |  |  |  |
| `GE_MUZL_041` | Weapon.VerticalRecoilMultiplier ×c 0.88<br>Weapon.HorizontalRecoilMultiplier ×c 0.82<br>Weapon.SpreadMultiplier ×c 0.95<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_MUZL_042` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 1 |  |  |  |  |
| `GE_MUZL_044` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 1.02 |  |  |  |  |
| `GE_MUZL_045` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 1.02 |  |  |  |  |
| `GE_MUZL_046` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 0.99<br>Weapon.AimTime ×c 0.98 |  |  |  |  |
| `GE_MUZL_047` | Weapon.VerticalRecoilMultiplier ×c 0.78<br>Weapon.HorizontalRecoilMultiplier ×c 0.88<br>Weapon.SpreadMultiplier ×c 0.98<br>Weapon.AimTime ×c 1.04 |  |  |  |  |
| `GE_MUZL_048` | Weapon.VerticalRecoilMultiplier ×c 0.8<br>Weapon.HorizontalRecoilMultiplier ×c 0.92<br>Weapon.SpreadMultiplier ×c 0.99<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_MUZL_049` | Weapon.VerticalRecoilMultiplier ×c 0.9<br>Weapon.HorizontalRecoilMultiplier ×c 0.94<br>Weapon.SpreadMultiplier ×c 0.9<br>Weapon.AimTime ×c 1.12 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_050` | Weapon.VerticalRecoilMultiplier ×c 0.86<br>Weapon.HorizontalRecoilMultiplier ×c 0.98<br>Weapon.SpreadMultiplier ×c 0.98<br>Weapon.AimTime ×c 1.03 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_051` | Weapon.VerticalRecoilMultiplier ×c 0.94<br>Weapon.HorizontalRecoilMultiplier ×c 0.95<br>Weapon.SpreadMultiplier ×c 0.92<br>Weapon.AimTime ×c 1.08 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_052` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 0.99<br>Weapon.AimTime ×c 0.98 |  |  |  |  |
| `GE_MUZL_053` | Weapon.VerticalRecoilMultiplier ×c 0.97<br>Weapon.HorizontalRecoilMultiplier ×c 0.97<br>Weapon.SpreadMultiplier ×c 0.95<br>Weapon.AimTime ×c 1.1 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_054` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 0.99<br>Weapon.AimTime ×c 0.98 |  |  |  |  |
| `GE_MUZL_055` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 0.99<br>Weapon.AimTime ×c 0.98 |  |  |  |  |
| `GE_MUZL_056` | Weapon.VerticalRecoilMultiplier ×c 0.95<br>Weapon.HorizontalRecoilMultiplier ×c 0.96<br>Weapon.SpreadMultiplier ×c 0.92<br>Weapon.AimTime ×c 1.08 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_057` | Weapon.VerticalRecoilMultiplier ×c 0.96<br>Weapon.HorizontalRecoilMultiplier ×c 0.97<br>Weapon.SpreadMultiplier ×c 0.9<br>Weapon.AimTime ×c 1.05 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_058` | Weapon.VerticalRecoilMultiplier ×c 0.94<br>Weapon.HorizontalRecoilMultiplier ×c 0.95<br>Weapon.SpreadMultiplier ×c 0.9<br>Weapon.AimTime ×c 1.08 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_059` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 0.92<br>Weapon.AimTime ×c 0.98 |  |  |  |  |
| `GE_MUZL_060` | Weapon.VerticalRecoilMultiplier ×c 0.96<br>Weapon.HorizontalRecoilMultiplier ×c 0.96<br>Weapon.SpreadMultiplier ×c 0.93<br>Weapon.AimTime ×c 1.07 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_061` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 0.97<br>Weapon.AimTime ×c 0.98 |  |  |  |  |
| `GE_MUZL_062` | Weapon.VerticalRecoilMultiplier ×c 0.96<br>Weapon.HorizontalRecoilMultiplier ×c 0.96<br>Weapon.SpreadMultiplier ×c 0.93<br>Weapon.AimTime ×c 1.04 |  |  |  |  |
| `GE_MUZL_065` | Weapon.VerticalRecoilMultiplier ×c 0.94<br>Weapon.HorizontalRecoilMultiplier ×c 0.95<br>Weapon.SpreadMultiplier ×c 0.9<br>Weapon.AimTime ×c 1.08 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_066` | Weapon.VerticalRecoilMultiplier ×c 0.94<br>Weapon.HorizontalRecoilMultiplier ×c 0.95<br>Weapon.SpreadMultiplier ×c 0.9<br>Weapon.AimTime ×c 1.08 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_067` | Weapon.VerticalRecoilMultiplier ×c 0.92<br>Weapon.HorizontalRecoilMultiplier ×c 0.94<br>Weapon.SpreadMultiplier ×c 0.9<br>Weapon.AimTime ×c 1.08 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_068` | Weapon.VerticalRecoilMultiplier ×c 0.9<br>Weapon.HorizontalRecoilMultiplier ×c 1.05<br>Weapon.SpreadMultiplier ×c 0.9<br>Weapon.AimTime ×c 1.02 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_069` | Weapon.VerticalRecoilMultiplier ×c 0.93<br>Weapon.HorizontalRecoilMultiplier ×c 0.94<br>Weapon.SpreadMultiplier ×c 0.9<br>Weapon.AimTime ×c 1.1 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_070` | Weapon.VerticalRecoilMultiplier ×c 0.95<br>Weapon.HorizontalRecoilMultiplier ×c 0.94<br>Weapon.SpreadMultiplier ×c 0.9<br>Weapon.AimTime ×c 1.1 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MUZL_071` | Weapon.VerticalRecoilMultiplier ×c 0.85<br>Weapon.HorizontalRecoilMultiplier ×c 1.05<br>Weapon.SpreadMultiplier ×c 0.88<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_MUZL_072` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.SpreadMultiplier ×c 1<br>Weapon.AimTime ×c 0.97 |  |  |  |  |

## GE_SGHT (34)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_SGHT_009` | Weapon.AdsZoomMultiplier = 1.2<br>Weapon.AimTime ×c 0.85<br>Weapon.MaxZeroingRange = Weapon.MinZeroingRange (Current) |  |  |  |  |
| `GE_SGHT_011` | Weapon.AdsZoomMultiplier = 3<br>Weapon.AimTime ×c 1.12<br>Weapon.MaxZeroingRange = 600<br>Weapon.MinZeroingRange = 100 |  |  |  |  |
| `GE_SGHT_011_CharacterEffects` | Character.WeaponSway.StabilizationTimeMultiplier = 1.6 |  |  |  |  |
| `GE_SGHT_011_MainSight` | Weapon.AdsZoomMultiplier = 3 |  |  |  |  |
| `GE_SGHT_016` | Weapon.AdsZoomMultiplier = 1.2<br>Weapon.AimTime ×c 0.85<br>Weapon.MaxZeroingRange = Weapon.MinZeroingRange (Current) |  |  |  |  |
| `GE_SGHT_023` | Weapon.AdsZoomMultiplier = 1.2<br>Weapon.AimTime ×c 0.85<br>Weapon.MaxZeroingRange = Weapon.MinZeroingRange (Current) |  |  |  |  |
| `GE_SGHT_025` | Weapon.AdsZoomMultiplier = 1.2<br>Weapon.AimTime ×c 1.02<br>Weapon.MaxZeroingRange = Weapon.MinZeroingRange (Current) |  |  |  |  |
| `GE_SGHT_026` | Weapon.AimTime ×c 0.97<br>Weapon.AdsZoomMultiplier = 1.5<br>Weapon.MinZeroingRange = 100<br>Weapon.MaxZeroingRange = 200 |  |  |  |  |
| `GE_SGHT_027` | Weapon.AdsZoomMultiplier = 1.2<br>Weapon.AimTime ×c 0.87<br>Weapon.MaxZeroingRange = Weapon.MinZeroingRange (Current) |  |  |  |  |
| `GE_SGHT_028` | Weapon.AimTime ×c 1.05<br>Weapon.AdsZoomMultiplier = 2<br>Weapon.MinZeroingRange = 100<br>Weapon.MaxZeroingRange = 300 |  |  |  |  |
| `GE_SGHT_029` | Weapon.AdsZoomMultiplier = 3<br>Weapon.MinZeroingRange = 100<br>Weapon.MaxZeroingRange = 300<br>Weapon.AimTime ×c 1.1 |  |  |  |  |
| `GE_SGHT_029_CharacterEffects` | Character.WeaponSway.StabilizationTimeMultiplier × 1 |  |  |  |  |
| `GE_SGHT_030` | Weapon.MaxZeroingRange = 400<br>Weapon.MinZeroingRange = 100 |  |  |  |  |
| `GE_SGHT_030_CharacterEffects` | Character.WeaponSway.StabilizationTimeMultiplier × 1.5 |  |  |  |  |
| `GE_SGHT_030_MainSight` | Weapon.AimTime ×c 1.1<br>Weapon.AdsZoomMultiplier = 4 |  |  |  |  |
| `GE_SGHT_030_TopSight` | Weapon.AimTime ×c 1.05<br>Weapon.AdsZoomMultiplier = 1.2 |  |  |  |  |
| `GE_SGHT_031` | Weapon.AdsZoomMultiplier = 6<br>Weapon.AimTime ×c 1.15<br>Weapon.MaxZeroingRange = 600<br>Weapon.MinZeroingRange = 100 |  |  |  |  |
| `GE_SGHT_031_CharacterEffects` | Character.WeaponSway.StabilizationTimeMultiplier = 1.6<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.8<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.4 |  |  |  |  |
| `GE_SGHT_031_MainSight` | Weapon.AdsZoomMultiplier = 6 |  |  |  |  |
| `GE_SGHT_032` | Weapon.AimTime × 1.2<br>Weapon.AdsZoomMultiplier = 2.5<br>Weapon.MaxZeroingRange = 1000<br>Weapon.MinZeroingRange = 100 |  |  |  |  |
| `GE_SGHT_032_CharacterEffects` | Character.WeaponSway.StabilizationTimeMultiplier = 1.6<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.8<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.4 |  |  |  |  |
| `GE_SGHT_033` | Weapon.AdsZoomMultiplier = 1.2<br>Weapon.AimTime ×c 1 |  |  |  |  |
| `GE_SGHT_034` | Weapon.AdsZoomMultiplier = 2.8<br>Weapon.AimTime ×c 1.15<br>Weapon.MinZeroingRange = 10<br>Weapon.MaxZeroingRange = 10 |  |  |  |  |
| `GE_SGHT_034_CharacterEffects` | Character.WeaponSway.StabilizationTimeMultiplier × 1 |  |  |  |  |
| `GE_SGHT_036` | Weapon.AimTime × 1 |  |  |  |  |
| `GE_SGHT_036_CharacterEffects` | Character.WeaponSway.StabilizationTimeMultiplier = 1.6 |  |  |  |  |
| `GE_SGHT_036_MainSight` | Weapon.AdsZoomMultiplier = 6<br>Weapon.AimTime ×c 1.12<br>Weapon.MaxZeroingRange = 600<br>Weapon.MinZeroingRange = 100 |  |  |  |  |
| `GE_SGHT_036_TopSight` | Weapon.AimTime ×c 1.05<br>Weapon.AdsZoomMultiplier = 1.2 |  |  |  |  |
| `GE_SGHT_037` | Weapon.AdsZoomMultiplier = 1.2<br>Weapon.AimTime ×c 1 |  |  |  |  |
| `GE_SGHT_038` | Weapon.AdsZoomMultiplier = 1.2<br>Weapon.AimTime ×c 1<br>Weapon.MaxZeroingRange = Weapon.MinZeroingRange (Current) |  |  |  |  |
| `GE_SGHT_039` | Weapon.AdsZoomMultiplier = 3<br>Weapon.AimTime ×c 1.15<br>Weapon.MaxZeroingRange = 800<br>Weapon.MinZeroingRange = 100 |  |  |  |  |
| `GE_SGHT_039_CharacterEffects` | Character.WeaponSway.StabilizationTimeMultiplier = 1.6<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.8<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.4 |  |  |  |  |
| `GE_SGHT_040` | Weapon.AdsZoomMultiplier = 3.5<br>Weapon.AimTime ×c 1.15<br>Weapon.MaxZeroingRange = 800<br>Weapon.MinZeroingRange = 100 |  |  |  |  |
| `GE_SGHT_040_CharacterEffects` | Character.WeaponSway.StabilizationTimeMultiplier = 1.6<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.8<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.4 |  |  |  |  |

## GE_Player (30)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_Player_BarbedWireSlow` | Movement.MaxSpeedMultiplier = 0.075 |  |  |  |  |
| `GE_Player_Emote_FullBody` | — |  |  | `State.Player.Action.Emote.FullBody` |  |
| `GE_Player_Fists` | Movement.SprintSpeedMultiplier ×c 1.1 |  |  |  |  |
| `GE_Player_GhilliEffects` | Character.AdsTimeMultiplier ×c 0.8<br>Character.AimSwayScaleMultiplier ×c 1.15<br>Movement.LeanTimeMultiplier ×c 1.15<br>Movement.UnleanTimeMultiplier ×c 1.15<br>Movement.MaxSpeedMultiplier ×c 0.95<br>Movement.JumpVelocityMultiplier ×c 0.95 |  |  |  | apply require: `State.Player.Ghilli.BodySuit`, `State.Player.Ghilli.Headwear` |
| `GE_Player_Ghilli_Armor` | — |  |  | `State.Player.Ghilli.BodySuit` |  |
| `GE_Player_Ghilli_Helmet` | — |  |  | `State.Player.Ghilli.Headwear` | remove ignore: `State.Player.Vitality.Dead` |
| `GE_Player_InsideCamoTent` | — |  |  | `State.Location.InsideCamoTent` |  |
| `GE_Player_Jump` | Character.AimSwayScaleMultiplier × Character.Weight (Current) via `CT_WeaponSway[StanceTransition_AimSwayScale]`<br>Character.AimSwaySpeedMultiplier × Character.Weight (Current) via `CT_WeaponSway[StanceTransition_AimSwaySpeed]` | 2 | 2 |  |  |
| `GE_Player_Landing` | Character.AimSwayScaleMultiplier × SetByCaller(Action.Player.Fall), fallback 1<br>Character.AimSwaySpeedMultiplier × SetByCaller(Action.Player.Fall), fallback 1 | 10 | 3 |  |  |
| `GE_Player_Mantle` | Character.AimSwayScaleMultiplier × Character.Weight (Current) via `CT_WeaponSway[Mantle_AimSwayScale]`<br>Character.AimSwaySpeedMultiplier × Character.Weight (Current) via `CT_WeaponSway[Mantle_AimSwaySpeed]` | 10 | 2 |  |  |
| `GE_Player_MaxSpeedMultiplier_Aiming` | Movement.MaxSpeedMultiplier × SetByCaller(Movement.MaxSpeedMultiplier), fallback 1 |  |  |  | ongoing require: `State.Player.Movement.Aiming` |
| `GE_Player_MaxSpeedMultiplier_Covert` | Movement.MaxSpeedMultiplier × SetByCaller(Movement.MaxSpeedMultiplier), fallback 1 |  |  |  | ongoing query: `AnyTagsMatch(State.Player.Stance.Current.Crouched, State.Player.Stance.Current.Prone)` |
| `GE_Player_ReadyToFirePlayRate` | Movement.ReadyToFirePlayRate × SetByCaller(Movement.ReadyToFirePlayRate), fallback 1 |  |  |  |  |
| `GE_Player_RessedByEnemy` | — | 60 |  | `State.Player.RessedByEnemy` |  |
| `GE_Player_SprintSpeedMultiplier` | Movement.SprintSpeedMultiplier × SetByCaller(Movement.SprintSpeedMultiplier), fallback 1<br>Movement.TacSprintSpeedMultiplier × SetByCaller(Movement.TacSprintSpeedMultiplier), fallback 1 |  |  |  |  |
| `GE_Player_SprintSpeedMultiplier_Temp` | Movement.SprintSpeedMultiplier × SetByCaller(Movement.SprintSpeedMultiplier)<br>Movement.TacSprintSpeedMultiplier × SetByCaller(Movement.TacSprintSpeedMultiplier) | 5 |  |  |  |
| `GE_Player_StaminaRegenPerSecondMultiplier` | Movement.StaminaRegenPerSecondMultiplier × SetByCaller(Movement.StaminaRegenPerSecondMultiplier), fallback 1 |  |  |  |  |
| `GE_Player_StaminaRegenPerSecondMultiplier_Covert` | Movement.StaminaRegenPerSecondMultiplier × SetByCaller(Movement.StaminaRegenPerSecondMultiplier), fallback 1 |  |  |  | ongoing query: `AnyTagsMatch(State.Player.Stance.Current.Crouched, State.Player.Stance.Current.Prone)` |
| `GE_Player_Stance_Crouch` | — |  |  | `State.Player.Stance.Current.Crouched` |  |
| `GE_Player_Stance_Prone` | — |  |  | `State.Player.Stance.Current.Prone` |  |
| `GE_Player_Stance_Transition` | Character.AimSwayScaleMultiplier × Character.Weight (Current) via `CT_WeaponSway[StanceTransition_AimSwayScale]`<br>Character.AimSwaySpeedMultiplier × Character.Weight (Current) via `CT_WeaponSway[StanceTransition_AimSwaySpeed]` | 5 | 3 |  |  |
| `GE_Player_StopSprint` | Character.AimSwayScaleMultiplier × SetByCaller(Action.Player.StopSprint), fallback 1<br>Character.AimSwaySpeedMultiplier × SetByCaller(Action.Player.StopSprint), fallback 1<br>Character.WeaponSway.TranslationStabilizationMultiplier × SetByCaller(Action.Player.StopSprint), fallback 1<br>Character.WeaponSway.RotationStabilizationMultiplier × SetByCaller(Action.Player.StopSprint), fallback 1<br>Character.WeaponSway.TranslationMultiplier × SetByCaller(Action.Player.StopSprint), fallback 1<br>Character.WeaponSway.RotationMultiplier × SetByCaller(Action.Player.StopSprint), fallback 1<br>Character.WeaponSway.StabilizationTimeMultiplier × SetByCaller(Action.Player.StopSprint), fallback 1 | 10 |  |  |  |
| `GE_Player_StopSprint_WeightEffect` | Character.AimSwayScaleMultiplier × Character.Weight (Current) via `CT_WeaponSway[StopSprintWeight_AimSwayScale]`<br>Character.AimSwaySpeedMultiplier × Character.Weight (Current) via `CT_WeaponSway[StopSprintWeight_AimSwaySpeed]`<br>Character.WeaponSway.TranslationStabilizationMultiplier × Character.Weight (Current) via `CT_WeaponSway[StopSprintWeight_TranslationStabilizationSway]`<br>Character.WeaponSway.RotationStabilizationMultiplier × Character.Weight (Current) via `CT_WeaponSway[StopSprintWeight_RotationStabilizationSway]`<br>Character.WeaponSway.TranslationMultiplier × Character.Weight (Current) via `CT_WeaponSway[StopSprintWeight_TranslationSway]`<br>Character.WeaponSway.RotationMultiplier × Character.Weight (Current) via `CT_WeaponSway[StopSprintWeight_RotationSway]` | 5 | 3 |  |  |
| `GE_Player_TacSprintEpired` | Character.AimSwayScaleMultiplier × Character.Weight (Current) via `CT_WeaponSway[StopTacSprint_AimSwayScale]`<br>Character.AimSwaySpeedMultiplier × Character.Weight (Current) via `CT_WeaponSway[StopTacSprint_AimSwaySpeed]`<br>Character.WeaponSway.TranslationStabilizationMultiplier × SetByCaller(Character.Weight), fallback 1<br>Character.WeaponSway.RotationStabilizationMultiplier × SetByCaller(Character.Weight), fallback 1<br>Character.WeaponSway.TranslationMultiplier × SetByCaller(Character.Weight), fallback 1<br>Character.WeaponSway.RotationMultiplier × SetByCaller(Character.Weight), fallback 1 | 15 |  |  |  |
| `GE_Player_TacSprintStaminaUsageMultiplier` | Movement.TacSprintStaminaUsageMultiplier × SetByCaller(Movement.TacSprintStaminaUsageMultiplier), fallback 1 |  |  |  |  |
| `GE_Player_Vaulting` | Character.AimSwayScaleMultiplier × Character.Weight (Current) via `CT_WeaponSway[Vaulting_AimSwayScale]`<br>Character.AimSwaySpeedMultiplier × Character.Weight (Current) via `CT_WeaponSway[Vaulting_AimSwaySpeed]` | 5 | 3 |  |  |
| `GE_Player_Weight_Heavy` | Movement.MaxSpeedMultiplier ×c 0.8<br>Movement.LeanTimeMultiplier ×c 1.5<br>Movement.UnleanTimeMultiplier ×c 1.5<br>Movement.JumpVelocityMultiplier ×c 0.85<br>Character.Weight + 3<br>Character.AimSwayScaleMultiplier × 1.175<br>Character.AimSwaySpeedMultiplier × 1.2<br>Character.AdsTimeMultiplier ×c 1.15<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.5 |  |  | `State.Player.Weight.Heavy` |  |
| `GE_Player_Weight_Light` | Movement.MaxSpeedMultiplier ×c 0.95<br>Movement.JumpVelocityMultiplier ×c 0.95<br>Character.Weight + 1<br>Movement.StaminaRegenPerSecondMultiplier ×c 0.85<br>Character.AimSwayScaleMultiplier × 1.02<br>Character.AimSwaySpeedMultiplier × 1.05<br>Character.AdsTimeMultiplier ×c 1.05 |  |  | `State.Player.Weight.Light` |  |
| `GE_Player_Weight_Medium` | Movement.MaxSpeedMultiplier ×c 0.875<br>Movement.JumpVelocityMultiplier ×c 0.9<br>Character.Weight + 2<br>Movement.StaminaRegenPerSecondMultiplier ×c 0.65<br>Character.AimSwayScaleMultiplier × 1.085<br>Character.AimSwaySpeedMultiplier × 1.1<br>Character.AdsTimeMultiplier ×c 1.06<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.3 |  |  | `State.Player.Weight.Medium` |  |
| `GE_Player_Weight_SuperHeavy` | Movement.MaxSpeedMultiplier ×c 0.8<br>Movement.LeanTimeMultiplier ×c 1.5<br>Movement.UnleanTimeMultiplier ×c 1.5<br>Movement.JumpVelocityMultiplier ×c 0.65<br>Character.Weight + 4<br>Character.AimSwayScaleMultiplier × 1.2<br>Character.AimSwaySpeedMultiplier × 1.25<br>Character.AdsTimeMultiplier ×c 1.17<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.7 |  |  | `State.Player.Weight.SuperHeavy` |  |

## GE_Weapon (25)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_Weapon_AimTime` | Weapon.AimTime × SetByCaller(Weapon.AimTime), fallback 1 |  |  |  |  |
| `GE_Weapon_EquipSpeedMultiplier` | Weapon.EquipSpeedMultiplier × SetByCaller(Weapon.EquipSpeedMultiplier), fallback 1 |  |  |  |  |
| `GE_Weapon_HorizontalRecoilMultiplier` | Weapon.HorizontalRecoilMultiplier × SetByCaller(Weapon.HorizontalRecoilMultiplier), fallback 1 |  |  |  |  |
| `GE_Weapon_StanceRecoil_AR_Crouch` | Weapon.VerticalRecoilMultiplier ×c 0.85<br>Weapon.HorizontalRecoilMultiplier ×c 0.85 |  |  |  |  |
| `GE_Weapon_StanceRecoil_AR_Prone` | Weapon.VerticalRecoilMultiplier ×c 0.7<br>Weapon.HorizontalRecoilMultiplier ×c 0.7 |  |  |  |  |
| `GE_Weapon_StanceRecoil_AR_Standing` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_Weapon_StanceRecoil_DMR_Crouch` | Weapon.VerticalRecoilMultiplier ×c 0.85<br>Weapon.HorizontalRecoilMultiplier ×c 0.85 |  |  |  |  |
| `GE_Weapon_StanceRecoil_DMR_Prone` | Weapon.VerticalRecoilMultiplier ×c 0.7<br>Weapon.HorizontalRecoilMultiplier ×c 0.7 |  |  |  |  |
| `GE_Weapon_StanceRecoil_DMR_Standing` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_Weapon_StanceRecoil_LMG_Crouch` | Weapon.VerticalRecoilMultiplier ×c 0.6<br>Weapon.HorizontalRecoilMultiplier ×c 0.6 |  |  |  |  |
| `GE_Weapon_StanceRecoil_LMG_Prone` | Weapon.VerticalRecoilMultiplier ×c 0.35<br>Weapon.HorizontalRecoilMultiplier ×c 0.25 |  |  |  |  |
| `GE_Weapon_StanceRecoil_LMG_Standing` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_Weapon_StanceRecoil_Pistol_Crouch` | Weapon.VerticalRecoilMultiplier ×c 0.85<br>Weapon.HorizontalRecoilMultiplier ×c 0.85 |  |  |  |  |
| `GE_Weapon_StanceRecoil_Pistol_Prone` | Weapon.VerticalRecoilMultiplier ×c 0.7<br>Weapon.HorizontalRecoilMultiplier ×c 0.7 |  |  |  |  |
| `GE_Weapon_StanceRecoil_Pistol_Standing` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_Weapon_StanceRecoil_SMG_Crouch` | Weapon.VerticalRecoilMultiplier ×c 0.85<br>Weapon.HorizontalRecoilMultiplier ×c 0.85 |  |  |  |  |
| `GE_Weapon_StanceRecoil_SMG_Prone` | Weapon.VerticalRecoilMultiplier ×c 0.7<br>Weapon.HorizontalRecoilMultiplier ×c 0.7 |  |  |  |  |
| `GE_Weapon_StanceRecoil_SMG_Standing` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_Weapon_StanceRecoil_SR_Crouch` | Weapon.VerticalRecoilMultiplier ×c 0.85<br>Weapon.HorizontalRecoilMultiplier ×c 0.85 |  |  |  |  |
| `GE_Weapon_StanceRecoil_SR_Prone` | Weapon.VerticalRecoilMultiplier ×c 0.7<br>Weapon.HorizontalRecoilMultiplier ×c 0.7 |  |  |  |  |
| `GE_Weapon_StanceRecoil_SR_Standing` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_Weapon_StanceRecoil_Shotgun_Crouch` | Weapon.VerticalRecoilMultiplier ×c 0.85<br>Weapon.HorizontalRecoilMultiplier ×c 0.85 |  |  |  |  |
| `GE_Weapon_StanceRecoil_Shotgun_Prone` | Weapon.VerticalRecoilMultiplier ×c 0.7<br>Weapon.HorizontalRecoilMultiplier ×c 0.7 |  |  |  |  |
| `GE_Weapon_StanceRecoil_Shotgun_Standing` | Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_Weapon_VerticalRecoilMultiplier` | Weapon.VerticalRecoilMultiplier × SetByCaller(Weapon.VerticalRecoilMultiplier), fallback 1 |  |  |  |  |

## GE_MAG (15)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_MAG_FAL_10rd` | Weapon.AimTime ×c 0.85<br>Weapon.VerticalRecoilMultiplier ×c 0.84<br>Weapon.HorizontalRecoilMultiplier ×c 0.85<br>Weapon.EquipSpeedMultiplier ×c 1.24 |  |  |  |  |
| `GE_MAG_FAL_10rd_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 0.78 |  |  |  |  |
| `GE_MAG_Glock_17rd` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAG_LMG_02_100rd` | Weapon.AimTime ×c 1.1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAG_LMG_02_100rd_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAG_M249_200rd` | Weapon.AimTime ×c 1.2<br>Weapon.VerticalRecoilMultiplier ×c 1.17<br>Weapon.HorizontalRecoilMultiplier ×c 1.17<br>Weapon.EquipSpeedMultiplier ×c 0.93 |  |  |  |  |
| `GE_MAG_M249_200rd_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.25 |  |  |  |  |
| `GE_MAG_MK22_10rd` | Weapon.AimTime ×c 1.06<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.EquipSpeedMultiplier ×c 0.9 |  |  |  |  |
| `GE_MAG_MK22_10rd_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.12 |  |  |  |  |
| `GE_MAG_SMG_03` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAG_SMG_03_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAG_SR_04_5rd` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAG_SV98_10rd` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_MAG_SV98_10rd_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_MAG_SVDM` | Weapon.AimTime ×c 1.06<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.EquipSpeedMultiplier ×c 0.9 |  |  |  |  |

## GE_FGP (10)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_FGP_02` | Weapon.VerticalRecoilMultiplier ×c 0.7<br>Weapon.HorizontalRecoilMultiplier ×c 0.85<br>Weapon.SpreadMultiplier ×c 0.83<br>Weapon.AimTime ×c 1.1<br>Weapon.EquipSpeedMultiplier ×c 0.92 |  |  |  |  |
| `GE_FGP_02_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.9<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.93<br>Character.AimSwayVerticalMovementMultiplier ×c 0.74<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.78<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.7 |  |  |  |  |
| `GE_FGP_03` | Weapon.VerticalRecoilMultiplier ×c 0.94<br>Weapon.HorizontalRecoilMultiplier ×c 0.75<br>Weapon.SpreadMultiplier ×c 0.78<br>Weapon.AimTime ×c 0.85<br>Weapon.EquipSpeedMultiplier ×c 1.1 |  |  |  |  |
| `GE_FGP_03_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.95<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.95<br>Character.AimSwayVerticalMovementMultiplier ×c 0.9<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.88<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.8 |  |  |  |  |
| `GE_FGP_04_BipodState` | Weapon.VerticalRecoilMultiplier ×c 0.25<br>Weapon.HorizontalRecoilMultiplier ×c 0.28<br>Weapon.SpreadMultiplier ×c 0.45<br>Weapon.AimTime ×c 0.92 |  |  |  |  |
| `GE_FGP_04_BipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.55<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.5<br>Character.AimSwayVerticalMovementMultiplier ×c 0.5<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.78<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.6 |  |  |  |  |
| `GE_FGP_04_NonBipodState` | Weapon.VerticalRecoilMultiplier ×c 0.88<br>Weapon.HorizontalRecoilMultiplier ×c 0.9<br>Weapon.SpreadMultiplier ×c 0.94<br>Weapon.AimTime ×c 1.1<br>Weapon.EquipSpeedMultiplier ×c 0.98 |  |  |  |  |
| `GE_FGP_04_NonBipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.95<br>Character.AimSwayHorizontalMovementMultiplier ×c 0.9<br>Character.AimSwayVerticalMovementMultiplier ×c 0.88<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.78<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.6 |  |  |  |  |
| `GE_FGP_04_UnfoldedBipodState` | Weapon.VerticalRecoilMultiplier ×c 1.15<br>Weapon.HorizontalRecoilMultiplier ×c 1.15<br>Weapon.SpreadMultiplier ×c 1.15<br>Weapon.AimTime ×c 1.05 |  |  |  |  |
| `GE_FGP_04_UnfoldedBipodState_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 1.05<br>Character.AimSwayHorizontalMovementMultiplier ×c 1.05<br>Character.AimSwayVerticalMovementMultiplier ×c 1.1<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.08<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.08 |  |  |  |  |

## GE_MZL (7)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_MZL_04` | Weapon.VerticalRecoilMultiplier ×c 0.84<br>Weapon.HorizontalRecoilMultiplier ×c 0.9<br>Weapon.SpreadMultiplier ×c 0.88<br>Weapon.AimTime ×c 1.15 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MZL_05` | Weapon.VerticalRecoilMultiplier ×c 0.9<br>Weapon.HorizontalRecoilMultiplier ×c 0.94<br>Weapon.SpreadMultiplier ×c 0.91<br>Weapon.AimTime ×c 1.08 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MZL_06` | Weapon.VerticalRecoilMultiplier ×c 0.88<br>Weapon.HorizontalRecoilMultiplier ×c 0.95<br>Weapon.SpreadMultiplier ×c 0.92<br>Weapon.AimTime ×c 1.1 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MZL_07` | Weapon.VerticalRecoilMultiplier ×c 0.88<br>Weapon.HorizontalRecoilMultiplier ×c 0.93<br>Weapon.SpreadMultiplier ×c 0.9<br>Weapon.AimTime ×c 1.1 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MZL_08` | Weapon.VerticalRecoilMultiplier ×c 0.82<br>Weapon.HorizontalRecoilMultiplier ×c 0.9<br>Weapon.SpreadMultiplier ×c 0.89<br>Weapon.AimTime ×c 1.12 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MZL_09` | Weapon.VerticalRecoilMultiplier ×c 0.86<br>Weapon.HorizontalRecoilMultiplier ×c 0.92<br>Weapon.SpreadMultiplier ×c 0.88<br>Weapon.AimTime ×c 1.12 |  |  | `Weapon.State.Suppressed` |  |
| `GE_MZL_10` | Weapon.VerticalRecoilMultiplier ×c 0.9<br>Weapon.HorizontalRecoilMultiplier ×c 0.94<br>Weapon.SpreadMultiplier ×c 0.91<br>Weapon.AimTime ×c 1.1 |  |  | `Weapon.State.Suppressed` |  |

## GE_AK74 (6)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_AK74_Mag_30rd` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1 |  |  |  |  |
| `GE_AK74_Mag_30rd_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_AK74_Mag_Drum75rd` | Weapon.AimTime ×c 1.26<br>Weapon.VerticalRecoilMultiplier ×c 1.22<br>Weapon.HorizontalRecoilMultiplier ×c 1.24<br>Weapon.EquipSpeedMultiplier ×c 0.93 |  |  |  |  |
| `GE_AK74_Mag_Drum75rd_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.24 |  |  |  |  |
| `GE_AK74_Mag_Ext60rd` | Weapon.AimTime ×c 1.19<br>Weapon.VerticalRecoilMultiplier ×c 1.19<br>Weapon.HorizontalRecoilMultiplier ×c 1.21<br>Weapon.EquipSpeedMultiplier ×c 0.93 |  |  |  |  |
| `GE_AK74_Mag_Ext60rd_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1.21 |  |  |  |  |

## GE_4xElcanSpectr (3)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_4xElcanSpectr_CharacterEffects` | Character.WeaponSway.StabilizationTimeMultiplier × 1.5 |  |  |  |  |
| `GE_4xElcanSpectr_MainSight` | Weapon.AimTime ×c 1.1<br>Weapon.AdsZoomMultiplier = 4 |  |  |  |  |
| `GE_4xElcanSpectr_TopSight` | Weapon.AimTime ×c 1.05<br>Weapon.AdsZoomMultiplier = 1.2 |  |  |  |  |

## GE_Item (4)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_Item_LargeTacVest` | Character.ReloadSpeedMultiplier × 1.08<br>Character.UtilityEquipSpeedMultiplier × 1.08<br>Character.UtilityHolsterSpeedMultiplier × 1.08 |  |  |  |  |
| `GE_Item_MediumTacVest` | Character.ReloadSpeedMultiplier × 1.05<br>Character.UtilityEquipSpeedMultiplier × 1.05<br>Character.UtilityHolsterSpeedMultiplier × 1.05 |  |  |  |  |
| `GE_Item_SmallTacVest` | Character.ReloadSpeedMultiplier × 1.02<br>Character.UtilityEquipSpeedMultiplier × 1.02<br>Character.UtilityHolsterSpeedMultiplier × 1.02 |  |  |  |  |
| `GE_Item_UsageRateMultiplier` | Item.UsageRateMultiplier × SetByCaller(Item.UsageRateMultiplier), fallback 1 |  |  |  |  |

## GE_GrantSkill (3)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_GrantSkill_DoorBreach` | — |  |  | `Skill.DoorBreach` |  |
| `GE_GrantSkill_Lockpicking` | — |  |  | `Skill.Lockpicking` |  |
| `GE_GrantSkill_SniperKillFocusRefresh` | — |  |  | `Skill.SniperKillFocusRefresh` |  |

## GE_Spotting (3)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_Spotting_CustomDepthStencilValue` | CustomDepthStencilValue = SetByCaller(CustomDepthStencilValue), fallback 1 |  |  |  |  |
| `GE_Spotting_IncreasedSpottedTime` | Spotting.SpottedTimeMultiplier × SetByCaller(Spotting.SpottedTimeMultiplier), fallback 1 |  |  |  |  |
| `GE_Spotting_IncreasedSpottingDuration` | Spotting.SpottingDurationMultiplier × SetByCaller(Spotting.SpottingDurationMultiplier), fallback 1 |  |  |  | apply require: `Item.Archetype.Spotting` |

## GE_Vehicle (3)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_Vehicle_FuelUsageReductionMultiplier` | FuelUsageReductionMultiplier = SetByCaller(FuelUsageReductionMultiplier), fallback 1 |  |  |  |  |
| `GE_Vehicle_Health` | Health × SetByCaller(Health), fallback 0 |  |  |  |  |
| `GE_Vehicle_ImpactReductionMultiplier` | Health.ImpactReductionMultiplier = SetByCaller(Health.ImpactReductionMultiplier), fallback 1 |  |  |  |  |

## Other effects (37)

| Effect | Modifiers | Duration | Stacks | Granted tags | Requirements |
|---|---|---:|---:|---|---|
| `GE_10xScope` | Weapon.AimTime × 1.15<br>Weapon.AdsZoomMultiplier = 6<br>Weapon.MaxZeroingRange = 1000<br>Weapon.MinZeroingRange = 100 |  |  |  |  |
| `GE_10xScope_CharacterEffects` | Character.WeaponSway.StabilizationTimeMultiplier = 1.6<br>Character.WeaponSway.RotationStabilizationMultiplier × 1.8<br>Character.WeaponSway.TranslationStabilizationMultiplier × 1.4 |  |  |  |  |
| `GE_3xScope` | Weapon.AdsZoomMultiplier = 3<br>Weapon.MinZeroingRange = 100<br>Weapon.MaxZeroingRange = 300<br>Weapon.AimTime ×c 1.1 |  |  |  |  |
| `GE_3xScope_CharacterEffects` | Character.WeaponSway.StabilizationTimeMultiplier × 1.35 |  |  |  |  |
| `GE_4xElcanSpectr` | Weapon.MaxZeroingRange = 400<br>Weapon.MinZeroingRange = 100 |  |  |  |  |
| `GE_4xHybrid` | Weapon.AdsZoomMultiplier = 4<br>Weapon.AimTime + 0.35 |  |  |  |  |
| `GE_6xScope` | Weapon.AdsZoomMultiplier = 3<br>Weapon.AimTime + 0.2<br>Weapon.MaxZeroingRange = 500<br>Weapon.MinZeroingRange = 100 |  |  |  |  |
| `GE_6xScope_MainSight` | Weapon.AdsZoomMultiplier = 3 |  |  |  |  |
| `GE_ADS` | Movement.MaxSpeedMultiplier ×c 0.5 |  |  |  |  |
| `GE_CantedIrons` | Weapon.AimTime = 0.1<br>Weapon.AdsZoomMultiplier = 2 |  |  |  |  |
| `GE_Defib` | — |  |  | `State.Player.Action.Appliable.Reviving.Friendly` |  |
| `GE_DoorBreach` | Movement.MaxSpeedMultiplier × 1 × `CT_DoorMovement[Door Breach Ramp In and Out]` @Duration<br>Character.AimSwayScaleMultiplier × Character.Weight (Current) via `CT_WeaponSway[StopTacSprint_AimSwayScale]`<br>Character.AimSwaySpeedMultiplier × Character.Weight (Current) via `CT_WeaponSway[StopTacSprint_AimSwaySpeed]` | 0.8 |  |  |  |
| `GE_DrawBow` | Movement.MaxSpeedMultiplier ×c 0.9 |  |  |  |  |
| `GE_EotechHoloSight` | Weapon.AdsZoomMultiplier = 1.2<br>Weapon.AimTime ×c 0.9<br>Weapon.MinZeroingRange = 100<br>Weapon.MaxZeroingRange = 100 |  |  |  |  |
| `GE_ForceOpenDoor` | — |  |  | `State.Player.ForceOpenDoor` |  |
| `GE_GRP_05` | Weapon.HorizontalRecoilMultiplier = 0<br>Weapon.VerticalRecoilMultiplier = 0 |  |  |  |  |
| `GE_HeavyHelmet_Passive` | Character.SuppressionReductionMultiplier × 0.32 |  |  |  | remove ignore: `State.Player.Vitality.Dead` |
| `GE_MMGL_RotaryPassengerSway` | Character.AimSwayScaleMultiplier ×c 4<br>Character.AimSwaySpeedMultiplier ×c 1.25<br>Character.WeaponAccuracyMultiplier ×c 2.5<br>Character.AdsTimeMultiplier ×c 1.5<br>Character.ReloadSpeedMultiplier ×c 0.9 |  |  |  | ongoing require: `State.Player.Vehicle.Seat.LittleBirdBench` |
| `GE_Meta_ResourceChange` | Attribute.Meta.Currency.Cash + SetByCaller(Attribute.Meta.Currency.Cash)<br>Attribute.Meta.XP.Role.Driver + SetByCaller(Attribute.Meta.XP.Role.Driver)<br>Attribute.Meta.Currency.SkillPoint.Role.Driver + SetByCaller(Attribute.Meta.Currency.SkillPoint.Role.Driver)<br>Attribute.Meta.XP.Role.Infantry + SetByCaller(Attribute.Meta.XP.Role.Infantry)<br>Attribute.Meta.Currency.SkillPoint.Role.Infantry + SetByCaller(Attribute.Meta.Currency.SkillPoint.Role.Infantry)<br>Attribute.Meta.XP.Role.Medic + SetByCaller(Attribute.Meta.XP.Role.Medic)<br>Attribute.Meta.Currency.SkillPoint.Role.Medic + SetByCaller(Attribute.Meta.Currency.SkillPoint.Role.Medic)<br>Attribute.Meta.XP.Role.Pilot + SetByCaller(Attribute.Meta.XP.Role.Pilot)<br>Attribute.Meta.Currency.SkillPoint.Role.Pilot + SetByCaller(Attribute.Meta.Currency.SkillPoint.Role.Pilot)<br>Attribute.Meta.XP.Role.Recon + SetByCaller(Attribute.Meta.XP.Role.Recon)<br>Attribute.Meta.Currency.SkillPoint.Role.Recon + SetByCaller(Attribute.Meta.Currency.SkillPoint.Role.Recon)<br>Attribute.Meta.XP.Role.Support + SetByCaller(Attribute.Meta.XP.Role.Support)<br>Attribute.Meta.Currency.SkillPoint.Role.Support + SetByCaller(Attribute.Meta.Currency.SkillPoint.Role.Support)<br>Attribute.Meta.XP.Platform.Bobcat + SetByCaller(Attribute.Meta.XP.Platform.Bobcat)<br>Attribute.Meta.XP.Platform.Havoc + SetByCaller(Attribute.Meta.XP.Platform.Havoc)<br>Attribute.Meta.XP.Platform.Huey + SetByCaller(Attribute.Meta.XP.Platform.Huey)<br>Attribute.Meta.XP.Platform.Kodiak + SetByCaller(Attribute.Meta.XP.Platform.Kodiak)<br>Attribute.Meta.XP.Platform.Leopard + SetByCaller(Attribute.Meta.XP.Platform.Leopard)<br>Attribute.Meta.XP.Platform.LittleBird + SetByCaller(Attribute.Meta.XP.Platform.LittleBird)<br>Attribute.Meta.XP.Platform.PZH2000 + SetByCaller(Attribute.Meta.XP.Platform.PZH2000)<br>Attribute.Meta.XP.Platform.SpawnVehicle + SetByCaller(Attribute.Meta.XP.Platform.SpawnVehicle)<br>Attribute.Meta.XP.Platform.WEPN_004 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_004)<br>Attribute.Meta.XP.Platform.WEPN_001 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_001)<br>Attribute.Meta.XP.Platform.WEPN_013 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_013)<br>Attribute.Meta.XP.Platform.WEPN_010 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_010)<br>Attribute.Meta.XP.Platform.WEPN_020 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_020)<br>Attribute.Meta.XP.Platform.WEPN_003 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_003)<br>Attribute.Meta.XP.Platform.WEPN_009 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_009)<br>Attribute.Meta.XP.Platform.WEPN_002 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_002)<br>Attribute.Meta.XP.Platform.WEPN_012 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_012)<br>Attribute.Meta.XP.Platform.WEPN_021 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_021)<br>Attribute.Meta.XP.Platform.WEPN_014 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_014)<br>Attribute.Meta.XP.Platform.WEPN_019 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_019)<br>Attribute.Meta.XP.Platform.WEPN_016 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_016)<br>Attribute.Meta.XP.Platform.WEPN_022 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_022)<br>Attribute.Meta.XP.Platform.WEPN_007 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_007)<br>Attribute.Meta.XP.Platform.WEPN_015 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_015)<br>Attribute.Meta.XP.Platform.WEPN_005 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_005)<br>Attribute.Meta.XP.Platform.WEPN_006 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_006)<br>Attribute.Meta.XP.Platform.WEPN_025 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_025)<br>Attribute.Meta.XP.Platform.WEPN_024 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_024)<br>Attribute.Meta.XP.Platform.WEPN_011 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_011)<br>Attribute.Meta.XP.Platform.WEPN_023 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_023)<br>Attribute.Meta.XP.Platform.WEPN_018 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_018)<br>Attribute.Meta.XP.Platform.WEPN_008 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_008)<br>Attribute.Meta.XP.Platform.WEPN_017 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_017)<br>Attribute.Meta.XP.Platform.WEPN_026 + SetByCaller(Attribute.Meta.XP.Platform.WEPN_026) |  |  |  |  |
| `GE_MolotovBurning` | — |  |  | `State.Player.Molotov.Burning` |  |
| `GE_OPT_08` | Weapon.AimTime ×c 1.05<br>Weapon.AdsZoomMultiplier = 2.5<br>Weapon.MinZeroingRange = 100<br>Weapon.MaxZeroingRange = 300 |  |  |  |  |
| `GE_PWSCQB74` | Weapon.VerticalRecoilMultiplier ×c 0.8<br>Weapon.HorizontalRecoilMultiplier ×c 0.97<br>Weapon.SpreadMultiplier ×c 0.96<br>Weapon.AimTime ×c 1.04 |  |  | `Weapon.State.Suppressed` |  |
| `GE_PilotHelmet_Active` | — |  |  | `State.Player.Armor.PilotHelmet.Active` | ongoing query: `AnyExprMatch(AllTagsMatch(State.Player.Vehicle.Rotary, State.Player.Vehicle.Role.Driver), AllTagsMatch(State.Player.Vehicle.Rotary, State.Player.Vehicle.Role.Gunner))`<br>remove ignore: `State.Player.Vitality.Dead` |
| `GE_PilotHelmet_Passive` | — |  |  | `State.Player.Armor.PilotHelmet.Passive` | ongoing ignore: `State.Player.Armor.PilotHelmet.Active`<br>remove ignore: `State.Player.Vitality.Dead` |
| `GE_RK6` | Weapon.VerticalRecoilMultiplier ×c 0.85<br>Weapon.HorizontalRecoilMultiplier ×c 0.92<br>Weapon.SpreadMultiplier ×c 0.85<br>Weapon.AimTime ×c 1.1<br>Weapon.EquipSpeedMultiplier ×c 1 |  |  |  |  |
| `GE_RK6_CharacterEffects` | Character.AimSwaySpeedMultiplier ×c 0.92<br>Character.AimSwayHorizontalMovementMultiplier ×c 1<br>Character.AimSwayVerticalMovementMultiplier ×c 0.88<br>Character.WeaponSway.TranslationStabilizationMultiplier × 0.88<br>Character.WeaponSway.RotationStabilizationMultiplier × 0.78 |  |  |  |  |
| `GE_RedDot` | Weapon.AdsZoomMultiplier = 1.2<br>Weapon.AimTime ×c 0.9<br>Weapon.MaxZeroingRange = Weapon.MinZeroingRange (Current) |  |  |  |  |
| `GE_ShootingRangeTutorial_FlyBy` | — |  |  | `State.CharacterModifier.Vehicle.ShootingRange` |  |
| `GE_Stanag_30Rounds` | Weapon.AimTime ×c 1<br>Weapon.VerticalRecoilMultiplier ×c 1<br>Weapon.HorizontalRecoilMultiplier ×c 1<br>Weapon.EquipSpeedMultiplier ×c 0.98 |  |  |  |  |
| `GE_Stanag_30Rounds_CharacterEffects` | Character.AimSwayScaleMultiplier ×c 1 |  |  |  |  |
| `GE_SuperHeavyHelmet_Passive` | Character.SuppressionReductionMultiplier × 0.2 |  |  | `State.Player.Armor.SuperHeavyHelmet.Passive` | remove ignore: `State.Player.Vitality.Dead` |
| `GE_TankHelmet_Active` | Character.SuppressionReductionMultiplier = 0 |  |  | `State.Player.Armor.TankHelmet.Active` | ongoing query: `AnyExprMatch(AllTagsMatch(State.Player.Vehicle.Role.Driver, State.Player.Vehicle.Tracked), AllTagsMatch(State.Player.Vehicle.Role.Gunner, State.Player.Vehicle.Tracked))`<br>remove ignore: `State.Player.Vitality.Dead` |
| `GE_TankHelmet_Passive` | — |  |  | `State.Player.Armor.TankHelmet.Passive` | ongoing ignore: `State.Player.Armor.TankHelmet.Active`<br>remove ignore: `State.Player.Vitality.Dead` |
| `GE_UnlimitedTacSprint` | Movement.TacSprintStaminaUsageMultiplier = 0<br>Weapon.FocusEnergyUsageMultiplier = 0 | 60 |  | `State.Player.Stimulant.UnlimitedTacSprint`<br>`State.Player.InhibitWeight.StepDown` |  |
| `GE_UseAppliable` | Movement.MaxSpeedMultiplier ×c 0.5 |  |  |  |  |
| `GE_UsePlaceable` | Movement.MaxSpeedMultiplier ×c 0.4 |  |  |  |  |
| `GE_Weapons_DetonatorRangeMultiplier` | Weapon.DetonatorRangeMultiplier × SetByCaller(Weapon.DetonatorRangeMultiplier), fallback 1 |  |  |  |  |
