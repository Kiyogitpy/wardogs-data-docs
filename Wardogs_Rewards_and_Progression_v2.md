---
title: "Rewards & Progression"
nav_order: 2
---

# Wardogs — Rewards & Progression Reference (v2, corrected)
*Extracted from cooked game data (build `++Wardogs+Live-CL-516586`, UE 5.7.4). All numbers below come directly from the game's own DataTables.*

> **Correction note:** v1 of this doc pulled from [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json)/[`DT_CashRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_CashRewards.json) — those tables turned out to be **stale/placeholder** (nearly everything reads `0`). The real, live numbers live in a separate, much bigger family of per-category tables (`DT_Reward_Cash_*`, `DT_ChallengeRewards_*`) under [`CashRewardsDataTable/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable). This version replaces those zeros with the actual base values, including per-item, per-vehicle, and per-buildable breakdowns that weren't in v1 at all.

---

## Season 02 update (2026-10-15)

- **Role Mastery XP curve changed** for all six roles, which still share one curve. Level 10: 35,000 → 25,000. Level 20: 250,000 → 111,500. Level 50: 1,500,000 → 1,150,000. Level 100: 6,000,000 → 5,132,500. Levels 0 to 9 are unchanged. See [section 1](#1-role-mastery-xp-curve-updated-in-season-02).
- **New tank variant:** [`TNK_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/TNK_04.json) (Default) destroyed pays a base of 5,000. See [section 5a](#5a-vehicle-destroyed-dt_reward_cash_vehicledestroyed).
- **New faction bonus row:** `FactionWinBonus` in the end-of-match challenge data. Alpha 10,000, the other alignment tags 0. See [section 10](#10-end-of-match-challenge-rewards-dt_challengerewards_endofmatch).
- **Supply crate session rewards:** DeploySupplyCrate literal 250 → 125. DestroySupplyCrate (Free) 250 → 150. PlayerDelivered 150 → 100.
- **Vehicle session rewards** (per-kill calculator data, not in the tables below): TNK_01 Artillery 14,000 → 8,000. TNK_01 AntiAir 10,000 → 3,500. MistralAA 2,000 → 650. Phalanx 3,000 → 1,200. Mortar 300 → 650.
- **Supply crate XP curve:** [`CRV_Challenges_Curves_PurchaseFromSupplyCrate_XP`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_PurchaseFromSupplyCrate_XP.json) key 2 time 75 → 10.
- **New challenge state trees (4):** [`ST_Challenges_Challenge_PassengersDelivered`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/StateTrees/ST_Challenges_Challenge_PassengersDelivered.json), [`ST_Challenges_Challenge_RewardedKills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/StateTrees/ST_Challenges_Challenge_RewardedKills.json), [`ST_Challenges_Challenge_RewardedRevives`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/StateTrees/ST_Challenges_Challenge_RewardedRevives.json), and [`ST_Challenges_Challenge_RewardedVehiclesDestroyed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/StateTrees/ST_Challenges_Challenge_RewardedVehiclesDestroyed.json). Not yet covered in the tables below.
- **New supply crate curves (2):** [`CRV_Challenges_Curves_DeploySupplyCrate_XP`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_DeploySupplyCrate_XP.json) and [`CRV_Challenges_Curves_DestroySupplyCrate_Cash`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_DestroySupplyCrate_Cash.json), referenced by [`DT_Challenges_Curves_PurchaseFromSupplyCrate`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/DT_Challenges_Curves_PurchaseFromSupplyCrate.json).

---

## 1. Role Mastery XP Curve (updated in Season 02)

Applies identically to all 6 roles: Infantry, Medic, Support, Recon, Pilot, Driver.

| Level | XP | Level | XP | Level | XP | Level | XP |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 26 | 225,600 | 52 | 1,218,800 | 78 | 2,424,200 |
| 1 | 200 | 27 | 246,700 | 53 | 1,253,450 | 79 | 2,504,600 |
| 2 | 750 | 28 | 266,950 | 54 | 1,290,850 | 80 | 2,597,000 |
| 3 | 1,250 | 29 | 288,450 | 55 | 1,333,000 | 81 | 2,674,400 |
| 4 | 3,000 | 30 | 318,200 | 56 | 1,368,650 | 82 | 2,760,050 |
| 5 | 6,250 | 31 | 346,300 | 57 | 1,406,550 | 83 | 2,842,950 |
| 6 | 9,250 | 32 | 381,050 | 58 | 1,443,950 | 84 | 2,935,100 |
| 7 | 13,000 | 33 | 419,100 | 59 | 1,483,600 | 85 | 3,052,250 |
| 8 | 17,250 | 34 | 462,950 | 60 | 1,529,500 | 86 | 3,146,400 |
| 9 | 22,500 | 35 | 525,000 | 61 | 1,567,650 | 87 | 3,248,800 |
| 10 | 25,000 | 36 | 559,150 | 62 | 1,608,550 | 88 | 3,347,950 |
| 11 | 28,750 | 37 | 596,250 | 63 | 1,648,200 | 89 | 3,456,850 |
| 12 | 33,750 | 38 | 632,100 | 64 | 1,691,100 | 90 | 3,598,750 |
| 13 | 37,500 | 39 | 670,850 | 65 | 1,740,500 | 91 | 3,714,650 |
| 14 | 43,750 | 40 | 712,500 | 66 | 1,781,900 | 92 | 3,840,300 |
| 15 | 54,750 | 41 | 750,400 | 67 | 1,825,800 | 93 | 3,962,450 |
| 16 | 64,500 | 42 | 791,250 | 68 | 1,868,700 | 94 | 4,095,850 |
| 17 | 75,000 | 43 | 830,850 | 69 | 1,914,600 | 95 | 4,270,500 |
| 18 | 84,750 | 44 | 873,350 | 70 | 1,967,750 | 96 | 4,416,400 |
| 19 | 95,750 | 45 | 920,850 | 71 | 2,011,900 | 97 | 4,574,050 |
| 20 | 111,500 | 46 | 962,950 | 72 | 2,059,050 | 98 | 4,727,200 |
| 21 | 127,200 | 47 | 1,007,950 | 73 | 2,104,950 | 99 | 4,892,850 |
| 22 | 145,400 | 48 | 1,051,700 | 74 | 2,154,600 | **100** | **5,132,500** |
| 23 | 163,200 | 49 | 1,098,350 | 75 | 2,218,000 | | |
| 24 | 183,450 | 50 | 1,150,000 | 76 | 2,278,900 | | |
| 25 | 206,600 | 51 | 1,183,400 | 77 | 2,353,300 | | |

Source: [`DT_RoleMasteryDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Levels/Roles/DT_RoleMasteryDefinitions.json)

---

## 2. Cash Reward Fields — How to Read Every Table Below

Each `DT_Reward_Cash_*` row has a `base` cash value plus context modifiers applied multiplicatively/additively on top:
- `FriendlyModifier` — multiplier if the target/action involves a friendly (often negative → reward killed/zeroed for TK-adjacent cases)
- `NeutralModifier` — multiplier for neutral-faction interactions
- `OwnerModifier` — multiplier if the instigator "owns" the thing (e.g. built it themselves)
- `ModifierCZ` / `ModifierHZ` / `ModifierHZM` — multiplier if the action happens in a Control Zone / Hot Zone / Hot Zone Magnet
- `AssistBaseModifier` / `AssistScalingModifier` / `CrewAssistModifier` / `LogisticAssistModifier` — how assist credit splits between instigator and assisters

**Effective reward = `base × relevant modifier(s)`.** Real example: destroying a Littlebird (`base`=800) inside a Hot Zone = 800 × 1.5 = **1,200 cash**.

**Zone multiplier switch:** the switch in the sidebar shows each Base figure below as paid in a control zone (× its `ModifierCZ`) or a hot zone, the prio zone (× its `ModifierHZ`), with you and the target both in it. Figures that change are highlighted. Rows with no zone modifier (objectives, end of match, spotting, buildables) stay the same.

---

## 3. Player-Kill Cash Rewards ([`DT_Reward_Cash_PlayerKill`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/KillScore/DT_Reward_Cash_PlayerKill.json))

| Context | Base | Notes |
|---|---|---|
| Default player kill | **250** | Friendly-fire modifier: ×-6 (punished hard) |
| Kill from artillery (TNK_01 Artillery) while instigator is in no-man's-land | **5,000** | Huge — artillery kills from the open field pay 20× a normal kill |
| Kill while instigator is in a zone (artillery variant) | **100** | Friendly-fire ×-50 |

---

## 4. Revive & Heal Cash Rewards

### 4a. Revive ([`DT_Reward_Cash_Revive`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Revive/DT_Reward_Cash_Revive.json)) — reward goes to the reviver

| Method used | Base cash |
|---|---|
| No item (bare-hands revive) | 1,500 |
| Defibrillator | 1,000 |
| Resuscitator | 1,000 |
| MedKit | 800 |
| StimPen | 400 |
| AdrenalinePen | 100 |

(All scale further ×1.2–2.0 in Control/Hot Zones per the CZ/HZ/HZM modifiers.)

### 4b. Heal ([`DT_Reward_Cash_Heal`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Heal/DT_Reward_Cash_Heal.json)) — reward to the healer

| Item | Base cash |
|---|---|
| Default (no item tag) | 10 |
| Bandage | 400 |
| SuperBandage | 1,000 |
| MedKit (Standard) | 100 |
| AdrenalinePen (on revive-heal) | 1,200 |
| Defibrillator (on revive-heal) | **1,500** |
| Resuscitator (on revive-heal) | 1,500 |
| StimPen | 0 |

---

## 5. Vehicle-Related Cash Rewards

### 5a. Vehicle destroyed ([`DT_Reward_Cash_VehicleDestroyed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle/DT_Reward_Cash_VehicleDestroyed.json))

| Vehicle | Base cash |
|---|---|
| DuneBuggy | 300 |
| Bobcat | 100 |
| Humvee | 500 |
| Kodiak | 500 |
| Littlebird | 800 |
| ROT_01 (Huey) | 1,200 |
| **TNK_01 Heavy (tank)** | **5,000** |
| **TNK_01 Artillery** | **6,000** |
| SpawnVehicle | 4,000 |
| **Havoc (attack heli)** | **6,000** |
| **TNK_04 (tank, Default)** | **5,000** |

### 5b. Vehicle repair ([`DT_Reward_Cash_Repair`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle/DT_Reward_Cash_Repair.json))

| Tool | Base cash |
|---|---|
| Default / Wrench (Standard) | 20 |
| Drill (Light) | 20 |
| Drill (Heavy) | 25 |

### 5c. Vehicle refuel ([`DT_Reward_Cash_Refuel`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle/DT_Reward_Cash_Refuel.json))

| Context | Base cash |
|---|---|
| Default fallback | 10 |

### 5d. Vehicle transport ([`DT_Reward_Cash_VehicleTransport`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle/DT_Reward_Cash_VehicleTransport.json))

| Context | Base cash |
|---|---|
| Default fallback | 20 |
| Spawned on vehicle (driver gets a passenger credit) | 100 |
| Passenger successfully transported | 250 |

---

## 6. Objective Cash Rewards

### 6a. Control Zone / Hot Zone / Magnet Zone ([`DT_Reward_Cash_ControlZoneReward`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Objective/DT_Reward_Cash_ControlZoneReward.json))

| Event | Base cash |
|---|---|
| Control Zone — contested | 150 |
| Control Zone — not owned | 150 |
| Control Zone — owned | 150 |
| Control Zone — entered (first time, that life) | 100 |
| Hot Zone — not owned | 600 |
| Hot Zone — contested | 600 |
| Hot Zone — owned | 600 |
| Hot Zone — entered | 0 |
| Magnet Zone — contested | 600 |
| Magnet Zone — owned | 700 |
| Magnet Zone — not owned | 600 |
| **Spawn-vehicle enters Control Zone** | **3,000** |

### 6b. HotZone Magnet / Tower events ([`DT_Reward_Cash_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/HotZoneMagnet/DT_Reward_Cash_HotZoneMagnet.json))

| Event | Base cash |
|---|---|
| Activated the magnet (instigator) | **5,000** |
| Near an activated magnet | 5,000 |
| Deactivated the magnet (instigator) | 200 |
| Magnet destroyed (unused row) | 150 |
| Captured a hostile tower (instigator) | 1,000 |
| Near a captured hostile tower | 1,000 |
| Captured a neutral tower (instigator) | 250 |
| Near a neutral tower | 250 |

### 6c. End-of-match faction placement ([`DT_Reward_Cash_EndGameFactionReward`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Objective/DT_Reward_Cash_EndGameFactionReward.json))

| Placement | Base cash |
|---|---|
| Default (no item used — revive context reused here) | 100 |
| 1st place faction | 200 |
| 2nd place faction | 150 |
| 3rd place faction | 100 |

---

## 7. Buildable Cash Rewards

Three separate tables by action — **Built**, **Placed**, **Placed-in-FOB** — plus **Destroyed** (someone else's build dying):

| Buildable | Built | Placed | Placed-in-FOB | Destroyed |
|---|---|---|---|---|
| HBlock | 1 | 100 | 100 | 100 |
| TallHBlock | 1 | 200 | 200 | 100 |
| Gate | 1 | 300 | 300 | 500 |
| FOB | 1 | 1,000 | 1,000 | **5,000** |
| HBlockQuadWall | 1 | 500 | 500 | 125 |
| Mortar | 1 | 300 | 300 | 300 |
| BarbedWire | 1 | 10 | 10 | 75 |
| TankTrap | 1 | 100 | 100 | 250 |
| AirRaidShelter | 1 | 500 | 500 | 1,400 |
| Bunker | 1 | 500 | 500 | 1,400 |
| CrowsNest | — | — | — | 1,400 |
| CamoNetTent | — | — | — | 75 |
| Door | — | — | — | 100 |
| HotzoneMagnet | — | — | — | **3,000** |
| SandbagWall | — | — | — | 100 |

("Built" rewards are tiny flat 1-cash credits — the real payout is the "Placed" value; "Destroyed" rewards go to whoever destroys an enemy structure, scaled by `FriendlyModifier: -0.75` if it turns out to be a teammate's.)

---

## 8. Deployable (Supply Crate / Explosives) Cash Rewards

### 8a. Deployed ([`DT_Reward_Cash_DeployedSupplyCrate`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Deployable/DT_Reward_Cash_DeployedSupplyCrate.json))

| Item | Base cash |
|---|---|
| Default fallback | 25 |
| Supply Crate Container (Free) | 25 |
| Supply Crate (Small / Small Armoured) | 50 |
| Supply Crate (Large / Large Armoured) | 150 |

### 8b. Destroyed ([`DT_Reward_Cash_DeployableDestroyed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Deployable/DT_Reward_Cash_DeployableDestroyed.json), destroying enemy deployables)

| Item | Base cash |
|---|---|
| Claymore | 100 |
| C4 Explosive | 100 |
| AT Mine | 100 |
| Supply Crate (various) | 100–200 |

---

## 9. Spotting Cash Rewards ([`DT_Reward_Cash_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Rewards/DT_Reward_Cash_Spotting.json))

| Event | Min | Max |
|---|---|---|
| Target spotted | 15 | 275 |
| Spotted target destroyed | 50 | 500 |

(Scaled between min/max by an assist-scaling curve based on how much the spot contributed to the kill.)

---

## 10. End-of-Match Challenge Rewards ([`DT_ChallengeRewards_EndOfMatch`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_EndOfMatch.json))

Faction placement bonus formula: `CashEarned × PlacementModifier`, where:

| Placement | Cash multiplier | XP multiplier (all 6 roles) |
|---|---|---|
| 1st place | 0.3× | **2.0×** |
| 2nd place | 0.25× | 1.75× |
| 3rd place | 0.2× | 1.5× |

So the winning faction gets +30% of their earned match cash as a bonus **and double XP** on top of whatever they earned in-match, across every role simultaneously.

A separate `FactionWinBonus` row (new in Season 02) is a flat cash bonus selected by faction alignment tag:

| Alignment tag | Bonus cash | Variable |
|---|---|---|
| Alpha | 10,000 | `LonestarBonus` |
| Bravo | 0 | `ValkyraBonus` |
| Charlie | 0 | `ManticoreBonus` |
| Default | 0 | `DefaultReward` |

---

## 11. Challenge Tips (unchanged from v1 — confirmed still accurate, lives in [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json))

| Challenge | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|
| Heal | 5 | 10 | 15 | 20 |
| Revive | 10 | 15 | 20 | 25 |
| Player Delivered | 15 | 20 | 25 | 30 |
| Repair | 5 | 10 | 15 | 20 |
| Refuel | 5 | 10 | 15 | 20 |

Pre-Tip: +50 cash per tip, capped at 500.

---

## 12. Season

| Field | Value |
|---|---|
| Current Season Number | 1 |
| SeasonDefinitions array | empty (not populated this build) |

---

## 13. Biggest Payouts in the Game (corrected)

| Rank | Reward | Amount |
|---|---|---|
| 1 | Destroying a Havoc attack helicopter | 6,000 |
| 1 (tie) | Destroying a TNK_01 Artillery vehicle | 6,000 |
| 3 | Activating/being near the HotZone Magnet | 5,000 |
| 3 (tie) | Killing a player from artillery in the open field | 5,000 |
| 3 (tie) | Destroying an enemy FOB | 5,000 |
| 3 (tie) | Destroying a TNK_01 Heavy tank | 5,000 |
| 7 | Destroying a SpawnVehicle | 4,000 |
| 8 | Spawn-vehicle reaching Control Zone | 3,000 |
| 8 (tie) | Destroying a HotzoneMagnet buildable | 3,000 |
| 10 | Capturing/defending a hostile tower | 1,000 |

---

## 14. End-of-Match Reward — Full Breakdown

The end-of-match bonus is a real **formula**, not a flat number, computed per faction at round end:

```
CashBonus = CashEarned_thisMatch × PlacementModifier
XPBonus   = XPEarned_thisMatch   × PlacementModifier   (applied separately, per role: Driver/Infantry/Medic/Pilot/Recon/Support)
```

**Placement modifiers:**

| Placement | Cash multiplier | XP multiplier |
|---|---|---|
| 1st place | **0.3×** | **2.0×** |
| 2nd place | 0.25× | 1.75× |
| 3rd place | 0.2× | 1.5× |

1st place gets 30% of their earned match cash back as a bonus plus double XP across every role; 2nd/3rd still get a smaller consolation cut.

**Input caps (`CurveFloat` assets, applied before the multiplier):**
- [`CRV_Challenges_Curves_EndOfMatch_CashEarned`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_EndOfMatch_CashEarned.json) — passes `CashEarned` through 1:1 up to **100,000**, flat beyond that (hard cap)
- [`CRV_Challenges_Curves_EndOfMatch_XPEarned`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_EndOfMatch_XPEarned.json) — passes `XPEarned` through 1:1 up to **2,500**, default fallback 1.5 beyond that

So no matter how big the match was, the bonus calculation treats anything above 100k cash / 2.5k XP earned-that-match as capped before the placement multiplier applies.

**Flat placement bonus on top** (separate from the formula above, from [`DT_Reward_Cash_EndGameFactionReward`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Objective/DT_Reward_Cash_EndGameFactionReward.json)):

| Placement | Flat cash |
|---|---|
| 1st | 200 |
| 2nd | 150 |
| 3rd | 100 |

## 15. Dynamic Per-Kill Reward Calculator ([`DT_ChallengeRewards_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_SessionEvents_Shared.json))

Kill rewards are not flat either — resolved through a ~20-variable formula per kill:

```
Reward = (1 − min(LastVictimCount,4) × 0.24)
         × [ (BaseReward + min(KillStreak−1,5) × 50) × InstigatorZoneWeight
           + (BaseReward + min(KillStreak−1,5) × 50) × TargetZoneWeight ]
         × DistanceScalar × RevengeMod × KillStreakStoppedMod
         × FriendlyMod
         × CrewPenaltyMod ^ min(CrewCount−1, CrewCountMax)
```

**Base rewards by kill type:**

| Kill type | Base |
|---|---|
| Default player kill | 300 |
| Headshot | 350 |
| Precision Artillery Strike kill | 250 |
| Air Vehicle kill | 300 |

**Key modifiers:**

| Modifier | Value | Trigger |
|---|---|---|
| Last-victim diminishing returns | −24% per repeat kill on same player, capped at 4 stacks | Spawn-camping tax |
| Kill streak bonus | +50 per streak kill, capped at 5 | Up to +250 at streak cap |
| Kill-streak-stopped bonus | 1.5× | Ending an enemy's streak (non-friendly, non-sniper, non-artillery) |
| Revenge kill bonus | 2.0× | Killing the player who last killed you |
| Friendly-fire penalty | −3.0× (i.e. negative reward) | Teamkill |
| Ressed-by-enemy penalty | 0.01× | Near-zero reward if the victim was revived by an enemy medic first |
| Crew-assist penalty | 0.8 ^ (crew count − 1), up to 5 crew | Reward splits down as more crew members are credited |
| Control Zone bonus | 5.0× weight | Kill happens in/near a Control Zone |
| Hot Zone bonus | 10.0× weight | Kill happens in/near a Hot Zone |
| Hot Zone Magnet active bonus | 10.0× weight | Stacks when the Magnet is active |
| Target-in-friendly-Hot-Zone | 4.0× weight | Killing in the enemy's own Hot Zone |
| Target-in-friendly-Control-Zone | 2.0× weight | Killing in the enemy's own Control Zone |
| Distance scalar (sniper/artillery only) | via `LiveCurves.Challenges.SessionEvents.PlayerKill.DistanceScalar` (+`.Artillery` variant) | Longer-range sniper/artillery kills scale reward by distance |

Net effect: a long-range artillery kill on a streaking player inside an active Hot Zone Magnet, ending their streak, stacks almost every bonus multiplier simultaneously — by far the highest-value kill in the game. A teamkill or a kill on someone an enemy medic just rezzed is deliberately punished into near-zero or negative reward.

---

## 16. What Was Wrong in v1 (honesty note)

v1 of this doc used [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json)/[`DT_CashRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_CashRewards.json) — those are evidently a **deprecated or placeholder layer** (almost every `ResourceValue` in them reads 0.0). The real, currently-live reward logic routes through `WDCustomRewardTableRow` entries in the [`CashRewardsDataTable/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable) folder tree (organized by category: KillScore, Revive, Heal, Vehicle, Objective, Buildable, Deployable, HotZoneMagnet) plus `WDChallengeRewardDefinition` rows for end-of-match bonuses. This version (v2) is built from those and is the accurate picture — so no, v1 was not all of it, not even close on the cash side.

**Still not pulled** (exists in the game data, flagged for a future pass): [`DT_Meta_RewardScalingCurves`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Rewards/DT_Meta_RewardScalingCurves.json), `DT_RewardLookup_SessionEvent_*` (session-event lookups for Spotting/Buildables/KOTH game mode), [`DT_DemoRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/Demo/DT_DemoRewards.json), cosmetic/item unlock rewards tied to the `TreeRewardTrack` battle-pass UI widgets, and [`DA_UI_PlatformMastery_RewardData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Mastery/Platforms/Data/DA_UI_PlatformMastery_RewardData.json). Say the word if you want those too.

---

*Full raw JSON for every table above lives in [`Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable) and [`Wardogs/Content/Meta/Challenges/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Meta/Challenges).*
