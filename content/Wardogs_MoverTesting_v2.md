---
title: "MoverTesting"
parent: "Content"
redirect_from: ["/Wardogs_MoverTesting_v2.html", "/Wardogs_MoverTesting_v2"]

> **See also.** Base `MaxSpeed`, sprint scales and other values the export omits (class defaults), speed per stance, and the curves and audio in `GameMechanics/Player` are on [Player Movement](Wardogs_PlayerMovement_v1.md).

---

# Wardogs — Mover & Character Movement Reference
*Extracted from the cooked JSON export under `Content/MoverTesting` (78 files, 177 export blocks). Values are raw asset properties. Where a meaning comes from a property name rather than from the export, it is marked as inferred. A "-" in a table means the property is absent from the export.*

> **Scope note:** the folder is named "MoverTesting", but it holds the live character movement stack: ground, falling, parachute, climbing, ladder, mantling, vaulting, swimming, ragdoll, body dragging, weight classes, camera-lock modifier states, and the input map. The name is kept as it is in the dump.

---

## 1. Inventory

| Folder | Files | Export types | Contents |
|---|---|---|---|
| [`CharacterModifierStates/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/MoverTesting/CharacterModifierStates) | 18 | `WDCharacterModifierStateDefinition` | State-driven camera locks, camera modifiers, and character modifiers |
| `Settings/` | 19 | `BHGroundMovementData` (x2), `WDFallingData`, `WDParachuteData`, `BHClimbingData`, `BHMantlingData`, `BHVaultingData`, `WDTraversingData` (x3), `BHLadderClimbingData`, `BHMoverSwimmingDataAsset`, `BHMoverModeData_NoClip`, `BHPawnMoverModeData`, `WDBipodMountingData`, `WDBodyDraggingData`, `WDMoverWeightData`, `WDRagdollMovementData`, `WDVehicleData` | Per-mode movement tuning |
| `Curves/` (+ `Breathing/`, [`CrashLanding/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/MoverTesting/Curves/CrashLanding), `Doors/`, `Falling/`, [`Leaning/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/MoverTesting/Curves/Leaning), [`Traversing/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/MoverTesting/Curves/Traversing)) | 39 | `CurveFloat` (21), `CurveVector` (16), `CurveTable` (2) | Curves that drive lean, stance, traversal, falling, and camera |
| [`Blueprints/Ladders/LadderData/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/MoverTesting/Blueprints/Ladders/LadderData) | 1 | `PDA_LadderData_C` | Ladder mesh set |
| `Input/` | 1 | `InputMappingContext` | Player key bindings ([`IMC_MoverPlayer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Input/IMC_MoverPlayer.json)) |

Totals: 18 + 19 + 39 + 1 + 1 = **78**. The 39 curve assets split as 21 float curves (`CurveFloat`, including the 9 at the Curves root), 16 vector curves (including the six stance-transition curves at the root), and 2 curve tables.

---

## 2. Character Modifier States (`WDCharacterModifierStateDefinition`, 18 assets)

Each state is a tag plus a set of conditions. When the conditions pass, the state's camera modifiers and character modifiers apply. The table lists the state tag, the priority, and the condition and modifier classes. Priority is shown as "-" where the export has no `Priority` field (12 of 18 have one).

| Asset | State tag | Priority | Conditions | Character modifiers | Camera modifiers |
|---|---|---|---|---|---|
| AnimationFrustum | `State.CharacterModifier.AnimationFrustum` | 126 | StateTags | AnimationFrustum (quaternion rotation 0, 0, 0.707, 0.707) | - |
| BipodMounting | `State.CharacterModifier.BipodMounting` | 124 | StateTags | BipodMounting, BipodMountingCameraLock | - |
| BodyDragging | `State.CharacterModifier.BodyDragging` | - | StateTags, MovementMode | CameraLock | - |
| CameraPitch | `State.CharacterModifier.CameraPitch` | 10 | StateTags | CameraPitch | - |
| Climbing | `State.CharacterModifier.Climb` | - | StateTags, MovementMode | TraversingCameraLock, TraversingFirstPersonLock | - |
| CrashLanding | `State.CharacterModifier.CrashLanding` | - | StateTags | CrashLanding | - |
| Critical | `State.CharacterModifier.Critical` | 0 | StateTags | IgnoreLookInput (blueprint) | Critical |
| Emote_FullBody | `State.CharacterModifier.Emote.FullBody` | 0 | StateTags | IgnoreLookInput (blueprint) | Critical |
| HeavyBreathing | `State.CharacterModifier.Camera.HeavyBreathing` | 10 | Tags | - | HeavyBreathing (blueprint) |
| Ladder | `State.CharacterModifier.Ladder` | - | StateTags, MovementMode | Ladder, LadderCameraLock | - |
| Lean | `State.CharacterModifier.Lean` | 30 | StateTags | Lean | - |
| Mantling | `State.CharacterModifier.Mantle` | - | StateTags, MovementMode | TraversingCameraLock | - |
| Parachute | `State.CharacterModifier.Parachute` | 128 | StateTags, MovementMode | ParachuteCameraLock | - |
| Prone | `State.CharacterModifier.Prone` | 9 | StateTags, ProneOrTransition | ProneCameraLock, ProneWallLock | - |
| Stance | `State.CharacterModifier.Stance` | 0 | StateTags | Stance | - |
| Vaulting | `State.CharacterModifier.Vault` | - | StateTags, MovementMode | TraversingCameraLock | - |
| Vehicle | `State.CharacterModifier.Vehicle` | 100 | StateTags | VehicleSeat | VehicleFreeLook |
| VehicleCritical | `State.CharacterModifier.Vehicle.Critical` | 0 | StateTags | - | PanToKillerVehicle, Critical |

**Conditions**

- **StateTags** is a boolean tag query. Each one has a `TagDictionary`, an encoded `QueryTokenStream`, and a readable `AutoDescription`.
- **MovementMode** requires a mover mode tag. The mapping is: BodyDragging to `Mover.Mode.BodyDragging`, Climbing to `Mover.Mode.Traversing.Climbing`, Ladder to `Mover.Mode.LadderClimbing`, Mantling to `Mover.Mode.Traversing.Mantling`, Parachute to `Mover.Mode.Parachuting`, Vaulting to `Mover.Mode.Traversing.Vaulting`.
- **ProneOrTransition** applies to Prone (prone stance or a transition into or out of prone).
- **Tags** on HeavyBreathing requires `Meta.Punishment.HeavyBreathing`, so the camera effect follows a punishment tag rather than a state query.

**Example query, Bipod mounting:** `ALL( ALL( Action.Weapon.Bipod.Mount ), NONE( State.Player.Vitality.Critical, State.Player.Vitality.Dead, State.Player.Vehicle.Role.ActivePassenger, State.Player.Vehicle.Role.Driver, ... ) )`. The readable description is "We are alive and not in a vehicle". Most ground states use the same "alive and not in a vehicle" core.

**Example query, Critical:** `ALL( ANY( State.Player.Vitality.Critical ), NONE( State.Player.Vehicle.Role.ActivePassenger, State.Player.Vehicle.Role.Driver, ... ) )`. The description is "We are in a critical state and not in a vehicle."

### 2a. Modifier parameters

Only values that are actually present in the export are listed. Lock values are angles in degrees (inferred from the name `LockAngle`).

| Modifier | Pitch lock | Yaw lock | Other |
|---|---|---|---|
| BipodMountingCameraLock | 10 | 10 | No smoothing |
| BodyDragging CameraLock | 45 (CapsuleRotation, interpolated, speed 2, smooth 0.8, max turn 5) | 45 (NetworkSmoothingComponentRotation, smooth 0.8, max turn 5) | Roll lock: None |
| Climbing / TraversingCameraLock | 40 (smooth) | 60 (smooth) | |
| Ladder (LadderCameraLock) | 45 (centre offset 30, smooth 0.7) | 40 (smooth 0.7) | |
| Mantling / Vaulting TraversingCameraLock | 80 (smooth 0.7) | 120 (ControlRotation, smooth, max turn 5, target interp speed 1) | |
| Parachute CameraLock | 60 (CapsuleRotation, interpolated, smooth 0.7) | 60 (CapsuleRotation, TargetCapsuleRotation, smooth 0.7) | |
| Prone CameraLock | WorldZero, interpolated, centre offset 5, interp speed 3 | 90 (ControlRotation, TargetLookRotation, smooth 0.4, max turn 5, target interp 1.5) | Target exit multiplier 5 |
| Critical (camera) | 40 | - | |
| VehicleCritical (camera) | 30 | 30 | |
| Lean | - | - | Interpolation speed 15 |

**Critical state, transform detail**

| Target | Transform mode | Offset mode | Bone | Offset | Rotation (P, Y, R) |
|---|---|---|---|---|---|
| DefaultState | Character | RelativeWorldOffset | head | world (0, -200, 0) | - |
| DraggedState | Character | RelativeOffset | pelvis | relative (3, 20, 0) | (0, 110, -90) |

Transition time is 0 for both. The Emote_FullBody variant uses the same modifier classes with a default-state bone of `head`, a relative offset mode, and a rotation of (0, 75, -90).

**Other modifiers**

- **AnimationFrustum:** a quaternion rotation of (0, 0, 0.707, 0.707), which is a 90 degree turn about Z.
- **CrashLanding:** three curves. `OffsetCurve` = [`CRV_CrashLandingOffset`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Curves/CrashLanding/CRV_CrashLandingOffset.json), `OffsetScalarCurve` = [`CRV_CrashLandingScalar`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Curves/CrashLanding/CRV_CrashLandingScalar.json), `TimeToPlayCurve` = [`CRV_CrashLandingTime`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Curves/CrashLanding/CRV_CrashLandingTime.json).
- **Stance:** a map of six `(From, To)` stance pairs to `CurveVector` transition offsets (section 4).
- **Lean:** interpolation speed 15.
- **NetMask 3** is set on the CameraPitch, CrashLanding, Lean, Stance, and Vehicle modifiers. It is a replication mask (inferred from the name).
- **Referenced but not in this folder:** [`CRV_LandingPunishment_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_LandingPunishment_Damage.json) (used by the falling settings) and [`CRV_ParachutePunishment_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_ParachutePunishment_Damage.json) (used by the parachute settings) are referenced from section 3 but are not among the 39 curve files.

---

## 3. Movement Settings (`Settings/`, 19 assets)

### 3a. Ground movement (two assets, shared shape)

| Parameter | [`DA_GroundMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_GroundMovement.json) | [`DA_BodyDragging_GroundMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_BodyDragging_GroundMovement.json) |
|---|---|---|
| MinSpeed | 80 | 80 |
| Friction | 6 | 6 |
| BackMaxSpeedScale / StrafeMaxSpeedScale | 0.7 / 0.7 | 0.7 / 0.7 |
| ForwardStrafeScale | 0.6 | 0.6 |
| BackwardStrafeScale | - | 0.35 |
| ForwardStrafeScaleSprinting / TacSprinting | 0.3503 / 0.3503 | 0.3503 / 0.3503 |
| MinStartTacSprintPercentage | 0.2 | 0.2 |
| BlockSprintTime / BlockTacSprintTime | 0.8 / 0.6 | - |
| JumpVelocity | 320 | 320 |
| MaxJumpStamina / JumpStaminaCost | 150 / 50 | 150 / 50 |
| JumpStaminaRegenPerSecond / JumpCooldown | 50 / 0.05 | 50 / 0.05 |
| PostVaultFrictionTime | 0.6 | 0.6 |
| SlowWalk settings (Slow / Moderate / Fast) | 0.2 / 0.4 / 0.6 | 0.2 / 0.4 / 0.6 |
| LeanTime / UnleanTime | 0.55 / 0.35 | 0.55 / 0.35 |
| UnleanInterpolationSpeedCollided / LeanTraceRadius | 15 / 10 | 15 / 10 |
| StanceCooldown / StanceStaminaRegenPerSecond | 0.15 / 50 | 0.15 / 50 |
| ProneSweepDistance | 125 | - |
| bValidateProneFeetLocation | False | - |
| InputMappingContext | - | [`IMC_Player_BodyDrag`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IMC_Player_BodyDrag.json) |

**Stance table (both ground assets, identical)**

| Stance | Capsule half-height | Capsule radius | Eye height | Stance stamina cost |
|---|---|---|---|---|
| Stand | 96 | 34 | 168 | 20 |
| Crouch | 68 | 34 | 118 | 30 |
| Prone | 34 | 34 | 36 | 50 |

| Transition | Time (s, inferred) |
|---|---|
| Stand to Crouch | 0.3 |
| Crouch to Prone | 0.4 |
| Prone to Crouch | 0.5 |
| Crouch to Stand | 0.3 |

Each stance also has acceleration and max-speed modifiers (`BHFloatModifier_Operation` objects). The modifier values are in the referenced sub-objects and are not expanded here.

### 3b. Body dragging (`WDBodyDraggingData`)

| Parameter | Value |
|---|---|
| bUseIK | True |
| LeftHandSocketName / RightHandSocketName | `Socket_Drag_l` / `Socket_Drag_r` |
| DrageeOffset | 20 |
| DrageeRotationSpeed | 2.5 |
| Trace channel | `ECC_GameTraceChannel6` (key is hashed; value only) |

### 3c. Falling and parachute

**[`DA_FallingMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_FallingMovement.json) (`WDFallingData`)**

| Parameter | Value |
|---|---|
| Acceleration / MaxSpeed / MaxStopSpeed | 5 / 300 / 150 |
| AirFriction / AirControlPercentage | 1 / 0.2 |
| VerticalTerminalSpeed / HorizontalTerminalSpeed | 5300 / 5300 |
| FallingFloorTraceDistance | 1,000,000 |
| bStayBasedInAir | True |
| Impart base velocity (X, Y, Z) | True, True, True |
| Landing damage lookup | [`CRV_LandingPunishment_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_LandingPunishment_Damage.json) |
| Landing damage type | `WDFallDamageType` |
| Air-control curve | [`CRF_Falling_SurfaceAngleToAirControl`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Curves/Falling/CRF_Falling_SurfaceAngleToAirControl.json) |
| Push-off curve | [`CRF_Falling_SurfaceAngleToPushOffForce`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Curves/Falling/CRF_Falling_SurfaceAngleToPushOffForce.json) |
| InputMappingContext | [`IMC_Player_Falling`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IMC_Player_Falling.json) |

**[`DA_ParachuteMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_ParachuteMovement.json) (`WDParachuteData`)**

| Parameter | Value |
|---|---|
| GliderAcceleration | 1250 |
| PullUpDragAcceleration | 1500 |
| PitchSpeed / RollSpeed | 1 / 1 |
| MinPitch / MaxPitch / MaxRoll | -10 / 15 / 20 |
| SwingForceMultiplier | 5 |
| PullUpStaminaUsagePerSecond / PullUpStaminaRegenPerSecond | 50 / 30 |
| MinFallHeightBeforeAbleToParachute | 100 |
| Velocity damage lookup | [`CRV_ParachutePunishment_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_ParachutePunishment_Damage.json) |
| Velocity damage type | `WDFallDamageType` |
| ParachutingFloorTraceDistance | 1,000,000 |

### 3d. Traversal: climbing, mantling, vaulting

**[`DA_ClimbingMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_ClimbingMovement.json) (`BHClimbingData`)**

| Parameter | Value |
|---|---|
| MaxLedgeLookAngle | 60 |
| MaxClimbPercentToCancel | 0.65 |
| BaseScaleOverSpeed / BaseTraversalSpeed | 145 / 145 |
| FindWallTraceDistance | 20 |
| ClampedTraversalDirectionMask | 1 |
| Scale-over animations | `A_TP_Rifle_Climb_Still_Scaling_180`, `A_TP_Rifle_Climb_Still_OnTop_180` |
| Montage choosers | `CHT_Traversal_Climbing_ThirdPerson` (plus `_RM_On` and `_RM_Off` root-motion variants) |

**[`DA_MantlingMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_MantlingMovement.json) (`BHMantlingData`)**

| Parameter | Value |
|---|---|
| MaxAllowedWallAngle | 60 |
| MaxHeightAboveLedgeToScaleOver | 55 |
| MaxWallWidth | 30 |
| BaseScaleOverSpeed | 200 |
| FindWallTraceDistance | 50 |
| MaxTargetFloorHeight | 35 |
| AllowedScaleOverDirectionMask / AllowedTraversalDirectionMask | 11 / 11 |
| ClampedTraversalDirectionMask | 199 |
| bUseForwardOnlyHeight / ForwardOnlyHeight | True / 127.5 |
| Montage choosers | `CHT_Traversal_Mantling_ThirdPerson` (plus `_RM_On` / `_RM_Off`) |

**[`DA_VaultingMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_VaultingMovement.json) (`BHVaultingData`)**

| Parameter | Value |
|---|---|
| VaultDistance | 74 |
| BaseTraversalSpeed | 600 |
| MovementSpeedInterpSpeed | 5 |
| ClampedTraversalDirectionMask | 131 |
| Montage choosers | `CHT_Traversal_Vaulting_ThirdPerson` (plus `_RM`) |

**First-person variants (`WDTraversingData`)**

| Asset | First-person montage chooser |
|---|---|
| [`DA_WDClimbingMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_WDClimbingMovement.json) | `CHT_Traversal_Climbing_FirstPerson` |
| [`DA_WDMantlingMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_WDMantlingMovement.json) | `CHT_Traversal_Mantling_FirstPerson` |
| [`DA_WDVaultingMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_WDVaultingMovement.json) | `CHT_Traversal_Vaulting_FirstPerson` |

### 3e. Ladder ([`DA_LadderClimbingMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_LadderClimbingMovement.json), `BHLadderClimbingData`)

| Parameter | Value |
|---|---|
| LadderEntryAngleThreshold | 60 |
| ClimbUp max / min speed / acceleration | 160 / 40 / 100,000 |
| ClimbDown max / min speed / acceleration | 160 / 40 / 500 |
| SlideDownSpeed / SlideDownAcceleration | 320 / 1000 |
| JumpOffForce | 300 |
| Transition curves (indices 1 to 4) | 1: [`CRV_LMF_Ladder_ClimbOntoAnimation`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/MovementFeatures/Ladder/Curves/CRV_LMF_Ladder_ClimbOntoAnimation.json) (0.25 s); 2: [`CRV_LMF_Ladder_ClimbOntoFromTopAnimation`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/MovementFeatures/Ladder/Curves/CRV_LMF_Ladder_ClimbOntoFromTopAnimation.json) (0.75 s); 3: [`CRV_LMF_Ladder_ClimbOntoAnimation`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/MovementFeatures/Ladder/Curves/CRV_LMF_Ladder_ClimbOntoAnimation.json) (0.25 s); 4: [`CRV_LMF_Ladder_ClimbOffAtTopAnimation`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/MovementFeatures/Ladder/Curves/CRV_LMF_Ladder_ClimbOffAtTopAnimation.json) (1.0 s) |
| InputMappingContext | [`IMC_LadderClimbing`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IMC_LadderClimbing.json) |

Index 0 is not present in the export. The four entries are as listed.

### 3f. Swimming, no-clip, vehicle, weight, ragdoll

**[`DA_SwimmingMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_SwimmingMovement.json) (`BHMoverSwimmingDataAsset`)**

| Parameter | Value |
|---|---|
| WaterAcceleration | 4000 |
| InputDeceleration | 500 |
| InputMappingContext | [`IMC_Player_Swimming`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IMC_Player_Swimming.json) |

**[`DA_NoClipMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_NoClipMovement.json) (`BHMoverModeData_NoClip`)**: one property, the InputMappingContext [`IMC_Player_NoClipping`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IMC_Player_NoClipping.json).

**[`DA_VehicleMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_VehicleMovement.json) (`WDVehicleData`)**

| Parameter | Value |
|---|---|
| EntryForceCompleteActionTags | Sprint, TacSprint, Binoculars.ADS, RangeFinder.ADS, Weapon.ADS, Weapon.Bipod |
| LeaveForceCompleteActionTags | Binoculars.ADS, RangeFinder.ADS, Weapon.ADS |
| HitValidationBoundsMultiplier | 2 |

**[`DA_CharacterWeight`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_CharacterWeight.json) (`WDMoverWeightData`)**

| Class (tag) | MinWeight | Gameplay effect |
|---|---|---|
| `State.Player.Weight.Lightest` | 0 | none |
| `State.Player.Weight.Light` | 10,000 | `GE_Player_Weight_Light_C` |
| `State.Player.Weight.Medium` | 17,000 | `GE_Player_Weight_Medium_C` |
| `State.Player.Weight.Heavy` | 27,000 | `GE_Player_Weight_Heavy_C` |
| `State.Player.Weight.SuperHeavy` | 40,000 | `GE_Player_Weight_SuperHeavy_C` |

The weight unit is not stated.

**[`DA_WDRagdollMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_WDRagdollMovement.json) (`WDRagdollMovementData`)**

| Parameter | Value |
|---|---|
| PhysicsAsset | `PA_TPCharacter_Simplified_Physics` |
| SimulationRoot / CapsuleTarget | `pelvis` / `spine_04` |
| CapsuleProxyCollisionProfile | `RagdollProbe` |
| CapsuleProxy linear limit | Limited on all axes, stiffness 250, damping 2, soft |
| Replicated body `pelvis` | linear break 300, angular break 500, linear plasticity 0.1, angular plasticity 10, shock propagation 0.3 |
| DriveForcesBlendTime / DriveForcesTargetMultiplier | 0.75 / 0.12 |
| MeshCollisionProfile | `Ragdoll` |

The bone lists are hashed keys, but their values are readable. One list has 12 bones: pelvis, spine_02, spine_03, spine_04, upperarm_r, lowerarm_r, upperarm_l, lowerarm_l, thigh_l, calf_l, thigh_r, calf_r. A second has upper arms and thighs, and a third has feet and calves. A value of 200 is stored under a hashed key and is not named.

**Empty assets (no properties exported):** [`DA_BipodMountingMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_BipodMountingMovement.json) (`WDBipodMountingData`) and [`DA_DummyMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_DummyMovement.json) (`BHPawnMoverModeData`).

---

## 4. Curves (39 assets)

### 4a. Float curves

| Curve | Keys | Points (time, value) | Use (from folder / name) |
|---|---|---|---|
| CRV_Camera_LockSmoothCurve_BodyDragging | 2 | (0, 1), (0.8, ~0) | Smooth camera lock release, body dragging |
| CRV_Camera_LockSmoothCurve_Climbing | 2 | (0, 1), (1, ~0) | Smooth camera lock release, climbing |
| CRV_Camera_LockSmoothCurve_Mantling | 2 | (0, 1), (1, ~0) | Smooth camera lock release, mantling and vaulting |
| CRV_Camera_LockSmoothCurve_ProneYaw | 2 | (0, 1), (0.8, ~0) | Smooth yaw lock, prone |
| CRV_JumpHeightScalar | 2 | (0, 0.5), (1, 1) | Scales jump height |
| CRV_LandSlowdownFriction_Scale | 3 | (0.5, 1), (39.9, 1), (110, 1.625) | Friction after landing, by speed |
| CRV_LandSlowdownFriction_Scale_Time | 2 | (0.1, 0.8), (75, 1.088) | Duration of landing friction |
| CRV_StanceSpeedStaminaMultiplier | 2 | (0, 0.4), (1, 1) | Speed multiplier as stamina falls |
| CRV_StanceStaminaMultiplier | 2 | (0, 0.4), (1, 1) | Stamina regen multiplier by stance |
| CRF_Falling_SurfaceAngleToAirControl | 2 | (0, 0), (90, 1) | Air control by surface angle (degrees) |
| CRF_Falling_SurfaceAngleToPushOffForce | 2 | (0, 1000), (90, 0) | Push-off force by surface angle |
| CRV_Lean_FromLeft / CRV_Lean_FromRight | 2 | (0, 0), (1, 1) | Unlean from left and right |
| CRV_Lean_ToLeft / CRV_Lean_ToRight | 3 | (0, 0), (0.4, 0.8), (1, 1) | Lean to left and right |
| CRV_CrashLandingTime | 2 | (0.755, 0.398), (362, 1.125) | Crash-landing time |
| CRV_Climbing_HeightSpeedMultiplier | 2 | (0, 0.92), (1, 1) | Climb speed by height |
| CRV_Mantling_HeightSpeedMultiplier | 2 | (0, 1), (1, 0.7) | Mantle speed by height |
| CRV_Mantling_TransitionDepth | 2 | (0.1, ~0), (0.7, 1) | Mantle transition depth |
| CRV_Vaulting_HeightSpeedMultiplier | 2 | (0, 1), (1, 0.5) | Vault speed by height |
| CRV_Vaulting_SpeedMultiplier | 2 | (0, 1), (0.5, 1) | Vault speed profile |

### 4b. Vector curves

| Curve | Axes with keys | Range | Use |
|---|---|---|---|
| CRV_HeavyBreathingOffset | X (4 keys), Y (4 keys) | X -0.5 to 1.5, Y -1 to 1 | Camera offset while breathing heavily |
| CRV_StanceTransition_CameraOffset_CrouchToProne | X (6 keys) | X -27.9 to 0 | Camera offset during stance change |
| CRV_StanceTransition_CameraOffset_ProneToCrouch | X (3 keys) | X -22.5 to 0 | Camera offset during stance change |
| CRV_StanceTransition_CameraOffset_StandToCrouch | none | - | Empty in the export |
| CRV_StanceTransition_CameraOffset_CrouchToStand | none | - | Empty in the export |
| CRV_StanceTransition_CameraOffset_StandToProne | none | - | Empty in the export |
| CRV_StanceTransition_CameraOffset_ProneToStand | none | - | Empty in the export |
| CRV_CrashLandingOffset | X (4 keys) | X -505 to 88.5 | Camera offset during crash landing |
| CRV_CrashLandingScalar | X (2 keys) | X 0.022 to 0.05 | Scalar for crash-landing offset |
| CRV_Climbing_ScaleOver_TransitionOffset | 1 key | ~0 | Scale-over offset (climbing) |
| CRV_Climbing_ScaleOver_TransitionWeight | X, Y, Z (2 keys each) | 0 to 1 | Scale-over blend weight (climbing) |
| CRV_Climbing_TransitionWeight | 2 keys | 0 to 1 | Traversal blend weight (climbing) |
| CRV_Mantling_ScaleOver_TransitionOffset | 1 key | ~0 | Scale-over offset (mantling) |
| CRV_Mantling_ScaleOver_TransitionWeight | X, Y, Z (2 keys each) | 0 to 1 | Scale-over blend weight (mantling) |
| CRV_Mantling_TransitionWeight | X, Y, Z (2 keys each) | 0 to 1 | Traversal blend weight (mantling) |
| CRV_Vaulting_TransitionOffset | Z (3 keys) | Z ~0 to 45 | Vault transition offset |

### 4c. Curve tables

| Table | Row | Keys | Points (time, value) |
|---|---|---|---|
| CT_HeavyBreathing | `SpeedByScale` | 2 | (0, 0.2), (3, 2) |
| CT_HeavyBreathing | `IntensityByScale` | 2 | (0, 0), (2, 10) |
| CT_DoorMovement | `Door Breach Ramp In and Out` | 3 | (0, 1), (0.3, 0.65), (1, 1) |

**Notes**

- Four of the six stance-transition vector curves are empty in the export (StandToCrouch, CrouchToStand, StandToProne, ProneToStand). Only CrouchToProne and ProneToCrouch carry keys, so the camera's stance-change offset is only defined for those two transitions in this dump.
- Vector curves store their data as one `FloatCurves` array with one entry per axis. Keys sit only on the axes listed above.
- Time axes are not labelled. Some look normalized (0 to 1), others are clearly not (up to 362 for crash-landing time, up to 110 for landing friction). The units are not stated.

---

## 5. Input Map ([`IMC_MoverPlayer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Input/IMC_MoverPlayer.json), 26 mappings)

| Action | Keys (keyboard / gamepad) | Notes |
|---|---|---|
| IA_Player_MoveDirectional | W, S, A, D / Gamepad_Left2D | Keyboard uses swizzle and negate modifiers. Gamepad has dead-zone and reroute modifiers |
| IA_Player_Jump | SpaceBar / Gamepad_FaceButton_Bottom | |
| IA_Player_Sprint_Toggle | LeftShift / Gamepad_LeftThumbstick | |
| IA_Player_TacticalSprint_Toggle | LeftShift / Gamepad_LeftThumbstick | Same keys as Sprint_Toggle |
| IA_Player_Crouch | C | |
| IA_Player_Prone | LeftControl | |
| IA_Player_CrouchProne | Gamepad_FaceButton_Right / (none) | Second entry has no key |
| IA_Ping | MiddleMouseButton / Gamepad_RightThumbstick | |
| IA_Player_CancelClimbing | SpaceBar / Gamepad_FaceButton_Bottom | Same keys as Jump |
| IA_Player_Traverse | SpaceBar / Gamepad_FaceButton_Bottom | Same keys as Jump |
| IA_Player_SlowWalk | LeftAlt | |
| IA_Player_CutParachute | C / Gamepad_FaceButton_Right | Same key as Crouch |
| IA_Player_Lean_Left | Q | |
| IA_Player_Lean_Right | E | |

**Shared keys:** `C` is bound to both Crouch and CutParachute, and `SpaceBar` is bound to Jump, CancelClimbing, and Traverse. The export does not say how the game chooses between them. It presumably depends on which action is active (for example, the parachute action only exists while parachuting), but that is not confirmed here.

---

## 6. Ladder Data ([`DA_Ladder_Industrial`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Blueprints/Ladders/LadderData/DA_Ladder_Industrial.json), `PDA_LadderData_C`)

| Part | Mesh |
|---|---|
| TopMesh | `SM_Climbable_Fixed_Ladder_Top_01` |
| MiddleMesh | `SM_Climbable_Fixed_Ladder_01` |
| BottomMesh | `SM_Climbable_Fixed_Ladder_01` |

The middle and bottom segments share one mesh. This is a single ladder variant (Industrial).

---

## 7. How Values Combine

- **State modifiers.** A state applies when its conditions pass (section 2). Its camera locks then limit how far the camera can move from the body. Pitch and yaw lock angles are the limits. Smoothing curves ease the lock on and off. Priority presumably decides which state wins when several are active, but the export does not say so. It has priorities for 12 states only, and the rule for ties is not in the dump.
- **Stamina.** Jumping costs 50 from a 150 pool, regenerating at 50 per second, with a 0.05 s cooldown. Each stance carries a `StanceStaminaCost` of 20 (stand), 30 (crouch), or 50 (prone); how that cost is charged is not stated. Parachute pull-up costs 50 per second and regenerates at 30. These are all tied to the same stamina pool.
- **Ground vs body drag.** The body-drag asset (section 3a) reuses the base ground numbers and adds a backward strafe scale of 0.35. It drops the sprint block timers (`BlockSprintTime`, `BlockTacSprintTime`) and the prone feet check. Body dragging is therefore not a separate speed model. It is the ground model with a different input map and different rules around sprinting.
- **Falling and parachute.** Landing damage comes from a curve keyed by impact speed ([`CRV_LandingPunishment_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_LandingPunishment_Damage.json), [`CRV_ParachutePunishment_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_ParachutePunishment_Damage.json)). Air control and push-off are set per surface angle ([`CRF_Falling_SurfaceAngleToAirControl`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Curves/Falling/CRF_Falling_SurfaceAngleToAirControl.json), `..._PushOffForce`).
- **Weight.** Each weight class applies one gameplay effect (`GE_Player_Weight_*`) once the character's weight passes its threshold. The effects themselves are not in this category.

---

## 8. Still Not Pulled / Limitations

- **Empty assets.** [`DA_BipodMountingMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_BipodMountingMovement.json) and [`DA_DummyMovement`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Settings/DA_DummyMovement.json) have no exported properties. Their values, if any, are not in the dump.
- **Empty stance curves.** Four of six stance-transition curves have no keys in the export (section 4b). Their intended camera motion cannot be read from this dump.
- **Priority semantics.** Priority values exist on 12 states, and their ordering is not documented in the export. Whether a higher number wins, and how ties are broken, is not confirmed.
- **Description mismatch.** The `VehicleCritical` state's description reads "critical/dead state and in a vehicle", but its state query lists only `State.Player.Vitality.Critical`. The export does not contain a Dead tag there. The discrepancy is noted as exported.
- **Unnamed keys.** Some properties use hashed keys (for example the ragdoll bone lists, the body-drag trace channel, and the ragdoll value 200). Their values are reported by position and value, and their property names are not known.
- **Blueprint and referenced-only assets.** `B_CharacterModifier_IgnoreLookInput_C` and `B_CameraModifier_HeavyBreathing_C` are blueprints, so their logic is not in the export. Montage choosers (`CHT_*`), animations (`A_TP_*`), gameplay effects (`GE_*`), and the `BHFloatModifier_Operation` sub-objects are referenced but not expanded here.
- **Query expansion.** The `AutoDescription` strings are the readable form of each state query. The encoded `QueryTokenStream` was not decoded, so the descriptions are the source of truth for the logic in this doc.
- **Units.** Speeds, stamina, heights, weights, and curve time axes have no units in the export. Values are reported as stored.
  - **See [`docs/UNITS.md`](../docs/UNITS.md)** for the project-wide units reference (UE 5.7 defaults + Wardogs-specific suffixes).
- **Input resolution.** The export does not say how shared keys are resolved between actions (section 5).
