---
title: Round 23 projectile drag survey
nav_exclude: true
---

# Round 23 projectile drag survey

Question from [round 21](round21-artillery-range-check.md): the Standard 155 mm shell carries `DragModel.Value` 80 against 2.5 on the Expensive one. Is
80 alone, and what does each large value imply? Every `WDProjectileData` asset in `data/` was read (not only the Caliber folders), omitted fields were
filled from the `FWDProjectileStats` constructor defaults (Value 1.0, Length 1.5, Diameter 0.9, Mass 0.00746; see [Projectile Flight §5](../../pipelines/Wardogs_ProjectileFlight_v1.md)),
and the drag term and integrator of `_tools/shell_sim.py` were run on each. Nothing is fitted. Regenerate with `python -I _tools/projectile_drag_survey.py`.

Labels: **Data** is read from the assets; **Derived** is arithmetic on the documented force model; **Assumed** is a yardstick chosen here.

## Survey (Data)

37 projectile data assets; 24 set DragModel.Value (median 1.4); the others use the constructor default 1

| Asset | Calibre tag | DragModel.Value | Curve row | Mass (kg) | Diameter (cm) | Length (cm) | Actor moves it |
|---|---|---:|---|---:|---:|---:|---|
| `DA_155mm_Expensive_ProjectileData_SB` | `Item.Caliber.155mm.Expensive.Sandbox` | 80 | GC (Cylinder) | 70 | 8.4 | 25.4 | yes |
| `DA_155mm_Standard_ProjectileData` | `Item.Caliber.155mm.Standard` | 80 | GC (Cylinder) | 70 | 8.4 | 25.4 | yes |
| `DA_155mm_Standard_ProjectileData_SB` | `Item.Caliber.155mm.Standard.Sandbox` | 80 | GC (Cylinder) | 70 | 8.4 | 25.4 | yes |
| `DA_120x800mm_Standard_ProjectileData` | `Item.Caliber.120x800mm.Standard` | 11.5 | GC (Cylinder) | 15 | 12 | 8 | yes |
| `DA_120x570mm_ProjectileData` | `Item.Caliber.120x570mm` | 10 | GC (Cylinder) | 20 | 12 | 57 | yes |
| `DA_125x570mm_ProjectileData` | `Item.Caliber.125x570mm` | 10 | GC (Cylinder) | 23 | 12.5 | 65 | yes |
| `DA_Arrow_Explosive_ProjectileData` | `Item.Caliber.Arrow.Explosive` | 10 | GC (Cylinder) | 0.045 | 0.85 | 75 | no |
| `DA_155mm_Expensive_ProjectileData` | `Item.Caliber.155mm.Expensive` | 2.5 | GC (Cylinder) | 19 | 10.5 | 40 | yes |
| `DA_Arrow_Combat_ProjectileData` | `Item.Caliber.Arrow` | 2.5 | None | 0.029 | 0.65 | 75 | no |
| `DA_30mm_ProjectileData` | `Item.Caliber.30mm` | 2 | GC (Cylinder) | 0.22 | 3 | 29 | no |
| `DA_545mm_ProjectileData` | `Item.Caliber.545mm` | 1.4 | G7 (Boat Tail) | 0.0034 | 0.56 | 1.71704 | no |
| `DA_93mm_ProjectileData` | `Item.Caliber.93mm` | 1.4 | GC (Cylinder) | 2 | 9.3 | 72 | yes |
| `DA_7mmBuckshot_ProjectileData` | `Item.Caliber.7mmBuck` | 1.3 | GA (Pellet) | 0.004 | 0.83282 | 0.7 | no |
| `DA_45ACP_ProjectileData` | `Item.Caliber.45ACP` | 1.27 | G1 (Flat Bottom) | 0.015 | 1.15 | 0.95758 | no |
| `DA_9mm_ProjectileData` | `Item.Caliber.9mm` | 1.27 | G1 (Flat Bottom) | 0.007 | 0.9017 | 1.0541 | no |
| `DA_556mm_ProjectileData` | `Item.Caliber.556mm` | 1.26 | G7 (Boat Tail) | 0.0041 | 0.57 | 1.2696 | no |
| `DA_BatteryCharge_ProjectileData` | `Item.Caliber.BatteryCharge` | 1.26 | G7 (Boat Tail) | 0.0041 | 0.57 | 1.2696 | no |
| `DA_762mm_ProjectileData` | `Item.Caliber.762mm` | 1.2 | G7 (Boat Tail) | 0.008 | 0.792 | 1.4986 | no |
| `DA_122_mm_HAVOC_ProjectileData` | `Item.Caliber.122mm.Havoc` | 1 (default) | GC (Cylinder) | 57 | 12.2 | 254 | yes |
| `DA_122mm_ProjectileData` | `Item.Caliber.122mm` | 1 (default) | GC (Cylinder) | 57 | 12.2 | 254 | yes |
| `DA_20x102mm` | `Item.Caliber.20x102mm` | 1 (default) | G7 (Boat Tail) | 0.04 | 1 | 9.9 | no |
| `DA_45Colt_ProjectileData` | `Item.Caliber.45Colt` | 1 (default) | G1 (Flat Bottom) | 0.01 | 1.14 | 1.8796 | no |
| `DA_50AE_ProjectileData` | `Item.Caliber.50AE` | 1 (default) | G7 (Boat Tail) | 0.019 | 1.27 | 3.2 | no |
| `DA_50Cal_ProjectileData` | `Item.Caliber.50Cal` | 1 (default) | G7 (Boat Tail) | 0.051 | 1.2954 | 5.867 | no |
| `DA_70mm_ProjectileData` | `Item.Caliber.70mm` | 1 (default) | GC (Cylinder) | 10.1 | 12 | 137 | no |
| `DA_72mm_ProjectileData` | `Item.Caliber.72mm` | 1 (default) | G7 (Boat Tail) | 9.2 | 7.2 | 142 | yes |
| `DA_12g_RifledSlug_ProjectileData` | `Item.Caliber.12g.RifledSlug` | 1 (default) | GL (Blunt Nose) | 0.028 | 1.85 | 3 | no |
| `DA_84mm_ProjectileData` | `Item.Caliber.84mm` | 1 (default) | GC (Cylinder) | 2.3 | 8.4 | 25.4 | yes |
| `DA_TVGuidedMissile_Data` | `Item.Caliber.84mm.TVGuided` | 1 (default) | GC (Cylinder) | 2.3 | 8.4 | 25.4 | yes |
| `DA_DebugHomingRocketData` | `Item.Caliber.84mm` | 1 (default) | GC (Cylinder) | 1 | 4 | 37 | no |
| `DA_Drone_ProjectileData` | `Item.Caliber.DroneProjectile` | 1 (default) | GC (Cylinder) | 10 | 10 | 130 | yes |
| `DA_308Winchester_ProjectileData` | `Item.Caliber.308Win` | 0.9 | G7 (Boat Tail) | 0.012 | 0.782 | 3.2 | no |
| `DA_762x54mm_ProjectileData` | `Item.Caliber.762x54mm` | 0.9 | G7 (Boat Tail) | 0.011729 | 0.79248 | 3.048 | no |
| `DA_762x51mm_ProjectileData` | `Item.Caliber.762x51mm` | 0.89 | G7 (Boat Tail) | 0.01 | 0.782 | 2.78994 | no |
| `DA_40mm_ProjectileData` | `Item.Caliber.40mm` | 0.8 | GC (Cylinder) | 0.23 | 4 | 9.8806 | yes |
| `DA_338Norman_ProjectileData` | `Item.Caliber.338Nor` | 0.72 | G7 (Boat Tail) | 0.01944 | 0.86106 | 3.02006 | no |
| `DA_35x228mm_ProjectileData` | `Item.Caliber.35x228mm` | 0.5 | G7 (Boat Tail) | 0.375 | 3.5 | 14 | no |

`Actor moves it` is `bActorHandlesProjectileMovement`; the drag lookup is the same native function either way ([Projectile Flight §7](../../pipelines/Wardogs_ProjectileFlight_v1.md)).

## Outliers (Data)

Outliers (Value above 3 x the median 1.4): DA_120x570mm_ProjectileData (10), DA_120x800mm_Standard_ProjectileData (11.5), DA_125x570mm_ProjectileData (10), DA_155mm_Expensive_ProjectileData_SB (80), DA_155mm_Standard_ProjectileData (80), DA_155mm_Standard_ProjectileData_SB (80), DA_Arrow_Explosive_ProjectileData (10). In three tiers:

1. **Value 80, mass 70 kg, diameter 8.4 cm: `DA_155mm_Standard_ProjectileData`, `DA_155mm_Standard_ProjectileData_SB` and `DA_155mm_Expensive_ProjectileData_SB`.**
   The last one is tagged `Item.Caliber.155mm.Expensive.Sandbox` but carries the Standard numbers, not the Expensive 2.5 / 19 kg / 10.5 cm. 80 is 57 times the
   median and 32 times the Expensive 155. Nothing else in the data comes within a factor of seven of it.
2. **Value 10 to 11.5 on the 120/125 mm tank rounds** (`DA_120x570mm` 10 / 20 kg / 12 cm, `DA_120x800mm_Standard` 11.5 / 15 kg / 12 cm, `DA_125x570mm` 10 / 23 kg / 12.5 cm).
   A consistent authored range for the large cylinders, 4 to 5 times the Expensive 155.
3. **`DA_Arrow_Explosive_ProjectileData` 10** (0.045 kg, 0.85 cm, row `GC (Cylinder)`): the explosive arrow's Value matches the tank-round tier, four times
   the combat arrow's 2.5 (that arrow has no curve row, so its Cd is the bare Value).

Not outliers but worth knowing: `DA_122mm` / `DA_122_mm_HAVOC` (57 kg, 12.2 cm), `DA_70mm`, `DA_72mm`, `DA_84mm`, `DA_TVGuidedMissile`, `DA_Drone` and `DA_20x102mm`, `DA_50AE`, `DA_50Cal`,
`DA_45Colt`, `DA_12g_RifledSlug` omit `Value` and therefore use 1.0. The small-arms rounds sit between 0.5 and 1.4.

## What each implies (Derived)

Terminal speed is the vertical speed at which the drag deceleration equals gravity (9.8 m/s²), using each asset's `GC (Cylinder)` row of `CT_Projectile_DragCoefficients`.
The range column is a **yardstick**: the 155 mm artillery's 300 m/s launch speed, applied to every row so that the Value is the only difference. The 120/125 mm guns and the
others launch at their own weapon speeds, so those range figures are not predictions for those weapons.

| Asset | Value | Mass | Diameter | Terminal speed (m/s) | Drag decel at 300 m/s (m/s^2) | Max flat range at 300 m/s (m) |
|---|---:|---:|---:|---:|---:|---:|
| `DA_155mm_Expensive_ProjectileData_SB` | 80 | 70 | 8.4 | 62.6 | 376.2 | 814 (at 29.9 deg) |
| `DA_155mm_Standard_ProjectileData` | 80 | 70 | 8.4 | 62.6 | 376.2 | 814 (at 29.9 deg) |
| `DA_155mm_Standard_ProjectileData_SB` | 80 | 70 | 8.4 | 62.6 | 376.2 | 814 (at 29.9 deg) |
| `DA_120x800mm_Standard_ProjectileData` | 11.5 | 15 | 12 | 53.2 | 515.0 | 642 (at 28.8 deg) |
| `DA_120x570mm_ProjectileData` | 10 | 20 | 12 | 66.4 | 335.9 | 886 (at 30.4 deg) |
| `DA_125x570mm_ProjectileData` | 10 | 23 | 12.5 | 68.4 | 316.9 | 925 (at 30.6 deg) |
| `DA_155mm_Expensive_ProjectileData` | 2.5 | 19 | 10.5 | 147.5 | 67.7 | 2582 (at 37.0 deg) |
| `DA_93mm_ProjectileData` | 1.4 | 2 | 9.3 | 72.6 | 282.4 | 1006 (at 31.0 deg) |
| `DA_122_mm_HAVOC_ProjectileData` | 1 | 57 | 12.2 | 283.9 | 12.2 | 5692 (at 42.4 deg) |
| `DA_122mm_ProjectileData` | 1 | 57 | 12.2 | 283.9 | 12.2 | 5692 (at 42.4 deg) |
| `DA_70mm_ProjectileData` | 1 | 10.1 | 12 | 148.8 | 66.5 | 2608 (at 37.0 deg) |
| `DA_84mm_ProjectileData` | 1 | 2.3 | 8.4 | 102.7 | 143.1 | 1616 (at 33.8 deg) |
| `DA_TVGuidedMissile_Data` | 1 | 2.3 | 8.4 | 102.7 | 143.1 | 1616 (at 33.8 deg) |
| `DA_DebugHomingRocketData` | 1 | 1 | 4 | 140.7 | 74.6 | 2437 (at 36.5 deg) |
| `DA_Drone_ProjectileData` | 1 | 10 | 10 | 175.5 | 46.7 | 3177 (at 38.3 deg) |

- **Standard 155 mm (80):** terminal speed 62.6 m/s, 376 m/s² of drag at 300 m/s (38 g), and a best flat range of 814 m at 1 ms (804 m at the 33 ms native step) from a 300 m/s launch.
  The round-21 comparison needs the shell to reach more than 2 km; this model cannot do that for any elevation. Either the logged shells were not Standard rounds, or the
  Standard asset's 80 is not applied by the actor-driven path the way the page reads it.
- **Expensive 155 mm (2.5):** terminal speed 147.5 m/s, 67.7 m/s² at 300 m/s, 2582 m best range. This is the shell that matches the logged impacts.
- **`DA_155mm_Expensive_ProjectileData_SB` (80 / 70 kg / 8.4 cm):** it flies exactly like the Standard shell in this model (identical row above), despite its name. Whether the sandbox
  assets are used in the live game is not known from the data; a sandbox copy that fails to follow the Expensive numbers may be a copy-paste of the Standard asset.
- **120/125 mm tank rounds (10 to 11.5):** terminal speeds of 53 to 68 m/s and 317 to 515 m/s² of drag at 300 m/s. Their real launch speeds are far above the yardstick; on the `GC (Cylinder)` row
  the curve climbs from 1.10 at 300 m/s to 1.60 at 600 m/s, so their Cd is 11 to 18 at those speeds. The figures here only rank the Values; they are not range predictions for those guns.
- **Arrow, explosive (10):** Cd is four times the combat arrow's (Value 10 on the `GC (Cylinder)` row against 2.5 with no row). It launches at bow speed, far below the yardstick, so no range is given.

Every row with a Value above 2.5 except the explosive arrow also has `bActorHandlesProjectileMovement: true`, so for them the force model runs inside the projectile actor's mover, not in
the subsystem tick ([Projectile Flight §7](../../pipelines/Wardogs_ProjectileFlight_v1.md)); the step there is the mover's, probably 1/30 s ([§3, Rate](../../pipelines/Wardogs_ProjectileFlight_v1.md)).

## Open

- Whether `BP_155mm_Standard` (or a projectile-data override at spawn) changes drag; the Blueprint export is not part of this survey.
- Whether the `_SB` ("sandbox") assets ship in the live item set.
- Nothing here was observed running; the figures are static readings plus `_tools/shell_sim.py`.
