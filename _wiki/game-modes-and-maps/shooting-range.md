---
title: "Shooting Range"
parent: "Game Modes & Maps"
description: "The practice range: moving targets that drop when hit, with a tutorial that runs on top of it."
---

# Shooting Range

| Shooting Range | |
|---|---|
| Type | Practice range |
| Teams | Three factions set up, as in King of the Hill |
| Objective | None; practice shooting at moving targets |
| Match flow | Single playing state, no pre-match or post-match stages |
| Internal name | ShootingRange (game feature), with a separate tutorial feature |
{: .wiki-infobox }

The Shooting Range is a practice area with no scoring. Its main feature is a moving target that drops when hit and then pops back up. A separate tutorial runs on top of the range to teach the basics.

## Overview

The range is a single playing state. It has no pre-match or post-match stages in the data, which sets it apart from the other modes. Its match scene data was added in Season 2.

## Rules and objectives

- **No score.** The range has no objective and no win condition in the data.
- **Moving target.** The target has a fall of 0.5 seconds when it is knocked down. It has audio for popping up and for being knocked down. Its movement range is 15 to 25, but the data does not state the unit.
- **Layout.** The range's world layout is a separate data layer, and its contents are not in the sources.
- **Teams.** The range uses the same three-faction setup as King of the Hill.
- **Tutorial.** The tutorial is a separate feature that runs on top of the range. Its details are on its own data page.

## Rewards

The range has no cash or XP table. Practice on the range does not appear in the reward tables in the sources.

## See also

- [Maps](maps.md), which lists the training gyms beside the range
- [PvE Scenarios](pve-scenarios.md)
- [King of the Hill](king-of-the-hill.md)

## Sources

- [ShootingRange game feature](../../game-features/Wardogs_GameFeatures_ShootingRange_v2.md)
- [ShootingRange tutorial game feature](../../game-features/Wardogs_GameFeatures_ShootingRangeTutorial_v2.md)
- [Maps and gym data](../../content/Wardogs_Maps_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
