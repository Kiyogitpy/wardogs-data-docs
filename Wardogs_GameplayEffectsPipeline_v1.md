# Wardogs — Gameplay Effects Pipeline (v1)

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Complete code↔data trace of **gameplay effects (GEs)** in Wardogs — the
system that models buffs, debuffs, weapon-attachment modifiers, status
states, player skills, and timed cues. Third pipeline doc after
[`Wardogs_DamagePipeline_v1.md`](Wardogs_DamagePipeline_v1.md) (infantry)
and [`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md).

Build: `++Wardogs+Live-CL-516586` · Engine: UE 5.7 · GAS fork: "BH"
(Embark Studios in-house GAS variant)

---

## TL;DR

Wardogs uses Embark's custom **BH-GAS fork** rather than Unreal's
vanilla GameplayAbilitySystem. Core architecture:

- **`UBHGameplayEffect`** = effect definition (duration, stacks,
  modifiers, grant tags, requirement tags)
- **`UBHGameplayEffectComponent`** = actor component carrying active
  effects + attributes
- **`UBHTaggedGameplayEffects`** = data asset that maps GameplayTag →
  specific effect preset
- **338 GE_* subclasses** in the SDK, each a specific gameplay effect
  (weapon attachments, player states, cues, etc.)

**No `UAttributeSet` subclasses** — attributes are implemented as a
`TMap<FGameplayTag, float>` on the component rather than typed C++
fields. This is the key BH-GAS divergence from vanilla UE GAS.

## 1. The core classes

### 1.1 `UBHGameplayEffect` (0x270 bytes)

Base class for all gameplay effects. Defined in
[`sdk/raw/BHGameplayEffects_classes.hpp`](sdk/raw/BHGameplayEffects_classes.hpp).

Properties:

| Offset | Field | Type | Purpose |
|---|---|---|---|
| 0x30 | `Duration` | `float` | Effect duration in seconds (0 = instant, -1 = infinite) |
| 0x34 | `MaxStacks` | `uint16` | Max concurrent stacks on target |
| 0x36 | `StackDurationRefreshPolicy` | `enum` | How duration refreshes on re-apply |
| 0x37 | `StackExpirationPolicy` | `enum` | What happens when a stack expires |
| 0x38 | `Modifiers` | `TArray<FNone_>` | List of attribute modifications (Dumper-opaque) |
| 0x48 | `GrantedTags` | `FGameplayTagContainer` | Tags given to the target while effect is active |
| 0x68 | `ApplicationRequirements` | `FBHGameplayTagRequirements` | Tags required on target to apply |
| 0xF0 | `OngoingRequirements` | `FBHGameplayTagRequirements` | Tags that must stay present for effect to remain |
| 0x178 | `RemovalRequirements` | `FBHGameplayTagRequirements` | Tags that trigger removal |
| 0x200 | `Tags` | `FGameplayTagContainer` | Tags identifying the effect itself |
| 0x220 | `bAllowClientPredictedApplication` | `bool` | Client-side prediction for apply |
| 0x221 | `bAllowClientPredictedModification` | `bool` | Client-side prediction for modify |

The three enum stacking/expiration policies and the opaque `Modifiers`
list are documented in `BHGameplayEffects_structs.hpp`.

### 1.2 `UBHGameplayEffectComponent` (0xCD0 bytes)

The actor component that owns + applies effects. Defined in
[`sdk/raw/BHGameplayEffects_classes.hpp`](sdk/raw/BHGameplayEffects_classes.hpp).

Key properties:

| Offset | Field | Purpose |
|---|---|---|
| 0x288 | `DefaultAttributes` | `TMap<FGameplayTag, float>` — initial attribute values |
| 0x3D8 | `AttributeReplication` | Net-replicated attribute container |
| 0x508 | `EffectContainer` | Active effects on this component |
| 0x998 | `TagSerializer_AllCounts` | Full tag-count replication state |
| 0xB18 | `TagSerializer_ReplicatedOnly` | Replicated subset of tag counts |
| 0xC98 | `NetworkPredictionWorldManager` | Points to the global prediction system |

Key functions (abbreviated signatures):

| Function | Role |
|---|---|
| `ApplyEffect(Effect, ..., CustomMagnitudes, Mode)` | Apply an effect with optional per-magnitude overrides |
| `ApplyLocalEffect(Effect, ..., CustomMagnitudes, LocalHandle)` | Client-only effect (predicted) |
| `ModifyEffectCustomMagnitude(Handle, Tag, DeltaValue)` | Modify an active effect's magnitude at runtime |
| `ModifyEffectStacks(..., Handle, Delta, Mode)` | Add/remove stacks on an existing effect |
| `RemoveEffect(Handle, Mode)` | Remove an effect |
| `FindOrAddAttribute(Attribute, InitialValue, ...)` | Attribute system entry point |
| `SetAttributeBaseValue(..., Handle, newbase)` | Server-authoritative attribute set |
| `ServerApplyEffect(request, SyncFrame)` | Server-side effect application (RPC) |
| `ServerModifyEffect(Handle, PredictionKey, Delta, SyncFrame)` | Server-side modification (RPC) |
| `UpdateGameplayTag(Tag, Delta, ...)` | Grant/revoke a tag |

**Prediction architecture:** `UBHGameplayEffectComponent` inherits from
`UBHGameplayPredictionComponent` and uses UE's
`UNetworkPredictionWorldManager` — this is a **networked-prediction**
model with client prediction + server reconciliation, not pure
server-authoritative dispatch. Open security implications in §6.

### 1.3 `UBHGameplayEffectLibrary` — Blueprint utility functions

Static blueprint functions for querying attribute values + applying
local effects:

| Function | Purpose |
|---|---|
| `GetValues(Handle, base, Current, ...)` | Read base + current value of an attribute |
| `ModifyBase(Delta, Handle, Value, ...)` | Modify base attribute |
| `SetBase(Delta, Handle, newbase)` | Set base attribute |
| `MakeLocalEffectHandle(...)` | Create a prediction handle for local effects |

### 1.4 `UBHTaggedGameplayEffects` — Data asset preset

The data-asset wrapper. Each instance holds a `TMap<GameplayTag,
FBHGameplayEffectPreset>` where the preset specifies:
- `Effect` — TSoftClassPtr to a specific `GE_*` subclass
- `Stacks` — stack count to apply
- `CustomMagnitudes` — array of magnitude overrides

## 2. The effect catalog — 338 GE_* subclasses

Grouped by filename prefix (second underscore-delimited token):

| Prefix | Count | Purpose |
|---|---:|---|
| `GE_MAGZ_*` | 60 | Magazine attachment effects (capacity, reload speed) |
| `GE_FGRP_*` | 54 | Foregrip attachment effects (recoil control, stability) |
| `GE_MUZL_*` | 47 | Muzzle attachment effects (flash, sound, dispersion) |
| `GE_SGHT_*` | 34 | Sight / scope attachment effects (ADS speed, zoom modifier) |
| `GE_Player_*` | 30 | Player-wide status effects (stimulant, bleed, stun, etc.) |
| `GE_Weapon_*` | 25 | Weapon-generic effects (AimTime, EquipSpeedMultiplier, Recoil, per-stance recoil) |
| `GE_MAG_*` | 15 | Short-prefix magazine variants |
| `GE_FGP_*` | 10 | Short-prefix foregrip variants |
| `GE_MZL_*` | 7 | Short-prefix muzzle variants |
| `GE_AK74_*` | 6 | AK74-specific effects (weapon-specific attachment chain) |
| `GE_Item_*` | 4 | Item-usage effects |
| `GE_4xElcanSpectr_*` | 4 | 4x Elcan sight effects (specific scope with sub-effects) |
| `GE_Vehicle_*` | 3 | Vehicle-interaction effects (seat occupied, driver bonus) |
| `GE_Spotting_*` | 3 | Spotting system (mark enemy, friendly mark) |
| `GE_TankHelmet_*` | 2 | Tank helmet attachment |
| `GE_Stanag_*` | 2 | STANAG magazine effects |
| `GE_RK6_*` | 2 | RK6 helmet |
| `GE_PilotHelmet_*` | 2 | Pilot helmet |
| `GE_GrantSkill_*` | 2 | Skill-unlock effects |
| `GE_6xScope_*` | 2 | 6x scope effects |

Full list of 338 is enumerable from
`ls sdk/raw/GE_*_classes.hpp`.

### 2.1 Representative example — `GE_Weapon_StanceRecoil_*`

20 effects for per-stance recoil mod (archetype × stance):

```
GE_Weapon_StanceRecoil_AR_Crouch        GE_Weapon_StanceRecoil_DMR_Prone
GE_Weapon_StanceRecoil_AR_Prone         GE_Weapon_StanceRecoil_DMR_Standing
GE_Weapon_StanceRecoil_AR_Standing      GE_Weapon_StanceRecoil_LMG_Crouch
GE_Weapon_StanceRecoil_DMR_Crouch       (...)
```

**Observation:** per-stance × per-archetype recoil is modeled as
individual GE classes rather than parameterized data on a single
effect. This is a Blueprint-friendly design (each GE is a
`BlueprintGeneratedClass`) but produces large catalog counts.

## 3. The data presets

### 3.1 `DA_CharacterEffectPresets.json`

Location: [`data/Wardogs/Content/GameMechanics/GameplayEffects/Presets/DA_CharacterEffectPresets.json`](data/Wardogs/Content/GameMechanics/GameplayEffects/Presets/DA_CharacterEffectPresets.json)

Row structure (per `UBHTaggedGameplayEffects`):

```json
{
  "Data": [
    {
      "Key": { "TagName": "GameplayCue.Door.Breach" },
      "Value": {
        "Effect": { "ObjectName": "GE_DoorBreach_C", "ObjectPath": "..." },
        "Stacks": 1,
        "CustomMagnitudes": []
      }
    }
    // ... more entries
  ]
}
```

Each tag like `GameplayCue.Door.Breach` triggers the mapped GE_*
class with the specified stacks and (optional) magnitude overrides.

### 3.2 `DA_DefaultPlayerEffects.json`

Default effects applied on player spawn. Maps initial-state tags to
baseline effects (e.g., default breathing, aim steady, movement
stamina). Same structure as `DA_CharacterEffectPresets`.

### 3.3 `DA_CharacterModifierState_StimulantEffects.json`

Stimulant / healing item effect catalog. Specific to the StimPen plugin.

Location: [`data/Wardogs/Plugins/GameFeatures/Items/StimPen/Content/Data/DA_CharacterModifierState_StimulantEffects.json`](data/Wardogs/Plugins/GameFeatures/Items/StimPen/Content/Data/DA_CharacterModifierState_StimulantEffects.json)

## 4. The attribute system

### 4.1 Attributes-as-tags design

**Divergence from vanilla GAS:** instead of `UAttributeSet` C++
subclasses with typed properties (vanilla GAS pattern), Wardogs
represents attributes as a flat **map keyed by GameplayTag**:

```cpp
TMap<FGameplayTag, float> DefaultAttributes;    // UBHGameplayEffectComponent
```

Each attribute is identified by its tag (e.g., `Attribute.Health.Max`,
`Attribute.Stamina.Current`). Values are stored in
`FBHGameplayAttributeRepContainer` (replicated).

### 4.2 Attribute access

Blueprint-exposed APIs on `UBHGameplayEffectLibrary`:

```cpp
GetValues(Handle, base, Current, ...)   // read base + current
ModifyBase(Delta, Handle, Value, ...)   // additive modification
SetBase(Delta, Handle, newbase)         // absolute set
```

### 4.3 Attribute → modifier chain

When a GE applies, its `Modifiers` list (opaque in SDK) iterates and
calls `ModifyBase` or `SetBase` on the target component's attributes.
The exact iteration order and whether multiple modifiers for the
same attribute multiply or add is a §6 open question.

## 5. End-to-end example — equipping a 6x scope

1. Player equips a weapon attachment configured with a `GE_6xScope_C` reference
2. The attachment Blueprint calls `UBHGameplayEffectComponent::ApplyEffect(GE_6xScope_C, 1, [], Mode)`
3. `ApplyEffect` creates a prediction handle, pushes to `EffectContainer`
4. The GE's `Modifiers` iterate — e.g., modifies `Attribute.Weapon.ADSZoom` from 1.0 to 6.0
5. The GE's `GrantedTags` apply — e.g., grants `Weapon.State.Scoped.Long`
6. Client renders scoped view based on `GrantedTags`
7. On unequip, the handle is removed, modifiers roll back, tags revoked

Same mechanism applies to:
- Weapon attachments (magazine, foregrip, muzzle, sight)
- Player status effects (stim pen, bleed, exhaustion)
- Vehicle driver bonuses
- Spotting marks

## 6. Still Not Pulled / Open Questions

### 6.1 Modifier array internal structure (`SDK`-gated)
`UBHGameplayEffect::Modifiers` is `TArray<FNone_>` — Dumper-7 could
not resolve the per-modifier struct type. Needs:
- Deeper SDK regeneration with more context, OR
- Static IDA RE of the modifier iterator in `ApplyEffect`

### 6.2 Stacking math (`IDA`-fillable)
When `MaxStacks > 1` and the same effect applies multiple times, the
math on `Modifiers` output is not documented. Candidates:
- Linear (stack 2 = 2× modifier)
- Multiplicative (stack 2 = modifier²)
- Capped by `StackDurationRefreshPolicy` enum

### 6.3 Attribute iteration order (`IDA`-fillable)
When multiple GEs modify the same attribute, the resolution order
needs IDA RE of the `AttributeReplication` consumer.

### 6.4 Client-prediction authority model (`SECURITY`-flagged)
`bAllowClientPredictedApplication` and
`bAllowClientPredictedModification` toggles exist on each GE. This
means:
- Some effects are client-predicted and server-reconciled
- Some effects are server-authoritative only

The threat-model question: does the reconciliation always roll back
illegitimate predictions, or does the client's optimistic state
persist until a server mismatch is detected?

**Routing:** this is a server-authority question that goes through
[`SECURITY.md`](SECURITY.md), not public write-up.

### 6.5 Full GE_* catalog values (`EXPORT`-fillable)
Only the structural signatures of the 338 GE_* subclasses are
captured. The actual configured values (duration, stack count,
modifier amounts, granted tags) require per-asset extraction. Each
GE_* has an associated `.uasset` that CUE4Parse can parse — not yet
in current dump.

### 6.6 Prediction conflict resolution (`IDA`-fillable)
`UNetworkPredictionWorldManager` handles rollback. The specific
rollback mechanism (snapshot + replay vs forward-correction) is
documented at UE level but Wardogs-specific extensions may apply.

## 7. Cross-references

### SDK files cited
- [`sdk/raw/BHGameplayEffects_classes.hpp`](sdk/raw/BHGameplayEffects_classes.hpp) — `UBHGameplayEffect`, `UBHGameplayEffectComponent`, `UBHGameplayEffectLibrary`, `UBHTaggedGameplayEffects`
- [`sdk/raw/BHGameplayEffects_structs.hpp`](sdk/raw/BHGameplayEffects_structs.hpp) — effect stacking enums, `FBHGameplayEffectPreset`, `FBHGameplayEffectHandle`, `FBHAttributeHandle`
- [`sdk/raw/BHGameplayPrediction_classes.hpp`](sdk/raw/BHGameplayPrediction_classes.hpp) — the prediction component base
- `sdk/raw/GE_*_classes.hpp` (338 files) — individual effect subclasses

### Data files cited
- [`data/Wardogs/Content/GameMechanics/GameplayEffects/Presets/DA_CharacterEffectPresets.json`](data/Wardogs/Content/GameMechanics/GameplayEffects/Presets/DA_CharacterEffectPresets.json)
- [`data/Wardogs/Content/GameMechanics/GameplayEffects/Presets/DA_DefaultPlayerEffects.json`](data/Wardogs/Content/GameMechanics/GameplayEffects/Presets/DA_DefaultPlayerEffects.json)
- [`data/Wardogs/Plugins/GameFeatures/Items/StimPen/Content/Data/DA_CharacterModifierState_StimulantEffects.json`](data/Wardogs/Plugins/GameFeatures/Items/StimPen/Content/Data/DA_CharacterModifierState_StimulantEffects.json)

### Related reference docs
- [`Wardogs_DamagePipeline_v1.md`](Wardogs_DamagePipeline_v1.md) — infantry damage uses GAS modifier chain
- [`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md) — vehicle damage uses per-vehicle rules (not GAS)
- [`Wardogs_GameMechanics_v2.md`](Wardogs_GameMechanics_v2.md) — broader mechanics context
- [`Wardogs_GameplayTags_v1.md`](Wardogs_GameplayTags_v1.md) — tag catalog

## Change log

| Date | Change |
|---|---|
| 2026-10-16 | v1 — First complete trace of BH-GAS architecture. 338 GE_* classes catalogued by prefix. Attribute system documented as `TMap<FGameplayTag, float>` divergence from vanilla GAS. Prediction + server-reconciliation security question flagged (§6.4). |
