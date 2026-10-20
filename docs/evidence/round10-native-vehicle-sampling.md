---
title: Round 10 native vehicle sampling
nav_exclude: true
---

# Round 10 native vehicle sampling

The corrected default **Points** fixture covers all **36 published physical vehicle models**, including the 18 previously excluded wheel models. Format 2 contains **204 represented nodes, 1,131 authored socket targets and 143 bounds-origin targets**. Its 78 wheel instances belong to **18 shared native components**. This establishes reference-pose input coverage and corrects the recovered sampling policy; it does not establish in-game contact or damage parity. Overall integration, test results and open reproductions belong in the [Round 10 vehicle blast audit](round10-vehicle-blast-audit.md).

## Frozen-build evidence

The matching offline image is `E:/Reverse_Engineer/wardogs_analysis/WardogsClient-Win64-Shipping.restored.exe`, SHA-256 `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`, image base `0x140000000`. All addresses below are RVAs. Corpus text comes from read-only `decompiled_cl516586_20261017_mmvpuc__/corpus.sqlite`; decisive claims were checked against raw PE bytes and Capstone disassembly. No game process or IDA database was opened.

External artifacts are under `E:/Reverse_Engineer/wardogs_analysis/round10_vehicle_ism_20261020`. The native policy report retains 21 bounded raw spans, their bytes, hashes and disassembly. SDK offsets and local UE source aided interpretation; the matching binary establishes the behavior described here.

| Evidence | Exact native path |
|---|---|
| Default Points dispatch | `0x6EFFDC0` selects `0x6EFD9C0` for mode `2` with a nonempty cloud; other modes have separate rules |
| ISM class branch | `0x3A39990` identifies `InstancedStaticMeshComponent`; tested by `0x6EFD9C0` |
| Ordinary bounds | Static-mesh-component CalcBounds `0x3DB5AB0`; mesh GetBounds `0x44C2BA0` copies authored `ExtendedBounds` at mesh `+0x250` |
| ISM aggregate bounds | Vtable `0xA4DBDD8`, slot `+0x598` → `0x3F5AF30` → `0x3F6DBC0` → `0x3F5B100`; union at `0x2835B30` |
| BoundsScale default | Primitive constructor instruction `0x3D0F5F0` writes float `1` at component `+0x344` |
| Cloud angle mask | `0x6EFDA34–0x6EFDAC5` supplies bounds and angle to `0x6F030A0`; cloud traversal `0x6F03340` consumes the mask |
| Per-target retention | `0x6EF7950` → callback `0x6EF6EE0` → `0x6F03720` → `0x6EF70D0` |
| Actor ordering and filtering | Producer `0x6EFFDC0` sorts through `0x6B6FFD0`; consumer `0x6F042A0` invokes damageable filter `+0x40` at `0x6F04E3A`, resolving to `0x6C2A790` |

## Instance targets and identity

The producer groups overlap records by native component and retains their Item entries in encounter order. The Points ISM branch requires `0 <= Item < PerInstanceSMData.Num` at component `+0x668`. It loads the 128-byte instance matrix from `+0x660 + Item*128` and composes it with ComponentToWorld at `+0x210`.

With matching damage-query sockets, targets are transformed for each overlapped instance and sorted within that instance by float squared distance from the explosion origin. Without sockets, the target is that instance's transformed **authored mesh bounds origin**, rather than the aggregate component bounds origin. All 78 wheel instances represented here have zero matching damage-query sockets.

The candidate retains a pointer to its overlap Item. In the normal target-component acceptance branch, raw instructions `0x6F03A60–0x6F03A75` compare hit `Item` at `FHitResult+0xA8` with the requested Item and reject mismatches. Optional special-actor acceptance precedes this branch and remains a separate contextual policy.

Fixture keys such as `component[0]` make per-node records unique. Their `component` field remains the **shared native identity**; `node_index` and `instance_index` identify the displayed placement and reference instance. Model-level `instance_groups` binds the ordered instance/node lists and common aggregate bounds. Independent wheel components must not be fabricated from these keys.

## Bounds and cloud angles

For an ordinary static mesh, let local bounds be origin `o`, extent `e`, sphere radius `r`, and world transform be linear part `M` plus translation `t`. Native CalcBounds computes world origin `M o + t`, extent `abs(M) e`, and radius `min(length(world extent), r * max(world basis length))`. BoundsScale multiplies extent and radius. Its native default is `1`, with no serialized override found in the 33 source variant assemblies.

ISM aggregate bounds use **every currently present instance**, without an overlap or collision-active predicate in this loop. Each authored mesh box is transformed to a world box; its initial sphere radius is the world-box extent length. Instances are then combined in array order. For two bounds, native union computes:

```text
minimum = min(a.origin - a.extent, b.origin - b.extent)
maximum = max(a.origin + a.extent, b.origin + b.extent)
origin = (minimum + maximum) / 2
extent = (maximum - minimum) / 2
radius = min(length(extent),
             max(distance(a.origin, origin) + a.radius,
                 distance(b.origin, origin) + b.radius))
```

Thus an instance whose collision is inactive still contributes if it remains in PerInstanceSMData. Source-reference membership cannot prove which instances remain during every runtime tyre transition.

Points chooses **90° outside the component bounds sphere and 180° inside**, using a radius guard of approximately `0.0001 cm` (`0.000001 m`). Raw constants are at `0x9AD4848` and `0x9AD4858`. Helper `0x6F030A0` normalizes the bounds-origin and cloud-start directions from the explosion origin, takes their clamped dot product through acos, and compares degrees directly against the supplied angle. Cloud indices `0` and `1` are exempt. There is no fixed 10° cap in this helper. Earlier fixed-10° fixture reasoning mixed settings from separate paths and is superseded for default Points.

## Gather, sort, filter and tag deduplication

The complete ordering matters: **gather target hits → sort actor hits by float Distance → filter duplicate components with swap removal → deduplicate hit-location tags → apply damage**. Keeping all eligible targets does not mean applying all of their hits.

`0x6EF7ACB` resets the retained result index to `-1` inside every target iteration. `0x6EF70D0` therefore retains the strict closest accepted original-origin Distance across cloud starts **for that target**, rather than across all targets of the component. The actor producer subsequently sorts collected hit records by Distance using `0x6B6FFD0`.

Vehicle filter `0x6C2A790` records the first encountered component pointer from hit `+0xD8`. Later duplicates are removed by copying the final array entry into the duplicate's slot, decrementing the array and rechecking that slot. It does not compare distances. For initially sorted `[A0, A1, A2, B0, B1, C0]`, with repeated letters denoting components, it retains **`[A0, C0, B1]`**: swap removal exposes the farther B candidate before B's nearer candidate. Independent per-component minima would instead choose B0.

This supersedes the Round 8/9 claim that nearest accepted retention across all component targets fully described the native result. The first retained valid actor hit is distance-derived, rather than based on GLB node order; subsequent order can change through swap removal. Hit-location tag deduplication then retains applications according to that filtered order. The damage application path's actor/tag gate at `0x6F06B10` must not be replaced with one application per display node.

Target sort keys and hit Distance are floats. Equal keys, native unstable sort behavior, overlap encounter order and subsequent swaps remain ordering limits. Reference fixtures cannot recover a live equal-distance ordering from source data alone.

## Artifacts, validation and limits

| Artifact under the external root | SHA-256 |
|---|---|
| `candidate-sampling-fixture-v4.json` | `f48bb064aa586142a96211413688aba470a1791bce0adcc2ede49eadcca00041` |
| `native-ism-policy-v1.json` | `74620e2441ea57117c160797ca26b14c96c9be4b6983141f13084b5a6fd5a987` |
| `aggregate-sphere-validation-v2.json` | `ebdc386c61597555b366b43a2b6499613ee02221a061d8c064ef92d589cb1c59` |

The fixture hash-binds source inputs and native proof. `README.md`, `summary-v2.json`, `build_ism_evidence_v1.py` and `correct_ism_bounds_v4.py` preserve the restart recipe. V4 corrects per-instance diagnostic sphere fields to the native ISM box-diagonal rule; V3 already had the correct aggregate spheres. An independent eight-corner transform and ordered union check matches all 18 aggregate origins, extents and radii within `4.44e-16 m`. Bound artifact hashes and all 98 unique represented static-mesh JSON hashes were verified.

Source frames come from fresh skeletal exports and serialized component/socket metadata, without using compressed GLB node matrices. Skeletal reference matrices round to five decimal places in glTF units. Prior placement checks cover all 204 node/variant rows, with maximum published-geometry bound difference **0.573 mm**. Shared variants have equal source rows; this is reference-pose placement validation, not exact runtime transform provenance.

Instance indices describe homogeneous **all-intact or all-destroyed** wheel states. Partial tyre destruction can remap native indices and is unsupported here. Native overlap membership and encounter order remain runtime inputs; display CC overlap tests and LOS remain approximations. Steering, suspension, deployment, collision masks, omitted query components, special actor acceptance and synthetic no-hit policies can change actual contacts. Complete authored-input coverage and recovered ordering do not close those boundaries or establish game parity.
