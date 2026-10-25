---
title: Round 42 buildables, progression and economy
nav_exclude: true
---

# Round 42: buildables, progression and economy backlog

Topic `econ-buildables`. Evidence: cooked data read with the offline extractor and the repository's `data/` export, SDK headers, the decompiled corpus (CL-516586, RVAs, image base `0x140000000`) and static disassembly. Nothing was run, no devirtualization. Scratch and helper scripts: `E:/Reverse_Engineer/wardogs_analysis/round42_econ/`.

Statuses: FOUND (value read, with the asset), SETTLED (answered in an earlier round, reference given), SERVER, ABSENT (searched, list given), NATIVE (open, exact next step), NOT WORKED (deferred, no budget this round; nothing claimed).

New or changed files: this page, `_tools/structure_hits.py` (idempotent), `assets/data/structure-hits.json`.

## Summary

| Status | Buildables | Progression and economy | Total |
|---|---:|---:|---:|
| FOUND | 6 | 15 | 21 |
| SETTLED earlier | 5 | 11 | 16 |
| SERVER | 0 | 5 | 5 |
| ABSENT | 2 | 3 | 5 |
| NATIVE (open) | 2 | 5 | 7 |
| NOT WORKED | 6 | 3 | 9 |
| Rows | 21 | 42 | 63 |

(Rows that have two parts are counted once, under the main answer.)

## Buildables

| # | Row | Status | Result |
|---|---|---|---|
| B1 | Hits to destroy each structure | FOUND (Derived) | All 66 projectile and explosive sources against all 31 buildable assets: `assets/data/structure-hits.json`, tool `python -I _tools/structure_hits.py`. Selection below. |
| B2 | How several matching damage entries stack | SETTLED | `pipelines/Wardogs_DamagePipeline_v2.md` section 6 (native `0x6BB6FB0`): `Percentage_Ongoing` multiplies the running amount by `1 + Amount/100`, `Add` adds, clamp at 0 once. All 354 non-empty buildable entries are `Percentage_Ongoing` except 8 `Add` entries (tracked vehicle). So matching entries multiply, in any order. |
| B3 | Entry requirements (instigator, target, hit location) and priority | SETTLED + FOUND | Matching rule: DamagePipeline section 4-5. For the 20 buildable damage rows the tool asserts no entry has an instigator, target or hit-location requirement and none is a custom operation: the only requirement is the source tag (all required tags must be in the lineage of the hit's source and context tags). Priority categories (`Bone`, `Melee`, `CaliberEffectiveness`) do not change the arithmetic because the operations commute. |
| B4 | Drill Rig fuel units and run time | SETTLED | `docs/evidence/round38-building-data.md` section 6: timers in seconds, run time = fuel x 0.03 s (60 s at the 2,000 minimum, 300 s at the 10,000 maximum), recharge 900 s. |
| B5 | Refuel Station and IED damage | FOUND | The table cell `-` only means no IED-specific entry. The IED (`Meta.Damage.Explosive.Utility.IED`, base 300) matches the parent `Meta.Damage.Explosive.Utility` entry, which is 0 percent for the stations, so it does its base damage: 300 per hit: 6 hits on a Refuel Station (1,600 health). The Repair Station has its own IED entry (+1000 percent) and falls in 1 hit (JSON `hits.IED`). |
| B6 | `RepairSpeedMultiplier` meaning | SETTLED | `round38-building-native.md` sections 1 and 3: applied only when the structure is fully built (`0x85F2020`), so it multiplies the hit amount for repair only. |
| B7 | MG Nest rate, range, targets | FOUND (targets ABSENT) | `WE_STN_06_MountedMachineGun` ("Mounted M2 Browning", `DA_MWSY_001_Heavy_MountedMachineGun_Stats`): 600 rounds/min (the stats asset omits it; native struct default 600, `0x699E6C0`), effective range 1,000 m, 50 Cal, starting ammo 60 `Id.Item.50Cal.Tracer`, reload 8 s, automatic. Also in `assets/data/vehicle-weapons.json`. No target list exists in the stats or the actor data (searched `DA_MWSY_001*`, `WE_STN_06*`, `DA_Buildable_MGNest`): the gun is a player-operated stationary weapon, so there is nothing to list. |
| B8 | Vanguard CIWS magazine duration | FOUND (Derived) | `WE_STN_02` ("Mounted Verba"), 1,800 rounds/min, starting ammo 500 `Id.Item.20x102mm`, reload 3 s: 500 / (1,800 / 60) = 16.7 s of continuous fire per magazine. |
| B9 | Stingray drone reload | SETTLED | `docs/evidence/round36-combat.md` section 4 (a restock, not a reload); restock fields in `round36_combat.py stationary`. |
| B10 | Loudspeaker function | ABSENT | Searched `DA_Buildable_*`, the buildable folder listing, `vehicle-weapons.json` (no Loudspeaker weapon), the reward tables. Only reward rows exist (see B11). |
| B11 | Mortar, Phalanx, Talon 9K-SAM, Loudspeaker rows | FOUND (rewards) / ABSENT (hammer data) | No `DA_Buildable_*` folder for them exists in `Items/Buildables/Content/Data/Buildables/` (25 folders listed, none of the four). Their destroy rewards do exist in `DT_ChallengeRewards_SessionEvents_Buildables`: Mortar cash 650 / Role XP 175, MistralAA 650 / 175, Phalanx 1,200 / 300, Loudspeaker 200 / 50 (table below). |
| B12 | FOB placement rules | NATIVE (open) | Known: safe-zone and ladder-bounds conditions (`round38-building-data.md` section 4). The FOB-specific placement check is not located. Next step: the placement flow `0x85BF0F0` (checks `PlacementCost`) and the callees that read the FOB flag in the data asset; look for the `FOBPlacementCheck` virtual in `UWDBuildableDataAsset` vtable. |
| B13 | Explosive whitelist empty | NOT WORKED | Deferred. |
| B14 | World-prop health, hits, fall time | NOT WORKED | Deferred (`CP_*_C` prefab classes are not exported). |
| B15 | Destruction lookup consumers | NOT WORKED | Deferred. |
| B16 | Demolition impulse, mass, thresholds | NOT WORKED | Deferred. |
| B17 | Demolition zones `Important` / `Distant`; remnant `Offset` fields | NOT WORKED | Deferred. |
| B18 | Item weight and inventory-size units | NOT WORKED | Deferred. |
| B19 | Hammer swing period (seconds to build) | FOUND (Derived) | The three use montages carry a named `Hit` notify inside the loop section (`bTriggerOnDedicatedServer` true, tick type Queued, track rate scale 1.0): Medium `Hit` 0.2515 s in loop 0.2 to 0.7667 s, Small `Hit` 0.2444 s in loop 0.1667 to 0.7333 s, Large `Hit` 0.4496 s in loop 1.05 - 0.1667. So one hit per loop pass: 0.567 s (Small, Medium), 0.883 s (Large) at play rate 1. The hammer item data has no use-rate, cooldown or play-rate field (diffed the three `ID_*Hammer` assets: only BuildAmount, trace and dismantle values differ). Evidence: `E:/Reverse_Engineer/wardogs_analysis/round42_econ/am/AM_FP_BuildTool_Use.json` (dump of the Medium montage). The native consumer of the `Hit` notify name is still not decoded, so seconds stay Derived. The shop text calls the Large hammer "fast": per second it builds 1.5 / 0.883 = 1.70 against the Medium's 1.76, so the text is not explained by the loop; unresolved. |
| B20 | FOB `Buildable.Damage.DoNotTakeDamage` | ABSENT (by name) | The string `Buildable.Damage.DoNotTakeDamage` occurs in exactly one place in `data/` (`DA_Buildable_FOB`, FName at +0x2F0) and nowhere in the executable (searched ASCII and UTF-16), and it is not a registered gameplay tag (no row in `DefaultGameplayTags.ini` or the tag lists). A name that no code and no other asset mentions cannot be matched by value; with round 38's finding that no function reads `+0x2F0`, the field is dead data in this build. Open (NATIVE): a read of the FName by number rather than by string is not excluded; next step is `xref` of `+0x2F0` over virtual calls in `0x8590000..0x85D0000`. |
| B21 | FOB vitality 300 vs data 15,000 | NATIVE (open) | Data: `DA_Buildable_FOB.MaxHealth` 15,000; the FOB Blueprint default overrides `WDVitalityComponent.BaseHealth/MaxHealth` to 300. `GetProgress` uses `health / data.MaxHealth (+0x78)` (`0x858C300`). The function that copies the data value into the vitality component was not found (scanned `0x8570000..0x8610000` for `+0x78` readers; candidates `0x858A830`, `0x858FF60`, `0x85AC000` are not it). Do not state either number as the FOB's real health. |

### B1: hits to destroy, selection

Point blank, full base damage at the centre of an explosion, no falloff, no ricochet or penetration, finished structure; 12 gauge is per pellet; each cell is `ceil(health / damage)` where damage is the base times every matching entry. `-` means the source cannot damage it. Full table: `assets/data/structure-hits.json`.

| Source | Base | SandbagWall | HBlock | TallHBlock | Door | Gate | Bunker | BarbedWire | Radio | RepairStation | TankTrap | BremmerWall | FOB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Health | | 735 | 1,600 | 2,250 | 2,200 | 5,320 | 5,000 | 250 | 1,000 | 1,600 | 4,500 | 6,500 | 15,000 |
| 556mm FMJ | 28 | 175 | 286 | 402 | 524 | 1,267 | 893 | 60 | 239 | 286 | 1,072 | 1,161 | 2,679 |
| 762x51mm FMJ | 60 | 82 | 134 | 188 | 245 | 592 | 417 | 28 | 112 | 134 | 500 | 542 | 1,250 |
| 50Cal FMJ | 90 | 55 | 89 | 125 | 163 | 395 | 278 | 19 | 75 | 89 | 334 | 362 | 834 |
| 50Cal ArmorPiercing | 90 | 28 | 66 | 93 | 82 | 198 | 155 | 10 | 38 | 66 | 167 | 268 | 618 |
| 20x102mm | 60 | 62 | 334 | 469 | 459 | 178 | 84 | 9 | 9 | 107 | 150 | 542 | 313 |
| 30mm | 100 | 15 | 32 | 45 | 44 | 107 | 50 | 5 | 5 | 32 | 90 | 130 | 300 |
| 35x228mm | 60 | 62 | 334 | 469 | 459 | 178 | 84 | 21 | 84 | 107 | 300 | 542 | 313 |
| 40mm | 100 | 8 | 11 | 15 | 22 | 54 | 100 | 3 | 2 | 11 | 90 | 44 | 50 |
| 72mm | 200 | 1 | 4 | 7 | 2 | 3 | 18 | 1 | 1 | 1 | 5 | 10 | 5 |
| 84mm | 100 | 1 | 4 | 7 | 3 | 6 | 35 | 1 | 1 | 1 | 9 | 11 | 6 |
| 122mm.Havoc | 300 | 1 | 3 | 5 | 1 | 2 | 12 | 1 | 1 | 1 | 3 | 7 | 4 |
| 120x570mm | 150 | 2 | 4 | 7 | 4 | 5 | 33 | 1 | 1 | 1 | 8 | 11 | 5 |
| 155mm.Standard | 450 | 1 | 8 | 11 | 14 | 5 | 55 | 1 | 1 | 5 | 5 | 15 | 35 |
| C4 | 250 | 1 | 2 | 4 | 3 | 2 | 27 | 1 | 1 | 1 | 6 | 7 | 5 |
| IED | 300 | 1 | 1 | 2 | 1 | 1 | 12 | 1 | 1 | 1 | 3 | 5 | 1 |
| M67 frag grenade | 100 | 1 | 8 | 13 | 3 | 6 | 35 | 1 | 1 | 1 | 9 | 19 | 10 |
| Claymore | 150 | 5 | 11 | 15 | 15 | 36 | 67 | 2 | 2 | 11 | 60 | 44 | 100 |
| AT mine | 300 | 3 | 6 | 8 | 8 | 18 | 34 | 1 | 1 | 6 | 30 | 22 | 50 |
| Molotov | 40 | 19 | 40 | 57 | 55 | 133 | 125 | 7 | 25 | 40 | 113 | 163 | 375 |

Changes against round 36 (`round36-combat.md` section 2), which used only the single-tag entries: it ignored the sub-calibre entries that stack with the rocket entry (`Explosive.Rocket.120mm` is `-50%` on top of the rocket `+650%`), so its 120 mm rocket counts were low (Sandbag Wall 1, Bunker 23 become 2 and 33 here). The M67 frag grenade carries `Meta.Damage.Explosive.Rocket.60mm` in its source context (`explosive-actors.json`), so the rocket entries apply to it under the matching rule (Sandbag Wall 1 hit, not 8). The tracked-vehicle entry is a flat `Add` (500 or 1,000 per hit depending on the structure, 8 structures).

### Rewards for destroying and building (found while closing B11 and the buildable challenge rows)

`DT_ChallengeRewards_SessionEvents_Buildables` (plugin `Rewards/BuildableRewards`), base cash / Role XP before the alignment, zone and assist modifiers:

| Row | Cash | Role XP |
|---|---:|---:|
| Destroyed: FOB | 2,500 (+ up to 7,500 by the FOB's supplies, 25,000 supplies = full bonus) | 500 |
| Destroyed: Hot Zone Magnet | 2,750 | 700 |
| Destroyed: Phalanx | 1,200 | 300 |
| Destroyed: Mortar, MistralAA | 650 | 175 |
| Destroyed: Bunker, Gate, Crow's Nest, Air Raid Shelter, Loudspeaker, Refuel and Repair Station | 200 | 50 |
| Destroyed: SV Shelter | 250 | 65 |
| Destroyed: Door | 100 | 25 |
| Destroyed: Bremmer Wall 30, Gate Ramp 85, Quad Wall 75, Tall Hesco 20, Tank Trap 20, Hesco 15, Sandbag Wall 15, Wood Base 15, Radio 20, Barbed Wire 5, Camo Net Tent 5 | as listed | 5 to 20 |
| Damaged | 0 base | none |
| Building (per hit) / Finished | 5 / 0.5 | 1 / 0.25 |
| Build supplies deposited (owner / interactor) | 0.5 / 0.4 per supply | 0.1 per supply |
| Build supplies consumed (owner / instigator) | 1.4 per supply / 1,500 | 0.1 per supply / 250 |
| Schematic placed | 10 | none |
| FOB hacked / FOB door closed / FOB owner payed | 1,000 / 75 / 1 | 0 / none / none |

The row lookup is `DT_RewardLookup_SessionEvent_BuildableDestroyed` (36 rows, all with a reward row). The destroy states (`ST_Challenges_SessionEvents_Buildable_BuildableDestroyed` and `_Assist`) take their tag through that lookup.

## Progression and economy

| # | Row | Status | Result |
|---|---|---|---|
| P1 | Shop price modifiers: apply as percent of price? | NATIVE (open) | Data fits percent of price: Faction rows 0 (signature rifles free), Level 50 (half price at Wardog level 8 or below), LosingFaction 80, FirstPurchase 90, `RefundModifier` 0.9. The applying code is not located. Structs (SDK): `FWDEntityPriceModifier` is a class with a vtable at +0, `EntityTarget` +0x08, `Data` array +0x10, `Multiplier` float +0x20; subclasses `_Level` (LevelType +0x28, Role tag +0x2C, LevelRequirement +0x34, Level +0x38), `_FirstPurchase` (RequiredTag +0x28), `_LosingFaction` (ScoreDifference +0x28), `_Faction`. `UWDEconomyConfig.PriceModifiers` is at +0x38. Searched: the whole corpus for `0.01f` (two hits, both in the damage evaluator `0x6BB6FB0`), the economy subsystem and component vtable bodies (`0x188B000..0x1898800`: no `/100`, `*0.01`, `0.9`), the global of the tag `Vendor.Discount.FirstPurchase` (registration `0x1271930`, global `0x14D3693D0`: no code reads it by name; the tag is only data for `RequiredTag`). Next step: find the `FWDEntityPriceModifier` vtable through the struct ops table at `0x4CE9B930` (registration thunk `0x69C4B70`) and read its virtual method that returns the modified price. |
| P2 | Refund modifier 0.9 consumer | NATIVE (open) | Class `UWDPlayerRefundComponent` exists (alias `UWDPlayerRefundComponent_VFT` in the corpus); its methods were not read. Same next step as P1. |
| P3 | Skill unlock level and cost, skill points | SETTLED | `round36-econ.md` section 4 (ABSENT: no skill in any unlock table; skill points are reserved tags). |
| P4 | Skill effects that have data | SETTLED | All 62 skill rows with display names, GameplayEffect modifiers and curves: `game-features/Wardogs_Progression_v1.md`; the 68 nodes without an effect row have only a name and description (`round36-econ.md` section 4). |
| P5 | Skill curve time axis | NOT WORKED | Deferred. |
| P6 | Role XP curve: running total or step | FOUND | Cumulative threshold. `DT_RoleMasteryDefinitions` level `XP` values are strictly increasing (Infantry 200, 750, 1,250, 3,000 ... 5,132,500) and each role has one running attribute (`Attribute.Meta.XP.Role.<Role>`); the backend struct `Pragma_Content_LevelDefinition` has `Level` and `XP` (int64). The last step is 239,650 while the level-100 value is 5,132,500, so a step table would put 5.1 million XP into one level against reward rows of 5 to 750. All six role rows are identical. |
| P7 | Role levels to Wardog level | ABSENT | Searched `Content/Meta/Levels` (only `DT_RoleMasteryDefinitions`), the tag list (`Attribute.Meta.XP.*` has Role and Platform only, no Wardog or total), `DT_MetaTree_Roles` Wardog tree (MinLevel gate, no MetaId). The Wardog level is not computed from any client table; it is a server value (the tree upgrade request is checked by the backend). |
| P8 | Role XP thresholds "absent" | SETTLED | Outdated backlog text: the table exists (`round36-econ.md` section 7, 101 rows x 6 roles). |
| P9 | Platform mastery | SETTLED | `round36-econ.md` section 1. |
| P10 | Achievement rewards | SETTLED | `round36-econ.md` section 2 (no reward but the Steam achievement). |
| P11 | Gold Bar price and rate | SETTLED, SERVER | `round36-econ.md` section 5. |
| P12 | Gold Exchange rate history, season-reset conversion | SETTLED, SERVER | `round36-econ.md` sections 5 and 6 (`DT_ExchangeDefinitions` empty; `EndOfSeasonCashValue` and `RewardedGoldBars` in the response proto). |
| P13 | Intel | SETTLED | `round36-econ.md` section 5 (no spend path). |
| P14 | Starting cash conflict | FOUND | `DT_CurrenciesDefinitions` (`Content/Meta/CurrencyDefinitions`): `Attribute.Meta.Currency.Cash` `InitialBalance` 10000, `Attribute.Meta.Currency.GoldBars` `InitialBalance` 0. A session can override it (`WDGameModeSession.OverrideStartingCash` -1 = use this default, `round40-modes-ai-other.md`). The Progression page is right; the Currencies page is wrong. |
| P15 | Cash and Gold Bar carry-over | SETTLED, SERVER | `round36-econ.md` section 5. |
| P16 | Season definitions empty | SETTLED | `round36-econ.md` section 6. |
| P17 | Season dates and names | SETTLED, SERVER | `round36-econ.md` section 6. |
| P18 | MH-6 Black and Gold expiry | SETTLED | `round36-econ.md` section 6: `ExpirationTime` 2026-12-31 00:00 UTC, type 1; enforcement is server-side. |
| P19 | Taxi skin, AK74 Black and Gold, Paper/Rock/Scissors emotes, faction/grenade/helmet vehicle skins, bobbleheads, A-91/M17S/KH-2002 weapon skins, cosmetics not on the Gold Market, skin and emote prices and rarity | SETTLED, ABSENT | `round36-econ.md` section 6: only two routes exist in the client (Gold Market `PurchaseCollectionItem`, backend `GrantCollectionItems`/order fulfilment); items with no Gold Market row can only come from the second route or from outside the client, which cannot be told apart statically. No price or unlock field exists on the cosmetic rows (`DT_Cosmetics_Season01_*`). |
| P20 | Wagers: settlement and payout, death/leave effect, multi-objective bonus, offer rule, unlock level | SETTLED, SERVER | `round36-econ.md` section 3 (counts, odds, limits found; settlement is backend). |
| P21 | Challenge tier value unit; tips | FOUND | The tip rows are formulas on a runtime value: `Challenges.Rewards.SendTip` is cash `0 - TipAmount` and `ReceiveTip` is cash `+TipAmount` (`TipAmount` is a game value). The per-action tip tags (`Tip.Heal`, `Tip.Repair`, `Tip.Refuel`, `Tip.Revive`, `Tip.PlayerDelivered`) have no row of their own: the amounts come from the action's reward, so the unit is cash. |
| P22 | `Challenges.Rewards.*` tags without a row (44 pairs) | FOUND | The tool that produced the old count scanned only the `DT_ChallengeRewards_SessionEvents_*` tables. Seven reward tables exist (Shared 298 rows, EndOfMatch, Buildables, HotZoneMagnet, Spotting, TeamOffence, Crowbar; 486 rows). Of the 54 distinct `Challenges.Rewards.*` tags the challenge state trees name, 37 have a row. The other 17: 7 are base tags that the lookup registries expand to variant rows (`VehicleDestroyed`, `VehicleDestroyed.Assist.{CrewAssist,FOBSuppliedAssist,LogisticAssist,ReviveAssist}`, `DestroySupplyCrate`, `RepairVehicle`; every one of the lookup tables' reward tags has a row); 5 are `Tip.{Heal,Repair,Refuel,Revive,PlayerDelivered}` (P21); `Buildables.BuildSuppliesDeposited` has the `.Owner` and `.Interactor` rows; 4 have neither a row nor a lookup that was found: `Assist.VehicleDestroyed`, `Assist.VehicleDestroyed.DamageAssist`, `Spotting.Refreshed`, `ZoneEntry.SpawnVehicle`. |
| P23 | KOTH challenge reward amounts | FOUND | The KOTH rows' own `Rewards` lists are empty because the KOTH state trees use the same shared reward tags as every mode (41 tags): 26 have a row in `DT_ChallengeRewards_SessionEvents_Shared`, the vehicle, heal, revive, repair and supply-crate tags resolve through the KOTH lookup tables to the same variant rows. Base values (cash / Role XP): player kill 300 / 250; revive with the defibrillator 600 / 250 (resuscitator 500 / 250); heal with a bandage 200 / 80 (med kit 40 / 50); repair with a standard wrench 5 / 2.5; destroy a Kodiak 250 / 150, a Heavy tank (TNK_01) 5,500 / 750, a Havoc 7,000 / 500; destroy a free supply crate 150 / 150; passenger survived 500 / 100; player delivered 100 / 12.5. All multiplied by the same zone, kill-streak and last-victim terms as the other modes (`assets/data/zone-rewards.json`). The wiki's "Not in data" for KOTH is wrong. |
| P24 | Team Offence challenge rewards | FOUND | `DT_ChallengeRewards_TeamOffence` (not in the earlier tool's glob): `Challenges.Rewards.TeamOffence.Forgive` is cash 500 flat. `Challenges.Rewards.TeamOffence.Punish.Kill` is not cash: it is a points tag, `clamp((5 + DamageContribution) x CauseMultiplier, 1, 5) / HalvingDivisor`; `DamageContribution` 0, cause multipliers: Claymore kill 0.1, environment kill 0.1, explosive kill 0.8, headshot, sniper and precision-artillery kills 1.0, default 1.0; the divisor is 2.5 when the kill was flagged (`Challenges.Context.TeamkillFlagged`). So a punished team kill is worth at most 5 points, 2 when flagged. The tag is the same one `Challenges.Rewards.TeamkillPunish` describes ("points expression, not a currency grant"). No XP row. |
| P25 | Team Offence Punish / Voter descriptions | ABSENT | Both `WDChallengeDefinition` rows have `Description` `CultureInvariantString` null and an empty `Rewards` list; names are "Team Offence Punish" and "Teamkill Voter". The reward is the P24 row granted by the state trees. |
| P26 | Team Offence vote outcomes | FOUND (structure), NATIVE for the message handling | The Voter state tree has states Idle, Answered (children Reward and NoReward), Closed, Active (children Waiting, Decide, ForgiveByLeave, Done). `Reward` runs `Calculate Forgive Reward` and `Grant Reward` (the 500 cash); `NoReward` runs `Stamp Reject Reward`, a record update only. A condition `Vote Was Reject` and `Reject Cooldown Elapsed` choose between them. `ForgiveByLeave` listens for `WDSafeZoneLeftMessage` and records a ballot vote "Forgive By Leave": the voter leaving the safe zone before deciding records a forgive. "Voter expired" matches the `Gave Up` condition; the vote-notice handling code itself is not read. |
| P27 | Buildable challenge rewards | FOUND | `DT_Challenges_SessionEvents_Buildables` has zero challenge rows, but the rewards live in `DT_ChallengeRewards_SessionEvents_Buildables` and are granted by the `ST_Challenges_SessionEvents_Buildable_*` trees: see the table in Buildables. Damaged pays 0 base cash; Destroyed pays the per-structure amounts; Schematic Placed pays 10. The wiki's "not in data" is wrong. |
| P28 | Buildable reward inputs: producers and ranges | NATIVE (open) | `BuildProgress`, `BuildSuppliesDeposited`, `TotalFOBSupplies` (cap 25,000 in the formula), `LastVictimCount` are state-tree game values written by native code. Next step: the game-value provider of `WDSessionEventsCalculateRewardTask` (look up the class from the task instance data `WDSessionEventsCalculateRewardTaskInstanceData`). |
| P29 | Spotting Role XP and target amounts | FOUND | `DT_ChallengeRewards_SessionEvents_Spotting` (130 rows: 65 `Added`, 65 `Removed`). Role XP base: `Added` 5 to 100 (ATMine 5, Valkyra spawn vehicle 100), `Removed` (the spotted target destroyed) 5 to 500. Cash base: `Added` 5 to 1,000, `Removed` 10 to 5,000 (Havoc 5,000). Examples: `Added.Player` cash 100 / XP 25 (refreshed spot 50 / 12.5); `Removed.Player` cash 400 / XP 150; `Removed.Havoc` 5,000 / 250. Alignment factors: friendly 0, neutral 0.25, hostile 1; zone factors 1 (added) or control 2, hot zone and magnet 4 (removed). |
| P30 | Spotting a Player target | FOUND | The rows exist: `Challenges.Rewards.Spotting.Added.Player` and `Removed.Player` (the old text said no lookup row; the Player rows are direct, not through a lookup). |
| P31 | `DestroyedByTeamModifier` / `KilledByEnemyFactor` | FOUND | A penalty. Selector: when `Challenges.Context.KilledByEnemy` is set, cash is multiplied by `KilledByEnemyFactor` 0.25; Role XP uses `KilledByEnemyReward` instead of the base (Player 75 instead of 150, Havoc 125 instead of 250: half). Zone and faction values are in the same table (P29). |
| P32 | Hot Zone magnet Role XP | FOUND, ABSENT | `DT_ChallengeRewards_SessionEvents_HotZoneMagnet`: `MagnetActivated` cash 2,500 / Role XP 500; `TowerCaptured` cash 250 (hostile x6 = 1,500 by the factor) / Role XP 100 (hostile 300); `MagnetDeactivated` cash 2,500, no Role XP resource (ABSENT). |
| P33 | Passive mission Time Played interval | NATIVE (open) | The state tree `ST_Challenge_TimePlayed` waits with a Delay task whose `Duration` is bound to the state parameter `UpdateInterval` (Double). The Double value sits in the property-bag value bytes of `DT_PassiveMissionChallenges` (`TimePlayed.1` to `.5`: descriptors RequiredAmount Int32, Objective Struct, UpdateInterval Double, TimePlayed Double; SerialSize 28). The 28-byte block is identical in all five tiers and contains one double 5.0 (`00 00 00 00 00 00 14 40` at its end); which of the two doubles it is, and the layout in front of it, is not verified, so no value is claimed. Next step: decode the bag with the layout of `FInstancedPropertyBag` (value order and alignment), or read `RequiredAmount` of two tiers to anchor the offsets; package bytes are in `E:/Reverse_Engineer/wardogs_analysis/round36_econ/out/passive.bin`. |
| P34 | Reward zone and faction factors | SETTLED + FOUND | Shared PlayerKill: ControlZone 5, HotZone 10, HotZoneMagnet 10, Friendly -3, Revenge 2, KillStreakStopped 1.5, TargetFriendly zone 2 and 4, LastVictim reduction 0.24 (max 4 victims), kill streak value 50 (max 5). Also on `assets/data/zone-rewards.json` and the zone rewards doc. |
| P35 | Factory Investment name | FOUND | `DA_FactoryInvestment_01` `DisplayName` "Zaystev Foundry" (the earlier text was cut off by the export). Description: "The Zaystev Foundry is the most reliable and consistent Investment to get specific items from over the season and save cash." Cost 200 cash, type Passive. Map icon texture `T_UI_Icon_FiringMode_FullAuto_White_256` (also the fallback icon). |
| P36 | `QueueSize`, `SlotAmount`, recipe discount, build time unit | FOUND (partly) | Curves in `CT_Factory_UpgradeValues` (constant steps, rank 1 to 5): `QueueSize` 5, 10, 15, 20, 20; `StorageSize` 5, 10, 15, 20, 20; `SlotAmount` 1, 2, 3, 4, 5. The investment asset uses `QueueSize` for each of the three lines and `StorageSize` for storage; `SlotAmount` is not referenced by the asset. The discount 20 is percent: the production cost of the four recipes that are also sold equals 80% of the vendor price (AK74M 640 of 800, M4 2,240 of 2,800, MP9 1,100 of 1,375, Super-45 4,480 of 5,600); `bOverrideProductionCost` false. `RecipeDuration` 10 (all six recipes): the unit is not stated and no consumer was found (the module `FactoryInvestmentRuntime` has no UFUNCTION; `UWDFactoryInvestment` vtable `0xBC7C280`, slots `0x88F13A0`, `0x88F2030` not read), so seconds stays an inference. |
| P37 | Factory display name and icon | FOUND | See P35 (`SourceString` present in the asset; icon is a texture path). |
| P38 | Emergency Resuscitator route, Halftrack Backpack route | ABSENT | Not worked beyond the earlier search; no vendor, loot or tree row names them (`round36-econ.md` section 7 unlock lists carry no entry). |
| P39 | Hidden vendor items (`bShowInVendor` false) | NOT WORKED | Deferred. |
| P40 | Vendor `LevelToUnlock` consumer | NOT WORKED | Deferred. |
| P41 | First-spawn starting items | NATIVE (open) | Unchanged from `round12-spawn-provisioning.md` (`0x6784010`, `0x6BD5860`, `Server_ApplyLoadout`). |
| P42 | Exchange, season and debug/mock investments empty or test-only | SETTLED | Not player data. |

## Wiki updates

- `_wiki/progression-and-economy/king-of-the-hill-challenges.md` and the KOTH rows in `team-offence`-style tables: "Not in data" for cash and Role XP -> the base amounts of the shared reward rows (player kill 300 / 250, revive 600 or 500 / 250, heal 200 / 80, repair 5 / 2.5, Kodiak 250 / 150, Heavy tank 5,500 / 750, Havoc 7,000 / 500, free crate 150 / 150, passenger 500 / 100, delivered 100 / 12.5); say the amounts are the same as in other modes and the "worked out during the match" wording is replaced by the formula terms.
- `_wiki/progression-and-economy/team-offence-challenges.md`: Cash "Not in the data" -> Forgive (the voter's decision) pays 500 cash; Punish gives 1 to 5 points (5 at most, 2 when the kill was flagged, 0.5 for Claymore and environment kills, 4 for explosive kills), not cash; no XP. `_wiki/game-modes-and-maps/team-offence.md` line 35 and line 28: reward amounts as above; "forgive by leave" -> leaving the safe zone before deciding records a forgive; "voter expired" -> the voter gave up.
- `_wiki/progression-and-economy/buildable-challenges.md` (lines 35 to 40): "not in data (match score only)" -> destroyed-structure cash and Role XP per structure (FOB 2,500 + up to 7,500 and 500 XP, Magnet 2,750 / 700, Phalanx 1,200 / 300, Mortar and Talon 650 / 175, Bunker, Gate, Crow's Nest, shelters, Refuel and Repair Station 200 / 50, Door 100 / 25, walls 15 to 85, barbed wire 5); damaged 0; schematic placed 10; building 5 per hit.
- `_wiki/progression-and-economy/spotting-challenges.md` (lines 16, 26, 27): Role XP "Not in the data" -> Spotted 5 to 100, Spotted Target Destroyed 5 to 500 by target (Player 25 and 150); a target destroyed by the enemy pays 0.25x cash and half the Role XP; Player targets have their own rows.
- `_wiki/progression-and-economy/hot-zone-magnet-challenges.md`: Role XP -> Magnet Activated 500, Tower Captured 100 (300 hostile); Magnet Deactivated pays cash 2,500 and no XP.
- `_wiki/progression-and-economy/currencies.md` (line 56): "starting balance not in the data" -> Cash starts at 10,000, Gold Bars at 0 (`DT_CurrenciesDefinitions`); a mode can override it.
- `_wiki/progression-and-economy/factory-investment.md` (lines 16, 31, 32) and `game-features` factory page: full name "Zaystev Foundry" and its description; production discount 20 is percent (recipe cost is 80% of the shop price); queue size steps 5, 10, 15, 20, 20 and storage 5, 10, 15, 20, 20 over five ranks; build time unit still unconfirmed.
- `_wiki/progression-and-economy/{assault,driver,pilot,recon,medic,support}.md` and `cash-and-rewards.md` (line 142): role XP values are cumulative totals needed to reach the level.
- `_wiki/equipment/*.md` structure pages (door, gate, bunker, recon tower, recon tent, shelter, indirect fire shelter, Hesco walls, sandbag wall, wood base, FOB, Builder's Radio, barbed wire, refuel and repair stations): hit counts for rifle, sniper, .50, cannon, rocket, C4, IED, grenade, Claymore, mine and Molotov sources from `assets/data/structure-hits.json`; replace the four-source bound; 120 mm rocket counts go up (Sandbag Wall 2, Bunker 33).
- `_wiki/equipment/refuel-and-repair-stations.md` (line 72): "no single IED entry" -> the IED does 300 per hit through the Utility explosive entry; Refuel Station 6 hits, Repair Station 1 hit.
- `_wiki/equipment/mg-nest.md` (lines 18, 34) and `_wiki/guides/building-guide.md` (line 89): MG Nest gun 600 rounds/min, range 1,000 m, 60 rounds per magazine, 8 s reload; no target list in the data.
- `_wiki/equipment/vanguard-ciws.md` (line 49): a full 500-round magazine lasts 16.7 s of continuous fire; 3 s reload.
- `_wiki/equipment/builders-radio.md`, `forward-operating-base.md`: do not state that the FOB cannot take damage; the `DoNotTakeDamage` field is unread data. Building speed pages: one hit per swing loop, 0.567 s (small, medium hammer), 0.883 s (large) as a derived figure.
- `_wiki/equipment/loudspeaker.md`, `mortar`, `talon`, `phalanx` pages: add the destroy rewards; keep "function not in the data" for the loudspeaker.
- `_wiki/progression-and-economy/passive-missions.md` (line 32): leave "not in the data" (value not verified).
