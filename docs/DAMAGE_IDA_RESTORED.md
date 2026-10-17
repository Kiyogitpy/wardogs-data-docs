# Damage trace — restored executable

Recorded 2026-10-17 using IDA 9.3, embedded IDAPython 3.13.7 and
Hex-Rays 9.3.0.260213. The restored input supports a native damage trace.
**B-2's evaluator contract is established; B-1 is partially resolved.**
Blueprint helper bodies, ordering between target-tag groups, final health
application and server behavior remain unverified. No game was executed
and no process or service was contacted for gameplay research.

## Input and saved analysis

- Source: `E:/Reverse_Engineer/wardogs_analysis/WardogsClient-Win64-Shipping.restored.exe`.
- Size: 231,695,256 bytes; SHA-256:
  `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.
- Preferred image base: `0x140000000`; image size: `0xE15D000`.
- Embedded UTF-16LE marker: `++Wardogs+Live-CL-516586` at file offset
  162,174,544. This corroborates the documented build label; it does not
  authenticate the restored file as byte-identical to an original release.
- Work directory:
  `E:/Reverse_Engineer/wardogs_analysis/ida_damage_restored_20261017_jzus_7lg`.
- Saved database: `damage_restored.i64` in that directory. The directory
  also contains the byte-identical input copy, input manifest, scripts,
  IDA logs, pseudocode and independent Capstone instruction listings.
  These large local artifacts are outside the checkout.

The supplied `IDAMappings/5.7.4-516586+++Wardogs+Live-Wardogs.idmap`
and the checkout mapping have identical SHA-256
`f4b2942331061187454b625821f8a6119b267551d22dc1cabbdf1a4f3ee1afdb`.
After this comparison, the duplicate checkout and temporary analysis maps
were deleted at the user's request. The sole authoritative map is now
`E:/Reverse_Engineer/wardogs_analysis/IDAMappings/5.7.4-516586+++Wardogs+Live-Wardogs.idmap`.
Selected damage vtable labels were applied after checking their pointers
against code. A full mapping import was not performed.

Both `GObjects-Dump-WithProperties.txt` and `GObjects-Dump.txt` in the
research root declare the same build label and 148,028 objects. Selected
property records corroborate `DamageCategoriesDataAsset`, the category
array, and the custom operation's parameter block. Their recorded object
addresses were not used as static executable addresses. These dumps do
not supply Blueprint bytecode or native method implementations.

## Method and limitations

Exact native-name registration pairs located `ModifyDamage` and
`GetModificationAmount`. Their wrappers led to the native methods below.
Method roles are analyst labels unless a reflected registration identifies
the method. Addresses below are **file RVAs for this hash**, not live
process addresses or generally portable offsets.

IDA decoded imports and executable instructions. Its PE loader reported
35,222 invalid unwind entries out of 747,204 entries and skipped those
entries. Some surviving ranges describe only fragments or include padding;
they were not accepted as complete method boundaries. Bounded control
flow and independent Capstone decoding established the inspected ranges.
Scoped functions were repaired in the owned database; broad autoanalysis
was disabled. This is not a claim of complete analysis of the executable.

The first load stalled after IDA's default PDB search failed. That
task-owned IDA process was stopped and a fresh database was loaded with
`-Opdb:off`; subsequent passes exited successfully. No vendor PDB was
available. ClassInformer failed to load, but IDAPython and Hex-Rays worked.
A provisional boundary and an incorrect no-return classification initially
truncated the custom adapter's pseudocode; clearing those in the owned
database recovered its body. Its parameter copies and floating argument
were also checked against instructions. The evaluator, collector, matcher,
adapter and sorting helpers decompiled.

## Native locations

| Role | RVA | Evidence |
|---|---|---|
| Reflected `exec_ModifyDamage` | `0x6F08A60` | Registration name at `0xB432298`; pair at `0xB434AD0`; direct call to native method |
| Native subsystem `ModifyDamage` | `0x6F02EC0` | Wrapper call; converts event inputs and calls selected system's virtual evaluator |
| Select first active damage system | `0x6EFFD40` | Iterates subsystem collection and returns first valid object passing its active predicate |
| Global evaluator | `0x6BB6FB0` | Global vtable `0xB3217D0`, slot `0x2B0`; inspected through `0x6BB7479` exclusive |
| Global collection | `0x6BB6A60` | Same vtable, slot `0x2B8`; registry/tag traversal and per-group sorting |
| Match and append row entries | `0x6BB6730` | Callback thunk at `0x6BB6A50`; loops 184-byte entries |
| Requirement-container matching | `0x6BB5D20` | Each required tag must occur in explicit or parent-tag arrays |
| Category priority lookup | `0x6BB8970` | Exact category lookup returning zero-based index or -1 |
| Per-group sort / fallback | `0x6BB61A0` / `0x6BB5F40` | Signed comparisons of priority; swaps with no secondary key |
| Custom dispatch adapter | `0x6BB7900` | Copies original input struct, supplies current amount separately, dispatches event/native override |
| Reflected `exec_GetModificationAmount` | `0x6BB7B30` | Registration pair at `0xB322038`; virtual override call |
| Base `GetModificationAmount` | `0x15B83B0` | Slot 86 of `0xB321D30`; returns 0.0 |
| Armor-durability override | `0x6BB7E10` | Slot 86 of `0xB322140`; see [corpus cross-check](#corpus-cross-check) |

The subsystem's bool parameter bypasses the selected evaluator on the
inspected branch. The exec passes it as `popped bool != 0`. When it is
set, the native method returns the leading float of its event argument
unchanged. Its gameplay name was not recovered. The corpus records 17
direct call sites to `0x6F02EC0`: the exec at `0x6F08B42` and 16 native
callers whose roles are not traced.

With the bool clear, the method returns the converted amount without
evaluation when that amount is not positive, no system is selected, or
the selected system is flagged as garbage. It broadcasts
`OnDamageModified` on every path. The selected-system predicate reads the
base active field through a slot-89 implementation (`0x178DF10`) that the
linker shares with unrelated classes. Only the first such system is
evaluated. This does not establish which system an actual gameplay event
will select.

## B-1: selection and ordering

The collector obtains registry rows while walking target tags. The callback
processes the row's complete entry array; it appends every eligible matching
entry, without stopping after the first match. Its return is always false,
so it does not itself terminate the caller's tag traversal.

The callback first skips entries whose three requirement arrays and
hit-location requirement array are empty **and** whose literal amount is
zero. The custom flag and operation enum do not override that preliminary
test. This skips the 60 empty `None` entries identified by the export audit.
A zero-valued percentage entry with requirements is a distinct case.

For entries passing that preliminary test:

1. Required alignment 0 is unrestricted; otherwise it must equal the event
   alignment.
2. All tags in each instigator, target and source requirement container
   must occur in that event container's explicit or parent-tag arrays.
   Empty requirement containers pass.
3. An empty hit-location container passes; a populated container requires
   at least one match against the hit tag's explicit or parent tags.
4. The selected modification is copied into the target-tag group. The
   match callback (`0x6BB6730`) replaces the copy's `PriorityIndex` with
   the category lookup result. It stores the original row entry index in
   the copy's trailing padding at offset `0x24`, which the SDK declares
   only as `Pad_24`.

Category lookup returns the **first exact tag match's zero-based array
index**, or **-1** if missing. Each target-tag group's modifier array is
sorted by that signed index in ascending order. Missing categories
therefore sort before index 0. The sort uses swaps and no secondary key:
it does not promise stable source order for equal categories.

With the exported category asset, the known order within a group is:
Calibre, AmmoModifier, CaliberEffectiveness, Bone,
PenetrationEffectiveness, Tracer, Weapon, Armor, Melee, Ricochet,
Penetration, Friendly. Serialized infantry indexes of -1 do not control
this order because the collector overwrites them.

The evaluator visits the populated slots of a grouped sparse collection,
then visits the sorted array in each slot. **This is not one global sort
across all target-tag groups.** The collector starts at the target
entity tag and walks parent tags up to, but not including,
`RootDamageTag`, looking up a registry row at each level. The instigator
and source tags are added to their own context containers; the target tag
is not. The parent-tag step (`0x395F4D0`) and group insertion
(`0x6BB5ED0`) have no corpus body. Group order, registry fallback and
duplicate-row effects therefore need further tracing before claiming a
total order for an arbitrary event. B-1 remains partial.

## B-2: evaluator arithmetic

Let `S = ModifyDamageData.Amount` on evaluator entry and initialize
`C = S`. For each selected modification, the inspected code implements:

| Branch | Delta | Update |
|---|---|---|
| Non-custom `None` (0), or unrecognized enum | No calculation | Leave C unchanged |
| Non-custom `Percentage_Starting` (1) | `(Amount * 0.01f) * S` | `C += delta` |
| Non-custom `Percentage_Ongoing` (2) | `(Amount * 0.01f) * C` | `C += delta` |
| Non-custom `Add` (3) | `Amount` | `C += delta` |
| Custom | `GetModificationAmount(originalData, C)` | `C += returnedDelta` |

For custom modifications the evaluator does **not** additionally apply the
serialized enum or literal amount. It resolves a valid operation class's
default object, then dispatches its implementation. Invalid/unavailable
custom classes are skipped. The data struct's original amount remains S;
the separate float argument carries C. Individual custom bodies can use
those inputs differently and remain to be traced.

Instruction anchors in the global evaluator:

```text
RVA 6BB72DE: current passed in xmm2 to custom adapter at 6BB7900
RVA 6BB72F8: custom return stored as result delta
RVA 6BB72FD: addss current, returnedDelta
RVA 6BB7306: non-custom enum selection
RVA 6BB7324: ongoing Amount *= 0.01f
RVA 6BB7329: ongoing delta *= current
RVA 6BB732F: starting Amount *= 0.01f
RVA 6BB7334: starting delta *= starting
RVA 6BB733C: addss current, delta
RVA 6BB73E7: maxss current, 0
```

The nonempty-collection path clamps C to at least zero after all groups,
not after each modification. No upper bound is applied. The
empty-collection path returns S without passing through that clamp. A
non-custom delta is applied before its absolute magnitude is checked
against approximately `1e-8` for recording in the event's result list;
that threshold does not suppress its arithmetic. Custom deltas are
recorded without the threshold. The result list's location and record
layout come from types outside the validated set.

Thus a selected non-custom ongoing amount of 0 has zero delta; -25 gives
`C *= 0.75` algebraically, while +100 gives `C *= 2`. These are explanations
of the native operator, not claims about a particular hit or the raw values
inside an untraced custom helper. Arithmetic uses single-precision floats.

## Corpus cross-check

On 2026-10-17 this trace was rechecked against the
[decompilation corpus](DECOMPILATION_CORPUS.md) for the same input hash.
`corpus.sqlite` was opened read-only. Every claim needed a function body
and RVA. A separate verifier checked each struct offset, field name and
type against `validated_sdk_types.h` and `schema.json`. Claims resting on
a type outside the 14 validated layouts stayed unverified. Some
instruction, vtable and registration checks read the restored executable's
bytes directly, read-only. No analysis database was opened.

No verified finding contradicts the native locations, B-1 matching and
sorting, or B-2 arithmetic above. The doc's statements are confirmed at
these RVAs:

- Exec to native method and bypass: `0x6F08A60`, `0x6F02EC0`.
- First-active-system selection: `0x6EFFD40`.
- Evaluator and collector slots 86/87: `0x6BB6FB0`, `0x6BB6A60`.
- Entry skip, alignment and requirement matching: `0x6BB6730`, `0x6BB5D20`.
- Category lookup: `0x6BB8970`.
- Unstable ascending sort: `0x6BB61A0`, `0x6BB5F40`.
- Operation arithmetic, including no change for `None` or an unknown
  enum, and the final floor: `0x6BB6FB0`.
- Custom dispatch with the running amount as a separate float:
  `0x6BB7900`, `0x6BB7B30`.

New findings:

- **Base override:** `0x15B83B0` returns 0.0. A Blueprint operation that
  does not override `GetModificationAmount` contributes no delta.
- **Blueprint overrides:** the four `B_*_C` overrides are Blueprint
  script. None of their bodies is in the native corpus.
- **Armor durability (`0x6BB7E10`):** returns 0 when the target actor
  (`FWDModifyDamageData+0x50`) is null or flagged as garbage. Otherwise it
  walks the target context tags (`+0x60`), calls the actor's virtual
  `+0x738`, and returns `value × -0.01 × current`. What that virtual
  returns is not traced.
- **Shared vtable:** `0xB321D30` serves both
  `UWDCustomDamageModificationOperation` and
  `UWDCustomAttributeModification`, because the linker merged the
  identical tables.
- **Schema gap:** `schema.json`'s `EObjectFlags` lacks `0x40000000`. The
  SDK (`sdk/raw/Basic.hpp`) names it `MirroredGarbage`; it is the
  garbage test used throughout these bodies.

Still unverified:

| Item | RVA | Reason |
|---|---|---|
| Event-to-`FWDModifyDamageData` conversion, so the relation between the event amount and S | `0x6EF8DE0` | No corpus body |
| Event argument type and its leading `Amount` | `0x6F02EC0` | `FWDDamageEventData` not validated |
| Result list at event `+0x190` and its record layout | `0x6BB6FB0` | Types not validated |
| Default object at `UClass+0x110`; subclass check via `+0x30`/`+0x38` | `0x6BB6FB0` | `UClass`/`UStruct` not validated |
| `+0xD4 & 0x80` as the native-class test | `0x6BB7900` | Engine-semantics inference |
| Group order (insertion order would run most specific tag first) | `0x6BB6FB0`, `0x6BB5ED0` | Container internals; no body |
| Registry row entries at `+0x10`; parent-tag step | `0x6BB6A60`, `0x395F4D0` | Row type not validated; no body |
| Event alignment at input-struct `+0x60` | `0x6BB6730` | Input struct not validated |
| Registry name and category asset from game settings `+888`/`+896` | `0x6BB6A60`, `0x6C03540` | Type not validated |
| No other `GetModificationAmount` dispatch site | `0x6BB7C12`, `0x6BB7AC7` | 1,972 other `+0x2B0` sites untraced |
| Delegate broadcast internals | `0x18FCDB0` | Container layout opaque |
| Individual instruction anchors listed under B-2 | `0x6BB72DE`–`0x6BB73E7` | Only call site `0x6BB72F3` rechecked |

The category order listed under B-1 comes from the exported asset and was
not part of this code check.

## Remaining work

Trace the four Blueprint helper bodies, which are not in the native
corpus, and the value behind the armor-durability override, to determine
their bindings, row selection, fallback and returned deltas (B-3/B-4). Finish the target-tag/registry/group-order trace before
producing an end-to-end infantry example. Vehicle/explosive caller paths,
health application and server authority are outside this completed slice.
Any security finding follows [SECURITY.md](../SECURITY.md).

The [earlier failed-input report](DAMAGE_IDA_RESULTS.md) remains valid for
its different binary hash. It is not the result of this restored-input run.
