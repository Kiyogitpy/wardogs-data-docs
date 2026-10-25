---
title: "Hit Registration: From Projectile Trace to Damage Event"
redirect_from: ["/Wardogs_HitRegistration_v1.html", "/Wardogs_HitRegistration_v1"]
parent: "Damage & Combat Systems"
description: "How a projectile step becomes a hit: trace shape and channel, ignore lists, ricochet and penetration, the hit-event struct, delivery to the damage pipeline, alignment and impact cues"
---

# Wardogs — Hit registration: from a projectile trace to a damage event

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

What happens between a projectile's per-step movement and the damage event that
[Damage Pipeline](Wardogs_DamagePipeline_v2.md) picks up: which trace is cast and
against what, who is ignored, how a blocking hit turns into a ricochet, a
penetration or a stop, what the resulting hit record contains, how that record
reaches the damage builder, and which impact cue is sent. Flight itself (forces,
integrator, step length) is in [Projectile Flight](Wardogs_ProjectileFlight_v1.md); this page starts where
that page says "sweep a trace" and "detonation is by trace hit".

**Short answer.**

- Bullets are simulated projectiles. Each fixed step the subsystem casts **one line
  trace** from the projectile's position to its next position on **`ECC_Visibility`
  (channel 3)**, with query tag `WeaponTrace`, **complex collision on**, face index and
  physical material returned, and a response container that is Block for every channel
  (§2). Actor-driven projectiles trace through the mover instead, with a sphere/capsule
  sweep that degrades to a line (§2.5).
- No separate hit-scan path was found. The word appears only as a flag in the
  damage-side projectile data (§3).
- A blocking hit goes through one function, `0x6F36F40`: penetration geometry, then a
  ricochet roll, then the penetration step, then the hit record and its cue (§4).
  Ricochet and penetration use a deterministic random stream that is part of the
  replicated simulation state.
- The hit record (`FWDProjectileHitData`, 0x238 bytes) carries the `FHitResult`, the
  impact velocity, the full simulation snapshot and the ricochet and penetration
  history (§5). It is stored on the projectile instance, broadcast, and handed to the
  proxy component's hit handler `0x6B73E90`, which builds the `FWDDamageEventData`
  through `0x6B725B0` (§6).
- Friendly and self hits are not filtered out of the trace. They are damage events
  whose **alignment** is `Friendly` when instigator and target resolve to the same
  8-byte team value; two rows of the infantry rule table then reduce bullet damage by
  half (§6.4).

Build: `++Wardogs+Live-CL-516586` · Engine: UE 5.7 · Native addresses are file RVAs
(image base `0x140000000`).

**Evidence level: static-analysis image; virtualized dispatch not removed.** Everything
below was read with capstone and pefile from the flat executables. The reading copy is
the restored image `WardogsClient-Win64-Shipping.restored.exe` (SHA-256
`a5c3db10…2b4f0cc37`); the static-analysis image was compared byte for byte for every
function cited in §9. All are identical except `0x3C95C30` (the
`FCollisionQueryParams` constructor) and `0x42D9770` (set every channel of a response container), which begin with a protection-layer dispatch
stub in the analysis image and are read from the restored image, as
[IDA claim exposure](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/IDA_CLAIM_EXPOSURE.md)
prescribes. Byte patterns for the main claims are re-checked by
[`_tools/hit_registration_check.py`](../_tools/hit_registration_check.py). No game was
run and no process was observed; nothing here is a runtime measurement.

| Label | Meaning |
|---|---|
| **Native** | Read from instructions or constants in the executable; RVA cited |
| **Config** | Read from the packed `Wardogs/Config/*.ini` (the same extraction the [packed-configuration evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round8-config.md) uses) |
| **Data** | Read from the cooked export under `data/` |
| **SDK** | Class or struct layout from `sdk/raw` |
| **Derived** | Follows from the above by arithmetic or by the stock Unreal Engine definition of a type |
| **Open** | Not established; §10 lists what would close it |

---

## At a glance

| Stage | Status | Section |
|---|---|---|
| Trace shape, channel, query parameters | **Native** | §2.1–2.2 |
| What the trace can hit (channels, collision profiles, character capsule vs mesh) | **Config** + **Native** | §2.3 |
| Ignored actors and components | **Native**, partly **Open** | §2.4 |
| Actor-driven (mover) trace | **Native**, shape source **Open** | §2.5 |
| Complex vs simple collision | **Native** | §2.6 |
| Hit-scan | No path found | §3 |
| Impact function, ordering of ricochet, penetration, stop | **Native** | §4.1 |
| Ricochet probability and reflection | **Native** + **Config** | §4.3 |
| Penetration | **Native**, formulas in the linked evidence page | §4.4 |
| Surface and projectile parameter tables | **Config** + **Data** | §4.6–4.7 |
| Hit record, history bitmaps, storage, broadcast | **Native** + **SDK** | §5 |
| Delivery to the damage builder, eligibility | **Native** | §6.1–6.3 |
| Alignment (friendly fire, self hit) | **Native** + **Data** | §6.4 |
| Bone and vehicle-section resolution | **Native**; detail in linked pages | §6.5 |
| Client, server, replay, random stream | **Native** (flow only), server-side handling not documented here | §7 |
| Impact cue and decal selection | cue dispatch **Native**; selection **Open** | §8 |

---

## 1. The path in one view

```text
UWDProjectileSubsystem::Tick 0x6F3BC70           fixed step, floor(1000/Rate) ms        (Projectile Flight §3)
 -> 0x6F3D130 -> 0x6F3CB80 -> 0x6F3C060          substep: forces, d = (v0+v1)/2 * dt
      if inst+0x25C == 0 and any |d_i| > 1e-4:
          world = 0x4529050(subsystem)
          0x3CAB670(world, &hit, Start = inst.Location, End = Start + d,
                    ECC_Visibility(3), Params = inst+0x140, ResponseParams = inst+0x1B8)   @0x6F3C75A
      progress += |d| * hit.Time ; elapsed += dt * hit.Time
      if hit.bBlockingHit (hit+0xAD bit 0):
          0x6F36F40(subsystem, inst, &hit, &previousVelocity)                         @0x6F3C8C1
              location := hit.Location ; velocity := previous + (new - previous) * hit.Time
              0x6F2F740  penetration geometry (exit trace 0x6F2FC20, thickness, capacity)
              0x6F36600  ricochet roll, unless the exit result forced a decision
              0x6F36190  penetration step (only if no ricochet and the target allows it)
              0x6F353F0  hit record: bitmaps, HitCount++, copy to inst+0x2E8, broadcast,
                         hand-off to the proxy component 0x6B73E90 (or cue-only path)
              neither ricochet nor penetration: cue 0x6F380A0, velocity := 0, end 0x6F342B0
 proxy component 0x6B73E90(hit, inst)
      0x6B721B0   is this hit eligible to damage?          (§6.2)
      0x6B73500   CustomHitResults                          (§6.3)
      0x6B725B0   build FWDDamageEventData, ModifyDamage    (Damage Pipeline §7.6)
      0x6B717C0   post-damage cue and hit-marker data
```

**Native.** All RVAs above are file RVAs in the restored image; §9 lists each function and
whether the analysis image matches.

---

## 2. The trace

### 2.1 Shape and call

**Native.** The integrator `0x6F3C060` casts `0x3CAB670` at `0x6F3C75A`. The arguments
are set up by the instructions before it:

| Argument | Value | Instruction |
|---|---|---|
| world | `0x4529050(subsystem)` | `0x6F3C723` |
| out hit | local `FHitResult` (0x100 bytes) | `0x6F3C744` |
| start | the instance's current location (`inst+0x08`, three doubles) | `0x6F3C59A` |
| end | start + displacement; displacement is the trapezoid `(v_old + v_new)/2 * dt` (factor 0.5 from `0x9AADA60`), after the range limiter `0x76DF9A0` | `0x6F3C4C7`–`0x6F3C540` |
| trace channel | **3** (`mov dword [rsp+0x20],3`) | `0x6F3C74B` |
| query parameters | instance `+0x140` | `0x6F3C734` |
| response parameters | instance `+0x1B8` | `0x6F3C72F` |

`0x3CAB670` forwards to `0x3CAE910`, the world's single-line-trace-by-channel entry; the
wrapper adds the stock default object-query parameters (global `0xD279A10`) as a last
argument. This is a **line trace**: there is no shape argument, no rotation and no radius.
The channel number is 3, which the SDK's `ECollisionChannel` names **`ECC_Visibility`**
([`Engine_structs.hpp`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/sdk/raw/Engine_structs.hpp#L507)).

The trace is skipped when instance byte `+0x25C` is non-zero (`0x6F3C713`) and when no
displacement component exceeds `1e-4` (double at `0x9AD4600`, tests at `0x6F3C577`–`0x6F3C594`).
Byte `+0x25C` is zero in the instance constructor (`0x6B8E3AD`, dword `0x01010100` at `+0x25C`) and
nothing in the projectile code was found to set it; it is only copied with the instance.

After the trace, `|d_i| * hit.Time` is added to the instance's absolute-move vector
(`+0x40..0x50`) and `dt * hit.Time` to elapsed time (`+0x290`); a blocking hit then calls the
impact function (`0x6F3C8C1`). The impact function receives the previous velocity so that the
velocity at the point of impact is the linear interpolation by `hit.Time`.

### 2.2 Query parameters

**Native.** The instance constructor `0x6B8E100` builds the two parameter blocks once per
projectile (the spawn path `0x6F39940` builds the same pair for its local copy):

| Block | Construction | Result |
|---|---|---|
| `inst+0x140` | `0x3C95C30(this, TraceTag = global 0xD367EE0, bInTraceComplex = 1, IgnoreActor = null)` at `0x6B8E2F4`–`0x6B8E301`; the `FName` global is initialised from the string `"WeaponTrace"` (`0x6B8E4A8`) | query tag `WeaponTrace`; **trace complex = true**; initial-overlap flag at its stock default (1) |
| `inst+0x140` + `0x12` | word `0x0101` stored by the instance initialiser `0x6F30F70` | **return face index = true**, **return physical material = true** |
| `inst+0x1B8` | `0x42AF7C0` (default response params) then `0x42D9770(this, 2)` | the response container is **Block for every channel** |

Field names follow the stock `FCollisionQueryParams` field order (**Derived**: the constructor `0x3C95C30`
writes `TraceTag` at `+0`, the complex flag at `+0x10`, and the later flag bytes at the offsets the stock
layout gives them). Because the response container is all-Block, the container does not narrow the trace; what
the trace can hit is decided by each object's own response to channel 3 (§2.3).

### 2.3 What the trace can hit

**Config.** The packed `DefaultEngine.ini` defines 18 project trace and object channels
(lines 749–766; `GameTraceChannelN` is enum value 13 + N):

| Enum | Name | Default response | Trace type |
|---:|---|---|---|
| 0 | WorldStatic | Block | object |
| 1 | WorldDynamic | Block | object |
| 2 | Pawn | Block | object |
| **3** | **Visibility** | Block | trace (**the projectile line trace**) |
| 4 | Camera | Block | trace |
| 5 | PhysicsBody | Block | object |
| 6 | Vehicle | Block | object |
| 7 | Destructible | Block | object |
| 14 | WDVehicleCamera | Block | |
| 15 | WDBuildablePlacement | Overlap | trace |
| 16 | WDRotor | Overlap | |
| 17 | SpatialTracker | Ignore | trace |
| 18 | WDAimAssist | Ignore | trace |
| 19 | FluidTrace | Ignore | trace |
| 20 | AudioOcclusion | Ignore | trace |
| 21 | **WDProjectile** | Block | object |
| 22 | WDMeleeHit | Block | |
| 23 | Landscape | Ignore | trace |
| 24 | WDWaterBody | Block | |
| 25 | WDImpulseResonance | Ignore | trace |
| 26 | Ping | Ignore | trace |
| 27 | WDExplosive | Block | |
| 28 | WDSmashableWindow | Block | |
| 29 | VisibilityNoPawn | Ignore | trace |
| 30 | Ragdoll | Block | |
| 31 | WDDroppedItem | Block | |

Enum values 8–13 (`EngineTraceChannel1..6`) are unused. Two channels are relevant to bullets and they
are **not interchangeable**: the native line trace asks every object "do you block `Visibility`?", while
`WDProjectile` is the object type of the `ProjectileSweep` profile (§2.5). The collision profiles
treat them differently:

| Profile (object type) | `Visibility` | `WDProjectile` | Consequence for the line trace |
|---|---|---|---|
| `Pawn` (stock profile) | Ignore | Block | not stopped |
| `CharacterMesh` | Block | Block | the skeletal-mesh bodies stop it |
| `Ragdoll` | Block | Ignore | stops the trace |
| `WDVehiclePhysics` | Block | Ignore | stops the trace |
| `WDVehicleComplex` (QueryOnly) | Block | Block | stops it; the complex mesh is the hit surface |
| `VehiclePhysicsProxy` (PhysicsOnly) | Ignore | Ignore | never queried |
| `InvisibleWall`, `InvisibleWallDynamic`, `BHDemolitionBushes` | Ignore | Ignore | invisible to bullets and to the sweep |
| `WDDroppedItem`, `WDTraversal`, `WDVehicleWeaponPhysics*` | Ignore | Ignore | invisible to bullets |
| `WDForwardOperatingBase` | Block | Ignore | stops the trace |
| `WDBarbedWire` | Block | Overlap | stops the trace |

Rows come from the `Profiles`/`EditProfiles` lines 677–790 of the packed `DefaultEngine.ini`
(removals applied). Profiles whose collision mode is `NoCollision` or `PhysicsOnly` are not queried by a
line trace at all.

**Character capsule and mesh.** **Native + Config.** The mover character's constructor `0x6E67160`
sets the capsule's response to channel 3 (Visibility) to Ignore (`0x6E67CCD`); the mesh takes profile
`CharacterMesh` (`0x6E67D25`), whose packed definition blocks Visibility
([details](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round8-config.md)).
A bullet therefore registers on the **physics-asset bodies** of the mesh, not on the capsule, which is why a
hit carries a bone: `FHitResult.BoneName` (`+0xF0`) is the body's bone. Whether the six tapered-capsule
bodies are registered as query shapes is still [open](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round8-collision.md)
(O-2).

### 2.4 Ignored actors and components

**Native.** After a projectile is spawned, `0x6F37510` fills the instance's `FCollisionQueryParams`
(`inst+0x140`) from its proxy component (weak pointer at `inst+0x104`):

1. the proxy component's owning actor (`proxy+0xC8`, the shooter's character) with
   `AddIgnoredActor` (`0x3C9B230`);
2. the proxy's `GetIgnoredActors` (vtable slot `0x530`, `0x6B73810`; the exec thunk `0x69E8F70` calls that slot) with the
   array-add helper `0x3C9B290`. The slot forwards to an interface object held at `proxy+0xEC` (its slot `+0x110`); with no such
   object it returns the owning character (slot `0x510`) and one object derived from it by `0x6E6EE40` (not identified);
3. the proxy's `GetIgnoredComponents` (slot `0x528`, `0x6B73940`; thunk `0x69E8FF0`) with the array-add helper `0x3C9B420`. The slot forwards
   to the same interface object (its slot `+0x108`); with no such object it returns an empty array;
4. the object in the weak pointer at `inst+0x120`, if valid, with `AddIgnoredActor`. That pointer is the projectile's own actor (**Inferred**: the hit handler passes it to `GetOwningController(const AWDProjectile*)`, and the cue code uses it as the effect causer), so an actor-driven projectile does not block its own trace;
5. when instance byte `+0x28D` is set (it is 1 after the constructor: word `0x0100` at `+0x28C`, `0x6B8E3C8`), `0x6F37750`
   runs a vehicle-related check (instigator's seated vehicle, a direction test against -0.8 and a gameplay-tag test through
   the character's tag owner at `+0x620`) that can set `inst+0x129`; the consumer of that byte was not located.

On the fire side, when a projectile's `IgnoreInstigatorVehicleTime` (stats `+0x2E4`) is greater than 0, the
weapon fire path (`0x6B937D0`) appends the shooter's seated vehicle (`0x6E6EBA0`) to the spawn request's
ignore list. How the time value limits that ignore after spawning was not located (O-9). The cooked values
are in §4.7.

Class-level rules that are not part of the query: `ImpactIgnoreAngleClasses` (§4.4) and the
penetration-history ignore list (§4.6).

### 2.5 Actor-driven projectiles (mover trace)

**Native.** An instance with `bActorHandlesProjectileMovement` is not integrated by the subsystem. Its
`UWDProjectileMove` simulation tick `0x76D9110` traces instead: it copies the instance's query parameters
(`0x3C95AB0`), replaces the tag with the `FName` initialised from `"Trace_Mover_Projectile"`, takes the
response parameters from the stock default (`0xD2799F0`), and calls `0x3CB56B0` with trace channel **3**
(`mov dword [rsp+0x28],3` at `0x76D9679`) and a collision shape obtained through a virtual call
(slot `0x8B0`, `0x76D963E`). `0x3CB56B0` switches on the shape type; a sphere or capsule whose
extent is at most `1e-4` (float at `0x9AAD9D0`, compare at `0x3CB56F5`) is handled as a degenerate shape and
falls to the line path of §2.1; anything larger is a swept-shape query. On a blocking hit it pulls the hit time back by a small
margin (about `0.1 / length` of the sweep, capped, plus `0.001`, `0x76D96E8`–`0x76D9706`) and calls the same impact function
`0x6F36F40` (`0x76D97A8`).

[SDK] `AWDProjectile` has `SweepProfileName` (`+0x2F8`), and the packed config defines a profile **`ProjectileSweep`**
(object type `WDProjectile`, `NoCollision`, "Profile for sweeping mover projectiles"; it ignores Camera,
WDVehicleCamera, WDBuildablePlacement, WDRotor, WDProjectile, WDMeleeHit, WDWaterBody, WDExplosive and
WDSmashableWindow). The shipped Blueprint default of `SweepProfileName` is not in `data/`, and the native
tick passes channel 3 and the stock response parameters rather than a profile, so which query actually uses
`ProjectileSweep` is **Open** (O-1).

### 2.6 Complex vs simple collision

**Native.** The query is complex (`bTraceComplex` true, §2.2) and returns the face index. Against a mesh
that has complex-as-simple or per-triangle collision the trace result is therefore the triangle; the vehicle
pages rely on that (the `WDVehicleComplex` profile, §2.3, is the vehicle's queryable surface; section routing
in §6.5). Characters are simple physics-asset bodies (20 bodies; see the [hit-box data](../assets/data/infantry-hitboxes.json)).
The mover sweep of §2.5 is a shape query and uses the simple representation.

---

## 3. Hit-scan vs projectile

**Native + SDK.** No hit-scan path was found in the code that fires and simulates bullets: the fire path
`0x6F1DDC0` builds a spawn request for the projectile subsystem (launch speed from the weapon's
`InitialBulletSpeed`, [Projectile Flight §2](Wardogs_ProjectileFlight_v1.md)), and the subsystem owns every
step. Two things look like hit-scan but are not:

- `FWDAdditionalDamageData_Projectile` (SDK, 0x0C bytes: `ProjectileIndex`, `bPenetrated`, `bPenetrationForced`,
  `bIsHitScan`, `fireid`) has a hit-scan flag. The only writer found is `0x6B71254`'s function, which stores
  `bPenetrationForced` from stats `+0x205` (`bForcePenetrateThinSurfaces`) and `bIsHitScan` as the result of a
  byte compare (`sete`) on a context byte at `+0x2DA`; the meaning of that byte is **Open** (O-7).
- `UWDWeaponBehaviorComponent` (SDK) has `MuzzleTraceDistance`, `MuzzleTraceChannel` and
  `MuzzleTraceInterval` and caches a `CachedMuzzleHitResult`. That is a wall-collision check for the weapon
  (`GetWallCollisionAlpha`), not a shot.

The packed config's `SimulationFrameRate` (§4.6) is 30, so a projectile advances in `floor(1000/30)` = 33 ms
substeps; a very fast round is still stepped, not resolved instantly. Whether every weapon in the game uses the
projectile subsystem was not checked weapon by weapon.

---

## 4. Impact processing

### 4.1 Order inside `0x6F36F40`

**Native.** Arguments: subsystem (`rcx`), instance (`rdx`), `FHitResult*` (`r8`), previous velocity (`r9`).

| Step | What | RVA |
|---|---|---|
| 1 | `inst.Location := hit.Location` (`hit+0x10`); `inst.Velocity := previous + (new - previous) * hit.Time` | `0x6F36F5A`–`0x6F36FE1` |
| 2 | Debug text ("HitT", "ImpactVelocity", m/s) when the debug flag `0xD38145D` is set | `0x6F36FEA`–`0x6F371EB` |
| 3 | Penetration geometry: `0x6F2F740` fills a result block (thickness, effective thickness, angle, capacity, effectiveness, exit hit) | `0x6F372A3` |
| 4 | Ricochet roll `0x6F36600`, skipped when the penetration block's actor-override byte (`+0x118`) is set | `0x6F372C1`–`0x6F372D6` |
| 5 | If not ricocheted: when the hit actor implements `IWDDamageable`, its slot `+0x68` decides whether penetration is attempted; with no interface it is attempted. On `AWDMoverCharacter` the slot is `0x6E6BD40`: it hands the question to the object at character `+0x118` (`0x6B54AE0`, not decoded) and answers true when there is none. The attempt is `0x6F36190` | `0x6F372ED`–`0x6F3733E` |
| 6 | If penetrated, the material is compared with the penetration-history ignore list (§4.6); a match clears the "record penetration" argument | `0x6F3736C`–`0x6F37421` |
| 7 | Hit record `0x6F353F0` (§5) | `0x6F37477` |
| 8 | Neither ricochet nor penetration: terminal cue `0x6F380A0` with tag global `0xD381600` (skipped when the caller's fifth argument is true), then `inst.Location := hit.ImpactPoint` (`+0x28`), `Velocity := 0`, end of flight `0x6F342B0` | `0x6F374A1`–`0x6F374EA` |

The snapshot of the velocity passed to the hit record in step 7 is the **pre-exit** `ImpactVelocity`; exit losses
affect only later hits ([downstream trace](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round8-physical-material-downstream.md)).

### 4.2 Penetration decision (`0x6F2F740`)

**Native.** A penetration is considered when the projectile's `bShouldPenetrate` (stats `+0x204`) is set, or when
the hit actor has bit 3 of its flag byte `+0x62` set (a replication-related actor flag; not verified by name) and its `IWDDamageable` slot `+0x60` returns true (the result is stored in the
block's actor-override byte `+0x118`, `0x6F2F92B`). On `AWDMoverCharacter` slots `+0x38` and `+0x60` are the shared stub `0x1563050` (`xor al,al`), so
for characters the override is never set and `bShouldPenetrate` alone decides. It then runs the exit query `0x6F2FC20` (material response Disabled /
Planar / Default; geometry exit trace for Default), computes the angle between the impact normal and the incoming
direction, and calls `0x6F2FB30` with the larger of the entry and exit material densities. The
angle is forced to 0 when the hit actor's class is in `ImpactIgnoreAngleClasses` (`WDMoverCharacter`,
`WDTargetDummy`; list at subsystem `+0x430`, `0x6F2F9DE`–`0x6F2FA76`). Formulas for thickness, capacity and the
exit-speed update are in the
[downstream trace](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round8-physical-material-downstream.md)
and are not repeated here.

### 4.3 Ricochet (`0x6F36600`)

**Native.** Conditions and arithmetic, in order:

1. the hit has a valid physical material (`hit+0xB0`), and the current speed (`inst+0x20`) is at least `0.1` times the launch speed
   (`inst+0x88`, the initial velocity copied from the spawn request; `0x6F36649`–`0x6F366B9`);
2. the impact angle in degrees, measured from the surface normal (0° is head-on; `acos` of the normal dot the reversed direction
   from the penetration block), is **at least** `MinImpactAngleForRicochet` (stats `+0x214`; `0x6F366E8`). A hit on the front face gives at most 90°, so a minimum of 91 or
   more switches ricochet off in practice (§4.7);
3. probability `p` starts at 1.0 and is replaced by `PhysMatRicochetProbabilities[surface]` when the map has the surface
   (`0x6F36733`–`0x6F3673D`; map at subsystem `+0x320`, key = material `SurfaceType`, `material+0x60`);
4. `p` is multiplied by the value of every `ImpactAngleRicochetProbabilities` bin `[min, max]` that contains the angle
   (map at subsystem `+0x370`, `0x6F368E0`–`0x6F36915`);
5. `p` is multiplied by `t = clamp((effectiveness - X) / (Y - X), 0, 1)` with `(X, Y)` =
   `PenetrationEffectivenessRicochetProbabilities` (subsystem `+0x3C0/+0x3C4`; effectiveness = capacity / thickness from
   the penetration block, `+0x10`); if `|Y - X|` is below `1e-8`, `t` is 1 or 0 by comparing effectiveness with `Y`
   (`0x6F36928`–`0x6F3697E`);
6. the roll: the instance's random seed (`inst+0xD0`) is advanced with the stock `FRandomStream` step
   `seed * 196314165 + 907633515` (`0x6F36982`–`0x6F3699A`), the high 23 bits become a fraction in [0, 1)
   (`shr 9`, `or 0x3F800000`, minus 1), and the projectile **ricochets when `p * t` is strictly greater than the fraction**
   (`0x6F369B5`).

On success: the reflected direction is built around the surface normal with a random cone of at most
`MaxRicochetAngleVariance` (`+0x418`, converted to radians by `0x9AAFD70`) via `0x3FD4C50`; the new speed is the old speed times a
random lerp inside `PhysMatRicochetRestitutionCoefficient[surface]` (`Min`, `Max`; map at `+0x3C8`; `0x6F36D6F`–`0x6F36DC8`),
with a further random scaling from `MaxDeflectionPercentage{Shallow,Sharp}Angle` (`0x6F36BB2`–`0x6F36C88`); the
ricochet cue `0x6F380A0` is sent with tag global `0xD3815F0`; and, if the debug byte `inst+0x260` is set, an arc record is
appended to the debug array at `inst+0x268`.

With the packed values (§4.6) effectiveness 2 or more gives `t = 0`, so a round whose capacity is at least twice the
thickness never ricochets; effectiveness 1 or less gives `t = 1`; in between `t = 2 - effectiveness`.

### 4.4 Penetration step (`0x6F36190`)

**Native.** Summary of the [downstream trace](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round8-physical-material-downstream.md):
it needs the exit hit to be blocking (`result+0xC5` bit 0) and, unless the actor-override byte (`+0x118`) is set, `capacity > effective thickness`
and thickness at least `0.01` (`0x6F361B2`–`0x6F361F3`). The new velocity is
`old * (1 - thickness/capacity) * clamp(1 - 0.5 * (p + s), 0, 1)` with `p` = stats `PenetrationExitSpeedMultiplier`
(`+0x20C`) and `s` = `PenetrationPhysMatExitSpeedModifiers[entry surface]`. The exit point is nudged along the direction and a random
angular deflection is applied (`ExitDeflection*` in §4.6; distribution not re-derived). `bForcePenetrateThinSurfaces` (stats `+0x205`) is
not read by this function; its only reader found is the damage-side struct writer of §3.

### 4.5 Hit count and history

**Native.** `0x6F353F0` keeps a 16-bit hit counter at `inst+0x118` and two 16-bit bitmaps: ricochet at `+0x11A`, penetration at `+0x11C`.
At each hit, the bit number `HitCount` is set in the ricochet bitmap when the hit ricocheted (`0x6F354DD`–`0x6F354EE`), or in the
penetration bitmap when it penetrated and the history argument is true (`0x6F354F7`–`0x6F35516`); then `HitCount` is incremented
(`0x6F3551D`). Because the bitmaps are 16 bits wide, only the first 16 hits of a projectile are recorded in them. (Round 39, disassembly: the bit is set with `bts ecx, eax` on a zero-extended 16-bit load and stored back with `mov word [rdi+0x11A]`/`[rdi+0x11C]`. `bts` with a register bit offset takes it modulo 32, so hits 17 to 32 set a bit above bit 15 that the 16-bit store drops, and hit 33 sets bit 0 again. The counter at `+0x118` is incremented by `inc word` at `0x6F3551D`.) No other upper limit
on the number of hits was found: a projectile ends when a hit is neither a ricochet nor a penetration, when its speed or capacity runs out,
or at its lifetime.

### 4.6 Projectile system settings

**Config.** `[/Script/WDGame.WDGameSettings] ProjectileSystemSettings` in the packed `DefaultGame.ini` (line 303). The settings struct is copied
to subsystem `+0x2A0` ([evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round8-physical-material-downstream.md)); the
consumer offsets quoted in §4.2–4.4 are `+0x2A0` plus the SDK field offsets of
[`FWDProjectileSystemSettings`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/sdk/raw/WDGame_structs.hpp#L17969).

| Setting | Value | Consumer |
|---|---|---|
| `SimulationFrameRate` | **30** (step `floor(1000/30)` = 33 ms) | subsystem `+0x444`, [Projectile Flight §3](Wardogs_ProjectileFlight_v1.md) |
| `PenetrationEffectivenessRicochetProbabilities` | X = 2.0, Y = 1.0 | §4.3 step 5 |
| `ImpactAngleRicochetProbabilities` | 0–10°: 0.08; 10–20°: 0.18; 20–30°: 0.30; 30–40°: 0.42; 40–50°: 0.55; 50–60°: 0.67; 60–70°: 0.78; 70–80°: 0.87; 80–90°: 0.92 | §4.3 step 4 |
| `MaxRicochetAngleVariance` | 40° | §4.3 |
| `MaxDeflectionPercentageShallowAngle` | Min 0.2, Max 10.0 | §4.3 |
| `MaxDeflectionPercentageSharpAngle` | Min 0.2, Max 0.8 | §4.3 |
| `ExitDeflectionPenetrationEffectivenessRange` | X = 5.0, Y = 0.5 | §4.4 |
| `ExitDeflectionAngleRange` | 0°–7.5° | §4.4 |
| `ImpactIgnoreAngleClasses` | `WDMoverCharacter`, `WDTargetDummy` | §4.2 |
| `MaxPelletCount` | 16 | consumer not traced (O-11) |
| `MaxConsecutiveFullRefundedSubsteps` | 10 | consumer not traced (O-11) |
| `PenetrationPhysMatIgnoreList` | `PM_MetalChainLink`, `PM_GlassBulletProof`, `PM_Glass`, `PM_Glass_1cm`, `PM_VehicleCC_GlassBulletProof`, `PM_VehicleCC_Glass_Solid`, `PM_VehicleCC_Glass`, `PM_VehicleCC_ArmoredGlass`, `PM_VehicleCC_Reinforced_GlassBulletProof`, `PM_VehicleCC_StrongGlass`, `PM_Body`, `PM_Head`, `PM_VehicleCC_Glass_Humvee` | §4.1 step 6: such a penetration is not written to the penetration history bitmap (the velocity loss still happens) |

Per surface type (`PenetrationPhysMatExitSpeedModifiers`, `PhysMatRicochetProbabilities`,
`PhysMatRicochetRestitutionCoefficient`; the names are the `+PhysicalSurfaces` entries of the packed `DefaultEngine.ini`
lines 634–671):

| SurfaceType | Name | Exit-speed modifier | Ricochet probability | Restitution (Min-Max) |
|---:|---|---:|---:|---|
| 0 | Default | 0 | 0.3 | 0.25–0.45 |
| 1 | Asphalt | 0.15 | 0.4 | 0.2–0.4 |
| 2 | Bark | 0.1 | 0.25 | 0.1–0.25 |
| 3 | Body | 0 | 0 | 1–1 |
| 4 | Brick | 0.3 | 0.25 | 0.15–0.35 |
| 5 | Ceramic | 0.35 | 0.55 | 0.2–0.4 |
| 6 | Chemical | 0.1 | 0.05 | 0.05–0.2 |
| 7 | Coal | 0.25 | 0.2 | 0.2–0.4 |
| 8 | Concrete | 0.4 | 0.35 | 0.25–0.5 |
| 9 | Debris | 0.25 | 0.4 | 0.15–0.5 |
| 10 | Dirt | 0.2 | 0.08 | 0.05–0.15 |
| 11 | Electrical | 0.1 | 0.2 | 0.2–0.45 |
| 12 | Fabric | 0.05 | 0.02 | 0.1–0.15 |
| 13 | Fur | 0.05 | 0 | 0.1–0.15 |
| 14 | Glass | 0.05 | 0.1 | 0.15–0.4 |
| 15 | Grass | 0.05 | 0.1 | 0.05–0.15 |
| 16 | Gravel | 0.25 | 0.45 | 0.15–0.35 |
| 17 | Head | 0 | 0 | 1–1 |
| 18 | Ice | 0.15 | 0.8 | 0.5–0.85 |
| 19 | Lava | 0.9 | 0 | — |
| 20 | Leaf | 0.05 | 0 | 1–1 |
| 21 | Limestone | 0.3 | 0.6 | 0.25–0.5 |
| 22 | Marble | 0.35 | 0.65 | 0.35–0.6 |
| 23 | Metal | 0.4 | 0.45 | 0.35–0.65 |
| 24 | Mirror | 0.35 | 0.15 | 0.1–0.25 |
| 25 | Moss | 0.05 | 0.05 | 0.1–0.15 |
| 26 | Oil | 0.9 | 0.05 | 0.05–0.15 |
| 27 | Paper | 0.05 | 0.02 | 0.1–0.15 |
| 28 | Plaster | 0.25 | 0.2 | 0.15–0.35 |
| 29 | Rock | 0.35 | 0.5 | 0.35–0.55 |
| 30 | Rubber | 0.1 | 0.4 | 0.1–0.25 |
| 31 | Sand | 0.25 | 0.02 | 0.03–0.1 |
| 32 | Snow | 0.1 | 0.03 | 0.03–0.1 |
| 33 | Soil | 0.2 | 0.12 | 0.08–0.2 |
| 34 | Water | 0.9 | 0 | 0.35–0.6 |
| 35 | Wood | 0.15 | 0.3 | 0.15–0.35 |
| 36 | Plastic | 0.12 | 0.4 | 0.2–0.45 |
| 37 | NonRicochetable | 0.15 | 0.1 | 1–1 |
| 38 | BulletProofGlass | 1 | 0.1 | 0.15–0.4 |
| 39–62 | (unnamed) | 0 | 0.5 | 0.4–0.6 |

Which physical material has which surface type is a property of the `PM_*` assets, which are not in `data/`; only
`PM_Head` (SurfaceType17, density 0.2) and `PM_Body` (SurfaceType3) are documented, in the
[collision evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round8-collision.md).

### 4.7 Projectile parameters (cooked)

**Data.** Hit-relevant fields of every `ProjectileStats` in the export (37 assets). A `*` marks a field that is absent
from the cooked asset, so the value is the native constructor default (`0x699DEE0`): penetrate **on**,
force-thin **off**, penetration effectiveness **1.0**, exit-speed multiplier **0**, minimum ricochet angle **10°**,
pellets **1**, own-vehicle ignore **0 s**. "Actor proj." shows `bUseProjectileActor` / `bActorHandlesProjectileMovement`.
Ricochet angle 91 (or more) can never be met (§4.3), so those rounds never ricochet.

| Asset | Penetrate | Force thin | PenEff | ExitSpd | Ricochet min deg | Actor proj | Pellets | Ignore own vehicle s |
|---|---|---|---:|---:|---:|---|---:|---:|
| [`DA_120x570mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/120x570mm/DA_120x570mm_ProjectileData.json) | F | F* | 1* | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_120x800mm_Standard_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/120x800mm/DA_120x800mm_Standard_ProjectileData.json) | F | F* | 1* | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_122_mm_HAVOC_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/122mm/DA_122_mm_HAVOC_ProjectileData.json) | F | T | 2 | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_122mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/122mm/DA_122mm_ProjectileData.json) | F | T | 2 | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_125x570mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/125x570mm/DA_125x570mm_ProjectileData.json) | F | F* | 1* | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_12g_RifledSlug_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/7mm_Buckshot/DA_12g_RifledSlug_ProjectileData.json) | T* | F* | 1* | 0.12 | 10* | F | 1* | 0* |
| [`DA_155mm_Expensive_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/155mm/DA_155mm_Expensive_ProjectileData.json) | F | F* | 1* | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_155mm_Expensive_ProjectileData_SB`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/155mm/DA_155mm_Expensive_ProjectileData_SB.json) | F | F* | 1* | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_155mm_Standard_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/155mm/DA_155mm_Standard_ProjectileData.json) | F | F* | 1* | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_155mm_Standard_ProjectileData_SB`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/155mm/DA_155mm_Standard_ProjectileData_SB.json) | F | F* | 1* | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_20x102mm`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/20x102mm/DA_20x102mm.json) | T* | F* | 1.8 | 0* | 91 | F | 1* | 0.5 |
| [`DA_308Winchester_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/308Winchester/DA_308Winchester_ProjectileData.json) | T* | F* | 1* | 0.13 | 10* | F | 1* | 0* |
| [`DA_30mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/30mm/DA_30mm_ProjectileData.json) | T* | F* | 2 | 0* | 85 | F | 1* | 0.5 |
| [`DA_338Norman_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/338NormanMagnum/DA_338Norman_ProjectileData.json) | T* | F* | 1* | 0* | 10* | F | 1* | 0* |
| [`DA_35x228mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/35x228mm/DA_35x228mm_ProjectileData.json) | T* | F* | 0.75 | 0* | 91 | F | 1* | 0.5 |
| [`DA_40mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/40mm/DA_40mm_ProjectileData.json) | F | T | 1* | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_45ACP_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/45ACP/DA_45ACP_ProjectileData.json) | T* | F* | 1* | 0.32 | 10* | F | 1* | 0* |
| [`DA_45Colt_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/45Colt/DA_45Colt_ProjectileData.json) | T* | F* | 1* | 0.3 | 10* | F | 1* | 0* |
| [`DA_50AE_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/50AE/DA_50AE_ProjectileData.json) | T* | F* | 1* | 0.08 | 10* | F | 1* | 0* |
| [`DA_50Cal_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/50Cal/DA_50Cal_ProjectileData.json) | T* | F* | 3.5 | 0.05 | 10* | F | 1* | 0* |
| [`DA_545mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/545mm/DA_545mm_ProjectileData.json) | T* | F* | 1* | 0* | 10* | F | 1* | 0* |
| [`DA_556mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/556mm/DA_556mm_ProjectileData.json) | T* | F* | 1* | 0.18 | 10* | F | 1* | 0* |
| [`DA_70mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/70mm/DA_70mm_ProjectileData.json) | F | F* | 1* | 0* | 100 | F | 1* | 0.5 |
| [`DA_72mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/72mm/DA_72mm_ProjectileData.json) | F | T | 1* | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_762mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/762mm/DA_762mm_ProjectileData.json) | T* | F* | 1* | 0.15 | 10* | F | 1* | 0* |
| [`DA_762x51mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/726x51mm/DA_762x51mm_ProjectileData.json) | T* | F* | 1* | 0* | 10* | F | 1* | 0* |
| [`DA_762x54mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/762x54mm/DA_762x54mm_ProjectileData.json) | T* | F* | 1* | 0.14 | 10* | F | 1* | 0* |
| [`DA_7mmBuckshot_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/7mm_Buckshot/DA_7mmBuckshot_ProjectileData.json) | T* | F* | 1* | 0.28 | 10* | F | 8 | 0* |
| [`DA_84mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/84mm/DA_84mm_ProjectileData.json) | F | T | 1* | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_93mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/93mm/DA_93mm_ProjectileData.json) | F | T | 1* | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_9mm_ProjectileData`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/9mm/DA_9mm_ProjectileData.json) | T* | F* | 1* | 0.35 | 10* | F | 1* | 0* |
| [`DA_Arrow_Combat_ProjectileData`](../data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/Data/DataAssets/Arrow/DA_Arrow_Combat_ProjectileData.json) | T* | T | 0.5 | 0.55 | 30 | F | 1* | 0* |
| [`DA_Arrow_Explosive_ProjectileData`](../data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/Data/DataAssets/Arrow/DA_Arrow_Explosive_ProjectileData.json) | F | T | 1* | 0* | 50 | F | 1* | 0.5 |
| [`DA_BatteryCharge_ProjectileData`](../data/Wardogs/Plugins/GameFeatures/Items/Battery/Content/Data/DA_BatteryCharge_ProjectileData.json) | T* | F* | 1* | 0* | 10* | F | 1* | 0* |
| [`DA_DebugHomingRocketData`](../data/Wardogs/Content/Items/Resources/Ammo/DebugHomingRocket/DA_DebugHomingRocketData.json) | F | F* | 1* | 0* | 91 | F | 1* | 0* |
| [`DA_Drone_ProjectileData`](../data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/Data/Projectile/DA_Drone_ProjectileData.json) | F | F* | 1* | 0* | 91 | T/T | 1* | 0.5 |
| [`DA_TVGuidedMissile_Data`](../data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/DA_TVGuidedMissile_Data.json) | F | F* | 1* | 0* | 85 | T/T | 1* | 0.5 |

---

## 5. The hit record

**SDK + Native.** `FWDProjectileHitData` (0x238 bytes,
[`WDGame_structs.hpp`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/sdk/raw/WDGame_structs.hpp#L5211)) is built by
`0x6F353F0` and consumed by the proxy component, the damage builder and the cue code.

| Offset | Field | Written from | Notes |
|---|---|---|---|
| `+0x000` | `HitResult` (`FHitResult`, 0x100) | the trace result, copied at `0x6F35640` | `Time +4`, `Location +0x10`, `ImpactPoint +0x28`, `Normal +0x40`, `ImpactNormal +0x58`, `TraceStart +0x70`, `TraceEnd +0x88`, `bBlockingHit` bit 0 of `+0xAD`, `PhysMaterial +0xB0`, `HitObjectHandle +0xB8` (actor), `Component +0xD8`, `BoneName +0xF0` |
| `+0x100` | `CustomHitResults` (array of `FHitResult`) | `0x6B73500` (§6.3) | |
| `+0x110` | `ProjectileOrigin` | `inst+0x70` (spawn location), `0x6F356CE` | distance falloff origin ([Damage Pipeline §7.6](Wardogs_DamagePipeline_v2.md#76-the-bullet-event)) |
| `+0x128` | `ImpactVelocity` | the pre-exit velocity snapshot passed by the impact function (§4.1), `0x6F35717` | speed scale input |
| `+0x140` | `InitialVelocity` | `inst+0x88`, `0x6F356EE` | |
| `+0x158` / `+0x170` | `PostImpactLocation` / `PostImpactVelocity` | with a ricochet or penetration: `inst.Location` / `inst.Velocity` after the response; otherwise `hit.ImpactPoint` and the zero vector (`0x6F35C6D`–`0x6F35CC7`) | |
| `+0x188` / `+0x189` | `bRicocheted` / `bPenetrated` | arguments of §4.1 step 7, `0x6F3571A`, `0x6F35735` | |
| `+0x18A` | `bExploding` | written by `0x6B721B0` (§6.2) | |
| `+0x18C` | `ServerTime` | not written by `0x6F353F0` | writer **Open** (O-4) |
| `+0x190` / `+0x19C` | `AutoProxyFixedTickInfo` / `FromToPct` fixed-tick info (`NetworkPrediction`) | initialised to -1 by `0x6F353F0` | writers **Open** (O-4) |
| `+0x1A8` | `ProjectileId` | `inst+0xE0`, `0x6F356D2` | |
| `+0x1B0` | `SimulationData` (0x50): `ElapsedTime`, `Fuel`, `TotalAbsoluteWindDrift`, `TotalAbsoluteMove`, `HitCount`, `RicochetBitMap`, `PenetrationBitMap`, `RandomStreamSeed` | snapshot of the instance (`+0x290`, `+0x38`, `+0x58`, `+0x40`, `+0x118`, `+0x11A`, `+0x11C`, `+0xD0`) at `0x6F35C56`–`0x6F35D5F` | the state a replay of the step needs |

After building the record, `0x6F353F0` (a) appends a copy to the instance's `ProjectileHitData` array (`inst+0x2E8`, element size 0x238, `0x6F35FB6`–`0x6F35FFB`),
(b) broadcasts the subsystem's hit delegate (subsystem `+0xA0`, signature `(Hit, ImpactVelocity, ProjectileStats, ...)` in the
[SDK](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/sdk/raw/WDGame_classes.hpp#L44796)) with a copy of the stats (`0x6F36144`),
(c) prints the debug line when `0xD381580 >= 1` (`0x6F38360`), and (d) hands the record to the proxy component (§6.1).

---

## 6. From the hit record to a damage event

### 6.1 The proxy-component hit handler (`0x6B73E90`)

**Native.** `UWDProjectileProxyComponent` (SDK; vtable `0xB1AF7A0`, constructor `0x6B70C28`, `ProjectileOwnerId` at `+0xE0`) is the
component each shooter carries. `0x6F353F0` finds it from the instance (weak pointer `inst+0x104`; second route through the
projectile actor, weak pointer `inst+0x308`, `0x6F280F0`/`0x6DAEAA0`) and calls `0x6B73E90(proxy, &hit, inst)` (`0x6F35D8F`, `0x6F35DEE`).
An instance with no proxy and no actor-driven movement produces only the hit cue (`0x6F344D0` + `0x6F2D6E0`, `0x6F35E8A`–`0x6F35EA0`),
and only when the world's `AWDProjectileReplication` actor (`subsystem+0x1F0`, SDK) has the value 3 in its byte at `+0x170` and
`0x6B6FF90(hit actor)` is true.

The handler:

1. calls `0x6B721B0` (§6.2) and keeps its result;
2. looks up the instance's stats (`0x6BBA900`) and the owning controller (proxy slot `0x518`, `GetOwningController`, called with the object in `inst+0x120`);
3. reads the net mode (`0x3CAB0A0`, the owner actor's `GetNetMode`, **Derived**: stock `ENetMode`, value 3 = client);
4. branches on the net mode, on whether that controller is the local one (a virtual of the controller, slot `+0x7F0`; **Inferred**: `IsLocalController`), on the proxy's `IsServerOwned`
   (slot `0x520`, `0x6B73DE0`) and on a stats flag;
5. on the branch that builds damage, fills `CustomHitResults` from `0x6B73500`, calls the bullet event builder `0x6B725B0` and then the
   post-damage cue and hit-marker code `0x6B717C0` with the amount it returned;
6. on the other branches it may forward the record to the server through the `Server_ValidateClientHit` call (§7) or do nothing.

The truth table of step 4 is a network-authority matter and is not tabulated here; see §7 and
[`SECURITY.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/SECURITY.md).

### 6.2 Eligibility (`0x6B721B0`)

**Native.** Returns whether this hit may produce damage:

| Test | Source |
|---|---|
| hit actor valid, bit 3 of its flag byte `+0x62` set (same flag as in §4.2), and its class implements `IWDDamageable` (class `0x6C2A4E0`) | `0x6B721D8`–`0x6B72219` |
| the actor's `IWDDamageable` slot `+0x38` true and stats `+0x210` (unnamed bool, default true); the slot is the stub `0x1563050` (false) on `AWDMoverCharacter`, which then goes through the list test below | `0x6B7222B`–`0x6B722D7` |
| instance byte `+0x25D` non-zero (constructor default 1; copied with the instance, set nowhere else in the projectile code) | `0x6B722DA` |
| the hit actor is not matched by any element of the 8-byte array at `inst+0x130` (matcher `0x24738D0`), unless the damageable test above passed | `0x6B722E7`–`0x6B7230D` |
| or the hit is `bExploding` (§4.1; set by `0x6B72249`–`0x6B722C6`) | `0x6B72318` |

The array at `inst+0x130` is read here and in `0x6F353F0` (`0x6F35F39`); its writer was not located (O-6).

### 6.3 Custom hit results (`0x6B73500`)

**Native.** For a hit on a character it reads the target's mesh component (`+0x3A0` of the pawn) and its body instances
(`0x41FFAF0`) and returns a list of extra `FHitResult`s, stored in the record's `CustomHitResults` (`+0x100`). The damage builder evaluates each
custom hit separately and keeps the highest result (see [Damage Pipeline §7.6](Wardogs_DamagePipeline_v2.md#76-the-bullet-event), "Custom hits").
What the list holds for a typical bullet hit is **Open** (O-10).

### 6.4 Alignment: friendly fire and self hits

**Native + Data.** `ModifyDamage`'s conversion `0x6EF8DE0` sets `ModifyDamageData.Alignment` (`+0xB8`) as follows (`0x6EF92AA`–`0x6EF9396`):
the default is **2 (`Hostile`)**; when both the instigating and the target actor hold a valid weak pointer at `+0x2C0`, each pointed-to object is
asked by `0x6DAE470` for a value (it passes that object's member at `+0x5A0` to `0x6F143A0`), and if the two 8-byte values are equal the alignment
becomes **3 (`Friendly`)**. `Neutral` (1) is never produced by this function. An actor that damages itself resolves to the same value on both sides
and would therefore be `Friendly` (**Derived**).

**Data.** The infantry rule table
[`DT_GlobalDamage_InfantryData`](../data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json) has two entries with a required
alignment of `Friendly` (of 146):

| Entry | Source requirement | Operation |
|---:|---|---|
| 8 | `Meta.Damage.Bullet` | `Percentage_Ongoing` -50 (bullets do half to friendly targets) |
| 9 | `Meta.Damage.Utility.LargeHammer` | `Percentage_Ongoing` -70 |

Every other entry has alignment `None` and matches regardless. So, in the infantry table, friendly and self bullet damage is halved and not
removed. Nothing in the trace, the eligibility test or the damage builder compares teams. Whether other damage systems (vehicles,
buildables) use alignment, and the identity of the pawn-side value at `+0x2C0`, are **Open** (O-5). The existing
[cash-reward row](../content/Wardogs_Meta_v2.md) that halves reward for `Meta.Damage.Category.Friendly` shows the category tag exists on the reward side.

A target can also refuse damage altogether: the character's `IWDDamageable` slot `+0x30` (`0x6E6BD70`) returns the negation of `0x6E71010`, which asks
the character's gameplay-tag owner (`+0x620`, slot `+0x18`) whether it holds one tag read from a state object (`+0x2D8` → `+0x10C`); the tag
itself was not resolved (O-12).

### 6.5 Bone and section resolution

**Infantry.** The damage event carries the hit's `BoneName` (`FHitResult +0xF0`, event `+0x90`+). The hit-location tag is the exact `FName` match in
`DA_GlobalDamage_HitLocations_Player` (`0x6F01BB0`, config `ClassToHitLocations` maps `BHMoverPawn` and `WDTargetDummy` to it); an unmapped
bone gives no hit location ([Damage Pipeline §7.6](Wardogs_DamagePipeline_v2.md#76-the-bullet-event); data in
[`infantry-hitboxes.json`](../assets/data/infantry-hitboxes.json)). The 22 mapped bones:

| Bone | Hit-location tag (`Meta.Damage.HitLocation.Infantry.`…) | Impact remap (animation only) | Physics-asset body |
|---|---|---|---|
| `head` | `Head` | - | yes |
| `neck_01` | `Neck` | - | yes |
| `clavicle_l` | `Torso.Upper` | - | yes |
| `clavicle_r` | `Torso.Upper` | - | yes |
| `spine_05` | `Torso.Upper` | spine_04 | yes |
| `spine_04` | `Torso.Middle` | - | yes |
| `spine_03` | `Torso.Lower` | - | yes |
| `spine_02` | `Torso.Lower` | - | no |
| `spine_01` | `Torso.Lower` | pelvis | no |
| `upperarm_l` | `Arm.Upper` | - | yes |
| `upperarm_r` | `Arm.Upper` | - | yes |
| `lowerarm_l` | `Arm.Lower` | - | yes |
| `lowerarm_r` | `Arm.Lower` | - | yes |
| `hand_l` | `Arm.Hand` | - | yes |
| `hand_r` | `Arm.Hand` | - | yes |
| `pelvis` | `Pelvis` | - | yes |
| `thigh_l` | `Leg.Thigh` | - | yes |
| `thigh_r` | `Leg.Thigh` | - | yes |
| `calf_l` | `Leg.Calf` | - | yes |
| `calf_r` | `Leg.Calf` | - | yes |
| `foot_l` | `Leg.Foot` | - | yes |
| `foot_r` | `Leg.Foot` | - | yes |

**Vehicles.** The trace hits the vehicle's complex collision (§2.3, §2.6) and the first hit's component and face select the section; see
[Vehicle Damage §3.2](Wardogs_VehicleDamagePipeline_v1.md#32-from-a-hit-triangle-to-a-section) and
[§4.1](Wardogs_VehicleDamagePipeline_v1.md#41-order). The impact-sampling variants for explosives are in the vehicle evidence pages.

**Event builder.** `0x6B725B0` (see [Damage Pipeline §7.6](Wardogs_DamagePipeline_v2.md#76-the-bullet-event)) takes the hit record's
`HitCount` (`hit+0x1F0`), `RicochetBitMap` (`+0x1F4`) and `PenetrationBitMap` (`+0x1F8`) to add `Kinetic.Impact.Ricochet`/`.Penetration`
for hit number `HitCount - 2`, reads the speed from `ImpactVelocity` (`+0x128`) and the distance from `ProjectileOrigin`
(`+0x110`) to `ImpactPoint` (`+0x28`).

---

## 7. Authority, prediction and replay

**Native + SDK, flow only.** The projectile system is built for deterministic re-simulation, and the pieces are visible in the code and the SDK:

- the random stream behind every ricochet and penetration roll is the `inst+0xD0` seed (§4.3); the spawn setup carries a `Seed`
  (`FWDProjectileSimulationSetup.Seed`, SDK) and every hit record snapshots `RandomStreamSeed`, `ElapsedTime`, `Fuel`, wind drift,
  absolute move and the two history bitmaps (§5);
- `AWDProjectile` replicates `ProjectileNetId`, `ProjectileWeaponId`, `InitialLocation`, `InitialVelocity`, `SpawnTimeStamp` and its instigating proxy
  (SDK); `AWDProjectileReplication` is an `AInfo` with a fast-array container of replicated projectiles (delta compression registered in the packed config);
- `UWDProjectileProxyComponent` declares `Server_ValidateClientHit(FWDProjectileHitData)` and `Client_ValidateClientHit_Response(FWDProjectileHitValidationResult)`
  (SDK; the implementations are virtual slots `0x500` and `0x4F8` of the component's vtable, `0x6B74770` and `0x6B72370`, reached from the exec thunks
  `0x69E93E0` and `0x69E8E50`; the sender is `0x69E86F0`). The result struct carries `ProjectileNetId`, `ClientHitIndex`, `ElapsedTime` and `bValidHit`; the
  instance has `ValidClientProjectileHitData` and `bFailedHitValidation` fields (SDK);
- the hit record has `ServerTime` and `NetworkPrediction` fixed-tick fields (§5); the writers and readers of those fields are **Open** (O-4).

This page documents the flow, not its trust properties. What the server does with a forwarded hit is not described here (Damage Pipeline O-7 makes the
same reservation); findings in that area follow [`SECURITY.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/SECURITY.md).

---

## 8. Impact effects and decals

**Native.** Every hit produces a gameplay-cue event through the same two functions:

- `0x6F380A0(subsystem, inst, hit, selector)` builds the cue parameters with `0x6F344D0` and sends them. The parameter block gets: location =
  `hit.ImpactPoint` for a blocking hit, otherwise `hit.TraceEnd` (`0x6F3452F`–`0x6F34557`); normal = `hit.ImpactNormal`; the hit's physical material
  (`hit+0xB0`) and hit component (`hit+0xD8`) as weak pointers; the instance's weak pointer at `inst+0x120` (the projectile actor, §2.4) as the effect causer. It then goes through the
  `WDGameplayCue` manager (the object named by the string `"WDGameplayCue"`, `0x6F38321`): with the subsystem flag `+0xB0` clear it calls the manager's
  slot `+0x2E0` with the world, the tag global `0xD36C4A0` and mode 2 (`0x6F38253`–`0x6F38292`); with it set and the instance actor-driven it uses `0x6F2D6E0`
  (`0x6F38296`–`0x6F382AD`). The `selector` argument is one of the globals `0xD381600` (terminal hit), `0xD3815F0` (ricochet, `0x6F36DCD`) and the ones
  the penetration step passes (`0x6F36270`, `0x6F363AE`);
- it returns without a cue when the subsystem flag `+0xB0` is set and the instance is not actor-driven (`0x6F380B3`–`0x6F380CF`); when instance byte `+0x25E`
  is zero (default 1; `0x6F3812A`); when the hit actor implements `IWDDamageable` and both subsystem bytes `+0xB0` and `+0xB1` are clear (`0x6F380F7`–`0x6F38124`;
  damageable targets get their cue from the post-damage code `0x6B717C0` instead); and, for a projectile with an arming delay, whenever the selector is not
  `0xD381600` (`0x6F38137`–`0x6F3816F`). The meaning of the subsystem bytes `+0xB0` and `+0xB1` is **Open**.

The tag globals are initialised by static code and were not resolved to names (O-8).

[SDK] The cue notify Blueprint `GC_Weapon_Impact_C` (`AWDGameplayCueNotify_Actor`, tag family `GameplayCue.Weapon.Impact`) declares `SpawnImpactDecal`, `SpawnBloodDecal`,
`CreateGlassMeshDecal` and a `DefaultSurfaceResponse`, with `EPhysicalSurface` inputs. Its graph is not in `data/`, so which surface produces which decal, effect or
sound is **Open** (O-8). `FWDProjectileStats.ProjectileEffects.GameplayCueTag` names the in-flight cue per ammunition (for example
`GameplayCue.Weapon.RocketProjectile` on the 120x570 mm round) and is separate from the impact cue.

---

## 9. Function table

All RVAs are file RVAs. "Analysis image" is a byte comparison over the function's range (and its contiguous unwind chain); "same" means identical.

| RVA | Role | Analysis image |
|---|---|---|
| `0x6F3C060` | substep integrator; casts the trace (§2.1) | same |
| `0x6F3CB80`, `0x6F3D130` | step driver, per-instance driver | same |
| `0x3CAB670` | line trace by channel (wrapper) | same |
| `0x3CAE910` | line trace implementation (world physics scene virtual `+0x2C0`) | same |
| `0x3CB56B0` | shape-sweep wrapper used by the mover (§2.5) | same |
| `0x3C95C30` | `FCollisionQueryParams` constructor | **differs**: dispatch stub; read from the restored image |
| `0x42AF7C0` | response parameters default constructor | same |
| `0x42D9770` | response container: set every channel | **differs**: dispatch stub; read from the restored image |
| `0x6B8E100` | `FWDProjectileInstance` constructor (query params, flags) | same |
| `0x6F30E50`, `0x6F37510`, `0x6F37750` | instance init, post-spawn ignore lists, vehicle check | same |
| `0x6F39940` | spawn | same |
| `0x76D9110` | mover projectile simulation tick; traces (§2.5) | same |
| `0x6F36F40` | impact (§4.1) | same |
| `0x6F2F740`, `0x6F2FC20`, `0x6F2FB30` | penetration decision, exit query, capacity | same |
| `0x6F36600` | ricochet | same |
| `0x6F36190` | penetration step | same |
| `0x6F353F0` | hit record builder (§5) | same |
| `0x6F380A0`, `0x6F344D0`, `0x6F2D6E0` | cue dispatch, cue parameters, cue send | same |
| `0x6F342B0` | end of flight | same |
| `0x6B73E90` | proxy-component hit handler (§6.1) | same |
| `0x6B721B0` | eligibility, `bExploding` (§6.2) | same |
| `0x6B73500` | custom hit results (§6.3) | same |
| `0x6B725B0`, `0x6B717C0` | bullet damage event builder, post-damage cue | same |
| `0x6B73810`, `0x6B73940`, `0x6B73A60`, `0x6B73B30`, `0x6B73DE0` | proxy `GetIgnoredActors`, `GetIgnoredComponents`, `GetOwningCharacter`, `GetOwningController`, `IsServerOwned` (slots from the exec thunks) | same |
| `0x69E86F0`, `0x69E93E0`, `0x69E8E50`, `0x6B74770`, `0x6B72370` | RPC sender, exec thunks, vtable slots (§7) | same |
| `0x6EF8DE0`, `0x6F02EC0`, `0x6DAE470` | `ModifyDamage` conversion with alignment, entry, team value | same |
| `0x6E6BD70`, `0x6E71010` | `IWDDamageable` slot `+0x30` and its predicate | same |
| `0x699DEE0` | `FWDProjectileStats` constructor (defaults in §4.7) | same |

Vtables: `UWDProjectileProxyComponent` `0xB1AF7A0` (slots `0x4F8` response, `0x500` server call, `0x508` weapon for id, `0x510` owning character, `0x518` owning controller,
`0x520` is-server-owned, `0x528` ignored components, `0x530` ignored actors); `IWDDamageable` on `AWDMoverCharacter` `0xB40C038` and on the player class `0xB410D20`.

Reproduce:

```text
python -I _tools/hit_registration_check.py
WARDOGS_ANALYSIS_EXE=<analysis image> python -I _tools/hit_registration_check.py
```

---

## 10. What is open

1. **O-1: mover sweep.** Which collision shape slot `0x8B0` returns for an actor-driven projectile and which query, if any, uses the `ProjectileSweep` profile or
   the actor's `SweepProfileName` (§2.5).
2. **O-2: tapered capsules.** Whether the six tapered-capsule bodies are registered as query shapes (carried over from the collision evidence).
3. **O-3: server-side handling of a forwarded hit.** Not documented here (§7).
4. **O-4: fixed-tick and server-time fields.** Writers and readers of `ServerTime`, `AutoProxyFixedTickInfo` and `FromToPct` in the hit record; whether any
   target pose is reconstructed from them.
5. **O-5: alignment.** The identity of the object at pawn `+0x2C0` and the value `0x6F143A0` returns; whether non-infantry damage systems read alignment; how
   non-player instigators (AI, turrets) resolve.
6. **O-6: the array at `inst+0x130`.** Its writer and its exact meaning (§6.2).
7. **O-7: `bIsHitScan`.** The meaning of the context byte at `+0x2DA` behind the flag (§3); whether any weapon bypasses the projectile subsystem.
8. **O-8: impact cue tags and decal selection.** Names of the tag globals `0xD381600`, `0xD3815F0`, `0xD36C4A0`; the `GC_Weapon_Impact_C` graph (§8).
9. **O-9: `IgnoreInstigatorVehicleTime`.** How the time limits the ignore after the spawn (`inst+0x129`, `inst+0x28D`) (§2.4).
10. **O-10: `CustomHitResults` content** for infantry hits (§6.3).
11. **O-11: settings consumers.** `MaxPelletCount`, `MaxConsecutiveFullRefundedSubsteps`, and the exit-deflection distribution (§4.4, §4.6).
12. **O-12: `IWDDamageable` implementations.** The tag behind slot `+0x30`, slots `+0x38`, `+0x60`, `+0x68` for each actor type (§6.2, §4.1).
13. **O-13: runtime.** Nothing here was observed running; the trace shape and channel are static readings of the call site, and the stock Unreal definitions
    used for field names and `ENetMode` are assumptions about the engine build (UE 5.7).

Resolved here, from [Projectile Flight §12](Wardogs_ProjectileFlight_v1.md) item 3: the integer behind `floor(1000/Rate)` is the packed
`SimulationFrameRate` = 30, so the step is 33 ms.

Related: [Damage Pipeline](Wardogs_DamagePipeline_v2.md), [Vehicle Damage Pipeline](Wardogs_VehicleDamagePipeline_v1.md),
[Projectile Flight](Wardogs_ProjectileFlight_v1.md), [Combat Data Flow](Wardogs_CombatDataFlow_v1.md),
[Units](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/UNITS.md).
