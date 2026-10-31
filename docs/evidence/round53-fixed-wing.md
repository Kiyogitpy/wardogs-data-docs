# Round 53: the fixed-wing airplane (FWG_01) health, spawn, shop and status

Statuses: FOUND, NATIVE, SERVER, ABSENT, PROTECTED. Evidence: cooked data read (WdExtract dumps, exported `data/`) and decompiled corpus read (not run). The game was never run, no devirtualization. Extractor output: `E:/Reverse_Engineer/wardogs_analysis/round53_plane/` (`FWG/rawfiles.txt`, `Airplane/rawfiles.txt`, `dump/B_FWG_01.json`, `dump/PA_FWG_01.json`, `dump2/SM_FWG_01_Body.json`, `dump2/SK_FWG_01.json`).

Result in one line: the airplane has a start health number (150) and health-threshold effects, but **no health sections, no collision-slot map and no hit zones**, so no damage can reach it through the vehicle damage path. Round 52 was right to leave it out. There are no hit counts to compute, so `_tools/round52_explosive_hits.py` and `assets/data/explosive-hits-vs-vehicles.json` are unchanged.

## 1. Health, damage rules, hitboxes

| Finding | Status | Source |
|---|---|---|
| `InitialVehicleHealth` = 150.0 | FOUND | [`DA_FWG_01_GameplaySystems`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Vehicles/Pawns/Air/Airplane/FWG_01/Data/DA_FWG_01_GameplaySystems.json) `HealthSettings` |
| Smoke cue at main health below 90%; fuel-leak effects at fuel tank below 90% / 50% / 0% (0.1 / 0.4 / 0.5 per second) | FOUND | [`DA_FWG_01_GameplaySystems`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Vehicles/Pawns/Air/Airplane/FWG_01/Data/DA_FWG_01_GameplaySystems.json) threshold triggers (also `assets/data/vehicle-health-effects.json`) |
| Damage rule row `Meta.Damage.Vehicle.Air.Rotary.LittleBird` (copied from the Little Bird family; 7.5% rifle factor) | FOUND | [`DA_FWG_01_GameplaySystems`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Vehicles/Pawns/Air/Airplane/FWG_01/Data/DA_FWG_01_GameplaySystems.json) `DamageEntitySettings.VehicleDamageTag` |
| `MVF_HealthSections` fragment on [`VP_FWG_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Vehicles/Platforms/Air/VP_FWG_01.json) | ABSENT | The platform has only two fragments, `MVF_VehicleConfig` and `MVF_Seats`. Every other vehicle with a damage model (ROT_02, ROT_03, ROT_04, SPW, STN, TNK, WHL) carries `MVF_HealthSections` in its platform or parts. `_tools/damage_tables.py` `sections()` returns `{}` for [`VV_FWG_01_Default`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Vehicles/Variants/Air/VV_FWG_01_Default.json). |
| Collision-slot-to-section map (`ComplexSurfaceMappings`) and physics-group map | ABSENT | Both come only from `MVF_HealthSections` (pipeline section 3, registration `0x53214A0`). None exists. |
| Collision slots on the model | ABSENT | `SM_FWG_01_Body` has only the collision tag `CC_WorldStatic`; `SK_FWG_01` has no `CC_*` tag. Other vehicles use `CC_MainBody`, `CC_Engine`, `CC_FuelTank` and so on. |
| Physics asset `PA_FWG_01` | FOUND (no hit zones) | 10 bodies: `body_J` and the wheel bones only. The physics asset takes no part in damage zone lookup (pipeline section 3.1). |
| A hit with no section does nothing | FOUND (decompiled read, not run) | `sub_1453205D0` (`ApplyDamageToSection`, RVA `0x53205D0`): `sub_14532B660(a1 + 76, &key)` looks the section up in the map at component `+0x130`; a null result returns zero at once. With no fragment the map is empty, so every point and radial hit returns 0. Airplane damage slot 367 reaches this path like the other vehicles (pipeline section 1). |
| Collision damage | ABSENT | `ApplyCollisionDamage` reads the physics-group map (`+0x1D0`), also filled only by `MVF_HealthSections`. |
| Whether the 150 HP and the thresholds can ever fire | NATIVE (open) | The thresholds watch the `Attribute.Gameplay.Health` and `.FuelTank` attributes. Nothing in the data lowers those attributes for this vehicle. Whether native code lowers them by a path that skips sections (for example scripted destruction) was not traced. |
| `B_FWG_01` components | FOUND | `WDVehicleDamageModelComponent` (two instances, default properties), `WDDamageEntityComponent`, `BHComplexSurfaceComponent`, fuel, lock and seat components: the standard set, all with default properties. The damage model component is present but is given no sections. |

Conclusion for the explosive tables: with no section, `hits_to_destroy` has nothing to reduce, so there is no count. Nothing is added to the round 52 JSON or to the wiki comparison tables; their "not simulated" cells stay.

## 2. Spawn

| Finding | Status | Source |
|---|---|---|
| Variant tag `Vehicle.Variant.Air.Airplane.FWG.Default` is declared | FOUND | `Config/Tags/VehicleGameplayTags.ini`, [`VV_FWG_01_Default`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Vehicles/Variants/Air/VV_FWG_01_Default.json) |
| 20 of 21 air yards allow the generic `Air` tag, which covers every air variant tag, so their yard rule admits the airplane | FOUND (rule); tag hierarchy inferred | `assets/data/vehicle-spawns.json`, volumes of kind `air` (15 exclude `Land`, 5 exclude the faction APC tags) |
| The 21st air yard (NorthAmerica, no data layer, `WDSpawnVolume_UAID_E89C25C716F293DC02_1095813688`) lists Havoc, Little Bird, ROT_01 and ROT_04 only | FOUND | same JSON; it does not admit the airplane |
| 27 APC and light yards list `Air.Airplane` among their excluded tags | FOUND | same JSON. The level designers named the airplane family when keeping air out of ground yards. |
| No yard, board or experience config names the airplane as a vehicle to place; no world cell holds an `FWG` or `B_FWG_01` reference (the 20 map-file hits of `rawfiles FWG` are random cell names) | ABSENT | `FWG/rawfiles.txt` |
| What a yard actually places and how it chooses | NATIVE | the spawn volume logic and the vehicle-order path are native and were not traced; the data has no per-yard vehicle list |

So: allowed by the tag rules of 20 air yards, never named. The data does not show whether a match has ever spawned one.

## 3. Shop and unlock

| Finding | Status | Source |
|---|---|---|
| Not in the market table | ABSENT | [`Meta/Collection/DT_GoldMarket.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Collection/DT_GoldMarket.json) has helicopter vehicle rows, no airplane |
| Not in a role or unlock tree | ABSENT | [`Meta/CharacterSkills/DT_MetaTree_Roles.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_MetaTree_Roles.json), [`DA_UI_PlatformMastery_SceneData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Mastery/Platforms/Data/DA_UI_PlatformMastery_SceneData.json) and the skin tables (`Skin_*`, [`DT_Cosmetics_Season02_Skins`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season02_SkinsData/Content/Data/DT_Cosmetics_Season02_Skins.json)) name helicopters; none names the airplane |
| No vehicle UI entity row, display name or description | ABSENT | helicopters have `DT_EntityData_UI_Vehicles_*` rows in their plugins; the airplane has none, and no other file mentions it (`Airplane/rawfiles.txt` finds only the input assets) |
| No destroy-vehicle reward row, no wager row | ABSENT | `DT_RewardLookup_SessionEvent_DestroyVehicle*` and [`DT_WagerConditions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerConditions.json) name helicopter variants, not the airplane |
| No seat damage reduction row | ABSENT | [`DT_InfantryData_VehicleSeatDamageReduction`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json) has helicopter rows only |

## 4. Wired in elsewhere

| Finding | Status | Source |
|---|---|---|
| Six weapons list it as an allowed lock-on target: 9K333 Verba ([`Launcher_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/Launcher_04/Content/Launcher_04.json)) and the stationary weapons STN_01, STN_02, STN_03, STN_05, STN_06 | FOUND | `AllowedTargets` in [`ID_Launcher_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/Launcher_04/Content/Data/ID_Launcher_04.json) and `WE_STN_01/02/03/05/06_*` |
| Demolition ruleset lets it hit destructible objects | FOUND | [`BH_Demolition_RS_AirVehicles`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Demolition/RuleSets/Vehicles/BH_Demolition_RS_AirVehicles.json) `PermittedVehicles` |
| Input context [`IMC_Airplane_Driver`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Vehicles/Inputs/IMC_Airplane_Driver.json) is registered with settings and mapped | FOUND | `DefaultGame.excerpt.ini`, [`PIMC_Default_Config`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/PIMC_Default_Config.json); round 40 |
| Spotting tracker and range-finder entries for the class `WDAirplaneVehicle` | FOUND | [`DA_Tracker_Spatial_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Spatial/Data/DA_Tracker_Spatial_Spotting.json), [`DA_Tracker_Map_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Map/Data/DA_Tracker_Map_Spotting.json), `ID_RangeFinder_*`, [`ID_Binoculars_Standard`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Binoculars/Content/Data/ID_Binoculars_Standard.json), [`ID_Monocular`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/RangeFinder/Content/Data/ID_Monocular.json) |
| Flares: 3 starting, 3.5 s; fuel and fuel-leak effects | FOUND | `assets/data/vehicle-flares.json`, health-effects JSON; no flare logic in the Blueprint (round 40) |

## 5. Is it a test or unfinished vehicle?

Evidence is FOUND; the verdict is an inference.

- It lives in the base game [`Content/Vehicles`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Vehicles) folder. Every shipped vehicle is a game-feature plugin with its own UI and damage data.
- The meshes still use `M_F15E_*` and `MI_F15E_Interior` materials, a placeholder look taken from an F-15E model. The exhaust effects are named jet engine exhausts.
- No display name, shop row, unlock, reward, UI row or health sections.
- It has a complete flight model, destroyed mesh, seat data, inputs and spotting entries, so it was built far enough to fly. The combat and economy side was never finished.

Reading: an unfinished vehicle, flyable in principle, not set up as a playable product. The data cannot show whether any build placed it.

## Wiki updates

- `_wiki/vehicles/fixed-wing-airplane.md`: rewritten from "the data does not simulate hits" to the plain finding (150 start HP number, no damage zones so hits do nothing, no shop or unlock, not named by any yard, lock-on target of Verba and emplaced weapons, unfinished vehicle).
- `_wiki/vehicles/vehicle-comparison.md`: note reworded to say why no hit counts exist. `_wiki/guides/anti-vehicle-guide.md`: no change needed (no counts exist).
