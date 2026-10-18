# Damage evidence: native trace, corpus cross-check and RVA status

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

This page records the evidence behind the infantry damage pipeline: which
binaries were read, how, what each pass established, and how strong the
evidence is for each address the pipeline document cites. It replaces
three earlier notes: the trace brief (`DAMAGE_IDA_TRACE.md`), the failed
input-validation pass (`DAMAGE_IDA_RESULTS.md`) and the restored-executable
trace (`DAMAGE_IDA_RESTORED.md`). It includes the restored-trace updates
from commit `89cbd41`, which was never merged into `main`.

Behaviour is described in [DamagePipeline](../../Wardogs_DamagePipeline_v2.md).
This page gives the evidence behind it and does not restate the rules.
Nothing here is a runtime observation. No game was executed and no
process or service was contacted. No claim is made about server
authority or exploitability; security-relevant findings follow
[SECURITY.md](../../SECURITY.md).

All native addresses are **file RVAs for the restored executable's hash**
(§1). They are not live process addresses and do not carry over to other
builds. The one exception is §2.2, which concerns a different binary and
says so.

## 1. Binary identity and hashes

Hashes are copied from the earlier notes, from
[DamagePipeline §11](../../Wardogs_DamagePipeline_v2.md#binary-identity)
and from the corpus's own identity files. Nothing was recomputed for this
page.

### Executables, map and capture

| Artifact | Role | Size (bytes) | SHA-256 | Recorded in |
|---|---|---:|---|---|
| `WardogsFullDump_fixed.exe` | Dump-reconstructed PE; pass 1 failed on it (§2.2) | 234,214,912 | `97ec9e0d12ed4df164f95069d0243471d33bb2f2815e90c3b408f317a2b71543` | Results note |
| `WardogsClient-Win64-Shipping.restored.exe` | Restored executable; every RVA on this page | 231,695,256 | `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37` | Restored note; DamagePipeline §11; corpus `database_identity.json` and `final_verification.json` |
| `5.7.4-516586+++Wardogs+Live-Wardogs.idmap` | Dumper-7 map, binary format v2 | 4,942,224 | `f4b2942331061187454b625821f8a6119b267551d22dc1cabbdf1a4f3ee1afdb` | Results and restored notes; DamagePipeline §11; corpus `final_verification.json` |
| `Wardogs_1015.dmp` | Existing recorded capture, read in place during pass 1 | 14,177,243,536 | `92ccf844fb8ba7f98fea1f6b58786c8a43d45204dafab88ec4f3e1a5b3ba4f02` | Results note |

The restored executable declares image base `0x140000000` and image size
`0xE15D000`. It carries the UTF-16LE marker `++Wardogs+Live-CL-516586` at
file offset 162,174,544. That supports the documented build label but
does not prove the file is byte-identical to an original release. The
dump-reconstructed PE declares the same image base, image size
`0xDF5D000` and entry RVA `0x977EB60`, and has no such marker (§2.2).

The only map is
`E:/Reverse_Engineer/wardogs_analysis/IDAMappings/5.7.4-516586+++Wardogs+Live-Wardogs.idmap`
(see [`mappings/README.md`](../../mappings/README.md)). A duplicate
checkout copy had the same hash and was deleted at the user's request.

`GObjects-Dump-WithProperties.txt` and `GObjects-Dump.txt` in the research
root both declare the same build label and 148,028 objects. No hash is
recorded for either. They supply runtime reflection data (property
offsets) but no code, Blueprint bytecode or static addresses.

### Corpus

The decompilation corpus is described in
[DECOMPILATION_CORPUS.md](../DECOMPILATION_CORPUS.md). Its directory is
`E:/Reverse_Engineer/wardogs_analysis/decompiled_cl516586_20261017_mmvpuc__`.

- `final_verification.json`: `passed: true`. Input hashes: source
  `a5c3db10…0cc37`, map `f4b29423…1afdb`. It also lists a SHA-256 for each
  pseudocode shard.
- `database_identity.json`: input SHA-256 `a5c3db10…0cc37`, `.text`
  SHA-256 `919ba52a51e11edddbc4b076b318edce9feb81b78f9cda486587fbe4699181a8`,
  `.text` from `0x1000` to `0x9A27000`, and the 14 validated SDK layouts.
- `corpus.sqlite` is 1,585,963,008 bytes in the directory listing. No
  SHA-256 for it is recorded anywhere, and none was computed for this page.

Corpus scope: 437,174 candidates; 425,892 decompiled, 8,811 decompiled
with jumps, 2,471 failed (`export_summary.json`).

### Exported data inputs

The trace brief's export audit (repository baseline
`5b036b07cc40bb4c4c2cb98bce0d53214e217581`) recorded these hashes for the
damage-system files it inspected. They identify those inputs, not the
executable.

| File under `data/Wardogs/Content/GameMechanics/DamageSystem/` | SHA-256 |
|---|---|
| `DamageDataTables/DT_GlobalDamage_InfantryData.json` | `81698c8a24e46992ddcf24158ae92c4d2beb67594407491db83ecf631f5f72ff` |
| `DA_GlobalDamage_Categories.json` | `f0303f8bb71ba829d6ea8cf661e43ce1b1167d70f9781641f538f513f02c2f47` |
| `DamageDataTables/DT_Helpers/DT_InfantryData_BoneDamageModifiers.json` | `faefd350303877e23e045d79fb960f1e881849b57797225f9e22c507a70f1d33` |
| `DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json` | `e6a0b4befde7dcce495c484619460be0e714d344717a8a5d9429add9889fa64f` |

### Local work directories and result files

None of these is in the checkout.

| Pass | Directory under `E:/Reverse_Engineer/wardogs_analysis/` | Contents |
|---|---|---|
| 1 (failed) | `ida_damage_20261017___e23tea/` | Byte-identical PE copy, its IDA database, IDA log, probe scripts, `input_manifest.json`, `source_validation.json` |
| 2 (restored) | `ida_damage_restored_20261017_jzus_7lg/` | Byte-identical input copy, `damage_restored.i64`, input manifest, scripts, IDA logs, pseudocode, Capstone listings |
| 3 (corpus) | `decompiled_cl516586_20261017_mmvpuc__/` | `corpus.sqlite`, sharded pseudocode, identity and verification files |

Pass 1 result files:

| Result file | SHA-256 |
|---|---|
| `mapping_inventory.json` | `746da73a0e3d06ec7cfe99deabf278e34686b3eb12f3c197f8ffebd11f21208d` |
| `ida_probe_result.json` | `4c6f342b0ac160e1ce2132ff8adfcea0ac75063f49d3b45051f72fe264d24cea` |
| `recorded_capture_coverage.json` | `59704623c76425fca31b5a6ea72368cdaf418b56216fc5c9b0c9e6c4e4170a72` |

## 2. Method

There were three passes: an IDA pass on the dump-reconstructed PE, which
failed; a trace of the restored executable; and a read-only cross-check of
that trace against the corpus. §2.5 gives the rules for what counted as
evidence.

### 2.1 Questions B-1 to B-4

The trace brief set four questions after an audit of the exported rule
data. The audit established the data shape only:

| Evidence | Result |
|---|---|
| [Infantry rule table][infantry] | 146 entries: 12 custom percentages, 74 non-custom percentages, 60 `None` entries. All `PriorityIndex` values are -1; eight non-`None` categories occur |
| `None` entries | Empty requirements and hit locations, no custom operation, amount 0.0, alignment `None`, category `None`, index -1. Another 29 non-custom `Percentage_Ongoing` entries have amount 0.0 |
| [Category asset][categories] | Ordered list of 12 category tags |
| [Bone table][bones] | 20 rows, each with 12 hit-location values |
| [Seat-reduction table][seats] | 11 vehicle-variant rows with arm-tag/state-tag groups |

| Question | Asked | Where it was answered |
|---|---|---|
| B-1 | Which code selects and orders matching entries | Pass 2 and the corpus cross-check; [DamagePipeline §4–5](../../Wardogs_DamagePipeline_v2.md#4-entry-selection) |
| B-2 | How operations and custom returns update the amount | Pass 2; [DamagePipeline §6](../../Wardogs_DamagePipeline_v2.md#6-arithmetic) |
| B-3 | Bone row selection and fallback in `B_BoneDamageModifiers_C` | Blueprint bytecode, not native code; [DamagePipeline §7.1](../../Wardogs_DamagePipeline_v2.md#71-b_bonedamagemodifiers_c-entries-5-7-10) |
| B-4 | Bindings of the other custom operations | Bytecode for the three Blueprints; native code for `PlayerArmorDurability` ([DamagePipeline §7.2–7.5](../../Wardogs_DamagePipeline_v2.md#7-custom-operations)) |

The brief also fixed some reading rules that still apply. The generated
`ModifyDamage` wrapper ([`WDGame_functions.cpp`](../../sdk/raw/WDGame_functions.cpp#L48948))
and the `B_*::GetModificationAmount` wrappers only call `ProcessEvent`;
they are not implementations. Placeholder types such as `TArray<FNone_>`
for `FWDDamageableEntityTableRow.DamageModificationEntries` say nothing
about element handling.

### 2.2 Failed pass on the dump-reconstructed PE

This pass concerns `WardogsFullDump_fixed.exe` (`97ec9e0d…`), **not** the
restored executable. Its addresses do not apply elsewhere on this page.

IDA 9.3 loaded a byte-identical copy in autonomous mode with
auto-analysis off (`-a`). IDAPython ran and Hex-Rays initialized. The
script read loader segments and bounded candidate bytes, then exited 0. No
function was created or decompiled, and no bytes were patched. **B-1 and
B-2 stayed unresolved: no usable damage code was recovered.**

PE observations, offered without a diagnosis:

- The import directory is declared at RVA `0xCD05020`, size `0x55`, but
  `pefile` decoded zero import descriptors.
- The exception-directory RVA and size are zero.
- The first 64 KiB of `.text`, `.rdata` and `.pdata` each measured about
  7.997 bits per byte of entropy. That is unusual, but it does not prove
  encryption.
- An exact ASCII and UTF-16LE search for `++Wardogs+Live-CL-516586`
  found neither encoding.

The map parsed as Dumper-7 binary format v2 with a read-only decoder,
following the
[published layout](https://github.com/Encryqed/Dumper-7/blob/main/Dumper/Generator/Public/Generators/IDAMappingLayouts.h).
No symbols were imported into IDA.

| Map record kind | Count |
|---|---:|
| Strings | 95,999 |
| Enums | 3,225 |
| Structures/classes | 21,282 |
| Named globals | 3 |
| Vtables | 9,134 |
| Native exec functions | 1 |

The sole exec-function record, `AActor::AddComponent` at `0x9B0DEE8`,
fell in non-executable `.rdata` in this input. Four damage vtable labels
sampled in IDA held no canonical x64 pointers in their first eight
qwords:

| Map label | RVA | Canonical pointers in first 8 qwords |
|---|---:|---:|
| `UWDCustomDamageModificationOperation_VFT` | `0xB321D30` | 0/8 |
| `UWDGlobalDamageSystem_VFT` | `0xB3217D0` | 0/8 |
| `UWDDamageModificationOperation_PlayerArmorDurability_VFT` | `0xB322140` | 0/8 |
| `UWDDamageSubsystem_VFT` | `0xB434758` | 0/8 |

Each 64-byte IDA sample matched the PE's file bytes, so the IDA load did
not introduce the problem. In the restored executable the same vtable
RVAs hold valid code pointers (§3). The limitation is specific to this
input, but its cause was not identified.

`Wardogs_1015.dmp` names `WardogsClient-Win64-Shipping.exe` with module
size `0xE15D000`. None of its 68,650 `Memory64ListStream` ranges overlaps
that module, and there is no `MemoryListStream`. So the capture holds
**no** bytes of the main module. This is a coverage result, not an
assessment of the other modules.

### 2.3 Restored-executable trace

Pass 2 used IDA 9.3, embedded IDAPython 3.13.7 and Hex-Rays
9.3.0.260213 on a byte-identical copy of the restored executable.

- **Loader.** The first load stalled after IDA's default PDB search
  failed. That process was stopped and the database reloaded with
  `-Opdb:off`. No vendor PDB was available. ClassInformer failed to load.
- **Function boundaries.** IDA reported 35,222 invalid unwind entries out
  of 747,204 and skipped them. Some surviving ranges were fragments or
  included padding, so none was accepted as a method boundary unchecked.
  Bounded control flow and independent Capstone decoding fixed the ranges
  that were inspected.
- **Scope.** Scoped functions were repaired in the owned database and
  broad autoanalysis was disabled. This is not a complete analysis of the
  executable.
- **Truncated adapter.** A provisional boundary and a wrong no-return
  flag first cut short the custom adapter's pseudocode. Clearing both
  recovered the body. Its parameter copies and float argument were then
  checked against the instructions.
- **Map use.** Selected damage vtable labels from the map were applied
  after their pointers were checked against code. The map was not fully
  imported.
- **Entry points.** Exact native-name registration pairs located
  `ModifyDamage` and `GetModificationAmount`, and their wrappers led to
  the native methods. Method names are analyst labels unless a reflected
  registration supplies them.

Pass 2 established the native call path
([DamagePipeline §1](../../Wardogs_DamagePipeline_v2.md#1-call-path)), entry
selection (DamagePipeline §4), ordering within a target-tag group (§5)
and the evaluator arithmetic (§6). Every address it relied on is in the §3 table.
The subsystem's bool parameter returns the event's amount unchanged when
set; its gameplay name was not recovered.

#### B-1: selection and ordering

Pass 2 recovered the following. The callback scans a registry row's
whole entry array and appends every eligible match. It first drops an
entry only when all four requirement arrays are empty and its literal
amount is 0, which removes the 60 empty `None` entries. Alignment, tag
requirements and hit locations are then matched.

The match callback (`0x6BB6730`) also does two things to the copied
entry:

- It replaces the copy's `PriorityIndex` with the category's zero-based
  index, or -1 if the category is missing.
- It stores the source entry index at offset `0x24`, which the SDK
  declares only as `Pad_24`.

Each target-tag group is sorted ascending by that signed index, with no
secondary key. The order of equal-category entries is therefore not
guaranteed.

Two points were left open by pass 2 and closed in commit `89cbd41`:

- **Group order.** Insertion (`0x6BB5ED0`) reaches
  `TSparseArray::AddUninitialized` (`0x1587900`). That function appends,
  because the evaluator's map starts with no free slots and the collector
  never removes one. Groups therefore run in insertion order, most
  specific target tag first.
- **Parent-tag step.** `0x395F4D0` is `FGameplayTag::RequestDirectParent`.

Duplicate-row effects remain untraced.

#### B-2: evaluator arithmetic

Pass 2 established the operation table in
[DamagePipeline §6](../../Wardogs_DamagePipeline_v2.md#6-arithmetic).
Custom entries ignore their serialized enum and literal amount. The
original amount `S` stays in the struct passed to the operation, and the
running amount `C` is passed as a separate float. A single clamp at
zero, with no upper bound, runs after all groups, and only on the
non-empty path.

Instruction anchors in the global evaluator:

```text
RVA 6BB72E1: current amount into xmm2 for the custom adapter at 6BB7900
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

The first anchor was originally recorded as `0x6BB72DE`, which is the
instruction before `0x6BB72E1`; `89cbd41` corrected it.

### 2.4 Corpus cross-check

Pass 3 rechecked the pass-2 trace against the
[decompilation corpus](../DECOMPILATION_CORPUS.md) for the same hash.
`corpus.sqlite` was opened read-only, and every claim needed a function
body at a cited RVA.

A separate verifier checked each struct offset, field name and type
against `validated_sdk_types.h` and `schema.json`. Claims that rest on a
type outside the 14 validated layouts stayed unverified at that stage.
Some instruction, vtable and registration checks read the restored
executable's bytes directly, read-only. No analysis database was opened.

No verified finding contradicted the native locations, the B-1 matching
and sorting, or the B-2 arithmetic. New findings from the cross-check:

- **Base override.** The base `GetModificationAmount` (`0x15B83B0`, slot
  86 of `0xB321D30`) returns 0.0. A Blueprint operation that does not
  override it contributes no delta.
- **Blueprint overrides.** The four `B_*_C` overrides are Blueprint
  script, not native code. Their bodies were later read from cooked
  bytecode
  ([DamagePipeline §7.1–7.4](../../Wardogs_DamagePipeline_v2.md#7-custom-operations)).
- **Armor durability.** The override at `0x6BB7E10` returns
  `value × -0.01 × C`. Its virtual `+0x738` is `AActor` slot 231
  (`0x3A93090`), `FindComponentByClass`, called with
  `WDPlayerInventoryComponent`.
- **Shared vtable.** `0xB321D30` serves both
  `UWDCustomDamageModificationOperation` and
  `UWDCustomAttributeModification`; the linker merged the identical
  tables.
- **Schema gap.** `schema.json`'s `EObjectFlags` lacks `0x40000000`. The
  SDK (`sdk/raw/Basic.hpp`) names it `MirroredGarbage`, UE5's
  `RF_MirroredGarbage`, and it is the garbage test used throughout.
- **Event conversion.** The event-to-`FWDModifyDamageData` conversion
  (`0x6EF8DE0`) copies the event's `Amount` (`+0x0`) unchanged
  (`0x6EF8E2C`/`0x6EF8E37`), so `S` is the event amount.

The items the cross-check first left unverified were closed afterwards
(`8e3c4c3` in DamagePipeline, `89cbd41` in the restored note). Offsets
were confirmed against the runtime reflection data in the GObjects
property dump; engine details were confirmed from code. Values and
sources are in the
[DamagePipeline cross-check table](../../Wardogs_DamagePipeline_v2.md#offsets-and-engine-details-cross-checked).
One item remains open, and no document depends on it: the delegate
broadcast internals (`0x18FCDB0`), because the container layout is opaque.

**Correction.** The restored note said the corpus records "17 direct
call sites to `0x6F02EC0`: the exec at `0x6F08B42` and 16 native
callers". The `calls` table has 17 sites in 16 functions, and the exec is
one of those 16; `0x6B725B0` holds two of the sites. DamagePipeline §1.1
already gives the correct count.

### 2.5 Rules for what counts as evidence

1. **Hash-bound addresses.** An RVA is evidence only for the restored
   executable's hash. The build label in filenames is not hash evidence.
2. **Function claims need a body.** A claim about what a function does
   needs a `functions` row at its RVA with status `decompiled` or
   `decompiled_with_jumps`, a `code_path`, and no `JUMPOUT` or inline
   assembly in `traits`. Pseudocode is unreviewed decompiler output; it
   must be read, not just cited.
3. **No body means disassembly only.** Where a function has no corpus
   body, instructions read with Capstone from the restored executable
   (read-only) can support a claim. Such a claim is labelled
   disassembly-only, and the round-2 verifier kept those claims tagged
   "UNVERIFIED (exe-corroborated)". Where a body exists, instructions
   only recover what Hex-Rays dropped, such as float arguments.
4. **Offsets need a second source.** An offset must match one of the 14
   validated layouts or the GObjects runtime property dump. An SDK header
   alone is a lead, and placeholder types are not evidence.
5. **Labels are not ownership.** Map labels and vtable-slot aliases
   record membership, not ownership: identical-code folding shares one
   implementation across many slots. Names inferred from parameter shape
   are marked as inferences.
6. **Hard limits.** No `.i64` was opened during the cross-check or for
   this page. Static client code cannot establish server behaviour.

## 3. RVA status table

### How the table was built

1. Every `0x` token in
   [`Wardogs_DamagePipeline_v2.md`](../../Wardogs_DamagePipeline_v2.md) at
   `ac9b4b16` (branch `r6/veh`) was extracted with a regular expression.
   Values below `0x100000` are offsets, sizes or enum values and were
   dropped, as was the flag `0x40000000`. That left **103 RVAs**. The
   table was first built at `d560d33` (85 RVAs). Round 3's corrections
   added six, round 4's two, round 5's three and round 6's seven; none
   was dropped.
2. Each RVA was tagged with the numbered section (`##`/`###` heading)
   that cites it.
3. For each RVA, `corpus.sqlite` was queried read-only for:
   - the `functions` row at that exact RVA (`status`, `code_path`);
   - its `traits` row;
   - the enclosing row, when there was no exact match;
   - `aliases` and `failures`.

   The body text of each match was also searched for `JUMPOUT`, `__asm`
   and Hex-Rays warning lines.
4. RVAs without a body, plus every data RVA, were read from the restored
   executable with `pefile` and Capstone 5.0.7, read-only. Instructions
   were decoded at code RVAs; qwords and strings were read at data RVAs.
5. Statuses were checked against the round-1 and round-2 verifier
   ledgers (cited as r1/r2 row IDs) and DamagePipeline §11.
6. An independent verifier re-queried the corpus and re-read the bytes
   for every row (claims EV-1 to EV-12). It confirmed all of them,
   upgraded `0x5236E50` from `unverified` to `[exe]`, and confirmed the
   two misaligned citations. The eight RVAs added after `d560d33` went
   to the same verifier in round 5, which confirmed their statuses and
   the counts. The three round-5 additions (`0x6C98290`, `0x6F2C450`,
   `0x6F30E50`) are `corpus body` rows checked with `rva_status.py` at
   `349104e`; their roles come from the round-5 ledger (r5 T3-8). The
   seven round-6 additions were checked with `rva_status.py` at
   `ac9b4b16`; their roles and statuses come from the round-6 ledger
   (T2-5, T2-8, T2-12, T2-16, T2-18). "Verifier-confirmed round 6" means
   the verifier reproduced the body or the instructions itself;
   `0x6F35300` rests on the teammate's reading.

The corpus part can be re-run with `python -I` from any directory:

```python
import re, sqlite3
doc = open("Wardogs_DamagePipeline_v2.md", encoding="utf-8").read()
rvas = sorted({int(h, 16) for h in re.findall(r"0x[0-9A-Fa-f]+", doc)
               if 0x100000 <= int(h, 16) and int(h, 16) != 0x40000000})
db = sqlite3.connect("file:///E:/Reverse_Engineer/wardogs_analysis/"
                     "decompiled_cl516586_20261017_mmvpuc__/corpus.sqlite?mode=ro", uri=True)
for v in rvas:
    fn = db.execute("select status, code_path from functions where rva=?", (v,)).fetchone()
    tr = db.execute("select has_inline_assembly, has_jumpout from traits where rva=?", (v,)).fetchone()
    inside = None if fn else db.execute(
        "select rva from functions where rva<? and end_rva>? order by rva desc limit 1", (v, v)).fetchone()
    body = bool(fn and fn[0] in ("decompiled", "decompiled_with_jumps") and fn[1] and tr == (0, 0))
    print(f"0x{v:X}", "body" if body else "-", fn, tr, inside and f"in 0x{inside[0]:X}")
```

The same query, with section and line numbers and the PE section, is
[`_tools/rva_status.py`](../../_tools/rva_status.py), shared with the
[vehicle](vehicles.md) and [effects](effects.md) pages:

```text
python -I _tools/rva_status.py Wardogs_DamagePipeline_v2.md --rev ac9b4b16 --exe
```

Status key:

- **`corpus body`**: a `functions` row with a body at that exact RVA,
  with no `JUMPOUT` or inline assembly.
- **`[exe]`**: instructions or data bytes in the restored executable
  only, with no corpus body at that RVA. This covers instruction anchors
  inside a body, functions with no row, and every data address.
- **`GObjects`**: an offset or value backed by the runtime property dump.
- **`unverified`**: none of the above has been reproduced.

### Status counts

| Status | RVAs |
|---|---:|
| `corpus body` | 64 (4 of them cite or sit on the two misaligned rows) |
| `[exe]` | 39 (32 code, 7 data) |
| `GObjects` | 0 |
| `unverified` | 0 |
| **Total** | **103** |

These are the RVAs DamagePipeline cites at `ac9b4b16`. The eight cited
after `d560d33` were checked the same way and are in the table:
`0x6EF9450` and `0x6F08CE0` (the real entries behind the two misaligned
rows, whose bodies they are), `0x6B8E100`, `0x6BB6160`, `0x6B17D20` and
`0x6B83270` (`corpus body`), and `0x12CC0D0` and `0x12CC0F0` (`[exe]`,
FName initializers).

No cited RVA is itself a GObjects fact. The GObjects-backed items are
offsets that sit next to these RVAs. Examples are the event's `Amount`
(`+0x0`) and `ModificationResults` (`+0x190`), read at `0x6F02EC0` and
`0x6BB6FB0`, and the game-settings fallback `+0x378`/`+0x380`, read at
`0x6BB6A60`. They are listed with their sources in
[DamagePipeline §11](../../Wardogs_DamagePipeline_v2.md#offsets-and-engine-details-cross-checked).

### Table

Sections are DamagePipeline sections at `ac9b4b16`. Rows marked "(data)"
are not functions.

| RVA | Role | Cited in | Verification status |
|---|---|---|---|
| `0x12CC0D0` | FName initializer: `Client_ForceTakeHitCue` (UTF-16 at `0xB40F740`) | §10 | `[exe]`: `lea rdx, [rip+…]; lea rcx, [rip+…]; jmp 0x1725770` |
| `0x12CC0F0` | FName initializer: `Client_TriggerHitMarker` (UTF-16 at `0xB40F7E8`) | §10 | `[exe]`: same shape as `0x12CC0D0` |
| `0x1587900` | `TSparseArray::AddUninitialized`; it appends, so groups run in insertion order | §11 | `corpus body` |
| `0x395ADE0` | `UGameplayTagsManager::Get`, called by the parent-tag step | §11 | `corpus body` |
| `0x395F4D0` | Parent-tag step, `FGameplayTag::RequestDirectParent` | §11 | `[exe]`: no functions row; calls `0x395ADE0` at `0x395F4EB` |
| `0x3A93090` | `AActor` slot 231, `FindComponentByClass` (the armor op's `+0x738` call) | §11 | `corpus body` |
| `0x52311D0` | Adds the delta to the attribute value, then calls `SetAttributeBaseValue` | §10, §11, Change log | `[exe]`: no functions row (r2 HP-10) |
| `0x5236AF0` | `SetAttributeBaseValue` | §10, §11 | `[exe]`: no functions row (r2 HP-10, HP-14b) |
| `0x5236E50` | Base-value setter: hook, store, replication push | §10, §11 | `[exe]`: no aligned row (`0x5236E4A` is misaligned); reproduced by the verifier for this page (r2 HP-11 had left it unverified) |
| `0x53202B0` | Vehicle section pick (`ApplyDamageEvent`); §11 lists it as having no body | §11 | `[exe]`: no aligned row (`0x53202AB` is junk); sole caller `0x6B7FE50` |
| `0x6B17760` | `UWDCharacterVitalityComponent` damage handler | §10 | `corpus body` |
| `0x6B17D20` | Character health hook (`UWDCharacterVitalityComponent` slot 161): clamp to `[0, MaxHealth + MaxOverhealHealth + MaxDecayHealth]`, at least 1 while `bInvincible` | §10 | `corpus body` |
| `0x6B52A40` | `Auth_GetArmorDamageEvent`: target hook that filters armor tags | §7.6 | `corpus body` |
| `0x6B53000` | Armor break/crack caller of `ModifyDamage` | §1.1 | `corpus body` |
| `0x6B70D80` | Distance-falloff scale, direct hit | §7.6 | `corpus body` |
| `0x6B725B0` | Projectile-impact path: builds the bullet event and calls `ModifyDamage` twice | §1.1, §7.6, Change log | `corpus body` |
| `0x6B72D53` | Start of the per-custom-hit distance-scale range (inside `0x6B725B0`) | §7.6 | `[exe]` |
| `0x6B72DCB` | End of that range (inside `0x6B725B0`) | §7.6 | `[exe]` |
| `0x6B7330C` | Call site of `0x6B70D80` for the direct hit (inside `0x6B725B0`) | §7.6 | `[exe]` |
| `0x6B81CE0` | Creates the `Attribute.Gameplay.Health` handle (`+0x140`) | §10 | `corpus body` |
| `0x6B82520` | `UWDVitalityComponent` base damage: the health write | §10 | `corpus body` |
| `0x6B83270` | Base health hook (`UWDVitalityComponent` slot 161): clamp to `[0, MaxHealth]` | §10 | `corpus body` (a leaf with no `.pdata` entry) |
| `0x6B8E100` | Projectile instance constructor; sets the `+0x101` byte to 1 and the empty ammo tag at `+0xF0` | §7.6, §7.9 | `corpus body` |
| `0x6B92900` | Back-blast source; one if/else calls `0x6F042A0` (shooter on foot) or `0x6F06EB0` (shooter seated, `0x6E6EBA0`) | §1.1, §9 | `corpus body` (branch condition verifier-confirmed round 6, T2-12) |
| `0x6BB4D30` | Builds a WD damage event; used by every caller | §1.1 | `corpus body` |
| `0x6BB5D20` | Requirement-container match | §1, §4 | `corpus body` |
| `0x6BB5DC0` | `TSet::Emplace` | §11 | `corpus body` |
| `0x6BB5ED0` | Group insertion | §11 | `[exe]`: no functions row; tail-jumps to `0x6BB5DC0` at `0x6BB5F2C` |
| `0x6BB5F40` | Fallback sort | §1 | `corpus body` |
| `0x6BB6160` | `UWDGlobalDamageSystem` constructor; sets `RootDamageTag` to `Meta.Damage` | §5 | `corpus body` |
| `0x6BB61A0` | Per-group sort | §1, §5 | `corpus body` |
| `0x6BB6730` | Match a row's entries and append the selected ones | §1, §4 | `corpus body` |
| `0x6BB6A50` | Callback thunk to `0x6BB6730` | §1 | `corpus body` |
| `0x6BB6A60` | Collector; global vtable slot 87 (`+0x2B8`) | §1, §4, §5, §11 | `corpus body` |
| `0x6BB6FB0` | Global evaluator; slot 86 (`+0x2B0`) | §1, §5, §6 | `corpus body` |
| `0x6BB7153` | Loads the abs mask for the recording threshold (in `0x6BB6FB0`) | §6 | `[exe]` |
| `0x6BB715C` | Loads the `1e-8` threshold (in `0x6BB6FB0`) | §6 | `[exe]` |
| `0x6BB72DE` | Superseded anchor: the instruction before `0x6BB72E1` | §11 | `[exe]` |
| `0x6BB72E1` | `C` into `xmm2` for the adapter (in `0x6BB6FB0`) | §2, §6, §11, Change log | `[exe]` |
| `0x6BB72F8` | Custom return stored (in `0x6BB6FB0`) | §6 | `[exe]` |
| `0x6BB72FD` | `addss` custom delta (in `0x6BB6FB0`) | §6 | `[exe]` |
| `0x6BB7306` | Operation enum switch (in `0x6BB6FB0`) | §6 | `[exe]` |
| `0x6BB7324` | Ongoing: `Amount *= 0.01f` (in `0x6BB6FB0`) | §6 | `[exe]` |
| `0x6BB7329` | Ongoing: `delta *= C` (in `0x6BB6FB0`) | §6 | `[exe]` |
| `0x6BB732F` | Starting: `Amount *= 0.01f` (in `0x6BB6FB0`) | §6 | `[exe]` |
| `0x6BB7334` | Starting: `delta *= S` (in `0x6BB6FB0`) | §6 | `[exe]` |
| `0x6BB733C` | `addss` non-custom delta (in `0x6BB6FB0`) | §6 | `[exe]` |
| `0x6BB7344` | Recording-threshold compare (in `0x6BB6FB0`) | §6 | `[exe]` |
| `0x6BB73E7` | Final `maxss` clamp at 0 (in `0x6BB6FB0`) | §6 | `[exe]` |
| `0x6BB7900` | Custom-operation dispatch adapter | §1, §2, §11 | `corpus body` |
| `0x6BB7B30` | Reflected `exec_GetModificationAmount` | §1 | `corpus body` |
| `0x6BB7E10` | `PlayerArmorDurability` override (slot 86) | §7.5, §11 | `corpus body` |
| `0x6BB8970` | Category priority lookup | §1, §5 | `corpus body` |
| `0x6BBA900` | `GetProjectileStats(AmmoModifierTag)` | §7.6, §7.9 | `corpus body` |
| `0x6C255B0` | Impact-speed scale | §7.6, §11 | `[exe]`: no functions row (r2 BE-4) |
| `0x6C2A5F0` | `IWDDamageable` dispatch on the apply path | §1.1, §10 | `corpus body` |
| `0x6C2A790` | `IWDDamageable` slot 8 radial-hit filter: keeps one hit per component | §1.1 | `corpus body` (r5 T3-2, verifier-confirmed round 5; character use verifier-confirmed round 6, T2-8) |
| `0x6C98290` | `IWDWeaponOwner` `+0x90` (ranged-weapon slot 192): builds `Meta.Damage.AmmoModifier.<type>` from the loaded round's item tag | §7.9, Change log | `corpus body`; [exe] interface table `0xB389AB8+0x90` (r5 T3-8, verifier-confirmed round 5) |
| `0x6C98496` | `cmp ebx, 5; jne 0x6C98599`: a five-level item tag gives a two-name `<type>` (in `0x6C98290`) | §7.9 | `[exe]` anchor (r6 T2-5, verifier-confirmed round 6) |
| `0x6CA8730` | Explosive-actor caller of `ModifyDamage`; on a character, the thrown object's contact damage (`Kinetic.Impact.Throwable`, `DamageType.Impact`) | §1.1 | `corpus body` (verifier-confirmed round 6, T0-13; character contact path r6 T2-8) |
| `0x6CAB030` | Explosive actors' slot 236; calls `0x6CA8730` | §1.1 | `corpus body` |
| `0x6E6BD90` | `AWDMoverCharacter` / `AWDMoverPlayerCharacter` caller (slot 417 / 422), bool 1 | §1.1 | `corpus body` |
| `0x6E6DCC0` | Character `IWDDamageable` slot 8 (sub-vtable `0xB40C038`): empties the radial hits while the seat flag (`+0x3D0`) is clear, else `0x6C2A790` | §1.1 | `corpus body` (r6 T2-8, verifier-confirmed round 6) |
| `0x6E6EBA0` | Shooter's vehicle: `VehicleOperatorComponent` (`+0x768`) → `CurrentSeat` (`+0x188`) → `0x532DD70` | §1.1, §9 | `[exe]`: no functions row; `mov rcx, [rcx+0x768]; add rcx, 0x188; jmp 0x532DD70` (r6 T2-12, verifier-confirmed round 6) |
| `0x6E72D90` | Unnamed caller, bool 1 | §1.1 | `corpus body` |
| `0x6E74C40` | `ReceiveDamage` (interface slot 2), jumps to the vitality component | §10 | `corpus body` |
| `0x6E77C40` | Character `TakeDamage` override | §10 | `corpus body` |
| `0x6E7F0B0` | `ProcessEvent` stub, parameter shape of `Client_ForceTakeHitCue` | §10 | `corpus body` |
| `0x6E7F420` | `ProcessEvent` stub, parameter shape of `Client_TriggerHitMarker` | §10 | `corpus body` |
| `0x6EF8DE0` | Event to `FWDModifyDamageData` conversion | §1, §11, Change log | `[exe]`: no functions row; sole caller `0x6F02EC0` |
| `0x6EF8E2C` | Loads the event's `Amount` (`+0x0`) (in `0x6EF8DE0`) | §1 | `[exe]` |
| `0x6EF8E37` | Stores it as `ModifyDamageData.Amount` (in `0x6EF8DE0`) | §1 | `[exe]` |
| `0x6EF944F` | Builds the Unreal damage event | §1.1 | `corpus body`, misaligned: the entry is `0x6EF9450` |
| `0x6EF9450` | Real entry of the Unreal damage-event builder (row `0x6EF944F`) | §1.1, Change log | `corpus body`, misaligned: filed under row `0x6EF944F` |
| `0x6EF9840` | Apply step: `WDDamageable` path or `TakeDamage` | §1.1 | `corpus body` |
| `0x6EFFD40` | Selects the first active damage system | §1 | `corpus body` |
| `0x6F01BB0` | Hit-location lookup: asset by actor class (`ClassToHitLocations`), then an exact bone-name match; called by the armor hook | §7.6 | `corpus body`; [exe] call `0x6B52B8B`, store `0x6B52BB1` (r6 T2-16, T2-18, verifier-confirmed round 6) |
| `0x6F02EC0` | Native `UWDDamageSubsystem::ModifyDamage` | §1, §1.1 | `corpus body` |
| `0x6F03F60` | Vehicle-supply-container caller | §1.1 | `corpus body` |
| `0x6F042A0` | Back-blast caller, on-foot branch of `0x6B92900` | §1.1, §9, §11, Change log | `[exe]`: row status `failed` (call analysis failed); call at `0x6F0526C` |
| `0x6F06540` | Radial-damage caller | §1.1 | `corpus body` |
| `0x6F06EB0` | Seated back-blast caller: synthetic hits on that vehicle's occupants | §1.1, §9, Change log | `corpus body` (targets verifier-confirmed round 6, T2-12) |
| `0x6F07C10` | Reflected `BP_DamageActor`; skips `ModifyDamage` | §1.1 | `corpus body` |
| `0x6F08A60` | Reflected `exec_ModifyDamage` | §1, §1.1 | `corpus body` |
| `0x6F08CDC` | Reflected `SimpleDamageActor` | §1.1 | `corpus body`, misaligned: the registered entry is `0x6F08CE0` |
| `0x6F08CE0` | Registered entry of the reflected `SimpleDamageActor` (row `0x6F08CDC`) | §1.1, Change log | `corpus body`, misaligned: filed under row `0x6F08CDC` |
| `0x6F09210` | Reflected `SimpleDamageActorWithInstigatorController` | §1.1 | `corpus body` |
| `0x6F2AAA0` | Projectile subsystem set-up: fills the ammo-modifier map with the five `Meta.Damage.AmmoModifier.*` tags | §7.9 | `corpus body` (L202–236; r6 T2-5, verifier-confirmed round 6) |
| `0x6F2C450` | Predicted projectile simulation: ammo tag from `FWDProjectileSimulationSetup.AmmoModifierTag` | §7.9 | `corpus body` (r5 O-8; verifier-confirmed round 6, T0-19) |
| `0x6F30E50` | Projectile spawn: copies the ammo tag from the spawn parameters (`+0x40`) to instance `+0xF0` | §7.9, Change log | `corpus body` (L22; r5 T3-8, verifier-confirmed round 5) |
| `0x6F35300` | Ammo-modifier lookup in the projectile subsystem map (`+0x480`); empty tag when absent | §7.9 | `corpus body` (r6 P-5, teammate's reading; not re-run by the verifier, T2-5) |
| `0x7635EA0` | Vehicle supply containers' slot 127; calls `0x6F03F60` | §1.1 | `corpus body` |
| `0x76740F0` | Unnamed caller | §1.1 | `corpus body` |
| `0x768ED20` | `UWDVehicleOperatorComponent` slot 161 caller | §1.1 | `corpus body` |
| `0x7692B60` | `UWDVehicleOperatorComponent` slot 160 caller | §1.1 | `corpus body` |
| `0x76F5AE0` | Unnamed caller, bool 1 | §1.1 | `corpus body` |
| `0xB3217D0` | **Vtable (data):** `UWDGlobalDamageSystem_VFT`; `+0x2B0` = `0x6BB6FB0`, `+0x2B8` = `0x6BB6A60` | §1 | `[exe]` |
| `0xB322038` | **Registration pair (data):** name pointer to `"GetModificationAmount"`, code `0x6BB7B30` | §1 | `[exe]` |
| `0xB322140` | **Vtable (data):** `PlayerArmorDurability`; `+0x2B0` = `0x6BB7E10` | §7.5 | `[exe]` |
| `0xB40C038` | **Interface vtable (data):** `IWDDamageable` in `AWDMoverCharacter`; `+0x10` = `0x6E74C40` | §10 | `[exe]` |
| `0xB410D20` | **Interface vtable (data):** `IWDDamageable` in the player class; `+0x10` = `0x6E74C40` | §10 | `[exe]` |
| `0xB432298` | **String (data):** registration name `"ModifyDamage"` | §1 | `[exe]` |
| `0xB434AD0` | **Registration pair (data):** name `0xB432298`, code `0x6F08A60` | §1 | `[exe]` |

### Notes on particular rows

- **`0x6EF944F` (misaligned).** The corpus row starts one byte before the
  real entry. All 11 direct callers in the corpus target `0x6EF9450`, which begins with
  `mov [rsp+8], rbx`. Decoding from `0x6EF944F` gives a bogus first
  instruction, and Hex-Rays warns that "positive sp value has been
  detected, the output may be wrong". The rest of the body decodes the
  same code. DamagePipeline §1.1 now cites `0x6EF9450`.
- **`0x6F08CDC` (misaligned).** The reflected `SimpleDamageActor`
  registration points at `0x6F08CE0`. The corpus row at `0x6F08CE0` failed
  with "Candidate entry lies inside another function at RVA `0x6F08CDC`",
  and the bytes at `0x6F08CDC` are not a prologue. The body at
  `0x6F08CDC` does contain the `ModifyDamage` call at `0x6F090F1`.
  DamagePipeline §1.1 now cites `0x6F08CE0`.
- **`0x5236E50`.** The only corpus row nearby (`0x5236E4A`) is
  misaligned, so there is no body. Round 2 left the setter unverified (r2
  HP-11). For this page the verifier reproduced it from the disassembly:
  - a per-attribute hook lookup at `+0x378` (call through `[rax+0x58]`);
  - the base store `movsd [rdi+0x28], xmm6`;
  - on role 3, `lea rcx, [rbx+0x3D8]; call 0x52382E0` (the replication
    push), then the dirty mark and flush.

  It is now `[exe]`.
- **`0x53202B0`.** DamagePipeline cites it only in §11, as a function
  without a corpus body; its behaviour belongs to the
  [vehicle pipeline](../../Wardogs_VehicleDamagePipeline_v1.md). Its only
  indexed caller is `0x6B7FE50` (site `0x6B7FF49`). The verifier found
  that `0x53202B0` itself calls `0x5320400` (at `0x53203D0`). The exec
  thunk `0x5341430` repeats the section pick inline and calls `0x5320400`
  directly; it does not reach it through `0x53202B0`. The vehicle
  pipeline's §4 step 1 now says so.
- **Disassembly-only functions.** `0x52311D0`, `0x5236AF0` and
  `0x6C255B0` keep the round-2 tag "UNVERIFIED (exe-corroborated)" (r2
  HP-10, HP-14b, BE-4), which this table records as `[exe]`.
- **DamagePipeline §11's body-less list.** It first named only
  `0x53202B0`, `0x52311D0`, `0x5236AF0` and `0x6C255B0`. It now also
  names the four other cited functions with no corpus body at their
  entry (`0x5236E50`, `0x6EF8DE0`, `0x6BB5ED0`, `0x395F4D0`) and
  `0x6F042A0`, whose row failed to decompile.

### RVAs cited only by the evidence notes

These appear in the merged notes but not in DamagePipeline. They were
checked the same way.

| RVA | Role | Status |
|---|---|---|
| `0x15B83B0` | Base `GetModificationAmount`; returns 0.0 (`xorps xmm0, xmm0; ret`) | `corpus body` |
| `0x178DF10` | Slot-89 active predicate, shared by identical-code folding with unrelated classes | `corpus body` |
| `0x18FCDB0` | Delegate broadcast; internals open | `corpus body` |
| `0x6BB7479` | Exclusive end of the inspected evaluator range (the `functions` row's `end_rva`) | Not an instruction anchor |
| `0x6F02F3A` | Slot-86 indirect call in `ModifyDamage` (`call r9`) | `[exe]` |
| `0x6F08B42` | Exec's direct call to `0x6F02EC0` | `[exe]`; also in `calls` |
| `0xB321D30` | **Vtable (data)** shared by `UWDCustomDamageModificationOperation` and `UWDCustomAttributeModification`; `+0x2B0` = `0x15B83B0` | `[exe]` |

The dump-reconstructed PE addresses in §2.2 (`0x977EB60`, `0x9B0DEE8`,
`0xCD05020`, `0xB434758`, and the three vtable RVAs as sampled there)
describe a different hash. They are not given a status here.

## 4. History

Times are commit times (+02:00), or file times in the local work
directories.

| When | Pass or change | Established or corrected |
|---|---|---|
| 2026-10-16 23:49 | DamagePipeline v1 (`f4568b6`) | Initial SDK/data map |
| 2026-10-16 23:56 | Export audit baseline (`5b036b0`) | Data shape of the rule tables (§2.1); trace brief B-1 to B-4 written from it |
| 2026-10-17 00:14–00:18 | Pass 1, dump-reconstructed PE | No usable code; the map has one unrelated exec record; the capture has no main-module bytes (§2.2) |
| 2026-10-17 00:29 | Restored-exe validation (`70850fc`) | Map RVAs match the restored executable; damage vtables hold code pointers ([validation](../RESTORED_EXE_VALIDATION.md)) |
| 2026-10-17 00:29–00:33 | Pass 2, restored-executable trace | Call path, matching, per-group sort and B-2 arithmetic; group order and the conversion left open |
| 2026-10-17 00:39–01:38 | Corpus export | 437,174 candidates; `final_verification.json` passed |
| 2026-10-17 01:26 | Notes committed (`4b4a7b6`) | The three earlier notes and the corpus page enter the repository |
| 2026-10-17 02:21 | DamagePipeline v2 (`4440146`) | Single behaviour reference; corrected the GObjects reading of the second parameter (running `C`, not `S`) |
| 2026-10-17 02:43–03:26 | Bullet event and health write | Projectile path, per-weapon tables, character health write (DamagePipeline §7.6–7.9, §10) |
| 2026-10-17 07:34 | Pass 3, corpus cross-check (`362a0b1`) | Confirmed pass 2; added the base override, the armor op, the shared vtable and the schema gap; listed unverified items |
| 2026-10-17 07:36 | DamagePipeline closes the cross-check items (`8e3c4c3`) | Offsets confirmed against GObjects; `S` is the event amount; group order is insertion order; anchor `0x6BB72E1` |
| 2026-10-17 07:39 | Restored and brief notes updated (`89cbd41`, branch `docs/close-crosscheck-items`, not merged) | The same closures applied to the notes; only `0x18FCDB0` left open |
| 2026-10-17 08:14 | Round-2 verifier corrections (`d560d33`) | Corrected the bullet-event and health-write details; marked four functions without corpus bodies as disassembly-only |
| 2026-10-17 | This page | Merged the three notes; built the RVA status table (§3); found the two misaligned rows and corrected the call-site count |
| 2026-10-17 | Round-3 corrections applied to DamagePipeline | Cites `0x6EF9450` and `0x6F08CE0`; §11 lists every body-less function; `RootDamageTag`, the `+0x101` byte, the two player-character stubs and the role-3 decay-pool cut added |
| 2026-10-17 20:54 | Round-4 corrections (`e057d26`) | Cite the two vitality slot-161 clamps (`0x6B17D20`, `0x6B83270`); this table refreshed at `e057d26` (93 RVAs), with the six round-3 additions folded in |
| 2026-10-17 | Round-5 corrections (`349104e`) | The ammo-tag writer `0x6F30E50`, the fire-path builder `0x6C98290` and the simulation path `0x6F2C450` (§7.9); back-blast branch question O-8; this table refreshed at `349104e` (96 RVAs) |
| 2026-10-18 | Round-6 corrections (`ac9b4b16`) | The back-blast branch is the shooter's seat (`0x6E6EBA0`; O-8 closed); radial damage on characters (`0x6E6DCC0`, `0x6C2A790`); the ammo `<type>` rule (`0x6C98496`, `0x6F2AAA0`, `0x6F35300`); the armor hook's bone lookup (`0x6F01BB0`); this table refreshed at `ac9b4b16` (103 RVAs) |

## 5. Open items

- Delegate broadcast internals (`0x18FCDB0`): the container layout is
  opaque. No document depends on it.
- Duplicate-row effects in the collector are not traced.
- The gameplay meaning of `ModifyDamage`'s bool, and which damage system
  an actual event selects, are open
  ([DamagePipeline §1](../../Wardogs_DamagePipeline_v2.md#1-call-path)).
- Network authority is outside static analysis
  ([DamagePipeline §9](../../Wardogs_DamagePipeline_v2.md#9-open-questions-and-what-closes-them)).

[infantry]: https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json
[categories]: https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DA_GlobalDamage_Categories.json
[bones]: https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_BoneDamageModifiers.json
[seats]: https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json
