---
title: "Buildable Challenges"
parent: "Progression & Economy"
group: "Challenges"
description: "The eleven challenges for building, supplying, damaging and hacking buildables and forward operating bases, with the base amounts shown."
---

# Buildable Challenges

| Buildable Challenges | |
|---|---|
| **General** | |
| Kind | Event rewards for buildables and FOBs |
| Challenges | 11 |
| Auto-activate | 9 of 11 |
| Internal name | DT_Challenges_SessionEvents_Buildables |
{: .wiki-infobox }

Buildable challenges pay for work on buildables, the structures players place, including forward operating bases (FOBs). The eleven rows cover building, finishing, destroying, supplying, hacking and closing doors. Most pay cash and role XP from a base amount and a share for the owner or helpers.

## Overview

Rows are grouped by the kind of work: building and finishing, destroying and damaging, schematics and build supplies, and FOB events. The cash and XP columns show the base amounts. Where a row says "match score", the sources list that as the reward and give no cash or XP for it.

## How it works

- **Calculated.** Most rows are worked out from one input. Finishing a buildable uses the build cost, building uses the build amount, FOB resources used uses the cash spent, and hacks and door closures use the victim count.
- **Formula not given.** The sources list the base numbers and the owner or helper shares, but not the formula that combines them with the input. The numbers are shown as the game lists them.
- **Not automatic.** Buildable Damaged and Schematic Placed are not auto-activated.

## Challenges

| Challenge | What earns it | Cash (base) | Role XP (base) |
|---|---|---|---|
| Buildable Damaged | Damaging a buildable | 0 | None |
| Buildable Destroyed | Destroying a buildable | Per structure (see below) | Per structure (see below) |
| Buildable Destroyed Assist | Helping to destroy a buildable | Per structure, as above, split with the assisters | Per structure, as above |
| Buildable Finished | Finishing construction of a buildable | Base 0.5, owner assist 0.25 | Base 0.25, owner assist 0.1 |
| Buildable Building | Contributing to a buildable under construction | 5 per point of build progress inside a zone (1 outside), owner assist 1 | 1 per point of build progress, owner assist 0.4 |
| Schematic Placed | Placing a building schematic | 10 in a control zone, 20 in a hot zone, 0 outside a zone | None |
| Build Supplies Deposited | Placing build supplies in the FOB | Base 0.5, owner assist 0.25, default 0.4 | Base 0.25, owner assist 0.1, default 0.1 |
| Build Supplies Consumed | Using build supplies in the FOB | Base 0.5, owner assist 0.25 | Base 0.25, owner assist 0.1 |
| FOB Resources Used | Another player uses supplies from your FOB | Base 0.5, owner assist 0.25 | Base 0.25, owner assist 0.1 |
| FOB Hacked | Hacking an enemy FOB | Base 0.5, owner assist 0.25 | Base 0.25, owner assist 0.1 |
| Door Closed | Successfully closing a friendly door | Base 0.5, owner assist 0.25 | Base 0.25, owner assist 0.1 |

### Destroyed rewards by structure

| Structure | Cash | Role XP |
|---|---:|---:|
| Forward Operating Base | 2,500, plus up to 7,500 by the FOB's supplies | 500 |
| Hot Zone Magnet (Drill Rig) | 2,750 | 700 |
| Vanguard CIWS | 1,200 | 300 |
| L81 Mortar, Talon 9K-SAM | 650 | 175 |
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

The FOB's supplies bonus is the full 7,500 at 25,000 supplies. A destroyed structure pays on the same scale as the other modes (see [Cash and Rewards](cash-and-rewards.md)).

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
- Buildable reward formulas (JSON)
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
