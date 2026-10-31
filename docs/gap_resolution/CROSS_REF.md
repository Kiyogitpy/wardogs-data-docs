# Gap resolution — CROSS_REF

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Gaps that reference an asset / class / file **in another folder** without a link. 20 total across the project.

Resolution strategy: for each referenced name, find the file in `data/` or `sdk/` that defines it, add a proper markdown link.

## Catalog with mention-scan

### [Wardogs_Animation_v2.md](Wardogs_Animation_v2.html)

- **7. Still Not Pulled / Limitations**  →  _**Mirror table is not wired.** The `MirrorDataTable` field on every schema is `null`, so this table is not referenced by any motion-matching schema in this dump. It may be used by a different system (for example a control rig or first-person layer)._
  - Referenced: `MirrorDataTable`

### [Wardogs_Destruction_v2.md](Wardogs_Destruction_v2.html)

- **6. Still Not Pulled / Limitations**  →  _**Prefab classes are referenced by name only.** The `CP_*_C` blueprint classes are not exported here, so their contents (debris, collision, damage thresholds) are unknown._
  - Referenced: `CP_*_C`

### [Wardogs_GameFeatures_AlternativeCriticalCamera_v2.md](Wardogs_GameFeatures_AlternativeCriticalCamera_v2.html)

- **6. Still not pulled / limitations**  →  _**Post-process effect.** The [`DT_AlternativeCriticalCamera`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/DT_AlternativeCriticalCamera.json) registry has no rows in this export; the `PostProcessEffect.DeathState.Killcam_
  - Referenced: `DT_AlternativeCriticalCamera`, `PostProcessEffect.DeathState.Killcam`

### [Wardogs_GameFeatures_ControlZone_v2.md](Wardogs_GameFeatures_ControlZone_v2.html)

- **9. Limitations**  →  _**Alternator weight 0 entries** (Europe Farmland, NorthAmerica SmallFactory, Africa North/East/West, Russia Bazaar/River/Hillside) are read as never selected. The game may use them elsewhere; this was not checked._

### [Wardogs_GameFeatures_FactoryInvestment_01_v2.md](Wardogs_GameFeatures_FactoryInvestment_01_v2.html)

- **7. Still not pulled / limitations**  →  _**Icons and strings.** The display name and the map icon are localised or texture references; not resolved here._

### [Wardogs_GameFeatures_FlyByManager_v2.md](Wardogs_GameFeatures_FlyByManager_v2.html)

- **5. Still Not Pulled / Limitations**  →  _**Stop-sound targets** are inferred from the context tag, not from an explicit sound reference, since the stop behaviour has no sound field._

### [Wardogs_GameFeatures_Gunsmith_v2.md](Wardogs_GameFeatures_Gunsmith_v2.html)

- **12. Still Not Pulled / Limitations**  →  _**Texture and widget assets** (`T_Reticle_*`, `W_*`, `DL_Gunsmith_*`, `B_Gunsmith*`) are referenced by name or path only._
  - Referenced: `T_Reticle_*`, `W_*`, `DL_Gunsmith_*`, `B_Gunsmith*`
- **12. Still Not Pulled / Limitations**  →  _**Scope and sight item ids** (for example `Id.Item.OPT_08`) are referenced in the exclusivity and texture rows, but the item definitions are outside this plugin._
  - Referenced: `Id.Item.OPT_08`
- **12. Still Not Pulled / Limitations**  →  _**Popup options** (`DT_GunsmithPopupOptions`) hold five popup rows (see the Season 02 update). Popup text is referenced by key, and only some `So_
  - Referenced: [`DT_GunsmithPopupOptions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Data/Popups/DT_GunsmithPopupOptions.json), `SourceString`

### [Wardogs_GameFeatures_Parachutes_v2.md](Wardogs_GameFeatures_Parachutes_v2.html)

- **8. Still Not Pulled / Limitations**  →  _**[`CRV_ParachutePunishment_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_ParachutePunishment_Damage.json) curve values** are not in this plugin. Only the reference is here._
  - Referenced: [`CRV_ParachutePunishment_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_ParachutePunishment_Damage.json)
- **8. Still Not Pulled / Limitations**  →  _**Audio assets.** [`ID_Backpack_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Backpack_Audio.json), [`ID_Vest_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Vest_Audio.json)_
  - Referenced: [`ID_Backpack_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Backpack_Audio.json), [`ID_Vest_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Vest_Audio.json)

### [Wardogs_GameFeatures_UnderbarrelGrenadeLauncher_v2.md](Wardogs_GameFeatures_UnderbarrelGrenadeLauncher_v2.html)

- **9. Still Not Pulled / Limitations**  →  _**[`CT_Weapon_Spread`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Curves/CT_Weapon_Spread.json) values** are referenced by name only. The curve table is outside this plugin._
  - Referenced: [`CT_Weapon_Spread`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Curves/CT_Weapon_Spread.json)
- **9. Still Not Pulled / Limitations**  →  _**Test naming:** whether `TestGrenadeLauncher` is shipped or only a test build cannot be confirmed from the dump. The name and magazine-audio reference are the evidence._
  - Referenced: `TestGrenadeLauncher`

### [Wardogs_GameFeatures_Vehicles_v2.md](Wardogs_GameFeatures_Vehicles_v2.html)

- **15. Still not pulled / Limitations**  →  _**Units.** Speed, fuel, FuelEconomy, muzzle speed, drag area and mass are not labelled in the export. Treat them as relative values until a reference confirms them. Only fields with a unit suffix (`_mps`, `_kmh`, `_deg`, `_m`) have a known unit._
  - Referenced: `_mps`, `_kmh`, `_deg`
- **15. Still not pulled / Limitations**  →  _**Ural asset mapping.** `Ural.Battle` points at [`DA_WHL_07_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07/Content/Data/DA_WHL_07_Stats.json) rather than the ArmouredBattle asset (section 3). Numbers are identical, so this is only a_
  - Referenced: `Ural.Battle`, [`DA_WHL_07_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07/Content/Data/DA_WHL_07_Stats.json)

### [Wardogs_GameFeatures_Vehiclesmith_v2.md](Wardogs_GameFeatures_Vehiclesmith_v2.html)

- **10. Still Not Pulled / Limitations**  →  _**Vehicle stats and part lists** are not here. They are defined in the vehicle category (see the Vehicles reference)._
- **10. Still Not Pulled / Limitations**  →  _**Data layer and map assets** (`DL_Vehiclesmith_*`, `Vehiclesmith_Main_P`) are referenced by path only._
  - Referenced: `DL_Vehiclesmith_*`, `Vehiclesmith_Main_P`

### [Wardogs_Items_v2.md](Wardogs_Items_v2.html)

- **13. Still Not Pulled / Limitations**  →  _**Full throw and consumable action data.** The `AppliableActionData` and `ThrowActions` arrays are present but only partly decoded (required states, velocity curve references)._
  - Referenced: `AppliableActionData`, `ThrowActions`

### [Wardogs_Maps_v2.md](Wardogs_Maps_v2.html)

- **9. Still Not Pulled / Limitations**  →  _**Vertex factory and material paths.** The manifests reference materials and vertex factories by path and class name. The materials themselves are in other categories._

### [Wardogs_VFX_v2.md](Wardogs_VFX_v2.html)

- **11. Still Not Pulled / Limitations**  →  _**Object references only.** Recipe rows reference `B_CameraShake_*` blueprints and `NS_*` Niagara systems by path or class name. Only those references were pulled. The shake behavior and the Niagara internals are not in [`Content/VFX`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX)_
  - Referenced: `B_CameraShake_*`, `NS_*`, [`Content/VFX`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX)
