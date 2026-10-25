# Round 53: native defaults of the vehicle deployment board

Statuses: FOUND (value read), NATIVE (lives in code, consumer or meaning not read), PROTECTED, SERVER, ABSENT. Evidence level: static disassembly of `WardogsClient-Win64-Shipping.restored.exe` with capstone (helpers in `E:/Reverse_Engineer/wardogs_analysis/round40_veh/`: `rxref.py`, `rdis.py`) plus the decompiled corpus index. The game was never run; the protection layer was not touched (neither constructor sits behind it).

## Why this was open

Round 51 ([data page](../../game-features/Wardogs_VehicleSpawns_v1.md)) found that the board Blueprint `B_VehicleDeploymentBoard` sets only `RadarRestoreHealthThreshold` (0.55) and `PlayerDeployCooldown` (600), and no map board overrides anything. Only the Gym test boards set the respawn timer (240 s) and cooldown (120 s). So on the live maps every other board property is the native class default.

## Method

1. The board vtable `AWDVehicleDeploymentBoard_VFT` is at RVA `0xB690390` (corpus alias table).
2. `rxref.py B690390` finds two code references: `0x770967B` (the destructor, decompiled in the corpus) and `0x7708A2D`, inside the constructor.
3. `rdis.py 7708A00 1400` decodes the constructor, which starts at RVA `0x7708A00`. It zeroes the object, writes the vtable, then stores the float and int constants below. Offsets match the SDK layout (`sdk/raw/WDGame_classes.hpp`, `AWDVehicleDeploymentBoard`). Float constants are IEEE-754 immediates.

## Board properties (constructor `0x7708A00`)

| Property | Offset | Instruction | Native default | Blueprint | Value on live maps | Status |
|---|---|---|---|---|---|---|
| `VehicleRespawnTimer` | `0x408` | `mov [rdi+0x408], 0x43960000` | 300 s | not set | 300 s | FOUND |
| `LosingVehicleRespawnTimer` | `0x40C` | `0x42700000` | 60 s | not set | 60 s | FOUND |
| `VehicleHealthThreshold` | `0x3F8` | `0x3E99999A` | 0.3 | not set | 0.3 | FOUND |
| `VehicleSpeedThreshold` | `0x400` | `0x41200000` | 10 | not set | 10 | FOUND (unit not shown) |
| `MinRequiredScore` | `0x404` | `0x41A00000` | 20 | not set | 20 | FOUND |
| `LosingScoreThreshold` | `0x410` | `0xF` | 15 | not set | 15 | FOUND |
| `SpawnFailedRetryTime` | `0x414` | `0x41200000` | 10 s | not set | 10 s | FOUND |
| `PlayerDeployCooldown` | `0x418` | `0x42F00000` | 120 s | 600 s | 600 s | FOUND (Blueprint wins) |
| `RadarRestoreHealthThreshold` | `0x3FC` | `0x3F000000` | 0.5 | 0.55 | 0.55 | FOUND (Blueprint wins) |
| `MaxInteractionDistance` | `0x358` | `0x43FA0000` | 500 cm | not set | 500 cm | FOUND |
| `SpawnVehicleStateRetryDelay` | `0x3C0` | `0x3F800000` | 1 s | not set | 1 s | FOUND |
| `StreamingTimer` | `0x3C4` | `0x40A00000` | 5 s | not set | 5 s | FOUND |
| `LookbackSeconds` | `0x3D4` | `0x41F00000` | 30 s | not set | 30 s | FOUND |
| `DamageLookBackSeconds` | `0x3D8` | `0x41200000` | 10 s | not set | 10 s | FOUND |
| `MinRiskDisplaySeconds` | `0x3DC` | `0x41700000` (low half of a qword store) | 15 s | not set | 15 s | FOUND |
| `ContestedThreshold` / `LethalThreshold` | `0x3CC` / `0x3D0` | 1 / 2 | 1 / 2 | not set | 1 / 2 | FOUND (meaning unread) |
| `LineOfSightTargetZOffset` | `0x3A8` | `0x43160000` | 150 cm | not set | 150 cm | FOUND |

The Gym boards' 120 s cooldown therefore equals the native default, and their 240 s respawn timer is a real override of the native 300 s.

## MaxVehiclesPerPlayer

`UWDVehicleUtilityComponent` (vtable RVA `0xBCA4440`) constructor starts at `0x893EDE0`; `mov dword ptr [rdi+0xE0], 2` at `0x893EE0E` sets `MaxVehiclesPerPlayer`. The value 2 therefore holds in the class default as well as in `DefaultVehicleUtility.ini` (`MaxVehiclesPerPlayer=2`). It is a config property, not a Blueprint default; there is no Blueprint for the component. FOUND, confirmed.

## What consumes the values (NATIVE, partly read)

Scan of every function in `0x76F0000..0x7730000` for loads at the board offsets:
- `0x770C7B0` (rejection-reason selection): compares a player-state score against `+0x404` (MinRequiredScore) and the absolute value of a virtual call result (vehicle slot `+0x9C8`, a speed) against `+0x400` (VehicleSpeedThreshold), each choosing a rejection branch. Which of the three rejection tags (Driving, LowHP, NoSeat) each branch maps to was not traced.
- `0x770EF10` (board tick): compares each player-state score with `+0x404` and starts the risk update `0x770ABA0`.
- `0x770FDF0` (risk): reads `+0x3D4`, `+0x3D8`, `+0x3DC` (look-back and display times).
- `0x770DF00`: multiplies by `+0x3FC` (radar restore health fraction).
- `0x770E860`: reads `+0x3C4` (StreamingTimer).
- No direct read of `+0x408`, `+0x40C` (the two respawn timers), `+0x3F8` (health threshold) or `+0x418` (cooldown) was found in the board's own functions. They are probably read in code not reachable from the vtable slot list (inlined into a server path or reached through a thunk). NATIVE, open: the exact use of the respawn timers is inferred from their names and from the reflected functions `GetRemainingRespawnTimeSeconds` and `SpawnVehicleDestroyed`. Nothing PROTECTED was hit.

## Scope of the respawn timers

The board class owns exactly one vehicle, `CurrentSpawnVehicle` (the APC; fields `bIsSpawnVehicleAlive`, `SpawnVehicleDestroyed`). The two respawn timers therefore most likely time that deployment APC, not the vehicles of the yards (inferred from names, not from a read consumer).

## Open

- Consumer of the two respawn timers and of the health threshold (see above). Whether "losing" means the side's score deficit compared with `LosingScoreThreshold` (15) is inferred from the names only.
- Unit of `VehicleSpeedThreshold` (10).
- Per-yard vehicle counts and per-vehicle respawn: still not in client data.

## Reproduce

```
python rxref.py B690390          # vtable references: 0x770967B (dtor), 0x7708A2D (ctor)
python rdis.py 7708A00 1400      # board constructor
python rxref.py BCA4440          # 0x893EE19, 0x893EEF0 (component ctor)
python rdis.py 893EDF0 200
```

## Wiki updates

- `_wiki/game-modes-and-maps/maps.md` (Vehicle spawns on the main maps): add the respawn, losing-side respawn and deploy cooldown sentences.
- `_wiki/guides/vehicle-guide.md`: new tip on the destroyed spawn vehicle and the cooldown.
- `_wiki/vehicles/m113-apc-sv.md`: "Respawn time after a loss is not in the data" becomes 300 s (60 s for the losing side).
