---
title: "WDCore (feature)"
redirect_from: ["/Wardogs_GameFeatures_WDCore_v2.html", "/Wardogs_GameFeatures_WDCore_v2"]
parent: "Engine & Tooling Data"
description: "What This Folder Holds, Components, Pawn Data Scan, Animation Set"
---

# Wardogs — GameFeatures: WDCore
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: `Plugins/GameFeatures/WDCore/` — 3 JSON files.*

---

## 1. What This Folder Holds

The core player-character pack. It sets the player pawn data for the mover character, adds the aim-assist target manager to the game session, and holds the character's animation set.

| File | Type | Role |
|---|---|---|
| `Content/WDCore.json` | GameFeatureData + component action | Adds the aim-assist manager, scans pawn data |
| `Content/Character/WDCore_PlayerData.json` | `WDPawnData` | Player pawn: `B_WDCore_MoverPlayerCharacter_C` |
| `Content/Character/AnimSet_MoverCharacter.json` | `BHAnimationSet` | Animation set for the mover character |

---

## 2. Components

| Host | Component |
|---|---|
| `WDGameSession` | `B_WDAimAssistTargetManager` (in `Inputs/AimAssist`) |

---

## 3. Pawn Data Scan

The pack scans `BH.PawnData` (base `BHPawnData`) in `/WDCore/Character`. The only pawn data in the folder is `WDCore_PlayerData`.

---

## 4. Animation Set (`AnimSet_MoverCharacter`)

Six animation tags, each mapped to a base asset with first-person and third-person variants:

| Tag | Use (from name) |
|---|---|
| `Animation.Asset.Character.Revive` | Reviving a teammate |
| `Animation.Asset.Character.Drop` | Dropping an item |
| `Animation.Asset.Character.PickUp` | Picking up an item |
| `Animation.Asset.Character.DoorInteraction` | Opening a door |
| `Animation.Asset.Character.NPCIdle` | Idle for NPC-style characters |
| `Animation.Asset.Character.DoorBreach` | Breaching a door |

The asset paths for each animation are in the export but are not repeated here.

---

## 5. Still not pulled / limitations

- **Animation asset paths.** The per-tag asset and montage references are in the export but not expanded in this pass.
- **Pawn class.** `B_WDCore_MoverPlayerCharacter_C` is a Blueprint; its values are not in this folder.
- **Aim-assist manager.** The target manager's values are in its Blueprint and in the BHAimAssist plugin doc.

## 6. Other small plugin descriptors (round 73)

Eight further `GameFeatureData` descriptors are one-purpose plugins. Values are as exported.

| Descriptor | What it does |
|---|---|
| `BHMotionWarping` | Adds `BHMotionWarpingComponent` to `WDPlayerStateSession`, client and server |
| `CharacterCustomiser` | One `AddWorldPartitionContent` action, data layer `EDL_CharacterCustomiser` |
| `CHRM_001` | The charm plugin: one `AddWorldPartitionContent` action, data layer `EDL_CHRM_001` |
| `DamageExporter` | No actions; scans `/DamageExporter/Data` for `BH.Item` (`BHInventoryItemDefinition`), cook rule Unknown. A developer export tool |
| `WDClientDebugFeature` | Adds `WDClientDebugComponent` to `WDPlayerController`, client and server. Developer tool |
| `DispatchMetricsGame` | Adds `WDDispatchMetricsComponent` to `WDGameStateSession`, server only |
| `RegistryExporter` | Empty descriptor. A developer export tool |
| `ReportTracking` | Adds `WDReportTrackingComponent` to `WDGameStateSession`, server only |
