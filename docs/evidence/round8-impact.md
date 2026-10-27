---
title: Round 8 impact evidence
nav_exclude: true
---

# Round 8: contact and actor-impact amounts

Static inspection of CL-516586, restored executable SHA-256
`a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.
The corpus was opened read-only. Float arguments omitted by pseudocode were
checked in x64 instructions decoded from the original function entry with
Capstone; no game process or service was used.

## Thrown explosive contact

**Native + SDK.** `0x6CA8730` reads the actor's `ImpactDamage` at `+0x550`
into `xmm6` (`0x6CA8881`), moves it to `xmm1` (`0x6CA8959`), and calls
the damage-event builder `0x6BB4D30` (`0x6CA895C`). That builder writes
its float argument to event `Amount` (`+0`). The SDK names the field
`AWDExplosive::ImpactDamage` (`sdk/raw/WDGame_classes.hpp`). This is the
contact amount, not the detonation amount.

The source entity is copied from the actor's `DamageEntityComponent`
(`+0x300`), with two existing documented tags appended:
`Kinetic.Impact.Throwable` and `DamageType.Impact`. The original contact
hit is supplied to the event builder. The body calls the damageable
allow predicate (`+0x30`) before `ModifyDamage`; it does not dispatch the
general armor hook (`+0x18`) or the projectile armor hook (`+0x20`).
This is a bounded observation of this native body, not a claim about all
Blueprint callers or later damage handling.

**Static contact default: 10.** Explosive constructor `0x6CA7800` writes
qword `0x41200000` at actor `+0x550` (`0x6CA7AC4`), initializing
ImpactDamage to float 10 and the adjacent AdditionalGravity to zero.
The complete C4 constructor wrapper `0x6CA6A80` calls that constructor
at `0x6CA6A95` without overriding the field. Grenade wrapper
`0x6CADC90` and direct constructor `0x6CADED0` call it at `0x6CADCAA`
and `0x6CADEDD`; neither replaces ImpactDamage. Molotov wrapper
`0x86A0200` calls the grenade constructor at `0x86A0215` and has no
ImpactDamage override. These call/store checks used independently decoded
instructions for the complete native bodies.

Fresh local CDO exports in `round8_explosives_20261018` omit ImpactDamage
for `B_FragGrenade`, `B_ThrowableC4`, `B_ThrowableIED` and `B_Molotov`.
Their parent declarations select WDGrenade, WDC4, B_ThrowableC4 and
WDMolotovGrenade respectively. The four therefore inherit contact amount
10 under the documented native path. This does not assign contact damage
to the separately implemented placed landmines or confuse it with their
[resolved detonation defaults](round8-explosive-actors.md).

## Character struck by another actor

**Native.** `0x6E72D90` calls `0x6E6B670` at `0x6E7308B`, moves the
returned float from `xmm0` to the builder's `xmm1` (`0x6E730BB`), and
calls `0x6BB4D30` at `0x6E730C3`. Thus the event amount is computed by
`0x6E6B670`; it is not a fixed value stored in the infantry rule table.
The subsequent `ModifyDamage` call at `0x6E730D5` passes bool 1, which
returns the supplied amount without evaluating rule multipliers
([Damage §1](../../pipelines/Wardogs_DamagePipeline_v2.md#1-call-path)).

### Independently checked arithmetic and field boundary

Instructions `0x6E6BC3D`–`0x6E6BC5E` multiply three intersection-box side
lengths, including a double constant approximately `0.000001`, convert
the product to float, multiply mode `+0x70`, multiply settings `+0x88`,
then clear the sign bit. The settings object is validated against
`WDCommonPawnMovementSettings` (`0x69B6F80`); the SDK names `+0x88`
`UnresolvedCollisionDamageMultiplier`. Thus this last factor has an
independently identified owner and name.

The mode object is validated against `BHMoverMode_Base` (`0x527B020`).
Its SDK leaves `+0x70` inside opaque padding. Native constructor
`0x5283A40` explicitly zeros `+0x6C` through `+0x73` at `0x5283A78`.
A concrete writer starts at `0x529AB10` (the corpus row begins one byte too
early, at `0x529AB0F`). Its caller `0x529A940` is vtable slot 99 of
`UBHMoverMode_BodyDragging`/`UWDMoverMode_BodyDragging`, which derives from
ground movement; this does not establish a general ground-mode default.
Instructions `0x529AB63`–`0x529AB73` store mode
`+0x70 = float(input +0x40) * 0.001` with the binary double constant
`0.001` at RVA `0x9AC21A8` and a double intermediate. The input record's
layout is not named in the shipped SDK. The scale suggests a
millisecond-to-second conversion, but `StepMs` is not a verified name for
this offset. Other possible writers are not exhaustively traced.

### Actor-impact geometry and exact known factors

The `a2` input to `0x6E6B670` is an `FHitResult`, whose
`Component` weak pointer is at `+0xD8` and `BoneName` at `+0xF0`
(SDK layout). Helper `0x6E6D580`
uses those two fields to request the hit component's named body. If that
body supplies a finite, valid box and transform, the helper uses its
body-specific local box and transform. If the body is absent, its box is
invalid/non-finite, its transform scale is effectively zero, or its
transform fails validation, it obtains the hit component's local bounds
through `0x3D70090` and copies the component transform. That function's
branches match local UE 5.7
`Engine/Source/Runtime/Engine/Private/Components/SceneComponent.cpp:4161–4174`
(`USceneComponent::GetLocalBounds`). `0x6E6D580` multiplies each chosen box
endpoint by the corresponding transform scale and then replaces that
transform's scale with identity.

For the character side, `0x6E6B670` selects mesh or capsule using
`0x5296540`, obtains its `FBoxSphereBounds3d` local origin and box extent
via `0x3D70090`, and converts them to a local box
`[origin - extent, origin + extent]`. It computes the character component
transform relative to the hit-body/component transform through `0x165FE90`.
The latter's operations match `TTransform::GetRelativeTransform` in local
UE 5.7 `Core/Private/Math/TransformVectorized.cpp:205–249`: the translation
difference is inverse-rotated and divided by the other scale, with a
matrix path for negative scales. The caller transforms the character box
into that hit-body/component coordinate frame and forms its enclosing
axis-aligned box. Thus the hit box and transformed character box are
intersected in one frame. SDK layouts for `FBox3d` and
`FBoxSphereBounds3d` are here
and here.

Let `Hmin/Hmax` be the scaled hit box and `Cmin/Cmax` the transformed
character AABB. The native comparisons before `0x6E6BC3D` test for
disjoint boxes. Otherwise each intersection side is
`I_i = min(Hmax_i, Cmax_i) - max(Hmin_i, Cmin_i)`. A disjoint box takes the
zero-size empty-box branch; the corresponding local UE `TBox::Overlap`
returns `TBox(ForceInit)` (`Core/Public/Math/Box.h:79–85, 983–996`). The
known return formula is therefore

`abs(float(I_x * I_y * (I_z * 9.99999932944776e-7)) * mode[+0x70] * settings.UnresolvedCollisionDamageMultiplier)`

with zero intersection volume when disjoint and the native sequence of
double-to-float and float multiplications preserved. The `~1e-6` constant
converts cubic centimeters to cubic meters. Missing/invalid movement mode or
common settings returns zero before geometry. The source context comes from
the hitting actor's entity data with `DamageType.Impact`; individual actor
identities remain data dependent. Mode `+0x70`'s semantic name and complete
writer set remain open, although its value and one concrete writer are
identified by offset and instructions.

### Follow-up: input `+0x40` is the simulation substep duration

The input-identity limit above is resolved by tracing the original native
simulation dispatch. On this writer path, mode `+0x70` caches the supplied
simulation substep duration in **seconds**:

`mode[+0x70] = float(double(Params.TimeStep.StepMs) * 0.001)`

This conclusion does not import the newer local UE `FSimulationTickParams`
layout into the game. The game record's time-step block is located by its
actual copy and virtual dispatch, then its inner field is identified with
the shipped `FMoverTimeStep` layout.

1. Native component simulation `0x5203D10` copies its incoming 16-byte
   time-step record from `rdx` into stack `rsp+0x50`
   (`0x5203D37–0x5203D65`), changing the resimulation byte at record `+0xC`
   separately. `0x5204273–0x5204299` passes that local record as the sixth
   argument to state-machine simulation `0x51FAC40` at `0x52042A3`.
   The same copied record is later broadcast on component `+0xE0`
   (`0x520439E–0x52043B5`), which the shipped SDK identifies as
   `OnPostSimulationTick(const FMoverTimeStep&)`
   (Mover_classes.hpp:252).
   This independently identifies the record type. The shipped
   FMoverTimeStep names ServerFrame
   at `+0`, BaseSimTimeMs at `+4`, and float StepMs at `+8`.
2. `0x51FAC7B–0x51FAC95` loads that sixth-argument pointer and copies its
   16-byte block into local `rsp+0x78`. At each iteration,
   `0x51FAEEC–0x51FAEFD` reads incoming StepMs at `+8`, subtracts the
   accumulated used time in `xmm10`, and writes the current remaining
   substep duration to local `rbp-0x80` (the local block's `+8`). The
   state machine later clamps the returned RemainingMs, increments used
   time by StepMs minus RemainingMs, and advances BaseSimTimeMs by that
   consumed amount. This is substep accounting, not a guessed unit from
   the `0.001` constant alone.
3. `0x51FBFD8` loads the local time-step block. `0x51FC07B` copies it to
   `rbp+0x2F8`, while the assembled mode-input record begins at
   `rbp+0x2C0`. Thus the game record's TimeStep starts at `+0x38`, and its
   StepMs field is exactly input `+0x40`. Instructions
   `0x51FC377–0x51FC38B` pass that assembled record in `rdx` to the selected
   mode's virtual `+0x318`, slot 99.
4. Native vtable aliases identify `0x529AB10` itself as slot 99 of both
   `UBHMoverMode_GroundMovement` and `UWDMoverMode_GroundMovement`.
   BodyDragging's slot-99 override `0x529A940` delegates to this same body
   at `0x529AA21`. The conversion/write at `0x529AB63–0x529AB73` is
   therefore reached by the normal ground-mode simulation implementation
   as well as that demonstrated BodyDragging delegation. Zero in the
   constructor is an initialization value, not evidence that this field
   remains zero while ground-mode simulation runs.

Accordingly the actor-impact formula above has a verified time factor on
this path: overlap volume in cubic metres, multiplied by the cached
substep seconds and `UnresolvedCollisionDamageMultiplier`, with the
documented absolute value and conversion order. The factor is the supplied
substep duration; this does not equate it to a whole rendered frame's
duration or establish a fixed numerical value for every hit. The opaque
member's original source spelling and every possible writer in other
movement modes remain unclaimed. Those limits no longer prevent naming
the input `StepMs` and this particular cached value as seconds.
