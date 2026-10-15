# Wardogs — Game Mechanics Reference (v2)
*Extracted from cooked game data under `Content/GameMechanics` (467 files, 898 export blocks, UE 5.7 build `++Wardogs+Live-CL-509546`). Numbers are the raw values stored in the DataAssets and DataTables. Where the meaning of a field is inferred or unknown, the doc says so.*

> **Scope note:** The cash and reward tables (`Gamemode/Data/DT_CashRewards`, `DT_Rewards`, `DT_AssistCashRewards`, `DT_CashRewardModifiers`, and everything under `Gamemode/Data/CashRewardsDataTable/`) are covered in **`Wardogs_Rewards_and_Progression_v2.md`**. This doc does not repeat them. Note that `DT_Rewards` and `DT_CashRewards` are the stale placeholder layer described in that doc.

---

## 1. Folder Map

| Folder | Blocks (approx.) | What it holds |
|---|---|---|
| `Actions/` | ~115 | Action definitions (`BHActionDefinition` 98, `WDActionDefinition` 16) with tags, activation context and action class. Also `DT_EmoteData`. |
| `DamageSystem/` | ~14 | Damage categories, ammo modifiers, bone/hit-location multipliers, armour and helmet rules, vehicle-seat reduction, hit-location maps. |
| `Gamemode/` | ~32 | Reward tables (see the rewards doc), `WDFactionData` (4 factions), scalar reward curves, EQS spawn queries. |
| `Inventory/` | ~72 | Projectile stats (`WDProjectileData`, 31 assets), inventory operation rules, mag-packing curves. |
| `Player/PlayerCharacter/` | ~138 | Enhanced Input (`BHInputAction` 98, `InputMappingContext` 20, key settings 106), trigger and modifier classes, camera and perspective components, movement audio/effects config. |
| `Settings/` | ~67 | User-setting definitions (numeric, discrete, presets, buttons) in 7 settings DataTables, plus controller configs. |
| `WorldInteractable/` | ~30 | Vendor markets (4 DataTables), destructible door/building definitions, target dummy blueprint. |
| `AI/`, `Communication/`, `GameplayEffects/` | ~12 | Blackboard, EQS queries, AI services curve, assistance-request DataTable, tagged gameplay effects, curve table. |

---

## 2. Damage System

### 2a. Damage Categories (`DA_GlobalDamage_Categories`)

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

### 2b. Hit Locations (`DA_GlobalDamage_HitLocations_Player`)

The skeleton bone names map to 12 hit-location classes. These classes are the columns of the bone table in 2c.

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

The asset also has 2 `DamageImpactRemap` entries: `spine_01` is remapped to `pelvis`, and `spine_05` to `spine_04`.

### 2c. Bone Damage Multipliers (`DT_InfantryData_BoneDamageModifiers`)

Each row is a damage-type tag. Values are the per-hit-location multiplier. The `Universal` row is the fallback for anything not listed separately (inferred from the row name).

| Row | Head | Neck | Torso.Up | Torso.Mid | Torso.Low | Pelvis | Arm.Up | Arm.Low | Arm.Hand | Leg.Thigh | Leg.Calf | Leg.Foot |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Universal | 1.0 | 0.75 | 1.1 | 1.0 | 0.95 | 0.9 | 0.6 | 0.5 | 0.3 | 0.6 | 0.5 | 0.3 |
| AR | 2.35 | 2.35 | 1.0 | 1.0 | 1.0 | 1.0 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 |
| SMG | 2.1 | 2.1 | 1.05 | 1.05 | 1.05 | 1.05 | 1.3 | 1.3 | 1.3 | 1.3 | 1.3 | 1.3 |
| LMG | 2.3 | 2.3 | 1.05 | 1.05 | 1.05 | 1.0 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 |
| Shotgun | 1.5 | 1.5 | 0.9 | 0.9 | 0.9 | 0.9 | 1.05 | 1.05 | 1.05 | 1.05 | 1.05 | 1.05 |
| DMR | 2.5 | 2.5 | 1.3 | 1.3 | 1.3 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Sniper | 3.2 | 3.2 | 1.8 | 1.45 | 1.45 | 1.3 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 |
| Pistol | 2.1 | 2.1 | 1.05 | 1.05 | 1.05 | 1.05 | 1.3 | 1.3 | 1.3 | 1.3 | 1.3 | 1.3 |
| DamageType.Melee | 1.5 | 1.5 | 1.0 | 1.0 | 1.0 | 1.0 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 |
| CombatBow | 2.3 | 2.3 | 1.9 | 1.9 | 1.5 | 1.0 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 |
| Launcher | 1.5 | 1.5 | 1.0 | 0.6 | 0.6 | 0.6 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 |
| Vehicle.Cannon | 1.0 | 1.0 | 0.6 | 0.6 | 0.6 | 0.6 | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 | 0.3 |
| Vehicle.Turret.Minigun | 2.5 | 2.5 | 1.3 | 1.3 | 1.3 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Vehicle.Turret.MachineGun | 2.35 | 2.35 | 1.0 | 1.0 | 1.0 | 1.0 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 |
| Vehicle.Turret.Artillery | 3.2 | 3.2 | 1.8 | 1.8 | 1.8 | 1.3 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 |
| Vehicle.Turret.Heavy | 3.2 | 3.2 | 1.8 | 1.8 | 1.8 | 1.3 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 |
| Vehicle.HelicopterCannon | 3.2 | 3.2 | 1.8 | 1.8 | 1.8 | 1.3 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 |
| Vehicle.HelicopterRocket | 1.5 | 1.5 | 1.0 | 0.6 | 0.6 | 0.6 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 |

The Sniper row is the only one with a different Torso.Middle value (1.45) from Torso.Upper (1.8). Head and neck are always equal.

### 2d. Ammo Type Penetration Effectiveness (`DT_InfantryData_AmmoTypeEffectivenessPen`)

| Ammo tag | Modifier | Per-arm-class values (Small / Medium / High / Special) |
|---|---|---|
| `AmmoModifier.FMJ` | 1.0 | — |
| `AmmoModifier.Tracer` | 1.0 | — |
| `AmmoModifier.HollowPoint` | 1.5 | — |
| `AmmoModifier.HollowPoint.Tracer` | 1.5 | — |
| `AmmoModifier.ArmorPiercing` | 0.3 | 0.7 / 0.6 / 0.5 / 1.0 |
| `AmmoModifier.ArmorPiercing.Tracer` | 0.3 | 0.7 / 0.6 / 0.5 / 1.0 |

The per-arm keys use the `Meta.Damage.Arms.*` tag family. The name "Arms" is what the data uses; it is most likely an armour-class or penetration-tier axis, but that is not confirmed.

### 2e. Ammo Modifier Assets (`DamageSystem/AmmoModifiers/`, index in `DT_AmmoModifiers`)

Each asset multiplies the listed attribute on the projectile when that ammo tag is active.

| Ammo modifier | PenetrationEffectivenessMult | EffectiveRangeMult | PenetrationExitSpeedMult | TracerChance |
|---|---|---|---|---|
| ArmorPiercing | 1.8 | 1.2 | 0.0 | — |
| ArmorPiercing.Tracer | 1.76 | 1.2 | 0.0 | 1.0 |
| HollowPoint | 0.1 | 0.8 | 0.15 | — |
| HollowPoint.Tracer | 0.1 | 0.8 | 0.15 | 1.0 |
| Tracer | 1.0 | 1.0 | 0.075 | 1.0 |

The index asset `DT_AmmoModifiers` maps each tag to its `DA_AmmoModifier_*` asset (5 rows, all five listed above).

### 2f. Infantry Damage Modification Rules (`DT_GlobalDamage_InfantryData`, row `Meta.Damage.Infantry`)

The row has 129 entries. Most are no-op rows (60 entries with no requirements and 0% change). The table below lists the non-trivial unique rules. Values are percentage changes. Negative is a reduction.

| Category | Source | Target / hit | Change | Notes |
|---|---|---|---|---|
| Friendly | Bullet (hits Infantry) | — | −50% | Friendly-fire reduction |
| Friendly | LargeHammer | — | −70% | Friendly melee |
| Bone | Bullet (hits Infantry) | — | −75% | Custom operation, bone category |
| Bone | Cannon (hits Infantry) | — | −75% | Custom operation |
| Bone | ExplosiveBlunt (hits Infantry) | — | −75% | Custom operation |
| Calibre | 122mm | — | −45% | |
| Calibre | 155mm + Outer | — | −55% | |
| Calibre | Outer + 120mm / 84mm / 93mm | — | −50% each | |
| Calibre | Outer + C4 | — | −40% | |
| Calibre | Explosive | SuperHeavy | −50% | |
| Calibre | Rocket | Light / Medium / Heavy | −15% / −25% / −35% | Scales with target armour class |
| Calibre | 84mm + Inner | — | +1% | |
| Calibre | 7mmBuckshot / RifledSlug (hits Infantry) | — | 0% | Calibre pass-through |
| AmmoModifier | Bullet + ArmorPiercing | — | −20% | |
| AmmoModifier | Bullet + HollowPoint | — | +100% | |
| AmmoModifier | ExplosiveBlunt + Drone | — | +500% | |
| AmmoModifier | 7mmBuckshot | Helmet / Armor / SuperHeavy | −30% / −40% / −40% | |
| AmmoModifier | RifledSlug | Helmet / Armor / SuperHeavy | −5% / −13% / −12% | |
| AmmoModifier | Arrow | Any | 0% | |
| Penetration | Bullet (any target) | — | −50% | Custom operation |
| Penetration | Melee | Armor | −50% | Custom operation |
| PenetrationEffectiveness | Bullet + HollowPoint | Armor / Helmet | −40% / −40% | |
| PenetrationEffectiveness | 50Cal | Armor / Helmet | 0% | |
| PenetrationEffectiveness | Bullet (hits Infantry) | Armor / Helmet | 0% | Custom operation |

Friendly-fire and melee rules use the `Friendly` alignment. The rules are evaluated by `PriorityCategory` and `PriorityIndex`. The exact evaluation order and whether percentages stack additively or multiplicatively is not verified from the data.

### 2g. Armour and Helmet Rules (`DT_GlobalDamage_ArmorData`)

| Row | Entries | Effect as recorded |
|---|---|---|
| `Meta.Damage.Armor.Ghillie` | 6 | Source Bullet, Explosive, Cannon, Impact, Melee and one more: each −100% in Armor category |
| `Meta.Damage.Helmet.Ghillie` | 6 | Same pattern as the Ghillie armour row |
| `Meta.Damage.Armor` | 8 | Bullet −60%, Explosive −85%, Melee −50% (Armor); Bullet+Penetrate 0% (Penetration); Bullet+HollowPoint −30% (AmmoModifier); 7mmBuckshot −80% (AmmoModifier); target Ghillie −10000% (Armor) |
| `Meta.Damage.Helmet` | 7 | Bullet −60%, Explosive −85% (Armor); Bullet+HollowPoint −30%; Bullet+ArmorPiercing +30% (AmmoModifier); Bullet+Penetrate 0% |
| `Meta.Damage.Vehicle` (in `DT_GlobalDamage_InfantryData` family) | 10 | Mostly 0% or no-op; HollowPoint ±40%; Ricochet 0% |

**Unclear:** the Ghillie rows set −100% on most sources, and the `Meta.Damage.Armor` row sets −10000% against the Ghillie tag. Whether this is intended as full immunity or a placeholder should be checked in game.

### 2h. Vehicle Seat Damage Reduction (`DT_InfantryData_VehicleSeatDamageReduction`)

Each row is a vehicle variant. Its entries give `State.Player.Vehicle.SeatDamageReduction` by arm class. Values are percentage reductions applied to a player seated in that vehicle.

| Vehicle variant | Small / Medium | High | Special |
|---|---|---|---|
| Air.Rotary.ROT_01 (Default, MountedMachineGuns) | −50% | −20% | — |
| Air.Rotary.Havoc (Default) | −90% | −50% | −60% |
| Air.Rotary.Littlebird (Default, RocketPods, MountedMachineGuns) | −50% | −20% | — |
| Land.Wheeled.Humvee (Default, MachineGun, Minigun) | −70% | −40% | — |

The Havoc is the only seat row with a Special entry. The Humvee and Littlebird rows are identical across their variants.

### 2i. Hit-Location Asset for Infantry Damage

`DA_GlobalDamage_HitLocations_Player` holds the bone-to-class map in 2b. The bone table in 2c is keyed by the damage-type tag, and each row uses the 12 classes.

---

## 3. Projectiles (`Inventory/Equipment/Caliber/`, 31 `WDProjectileData` assets)

Units are not verified. The values are raw UE fields. Speed is `TypicalSpeed` (launch speed). `Thrust` is the sustained speed where present. Blank means the field is not set on the asset.

| Asset | ProjectileId | Base dmg | Expl. radius | Eff. radius | Falloff | Speed | Thrust | Mass | Drag | Ricochet ° |
|---|---|---|---|---|---|---|---|---|---|---|
| DA_TVGuidedMissile_Data | Caliber.84mm.TVGuided | 100 | 1000 | 400 | 0.5 | 22400 | 22000 | 2.3 | GC | 85 |
| DA_120x570mm_ProjectileData | Caliber.120x570mm | 150 | 750 | 420 | 0.3 | 22400 | 22000 | 20.0 | GC | 91 |
| DA_120x800mm_Standard | Caliber.120x800mm.Standard | 120 | 1000 | 500 | 0.45 | 15000 | 22000 | 15.0 | GC | 91 |
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
| DA_35x228mm | Caliber.35x228mm | 60 | — | 375 | 0.7 | 79200 | 22000 | 0.15 | G7 | 91 |
| DA_308Winchester | Caliber.308Win | 60 | — | — | — | 38500 | — | 0.012 | G7 | — |
| DA_338Norman | Caliber.338Nor | 105 | — | — | — | 50000 | — | 0.01944 | G7 | — |
| DA_762mm | Caliber.762mm | 42 | — | — | — | 38600 | — | 0.008 | G7 | — |
| DA_762x51mm | Caliber.762x51mm | 60 | — | — | — | — | — | 0.01 | G7 | — |
| DA_762x54mm | Caliber.762x54mm | 55 | — | — | — | 43000 | — | 0.0117 | G7 | — |
| DA_9mm | Caliber.9mm | 22 | — | — | — | 28000 | — | 0.007 | G1 | — |
| DA_45ACP | Caliber.45ACP | 30 | — | — | — | 32200 | — | 0.015 | G1 | — |
| DA_45Colt | Caliber.45Colt | 45 | — | — | — | 29200 | — | 0.01 | G1 | — |
| DA_50AE | Caliber.50AE | 63 | — | — | — | 41600 | — | 0.019 | G7 | — |
| DA_50Cal | Caliber.50Cal | 107 | — | — | — | 31500 | — | 0.051 | G7 | — |
| DA_545mm | Caliber.545mm | 26 | — | — | — | 30000 | — | 0.0034 | G7 | — |
| DA_556mm | Caliber.556mm | 28 | — | — | — | 40400 | — | 0.0041 | G7 | — |
| DA_12g_RifledSlug | Caliber.12g.RifledSlug | 105 | — | — | — | 29800 | — | 0.028 | GL | — |
| DA_7mmBuckshot | Caliber.7mmBuck | 25 | — | — | — | 29200 | — | 0.004 | GA | — |

Notes:
- Explosive rounds (rockets, grenades, artillery) carry a `DamageEntityData` tag (e.g. `Meta.Damage.Explosive.Rocket.155mm`). Bullets use `Meta.Damage.Bullet.<caliber>`.
- Rockets and cannon rounds set `bShouldPenetrate` to False. Ricochet angles are `MinImpactAngleForRicochet` in degrees.
- The `Drag` column is the `DragModel` row in `CT_Projectile_DragCoefficients` (GC Cylinder, G1 Flat Bottom, G7 Boat Tail, GL Blunt Nose, GA Pellet).
- Many 155mm and 120mm variants are duplicated across `_SB` (Sandbox) assets with different radii or mass. The Sandbox variant is a separate asset, not an override.

---

## 4. Action Definitions (`Actions/`, 114 `BH`/`WD` action definitions)

Each action carries an `ActionTag`, an `ActionClass` (blueprint), an `ActivationContextType` and a list of `ActionContext` flags. The context flags (Holdable, TwoHanded, OneHanded, Weapon, Interaction, Movement, UI, Emote, FollowProjectile) determine when the action is valid.

| Folder | Context | Count | Examples (tag) |
|---|---|---|---|
| `Actions/Appliables/` | WDAppliableItemActionContext | 4 | Appliable.PrimaryUse [Holdable, TwoHanded]; Appliable.SecondaryUse [Interaction, Holdable, TwoHanded] |
| `Appliables/Bandage/` | WDAppliableItemActionContext | 2 | Appliable.Bandage.PrimaryUse [Holdable, Interaction, TwoHanded]; Bandage.SecondaryUse [Holdable, TwoHanded] |
| `Character/` | WDEmoteActivationContext | 27 | `Action.Player.Emote.*` (26 emotes using `B_Action_Emote_C`) plus `Surrender_Drop` [Emote] |
| `Interaction/` | None / custom | 4 | Player.UseDoor, Player.Tracker, Player.Door.Breach, Player.Scene.VehicleAdmin |
| `Melee/` | WDGenericItemActionContext | 2 | Player.Melee.PrimaryUse and SecondaryUse [Holdable, TwoHanded, Weapon] |
| `Movement/` | Various | 25 | Jump, Sprint, TacSprint, Crouch, Prone, Crawl, Stand, Vaulting, Mantling, Climbing, Ladder, Fall, Swimming, Dragging, StopSprint, StopTacSprint |
| `Projectile/` | WDFollowProjectileActionContext | 1 | Projectile.Follow [FollowProjectile] |
| `Revive/` | Various | 2 | Player.Revive [Interaction, TwoHanded]; Player.RequestRevive |
| `UI/` | Mixed | 15 | Access inventory, tactical map, chatbox, radial wheel, ping wheel, equipment/garage/vehicle vendors, quick-slot change, ping and remove-ping, toggle hands |
| `Vehicle/` | None / Vehicle contexts | 1 | Vehicle.Movement [Movement] |
| `Vehicle/Weapons/` | WDVehicleWeaponActionContext | 7 | Vehicle.Weapon.Fire, PreFire, ADS, Reload, ActiveReload, Vehicle.Horn, Vehicle.ChangeStabilizingState |
| `Weapons/` | WDGenericItemActionContext / None | 26 | Weapon.Fire, Weapon.Reload, Weapon.ADS, Weapon.ChamberRound, Weapon.CycleFireMode, Weapon.CycleSights, Weapon.Zeroing.Increase/Decrease/Reset, Weapon.Bipod.Mount/ToggleFold, Weapon.MeleeBash, Throw.Primary/Back/Swap, Player.Lean.Left/Right, Player.Focus, Item.Inspect, Equipment.Change |

`DT_EmoteData` has 27 rows. `PlayRate` ranges from 0.95 to 1.2 (most at 1.0). Some rows set `Surrender_Drop` to a different flag.

---

## 5. Input (`Player/PlayerCharacter/Inputs/`)

| Item | Count | Notes |
|---|---|---|
| `BHInputAction` | 98 | 61 in `Inputs/`, 33 in `Inputs/PlayerController/`, 4 in `TaggedActions/` |
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

Input-side modifiers include `WDDeadZoneInputModifier` (10), `InputModifierSwizzleAxis` (9), `InputModifierNegate` (7), `WDAimAssistInputModifier` (1, filter `DA_AimAssistFilter`), `WDResponseCurveTypeModifier` (1), and `WDApplyAxisConfig` (8).

The controller configs in `Settings/Controls/ControllerConfigs/` (Infantry, GroundVehicle, HeavyVehicle, Helicopter) map these actions per device. Their contents were only partially decoded (see section 13).

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
| Controls.LookAccelMaxMultiplier | 0.5 | 10.0 | 1.6 | 1.0–3.0 | — | 1 decimal |
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

### 7a. Custom operation rules (`DA_CustomOperationRules`, 16 rules)

Each rule matches a drag/drop between inventory slots and performs a custom operation.

| # | Operation | Source item / slot | Destination item / slot |
|---|---|---|---|
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

- `WDCustomInventoryOperationRule_LoadAmmo` (2 rules) point to `DA_InventoryMagPackingData`.
- `WDCustomInventoryOperationRule_Transfer` (1 rule): `DefaultTransferTime` = 0.5 s. Equipment containers are `Inventory.Slot.Primary`, `Secondary`, `Sidearm`, `Specialist`, and others.

### 7d. Mag packing curves (`InventoryMagPacking/`, 37 `CurveFloat` plus `DA_InventoryMagPackingData`)

Three families, one curve per caliber:

| Family | Curve pattern (time, value) | Example |
|---|---|---|
| `CombineLooseAmmo/CR_CombineLooseAmmoCurve_<caliber>` | (0, 0.4–1.2) to (N, larger value) | 45ACP: (0, 0.4) (13, 1.9) (26, 3.8); 50Cal: (0, 1.2) (10, 7.0) (20, 14.0) |
| `ExtractAmmo/CR_ExtractAmmoCurve_<caliber>` | (0, 0.3–0.8) to (N, larger value) | 308Win: (0, 0.3) (60, 20.0); 545mm: (0, 0.3) (200, 40.0) |
| `LoadAmmo` family | not decoded in review | — |

The curve axis is not labelled in the data. The most likely reading is round count on the X axis and time or cost on the Y axis, but this is not verified.

---

## 8. Factions (`Gamemode/Data/DataAssets/`, `DT_FactionData`)

| Tag | Name | Short | Colour | Squad colour | Team ID | Safe zone tag |
|---|---|---|---|---|---|---|
| `Meta.Alignment.Faction.Alpha` | Lonestar | L* | `4CB1EF` | `EDA314` | 0 | `State.Location.SafeZone.Alpha` |
| `Meta.Alignment.Faction.Bravo` | Valkyra | Vlk | `FA503E` | `EDA314` | 1 | `State.Location.SafeZone.Bravo` |
| `Meta.Alignment.Faction.Charlie` | Manticore | Mtc | `1DD65C` | `EDA314` | 2 | `State.Location.SafeZone.Charlie` |
| `Meta.Alignment.Faction.Default` | White | White | — | — | 3 | — |

Each faction has block-colour materials (`MI_WDPlayerBlue` for Alpha, `MI_WDPlayerRed` for Bravo, `MI_WDPlayerGreen` for Charlie, `MI_WDPlayerNoTeam` for Default). The third-person character material list is set for two factions.

---

## 9. Player Character Components (`Player/PlayerCharacter/`)

| Component | Values |
|---|---|
| `WDFirstPersonCameraComponent` | FieldOfView **106.0**, OrthoWidth 512, `bAutoCalculateOrthoPlanes` false |
| `BHPerspectiveData` (`DA_PlayerCharacterComponents`) | Keyed templates (e.g. `FirstPersonBodyMesh`, each a `SkeletalMeshComponent` template). Full key list not expanded. |
| `WDWaveBreakerComponent` | Present, no exposed properties |
| `WDCharacterMovementEffectsComponentConfigurationDataAsset` | Per-stance movement effects (`Stances`, `JumpGameplayCueTag`, `LandingGameplayCueTags`, `StanceTransitionEffects`, `MovementModeEffects`) |
| `CurveFloat` (8) and `CurveVector` (4) in `Player/PlayerCharacter/Curves/` | Animation and camera curves (not decoded) |
| `Player/PlayerCharacter/MovementFeatures/Ladder/Curves` (3) | Ladder movement curves |

---

## 10. Destructible Objects (`WorldInteractable/Objects/EnvironmentalObjects/`)

| Asset type | Count | Notes |
|---|---|---|
| `BHDestructionBuildingDefinitionDataAsset` | 8 | One per door or garage type: `D_Door`, `D_InteractableDoor_Apartment`, `_ApartmentBalcony`, `_ApartmentEntrance`, `_Office`, `_WoodPVC`, `D_Interactable_GarageDoor_01a_Left`, `_Right`. Each has 1 required mesh, 1 chunk-data entry and 1 chunk lookup. |
| `BHDestructionBuildingDecoratorDefinitionDataAsset` | 7 | Decorators (`D_Decorator_Door`, `D_Decorator_InteractableDoor_*`) each with a `SaveID` GUID. |
| `B_TargetDummy` (blueprint) | 1 | Damage entity tag `Meta.Damage.Infantry`, vitality and inventory components. Hit-decay timers and armour toggles (`SetHelmetArmour`, `SetVestArmour`). Test asset. |

---

## 11. AI and EQS (`AI/`, `Gamemode/Objects/`)

| Asset | Contents |
|---|---|
| `BB_Enemy` (BlackboardData) | 8 keys: EnemyActor, HasLineOfSight, MoveGoal, SelfActor, TargetActor, Pressure, HasTeleportedToAO, SOClaimHandle |
| `EQS_FindDeploymentBoard` | Deployment-board search (1 option) |
| `EQS_FindNewFiringPosition` | Firing-position search (1 option) |
| `EQS_SpawnQuery_800` and `EQS_SpawnQuery_800_Bravo` | Spawn query, 800 units, with overlap test (2 each in `Gamemode/Objects`) |
| `CRV_EnemyDistancePressure` (CurveFloat) | Pressure falls from 1.0 at 0 to 0.0 at 3000 |

---

## 12. Assistance Requests, Vendors and Emotes

### 12a. Assistance requests (`Communication/AssistanceRequests/DT_AssistanceRequests`, 12 rows)

Rows: Ammo, Backup, Refueling, Healing, Repair, Revive, Pickup, Dropoff, Getout, SquadInvite, GetIn, Supplies. Each row has a `RequestClass` (`WDAssistanceRequest_*`), an `EventFeedTag`, `Duration`, `GameplayCueDuration`, distance limits for team events and spatial icons, and `CancelWhenEnteringVitalityStates`. The `bOnlyShowEventFeedToInvolvedPlayers` flag is true for the Repair, Revive, Dropoff and GetIn rows and false for Getout.

### 12b. Vendor markets (`WorldInteractable/NPCs/Vendor/`)

| Table | Rows | Price range (cash) | Notes |
|---|---|---|---|
| `VendorEquipment/DT_WeaponMarket` | 36 (154 price variations) | 0–1050 | Magazines, weapons, sizes; Alpha and Bravo faction-specific items |
| `VendorEquipment/DT_AttachmentMarket` | 17 | 380–1800 | Optics, muzzles, grips (e.g. `SniperScope10x` 1200, `EotechHoloSight` 620, `RK6ForeGrip` 380) |
| `VendorEquipment/DT_GearMarket` | 13 | 0–15000 | Vests (Small 100, Medium 250, Large 400), backpacks (Small 350 to ExtraLargeSling 5000) |
| `VendorEquipment/DT_UtilityMarket` | 3 | 200–800 | Bandage 200, SuperBandage 800, M67Grenade 200 |
| `VendorVehicles/DT_VehicleMarket` | 0 | — | Empty in this dump |

Each row has `VendorItemVariations` with `Price`, `LevelToUnlock`, `Amount`, `LifeTimeBuyLimit` and optional faction lock.

### 12c. Emote data (`Actions/Character/DT_EmoteData`, 27 rows)

Each row has a `PlayRate` (0.95 to 1.2) and several boolean flags whose names are hashed and not decoded. `Surrender_Drop` is the only row with a flag set to true in the first flag column.

---

## 13. Curves and Scalar Modifiers (summary)

- **Gamemode/Data/ScalarModifiers** (6 curves): `CF_Reward_Assist_DamagePlayer` and `DamageVehicle` ramp 0→1 over input 0–1. `CF_Reward_HealPlayer` ramps 0.25 to 1.0 over input 0–1.0. `CF_Reward_ReviveHealPlayer` 0→0.2 at 0.4, 1.0 at 1.0. `CF_Reward_Build` and `CF_Reward_SupplyCrateItemPurchase` are identity curves (output equals input) across ±1,000,000. These scale rewards; the reward tables are in the rewards doc.
- **Inventory/InventoryMagPacking** (37 curves): see 7d.
- **Total curves in folder:** 60 `CurveFloat` assets plus 1 `CurveTable` (`GameplayEffects/Curves`) and 4 `CurveVector`.

---

## 14. How Values Combine

- **Infantry hit damage:** the bone multiplier (2c) is chosen by damage-type row, then the hit location. The Universal row is the fallback. Infantry modification rules (2f, 2g) then adjust the result. The rules are sorted by `PriorityCategory` and `PriorityIndex`. The exact combination (additive percentages vs multiplicative) is not verified.
- **Armour-piercing and hollow-point:** the ammo-modifier assets (2e) multiply penetration effectiveness, range and exit speed. The per-arm penetration table (2d) then scales damage per armour class.
- **Vehicle occupants:** seat reduction (2h) is a flat percentage by vehicle variant and arm class.
- **Explosives:** `BaseDamage` and `ExplosiveRadius` (section 3) feed the Calibre rules (2f). Falloff is the `ExplosiveDamageFallOff` field.
- **Vendor price:** `Price` is per variation. The vendor UI applies the `LevelToUnlock` gate and the `LifeTimeBuyLimit`.

---

## 15. Still Not Pulled / Limitations

- **Hashed property names.** Many struct fields use names like `_aaabckamhakccdhbomlfj_$A0C70A22...$`. These are the arm-class arrays in 2d, the seat-reduction arrays in 2h, the `Emote` flags in 12c, and some action fields. Their meaning was inferred from neighbouring values and is not confirmed.
- **Operation semantics.** `Percentage_Ongoing` is the operation name on the modification entries. Its exact formula (additive, multiplicative, applied per tick or once) is not decoded.
- **Arm-class naming.** `Meta.Damage.Arms.Small/Medium/High/Special` is the tag family used. Its meaning as armour class or penetration tier is an inference.
- **Units.** Projectile speed, radius and mass units are not verified against the engine.
- **Controller configs.** `Settings/Controls/ControllerConfigs/` (13 files) and the 106 `BHPlayerMappableKeySettings` default keys were only partially decoded. Default key-to-action bindings are in `IMC_*` DefaultKeyMappings, which were counted but not expanded.
- **Infantry rules.** The 129-entry `Meta.Damage.Infantry` row was aggregated to unique rules (69 unique, 60 no-op). Not every unique rule is listed in 2f.
- **Vendor weapon market.** The 36 rows in `DT_WeaponMarket` were summarised by price range only. Individual items were not listed.
- **Empty vehicle market.** `DT_VehicleMarket` has 0 rows, so vehicle vendor prices are not in this dump.
- **Destruction chunk data.** Chunk IDs and mesh references in the destructible-building assets were counted, not expanded.
- **Player curves.** The 8 `CurveFloat` and 4 `CurveVector` assets in `Player/PlayerCharacter/Curves/` were not decoded.
- **Reward tables.** `Gamemode/Data/DT_CashRewards` (49 rows), `DT_Rewards` (78 rows), `DT_AssistCashRewards` (9), `DT_CashRewardModifiers` (9) and the `CashRewardsDataTable/` tree are covered in `Wardogs_Rewards_and_Progression_v2.md`, not here.
- **EQS details.** The EQS query contents (generators, tests and scoring equations) were listed by name only.
