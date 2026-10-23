---
title: "WDCharacterComponents (feature)"
redirect_from: ["/Wardogs_GameFeatures_WDCharacterComponents_v2.html", "/Wardogs_GameFeatures_WDCharacterComponents_v2"]
parent: "Player & Movement"
description: "What This Folder Holds, Components Added"
---

# Wardogs — GameFeatures: WDCharacterComponents
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/GameFeatures/WDCharacterComponents/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/WDCharacterComponents) — 1 JSON file ([`Content/WDCharacterComponents.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WDCharacterComponents/Content/WDCharacterComponents.json), 2 exports).*

---

## 1. What This Folder Holds

A single component pack that gives the character and player classes their supporting components: reference pose, suppression, death-state effects, movement effects, critical-event tracking, and ping.

---

## 2. Components Added

| Host actor | Component | Role (from name) |
|---|---|---|
| `WDMoverCharacter` | `B_CharacterReferencePoseComponent` | Reference pose for the character |
| `WDPlayerController` | `B_CharacterSuppressionComponent` | Suppression effects |
| `WDPlayerController` | `B_CharacterDeathStateEffectComponent` | Death-state effects |
| `WDPlayerStateSession` | `B_CharacterMovementEffectsComponent` | Movement effects |
| `WDPlayerController` | `WDCriticalEventTrackerComponent` | Tracks critical events |
| `WDPlayerStateSession` | `WDPingComponent` | Ping |

Two components are on the controller (suppression, death-state) and one on the player-state session (movement effects, ping). The critical-event tracker is on the controller. Its link to the critical camera in the AlternativeCriticalCamera pack is inferred from names.

---

## 3. Still not pulled / limitations

- **Component settings.** Values for the Blueprint components (suppression strength, death-effect timing, movement-effect parameters) are not in this folder.
- **Critical tracker.** `WDCriticalEventTrackerComponent` is a native class; its event rules are not in this export.
- **Ping.** Native `WDPingComponent`; no values exported.
