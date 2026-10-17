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
   at `main` `479c6c1` was extracted. Values below `0x100000` are struct
   offsets, sizes or enum values and were dropped. That left **42 RVAs**.
2. Each RVA was tagged with the numbered section that cites it and the
   doc's line numbers at `479c6c1`.
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
5. RVAs without a usable body were checked against the round-2 and
   round-3 verifier ledgers (cited as r2/r3 row IDs; the ledgers are local
   working files) and against the
   [damage evidence table](damage.md#table). Where neither covered one,
   it was disassembled for this page.
6. Every status that is not a plain corpus body was sent to an
   independent verifier as claims EV-1 to EV-22, shared with
   [the effects page](effects.md). The verifier re-ran the queries and
   the disassembly and confirmed all 22 claims and both pages' counts.
   It recorded EV-21 and EV-22 as citation errors in the pipeline docs
   (notes below and on the effects page).

The corpus part is
[`_tools/rva_status.py`](../../_tools/rva_status.py).
Run it with `python -I` from the repository root:

```text
python -I _tools/rva_status.py Wardogs_VehicleDamagePipeline_v1.md --rev 479c6c1 --exe
```

It prints one tab-separated line per RVA: citing sections and lines, PE
section, `body` or `-`, row status and reason, call count, enclosing row,
aliases and flags. It opens the corpus with `?mode=ro` and writes nothing.
`--exe` only reads section headers from the executable.

### Status key

- **`corpus body`**: a decompiled `functions` row with no `JUMPOUT` or
  inline assembly. Misaligned rows and rows with Hex-Rays warnings are
  flagged in the table.
- **`[exe]`**: instructions in the restored executable only. This covers
  functions with no row, failed or empty rows, and instruction anchors
  inside a body.
- **`GObjects`**: an offset or value backed by the runtime property dump.
- **vtable/data**: bytes at a data address.
- **`unverified`**: none of the above has been reproduced.

## 2. Status counts

| Status | RVAs |
|---|---:|
| `corpus body` | 29 (1 on a misaligned row, 1 with a Hex-Rays warning) |
| `[exe]` | 13 (12 code entries, 1 instruction anchor) |
| `GObjects` | 0 |
| vtable/data | 0 |
| `unverified` | 0 |
| **Total** | **42** |

Every cited address is in `.text`. No cited RVA is itself a GObjects
fact. The GObjects-backed values sit next to these RVAs: for example
`MVF_HealthSections.ComplexSurfaceMappings` (`0x90`) and
`PhysicsGroupMappings` (`0xE0`), which `0x53214A0` merges into the
component's `+0x180` and `+0x1D0` (r3 V-3).

## 3. Table

Sections are VehicleDamagePipeline sections; `L` numbers are its lines at
`479c6c1`.

| RVA | Role | Cited in | Verification status |
|---|---|---|---|
| `0x395F4D0` | Parent-tag step (`FGameplayTag::RequestDirectParent`); an unknown tag gives an empty parent | §2.2 (L143) | `[exe]`: no functions row; stores an empty tag at `0x395F592` (damage evidence table; r3 V-16, QC-4b) |
| `0x50BF880` | Complex-surface resolve: hit to collision slot | §3.1 (L168) | `[exe]`: no functions row; see notes |
| `0x50E7140` | Assembly: variant override layer, recurses into a base variant | §5.4 (L584, L589) | `[exe]`: no functions row (r3 V-1) |
| `0x50E7200` | Assembly: slot and fragment walk | §5.4 (L584) | `[exe]`: no functions row (r3 V-2, V-3) |
| `0x52311D0` | Attribute reduction helper; returns the change applied | §4.1 (L383), §5.4 (L602) | `[exe]`: no functions row (r2 HP-10, r3 V-6) |
| `0x5236990` | Registers a base-value hook (map at `+0x378`) | §5.4 (L600) | `[exe]`: no functions row (r3 V-6) |
| `0x5236C70` | Registers a current-value hook | §5.4 (L600) | `[exe]`: no functions row (r3 V-6) |
| `0x5307ED0` | Broadcasts `MVehicleSectionDestroyedMessage` | §4.1 (L393) | `corpus body` |
| `0x53202B0` | `ApplyDamageEvent` section pick | §4.1 (L371, L374), Change log (L694) | `[exe]`: no aligned row (`0x53202AB` is junk); damage evidence table, r3 V-22 |
| `0x5320400` | Section-pick continuation, reached from `0x53202B0` and the thunk | §4.1 (L372–373) | `corpus body` |
| `0x53205D0` | `ApplyDamageToSection` | §4.2 (L405) | `corpus body` |
| `0x53214A0` | Section registration (damage-model slot 159): merges the surface maps, first registration wins, registers the health hooks | §3.1 (L178), §5.4 (L592, L599), Change log (L694) | `corpus body`, misaligned: the body is filed under row `0x532149E`; see notes |
| `0x53288B0` | Native body of the reflected `DestroyVehicle` (not the destroy routine used) | §4.1 (L391) | `corpus body` |
| `0x532F730` | Section-damaged handling, base (slot 162, `+0x510`) | §4.1 (L384) | `corpus body` |
| `0x5338730` | Zone query | §3.1 (L162), §4.1 (L376), §7 (L671) | `corpus body` |
| `0x5339DD0` | `RerouteDamageInternal` | §4.2 (L405) | `corpus body` |
| `0x533A750` | Health hook: clamps the new value to `[0, MaxHealth]` | §5.4 (L601), Change log (L694) | `corpus body`, flagged: Hex-Rays warning; see notes |
| `0x5341430` | Reflected `ApplyDamageEvent` exec thunk | §4.1 (L372) | `corpus body` |
| `0x5345EA0` | Reflected `QueryDamageZoneForComplexHit` thunk | §3.1 (L164) | `[exe]`: row failed, the enclosing row is an empty nullsub; see notes |
| `0x53B6190` | Variant config replacement (`MVFCustomData_VehicleConfig`) | §5.4 (L594) | `corpus body` |
| `0x53D8E20` | `BHBaseVehiclePawn` destroy routine (unnamed) | §4.1 (L389) | `corpus body` |
| `0x6B18E70` | Damage-entity tag setter | §1 (L57) | `[exe]`: no functions row; see notes |
| `0x6B725B0` | Projectile-impact path | §1 (L40) | `corpus body` |
| `0x6B733AC` | Call to the hit-tag fetch `0x6B80230` (in `0x6B725B0`) | §1 (L40) | `[exe]`: `call 0x6b80230`; also in `calls` |
| `0x6B7FE50` | `ApplyWDDamage` | §1 (L45) | `corpus body` |
| `0x6B80230` | Vehicle hit-tag fetch: first `Meta.Damage.HitLocation.*` tag of the hit section | §1 (L42), §3 (L155), §3.1 (L163) | `corpus body` |
| `0x6B802D0` | Section-damaged handling, WD override (slot 162) | §4.1 (L385) | `corpus body` |
| `0x6BB6160` | `UWDGlobalDamageSystem` constructor; sets `RootDamageTag` | §1 (L64), §7 (L669) | `corpus body` |
| `0x6BB6A60` | Collector and parent walk (global slot 87) | §7 (L669) | `corpus body` |
| `0x6BB6FB0` | Global evaluator (slot 86) | §1 (L39) | `corpus body` |
| `0x6C2A5F0` | `IWDDamageable` dispatch | §1 (L43) | `corpus body` |
| `0x6EF8DE0` | Event to `FWDModifyDamageData` conversion (V-2) | §7 (L670) | `[exe]`: no functions row; damage evidence table, r3 EV-5 |
| `0x6F01BB0` | Second V-2 function | §7 (L670) | `corpus body`; see notes (the doc says it did not decompile) |
| `0x6F02EC0` | `UWDDamageSubsystem::ModifyDamage` | §1 (L39) | `corpus body` |
| `0x6F042A0` | Radial caller | §1 (L41) | `[exe]`: row status `failed` (call analysis failed); damage evidence table |
| `0x6F06540` | Radial caller | §1 (L41) | `corpus body` |
| `0x76740F0` | Radial caller | §1 (L41) | `corpus body` |
| `0x767BC40` | `UWDVehicleGameplaySystemsComponent` slot 161: sets the target tag | §1 (L56) | `corpus body` |
| `0x768ED20` | `UWDVehicleOperatorComponent` slot 161 | §1 (L48) | `corpus body` |
| `0x7692B60` | `UWDVehicleOperatorComponent` slot 160 | §1 (L48) | `corpus body` |
| `0x76B5560` | Vehicle pawn constructor; default tag `Meta.Damage.Vehicle` | §1 (L54) | `corpus body` |
| `0x76B7E80` | `AWDRotaryVehicle` slot 370 (`IWDDamageable`) | §1 (L44) | `corpus body` |

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
  `0x50C27C4`. Which hit field selects the slot is round-4 Track 1's
  question, not this page's.
- **`0x6B18E70`.** No functions row. The whole function is
  `mov rax, [rdx]; test rax, rax; je; mov [rcx+0xE0], rax; ret`: it stores
  the tag at `+0xE0` only when the tag is not empty. Its direct callers
  include both functions the doc names, `0x767BC40` (site `0x767CB8B`)
  and `0x76B5560` (site `0x76B58C7`).
- **`0x6F01BB0`.** The doc's V-2 row (L670) says "`0x6EF8DE0` /
  `0x6F01BB0`, which did not decompile". Only `0x6EF8DE0` lacks a row;
  `0x6F01BB0` has a decompiled body (668 bytes, no warning, 7 direct
  calls). The verifier's replacement for that cell is "`0x6EF8DE0` (no
  corpus row; disassembly) and `0x6F01BB0` (corpus body)" (EV-22). This
  page does not change the doc; V-2 is round-4 Track 3's question and may
  be rewritten there.
- **Ledger-backed `[exe]` rows.** `0x395F4D0`, `0x50E7140`, `0x50E7200`,
  `0x52311D0`, `0x5236990`, `0x5236C70`, `0x53202B0`, `0x6EF8DE0` and
  `0x6F042A0` were reproduced from the instructions in round 2 or 3 (or
  on the damage evidence page). This page only confirmed that they still
  have no usable row.

## 5. Open items

- The meaning of the hit-result field that `0x50BF880` reads, and the
  key of the `+0x180` lookup, are open in the doc's §3.1 and are not
  settled by a status table.
- V-2 to V-6 stay open in
  [VehicleDamagePipeline §7](../../Wardogs_VehicleDamagePipeline_v1.md#7-open-questions).
