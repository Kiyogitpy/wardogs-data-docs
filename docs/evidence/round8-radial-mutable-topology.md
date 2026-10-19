---
title: Round 8 character Mutable component topology
nav_exclude: true
---

# Round 8: third-person Mutable topology and radial candidates

Static CL-516586 executable, SDK, cooked CDO and local UE source review, 2026-10-18. This narrows the Mutable qualification in [round8-radial-points-components.md](round8-radial-points-components.md). No game process, service or IDA database was opened. The local UE 5.7.4 source is CL-51494982; its update behavior is corroboration, not exact-build proof.

## Result

The normal `AWDMoverPlayerCharacter` setup passes its existing third-person `CharacterMesh` (`actor +0x3A0`) to `MutableCharacterComponent.Init` (`actor +0x778`). The component creates a `UCustomizableObjectInstanceUsage`, which is a `UObject`, and attaches that usage to the supplied skeletal mesh component. A Mutable-generated skeletal mesh is assigned to the attached mesh component in the local UE implementation. This route changes the mesh asset and potentially its collision bodies; it does **not** create another third-person query primitive. The previously established one eligible third-person CharacterMesh candidate therefore survives this normal Mutable initialization/update route, subject to the mesh's actual query/body state.

This resolves the topology question for that route, not an invariant hit count for a live actor. Equipment, attachments, other later component mutations, LOS and sampling remain separate conditions; no live actor state was observed.

## Shipped executable path

`AWDMoverPlayerCharacter` virtual slot 115 at `0x6E7E530` calls base `AWDMoverCharacter` slot 115 `0x6E69D20`. Near the end of that base setup, original executable instructions at `0x6E6AFBE–0x6E6B01D` check actor `+0x778`, load actor `+0x3A0` into `rdx` at `0x6E6B013`, and call the Mutable component's virtual slot `+0x4F8` at `0x6E6B01D`. SDK `WDGame_classes.hpp:14005` identifies `+0x778` as `MutableCharacterComponent`; native construction `0x6E67160` stores it at actor `+0x778` and calls the `CharacterMesh` profile on the skeletal mesh at `+0x3A0`. The native base-pawn constructor stores that mesh at `+0x3A0`, as detailed in the companion report.

Both `UWDMutableCharacterComponent` and `UWDMutableComponent` vtables map slot 159 (`0x4F8`) to `0x6B44E60`. Its `a2` is the supplied mesh. On first initialization it creates an object named `MutableComponentInstanceUsage`, stores it at Mutable component `+0x430` (`sdk/raw/WDGame_classes.hpp:26571`), and passes `a2` to `0x66DE2A0`. The SDK declares `UCustomizableObjectInstanceUsage` as deriving from `UObject`, with `UsedSkeletalMeshComponent` at `+0x38` (`sdk/raw/CustomizableObject_classes.hpp:627-641`); `0x66DE2A0` records the supplied component as that weak attached target and marks the usage for a mesh set. The first-load branch calls `0x6B448B0` with the resolved `MutableObject`; that function associates a new customizable instance with the usage. The cooked `B_WDMoverPlayerCharacter` CDO's Mutable component names `/Game/Characters/Mutable/MUT_TP_Character` as its `MutableObject` (`round8_collision_20261018/B_WDMoverPlayerCharacter.json`, export `MutableCharacterComponent`; SHA-256 of the export is in the companion report).

The `0x6B421D0` lead is different: its only direct caller in the indexed native corpus is `0x6E7FA00`, twice for `FirstPersonBodyMutableInstance` and `FirstPersonArmsMutableInstance`. That routine creates first-person skeletal mesh components and applies `NoCollision` to them, as already established. `0x6B421D0` registers those usages with the Mutable component; it is not evidence of a second third-person collision primitive.

## Update mechanism and limit

Local UE plugin source `CustomizableObjectInstanceUsage.cpp:222-250` implements `AttachTo` by retaining the passed `USkeletalMeshComponent` and setting a pending mesh-update flag; `GetAttachParent` returns that component. `CustomizableObjectSystem.cpp:1300-1341` iterates usages for the updated instance, retrieves each attached parent, gets the generated `USkeletalMesh` for the usage's component name, and calls `Parent->SetSkeletalMesh(...)` when the asset differs. The same file's placeholder and discard branches (`:3915-3940`, `:4212-4229`) also set a skeletal mesh on the attached parent. `UCustomizableSkeletalComponent` in the shipped SDK derives from `USceneComponent`, not `UPrimitiveComponent` (`sdk/raw/CustomizableObject_classes.hpp:759-769`). These mechanisms support asset replacement on the existing `CharacterMesh`, rather than creation of a query-enabled mesh component. The exact compiled CL-516586 generic Mutable completion's final `SetSkeletalMesh` instruction was not independently located here, so source-level update details should not be treated as a byte-for-byte game trace.

Mutable can change which physics asset and shapes the existing component uses; [round8-helmet.md](round8-helmet.md) records the remaining helmet-selection and physics-asset uncertainties. Its generated mesh may therefore change *where* the one component can be hit even though this normal route does not add a radial candidate component.

Restored executable SHA-256: `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.
