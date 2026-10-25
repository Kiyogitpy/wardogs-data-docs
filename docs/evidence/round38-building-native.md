# Round 38: the building arithmetic (native)

Topic: `building-native`. Evidence: static disassembly and the decompiled corpus (CL-516586, RVAs, image base `0x140000000`) plus cooked data. Nothing was run; no devirtualization. Helpers: `E:/Reverse_Engineer/wardogs_analysis/round38_native/` (`fn.py` dumps a function by RVA, `dis.py`, `xref.py`). Table: `python -I _tools/build_time_table.py`.

## Summary

| # | Question | Status | Result |
|---|---|---|---|
| 1 | Hit to progress, hits, supplies per hit | NATIVE, traced | per hit `progress += A / T`; `A = BuildAmount * f60`; `T = round(Cost * S)`; supplies per hit average `A` |
| 2 | `Cost` to supplies | NATIVE; scale `S` is SERVER (live curve) | `Cost` is the total spent over the hits; `PlacementCost` separate, 0 everywhere |
| 3 | Repair, dismantle | NATIVE; refund ABSENT | repair = same path with `A * RepairSpeedMultiplier`; dismantle = damage |
| 4 | `BuildBuildable` extension | NATIVE, resolved | on the hammer path (the hammer class derives from it) |
| 5 | FOB `DoNotTakeDamage` | NOT RESOLVED | no native reader found |

## 1. Hit to progress

Chain: `Server_SingleHitMode_Construct` -> `0x86032F0` -> `0x85EAAA0` -> `0x85F1D90` (hit amount) -> `0x85F1F20` (arithmetic). `this` of `0x85F1F20` is the hammer's `UWDItemExtension_BuildBuildable` (`+0x138` SpendingHelper, `+0x140` CriticalHitSpotManager, `+0x15C` float credit).

- Normal hit: `A = BuildAmount (ext data +0x4C) * f60`, `f60` = `0x85FA770` = `WDBuildableDataAsset +0x60` (unnamed `_aaabkhhnlcojdebfcnjfd`; native default 1.0, constructor `0x8585020`). Data: Barbed Wire 3.5, Camo Net Tent 3.5, Hotzone Magnet 2.0, STN_02 1.25, all others 1.
- Critical-spot hit: `A = BuildAmountWhenTargetIsHit` (spot-manager data `+0x50`); no `f60`.
- In `0x85F1F20`: if `GetIsFullyBuilt` (interface call `0x8578A80`, name read from the binary; implementation `0x85BB060`: `abs(BuildingProgress(+0x144) - 1) <= 1e-8`) then `A *= RepairSpeedMultiplier (+0x64)` (instruction `0x85F2020`). So the multiplier is a repair multiplier only.
- `T` = `0x858D1D0` (= `GetTotalBuildCost` `0x8593FB0`) = `max(1, floor(abs(Cost * S) + 0.5))`, `Cost` at `+0x5C`; `GetPlacementCost` `0x8593E80` is the same on `PlacementCost` (`+0x58`); `GetTotalSupplyCost` `0x85940E0` is their sum.
- Progress per hit (`0x85F1F20`): `v14 = CeilToInt(A)` (`cvtss2si` trick), `u = min(min(v14, have) + credit, A)`, `x = min((1 - p) * T, u)`, gain `x / T`; credit `-= x`; when it goes below -1e-4 whole supplies `n = CeilToInt(-credit - min(max(T,1)*1e-4, 0.1))` are taken and added back. `p` = `GetProgress` (`0x8578B60`).
- Confirmed independently by `0x85F23C0` (client prediction): `BuildAmount * f60 / T`, or `BuildAmountWhenTargetIsHit / T`.

Result (S = 1): hits to build = `ceil(T / (BuildAmount * f60))`; supplies spent in total = `T` whichever hammer; Sandbag Wall (15) 30 / 15 / 10 hits Small / Medium / Large; Bunker (200) 400 / 200 / 134; FOB instant. Seconds = hits x swing period, which is not native (loop of the use montage 0.567 / 0.567 / 0.883 s used as an assumption). Stage thresholds only choose meshes.

## 2. Cost to supplies

- Placement: `PlacementCost` is checked in `0x85BF0F0` (`0x85F9F10`, action tag `Action.BuildTool.PlaceSchematic`) and spent by `0x85F3370`/`0x85F3070` (flow `0x85A9CE0`, link inferred). Data has 0 on every buildable. The build wheel shows `GetTotalSupplyCost` (`0x8605EF0`).
- Per hit: `Cost` is the total spent across the hits (section 1).
- Scale `S`: `0x6CB9970`. 1.0 when the player object has no component; otherwise a curve value (`UCurveFloat` evaluation `0x3E0DA70`) from a `LiveCurves` lookup (`0x6CB90B0`, globals `qword_14D36FC18/FD10`) sampled at a float of the game-state session object (`0x6DA30F0`, `+0x434`, by SDK layout `MatchPointTimer`, inferred). No asset in `data/` sets it; curve contents are live/server data (SERVER). The table uses 1.0.

## 3. Repair and dismantle

- Repair: `GetProgress` (`0x858C220`) returns `BuildingProgress` below 1.0 and `health / data.MaxHealth (+0x78)` when finished (`0x858C300`..). `TryAddBuildProgressOrHealth(fraction, supplies, controller)` (name read from the binary, impl `0x85929D0`) adds `fraction * MaxHealth` health with `fraction = A_rep / T`, capped; unneeded supplies refunded proportionally (`0x8592BA8`). Full repair from zero: `ceil(T / (BuildAmount * f60 * RepairSpeedMultiplier))`, about `15 / BuildAmount` hits for most structures (Bunker, Large: 20).
- Damage to an unfinished structure (`0x858FF60`) subtracts `damage / MaxHealth` from `BuildingProgress`; at 0 it is destroyed.
- Dismantle (`0x85D55A0` -> `0x85AFCD0`): a damage event `Damage.Type.Dismantle`, amount `DismantleRatePerHit` (250 / 200 / 150) times `DismantleModifiers` (Friendly 1.0 own structure, Hostile 0.5 other owner; key choice inferred). No supply credit call: refund ABSENT. `OnBuildableDestroyed` (`0x85D56A0`) not decoded.

## 4. `UWDItemExtensionData_BuildBuildable`

On the hammer path: `UWDItemExtensionData_BuildTool` derives from it; the hammer's `BuildAmount` is the base field `+0x4C` (read at `0x85F1EB6`). 3.0 is the constructor default (`0x85E7410`) for unset assets. `BuildAmountPerSecond` (`+0x50`) is for `UWDBuildingMode_Continuous`; hammers keep `Applicationtype` 0 (SingleHit).

## 5. FOB `DoNotTakeDamage`

Not resolved. `_aaaaoiekbaalgokkaahpa` is an `FName` at `WDBuildableDataAsset +0x2F0` set only on the FOB. `ReceiveDamage` (`0x8594C70` -> `0x858FF60`) has no read of it and no tag check (unfinished: lowers progress; finished: passes damage to the vitality component). A scan of the buildables functions for readers of `+0x2F0` found none; Blueprint or unmodelled paths are not excluded. Also: the FOB Blueprint default object overrides `WDVitalityComponent` `BaseHealth`/`MaxHealth` to 300 (generic `B_Buildable` has no override); how the vitality gets its health from the 15,000 data value is not decoded.

## Wiki updates

- Hammer / building article, build speed: old "not known" -> each hit adds `build amount / Cost` of progress; hits = `Cost / build amount` (Small 0.5, Medium 1, Large 1.5); Sandbag Wall 30 / 15 / 10, Bunker 400 / 200 / 134; Barbed Wire and Camo Net Tent 3.5x per hit, Hotzone Magnet 2x, STN_02 1.25x. No seconds until the swing rate is confirmed.
- Build Supplies: old "unknown" -> `Cost` is spent a little per hit (about the hammer's build amount per hit); total `Cost` whichever hammer; placement charges nothing today.
- Repair: old "unknown" -> a hit restores `build amount x repair multiplier / Cost` of maximum health; full repair about 15 / build amount hits (Bunker, Large hammer: 20).
- Dismantle: old "refunds unknown" -> damage 250 / 200 / 150 per hit on your own structure, half on someone else's; no refund found.
- Unfinished structures: damage removes build progress in proportion to maximum health.
- FOB: still unknown whether it takes damage; do not state either way.
