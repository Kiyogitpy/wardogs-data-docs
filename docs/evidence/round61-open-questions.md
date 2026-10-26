# Round 61: nine open wiki questions (R61-RE)

Static analysis only. Nothing was run. Evidence levels: cooked data read (JSON under `data/` and `assets/data/`), extractor dump of cooked packages (`WdExtract dump`, `findname`), static disassembly and decompiled-corpus reading (RVAs, image base 0x140000000). Method as in rounds 57 to 59. Extractor output and helper scripts are under `E:/Reverse_Engineer/wardogs_analysis/round61_re/` (`wd.sh` wrapper, `helm3/` pilot and tank helmet cue dumps, `cbm/` and `cbm2/` audio mixes, `cb/` control buses, `lastvictim.py`, `spotbase.py`, `spot_base.json`, `arr378.py`, `f85eeb80.c`). No protected (virtualized) code was devirtualized; where a call lands in a stub that the protection layer left empty it is marked PROTECTED.

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1 | Spotting pay drop per repeat | FOUND | Own rule: 50% less per repeat, up to 2 repeats (third spot pays 0). Kills: 24%, up to 4. |
| 2 | Pilot helmet muffling and highlight | FOUND (muffling); NATIVE (highlight is an on/off tracker switch, no strength) | Helicopter seat: vehicle volume 0.501 (-6 dB), low-pass 0.4. Elsewhere: low-pass 0.45 (0.5 own weapon). |
| 3 | Factory "slot amount" | NATIVE (value lookup PROTECTED) | Native code makes that many slots per production line; the investment asset gives it no upgrade. |
| 4 | Max restock shorter when nearly full | NATIVE (time consumer not located) | The request path never reads or scales a time; inferred: full time. |
| 5 | Infantry Only and unarmed vehicles | FOUND (no reader of the rule) | The rule is a server-browser label only; unarmed packs are not disabled, so they can spawn. |
| 6 | Sight zeroing default | FOUND | Default and reset value is the sight's minimum zeroing range (metres). |
| 7 | A-91, KH-2002, Bushmaster M17S at price 0 | FOUND | Free from the weapon vendor to the matching faction, level 1, limit one per life. |
| 8 | Stingray firing table vs the L81 | FOUND (unused); ABSENT (cause) | No widget, Blueprint or located code reads the Stingray table; no file says why it is longer. |
| 9 | "Not yet known" sections | see section 9 | 4 items settled, the rest stay open with reasons. |

## 1. Spotting repeat reduction

Table `DT_ChallengeRewards_SessionEvents_Spotting` (130 rows: 65 `Added` = spot, 65 `Removed` = spotted target destroyed; cash and Role XP resource each). Every cash and Role XP expression is `(1 - clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier) * (...)`. The row variables (script `lastvictim.py`):

- Spotting: `LastVictimCountMax` **2.0**, `LastVictimReductionMultiplier` **0.5** (the selector `LastVictimReductionModifier` -> `LastVictimReductionMultiplier`), all 130 rows.
- Kills for comparison (`DT_ChallengeRewards_SessionEvents_Shared`, PlayerKill and vehicle section rows): max **4.0**, modifier **0.24** (this is the "24%, up to four repeats" of the wiki).
- Other shared rows: heal rows 10 and 0 (cash) or 0.1, 0.2, 0.025 (XP, with max 10, 5, 40); refuel and repair rows 40 and 0.025.

So the third and later spot of the same kind of target pays factor `1 - 2 x 0.5 = 0`. `LastVictimCount` comes from the state tree `ST_Challenges_SessionEvents_KOTH_Spotting_Added` (and `_Removed`): tasks `Track Target Repeat Count`, `Resolve Repeat Action Count`, `Get Repeat Actions Cooldown` with `RepeatActionsCooldown` **180.0** (the same value in every kill, heal, revive, repair and refuel tree). A cooldown of 180 s most likely restarts the count (inferred from the name; the task itself is native and was not read). Which targets count as "the same kind" is therefore also native and not read.

Also read: base payouts (`spot_base.json`): `Added.Player` cash 100 / XP 25, refreshed 50 / 12.5; `Removed.Player` cash 400 / XP 150; spot cash 5 to 1,000, destroy cash 10 to 5,000. These differ from the "match-score" table figures 15 to 275 and 50 to 500 already on the page; the page now says the files do not show which table pays. Status FOUND (cooked data read).

Pages: `_wiki/game-mechanics/spotting.md`, `_wiki/progression-and-economy/cash-and-rewards.md`.

## 2. Pilot helmet

`ID_PilotHelmet` carries two Gameplay Effects: `GE_PilotHelmet_Active` (ongoing while `State.Player.Vehicle.Rotary` with role Driver or Gunner; grants `State.Player.Armor.PilotHelmet.Active`) and `GE_PilotHelmet_Passive` (ongoing whenever Active is not; grants `...Passive`). Each state has a cue (`GC_Player_Armor_PilotHelmet_Active` / `_Passive`, dump `helm3/`). The cue Blueprints do nothing but send a Crosstalk audio event: `Audio.Event.Player.State.Helmet.Pilot.Active.Start` / `.Stop` and `...Passive.Start` / `.Stop`. The events (`AE_Helmet_Pilot_*`, under `Content/Audio/Events/Gear/Helmets/Pilot/`) each run `AEB_ActivateControlBusMix` on a sound control bus mix (local only). The mixes (`Am_CBM_Pilot_Helmet_Active` and `_Passive`, under `Content/Audio/AudioModulation/ControlBusMixes/`, dump `cbm/`), attack and release 0.1 s on every stage:

| Mix | Bus | Target value |
|---|---|---:|
| Active | `AM_CB_VehicleMain_LPF` (low-pass frequency) | 0.4 |
| Active | `AM_CB_VehicleMain_Vol` (volume) | 0.501187 (= -6.0 dB) |
| Passive | Weapons1p LPF | 0.5 |
| Passive | Weapons3p, Whizby, Impact, VehicleMain, Footsteps 1p and 3p, Ambience, Ambience Rain, Dialogue 1p and 3p LPF | 0.45 each |

The buses use `SoundModulationParameterLPFFrequency` (control bus `AM_CB_VehicleMain_LPF`) and `SoundModulationParameterVolume`. The LPF parameter is a normalized 0 to 1 value in the engine's modulation system; the Hz it maps to is in the engine parameter, not in these files (inferred: 1 is unfiltered). Comparison (`cbm2/`): Tank Helmet Active LPF 0.6 (vehicle), volume 0.630957 (-4 dB), footsteps 3p LPF 0.6, tinnitus volume 0.501187, weapons 3p LPF 0.7; Tank Helmet Passive is the same list as the Pilot Passive.

The highlight: `State.Player.Armor.PilotHelmet.Active` is a native tag (string `0xB34F460`, registration `0x1290D10`, tag cell `0xD36B8A8`). Package search (`findname`) shows only the helmet item, two cues and two effects name it, so no Blueprint reads it. Its native reader is `0x720B1B0` (vtable slot 90 of `UWDUISpatialTrackersViewModel`, vtable cell `0xB502918`): it asks the pawn's ability component whether it has the tag (virtual call at offset 24, argument `qword_14D36B8A8`); with the tag (or the other condition `0x1476C89F0`) it runs a periodic update (interval from the data object at `this+856`, default 0.25 s) calling `0x720C0B0`, which does a box overlap query of actors (half extent `data+240` x 0.5, default 100000 cm) and updates the on-screen trackers; without the tag it clears them (`0x1472083E0`). So the highlight is an on/off switch for the HUD target markers; there is no strength value. Naming it "highlights target vehicles" is the shop text; which actors the query keeps was not read (NATIVE). Status: FOUND (muffling values, static data), NATIVE (highlight).

Pages: `_wiki/equipment/pilot-helmet.md`, `_wiki/equipment/tank-helmet.md`.

## 3. Factory investment slot amount

`CT_Factory_UpgradeValues` rows (`QueueSize`, `SlotAmount`, `StorageSize`; round 42 P36). `DA_FactoryInvestment_01` binds upgrade tags `Meta.Investment.Upgrade.Factory.ProductionLine{One,Two,Three}QueueSize` and `...StorageSize` to the `QueueSize` and `StorageSize` rows; no tag is bound to `SlotAmount`. The tags `...ProductionLine{One,Two,Three}SlotAmount` exist in the executable (strings `0xBC7B888`, `0xBC7B8C8`, `0xBC7B908`; registrations `0x1529820`, `0x1529BE0`, `0x1529A00`; cells `0xD3F5B28`, `0xD3F5B30`, `0xD3F5B38`).

Native readers of those cells (`riprefs.py`): the `UWDFactoryInvestment` constructor `0x88F0970` (puts all seven upgrade tags, three slot amounts included, into a map at `this+0x98` with level 1) and `0x88F2030`. In `0x88F2030` the loop over the production lines (count at `this+336`) picks the line's SlotAmount tag, calls `0x1563030` for the value `n`, and appends `n` 16-byte entries to the line's list (`line+16`, stride 16). So a slot amount is the number of entries in a line's list. The call target `0x1563030` is `xor eax, eax; ret` in the restored image (the real body is not present in the readable code), so the value that comes back cannot be read: PROTECTED. With the asset not binding the tag, inferred slot amount 1 per line. Status NATIVE (meaning inferred as slots per line); value lookup PROTECTED.

Page: `_wiki/progression-and-economy/factory-investment.md`.

## 4. Max restock time when nearly full

`Server_RequestRefuelOrRepair` -> `0x85EEB80` (round 41 R41-8; decompilation saved as `f85eeb80.c`). The function computes `pool`, `amount`, `fraction`, supplies charged and cash charged from the share restored, then creates the 80-byte record (`amount` float at `+24`, supplies at `+28`) and sends it to the pawn's action queue (`0x144552A20`) together with the row's cue tag (`*(row+32)`, the `RestockingCueTag` of `FRestockData`). It never reads `FRestockData.RestockTime` (`row+8`) nor derives a duration from `fraction`; `MaxAmount` (`row+0`) is not read either. The UI function `0x8600760` and the fraction helper `0x85FBFB0` read the same table only for cost and amount (no time). `FWDFobTakingResourceData` (SDK) has `RestockTime` (`+0x2C`) and `RelativeRestockAmount` (`+0x34`) fields, but no Blueprint names them (`findname`: 0 packages). Where the time is applied was not located (it may sit in the cue or an action). Inference: nothing in the request path shortens the time for a smaller share, so a Max restock takes its stored time. Status NATIVE (consumer not located).

Pages: `_wiki/building/refuel-and-repair-stations.md`, `_wiki/vehicles/fuel-and-refueling.md`.

## 5. Infantry Only and the unarmed vehicles

`Config/Experiences/KOTH_InfantryOnly.json`: `DisabledGameFeatures` = TNK_01, ROT_02, ROT_03_WeaponVariants, WHL_05_Minigun, STN_01, STN_02, STN_05, TNK_04, ROT_04_MachineGun, WHL_02_RingTurret, WHL_05_RingTurret, WHL_07_ArmouredBattle, WHL_08_RingTurret; `FeatureFlags` = `Experience.Rules.InfantryOnly`. The unarmed vehicle packs (WHL_01, WHL_02, WHL_05, WHL_06, WHL_07, WHL_08, ROT_03, ROT_04 base) are separate game features that are not in the list.

The tag `Experience.Rules.InfantryOnly` is a native tag (string `0xB34A8B8`, registration `0x12809B0`, cell `0xD36AB50`) declared with the description "Marks the experience as Infantry Only; mapped to a server-browser descriptor tag." The cell has two references only: its registration and the cleanup `0x99F5C73`. Nothing reads it. (Same for `Hardcore`, cell `0xD36AB58`.) Package search: only `DT_ExperienceServerBrowserTags`, `DA_ServerBrowserEntry` and `DA_PopupData_ServerInfo` name it. So no code blocks vehicle spawns on the rule; only the disabled feature list acts. Status FOUND (static; the removal of the disabled features itself is engine feature handling, not read).

Page: `_wiki/game-modes-and-maps/hardcore-and-infantry-only.md`.

## 6. Sight zeroing default

`UWDWeaponComponent` (current zero distance at `+0xF8C`; constructor `0x6B8E675` writes -1). `ResetZeroingDistance` (exec thunk `0x6B994C0`, native body `0x6B97560`): gets `GetZeroingRange(component)` through the owner interface (vtable offset 224, returns the `FInt32Interval` min and max) and calls `SetZeroingDistance` (`0x6B97310`) with the **minimum**; the setter clamps to the interval and stores at `+0xF8C`. `Increase` and `DecreaseZeroingDistance` (`0x6B991E0`, `0x6B98F80`) call the same setter. `0x6C9A6A0` handles an unset weapon: when the stored value is -1 it silently sets it to the range minimum (`0x6B971A0` shape, `0x6B97310` with notify false). So the default is the sight's minimum zeroing range. Unit: round 40 item 34 (`0x6B96820`: distance = range x 100 cm), i.e. metres. Data: `MinZeroingRange`/`MaxZeroingRange`/`ZeroingStep` in the weapon stats and sight modifiers (SDK `WDWeaponStats` `+0x160/+0x164/+0x168`); sights set the minimum to 10 to 100. Status FOUND (static).

Pages: `_wiki/game-mechanics/ballistics.md`, `_wiki/attachments/sights-and-optics.md`, `_wiki/guides/choosing-attachments.md`.

## 7. A-91, KH-2002 and Bushmaster M17S at price 0

Vendor tables `DT_WeaponVendor_EXT_AR_04` (A-91), the KH-2002 and WEPN_033 tables under `Plugins/GameFeatures/Weapons/Platforms/`: each row has `bFactionSpecific` true, `Faction` Bravo (A-91), Charlie (KH-2002), Alpha (WEPN_033), `Price` 0, `LevelToUnlock` 1, `LifeTimeBuyLimit` 1, `bShowInVendor` true, `bIsPreviewOnly` false, no required item, no account entitlement. Across all 35 weapon vendor rows these three are the only faction-specific rows and the only ones with a buy limit (the others have 0). `price-modifiers.json` also gives each of them a faction price modifier of 0 for the same faction. The Emergency Resuscitator uses the same field (1) and its shop text says "one per life", so the field means one per life. Factions are named Lonestar (Alpha), Valkyra (Bravo), Manticore (Charlie) on the factions page. So a player of that faction gets the rifle free from the weapon vendor. Whether the vendor hides the row from other factions was not shown (inferred). Status FOUND (cooked data read).

Generated pages were changed through the generator `_tools/wiki_weapons.py` (new `FACTION_WEAPONS` map from `price-modifiers.json`), then regenerated: `_wiki/weapons/a-91.md`, `kh-2002.md`, `bushmaster-m17s.md`. Page: `_wiki/guides/making-money.md`.

## 8. Stingray firing table

`WE_STN_05_Heavy_MainBarrel.ArtilleryRangeData` (`WDVehicleWeaponExtensionDataAsset` `+0x378`). Table values: `_tools/artillery_range_tables.py` (17 rows; travel times equal the L81's, distances 13 to 38 m longer from -500 to 200 mrad). Readers: `findname ArtilleryRangeData` and `findname ImpactDistance` over every package match only `W_STN_03_Reticle` (mortar) and `W_Artillery_Reticle` (SPH-2). The STN_05 package list contains only `DT_VehicleCrosshair_STN_05` for "Reticle". Round 36: the Stingray has no reticle widget with a table. `DA_Drone_ProjectileData` has no guidance block and the drone is a player-flown camera projectile (round 59), not an arc shell. A native reader of `+0x378` was looked for (`arr378.py`: many hits for the offset pair across the executable, since the pattern is common; none in the weapon and vehicle ranges was tied to the Stingray extension), and none was found that is tied to the Stingray, but the scan is not an exclusion (NATIVE reader not excluded, as in round 58 item 4). The cause of the longer distances is not stated by any file (ABSENT). Status FOUND (unused as far as read); ABSENT (cause).

Page: `_wiki/building/stingray.md`.

## 9. "What is not yet known" sections

| Page | Item | Status | Result |
|---|---|---|---|
| hit-registration | slow connection settlement | SERVER | Decided on the servers; the page now says it is not in the game files. |
| hit-registration | own-vehicle setting for every projectile | FOUND | `IgnoreInstigatorVehicleTime` is 0.5 on 20 of 36 projectile assets (18 of 34 `*ProjectileData` plus `DA_20x102mm` and `DA_TVGuidedMissile_Data`); absent (off) on 308, 338, 45 ACP, 45 Colt, 50 AE, 50 Cal, 5.45, 5.56, 7.62 x 51, 7.62, 7.62 x 54, 12 g slug, 7 mm buckshot, 9 mm, battery charge, combat arrow. Per ammunition type, not per weapon. |
| penetration-and-ricochet | speed kept after a bounce per material | FOUND | `assets/data/weapon-penetration.json` `config.surfaces[].restitution`; added as a column on the page. |
| penetration-and-ricochet | penetration 2 or more and ricochet | FOUND | Ricochet chance is multiplied by `t = clamp((effectiveness - X) / (Y - X), 0, 1)`, effectiveness = capacity / thickness, with the packed values effectiveness 2 or more gives 0 (pipeline section 4.3, `0x6F36600`). The page now says so. |
| penetration-and-ricochet | thickness unit; materials of world walls | ABSENT | Unchanged. |
| movement | acceleration units; slow-walk scale; plain sprint stamina | open | Not settled. The stance values 7, 12, 19 with friction 6.0 and `MaxStopSpeed` look like a Source-style unitless acceleration factor, but the movement code was not traced; slow-walk consumer and sprint cost need the Mover native path (NATIVE, not read this round). |
| status-effects | suppression feel; friendly fire for fire | open | Needs play or a rule outside the damage tables; not reachable statically in this round. |
| spotting | repeat reduction; player spot payout | FOUND | Section 1. |
| spotting | spot timings in play; base payout for all targets | open | Timings need play. The full per-target base list is in `spot_base.json`; the page gives the player rows and the ranges. |
| aim-assist | units of range and reticle sizes; pull feel; why RPG-7 is off | open / ABSENT | No unit in the data; feel needs play; no reason stated. |

## Wiki updates

- `_wiki/game-mechanics/spotting.md`: repeat rule 50% per repeat up to 2; player base pay; unknowns trimmed.
- `_wiki/progression-and-economy/cash-and-rewards.md`: spotting repeat rule pointer.
- `_wiki/equipment/pilot-helmet.md`, `_wiki/equipment/tank-helmet.md`: audio mix values, active and passive states, highlight is on or off.
- `_wiki/progression-and-economy/factory-investment.md`: slot amount meaning (inferred).
- `_wiki/building/refuel-and-repair-stations.md`, `_wiki/vehicles/fuel-and-refueling.md`: Max restock keeps its time (inferred).
- `_wiki/game-modes-and-maps/hardcore-and-infantry-only.md`: unarmed vehicles can spawn.
- `_wiki/game-mechanics/ballistics.md`, `_wiki/attachments/sights-and-optics.md`, `_wiki/guides/choosing-attachments.md`: default zero is the minimum zeroing range, metres.
- `_tools/wiki_weapons.py` and regenerated `_wiki/weapons/a-91.md`, `kh-2002.md`, `bushmaster-m17s.md`; `_wiki/guides/making-money.md`: faction rifles are free from the vendor.
- `_wiki/building/stingray.md`: range table is unused.
- `_wiki/game-mechanics/hit-registration.md`, `_wiki/game-mechanics/penetration-and-ricochet.md`: section 9 items.
