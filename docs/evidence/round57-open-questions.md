# Round 57: seven open wiki questions (R57-RE)

Static analysis only. Nothing was run. Evidence levels: cooked data read (JSON under `data/` and `assets/data/`), Blueprint bytecode read (extractor `dump`), static disassembly and decompiled-corpus reading (RVAs, image base 0x140000000). Extractor output lives under `E:/Reverse_Engineer/wardogs_analysis/round57_re/` (`bw/` barbed wire Blueprints, `fe/` fuel economy widget, `fn1/` name-map search, `tools/bcsum.py` bytecode summariser). No protected (virtualized) code was touched; no row below is PROTECTED.

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1 | Which seat fires the miniguns | FOUND | Humvee: the Gunner seat (seat index 1). AH-6M: the Driver (pilot). Z20: two Gunner seats (index 2 right gun, index 3 left gun). |
| 2 | Hot Potato pass multiplier growth | FOUND | Starts at 1, +1 per pass; no cap found. Also fuse = random(8..15) x 0.85^multiplier. |
| 3 | Team Offence 180 s | FOUND (inferred use) | Vote deadline = offence time + 180 s, sent to the voter prompt, which closes at it. |
| 4 | Revived-by-enemy state | FOUND | No effect on the revived player; it makes killing them worthless (cash x0.01, no Role XP, no assist XP, "No Value Kill", wagers ignore). |
| 5 | Barbed wire trigger | FOUND | Standing inside the wire's trigger box: 8 damage per 0.4 s on foot, wheel damage to moving wheeled vehicles, slow effect 7.5%. |
| 6 | Fuel economy direction | FOUND | Vendor label is "Fuel Economy (L/KM)": higher = more fuel per km (worse). |
| 7 | AI hearing alert amount | FOUND (data) | No fixed per-sound "alert amount". Hearing adds to detection by strength (existing formula); the alert map has Strength 1.0, radius 1000, decay 1%/s, update 0.5 s. |

## 1. Miniguns: which seat fires

Status FOUND (cooked data). Each armed variant has a `WD_MVF_WeaponFragment` inside its weapon part, with `RoleRequirements.RequireTags` and an `AllowList` of seat indices. The seat list comes from the variant's seat settings asset (`assets/data/vehicle-seats.json`).

| Vehicle | Part asset | RequireTags | AllowList (seat index) | Seat data |
|---|---|---|---|---|
| Humvee [Minigun] | `WHL_05_Minigun/Parts/VP_WHL_05_Humvee_RingMinigun` (fragment `WD_MVF_WeaponFragment_0`) | `State.Player.Vehicle.Role.Gunner` | `[1]` | [`DA_SeatSettings_WHL_05_Humvee_Minigun`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05/Content/Data/Minigun/DA_SeatSettings_WHL_05_Humvee_Minigun.json): 0 Driver, 1 Gunner (`bIsGunner`, `bShouldAutoEnterGunner`, exterior seat, idle pose `A_TP_Humvee_Turret_Minigun_Idle_Pose`), 2 to 4 ActivePassenger. Five seats, matching the shop's five. |
| AH-6M [Miniguns] | `ROT_03_WeaponVariants/Parts/VP_ROT_03_MachineGuns_Weaponry` (fragment on [`W_ROT_03_AttachedMachineGuns_Grouped`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/Weapons/W_ROT_03_AttachedMachineGuns_Grouped.json), tag `Miniguns`) | `State.Player.Vehicle.Role.Driver` | `[0]` | [`DA_ROT_03_Attack_SeatSettings`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/Data/WeaponVariants/DA_ROT_03_Attack_SeatSettings.json): 0 Driver, 1 ActivePassenger. No Gunner seat exists, so the pilot fires both guns. The weapon asset lists both muzzle sockets (`muzzleFlash_WeaponExtension_L`, `_R`) under one grouped weapon. |
| Z20 Lakota [Miniguns] | `ROT_04_MachineGun/Parts/VP_ROT_04_MountedMachineGun_R` and `_L` | `State.Player.Vehicle.Role.Gunner` | R: `[2]` (and `TargetInventoryIndex` 1); L: `[3]` | [`DA_ROT_04_SeatSettings_MachineGun`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04_MachineGun/Content/Data/MachineGun/DA_ROT_04_SeatSettings_MachineGun.json): 0 Driver, 1 ActivePassenger, 2 and 3 Gunner (auto-enter), 4 to 12 ActivePassenger. 13 seats. |

Reproduce: grep `RequireTags` / `AllowList` in the three part files under [`data/Wardogs/Plugins/GameFeatures/Vehicles/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Vehicles). The left/right naming of seats 2 and 3 follows the part names (`_R` allows 2, `_L` allows 3); which of those seats a player sees as "left" is not read.

## 2. Hot Potato pass multiplier

Status FOUND (static, decompiled corpus plus disassembly). `0x863AA90` is not the growth function: it is the **getter**. It walks the potato component's replicated fragment-data list, finds the entry of class `WDFragmentReplicatedData_HotPotato` and returns its first `uint32`; it returns 1 when the entry is absent. The real chain:

- `AWDHotPotatoThrowable` constructor `0x8636F60` sets the throwable's own counter (`+0x610`, decimal 1552) to **1**.
- At throw time a function in the same class (decompiled corpus `workers/04/code/086.c`, around line 7486) sets the thrown actor's `+0x610` to the result of the getter `0x863AA90` for the thrower's potato (1 when none), so the thrown potato carries the holder's multiplier.
- Hit handler `0x863ADA0` (once per throwable: it sets the byte at `+0x614`, decimal 1556, then calls the setter): for the player the potato reaches it calls `0x8638D40(component, throwable.+0x610 + 1)`. `0x8638D40` writes the value into the replicated fragment data (`*data = a2`, marked dirty), then calls `0x8638EE0`.
- So **multiplier = previous multiplier + 1 on each pass**, starting at 1. No clamp is applied in `0x8638D40` or `0x863ADA0`. Award per pass stays 5 x (multiplier x 2) = 10 x multiplier (round 39).
- `0x8638EE0` (restart timer): `t = rand(min(F48, F4C), max(F48, F4C)) x pow(F50, multiplier)` with the constructor floats 8.0, 15.0 and 0.85 (`WDItemExtensionData_HotPotato`, `0x8637170`), i.e. the base-0.85 power uses the multiplier as exponent (call to the pow import stub `0x98F80DA`). The timer calls `0x86377A0` when it ends, which builds a damage-style context against the holder (`0x144C46820(holder, ...)`); that the end of the timer penalises the holder is **inferred**, the amount was not decoded.

Examples (derived): multiplier 1 gives 6.8 to 12.75 s, 2 gives 5.8 to 10.9 s, 5 gives 3.5 to 6.7 s.

## 3. Team Offence 180 s

Status FOUND, use inferred. `WDTeamOffenceSettings` constructor `0x8936700`: `+0x44` = 180.0 (`OffenceRelevanceSeconds`; the other fields: `+0x38` 900.0, `+0x3C` 3, `+0x40` 0.5, `+0x60` 60.0, `+0x64` 15.0). The settings getter is `0x8936630`. Two readers of `+0x44` exist: `0x893C7B0` (offence-recording function, ballot creation) and the function around `0x893CC49..0x893CD08` (same pattern). Both store `settings.+0x44 + event time` (float at `+0x10` of the offence descriptor) as a **double at `+128` of the 152-byte ballot record**. `0x893AD40` sends that `+128` value to the voter in the vote payload; the client prompt tick `0x893E180` computes `deadline - now` and closes the prompt (`0x1475EC590`) at or below 0. So the 180 s is the vote's life. Not read: whether the server also cancels the ballot at the same deadline (the "voter expired" notice suggests it).

Side finding (round 45 flagged "by name only"): `0x893BA80` gives a voter's weight: if the voter's recorded approvals reach `ApprovalsPerSessionToFlag` (`+0x3C` = 3) the weight is `FlaggedVoterWeight` (`+0x40` = 0.5), otherwise 1.0.

## 4. Revived-by-enemy state

Status FOUND (cooked data). `GE_Player_RessedByEnemy`: Duration 60 s, **no modifiers**, grants `State.Player.RessedByEnemy` (`assets/data/ge-values.json`). So it changes nothing about the revived player. Consumers of the tag / the context tag `Challenges.Context.RessedByEnemy` (added in [`ST_Challenges_SessionEvents_KOTH_PlayerKill`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/ST_Challenges_SessionEvents_KOTH_PlayerKill.json) when the victim carries the state tag):

- [`DT_ChallengeRewards_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_SessionEvents_Shared.json), row `Challenges.Rewards.PlayerKill`: Cash selector `FriendlyModifier` picks `RessedByEnemyFactor` = **0.01** (kill cash x0.01); Role XP selector `BaseReward` picks `RessedByEnemyFactor` = **0.0**. Row `Challenges.Rewards.PlayerKill.Assist`: Role XP `BaseReward` picks `RessedByEnemyReward` = **0.0**.
- [`ST_Challenges_Challenge_RewardedKills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/StateTrees/ST_Challenges_Challenge_RewardedKills.json): the context is in the list with `Diminished` and `FriendlyKill`.
- Reward feed [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) (`Challenges.Rewards.PlayerKill.RessedByEnemy`): text "No Value Kill". [`DA_HUDFeedback`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/HUDFeedback/Data/DA_HUDFeedback.json) also has a conditional on the tag.
- Wagers: [`DT_WagerActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerActions.json) rule "Not a player an enemy revived".

## 5. Barbed wire trigger

Status FOUND (Blueprint bytecode). `B_Buildable_BarbedWire` has a `WDBuildable_ActorSpawnLocation` with `ActorToSpawn = B_BarbedWire_Damage_Volume`. That actor (a `WDTriggerVolume` subclass) has a box `TriggerVolume` (extent 16, 30, 70, scale 2.4, 4.5, 1.0; a "Moveable" variant extent 16, 30, 50) and these defaults: `FlatPlayerDamage` 8.0, `PercentageVehicleDamage` 10.0, `MinimumVehicleHealthPercent` 15.0, `EffectsToApply = [GE_Player_BarbedWireSlow x1]`, `ActorAllowList = [WDMoverCharacter, BHBaseVehiclePawn]`, `bPeriodicQueries` false.

- `OnEnterTriggerVolume` (calls native `WDTriggerVolume::OnEnterTriggerVolume`), adds the actor to `ActorsArray` and, if no timer yet, sets a **looping 0.4 s timer** (`K2_SetTimerDelegate(delegate, 0.4, true, 0, 0)`) calling `OnActorsArrayLoop`. `OnExitTriggerVolume` removes the actor and clears the timer when the array is empty.
- `OnActorsArrayLoop`: for a `WDMoverCharacter`, `TryDamagePlayer` (needs tag `State.Player.Vitality.Alive`; characters in a vehicle are skipped by `K2_IsDisallowedActor`): `SimpleDamageActor(..., Meta.Damage.DamageType.Enviroment, FlatPlayerDamage 8)`, with the buildable owner's controller as instigator when the wire is a buildable; then a camera shake (2.0) and an audio event. For a `BHBaseVehiclePawn`: only if the vehicle's velocity is not nearly zero (1.0) and it does not carry `State.Player.Vehicle.Tracked` or `.Rotary` (`IsDamageResistantVehicle`), `TryDamageVehicle` applies `ApplyDamage` to each wheel health section (`Attribute.Gameplay.Health.Wheel.*`) of `maxSectionHealth / 100 x 10` while the section is above 15 percent.
- The slow effect `GE_Player_BarbedWireSlow` (override of `Attribute.Gameplay.Movement.MaxSpeedMultiplier` to 0.075) is only named in `EffectsToApply`; the Blueprint itself never applies it, so the application is done by the native `WDTriggerVolume` (inferred, not disassembled). Whether it also slows vehicles is not known.
- Not read: whether the damage skips the builder's team.

## 6. Fuel economy direction

Status FOUND (cooked UI data). `W_VehicleVendor_Stat_FuelEconomy` `TitleText` = `STRINGS_VehicleVendor_Stats` key `VehicleStats.Title.FuelEconomy`, "Fuel Economy (L/KM)". `W_VehicleVendor_Stat_FuelCapacity` = "Fuel Capacity (L)". Litres per kilometre: a higher value uses more fuel (worse). Consistent with the values: Bobcat 2.2, SUV 2.9, Humvee 3.3, Ural/Wolf 4.0, helicopters 4.4, dune buggy 5.0, M113 5.7, tanks 8.0 to 10.0. The engine's actual fuel burn in play was not traced; the number is the vendor-listed stat.

## 7. Soldier hearing alert amount

Status FOUND (data); native application not traced. Searched `HearingAlert`, `AlertAmount`, `SoldierHearing` in all cooked data and `assets/data`: no such field. What exists:

- Detection (round 41): hearing strength per second = detectability x (1/x^2 - 1) x 0.05 with detectability 5.0 for gunfire and 1.0 for a vehicle occupant. Alert is reached at detection 0.8 (round 42). So a shot inside about 450 m fills detection in under a second.
- Alert map ([`AIInfluence_DataConfig`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/DataAssets/AIInfluence_DataConfig.json)): `InfluenceMap.AlertMap` Radius 1000.0, **Strength 1.0**, `SensesToUseForAlertMap = [AISense_Hearing]`. [`WDInfluenceConfigData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/InfluenceMap/WDInfluenceConfigData.json): alert map `DecayPercentagePerSecond` 1.0, `InfluenceMapUpdateFrequency` 0.5, `PropagateInfluence` false, `CreateArea` true. Team map: radius 1000, strength 1.0, decay 10, update 5.0. Enemy map: radius 500, strength 1.0, decay 10, update 2.0. The alert map feeds [`EQS_FindSearchLocation`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Search/Content/EQS/EQS_FindSearchLocation.json) (`WDEnvQueryGenerator_GenerateInfluenceLocations`, evaluator `BP_InfluenceEvaluator_AlertLocationGenerator`).
- Radius unit (cm or other) is not confirmed. The native code that writes a hearing stimulus into the map was not located.

## Wiki updates (done in this commit)

- `_wiki/vehicles/humvee-minigun.md`, `ah-6m-miniguns.md`, `z20-lakota-miniguns.md`, `vehicle-weapons.md`, `seats-and-passengers.md`: which seat fires the miniguns.
- `_wiki/game-modes-and-maps/hot-potato.md`: multiplier growth and the fuse.
- `_wiki/game-modes-and-maps/team-offence.md`: what 180 s does.
- `_wiki/game-mechanics/downed-and-revive.md`, `status-effects.md`: revived-by-enemy; barbed wire slow trigger.
- `_wiki/building/barbed-wire.md`: trigger box, damage, slow.
- `_wiki/vehicles/fuel-and-refueling.md`: fuel economy direction.
- `_wiki/game-modes-and-maps/ai-enemies.md`, `_wiki/guides/pve-guide.md`: hearing amount and influence maps.
