# Round 93: Drill Rig parameter choice and vehicle inactivity limits

Scope: offline review of the restored CL-516586 executable, its two native-analysis corpora, SDK layouts and cooked asset exports. No game process, instrumentation or live server was used. Addresses below are **RVAs**, image base `0x140000000`. Executable SHA-256: `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.

| Gap | Disposition | Result |
|---|---|---|
| G2: world versus Drill Rig speed/size | **Closed for the shipped native activation path and cooked default binding** | The buildable rig supplies its own data asset's speed and size directly to relocation. It does not need to copy them into the world component's default fields first. The inherited rig defaults are **5 m/s and (0.5, 0.5, 1)**, not the separate world defaults 3 m/s and approximately (0.6, 0.6, 1). |
| G3: `InactivityLifetimeOutSafeZone` reader, units and action | **Partial; consumer still open** | Native initialization to 300 and the data-to-component copy are confirmed. No typed downstream reader of this field was established. A different vehicle lifetime manager has real time/health behavior, but that does not establish this field's units or action. |

These are static implementation findings, not measured match behavior or a guarantee about a remote server's configuration.

## 1. G2 — the rig has a separate activation caller

### Initialization and cooked binding

The two defaults belong to different objects:

| Owner | Speed field | Size multiplier field | Native initializer |
|---|---|---|---|
| `UWDHotZoneMagnetGameStateComponent` | `+0xF0`: 3.0 | `+0xF8`: approximately (0.6, 0.6, 1) | `0x8566570`; speed write `0x8566608`, XY constant `0x85665E3` |
| `UWDBuildableHotZoneMagnetDataAsset` | `+0x39C`: 5.0 | `+0x3A0`: (0.5, 0.5, 1) | `0x85E05D0`; speed write `0x85E0666`, XY writes `0x85E060B` / `0x85E0612` |

The rig data export does **not** explicitly serialize either speed or multiplier; the values above are native defaults, not explicit JSON overrides. The world XY constant is a float-rounded 0.6 promoted to double, whereas the rig XY constant is exactly 0.5.

The cooked reference chain supplies the previously missing actor initialization link:

1. [`DA_Buildable_HotzoneMagnet`](../../data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/Hotzone_Magnet/DA_Buildable_HotzoneMagnet.json) names `B_Buildable_HotzoneMagnet_C` as its spawner's `BaseBuildableClass`.
2. That Blueprint's `WDBuildable_ActorSpawnLocation` component has `ActorToSpawn = B_HotzoneMagnet_functionality_C`.
3. `Default__B_HotzoneMagnet_functionality_C` explicitly sets `BuildableDataAsset` to [`DA_Buildable_HotzoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/Hotzone_Magnet/DA_Buildable_HotzoneMagnet.json). Its native parent is `WDBuildableHotZoneMagnetActor`.
4. The native actor constructor `0x85E6C90` initially clears `BuildableDataAsset` at `+0x2E8`; the cooked class default supplies the non-null reference. Native constructor state alone therefore was not the final initialized default.

The two Blueprint CDOs were freshly decoded from the on-disk cooked containers using the existing corrected mapping. The re-extracted data asset is semantically identical, across both exports, to the published JSON linked above. Private provenance records pin the mapping, extracted files and container metadata. No new Blueprint source is published here.

### Activation → explicit parameters → control-zone setters

`UWDBuildableHotZoneMagnetActivateInteractionContext` vtable slot 91 points to `0x8601700`. Its completion path checks the actor type and validity, then calls the rig-specific activation body `0x85EB820` at `0x860176E`.

That body requires actor authority (`role +0x170 == 3`), valid rig data and associated objects, and a non-negligible successful fuel withdrawal. Its relevant inputs are **the rig actor's `BuildableDataAsset`**, not the world component's default fields:

- `0x85EBA94` loads the rig data pointer from actor `+0x2E8`.
- `0x85EBAB1`, `0x85EBAC0`, `0x85EBAC8` multiply cached control-zone extents by the rig data's Z/Y/X multipliers at `+0x3B0/+0x3A8/+0x3A0`.
- `0x85EBAE2` loads the rig data's speed float at `+0x39C`.
- `0x85EBB80` passes that **float** as a stack argument; `0x85EBB99` calls the common activation function `0x856FE50` with the scaled extents and a true relocation/replace flag.

The common function is parameterized. It does not silently replace those arguments with its own `+0xF0/+0xF8` defaults. It forwards them through `0x85731A0` to `0x776DDD0` (call `0x85731FC`). The speed remains a float: its final argument load is at `0x85731EC`. This matters because an automatically inferred pseudocode prototype labels an intermediate argument as a byte; the machine instructions and SDK's reflected signature establish that it is a float.

The relocation setter `0x776DDD0`:

- accepts the rig's request when the control-zone objects are valid; the rig's true flag permits replacement of an existing relocation;
- sets the explicit-relocation flag at `+0x6A0`, stores the target centre, and writes the nonzero supplied extents to `+0x590`;
- stores the supplied speed at `+0x544`, clamped to at least 0.01 (`0x776DEEA` is the write); a zero speed argument retains the previous speed;
- takes the explicit-relocation branch past ordinary random/configured extent/speed selection (`0x776DF6F → 0x776E135`). Thus the later ordinary-config speed write is not evidence that the rig speed is overwritten on this path.

The inspected tower caller `0x85674A0` instead obtains its speed and size from the world component. This is a **caller/input distinction**, not a missing asset-to-world-default copy.

### Actual movement and duration consumers

`0x776D890` computes the relocation duration from Euclidean centre distance in centimetres, converts to metres and divides by the stored speed at `+0x544`. The square root, conversion, division and duration write are at `0x776DAEF`, `0x776DAF7`, `0x776DAFF` and `0x776DB07`. The conversion literal independently decodes to float 0.01. `0x85731A0` adds that returned travel time to the active duration (`0x8573201`).

`0x7770A80` is the authority-side transition consumer: it accumulates frame time at `+0x540`, reads transition state at `+0x538` and duration at `+0x53C`, interpolates extents and centre toward their targets, and submits movement through `0x3D78500`. It can remap the normalized transition progress through an optional configured curve (`0x3E07720`), so the speed parameter defines the travel-duration calculation, not a proof of constant instantaneous velocity. The state transition helper `0x776DB20` does not choose a new ordinary config while explicit relocation remains active; it follows that relocation's completion/delegate path instead.

**Correction to [round 46 B, section 3](round46-b.md#3-drill-rig-zone-movement-found-static-disassembly):** the missing link was the buildable rig's separate activation body, not a copy of rig fields into world defaults. The statement that the rig's 5.0 can apply only after such a copy is superseded.

### Publication wording supported by this evidence

For the Drill Rig page's movement/size paragraphs:

> The shipped rig activation path reads the rig's own data asset. With the inherited native defaults in the cooked rig, it uses 5 m/s to calculate travel duration and targets half the cached width and length, with unchanged height. Half width and half length give 25% of the planar area. Travel time is centre distance in metres divided by speed, and is added to the fuel-derived active duration; an optional curve can shape interpolation during that time. The separate world magnet defaults are 3 m/s and about 0.6 width/length; they are not the inputs chosen by this rig activation path. These are static defaults and code behavior, not a live-server measurement.

Do not describe the 5/0.5 pair as explicitly present in the data JSON, and do not claim that every runtime activation succeeds regardless of validity, fuel or authority gates. Remote server configuration, runtime mutation and observed match timing remain outside this finding's closure scope.

## 2. G3 — preserve the stored value, withdraw the unsupported timer claim

### Positive evidence

The component constructor `0x766B080` stores float 300.0 at `UWDVehicleGameplaySystemsComponent +0x75C`; the instruction is `0x766B3DF`.

During initialization `0x767BC40` copies the data asset's field at `+0x558` into the component. The actual native load/store pair is `0x767CD28` / `0x767CD30`. This establishes **storage provenance**, not units, elapsed-time accumulation, occupancy criteria, safe-zone criteria, expiry or removal.

### Why the lifetime manager is not proof of this field's consumer

The separate `UBHVehicleLifetimeManager` has an event registration path (`0x86D9320` → `0x86D9180`) and a tick path (`0x86D9680` → `0x86D9A60`). The actual PE instructions of the latter were reviewed even though neither exact `sub_` nor `loc_` name resolves to a DeepExtract row.

That routine has checks for occupancy/state/tags and proximity. The lifetime selection at `0x86D9E24`–`0x86D9E6D` reads the **global settings object's** integer `VehicleLifetime`, `DisabledVehicleLifetime` and `ParkedBadlyVehicleLifetime` fields (`+0x38/+0x3C/+0x40`), not gameplay component `+0x75C` or data asset `+0x558`. Its elapsed state is compared with that selected global lifetime; after expiry a separate setting scales a health/damage call (`0x86D9EB5`, `0x86D9F05`). This is a distinct native lifetime mechanism, not a demonstrated reader of `InactivityLifetimeOutSafeZone`.

### Negative-search limits and remaining dependencies

The retained vehicle-module scan covers unwind-described entries beginning in RVA `0x7600000`–`0x7700000`. It decodes 239,538 instructions from 6,596 entries, with **44 decode gaps**. Its only decoded exact `+0x75C` accesses are the constructor and copy stores above. That is a bounded result, not proof of client-wide absence.

A new whole-executable-section displacement candidate pass found 110 raw encodings, yielding 54 decoded exact-displacement accesses, with 7 candidates outside unwind coverage and 15 candidate-entry decode gaps. Many are clearly other storage (stack slots, container capacity, landscape dimensions, byte flags or unrelated numerical structures). They are **not** automatically readers of the vehicle field. Conversely, a displacement match does not identify a typed object. Candidate ownership review is incomplete, including the read sites at `0x5088F78` and `0x537C442`; rebased pointers, indexed accesses, other encodings, Blueprint code and decode gaps are not exhausted by this scan.

To close G3 requires an actual dataflow path from component `+0x75C` or asset `+0x558` to a unit-defining computation and a resulting action, including its activation gates. The remaining work is typed/alias-aware reader resolution, including outstanding cross-module candidates and any applicable cooked Blueprint consumer. If that path exists only in a different server artifact, that artifact must be obtained and matched; its existence or behavior cannot be inferred from a client-side negative search.

**Correction to [round 92, section 5](round92-modes-economy.md#5-inactivitylifetimeoutsafezone):** retain the native 300 and initialization-copy facts. Replace universal wording such as “nothing in the client executable reads the value” and any conclusion that missing behavior must therefore reside on the server with the bounded search result above.

**Publication disposition:** keep asset values 90, 10 and 30,000 as raw stored values, and identify the native component default as 300. Label unit, consumer and resulting action **unverified**. Do not call the table column seconds, convert 30,000 into hours, or describe an unoccupied-vehicle removal timer. The vehicle-config page and safe-zone wiki must use the same qualification. The existence of separate lifetime-manager settings does not validate those interpretations.

## 3. Verification and evidence boundary

The private retained bundle contains the original `query.py`, `bytes.py`, `fn-*.json`, disassembly excerpts and SQL receipts, plus resumption queries, decoded cooked CDOs, bounded byte receipts and an executable verifier. Raw decompilation and secrets are not included in this public note.

Actual local execution:

| Check | Result |
|---|---|
| `Python313/python.exe verify_resume.py` | **exit 0**, `PASS`: 31 primary-image byte anchors, altered-byte negative control rejected, conversion literal verified, cooked spawner/CDO/data links checked, published/re-extracted data exports semantically identical |
| Read-only alias/member and DeepExtract lookup checks in that verifier | **exit 0**; interaction slot and five named field/layout rows recovered; activation body resolves to function ID 829583 |
| `Python313/python.exe scan_whole.py` | **exit 0**; exact-displacement candidate inventory and coverage limits recorded above; not a consumer-absence proof |
| Corrected-mapping cooked extraction, buildable / functionality / data asset | **exit 0** each; each log reports `ok=1 fail=0`, with no parser errors |

The first cooked extraction using the uncorrected mapping returned process exit 0 but logged inherited-class/CDO parser errors. It is retained as a **failed semantic extraction**, not used as proof. The corrected-mapping exports above replaced that evidentiary attempt without overwriting it. Initial helper execution with the default Python failed due to missing `pefile`; the installed Python 3.13 interpreter had the required packages. A pre-correction database batch timed out (exit 124); explicit `COLLATE NOCASE` now uses the existing name index as an indexed search instead of a covering-index scan. None of these failures is hidden by a successful shell redirection.

Verification checks establish the listed bytes, links and query results; the causal interpretation was manually reviewed. They are not an automated proof of all possible initialized control-flow paths. **G2's shipped/default selection is closed; G3's unit/action/consumer remains open.**

## 4. G3 continuation — the two outstanding cross-module reads have different owners

This additive continuation resolves the ownership questions specifically identified in section 2; it does **not** close G3. The original report is preserved verbatim above.

### Landscape candidate: `0x5088F78`

The containing source function starts at `0x5088DC0`. The previous scan's `0x5088EF3` is an interior unwind entry, not the start needed to recover its receiver provenance. At `0x5088E32` the function calls class getter `0x33AEE90`. That getter registers **`/Script/Landscape.LandscapeProxy`**; both registration strings were independently checked in the executable. The returned class is passed into the iterator initialization at `0x5088ECF`; its current actor reaches RDI at `0x5088EEE` before the candidate read.

For this owner, `+0x758` is integer `ALandscapeProxy.ComponentSizeQuads` and `+0x75C` is integer **`ALandscapeProxy.SubsectionSizeQuads`**. The source uses their ratio, scene-transform scale and a logarithmic calculation. This is not the vehicle inactivity float. Matching the numerical displacement alone had left an unrelated landscape calculation on the candidate list.

### Vehicle-movement candidate: `0x537C442`

The containing source function starts at `0x537C260`, not the interior unwind entry `0x537C31C`. It is **`UMWheeledVehicleMovementComponent` vtable slot 206**, a different component class from `UWDVehicleGameplaySystemsComponent`. The executable's table pointer at `0xAB70E88` independently points to `0x537C260`; `0x537C285` preserves its original `this` in RDI.

The nested typed layout resolves the field precisely:

- `UMWheeledVehicleMovementComponent.WheeledVehicleInput`: `+0x6E0`.
- Its `FMWheeledVehicleInput` local-input structure: `+0x68`.
- `FMWheeledVehicleLocalInputs.RawCrawlingInput`: `+0x14`.
- Combined offset: **`+0x75C`**.

The candidate load at `0x537C442` therefore reads **raw crawling input**, not inactivity lifetime. It is copied into the outgoing parameter block at `0x537C450`. The reverse branch loads `ReplicatedInputState.CrawlInput` from `+0x7E4` at `0x537C4C2` and stores it to `+0x75C` at `0x537C4C8`. The reflected replicated structure starts at `+0x7D0`, and its `CrawlInput` is at `+0x14`, independently corroborating the identity.

### What this does and does not settle

These two reads are now excluded by **receiver provenance and typed nested layouts**, not by module proximity or field-name similarity. Neither supplies a reader, time unit or expiry action for `InactivityLifetimeOutSafeZone`. The separate lifetime manager remains separate.

The recovered component-vtable source bodies and additional candidates are retained privately for further alias-aware review. That review is not a complete control-flow or adjusted-pointer proof. Blueprint metadata also needs care: the nested scalar is Blueprint-visible, but the containing `InactivitySettings` properties on the component and data asset are not marked Blueprint-visible in the recovered SDK. Neither fact establishes that a cooked Blueprint consumes the field or proves that all possible reflected accesses are absent.

**Remaining obligation:** find an actual read derived from the initialized gameplay component's `+0x75C` or data asset's `+0x558`, including any adjusted/indexed pointer or applicable cooked script path, and follow it through a unit-defining operation to an action. No missing server implementation has been demonstrated; requesting a server artifact as though client absence were proved would still be unjustified. G3 remains **partial**, with units and action **unverified**.

### Verification

`py -3.13 resolve_typed.py` and `py -3.13 verify_typed.py` both returned **exit 0**. The latter checks the primary-image SHA-256, eleven instruction anchors, an altered-byte negative control, the actual movement vtable pointer, both landscape class-registration strings, seven typed layout rows, valid containing-function ranges and indexed DeepExtract name lookups. Private receipts retain the precise queries and excerpts. These checks verify the two exclusions, not universal reader absence or live behavior.
