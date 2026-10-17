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
- **Current value** = `((Base + ΣAdd) × (1 + Σ(Multiply − 1)) / D) × ΠMultiplyCompound + ΣAddFinal`,
  unless an Override is active. Stacks scale each modifier linearly
  (§4.2, §4.4).
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
| `ApplyEffect(Effect, Stacks, CustomMagnitudes, Mode)` | Native `0x5227F20`. `Stacks` is clamped to `[1, MaxStacks]` (`MaxStacks` 0 = 65535) by `0x522B1B0`; every call creates a new instance (§5) |
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

Grouped by filename prefix. Each effect's actual modifiers are on
[Gameplay Effect Values](Wardogs_GameplayEffect_Values_v1.md), exported
from the paks: 341 packages, the 338 SDK classes plus
`GE_GrantSkill_Lockpicking`, `GE_Meta_ResourceChange` and
`GE_MolotovBurning`.

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
value when no curve row is set, otherwise `Value × Curve(0)`;
`StackCount` evaluates the curve at the stack count; `StackCountNRM` uses
the stack count normalised by the effect's settings; `Lifetime` and
`Duration` index by time (Duration returns 0 when the effect's `Duration`
is 0).

**Stack scaling** (`0x522B7D0`) then applies to each modifier's
magnitude `m` for `n` stacks: `m' = (m − I) × n + I`, with `I = 0` for
Add, AddFinal and MultiplyCompound and `I = 1` for Multiply and Divide.
It is skipped for Override and for Scalars indexed by `StackCount` or
`StackCountNRM`, whose curve already uses the stacks. A modifier with 0
stacks is excluded. So `n` stacks of a ×1.1 Multiply give ×(1 + 0.1n),
and `n` stacks of a MultiplyCompound `v` give `v × n`, not `vⁿ`.

The combining function is `0x522E5C0`. The dirty-attribute flush
`0x522C4F0` starts from the base value (`+0x28`), runs each channel block
(record `+0x40`, stride `0x60`) through it (via the default evaluator
lambda `0x522A800`), and writes the result through `0x5237050` into the
current value (`+0x30`). The formula is in §4.4.

### 4.3 Base-value writes

**Native.** The base setter `0x5236E50` runs the attribute's base-value
hook, stores the new base, and pushes it into `AttributeReplication`
(`0x52382E0`) under a role check. Its direct callers are
`SetAttributeBaseValue` (`0x5236AF0`), the library `ModifyBase`
(`0x523A560`) and `SetBase` (`0x523AB10`), `FindOrAddAttribute`
(`0x522F8F0`) and the replication handler (`0x5233C00`). No effect-apply
function calls it, so modifiers feed only the current value; `0x522C4F0`
recomputes it from the base after every base write (§4.4).

**Hooks.** The component keeps hooks per attribute in a map at `+0x378`.
Each entry holds a base-value hook (registered through `0x5236990`, run
by the base setter) and a current-value hook (registered through
`0x5236C70`, run by the current-value setter `0x5237050`). The setters
pass the value to a hook as a float and take a float back, so a hooked
value loses double precision. Three functions call the two registration
helpers:

- vehicle health sections: `0x533A750` clamps to `[0, MaxHealth]`
  ([VehicleDamagePipeline §5.4](Wardogs_VehicleDamagePipeline_v1.md#54-hits-to-destroy));
- character health (`0x6B81CE0`, role 3 only): virtual slot 161, which
  clamps to `[0, MaxHealth + MaxOverhealHealth + MaxDecayHealth]` for
  characters (`0x6B17D20`; at least 1 while `bInvincible`) and to
  `[0, MaxHealth]` otherwise (`0x6B83270`);
- vehicle fuel (`0x7666070`).

No other path registers a hook: the two helpers have no other call or
pointer reference, and the map insert (`0x5223670`, emplace `0x521FDE0`)
is reached only from them. No `Attribute.Gameplay.Weapon.*` attribute has
a hook.

`SetAttributeBaseValue` is reached through two helpers:

- `0x52311D0` adds a delta to the attribute's stored value and calls it.
  Used by **character damage** (vitality `0x6B82520`, DamagePipeline §10),
  `Auth_Heal` (`0x6B83360`), the vehicle fuel component and others.
- `0x5236DE0`, a convenience wrapper, used by `ResetHealth` (`0x6B83560`),
  `Auth_DecreaseContainerAmount` (`0x6C66540`), the character's revive
  handler (`0x6E75620`, which writes `Attribute.Gameplay.PreTipValue`),
  the tipping component and vehicle weapon code.

### 4.4 Current value

**Native** (`0x522E5C0`). When any Override modifier is active, the first
active one in the attribute's Override list wins and nothing else counts.
Otherwise:

```
Current = ((Base + ΣAdd) × (1 + Σ(Multiply − 1)) / D) × ΠMultiplyCompound + ΣAddFinal
D       = 1 + Σ(Divide − 1), or 1 when |D| ≤ 1e-8
```

- The sums and the product run over the stack-scaled magnitudes (§4.2).
- Multiply and Divide add up among themselves: ×1.1 and ×1.2 give ×1.3,
  not ×1.32. Only MultiplyCompound multiplies.
- Only the `Default` channel exists (`EBHAttributeModChannel` has
  `Default` and `COUNT`), so every attribute has one block.
- The per-operation arrays live in the attribute record at
  `+0x40 + 0x60 × Channel + 0x10 × Op` (element stride `0x20`). An element
  counts only when its Filter passed (`+0x18`) and it has a magnitude
  (`+0x10`).
- The arithmetic is in doubles, but the magnitudes come from floats in
  the asset, so 0.7 enters as 0.699999988.

**Example.** `VerticalRecoilMultiplier` starts at 1.0 on every weapon
([Weapons §4](Wardogs_GameFeatures_Weapons_v2.md#4-default-weapon-attributes-wditemextensiondata_gameplayeffects)).
With `GE_FGRP_006` (×c 0.75) and `GE_Weapon_StanceRecoil_AR_Prone`
(×c 0.7), one stack each: 1.0 × 0.75 × 0.699999988 = 0.5249999911. No
weapon attribute has a hook (§4.3).

## 5. Application and prediction

**Native** (`ApplyEffect`, `0x5227F20`). When the component's role check
(`0x3CA8630`) does not return 3, a local predicted instance is created
only if a component flag (`+0x280`) is clear, `Mode` is not
`AuthorityOnly`, and the effect's `bAllowClientPredictedApplication`
(`+0x220`) is set. It then goes to `0x5219AB0` when `Mode` is
`ClientInstigated` and `ClientInstigatedApplicationPolicy` (`+0x222`) is
Enable, otherwise to `0x5219C70`.

Every `ApplyEffect` call creates its own instance: applying the same
effect twice gives two instances, never one with more stacks. The
effect's stacking policies are read only in `0x52317F0`.

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
From the effect export ([Gameplay Effect Values](Wardogs_GameplayEffect_Values_v1.md)):
`GE_6xScope` sets `Weapon.AdsZoomMultiplier = 3`, adds 0.2 to
`Weapon.AimTime`, and sets the zeroing range to 100–500;
`GE_6xScope_MainSight` sets `Weapon.AdsZoomMultiplier = 3`.

**Native.** On equip, `0x6C9F1A0` applies the attachment's
`AppliedEffects`, and `0x6C9E190` the selected sight's effects, to the
weapon item's own effect component (`WDItemExtension_GameplayEffects`
`+0xF0`), one stack each, after removing that slot's earlier handles.
The calls come from `0x6C9D170`, which is reached from
`SetPredictedAttachment`, `OnRep_ReplicatedAttachmentMap` and a delegate
bound in slot 159.

### 7.1 What applies to a weapon

These rules give a weapon's final attributes for an attachment set. [Weapon Attributes](Wardogs_WeaponAttributes_v1.md) applies them to every weapon and attachment.

- **Base.** The weapon item's `WDItemExtensionData_GameplayEffects.DefaultAttributes`, installed into the item's own component (`OnRegister` `0x6C692E0`). The `AimTime` in `WDItemExtensionData_RangedWeapon.DefaultAttributes` never changes the base: it is installed later with overwrite off (`0x6C9AFB0`).
- **Effects on the weapon** (the item's component, `+0xF0`), one stack each:
  - every equipped attachment's `AppliedEffects`;
  - the selected sight's `SightsData[name].AppliedEffects`;
  - with an underbarrel bipod unfolded, also its unfolded list (`FWDBipodAttachmentData` `+0x138`, `0x6C9F6E0`);
  - the stance preset `StanceGameplayEffects[stance]`, applied by `OnStanceChanged` (`0x6C9A420`, mode `AuthorityOnly`) with the preset's stack count, which is 1 in all data.
- **Not on the weapon.** `AppliedCharacterEffects` and the bipod's `+0x148` list go to the owning character's component (`WDMoverCharacter` `+0x740`), following the equip state.
- **Evaluation.** Each application is its own instance; the stacking policies act only in `0x52317F0`. Every modifier `Filter` is empty, and no weapon-related effect has requirements, a duration or `MaxStacks`. So every modifier counts with `n = 1`, and the §4.4 formula applies with no hook.
- **Data exceptions.**
  - `ID_MAGZ_065` and `ID_MAGZ_066` list the same effect in `AppliedEffects` and `AppliedCharacterEffects`.
  - The stance maps are keyed by stance, and two use mismatched effects: `ID_A91` maps Stand to `AR_Prone` (×c 0.7) and Crouch and Prone to `AR_Standing`, and `ID_WEPN_037` maps Prone to `AR_Standing`.
  - Seven sight effects override `MaxZeroingRange` with the current `MinZeroingRange` (an attribute-backed modifier).

Not traced: which sight name is selected first, how the bipod's `MountedAppliedEffects` (`+0x158`) apply, and when the attribute-backed zeroing magnitude is captured.

## 8. Open questions

| # | Question |
|---|---|
| E-1 | **Closed** (§4.4): the combining function is `0x522E5C0`, run by the flush `0x522C4F0` after every base write; stack scaling is linear per operation (§4.2) |
| E-2 | Duration semantics beyond 0 (for example whether −1 means infinite) |
| E-3 | Rollback mechanism and the role of `UNetworkPredictionWorldManager` |
| E-4 | **Closed**: every effect's modifiers, durations, stacks and granted tags are on [Gameplay Effect Values](Wardogs_GameplayEffect_Values_v1.md) |
| E-5 | **Closed** (§7): `0x6C9F1A0` / `0x6C9E190` apply attachment and sight effects to the weapon item's own component |
| E-6 | Vehicle health via effects: `GE_Vehicle_Health` and vehicle-side callers of `0x52311D0` (`0x7665D60`, and the `Auth_RefillFuel` exec thunk `0x7667280`; the corpus row `0x766727F` is an empty nullsub one byte early) are not traced |
| E-7 | **Closed**: `+0x150` = `OngoingRequirements` not met (`0x52330B0`, `0x522CB40`), so the effect's modifiers are excluded; `+0x3C` = pending predicted stack delta (`0x52313E0`, `0x5231DA0`); `+0x100` / `+0x12C` = `Num` / `NumFreeIndices` of the pending predicted-removal key set at `+0xF8` (equal = empty) |

## 9. Cross-references

- [`BHGameplayEffects_classes.hpp`](sdk/raw/BHGameplayEffects_classes.hpp), [`BHGameplayEffects_structs.hpp`](sdk/raw/BHGameplayEffects_structs.hpp), [`BHGameplayPrediction_classes.hpp`](sdk/raw/BHGameplayPrediction_classes.hpp), `sdk/raw/GE_*_classes.hpp` (338 files)
- [`Wardogs_DamagePipeline_v2.md`](Wardogs_DamagePipeline_v2.md): the rule pipeline and the character health write (§10)
- [`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md): vehicle sections, which reduce `Attribute.Gameplay.Health.*` attributes
- [`Wardogs_GameplayTags_v1.md`](Wardogs_GameplayTags_v1.md): tag catalog
- [`docs/evidence/effects.md`](docs/evidence/effects.md): evidence behind the native addresses, with a verification status for every RVA this page cites

## Change log

| Date | Change |
|---|---|
| 2026-10-16 | v1: BH-GAS architecture, 338 GE classes by prefix, attribute map, prediction question. |
| 2026-10-17 | Corrected against the decompilation corpus, SDK and data: attributes are double base/current records (the map is only defaults); `Modifiers` element type and operations documented; stacking is a per-modifier curve; base-value writes and the damage path traced; preset types, catalog descriptions, StanceRecoil count (21), the three preset files and the example rewritten from data; authority language removed; cues are a separate component. |
| 2026-10-17 | Effect values exported from the paks and published on Gameplay Effect Values; E-4 closed; the scope example uses the real modifiers. |
| 2026-10-17 | Independent verifier pass: closed E-1 with the combining formula (§4.4); stack scaling is linear per operation, not a curve (§4.2); `Fixed` with a curve row returns `Value × Curve(0)`; the attribute hooks and their three registrants (§4.3); E-7 added. |
| 2026-10-17 | Round-4 verifier pass: E-5 closed (§7) with what applies to a weapon (§7.1); E-7 closed; no weapon attribute has a hook; character health's hook clamps; `ApplyEffect` stacks are clamped and every call is a new instance (§5); E-6 citation corrected. |
