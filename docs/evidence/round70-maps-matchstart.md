# Round 70: spawn-to-zone distances, light and weather per map, and what the match start does to players (R70-RE)

Static analysis only. Nothing was run. Evidence levels: cooked data read (extractor `dump` of the four world packages and the sky Blueprint and presets, `findname` over the name tables), the exported JSON of rounds 51, 66, 67 and 68, static decompile (the corpus `corpus.sqlite`), SDK headers, the example server config. Scripts and raw output are under `E:/Reverse_Engineer/wardogs_analysis/round70_re/` (outside the repository): `dist.py` (distances), `sky/` (sky Blueprint, presets, `presets.json`, `findname` results), `map_xr.py`, `cb.py`, `ctx.py` (the 80 `MatchState.Playing` references mapped to functions and their bound callbacks, `xr_funcs.txt`), `build_json.py`, `apply_wiki.py`. Status words follow the round 36 brief: FOUND, NATIVE, SERVER, ABSENT, PROTECTED. Nothing sat behind the protection layer, so there are no PROTECTED rows. Addresses are RVAs (image base 0x140000000).

## Statuses

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1a | Distance from each side's spawn area to the middle of the zone area | FOUND | 3,520 to 4,130 m for all fifteen areas of the five main entries (table below). Inferred part: the spawn manager actor stands for the middle of the infantry grid, and Saburtulo's zone middle is the placed zone object because it has no region list. |
| 1b | Distance to the nearest Hot Zone Magnet tower | FOUND | 3,290 to 3,780 m. Nearest tower per area is in the table. |
| 2a | Sun angle or time | FOUND | Fixed. Ozeti and Saburtulo store the "late afternoon, clear" preset (sun 20.2 degrees up); Bakurani and Zestafona store "midday, clear" (43.8 degrees up). |
| 2b | Day and night cycle, dynamic weather | ABSENT | One `BP_SkyActor_C` per world with tick off; no `WDDynamicSky`, `WDTimeOfDayDataReplicated` or weather replication actor is named in any content package (`findname`). Rain exists only as one preset. |
| 2c | Which preset a match uses | SERVER | The server rotation entry has a `Lighting` field naming a preset by its title; the sky actor applies the preset whose title matches the replicated name. The stored preset is the default (inferred). |
| 2d | Fog density and start distance | FOUND (values), inferred (final effect) | Level actor values: Bakurani and Zestafona density 0.009, start 20 m, volumetric start 10 m; Ozeti and Saburtulo density 0.007, start 100 m. The applied preset overrides density, falloff and the volumetric start where it lists them. |
| 2e | Wind, thunder | NATIVE | The weather subsystem has wind range and air density setters; the time-of-day class carries a thunder schedule. No placed source; values not read. |
| 3a | Players teleported at match start | ABSENT | No function among the 60 that reference `MatchState.Playing` moves a player. |
| 3b | Health or inventory reset | ABSENT | None of them heals, refills or clears. |
| 3c | Pre-lobby gear kept | ABSENT (no removal found; kept, inferred) | The pre-lobby objects remove themselves; the player is not touched. |
| 3d | Starting Cash set at match start | FOUND (no) for the match start; NATIVE for the real moment | The only Cash write at match start is the pre-lobby payout. The base balance is the currency table value. The function that applies `InitialBalance` is not among the Playing subscribers and was not traced. |
| 3e | Base starting Cash per mode | FOUND | 10,000 for every mode using the default currency table (session override `OverrideStartingCash` = -1); PvE scenarios: Strike and Disarm 3,000, VIP Escort 2,000, Hunter Killer none. |

## 1. Spawn-to-zone distances

Positions are world metres from the placed actors in `assets/data/vehicle-spawns.json` (cm, divided by 100) and `assets/data/map-magnets-extents.json`. Spawn position: the infantry spawn manager of the data layer of each team slot (`experiences.<entry>.teams`); the deployment board is within 60 m of it (columns for the board are in the JSON). Distances are 2D (x and y). Result: `assets/data/map-spawn-distances.json`.

| Entry | Spawn area (team slot) | To zone area middle (m) | To nearest tower (m) | Tower |
|---|---|---:|---:|---:|
| Bakurani_KOTH_01 | Baghi (Alpha) | 3,939 | 3,607 | 5 |
| | Khevuli (Bravo) | 3,807 | 3,501 | 4 |
| | Chuta (Charlie) | 4,131 | 3,781 | 3 |
| Bakurani_KOTH_02 | Sanavi (Alpha) | 3,895 | 3,646 | 2 |
| | Rachuri (Bravo) | 3,851 | 3,525 | 4 |
| | Tavarshi (Charlie) | 3,822 | 3,458 | 3 |
| Madrid_KOTH_01 (Ozeti) | Granada (Alpha) | 3,522 | 3,291 | 2 |
| | Barcelona (Bravo) | 4,006 | 3,375 | 3 |
| | Malaga (Charlie) | 3,891 | 3,717 | 1 |
| ED_Detroit_KOTH_01 (Zestafona) | Boston (Alpha) | 3,729 | 3,445 | 3 |
| | Austin (Bravo) | 3,927 | 3,669 | 1 |
| | Chicago (Charlie) | 3,649 | 3,396 | 2 |
| Moscow_KOTH_01 (Saburtulo) | Kuzminki (Alpha) | 3,932 | 3,623 | 2 |
| | Rostokino (Bravo) | 3,867 | 3,540 | 5 |
| | Ramenki (Charlie) | 3,996 | 3,653 | 4 |

Zone area middle: Bakurani (-8,301, -11,201), Ozeti (-6,376, -6,111), Zestafona (-1,100, -2,105); Saburtulo has no region list ([round67](round67-maps.md)) so the placed zone object (-181, -59) m stands in (inferred). The Hot Zone moves during a match, so these are distances to the middle of the area it can reach.

Caveats. (a) The manager actor position is the centre of its spawn points (reading; the point cloud was not re-measured). (b) Saburtulo's boards carry swapped layer tags (round 51): the board tagged Kuzminki stands in Ramenki's area and the reverse, so board columns by layer in the JSON are crossed for those two; the infantry columns are by layer and correct. (c) The wiki side names (Lonestar, Valkyra, Manticore) pair with team slots by inference ([vehicle-spawns.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-spawns.json)); the table here uses the team slots.

## 2. Light and weather

Sources: the `BP_SkyActor_C` export in each world package (raw `round68_re/w/<World>.json`), the Blueprint `Environment/Lighting/Actors/BP_SkyActor` (`sky/BP_SkyActor.json`), the nine `PDA_LightSettings_C` presets under [`Environment/Lighting/DataAssets/Presets/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Environment/Lighting/DataAssets/Presets) (`sky/DA_LightSettings_*.json`, summary `sky/presets.json`), `WDSky` and `WDDynamicSky` in the SDK, `ExampleStandaloneServerConfig.ini`.

- **Sky actor.** `findname` for `BP_SkyActor` matches exactly the four world packages and the minimal gym. The Blueprint class default has `PrimaryActorTick.bStartWithTickEnabled` false and a stored `DA_LightSettings` (Morning). Each world instance stores its own: Kavkazi and NorthAmerica [`DA_LightSettings_Midday_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Environment/Lighting/DataAssets/Presets/DA_LightSettings_Midday_01.json) (title `DayClear`), Europe and Russia [`DA_LightSettings_Afternoon_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Environment/Lighting/DataAssets/Presets/DA_LightSettings_Afternoon_01.json) (title `DayLateClear`). The native parent `AWDSky` has `CurrentPresetName` (replicated, RepNotify) and `SetPreset(Name)`; the Blueprint's begin play reads the game state, loads the lighting scenario list (`GetPrimaryAssetIdList`, async load) and compares each preset's `UserTitle` with the name (`EqualEqual_StrStr` on `Conv_TextToString`). So the preset is chosen by name at begin play (reading of the Blueprint bytecode; the game state's value was not traced).
- **Server choice (SERVER).** `UWDServerMapRotationSettings` has `AllowedLightingScenarios`; the example config's `RotationEntries` carry `Lighting="DayEarlyClear"` and five other names, each used four times per map in the rotation (Bakurani, Ozeti, Zestafona). The six names map to Morning, MorningFoggy, Midday_01, Afternoon_01, AfternoonOvercast, AfternoonOvercastFog. The Sunrise (`DayStartClear`), Sunset (`DayEndClear`) and Rain (`DayLateRain`) presets are unused by the example. Saburtulo is not in the example.
- **No cycle (ABSENT).** `findname` over [`Wardogs/Content`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content) for `DynamicSky` returns only `UltraDynamicSky` texture names (no actor), `TimeOfDay` and `WeatherReplication` return nothing. The SDK classes `AWDDynamicSky` (solar time, moon, volumetric clouds), `AWDTimeOfDayDataReplicated` (day length, thunder schedule) and `AWDWeatherReplication` exist in code, but no package places them. The world files hold no other sky, fog or cloud actor (`PostProcessVolume` 3 to 5 per world and `SweejAmbienceVolume` are audio and grading helpers).
- **Wind (NATIVE).** `UWDWeatherSubsystem` has `SetWindRange`, `GetWindVector`, `SetAirDensity`, `IsRaining`; the values in play were not read.
- **Sun angle.** Directional light pitch/yaw/intensity on the actors: Kavkazi and NorthAmerica -43.75 / -88.80, intensity 200,000, 8,000 K, light function `MI_LightFunction_Midday` (preset: intensity 120,000); Europe and Russia -20.17 / -157.0 (preset: -20.17 / -170). Sun height = -pitch. The data does not say which way is north.
- **Fog.** Exponential height fog on the actors: Kavkazi and NorthAmerica density 0.009, falloff 0.1, second layer 0.002 / 0.02, start 2,000 cm (20 m), volumetric start 1,000 cm; Europe and Russia density 0.007, falloff 0.25, second layer 0.0005 / 0.05, start 10,000 cm (100 m). `SetupExponentialHeightFog` sets density, falloff, colour, volumetric terms, second layer, directional inscattering and both start distances from the preset; the presets list only the values they change, so whether the actor values or the engine defaults fill the unlisted ones is inferred. Preset fog density (thinnest first): Sunset 0.0009, Morning 0.002, Afternoon_01 0.004, Sunrise 0.007, Midday_01 0.009, AfternoonOvercast and AfternoonOvercastFog 0.015 (the fog preset adds a second layer of 0.02), MorningFoggy 0.06, Rain 0.3.
- **Rain.** Only [`DA_LightSettings_AfternoonOvercastRain`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Environment/Lighting/DataAssets/Presets/DA_LightSettings_AfternoonOvercastRain.json) has `RainSettings` ([`WD_HeavyRain`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Environment/Lighting/DataAssets/Presets/Weather/WD_HeavyRain.json), strength 1.0) and sets the directional light to not visible. `SetupRain` applies them (`ApplyRainSettings`, droplet and sky occlusion capture).

## 3. What the MatchState.Playing references do

The tag global `0xD2D2AC8` is registered by `0x11DD700`. Round 69 found 80 references in `xr_playing.txt`; `map_xr.py` maps them to 60 functions and one data reference (`0x99D7BA0`). Nearly all are the same shape: a begin-play or end-play handler asks the game state whether the tag is set and binds or unbinds a callback to the message for the tag. `cb.py` listed the callbacks each binds and `ctx.py` printed the code around the reference. Full classification: `assets/data/match-start.json`.

Findings by group:

- **Pre-lobby objects destroy themselves** (round 69): soccer pitch `0x76FFEF0`, targets `0x6A6F310`, Hot Potato `0x86390B0` and `0x8639660`, world radio `0x85F1630`. The payout `0x8640D40` is the only Cash write.
- **Spawn wall** `AWDSpawnWall` (`0x77022D0`, `0x7702350`): destroys itself when playing (`0x3A8F810` is the actor destroy wrapper). No instance is named in any content or plugin package (`findname`), so it is ABSENT in the four maps.
- **Game mode session** `0x6D8FB30` (begin play, `AWDGameModeSession` slot 115): its Playing callback `0x6D973D0` arms a repeating timer with `CashReportIntervalSeconds` (+0x4D0 = +1232) while playing, which logs each player's earned total (`0x6D96E60`, format "[Name=%s, Earned=%d]"). `0x6D97ED0` and `0x6D98170` push player data to the online interface and message each controller. No health, position or inventory change.
- **Player controller** (`0x6D4D200`, `0x6D51390`, `0x6D56600`): picks one of two state tags (UI or camera) depending on whether the match is playing; client side.
- **Components that only work while Playing**: refund (`0x6BE4BC0`), wager (`0x6D132F0`), call-for-help request (`0x6B03780`), dropped items (`0x6F0CD10`, `0x6F0D0D0`), lootables (`0x855B880`), free spawn vehicle (`0x765F5E0`, `0x765FE60`; class name inferred from neighbouring vtable), zone game state, regions and music (`0x775C430`, `0x8457B50`, `0x775CB20`), status HUD view models, PvE spawners.
- **The KOTH playing state itself** (`UWDMatchState_Playing_KOTH`): only the destructor and one override (`0x77697D0`, rounds a stored time value at +84) differ from the base; no player code.

So no function among these teleports, heals, clears or grants. This is a negative result over the functions read; callees reached through unnamed pointers (for example `0x6D99410` and `0x144C45DC0`) were not followed, and code that is not in the reference list (for example whatever spawns pawns on first join) is outside this check. Where players stand during the pre-lobby: the pitch, the targets, the vendors and the safe zone are placed in each team's spawn area ([round66](round66-map-actors.md), [round68](round68-boundaries.md)), so players are in that area; the move from the pre-lobby to the match needs no teleport (inferred).

### Starting Cash

- [`DT_CurrenciesDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CurrencyDefinitions/DT_CurrenciesDefinitions.json): `Attribute.Meta.Currency.Cash` `InitialBalance` 10,000 ([round42](round42-econ-buildables.md) P14).
- `DefaultGame.ini` `WDGameModeSession.OverrideStartingCash=-1`: use the table value ([round40](round40-modes-ai-other.md)). No per-experience override of the balance in the KOTH, Deathmatch, Sniper Showdown, Shooting Range or tutorial experience data (grep of `data/` for `InitialBalance` and `StartingCash`: only the currency table and the two scenario files).
- PvE: `ScenarioStartingCash` 3,000 (StrikeDisarm_01), 2,000 (VIPEscort_01), none for Hunter Killer ([round36](round36-ai.md)).
- When it is applied: not among the 60 Playing subscribers. The function that reads `InitialBalance` (struct `WDCurrencyDefinition`, +0x20) was not located. NATIVE, not traced; the match start does not set it. The pre-lobby payout adds on top ([round69](round69-prelobby.md)).

## Reproduce

`python -I dist.py`, `python -I build_json.py <repo>`; `WdExtract dump` of the four world packages (round 68 `w/`), `Environment/Lighting/Actors/BP_SkyActor` and the nine presets; `WdExtract findname Wardogs/Content BP_SkyActor` (and `DynamicSky`, `TimeOfDay`, `WeatherReplication`, `SpawnWall`); `python -I map_xr.py`, `cb.py`, `ctx.py <rva>`; `fn.py` from `round69_re` for single functions.

## Wiki updates

- `_wiki/game-modes-and-maps/bakurani.md`, `ozeti.md`, `zestafona.md`, `saburtulo.md`: two new columns in each spawn table (distance to the zone area middle and to the nearest tower), a note under the table, an infobox row and a "Light and weather" section.
- `_wiki/game-modes-and-maps/maps.md`: new "Lighting presets" section.
- `_wiki/game-modes-and-maps/pre-lobby.md`: "What happens at match start" updated (no teleport, no reset, gear kept: inferred), new "Starting Cash" subsection, infobox row.
- `_wiki/game-modes-and-maps/king-of-the-hill.md`: new "At the start of the match" rule.
