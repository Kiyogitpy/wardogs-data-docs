# Round 40: vehicles, explosives and throwables (RE40-VEH)

Continues [round 39](round39-vehicles-explosives.md). Statuses: FOUND, PROTECTED (path enters the protection layer; entry RVA given), ABSENT, NATIVE (open: what was read is stated). Evidence levels: cooked data read, Blueprint bytecode read, static disassembly (capstone on the restored exe and the decompiled corpus). The game was never run, no devirtualization. Extractor output and helper scripts: `E:/Reverse_Engineer/wardogs_analysis/round40_veh/` (`d1/` dumped `B_TNK_01`, `B_SPW`, `B_FWG_01`; `rdis.py`/`rxref.py` are copies of the round 38 helpers renamed because `dis.py` shadows the stdlib `dis` module when capstone imports `inspect`; `vcall.py` finds `call [reg+disp]` sites; `consts.py` lists Blueprint constants).

Generated data: `python -I _tools/vehicle_round40_tables.py --write` rebuilds `assets/data/vehicle-arcade-controls.json`, `vehicle-rotary-assists.json`, `vehicle-tire-models.json` and the page [`game-features/Wardogs_VehicleControlAssists_v1.md`](../../game-features/Wardogs_VehicleControlAssists_v1.md) (`--check` exits 1 when stale). The round 39 tool is unchanged.

Counts (18 entries below, covering the round 39 NOT DONE list): FOUND 11 (R40-1, 2, 4, 5, 6, 7, 8, 13, 14, 15, 16), ABSENT 1 (R40-9, plus the 30-degree sub-part of R40-14), PROTECTED 0 (no path entered the protection layer), NATIVE (open) 6 (R40-3, 10, 11, 17 worked but unresolved; R40-12 and R40-18 group the items not reached inside the timebox: 9 vehicle items and 10 explosive items, nothing guessed).

## Havoc projectile asset

Dropped from this round's scope: settled earlier, DamagePipeline O-9 closed. A pak-wide scan and the exe show `Item.Caliber.122mm.Havoc` is referenced only by the asset itself and two UI tables; the Havoc fires plain `Item.Caliber.122mm`. Not re-investigated.

## Vehicles

### R40-1 Empty fuel tank. FOUND (static disassembly); NATIVE for restart

Chain, all RVAs from the restored exe:

1. `UWDVehicleFuelComponent` fuel-attribute-changed handler `sub_1476667B0` (`0x76667B0`, args: component, old value `a4`): reads the fuel attribute (`component+312`), and when the new value is `<= 0.0` and the old value was `> 0.0` it broadcasts a delegate/message (`component+224`, the `WDVehicleOutOfFuelMessage` struct exists in the SDK), and then, if the owner pawn is the authority (`pawn+368 == 3`), calls **pawn virtual slot 303** (`call [vtable+0x978]`, `0x76667B0`).
2. Slot 303 on wheeled, tracked and base pawns is `sub_1453D6440` (`0x53D6440`): authority only; it **clears `bIsEngineRunning`** (`pawn+0x889`, SDK `Mechanized_classes.hpp` line 524, byte `+2185`), calls virtual slot 321 (`0x53D08A0`, the engine-state-changed handler that also runs from `OnRep_bIsEngineRunning`), and removes a gameplay tag/cue on the pawn's ability component (tail call `0x144C54670`, tag at `pawn+1968`). The rotary pawn's override (`0x53D64F0`) and airplane's (`0x53D6400`) call the same function and then one extra virtual on `pawn+2768` (rotary slot 227, airplane slot 228).
3. So: **running out of fuel (attribute reaching zero from above) stops the engine on the server**; the same state is what the fuel-leak and `VehicleOutOfFuel` events feed. `VehicleOutOfFuel` itself (`0x53DE5F0`, slot 317) stays a no-op base event with no Blueprint override in `B_TNK_01`, `B_SPW` or `B_FWG_01` (bytecode dumped this round, 0 hits for `OutOfFuel` / `HasFuel`).
4. Restart: `Server_StartEngine` (`0x53DE5D0`) -> slot 283 `0x53D4AE0` -> slot 302 `0x53D6070`. It refuses when the engine is already running (`+2185`), when slot 300 (`0x53CB360`) says no, or when flags at `+2168`/`+2169` are set or the object at `+2488` is valid. Slot 300 asks slot 316 (`0x76BB690` returns `pawn+3056`, `UWDVehicleGameplaySystemsComponent`) and calls its virtual `+1328` (slot 166); that body was not identified, so **whether a restart is blocked while the tank is empty is NATIVE (open)**. Evidence for the restart gate: disassembly only.

### R40-2 Smoke native timings `GetEffectiveSmokeTimings` (`0x869F010`). FOUND (disassembly)

The corpus failed on this function because `0x869F006` precedes it; `rdis.py 869F000` decodes it cleanly. It is a Blueprint thunk (`WDSmokeGrenadeVFXActor`) with three float inputs and three float outputs (SDK struct: inputs `TotalDurationSeconds`, `FadeInTimeSeconds`, `FadeOutTimeSeconds`; outputs the same three with `Out` prefix). With `offset` = the actor's `+0x36C` (set by `SetStartOffsetSeconds` `0x869F540`: `offset = max(arg, 0)`):

- `OutTotal = max(Total - offset, 0.1)` (constant 0.1 read at `0x9AD45A4`)
- `OutFadeIn = clamp(FadeIn - offset, 0, OutTotal)`
- `OutFadeOut = max(FadeOut, 0)`

`InitializeSmokeData` (`0x869F280`, args: transform component, `SmokeDelayTimeSeconds`, `OutTotalDuration`, `FadeOutTime` as the Blueprint wires them, statement 425 of `BP_SmokeGrenadeVFX`): stores `world time + OutTotal` at `+912` (end of the active volume), starts a timer for the smoke start after the delay (callback `0x869DAF0`, called at once when the delay is 0) and a destroy timer after `OutTotal + FadeOut` (callback `0x869E3D0`). So the smoke volume lasts `Total Duration`, then the plume fades for the fade-out time before the actor goes. A smoke grenade with `Total Duration` 120 (white, black) therefore fades out over a further 10 s (class default); signals with 180 or 64 likewise. A late-arriving client (start offset) loses that offset from the total and from the fade-in. The delay value is a Blueprint product (`CallFunc_Multiply_DoubleDouble_ReturnValue_1`), its inputs were not traced.

The smoke block bytes/floats on the vehicle countermeasure (V-6 of round 39: byte 1, floats 16.0 and 90.0, vector 0/400/200) are the item block of `FWDVehicleSmoke` in the targeting settings; their meanings are not named by the game and were not read natively (NATIVE, open).

### R40-3 Flare restock and lock-on interplay. NATIVE (open, further negative results)

Round 39's findings stand. New this round: the restock-related UFunction thunks all just forward (`Client_FlaresRestocked` `0x4DD6400` is a stub, `Server_RequestRefuelOrRepair` `0x85D5C80` forwards `(actor, station tag, speed)` to virtual slot 162 of the FOB component), the Blueprint dumps of `B_TNK_01`, `B_SPW`, `B_FWG_01` hold no flare logic, and the corpus has no function named for a seeker or lock-on consumer that reads `bFlaresActive` (`+0x791`) or the effective-range pair (`+0x2CC`/`+0x2D0`). Searched: token `+ 1937`, `+ 716`, `+ 720` in the corpus (no flare consumer), names `%Flare%`, `%Lock%`, `%Homing%`, `%Targeting%`, `%Missile%`. The homing setters that do exist are on the weapon owner (`SetHomingTarget` `0x6C2C600`, `ClearHomingTarget` `0x6C2B630`, `GetHomingTarget` `0x6C2B9A0`) and `CanFireWeaponWithLockOn` `0x6CA0FC0`; none was found reading flares.

### R40-4 Wheeled arcade controls `DA_ArcadeControls_*`. FOUND (cooked data)

Six `MWheeledVehicleArcadeDataAsset` assets (WHL_01, 02, 05 Humvee, 06 Dune Buggy, 07, 08); every stored field is in page section 1 and `vehicle-arcade-controls.json`. Highlights: Humvee and Wolf-110 are identical (understeer/oversteer recover 100, recover speeds 0 to 120, front/rear anti-roll 40, predict time 1.0, air pitch torque 400,000); the Kodiak/SUV adds drift assist (front 5, rear 60, recover up to 200); the Ural has drift ratios 2.5 / 30 and no anti-roll; the Dune Buggy has lean angle 15, pitch 20, anti-roll spring 1.0, predict time 3.5, airborne damping 1.5; WHL_01 has torque splitter 100, traction assist ratio 200 up to speed 50, anti-roll 100/100 with spring 1250, lean 50 and pitch 50. Which units the recover speeds use (km/h presumed) is not stated by the game.

### R40-5 Helicopter flight assist objects (rotary assist bodies). FOUND (cooked data)

[`DA_ROT_02_FlightCharacteristics`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/Data/DA_ROT_02_FlightCharacteristics.json), [`DA_ROT_03_FlightCharacteristicsDataAsset2000KGLight`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/Data/DA_ROT_03_FlightCharacteristicsDataAsset2000KGLight.json) and [`DA_ROT_04_FlightCharacteristicsDataAsset`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/Data/DA_ROT_04_FlightCharacteristicsDataAsset.json) (`BHRotaryFlightDataAsset`) each hold four controls (pitch, roll, yaw, collective) with an assist list (label, category `Core` / `Stability` / `AutoHover` / `EnvelopeLimits` / `TurnCoordination`, enabled flag, output mode, condition objects, body object). Page section 3 resolves every condition and body: for instance the Havoc climb-rate limit is a PID on world vertical velocity with target 36 km/h (P 0.111, D 0.167), enabled; "Limit sink rate" and "Stabilize released pitch when collective down" are present but disabled on the Havoc; roll and yaw drag-overshoot assists are disabled. 87 objects on ROT_02 alone. PID gain unit (radians against degrees) is the asset's own and not converted.

### R40-6 Tyre destruction. FOUND (cooked data); native sweep NATIVE (open)

Per wheel health trigger (all wheeled `DA_GameplaySystems_*`; WHL_06 shown, same shape elsewhere): at 55 percent wheel health the wheel gets a `WheelPop` cue, `WDWheeledVehicleWheelDragEffect` +1.5, `WDWheeledVehicleWheelFrictionEffect` -0.35, a steering/pull `WDWheeledVehicleEffect` of -0.125 (left) / +0.125 (right) and a braking modifier +0.05; the 0 percent threshold rows carry no effect objects. The wheel assets store intact tyre radius then two damaged radii (dune buggy 0.45, 0.345, 0.26 as round 39 noted). The native sweep-hit function `0x3A902D0`, the `GE_Vehicle_Health` consumer chain and `0x52311D0` callers were not reached (NATIVE, open).

### R40-7 Wheel tyre curves. FOUND (cooked data, partial)

Three `MWheeledVehicleTireModelSimpleDataAsset`s only (WHL_01, WHL_02, WHL_07): coefficients `Lnb Lnc Lnd Lne` and `Ltb Ltc Ltd Lte` plus force-against-slip preview curves. Page section 2 lists them with the peak of each curve (for example WHL_02 longitudinal peak magnitude 4645 at slip -1; WHL_07 2700 at slip -0.26). WHL_05, WHL_06 and WHL_08 name no tyre model asset. The reading of the letters as a Pacejka-style set comes from the names, not from code. Surface curves (per-surface grip) were not found in vehicle data: `DA_Vehicle_BrakingSurface_*` and `DA_Vehicle_Skidding_*` are audio maps (round 39 page note).

### R40-8 Vehicle-extension restock count. FOUND (cooked data + constructor)

Only the five stationary weapons restock (`bAllowsRestocking` true, inventory `Vehicle.AssociatedInventory.FOB`): STN_01 200 Munitions Supplies, STN_02 250 (`ResultingAmmoAmount` 500), STN_03 150, STN_05 900 Spare Parts Supplies plus 5,000 cash, STN_06 200 (`ResultingAmmoAmount` 60). The 24 vehicle weapons (WHL, TNK, ROT) do not restock from supplies (no field set). `ResultingAmmoAmount` unset on STN_01, STN_03 and STN_05 means the native default: constructor `0x76A8510` writes `1` at `+0x14C` and `1` at `+0x144` (disassembly confirmed this round). Whether the unit "1" means one magazine or one round for STN_01/03 is not shown.

### R40-9 Parachute from aircraft. ABSENT (vehicle data); NATIVE for the predicates

No vehicle asset mentions a parachute. The parachute lives on the character: `CanOpenParachute` (`0x52D14A0`) and `CanCutParachute` (`0x52D13A0`) are thunks into the character mover (they build `SyncStateCollection` / `AuxStateCollection` and call virtual `+1000`), `OnParachuteDeployed` (`0x5345610`) is a pawn event, and `UWDCharacterModifier_ParachuteCameraLock` handles the camera. Whether leaving an aircraft opens it is in the mover state code, not read.

### R40-10 Gear order. NATIVE (open)

Data observation only: the six-entry `GearRatios` list repeats the first ratio as its sixth entry on the Kodiak/Pickup (6.0 ... 6.0) and the Humvee (3.6 ... 3.6); the Ural's sixth (3.25) is not its first (5.62). A trailing reverse gear fits the repeat but no field names it (`bReverseAsBrake` exists at `+0x1BC` of another class). Not a confirmed meaning.

### R40-11 Native defaults for the `-` handling fields. NATIVE (partial)

Read this round: `UWDVehicleWeaponExtensionDataAsset` constructor (`0x76A8510`): `+0x144` = 1 (RestockSuppliesNeeded), `+0x14C` = 1 (ResultingAmmoAmount), `+0xB8` = 1.0 (float), `+0xC0` = 1, `+0xC4` = 4, `+0xC8` = 0.2 (`0x3E4CCCCD`), `+0xCC` = 2.5 (`0x40200000`), `+0x128` = 2.0, `+0x12C` = 0.5, `+0x130` = 0.5 (field names for these were not mapped). The wheeled `Characteristics`, `EngineData` and `Dynamics` constructors were not reached.

### R40-12 Not reached inside the timebox (NATIVE, open, nothing guessed)

Acceleration time (no stored value; inputs are the torque curve, gear ratios, mass and drag in the handling page); which of `EngineData` / `DynamicsData` drives a tracked vehicle and the torque/brake units; wheel-level values and mass units; the Refuel Max early-stop (the request forwards through `0x85D5C80` to FOB component slot 162, body not read); STN_05 geometry; damage-table operations and priority; vehicle input sub-objects (`DA_Input_*`); the `GE_Vehicle_Health` / `0x52311D0` callers and sweep hits `0x3A902D0`.

## Explosives and throwables

### R40-13 Claymore target rules. FOUND (Blueprint bytecode)

`B_Claymore` `CheckTargetConditions`: the overlapping pawn must carry the tag `State.Player.Vitality.Alive` and its `GetSpeedKPH` must be greater than 0.0 (a stationary target does not trigger). `CheckFaction` compares the faction tags of the placer and the target (`WDFactionComponent.GetFactionTag`). For vehicles the check reads `BHBaseVehiclePawn.GetCurrentDriver` and `BHVehicleSeatComponent.GetAllOccupants`, so a driver or passenger counts. A line trace (`LineTraceSingle`, debug draw 5.0 s) plus the sockets named `DamageQuerySocket*` on the target's mesh (`LineOfSightCheck`) decide whether the blast reaches; the explosion is `WDDamageSubsystem.SimulateRadialDamage` (150 damage, radius 300, effective 150). The trigger is the `TriggerBox` overlap event; a delay (`KismetSystemLibrary.Delay`, duration is a local variable, not extracted) precedes the blast. Destroying a Claymore awards `Meta.Progression.Resources.MatchScore.DestroyedDeployable`.

### R40-14 Placement conditions. FOUND (Blueprint bytecode)

`B_ClaymorePlacementCondition.IsSatisfied` and `B_AT_MinePlacementCondition.IsSatisfied` are identical: placement fails (warning `UI.Interactions.PlacementWarnings.InSafeZone`) when the placer has any of `State.Location.SafeZone.Alpha`, `.Bravo`, `.Charlie`, `.Hostile`. `B_PlaceableIED` uses the Claymore condition. No angle or slope test is in these classes; the "30-degree placement" the backlog mentions is not in these Blueprints (ABSENT here, may be in the native placement code, not read).

### R40-15 Mine data. FOUND (cooked data)

`B_AT_Mine`: damage 300, radius 750, effective 375, minimum 50, trace offset (0,0,50), `Z Offset` 20, `DetectFriendlyVehicles?` true, damage tag `Meta.Damage.Explosive.Utility.ATMine`. `B_ThrowableC4`: fuse after trigger 0.2 s, health 30, max detonation distance 100, damage 250, radius 600, effective 250, minimum 20, impulse 4000 / Z 2750, `bExplodeOnHealthDepleted` false. Native constructor values (`AWDExplosive` base) and the mine's after-blast behaviour were not read (NATIVE, open).

### R40-16 `TestGrenadeLauncher`, 40 mm underbarrel data. FOUND (cooked data)

`Id.Item.TestGrenadeLauncher` (display "TEST Grenade Launcher") is a real shipped item, in [`GrenadeLauncher.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/GrenadeLauncher.json) (plugin [`UnderbarrelGrenadeLauncher`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/UnderbarrelGrenadeLauncher.json)), the UI items table [`DT_EntityData_UI_Items`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Entities/DT_EntityData_UI_Items.json) and `DefaultGameplayTags.ini`. Stats ([`DA_GrenadeLauncher_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/DA_GrenadeLauncher_Stats.json)): 75 rounds per minute, semi-automatic, burst 1, muzzle speed 7,600, effective range 300, caliber `Item.Caliber.40mm`, one `Id.Item.40mm` per shot. [`DA_40mm_ProjectileData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/40mm/DA_40mm_ProjectileData.json): base damage 100, explosive radius 1,000, effective radius 250, falloff 1.0, blunt damage 80, impulse 750, mass 0.23, diameter 4.0, drag model 0.8 (`GC (Cylinder)`), arming delay 0.07 s, cue `GameplayCue.Weapon.RocketProjectile`. The existing page is [UnderbarrelGrenadeLauncher feature](../../game-features/Wardogs_GameFeatures_UnderbarrelGrenadeLauncher_v2.md).

### R40-17 Smoke volume pawn list. NATIVE (partial)

`UpdatePawnsInSmoke` (`0x869F600`) walks the actor's pawn array (`+856`, count `+864`), for each valid pawn calls virtual slot 231 (`+1848`) to get a component, copies its transform (`+528..+592`) and radii (`+608`, scaled by floats at `+1392` / `+1396` of that component) and passes them to `0x14869D740` together with the smoke point list (`+744`). It is the place smoke relates to pawns; what `0x14869D740` does with them (a per-pawn "in smoke" flag or a visibility test) was not read.

### R40-18 Not reached inside the timebox (NATIVE, open, nothing guessed)

Fire end at 45 s versus the ubergraph timer; burning removal; fire-field instigator; downstream friendly-fire rules; Molotov/Claymore/C4 native constructor values; mine after-blast; throw-velocity curve combination; `MinimumRemaining` field; [`CT_Weapon_Spread`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Curves/CT_Weapon_Spread.json); armoured targets.

## Wiki updates

- `_wiki/vehicles/` fuel pages (`fuel-and-refueling.md` line 31, `vehicle-guide.md` lines 120/121): empty tank "not yet known" -> "When a vehicle's fuel reaches zero the server stops its engine. Whether the engine can be restarted before refuelling is not yet known." Keep the fuel-leak sentence from round 39.
- `_wiki/equipment/m18-smoke-grenade.md`, `m18-signal-grenade.md`, `fire-smoke-and-flash.md`: smoke timing "not known" -> "Smoke stays for its Total Duration (white and black 120 s, blue signal 64 s, other signals 180 s, vehicle smoke screen 6 s), then the plume fades for the fade-out time (10 s for the grenades, 2 s for the vehicle screen) before it is removed. A smoke effect that is already running when you arrive loses that elapsed time from its duration."
- `_wiki/vehicles/` handling pages (Kodiak, Humvee, Dune Buggy, Ural, Wolf-110, Pickup; `vehicle-handling.md` if present): add a short "Driving assists" line pointing to the new data page values: Humvee and Wolf-110 identical (anti-roll 40, recover full speed 120), Kodiak drift assist (front 5, rear 60), Dune Buggy lean 15 degrees and pitch 20 degrees, Ural drift 2.5 / 30; "arcade assists not summarized" -> link the new page. Tyre model: Kodiak/Pickup, Ural and WHL_01 have a stored tyre model; the others do not.
- `_wiki/vehicles/` helicopter pages (Havoc, MH-6/AH-6, Z20 Lakota) and `_wiki/guides/vehicle-guide.md`: add the assist facts: climb-rate limit 36 km/h PID on all three, auto-hover when collective is neutral, level-at-low-speed on pitch and roll, ground resets ("Set to -1 on ground" collective, "Set to 0 on ground" pitch/roll), and that some assists are shipped disabled (Havoc: limit sink rate, yaw ground reset, roll drag-overshoot, roll damping).
- `_wiki/vehicles/` wheeled damage text ("flat tyre"): at 55 percent wheel health a tyre pops, adds wheel drag (+1.5), cuts grip (-0.35 friction), pulls the steering toward the damaged side (0.125) and adds 0.05 braking.
- `_wiki/vehicles/stationary-weapons` / STN pages: restock numbers (MG nest: 200 Munitions Supplies for 60 rounds; STN_02 250 for 500 rounds; STN_03 150 and STN_01 200 Munitions Supplies, rounds per restock not stored (default 1); Stingray 900 Spare Parts Supplies and 5,000 cash for one drone). Wheeled, tracked and rotary vehicle weapons do not restock this way.
- `_wiki/equipment/claymore.md`: "target tag not known" -> "A Claymore fires at a living enemy who is moving (speed above 0) inside its trigger zone, including vehicle drivers and passengers; a motionless target does not set it off. The blast must reach the target through the line-of-sight sockets." Placement: "cannot be placed in a safe zone (Alpha, Bravo, Charlie or the hostile safe zone)"; the same for the AT mine and the placeable IED. Remove or mark unverified any "30 degree" placement claim.
- `_wiki/equipment/at-mine.md`: add placement restriction (no safe zones) and `Z Offset` 20, `DetectFriendlyVehicles` true; `_wiki/equipment/c4.md`: 0.2 s detonation timer, 30 health, 100 max detonation distance.
- `_wiki/weapons/` underbarrel grenade launcher article (name in the wiki for `TestGrenadeLauncher`): 75 rounds/min, semi-automatic, muzzle speed 7,600, range 300, 40 mm round 100 damage, 10 m outer / 2.5 m effective radius, 80 blunt damage, arms after 0.07 s; item id `TestGrenadeLauncher` (internal name; shipped in the data).
- `_wiki/vehicles/countermeasures-and-flares.md`: no change from round 39; restock and lock-on stay "not yet known" (nothing new found).
- `_wiki/vehicles/` parachute mentions for aircraft: "no vehicle parachute exists in the data; the parachute belongs to the on-foot character".
