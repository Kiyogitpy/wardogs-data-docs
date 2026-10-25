---
title: Round 39 modes, AI and other gaps
nav_exclude: true
---

# Round 39: game modes, zones, AI and other gaps (RE39-MODES)

Static CL516586 review. Nothing was run. Native RVAs are for `WardogsClient-Win64-Shipping.restored.exe` (SHA-256 `a5c3db10...0cc37`), read from the decompiled corpus; constructor stores are decoded in `_tools/mode_rules.py` (raw 32-bit value and decoded number are checked there). Extractor output: `E:/Reverse_Engineer/wardogs_analysis/round39_modes/` (`hp/`, `ss/`, `bpd/` package dumps; `cfgc/`, `exc/`, `keep/`, `upall/` config copies). The repository copies are under `data/Wardogs/Config/` and the three plugin `Config/` folders. Machine-readable result: `assets/data/mode-rules.json` (`python -I _tools/mode_rules.py [--check]`).

Statuses: FOUND, NATIVE, SERVER, ABSENT as in the round 36 brief, plus **OPEN** for backlog items this pass did not reach (no search was made; they are listed so the next pass does not assume they were checked).

## New sources found this round

1. **Config files in the paks.** `Wardogs/Config/Experiences/*.json` (the experience definitions: which game features, data layers and rule flags each mode and map turns on), `Wardogs/Config/DefaultMatchState.ini`, `Wardogs/Config/ServerConfigs/ExampleStandaloneServerConfig.ini` (a community-server template with a 72-entry map rotation), and plugin ini files (`ControlZone`, `BaseScenario`, `VehicleUtility`). Obtained with `WdExtract rawfiles Wardogs/Config --copy` and `rawfiles .uplugin --copy`. Round 36 did not read these.
2. **`.uplugin` descriptions.** `HotPotato.uplugin`: "Hot Potato pre-lobby world feature. Enable this to run the hot potato mini-game while players wait in the pre-lobby." This settles what Hot Potato is.
3. **Native constructor defaults** for the match-state classes (`WDMatchState_Playing_KOTH`, `_Deathmatch`, `_SniperShowdown`) and the Hot Potato, server-seeding and stillness components.

## Priority items

### P1. Hot Potato: rules, scoring, teams, match length, win condition

Status: **FOUND** (what it is, scoring, items); **ABSENT** for team sizes, match length and win condition because Hot Potato has none: it is not a match mode.

- `HotPotato.uplugin` (`data/Wardogs/Plugins/GameFeatures/HotPotato/HotPotato.uplugin`): a **pre-lobby world feature**, "the hot potato mini-game while players wait in the pre-lobby". `BuiltInInitialFeatureState: Registered`, `EnabledByDefault: false`. No experience definition in `Config/Experiences` lists `HotPotato` in `EnabledGameFeatures`; the KOTH experience lists `ServerSeeding` ("Enable this to allow server seeding for this game mode"). So the client does not say which experience enables the potato: it is enabled by the server or a game-feature call outside the client files (SERVER for the switch).
- The scoring runs through `ServerSeeding`. `B_HotPotatoComponent` (added to `WDMoverPlayerCharacter`) is a Blueprint subclass of `WDHotPotatoComponent`. Its `BroadcastHotPotatoMessage(PassMultiplier)` bytecode (`bpd`/`hp/B_HotPotatoComponent.json`, `ExecuteUbergraph`): cast the owner to `WDMoverPlayerCharacter`; if it has a valid `PlayerState`, `Amount = 5 * (PassMultiplier * 2)`; broadcast a `WDPreGameLobbyAwardEvent {PlayerState, Amount, ReasonTag = UI.ServerSeeding.RewardReason.Potato}` through the `GameplayMessageSubsystem`. So the award is **10 x PassMultiplier** points for the player the event names. The reason text is "Hot! Hot! Hot!" (`STRINGS_ServerSeeding`).
- `WDHotPotatoThrowable.GetPassMultiplier` and `WDInventoryFragment_HotPotato.GetPassMultiplier` (`0x863B9F0`, `0x863B870`) return an integer, 1 if there is no fragment. How the multiplier grows per pass is native (`0x863AA90`, not traced).
- The three items: `Id.Item.HotPotato.Alpha`, `.Bravo`, `.Charlie` (the CDO lists Alpha, Charlie, Bravo). The three item definitions and the three throwable Blueprints are identical except the tag (diff of the dumps). The display text **is** in the data: `STRINGS_HotPotato` `Items.HotPotato` = "Gold Potato", description "- Don't hold it for too long...", flavour "Hot. Hot. Hot.". Gold M67 mesh, equip as an unarmed utility grenade, `ThrowVelocity` 2200 (primary, overarm) and 1400 (secondary, underarm), weight 1000. The throwable `B_HotPotato` has `ExplosionDamageValues` 0, `ImpactDamage` 0, `bExplodeOnHealthDepleted` false, `AdditionalGravity` -250: it is not damaging in the Blueprint defaults.
- Native defaults (constructors): `WDItemExtensionData_HotPotato` (`0x8637170`) three unnamed floats 8.0, 15.0, 0.85 at +0x48, +0x4C, +0x50; `WDHotPotatoComponent` (`0x8636FE0`) float 2.5 at +0x100. The names are hashed in this build, so what they mean (the 8 to 15 pair reads like a fuse range in seconds, 0.85 like a factor) is **not established**; do not publish a meaning.
- Server seeding award rules (the pending award the potato feeds), `WDServerSeedingPreLobbyComponent` ctor `0x863D6A0`: first award 150, cap 5000, periodic award 250 every 60.0 s (`ApplyPeriodicAward` `0x863EA30` calls the award handler `0x8641460` with the +0xEC value; the timer is armed at `0x863ECC0` from +0xE8), award handler clamps `pending + Amount` to [0, 5000] (`0x8641460`). A further 15.0 and an int 60 gate when the lobby award runs (`0x863EAC0`, `0x863EB70`, `0x8640600`). The pending amount is delivered when the match starts (`0x8640D40`, a message built from the amount), and the component's Blueprint lists `Vendor.Discount.FirstPurchase`. **What the amount buys is not decoded** (the tag suggests a first-purchase vendor discount; unproven). The sibling reason tags are `Shooting` ("Sharpshooter!"), `Soccer` ("GOAL!") and `Default` ("Waiting For Players"): the pre-lobby has three mini-games (shooting, soccer, potato).
- Evidence level: cooked Blueprint bytecode read, `.uplugin` text, static disassembly of constructors. Not run.

### P2. King of the Hill: team sizes, match length, win condition

Status: **FOUND** (teams, score rules, defaults); team size cap **SERVER**; time limit **ABSENT** in the client.

- **Teams.** `KOTH` game feature adds `B_FactionSetup_CreateThreeTeams` (factions Alpha, Bravo, Charlie, i.e. Lonestar, Valkyra, Manticore). `OverpopulatedTeamThresholdConfig = 2` and `bLockOverpopulatedTeamsConfig = true` in the example server config: a team may be at most 2 players larger than the smallest (`WDGameStateSession` `+0x574`). The maximum player count is `MaxPlayerCount` on the game state, set per server (SERVER); the client files give no number.
- **Match stages** (KOTH `RegisterMatchStates`): `WaitingForWorldLoad`, `WaitingForPlayerCount`, `Playing_KOTH`, `PostMatch`. `WaitingForPlayerCount.MinimumRequiredPlayers` is a config value; the example server file sets **20** (class default 0, ctor `0x6D6FB40`).
- **Win condition.** `WDMatchState_Playing_KOTH` (ctor `0x77560C0`): `ScoreLimit` **10**, `ScorePeriod` 0 (config sets it; the example server uses **24**), `MinScorePeriod` **18.0**, `MaxScorePeriod` **30.0**, `InactivityTimeoutSeconds` 0, `MatchHardCapSeconds` 0 (0 means unused in the check at `0x776F800`). `0x775BE60` clamps `ScorePeriod` into [Min, Max] (when Max > 0) and rounds it to a whole second: a configured 24 stays 24. `0x776F800` (the state's continue check) adds points each period (the winning faction's gain from the zone component, capped so the total cannot pass `ScoreLimit`), ends the state when the limit is reached, when the hard cap is set and passed, or when the inactivity timeout is set and no score change happened for that long. `DefaultControlZone.ini`: `WDControlZoneGameStateComponent.ScorePerControlZoneTick = 1`. So the **match ends when a faction reaches the score limit** (native default 10 points; a server can change it with `Auth_SetMatchScoreLimit`); there is **no time limit** in the defaults (hard cap 0). How many points one period gives (what `0x141BFF8F0` returns for the leading faction) was not traced; do not state a points-per-minute figure.
- `DefaultMatchState.ini` names `WDMatchStateWaitingToStart` (5.0 s), `WDMatchStateInProgress` (0 = no limit), `WDMatchStateEnding` (35.0 s). Those classes are **not in this build's SDK**; the state classes in use are the `BHMatchState` subclasses above. Treat the ini as legacy; the numbers are real file content but their consumer is not shown.
- Evidence level: config files read, constructor disassembly, partial decompiled logic. Not run.

### P3. Deathmatch: teams, match length, win condition, spawn, ammunition

Status: teams **FOUND**; win condition **FOUND** (score limit, native default); match length **ABSENT**; spawn selection and ammunition **NATIVE**.

- Two teams: `B_FactionSetup_CreateTwoTeams` creates Alpha and Bravo (default faction `Meta_Alignment_Faction_Default`). Stages: `WaitingForWorldLoad`, `WaitingForReadyUp` (not the player-count state KOTH uses), `Playing_Deathmatch`, `BHMatchState_PostMatch`.
- `WDMatchState_Playing_Deathmatch` ctor `0x848B6F0`: `ScoreLimit` **75** (`OnPlayerKilled` is its only function, so the score is kills). No time limit is set in the constructor chain (`BHMatchState` base ctor `0x4D5F580` only sets the tag). Whether kills are counted per team or per player was not traced.
- `WDHealthRegenComponent` ctor `0x848B5F0`: `HealthToRegenerate` **5.0** per `TickInterval` **1.0** s (the delay-timer byte is 0). This fills the wiki's "regeneration rate is not in the data".
- `B_DeathmatchSpawner` is an empty Blueprint subclass of `WDDeathmatchPlayerSpawnManagerComponent` (no CDO overrides, no functions): the spawn choice is native (`PlayerStarts` array, ctor `0x848F7A0` area). `WDLoadoutAmmoGenerationComponent` has no configurable fields (ctor `0x848B680` zeroes two pointers); ammunition amounts are native logic and the loadout path is in `docs/evidence/round8-loadout-deathmatch.md`.
- Player-to-team placement in a normal match: no assignment component is added by the Deathmatch feature (`AutoAssignFactions` is only a ShootingRange flag); placement is native lobby/ready-up logic. Status **NATIVE (not traced)**.

### P4. Zone layout and region choice (weights)

Status: layout choice **FOUND** (it is chosen by the server); weights in play **FOUND** for the example rotation; region selection **OPEN**.

- The server map rotation carries the layout. `WDServerMapRotationSettings.RotationEntries` entries are `(Map, Experience, Lighting, ZoneAlternator)` (example config, 72 entries, `RotationMode=Ordered`): each entry names the `ZoneAlternator.*` tag directly. `AWDControlZone` has a Config array `ControlZoneQueue` and a transient `ValidatedControlZoneAlternatorQueue` (SDK), i.e. the queue is filled from this rotation.
- In the example rotation every alternator tag appears exactly 6 times (3 maps x 4 alternators x 6 = 72 entries), including the **weight-0** ones. Data weights (`AlternatorSelectionWeight` in the five `DA_ControlZone*Config*` assets): Ozeti Default 1, Farmland **0**, Church 1, River 1; Zestafona Default 1, SmallFactory **0**, WaterTreatment 1, Houses 1; Bakurani Default 2, Farmland 1, Lumberyard 1 (the config has **no River entry**, yet the example rotation uses `ZoneAlternator.Bakurani.River.Circle` 6 times: that tag has no zone data in the Bakurani config, so what a server does with it is unknown; it may be stale or served by another config); Kenya Default 1, North/East/West **0**; Sabartulo Hospital 1, Bazaar/River/Hillside **0** (Russia). So weights do not decide which layout a rotation entry uses, and weight-0 layouts are used when the server names them. Where the server does not name an alternator, the code that would use `AlternatorSelectionWeight` was **not located** in this pass (searched the `AWDControlZone` `OnExperienceLoaded` registrations `0x7774DB0` family and `0x7766520`, which is not the alternator code). That fallback stays OPEN.
- Pairing: `Bakurani_KOTH_01` is paired with `ZoneAlternator.Bakurani.*`, `Madrid_KOTH_01` with `ZoneAlternator.Ozeti.*`, `Detroit_KOTH_01` with `ZoneAlternator.Zestafona.*` (see P8). Region choice (weight-5 regions): OPEN, not searched.

### P5. Starting cash conflict

Status: **FOUND**. `data/.../Meta/CurrencyDefinitions/DT_CurrenciesDefinitions.json` row `Attribute.Meta.Currency.Cash` has `InitialBalance = 10000`; `Attribute.Meta.Currency.GoldBars` `InitialBalance = 0`; there is **no Intel row**, so Intel has no starting balance in the client. So the Progression/Currencies pages that say 10,000 are right for Cash; the "Not in the data" text applies to **Intel only** (the Intel line `Starting balance. Not in the data.` is correct). The current `_wiki/progression-and-economy/currencies.md` already says 10,000 for Cash (lines 12, 26, 32) and "Not in the data" only on the Intel bullet (line 56). Wording note: `InitialBalance` is the client definition; the grant itself is backend/server (the table is a currency spec, no code reading it was traced). Check: `python -I _tools/mode_rules.py --check` asserts both values.

### P6. Vehicle damage V-7 scope conflict

Status: **FOUND (settled)**. `pipelines/Wardogs_VehicleDamagePipeline_v1.md` (row V-7) is current: V-7 is **closed** for physics contacts (round 6) and ordinary movement sweeps (round 8, `docs/evidence/round8-vehicle-sweep.md`: sweep conversion `0x3C7BCE0`/`0x3C6CBA0`, `FaceIndex=-1`, `MyItem=-1`, reverse branch of `0x3A902D0`). `docs/evidence/vehicles.md` §5 still said sweep-sourced hits (`0x3A902D0`) were open, and row `0x3A902D0` said "not traced". Both were stale; edited: §5 now says V-7 closed for contacts and ordinary sweeps, and what remains open is only a custom query with face indices or an instanced target whose item index matches a material slot. Open under V-7: none beyond that. Files: `docs/evidence/vehicles.md`.

### P7. AI reaction time

Status: **ABSENT** as a reaction-time field; the closest values **FOUND**.

- `WDAICharacterConfigData` (SDK `WDAIPvEAICoreRuntime_classes.hpp:1444-1457`) has no reaction, delay or reaction-time field; fields near it are `POILookAtSwitchTime` 2.5 s, `AlertWaitTime` 2.0 s, `RadiusToSearchForCovers` 3000 (round 36, ctor `0x8863090`).
- `BT_WDAIPvECore_AlertedReaction` (from `round36_ai/dump`, so the BT **is** exported, contradicting the backlog's "BT not exported"): root `Sequence_2` = `ApplyForJob` -> `WDBTTask_LookAtStimulusOrigin` -> `BTTask_ParametrizedWait` "Alerted Wait" (WaitTime bound to `WDAIDataProvider_AIConfigData`, field `EAIConfigDataField::WaitAlertedTime`, BT default 10.0, overridden by the config's `AlertWaitTime`, native default 2.0 s) -> a job-state selector that finds cover (`EQS_FindCoverNearby`, move to cover) or peeks (`EQS_FindPeekPointToStimulus`; `WDBTTask_PeekCover`, waits 1.0 s and a +/-2 s random wait). So the delay between noticing a stimulus and acting is: look at the stimulus origin, then **2.0 s** (default) before moving to cover. The build-up of detection (how long before an AI notices at all) is native and combines stance, movement and firing multipliers (round 36 section 2b/2c, not decoded). Wiki wording: "Not yet known" can become "no reaction-time value exists; after noticing, soldiers look toward the noise and wait 2.0 s (default `AlertWaitTime`) before moving".
- Evidence: BT data read, SDK, round 36 ctor.

## Remaining backlog items, in backlog order

### Modes, maps, zones

| Item | Status | Value and source |
|---|---|---|
| Tank Town: no rules, map name | FOUND | `Config/Experiences/Tanktown.json`: `Includes ["KOTH"]`, `DisallowedFeatureFlags ["Experience.Rules.SkipPlayerDowned"]`, editor-visible. Same game features and match flow as KOTH (three teams, score-limit win); no map of its own (it uses whatever data layers/map the server loads). Server-browser display data is not in the experience file. Evidence: config read. |
| Factions: what each is | OPEN | Not searched this round (round 36 conclusion stands). |
| Factions: weapons/gear differences | OPEN | Not searched. |
| Deathmatch factions placement | NATIVE | See P3. |
| Sniper Showdown stillness threshold | FOUND (native defaults) | `WDSniperShowdownStillnessSpottingComponent` ctor `0x8645410`; the Blueprint `B_SniperShowdown_StillnessSpottingComponent` overrides nothing (CDO empty). `UpdateInterval` 1.0 s, `DistanceThreshold` 5000.0 (unit assumed cm), `GracePeriod` 15.0 s, plus unnamed 5.0, 15.0, 90.0, int 3, 200.0 (+0xE4, +0xEC, +0xF0, +0xF8, +0xFC). The function that applies them (`GetWindowProgress`, `Client_ShowEventFeedMessage`) was not traced, so which number is the standing-still time is unproven. |
| Sniper Showdown OOB and explode | FOUND | Explode (`B_SniperShowdown_ExplodeComponent`): on `PlayerDied`, after a **1.5 s** delay, `SimulateRadialDamage` with `BaseDamage` 250, `ExplosiveRadius` 500, `MinimumExplosiveDamage` 30, `EffectiveExplosiveRadius` 250, `ExplosiveDamageFallOff` 0.5, `ExplosiveBluntDamage` 100, LOS check on, damage tag `Meta.Damage.Explosive.Utility.Claymore`, cue `GameplayCue.Claymore.Explode`. OOB (`B_SniperShowdown_OOBComponent`): on tag change, updates the gameplay tag count of `State.Location.SafeZone.Hostile` by +1 or -1 depending on the OR of `State.Location.Objective.ControlZone` and `State.Location.Objective.Hotzone`; starting items `Id.Item.SmallBackpack`, `Id.Item.Glock17`. The damage the hostile-zone tag applies is a gameplay effect elsewhere (not traced). |
| Sniper Showdown round length, leaderboard | FOUND (kill limit); ABSENT (length) | `WDMatchState_Playing_SniperShowdown` ctor `0x8644A30`: `KillLimit` **10**. No time value in the ctor chain; a round timer widget exists (`W_SniperShowdown_Timer`) but the duration source was not found. Leaderboard data remains empty. |
| Sniper Showdown factions and team sizes | FOUND (free-for-all) / NATIVE | Experience `SniperShowdown.json`: `FeatureFlags ["Experience.Rules.FreeForAll", "Experience.Rules.NoCashFeed"]`, pawn data `SniperShowdown_PlayerData`. Factions come from `WDSniperShowdownFactionAssignmentComponent` + `WDSniperShowdownFactionPool` (the Blueprint subclass is empty). Number of factions in the pool: native, not read. |
| Experiences: first-spawn route order | OPEN | Not searched. |
| Africa unnamed layout | FOUND | `Config/Experiences/Africa/Kenya_KOTH_01.json` (`Includes KOTH`, data layer `DL_Kenya`), and the Africa zone config `DA_ControlZone_Config_Africa` names its alternators `ZoneAlternator.Kenya.{Default,North,East,West}.Circle`. So the Africa layout is the Kenya KOTH map (Default weight 1, North/East/West weight 0). Display name for the server browser: not re-read. |
| Three layouts with no display name, four KOTH entries | FOUND (experience names) | Experiences present: Africa `Kenya_KOTH_01`; Europe `Berlin_KOTH_01`, `Madrid_KOTH_01`, `Paris_KOTH_01`; Kavkazi `Bakurani_KOTH_01`, `Bakurani_KOTH_02`, `Mindori_KOTH_01`, `Tevza_KOTH_01`, `Bakurani_SniperShowdown_01`; NorthAmerica `Detroit_KOTH_01`, `Detroit_SniperShowdown_01`; Russia `Moscow_KOTH_01`, `Moscow_SniperShowdown_01`. These are the config aliases; their display names are in the server-browser tables, not re-read this round. Each lists its data layers (map area and three spawn-area layers, e.g. Madrid: `DL_Madrid`, `DL_BarcelonaSpawn`, `DL_MalagaSpawn`, `DL_GranadaSpawn`). |
| Name links (Ozeti to Madrid etc.) | FOUND (Madrid, Detroit, Bakurani); OPEN (Moscow) | The example rotation pairs experience and zone alternator: `Madrid_KOTH_01` with `ZoneAlternator.Ozeti.*`, `Detroit_KOTH_01` with `ZoneAlternator.Zestafona.*`, `Bakurani_KOTH_01` with `ZoneAlternator.Bakurani.*`. That is a data link (Ozeti = Madrid map, Zestafona = Detroit map). The Russia zone config names its alternators `ZoneAlternator.Sabartulo.{Hospital,Bazaar,River,Hillside}.Circle` (spelled Sabartulo in the data), next to the experience `Moscow_KOTH_01`; Moscow does not appear in the example rotation. |
| Bakurani KOTH_01 and KOTH_02 | FOUND | Same `Includes KOTH`; they differ only in data layers: KOTH_01 `DL_Bakurani` + `DL_KhevuliSpawn`, `DL_ChutaSpawn`, `DL_BaghiSpawn`; KOTH_02 `DL_Bakurani` + `DL_RachuriSpawn`, `DL_TavarshiSpawn`, `DL_SanaviSpawn`. So they are the same map and rules with different spawn areas. |
| Zone placement choice | FOUND (server rotation) | See P4. |
| Zone region choice | OPEN | Not searched. |
| Zero-weight towers / alternators | FOUND (alternators) | See P4: used by server rotation entries. Towers: OPEN. |
| Hot Zone movement in play | OPEN | Not searched. |
| NorthAmerica Hot Zone height | OPEN | Not searched. |
| Region containment/overlap | OPEN | Not searched. |
| Gym Hot Zone sizing | OPEN | Not searched. (`Gym.json` experience: `Includes KOTH`, adds `FreeVehicleSpawner`.) |
| Map layouts beyond zone data (.umap) | OPEN | The rebuilt `rawfiles` mode can read `.umap`; not attempted. |
| Map areas (Saburtulo, Bakurani Outskirts, Africa) | OPEN | Not searched; data layer names above are the new lead. |
| Sniper Showdown Bakurani and Jutari | FOUND (partial) | `Bakurani_SniperShowdown_01` exists; Jutari not found in experiences. |

### AI and PvE

| Item | Status | Value and source |
|---|---|---|
| AI reaction time | ABSENT / FOUND closest | P7. |
| AI detection combine | OPEN | Not traced this round. |
| AI sight/hearing in play | OPEN | Not traced. |
| AI threat fade | OPEN | Not traced. |
| AI action order | FOUND (assets exist) | The `BT_WDAIPvECore_*` assets are in `round36_ai/dump` (Base, BaseReload, BaseReloadInCover, BaseShooting, BaseTakeCover, AlertedReaction, DefaultBehavior). Only AlertedReaction was summarised (P7). A full action order for `BT_WDAIPvECore_Base` is OPEN. |
| AI alert thresholds, EQS fields, blackboard use, units | OPEN | Not reached. |
| AI damage taken, AI accuracy | unchanged | Round 36 ABSENT stands; not re-searched. |
| PvE team sizes, Hunter Killer side, mission rewards, display names, scenario units/logic, VO durations | OPEN | Not searched. |
| `ScenarioPostMatchTimeoutDuration` | FOUND | `Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Config/DefaultBaseScenario.ini`: `[/Script/BaseScenarioRuntime.WDScenarioStateComponent] ScenarioPostMatchTimeoutDuration=15.0f`, `PvEGameEndUiDelay=0.5f`. |

### UI/settings and Other

All OPEN (not reached): ADS FOV option text, key rebinding, `BHUserSettingEnumDiscreteValues`, `IMC_*` contexts, hashed names, `_aaa` fields, water grid, FluidFlux, MicroBiome, smoke VFX, gameplay tags, mechanics units, `Percentage_Ongoing`, `EToolFonts`, significance, units, explosion timing, characters, achievements, automation, shooting range, moving target, localisation, skins.

## Other values picked up on the way (not in the backlog, usable by writers)

- `VehicleUtility` plugin ini: `WDVehicleUtilityComponent.MaxVehiclesPerPlayer = 2` (plugin description: caps per-player vehicle ownership on the session game mode).
- `DefaultItemSmith.ini`: `ModKitLimit=10`, `DefaultModKitName="Custom"`, default Gunsmith weapon `Id.Item.AK74M`.
- Example server file: `ServerMinPlayerCash/Max`, `ServerMinPlayerLevel/Max` (0 = no limit), `MaxReservedSlots` 0, high-ping kick settings (`WarmupSeconds` 15, `StallSeconds` 0.5, `MeasurementSeconds` 120, `SampleIntervalSeconds` 5, `DiscardHighestSampleFraction` 0.15), RCON default port 7776.
- Example rotation lighting presets: `DayEarlyClear`, `DayEarlyFog`, `DayClear`, `DayLateClear`, `DayLateGray`, `DayLateGrayFog` (12 each in 72 entries).
- Experience variants of KOTH: `KOTH_Hardcore` (alias Hardcore: no dynamic crosshair, squad-only killfeed, no HUD ammo, no minimap health, no quick slots, disables third-person vehicle camera) and `KOTH_InfantryOnly` (alias InfantryOnly: disables the tank, helicopter and ring-turret vehicle features TNK_01, ROT_02, ROT_03_WeaponVariants, WHL_05_Minigun, STN_01, STN_02, STN_05, TNK_04, ROT_04_MachineGun, WHL_02_RingTurret, WHL_05_RingTurret, WHL_07_ArmouredBattle, WHL_08_RingTurret).

## Reproduce

- Config: `WdExtract <Paks> <key> <usmap> <out> <oo2core> rawfiles Wardogs/Config --copy` (and `rawfiles .uplugin --copy`).
- Packages: `WdExtract ... list <prefix>` then `dump <files.txt>` (Hot Potato: `rawfiles HotPotato`, then `dump` of the package paths).
- Native: `corpus.sqlite` `search` on `UWDMatchState_Playing_KOTH_VFT` etc. finds the constructor (the function that stores the vtable and the defaults).
- Data check: `python -I _tools/mode_rules.py --check`.

## Wiki updates

- `_wiki/game-modes-and-maps/hot-potato.md` -> frontmatter and infobox: "Type: Game mode (Season 2)" -> "Pre-lobby mini-game (Season 2)"; "Rules: Not yet known" -> "Players pass a potato while waiting in the pre-lobby; each pass pays 10 x the pass multiplier in pre-lobby award points"; description line -> a pre-lobby mini-game, not a match mode.
- `_wiki/game-modes-and-maps/hot-potato.md` -> "Items. ... The item display text is not in the data" -> "The item is named Gold Potato (description: Don't hold it for too long...; flavour: Hot. Hot. Hot.); Alpha, Bravo and Charlie are identical in the data apart from their tag".
- `_wiki/game-modes-and-maps/hot-potato.md` -> "Objective, scoring, teams, match length and win condition. Not yet known." -> "Scoring: the award is 10 x pass multiplier, paid through Server Seeding with the message Hot! Hot! Hot!. There are no teams, match length or win condition: it runs while players wait for the match to start (the pre-lobby also has shooting and soccer mini-games)."
- `_wiki/game-modes-and-maps/hot-potato.md` -> "Rewards" section: add that the potato feeds the pre-lobby award (first award 150, periodic 250 per 60 s, cap 5000, as defaults); what the award buys is not decoded.
- `season-2-changes/game-modes-maps.md` (data page, not wiki) -> "Hot Potato game mode" and "Team Offence and Hot Potato are new game-mode plugins" -> "Hot Potato is a pre-lobby mini-game plugin" (left for the writer pass or a data-page edit; not changed here).
- `_wiki/game-modes-and-maps/king-of-the-hill.md` line 36 -> "Team sizes, match length and win condition. Not yet known." -> "Three teams. The match ends when a team reaches the score limit (default 10 points); a point period of 18 to 30 s applies (24 s in the example server file). There is no time limit by default. The player cap and the minimum players to start (20 in the example server file) are server settings."
- `_wiki/game-modes-and-maps/deathmatch.md` lines 35 to 37 -> "Health. ... regeneration rate is not in the data" -> "5 health per second"; "Team sizes, match length and win condition. Not yet known." -> "Two teams (Alpha and Bravo). The mode ends at a score limit of 75 (kills). No time limit in the data. Player caps are server settings."; "Spawning. ... not yet known" -> "Spawn choice is native code (no data)"; "Ammunition amounts" stays "not in the data (native)".
- `_wiki/game-modes-and-maps.md` line 19 and any Tank Town page -> "Tank Town: server browser lists it with no rules" -> "Tank Town uses the King of the Hill experience unchanged (same teams, score limit and zone); only the map/server-browser listing differs".
- `_wiki/game-modes-and-maps/factions.md` line 62 and `deathmatch.md` -> "how a player is placed into a faction is not known" -> keep, but add "Deathmatch creates two factions, Alpha and Bravo; King of the Hill creates three".
- `_wiki/game-modes-and-maps/sniper-showdown.md` line 27 (stillness) -> add the component defaults (update every 1 s, distance threshold 5000, grace period 15 s) with "meaning of each is not confirmed"; line 29 (OOB, explode) -> "A player who dies explodes after 1.5 s (250 damage, 500 radius, 250 effective radius, minimum 30, falloff 0.5, 100 blunt), using a Claymore damage type"; out-of-bounds: "leaving the control zone and hot zone adds the Hostile Safe Zone state"; line 32 (round length) -> "Kill limit 10; round length not in the data"; line 34 (factions) -> "Free-for-all rules flag; each player gets a faction from a pool".
- `_wiki/game-modes-and-maps/zone-layouts.md` lines 43 and 44, `bakurani.md` line 39 and 47, `control-zone.md` line 30 -> "the data suggests one placement is picked by weight at random per match, but the code path is not confirmed" -> "The server's map rotation names the layout (ZoneAlternator tag) for each map entry; in the example rotation every layout, including the weight-0 ones, appears equally often. The weights are therefore not what picks the layout when a rotation entry names one."
- `_wiki/game-modes-and-maps/ozeti.md`, `zestafona.md`, `bakurani.md`, `zone-layouts.md` (lines 66, 75, 93) -> "name link not confirmed in game" -> "the example server rotation pairs Madrid with the Ozeti layouts, Detroit with the Zestafona layouts and Bakurani with the Bakurani layouts" (Saburtulo/Moscow stays unconfirmed).
- `_wiki/game-modes-and-maps/bakurani.md` line 27 -> "how the two server-browser entries differ" -> "Bakurani KOTH 01 and 02 are the same map and rules; they use different spawn-area sets (Khevuli, Chuta, Baghi against Rachuri, Tavarshi, Sanavi)".
- `_wiki/game-modes-and-maps/unnamed-africa-layout.md` and `maps.md` line 42 -> "no display name / unnamed" -> "the Africa layout is the Kenya King of the Hill map (experience Kenya_KOTH_01, alternator tags ZoneAlternator.Kenya.*)".
- `_wiki/game-modes-and-maps/maps.md` -> add the extra experiences: Berlin, Paris, Mindori, Tevza (King of the Hill), Moscow (KOTH and Sniper Showdown), Bakurani and Detroit Sniper Showdown.
- `_wiki/progression-and-economy/currencies.md` -> keep "Cash starts at 10,000"; add the source (client currency definition, `InitialBalance`), and keep "Not in the data" only on the Intel row.
- `_wiki/progression-and-economy/cash-and-rewards.md` line 12 -> no change; optionally cite `DT_CurrenciesDefinitions`.
- `_wiki/game-modes-and-maps/ai-enemies.md` line 19 -> "Reaction time: Not yet known" -> "No reaction-time value. After noticing a sound or sight, a soldier turns toward it and waits 2.0 s (default) before moving to cover or peeking".
- `_wiki/game-modes-and-maps/pve-scenarios.md` -> add "After a mission ends the scenario state waits 15 s before the post-match step, and the end screen is delayed 0.5 s".
- `_wiki/game-mechanics` vehicle page that states vehicle ownership limit -> "a player may own at most 2 spawned vehicles at a time" (VehicleUtility `MaxVehiclesPerPlayer = 2`), if the page has a gap.
