---
title: "Season 3 / 0.3 Changes"
parent: "Patch Notes"
description: "Official S3 balance and progression numbers, current saved-data comparisons, and their evidence limits."
---

# Season 2 → Season 3 / 0.3

| S3 / 0.3 | |
|---|---|
| Observed game build | CL-533731, hotfix 533689 |
| Steam build | 26615518 |
| Compared with | Saved Season 2 CL-516586 exports |
| Current data | 7,082 parsed exports, plus curated config files |
{: .wiki-infobox }

The core reference tables now use the CL-533731 / hotfix 533689 snapshot. These notes compare saved values with Season 2. The [S2→S3 browser](../../season-3-changes/all-changes.md) includes the literal exported-field differences; the [S1→S2 browser](../../season-2-changes/all-changes.md) remains separate.

## Official Season 3 changes

The [developer's Season 3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221), published 11 November 2026, announce the changes below. Announced values and approximate speeds/heights are distinct from measured results or verification of a particular native consumer. The saved-data comparisons later on this page retain their own source and model limits.

**Availability matters:** S3 adds the Sabatulo city map and Limited mode. Limited excludes HP/AP ammunition, level 3/4 armor, attack vehicles, CIWS, Stingray, MG Nest, Drill Rig and anti-tank mines. The Infrared Range Finder leaves the vendor. **The Wager Vendor is removed**; remaining wager definitions are configuration, not evidence of an active S3 earning method.

### Weapons and equipment

| Announced change | S3 value or comparison |
| --- | --- |
| AR/LMG torso damage versus S2 | Upper +13%; middle/lower +3%, with the armor reduction percentages unchanged |
| Unarmored DMR hits | Two body shots; one headshot. Neck remains two shots |
| SVD/BMR-308/M14 against level-3 helmets | Two headshots, previously three |
| Compound Bow arrow speed | +50% announced; stored weapon settings and projectile fields are distinguished in the [bow article](../weapons/compound-bow.md) |
| Basic Parachute price | 500 → 1,250 cash |
| Sport Parachute price | 700 → 2,250 cash |
| Basic practical jump heights | About 100 m recommended; about 60 m may be survivable with a fast reaction; deployment blocked within about 20 m of the ground |
| Sport practical jump heights | About 60 m recommended; about 40 m may be survivable with a fast reaction |
| AMP-9 20-round magazine weight | 1 → 0.3 kg |
| IED / trigger weights | IED 1.5 → 2.7 kg; trigger 1.5 → 0.2 kg |
| Molotov unlock cost | 25,000 → 12,500 cash |

The notes also announce reduced TCX-SPR climb/drift and a prone-recoil fix; Molotov ignition with held-item dropping; a Halligan supply-crate interaction; and altered Sport Parachute controls. These behavioral announcements are not inferred solely from field presence. Current weapon recoil tables now use S3 settings with the historical calculation assumptions, while the older viewer retains S1/S2 history.

### Vehicles and supply drops

| Vehicle | Announced reverse speed, km/h |
| --- | --- |
| Bobcat | 16 → about 25 |
| Kodiak | 33 → about 57 |
| Humvee | 35 → about 57 |
| Dune Buggy | 43 → about 50 |
| Ural | 15 → 27 |
| Wolf-110 | 27 → about 40 |

| Specific variant | Vendor price, cash |
| --- | --- |
| Wolf-110 [M2 Browning] | 7,800 → 6,800 |
| Kodiak [M249] | 6,750 → 6,250 |
| AH-6M Littlebird [Miniguns] | 12,000 → 10,480 |
| Havoc | 28,000 → 26,000 |

Mounted minigun infantry multipliers increase by 50% at the head, 78% at the neck, 64% upper torso, 55% middle torso, 50% lower torso and 56% at pelvis/limbs. AH-6R rocket pods switch from 122 mm to their own 70 mm rockets. The CIWS change limits each 20×102 mm round to one hit per vehicle section and reduces maximum elevation 65°→60°; old multi-hit calculations are not evidence of the new consumer. The announced grenade-launcher fix changes tank-track destruction from one to three hits and engine disabling from three to five–six hits.

Announced approximate safe drop heights change to 35 m for standard and armored supply crates (previously about 60/80 m), and 40 m for pallets (previously about 90 m). Velocity also matters: about 80 km/h at those heights is guidance, not a guaranteed survival boundary.

### Progression, rewards and servers

| Unlock track / item | Level before → S3 |
| --- | --- |
| Assault: C4 / Molotov | C4 4→5; Molotov 13→8 |
| Support: Large Hammer / Verba | Hammer 8→14; Verba 14→8 |
| Recon: AMR 50 | 35→41 |
| Driver: tanks | 20–35→35–50 |
| Wardog: tanks | 145→200 |

Shared armor, backpacks, tactical vests and parachutes become multi-track unlocks. The announced seasonal cadence is roughly three months; role-based catch-up XP and vendor discounts grow week by week. The notes do not specify a universal fixed catch-up percentage. Losing-faction discounts now compare against the leading faction.

The announcement's broad Wardog tank statement should not replace every saved vehicle gate: current nodes list L2A6 at 200, T-72B3 at 155, SPH-2 at 145 and Vanguard AA at 165. The [current unlock tables](../progression-and-economy/currencies.md) retain those individual values alongside the announcement.

Announced cash for destroying L81 Mortar, Talon 9K-SAM, MG Nest or Stingray doubles 650→1,300; CIWS doubles 1,200→2,400. A vehicle kill using your own vehicle within 1,000 m of a control zone earns the full zone reward. The official spotted-target changes are:

| Target | Cash before → S3 |
| --- | --- |
| AH-6M [Miniguns] / AH-6R [Rockets] | 1,000→850 |
| Z20 Lakota [Miniguns] | 1,400→1,200 |
| L2A6 | 3,300→3,000 |
| T-72B3 | 2,400→2,000 |
| Hot Zone Magnet | 1,650→1,500 |

Spotted-target XP becomes 125 for players (was 150), 200 for FOBs (250), 200 for the Hot Zone Magnet (225), and 400 for spawn vehicles (500). Other announced reward changes cover air-vehicle kill streaks, lower-value supply drops, drill-activating fuel deposits and parachuting into enemy FOBs.

Official-server ping limits become 250 ms; community administrators retain their own limits. Squad invitations and join requests each queue up to five. The new seeding behavior supplies some free unarmed vehicles and clears vehicles at match start. These are developer-announced S3 rules, separate from the older subscriber/code searches preserved in the reference pages.

The [article fact-check record](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/S3_FACT_CHECK.md) tracks corrected examples and remaining source/model obligations. The full official article also covers cosmetics, controller bindings, Twitch Drops and fixes; announcement coverage is separate from the literal exported-field diff.

## Weapons and damage rules

| Stored input | Season 2 | S3 / 0.3 |
| --- | ---: | ---: |
| DMR caliber modifier: .308 Winchester | 0.85 | 0.91 |
| DMR caliber modifier: 7.62x54 mm | 0.8 | 0.9 |
| Infantry damage-rule entries | 146 | 168 |
| TNK_01 inner-radius grenade rule amount, each of three rows | -60 | -85 |
| TNK_01 40 mm grenade rule amount, each of three rows | 20 | -65 |

The other eleven archetype-caliber rows compare equal. These caliber modifiers are separate from ammunition base damage: the compared 5.56 mm, 7.62 mm and 9 mm projectile exports remain unchanged, with stored base damage 28, 34 and 22. The compared AK74M, M4 and M249 stats differ only in two aim-sway labels after the two explicitly checked label associations.

The TNK_01 AntiAir, Artillery and Heavy rows each grow from 29 to 31 entries and add Molotov and 70×1060 mm rocket entries. Rule amounts participate in damage selection and calculation; their signs do not directly specify final damage taken.

Current bone-modifier inputs also change the documented damage model. For M4 FMJ at the middle torso, the calculated value is **28.0 without armor and 14.0 with Heavy armor**, compared with 27.2 and 13.6 under the saved Season 2 inputs. The arithmetic uses the previously documented model; the current native consumer and server behavior have not been independently established. See [damage by hit location](../../pipelines/infantry-viewer.md) for the source and model limits.

## Buildables

The root buildable damage table has 19 rows and 401 entries, compared with 20 rows and 422 entries in Season 2. The drill's 22-entry row moved into a separate HotZoneMagnet GameFeature source. Following that declared source gives **20 rows and 423 entries** across the current two tables; the drill is not absent from the exported configuration.

The updated tables account for 32 buildable item definitions and six separately handled stationary-vehicle definitions. The feature's saved references establish where its data comes from; they do not prove mode activation or availability in a match. See [the drill rig](../building/drill-rig.md).

## Progression and coverage

The official notes name three added achievements: He's Behind You, Car Jacker and Slot Machine. The saved table also contains Sound The Horn; its growth is a configuration comparison, not an official count of newly released achievements.

The current snapshot lists **14 achievement entries versus ten** in the saved Season 2 table, with reviewed current condition trees and freshly decoded thresholds. Retained wager configuration lists **11 actions versus four**, and **90 conditions versus 50**. Its kill-count maximum rises **25→50**, and revive-count maximum **50→75**. These definitions remain stored even though the official S3 notes remove the Wager Vendor. The [achievements](../progression-and-economy/achievements.md) and [wagers](../progression-and-economy/wagers.md) articles distinguish current entries from retained, inactive vendor configuration.

All 90 wager-condition rows lack the old `Category` field, so their category remains unknown. An omitted price multiplier also remains unknown rather than becoming an invented default. Listing an entry does not prove that it is offered in every mode or on the current server.

The improved hotfix mapping resolves the earlier six missing-field canaries. The broad pass emits 7,082 files; supplying the parser's pinned ACL dependency resolves all 537 animation-loader failures. Those animations remain intentionally skipped by the extractor. **Three UI packages still fail, with five warnings overall**, so the strict complete-extraction gate remains rejected. Water-grid field meanings and current native consumers remain open.

The reference's current asset tables and calculations are updated, while earlier native findings, meshes and water images retain their explicit historical build scope. The old Season 2 side is a pinned saved export; its original containers were not independently reparsed. These are data-derived notes rather than official release notes or verified live match behavior.

## Selected stored curve comparisons

Three current CurveFloat key sequences were checked against exact packed float32 bytes and complete export boundaries, then compared with saved CL-516586 JSON exports. Current build attribution comes from retained input receipts. The links below pin the saved CL-516586 revision.

| Asset identifier | CL-516586 Time → Value | CL-533731 Time → Value | Key interpolation |
| --- | --- | --- | --- |
| [`CRV_ParachutePunishment_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/8d0d6a9a0a3a0a0170e7ff3929202a92a5b9c12b/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_ParachutePunishment_Damage.json) | 695→0; 1700→100 | 700→0; 900→20; 1200→100 | Linear |
| [`CRV_Challenges_Curves_DeploySupplyCrate_XP`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/8d0d6a9a0a3a0a0170e7ff3929202a92a5b9c12b/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_DeploySupplyCrate_XP.json) | 0→0; 500→0.1; 1000→0.25; 2000→0.5; 2500→1 | 0→0; 100→0.1; 1500→0.25; 5000→0.5; 10000→1 | Constant |
| [`CRV_SteerSpeedVariant_WHL_07`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/8d0d6a9a0a3a0a0170e7ff3929202a92a5b9c12b/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07/Content/Curves/CRV_SteerSpeedVariant_WHL_07.json) | 0→1.425; 21→1; 42.1→0.65; 80→0.5 | Same four complete key records, plus 95→0.5 and 100→3 | Cubic |

The XP curve's key values are unchanged; four input breakpoints move. The parachute curve's old final leave tangent changes from approximately 0.05540166 to 0. The WHL_07 added keys have matching arrive and leave tangents of approximately 0.0004710732 and 0.08496196, respectively, with no tangent weighting. Decimal notation abbreviates stored float32 representations.

These are stored-data comparisons. Historical field interpretation relies on the old mapping and pinned saved exports; old package bytes were not independently reparsed. The current key bodies were independently byte-checked, while native name resolution and build attribution retain their provenance limits. Asset names do not establish input units, consumer calls, effective damage, reward or steering behavior, or live/server activation. These comparisons do not establish full extraction or general schema compatibility. Other mapped field candidates remain unvalidated.

For general earlier-build context, see [Vehicle handling](../vehicles/vehicle-handling.md).

## Mounted asset paths

The saved Season 2 CL-516586 `.uasset` path list contains 66,550 unique paths; the CL-533731 / Steam build 26615518 effective mounted-provider inventory contains 67,689. Comparing exact paths gives **66,222 retained, 328 old-only and 1,467 new-only**. These are path identities, not comparisons of asset bytes: retained assets may have changed, and some different paths may represent casing changes or possible relocations.

The current inventory includes a separate HotZoneMagnet buildable root with 33 new-only asset paths, two new KOTH challenge-related paths, and additional vehicle grip-curve and animation assets. Molotov and Crowbar asset paths also change. These observations do not establish unlocks, handling values, active modes or other gameplay changes.

The current inventory also contains map packages, mostly generated partitions. The saved baseline lists `.uasset` paths only; without a validated old map manifest, map additions and removals are unknown. Package presence alone does not establish that a map is selectable or content is active.
