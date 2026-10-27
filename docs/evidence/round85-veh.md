# Round 85: vehicle physics data (veh)

Items V4-03, V4-07, V4-14, V4-15 of `BACKLOG-v4.md`. Statuses: FOUND, ABSENT, SERVER, PROTECTED. Evidence: cooked JSON exports under `data/Wardogs` (static), and the decompiled corpus `decompiled_cl516586_20261017_mmvpuc__` (read only; the game was never run, nothing devirtualized).

Generator: `_tools/vehicle_round85_tables.py` (`--write`, `--check`) writes three pages:

- `game-features/Wardogs_FixedWingFlightModel_v1.md` (V4-03)
- `game-features/Wardogs_VehicleConfigFields_v1.md` (V4-07, V4-14)
- `game-features/Wardogs_VehicleTurretControls_v1.md` (V4-15)

## Status

| Item | Status | Where |
|---|---|---|
| V4-03 flight, drag, engine fields of FWG_01 | FOUND | Flight-model page sections 1, 2, 4. `BHAirplaneDragDataAsset` 16 of 17 fields were unnamed on any page; all 17 are tabled now |
| V4-03 lift, drag, nose-steering curves | FOUND | section 3 (keys plus derived values every 2 to 5 degrees) |
| V4-03 22-row auto-trim table | FOUND | section 6a (row, key count, plateau end, zero crossing, end value); full keys stay in the export |
| V4-03 control assist stacks | FOUND | section 5 (PID gains, damping, throttle change rates, conditions) |
| V4-03 derived speed envelope | FOUND, labelled derived | section 6b |
| V4-07 wheeled, tracked, rotary config sub-fields | FOUND | config page sections 1 to 3. Gameplay cue tags and prediction-settings internals are left to the export |
| V4-07 `MTrackedVehicleWheelData` | FOUND | config page section 2 (spring rate, suspension length, wheel radius, incline angle, incline grip, lateral friction) |
| V4-07 `BHRotaryFlightDataAsset`, `BHAirVehicleDragDataAsset` | FOUND | config page sections 3 and 4 |
| V4-07 wheel `Values[state]` read | still open (L, carried from v3) | not touched |
| V4-14 refuel and repair station rates | FOUND earlier (already on the station page: Fast 5% in 3 s, Max 9 s; canister 2.0 per 0.75 s; drills); the two stale "not traced" lines in `Wardogs_Buildables_v1.md` now point there | no new data needed |
| V4-14 vehicle fuel burn in play | FOUND (static native read) | config page section 5; `FuelSettings` KML and RPML were undocumented |
| V4-14 build cost, build time | SERVER (stays closed) | not touched |
| V4-15 six vehicle crosshair tables | FOUND (there are eight tables; STN_01 and STN_06 are empty) | turret page section 4 |
| V4-15 23 `WDVehicleWeaponDataAsset` | FOUND | turret page sections 1 to 3 |

## V4-03 derived speed envelope

The data has no top speed or stall speed (round 39 said so; that stays true). The derived estimate is in the flight-model page section 6b with its formula and inputs. Method:

- Inputs: `MassOverride` 10,000 (read as kg), `MaxEngineThrust_n` 226,800 (read as N), `MainLiftMultiplier` 0.4, density 1.25 kg/m3 (`AirDensityAtSeaLevel` 0.00125 read as g/cm3), g 9.81 (assumed), airfoil areas and incidence angles from `DA_FWG_01_FlightCharacteristics`, lift and drag curves evaluated as Unreal rich curves (Bezier handles from the stored tangents and weights; script `rich curve` code in the generator).
- Lift = q x 0.4 x sum(area x CL(alpha + incidence)) over the up-lifting airfoils (all but the airbrake, which is force 0 retracted, and the rudders, which lift sideways). Drag = q x sum(area x CD(alpha + incidence)) over the eleven non-airbrake airfoils. Body drag fields left out (their native formula is not decoded; read as cm2 they would add under 1%).
- Result: the lift sum peaks at 14.9 degrees (area-weighted coefficient 207 m2), level stall about 99 km/h; drag equals full thrust near 880 km/h.
- Cross-check: the auto-trim table zero crossing (speed with no pitch trim) is 140 km/h at 10% throttle and 430 km/h at 100% (gear up). The physics model puts the same throttles at 273 and 879 km/h. They disagree by about 2x; the page says so and treats 430 km/h as the designer-tuned figure and 880 km/h as an unvalidated upper bound. The disagreement could come from the unit readings, from the thrust being speed-dependent in native code, or from drag terms in native code; none can be tested without running the game.

Neither number is a stored top speed; the wiki page says "closest the data comes to a cruise speed" for the auto-trim figure and "derived, with assumed units" for the physics figure.

## V4-14 native trace (static)

Entry point named in the backlog: `Auth_RefillFuel` exec thunk `0x7667280`. It adds a float to the fuel attribute through `0x52311D0` (known since round 4). The refill amounts that matter to players (station Fast/Max, canister, drills) are data-driven and were already found.

New: the fuel burn tick of `UWDVehicleFuelComponent`.

| RVA | What it does |
|---|---|
| `0x7666FA0` (`sub_147666FA0`, vtable slot 131) | Tick with `dt` in `xmm1`. When the owner byte `+0x170` equals 3 and the component flag `+0x134` is clear: `drain = burnRate(owner) * dt`, plus `leak * dt` if the leak value at `+0x178` is positive (the value set by the `WDFuelComponentEffect` leak steps); if the sum is above 0.0001 the fuel attribute is lowered through `0x52311D0` on the handle at `+0x138`. Otherwise it calls a virtual at `+0x428` with 0 (stops the tick) |
| `0x7665DB0` (`sub_147665DB0`) | `burnRate`. `v4` = owner virtual at `+0x9C8` (speed, km/h as the 1/3600 constant implies). If `v4` is at most the threshold in slot `a1[70]`, a second owner virtual (`+0x950`, probably engine RPM, result dropped by the decompiler) is multiplied by `(1/3600) / a1[71]`; otherwise `v4 * (1/3600) / a1[69]`. If owner virtual `+0x940` says boosting, multiplied by `a1[74]`. Finally multiplied by `a1[95]` (the fuel-usage multiplier, `GetFuelUsageReductionMultiplierValue`), or by a curve sample at `+82` when `a1[95]` is below -0.0001 (sentinel) |
| `0x7666F20` | tick enable / disable by owner state 3 |

Slot-to-field mapping is inferred, not decoded: moving divisor = `KML` (checked against the data: vendor "fuel economy" equals 1/KML for Havoc 4.44, Humvee 3.33, Kodiak 2.86, Bobcat 2.22, Dune Buggy 5, Ural 4, M113 5.71, SPH-2 and L2A6 8, Gepard 10; T-72B3 differs, vendor 8.5 against 6.96), idle divisor = `RPML`, threshold = `IdleSpeedThreshold`, `a1[74]` = `FuelConsumptionOnBoostMultiplier`. `FWDFuelSettings` field order from the SDK dump is MaxFuel, KML, RPML, IdleSpeedThreshold, LowFuelThreshold, FuelConsumptionOnBoostMultiplier, but the runtime copy in the component is ordered KML, IdleSpeedThreshold, RPML, ..., boost, so the cooked layout was not used. `IdleSpeedThreshold` and `LowFuelThreshold` are never set in the cooked assets, so their defaults (native constructor) are not known; the idle burn can therefore not be given in litres per second. Status: moving burn FOUND (static, inferred slot map); idle burn NOT RESOLVED.

Nothing was run. Elytra-virtualized code was not touched; the fuel component code is plain.

## Other findings worth recording

- `WDVehicleWeaponDataAsset` has no camera data for the Havoc and Little Bird rocket pods and the Little Bird grouped machine guns (`W_ROT_02_122mm`, `W_ROT_03_122mm`, `W_ROT_03_AttachedMachineGuns_Grouped`).
- Tank main guns (`W_TNK_03`, `W_TNK_01_Artillery`, `W_TNK_01_Heavy`, `W_TNK_04`) and the Havoc 30 mm cannon use `FullSim` turret simulation with drive strength (2,000 to 10,000) and damping 0.05; every other turret uses a plain rotation speed.
- Several STN and ring-turret assets store the yaw limits with the limit flag unset (STN_01/02/03/05 as min 90 / max -90). What the engine does with an unset flag is not traced.
- Air drag: Havoc and FWG_01 share the same front area and coefficient; FWG_01 has 4x the top and bottom area and 10x the angular-velocity torque coefficients.
- The airplane has no `FuelSettings` at all (no max fuel, no KML), so it cannot burn fuel in any way the data describes.

## Not resolved

- The unit and the exact native formula of the six drag areas; hence the body drag in the speed envelope.
- Idle fuel burn (default `IdleSpeedThreshold`, RPM source).
- Whether auto-trim row selection uses landing gear state and throttle exactly as the row names suggest (native).
- Wheel `Values[state]` read (carried).

## Checks run

- `python -I _tools/vehicle_round85_tables.py --check` exits 0.
- `python -I _tools/check_links.py`: 0 broken.
- Secrets grep on `git diff main...HEAD` (see commit).
- `content/Wardogs_DataTables_*` were not regenerated: running `_tools/datatable_catalog.py --write` produces about 180 lines of unrelated churn from earlier rounds (stale "Documented in" links), so it was left for the lead; the new turret page names all eight `DT_VehicleCrosshair_*` tables, so the next run lists it.
