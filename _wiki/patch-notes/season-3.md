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
| Comparison | Asset paths accounted for; gameplay values not validated |
{: .wiki-infobox }

This page tracks the data coverage for the S3 / 0.3 build. It is not an official release note, and a reliable list of gameplay changes is not yet available.

## Data coverage

The attempted export failed its completeness checks: the exported data was 31.7% smaller than the Season 2 baseline and six expected weapon and ammunition fields were missing. The affected assets were present, but their data was not fully decoded. These results cannot establish whether a weapon, ammunition type or other gameplay value changed.

The wiki's existing tables, calculators and Season 2 comparisons describe earlier data, principally build CL-516586. They have not been updated or validated for S3 / 0.3 and should not be treated as current S3 values. No numeric balance changes are confirmed by this comparison.

A gameplay comparison needs a complete, validated export of the newer build before changes can be listed here. See the [Season 2 notes](season-2.md) for the earlier comparison.

## Mounted asset paths

The saved Season 2 CL-516586 `.uasset` path list contains 66,550 unique paths; the CL-533731 / Steam build 26615518 effective mounted-provider inventory contains 67,689. Comparing exact paths gives **66,222 retained, 328 old-only and 1,467 new-only**. These are path identities, not comparisons of asset bytes: retained assets may have changed, and some different paths may represent casing changes or possible relocations.

The current inventory includes a separate HotZoneMagnet buildable root with 33 new-only asset paths, two new KOTH challenge-related paths, and additional vehicle grip-curve and animation assets. Molotov and Crowbar asset paths also change. These observations do not establish unlocks, handling values, active modes or other gameplay changes.

The current inventory also contains map packages, mostly generated partitions. The saved baseline lists `.uasset` paths only; without a validated old map manifest, map additions and removals are unknown. Package presence alone does not establish that a map is selectable or content is active.
