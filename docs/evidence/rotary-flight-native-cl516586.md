# Rotary flight model — native defaults and assist semantics — CL516586

This page closes the gap left open by the generated vehicle pages: [`Wardogs_VehicleConfigFields_v1.md`](../../game-features/Wardogs_VehicleConfigFields_v1.md) and [`Wardogs_VehicleControlAssists_v1.md`](../../game-features/Wardogs_VehicleControlAssists_v1.md) print `-` for every field a flight asset does not serialise and state that "the native default applies, not read". The constructor defaults are now read, so the effective value of every `BHRotaryFlightDataAsset` field is known, including the ones no shipped asset sets.

The same pass recovered the assist evaluation contract (`IsEnabled` → `GetInfluence` → body `Update`), the exact runtime semantics of `StabilizedAfterInputReleased` and `WasOnGroundAtStart`, and a data-consistent explanation of the MH-6's ~1.4 s press-to-lift-off delay.

Evidence class: **static reading of the shipped executable and cooked data. Nothing was executed.** Claims below are marked observed (binary read), data (cooked asset) or inferred where the step is a reading of names rather than decoded logic.

## Source and build identity

| Item | Value |
| --- | --- |
| Build | `5.7.4-516586+++Wardogs+Live-Wardogs` (manifest build 25937608) |
| Shipped client | `WardogsClient-Win64-Shipping.exe`, SHA-256 `1090559a81a9dda972f86c3d1c13577b747fa337d91ee300f70ad07f1900fea1` |
| Restored reference image (text read statically) | SHA-256 `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`, image base `0x140000000` |
| Canonical Dumper-7 v2 map | `5.7.4-516586+++Wardogs+Live-Wardogs.idmap`, SHA-256 `f4b2942331061187454b625821f8a6119b267551d22dc1cabbdf1a4f3ee1afdb` |
| Tooling | IDA Pro 9.5 + Hex-Rays headless (`idalib`), Capstone 5, Dumper-7 v2 map decoder |

Function addresses are RVAs in the restored image. Class and field layout come from the dumped declarations in [`sdk/raw/Mechanized_classes.hpp`](../../sdk/raw/Mechanized_classes.hpp) and [`sdk/raw/Mechanized_structs.hpp`](../../sdk/raw/Mechanized_structs.hpp), which were produced from this same build.

**Provenance limit:** the restored image is a third-party reconstruction; its producer and recipe remain unknown, and the historical reconstruction was not rerun for this page. Every RVA below was read in that image and cross-checked against the canonical map's vtable for the class named; selected-agreement reading is not a whole-executable provenance or runnability claim.

## 1. Constructor defaults for `BHRotaryFlightDataAsset`

### 1.1 Method

`UBHRotaryFlightDataAsset` is a `UDataAsset` with 30 own fields at `0x130` (class `0x160`, base `0x30`). Its UClass constructor is RVA `0x145384750` (449 bytes). The function installs vtable `0x14AB8B210`, which is `UBHRotaryFlightDataAsset_VFT` in the canonical map, and writes every field at the offset the SDK declaration gives.

The identification is independently attested by the save behaviour: all three shipped assets serialise `bEnableMaxAngularVelocity = false` although the constructor writes `true`. Under Unreal's tag-skip save rule a `false` would not be stored if it equalled the class default object, so the stored value proves the CDO value is `true` and that these assets were saved against this constructor. **Observed.**

### 1.2 Effective values

`absent → N` means the asset stores nothing and the constructor value `N` is effective. Curve pointers are `null` when absent; `-` in the control-force rows means the asset leaves that struct field at its default (zero), not that the feature is off.

| Field | Constructor | ROT_02 (Havoc) | ROT_03 (Little Bird / MH-6) | ROT_04 |
| --- | --- | --- | --- | --- |
| `LiftPitchAngle` | 0 | absent → 0 | absent → 0 | absent → 0 |
| `LiftForceOffset_LS` | (0, 0, 300) | absent | absent | absent |
| `RotorSettings.MaxLiftCoeff` | 1.77 | 1.8 | 1.25 | 5.75 |
| `RotorSettings.StallLiftCoeff` | 1.0 | absent → 1.0 | absent → 1.0 | 3.0 |
| `RotorSettings.BladeAngleOfAttackForZeroLift_deg` | −4 | absent → −4 | absent → −4 | absent → −4 |
| `RotorSettings.BladeAngleOfAttackForMaxLift_deg` | 18 | absent → 18 | absent → 18 | absent → 18 |
| `RotorSettings.BladeAngleOfAttackForStall_deg` | 25 | 40 | absent → 25 | absent → 25 |
| `RotorSettings.RotorRadius` | 415 | 600 | absent → 415 | 800 |
| `RotorSettings.LiftForcesAppliedAtRadius` | 330 | 1000 | absent → 330 | 275 |
| `RotorSettings.LowAltitude_m` | 0 | 40 | 75 | 50 |
| `RotorSettings.HighAltitude_m` | 5000 | 200 | 250 | 250 |
| `RotorSettings.MaxAltitude_m` | 5500 | 280 | 325 | 350 |
| `RotorSettings.LowAltitudeRotorEfficiency` | 1.0 | absent → 1.0 | absent → 1.0 | absent → 1.0 |
| `RotorSettings.HighAltitudeRotorEfficiency` | 0.5 | 0.65 | 0.75 | 0.65 |
| `RotorSettings.MaxAltitudeRotorEfficiency` | 0.2 | 0.4 | 0.45 | 0.4 |
| `RotorSettings.TailRotorNeutralTorque` | 300,000,000 | 600,000,000 | 600,000,000 | 600,000,000 |
| `PitchControlForce` | — | RotorBladeAngle, MaxTorque 4.8e9, Δ 1.3 | RotorBladeAngle, 4.8e9, Δ 2.0 | RotorBladeAngle, 4.8e9, Δ 6.0 |
| `RollControlForce` | — | RotorBladeAngle, 1.5e9, Δ 0.42 | RotorBladeAngle, 1.5e9, Δ 0.6 | RotorBladeAngle, 1.5e9, Δ 0.85 |
| `YawControlForce` | — | MaxTorque 330,000,100 | 37,000,000 | 500,000,000 |
| `CollectiveControlForce` | — | 400,000…2,800,000 N, blade Δ −0.5…10 | 400,000…2,800,000 N, Δ −3.0…14.5 | 400,000…3,400,000 N, Δ −1.9…10.67 |
| `_aaacdfalmgfnbmfhcjamk` (obfuscated name) | 4 | absent → 4 | absent → 4 | absent → 4 |
| `bEnableMaxAngularVelocity` | **true** | false | false | false |
| `MaxAngularVelocityDegPerS` | 3600 | 83 | 83 | 83 |
| `DefaultFMAssistanceLevel` | all false | bNeutralLift, bRateLock | bRateLock | bRateLock |
| `TranslationalLiftPercent` | 0 | 20 | 16 | 25 |
| `TranslationalLiftMinAtHorizSpeed_mps` | 8 | 24 | 20 | 24 |
| `TranslationalLiftMaxAtHorizSpeed_mps` | 12 | 34 | 28 | 34 |
| `GroundEffectAltitude_m` | **5.0** | absent → 5.0 | absent → 5.0 | absent → 5.0 |
| `GroundEffectFalloff_m` | 5.0 | 12 | 12 | 12 |
| `GroundEffectExp` | **2.0** | absent → 2.0 | 1.1 | absent → 2.0 |
| `GroundEffectStrengthPercent` | **20.0** | absent → 20 | absent → 20 | 30 |
| `SleepWaitingTime` | 5.0 | absent → 5.0 | 3 | 8 |
| `CyclicAttenuationMinSpeed_kmh` | **150** | absent → 150 | 200 | absent → 150 |
| `CyclicAttenuationMaxSpeed_kmh` | **300** | absent → 300 | absent → 300 | absent → 300 |
| `CyclicAttenuationFactor` | **0.35** | 0.45 | 0.6 | 0.45 |

Hashed `RotorSettings` members keep their obfuscated names in the export and are not reproduced here except where a value is quoted; they are not needed for any statement on this page.

### 1.3 What the table changes

- **Ground effect is a mixture, not a set.** No asset stores the four-field quartet. ROT_02 stores only `Falloff`; ROT_03 `Falloff` + `Exp`; ROT_04 `Falloff` + `Strength`. Effective values are: strength **20 / 20 / 30 %**, altitude **5 m** everywhere, falloff **12 m** everywhere, exponent **2 / 1.1 / 2**. Reading one asset and assuming the others share its ground-effect behaviour is wrong in both directions.
- **The angular-velocity cap is inert.** The constructor enables it at 3600 °/s; every shipped helicopter overrides the flag to `false`, so the authored `83` °/s value never applies. The shipped flight model runs on control forces (torques), not on an angular-velocity clamp.
- **Six fields are never set by any asset:** `LiftPitchAngle` (0), `LiftForceOffset_LS` (0, 0, 300), the obfuscated `_aaacdfalmgfnbmfhcjamk` (4), `GroundEffectAltitude_m` (5 m), `RollPitchYawStrengthCurve` (null) and `CyclicAttenuationMaxSpeed_kmh` (300 km/h).
- **ROT_03 inherits its rotor geometry entire:** radius 415, lift forces at 330, blade angle of attack −4/18/25, `StallLiftCoeff` 1.0 and low-altitude efficiency 1.0 all come from the constructor.

## 2. Assist evaluation contract

### 2.1 Three virtuals, one direction

The binary retains the `PURE_VIRTUAL` message strings, which name the interface and its source lines (all in `BHRotaryMovementControlAssist.h`):

| Virtual | Base implementation RVA | Source line | Role |
| --- | --- | --- | --- |
| `UBHRotaryMovementControlAssistCondition::IsEnabled` | `0x145368B30` | 318 | Gate: may this assist run this frame? |
| `UBHRotaryMovementControlAssistCondition::GetInfluence` | `0x145362F10` | 163 | Weight (0…1) from the In/Out interpolation ramps |
| `UBHRotaryMovementControlAssistBody::Update` | `0x14537A910` | 196 | Produce this assist's control value |

Each base implementation is the stock `PURE_VIRTUAL` body — a `checkf(..., "Pure virtual not implemented (%s)", L"UBHRotaryMovementControlAssist…")`. A condition therefore cannot contribute force directly; it gates and weights, and a body produces a value. **Observed.**

### 2.2 Bodies produce control values

- **PID body** (`UBHPIDRotaryMovementControlAssistBody::Update`, `0x14537A410`): computes the PID error from the condition-selected control value and target, then clamps the result against `OutputParams.MaxPIDOutput` (`[this+0x3C]`, symmetric min/max), applies `OutputType` (`Speed` integrates with `DeltaTime` and adds the processed input at `[ctx+0x2C]`; `Value` does not integrate), and runs an `FMSmoothingFilter` (`[this+0xC4]`) before writing the result. **Observed.**
- **Damping body** (`UBHDampingRotaryMovementControlAssistBody::Update`, `0x14537A380`): `timer += DeltaTime` at `[this+0x48]`, then evaluates the interpolation toward the target. The asset's `InterpTimeS` / `InterpSpeed` / `exp` therefore act in real frame time. **Observed.**
- **Set-to-value body** returns its stored `Value` with no time state. **Observed.**

All three shipped assets use `EBHRotaryMovementControlAssistOutputMode::Mixed` for **every** assist (29 on ROT_02, 39 each on ROT_03 and ROT_04); there is not one `Additive` instance. So the additive branch is untested by shipped data. **Data.**

### 2.3 Torque and angular velocity appear only outside the assist interface

Torque is introduced by the flight asset's control-force structs, not by assists. From the same header:

- `FRotationalControlForce { ERotationalControlType Type; float MaxTorque; float MaxRotorBladeAngleDelta; }` — pitch, roll and yaw.
- `FLinearControlForce { ELinearControlType Type; float MinForce; float MaxForce; float MinRotorBladeAngleDelta; float MaxRotorBladeAngleDelta; }` — collective.

The per-asset values are in section 1.2. A processed control value is mapped through these structs into rotor blade angle / torque, which is why the PID and damping bodies only ever return a normalised value. **Observed + data.**

The component also exposes a max-angular-velocity path (`bEnableMaxAngularVelocity`, `MaxAngularVelocityDegPerS`); it is disabled on every shipped aircraft (section 1.3), so nothing in the shipped model writes angular velocity directly from an assist.

### 2.4 Ordering: what is settled and what is not

Settled: per assist, `IsEnabled` gates, `GetInfluence` weights, body `Update` produces the value, and the value is blended into the control's processed value in `Mixed` mode. Input damping is **not** a stage around this pass — "Dampen pressed/released inputs" entries are assists in the same per-control list, so their stored index is their order. **Observed + data.**

Not settled: the order of control-force application versus drag inside the per-frame update, and the exact `Mixed` blend formula. The component's per-frame function was not isolated: `UBHRotaryMovementComponent` derives from `UMVehicleMovementComponent` (`UPawnMovementComponent`), most candidate overrides turned out to be replication and runtime-config serialisers, and the drag asset (`BHAirVehicleDragDataAsset`, component pointer at `0x4E8`) is a separate data path. **Open** — see section 5.

## 3. Condition runtime semantics

### 3.1 `StabilizedAfterInputReleased` — state machine, not a dwell timer

`UBHStabilizedAfterInputReleasedControlAssistCondition` is `0x88` bytes; the runtime state hides in the dump's `Pad_7C[0xC]`:

| Offset | Field |
| --- | --- |
| `0x68` | `StabilityControlValueType` |
| `0x6C` | `StabilityControlValueComponent` |
| `0x70` | `StabilityThreshold` |
| `0x74` | `TimeThresholdS` |
| `0x78` | `TimeoutS` |
| `0x7C` | latch (runtime byte) |
| `0x80` | stable-dwell accumulator (runtime float) |
| `0x84` | released-time accumulator (runtime float) |

`IsEnabled(this, ctx, evalCtx, …, DeltaTime)` is `0x145368D30` plus its shared tail `0x145368DC5`:

```
if (StabilityControlValueType == Unknown) return false;

if (abs(evalCtx->rawInput /* +0x28 */) >= 1e-4) {   // stick held; hard-coded epsilon
    latch = 1; releasedTimer = 0;                   // arm
    return false;
}
if (latch == 0) return false;                       // released but never armed

releasedTimer += DeltaTime;
if (TimeoutS > 0 && releasedTimer > TimeoutS) {     // optional absolute window
    latch = 0; return false;
}

metric = SelectControlValue(evalCtx, type /*0x68*/, component /*0x6C*/);
if (abs(metric) >= StabilityThreshold) {            // still moving
    stableTimer = 0; latch = 1;
    return true;
}
stableTimer += DeltaTime;
if (stableTimer < TimeThresholdS) {                 // stable, not long enough yet
    latch = 1; return true;
}
latch = 0; return false;                            // stable long enough -> assist off
```

Interpretation:

- `TimeThresholdS` is **not** a minimum dwell before the assist activates. It is how long the measured value must stay inside `StabilityThreshold` before the assist **switches off**. The assist is active from stick release (after arming) until the airframe has been stable for `TimeThresholdS`.
- `TimeoutS` is an upper bound on how long the assist may remain active after release, independent of stability. When it is zero or absent the bound is skipped; the shipped collective instances omit it, so they are bounded only by the stability dwell.
- "Input released" is `|raw input| < 1e-4`, hard-coded. This is much tighter than the asset-side `InputState` condition (thresholds such as 0.01), and both must pass for the assist to run.
- `StabilityThreshold` is compared against the value selected by `StabilityControlValueType`/`Component` — world vertical speed for the collective hover assists, a local angular-velocity component for pitch/roll/yaw.
- Holding the stick rearms the latch and resets both accumulators; the state is per condition instance and lives across frames.

**Observed.**

### 3.2 `WasOnGroundAtStart` — a latched take-off state

`UBHWasOnGroundAtStartRotaryMovementControlAssistCondition` has **zero** own fields (`0x68`, same as its parent). Its `IsEnabled` (`0x145368E30`) is:

```
if (Cast<BHRotaryMovementComponent>(ctx)) {              // StaticClass 0x1453482B0
    return a6 || component->vfunc_0x738();               // slot 231
}
if (Cast<BHAirplaneMovementComponent>(ctx)) {            // StaticClass 0x145314710
    return a6 || airplane_was_on_ground_at_start(ctx);   // 0x145331D80
}
return false;
```

- The cast targets are certain: `0x1453482B0` is the `BHRotaryMovementComponent::StaticClass` registration (`/Script/Mechanized`, class size 1568) and `0x145314710` is `BHAirplaneMovementComponent::StaticClass` (size 1648).
- The rotary path asks the movement component's virtual slot 231 (`+0x738`) for a latched state.
- The airplane helper `0x145331D80` keeps a latch byte at `+0x654` and a cached altitude at `+0x658`; it clears the latch when horizontal speed passes a threshold scaled by 100 or when the aircraft has climbed more than 0.1 m, and otherwise returns the latch.

So the condition is a latched "the aircraft has not taken off since spawn" state, not a ground trace, and it has no dwell or threshold of its own. **Observed.**

Crucially, its only consumer in shipped data — `CollectiveControl_3` assist `Reset collective on ground when engaged` (`EASE_IN_EASE_OUT`, `InterpTimeS` 2.5) — has `bEnabled = false` in **all three** assets. The condition never runs on the shipped helicopters. The *active* on-ground gate is a different condition, `IsOnGround`, used by "Set to -1 on ground" (enabled on all three). **Data.** This is the concrete case where a stored flag does not describe the helicopter's behaviour.

## 4. The MH-6's ~1.4 s press-to-lift-off

**Identity:** MH-6 = ROT_03. The vehicle table row `Vehicle.Variant.Air.Rotary.Littlebird.Default` in `DT_EntityData_UI_Vehicles_ROT_03.json` carries `FriendlyName "MH-6"`, and the ROT_03 damage row is `Meta.Damage.Vehicle.Air.Rotary.LittleBird`.

**Not the cause:** the `WasOnGroundAtStart` assist is disabled (section 3.2), and the condition itself is a latch, not a timer.

**What is enabled on the ROT_03 collective:**

| # | Assist | Enabled | Condition | Body |
| --- | --- | --- | --- | --- |
| 3 | Dampen pressed inputs - up | yes | `Collective == 1.0` (full up); influence In 1.0 s/exp 2, Out 1.5 s/exp 1.5 | Damping `EASE_IN_EASE_OUT`, `InterpTimeS 1.5`, exp 1.25 |
| 4 | Dampen pressed inputs - down | yes | `Collective == −1.0` | Damping `EASE_IN_EASE_OUT`, 1.5 s, 1.25 |
| 5 | Set to −1 on ground | yes | `Collective Equal` (threshold 0) **and** `IsOnGround` | `SetToValue −1.0` |
| 6 | Stabilize after input released | yes | Stabilized `WorldVelocity_KmPerH/Z < 0.00036`, In 1.5 s/exp 1.5 | PID `P 0.02`, `D 0.02` |
| 7 | Hover assist | yes | Collective released, has pilot | PID `P = D = 0.555556` |
| 8 | Dampen released inputs | yes | Collective released | Damping `EASE_IN_EASE_OUT`, 1.5 s/exp 1.5 |

Mechanism at the level the code supports:

1. On the ground with the stick neutral, assist #5 is authored to force the collective to −1 (full down). Whether it outranks the later "Dampen released inputs" (#8, released → target 0) in the `Mixed` blend is inside the undecompiled frame function; the authored design starts lift-off from a pinned-down collective either way.
2. Pulling full collective fails #5's `Collective Equal` test immediately, so the pin releases and #3 engages (it matches only at full up).
3. #3 ramps the collective from the current value toward full up with `EASE_IN_EASE_OUT`, `InterpTimeS = 1.5` s, exp 1.25. The damping `Update` integrates real `DeltaTime`, so this is a genuine 1.5 s ease-in-out ramp.
4. Lift crosses weight when the ramp passes the neutral-collective point. 1.4 s is ≈93 % of the 1.5 s ramp, and the ease-in makes the early part slow.
5. ROT_04's equivalent (same list position) is `InterpTimeS = 1.0` and triggers on any upward input (`GreaterThan 0`), which matches the symptom being MH-6-specific. ROT_02 keeps 1.5 s but is a much heavier airframe.

**Ruled out:** engine spool — `DA_ROT_03_Engine` stores only `EngineRPMDecreaseRatePerSecond = 850`, no spool-up time; `SleepWaitingTime` = 3 s, not 1.4 s; ground effect (5 m, 20 %) *adds* lift near the ground and would shorten, not lengthen, lift-off; the auto-hover ramps also use 1.5 s but are post-release stabilisers, not a ground gate.

**Confidence:** high that the 1.5 s collective-up damping ramp is the dominant authored delay and that the disabled `WasOnGroundAtStart` is not involved; the exact 1.4 s figure remains an inference until the frame function is decompiled and the ramp is simulated with the real neutral-collective value.

## 5. Still Not Pulled / Limitations

- **Per-frame order of control forces versus drag is not decoded.** The component's frame function was not isolated, and the `Mixed` blend formula is therefore unproven. This is the next pass; it also affects the exact lift-off timing in section 4.
- **Rotary component virtual slot 231 (`+0x738`)**, used by `WasOnGroundAtStart`, has not been decompiled; whether it is a stored latch or recomputes a condition each call is inferred from the name and the airplane helper's shape, not read.
- **No gameplay measurement was used.** The 1.4 s observation is the reporter's; nothing here was run, and the timing derivation is a consistency argument.
- **The restored image is a third-party reconstruction** (see source limits above). Function RVAs are given so the reading can be repeated against a matching image, but no runnability or whole-binary provenance is claimed.
- The assist count in section 2.2 includes nested `MultiAssistBody` children as separate assist records; the generated assist page prints them per control and should be used for per-control navigation.

## 6. Where the numbers come from

- Flight assets: [`DA_ROT_02_FlightCharacteristics`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/Data/DA_ROT_02_FlightCharacteristics.json), [`DA_ROT_03_FlightCharacteristicsDataAsset2000KGLight`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/Data/DA_ROT_03_FlightCharacteristicsDataAsset2000KGLight.json), [`DA_ROT_04_FlightCharacteristicsDataAsset`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/Data/DA_ROT_04_FlightCharacteristicsDataAsset.json).
- Engine assets: `DA_ROT_02_Engine.json`, `DA_ROT_03_Engine.json`, `DA_ROT_04_Engine.json` beside them.
- Class layout: [`sdk/raw/Mechanized_classes.hpp`](../../sdk/raw/Mechanized_classes.hpp) (flight data asset at `BHRotaryFlightDataAsset`, movement component at `BHRotaryMovementComponent`, assist classes `BHRotaryMovementControlAssist*`) and [`sdk/raw/Mechanized_structs.hpp`](../../sdk/raw/Mechanized_structs.hpp) (`FRotorSettings`, `FRotationalControlForce`, `FLinearControlForce`).
- Native RVAs used: constructor `0x145384750`; condition interface `0x145368B30` / `0x145362F10`; body interface `0x14537A910`; PID update `0x14537A410`; damping update `0x14537A380`; stabilized gate `0x145368D30` + `0x145368DC5`; was-on-ground gate `0x145368E30`; rotary StaticClass `0x1453482B0`; airplane StaticClass `0x145314710`; airplane latch helper `0x145331D80`.
