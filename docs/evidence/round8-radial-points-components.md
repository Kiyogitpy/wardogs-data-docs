---
title: Round 8 radial point cloud and character components
nav_exclude: true
---

# Round 8: radial point-cloud selection, distance and character components

Static CL-516586 investigation, 2026-10-18. This supplements [round8-radial.md](round8-radial.md). Original executable bytes were read offline and independently disassembled with Capstone; the existing SQLite corpus was opened read-only for navigation and pseudocode. No game process, service or IDA database was opened. No raw corpus or complete Blueprint dump is included.

## Result

The alternate routine `0x6EFD9C0` is the **Points / point-cloud occlusion** mode named by the shipped console variable, rather than a separately named voxel damage model. It reaches the same `0x6F03720` accepted-hit builder and distance writer as Center and Disc. Moving the occlusion ray's start does **not** move the distance reference away from the original blast origin. The shipped native default selects Points, with first-unoccluded-point termination; it does not guarantee the globally closest collision point.

The fresh `B_WDMoverPlayerCharacter` default subobjects contain two primitives: CharacterCapsule and CharacterMesh. The capsule's native response ignores Visibility; CharacterMesh's inherited shipped response blocks it. The Blueprint adds an AI perception source, not another primitive. Native first-person setup can instantiate two additional skeletal meshes, but explicitly applies NoCollision to both. Thus one third-person CharacterMesh is the supported ordinary default character candidate, conditional on its loaded bodies and query state. This does not establish one successful hit for every blast or an invariant component count for every runtime player actor.

## Selector and shipped defaults

Original executable registrations and initial data are:

| Console variable | Registration RVA | Backing RVA | Initial value |
|---|---:|---:|---:|
| `WD.DamageSystem.ExplosiveOcclusionMethod` | `0x12DDFC0` | `0xCED1158` | 2, Points |
| `WD.DamageSystem.PointDiscardMode` | `0x12DE080` | `0xCED115C` | 2, stop at first unoccluded point |
| `WD.DamageSystem.AngleDiscardThreshold` | `0x12DDEC0` | `0xCED1160` | 10 degrees |
| `WD.DamageSystem.SeparateVehicleOverlaps` | `0x12DDF00` | `0xCED1164` | true |
| `WD.DamageSystem.QueryPointEarlyRejectionDistance` | `0x12DE040` | `0xCED1168` | 100 cm |
| `WD.DamageSystem.PointCloudRadius` | `0x12DE000` | `0xCED116C` | 50 cm |
| `WD.DamageSystem.MinRingRadius` | `0x12DDF80` | `0xCED1170` | 20 cm |

The registration is independently machine-backed: `0x12DDFD3` supplies `&0xCED1158`, `0x12DDFDA` supplies its name, and `0x12DDFE8` calls the integer-reference registration helper. For PointDiscardMode the corresponding instructions are `0x12DE093`, `0x12DE09A`, `0x12DE0A8`. The original backing bytes at `0xCED1158` and `0xCED115C` are each `02 00 00 00`; these are initial data values, not observed live console state.

The registration help identifies method 0 as Center, 1 as Disc and 2 as Points. Actual control flow agrees: cloud construction is called at `0x6F00BAD` (real entry `0x6EF63C0`; corpus row starts three bytes early). `0x6F00BB2–0x6F00BCB` enables the Points branch only when method equals 2 **and** the generated cloud count is nonzero. `0x6F01183` checks method 1, which calls Disc gather `0x6EFAF20` at `0x6F011F6`. Otherwise `0x6F01200–0x6F0124E` selects `0x6EFD9C0` when the Points flag is true; `0x6F01255–0x6F01295` falls back to ordinary `0x6EFC4A0`. An empty generated cloud therefore falls back even with method 2. Other method values also take that fallback.

Narrow exact-name searches across the 219 extracted packed `.ini` members found no assignments to the seven variables above. Packed configuration is rooted at `E:/Reverse_Engineer/wardogs_analysis/round8_config_20261018/extracted`. This bounds the static configuration search; command-line, console, code and external configuration changes remain possible.

`SeparateVehicleOverlaps` is now identified, resolving the unnamed global in the earlier report. Gather pseudocode shows the extra object-query mask `0x40`, followed by the Visibility channel-3 query. The variable's help describes separate vehicle and visibility overlaps. This supplement does not independently rederive the helpers' complete simple/complex flag interpretation from the help string alone.

## Point-cloud results use the original-origin distance

There are two forms of the same callback path inside `0x6EFD9C0`:

```text
6EFD9C0 -> 6EF7950 -> 6F03340 -> 6EF8A80 -> 6EF6EE0 -> 6F03720
6EFD9C0 (inline equivalent at 6EFE34F) -> 6F03340 -> same callback chain
```

The class-specific sample branches produce temporary 40-byte candidate records and pass them to `0x6EF7950`. Its call at `0x6EF7AFA` invokes cloud iterator `0x6F03340`; `0x6EF79C2` installs callback `0x6EF8A80`. The instanced-mesh inline loop independently installs that same callback at `0x6EFE20D`, stores it at `0x6EFE34B`, and calls the iterator at `0x6EFE34F`. These are callback invocations, so a direct-call search for the final hit builder alone misses this path.

Iterator `0x6F03340` combines the blast origin with cloud offsets at `0x6F033CF–0x6F03412`; it can also traverse precomputed start positions. Its callback invocations at `0x6F0348A` and `0x6F03691` pass the selected start point in `r8`. Callback `0x6EF8A80` loads the supplied point index and jumps directly to `0x6EF6EE0`. That function passes the original gather context, candidate point and selected ray start into `0x6F03720` at `0x6EF703E`. The gather context's original-origin pointer at `+0x40` is preserved; the selected ray start is a separate argument.

All accepted-hit exits of that builder converge on the distance calculation at `0x6F03991–0x6F039C7`: subtract the original gather origin from the selected result point, sum squared XYZ differences, take the square root, convert to float and store `FHitResult.Distance` at hit `+0x8`. The result point is:

- accepted ordinary collision: `ImpactPoint` at hit `+0x28`, loaded by `0x6F03A7B–0x6F03A8A`;
- accepted target-root exception: candidate point, loaded at `0x6F03983`;
- accepted synthetic skip-LOS hit: constructor-supplied candidate/ImpactPoint, reloaded at `0x6F03B55–0x6F03B64`.

The distance write precedes insertion/replacement through `0x6EF70D0` (`0x6F039CC`). The cloud traversal changes acceptance and which collision is found, but not this formula. It must not be described as ray-travel distance from whichever cloud point happens to be tested. Temporary candidate distance/sort values also are not the final damage distance.

PointDiscardMode changes search completeness. At value 1, `0x6EF6EEA–0x6EF6FA2` rejects a proposed start when its squared candidate-to-start length is at least the currently retained hit's squared TraceStart-to-TraceEnd length. At value 2, `0x6EF7054–0x6EF7060` returns a stop boolean after success. The iterator consumes that return at `0x6F0348C–0x6F0348E` or `0x6F03693–0x6F03695`. Consequently the default is first accepted unoccluded start in traversal order; it need not exhaust all starts to minimize original-origin-to-ImpactPoint distance. The existing retained-hit comparison still applies when multiple results actually reach it.

The early rejection distance is a separate candidate gate. `0x6EFE220–0x6EFE27C` skips the candidate when its original-origin squared distance exceeds `(ExplosiveRadius + rejectionDistance)^2`, provided rejectionDistance is positive. This is not an added falloff radius. The accepted-hit radius checks and final amount formula remain those documented in the earlier radial report.

## Character component evidence

Fresh local export:
`E:/Reverse_Engineer/wardogs_analysis/round8_collision_20261018/B_WDMoverPlayerCharacter.json`
(SHA-256 `f36bbf5c1977cf6044f73589b9344747d0e0c871f07f5bd9f4ea0f627e7ec312`). Its generated-class SuperStruct is native `WDMoverPlayerCharacter`; its CDO RootComponent points to CharacterCapsule.

| Default subobject | Class and query significance |
|---|---|
| CharacterCapsule | `BHMoverCapsuleComponent`; root primitive; authored half-height 96 cm. Native derived constructor sets Visibility Ignore. |
| CharacterMesh | `WDSkeletalMeshComponentBudgeted`; third-person primitive; SK_DefaultCharacter default; QueryOnly / Custom in the cooked component, inheriting the configured CharacterMesh response array. Visibility Block. |
| NetworkSmoothingComponent, FirstPersonCamera | Scene/camera components, without primitive collision geometry. |
| Movement, action, animation, vitality, gameplay effect/cue, inventory, damage entity, mutable character, weapon behavior, vehicle operator, voice and interaction components | Other native actor components; their presence does not itself create another blast collision body. |
| AIPerceptionStimuliSource | The only node in SCS RootNodes and AllNodes; its template class is `AIPerceptionStimuliSourceComponent`, not a primitive. The separate DefaultSceneRootNode is not an additional node in those arrays. |

Native construction independently corroborates the two primitive defaults. `WDMoverPlayerCharacter` constructor `0x6E7D050` calls `WDMoverCharacter` constructor at `0x6E7D09D`; the latter calls `BHMoverPawn` constructor `0x5282640` at `0x6E671B9`. Base constructor creates the capsule through `0x188C980` at `0x52829CB` and stores it at actor `+0x398`. It creates the skeletal mesh at `0x5282BC9` and stores it at actor `+0x3A0` (`0x5282BE7`/`0x5282BF0`). Player construction changes the mesh default-subobject class before calling the base; the fresh export establishes the resulting WDSkeletalMeshComponentBudgeted class.

The derived capsule response is explicit at `0x6E67CC5–0x6E67CCD`: channel 3 (Visibility), response 0 (Ignore), virtual SetCollisionResponseToChannel. The mesh receives named profile CharacterMesh at `0x6E67D25–0x6E67D48`. The packed profile and Blueprint override resolution are documented in [round8-config.md](round8-config.md#charactermesh-collision-responses), and the physics-body registration is separately addressed in [round8-tapered-query.md](round8-tapered-query.md). These prove a query-capable default mesh; they do not guarantee that every body is registered, enabled or within a particular overlap at a particular instant.

First-person meshes are not constructor-created CDO primitives: player constructor initializes actor `+0xBC8` and `+0xBD0` to null. Runtime setup `0x6E7FA00` resolves/creates them using helper `0x6E7CB60` and attaches them to the relevant scene nodes. Both are explicitly assigned the global profile at `0xD279978`: virtual profile calls at `0x6E7FBA1` (body) and `0x6E7FFA3` (arms). Its initializer `0x117B9C0–0x117B9CE` names UTF-16 `NoCollision` at `0xA02BD18`, independently read from the executable. Do not infer extra radial hits from the two first-person mesh fields merely because the SDK exposes them.

Packed `DefaultGame.ini:300` also supplies the concrete LOS class lists left unnamed earlier: SkipLOSCheck contains WDDestructionBuilding; IgnoreInLOSCheck contains WDMoverCharacter; IgnoreAttachParentOcclusion contains WDC4. WDMoverPlayerCharacter derives from WDMoverCharacter. The class names do not by themselves mean that a player bypasses every LOS test; the existing gather's respective flag paths still govern those effects.

## Closure and remaining boundary

The subsequent [Mutable component association trace](round8-radial-mutable-topology.md) resolves the normal third-person completion/association lead described below: it reuses the existing CharacterMesh component. Arbitrary later mutations and per-hit acceptance remain conditional.

Close the alternate-mode distance-writer question and the unnamed mode/config selector. The static default supports **one eligible third-person mesh component**, with one retained valid hit per component under the ordinary character filter. It supports neither a universal successful-hit count nor summing a fixed number of body/bone samples: overlaps, sampling, LOS, the retained-hit filter and protected-seat rejection still apply.

A fixed count for every live character remains conditional because this work did not enumerate all mutable-generated meshes, inventory attachments and later component/collision mutations. Native `0x6E7FA00` already demonstrates component creation after construction, and CDO serialization cannot enumerate an actor's complete future state. The exact next static lead is the third-person mutable completion/association path rooted at the character's MutableCharacterComponent (`+0x778`), including `0x6B421D0` and the mesh/class selection callback chain; distinguish replacement of CharacterMesh's asset from creation of another query-enabled primitive. A reproducible actor-state query would settle the actual registered component/body set, but no runtime observation was performed or is claimed here.

Original restored executable SHA-256: `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.
