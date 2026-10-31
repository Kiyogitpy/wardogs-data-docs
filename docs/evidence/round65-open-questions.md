# Round 65: map cover materials, zone regions, Hot Potato, Team Offence, spotting cash (R65-RE)

Static analysis only. Nothing was run. Evidence levels: cooked data read (extractor dump of cooked packages with `WdExtract dump` and `list`/`findname`), decompiled-corpus reading and capstone disassembly (RVAs, image base 0x140000000). Method as in rounds 58 to 62. Extractor output and scripts are under `E:/Reverse_Engineer/wardogs_analysis/round65_re/` (`scan_cells.py` cell scanner, `resolve_mats.py` mesh to physical material, `agg2.py` and `make_asset.py` summary, `apply_cover.py` article section writer, `census.py` and `shapes.py` type census, `edl/` placed zone objects). No protected (virtualized) code was devirtualized and no row below needed it; no row is PROTECTED.

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1 | Cover materials per map | FOUND | About 109,600 (Bakurani), 69,800 (Ozeti), 98,700 (Zestafona) and 189,500 (Saburtulo) wall and building pieces; per-material counts below and in `assets/data/map-cover-materials.json`. |
| 2a | Saburtulo zone regions | ABSENT | The zone object placed in the Russia world has an empty region slot; no minimap or config region list. |
| 2b | Kenya region list and map area | ABSENT | No Africa or Kenya world, data layer or minimap exists in the paks. |
| 2c | Jutari region list and map area | ABSENT (regions); FOUND (area) | No region list. It shares the Kavkazi (Bakurani) world; its fixed zone sits about 400 m east of the Bakurani region area. |
| 2d | Minimap rows | FOUND (data fix) | The Russia and NorthAmerica rows of the minimap table were wrong; corrected. |
| 3 | Hot Potato fuse expiry | FOUND (data) and NATIVE (handler) | Explosion cue on the holder, a destroyed message, and the potato is consumed. No damage and no point loss. Round 57's inferred penalty is not supported. |
| 4 | Team Offence 180 s cancel | NATIVE | The server cancels: a one-shot server timer at ballot creation removes silent voters and re-tallies. |
| 5 | Spotting versus destroying cash | FOUND | Two different tables, and the vehicle is the SPH-2 (artillery row), not the L2A6. |

## 1. Map cover materials. FOUND

**Source.** The four main maps map onto four world packages (the pairing for Ozeti, Zestafona and Saburtulo is the existing name link in the wiki: Madrid entry = Europe, Detroit = NorthAmerica, Moscow = Russia; Bakurani = Kavkazi by its data layer): `Content/Maps/Worlds/<World>/<World>/_Generated_/*.umap`, the cooked World Partition cells. Cell counts: Kavkazi 9,753, Europe 10,141, NorthAmerica 9,976, Russia 10,746 (40,616). Each dumped cell holds `InstancedStaticMeshComponent`, `HierarchicalInstancedStaticMeshComponent`, `StaticMeshComponent`, `SplineMeshComponent` and `EpSpawned*` components, each with a `StaticMesh` and `PerInstanceSMData` (one entry per placed instance). Placed instances are therefore readable directly; no external-actor files exist (the round 51 file list has none). Cells are 30 ms each to dump; a batch script wrote one record per component (mesh path, instance count, `OverrideMaterials`, component bounds centre) and deleted the dump.

**Counted and not counted.** Not counted: `HLODInstancedStaticMeshComponent` proxies (distance stand-ins; 1.2 million instances per big world), anything under `/Foliage/`, `/HLOD/`, [`/Landscape/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Environment/Landscape) and `RuntimeVirtualTextureDecals`, meshes embedded in the cell itself (terrain tiles and HLOD meshes, `/Game/Maps/Worlds/...`), and `WorldBuilding/Prefab_Collisions` blocks (collision profile `WDTraversal`, which ignores the visibility and world-static channels, so they are movement helpers and not bullet cover; 8,000 to 18,000 per world, material instance `MI_PrefabCollisions_01a` = Dirt). Wall and building pieces are meshes under [`Environment/Architecture`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Environment/Architecture), `ExternalAssets`, `Props/Walls_and_Fences` and `Transport_Infrastructure/Road_Barriers`. The remaining placed objects (props, roads, rocks, Megascans scatter, blockout meshes under [`Maps/Gyms`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Maps/Gyms) and `Maps/WhiteBox_Assets`) are in the JSON under `other_pieces_not_counted` only as a total.

**Material to physical material.** `mesh_mats.json`: each mesh's `StaticMaterials` slots (3,099 meshes dumped, 6 missing from the paks); component `OverrideMaterials` replace a slot by index. `mat_phys.json`: the 1,011 material paths were dumped and the `Parent` chain followed (up to four hops, including `/BHMaterials/_Masters/MMi_*` plugin masters) until a `PhysMaterial` appeared: 932 resolved, 79 stayed `none` (mesh decals `MI_MeshDecal*`, flags, engine default, cell-local materials). This replaces the round 62 census, in which 1,328 of 3,152 material instances showed none because the parent chain was not followed.

**Counting rule.** A piece is one placed instance. It is counted under every physical material of its mesh slots (`pieces_with_material`; rows exceed the total). The slot surface areas are not in the data, so an equal split over the slots is also stored (`slot_split_share`, sums to the total) but not used in the wiki. `play` scope keeps pieces whose component centre is inside the bounding box of the map's zone-region polygons (`DA_ControlZoneRegionsConfig_*`) plus 500 m; this is an approximation (component centres, not single instances). Saburtulo has no region list, so only its `world` scope is given. Built-up area is the 1st to 99th percentile of building positions.

**Totals** (wall and building pieces; building / wall and fence and barrier):

| Map (world) | Scope | Pieces | Building | Wall | Different meshes | Whole world | Built-up area (km) |
|---|---|---:|---:|---:|---:|---:|---|
| Bakurani (Kavkazi) | play | 109,586 | 106,793 | 2,793 | 845 | 202,748 | 7.8 x 7.7 |
| Ozeti (Europe) | play | 69,833 | 66,641 | 3,192 | 828 | 114,190 | 6.6 x 4.3 |
| Zestafona (NorthAmerica) | play | 98,745 | 97,329 | 1,416 | 986 | 129,411 | 6.7 x 5.9 |
| Saburtulo (Russia) | world | 189,545 | 184,855 | 4,690 | 1,017 | 189,545 | 5.0 x 4.6 |

**Pieces whose mesh has the physical material in at least one slot** (top rows; share of the scope total; `none` = decals):

| Material | Bakurani | Ozeti | Zestafona | Saburtulo |
|---|---:|---:|---:|---:|
| Wood | 30,535 (28%) | 21,921 (31%) | 17,185 (17%) | 49,790 (26%) |
| Concrete | 25,274 (23%) | 14,051 (20%) | 28,672 (29%) | 60,809 (32%) |
| Brick | 24,195 (22%) | 16,523 (24%) | 12,525 (13%) | 49,470 (26%) |
| Metal | 23,380 (21%) | 12,286 (18%) | 39,303 (40%) | 31,000 (16%) |
| Plaster | 7,960 (7%) | 5,370 (8%) | 3,716 (4%) | 11,151 (6%) |
| Rubber | 5,413 (5%) | 4,265 (6%) | 1,997 (2%) | 10,035 (5%) |
| Ceramic | 3,743 (3%) | 2,269 (3%) | 1,788 (2%) | 5,715 (3%) |
| Glass | 520 | 184 | 939 | 3,061 |
| none (decals) | 7,752 | 5,343 | 3,660 | 12,264 |

Reading: Zestafona (NorthAmerica, an industrial world) is metal first (girders, panels); Saburtulo is mostly concrete (apartment walls and floors); Bakurani and Ozeti are wood, brick and concrete, with Ozeti brick-heavier. The physical material is what the game's penetration code reads, so the density table in the penetration page applies directly (concrete 8.5, metal 7.0 to 7.85, brick 5.2, plaster 3.0, wood 2.56).

**Limits.** (a) Pieces are counted, not wall area; a trim strip counts like a wall panel, so wood and rubber are over-weighted against area. (b) Buildings that break apart: `BHDemolitionCellProxyActor` (about 250 per world) is a cell marker with no mesh, so run-time demolition pieces are not counted. (c) Which pieces sit inside a given building or zone is not resolved; the `play` box is a rectangle. (d) Mindori and Tevza share the Kavkazi world with Bakurani and Berlin and Paris share Europe with Ozeti, so a world total is not one map's total; the `play` scope removes most of that, except Saburtulo. (e) Collision profiles per piece (some architecture components may have bullet collision off) were not filtered. (f) Component centres approximate where instances lie (an ISM component spans at most one 256 m cell in a PCG grid, inferred from the grid actor names `PCGPartitionGridActor_25600_*`).

Data: `assets/data/map-cover-materials.json`; data page section `content/Wardogs_Maps_v2.md` section 10; wiki: "Cover materials" in `bakurani.md`, `ozeti.md`, `zestafona.md`, `saburtulo.md`.

## 2. Zone regions and map area for Saburtulo, Kenya and Jutari

**2a. Saburtulo. ABSENT.** Placed zone objects were dumped from the ControlZone and SniperShowdown external data layer cells (`Wardogs/Plugins/GameFeatures/ControlZone/Content/EDL/...` and `.../Experiences/SniperShowdown/Content/EDL/...`; 52 cells). Each world has a `B_ControlZone_C` with a `WDControlZoneRegionsComponent`. The `ControlZoneRegionsConfig` field is set for Kavkazi ([`DA_ControlZoneRegionsConfig_Kavkazi`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZoneRegions/Content/Data/Config/DA_ControlZoneRegionsConfig_Kavkazi.json), cell `DI57U377P4HGVVFLQBP6NX1PK`), Europe ([`DA_ControlZoneRegionsConfig_Europe`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZoneRegions/Content/Data/Config/Europe/DA_ControlZoneRegionsConfig_Europe.json), cell `DNQPZNJYQQVIKB3E69WJPTIKS`) and NorthAmerica (`..._NorthAmerica`, cell `2J1T16NJUU3ARURBVVFQJHNA0`), and empty for Russia (cell `92ULMU24BRXYC0A1LPIJ5KUNA`, config [`DA_ControlZone_Config_Russia`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZone_Config_Russia.json)) and for all three Sniper Showdown zone objects (Kavkazi `5MM0KLRGTJM0WDTR3XZKMP52U`, NorthAmerica `3KGW8CCXL9FNRX9Q4MI2VN3NC`, Russia `BYEY5U43IVIICLV37S1KFHKB8`). No other asset in the paks references a region list for Russia: the `DA_ControlZoneRegionsConfig_*` assets are the three in the ControlZoneRegions plugin; `WDShapePlacementZoneComponent` objects in the Russia cells (40) are ladder no-build boxes. A scan of Russia cell types found no region, alternator or zone-volume actor besides the two zone objects, five hot-zone magnets, three safe zones and three spawn managers. The minimap data has no region field.

**2b. Kenya. ABSENT.** `findname Wardogs Kenya` returns only [`DA_ControlZone_Config_Africa`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZone_Config_Africa.json) (alternator tags `ZoneAlternator.Kenya.*`). `list DL_` (61 data layers) holds no `DL_Kenya`; the minimap list `DA_UI_*` has no Africa row; no world folder under `Content/Maps/Worlds` other than Europe, Kavkazi, NorthAmerica, Russia and `_Global`. [`Kenya_KOTH_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Config/Experiences/Africa/Kenya_KOTH_01.json) enables the data layer `DL_Kenya`, which is not in the paks. So neither a map area nor a region list exists in the client (the map is not shipped in this build, inferred).

**2c. Jutari. ABSENT (regions); FOUND (area).** The Sniper Showdown experience (`ED_SniperShowdown`) enables `EDL_SniperShowdown`, whose Kavkazi cell holds `B_ControlZone_C` with [`DA_ControlZoneConfig_SniperShowdown_Bakurani`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZoneConfig_SniperShowdown_Bakurani.json), ControlZoneComponent at world (-672,688; -1,117,098) with extents 35,000 and Hot Zone 7,500. The Kavkazi minimap ([`DA_UI_Kavkazi`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Tools/WorldCapture/Textures/Kavkazi/DA_UI_Kavkazi.json)) is 16,384 px at 100 units per pixel: x -1,632,000 to 0, y -2,040,000 to -408,000 (16.32 km square). The Bakurani region polygons span x -946,720 to -713,386 and y -1,242,515 to -997,663, so the Jutari spot is about 407 m east of the region box edge, inside the Bakurani world's built area (x -12.3 to -4.6 km, y -15.0 to -7.3 km). So Jutari has no area of its own: it is a fixed spot in the Kavkazi world. Its region slot is empty (2a).

**2d. Minimap table fix.** [`DA_UI_Russia`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Tools/WorldCapture/Textures/Russia/DA_UI_Russia.json): SizeX 16,384, `WorldUnitsPerPixel` 100, bounds -816,000 to 816,000 on both axes (16.32 km, centred on the origin). [`DA_UI_NorthAmerica`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Tools/WorldCapture/Textures/NorthAmerica/DA_UI_NorthAmerica.json): SizeX 16,384, 100, bounds -819,200 to 819,200. The table in `content/Wardogs_UI_v2.md` had copied other rows (Russia showed the Kavkazi bounds and 32,768 px; NorthAmerica 32,768 px); corrected in this round. The wiki's "16.3 km" (Saburtulo) and "16.4 km" (Zestafona) were already right. Russia's built-up area (x -3.2 to 1.8 km, y -2.2 to 2.4 km) sits inside its real bounds.

Pages: `saburtulo.md`, `unnamed-africa-layout.md`, `bakurani-outskirts-jutari.md`, `zone-layouts.md`.

## 3. Hot Potato fuse expiry. FOUND (data) and NATIVE (handler)

Restart timer `0x8638EE0` (round 57): `t = rand(min, max) x pow(0.85, multiplier)`, then `0x143AB8810` (timer set) with the delegate `0x86377A0` (timer-end handler, one-shot, rate `t`). The handler `0x86377A0` does three things and nothing else:

1. If the item has not already been handled (`*(a1+240) == 0`): gets the holder pawn; when the pawn is the authority copy (`+368 == 3`) it builds a gameplay-cue parameter block (instigator, effect causer and source object all the holder, location from the holder's data) and calls `0x4C46820` (execute-gameplay-cue on the actor: it looks up the `WDGameplayCueInterface` of the actor and calls the `WDGameplayCue` subsystem's handler, vtable +688, or +736 when the actor has no interface; identified by those names) with the tag read from the extension data at `+84`. That field is `ExplodeGameplayCueTag` of `WDItemExtensionData_HotPotato` (SDK `HotPotatoRuntime_classes.hpp`, `+0x54`). The cooked value in [`ID_HotPotato_Alpha`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/HotPotato/Content/Data/Items/ID_HotPotato_Alpha.json)/`Bravo`/`Charlie` is `GameplayCue.Grenade.Explode`.
2. Broadcasts `WDHotPotatoDestroyedMessage` (message type created at `0x86377A0` and `0x86376A0`, global `qword_14D3E7B10`); `0x86376A0` is the thrown potato actor's own removal path and sends the same message.
3. Sends `WDConsumeItemMessage` with a byte payload 1 (`0x69C8C50` creates the type) to the owning slot: the item is consumed.

No damage, gameplay-effect or health call exists in `0x86377A0` or its callees (callee list: `0x8636E60`, `0x675CDB0`, `0x6E65DE0`, `0x4C46820`, `0x4D4A4E0`, `0x675C960`, `0x4D49E50`, `0x69C8C50`, helpers). `0x8637A70` (the only other user of `0x4C46820` in this module) takes its tag from `a1+248` and then schedules a next-tick delegate (`0x144552A60`); it is most likely the thrown potato actor's own explode path (the actor class derives from `AWDExplosive`, whose cooked `ExplodeGameplayCueTag` is set on `B_HotPotato`; inferred, the class of `a1` was not proven). It also makes no damage call.

Cooked data: the cue `GC_Grenade_Explode` (`Content/GameplayCues/Weapon/`) is a `WDGameplayCueNotify_Actor` with only `OnExecute` and `SpawnEffects` (sound, Niagara, decal; Blueprint read). The thrown potato `B_HotPotato` (parent of Alpha/Bravo/Charlie, `HotPotato/Content/Data/Blueprints/`) sets `ExplosionDamageValues` `BaseDamage` 0, `ExplosiveRadius` 0, `ImpactDamage` 0, `bExplodeOnHealthDepleted` false; Alpha, Bravo and Charlie override none of them. `B_HotPotatoComponent` (player component) has only `BroadcastHotPotatoMessage(PassMultiplier)`, which makes the pre-lobby award event on a pass (round 39); no negative award. So the penalty round 57 inferred is not found: expiry costs the holder the potato and the chain of pass rewards, and plays the explosion effect. Whether the effect or the lobby knocks the player over is not in the data (static, not run).

Page: `hot-potato.md`.

## 4. Team Offence: who cancels the ballot at 180 s. NATIVE (server)

Ballot creation `0x893C7B0` (server only: it runs in the subsystem that owns the ballot array at subsystem `+56`, count `+64`, 152-byte records). Deadline: `settings.+68` (float, 180.0, round 57) plus the offence time (`0x893C7B0`, `v46 = settings+68 + descriptor+16`), stored as the double at record `+128`. At the end of the function (`0x893CE0D` to `0x893CF1C`): it gets the game state (world `+0x1B0`), calls its vtable `+0x768` (server world time, double), computes `max(deadline - now, 0)` in `xmm6` (`0x893CE50..0x893CE66`), and calls `0x3ED2C80` (timer manager set-timer; `rcx` timer manager from `0x45C0110`, `rdx` = handle at record `+136` (`rsi - 0x10`), `r8` = delegate bound to `0x893C060` with the ballot id, `xmm3` = rate, loop byte 0). So a one-shot server timer is armed for the remaining life of the vote.

Callback `0x893C060(subsystem, ballotId)`: finds the ballot; if it is not closed (`+144 == 0`) it collects voters whose answered flag (`voter +9`) is 0, removes them from the ballot (compaction loop), calls the tally `0x893D5E0`, then, for the removed voters, calls `0x893DB30` with the tag at `settings.+72` and a `Seconds` text parameter (inferred to be the "voter expired" notice, whose text with `{Seconds}` is from round 45) and `0x8939910` once per removed voter (inferred to dismiss the prompt; not read).

Tally `0x893D5E0`: sums voter weights (voter `+12`, 1.0 or 0.5 flagged); `half = total x 0.5`; `punish = sum of weights with answered and punish (+9 and +8)`; `waiting = sum of unanswered weights`. If `punish > half` the outcome is Punish (record `+145 = 1`); else if `punish + waiting > half` it returns and waits; else (including zero voters) Forgive (`+145 = 2`; SDK `EWDTeamOffenceBallotOutcome` Punish = 1, Forgive = 2). Closing clears the timer (`0x144552660`, handle `+136`). At the deadline `waiting` is 0 (the silent voters were just removed), so the ballot always closes there. Also `0x893C4E0` (voter logout) and the safe-zone path use the same tally.

The client prompt tick `0x893E180` (round 57) closes the prompt on the deadline it receives (`0x893AD40` sends the `+128` double); that is the display side only. So the server cancels, not only the client. Static; not run.

Page: `team-offence.md`.

## 5. Season 2 spotting versus destroying cash. FOUND

The patch note's "L2A6 artillery variant" was wrong twice: the rows are `TNK_01.Artillery`, which is the SPH-2 (`sph-2.md`: internal name `TNK_01 (artillery variant)`; the L2A6 is `TNK_01.Heavy`, the Gepard `TNK_01.AntiAir`). And the two amounts are in different rows of one table plus a third value in another table:

| Table | Row | Season 1 | Season 2 | Meaning |
|---|---|---:|---:|---|
| [`DT_ChallengeRewards_SessionEvents_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_Spotting.json) | `Challenges.Rewards.Spotting.Added.TNK_01.Artillery` `DefaultReward` | 1,500 | 400 | cash to the spotter when the spot is placed (`RefreshedReward` 750 to 200 when re-spotted) |
| same | `Challenges.Rewards.Spotting.Removed.TNK_01.Artillery` `DefaultReward` | 8,000 | 1,200 | cash to the spotter when the spotted vehicle is destroyed; `KilledByEnemyFactor` 0.25 applies when the enemy side did it, as in `spotting-challenges.md` |
| [`DT_ChallengeRewards_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_SessionEvents_Shared.json) | `Challenges.Rewards.VehicleDestroyed.TNK_01.Artillery` `BaseReward` | 14,000 | 8,000 | cash to the player who destroys the SPH-2 |

For comparison, Season 2 values for the other [`TNK_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_01/Content/TNK_01.json) rows: Heavy (L2A6) spot 750 (375 refreshed), spotted-destroyed 3,300, destroy 5,500; AntiAir (Gepard) spot 625 (325), spotted-destroyed 2,100, destroy 3,500. The season diff (`season-2-changes/player-movement.md`) lists the Added row 1,500 to 400 and the Removed row 8,000 to 1,200, which matches. Role XP for all three is unchanged here.

Pages: `patch-notes/season-2.md` (lines on spotting cash and challenge reward tables), `guides/faq.md` (one fact corrected: SPH-2, not L2A6).

## Wiki updates (done in this commit)

- `_wiki/game-modes-and-maps/bakurani.md`, `ozeti.md`, `zestafona.md`, `saburtulo.md`: "Cover materials" section (table, total, link to penetration page for densities), "Built-up area" infobox row, sources note; Saburtulo zone regions wording.
- `_wiki/game-modes-and-maps/unnamed-africa-layout.md`, `bakurani-outskirts-jutari.md`, `zone-layouts.md`: map area (Kenya absent, Jutari shares the Bakurani world), region slot empty.
- `_wiki/game-modes-and-maps/hot-potato.md`: expiry effect and no penalty (old: inferred penalty).
- `_wiki/game-modes-and-maps/team-offence.md`: the server ends the vote at the deadline and how it counts.
- `_wiki/patch-notes/season-2.md`, `_wiki/guides/faq.md`: SPH-2 spotting 400 / spotted-destroyed 1,200 / destroy 8,000, not L2A6.
- `_wiki/game-mechanics/penetration-and-ricochet.md`: "not yet known" points at the map articles.
- `content/Wardogs_Maps_v2.md` section 10 and `assets/data/map-cover-materials.json` (data); `content/Wardogs_UI_v2.md` minimap rows for Russia and NorthAmerica.
- No generator change and no regenerated page.
