# Round 85: page hygiene (stale "not decoded" wording)

Teammate hyg, cluster E of `BACKLOG-v4` (census v4). Each stale sentence was checked against the page or evidence file that now documents the fact. Resolved sentences were reworded to state the fact briefly or to link the page that has it. Sentences still open were left alone. No generated block (`<!-- ... -->` marker) was touched and no number was changed.

## Changed (11 hits)

| File | Old phrase | New text (summary) | Source of the fact |
|---|---|---|---|
| `game-features/Wardogs_GameFeatures_Ammo_v2.md` (section 5) | "The `AmmoModifiers` assets are the most likely source of ammo types ... Their damage and behaviour values were not checked in this pass" | Assets are the source of ammo types, indexed by [`DT_AmmoModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DT_AmmoModifiers.json); values linked to Game Mechanics v2 section 2e | `content/Wardogs_GameMechanics_v2.md` section 2e (penetration, range, exit speed, tracer chance per asset); [`DT_AmmoModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DT_AmmoModifiers.json) index in `content/Wardogs_DataTables_v1.md` |
| `game-features/Wardogs_GameFeatures_Ammo_v2.md` (section 6) | "Their contents were not decoded here; a dedicated pass ... would be needed for ammo values" | Values tabled in Game Mechanics v2 section 2e | same as above |
| `content/Wardogs_GameMechanics_v2.md` (load and extract curve table) | `LoadAmmo` family: "not decoded in review" | Loading time curves, linked to Ammo Packing | `game-features/Wardogs_AmmoPacking_v1.md` (rule `UWDCustomInventoryOperationRule_LoadAmmo`, `CR_LoadAmmoCurve_*` rows) |
| `content/Wardogs_GameMechanics_v2.md` (curve note under that table) | "The curve axis is not labelled ... not verified" | X axis is the round count; packing time is curve(rounds) times a multiplier (Derived) | `game-features/Wardogs_AmmoPacking_v1.md` (curves evaluated at the round count, time = curve(rounds) x multiplier) |
| `content/Wardogs_GameMechanics_v2.md` (player curve table) | `CurveFloat` (9) and `CurveVector` (4) ... "(not decoded)" | Animation and camera curves; several tabled in Player Movement | `content/Wardogs_PlayerMovement_v1.md` (curve table, section 3 and slope/look curves) |
| `content/Wardogs_GameMechanics_v2.md` (limitations) | "Player curves. The 9 CurveFloat and 4 CurveVector assets ... were not decoded." | Several tabled in Player Movement; animation and camera uses of the rest not decoded | same as above |
| `game-features/Wardogs_GameFeatures_Vehicles_v2.md` (limitations) | "wheel-level MWheeledVehicleWheelDataAsset values ... are not tabled" | Friction values tabled in Vehicle Assets section 14; `Values[0..2]` meaning still unconfirmed | `game-features/Wardogs_VehicleAssets_v1.md` section 14 (`LateralFriction.Values`, `LongitudinalFriction.Values`) |
| `game-features/Wardogs_GameFeatures_Weapons_v2.md` (limitations) | "ADS, recoil, view kick, sway and falloff curves ... They are not decoded." | Keyframes tabled with every key in Weapon Spread and Recoil Data; falloff in Weapons v2; 7 standalone `CurveFloat` still not decoded | `content/Wardogs_WeaponSpreadRecoilData_v1.md` and `assets/data/weapon-spread-recoil.json`; `content/Wardogs_Weapons_v2.md` (distance damage falloff) |
| `game-features/Wardogs_GameFeatures_WorldFeatures_v2.md` (header line) | "StateTree internals were summarised, not decoded." | Pointer to Challenges v1 | `game-features/Wardogs_Challenges_v1.md` (event tag, branches and conditions per tree, incl. `ST_Challenges_SessionEvents_KOTH_HotZoneMagnet_*`) |
| `game-features/Wardogs_GameFeatures_WorldFeatures_v2.md` (section 4, HotZone) | "They are not decoded here." | Events and conditions tabled in Challenges v1 | same as above |
| `game-features/Wardogs_GameFeatures_WorldFeatures_v2.md` (limitations) | "StateTree logic ... summarised, not decoded. Triggers and conditions are not confirmed." | Triggers and conditions tabled in Challenges v1 | same as above |

## Left open (5 hits)

| File | Phrase | Why left open |
|---|---|---|
| `game-features/Wardogs_GameFeatures_Vehicles_v2.md` (restock column note) | "The restock semantics and tag are not decoded." | Still open. Only name-based reading exists (line about `RestockSuppliesNeeded` "inferred from names"). No page or evidence file gives the rule. |
| `game-features/Wardogs_GameFeatures_Spotting_v2.md` (reward lookup) | "The `Player` target ... path that pays a spotted player was not traced." | Still open per BACKLOG-v4 V4-13. No evidence file traces the pay path. |
| `game-features/Wardogs_GameFeatures_Spotting_v2.md` (limitations) | "The `Player` target has a calculator row but no lookup row. The path ... was not traced." | Same as above. |
| `game-features/Wardogs_GameFeatures_Weapons_v2.md` (section 10) | "7 `CurveFloat` objects ... not decoded here" (standalone curves, table row) | Still open per BACKLOG-v4 V4-19. The keyframes inside `WDWeaponStatsData` are now decoded (changed above); the 7 standalone assets are not. |
| `content/Wardogs_Items_v2.md` | census phrase "damage modifier stacking / requirements not decoded" | Phrase not found in this page. Remaining `not decoded` lines there (ammo crate placeable, holdable fields) are outside this cluster and still open. |

## Checks

- `python -I _tools/check_links.py`: no broken links (0 broken).
- Secrets grep on `git diff main...HEAD`: no hits.
