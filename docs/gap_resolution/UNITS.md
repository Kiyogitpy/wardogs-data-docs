# Gap resolution — UNITS

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Gaps where a data value's **unit is undocumented or inferred**. 13 total across the project.

Resolution strategy: one authoritative units table in `docs/UNITS.md` that maps UE property type + context to its unit, then update each affected doc to cite that table.

## Catalog

### [Wardogs_Demolition_v2.md](Wardogs_Demolition_v2.html)

- **8. Still Not Pulled / Limitations**  →  _**Units are not stated.** Minimum distance, cull distances and fragment physics are used as exported. The cm assumption is an inference._

### [Wardogs_Developers_v2.md](Wardogs_Developers_v2.html)

- **3. Still Not Pulled / Limitations**  →  _**Units are assumed to be Unreal units (cm by default).** The conversion to metres above is an assumption._

### [Wardogs_Environment_v2.md](Wardogs_Environment_v2.html)

- **16. Still not pulled / limitations**  →  _**Unit assumptions.** Distances are assumed to be Unreal cm. Sun `Intensity` is assumed to be lux. Neither is stated in the export._

### [Wardogs_GameFeatures_PvE_v2.md](Wardogs_GameFeatures_PvE_v2.html)

- **8. Still not pulled / limitations**  →  _**Units.** Curve times and values, and the helicopter speed, have no stated units._

### [Wardogs_GameFeatures_UnderbarrelGrenadeLauncher_v2.md](Wardogs_GameFeatures_UnderbarrelGrenadeLauncher_v2.html)

- **8. How Values Combine**  →  _**Ballistics:** a 7,600 initial speed over an effective range of 300. Units are not stated, so the range-to-speed relation cannot be checked from this folder._

### [Wardogs_Items_v2.md](Wardogs_Items_v2.html)

- **13. Still Not Pulled / Limitations**  →  _**Weight unit not stated.** The dump gives values (0.08 to 42.0) without a unit. Assume it is the game's internal weight unit until confirmed._

### [Wardogs_Maps_v2.md](Wardogs_Maps_v2.html)

- **9. Still Not Pulled / Limitations**  →  _**Units and meaning.** Health (1.0), DamageIncrease (3.5), the grid bounds, and the simulation values have no units in the export. The `Iteration` counter and the sample meaning of 65535 in the height grid are not verified._

### [Wardogs_MoverTesting_v2.md](Wardogs_MoverTesting_v2.html)

- **8. Still Not Pulled / Limitations**  →  _**Units.** Speeds, stamina, heights, weights, and curve time axes have no units in the export. Values are reported as stored._

### [Wardogs_Plugin_BHAimAssist_v2.md](Wardogs_Plugin_BHAimAssist_v2.html)

- **7. Still not pulled / limitations**  →  _**Units.** The time axis is named "Time" in the curve, but it is used as distance (key values 150 to 30000). The unit is assumed to be Unreal units (cm). Not confirmed by the export._

### [Wardogs_Significance_v2.md](Wardogs_Significance_v2.html)

- **7. Still Not Pulled / Limitations**  →  _**Units are not stated.** Distances are assumed to be cm and timings seconds. Both are inferences._

### [Wardogs_VFX_v2.md](Wardogs_VFX_v2.html)

- **11. Still Not Pulled / Limitations**  →  _**Unit and meaning uncertainty.** Sizes, lifetimes, and offsets have no units in the export. Multiplier names (for example `Flash Size Multiplyer 1P`) are read literally, and how they stack at runtime is not verified._

### [Wardogs_Weapons_v2.md](Wardogs_Weapons_v2.html)

- **6. Still Not Pulled / Limitations**  →  _**Units are not stated** in the export. Speeds are assumed to be cm/s and ranges to be metres, based on the falloff-curve and EffectiveRange check. That is an inference._
- **6. Still Not Pulled / Limitations**  →  _`CF_*_ADS_Curve` and `ADS_Blur_Curve` have no stated output meaning._
