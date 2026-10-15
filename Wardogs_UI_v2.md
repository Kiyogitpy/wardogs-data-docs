# Wardogs — UI Data Reference (v2)
*Extracted from cooked game data (`Wardogs/Content/UI`, 586 JSON files holding 774 export blocks: 486 UDataAsset, 188 UObject, 88 UDataTable, 11 curve assets, 1 common input table). Values are as exported; nothing here was checked in-game. Multi-export files were split on their `--- export:` headers before parsing.*

> **Scope note:** this is the UI-layer data: HUD trackers and feeds, map and minimap setup, ping and radial wheels, vendor and inventory grids, tooltips, settings display, frontend scenes, localisation-tag tables, and UI audio. Gameplay numbers (cash, XP, weapon stats) live in other categories. Where a UI asset refers to a gameplay tag or entity, the tag is named but its gameplay value is not included here.

---

## 1. Inventory of the Category

| Top folder | Export blocks | Notes |
|---|---|---|
| `Features/` | 720 | All screens and HUD elements; see section 1b for the breakdown |
| `Data/` | 37 | Shared tables: entities, tagged icons, audio, scenes, interaction, tag-to-text |
| `Tools/` | 9 | Minimap texture definitions (`Tools/WorldCapture`) and editor-only tracker data |
| `Shared/` | 4 | Rich-text image tables |
| `Cursors/`, `Input/`, `Prototype/` | 4 | Software cursor, common input actions, one prototype |

### 1a. Most common asset types

| Type | Count | What it is |
|---|---|---|
| `DataTable` | 88 | Row tables (see section 13) |
| `WDPingActionAsset` | 35 | One per ping-wheel entry |
| `WDUITutorialsContentData` | 26 | LearnToPlay tab content (all under `Frontend/LearnToPlay`) |
| `WDUIContainerGridData` | 16 | Grid size and label per container view |
| `WDUIRadialWheelSlotTypeDataAsset` | 16 | Radial wheel slot definitions |
| `WDUIMaterialTrackerDataAsset` | 15 | Map material-tracker settings (`Map_Optimisation`) |
| `WDPingAction_SendTextMessage` / `WDPingAction_VoxRequest` | 15 / 15 | Ping action behaviours |
| `WDUIButtonPromptsBarData` | 12 | Button prompt bars |
| `WDUIMapTrackerData` | 12 | Basic map tracker settings |
| `WDUITooltipContainerData` | 10 | Container tooltip layouts |
| `WDUILineOfSightRules` / `WDUIWorldDistanceOpacityRules` | 11 / 10 | Shared rule assets used by trackers and markers |
| `WDMinimapTextureData` | 7 | One per world minimap texture |

### 1b. Export blocks by feature folder

| Folder under `Features/` | Blocks | Folder under `Features/` | Blocks |
|---|---|---|---|
| `HUD` | 190 | `Popups` | 11 |
| `Frontend` | 129 | `Scoreboard` | 8 |
| `PingWheel` | 109 | `ContextDrawer`, `DeathRecap` | 6 each |
| `Vendor` | 85 | `DeploymentBoard` | 5 |
| `Tooltips` | 43 | `GameOver` | 4 |
| `Map` | 36 | `PocketWorldRender`, `QuickRestock` | 3 each |
| `Inventory_2_0` | 28 | `AccountBar`, `AdminPanel`, `FactionSelect`, `TVGuided` | 1–2 each |
| `RadialWheel` | 28 | | |
| `Settings` | 21 | | |

---

## 2. Minimap and World Textures

Each `DA_UI_<Map>` asset (`WDMinimapTextureData`) binds a virtual texture to world coordinates. Map files: `Tools/WorldCapture/Textures/<Map>/`.

| Map | Texture | SizeX (px) | WorldUnitsPerPixel | Bounds X (min → max) | Bounds Y (min → max) | UV max |
|---|---|---|---|---|---|---|
| Europe | `T_UI_Europe_VT` | 32,768 | not set | −1,616,000 → 16,000 | −1,616,000 → 16,000 | 1.0 |
| NorthAmerica | `T_UI_NorthAmerica_VT` | 32,768 | not set | −819,200 → 819,200 | −819,200 → 819,200 | 1.0 |
| Russia | `T_UI_Russia_VT` | 32,768 | not set | −1,632,000 → 0 | −2,040,000 → −408,000 | 1.0 |
| Kavkazi | `T_UI_Kavkazi_VT` | 16,384 | 100 | −1,632,000 → 0 | −2,040,000 → −408,000 | 1.0 |
| Gym_Minimal | `T_UI_Gym_Minimal_VT` | 9,803 | 51 | −250,001.7 → 249,998.5 | −245,100.0 → 254,900.0 | 0.598 |
| PCGBuildAutomationTestLevel | `T_UI_PCGBuildAutomationTestLevel_VT` | 4,032 | not set | −100,800 → 100,800 | −100,800 → 100,800 | 0.984 |
| Shooting_Range_4 | `T_UI_Shooting_Range_4_VT` | not set | not set | −100,000 → 100,000 | −100,000 → 100,000 | 0.977 |

Z bounds are present on every map (for example Europe ±164,285.9; Shooting_Range_4 −30,000 → 30,000).

**Derived, not stored:** where `SizeX` and the XY bounds are both present, bounds width ÷ SizeX gives the implied world units per pixel. Europe and Russia give about 49.8, Kavkazi about 99.6 (matching its stored 100), NorthAmerica and PCGBuildAutomationTestLevel exactly 50.0, and Gym_Minimal 51.0 (matching its stored 51). Europe and Russia have no stored `WorldUnitsPerPixel`, so the derived figure is the only one available.

---

## 3. Map and Minimap Trackers

Trackers are registered in `DT_TrackerData_Minimap` (17 rows), `DT_TrackerData_Map` (17 rows, tactical map) and `DT_TrackerData_Spatial` (13 rows, world-space markers). Each row binds a `Trackers.Type.*` tag to a tracker class and a widget (`W_Tracker_Map_*` or `W_Tracker_Spatial_*`).

### 3a. Tracker types on the minimap and tactical map

| Tracker tag | Tracker class | Widget family | Recreate on faction change |
|---|---|---|---|
| `Trackers.Type.Character` | `WDUIPersistentDataTracker` | Player | Yes |
| `Trackers.Type.Vehicle` | `WDUIPersistentDataTracker` | Vehicle | Yes |
| `Trackers.Type.StationaryVehicle` | not captured | StationaryVehicle | Yes |
| `Trackers.Type.Spawn` | `WDUIPersistentDataTracker` | Spawn | Yes |
| `Trackers.Type.SafeZone` | `WDUIPersistentDataTracker` | SafeZone | Yes |
| `Trackers.Type.Vendor` | `WDUIPersistentDataTracker` | Vendor | Yes |
| `Trackers.Type.DeploymentBoard` | `WDUIPersistentDataTracker` | DeploymentBoard | Yes |
| `Trackers.Type.RefuelStation` | `WDUIPersistentDataTracker` | FuelStation | **No** |
| `Trackers.Type.Corpse` | `WDUIStaticTransformTracker` | Corpse | Yes |
| `Trackers.Type.Deployable` | `WDUIPersistentDataTracker` | Deployable (requires `Id.Item`) | Yes |
| `Trackers.Type.SupplyCrate` / `SupplyPallet` | `WDUIPersistentDataTracker` | SupplyCrate / SupplyPallet | Yes |
| `Trackers.Type.AssistanceRequest` | `WDUIPersistentDataTracker` | AssistanceRequest | Yes |
| `Trackers.Type.Ping` | `WDUIPingTracker` | Ping | Yes |
| `Trackers.Type.Ping.Contextual` | `WDUIPingTracker` | Contextual | Yes |
| `Trackers.Type.Ping.Contextual.MarkCoordinates` | `WDUIPingTracker` | Marker | Yes |
| `Trackers.Type.HitMarker` | `WDUIPersistentDataTracker` | HitMarker | Yes |

On the minimap table, four trackers require gameplay tags: `Character`, `Vehicle` and `StationaryVehicle` need their `*.Data` and `*.Transforms` tags (`Vehicle` and `StationaryVehicle` also need `Vehicle`), and `Deployable` needs `Id.Item` and `Trackers.Type.Deployable`. All other rows have no required tags.

### 3b. Per-tracker display settings (map variants)

| Asset | Type | ZOrder | Other notable values |
|---|---|---|---|
| `DA_Tracker_Minimap_Spawn` | WDUIMapTrackerData | 1 | — |
| `DA_Tracker_Minimap_Corpse` | WDUITimedMapTrackerData | 10 | — |
| `DA_Tracker_Minimap_DeploymentBoard` | WDUIMapTrackerData | 20 | Default tracker icon set |
| `DA_Tracker_Minimap_Vendor` | WDUIVendorMapTrackerData | 20 | `VendorTextures` ×2 |
| `DA_Tracker_Minimap_Vehicle` | WDUIVehicleMapTrackerData | 25 | `OccupantsTextFormat`, 4 assistance-request textures |
| `DA_Tracker_Minimap_Ping` | WDUIPingMapTrackerData | 40 | 2 ping colours |
| `DA_Tracker_Minimap_AssistanceRequestPing` | WDUIAssistanceRequestMapTrackerData | 40 | 1 texture, 1 ping colour, 1 tracker exception |
| `DA_Tracker_Minimap_ContextualPing` | WDUIContextualMapTrackerData | 40 | 6 textures and colours |
| `DA_Tracker_Minimap_Player` | WDUIPlayerMapTrackerData | 80 | `DefaultTexture` = `T_UI_FriendlyMarker_Map_Icon`, `SelfOrSquadTexture` = `T_UI_PlayerMarker_Map_Icon`; 9 assistance-request and 10 acknowledged textures |
| `DA_Tracker_Map_Player` (tactical) | WDUIPlayerMapTrackerData | — | `DefaultIconScale` 0.75, `LowHealthColor`, `OverHealHealthColor` |
| `DA_Tracker_Map_HitMarker` | WDUITimedMapTrackerData | 40 | `Duration` 150 (unit not stated in the asset) |

**Material-tracker removal times** (`Features/Map/Map_Optimisation`, 15 assets): `RemovalTime` = **10** on AssistanceRequest, Corpse, Ping and ContextualPing. The others have no removal time. Every one carries a `ZoomScaleCurve`.

### 3c. Spatial (world-space) trackers

| Asset | Type | Key values |
|---|---|---|
| `DA_SpatialTrackers` | WDUISpatialTrackersData | `FocusPointDistanceScoreMultiplier` 0.6; 6 `WorldDistanceScoreMultipliers` |
| `DA_Tracker_Spatial_AssistanceRequest` | WDUIAssistanceRequestSpatialTrackerData | `StalkMaxYSize` 300, `StalkSizeChangeRate` 1500, `PingScaleMaxDistance` 10, `Duration` 20, `ZOrder` 3 |
| `DA_Tracker_Spatial_ContextualPing` | WDUIContextualPingSpatialTrackerData | `StalkMaxYSize` 300, `StalkSizeChangeRate` 1500, `PingScaleMaxDistance` 10 |
| `DA_Tracker_Spatial_Ping` | WDUIPingSpatialTrackerData | `StalkMinYSize` 0, `StalkMaxYSize` 0, `StalkSizeChangeRate` 1500, `PingScaleMaxDistance` 10 |
| `DA_Tracker_Spatial_Player` | WDUIPlayerSpatialTrackerData | `bUseOcclusionFade` True, `OcclusionFadeDuration` 0.5 |
| `DA_Tracker_Spatial_Vehicle` | WDUIVehicleSpatialTrackerData | `bHideIfDrivenByLocalPlayer` True, `bUseOcclusionFade` True, fade 0.5 |
| `DA_Tracker_Spatial_Vehicle_LockOn` | WDUISpatialTrackerData | `bUseOcclusionFade` True, fade 0.5 |
| `DA_Tracker_Spatial_ActiveZone` | WDUIActiveZoneData | `ValueSmoothingSpeed` 0.5 |
| `DA_Tracker_Spatial_Interactable_*` (2) | WDUIInteractableActorData | Second variant is screen-clamped |

Spatial `RuleSets` and `DistanceRulesets` reference shared rule assets (section 9). The meaning of the `Stalk*` fields is inferred from their names and was not confirmed.

---

## 4. Ping Wheel

The ping wheel has 35 entries in five categories. Each entry is one `DT_PingActions_*` row that points to one `WDPingActionAsset`.

| Category table | Rows | Category tag | Preferred page |
|---|---|---|---|
| `DT_PingActions_Emote` | 10 | not captured | not captured |
| `DT_PingActions_Orders` | 5 | `UI.Features.PingWheel.Category.Squad` | 2 |
| `DT_PingActions_Request` | 10 | `UI.Features.PingWheel.Category.Requests` | 1 |
| `DT_PingActions_Social` | 5 | not captured | not captured |
| `DT_PingActions_Squad` | 5 | not captured | not captured |

### 4a. Orders (Squad category, page 2)

| Action | Slot | Icon |
|---|---|---|
| Fortify | 1 | `T_UI_Icon_PingWheel_fortify` |
| Defend | 2 | `T_UI_Icon_PingWheel_Defend_64x64` |
| Attack | 3 | `T_UI_Icon_PingWheel_Attack_64x64` |
| FallBack | 4 | `T_UI_Icon_PingWheel_FallBack_64x64` |
| Regroup | 5 | `T_UI_Icon_PingWheel_Regroup_64x64` |

### 4b. Requests (page 1) and their gating

| Action | Required player-state tag | Blocked player-state tag |
|---|---|---|
| Backup | — | Driver |
| Ammo | — | Driver |
| Healing | — | Driver |
| Supplies | — | — |
| Pickup | — | ActivePassenger, and others |
| Dropoff | ActivePassenger, Gunner, and others | not captured |
| Repair | Driver | — |
| Refueling | Driver | — |
| GetIn | Driver | — |
| GetOut | Driver | — |

`bRequestPlayerMapCoordinates` is True on Backup, Fuel, Healing, Pickup, Repair and Supplies. It is not set on Dropoff, GetIn, GetOut or Ammo, as far as the digest shows.

### 4c. Action asset behaviours

| Asset class | Count | Fields that vary |
|---|---|---|
| `WDPingActionAsset` | 35 | `Text`, `Icon`, `Actions` (values 1–4), `NonTriggerableDescriptions` (1–2 items), `LockedDescription` (21 of 35), `bIsWorkInProgress`, `bRequestPlayerMapCoordinates` |
| `WDPingAction_SendTextMessage` | 15 | `ChannelType`, `PingActionChatLocText` |
| `WDPingAction_VoxRequest` | 15 | `GameplayCueTag` |
| `WDPingAction_Emote` | 10 | Emote reference |
| `WDPingAction_CheckSquadStatus` | 10 | `bCheckIsSquadLeader` True on 5 |
| `WDPingAction_ShowSpatialMarker` | 6 | `SpatialMarkerTag` |
| `WDPingAction_AssistanceRequest_*` | 10 | One per request type (Ammo, Backup, Dropoff, Refueling, GetIn, GetOut, Healing, Pickup, Repair, Supplies) |

Emote icons include Assault, Move_Up, Point, Surrender_Drop, Halt, Middle_Finger, Paper, Rock, Scissors and Shh. Social icons are the Nice, No, Sorry, Thanks and Yes set.

---

## 5. Radial Wheels

| Wheel tag | Display name / title | Close action | Slot table |
|---|---|---|---|
| `UI.RadialWheel.Equipment` | "TAC-VEST" | `UI.Action.Feature.RadialWheel.Equipment.ToggleScene` | `DT_RadialWheelSlotType_EquipmentData` (7 rows) |
| `UI.RadialWheel.VoiceChat` | "SELECT VOICE CHANNEL" (description: "Current - {TalkingChannel}") | `UI.Action.Feature.RadialWheel.VoiceChat.ToggleScene` | `DT_RadialWheelSlotType_VoiceChatData` (2 rows) |

`DT_RadialWheelSlotType_Vehicles` has 9 rows. Slot-type assets cover empty and locked states: `EmptySlotTitleText`, `EmptySlotDescriptionText`, `LockedSlotTitleText`, `LockedSlotDescriptionText`, `EmptyTextureScale`, `LockedTextureScale`, and `QuantityTextAngleOverride`. Voice-channel slot assets also hold `ChannelType`, `Action`, `Icon` and `IconScale`.

---

## 6. Feeds and Notifications

### 6a. Reward feed (`DA_RewardFeed`, `DT_RewardFeedActions`, 52 rows)

| Setting | Value |
|---|---|
| `InitialExpiryTime` (feed) | 6 |
| `XPTextFormat` (entry) | `{XPValue}XP` |
| Action table | 52 rows, each with `DisplayText`, `bIsTip` and an optional `AudioEventTag` |

Sample rows (tag → text):

| Tag (short) | Feed text | Audio tag |
|---|---|---|
| `MatchScore.KillScore` | Enemy Player Killed | — |
| `MatchScore.DownedScore` | Enemy Player Downed | — |
| `MatchScore.HealedScore` | Friendly Player Healed | `Audio.Event.UX.Cash.HealedScore` |
| `MatchScore.RevivedScore` | Friendly Player Revived | `Audio.Event.UX.Cash.RevivedScore` |
| `MatchScore.VehicleKillScore` | Enemy Vehicle Destroyed | `Audio.Event.UX.Cash.DestroyedVehicle` |
| `MatchScore.DamageAssist.Player` | Enemy Kill Assist | `Audio.Event.UX.Combat.KillAssist` |
| `MatchScore.SupplyCrateKillScore` | Destroyed Enemy Supply Crate | `Audio.Event.UX.Cash.DestroyedVehicle` |
| `MatchScore.TowerCaptured` | Tower Captured | `Audio.Event.UX.Cash.BuiltScore` |
| `MatchScore.ObjectiveScore.SpawnVehicle.ControlZoneEntered` | Spawn Vehicle Delivered | `Audio.Event.UX.Cash.DeliveredSpawnVehicle` |
| `MatchScore.DropOffPassengerSurvived` | Passenger Survived | `Audio.Event.UX.Cash.PassengerSurvived` |
| `MatchScore.SchematicBuiltScore.FinalBuilder` | Finished Building | `Audio.Event.UX.Cash.BuiltScore` |

The remaining rows cover friendly-fire and destroyed-friendly variants, schematic and FOB build steps, magnet zone states, deployables, supply crates and transport assists.

### 6b. Challenges feed (`DT_ChallengesFeedActions`, 68 rows)

Rows are keyed `Challenges.Rewards.*`. Some carry `ConditionalExpressions` on context tags. For example, `Challenges.Rewards.PlayerKill` shows **"No Value Kill"** when the context is `Challenges.Context.RessedByEnemy`, which is the feed-side counterpart of the ressed-by-enemy penalty. `Challenges.Rewards.PlayerKill.CrewAssist` shows "Kill Assist" and `.LogisticAssist` shows "Deployed Player Assist".

### 6c. Tipping

`DT_TippingReward` (4 rows, reward-feed row type). `DA_TippingData` `TipPromptDuration` = 8.

### 6d. Killfeed (`DA_Killfeed`, `DA_KillfeedEntry`)

| Setting | Value |
|---|---|
| `MaximumEntries` | 5 |
| `EntryDuration` | 10 (unit not stated; likely seconds) |
| Preloaded kill-context icons | 8: Headshot, Falling, Default, RoadKill, Penetration, Ricochet, WeaponMelee, RangedWeaponMelee |
| `DistanceTextFormat` | `[{Distance} {Unit}]` |
| `DisconnectedPlayerText` | "Disconnected Player" |

### 6e. Event feed (`DT_EventFeedTypes`, 34 rows; `DA_EventFeedEntry`)

| Setting | Value |
|---|---|
| Entry `EntryDuration` | 5 |
| Each type has | `DisplayTextSelf`, `DisplayTextOther`, `MaxDistanceForTeamEvents` |
| Acknowledge icon | `T_UI_Icon_PingWheel_Affirmative_64x64` |

Examples: `Type.Acknowledgement` ("{RequestPlayerName} acknowledged <Highlight>{PlayerName}</>'s request"), `Type.Safezone.Exit` ("{RequestPlayerName} have left the Safe Zone"), `Type.Request.Cancelled`.

### 6f. Feedback and chat

| Asset | Key values |
|---|---|
| `DA_HUDFeedback` | `EntryDuration` 4.5 |
| `DA_Chatbox` | `MaximumCachedMessages` 50, `DisplayDuration` 10, `MaxCharactersPerMessage` 64, mention prefix `@`, profanity filter `DA_ProfanityFilter` |
| Chat channel tags | Player name, mention-me and mention-other links, coordinate link |

---

## 7. HUD Core Elements

| Asset | Type | Key values |
|---|---|---|
| `DA_Crosshair` | WDUICrosshairData | `Opacity` 0.6, `HairLength` 7.5, `Gap` 0, `SpreadMultiplier` 600, `BuildableCheckRadius` 310, `bShowDot` True, `RevealGraceTime` 0.4, `RevealAnimPlayRate` 1.2, `FallbackCrosshairProjectionDistance` 1000. Hidden during 14 action tags (Sprint, TacSprint, Ladder, Climbing, Mantling, Vaulting, Revive, MeleeBash, Reload, ChamberRound, Swimming, Parachuting, Inspect, Prone.Crawl) and 3 gameplay tags (Vitality.Critical, Vitality.Dead, Vehicle.Role.ActivePassenger) |
| `DA_Compass` | WDUICompassData | 8 cardinal/intercardinal labels at 45° steps (N = 0, E = 90, S = 180, W = 270); `IconSize` 18×18; `FadeStart` 0.4; `bCullPingsAtEdgeOfCompass` True |
| `DA_FadeOut` | WDUIFadeOutData | `BlackoutTransitionDurationOut` 3; "Respawning in {Time}..." |
| `DA_HUDQuickSlots` | WDUIHUDQuickSlotsData | `TimeUntilFadeStarts` 4 |
| `DA_HUDPrompts` | WDUIHUDPromptsData | `ProneBlockedDisplayTime` 1.2; `bEnableTraversalPrompt` False |
| `DA_HUDFalling` | WDUIHUDFallingData | `MinimumGaugeActivationHeight` 5; `bShowGaugeWhileFallingWithoutParachute` False |
| `DA_DeathState` | WDUIDeathStateData | `TimeBetweenDistanceChecks` 1; `MaxBlackoutOpacity` 1; `MaximumDistanceToConsiderAsNearby` 100 |
| `DA_EquippedItem` | WDUIEquippedItemData | Default magazine, bullet and chamber textures; `EquippedItemNameTextFormat` `{ItemDisplayName} // {ResourceDisplayName} // SN ...` |
| `DA_ScopeReticle` | WDUIScopeReticleData | `DeadZoneSize` 0, `DampenZoneSize` 0 (15 reticle types in `DT_ScopeReticleTypes`) |
| `DA_WeightDisplay` | WDUIWeightDisplayData | `HeaviestWeightBuffer` 15 |
| `DA_VehicleFuelHealth` | WDUIVehicleFuelHealthData | `LowFuelThreshold` 0.2 |
| `DA_Passengers` | WDUIPassengersData | "PASSENGERS [{Occupants}/{Capacity}]"; `PassengerCollapseThreshold` 13 |
| `DA_KillfeedEntry` | WDUIKillfeedEntryData | See 6d |

Vehicle HUD assets (`WDUIVehicleStateData` ×2, `WDUIVehicleWeaponAmmoData` ×2, `WDUIVehicleReloadingMinigameData`, `WDUIVehicleFlaresData`, `WDUIVehicleThreatIndicatorData`, and others) hold icon sets, colour thresholds and a reloading minigame that uses quadrant-based inputs. Their numeric detail was not extracted (section 14).

---

## 8. Vendor, Inventory and Container Grids

### 8a. Container grid sizes (`WDUIContainerGridData`, 16 assets)

| Asset | Min W×H | Max W×H | Notes |
|---|---|---|---|
| `DA_ContainerGrid_Inventory_Slot` | 1×1 | 1×1 | Single-slot equipment |
| `DA_ContainerGrid_Inventory_Slot_Weapon` | 1×1 | 1×1 | |
| `DA_ContainerGrid_Inventory_Slot_Vest` | 1×1 | 1×1 | |
| `DA_ContainerGrid_Inventory_Slot_Attachment` | 1×1 | 1×1 | |
| `DA_ContainerGrid_Vendor_Backpack` | 9×2 | 9×2 | Label "Backpack"; fixed-size grid |
| `DA_ContainerGrid_Vendor_Slot` | 1×1 | 1×2 | Label "Backpack" |
| `DA_ContainerGrid_Vendor_Slot_Weapon` | 1×1 | 1×2 | Label "Backpack" |
| `DA_ContainerGrid_Vendor_Slot_Attachment` | 1×1 | 1×1 | |

Subslot grids (Backpack, Storage, Vest, Vault) and the vehicle-inventory grid carry labels and `bUseItemAsSlotName` settings but no size bounds.

### 8b. Vendor panels and types

`DT_VendorTypes` has 3 rows:

| Vendor type | Default panel | Swap to default on close | Panel buttons |
|---|---|---|---|
| `Vendor.Type.Equipment` | `Vendor.Panel.Overview` | True | Overview, and others |
| `Vendor.Type.Vehicle` | — | False | Land (50×50 minimum size), and others |
| `Vendor.Type.Garage` | `Vendor.Panel.Garage.Overview` | True | Overview, and others |

Panel data assets: `WDUIVendorPanelData_Utility` (2), `_Gear`, `_Weapons`, `_Garage`, `_GarageOverview`, `_GarageSupplyCrate`, `_Overview`, `_Vehicles`. Utility panels set `bTryPurchaseEvenIfDesiredSlotIsUnavailable` True and `bCheckForSubslotSupportWhenFilteringPurchases` True, and show "CAP. {Amount}/{Capacity}".

### 8c. Purchasable item cards

Purchasable card assets (`WDUIPurchasableItemCardData_Vendor`, 4) share these texts:

| Text key | Value |
|---|---|
| `MultipleItemsPriceTooltipFormat` | `{Value} per Item` |
| `UnlockLevelTextFormat` | `{Role} Lvl {Level}` (vehicles and some gear); "No storage space available" (the generic purchasable card) |
| `InsufficientFundsWarning` | "Not Enough Cash" |
| `ItemAmountType` | `EWDUIItemAmountType::InInventory` |

Vehicle vendor (`DA_VehicleVendor`): `VehicleTypeFormat` `{Subcategory} Vehicle`, `bFlushInputOnEnter` True.

---

## 9. Shared Rule Assets

Rule assets are reused across trackers, markers and HUD elements. Counts are the number of assets.

| Rule type | Count | Typical fields |
|---|---|---|
| `WDUILineOfSightRules` | 11 | `SquaredRange` (11), `TraceChannel` (4), `Range` (3), `bUseAdditionalCharacterTraces`, `BlockedOpacity`, `bRequireRenderedComponent` |
| `WDUIWorldDistanceOpacityRules` | 10 | `MaximumVisibleDistance`, `MinimumVisibleDistance`, `FalloffRangeMinimum`/`Maximum`, `MaxOpacity`, `Targets` |
| `WDUIScreenClampingRules` | 9 | `ClampingAsPixels` (5), `ClampingAsPercentage` (4), `bClampByScreenPercentage` |
| `WDUIWorldDistanceScaleRules` | 7 | `DistanceForScalingEnd`, `StartScale`, `EndScale` |
| `WDUIScreenDistanceOpacityRules` | 6 | `MaximumVisibleDistance`, `FalloffRangeMaximum`, `OpacityRange`, `bInvertOpacity` |
| `WDUILocationOffsetRules` | 4 | `Offset`, `bDynamicOffset`, `DynamicOffsetDistanceCurve`, `AttachBone` |
| `WDUIScreenLocationOffsetRules` | 4 | `bOffsetAfterScreenClamping`, `bOffsetByScreenPercentage`, `OffsetAsPercentage` |
| `WDUIContextTextRules` / `WDUINameTextRules` / `WDUIDistanceTextRules` | 4 each (contexts 4, names 4, distance 4) | Text state and rules |
| `WDUIOpacityMultiplierRule` / `WDUIScaleMultiplierRule` | 2 / 1 | `Multiplier`, `Targets` |
| `WDUIFocusFadeInOpacityRules` | 3 | `Targets` |

Trackers reference these by `RuleSets` and `DistanceRulesets` (arrays of 1–7 entries). The exact evaluation order between rules is not known from the data.

---

## 10. Settings, Input and Cursor

| Asset | Key values |
|---|---|
| `DA_SoftwareCursor` (`WDUISoftwareCursorData`) | `FallbackCursorSize` 18×21.33; `DeadZoneRadius` 0.15; `AnalogStickResponseCurve` = `C_CursorAnalogStickResponseCurve`; `CursorInfoMap` |
| `DA_DeadZoneAnalogue` | Test readout text "X: {XValue}%, Y: {YValue}%" for both sticks |
| `DA_DeadZoneTrigger` | "Trigger: {Percentage}%" for left and right triggers |
| `DT_Settings_DisplayData` (15 rows) | Includes gamepad move-stick dead-zone presets: `Preset`, `Centre`, `Axial`, `MaxInput` |
| `DT_SettingTypeUIData` (12 rows) | Display widget types: Numeric, Keybind, InputField, Rotator, Switch, Dropdown, Hyperlink, Button, JoystickAxis, JoystickAction, Status, RetryCommunication |
| `WDUISettingValueData` (3) | `bCanBeNudged` (1), `bCanBeContinuouslyNudged` (3), `NudgeCurve` (3) |
| `WDUISettingsPanelData` (6), `WDUISettingsData` (1), `WDUIInitialSettingsData` (1) | Settings panel pages, categories and first-run settings |

Common UI input actions are in `UCommonGenericInputActionDataTable` (1 table) and `DT_UIInputActionData` (1 row).

---

## 11. Frontend Scenes, Mastery and Tutorials

### 11a. Scene tables

| Table | Rows | Example scenes |
|---|---|---|
| `DT_SceneData_Frontend` | 28 | `Logo`, `Photosensitivity`, `Start`, `InitialSettings`, `Home`, `Career`, `Customize` |
| `DT_SceneData_Match` | 24 | In-match scenes |
| `DT_SceneData_Shared` | 4 | Shared scenes |

Scene fields: `InputMode` (`EWDInputMode::UI`), `bResetFocusOnEnter` (True on the sampled rows), `bShouldBlockBack` (True on `Logo`, `Photosensitivity`, `Start`, `InitialSettings`; False on `Home`, `Career`, `Customize`), `bIsFocusable`.

### 11b. Role skill tree (`DT_CharacterSkillNodes_Data`, 131 rows)

| Role | Nodes |
|---|---|
| Infantry | 29 |
| Recon | 28 |
| Support | 27 |
| Medic | 23 |
| Driver | 12 |
| Pilot | 12 |

Each node has a `FriendlyName` (for example "Medkits have more uses"), a `Description` and a `NodeIcon`. Sample Medic nodes: `BuffApplicationTime`, `BuffDuration.Self`, `ChargeTime.Defibrillator`, `HealthierRevive`, `HealTime.Self`, `IncreaseBleedTime`, `MedicBag`, `ReviveSpeed.Standard`. Driver and Pilot nodes split by vehicle class (Ground Vehicles, Air Vehicles, Mounted MG). Scene titles use `{ROLENAME} MASTERY` and `{PLATFORMNAME} PLATFORM`.

### 11c. LearnToPlay tutorials

All 26 `WDUITutorialsContentData` assets sit under `Frontend/LearnToPlay/Data/ContentSceneData/TabData/`. Tab folders include `Introduction`, `UsingEquipment`, `Vehicles` and `TravelToObjective`. Each carries `MediaPlayer` and `ContentTabData` references.

### 11d. Loading screen tips

`DT_LoadingScreenTips` has **110 rows**. Tag prefixes: `Tip.Economy.*`, `Tip.Items.*` (including weapon examples), `Tip.ControlZone.*`.

---

## 12. Entities, Icons and Localisation Tags

| Table | Rows | Role |
|---|---|---|
| `DT_EntityData_UI_Items` | 295 | UI entity data per `Id.Item.*` (e.g. `Id.Item.Fists`, `Id.Item.Bandage`, `Id.Item.SuperBandage`) |
| `DT_EntityData_UI_Garage` | 2 | Garage entities |
| `DT_EntityData_UI_VehicleAmmo` | 5 | Vehicle ammo entities |
| `DT_EntityData_UI_Misc` | 1 | Misc entity |
| `DT_InteractionContextData` | 86 | Interaction prompt text and condition rules, e.g. `Interaction.Context.Container.Loot` → "Container" |
| `DT_InteractionContexts` | 70 | Second interaction table (`BHEntityData_UI` row type) |
| `DT_TaggedIcons` | 63 | Inventory slot and general tag icons |
| `DT_Calibers_TaggedIcons` | 33 | Calibre icons |
| `DT_CaliberModifiers_TaggedIcons` | 6 | Calibre modifier icons |
| `DT_DamageTypes_TaggedIcons` | 3 | Fall, Impact, Explosive |
| `DT_LevelIcons` | 7 | Role level icons: Wardog, Driver, Infantry, and others |
| `DT_TooltipData` | 33 | Tooltip widget and view-model mapping |

**Gameplay-tag-to-text tables** (`Data/GameplayTagsToText`, 15 tables, 319 rows total): Categories 106, InventorySlots 37, SceneNames 36, Calibers 28, Archetypes 16, Ammunition 14, Roles 13, ServerTags 23, Damage 9, Tooltips 10, Components 7, EventLog 6, Tutorials 5, PlayerStates 5, Prompts 4.

---

## 13. Data Tables (all 88)

Grouped by row type. Row counts from the export; zero-row tables are listed on their own because they may be placeholders.

| Row type (RowStruct) | Tables | Total rows | Covered in |
|---|---|---|---|
| `BHEntityData_UI` | 5 | 373 | Section 12 |
| `WDUIGameplayTagToTextTableRow` | 15 | 319 | Section 12 |
| `WDMetaTreeNodeData_UI` | 1 | 131 | Section 11b |
| `WDRewardFeedActionDataTableRow` | 3 | 124 | Section 6 |
| `WDLoadingScreenTips` | 1 | 110 | Section 11d |
| `WDUITaggedIconRow` | 5 | 107 | Section 12 |
| `WDUIInteractionContextDataTableRow` | 1 | 86 | Section 12 |
| `WDSceneDataTableRow` | 3 | 56 | Section 11a |
| `WDUITrackerDataTableRow` | 4 | 51 | Section 3 |
| `RichImageRow` | 5 | 35 | Not detailed |
| `WDUIPingAction` | 5 | 35 | Section 4 |
| `WDEventFeedActionDataTableRow` | 1 | 34 | Section 6e |
| `WDUITooltipDataTableRow` | 1 | 33 | Section 12 |
| `WDUIActionSoundTableRow` | 1 | 20 | Section 13 notes |
| `WDUIRadialWheelSlotTypeTableRow` | 3 | 18 | Section 5 |
| `WDUITaggedWidgetParamsRow` | 2 | 16 | Not detailed |
| `WDUIPopupTypeDataTableRow` | 2 | 16 | Not detailed |
| `WDUIMaterialTrackerDataTableRow` | 1 | 15 | Section 13 notes |
| `RichTextStyleRow` | 10 | 15 | Not detailed |
| `WDUIScopeReticleType` | 1 | 15 | Section 7 |
| `WDUIUserSettingDisplayDataTableRow` | 1 | 15 | Section 10 |
| `WDUIDeploymentBoardRejectionTableRow` | 1 | 10 | Not detailed |
| `WDUILevelTableRow` | 1 | 7 | Section 12 |
| `WDUIScoreboardStatTableRow` | 1 | 5 | Section 13 notes |
| `WDUIInteractionContextStateDataTableRow` | 1 | 4 | Not detailed |
| `WDPlacementUiTextRecord` | 1 | 3 | Not detailed |
| `WDUIVendorType` | 1 | 3 | Section 8b |
| `WDUIInteractableComponentStateDataTableRow` | 1 | 2 | Not detailed |
| `WDDevMenuMapsDataTableRow` | 1 | 2 | Not detailed |
| `WDUIIndicatorTableRow` | 1 | 2 | Not detailed |
| `WDUIRadialWheelTableRow` | 1 | 2 | Section 5 |
| `WDUIInputActionDataTableRow` | 1 | 1 | Section 10 |
| `SDUINotificationDataRow` | 1 | 1 | Not detailed |
| Zero-row tables (listed below) | 5 | 0 | — |

Counts come from a grouping of all 88 `DataTable` exports by RowStruct. Row types that appear in more than one table are listed once with the combined count.

**Zero-row tables:** `DT_PlayerIdentities`, `DT_ExperienceServerBrowserTags`, `DT_OnlineRegions`, `DT_ServerBrowserMapTexture`, `DT_PopupButtons`. These may be placeholders or unused in this build.

Notable non-trivial tables:

- `DT_UIAudioData` (20 rows, `WDUIActionSoundTableRow`): maps UI tags to MSS sound assets. Several rows have an **empty** `AssetPathName`, so the sound is unset: `UI.Audio.Vendor.Open`, `UI.Audio.Vendor.Close`, `UI.Audio.RewardFeed.CashComboAdd`, `UI.Audio.RewardFeed.CashComboBank`.
- `DT_MaterialTrackerSettingsData` (15 rows): material-tracker settings, paired with section 3b.
- `DT_PopupTypes_Features` (13) and `DT_PopupTypes_Generic` (3): popup type definitions.
- `DT_ScoreboardStats_Default` (5): default scoreboard columns.
- `DT_LootedComponentTypes` (4): loot-container component widget params.

---

## 14. Curves and Textures

| Asset | Type | Use (from name) |
|---|---|---|
| `C_CursorAnalogStickResponseCurve` | CurveFloat | Cursor analogue-stick response; keys run from (0, ~0) to (1, 1), cubic auto tangents |
| `C_DynamicLocationOffsetPlayerTracker` / `C_DynamicLocationOffsetVehicleTracker` | CurveFloat | Dynamic location offset for tracker markers |
| `CC_SpatialPingTimeline` / `CC_SpatialPingDangerTimeline` | CurveLinearColor | Spatial ping colour timeline (normal and danger) |
| `CC_AlphaTime` / `CC_LinesTimeline` / `CC_PulseTimeline` | CurveLinearColor | HUD animation timelines |
| `CA_SpatialPingTimeline` / `CA_SpatialPingDangerTimeline` / `CA_ThrobberTime` | CurveLinearColorAtlas | Gradient atlases for the same timelines |

Curve key values were not extracted, so the shapes are not documented here.

---

## 15. How the Pieces Connect

- A **tracker** is defined by a row in one of the three tracker tables (section 3). It picks a widget and a data asset. The data asset chooses textures, colours and `ZOrder`, and points to **rule assets** (section 9) that decide opacity, scale, clamping and visibility by distance.
- A **ping** starts from a ping-wheel row (section 4), which gates it by player state. The action asset then decides what is sent: text to a channel, a voice request, a spatial marker or a squad-status check. Pings that place a map coordinate set `bRequestPlayerMapCoordinates`.
- **Feeds** (section 6) match an event tag to display text and an audio tag. Reward-feed rows are keyed by the same `Meta.Progression.Resources.*` tags that the cash and XP tables use.
- **Vendor and inventory** grids (section 8) combine a container-grid size, a layout, an item card and a panel type from `DT_VendorTypes`.

---

## 16. Still not pulled / limitations

- **Curve keyframes** (section 14) and **`WDUIMaterialTrackerDataAsset` ZoomScaleCurve** values were not extracted. Only the names are listed.
- **Field meanings not confirmed:** `ZOrder` direction (higher drawn on top is inferred from values), `RemovalTime` and `Duration` units (seconds assumed for the 10 and 20 values, but not stated), `EntryDuration` units, the `Stalk*` spatial fields, `Actions=[N]` on ping assets, `bIsWorkInProgress` (not shown on every asset), and the `RuleSets` evaluation order.
- **Partially extracted:** the tactical map's `SmallestViewSize` and `LerpZoomPresetTolerance`; the full list of `Actions` for each ping action; the `Challenges.Rewards.*` condition tags; the vehicle-HUD assets in section 7.
- **Not covered in detail:** `DT_RichText_Style_*` and `DT_RichImg_*` styling rows (only counted); `DT_CustomEmojis` and tooltip emojis (only counted); `DA_Settings*` category contents; `WDUIMockInvestmentCardData` and other mock or prototype assets; loading-screen tip text.
- **Multi-export files:** 60 files contain more than one export block. They are parsed correctly by splitting on the `--- export:` header, but sub-objects such as `WDUIViewModelExtension_HideReasons_0` appear in the same file and were counted separately.
- Localised strings are taken from `SourceString` (the English source text). Localised builds may differ.
- Nothing in this document was verified against live gameplay or the running UI.

---

*Source directory: `Wardogs/Content/UI`. Parsing scripts are in the session scratchpad and were not written into the dump.*
