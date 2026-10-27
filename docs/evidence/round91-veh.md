# Round 91: vehicles (veh)

Items V5-01 and V5-08 of `BACKLOG-v5.md`. Evidence: cooked JSON exports under `data/Wardogs` (static) and the decompiled corpus `decompiled_cl516586_20261017_mmvpuc__` plus capstone over the restored executable (static; nothing was run, nothing devirtualized). All addresses are RVAs. Work scripts were kept in `E:/r91/work/veh/`, not committed.

Generator: `_tools/vehicle_round85_tables.py` (`--write`, `--check`) now also writes `assets/data/vehicle-gameplay-settings.json` and section 6 of `game-features/Wardogs_VehicleConfigFields_v1.md`.

## Status

| Item | Status | Where |
|---|---|---|
| V5-01 abandoned-vehicle lifetime (`InactivitySettings.InactivityLifetimeOutSafeZone`) | FOUND (data; meaning from the name, removal not traced) | config page section 6. Havoc 90 s, MH-6 family 10 s, stationary emplacements STN_01/02/03/05/06 30,000 s; every other vehicle sets none |
| V5-01 `bIsInventoryAccessible`, `LockSettings`, `FactionSettings` | FOUND | same table. Inventory accessible on every asset that sets `InventorySettings` (not set on Bobcat, Dune Buggy, STN_04, airplane); one lock cue tag everywhere; faction settings only on STN assets (`bShouldFactionChange` false, STN_04 neutral after 36,000 s) |
| V5-01 `bAllowSameFactionOccupantsOnly` | FOUND (data; the check itself not traced) | 6 interaction assets: Havoc, M113 APC SV, Gepard, SPH-2, L2A6, T-72B3. Short note added to the Seats and passengers wiki article |
| V5-01 ramming fields (`WD_MVF_DestructionInvokerFragment`) | FOUND (14 platforms; per-field meaning from names, Derived) | config page section 6: collision box, centre, mass, `DamageRecievedWhenChunkDestroyed` (8 platforms: 200 / 150 / 3), `CounterForceMultiplier` (9), `VelocityOffsetMultiplier` (14). JSON in `assets/data/vehicle-gameplay-settings.json` |
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
