---
title: "Rewards & Progression"
nav_order: 2
---

# Wardogs — Rewards & Progression Reference (v2, corrected)
*Extracted from cooked game data via CUE4Parse (build `++Wardogs+Live-CL-509546`, UE 5.7.4). All numbers below come directly from the game's own DataTables.*

> **Correction note:** v1 of this doc pulled from [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json)/[`DT_CashRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_CashRewards.json) — those tables turned out to be **stale/placeholder** (nearly everything reads `0`). The real, live numbers live in a separate, much bigger family of per-category tables (`DT_Reward_Cash_*`, `DT_ChallengeRewards_*`) under [`CashRewardsDataTable/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable). This version replaces those zeros with the actual base values, including per-item, per-vehicle, and per-buildable breakdowns that weren't in v1 at all.

---

## 1. Role Mastery XP Curve (unchanged from v1, confirmed correct)

Applies identically to all 6 roles: Infantry, Medic, Support, Recon, Pilot, Driver.

| Level | XP | Level | XP | Level | XP | Level | XP |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 26 | 388,000 | 52 | 1,589,500 | 78 | 3,064,000 |
| 1 | 200 | 27 | 413,500 | 53 | 1,634,500 | 79 | 3,154,750 |
| 2 | 750 | 28 | 438,000 | 54 | 1,682,250 | 80 | 3,257,500 |
| 3 | 1,250 | 29 | 464,000 | 55 | 1,734,750 | 81 | 3,345,250 |
| 4 | 3,000 | 30 | 500,000 | 56 | 1,780,750 | 82 | 3,441,250 |
| 5 | 6,250 | 31 | 534,000 | 57 | 1,829,000 | 83 | 3,534,500 |
| 6 | 9,250 | 32 | 576,000 | 58 | 1,876,750 | 84 | 3,637,000 |
| 7 | 13,000 | 33 | 622,000 | 59 | 1,926,750 | 85 | 3,764,500 |
| 8 | 17,250 | 34 | 675,000 | 60 | 1,983,000 | 86 | 3,869,000 |
| 9 | 22,500 | 35 | 750,000 | 61 | 2,031,500 | 87 | 3,981,750 |
| 10 | 35,000 | 36 | 791,000 | 62 | 2,082,750 | 88 | 4,091,250 |
| 11 | 46,250 | 37 | 835,500 | 63 | 2,132,750 | 89 | 4,210,500 |
| 12 | 58,500 | 38 | 878,500 | 64 | 2,186,000 | 90 | 4,362,750 |
| 13 | 71,500 | 39 | 925,000 | 65 | 2,245,750 | 91 | 4,489,000 |
| 14 | 85,000 | 40 | 975,000 | 66 | 2,297,500 | 92 | 4,625,000 |
| 15 | 110,000 | 41 | 1,020,500 | 67 | 2,351,750 | 93 | 4,757,500 |
| 16 | 131,750 | 42 | 1,069,500 | 68 | 2,405,000 | 94 | 4,901,250 |
| 17 | 158,000 | 43 | 1,117,000 | 69 | 2,461,250 | 95 | 5,086,250 |
| 18 | 183,750 | 44 | 1,168,000 | 70 | 2,524,750 | 96 | 5,242,500 |
| 19 | 214,500 | 45 | 1,225,000 | 71 | 2,579,250 | 97 | 5,410,500 |
| 20 | 250,000 | 46 | 1,275,500 | 72 | 2,636,750 | 98 | 5,574,000 |
| 21 | 269,000 | 47 | 1,329,500 | 73 | 2,693,000 | 99 | 5,750,000 |
| 22 | 291,000 | 48 | 1,382,000 | 74 | 2,753,000 | **100** | **6,000,000** |
| 23 | 312,500 | 49 | 1,438,000 | 75 | 2,826,750 | | |
| 24 | 337,000 | 50 | 1,500,000 | 76 | 2,898,000 | | |
| 25 | 365,000 | 51 | 1,543,750 | 77 | 2,982,750 | | |

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

**Still not pulled** (exists in the dump, flagged for a future pass): [`DT_Meta_RewardScalingCurves`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Rewards/DT_Meta_RewardScalingCurves.json), `DT_RewardLookup_SessionEvent_*` (session-event lookups for Spotting/Buildables/KOTH game mode), [`DT_DemoRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/Demo/DT_DemoRewards.json), cosmetic/item unlock rewards tied to the `TreeRewardTrack` battle-pass UI widgets, and [`DA_UI_PlatformMastery_RewardData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Mastery/Platforms/Data/DA_UI_PlatformMastery_RewardData.json). Say the word if you want those too.

---

*Full raw JSON for every table above lives in [`Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable) and [`Wardogs/Content/Meta/Challenges/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Meta/Challenges).*
