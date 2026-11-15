---
title: "S3 / 0.3 Coverage"
parent: "Patch Notes"
description: "Build identification and data coverage for S3 / 0.3."
---

# S3 / 0.3 Coverage

| S3 / 0.3 | |
|---|---|
| Observed game build | CL-533731, hotfix 533689 |
| Steam build | 26615518 |
| Comparison | Asset paths accounted for; three stored curves compared; gameplay values not validated |
{: .wiki-infobox }

This page tracks the data coverage for the S3 / 0.3 build. It is not an official release note, and a reliable list of gameplay changes is not yet available.

## Data coverage

The attempted export failed its completeness checks: the exported data was 31.7% smaller than the Season 2 baseline and six expected weapon and ammunition fields were missing. The affected assets were present, but their data was not fully decoded. These results cannot establish whether a weapon, ammunition type or other gameplay value changed.

The wiki's existing tables, calculators and Season 2 comparisons describe earlier data, principally build CL-516586. They have not been updated or validated for S3 / 0.3 and should not be treated as current S3 values. Three selected stored-curve comparisons are described below; the full balance data and mapping remain unvalidated.

A broad gameplay comparison needs a complete, validated export of the newer build. See the [Season 2 notes](season-2.md) for the earlier comparison.

## Selected stored curve comparisons

Three current CurveFloat key sequences were checked against exact packed float32 bytes and complete export boundaries, then compared with saved CL-516586 JSON exports. Current build attribution comes from retained input receipts. The asset links below point to the saved CL-516586 exports.

| Asset identifier | CL-516586 Time → Value | CL-533731 Time → Value | Key interpolation |
| --- | --- | --- | --- |
| [`CRV_ParachutePunishment_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_ParachutePunishment_Damage.json) | 695→0; 1700→100 | 700→0; 900→20; 1200→100 | Linear |
| [`CRV_Challenges_Curves_DeploySupplyCrate_XP`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_DeploySupplyCrate_XP.json) | 0→0; 500→0.1; 1000→0.25; 2000→0.5; 2500→1 | 0→0; 100→0.1; 1500→0.25; 5000→0.5; 10000→1 | Constant |
| [`CRV_SteerSpeedVariant_WHL_07`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07/Content/Curves/CRV_SteerSpeedVariant_WHL_07.json) | 0→1.425; 21→1; 42.1→0.65; 80→0.5 | Same four complete key records, plus 95→0.5 and 100→3 | Cubic |

The XP curve's key values are unchanged; four input breakpoints move. The parachute curve's old final leave tangent changes from approximately 0.05540166 to 0. The WHL_07 added keys have matching arrive and leave tangents of approximately 0.0004710732 and 0.08496196, respectively, with no tangent weighting. Decimal notation abbreviates stored float32 representations.

These are stored-data comparisons. Historical field interpretation relies on the old mapping and pinned saved exports; old package bytes were not independently reparsed. The current key bodies were independently byte-checked, while native name resolution and build attribution retain their provenance limits. Asset names do not establish input units, consumer calls, effective damage, reward or steering behavior, or live/server activation. These comparisons do not establish full extraction or general schema compatibility. Other mapped field candidates remain unvalidated.

For general earlier-build context, see [Vehicle handling](../vehicles/vehicle-handling.md).

## Mounted asset paths

The saved Season 2 CL-516586 `.uasset` path list contains 66,550 unique paths; the CL-533731 / Steam build 26615518 effective mounted-provider inventory contains 67,689. Comparing exact paths gives **66,222 retained, 328 old-only and 1,467 new-only**. These are path identities, not comparisons of asset bytes: retained assets may have changed, and some different paths may represent casing changes or possible relocations.

The current inventory includes a separate HotZoneMagnet buildable root with 33 new-only asset paths, two new KOTH challenge-related paths, and additional vehicle grip-curve and animation assets. Molotov and Crowbar asset paths also change. These observations do not establish unlocks, handling values, active modes or other gameplay changes.

The current inventory also contains map packages, mostly generated partitions. The saved baseline lists `.uasset` paths only; without a validated old map manifest, map additions and removals are unknown. Package presence alone does not establish that a map is selectable or content is active.
