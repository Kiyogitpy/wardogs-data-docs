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
   at `main` `e057d26` was extracted. Values below `0x100000` are struct
   offsets, sizes or enum values and were dropped. That left **61 RVAs**.
   The page was first built at `479c6c1` (42 RVAs). Round 4's corrections
   added 20 RVAs, and `0x395F4D0` is no longer cited.
2. Each RVA was tagged with the numbered section that cites it and the
   doc's line numbers at `e057d26`.
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

The corpus part is
[`_tools/rva_status.py`](../../_tools/rva_status.py).
Run it with `python -I` from the repository root:

```text
python -I _tools/rva_status.py Wardogs_VehicleDamagePipeline_v1.md --rev e057d26 --exe
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
| `corpus body` | 40 (3 on misaligned rows; 3 with a Hex-Rays warning, 2 of them misaligned) |
| `[exe]` | 21 (14 code entries, 7 instruction anchors) |
| `GObjects` | 0 |
| vtable/data | 0 |
| `unverified` | 0 |
| **Total** | **61** |

Every cited address is in `.text`. No cited RVA is itself a GObjects
fact. The GObjects-backed values sit next to these RVAs: for example
`MVF_HealthSections.ComplexSurfaceMappings` (`0x90`) and
`PhysicsGroupMappings` (`0xE0`). The section registration `0x53214A0`
merges them into the component's `+0x180` (through `0x538ABD0`) and
`+0x1D0` (through `0x53167B0`) (r3 V-3, r5 T0-9). `0x53167B0` is not
cited by the doc at `e057d26`.

## 3. Table

Sections are VehicleDamagePipeline sections; `L` numbers are its lines at
`e057d26`.

| RVA | Role | Cited in | Verification status |
|---|---|---|---|
| `0x46E3930` | Data-registry source sort: pair pass and stable merge, descending priority, ties in insertion order | §2.2 (L150) | `corpus body` |
| `0x46EC5B0` | Data-registry source registration (`UMetaDataRegistrySource` slot 104): append, or update the priority | §2.2 (L150) | `corpus body` |
| `0x46ED100` | Row lookup (`UDataRegistry` slot 103): the first source that has the row | §2.2 (L151) | `corpus body`, misaligned and flagged: the body is filed under row `0x46ED0FF`; see notes |
| `0x46EDC20` | Source re-sort (`UMetaDataRegistrySource` slot 112) | §2.2 (L150) | `corpus body` |
| `0x50BF500` | Indexed slot name for instanced wheels (`CC_Wheel` → `CC_Wheel_2`); called from `0x50BF880` | §3.2 (L417) | `[exe]`: no functions row (r4 HB-4) |
| `0x50BF880` | Complex-surface resolve: hit to collision slot | §3.1 (L177), §3.2 (L391) | `[exe]`: no functions row; see notes |
| `0x50E7140` | Assembly: variant override layer, recurses into a base variant | §5.4 (L659, L664) | `[exe]`: no functions row (r3 V-1) |
| `0x50E7200` | Assembly: slot and fragment walk | §5.4 (L659) | `[exe]`: no functions row (r3 V-2, V-3) |
| `0x50F06E7` | Component registration check `cmp byte [rdi+0x3D2], r12b` (in `0x50F044C`) | §3.2 (L392) | `[exe]` (r4 HB-3) |
| `0x50F41D0` | Physics-group tag from the hit body | §3.1 (L199) | `[exe]`: no functions row (r4 HB-7) |
| `0x52311D0` | Attribute reduction helper; returns the change applied | §4.1 (L457), §5.4 (L677) | `[exe]`: no functions row (r2 HP-10, r3 V-6) |
| `0x5236990` | Registers a base-value hook (map at `+0x378`) | §5.4 (L675) | `[exe]`: no functions row (r3 V-6) |
| `0x5236C70` | Registers a current-value hook | §5.4 (L675) | `[exe]`: no functions row (r3 V-6) |
| `0x5307ED0` | Broadcasts `MVehicleSectionDestroyedMessage` | §4.1 (L467) | `corpus body` |
| `0x531FC20` | `ApplyCollisionDamage` (damage-model slot 160); reads `+0x1D0` | §3.1 (L197) | `corpus body` |
| `0x53202B0` | `ApplyDamageEvent` section pick | §4.1 (L445, L448), Change log (L771) | `[exe]`: no aligned row (`0x53202AB` is junk); damage evidence table, r3 V-22 |
| `0x5320400` | Section-pick continuation, reached from `0x53202B0` and the thunk | §4.1 (L446–447) | `corpus body` |
| `0x53205D0` | `ApplyDamageToSection` | §4.2 (L479) | `corpus body` |
| `0x53214A0` | Section registration (damage-model slot 159): merges the surface maps, first registration wins, registers the health hooks | §3.1 (L191), §5.4 (L667, L674), Change log (L771) | `corpus body`, misaligned: the body is filed under row `0x532149E`; see notes |
| `0x53288B0` | Native body of the reflected `DestroyVehicle` (not the destroy routine used) | §4.1 (L465) | `corpus body` |
| `0x532D4C0` | Second `+0x1D0` reader, on the component-hit path | §3.1 (L197) | `corpus body` |
| `0x532F730` | Section-damaged handling, base (slot 162, `+0x510`) | §4.1 (L458) | `corpus body` |
| `0x5338730` | Zone query | §3.1 (L171), §4.1 (L450), §7 (L747) | `corpus body` |
| `0x5339DD0` | `RerouteDamageInternal` | §4.2 (L479) | `corpus body` |
| `0x533A750` | Health hook: clamps the new value to `[0, MaxHealth]` | §5.4 (L676), Change log (L771) | `corpus body`, flagged: Hex-Rays warning; see notes |
| `0x5341430` | Reflected `ApplyDamageEvent` exec thunk | §4.1 (L446) | `corpus body` |
| `0x5345EA0` | Reflected `QueryDamageZoneForComplexHit` thunk | §3.1 (L173) | `[exe]`: row failed, the enclosing row is an empty nullsub; see notes |
| `0x538ABD0` | Merges `ComplexSurfaceMappings` (fragment `+0x90`) into `+0x180`: per group, slot pairs added and the default overwritten; called from the section registration | §3.1 (L194) | `corpus body` |
| `0x53952A0` | Section lookup by (surface group, slot) in `+0x180`, with the default and parent-group fallbacks | §3.1 (L179), §3.2 (L391) | `corpus body`, misaligned and flagged: the body is filed under row `0x539529D`; see notes |
| `0x53A00C6` | Component registration check `cmp byte [rcx+0x28A], 0` (in `0x53A00C0`) | §3.2 (L392) | `[exe]` (r4 HB-3) |
| `0x53B6190` | Variant config replacement (`MVFCustomData_VehicleConfig`) | §5.4 (L669) | `corpus body` |
| `0x53D8E20` | `BHBaseVehiclePawn` destroy routine (unnamed) | §4.1 (L463) | `corpus body` |
| `0x6B18E70` | Damage-entity tag setter | §1 (L58) | `[exe]`: no functions row; see notes |
| `0x6B725B0` | Projectile-impact path | §1 (L40), §7 (L749) | `corpus body` |
| `0x6B733AC` | Call to the hit-tag fetch `0x6B80230` (in `0x6B725B0`) | §1 (L40) | `[exe]`: `call 0x6b80230`; also in `calls` |
| `0x6B7FE50` | `ApplyWDDamage` | §1 (L46) | `corpus body` |
| `0x6B80230` | Vehicle hit-tag fetch: first `Meta.Damage.HitLocation.*` tag of the hit section | §1 (L43), §3 (L164), §3.1 (L172) | `corpus body` |
| `0x6B802D0` | Section-damaged handling, WD override (slot 162) | §4.1 (L459) | `corpus body` |
| `0x6B8E2F4` | Trace parameters set by the projectile instance constructor: `mov r9b, 1` (complex trace) before `call 0x3C95C30` (in `0x6B8E100`) | §3.2 (L409) | `[exe]` (r4 HB-2) |
| `0x6BB6160` | `UWDGlobalDamageSystem` constructor; sets `RootDamageTag` | §1 (L66), §7 (L745) | `corpus body` |
| `0x6BB6A60` | Collector and parent walk (global slot 87) | §7 (L745) | `corpus body` |
| `0x6BB6FB0` | Global evaluator (slot 86) | §1 (L39) | `corpus body` |
| `0x6C2A5F0` | `IWDDamageable` dispatch | §1 (L44) | `corpus body` |
| `0x6EF8DE0` | Event to `FWDModifyDamageData` conversion (V-2) | §7 (L746) | `[exe]`: no functions row; damage evidence table, r3 EV-5 |
| `0x6F01820` | Finds the actor's `UWDDamageEntityComponent` and copies its `DamageEntityData` | §7 (L746) | `[exe]`: no functions row (r4 TT-1) |
| `0x6F01BB0` | V-2 path: fills an empty hit-location tag from `ClassToHitLocations` by bone name | §7 (L746) | `corpus body`; see notes (at `479c6c1` the doc said it did not decompile) |
| `0x6F02EC0` | `UWDDamageSubsystem::ModifyDamage` | §1 (L39) | `corpus body` |
| `0x6F042A0` | Radial caller | §1 (L41) | `[exe]`: row status `failed` (call analysis failed); damage evidence table |
| `0x6F06540` | Radial caller | §1 (L41) | `corpus body` |
| `0x6F30F70` | Projectile trace parameters: `mov word [rdi+0x152], 0x101` (face index and physical material on; in `0x6F30E50`) | §3.2 (L409) | `[exe]` (r4 HB-2) |
| `0x76736C0` | Collision path, between `0x767E640` and `0x76740F0` | §7 (L748) | `corpus body` |
| `0x76740F0` | Radial caller | §1 (L42), §7 (L748) | `corpus body` |
| `0x7674428` | `cmove` of `Meta.Damage.Landscape` (`0xD36A610`) when the source tag is empty (in `0x76740F0`) | §7 (L748) | `[exe]` (r4 TT-5) |
| `0x7674435` | Loads `Meta.Damage.DamageType.Impact` (`0xD36A818`) for the source context (in `0x76740F0`) | §7 (L748) | `[exe]` (r4 TT-5) |
| `0x767BC40` | `UWDVehicleGameplaySystemsComponent` slot 161: sets the target tag | §1 (L57) | `corpus body` |
| `0x767E640` | Component-hit (collision) path; called from `0x768A280` | §3.1 (L198), §7 (L748) | `corpus body` |
| `0x768A280` | Reflected `OnMeshHitEvent` (`WDVehicleGameplaySystemsComponent`) | §7 (L748) | `corpus body` |
| `0x768ED20` | `UWDVehicleOperatorComponent` slot 161 | §1 (L49) | `corpus body` |
| `0x7692B60` | `UWDVehicleOperatorComponent` slot 160 | §1 (L49) | `corpus body` |
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
- **`0x395F4D0`.** The parent-tag step was cited at `479c6c1` (§2.2) and
  is no longer cited. Its status (`[exe]`, no functions row) is kept on
  the [damage evidence page](damage.md#table).

## 5. Open items

- V-3 and V-6 stay open in
  [VehicleDamagePipeline §7](../../Wardogs_VehicleDamagePipeline_v1.md#7-open-questions).
  A status table settles where the code is, not what it does.
