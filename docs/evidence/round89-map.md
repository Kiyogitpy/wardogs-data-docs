# Round 89: map height grids and map asset unnamed fields (V4-22)

Static data read only. Nothing was run, no native code was traced. Evidence level: cooked JSON exports (`data/Wardogs/Content/Environment/Water/FluidFlux/**`, [`Content/Maps/Gyms/Water`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Maps/Gyms/Water), [`Content/Maps/SightBlockers`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Maps/SightBlockers)). Generator: `_tools/map_height_grids.py` (`--check`). Outputs: `assets/data/map-height-grids.json`, `assets/img/maps/{bakurani,ozeti,gym}-water-height.png`, the generated table in `content/Wardogs_Environment_v2.md` section 13b, section 4b and 7 of `content/Wardogs_Maps_v2.md`, a "Water height" section on the Bakurani and Ozeti wiki pages.

## Statuses

| # | Field / question | Status | Answer |
|---|---|---|---|
| 1 | `Heights` encoding | FOUND | `GridWidth` x `GridHeight` unsigned 16-bit values, row-major; row 0 at world Y = `worldmin.Y`, rows run toward +Y, columns toward +X from `worldmin.X`. |
| 2 | Meaning of 65535 | FOUND | No water in that cell (dry). 84% to 98% of cells per grid (gym 95.3%). |
| 3 | Scale / offset to world cm | FOUND | Other values `v` (0 to 65534): `z_cm = z0 + v/65534 * (z1 - z0)`. The smallest wet value is 0 and the largest 65534 in all 41 grids, so the range is normalised per grid. Heights are water surface heights, not terrain. |
| 4 | `_aaaajahedjfgkemenmnfj` (`z0`) and `_aaaajbpajedfcbkcoihjn` (`z1`) | FOUND | Lowest and highest water surface in the grid (cm). Both lie inside the linked state's box `[AreaLocation.Z - AreaSize.Z, AreaLocation.Z]` in all 41 grids; `z0` is within 2 cm of the box bottom plus 5 cm in 21 of them. |
| 5 | `_aaabflcohlopnaadhglfk` | FOUND | Soft reference to the linked `PDA_FluxSimulationState_C` (40 of 40 plus the gym). |
| 6 | Grid origin and cell size | FOUND | `worldmin` is the minimum corner (cm); `worldmin + WorldSize/2` equals the state's `AreaLocation` X and Y in 41 of 41. Cell = `WorldSize.X/GridWidth` by `WorldSize.Y/GridHeight`: 200 cm (34 map grids and the gym), 400 cm (2), 800 cm (3), 1200 cm (1). Grids are not always square (`GridHeight` 128 to 512). |
| 7 | Min/max height per map | FOUND | Bakurani (Kavkazi): 23 grids, -1,015.95 m to -805.93 m. Ozeti (Europe): 17 grids, -1,063.46 m to -883.03 m. Gym: -22.17 m to 20.46 m. |
| 8 | Grids for Zestafona and Saburtulo | ABSENT | The North America states have no grid asset and Russia has no flux assets at all (matches the "14 river sections" actor count, which has no grid). |
| 9 | Sight blocker 7-field block | FOUND (layout), not resolvable (runtime purpose) | See below. |
| 10 | Native reader of the grids | not resolvable here | Not traced (task said native code only if needed). The decode is closed on data: tile edge agreement and the box relations below. |

## Verification of the decode

- **Orientation and scale by tile overlap.** Neighbouring grids overlap on the map. Sampling the overlap, 35 same-world pairs have water on both sides; with row 0 at `worldmin.Y` and +Y with the row index the mean absolute height difference between the two grids is 3.5 to 364 cm (median about 29 cm), on per-grid ranges of 3 to 117 m. With the row order flipped, almost no pair has water on both sides.
- **Rivers connect.** `bakurani-water-height.png` and `ozeti-water-height.png` show continuous rivers that fall steadily downstream, flat lakes (Ozeti's northern lake is one colour), and river branches that join, across tile borders. The play box (zone regions plus 500 m, `map-boundaries.json`) is drawn on each image: the Bakurani river enters from the north and meets the east-west river inside it and the Ozeti river crosses it east to west.
- **Landmark.** Hot Zone Magnet tower z on Bakurani is -917 m (`map-magnets-extents.json`) and the water range is -1,016 to -806 m; ground in the play box is -991 to +251 m (round 68), so water sits at or under the ground. World `KillZ` is -1,500 m, below all water.
- **Box relations.** `AreaLocation.Z - CaptureOffset` is exactly 0.75 x `AreaSize.Z` in all 41 states, and `z0` equals `AreaLocation.Z - AreaSize.Z + 5` cm (within 2 cm) in 21 grids, i.e. the heights are in the same world Z as the state box. Sample distribution of the gym (95.3% at 65535) matches the earlier count.
- Run: `python -I _tools/map_height_grids.py --check` exits 0; it asserts per grid that `Heights.size = GridWidth * GridHeight` and that the wet minimum is 0 and maximum 65534.

## Sight blockers: the seven unnamed fields (`WDSightBlockerBakedDataAsset`)

The "seven unnamed fields" per map asset are the properties of the inner struct `_aaaajmobmggidbdjfpocf` (one is already named, `SphereRadius`). Checked on all four assets (Europe 3125 spheres/384 instances, North America 2880/185, Russia 4833/708, Kavkazi 4546/813):

| Field | Status | Reading from values |
|---|---|---|
| `_aaaamnbgmbebkhjgdpodm` | FOUND | Per-sphere centre (X, Y, Z) in cm; all lie inside the asset's bounds box. |
| `_aaaamhopkmmkgfmimfdeo` | FOUND | Identical copy of the centre array (equal in all four assets). |
| `SphereRadius` (named) | FOUND | 148.5 to 222.8 cm. |
| `_aaaaohkppedakmnmcadii` | FOUND | Squared radius: equals `SphereRadius`^2 to a relative error under 1e-7. |
| `_aaaalfdjjflfjimdifpgi` | FOUND (layout) | Per-sphere `Start`/`Count`, always `Start` = sphere index and `Count` = 1. Role of the range not resolved. |
| `_aaaaionfifjecfgkkalml` | FOUND (layout) | Per-sphere `Start`/`Count`, all zero in all four assets (empty ranges). Role not resolved. |
| `_aaaaoeihhdopijahgcelp` | FOUND (layout) | Instance table, one row per instance: running index, `Key` {`Cell` X,Y ints, `MeshId` 1 to 7, `InstanceID`} (`_aaaamebjchmcpoboffena` is the running index). How instances tie to spheres is not resolved (spheres outnumber instances 4 to 8 times). |

Top level: `_aaabbmbilgonhfinicfad` = sphere count (equals the array lengths), `_aaabinandjigbbhlnddom` = instance count (equals the instance table), `_aaaaklfjghingmcjnffnc` = one-element list of the world soft path, `_aaaaljhigckboolllndci` = bounds box (FBox, IsValid 1), 22 to 65 cm wider than the sphere centres in X and Y and much taller in Z. What a sight blocker does in play is not decoded.

## Not done

- The warmup manifest unnamed fields (`_aaaapdikiogmbgbndfgmm` is the world soft path, `_aaaamebjchmcpoboffena` is a running index) were only looked at in passing.
- No native code was read.
