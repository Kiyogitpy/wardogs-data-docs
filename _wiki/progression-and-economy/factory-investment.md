---
title: "Factory Investment"
parent: "Progression & Economy"
description: "The first factory investment: three production lines that build weapons and optics, with queue and storage upgrades and recipe costs."
---

# Factory Investment

| Factory Investment | |
|---|---|
| Type | Passive investment |
| Cost | 200 cash |
| Production lines | 3 |
| Upgrades | Queue size (three lines), storage size |
| Full in-game name | Not yet known: the data cuts it off after "Zaystev Foun" |
| Internal name | Factory 01 investment (Id.Investment.Factory01) |
{: .wiki-infobox }

The factory investment is a passive purchase. Once bought, it runs three production lines that build weapons and optics. Each line makes two items, and each item has a cost and a build time. Upgrades raise how many items a line can queue and how much the factory can store.

## Overview

The first factory investment sets up three lines and six recipes. It is passive: it does not need active use once bought. The data does not say what it unlocks at purchase.

## How it works

- **Lines.** Each line can make only the two recipes listed for it.
- **Queues.** Each line has a queue. The queue size comes from an upgrade. The data reads the queue size from the level of the upgrade.
- **Storage.** The factory has a storage size, also set by an upgrade.
- **Recipes.** Each recipe has a production cost and a production discount. The discount is 20 in the data. Whether it is a percentage, and how it applies, is not confirmed.
- **Build time.** Every recipe takes 10 in the data. The unit is not stated, and seconds is an inference.

## Numbers

### Production lines

| Line | Recipes |
|---|---|
| Line 1 | AK-74M, M4 |
| Line 2 | Super-45, MP9 |
| Line 3 | 4x Elcan Spectr, Eotech Holographic |

### Recipe costs

| Recipe | Cost |
|---|---|
| AK-74M | 640 |
| M4 | 2,240 |
| MP9 | 1,100 |
| Super-45 | 4,480 |
| 4x Elcan Spectr | 640 |
| Eotech Holographic | 496 |

### Upgrades

| Level | Queue size (per line) | Slot amount | Storage size |
|---|---|---|---|
| 1 | 5 | 1 | 5 |
| 2 | 10 | 2 | 10 |
| 3 | 15 | 3 | 15 |
| 4 | 20 | 4 | 20 |
| 5 | 20 | 5 | 20 |

The data gives a separate "slot amount" value. Its meaning is inferred from the name. Levels above 5 keep the level 5 values.

The investment starts with its upgrade at level 1 for each of the three queues and for storage.

## Tips that follow from the numbers

- The cheapest recipe is the Eotech Holographic optic (496). The most expensive is the Super-45 (4,480).
- Queue and storage both double from level 1 to level 2, then gain a step each level until level 4.

## Season 2 changes

- AK-74M's recipe cost went from 1,280 to 640.
- MP9's recipe cost went from 720 to 1,100.
- Super-45's recipe cost went from 2,080 to 4,480.

## See also

- [Shops](shops.md), where many of the same weapons are sold
- [Cash and Rewards](cash-and-rewards.md)
- [Progression & Economy](../progression-and-economy.md)

## Sources

- [FactoryInvestment (feature)](../../game-features/Wardogs_GameFeatures_FactoryInvestment_v2.md)
- [FactoryInvestment_01 (feature)](../../game-features/Wardogs_GameFeatures_FactoryInvestment_01_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
