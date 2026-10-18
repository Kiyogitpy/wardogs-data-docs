# GObjects damage analysis — 2026-10-17

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Analysis of the `GObjects-Dump.txt` + `GObjects-Dump-WithProperties.txt`
runtime object dumps for damage-pipeline-relevant classes. Complements the
triage AI's binary-trace work by establishing the Blueprint local-variable
names and runtime struct layouts.

**Scope:** read-only extraction from pre-recorded GObjects dumps. No
code execution. No decompilation (the triage AI handles that
side).

**Build identity confirmed:** `5.7.4-516586+++Wardogs+Live-Wardogs`,
148,028 total UObject instances. Matches the committed idmap and the
restored exe.

---

## 1. Damage class catalog (runtime addresses)

Confirmed native/Blueprint classes in the GObjects runtime dump:

| GObjects index | Runtime addr | Kind | Full name |
|---|---|---|---|
| `0x16FF` | `0x7FF40F7B41B8` | Class | `WDGame.WDCustomDamageModificationOperation` |
| `0x1700` | `0x7FF40F7B43C0` | Class | `WDGame.WDDamageModificationOperation_PlayerArmorDurability` |
| `0x16FE` | `0x7FF40F7B3FB0` | Class | `WDGame.WDGlobalDamageSystem` |
| `0x180D` | `0x7FF40F7D6628` | Class | `WDGame.WDDamageSubsystem` |
| `0x1704` | `0x7FF40F7B4BE0` | Class | `WDGame.WDDamageHitLocationsDataAsset` |
| `0xD87` | `0x7FF40F68A468` | Class | `BHGameplayEffects.BHGameplayEffect` |
| `0xD88` | `0x7FF40F68A670` | Class | `BHGameplayEffects.BHGameplayEffectComponent` |
| `0xDA0` | `0x7FF40F68CD08` | Class | `BHHitValidation.BHHitValidationWorldSubsystem` |
| `0x5AF0` | `0x7FF40FD8DD78` | ScriptStruct | `WDGame.WDDamageableEntityTableRow` |
| `0x5AF9` | `0x7FF40FD8E438` | ScriptStruct | `WDGame.WDArchetypeCaliberDamageModifierData` |
| `0x5AF8` | `0x7FF40FD8E378` | ScriptStruct | `WDGame.WDBoneDamageModifierData` |
| `0x39A0` | `0x7FF40FC117C8` | ScriptStruct | `WDGame.WDModifyDamageData` |
| `0x3979` | `0x7FF40FC0F708` | ScriptStruct | `WDGame.WDDamageEntityData` |
| `0x39E3` | `0x7FF40FC15058` | ScriptStruct | `WDGame.WDDamageEventData` |

## 2. Hash-name resolutions

### 2.1 `_aaabapbnbhiopifeenjml`

**Context:** property on `WDArchetypeCaliberDamageModifierData` (ScriptStruct `0x5AF9`).

**Runtime type:** `MapProperty` at offset `0x10`.

**Interpretation:** this is the caliber→multiplier lookup map on each
row of the ArchetypeCaliberModifiers data table. The map is keyed by
caliber `FGameplayTag` and values are `float` multipliers. (See
[`data/.../DT_InfantryData_ArchetypeCaliberModifiers.json`](../data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json)
rows.)

The sibling struct `WDBoneDamageModifierData` names this same map
field symbolically as `HitLocations` at `0x10` — so the hashed field is
almost certainly the caliber-equivalent of `HitLocations` with the
analogous semantics. Reasonable native rename:
`_aaabapbnbhiopifeenjml` → `CaliberValues` (or `Multipliers`, or similar).

### 2.2 `_aaabddjaiakieibfbondk`

**Context:** second parameter on every `GetModificationAmount` function
in all 4 B_* modifier Blueprints (and the C++ base
`UWDCustomDamageModificationOperation`).

**Runtime type:** `FloatProperty` at offset `0xC8` of the function's
parameter block.

**Interpretation:** given the triage AI's binary-trace finding that the
evaluator does `current += amount × 0.01 × starting/current`, this
float parameter is the **current damage amount being modified**
(the running total). The function signature in C++ terms:

```cpp
float GetModificationAmount(const FWDModifyDamageData& Data, float CurrentDamage) const;
```

Reasonable rename: `_aaabddjaiakieibfbondk` → `CurrentDamage` or
`StartingDamage`.

## 3. Runtime struct layouts (verified against SDK)

All struct property offsets from GObjects runtime dump match the SDK
earlier committed. This cross-verifies the SDK against the live
object system.

### 3.1 `FWDModifyDamageData` (ScriptStruct `0x39A0`)

| Offset | Property | Type |
|---:|---|---|
| `0x00` | `Amount` | FloatProperty |
| `0x08` | `InstigatorEventData` | StructProperty (`FWDDamageEventEntityData`) |
| `0x18` | `InstigatorEntityData` | StructProperty (`FWDDamageEntityData`) |
| `0x48` | `TargetEventData` | StructProperty |
| `0x58` | `TargetEntityData` | StructProperty |
| `0x88` | `SourceEntityData` | StructProperty |
| `0xB8` | `Alignment` | EnumProperty (`EWDDamageAlignment`) |
| `0xBC` | `HitLocation` | StructProperty (`FGameplayTag`) |

Matches [`sdk/raw/WDGame_structs.hpp`](../sdk/raw/WDGame_structs.hpp) line 4646.

### 3.2 `WDDamageSubsystem` (Class `0x180D`)

| Offset | Property | Type |
|---:|---|---|
| `0x30` | `OnDamageModified` | MulticastInlineDelegateProperty |
| `0x40` | `DamageSystems` | ArrayProperty |
| `0x50` | `DamageTypes` | MapProperty |
| `0xA0` | `LoadedHitLocationClasses` | ArrayProperty |
| `0xB0` | `LoadedHitLocationAssets` | ArrayProperty |
| `0xC0` | `ClassToHitLocations` | MapProperty |
| `0x110` | `ClassToHitLocations_Loaded` | MapProperty |

`OnDamageModified` at `0x30` is a multicast delegate on the subsystem;
which systems bind to it is not established by the dump.

### 3.3 `WDGlobalDamageSystem` (Class `0x16FE`)

| Offset | Property | Type |
|---:|---|---|
| `0x30` | `DamageRegistryName` | NameProperty |
| `0x38` | `DamageCategoriesDataAsset` | ObjectProperty |
| `0x40` | `RootDamageTag` | StructProperty |

The `DamageCategoriesDataAsset` reference confirms
[`data/.../DA_GlobalDamage_Categories.json`](../data/Wardogs/Content/GameMechanics/DamageSystem/DA_GlobalDamage_Categories.json)
is the authoritative category list.

## 4. Blueprint modifier internals (local-variable names)

Each of the 4 custom-modifier Blueprints exposes its function's local
variables via the GObjects dump. The variable names + types reveal the
algorithm shape per modifier **without the binary decompilation step**.

### 4.1 `B_ArchetypeCaliberModifiers_C.GetModificationAmount` (Function `0x16CDD`)

Property field: `DataTable` at `0x28` (ObjectProperty, holds reference to
[`DT_InfantryData_ArchetypeCaliberModifiers`](../data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json)).

Function locals (parameter block):

| Offset | Name | Type | Notes |
|---:|---|---|---|
| `0x00` | `ModifyDamageData` | StructProperty | input `FWDModifyDamageData` |
| `0xC8` | `_aaabddjaiakieibfbondk` | FloatProperty | input current damage (see §2.2) |
| `0xCC` | `ReturnValue` | FloatProperty | output |
| `0xD0` | `WeaponClassBoneModifier` | FloatProperty | **lookup result from DT, keyed by weapon archetype** |
| `0xD4` | `UniversalBoneModifier` | FloatProperty | **fallback lookup from Universal row** |
| `0xD8` | `HitLocation` | StructProperty | pulled from input |
| `0xE0-0xFF` | loop/temp variables | int/bool | iteration state |
| `0x100` | `CallFunc_IsValid_ReturnValue` | BoolProperty | validity check result |
| `0x104` | `CallFunc_RequestDirectParent_ReturnValue` | StructProperty | **tag parent lookup** |
| `0x110` | `CallFunc_BreakGameplayTagContainer_GameplayTags` | ArrayProperty | tag container decomposition |

**Algorithm shape (inferred):**
1. Break input tag container → array of tags
2. For each tag, request direct parent (walk the tag hierarchy)
3. Look up `WeaponClassBoneModifier` from DataTable keyed by weapon class
4. Look up `UniversalBoneModifier` as fallback
5. Multiply and subtract to combine, return result

### 4.2 `B_BoneDamageModifiers_C.GetModificationAmount` (Function `0x16CDA`)

Same `DataTable` property pattern. Function locals adds:

| Offset | Name | Type |
|---:|---|---|
| `0xE6` | `CallFunc_MatchesTag_ReturnValue` | BoolProperty |
| `0xE8`, `0xF0` | 2× `CallFunc_Multiply_DoubleDouble_ReturnValue` | DoubleProperty |
| `0x100` | `CallFunc_Subtract_DoubleDouble_ReturnValue` | DoubleProperty |

**Algorithm shape:** iterate datatable rows, do tag matching
(`MatchesTag`), apply two multiplications (likely base × class
multiplier × universal multiplier), subtract 1 (to produce the "delta"
format expected by the evaluator — matches the triage AI's `delta +=
amount × 0.01 × starting/current` formula).

### 4.3 `B_AmmoTypeEffectiveness_C.GetModificationAmount` (Function `0x16CD3`)

**No DataTable property on the class itself.** The function pulls data
from the target's armor state at runtime. Function locals:

| Offset | Name | Type | Notes |
|---:|---|---|---|
| `0x00` | `ModifyDamageData` | StructProperty | input |
| `0xC8` | `_aaabddjaiakieibfbondk` | FloatProperty | input current damage |
| `0xCC` | `ReturnValue` | FloatProperty | output |
| `0xD0` | `BaseDamage` | DoubleProperty | base pulled from projectile |
| `0xD8` | `PenetrationEffectivenessMultiplier` | DoubleProperty | penetration factor |
| `0xE0` | `ProjectileId` | StructProperty (FGameplayTag) | which projectile hit |
| `0xE8` | `AmmoModifierTag` | StructProperty (FGameplayTag) | ammo type (AP, HP, Tracer) |
| `0xF0` | `Current Damage Reduction` | FloatProperty | **live armor reduction state** |
| `0xF8` | `CurrentDurability` | DoubleProperty | **remaining armor durability** |
| `0x100` | `ArmorId` | StructProperty | which armor piece |
| `0x108` | `HitArmorType` | StructProperty | armor class hit |
| `0x118` | `hitactor` | ObjectProperty | the hit actor itself |
| `0x120` | `EffectiveReduction` | DoubleProperty | final computed reduction |
| `0x128` | `Ammo Modifier Type` | StructProperty | |
| `0x130` | `Source Entity Data Context` | StructProperty | |
| `0x150` | `AmmoArmorScalar` | DoubleProperty | **ammo × armor coupling scalar** |

**Key finding — this is NOT just a caliber lookup.** The ammo type
effectiveness blueprint factors in:
- Current armor durability (`CurrentDurability`)
- Current damage reduction state (`Current Damage Reduction`)
- Live armor-piece ID (`ArmorId`)
- Hit-armor-type tag (`HitArmorType`)
- Projectile-specific `AmmoArmorScalar`

**Open question that this surfaces:** ammo-type effectiveness is a
**stateful, armor-dependent calculation**, not a stateless lookup.
This means the modifier chain's behavior depends on the target's
current armor state. The data table alone cannot predict the output
— the target's live state must be read.

Expands pipeline doc §7.4 (PlayerArmorDurability behaviour) — the
ammo-type modifier and the armor-durability modifier are coupled.

### 4.4 `B_VehicleSeatDamageReduction_C.GetModificationAmount` (Function `0x16CD7`)

Function locals:

| Offset | Name | Type |
|---:|---|---|
| `0xD0` | `CurrentSeatSetUp` | StructProperty |
| `0x4A8` | `Current Projectile Arms Tag` | StructProperty |
| `0x4B0` | `DataTable` | ObjectProperty |
| `0x4B8` | `PlayerCharacter` | ObjectProperty |
| `0x4E0` | `K2Node_DynamicCast_AsWDMover_Player_Character` | ObjectProperty |

**Algorithm shape:** cast hit actor to `WDMover_Player_Character` (if
possible), look up current seat setup, resolve current projectile's
"arms tag" (penetration class), look up vehicle-seat-reduction table.

Note the LARGE offset gap (0xD0 → 0x4A8) — `CurrentSeatSetUp` is a
substantial struct (~0x3D8 bytes).

## 5. UFunction entry points in GObjects

Each custom modifier Blueprint has a GObjects-registered Function
entry with a runtime address. These are the targets for IDA Function
xref:

| Blueprint | Function obj | Runtime addr |
|---|---|---|
| `B_ArchetypeCaliberModifiers_C` | `GetModificationAmount` | `0x2087C74FD00` |
| `B_BoneDamageModifiers_C` | `GetModificationAmount` | `0x2087C74FE00` |
| `B_AmmoTypeEffectiveness_C` | `GetModificationAmount` | `0x2087C74C700` |
| `B_VehicleSeatDamageReduction_C` | `GetModificationAmount` | `0x2087C74FF00` |

These are runtime UFunction object addresses (not VAs in the exe).
IDA session would xref the UFunction::ProcessEvent calls that invoke
these.

## 6. Caveats

- Addresses in this doc are **runtime UObject addresses** captured
  during a specific game session. They identify object identity, not
  code location — code locations are the RVAs in the idmap and the
  decompiled addresses in the triage AI's trace.
- Property offsets apply to the specific build captured in the dump
  (CL-516586). A patch may shift offsets.
- No security-relevant findings claimed here; any such question routes
  through [`SECURITY.md`](../SECURITY.md).
- Blueprint-local-variable names are the **author's own names at
  Blueprint compile time**. They are hints at algorithm structure,
  not binding specifications of semantics.

## 7. Cross-references

- [`Wardogs_DamagePipeline_v2.md`](../pipelines/Wardogs_DamagePipeline_v2.md) — damage pipeline (being audited by triage AI)
- [`docs/RESTORED_EXE_VALIDATION.md`](RESTORED_EXE_VALIDATION.md) — exe + idmap byte-level match
- [`docs/evidence/damage.md`](evidence/damage.md) — the IDA trace brief, the failed first pass and the restored-exe trace, merged, with a status for every cited RVA
- [`sdk/raw/`](../sdk/raw/) — Dumper-7 CppSDK (static view)
- [`mappings/`](../mappings/) — IDA + usmap mappings
- GObjects dumps (local-only, 16MB + 25MB — not committed due to size): `wardogs_analysis/GObjects-Dump*.txt`
