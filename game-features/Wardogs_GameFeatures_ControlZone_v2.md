---
title: "Control Zone"
redirect_from: ["/Wardogs_GameFeatures_ControlZone_v2.html", "/Wardogs_GameFeatures_ControlZone_v2"]
parent: "Game Modes & Maps"
description: "The Control Zone mode package: zone geometry, hot zone movement, balance modifiers, reward feed, placement rules, HUD and AI teleport."
---

# Wardogs — GameFeature: ControlZone Reference
*Extracted from cooked game data (build `++Wardogs+Live-CL-516586`, UE 5.7.4). Source: [`Wardogs/Plugins/GameFeatures/ControlZone/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/ControlZone) (21 JSON files). Scripted pass over every file, then spot-checked against the configs and tables.*

> **Scope:** this folder defines **how Control Zones are shaped, placed and moved** per map, and the HUD, placement and reward-feed plumbing around them. The per-tick **reward cash values** for Control Zone and Hot Zone (contested, owned, entered, passenger events) are in `Wardogs_Rewards_and_Progression_v2.md`, section 6a. The **map-level zone regions** are in the sibling doc `Wardogs_GameFeatures_ControlZoneRegions_v2.md`.

---

## Season 02 update (2026-10-15)

- Four zone configs added: [`DA_ControlZoneConfig_SniperShowdown_NorthAmerica`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZoneConfig_SniperShowdown_NorthAmerica.json), [`DA_ControlZoneConfig_SniperShowdown_Russia`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZoneConfig_SniperShowdown_Russia.json), [`DA_ControlZone_Config_Africa`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZone_Config_Africa.json) and [`DA_ControlZone_Config_Russia`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZone_Config_Russia.json) (zone configs 5 → 9; JSON files 17 → 21).
- Africa and Russia are 55,000 × 55,000 × 15,000 cylinders with 8,500-unit Hot Zones and 25 s move delay. Each has four alternators, all Ellipse zones of 50,000 × 50,000 × 50,000: Africa `Kenya.Default` weight 1.0 (North, East, West 0.0); Russia `Sabartulo.Hospital` weight 1.0 (Bazaar, River, Hillside 0.0).
- The two new Sniper configs are 35,000 × 35,000 × 17,000 cylinders with 7,500-unit Hot Zones, no alternators, zero first and move delay, default speed 1.5 and the same speed table as the Sniper Bakurani config.

Full before/after list: [Season 2 Changes → Game Modes & Maps]({{ '/season-2-changes/game-modes-maps.html' | relative_url }}).

---

## 1. Package Contents

| Group | Files | Contents |
|---|---|---|
| Root bundle | 1 | [`ControlZone.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone.json) (`GameFeatureData`) with 4 actions: `AddComponents`, `AddWorldPartitionContent`, `DataRegistrySource`, and a `WDGameFeatureAction_AddWidgetElements` that adds 15 HUD widget instances. |
| Zone configs ([`ControlZone/Config/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config)) | 9 | `WDControlZoneConfigDataAsset`: Bakurani, Gym_Minimal, SniperShowdown_Bakurani, SniperShowdown_NorthAmerica, SniperShowdown_Russia, Europe, NorthAmerica, Africa, Russia. |
| Balance | 1 | [`DT_ControlZoneContributionModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Data/DT_ControlZoneContributionModifiers.json) (3 rows): vitality multipliers. |
| Reward feed | 1 | [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) (12 rows). |
| Placement UX | 2 | [`DT_ControlZone_PlacementDisplayTexts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/DT_ControlZone_PlacementDisplayTexts.json) (1 row), [`DT_DeploymentRejectionReasons_ControlZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/DeploymentBoard/DT_DeploymentRejectionReasons_ControlZone.json) (1 row). |
| AI | 1 | [`EQS_FindControlZoneTeleportLocation`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/AI/EQS/EQS_FindControlZoneTeleportLocation.json) (EnvQuery with 1 generator, 3 tests). |
| HUD / trackers | 5 | [`DA_GameModeStatus`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/GameModeStatus/Data/DA_GameModeStatus.json), [`DA_GameModeStatusEntry`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/GameModeStatus/Widgets/Entry/Data/DA_GameModeStatusEntry.json), [`DA_Tracker_Map_ControlZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/Trackers/MapTrackers/Data/DA_Tracker_Map_ControlZone.json), [`DT_TrackerData_Map_ControlZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/Trackers/MapTrackers/Data/DT_TrackerData_Map_ControlZone.json), [`DA_ControlZone_SpatialTracker`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/Trackers/SpatialTrackers/Data/DA_ControlZone_SpatialTracker.json), [`DT_Trackers_ControlZone_Spatial`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/Trackers/SpatialTrackers/Data/DT_Trackers_ControlZone_Spatial.json). |

Note: [`DT_TrackerData_Map_ControlZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/Trackers/MapTrackers/Data/DT_TrackerData_Map_ControlZone.json) and [`DT_Trackers_ControlZone_Spatial`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/Trackers/SpatialTrackers/Data/DT_Trackers_ControlZone_Spatial.json) are DataTables with 1 row each. Their rows point to the `DA_` data assets.

---

## 2. Zone Geometry Per Config

Every base zone is a **Cylinder** (`EWDZoneShape::Cylinder`); the Africa and Russia alternators are **Ellipse** zones (see 2a). Each config has a **Control Zone** (the capture area, `ZoneData.ControlZoneData`) and an inner **Hot Zone** (`ZoneData.HotZoneData`). Values are in engine units (cm).

| Config | Control Zone extents (X × Y × Z) | Hot Zone extents (X × Y × Z) | Centre (X, Y, Z) | Alternators |
|---|---|---|---|---|
| [`DA_ControlZoneConfig_Bakurani`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZoneConfig_Bakurani.json) | 50,000 × 50,000 × 17,000 | 8,500 × 8,500 × 17,000 | (-836,067, -1,123,312, -95,160) | **3** (see 2a) |
| [`DA_ControlZone_Config_Europe`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZone_Config_Europe.json) | 55,000 × 55,000 × 15,000 | 8,500 × 8,500 × 15,000 | (-638,341, -620,784, n/a) | **4** (see 2a) |
| [`DA_ControlZone_Config_NorthAmerica`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZone_Config_NorthAmerica.json) | 50,000 × 50,000 × 50,000 | 8,500 × 8,500 × **85,000** | (-112,728, -211,237, n/a) | **4** (see 2a) |
| [`DA_ControlZoneConfig_SniperShowdown_Bakurani`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZoneConfig_SniperShowdown_Bakurani.json) | 35,000 × 35,000 × 17,000 | 7,500 × 7,500 × 17,000 | (-672,688, -1,117,098, n/a) | none |
| [`DA_ControlZoneConfig_SniperShowdown_NorthAmerica`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZoneConfig_SniperShowdown_NorthAmerica.json) | 35,000 × 35,000 × 17,000 | 7,500 × 7,500 × 17,000 | (-61,478, -245,857, 3,641) | none |
| [`DA_ControlZoneConfig_SniperShowdown_Russia`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZoneConfig_SniperShowdown_Russia.json) | 35,000 × 35,000 × 17,000 | 7,500 × 7,500 × 17,000 | (-40,227, -65,866, 13,214) | none |
| [`DA_ControlZone_Config_Africa`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZone_Config_Africa.json) | 55,000 × 55,000 × 15,000 | 8,500 × 8,500 × 15,000 | (231,528, 240,518, 0) | **4** (see 2a) |
| [`DA_ControlZone_Config_Russia`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZone_Config_Russia.json) | 55,000 × 55,000 × 15,000 | 8,500 × 8,500 × 15,000 | (-18,147, -5,916, 13,214) | **4** (see 2a) |
| [`DA_ControlZoneConfig_Gym_Minimal`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZoneConfig_Gym_Minimal.json) | 5,000 × 5,000 × 2,500 | none (shape only) | (9,290, -1,030, 0) | none |

Notes:
- The NorthAmerica Hot Zone is 85,000 tall against a Control Zone that is 50,000 tall. That is about 1.7× the Control Zone height, unlike the other configs where the two heights are equal. It may be intentional, but the values look unusual and were not verified in-game.
- The Gym config has no Hot Zone extents, only a shape. Its Hot Zone sizing must come from elsewhere.
- Centre Z is only listed where the config sets it (Bakurani, Africa, Russia and the two new Sniper configs). For the others, the Z of the actor location was not captured in this pass.

### 2a. Alternator zones (`AlternatorZoneData`)

An alternator is an **alternative placement** of the same zone. Each entry has its own Control Zone, Hot Zone, a `AlternatorTag` and a `AlternatorSelectionWeight`. The weight suggests one placement is chosen by weighted random selection per match (inferred, not confirmed in code). For Bakurani, Europe and NorthAmerica each alternator's extents match the base config. The Africa and Russia alternators are 50,000 × 50,000 × 50,000 Ellipse zones with 8,500 × 8,500 × 50,000 Hot Zones, which do not match their base config.

| Config | Alternator tag | Weight |
|---|---|---|
| Bakurani | `ZoneAlternator.Bakurani.Default.Circle` | 2.0 |
| Bakurani | `ZoneAlternator.Bakurani.Farmland.Circle` | 1.0 |
| Bakurani | `ZoneAlternator.Bakurani.Lumberyard.Circle` | 1.0 |
| Europe | `ZoneAlternator.Ozeti.Default.Circle` | 1.0 |
| Europe | `ZoneAlternator.Ozeti.Farmland.Circle` | **0.0** (zero weight) |
| Europe | `ZoneAlternator.Ozeti.Church.Circle` | 1.0 |
| Europe | `ZoneAlternator.Ozeti.River.Circle` | 1.0 |
| NorthAmerica | `ZoneAlternator.Zestafona.Default.Circle` | 1.0 |
| NorthAmerica | `ZoneAlternator.Zestafona.SmallFactory.Circle` | **0.0** (zero weight) |
| NorthAmerica | `ZoneAlternator.Zestafona.WaterTreatment.Circle` | 1.0 |
| NorthAmerica | `ZoneAlternator.Zestafona.Houses.Circle` | 1.0 |
| Africa | `ZoneAlternator.Kenya.Default.Circle` | 1.0 |
| Africa | `ZoneAlternator.Kenya.North.Circle` | **0.0** (zero weight) |
| Africa | `ZoneAlternator.Kenya.East.Circle` | **0.0** (zero weight) |
| Africa | `ZoneAlternator.Kenya.West.Circle` | **0.0** (zero weight) |
| Russia | `ZoneAlternator.Sabartulo.Hospital.Circle` | 1.0 |
| Russia | `ZoneAlternator.Sabartulo.Bazaar.Circle` | **0.0** (zero weight) |
| Russia | `ZoneAlternator.Sabartulo.River.Circle` | **0.0** (zero weight) |
| Russia | `ZoneAlternator.Sabartulo.Hillside.Circle` | **0.0** (zero weight) |

The `bActivateAlternator` flag is **True** on Bakurani, Europe, NorthAmerica, Africa and Russia. It is not set on the Sniper and Gym configs. Those have no alternators at all.

The weight-0 entries are kept in the data. Under a weighted pick they would never be chosen. They may be placements disabled for balance or testing; that is an inference from the weight alone.

---

## 3. Hot Zone Movement

Hot Zones move during a match. Movement is controlled by `HotZoneMovementData`.

| Config | MoveDelay | FirstMoveDelay | Inner radius % | Default speed | Dynamic speeds | Speed table | Min move distance |
|---|---|---|---|---|---|---|---|
| Bakurani | 25.0 | not set | 0.95 | 1.0 | on | 0.75, 1.0, 1.25, 1.5, 1.75, 2.0 | not set |
| Europe | 25.0 | not set | 0.95 | 1.0 | on | 0.75, 1.0, 1.25, 1.5, 1.75, 2.0 | not set |
| NorthAmerica | 25.0 | not set | 0.95 | 1.0 | on | 0.75, 1.0, 1.25, 1.5, 1.75, 2.0 | not set |
| Gym_Minimal | 25.0 | not set | **1.0** | 1.0 | on | 0.75, 1.0, 1.25, 1.5, 1.75, 2.0 | **750** |
| SniperShowdown_Bakurani | **0.0** | **0.0** | 0.95 | **1.5** | on | **1.25, 1.5, 2.0, 2.25, 2.75, 3.0** | not set |
| SniperShowdown_NorthAmerica | **0.0** | **0.0** | 0.95 | **1.5** | on | **1.25, 1.5, 2.0, 2.25, 2.75, 3.0** | not set |
| SniperShowdown_Russia | **0.0** | **0.0** | 0.95 | **1.5** | on | **1.25, 1.5, 2.0, 2.25, 2.75, 3.0** | not set |
| Africa | 25.0 | not set | 0.95 | 1.0 | on | 0.75, 1.0, 1.25, 1.5, 1.75, 2.0 | not set |
| Russia | 25.0 | not set | 0.95 | 1.0 | on | 0.75, 1.0, 1.25, 1.5, 1.75, 2.0 | not set |

How the fields read (inferred from names; no runtime check):
- **MoveDelay**: seconds between Hot Zone relocations (25 s on the standard maps).
- **FirstMoveDelay**: delay before the first move. Only the Sniper configs set it, to 0.
- **HotZoneInnerRadiusPercentage**: the Hot Zone's effective inner radius as a fraction of its extents. 0.95 is the standard. 1.0 on Gym means the full extent.
- **DefaultSpeed** and **HotzoneSpeeds**: move speed multiplier. The speed table is used when `bUseDynamicHotzoneSpeeds` is on. The Sniper configs run faster throughout, from 1.25 to 3.0.
- **MinHotZoneMoveDistance**: smallest move allowed, in units. Only Gym sets it (750).
- **HotZoneTransitionEasingCurve**: an easing curve over the move, with keys at time 0 → 0 and time 1 → 1 on the standard configs (cubic, auto tangents).

---

## 4. Balance: Contribution Modifiers ([`DT_ControlZoneContributionModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Data/DT_ControlZoneContributionModifiers.json))

Applied to a player's contribution to the zone based on their vitality state.

| Row | Vitality tag | Multiplier |
|---|---|---|
| Alive | `State.Player.Vitality.Alive` | **1.0** |
| Critical | `State.Player.Vitality.Critical` | **0.0** |
| Dead | `State.Player.Vitality.Dead` | **0.0** |

So a critically wounded player does not contribute to capturing a zone. The multiplier is a flat 0 or 1.

---

## 5. Reward Feed Actions ([`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json), 12 rows)

These rows are the reward-feed messages. Each is keyed by a `Meta.Progression.Resources.MatchScore.ObjectiveScore.*` tag. The rows have **no display text in this table** (`SourceString` is None) and their `Tag` column is None, so the strings are localised elsewhere.

| Feed key | Event | Audio event |
|---|---|---|
| `ControlZoneContested` | Control Zone contested | none |
| `ControlZoneEntered` | Entered Control Zone | none |
| `ControlZoneOwned` | Control Zone owned | none |
| `ControlZoneNotOwned` | Control Zone not owned | none |
| `HotzoneContested` | Hot Zone contested | none |
| `HotzoneEntered` | Entered Hot Zone | none |
| `HotzoneOwned` | Hot Zone owned | none |
| `HotzoneNotOwned` | Hot Zone not owned | none |
| `ControlZoneDeliveredPassengers` | Passenger delivered to Control Zone | `Audio.Event.UX.Cash.DeliveredPassenger` |
| `HotzoneDeliveredPassengers` | Passenger delivered to Hot Zone | `Audio.Event.UX.Cash.DeliveredPassenger` |
| `ControlZonePassengerSpawned` | Passenger spawned in Control Zone | `Audio.Event.UX.Cash.SpawnPassenger` |
| `HotzonePassengerSpawned` | Passenger spawned in Hot Zone | `Audio.Event.UX.Cash.SpawnPassenger` |

The cash amounts for these same events are in `Wardogs_Rewards_and_Progression_v2.md`, section 6a. The feed keys here are the match-score resource tags those amounts are booked to.

---

## 6. Placement and Deployment Rejection

Two strings handle the case where a player tries to place or deploy outside a Control Zone.

| Table | Tag | Localised key |
|---|---|---|
| [`DT_ControlZone_PlacementDisplayTexts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/DT_ControlZone_PlacementDisplayTexts.json) | `UI.Interactions.PlacementWarnings.NotInControlZone` | `PlacementWarning.LocationNotInControlZone` |
| [`DT_DeploymentRejectionReasons_ControlZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/DeploymentBoard/DT_DeploymentRejectionReasons_ControlZone.json) | `Interactive.Deployment.Rejection.NotInControlZone` | `RejectionReasons.NotInControlZone` |

Both live in `/ControlZone/UI/STRINGS_ControlZone`.

---

## 7. HUD: Game Mode Status

The HUD element `UI.HUD.Element.GameModeStatus` is registered by the root bundle with the widget `W_GameModeStatus` (under `/ControlZone/UI/GameModeStatus/`).

Localised strings used by this element:

| Key | Use |
|---|---|
| `ControlZone.HUD.GameModeStatus.State.WaitingToStart` | Before the zone is active |
| `ControlZone.HUD.GameModeStatus.State.Contested` | Zone is contested |
| `ControlZone.HUD.GameModeStatus.State.Controlled` | Zone is controlled |
| `ControlZone.HUD.SpatialTrackers.AOZone` | Off-zone pointer text (Control Zone) |
| `ControlZone.HUD.SpatialTrackers.HotZone` | Off-zone pointer text (Hot Zone) |

The [`DA_GameModeStatus`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/GameModeStatus/Data/DA_GameModeStatus.json) and [`DA_GameModeStatusEntry`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/GameModeStatus/Widgets/Entry/Data/DA_GameModeStatusEntry.json) data assets hold the layout and per-entry settings. Their numeric content was not extracted in this pass (section 9).

---

## 8. AI: Teleport Location Query ([`EQS_FindControlZoneTeleportLocation`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/AI/EQS/EQS_FindControlZoneTeleportLocation.json))

An Environment Query used to find a teleport destination near a Control Zone.

| Element | Type | Detail |
|---|---|---|
| Generator | `WDEnvQueryGenerator_ConeBetweenContexts` | Cone between two contexts, with the centre actor being `EQS_Context_ControlZone` |
| Test 1 | `EnvQueryTest_Distance` | Distance test |
| Test 2 | `EnvQueryTest_Distance` | Distance test with `DistanceTo` = `EQS_Context_ControlZone` |
| Test 3 | `WDEnvQueryTest_InControlZone` | Keeps only points inside a Control Zone |

The purpose (where the AI teleports to) is inferred from the name and the tests. The distance thresholds were not extracted.

---

## 9. Limitations

- **Not extracted in this pass:** numeric content of [`DA_GameModeStatus`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/GameModeStatus/Data/DA_GameModeStatus.json), [`DA_GameModeStatusEntry`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/GameModeStatus/Widgets/Entry/Data/DA_GameModeStatusEntry.json), the map and spatial tracker assets ([`DA_Tracker_Map_ControlZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/Trackers/MapTrackers/Data/DA_Tracker_Map_ControlZone.json), [`DA_ControlZone_SpatialTracker`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/Trackers/SpatialTrackers/Data/DA_ControlZone_SpatialTracker.json)), and the distance thresholds in the EQS tests. The files exist and are listed in section 1.
- **Reward cash values** are not in this folder. Use `Wardogs_Rewards_and_Progression_v2.md`, section 6a.
- **Zone regions** (the polygon data that says which areas of the map count as capturable) are in [`ControlZoneRegions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZoneRegions/Content/ControlZoneRegions.json), not here. See the sibling doc.
- **The 15 HUD widget instances** in the root bundle are listed as entries in [`ControlZone.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone.json). Only the main `W_GameModeStatus` element was resolved to a class in this pass. The other 14 instances were not individually mapped.
- **Alternator weight 0 entries** (Europe Farmland, NorthAmerica SmallFactory, Africa North/East/West, Russia Bazaar/River/Hillside) are read as never selected. The game may use them elsewhere; this was not checked.
  - **See [`docs/CROSS_REFERENCE.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/CROSS_REFERENCE.md)** for the project-wide cross-reference index of where referenced assets are defined.
- **The NorthAmerica Hot Zone height** (85,000 against 50,000) is reported as found and not interpreted.
- The Gym config's Hot Zone sizing is not defined in this folder.

## 10. Config file (round 73)

`DefaultControlZone` has one section, `WDControlZoneGameStateComponent`, with `ScorePerControlZoneTick=1`: one score point per zone tick.
