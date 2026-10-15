# Wardogs — GameFeatures: PerformanceCaptures (v2)
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: `Plugins/GameFeatures/PerformanceCaptures/` — 4 JSON files.*

---

## 1. What This Folder Holds

The performance-capture tooling: a game-state component for capturing performance data, and three per-world data assets that define the world bounds and how each world is divided into a grid for capture.

| File | Type | Role |
|---|---|---|
| `Content/PerformanceCaptures.json` | GameFeatureData + component action | Adds the capture component to the game state |
| `Content/GridCell/WorldData/DT_PerformanceCaptureWorldData_GymCore.json` | `WDPerformanceCaptureWorldData` | Gym test world |
| `Content/GridCell/WorldData/DT_PerformanceCaptureWorldData_ICB_WP.json` | `WDPerformanceCaptureWorldData` | ICB world (World Partition) |
| `Content/GridCell/WorldData/DT_PerformanceCaptureWorldData_WorldMGT.json` | `WDPerformanceCaptureWorldData` | World management test world |

---

## 2. Component

| Item | Value |
|---|---|
| Host | `WDGameState` |
| Component | `B_PerformanceCaptureGameStateComponent` |
| Flags | client component: true (the server flag was not read in this pass) |

---

## 3. World Data

| World | Min (X, Y) | Max (X, Y) | Slices (X × Y) |
|---|---|---|---|
| `GymCore` | (13470, 50750) | (213140, 251100) | 5 × 5 |
| `ICB_WP` | not in export | (1626500, 1625600) | 5 × 5 |
| `WorldMGT` | (7640, 7590) | (788520, 786970) | 5 × 5 |

Each world is split into a 5 × 5 grid for capture. Bounds are in native units (Unreal cm is assumed, not confirmed). `ICB_WP` omits `WorldBoundsMin` in the export; its minimum is therefore a default value that the dump does not show.

Z bounds are 0.0 in every world.

---

## 4. How Values Combine

- The game state gets the component from the pack. The world-data asset defines the grid; the component's use of it is inferred from the names.
- Each world's bounds and 5 × 5 slices set the cell size. Cell size is bounds divided by slices. For example, GymCore comes to about 39,900 by 40,100 units per cell (computed, not exported).

---

## 5. Still not pulled / limitations

- **Capture output.** What the component records per cell (frame times, draw calls, memory) is in the native class and not in this export.
- **Grid use.** How the capture is started and where its output goes is not in this folder.
- **ICB_WP minimum.** Not in the export.
- **Units.** Unit scale is assumed.
