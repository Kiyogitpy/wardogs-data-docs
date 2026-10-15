---
title: "TeamkillTracking (feature)"
parent: "Game Features"
---

# Wardogs — GameFeatures: TeamkillTracking (v2)
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: `Plugins/GameFeatures/TeamkillTracking/` — 1 JSON file (`Content/TeamkillTracking.json`, 2 exports).*

---

## 1. What This Folder Holds

A single pack that adds the teamkill-tracking component to the game session.

| Item | Value |
|---|---|
| Action | `GameFeatureAction_AddComponents` |
| Host | `WDGameStateSession` |
| Component | `WDTeamkillTrackingComponent` (module `TeamkillTrackingRuntime`) |

---

## 2. How It Is Used

The component runs on the game-state session, so it is available for every session mode that uses that class. The teamkill penalty itself is referred to in the Rewards work (teamkill is a negative reward multiplier), but this pack does not define those values.

---

## 3. Still not pulled / limitations

- **Penalty rules.** How many teamkills trigger what, and what the penalties are, are inside the native component. Not in this export.
- **Scope.** The component is added to the session class; which modes load it is determined by the GFD activation, not in this file.
