# Round 58: seven open wiki questions (R58-RE)

Static analysis only. Nothing was run. Evidence levels: cooked data read (JSON under `data/` and `assets/data/`), Blueprint bytecode read (extractor `dump`), static disassembly and decompiled-corpus reading (RVAs, image base 0x140000000). Extractor output lives under `E:/Reverse_Engineer/wardogs_analysis/round58_re/` (`fn_*/` name-map searches, `bat/` battery and range-finder Blueprints and item definitions, `ds/` destruction curve). Method as in round 57: find the open sentence, read the page, then trace the value with `round40_veh/rdis.py`, `rxref.py` and the corpus `calls` and `aliases` tables. No protected (virtualized) code was touched; no row below is PROTECTED.

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1a | Do flares break a lock-on | FOUND (no) | They do not clear a lock. They act on a missile already in flight: inside the flare band the missile re-aims at a flare point beside the helicopter, and near that point it drops its target. |
| 1b | Do flares stop a new lock | NATIVE | Helicopters report "cannot be locked on to" while flares are active (airplane never does); the reader of that flag was not found. |
| 1c | How long | FOUND | The flare active window (3.5 s on every flare vehicle in the data; native default 5 s), then a 5 s cooldown. |
| 1d | Does vehicle smoke touch lock-on | ABSENT | The smoke fire code never calls the targeting functions and carries no targeting field. |
| 1e | What removes a flare on a key press | FOUND | The fire handler removes one `Id.Item.Flares` from the vehicle inventory (smoke: the smoke item). |
| 2 | Sight value that reaches 3.25 | FOUND (derivation inferred) | The weapon's aiming zoom (magnification). The in-game setting text says "below 3.25x". |
| 3 | Meaning of the spread input | FOUND | Speed divided by the stance's full speed, clamped 0 to 1 (4.0, 2.5, 0.5 m/s). |
| 4 | L81 mortar -300 mrad travel time | ABSENT (cause); FOUND (unused) | No sight or Blueprint reads the travel time column; the reason for the round number is not stated. |
| 5a | Battery life | FOUND | A battery is a magazine of charges: 100 (Battery) and 250 (High Capacity). |
| 5b | "Reload" on range finder and drills | FOUND | Swaps the battery in the item's single battery slot (shared magazine reload). |
| 5c | Low battery sound | FOUND | Fires once when 20 or fewer charges remain while the range finder scope is in use. |
| 5d | Range finder drain | FOUND | 3 charges on raising the scope, then 1 charge per 0.8 s (1.25 per second). |
| 6a | Tracked gear lists | FOUND | The zero entry is neutral; entries before it are reverse, after it forward. |
| 6b | Boost path | FOUND | Holding the boost input swaps the torque scale for `BoostScale`, only if `bEnableBoost`; no vehicle enables it. |
| 6c | Second tracked engine curve | FOUND | The 1,400 at 1,911 curve (Dynamics asset) is the one the tracked engine evaluates; the first (Engine asset) has no runtime reader. |
| 7 | Destruction angle and distance curves | FOUND | Priority scores that order which destructible buildings the game refreshes first; angle in degrees, distance in game units. They do not change damage. |

## 1. Flares and smoke against lock-on

### What the earlier rounds tried

Rounds 42 and 46 looked for a flare read inside the lock code: the two lock Blueprints (`B_Action_Ads`, `B_Action_Vehicle_Weapon_Ads`), the lock-list accumulator `0x6A68DF0`, the readers of `bFlaresActive` (`+0x791`, only the getter `0x767A0B0` with UI callers) and the writers of the engine homing component. All negative, so flares were recorded as "no confirmed effect". They did not look at the **target side of the projectile guidance**, which is where the flare logic lives.

### The targeting interface

`IWDTargetableInterface` (SDK `WDGame_classes.hpp` line 61383) has seven functions. Their interface slots are fixed by the exec thunks (`0x7662010` and neighbours, `call [rax+N]`): `CanBeTargeted` +0x10, `GetTargetLocation` slot 3, `GetClearTargetWhenClose` +0x20, `GetClearTargetThresholdDistance` +0x28, `ShouldFollowTarget` slot 6, `CanBeLockedOnTo` +0x38, `GetNearMissBox` +0x40. The wrappers that the guidance function calls are named by their cached function names (initialiser `0x13B48E0..0x13B4988`, strings `0xB649588...`): `0x76619C0` CanBeTargeted, `0x7661A30` threshold distance, `0x7661AA0` clear-when-close, `0x7661B10` near-miss box, `0x7661C20` target location, `0x7661D00` should-follow.

The implementers are the vehicle classes. `AWDRotaryVehicle` vtable slots 392 to 398 and `AWDAirplaneVehicle` slots 389 to 395:

| Interface function | Rotary slot / address | Airplane slot / address | Behaviour |
|---|---|---|---|
| CanBeTargeted | 392 `0xD356F0` | 389 `0xD356F0` | always true |
| GetTargetLocation(projectile location, bool) | 393 `0x76B70B0` | 390 `0x76B33C0` | see below |
| GetClearTargetWhenClose | 394 `0x76B3300` | 391 `0x76B3300` | returns `bFlaresActive` (via `0x767A0B0`) |
| GetClearTargetThresholdDistance | 395 `0x76B32C0` | 392 `0x76B32C0` | targeting settings `+0x18` x 100 (`TargetingClearTargetThresholdDistance`, 100.0 on ROT_02/03/04, so 10,000 cm = 100 m) |
| ShouldFollowTarget(projectile location) | 396 `0x76B8080` | 393 `0x76B3D20` | false while the missile is inside the flare band |
| CanBeLockedOnTo | 397 `0x76B63B0` | 394 `0xD356F0` | **rotary: `not bFlaresActive`**; airplane: always true |
| GetNearMissBox | 398 `0x76B6F30` | 395 `0x5F80280` | rotary: from the targeting settings; airplane: an empty (invalid) box, `mov byte [rdx+0x30], 0` |

### What the guidance function does with them

`0x6F2E620` (guidance, read by round 47) is fed the projectile record by `0x76D8A00` (record target `+0xF8`, flag byte `+0x100`). The per-tick updater `0x6F3D690` stores `ShouldFollowTarget(projectile location)` into `record +0x100` (call `0x6F3D70E`).

- **ShouldFollowTarget** (`0x76B3D20`, airplane copy; rotary `0x76B8080` has the same structure): distance from the projectile to the vehicle (`0x1DA61A0` = actor location), compared with `FlaresEffectiveRangeMin`/`Max` (targeting settings `+0x6C`/`+0x70`, multiplied by 100 at `0x9AC21F0`). It returns `not (min <= d <= max)`. It does **not** test whether flares are active.
- **GetTargetLocation** (`0x76B33C0`, rotary `0x76B70B0`): if the bool argument (the record flag from ShouldFollowTarget) is true **or** flares are not active, it returns the normal target location. If the argument is false and `bFlaresActive` is true it transforms the two flare offsets (`FlaresLeftTargetLocationOffset`, `FlaresRightTargetLocationOffset`, settings `+0x80` and `+0x98`) by the vehicle transform and returns whichever of the two is nearer the projectile (`comiss`, `cmovbe` at `0x76B3777`). `settings +0x168` (`bDebug`) only draws debug shapes.
- **Clear when close** (`0x6F2E620`, `0x6F2E940..0x6F2E9A3`): when `GetClearTargetWhenClose` (flares active) is true and the distance from the projectile to the returned location is below the threshold, the target record is removed (`0x6F34110` find, `0x6F30860` clear). The missile stops steering.
- Guidance only acts while the motor thrusts (round 47), and only three projectile assets are guided at all (`assets/data/r46-guidance.json`: 72 mm, 70 mm, a debug rocket).

Data (cooked, `DA_GameplaySystems_ROT_02/03`, [`DA_ROT_04_GameplaySystems`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/Data/DA_ROT_04_GameplaySystems.json)): flare points left and right of the vehicle at Y = +/-700 cm, Z = 200 cm (Havoc), +/-400, 200 (MH-6 family), +/-500, 350 (Z20); `FlaresEffectiveRangeMin`/`Max` 5/300 (Havoc), 10/300 (MH-6 family), 15/300 (Z20) metres; `FlaresActiveTime` 3.5 s; `TargetingClearTargetThresholdDistance` 100.0. The airplane asset sets only `StartingFlaresAmount` 3 and `FlaresActiveTime` 3.5; its flare points and range use native defaults (range 25 to 100; offsets not read), so where its flares pull a missile is not known.

### Answers

- **1a. Do flares break a lock?** No lock is cleared (nothing writes the lock lists from the flare code). The visible effect is on the **missile in flight**: inside the band the missile re-aims at a flare point; within about 100 m of that point it gives up its target. FOUND (static disassembly; not run).
- **1b. A new lock.** The rotary class returns `CanBeLockedOnTo = not bFlaresActive`; the airplane returns true. The name map has no Blueprint caller (findname for `CanBeLockedOnTo` and `ShouldFollowTarget` matches 0 packages; the FName cell `0xD3B0F50` has no reader in code), and no native caller was located (a scan of the lock manager range found none). So a helicopter is marked unlockable while its flares burn, which matches the in-game tip, but what consumes the flag is **NATIVE, not found**. Inferred, not proven.
- **1c. How long.** `FlaresActiveTime` (3.5 s all flare vehicles in the data), then a 5 s cooldown (rounds 39 and 42). The diversion only exists while `bFlaresActive` is true.
- **1d. Smoke.** `0x766F240` (smoke fire) calls only the net-mode check, the inventory removal, replication marks, the cue and timers (callee list from the corpus `calls` table); it never calls a targeting wrapper, and the smoke settings struct has no range, offset or lock field. ABSENT. Smoke clouds act on sight through the smoke blocker actors (not traced further).
- **1e. Key press.** `0x766EDF0` (flare fire, skipped when the net mode is Client, value 3) requires the cooldown flag and a count above 0 (`+0x790`), then unless the developer flag at `0x15F1E20/0x15F1DE0` is set calls `0x679E540(inventory, +0x2C0 flares tag, mode 2, count 1)`. `0x679E540` wraps `0x678BD80`, the same core that `RemoveItemFromInventory` (`0x67AAC50`) calls, so it is **one item removed**. If the removal fails the fire aborts. The smoke twin `0x766F240` does the same with the smoke tag (`+0x350`) and its own flags (`+0x7B4`, `+0x7BC`). The count then follows the inventory through `OnItemRemoved` (round 45). FOUND.
- **Verba, Talon and Stingray.** They share the lock Blueprints (round 42) and the same projectile guidance; the 72 mm rocket (Verba, Talon) is guided with constant 30 and max turn 10 (round 46). No weapon-specific flare or smoke rule exists in their data. Whether the Stingray's rocket is one of the guided assets was not re-checked here.

## 2. The sight value that reaches 3.25

Round 46 found `base = 72` when weapon component `+0x3F4` is 3.25 or more, set by `0x6B879E0` from `max(<float at +0x3F8 of the object at handler +0x438>, <float at handler +0x454>)` in the ADS multiplier attribute handlers (`0x6C99E52`, `0x6C9A902`). New reading:

- The same handler first writes `+0x3E8` (`0x6B879A0`) and the ADS multiplier base `+0x3F0` (`0x6B87960`), which also writes `+0x3F8 = base + base * (+0x400) * (+0x404)` (zoom plus focus bonus). So `+0x3F8` is the weapon's **aiming zoom including the focus bonus**, and `+0x3F4` is the larger of that zoom and a second stored float.
- The user-facing text agrees: [`DT_Settings_General`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Settings/General/DT_Settings_General.json), `UserSettings.General.FieldOfView.AimingMode`: "Affected: ADS FOV is based on the user's FOV setting at low magnification levels (below 3.25x)" (round 40).
- So: the value is the sight magnification. A sight of 3.25x or more uses 72 degrees as its base even in Affected mode. The weapon-data sights above 3.25x are the 4x and larger scopes (the sights page lists 29 zoom values from 1.2 to 6).

FOUND for the meaning (cooked option text plus handler structure). Inferred: that `+0x3F4` is exactly the zoom (the second float, handler `+0x454`, and the object at handler `+0x438` were not identified). Side effect for the wiki: the "4x on 90 degrees gives 22.5" example was wrong for Affected mode, a 4x sight uses 72/4 = 18 degrees.

## 3. The spread input

`pipelines/Wardogs_WeaponSpread_v1.md` section on `UpdateSpread` (round 41) already holds the proof: `x = clamp(v / vref, 0, 1)` with `v` the 2D speed (cm/s) and `vref` = {50, 250, 400} cm/s for prone, crouch, stand (static array set at `0x6CA01F7`); curve value = `Value x CT_Weapon_Spread[row](x)`; then `S' = FInterpTo(S, SpreadMultiplier x curve, dt, 25)`. The wiki page only said "what the 0 to 1 input measures is not traced". Vehicle-mounted weapons evaluate the same row at level 0 (input 0). FOUND (static, round 41; closed on the wiki here).

## 4. L81 mortar -300 mrad travel time

`WE_STN_03_Heavy_MainBarrel.ArtilleryRangeData` rows (`FWDArtilleryRangeEntryData`: Milliradians, ImpactDistance, TravelTime). Readers: the mortar reticle `W_STN_03_Reticle` reads Milliradians (+650 label) and ImpactDistance only; round 36 showed the SPH-2 widget reads neither. This round: the reticle bytecode contains no `TravelTime` (checked in `round36_combat/d4/W_STN_03_Reticle.json`: `ImpactDistance` once, `TravelTime` zero times), and a name-map search for `TravelTime` over all Wardogs packages matched 10 packages: three audio assets and the projectile Blueprints (`BP_120x800mm`, `BP_155mm_Standard`, `BP_122mm`, `BP_93mm`, `BP_Arrow`), which use the **runtime** `GetExpectedTravelTime`/`GetCurrentTravelTime`, not the table. No Blueprint reads the table column. A native reader was not excluded (struct copies), but none of the visible paths uses it.

So the 20.0 s at -300 mrad (and 22.0 at +300) sits in a column the sight does not show and no Blueprint reads. Why the value is a round number is not stated by any file. Status: unused as far as read (FOUND), cause ABSENT.

## 5. Batteries, the "reload" action and the low battery sound

Items checked: [`ID_Battery`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Battery/Content/Data/ID_Battery.json), [`ID_LrgBattery`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Battery/Content/Data/ID_LrgBattery.json), [`ID_Battery_Charge`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Battery/Content/Data/ID_Battery_Charge.json), [`ID_RangeFinder_Expensive`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/RangeFinder/Content/Data/ID_RangeFinder_Expensive.json), [`ID_HeavyDrill_RepairTool`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/VehicleRepairTool/Content/Data/ID_HeavyDrill_RepairTool.json), [`ID_LightDrill_RepairTool`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/VehicleRepairTool/Content/Data/ID_LightDrill_RepairTool.json), [`ID_Defibrillator_Standard`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Defibrillator/Content/Data/ID_Defibrillator_Standard.json), `B_Action_RangeFinder_ADS`, `B_Action_VehicleRepairTool_Continuous`, `B_Action_VehicleRepairTool_Reload` (dumps under `round58_re/bat/`).

- **Battery life.** A battery is an **inventory magazine**: [`ID_Battery`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Battery/Content/Data/ID_Battery.json) has context `Item.Attachment.Magazine.Battery` and a hidden `Item.Ammo` container allowing only `Id.Item.BatteryCharge` ("Charge", stack 100). `MaxSlotAmountStackSize` is **100** (Battery) and **250** ([`ID_LrgBattery`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Battery/Content/Data/ID_LrgBattery.json)), and `DefaultContainerItems` is one BatteryCharge with `Amount` unset; the same pattern on a 30-round rifle magazine ([`ID_AK74M_Mag_Standard`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Attachments/Magazines/AR/AK74M_Mag_30rd/ID_AK74M_Mag_Standard.json), stack 30) means a new one is full. The defibrillator page already used 100 and 250. Drills: the continuous action's Hit notify calls `WDItemExtension_Battery::UseCharges(ChargesToUse)`; `ChargesToUse` = 1 on both drills (`ID_*Drill_RepairTool` line 16). `UseCharges` (`0x8556C80`) removes `min(n, remaining)` charges (`0x679E570`). `ChargesPerSecondConsumption` 1.25 on both drills has no reader in the battery extension (its vtable has no overrides) and the repair action does not use it; a per-second drain for the drills was not found. A repair swing therefore costs 1 charge; the swing rate (drill page: 0.5 s Heavy, 0.75 s Light) is not proven to be the Hit rate. FOUND for capacity and per-hit cost; per-second life inferred.
- **"Reload".** [`DA_Action_RangeFinder_Reload`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/RangeFinder/Content/Data/Actions/DA_Action_RangeFinder_Reload.json) runs `B_Action_Reload` (round-by-round shared magazine reload); the range finder, the drills and the defibrillator each have one `Item.Attachment.Magazine` container, size 1, allowing `Item.Attachment.Magazine.Battery`, default content `Id.Item.Battery`. The drill's reload Blueprint calls `B_Action_Reload.BP_CanActivate` and plays the reload montages. So the action **swaps in a fresh battery**. FOUND.
- **Range finder drain and the low battery sound.** The range finder's `WDItemExtensionData_Battery` says 0 per second, but the optic is a `WDItemExtension_PrototypeMaskedScopes` and **that** extension runs its own battery logic. The data class constructor defaults (`0x862EF6A..0x862EF92`): `+0xBC` = 3, `+0xC0` = 1, `+0xC4` = 1.0 s, `+0xC8` = 20. The cooked range finder overrides only `+0xC4` (0.8) and the scope count, so the rest are the defaults. `0x86342E0(active)`: starting sets a looping timer with period `+0xC4` and first calls the tick with `+0xBC` charges; the timer callback (`0x8633170`) calls the tick with `+0xC0`. The tick `0x8631E90`: on the authority (`0x675CE10`, role value 3) it spends the charges through `0x8556C80`; then reads the remaining charges (`0x8556B90`); if the warning has not yet fired this use (`this+0x127`), the remaining count is above 0 and **at or below `+0xC8` = 20**, it sets the flag and broadcasts the battery-low delegate; if the battery has no charge left it calls `0x86342E0(0)` (stop). `B_Action_RangeFinder_ADS` binds that delegate (`OnBatteryLow`) to the `Audio.Event.Item.RangeFinder.LowBattery` request and stops the sound with the `.Stop` event on cancel and complete. Result: 3 charges on raising, then 1 charge per 0.8 s (1.25 per second): about 78 s from a full Battery and about 198 s from a full High Capacity Battery; the warning starts at 20 charges, about 16 s before empty. FOUND (static, defaults read from the constructor, not run).

## 6. Vehicle gear and boost paths, second tracked engine curve

- **Tracked gears.** At begin-play (`0x539BBB0`, loop `0x539BCCE..0x539BD05`) the tracked component scans the Dynamics asset's `Gears` (array at asset `+0xD8`, stride 12 bytes: ratio, down ratio, up ratio) for the **first entry whose ratio is exactly 0**, stores that index as the neutral index (`+0x448`) and starts in the next gear (`+0x44C`, `+0x450`). The displayed gear number is `abs(current - neutral)` (`0x5397530`); `0x539825A` returns 0 when the current gear is below neutral. So entries before the zero entry are reverse and entries after it forward. Cooked lists: TNK_01 and SPW `[5, 0, 8, 6, 2.65]` (reverse 5, neutral, forward 8, 6, 2.65), TNK_04 `[5, 0, 8, 6, 3.6]`. The "10" and "7" gear counts on the wiki are the Engine asset lists, which are not live (below). FOUND (the "before the zero entry is reverse" half rests on the convention plus `abs()` display, inferred).
- **Boost.** The wheeled setup `0x536EDF0` copies the asset engine block into the component: torque scale to `+0x4F8` (and a backup to `+0x558`), `bEnableBoost` to `+0x521`, `BoostScale` to `+0x554`. The input function `0x535ED00` (called from `0x5356047`), `0x535EE51..0x535EE71`: only if `bEnableBoost` is set, it writes `+0x4F8` = `BoostScale` when the boost axis (`RawBoostingInput`, input struct `+0x48`) is above 0, and the backup (normal torque scale) otherwise. So boost **replaces** the engine torque scale while the input is held. Every wheeled asset leaves `bEnableBoost` false (round 45), so no cooked vehicle boosts. FOUND. The tracked `BoostScale` (EngineData `+0x10C`) has no reader (below).
- **Second tracked engine curve.** `UMTrackedVehicleMovementComponent` holds only the Dynamics asset (`+0x3C0`; at begin-play it is copied to `+0x430`). The engine update `0x53ABAB0` evaluates `Dynamics + 0x38` (`EngineTorqueCurve`) at the current RPM (`+0x4B0`) with `0x3E07720`, multiplied by `TorqueMultiplier` (`+0xC0`), and uses `MaxRPM` (`+0xF4`). The Engine asset (1,800 at 1,400, M113 2,500 at 1,200) is referenced only by the config (round 41) and none of its distinctive fields (`EngineExtraPowerRatio +0x108`, `BoostScale +0x10C`, `ChangeTime +0xE4`, retarder ratios) is read together in the tracked code range. So the **live curve is the one the wiki called the "second" (1,400 at 1,911 RPM)**, and the first curve and the Engine asset gear lists are not evaluated by the tracked component as far as read. NATIVE-leaning FOUND: no reader found, a pawn-init copy was not excluded.

## 7. Destruction angle and distance curves

The two curves ([`CF_DestructionBuildingAngleScore`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Destruction/CF_DestructionBuildingAngleScore.json), [`CF_DestructionBuildingDistanceScore`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Destruction/CF_DestructionBuildingDistanceScore.json)) are the `AnglePrioritizationCurve` and `DistancePrioritizationCurve` of `UBHDestructionTailorSettings` (SDK `BHDestructionTailor_classes.hpp`; neighbouring settings `AngleScoreMultiplicationWhileScoping`, `BuildingUpdatesPerFrame`, `UpdateStepDistance`) and live in the subsystem at `+0x1E0` and `+0x1D8`. They are not in `BHDestructionSettings`, which is why round 45 found no consumer there. The scorer is `0x64F1C40`:

- for each tracked building it builds the camera-to-building direction, takes the dot product with the view direction, `acos` (`0x98F814C`) and multiplies by 57.2958 (`0x9AD4834`), so the **angle is in degrees** between the view direction and the building;
- the **distance** is the 3D camera-to-building length in world units;
- score = `AngleCurve(angle)` (multiplied by `AngleScoreMultiplicationWhileScoping`, `settings +0xB0`, while the camera zoom `subsystem +0x54` is above 1) plus `DistanceCurve(zoom x distance)` (`0x3E07720` at `0x64F21D9` and `0x64F2204`), stored per building (`+0x110` array) and sorted by `0x64ECFF0`; `BuildingUpdatesPerFrame` (settings `+0xB8`) buildings are then refreshed per frame in that order.

So the curves are a **refresh priority**: the angle curve gives 0.7 straight ahead falling to 0 at 100 degrees, the distance curve 1.0 up to 2,000 units falling to 0.5 at 50,000 and 0.1 at 75,000 (so 20 m, 500 m and 750 m if the unit is centimetres, which is inferred from the engine's usual unit and the 100 scale used elsewhere). They do not scale damage or force; the force thresholds are the separate `1,200` and `400` settings (round 45). What the refresh does to a building (visual state, collision, remnant swap) was not traced. FOUND for the meaning; effect of the refresh NATIVE.

## Not done

- The reader of `CanBeLockedOnTo` and what it does to an existing lock (1b).
- Where the airplane's flare points sit (native defaults of `FWDFlaresSettings` offsets).
- The second float and the object behind the 3.25 value (2).
- A per-second drain for the drills, if any (5).
- A pawn-init copy of the tracked Engine asset (6).

## Wiki updates (done in this commit)

- `_wiki/vehicles/countermeasures-and-flares.md`, `_wiki/guides/vehicle-guide.md`, `_wiki/guides/faq.md`, `_wiki/building/talon-9k-sam.md`, `_wiki/building/stingray.md`: what flares do to missiles and locks, smoke, the key press.
- `_wiki/attachments/sights-and-optics.md`, `_wiki/game-mechanics/controls-and-settings.md`: the 3.25 magnification rule and a corrected example.
- `_wiki/game-mechanics/spread-and-recoil.md`: the spread input.
- `_wiki/building/l81-mortar.md`: the -300 row.
- `_wiki/equipment/batteries.md`, `infrared-range-finder.md`, `drills.md`, `defibrillator.md` (cross-check): battery capacity, reload, drain, low battery.
- `_wiki/vehicles/vehicle-handling.md`: tracked gear order, boost, the live tracked curve.
- `_wiki/game-mechanics/destruction.md`: the two curves.
