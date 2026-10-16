# Wardogs — Vehicle Damage Pipeline, Full Trace (v1)

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Complete code↔data trace of how damage resolves against **vehicle
targets** in Wardogs. Companion doc to
[`Wardogs_DamagePipeline_v1.md`](Wardogs_DamagePipeline_v1.md) (infantry
targets) — but the vehicle architecture is **fundamentally different**.

Build: `++Wardogs+Live-CL-516586` · Engine: UE 5.7

---

## TL;DR

Vehicle damage does **NOT** use the infantry-style 5-modifier blueprint
chain. Instead, each vehicle class has its **own damage rule table**
(`DT_GlobalDamage_VehicleData_<CODE>.json`) containing 16–66 individual
rules. Each rule is a **filter + percentage modifier**: match the hit
by source tags (damage type, caliber, hit location), then apply a
multiplicative percentage change.

The modifier chain pattern seen in infantry is absent — zero vehicle
rules use `CustomOperationClass`; all are literal `Percentage_Ongoing`
operations with requirement filters.

**22 per-vehicle DTs ship in Season 02.** Together they define
~500 individual damage rules, organized into **7 priority categories**:
Calibre, Armor, Bone, CaliberEffectiveness, AmmoModifier, Ricochet, Melee.

## 1. Architecture overview

### 1.1 Where the data lives

| Table | Purpose |
|---|---|
| [`DT_GlobalDamage_VehicleData`](data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_VehicleData.json) | **Fallback** table with 1 row `Meta.Damage.Vehicle`, 10 placeholder entries (all zero / none) — the base dispatch when a vehicle hits don't have a per-vehicle override |
| `DT_GlobalDamage_VehicleData_<CODE>.json` | **Per-vehicle override** — one file per vehicle class, one row keyed by that vehicle's gameplay tag |

Per-vehicle DT locations:

```
data/Wardogs/Plugins/GameFeatures/Vehicles/<CODE>/Content/DataTables/
data/Wardogs/Plugins/GameFeatures/Vehicles/<CODE>/Content/DataTable/   (STN_03 only)
```

### 1.2 Row structure

Row key = the vehicle's identity tag:

| Vehicle code | Row key |
|---|---|
| ROT_02 | `Meta.Damage.Vehicle.Air.Rotary.Havoc` |
| ROT_03 | `Meta.Damage.Vehicle.Air.Rotary.<model>` |
| TNK_01 | `Meta.Damage.Vehicle.Ground.Tank.<model>` |
| WHL_05_Humvee | `Meta.Damage.Vehicle.Ground.Wheeled.Humvee` |
| STN_01-06 | `Meta.Damage.Vehicle.Stationary.<model>` |

The row contains a `DamageModificationEntries` list of
`FWDDamageModificationEntry` structs (same type as infantry uses, but
populated differently).

### 1.3 Entry structure

Each entry is a (filter, modifier) rule:

```json
{
  "InstigatorRequirements": [...],   // tags required on the shooter
  "TargetRequirements": [...],       // tags required on the vehicle's state
  "SourceRequirements": [...],       // tags required on the damage source
  "AlignmentRequired": "EWDDamageAlignment::None",
  "PossibleHitLocations": [...],     // which hit locations trigger
  "OutModification": {
    "bUseCustomOperation": false,    // zero vehicles use custom ops
    "Operation": "Percentage_Ongoing",
    "Amount": <float>,               // percentage change (positive = amp, negative = reduce)
    "PriorityCategory": {
      "TagName": "Meta.Damage.Category.<Category>"
    },
    "PriorityIndex": -1              // not used; array order wins
  }
}
```

**Reading the Amount:**
- `-95` → damage reduced to **5%** of input
- `-50` → damage reduced to **50%**
- `0` → no change
- `+200` → damage amplified to **300%**
- `+400` → damage amplified to **500%**

Equivalent: `finalAmount = inputAmount × (1 + Amount/100)`.

## 2. The 7 priority categories

Rules group into these categories (from an aggregation across all 22
vehicle DTs — 531 total rules):

| Category | Count | Role |
|---|---:|---|
| `Calibre` | 299 | Specific caliber/weapon-type modifiers (bullets, cannon rounds, specific rocket types) |
| `Armor` | 104 | Armor-class damage reduction (broad damage-type reductions) |
| `Bone` | 44 | Hit-location modifiers (same as infantry's bone system) |
| `CaliberEffectiveness` | 30 | Caliber-vs-vehicle effectiveness scaling |
| `AmmoModifier` | 23 | Ammo-type modifiers (AP/HE/HP effectiveness per vehicle) |
| `Ricochet` | 16 | Ricochet handling for angled hits |
| `Melee` | 10 | Melee damage against vehicles |

The categories control grouping/precedence — the actual execution order
is a §7 open question deferred to IDA RE (same as infantry's §7.1).

## 3. Vehicle inventory and damage profile summary

All 22 vehicles with their rule count and amount range:

| Code | Entries | Amount range | Notes |
|---|---:|:---|---|
| ROT_02 | 26 | `[-95%, +450%]` | Attack helicopter (Havoc) |
| ROT_03 | 24 | `[-95%, +500%]` | Attack helicopter variant |
| ROT_04 | 23 | `[-95%, +450%]` | Transport helicopter |
| SPW_01 | 24 | `[-100%, +500%]` | Spawn point / support |
| STN_01 | 18 | `[-100%, +1500%]` | Stationary emplacement — large weak-spot amp |
| STN_02 | 18 | `[-100%, +2000%]` | Stationary emplacement — max weak-spot amp |
| STN_03 | 18 | `[-100%, +1000%]` | Stationary emplacement |
| STN_04 | 23 | `[-95%, +250%]` | Stationary — different profile |
| STN_05 | 18 | `[-100%, +1000%]` | Stationary emplacement |
| STN_06 | 18 | `[-100%, +1000%]` | Stationary emplacement |
| TNK_01 | **66** | `[-100%, +500%]` | Tank — most-detailed profile (66 rules) |
| TNK_04 | 23 | `[-100%, +450%]` | Tank variant |
| WHL_01 | 16 | `[-95%, +500%]` | Wheeled vehicle — simplest (16 rules) |
| WHL_02 | 23 | `[-95%, +700%]` | Wheeled |
| WHL_05_Humvee | 28 | `[-95%, +500%]` | Humvee base |
| WHL_05_Minigun | 28 | `[-98%, +800%]` | Humvee minigun variant |
| WHL_05_RingTurret | 28 | `[-96%, +650%]` | Humvee ring turret variant |
| WHL_06_DuneBuggy | 26 | `[-95%, +500%]` | Dune buggy |
| WHL_07_Ural | 27 | `[-95%, +500%]` | Ural truck |
| WHL_08 | 28 | `[-95%, +600%]` | Wheeled |
| WHL_08_RingTurret | 28 | `[-96%, +600%]` | Wheeled turret variant |

## 4. Worked example — ROT_02 Havoc (26 rules)

Full damage profile for the Havoc attack helicopter. Rules execute in
array order (per §7.1 of the infantry doc — same resolution-order
assumption applies). Each row is: category / source-tag filter →
Amount.

| # | Category | Source filter | Amount | Interpretation |
|---|---|---|---:|---|
| 1 | Armor | `Meta.Damage.Bullet` | **-95%** | Heavy armor vs any bullet |
| 2 | Armor | `Meta.Damage.Cannon` | **-70%** | Resistant to any cannon round |
| 3 | Calibre | `Explosive.Rocket` + `Radius.Inner` | **+400%** | **5x damage** on inner-radius rocket hit |
| 4 | Calibre | `Explosive.Grenade` + `Radius.Inner` | -20% | Grenade splash resistance |
| 5 | Armor | `Bullet.308Win` | -70% | .308Win-specific override (less reduced than base bullet) |
| 6 | Calibre | `Explosive.Utility.ATMine` | **+200%** | **3x damage** on AT mine |
| 7 | Armor | `Explosive.Utility.C4` | -15% | Light C4 resistance |
| 8 | Armor | `Explosive.Utility.IED` | +45% | IED amplification |
| 9 | Armor | `Explosive.Utility.Claymore` | -75% | Claymore ineffective |
| 10 | Calibre | `Cannon.30mm` | -35% | 30mm cannon less effective |
| 11 | Calibre | `Cannon.35x228mm` | -46% | 35mm less effective |
| 12 | Calibre | `Explosive.Rocket.72mm` | -60% | Small rocket less effective |
| 13 | Calibre | `Explosive.Rocket.93mm` | -30% | 93mm partial reduction |
| 14 | Calibre | `Explosive.Rocket.93mm` | -45% | **Second 93mm entry** — stacks or overrides? (§7 open) |
| 15 | Calibre | `Explosive.Rocket.120x800mm` | -10% | Large tank rocket slight reduction |
| 16 | Calibre | `Explosive.Rocket.84mm` | +30% | 84mm amplification |
| 17 | Calibre | `Explosive.Rocket.84mm` | -5% | **Second 84mm entry** — stacks or overrides? |
| 18 | Calibre | `Explosive.Rocket.120mm` | **+150%** | **2.5x** on 120mm rocket |
| 19 | Calibre | `Cannon.20x102mm` | -76% | 20mm cannon weak |
| 20 | Calibre | `Explosive.Rocket.122mm` | -85% | 122mm rocket weirdly weak (data check candidate) |
| 21 | Calibre | `Explosive.Grenade.40mm` | -30% | 40mm GL reduction |
| 22 | Calibre | `Explosive.Rocket` | +50% | Generic rocket amplification |
| 23 | **Bone** | `Meta.Damage.Bullet` | **+300%** | **4x damage** on specific hit location (likely crewseats/windshield) |
| 24 | **Bone** | `Meta.Damage.Bullet` | -50% | Second bone rule for bullets, reduction (likely armor-plated section) |
| 25 | Calibre | `Explosive.Drone` | **+450%** | **5.5x** on kamikaze drone — biggest amplifier |
| 26 | Calibre | `Explosive.Rocket.125mm` | +150% | 125mm tank rocket amplification |

**Observations:**
- Multiple entries for the same source tag (rules 13/14 for 93mm, 16/17 for 84mm) imply **PossibleHitLocations** or other filters differentiate them. Need to re-dump with those filter fields included.
- Max amplifier is `+450%` for drone strikes — matches gameplay expectation of kamikaze drones being effective
- Bone rules (23, 24) show hit-location-based mod: the +300% is likely the pilot cockpit; the -50% is likely the armored underside

## 5. Top damage source tags (across all 22 vehicles)

| Tag | Occurrence count |
|---|---:|
| `Meta.Damage.Bullet` | 94 |
| `Meta.Damage.Explosive.Rocket` | 42 |
| `Meta.Damage.Explosive.Radius.Inner` | 34 |
| `Meta.Damage.Cannon.20x102mm` | 24 |
| `Meta.Damage.Explosive.Utility.IED` | 23 |
| `Meta.Damage.Cannon.35x228mm` | 23 |
| `Meta.Damage.Explosive.Rocket.120mm` | 23 |
| `Meta.Damage.Explosive.Rocket.125mm` | 23 |
| `Meta.Damage.Cannon.30mm` | 22 |
| `Meta.Damage.Explosive.Rocket.120x800mm` | 22 |

Every vehicle has a `Meta.Damage.Bullet` rule (universal baseline),
and the top rockets/cannons appear across most vehicles. This creates
the **damage matrix** — the data model that answers "how much damage
does weapon X do to vehicle Y."

## 6. Vehicle section/health model (SDK)

Vehicles are divided into **health sections** (engine, cockpit, fuel
tank, wheels, etc.), each with its own health pool and damage routing.

### 6.1 `FVehicleHealthSection` (0x140 bytes)

[`sdk/raw/Mechanized_structs.hpp#L523`](sdk/raw/Mechanized_structs.hpp#L523):

```cpp
struct FVehicleHealthSection final {
    float MaxHealth;                                 // 0x00
    FGameplayTagContainer Tags;                      // 0x08 — section identity tags
    bool _aaachkphmgcampdlhdkkf;                     // 0x28 — unresolved flag
    TMap<FGameplayTag, FVehicleDamageRouting> PreDamageRouting;        // 0x30
    bool _aaacikmpjffpcggjhonpl;                     // 0x80 — unresolved flag
    TMap<FGameplayTag, FVehicleDamageRouting> PostDamageRouting;       // 0x88
    bool _aaadafjbjhkkggmmjaeba;                     // 0xD8 — unresolved flag
    TMap<FGameplayTag, FVehicleDamageRouting> SimultaneousDamageRouting; // 0xE0
    FGameplayTag RepairInteractionContextTag;        // 0x130
    FGameplayTag RepairInteractionTrackerPointTag;   // 0x138
};
```

**Three damage routing maps** — each keyed by damage-type tag,
pointing to a routing rule:

- **PreDamageRouting** — damage routed *before* applying to this section
- **PostDamageRouting** — damage routed *after* applying (overflow /
  spillover to connected sections)
- **SimultaneousDamageRouting** — damage split simultaneously across
  multiple sections

### 6.2 `FVehicleDamageRouting` (0x30 bytes)

```cpp
struct FVehicleDamageRouting final {
    FBHScalableFloat Scalar;             // 0x00 — multiplier applied to routed damage
    bool bUseAbsoluteHealth;             // 0x28 — route to absolute health vs section
    bool bOnlyWhenDepleted;              // 0x29 — only route when section is depleted
};
```

**Interpretation:** when a section takes damage, its routing maps
determine how damage propagates. For example, a hit to the main rotor
section might `PostDamageRouting` 50% of damage into the hull section
when the rotor is depleted (`bOnlyWhenDepleted = true`).

### 6.3 How this ties to §4's rule table

Open question: the per-vehicle DT's rules apply **before** reaching the
section routing, or **after**. Likely:

```
raw damage from hit
  → per-vehicle DT rule chain (§4)
  → section identification (hitbox → section tag)
  → section's PreDamageRouting map (route to connected sections if any)
  → apply to section MaxHealth
  → section's PostDamageRouting (spillover if section destroyed)
```

This is a §7 IDA-RE question.

## 7. Still Not Pulled / Open Questions

### 7.1 Duplicate-tag entries (`IDA` + `EXPORT`-fillable)
ROT_02 has two entries for `Explosive.Rocket.93mm` (-30% and -45%)
and two for `.84mm` (+30% and -5%). The differentiator is either
`PossibleHitLocations` (hit-location-specific sub-rules) or an
`InstigatorRequirements` filter. Current export shows these fields as
empty for both duplicates, but they must differ somehow — the duplicates
would otherwise be unreachable. Possibilities:
- Export dropped non-empty filters
- Rules are resolved by some secondary matching mechanism not visible
  in the raw data

Resolve by re-dumping with full nested properties, or by IDA tracing
the rule-selection function.

### 7.2 Rule execution order per entry (`IDA`-fillable)
Same question as infantry §7.1 — all `PriorityIndex` are `-1`, so
rules apply in array order. Needs IDA confirmation on the
`FDamageModificationEntry` consumer in the orchestrator.

### 7.3 Section routing vs rule chain order (`IDA`-fillable)
Where in the pipeline does the §4 rule chain run relative to the §6
section routing? Candidates:
- Rules apply, result goes to section → section routes to others
- Section identification happens first → then rules filter → then route
- Rules + routing interleave per section

Needs IDA RE of the vehicle damage subsystem.

### 7.4 Universal fallback vs per-vehicle override (`IDA`-fillable)
When no per-vehicle DT exists (e.g., a new vehicle shipped without
its DT), does the game fall back to `DT_GlobalDamage_VehicleData`'s
placeholder row, or crash? The placeholder row has all-zero entries,
suggesting a "no-op" fallback is intended.

### 7.5 PriorityCategory purpose (`SDK`-fillable, follow-up)
7 priority categories group rules, but with `PriorityIndex=-1` on all
entries, the categories don't drive ordering. Candidates for their
role:
- UI display grouping ("here are all armor rules")
- Debug filtering
- Future-use rule-set extension points
- Server-authority rule-set subset selection

Needs SDK trace of consumers of `PriorityCategory`.

### 7.6 Multi-vehicle variants (`EXPORT`-fillable)
`WHL_05_Humvee` + `WHL_05_Minigun` + `WHL_05_RingTurret` all represent
Humvee variants with slightly different profiles. Need to confirm:
- Does the game pick a DT based on loaded weapon/attachment?
- Or does each variant have its own class and tag?

### 7.7 Server-authoritative rule evaluation (`SECURITY`-flagged)
Open security question (does **not** go in a public PR — route through
[`SECURITY.md`](SECURITY.md)):
- Does the rule evaluation happen server-side with trusted hit data?
- Does the client send a damage amount or just a hit event?
- Where in the pipeline is network authority asserted?

Addressed per the project's responsible-disclosure policy — details
tracked internally.

## 8. Cross-references

### SDK files cited
- [`sdk/raw/Mechanized_structs.hpp`](sdk/raw/Mechanized_structs.hpp) — line 511 (`FVehicleDamageRouting`), 523 (`FVehicleHealthSection`), 694 (`FVehicleDamagePhysicsData`)
- [`sdk/raw/WDGame_structs.hpp`](sdk/raw/WDGame_structs.hpp) — line 4646 (`FWDModifyDamageData`), 4870 (`FWDDamageModification`), 4887 (`FWDDamageModificationEntry`)
- Related: `GC_DamagedVehicle_*_classes.hpp` (visual damage states, Niagara/VFX response)

### Data files cited
- Fallback: `data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_VehicleData.json`
- Per-vehicle (22 files): `data/Wardogs/Plugins/GameFeatures/Vehicles/<CODE>/Content/*/DT_GlobalDamage_VehicleData_<CODE>.json`

### Related reference docs
- [`Wardogs_DamagePipeline_v1.md`](Wardogs_DamagePipeline_v1.md) — infantry damage pipeline (companion, different architecture)
- [`Wardogs_AllVehicles_Stats_Damage_v1.md`](Wardogs_AllVehicles_Stats_Damage_v1.md) — per-vehicle stats and base damage values
- [`Wardogs_GameFeatures_Vehicles_v2.md`](Wardogs_GameFeatures_Vehicles_v2.md) — vehicle game-feature loadouts

## Change log

| Date | Change |
|---|---|
| 2026-10-16 | v1 — First complete trace. Found that vehicle damage architecture is distinct from infantry: per-vehicle rule tables with literal operations + requirement filters, not a central modifier blueprint chain. Full ROT_02 Havoc profile extracted (26 rules). Summary of all 22 vehicles' profiles. §6 section/health model documented from `Mechanized_structs.hpp`. §7 open questions distinct from infantry pipeline. |
