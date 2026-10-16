# Damage IDA pass — input validation results

**Historical input:** this report concerns `WardogsFullDump_fixed.exe`.
The later [restored-executable trace](DAMAGE_IDA_RESTORED.md) recovered
the native evaluator and partially resolved ordering using a different hash.

Recorded 2026-10-17. The offline IDA pass ran successfully against an owned
copy of the reconstructed PE. **B-1 and B-2 remain unresolved:** the
inspected artifacts did not provide a usable damage implementation to
trace. No native call graph, modifier-order result, or damage pseudocode
was recovered. The [trace brief](DAMAGE_IDA_TRACE.md) remains the question
set, not a record of completed implementation analysis.

## Inputs and identity

| Artifact | Size in bytes | SHA-256 |
|---|---:|---|
| `WardogsFullDump_fixed.exe` | 234214912 | `97ec9e0d12ed4df164f95069d0243471d33bb2f2815e90c3b408f317a2b71543` |
| `5.7.4-516586+++Wardogs+Live-Wardogs.idmap` | 4942224 | `f4b2942331061187454b625821f8a6119b267551d22dc1cabbdf1a4f3ee1afdb` |
| Existing `Wardogs_1015.dmp` | 14177243536 | `92ccf844fb8ba7f98fea1f6b58786c8a43d45204dafab88ec4f3e1a5b3ba4f02` |

The PE and mapping originals were left unchanged. A byte-identical PE
copy and separate IDA database were created in the local research
workspace. The 14 GB capture was read in place and was not copied into
this repository. It is an existing recorded artifact, not a new capture.

The reconstructed PE declares AMD64/PE32+, preferred image base
`0x140000000`, image size `0xDF5D000`, and entry RVA `0x977EB60`.
Its import directory is declared at RVA `0xCD05020`, size `0x55`, but
`pefile` decoded zero import descriptors. Its exception-directory RVA
and size are zero. These are observations, not a diagnosis of their cause.

An exact ASCII and UTF-16LE search for `++Wardogs+Live-CL-516586` found
neither encoding in this PE. That bounded search does not authenticate
or disprove a build identity. The reconstructed PE has not been established
as the exact original binary matching the SDK and mapping.

## Mapping format and coverage

The mapping parses as Dumper-7 binary format version 2, using the
[published packed layout](https://github.com/Encryqed/Dumper-7/blob/main/Dumper/Generator/Public/Generators/IDAMappingLayouts.h).
The upstream [generator](https://github.com/Encryqed/Dumper-7/blob/main/Dumper/Generator/Private/Generators/IDAMappingGenerator.cpp)
records native exec-function RVAs. A read-only decoder checked section
boundaries, enum/structure records, and referenced length-prefixed strings.
No bulk symbol import was applied to IDA.

| Decoded record kind | Count |
|---|---:|
| Strings | 95999 |
| Enums | 3225 |
| Structures/classes | 21282 |
| Named globals | 3 |
| Vtables | 9134 |
| Native exec functions | 1 |

The sole exec-function record is `AActor::AddComponent`, RVA `0x9B0DEE8`.
There is no exec-function record for `ModifyDamage`, `GetModificationAmount`,
or `GlobalDamageSystem`. Rich type metadata therefore must not be treated
as comprehensive native function coverage.

## What IDA confirmed

IDA 9.3 loaded the owned PE copy; IDAPython ran and Hex-Rays initialized.
The command used autonomous mode and `-a` to disable auto-analysis. The
script inspected loader segments and bounded candidate bytes, then exited
0 through `ida_pro.qexit`. No target execution or debugger session occurred.

The sole mapped exec-function RVA falls in IDA's non-executable `.rdata`
segment for this input, not `.text`. Its label does not establish a usable
function in this image. The following damage-related mapping records
were also sampled in IDA:

| Mapping label | RVA | First eight 64-bit words: canonical x64 pointers |
|---|---:|---:|
| `UWDCustomDamageModificationOperation_VFT` | `0xB321D30` | 0/8 |
| `UWDGlobalDamageSystem_VFT` | `0xB3217D0` | 0/8 |
| `UWDDamageModificationOperation_PlayerArmorDurability_VFT` | `0xB322140` | 0/8 |
| `UWDDamageSubsystem_VFT` | `0xB434758` | 0/8 |

Every 64-byte IDA sample matched the copied PE's corresponding file bytes
in an independent comparison. These results rule out a byte discrepancy
introduced by this IDA load for those samples. They do not identify whether
the underlying limitation is protection, incomplete reconstruction, a build
mismatch, or another cause. The samples do not support treating these
locations as working function-pointer tables for the requested trace.

The first 64 KiB samples of `.text`, `.rdata`, and `.pdata` each measured
approximately 7.997 bits of entropy per byte. This corroborates unusual
sampled content but does **not** prove encryption or characterize every
page in those sections.

Whole-image auto-analysis and cross-reference construction were not
requested after these locator checks failed. No absence-of-callers claim
is made from an analysis database without that coverage. No function was
created or decompiled from these candidate locations, and no bytes were
patched to manufacture a plausible function.

## Existing recorded capture

`Wardogs_1015.dmp` is a readable MDMP artifact. Its module list identifies
`WardogsClient-Win64-Shipping.exe`, with module size `0xE15D000`. However:

- None of its 68650 `Memory64ListStream` ranges overlaps the named main
  module's address interval: captured module bytes in that stream are **0**.
- There is no separate `MemoryListStream` in its stream directory.
- The inspected damage RVAs and the module header therefore have no
  backing bytes in that captured module interval.

This is a module-coverage result, not an assessment of the other captured
modules or of why the main module is absent. The capture's module size and
timestamp also differ from the reconstructed PE's declarations. These
metadata differences are insufficient to establish a different game build,
but they prevent assuming the two inputs have a verified shared identity.

## Consequence for the research questions

| Question | Result | Evidence still needed |
|---|---|---|
| B-1 / DamagePipeline §7.1: filtering and evaluation order | Unresolved; no consumer body recovered | Readable, build-matched damage implementation and an established entry point |
| B-2 / §7.2: percentage/custom-return arithmetic | Unresolved; no operation branch recovered | Actual operation implementation and operand provenance |
| B-3 / §7.3: bone lookup/fallback | Still open; existing table coverage remains valid | Bound consumer or Blueprint body |
| B-4 / §7.5–7.6: helper bindings and return values | Still open; raw table enumeration remains valid | Readable consumer bodies/bindings |

The next useful input is a matching existing analysis database, readable
offline module image, or recorded artifact that actually contains the
relevant module pages. Validate its hash, correspondence, and candidate
code before repeating B-1/B-2. A mapping with only type information and
one unrelated exec-function record cannot substitute for that code.

There is no evidence here for a modifier-order formula, server-authority
guarantee, or vulnerability. Security-relevant findings still follow
[SECURITY.md](../SECURITY.md). This pass created no live session, loaded no
driver, and performed no game-state modification.

## Retained local evidence

The owned analysis directory is:

`E:/Reverse_Engineer/wardogs_analysis/ida_damage_20261017___e23tea/`

It retains the copied inputs, `WardogsFullDump_fixed.exe.i64`, IDA log,
and scoped validation scripts. Small result files can be checked against
these SHA-256 values:

| Result file | SHA-256 |
|---|---|
| `mapping_inventory.json` | `746da73a0e3d06ec7cfe99deabf278e34686b3eb12f3c197f8ffebd11f21208d` |
| `ida_probe_result.json` | `4c6f342b0ac160e1ce2132ff8adfcea0ac75063f49d3b45051f72fe264d24cea` |
| `recorded_capture_coverage.json` | `59704623c76425fca31b5a6ea72368cdaf418b56216fc5c9b0c9e6c4e4170a72` |

`source_validation.json` records the PE directory and entropy checks.
`input_manifest.json` identifies the original/copy hashes. These are
ordinary CLI/IDAPython evidence files, not REA MCP Evidence records.
