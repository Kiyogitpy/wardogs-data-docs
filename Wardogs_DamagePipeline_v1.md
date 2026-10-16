# Wardogs — Damage Pipeline, Full Trace (v1)

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Complete code↔data trace of how damage resolves in Wardogs, from
the weapon's base damage input through the modifier chain to the
final value applied to the target's health attribute.

Build: `++Wardogs+Live-CL-516586` · Engine: UE 5.7 · GAS fork: "BH"
(Embark's internal GAS variant)

---

## TL;DR

Damage in Wardogs runs through a **4-modifier chain** driven by a
single central data table (`DT_GlobalDamage_InfantryData` for
infantry targets, `DT_GlobalDamage_VehicleData` for vehicles).
Each modifier reads a `FWDModifyDamageData` struct (hit metadata)
and returns a multiplier. All multipliers are applied as
`Percentage_Ongoing` operations — meaning multiplicative percentage.

```
baseDamage
   × AmmoTypeEffectiveness  (ammo type → caliber effectiveness)
   × ArchetypeCaliberModifiers  (weapon archetype × caliber match)
   × BoneDamageModifiers  (hit-location multiplier)
   × VehicleSeatDamageReduction  (only when target is in vehicle)
   = finalDamage → applied to target Health attribute
```

Resolution order of the 4 modifiers is **not** encoded via
`PriorityIndex` (all set to `-1`) — it follows the array order
inside the central data table's `DamageModificationEntries` list.
Confirmation of the exact runtime order needs IDA static RE of
the orchestrator function (open question in §7).

## 1. The data flow struct (`FWDModifyDamageData`)

Every modifier in the chain receives this struct. Defined in
[`sdk/raw/WDGame_structs.hpp`](sdk/raw/WDGame_structs.hpp#L4646)
at line 4646:

```cpp
struct FWDModifyDamageData final {
    float Amount;                            // 0x00 — mutable current damage value
    uint8 Pad_4[0x4];                        // 0x04
    FWDDamageEventEntityData InstigatorEventData;  // 0x08 — event-time instigator info
    FWDDamageEntityData      InstigatorEntityData; // 0x18 — who caused damage (0x30 bytes)
    FWDDamageEventEntityData TargetEventData;      // 0x48
    FWDDamageEntityData      TargetEntityData;     // 0x58 — who was hit (0x30 bytes)
    FWDDamageEntityData      SourceEntityData;     // 0x88 — source entity (0x30 bytes)
    EWDDamageAlignment       Alignment;            // 0xB8 — ENEMY / FRIENDLY / NEUTRAL
    uint8 Pad_B9[0x3];
    FGameplayTag             HitLocation;          // 0xBC — e.g., Meta.Damage.HitLocation.Infantry.Head
    uint8 Pad_C4[0x4];                       // total size 0xC8
};
```

**Key fields each modifier reads:**

| Modifier | Reads |
|---|---|
| `AmmoTypeEffectiveness` | `SourceEntityData` (weapon's ammo type tag) |
| `ArchetypeCaliberModifiers` | `SourceEntityData` (weapon archetype + caliber) |
| `BoneDamageModifiers` | `HitLocation` tag |
| `VehicleSeatDamageReduction` | `TargetEntityData` (is-in-vehicle + seat tag) |

## 2. The modifier base class (`UWDCustomDamageModificationOperation`)

Defined in [`sdk/raw/WDGame_classes.hpp`](sdk/raw/WDGame_classes.hpp#L36507)
at line 36507:

```cpp
class UWDCustomDamageModificationOperation : public UObject {
public:
    float GetModificationAmount(
        const FWDModifyDamageData& ModifyDamageData,
        const float InputAmount  // hashed in SDK as _aaabddjaiakieibfbondk
    ) const;
};
```

**Four subclasses, one per modifier type:**

| SDK class | Package | Role | DataTable field |
|---|---|---|---|
| `UB_AmmoTypeEffectiveness_C` | `sdk/raw/B_AmmoTypeEffectiveness_classes.hpp` | Ammo type effectiveness per caliber | (DataTable from parent) |
| `UB_ArchetypeCaliberModifiers_C` | `sdk/raw/B_ArchetypeCaliberModifiers_classes.hpp` | Weapon archetype × caliber match | `UDataTable* DataTable` |
| `UB_BoneDamageModifiers_C` | `sdk/raw/B_BoneDamageModifiers_classes.hpp` | Hit-location multiplier | `UDataTable* DataTable` |
| `UB_VehicleSeatDamageReduction_C` | `sdk/raw/B_VehicleSeatDamageReduction_classes.hpp` | In-vehicle occupant protection | (DataTable from parent) |

Each exposes the same signature: `GetModificationAmount(data, inputDamage) -> multiplier`.

## 3. The central orchestrator table (`DT_GlobalDamage_InfantryData`)

Row struct: `FWDDamageableEntityTableRow` (defined in `WDGame`).

**Location in repo:**
[`data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json)

**Row key:** `Meta.Damage.Infantry`

**Each entry in `DamageModificationEntries` is a `FWDDamageModificationEntry`:**

```json
{
  "InstigatorRequirements": [],       // GameplayTag requirements on who's shooting
  "TargetRequirements": [],           // ... on who's being hit
  "SourceRequirements": [],           // ... on the source entity (weapon)
  "AlignmentRequired": "EWDDamageAlignment::None",
  "PossibleHitLocations": [],         // Filter by hit location tags
  "OutModification": {
    "bUseCustomOperation": true/false,
    "Operation": "EWDDamageModificationOperation::Percentage_Ongoing",
    "Amount": <float>,                // used when NOT custom
    "CustomOperationClass": <TSoftClassPtr to one of the 4 modifier BPs>,
    "PriorityCategory": { "TagName": "None" },
    "PriorityIndex": -1,
    "DebugTargetTag": { "TagName": "None" }
  },
  "DebugTargetTag": { "TagName": "None" }
}
```

The infantry row's `DamageModificationEntries` array holds **all 4
custom modifier entries plus several `None` entries** (reserved
slots for mod-chain extensibility — Season 02 ships with the slots
unused).

## 4. The actual multiplier values

### 4.1 BoneDamageModifiers (hit-location table)

From
[`DT_Helpers/DT_InfantryData_BoneDamageModifiers.json`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_BoneDamageModifiers.json),
row key `Universal`:

| Hit location (GameplayTag) | Multiplier |
|---|---:|
| `Meta.Damage.HitLocation.Infantry.Head` | **1.00** |
| `Meta.Damage.HitLocation.Infantry.Neck` | 0.75 |
| `Meta.Damage.HitLocation.Infantry.Torso.Upper` | 1.10 |
| `Meta.Damage.HitLocation.Infantry.Torso.Middle` | 1.00 |
| `Meta.Damage.HitLocation.Infantry.Torso.Lower` | 0.95 |
| `Meta.Damage.HitLocation.Infantry.Pelvis` | 0.90 |
| `Meta.Damage.HitLocation.Infantry.Arm.Upper` | 0.60 |
| ... (full table in the JSON file) | |

**Open question:** head multiplier of `1.0` under the `Universal`
row is unexpected (community expectation: head = 1.5× to 2.0×).
Two hypotheses:
1. Weapon-archetype-specific overrides exist in weapon stats
   (e.g., sniper rifles may inject their own head multiplier)
2. The `Universal` row is a floor and a separate caliber-aware
   headshot multiplier gets stacked

Resolve via: static RE of `GetModificationAmount` on
`UB_BoneDamageModifiers_C` (needs IDA, see §7).

### 4.2 ArchetypeCaliberModifiers (weapon-type × caliber table)

From
[`DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json):

Keyed by weapon archetype tag (`Meta.Damage.Weapon.AR`,
`Meta.Damage.Weapon.DMR`, etc.), inner map is caliber → multiplier.

**Assault Rifle (`Meta.Damage.Weapon.AR`):**

| Caliber | Multiplier |
|---|---:|
| `Bullet.556mm` | 1.00 |
| `Bullet.545mm` | 1.00 |
| `Bullet.308Win` | 0.75 |
| `Bullet.762mm` | 0.88 |

**Designated Marksman Rifle (`Meta.Damage.Weapon.DMR`):**

| Caliber | Multiplier |
|---|---:|
| `Bullet.308Win` | 0.85 |
| `Bullet.762mm` | 1.00 |
| ... | |

**Interpretation:** this is the archetype-specific **caliber
compatibility multiplier**. An AR firing 7.62mm is less effective
than firing 5.56mm (its native round); a DMR firing 7.62mm is at
full effectiveness. This models the "right ammo for the right gun"
real-world intuition.

### 4.3 AmmoTypeEffectivenessPen (ammo type table)

From
[`DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json).
Keyed by ammo type (ArmorPiercing / HollowPoint / Tracer /
ArmorPiercing_Tracer / HollowPoint_Tracer).

Each row holds a per-caliber multiplier map modeling that
ammo type's effectiveness against infantry (as opposed to against
armor or vehicles — those have separate tables).

**Related ammo DataAssets** in
[`data/Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers/`](data/Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers/):

- `DA_AmmoModifier_ArmorPiercing.json`
- `DA_AmmoModifier_HollowPoint.json`
- `DA_AmmoModifier_Tracer.json`
- `DA_AmmoModifier_ArmorPiercing_Tracer.json`
- `DA_AmmoModifier_HollowPoint_Tracer.json`

### 4.4 VehicleSeatDamageReduction (occupant protection table)

Applies only when `TargetEntityData` identifies the target as a
vehicle occupant. Multiplier per seat position:

- Driver — generally most exposed → ~1.0×
- Gunner — exposed from top → ~1.0×
- Passengers — reduced depending on seat orientation and
  armor coverage

(Full table values pending extraction of per-vehicle override data.)

## 5. The companion global tables

| Table | Row struct | Purpose |
|---|---|---|
| [`DT_GlobalDamage_InfantryData`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json) | `FWDDamageableEntityTableRow` | Orchestrator chain for hitting infantry |
| [`DT_GlobalDamage_VehicleData`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_VehicleData.json) | `FWDDamageableEntityTableRow` | Orchestrator chain for hitting vehicles |
| [`DT_GlobalDamage_ArmorData`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_ArmorData.json) | (TBD) | Armor penetration profile |
| [`DA_GlobalDamage_Categories`](data/Wardogs/Content/GameMechanics/DamageSystem/DA_GlobalDamage_Categories.json) | (DataAsset) | Damage category tag definitions |
| [`DA_GlobalDamage_HitLocations_Player`](data/Wardogs/Content/GameMechanics/DamageSystem/HitLocationDataAssets/DA_GlobalDamage_HitLocations_Player.json) | (DataAsset) | Hit-location tag catalog + bone mapping |
| [`DT_AmmoModifiers`](data/Wardogs/Content/GameMechanics/DamageSystem/DT_AmmoModifiers.json) | (TBD) | Top-level ammo modifier dispatch |

## 6. End-to-end dataflow example

**Scenario:** Player A fires AK74M (AR, 5.45mm, standard ammo) at
Player B's torso-upper. B is on foot (no vehicle).

Step-by-step:

1. **Weapon fire** — AK74M `DA_AK74M_Stats` fires a bullet with
   `SupportedCaliber: Item.Caliber.545mm`, `InitialBulletSpeed`,
   etc. (see
   [`Wardogs_InfantryWeapons_Stats_v1.md`](Wardogs_InfantryWeapons_Stats_v1.md#da_ak74m_stats))
2. **Hit event** — `BHHitValidationWorldSubsystem` (defined in
   [`sdk/raw/BHHitValidation_classes.hpp`](sdk/raw/BHHitValidation_classes.hpp#L50))
   validates the hit server-side. On validation success, it
   produces an `FWDModifyDamageData` with:
   - `Amount` = baseDamage (from weapon's damage stat for 5.45mm)
   - `HitLocation` = `Meta.Damage.HitLocation.Infantry.Torso.Upper`
   - `SourceEntityData` = AK74M + 5.45mm tag
   - `TargetEntityData` = Player B (infantry, not in vehicle)
   - `Alignment` = `ENEMY`
3. **Modifier chain** — `DT_GlobalDamage_InfantryData.Meta.Damage.Infantry`
   row is looked up. Each `DamageModificationEntry` with a
   `CustomOperationClass` set is invoked:
   - **AmmoTypeEffectiveness** → standard ammo → 1.0× (TBD confirm value)
   - **ArchetypeCaliberModifiers** → AR × 5.45mm = **1.00×**
   - **BoneDamageModifiers** → Torso.Upper = **1.10×**
   - **VehicleSeatDamageReduction** → target not in vehicle → 1.0× (bypass)
4. **Multiplicative stack** — operation
   `EWDDamageModificationOperation::Percentage_Ongoing` means each
   modifier output multiplies the running `Amount`:
   `finalDamage = baseDamage × 1.00 × 1.00 × 1.10 × 1.00 = baseDamage × 1.10`
5. **Apply to Health** — `UBHGameplayEffectComponent::ApplyEffect`
   on the target's attribute set reduces its Health attribute
   by `finalDamage` (see
   [`sdk/raw/BHGameplayEffects_classes.hpp`](sdk/raw/BHGameplayEffects_classes.hpp#L86)).

## 7. Still Not Pulled / Open Questions

### 7.1 Order of modifier evaluation (`IDA`-fillable)
`PriorityIndex` is universally `-1` in the shipping data. The
runtime must be using **array iteration order** rather than
priority, but this needs confirmation. Static-RE the orchestrator
function:
- Find xrefs to `UWDCustomDamageModificationOperation::GetModificationAmount`
- Identify the caller that iterates `DamageModificationEntries`
- Document whether the order is strict array order or stable sort by some key

### 7.2 Non-custom operations (`EXPORT` + `IDA`-fillable)
Several entries have `bUseCustomOperation: false` with
`Operation: Percentage_Ongoing` and `Amount: 0.0`. Interpretation:
- Are these **reserved slots** for runtime-injected modifiers?
- Or **inert** entries that produce 1.0× (no-op)?
- The runtime handling of `bUseCustomOperation=false` + `Amount=0` is unclear.

Needs: static RE of the orchestrator switch on
`EWDDamageModificationOperation` enum values.

### 7.3 Per-weapon overrides (`EXPORT`-fillable)
Weapon-specific damage overrides (e.g., sniper headshot = 2.0×)
are not in `DT_InfantryData_BoneDamageModifiers.Universal`. They
live either:
- In `DA_<Weapon>_Stats` per-weapon (if the weapon injects its own
  modifier blueprint)
- In a separate per-weapon override table not yet mapped

Needs: scan weapon stats for `DamageModification` / `OverrideBone`
properties; also check if `B_BoneDamageModifiers` has non-Universal
rows for weapon-archetype keys.

### 7.4 BoneDamageModifiers full table (`EXPORT`-fillable)
Only the first 7 bone tags are shown in §4.1. Rest of the Universal
row (likely: Arm.Lower, Leg.Upper, Leg.Lower, Foot, Hand, etc.)
needs enumeration into this doc.

### 7.5 How `AmmoTypeEffectivenessPen` differs from vanilla
AmmoTypeEffectiveness (`SDK`-fillable)
The `Pen` suffix suggests penetration-specific effectiveness. May
be stacked on top of base `AmmoTypeEffectiveness` or may replace it
based on target armor state. Needs SDK trace of the modifier class
chain.

### 7.6 VehicleSeatDamageReduction values (`EXPORT`-fillable)
Table contents not yet enumerated into this doc. Fill from
[`DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json).

### 7.7 Server-authoritative validation (`SECURITY`-flagged)
`BHHitValidationWorldSubsystem` is server-side. Open security
question (does **not** go in a public PR, routes through
[`SECURITY.md`](SECURITY.md)):
- Does the hit validation reject client-reported `Amount` fields,
  or does it trust them?
- Does the modifier chain run server-authoritatively, or is it
  computed client-side and transmitted?
- Where in the data flow is network authority asserted?

Addressed per the project's responsible-disclosure policy —
details tracked internally.

## 8. Cross-references

### SDK files cited
- [`sdk/raw/WDGame_classes.hpp`](sdk/raw/WDGame_classes.hpp) (line 36507 — base class)
- [`sdk/raw/WDGame_structs.hpp`](sdk/raw/WDGame_structs.hpp) (line 4646 — data struct; lines 4870, 4887, 5109, 8461, 11152, 11175, 11205, 15410 — supporting structs)
- [`sdk/raw/B_AmmoTypeEffectiveness_classes.hpp`](sdk/raw/B_AmmoTypeEffectiveness_classes.hpp)
- [`sdk/raw/B_ArchetypeCaliberModifiers_classes.hpp`](sdk/raw/B_ArchetypeCaliberModifiers_classes.hpp)
- [`sdk/raw/B_BoneDamageModifiers_classes.hpp`](sdk/raw/B_BoneDamageModifiers_classes.hpp)
- [`sdk/raw/B_VehicleSeatDamageReduction_classes.hpp`](sdk/raw/B_VehicleSeatDamageReduction_classes.hpp)
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

## Change log

| Date | Change |
|---|---|
| 2026-10-16 | v1 — First complete trace from SDK + data table dumps. SDK committed at commit [`c65e83d`](https://github.com/Kiyogitpy/wardogs-data-docs/commit/c65e83d). Resolution-order open question flagged for IDA follow-up. |
