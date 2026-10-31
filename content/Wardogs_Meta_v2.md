---
title: "Meta Progression"
redirect_from: ["/Wardogs_Meta_v2.html", "/Wardogs_Meta_v2"]
parent: "Rewards & Unlocks"
description: "Meta progression data: role unlock trees, character skill effects and reward scaling curves."
---

# Wardogs: Meta Data Reference
*Extracted from cooked game data ([`Wardogs/Content/Meta`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Meta), 80 files, UE 5.7 export to JSON). Values are the raw asset values. Interpretations are marked as inferred.*

> **Scope:** the progression and meta-systems layer: role unlock trees, character skill effects, achievements and missions, currency and the gold market, and the reward scaling curves. The per-kill and per-event cash values are in [Wardogs_Rewards_and_Progression_v2.md](../Wardogs_Rewards_and_Progression_v2.md). This doc links to that file and does not repeat those values.

---

## Season 02 update (2026-10-15)

- **New Wagers system:** 7 new files under `Wagers/`. A vendor in spawn, unlocked by `Meta.Unlocks.Wager`, takes a cash stake of 2,500 to 100,000 on in-match objectives (section 13).
- **New challenge tables:** [`DT_PassiveMissionChallenges`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/DT_PassiveMissionChallenges.json) went from 0 rows to 15 (five tiers for each passive mission). [`DT_Challenges_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_Challenges_SessionEvents_Shared.json) went from 0 rows to 10 (one per achievement).
- **Achievements:** [`DT_Achievements`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Achievements/DT_Achievements.json) went from 0 rows to 10 rows, one per achievement (section 5).
- **New curves and state trees:** 2 supply-crate curve tables ([`CRV_Challenges_Curves_DeploySupplyCrate_XP`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_DeploySupplyCrate_XP.json), [`CRV_Challenges_Curves_DestroySupplyCrate_Cash`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_DestroySupplyCrate_Cash.json)) and 4 challenge StateTrees (`ST_Challenges_Challenge_*`).
- **Unlock tree, Driver:** 15 nodes to 21. Total cash to unlock all: 1,174,750 to 2,308,250.
- **Unlock tree, Wardog:** 58 nodes to 63. Most expensive node 500,000 to 200,000 cash. Total cash to unlock all: 2,787,500 to 2,645,000.
- **Unlock tree, Pilot:** Havoc helicopter (`Vehicle.Variant.Air.Rotary.Havoc.Default`, L35) 500,000 to 650,000 cash. Pilot total 959,750 to 1,218,250.
- **Unlock tree, Infantry, Medic and Support:** most expensive node 200,000 to 250,000 (Infantry, Support) and 150,000 to 200,000 (Medic). Totals: Infantry 965,000 to 1,270,000, Medic 1,040,000 to 1,220,000, Support 1,240,000 to 1,630,000.
- **Gold market:** 20 entries worth 200 Gold Bars to 27 entries worth 275 Gold Bars. New `ChocolateChip` category: 3 items at 10 Gold Bars each.
- **Cosmetic sets:** 11 to 12 (added `Meta.Cosmetic.ChocolateChip`).
- **Gold market by category:** `TwoToneDesert` 12 items (115 Gold Bars) to 15 items (150 Gold Bars). `DigitalWood` 4 items (40 Gold Bars) to 5 items (50 Gold Bars).
- **Supply crate purchase XP curve:** key (75, 5) to (10, 5).
- **End-of-match rewards:** 4 rows to 5. New `FactionWinBonus` row.
- **Session-event reward rows:** 161 to 298.
- **Mock investments:** 2 placeholder entries in one row, still debug data.
- **Role XP tables:** Driver level 10 XP 35,000 to 25,000, and level 100 XP 6,000,000 to 5,132,500. The same change appears for every role. The XP curve values are in the rewards doc.

Full before/after list: [Season 2 Changes → Rewards & Unlocks]({{ '/season-2-changes/rewards-unlocks.html' | relative_url }}).

---

## 1. Folder Map

| Subfolder | Files | Contents |
|---|---|---|
| Challenges | 30 | End-of-match, session-event and demo tables; 4 challenge StateTrees (`ST_Challenges_Challenge_*`); 22 curve tables under [`RewardData/CurveTables`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables) |
| CharacterSkills | 13 | 6 skill tables (`DT_*Skills`), 6 curve tables (`CT_*Skills`), and the unlock tree [`DT_MetaTree_Roles`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_MetaTree_Roles.json) |
| Achievements | 11 | 10 achievement StateTrees; [`DT_Achievements`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Achievements/DT_Achievements.json) (10 rows) |
| Missions | 4 | 2 mission StateTrees; [`DT_PassiveMissions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/DT_PassiveMissions.json) (3 rows); [`DT_PassiveMissionChallenges`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/DT_PassiveMissionChallenges.json) (15 rows) |
| Rewards | 3 | [`DT_Meta_RewardScalingCurves`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Rewards/DT_Meta_RewardScalingCurves.json) and 2 scaling curves |
| Cosmetics | 2 | [`DT_CosmeticSets_Debug`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Cosmetics/DT_CosmeticSets_Debug.json): 12 cosmetic sets |
| Investments | 2 | 2 debug investment definitions (`DA_TestInvestment*`) |
| (root) | 1 | [`DT_SeasonDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/DT_SeasonDefinitions.json) (season 1, no season list) |
| ClientHotConfigs | 1 | 3 INI-style client config blobs (subsystem settings) |
| Collection | 1 | [`DT_GoldMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Collection/DT_GoldMarket.json): 27 gold-bar store entries |
| CurrencyDefinitions | 1 | Cash and Gold Bars currency rows |
| ExchangeDefinitions | 1 | [`DT_ExchangeDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/ExchangeDefinitions/DT_ExchangeDefinitions.json): Gold Bars row with no exchange rates |
| Levels | 1 | [`DT_RoleMasteryDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Levels/Roles/DT_RoleMasteryDefinitions.json): role XP curves (in the rewards doc) |
| MockInvestments | 1 | [`DT_MockInvestments`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/MockInvestments/DT_MockInvestments.json): 1 row with 2 placeholder entries |
| Resources | 1 | [`DT_Meta_ResourceEffects`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Resources/Effects/DT_Meta_ResourceEffects.json): one GameplayEffect hook |
| Wagers | 7 | Wager vendor tables (pricing, objectives, actions, conditions, challenges, UI); see section 13 |

18 files hold more than one `--- export:` block (for example a StateTree plus its schema and helper blueprint classes). Each block is parsed separately.

---

## 2. Role Unlock Trees ([`DT_MetaTree_Roles`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_MetaTree_Roles.json))

Each role has a list of unlock nodes. A node is an item, vehicle or supply crate, keyed by its `ID` tag. Each node has one level entry with a **Cost** (cash) and a **Prerequisite** (a minimum level). The XP side of progression is in [`DT_RoleMasteryDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Levels/Roles/DT_RoleMasteryDefinitions.json) (rewards doc, section 1).

| Role | Nodes | Level gate | Cost per node (cash) | Zero-cost nodes | Cash to unlock all | Gate type |
|---|---|---|---|---|---|---|
| Driver | 21 | L3 to L35 | 750 to 500,000 | 0 | 2,308,250 | Meta.Role.Driver |
| Infantry | 40 | L2 to L50 | 0 to 250,000 | 5 | 1,270,000 | Meta.Role.Infantry |
| Medic | 38 | L1 to L50 | 0 to 200,000 | 4 | 1,220,000 | Meta.Role.Medic |
| Pilot | 11 | L2 to L35 | 750 to 650,000 | 0 | 1,218,250 | Meta.Role.Pilot |
| Recon | 58 | L2 to L50 | 0 to 200,000 | 7 | 2,445,000 | Meta.Role.Recon |
| Support | 33 | L1 to L50 | 0 to 250,000 | 5 | 1,630,000 | Meta.Role.Support |
| Wardog | 63 | L1 to L150 | 0 to 200,000 | 3 | 2,645,000 | MinLevel only (no MetaId, no XP tag) |

**Notes**
- The six combat roles gate each node with a `MinLevel` against that role's own `MetaId` and XP tag (`Attribute.Meta.XP.Role.<Role>`).
- Tank and helicopter nodes are the most expensive: `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` (Driver, 500,000 cash, L35) and `Vehicle.Variant.Air.Rotary.Havoc.Default` (Pilot, 650,000 cash, L35). The Wardog tree has no tank node above 200,000 cash.
- **The Wardog tree is different.** Its 63 nodes have a `MinLevel` gate from L1 to L150 but no `MetaId` and no XP tag. The export does not name the level track that gates it. [`DT_RoleMasteryDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Levels/Roles/DT_RoleMasteryDefinitions.json) has no Wardog row, and the XP table stops at level 100 (see section 12).
- Most zero-cost nodes are magazines and ammo (for example `Id.Item.STANAGMagazine`, `Id.Item.Arrow`, `Id.Item.SV98Magazine`). A few are explosives or rounds (`Id.Item.C4Explosive`, `Id.Item.93mm`), so cost zero does not always mean ammo.

---

## 3. Character Skill Effects (`DT_*Skills`)

Each skill row holds a `SkillEffects` list. Each entry has:
- a **slot** that says what the effect attaches to: `Item` (the held weapon), `Character`, `Character.HeldItemUpdated`, `Revive.Target`, `Vehicle`, or `SupplyCrate`;
- a **GameplayEffect** class (`GE_*`) that applies the change;
- one or more **magnitudes**, each an attribute tag (for example `Attribute.Gameplay.Weapon.AimTime`) with either a literal or a curve row in the matching `CT_*Skills` table;
- an optional **gate** (`ItemApplicationRequirements`) that limits the effect to items with a given archetype or ID tag.

The full skill list with display names, resolved GameplayEffect modifiers and level curves (all 62 rows, including the plugin tables) is on [Progression Tables](../game-features/Wardogs_Progression_v1.md). The live reward curves, currencies and cosmetic rows are there too.

There are **57 effect entries** across six roles, using **18 distinct GE classes**. The `Revive.Target`, `Vehicle` and `SupplyCrate` slot names are read from the names only; their targets are not spelled out in the export.

| Role | Skill row | Slot | GE | Attribute | Curve row / literal | Gate |
|---|---|---|---|---|---|---|
| Infantry | SprintBreach | Character | GE_GrantSkill_DoorBreach_C | (none) | (none) | none |
| Infantry | ReturnToFireSpeed.AssaultRifle | Character | GE_Player_ReadyToFirePlayRate_C | Movement.ReadyToFirePlayRate | ReadyToFireSpeed_AssaultRifle | Archetype AR |
| Infantry | AimMoveSpeed.AssaultRifle | Character.HeldItemUpdated | GE_Player_MaxSpeedMultiplier_Aiming_C | Movement.MaxSpeedMultiplier | AimMoveSpeed_AssaultRifle | Archetype AR |
| Infantry | HorizontalRecoil.AssaultRifle | Item | GE_Weapon_HorizontalRecoilMultiplier_C | Weapon.HorizontalRecoilMultiplier | HorizontalRecoil_AssaultRifle | Archetype AR |
| Infantry | VerticalRecoil.AssaultRifle | Item | GE_Weapon_VerticalRecoilMultiplier_C | Weapon.VerticalRecoilMultiplier | VerticalRecoil_AssaultRifle | Archetype AR |
| Infantry | AimDownSightSpeed.AssaultRifle | Item | GE_Weapon_AimTime_C | Weapon.AimTime | AimDownSightSpeed_AssaultRifle | Archetype AR |
| Infantry | WeaponSwitchSpeed | Item | GE_Weapon_EquipSpeedMultiplier_C | Weapon.EquipSpeedMultiplier | WeaponSwitchSpeed | none |
| Infantry | HorizontalRecoil.SMG | Item | GE_Weapon_HorizontalRecoilMultiplier_C | Weapon.HorizontalRecoilMultiplier | HorizontalRecoil_SMG | Archetype SMG |
| Infantry | VerticalRecoil.SMG | Item | GE_Weapon_VerticalRecoilMultiplier_C | Weapon.VerticalRecoilMultiplier | VerticalRecoil_SMG | Archetype SMG |
| Infantry | AimDownSightSpeed.SMG | Item | GE_Weapon_AimTime_C | Weapon.AimTime | AimDownSightSpeed_SMG | Archetype SMG |
| Infantry | ReturnToFireSpeed.SMG | Character | GE_Player_ReadyToFirePlayRate_C | Movement.ReadyToFirePlayRate | ReadyToFireSpeed_SMG | Archetype SMG |
| Infantry | AimMoveSpeed.SMG | Character.HeldItemUpdated | GE_Player_MaxSpeedMultiplier_Aiming_C | Movement.MaxSpeedMultiplier | AimMoveSpeed_SMG | Archetype SMG |
| Infantry | UnarmedSprintSpeed | Character.HeldItemUpdated | GE_Player_SprintSpeedMultiplier_C | Movement.SprintSpeedMultiplier; Movement.TacSprintSpeedMultiplier | UnarmedSprintSpeed_SprintSpeed; UnarmedSprintSpeed_TacSprintSpeed | Fists |
| Infantry | TacticalSprintRecovery | Character | GE_Player_StaminaRegenPerSecondMultiplier_C | Movement.StaminaRegenPerSecondMultiplier | TacticalSprintRecovery | none |
| Infantry | CovertStaminaRegen | Character | GE_Player_StaminaRegenPerSecondMultiplier_Covert_C | Movement.StaminaRegenPerSecondMultiplier | CovertStaminaRegen | none |
| Infantry | TacticalSprintDuration | Character | GE_Player_TacSprintStaminaUsageMultiplier_C | Movement.TacSprintStaminaUsageMultiplier | TacticalSprintDuration | none |
| Infantry | CovertMovementSpeed | Character | GE_Player_MaxSpeedMultiplier_Covert_C | Movement.MaxSpeedMultiplier | CovertMovementSpeed | none |
| Medic | ReduceUsage.Medkit | Item | GE_Item_UsageRateMultiplier_C | Item.UsageRateMultiplier | ReduceUsage_Medkit | ID.Item.MedKit.Standard |
| Medic | MedicalItemSwapSpeed | Item | GE_Weapon_EquipSpeedMultiplier_C | Weapon.EquipSpeedMultiplier | MedicalItemSwapSpeed | Item.Context.Medical |
| Medic | ReviveSpeedBoost.Teammate | Revive.Target | GE_Player_SprintSpeedMultiplier_Temp_C | Movement.SprintSpeedMultiplier; Movement.TacSprintSpeedMultiplier | ReviveSpeedBoost_Teammate_SprintSpeed; ReviveSpeedBoost_Teammate_TacSprintSpeed | none |
| Medic | ReviveSpeedBoost.Self | Revive.Target | GE_Player_SprintSpeedMultiplier_Temp_C | Movement.SprintSpeedMultiplier; Movement.TacSprintSpeedMultiplier | ReviveSpeedBoost_Self_SprintSpeed; ReviveSpeedBoost_Self_TacSprintSpeed | none |
| Support | ReadyToFireSpeed.LMG | Character | GE_Player_ReadyToFirePlayRate_C | Movement.ReadyToFirePlayRate | ReadyToFireSpeed_LMG | Archetype LMG |
| Support | AimMoveSpeed.LMG | Character.HeldItemUpdated | GE_Player_MaxSpeedMultiplier_Aiming_C | Movement.MaxSpeedMultiplier | AimMoveSpeed_LMG | Archetype LMG |
| Support | HorizontalRecoil.LMG | Item | GE_Weapon_HorizontalRecoilMultiplier_C | Weapon.HorizontalRecoilMultiplier | HorizontalRecoil_LMG | Archetype LMG |
| Support | VerticalRecoil.LMG | Item | GE_Weapon_VerticalRecoilMultiplier_C | Weapon.VerticalRecoilMultiplier | VerticalRecoil_LMG | Archetype LMG |
| Support | AimDownSightSpeed.LMG | Item | GE_Weapon_AimTime_C | Weapon.AimTime | AimDownSightSpeed_LMG | Archetype LMG |
| Support | WeaponSwitchSpeed | Item | GE_Weapon_EquipSpeedMultiplier_C | Weapon.EquipSpeedMultiplier | WeaponSwitchSpeed | none |
| Support | HorizontalRecoil.Shotgun | Item | GE_Weapon_HorizontalRecoilMultiplier_C | Weapon.HorizontalRecoilMultiplier | HorizontalRecoil_Shotgun | Archetype Shotgun |
| Support | VerticalRecoil.Shotgun | Item | GE_Weapon_VerticalRecoilMultiplier_C | Weapon.VerticalRecoilMultiplier | VerticalRecoil_Shotgun | Archetype Shotgun |
| Support | AimdownSightspeed.Shotgun | Item | GE_Weapon_AimTime_C | Weapon.AimTime | AimDownSightSpeed_Shotgun | Archetype Shotgun |
| Support | ReadyToFireSpeed.Shotgun | Character | GE_Player_ReadyToFirePlayRate_C | Movement.ReadyToFirePlayRate | ReadyToFireSpeed_Shotgun | Archetype Shotgun |
| Support | AimMoveSpeed.Shotgun | Character.HeldItemUpdated | GE_Player_MaxSpeedMultiplier_Aiming_C | Movement.MaxSpeedMultiplier | AimMoveSpeed_Shotgun | Archetype Shotgun |
| Recon | SniperKillFocusReset | Character | GE_GrantSkill_SniperKillFocusRefresh_C | (none) | (none) | none |
| Recon | ReadyToFireSpeed.Sniper | Character | GE_Player_ReadyToFirePlayRate_C | Movement.ReadyToFirePlayRate | ReadyToFireSpeed_Sniper | Archetype Sniper |
| Recon | AimMoveSpeed.Sniper | Character.HeldItemUpdated | GE_Player_MaxSpeedMultiplier_Aiming_C | Movement.MaxSpeedMultiplier | AimMoveSpeed_Sniper | Archetype Sniper |
| Recon | HorizontalRecoil.Sniper | Item | GE_Weapon_HorizontalRecoilMultiplier_C | Weapon.HorizontalRecoilMultiplier | HorizontalRecoil_Sniper | Archetype Sniper |
| Recon | VerticalRecoil.Sniper | Item | GE_Weapon_VerticalRecoilMultiplier_C | Weapon.VerticalRecoilMultiplier | VerticalRecoil_Sniper | Archetype Sniper |
| Recon | AimDownSightSpeed.Sniper | Item | GE_Weapon_AimTime_C | Weapon.AimTime | AimDownSightSpeed_Sniper | Archetype Sniper |
| Recon | WeaponSwitchSpeed.ReconWeaponry | Item | GE_Weapon_EquipSpeedMultiplier_C | Weapon.EquipSpeedMultiplier | WeaponSwitchSpeed_ReconWeaponry | none |
| Recon | HorizontalRecoil.Marksman | Item | GE_Weapon_HorizontalRecoilMultiplier_C | Weapon.HorizontalRecoilMultiplier | HorizontalRecoil_DMR | Archetype DMR |
| Recon | VerticalRecoil.Marksman | Item | GE_Weapon_VerticalRecoilMultiplier_C | Weapon.VerticalRecoilMultiplier | VerticalRecoil_DMR | Archetype DMR |
| Recon | AimDownSightSpeed.Marksman | Item | GE_Weapon_AimTime_C | Weapon.AimTime | AimDownSightSpeed_DMR | Archetype DMR |
| Recon | ReadyToFireSpeed.Marksman | Character | GE_Player_ReadyToFirePlayRate_C | Movement.ReadyToFirePlayRate | ReadyToFireSpeed_DMR | Archetype DMR |
| Recon | AimMoveSpeed.Marksman | Character.HeldItemUpdated | GE_Player_MaxSpeedMultiplier_Aiming_C | Movement.MaxSpeedMultiplier | AimMoveSpeed_DMR | Archetype DMR |
| Recon | WeaponSwitchSpeed.Pistol | Item | GE_Weapon_EquipSpeedMultiplier_C | Weapon.EquipSpeedMultiplier | WeaponSwitchSpeed_Pistol | Archetype Pistol |
| Pilot | HorizontalRecoil.MountedGun | Item | GE_Weapon_HorizontalRecoilMultiplier_C | Weapon.HorizontalRecoilMultiplier | HorizontalRecoil_MountedGun | ROT_01.MountedMachineGun |
| Pilot | VerticalRecoil.MountedGun | Item | GE_Weapon_VerticalRecoilMultiplier_C | Weapon.VerticalRecoilMultiplier | VerticalRecoil_MountedGun | ROT_01.MountedMachineGun |
| Pilot | ImpactDamageReduction | Vehicle | GE_Vehicle_ImpactReductionMultiplier_C | Health.ImpactReductionMultiplier | ImpactDamageReduction | none |
| Pilot | FuelUsageReduction | Vehicle | GE_Vehicle_FuelUsageReductionMultiplier_C | FuelUsageReductionMultiplier | FuelUsageReduction | none |
| Pilot | AimDownSightSpeed.MountedGun | Item | GE_Weapon_AimTime_C | Weapon.AimTime | AimDownSight_MountedGun | ROT_01.MountedMachineGun |
| Pilot | IncreasedHealth.SupplyCrate | SupplyCrate | GE_Vehicle_Health_C | Health | IncreasedHealth_SupplyCrate | none |
| Driver | HorizontalRecoil.MountedGun | Item | GE_Weapon_HorizontalRecoilMultiplier_C | Weapon.HorizontalRecoilMultiplier | HorizontalRecoil_MountedGun | ID.Item.HeavyTankMountedMachineGun |
| Driver | VerticalRecoil.MountedGun | Item | GE_Weapon_VerticalRecoilMultiplier_C | Weapon.VerticalRecoilMultiplier | VerticalRecoil_MountedGun | ID.Item.HeavyTankMountedMachineGun |
| Driver | ImpactDamageReduction | Vehicle | GE_Vehicle_ImpactReductionMultiplier_C | Health.ImpactReductionMultiplier | ImpactDamageReduction | none |
| Driver | FuelUsageReduction | Vehicle | GE_Vehicle_FuelUsageReductionMultiplier_C | FuelUsageReductionMultiplier | FuelUsageReduction | none |
| Driver | AimDownSightSpeed.MountedGun | Item | GE_Weapon_AimTime_C | Weapon.AimTime | AimDownSight_MountedGun | ID.Item.HeavyTankMountedMachineGun |
| Driver | IncreasedHealth.SupplyCrate | SupplyCrate | GE_Vehicle_Health_C | Health | IncreasedHealth_SupplyCrate | none |

### 3a. Curve shapes (`CT_*Skills`)

Each CT row is a rich curve with keys at fixed times and constant extrapolation. There are 61 rows. Their values fall into two families:

| Family | Key points (Time, value) | Rows using it | Reading |
|---|---|---|---|
| Reduce | (0, 1.0), (2, 0.8), (3, 0.7), (4, 0.6) | 36 | Recoil and aim-time multipliers; the value falls as the skill rank rises |
| Boost | (0, 1.0), (2, 1.2), (4, 1.4) | 25 | Movement, sprint, stamina regen, equip and ready-to-fire speed; the value rises as the rank rises |

The `Time` axis is named only as `Time`. The keys sit at 0, 2, 3 and 4, so the rank-to-time mapping is inferred, not read from the data. Lower-is-better reading for recoil and aim is an inference from the family shape.

Three CT rows are never referenced by a skill row: `IncreasedSpottingDuration`, `IncreasedSpottedTime`, `IncreasedDetonatorRange`. They may be retired skills. The export cannot show whether any runtime path reads them.

---

## 4. Reward Scaling Curves (`CurveFloat` assets)

These curves scale the rewards documented in the rewards doc. The input axis is inferred from the asset name unless stated. Curves with keys clamp to their first and last key outside the key range; the `DefaultValue` field only applies to curves with no keys.

| Asset | Input axis | Key points (input, output) |
|---|---|---|
| CRV_Challenges_Curves_DeploySupplyCrate_XP | supply crate deploy input (unclear, 0 to 2,500) | (0, 0), (500, 0.1), (1,000, 0.25), (2,000, 0.5), (2,500, 1) |
| CRV_Challenges_Curves_DestroySupplyCrate_Cash | supply crate destroy input (unclear, 0 to 5,000) | (0, 1), (500, 1.1), (1,000, 1.25), (2,000, 1.5), (2,500, 2), (5,000, 3) |
| CRV_Challenges_Curves_DestroyVehicleAssist_DamageFraction | damage fraction of the vehicle (0 to 1) | (0, 0), (1, 1) |
| CRV_Challenges_Curves_DestroyVehicle_FactionScoreDifference | faction score difference (negative = behind) | (-50, 2), (-50, 1.75), (-20, 1.5), (-10, 1.25), (-5, 1), (0, 1) |
| CRV_Challenges_Curves_EndOfMatch_CashEarned | cash earned in the match (passes through 1:1 up to 100,000) | (0, 0), (10,000, 10,000), (20,000, 20,000), (30,000, 30,000), (40,000, 40,000), (50,000, 50,000), (60,000, 60,000), (70,000, 70,000), (80,000, 80,000), (90,000, 90,000), (100,000, 100,000) |
| CRV_Challenges_Curves_EndOfMatch_XPEarned | XP earned in the match (passes through 1:1 up to 2,500) | (0, 0), (500, 500), (1,000, 1,000), (1,500, 1,500), (2,000, 2,000), (2,500, 2,500) |
| CRV_Challenges_Curves_HealPlayer_HealPlayer | heal fraction (inferred) | (0, 0.25), (0.3, 0.25), (0.4, 0.5), (0.5, 0.7), (0.6, 0.85), (0.7, 0.95), (0.8, 1) |
| CRV_Challenges_Curves_HealPlayer_ReviveHealPlayer | revive heal fraction (inferred) | (0, 0), (0.4, 0.2), (1, 1) |
| CRV_Challenges_Curves_PlayerDelivered_PlayerCount | player count delivered | (0, 1), (10, 1.1), (20, 1.2), (30, 1.3), (40, 1.5), (50, 2), (75, 3) |
| CRV_Challenges_Curves_PlayerKill_DistanceScalar | kill distance (Unreal units, likely cm; 30,000 = 300 m) | (0, 1), (30,000, 1.5), (40,000, 2), (50,000, 2.5), (60,000, 3), (70,000, 3.25), (80,000, 3.5), (90,000, 4) |
| CRV_Challenges_Curves_PlayerKill_DistanceScalar_Artillery | artillery kill distance (Unreal units, likely cm) | (0, 1), (50,000, 1.25), (150,000, 1.5) |
| CRV_Challenges_Curves_PlayerKill_KillAssist | assist index (unclear, input 1 to 2) | (1, 0), (2, 1) |
| CRV_Challenges_Curves_PurchaseFromSupplyCrate_XP | supply crate purchase input (unclear, 0 to 1,000) | (0, 0), (1, 1), (10, 5), (250, 25), (500, 50), (750, 100), (1,000, 200) |
| CRV_Challenges_Curves_VehicleAirborne_ElapsedAirTimeCurve | elapsed air time (seconds, inferred) | (0, 0), (1.5, 1), (2, 3), (3, 5), (4, 8) |
| CRV_Meta_MatchScoreScalar | match score (18 to 30) | (18, 0.6), (21, 0.7), (24, 0.8), (27, 0.9), (30, 1) |
| CRV_Meta_PlayerCountCashScalar | player count (0 to 60) | (0, 0), (10, 0), (10, 0.15), (20, 0.2), (25, 0.3), (30, 0.4), (35, 0.5), (40, 0.7), (45, 0.8), (50, 0.9), (60, 1) |

**Flag:** [`DT_Meta_RewardScalingCurves`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Rewards/DT_Meta_RewardScalingCurves.json) row `Challenges.Rewards.PlayerCountXPScalar` points at [`CRV_Meta_PlayerCountCashScalar`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Rewards/Curves/CRV_Meta_PlayerCountCashScalar.json), the same asset as the cash row ([`CRV_Meta_PlayerCountCashScalar`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Rewards/Curves/CRV_Meta_PlayerCountCashScalar.json)). The XP scalar may be a copy-paste reference rather than its own curve. The rewards doc lists [`DT_Meta_RewardScalingCurves`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Rewards/DT_Meta_RewardScalingCurves.json) as not yet pulled, so this scalar's effect is not documented there. Verify in-game before relying on an XP-specific scale.

---

## 5. Achievements ([`Achievements/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Meta/Achievements))

[`DT_Achievements`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Achievements/DT_Achievements.json) has **10 rows**, one per achievement, with an ID and a display name. It has no reward or threshold fields. The 10 achievement StateTrees hold the logic. Each one watches for a game event or a match stat, evaluates it, and moves to its unlock state. Threshold values are not serialized in the export (section 12), so this table lists the state count, the event tags and the classes each tree listens to, and the named nodes.

| Row ID | Display name |
|---|---|
| ACH_TUTORIAL_COMPLETED | Complete The Tutorial |
| ACH_TUTORIAL_PUNCH_KRISTOPHER | Punch Kristopher |
| ACH_ECONOMY_TOP_CASH_EARNER | Top Cash Earner |
| ACH_ECONOMY_SINGLE_LIFE_PROFIT | Single Life Profit |
| ACH_ECONOMY_LOADOUT_SPEND | Loadout Spender |
| ACH_SURVIVAL_CONTROL_ZONE_SURVIVOR | Control Zone Survivor |
| ACH_COMBAT_LONG_SHOT | Long Shot |
| ACH_MATCH_CLEAN_SWEEP | Clean Sweep |
| ACH_COMBAT_RICOCHET_KILL | Ricochet Kill |
| ACH_COMBAT_DEFIBRILLATOR_KILL | Defibrillator Kill |

| StateTree | States | Event tags | Named nodes (first 7) |
|---|---|---|---|
| ST_Achievement_CleanSweep | 4 | none | Own Score Above Zero, Opposition Scoreless, Get Faction Tag |
| ST_Achievement_ControlZoneSurvivor | 11 | Event.StateTree.PlayerSpawned, Event.StateTree.PlayerVitalityChanged | Global - Spawn Listener, Global - Vitality Listener, Get Pawn from PlayerState, Survive Timer - Delay, Pawn Is Alive, Died - Object Equals |
| ST_Achievement_DefibrillatorKill | 5 | Event.StateTree.DefibrillatorVitalityChanged | Listen For Vitality Changed, ObjectEquals, TagEqual, ActorHostility, Has Tags |
| ST_Achievement_LoadoutSpend | 5 | Event.StateTree.LoadoutPurchased | Listen for Event, TagEqual, Integer Compare |
| ST_Achievement_LongShot | 5 | Event.StateTree.LongShotVitalityChanged | Listen For Vitality Changed, ObjectEquals, TagEqual, ActorHostility, FloatCompare, Has Tags |
| ST_Achievement_PunchKristopher | 5 | Event.StateTree.CharacterDamaged | Listen For Character Damaged, Target Is Kristopher, Damage Is Melee, ObjectEquals |
| ST_Achievement_RicochetKill | 5 | Event.StateTree.RicochetVitalityChanged | Listen For Vitality Changed, ObjectEquals, TagEqual, ActorHostility, Has Tag |
| ST_Achievement_SingleLifeProfit | 5 | Event.StateTree.ProfitChanged | Listen for Event, Integer Compare |
| ST_Achievement_TopCashEarner | 4 | none | Placement Equal 1, Earned Greater 0, Get Players Match Stat |
| ST_Achievement_TutorialCompleted | 3 | Event.StateTree.TutorialCompleted | Listen for Event |

**Notes**
- [`ST_Achievement_LongShot`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Achievements/StateTrees/ST_Achievement_LongShot.json), [`ST_Achievement_RicochetKill`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Achievements/StateTrees/ST_Achievement_RicochetKill.json) and [`ST_Achievement_DefibrillatorKill`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Achievements/StateTrees/ST_Achievement_DefibrillatorKill.json) all listen to `WDPlayerVitalityChangedMessage`, each with its own event tag. These are kill-condition variants of one pattern.
- [`ST_Achievement_CleanSweep`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Achievements/StateTrees/ST_Achievement_CleanSweep.json) reuses the `Evaluate TopCashEarner` state name from [`ST_Achievement_TopCashEarner`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Achievements/StateTrees/ST_Achievement_TopCashEarner.json), but its conditions are score-based (`Own Score Above Zero`, `Opposition Scoreless`).
- All achievement trees use the `WDChallengeStateTreeSchema` schema, the same schema the missions use.

---

## 6. Missions (`Missions/`)

[`DT_PassiveMissions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/DT_PassiveMissions.json) has 3 rows. Each has five challenge tiers and a difficulty weight of 1, and no unlock prerequisite.

| Passive mission | Challenge tiers | Difficulty weight | Unlock prerequisite |
|---|---|---|---|
| Mission.Passive.EarnCash | 1, 2, 3, 4, 5 | 1 | none |
| Mission.Passive.EarnAnyRoleXp | 1, 2, 3, 4, 5 | 1 | none |
| Mission.Passive.TimePlayed | 1, 2, 3, 4, 5 | 1 | none |

Two mission StateTrees track objective progress and auto-complete it:

| StateTree | States | Event tags | Named nodes (first 8) |
|---|---|---|---|
| ST_Challenge_EarnResource | 7 | none as a tag; listens to WDPlayerResourceChangedMessage | Load Objective Progress, Integer Expression, Wait for Event, B Update Value from Resource Event, Update Objective Progress, B Auto Complete, Integer Compare |
| ST_Challenge_TimePlayed | 7 | none (timer driven: UTC now and time difference) | Load Objective Progress, Integer Expression, B Get Utc Now, Delay Task, B Get Time Diff, Update Objective Progress, B Auto Complete, B Check Time Diff |

[`DT_PassiveMissionChallenges`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/DT_PassiveMissionChallenges.json) has **15 rows**, five tiers for each passive mission. Each tier sets an objective target and an `Attribute.Meta.Currency.Intel` reward quantity:

| Challenge tier | Objective (target) | Reward (Intel) |
|---|---|---|
| `Mission.Passive.EarnCash` .1 to .5 | `Challenges.Objective.CashEarned`: 5,000, 12,000, 30,000, 80,000, 200,000 | 100, 200, 300, 400, 500 |
| `Mission.Passive.EarnAnyRoleXp` .1 to .5 | `Challenges.Objective.RoleXpEarned`: 500 at every tier | 100, 200, 300, 400, 500 |
| `Mission.Passive.TimePlayed` .1 to .5 | `Challenges.Objective.TimePlayed`: 1,800 at every tier | 100, 200, 300, 400, 500 |

Both mission StateTrees are referenced here: [`ST_Challenge_EarnResource`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/StateTrees/ST_Challenge_EarnResource.json) for the cash and XP missions, [`ST_Challenge_TimePlayed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/StateTrees/ST_Challenge_TimePlayed.json) for time played.

---

## 7. Currency, Exchange and Gold Market

| Currency tag | Display name | Initial balance |
|---|---|---|
| Attribute.Meta.Currency.Cash | Cash | 10,000 |
| Attribute.Meta.Currency.GoldBars | Gold Bars | 0 |

[`DT_ExchangeDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/ExchangeDefinitions/DT_ExchangeDefinitions.json) has one row for `Attribute.Meta.Currency.GoldBars` with ExchangeRates: an empty list. No cash-to-gold rate is set in this build.

[`DT_GoldMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Collection/DT_GoldMarket.json) has 27 entries worth **275 Gold Bars** in total. Expiration types: EXPIRATION_NO_END_TIME x1, NO_EXPIRATION x26. The `EXPIRATION_NO_END_TIME` name suggests the entry has no end time, but the export has no end-time value to confirm this.

| Category | Items | Gold Bar cost | Total bars (all items) | Tile sizes |
|---|---|---|---|---|
| BlackAndGold | 1 | 30 | 30 | HERO_TILE x1 |
| DigitalWood | 5 | 5 to 15 | 50 | LARGE_SQUARE x1, SMALL_SQUARE x2, SMALL_RECTANGLE x2 |
| TwoToneDesert | 15 | 5 to 15 | 150 | SMALL_SQUARE x6, SMALL_RECTANGLE x6, LARGE_SQUARE x3 |
| Emote | 3 | 5 | 15 | LARGE_SQUARE x1, SMALL_SQUARE x2 |
| ChocolateChip | 3 | 10 | 30 | SMALL_RECTANGLE x2, LARGE_RECTANGLE x1 |

Gold-market entries are cosmetics: weapon skins, vehicle skins, a parachute skin, and emotes (`Id.Emote.*`).

[`DT_CosmeticSets_Debug`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Cosmetics/DT_CosmeticSets_Debug.json) has 12 sets: `Meta.Cosmetic.Featured`, `Meta.Cosmetic.BlackAndGold`, `Meta.Cosmetic.Frogman`, `Meta.Cosmetic.DigitalWood`, `Meta.Cosmetic.TripleDesert`, `Meta.Cosmetic.DigitalFlora`, `Meta.Cosmetic.TwoToneDesert`, `Meta.Cosmetic.Emote`, `Meta.Cosmetic.Bobblehead`, `Meta.Cosmetic.Taxi`, `Meta.Cosmetic.FactionLogo`, `Meta.Cosmetic.ChocolateChip`. The `_Debug` name suggests they are test data.

---

## 8. Investments (debug data)

| Investment ID | Display name | Purchase cost |
|---|---|---|
| Id.Investment.DebugOne | Debug One Title | 100 (Cash) |
| Id.Investment.DebugTwo | Debug Two Title | 200 (Cash) |

Assets: [`DA_TestInvestmentOne`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Investments/DA_TestInvestmentOne.json) and [`DA_TestInvestmentTwo`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Investments/DA_TestInvestmentTwo.json) (`WDInvestmentDefinition`, each with an empty `WDInvestmentCore` archetype). Map icons are borrowed UI textures (`T_UI_Icon_AddToSquad` and `T_UI_Icon_FiringMode_FullAuto_White_256`), and the second asset reuses the title text and text key for its description. Both are debug leftovers with no live use.

[`DT_MockInvestments`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/MockInvestments/DT_MockInvestments.json) has one row (`Meta.MockInvestment.Definitions`) with two placeholder investments and one active ID, `Meta.MockInvestment.Bandage`:

| Mock key | Item | Quantity | Cash cost | Wait (seconds) |
|---|---|---|---|---|
| Meta.MockInvestment.AK74M | Id.Item.AK74M | 1 | 1,000 | 43,200 |
| Meta.MockInvestment.Bandage | Id.Item.Bandage | 5 | 200 | 43,200 |

---

## 9. Season, Resource Effect, Demo Reward, Client Configs

- **Season:** [`DT_SeasonDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/DT_SeasonDefinitions.json) sets `CurrentSeasonNumber = 1` and an empty `SeasonDefinitions` list.
- **Resource effect:** [`DT_Meta_ResourceEffects`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Resources/Effects/DT_Meta_ResourceEffects.json) maps `Meta.Effect.Resource` to `GE_Meta_ResourceChange`, the GameplayEffect used for resource changes. Its magnitude is not in this table.
- **Demo reward:** [`DT_DemoRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/Demo/DT_DemoRewards.json) row `Meta.Progression.Context.DefaultReward` gives `Attribute.Meta.Currency.Cash` a base of 100. It is divided by 2 when the context carries `Meta.Damage.Category.Friendly`. This looks like a template row, not a live reward.
- **Client configs:** [`DT_ClientHotConfigs`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/ClientHotConfigs/DT_ClientHotConfigs.json) has three INI-style blobs. Values confirmed in the text: `ServerBrowserSubsystem` sets `MaxSelectedRegions=3`, `ServerIDLength=6` and `bAllowGlobalSearch=False`. `AuthSubsystem` sets `bEnableFulfillOrders=True`. `CommunicationSubsystem` sets `MaxLoginRetries=2`, `LoginRetryDelaySeconds=30.0`, `LoginRetryJitterFraction=0.25`, login give-up retry delays of 10 to 300 seconds, `LoginHangingTimeoutSeconds=60.0`, `LoginStuckTimeoutSeconds=90.0`, plus voice and channel join retry settings. The blob also holds commented-out voice endpoint overrides, which are not reproduced here.

---

## 10. Challenge Tables Covered Elsewhere

- [`DT_ChallengeRewards_EndOfMatch`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_EndOfMatch.json) (5 rows: three placements, a `FactionWinBonus` row and a `Bonus` row). Rewards doc, sections 10 and 14.
- [`DT_ChallengeRewards_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_SessionEvents_Shared.json) (298 rows, about 8.0 MB raw, the largest file in Meta). Rewards doc, section 15. Row tags cover `PlayerKill` (with assist variants), `VehicleDestroyed` (per vehicle, per assist type), `DestroyVehicleSection`, `HealPlayer`, `RevivePlayer`, `DestroySupplyCrate`, `PurchaseFromSupplyCrate`, `DeploySupplyCrate`, `RepairVehicle`, `RefuelVehicle`, `VehicleAirborne`, `ZoneEntry` and `ZonePresence`, plus tip and pre-tip events.
- [`DT_RoleMasteryDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Levels/Roles/DT_RoleMasteryDefinitions.json) (6 role rows, 100 levels each). Rewards doc, section 1.
- [`DT_Challenges_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_Challenges_SessionEvents_Shared.json): **10 rows**, one per achievement (`Achievement.*` tags, matching [`DT_Achievements`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Achievements/DT_Achievements.json)). Its curve dependencies are in [`Challenges/RewardData/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Meta/Challenges/RewardData).

---

## 11. How Values Combine

- **Unlock:** a node's cash cost is paid once. The node unlocks when the role level meets the node's `MinLevel`. The export gives one prerequisite per node, so no AND or OR logic between prerequisites is visible here.
- **Skill effect:** the attribute receives the literal or the curve value at the skill rank. The GE applies only when the held item matches the gate tag. Skills that share a GE (for example `GE_Weapon_AimTime_C` used by several AimDownSightSpeed rows) differ by curve row and gate tag.
- **Reward scaling:** the scaling curves are evaluated against their input (player count, match score, cash or XP earned) and multiply the base reward. The base values and the full formula are in the rewards doc.

---

## 12. Still Not Pulled / Limitations

- **Achievement and mission thresholds are not in the export.** The StateTrees reference parameters such as `DistanceThreshold` in [`ST_Achievement_LongShot`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Achievements/StateTrees/ST_Achievement_LongShot.json), and integer comparisons in `LoadoutSpend`, `SingleLifeProfit` and `TopCashEarner`, but no values are serialized. [`DT_Achievements`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Achievements/DT_Achievements.json) has no reward or threshold fields, so achievement rewards and thresholds cannot be recovered from this folder.
- **Wardog level track is unexplained.** The Wardog tree gates on `MinLevel` up to 150 with no `MetaId`. No matching XP table or role row exists in the export.
- **Skill curve time axis is unlabeled.** The mapping from skill rank to curve `Time` is inferred.
- **Unnamed fields.** Some fields in the challenge tables are unnamed ("unnamed field"). Their meaning is inferred from values only.
- **Empty tables.** The exchange rates in [`DT_ExchangeDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/ExchangeDefinitions/DT_ExchangeDefinitions.json), and the season list in [`DT_SeasonDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/DT_SeasonDefinitions.json) have no data, so they are noted as present but empty.
- **Debug and template content.** `DA_TestInvestment*`, [`DT_MockInvestments`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/MockInvestments/DT_MockInvestments.json), [`DT_CosmeticSets_Debug`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Cosmetics/DT_CosmeticSets_Debug.json) and [`DT_DemoRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/Demo/DT_DemoRewards.json) look like test data. They are listed for completeness and may not ship.

---

## 13. Wagers (`Wagers/`)

The wager vendor is new in this update. It is unlocked by `Meta.Unlocks.Wager` and sits in spawn. A player stakes cash on in-match objectives, with conditions that change the payout. The folder has 7 tables, all new.

[`DT_WagerPricing`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerPricing.json) holds the stake limits and payout caps:

| Setting | Value |
|---|---|
| Minimum stake | 2,500 |
| Maximum stake | 100,000 |
| Maximum payout | 5,000,000 |
| Fold bonus step | 0.25 |
| Lives odds | 1.009, 1.003, 1.002, 1.001 |

Two more pricing fields are unnamed fields (values 1.001 and 100.0).

[`DT_WagerActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerActions.json) has 4 actions. Each has a display name with a `{Count}` placeholder:

| Action | Display name | Player objectives |
|---|---|---|
| `Wager.Action.Kills` | Get {Count} Kills | 8 |
| `Wager.Action.Revives` | Revive {Count} Teammates | 4 |
| `Wager.Action.PlayerDelivery` | Deliver {Count} people to the Control Zone | 1 |
| `Wager.Action.VehiclesDestroyed` | Destroy {Count} Occupied Vehicles | 1 |

[`DT_WagerObjectiveCatalog`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerObjectiveCatalog.json) has 17 objectives. Three are test entries (`TestParked`, `TestLockedWagerNode`, `TestLockedNodeInNoTree`), and the table below lists the other 14:

| Objective | Action | Count | Odds | Conditions |
|---|---|---|---|---|
| Kills3 | Kills | 3 | 1.001 | 0 |
| Kills2WithHeadshot | Kills | 2 | 1.2012 | 1 |
| Revives2 | Revives | 2 | 1.001 | 0 |
| PlayerDelivery3 | PlayerDelivery | 3 | 1.001 | 0 |
| VehiclesDestroyed1 | VehiclesDestroyed | 1 | 1.001 | 0 |
| Hammertime1 | Kills | 10 | 1.5 | 2 |
| Hammertime2 | Kills | 20 | 1.64 | 2 |
| Hammertime3 | Kills | 25 | 1.72 | 2 |
| MedicMarathon1 | Revives | 30 | 1.37 | 2 |
| MedicMarathon2 | Revives | 40 | 1.44 | 2 |
| MedicMarathon3 | Revives | 50 | 1.51 | 2 |
| AllDrillerNoFiller1 | Kills | 15 | 1.57 | 2 |
| AllDrillerNoFiller2 | Kills | 20 | 1.64 | 2 |
| AllDrillerNoFiller3 | Kills | 25 | 1.72 | 2 |

All 14 have no cooldown. The three test entries include a 300-second cooldown and two entries that point at unlock nodes.

[`DT_WagerConditions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerConditions.json) has 50 rows. Of these, 39 are per-action conditions (13 for kills, 11 for player delivery, 9 for vehicles destroyed, 6 for revives). The other 11 are standalone conditions: `Naked`, `Deathwish`, `TimeLimit`, `NoVehicles`, `NoResupply`, `InControlZone`, `InHotzone`, `NoArmor`, `Loadout20k`, `NoBandages` and `Under50HP`.

The remaining tables are presentation and challenge wiring: [`DT_WagerChallenges`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerChallenges.json) (4 rows, one per action, named "Get Kills", "Dropoff People", "Revive Teammates" and "Destroy Occupied Vehicles"), [`DT_EntityData_UI_Wagers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_EntityData_UI_Wagers.json) (1 row, the vendor's name and description) and [`DT_TooltipData_Wagers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_TooltipData_Wagers.json) (2 rows, one tooltip each for the action and condition tiles).

