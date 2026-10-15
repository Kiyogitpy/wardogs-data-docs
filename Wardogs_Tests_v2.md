---
title: "Tests"
parent: "Content"
---

# Wardogs: Tests Data Reference (v2)
*Extracted from cooked game data ([`Wardogs/Content/Tests`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Tests), 2 files). These are automated load-test profiles, not gameplay data.*

> **Scope:** the load-test (bot) setup: how many clients to launch per server profile, and what each automated client does. These are the test profiles the Random Scatter orchestrator uses.

---

## 1. File Map

| File | Row struct | Rows |
|---|---|---|
| LoadTests/Data/DT_ServerTestingProfiles.json | WDAutomatedTestServerProfile | 11 |
| LoadTests/Orchestrators/RandomScatter/Data/DT_ClientTestingProfiles.json | WDAutomatedTestClientProfile | 4 |

---

## 2. Server Profiles ([`DT_ServerTestingProfiles`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Tests/LoadTests/Data/DT_ServerTestingProfiles.json))

Each row sets how many automated clients join a test server, and which orchestrator blueprint runs the test.

| Profile | Total clients | Clients opt in | Orchestrator | Custom player controller |
|---|---|---|---|---|
| Default | 100 | yes | B_Default | default |
| SoloTest | 1 | yes | B_SoloTest | default |
| Default10Players | 10 | yes | B_Default10Players | default |
| 100Players | 100 | yes | B_100Players | default |
| 100GroundVehicles | 100 | yes | B_100GroundVehicles | default |
| 100TrackedVehicles | 100 | yes | B_100TrackedVehicles | default |
| 100Helicopters | 100 | yes | B_100Helicopters | default |
| 30BotOrchestra | 30 | yes | B_30BotOrchestra | default |
| MovementMedley | 100 | yes | B_MovementMedley | default |
| Macarena | 100 | yes | B_Macarena | default |
| InputTest | 5 | yes | B_InputTest | PC_AutomatedPlayerController_C |

Client counts run from 1 (`SoloTest`) to 100 (the `Default`, `100*` and `MovementMedley` / `Macarena` profiles). `InputTest` uses the automated player controller (`PC_AutomatedPlayerController`) with 5 clients.

---

## 3. Client Profiles ([`DT_ClientTestingProfiles`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Tests/LoadTests/Orchestrators/RandomScatter/Data/DT_ClientTestingProfiles.json))

Each client profile is a sequence of automated inputs for the test pawn `B_WDMoverPlayerCharacter`. An input is either a key press or an action (`InputAction`) fired at a random interval and held for a random duration, drawn from the Min to Max ranges.

| Client profile | Input method | Custom spawn | Custom test function | Console commands | Inputs | Automated inputs (interval, duration) |
|---|---|---|---|---|---|---|
| Character | Asynchronous | no | none | none | 5 | IA_Player_MoveDirectional every 2-2 s for 1-3 s; IA_Player_Jump every 2-2 s for 0-0 s; IA_Player_Sprint_Toggle every 2-2 s for 1-3 s; IA_Player_Prone every 3-5 s for 0.5-1 s; IA_Player_Crouch every 1-2 s for 0.5-1 s |
| DownedCharacter | Asynchronous | no | B_AutoTestFunc_DownedPlayer | none | 6 | IA_Player_MoveDirectional every 2-2 s for 1-3 s; IA_Player_Jump every 2-2 s for 0-0 s; IA_Player_Sprint_Toggle every 2-2 s for 1-3 s; IA_Player_Prone every 3-5 s for 0.5-1 s; IA_Player_Crouch every 1-2 s for 0.5-1 s; IA_Player_DownedGiveUp every 1-2 s for 0.5-5 s |
| TriggerHappyCharacter | Asynchronous | yes | B_AutoTestFunc_TriggerHappyPlayer | WD.Player.SetInfiniteAmmo True, WD.Player.SetInvulnerable True | 2 | IA_Player_MoveDirectional every 0-0 s for 1-1 s; IA_Player_PrimaryUse every 0-5 s for 10-10 s |
| MovementCharacter | Sequential | yes | B_AutomatedTestFunc_CustomSpawner | none | 3 | (unset) every 10-10 s for 10-10 s; W every 20-20 s for 20-20 s; (unset) every 10-10 s for 10-10 s |

**Notes**
- `Character` is the baseline: move, jump, sprint toggle, prone and crouch, each on a random interval.
- `DownedCharacter` adds a `DownedGiveUp` action to the baseline, which exercises the downed state.
- `TriggerHappyCharacter` spawns with infinite ammo and invulnerability (`WD.Player.SetInfiniteAmmo True`, `WD.Player.SetInvulnerable True`). `PrimaryUse` is held for 10 s on a 0 to 5 s interval.
- `MovementCharacter` is the only sequential profile. Its input sequence is fixed: a 10 s action, then holds `W` for 20 s, then a 10 s action.

---

## 4. Still Not Pulled / Limitations

- **Orchestrator and test-function blueprints are not in this dump.** The `B_Default`, `B_SoloTest` and `B_AutoTestFunc_*` logic (how clients are spawned and scattered) is not available.
- **Interval and duration values are the ranges as exported.** The random distribution inside a range is not in the data.
- **Input `None` entries** are actions with no key. Their identity comes from `InputAction`, which is empty in some entries.
- **These are test-only assets.** They are not gameplay data and do not affect the player-facing game.

