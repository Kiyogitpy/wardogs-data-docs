# Round 39: Medical, status and movement gaps

GitHub-only evidence page (docs/ is not on the site). Backlog sections "Medical & status" and "Movement & player" of the round 38 backlog.
Statuses: FOUND, NATIVE, SERVER, ABSENT, plus NOT SEARCHED where the timebox ran out (stated, never guessed).
Evidence levels: **cooked data read** (exported JSON or package bytes), **bytecode read** (Blueprint Kismet bytecode from `WdExtract dump`, rendered with the round 20 decoder), **static disassembly / decompile** (restored exe, corpus `decompiled_cl516586_20261017_mmvpuc__`, image base 0x140000000, RVAs), **Derived**. The game was not run; no devirtualization.

Method. `WdExtract` (round36_ai/bin) `list ""` for the package list, `findname Wardogs <tag>` to find which packages carry a gameplay-tag name (tags are FNames in the name map; unversioned property names are not, so `findname` proves "no asset uses this tag" but not "no asset sets this property"), `dump` for B_Action_* Blueprints under `E:/Reverse_Engineer/wardogs_analysis/round39_med/`, then the corpus `functions` table for RVAs. Generated data: `python -I _tools/round39_medical_tables.py --write` writes `assets/data/medical-status-r39.json` and the spot-time table on the Spotting page.

## Counts

| Status | Count |
|---|---|
| FOUND (includes partial and derived readings, each labelled) | 17 |
| NATIVE (partial: Enox decay amount, revive hold/penalty fields, armour weight default) | 3 |
| ABSENT (Medic skill nodes incl. Enox/defibrillator/IFAK skills, IncreaseBleedTime, natural regen outside Deathmatch) | 6 |
| SERVER | 0 |
| NOT SEARCHED (timebox) | 23 |

49 backlog items: 27 medical and status, 22 movement and player.

---

# Medical and status

## M1. Bandage: where the +35 HP is applied. FOUND
`ID_Bandage` appliable action data has `InteractionTimeMethod` = `AnimationLength`, `Notifier` None (cooked data read). `B_Action_Appliable_Base.CalculateTotalInteractionTime` sets `TotalInteractionTime` to the montage length; the action then waits `WaitForSimulationTime(TotalInteractionTime)` and its `Completed` handler calls `OnInteractionFinished`, which calls `HandleApplication` (bytecode read). `HandleApplication` does `ModifyBase(Health attribute, AttributeValue 35, delta)`. So the heal lands once, at the end of the use montage (5.2333 s self, 4.8333 s teammate), not at a notify. Item kit with a `Notifier` (IFAK) uses `GetAnimationNotifyPosition` instead; that is the earlier `Heal` notify reading.

## M2. Medic skill magnitudes (19 of 23 nodes). ABSENT
Searched: `DT_MedicSkills` (4 rows only), `CT_MedicSkills` (6 curves), all `DT_*Skills` and `DT_Skills_*` plugin tables, `WdExtract findname Wardogs` for every one of the 19 tag names (`HealTime`, `BuffDuration`, `ChargeTime.Defib`, `ReduceUsage.Defib`, `StunResistance`, `LessSuppression`, `IncreaseBleedTime`, `HealthierRevive`, `ReviveSpeed.Standard`, `MedicBag`, `MedkitUsage`, `ReducedFalldamage`, `ReviveDamageReduction`, `DragSpeed`, `MedicalItemWeightReduction`, `BuffApplicationTime`): only the UI text tables (`DT_CharacterSkillNodes_Data`, node presets) carry them; and a string scan of the exe: no `Meta.Role.Medic.*` string (only `Meta.Skill.Character`, `.Item`, `.Revive.Instigator`, `.Revive.Target`, `.SupplyCrate`, `.Vehicle`). Result: no client asset or native string reads these nodes, so no number exists in the game files. Whether the server applies them is unknown (not a SERVER finding: no request/response struct was searched). Also covers Enox "Self-healing speed" (M8), Defibrillator charge/charges-per-battery (M20), IFAK self/teammate heal speed (M21).

## M3. Medical Bag durability and `UsageRateMultiplier`. FOUND (negative)
`Attribute.Gameplay.Item.UsageRateMultiplier` appears in exactly three packages: `ID_MedKit_Standard` (default 1), `DT_MedicSkills`, `GE_Item_UsageRateMultiplier` (findname). No `B_Action_MedKit_*` bytecode reads it, and no exe string exists for it. Durability is spent by `WDItemExtension_MedKit::Auth_ReduceDurability(cost)` (thunk `0x8558A60`, helper `0x6C1D110` subtracts the cost from the stored value, no multiplier) with a fixed cost from the item data: `HealSelfDurabilityCost` in `B_Action_MedKit_SecondaryUse.HandleApplication`, `HealOtherDurabilityCost` in `B_Action_MedKit_MultiUse.HandleApplication` (after `ForceHandleApplication` succeeds), `ReviveOtherDurabilityCost` in `MultiUse.OnInteractionFinished` (bytecode read). So the cost is charged once per application call, and no consumer of the skill multiplier was found: the 1.0 to 0.6 curve does not scale durability in any code read. How many `HandleApplication` calls one "heal other" makes (continuous) is base-class timing and was not traced.

## M4. Adrenaline Pen, second pen during the 60 s. FOUND (native defaults) / Derived
`B_Action_StimPen` has no guard against an active effect; it applies each `EffectsToApply` entry (`GE_UnlimitedTacSprint`, Stacks 1) through `ApplyEffect` (bytecode read). `GE_UnlimitedTacSprint` sets no `MaxStacks` or stack policies; the `UBHGameplayEffect` constructor `0x5225C60` gives `MaxStacks` = 1, `StackDurationRefreshPolicy` = 0 (`RefreshOnSuccessfulApplication`), `StackExpirationPolicy` = 1 (`RemoveSingleStackAndRefreshDuration`), `Duration` = 0 (static disassembly, enum names from `BHGameplayEffects_structs.hpp`). **Derived:** a second pen keeps one stack and restarts the 60 s.

## M5. Adrenaline Pen on a teammate. FOUND
PrimaryUse (teammate) and SecondaryUse (self) both list `GE_UnlimitedTacSprint` x1 with no custom magnitude; teammate use requires `State.Player.Vitality.Alive` on target and owner (cooked data read). The action applies the effect to `TargetCharacter` via its `BHGameplayEffectComponent`. So a teammate gets the same 60 s unlimited tactical sprint plus the weight step-down tag; nothing extra.

## M6. Item-switch speed skill coverage. FOUND
`DT_MedicSkills` row `MedicalItemSwapSpeed` requires item tag `Item.Context.Medical` (`ItemApplicationRequirements.RequireTags`). Items carrying that context (scan of every `ID_*`): Medical Bag, Bandage, Individual First Aid Kit (`Id.Item.SuperBandage`), Defibrillator, Emergency and Field Resuscitator, Stim Pen. The Enox does not carry it.

## M7. Enox decay rate. NATIVE (partial)
Re-read: `Auth_CharacterHeal` `0x6B168B0` starts a looping timer with period `DecayRate` (+0x16C = 5 s); the callback `0x6B16EC0` subtracts `fabs(sub_1452311D0(a1+320, ...))` from the pool (+0x17C). `0x52311D0` is a gameplay-attribute evaluation helper (weak-pointer attribute handle, `[rdi+rbp*8+0x28] + delta`), not a read of `DecayMagnitude`. `DecayMagnitude` (+0x170) has no reader in `0x6B16000-0x6B19000`. So the period is confirmed (5 s) but the amount per tick is not: the "5 HP every 5 s" reading stays **Derived and unconfirmed**.

## M8. Enox "Self-healing speed" skill. ABSENT (see M2).

## M9. Resuscitators: health after revive, units used, what ends it. FOUND
The earlier note "the resuscitator Blueprint is the base appliable action" was wrong: `Action.Appliable.Resuscitator.PrimaryUse` uses `B_Action_Resuscitator` (`Enox/Content/Data/ResuscitatorTest/`). Its `OnInteractionFinished` calls `TargetCharacter->RevivePlayer(Instigator, ContextTags(ItemId), Appliable.AttributeValue, Item)` once, then marks the item for consume (bytecode read). `ID_Resuscitator` and `ID_Resuscitator_Standard` both have `AttributeValue` = **10.0** (cooked data read), so a resuscitator revive passes health 10. Container data: 10 units, `UpdateTime` 4.0, `UpdateAmount` 1.0, `InteractionTimeMethod` `UntilItemEmptyOrTargetFull`. `CalculateTotalInteractionTime` (container branch) computes `(TotalModifyAmount / UpdateAmount + 1) * UpdateTime` with `TotalModifyAmount` = `CalculateAmountToFullTarget`, which the base class returns as 0 and the resuscitator does not override: **Derived total interaction time 4 s**, then one revive and the item is consumed; the 10 container units are not stepped through for a revive. Caveat: the chain through `TotalInteractionTime` was read in bytecode, the runtime result was not observed.

## M10. Health after a hand revive and after a resuscitator revive. FOUND
Mechanism (static disassembly): the native `RevivePlayer` implementation `0x6E75620` takes the health in `xmm3` (saved to `xmm6`) and calls `ResetHealth` `0x6B16E80` with it at `0x6E75AD6`. `ResetHealth`: if the value is 0 it loads `DefaultHealthToReviveTo` (+0x160 = 25), then sets the Health attribute through `0x5236DE0` (`SetNumericValue`-style). The hand revive (`UWDReviveInteractionContext`, vtable slot 91 `0x772D860`) calls character vtable slot 323 (`0x6E75620`) with `xmm3` = its own float at +0x240; the constructor `0x772C5F0` sets that float to `0x41200000` = **10.0**. No Blueprint sets it (`WDReviveInteractionContext` is named only in `B_Action_Revive` as a type and in the shooting-range tutorial). So: hand revive 10, resuscitator 10, Defibrillator 35, Medical Bag 50, and 25 only if a caller passes 0. This corrects the earlier reading that the base revive used the 25 default.

## M11. `CriticalReviveHoldThreshold` and `BleedOutRevivePenaltyOffset`. NATIVE (partial)
`CriticalReviveHoldThreshold` (+0x970): read once, by `0x6E69D20` (the downed-player interaction setup), which passes it as the hold threshold of the revive interaction context (`UWDReviveInteractionContext`, built by `0x772C270`); `HealHoldThreshold` (+0x974) goes the same way to the heal context. So it is the hold time (seconds presumed) of the revive interaction: 20 in data (native 2), consistent with `B_Action_Revive.ReviveHoldTime` 20. `BleedOutRevivePenaltyOffset` (+0x988): only the constructor writes it in `0x6E00000-0x6F00000`; the bleed-timer start `0x6E75540` uses +0x980, +0x984 and the +0xA70 counter only. No reader found: unresolved.

## M12. `IncreaseBleedTime` and `HealthierRevive`. ABSENT (see M2).

## M13. `GE_Player_RessedByEnemy` apply site. FOUND
`B_Action_Resuscitator.OnInteractionFinished` applies `GE_Player_RessedByEnemy` to the target when `AreActorsOfSameFaction(target, instigator)` is false (bytecode read). The same action sets `State.Player.Action.Appliable.Reviving.Enemy` instead of `.Friendly` when the factions differ. The effect: 60 s, granted tag `State.Player.RessedByEnemy` (ge-values.json; the previous page spelled the tag `RessedByEnemy`). So a resuscitator can revive an enemy and the revived enemy carries the tag for 60 s. The item's own context is `Appliable.Context.ReviveFriendly`; whether targeting an enemy is reachable depends on interaction rules not traced.

## M14. Infantry natural regeneration outside Deathmatch. ABSENT
Searched: `UWDVitalityComponent` constructor `0x6B81720` (RegenDelay 10 only), damage path `0x6B82520` (broadcasts the `RegenTimer` delegate only), the whole `0x6B16000-0x6B19000` vitality range for health adds (only `Auth_Heal`), and every game-feature `AddComponents` list for a regen component (only `WDHealthRegenComponent`, in Deathmatch). No tick adds health to infantry outside Deathmatch.

## M15. Deathmatch regeneration rate. FOUND
`UWDHealthRegenComponent` constructor `0x848B5F0`: `HealthToRegenerate` (+0xE8) = **5.0**, `TickInterval` (+0xEC) = **1.0** (also in round 17 native defaults). The Deathmatch feature adds the component directly (`GameFeatureAction_AddComponents` to `WDMoverCharacter`), no Blueprint override. `OnRegenTimerStarted` `0x84965F0` stores `RegenDelay` (10 s) plus world time. **Derived:** 5 HP per 1 s tick after 10 s without damage. The tick body itself was not located (searched `0x8485000-0x8497000` for readers of +0xE8/+0xEC).

## M16. Suppression strength. FOUND (partial)
`B_CharacterSuppressionComponent` (WDCharacterComponents) holds four effects (bytecode-export read): Default post-process `PostProcessEffect.Suppression.Default` with `PostProcessingIntensityDecayMultiplier` **0.4**; Concussive `PostProcessEffect.Suppression.Concussive` decay **0.1**; two camera shakes (`B_CameraShake_Suppression`, `B_CameraShake_Suppression_Backblast`). `DT_PostProcessEffects`: Default has `Duration` 0 (driven by intensity), Concussive `Duration` 2.0 s; both use `MI_PP_Damage`. Per projectile: `SuppressionData.BaseSuppression` (0.2 for 9mm and 7mm buckshot, 0.22 45 Colt, 0.32 50AE, 0.9 for 120/122/125/155 mm) with a distance falloff range and one of six `CR_SuppressionCurve_*` curves (all 30 projectile assets are in `medical-status-r39.json`). Not found: the unit of the decay multiplier and how Strength maps to blur or movement. No movement effect from suppression was found in the component.

## M17. Spotted duration. FOUND
Spotter items (`Binoculars_Standard`, `Monocular`, `RangeFinder_Standard`, `RangeFinder_Expensive`) carry `BH_SpottingExtensionData` per target class: infantry `SpotTime` 0.5, `SpotRefreshTime` 1.0, `DecayTime` 30, `PersistentSpotTime` 180; rotary, airplane and wheeled vehicles 0.75 / 1.25 / 60 / 180; tracked 1.25 / 1.5 / 90 / 180; buildables and bases up to 2.5 / 5.0 / 900 to 3600. `CT_ReconSkills` rows `IncreasedSpottedTime` and `IncreasedSpottingDuration`: 1.0, 1.2 (level 2), 1.4 (level 4). The old note "`CT_ReconSkills` outside folder" was stale: it is in `data/`. Units not exported (seconds presumed). Table: Spotting page, `medical-status-r39.json` `spotting`.

## M18. Tinnitus. FOUND (partial)
Audio event `Audio.Event.Player.State.Tinnitus` runs `AEB_SetTinnitusMix` (control-bus mix `AM_CBM_Tinnitus`: low-pass bus target 1.0, attack 0.1 s, release 0.1 s, hold time 1.0 s, persistent, max 3 instances). `AE_Player_State_BackBlast` runs the same behavior with `IsBackBlast` true. `BP_Explosions` names the tinnitus event and `F_TinnitusCameraRadius`. Triggers: a nearby explosion (radius struct, value not exported) and backblast. Total duration depends on the behavior's hold plus release; not a gameplay-state tag. Removal by the Tank Helmet was not traced.

## M19. `State.Player.Vitality.Critical` setter and critical camera curves. NOT SEARCHED
Timebox. Known from earlier rounds only.

## M20. Armour durability for bullets. NOT SEARCHED

## M21. Armour donning and removal time. NOT SEARCHED
(Armour is inventory-slot gear; no action definition seen in the armor plugin listing: `ID_*Armor`, `ID_*Helmet` only. That is a listing, not a search.)

## M22. Armour and helmet weight. FOUND (partial)
Weight fragment values (cooked data read): Level 1 Armor 3.0, Level 2 4.5, Level 3 10.5, Level 4 18.0, Ghillie Suit 1.5; Level 2 Helmet 1.6, Level 3 3.0, Level 4 4.5. Level 1 Helmet, Tank Helmet, Pilot Helmet, Ghillie Headwear each have a `BHInventoryFragment_Weight` with the `Weight` property omitted (cooked as the class default). The class default was not located: the `UBHInventoryFragment_Weight` vtable has three references (`0x6779110` and `0x67793A0` are other fragment classes' constructors, `0x6A9B240` was not read). Status NATIVE (not located).

## M23 to M26. Halligan durability exhaustion; Ghillie suit and protection in damage tables (two items). NOT SEARCHED

## Defibrillator skills, IFAK skills
ABSENT, see M2.

---

# Movement and player

## P1. Crouched and prone acceleration. FOUND
`content/Wardogs_PlayerMovement_v1.md` §1 already lists the stance acceleration modifiers (**Set 7** stand, **Set 12** crouch, **Set 19** prone) and speed modifiers; the wiki page still says "not yet known". Deceleration columns: no per-stance deceleration field in `BHGroundMovementData` was found in the SDK header (not re-searched in native).

## P2 to P5. Stance modifier vtable `+0x470`; sprint, slow walk and ADS combination; movement curve input units; `CRV_LandGunBob` and look-acceleration consumers. NOT SEARCHED

## P6. Leaving a moving vehicle, input unit. NOT SEARCHED (curve 40 to 75 unchanged)

## P7. Parachute fall height and clearance units. FOUND (Derived)
Same pattern as the landing curve: `DA_FallingMovement` speeds and the parachute `VerticalMaxSpeed` 5000 default are on the cm/s scale (5000 cm/s = 50 m/s, a free-fall terminal speed), so the heights 400 and 1000 and the opening distances are most likely cm (4 m and 10 m). Not read from code.

## P8. Parachute damage curve `CRV_ParachutePunishment_Damage`. FOUND
Already on the Player Movement page (695 to 0, 1,700 to 100, linear). The "values not in the plugin" note in the Parachutes page is stale (the curve is under `Content/GameMechanics/Player/PlayerCharacter/Curves/`).

## P9. Parachute Basic max speeds, roll speed, Sport max pull-up stamina. FOUND
`UBHParachuteData` constructor `0x52704B0` (static disassembly, floats decoded): `HorizontalMaxSpeed` **2000**, `VerticalMaxSpeed` **5000**, `HorizontalAcceleration` 0, `GliderAcceleration` 1500, `PullUpDragAcceleration` 800, `TurnAcceleration` 45, `PitchSpeed` 2, `RollSpeed` **2**, `MinPitch` -30, `MaxPitch` 10, `MaxRoll` 25, `SwingForceMultiplier` 20, `MaxPullUpStamina` **100**, `PullUpStaminaUsagePerSecond` 20, `PullUpStaminaRegenPerSecond` 20, `PivotOffset` 150, `OpenDuration` 1, `MinFallHeightBeforeAbleToParachute` 50, `MinHeightOpenParachuteFromGround` 250. `DA_ParachuteMovement_Basic` omits `HorizontalMaxSpeed` and `VerticalMaxSpeed` (so 2000 and 5000 apply) and sets `RollSpeed` 1; `DA_ParachuteMovement_Sport` omits `RollSpeed` (2) and `MaxPullUpStamina` (100). With usage 50/s and regen 30/s, the Sport pull-up stamina is 2 s of full pull-up, refilling in 3.3 s. (Offsets from `BHMover_classes.hpp`.)

## P10 to P18. Other parachute registries, stance camera curves, mover state priority, query tokens, input resolution, action response types, input-to-action mapping, pawn Blueprint values, kit mapping, ping component, critical event tracker, animation PSD data. NOT SEARCHED

## P19. Component settings: suppression strength, death-effect timing, movement-effect parameters. FOUND (partial)
Suppression: see M16 (the component Blueprint is in the paks; the page said it was not in the folder). Death-effect timing and movement-effect parameters: not searched.

## Fall damage and stamina (priority list). FOUND (already on page, Derived units)
Landing damage `CRV_LandingPunishment_Damage` (670 to 0, 875 to 100, 1080 to 200), `LandingDamageType` `WDFallDamageType`. Unit: cm/s on the evidence of the 5000 / 5300 terminal speeds; 670 cm/s is a drop of about 2.3 m at 980 cm/s^2 (**Derived**). The Medic `ReducedFalldamage` node has no data row (M2). Stamina values already on the page (jump 50 of 150 at 50/s, stance pool 100, tac sprint 20/s); the new stamina value is the Sport parachute pull-up pool (P9).

---

## Wiki updates

| Wiki file | Old | New |
|---|---|---|
| `_wiki/equipment/bandage.md` (line 35) | heal lands at a `Heal` notify; application path not traced | the +35 is applied once when the use animation ends (5.23 s self, 4.83 s teammate) |
| `_wiki/progression-and-economy/medic.md`, `_wiki/equipment/medical-items.md` (88), `_wiki/equipment/defibrillator.md` (44), `_wiki/equipment/medical-bag.md` (59), `_wiki/equipment/individual-first-aid-kit.md` (39), `_wiki/equipment/enox.md` (41) | skill size "not in the data" | no number exists in the game files for these 19 nodes and nothing in the client reads them (data and code searched); effect unknown |
| `_wiki/equipment/medical-bag.md` (40 to 42), `_wiki/equipment/medical-items.md` (84) | unknown whether `UsageRateMultiplier` scales durability | no code reads it; durability is charged as a fixed amount (25 self, 2 other, 10 revive) once per application; the "more uses" skill curve does not appear to change it |
| `_wiki/equipment/adrenaline-pen.md` (41) | second pen during 60 s unknown | one stack only; a second pen restarts the 60 s (derived from effect defaults) |
| `_wiki/equipment/adrenaline-pen.md` (54), `_wiki/equipment/medical-items.md` (62) | teammate effect unknown | the teammate gets the same 60 s unlimited tactical sprint; target must be alive |
| `_wiki/equipment/adrenaline-pen.md` (45) | which items the item-switch skill covers unknown | Medical Bag, Bandage, Individual First Aid Kit, Defibrillator, both Resuscitators, Stim Pen (not Enox) |
| `_wiki/equipment/enox.md` (35), `_wiki/game-mechanics/status-effects.md` (70) | decay "5 HP every 5 s" derived | decay period 5 s is confirmed; the amount per tick is still not read from code (keep as derived) |
| `_wiki/equipment/field-resuscitator.md` (35, 36, 46), `_wiki/equipment/medical-items.md` (66), `_wiki/game-mechanics/downed-and-revive.md` (32, 35) | health after revive, units used unknown | resuscitator revive passes 10 health, revives once and uses up the item; hand revive also gives 10; defibrillator 35, medical bag 50 |
| `_wiki/game-mechanics/status-effects.md` (102) | what applies `RessedByEnemy` not traced | applied by the resuscitator when the revived player is on another faction (60 s) |
| `_wiki/guides/beginners-guide.md` (56), `_wiki/equipment/medical-items.md` (78), `_wiki/game-mechanics/downed-and-revive.md` | natural regeneration outside Deathmatch not yet known | no regeneration outside Deathmatch was found in the game code |
| `_wiki/game-modes-and-maps/deathmatch.md` (34) | regen rate not in folder | 5 health per second after 10 s without damage (derived from 5 per 1 s tick) |
| `_wiki/game-mechanics/status-effects.md` (25), `_wiki/equipment/tank-helmet.md` (55) | suppression strength not in the data | each bullet class has a suppression value (0.2 small pistol rounds to 0.9 for 120 mm and larger) that falls off with distance; the screen effect fades at 0.4 of its rate (concussive 0.1, lasts 2 s) |
| `_wiki/game-mechanics/status-effects.md` (58), `_wiki/game-mechanics/spotting.md` (61) | how long a spot lasts not in the data | infantry: 0.5 s to spot, fades over 30 s, kept up to 180 s; vehicles 60 to 90 s; Recon skills x1.2 and x1.4 |
| `_wiki/game-mechanics/status-effects.md` (94) | Tinnitus trigger and duration unknown | triggered by nearby explosions and backblast; a low-pass hold of about 1 s |
| `_wiki/game-mechanics/movement.md` (55, 56) | crouch and prone acceleration not yet known | acceleration set to 7 (stand), 12 (crouch), 19 (prone); deceleration still unknown |
| `_wiki/equipment/parachutes.md` (15 to 20, 58) | units not stated; Basic max speeds and Sport stamina unknown | Basic max speeds default 2000 horizontal and 5000 vertical; Sport pull-up stamina pool 100 (drain 50/s, refill 30/s); heights and speeds are most likely centimetres |
| `_wiki/equipment/medical-bag.md`, `_wiki/game-mechanics/downed-and-revive.md` | hold time of revive | the revive hold time threshold in the player is 20 (data) |

Total wiki updates: 17 rows (some rows cover several wiki files).
