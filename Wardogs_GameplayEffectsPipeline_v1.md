---
title: "Gameplay Effects Pipeline"
parent: "Pipelines"
nav_order: 3
---

# Wardogs — Gameplay Effects Pipeline

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

How gameplay effects (GEs) and attributes work in Wardogs: weapon
attachment modifiers, player movement and stance modifiers, skills, and
the attribute store that also holds health. Companion to
[`Wardogs_DamagePipeline_v2.md`](Wardogs_DamagePipeline_v2.md) and
[`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md).

Build: `++Wardogs+Live-CL-516586` · Engine: UE 5.7 · GAS fork: "BH"
(Embark's in-house GAS variant) · Native addresses are file RVAs in the
restored executable (damage doc §11). Labels: **Native** (code, RVA cited,
unreviewed decompiler output), **SDK**, **Data**, **Open**.

---

## TL;DR

- **`UBHGameplayEffect`** defines an effect: duration, stacking,
  modifiers, granted tags, requirement tags.
- **`UBHGameplayEffectComponent`** carries the active effects and the
  attributes of an actor.
- **Attributes are records keyed by gameplay tag**, each with a double
  base value and current value, replicated as a fast array. There are no
  game `UAttributeSet` subclasses. `DefaultAttributes`
  (`TMap<FGameplayTag, float>`) only holds initial values.
- **338 `GE_*` classes** ship in the SDK, all `: public UBHGameplayEffect`.
- **Damage does not go through effects.** Character damage writes the
  `Attribute.Gameplay.Health` base value directly (DamagePipeline §10).

## 1. The core classes

### 1.1 `UBHGameplayEffect` (0x270 bytes)

**SDK**, [`BHGameplayEffects_classes.hpp`](sdk/raw/BHGameplayEffects_classes.hpp):

| Offset | Field | Type | Notes |
|---|---|---|---|
| 0x30 | `Duration` | `float` | The Duration-indexed scalar returns 0 when this is 0 (§4.2); "−1 = infinite" is not verified |
| 0x34 | `MaxStacks` | `uint16` | |
| 0x36 | `StackDurationRefreshPolicy` | enum | |
| 0x37 | `StackExpirationPolicy` | enum | |
| 0x38 | `Modifiers` | `TArray<FBHAttributeModifier>` | Dumper shows `TArray<FNone_>`; the element type is in §4.2 |
| 0x48 | `GrantedTags` | `FGameplayTagContainer` | |
| 0x68 | `ApplicationRequirements` | `FBHGameplayTagRequirements` | |
| 0xF0 | `OngoingRequirements` | `FBHGameplayTagRequirements` | |
| 0x178 | `RemovalRequirements` | `FBHGameplayTagRequirements` | |
| 0x200 | `Tags` | `FGameplayTagContainer` | |
| 0x220 | `bAllowClientPredictedApplication` | `bool` | Read by `ApplyEffect` (§5) |
| 0x221 | `bAllowClientPredictedModification` | `bool` | |
| 0x222 | `ClientInstigatedApplicationPolicy` | enum | Read by `ApplyEffect` (§5) |

### 1.2 `UBHGameplayEffectComponent` (0xCD0 bytes)

**SDK.** Inherits `UBHGameplayPredictionComponent`.

| Offset | Field | Notes |
|---|---|---|
| 0x288 | `DefaultAttributes` | `TMap<FGameplayTag, float>`: initial values only |
| 0x378 | per-attribute hook map | Run by the base-value setter (§4.3) |
| 0x3D8 | `AttributeReplication` | Fast array of `FBHGameplayAttributeRepData` |
| 0x508 | `EffectContainer` | Active effects |
| 0x998 | `TagSerializer_AllCounts` | |
| 0xB18 | `TagSerializer_ReplicatedOnly` | |
| 0xC98 | `NetworkPredictionWorldManager` | Pointer; its role in rollback is not traced |

Functions (reflected names; native bodies where traced):

| Function | Notes |
|---|---|
| `ApplyEffect(Effect, …, CustomMagnitudes, Mode)` | Native `0x5227F20`; prediction branches in §5 |
| `ApplyLocalEffect(…)` | "Client-only" is not verified |
| `ModifyEffectCustomMagnitude`, `ModifyEffectStacks`, `RemoveEffect` | |
| `FindOrAddAttribute(Attribute, InitialValue, …)` | Native `0x522F8F0` |
| `SetAttributeBaseValue(…, Handle, newbase)` | Native `0x5236AF0`, gated on a role check; calls the setter `0x5236E50`. Used by the damage path through `0x52311D0` (§4.3) |
| `ServerApplyEffect(request, SyncFrame)` | Thunk `0x521B800` runs a check (`0x5236230`, prediction-key fields and effect class) before `0x5236070` |
| `ServerModifyEffect`, `UpdateGameplayTag` | |

### 1.3 `UBHGameplayEffectLibrary`

| Function | Notes |
|---|---|
| `GetValues(Handle, Base, Current, …)` | Reads base and current |
| `ModifyBase(…)` | Native `0x523A560` |
| `SetBase(…)` | Native `0x523AB10` |
| `MakeLocalEffectHandle(…)` | |

### 1.4 `UBHTaggedGameplayEffects`

A data asset holding `TMap<GameplayTag, FBHGameplayEffectPreset>`. The
preset's `Effect` is a `TSubclassOf` (not a soft pointer), `Stacks` is
`int32`, and `CustomMagnitudes` lists magnitude overrides. The soft class
pointer belongs to a different struct, `FBHGameplayEffectTaggedTableRow.GameplayEffect`.

## 2. The effect catalog

**SDK.** 338 `sdk/raw/GE_*_classes.hpp` files, every class
`: public UBHGameplayEffect`. **Data:** 332 distinct `GE_*_C` class names
are referenced somewhere in the export. One of them,
`GE_GrantSkill_Lockpicking` (from the Lockpicking feature's
`DT_Skills_Lockpicking.json`), has no SDK header, and eight SDK classes are
never referenced.

Grouped by filename prefix. The descriptions say only what the class
names show; effect values are not in the export (§7).

| Prefix | Count | What the names show |
|---|---:|---|
| `GE_MAGZ_*` | 60 | Magazine attachments |
| `GE_FGRP_*` | 54 | Foregrip attachments |
| `GE_MUZL_*` | 47 | Muzzle attachments |
| `GE_SGHT_*` | 34 | Sights and scopes |
| `GE_Player_*` | 30 | Movement, stance, weight, ghillie, jump and mantle modifiers (no stimulant, bleed or stun effects) |
| `GE_Weapon_*` | 25 | Aim time, equip speed, recoil, per-stance recoil |
| `GE_MAG_*` | 15 | Short-prefix magazines |
| `GE_FGP_*` | 10 | Short-prefix foregrips |
| `GE_MZL_*` | 7 | Short-prefix muzzles |
| `GE_AK74_*` | 6 | AK74-specific attachments |
| `GE_Item_*` | 4 | Three tac vests and `UsageRateMultiplier` |
| `GE_4xElcanSpectr_*` | 4 | 4× Elcan sight |
| `GE_Vehicle_*` | 3 | `FuelUsageReductionMultiplier`, `Health`, `ImpactReductionMultiplier` |
| `GE_Spotting_*` | 3 | `CustomDepthStencilValue`, `IncreasedSpottedTime`, `IncreasedSpottingDuration` |
| `GE_TankHelmet_*` | 2 | Tank helmet |
| `GE_Stanag_*` | 2 | STANAG magazine |
| `GE_RK6_*` | 2 | RK6 foregrip (`ID_RK6_Grip.json`) |
| `GE_PilotHelmet_*` | 2 | Pilot helmet |
| `GE_GrantSkill_*` | 2 | Skill grants |
| `GE_6xScope_*` | 2 | 6× scope |

`GE_Weapon_StanceRecoil_*` is 21 classes: 7 weapon archetypes × 3 stances
(Standing, Crouch, Prone).

## 3. The data presets

**Data.**

- [`DA_CharacterEffectPresets`](data/Wardogs/Content/GameMechanics/GameplayEffects/Presets/DA_CharacterEffectPresets.json):
  one row, `GameplayCue.Door.Breach` → `GE_DoorBreach_C`, 1 stack.
- [`DA_DefaultPlayerEffects`](data/Wardogs/Content/GameMechanics/GameplayEffects/Presets/DA_DefaultPlayerEffects.json):
  one row, `Skill.DoorBreach` → `GE_GrantSkill_DoorBreach_C`, 1 stack.
  When it is applied (for example on spawn) is not traced.
- [`DA_CharacterModifierState_StimulantEffects`](data/Wardogs/Plugins/GameFeatures/Items/StimPen/Content/Data/DA_CharacterModifierState_StimulantEffects.json)
  is not an effect catalog. It is a `WDCharacterModifierStateDefinition`:
  an FOV camera modifier (×1.05) gated on
  `State.Player.Stimulant.UnlimitedTacSprint` and ignored while
  `State.Player.Vitality.Critical`. It contains no GEs.

## 4. The attribute system

### 4.1 Attribute records

**Native + SDK.** At runtime each attribute is a record keyed by its tag,
holding a **double** base value (record `+0x28`) and current value
(`+0x30`) and its owning component (`+0x18`). Records replicate through
`AttributeReplication` as
`FBHGameplayAttributeRepData {AttributeTag, double BaseValue @0x18, double CurrentValue @0x20}`;
the receive handler is `0x5233C00`. `DefaultAttributes` supplies the
initial floats.

Attribute tags come from the native tag initializers, for example
`Attribute.Gameplay.Health`, `Attribute.Gameplay.Health.Max`,
`Attribute.Gameplay.Fuel` and the vehicle part healths
`Attribute.Gameplay.Health.Engine`, `.Tail`, `.Tracks`. No
`Attribute.Weapon.*` tags exist.

### 4.2 Modifiers

**SDK.** Each entry of `UBHGameplayEffect::Modifiers` is an
`FBHAttributeModifier`:

| Field | Type |
|---|---|
| `Attribute` (0x00) | `FGameplayTag` |
| `Operation` (0x08) | `EBHAttributeModOp`: `Add`, `Multiply`, `Divide`, `MultiplyCompound`, `AddFinal`, `Override` |
| `Channel` (0x09) | `EBHAttributeModChannel` |
| `Modifier` (0x10) | `FInstancedStruct`: one of `FBHAttributeMod_Scalar`, `FBHAttributeMod_Attribute`, `FBHAttributeMod_SetByCaller` |
| `Filter` (0x20) | `FBHGameplayTagRequirements` |

**Native.** The Scalar evaluator (`0x522E960`) switches on
`CurveIndexing` (`EBHAttributeScalarIndex`): `Fixed` returns the plain
value; `StackCount` evaluates the curve at the stack count;
`StackCountNRM` uses the stack count normalised by the effect's settings;
`Lifetime` and `Duration` index by time (Duration returns 0 when the
effect's `Duration` is 0). **Stack scaling is therefore a per-modifier
curve set in data**, not a fixed linear or multiplicative rule.

How the operations and channels combine into the current value is
**Open**: the combining function is not located.

### 4.3 Base-value writes

**Native.** The base setter `0x5236E50` runs the per-attribute hook (map
at `+0x378`, probably a clamp), stores the new base, and pushes it into
`AttributeReplication` (`0x52382E0`) under a role check. Its direct
callers are `SetAttributeBaseValue` (`0x5236AF0`), the library
`ModifyBase` (`0x523A560`) and `SetBase` (`0x523AB10`),
`FindOrAddAttribute` (`0x522F8F0`) and the replication handler
(`0x5233C00`). No effect-apply function calls it, so modifiers most
likely feed the current value instead.

`SetAttributeBaseValue` is reached through two helpers:

- `0x52311D0` adds a delta to the attribute's stored value and calls it.
  Used by **character damage** (vitality `0x6B82520`, DamagePipeline §10),
  `Auth_Heal` (`0x6B83360`), the vehicle fuel component and others.
- `0x5236DE0`, a convenience wrapper, used by `ResetHealth` (`0x6B83560`),
  `Auth_DecreaseContainerAmount` (`0x6C66540`), the character's revive
  handler (`0x6E75620`, which writes `Attribute.Gameplay.PreTipValue`),
  the tipping component and vehicle weapon code.

## 5. Application and prediction

**Native** (`ApplyEffect`, `0x5227F20`). When the component's role check
(`0x3CA8630`) does not return 3, a local predicted instance is created
only if a component flag (`+0x280`) is clear, `Mode` is not
`AuthorityOnly`, and the effect's `bAllowClientPredictedApplication`
(`+0x220`) is set. It then goes to `0x5219AB0` when `Mode` is
`ClientInstigated` and `ClientInstigatedApplicationPolicy` (`+0x222`) is
Enable, otherwise to `0x5219C70`.

These are code facts. What they mean for authority, and how rollback
works, are **Open**; the doc makes no server-authority claim, and
security questions go through [`SECURITY.md`](SECURITY.md).

## 6. Gameplay cues

**Native.** Cues are handled by a separate component,
`UWDGameplayCueComponent` (module WDGameplayCue), with multicast invoke
RPCs. Not every cue comes from an effect: `GameplayCue.Player.ReviveAlly`
is fired by a direct call (`0x6E75620` → `0x4C45DC0`).

## 7. Example: a scope attachment

**Data.** `ID_6xScope.json` lists `GE_6xScope_C` in
`AttachmentData.AppliedEffects`, and `GE_6xScope_MainSight_C` per sight.
The code that applies them on equip is not traced, and the effects'
modifier values are not in the export (the `GE_*` assets were not
exported).

## 8. Open questions

| # | Question |
|---|---|
| E-1 | How `EBHAttributeModOp` operations and channels combine into the current value |
| E-2 | Duration semantics beyond 0 (for example whether −1 means infinite) |
| E-3 | Rollback mechanism and the role of `UNetworkPredictionWorldManager` |
| E-4 | `GE_*` asset values (modifiers, durations, granted tags): needs the assets exported |
| E-5 | The equip code path that applies attachment effects |
| E-6 | Vehicle health via effects: `GE_Vehicle_Health` and vehicle-side callers of `0x52311D0` (`0x7665D60`, `0x766727F`) are not traced |

## 9. Cross-references

- [`BHGameplayEffects_classes.hpp`](sdk/raw/BHGameplayEffects_classes.hpp), [`BHGameplayEffects_structs.hpp`](sdk/raw/BHGameplayEffects_structs.hpp), [`BHGameplayPrediction_classes.hpp`](sdk/raw/BHGameplayPrediction_classes.hpp), `sdk/raw/GE_*_classes.hpp` (338 files)
- [`Wardogs_DamagePipeline_v2.md`](Wardogs_DamagePipeline_v2.md): the rule pipeline and the character health write (§10)
- [`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md): vehicle sections, which reduce `Attribute.Gameplay.Health.*` attributes
- [`Wardogs_GameplayTags_v1.md`](Wardogs_GameplayTags_v1.md): tag catalog

## Change log

| Date | Change |
|---|---|
| 2026-10-16 | v1: BH-GAS architecture, 338 GE classes by prefix, attribute map, prediction question. |
| 2026-10-17 | Corrected against the decompilation corpus, SDK and data: attributes are double base/current records (the map is only defaults); `Modifiers` element type and operations documented; stacking is a per-modifier curve; base-value writes and the damage path traced; preset types, catalog descriptions, StanceRecoil count (21), the three preset files and the example rewritten from data; authority language removed; cues are a separate component. |
