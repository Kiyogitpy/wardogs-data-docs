# Round 91: vehicles (veh)

Items V5-01 and V5-08 of `BACKLOG-v5.md`. Evidence: cooked JSON exports under `data/Wardogs` (static) and the decompiled corpus `decompiled_cl516586_20261017_mmvpuc__` plus capstone over the restored executable (static; nothing was run, nothing devirtualized). All addresses are RVAs. Work scripts were kept in `E:/r91/work/veh/`, not committed.

Generator: `_tools/vehicle_round85_tables.py` (`--write`, `--check`) now also writes `assets/data/vehicle-gameplay-settings.json` and section 6 of `game-features/Wardogs_VehicleConfigFields_v1.md`.

## Status

| Item | Status | Where |
|---|---|---|
| V5-01 abandoned-vehicle lifetime (`InactivitySettings.InactivityLifetimeOutSafeZone`) | FOUND (data; meaning from the name, removal not traced) | config page section 6. Havoc 90 s, MH-6 family 10 s, stationary emplacements STN_01/02/03/05/06 30,000 s; every other vehicle sets none |
| V5-01 `bIsInventoryAccessible`, `LockSettings`, `FactionSettings` | FOUND | same table. Inventory accessible on every asset that sets `InventorySettings` (not set on Bobcat, Dune Buggy, STN_04, airplane); one lock cue tag everywhere; faction settings only on STN assets (`bShouldFactionChange` false, STN_04 neutral after 36,000 s) |
| V5-01 `bAllowSameFactionOccupantsOnly` | FOUND, reader NATIVE (follow-up) | 6 interaction assets: Havoc, M113 APC SV, Gepard, SPH-2, L2A6, T-72B3. Short note added to the Seats and passengers wiki article |
| V5-01 ramming fields (`WD_MVF_DestructionInvokerFragment`) | FOUND (14 platforms), readers NATIVE (follow-up) | config page section 6: collision box, centre, mass, `DamageRecievedWhenChunkDestroyed` (8 platforms: 200 / 150 / 3), `CounterForceMultiplier` (9), `VelocityOffsetMultiplier` (14). JSON in `assets/data/vehicle-gameplay-settings.json` |
| V5-08 auto-trim row selection | FOUND (native, static) | flight-model page section 6a; details below |
| V5-08 drag formula and units of the six areas | NOT RESOLVED | details below; no physics envelope published |

## V5-08 auto-trim row rule (native)

Class `UBHAutoTrimCurveSamplingRotaryMovementControlAssistBody` (the class the airplane pitch assist uses), vtable functions found through the corpus `aliases` table:

- `0x5366870` (load): walks the rows of the `CurveTable` (`+0x28`). A row name must contain `Gear_` (number parsed) and `Thrust_` (number parsed). The row goes into one of two arrays: gear number 0 into the array at `this+0x40`, any other number (1) into the array at `this+0x30`. Each element is `{thrust key = number * 0.01 (double), curve object}`. Both arrays are then sorted (`0x534FB90`, by the key).
- `0x5379DE0` (evaluate): reads the landing-gear state through `0x532CC30`. The state byte follows `EMAirplaneLandingGearStateId`: Down(1) gives blend 0, Up(3) gives blend 1, Retracting(2) and Extending(4) give a progress fraction from two floats of the state record (the code is identical for both transit states, so the direction in transit is inferred, not read). Blend 0 samples the `Gear_0` list, blend 1 the `Gear_1` list, in between both are sampled and `(g1 - g0) * blend + g0` is returned. So `Gear_1` is the gear-up set and `Gear_0` the gear-down set (this agrees with the earlier reading from the names).
- `0x5353990` (sample one list): looks up the current engine thrust ratio (`0x532C850`, float, 0 to 1) with a binary search over the sorted keys, takes the two neighbouring rows (the first or last row alone outside the range), weight `t = clamp((ratio - key_lo) / (key_hi - key_lo), 0, 1)`, evaluates each row's curve through the curve object's virtual at `+0x88` (`GetFloatValue`, disassembly: `movsd xmm1,[rsi+8]; call [rax+0x88]`) at the airspeed, and returns `v_lo + t * (v_hi - v_lo)`. A zero key distance gives 0 or 1 by comparison.
- The airspeed argument: in the evaluate function the vehicle's body-space velocity is rotated into the airplane frame by the inverse of the body rotation (the constants `(-1,-1)` and `(-1,1)` are the quaternion conjugate), the forward component is taken, and the value goes through `0x14163E5D0(value, 12, 14)`. 12 and 14 match `EUnit::CentimetersPerSecond` and `EUnit::KilometersPerHour` in the engine's unit enum (identification by enum position only; the converter body was not opened). That agrees with the table name `...ByAirspeedKmPH` and with the keys running to 1200.

Consequence for the page: the table is interpolated in both throttle and airspeed, so the 22 rows are control points, not steps. The zero crossings the page publishes (140 km/h at 10% throttle, 430 km/h at 100%, gear up) stay valid as read-from-table figures at those exact throttle keys; between the keys the native code blends.

## V5-08 drag and lift formula: NOT RESOLVED

What was tried (all static):

- SDK offsets: `UBHAirplaneMovementComponent+0x4A0` = `DragDataAsset`; `UBHAirplaneDragDataAsset` doubles at `+0x30` (`AirDensityAtSeaLevel`), `+0x38` to `+0x58` (front, rear, side, bottom, top area), `+0x60` (`DragCoefficient`), torque coefficients from `+0x70`. Engine asset: `MaxEngineThrust_n` at `+0x70`, `MinEngineThrust_n` at `+0x74`.
- Corpus scans for `+ 1184` (with and without the `LL` suffix) over `0x5200000` to `0x5500000`: no airplane function dereferences the drag asset through the component. Corpus-wide scans for functions reading six or seven of the offsets `+0x30` to `+0x60` as doubles; capstone scans over `0x5200000` to `0x5500000` for double loads at those displacements (7 of 7 in about 40 functions; the ones inspected in the airplane code range, `0x533D040`, `0x53C3AA0`, `0x53C7200`, are transform and ground-trace code); a scan for the debug-draw flag byte at `+0x68` together with the double loads (4 functions, none drag); scans for float loads at `+0x70` and `+0x74` of the engine asset (14 functions, none engine thrust).
- The airplane movement component's own vtable functions (about 40 unique ones in `0x531E37C` to `0x5377360`) hold setup, networking, runtime-config labels (the serializer `0x5339040` names `"DragData."`, `"FlightCharacteristics."`, `"BodyData."`) and control code; none holds the force computation. The force step is most likely a physics-thread callback that the vtable does not reach, or sits in code the corpus did not attribute to the class; it was not located.

Why no envelope: the unit of the six areas (square centimeters or square meters), whether the thrust is multiplied by 100 on the way to the physics engine's force unit (kilograms times centimeters per second squared, so newtons times 100), and whether the lift multiplier applies to drag are native facts that were not read. The round 85 model assumed SI inputs and landed a factor of two away from the auto-trim zero crossings; because the auto-trim table is itself native-confirmed to be sampled by forward speed in km/h and by thrust ratio, the 140 and 430 km/h figures are the only speed figures the game's own data supports. The page keeps them; no stall speed or top speed is published. A next step is to find the aerodynamics step from the physics side (the callback set up in the component's initialization `0x5330CD0`, which sizes arrays at `+0x4F8` to `+0x640`) rather than from the data asset pointer.

## Follow-up: native readers (V5-01) and the physics callback (V5-08)

### Same-faction flag: `UWDVehicleOperatorComponent` vtable slot 163, `0x7693880`
The function builds the enter-denied result for an interaction. It reads the data asset through the weak pointer at `vehicle component+472` and tests the byte at `+168` (`bAllowSameFactionOccupantsOnly`). With the flag set: faction of the vehicle's owner (component at `+1576`) against the enterer's faction; if they differ and the vehicle faction is not the neutral global `0x14D2692F8`, the denial tag `0x14D2E7A88` is added. It then loops over the seats (count byte at `+232` of the interaction object) and denies when any occupant's faction differs from the vehicle faction. After the flag block, a second test (`0x14767A1B0` on the vehicle component, not decoded) denies entry when the factions differ and the vehicle is not neutral, with or without the flag. Which object is "enterer" and which "occupant list" in the loop is from the decompiler's argument flow (static, moderate confidence).

### Ramming fields: component `UWDVehicleDestructionInvokerComponent` (members of the fragment copied at start-up)
- `0x76AC670` copies the fragment into a 0x48-byte block stored at component `+0xE8` by `0x6BCA060`: centre `+0xE8`, extents `+0x100`, constant float 0.04 at `+0x118`, `VehicleMass` `+0x11C`, `VelocityOffsetMultiplier` `+0x120`, `DamageRecievedWhenChunkDestroyed` `+0x124`, `CounterForceMultiplier` `+0x128` (store offsets read from the disassembly of `0x76AC670`).
- `0x6BC96E0` (sweep callback): sweeps the box (half extents = extents x 0.5) with the box centre shifted by velocity x `+0x120`; computes `speed x VehicleMass` and returns early below a threshold from `0x1465297A0`; hit destructibles get `0x6BC8F60` with that product as the fourth argument.
- `0x6BC9160` (chunk-destroyed event): calls `0x6BC9250`, which invokes a vtable function (`+0x500`) of the owner's damage object with `+0x124` as the amount, then adds the event's float to the pending total at `+316` and schedules `0x6BC9450`.
- `0x6BC9450` (delayed): clamps the pending total to 0 to 300,000, takes the direction from the owner's velocity, applies `-(total x direction x +0x128)` through owner vtable `+1800`, resets the total to 0.
Not read: the numeric threshold behind `0x1465297A0`, and what the `+0x500` call does with the amount beyond naming it damage (it is the amount-taking call on the damage object).

### Abandoned-vehicle lifetime: no reader in the client
`InactivityLifetimeOutSafeZone` is copied from the data asset (`+1368`) into the gameplay-systems component (`+1884`) at `0x767BC40`. Displacement scans (`0x75C`, `0x558`) over `0x6000000` to `0x8000000` find no function that reads the value (the other hits are unrelated fields at the same offset). The removal runs on the server. `UBHVehicleLifetimeManager` (settings `VehicleLifetime`, `DisabledVehicleLifetime`, `ParkedBadlyVehicleLifetime`, damage tick) is the related server-side class; its values are not in the exports.

### V5-08 physics callback: still not found
- The callback registered in the init `0x5330CD0` is `0x5334F50`, a replication-role check forwarding to `0x142480AB0`; it is not the aerodynamics step.
- Unit conversion `0x163E5D0` is the engine's generic converter: units in `dl` and `r8b`, `result = factor(from) x value / factor(to)` with a same-group check through the table at `0x9AD3AD0`. With 12 and 14 this is centimeters per second to kilometers per hour by enum position, so the auto-trim keys are km/h (the converter's table was not decoded).
- Further scans over `0x5200000` to `0x5500000`: float loads at the aerodynamic settings offsets of the flight data (`MainLiftMultiplier`, `MaxSpeedForLiftCalculations_kmh` and the altitude multipliers: 8 functions, all copy or compare code) and for the airfoil array. No lift, drag or thrust arithmetic was located. The aerodynamics step is probably in protected or unattributed code. No formula or unit was confirmed, so no speed envelope is published.
