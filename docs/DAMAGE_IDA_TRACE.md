# Damage modifier trace brief

Prepared 2026-10-17 for path B, following the export audit of
[DamagePipeline v1](../Wardogs_DamagePipeline_v2.md). This brief identifies
native/Blueprint implementation questions. Results are recorded separately;
this brief records no runtime observation or server-validation result. The SDK gap sweep
(path A) remains separate; this audit changes no SDK files.

**2026-10-17 execution update:** the [first input-validation pass](DAMAGE_IDA_RESULTS.md)
could not recover usable code from the reconstructed dump. A later
[restored-executable pass](DAMAGE_IDA_RESTORED.md) established B-2's
native evaluator contract and partially resolved B-1: matching, category
priority replacement, per-group sorting and unstable ties. Ordering between
groups and B-3/B-4 helper bodies remain open. A read-only
[corpus cross-check](DAMAGE_IDA_RESTORED.md#corpus-cross-check) then
confirmed that contract. It also established the call edge from
`ModifyDamage` to the global evaluator, identified the second
`GetModificationAmount` float as the running amount, and recovered the
native armor-durability override. The Blueprint helper bodies are not in
the native corpus.

## What the export audit establishes

| Evidence | Result | What remains unknown |
|---|---|---|
| [Infantry rule table][infantry] | 146 entries; 12 custom percentages, 74 non-custom percentages, 60 `None` entries | Matching, selection, evaluation order, and arithmetic |
| Custom class references in that row | Five classes; repeated references under different requirements | Which entries execute for a given event |
| Infantry priority fields | All `PriorityIndex` values are -1; eight non-`None` categories occur | Meaning of the sentinel, category ordering, and tie behavior |
| [Category asset][categories] | Ordered export list of 12 category tags | Whether/how that order is consumed |
| [Bone table][bones] | 20 rows, each with 12 hit-location values | Row selection, fallback, and application |
| [Seat-reduction table][seats] | 11 vehicle-variant rows with arm-tag/state-tag groups | Lookup, missing-row behavior, and returned quantity |

The 60 `None` entries have empty requirements/hit locations, no custom
operation, amount 0.0, alignment `None`, category `None`, and index -1.
This describes their serialized shape; it does not establish their purpose
or whether the consumer skips them. Another 29 entries are non-custom
`Percentage_Ongoing` with amount 0.0 and must be examined separately.

The source document now enumerates the full Universal row and all 11 seat
rows. Those coverage questions need no new extraction. Existing archetype
bone rows also remove the need to hypothesize an undiscovered override
table merely to explain a Universal head value of 1.0.

## Session inputs and limitations

Use an existing offline analysis session when it matches the original
`WardogsClient-Win64-Shipping.exe` for the documented CL-516586 build.
Record the original binary's path, SHA-256, PE image base, and analysis
database identity before recording implementation evidence. The build
label in the documents and mapping filenames is not binary-hash evidence.
No matching original executable was present in this checkout during the
initial audit. The subsequent pass inspected an external reconstructed PE
and an existing recorded capture; their exact build match remains unverified.

The sole map at
`E:/Reverse_Engineer/wardogs_analysis/IDAMappings/5.7.4-516586+++Wardogs+Live-Wardogs.idmap`
is 4,942,224
bytes and parses as Dumper-7 binary format v2. The former plain-text
description/import example in `mappings/README.md` has been corrected.
The inspected file has only one native exec-function record, unrelated to
damage, despite its extensive type/vtable metadata. See the results before
attempting an import. Do not assume an image base or apply addresses from
a different build.

Generated headers contain incomplete type placeholders such as
`TArray<FNone_>` for `FWDDamageableEntityTableRow.DamageModificationEntries`.
Use the concrete entry structure and actual implementation evidence when
recovering element handling; do not infer semantics from a placeholder.

The generated [`ModifyDamage` function](../sdk/raw/WDGame_functions.cpp#L48948)
looks up a `UFunction`, calls `ProcessEvent`, and returns the parameter
block's return value. It is a call wrapper, not the damage algorithm.
Likewise, the `B_*::GetModificationAmount` wrappers do not contain their
Blueprint implementations. Record native delegation or an unavailable
Blueprint script body explicitly rather than claiming the wrapper is the
implementation.

## B-1 — Find the consumer and establish evaluation order

**Question:** which implementation selects and iterates matching damage
entries, and what controls their evaluation order?

Starting points:

- [`UWDDamageSubsystem::ModifyDamage`](../sdk/raw/WDGame_classes.hpp#L44447)
  accepts `FWDDamageEventData&`, an unresolved bool parameter, and returns
  a float. The owning subsystem also declares a `DamageSystems` collection.
- [`UWDGlobalDamageSystem`](../sdk/raw/WDGame_classes.hpp#L36482)
  declares `DamageRegistryName`, `DamageCategoriesDataAsset`, and
  `RootDamageTag`. These fields give consumer leads; they do not prove a
  call edge from `ModifyDamage` or identify the native orchestration method.
  *Update:* the restored trace shows that edge. `ModifyDamage`
  (`0x6F02EC0`) makes an indirect slot-86 call at `0x6F02F3A` on the
  first active damage system. The global system's slot-86 implementation
  is `0x6BB6FB0`, and its collector reads these three fields.
- [`FWDDamageModificationEntry`](../sdk/raw/WDGame_structs.hpp#L4887)
  declares requirement containers, alignment, hit locations, and the
  output operation. [`FWDDamageModification`](../sdk/raw/WDGame_structs.hpp#L4870)
  declares category and priority fields.

Follow the real implementation behind the interface and identify registry
row selection, requirement matching, category lookup, and the loop that
consumes entries. Distinguish source array order from any filtered,
grouped, cached, or sorted collection. Inspect what happens when indexes
are -1, when categories differ, and when multiple requirements match.
The existence of a category list is a question to investigate, not proof
that it supplies precedence.

**Completion evidence:** an annotated implementation fragment identifying
the consumer and ordering/filtering rules, with a build-matched code
location and any unresolved delegation recorded. Update §7.1 only to the
extent that the fragment proves the behavior. A caller list or SDK
declaration alone does not close B-1.

## B-2 — Establish operation and custom-return arithmetic

**Question:** how do enum selection, literal `Amount`, and custom return
values update the working damage quantity?

[`EWDDamageModificationOperation`](../sdk/raw/WDGame_structs.hpp#L1683)
declares `None`, `Percentage_Starting`, `Percentage_Ongoing`, and `Add`.
The enum names provide no implementation of those cases.

Useful zero-based infantry entry witnesses:

| Entry | Exported shape | Question for the consumer |
|---|---|---|
| 0 | `None`, non-custom, amount 0 | Is it skipped, and at what stage? |
| 5 | Bone custom class, percentage operation, amount -75 | Does the custom return replace, combine with, or ignore the literal? |
| 8 | Non-custom percentage, amount -50, Friendly alignment | How is the amount scaled and applied after matching? |
| 16 | Non-custom percentage, amount 0, Tracer category | What does zero do in this branch? |
| 138 | Ammo custom class, amount 0, armor/bullet requirements | What quantity does its return represent? |

Trace the operation switch and the values entering/leaving each case.
Identify the original versus current damage input, percentage scaling,
aggregation timing, and any clamping or early exit. Do not interpret a
negative literal as a direct multiplier or a zero literal as proven neutral
before examining the relevant branch. Keep custom and non-custom paths
separate until their relationship is established.

The interface [`GetModificationAmount`](../sdk/raw/WDGame_classes.hpp#L36510)
returns a float and takes an unresolved second float parameter. Establish
that parameter's source and meaning at the actual caller. *Update:* the
evaluator passes the running amount there, and adds the return value to
it. See [B-2 in the restored trace](DAMAGE_IDA_RESTORED.md#b-2-evaluator-arithmetic).
[`FWDDamageModificationDebugData`](../sdk/raw/WDGame_structs.hpp#L11152)
contains `AmountBeforeCalculation`, `AdjustAmount`, and
`AmountAfterCalculation`; these are useful static leads, not observations
of a computation.

**Completion evidence:** branch-supported arithmetic or pseudocode that
identifies each operand and custom-return treatment. Mark any enum case
not reached in the inspected implementation as unresolved. Document an
example only after its row selection, matching, order, and arithmetic have
support; do not restore the previous `baseDamage × 1.10` example by
assuming the Universal bone row.

## B-3 — Establish bone row selection and fallback

**Question:** how does `B_BoneDamageModifiers_C` choose a table row and
hit-location value, including fallback and tag hierarchy?

The [subclass declaration](../sdk/raw/B_BoneDamageModifiers_classes.hpp)
contains a `DataTable` field. Recover the actual binding and implementation
or Blueprint script. The [existing export][bones] contains both
`Universal` and archetype rows. For example, `Torso.Upper` is 1.10 in
Universal and 0.885 in AR; Head is 1.0 in Universal and 2.35 in AR.
These are competing candidate lookups, not numbers to multiply together
without evidence.

Trace the row key's producer, any exact/parent-tag match, missing-row and
missing-location handling, and the returned quantity. Distinguish
archetype-specific rows already present from any additional per-weapon
mechanism that may or may not exist.

**Completion evidence:** concrete table binding, selection/fallback rule,
and the selected value's path into B-2. If the Blueprint body is unavailable,
record that exact boundary instead of assigning behavior from class names.

## B-4 — Establish the remaining helper bindings

**Question:** which helpers are bound to the remaining referenced classes,
and how are their raw fields converted into custom-operation results?

| Referenced class | Existing input lead | Required evidence |
|---|---|---|
| `B_ArchetypeCaliberModifiers_C` | Declared `DataTable`; [archetype/caliber helper][archetype] | Bound table, source tag derivation, lookup and fallback, returned quantity |
| `B_AmmoTypeEffectiveness_C` | [Pen helper][ammo-pen] has six rows and arm-group values; infantry entries 138–141 have armor/helmet requirements | Actual table binding and use of `Modifier` versus the arm-group map |
| `WDDamageModificationOperation_PlayerArmorDurability` | Infantry entries 142–144 name the native class with target/source requirements | Branch selection, durability input source, return semantics. Override recovered at `0x6BB7E10`; its input value is still untraced ([cross-check](DAMAGE_IDA_RESTORED.md#corpus-cross-check)) |
| `B_VehicleSeatDamageReduction_C` | [Seat helper][seats] has variant rows and `State.Player.Vehicle.SeatDamageReduction` values | Bound table, variant/state matching, missing-row handling, return semantics |

The ammo and seat subclass declarations do not expose their own `DataTable`
field; the base declaration does not establish such a binding either.
Recover the binding rather than describing it as inherited. The seat table
contains no explicit Driver/Gunner/Passenger rows. Its negative values
must remain raw values until B-2/B-4 establish their meaning.

**Completion evidence:** a source-to-return trace for each inspected
class, with unresolved classes left open. An inheritance chain or shared
function signature does not establish a helper table's execution.

## Recording results and stopping

Start the IDA session with B-1 and B-2. B-3 and B-4 give bounded follow-ups
after the orchestrator/call boundary is known. For each result record:

- Question ID and the original binary's hash/build identity.
- Actual implementation location and whether it is native or Blueprint.
- Source asset, row/entry index, input fields, and the relevant code evidence.
- What is established, what remains inferred, and which calls/bodies were
  unavailable or outside the inspected path.

Return non-sensitive behavior documentation to DamagePipeline §7. Preserve
security-relevant authority/validation findings privately under
[SECURITY.md](../SECURITY.md); no authority guarantee or vulnerability is
established by this brief. Static client code or a future isolated client
capture alone cannot prove the behavior of an unavailable server build.

If the matching implementation, mapping importer, or Blueprint body is
unavailable, retain the affected question as unresolved and record the
missing artifact. This brief does not authorize instrumentation, game-state
changes, or testing against live services. Any separate runtime work must
follow the established offline/isolated-session boundary, including the
restriction on server-connected tutorials to sessions that no other player
can join or share.

## Audit provenance

Repository baseline: `5b036b07cc40bb4c4c2cb98bce0d53214e217581`.
These SHA-256 values identify the exported inputs inspected, not the
shipping executable or a successful runtime collection:

| File under the damage-system directory | SHA-256 |
|---|---|
| `DamageDataTables/DT_GlobalDamage_InfantryData.json` | `81698c8a24e46992ddcf24158ae92c4d2beb67594407491db83ecf631f5f72ff` |
| `DA_GlobalDamage_Categories.json` | `f0303f8bb71ba829d6ea8cf661e43ce1b1167d70f9781641f538f513f02c2f47` |
| `DamageDataTables/DT_Helpers/DT_InfantryData_BoneDamageModifiers.json` | `faefd350303877e23e045d79fb960f1e881849b57797225f9e22c507a70f1d33` |
| `DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json` | `e6a0b4befde7dcce495c484619460be0e714d344717a8a5d9429add9889fa64f` |

[infantry]: https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json
[categories]: https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DA_GlobalDamage_Categories.json
[bones]: https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_BoneDamageModifiers.json
[seats]: https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json
[archetype]: https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json
[ammo-pen]: https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json
