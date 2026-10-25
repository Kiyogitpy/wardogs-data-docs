# Round 55: Season 2 changes to the infantry and buildable damage tables

Static analysis only. Nothing was run in game. Status labels: FOUND (read in cooked data), NATIVE (read in the executable), SERVER (decided server side, not visible), ABSENT (searched for, not there).

The Season 2 notes said these were "meaning not clear from the data": infantry global damage entries (entry 89, -13 to -30, new `Percentage_Ongoing` entries) and the buildable damage table entries. Both are readable. Every entry carries its own requirement lists in the cooked JSON (source tag, target tag, hit location), so no package bytes were needed. The only thing the season diff could not give was the match between a Season 1 entry and a Season 2 entry, because Season 2 inserted entries and every later index moved. This round diffs by content instead of by index.

Reproduce: `python -I _tools/round55_s2_damage_diff.py` (Season 1 export at `E:/r22/s1/data`, the same input as `_tools/season_diff.py`). The buildable factors use the round 42 evaluator `_tools/structure_hits.py`.

## How an entry is read

R55-1. **What an entry matches.** An entry applies when every tag in `SourceRequirements` is in the lineage of the hit's source tags (the projectile tag, its context tags such as `Meta.Damage.Arms.High`, the ammo modifier tag, the weapon tag), every tag in `TargetRequirements` is in the lineage of the target hit piece's tags, and the hit location is under one of `PossibleHitLocations`. Empty lists match anything. A parent tag matches its children (`Meta.Damage.Armor` matches `Armor.Light` to `Armor.SuperHeavy`; `Meta.Damage.HitLocation.Infantry` matches every body part). Status: NATIVE (collector and evaluator, [Damage Pipeline 4 to 6](../../pipelines/Wardogs_DamagePipeline_v2.md)); the entries FOUND.

R55-2. **What `Percentage_Ongoing` means.** Amount `a` multiplies the running damage by `1 + a/100`: -30 is x0.70, -13 is x0.87, +35 is x1.35, 0 is no change. Entries multiply, they do not add, so order does not matter. This is the factor established in [round 52](round52-explosives-vs-vehicles.md) (R52-2). The infantry table and the buildable table use the same evaluator. Status: NATIVE for the arithmetic.

R55-3. **Amount 0 is an empty slot, not a rule.** Entries with `Percentage_Ongoing` and Amount 0.0 and no custom class multiply by 1.0. Season 2 added several (see the table) and removed several; they change nothing. Status: FOUND.

R55-4. **Custom operation entries ignore Amount.** Entry 6 has `bUseCustomOperation` and a Blueprint class; the Amount field is unused, and the class returns `C x W - C` (a factor of W) from a data table (R55-5). Status: FOUND (class and table), NATIVE (arithmetic, Damage Pipeline 7.2).

## Infantry table: DT_GlobalDamage_InfantryData (row Meta.Damage.Infantry)

Season 1 had 129 entries, Season 2 has 146. By content, 5 entries went and 22 came. Indexes below: "S2" is the Season 2 index (the one the season diff prints as "Entry N"), "S1" is the Season 1 index. The combined diff showed Season 1 index 83 as entry 89 because six entries were inserted before it.

### Entry 89: 12 gauge rifled slug against a vest (-13 to -30)

R55-6. S1 83 and S2 89 are the same entry. Source `Meta.Damage.Bullet.12g.RifledSlug`, target `Meta.Damage.Armor` (any vest class: Light, Medium, Heavy, Super heavy), location `HitLocation.Infantry` (any body part), category AmmoModifier. Amount -13.0 became -30.0, so the factor went from x0.87 to x0.70. It stacks with the vest's own reduction, with the slug's other entries (helmet -5, Super heavy helmet -12, both unchanged: S2 87 and 88) and with the Special/Small arm class rules. Status: FOUND. The rule matches only a hit piece that carries an `Armor` tag, so it is a vest-covered part (the helmets carry `Helmet` tags and have their own slug entries).

Weapons: the slug is the 12 gauge rifled round, used by the M500 and MP43 (shotguns that take the `12g` caliber).

### New entries 26, 27, 29, 30, 31: arrows against armor

R55-7. Source `Meta.Damage.Bullet.Arrow` (the Compound Bow's combat arrow and explosive arrow share the tag). Season 1 had only three no-op entries for arrows (S1 24, 25, 26: Armor 0, Helmet 0, no target 0). Season 2:

| S2 | Target | Amount | Factor |
|---:|---|---:|---:|
| 26 | Heavy vest | -10 | x0.90 |
| 27 | Super heavy vest | -34 | x0.66 |
| 29 | Light helmet | 0 | x1.00 (empty) |
| 30 | Heavy helmet | -10 | x0.90 |
| 31 | Super heavy helmet | -34 | x0.66 |

Light and Medium vests and the Medium helmet have no entry: x1.00. The removed S1 25 (Armor, Arrow, 0) was a no-op; its place is taken by the four per-class entries. Status: FOUND.

### New entry 6: weapon type by round (custom, Amount unused)

R55-5. S2 entry 6 (source `Meta.Damage.Bullet`, location `HitLocation.Infantry`, category Calibre) runs `B_ArchetypeCaliberModifiers_C` against the new table `DT_InfantryData_ArchetypeCaliberModifiers`. Neither the entry nor the table exists in Season 1 (the Season 1 `DT_Helpers` folder has three tables, Season 2 has four). The row is the weapon type from the hit's context (`Meta.Damage.Weapon.AR`, `.DMR`, `.LMG` and so on); the key is the caliber. A bullet whose weapon type has no row, or whose caliber has no key, gets x1.0. The factors that are not 1.0:

| Weapon type | Round | Factor | Weapons |
|---|---|---:|---|
| Assault rifle | .308 Winchester | x0.75 | FAL |
| Assault rifle | 7.62x39 mm | x0.88 | TCX-SPR |
| Designated marksman rifle | .308 Winchester | x0.85 | BMR-308, M14 |
| Designated marksman rifle | 7.62x54R | x0.80 | SVD |
| Light machine gun | 7.62x54R | x0.75 | PKM |
| Light machine gun | .308 Winchester | x0.75 | Evo-3 Ultra |

Every other pairing in the table is x1.0 (5.56 and 5.45 rifles, the SKS's 7.62x39 as a marksman rifle, every sniper rifle, all pistols, SMGs, shotguns, the Compound Bow, the mounted M2 Browning, the vehicle machine guns and miniguns, the .50 cal turret). This is on top of the Season 2 base damage cuts (.308 60 to 45, 7.62x54R 55 to 44). Status: FOUND. The published weapon articles already include it (they are built with `_tools/damage_tables.py`, which has used the table since round 24); the patch notes did not mention it.

### New entries 118 and 119: autocannon rounds against players

R55-8. Sources `Meta.Damage.Cannon.35x228mm` (Flakpanzer Gepard) and `Meta.Damage.Cannon.20x102mm` (Vanguard CIWS and the other stationary 20 mm guns), location any body part, category AmmoModifier, Amount -30 each: x0.70. Season 1 had no entry for either caliber (only the generic `Cannon` entries, which remain: the -75 bone entry S2 10 and the armor and helmet effectiveness entries S2 139 and 141, unchanged). Status: FOUND.

### New entries 109 and 115: blast outer ring against players

R55-9. Source `Explosive.Rocket.125mm` plus `Explosive.Radius.Outer` (the T-72B3 cannon shell) and `Explosive.Grenade.40mm` plus `Explosive.Radius.Outer` (the MGL-40 grenade), Amount -50 each: x0.50 in the outer ring, in addition to the distance falloff. The inner ring and a direct hit are untouched. The same -50 already applied to the 84, 93 and 120 mm rockets (S2 111 to 113 are the old S1 102 to 104, unchanged) and -55 to the 155 mm. Status: FOUND.

### New entry 106: Molotov against a Super heavy vest

R55-10. Source `Explosive.Utility.Molotov`, target `Armor.SuperHeavy`, Amount -30: x0.70 for a hit that lands on a Super heavy vest. No entry for lighter classes. Status: FOUND. Whether the burning area applies its damage per tick through this evaluator or by another route is not traced; the entry is read from the table only.

### New entries 124 to 131: .50 cal rounds against players

R55-11. Source `Meta.Damage.Bullet.50Cal`, category PenetrationEffectiveness. These are the AMR 50 and the mounted M2 Browning (the 50 Cal caliber's weapon types are `Weapon.Sniper` and `Weapon.HMG.MWSY_001`, and the 12.7 mm vehicle turret `Weapon.Vehicle.Turret.STN_06`). Season 1 had two empty entries for it (S1 113: Armor 0, S1 114: Helmet 0) and nothing else.

| S2 | Where | Amount | Factor |
|---:|---|---:|---:|
| 124 | Head, neck | -15.6 | x0.844 |
| 125 | Upper torso | -12.5 | x0.875 |
| 126 | Middle torso, lower torso | -6.0 | x0.94 |
| 127 | Middle torso, lower torso | -7.7 | x0.923 |
| 128 | Heavy vest | -10 | x0.90 |
| 129 | Super heavy vest | -12.5 | x0.875 |
| 130 | Heavy helmet | -10 | x0.90 |
| 131 | Super heavy helmet | -20 | x0.80 |

Entries 126 and 127 are identical in the export except for the amount: both list middle and lower torso. Both match, so a middle or lower torso hit takes x0.94 x 0.923 = x0.868. It is possible the second was meant for another body part (the pelvis is the part missing from the list); the data cannot show it, so the published value follows the data. Light and Medium vests and helmets, and every other body part, have no entry (x1.00). Location entries multiply with the armor-class entries (a head hit into a Super heavy helmet gets x0.844 x 0.80). Status: FOUND (126 and 127 duplicate locations: as exported).

### New entry 136 and removed S1 116: Super heavy helmet

R55-12. S2 136: target `Helmet.SuperHeavy`, source `Bullet` plus `AmmoModifier.ArmorPiercing` plus `Weapon.Sniper`, Amount -20: armor-piercing sniper rounds (SV98, Mosin Nagant, MK22, AMR 50, Scout Rifle TD) do x0.80 to a Super heavy helmet. Removed S1 116: target `Helmet.SuperHeavy`, source `Meta.Damage.Arms.High`, Amount -25: in Season 1 every round of the High arm class (7.62x39, 7.62x51, 7.62x54R, .308, .338 Norma Magnum, .50 AE, 30 mm, arrows) did x0.75 to a Super heavy helmet. Season 2 dropped it. (The Season 2 armor reduction also fell, Super heavy 65 to 60%.) For a full metal jacket 7.62 hit the share of damage that gets through a Super heavy helmet went from about 26% (0.35 left after a 65% reduction, times 0.75) to 40% (a 60% reduction, no extra cut). Status: FOUND.

### New entry 41: empty

R55-13. S2 41: source `Bullet.556mm` plus `Weapon.Sniper.WEPN_035` (Scout Rifle TD), head and neck, category Weapon, Amount 0.0. A placeholder: x1.00. The Scout Rifle TD has no head or neck rule in Season 2. Status: FOUND (no effect).

### Entry accounting

| Kind | S2 entries |
|---|---|
| Changed amount | 89 (S1 83) |
| New rule with effect | 6, 26, 27, 30, 31, 106, 109, 115, 118, 119, 124 to 131, 136 |
| New empty slots (Amount 0) | 29, 41 |
| Removed with effect | S1 116 |
| Removed empty slots | S1 25, 113, 114 |

Total 22 added, 5 removed.

## Buildable table: DT_GlobalDamage_BuildableData

Rows are named by the structure's damage tag; the structure is found from the `Meta.Damage.Buildable.*` tag in its data asset (`DA_Buildable_*`). Mapping used: FOB = Forward Operating Base; Door; BarbedWire = Barbed Wire; AirRaidShelter = Indirect Fire Shelter; Bunker; CamoTent = Recon Tent; CrowsNest = Recon Tower; SmallHesco = Hesco Block (Small); LargeHesco = Hesco Block (Large); QuadLargeHescoWall = Hesco Wall; HescoGate = Gate; BuildableHotzoneMagnet = Drill Rig; RepairStation and RefuelStation; SandbagWall; TankTrap = Hedgehog; Radio = Builder's Radio; BremmerWall = Bremer Wall; SV_Shelter = Shelter; WoodBase = Wood base. Status: FOUND.

R55-14. **What changed.** Three sources: `Cannon.35x228mm` (Flakpanzer Gepard), `Cannon.20x102mm` (Vanguard CIWS and the other stationary 20 mm guns) and `Explosive.Rocket.125mm` (T-72B3 cannon shell). All 18 Season 1 rows gained a 125 mm entry (amounts below; three of them are 0, a no-op). Ten rows gained a 20 mm entry. Six rows had their 35 mm amount changed. The `Cannon.30mm` and generic `Explosive.Rocket` rules are unchanged. Status: FOUND.

Damage factor against each structure, Season 1 to Season 2 (damage divided by the round's base damage, all matching entries multiplied; the 125 mm shell also meets the generic rocket rule, which is why its factors are above 1). "Hits" is the count for the main part at point blank, derived as in round 42.

| Structure | 35 mm cannon | 20 mm cannon | 125 mm shell | 125 mm hits |
|---|---|---|---|---|
| Forward Operating Base | 0.80 to 0.80 | 1.0 to 0.80 (new -20) | 15.0 to 20.25 (new +35) | 7 to 5 |
| Door | 0.20 to 0.08 | 1.0 to 0.08 | 7.5 to 3.75 (new -50) | 2 to 4 |
| Gate | 0.60 to 0.50 | 1.0 to 0.50 | 9.5 to 7.6 (new -20) | 4 to 5 |
| Hesco Block (Small) | 0.25 to 0.08 | 1.0 to 0.08 | 2.2 to 2.75 (new +25) | 5 to 4 |
| Hesco Block (Large) | 0.15 to 0.08 | 1.0 to 0.08 | 1.8 to 2.16 (new +20) | 9 to 7 |
| Hesco Wall | 1.0 to 1.0 | 1.0 to 1.0 | 3.0 to 1.5 (new -50) | 11 to 21 |
| Bremer Wall | 0.30 to 0.20 | 1.0 to 0.20 | 3.5 to 4.025 (new +15) | 13 to 11 |
| Builder's Radio | 0.25 to 0.20 | 2.0 to 2.0 | 11.0 to 11.0 (new 0) | 1 to 1 |
| Repair and Refuel Station | 0.25 to 0.25 | 1.0 to 0.25 | 16.0 to 12.8 (new -20) | 1 to 1 |
| Sandbag Wall | 0.20 to 0.20 | 1.0 to 0.20 | 7.5 to 3.75 (new -50) | 1 to 2 |
| Hedgehog | 0.25 to 0.25 | 0.5 to 0.5 | 5.5 to 3.85 (new -30) | 6 to 8 |
| Drill Rig | 0.135 to 0.135 | 1.0 to 0.135 | 9.5 to 7.6 (new -20) | not computed |
| Indirect Fire Shelter, Bunker, Recon Tower | 1.0 to 1.0 | 1.0 to 1.0 | 1.45 to 1.015 (new -30) | 23 to 33 |
| Barbed Wire, Recon Tent | 0.2 to 0.2 | 0.5 to 0.5 | 3.0 to 3.0 (new 0) | 1 to 1 |

The new 20 mm entries are: FOB -20, Door -92, Gate -50, Hesco Block (Small) -92, Hesco Block (Large) -92, Bremer Wall -80, Repair Station -75, Refuel Station -75, Sandbag Wall -80, Drill Rig -86.5. The changed 35 mm amounts: Door -80 to -92, Hesco Block (Small) -75 to -92, Gate -40 to -50, Hesco Block (Large) -85 to -92, Builder's Radio -75 to -80, Bremer Wall -70 to -80. The 125 mm amounts: FOB +35, Door -50, Gate -20, Hesco Block (Small) +25, Hesco Block (Large) +20, Hesco Wall -50, Bremer Wall +15, Repair and Refuel Station -20, Sandbag Wall -50, Hedgehog -30, Drill Rig -20, Indirect Fire Shelter, Bunker and Recon Tower -30, Barbed Wire, Recon Tent and Builder's Radio 0.

R55-15. **The "5 to 17 percentage points" in the old wiki sentence** is the 35 mm cannon amount changes (-40 to -50 is 10, -75 to -80 is 5, -70 to -80 is 10, -80 to -92 is 12, -85 to -92 is 7, -75 to -92 is 17). The "six values in three entries" in the Sandbag Wall article is the same group. Status: FOUND.

R55-16. **New rows.** `Meta.Damage.Buildable.WoodBase` (22 entries) and `Meta.Damage.Buildable.SV_Shelter` (23 entries) exist only in Season 2: the Season 1 export has no row and no `DA_Buildable_WoodBase` or `DA_Buildable_Shelter`. They are not "changes" in the table sense; against the Wood base the 35 and 20 mm cannons do x0.20, the 125 mm shell x3.75 (2 hits); against the Shelter the cannons x0.08 and the shell x2.16 (7 hits). Status: FOUND.

R55-17. **Order of tags is irrelevant for outcomes; categories are not read.** `CaliberEffectiveness`, `Calibre` and `AmmoModifier` are only ordering labels for the evaluator. Status: NATIVE.

## Task B: MG Nest lock-on target list (round 42 B7)

R55-18. Round 42 item B7 (`round42-econ-buildables.md`) says the MG Nest has no target list ("the gun is a player-operated stationary weapon, so there is nothing to list"). That is wrong. `WE_STN_06_MountedMachineGun` (data path `Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Weapons/WeaponExtensions/WE_STN_06_MountedMachineGun.json`) has a lock-on block with `TimeToTarget` 2.0, `FireDelayAfterLock` 0.5, `bOnlyFireWhenLockedOn` true and an `AllowedTargets` list of seven air variants: Littlebird.Default, Littlebird.MountedMachineGuns, Littlebird.RocketPods, ROT_01.Default, ROT_01.MountedMachineGuns, Havoc.Default and Airplane.FWG.Default. No ground vehicle, no emplacement, no infantry. Round 54 found it; I re-read the file and confirm it. The wiki is right: `_wiki/building/mg-nest.md` already says "a target list of air vehicles only (the Little Bird family, the Havoc, the Huey and the fixed-wing airplane), with fire allowed only while locked on" and "the data does not show how a gun that a player operates uses it". No wiki change was needed. Status: FOUND (B7 corrected: targets FOUND, air only; the earlier search missed the block because it looked for a target list in the stats asset and the actor data, not in the weapon extension's lock-on struct). How the lock is used by a player-operated gun stays unknown (not traced).

A correction note was added next to B7 in `round42-econ-buildables.md`.

## Wiki updates

| Wiki file | Change |
|---|---|
| `_wiki/patch-notes/season-2.md` | Damage and armor: bullets for entries 89, arrows, weapon-type multipliers, cannon rounds, blast outer ring, Molotov, .50 cal, Super heavy helmet; structure bullets for the 35 mm, 20 mm and 125 mm rules |
| `_wiki/game-mechanics/health-and-damage.md` | New section "Rules that depend on the weapon or the round" with current values |
| `_wiki/game-mechanics/armor.md` | New section on rounds with their own armor rules |
| `_wiki/building.md` | "do not say which structures" sentence replaced with the decoded rules |
| `_wiki/building/*.md` | Season 2 changes sections: the cannon and shell rules for the structure |
