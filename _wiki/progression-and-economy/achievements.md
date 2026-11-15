---
title: "Achievements"
parent: "Progression & Economy"
group: "Challenges"
description: "The 14 achievement entries in the S3 / 0.3 snapshot, their saved conditions and the four decoded thresholds."
---

# Achievements

The [official Season 3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) announce **three added Steam achievements**: He's Behind You, Car Jacker and Slot Machine. The saved table below contains 14 entries versus 10 in S2, including Sound The Horn as a fourth data addition; the announcement does not claim all four were newly released Steam achievements. Configuration presence and Steam release availability remain distinct.

The CL-533731 / hotfix 533689 snapshot lists **14 achievement entries**, compared with ten in the saved Season 2 table. Each has a Steam achievement ID and is marked to auto-activate. No cash, XP or item rewards are serialized in these entries; this does not establish backend rewards or when an achievement is available.

The goals below summarize the reviewed current StateTree configuration. Event production, native task behavior and backend award behavior are not independently verified. The four numeric blocks were decoded from current saved package bytes: **100,000 cash twice, 3,600 seconds and 95,000 cm (950 m)**.

## Current saved goals

| Achievement | Saved goal | Threshold |
|---|---|---|
| Complete The Tutorial | Tutorial completion event. | No numeric threshold |
| Punch Kristopher | Punch Kristopher with fists. | No numeric threshold |
| Top Cash Earner | Finish first in the cash-earned placement, with cash earned above zero. | No numeric threshold |
| Single Life Profit | Current-life cash profit reaches the stored threshold. | 100000 cash |
| Loadout Spender | A loadout purchase event passes the stored cash threshold; the event amount sign remains unverified. | 100000 cash |
| Control Zone Survivor | A control-zone/alive timer is configured for one hour; effective event filtering remains unverified. | 3600 seconds |
| Long Shot | A hostile kill reaches the distance threshold; the saved cause filter excludes vehicle, AT-mine and claymore tags. | 950 m (95,000 stored cm) |
| Clean Sweep | Your final faction score is above zero and the highest opposing score is zero. | No numeric threshold |
| Ricochet Kill | A hostile kill carries the ricochet context. | No numeric threshold |
| Defibrillator Kill | A hostile kill has the defibrillator cause tag. | No numeric threshold |
| He's behind you | A hostile backblast kill while the pawn has the control-zone tag. | No numeric threshold |
| Car Jacker | A supply-crate reward event carries the stolen-pallet context. The name alone does not establish a vehicle-theft requirement. | No numeric threshold |
| Slot Machine | Hot-zone activation with at least three guessed digits and a code containing at least four digits. | No numeric threshold |
| Sound The Horn | Interact with the shooting-range horn lever; the unlock follows the configured sound-wait task. | No numeric threshold |

Control Zone Survivor's configured timer returns to waiting on the recorded tag/respawn/vitality transitions; the effective event filtering is not proved. Loadout Spender compares the purchase event's cash amount against 100,000, with native sign interpretation still open. The complete criteria, Steam IDs, source fingerprints and threshold evidence are retained in [economy data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json).

## Season comparison

The saved Season 2 shared achievement table has ten entries; the current reviewed list has fourteen. The additional names in this list are He's behind you, Car Jacker, Slot Machine and Sound The Horn. This table comparison alone does not establish when an achievement became available on Steam or whether another historical feature supplied it.

The [historical Season 2 article](https://github.com/Kiyogitpy/wardogs-data-docs/blob/8d0d6a9a0a3a0a0170e7ff3929202a92a5b9c12b/_wiki/progression-and-economy/achievements.md) is retained separately. See the [S2→S3 notes](../patch-notes/season-3.md) and [stored reward differences](../../season-3-changes/rewards-unlocks.md).

## Sources and related pages

- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md)
- [Wagers](wagers.md)
- [Cash and rewards](cash-and-rewards.md)
- [Current economy JSON](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json)
