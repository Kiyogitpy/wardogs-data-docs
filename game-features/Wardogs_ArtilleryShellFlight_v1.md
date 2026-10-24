---
title: "Artillery Shell Flight Data"
redirect_from: ["/Wardogs_ArtilleryShellFlight_v1.html", "/Wardogs_ArtilleryShellFlight_v1"]
parent: "Weapons & Ammo"
description: "155 mm artillery shell flight: Blueprint actors, mover modes, gravity and how the shell moves"
---

# Wardogs: Artillery Shell Flight Data (what is and is not known)

The 155 mm shell data assets (`DA_155mm_*_ProjectileData`) set `bActorHandlesProjectileMovement: true` and name a Blueprint actor. This page records what the cooked actor and the world settings contain, and what they do not. All numbers below are read from the game's own paks with the offline extractor; nothing was run or fitted. The rows are in [`assets/data/shell-actors.json`](../assets/data/shell-actors.json) (written by [`_tools/shell_actors.py`](../_tools/shell_actors.py)); the round 21 export of the actors is the first time they are in this repository (the `ProjectileActors` folder under `data/` holds only camera assets).

## 1. Which actor flies which shell

| Data asset (`WDProjectileData`) | `ProjectileActor` | Native parent class | Mover mode class (tag) |
|---|---|---|---|
| `DA_155mm_Standard_ProjectileData`, `..._SB` | `BP_155mm_Standard` | `WDProjectile` | `WDProjectileMove` (`Mover.Mode.Projectile.Standard`) |
| `DA_155mm_Expensive_ProjectileData`, `..._SB` | `BP_155mm_Expensive` | `WDCameraProjectile` | `WDArtilleryProjectileMove` (`Mover.Mode.Projectile.Artillery`) |

The same export covers the other actor-driven projectiles named by a `DA_*_ProjectileData`: `BP_120x570mm`, `BP_120x800mm` (artillery mover), `BP_125x570mm`, `BP_122mm`, `BP_40mm`, `BP_72mm`, `BP_84mm`, `BP_93mm`, `BP_Drone_Projectile` (`WDGlideProjectileMove`) and `BP_MoverProjectile` (`WDTVGuidedProjectileMove`). No mortar projectile data asset (`DA_*_ProjectileData`) exists in the export (mortar is audio only), but the mortar does have a range table: see section 5.

Fields on the 155 mm data assets that feed the actor (all `ProjectileStats`):

| Field | Standard (and `_SB`) | Expensive (`_SB` identical) |
|---|---:|---:|
| `TypicalSpeed` | 15000.0 | 15000.0 |
| `ThrustSpeed` | 22000.0 | 22000.0 |
| `MaxProjectileLifetime` | 40.0 | 40.0 |
| `ProjectileDimensions.Mass` | 70.0 | 19.0 |
| `ProjectileDimensions.DragModel.Value` | 80.0 | 2.5 |
| `bShouldPreSimulate` / `bClientPredictive` | false / false | false / false |

## 2. What the Blueprint actors set

Both actors are Mover-driven: a `BHMoverComponent` holds one movement mode, and the mode is a native class. The Blueprint stores **no** speed, thrust, drag, gravity-scale, bounce or max-speed value.

| Item | `BP_155mm_Standard` | `BP_155mm_Expensive` |
|---|---|---|
| Mover mode class | `WDProjectileMove` | `WDArtilleryProjectileMove` |
| Mode data asset | `DA_DummyMovement` (`BHPawnMoverModeData`, an empty export: no properties stored) | none |
| Mode properties stored in the Blueprint | none | `InputMultiplier` 0.02, `bIgnoreVerticalInput` true |
| Shared mover settings (`BHCommonMovementSettings`) | no values stored | no values stored |
| Sync state types | `MoverDefaultSyncState`, `WDDefaultProjectileSyncState` | `WDProjectileSyncState`, `WDDefaultProjectileSyncState` |
| `bHandlesOwnLifetime` / `ExtendedLifetime` | true / 2.0 s | true / 2.0 s |
| `ProjectileVelocityMultiplier` | 1.0 | 1.0 |
| Actor tick | `bCanEverTick` true (CDO) | not set in the CDO (`ReceiveTick` is implemented) |
| Collision box extent (`BoxComponent`) | 30.6 x 5.5 x 5.5 | 30.6 x 5.5 x 5.5 |
| `SpinSpeed` / `SpinRotator` | 100.0 / yaw 1.0 | 20.0 / yaw 2.0, pitch and roll 0.001 |
| `TravelTimeZoomOutRange` / multiplier range | 0 to 30 / 0.1 to 0.01 | 0 to 20 / 0.1 to 0.01 |
| Camera (Expensive only) | - | spring-arm data asset `DA_155mm_Expensive_Camera`, shake `B_CameraShake_ArtilleryTravel`, HUD layout `UI.HUD.Layout.Vehicle.Gunner.Artillery`, fade 4.0 s |

Blueprint bytecode (the Event Graph, `ReceiveTick`, and the debug print function) only does presentation work:

- `BP_155mm_Standard`: each tick reads `GetCurrentTravelTime` and `GetExpectedTravelTime` (native, on `WDProjectile`), clamps and divides them into a normalized travel duration, and adds a local rotation to the mesh (`SpinRotator` times `SpinSpeed`). `PrintDebugMessages` prints the travel times when `bDebug` is set.
- `BP_155mm_Expensive`: the same spin, plus camera work (detach from the shell after a travel time, zoom-out with `MapRangeClamped`, free-look toggles, camera shake stop). It reads the weapon's fire simulation data (`GetWeaponFireSimulationData`) and sets a world location on a component, but the calls found are all camera and presentation calls.
- Neither Blueprint calls anything that applies force, thrust, drag or gravity to the shell, and neither writes a velocity.

So the flight of the 155 mm shell is computed by the native Mover mode classes, from the data-asset fields above. That native code is not in the data export.

## 3. World gravity

| Source | Value |
|---|---|
| `Engine/Config/BaseEngine.ini`, `[/Script/Engine.PhysicsSettings]` | `DefaultGravityZ=-980.0` |
| `Wardogs/Config/DefaultEngine.ini`, same section | section present, **no gravity key** |
| `WDWorldSettings` of the nine map files (Europe, Kavkazi, NorthAmerica, Russia, Frontend, Gym_Minimal, MovementGymTestLevel, DiscoveryMap, PocketWorldLevel) | no `bGlobalGravitySet` / `GlobalGravityZ` property stored |

Result: world gravity is the UE default of -980.0 cm/s^2 (9.8 m/s^2 downward), taken from the base engine config packed in the game paks. The `.ini` files were read from the paks, not from a game install folder. Not checked: gravity-override volumes placed in the world-partition cells of the four large maps (the cell files were not scanned), and whether the native projectile mover applies world gravity, a gravity scale of its own, or none (see section 4).

## 4. What is not known

- **Native thrust and drag maths** (`WDProjectileMove`, `WDArtilleryProjectileMove`): decoded on [Projectile Flight: Thrust, Drag and Gravity](../pipelines/Wardogs_ProjectileFlight_v1.md). Gravity, drag and wind are modelled natively with the same force model as every other projectile; the 155mm assets set `ThrustSpeed` but never `bShouldThrust`, so the shell does not thrust. The `WDArtilleryProjectileMove` rotation step is still untraced.
- How `TypicalSpeed`, `ThrustSpeed`, `Mass`, `DragModel` and `MaxProjectileLifetime` enter the mover: not known from data alone. The existence of a native range helper `WDArtilleryRangeLibrary::SimulateImpactDistance` (inputs: projectile stats, weapon stats, an air-density value) shows that range is simulated natively, but its body is not in the export.
- Units of the data-asset fields: still the UE convention (cm, cm/s, kg as stored). Only the gravity value is confirmed against the engine config.
- Whether the native mode constructors give non-zero default values for speed limits, drag or gravity scale: the Blueprints store none, so any such values live in native constructors and are not in this file.
- No curve is fitted to calculator or in-game range data on this page. The relation between the range tables' milliradians and the sight's dial mils on the SPH-2 is not known (section 5).

## 5. `ArtilleryRangeData` tables (game range tables)

Three weapon extension data assets carry a table `ArtilleryRangeData`: a list of rows `{Milliradians, ImpactDistance, TravelTime}`. `ImpactDistance` is in metres and `TravelTime` in seconds (the SPH-2 values match the flight maths in seconds, section 4 of the projectile-flight page; the unit is not stated in the export).

| Weapon | Asset | Rows | Milliradians | ImpactDistance (m) | TravelTime (s) |
|---|---|---:|---|---|---|
| SPH-2 | `WE_TNK_01_Artillery` (`Vehicles/TNK_01/.../WeaponExtensions/Artillery/`) | 41 | 20 to 1400, rising | 600 up to 2,600 (at 619 mrad), then back down to 700 | 2.74 to 23.73 (low arc), 27.68 to 37.00 (high arc) |
| L81 Mortar | `WE_STN_03_Heavy_MainBarrel` (`Vehicles/STN_03/.../WeaponExtensions/`) | 17 | -500 to 300 in steps of 50 | 684 down to 80 | 15.94 to 22.39 |
| Stingray | `WE_STN_05_Heavy_MainBarrel` (`Vehicles/STN_05/.../WeaponExtensions/`) | 17 | -500 to 300 in steps of 50 | 697 down to 80 | 15.94 to 22.39 (identical to the mortar's) |

The SPH-2 table is a low arc rising to the longest row, then a high arc with the elevation still rising and the distance falling. The mortar and Stingray tables have one arc each. The tables are stored data; how they were produced (the native range helper named in section 4 is one candidate) is not known. `python -I _tools/artillery_range_tables.py` prints all three, and `--calc <weapons.json>` compares them with the community calculator's dial readings.

Comparison with the community calculator (`wardogs-calculator`, dial mils measured on the in-game MIL scale; `_tools/artillery_range_tables.py --calc`), same range, game mrad minus calculator mil:

| Weapon | Difference | Note |
|---|---|---|
| SPH-2 low arc | +44.5 to +97.3 (median +50.5), 15 rows | not constant: smallest near 2,000 to 2,200 m, largest at 2,600 m and at the short end |
| SPH-2 high arc | -33.8 to -1.6 (median -5.4), 18 rows | shrinks toward short range; largest at 2,500 m |
| L81 Mortar | -650.0 to -648.0, 17 rows | a constant shift of 650 (the calculator's rows are 150 to 850 mils; the game table's last two rows, 250 and 300 mrad, sit at 900 and 950 on that scale, outside the 150 to 850 sight limits) |
| Stingray | none | the calculator has no Stingray table |

The SPH-2 offset is not a unit conversion or a fixed shift, and its cause is not known. The calculator values were measured in game on the dial and checked against logged impacts (round 21), so the dial values are the ones to use for aiming.

Comparison with `shell_sim.py` (Expensive shell, elevation = mrad / 1000 rad as degrees, 1 ms step), SPH-2 rows only:

| Arc | Range, sim minus game | Travel time, sim minus game |
|---|---|---|
| Low (21 rows) | -283.4 to -18.1 m (median -102.7), short of the game range at every row, worst at the short end | -1.57 to -0.47 s (median -0.8); sim is 43 to 98 percent of the game time |
| High (19 rows) | +21.8 to +103.6 m (median +59.9) | -0.44 to -0.11 s (median -0.2); sim is 98.4 to 99.7 percent of the game time |

So the game's high-arc travel times agree with the flight maths at the table's own true-milliradian elevation to within 0.4 s, while its low-arc times are up to 1.6 s longer, and in both arcs the ranges at that elevation differ by tens to hundreds of metres. This does not show that the table elevation is the true barrel elevation; it shows only that the travel times are close to it on the high arc. The mortar and Stingray are not simulated (no 120 mm flight data). The mortar and Stingray rows have one travel time (20.0 s at -300 mrad) that breaks the trend of its neighbours (17.86 s above, 19.02 s below); it is identical in both tables and unexplained.

## 6. Reproduce

1. Build `tools/cue4parse_extractor` ([README](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/tools/cue4parse_extractor/README.md)); `list BP_` finds the actor packages, `dump <files.txt>` exports them and `rawfiles <text> --copy` writes the packed `.ini` files.
2. `python _tools/shell_actors.py --dump <dumpdir> --world <dir with world.json>` rewrites `assets/data/shell-actors.json`.
3. `python -I _tools/artillery_range_tables.py [--calc <weapons.json>]` prints the three range tables of section 5 and the comparisons.
