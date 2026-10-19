---
title: Round 8 collision and physical materials
nav_exclude: true
---

# Round 8: collision, tapered capsules and physical materials

Bounded static CL-516586 investigation, 2026-10-18. Evidence: original restored executable (existing corpus SHA-256 `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`), read-only corpus, independent Capstone disassembly, SDK and fresh offline cooked exports. No game, process, service or IDA database was opened; no files were uploaded. Only this report was added to the repository for this pass.

## Results

Follow-ups resolve the static [profile response table](round8-config.md),
[tapered-element query builder](round8-tapered-query.md), and
[penetration/velocity/history consequences](round8-physical-material-downstream.md).
The table below records this earlier pass's boundaries; use those linked
reports and the active register for current status.

| Item | Result | Remaining limit |
|---|---|---|
| Character collision channels | Native constructor chain and profile application located; cooked component is Custom/QueryOnly | Exact effective response table still requires the shipped CharacterMesh collision profile/config, including overrides |
| Tapered capsule query shapes | Cooked elements, SDK layout and existence of a Chaos tapered-capsule type confirmed | No FK element-to-query-shape builder traced; six bodies' trace eligibility stays open |
| PM_Head / PM_Body | Fresh exports and native material defaults verified; material participates in projectile penetration geometry and density calculation | No health damage multiplier keyed directly by SurfaceType17/3 established |

## Character collision: native defaults are not the final profile

SDK `BHMover_classes.hpp:392` identifies `ABHMoverPawn`, including CharacterCapsuleComponent `+0x398` and CharacterMeshComponent `+0x3A0`. `AWDMoverCharacter` derives from it (`WDGame_classes.hpp:13986`).

Base constructor `0x5282640` creates the capsule and a `BHSkeletalMeshComponentBudgeted`. For the mesh, independently disassembled calls are:

- `0x5282C47`, virtual `+0x790`, argument 2: **SetCollisionObjectType(Pawn)**. This is not a call setting all channel responses to Block. Reflected `SetCollisionObjectType` at `0x3D47C80` uses virtual `+0x790`; vtable slot 242 resolves to `0x4420FF0`. That function invokes `0x4209E80`, which stores BodyInstance object channel `+0x15` and marks its profile Custom.
- `0x5282C5C`, virtual `+0x780`, argument 3: **SetCollisionEnabled(QueryAndPhysics)**. Reflected `SetCollisionEnabled` at `0x3D47C00` uses this virtual. SDK `ECollisionEnabled` values are NoCollision 0, QueryOnly 1, PhysicsOnly 2, QueryAndPhysics 3.

Derived `AWDMoverCharacter` constructor `0x6E67160` applies additional changes:

- The capsule receives `SetCollisionResponseToChannel`: channel 3 / response 0 at `0x6E67CCD`; channel 14 / response 1 at `0x6E67CE8`; channel 18 / response 1 at `0x6E67D03`. SDK `Engine_structs.hpp` identifies channel 3 as Visibility, 14 as GameTraceChannel1 and 18 as GameTraceChannel5; response 0 is Ignore, 1 Overlap. These are capsule changes, not a mesh response table.
- The mesh is assigned profile **CharacterMesh** at `0x6E67D25–0x6E67D48`, through virtual `+0x788` / slot 241. Vtable lookup resolves it to `0x4323CC0`, which calls the BodyInstance profile setter `0x4209690` at `0x4323D4D`.
- The BodyInstance setter applies named profile data through `0x41FFB60`. In its profile-loading branch, machine `0x41FFC1F–0x41FFC2D` obtains the collision-profile singleton and invokes `0x3CAEFF0` with profile name and BodyInstance. Therefore the final per-channel responses cannot be inferred from the earlier constructor's object-type/enabled arguments.

A fresh export of `Wardogs/Content/MoverTesting/B_WDMoverPlayerCharacter` succeeded. Its CharacterMesh subobject has BodyInstance CollisionEnabled **QueryOnly** and CollisionProfileName **Custom**; it serializes no response-channel container. Component transform remains Z -96 cm, Yaw -90 degrees. The old statement that the absent responses are simply native class defaults is too strong: the native constructor explicitly applies a named profile before the Blueprint's Custom/QueryOnly override. Configuration resolution and archetype serialization must be considered.

No complete CharacterMesh profile definition was found in the repository's exported `data/Wardogs/Config` files. This pass did not extract packed engine configuration, execute class-default construction or resolve runtime modifications. Keep `collision-channels` open, narrowed to that profile/config question. The capsule changes above do not prove which projectile channels hit the mesh bodies.

## Tapered capsules: metadata verified, query construction still open

Existing local physics export `iv_work/phys/physics.json` and `_tools/infantry_model.py` describe PA_TPCharacter_Simplified: 20 bodies, 9 boxes, 1 sphere, 6 sphyls and 6 tapered capsules; there can be multiple primitives on one body. The tapered bodies are calf_l, calf_r, lowerarm_l, lowerarm_r, thigh_l and thigh_r. Their cooked element CollisionEnabled is QueryAndPhysics, and body CollisionReponse is BodyCollision_Enabled/default. This is metadata, not proof that Chaos registers each element as a query shape.

SDK `Engine_structs.hpp:11352` gives FKAggregateGeom.TaperedCapsuleElems at aggregate `+0x40`; UBodySetup.AggGeom is at body setup `+0x38` (`Engine_classes.hpp:3721`), placing the tapered array at body setup `+0x78`. FKTaperedCapsuleElem (`Engine_structs.hpp:11458`) has size `0x70`, Center `+0x30`, Rotation `+0x48`, Radius0/Radius1 `+0x60/+0x64`, Length `+0x68`, and bOneSidedCollision `+0x6C`.

The executable does recognize a Chaos implicit-object type named TaperedCapsule. Function `0x21D7F90` maps low-five-bit type `0x10` to the name global `0xD14FBB0`; the dispatcher and name initialization were inspected in machine instructions. This proves that the type exists in the shipped binary, not that FKTaperedCapsuleElem bodies are instantiated with it for ray queries. The other obvious string hit, `p.ChaosCloth.UseOptimizedTaperedCapsule` (`0x153C7E0`), is a cloth setting; it does not establish skeletal rigid-body query behavior.

`tools/cue4parse_extractor/PhysicsMode.cs` reads the tagged AggGeom element arrays and exports their dimensions/settings. It supplies the string QueryAndPhysics as a marked default when the element omits CollisionEnabled. `_tools/infantry_model.py` independently builds a visualization mesh from the convex hull of two end spheres. Neither executes Unreal shape creation, so neither closes the query question.

Exact next static lead: locate the native body-instantiation/geometry builder that consumes UBodySetup's array at `+0x78`, strides elements by `0x70`, and reads Radius0/Radius1/Length. Follow the created implicit object and shape query/simulation filter flags through registration. None of the bounded string/alias searches located a named FK-to-Chaos builder. No negative claim that the bodies are unhittable is justified, and no positive claim follows merely from QueryAndPhysics.

## Physical materials: verified data and an actual ballistic consumer

Fresh WdExtract export succeeded for both packages (3 total exports including the player Blueprint; 0 failures). Raw JSON stays local in `E:/Reverse_Engineer/wardogs_analysis/round8_collision_20261018/`.

| Property | PM_Head | PM_Body |
|---|---|---|
| Class | WDPhysicalMaterial | WDPhysicalMaterial |
| SurfaceType | SurfaceType17 | SurfaceType3 |
| AudioSurface | Flesh | Flesh |
| Density | 0.2 cooked | omitted; native UPhysicalMaterial constructor defaults to 1.0 |
| BallisticResponse | omitted | omitted |

WDPhysicalMaterial constructor `0x69DA990`, machine `0x69DA9B0`, initializes BallisticResponse `+0xB0` to 0 = **Default**. Its other explicit defaults are PlanarThickness 1.0 and Roughness 0 (`0x69DA9C8`, qword store covering both floats), AudioSurface 0 (`0x69DA9D3`). UPhysicalMaterial base constructor `0x2467720` initializes Density `+0x3C` to 1.0. The cooked head overrides Density to 0.2; body does not.

Both fresh exports contain very small subnormal values labeled PlanarThickness. This report does not treat those as a meaningful thickness or assert why they occur; the mapping/serialized field needs a separate check before numeric use. The assets omit BallisticResponse and inherit Default, so these exported PlanarThickness values do not select the Planar branch by themselves.

There is a concrete native ballistic consumer:

1. `0x6F2F740` considers penetration when projectile stats bShouldPenetrate (`+0x204`) is set, or when the hit actor's WDDamageable override permits it. It invokes `0x6F2FC20` at `0x6F2F889`.
2. `0x6F2FC20` resolves FHitResult.PhysMaterial `+0xB0` at `0x6F2FC40–0x6F2FC50`, checks WDPhysicalMaterial class, and reads material BallisticResponse `+0xB0`. **Disabled (2)** rejects the exit-hit calculation at `0x6F2FC8D–0x6F2FC96`; **Planar (1)** selects a synthetic plane/thickness exit path (`0x6F2FD7A–0x6F2FDA1` reads PlanarThickness `+0xB4`). Default uses the body-geometry exit query later in this function.
3. On a successful entry/exit result, `0x6F2FA7E–0x6F2FAD1` resolves entry and exit physical materials, reads their Density at `+0x3C`, and chooses the maximum. It passes this density into the penetration calculation `0x6F2FB30` at `0x6F2FAED`. Instructions `0x6F2FBA0–0x6F2FBC7` clamp density to at least 0.001 and include it with projectile area in the calculation's denominator.

Thus “physical materials are only used for effects” would be incorrect. PM_Head/Body can affect projectile penetration through WDPhysicalMaterial behavior and density, independently of the raw bone hit-location mapping. The health rule pipeline still does not have a demonstrated direct SurfaceType17/3 multiplier, and this pass does not establish every downstream speed/damage effect of the penetration result. Keep that distinction in the viewer and documentation.

Suggested item updates: narrow `physical-material` to unresolved direct health-scalar use and full downstream ballistic consequences; retain `collision-channels` and `tapered-capsule-query` with the precise remaining leads above. Do not change the rendered six shapes on the strength of metadata alone.
