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
(§11).

Build: `++Wardogs+Live-CL-516586` · Engine: UE 5.7 · GAS fork: "BH"
(Embark's internal GAS variant) · Native addresses are file RVAs in the
restored executable, SHA-256 `a5c3db10…2b4f0cc37` (§11).

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
| Character health write: `ReceiveDamage` → vitality → base value of `Attribute.Gameplay.Health` | **Native** | §10 |
| Network authority | **Open** | §9 |

The short version: every selected rule, custom or not, multiplies the
running damage by a factor, and the total is clamped at zero once at the
end. Non-custom rules give `1 + Amount/100`. The bone operation gives
`Universal × weapon row` for the hit location. Armor gives
`1 − reduction% × ammo scalar / 100`. Because everything multiplies,
the order of evaluation does not change the result. §7.7 gives damage per
bullet for 33 weapons: an AK74M does 26 base, 61.1 to the head and 25.3
to the upper torso of an unarmored target.

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
float (reflected parameters: event at `0x0`, size `0x1D0`; bool at
`0x1D0`; return at `0x1D4`). It first converts the event into
`FWDModifyDamageData` (`0x6EF8DE0`), copying the event's `Amount` (`+0x0`)
into `ModifyDamageData.Amount` unchanged (`0x6EF8E2C`/`0x6EF8E37`), so
**`S` is the event's amount**. With the bool set it returns the event's
amount without evaluating; its gameplay meaning is **Open**. Without it,
the evaluator only runs when `S > 0`; otherwise `S` is returned as is. Which system an actual event selects is
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

Others are identified by the tags and classes they use:

| Caller | RVA | Path |
|---|---|---|
| Projectile impact (two calls) | `0x6B725B0` | Bullets and other projectiles; builds the event in §7.6 |
| Explosive actors (`AWDExplosive`, `AWDC4`, `AWDGrenade`, `AWDLandmine`, slot 236 via `0x6CAB030`) | `0x6CA8730` | Explosive detonation |
| Radial damage, also behind reflected `SimulateRadialDamage` | `0x6F06540` | Uses `Meta.Damage.Explosive.Radius.Inner` / `.Outer` |
| Back-blast | `0x6F06EB0` (from `0x6B92900`) | `Meta.Damage.DamageType.BackBlast` |
| Armor break / crack | `0x6B53000` | `Hitmarker.Armor.Break` / `.Crack` |
| Reflected `SimpleDamageActor` | `0x6F08CE0` (corpus body under the misaligned row `0x6F08CDC`) | Blueprint-callable |
| Vehicle supply containers (slot 127) | `0x6F03F60` | Via `0x7635EA0` |

Four more callers, so all 17 call sites are identified:

- `0x6E72D90`: a character hit by an actor (a delegate bound in
  `AWDMoverCharacter` slot 169). It skips dead characters; the source is
  the hitting actor's entity data plus `DamageType.Impact`.
- `0x6F042A0`: a second back-blast path from `0x6B92900` (see the table).
  The two are the branches of one if/else; what picks the branch is not
  traced (O-8).
- `0x76740F0`: vehicle collision
  ([VehicleDamagePipeline V-4](Wardogs_VehicleDamagePipeline_v1.md#7-open-questions)).
- `0x76F5AE0`: periodic `WDDoor` damage, from `PostFixedSimTick`.

`0x6E72D90` and `0x76F5AE0` pass 1. Each caller builds its own event
(`0x6BB4D30`), so `S` is whatever that caller supplies.

The reflected `BP_DamageActor` (`0x6F07C10`) goes straight to the
application step below without calling `ModifyDamage`. Damage dealt
through it skips the rule tables entirely.

Most callers then hand the result to the same two steps:

1. **Build an Unreal damage event** (`0x6EF9450`; the corpus row
   `0x6EF944F` starts one byte early): damage = the modified
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

For characters and vehicles the `WDDamageable` path is the one taken; the
character's health write is traced in §10, the vehicle section model in
[VehicleDamagePipeline §4](Wardogs_VehicleDamagePipeline_v1.md).

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
the original struct and the running amount `C` (`xmm2`, `0x6BB72E1`).
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
2. Look that tag up in the damage data registry (`DamageRegistryName`;
   when unset, the collector fills it and the category asset from
   `WDGameSettings.DamageSystemSettings.GlobalDamageDataRegistryName` /
   `GlobalDamageCategoryDataAsset`, `+0x378`/`+0x380`).
   If a `FWDDamageableEntityTableRow` exists, match its entries (§4) and
   file the selected ones under that tag. A group is created when its
   first entry is selected.
3. Move to the tag's direct parent and repeat. Stop on reaching
   `RootDamageTag` or when there is no parent. `RootDamageTag` is
   `Meta.Damage`, set by the system's constructor (`0x6BB6160`) from a
   native tag global, and is itself never evaluated.

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
- Every term is recorded in the event's `ModificationResults` list
  (`FWDDamageEventData +0x190`). A custom term is appended before its call,
  unconditionally; a non-custom delta is applied first and recorded only
  when `|delta| > 1e-8` (abs mask and threshold loaded at `0x6BB7153`/
  `0x6BB715C`, compare at `0x6BB7344`). The threshold never suppresses
  arithmetic.
- All arithmetic is single-precision float.

Instruction anchors: `0x6BB72E1` current amount into `xmm2` for the adapter,
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

### 7.6 The bullet event

**Native** (`0x6B725B0`, the projectile-impact path; it uses
`Meta.Damage.DamageType.Projectile` and the `Kinetic.Impact` tags). For a
direct hit it builds the event from the projectile data asset and the
firing weapon:

| Event field | Value | Evidence |
|---|---|---|
| Stats | `GetProjectileStats(AmmoModifierTag)`: the asset's `ProjectileStats` (`+0x38`), or the per-ammo-type variant in `CachedModifiedProjectileStats` (`+0x350`) | `0x6BBA900` |
| `S` | `DamageValues.BaseDamage`; `ExplosiveBluntDamage` instead when the projectile has an arming delay and its flight time (`FWDProjectileInstance.ElapsedTime`, seconds) is below `ArmingDelay − 0.0001`, or when an unnamed instance byte (`+0x101`) is clear. That byte is unreflected (no name in GObjects); the instance constructor sets it to 1, and no writer that clears it was found. Then scaled twice, below | stats `+0x30` / `+0x44`, `+0x180`, `+0x184`; instance `+0x290`, `+0x101` (constructor `0x6B8E100`) |
| Speed scale | `× clamp(impact speed / reference speed, 0, 1)`. Reference is the weapon's `TypicalSpeed` when `bOverrideTypicalSpeed` is set and that value is > 0, else the projectile's `TypicalSpeed` | `0x6C255B0`; weapon `+0xA0`/`+0xA4`, stats `+0x1FC` |
| Distance scale | `× DistanceDamageFalloffCurve(distance)` when the weapon's `bUseDistanceDamageFalloffCurve` is set; distance is shot origin to hit point in **centimetres** | `0x6B70D80` (direct hit, called at `0x6B7330C`); `0x6B72D53`–`0x6B72DCB` per custom hit; weapon `+0xA8`/`+0xB0`; hit `ImpactPoint` `+0x28`, `ProjectileOrigin` `+0x110` |
| Armor in target context | The target's hook (`IWDDamageable` sub-vtable `+0x20`) runs before `ModifyDamage`. For characters it calls `Auth_GetArmorDamageEvent`, which copies the target's entity data and then **removes every armor tag except the first one (in context order) whose piece's `CoveredHitLocations` contains the hit-location tag** (derived from the hit bone and written to `HitLocationTag`, event `+0x1A0`). With no resolved hit location, all armor tags are removed. Only the covering piece reaches §7.3 and §7.5. When the projectile has `bShouldPenetrate` and the covering piece passes the hook's checks, it then appends `Meta.Damage.Armor.Penetrate` (penetration test passes) or `Meta.Damage.Armor.Throughput` to the source context; the armor rule table (`DT_GlobalDamage_ArmorData`) keys on `Armor.Penetrate` | `0x6B52A40`; alias labels `AWDMoverCharacter` slot 390, `AWDTargetDummy` slot 242 |
| Source tag | stats `DamageEntityData.Tag`, e.g. `Meta.Damage.Bullet.545mm` | stats `+0x00` |
| Source context, in order | stats `DamageEntityData.Context` (e.g. `Meta.Damage.Arms.Medium`); the firing weapon's damage tag (e.g. `Meta.Damage.Weapon.AR.A91`); `Kinetic.Impact.Ricochet` / `.Penetration` when bit (HitCount − 2) of `RicochetBitMap` / `PenetrationBitMap` is set; the asset's `ProjectileId` (e.g. `Item.Caliber.545mm`); then, only if the hit is not `bExploding`, `Meta.Damage.DamageType.Projectile` and (with an arming delay, armed or not) `Kinetic.Impact.ExplosiveBlunt`. An exploding hit skips both scales, the hook and `ModifyDamage` here. The source `CauseEntityTag` (event `+0x88`) is overwritten from the slot record (`+0x1C`) | `0x6B725B0`; tag names from the static initializers |
| Custom hits | If the hit carries `CustomHitResults`, each custom hit gets its own copy of the event (distance scale, hook, `ModifyDamage`). The one with the highest result above 0 is kept and the direct-hit `ModifyDamage` is skipped. The direct path runs only when there are no custom hits or none scores above 0 | `0x6B725B0` |

The weapon tag is identified by value: the slot record supplies a tag,
and every weapon item's `DamageEntityData.Tag` in the export is such a
tag (`ID_A91` → `Meta.Damage.Weapon.AR.A91`). The table's own rule 97,
which requires `Meta.Damage.Weapon.Pistol.M1911` in the source, only
matches if the weapon tag is there.

Consequences for §7.1–7.2: the specific weapon tag has no row, so the
one-level parent fallback lands on the archetype row
(`Meta.Damage.Weapon.AR`). The caliber key is the source tag.

### 7.7 Per-weapon damage per bullet

**Derived**, generated by
[`_tools/damage_tables.py`](_tools/damage_tables.py) from the export
with the rules above. Assumptions: point blank (both scales at 1; see
§7.8), hostile alignment, FMJ (the base stats), a direct hit with no
ricochet or penetration, an unarmored target outside any vehicle, and no
instigator tags (no infantry entry needs them). Shotgun values are per pellet. Each cell shows damage per bullet
and the total factor on `BaseDamage`. The last column lists the entries
with a factor other than 1.

<!-- damage_tables default -->
| Weapon | Weapon tag | Caliber | Base | Head | Neck | Torso.Upper | Torso.Middle | Arm.Upper | Leg.Thigh | Entries applied |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| A91 | `AR.A91` | `556mm` | 28 | 65.8 (×2.35) | 49.4 (×1.76) | 27.3 (×0.974) | 27.2 (×0.97) | 15.1 (×0.54) | 15.1 (×0.54) | 5 |
| TAR21 | `AR.A91` | `556mm` | 28 | 65.8 (×2.35) | 49.4 (×1.76) | 27.3 (×0.974) | 27.2 (×0.97) | 15.1 (×0.54) | 15.1 (×0.54) | 5 |
| WEPN_033 | `AR.A91` | `556mm` | 28 | 65.8 (×2.35) | 49.4 (×1.76) | 27.3 (×0.974) | 27.2 (×0.97) | 15.1 (×0.54) | 15.1 (×0.54) | 5 |
| AK74M | `AR.AK47M` | `545mm` | 26 | 61.1 (×2.35) | 45.8 (×1.76) | 25.3 (×0.974) | 25.2 (×0.97) | 14.0 (×0.54) | 14.0 (×0.54) | 5 |
| WEPN_030 | `AR.Fal` | `308Win` | 45 | 79.3 (×1.76) | 59.5 (×1.32) | 32.9 (×0.73) | 32.7 (×0.728) | 18.2 (×0.405) | 18.2 (×0.405) | 5, 6 |
| WEPN_029 | `AR.Galil` | `556mm` | 28 | 65.8 (×2.35) | 49.4 (×1.76) | 27.3 (×0.974) | 27.2 (×0.97) | 15.1 (×0.54) | 15.1 (×0.54) | 5 |
| KH2002 | `AR.KH2002` | `556mm` | 28 | 65.8 (×2.35) | 49.4 (×1.76) | 27.3 (×0.974) | 27.2 (×0.97) | 15.1 (×0.54) | 15.1 (×0.54) | 5 |
| M4 | `AR.M4` | `556mm` | 28 | 65.8 (×2.35) | 49.4 (×1.76) | 27.3 (×0.974) | 27.2 (×0.97) | 15.1 (×0.54) | 15.1 (×0.54) | 5 |
| WEPN_037 | `AR.WEPN_037` | `762mm` | 34 | 70.3 (×2.07) | 52.7 (×1.55) | 29.1 (×0.857) | 29.0 (×0.854) | 16.2 (×0.475) | 16.2 (×0.475) | 5, 6 |
| RFB | `DMR.RFB` | `308Win` | 45 | 93.7 (×2.08) | 70.3 (×1.56) | 45.0 (×1) | 45.1 (×1) | 28.7 (×0.637) | 28.7 (×0.637) | 5, 6 |
| SKS | `DMR.SKS` | `762mm` | 34 | 83.3 (×2.45) | 62.5 (×1.84) | 40.0 (×1.18) | 40.1 (×1.18) | 25.5 (×0.75) | 25.5 (×0.75) | 5 |
| SVDM | `DMR.SVDM` | `762x54mm` | 44 | 86.2 (×1.96) | 64.7 (×1.47) | 41.4 (×0.942) | 41.5 (×0.944) | 26.4 (×0.6) | 26.4 (×0.6) | 5, 6 |
| WEPN_034 | `DMR.WEPN_034` | `308Win` | 45 | 93.7 (×2.08) | 70.3 (×1.56) | 45.0 (×1) | 45.1 (×1) | 28.7 (×0.637) | 28.7 (×0.637) | 5, 6 |
| LMG_02 | `LMG.LMG_02` | `762x54mm` | 44 | 77.6 (×1.76) | 58.2 (×1.32) | 32.1 (×0.73) | 32.0 (×0.728) | 17.8 (×0.405) | 17.8 (×0.405) | 5, 6 |
| M249 | `LMG.M249` | `556mm` | 28 | 65.8 (×2.35) | 49.4 (×1.76) | 27.3 (×0.974) | 27.2 (×0.97) | 15.1 (×0.54) | 15.1 (×0.54) | 5 |
| WEPN_036 | `LMG.WEPN_036` | `308Win` | 45 | 79.3 (×1.76) | 59.5 (×1.32) | 32.9 (×0.73) | 32.7 (×0.728) | 18.2 (×0.405) | 18.2 (×0.405) | 5, 6 |
| WEPN_027 | `Pistol.Deagle` | `50AE` | 63 | 132.3 (×2.1) | 99.2 (×1.58) | 72.8 (×1.16) | 66.2 (×1.05) | 49.1 (×0.78) | 49.1 (×0.78) | 5 |
| Glock17 | `Pistol.G60` | `9mm` | 22 | 46.2 (×2.1) | 34.7 (×1.58) | 25.4 (×1.16) | 23.1 (×1.05) | 17.2 (×0.78) | 17.2 (×0.78) | 5 |
| WEPN_032 | `Pistol.G60` | `9mm` | 22 | 46.2 (×2.1) | 34.7 (×1.58) | 25.4 (×1.16) | 23.1 (×1.05) | 17.2 (×0.78) | 17.2 (×0.78) | 5 |
| Judge | `Pistol.Judge` | `45Colt` | 45 | 94.5 (×2.1) | 70.9 (×1.58) | 52.0 (×1.16) | 47.2 (×1.05) | 35.1 (×0.78) | 35.1 (×0.78) | 5 |
| WEPN_026 | `Pistol.M1911` | `45ACP` | 30 | 81.9 (×2.73) | 61.4 (×2.05) | 45.0 (×1.5) | 41.0 (×1.37) | 30.4 (×1.01) | 30.4 (×1.01) | 5, 97 |
| WEPN_028 | `SMG.MP5` | `9mm` | 22 | 46.2 (×2.1) | 34.7 (×1.58) | 25.4 (×1.16) | 23.1 (×1.05) | 17.2 (×0.78) | 17.2 (×0.78) | 5 |
| MP9 | `SMG.MP7` | `9mm` | 22 | 46.2 (×2.1) | 34.7 (×1.58) | 25.4 (×1.16) | 23.1 (×1.05) | 17.2 (×0.78) | 17.2 (×0.78) | 5 |
| SMG_03 | `SMG.SMG3` | `9mm` | 22 | 46.2 (×2.1) | 34.7 (×1.58) | 25.4 (×1.16) | 23.1 (×1.05) | 17.2 (×0.78) | 17.2 (×0.78) | 5 |
| Vector | `SMG.Vector` | `45ACP` | 30 | 63.0 (×2.1) | 47.3 (×1.58) | 34.7 (×1.16) | 31.5 (×1.05) | 23.4 (×0.78) | 23.4 (×0.78) | 5 |
| WEPN_031 | `SMG.WEPN_031` | `9mm` | 22 | 46.2 (×2.1) | 34.7 (×1.58) | 25.4 (×1.16) | 23.1 (×1.05) | 17.2 (×0.78) | 17.2 (×0.78) | 5 |
| M500 | `Shotgun.M12G` | `7mmBuck` | 25 | 37.5 (×1.5) | 28.1 (×1.12) | 24.8 (×0.99) | 22.5 (×0.9) | 15.8 (×0.63) | 15.8 (×0.63) | 5 |
| MP43 | `Shotgun.M12G` | `7mmBuck` | 25 | 37.5 (×1.5) | 28.1 (×1.12) | 24.8 (×0.99) | 22.5 (×0.9) | 15.8 (×0.63) | 15.8 (×0.63) | 5 |
| MK22 | `Sniper.MRAD` | `308Win` | 45 | 192.0 (×4.27) | 144.0 (×3.2) | 118.8 (×2.64) | 87.0 (×1.93) | 40.5 (×0.9) | 40.5 (×0.9) | 5 |
| SR_04 | `Sniper.MRAD` | `50Cal` | 90 | 324.1 (×3.6) | 243.1 (×2.7) | 207.9 (×2.31) | 151.0 (×1.68) | 81.0 (×0.9) | 81.0 (×0.9) | 5, 124, 125, 126, 127 |
| WEPN_017 | `Sniper.Mosin` | `762x54mm` | 44 | 187.7 (×4.27) | 140.8 (×3.2) | 116.2 (×2.64) | 85.1 (×1.93) | 39.6 (×0.9) | 39.6 (×0.9) | 5 |
| SV98 | `Sniper.SV98` | `762x54mm` | 44 | 187.7 (×4.27) | 140.8 (×3.2) | 116.2 (×2.64) | 85.1 (×1.93) | 39.6 (×0.9) | 39.6 (×0.9) | 5 |
| WEPN_035 | `Sniper.WEPN_035` | `556mm` | 28 | 119.5 (×4.27) | 89.6 (×3.2) | 73.9 (×2.64) | 54.1 (×1.93) | 25.2 (×0.9) | 25.2 (×0.9) | 5 |
<!-- /damage_tables -->

Armor scales these per §7.3, but only where the piece covers the hit
location: FMJ into heavy body armor halves the torso values and leaves
headshots untouched. Ammo types against armor are in §7.9.

### 7.8 Damage over distance

**Derived**, `_tools/damage_tables.py --falloff`: upper-torso damage
from §7.7 times each weapon's distance curve. Curve keys are shown in
metres (the stored `Time` is centimetres). The speed scale is left at 1.
All 24 speed overrides in the data (13,000–60,300 cm/s) are below their
weapon's muzzle speed, so it only bites once a round has slowed that far,
which depends on drag and is not modelled here. † marks a curve with
cubic keys, where values between keys are a linear approximation.

<!-- damage_tables --falloff -->
| Weapon | Curve keys (m → ×) | 50 m | 100 m | 200 m | 400 m | 800 m | 1200 m |
|---|---|---:|---:|---:|---:|---:|---:|
| A91 | 0: 1, 300: 1, 1200: 0.2 | 27.3 | 27.3 | 27.3 | 24.8 | 15.1 | 5.5 |
| TAR21 | 0: 1, 300: 1, 1200: 0.2 | 27.3 | 27.3 | 27.3 | 24.8 | 15.1 | 5.5 |
| WEPN_033 | 0: 1, 300: 1, 1200: 0.2 | 27.3 | 27.3 | 27.3 | 24.8 | 15.1 | 5.5 |
| AK74M | 0: 1, 500: 1, 1200: 0.2 | 25.3 | 25.3 | 25.3 | 25.3 | 16.6 | 5.1 |
| WEPN_030 | 0: 1, 800: 1, 1200: 0.2 | 32.9 | 32.9 | 32.9 | 32.9 | 32.9 | 6.6 |
| WEPN_029 | 0: 1, 400: 1, 1200: 0.2 | 27.3 | 27.3 | 27.3 | 27.3 | 16.4 | 5.5 |
| KH2002 | 0: 1, 300: 1, 1200: 0.2 | 27.3 | 27.3 | 27.3 | 24.8 | 15.1 | 5.5 |
| M4 | 0: 1, 500: 1, 1200: 0.2 | 27.3 | 27.3 | 27.3 | 27.3 | 17.9 | 5.5 |
| WEPN_037 | 0: 1, 400: 1, 1200: 0.2 | 29.1 | 29.1 | 29.1 | 29.1 | 17.5 | 5.8 |
| RFB | 0: 1, 500: 1, 1200: 0.2 | 45.0 | 45.0 | 45.0 | 45.0 | 29.6 | 9.0 |
| SKS | 0: 1, 400: 1, 1200: 0.2 | 40.0 | 40.0 | 40.0 | 40.0 | 24.0 | 8.0 |
| SVDM | 0: 1, 800: 1, 1200: 0.2 | 41.4 | 41.4 | 41.4 | 41.4 | 41.4 | 8.3 |
| WEPN_034 | 0: 1, 500: 1, 1200: 0.2 | 45.0 | 45.0 | 45.0 | 45.0 | 29.6 | 9.0 |
| LMG_02 | 0: 1, 1000: 1, 1500: 0.2 | 32.1 | 32.1 | 32.1 | 32.1 | 32.1 | 21.8 |
| M249 | 0: 1, 700: 1, 1200: 0.2 | 27.3 | 27.3 | 27.3 | 27.3 | 22.9 | 5.5 |
| WEPN_036 | 0: 1, 1000: 1, 1500: 0.2 | 32.9 | 32.9 | 32.9 | 32.9 | 32.9 | 22.3 |
| WEPN_027 | 0: 1, 100: 1, 1200: 0.2 | 72.8 | 72.8 | 67.5 | 56.9 | 35.7 | 14.6 |
| Glock17 | 0: 1, 50: 1, 1200: 0.3 | 25.4 | 24.6 | 23.1 | 20.0 | 13.8 | 7.6 |
| WEPN_032 | 0: 1, 50: 1, 1200: 0.3 | 25.4 | 24.6 | 23.1 | 20.0 | 13.8 | 7.6 |
| Judge | none | 52.0 | 52.0 | 52.0 | 52.0 | 52.0 | 52.0 |
| WEPN_026 | 0: 1, 50: 1, 1200: 0.3 | 45.0 | 43.7 | 40.9 | 35.4 | 24.5 | 13.5 |
| WEPN_028† | 0: 1, 200: 1, 300: 0.6, 1200: 0.1 | 25.4 | 25.4 | 25.4 | 13.8 | 8.2 | 2.5 |
| MP9† | 0: 1, 100: 1, 200: 0.6, 1200: 0.1 | 25.4 | 25.4 | 15.2 | 12.7 | 7.6 | 2.5 |
| SMG_03† | 0: 1, 200: 1, 300: 0.6, 1200: 0.1 | 25.4 | 25.4 | 25.4 | 13.8 | 8.2 | 2.5 |
| Vector | 0: 1, 50: 1, 70: 0.6, 100: 0.4, 150: 0.3, 1200: 0.2 | 34.7 | 13.9 | 10.2 | 9.6 | 8.3 | 6.9 |
| WEPN_031† | 0: 1, 200: 1, 300: 0.6, 1200: 0.1 | 25.4 | 25.4 | 25.4 | 13.8 | 8.2 | 2.5 |
| M500 | none | 24.8 | 24.8 | 24.8 | 24.8 | 24.8 | 24.8 |
| MP43 | none | 24.8 | 24.8 | 24.8 | 24.8 | 24.8 | 24.8 |
| MK22 | 0: 1, 500: 1, 1000: 1, 1600: 0.4 | 118.8 | 118.8 | 118.8 | 118.8 | 118.8 | 95.0 |
| SR_04 | 0: 1, 500: 1, 2000: 1, 2500: 0.4 | 207.9 | 207.9 | 207.9 | 207.9 | 207.9 | 207.9 |
| WEPN_017 | 0: 1, 500: 1, 1200: 0.4 | 116.2 | 116.2 | 116.2 | 116.2 | 86.3 | 46.5 |
| SV98 | 0: 1, 1000: 1, 1500: 0.4 | 116.2 | 116.2 | 116.2 | 116.2 | 116.2 | 88.3 |
| WEPN_035 | 0: 1, 300: 1, 1200: 0.2 | 73.9 | 73.9 | 73.9 | 67.3 | 41.1 | 14.8 |
<!-- /damage_tables -->

### 7.9 Ammo type against armor

**Native** (`0x6BBA900` miss path). An ammo variant's stats are a copy of
the base stats with the ammo-modifier tag added to
`DamageEntityData.Context`, then the `DA_AmmoModifier_*` attribute
multipliers applied. None of the five assets touches a damage value: they
change penetration effectiveness, effective range, penetration exit speed
and tracer chance. FMJ has no asset, so its stats are the plain copy with
no tag. Ammo type therefore changes damage only through that tag: the
HP/AP rules and the ammo scalar in §7.3.

The tag reaches the event from the projectile's ammo tag (instance
`+0xF0`, empty from the constructor `0x6B8E100`), which `0x6F30E50` sets
from the spawn parameters. On the fire path the weapon owner
(`IWDWeaponOwner` `+0x90`, `0x6C98290`) builds
`Meta.Damage.AmmoModifier.<type>` from the loaded round's item tag.
Predicted simulations use `FWDProjectileSimulationSetup.AmmoModifierTag`
(`0x6F2C450`). Which item-tag parts form `<type>` is only partly decoded
(`0x6C98290`).

**Derived**, `_tools/damage_tables.py --ammo M4`: M4 (5.56 mm,
`Arms.Medium`, base 28), point blank, armor piece covering the hit:

<!-- damage_tables --ammo M4 -->
| Ammo | Torso, no armor | Torso, Light | Torso, Medium | Torso, Heavy | Torso, SuperHeavy | Head, no helmet | Head, Light helmet | Head, Medium helmet | Head, Heavy helmet | Head, SuperHeavy helmet | Entries applied |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| FMJ | 27.3 | 19.1 | 16.4 | 13.6 | 10.9 | 65.8 | 46.1 | 39.5 | 32.9 | 26.3 | 5, 138, 140 |
| Tracer | 27.3 | 19.1 | 16.4 | 13.6 | 10.9 | 65.8 | 46.1 | 39.5 | 32.9 | 26.3 | 5, 138, 140 |
| HollowPoint | 54.5 | 8.1 | 5.9 | 3.7 | 1.5 | 131.6 | 13.0 | 9.5 | 5.9 | 2.4 | 5, 18, 20, 21, 133, 134, 138, 140 |
| ArmorPiercing | 21.8 | 17.9 | 16.6 | 15.3 | 14.0 | 52.6 | 43.2 | 40.0 | 36.8 | 33.7 | 5, 15, 138, 140 |
<!-- /damage_tables -->

Hollow point doubles damage against bare flesh (entry 18, +100 %) but is
cut hard by any covering armor: entries 20/21 (−70 % helmet, −55 % armor),
133/134 (−40 %) and the 1.5 ammo scalar. Armor piercing loses 20 %
everywhere (entry 15) but its 0.6 scalar for medium arms keeps most of
its damage through armor. Tracer behaves like FMJ. Swap the weapon name to
table any other weapon.

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
| O-6 | End-to-end number for one concrete hit | **Closed for bullets** (§7.6–7.9): every ammo type, armored or not, by distance. Only the speed scale after drag is not modelled |
| O-7 | The health write | **Closed** (§10). Network authority stays open: role checks are visible in code, but server behaviour cannot be observed statically. Security-relevant findings go through [`SECURITY.md`](SECURITY.md), not this document |
| O-8 | Which branch of `0x6B92900` runs for a back-blast: `0x6F042A0` (traced hits) or `0x6F06EB0` (a synthetic hit, [VehicleDamagePipeline §3.2](Wardogs_VehicleDamagePipeline_v1.md#32-from-a-hit-triangle-to-a-section)) | Open: the if/else condition in `0x6B92900` is not traced |

## 10. From damage to health (characters)

**Native.** For a character, the application step (§1.1) dispatches
through `IWDDamageable` (`0x6C2A5F0`) and health is written directly as an
attribute base value. No gameplay effect is applied.

1. `AWDMoverCharacter` carries `IWDDamageable` at object `+0x640`
   (interface vtables `0xB40C038`, and `0xB410D20` for the player class).
   Slot 2, `ReceiveDamage`, is `0x6E74C40` in both. It jumps to the
   vitality component (object `+0x748`), vtable `+0x500`.
2. `UWDCharacterVitalityComponent` (`0x6B17760`) returns 0 for damage
   ≤ 0. A character without `State.Player.Vitality.Alive` (downed or
   dead; the code does not distinguish) gets no health write, and 0 is
   returned. Only an `AWDMoverPlayerCharacter` owner gets more: it receives
   the damage event through the `ProcessEvent` stub
   `AWDMoverPlayerCharacter::Client_ForceTakeHitCue` (`0x6E7F0B0`), and
   when the instigating controller's pawn is a player character, that pawn
   receives it too through `::Client_TriggerHitMarker` (`0x6E7F420`, with
   a `State.Player.Vitality.Critical` tag container). The names come from
   the functions' FName initializers (`0x12CC0D0`, `0x12CC0F0`). Otherwise
   it calls the base `UWDVitalityComponent` (`0x6B82520`), then, only when
   the owning actor's role value is 3, reduces a decay pool at `+0x17C` by
   the damage, at most to 0.
3. `0x6B82520` calls `0x52311D0` on the `Attribute.Gameplay.Health`
   handle (component `+0x140`, created in `0x6B81CE0`) with
   `−CurrentDamage`. `0x52311D0` adds that delta to the attribute's
   stored value and calls `SetAttributeBaseValue` (`0x5236AF0`), whose
   setter (`0x5236E50`) runs the attribute's base-value hook, stores the
   new base and pushes it into the replicated attribute array. Character
   health registers a base- and a current-value hook in `0x6B81CE0`, only
   when the owner's role value is 3. Both call the vitality component's
   virtual slot 161. For characters (`0x6B17D20`) it clamps the value to
   `[0, MaxHealth + MaxOverhealHealth + MaxDecayHealth]`, and to at least
   1 while the owning `WDMoverCharacter` has `bInvincible`. The base
   component's version (`0x6B83270`) clamps to `[0, MaxHealth]`.
4. Back in `0x6B82520`: if the applied change is zero it returns 0.
   Otherwise it records whether current health is now ≤ 0, broadcasts
   `OnDamageTaken` and `RegenTimer` (with `RegenDelay`), and sends
   `WDEvent_Damage`. Only then, if health was ≤ 0, it broadcasts
   `OnBeforeKilled` and `OnKilled` and sends `WDEvent_Killed`. It returns
   the size of the applied change, which the caller writes back to
   `CurrentDamage`.

A character's `TakeDamage` override (`0x6E77C40`) does not write health:
it converts an incoming Unreal damage event into a WD event and re-enters
the application step. The role checks on this path (`0x6B82520` and
`0x5236AF0` both gate on a role value of 3) are code facts; what they mean
for server behaviour is not established here.

## 11. Evidence and sources

### Evidence reports

| Report | What it holds |
|---|---|
| [`docs/evidence/damage.md`](docs/evidence/damage.md) | Evidence behind §1 and §4–6: input hashes, the three native passes (questions B-1 to B-4, the failed pass on the dump-reconstructed exe, the restored-exe trace with its instruction anchors), the corpus cross-check, and a verification status for every RVA this page cites |
| [`docs/GOBJECTS_DAMAGE_ANALYSIS.md`](docs/GOBJECTS_DAMAGE_ANALYSIS.md) | Runtime class catalog and struct offsets (§2). Its Blueprint-locals reading is superseded by §7 |
| Blueprint bytecode (local, not committed) | Raw CUE4Parse exports with `ScriptBytecode`, a statement listing with byte offsets, and annotated pseudocode for each of the four `B_*` classes (§7.1–7.4) |
| [`docs/RESTORED_EXE_VALIDATION.md`](docs/RESTORED_EXE_VALIDATION.md) | Restored exe ↔ idmap match; damage vtables valid |
| [`docs/DECOMPILATION_CORPUS.md`](docs/DECOMPILATION_CORPUS.md) | The local corpus behind §1.1, §5 and §7.5; queried read-only with `corpus_q.py` (body, callers, callees, vtable slots) |

### Offsets and engine details cross-checked

Offsets the code relies on, confirmed against the runtime reflection data
in the GObjects property dump (independent of the SDK headers and of the
corpus's validated types):

| Item | Value | Source |
|---|---|---|
| `FWDDamageEventData.Amount` / `.ModificationResults` | `0x0` / `0x190` (size `0x1D0`) | GObjects `WDDamageEventData`; `ModifyDamage` parameter block |
| `FWDDamageableEntityTableRow.DamageModificationEntries` | `0x10` | GObjects `WDDamageableEntityTableRow` |
| `FWDDamageModificationInputData` contexts / `Alignment` / `HitLocation` | `0x0`, `0x20`, `0x40` / `0x60` / `0x64` | GObjects `WDDamageModificationInputData` |
| `UWDGameSettings` `+0x378` / `+0x380` | `DamageSystemSettings` (`0x338`) `.GlobalDamageDataRegistryName` (`+0x40`) / `.GlobalDamageCategoryDataAsset` (`+0x48`) | SDK and GObjects agree |
| `UClass` default object | `+0x110` | SDK `CoreUObject_classes.hpp` |
| Subclass check `+0x30`/`+0x38` | UE5's struct base chain (`StructBaseChainArray`, `NumStructBasesInChainMinusOne`), the engine's fast `IsChildOf` | Code pattern in `0x6BB6A60`, `0x6BB7E10` |
| Adapter's `+0xD4 & 0x80` | `UClass::ClassFlags` bit `CLASS_Native` (`0x80`): native override → direct virtual call, otherwise `ProcessEvent` | UE `EClassFlags`; `CastFlags` follows at `0xD8` in the SDK |
| Group order = insertion order | `0x6BB5ED0` → `TSet::Emplace` `0x6BB5DC0` → `TSparseArray::AddUninitialized` `0x1587900`, which appends unless the free count (`+0x34`) is non-zero. The evaluator builds the map with none and the collector never removes | Code |
| Parent-tag step `0x395F4D0` | `UGameplayTagsManager::Get` (`0x395ADE0`) then the manager lookup: `FGameplayTag::RequestDirectParent` | Code |
| Armor op's `+0x738` | A virtual call, `AActor` slot 231 (`0x3A93090`): `FindComponentByClass` over the actor's components (`+0x240`), here with `WDPlayerInventoryComponent` | Code |
| Only dispatcher of `GetModificationAmount` by name | The `GetModificationAmount` name global is referenced only by the adapter `0x6BB7900` | Corpus full-text search |
| Category order | Calibre, AmmoModifier, CaliberEffectiveness, Bone, PenetrationEffectiveness, Tracer, Weapon, Armor, Melee, Ricochet, Penetration, Friendly | `DA_GlobalDamage_Categories.json` |
| Garbage flag `0x40000000` | `RF_MirroredGarbage` (UE5's replacement for `RF_PendingKill`); `sdk/raw/Basic.hpp` has it, the corpus `schema.json` enum import omits it | SDK, UE `ObjectMacros.h` |

Several cited functions have no aligned corpus body: `0x53202B0`,
`0x52311D0`, `0x5236AF0`, `0x5236E50`, `0x6C255B0`, `0x6EF8DE0`,
`0x6BB5ED0` and `0x395F4D0`; `0x6F042A0` has a failed row. Claims that
rest on them (the section pick, the base-value write, the speed scale,
the conversion, group order, the parent-tag step) are backed by
disassembly (`[exe]`) only. Each was reproduced from the instructions;
none is left unverified
([status table](docs/evidence/damage.md#3-rva-status-table)).

The evaluator's instruction anchors (§6) were each checked against the
disassembly; `0x6BB72E1` replaces an earlier `0x6BB72DE`, which is the
instruction before it.

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
| 2026-10-17 | Traced the projectile-impact path (`0x6B725B0`): the bullet event's starting amount and tags come from the projectile data asset and the firing weapon (§7.6). Added a per-weapon damage table for 33 weapons, generated by `_tools/damage_tables.py` (§7.7). Named more `ModifyDamage` callers; `BP_DamageActor` bypasses the rule tables. |
| 2026-10-17 | Starting amount scales by impact speed and the weapon's distance curve (cm); armor tags are filtered to the piece covering the hit location before `ModifyDamage` (§7.6). Added damage over distance (§7.8). `UNITS.md` corrected: the falloff curve's `Time` is cm, not metres. |
| 2026-10-17 | Closed the cross-check items: `S` is the event amount (`0x6EF8DE0`); the evaluator is skipped for `S ≤ 0`; recording rules; registry/category fallback to `WDGameSettings`; offsets confirmed by runtime reflection (§11); anchor `0x6BB72E1`. |
| 2026-10-17 | Health write traced (§10): `ReceiveDamage` → vitality component → base-value write on `Attribute.Gameplay.Health`; no effect involved. Corrects the earlier note that `SetAttributeBaseValue` is only used by healing (its helper `0x52311D0` had no corpus function entry, so its calls were not indexed). |
| 2026-10-17 | Ammo variants: the modified stats add the ammo-modifier tag and change no damage value (§7.9). Generator gained real armor values and an `--ammo` mode; added the ammo × armor table. |
| 2026-10-17 | Independent verifier pass: corrected the blunt-damage condition (flight time, instance byte `+0x101`), the direct-hit distance-scale evidence, armor filtering (first covering piece only) and the Penetrate/Throughput tags, the exploding-hit and custom-hit paths, the downed-character branch and the order of death handling; noted the four functions without corpus bodies. |
| 2026-10-17 | Another independent verifier pass: `RootDamageTag` is `Meta.Damage` and is never evaluated (§5); corrected two citations that sat on misaligned corpus rows (`0x6EF9450`, `0x6F08CE0`); named the two player-character stubs from their FName initializers and noted that the decay-pool cut runs only for role 3 (§10); every function without a corpus body is listed and reproduced from disassembly; the three IDA notes are merged into [`docs/evidence/damage.md`](docs/evidence/damage.md) (§11). |
| 2026-10-17 | Round-4 verifier pass: character health's hooks clamp through vitality slot 161 (§10); all 17 `ModifyDamage` call sites named (§1.1). |
| 2026-10-17 | Round-5 verifier pass: the projectile's ammo tag (`+0xF0`) is set by `0x6F30E50` from the spawn parameters, built on the fire path by `0x6C98290` (§7.9); the `<type>` rule is only partly decoded. The two back-blast paths are branches of one if/else whose condition is open (O-8). |
