# Wardogs — Damage Pipeline, Data and SDK Map (v1)

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Map of exported damage configuration, generated SDK interfaces and a
bounded [native damage trace](docs/DAMAGE_IDA_RESTORED.md). The evaluator's
arithmetic and ordering within target-tag groups are established. Ordering
between groups, custom helper bodies, final health application and network
authority remain unverified. The [IDA trace brief](docs/DAMAGE_IDA_TRACE.md)
tracks the remaining implementation questions.

Build: `++Wardogs+Live-CL-516586` · Engine: UE 5.7 · GAS fork: "BH"
(Embark's internal GAS variant)

---

## TL;DR

The infantry table contains **146 configured entries**, including
requirement filters, literal amounts, and custom-operation references:

| Exported entry kind | Count |
|---|---:|
| Custom operation, `Percentage_Ongoing` | 12 |
| Non-custom, `Percentage_Ongoing` | 74 |
| Non-custom, `None` | 60 |

The 12 custom entries reference **five distinct classes**, including
`WDDamageModificationOperation_PlayerArmorDurability` (§2). They are not
evidence that every hit executes a four-step chain.

All 146 entries have serialized `PriorityIndex = -1`. The native collector
replaces that value with the category's array index and sorts each
target-tag group by ascending priority; ties have no stable-order guarantee.
Non-custom `Percentage_Ongoing` adds `Amount * 0.01 * current`; custom
operations return an additive delta (§7.1–7.2). Their individual bodies
and ordering between groups remain to be traced.

## 1. The data flow struct (`FWDModifyDamageData`)

The custom-operation interface accepts this struct. Defined in
[`sdk/raw/WDGame_structs.hpp`](sdk/raw/WDGame_structs.hpp#L4646)
at line 4646:

```cpp
struct FWDModifyDamageData final {
    float Amount;                            // 0x00 — evaluator starting amount
    uint8 Pad_4[0x4];                        // 0x04
    FWDDamageEventEntityData InstigatorEventData;  // 0x08 — event-time instigator info
    FWDDamageEntityData      InstigatorEntityData; // 0x18 — who caused damage (0x30 bytes)
    FWDDamageEventEntityData TargetEventData;      // 0x48
    FWDDamageEntityData      TargetEntityData;     // 0x58 — who was hit (0x30 bytes)
    FWDDamageEntityData      SourceEntityData;     // 0x88 — source entity (0x30 bytes)
    EWDDamageAlignment       Alignment;            // 0xB8 — None / Neutral / Hostile / Friendly
    uint8 Pad_B9[0x3];
    FGameplayTag             HitLocation;          // 0xBC — e.g., Meta.Damage.HitLocation.Infantry.Head
    uint8 Pad_C4[0x4];                       // total size 0xC8
};
```

**Available inputs and investigation leads:**

| Modifier | Candidate inputs to inspect; reads not established by the SDK |
|---|---|
| `AmmoTypeEffectiveness` | Source/target entity context and ammo tags |
| `ArchetypeCaliberModifiers` | Source context and archetype/caliber row selection |
| `BoneDamageModifiers` | Hit-location tag and archetype/fallback row selection |
| `VehicleSeatDamageReduction` | Target context and vehicle-variant/state-tag lookup |
| `PlayerArmorDurability` | Armor/helmet context and durability inputs |

## 2. The modifier base class (`UWDCustomDamageModificationOperation`)

Defined in [`sdk/raw/WDGame_classes.hpp`](sdk/raw/WDGame_classes.hpp#L36507)
at line 36507:

```cpp
class UWDCustomDamageModificationOperation : public UObject {
public:
    float GetModificationAmount(
        const FWDModifyDamageData& ModifyDamageData,
        const float _aaabddjaiakieibfbondk  // current running damage; native caller verified
    ) const;
};
```

**Five custom-operation classes referenced by the infantry row:**

| SDK class | Infantry array indexes (zero-based) | Declaration |
|---|---|---|
| `UB_BoneDamageModifiers_C` | 5, 7, 10 | [`B_BoneDamageModifiers_classes.hpp`](sdk/raw/B_BoneDamageModifiers_classes.hpp) |
| `UB_ArchetypeCaliberModifiers_C` | 6 | [`B_ArchetypeCaliberModifiers_classes.hpp`](sdk/raw/B_ArchetypeCaliberModifiers_classes.hpp) |
| `UB_AmmoTypeEffectiveness_C` | 138, 139, 140, 141 | [`B_AmmoTypeEffectiveness_classes.hpp`](sdk/raw/B_AmmoTypeEffectiveness_classes.hpp) |
| `UWDDamageModificationOperation_PlayerArmorDurability` | 142, 143, 144 | [`WDGame_classes.hpp`](sdk/raw/WDGame_classes.hpp#L36557) |
| `UB_VehicleSeatDamageReduction_C` | 145 | [`B_VehicleSeatDamageReduction_classes.hpp`](sdk/raw/B_VehicleSeatDamageReduction_classes.hpp) |

The native evaluator adds the returned `float` as a damage delta, passing
the original input struct and current running damage separately. It does
not additionally apply the custom entry's literal amount or enum. The generated
Blueprint function files call `ProcessEvent`; they do not contain the
modifier implementations. Only the archetype and bone subclass declarations
above expose a `DataTable` field. A table binding must not be invented for
the other classes from their names or inheritance.

## 3. The infantry rule table (`DT_GlobalDamage_InfantryData`)

Row struct: `FWDDamageableEntityTableRow` (defined in `WDGame`).

**Location in repo:**
[`data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json)

**Row key:** `Meta.Damage.Infantry`

**Each entry in `DamageModificationEntries` is a `FWDDamageModificationEntry`:**

```json
{
  "InstigatorRequirements": [],       // exported requirement containers
  "TargetRequirements": [],
  "SourceRequirements": [],
  "AlignmentRequired": "EWDDamageAlignment::None",
  "PossibleHitLocations": [],         // Filter by hit location tags
  "OutModification": {
    "bUseCustomOperation": true/false,
    "Operation": "EWDDamageModificationOperation::Percentage_Ongoing",
    "Amount": <float>,                // custom/literal interaction unverified
    "CustomOperationClass": <class reference or null>,
    "PriorityCategory": { "TagName": "None" },
    "PriorityIndex": -1,
    "DebugTargetTag": { "TagName": "None" }
  },
  "DebugTargetTag": { "TagName": "None" }
}
```

This is a schematic with comments/placeholders, not literal JSON. The
actual array has 146 entries and eight distinct non-`None` priority-category
tags, plus `None`. Its 12 custom references repeat classes under different
requirements. For example, entries 138–141 reference the ammo-effectiveness
class under armor/helmet and bullet/cannon requirements. The requirement
matching algorithm itself is unverified.

The separate categories asset lists 12 category tags. Its list order is
an input to investigate, not proof of execution order. All 60 `None`
entries have empty requirements/hit locations, no custom class, amount
0.0, and default category/index. Their intended purpose is not established;
they must not be described as reserved runtime-injection slots.

## 4. Exported helper values (application unverified)

### 4.1 BoneDamageModifiers (hit-location table)

From
[`DT_Helpers/DT_InfantryData_BoneDamageModifiers.json`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_BoneDamageModifiers.json),
row key `Universal`:

| Hit location (GameplayTag) | Exported value |
|---|---:|
| `Meta.Damage.HitLocation.Infantry.Head` | **1.00** |
| `Meta.Damage.HitLocation.Infantry.Neck` | 0.75 |
| `Meta.Damage.HitLocation.Infantry.Torso.Upper` | 1.10 |
| `Meta.Damage.HitLocation.Infantry.Torso.Middle` | 1.00 |
| `Meta.Damage.HitLocation.Infantry.Torso.Lower` | 0.95 |
| `Meta.Damage.HitLocation.Infantry.Pelvis` | 0.90 |
| `Meta.Damage.HitLocation.Infantry.Arm.Upper` | 0.60 |
| `Meta.Damage.HitLocation.Infantry.Arm.Lower` | 0.50 |
| `Meta.Damage.HitLocation.Infantry.Arm.Hand` | 0.30 |
| `Meta.Damage.HitLocation.Infantry.Leg.Thigh` | 0.60 |
| `Meta.Damage.HitLocation.Infantry.Leg.Calf` | 0.50 |
| `Meta.Damage.HitLocation.Infantry.Leg.Foot` | 0.30 |

That is the complete 12-location `Universal` row. The same exported
table has **20 rows**, including weapon-archetype rows. Every row has 12
hit-location entries. Representative head values are:

| Row | Exported head value |
|---|---:|
| `Universal` | 1.0 |
| `Meta.Damage.Weapon.AR` | 2.35 |
| `Meta.Damage.Weapon.SMG` | 2.1 |
| `Meta.Damage.Weapon.LMG` | 2.35 |
| `Meta.Damage.Weapon.Shotgun` | 1.5 |
| `Meta.Damage.Weapon.DMR` | 2.45 |
| `Meta.Damage.Weapon.Sniper` | 4.2667 |

The full row roster and remaining values are in the linked export.
Archetype-specific data is therefore already available. What remains
unknown is how the consumer chooses a row, whether/how `Universal` is a
fallback, and how the selected value enters an operation. The Universal
head value alone cannot establish a final headshot multiplier.

### 4.2 ArchetypeCaliberModifiers (weapon-type × caliber table)

From
[`DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json):

Keyed by weapon archetype tag (`Meta.Damage.Weapon.AR`,
`Meta.Damage.Weapon.DMR`, etc.), inner map is caliber → multiplier.

**Assault Rifle (`Meta.Damage.Weapon.AR`):**

| Caliber | Exported value |
|---|---:|
| `Bullet.556mm` | 1.00 |
| `Bullet.545mm` | 1.00 |
| `Bullet.308Win` | 0.75 |
| `Bullet.762mm` | 0.88 |

**Designated Marksman Rifle (`Meta.Damage.Weapon.DMR`):**

| Caliber | Exported value |
|---|---:|
| `Bullet.308Win` | 0.85 |
| `Bullet.762mm` | 1.00 |
| ... | |

The tables above shorten `Meta.Damage.Bullet.*` tags to `Bullet.*`.
These are exported archetype/caliber values. Their selection and arithmetic
have not been traced; the data does not establish a design rationale or
final relative damage for weapons using those calibers.

### 4.3 AmmoTypeEffectivenessPen (ammo type table)

From
[`DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json).
There are six rows, including FMJ. Their explicit `Modifier` values are:

| Row suffix under `Meta.Damage.AmmoModifier.*` | `Modifier` |
|---|---:|
| `FMJ` | 1.0 |
| `Tracer` | 1.0 |
| `HollowPoint` | 1.5 |
| `HollowPoint.Tracer` | 1.5 |
| `ArmorPiercing` | 0.3 |
| `ArmorPiercing.Tracer` | 0.3 |

The two ArmorPiercing rows also have an opaque-keyed map with
`Meta.Damage.Arms.Small` 0.7, `Medium` 0.6, `High` 0.5, and `Special` 1.0.
This is not a per-caliber map. Binding this helper table to a specific
custom operation and interpreting how `Modifier` combines with that map
still require consumer evidence.

**Related ammo DataAssets** in
[`data/Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers/`](data/Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers/):

- `DA_AmmoModifier_ArmorPiercing.json`
- `DA_AmmoModifier_HollowPoint.json`
- `DA_AmmoModifier_Tracer.json`
- `DA_AmmoModifier_ArmorPiercing_Tracer.json`
- `DA_AmmoModifier_HollowPoint_Tracer.json`

### 4.4 VehicleSeatDamageReduction (occupant protection table)

The [existing seat-reduction export](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json)
has **11 vehicle-variant rows**, with grouped arm tags
and values keyed by `State.Player.Vehicle.SeatDamageReduction`. It is not
an explicit Driver/Gunner/Passenger table. Below, variant names omit the
common `Vehicle.Variant.` prefix; column names omit `Meta.Damage.Arms.`.

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

These are raw numbers from opaque-keyed groups; `—` means no such group
is exported, not zero. Their interpretation as a percentage, multiplier,
or adjustment is unverified, as are missing-row behavior and the actual
vehicle-state lookup.

## 5. The companion global tables

| Table | Row struct | Purpose |
|---|---|---|
| [`DT_GlobalDamage_InfantryData`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json) | `FWDDamageableEntityTableRow` | Configured infantry rules |
| [`DT_GlobalDamage_VehicleData`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_VehicleData.json) | `FWDDamageableEntityTableRow` | Configured vehicle rules; consumer not traced here |
| [`DT_GlobalDamage_ArmorData`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_ArmorData.json) | `FWDDamageableEntityTableRow` | Four armor/helmet rule rows |
| [`DA_GlobalDamage_Categories`](data/Wardogs/Content/GameMechanics/DamageSystem/DA_GlobalDamage_Categories.json) | (DataAsset) | Damage category tag definitions |
| [`DA_GlobalDamage_HitLocations_Player`](data/Wardogs/Content/GameMechanics/DamageSystem/HitLocationDataAssets/DA_GlobalDamage_HitLocations_Player.json) | (DataAsset) | Hit-location tag catalog + bone mapping |
| [`DT_AmmoModifiers`](data/Wardogs/Content/GameMechanics/DamageSystem/DT_AmmoModifiers.json) | `FWDAmmoModifierTableRow` | Five ammo-tag-to-data-asset rows |

## 6. Candidate trace: an AR/5.45 mm upper-torso hit

This example identifies questions for static analysis; it does not
calculate verified final damage.

1. The archetype/caliber table has `Meta.Damage.Weapon.AR` with
   `Meta.Damage.Bullet.545mm` value 1.0.
2. The bone table has upper-torso value 1.10 in `Universal`, but 0.885
   in `Meta.Damage.Weapon.AR`. The consumer's row-selection/fallback
   algorithm must be established before choosing either value.
3. The infantry table contains literal and custom rules with source,
   target, alignment, hit-location, and category fields. Native filtering,
   per-group ordering and evaluator arithmetic are now established (§7.1–7.2);
   the complete selected sequence and helper outputs for this hit remain open.
4. The SDK exposes [`UWDDamageSubsystem::ModifyDamage`](sdk/raw/WDGame_classes.hpp#L44447)
   and [`UWDGlobalDamageSystem`](sdk/raw/WDGame_classes.hpp#L36482).
   The restored native trace connects the subsystem to its selected
   damage-system evaluator and the global evaluator to collected modifiers.
   It does not connect that result to final health application.
5. `BHHitValidationWorldSubsystem` and `BHGameplayEffectComponent::ApplyEffect`
   are declared in the SDK. Their declarations do not establish an edge
   into this calculation, the health effect used, or network authority.

The earlier `baseDamage × 1.10` example depended on unverified row
selection and aggregation assumptions and has been withdrawn.

## 7. Still Not Pulled / Open Questions

### 7.1 Order of modifier evaluation (NATIVE TRACE; PARTIAL)

The [restored-input trace](docs/DAMAGE_IDA_RESTORED.md) recovered the
global collector and evaluator. Each row retains all eligible matching
entries. All required instigator/target/source tags must match explicit
or parent tags; alignment is optional, and populated hit-location
requirements need at least one match.

The collector replaces each copied `PriorityIndex` with the category's
zero-based position in `DamageCategories`; missing categories yield -1.
Each target-tag group is sorted by ascending signed priority, with no
stable-order guarantee for ties. This establishes category order within
a group, not a single global category sort. Registry fallback, hierarchy
traversal and ordering between groups remain open under B-1.

### 7.2 Operation arithmetic and custom return values (NATIVE CONTRACT VERIFIED)

Let S be `ModifyDamageData.Amount` on entry and initialize C = S.
The native evaluator applies selected modifications as follows:

| Operation | Update |
|---|---|
| Non-custom `None` / unrecognized | No change |
| Non-custom `Percentage_Starting` | `C += (Amount * 0.01f) * S` |
| Non-custom `Percentage_Ongoing` | `C += (Amount * 0.01f) * C` |
| Non-custom `Add` | `C += Amount` |
| Custom | `C += GetModificationAmount(originalData, C)` |

Custom entries bypass the literal amount/enum arithmetic. Their individual
bodies remain open; raw bone/seat helper values cannot yet be substituted
for returned deltas. The nonempty-collection path clamps C to at least
zero after all groups; the empty-collection path returns S directly.

The collector skips entries with empty requirement/hit arrays and literal
amount zero, including the 60 empty `None` entries. A selected non-custom
ongoing amount of zero adds zero; entries with requirements are not skipped
solely because their amount is zero. See the [evidence report](docs/DAMAGE_IDA_RESTORED.md)
for method locations, instruction anchors, recording thresholds and limits.

### 7.3 Bone row selection and per-weapon overrides (PARTIAL)

Existing archetype rows are established by the export (§4.1), including
AR and Sniper. The earlier claim that overrides must live elsewhere was
unsupported. **B-3** traces the row key, fallback, tag hierarchy, and
application of the chosen values. This audit does not establish whether
additional per-weapon override mechanisms exist; that is a separate
question rather than an assumed explanation for `Universal.Head = 1.0`.

### 7.4 BoneDamageModifiers coverage (DATA ENUMERATED)

Section 4.1 now enumerates all 12 Universal locations using their actual
exported tags, including `Leg.Thigh`, `Leg.Calf`, and `Leg.Foot`. The
existing JSON contains all 20 rows (240 location/value pairs). A re-parse
is not required for this coverage question. Runtime selection and
application remain open under §7.3; data enumeration does not resolve them.

### 7.5 Ammo-effectiveness table binding and return semantics (OPEN)

The `Pen` helper contains six rows and the values summarized in §4.3.
The infantry row references `B_AmmoTypeEffectiveness_C` under explicit
armor/helmet requirements. The helper filename and class name do not
establish their binding, a second "vanilla" operation, or stacking.
**B-4** traces the binding, row selection, and returned quantity before
§7.2 can interpret it. Declarations alone are insufficient.

### 7.6 VehicleSeatDamageReduction values (DATA ENUMERATED; CONSUMER OPEN)

Section 4.4 now enumerates all 11 variant rows from the existing export.
No additional extraction is required to list those values. **B-4** still
needs to establish row/group lookup, missing-row handling, the meaning
of the state-tag numbers, and the custom return value. Driver/gunner
exposure assumptions are not a substitute for those checks.

### 7.7 Network authority and health application (UNRESOLVED)

The available SDK declarations do not establish server-only execution,
input validation, or the final health-write path. The native trace covers
client-side calculation only; no runtime session was used. Any security-relevant
findings arising from that investigation must be tracked privately and
routed through [`SECURITY.md`](SECURITY.md). No server-authority guarantee
or vulnerability is claimed by this document.

## 8. Cross-references

### SDK files cited
- [`sdk/raw/WDGame_classes.hpp`](sdk/raw/WDGame_classes.hpp) (line 36507 — base class)
- [`sdk/raw/WDGame_structs.hpp`](sdk/raw/WDGame_structs.hpp) (line 4646 — data struct; lines 4870, 4887, 5109, 8461, 11152, 11175, 11205, 15410 — supporting structs)
- [`sdk/raw/B_AmmoTypeEffectiveness_classes.hpp`](sdk/raw/B_AmmoTypeEffectiveness_classes.hpp)
- [`sdk/raw/B_ArchetypeCaliberModifiers_classes.hpp`](sdk/raw/B_ArchetypeCaliberModifiers_classes.hpp)
- [`sdk/raw/B_BoneDamageModifiers_classes.hpp`](sdk/raw/B_BoneDamageModifiers_classes.hpp)
- [`sdk/raw/B_VehicleSeatDamageReduction_classes.hpp`](sdk/raw/B_VehicleSeatDamageReduction_classes.hpp)
- [`sdk/raw/WDGame_functions.cpp`](sdk/raw/WDGame_functions.cpp#L48948) — generated `ModifyDamage` wrapper, not its native implementation
- [`sdk/raw/BHGameplayEffects_classes.hpp`](sdk/raw/BHGameplayEffects_classes.hpp)
- [`sdk/raw/BHHitValidation_classes.hpp`](sdk/raw/BHHitValidation_classes.hpp)

### Data files cited
- `data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json`
- `data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_BoneDamageModifiers.json`
- `data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json`
- `data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json`
- `data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json`
- `data/Wardogs/Content/GameMechanics/DamageSystem/DA_GlobalDamage_Categories.json`
- `data/Wardogs/Content/GameMechanics/DamageSystem/DT_AmmoModifiers.json`
- `data/Wardogs/Content/GameMechanics/DamageSystem/HitLocationDataAssets/DA_GlobalDamage_HitLocations_Player.json`

### Related reference docs
- [`Wardogs_InfantryWeapons_Stats_v1.md`](Wardogs_InfantryWeapons_Stats_v1.md) — per-weapon base damage values
- [`Wardogs_GameMechanics_v2.md`](Wardogs_GameMechanics_v2.md) — broader gameplay framework context
- [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) — RE methodology used to produce this doc
- [`docs/DAMAGE_IDA_TRACE.md`](docs/DAMAGE_IDA_TRACE.md) — audited inputs and bounded IDA trace targets B-1 through B-4
- [`docs/DAMAGE_IDA_RESULTS.md`](docs/DAMAGE_IDA_RESULTS.md) — offline input-validation evidence and the remaining implementation boundary
- [`docs/DAMAGE_IDA_RESTORED.md`](docs/DAMAGE_IDA_RESTORED.md) — restored-input native evaluator, matching and per-group ordering evidence

## Change log

| Date | Change |
|---|---|
| 2026-10-16 | v1 — Initial SDK/data map. SDK committed at commit [`c65e83d`](https://github.com/Kiyogitpy/wardogs-data-docs/commit/c65e83d). |
| 2026-10-17 | Evidence audit — corrected rule/class counts and unsupported execution/authority claims; enumerated existing Universal and vehicle-variant values; prepared the IDA trace brief. Native behavior remains unverified. |
| 2026-10-17 | IDA input-validation pass — decoded mapping v2 and checked the reconstructed PE/recorded capture. Damage consumer and operation implementation unavailable in inspected inputs; §7.1–7.2 remain open. |
| 2026-10-17 | Restored executable — recovered native matching, category-priority replacement, per-group sorting and operation/custom-delta arithmetic. §7.1 partial; §7.2 evaluator contract verified. Blueprint bodies and final application remain open. |
