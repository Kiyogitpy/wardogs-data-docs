---
title: Round 8 packed configuration
nav_exclude: true
---

# Round 8: packed collision and hit-location settings

Static CL-516586 evidence, 2026-10-18. An isolated CUE4Parse helper read `.ini`
members from the installed `E:/Steam/steamapps/common/Wardogs/Wardogs/Content/Paks`
(32 mounted VFS, 149,124 files, 219 `.ini` entries). The installed shipping
executable reports `++Wardogs+Live-CL-516586`. The AES key was passed by file
path to the helper and was not printed. The extracted configuration and helper
remain outside the repository in
`E:/Reverse_Engineer/wardogs_analysis/round8_config_20261018/`; only the
following reviewed entries are recorded here.

## `CharacterMesh` collision responses

Packed `Wardogs/Config/DefaultEngine.ini` (SHA-256
`77412ce15622d61548a9b4298cc5202c55205723bb5993b0fe106b16b3592aba`)
removes the stock `CharacterMesh` profile at line 687, replaces it at line 705,
and edits it at line 784. The replacement names **Pawn** as object type and
**QueryAndPhysics** as profile collision mode. Its explicit responses ignore
Pawn, Visibility and Vehicle. The edit makes WDVehicleCamera **Overlap**,
Visibility **Block**, and PhysicsBody **Ignore**. The `(Channel="Visibility")`
entry means Block: UE 5.7 `EngineTypes.h:1320-1321` gives `FResponseChannel`
an ECR_Block default, and `CollisionProfile.cpp:663-676,682-699` applies the
edit after the replacement's responses.

All other channels start with the engine default Block except custom channels
whose defaults are set in the same packed file at lines 749-766
(`CollisionProfile.cpp:371-374,469-470`). The resulting responses for the
named built-in and project channels are:

| Response | Channels |
|---|---|
| Ignore | Pawn, Vehicle, PhysicsBody; SpatialTracker, WDAimAssist, FluidTrace, AudioOcclusion, Landscape, WDImpulseResonance, Ping, VisibilityNoPawn |
| Overlap | WDVehicleCamera, WDBuildablePlacement, WDRotor |
| Block | WorldStatic, WorldDynamic, Visibility, Camera, Destructible; WDProjectile, WDMeleeHit, WDWaterBody, WDExplosive, WDSmashableWindow, Ragdoll, WDDroppedItem |

The prior [constructor trace](round8-collision.md#character-collision-native-defaults-are-not-the-final-profile)
shows `AWDMoverCharacter` applying this named profile to the mesh. The cooked
`B_WDMoverPlayerCharacter` CharacterMesh export then serializes BodyInstance
`CollisionEnabled=QueryOnly` and `CollisionProfileName=Custom`, with no
response array (`E:/Reverse_Engineer/wardogs_analysis/round8_collision_20261018/B_WDMoverPlayerCharacter.json:4826-4829`). Thus the **profile** says
QueryAndPhysics, while this **Blueprint component** is QueryOnly/Custom. UE
5.7 `CollisionProfile.cpp:184-200` and `BodyInstance.cpp:194-202,297-309,4394-4451,4482-4495`
show that applying a profile fills the response array, and loading Custom
rebuilds the response container from that array. With no response override in
this Blueprint export, the inherited profile responses above are the static
answer for this component. This does not establish later runtime changes or
the separate physics-body shape-registration question.

## `ClassToHitLocations` entries and precedence

Packed `Wardogs/Config/DefaultGame.ini` (SHA-256
`56fda1824b851a0a02f57d96216f35e30078000e1f4148ce26c1a0ddc233f1bd`)
has one `[/Script/WDGame.WDDamageSubsystem]` assignment at lines 1040-1041:

| Config class key | Hit-location asset |
|---|---|
| `/Script/BHMover.BHMoverPawn` | `/Game/GameMechanics/DamageSystem/HitLocationDataAssets/DA_GlobalDamage_HitLocations_Player.DA_GlobalDamage_HitLocations_Player` |
| `/Script/WDGame.WDTargetDummy` | Same asset |

These are the two concrete shipped pairs found across the 219 packed `.ini`
members. `AWDMoverCharacter` derives from `ABHMoverPawn`
(`sdk/raw/WDGame_classes.hpp:13986`); `AWDTargetDummy` derives from
`AWDTarget : AActor` (`sdk/raw/WDGame_classes.hpp:7599,34073`). Their
inheritance branches do not overlap, so no shipped target can match both
configured keys. The [loaded-map writer and reader](round8-armor.md#hit-location-map-writer)
establish the class test and asset lookup. Its hash-map iteration order would
matter if overlapping class keys were configured, but this shipped map poses
no such precedence contest. This is a static config result, not a claim about
unobserved later config or runtime mutation.
