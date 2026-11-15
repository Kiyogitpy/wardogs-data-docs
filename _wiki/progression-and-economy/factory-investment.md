---
title: "Factory Investment"
parent: "Progression & Economy"
group: "Economy"
description: "The first factory investment: three production lines that build weapons and optics, with queue and storage upgrades and recipe costs."
---

# Factory Investment

| Factory Investment | |
|---|---|
| Stored type | Passive investment; current operation unverified |
| Stored purchase cost | 200 cash |
| Production lines | 3 |
| Upgrades | Queue size (three lines), storage size |
| Full in-game name | Zaystev Foundry |
| Internal name | Factory 01 investment (Id.Investment.Factory01) |
{: .wiki-infobox }

The factory definition is marked passive and configures three production lines for weapons and optics. This describes the saved setup; current purchase, scheduling and production consumers have not been established. Each line makes two items, and each item has a cost and a build time. Upgrades raise how many items a line can queue and how much the factory can store.

## Overview

The first factory investment sets up three lines and six recipes. Its saved type is Passive; that enum alone does not prove unattended production. The reviewed definition does not identify a purchase-time unlock grant.

## How it works

- **Lines.** Each line can make only the two recipes listed for it.
- **Queues.** Each line has a queue. The queue size comes from an upgrade. The game reads the queue size from the level of the upgrade.
- **Storage.** The factory has a storage size, also set by an upgrade.
- **Recipes.** Each recipe has a production cost and a production discount. All six rows store ProductionDiscount=20 and bOverrideProductionCost=false. Their stored ProductionCost values are listed below; the false override flag means these fields alone do not establish the charged price or prove it is 80% of the current shop price.
- **Build time.** Every recipe stores RecipeDuration=10. The unit and current timing consumer are not confirmed.

## Numbers

### Production lines

| Line | Recipes |
|---|---|
| Line 1 | AK74, M4 |
| Line 2 | Super-45, AMP-9 |
| Line 3 | 4x Elcan Spectr, Eotech Holographic |

### Stored recipe costs

| Recipe | Cost |
|---|---|
| AK74 | 640 |
| M4 | 2,240 |
| AMP-9 | 1,100 |
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

The game also has a slot amount for each level. The Zaystev Foundry's own upgrade list never uses it, and each line stores slot-upgrade level 1. This does not prove its runtime slot count. The historical CL516586 code analysis read the slot amount. When the factory is set up, the code takes the slot amount for each production line and makes that many slots for the line, so a slot amount is a count of slots per line, separate from the queue size (inferred from the code; the step that looks the value up could not be read). The saved curves use constant extrapolation beyond level 5; whether such levels are reachable is unverified.

The investment starts with its upgrade at level 1 for each of the three queues and for storage.

## Tips that follow from the numbers

- Among the stored ProductionCost fields, the Eotech Holographic optic is lowest (496) and the Super-45 highest (4,480). These are not verified transaction prices.
- Queue and storage both double from level 1 to level 2, then gain a step each level until level 4.

## Season 2 changes

- AK74's recipe cost went from 1,280 to 640.
- AMP-9's recipe cost went from 720 to 1,100.
- Super-45's recipe cost went from 2,080 to 4,480.

## See also

- [Shops](shops.md), where many of the same weapons are sold
- [Cash and Rewards](cash-and-rewards.md)
- [Progression & Economy](../progression-and-economy.md)

## Sources

- [Factory Investment](../../game-features/Wardogs_GameFeatures_FactoryInvestment_v2.md)
- [Factory Investment 01](../../game-features/Wardogs_GameFeatures_FactoryInvestment_01_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
