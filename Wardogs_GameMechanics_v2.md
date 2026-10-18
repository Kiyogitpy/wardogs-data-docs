---
title: "GameMechanics"
parent: "Content"
---

# Wardogs — Game Mechanics Reference
*Extracted from cooked game data under [`Content/GameMechanics`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics) (467 files, 898 export blocks, UE 5.7 build `++Wardogs+Live-CL-516586`). Numbers are the raw values stored in the DataAssets and DataTables. Where the meaning of a field is inferred or unknown, the doc says so.*

> **Scope note:** The cash and reward tables ([`Gamemode/Data/DT_CashRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_CashRewards.json), [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json), [`DT_AssistCashRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_AssistCashRewards.json), [`DT_CashRewardModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_CashRewardModifiers.json), and everything under [`Gamemode/Data/CashRewardsDataTable/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable)) are covered in **`Wardogs_Rewards_and_Progression_v2.md`**. This doc does not repeat them. Note that [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) and [`DT_CashRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_CashRewards.json) are the stale placeholder layer described in that doc.

---

## Season 02 update (2026-10-15)

- **Files:** 20 added and 1 removed (486 files, was 467).
- **Added:** [`DA_125x570mm_ProjectileData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/125x570mm/DA_125x570mm_ProjectileData.json) (base damage 150, explosion radius 750, mass 23.0); 6 `CR_SuppressionCurve_*` curves; 2 action definitions ([`DA_Action_AccessLooting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Actions/UI/DA_Action_AccessLooting.json), [`DA_Action_AccessWagerVendor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Actions/UI/DA_Action_AccessWagerVendor.json)); 8 door and decorator assets; [`DT_PingTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Communication/Pings/DT_PingTypes.json); [`DT_InfantryData_ArchetypeCaliberModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json); [`CRV_DamageIndicator_IntensityResponse`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_DamageIndicator_IntensityResponse.json).
- **Removed:** `AR_SuppressionCurve` (the 545mm projectile now uses [`CR_SuppressionCurve_Medium`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/CR_SuppressionCurve_Medium.json)).
- **Projectile base damage:** 308Winchester 60 → 45, 50Cal 107 → 90, 762mm 42 → 34, 762x54mm 55 → 44.
- **Projectile mass:** 35x228mm 0.15 → 0.375.
- **Bone multipliers:** AR torso upper 1.0 → 0.885; Sniper head 3.2 → 4.2667; DMR head 2.5 → 2.45; LMG head 2.3 → 2.35; CombatBow torso upper 1.9 → 2.07; Minigun head 2.5 → 1.25 (neck 0.98). New turret rows [`STN_06`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/STN_06.json) and `HMG.MWSY_001`.
- **Armour and helmet:** new rule for Bullet from Sniper against the High arm class, +28% (Armor).
- **Infantry rules:** RifledSlug vs Armor −13% → −30%. New rules: Molotov vs SuperHeavy −30%, Arrow vs Heavy −10% and SuperHeavy −34%, 50Cal per-location rules.
- **Vehicle seat reduction:** ROT_01 and Littlebird Small/Medium −50% → −25%, High −20% → −15%. New [`ROT_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/ROT_04.json) row with the same values as ROT_01.
- **Vendors:** AttachmentMarket top price 1800 → 1500 (`MZL_04`). GearMarket LargeBackpack 2400 → 1600, LargeSlingBackpack 3500 → 2400, ExtraLargeSlingBackpack 5000 → 4000. WeaponMarket gains `125x570mm` ammo at 210.
- **Destructibles:** building definitions 8 → 14, decorators 7 → 9.
- **Action definitions:** `BHActionDefinition` 98 → 100 (UI folder 15 → 17).
- **Settings:** `Controls.LookAccelMaxMultiplier` minimum 0.5 → 1.2, maximum 10.0 → 5.0, default 1.6 → 1.5.
- **Curves:** CurveFloat 60 → 66, player curves 8 → 9.

---

## 1. Folder Map

| Folder | Blocks (approx.) | What it holds |
|---|---|---|
| `Actions/` | ~117 | Action definitions (`BHActionDefinition` 100, `WDActionDefinition` 16) with tags, activation context and action class. Also [`DT_EmoteData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Actions/Character/DT_EmoteData.json). |
| [`DamageSystem/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/DamageSystem) | ~14 | Damage categories, ammo modifiers, bone/hit-location multipliers, armour and helmet rules, vehicle-seat reduction, hit-location maps. |
| `Gamemode/` | ~32 | Reward tables (see the rewards doc), `WDFactionData` (4 factions), scalar reward curves, EQS spawn queries. |
| `Inventory/` | ~78 | Projectile stats (`WDProjectileData`, 32 assets), suppression curves, inventory operation rules, mag-packing curves. |
| [`Player/PlayerCharacter/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter) | ~138 | Enhanced Input (`BHInputAction` 98, `InputMappingContext` 20, key settings 106), trigger and modifier classes, camera and perspective components, movement audio/effects config. |
| `Settings/` | ~67 | User-setting definitions (numeric, discrete, presets, buttons) in 7 settings DataTables, plus controller configs. |
| [`WorldInteractable/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/WorldInteractable) | ~38 | Vendor markets (4 DataTables), destructible door/building definitions, target dummy blueprint. |
| `AI/`, [`Communication/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Communication), [`GameplayEffects/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/GameplayEffects) | ~13 | Blackboard, EQS queries, AI services curve, assistance-request DataTable, tagged gameplay effects, curve table. |

---

## 2. Damage System

### 2a. Damage Categories ([`DA_GlobalDamage_Categories`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DA_GlobalDamage_Categories.json))

Used as `PriorityCategory` on modification entries. The list order is the category list in the asset (exact resolution order not verified).

| # | Category tag |
|---|---|
| 1 | `Meta.Damage.Category.Calibre` |
| 2 | `Meta.Damage.Category.AmmoModifier` |
| 3 | `Meta.Damage.Category.CaliberEffectiveness` |
| 4 | `Meta.Damage.Category.Bone` |
| 5 | `Meta.Damage.Category.PenetrationEffectiveness` |
| 6 | `Meta.Damage.Category.Tracer` |
| 7 | `Meta.Damage.Category.Weapon` |
| 8 | `Meta.Damage.Category.Armor` |
| 9 | `Meta.Damage.Category.Melee` |
| 10 | `Meta.Damage.Category.Ricochet` |
| 11 | `Meta.Damage.Category.Penetration` |
| 12 | `Meta.Damage.Category.Friendly` |

### 2b. Hit Locations ([`DA_GlobalDamage_HitLocations_Player`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/HitLocationDataAssets/DA_GlobalDamage_HitLocations_Player.json))

The skeleton bone names map to 12 hit-location classes. These classes are the columns of the bone table in 2c.

The lookup is an exact match on the hit bone name (`FHitResult.BoneName`) in `DamageHitLocations`. There is no walk up parent bones. A bone without an entry, or a hit with no bone, gets no hit location (the empty tag). The asset is found per actor class through the damage subsystem's `ClassToHitLocations` (`0x6F01BB0` → `0x6BB8D00`). With no hit location, the entries that require `Meta.Damage.HitLocation.Infantry` do not apply ([DamagePipeline §4](Wardogs_DamagePipeline_v2.md#4-entry-selection) rule 4; entries 5-7, 10, 138-143), and the armor hook removes all armor tags ([DamagePipeline §7.6](Wardogs_DamagePipeline_v2.md#76-the-bullet-event)).

| Bone(s) | Hit location class |
|---|---|
| `head` | Head |
| `neck_01` | Neck |
| `clavicle_l`, `clavicle_r`, `spine_05` | Torso.Upper |
| `spine_04` | Torso.Middle |
| `spine_03`, `spine_02`, `spine_01` | Torso.Lower |
| `upperarm_l`, `upperarm_r` | Arm.Upper |
| `lowerarm_l`, `lowerarm_r` | Arm.Lower |
| `hand_l`, `hand_r` | Arm.Hand |
| `pelvis` | Pelvis |
| `thigh_l`, `thigh_r` | Leg.Thigh |
| `calf_l`, `calf_r` | Leg.Calf |
| `foot_l`, `foot_r` | Leg.Foot |

Bodies that can be hit: the live player's physics asset `PA_TPCharacter_Simplified` has 20 bodies, one per bone in this table except `spine_01` and `spine_02`, so every traced body gets a hit location and those two entries are never produced. The ragdoll asset (`PA_TPCharacter_Simplified_Physics`) adds `spine_02` and a collision-disabled `root` body and drops `spine_05`.

The asset also has 2 `DamageImpactRemap` entries: `spine_01` is remapped to `pelvis`, and `spine_05` to `spine_04`. The remap is not used for damage. Damage looks up the hit bone as traced (`0x6F01BB0`, called with `FHitResult.BoneName` by the armor hook `0x6B52A40`, by `0x6EF8DE0` and by three more damage-side callers; none applies the remap), so a hit on the `spine_05` body is `Torso.Upper`. A sixth caller, `AWDMoverPlayerCharacter` slot 330 (`0x6E830E0`), does not remap either; its role is not traced. The remap (`0x6F01530` → `0x6BB8D40`) is applied in two other places: when a ragdoll starts, to choose the body that receives the hit impulse (`0x6EF8460`); and in the character anim instance (`0x6A7AC00`, `0x6A7B2C0`), which remaps first and then looks up the hit location for the hit-reaction animation (so there `spine_05` gives `Torso.Middle`).

### 2c. Bone Damage Multipliers ([`DT_InfantryData_BoneDamageModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_BoneDamageModifiers.json))

Each row is a damage-type tag. Values are the per-hit-location multiplier. The `Universal` row is the fallback for anything not listed separately (inferred from the row name).

| Row | Head | Neck | Torso.Up | Torso.Mid | Torso.Low | Pelvis | Arm.Up | Arm.Low | Arm.Hand | Leg.Thigh | Leg.Calf | Leg.Foot |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Universal | 1.0 | 0.75 | 1.1 | 1.0 | 0.95 | 0.9 | 0.6 | 0.5 | 0.3 | 0.6 | 0.5 | 0.3 |
| AR | 2.35 | 2.35 | 0.885 | 0.97 | 0.97 | 1.0 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 |
| SMG | 2.1 | 2.1 | 1.05 | 1.05 | 1.05 | 1.05 | 1.3 | 1.3 | 1.3 | 1.3 | 1.3 | 1.3 |
| LMG | 2.35 | 2.35 | 0.885 | 0.97 | 0.97 | 1.0 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 |
| Shotgun | 1.5 | 1.5 | 0.9 | 0.9 | 0.9 | 0.9 | 1.05 | 1.05 | 1.05 | 1.05 | 1.05 | 1.05 |
| DMR | 2.45 | 2.45 | 1.07 | 1.18 | 1.24 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 |
| Sniper | 4.2667 | 4.2667 | 2.4 | 1.9333 | 1.9333 | 1.7333 | 1.5 | 1.5 | 1.5 | 1.5 | 1.5 | 1.5 |
| Pistol | 2.1 | 2.1 | 1.05 | 1.05 | 1.05 | 1.05 | 1.3 | 1.3 | 1.3 | 1.3 | 1.3 | 1.3 |
| DamageType.Melee | 1.5 | 1.5 | 1.0 | 1.0 | 1.0 | 1.0 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 |
| CombatBow | 2.3 | 2.3 | 2.07 | 1.96 | 1.5 | 1.0 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 |
| Launcher | 1.5 | 1.5 | 1.0 | 0.6 | 0.6 | 0.6 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 |
| Vehicle.Cannon | 1.0 | 1.0 | 0.6 | 0.6 | 0.6 | 0.6 | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 |
| Vehicle.Turret.Minigun | 1.25 | 0.98 | 0.57 | 0.62 | 0.65 | 0.47 | 0.47 | 0.47 | 0.47 | 0.47 | 0.47 | 0.47 |
| Vehicle.Turret.MachineGun | 2.35 | 2.35 | 1.0 | 1.0 | 1.0 | 1.0 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 |
| Vehicle.Turret.Artillery | 2.35 | 2.35 | 0.885 | 0.97 | 0.97 | 1.0 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 |
| Vehicle.Turret.Heavy | 2.35 | 2.35 | 0.885 | 0.97 | 0.97 | 1.0 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 |
| Vehicle.Turret.STN_06 | 2.2 | 2.2 | 1.2 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Vehicle.Turret.HMG.MWSY_001 | 2.2 | 2.2 | 1.2 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Vehicle.HelicopterCannon | 3.2 | 3.2 | 1.8 | 1.8 | 1.8 | 1.3 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 |
| Vehicle.HelicopterRocket | 1.5 | 1.5 | 1.0 | 0.6 | 0.6 | 0.6 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 |

Head and neck are equal in every row except `Vehicle.Turret.Minigun`, where the neck value is lower. The [`STN_06`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/STN_06.json) and `HMG.MWSY_001` turret rows are new in this update.

### 2d. Ammo Type Penetration Effectiveness ([`DT_InfantryData_AmmoTypeEffectivenessPen`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json))

| Ammo tag | Modifier | Per-arm-class values (Small / Medium / High / Special) |
|---|---|---|
| `AmmoModifier.FMJ` | 1.0 | — |
| `AmmoModifier.Tracer` | 1.0 | — |
| `AmmoModifier.HollowPoint` | 1.5 | — |
| `AmmoModifier.HollowPoint.Tracer` | 1.5 | — |
| `AmmoModifier.ArmorPiercing` | 0.3 | 0.7 / 0.6 / 0.5 / 1.0 |
| `AmmoModifier.ArmorPiercing.Tracer` | 0.3 | 0.7 / 0.6 / 0.5 / 1.0 |

The per-arm keys use the `Meta.Damage.Arms.*` tag family. The name "Arms" is what the data uses; it is most likely an armour-class or penetration-tier axis, but that is not confirmed.

### 2e. Ammo Modifier Assets ([`DamageSystem/AmmoModifiers/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers), index in [`DT_AmmoModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DT_AmmoModifiers.json))

Each asset multiplies the listed attribute on the projectile when that ammo tag is active.

| Ammo modifier | PenetrationEffectivenessMult | EffectiveRangeMult | PenetrationExitSpeedMult | TracerChance |
|---|---|---|---|---|
| ArmorPiercing | 1.8 | 1.2 | 0.0 | — |
| ArmorPiercing.Tracer | 1.76 | 1.2 | 0.0 | 1.0 |
| HollowPoint | 0.1 | 0.8 | 0.15 | — |
| HollowPoint.Tracer | 0.1 | 0.8 | 0.15 | 1.0 |
| Tracer | 1.0 | 1.0 | 0.075 | 1.0 |

The index asset [`DT_AmmoModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DT_AmmoModifiers.json) maps each tag to its `DA_AmmoModifier_*` asset (5 rows, all five listed above).

### 2f. Infantry Damage Modification Rules ([`DT_GlobalDamage_InfantryData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json), row `Meta.Damage.Infantry`)

The row has 146 entries. Most are no-op rows (60 entries with no requirements and 0% change). The table below lists the non-trivial unique rules. Values are percentage changes. Negative is a reduction.

| Category | Source | Target / hit | Change | Notes |
|---|---|---|---|---|
| Friendly | Bullet (hits Infantry) | — | −50% | Friendly-fire reduction |
| Friendly | LargeHammer | — | −70% | Friendly melee |
| Bone | Bullet (hits Infantry) | — | −75% | Custom operation, bone category |
| Bone | Cannon (hits Infantry) | — | −75% | Custom operation |
| Bone | ExplosiveBlunt (hits Infantry) | — | −75% | Custom operation |
| Calibre | 122mm | — | −45% | |
| Calibre | 155mm + Outer | — | −55% | |
| Calibre | Outer + 120mm / 125mm / 84mm / 93mm / 40mm | — | −50% each | |
| Calibre | Outer + C4 | — | −40% | |
| Calibre | Explosive | SuperHeavy | −50% | |
| Calibre | Molotov | SuperHeavy | −30% | New in this update |
| Calibre | Rocket | Light / Medium / Heavy | −15% / −25% / −35% | Scales with target armour class |
| Calibre | Bullet (hits Infantry) | — | 0% | Custom operation, archetype caliber modifiers (new) |
| Calibre | 84mm + Inner | — | +1% | |
| Calibre | 7mmBuckshot / RifledSlug (hits Infantry) | — | 0% | Calibre pass-through |
| AmmoModifier | Bullet + ArmorPiercing | — | −20% | |
| AmmoModifier | Bullet + HollowPoint | — | +100% | |
| AmmoModifier | ExplosiveBlunt + Drone | — | +500% | |
| AmmoModifier | 7mmBuckshot | Helmet / Armor / SuperHeavy | −30% / −40% / −40% | |
| AmmoModifier | RifledSlug | Helmet / Armor / SuperHeavy | −5% / −30% / −12% | Armor value was −13% |
| AmmoModifier | Arrow | Any / Light / Helmet | 0% | |
| AmmoModifier | Arrow | Heavy / SuperHeavy | −10% / −34% | New in this update |
| AmmoModifier | 35x228mm / 20x102mm | Infantry | −30% | New in this update |
| Tracer | Bullet + HollowPoint | Helmet / Armor | −70% / −55% | New in this update |
| Penetration | Bullet (any target) | — | −50% | Custom operation |
| Penetration | Melee | Armor | −50% | Custom operation |
| PenetrationEffectiveness | Bullet + HollowPoint | Armor / Helmet | −40% / −40% | |
| PenetrationEffectiveness | 50Cal | Head / Neck | −15.6% | New in this update |
| PenetrationEffectiveness | 50Cal | Upper torso | −12.5% | New in this update |
| PenetrationEffectiveness | 50Cal | Middle / Lower torso | −6.0% and −7.7% | New in this update |
| PenetrationEffectiveness | 50Cal | Heavy / SuperHeavy | −10% / −12.5% and −10% / −20% | New in this update |
| PenetrationEffectiveness | Bullet, Cannon, ExplosiveBlunt (hits Infantry) | Armor / Helmet | 0% | Custom operation |

Friendly-fire and melee rules use the `Friendly` alignment. The rules are evaluated by `PriorityCategory` and `PriorityIndex`. The exact evaluation order and whether percentages stack additively or multiplicatively is not verified from the data.

### 2g. Armour and Helmet Rules ([`DT_GlobalDamage_ArmorData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_ArmorData.json))

| Row | Entries | Effect as recorded |
|---|---|---|
| `Meta.Damage.Armor.Ghillie` | 6 | Source Bullet, Explosive, Cannon, Impact, Melee and one more: each −100% in Armor category |
| `Meta.Damage.Helmet.Ghillie` | 6 | Same pattern as the Ghillie armour row |
| `Meta.Damage.Armor` | 9 | Bullet −60%, Explosive −85%, Melee −50% (Armor); Bullet from Sniper vs High arm class +28% (Armor, new); Bullet+Penetrate 0% (Penetration); Bullet+HollowPoint −30% (AmmoModifier); 7mmBuckshot −80% (AmmoModifier); target Ghillie −10000% (Armor) |
| `Meta.Damage.Helmet` | 8 | Bullet −60%, Explosive −85% (Armor); Bullet from Sniper vs High arm class +28% (Armor, new); Bullet+HollowPoint −30%; Bullet+ArmorPiercing +30% (AmmoModifier); Bullet+Penetrate 0%; 7mmBuckshot −80% (AmmoModifier); target Ghillie −1000% (Armor) |
| `Meta.Damage.Vehicle` (in [`DT_GlobalDamage_InfantryData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json) family) | 10 | Mostly 0% or no-op; HollowPoint ±40%; Ricochet 0% |

**Unclear:** the Ghillie rows set −100% on most sources, and the `Meta.Damage.Armor` row sets −10000% against the Ghillie tag. Whether this is intended as full immunity or a placeholder should be checked in game.

### 2h. Vehicle Seat Damage Reduction ([`DT_InfantryData_VehicleSeatDamageReduction`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json))

Each row is a vehicle variant. Its entries give `State.Player.Vehicle.SeatDamageReduction` by arm class. Values are percentage reductions applied to a player seated in that vehicle.

| Vehicle variant | Small / Medium | High | Special |
|---|---|---|---|
| Air.Rotary.ROT_01 (Default, MountedMachineGuns) | −25% | −15% | — |
| Air.Rotary.ROT_04 (Default, MountedMachineGuns) | −25% | −15% | — |
| Air.Rotary.Havoc (Default) | −90% | −50% | −60% |
| Air.Rotary.Littlebird (Default, RocketPods, MountedMachineGuns) | −25% | −15% | — |
| Land.Wheeled.Humvee (Default, MachineGun, Minigun) | −70% | −40% | — |

The Havoc is the only seat row with a Special entry. The Humvee, Littlebird and ROT_01 rows are identical across their variants. [`ROT_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/ROT_04.json) is new in this update.

### 2i. Hit-Location Asset for Infantry Damage

[`DA_GlobalDamage_HitLocations_Player`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/HitLocationDataAssets/DA_GlobalDamage_HitLocations_Player.json) holds the bone-to-class map in 2b; the damage subsystem picks it by the hit actor's class (`ClassToHitLocations`, `0x6F01BB0`). Where the `ClassToHitLocations` keys are registered is unverified (only one hit-location asset exists). The bone table in 2c is keyed by the damage-type tag, and each row uses the 12 classes.

---

### 2j. Archetype Caliber Modifiers ([`DT_InfantryData_ArchetypeCaliberModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json), new)

Each row is a weapon archetype with per-hit-location values stored under an unnamed field. Rows: `AR`, `DMR`, `LMG`, `Sniper`, `Pistol`, `SMG`, `Shotgun`, [`CombatBow`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/CombatBow.json), `HMG.MWSY_001`, `Vehicle.Turret.MachineGun`, `Vehicle.Turret.Minigun` and `Vehicle.Turret.STN_06`. The Bullet calibre rule in 2f uses the `B_ArchetypeCaliberModifiers` operation, which is most likely the reader of this table. The values are not listed here.

### 2k. Suppression Curves (`Inventory/CR_SuppressionCurve_*`, new)

Six shared `CurveFloat` assets, all in [`Inventory/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Inventory). Each projectile's `SuppressionData.DistanceFalloffCurve` points at one of them. They replace the removed `AR_SuppressionCurve`.

| Curve | Projectiles that reference it |
|---|---|
| [`CR_SuppressionCurve_Small`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/CR_SuppressionCurve_Small.json) | 9mm, 45ACP, 45Colt, 50AE, 7mmBuckshot |
| [`CR_SuppressionCurve_Medium`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/CR_SuppressionCurve_Medium.json) | 545mm, 556mm, 762mm, 12g RifledSlug |
| [`CR_SuppressionCurve_Large`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/CR_SuppressionCurve_Large.json) | 308Winchester, 762x54mm |
| [`CR_SuppressionCurve_Special`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/CR_SuppressionCurve_Special.json) | 20x102mm, 30mm, 35x228mm, 50Cal |
| [`CR_SuppressionCurve_GrenadeLauncher`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/CR_SuppressionCurve_GrenadeLauncher.json) | 40mm |
| [`CR_SuppressionCurve_Rocket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/CR_SuppressionCurve_Rocket.json) | 70mm, 72mm, 84mm, 93mm, 120x570mm, 120x800mm, 122mm, 122mm HAVOC, 155mm Expensive |

The 125x570mm, 155mm Standard (and its `_SB` variants), 338 Norman Magnum, 762x51mm and TV-guided missile assets do not reference an external suppression curve.

---

## 3. Projectiles ([`Inventory/Equipment/Caliber/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber), 32 `WDProjectileData` assets)

Units are not verified. The values are raw UE fields. Speed is `TypicalSpeed` (launch speed). `Thrust` is the sustained speed where present. Blank means the field is not set on the asset.

| Asset | ProjectileId | Base dmg | Expl. radius | Eff. radius | Falloff | Speed | Thrust | Mass | Drag | Ricochet ° |
|---|---|---|---|---|---|---|---|---|---|---|
| DA_TVGuidedMissile_Data | Caliber.84mm.TVGuided | 100 | 1000 | 400 | 0.5 | 22400 | 22000 | 2.3 | GC | 85 |
| DA_120x570mm_ProjectileData | Caliber.120x570mm | 150 | 750 | 420 | 0.3 | 22400 | 22000 | 20.0 | GC | 91 |
| DA_120x800mm_Standard | Caliber.120x800mm.Standard | 120 | 1000 | 500 | 0.45 | 15000 | 22000 | 15.0 | GC | 91 |
| DA_125x570mm | Caliber.125x570mm | 150 | 750 | 420 | 0.3 | 22400 | 22000 | 23.0 | GC | 91 |
| DA_122_mm_HAVOC | Caliber.122mm.Havoc | 300 | 300 | 600 | 0.6 | 143000 | 20000 | 57.0 | GC | 91 |
| DA_122mm | Caliber.122mm | 100 | 600 | 200 | 1.0 | 143000 | 20000 | 57.0 | GC | 91 |
| DA_155mm_Expensive | Caliber.155mm.Expensive | 450 | 2000 | 1000 | 0.93 | 15000 | 22000 | 19.0 | GC | 91 |
| DA_155mm_Expensive_SB | Caliber.155mm.Expensive.Sandbox | 450 | 2000 | 750 | 0.5 | 15000 | 22000 | 70.0 | GC | 91 |
| DA_155mm_Standard | Caliber.155mm.Standard | 450 | 2000 | 750 | 0.5 | 15000 | 22000 | 70.0 | GC | 91 |
| DA_155mm_Standard_SB | Caliber.155mm.Standard.Sandbox | 450 | 2000 | 750 | 0.5 | 15000 | 22000 | 70.0 | GC | 91 |
| DA_70mm | Caliber.70mm | 100 | 1000 | 400 | 0.5 | 22400 | 22000 | 10.1 | GC | 100 |
| DA_72mm | Caliber.72mm | 200 | 1080 | 200 | 0.8 | 45000 | 17500 | 9.2 | G7 | 91 |
| DA_84mm | Caliber.84mm | 100 | 1000 | 400 | 1.0 | 22400 | 22000 | 2.3 | GC | 91 |
| DA_93mm | Caliber.93mm | 110 | 1200 | 250 | 0.9 | 12000 | 17000 | 2.0 | GC | 91 |
| DA_40mm | Caliber.40mm | 100 | 1000 | 250 | 1.0 | 7500 | 20000 | 0.23 | GC | 91 |
| DA_30mm | Caliber.30mm | 100 | 300 | 100 | 1.0 | 80000 | 20000 | 0.22 | GC | 85 |
| DA_20x102mm | Caliber.20x102mm | 60 | — | 375 | 0.7 | 22400 | 22000 | 0.04 | G7 | 91 |
| DA_35x228mm | Caliber.35x228mm | 60 | — | 375 | 0.7 | 79200 | 22000 | 0.375 | G7 | 91 |
| DA_308Winchester | Caliber.308Win | 45 | — | — | — | 38500 | — | 0.012 | G7 | — |
| DA_338Norman | Caliber.338Nor | 105 | — | — | — | 50000 | — | 0.01944 | G7 | — |
| DA_762mm | Caliber.762mm | 34 | — | — | — | 38600 | — | 0.008 | G7 | — |
| DA_762x51mm | Caliber.762x51mm | 60 | — | — | — | — | — | 0.01 | G7 | — |
| DA_762x54mm | Caliber.762x54mm | 44 | — | — | — | 43000 | — | 0.0117 | G7 | — |
| DA_9mm | Caliber.9mm | 22 | — | — | — | 28000 | — | 0.007 | G1 | — |
| DA_45ACP | Caliber.45ACP | 30 | — | — | — | 32200 | — | 0.015 | G1 | — |
| DA_45Colt | Caliber.45Colt | 45 | — | — | — | 29200 | — | 0.01 | G1 | — |
| DA_50AE | Caliber.50AE | 63 | — | — | — | 41600 | — | 0.019 | G7 | — |
| DA_50Cal | Caliber.50Cal | 90 | — | — | — | 31500 | — | 0.051 | G7 | — |
| DA_545mm | Caliber.545mm | 26 | — | — | — | 30000 | — | 0.0034 | G7 | — |
| DA_556mm | Caliber.556mm | 28 | — | — | — | 40400 | — | 0.0041 | G7 | — |
| DA_12g_RifledSlug | Caliber.12g.RifledSlug | 105 | — | — | — | 29800 | — | 0.028 | GL | — |
| DA_7mmBuckshot | Caliber.7mmBuck | 25 | — | — | — | 29200 | — | 0.004 | GA | — |

Notes:
- Explosive rounds (rockets, grenades, artillery) carry a `DamageEntityData` tag (e.g. `Meta.Damage.Explosive.Rocket.155mm`). Bullets use `Meta.Damage.Bullet.<caliber>`.
- Rockets and cannon rounds set an unnamed field to False. Ricochet angles are `MinImpactAngleForRicochet` in degrees.
- The `Drag` column is the `DragModel` row in [`CT_Projectile_DragCoefficients`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/Curves/CT_Projectile_DragCoefficients.json) (GC Cylinder, G1 Flat Bottom, G7 Boat Tail, GL Blunt Nose, GA Pellet).
- Many 155mm and 120mm variants are duplicated across `_SB` (Sandbox) assets with different radii or mass. The Sandbox variant is a separate asset, not an override.

---

## 4. Action Definitions (`Actions/`, 116 `BH`/`WD` action definitions)

Each action carries an `ActionTag`, an `ActionClass` (blueprint), an `ActivationContextType` and a list of `ActionContext` flags. The context flags (Holdable, TwoHanded, OneHanded, Weapon, Interaction, Movement, UI, Emote, FollowProjectile) determine when the action is valid.

| Folder | Context | Count | Examples (tag) |
|---|---|---|---|
| [`Actions/Appliables/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Actions/Appliables) | WDAppliableItemActionContext | 4 | Appliable.PrimaryUse [Holdable, TwoHanded]; Appliable.SecondaryUse [Interaction, Holdable, TwoHanded] |
| [`Appliables/Bandage/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Actions/Appliables/Bandage) | WDAppliableItemActionContext | 2 | Appliable.Bandage.PrimaryUse [Holdable, Interaction, TwoHanded]; Bandage.SecondaryUse [Holdable, TwoHanded] |
| `Character/` | WDEmoteActivationContext | 27 | `Action.Player.Emote.*` (26 emotes using `B_Action_Emote_C`) plus `Surrender_Drop` [Emote] |
| `Interaction/` | None / custom | 4 | Player.UseDoor, Player.Tracker, Player.Door.Breach, Player.Scene.VehicleAdmin |
| `Melee/` | WDGenericItemActionContext | 2 | Player.Melee.PrimaryUse and SecondaryUse [Holdable, TwoHanded, Weapon] |
| `Movement/` | Various | 25 | Jump, Sprint, TacSprint, Crouch, Prone, Crawl, Stand, Vaulting, Mantling, Climbing, Ladder, Fall, Swimming, Dragging, StopSprint, StopTacSprint |
| `Projectile/` | WDFollowProjectileActionContext | 1 | Projectile.Follow [FollowProjectile] |
| `Revive/` | Various | 2 | Player.Revive [Interaction, TwoHanded]; Player.RequestRevive |
| `UI/` | Mixed | 17 | Access inventory, tactical map, chatbox, radial wheel, ping wheel, equipment/garage/vehicle vendors, access looting and wager vendor (new), quick-slot change, ping and remove-ping, toggle hands |
| `Vehicle/` | None / Vehicle contexts | 1 | Vehicle.Movement [Movement] |
| [`Vehicle/Weapons/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Actions/Vehicle/Weapons) | WDVehicleWeaponActionContext | 7 | Vehicle.Weapon.Fire, PreFire, ADS, Reload, ActiveReload, Vehicle.Horn, Vehicle.ChangeStabilizingState |
| `Weapons/` | WDGenericItemActionContext / None | 26 | Weapon.Fire, Weapon.Reload, Weapon.ADS, Weapon.ChamberRound, Weapon.CycleFireMode, Weapon.CycleSights, Weapon.Zeroing.Increase/Decrease/Reset, Weapon.Bipod.Mount/ToggleFold, Weapon.MeleeBash, Throw.Primary/Back/Swap, Player.Lean.Left/Right, Player.Focus, Item.Inspect, Equipment.Change |

[`DT_EmoteData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Actions/Character/DT_EmoteData.json) has 27 rows. `PlayRate` ranges from 0.95 to 1.2 (most at 1.0). Some rows set `Surrender_Drop` to a different flag.

---

## 5. Input ([`Player/PlayerCharacter/Inputs/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs))

| Item | Count | Notes |
|---|---|---|
| `BHInputAction` | 98 | 61 in `Inputs/`, 33 in [`Inputs/PlayerController/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/PlayerController), 4 in [`TaggedActions/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/TaggedActions) |
| Value types | 81 None (bool), 15 Axis1D, 2 Axis2D | |
| `InputMappingContext` | 20 | IMC_Player, IMC_PlayerAiming, IMC_Emote, IMC_Inventory, IMC_Interaction, IMC_LadderClimbing, IMC_Player_Downed, IMC_Player_Parachuting, IMC_Player_Swimming, IMC_Tipping, IMC_UIKeybinds_Registration, and others |
| `BHPlayerMappableKeySettings` | 106 | Per-action rebinding slots (`SlotContext` on 40) |
| `PlayerMappableInputConfig` | 1 | `Default` config, display name `Default Input Config` |
| Trigger classes | Pressed 63, Released 45, Tap 29, Hold 30, TapXTimes 1, Pulse 2, ChordAction 3 | |

Notable thresholds:

| Trigger | Value | Used by |
|---|---|---|
| Hold, one-shot 0.5 s | HoldTimeThreshold 0.5 | IMC_Inventory, IMC_PlayerController, GroundVehicle alternate |
| Hold, one-shot 0.1–0.25 s | 0.1 / 0.2 / 0.25 | Chat open (chorded), PingWheel, RadialWheel (equipment and voice chat) |
| Hold, one-shot 0.3 s | 0.3 | Infantry BumperLeaner |
| Tap | — | Quick-slot 0–9, next/previous item, next/previous weapon (`TapReleaseTimeThreshold` set on one) |

Input-side modifiers include `WDDeadZoneInputModifier` (10), `InputModifierSwizzleAxis` (9), `InputModifierNegate` (7), `WDAimAssistInputModifier` (1, filter [`DA_AimAssistFilter`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/DA_AimAssistFilter.json)), `WDResponseCurveTypeModifier` (1), and `WDApplyAxisConfig` (8).

The controller configs in [`Settings/Controls/ControllerConfigs/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Settings/Controls/ControllerConfigs) (Infantry, GroundVehicle, HeavyVehicle, Helicopter) map these actions per device. Their contents were only partially decoded (see section 13).

---

## 6. User Settings (`Settings/`)

Seven settings DataTables hold the setting rows (`BHUserSettingDataTableRow` for `General`, `Audio`, `Accessibility`, `Controls`, `Extras`, `Keybindings`, `Video`). The definitions are split across these asset types:

| Asset type | Count | Role |
|---|---|---|
| `BHUserSettingNumericData` | 24 | Slider range, default, display scale |
| `BHUserSettingDiscreteData` | 15 | Discrete (enum) setting with a default index |
| `BHUserSettingEnumDiscreteValues` | 16 | The named values for each discrete setting |
| `WDUserSettingDiscretePresetData` | 3 | Presets that set many values at once (gamepad dead-zone presets) |
| `WDUserSettingButtonData` | 2 | Mic test and retry-communication buttons |
| `BHUserSettingInputFieldData` | 1 | Text input field |
| `WDUserSettingHyperlinkData` | 1 | Link (Extras) |
| `BHEnhancedInputPlayerBindsPresetData` | 13 | Keybind preset data |

Numeric settings (sample, from the 24):

| Setting | Minimum | Maximum | Default | Display | Step | Notes |
|---|---|---|---|---|---|---|
| Accessibility.NameplateBackgroundOpacity | — | 100 | — | 0–100 % | 1 | Shown as percent |
| Controls.Gamepad.Deadzone.LeftTriggerMax | 5 | 100 | 100 | 1–10 | 1 | |
| Controls.Gamepad.Deadzone.LeftTriggerMin | — | 95 | — | 1–10 | 1 | |
| Controls.Gamepad.Deadzone.LookStickAxial | — | 30 | 15 | 1–10 | 1 | |
| Controls.Gamepad.Deadzone.LookStickCentre | — | 30 | 15 | 1–10 | 1 | |
| Controls.Gamepad.Deadzone.LookStickMaxInput | — | 15 | 15 | 1–10 | 1 | |
| Controls.Gamepad.Deadzone.MoveStickAxial | — | 30 | 15 | 1–10 | 1 | |
| Controls.Gamepad.Deadzone.MoveStickCentre | — | 30 | 15 | 1–10 | 1 | |
| Controls.Gamepad.Deadzone.MoveStickMaxInput | — | 15 | 15 | 1–10 | 1 | |
| Controls.Gamepad.Deadzone.RightTriggerMax | 5 | 100 | 100 | 1–10 | 1 | |
| Controls.Gamepad.Deadzone.RightTriggerMin | — | 95 | — | 1–10 | 1 | |
| Controls.LookAccelMagnitudeThreshold | 0.01 | — | 0.9 | 0.01 | 0.01 | |
| Controls.LookAccelMaxMultiplier | 1.2 | 5.0 | 1.5 | 1.2–5.0 | — | 1 decimal. Was 0.5 / 10.0 / 1.6, display 1.0–3.0 |
| Controls.LookAccelPitchWeight | — | — | 0.2 | — | 0.05 | |
| Controls.RotaryMouseAxisIsolation | — | 100 | — | 0–100 % | 5 | |
| Controls.SensitivityRelativeCoefficient | — | 100 | 100 | 0–100 % | 1 | |
| Controls.HOTASDeadzone | — | 0.5 | 0.05 | 0–0.5 | 0.01 | |
| Controls.HOTASSensitivity | 0.1 | 2.0 | 1.0 | 0.1–2.0 | 0.05 | |
| General.FieldOfView.FirstPersonMesh | — | — | 0.3333 | 1–10 | 1 | Masked value |
| Video.Sharpness | — | 1.5 | 1.2 | — | 0.01 | |

The remaining numeric rows (not all printed in review) cover accessibility, video and other controls options. The full list is in the `Settings/` folder.

Discrete settings include `Accessibility.HUD_Visibility` (default index 1, value `EWDUIHUDVisibilityType::On`), `Controls.GamepadResponseCurveType` (default index 1, `Linear`), and the dead-zone presets (`DeadZonePreset_LookStick`, `DeadZonePreset_MoveStick`, each with `EWDDeadZoneAnaloguePresets::None` as a value).

---

## 7. Inventory Operation Rules and Mag Packing (`Inventory/`)

### 7a. Custom operation rules ([`DA_CustomOperationRules`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/DA_CustomOperationRules.json), 17 rules)

Each rule matches a drag/drop between inventory slots and performs a custom operation.

| # | Operation | Source item / slot | Destination item / slot |
|---|---|---|---|
| New | Block: loose ammo swapped with a magazine in a vendor (`WDCustomInventoryOperationRule_Block`) | Item.Context.ForceToStorage | Attachment.Magazine |
| 0 | Weapon mag swapped with another mag | Attachment.Magazine (slot Magazine) | Attachment.Magazine |
| 1 | Mag swapped with a weapon's mag | Attachment.Magazine | Attachment.Magazine (weapon) |
| 2 | Mag dragged onto a weapon | Attachment.Magazine | Item.Weapon |
| 3 | Mag put into an empty weapon mag slot | Attachment.Magazine | Attachment.Magazine (slot) |
| 4 | Weapon mag taken out to an empty slot | Attachment.Magazine (slot) | empty |
| 5 | Loose ammo dragged into magazine | Item.Ammo | Attachment.Magazine |
| 6 | Loose ammo dragged onto loose ammo | Item.Ammo | Item.Ammo |
| 7 | Ammo dragged onto a magazine | Item.Ammo | Attachment.Magazine |
| 8 | Ammo swapped with a weapon | Item.Ammo | Item.Weapon |
| 9 | Ammo put into chamber slot | Item.Ammo | Attachment.Chamber (slot) |
| 10 | Ammo swapped from chamber to inventory | Attachment.Chamber | Item.Ammo |
| 11 | Loose ammo swapped from mag to inventory | Item.Ammo (slot) | Item.Ammo |
| 12 | Ammo taken from chamber to empty slot | Attachment.Chamber | empty |
| 13 | Loose ammo taken from internal mag to empty slot | Item.Ammo (slot) | empty |
| 14 | Ammo put into weapon ammo slot | Item.Ammo | Item.Ammo (slot) |
| 15 | Item transferred between inventories or equipment slots | any | any |

The numbers in the table are from the previous export. In the current asset the Block rule is index 0, so every other index is one higher than shown here. Some operation descriptions were also reworded in this update (for example, the chamber rule now reads "Ammo being put into a weapons chamber slot").

### 7b. Reload rules (`WDCustomInventoryOperationRule_Reload`, 13 rules)

| Reload type | Context | Insert ammo type | Weapon slot | Count |
|---|---|---|---|---|
| Ammo | Insert | Weapon | — | 5 |
| Ammo | Remove | — | — | 2 |
| Ammo | Insert | Magazine | — | 1 |
| Magazine | SwapOrInsert | — | Source | 1 |
| Magazine | SwapOrInsert | — | Destination | 1 |
| Magazine | SwapOrInsert | — | — | 1 |
| Magazine | Insert | — | — | 1 |
| Magazine | Remove | — | — | 1 |

### 7c. Load-ammo and transfer rules

- `WDCustomInventoryOperationRule_LoadAmmo` (2 rules) point to [`DA_InventoryMagPackingData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/InventoryMagPacking/DA_InventoryMagPackingData.json).
- `WDCustomInventoryOperationRule_Transfer` (1 rule): `DefaultTransferTime` = 0.5 s. Equipment containers are `Inventory.Slot.Primary`, `Secondary`, `Sidearm`, `Specialist`, and others.

### 7d. Mag packing curves ([`InventoryMagPacking/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Inventory/InventoryMagPacking), 37 `CurveFloat` plus [`DA_InventoryMagPackingData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/InventoryMagPacking/DA_InventoryMagPackingData.json))

Three families, one curve per caliber:

| Family | Curve pattern (time, value) | Example |
|---|---|---|
| `CombineLooseAmmo/CR_CombineLooseAmmoCurve_<caliber>` | (0, 0.4–1.2) to (N, larger value) | 45ACP: (0, 0.4) (13, 1.9) (26, 3.8); 50Cal: (0, 1.2) (10, 7.0) (20, 14.0) |
| `ExtractAmmo/CR_ExtractAmmoCurve_<caliber>` | (0, 0.3–0.8) to (N, larger value) | 308Win: (0, 0.3) (60, 20.0); 545mm: (0, 0.3) (200, 40.0) |
| `LoadAmmo` family | not decoded in review | — |

The curve axis is not labelled in the data. The most likely reading is round count on the X axis and time or cost on the Y axis, but this is not verified.

---

## 8. Factions ([`Gamemode/Data/DataAssets/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DataAssets), [`DT_FactionData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_FactionData.json))

| Tag | Name | Short | Colour | Squad colour | Team ID | Safe zone tag |
|---|---|---|---|---|---|---|
| `Meta.Alignment.Faction.Alpha` | Lonestar | L* | `4CB1EF` | `EDA314` | 0 | `State.Location.SafeZone.Alpha` |
| `Meta.Alignment.Faction.Bravo` | Valkyra | Vlk | `FA503E` | `EDA314` | 1 | `State.Location.SafeZone.Bravo` |
| `Meta.Alignment.Faction.Charlie` | Manticore | Mtc | `1DD65C` | `EDA314` | 2 | `State.Location.SafeZone.Charlie` |
| `Meta.Alignment.Faction.Default` | White | White | — | — | 3 | — |

Each faction has block-colour materials (`MI_WDPlayerBlue` for Alpha, `MI_WDPlayerRed` for Bravo, `MI_WDPlayerGreen` for Charlie, `MI_WDPlayerNoTeam` for Default). The third-person character material list is set for two factions.

---

## 9. Player Character Components ([`Player/PlayerCharacter/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter))

| Component | Values |
|---|---|
| `WDFirstPersonCameraComponent` | FieldOfView **106.0**, OrthoWidth 512, `bAutoCalculateOrthoPlanes` false |
| `BHPerspectiveData` ([`DA_PlayerCharacterComponents`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/DA_PlayerCharacterComponents.json)) | Keyed templates (e.g. `FirstPersonBodyMesh`, each a `SkeletalMeshComponent` template). Full key list not expanded. |
| `WDWaveBreakerComponent` | Present, no exposed properties |
| `WDCharacterMovementEffectsComponentConfigurationDataAsset` | Per-stance movement effects (`Stances`, `JumpGameplayCueTag`, `LandingGameplayCueTags`, `StanceTransitionEffects`, `MovementModeEffects`) |
| `CurveFloat` (9) and `CurveVector` (4) in [`Player/PlayerCharacter/Curves/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves) | Animation and camera curves (not decoded) |
| [`Player/PlayerCharacter/MovementFeatures/Ladder/Curves`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/MovementFeatures/Ladder/Curves) (3) | Ladder movement curves |

---

## 10. Destructible Objects ([`WorldInteractable/Objects/EnvironmentalObjects/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects))

| Asset type | Count | Notes |
|---|---|---|
| `BHDestructionBuildingDefinitionDataAsset` | 14 | One per door or garage type (six added in this update: [`D_InteractableDoor_Buisness`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_InteractableDoor_Buisness.json), [`D_Interactable_Commercial_Door_01a_L`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_Interactable_Commercial_Door_01a_L.json)/`_R`, [`D_Interactable_Door_Wood_01a`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_Interactable_Door_Wood_01a.json), `D_Interactable_HospitalDoor_01a_L`/`_R`): [`D_Door`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_Door.json), [`D_InteractableDoor_Apartment`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_InteractableDoor_Apartment.json), `_ApartmentBalcony`, `_ApartmentEntrance`, `_Office`, `_WoodPVC`, [`D_Interactable_GarageDoor_01a_Left`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_Interactable_GarageDoor_01a_Left.json), `_Right`. Each has 1 required mesh, 1 chunk-data entry and 1 chunk lookup. |
| `BHDestructionBuildingDecoratorDefinitionDataAsset` | 9 | Decorators (`D_Decorator_Interactable_HospitalDoor_01a_L`/`_R` added in this update) ([`D_Decorator_Door`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors/D_Decorator_Door.json), `D_Decorator_InteractableDoor_*`) each with a `SaveID` GUID. |
| [`B_TargetDummy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/TargetDummy/B_TargetDummy.json) (blueprint) | 1 | Damage entity tag `Meta.Damage.Infantry`, vitality and inventory components. Hit-decay timers and armour toggles (`SetHelmetArmour`, `SetVestArmour`). Test asset. |

---

## 11. AI and EQS (`AI/`, [`Gamemode/Objects/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Gamemode/Objects))

| Asset | Contents |
|---|---|
| [`BB_Enemy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/AI/BB_Enemy.json) (BlackboardData) | 8 keys: EnemyActor, HasLineOfSight, MoveGoal, SelfActor, TargetActor, Pressure, HasTeleportedToAO, SOClaimHandle |
| [`EQS_FindDeploymentBoard`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/AI/EQS/EQS_FindDeploymentBoard.json) | Deployment-board search (1 option) |
| [`EQS_FindNewFiringPosition`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/AI/EQS/EQS_FindNewFiringPosition.json) | Firing-position search (1 option) |
| [`EQS_SpawnQuery_800`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Objects/EQS_SpawnQuery_800.json) and [`EQS_SpawnQuery_800_Bravo`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Objects/EQS_SpawnQuery_800_Bravo.json) | Spawn query, 800 units, with overlap test (2 each in [`Gamemode/Objects`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Gamemode/Objects)) |
| [`CRV_EnemyDistancePressure`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/AI/Services/CRV_EnemyDistancePressure.json) (CurveFloat) | Pressure falls from 1.0 at 0 to 0.0 at 3000 |

---

## 12. Assistance Requests, Vendors and Emotes

### 12a. Assistance requests ([`Communication/AssistanceRequests/DT_AssistanceRequests`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Communication/AssistanceRequests/DT_AssistanceRequests.json), 12 rows)

Rows: Ammo, Backup, Refueling, Healing, Repair, Revive, Pickup, Dropoff, Getout, SquadInvite, GetIn, Supplies. Each row has a `RequestClass` (`WDAssistanceRequest_*`), an `EventFeedTag`, `Duration`, `GameplayCueDuration`, distance limits for team events and spatial icons, and `CancelWhenEnteringVitalityStates`. The `bOnlyShowEventFeedToInvolvedPlayers` flag is true for the Repair, Revive, Dropoff and GetIn rows and false for Getout.

### 12b. Vendor markets ([`WorldInteractable/NPCs/Vendor/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor))

| Table | Rows | Price range (cash) | Notes |
|---|---|---|---|
| [`VendorEquipment/DT_WeaponMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment/DT_WeaponMarket.json) | 37 (155 price variations) | 0–1050 | Magazines, weapons, sizes; Alpha and Bravo faction-specific items. `125x570mm` ammo (210) added in this update |
| [`VendorEquipment/DT_AttachmentMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment/DT_AttachmentMarket.json) | 17 | 380–1500 | Optics, muzzles, grips (e.g. `SniperScope10x` 1200, `EotechHoloSight` 620, `RK6ForeGrip` 380). `MZL_04` was 1800 (now 1450) |
| [`VendorEquipment/DT_GearMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment/DT_GearMarket.json) | 13 | 0–15000 | Vests (Small 100, Medium 250, Large 400), backpacks (Small 350 to ExtraLargeSling 4000; LargeBackpack 1600, LargeSlingBackpack 2400) |
| [`VendorEquipment/DT_UtilityMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment/DT_UtilityMarket.json) | 3 | 200–800 | Bandage 200, SuperBandage 800, M67Grenade 200 |
| [`VendorVehicles/DT_VehicleMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor/VendorVehicles/DT_VehicleMarket.json) | 0 | — | Empty in this export |

Each row has `VendorItemVariations` with `Price`, `LevelToUnlock`, `Amount`, `LifeTimeBuyLimit` and optional faction lock.

### 12c. Emote data ([`Actions/Character/DT_EmoteData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Actions/Character/DT_EmoteData.json), 27 rows)

Each row has a `PlayRate` (0.95 to 1.2) and several boolean flags whose names are unnamed fields. `Surrender_Drop` is the only row with a flag set to true in the first flag column.

### 12d. Ping and hit-marker types ([`Communication/Pings/DT_PingTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Communication/Pings/DT_PingTypes.json), 4 rows, new)

Rows: `Communication.Ping`, `Communication.Ping.Type.Context.Map.MarkCoordinates`, `Communication.AssistanceRequest` and `Trackers.Type.HitMarker`. Row struct `WDPingTypeData`.

---

## 13. Curves and Scalar Modifiers (summary)

- **Gamemode/Data/ScalarModifiers** (6 curves): [`CF_Reward_Assist_DamagePlayer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/ScalarModifiers/Assists/CF_Reward_Assist_DamagePlayer.json) and `DamageVehicle` ramp 0→1 over input 0–1. [`CF_Reward_HealPlayer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/ScalarModifiers/Heal/CF_Reward_HealPlayer.json) ramps 0.25 to 1.0 over input 0–1.0. [`CF_Reward_ReviveHealPlayer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/ScalarModifiers/Heal/CF_Reward_ReviveHealPlayer.json) 0→0.2 at 0.4, 1.0 at 1.0. [`CF_Reward_Build`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/ScalarModifiers/Buildables/CF_Reward_Build.json) and [`CF_Reward_SupplyCrateItemPurchase`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/ScalarModifiers/SupplyCratePurchase/CF_Reward_SupplyCrateItemPurchase.json) are identity curves (output equals input) across ±1,000,000. These scale rewards; the reward tables are in the rewards doc.
- **Inventory/InventoryMagPacking** (37 curves): see 7d.
- **Total curves in folder:** 66 `CurveFloat` assets plus 1 `CurveTable` ([`GameplayEffects/Curves`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/GameplayEffects/Curves)) and 4 `CurveVector`.

---

## 14. How Values Combine

- **Infantry hit damage:** the bone multiplier (2c) is chosen by damage-type row, then the hit location. The `Universal` value and the weapon row's value multiply ([DamagePipeline §7.1](Wardogs_DamagePipeline_v2.md#71-b_bonedamagemodifiers_c-entries-5-7-10)). Infantry modification rules (2f, 2g) then adjust the result. The rules are sorted by `PriorityCategory` and `PriorityIndex`. The exact combination (additive percentages vs multiplicative) is not verified.
- **Armour-piercing and hollow-point:** the ammo-modifier assets (2e) multiply penetration effectiveness, range and exit speed. The per-arm penetration table (2d) then scales damage per armour class.
- **Vehicle occupants:** seat reduction (2h) is a flat percentage by vehicle variant and arm class.
- **Explosives:** `BaseDamage` and `ExplosiveRadius` (section 3) feed the Calibre rules (2f). Falloff is the `ExplosiveDamageFallOff` field.
- **Vendor price:** `Price` is per variation. The vendor UI applies the `LevelToUnlock` gate and the `LifeTimeBuyLimit`.

---

## 15. Still Not Pulled / Limitations

- **Unnamed fields.** Many struct fields have no readable name and are called unnamed fields here. These are the arm-class arrays in 2d, the seat-reduction arrays in 2h, the `Emote` flags in 12c, and some action fields. Their meaning was inferred from neighbouring values and is not confirmed.
  - **SDK (2026-10-16) — Emote flags (12c):** [`FWDEmoteData`](sdk/raw/WDGame_structs.hpp#L14430) is a 0x30-byte struct (inherits from `FBHGameplayTaggedTableRow`) with 8 fields:
    - `_aaaakmaiagceginhpgeoe` (bool, 0x10) — unresolved flag #1
    - `_aaaamcjgaokphjebecjic` (bool, 0x11) — unresolved flag #2
    - `PlayRate` (float, 0x14) — animation playback rate ✓
    - `bHolsterWeapon` (bool, 0x18) — holster weapon during emote ✓
    - `_aaabgjmmjbmjfbncaafch` (bool, 0x19) — unresolved flag #3
    - `_aaabjdgjapjmbgmpamikg` (bool, 0x1A) — unresolved flag #4
    - `_aaabelpijohgmmanaeoif` (`FGameplayTagContainer`, 0x20) — unresolved tag list (candidate: "allowed states" / "restricted contexts" / "required unlocks")
  - 4 of 7 "Emote flag" bools remain Dumper-unresolved; 2 are resolved to `bHolsterWeapon` + `PlayRate`.
  - **SDK (2026-10-16) — seat-reduction arrays (2h):** see [`Wardogs_DamagePipeline_v2.md`](Wardogs_DamagePipeline_v2.md#84-vehicleseatdamagereduction-occupant-protection-table) — the arrays belong to `UB_VehicleSeatDamageReduction_C` (one of 4 damage modifier blueprints), reading per-seat `FGameplayTag → float` map from a DataTable at runtime.
  - Arm-class arrays (2d) and action fields are not yet matched to a specific SDK struct; follow-up pass needed.
- **Operation semantics.** `Percentage_Ongoing` is the operation name on the modification entries. Its exact formula (additive, multiplicative, applied per tick or once) is not decoded.
- **Arm-class naming.** `Meta.Damage.Arms.Small/Medium/High/Special` is the tag family used. Its meaning as armour class or penetration tier is an inference.
- **Units.** Projectile speed, radius and mass units are not verified against the engine.
- **Controller configs.** [`Settings/Controls/ControllerConfigs/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Settings/Controls/ControllerConfigs) (13 files) and the 106 `BHPlayerMappableKeySettings` default keys were only partially decoded. Default key-to-action bindings are in `IMC_*` DefaultKeyMappings, which were counted but not expanded.
- **Infantry rules.** The 146-entry `Meta.Damage.Infantry` row was aggregated to unique rules (86 unique, 60 no-op). Not every unique rule is listed in 2f.
- **Vendor weapon market.** The 37 rows in [`DT_WeaponMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment/DT_WeaponMarket.json) were summarised by price range only. Individual items were not listed.
- **Empty vehicle market.** [`DT_VehicleMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor/VendorVehicles/DT_VehicleMarket.json) has 0 rows, so vehicle vendor prices are not in this export.
- **Destruction chunk data.** Chunk IDs and mesh references in the destructible-building assets were counted, not expanded.
- **Player curves.** The 9 `CurveFloat` and 4 `CurveVector` assets in [`Player/PlayerCharacter/Curves/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves) were not decoded.
- **Reward tables.** [`Gamemode/Data/DT_CashRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_CashRewards.json) (49 rows), [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) (78 rows), [`DT_AssistCashRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_AssistCashRewards.json) (9), [`DT_CashRewardModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_CashRewardModifiers.json) (9) and the [`CashRewardsDataTable/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable) tree are covered in `Wardogs_Rewards_and_Progression_v2.md`, not here.
- **EQS details.** The EQS query contents (generators, tests and scoring equations) were listed by name only.

---

## Change log

| Date | Change |
|---|---|
| 2026-10-18 | Round-6 verifier pass: the hit location is an exact bone-name lookup with no parent walk and no remap for damage (2b; `DamageImpactRemap` only drives the ragdoll impulse and hit-reaction animation); the live player physics asset `PA_TPCharacter_Simplified` and its 20 bodies (2b); the asset is picked by actor class (2i); the `Universal` and weapon bone rows multiply (14). |
