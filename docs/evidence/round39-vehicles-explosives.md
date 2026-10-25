# Round 39: vehicles, explosives and throwables (RE39-VEH)

Backlog source: the "Vehicles" and "Explosives & throwables" sections of the round 38 backlog. Statuses: FOUND, NATIVE, SERVER, ABSENT, plus NOT DONE for items that were not reached inside the per-item timebox (nothing was guessed for them). Evidence levels: cooked data read, Blueprint bytecode read, static disassembly of the decompiled corpus. The game was never run, no devirtualization was attempted. Extractor output is under `E:/Reverse_Engineer/wardogs_analysis/round39_veh/` (`out/` Molotov Blueprints, `out2/` throwable Blueprints, `out3/` repair/fuel action Blueprints and `ESmokeTypes`).

Generated data: `python -I _tools/vehicle_round39_tables.py --write` rebuilds `assets/data/vehicle-weapons.json`, `vehicle-seats.json`, `vehicle-health-effects.json`, `vehicle-flares.json`, `vehicle-repair-tools.json` and the page [`game-features/Wardogs_VehicleWeaponsEffects_v1.md`](../../game-features/Wardogs_VehicleWeaponsEffects_v1.md) (`--check` exits 1 when stale).

Counts: FOUND 15, NATIVE 3 (partial), ABSENT 5, NOT DONE 29 (listed at the end).

## Vehicles

### V-1 Vehicle machine guns: rate and range. FOUND (cooked data; native default for one field)

Source: `WDVehicleWeaponExtensionDataAsset` (`WE_*`) -> `WeaponStatsData` -> `WeaponStats.RoundsPerMinute` / `EffectiveRange`. Full table: page section 1.

| Weapon | Vehicles (extension asset) | Rounds/min | Range (m) | Calibre | Reload (s) |
|---|---|---:|---:|---|---:|
| M249 (ring and mounted) | Kodiak/SUV ring `WE_WHL_02_RingTurret`, Humvee ring `WE_WHL_05_RingTurret`, Ural Defender `WE_WHL_07_Turret`, L2A6 mounted `WE_TNK_01_Heavy_MountedMachineGun` | 850 (stats asset `DA_M249_Stats`, the infantry M249 asset) | 700 | 5.56 | 4.25 |
| M2 Browning | Wolf-110 ring `WE_WHL_08_RingTurret`, T-72B3 mounted `WE_TNK_04_MountedMachineGun`, MG nest `WE_STN_06_MountedMachineGun` | 600 (native default, asset omits it) | 1,000 | .50 cal | 8.0 |
| PKTM coaxial (T-72B3) | `WE_TNK_04_MachineGun` (stats asset `DA_LMG_02_Stats`) | 600 (native default, asset omits it) | 1,000 | 7.62x54 | 4.25 |
| MG3A1 coaxial (L2A6) | `WE_TNK_01_MachineGun` | 650 | 200 | .308 | 4.25 |
| M134D minigun | AH-6M `WE_ROT_03_AttachedMachineGuns`, Humvee `WE_WHL_05_RingMinigun` | 1,500 | 800 | .308 | 4.25 |
| Z20 Lakota machine gun | `WE_ROT_04_MountedMachineGun` (+ `_L`) | 1,500 | 1,500 | .308 | 5.0 |

The default 600 is the `FWDWeaponStats` constructor value at `+0x138`, the same rule `_tools/spray_patterns.py` and the spray page already apply ("— -> 600" for the M2). Evidence: cooked data (rates and ranges where the asset sets them), native constructor default (600). Reproduce: the tool above, section 1 of the page.

### V-2 Helicopter flares: restock, cooldown, lock-on, "3 bursts". FOUND (cooldown, consumption, text) / NATIVE (restock, lock-on)

- **Cooldown 5.0 s, FOUND (native default).** `FWDFlaresSettings` sits at component `+0x2C0` (targeting settings `+0x260`, countermeasure settings `+0x60`). The targeting-settings constructor `sub_14766AEA0` (RVA `0x766AEA0`) writes at struct `+0x60`: starting amount 0 (memset), range min `0x41C80000` = 25.0, range max `0x42C80000` = 100.0, active time `0x40A00000` = 5.0, cooldown `0x40A00000` = 5.0. No shipped asset sets `FlaresCooldownTime` (round 36), so every flare vehicle uses 5.0 s. Active time is 3.5 s on every vehicle (data).
- **Fire path (static).** `Server_FireFlares` impl `sub_14766EDF0` (`0x766EDF0`): proceeds only when the cooldown flag (`+0x798`, constructor default true at `0x766B080`) is set and `sub_14679E540(inventory, FlaresIdTag, 2, 1)` -> `sub_14678BD80` removes **one** unit of the flare item from the vehicle inventory (stops at count 1). Then it sets `bFlaresActive` (`+0x791`), clears the cooldown flag, and starts two timers on the component: `FlaresActiveTime` (callback `0x76794B0` clears `bFlaresActive`) and `FlaresCooldownTime` (callback at `0x7679520`, a lambda the corpus did not split out; it is the only writer left that can set the cooldown flag again).
- **Flare count is the inventory.** `sub_14767E260` (`0x767E260`, reached from `0x7689D10`) adds `a4` to `CurrentFlaresAmount` (`+0x790`) when the added item's tag equals `FlaresIdTag`; `sub_14767E3A0` subtracts on removal. So the count is the number of `Id.Item.Flares` units in the vehicle inventory; `OnRep_UpdateFlareCount` (`0x768AC90`) mirrors it to the client.
- **"3 bursts per use" vs 2 flares.** The text is the string `TooltipDescription.Countermeasure.Flares` ("- Deploys 3x bursts of flares") in `DT_EntityData_Ext_Flares`; no number in any asset or function is 3 for bursts. The vendor row `DT_VendorData_Ext_Flares` sells `Id.Item.Flares` with `Amount` 1 for 750 (level 1). A press removes one flare unit (above). The two do not conflict in data: 2 is the starting inventory (units), "3x bursts" is flavour text for the visual (left/right target offsets in the struct). The airplane starts with 3 units (`FWG_01`).
- **Restock: NATIVE, not found.** The function that grants `StartingFlaresAmount` (`+0x2C8`) into the inventory was not located (searched the vehicle component range `0x7660000-0x76B0000` for byte reads of `+712`: no hit; `Client_FlaresRestocked` is a UI/reflection stub `0x4DD6400`). Evidence cannot say whether a station tops flares up.
- **Lock-on: NATIVE, not found.** The only reads of `bFlaresActive` (`+0x791`) in the corpus are in the fire function and the active-time callback; no lock-on consumer reads it (token search "1937" returns 10 functions, none a missile consumer). The effective-range pair (`+0x2CC`, `+0x2D0`) has no reader found.

Evidence: cooked data; static disassembly (`sub_14766EDF0`, `sub_14766AEA0`, `sub_14767E260`).

### V-3 Empty fuel tank. NATIVE (partial)

`UWDVehicleFuelComponent::GetVehicleHasFuel` (`0x7667660`) returns `fuel attribute > 0` (when a flag at `+184` is set, else true). The event `ABHBaseVehiclePawn::VehicleOutOfFuel` (`0x53DE5F0`, slot 317) exists; its base body is the shared no-op `0x1562FE0`, `AWDRotaryVehicle` overrides it at `0x76B8A70` (ends in a protected-region jump). The only other `+2536`-slot user in the vehicle range is the stationary loudspeaker (unrelated). Data side found: tank damage adds a fuel leak (`WDFuelComponentEffect.FuelLeakPerSecondValue`: 0.1 at tank health below 10 percent up to 3.0 at 0 percent; see page section 4). The engine-stop consequence is not shown by any value or readable function. Searched: Blueprint bytecode in the data folder (no `OutOfFuel`/`HasFuel` hit), corpus callers of `0x53DE5F0`, `0x7667660` (none direct).

### V-4 Fuel canister: 25 per use against 2.0 every 0.75 s. FOUND (bytecode)

`ID_FuelCan_40L` carries `WDItemExtensionData_Appliable.AttributeValue = 25.0` (attribute `Attribute.Gameplay.Fuel`) and `ContainerData` `MaxAmount` 40, `UpdateTime` 0.75, `UpdateAmount` 2.0. Neither `B_Action_FuelCan_Refuel` nor `B_Action_FuelCan_ReFill` reads `AttributeValue` (0 hits in their bytecode; `UpdateAmount` is read 5 and 3 times). So the shop's "25" is the item's attribute value that the timed action ignores; the real flow is 2.0 per 0.75 s (2.67 per second, 15 s for 40). The 20 L can (`ID_FuelCan_20L`) exists in data and has no vendor row (unchanged from round 36).

### V-5 Hand repair: Wrench durability, time per application, repair rate. FOUND (bytecode)

`B_Action_VehicleRepairTool::HandleApplication` (bytecode, statements 830 to 1812): `RepairAmount` = `AppliableContainerData.UpdateAmount`; that value goes to `TryRepairVehicleHealthZone(RepairValue)`; `WDDurabilityHelpers::UpdateDurability(owner, inventory extension, RepairAmount * -1.0, 0.0, 100000.0)` takes the same amount off the item. `AttributeValue 5.0` on the items is not read there.

| Item | Health per application | Seconds per application | Health per second | Durability | Time to empty |
|---|---:|---:|---:|---:|---:|
| Wrench | 10 | 0.68 | 14.71 | 600 | 40.8 s (60 applications, 600 health) |
| Light Drill | 14.5 | 0.75 | 19.33 | none | - |
| Heavy Drill | 14.5 | 0.5 | 29.0 | none | - |

So durability 600 is health units repaired (60 applications), not uses or seconds, and the wiki's "5 health per application" is the unread `AttributeValue`. Whether `TryRepairVehicleHealthZone` clamps to missing zone health is native and not read. Drills have no durability fragment (they cannot wear out; consequence of `UpdateDurability` on an item without the fragment not read).

### V-6 Countermeasures "Not stated". FOUND

`TargetingSettings.CountermeasureSettings` in the gameplay-systems asset: flare block on FWG_01, ROT_02, ROT_03, ROT_04 only. A smoke block (item `Id.Item.VehicleSmoke`, cue `GameplayCue.Vehicle.Countermeasures.Smoke`, byte at `+0x08` = 1, floats 16.0 and 90.0, vector 0/400/200) is also present on **TNK_01 Heavy (L2A6)**, **TNK_03 (Gepard)**, **TNK_04 (T-72B3)**, and **SPW (M113)** (byte 255). Wheeled vehicles, Kodiak, Humvee, Dune Buggy, Bobcat, Ural, Wolf-110 and the SPH-2 artillery variant have no countermeasure block. The member names are obfuscated, so the meaning of the byte and floats is not named by the game (the byte sits where flares keep the starting amount; the shop stats list "Smoke" only for the L2A6). Evidence: cooked data.

### V-7 Pickup seats, ROT_03 and ROT_04 seats, seat roles. FOUND (cooked data)

- Pickup: base seat asset `DA_SeatSettings_WHL_02` has 4 seats (Driver, 3 active passengers). `DA_WHL_02_Pickup_ExtraSeats` (referenced by the pickup chassis part `VP_WHL_02_RearBack_Pickup_Chassis` under the fragment key `ExtraSeats`) has 6: Driver, 3 active passengers, then 2 active passengers flagged `bIsExteriorSeat` (the bed). So the "extra 2" are the two exterior bed seats; the 6 includes the base 4 (whether the fragment replaces or adds to the base seat fragment is part-assembly code, not read; the 6 stated is consistent with replacement).
- ROT_03 (MH-6/AH-6): `DA_ROT_03_SeatSettings` 6 seats (Driver, 1 interior active passenger, 4 exterior active passengers); `DA_ROT_03_Attack_SeatSettings` 2 seats (Driver, active passenger). ROT_04 (Z20): 13 seats (Driver + 12 active passengers); the machine-gun variant `DA_ROT_04_SeatSettings_MachineGun` 13 seats with 2 gunners. ROT_02 Havoc: Driver + Gunner. FWG_01: Driver + 1 active passenger. SPW (M113): Driver + 9 passive passengers.
- STN_01 to STN_06: one seat each, `Gunner` (exterior) for STN_01, 02, 03, 05, 06, role `None` (exterior, crew flag) for STN_04. No stats asset (unchanged: ABSENT).
- Active versus passive: ABSENT as a data difference. `ActivePassenger` and `PassivePassenger` are only role tags on `SeatRoleTag`; only the M113 uses `PassivePassenger` (9 seats). The seat animation block carries a `Seat.Passive` blend-space key on the driver too, so the word is also an animation name. No consumer function was searched, so what the role does in play is not in the data.

### V-8 Vehicle health-trigger effect objects. FOUND (cooked data)

251 threshold rows over 23 gameplay-systems assets; table in page section 4. Effect objects: cue 155, wheeled 94, fuel leak 50, wheel drag 44, wheel friction 44, engine 43, tracked track speed 24, rotary behaviour 20, rotary disable-assists 7, wheel cue 12, turret 4. Highlights: `WDVehicleTurretEffect` `bStabilisationPermitted = false` below 25 percent of body health; tracked `TrackSpeedModifier` 0.6 below 55 percent engine health and 1.0 at 55 percent track health; rotary main rotor `ModifierValue` -0.05 at 55 percent and -0.75 at 0; tail rotor RPM multiplier -0.025 (55), -0.1 (25, 30), -0.9 or -1.2 (0); fuel leak per second 0.1 / 0.4 / 0.75 / 2.0 / 3.0 by threshold. `WDVehicleEngineEffect` serialises nothing except `bIsDestroyed: false` at 55 percent engine health, so below 55 percent the class default applies (not read; inferred true). Unit of `FuelLeakPerSecondValue` (fraction or absolute) not read.

### V-9 Fixed-wing airplane top speed. ABSENT

Searched: `FWG_01` stats (none exist, as for the other `FWG` data), `DA_FWG_01_Engine`, `_Body`, `_Drag`, `_FlightCharacteristics`, `_Config`. No speed limit is stored. Inputs found for a physics result: `MaxEngineThrust_n` 226,800, `MassOverride` 10,000, `DragCoefficient` 0.0056, areas front 4000 / rear 3500 / side 5000 / top and bottom 2,800,000, `AirDensityAtSeaLevel` 0.00125, `MaxAngularVelocityOverride_degps` 180. A terminal speed would have to come from the lift/drag curves in a simulation, which is not a stored value.

### V-10 Airplane `FlightCharacteristics`. FOUND (partial)

`DA_FWG_01_FlightCharacteristics`: airfoil list (fuselage, airbrake with 45-degree incidence and 30 area, extendable) plus control-assist objects: a G-limit condition ("GForce exceeds limit", local G on Z greater than 6.0) that reduces pitch, pitch auto-trim from the airspeed curve table, PID stabilise-after-release (gains 0.2094 / 0.001745 / 0.08727), damping interp speed 0.5, "engage when fully stopped" and the change-rate block (increase/decrease 0.5 per second). Helicopter `DA_ArcadeControls_*` and the other ~270 assist objects were not decoded.

### V-11 Max incline. ABSENT (wheeled and rotary), FOUND (tracked, unchanged)

`MaxInclineAngle` 50.0 appears on `DA_TNK_01_WheelData`, `DA_TNK_04_WheelData`, `DA_SPW_01_WheelData` only. The wheeled `Characteristics` assets store `MaxSlopeLockSpeed` 2.0 (hill-hold speed, WHL_02 shown) but no angle; rotary assets have none.

### V-12 Havoc, vehicle rocket calibres, `_SB` shells. FOUND

- Every `WE_*` extension (24) names its ammo through `AmmoCaliberTag`. Havoc (ROT_02) and ROT_03 rocket pods use `Item.Caliber.122mm` and the shop item `ID_VehicleHelicopterRockets`; the projectile asset with that tag is `DA_122mm_ProjectileData` (BaseDamage 100, ExplosiveRadius 600, EffectiveExplosiveRadius 200, falloff 1.0). `DA_122_mm_HAVOC_ProjectileData` (tag `Item.Caliber.122mm.Havoc`, BaseDamage 300, radius 300, effective 600, falloff 0.6, the swapped pair) is referenced by **no** vehicle weapon, item or stats asset in the export. If the tag match is exact, the Havoc pods fire the plain 122 mm asset. How native code picks the projectile asset (an exact tag match or a vehicle-specific lookup) was not read.
- `70mm`, `84mm` and `84mm.TVGuided` projectile assets have their own ammo items (`ID_70mm`, `ID_84mm`) but no vehicle weapon extension names those calibres: the 24 extensions use 122mm, 30mm, .308, 5.56, .50, 7.62x54, 72mm (Verba), 20x102, 120x800 mortar, 35x228, 155, 120x570, 125x570 and DroneProjectile. So no vehicle weapon in data fires 70 mm or 84 mm.
- `_SB` (Sandbox) shells: `ID_155mm_SB`, `ID_155mm_Standard_SB`, `ID_155mm_Expensive_SB`, tags `ID.Item.155mm.Sandbox`, projectile tags `Item.Caliber.155mm.Standard.Sandbox`; fired by the item `ID_VehicleTurretArtillery_SB`; `ID.Item.155mm.Sandbox` has a vendor row in `DT_WeaponMarket`. They are cooked and listed in a vendor table; whether the live shop uses that table for them was not read.

### V-13 Weapon names to weapon tags. FOUND (partial)

Each `WE_*` asset carries `WeaponExtensionName` (shown in the page) and `WeaponItemId`; the mapping from the shop's `VehicleWeaponryNames` strings to these is by that name, as in the table. `PossibleHitLocations` to model was not mapped.

## Explosives and throwables

### E-1 Molotov: impact or fuse. FOUND (cooked Blueprint + static)

`B_Molotov` CDO sets the obfuscated bool `_aaablepeghlpjblibpkdm` (`AWDExplosive +0x49C`) to **true**. `AWDExplosive` mesh-impact handler `0x6CAB030` (virtual slot 236, reached through the reflected `OnMeshImpactEvent` `0x6CAD250` thunk): `if (+0x49C || (threshold +0x498 != 0 and impact speed squared >= threshold squared)) call virtual slot 237` (the detonation, `0x86A15B0` for the Molotov) on the first impact. With the bool set, the threshold (0.0) is irrelevant. The fuse (5.0 s, not cookable) remains the backstop. Across all dumped throwables (frag, Gold frag, 8 smoke colours, C4, IED, mine, Claymore, world smoke) **only `B_Molotov` sets this bool**; the others burst on their fuse (frag 4.0 s cookable, smoke 3.0 s) or by their own trigger (C4 `bStickOnImpact`). Not resolved: the net-role test (`sub_143A9B050 != 3`) that picks between the two code paths in `0x6CAB030`; both test the same bool before exploding. Round 36's "no reader of `+0x498` found" is explained: the reader is the same handler, which reads the bool and the float at `a1[294]`/`+1180`.

### E-2 Molotov patch spacing. FOUND (static, derived reading)

Spawner `0x86A15B0` places patches with helper `0x86A0A70`, a golden-angle (Vogel) spiral: for patch `i` of `N` it uses angle `i * 2.39996 rad` and radius `R * sqrt(i / (N - 1))`; `i = 0` is the centre. `N` = `+0x678` = 15 (Blueprint), `R` = `+0x670` = 250 cm. So radii (cm) for i = 0..14: 0, 66, 94, 116, 134, 150, 164, 177, 189, 200, 211, 221, 231, 240, 250, each patch a 200 x 200 x 50 cm box (BoxExtent 100 x 100 x 25). The spiral centre is moved along the throw direction by `ratio * 250 * 1.5` cm (`+0x674` = 1.5), where `ratio` is a quotient of two vector lengths (read as the horizontal share of the impact velocity). On a steep downward hit (flag + z <= -0.7) the first `(int)(2N * 0.3 + 0.5) >> 1` = 4 patches use a reduced radius `sqrt(0.3) * 250` = 137 cm (`+0x680` = 0.3). Each point is then snapped to the ground by traces (`sub_143CAB670` etc.). Patch actors receive `+0x684` (100) and the field `+0x2D0..+0x2DC` values; unchanged (not decoded).

### E-3 Smoke type `NewEnumerator1`. FOUND (cooked data)

`ESmokeTypes` is a `UserDefinedEnum` whose `DisplayNameMap` names `NewEnumerator0` = "Covering" and `NewEnumerator1` = "Signal". The six coloured grenades with `SmokeType NewEnumerator1` are the signal grenades (blue, green, orange, purple, plus the others on the wiki page); the Covering type is the other group.

### E-4 Signal grenade map marker. FOUND (partial)

`DA_Tracker_Map_SmokeGrenade` (`WDUIDeployableMapTrackerData`) has 5 entries keyed by item tag: Red = "Hostile" ("Hostile position here!"), Blue = "Friendly" ("Friendly positions Here!"), Yellow = "Alert" ("Alert point here!"), Green = "Supply Request" ("Supplies needed here!"), Purple = "Landing Zone" ("Safe Landing Zone here!"). Row `Trackers.Type.SmokeGrenade` in `DT_TrackerData_Map_SmokeGrenade` uses class `WDUIPersistentDataTracker`, view model `WDUIDeployableMapTrackerViewModel`, widget `W_Tracker_Map_Deployable`, required tags `Trackers.Type.SmokeGrenade` + `Id.Item`, and `bShouldRecreateOnFactionChange` = true. Who can see the markers (team filter) is decided in the view-model code, not read.

### E-5 Smoke and enemy AI sight. ABSENT (data) / inference

Searched: `BP_SmokeGrenadeVFX` (components: scene root and a Niagara component only; the 8 trace directions with a 65 cm sphere are for shaping the plume against geometry), `B_SmokeGrenade_*` (static mesh, damage entity, faction, cue, interactable: no collision volume or sight-blocker registration). `UWDSightBlockerSubsystem` reads baked `UWDSightBlockerBakedDataAsset` per-map data (`DA_SightBlockers_Europe/Kavkazi/NorthAmerica`), not dynamic actors, and its one caller is the aim-assist picker (round 36). The AI uses the engine `AISenseConfig_Sight` (round 36 AI). Nothing in data or code makes smoke an obstruction to those traces; the engine sight sense is geometry-only, so no smoke blocking of AI sight is found (negative result from static search, not proof).

### E-6 Smoke total duration `GetEffectiveSmokeTimings` (`0x869F010`). NATIVE, stuck

The corpus lists `0x869F010` as a failed decompile ("entry lies inside another function at `0x869F006`", the neighbour `sub_14869F006` is a 2-instruction stub). Body not recoverable here. Data side unchanged: `Total Duration` per smoke asset (64 on `DA_SmokeGrenade_Blue`), page values 2 + 2 + 2.

### E-7 Vehicle weapons firing 70 mm, 84 mm, 122 mm.Havoc, `_SB`. FOUND

See V-12.

### E-8 `TestGrenadeLauncher`, flash and stun. ABSENT

Flash and stun grenades: no item, shop row or effect in this export (unchanged). `TestGrenadeLauncher`: not searched this round (see NOT DONE).

## NOT DONE (not reached inside the timebox; no values guessed)

Vehicles: acceleration time (not stored in the engine assets read; only the airplane's physics inputs were read); which of EngineData/DynamicsData drives a tracked vehicle and the torque/brake units; native defaults for the `—` fields; gear order; wheel-level values; mass units; Refuel Max restock early stop; parachute from aircraft; `GE_Vehicle_Health`/`0x52311D0` callers; sweep hits `0x3A902D0`; tyre destruction; STN_05 geometry; damage-table operations and priority; rotary assist bodies (only the airplane's were read); vehicle-extension restock count; the handling "Not yet known" column; wheel/surface curves; vehicle input sub-objects. Explosives: fire end at 45 s versus ubergraph timer; burning removal; fire-field instigator; downstream friendly-fire rules; mine/Claymore/C4 native constructor values; Claymore target tag; 30-degree placement; mine after-blast; placement conditions; smoke volume pawn list; throw-velocity curve combination; `MinimumRemaining` field; 40 mm underbarrel data; `CT_Weapon_Spread`; `TestGrenadeLauncher`; armoured targets.

## Wiki updates

- `_wiki/vehicles/vehicle-weapons.md` (Machine guns section): "The rate and range of the M249 are not yet known on any of the four" -> "All four M249 mounts fire 850 rounds/min with a 700 m range."
- `_wiki/vehicles/vehicle-weapons.md` (Machine guns section): "Their rate and range are not yet known" (M2 Browning) -> "The M2 Browning fires 600 rounds/min (the game's default rate; the weapon data does not set one) out to 1,000 m."
- `_wiki/vehicles/vehicle-weapons.md` (L2A6 coaxial sentence): "its rate and range are not yet known" (T-72B3 PKTM) -> "the PKTM fires 600 rounds/min (default rate) out to 1,000 m."
- `_wiki/vehicles/vehicle-weapons.md` (table, rows lines 56 to 60): replace each "Not yet known" rate/range for M249, M2 Browning and PKTM with 850 / 700 m, 600 / 1,000 m and 600 / 1,000 m.
- `_wiki/vehicles/humvee-m249.md`, `kodiak-m249.md`, `ural-defender-m249.md`: rate "Not yet known" -> 850 rounds/min; range "Not yet known" -> 700 m. Same for the L2A6's mounted M249 in `_wiki/vehicles/l2a6.md`.
- `_wiki/vehicles/wolf-110-m2-browning.md`, `_wiki/vehicles/t-72b3.md`: M2 Browning rate "Not yet known" -> 600 rounds/min (default), range -> 1,000 m; `t-72b3.md` PKTM -> 600 rounds/min (default), 1,000 m.
- `_wiki/vehicles/countermeasures-and-flares.md` (Amounts and reloading): "The item text's '3 bursts per use' does not match these helicopter counts, and the data does not say how the two fit together. How flares are restocked is not yet known." -> "A flare press uses one flare from the vehicle's inventory and starts a 5 second cooldown (the game's default; no vehicle sets its own). The '3x bursts' line is item text only; no number in the data is 3 bursts. How flares are restocked is not yet known."
- `_wiki/vehicles/countermeasures-and-flares.md` (line 61 and "The other vehicles list no countermeasure"): "These include the SPH-2 ..., the Flakpanzer Gepard, the T-72B3, the M113 APC SV and every wheeled vehicle." -> "The Flakpanzer Gepard, the T-72B3 and the M113 APC SV have a smoke countermeasure in their game systems data (one charge each on the Gepard and T-72B3, 255 on the M113), like the L2A6; the SPH-2 variant, the Kodiak, Humvee, Dune Buggy, Bobcat, Ural and Wolf-110 have none." (Per-vehicle pages: update the countermeasure row for `flakpanzer-gepard.md`, `t-72b3.md`, `m113-apc-sv.md` from "Not stated" to "Smoke".)
- `_wiki/guides/vehicle-guide.md` (line 101) and countermeasures Tips: "The data gives each helicopter 2 starting flares, while the item text says 3 bursts per use" -> "Each helicopter starts with 2 flares; each press uses one and then waits 5 seconds before the next. The '3 bursts' in the item text is not a count."
- `_wiki/equipment/wrench.md` (How it works): "adds 5 vehicle health per application ... Durability is 600 ... What that number counts ... not stated. The time for each application is not yet known." -> "Each application repairs 10 vehicle health every 0.68 seconds (about 14.7 per second). Durability 600 is health: a full Wrench repairs 600 health in about 41 seconds (60 applications)."
- `_wiki/equipment/` drill articles (Light Drill, Heavy Drill) and `_wiki/vehicles/repair-and-vehicle-parts.md` (line 103), `_wiki/guides/vehicle-guide.md` (line 137): "+5 per application", time not stored -> Light Drill 14.5 health every 0.75 s (19.3 per second), Heavy Drill 14.5 every 0.5 s (29 per second), no durability listed; Wrench 10 every 0.68 s.
- `_wiki/equipment/fuel-canister.md` (line 31), `_wiki/vehicles/fuel-and-refueling.md` (line 41): "25 fuel per use ... how the two fit together" -> "The shop line '25 fuel per use' is not what the refuel action uses. The action adds 2 fuel every 0.75 seconds (about 2.7 per second), so a full 40 L canister empties in about 15 seconds."
- `_wiki/vehicles/seats-and-passengers.md` and `_wiki/vehicles/pickup*.md`/`kodiak.md`: pickup "extra 2 seats, source unresolved" -> "The Pickup's six seats are the driver, three interior passengers and two passengers in the bed (exterior seats)." ROT_03/ROT_04 seat counts: MH-6 / AH-6 base 6 seats (4 exterior), AH-6 attack variant 2, Z20 Lakota 13, Havoc 2, fixed-wing 2, M113 10 (9 passive).
- `_wiki/vehicles/fixed-wing-airplane.md` (lines 17, 32) and `_wiki/vehicles.md` (line 58): top speed "Not stated" -> "The data stores no top speed: the airplane's speed comes from engine thrust (226,800 N), mass (10,000) and drag, not from a limit."
- `_wiki/equipment/molotov.md`: "Whether a thrown Molotov bursts on impact or on its fuse" -> "A thrown Molotov bursts on its first impact (it is the only throwable set to do so); the 5 second fuse is only a backstop." Patch layout line (line 49): spacing "not known" -> "The 15 patches lie on a spiral out to about 2.5 metres from the impact point (the spiral centre is pushed up to 3.75 metres further along the throw), each patch 2 m x 2 m."
- `_wiki/equipment/fire-smoke-and-flash.md`, `m18-smoke-grenade.md`: smoke AI sight "not determined" -> "Nothing in the data makes smoke block enemy soldiers' sight; the smoke has no collision or sight-blocker."
- `_wiki/equipment/m18-signal-grenade.md` (line 42), `fire-smoke-and-flash.md` (line 68): how markers are created -> "Each signal colour adds a map marker through the deployable map tracker (Red Hostile, Blue Friendly, Yellow Alert, Green Supply Request, Purple Landing Zone); the game names the smoke types 'Covering' and 'Signal'." Who sees the marker is not in the data.
- `_wiki/equipment/` 122 mm / Havoc rocket articles: if the wiki quotes the `.Havoc` asset's 300 damage / 3 m inner radius for the Havoc pods, replace with the plain 122 mm asset (100 damage, 6 m outer, 2 m inner, falloff 1.0), because no vehicle weapon references the `.Havoc` asset. (The shop-listed rocket pods use `Item.Caliber.122mm`.)
- `_wiki/guides/vehicle-guide.md` (line 120/121), `fuel-and-refueling.md` (line 31): empty tank "not yet known" stays; add "Fuel tank damage makes the tank leak fuel: 0.1 per second below 10 percent tank health up to 3 per second when the tank is destroyed (varies by vehicle)."
