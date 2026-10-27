# Round 91, teammate itm: item extensions, placeables, Molotov selection, Medical Bag steps

Backlog items V5-02, V5-03, V5-04, V5-05 of `BACKLOG-v5.md` (census v5, `round90-census-v5.md`). Static work only: the exported `ID_*` and `DT_GlobalDamage_*` JSON under `data/Wardogs`, and the Blueprint listings from round 86 (`E:/r86/work/bp/lst`, produced with WdExtract and `tools/cue4parse_extractor/kismet_listing.py`, method in `round86-bp.md`). No Elytra-protected code touched; the game was not run.

## Status per item

| Item | Part | Status | Result |
|---|---|---|---|
| V5-02 | `WDInventoryFragment_Armor.DamageContextTag`, 14 pieces | FOUND | Table of piece, tag, covered hit locations, durability and every rule row (`DT_GlobalDamage_InfantryData` and `_ArmorData`) that names the tag. Level 2 Helmet, Pilot Helmet and Tank Helmet are named by no rule. ItemShop section 9.1. |
| V5-02 | `Throwable.bDropOnInterrupt`, `ItemToConsume` | FOUND | `bDropOnInterrupt` false on 14 of 16 throwables (the two frag grenades do not set it); C4 trigger consumes `Id.Item.C4Explosive`, IED trigger consumes `Id.Item.IED.Explosive`. Section 9.2. |
| V5-02 | `RangedWeapon.bDropAfterUse`, `FireChargeTime` | FOUND | Only `Id.Item.Launcher_04` (9K333 Verba): true, 0.5 s. Section 9.3. |
| V5-02 | `RangedBow` | FOUND | Full draw 1.4 s, wait before completion 0.33 s, draw FOV shift type `ActiveCurve`, curve keys 0 : 0, 0.25 : 0, 0.5 : 1.02. Section 9.3. |
| V5-02 | `Appliable` extras | FOUND | Only Enox (animation tag, play-before-consume true, `DecayHealAmount` 40) and the two resuscitators (consume animation tag) set them. Section 9.4. |
| V5-02 | `Keycard` faction and number | FOUND | Six cards. Data oddity: `Bravo.1` carries number 2 (same as `Bravo.2`). Door table: ABSENT (no reader or door names a card; round 75). Section 9.5, wiki `keycards`. |
| V5-02 | `Droppable` box-extent override and `ThrowingForce` | FOUND | 45 items override the box; `ThrowingForce` 300 only on the Large Hammer. Section 9.6. |
| V5-03 | Placeable ext, 4 assets | FOUND | Start and max health 1 / 1 on AT mine, Claymore, IED; 100 / 100 with lifetime 20 s on the ammo crate; collision sizes, blocked classes, `bCanPlaceOnOtherPlaceable` false. Fire page 5.1b. `Items_v2` 268 and 485 rewritten. |
| V5-03 | Fuel Can `Trace Distance` 500 | FOUND | Bytecode confirms the use: one line trace from the eye point along the view for 500 cm in `B_Action_FuelCan_Refuel.CheckDistance` and `B_Action_FuelCan_ReFill.DistanceCheck`. The 20 L can exports the item id `Id.Item`. |
| V5-03 | Repair Tool `ChargesToUse` | FOUND | 1 on the heavy and light drills; the wrench sets no field. Where the number is read is native (not traced). |
| V5-03 | Hammer `DismantleTraceDistance` 275, critical-spot manager | FOUND | Large and Medium 275, Small unset; spot distance 340 (Large) and 290 (Medium, Small); 135 degrees; build amount 8 / 5 / 3. Buildables section 3. |
| V5-03 | Binocular `TrackingBoundsDiameter` 350 | FOUND | 350 on all four optics; `bShowDistance` false on binoculars and monocular. Spotting 7c. |
| V5-04 | Molotov friendly and self damage | FOUND (Derived) | Documented selection run over every `DT_GlobalDamage_*` table for source `Meta.Damage.DamageType.Enviroment`: 0 kept entries match. The two Friendly entries need `Bullet` and `LargeHammer` sources. So no rule changes the 15 per tick against enemy, teammate or thrower; the fire loop has no team or owner test either, so the thrower is hurt. Caveat: the source container is assumed to hold only the passed damage tag (the native builder `0x6F09210` was not re-read). Not covered: any game-mode friendly-fire switch, and the character damageable refusal tag (O-12). |
| V5-05 | Medical Bag application steps | FOUND | Looping timer with period `HealOtherDuration` (1.5 s when healing a teammate), first step after 1.5 s; each step heals 15 and spends 2 durability once, only when the heal returned more than 0; a step that heals nothing on a full target ends the use. Self-heal the same with 35 / 5 s / 25. Revive: single event, 10 durability spent in both faction cases, `GE_Player_RessedByEnemy` applied when the factions differ, wheel time 6.5 s (Derived). |
| V5-05 | What happens at 0 durability | SERVER / native | The "until item empty" stop is inside the native action layer; `Auth_ReduceDurability` is a native stub. Not traced. |
| any | Elytra-protected code | PROTECTED | Not touched. |

SERVER marks: `ForceHandleApplication` runs only when `HasAuthority()` (server); on a client the step does not heal, it only checks whether the target is full. The Molotov damage call also runs on the server (fire field replicated, damage authoritative).

## Method

Item fields: `_tools/item_extension_tables.py` reads every `ID_*.json` with `weapon_vendor_tables.exports()` and prints per extension type. Item names come from `item_shop_tables.Ctx`.

Medical Bag: `B_Action_MedKit_MultiUse` listing (functions `CalculateProgressWheelInteractionTime`, `DoTimedApplication`, `HandleApplication`, `ForceHandleApplication`, `OnInteractionFinished`, `BP_OnCancel`) and `B_Action_Appliable_Base` (`OnInteractionStarted`, `OnInteractionFinished`, `ConsumeItem`). Key reads:

- `OnInteractionStarted` offsets 262 to 575: `K2_SetTimerDelegate(DoTimedApplication, Select(UpdateTime, ProgressWheelInteractionTime, UpdateTime > 0), looping true, initial delay 0)`.
- `MedKit_MultiUse.CalculateProgressWheelInteractionTime` offset 593: `SelectFloat(A = HealOtherDuration + ReviveOtherHealthAmount / HealOtherAmount x HealOtherDuration, B = HealOtherDuration, pick A when bIsReviving)`.
- `HandleApplication` offsets 108 to 333: `ForceHandleApplication`, then `Auth_ReduceDurability(HealOtherDurabilityCost)` only after it succeeded; the end test at 688 to 1011 (`current health >= max health` then `OnInteractionFinished`) is reached only when the heal failed.
- `EWDAppliableInteractionTimeMethod`: 0 AnimationLength, 1 UntilItemEmptyOrTargetFull, 2 AnimationNotifier (SDK `WDGame_structs.hpp`). The Medical Bag uses 1 with `bUseAppliableProgressWheel` false, which `OnInteractionStarted` routes to the timer branch (offsets 124 to 262).
- `OnInteractionFinished` (MultiUse, reviving branch): `RevivePlayer(...)`, then `AreActorsOfSameFaction`; the false branch applies `GE_Player_RessedByEnemy` and both branches flow back to `Auth_ReduceDurability(ReviveOtherDurabilityCost)`.

Molotov: `B_Molotov_FireField` listing (`TryDamagePlayer`, `OnActorsArrayLoop`), `pipelines/Wardogs_DamagePipeline_v2.md` sections 4 and 6, `pipelines/Wardogs_HitRegistration_v1.md` section 6.4 (alignment), and the rule tables. The selection was executed by the generator block `molotov` (counts per table, section 4.1 of the Damage Pipeline).

Side finding (Data): `ST_Challenges_SessionEvents_TeamOffencePunish` state "Environment Kill" tests the cause tag `Meta.Damage.DamageType.Enviroment` and adds `Challenges.Context.EnvironmentKill`; the "Barbed Wire Kill" state completes immediately. What the context does to the punishment was not traced.

## Update pipeline (for the lead)

```
python -I _tools/item_extension_tables.py --write    # blocks item_ext * in ItemShop, FireAndUtility, Buildables, Spotting, Medical, DamagePipeline
python -I _tools/item_extension_tables.py --check
python -I _tools/medical_tables.py --write           # worked-example rows for the Medical Bag now count steps
```

`_tools/pipeline_registry.json` does not exist on this branch, so the new generator is listed here only.
