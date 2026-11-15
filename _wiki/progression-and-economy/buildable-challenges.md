---
title: "Buildable Challenges"
parent: "Progression & Economy"
group: "Challenges"
description: "The twelve challenges for building, supplying, damaging and hacking buildables and forward operating bases, with the base amounts shown."
---

# Buildable Challenges

The [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) announce doubled enemy-emplacement cash: L81 Mortar, Talon 9K-SAM, MG Nest and Stingray go from 650 to **1,300**, and Vanguard CIWS from 1,200 to **2,400**. The table below is saved challenge data; the announcement does not identify its binary consumer. It also announces the enemy-FOB parachute reward and the fuel-deposit drill kickback without specifying amounts.

| Buildable Challenges | |
|---|---|
| **General** | |
| Kind | Event rewards for buildables and FOBs |
| Challenges | 12 |
| Auto-activate | 10 of 12 (stored flags) |
| Internal name | DT_Challenges_SessionEvents_Buildables |
{: .wiki-infobox }

Buildable challenge definitions describe configured rewards for work on buildables, the structures players place, including forward operating bases (FOBs). The twelve rows cover building, finishing, destroying, supplying, hacking and closing doors. Most contain cash and Role XP expressions with owner or helper terms; their current activation is not established.

## Overview

Rows are grouped by the kind of work: building and finishing, destroying and damaging, schematics and build supplies, and FOB events. The cash and XP columns show the base amounts. Where a row says "match score", the sources list that as the reward and give no cash or XP for it.

## How it works

- **Calculated.** Most rows are worked out from one input. Finishing a buildable uses the build cost, building uses the build amount, FOB resources used uses the cash spent, and hacks and door closures use the victim count.
- **Formulas.** Current reward rows include expressions, selectors and variables. The table summarizes those stored inputs; the resulting payout still depends on event inputs, context tags and the current evaluator. Those live bindings have not been verified.
- **Not automatic.** Buildable Damaged and Schematic Placed store false auto-activation flags.

## Challenges

| Challenge | What earns it | Cash (base) | Role XP (base) |
|---|---|---|---|
| Buildable Damaged | Damaging a buildable | 0 | None |
| Buildable Destroyed | Destroying a buildable | Per structure (see below) | Per structure (see below) |
| Buildable Destroyed Assist | Helping to destroy a buildable | Per structure, as above, split with the assisters | Per structure, as above |
| Buildable Finished | Finishing construction of a buildable | BuildCost × (0.5 base or 0.25 owner-assist) × zone factor (2 hot / 1 control / 0.5 outside), plus 25 for the in-zone schematic-owner selector | BuildCost × (0.25 base or 0.1 owner-assist) |
| Buildable Building | Contributing to a buildable under construction | 5 per point of build progress inside a zone (1 outside), owner assist 1 | 1 per point of build progress, owner assist 0.4 |
| Schematic Placed | Placing a building schematic | 10 in a control zone, 20 in a hot zone, 0 outside a zone | None |
| Build Supplies Deposited | Placing build supplies in the FOB | Owner: 0.5 per supply (1 for the friendly-context selector); interactor: 0.4 per supply; zone factor 1 in either zone, 0.1 outside | 0.1 per supply, with the same zone factor |
| Build Supplies Consumed | Using build supplies in the FOB | Owner: 1.4 × the input named BuildSuppliesDeposited, zone factor 1 inside / 0.1 outside; instigator: 1,500, zone factor 1 inside / 0.2 outside | Owner: 0.1 × that input and zone factor; instigator: 250 |
| FOB Resources Used | Another player uses supplies from your FOB | 1 × CashSpent | No Role XP resource in this row |
| FOB Hacked | Hacking an enemy FOB | Base 1,000 (2,500 under the BuildableOwner context); zone factor 2 hot / 1 control / 0 outside; repeat reduction 50%, capped at two | Base 500 hot / 250 control / 0 outside; same repeat reduction |
| Door Closed | Successfully closing a friendly door | Base 75; zone factor 2 hot / 1 control / 0 outside; repeat reduction 50%, capped at two | No Role XP resource in this row |
| Parachute Into Enemy FOB | Entering an enemy FOB by parachute | Base 1,000; zone factor 2 hot / 1 control / 0 outside; repeat reduction 100%, capped at one | No Role XP resource in this row |

### Destroyed rewards by structure

| Structure | Cash | Role XP |
|---|---:|---:|
| Forward Operating Base | 2,500, plus up to 7,500 by the FOB's supplies | Base 500, plus up to 250 by supplies |
| Hot Zone Magnet (Drill Rig) | 2,750 | 700 |
| Vanguard CIWS | 2,400 | 300 |
| L81 Mortar, Talon 9K-SAM | 1,300 | 175 |
| Bunker, Gate, Recon Tower, Indirect Fire Shelter, Loudspeaker, Refuel Station, Repair Station | 200 | 50 |
| SV Shelter | 250 | 65 |
| Door | 100 | 25 |
| Bremer Wall | 30 | 10 |
| Gate ramp | 85 | 20 |
| Hedgehog, Hesco Block (Large), Hesco Block (Small) | 20, 20, 15 | 5 |
| Hesco Wall | 75 | 20 |
| Builder's Radio | 20 | 10 |
| Sandbag Wall, Wood base | 15 | 5 |
| Barbed Wire, Recon Tent | 5 | 5 |
| Bunker floor or roof, Recon Tower floor, shelter floor | 10 | 5 |
| Damaged (any structure) | 0 | none |

The FOB's supplies bonus is the full 7,500 at 25,000 supplies. These challenge expressions are distinct from the match cash table; matching or differing bases do not establish which path pays in a current match (see [Cash and Rewards](cash-and-rewards.md)).

## Season 2 changes

The sources list no Season 2 changes for these rows.

## See also

- [Challenges](challenges.md), the overview of every challenge category
- [Building](../building.md)
- [Forward Operating Base](../building/forward-operating-base.md)
- [Crowbar Challenges](crowbar-challenges.md)

## Sources

- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md), sections 3 and 6
- Buildable challenge table (JSON)
- [Current buildable reward formulas](../../data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengeRewards_SessionEvents_Buildables.json)
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
