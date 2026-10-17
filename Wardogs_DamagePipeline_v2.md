---
title: "Damage Pipeline"
parent: "Pipelines"
nav_order: 1
---

# Wardogs — Damage Pipeline

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

How a damage amount is modified between a hit and the number handed back
to the game: which rules are selected, in what order, and with what
arithmetic. This is the single reference for the infantry damage
pipeline. It folds in the native trace, the GObjects Blueprint analysis
and the restored-executable validation; those reports remain as evidence
(§10).

Build: `++Wardogs+Live-CL-516586` · Engine: UE 5.7 · GAS fork: "BH"
(Embark's internal GAS variant) · Native addresses are file RVAs in the
restored executable, SHA-256 `a5c3db10…2b4f0cc37` (§10).

Every claim carries one of these labels:

| Label | Meaning |
|---|---|
| **Data** | Read from the Season-02 cooked export under `data/` |
| **Native** | Read from native code in the restored executable; RVA cited |
| **Bytecode** | Read from a cooked Blueprint's Kismet bytecode |
| **Derived** | Follows from Native and Data facts by arithmetic alone |
| **Open** | Not yet established; §9 says what closes it |

---

## At a glance

| Stage | Status | Section |
|---|---|---|
| Entry: reflected `ModifyDamage` → subsystem → first active damage system | **Native** | §1 |
| Callers, and where the result goes: Unreal damage event → `TakeDamage` | **Native** | §1.1 |
| Rule data: 146 infantry entries, 5 custom operation classes | **Data** | §3 |
| Entry selection: skip rule and requirement matching | **Native** | §4 |
| Order within a target-tag group: category index, ascending, no tie-breaker | **Native** | §5 |
| Order between groups: target tag first, then each parent tag | **Native** | §5 |
| Operation arithmetic, custom-delta contract, final clamp | **Native** | §6 |
| Four Blueprint operations: bone, caliber, ammo vs armor, vehicle seat | **Bytecode** | §7.1–7.4 |
| `PlayerArmorDurability`: `−(armor reduction %) × C` from the equipped item | **Native** + **Data** | §7.5 |
| Health write inside `TakeDamage` overrides; network authority | **Open** | §9 |

The short version: every selected rule, custom or not, multiplies the
running damage by a factor, and the total is clamped at zero once at the
end. Non-custom rules give `1 + Amount/100`. The bone operation gives
`Universal × weapon row` for the hit location. Armor gives
`1 − reduction% × ammo scalar / 100`. Because everything multiplies,
the order of evaluation does not change the result. A worked example is
in §7.6.

## 1. Call path

**Native.** The reflected thunk and the methods it reaches:

| Step | Role | RVA |
|---|---|---|
| 1 | Reflected `exec_ModifyDamage` (registration name at `0xB432298`, pair at `0xB434AD0`) | `0x6F08A60` |
| 2 | Native `UWDDamageSubsystem::ModifyDamage`: converts the event and calls the selected system's virtual evaluator | `0x6F02EC0` |
| 3 | Select the first valid damage system in `DamageSystems` whose active predicate passes | `0x6EFFD40` |
| 4 | `UWDGlobalDamageSystem` evaluator (vtable `0xB3217D0`, slot `0x2B0`) | `0x6BB6FB0` |
| 5 | Collection: registry/tag traversal and per-group sorting (same vtable, slot `0x2B8`) | `0x6BB6A60` |
| 6 | Match a registry row's entries and append the selected ones (callback thunk `0x6BB6A50`) | `0x6BB6730` |
| 7 | Requirement-container match | `0x6BB5D20` |
| 8 | Category priority lookup | `0x6BB8970` |
| 9 | Per-group sort / fallback sort | `0x6BB61A0` / `0x6BB5F40` |
| 10 | Custom operation dispatch adapter | `0x6BB7900` |
| 11 | Reflected `exec_GetModificationAmount` (pair at `0xB322038`) | `0x6BB7B30` |

`ModifyDamage` takes `FWDDamageEventData&` and a bool, and returns a
float. On the inspected branch the bool bypasses the evaluator; its
gameplay meaning is **Open**. Which system an actual event selects is
also **Open**: step 3 reads the base active field and returns the first
match.

### 1.1 Callers and where the result goes

**Native.** `ModifyDamage` (`0x6F02EC0`) has 17 direct call sites in 16
functions. The identifiable ones:

| Caller | RVA | Bool passed |
|---|---|---|
| Reflected `exec_ModifyDamage` (Blueprint-callable) | `0x6F08A60` | From the caller |
| Reflected `SimpleDamageActorWithInstigatorController` | `0x6F09210` | 0 |
| `UWDVehicleOperatorComponent` virtuals (slots 160, 161) | `0x7692B60`, `0x768ED20` | 0 |
| `AWDMoverCharacter` / `AWDMoverPlayerCharacter` virtual (slot 417 / 422) | `0x6E6BD90` | 1 |

The rest are unnamed functions (`0x6E72D90`, `0x6F042A0`, `0x76740F0`,
`0x6F06540`, `0x6B53000`, `0x6F06EB0`, `0x76F5AE0`, `0x6CA8730`,
`0x6B725B0` ×2, `0x6F03F60`, `0x6F08CDC`). `0x6E72D90` and `0x76F5AE0`
also pass 1. Each caller builds the event (`0x6BB4D30`) itself, so `S` is
whatever amount that caller supplies.

Most callers then hand the result to the same two steps:

1. **Build an Unreal damage event** (`0x6EF944F`): damage = the modified
   amount; the hit result is copied in; shot direction = the normalised
   trace; the `UDamageType` class is looked up by damage-type tag in the
   subsystem's `DamageTypes` map, with the base class as fallback.
   Callers pass `Meta.Damage.DamageType.Impact` or
   `Meta.Damage.DamageType.Explosive`.
2. **Apply it** (`0x6EF9840`): reads the world's `WDGameStateSession` and,
   when the session carries a particular mode tag, filters targets through
   a class list in `WDGameSettings`. Targets implementing `WDDamageable`
   take a dedicated path (`0x6C2A5F0`). Every other actor gets
   `TakeDamage(damage, event, instigator, causer)`, called through
   vtable `+0x6B0`.

So this pipeline ends where Unreal's standard damage call begins. The
health write happens inside the targets' `TakeDamage` overrides and the
effects pipeline, not here.

## 2. The data passed to custom operations

`FWDModifyDamageData`, declared in
[`sdk/raw/WDGame_structs.hpp`](sdk/raw/WDGame_structs.hpp#L4646). The
GObjects dump's runtime property offsets match the SDK field for field.

```cpp
struct FWDModifyDamageData final {
    float Amount;                                  // 0x00 — starting amount S
    uint8 Pad_4[0x4];
    FWDDamageEventEntityData InstigatorEventData;  // 0x08
    FWDDamageEntityData      InstigatorEntityData; // 0x18 — 0x30 bytes
    FWDDamageEventEntityData TargetEventData;      // 0x48
    FWDDamageEntityData      TargetEntityData;     // 0x58
    FWDDamageEntityData      SourceEntityData;     // 0x88
    EWDDamageAlignment       Alignment;            // 0xB8 — None / Neutral / Hostile / Friendly
    uint8 Pad_B9[0x3];
    FGameplayTag             HitLocation;          // 0xBC — e.g. Meta.Damage.HitLocation.Infantry.Head
    uint8 Pad_C4[0x4];                             // size 0xC8
};
```

The operation interface,
[`UWDCustomDamageModificationOperation`](sdk/raw/WDGame_classes.hpp#L36507):

```cpp
float GetModificationAmount(const FWDModifyDamageData& ModifyDamageData,
                            float CurrentDamage) const;  // SDK name: _aaabddjaiakieibfbondk
```

**Native.** The adapter at `0x6BB7900` receives the class default object,
the original struct and the running amount `C` (`xmm2`, `0x6BB72DE`).
For a native override it calls vtable slot 86 (`+0x2B0`) directly. For a
Blueprint it fills the function's parameter block (struct copy at `0x00`,
`C` at `0xC8`, return at `0xCC`) and calls `ProcessEvent`.
`ModifyDamageData.Amount` is therefore always `S`. The hashed second
parameter is the running damage, not the starting damage.

Nothing from the rule entry reaches the operation: the receiver is the
shared default object and the parameters are the event and `C`. A custom
operation cannot read its entry's literal `Amount` or `Operation`, and
the evaluator ignores both (§6). The `-75` and `-50` literals on custom
entries in §3 have no effect on the result.

## 3. Rule tables

**Data.** [`DT_GlobalDamage_InfantryData`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json),
row `Meta.Damage.Infantry`, row struct `FWDDamageableEntityTableRow`.
Its `DamageModificationEntries` array has **146 entries**:

| Entry kind | Count |
|---|---:|
| Non-custom `Percentage_Ongoing` | 74 (29 of them with amount 0) |
| Non-custom `None`, empty requirements, amount 0 | 60 |
| Custom operation (serialized as `Percentage_Ongoing`) | 12 |

No infantry entry uses `Percentage_Starting` or `Add`. All 146 have
serialized `PriorityIndex = -1`, which the collector overwrites (§5).
Non-zero non-custom amounts range from -70 to +500.

Each entry is a `FWDDamageModificationEntry` (184 bytes, `0xB8`, in the
native loop):

```text
InstigatorRequirements, TargetRequirements, SourceRequirements  — tag containers
AlignmentRequired                                               — EWDDamageAlignment
PossibleHitLocations                                            — tag container
OutModification:
    bUseCustomOperation, Operation, Amount, CustomOperationClass,
    PriorityCategory, PriorityIndex, DebugTargetTag
```

Category use among the 86 non-`None` entries: Weapon 22, AmmoModifier 18,
Calibre 17, PenetrationEffectiveness 17, Tracer 5, Bone 3, Friendly 2,
Penetration 2. CaliberEffectiveness, Armor, Melee and Ricochet are
defined (§5) but unused by this row.

### 3.1 The custom entries

Zero-based indexes. Blueprint classes live under
`/Game/GameMechanics/DamageSystem/ConditionalDamageFunctions/`.

| Entries | Class | Category | Target requires | Source requires | Hit location |
|---|---|---|---|---|---|
| 5 | `B_BoneDamageModifiers_C` | Bone | — | `Meta.Damage.Bullet` | `…HitLocation.Infantry` |
| 7 | `B_BoneDamageModifiers_C` | Bone | — | `…Kinetic.Impact.ExplosiveBlunt` | `…HitLocation.Infantry` |
| 10 | `B_BoneDamageModifiers_C` | Bone | — | `Meta.Damage.Cannon` | `…HitLocation.Infantry` |
| 6 | `B_ArchetypeCaliberModifiers_C` | Calibre | — | `Meta.Damage.Bullet` | `…HitLocation.Infantry` |
| 138, 139 | `B_AmmoTypeEffectiveness_C` | PenetrationEffectiveness | `Meta.Damage.Armor` | Bullet; Cannon | `…HitLocation.Infantry` |
| 140, 141 | `B_AmmoTypeEffectiveness_C` | PenetrationEffectiveness | `Meta.Damage.Helmet` | Bullet; Cannon | `…HitLocation.Infantry` |
| 142, 143 | `WDDamageModificationOperation_PlayerArmorDurability` | PenetrationEffectiveness | Helmet; Armor | `…ExplosiveBlunt` | `…HitLocation.Infantry` |
| 144 | `WDDamageModificationOperation_PlayerArmorDurability` | Penetration | `Meta.Damage.Armor` | `…DamageType.Melee` | — |
| 145 | `B_VehicleSeatDamageReduction_C` | Penetration | — | `Meta.Damage.Bullet` | — |

### 3.2 Companion tables

| Table | Row struct | Contents |
|---|---|---|
| [`DT_GlobalDamage_VehicleData`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_VehicleData.json) | `FWDDamageableEntityTableRow` | Vehicle rules; see [VehicleDamagePipeline](Wardogs_VehicleDamagePipeline_v1.md) |
| [`DT_GlobalDamage_ArmorData`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_ArmorData.json) | `FWDDamageableEntityTableRow` | Four armor/helmet rule rows |
| [`DA_GlobalDamage_Categories`](data/Wardogs/Content/GameMechanics/DamageSystem/DA_GlobalDamage_Categories.json) | DataAsset | The 12 ordered category tags (§5) |
| [`DA_GlobalDamage_HitLocations_Player`](data/Wardogs/Content/GameMechanics/DamageSystem/HitLocationDataAssets/DA_GlobalDamage_HitLocations_Player.json) | DataAsset | Hit-location tags and bone mapping |
| [`DT_AmmoModifiers`](data/Wardogs/Content/GameMechanics/DamageSystem/DT_AmmoModifiers.json) | `FWDAmmoModifierTableRow` | Five ammo-tag → data-asset rows |

## 4. Entry selection

**Native** (`0x6BB6A60`, `0x6BB6730`, `0x6BB5D20`). The collector runs
only when the event's instigator, target and source tags are all set;
otherwise nothing is selected and `S` is returned unchanged. It then
builds three containers to match against:

- instigator context tags plus the instigator tag;
- target context tags only (the target's own tag drives the walk in §5,
  not matching);
- source context tags plus the source tag.

For each registry row it reaches it scans the whole entry array and keeps
every entry that passes, not just the first.

1. **Skip:** an entry is dropped when all four requirement arrays are
   empty *and* its literal amount is 0, regardless of custom flag or
   operation. This removes the 60 empty `None` entries. A zero-amount
   entry that has requirements is not skipped by this test.
2. **Alignment:** required alignment `None` (0) matches anything;
   otherwise it must equal the event's alignment.
3. **Tag requirements:** every tag in each instigator, target and source
   requirement container must appear in the event's matching container,
   either explicitly or as a parent tag. Empty containers pass.
4. **Hit location:** an empty container passes; a populated one needs at
   least one tag present in the hit tag's explicit or parent tags.
5. **Record:** the modification is copied into its target-tag group with
   `PriorityIndex` replaced by the category index (§5); the source entry
   index is kept separately.

## 5. Ordering

**Native** (`0x6BB8970`, `0x6BB61A0`). The category lookup returns the
zero-based index of the first exact match in
`DA_GlobalDamage_Categories.DamageCategories`, or -1 when absent. Each
target-tag group is then sorted by that signed index, ascending:

| Index | Category | Index | Category |
|---:|---|---:|---|
| 0 | Calibre | 6 | Weapon |
| 1 | AmmoModifier | 7 | Armor |
| 2 | CaliberEffectiveness | 8 | Melee |
| 3 | Bone | 9 | Ricochet |
| 4 | PenetrationEffectiveness | 10 | Penetration |
| 5 | Tracer | 11 | Friendly |

A missing category (-1) sorts before index 0.

> **Ordering caveat — no tie-breaker.** The sort swaps on the category
> index alone, with no secondary key. Entries in the same category keep
> no guaranteed order, so source array order does not decide ties.

Among the custom operations, two pairs share a category: ammo
effectiveness (138–141) and armor durability (142–143) are both
PenetrationEffectiveness, and armor durability (144) and seat reduction
(145) are both Penetration. Their source requirements differ, so a single
event matches both members of a pair only if its source container carries
both tags.

**Groups and their order** (`0x6BB6A60`, `0x6BB6FB0`). Groups are levels
of the target's tag hierarchy:

1. Start at the event's target tag.
2. Look that tag up in the damage data registry (`DamageRegistryName`).
   If a `FWDDamageableEntityTableRow` exists, match its entries (§4) and
   file the selected ones under that tag. A group is created when its
   first entry is selected.
3. Move to the tag's direct parent and repeat. Stop on reaching
   `RootDamageTag` or when there is no parent.

The evaluator builds a fresh group map for every evaluation and walks it
in slot order, which for a freshly built Unreal map is insertion order.
Groups are therefore evaluated **most specific tag first, then each
parent**, and each group's sorted array runs to completion before the
next. **This is not one global sort across groups.** A target tag with
only one registry row along its chain, such as `Meta.Damage.Infantry`,
gives a single group.

**Derived — when order matters at all.** Every non-custom infantry entry
is `Percentage_Ongoing` or skipped, so each one multiplies `C` by
`1 + Amount/100` (§6), and all five custom operations return a fixed
fraction of `C` (§7). Multiplication commutes, so neither the missing
tie-breaker nor the group order changes an infantry result, apart from
single-precision rounding. The tie-breaker caveat still matters for any
future operation whose delta is not proportional to `C`, and for tables
that use `Add` or `Percentage_Starting`.

## 6. Arithmetic

**Native** (`0x6BB6FB0`). Let `S = ModifyDamageData.Amount` at entry and
start with `C = S`. For each selected modification, in the order of §5:

| Operation | Delta | Update |
|---|---|---|
| Non-custom `None` (0) or unrecognized | — | `C` unchanged |
| Non-custom `Percentage_Starting` (1) | `(Amount * 0.01f) * S` | `C += delta` |
| Non-custom `Percentage_Ongoing` (2) | `(Amount * 0.01f) * C` | `C += delta` |
| Non-custom `Add` (3) | `Amount` | `C += delta` |
| Custom | `GetModificationAmount(originalData, C)` | `C += delta` |

- Custom entries skip the literal enum and amount entirely. The evaluator
  resolves the class default object and dispatches to it; an invalid or
  unavailable class is skipped.
- After **all** groups, the non-empty path clamps once: `C = max(C, 0)`
  (`0x6BB73E7`). With nothing selected, `S` is returned unclamped.
- A non-custom delta is applied first and only then compared with about
  `1e-8` to decide whether it is recorded in the event's result list. The
  threshold never suppresses arithmetic.
- All arithmetic is single-precision float.

Instruction anchors: `0x6BB72DE` current amount into the adapter,
`0x6BB72F8` custom return stored, `0x6BB72FD` `addss` custom delta,
`0x6BB7306` enum switch, `0x6BB7324`/`0x6BB7329` ongoing scale,
`0x6BB732F`/`0x6BB7334` starting scale, `0x6BB733C` `addss` delta,
`0x6BB73E7` `maxss` clamp.

**Derived.** A selected ongoing entry with amount `a` contributes a factor
of `1 + a/100`. For example, -25 gives ×0.75, -50 gives ×0.5, +100 gives
×2, and 0 leaves `C` unchanged. Entry 8 (Friendly alignment, bullet
source, infantry hit location, -50) therefore halves the running amount
of every friendly bullet hit it matches. What the other selected entries
do to that same hit is a separate question.

## 7. Custom operations

Four of the five classes are Blueprints. Their logic is Kismet bytecode
in the cooked `B_*.uasset` files under
`/Game/GameMechanics/DamageSystem/ConditionalDamageFunctions/`, read
statically from the game's paks with CUE4Parse and the 5.7.4 usmap
(**Bytecode** below). Each class has exactly one function,
`GetModificationAmount`. Its cooked second-parameter name is
`CurrentDamageAmount`, which is `C`. **None of the four reads
`ModifyDamageData.Amount` (`S`).**

All five operations return a fixed fraction of `C`, so each one is a
factor on the running amount:

| Operation | Factor on `C` | Section |
|---|---|---|
| Bone | `U × W` | §7.1 |
| Archetype/caliber | `W` | §7.2 |
| Ammo type vs armor | `1 − DPR × AAS / 100` | §7.3 |
| Vehicle seat | `1 + pct / 100` | §7.4 |
| Armor durability | `1 − R / 100` | §7.5 |

**Derived.** Together with §6, the infantry pipeline reduces to
`max(S × ∏ factors, 0)` over the selected entries. Order and ties do not
change it, apart from single-precision rounding (§5).

Several operations read tags from the event's **source context**
(`SourceEntityData.Context`) and **source tag** (`SourceEntityData.Tag`).
Which tags a given weapon puts there is set by the calling code (§1.1);
the operations below say what they look for.

### 7.1 `B_BoneDamageModifiers_C` (entries 5, 7, 10)

**Bytecode.** Table: class variable `DataTable`, default
[`DT_InfantryData_BoneDamageModifiers`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_BoneDamageModifiers.json);
row struct `WDBoneDamageModifierData`, map `HitLocations`.

```text
if DataTable invalid                                   → return 0
if source tag is exactly Meta.Damage.Explosive.Drone   → return 0
U = DT["Universal"].HitLocations[HitLocation]          (1.0 if no Universal row)
W = for each source-context tag, in order:
      row named by the tag, else by its direct parent (one level)
      first row found → W = row.HitLocations[HitLocation]
    no row found → W = 1.0
return C × U × W − C
```

The `Universal` row and the weapon row **multiply**; neither replaces the
other. The weapon rows are keyed by tags such as `Meta.Damage.Weapon.AR`
in the source context. Drone explosives are exempt.

Edge case: the map lookups ignore their found flag. If a row exists but
has no value for the hit location, the value becomes 0 and the hit's
running amount is zeroed. Every row in the current table carries all 12
infantry locations, so this only affects hit locations outside those 12.

### 7.2 `B_ArchetypeCaliberModifiers_C` (entry 6)

**Bytecode.** Table: class variable `DataTable`, default
[`DT_InfantryData_ArchetypeCaliberModifiers`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json);
row struct `WDArchetypeCaliberDamageModifierData`, map `CaliberModifiers`
(the export's `_aaabapbnbhiopifeenjml`).

```text
if DataTable invalid → return 0
row = first source-context tag naming a row, else its direct parent
W   = row.CaliberModifiers[source tag]
      else row.CaliberModifiers[parent of source tag]
      else 1.0                                  (also 1.0 if no row)
return C × W − C
```

The row is the weapon archetype from the source context; the key is the
caliber in the source tag. There is no `Universal` row here.

### 7.3 `B_AmmoTypeEffectiveness_C` (entries 138–141)

**Bytecode.** Table: a hard-coded reference to
[`DT_InfantryData_AmmoTypeEffectivenessPen`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json),
not a class variable; row struct `WDAmmoTypeEffectivenessData`, fields
`Modifier` and `ArmsClassOverrides` (the export's
`_aaabckamhakccdhbomlfj`).

```text
if target actor invalid → return 0
DPR = armor reduction of the hit piece, exactly as §7.5:
      first target-context tag under Meta.Damage.Armor / Meta.Damage.Helmet
      → equipped item → WDInventoryFragment_Armor
      → GetDurabilityStage(current durability).DamagePercentageReduction
      (0 if any step fails)
ammo = first source-context tag under Meta.Damage.AmmoModifier,
       default Meta.Damage.AmmoModifier.FMJ
AAS  = row[ammo].ArmsClassOverrides[first source-context tag under Meta.Damage.Arms]
       else row[ammo].Modifier
       else 1.0 if the row is missing
return −C × DPR × AAS / 100
```

The ammo type scales how much of the armor's reduction applies. There is
no clamp inside the operation, but with the current data `DPR × AAS`
peaks at 90 (60 × 1.5), so the factor stays positive. The function also
calls `WDProjectileSubsystem::GetProjectileStats` and stores
`BaseDamage` and `PenetrationEffectivenessMultiplier`, but never reads
them.

**Derived** (current data; DPR from §7.5):

| Ammo | AAS | vs Light (30) | vs Medium (40) | vs Heavy (50) | vs SuperHeavy (60) |
|---|---:|---:|---:|---:|---:|
| FMJ / Tracer | 1.0 | ×0.70 | ×0.60 | ×0.50 | ×0.40 |
| HollowPoint (+Tracer) | 1.5 | ×0.55 | ×0.40 | ×0.25 | ×0.10 |
| ArmorPiercing, `Arms.Small` | 0.7 | ×0.79 | ×0.72 | ×0.65 | ×0.58 |
| ArmorPiercing, `Arms.Medium` | 0.6 | ×0.82 | ×0.76 | ×0.70 | ×0.64 |
| ArmorPiercing, `Arms.High` | 0.5 | ×0.85 | ×0.80 | ×0.75 | ×0.70 |
| ArmorPiercing, other or no arms tag | 0.3 | ×0.91 | ×0.88 | ×0.85 | ×0.82 |

`Arms.Special` maps to 1.0 on the ArmorPiercing rows, so it behaves like
FMJ. Helmets use the same arithmetic with their own `R` (§7.5).

### 7.4 `B_VehicleSeatDamageReduction_C` (entry 145)

**Bytecode.** Table: a function-local reference to
[`DT_InfantryData_VehicleSeatDamageReduction`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json).
Rows hold `DamageSourceGroups[]`, each with `DamageSources` (arms tags)
and `VehicleSeats` (seat tag → percent); the export shows these as
`_aaabcmifdcijaclkbgcnk`, `_aaaanjpnkielfelgbcjma` and
`_aaaamdojmnlcookpbppgb`.

```text
arms = first source-context tag under Meta.Damage.Arms      (none → return 0)
target must be a WDMoverPlayerCharacter inside a vehicle    (else → return 0)
instigator in the same vehicle                              → return 0
row  = the victim vehicle's GetVehicleTag() name            (no parent fallback)
grp  = first group whose DamageSources contains arms exactly
pct  = first of the current seat's SeatTags found in grp.VehicleSeats
return C × pct / 100                                        (any miss → 0)
```

The stored percentages are negative, so the factor is `1 + pct/100`: for
example `-70` on a Humvee gives ×0.30 and `-25` on a Littlebird gives
×0.75. Shots from inside the same vehicle get no reduction.

### 7.5 `WDDamageModificationOperation_PlayerArmorDurability` (entries 142–144)

The only native custom operation. Vtable `0xB322140`; its slot 86 override
is `0x6BB7E10` (the base slot returns 0). Declaration
[`WDGame_classes.hpp`](sdk/raw/WDGame_classes.hpp#L36557).

**Native.** Given the event and the running amount `C`:

1. Take the target actor (`TargetEventData.Actor`) and its
   `WDPlayerInventoryComponent`. No actor or no component returns 0.
2. Scan the target's context tags for the first one under
   `Meta.Damage.Armor` or `Meta.Damage.Helmet`. That tag picks the item.
   This is whichever such tag comes first, not necessarily the one the
   rule entry required.
3. Resolve the equipped item for that tag and its
   `WDInventoryFragment_Armor`. The item instance must carry
   `WDFragmentReplicatedData_Armor`; otherwise return 0.
4. Call `GetDurabilityStage(Durability)` with the instance's current
   durability. Stages divide the item's maximum durability into equal
   bands; at durability 0 or below, the last stage applies.
5. Return `−(DamagePercentageReduction × 0.01) × C`.

The result is a fixed fraction of `C`: a factor of `1 − R/100`.

**Data.** Every armor item gives all four of its stages the same `R`, so
durability does not change the reduction in the current data:

| Item | Context tag | Max durability | `R` (%) | Covered hit locations |
|---|---|---:|---:|---|
| `ID_LightArmor` | `Meta.Damage.Armor.Light` | 200 | 30 | Torso (upper, middle, lower) |
| `ID_MediumArmor` | `Meta.Damage.Armor.Medium` | 220 | 40 | Torso |
| `ID_HeavyArmor` | `Meta.Damage.Armor.Heavy` | 250 | 50 | Torso |
| `ID_SuperHeavyArmor` | `Meta.Damage.Armor.SuperHeavy` | 300 | 60 | Torso, pelvis, upper arm |
| `ID_LightHelmet` | `Meta.Damage.Helmet.Light` | 80 | 30 | Head |
| `ID_MediumHelmet` | `Meta.Damage.Helmet.Medium` | 100 | 40 | Head |
| `ID_HeavyHelmet` | `Meta.Damage.Helmet.Heavy` | 180 | 50 | Head, neck |
| `ID_SuperHeavyHelmet` | `Meta.Damage.Helmet.SuperHeavy` | 200 | 60 | Head, neck |
| `ID_PilotHelmet` | `Meta.Damage.Helmet.Pilot` | 180 | 30 | Head |
| `ID_TankHelmet` | `Meta.Damage.Helmet.Tank` | 180 | 55 | Head, neck |
| Ghillie armor/helmets | `….Ghillie` | — | 0 (no stages) | — |

Source: [`Items/Armor/Content/Data/`](data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/).

**Derived.** Entries 142–143 apply this to explosive-blunt hits on helmet
and armor targets, and entry 144 to melee hits on armor targets. A
heavy-armor target hit by explosive blunt damage therefore has that
group's running amount halved by this operation. Bullet and cannon hits
on armor and helmets go through `B_AmmoTypeEffectiveness_C` instead
(entries 138–141, §7.3).

### 7.6 Worked example: custom-operation factors for an AR hit

**Derived**, under stated assumptions about the event's tags. Those tags
are set by the weapon code (§1.1), which has not been traced:

- source tag `Meta.Damage.Bullet.545mm` (so `Meta.Damage.Bullet`
  requirements match through the parent);
- source context contains `Meta.Damage.Weapon.AR` as its first tag with a
  bone-table row, and no ammo-modifier tag, so FMJ is assumed;
- for the armored case, target context contains `Meta.Damage.Armor.Heavy`;
- the target is not in a vehicle.

| Hit | Bone (§7.1) | Caliber (§7.2) | Armor (§7.3) | Custom product |
|---|---:|---:|---:|---:|
| Upper torso, no armor | 1.10 × 0.885 | 1.00 | — | **×0.9735** |
| Upper torso, heavy armor | 1.10 × 0.885 | 1.00 | ×0.50 | **×0.4868** |
| Head, no helmet | 1.0 × 2.35 | 1.00 | — | **×2.35** |
| Upper arm, no armor | 0.60 × 0.90 | 1.00 | — | **×0.54** |

The final amount is `S` × this product × the factor of every non-custom
entry the event also matches, clamped at zero. Which of the 74 non-custom
entries match depends on the full event tag set, so they are left out
here.

## 8. Helper table values

**Data.** The exported values the operations in §7 read. Each table
names the operation that consumes it.

### 8.1 BoneDamageModifiers (hit-location table)

[`DT_InfantryData_BoneDamageModifiers`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_BoneDamageModifiers.json)
has 20 rows, each with 12 hit locations. Row `Universal`:

| Hit location (`Meta.Damage.HitLocation.Infantry.*`) | Value |
|---|---:|
| `Head` | 1.00 |
| `Neck` | 0.75 |
| `Torso.Upper` | 1.10 |
| `Torso.Middle` | 1.00 |
| `Torso.Lower` | 0.95 |
| `Pelvis` | 0.90 |
| `Arm.Upper` | 0.60 |
| `Arm.Lower` | 0.50 |
| `Arm.Hand` | 0.30 |
| `Leg.Thigh` | 0.60 |
| `Leg.Calf` | 0.50 |
| `Leg.Foot` | 0.30 |

Head values in archetype rows:

| Row | Head |
|---|---:|
| `Universal` | 1.0 |
| `Meta.Damage.Weapon.AR` | 2.35 |
| `Meta.Damage.Weapon.SMG` | 2.1 |
| `Meta.Damage.Weapon.LMG` | 2.35 |
| `Meta.Damage.Weapon.Shotgun` | 1.5 |
| `Meta.Damage.Weapon.DMR` | 2.45 |
| `Meta.Damage.Weapon.Sniper` | 4.2667 |

Consumed by §7.1, which multiplies the `Universal` value by the weapon
row's value. An AR upper-torso hit therefore gets 1.10 × 0.885 = 0.9735,
and an AR headshot 1.0 × 2.35 = 2.35.

### 8.2 ArchetypeCaliberModifiers (weapon type × caliber)

[`DT_InfantryData_ArchetypeCaliberModifiers`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json),
rows keyed by weapon archetype, each a caliber → value map. Calibers
below shorten `Meta.Damage.Bullet.*`.

| Archetype | `556mm` | `545mm` | `308Win` | `762mm` | `762x54mm` |
|---|---:|---:|---:|---:|---:|
| `Meta.Damage.Weapon.AR` | 1.00 | 1.00 | 0.75 | 0.88 | — |
| `Meta.Damage.Weapon.DMR` | — | — | 0.85 | 1.00 | 0.80 |

`—` means the caliber is not in that row's map. Other archetype rows are
in the export.

### 8.3 AmmoTypeEffectivenessPen (ammo type)

[`DT_InfantryData_AmmoTypeEffectivenessPen`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json),
six rows:

| Row (`Meta.Damage.AmmoModifier.*`) | `Modifier` |
|---|---:|
| `FMJ` | 1.0 |
| `Tracer` | 1.0 |
| `HollowPoint` | 1.5 |
| `HollowPoint.Tracer` | 1.5 |
| `ArmorPiercing` | 0.3 |
| `ArmorPiercing.Tracer` | 0.3 |

Both ArmorPiercing rows also carry an arms-class map: `Meta.Damage.Arms.Small`
0.7, `Medium` 0.6, `High` 0.5, `Special` 1.0. Related data assets live in
[`AmmoModifiers/`](data/Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers/).

### 8.4 VehicleSeatDamageReduction (occupant protection table)

[`DT_InfantryData_VehicleSeatDamageReduction`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json):
11 vehicle-variant rows with values grouped by arms class, keyed by
`State.Player.Vehicle.SeatDamageReduction`. There are no explicit
driver/gunner/passenger rows. Variant names omit `Vehicle.Variant.`;
columns omit `Meta.Damage.Arms.`.

| Vehicle variant | Small + Medium | High | Special |
|---|---:|---:|---:|
| `Air.Rotary.ROT_01.Default` | -25 | -15 | — |
| `Air.Rotary.ROT_01.MountedMachineGuns` | -25 | -15 | — |
| `Air.Rotary.Havoc.Default` | -90 | -50 | -60 |
| `Air.Rotary.Littlebird.Default` | -25 | -15 | — |
| `Air.Rotary.Littlebird.RocketPods` | -25 | -15 | — |
| `Air.Rotary.Littlebird.MountedMachineGuns` | -25 | -15 | — |
| `Land.Wheeled.Humvee.Default` | -70 | -40 | — |
| `Land.Wheeled.Humvee.MachineGun` | -70 | -40 | — |
| `Land.Wheeled.Humvee.Minigun` | -70 | -40 | — |
| `Air.Rotary.ROT_04.Default` | -25 | -15 | — |
| `Air.Rotary.ROT_04.MountedMachineGuns` | -25 | -15 | — |

`—` means no group is exported, not zero. Consumed by §7.4: each value
is a percentage change, so -25 gives ×0.75 and -90 gives ×0.10.

## 9. Open questions and what closes them

| # | Question | Status |
|---|---|---|
| O-1 | Order between target-tag groups | **Closed** (§5): most specific tag first, then parents |
| O-2 | `PlayerArmorDurability` return | **Closed** (§7.5): `−(R/100) × C` |
| O-3 | Callers, origin of `S`, consumer of the result | **Closed** (§1.1). The bool's gameplay meaning stays open |
| O-4 | Entry data never reaches custom operations | **Closed** (§2) |
| O-5 | Four Blueprint bodies | **Closed** (§7.1–7.4), from the cooked bytecode |
| O-6 | End-to-end number for one concrete hit | **Partly closed** (§7.6): the custom-operation factors are computable. Which non-custom entries match needs the exact event tags each weapon sets |
| O-7 | The health write inside `TakeDamage` overrides, and network authority | Open. The write belongs to the effects pipeline; server behaviour cannot be observed statically. Security-relevant findings go through [`SECURITY.md`](SECURITY.md), not this document |

## 10. Evidence and sources

### Evidence reports

| Report | What it holds |
|---|---|
| [`docs/DAMAGE_IDA_RESTORED.md`](docs/DAMAGE_IDA_RESTORED.md) | Native trace of §1 and §4–6: method, loader limits, instruction anchors |
| [`docs/GOBJECTS_DAMAGE_ANALYSIS.md`](docs/GOBJECTS_DAMAGE_ANALYSIS.md) | Runtime class catalog and struct offsets (§2). Its Blueprint-locals reading is superseded by §7 |
| Blueprint bytecode (local, not committed) | Raw CUE4Parse exports with `ScriptBytecode`, a statement listing with byte offsets, and annotated pseudocode for each of the four `B_*` classes (§7.1–7.4) |
| [`docs/RESTORED_EXE_VALIDATION.md`](docs/RESTORED_EXE_VALIDATION.md) | Restored exe ↔ idmap match; damage vtables valid |
| [`docs/DECOMPILATION_CORPUS.md`](docs/DECOMPILATION_CORPUS.md) | The local corpus behind §1.1, §5 and §7.5; queried read-only with `corpus_q.py` (body, callers, callees, vtable slots) |
| [`docs/DAMAGE_IDA_TRACE.md`](docs/DAMAGE_IDA_TRACE.md) | Original question set B-1 to B-4 |
| [`docs/DAMAGE_IDA_RESULTS.md`](docs/DAMAGE_IDA_RESULTS.md) | Failed pass on the earlier dump-reconstructed exe (different hash) |

### Binary identity

| Artifact | SHA-256 | Size |
|---|---|---:|
| `WardogsClient-Win64-Shipping.restored.exe` | `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37` | 231,695,256 |
| `5.7.4-516586+++Wardogs+Live-Wardogs.idmap` | `f4b2942331061187454b625821f8a6119b267551d22dc1cabbdf1a4f3ee1afdb` | 4,942,224 |

The restored image carries the UTF-16LE build marker
`++Wardogs+Live-CL-516586`. RVAs here apply only to this hash.

### SDK

- [`WDGame_classes.hpp`](sdk/raw/WDGame_classes.hpp): operation base (L36507), `PlayerArmorDurability` (L36557), `UWDGlobalDamageSystem` (L36482), `UWDDamageSubsystem::ModifyDamage` (L44447)
- [`WDGame_structs.hpp`](sdk/raw/WDGame_structs.hpp): `FWDModifyDamageData` (L4646), `FWDDamageModification` (L4870), `FWDDamageModificationEntry` (L4887), `EWDDamageModificationOperation` (L1683), `FWDDamageModificationDebugData` (L11152)
- Blueprint declarations: [`B_BoneDamageModifiers`](sdk/raw/B_BoneDamageModifiers_classes.hpp), [`B_ArchetypeCaliberModifiers`](sdk/raw/B_ArchetypeCaliberModifiers_classes.hpp), [`B_AmmoTypeEffectiveness`](sdk/raw/B_AmmoTypeEffectiveness_classes.hpp), [`B_VehicleSeatDamageReduction`](sdk/raw/B_VehicleSeatDamageReduction_classes.hpp)
- [`WDGame_functions.cpp`](sdk/raw/WDGame_functions.cpp#L48948): generated `ModifyDamage` `ProcessEvent` wrapper, not the implementation

### Related reference docs

- [`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md): vehicle targets
- [`Wardogs_GameplayEffectsPipeline_v1.md`](Wardogs_GameplayEffectsPipeline_v1.md): attribute application
- [`Wardogs_CombatDataFlow_v1.md`](Wardogs_CombatDataFlow_v1.md): end-to-end flow
- [`Wardogs_InfantryWeapons_Stats_v1.md`](Wardogs_InfantryWeapons_Stats_v1.md): per-weapon base damage

## Change log

| Date | Change |
|---|---|
| 2026-10-16 | v1: initial SDK/data map. |
| 2026-10-17 | v1 evidence audit; failed IDA pass on the dump-reconstructed exe; restored-exe trace of selection, per-group ordering and arithmetic. |
| 2026-10-17 | **v2:** single reference. Merged the native trace, GObjects Blueprint analysis and exe validation; added evidence labels, the custom-entry table, the commutativity result for non-custom entries, the dead custom literals, and the shared-category ties among custom operations. Corrected the GObjects reading of the operation's second parameter (running damage `C`, not starting damage). |
| 2026-10-17 | Decompilation corpus (verify passed): closed O-1 (group order by target-tag hierarchy), O-2 (`PlayerArmorDurability` = `−(R/100) × C`, with per-item `R`), O-3 (callers; result flows into an Unreal damage event and `TakeDamage`) and O-4 (no entry data reaches custom operations). Added the collector's preconditions and the target-context matching rule. |
| 2026-10-17 | Blueprint bytecode (cooked assets, read statically): closed O-5 with the four operation bodies. All five custom operations are factors on `C`, so the infantry result is order-independent. Added the ammo-vs-armor factor table and a worked example (§7.6). Bone `Universal` and weapon rows multiply. |
