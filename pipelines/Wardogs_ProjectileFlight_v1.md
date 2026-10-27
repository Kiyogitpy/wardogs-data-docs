---
title: "Projectile Flight: Thrust, Drag and Gravity"
redirect_from: ["/Wardogs_ProjectileFlight_v1.html", "/Wardogs_ProjectileFlight_v1"]
parent: "Damage & Combat Systems"
description: "How a projectile moves from muzzle to hit: launch velocity, gravity, drag, thrust and wind"
---

# Wardogs — Projectile flight: thrust, drag and gravity

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

How a projectile moves between the muzzle and the hit: launch velocity, the
per-step force model (gravity, drag, thrust, wind), the integrator, and the
conditions that end the flight. It answers one question first raised by an
outside review: `DA_155mm_Standard_ProjectileData` sets
`bActorHandlesProjectileMovement: true`, so does an artillery shell fly by
different rules, and is drag modelled at all?

**Short answer.** Drag is modelled, in native code, and the artillery shell
uses the same force model as every other projectile. The flag does not switch
to a different physics; it switches *who runs the step*. For a normal
projectile the projectile subsystem integrates the step itself
(§3). For an actor-driven projectile the subsystem skips the integration and the
actor's mover mode (`UWDProjectileMove`, or `UWDArtilleryProjectileMove`)
asks the **same native helpers** for gravity, drag, wind and thrust each tick
(§7). What stays open is which mover mode the Blueprint actor
`BP_155mm_Standard` selects and whether its Blueprint changes anything (§11);
that needs the Blueprint export, not more native analysis.

Build: `++Wardogs+Live-CL-516586` · Engine: UE 5.7 · Native addresses are file
RVAs (image base `0x140000000`).

**Evidence level: static-analysis image; virtualized dispatch not removed.**
Everything below was read with capstone and pefile from the flat executables.
The restored image
`WardogsClient-Win64-Shipping.restored.exe` (SHA-256 `a5c3db10…2b4f0cc37`) is
the reading copy. The static-analysis image was byte-compared against it for
every function cited here (§10): all are byte-identical except the weather
wind getter `0x6F78270`, which begins with a protection-layer dispatch stub in
the analysis image and is read from the restored image, as
[IDA claim exposure](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/IDA_CLAIM_EXPOSURE.md) prescribes. The
decompilation corpus was used read-only to locate functions and field names;
the constants and offsets were re-read from the bytes with
[`_tools/projectile_flight_check.py`](../_tools/projectile_flight_check.py).
No game was run and no process was observed. Nothing here was fitted to
calculator or in-game measurements.

| Label | Meaning |
|---|---|
| **Native** | Read from instructions or `.rdata` constants in the executable; RVA cited |
| **Data** | Read from the cooked export under `data/` |
| **SDK** | Class or struct layout from `sdk/raw` |
| **Derived** | Arithmetic on Native and Data facts only |
| **Inferred** | Role deduced from how the code uses a field; not named anywhere |

---

## 1. Summary of the model

Per fixed step of `dt` seconds, for a projectile with stats `S`
(`FWDProjectileStats`), velocity `v` (cm/s) and position `x` (cm):

```text
a  = g + a_thrust + a_drag + a_wind                      (cm/s^2, vector)
v1 = v + a * dt              then, if S.MaxSpeed > 0:  |v1| <= S.MaxSpeed
dx = (v + v1) / 2 * dt                                   (trapezoid)
sweep a trace x -> x + dx; on a hit the step stops at the hit fraction f
```

| Term | Formula | Section |
|---|---|---|
| Gravity `g` | `(0, 0, G)` when `S.bAffectedByGravity` (default true), `G` = `UPhysicsSettings` default object `+0x38` (project gravity, cm/s²); else `0`. Scaled by a fuel curve while thrusting | §4 |
| Drag `a_drag` | `-(100/m) · ½ρ · Cd · (π/4)(D/100)² · (|v|/100)² · v̂` with `ρ = 1.2`, `Cd = DragModel.Value × Curve(|v|/100)`, `D` cm, `m` kg | §5 |
| Thrust `a_thrust` | `ThrustSpeed · v̂` (cm/s², despite the name) while fuel remains and the start delay has passed | §6 |
| Wind `a_wind` | `0.75 · Wind · clamp((T² − X²)/X², 0, 1)`, `T` = absolute path travelled | §6.4 |
| Step | `dt = floor(1000 / Rate) · 0.001` s, `Rate` = `SimulationFrameRate` = 30 (`DefaultGame.ini`), so 33 ms | §3 |

Launch speed is the **weapon's** `InitialBulletSpeed` (cm/s), not the
projectile's `TypicalSpeed` (§2). `ThrustSpeed` is a cm/s² acceleration, not a
cruise speed (§6). All lengths are centimetres, all times seconds, the drag
level is metres per second and mass is kilograms (§9).

---

## 2. Launch velocity

**Native.** The fire path `0x6F1DDC0` builds the spawn request. Its velocity
is a unit direction times `unk_146BBD500(weaponStats)`, and that getter is
`movss xmm0,[rcx+0xDA0]; ret` (`0x6BBD500`): **`FWDWeaponStats.InitialBulletSpeed`**
(SDK `+0xDA0`). The same request stores the projectile's `TypicalSpeed`
(`FWDProjectileStats +0x1FC`, copied at `0x6F1DFB0`) and
`EffectiveRange × 100` (`0x6BBD420`: `[stats+0xDA4] × 100.0`, so
`EffectiveRange` is metres and the request holds centimetres).

`TypicalSpeed` is **not** read by the integrator (`0x6F3C060`) or by the mover
mode's move generator (`0x76D8A00`). Its readers found are the suppression
scaler (`0x6F3B0E0`, which scales suppression by `speed / TypicalSpeed` when
the round is slower than `TypicalSpeed`; read at `0x6F3B9BE`) and the ammo
modifier multiplier (`0x6BBAB70`, which multiplies `+0x1FC` by a modifier
value). The constructor default is 60000 cm/s (`0x699DEE0`).

**Ammo modifier applier (round 39, static).** `0x6BBAB70(stats, out, modifierAsset)` multiplies fields of a per-ammo copy of the projectile stats by the
values in `AttributeModificationMultipliers`; each key is matched by a gameplay-tag global. The tag-to-field map read from the tag registration
functions: BaseDamage `+0x30`, ExplosiveRadius `+0x34`, MinimumExplosiveDamage `+0x38`, EffectiveExplosiveRadius `+0x3C`, ExplosiveDamageFallOff `+0x40`,
Length `+0x68`, Diameter `+0x6C`, Mass `+0x70`, DragModelValue `+0x78`, **TypicalSpeed `+0x1FC`**, **EffectiveRangeMultiplier `+0x200`**,
**PenetrationEffectivenessMultiplier `+0x208`**, ThrustSpeed `+0x2B0`, Suppression.BaseValue `+0xB8`, Suppression.DistanceFalloff.Min and Max
`+0xBC` and `+0xC0`, Suppression.FriendlySafeRadius `+0x150`, Suppression.FriendlyMultiplier `+0x154`, TravelDistanceWhizBy `+0x2D4`,
DistanceToPlayerWhizBy `+0x2D8`, **TracerChance `+0x1F4`** (assigned, not multiplied) and **PenetrationExitSpeedMultiplier `+0x20C`**. The five
`DA_AmmoModifier_*` assets set only EffectiveRangeMultiplier, PenetrationEffectivenessMultiplier, PenetrationExitSpeedMultiplier and TracerChance, so
**no ammo type changes `TypicalSpeed`**, and `InitialBulletSpeed` is a weapon field the applier never touches. The weapon-component spawn routine
`0x6B747F0` builds the request range as `EffectiveRange x 100` (`0x6BBD420`) times `GetProjectileStats(projectile, ammoTag)+0x200`, so the armor-piercing
1.2 and hollow-point 0.8 multiply the range value that the spawn request carries (the value section 6.4 reads as `X`; inferred). The infantry fire
path `0x6F1DDC0` calls `GetProjectileStats` with the global at `0xD2692F8`, which is never written and is used as the empty gameplay tag elsewhere,
and `0x6BBA900` returns the base stats when the tag is 0. Constructor defaults of the projectile stats (`0x699DEE0`): `MaxProjectileLifetime` (`+0x188`)
10.0 s (`0x41200000`, store at `0x699E09B`), `TypicalSpeed` 60000, EffectiveRangeMultiplier 1.0. The bullet projectile assets do not set
`MaxProjectileLifetime`, so bullets live 10 s.

| Quantity | Value | Source |
|---|---:|---|
| 155 mm artillery `InitialBulletSpeed` | 30000 cm/s (300 m/s) | **Data**, `DA_TNK_01_Artillery_Weapon_Stats` |
| `ArtilleryBarrelTest` `InitialBulletSpeed` | 46400 cm/s | **Data**, `DA_ArtilleryBarrelTest_Stats` |
| 155 mm `TypicalSpeed` | 15000 cm/s (150 m/s) | **Data**, `DA_155mm_Standard_ProjectileData` |
| 155 mm `ThrustSpeed` | 22000 (unused, see §6.1) | **Data** |

So the artillery shell leaves the barrel at 300 m/s while its own
`TypicalSpeed` says 150 m/s. The two are different fields with different jobs.
Whether `InitialBulletSpeedModifier` (`UWDWeaponComponent +0x114`, SDK) is
folded into the weapon stats before `0x6F1DDC0` is open (§11).

---

## 3. Which code runs the step

**Native.** `UWDProjectileSubsystem` is a tickable world subsystem (vtable
`0xB440498`, constructor `0x6F2AAA0`; its tickable sub-object vtable
`0xB440798`, slot 0 = `Tick` = `0x6F3BC70`). Each live projectile is one
800-byte (`0x320`) `FWDProjectileInstance` (SDK). Instance fields used here,
relative to the instance:

| Offset | Field | Note |
|---|---|---|
| `+0x08` | `Location` (3 doubles) | `FWDProjectileMovementData.Location` |
| `+0x20` | `Velocity` (3 doubles) | |
| `+0x38` | `CurrentFuel` (float) | initialised from `S.TotalFuel` (`0x6F30E50`: `inst+56 = stats+540`) |
| `+0x40` | `TotalAbsoluteMove` (3 doubles) | per-axis sum of `|dx|` |
| `+0x58` | `TotalAbsoluteWindDrift` (3 doubles) | |
| `+0xC4` | float `X` (wind threshold, §6.4) | initialised from the spawn request (`0x6F30E50`, request `+180`) |
| `+0xC8` | state byte | 1, 2 = flying (simulated); 3 = post-impact countdown (float at `+0xDC`); 4 = not simulated (meaning not traced) |
| `+0xD8` | max lifetime (float) | `inst+216 = stats+392` = `MaxProjectileLifetime` (`0x6F30E50`) |
| `+0x128` | **actor handles movement** | `inst+296 = stats+496` = `bActorHandlesProjectileMovement` (store at `0x6F3A535–0x6F3A53C`, in `0x6F39940`) |
| `+0x290` | `ElapsedTime` (double) | |
| `+0x2E0` | step accumulator (double, ms) | |

`Tick` (`0x6F3BC70`; the function with the fixed-step accumulator, slot 0 of the tickable sub-object vtable):

```text
step_ms = floor(1000 / Rate)                 Rate = int at tickable +0x40C (subsystem +0x444)
for each instance:
    acc_ms += DeltaTime * 1000
    if acc_ms >= step_ms:   acc_ms -= step_ms
        dt = step_ms * 0.001                 (xmm6 passed in xmm2 to 0x6F3CB80)
        if inst.+0x128 (actor handles movement):  no native integration, instance kept alive
        else:  0x6F3CB80(inst, dt) integrates;  a false return removes the instance
```

The actor-driven exemption is explicit in three places: the spawn code copies
the flag to `inst+0x128` (`0x6F39940`), `Tick` branches on it at `0x6F3BE31`,
and the step driver `0x6F3D130` returns "alive" for it before it would call
`0x6F3CB80` (`0x6F3D164: cmp byte [rbx+0x128],0`). `0x6F3CB80` itself returns 0
immediately when `inst+0x128` is set.

**`Rate` is `SimulationFrameRate`, and it is 30.** (Round 23.) The int at tickable `+0x40C`
(subsystem `+0x444`) is `FWDProjectileSystemSettings.SimulationFrameRate` (SDK `+0x1A4`), the last
field of the `ProjectileSystemSettings` struct the subsystem holds at `+0x2A0`:

| Step | Where | Value |
|---|---|---|
| Class default | the struct constructor `0x6F2A600` stores `0x1E` at struct `+0x1A4` (`0x6F2A792`); the subsystem constructor `0x6F2AAA0` calls it on `+0x2A0` (`0x6F2ACE3`) | 30 |
| Config | `Wardogs/Config/DefaultGame.ini` line 303, `[/Script/WDGame.WDGameSettings]`, `ProjectileSystemSettings=(…,MaxConsecutiveFullRefundedSubsteps=10,SimulationFrameRate=30)` (SHA-256 `56fda182…33f1bd`, the same file as [round 8 config](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round8-config.md)) | 30 |
| Load | subsystem `Initialize` (`0x6F37F12`–`0x6F37F25`) resolves the `WDGameSettings` object (`0x6C03540`) and copies its `+0x458` struct into `+0x2A0` with the copy-assign `0x6F2C180`, which copies `+0x1A4` at `0x6F2C427`–`0x6F2C432` | 30 |

No other write to subsystem `+0x444` (or to the tickable `+0x40C`) exists in `0x6F20000`–`0x6F50000`; the
settings object's own constructor initialises the same struct through the same `0x6F2A600`
(`0x6C02F3A`). The field is read at four sites, each computing `floor(1000/Rate)` the same way
(`cvtdq2pd`, `divsd` by 1000.0, `roundpd` mode 3 = truncate; `Rate = 0` gives a step of 0): `Tick`
(`0x6F3BCB7`), and `0x6F2C72C`, `0x6F3D798`, and `0x6F34343`, which stores the step (`entry+0x100`) and the
instance accumulator (`entry+0x108`) in the per-handle tracer-presentation entry (map at `+0x140`,
stride `0x168`). So:

- **Fixed, not variable:** `dt = floor(1000/30) = 33` ms = `0.033` s, `Tick` accumulates real frame time
  and runs at most one step per tick (`acc ≥ 33 → acc −= 33`; an accumulator within an epsilon of zero is
  snapped to 0). A frame longer than 33 ms leaves a backlog that drains one step per later tick.
- **Not replicated as a value:** nothing in the traced readers sends it. Each machine reads its own
  `DefaultGame.ini` (the same shipped file), so server and client agree by configuration.
- **Only for native-stepped projectiles.** Actor-driven projectiles (`bActorHandlesProjectileMovement`,
  §7: the 155 mm shells, 120/125 mm, 122 mm, 93 mm and others) use the mover time step instead.
  `DefaultNetworkPrediction.ini` sets `PreferredTickingPolicy=Fixed` and `FixedTickFrameRate=30`, i.e.
  `1/30` s = 33.3 ms if the projectile mover ticks on the fixed policy (not confirmed for
  `BP_155mm_Standard`). Against `_tools/shell_sim.py` the difference between 33 and 33.3 ms is 0.01 m.
- **Build check:** the settings constructor, the copy, `Initialize` and `Tick` are byte-identical in the
  analysis image and the older reference image; the readers above were read in the reference image.

`0x6F3CB80` loops the substep `0x6F3C060` until the step's time is consumed
(each call returns the unused fraction `(1 − f)·dt` after a hit) and then runs
the hit and replication bookkeeping.

---

## 4. Gravity

**Native**, in the integrator (`0x6F3C060`, flag read at `0x6F3C16B`) and in the
helper `0x6F2E4B0` that the mover mode also calls:

```text
if S.bAffectedByGravity (+0x2E0):   g = (0, 0, G)   with G = float [ [Class(PhysicsSettings)+0x110] + 0x38 ]
else:                               g = (0, 0, 0)
```

`0x42AA2C0` resolves the class `/Script/Engine.PhysicsSettings` (the strings
`PhysicsSettings` and `/Script/Engine` are loaded at `0x42AA2F4–0x42AA315`);
`+0x110` is `UClass::ClassDefaultObject` and `+0x38` is the first property of
`UPhysicsSettings`, `DefaultGravityZ`. So the projectile gravity is the
project's physics gravity, in cm/s². The x and y components are the zero
vector (`0xCCA3468`, `0xCCA3478`). `bAffectedByGravity` defaults to **true**
(`0x699DEE0`, store at `+0x2E0`), and the 155 mm assets do not override it.

**Value.** `DefaultGravityZ` is −980.0 cm/s², read from
`[/Script/Engine.PhysicsSettings]` in the engine base config packed in the game
paks; the game's own `DefaultEngine.ini` sets no gravity key and the
WorldSettings of the nine map files set no `bGlobalGravitySet` or
`GlobalGravityZ` (see [Artillery shell flight data](../game-features/Wardogs_ArtilleryShellFlight_v1.md)).
Not checked: gravity-override volumes in the world-partition cells of the four
large maps.

**Fuel curve.** While thrust is active (§6.1) and
`S.FuelGravityAffect` (`+0x228`, a `FRuntimeFloatCurve`) has keys, gravity is
multiplied by `Curve(CurrentFuel / TotalFuel)` (`0x6F2E5A0–0x6F2E5C9`:
`xmm1 = fuel / [stats+0x21C]`, then the curve evaluator `0x3E07720`). With no
thrust the multiplier is 1.

---

## 5. Drag

**Native**, `0x6F2E240` (called as `(subsystem, out, stats, &velocity)`):

```text
Cd   = DragModel.GetValueAtLevel( float(|v| * 0.01) )          // 0x6BBA8A0 -> 0x48AA830
k    = D^2 * rho * Cd * (pi/8 * 1e-4)                          // D = stats+0x6C, rho = 1.2
F    = k * (|v|^2 * 1e-4)                                      // newtons, = 0.5 rho Cd (pi/4)(D/100)^2 (|v|/100)^2
m    = max(stats+0x70, 0.001)                                  // kg
a_drag = -100 * F / m * v_hat                                  // cm/s^2, opposite to v
v_hat = v / |v|   (zero vector if |v|^2 <= 1e-8)
```

Constants (each re-read from `.rdata` by the check tool):

| Constant | Value | RVA |
|---|---:|---|
| `π/8 × 10⁻⁴` | `3.92699076e-05` (float) | `0xB440AF0` |
| `10⁻⁴` | `9.99999955e-05` (double) | `0x9C083B0` |
| `−100` | double | `0xA4E07F8` |
| air density `ρ` | `1.2` (float), kg/m³ | `0xA3BEF68`; the weather subsystem's getter `0x6F77F90` returns `1.2` from `0xCED2C4C` |
| level scale | `0.01` (double) | `0x9AD4640` |
| minimum mass | `0.001` (float) | `0x9AAFD68` |

Reading the code: `ρ` starts as the default float `1.2`; if the world has a
`WDWeatherSubsystem` (class name string at `0x6F777D6`, looked up through
`0x6F29130`, world subsystem map at `+0x9D0`) it is replaced by the getter's
result, which is the constant `1.2`. So `ρ = 1.2` in every case in this build.

**The drag coefficient lookup.** `0x6BBA8A0` takes `stats+0x68` (the
`FWDProjectileDimensions`), adds `0x10` to reach `DragModel`
(`FBHScalableFloat`, stats `+0x78`) and tail-calls the scalable-float
evaluator `0x48AA830`, with the level `float(|v| × 0.01)`: **speed in metres
per second**. The evaluator (`0x48A8480`) returns `Value × RichCurve.Eval(level)`
when the curve-table row resolves, else `Value`. So:

```text
Cd(v) = DragModel.Value * Curve[row](|v| in m/s)
```

The row is `DragModel.Curve.RowName` in
`CT_Projectile_DragCoefficients`,
whose `Time` axis is therefore **m/s** (the G7 and G1 rows rise sharply at 274–366
on that axis, which is where the speed of sound sits). The 155 mm assets use
row `GC (Cylinder)`: 0.71 at 0, 0.66 at 150, 1.10 at 300, 1.60 at 600.
`DragModel.Value` defaults to **1.0** when the cooked asset omits it (the
`FWDProjectileStats` constructor `0x699DEE0` stores `0x3F800000` at `+0x78`),
so rows without a `Value` (for example `.50 Cal`) use the bare curve.

**Diameter and mass.** `D = stats+0x6C` is in **centimetres** (the area is
converted with the `10⁻⁴` factor; `.50 Cal` carries 1.2954) and `m = stats+0x70`
in **kilograms**. Constructor defaults: `Length 1.5`, `Diameter 0.9`,
`Mass ≈ 0.00746`.

**Mach and altitude.** There is no altitude or temperature term; `ρ` is a
constant, and the only speed dependence is the `Cd` curve.

---

## 6. Thrust, fuel and wind

### 6.1 Thrust

**Native**, `0x6F30280` (also called from the mover move generator). Active when

```text
S.bShouldThrust (+0x219)  AND  CurrentFuel > 0
AND ( |S.ThrustStartDelay (+0x2B4)| <= 1e-8   OR   S.ThrustStartDelay < Elapsed )
```

then, with `bHasThrustInstability` (`+0x2B8`, read as `+696` at `0x6F30280`) false:

```text
a_thrust = ThrustSpeed (+0x2B0) * v_hat           // cm/s^2, along the current velocity
```

and zero otherwise. `ThrustSpeed` is therefore an **acceleration in cm/s²**
along the velocity, not a speed. With `bHasThrustInstability` true the function
adds a lateral term proportional to `|v|`, to `ThrustInstabilityYawScale`
(`+0x2BC`) and to `ThrustInstabilityPitchScale` (`+0x2C4`), built in the basis
of the velocity; the two scalar factors come from two runtime functions
(`0x1498F816A`, `0x1498F815E`) that were not resolved. No 155 mm asset sets
`bHasThrustInstability`.

**Constructor defaults** (`0x699DEE0`): `bShouldThrust` **false**, `TotalFuel`
1000, `FuelBurnRate` 10, `ThrustSpeed` 0, `ThrustStartDelay` 0, `MaxSpeed` 0.
The cooked 155 mm assets set `ThrustSpeed: 22000` but never set
`bShouldThrust`, so **the 155 mm shell does not thrust**; the 22000 is inert
(the same holds for `84mm`, `120x570mm`, `122mm` and others that carry
`ThrustSpeed` without `bShouldThrust`). Assets that do thrust:

| Asset | `bShouldThrust` | `ThrustSpeed` | `TotalFuel` | `FuelBurnRate` | `ThrustStartDelay` | `MaxSpeed` | Burn time `TotalFuel/FuelBurnRate` |
|---|---|---:|---:|---:|---:|---:|---:|
| `DA_72mm` | true | 17500 | 180 | 30 | 0.35 s | 20000 | 6.0 s |
| `DA_93mm` | true | 17000 | 100 | 40 | 0.04 s | 22000 | 2.5 s |
| `DA_122_mm_HAVOC` | true | 20000 | 1000 (default) | 10 (default) | 0 | 0 | 100 s (defaults) |

All from **Data** plus the defaults above. `DA_DebugHomingRocketData` sets
20 s, fuel 100, burn rate 1.0 (see [Items §7c](../content/Wardogs_Items_v2.md)).

### 6.2 Fuel burn

**Native** (`0x6F3C060`, `FuelBurnRate` read at `0x6F3C842`): after a step, if the thrust vector
is non-zero,

```text
CurrentFuel -= FuelBurnRate (+0x220) * dt * f          // f = step fraction completed
```

so fuel is consumed per second of powered flight at `FuelBurnRate` units per
second, and thrust ends when `CurrentFuel <= 0`.

### 6.3 Speed cap

`S.MaxSpeed` (`+0x2CC`): after `v1 = v + a·dt`, if `MaxSpeed > 0` the vector is
clamped to that length (`MaxSpeed` read at `0x6F3C449`, then `0x165ED30`,
`FVector::GetClampedToMaxSize`, tolerance `1e-4`). Default 0 means no cap. Cooked values: `72mm` 20000 cm/s,
`93mm` 22000 cm/s.

### 6.4 Wind

**Native.** `0x6F30680` (mover path) and the matching inline code in
`0x6F3C060`:

```text
t      = clamp( (T^2 - X^2) / (2X^2 - X^2), 0, 1 )     // X = inst+0xC4, T^2 = |TotalAbsoluteMove|^2 (inst+0x40..)
a_wind = Wind * t * 0.75                               // 0.75 = float at 0xCED1BA8
```

`Wind` is a 3-vector held by `WDWeatherSubsystem` (`0x6F78270` returns the
override vector at `+0xB8` if its flag at `+0xD0` is set, else the current
vector at `+0xA0`). `TotalAbsoluteWindDrift` accumulates `a_wind·dt`. The wind
therefore fades in with the distance already travelled and is at full
strength once `T² ≥ 2X²`. **Inferred:** `X` is `EffectiveRange × 100` cm,
because the fire path stores that value in the spawn request next to the
velocity (§2); not confirmed. For the artillery weapon that would put the
onset at 10 km.

---

## 7. The actor-driven path (`bActorHandlesProjectileMovement`)

**Native.** `AWDProjectile` (SDK, size `0x3B0`) owns a `UBHMoverComponent`
(`+0x2D8`). Its movement modes derive from `UWDProjectileMove`
(vtable `0xB676380`); the artillery shell's mode would be
`UWDArtilleryProjectileMove` (vtable `0xB6720E8`, SDK fields `InputMultiplier`
`+0x90` and `bIgnoreVerticalInput` `+0x94`), and `UWDGlideProjectileMove`
(vtable `0xB673188`) derives from that. Their overridden slots:

| Slot | `UWDProjectileMove` | Role |
|---|---|---|
| 98 | `0x76D8A00` | **GenerateMove**: the force model |
| 99 | `0x76D9110` | simulation tick: applies the move and traces |
| 94 | `0x76D7B90` | shared with Artillery and Glide |

`GenerateMove` (`0x76D8A00`) looks up the same native `FWDProjectileInstance`
through the subsystem (`0x6F34FE0`, keyed by the projectile handle read from
the owning actor), reads its stats with `0x6BBA900`, and then calls the **same
helpers** as §3 in this order:

```text
a_grav  = 0x6F2E4B0(subsystem, inst, stats)                        // gravity (+ fuel curve)
a_drag  = 0x6F2E240(subsystem, stats, &syncState.Velocity)         // drag, §5
a_wind  = 0x6F30680(subsystem, stats, &Location, X, |TotalAbsoluteMove|^2)   // wind, §6.4
a      += 0x6F30280(subsystem, inst, stats, &Velocity, ...)        // thrust, only if a sync state exists
v1      = v + (a_grav + a_drag + a_wind [+ a_thrust]) * dt          // dt = mover time step
```

then writes the proposed linear velocity into the `FProposedMove` (flag byte
`0x80` at `+1`). When `0x6F307C0` returns true, `0x6F2E620` (4370 bytes, probably the
guided-flight steering driven by `FWDProjectileGuidance`, stats `+0x158`; not
traced) supplies the base velocity instead of the current one. The tick `0x76D9110`
integrates exactly as §1: displacement
`(v_new − v_old)·dt/2 + v_old·dt`, a sweep trace named `Trace_Mover_Projectile`
(`0x143CB56B0`), and impact handling through the native instance
(`0x6F36F40`).

`UWDArtilleryProjectileMove`'s move generator (`0x76CC730`) calls the base
`GenerateMove`, then reads the `WDProjectileSyncState` component at `+0x80`
and passes the proposed velocity through `0x1670CB0` (build a rotation from
the state, transform the vector), writing the result back. It looks like a
steering rotation applied after the force model; `InputMultiplier` and
`bIgnoreVerticalInput` are the SDK tunables. That function was not traced
further.

**What this means for the review question.** The actor does not run
independent physics. If the Blueprint `BP_155mm_Standard` uses a
`UWDProjectileMove`-family mode, its flight is the model of §1 with the
155 mm stats. If the Blueprint replaces the mode or moves the actor in its own
event graph, that part is **Blueprint bytecode** and is documented from the
Blueprint export, not here. Native hooks the actor can call regardless:
`GetCurrentVelocity`, `GetCurrentLocation`, `GetCurrentTravelTime`,
`GetExpectedTravelTime`, `GetSpawnLocation`, `GetSpawnVelocity`,
`GetProjectileData` (SDK `AWDProjectile` functions), plus the
`WDProjectileSubsystem` queries (`IsProjectileHandlingMovementExternally`).

---

## 8. Worked values for the 155 mm shells

**Derived** from §1 and §5 with the cooked data. Gravity `G = −980 cm/s²`
(assumed, see §4). `a_drag` below is the deceleration only, at the speed shown,
with `ρ = 1.2` and the linear interpolation of the `GC (Cylinder)` row.

| Asset | `DragModel.Value` | `D` cm | `m` kg |
|---|---:|---:|---:|
| `DA_155mm_Standard` (and `_SB`, `Expensive_SB`) | 80 | 8.4 | 70 |
| `DA_155mm_Expensive` | 2.5 | 10.5 | 19 |

| Speed | `Cd` Standard | `a_drag` Standard | `Cd` Expensive | `a_drag` Expensive |
|---:|---:|---:|---:|---:|
| 50 m/s | 53.7 | 6.4 m/s² | 1.68 | 1.2 m/s² |
| 100 m/s | 51.4 | 24.4 m/s² | 1.61 | 4.4 m/s² |
| 150 m/s | 52.8 | 56.4 m/s² | 1.65 | 10.2 m/s² |
| 200 m/s | 56.2 | 106.8 m/s² | 1.76 | 19.2 m/s² |
| 300 m/s | 88.0 | 376 m/s² | 2.75 | 67.7 m/s² |

Two consequences that follow from the equations (not measurements):

- Setting `a_drag = 9.8 m/s²` (drag balancing gravity alone) gives a terminal
  speed of about **62.6 m/s** for the Standard shell and about **147.5 m/s**
  for the Expensive shell. The Expensive figure sits next to its
  `TypicalSpeed` of 150 m/s. That is an observation about the numbers, not
  evidence that `TypicalSpeed` is derived from drag.
- A shell launched at 300 m/s with `Value = 80` loses most of its speed within
  a few seconds; the Expensive shell with `Value = 2.5` keeps a long, flat
  flight. `DragModel.Value = 80` on the Standard asset (and on the `_SB`
  copies) is a very large multiplier next to the other 155 mm and 120 mm
  assets (2.5 to 11.5); whether it is intended is a data question.

These numbers hold only if the shell flies through the native force model
(§7). They say nothing about the Blueprint.

---

## 9. Units

| Quantity | Unit | Evidence |
|---|---|---|
| Position, displacement, `Diameter`, `Length` | **centimetres** | UE world units; `0xB440AF0` and `0x9C083B0` apply `10⁻⁴` to cm² |
| Velocity, `InitialBulletSpeed`, `TypicalSpeed`, `MaxSpeed` | **cm/s** | `|v| × 0.01` is passed as the drag level; the `10⁻⁴` factor converts `|v|²` to m²/s² |
| `ThrustSpeed` | **cm/s² (acceleration)**, mis-named | added to `a` and multiplied by `dt` (`0x6F3C060`) |
| Gravity | cm/s² | `UPhysicsSettings` default, UE convention |
| `Mass` | **kg** | `a = F/m` then `× 100` (m/s² to cm/s²), `0x6F2E240` |
| Air density | kg/m³ (`1.2`) | |
| Drag curve `Time` axis | **m/s** | level is `|v| × 0.01` |
| `EffectiveRange` | **metres** | `0x6BBD420` multiplies by `100.0` |
| `FuelBurnRate` | fuel units per second | `0x6F3C060` multiplies by `dt` |
| Times (`ArmingDelay`, `ThrustStartDelay`, `MaxProjectileLifetime`) | seconds | compared with `ElapsedTime` (seconds) |

Docs that said otherwise: [GameMechanics §3](../content/Wardogs_GameMechanics_v2.md)
called `Thrust` "the sustained speed"; it is an acceleration (corrected there).
[`docs/UNITS.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/UNITS.md) already had `InitialBulletSpeed` in cm/s and
projectile `Mass` in kg; its curve-axis list now includes the drag curve.

---

## 10. Arming, lifetime and detonation

- **No arming distance.** `FWDProjectileStats` (SDK) has `bHasArmingDelay`
  (`+0x180`) and `ArmingDelay` (`+0x184`), both time-based; there is no
  minimum arming distance field. Defaults: no delay.
- **Arming delay.** In the hit-event builder (`0x6F344D0`), at `0x6F346ED–0x6F34711`:
  `bHasArmingDelay` and `(ArmingDelay − 0.0001) > ElapsedTime` take the branch that attaches the
  global tag at `0xD3815F8` to the hit event (an unarmed marker; its
  consumer was not traced). 155 mm Standard has no delay; 155 mm Expensive
  has 1.3 s; 120x800 0.1 s, 84 mm 0.03 s, 72 mm 0.13 s, 93 mm 0.099 s,
  40 mm 0.07 s.
- **Lifetime.** `alive = (inst+0xD8 ≥ ElapsedTime) AND inst+0x28C == 0`
  (`0x76E07D0`). `MaxProjectileLifetime` default 10 s; 155 mm 40 s. The
  native subsystem applies it only to projectiles it integrates; for
  actor-driven projectiles the native check is skipped (`0x6F3D130`) and the
  actor's own lifetime fields apply (SDK `bHandlesOwnLifetime`,
  `ExtendedLifetime`).
- **Detonation by impact.** The sweep trace of §1 ends the step at the hit
  fraction `f`; the impact is processed by `0x6F36F40`. The hit event also
  carries `|v| × Mass` (`0x6F346D1–0x6F346E9`). Penetration and ricochet use
  `bShouldPenetrate` (default true, the 155 mm assets set false) and
  `MinImpactAngleForRicochet` (default 10°, the 155 mm assets set 91°, which
  disables ricochet).
- **Pre-simulation.** `bShouldPreSimulate` (default true; the 155 mm assets
  set false) makes the spawn code run up to three substeps at once
  (`0x6F37510`).

---

## 11. Function table

All RVAs are file RVAs. "Same" means byte-identical in the static-analysis
image; the check tool prints it with `WARDOGS_ANALYSIS_EXE` set.

| RVA | Size | Role | Analysis image |
|---|---:|---|---|
| `0x6F3BC70` | 870 | `UWDProjectileSubsystem` tickable `Tick`: fixed-step accumulator | same |
| `0x6F3CB80` | 1449 | step driver: loops the substep, bookkeeping | same |
| `0x6F3C060` | 2840 | **substep integrator**: gravity + thrust + drag + wind, clamp, trace | same |
| `0x6F2E240` | ~0x270 | **drag** acceleration | same |
| `0x6F2E4B0` | ~0x170 | gravity with the fuel-gravity curve | same |
| `0x6F30280` | 1022 | **thrust** acceleration | same |
| `0x6F30680` | ~0x13A | wind acceleration | same |
| `0x6F78270` | small | weather wind vector getter | **differs**: dispatch stub in the analysis image; read from the restored image |
| `0x6F77F90` | 9 | weather air-density getter (`1.2`) | same |
| `0x6F30E50` | 555 | instance initialisation (fuel, lifetime, `X`) | same |
| `0x6F39940` | 5116 | spawn: copies `bActorHandlesProjectileMovement` to `inst+0x128` | same |
| `0x6F3D130` | ~0x94 | per-instance step driver; actor-driven returns early | same |
| `0x6F37510` | 572 | post-spawn setup, pre-simulation | same |
| `0x76E07D0` | 36 | lifetime test | same |
| `0x6F1DDC0` | 1075 | fire path: spawn request, launch velocity | same |
| `0x6BBD500` | 8 | `InitialBulletSpeed` getter (`+0xDA0`) | same |
| `0x6BBD420` | 17 | `EffectiveRange × 100` (`+0xDA4`) | same |
| `0x6BBA900` | 618 | stats lookup with ammo modifier | same |
| `0x6BBAB70` | 1243 | ammo modifier multipliers on stats fields | same |
| `0x6BBA8A0` | 0x40 | drag-model level eval (`|v|×0.01`) | same |
| `0x48AA830`, `0x48A8480` | 0x90, 430 | `FScalableFloat::GetValueAtLevel` | same |
| `0x165ED30` | 0xE0 | `FVector::GetClampedToMaxSize` | same |
| `0x699DEE0` | 0x395 | `FWDProjectileStats` default constructor | same |
| `0x6F3B0E0` | 2949 | suppression scale using `TypicalSpeed` | same |
| `0x76D8A00` | 986 | `UWDProjectileMove` **GenerateMove** | same |
| `0x76D9110` | 2727 | `UWDProjectileMove` simulation tick | same |
| `0x76CC730` | 140 | `UWDArtilleryProjectileMove` move generator | same |

Vtables: `UWDProjectileSubsystem` `0xB440498` (tickable `0xB440798`),
`UWDProjectileMove` `0xB676380`, `UWDArtilleryProjectileMove` `0xB6720E8`,
`UWDGlideProjectileMove` `0xB673188`. Several of the cited addresses
(`0x6F2E240`, `0x6F2E4B0`, `0x6F30680`, `0x6F3D130`, `0x76E07D0`) have no row
in the decompilation corpus; they were read as raw bytes. The corpus's
decompiled output of `0x6F3C060` and `0x6F3CB80` shows some helpers as `unk_*`
calls; their bodies are the ones listed.

Reproduce:

```text
python _tools/projectile_flight_check.py
WARDOGS_ANALYSIS_EXE=<analysis image> python _tools/projectile_flight_check.py
```

---

## 12. What is open

1. **Which mover mode `BP_155mm_Standard` uses, and what its Blueprint does.**
   The Blueprint export (see
   [Artillery shell flight data](../game-features/Wardogs_ArtilleryShellFlight_v1.md))
   shows `BP_155mm_Standard` uses mode `Mover.Mode.Projectile.Standard`
   (`WDProjectileMove`, empty `DA_DummyMovement`) and its bytecode only spins
   the mesh and computes travel-time fractions, so §7 applies to it.
   `BP_155mm_Expensive` uses the `Artillery` mode (`WDArtilleryProjectileMove`)
   with `InputMultiplier` 0.02, whose rotation step is not traced. If the actor's Blueprint calls
   `Set Velocity`, adds its own forces, or overrides the mode, §8 does not
   apply to it.
2. **World gravity.** Resolved: −980.0 cm/s² (§4). Open only: override volumes
   in world-partition cells, and any gravity scale applied by the artillery
   mode.
3. **`Rate`.** Resolved in round 23: `SimulationFrameRate` = 30 (class default and `DefaultGame.ini`),
   so the native step is 33 ms (§3). Still open: the mover time step of the actor-driven path (probably the
   `FixedTickFrameRate=30` fixed policy, 33.3 ms), and whether any server config overrides the value.
4. **Subsystem flag `+0xB0`.** When set, `Tick` only advances `ElapsedTime` and
   checks the lifetime, without integrating (`0x6F3BE3A`). Its meaning
   (client replay, server verification, or a mode switch) is not established.
5. **Launch speed modifiers.** Whether `InitialBulletSpeedModifier` or attachment
   modifiers change `InitialBulletSpeed` before the spawn request (§2). Round 39: ammo-type modifiers do not (§2, ammo modifier applier); `component+0x114` is applied to the pellet speed in the shotgun path (Weapon Spread §11).
6. **`X` of the wind ramp** (§6.4): initial value and meaning (inferred
   `EffectiveRange × 100`); the unit of the wind vector. Round 39: the spawn request range is `EffectiveRange × 100 ×` the ammo's `EffectiveRangeMultiplier` (AP 1.2, HP 0.8; §2), still not seen to be the same field as `X`.
7. **Thrust instability** (§6.1): the two scalar functions `0x1498F816A` and
   `0x1498F815E`.
8. **Artillery mode rotation** (§7): what `WDProjectileSyncState +0x80` holds
   and how `InputMultiplier` feeds it.
9. **Arming tag `0xD3815F8`** (§10): consumer and meaning; whether the 155 mm
   shell is blocked from detonating by it.
10. **`DragModel.Value = 80`** on the Standard 155 mm (and `_SB`) assets against
    2.5 on the Expensive asset: data intent unknown; §8 shows its effect. The survey of every projectile
    asset ([round 23](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round23-projectile-drag-survey.md))
    finds 80 only on the 155 mm Standard family and `DA_155mm_Expensive_ProjectileData_SB`, which carries
    the Standard numbers (70 kg, 8.4 cm).
11. **Actor-driven lifetime.** Which code ends an actor-driven projectile at
    `MaxProjectileLifetime` (40 s for 155 mm).
12. **Runtime check.** Nothing here was observed running; the equations are
    static readings.

Related: [Damage Pipeline §7.8](Wardogs_DamagePipeline_v2.md) (speed scale after
drag), [Combat Data Flow](Wardogs_CombatDataFlow_v1.md),
[Units](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/UNITS.md), [native defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round17-native-defaults.md),
[artillery range check](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round21-artillery-range-check.md) (the model against logged impacts and the calculator table).
