---
title: "Vehicles"
redirect_from: ["/Wardogs_Vehicles_v2.html", "/Wardogs_Vehicles_v2"]
parent: "Vehicles"
description: "Folder Inventory, Vehicle Identity, Rigid Body, Engine, Drag, Flight Characteristics"
---

# Wardogs — Vehicles Reference
*Extracted from cooked game data (`Wardogs/Content/Vehicles`, 121 JSON files, all parsed). Multi-object files were split on each `--- export:` header; the first export is the asset, later exports are its sub-objects (input triggers, modifiers, curve keys, etc.). Build `++Wardogs+Live-CL-516586`, UE 5.7.*

> **Scope note:** this folder defines **one complete vehicle**: the **FWG_01 fixed-wing airplane** (platform `VP_FWG_01`, variant `VV_FWG_01_Default`). It also holds the shared vehicle input mappings, interaction contexts, camera spring arms, a free-vehicle spawner rule set, and helicopter/tracked-vehicle *curves* that are referenced by the airplane or left unused. Stats for Humvee, Kodiak, Littlebird, tanks etc. are **not** in this folder (see section 12).

> **Unit note:** the export carries unit suffixes in property names where they exist (`_n` newtons, `_m`, `_cm`, `_mps`, `_degps`, `_deg`, `_KMPH`). Anything without a suffix is shown as exported with its unit marked "not stated".

---

## Season 02 update (2026-10-15)

- **Countermeasures input renamed.** `IA_Vehicle_FireFlares` is replaced by `IA_Vehicle_FireCountermeasures` (InputTag `Input.NamedActions.Vehicle.FireCountermeasures`). The action count stays at 77. The keys are unchanged: V on keyboard, DPad_Up on gamepad, and the HOTAS flares button.
- **Supply crate gamepad binding added.** `Gamepad_DPad_Up` now triggers `IA_Vehicle_Deploy_SupplyCrate` in the land, rotary driver and rotary driver-gunner contexts.
- **Trigger key names.** `Gamepad_LeftTriggerAxis` / `Gamepad_RightTriggerAxis` are now `Gamepad_LeftTrigger` / `Gamepad_RightTrigger` for Collective (rotary driver and driver-gunner) and Weapon Focus (mounted gunner).
- **Mapping counts per context (old → new):** `IMC_DefaultVehicleInputs` 22 → 21 (`ChangeSeat_0` loses its `Gamepad_FaceButton_Right` binding), `IMC_LandVehicles_Driver` 40 → 41, `IMC_RotaryVehicles_Driver` 37 → 38, `IMC_RotaryVehicles_DriverGunner` 42 → 43.
- No input contexts were added or removed. The 11 mapping contexts and the 77 input actions are unchanged in number.

Full before/after list: [Season 2 Changes → Vehicles]({{ '/season-2-changes/vehicles.html' | relative_url }}).

---

## 1. Folder Inventory

| Subfolder | Files | Main object types | What it is |
|---|---|---|---|
| `Inputs/` | 88 | `BHInputAction` (77), `BHPlayerMappableKeySettings` (8), `InputMappingContext` (3) | Vehicle input actions and key bindings. The other 8 mapping contexts sit as sub-exports inside their `IMC_*` files (11 contexts in total, section 8b) |
| `Pawns/Air/Airplane/FWG_01/Data/` | 16 | `BHAirplaneBodyDataAsset`, `BHAirplaneDragDataAsset`, `BHAirplaneEngineDataAsset`, `BHAirplaneFlightDataAsset`, `BHAirplaneVehicleConfigDataAsset`, `MRotaryVehicleSpringArmDataAsset`, `BHRotaryVehicleSensorsDataAsset`, `BHSeatSettingsDataAsset`, `WDAttributeEffectsTrigger_VehicleHealth`, `MAirplaneInputControlsDataAsset`, `CurveFloat` x5, `CurveTable` x1 | The FWG_01 airplane |
| `Pawns/Air/Helicopter/Data/Curves/` | 6 | `CurveFloat` x5, `CurveVector` x1 | Helicopter aero/assist curves (referenced by the airplane, see section 12) |
| `Pawns/Tracked/Curves/` | 1 | `CurveFloat` | APC torque curve (not referenced by anything in this dump) |
| `Platforms/Air/` | 1 | `ModularVehiclePlatform` | `VP_FWG_01` |
| `Variants/Air/` | 1 | `ModularVehicleVariant` | `VV_FWG_01_Default` |
| `Interaction/` | 2 | `WDVehicleInteractionContextsData` | Vehicle interaction context tables |
| `Shared/` | 2 | `CurveFloat` | Player-vs-vehicle collision curve, rotation damage multiplier |
| `Weapons/WeaponExtensions/ProjectileActors/` | 3 | `MVehicleSpringArmDataAsset` | Weapon-camera spring arms (155mm, 120x800mm, drone) |
| `FreeVehicle/Data/` | 1 | `WDFreeVehicleSpawnerDataAsset` | `DA_FreeVehicleSpawner_Rules` |

---

## 2. Vehicle Identity

| Asset | Key value |
|---|---|
| Platform `VP_FWG_01` | Implementation blueprint `B_FWG_01_C`; spawn bounds Min (-969.2, -664.4, -3.8) to Max (967.6, 664.4, 576.8) |
| Platform fragments | `Config` (`MVF_VehicleConfig_0`, enabled), `Seats` (`MVF_Seats`, enabled) |
| Variant `VV_FWG_01_Default` | `VariantID` = `Vehicle.Variant.Air.Airplane.FWG.Default`; `bIncludeInBuildCommandLine` = true; base = `VP_FWG_01` |
| Vehicle class tag | `State.Player.Vehicle.Airplane` |
| Config asset `DA_FWG_01_Config` | Bundles Body, Engine, Drag, FlightCharacteristics, GameplaySystems, CameraBehaviourSettings, SensorsData, InputControls |
| Destroyed mesh | `SM_FWG_01_Destroyed` |

---

## 3. Rigid Body, Engine, Drag

### 3a. Body (`DA_FWG_01_Body`, `BHAirplaneBodyDataAsset`)

| Property | Value |
|---|---|
| Mass override | **10,000** (unit not stated, likely kg) |
| Inertia tensor override (X / Y / Z) | 600,000,000 / 160,000,000 / 250,000,000 |
| Centre of mass override | (-150, 0, 0) |
| Max angular velocity override | **180 deg/s** |

### 3b. Engine (`DA_FWG_01_Engine`, `BHAirplaneEngineDataAsset`)

| Property | Value |
|---|---|
| Max engine thrust | **226,800 N** (`MaxEngineThrust_n`) |
| Min engine thrust | 0 N |
| Thrust origin (local) | (-700, 0, 0) |
| Thrust direction (local) | (1, 0, 0) |
| Fan RPM ramp up / down | 5,000 / 5,000 per second |

### 3c. Drag (`DA_FWG_01_Drag`, `BHAirplaneDragDataAsset`)

| Property | Value |
|---|---|
| Air density at sea level | 0.00125 (as exported; unit not stated) |
| Front / rear / side / top / bottom area | 4,000 / 3,500 / 5,000 / 2,800,000 / 2,800,000 |
| Drag coefficient | 0.0056 |
| Yaw / Pitch / Roll angular-velocity-induced drag torque coef | 2.4e12 / 1.2e13 / 9.5e11 |
| Pitch / Yaw / Roll linear-velocity-induced drag torque coef | 90,000 / 70,000 / 0.18 (roll linear) |
| Yaw skid-angle curve | `CF_YawDragAngle_AggressiveNearZero` (helicopter folder) |
| Pitch angle curve | `CF_PitchDragAngle` (helicopter folder) |
| Reverse yaw correction coef | 0.8 |
| Draw debug lines | true |

### 3d. Vehicle config (`DA_FWG_01_Config`, `BHAirplaneVehicleConfigDataAsset`)

| Field | Value |
|---|---|
| Sub-assets | Body / Engine / Drag / FlightCharacteristics / GameplayConfig / SensorsData / InputControls all point to `DA_FWG_01_*` |
| Third-person and first-person camera | Both use `DA_FWG_01_CameraBehaviourSettings` |
| Horn minimum hold time | 0.05 s |
| Gameplay cue tags | Dust kickup `GameplayCue.Vehicle.DustKickup`; engine loop `GameplayCue.Vehicle.Engine.Running.FWG_01`; collision `...Collision.FWG_01`; destroyed `...Destroyed.FWG_01`; post-destroyed `...PostDestroyed.FWG_01`; seat change `GameplayCue.Vehicle.ChangedSeats`; enter `GameplayCue.Vehicle.Enter`; exit `GameplayCue.Vehicle.Exit`; chase cam toggle `GameplayCue.Vehicle.ToggleChaseCam` |
| Exit damage curve | `CRV_ExitVehiclePunishment_Damage` (player curves folder) |
| Extensions | `CBM` -> `DA_Vehicle_Air_Helicopter_CBM_Map`; `Audio` -> `DA_Vehicle_Helicopter_Shared_Audio` (shared helicopter audio) |

---

## 4. Flight Characteristics (`DA_FWG_01_FlightCharacteristics`, 23 exports)

### 4a. Aerodynamic surfaces (12 airfoils)
Lift-force origin is in cm (`LiftForceOrigin_LS_cm`); area is `SurfaceArea_m`.

| # | Airfoil | Area (m²) | Incidence (deg) | Max +/- deflection (deg) | Input mode | Extendable | Lift origin (LS cm) |
|---|---|---|---|---|---|---|---|
| 0 | Fuselage | 10 | 0 | 0 / 0 | Direct | no | (-100, 0, 0) |
| 1 | Airbrake | 30 | -45 | 0 / 0 | Direct | **yes** | (50, 0, 50) |
| 2 | Left Wing | 130 | 2 | 0 / 0 | Direct | no | (-150, -300, 0) |
| 3 | Right Wing | 130 | 2 | 0 / 0 | Direct | no | (-150, 300, 0) |
| 4 | Left Aileron | 40 | 0 | 20 / 20 | Direct | no | (-250, -500, 0) |
| 5 | Right Aileron | 40 | 0 | 20 / 20 | Direct | no | (-250, 500, 0) |
| 6 | Left Flap | 30 | 2 | 18 / 0 | **Relative** | no | (-200, -250, 0) |
| 7 | Right Flap | 30 | 2 | 18 / 0 | **Relative** | no | (-200, 250, 0) |
| 8 | Left Elevator | 55 | 0 | 40 / 40 | Direct | no | (-600, -300, 0) |
| 9 | Right Elevator | 55 | 0 | 40 / 40 | Direct | no | (-600, 300, 0) |
| 10 | Left Rudder | 40 | 0 | 20 / 20 | Direct | no | (-600, -150, 75) |
| 11 | Right Rudder | 40 | 0 | 20 / 20 | Direct | no | (-600, 150, 75) |

Timing on every airfoil: extension and retraction time 1.0 s; force multiplier when retracted 0.0. Main lift multiplier (`AerodynamicSettings.MainLiftMultiplier`) = **0.4**.

The airbrake is the only extendable surface; the airbrake control row in 4b drives it with extension 1.0.

### 4b. Control mapping (which surfaces each control drives)

| Control | Airfoil | Deflection | Extension |
|---|---|---|---|
| Pitch | Left Elevator | 1.0 | 0.0 |
| Pitch | Right Elevator | 1.0 | 0.0 |
| Roll | Left Aileron | **0.3** | 0.0 |
| Roll | Right Aileron | **0.0** | 0.0 |
| Roll | Left Elevator | 0.0 | 0.0 |
| Roll | Right Elevator | 0.0 | 0.0 |
| Yaw | Left Rudder | -1.0 | 0.0 |
| Yaw | Right Rudder | -1.0 | 0.0 |
| Flaps | Left Flap | 1.0 | 0.0 |
| Flaps | Right Flap | 1.0 | 0.0 |
| Airbrake | Airbrake | 0.0 | **1.0** |

Throttle, wheel brake and pitch/roll/yaw/flap/airbrake controls are each a `BHRotaryMovementControl` sub-object with an assist stack (section 4d). The roll row is worth verifying: the right aileron deflection is exported as 0.0 while the left is 0.3, which looks asymmetric.

### 4c. Landing gear

| Wheel | Side | Bone (wheel / suspension / steer) | Braking | Steering strength / damping / max angle | Brake-steer influence |
|---|---|---|---|---|---|
| Nose | `NoseCenter` | `wheelF_J` / `wheelMechanismF_J` / `wheelMechanismRotateF_J` | 0 | 250 / 50 / 45 deg | 0.0 |
| Rear left | `RearLeft` | `wheelL_J` / `wheelMechanismL_J` | **1,000,000** | none | 0.2 |
| Rear right | `RearRight` | `wheelR_J` / `wheelMechanismR_J` | **1,000,000** | none | 0.2 |

Nose-wheel steering influence by forward speed (`Curve_FWG_01_NoseCenterWheel_SteeringInfluenceByForwardSpeedKmPH`): **1.0 at 0 and 50 km/h, falling to 0.0 at 100 km/h**.

### 4d. Other flight tuning

| Property | Value |
|---|---|
| Max angular velocity limit | **disabled** (`bEnableMaxAngularVelocity` = false); the 83 deg/s value is stored but inactive |
| Translational lift | 20% (`TranslationalLiftPercent`), ramps from 24 m/s to 34 m/s horizontal speed |
| Ground effect | altitude 8.38 m, falloff 8.38 m, **strength 0%** (disabled) |
| Pitch hover assistance curve | `CF_PitchHoverAssistance` |
| Rear rotor efficiency curve | `TestHelo_RearRotorEfficiency_Curve2000KG` (helicopter folder) |
| G-force control falloff | `CF_GForceControlFalloff_AprilKom` (helicopter folder) |
| Default FM assistance | Neutral lift on, rate lock on |
| Auto-trim table | `CurveTable_FWG_01_AutoTrimByAirspeedKmPH`: 22 rows named `Gear_{0,1}_Thrust_{0..100 step 10}` |

The assists are typed with helicopter categories (`EBHHeliAssistCategory::Core`, assist labels such as "Reduce pitch when exceeding GForce limit", "Stabilize after input released", "Engage when fully stopped"). See section 12.

The lift and drag curve keys, the nose-wheel steering curve, the 22 auto-trim rows, every assist body (PID gains, damping, throttle change rates) and a derived speed envelope are in [Fixed-wing flight model](../game-features/Wardogs_FixedWingFlightModel_v1.md).

---

## 5. Gameplay Systems (`DA_FWG_01_GameplaySystems`)

| Area | Setting | Value |
|---|---|---|
| Health | Initial vehicle health | **150** |
| Health | Damage entity tag | `Meta.Damage.Vehicle.Air.Rotary.LittleBird` (copied from the Littlebird) |
| Health | Player collision damage curve | `CRV_VehiclePlayerCollision` |
| Health threshold triggers, main health (`Attribute.Gameplay.Health`) | 1 trigger at **90%** | Above-threshold effects: none |
| Health threshold triggers, fuel tank (`Attribute.Gameplay.Health.FuelTank`) | 3 triggers at **90%, 50%, 0%** | Above-threshold effects: none |
| Fuel leak per second | Three `WDFuelComponentEffect` values: **0.1**, **0.4**, **0.5** | Sub-objects `_2`, `_3`, `_5`; which fuel threshold each drives is not stated in the export |
| Damage cues | `GameplayCue.Vehicle.Smoking`; `GameplayCue.Vehicle.HIDZ.Damaged.FuelComponent` | No lifetime (`bHasLifetime` false) |
| Countermeasures | Flares `Id.Item.Flares`; **3 starting**, active **3.5 s**; flare cue `GameplayCue.Vehicle.Countermeasures.Flares`; Niagara `NS_Flares` | |
| Targeting | Location offset (0, 0, 150) | |
| Add-fuel input action | `Input.NamedActions.HoldableItem.PrimaryUse` | |
| HUD | Driver HUD layout `UI.HUD.Layout.Vehicle.Crew.Air` | |
| Lock | Lock-state cue `GameplayCue.Vehicle.LockStateChange` | |

### Seats (`DA_FWG_01_SeatSettings`)
Two seat setups only:

| Seat role tag | Crew seat | Gunner | Exterior | Standing |
|---|---|---|---|---|
| `State.Player.Vehicle.Role.Driver` | **true** | false | false | false |
| `State.Player.Vehicle.Role.ActivePassenger` | false | false | false | false |

Both are exported with the identifier "Not Selected" and priority 0. No gunner seat exists on this airplane.

### Sensors (`DA_FWG_01_SensorsData`)

| Property | Value |
|---|---|
| Landing strut sensor boxes | 2 (left and right), extents 230 x 10 x 25, translated (23, +/-108, -3.5) |
| Altitude sensor length | 1,000 |
| On-ground collision channel | `ECC_GameTraceChannel1` |

---

## 6. Cameras

### 6a. Third/first-person behaviour (`DA_FWG_01_CameraBehaviourSettings`, `MRotaryVehicleSpringArmDataAsset`)

| Property | Value |
|---|---|
| Socket offset | (-750, 0, 300) |
| Target arm length | 1,000 |
| Pitch map (input -> output) | -45..45 -> -25..10 |
| Velocity map (input -> output) | 100..7,000 -> 0.3..5.0 (units not stated) |
| Default lerp speed | 5.0 |
| Camera behaviour min velocity | 1.0 |
| Camera lag / rotation lag speed | 5.0 / 3.0 |
| Camera lag max distance | 300 |
| Inherit roll | false |
| Rotation lag curve | `DA_FWG_01_CameraRotationCurve`: 4.0 at t=0, 4.0 at t=48, 14.0 at t=72 |
| FOV vs speed curve | `DA_FWG_01_SpeedFOVCurve` (see section 7) |

### 6b. Weapon spring arms (`Weapons/WeaponExtensions/ProjectileActors/`)

| Asset | Probe min dist | Camera lag speed | Rotation lag speed | Lag max dist | Notes |
|---|---|---|---|---|---|
| `DA_155mm_Expensive_Camera` | 20 | 4.0 | 14.0 | 1.0 | FP lag: yaw 12, pitch 30, roll 12 |
| `DA_120x800mm_Expensive_Camera` | 20 | 4.0 | 14.0 | 1.0 | Identical FP lag to 155mm |
| `DA_Drone_Camera` | 20 | **0.5** | 14.0 | 1.0 | Adds `bAllowAdditionalAxisRotationLagInFreeCam` = true |

All three share velocity range upper bound 100 and an empty FOV-vs-speed curve.

---

## 7. Curves

| Asset | Keys (time, value) | Notes |
|---|---|---|
| `DA_FWG_01_SpeedFOVCurve` | (0, 0), (8.13, 3), (59.93, 10), (218.56, 11), (240.42, 20), (269.43, 23) | FOV vs speed (x unit not stated) |
| `Curve_Symmetrical_LiftCoefFromAngleOfAttackDeg` | (-90, 0), (-45, -1.1), (-25, -0.5), (-16, -1.0), (0, 0), (16, 1.0), (25, 0.5), (45, 1.1), (90, 0) | Lift coefficient vs AoA (deg) |
| `Curve_DragCoefFromAngleOfAttackDeg` | (-180, 0.01), (-90, 2.5), (0.008, 0.01), (90, 2.5), (180, 0.01) | Drag coefficient vs AoA (deg) |
| `CF_PitchDragAngle` | (-180, 0), (-135, -0.707), (-90, -1), (-45, -0.707), (0, 0), (45, 0.707), (90, 1), (135, 0.707), (180, 0) | Helicopter folder; used by airplane drag |
| `CF_YawDragAngle_AggressiveNearZero` | (-180, 0), (-90, -1), (-32, -0.8), (-10.2, -0.5), (0, 0), (10.2, 0.5), (32, 0.8), (90, 1), (180, 0) | Helicopter folder; used by airplane drag |
| `CF_PitchHoverAssistance` | (-90, 0), (-60, 0.4), (-45, 1), (45, 1), (60, 0.4), (90, 0) | Hover assist |
| `TestHelo_RearRotorEfficiency_Curve2000KG` | (-40, 0.65), (0.7, 0), (20, 0.8), (40, 0.92), (80, 1), (120, 1), (160, 0.98) | Rear rotor efficiency |
| `Havoc_RearRotor_EfficacyCurve` | single key (0, 0) | Havoc rotor curve, effectively flat in this export |
| `CF_GForceControlFalloff_AprilKom` (CurveVector) | X: (5.8, 1.0); Y: (0.05, 1.0), (3.3, 0.4), (8.2, 0.25), (12.5, 0.2); Z: (-15, 0.3) | G-force control falloff, three axes |
| `CRV_TrackedVehicle_TorqueCurve_APC` | (1200, 2500), (2211.6, 1500), (3057.7, 500) | APC torque; no tracked vehicle in this dump uses it |
| `CRV_VehiclePlayerCollision` | (15, 0), (25, 40), (40, 75), (65, 110) | Vehicle-vs-player collision damage (input unit not stated; likely speed) |
| `DA_VehicleRotationDamageMultiplier` | (0, 1.0), (20, 1.2), (40, 1.5), (80, 1.8), (100, 2.5), (120, 3.5), (150, 10.0) | Damage multiplier ramp (input unit not stated) |

---

## 8. Input

### 8a. Input action inventory (77 `BHInputAction` assets, all `IA_Vehicle_*` except as noted)

| Group | Count | Examples (InputTag) |
|---|---|---|
| Vehicle controls | 30 | `Input.NamedActions.Vehicle.Airbrake`, `...AirplaneThrottleUp/Down`, `...Collective`, `...Cyclic`, `...Pedals`, `...Steering`, `...Throttle`, `...Brake`, `...Handbrake`, `...Horn`, `...GearShift1..6`, `...GearShiftR`, `...FireCountermeasures`, `...Deploy_SupplyCrate`, `...OpenGarageVendor`, `...CycleLockState`, `...AggressiveMode`, `...Crawl` |
| Camera | 11 | `Input.NamedActions.Vehicle.Camera.FreeLook`, `...FreeLookDirectional`, `...FreeLookReset`, `...HoldFreeLook`, `...LeftView`, `...RearView`, `...RightView`, `...ToggleFreeLook`, `...ToggleMode`, `...ZoomIn`, `...ZoomOut` |
| Seat change | 14 | `Input.NamedActions.Vehicle.ChangeSeat.Seat_0` ... `Seat_11`, `.Next`, `.Prev` |
| Weapon extension | 22 | `Input.NamedActions.Vehicle.WeaponExtension.Fire`, `...Reload`, `...Focus`, `...ADS`, `...Crouch`, `...CycleFireMode`, `...CycleWeapons`, `...Change.1..6`, `...ActiveReload.Up/Down/Left/Right`, `...Guidance.MoveDirectional`, `...RotationControl.Key/Mouse/Gamepad`, `...SpecialAction` |

Value types: 14 are `Axis1D`, 8 are `Axis2D`, 55 have no ValueType (digital). Accumulation is `Cumulative` on 15 actions. Trigger usage across the 77: `Released` 35, `Pressed` 31, `Down` 18, `Hold` 6, `Tap` 6, `TapXTimes` 1.

Modifiers present on the action itself: dead zone on Airbrake, AirplaneWheelBrake, GearUp and AggressiveMode; scalar on both flap actions; negate on ThrottleDown and RetractFlaps. Pedals, Cyclic and Throttle carry no action-level modifiers (their shaping lives in the mapping contexts, section 8b).

Named actions referenced by these mapping contexts but **defined outside this folder**: `IA_Ping`, `IA_Interaction_Next/Previous`, `IA_OpenVehicleInteractionMenu`, `IA_UI_RadialWheel_VoiceChat(+_ChordedAction)`, `IA_VoiceChat_ToggleTalk`.

### 8b. Mapping contexts (default key bindings, action <- keys)

| Context | Mappings | Actions | Representative bindings |
|---|---|---|---|
| `IMC_Airplane_Driver` | 29 | 15 | Cyclic: W/S/A/D, Gamepad_Left2D, MouseX/Y. Pedals: E/Q, Gamepad_RightX, MouseX. Throttle up X / down Z (gamepad triggers). Airbrake: SpaceBar. Flaps extend: Period, retract: Comma. Gear up: G. Wheel brake: LeftControl. Aggressive mode: LeftShift. Fire countermeasures: V. Free look LeftAlt / Gamepad_DPad_Left. Supply crate: G |
| `IMC_LandVehicles_Driver` | 41 | 27 | Throttle W / Gamepad_RightTriggerAxis. Steering A/D/Gamepad_Left2D/MouseX. Brake S / LeftTrigger. Handbrake SpaceBar / Gamepad_FaceButton_Bottom. Gears 1-6 = keys One-Six, reverse R. Crawl LeftControl. Horn H / LeftThumbstick. Garage vendor B. Lock state L. Camera views Left/Right/Down, zoom PageUp/PageDown. Supply crate DPad_Up |
| `IMC_TrackedVehicles_Driver` | 37 | 21 | Throttle W/S + triggers. Tracked steering A/D/Gamepad_LeftX/MouseX. Brake S. Handbrake SpaceBar. Crawl LeftControl. Countermeasures V / DPad_Up |
| `IMC_RotaryVehicles_Driver` | 38 | 16 | Collective LeftShift / LeftControl / triggers. Cyclic W/S/A/D, Gamepad_Left2D, MouseX/Y. Pedals E/Q, shoulders, MouseX. Countermeasures V / DPad_Up. Lock L. Supply crate G / DPad_Up |
| `IMC_RotaryVehicles_DriverGunner` | 43 | 18 | Driver bindings plus `Weapon_Use` LeftMouseButton / FaceButton_Bottom / SpaceBar, `Weapon_Reload` R |
| `IMC_MountedGunnerInput` | 37 | 20 | Fire: LeftMouseButton, Gamepad_RightTriggerAxis, SpaceBar. ADS RightMouseButton. Focus LeftShift. Reload R. Cycle fire mode B. Cycle weapons Z. Change weapon 1-6 = keys One-Six. Rotation control W/S/A/D or mouse. Crouch C. Special action SpaceBar |
| `IMC_DefaultVehicleInputs` | 21 | 17 | Interaction menu F. Camera mode C. Seats: F1-F12 (`ChangeSeat_0..11`), Next = Zero, Prev = Nine. Ping MiddleMouseButton |
| `IMC_VehicleActiveReload` | 12 | 4 | Active-reload arrows: Up W, Down S, Left A, Right D (and DPad) |
| `IMC_RotaryVehicles_Joystick` | 6 | 4 | HOTAS: Pedals = `HOTAS_Axis_Yaw`; Cyclic = `HOTAS_Axis_Roll` / `HOTAS_Axis_Pitch`; Collective = `HOTAS_Axis_Throttle`; Free look = `HOTAS_Axis_LookYaw` / `LookPitch` |
| `IMC_RotaryVehicles_JoystickActions` | 11 | 11 | HOTAS buttons: `HOTAS_Action_Fire`, `Reload`, `Flares`, `Horn`, `ToggleCameraMode`, `GarageVendor`, `CycleLockState`, `DeploySupplyCrate`, `Ping`, `VoipToggleTalk`, `FreeLookReset` |
| `IMC_VehicleInteractionCycleOptions` | 4 | 2 | Previous: MouseScrollUp (negated), DPad_Up. Next: MouseScrollDown, DPad_Down |

Each `BHPlayerMappableKeySettings` entry (8 mains and sub-objects inside the driver contexts) sets a user-rebindable slot. The `SettingBehavior` on each mapping is `InheritSettingsFromAction` or `OverrideSettings`; a few are `IgnoreSettings`.

---

## 9. Interaction Contexts

| Table | Configs | Entries |
|---|---|---|
| `VehicleInteractionContext_StationaryVehicles` | 3 | `B_InternalVehicleInteractionContext`, `B_VehicleExitInteractionContext`, `B_VehicleEnterInteractionContext_Stationary` |
| `VehicleInteractionContextsDefault` | 12 | `B_VehicleEnterInteractionContext`, `B_VehicleExitInteractionContext`, `B_InternalVehicleInteractionContext`, `B_VehicleToggleEngineInteractionContext`, `B_VehicleLockInteractionContext`, `B_VehicleKickPassengersInteractionContext`, `B_VehicleGarageVendorInteractionContext`, `B_VehicleSupplyCrateInteractionContext`, `B_VehicleInventoryInteractionContext`, `B_VehicleRepositionInteractionContext`, `B_VehicleWeaponRestockInteractionContext`, `B_VehicleLockedInteractionContext` |

Ordering (`FactionBasedOrdering`): `Enter.Driver`, `Enter`, `Unlock`, `Locking`, `SquadLock`, `Locked`. `NonFactionBasedOrdering`: `Enter.Driver`, `Enter`, `Unlock`, `Locking`, `SquadLock` (no `Locked`).

Almost every `Config` field is at default (`InteractionTag` and `InteractionPointTag` = `None`). The one explicit override is `B_InternalVehicleInteractionContext` with gamepad behaviour `EWDWorldInteractableContextBehaviour::Hold`.

---

## 10. Free Vehicle Spawner Rules (`DA_FreeVehicleSpawner_Rules`)

Three factions (`Meta.Alignment.Faction.Alpha`, `.Bravo`, `.Charlie`), each with the same three-rule set:

| Rule | Subject | Timer / delay | Score option | Vehicle to spawn | Max available | Removal | Passive | Constant tick |
|---|---|---|---|---|---|---|---|---|
| R0 | Spawn | none | AnyFaction | `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | 1 | RemoveOnSuccess (value 4) | true | false |
| R1 | Timer | **900 s** | HighestScoreFaction | none (acts as trigger, `OnSuccess = TriggerRule`, target rule 0) | 0 | DoNotRemove | false | true |
| R2 | Spawn | **1,200 s** | AnyFaction | `Vehicle.Variant.Air.Rotary.ROT_04.Default` | 1 | DoNotRemove | false | true |

Common fields: `SpawnOption = SpawnX`, `TimerOption = TimerXSeconds`, `RuleOption = RuleSuccess`, `VehicleOption = VehicleDestroyed`, `VehicleArgument` = FirstVehicle (R0, R2) or LastVehicle (R1), `ScoreValue` 0, `NumberOfVehicles` 0 or 1.

The rule-field meanings are read from enum names. Runtime behaviour (what "spawn X" and "timer X seconds" trigger) is not verified.

---

## 11. How Values Combine

- **Airplane lift:** the export lists each surface's area (`SurfaceArea_m`), incidence and the lift coefficient curve, plus `MainLiftMultiplier` 0.4. How these combine in the solver is not in the export. Control inputs move surfaces by the deflection values in section 4b, up to the per-airfoil max (for example elevators +/-40 deg, rudders +/-20 deg).
- **Health and fuel:** the airplane starts at 150 health. Threshold triggers sit at 90% (main health) and 90/50/0% (fuel tank). Three fuel-leak effects exist (0.1, 0.4, 0.5 per second). The export does not say which threshold drives which leak, and the threshold triggers have no above-threshold effects attached.
- **Parachute and camera numbers are separate systems:** the camera spring arms (section 6) are per-weapon and do not feed flight.

---

## 12. Oddities and Things to Verify

- **Helicopter data reused by the airplane.** `DA_FWG_01_FlightCharacteristics` references `TestHelo_RearRotorEfficiency_Curve2000KG`, `CF_GForceControlFalloff_AprilKom`, and `CF_PitchHoverAssistance`. The airplane's drag uses `CF_PitchDragAngle` and `CF_YawDragAngle_AggressiveNearZero`. The assist stack is typed `EBHHeliAssistCategory::Core`. This looks like copy-over from the helicopter. Treat these as the airplane's live numbers, but expect the "Heli" naming to be inherited.
- **Littlebird damage tag.** The airplane's damage entity tag is `Meta.Damage.Vehicle.Air.Rotary.LittleBird`.
- **Asymmetric roll.** Right aileron deflection exported as 0.0 vs left 0.3 (section 4b).
- **Disabled systems.** Max angular velocity limit (83 deg/s) and ground effect strength (0%) are present but off.
- **Spawner rule references.** The spawner references `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` and `Vehicle.Variant.Air.Rotary.ROT_04.Default`. Neither asset is defined in this folder, and what `ROT_04` is was not checked.
- **Unused curve.** `CRV_TrackedVehicle_TorqueCurve_APC` is in `Pawns/Tracked/Curves` but nothing in this dump refers to it.
- **Stripped or hashed property names.** Several exports carry internal hash keys such as `_aaabefidebfnobnbphclo` (`_aaabelnajgoacnpmnokoe_$...` before 2026-10-18). These are unnamed properties and are not interpreted here.

---

## 13. Still Not Pulled / Limitations

- **No ground vehicle, tank, or helicopter definitions.** The Humvee, Kodiak, Bobcat, DuneBuggy, TNK_01, Littlebird, ROT_04, and Havoc vehicle assets (health, seats, weapons, mass) are not in this folder. Only curves and inputs for them are here. A search across other categories is needed.
- **Units not stated** for velocity maps, the SpeedFOV x-axis, air density, drag areas, and several curve inputs. Values are given as exported.
- **Default-valued fields are omitted** from exports. Where a property is missing (for example `Basic`-class fields), the runtime default is not known from the dump.
- **Assist and control graph.** The `BHRotaryMovementControl` assist bodies (PID, damping, smoothed influence) are present as sub-objects but only their labels and top-level modes were summarised.
- **Input sub-objects.** Modifier and trigger parameters (dead zones, scalars, actuation thresholds) are present on each action but were only spot-checked (for example Airbrake `InputTriggerReleased` ActuationThreshold 0.1).
- **Shared curves.** The collision and damage-multiplier curves are exported with no input-unit suffix; their meaning is inferred from the names.

## Change log

| Date | Change |
|---|---|
| 2026-10-18 | `data/` re-exported with the v2 usmap (names only; values unchanged): the example hashed key is now `_aaabefidebfnobnbphclo`. |
