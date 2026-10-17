# Vehicle damage evidence: RVA status

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

This page records how strong the evidence is for each native address that
[VehicleDamagePipeline](../../Wardogs_VehicleDamagePipeline_v1.md) cites.
It follows the method of the
[damage evidence page](damage.md#3-rva-status-table) and does not restate
the vehicle rules. Nothing here is a runtime observation: no game was run
and no process or service was contacted. No claim is made about server
authority or exploitability; security questions go through
[SECURITY.md](../../SECURITY.md).

All addresses are **file RVAs in the restored executable**
`WardogsClient-Win64-Shipping.restored.exe` (SHA-256
`a5c3db10…0cc37`, image base `0x140000000`). The binary, map, corpus and
their hashes are listed in
[damage evidence §1](damage.md#1-binary-identity-and-hashes). The rules for
what counts as evidence are those of
[damage evidence §2.5](damage.md#25-rules-for-what-counts-as-evidence).

## 1. Method

1. Every `0x` token in
   [`Wardogs_VehicleDamagePipeline_v1.md`](../../Wardogs_VehicleDamagePipeline_v1.md)
   at `349104e` (branch `r5/veh`) was extracted. Values below `0x100000`
   are struct offsets, sizes or enum values and were dropped. That left
   **87 RVAs**. The page was first built at `479c6c1` (42 RVAs). Round 4's
   corrections added 20 RVAs, and `0x395F4D0` is no longer cited. Round
   5's corrections added 26.
2. Each RVA was tagged with the numbered section that cites it and the
   doc's line numbers at `349104e`.
3. For each RVA, `corpus.sqlite` was queried read-only for:
   - the `functions` row at that exact RVA (`status`, `reason`,
     `code_path`);
   - its `traits` row (inline assembly, `JUMPOUT`);
   - the enclosing row, when there is no exact one;
   - direct calls to it in `calls`, and its `aliases`.

   The body text was searched for `JUMPOUT`, `__asm` and Hex-Rays warning
   lines, and nullsub rows with an empty body were flagged.
4. For every RVA, the first instructions were decoded from the restored
   executable with `pefile` and Capstone 5.0.7, read-only, to check that a
   row starts on a real entry (a `.pdata` start or a registered or vtable
   pointer, with a normal prologue).
5. RVAs without a usable body were checked against the round-2 to
   round-4 verifier ledgers (cited as r2/r3/r4 row IDs; the ledgers are
   local working files) and against the
   [damage evidence table](damage.md#table). Where neither covered one,
   it was disassembled for this page.
6. At `479c6c1`, every status that is not a plain corpus body was sent to
   an independent verifier as claims EV-1 to EV-22, shared with
   [the effects page](effects.md). The verifier re-ran the queries and
   the disassembly and confirmed all 22 claims and both pages' counts.
   It recorded EV-21 and EV-22 as citation errors in the pipeline docs
   (notes below and on the effects page). The 20 RVAs added at `e057d26`
   went to the same verifier in round 5, which confirmed the RVA set,
   every status and the counts. All of their `[exe]` statuses rest on
   round-4 ledger rows, and the instruction at each anchor was decoded
   again for this page. The verifier corrected one role (`0x538ABD0`,
   which merges into `+0x180`, not `+0x1D0`).
7. The 26 RVAs added at `349104e` come from the round-5 ledger (rows
   T0-9, T3-1, T3-2, T3-5 to T3-8) and the teammate findings it checked
   (O-1 to O-8). Each status names its ledger row. "Verifier-confirmed
   round 5" means the verifier reproduced the body or the instructions
   itself. `0x5304690`, `0x6CA8730` and `0x6F2C450` rest on the
   teammate's reading only, and `0x76AB5F0` was disassembled again for
   this page.

The corpus part is
[`_tools/rva_status.py`](../../_tools/rva_status.py).
Run it with `python -I` from the repository root:

```text
python -I _tools/rva_status.py Wardogs_VehicleDamagePipeline_v1.md --rev 349104e --exe
```

It prints one tab-separated line per RVA: citing sections and lines, PE
section, `body` or `-`, row status and reason, call count, enclosing row,
aliases and flags. It opens the corpus with `?mode=ro` and writes nothing.
`--exe` only reads section headers from the executable.

### Status key

- **`corpus body`**: a decompiled `functions` row with no `JUMPOUT` or
  inline assembly. Misaligned rows and rows with Hex-Rays warnings are
  flagged in the table. A body filed under a misaligned enclosing row
  counts as `corpus body`; when that row carries a Hex-Rays warning, the
  claim rests on the instructions (see the notes).
- **`[exe]`**: instructions in the restored executable only. This covers
  functions with no row, failed or empty rows, and instruction anchors
  inside a body.
- **`GObjects`**: an offset or value backed by the runtime property dump.
- **vtable/data**: bytes at a data address.
- **`unverified`**: none of the above has been reproduced.

## 2. Status counts

| Status | RVAs |
|---|---:|
| `corpus body` | 59 (3 on misaligned rows; 3 with a Hex-Rays warning, 2 of them misaligned) |
| `[exe]` | 28 (18 code entries, 10 instruction anchors) |
| `GObjects` | 0 |
| vtable/data | 0 |
| `unverified` | 0 |
| **Total** | **87** |

Every cited address is in `.text`. No cited RVA is itself a GObjects
fact. The GObjects-backed values sit next to these RVAs: for example
`MVF_HealthSections.ComplexSurfaceMappings` (`0x90`) and
`PhysicsGroupMappings` (`0xE0`). The section registration `0x53214A0`
merges them into the component's `+0x180` (through `0x538ABD0`) and
`+0x1D0` (through `0x53167B0`) (r3 V-3, r5 T0-9). The doc cites
`0x53167B0` from `349104e` on.

## 3. Table

Sections are VehicleDamagePipeline sections; `L` numbers are its lines at
`349104e`.

| RVA | Role | Cited in | Verification status |
|---|---|---|---|
| `0x3EAF060` | Builds a hit result from location, normal, actor and component only (memset first, so `FaceIndex`, `MyItem` and `Item` are 0); used for the `0x6F06EB0` back-blast hit and the radial synthetic hits | §3.2 (L446) | `corpus body`; [exe] memset at `0x3EAF08E` (r5 T3-1, verifier-confirmed round 5) |
| `0x46E3930` | Data-registry source sort: pair pass and stable merge, descending priority, ties in insertion order | §2.2 (L150) | `corpus body` |
| `0x46EC5B0` | Data-registry source registration (`UMetaDataRegistrySource` slot 104): append, or update the priority | §2.2 (L150) | `corpus body` |
| `0x46ED100` | Row lookup (`UDataRegistry` slot 103): the first source that has the row | §2.2 (L151) | `corpus body`, misaligned and flagged: the body is filed under row `0x46ED0FF`; see notes |
| `0x46EDC20` | Source re-sort (`UMetaDataRegistrySource` slot 112) | §2.2 (L150) | `corpus body` |
| `0x50BF500` | Indexed slot name for instanced wheels (`CC_Wheel` → `CC_Wheel_2`); called from `0x50BF880` | §3.2 (L426) | `[exe]`: no functions row (r4 HB-4) |
| `0x50BF880` | Complex-surface resolve: hit to collision slot | §3.1 (L177), §3.2 (L397) | `[exe]`: no functions row; see notes |
| `0x50E7140` | Assembly: variant override layer, recurses into a base variant | §5.4 (L714, L719) | `[exe]`: no functions row (r3 V-1) |
| `0x50E7200` | Assembly: slot and fragment walk | §5.4 (L714) | `[exe]`: no functions row (r3 V-2, V-3) |
| `0x50EEE90` | Vehicle collision-profile selector: type 2 (`MVCT_QueryProxy`) returns `VehicleQueryProxy` and ignores the entry's profile name | §3.1 (L214) | `corpus body`; [exe] switch re-read (r5 T3-7, verifier-confirmed round 5) |
| `0x50F06E7` | Component registration check `cmp byte [rdi+0x3D2], r12b` (in `0x50F044C`) | §3.2 (L398) | `[exe]` (r4 HB-3) |
| `0x50F41D0` | Physics-group tag from the hit body | §3.1 (L199) | `[exe]`: no functions row (r4 HB-7) |
| `0x52311D0` | Attribute reduction helper; returns the change applied | §4.1 (L512), §5.4 (L732) | `[exe]`: no functions row (r2 HP-10, r3 V-6) |
| `0x5236990` | Registers a base-value hook (map at `+0x378`) | §5.4 (L730) | `[exe]`: no functions row (r3 V-6) |
| `0x5236C70` | Registers a current-value hook | §5.4 (L730) | `[exe]`: no functions row (r3 V-6) |
| `0x5304690` | `UMRotorStaticMeshComponent` constructor; sets its own default collision profile (`+0x670`), cited as not traced | §3.1 (L218) | `corpus body` (r5 O-7; not re-read by the verifier) |
| `0x5307ED0` | Broadcasts `MVehicleSectionDestroyedMessage` | §4.1 (L522) | `corpus body` |
| `0x53167B0` | Merges `PhysicsGroupMappings` (fragment `+0xE0`) into `+0x1D0`; called from the section registration | §3.1 (L194) | `corpus body`; [exe] call site `0x5321B05` (r5 T0-9, verifier-confirmed round 5) |
| `0x531FC20` | `ApplyCollisionDamage` (damage-model slot 160); reads `+0x1D0` | §3.1 (L197) | `corpus body` |
| `0x53202B0` | `ApplyDamageEvent` section pick | §4.1 (L494, L497), Change log (L830) | `[exe]`: no aligned row (`0x53202AB` is junk); damage evidence table, r3 V-22 |
| `0x5320394` | `mov r8, [rbx+0x40]`: radial pick takes `ComponentHits[0]` (in the section pick) | §4.1 (L500) | `[exe]` anchor (r5 T3-2, verifier-confirmed round 5) |
| `0x5320400` | Section-pick continuation, reached from `0x53202B0` and the thunk | §4.1 (L495–496) | `corpus body` |
| `0x53205D0` | `ApplyDamageToSection` | §4.2 (L534) | `corpus body` |
| `0x53214A0` | Section registration (damage-model slot 159): merges the surface maps, first registration wins, registers the health hooks | §3.1 (L191), §5.4 (L722, L729), Change log (L830) | `corpus body`, misaligned: the body is filed under row `0x532149E`; see notes |
| `0x53288B0` | Native body of the reflected `DestroyVehicle` (not the destroy routine used) | §4.1 (L520) | `corpus body` |
| `0x532D4C0` | Second `+0x1D0` reader, on the component-hit path | §3.1 (L197) | `corpus body` |
| `0x532F730` | Section-damaged handling, base (slot 162, `+0x510`) | §4.1 (L513) | `corpus body` |
| `0x53303F0` | Binds a wheel ISM to the movement component's wheel-state delegate (`+0x3C0`) with handler `0x5336DD0`; stores the intact flag at `+0xA38` | §3.2 (L477) | `corpus body`; [exe] `0x53303F0`–`0x533047C` (r5 T3-5, verifier-confirmed round 5) |
| `0x5336DD0` | Wheel-state handler: `SetWheelUseAlternativeCollision`, `SetWheelActive` and `SetWheelMaterialParams` per state | §3.2 (L477) | `[exe]`: no functions row; whole handler `0x5336DD0`–`0x5336EA3` (r5 T3-5, verifier-confirmed round 5) |
| `0x5338730` | Zone query | §3.1 (L171), §4.1 (L499), §7 (L802) | `corpus body` |
| `0x5339DD0` | `RerouteDamageInternal` | §4.2 (L534) | `corpus body` |
| `0x533A750` | Health hook: clamps the new value to `[0, MaxHealth]` | §5.4 (L731), Change log (L830) | `corpus body`, flagged: Hex-Rays warning; see notes |
| `0x533B6F0` | `SetWheelActive`: activates or deactivates one wheel instance and its remap entry | §3.2 (L478) | `[exe]`: no functions row; `0x533B715`–`0x533B744`, `0x533B87A` (r5 T3-5, T3-6, verifier-confirmed round 5) |
| `0x533BA20` | `SetWheelMaterialParams` | §3.2 (L479) | `corpus body` (r5 T3-5; call at `0x5336E8F`, verifier-confirmed round 5) |
| `0x533BAE0` | `SetWheelUseAlternativeCollision` | §3.2 (L478) | `corpus body` (r5 T3-5; call at `0x5336E1F`, verifier-confirmed round 5) |
| `0x5341430` | Reflected `ApplyDamageEvent` exec thunk | §4.1 (L495) | `corpus body` |
| `0x5345EA0` | Reflected `QueryDamageZoneForComplexHit` thunk | §3.1 (L173) | `[exe]`: row failed, the enclosing row is an empty nullsub; see notes |
| `0x5365660` | Enumerates the movement component's wheel setups: axles at `+0x6C0` (stride `0x70`), then each axle's wheel list | §3.2 (L467), §7 (L809) | `corpus body` (r5 T3-6, verifier-confirmed round 5) |
| `0x5370A40` | Wheel-state update: counts wheels axle by axle and broadcasts (wheel index, old, new) on a state change | §3.2 (L465, L476) | `corpus body` (r5 T3-5, T3-6, verifier-confirmed round 5) |
| `0x538ABD0` | Merges `ComplexSurfaceMappings` (fragment `+0x90`) into `+0x180`: per group, slot pairs added and the default overwritten; called from the section registration | §3.1 (L193) | `corpus body` |
| `0x53952A0` | Section lookup by (surface group, slot) in `+0x180`, with the default and parent-group fallbacks | §3.1 (L179), §3.2 (L397) | `corpus body`, misaligned and flagged: the body is filed under row `0x539529D`; see notes |
| `0x539ABB9` | `MVF_InstancedWheels` apply: assigns each wheel's `DataIndex` from the axle-major enumeration and binds both wheel ISMs | §3.2 (L467) | `corpus body` (row on a `.pdata` start; r5 T3-6, verifier-confirmed round 5) |
| `0x539B6E7` | `movzx r8d, byte [r13+0x344]` (`DeflatedMeshMode`): destroyed-mesh threshold 1 if `All`, else 2 (in `0x539ABB9`) | §3.2 (L482) | `[exe]` anchor (r5 T3-5, verifier-confirmed round 5) |
| `0x53A00C6` | Component registration check `cmp byte [rcx+0x28A], 0` (in `0x53A00C0`) | §3.2 (L398) | `[exe]` (r4 HB-3) |
| `0x53B6190` | Variant config replacement (`MVFCustomData_VehicleConfig`) | §5.4 (L724) | `corpus body` |
| `0x53D8E20` | `BHBaseVehiclePawn` destroy routine (unnamed) | §4.1 (L518) | `corpus body` |
| `0x6B18E70` | Damage-entity tag setter | §1 (L58) | `[exe]`: no functions row; see notes |
| `0x6B725B0` | Projectile-impact path | §1 (L40), §7 (L804) | `corpus body` |
| `0x6B733AC` | Call to the hit-tag fetch `0x6B80230` (in `0x6B725B0`) | §1 (L40) | `[exe]`: `call 0x6b80230`; also in `calls` |
| `0x6B7FE50` | `ApplyWDDamage` | §1 (L46) | `corpus body` |
| `0x6B80230` | Vehicle hit-tag fetch: first `Meta.Damage.HitLocation.*` tag of the hit section | §1 (L43), §3 (L164), §3.1 (L172) | `corpus body` |
| `0x6B802D0` | Section-damaged handling, WD override (slot 162) | §4.1 (L514) | `corpus body` |
| `0x6B8E100` | Projectile instance constructor; stores the empty ammo tag at `+0xF0` (`0x6B8E21F`) | §7 (L804) | `corpus body`; [exe] `0x6B8E218`–`0x6B8E21F` (r5 T3-8, verifier-confirmed round 5) |
| `0x6B8E2F4` | Trace parameters set by the projectile instance constructor: `mov r9b, 1` (complex trace) before `call 0x3C95C30` (in `0x6B8E100`) | §3.2 (L416) | `[exe]` (r4 HB-2) |
| `0x6B92900` | Back-blast source: one if/else calls `0x6F042A0` or `0x6F06EB0` | §3.2 (L450), §7 (L807) | `corpus body` (r5 T0, verifier-confirmed round 5) |
| `0x6BB6160` | `UWDGlobalDamageSystem` constructor; sets `RootDamageTag` | §1 (L66), §7 (L800) | `corpus body` |
| `0x6BB6A60` | Collector and parent walk (global slot 87) | §7 (L800) | `corpus body` |
| `0x6BB6FB0` | Global evaluator (slot 86) | §1 (L39) | `corpus body` |
| `0x6C2A5F0` | `IWDDamageable` dispatch | §1 (L44) | `corpus body` |
| `0x6C2A790` | Vehicle `IWDDamageable` slot 8: keeps one radial hit per component | §4.1 (L501) | `corpus body`; [exe] vtable slot 8 in all six vehicle sub-vtables, `0x6C2A8D3` (r5 T3-2, verifier-confirmed round 5) |
| `0x6C98290` | `IWDWeaponOwner` `+0x90` (ranged-weapon slot 192): builds `Meta.Damage.AmmoModifier.<type>` from the loaded round's item tag | §7 (L804) | `corpus body`; [exe] interface table `0xB389AB8+0x90` (r5 T3-8, verifier-confirmed round 5) |
| `0x6CA8730` | Explosive-actor path: point event from the impact hit (V-7) | §3.2 (L452), §7 (L806) | `corpus body` (r5 O-4; whether the hit carries `MyItem` is unverified) |
| `0x6EF8DE0` | Event to `FWDModifyDamageData` conversion (V-2) | §7 (L801) | `[exe]`: no functions row; damage evidence table, r3 EV-5 |
| `0x6EFFDC0` | Radial gather: complex Visibility line traces with face indices, per overlapped component | §3.2 (L438) | `corpus body` (r5 T3-1, verifier-confirmed round 5) |
| `0x6F0005A` | `mov word [rbp+0x252], 0x101`: face index and physical material on (in `0x6EFFDC0`) | §3.2 (L440) | `[exe]` anchor (r5 T3-1, verifier-confirmed round 5) |
| `0x6F01820` | Finds the actor's `UWDDamageEntityComponent` and copies its `DamageEntityData` | §7 (L801) | `[exe]`: no functions row (r4 TT-1) |
| `0x6F01BB0` | V-2 path: fills an empty hit-location tag from `ClassToHitLocations` by bone name | §7 (L801) | `corpus body`; see notes (at `479c6c1` the doc said it did not decompile) |
| `0x6F02EC0` | `UWDDamageSubsystem::ModifyDamage` | §1 (L39) | `corpus body` |
| `0x6F03720` | Radial hit filter and adder: keeps a hit only on the traced component (and instance) | §3.2 (L442) | `[exe]`: no aligned row (body filed under `0x6F0371F`, a lone `ret`); `0x6F0376E`–`0x6F03785`, `0x6F03A27`–`0x6F03A75` (r5 T3-1, verifier-confirmed round 5) |
| `0x6F042A0` | Back-blast path through the radial gather (one branch of `0x6B92900`) | §1 (L41), §3.2 (L438), §7 (L807), Change log (L832) | `[exe]`: row status `failed` (call analysis failed); damage evidence table |
| `0x6F06540` | Radial caller | §1 (L41), §4.1 (L504) | `corpus body` |
| `0x6F06EB0` | Back-blast path without traces: synthetic hit on the actor's first primitive component | §3.2 (L446), §4.1 (L505), §7 (L807), Change log (L832) | `corpus body` (L259–311; r5 T3-1, verifier-confirmed round 5) |
| `0x6F2C450` | Predicted projectile simulation: ammo tag from `FWDProjectileSimulationSetup.AmmoModifierTag` | §7 (L804) | `corpus body` (r5 O-8; the verifier accepted the text) |
| `0x6F30E50` | Projectile spawn: copies the ammo tag from the spawn parameters (`+0x40`) to instance `+0xF0` | §7 (L804) | `corpus body` (L22; r5 T3-8, verifier-confirmed round 5) |
| `0x6F30F70` | Projectile trace parameters: `mov word [rdi+0x152], 0x101` (face index and physical material on; in `0x6F30E50`) | §3.2 (L416) | `[exe]` (r4 HB-2) |
| `0x76736C0` | Collision path, between `0x767E640` and `0x76740F0` | §7 (L803) | `corpus body` |
| `0x76740F0` | Collision path: point event from the `OnComponentHit` hit | §1 (L42), §3.2 (L451), §7 (L803, L806) | `corpus body` |
| `0x7674428` | `cmove` of `Meta.Damage.Landscape` (`0xD36A610`) when the source tag is empty (in `0x76740F0`) | §7 (L803) | `[exe]` (r4 TT-5) |
| `0x7674435` | Loads `Meta.Damage.DamageType.Impact` (`0xD36A818`) for the source context (in `0x76740F0`) | §7 (L803) | `[exe]` (r4 TT-5) |
| `0x767BC40` | `UWDVehicleGameplaySystemsComponent` slot 161: sets the target tag | §1 (L57) | `corpus body` |
| `0x767E640` | Component-hit (collision) path; called from `0x768A280` | §3.1 (L198), §7 (L803) | `corpus body` |
| `0x768A280` | Reflected `OnMeshHitEvent` (`WDVehicleGameplaySystemsComponent`) | §7 (L803) | `corpus body` |
| `0x768ED20` | `UWDVehicleOperatorComponent` slot 161 | §1 (L49) | `corpus body` |
| `0x7692B60` | `UWDVehicleOperatorComponent` slot 160 | §1 (L49) | `corpus body` |
| `0x76AB5F0` | `GetWheelAxleSideFromIndex`: axle = index ≥ 2, side = index & 1 | §3.2 (L470) | `[exe]`: no functions row; leaf `cmp ecx, 2; setge al; and cl, 1` (r5 O-6), disassembled again for this page |
| `0x76B5560` | Vehicle pawn constructor; default tag `Meta.Damage.Vehicle` | §1 (L55) | `corpus body` |
| `0x76B7E80` | `AWDRotaryVehicle` slot 370 (`IWDDamageable`) | §1 (L45) | `corpus body` |

## 4. Notes on particular rows

- **`0x53214A0` (misaligned).** The row at `0x53214A0` failed with
  "Candidate entry lies inside another function at RVA `0x532149E`". The
  row `0x532149E` holds the body; its first instruction decodes as
  `and al, 0x40`, and the real prologue `mov [rsp+0x18], rbx` starts at
  `0x53214A0`. The doc cites the true entry: it is
  `UBHVehicleDamageModelComponent` slot 159, and its only direct
  reference is the WD override's tail jump at `0x6B7FE45`. The body
  carries no Hex-Rays warning, and r3 V-3 matched its offsets against the
  instructions.
- **`0x533A750` (warning).** The pseudocode starts with "local variable
  allocation has failed, the output may be wrong!". The clamp the doc
  relies on (`minss` with `MaxHealth`, `maxss` with 0) was reproduced from
  the instructions in r3 V-6, so the claim does not rest on the
  pseudocode alone.
- **`0x5345EA0`.** The exact row failed ("inside another function at RVA
  `0x5345E9F`"). The enclosing row is `nullsub_1776`, whose pseudocode is
  empty: `0x5345E9F` is a lone `ret` before the thunk. The thunk is the
  registered `QueryDamageZoneForComplexHit`. Its instructions take the
  owner's interface at `+0xC8` → `+0x338` (`0x5345F7D`–`0x5345F8B`), call
  `0x50BF880` (`0x5345FAB`), look the slot up in component `+0x180`
  through `0x53952A0` (`0x5345FDE`), and otherwise return a default tag
  (`0x5345FED`).
- **`0x50BF880`.** No functions row. It starts with a normal prologue,
  tests the hit result's first field (`cmp dword [r9], 0; jl`) and reads
  `r9 + 0xD8` before the owner check (`+0xC8`). Its direct callers are
  the zone query (`0x5338777`), the thunk (`0x5345FAB`), `0x50C259A` and
  `0x50C27C4`. Round 4 traced which hit fields select the slot (r4 HB-1);
  the rule is in the doc's §3.2.
- **`0x53952A0` (misaligned, warning).** No row at `0x53952A0`. The
  enclosing row `0x539529D` holds the body, but decoding from there gives
  `shr byte [rbx], cl; ror dword [rax-0x77], 1; pop rsp`, and Hex-Rays
  warns "positive sp value has been detected". The real prologue
  `mov [rsp+8], rbx` starts at `0x53952A0`, and both direct calls in the
  corpus target it. r4 HB-5 read the lookup (key, default and
  parent-group walk) from the instructions at its call sites and from
  the body, so the claim does not rest on the pseudocode alone.
- **`0x46ED100` (misaligned, warning).** The row at `0x46ED100` failed
  ("inside another function at RVA `0x46ED0FF`"). The row `0x46ED0FF`
  holds the body, starts with the junk instruction `dec dword [rax-0x77]`
  and carries the same "positive sp value" warning. The real prologue
  `mov [rsp+0x18], rbx` starts at `0x46ED100`, which is `UDataRegistry`
  slot 103. r4 TT-4 reproduced the first-source-wins lookup from the
  instructions.
- **`0x6B18E70`.** No functions row. The whole function is
  `mov rax, [rdx]; test rax, rax; je; mov [rcx+0xE0], rax; ret`: it stores
  the tag at `+0xE0` only when the tag is not empty. Its direct callers
  include both functions the doc names, `0x767BC40` (site `0x767CB8B`)
  and `0x76B5560` (site `0x76B58C7`).
- **`0x6F01BB0`.** At `479c6c1`, the doc's V-2 row (L670) said "`0x6EF8DE0` /
  `0x6F01BB0`, which did not decompile". Only `0x6EF8DE0` lacks a row;
  `0x6F01BB0` has a decompiled body (668 bytes, no warning, 7 direct
  calls). The verifier's replacement for that cell is "`0x6EF8DE0` (no
  corpus row; disassembly) and `0x6F01BB0` (corpus body)" (EV-22).
  Corrected in the doc: round 4 closed V-2 (TT-1) and rewrote the row,
  citing `0x6F01BB0` as a body.
- **Ledger-backed `[exe]` rows.** `0x50E7140`, `0x50E7200`, `0x52311D0`,
  `0x5236990`, `0x5236C70`, `0x53202B0`, `0x6EF8DE0` and `0x6F042A0` were
  reproduced from the instructions in round 2 or 3 (or on the damage
  evidence page). The entries `0x50BF500`, `0x50F41D0` and `0x6F01820`
  and the anchors `0x50F06E7`, `0x53A00C6`, `0x6B8E2F4`, `0x6F30F70`,
  `0x7674428` and `0x7674435` were reproduced in round 4 (r4 HB-2 to HB-4,
  HB-7, TT-1, TT-5). This page only confirmed that the entries still have
  no row and start on a `.pdata` entry with a normal prologue, and that
  each anchor decodes to the instruction in the table.
- **Round-5 `[exe]` rows.** The entries `0x5336DD0` and `0x533B6F0` and
  the anchors `0x5320394`, `0x539B6E7` and `0x6F0005A` were reproduced
  by the round-5 verifier (r5 T3-1, T3-2, T3-5). For this page, each
  entry was checked for a `.pdata` start and each anchor decoded to the
  instruction in the table. `0x6F03720` has no `.pdata` entry of its own;
  the byte before it (`0x6F0371F`, the enclosing row) is a lone `ret`,
  and it starts with `mov rax, rsp` and has five direct calls.
  `0x76AB5F0` is a leaf with no `.pdata` entry; its whole body
  (`cmp ecx, 2; setge al; and cl, 1; mov [rdx], al; mov [r8], cl; ret`)
  was decoded for this page. The verifier accepted its reading from the
  teammate (O-6) without re-running it.
- **`0x539ABB9`.** The row sits on an odd address, but that address is a
  `.pdata` start, so it is a real entry. Its second instruction already
  stores through `r11` (`mov [r11-0x20], rax`). The verifier read the
  body at lines 177–286 (r5 T3-6).
- **`0x395F4D0`.** The parent-tag step was cited at `479c6c1` (§2.2) and
  is no longer cited. Its status (`[exe]`, no functions row) is kept on
  the [damage evidence page](damage.md#table).

## 5. Open items

- V-3 and V-6 to V-10 stay open in
  [VehicleDamagePipeline §7](../../Wardogs_VehicleDamagePipeline_v1.md#7-open-questions).
  A status table settles where the code is, not what it does.
