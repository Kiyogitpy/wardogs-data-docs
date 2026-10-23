---
title: Round 11 collision research
nav_exclude: true
---

# Collision resources and native actor-hit ordering

Checkpoint: 2026-10-20, starting at `34cf1248`. The persistent RE goal proceeds
in this order: vehicle collision/blast parity; spawn/loadout provisioning;
mapping residuals; targeted corpus cleanup; EXE restoration/devirtualization.
**The first track is active and incomplete.** Subsequent tracks have not been
started by this continuation. No game process or game service was accessed.

## Closed in this continuation

The preview's actor-hit sort previously used JavaScript's stable sort. Raw
CL-516586 routine `0x6B6FFD0`, with heap fallback `0x6B6FA90`, does not preserve
equal float-distance order. Two equal hits reverse; three equal hits change
from `[A,B,C]` to `[B,C,A]`. The preview now reproduces the native short-array,
partition and heap paths before the existing component swap filter.

Controlled Unicorn replay runs only these two raw routines over synthetic
256-byte records, with Distance at offset 8. An instruction whitelist rejects
execution outside the two routine ranges and three explicit helper models.
The `logf` and `memset` IAT identities were checked; the cookie-check model
asserts the expected cookie argument. This does not execute a host game
process or establish scene-query parity. All **783** replay permutations match
the JavaScript model; the replay reaches heap fallback **605** times. Tests
include equal keys, repeated keys, ascending/descending inputs and seeded
mixed inputs up to 128 hits. Regression checks also cover unequal JavaScript
numbers that round to the same native float.

The algorithm is now established for the tested finite-distance inputs.
**Actual overlap encounter order remains an unavailable runtime input.** The
separate authored-target sort is outside this actor-hit sort correction.

## Acquired collision resources

The fresh assembly census covers **33 variants**, **349 component/state rows**
and **156 unique mesh packages**, with zero unresolved package names. Rows
include skeletal meshes, unregistered components and intact/destroyed wheel
references; 349 is not a count of simultaneously active components.

| Acquisition | Result |
|---|---|
| Static mesh bodies | 121 BodySetups / 121 cooked payload occurrences |
| Explicit ComplexCollisionMesh references | 100 unique packages / 100 payload occurrences |
| Skeletal physics assets | 31 assets / 47 bodies / 11 cooked payload occurrences |
| Skeletal primitive metadata | 77 boxes, 98 convex elements, 10 capsules |
| All acquisition stages | Zero recorded extraction failures |

The **232** payload occurrences contain **190 distinct payload hashes**. The
expanded diagnostic decoder fully consumes all 190. Of these, 180 also pass
the old Gepard decoder and retain identical decoded output after removing
the added sentinel diagnostics. Ten previously rejected payloads require
lossless exceptional-UV handling or explicit convex missing-index handling.
The diagnostic output preserves **6,582 non-finite UV scalar values** with
their original byte patterns. Collision coordinates remain finite-checked.
Missing twins and unused-vertex markers are retained, without claiming that
those hulls form closed manifolds. Local UE source is schema guidance from
a different engine changelist, not proof of target runtime behavior.

All 190 distinct payloads reject a truncated tail and an invalid precision
header; 89 convex-bearing payloads reject an invalid half-edge vertex.
Original bytes and all raw geometry remain outside the checkout.

All **28 registered-component display omissions** now have linked resource
records. In particular, STN_05 references a recovered **274-triangle** mortar
base proxy. It remains table-only in the published viewer; acquisition alone
does not establish attachment, eligibility or placement. A render mesh's own
cooked BodySetup and the referenced proxy's independently cooked BodySetup
are recorded separately and must not be substituted for each other.

## Verification and restart

### Authored placement and partial wheel continuation

The follow-up places **27 of the 28** registered display omissions using
source component, bone and socket transforms. The remaining STN_06 gun proxy
requests missing `receiver_J`; it receives no fallback placement. All **126**
previously recorded static reference frames match exactly, including the T-72
barrel's named socket. Raw component GetSocketTransform `0x3D72B90`, reached
through skeletal-component vtable slot `+0x520`, uses a socket-map result
before its bone fallback. Skeletal asset slot `+0x3F8` resolves to
`0x44122D0`. Thus a socket sharing a bone's name does not make that attachment
ambiguous. Runtime socket overrides remain separate.

The later attachment-policy audit confirms that `SK_Browning_Mounted` has
**54 bones / 19 sockets** and no `receiver_J`. The fragment omits SocketMode;
native query constructor `0x50E09B0` supplies Explicit mode. Resolver
`0x50EE770` requires a positive `DoesSocketExist` result for a named explicit
socket. The skeletal vtable's slot `+0x540` reaches `0x3D6BE50`. Although
`GetSocketTransform` can retain the component transform on a miss, that alone
does not justify placing this proxy: the attachment caller separately gates
complete versus partial matches. Native manager constructor `0x50E08C0`,
called by the actor constructor at `0x50E0200`, disables partial attachment by
default. `missing-socket-attachment-policy-v1.json` and
`attachment-policy-validation-v1.json` verify **21 owned cases** spanning
default initialization, explicit socket responses and the caller gate.
Predicate responses are supplied; derived defaults, runtime aliases and
actual attachment state remain outside the replay. The proxy stays unplaced.

The profile constructor `0x50E0AD0` writes Flags **3** at settings `+0x0C`.
The direct static and skeletal fragment constructors call it on their
CollisionProfile fields. Explicit cooked flags win. Native `0x50E66C0` and
`0x50E6950` apply bit 0's configured Visibility/Camera/GameTraceChannel1 mask
for collision Types 0–2; set bits block and unset bits ignore. All **28**
omissions have a recovered **base Visibility response of Block**, with no
serialized shape overrides. This establishes their base response, not active
query registration or complex-shape eligibility. All three SPW interiors
explicitly use Flags 0 and remain Visibility Ignore. The broader 233-row
component census leaves 30 explicit-profile rows separate from flag-derived
responses; it does not infer their response from Flags.

Raw SetWheelActive `0x533B6F0` appends an activated instance. Removal uses
swap removal and changes the former last wheel record's InstanceIndex to
the removed index. Its **DataIndex remains unchanged**. Native owner helpers
`0x50C1000` and `0x50C1840` maintain Item-to-DataIndex mapping, and consumer
`0x50BF500` uses that mapping when forming indexed slot FNames. For example,
starting at `[0,1,2,3]`, removing wheel 1 produces `[0,3,2]`; Item 1 then
resolves to suffix `_3`. Reactivating wheel 1 appends it, producing
`[0,3,2,1]`. Current health states alone do not reveal this history.

Controlled replay passes **3,840 transitions** over 96 two-/four-/six-wheel
cases and **8,552 native indexed-slot resolutions**. Engine instance addition,
swap removal, cached transforms, weak handles, record lookup and resize are
explicit models. Native wheel-record and remap writes, normalization and slot
suffix consumption execute in the emulator. The fixture supplies successful
operations, registered same-owner components and empty group overrides; it
does not execute Chaos, rendering or asynchronous lifecycle behavior. The
viewer still exposes homogeneous wheel states rather than arbitrary histories.

Receipts: `omission-placement-v2.json`, `socket-precedence-policy-v1.json`,
`collision-settings-v1.json`, `wheel-remap-replay-v1.json` and
`wheel-manager-replay-v2.json` in the private evidence root. The earlier
placement v1 deliberately left a socket/bone name collision unresolved; v2
supersedes it after checking the shipped socket-first path.

The corrected actor-hit sort passes **6,864 catalog shots**, **62 additional
fresh/out-of-range shots** and **339 section applications**. The wider audit
passes **28,600 scenarios** and **2,364 indexed-query comparisons** over the
existing 36 displayed models and 22 explosive sources. It still records 1,089
outward damage increases and excludes STN_05 for missing published geometry.
These are software contracts, not live-game comparison results. Browser and
live-site checks were not rerun for this arithmetic-only change.

Private evidence root:
`E:/Reverse_Engineer/wardogs_analysis/round11_collision_parity_20261020/`.
Its `README.md` records exact outputs and next steps. Principal receipts:

- `assembly-census-v1.json`, `proxy-links-v1.json`, `collision-census-v1.json`;
- `decoder-validation-v1.json` and the three decoded resource directories;
- `native-sort-replay-v3.json`, `sort-model-validation-v2.json`;
- `impact-contracts-v1.json`, `blast-audit-v1.json`.

### Query filters and cooked contact comparison

The default engine ray path now has a target-specific filter trace. The
explosion LOS helper `0x6F03720` calls `0x3CAB670`; its world wrapper
`0x3CAE910` selects the world's PhysicsQueryHandler or the engine fallback.
The mapped default handler's vtable slot `+0x2C0` leads through `0x4252460`
and `0x3CAEB60` to that same fallback. Engine ray implementation `0x3C81440`
constructs callback `0x3C95950`; its PreFilter entries at vtable
`0xA3A1FD8 + 0x18/0x20` lead through thunk `0x3CADBD0` to `0x4250760`.
The wrapper checks the shape's query-enabled bit before common prefilter
`0x42505F0`. A different runtime handler remains outside this traced path.

Controlled replay results:

| Native decision | Coverage and boundary |
|---|---|
| Common prefilter | **79,360 cases**: complexity, trace/object channels, response pairs, extra masks, ignored actors/components and overlap/touch/block switches. No helper models. |
| Shape query gate plus common filter | **4,608 cases**: four storage selectors, both flag locations and enabled/disabled states. Shape-filter extraction and particle/component lookup are explicit fixture adapters. |
| Collision-enable creation block | **1,536 cases**: all input boolean flags, six collision modes, storage selectors and existing shape bits. Isolated block entry has supplied register context; preceding body construction is not executed. |

The creation block is `0x422A542–0x422A6A8`. Its collision-mode intersection
table at `0xA5FB0F0` agrees with the independent mode model. Query enable is
the conjunction of body-query and shape-query permission; simulation/probe
bits remain separate. The triangle branch at `0x423BB9B–0x423BBB6` supplies
isComplex=1 and shape collision mode 3 (QueryAndPhysics). This explains why
body query permission controls that triangle shape, while a simple-only
shape mask still fails a complex trace. Actual registration and later flag
mutations remain unobserved.

Private cooked reference scenes now cover the **36 displayed models** with
**230 placed triangle nodes and 196,094 triangles**, adding 26 placed bodies.
STN_05 has no displayed model and is outside this comparison; the unresolved
Browning gun attachment remains excluded. These scenes use each owning
mesh's cooked collision payload and source reference transforms. The three
SPW interiors remain excluded by their explicit Visibility Ignore settings.

The comparison holds origins fixed and runs the same double-sided software
raycaster and approximate overlap admission on three representations: display
geometry, cooked represented bodies, and cooked bodies plus placed omissions.
Across **12,056 cases / 22 explosive sources**, replacing represented geometry
changes contact selection or damage in **3,470** cases; adding the omitted
bodies changes it in **1,010**. Main-damage changes greater than 0.01 occur
in 572 and 131 cases respectively. There are **zero unresolved material-slot
contacts**. Source identities were checked for 413 inputs. Surface origins
selected on display triangles can change sides of a cooked hull after tiny
coordinate changes; these are conditional sensitivity results, not observed
game errors or native-physics validation. The viewer assets are unchanged.

New receipts: `query-filter-policy-v1.json`, `query-prefilter-replay-v1.json`,
`shape-query-gate-replay-v1.json`, `shape-enable-creation-replay-v1.json`,
`conditional-cooked-scenes-v1/manifest.json`,
`cooked-contact-comparison-v1.json` and `cooked-comparison-input-audit-v1.json`.

### Native triangle-ray boundary replay

The shipped triangle-mesh virtual wrapper (`0x2327D60`, vtable
`0x9C10FC8 + 0xB0`) now executes under isolated emulation through both
16-bit and 32-bit index paths, including their native visitors. All **1,184
owned synthetic cases pass**: 1,152 culling/winding/edge/endpoint cases,
12 face-order cases and 20 small/degenerate-triangle cases. Only a checked
security-cookie adapter is supplied; geometry and traversal routines execute
their frozen-build bytes. Fixtures use a supplied one-node BVH with bounds
padded by 0.01 cm, so these tests do not establish actual cooked BVH traversal.

The visitor uses float32 vertices, double intersection arithmetic and a
float32 traversal distance. Four fixture cases select the slightly farther
face because rounding either excludes a nearer successor or admits a farther
successor. Equal-distance faces can overwrite earlier hits. The determinant
and barycentric tolerance is `float32(1e-8)` in the visitor's local UE units;
normal normalization has a separate squared-length threshold and can return
a zero normal for an accepted small triangle. A strict double-nearest query
with stable ties does not reproduce these decisions.

The portable diagnostic model in [_tools/vehicle_native_ray.js](../_tools/vehicle_native_ray.js)
matches all 1,184 native receipt decisions. Run
`node _tools/vehicle_native_ray_check.js <private native-triangle-ray-replay-v3.json>`.
The visitor-only entry requires supplied face order and local centimetre
coordinates. The cooked-BVH entry is validated separately below. Neither
entry supplies world scene membership or instance transforms.
No viewer ray behavior was changed by this diagnostic integration.

Native shape creation sets backface culling from the inverse of the body's
double-sided flag. Two acquired own bodies explicitly serialize that flag as
true (ROT_03/ROT_04 body meshes). The native class default for the other 119
omitted flags is now established below. The BodySetup constructor preserves
that bit, so its mask alone would not prove the default is false.
Mirrored placements also need determinant-aware winding/culling handling;
the earlier double-sided cooked comparison does not settle it.

New receipt: `native-triangle-ray-replay-v3.json`; v1/v2 retain their narrower
small-index and wrapper-boundary results.

### Native defaults, cooked BVH traversal and scale wrappers

The frozen allocator `0x19305A0` zero-fills new/non-recycled UObject storage
through a verified `VCRUNTIME140!memset` import. The native CDO path
`0x180D760` allocates with flags `0x31`; its post-construction property copy
uses the superclass's property-size boundary. BodySetupCore ends at `0x38`,
well below the `bDoubleSidedGeometry` bit at `0xD8`. BodySetup's own mask
preserves bit 3, leaving the allocated zero intact. Its post-init hook changes
the GUID at `0x108`; the relevant native UClass and post-CDO hooks are empty.
**256 zero-fill/default-path cases and 256 flag-preservation cases pass.**
This establishes the native class default as false. It does not capture a
live CDO or rule out arbitrary serialized archetype overrides/runtime changes.

Native factory callers `0x423BCE0` and `0x3550970` copy BodySetup's bit into
geometry parameters; `0x423A2C0` sets triangle backface culling to its inverse.
The culling setter is `0x232A9C0`. All 121 acquired own bodies have either
the omitted native-default flag (119) or an explicit true flag (2).

The local mesh replay now uses **original decoded cooked BVH topology and
bounds**, with no padding, across **120 distinct own-body payloads**. Both
index widths and both culling choices run through the shipped wrapper and
native visitors: **6,720 queries, 5,430 hits and 30,746 face visits**. The
portable model matches the exact face-visit sequence, hit/miss, face index,
time, position and normal. Queries enter in asset-local centimetres; this
does not establish world broadphase/filter membership or dynamic poses.

The native scaled-mesh vtable slot reaches `0x21DD860`; its scale setter is
`0x21E1B20`. This wrapper rounds scaled inputs and output vectors through
float32, normalizes the local ray direction in double precision and rejects
the far endpoint with a strict comparison after the local inclusive query.
It clamps scale magnitudes below `float32(1e-6)` to a positive minimum,
including tiny negative values. At zero time it writes the original start
and negative incoming direction. **3,456 owned cases pass**, including
mirrors, nonuniform/near-zero scales, tilted faces and **1,332 zero-time hits**.
The portable model matches every case, including native BVH visit order.
Mirrors retain local triangle winding and transform the ray through inverse
scale; simply reflecting world vertices without handling winding is inadequate.

Run the private-receipt comparisons with:

```text
node _tools/vehicle_cooked_ray_check.js <cooked-bvh-ray-replay-v1.json>
node _tools/vehicle_scaled_ray_check.js <scaled-mesh-ray-replay-v2.json>
```

`ray-default-policy-v1.json` binds 24 raw spans and six vtable slots;
`body-default-replay-v1.json`, `cooked-bvh-ray-replay-v1.json`,
`scaled-mesh-ray-replay-v2.json` and `portable-ray-model-validation-v2.json`
record the proofs. The portable validation covers **11,360 cases** across
the three ray suites. Raw resources stay outside the checkout, and viewer
behavior remains unchanged by these diagnostic additions.

### Native transformed wrapper and actor-ray entry

The transformed-object wrapper (vtable `0x9C05E00`, slot `0xB0`, actual
entry `0x20706C0`; indexed corpus start `0x20706BD`) passes **4,608 owned
cases**, including optional scaled meshes, rotations, translations and large
coordinates. All hit/face/time decisions and supplied BVH visitation orders
match the portable model. In **1,728 zero-time hits**, this wrapper leaves
the caller's position/normal storage untouched. The portable API explicitly
returns unspecified vectors for that branch rather than manufacturing them.
The wrapper's own FTransform scale is unit in these fixtures; mesh scaling
uses the separately replayed scaled implicit object.

The world query's visitor vtable `0x9C39670 + 0x10` reaches `0x246F800`, a
jump to `0x2466830`. Its **1,728 single-shape actor cases / 866 hits** pass
with owned particle poses, direct/scaled/transformed mesh dispatch and a
blocking-hit buffer. Actor rotation is read as float32; actor translation is
double. The portable model matches hit admission, face, float32 reported
distance, updated double query length and continue/stop decisions. Position
and normal also match where the inner geometry supplies them. **54 cases**
inherit unspecified vectors from the transformed wrapper and exclude those
vectors from comparison; other hit fields remain checked. Fixture broadphase
admission is supplied and pre/post filters are disabled. Multiple-shape bounds
and filtered shape iteration remain outside this replay.

The world entry `0x3C81440` rounds segment magnitude to float32 and divides
the double delta by that rounded magnitude. Its direction therefore need not
have exactly unit length. **1,051 arithmetic/threshold cases** match exactly,
including 15 rejected near-zero segments. These execute selected raw blocks
with supplied registers; intervening engine setup/locking and scene traversal
are not executed.

The downstream hit converter `0x3C6C430` is saved and statically traced. When
distance is nonpositive and the query-geometry argument is null, its math
uses the segment start and reverse segment direction instead of the incoming
position/normal vectors. A nonnull query geometry takes another helper path.
The caller ABI and converter fallback still need controlled replay; the
saved pseudocode alone does not settle the 54 unspecified-vector cases.

New receipts: `transformed-mesh-ray-replay-v1.json`,
`actor-ray-visitor-replay-v1.json`, `world-ray-input-replay-v1.json`,
`world-ray-replay-input-audit-v1.json` and
`portable-ray-model-validation-v3.json`. The six portable comparison suites
pass **18,747 cases**; this count includes the 54 explicitly limited actor
cases described above. Producers, transitive setup inputs, raw ranges and
dispatch bindings were checked. The viewer still uses its existing backend.

### Multi-shape filtering, hit conversion and reference-backend integration

The native two-shape loop now passes **3,328 cases**, including world-bounds
rejection, simple/complex flags, disabled query shapes, Ignore/Overlap/Block,
ignored actor/component identities and reversed shape order. The query gate
and common filter execute their frozen bytes. Only filter/identity extraction
and the security cookie use adapters. The portable model matches filter-call
order/results, geometry face visits, selected shape/face, distance, query
length, vectors and traversal continuation. Broadphase admission, world bounds,
filter words and fast-ray parallel/inverse values are supplied fixtures;
postfilter is disabled and touches are ignored, as in the LOS configuration.

The ray-hit converter math passes **1,016 cases / 992 accepted records**,
including all 866 earlier actor hits and 150 additional zero/negative-distance,
missing-vector-flag, nonfinite and small-segment cases. Its null-query-geometry
path discards incoming vectors at nonpositive distance, uses the segment start
as impact point and safely normalizes the reverse segment for its normal.
That establishes the downstream fallback for the 54 actor cases with
unspecified inner vectors. Positive-distance invalid vectors reach the native
invalid-reset boundary. Response is supplied as Block; identity filling is a
no-op adapter, and optional face/material/object outputs remain outside this
math replay. The separate native ray callsite passes **64 ABI cases** and
supplies null for argument 8; the RSI zeroing and subsequent writes were
checked against the frozen function. Intervening calls rely on the Windows
x64 nonvolatile-register contract.

The eight portable ray suites now pass **23,091 comparisons**, bound in
`portable-ray-model-validation-v4.json`. New receipts are
`multi-shape-ray-replay-v1.json`, `ray-hit-conversion-replay-v1.json` and
`ray-converter-callsite-replay-v1.json`. The identity helper `0x3CB3030` is
also saved for subsequent object/material tracing; it is not fully replayed.

The private builder `build_native_reference_scenes.py` produces a native-query
manifest for **36 scenes / 230 placed components / 196,094 triangles**, with
**113 distinct used cooked resources**. It retains original local vertices,
BVHs, face/material lookup and per-body culling. Supplied poses are decomposed
from source-reference matrices rather than baked into float32 world vertices.
The largest matrix reconstruction error is `4.44e-6`; these are rounded source
poses, not recovered original quaternion bits or captured runtime poses.
Eligibility and encounter order remain supplied reference assumptions.

[_tools/vehicle_cooked_backend.js](../_tools/vehicle_cooked_backend.js) attaches
these private resources to the existing offline blast simulation. The core
now optionally uses `traceSegment(start, end)`, preserving authored endpoints
through native world-input rounding; its existing ray backend remains the
default. A regression fixture checks both pretrace and target endpoints.
The default viewer checks pass **6,864 catalog shots**, 62 extra shots and
339 section-routing cases. Cooked query geometry is prepared once and checked
against all 6,720 original native cooked-BVH cases.

Across **12,056 cases / 22 sources / 36 scenes**, the conditional native
backend changes selected contacts, first section or main damage in **965**
cases versus the existing double-sided cooked-scene raycaster. Main-damage
changes above 0.01 occur in **442** cases. There are **zero unresolved material
slots**. This comparison holds cooked GLB closest-point overlap admission and
sampling metadata fixed; it combines culling, local query arithmetic, supplied
pose decomposition and native hit conversion effects. It is not an observed
game discrepancy or a count of every numerical contact difference.

Receipts: `conditional-native-scenes-v1/manifest.json`,
`native-reference-contact-comparison-v1.json` and
`native-reference-input-audit-v1.json`. The audit checks **194 comparison
input identities**, source poses/resources and the three new probe producers.
The backend remains a private Node reference tool. The browser viewer has no
new native-query mode or published cooked assets.

The complete conditional scene ray path now matches a native oracle on
**858 segments / 605 hits / 4,980 candidate calls** across all 36 scenes.
`reference-scene-native-oracle-v1.json` and the ninth portable ray checker
bring the current ray validation to **23,949 comparisons** in
`portable-ray-model-validation-v5.json`. Candidate admission, reference poses,
Block eligibility and encounter order are supplied; the oracle does not
establish native world acceleration or captured scene state.

Target-point ordering is now corrected in the simulation: native float32
squared-distance keys in UE centimetres feed the same unstable sorting
algorithm used for actor hits. Native target-sort replay covers **783 arrays
/ 605 heap calls**; a separate arithmetic replay verifies **1,029 keys**.
Equal keys can reorder. The actor-sort regression and the existing viewer
checks pass after this change. Current comparison and input receipts are
`native-reference-contact-comparison-v2.json` and
`native-reference-input-audit-v2.json`; the 12,056-case comparison retains
**965 changes / 442 main-damage changes above 0.01 / zero unresolved slots**.
The v1 comparison receipts above are historical.

The local no-MTD sphere overlap model separately matches **13,288 native
comparisons**: 1,696 sphere/triangle cases, 4,032 owned one-leaf mesh cases
and 7,560 queries over 120 original cooked meshes, with exact traversal order
across 36,299 face visits in the cooked set. The query-transform translation
is in unscaled mesh coordinates; mesh scale is applied separately. Native
degenerate-triangle behavior can differ from a generic closest-point test.
`portable-overlap-model-validation-v1.json` bound these three suites at that
checkpoint; integration and the current validation are described below.

The next actor layer passes **300 owned single-shape cases / 176 overlaps**
through native visitor `0x2461330`, dispatcher `0x2042BA0`, relative transform
`0x165FE90` and the unscaled mesh path. `actor-overlap-validation-v1.json`
binds `actor-sphere-overlap-replay-v2.json` to the checker and frozen bytes.
Geometry outcomes and face traversal match exactly with the native-dispatched
local centre; the inverse actor transform has a separate numerical tolerance.
Admission and query/actor poses are supplied, filters and MTD are disabled,
and TLS initialization state is owned fixture data. This is the overlap
method of a **hit-record visitor**, not the default overlap-buffer visitor.

Its transformed unscaled path now passes **600 cases / 348 overlaps** in
`actor-sphere-overlap-replay-v3.json`. Native code composes shape and actor
poses before inversion; sequential inversion differs slightly with float32
actor quaternions. The checker follows the composed pose, with numerical
transform tolerance and exact geometry/traversal using native local centres.
The scaled/transformed path adds **1,800 cases / 996 overlaps** in
`actor-sphere-overlap-replay-v6.json`. The latter supplies native-generated
query bounds and centres to the model; radius/scale, geometry outcomes and
face traversal match exactly. Generic scaled dispatch transforms query bounds
separately, so the direct sphere overload's AABB is not interchangeable.
`portable-overlap-model-validation-v2.json` binds all five current suites
and **15,688 cases**, including the 13,288 earlier local comparisons after
extracting the common traversal. V1 validation receipts are historical.

The corrected `default-overlap-route-v2.json` decodes **all 137 query-type
entries** in the two-level dispatch table. V1 incorrectly labelled a call
as the sphere route without decoding that table and is superseded. The world
chain remains `0x3CA0DA0` → `0x3C99310` → `0x3C73C30`, but sphere type 0
selects **`0x24495D0`**, not `0x24474B0` (type 1). With query flag `0x40`
clear, the sphere constructor selects vtable `0x9C39BC8`; its overlap thunk
reaches **`0x2460100` → `0x2042BA0`** and the already tested sphere geometry
dispatch. The buffer's blocking indicator is offset 68 rather than 140.
`default-actor-sphere-overlap-replay-v1.json` now replays that actual sphere
visitor over **1,800 scaled/transformed cases / 996 overlaps**, still using
native query bounds/centres for the portable geometry comparison.

`multi-shape-overlap-replay-v1.json` adds **1,088 cases** through the native
default visitor, query gate/common prefilter, two-shape bounds checks, Touch
and Block collection, and finalizer `0x246C800`. These cover both orders,
query enablement/complexity, response masks, actor/component exclusions,
ignore flags, Block demotion and early termination. Touch records retain
encounter order; the finalizer appends the last retained Block record after
them. The portable unscaled actor model matches filter calls, face visits
and final result order. Supplied shape bounds, filter words, actor identity
and world admission remain fixture inputs. Postfilters and allocation growth
are outside this replay.

`overlap-callback-setup-replay-v1.json` separately verifies **32 cases** in
callback constructor `0x3C95950` and the actual world setup block before
`0x3C71108`. World overlap forces callback Block-to-Touch demotion and keeps
supplied ignore flags. Query flags are 4, or 36 when skipping narrow phase.
The replay uses empty/single ignore lists and stops before world execution.
`portable-overlap-model-validation-v3.json` binds **eight current suites /
18,608 cases** after the model additions. Earlier validation receipts are
historical. That checkpoint preceded the private overlap integration below.

Scaled query inputs are now computed from the supplied world sphere and poses.
The native bounds helper rotates **four box diagonals** and takes componentwise
maxima. Summing absolute rotation-matrix terms differed in 24 float32 bound
coordinates near zero; reproducing the native arithmetic removes those
differences. The 1,800-case input check now has **zero centre or bound
differences**, with exact geometry outcomes and traversal. This proves the
tested fixtures, not every possible pose/scale or future build.

`reference-scene-native-overlap-oracle-v1.json` runs the actual default sphere
visitor and original cooked resources across **36 scenes / 744 sphere queries
/ 4,814 candidate calls / 7,739 face visits**. The computed model matches
membership and traversal, including **819 scaled candidates**. Of the 744
queries, 352 overlap at least one component. Scene candidates, eligibility,
source-reference poses and encounter order remain supplied assumptions;
world acceleration and result identity conversion are outside this oracle.

The private backend now exposes `overlapSphere(origin, radius)`, and the blast
core uses its supplied component membership/order when present. This removes
the closest-point gate from that backend's simulation path. The default viewer
keeps its existing geometry path. Attached-backend membership matches all 744
oracle cases; the core regression verifies both an accepted component and an
empty sphere result without calling the closest-point gate. Default viewer
checks still pass **6,864 catalog shots / 62 extra shots / 339 routing cases**.

Current receipts are `portable-overlap-model-validation-v4.json` (**11 suites /
21,896 comparisons**) and `portable-ray-model-validation-v6.json` (**9 suites /
23,949 comparisons**). Counts include repeated queries checked at different
layers. `native-reference-contact-comparison-v3.json` compares **12,056 blast
cases** with the integrated backend, plus a native-ray-only control. The
overall legacy comparison remains **965 changed cases / 442 main-damage
changes above 0.01 / zero unresolved slots**. Isolating the sphere-overlap
change yields **zero additional selected-contact/first-section/main-damage
changes** in that set. The 744 standalone sphere queries likewise have no
membership differences from the prior closest-point gate on these inputs.
These are conditional software comparisons, not observed game discrepancies.
`native-reference-input-audit-v3.json` checks **195 comparison input identities**.

Overlap-result conversion now has a **452-case native replay**, including
**371 hash-path cases / 45 linear-path cases / 36 empty-input cases**.
The frozen threshold at `0xCD52590` is 3. `0x3C6B360` executes native response
classification, weak-object resolution/equality, both dedup paths and record
copying against owned fixtures; shape-handle/filter extraction and converted
identity filling are explicit adapters in this replay. The key includes
physics-owner identity, component weak identity and effective item index.
The item index participates only when the resolved component's flag at
offset 667 contains `0x10`; otherwise it is treated as `-1`. Duplicate
replacement preserves the first result's position and upgrades its contents
only from nonblocking to blocking. Existing output records are included.
`overlap-result-dedup-replay-v1.json` and the portable dedup checker match
classification, retained records and order. Tests stay within the inline map
capacity; allocation growth is not covered.

Two separate identity replays execute `0x3CA2B40` without replacing identity
helpers. **144 body-instance cases** cover direct/type-8 user data, optional
weld-parent selection with an empty weld map, valid/stale/null owner weak
references, physics-owner selection and a null virtual owner override.
**336 direct-component cases** cover native weak assignment and a native
one-entry ISM lookup. Storage values below 2 select a null map key; other
values use the particle pointer. A nonnegative first index with second `-1`
is used directly; a nonnegative second index uses the high-bit encoding.
The body and component receipts are `overlap-body-identity-replay-v1.json`
and `overlap-component-identity-replay-v1.json`. These prove conversion of
owned state, not the actual game's component/body/instance mapping.

`overlap-result-model-validation-v1.json` originally bound **932 comparisons**.
The current v2 receipt below also reconstructs the exact previously tested query
module by removing only the new dedup function/export, and verifies every
other v3 blast-comparison input unchanged. This preserves the prior query
evidence without treating a historical whole-file hash as current.
The follow-up `overlap-weld-owner-identity-replay-v1.json` adds **48 cases /
24 owned callback invocations**. Native weld-map iteration tests active shape
matches, inactive entries, misses and weld-parent fallback. The type-8 owner
callback protocol copies a supplied weak identity to the owner field without
changing the selected body component or physics owner. The callback itself
is a small owned guest implementation; this does not recover the shipped
owner implementation or actual game welding state.

`overlap-instance-consumer-replay-v2.json` adds **120 cases** through native
`GetItemIndex` (`0x3EC25F0`) and the entry gate of `GetInstanceTransform`
(`0x3F6BA10`). Its **13 accepted cases** stop at the matrix-to-transform call
boundary and identify the selected 128-byte matrix record. Rejected cases
return false without writing the supplied transform. High-bit encoded item
values stay negative here and are rejected; native indexed-slot helper
`0x50BF500` likewise leaves the base FName unchanged for negative input.
These encodings must not be silently treated as physical array indices.
The checker makes **23,113 cross-receipt joins** from accepted physical items
to the previously replayed wheel remap states and indexed slot suffixes.
Those joins are consistency checks between separately proven stages, not a
new native end-to-end replay or a captured lifecycle history.

`overlap-result-model-validation-v2.json` now binds **five suites / 1,100
comparisons**, including the 932 earlier cases, and preserves the query-source
equivalence proof. V1 is historical. Multi-entry identity-map collision
coverage, serial allocation and GC barriers remain outside these replays.
The private backend still receives source-reference component identities;
it does not claim captured native object provenance.

The static pose precision follow-up is now verified. `MeshMode.Bones` adds
`decoded_ue_local` to bone/socket records, with unrounded decoded binary32
values and authoritative bit patterns, plus an explicit precision label. The
35-package extraction preserves all existing skeletal output fields exactly:
**1,100 bones, 279 socket occurrences and 13,511 decoded scalars**, including
545 negative zeros. `decoded-pose-validation-v1.json` binds the sources,
binaries, schema and outputs. Build: 666 warnings, zero errors; extraction:
zero failures. The old mixed package list also skipped 121 non-skeletal
packages; the new list requests exactly the 35 skeletal packages.

The parser's `ReadFReal` narrows binary64 to binary32. Private raw-package
recovery therefore goes further than the new exporter fields.
`serialized-reference-pose-v1.json` recovers **11,000 serialized binary64 bone
scalars** from unique complete-array matches in all 35 packages. Every scalar
rounds to the decoded float bit pattern, preceding parent indices agree and
the arrays lie within one bounded Zen export each. **5,974 values** change
when narrowed to binary32.

`serialized-socket-pose-v1.json` recovers **1,077 serialized binary64 socket
scalars** from 359 vector/rotator property ranges. The remaining 478 omitted
vector fields retain explicit parser defaults; they are not claimed as stored
bytes. This covers 279 occurrences of **235 unique sockets** in 36 source
packages; 795 serialized scalar occurrences change when narrowed. Debug parser
positions, complete bit comparisons and owning export bounds bind the ranges.
The first socket probe failed on plugin mount-path resolution and has no valid
manifest; its partial output is excluded. V2 resolves only unique source-file
basenames and completed all 35 meshes.

`serialized-pose-checkpoint-validation-v1.json` independently rechecks **82
input identities, 3,659 serialized ranges and 235 duplicate-socket consistency
keys**. These new receipts do not replace the historical scene/oracle inputs
or imply those scenes have been regenerated with the recovered precision.
Raw packages and pose receipts remain private outside this repository.

The positive-scale transform multiply at `0x16670B0`, called by the native
socket-transform path `0x3D72B90`, now has an exact portable model in
`_tools/vehicle_native_transform.js`. Unlike the exporter's composition, its
positive-scale branch does not normalize after each quaternion multiply.
`reference-bone-composition-native-v1.json` accumulates all 35 recovered
hierarchies through **1,065 shipped native multiplications**; the 35 root
transforms are copied. All 1,100 component records match the portable model
bit for bit. Every recovered bone scale is nonnegative. This proves arithmetic
on supplied hierarchies, not the actual engine reference-pose construction
caller or the negative-scale matrix branch.

`reference-bone-world-caller-v2.json` then executes the native bone-transform
wrapper/core (`0x3D6E180` / `0x3D6E200`) in **7,860 owned cases**. Its 6,600 valid
cases select the expected 96-byte component-pose record and compose it with
one of three supplied world transforms; 1,260 disabled/invalid-index cases
return the supplied identity. Both buffer selectors are covered, with an
unmapped poison pointer in the other buffer. The native weak resolver executes
on a null leader weak reference. No remapping or animation lifecycle is claimed.

The mutable identity at `0xD01A840` lies in the unbacked virtual tail of `.data`.
V1's emulator mapping zero-filled it, causing the portable rejection-case
comparison to fail. V2 explicitly supplies initialized identity state; this is
owned fixture state, not recovered startup behavior or literal stored identity
bytes. V1 is superseded. The original
`reference-transform-model-validation-v1.json` bound 107,520 scalar bit patterns;
the current v2 validation below extends the checker and preserves v1 as history.

`reference-socket-transform-native-v1.json` executes native skeletal socket
local-transform helper `0x44176D0`, reached from reflected wrapper `0x3A76F30`.
All **279 socket occurrences** execute native rotator conversion `0x166D220`
and the shipped packed sine/cosine path (`0x98EB1D0` -> `0x98ED960`), followed
by native positive-scale composition. Trigonometry is not replaced by host
math. The portable multiply consumes the frozen native local results; this
does not claim a portable trigonometric implementation. The current
`reference-transform-model-validation-v2.json` binds all three native receipts,
source/SDK identities, code ranges and the updated model/checker, and checks
**110,868 scalar bit patterns**.

> **Round 19 re-verification.** Evidence level: static-analysis image; virtualized dispatch not removed. Helper `0x44176D0` has byte-identical code in both images (no stub, no changed constant or branch); the page-level difference lies in the preceding function's tail at the page start (`0x4417000`–`0x441705F`). Unaffected.

The socket-cache construction entry is now aligned and replayed at
`0x441D5B0` (the corpus begins at a garbage prefix, `0x441D5AF`).
`socket-cache-construction-v2.json` executes all 35 meshes through the native
builder, reference/skeleton getters, bone-name lookup, sparse reserve,
insertion/hash/duplicate logic, and native rotator conversion/trigonometry.
Owned preallocated storage holds 64 entries, 128 allocation bits and 128 hash
buckets; allocation growth and resetting a populated cache are not covered.
Only bounded `memset`/`memmove` and the security-cookie assertion are supplied.
The bone-name map uses **20-byte entries**, confirmed in the native lookup;
the initial 24-byte fixture was rejected by the instruction budget and fixed
before producing the receipt.

The builder converts **279 socket occurrences into 271 cache entries**.
Eight skeleton duplicates in ROT_04, WHL_02, WHL_05 and WHL_07 are shadowed by
mesh sockets. Every constructed entry passes native `FindSocketInfo` and the
real skeletal `DoesSocketExist` predicate (`0x3D6BE50` -> `0x3D723E0`).
Four ROT_02/ROT_03 windshield-wiper entries have bone index `-1`, but the
predicate still succeeds through the socket object's nonzero authored
`BoneName`; it does not validate that bone index.

`socket-cache-world-caller-v1.json` executes the complete skeletal
`GetSocketTransform` path with real one-entry cache lookup/hash in **4,464
cases**, including **64 missing-bone cases**. World space (`0`) and
parent-bone-local space (`3`), both pose buffers, enabled/disabled components
and two supplied world transforms are covered. A matching socket with missing
bone returns its cached local transform for space 3, and the **component world
transform** for space 0. The portable policy matches all **53,568 output scalar
bit patterns**. These fixtures supply FName/object identities and cache state;
actor/component-relative spaces, aliases, cache misses and live state remain
separate. The existing scene loader's skeleton-first/mesh-override ordering is
correct; its missing-bone omission must not be used as this native fallback.
The Browning `receiver_J` remains a separate absent-socket case and unplaced.

Actual component-pose construction is now traced through `0x445D550`, called
from the reference-pose reset path at `0x3D80100`. The scalar branch normalizes
each child quaternion after multiplication, whereas the earlier arithmetic-only
hierarchy did not. **239 bone records** differ from that raw accumulation.
`reference-pose-construction-native-v2.json` executes all 35 recovered
hierarchies in scalar mode and ISPC dispatch level 2: **70 cases / 2,200 bone
records**, with identical output between the two paths and intact output
canaries. `_tools/vehicle_reference_pose_check.js` verifies **26,400 scalar bit
patterns** against the normalized portable construction model. Full bones are
required in parent order; partial required-bone lists and negative scales are
outside this construction fixture.

The frozen feature flag at `0xCD5FB90` is 1, selecting the ISPC dispatcher.
Unicorn cannot execute the vector instructions at dispatch levels 3, 4 and 7;
exact failures are retained in the v2 receipt. The old v1 mode name
`ispc_sse2` was provisional; use the **numbered v2 dispatch levels** as evidence.
An isolated local leaf-math fixture then ran frozen routines at levels **2, 3
and 4** on this host: **105 cases / 3,300 bone records**. It maps only 22
verified static code/data pages, permits no out-of-leaf branches or calls,
checks CPU capabilities and output canaries, releases its own mapping and
never loads the game or attaches to a process. Levels 2 and 3 match the scalar
results exactly. Level 4 uses fused operations and differs in **187 records**
by at most `2.842170943040401e-14`; those 1,100 records are **native baked
inputs**, not a claim that the scalar portable model predicts FMA arithmetic.
Host AVX-512 is unavailable, so level 7 was skipped. The receipt is
`reference-pose-host-math-v1.json`; actual game feature selection is not captured.

`pose-socket-checkpoint-validation-v2.json` is the current source binding for
these construction, cache and caller proofs. It also reruns the earlier
arithmetic fixtures against the current helper/checker sources; older
transform-validation whole-module hashes are historical. No existing scene
oracle or browser default was changed by this continuation.

The normalized frame and scene refresh is now integrated and verified.
`engine-reference-transforms-v1.json` contains **1,371 bone/socket frames**
from the native host-level-4 pose profile and canonical cache policy. Native
matrix conversion `0x1676730` produces `engine-reference-frames-v1.json`.
The source assembly refresh changes 177 of 233 regular component placements
and 195 represented frames; the largest matrix-coordinate delta is
`0.0011171837159469037` UE centimetres. The same 16 source assemblies remain
unresolved, including the absent Browning socket; there are no new resolution
regressions. Fragment/static-socket affine assembly still uses decoded source
inputs and is not claimed as native whole-attachment execution.

`conditional-native-scenes-v2/manifest.json` preserves all **36 scenes, 230
components and 196,094 triangles**, including 26 added omission occurrences.
Sampling points and homogeneous ISM aggregate bounds were regenerated from
these frames. Independent eight-corner boxes and ordered union verify all
**18 ISM groups / 78 instances**, within `4.440892098500626e-16` metres.
Rendering and conditional query resources now use the same refreshed inputs.

`reference-scene-native-oracle-v2.json` supplies **858 rays / 599 hits / 4,980
native candidate calls**. The complete portable backend matches node, face,
material, distance, flags and converted-vector checks. The v2 overlap oracle
covers **744 spheres / 4,814 candidates / 7,739 face visits**, including 819
scaled candidates, with exact membership/traversal and scaled-query input
checks. The older v1 ray/overlap fixtures still pass after the checker adds
explicit manifest/fixture path options.

The new **12,056-case / 22-source** explosion comparison reports zero unknown
slots. Relative to the previous native-reference profile, 946 contact/order or
main-damage signatures change; ten main-damage changes exceed 0.01 and the
maximum is **313.5**. Small frame changes near boundaries can change the
selected slot or retained contact order, so these were not dismissed as small
numerical drift. Both profiles of all ten cases were captured: **929 unique
rays / 6,882 native candidate calls** and **20 spheres / 180 candidates**.
`critical-pose-native-query-replay-v1.json` then feeds only recorded native
query results into 20 portable explosion simulations. All contact identities,
order, first sections, application amounts and main damage reproduce exactly.
This validates query-backed integration; it is not a full native gameplay or
live-world invocation. Comparison with legacy queries on the new scenes shows
860 contact/damage changes and 438 main-damage changes above 0.01.

### Local reference mode in the viewer

The viewer now accepts a **local-only reference pack**, replacing both the
rendered collision mesh and simulation metadata/query geometry. The private
`native-reference-pack-v1.json.gz` contains all 36 scenes and 113 resources:
**10,897,954 compressed bytes**. No raw geometry or pack is written into the
checkout. Open **Local reference geometry**, choose this file, and use
**Use published geometry** to release it and return to the existing view.
The browser verifies the frozen build, manifest, resource and GLB hashes;
GLBs with external resource links are rejected before a blob URL is created.
Unsupported/malformed packs do not replace an active valid pack.

`assets/js/vehicle-cooked-queries.js` is generated from the canonical RE math
and backend helpers by `node _tools/build_vehicle_cooked_queries.js`;
`--check` verifies freshness. The Node backend keeps its existing `attach`
contract and adds an injected prepared-resource loader for the browser.
Reversing only that loader change reconstructs the exact historical backend
hash used by the v4 comparison; no ray/overlap arithmetic was changed.
`browser-reference-pack-validation-v2.json` verifies all 36 packed models
against the 858-ray and 744-sphere native oracles, plus seven negative/lifecycle
checks. Unknown models remain explicit and disposing a pack revokes its URLs.

Browser verification passes at **1440px and 360px**, including local import,
a native-query-backed shot, malformed-file recovery preserving the active
pack, destroyed-wheel switching and reset to published geometry. Existing
checks pass for all **23 vehicles / 154 routing slots**, Gepard transfer,
three SPW front shots and 30mm blast controls. The pre-change browser harness
failed a shorthand CSS `background` assertion; the intended `backgroundColor`
property is now checked, and the complete suite passes. Screenshots were
reviewed together and the UI detector reported no findings. A focused browser
confirmation also passes after self-contained-GLB validation was added.
The harness uses deployed theme CSS plus current rules as native nested CSS;
a Jekyll/Sass build was not run.

`native-scene-refresh-validation-v1.json` binds **654 current input identities**,
the native ranges, independent ISM audit, frame refresh, critical-query replay,
pack and browser evidence. Earlier whole-backend hashes are preserved through
the explicit loader-only source-equivalence check. Core gates pass: **6,864
catalog shots, 62 fresh/out-of-range shots and 339 routing applications**;
link checking reports zero broken links. No commit or push was made.

The default shape-complexity audit below resolves the shipped policy for the
112 BodySetups that omit `CollisionTraceFlag`.
Separate available offline evidence from genuinely unavailable runtime state
before claiming track completion; the complete ordered backlog remains active.
Default filter decisions are traced, but actual active-shape/filter values
and world state are not captured.
Partial-wheel index maintenance and indexed-slot consumption are now traced;
actual mutation history and physics-body timing remain inputs. Terrain,
dynamic pose and original overlap order remain separate inputs; no full
parity claim follows from resource acquisition or modeled replay.

Pre-existing extractor `Program.cs`, `README.md` and `CollisionMode.cs` changes,
`_tools/content.md` and `graphify-out/` remain outside this continuation. No commit or push was made.

### Shipped shape complexity and damage-location admission

The frozen core constructors `0x2446940` and `0x24677E0` write sentinel
`0xFF` to `DefaultShapeComplexity` at settings `+0x75`, and enable deprecated
`bDefaultHasComplexCollision` at `+0x56`. Derived constructor `0x42E4930`
preserves those values. Core post-initializer `0x246F660` converts the
sentinel to **UseSimpleAndComplex** when the legacy setting is true, or
UseSimpleAsComplex when false; explicit non-sentinel values are preserved.
Derived post-initializer `0x42D30A0` calls it and installs the class default
through the previously unindexed eight-byte setter `0x2470310`.
BodySetup getter `0x246D6E0` uses the settings value only when its own byte at
`+0x31` is zero. SDK offsets and enum values agree with these raw instructions.

`physics-config-audit-v2.json` inventories **220 readable shipped INI files**,
with no assignments to either property. All 35 sampled skeletal package hashes
still match the frozen extraction; the installed executable identifies
CL-516586. `shape-complexity-native-v2.json` passes all three constructor paths,
**512 post-initializer cases and 1,024 BodySetup fallback cases**. Native
derived initialization and the setter run over owned objects; base config
loading, solver defaults, FName creation and class lookup have explicit helper
stand-ins. `shape-complexity-validation-v1.json` binds 19 inputs and classifies
all **121 extracted BodySetups** under the inspected shipped policy: 112
omitted flags resolve to UseSimpleAndComplex, matching nine explicit flags.
Saved/user/command-line/hotfix overrides and active physics shape construction
were not captured. This resolves the shipped default, without establishing
which shapes are active in a running world.

The per-actor location-pointer admission gate at `0x6F06AE6–0x6F06B22`
also passes **4,360 native decisions across 261 sequences**. An existing
non-null location suppresses a later match; null locations pass repeatedly.
The existing viewer matches every retained index and all 2,595 suppressions.
Receipts are `damage-location-gate-native-v1.json` and
`damage-location-gate-portable-validation-v1.json`. These tests supply an
existing list for one actor and symbolic location identities, stopping before
insertion or at the native duplicate skip. Actor-map lookup, location
resolution, insertion/GC barriers, damageability callbacks and downstream
damage are outside this replay. No calculator behavior needed changing.

Core verification still passes 6,864 catalog shots, 62 fresh/out-of-range shots
and 339 routing applications. The first track remains incomplete: continue
with the native damage consumer and its caller boundaries. Runtime world,
activation, mutation history and encounter order remain unavailable inputs;
later ordered tracks remain pending. No game/server process was accessed.

### Native blast falloff precision correction

Raw instructions `0x6F06792–0x6F06837` expose a precision gap in the preview's
otherwise correct piecewise blast formula. Native code reads float32 damage,
radii, distance, falloff and minimum. It rounds `1 - falloff` to float32,
interpolates with doubles, rounds the resulting factor to float32, then
multiplies base damage in float32 before applying the minimum. The preview
now follows those operations. This also preserves native branch priority and
the small-denominator rule; it does not change collision or section routing.

`blast-falloff-native-v2.json` replays the original constant loads and raw
arithmetic on **3,682 finite cases**, including all 22 exported explosive
sources, adjacent float32 boundaries, fractional falloff and narrow/reversed
radii. The corrected preview matches every result exactly, including stored
float bits. Before correction, 1,139 of 2,508 catalog cases differed, by at
most `0.00003598925263759156` damage. Larger synthetic narrow-radius cases
also demonstrated why rounding inputs before branch decisions matters.
The historical module and failed baseline are retained privately.

`_tools/vehicle_blast_falloff_check.js` accepts a private native receipt;
the core checker now includes native expected values near the MAAWS inner
and outer boundaries and for the small-denominator/minimum branches.
`critical-pose-native-query-replay-v2.json` replays both historical and current
calculators using the same recorded native queries. All 20 cases preserve
contact identities/order and first sections. Their maximum main-damage
adjustment is `0.000003923688609575038`.
`critical-pose-falloff-native-v1.json` directly executes native arithmetic for
all **63 retained per-hit base amounts**, matching the current calculator.
Damage modification and health routing remain portable in this integration.

The current full comparison is `native-reference-contact-comparison-v5.json`:
**12,056 cases, 36 scenes, zero unknown slots**. Versus legacy queries it has
864 contact/damage signatures changing and 438 main-damage differences above
0.01. Between the two native-reference pose profiles, 952 signatures change;
the same ten main-damage differences exceed 0.01, with maximum 313.5.
Earlier comparison tables retain their historical arithmetic and hashes.

Core gates pass 6,864 catalog shots, 62 fresh/out-of-range shots and 339 routing
applications. Browser checks pass at 1440px and 360px, including 23 vehicles,
154 routing slots, Gepard transfer, three SPW fronts, 30mm blast, reference
pack import, malformed-file recovery, wheel switching and reset. Screenshots
were skipped for this arithmetic correction; no UI or Sass changes were made.
Link and diff checks pass. Next: continue beyond base amount and admission
into native damage modification and vehicle section consumption. The first
track and the full ordered goal remain active and incomplete.

### Native section routing and health clamp correction

Owned-object replay now executes `0x53205D0` section consumption and
`0x5339DD0` pre/post routing, the native sparse-map lookup/iteration and visit
counter lookup, attribute read/change wrappers `0x52301F0` / `0x52311D0`,
base setters `0x5236AF0` / `0x5236E50`, and health clamp `0x533A750`.
The fixture supplies valid authority/filter services, constant scalable-float
responses, empty section requirements and callback continuation policy.
Its dirty-attribute service mirrors base health to current health, modeling
no active modifiers. Notifications, reference release and bounded-map
initialization are explicit fixture services; destruction and replication
are not executed.

This exposed three preview errors. Routing arithmetic and the health clamp
need float32 rounding. The loop guard counts visits **per section in a shared
pre/post context**, rather than limiting total recursion depth; reaching the
guard aborts that context. Simultaneous routing uses a fresh context and runs
before the depleted-main callback suppresses post routing. A chain through
12 distinct sections can therefore complete, while a pre-route cycle must
abort without applying its remaining damage. Current exported main sections
have no simultaneous routes; that last correction is demonstrated by owned
synthetic configurations, not claimed as a current-profile damage change.

`section-routing-native-v2.json` contains **536 cases / 978 native section
calls**: all 339 fresh current-profile applications plus depleted/fractional
states, threshold amounts, cycles, long chains and routing flags. The previous
calculator differed in 111 cases, including 12 current-profile cases with
maximum health error `0.000024414062522737368`. The corrected calculator
matches every health value, handled amount and ordered health change exactly.
The historical calculator and baseline are retained privately.
`_tools/vehicle_section_routing_check.js` accepts this private receipt;
the core checker also retains focused cycle, long-chain and simultaneous
regressions. Gepard's reviewed front shot now uses native health changes
`267.9000244140625` main and `14.100006103515625` fuel; display rounding stays
the same.

`critical-pose-native-query-replay-v3.json` preserves contact identities/order
and first sections in all 20 critical cases. Its maximum main-damage change
from the previous routing is `0.00004646301272259734`.
`critical-pose-section-routing-native-v1.json` then directly executes all
**46 supplied applications / 82 native section visits** in those sequences.
Every final section health and ordered health change agrees exactly. Incoming
rule-modified amounts and no-modifier attribute state remain supplied inputs.

The current full scene comparison is v6: **12,056 cases, 36 scenes, zero
unknown slots**, 866 legacy/native contact-or-damage changes and 438 main
differences above 0.01. The two native pose profiles have 971 changing
signatures; ten main differences exceed 0.01, still with maximum 313.5.
The 3,682 native falloff cases, core 6,864 catalog shots / 62 additional shots /
339 routing checks and full desktop/mobile browser suite pass. No screenshots
or Sass build were needed for this arithmetic/control correction.

Next: native event conversion and `ModifyDamage` rule evaluation. Current
native routing proof covers the declared owned services, not dynamic attribute
modifiers, requirements, actor lifecycle or captured world state. The first
track and all later ordered work remain incomplete; nothing was committed,
pushed or run against a game/server process.

### Native vehicle rule collection and evaluation

The next replay executes the native collector `0x6BB6A60`, callback/thunk
`0x6BB6A50` / `0x6BB6730`, requirement matcher `0x6BB5D20`, category lookup
`0x6BB8970`, group sort `0x6BB61A0` / `0x6BB5F40`, and evaluator
`0x6BB6FB0`. Registry rows and categories are reconstructed from the existing
exports. Registry discovery and typed-row access, symbolic FName/tag-parent
services and bounded group allocation are supplied. Inputs specify hostile
alignment, an explicit `Meta.Damage` instigator with empty context, empty
target context, the reviewed source context and each slot's hit location.
Runtime registry overrides and extra actor/weapon context are not captured.

> Round 19 re-verification (static-analysis image; virtualized dispatch not removed): in the static-analysis image the whole `0x6BB8970` body (0x6BB8970-0x6BB897E) is a dispatch stub (`mov r9,[rip+x]; jmp [r9-0x9A8]`), so that image cannot confirm the logic; the table base is filled at run time and the slot is not statically resolvable. The older reference image holds the original body: walk the `+0x30` array (count `+0x38`) comparing 8-byte entries to `[rdx]`, return the byte-offset index (`sar 3`) of the first match, else -1. That matches this claim. Verdict: unaffected (supported by the reference image, not by the static-analysis image).

`vehicle-rule-collector-native-v1.json` covers **6,776 source/slot/radius
cases**, representing 4,356 unique native contexts. It performs 19,580
registry-level lookups and 8,668 typed-row checks. Every selected operation
for these blast contexts is `Percentage_Ongoing`; groups contain at most four
entries. A portable ordered float32 fold matches all final amounts and every
`ModificationResults` record, including the record threshold. There are
10,923 arithmetic terms across the full case table.

The viewer's existing combined-factor calculation differs in **1,123 cases**,
by at most `0.000244140625` damage. This is still an open integration gap:
the current viewer has not yet been switched to ordered native operations.
`native-vehicle-rule-recipes-v1.json` prepares **317 compact recipes** covering
all 23 vehicles / 154 slots / 22 sources / both radius tags, in 149,787 bytes.
Each recipe was independently folded against its native result. This private
artifact is hash-bound to the current catalog and is not a published asset.

`vehicle-rule-owned-cases-native-v2.json` adds **33 synthetic cases** for
starting versus ongoing percentages, Add order, source conjunction, hit-tag
parent matching, alignment, empty required tags, target-tag exclusion from
target context, nonempty/empty clamp behavior and tiny-delta recording. It
also verifies missing-category priority and specific-group-before-parent
execution with an example that would differ under a global sort; the root
tag is excluded. Native sorting is exercised with arrays through 64 entries.
Custom operation dispatch remains outside this vehicle-only replay.

Next: integrate the verified ordered recipes into the canonical data export
and viewer, then validate event conversion and subsystem dispatch. The
`0x6EF8DE0` event converter is now captured as an aligned raw span; capture
alone is not execution proof. No calculator/UI behavior changed in this rule
investigation, so prior browser checks were not rerun. The complete ordered
goal remains active and incomplete.

### Ordered rule integration in the canonical export and viewer

The integration gap above is now resolved for the declared vehicle blast
contexts. `python _tools/damage_tables.py --json` generates ordered recipes
from the source registry rows and category asset. The compiler preserves
group order, native short-sort tie behavior, literal float32 amounts and the
nonempty-group clamp. All **6,776 exported source/slot/radius mappings** match the native
collector output exactly. Six additional owned compiler cases verify operation
order and category handling. Selected custom operations or groups above the
verified eight-entry short-sort path stop export explicitly; current blast
groups contain at most four entries.

The catalog stores per-slot recipe IDs and **618 per-vehicle recipes**;
identical recipes are shared within each vehicle. Its size is **1,120,763
bytes**. Canonical regeneration is byte-for-byte repeatable. Removing only
the new recipe fields and two metadata fields reproduces every pre-existing
catalog field exactly. Earlier native receipts remain bound to the archived
pre-integration catalog; the preservation check establishes their input
equivalence for the new export.

`vehicle-impact.js` now evaluates ordered starting/ongoing percentage and Add
deltas in float32. Normal exported vehicle blasts use these recipes, replacing
combined-factor multiplication. A missing recipe in a recipe-bearing vehicle
is an error. The public factor-only vehicle input format remains supported
for external callers and existing synthetic fixtures; displayed factor tables
remain analytic summaries. Inner/Outer selection also compares float32 radii.
`_tools/vehicle_blast_rules_check.js` verifies both recipe contents and actual
browser arithmetic against all **6,776 catalog cases and 33 owned cases**.
The core gate retains native Havoc/72mm values that differ from simple factor
multiplication, plus order, missing-recipe and legacy-format regressions.

`critical-pose-native-query-replay-v4.json` preserves all 20 critical cases'
contact identities/order and first sections. Its maximum main-damage change
from the previous calculation is `0.00006103515625`.
`critical-pose-falloff-native-v2.json` verifies all **63 base amounts**;
`critical-pose-rules-native-v1.json` directly executes native collection and
evaluation for all **63 modified contact amounts**.
`critical-pose-section-routing-native-v2.json` executes the **46 supplied
applications / 82 section calls**, matching every final health value and
ordered health change. These remain owned fixtures with the stated registry,
tag, attribute and continuation services, not a whole game invocation.

The current full comparison is v7: **12,056 cases / 36 scenes**, zero unknown
slots, 865 legacy/native contact-or-damage signature changes and 438 main
differences above 0.01. The two native pose profiles have 967 changing
signatures; ten main differences exceed 0.01, with maximum 313.5.
Core checks pass 6,864 catalog shots, 62 additional shots and 339 routing
applications. The separate 536 native routing and 3,682 falloff cases pass;
the generated cooked-query bundle is current. Desktop/mobile browser checks
pass, including reference-pack import, recovery, wheel switching and reset.
Screenshots and a Sass build were skipped for this arithmetic/data change.

Next: execute the native event conversion and subsystem dispatch boundaries.
Additional runtime context, registry overrides, dynamic attribute modifiers,
actor lifecycle and captured world state remain outside the current proof.
The first track and complete ordered goal remain active and incomplete.

### Native event conversion, activation and dispatch

`damage-event-dispatch-native-v1.json` executes the full `0x6EF8DE0`
converter and `0x6F02EC0` ModifyDamage wrapper: **240 reference/field-copy
cases, eight alignment cases and 72 dispatch cases**, all passing. The
converter resolves missing actors/controllers through pawn links and reads
actor damage entities through the stats component. Explicit target entities
take precedence over actor discovery and bone fallback. Source context and
cause tags survive conversion. Some invalid references remain when no valid
replacement exists; this is not general pointer sanitization. Equal faction
tags yield Friendly, including equal None tags when both player states are
valid but their faction components are absent or invalid.

The shipped config audit reads **220 INI files**, with no unreadable files,
and revalidates 35 frozen skeletal-package identities. It configures one
`WDGlobalDamageSystem` with `bStartActive=True`, the `GlobalDamageData`
registry and the exported category asset. It also supplies the LOS class
lists: skip destruction buildings, ignore mover characters and ignore C4
attach-parent occlusion. This is shipped configuration, without user,
command-line or hotfix overrides.

`damage-activation-critical-native-v1.json` executes the native base/global
constructors, the settings activation loop up to `0x6F02427`, the real
global-system VFT and native active setter/getter. The constructor defaults
to inactive; the settings loop applies each configured start flag. **56
activation/bypass/amount cases pass**, preserving negative-zero bits and
selecting the first active system. Later subsystem initialization is outside
this prefix replay.

All **63 critical contact events** now traverse activation, conversion,
selection, native rule collection/evaluation and ModifyDamage. Final float32
amounts and modification records match the earlier rule-only receipts exactly.
The ten Ural contacts with no explicit hit location execute the populated
native class-mapper miss path. The shipped map contains BHMoverPawn and
WDTargetDummy; Ural's exported implementation is WDWheeledVehiclePawn, whose
SDK ancestry reaches APawn through ModularVehicle and excludes both mapped
classes. Owned class metadata reproduces this ancestry; both entries are
visited and None is returned. This does not exercise a successful bone-map
lookup.

UObject allocation, class/component discovery, tag/registry services, GC
barriers and delegate observation remain supplied fixture services. This
closes the declared event/dispatch boundary, not whole gameplay execution or
captured-world parity. No viewer code changed during this checkpoint; prior
UI/arithmetic checks were not repeated. Next: radial event construction and
the vehicle target-interface handoff, followed by a first-track completion
audit. The ordered goal remains active; tracks two through five are pending.

### Radial event constructor and caller window

`radial-event-caller-native-v1.json` extends all **63 critical contacts**
through the native radial caller window `0x6F06B2F`–`0x6F06BD1`. This
executes the actor/controller pair constructors, event constructor
`0x6BB4D30`, hit-result and actor-instance-handle copies, target acceptance,
the no-op pre-damage hook and ModifyDamage. Final float32 amounts and every
modification record remain exact. The event initially carries the instigator
controller and target actor; conversion recovers the instigator pawn and its
damage entity. The constructor leaves modification results empty, and an
owned allocation service supplies storage when native evaluation requests it.

Another **32 cases** cover all two-tag acceptance-query answers, positive,
nonpositive and negative-zero amounts, and both GC-barrier states. Rejected
events stop at `0x6F06CC5` without calling the pre-hook or ModifyDamage.
Eight standalone constructor cases copy nontrivial hit fields and source
context/cause tags, preserve amount bits and leave both buffer canaries intact.
Hit padding and unused flag bits are not treated as semantic fields.

The replay uses one native vehicle interface table at `0xB668BE8`, whose
`+0x18` pre-hook is the native no-op `0x1562FE0` and whose `+0x30`
acceptance method is `0x76B63E0`. This does not establish per-vehicle runtime
interface identity. Acceptance tag-query answers use owned symbolic tag
identities; their real tag labels have not been recovered here. Upstream
gathering, source/radius context assembly, final damage-context construction
and ReceiveDamage remain outside this caller-window proof. The first track
remains incomplete. No product code changed and prior UI tests were not rerun.

### Native hit-location lookup and safe-zone acceptance

`vehicle-hit-location-native-v1.json` verifies all **154 exported vehicle
slots** and **22 owned lookup cases**. The replay executes `0x6B80230`,
the complex-zone wrapper `0x5338730`, group inheritance/default lookup
`0x53952A0`, native slot/section maps and `0x395D3C0` tag matching. Complex
surface hit resolution supplies the group/slot pair. Tag-manager node
acquisition, parent metadata, locks and reference release are owned services;
the comparisons, iteration and first-match decisions execute natively.

Current-group defaults precede parent-slot lookup. An explicit slot mapping
to None, an absent section or a section without matching tags ends the lookup;
it does not resume the parent search. The group root participates in parent
lookup. The first section tag matching `Meta.Damage.HitLocation` wins,
including that exact root tag. This last case exposed a one-line exporter
discrepancy: `_tools/damage_tables.py` previously accepted descendants only.
It now accepts the root too. The native-backed regression gate passes **154
catalog comparisons and six compiler boundaries** and rejects the archived
implementation specifically at the root-tag case. Canonical regeneration
leaves the shipped catalog **byte-for-byte unchanged**. Runtime registration
of unknown tags remains outside the static compiler's contract.

`vehicle-acceptance-tags-native-v1.json` executes two static initializers and
the native tag-store prefix, recovering globals `0xD36B8E8` =
`State.Location.SafeZone` and `0xD36B8F0` =
`State.Location.SafeZone.Hostile`. It stops before engine tag/delegate
registration. `vehicle-gate-caller-native-v1.json` replaces the preceding
boolean query service with the actual vehicle query VFT, `0x53CB980` and
`0x5230BE0`, over an owned cached tag container and parent cache.

> **Round 19 re-verification.** Evidence level: static-analysis image; virtualized dispatch not removed. Function `0x5230BE0` begins with a protection-layer dispatch stub in the static-analysis image (`mov reg,[rip+x]` then `jmp [reg+disp]` through a runtime-filled global table, so its target is not statically resolvable); the older reference image holds the plain body, and it null-checks the tag, then searches the explicit array (`+0x4E8`/`+0x4F0`) and the cached parent array (`+0x4F8`/`+0x500`), matching the description. Classification: unaffected by the stub.

The native acceptance rule is **outside SafeZone or inside SafeZone.Hostile**.
Friendly safe-zone descendants are rejected; hostile descendants are
accepted. A missing or garbage-marked tag owner returns false to the safe-zone
query and therefore accepts at this gate. All **72 state/amount/GC cases**
pass, and all **63 critical caller-window contacts** still match exact amounts
and modification records. Cache population/updates, the actual world state
and per-class runtime interface identity remain unverified. Final damage
context dispatch and ReceiveDamage are still open, so track one remains
incomplete. No browser rerun was needed for the compiler correction because
the generated catalog and browser code are unchanged.

### Native damage-context dispatch through vehicle health

New direct-control-flow captures recover the tails omitted by several corpus
and unwind bounds: event assignment `0x69E6ED0` is **660 bytes**,
ApplyWDDamage `0x6B7FE50` is **521**, interface dispatch `0x6C2A5F0` is
**416**, and subsystem handoff `0x6EF9840` is **1,642**. The section outer
application `0x5320400` is **455 bytes**, rather than the earlier partial
148-byte capture. Historical captures remain intact. The new capture walks
direct branches to returns or declared external tail jumps; execution guards
reject instructions outside the captured reachable set. This does not imply
the underlying corpus has been repaired.

`full-vehicle-handoff-native-v1.json` connects native code in **one owned
emulator**: the post-gather radial event caller and rules, FWDDamageContext
construction and event assignment, subsystem handoff, native interface fallback,
vehicle receiver `0x76B7E80`, ApplyWDDamage, outer section selection/application
and the existing native section/attribute routing. All **20 critical sequences,
46 applications and 82 section calls** match the prior final health, ordered
changes and handled amounts exactly. The same owned target actor and health
component persist through each sequence. Modification-result arrays are copied
into separate storage, buffer canaries survive, and the temporary component
damage-cause field is restored after application.

Eight additional cases exercise negative, zero, negative-zero, threshold and
ordinary positive amounts. Last-damage cause updates only after a positive
handled amount. A tiny amount can pass the outer `1e-8` gate while producing
zero health change; direct native section replay confirms that result. The
test initially assumed such an amount would necessarily change health, then
replaced that assumption with the independent native section oracle.

World/GameState/class/interface/reflection services, authoritative owner flags,
first-section complex-zone resolution, array allocation and no-modifier
attribute services remain supplied. The fixture selects native interface
fallback, disables the game-state damage-disable flag and skips telemetry.
Pre-damage notifications and actor destruction/continuation are observed or
modeled services. CurrentDamage transfer and attachment of the radial typed
struct to the constructed context are explicit bridges; the complete radial
caller is not executed across those bridges. Blueprint overrides, dynamic
modifiers, replication and actual world/lifecycle effects remain unproven.

`vehicle-receive-table-inventory-v1.json` binds **six static interface tables**
containing **five receiver thunks** that tail-call `0x6B7FE50`.
`vehicle-receivers-native-v1.json` executes all six tables through the native
health handoff in **24 valid/missing/garbage/wrong-type component cases**.
The `0x76B3C90` thunk tests presence and the garbage flag but lacks the type
check used by the other four thunks; compatible owned wrong-type memory
therefore reaches application in that case. This is a code-path distinction,
not a runtime vulnerability claim. Vehicle-class attribution and runtime
installation of these tables have not been established.

Next: audit the remaining first-track boundaries, including class/table
attribution, whole radial context assembly and the other collision/contact
callers. Track one remains incomplete; tracks two through five remain pending
in their original order. No calculator data or JavaScript changed in this
checkpoint, so prior UI/arithmetic gates were not repeated.

### Numbered material slots and native collision damage

The first-track audit preserves the original collision/contact/explosion
objective and separates completed native fixtures, remaining caller integration
and unavailable runtime inputs. The private restart artifact is
`FIRST_TRACK_AUDIT_v1.md`; it explicitly leaves the first track incomplete.

`numbered-material-slot-audit-v1.json` closes pipeline question V-9 for the
frozen authored assets. All **276 registered static component/state rows**
resolve to **217 own/collision meshes**. No literal numbered material slot
matches either indexed-wheel base, `CC_Wheel` or `CC_Tyre`. Other numbered
material names exist and are retained in the receipt. This establishes asset
names, not runtime mesh overrides or active-state participation.

`collision-damage-caller-native-v1.json` executes the complete
`0x76740F0` collision damage caller, `0x6EF9450` point-event construction,
native context copy, typed point-event allocation/copy, dispatch, vehicle
receiver and shared health path. **552 cases across all 23 current target
tags** match independent native rule and baseline health results: tracked,
wheeled and empty source tags; driver presence; both GC-barrier states; and
100 or negative-zero starting damage. Source context and cause survive,
Impact is appended, and an empty source root becomes Landscape. The exact
native tag initializer/store dataflow is retained separately.

For the applicable stationary row, the replay confirms **100 + 1000 = 1100**
when a tracked source matches the Add rule. It also verifies modification
records after context copy, native point-type tests, shot-direction
normalization, final health/handled amounts and last-cause behavior. Unlike
the earlier radial handoff fixture, this collision caller constructs and
attaches its typed event without a manual context bridge.

Incoming collision magnitude and hit/zone resolution remain supplied.
World/subsystem and actor-component lookups, the unchanged controller
override, disabled cause-override predicate, default damage-type resolution,
allocation/typed cleanup and the previously declared baseline attribute and
lifecycle services remain owned fixture services. Actual class installation,
world physics and runtime effects are not proven. Upstream magnitude helper
`0x7671DA0` and contact/admission callers `0x76736C0` / `0x767E640` are now
captured by direct control flow; capture alone is not execution evidence.
Those boundaries and complete radial context assembly are next. The ordered
goal remains active. No calculator or browser code changed here.

### Complete radial caller assembly after owned gathering

`full-radial-caller-native-v2.json` executes `0x6F06540` from entry to return
after an owned one-actor gather. It now runs the native per-component filter
`0x6C2A790`, falloff and source/radius context assembly, repeated-location
admission, event construction, CurrentDamage transfer, typed radial-event
attachment, deep hit-array copy, dispatch, baseline section health and cleanup.
The manual context bridges in the earlier radial handoff fixture are no longer
needed on this path. All **20 critical scenes / 63 contacts / 46 applications**
match exact amounts, modification records, handled amounts, final health and
ordered health changes.

**24 owned cases** cover repeated components, repeated nonempty tags, empty
hit locations, empty gathers/hit lists, safe zones, damageability, roles and GC
branches. Component duplicates use native last-entry swaps; the copied typed
event retains the resulting whole hit array. Different components sharing a
nonempty location produce one admitted event, while empty locations remain
separate. These cases preserve the first-hit section selection used by the
native vehicle health path.

The first receipt's label for actor byte `+0x62`, bit 3 was wrong: that flag is
`bCanBeDamaged`, not authority. V1 bytes and source are preserved; V2 corrects
the label and adds separate Role `+0x170` tests. With `bCanBeDamaged=false`,
the radial caller skips the actor before filtering. Under supplied roles
0, 1 or 2, an otherwise eligible event reaches dispatch but native health
application handles zero and writes no health. Role 3 supplies the baseline
critical cases. This verifies code paths under supplied state, not actual
server behavior.

World gathering/encounter order, actor/weak-object resolution, set/map and
array allocation, hit-location/zone resolution, reflection/class services,
notifications, typed cleanup and baseline no-modifier/lifecycle services
remain supplied. The set/map service allocates and links storage; native
hashing, comparison, filtering, tag admission and caller iteration execute in
the emulator. Actual world state and cross-actor gather identity remain
outside this proof.

`collision-magnitude-native-v1.json` additionally executes the full
`0x7671DA0` magnitude helper in **384 finite cases**. It verifies the double
vector norm times `0.036`, conversion to float32, missing-curve return,
conditional `0.1` floor, negated-depth and speed threshold branches, and
float32 scaling order. Curve resolution/evaluation remain supplied; real
curve assets and population of component offsets `0x5F8`–`0x608` are not yet
verified. Those fields retain offset labels rather than guessed gameplay
names.

The private completion matrix is updated as `FIRST_TRACK_AUDIT_v2.md`.
Next: collision curve/settings provenance and native contact admission at
`0x76736C0` / `0x767E640`, then remaining class/caller boundaries. First-track
completion remains unproven; later tracks remain pending in order. Calculator
code/data are unchanged, so UI/arithmetic checks were not repeated.


### Shipped collision curves and omitted native defaults

`shipped-collision-curves-native-v1.json` executes the native settings and
data-asset constructors, runtime external/inline curve lookup, rich-curve
evaluator and unweighted interpolation, followed by the full collision
magnitude helper. **23 settings assets / 38 curves cover all 33 variants** by
authored reference reachability. **534 curve samples and 3,312 magnitude checks
pass**, including serialized keys, constant bounds and exact float32 composition.
There is no supplied curve-value callback. This compares native standalone
curve evaluation with native magnitude composition; it is not an independent
cubic oracle or a live-game comparison.

All 23 assets omit the relevant scalar properties. Native constructor defaults
are HighSpeedThreshold 30, bCrushDamageAtHighSpeed true, SpeedCrushFactor
float32(0.8), CrushPenetrationThreshold 20, CrushDamageMultiplier 1000 and
VehicleDamageCooldownTimer 0.5. SDK layout now binds these names to component
fields +0x5F8 through +0x60C. Empty inline curves use the native MAX_FLT default
sentinel and return the caller default. All 38 exported curves are unweighted.
The native rich-curve VFT points to the executed evaluator at slot 17.

A fresh read-only CUE4Parse export from the installed PAKs matches the exact
DamageEntitySettings / FloatCurve properties for all **61 packages**. All
**35** previously frozen skeletal-package identities also match. This binds
the data to the same installed asset set; it does not capture live overrides.
Serialized property overlay, base/unrelated targeting-constructor services,
native gameplay configuration copy/precedence and runtime loading remain
supplied or unverified. Component construction and contact callbacks are not
established by this receipt.

A second label correction applies to the radial fixture: `event_face` and
`typed_hit_faces` were owned opaque IDs stored in **FHitResult.MyItem +0xA4**,
not FaceIndex +0. `full-radial-hit-id-label-correction-v1.json` renames those
fields to `event_my_item` / `typed_hit_my_items`. The original receipt remains
preserved, and reversing all 144 label instances reproduces it exactly.
Filtering, order, hit-copy and numeric results are unchanged. This correction
is derived evidence, not another native execution.

`shipped-curves-checkpoint-validation-v1.json` binds the frozen EXE, native CFG
and constant bytes, producer/fixture identities, SDK/source inputs, fresh PAK
exports and the reversible label correction. `FIRST_TRACK_AUDIT_v3.md` records
the remaining first-track boundaries. Next: native contact admission at
0x76736C0 / 0x767E640, configuration precedence and class/caller attribution.
Track one remains incomplete; tracks two through five remain pending in order.
Calculator code/data are unchanged, so UI/arithmetic checks were not repeated.


### Native contact admission and mesh-hit vector derivation

`contact-admission-native-v2.json` executes the complete native 0x76736C0
helper with the shipped settings and native curve evaluator. **1,242 catalog
cases pass, with 894 forwarding positive amounts**, plus **17 boundary cases**.
Null/garbage targets, non-authority owner roles, missing class/interface,
existing cooldown and selected secondary-set/seat-list conditions suppress
contacts before magnitude evaluation. An admitted positive amount inserts a
cooldown entry and requests a non-looping **0.5-second** timer. The damage caller
receives the other actor as target and the owner as both source and instigator.
The final damage caller is supplied on this receipt; it has separate native
execution evidence and is not yet joined here.

Native class-registration arguments bind 0x53CAB60 to BHBaseVehiclePawn,
0x527B100 to BHMoverPawn and 0x6E65DE0 to WDMoverCharacter. The helper selects
component curve +0x460 for vehicle ancestry, +0x570 for mover-pawn ancestry,
and +0x4E8 otherwise. Only the mover-pawn branch requests crush scaling.
The native +0x758 getter executes and the SDK identifies VehicleSeatComponent;
the related-actor list acquisition remains supplied. V1 fixtures used misleading
`driver` object labels. V2 corrects those labels, executes the seat getter and
retains every prior numeric result; both versions remain preserved.

`mesh-hit-contact-native-v2.json` runs selected complete entry/return paths of
0x767E640 through vector derivation and the actual contact helper: **276 catalog
cases and 266 boundary cases pass**, with **536 contact-helper calls**. It tests
the owner velocity squared, converted to float32, against 100; values at or
below the threshold return before contact handling. WDMoverCharacter targets
also return early. Valid movable primitives that pass the supplied simulation
query contribute their supplied float32 mass. When their float32 mass sum is
at least 1, native code divides the impulse by that sum in double precision;
otherwise it keeps the impulse. The resulting vector drives actual native
curve/magnitude/contact handling.

These mesh-hit paths end naturally at a supplied positive duplicate-cache
gate after contact handling. Later self-damage, effects and propagation branches
remain unexecuted. Owner velocity, virtual physics queries/masses, reflection,
weak-object creation, set storage/lookup/removal, related-actor acquisition,
timer manager/scheduling, allocation and final damage dispatch remain supplied.
No actual world physics, cache lifecycle or server behavior is established.
`contact-admission-checkpoint-validation-v1.json` binds both current receipts,
the seat getter, static class names, native CFG/constants and their input chain.
`FIRST_TRACK_AUDIT_v4.md` keeps the whole first-track objective open. Next work
is later mesh-hit branches, native configuration copy/precedence and remaining
class/caller boundaries. Tracks two through five remain pending in order.
No calculator code/data changed; no UI/arithmetic rerun or push was performed.


### Native gameplay-config copy joined to contact handling

`gameplay-config-copy-native-v2.json` executes complete entry/return paths of
0x767BC40 with an owned vehicle owner at Role 0 and explicit setup services.
**46 shipped-settings cases and eight boundary/override cases pass**, including
**235 native runtime-curve copies** through 0x36269E0. Native code selects the
supplied candidate, writes GameplayConfig +0xF0, and transfers the damage tag,
all five curves and the six collision scalar fields into DamageEntitySettings
+0x3D0. The source data asset is populated by the fixture from verified native
defaults and shipped serialized collision properties. Unrelated source settings
remain at their native defaults.

A missing/garbage container preserves the earlier config pointer; a missing or
incompatible candidate clears it. A garbage candidate is assigned to +0xF0 but
its settings are not copied. Missing/garbage owners return before selection.
Owned non-default scalar values also copy exactly, so this behavior does not
rely on constructor values coincidentally matching in both objects. Both GC
flag states are covered with supplied barriers.

`config-contact-joined-native-v1.json` then runs native contact handling in
the same emulator state after each of **23 native configuration copies**.
All **1,242 contacts / 894 positive forwards** match the separate contact
receipt exactly in amount, curve choice, admission and timer requests. There
are no component damage-settings writes between native BeginPlay and native
contact handling. The fixture changes the supplied owner Role from 0 to 3
before contact handling; this does not establish authority BeginPlay behavior.
A null cached world pointer takes the native fallback lookup, whose result is
supplied, before scheduling a timer.

Contact receipt V3 corrects an aliasing bug in trace recording: later standalone
oracle evaluations could append to an earlier case's `curve_samples` list.
`contact-admission-native-v3.json` snapshots that list and proves exactly one
native curve sample per catalog contact. V1/V2 remain preserved; every amount,
curve selection, admission and timer result is unchanged. V3 is the current
contact receipt. Mesh-hit V2 results do not retain that sample list and are
unaffected. The correction changes fixture trace storage, not native code.

The native settings copy is now executed and joined. Module/asset acquisition,
class compatibility, source property deserialization, delegate/setup services,
optional components/subsystems, unrelated targeting/final continuations,
engine storage/timers and final damage dispatch remain supplied. Actual module
assembly/loading precedence, authority setup, complete BeginPlay effects and
later mesh-hit effects/self-damage/propagation remain unverified.
`config-contact-checkpoint-validation-v1.json` binds these results and verifies
that the V3 correction leaves prior numeric outcomes unchanged.
`FIRST_TRACK_AUDIT_v5.md` and `RESUME_CHECKPOINT_v32.md` preserve the next work.
Track one is still incomplete; tracks two through five remain pending in order.
No calculator changes, UI/arithmetic rerun, live access, commit or push occurred.


### Native settings/contact and mesh-hit joined through health (checkpoint v33)

`config-contact-damage-joined-native-v2.json` joins native BeginPlay collision
settings copy, contact admission, magnitude and curves to the complete native
0x76740F0 damage caller, point event/context construction, rule evaluation,
interface dispatch, baseline section health, cleanup and cooldown scheduling
in **one emulator and allocator**. **1,242 settings/contact cases, 414 cases
across all 23 catalog vehicle rows (22 distinct damage tags), and four suppression cases pass**, producing
**1,308 applications** checked against separate native rule/health runs.
Tracked, wheeled and empty source tags, both GC flag states and all three
contact-class branches are included. Health clipping is checked natively.

`config-mesh-damage-joined-native-v1.json` additionally connects the native
mesh-hit vector derivation to that damage path after native settings copy.
Its **276 catalog and 266 boundary cases pass**, with **479 applications**.
Vector, virtual-query selection, curve, incoming amount and timer results
match the isolated mesh/contact receipt. Component damage settings remain
unchanged between native setup and the mesh-hit callback.

There is no manual event/context/amount bridge on either joined path. Shared
engine-service PE code/global images switch at native caller boundaries;
fixture heap, call arguments and contexts are not copied at those switches.
Unicorn translation-cache flushing is required after these switches: without
it, an earlier translated stub can survive a byte restoration. The successful
fixtures flush the cache. `joined-service-image-code-audit-v1.json` separately
checks **57 protected native spans** against the frozen code across both
images and the return transition.

Source property population, module/class lookup, Role-0 setup followed by
supplied Role-3 contacts, reflection, hit/zone resolution, physics state and
virtual queries/masses, weak objects, set/cache/timer/allocation/typed cleanup,
and baseline no-modifier/lifecycle services remain supplied. The mesh callback
still returns naturally at a supplied positive duplicate-cache gate after the
contact path. Later self-damage/effects/propagation, actual cache semantics,
module loading precedence, authority setup and runtime class/world installation
remain open. The separate native final-damage-caller boundary is now joined;
this does not close those other boundaries.

`config-damage-joined-checkpoint-validation-v1.json`, `FIRST_TRACK_AUDIT_v6.md`
and `RESUME_CHECKPOINT_v33.md` bind the results and next work. Track one remains
incomplete; tracks two through five remain queued in order. No product code
changed, so UI checks were not repeated. No live access, commit or push occurred.


### Native mesh duplicate cache and component selection (checkpoint v34)

`mesh-duplicate-cache-native-v1.json` executes the native 273-byte key hash,
set lookup/insertion, weak-handle equality/validity and the expiry callback's
full hash unlink plus sparse-slot release. **1,024 uint32 hash-model cases,
54 weak-handle cases and 74 cache operations pass**. Owned chunked object slots
exercise index, serial and packed flag checks. Forced hash chains cover
duplicate insertion, deletion and free-slot reuse with four inline buckets or
64 external buckets. The key is an ordered pair of weak handles plus
**FHitResult.Item +0xA8**. This differs from the earlier radial fixture's opaque
IDs stored in MyItem +0xA4.

Sparse removal alone is not full set deletion: it leaves hash-chain links
behind. The actual expiry wrapper at 0x7677E80 enters 0x766C4B0, which unlinks
the hash chain before sparse release. The mesh callback constructs the matching
delegate VFT; slot 11 points to that wrapper. This executes native expiry logic
under owned invocation, not elapsed-time scheduling or timer-manager behavior.
Storage is preallocated for 32 elements; allocation/growth/rehash paths remain
unexecuted and memmove is supplied.

`mesh-native-cache-joined-v1.json` removes the supplied duplicate-gate result
from the shared settings/mesh/contact/damage/health fixture. **276 catalog and
266 boundary cases retain exact damage, health, vector and timer results**,
and **six seeded cache cases pass**, totaling **485 applications**. Native
hash/lookup now runs in the mesh callback. On misses, native 0x76696D0 selects
the damage-model class through its cached native getter; the optional virtual
component lookup is supplied as null and the callback returns naturally.
An exact cache hit skips that later selection. Changed Item, reversed handles
and a deliberately colliding valid handle miss; native expiry makes an exact
key eligible for selection again. Contact damage occurs before this gate, so
those cache choices do not undo the preceding contact damage.

Native registration arguments identify the requested class as
WDVehicleDamageModelComponent, bound by `contact-class-labels-v2.json`.
Its virtual receiver at 0x6B7FCD0 is now captured as 321 bytes despite the
corpus row having failed. Capture alone is not receiver execution or corpus
repair. Non-null receiver behavior, later own-damage/effects/secondary paths,
callback-driven cache insertion and actual timer execution remain next work.
Object/class tables, component discovery, property/setup/physics/reflection,
hit/engine/lifecycle services retain their declared owned boundaries.

`mesh-cache-checkpoint-validation-v1.json`, `FIRST_TRACK_AUDIT_v7.md` and
`RESUME_CHECKPOINT_v34.md` bind these results. Track one remains incomplete;
tracks two through five remain queued in order. No product code changed,
UI checks were not repeated, and no live access, commit or push occurred.


### Native WD collision receiver and constructor attribution (checkpoint v35)

`own-collision-receiver-native-v1.json` executes the recovered 321-byte
0x6B7FCD0 WD receiver, the 1,621-byte base 0x531FC20 receiver and native
0x53205D0 baseline section health. **720 finite cases and five owned boundary
cases pass**, checked against **17 separate native health oracles**. Inputs
cover negative/zero/epsilon/ordinary/clipped amounts, double factors followed
by float32 conversion, owner roles, damageability and stats/inventory branches.
The receiver is invoked directly; it is not yet the non-null component returned
to the mesh callback.

Native base code clamps the incoming float amount at zero, multiplies by the
native double attribute result and converts to float32 before its epsilon
check. Its Role-3, bCanBeDamaged and supplied enable predicate gates control
entry to section health. The WD wrapper optionally changes the temporary
`+0x2B8` cause through supplied stats/interface discovery and an inventory-cause
result, then restores the prior cause in every case. Positive handled damage
and vehicle ancestry control its notification call. A supplied garbage owner
with an accepting base enable predicate can still reach that notification;
the wrapper's cause-override garbage check is not a general notification gate.
This describes owned branch inputs, not actual object-lifetime behavior.

The native 187-byte WD object constructor also executes with its base constructor
and final lifecycle helper supplied. Guard canaries are preserved. It installs
primary VFT `0xB30DFF8`; the actual native pointer at `+0x500` (`0xB30E4F8`)
points to `0x6B7FCD0`. This strengthens receiver/table attribution beyond corpus
aliases. The class initializer at `0x6B80930` is distinct from the object
constructor at `0x6B7FB50`.

Surface resolution is supplied as a fallback to the main health section;
class/stats/inventory lookup, enable predicate, optional operator discovery,
attribute/requirement services, notifications and lifecycle remain supplied.
Owner non-null is an input precondition. Actual runtime class installation,
all surface-routing branches, non-null mesh integration and later mesh effects
remain unverified. No corpus row was rewritten: a failed decompiler row has
usable captured/executed native code, which is a different result.

`own-receiver-checkpoint-validation-v1.json`, `FIRST_TRACK_AUDIT_v8.md` and
`RESUME_CHECKPOINT_v35.md` bind this checkpoint. Next: return an owned non-null
model component to the mesh callback, execute the own-vehicle and rotation
curve paths into this receiver, then later effects/cache/timer boundaries.
Track one remains incomplete; tracks two through five remain queued. No product
code changed, UI checks were not repeated, and no live access or push occurred.


### Non-null mesh collision receiver joined (checkpoint v36)

`nonnull-mesh-receiver-native-v1.json` joins native settings copy, the mesh
callback, target contact/point/rules/health, and the separate owner's collision
curve/receiver/health path in one emulator. **621 catalog cases and four
boundary cases pass** across 23 settings assets, three contact classes, three
owner velocities and three impact normals. They include **622 owner receiver
calls, 177 positive owner-health changes and 495 target applications**, checked
against 37 separate native owner-health results. Target health/events remain
identical to the previously validated contact path while owner results vary
with the impact-normal projection.

Native code projects the owner velocity onto Hit.ImpactNormal, takes the
projected vector norm, multiplies by 0.036 and converts to float32 for
VehicleCollisionCurve at component +0x3D8. The selected ray-miss/no-secondary
branch supplies native multipliers of one; float32 composition agrees exactly
with the amount received by 0x6B7FCD0. Its base receiver and section health run
natively, with a separate owner model and health state. No gameplay event,
context or amount is rebuilt between these paths.

The callback now reaches native duplicate insertion and constructs its actual
64-byte expiry closure. Native 0x158B640 also builds populated three/four-unit
(48/64-byte) delegate descriptors; the low-level allocator and timer service
remain supplied. The service records and consumes the descriptor, not elapsed
time. Earlier fixture versions supplied allocation storage without populating
that descriptor; their timer calls established request arguments, not complete
delegate assembly. The current replay includes the populated descriptor.

A native repeat/expiry sequence uses the **actual constructed closure**, with
its full native VFT mapped. An exact repeated key skips owner damage after the
already-tested target contact. Invoking the closure through VFT +0x58 runs
native hash unlink/expiry; a following callback applies owner damage again.
The contact cooldown lookup is deliberately reset by the owned fixture between
calls, so this does not establish cumulative real-time cooldown behavior.
Health baselines are also reset between independent observations.

`nonnull-service-image-audit-v2.json` checks 22 protected native spans/data
across upstream, owner-receiver and return service images. Version 1 of that
image audit and its fixture remain preserved; V2 maps the whole expiry VFT
needed for the real indirect closure call. PE service-image switching flushes
Unicorn's translation cache and leaves gameplay heap/context state intact.

This path supplies a ray miss, nonmatching secondary class, base-vehicle
callback/filter results, physics/virtual state, source property/setup and
reflection/component discovery, attributes/notifications/lifecycle, allocation
and timer-manager services. Ray-hit/rotation, matching secondary propagation,
base effects, allocator growth, actual timing/world/authority and runtime class
installation remain open. `nonnull-mesh-checkpoint-validation-v1.json`,
`FIRST_TRACK_AUDIT_v9.md` and `RESUME_CHECKPOINT_v36.md` bind the checkpoint.
Track one remains incomplete; tracks two through five stay queued. No product
code changed, UI checks were not repeated, and no live access or push occurred.


### Native ray-hit rotation multiplier joined (checkpoint v37)

`mesh-rotation-native-v1.json` executes the selected ray-hit branch through
native root up-vector calculation, between-vector quaternion, quaternion-to-
rotator conversion, axis normalization and the actual rotation curve, followed
by the already-native owner receiver/health/cache/timer-descriptor path.
**621 catalog cases and two ray/root boundaries pass**: 23 settings assets and
27 orientations, including pitch/roll tilts, quarter turns, opposite up vectors,
rotated roots, a diagonal normal and mixed gimbal lock. There are **299 positive
owner-health changes and 434 target applications**, with **61 separate native
owner-health results**. Target health/events stay unchanged across orientations.

The caller normalizes each angle to its signed axis range and evaluates
RotationDamageMultiplier at component +0x648 using **abs(Pitch) + abs(Roll)**,
converted to float32. Yaw is excluded. The default curve value is one, including
empty inline curves. Native up vectors and quaternion mapping agree with a
unit-quaternion model; native Euler output agrees with an independent branch
model, including the singularity cases. Curve input and final float32 amount
composition agree exactly. For an identity owner and a ground normal tilted
30 degrees, the shipped example multiplier is approximately 1.35.

Ray result/normal and owner transform are owned inputs. Native helpers execute
around three supplied numeric library boundaries: atan2, fmod and asin use
Python math callbacks. Their PE import thunks are verified against the frozen
CRT import directory. This does not prove those library implementations or an
actual world trace. `rotation-service-image-audit-v1.json` checks 16 protected
native spans across upstream/owner/return service images.

`demolition-multiplier-static-labels-v1.json` identifies the next branch from
native registration arguments: BHDemolitionCellRepresentation,
InstancedStaticMeshComponent and BHDemolitionDataFragment_VehicleDamage.
The captured caller selects a matching fragment and uses its first float as
the XMM9 collision multiplier. The earlier generic description as a secondary
propagation branch was too broad; this is a demolition data-fragment multiplier
path. Its matching branch/query and authored data remain unexecuted/unbound.

Actual trace traversal, demolition-fragment/query behavior, base-vehicle
filter/effects, allocation growth, timer scheduling, module loading, authority,
class installation and runtime world/lifecycle state remain open.
`rotation-mesh-checkpoint-validation-v1.json`, `FIRST_TRACK_AUDIT_v10.md` and
`RESUME_CHECKPOINT_v37.md` bind the checkpoint. Track one remains incomplete;
tracks two through five remain queued. No product code changed, UI checks were
not repeated, and no live access, commit or push occurred.


### Checkpoint v38: native demolition lookup and typed fragment multiplier

The selected native 52FD760 read-only query now executes with its membership,
component-to-ID and ID-to-asset map lookups. The native 767E640 caller selects
the first matching VehicleDamage fragment (including derived types), composes
the multiplier and reaches native owner health in the same emulator.

Fresh PAK headers recover the dynamic FInstancedStruct types that ordinary
JSON exports omit: 39 VehicleImpulse fragments and four VehicleDamage fragments
across the 39 currently exported demolition assets. The mapping identifies
these as sibling types. RestitutionImpulseMultiplier is not a damage multiplier.
The four DamageMultiplier values are zero; 35 assets have no matching fragment.
For these lists, successful query/predicate selection yields multiplier zero;
query rejection falls back to one. These are conditional outcomes: every asset
references a ruleset and the ruleset predicate is still a supplied callback.

mesh-demolition-native-v1.json covers 23 settings x39 assets x2 predicate
outcomes (1,794 cases), plus25 owned guard/type/order/scalar cases. Separate
native owner-health results verify final amounts; target health/events remain
unchanged across asset/predicate choices. demolition-service-image-audit-v1.json
checks30 protected native spans across upstream/owner/return images.

World, class installation, representation maps, source loading, physics,
allocation/timing and engine services remain supplied. The read-only query
skips demolition mutation. Actual ruleset eligibility is next: authoring
reference closure finds19 packages, not yet freshly compared or executed.
Native base effects/filtering, growth/rehash, other caller integration and
runtime world/lifecycle boundaries also remain open. Track one is incomplete;
tracks two through five remain queued. No product code changed, UI checks were
not repeated, and no live access, commit or push occurred.

demolition-mesh-checkpoint-validation-v1.json binds this evidence closure;
FIRST_TRACK_AUDIT_v11.md and RESUME_CHECKPOINT_v38.md preserve the next work.


### Checkpoint v39: native vehicle-context demolition rules

Fresh installed PAK exports match all66 objects in19 referenced rule packages
by export index, name, type and properties. Native Or/Ruleset/Vehicle predicates,
class casts, cached class getters, actor variant getter and tag-container match
now execute in a separate owned vehicle-context fixture. Native explosion and
buildable predicates execute their missing-context rejection paths.

`demolition-rules-native-v1.json` passes2,574 catalog cases:39 demolition assets
x33 authored variant tags x2 supplied contact flags.1,254 permit and1,320 reject;
11 additional actor/class/variant/tag/cycle guard cases pass. The native match
checks the input tag against permitted explicit and parent entries. Parent
container construction and tag identities remain supplied. Do not infer a
standard tag direction from the names alone. Both authored contact bits are
true; individual-bit meaning is not established by this catalog replay.

The prior mesh demolition lookup/multiplier receipt still uses a supplied
predicate outcome. Joining actual rules into that same emulator is next.
Positive explosion/buildable context paths, class/variant installation,
property loading, actual world participation, growth and lifecycle remain
separate boundaries. No complete-track or live-parity claim is made.
`demolition-rules-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v12.md and
RESUME_CHECKPOINT_v39.md bind this increment. Track1 remains incomplete;2-5
remain queued in order. No product code, live access, commit or push.


### Checkpoint v40: native rules-to-damage join and positive metadata graphs

`rules-mesh-native-v2.json` joins actual authored native rules to the52FD760
query,767E640 typed fragment multiplier and native owner health in one emulator.
It passes3,003 catalog cases:39assets x33variant tags at one configuration, plus
22other configurations x39assets xone permitting/one rejecting variant. This is
not the full23x39x33matrix.1,485permit,1,518reject;1,050cases change owner health.
Seven independent native owner-health results check final amounts. Native
configuration copies and target health/events match the frozen conditional
baseline; the supplied predicate callback never executes.

V2 also passes184regressions across23configurations, four contact categories
(other/vehicle/pawn/special) and permitting/rejecting variants. The first joined
fixture installed a second owned vehicle-class identity and misclassified
vehicle contacts outside its selected-other catalog. V2 reuses the original
contact class. `rules-class-identity-correction-v1.json` retains eight direct
comparisons, including the two affected vehicle outcomes, and proves the fix.
Configuration setup retains its supplied class/config services; native code
is restored before mesh handling. The current image audit verifies50protected
spans after setup and across owner/return images.

`demolition-metadata-native-v1.json` proves270authored/boundary and44owned
positive/negative typed metadata cases. Native explosion code evaluates the
shipped ANY tag-query bytecode and accepts matching finite Distance<=the
configured threshold. Native buildable code checks explicit/parent blocklists
and inverts the match. Four native constructor cases additionally prove the
omitted buildable blocklist defaults to empty, initialize the explosion query
and bind both VFT+2B0 predicate slots. UObject/base initialization is supplied.
`demolition-metadata-graph-native-v1.json` then passes7,761cases over all39asset
rule graphs, including source tags/children, thresholds/nextfloatabove and
buildable metadata.3,081permit. These graphs are separate from an explosion
caller/world/damage join. The metadata code audit verifies36protected spans.

Correction to earlier boolean labels:SDK EBHDemolitionType is Blocking=0 and
Overlap=1; context byte+8 is the enum, not a blocking-hit boolean. Native200case
truth table verifies bit0 permitsOverlap andbit1 permitsBlocking. Existing
`blocking`/`blocking_hit` boolean fields storebool(rawtype), so true meansOverlap.
The mesh query supplies raw1Overlap. `demolition-type-label-correction-v1.json`
binds59,706legacy field occurrences across four frozen receipts without changing
numeric results. Both authored permit bits were true, so catalog outcomes stand.

Native graph/query/health execution uses supplied object/class/variant/map and
property population, tag identities/parent-container construction, world,
physics, CRT, allocator, registry/locks/reference lifetime and timer services.
The read-only query skips actual demolition mutation; graph growth is untested.
Base53C7AC0callback/effects and532D4C0filter remain supplied; their full selected
CFGs are now captured but unexecuted. Actual explosion caller/world integration,
loading/authority/class/runtime lifecycle, allocation growth and scheduling also
remain open. Track1 remains incomplete;2-5 remain queued. No live access, product
code change, commit or push.

`rules-mesh-metadata-checkpoint-validation-v2.json`, FIRST_TRACK_AUDIT_v13.md and
RESUME_CHECKPOINT_v40.md preserve this checkpoint and its next steps.


### Checkpoint v41: native collision physics lookup/gate and base callback

The former532D4C0filter shortcut is now a native hit-to-physics-group and
VehicleDamagePhysicsData lookup. Native50F41D0 checks component membership,
resolves body-setup weak pointers, selects one of nine geometry arrays, applies
optional shape-name overrides and chooses a group by body-result index. Native
532D4C0/48A9940 select exact or nearest-parent physics data, including the
bExecuteCollisionEffects byte. Native FName hashing and parent-manager wrapper
execute; object/map/geometry installation, registry lookup, locks and reference
lifetime remain supplied.

Fresh PAK exports match15explicit MVF_HealthSections objects and all40authored
PhysicsGroupMappings rows. One disables collision effects and39enable them.
These are explicit exports; inherited/omitted fragments and active module
applicability are not established. `collision-physics-native-v1.json` passes
220authored queries plus37weak-reference/index/geometry/override/parent cases.
The populated fields cover flag/modifier selection, not damage routing.

`filter-rules-mesh-native-v1.json` embeds that native lookup into767E640 without
a gameplay answer bridge.3,680cases cover23settings x40rows xexact/child query
xpermitting/rejecting demolition variants; four missing-map/nomatch cases also
pass. The false flag suppresses the callback in92catalog cases; the remaining
3,588reach it. Missing physics data also reaches it. Prior target/owner health
and events match. The base53C7AC0body remains a suppliednoop in this joined
receipt; the owner-receiver phase retains its previous supplied group fallback.
The service-image audit verifies70native spans after setup/upstream/owner/return.

Separately, `base-collision-callback-native-v1.json` executes the full selected
53C7AC0body, native impulse normalization/up-vector math, vehicle-class alias,
4C46730cue wrapper and the cached4C47EB0provider/TLS path.1,068finite arithmetic
cases and30guards/handoffs pass, producing735owned manager-receiver dispatches.
The pawn branch compares impulse squared length strictly above a supplied
character threshold and records impulse length as RawMagnitude. The general
branch uses float32(abs(relative velocity dot Hit.Normal)) strictly above a
supplied threshold. Native orientation gating and recursive two-vehicle handoff
are covered. Location, Normal, instigator/causer handles and physical material
are checked at the FWDGameplayCueParameters receiver boundary. Engine physics,
weak-key creation, class/config inputs and the already initialized provider/
manager receiver are supplied; actual cue rendering/replication is untested.
Authored base-config threshold/default acquisition remains open.

The separate filter/callback code audit checks124native spans; together with
the joined audit this is194checks. Side-selector clarification:
`collision-physics-side-labels-v1.json` binds the legacyown_side field to the
raw fifth50F41D0argument: false selects MyBoneName+F8/MyItem+A4, true selects
BoneName+F0/Item+A8.532D4C0usesfalse. Hit.ElementIndex+AC, notFaceIndex, selects
the geometry element. Earlier frozen numeric receipts are unchanged.

Next is replacing the mesh's supplied53C7AC0callback with the verified native
body. That integration must enlarge the owned actor allocation safely, preserve
component/stats/owner pointers and reconcile class identities and service
images. Physics routing under the owner receiver, actual base-config loading,
explosion caller/world integration, growth/scheduling and runtime class/world/
lifecycle inputs remain open. Track1is incomplete;2-5 remain queued. No live
access, product-code change, commit or push.

`filter-base-callback-checkpoint-validation-v2.json`, FIRST_TRACK_AUDIT_v14.md
and RESUME_CHECKPOINT_v41.md preserve the evidence and continuation.


### Checkpoint v42: native base callback joined through cue parameters

`full-callback-mesh-native-v1.json` removes the supplied53C7AC0callback from the
selected767E640path. Native complex-hit/physics-data lookup, base callback,
cue wrapper/cached provider path, demolition rules/fragment factor and owner/
target health now execute in the same emulator.3,680catalog cases and736contact
category/simulation/flag/demolition regressions pass. The catalog produces3,588
owned cue-manager dispatches; the category regressions produce276. Six separate
native callback results check the typed cue fields. Health, events and selected
source/context fields match the previous conditional-callback baseline.

Both owned actor objects were copied into guarded0xAD0allocations, with owner,
component, stats, controller and cache references updated. Guards hold in every
case. The joined class-marker views now use one pawn identity across contact,
query, point-event and callback services. The old contact/point/query pawn
indices were2/1/3; current pawn/vehicle/special markers are0/1/2. Callback and
contact classify vehicles as pawns consistently. This proves the supplied
marker profile, not actual runtime UClass installation or inheritance state.
The post-setup service-image audit verifies80protected native spans.

The callback receives the native mass-adjusted collision vector, not the
original mesh-hit impulse. With owned impulse(1000,2000,3000) and masses10/20,
the observed callback argument is(33.333333333333336,66.66666666666667,100).
The frozen input field remains namedimpulse. Cue position/normal, magnitude,
instigator/causer and physical-material copy are checked independently; padding
bytes are not treated as semantic fields.

`callback-config-defaults-native-v1.json` executes the native base constructor
and four derived config constructors, including null initializer guards. Nine
cases prove the common callback threshold+128defaults30, character threshold
+12Cdefaults10 and default cue tagNone. Native registration name/size/constructor
arguments bind all five classes. Base UObject and derived lifetime/delegate
services remain supplied. Fresh PAK exports match25complete config Properties
objects covering references to all23settings rows.19explicitly provide collision
cue tags; six retainNone. Two rotary configs override the separate public
CollisionEffectImpactThreshold+124to10; neither overrides callback+128.

`authored-callback-mesh-native-v1.json` replays these effective candidate fields
in300same-emulator cases: general20/30/31boundaries, pawn squared-vector9/16
boundaries, recursive vehicle handoff and two demolition outcomes. All pass,
with152cue dispatches and preserved health results. This is a reference-linked
candidate replay: active variant/config selection, native property loading,
runtime actor cue overrides and actual rendering/replication remain unproven.

Next is native physics-group routing in the owner collision receiver. Its
53C9A90/53CA690mesh discovery and50F41D0group fallback are still supplied, and
its populated routing-map branch has not been joined. Config/module loading
precedence, explosion caller/world integration, growth/scheduling and actual
runtime world/class/lifecycle state also remain open. Track1remains incomplete;
2-5remain queued in order. No live access, product-code change, commit or push.

`full-callback-config-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v15.md
and RESUME_CHECKPOINT_v42.md preserve this checkpoint.


### Checkpoint v43: native owner physics section routing joined

The full mesh callback now reaches native owner physics-group selection,
collision modifier, sequential and simultaneous health routing. The new
`full-routed-mesh-native-v1.json` passes 3,680 cases: 23 gameplay settings,
40 explicit physics rows, exact and child tags, and two demolition outcomes.
Target health, events, selected source/context fields and 3,588 cue dispatches
match the frozen callback baseline. Owner health and handled return match an
independent native receiver replay using the amount produced by mesh code.
The gameplay path shares one emulator; the replay is verification only.

`physics-routing-receiver-native-v1.json` passes 1,120 catalog cases and
26 owned guard/variant cases against a stateful native section-health oracle.
The source has 32 rows with one sequential route, six with one sequential and
two simultaneous routes, and two with two sequential routes. Sequential routes
multiply the remaining amount and accumulate handled damage. Simultaneous
routes multiply the original scaled amount and do not add their handled result
to the function return. Both can change health. Routing entries have a 20-byte
stride. Sparse inline/external allocation bits and holes are exercised.
Four health sections are declared owned inputs: main, fuel tank and both front
wheels. This does not establish installed runtime attribute sets or map order.

Correction to v42: 53C9A90 and 53CA690 resolve seat occupants/fallback pawns;
they are not mesh discovery. Missing occupants do not skip physics lookup.
Native 531FC20 still reaches 50F41D0 using MyBone/MyItem hit fields, resolves
the nearest parent physics row and applies native 53984A0 before routing.
The authored row with collision effects disabled still applies collision
damage; its coefficient is 18.5, so an admitted 100-unit input damages main
health by 1,850. The effect flag controls the cue callback, not damage admission.

`full-routed-driver-native-v1.json` passes 280 joined cases: 40 physics rows
and seven owned seat/pawn/controller states. The same pawn marker is used by
contact, callback, query and driver cast. Valid drivers supply causer/controller;
absent or non-pawn occupants supply neither. A garbage pawn pointer can remain
in the causer field while controller is zero. This records native output,
without asserting that such a pointer is valid. Positive historical-seat/world
fallback remains untested. Code bytes are checked in upstream, owner, restored
upstream and post-catalog phases; successful producers and fixtures are frozen.

Remaining track 1 work includes config/module selection and loading precedence,
inherited/omitted fragment application, explosion caller/world integration,
cache growth/rehash and timer scheduling, and actual world/class/lifecycle/
animation/history inputs. Engine attribute, registry, requirement and lifetime
services remain supplied. Track 1 is incomplete; tracks 2-5 remain queued in
order. No live access, product behavior change, commit or push.

`full-routed-mesh-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v16.md,
RESUME_CHECKPOINT_v43.md and checkpoint-integrity-v43.json preserve this result.


### Checkpoint v44: native config override/fallback selection

`vehicle-config-selection-native-v1.json` verifies native 53CBBC0 application
at UMVF_VehicleConfig VFT slot 89, with native typed-metadata helper 53B6190
and config/pawn class getters. Frozen VFT bytes bind that slot and metadata
slot 88 (53CE640). The helper's registration-name argument binds the label
MVFCustomData_VehicleConfig, matching the SDK OverrideVehicleConfig field;
the module's fallback VehicleConfig soft reference is at +40.

2,400 cases cover override and fallback resolution states, metadata presence
and exact/derived/unrelated types, target class/presence, GC mode and declared
cold/warm metadata registration. Sixteen further cases change the override
between its two resolution calls. Native selection prefers a typed override;
an absent, unresolved or unrelated override uses the module fallback. A typed
override whose object is marked garbage is selected first, then fails the
final validity guard without trying the fallback. A changed second resolution
also fails without falling back when null, unrelated or garbage. Only a valid
selected config and valid target class cause pawn+A78 installation and the
VFT+8E0 notification dispatch. Failure preserves the previous config pointer.

This proves native control flow for supplied soft-reference results, class
marker profiles and target context. The engine resolver, metadata registration,
target-context service and notification body remain supplied. It does not prove
PAK asset loading, module ordering, inherited fragment application or complete
config acquisition through the full mesh. Track 1 remains incomplete; tracks
2-5 remain queued in order. No live access, product-code change, commit or push.

Next native leads are metadata selection 53CE640 and the actual pawn config
notification 53C0080 (ABHBaseVehiclePawn VFT slot 284 / +8E0), followed by
linking selected config fields to the existing callback/routing path. Remaining
explosion caller/world, cache/timer and runtime input gaps stay separate.

`vehicle-config-selection-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v17.md,
RESUME_CHECKPOINT_v44.md and checkpoint-integrity-v44.json preserve this result.


### Checkpoint v45: native config metadata and base notification

`vehicle-config-metadata-native-v1.json` passes 600 metadata/path guard cases
and 75 source-linked request cases for 25 explicit MVF_VehicleConfig exports.
Native 53CE640 chooses a typed override with a non-empty package field or the
module fallback. Native 17A4E20 deep-copies the soft path, including UTF-8
subpaths, and 1603EE0 destroys temporary path strings. The request pair is
moved into the output, the temporary pair is zeroed and the valid flag is set.
That flag records a request handle, not proof that the asset exists or loaded.
48AC720 remains a recording asset-request engine boundary. Fresh PAK decoding
in `config-module-pak-v1/manifest.json` subsequently matches all 25 complete
module Properties objects at their names/types/export indices. No VehicleConfig
field was omitted in this explicit module set. Active module order and inherited
fragment application remain unproven.

`vehicle-config-notification-native-v1.json` replaces the selection fixture's
notification shortcut with actual base-pawn 53C0080. Native camera guards and
53A4630 install camera assets; 26CCE10 copies five arrays of 8-byte input names.
Native role-3 history arithmetic clamps rate/scale, allocates 44-byte entries,
moves the buffer and releases the old one. 324 camera/input/event-guard cases,
192 history cases and 400 selection/notification cases pass. Frozen base-pawn
VFT bytes bind slot 284/+8E0 to 53C0080 and slot 311/+9B8 to the native default
return. Engine camera transform/activation, allocation/copy/free, scale, lifecycle
and registration services are supplied. Positive event maps and new network
physics settings creation have not been exercised.

Correction to the v44 corpus lead: actor +788 is VehicleEventComponent, not
the operator component; config +60 is EventMappings. Actor +768/+770 are third-
and first-person spring arms. SDK offsets and native field accesses bind these
labels. The current notification fixture intentionally exercises missing or
garbage event components. It does not replace the event mapping body with a
successful result.

Derived notification overrides are distinct: airplane 53BFEE0, rotary 53C0540,
tracked 53C06E0 and wheeled/WD-wheeled 53C0B50. Their direct CFGs are captured
but not executed by this base-pawn suite. These overrides, positive event/
network branches and linking native selected config into the full mesh remain
next. Explosion caller/world integration, cache/timer behavior and genuine
runtime input gaps remain open. Track 1 is incomplete; tracks 2-5 remain queued
in order. No live access, product-code change, commit or push.

`config-metadata-notification-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v18.md,
RESUME_CHECKPOINT_v45.md and checkpoint-integrity-v45.json preserve this result.


### Checkpoint v46: native wheeled config notification and axle construction

`wheeled-config-notification-native-v1.json` joins native config selection and
installation to actual wheeled 53C0B50, the base notification and seven native
wheeled setter helpers. Frozen VFT entries bind both MWheeledVehiclePawn and
WDWheeledVehiclePawn slot 284 to this body. 486 component/asset guards, 216
rate/axle/wheel cases and 256 selection cases pass their expected outcomes.
The guard suite includes 54 explicitly expected native read faults, rather
than 486 successful applications: the input setter 536F090 does not guard a
null input asset. Garbage-marked input assets are also copied. Other individual
asset setters have their own guards. A fault can occur after earlier settings
have already changed; no rollback is asserted.

Native characteristics update rate clamps to 50..1000, with timestep 1/rate;
mass, engine/transmission fields and three gear ratios are installed. Native
axle construction uses 112-byte records and deep-copies 64-byte wheel
configuration records, preserving owned names, physics tags and indices.
Non-empty axle/wheel arrays, native temporary destructors and selected pointer
storage execute. Wheel tag containers and runtime wheel-state arrays are empty
in these owned profiles. Allocation/copy/free, weak-handle registration and
component/profile virtual activation remain supplied engine services.

The derived actor component lives at +AD0, so the old base fixture allocation
cannot contain it. The new fixture uses a separately guarded C00-byte actor
and a guarded 2000-byte physics allocation; both retain their end guards.
These capacities are fixture allocations, not claims about actual UClass size.
No actual asset loading, physics world registration or config-to-mesh join is
claimed. Air/rotary/tracked overrides, positive event/network branches, full
config acquisition, explosion caller/world and cache/timer gaps remain open.
Track 1 is incomplete; tracks 2-5 remain queued in order. No live access,
product-code change, commit or push.

`wheeled-notification-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v19.md,
RESUME_CHECKPOINT_v46.md and checkpoint-integrity-v46.json preserve this result.


### Checkpoint v47: native wheeled config-to-collision join

`configured-routed-mesh-native-v1.json` connects the native wheeled/base config
constructors, module selection, wheeled/base notification and axle construction,
gameplay settings copy, and full collision/cue/health path in one emulator.
Nine source-linked wheeled configs pass 2,880 catalog cases (40 physics rows,
exact/child tags, two demolition outcomes and override/fallback selection).
Their target/owner damage results match the frozen routed-mesh baseline.
2,808 catalog cue dispatches match independent native callback replays using
the selected config's actual cue tag and native 30/10 threshold defaults.
216 further cases verify equality/above-threshold, pawn-vector and recursive
vehicle behavior against the prior authored-config suite.

The settings-copy path now executes native 53CB340 to read the selected actor
+A78 pointer, native 188F5C0 to check the selected config's GameplayConfigDataAsset
reference, and native 767BC40/36269E0 to install settings. The old supplied
container/getter shortcuts are absent in this phase. The actor's config pointer,
its callback fields, its gameplay reference and copied component settings remain
unchanged through collision. The callback does not reinstall a substitute config
or rewrite its thresholds/tags. Native-copy preservation already present in the
mesh fixture remains enabled. The actor uses guarded C00 storage and an A00
owned VFT; previous owner/component/cue/controller/stats/cache references are
updated explicitly.

36 rejected-reference cases exercise null or unrelated gameplay assets through
both selection routes. Native setup clears component +F0 and does not copy
settings. Actor +A78 still holds the selected vehicle config. The harness does
not invoke collision for these cases; its ready_for_collision flag is an
orchestration decision, not a newly discovered native collision guard.

Source cue fields and the GameplayConfig reference are supplied property
overlays after native construction. UObject/delegate initialization, class
markers, soft resolution, physical world, movement/input profiles and engine
lifecycle services remain owned inputs. The movement profile used for setter/
axle activation is synthetic, distinct from each config's authored subassets;
primitive mass/pose queries are still supplied. This proves a native control-
and-data join, not actual UObject loading, active variant/module ordering or
physical installation in a game world. Air/rotary/tracked notifications,
positive event/network branches, explosion caller/world integration and cache/
timer gaps remain open. Track 1 is incomplete; tracks 2-5 remain queued in order.
No live access, product-code change, commit or push.

`configured-routed-mesh-checkpoint-validation-v1.json`, FIRST_TRACK_AUDIT_v20.md,
RESUME_CHECKPOINT_v47.md and checkpoint-integrity-v47.json preserve this result.


### Native throwable-contact impact caller checkpoint v48

The frozen build's native `6CA8730` throwable-contact caller now executes through
point-event assembly, source rules and target health in an owned fixture.
1,840 cases span 23 canonical targets, four declared source profiles, five damage
amounts, driver presence and GC variants. 1,380 nonempty-root cases match an
independent native collision point-caller replay with equivalent enriched source.
The 460 empty-root cases have no paired oracle: the throwable caller preserves
`None`, while the older collision caller substitutes `Landscape`.

Native source/controller getters execute. The caller uniquely adds Throwable
and Impact contexts and replaces source cause with actor EntityId. Hit location
remains `None`. 18 guards, 83 timing cases and two repeat sequences pass; 85 code
image checks preserve 17 captured functions. Positive handled damage sets the
repeat latch. A latched positive cooldown compares float32(double world time
minus stored float) with the cooldown; equality admits. This function leaves the
stored timestamp unchanged. External scheduling effects remain unproven.

World/mode/target/interface lookup and engine tag/lifetime services are supplied;
mode codes remain raw values. This is throwable contact impact, distinct from
radial detonation. Radial gather `6F01E50` and upstream `6EFFDC0` are CFG-captured
but unexecuted. Actual world/multi-actor/lifecycle integration, asset installation,
derived notification/event/network branches, cache growth and timers remain open.
Track 1 is incomplete; tracks 2-5 remain queued in order. No commit or push.

Private restart: `RESUME_CHECKPOINT_v48.md`, `FIRST_TRACK_AUDIT_v21.md`,
`explosive-impact-checkpoint-validation-v1.json`, `checkpoint-integrity-v48.json`
under `round11_collision_parity_20261020`.


### Native radial gather builder checkpoint v49

Native `6F01E50` now iterates supplied sparse world results and constructs actor/
radial-event records through native constructors and deep hit-array copies.
20 critical scenes (63 contacts) and 24 owned guard/filter cases preserve the
prior full-radial damage and health results. 102 standalone gather cases verify
multi-actor construction across 0–137 slots, inline/heap bitmaps, holes and
occupied null/garbage actors. Joined health cases still contain one valid actor.

Native event construction copies base damage into both leading damage fields;
the outer caller still computes per-contact falloff from the original inputs.
This replaces the prior shortcut's assumptions about constructed event fields.
3,818 native image checks pass. Upstream `6EFFDC0` additionally executes through
the radial caller for 16 empty-query/invalid-world cases with 16 image checks.
The engine query boundary observes shape 2/radius 2000; query results are supplied
empty. Nonempty native grouping, component geometry/LOS, actual world identity,
multi-actor health and lifecycle remain open. Engine setup and lifetime services
remain owned; empty-query options setup is a no-op, not a native-copy proof.

Track 1 remains incomplete; tracks 2–5 remain queued in order. Private restart:
`RESUME_CHECKPOINT_v49.md`, `FIRST_TRACK_AUDIT_v22.md`,
`native-radial-gather-checkpoint-validation-v1.json`, `checkpoint-integrity-v49.json`
under `round11_collision_parity_20261020`. No commit or push.


### Native nonempty overlap grouping checkpoint v50

A bounded native `6EFFDC0` window now processes supplied nonempty engine overlaps
into actor/component groups. 64 cases verify first-seen order, repeated item
append, invalid actor/component/interface handling, bone selection and native
transform copying, including growth to 20 actors, nine components, 11 items and
nine transforms. 1,792 native image checks pass; input overlap records stay intact.

Execution stops explicitly at `6F0088C`, before LOS, final contact/map construction,
cleanup, return or damage. Engine query/weak/class/config/bone/pose data and
allocation/rehash services remain supplied. The actual vehicle virtual disables
the special distance path, leaving its distance field at FLTMAX. This proves
native grouping/copy behavior, not actual geometry/LOS or complete world parity.

Track 1 remains incomplete; tracks 2–5 stay queued. Private restart:
`RESUME_CHECKPOINT_v50.md`, `FIRST_TRACK_AUDIT_v23.md`,
`nonempty-world-group-checkpoint-validation-v1.json`, `checkpoint-integrity-v50.json`
under `round11_collision_parity_20261020`. No commit or push.


### Native nonempty world gather return checkpoint v51

Native `6EFFDC0` now completes its nonempty world-gather return for declared
mode-0 pose-class and engine-trace inputs. 140 cases cover 440 supplied traces;
5,600 native code-image checks pass. Execution extends the prior grouping window
through native sampler/lazy initialization, LOS admission, contact insertion,
distance sorting, final sparse-map ownership transfer and intermediate cleanup.
The same UC frame is paused to install supplied class/owner views, then resumed.

Native sample initialization produces the 15-point pattern and later calls use
its cache. Range equality admits; misses, wrong components and far impacts reject.
Equal-distance contacts can reorder during native sorting; actual receipt order
is retained. Original overlap bytes remain intact and source hit arrays clear
after native ownership transfer. Distinct actor contacts are constructed, while
outer radial damage and independent actor health remain unjoined.

Mode 0 explicitly overrides the frozen default 2. Other modes/classes, real
physics, query-option copying and engine lifecycle remain unproven. Engine
queries/traces, class/weak/config/bone/pose, allocation/rehash/free and thread-guard
services remain supplied. Track 1 is incomplete; tracks 2–5 remain queued.
Private restart: `RESUME_CHECKPOINT_v51.md`, `FIRST_TRACK_AUDIT_v24.md`,
`complete-world-gather-checkpoint-validation-v2.json`, `checkpoint-integrity-v51.json`
under `round11_collision_parity_20261020`. No commit or push.


### Native world-to-radial independent health checkpoint v52

The nonempty native world gather now feeds native gather-event construction,
radial filtering/falloff, source rules, typed dispatch and independent actor
health in one UC. 288 mode-0 cases across 23 damage target tags match 1,104
separate per-actor native radial replays. Distinct model/interface/tag-owner/
attribute objects preserve per-actor health, events and damage causes. Owned
actor/component views are prepared before entry; no grouping pause or synthesized
gather output is used. Models here have one synthetic main health attribute.

The joined fixture now uses one shared settings object for world and damage,
and native query setup/copy replaces no-op options handling. Four direct audit
replays verify both fixes. Algorithm 1 additionally passes 32 comparison cases
across three damage tags against a separate mode-0 joined fixture. Together,
13,002 native code-image checks pass. Native query inputs use empty ignore lists.

Modes 0/1 override frozen default 2. Default-mode execution, other component
classes, authored multi-section health/config joins and actual engine geometry,
identity/lifecycle remain open. Physics queries/traces, class/weak/property/pose/
hit-location views and allocator/rehash/name/thread/free services remain supplied.
The 23 damage tags do not establish 23 native physics subclasses. Track 1 stays
incomplete; tracks 2–5 remain queued. Private restart: `RESUME_CHECKPOINT_v52.md`,
`FIRST_TRACK_AUDIT_v25.md`, `joined-world-radial-checkpoint-validation-v1.json`,
`checkpoint-integrity-v52.json` under `round11_collision_parity_20261020`.
No commit or push.


### Frozen-default world query checkpoint v53

Native selector 2, the frozen PE default, now runs the SkinnedMesh pose path
through visibility masks/callbacks, contact construction, radial rules and
independent actor health. All 288 cases match the frozen mode-0 joined dataset
across 23 damage tags. 552 visibility-cache reuses are directly observed.
32 additional cases cover blocked/clear misses, cache reuse, bounds variation,
radius equality/outside and GC/order. Together, 18,880 code-image checks pass.

The remaining branch getters are now statically name-bound to
SkeletalMeshComponent, InstancedStaticMeshComponent and ShapeComponent. Their
positive paths, authored multi-section health/config joins and actual engine
geometry/identity/lifecycle remain open. Engine bounds/queries, class/pose/weak/
property views and allocator/runtime services remain supplied. Static default
selection does not prove live config, and image counts are not branch coverage.

Track 1 remains incomplete; tracks 2–5 stay queued. Private restart:
`RESUME_CHECKPOINT_v53.md`, `FIRST_TRACK_AUDIT_v26.md`,
`default-world-checkpoint-validation-v1.json`, `checkpoint-integrity-v53.json`
under `round11_collision_parity_20261020`. No commit or push.

### Native component branches checkpoint v54

The frozen default selector 2 now has 64 owned component cases (16 scenarios,
GC on/off, trace hit/miss): Skinned pose/empty, generic center, Skeletal default
and indexed body handles, InstancedStaticMesh identity/translation/index bounds/
empty pose/item filtering, and Shape raw codes 1/2/3 candidate points. Analytic
world point sets and a separate native radial-to-health oracle match; 4,288
code-image checks and guarded component allocations pass. Skeletal sampling
passes no item filter, while the instanced route rejects a wrong Hit.Item.

Class metadata, body handles/poses, shape values, physics and runtime services
remain supplied. Unit component transforms and translated instances are tested;
rotation/scale breadth, real engine views and authored multi-section config joins
remain open. Code-image counts are not branch coverage. Track 1 is incomplete;
tracks 2-5 remain queued. Private restart: RESUME_CHECKPOINT_v54.md,
FIRST_TRACK_AUDIT_v27.md, component-branches-checkpoint-validation-v1.json,
checkpoint-integrity-v54.json under round11_collision_parity_20261020.
No live server access, commit or push.

### Authored section health checkpoint v55

226 native world-to-health cases passed across 23 vehicle damage-row groups:
113 exported section views with GC off/on, 452 independent actor health oracles,
and 15,142 code-image checks. Two actors retain distinct authored health limits
and routing state. Source checks bind 139 files and match enabled health
fragments for all 32 included variants. These prove config arithmetic under
supplied initialization and section resolution; native asset loading/module
order and actual physics remain open. Track 1 is incomplete; tracks 2-5 queued.

Private restart: RESUME_CHECKPOINT_v55.md, FIRST_TRACK_AUDIT_v28.md,
world-authored-sections-checkpoint-validation-v1.json, checkpoint-integrity-v55.json.
A separate 308-case native surface/section resolver run is pending and excluded
from this checkpoint's proof. No live access, commit or push.

### Native surface/section join checkpoint v56

All 154 catalog slots passed through native component-registry/face/item lookup,
surface group/slot resolution, section and hit-location selection, damage rules
and authored section health: 308 cases with GC off/on and two actors. Another
46 guard/item/numbered-slot cases passed. Across these, 662 separate native health
oracles match. The former supplied 6B80230/5338730/50BF880 answers now execute
natively. StaticMeshComponent is PE-name-bound; runtime metadata remains owned.

Eight empty-fragment cases also pass native discovery/dead-object gates and the
WD/base apply continuation. Total: 28,738 code-image checks. Populated fragment
installation, attribute/delegate creation, actual asset loading/registration,
geometry and remaining runtime/lifecycle gaps stay open. Catalog registry/face
views and engine services are supplied; counts do not imply branch coverage.
Track 1 remains incomplete; tracks 2-5 stay queued.

Private restart: RESUME_CHECKPOINT_v56.md, FIRST_TRACK_AUDIT_v29.md,
world-surface-resolver-checkpoint-validation-v1.json, checkpoint-integrity-v56.json.
All capture jobs are terminal. No live access, commit or push.

### Native fragment installation checkpoint v57

46 source-ordered installation setups and 308 downstream slot-damage cases passed.
Native insertion starts from empty preallocated section and complex-surface maps;
source config identities are preserved. Enabled fragments are applied separately,
and all 32 variant health/complex views match their 23 source templates. Native
world-to-health results match separate native health oracles. Total: 26,512
code-image checks, which do not imply branch coverage.

Attribute handles, registration/notification backends and engine runtime services
remain supplied. Physics-group maps are empty in this dataset; the next prototype
copies real source physics rows natively. Runtime module order, real attributes,
callback delivery, geometry and lifecycle remain open. Track 1 is incomplete;
tracks 2-5 queued. Private restart: RESUME_CHECKPOINT_v57.md, FIRST_TRACK_AUDIT_v30.md,
populated-fragment-checkpoint-validation-v1.json, checkpoint-integrity-v57.json.
No live access, commit or push.

### Corrected native physics installation checkpoint v58

All three source health-fragment maps now install natively: health sections,
complex-surface mappings and physics-group routing. The corrected run passed
46 setups and 308 downstream slot-damage cases, installing 92 physics groups
across 23 templates with GC off/on. Total: 26,834 code-image checks.

Physics tag/float entries are 20 bytes. The initial new fixture incorrectly used
24 bytes and its partial run was stopped before a success receipt. A native
consumer regression now rejects that malformed layout and matches independent
native health results after correction (two cases, 160 additional image checks).
The two labels select installation GC; they do not independently toggle consumer
GC. Historical physics-prototype claims are superseded by the private layout
correction. v57's health/complex validation is unaffected.

Geometry, real attribute/delegate/notification backends and runtime module order
remain open. Track 1 is incomplete; tracks 2-5 queued. Private restart:
RESUME_CHECKPOINT_v58.md, FIRST_TRACK_AUDIT_v31.md,
physics-fragment-checkpoint-validation-v1.json, checkpoint-integrity-v58.json.
No live access, commit or push.

### Installed physics to native collision health checkpoint v59

46 native source installations now feed native primitive/body group lookup,
parent-group selection, physics routing and authored section health. All 416
cases passed across 23 templates: exact/child group queries, small/depletion-sized
damage, and explicitly observed consumer GC off/on. No group or section-result
injection is used. Native health oracles match; 13,534 code-image checks pass.

Physics routes may reference globally named tags absent from a model's health
map. The independent oracle now preserves those names while keeping the health
sections absent; health/event behavior matches. Shape reachability remains an
owned input. Primitive/body/weak registration, real runtime backends and asset
loading remain open. Track 1 is incomplete; tracks 2-5 queued. Next is joining
native-installed maps to the full mesh/contact callback chain.

Private restart: RESUME_CHECKPOINT_v59.md, FIRST_TRACK_AUDIT_v32.md,
installed-geometry-checkpoint-validation-v1.json, checkpoint-integrity-v59.json.
All capture jobs are terminal. No live access, commit or push.

### Installed maps through native contact callback checkpoint v60

All 416 source-linked contact cases passed across 23 templates and 46 native
installations, with installation/contact GC off/on. Native-installed health,
complex and physics map identities survive the full owned mesh/contact/filter/
base-callback/cue/rules/owner-health chain; contact setup reads the physics map
without reseeding it. Owner health uses authored maxima. Separate native full
callback and section-health fixtures match upstream/target outputs and authored
owner health/events/returns/recursive calls. 5,860 image integrity checks pass.

Settings linkage is static; native active configuration selection remains the
next catalog join. A separate Humvee configuration prototype passes GC off/on,
but does not establish catalog completion. Owned geometry/registry, attribute/
delegate/notification/timer backends and actual engine lifecycle remain open.
Track 1 is incomplete; tracks 2-5 queued. Private restart: RESUME_CHECKPOINT_v60.md,
FIRST_TRACK_AUDIT_v33.md, installed-contact-checkpoint-validation-v1.json,
checkpoint-integrity-v60.json. All capture jobs terminal. No live access or push.

### Native selected configuration and installed contact checkpoint v61

All 576 cases passed: nine authored wheeled configurations/eight templates,
18 native source installations and 36 override/fallback selection setups. Native
configuration construction/selection/notification and linked settings copy now
precede the full owned contact chain and source-installed owner health/physics
maps in one emulator. Config/map identities and copied settings survive. Separate
configured callback and section-health fixtures match target/cue/config outputs
and authored owner health/events/returns/recursive requests. 7,290 code-image
integrity checks pass. Installation/contact GC is varied; configuration-stage GC
is not independently varied. First exact group adds low/high speed boundaries.

Real attribute/delegate/notification backends, auxiliary gameplay/module lifecycle,
actual geometry/loading/order and network/event/cache/timer delivery remain open.
Static backend leads and raw CFGs are saved privately, without execution claims.
Track 1 is incomplete; tracks 2-5 queued. Private restart: RESUME_CHECKPOINT_v61.md,
FIRST_TRACK_AUDIT_v34.md, ATTRIBUTE_BACKEND_NEXT_v1.md,
installed-configured-checkpoint-validation-v1.json, checkpoint-integrity-v61.json.
All capture jobs terminal. No live access, commit or push.

The v61 high-speed cases do not deplete owner sections under these authored
curve/routing outputs; they do not establish destruction behavior. The validator
records 308 nonpositive owner requests and zero depleted cases.
