---
title: "Round 36 combat: refuel and repair, buildables, stationary weapons, flares, Ghillie, Molotov, smoke, artillery HUD"
parent: "Evidence"
nav_exclude: true
---

# Round 36 combat

GitHub-only evidence page (docs/ is excluded from the site), so asset names and RVAs are fine here.

Method: cooked data read from `data/` and from fresh `WdExtract` dumps (`dump`, `list`, `findname`; output under `E:/Reverse_Engineer/wardogs_analysis/round36_combat/`), Blueprint bytecode rendered with `tools/cue4parse_extractor/kismet_listing.py`, and static reading of the decompiled corpus (`corpus.sqlite`, RVAs for CL-516586). No devirtualization, nothing run. The numbers that can be re-derived from `data/` are reproduced by `python -I _tools/round36_combat.py --check`.

| # | Gap | Status |
|---|---|---|
| 1 | Refuel and repair rates, 13.33 multiplier, zero fuel | FOUND (station and canister rates, multiplier meaning); NATIVE (supply conversion, zero-fuel effect) |
| 2 | Build time, Cost to supplies, hits to destroy | NATIVE (build arithmetic, partly traced); hits to destroy DERIVED |
| 3 | MG Nest 3,000 vs 1,800 HP | FOUND (data) with one native caveat |
| 4 | Stingray reload | FOUND (it is a restock, not a reload) |
| 5 | Flares | FOUND (counts, ranges, time); NATIVE (restock, cooldown, lock-on effect) |
| 6 | Ghillie suit and headwear | FOUND (a Gameplay Effect nobody had read) |
| 7 | Molotov | FOUND (patch box, armor, friendly rows); NATIVE (impact vs fuse) |
| 8 | Smoke | FOUND (single consumer is aim assist); AI sight not determined |
| 9 | SPH-2 dial vs table | FOUND (HUD binding and label rules) |
| 10 | Mortar minimum range | FOUND (data limit differs from the community stop); DERIVED |

## 1. Refuel and repair rates

**Status: FOUND (rates), NATIVE (supply conversion, zero fuel). Evidence: cooked data read; Blueprint bytecode read; static disassembly of selected functions.**

### 1a. Refuel Station and Repair Station

`B_BuildableRefuelStation` / `B_RefuelStation` hold no logic (components only: `WDTrackedByFobComponent`, `WDBuildableTrackerComponent`). The station numbers live in the FOB refuel and repair scene asset, `Items/Buildables/Content/Data/UI/FobRefuelRepair/DA_Scene_FobRefuelRepair` (`WDUIFobRefuelRepairData`, `StationData`, struct `FStationData` / `FRestockData`):

| Station | Button | `MaxAmount` (fraction of the tank or health pool) | `Cost` (cash) | `RestockTime` (s) | Supply item | `ItemCostPerSingleRestock` |
|---|---|---:|---:|---:|---|---:|
| Refuel | Fast | 0.05 | 75 | 3.0 | `Id.Item.FuelSupplies` | 5 |
| Refuel | Max | 1.0 | 1,500 | 9.0 | `Id.Item.FuelSupplies` | 5 |
| Repair | Fast | 0.05 | 100 | 3.0 | `Id.Item.SparePartsSupplies` (Mechanical Supplies) | 5 |
| Repair | Max | 1.0 | 2,000 | 9.0 | `Id.Item.SparePartsSupplies` | 5 |

Reading: a Fast restock is 5% of the pool in 3 s for 75 (refuel) or 100 (repair) cash, a Max restock is up to 100% in 9 s for 1,500 or 2,000 cash. The cash is 5% of the Max price (75 = 5% of 1,500, 100 = 5% of 2,000), which is what the field names (`MaxAmount`, `Cost`) suggest. The request goes through `WDPawnBuildableManager::Server_RequestRefuelOrRepair(Fob, StationTag, EFobRestockSpeed)`; the runtime record is `FWDFobTakingResourceData` (`ItemCostPerRestock`, `MoneyCost`, `RelativeRestockAmount`, `RestockTime`). The sale appears to pay the FOB owner (inferred from `WDFobStationPayOwner.MoneySpent` and the session event `ST_Challenges_SessionEvents_Buildable_FOBOwnerPayed`). **Not read:** how `ItemCostPerSingleRestock` 5 scales with `RelativeRestockAmount` (native), and whether a Max restock takes 9 s regardless of how empty the vehicle is (the 9.0 is the stored time; scaling by missing amount is not shown). The FOB component only wires the scene: `WDForwardOperatingBaseComponent::TryOpenFOBRefuelRepair` (`0x8611C70`), `TimeBetweenVehicleSupplyTicks` 0.5 s and `MinHpPercentageToBeActive` 90.0 are native constructor defaults (`0x85E7010`: stores `0x3F000000` at `+0x244`, `0x42B40000` at `+0x190`); `FuelConsumptionRate` (`+0x21C`) is zero-initialised. The 0.5 s tick drives the vehicle-side supply display refresh (`0x8613040` -> `0x86262A0`), not a refuel.

### 1b. Fuel Canister

The canister item (`ID_FuelCan_40L`, `ContainerData`) holds `MaxAmount` 40, `UpdateTime` 0.75 s, `UpdateAmount` 2.0. `B_Action_FuelCan_Refuel` (bytecode, `HandleApplication`): each timed application calls `ModifyBase(UpdateAmount)` on the vehicle's `Attribute.Gameplay.Fuel` (clamped by the capacity attribute), removes the amount actually added from the canister (`Attribute.Gameplay.Appliable.Amount`, written through `SetBase`), and broadcasts `S_OnRefuelReward`. The loop repeats until the canister is empty or the target is full (`UntilItemEmptyOrTargetFull`). Derived rates: 2.0 per 0.75 s = 2.67 units per second, an empty-to-full 40 L canister in 15 s (20 applications); the 20 L item (`ID_FuelCan_20L`) is slower: 1.0 per 1.5 s = 0.67 per second, 30 s. Whether the vehicle's fuel attribute is in litres is not stated (the canister is labelled litres in the UI strings).

`B_Action_FuelCan_ReFill` (filling the canister from a world refuel point, `WDItemRefuelComponent` actors under `WorldInteractable/.../ItemRefuelPoints`): per update it adds `min(RefuelPerUpdate, missing)` to the canister and charges the player `RefuelPerUpdate * PricePerLiter` cash (skipped in safe zones when the source is flagged `bFreeInSpawn`). The total interaction time is `(amountToFull / max(RefuelPerUpdate, 0.01) + 1) * UpdateTime` (`RefuelStationUpdateTime`). `RefuelPerUpdate`, `PricePerLiter` and `CurrentFuel` are per-pump fields of `FWDFuelSourceCounter` (set on the placed pump actors, not read here). This answers "where the fuel comes from": a world refuel point, paid in cash; the FOB Refuel Station does not fill canisters.

### 1c. The stored 13.33 multiplier

`RepairSpeedMultiplier` is a field of every `WDBuildableDataAsset` (`+0x64`), not a vehicle-repair rate: 32 buildable assets have it. Values equal `Cost / 15` on 21 of the 32 (Refuel Station 200 -> 13.33, Repair Station 200 -> 13.33, Radio 20 -> 1.33, Tank Trap 22 -> 1.47, Quad Wall 75 -> 5.0). The multi-stage parents and the larger weapons deviate (Bunker 200 -> 6.67, Door 80 -> 2.0, Gate 200 -> 5.67, Talon 650 -> 66.67, STN_02 1200 -> 100, STN_03 600 -> 10). So the number is a per-structure design value for how fast a hammer repairs or builds that structure, and the Refuel and Repair Station's 13.33 says nothing about vehicle refuelling or repair. Native evidence (inferred): in `sub_1485F1F20` (called from the single-hit construct path `Server_SingleHitMode_Construct` -> `0x86032F0` -> `0x85EAAA0` -> `0x85F1D90` -> `0x85F1F20`) the hit amount is multiplied by `*(float*)(object + 0x64)` when a buildable-interface bool (`0x8578A80`) is true; `+0x64` is the offset of `RepairSpeedMultiplier` in the SDK. Which condition the bool is (finished, damaged, repairing) is not decoded.

### 1d. Hand repair

Wrench and drills: +5 HP per use is already on the wiki. The timing is `UpdateTime`/`UpdateAmount` style data on those items and was not re-read in this round.

### 1e. Zero fuel

**Status: NATIVE, effect not recovered.** `ABHBaseVehiclePawn::VehicleOutOfFuel` exists (reflection thunk `0x53DE5F0` -> virtual slot 317); the base implementation is the shared no-op `0x1562FE0`; `AWDRotaryVehicle` overrides it at `0x76B8A70`, which ends in a `JUMPOUT` into the protected region (not followed). Related data: analytics event `WDAnalyticsEvent_VehicleOutOfFuel`, message `WDVehicleOutOfFuelMessage {PlayerState, VehicleTag}`, and the loading tip about turning the engine off in the artillery tank "to avoid draining fuel needlessly". The consequence (engine stop, no restart) is the natural reading but is not shown by any value or readable function. Not published as fact.

## 2. Buildables: build time, Cost to supplies, hits to destroy

**Status: NATIVE (partly traced), hits to destroy DERIVED. Evidence: cooked data plus static disassembly.**

- Hammer data (already on the page): `BuildAmount` 0.5/1/1.5, critical-spot `BuildAmountWhenTargetIsHit` 3/5/8, dismantle 150/200/250 per hit and per second. `UWDItemExtensionData_BuildBuildable` carries `BuildAmount` and `BuildAmountPerSecond` (native default 3.0 and 3.0), so a continuous-mode path exists (`UWDBuildingMode_Continuous`, `Server_ContinuousMode_Construct`) besides the single-hit mode.
- Cost to supplies: in the single-hit path the amount handed to the supply helper is `round(hit amount)`: `sub_1485F1F20` computes `v14 = -((int)(-0.5 - 2*a) >> 1)` with `a = hitAmount` (times the `+0x64` multiplier when the bool above is set), clamps it by what the structure still needs (`sub_1485FA930`) and by the available supplies, and returns the integer amount and a float progress. The progress per supply unit is therefore native and needs the stage total (`Cost` is the total supplies for the structure, stage progress is 0..1); no build time per structure can be stated. Do not publish a seconds-per-structure number.
- Hits to destroy (**Derived**, point blank, full base damage, no falloff, no armor-like rules): `ceil(MaxHealth / (base * (1 + factor)))`, where `factor` is the per-source percentage already tabulated on the Buildables page (`Meta.Damage.Buildable.*` rows) and `base` is M4 5.56 FMJ 28, M67 frag 100, 120 mm tank rocket 150 (`Explosive.Rocket.120mm`), C4 250. Counts for a selection (the full set is printed by `_tools/round36_combat.py`):

| Structure | HP | M4 5.56 FMJ | M67 frag | 120 mm rocket | C4 |
|---|---:|---:|---:|---:|---:|
| Barbed Wire | 250 | 60 | 3 | 1 | 1 |
| Sandbag Wall / Wood base | 735 | 175 | 8 | 1 | 1 |
| Hesco (HBlock) | 1,600 | 286 | 11 | 5 | 2 |
| Door | 2,200 | 524 | 22 | 2 | 3 |
| Tall Hesco / Shelter | 2,250 | 402 | 15 | 9 | 4 |
| Tank Trap | 4,500 | 1,072 | 90 | 6 | 3 |
| Bunker / Recon Tower / Indirect Fire Shelter | 5,000 | 893 | 100 | 23 | 14 |
| Gate | 5,320 | 1,267 | 54 | 4 | 2 |
| Bremer Wall | 6,500 | 1,161 | 44 | 13 | 7 |
| Refuel / Repair Station | 1,600 | 286 | 11 | 2 | 2 |
| FOB | 15,000 | 2,679 | 50 | 7 | 5 |

The Refuel and Repair Station rows come from the page's factors (rocket +1500%, C4 +600%); the table is a bound under the assumptions above, not an observed hit count.

## 3. MG Nest health

**Status: FOUND (data), native caveat. Evidence: cooked data read.**

The MG Nest is a stationary vehicle (`STN_06`) built through a buildable plot. Health values in the data: vehicle `DA_GameplaySystems_STN_06.InitialVehicleHealth` 1,800 and `VP_STN_06` `MaxHealth` 1,800; buildable `DA_Buildable_MGNest.MaxHealth` 3,000. For the other five stationary weapons both are equal (Talon 3,000, STN_02 5,000, STN_03 3,000, STN_04 1,000, STN_05 3,000). The completed gun is the vehicle actor, and the vehicle damage pipeline counts against the vehicle's own health pool (1,800); `B_Buildable_StationaryVehicle` (the plot actor that exists while building) has a `WDVitalityComponent` and `WDBuildableComponent` with no property overrides, so it takes `MaxHealth` from the buildable asset (3,000). So 3,000 is the plot's health while it is being built, 1,800 is the finished gun's. **Not proven:** the native `WDVehicleBuildableComponent` (reads `SoftBuildableData`, `OnVehicleDamageEventStarted` `0x85D57C0`) could copy the buildable health onto the vehicle at completion; no data asset or readable function does so, but the function bodies were not fully decoded.

## 4. Stingray reload

**Status: FOUND. Evidence: cooked data read; native constructor default read.**

The Stingray (`STN_05`) is not a reloaded gun. `WE_STN_05_Heavy_MainBarrel`: `ReloadSetupData` `Standard`, `ReloadTime` 0.0, `StartDelayTime` 1.0, `EndDelayTime` 1.0 (the other stationary weapons: STN_01 5.0, STN_02 3.0, STN_03 4.5, STN_06 8.0, all with 1.0 and 1.0), starting inventory `Id.Item.DroneProjectile` 0. The ammunition path is a restock: `bAllowsRestocking` true, `RestockSuppliesTag` `Id.Item.SparePartsSupplies` (Mechanical Supplies, not Ammo Supplies), `RestockSuppliesNeeded` 900, the unnamed field `_aaabbaggelnmdnpaealoj` (read by `GetAmountOfRestockCashNeeded`) 5,000 cash, `RestockInventoryTag` `Vehicle.AssociatedInventory.FOB`. The result of one restock, `ResultingAmmoAmount`, is not serialized on this asset, so it keeps the native default of `UWDVehicleWeaponExtensionDataAsset` (constructor `0x76A8510`: the dword at `+0x14C` is 1, with `+0x144` RestockSuppliesNeeded 1 and `+0x148` cash 0 defaults). One restock therefore gives one drone. The player-facing flow is the drone reload scene (`DA_Scene_DroneReload`, button text "PURCHASE STINGRAY", labels "SPARE PARTS" and "CASH", "DEPLOYING..." progress bar driven by `HandleProgressBarAnimation(TotalTime)`). The scene's duration value is native. The MG Nest restocks 60 rounds for 200 Munitions Supplies (`ResultingAmmoAmount` 60 in the data); STN_02 gives 500 for 250; STN_03 and STN_01 do not serialize it.

Also found: the Stingray is a lock-on weapon. `TargetingSetup`: air vehicles only (`AllowedTargets` Little Bird variants, FWG airplane, Havoc, ROT_01), `bOnlyFireWhenLockedOn` true, `TimeToTarget` 2.0 s, `FireDelayAfterLock` 0.5 s, `TargetingDistance.Max` 100000. The Talon (`STN_01`) has the same `TimeToTarget` 2.0, `FireDelayAfterLock` 0.5 and the handheld `Launcher_04` 2.0 / 0.25 (`TargetingDistance.Max` 120000).

## 5. Flares

**Status: FOUND (per-vehicle data), NATIVE (restock, cooldown, lock-on effect). Evidence: cooked data read; native structure layout.**

`FWDFlaresSettings` per vehicle (`DA_*GameplaySystems*`):

| Vehicle | Internal | Starting flares | Active time (s) | Effective range min / max (m) |
|---|---|---:|---:|---|
| Fixed-wing airplane | FWG_01 | 3 | 3.5 | not set |
| Havoc | ROT_02 | 2 | 3.5 | 5 / 300 |
| MH-6, AH-6M, AH-6R | ROT_03 (all variants) | 2 | 3.5 | 10 / 300 |
| Z20 Lakota (all variants) | ROT_04 | 2 | 3.5 | 15 / 300 |

(Internal names from the `Internal name` row of each vehicle page: Havoc ROT_02, MH-6 and AH-6 ROT_03, Z20 Lakota ROT_04.) The struct also holds `FlaresCooldownTime`, left/right flare target offsets and a gameplay cue. None of the shipped values set `FlaresCooldownTime`. Runtime state on `WDVehicleGameplaySystemsComponent`: `CurrentFlaresAmount` (replicated), `bFlaresActive`, `bFireFlareCooldownReached`, `Client_FlaresRestocked`, `Server_FireFlares` (impl `0x766EDF0`: sets `bFlaresActive`, records the server time and the activation location, applies the cue). Whether and when flares are restocked, the cooldown length, and how a lock-on weapon treats an active flare (the min/max "effective range" reads like the distance band in which a flare can decoy a projectile) are in native code that was not recovered: the lock-on consumers named in the SDK (`TargetingSetup`, `IsLockedOnTo` cues) have no flag, tag or data row mentioning flares. The in-game tip says flares "momentarily prevent heat-seeking projectiles from locking". Smoke (a separate vehicle countermeasure) has no data link to lock-on either (section 8).

## 6. Ghillie suit and headwear

**Status: FOUND. Evidence: cooked data read (`assets/data/ge-values.json`, `GE_Player_GhilliEffects`).**

The armor item `ID_GhillieArmor` applies `GE_Player_Ghilli_Armor` (grants `State.Player.Ghilli.BodySuit`) and `GE_Player_GhilliEffects`; the helmet applies `GE_Player_Ghilli_Helmet` (grants `State.Player.Ghilli.Headwear`, removal requirement ignores `State.Player.Vitality.Dead`). `GE_Player_GhilliEffects` requires both tags, so it only applies when the suit and the headwear are worn together, and its modifiers (all `MultiplyCompound`) are:

| Attribute | Multiplier |
|---|---:|
| `AdsTimeMultiplier` | 0.80 (aim down sights 20% faster) |
| `AimSwayScaleMultiplier` | 1.15 (15% more aim sway) |
| `LeanTimeMultiplier` | 1.15 |
| `UnleanTimeMultiplier` | 1.15 |
| `MaxSpeedMultiplier` | 0.95 (5% slower) |
| `JumpVelocityMultiplier` | 0.95 |

Detection, spotting and AI: a `findname` search of every cooked package finds the tags `State.Player.Ghilli.*` only inside these three effects (`fn1/findname.txt`), so no data asset reads them. The cooked effects on detection are the ones already documented: infrared range finder exclusion (`ID_RangeFinder_Expensive` `CharacterGearsToIgnore`) and the killcam rule (`DA_CharacterModifierState_*Critical`, no death cam after the wearer kills). The AI detectability component (`round36-ai`) has stance values only and no camouflage term. Damage: the items have no `CoveredHitLocations`, so the armor-coverage rule cannot select them; `DT_GlobalDamage_ArmorData` has rows `Meta.Damage.Armor.Ghillie` and `Meta.Damage.Helmet.Ghillie` (six entries each, `Percentage_Ongoing -100`) and an entry in the generic armor row with target requirement `Meta.Damage.Armor.Ghillie` (`-10000`) and in the helmet row with `Meta.Damage.Helmet.Ghillie` (`-1000`). What those rows do to the wearer is not shown by any consumer; the wiki's "no damage reduction" stays the safe statement.

## 7. Molotov

**Status: FOUND (patch size, armor, friendly rows), NATIVE (impact vs fuse). Evidence: Blueprint dump, cooked data read, static disassembly.**

- Patch size: `B_Molotov_TriggerVolume` has a `BoxComponent` with `BoxExtent` 100 x 100 x 25 (cm, half extents), so each trigger box is 200 x 200 x 50 cm (2 m x 2 m x 0.5 m), overlapping `Pawn` only. 15 patches per throw (Blueprint value, native default 12), life 45 s. Whether one trigger volume is made per patch is stated by the creation function (`0x86A15B0`) but the spacing and total spread are native and not decoded; do not publish a total fire radius.
- Impact vs fuse: `B_Molotov` has only a flight-sound `ReceiveBeginPlay` (bytecode); it does not override the fuse (5.0 s, `bCanBeCooked` false). `AWDExplosive::CollisionExplodeImpactThreshold` (`+0x498`) is 0.0 in the constructor (`0x6CA7800`) and no Blueprint sets it; no read of `+0x498` was found outside constructors, so no impact-detonation path was located. Only the fuse path is confirmed (round 23: `StartFuseTimer` -> explode). It also explodes when its 50 starting health is depleted (`bExplodeOnHealthDepleted` true). **Status: fuse confirmed, impact trigger not found (NATIVE).**
- Armor: the fire damage is `Meta.Damage.DamageType.Enviroment`. No row in `DT_GlobalDamage_ArmorData`, `_InfantryData` or `_VehicleData` has that source requirement, so none of the armor rows applies to the fire tick (**Derived** from the tables; armor rows match Bullet, Explosive and Melee). The detonation burst (`Meta.Damage.Explosive.Utility.Molotov`) matches the Explosive armor rows (-85%) and `DT_GlobalDamage_InfantryData` adds -30% against `Meta.Damage.Armor.SuperHeavy`.
- Teammates: `DT_GlobalDamage_InfantryData` has `AlignmentRequired = Friendly` entries only for Bullet (-50%) and Large Hammer (-70%). The Molotov burst and the fire tick have no friendly entry, and the fire field loop has no team check (round 20). **Derived:** the tables do not reduce a teammate's Molotov damage; whether the mode disables friendly damage elsewhere (team-kill tracking exists) is not in these tables.
- How burning ends: already on the page (leave the patch; the 45 s life of the volume).

## 8. Smoke

**Status: FOUND (consumers). Evidence: `corpus.sqlite` call search, round 26 notes re-checked.**

The only caller of the sight-blocker query `UWDSightBlockerSubsystem` (`0x6F4E2D0`) is `0x6D820B0` (site `0x6D821E1`), the aim-assist target manager. Producers are the grenade smoke volume and the vehicle smoke trail. No call from the AI perception, spotting, minimap, damage, hit-registration or lock-on code. No smoke Gameplay Effect or tag exists. So the cooked game uses smoke to block aim assist and the visual; nothing found makes smoke block spotting, lock-on or thermal (there is no thermal sight in the data). **Not determined:** whether engine AI sight traces (`AISense_Sight`, sight 2,000 m per round 36 AI) are blocked by the smoke geometry; the smoke cloud is built from client-side traces and has no server-side volume (round 26), so a dedicated server cannot see it at all.

## 9. SPH-2 dial against the game table

**Status: FOUND. Evidence: Blueprint bytecode of `W_Artillery_Reticle` (TNK_01) and `W_STN_03_Reticle` (STN_03) dumped and read.**

The MIL scale widget binds to `VehicleCrosshairViewModel.WeaponPitchBindable` (a float in degrees; handler `OnTurretPitchUpdated`) and converts it: `PitchMilliradians = DegreesToRadians(pitch) * 1000`, a true milliradian. The writer of `WeaponPitchBindable` is native and was not located, so the zero of that angle (hull, horizon or rest angle) is not read; the weapon limits are in `W_TNK_01_Artillery` (`MinWeaponPitchAngle` 2.0, `MaxWeaponPitchAngle` 80.0 degrees = 34.9 to 1396 mrad).

SPH-2 widget (`W_Artillery_Reticle`):
- the scale spans from the first to the last `Milliradians` of `WeaponData->ArtilleryRangeData` (first row 20 mrad, last 1400), one tick per mil, a label "{Mil} mils" every 10 mils equal to the true mrad value;
- the distance label on each tick is not the stored `ImpactDistance`: `UpdateDistanceText` calls `WDArtilleryRangeLibrary::SimulateImpactDistance(ProjectileStats, WeaponStats, mil, AltitudeAboveSeaLevel, AirDensity 1.2)` and prints `{Distance}m` (the 155 mm Expensive projectile for the initial build);
- neither `ImpactDistance` nor `TravelTime` of the table is read by this widget (zero references in the bytecode); only the `Milliradians` column is used, for the span and the pointer interpolation (the pointer is placed at `index + (pitch - mil[i]) / (mil[i+1] - mil[i])`, scrolled by +1.37 items for alignment).

So for the SPH-2 the stored `ImpactDistance` column is not what the player reads: the HUD range scale is a live simulation with altitude. That explains why the table and the community dial differ and why the difference is not a fixed shift (+45 to +97 mrad on the low arc, -2 to -34 on the high arc); the table is a pre-computed set that the sight does not use for labels.

Mortar widget (`W_STN_03_Reticle`): it reads the table directly. The mil label is `Array_Get(RangeData, i).Milliradians + 650.0` (hard-coded constant in `PopulateViews`, label "{Mils}") and the distance label is the stored `ImpactDistance` ("{Distance}m"). That is why the community dial is the table plus exactly 650. The pointer uses the true pitch against the unshifted table mrad (`UpdateTimeAndDistanceScale` identical in form to the SPH-2's). So `ArtilleryRangeData` is used by the HUD (mortar fully, SPH-2 only for the mil span); no AI reader was found (the AI team's firing logic is outside this round). The Stingray has no reticle widget with a table (it is a lock-on weapon).

## 10. Mortar minimum range

**Status: DERIVED, with a conflict with the community stop. Evidence: cooked data read.**

`W_STN_03_MainBarrel` limits the barrel to `bLimitWeaponPitch` true, `MinWeaponPitchAngle` -29.0 and `MaxWeaponPitchAngle` 15.0 degrees = -506.1 to +261.8 mrad. The table rows reach 300 mrad (80 m), so the 300 mrad row (dial 950) is beyond the barrel's limit, but the 250 mrad row (dial 900, 110 m) is inside it. The community's dial stop at 850 mils (200 mrad, 132 m) is 61.8 mrad below the data limit (261.8 mrad = dial 911.8). Linear interpolation of the table at 261.8 mrad gives about 102.9 m (the HUD uses the same linear interpolation for the pointer; the physical impact is not the table), so the data allows firing shorter than 132 m, down to about 103 m. The community stop at 850 is not explained by any limit in this asset; another limit may apply (seat or camera pitch, or the stop being a measurement limit). Treat 132 m as the shortest range the community measured and about 103 m as the shortest the weapon data would allow.

## Wiki updates

Do not edit `_wiki/` in this round. Changes for the writer round (`wiki file -> change`):

- `_wiki/vehicles/fuel-and-refueling.md`: "Refuel rate: Not yet known" and the closing "refuel rate ... not yet known" -> Refuel Station Fast: 5% of the tank in 3 s for 75 cash and 5 Fuel Supplies; Max: up to 100% in 9 s for 1,500 cash and 5 Fuel Supplies. Canister: 2.0 per 0.75 s (2.67 per second, 15 s for 40 L; 20 L item 1.0 per 1.5 s). Fuel Canister fill happens at world refuel points for cash (see fuel-canister). Zero fuel stays "not shown by the data".
- `_wiki/vehicles/repair-and-vehicle-parts.md`: table row "Refuel and Repair Stations ... Not yet known" -> Repair Station Fast: 5% in 3 s for 100 cash and 5 Mechanical Supplies; Max: up to 100% in 9 s for 2,000 cash and 5 Mechanical Supplies. Replace "Its repair multiplier is stored as 13.33, but the data does not say what that multiplier does" with: the 13.33 is the structure's own hammer-repair speed multiplier (every buildable has one, mostly Cost divided by 15) and is not a vehicle repair rate.
- `_wiki/equipment/refuel-and-repair-stations.md` (if present) and `_wiki/equipment/buildables.md` line 165: "Their refuel and repair rates are not yet known" -> the table above. Also buildables.md line 146/44 hammers: build time per structure stays "not known" (native), but add the derived hits-to-destroy table for the common sources, labelled derived.
- `_wiki/equipment/fuel-canister.md`: "where the fuel comes from ... not yet known" -> world refuel points (pumps) for cash; add the 2.0 per 0.75 s rate and the slower 20 L item.
- `_wiki/equipment/mg-nest.md` Health: "Which of the two decides ... not confirmed" -> the finished gun is the STN_06 vehicle with 1,800 HP; 3,000 is the buildable plot's value (data; one native caveat).
- `_wiki/equipment/stingray.md`: Reload "Not yet known" -> no reload step (0.0 s plus 1.0 s start and end delay); the drone is bought by restock: 900 Mechanical (Spare Parts) Supplies and 5,000 cash for one drone. Correct "900 Ammo Supplies" to Mechanical Supplies. Add that it is a lock-on weapon: air targets only, fires 0.5 s after lock (2.0 s to target).
- `_wiki/vehicles/countermeasures-and-flares.md`: "no per-vehicle starting count" -> airplane 3, Havoc 2, MH-6 and AH-6 2, Z20 Lakota 2, each active 3.5 s; effective range bands 5-300 m (Havoc), 10-300 m (MH-6, AH-6), 15-300 m (Z20). Restock and lock-on effect stay "not shown".
- `_wiki/equipment/talon-9k-sam.md`: add the lock timings (2.0 s to target, 0.5 s fire delay after lock) and that flares have no data link to it.
- `_wiki/equipment/ghillie-body-suit.md` and `ghillie-headwear.md`: add the effect when both are worn: ADS 20% faster, aim sway +15%, lean and unlean 15% slower, move speed -5%, jump -5%. Keep "no damage reduction in the item data".
- `_wiki/equipment/molotov.md` and `fire-smoke-and-flash.md`: each fire patch is a 2 m x 2 m x 0.5 m box, 15 patches, 45 s; armor does not appear in any rule for the fire tick; teammate fire has no reduction row (derived); the burst is on the 5.0 s fuse (no impact trigger found).
- `_wiki/equipment/fire-smoke-and-flash.md` smoke: "What the cloud blocks ... not yet known" -> the only code that consults the smoke is the aim assist; spotting, lock-on and (so far found) AI are not affected; AI sight not determined.
- `_wiki/game-mechanics/artillery.md` and `_wiki/vehicles/sph-2.md`: replace "why the two differ is not known" with: the SPH-2 sight prints distances from a live simulation (with altitude), it does not read the table's distances; the table is not what the dial shows, hence a varying offset. The mortar sight reads the table directly and adds a constant 650 to the mil label.
- `_wiki/equipment/l81-mortar.md`: "Why the scales are shifted by 650 is not known" -> hard-coded +650 on the mil labels in the mortar sight widget. Minimum range: the barrel pitch limit (+15 degrees = dial 911.8) allows about 103 m by table interpolation; 132 m is the community-measured stop; say which is which.
