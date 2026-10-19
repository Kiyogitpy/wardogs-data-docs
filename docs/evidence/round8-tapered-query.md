---
title: Round 8 tapered capsule query construction
nav_exclude: true
---

# Tapered elements reach the native geometry builder

Static CL-516586 investigation, 2026-10-18. Instructions were decoded from
the restored executable (SHA-256
`a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`),
with the existing read-only corpus and local UE 5.7 source as navigation.
No game process was started. This follows the earlier
[metadata-only investigation](round8-collision.md#tapered-capsules-metadata-verified-query-construction-still-open).

## Actual element-to-shape loop

`0x423A2C0` is the geometry builder. Instructions `0x423AE8E`–`0x423AEA1`
read its geometry pointer at input `+0x140`, then the tapered array at
geometry `+0x40`, its count at `+0x48`, and compute the end pointer with
stride `0x70`. These match the SDK's `FKAggregateGeom.TaperedCapsuleElems`
and `FKTaperedCapsuleElem` layout. This is an actual consumer, rather
than a type-registration or rendering reference.

Each element calls scaling helper `0x4244430` at `0x423AED1`. The body
clamps the resulting two radii and half length to the small positive
threshold. Its ordinary branch builds endpoints around the scaled center
and rotated half-length axis. Instructions `0x423B03C`, `0x423B06B`,
`0x423B076` add the two clamped radii, multiply by one half, and convert
the result to double for argument `xmm3`. Call `0x423B07A` passes this
mean radius and the two endpoints to constructor `0x21A6160`.

The same constructor is used for ordinary sphyl geometry at
`0x423AD76`. It stores the first endpoint, endpoint difference, segment
length, and radius (`+0x10`) in the implicit object. Thus this builder
approximates a tapered element with a straight capsule whose radius is
the arithmetic mean of its two scaled/clamped radii. It does not create
the Chaos tapered-capsule type merely because that type exists.

This matches local source
`E:/UE_5.7/Engine/Source/Runtime/Engine/Private/PhysicsEngine/Experimental/ChaosInterfaceUtils.cpp`:
line 22 defines `CREATE_STRAIGHT_CAPSULE_GEOMETRY_FOR_TAPERED_CAPSULES`;
lines 194–218 iterate these elements and create `Chaos::FCapsule` with
mean radius. The executable's matching loop and constructor calls provide
the build-specific corroboration; the local source alone would not prove
the shipped configuration.

## Registration and query boundary

After construction the loop reads element collision mode from byte
`+0x19`, calls shape helper `0x422A320`, and appends both shape and
geometry to its output arrays. The helper combines body and element
collision modes, copies query/simulation filter data and sets enabled
bits. Its caller `0x42333F0` invokes the builder at `0x4233453`, applies
shape materials through `0x41E0EA0` and installs the geometry in the
physics actor through `0x2470790` (or its existing-union path).

The matching local source at lines 104–135 names the helper operations:
`SetQueryData`, `SetSimData`, intersection of body/shape collision modes,
and `SetQueryEnabled`. The six player tapered elements serialize
QueryAndPhysics; the player mesh serializes QueryOnly, so their combination
permits queries. Channel acceptance is governed separately by the
[packed CharacterMesh responses](round8-config.md).

Independent review confirmed the native query flag and registration path.
The intersection table at `0xA5FB0F0`, row QueryOnly / column
QueryAndPhysics, returns QueryOnly. Instructions `0x422A600`,
`0x422A612`–`0x422A617` (alternate storage `0x422A645`–`0x422A64A`)
map its query bit into shape bit 1. Registration calls occur at
`0x4233453` (builder), `0x42334EE` / `0x423351E` (materials),
`0x423357C` / `0x42335AF` (union installation), and `0x4233639`
(shape-pointer append).

The upstream callable body starts at **`0x42347D0`**, not the corpus's
`0x42347CA` boundary, which includes a misleading prefix. Actual call
`0x41E86EA` targets `0x42347D0`. Instructions `0x42349FA`–`0x4234A05`
set the geometry parameter to BodySetup `+0x38` (AggGeom); the subsequent
call at `0x4234A42` reaches registration. Thus the tapered array is
BodySetup `+0x78`, as independently predicted by the SDK layout.

The builder's simple-geometry gate (`0x423A37B`–`0x423A392`) requires
not UseComplexAsSimple, or no triangle mesh. This closure establishes
native construction and query capability, not universal acceptance under
every geometry mode, channel response or later runtime override. The
viewer retains authored tapered primitives with an explicit approximation
note; it does not claim to display the runtime mean-radius shape exactly.
