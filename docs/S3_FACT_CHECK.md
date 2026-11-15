# S3 article fact-check

This check uses the saved CL533731 / hotfix533689 exports in Git data tree `592912092880ffb3e02a5a8e9f5e4b6e79bc8116`. It checks the articles as well as the generated tables. Updating the export snapshot did not, by itself, update every example, explanation or historical assumption in the wiki.

The current check is **partial**. A corrected article can still contain unchecked claims. A matching generated table verifies a calculation against its inputs, not the current game's native implementation or server settings. The review records keep those distinctions explicit.

## Official-note reconciliation

The [official S3 announcement](https://store.steampowered.com/news/app/1867240/view/688648135317127221) is now cross-checked against the wiki. The [122 overlapping announcement-to-page mappings](S3_OFFICIAL_CROSSCHECK.json) record values, units and targets; that is a mapping count, not a count of unique changes. Vehicle variant prices, reverse speeds, parachute guidance, equipment weights, unlock levels, reward changes, ping policy and drop packages retain their stated approximations and source scope.

All **411 current unlock nodes** are displayed across the six role articles and the Wardog table. All **nine Twitch Drop packages** were reconstructed and checked, including each watch threshold, item and quantity. The Wager Vendor is explicitly removed; its saved configuration is retained for comparison. Limited Mode, Sabatulo and Twitch Drops have dedicated pages.

The announcement's broad Wardog tank-level statement differs from individual saved nodes; those values are preserved separately. Three announced achievement additions are distinguished from the saved table's ten-to-fourteen growth. Black & Gold Littlebird carryover is an announced two weeks, while the retained config date does not prove availability. Catch-up percentages and several new reward amounts are unspecified and remain unknown.

The [coverage record](S3_FACT_CHECK_COVERAGE.json) accounts for **421 pages**: the original 418 plus three additions. **226 current pages changed**. Review remains **285 partial, 21 navigation-only and 115 unread reference/model pages**. Those categories are deliberately separate from the official-note reconciliation; no substantive page is admitted as wholly current-native verified. Public page hashes bind canonical Git content, while private evidence preserves the Windows working-copy byte identities and preimages.

## Corrections made

| Topic | Correction | Evidence and limits |
| --- | --- | --- |
| M4 armor examples | Upper torso: 30.8 HP without armor, 15.4 with Heavy. Middle torso: 28.0 / 14.0. Lower torso: 26.6 / 13.3. | [Current hit-location model](../assets/data/weapon-damage-locations.json), point blank, FMJ, historical damage formula with S3 inputs. These body parts are distinct. |
| DMR caliber factors | .308: 0.85→0.91; 7.62×54: 0.80→0.90. | [Current caliber rows](../data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json); the earlier values remain historical. |
| Role progression | Stored XP at levels 10 / 50 / 100: 36,750 / 1,950,000 / 6,600,000. Seven trees contain 411 nodes. | [Economy model](../assets/data/economy.json) and [raw role definitions](../data/Wardogs/Content/Meta/Levels/Roles/DT_RoleMasteryDefinitions.json). Stored thresholds are distinct from a verified cumulative-XP consumer. |
| Gold Exchange | The current level-35 node stores a 100,000 cost, replacing the guide's old 150,000. | [Current role tree](../data/Wardogs/Content/Meta/CharacterSkills/DT_MetaTree_Roles.json). Activation and server overrides are separate questions. |
| Shop discounts | Removed the unsupported level-8 50% discount and the derived 45% price. | [Price modifiers](../assets/data/price-modifiers.json). An omitted multiplier stays unknown; earlier percentage interpretations are conditional. |
| Passive missions | The 15 reward entries store an invalid reward type and disable automatic activation. | [Economy tables](../assets/data/economy.json). Listed goals and quantities do not establish that Intel is currently awarded. |
| Ghillie protection | Applied-effect references are present; their effect definitions are missing from this corpus. Omitted armor stages/coverage do not establish zero protection. | [Hit-location model assumptions](../assets/data/weapon-damage-locations.json). Its no-armor treatment is an assumption. |
| Loudspeaker | Corrected the claim that it had no buildable data. Its saved definition includes cost 200 and health 1,000. | [Loudspeaker article](../_wiki/building/loudspeaker.md). Its effective function remains unverified. |
| Stingray | Distinguished zero stored initial inventory from restock supplies 900 and a cash-associated field 5,000; removed the invented one-drone restock default. | [Stingray article](../_wiki/building/stingray.md). Field consumers and the reload state machine remain open. |
| Vehicle hull figures | Included the main-body ×0.5 factor in affected helicopter, Kodiak, Humvee, Dune Buggy, Ural and Wolf examples and comparison pages. | [Vehicle hit-location model](../assets/data/vehicle-hitboxes.json), with historical damage-rule assumptions; these are not measured S3 damage values. |
| Helicopter seats | Little Bird and ROT_04 rows store −40% for small/medium arms and −17.5% for high arms, replacing the articles' −25% / −15% examples. | [Current seat-reduction rows](../data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json). Current application remains a consumer question. |
| Refuel Station explosives | Corrected the model's IED count from six to one after combining applicable modifiers. | [Structure-hit model](../assets/data/structure-hits.json). Selection, stacking and health calculations retain their historical formula assumptions. |
| Effective range | A table's range marker does not define a damage cutoff. The damage calculation uses its separate falloff curve. | [Weapon comparison](../_wiki/weapons/weapon-comparison.md); historical flight formulas remain model assumptions. |
| Recoil and omitted defaults | Weapon tables now read S3 authored recoil settings; TCX-SPR's ten-shot model climb is 12.6°, previously 15.9°. The S1/S2 viewer remains historical. Omitted RPM, accuracy, range and spread values retain explicit historical-default assumptions. | [Weapon generator](../_tools/wiki_weapons.py). All 61 ordered current patterns were checked against raw fields; one differs from the retained S2 model. This does not establish current native aim displacement. |
| Weapon unlock fields | Current role prerequisites are displayed separately from vendor level fields: for example AMR 50 Recon 41 and Verba Support 8. | [Current unlock nodes](../assets/data/economy.json). An absent matching node is unresolved, rather than treated as unrestricted access. |
| Bow hub | Replaced the hard-coded 160 m/s with current initial/typical settings, 240/204 m/s under the cm/s assumption. | [Compound Bow](../_wiki/weapons/compound-bow.md). The official +50% announcement and the separate weapon/projectile fields do not identify a measured release speed. |
| Historical citations | Pinned 204 raw-data links in archived S1→S2 pages to the saved S2 revision. | Historical figures are preserved; those citations no longer follow changing `main` data. |

## What remains separate

The saved S2→S3 comparison is a literal comparison of exported values. The old original containers were not independently reparsed. It does not identify every effective gameplay change.

Current native damage, armor wear, spread, recoil, charging, reward and feature-activation behavior requires current consumers and defaults. Historical meshes and reference poses remain CL516586 evidence. Water-field meanings and all 90 wager categories remain unresolved. Three UI packages still fail extraction, with five warnings overall; the complete-extraction gate has not passed.

The [S3 update record](SEASON3_UPDATE.md) describes the published snapshot and reproducible comparison. Independent reviews found seven integration defects and two later source/encoding defects; each was repaired with retained preimages, source-coordinate fixtures or targeted regression checks. Current model generation, source/link checks and publication verification are separate from the outstanding native and reference-review obligations.
