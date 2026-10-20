---
title: Gepard collision inputs and native bounds
nav_exclude: true
---

# Gepard: native bounds and collision-filter inputs

Offline CL-516586 investigation, 2026-10-19. The restored executable and
existing read-only corpus were inspected; no game process or IDA database
was opened. This supplements the [explosive audit](round8-explosive-viewer-audit.md).

## Native static-mesh candidate bounds

**Gepard's actual render meshes also author 89 `DamageQuerySocket`
points**: Body 59, Spin 14, Pitch 10 and three on each barrel. The native
producer recognizes their FName comparison index, including numbered
instances, and transforms them into precomputed candidate records. The
bounds-origin candidate below is the zero-sample fallback, not a substitute
for those authored points. Bounds still supply the component's angle-test
direction. The dedicated CC collision meshes have no socket exports; the
socket source is the attached **SM render asset**. See the
[socket producer proof](round8-gepard-native-sampling.md#candidate-construction-and-order).

Points gathering calls component virtual `+0x598` at `0x6EFDA34`–`0x6EFDA4D`,
with its transform at component `+0x210`. For static mesh components this
is `0x3DB5AB0`. It transforms the mesh's bounds origin, rather than choosing
a closest collision vertex or using the collision triangles' bounding box.
The generic bounds-seed branch is conditional on there being no precomputed
samples for that overlap; this is not a claim that every overlap takes it.
See the [sampling trace](round8-gepard-native-sampling.md).

`0x3DB5AB0` reads StaticMesh from component `+0x5A8` and calls
`0x44C2BA0`. The latter was missing from the decompilation corpus but is
small enough to verify directly: instructions `0x44C2BA0`–`0x44C2BD0`
copy 56 bytes from mesh `+0x250` to the output. The matching SDK names
this field `UStaticMesh.ExtendedBounds` (`sdk/raw/Engine_classes.hpp:23489`).
Thus the authored ExtendedBounds, not parsed RenderData.Bounds, supplies
this native seed when the ordinary static-mesh branch applies. The
component transform still depends on actual animation/attachments.

Using original component-space reference bones, fresh mesh/socket exports,
and `vehicle_models.place` gives the following reference-pose origins.
These are transformed cooked inputs, not observed runtime component bounds.
Coordinates are displayed metres, with front along +Z and up along +Y.

| Render component mesh | Bounds-origin X | Y | Z |
|---|---:|---:|---:|
| Body | 0.000000153 | 1.150531840 | -0.124036710 |
| Turret Spin | -0.000000076 | 2.496075300 | -0.268854200 |
| Turret Pitch | -0.000003510 | 2.475440233 | 0.063303480 |
| Barrel L | 0.952438180 | 2.524649821 | 2.582917800 |
| Barrel R | -0.949790480 | 2.520825854 | 2.580143300 |

The placed GLB's node transforms also contain mesh quantization/dequantization
transforms. Applying those node matrices to asset-local Unreal bounds would
scale and translate the bounds incorrectly. The reconstruction instead
composes source attachment and reference-bone transforms before the usual
UE-centimetre to display-metre conversion.

External fixture:
`E:/Reverse_Engineer/wardogs_analysis/round8_gepard_explosive_collision_20261019/gepard-reference-inputs.json`.
It records all seven component transforms, the five authored bounds and
input manifest SHA-256 values. Chassis and TurretSkeleton have no published
triangle representation; their query eligibility must be checked separately.

## Collision complexity defaults and shape filtering

The native BodySetup constructor chain (`0x4227DA0` → `0x24676F0`) initializes
`UBodySetupCore.CollisionTraceFlag` at `+0x31` to zero (UseDefault; raw
write `0x246770E`). The skeletal-body constructor `0x42AE030` calls that
BodySetup constructor and adds its profile array without replacing the flag.
The fresh Gepard BodySetup exports omit an authored CollisionTraceFlag.

Getter `0x246D6E0` was independently disassembled: it loads the global
physics default from `+0x75`, reads body `+0x31`, and uses the latter only
when nonzero (`0x246D6F0`–`0x246D70A`). Native core construction
`0x24677E0` initializes default complexity to `0xFF` and the deprecated
complex-collision boolean to true. PostInit `0x246F660` converts that
sentinel to **1, UseSimpleAndComplex**, at `0x246F66E`–`0x246F67D`.
The derived physics-settings constructor `0x42E4930` calls the core
constructor; its PostInit `0x42D30A0` calls the core fixup at `0x42D30AD`.
Neither inspected derived routine replaces `+0x75`. None of the 219
extracted packed INI files assigns `DefaultShapeComplexity` or
`bDefaultHasComplexCollision`. This establishes the inspected shipped
default chain; external overrides and later runtime changes are not excluded.

Native `FBodyInstance` filter construction at `0x41E1B20` keeps simple
and complex query masks separate. The raw tail `0x41E1F0D`–`0x41E1F3A`
sets simple bit 1 and adds complex bit 2 **only for complexity 2**
(UseSimpleAsComplex). `0x41E1F45`–`0x41E1F54` sets complex bit 2 and
adds simple bit 1 only for complexity 3 (UseComplexAsSimple).

The shape-creation helper `0x422A320` selects query data at
`params + 0x14 + 0x10 * isComplexShape` (`0x422A380`–`0x422A3A4`).
Caller `0x423A2C0` supplies zero for primitive/convex shapes and one
for triangle meshes. This matches the separately inspected local UE
`ChaosInterfaceUtils.cpp` shape helper, while the bit construction matches
local `BodyInstance.cpp`. Consequently, a Visibility-blocking component
profile alone does not establish participation in a **complex** trace:
the shape's query mask matters too. Do not automatically add the skeletal
convex/boxes as complex-LOS blockers merely because they were recovered.
Exact query prefilter/registration and runtime overrides remain boundaries.

Local engine source is UE 5.7.4 **CL51494982**, not Wardogs CL516586. It is
schema guidance; the target-specific address/field claims above come from
the matching SDK and independently decoded executable instructions.

## Explicit incoming-direction fixture

The native projectile formula is already established:
`origin = impact - 0.5 * Length * SafeNormal(ImpactVelocity)`.
All 16 positive-radius projectile assets have an authored Length value;
the current catalog's MAAWS 84 mm value is 25.4 cm. For the reproducible
front hit `[0,1,3.7272073545342943]`, an **assumed** incoming direction
`[0,0,-1]` produces origin `[0,1,3.8542073545342943]`: 12.7 cm outward.
Zero velocity instead produces zero offset. The viewer camera and clicked
surface normal cannot establish the projectile's actual incoming velocity.
This direction is recorded as a scenario input, not an inferred game state.

## Conditional cooked-geometry probe

`gepard_socket_probe.js` in the external evidence root joins all five
render components to decoded cooked triangles and CC material slots, places
their 89 socket candidates with the original reference transforms, sorts by
original-origin distance, applies the 10-degree component angle gate and
shared pretrace cache, and retains the nearest accepted result after each
candidate's first accepted cloud start. The native shipped Points branch
copies complex query parameters into the cloud pretrace as well as using
complex candidate LOS (`0x6F00FD1`); the cloud constructor's initial simple
flag alone does not describe that branch.

This isolated probe accepts Body, Spin, Pitch and both barrels. All map to
MainBody, so it produces one application with 267.9 main-health loss and
14.1 FuelTank loss **routed from MainBody**, with no FuelTank contact. That
holds for zero offset and the explicit 12.7 cm incoming-direction offset,
using either double-sided triangles or an assumed single-sided test with
the UE winding convention. These are conditional offline results, not
observed damage. A bounds-only counterfactual omitted Pitch, showing why
the actual authored socket inputs matter even when tag deduplication leaves
the same health total.

The cooked front ray reaches `[0,1,3.7268998241731515]`, about 0.308 mm
from the published-GLB fixture's Z coordinate. The decoder's 1e-6 m match
is against raw component exports, not a claim that the compressed placed
viewer mesh preserves every world coordinate at that tolerance.

Probe assumptions remain explicit: all five static components are eligible;
both skeletal components are excluded; source assembly order is supplied;
there are no level/terrain occluders; engine query tolerances and optional
overlap Item gates are not reproduced. Raw complexity/filter evidence
narrows shape eligibility, but actual registration, later overrides and
engine overlap records are not observed. This is sufficient to compare
the recovered sampling inputs, not to replace the viewer with a claim of
runtime parity.

Artifacts: `gepard-socket-probe.json`,
`gepard-socket-probe-single-sided.json`, `gepard_socket_probe.js` and
`gepard-reference-inputs.json` under the external evidence root. The script
uses `VehicleImpactGeometry.rayTriangle` and the existing routing evaluator;
it is not an independent engine-query or damage-arithmetic oracle. It
refuses to overwrite the output report. The earlier
`gepard-bounds-probe-v2.json` is a zero-socket counterfactual and must not
be substituted for the authored-socket case.
