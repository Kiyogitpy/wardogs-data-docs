# Round 86, teammate bp: Blueprint extraction and decoding (census cluster D)

Backlog items V4-06, V4-16, V4-17, V4-18 of `BACKLOG-v4.md`. Everything below was read from the shipped paks with WdExtract (CUE4Parse) and from the restored executable with a static disassembler. The game was not run. Nothing from the Elytra layer was touched.

## Status per item

| Item | Part | Status | Result |
|---|---|---|---|
| V4-06 | Mine, Claymore, IED placement conditions | FOUND | The three placeables list one condition class each (`B_AT_MinePlacementCondition`, `B_ClaymorePlacementCondition` for Claymore and for `B_PlaceableIED`). The classes are identical: fail with `UI.Interactions.PlacementWarnings.InSafeZone` if the placer has `State.Location.SafeZone.Alpha/Bravo/Charlie/Hostile`. No distance, surface, slope or count test. (The census said these were never exported; round 40 had already decoded them, and the FireAndUtility page still carried the stale "not exported" sentence. Re-read from a fresh export and corrected.) |
| V4-06 | Buildable conditions | FOUND | `B_SafeZonePlacementCondition`: tag test plus closest point of any `B_SafeZone` trigger volume must be more than `MinDistanceToSafezone` = 300 cm away. `B_WithinLadderBoundsPlacementCondition`: `BlockRadius` 100 cm, no Blueprint logic (native `WDWithinLadderBoundsPlacementCondition`, already on the Buildables page). |
| V4-06 | Mine/Claymore 30 degree angle and 400 unit reach | NATIVE, not traced | Not tested in any Blueprint. The fields are read by native placement code. |
| V4-06 | `SpawnerOverride`, three gameplay cue tags | FOUND | 32 of 68 buildable definitions set the same three cue tags; `SpawnerOverride` is always an inline `WDActorBuildSpawner`. No numbers. |
| V4-16 | Fire-field `+0x2D4`, `+0x2D8`, `+0x2DC` | FOUND (static) | Function `0x86A0E20`: fire clusters. Horizontal merge radius 600 cm, vertical tolerance 150 cm, at most 4 clusters. |
| V4-16 | Fire-field `+0x2D0` (2000 on the Blueprint, 250 native) | NATIVE, not traced | No reader in the field class code (`0x86A0140` to `0x86A2000`). |
| V4-16 | Molotov burst on impact vs fuse | FOUND | Already settled in round 39 (E-1): `B_Molotov` sets `AWDExplosive+0x49C`, so the first mesh impact detonates it; the 5 s fuse is the backstop. Re-verified: the Blueprint class has no `Explode` logic of its own (listing: begin play only starts the flight audio). |
| V4-16 | Friendly and self fire damage, end of life | PARTLY | Fire field `InitialLifeSpan` 45 s (class default). `B_Molotov_FireField` bytecode has no team or owner test (round 40). Whether later damage rules drop friendly or self damage is native and not traced. |
| V4-17 | `B_Action_*` weapon and movement set | FOUND | 96 classes exported and read; 9 have no bytecode. Class defaults added to `bp-defaults.json` topic `actions` (23 values). Fall, Mantling, Stance, Chamber, Reload, Sprint documented on the ItemActions page. |
| V4-17 | `bRebufferAction` ([`DA_Action_Chamber`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Actions/Weapons/DA_Action_Chamber.json)) | PARTLY | Blueprint side found: `B_Action_ChamberWeapon.BP_OnCancel` returns `EBHGameplayActionCancellationResponse::Buffer` when cancelled before the chamber is done. The flag's own native reader is not traced. |
| V4-17 | Unused bool pair ([`DA_Action_UI_ChangeQuickSlot`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Actions/UI/DA_Action_UI_ChangeQuickSlot.json)) | ABSENT in Blueprints | Neither obfuscated field name occurs in any of the 96 `B_Action_*` listings. Native only. |
| V4-17 | `FullBuffer` vs `PartialBuffer` | PARTLY | Data census generated (22 Full, 34 Partial entries, 20 Full at -10 s). Native handling not traced. |
| V4-18 | `B_DeathmatchSpawner` | ABSENT | Empty Blueprint subclass of native `WDDeathmatchPlayerSpawnManagerComponent`: no variables, overrides, defaults or bytecode. Spawn rules are native (not traced). |
| V4-18 | `B_SniperShowdown_OOBComponent` | FOUND | No timer. Adds/removes one count of `State.Location.SafeZone.Hostile` when the character has neither `State.Location.Objective.ControlZone` nor `.Hotzone` tag. The 20 s countdown is elsewhere. |
| V4-18 | `B_SniperShowdown_ExplodeComponent` | FOUND | On `OnKilled`, 1.5 s delay, then `SimulateRadialDamage`: 250 / 500 / 250 / min 30 / falloff 0.5 / blunt 100, Claymore damage tag. |
| V4-18 | KOTH and Hot Zone StateTrees | FOUND | All 83 `ST_Challenges_*` trees decoded (states, transitions, conditions with values, bindings) into `assets/data/challenge-statetrees.json`; generated tables on the KOTH page. The reward arithmetic is native. |
| V4-13 (bonus) | `LastVictimCount` consumer | FOUND (wiring) | `Resolve Repeat Action Count` with a 180 s cooldown produces `RepeatCount`, bound into `Calculate Reward` as `LastVictimCount` in 29 trees. The formula is native. |
| any | Elytra-protected code | PROTECTED | Not touched. |

SERVER marks: the chamber round move in `B_Action_ChamberWeapon` runs only on a dedicated server, non-bot (`IsDedicatedServer` / `IsBotControlled` tests, offsets 956 to 1110). Nothing else in this cluster is server-only.

## Method and commands

WdExtract (`E:/Reverse_Engineer/wardogs_analysis/round76_icons/bin/WdExtract.exe`, arguments as in `E:/r86/CONTRACT.md`, mappings `normal-order.usmap`):

```
WdExtract <Paks> <aes> <normal-order.usmap> <out> <Paks>/oo2core_9_win64.dll list B_          # 761 packages starting with B_
WdExtract ... list B_Action_ / list B_Molotov / list ST_Challenges                              # prefix is on the file name
WdExtract ... dump <files.txt>                                                                  # one JSON per package, bytecode included
python tools/cue4parse_extractor/kismet_listing.py <in.json> <out.txt>
```

`list` matches the start of the package file name, so the condition Blueprints are found with `list B_` and then filtered (`grep -E "PlacementCondition|B_Action_|..."`), not with a long name. The 211 selected packages (`E:/r86/work/bp/sel1.txt`, copied to `dump1/t86.txt`) went to `E:/Reverse_Engineer/wardogs_analysis/round86_bp/dump1`; the 83 state trees to `E:/Reverse_Engineer/wardogs_analysis/round86_bp/dump_st`.

`kismet_listing.py` was extended: it failed on `EX_LetValueOnPersistentFrame`, `EX_ComputedJump` and the delegate statements that every ubergraph uses, so the event-graph Blueprints (`B_Action_*`, the Sniper Showdown components) gave no output. It now renders them and falls back to a raw dump for an unknown statement.

Native reads (restored exe, `capstone` + `pefile`, RVA = file image RVA):

```
python - 0x86A0140 0x86A2000 0x2D0,0x2D4,0x2D8,0x2DC     # scan of mem operands with these displacements
```

Hits: stores in the constructor `0x86A0140` (250, 600, 150, 4 as in `native-defaults.json`) and reads in the function that starts at `0x86A0E20` (`movss` from `+0x2D4` at `0x86A0F45` and `+0x2D8` at `0x86A0FDF`, `cmp esi, [rcx+0x2DC]` at `0x86A137D`). The array it maintains is at `+0x2F0` (40-byte elements: a summed position and a count at `+0x20`), the second array at `+0x2E0` holds the objects created for new clusters.

## Update pipeline (for the lead)

```
python -I _tools/bp_defaults.py            # now reads two dump folders: DUMP_DIR (round 17) and DUMP_DIR_R86 (E:/Reverse_Engineer/wardogs_analysis/round86_bp/dump1)
python -I _tools/bp_defaults.py --check
python -I _tools/statetree_outline.py      # reads E:/Reverse_Engineer/wardogs_analysis/round86_bp/dump_st, writes assets/data/challenge-statetrees.json
python -I _tools/statetree_tables.py --write | --check
python -I _tools/action_tables.py --write | --check      # new modes bp_settings, buffers; --check is new
python -I _tools/utility_throwable_tables.py --write
```

If `E:/r86/work/bp` is moved, change `DUMP_DIR_R86` in `_tools/bp_defaults.py` and `DUMP_DIR` in `_tools/statetree_outline.py`; both generators leave the committed JSON untouched when their dump folder is absent.

## Files

- Pages: `content/Wardogs_ItemActions_v1.md` (sections 9 and 10), `game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md` (5.1), `game-features/Wardogs_GameFeatures_Experiences_v2.md` (3c), `game-features/Wardogs_GameFeatures_Deathmatch_v2.md`, `game-features/Wardogs_FireAndUtility_v1.md`, `game-features/Wardogs_Buildables_v1.md` (14.4).
- Data: `assets/data/bp-defaults.json` (+ topics `actions`, `placement`, `sniper_showdown`), `assets/data/challenge-statetrees.json`.
- Tools: `_tools/statetree_outline.py`, `_tools/statetree_tables.py`, `_tools/bp_defaults.py`, `_tools/action_tables.py`, `_tools/utility_throwable_tables.py`, `tools/cue4parse_extractor/kismet_listing.py`.

## Limits

- StateTree node classes are not named in the export (the instanced-struct type is lost); the editor name and the instance values are. Behaviours of native tasks (`Calculate Reward`, `Actor In Control Zone`) are known only by name and wiring.
- The cluster function at `0x86A0E20` was read statically; its caller and the type of the created cluster object were not.
