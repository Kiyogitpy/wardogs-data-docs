# Round 45, agent B: vehicles, buildables, AI, modes, other open items

Continues [round 42](round42-vehicles-explosives.md) and [round 43](round43-econ-buildables.md). Static review of CL516586 only; nothing was run. Native RVAs are for `WardogsClient-Win64-Shipping.restored.exe` (SHA-256 `a5c3db10...0cc37`), read from the decompiled corpus (`corpus.sqlite`) and with capstone disassembly; no devirtualization. Cooked data was re-dumped with `WdExtract dump` (maps and cells) and `rawfiles`. Scratch: `E:/Reverse_Engineer/wardogs_analysis/round45_b/` (`ctordef.py`, `dispscan.py`, `findctor.py`, `strxref.py`, `maps/`).

Counts (24 items from the backlog sections Vehicles 7, Explosives 1, Buildables 2, AI and PvE 5, Progression 1, Modes 3, Other 5): **FOUND 18** (4 of them with a named native remainder), **ABSENT 2**, **NATIVE (open) 4**, PROTECTED 0, SERVER 0.

New data: [`assets/data/vehicle-native-defaults.json`](../../assets/data/vehicle-native-defaults.json) (tool `_tools/r45_vehicle_defaults.py`, native-constructor snapshot read with `_tools/ctor_defaults.py`) and [`assets/data/r45-misc.json`](../../assets/data/r45-misc.json) (tool `_tools/r45_misc_data.py`).

| # | Item | Status | One line |
|---|---|---|---|
| 1 | Wheel-level values | FOUND (index read not located) | `Values[0..2]` = intact / damaged / destroyed; every unset key is the native default, not 0 |
| 2 | Flare restock and lock-on | FOUND (restock), ABSENT (lock-on) | restock = adding `Id.Item.Flares` to the vehicle inventory; no lock path found |
| 3 | Tyre destruction | FOUND | wheel state byte written by `0x537C580` from the wheel health attribute |
| 4 | Native defaults for `-` fields | FOUND | constructors read: wheeled (5 classes), tracked engine, helicopter engine |
| 5 | Gear order | NATIVE (open) | default list `[3, 5]` and `bUseAutoReverse` true support "last = reverse"; consumer not read |
| 6 | Active vs passive passengers | FOUND | no rule difference in data; separate input-context sets and a pose flag |
| 7 | Handling column "Not yet known" | FOUND | the unset input fields take the defaults of `MWheeledVehicleInputDataAsset` |
| 8 | Smoke volume pawn list | FOUND (function role), NATIVE (result use) | per-pawn capsule-in-smoke test `0x869D738`; result not consumed in `UpdatePawnsInSmoke` |
| 9 | Drill Rig magnet and the hot zone | FOUND (size), NATIVE (movement) | zone extents x size multiplier; speed has no native reader |
| 10 | Emplacement cash rows, Placed vs Placed-in-FOB | NATIVE (open) | the pick is the engine data-registry lookup, not WD code |
| 11 | AI unit system | FOUND | `WorldToMeters` is the default 100, so 1 unit = 1 cm |
| 12 | PvE mission names | ABSENT | no scenario title in `Game.locres` (15 languages) |
| 13 | Scenario unit counts, helicopter speed units | FOUND | cm/s mover curve; vendor speed label KM/H; vehicle spawners counted |
| 14 | Scenario quest logic | FOUND | extraction flow and the spline mover read |
| 15 | Sniper Showdown faction count | FOUND | 100 free-for-all factions, least-populated assignment |
| 16 | Team Offence vote outcomes | FOUND | texts, defaults and thresholds |
| 17 | Deathmatch faction placement | FOUND (rule), NATIVE (first join) | player-chosen team, optional imbalance lock |
| 18 | Sniper Showdown faction count (duplicate of 15) | FOUND | see 15 |
| 19 | Map layouts beyond zone data | FOUND (partial) | world bounds, cell census, 450 Sniper Showdown loot points |
| 20 | Hashed property names | NATIVE (open) | token format decoded; no unsalted hash fits |
| 21 | Unnamed `_aaa` fields | NATIVE (open) | the token carries the real name length; no name proven |
| 22 | Water height grid | FOUND | sampler and both doubles read |
| 23 | Fluid Flux shader and packing | ABSENT | material functions are stripped in the cooked build |
| 24 | Mechanics units | FOUND | percent semantics from the cooked bytecode |

## 1. Wheel-level values. FOUND (cooked data + static disassembly); index read NATIVE

Every `MWheeledVehicleWheelDataAsset` field except `bPhysicsSurfaceUpdate` is a `FWheeledVehicleWheelConfigValue`, three floats (`Values`, `Values[1]`, `Values[2]`). The wheel state writer (item 3) produces 0, 1 or 2, so the three floats are **intact, damaged, destroyed**; the dune buggy radius 0.45 / 0.345 / 0.26 and brake torque 4000 / 3000 / 400 follow that order. The direct `Values[state]` read (an array indexed by the state byte) was not located: the only matching indexed loads are in unrelated functions (`sibscan.py` over `0x5200000-0x5500000`).

**Cooked JSON omits a key that equals the class default**, and the default is not 0. The constructor `0x5311EB0` (found through the vtable cross-reference of `UMWheeledVehicleWheelDataAsset`) stores: lateral and longitudinal friction and scale **1.0**, overturn / roll-moment / self-align scale 0, tyre pressure 2.0, radius **0.25**, width 0.2, rim / forward / vertical / cast offset 0, mass **10**, brake torque **1000**, suspension up and down travel **0.1**, spring **5000**, compression and relaxation damper **1000**, preload 0, physical-material lerp **1.0**. So `LateralFriction` on WHL_01 "intact" is 1.0 (not missing), WHL_08's `PhysMatLerpValue` intact is 1.0, and so on. The filled table for all 14 wheel assets is `assets/data/vehicle-native-defaults.json` section `wheelAssets` (`defaultFilled` lists what was filled).

Reproduce: `python -I _tools/r45_vehicle_defaults.py`; constructor: `python _tools/ctor_defaults.py 5311eb0 sdk/raw/Mechanized_classes.hpp UMWheeledVehicleWheelDataAsset`.

## 2. Helicopter flare restock and lock-on. Restock FOUND; lock-on ABSENT (bounded)

**Restock.** `CurrentFlaresAmount` (`+0x790`, uint8) is not set by a flare function at all: it **mirrors the vehicle inventory**. The Blueprint-visible `OnItemAdded(Path, Item, Delta, Context, Inventory)` (thunk `0x7689D10`) calls `0x767E260(this, ?, itemTag, delta)`; on the authority (`+368 == 3`) it compares the item tag with the flare settings tag (`FlaresIdTag`, `Id.Item.Flares` in every `DA_*GameplaySystems`; the compare is `0x395D3C0` against component `+0x2C0`), then `count += Delta`, marks the property for replication and, when the count is non-zero, calls `0x7673540` (the `Client_FlaresRestocked` event). The smoke block (`+0x350`) is handled by the same function with its own tag (count `+0x7B4`). `OnItemRemoved` (`0x7689EE0`) calls `0x767E3A0`, which subtracts. So **a restock is an inventory add of `Id.Item.Flares` to the vehicle**: the garage vendor row `DT_VendorData_Ext_Flares` sells `Id.Item.Flares` (category `Vendor.Category.Vehicle.CounterMeasures`, price **750**, amount **1**, level to unlock 1) and the spawn inventory `ID_SPW_Inventory` allows `Id.Item.VehicleSmoke` and `Id.Item.Flares` in its sub-slots. The count is decremented by the remove handler; what removes the item when the countermeasure key is pressed (the server fire function `Server_FireFlares`) was not traced.

**Lock-on.** Still no flare read in any lock path. This round added: `HomingTarget` lives on the weapon (`WDItemExtension_RangedWeapon +0x148`, `AWDVehicleWeaponExtension +0x380`); the cooked projectile data has no homing field (`bIsHomingProjectile` is an engine `UProjectileMovementComponent` bit, set in no cooked asset; only `DA_DebugHomingRocketData` and an audio event mention homing); so homing is switched on by native code that was not located. Searched: `0x6A68DF0`, the lock-list helpers, both lock Blueprints, `+0x790..0x798` readers (UI only), 3 projectile data families. **Next step:** find the writer of `UProjectileMovementComponent +0x1B4` (HomingTargetComponent) in the weapon-owner `SetHomingTarget` path (`0x6C2C600` is only the interface thunk).

## 3. Tyre destruction. FOUND (static disassembly)

The "physics sweep" function `0x3A902D0` of round 40 is a generic engine sweep helper and is not involved. Tyre state is attribute driven: `0x5356B00` (wheel set-up) binds the delegate `0x537C580` to the health attribute of each wheel (`*(wheel+48)`); on a change `0x537C580` stores into the replicated byte array at vehicle `+0x9B0`: **2 when the wheel's health is 0, 1 when health / max health is at or below the threshold of the matching trigger entry (stride 64, float at `+0x38`; 55 percent in the cooked triggers), otherwise 0**. The change handler `0x5370A40` compares with the previous copy (`+0x9D8`), notifies listeners and refreshes the wheel (`0x53AA370`, mesh radius). The effects at 55 percent (WheelPop cue, drag +1.5, friction -0.35, pull +/-0.125, brake +0.05) are the cooked trigger rows of round 40. So damage reaches a tyre as health loss on the wheel's section, not through a sweep.

## 4. Native defaults for the `-` handling fields. FOUND (static disassembly)

Constructors read (class, ctor): wheeled engine/transmission `0x530F660`, input `0x530F7A0`, axles `0x530F5A0`, characteristics `0x5384E80`, wheel `0x5311EB0`, tracked engine data `0x5304980`, helicopter engine `0x53846F0` (chosen by value coherence; two other functions store the same vtable and different values, so this one is the least certain). Values used by the handling page's em dashes:

| Field | Default | Vehicles that show `-` |
|---|---:|---|
| `IdleRPM` | 1,000 | WHL_02 (all three variants) |
| `TorqueScale` | 1.0 | WHL_01, WHL_05 |
| `LimitRpm` (6,500), `LimiterTime` (100), `FrictionTorque` (50) | as shown | those not set per asset (see JSON `defaultFilled`) |
| `bEnableBoost` | false | every wheeled asset (none sets it; each sets `BoostScale`, 1.03 to 1.2) |
| Axle `TorqueShare` | 0.5 | WHL_02 and WHL_07 axles |
| Axle `MaxSteerAngle` | 0 | unset axles |
| Tracked `TrackMass` / `SprocketMass` | 600 / 64 | TNK_01 Artillery, Heavy, TNK_04 |
| Tracked `BoostScale` / `BrakeForce` | 1.0 / 20 | TNK_01 Anti-Air boost; Artillery, Heavy, TNK_04 brake |
| Helicopter engine | operating 15,000, rates 1,000 / 1,000, main rotor 400 low / 500 operating, tail 1,500 | Havoc (empty asset), and the fields ROT_03 / ROT_04 leave unset |

`bEnableBoost` false with a stored `BoostScale` means the "Boost 1.03" column may be inert; whether the sim honours the flag was not traced. All values: `assets/data/vehicle-native-defaults.json` (`ctors`, `engineTransmission`, `axles`, `characteristics`).

## 5. Gear order (last wheeled ratio is reverse?). NATIVE (open)

Evidence for: the transmission constructor sets `bUseAutoReverse` true and the default `GearRatios` list is **two entries, 3.0 and 5.0** (a forward gear and a larger last entry), `CrawlingGear` 1, `FinalGearRatio` 3.0; Kodiak/Pickup (6.0 ... 6.0) and Humvee (3.6 ... 3.6) repeat the first ratio last, the Ural's last (3.25) is lower. No field names a reverse ratio (Chaos has `ReverseGearRatios`, this Mechanized struct does not). Evidence against: none found. The reader of `GearRatios` (asset `+0x88`) in the simulation was not located. **Next step:** the wheeled simulation setup that copies `TransmissionData` (look for the consumer of asset `+0x58..0xA7`, `bUseAutoReverse` at `+0x59`).

## 6. Active vs passive passengers. FOUND (cooked data + SDK)

Roles are the seat tags `State.Player.Vehicle.Role.{Driver,Gunner,ActivePassenger,PassivePassenger}`. Seat counts (`vehicle-seats.json`): Driver 23, ActivePassenger 62, Gunner 21, PassivePassenger 9 (M113 seats 1 to 9 only), none 1 (loudspeaker). **No gameplay rule distinguishes the two passenger roles in the data**: all 17 modifier-state queries (`DA_CharacterModifierState_*`) and the Sprint, Tac-Sprint and ping-request blocks list both together. What differs: `MVehicleInputControlsDataAsset` has separate `ActivePassengerInputMappingContexts` and `PassivePassengerInputMappingContexts` arrays (`BHBaseVehiclePawn::GetVehiclePassivePassengerInputContext`), and the third-person animation has `bIsPassivePassenger` (`WDThirdPersonAnimInstance +0xE7C`, passive aim offset `VehiclePassengerPassiveAO`). None of the 15 cooked input-controls assets sets either passenger array (they set only the driver array, gunner on two), so by data both roles get no vehicle input context beyond the shared one. Player reading: the M113 rear seats are a passive-passenger pose; elsewhere passengers are "active" seats with no extra controls in the data.

## 7. Handling column "Not yet known" (Bobcat, Kodiak, Humvee, Ural, Wolf-110). FOUND

These are the unset fields of the input asset: `MWheeledVehicleInputDataAsset` defaults (ctor `0x530F7A0`): steer sensitivity **5.0** (Kodiak, Ural and Wolf-110 store none), steer input gravity 1.5, steer range 100, steer dead zone **0.01** (the Bobcat sets 0.05), steering assist 0 (Bobcat 20), assist threshold angle 1.0, throttle / brake / clutch sensitivity **3.0**, range 100, dead zone 0.01. Per vehicle effective values: `assets/data/vehicle-native-defaults.json` section `input`.

## 8. Smoke volume pawn list and fuse. FOUND (function role); NATIVE (use of the result)

`UpdatePawnsInSmoke` (`0x869F600`) passes each pawn's capsule (transform, half-height scaled by `+1392`, radius by `+1396`) and the smoke point list (`+744`) to **`0x869D738`**, a pure containment test: the capsule's bounding box must lie inside one of the list's spheres (32-byte entries: centre and radius) or inside the volume radius (`+96`), returning 1 or 0. The decompiled caller drops the return value, so what consumes "pawn in smoke" was not found (it may be elided by the decompiler). Fuse: already settled (smoke grenades `BaseFuseTime` 3, native base 5; Fire and Utility page). **Next step:** check whether `0x869D740` stores into a per-pawn flag through its seventh argument (`sub_143A99480(a1)`).

## 9. Drill Rig magnet: effect on the hot zone. FOUND (size); NATIVE (movement)

World component `WDHotZoneMagnetGameStateComponent` (native defaults, ctor `0x8566570`): speed `+0xF0` = 3.0, size multiplier `+0xF8` = (0.6, 0.6, 1.0); the Blueprint CDO overrides only the 900 s recharge and 180 s duration. On activation the authority handler `0x85674A0` and the client function `0x8571F80` multiply the **hot-zone cache extents component-wise by the world component's size multiplier** and pass the result to the control-zone component callback `0x8571E20`; tower number, durations and location are stored and replicated by `0x856FE50`. So an activation **shrinks the zone to 0.6 x 0.6 of its X and Y extents (area 36 percent, height unchanged)** with the native default; the rig's own data asset also carries 0.5 / 0.5 / 1.0 and speed 5.0, but the two functions read the world component's pair, not the asset's (which pair a server override uses is not shown). The speed float has **no native reader** (only the Blueprint getter `0x8573ED0`), and no cooked Blueprint calls `GetConfigHotZoneMagnetSpeed`, so how fast the zone travels is not in readable code. **Next step:** the control-zone component's location event binding (`BindHotZoneLocationEventBinding` `0x7772BD0`) and whatever consumes the new location.

## 10. Emplacement cash rows; Placed vs Placed-in-FOB. NATIVE (open)

Searched: the exe for the strings `CashRewards`, `BuildablePlaced`, `DefaultReward` (only event names `OnBuildablePlaced`; no table or registry name in native code, so the registry id is built from data tags), `DR_CashRewards` sources (15 tables; the three buildable tables share row names). With identical row names the choice is made by the engine's `UDataRegistry` source order (engine code, not WD): the WD binary adds nothing to decide it. **Next step:** read `UDataRegistry::GetCachedItem` (vtable `0xA7838E0`) for first-source versus last-source resolution; or log a placement reward. The row-less emplacements stay as in round 38 (default row applies if the engine falls back).

## 11. AI unit system. FOUND (cooked World Settings)

All four world maps (`Europe`, `Kavkazi`, `NorthAmerica`, `Russia`) have a `WDWorldSettings` export with no `WorldToMeters` property, so the engine default **100** applies: **1 Unreal unit = 1 cm**. The AI radii (`SightRadius` 200,000, `HearingRange` 100,000) are therefore 2,000 m and 1,000 m. Playable bounds (units, so /100 for m): Europe X -1,042,343 to -190,525, Y -975,825 to -201,000 (about 8.5 x 7.8 km); Kavkazi X -1,400,000 to -300,000, Y -1,700,000 to -600,000 (11 x 11 km); North America X -620,000 to 430,000, Y -600,000 to 320,000 (10.5 x 9.2 km); Russia -660,000 to 660,000 both (13.2 x 13.2 km). Kill Z is -150,000 (1,500 m) on three maps. Out-of-bounds is on in all four.

## 12. PvE mission names. ABSENT

Searched `Game.locres` English (5,948 entries; the same count in all 15 languages) for strike, swipe, disarm, hunter, killer, VIP, escort, scenario, mission: only "Missions" (frontend button), "Disarm" (mine interaction), "VIP" (player identity) and settings strings. The scenario plugin string tables (`STRINGS_StrikeDisarm_01`, `STRINGS_VIPEscort_01`) hold the placeholders "[PH] Strike and Swipe" and "[PH] VIP Escort"; Hunter Killer has no string table. No other title source exists in the client.

## 13. Scenario unit counts and helicopter speed units. FOUND

Counts (round 36) stand: Strike and Disarm 53 spawners, VIP Escort 95, Hunter Killer 0 (its 28 cells hold only text labels and instanced meshes). New: vehicle spawners placed (`b_VehicleSpawner_C`): Strike and Disarm 5 (Kodiak Pickup shown, faction Alpha), VIP Escort 6. Units: world units are cm (item 11). The extraction helicopter is moved by the quest mover at **cm per second**: distance += Curve(distance / spline length) x delta time; `Extraction_Helicopter_Speed_Curve_Entry` is 300 until 70 percent of the path, easing to 100 at the end (3 m/s then 1 m/s). The vendor stat label is "Max Speed (KM/H)", so helicopter max speeds on the vendor page are km/h.

## 14. Scenario quest logic (`Q_*` / `SQ_*`). FOUND

Round 36 read the graphs; this round read the runtime of the unfinished piece, `SQ_Extraction_Helicopter` (used by Strike and Disarm and VIP Escort). Entry nodes `Alpha`, `Bravo`, `Charlie` choose the helicopter's faction; each spawns a `Vehicle.Variant.Air.Rotary.Littlebird.Default` at `QuestObjective.BaseScenario.Extraction.Vehicle` with the engine started and a dummy pilot (`B_DummyPilot`); an OR node joins them; the helicopter flies the **EntryPath** spline (`WDQuestNodeLatentAction_WaitForVehicleMovedAlongSpline`, tick `0x88A48E0`, speed curve above); then `WaitForPlayersToGetInVehicles` for the extraction vehicle; then it flies the **ExitPath** with gravity disabled at the spline end; the scenario completes afterwards. The wait-for-players rule (all players or any) is native and not read.

## 15 and 18. Sniper Showdown faction count and team sizes. FOUND

`WDSniperShowdownFactionPool` is a class whose **constructor (`0x8644C80`) creates 100 faction data objects** named `FFAFactionData_001` to `_100` (display "FFA 1" to "FFA 100"); its CDO array (`+0x28`) holds them. `WDSniperShowdownFactionAssignmentComponent` spawns one faction actor per pool entry at BeginPlay (`0x864A150`) and assigns every joining player (`0x864B1D0` -> `0x86464B0`) to the **non-default faction with the fewest members** (first wins ties). So the mode is free-for-all with up to 100 single-player factions; with more than 100 players the extra players share factions (team size 1, or 2 beyond 100). Bonus: the mode's data-layer cells place **450 loot points** (150 per map: Kavkazi 87 high / 21 middle / 42 low, North America 69 / 16 / 65, Russia 79 / 19 / 52), tagged `Lootable.SniperOnly.{High,Middle,Low}Value`.

## 16. Team Offence vote outcomes. FOUND

`STRINGS_TeamOffence` and the notice tags give the player-facing texts, and the constructor of `WDTeamOffenceSettings` (`0x8936700`; no ini section overrides it in the excerpt) gives the numbers.

- Voter expired (`VoterExpired`): "You were removed from the vote on {OffenderName}: no decision was made within {Seconds} seconds." (`{Seconds}` is sent by the server with the notice).
- Left the safe zone (`VoterSafeZoneForgive`): "You left the safe zone before deciding, so your vote on {OffenderName} was recorded as Forgive."
- Other notices: punished "{OffenderName} was punished."; forgiven "{OffenderName} was forgiven."; banned "{OffenderName} was punished, they have been banned."; offender "You were punished for a team offence. You have {Points} of {Threshold} points before a kick vote."; "Removed for repeated team offences."
- Defaults: kick-vote threshold **15 consequence points**; `OffenceRelevanceSeconds` **180 s** (by name); **60 s** self-defence window; **900 s** reject-reward cooldown; `ApprovalsPerSessionToFlag` **3** and `FlaggedVoterWeight` **0.5** (meaning by field name only); ban lengths **600, 1,500, 3,600, 86,400 s** (10 min, 25 min, 1 h, 24 h) in that order; forgiveness time **604,800 s** (7 days).

## 17. Deathmatch faction placement. FOUND (rule); first-join placement NATIVE

`bAutoAssignFactions` is False in `DefaultGame.ini` (`bAutoAssignFirstFaction` is an editor/tutorial flag), so the server does not place players. A player picks a team (Alpha or Bravo) and the server validates it in `0x6D8F0B0`: when `bLockOverpopulatedTeams` (`WDGameStateSession +0x571`, ini False) is off the switch is always allowed; when it is on, the target team's size minus the smallest other team's size must be below `OverpopulatedTeamThreshold` + the invite bonus (ini threshold 2). `0x6D8EF10` is the "first faction" auto-assign and `0x6D8EE70` assigns a given tag (default faction when none). Which team a new player is shown first on joining is not traced (login handler `0x6D9A130`).

## 19. Map layouts beyond zone data. FOUND (partial)

The four world maps are World Partition levels (Europe 10,138, Russia 10,734, Kavkazi, North America streaming cells). A random 100 of 10,746 Russia cells hold only art and ambience: instanced and static meshes, HLOD, PCG partition actors, splines, destruction-ambience volumes, 3 `PropVehicle_C` props, 5 doors; **no `PlayerStart`, spawn volume, control-zone, FOB or buildable actors** in the cells. Gameplay placements live in the experience data layers (external data layers): the Sniper Showdown layers place 150 loot points per map (item 15), the Control Zone layer has `B_ControlZone_C` with `WDControlZonePlacementZoneComponent`, `WDControlZoneRegionsComponent` and `WDZoneComponent` (6 cells), and the PvE scenario layers hold the spawners of item 13. Spawn points are not placed in cells (consistent with the spawn-volume design). Bounds: item 11 and `assets/data/r45-misc.json` `worlds`.

## 20. Hashed property names. NATIVE (open); format decoded

Token = `_aaa` + **2 nibbles = the real name's length** + **16 nibbles = a 64-bit hash**, each nibble written as a letter `a`..`p`. Checked on all 17 known token / name pairs (round 12): the length byte equals the name length every time (for example `_aaaamiek...` = 12 = `ChargesToUse`). The remaining 64 bits did not match: xxh64 and xxh3 (seeds 0, 1, 0x1234, 0xFFFFFFFF), CityHash64 (plain and seeded), MurmurHash3 x64-128 (both halves), CRC32, Adler32, MD5, SHA-1/224/256/384/512, SHA3-256, BLAKE2b/2s (first or last 8 bytes, big or little endian), over UTF-8, UTF-16LE, lower-cased and NUL-terminated spellings (earlier rounds excluded FNV, djb2, sdbm, Murmur64A, XXH64). The same token is the same name everywhere, so it is a function of the name only; a keyed or salted hash is the likely reason. **Next step:** the build's obfuscation tool is not in the client; the only route is more known pairs plus a keyed-hash search, or the name table of a serialized owner descriptor.

## 21. Unnamed `_aaa` fields (`EWDEmoteData` and others). NATIVE (open); constraint added

No reader names them, and no cooked Blueprint references `WDEmoteData` (`findname` finds only `DT_EmoteData`). The token length rule (item 20) gives the real name length: `WDEmoteData` fields 10, 12, 22, 25 characters and the tag container 20; `WDEmoteActivationContext` tag 14. Across the SDK there are **7,334 distinct tokens**; lengths run 3 to 57 with a peak at 9 to 16. No names are claimed.

## 22. Water height grid. FOUND (static disassembly)

Sampler `0x76C1430` (grid), `0x6F771B0` (subsystem), getter `0x6F77110`. Grid asset layout: `+0x30/+0x38` world minimum X, Y; `+0x40/+0x48` world size X, Y (doubles); `+0x50/+0x54` width, height; **`+0x58/+0x60` = height range low and high**; `+0x88` the `uint16` samples. The point is converted to grid coordinates (`u = (x - minX) / sizeX x width - 0.5`), the four neighbours are blended bilinearly, a sample of **65,535 means no water** and is skipped (the remaining weights are renormalised), and **height = low + sample / 65,535 x (high - low)**. The subsystem returns `max(height - query Z, 0)`, the water depth at the point. Users: `WDMolotovGrenade::Auth_Explode` (`0x86A15B0`, where depth decides what happens to the fire) and `0x6E6FD40`. This confirms the round-42 hypothesis and gives the use.

## 23. Fluid Flux shader and channel packing. ABSENT

`Wardogs/Content/FluidFlux` has 283 files (90 surface material functions such as `MF_SurfaceFluxGet`, `MF_SurfaceFluxSet`). The cooked `MaterialFunction` exports hold only `bExposeToLibrary` and a `StateId`: expression graphs are stripped, shaders are in the compiled shader library. Channel meaning stays by field name only (`GroundMap`, `VelocityDepthFoamMap`, `HeightWetMap`).

## 24. Mechanics units (arm-class, seat-reduction arrays). FOUND

The cooked bytecode pseudo-code (`B_VehicleSeatDamageReduction`, `B_ArchetypeCaliberModifiers`, `B_BoneDamageModifiers`, `B_AmmoTypeEffectiveness`) gives the semantics: seat reduction values are **percents** (`return C * pct / 100`, the table stores negative values such as -25, so new damage = C x (1 + pct/100)); element struct is `FWDVehicleSeatDamageSourceEntry` (a `DamageSources` tag container and a `VehicleSeats` map tag to float); the row key is the victim's vehicle tag, the group is the first whose sources contain the projectile's `Meta.Damage.Arms.*` tag exactly. Archetype-caliber and bone modifiers are **multipliers** of the current damage (new = C x W, new = C x U x W). Armour reduction is a percent of the armour stage times the ammo scalar.

## Wiki updates

- `_wiki/vehicles/countermeasures-and-flares.md` -> "How flares are restocked is not yet known" -> "Flares are an inventory item (Flares, 750 cash in the vehicle vendor, one per purchase); the vehicle's flare count follows its inventory, so buying or being given the item adds that many flares and each use removes one". Keep "no flare rule that breaks a lock-on was found".
- `_wiki/vehicles/flakpanzer-gepard.md`, `t-72b3.md`, `l2a6.md`, `m113-apc-sv.md` and other tank pages: "how charges come back is not yet known" -> "smoke charges follow the vehicle inventory in the same way as flares (the item must be added to the vehicle); the data does not say what sells or gives smoke charges".
- `_wiki/vehicles/vehicle-handling.md`, the wheeled handling pages and `repair-and-vehicle-parts.md`: where a value is "not stored" for idle RPM, torque scale, steering sensitivity or torque share, replace with the native defaults: idle RPM 1,000 (WHL_02), torque scale 1.0 (Bobcat, Humvee), steering sensitivity 5.0 (Kodiak, Ural, Wolf-110), steer dead zone 0.01, axle torque share 0.5; tracked track mass 600 and sprocket mass 64 (Artillery, Heavy, TNK_04); "Boost" is stored but the boost switch is off in every asset (do not claim a boost effect).
- Tyre pages (`bobcat.md`, `humvee*.md`, `kodiak*.md`, `ural*.md`, `dune-buggy.md`): add that each tyre has three states: intact, damaged (at or below 55 percent of the wheel's health) and destroyed (0), with the radius, friction and brake values of the wheel data.
- `_wiki/vehicles/seats-and-passengers.md` -> "active versus passive passenger" gap -> "Only the M113's nine rear seats are passive passengers; every other passenger seat is an active passenger seat. The data gives both the same rules; the passive seats use a different pose."
- `_wiki/vehicles/vehicle-handling.md` "Gear order" -> keep "inferred": the last list entry is probably the reverse gear (the game's own default list has a larger last entry); not proven.
- `_wiki/equipment/drill-rig.md` -> "movement itself not read" -> "an activated rig shrinks the hot zone to 0.6 of its width and length (36 percent of the area) with the world default; how it moves the zone is not in the readable code".
- `_wiki/game-modes-and-maps/sniper-showdown.md` -> "faction count not yet known" -> "free-for-all: the game prepares 100 single-player factions and puts each player on the least-filled one; each map has 150 sniper-only loot points (87/21/42 on Kavkazi, 69/16/65 on North America, 79/19/52 on Russia, high/middle/low)".
- `_wiki/game-modes-and-maps/deathmatch.md` and `factions.md` -> "how a player is placed into a faction is not known" -> "Players choose Alpha or Bravo; the server places nobody automatically. Team-size locking is off by default; when on, a switch is refused if the target team would be 2 or more players larger than the smallest team".
- `_wiki/game-modes-and-maps/pve-scenarios.md` and the mission pages: add the extraction helicopter (a Littlebird with a dummy pilot flies 3 m/s along an entry path, waits for players to board, then flies the exit path); mission names stay placeholders; Strike and Disarm has 5 and VIP Escort 6 vehicle spawners; helicopter vendor speeds are km/h.
- `_wiki/game-modes-and-maps/maps.md` (or the map pages): playable areas Europe about 8.5 x 7.8 km, Kavkazi 11 x 11 km, North America 10.5 x 9.2 km, Russia 13.2 x 13.2 km; one world unit is 1 cm; killing ground at 1,500 m below.
- Team Offence page (`_wiki/game-modes-and-maps/team-offence.md` or the moderation page): add the notice texts and numbers of item 16 (15 points before a kick vote, 180 s relevance, 60 s self-defence window, bans of 10 min, 25 min, 1 h and 24 h, forgiveness after 7 days, a voter who left the safe zone is recorded as Forgive).
- `_wiki/weapons-and-explosives/` Molotov page: "extinguished by water" gap if any -> the Molotov explosion asks the water-height grid for the depth at the impact point (item 22).
- Pages that say a fluid, water or foam channel is "not yet known": keep as is (item 23 ABSENT).
