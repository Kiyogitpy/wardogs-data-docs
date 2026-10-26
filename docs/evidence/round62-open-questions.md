# Round 62: seven open wiki questions (R62-RE)

Static analysis only. Nothing was run. Evidence levels: cooked data read (JSON under `data/` and `assets/data/`), extractor dump of cooked packages (`WdExtract dump`, `list`, `findname`), static disassembly and decompiled-corpus reading (RVAs, image base 0x140000000). Method as in rounds 58, 59 and 61. Extractor output and helper scripts are under `E:/Reverse_Engineer/wardogs_analysis/round62_re/` (`fn.py` corpus function printer, `scan.py` capstone pattern scan, `rep.py` page editor, `supp/` suppression Blueprints and curves, `pm/` physical materials, `miall/` all 3,192 `MI_*` material instances, `mi_phys.json` their physical-material census, `wall/`, `mid/`). No protected (virtualized) code was devirtualized and no row below needed it; no row is PROTECTED.

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1a | Acceleration units | FOUND | A rate per second in target speeds (Quake-style): speed gained per tick = acceleration x max(target speed, stop speed 100 cm/s) x dt. Full speed in about 1/acceleration s. |
| 1b | Slow-walk scales applied? | FOUND | Yes. Speed = MinSpeed + (MaxSpeed - MinSpeed) x scale (0.2, 0.4, 0.6). |
| 1c | Plain sprint stamina | ABSENT | None. Only the tactical-sprint flag charges stamina (20 per second). |
| 2 | Suppression in numbers | FOUND (effects); ABSENT (blur formula, no aim/sway/movement reader) | Strength 0 to 1 drives a screen effect and a camera shake only. Nothing else reads it. |
| 3a | Aim assist units | FOUND (derived); NATIVE (rate consumer not located) | Range in world units (cm, inferred); reticle sizes are fixed fractions of the reticle depth; rates are per-second speeds (inferred). |
| 3b | RPG-7 exclusion | FOUND | A zeroed settings asset with Off modes, shared by four launchers (not only the RPG-7). Reason ABSENT. |
| 4a | Thickness unit | FOUND | World units (cm), measured entry to exit along the shot, search up to 2 m; planar surfaces use stored thickness x 10. |
| 4b | World wall materials | FOUND | Physical material comes from the wall's render material instance, not the mesh; census below. Per-placed-wall assignment lives in the maps (not read). |
| 5 | Airplane flare points | FOUND | Native defaults: both points at (0, +200, -50) cm, i.e. the same spot 2 m right and 0.5 m below. |
| 6 | Second float behind 3.25 | FOUND | The sight's maximum variable zoom (`ZoomMultiplierMax`). |
| 7 | Drill per-second drain | ABSENT | No reader of `ChargesPerSecondConsumption` exists; native default 5.0, cooked drills 1.25, both unused. |

## 1. Movement

Mover mode `UBHMoverMode_GroundMovement` (vtable `0xAAEFB78`; WD subclass `0xB3E03A0`), data `UBHGroundMovementData`.

**1a. Acceleration units. FOUND.** Cooked `DA_GroundMovement` (`data/Wardogs/Content/MoverTesting/Settings/`): stance acceleration modifiers are `BHFloatModifier_Operation` with the default operation Set (enum 0, SDK `EBHFloatValueOperationType`): 7 Stand, 12 Crouch, 19 Prone. `Friction` 6.0, `MinSpeed` 80; `MaxSpeed` and `MaxStopSpeed` are not set, so the constructor defaults apply (`0x52834F0`, writes at `0x528357C..0x5283620`): Acceleration 7.0, MaxSpeed 536, MinSpeed 120, MaxStopSpeed 100.0, Friction 8.0. The step is `0x5287F80` (vtable slot 118, called per simulation tick with the tick length in milliseconds; `dt = ms x 0.001`):

- Friction: `speed' = max(speed - Friction x max(speed, MaxStopSpeed) x dt, 0)` (Friction from vtable +1176, MaxStopSpeed from +1168; the +1168 role is inferred from its use as the floor in both places).
- Wish velocity from `0x52867F0` (input direction x speed, below).
- Accelerate: `addspeed = wishspeed - dot(velocity, wishdir)`; `accelspeed = min(Acceleration(+1128, `0x528EA30`) x dt x max(wishspeed, stop speed), addspeed)`; velocity += accelspeed x wishdir. This is the Quake `Accelerate`, so the acceleration is unitless per second (multiples of the target speed). The WD subclass (`0x6DC0E20`) multiplies it by an attribute value (an "acceleration multiplier"; its value is a gameplay-effect number, not traced).

Derived times: standing 432 cm/s target, 7 x 432 = 3,024 cm/s^2, 0.14 s; crouched 270, 12 x 270 = 3,240, 0.08 s; prone about 80 with the 100 floor, 19 x 100 = 1,900, 0.04 s. Stop from 432 cm/s: exponential 6 per second down to 100 cm/s (0.24 s) then 600 cm/s^2 (0.17 s), about 0.4 s. All derived, not timed in play.

**1b. Slow-walk scales. FOUND.** `0x52867F0` (wish velocity, called from `0x5287F80` and `0x5288E30`). With the aux state at `a4`: `[+8]` bIsSprinting, `[+9]` bIsTacSprinting, `[+10]` bIsSlowWalking, `[+0x14]` the setting (EBHSlowWalkSettings). `v38` = MaxSpeed (vtable +1136, `0x5291720`), `v41` = MinSpeed (+1144, `0x52923C0`), `mag = clamp(|input|, 0, 1)`. If sprinting or tac-sprinting: `v38` unchanged. Else if `mag >= 1` and bIsSlowWalking: look up the setting in the mode data TMap at data `+0xD8` (`unk_143BD5570`, data pointer from `0x145280140`), `v38 = (v38 - v41) x scale + v41`. Else (analog tilt below 1) `v38 = (v38 - v41) x mag + v41`. Data: Slow 0.2, Moderate 0.4, Fast 0.6. Standing top speed 4.3 m/s gives about 1.5, 2.2, 2.9 m/s; crouched 2.7 gives 1.2, 1.6, 1.9; prone about 0.8 for all (top speed near the 0.8 minimum). Whether the ADS and weight-class slowdowns enter `v38` before the blend (probable, they are attribute multipliers in the WD override of the max-speed getter, `0x6DC1000`) was not traced: inferred. The earlier input-state write (`0x529BBD0`, aux `+0x14`) is the producer.

**1c. Sprint stamina. ABSENT.** The tac-sprint usage getter is vtable slot 158 (`0x5293970`, data `+0x148` = `TacSprintStaminaUsagePerSecond` 20; WD override `0x6DC1190` scales it by an attribute). Its only consumer in the mode code is `0x52899FB` (`call [rax+0x4F0]` at `0x5289AE9`), guarded by `cmp byte [rax+9], 0` (the tac-sprint flag) and spending through `0x52E2280`. The other stamina spender `0x52CBE50` is the jump and stance cost path. No code ties stamina to the plain sprint flag (`+8`); the plain sprint only has `BlockSprintTime` 0.8 s. Searched: `0x5280000..0x52C0000` for loads of `+0x148`, callers of `0x52E2280` and `0x52E0E30`.

Pages: `_wiki/game-mechanics/movement.md`.

## 2. Suppression

`UWDSuppressionComponent` (`vtable 0xB30BC18`) holds a map of two effect classes (SDK `SuppressionEffects`, `+0xE0`); cooked `B_CharacterSuppressionComponent` lists `WDSuppressionEffect_PostProcess` x2 (decay multiplier 0.4 default, 0.1 concussive) and `WDSuppressionEffect_CameraShake` x2. The weapon cue `GC_Weapon_Suppression.HandleSuppression` calls `WDMoverPlayerCharacter.GetSuppressionComponent` then `Suppress(type, NormalizedMagnitude)` (bytecode read, `supp/`); the backblast cue `GC_Weapon_BackBlast_Concussion` also references the component. The effect object keeps a strength float at `+0x28`: add (`0x6B7B340`, clamp(strength + x, 0, 1)), decay (`0x6B7BFF0`/`0x6B7C030`/`0x6B7C0B0`, strength = max(strength - dt, 0)), active test (`0x6B7BDD0`, strength above 1e-8). The post-process effect (`0x6B7B520`, `0x6B7C490`) feeds the strength into a scalar parameter of `MI_PP_Damage`; the camera-shake effect (`0x6B7B360`) starts the shake through the camera manager (vtable +2256).

Numbers (cooked, `supp/`): default shake `B_CameraShake_Suppression`: Duration 0.5, ChromaticAberration 4.5, LocationAmplitudeMultiplier 0.1125 (X 5.0, Y 0.5 at frequency 3), RotationAmplitudeMultiplier 0.45 at 12, FOV amplitude 0.9. `B_CameraShake_Suppression_Backblast`: Duration 0.5, BlendOut 0.3, ChromaticAberration 10, RotationAmplitudeMultiplier 2.0 (Pitch 8, Yaw 5, Roll 5), FOV amplitude 6. Post process: `PostProcessEffect.Suppression.Default` Duration 0 (intensity driven), `.Concussive` Duration 2.0 with a `DarkenProgress` curve. `MI_PP_Damage` has one `SuppressionIntensity` scalar (default 0) next to blur, darken, desaturation and vignette controls.

Not available: the material graph of `M_PP_Damage` is not in the export (the dump holds the parameter list only), so the blur amount per strength is ABSENT. No aim, sway, spread, recoil or speed effect: no Blueprint names `GetStrength`, `GetTimeSuppressed` or `GetEffect` (`findname` over `Wardogs/`: 0 packages for `GetTimeSuppressed` and `WDSuppressionComponent`; the component name appears only in the component Blueprint and the two cues), and `GetStrength` (`0x6B7C630`), `GetTimeSuppressed` (`0x6B7C650`) and `GetEffect` (`0x6B7C5A0`) have no direct native caller in the corpus `calls` table; the getter of the component (`0x6B7BB20`) is called only by `0x6B7B290` and `GetEffect`. Static, so a call through a virtual table or a stripped caller is not excluded.

Pages: `_wiki/game-mechanics/status-effects.md`.

## 3. Aim assist

**3a. Units. FOUND (derived) / NATIVE.** The module is a port of the Lyra aim-assist design (`BHAimAssist`: `BHAimAssistInputModifier`, `BHAimAssistSettingsData`, `FilterData`). Cooked settings (AR, SR, Melee, `Content/Items/Weapons/DA_AimAssistSettings_*.json`): reticle `ReticleDepth` equals `TargetRange` (30,000, 40,000, 800) and the reticle sizes are fixed fractions of it in every class: inner width 0.03 and height 0.024, outer and targeting width 0.09 and height 0.072 (AR 900/720/2700/2160 at 30,000; SR 1200/960/3600/2880 at 40,000; Melee 24/19.2/72/57.6 at 800). So the sizes are world units at the reticle depth and the angular size is constant: outer about 5.1 by 4.1 degrees, inner about 1.7 by 1.4 (derived: 2 atan(0.045) = 5.15, 2 atan(0.036) = 4.12). The range unit (cm) is inferred from the engine convention and from the plausibility of 300 m, 400 m and 8 m. The settings are read through the scalable-float getter `0x48AA770` (offsets 0x2C0, 0x2E8, 0x310 for the slow strengths were seen in the reticle blend at `0x6762290`); the code that applies `PullLerpInRate` (+0x210) and `PullLerpOutRate` (+0x238) was not located (scans for `mov e.., 0x210/0x238` and `lea` in `0x6700000..0x6780000` found only constructor hits). The "per second interpolation speed" reading is inferred from the names and the Lyra design; the Season 2 values 10 and 8 equal that design's defaults.

**3b. RPG-7 exclusion. FOUND.** `DA_AimAssistSettings_RPG`: `PullMode` and `PullModeADS` Off, every reticle, range, strength and rate field 0. Items pointing at it (scan of every `ID_*.json` for `AimAssistSettingsDataAsset`): `ID_RPG7`, `ID_Launcher_04` (9K333 Verba), `ID_MMGL` (MGL-40), `ID_CGM4` (MAAWS), `ID_ArtilleryBarrelTest`, `ID_TankBarrelTest`. So four player launchers have no aim assist, not only the RPG-7 (the wiki said one). No code or data states a reason (ABSENT).

Pages: `_wiki/game-mechanics/aim-assist.md`, `_wiki/patch-notes/season-2.md`, `_wiki/game-mechanics.md`, `content/Wardogs_MiscGameplayAssets_v1.md` (sentence 7e).

## 4. Penetration

**4a. Thickness unit. FOUND.** The result block's thickness (`+0`) is written by `0x6F2FC20` (called from `0x6F2F740`, consumed by `0x6F36190`). Planar branch (hit actor type byte `+176 == 1`): distance from the hit point to the plane offset by the material's thickness, in world units, then `x ProjectileSystemSettings.PlanarSurfaceThicknessScale` (+1816, `10.0`, `DefaultGame.ini`). Volumetric branch: a second trace of length `min(1.2 x half-diagonal of the hit part's bounds, 200)` along the shot from the entry point (`0x6F2FC20` tail), thickness = distance between entry and second hit; no second hit means no pass. Both are world distances; world units are centimetres (engine convention, inferred). The ray length cap is 200 units (2 m). The debug text in `0x6F36F40` prints speed as `cm/s x 0.01` m/s, consistent with centimetres.

**4b. World wall materials. FOUND (mechanism); the per-wall table is in map data not read.** World static meshes carry no physical material in their own export; the physical material is the `PhysMaterial` of the render material instance applied to them. Examples (`mid/`): `MI_Tiling_Stone_Wall_03` and `MI_Trim_Concrete_Plain_01a` give `PM_Concrete`, `MI_Tiling_Walls_Warehouse_400cm_MetalCorrugated` gives `PM_Metal`. Census of all 3,192 `MI_*` packages (`mi_phys.json`, 3,152 parsed): 1,824 name a physical material (Metal 682, Fabric 305, Concrete 137, Glass 71, Wood 65, Plastic 52, Head 48, Leaf 48, Dirt 43, Rubber 40, Paper 39, Body 34, Gravel 32, Brick 29, Asphalt 29, Bark 25, Rock 19, Plaster 17, Ceramic 13, Water 12, others fewer) and 1,328 name none (inherited from the parent material). The 256 `Environment/Architecture` material instances: Concrete 71, Metal 53, Brick 18, Wood 16, Plaster 11, Glass 8, Fabric 6, Rock 4, none 57; the 63 whose name contains "Wall": Concrete 40, Brick 10, Metal 4, Wood 1, Plaster 1, none 7. Physical-material densities (`pm/`, `Density`; used as `rho`, the larger of entry and exit): Concrete 8.5, Metal 7.0, MetalSheet 7.85, MetalSolid 7.0, MetalCorrugated 6.0, MetalWeak 2.0, Brick 5.2, Ceramic 4.5, Plaster 3.0, Rock 3.0, Gravel 3.0, Wood 2.56, Asphalt 2.4, Fabric 1.5, Soil 1.5, Dirt 1.25, Plastic 1.3, Rubber 0.7, Paper 0.85, GlassBulletProof 9.18; Glass and Body omit it (native default 1.0, inferred). The `PlanarThickness` values in the same dump read as denormal garbage (offset skew in the property map), so no planar thickness table is claimed. Which mesh a given map places where lives in the map packages, not read.

Pages: `_wiki/game-mechanics/penetration-and-ricochet.md`.

## 5. Airplane flare points

`FWDFlaresSettings` is at targeting settings `+0x60`, built by the settings constructor `0x766AEA0`: the flare left offset (struct `+0x20` = `+0x80`) is written `x = 0` (`0x766AF39`), `y = 0x4069000000000000 = 200.0` (`+0x88`), `z = 0xC049000000000000 = -50.0` (`+0x90`); the flare right offset (struct `+0x38` = `+0x98`) is `x = 0`, `y = 200.0` (`+0xA0`), `z = -50.0` (`+0xA8`). Both points are the same, (0, +200, -50) cm: 2 m to the right and 0.5 m below the vehicle origin (UE local +Y is right). `DA_FWG_01_GameplaySystems` sets only `StartingFlaresAmount` 3 and `FlaresActiveTime` 3.5 (`assets/data/vehicle-flares.json`), so these defaults apply. `GetTargetLocation` (`0x76B33C0`) picks the nearer of the two transformed points; with identical points the choice is moot. Static; not run.

Pages: `_wiki/vehicles/countermeasures-and-flares.md`.

## 6. Second float behind 3.25

The handlers `0x6C99E52` and `0x6C9A902` (attribute-changed callbacks of `UWDItemExtension_RangedWeapon`, `+0x128` = weapon component) pass `max(obj+0x3F8, this+0x454)` to `0x6B879E0`. `this+0x438` is a pointer into the extension's hash map at `this+0x3E8` (entries of 1,208 bytes, lookup `0x6C96FB0` keyed by the 8-byte value at `this+0x474`, assigned at `0x6C9BC3D` and `0x6C9DC95`), so `obj+0x3F8` is the same aiming-zoom float as the weapon-state `+0x3F8`. The float `this+0x454` is the upper limit of a zoom ramp: the ramp value `+0x3D4` is clamped to `[+0x450, +0x454]` (`0x6C94847`), grows by `+0x458` per step and eases by `+0x45C` (`0x6C99560`, `0x6C9ECB0`). That is `FWDVariableZoomData` (`bCanVariableZoom`, `ZoomMultiplierMin`, `ZoomMultiplierMax`, `MouseZoomMultiplierStep`, `ControllerZoomMultiplierStep`, `ZoomMultiplierInterpTime`, SDK `WDGame_structs.hpp` line 16108): `+0x450` Min, `+0x454` Max. The getter `0x6C97CE0` repeats the same `max(...)`. The copy from the sight data into the extension was not traced (inferred by role). Cooked variable-zoom sights: 10x Scope 6 to 10, 6x Scope 3 to 6, 1x-6x LPVO Short Dot 3 to 6, Frontier 2.5x-10x 2.5 to 10, Leatherwood ART II 3 to 9 (`AdsZoomMultiplier` 3, so its max, not its listed 3x, decides). Sights that cannot zoom have max 0 and use the fixed magnification.

Pages: `_wiki/attachments/sights-and-optics.md`, `_wiki/game-mechanics/controls-and-settings.md`.

## 7. Drill per-second drain

`UWDItemExtensionData_Battery` (SDK `BatteryRuntime_classes.hpp`) has `ChargesPerSecondConsumption` at `+0x48` and `ItemId` at `+0x4C`. Its constructor (`0x85568D0`) sets `+0x48 = 0x40A00000 = 5.0`; cooked drills set 1.25. The module's code is four functions plus the data getter `0x85567D0` (class cell `0xD3E4CA8`, whose only uses are inside `0x8556600` and `0x85567D0`); `0x85567D0` is called only by `UseCharges` (`0x8556C80`), `HasAnyCharge`, `RemainingChargeAmount`, `0x8556AE0` and `0x8556B90`, and a scan of `0x8550000..0x8570000` finds no load of `+0x48`. No other code references the data class cell, so no code reads the figure. The drills' own drain is the Blueprint hit notify calling `UseCharges(1)` (round 58). The range finder's 1 charge per 0.8 s is its own scope extension (`0x8631E90`). Status ABSENT (no reader), static.

Pages: `_wiki/equipment/drills.md`, `_wiki/equipment/batteries.md`.

## Wiki updates (done in this commit)

- `_wiki/game-mechanics/movement.md`: acceleration meaning and times, stopping time, slow-walk speeds, plain sprint costs nothing; "Not yet known" trimmed to one item.
- `_wiki/game-mechanics/status-effects.md`: what suppression does (screen effect, camera shake numbers, no aim or movement effect); unknown reworded to the blur formula.
- `_wiki/game-mechanics/aim-assist.md`, `_wiki/game-mechanics.md`, `_wiki/patch-notes/season-2.md`, `content/Wardogs_MiscGameplayAssets_v1.md`: units, reticle shape, launchers (four) have the assist off.
- `_wiki/game-mechanics/penetration-and-ricochet.md`: thickness unit, wall materials, density table, unknown trimmed.
- `_wiki/vehicles/countermeasures-and-flares.md`: airplane flare points.
- `_wiki/attachments/sights-and-optics.md`, `_wiki/game-mechanics/controls-and-settings.md`: the 3.25 test uses the maximum zoom.
- `_wiki/equipment/drills.md`, `_wiki/equipment/batteries.md`: no per-second drain.
- No generator change and no regenerated page.
