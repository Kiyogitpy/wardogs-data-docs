# Gap resolution — SDK

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Gaps where **the SDK resolves a hashed field name, unnamed property, or enum value**. 26 total across the project.

The SDK is now in [`../sdk/`](../sdk/) (3655 files, 1807 packages).

Resolution workflow per gap:

1. Identify the DataAsset / Blueprint class the data doc covers
2. Open `sdk/raw/<Package>_classes.hpp` for that class
3. Find the property matching the hashed/unnamed field in the data doc
4. Replace the opaque reference with the SDK's symbolic name
5. Add backlink from the SDK file to the data doc (optional)

## Catalog

### [Wardogs_Audio_v2.md](Wardogs_Audio_v2.html)

- **Still not pulled / limitations**  →  _**Behaviour logic.** The `AEB_*` and `WDAudioEventBehavior*` classes are Blueprint or C++ classes. Their code is not exported, so execution order, blending and what each behaviour does internally are inferred from property names._
- **Still not pulled / limitations**  →  _**Hashed property names.** The float on events (222 instances including behaviours), the bool and enum on DT_VoxData rows, and a list-valued hash on `WDAudioEventBehaviorApplyImpulseResonance` are unnamed. Their meaning is not confirmed. The reload-stage value 50.5 and comms value 80.0 are the most _

### [Wardogs_Environment_v2.md](Wardogs_Environment_v2.html)

- **16. Still not pulled / limitations**  →  _**Height grid arrays** (`WDWaterHeightGridAsset`) are binary data keyed by unnamed field names. Only metadata is reported here (world size, grid width, origin, linked state). Height values are not decoded._
- **16. Still not pulled / limitations**  →  _**Enum names** in `DT_VehiclePropList` are cooked as `NewEnumeratorN`. Only the index is shown._

### [Wardogs_ExternalAssets_v2.md](Wardogs_ExternalAssets_v2.html)

- **8. Still not pulled / Limitations**  →  _**Unresolved property names.** Some properties appear only as GUID-style keys. On every `RequiredMeshes` entry the value is `EBHDestructionCPDInputStyle::Building`. Cosmetic decorator entries carry an unnamed list. Their meaning is not known from this export._
- **8. Still not pulled / Limitations**  →  _**Connection semantics inferred.** "Vital" and "proportional" support links are read from property names. Runtime behaviour is not confirmed._
- **8. Still not pulled / Limitations**  →  _**Decorator-to-building link is by name.** Only the `OwningChunkIDs` GUIDs give a hard link, and they were spot-checked, not checked for every decorator._

### [Wardogs_GameFeatures_AI_v2.md](Wardogs_GameFeatures_AI_v2.html)

- **11. Still not pulled / limitations**  →  _**Unnamed localisation keys.** Some properties appear as `_aaa…` hashes; those were not resolved._

### [Wardogs_GameFeatures_Experiences_v2.md](Wardogs_GameFeatures_Experiences_v2.html)

- **5. Still not pulled / limitations**  →  _**Unnamed keys.** Localised strings use `_aaa…` keys; their values are shown where the source string is present._

### [Wardogs_GameFeatures_Skins_v2.md](Wardogs_GameFeatures_Skins_v2.html)

- **6. Still Not Pulled / Limitations**  →  _**`CPD` field meanings.** The UV, wear and mastery field names are as exported. Their effect on rendering is not confirmed._

### [Wardogs_GameFeatures_Vehicles_v2.md](Wardogs_GameFeatures_Vehicles_v2.html)

- **15. Still not pulled / Limitations**  →  _**Unnamed fields.** Some fields have no readable name. Their meanings are unknown and were skipped (for example, several flags on health triggers and vendor variations)._

### [Wardogs_GameFeatures_Weapons_v2.md](Wardogs_GameFeatures_Weapons_v2.html)

- **10. Still not pulled / limitations**  →  _**Units and meanings** of accuracy, deviation, focus energy, recoil relief, `TypicalSpeed`, `AimTime` and the zeroing values are inferred from property names._

### [Wardogs_GameFeatures_WorldFeatures_v2.md](Wardogs_GameFeatures_WorldFeatures_v2.html)

- **6. Still not pulled / limitations**  →  _**Localisation keys.** Some `_aaa…` localisation keys are present; their text is not resolved here._

### [Wardogs_GameMechanics_v2.md](Wardogs_GameMechanics_v2.html)

- **15. Still Not Pulled / Limitations**  →  _**Unnamed fields.** Many struct fields have no readable name and are called unnamed fields here. These are the arm-class arrays in 2d, the seat-reduction arrays in 2h, the `Emote` flags in 12c, and some action fields. Their meaning was inferred from neighbouring values and is not confirmed._

### [Wardogs_InfantryWeapons_Stats_v1.md](Wardogs_InfantryWeapons_Stats_v1.html)

- **5. Still not pulled / limitations**  →  _**Unnamed fields.** Some properties are listed without a readable name, such as `_aaabimbpohdlmnphjbidm` (mostly `1.0`). Their meaning is not stated in the data._

### [Wardogs_Items_v2.md](Wardogs_Items_v2.html)

- **13. Still Not Pulled / Limitations**  →  _**Unnamed property keys omitted.** Keys of the form `_aaa…` (21 letters a–p; `_aaa..._$HEX$_$N$` before 2026-10-18) (several per aim-assist asset and a few on containers) are internal and were skipped. Their meaning is unknown._

### [Wardogs_Maps_v2.md](Wardogs_Maps_v2.html)

- **9. Still Not Pulled / Limitations**  →  _**Unnamed fields.** Several properties in the height grid, the warmup manifests, and the sight blocker assets are unnamed fields. Their values were read and reported, but their names are not known. Those values are cited by position and value only._

### [Wardogs_Meta_v2.md](Wardogs_Meta_v2.html)

- **12. Still Not Pulled / Limitations**  →  _**Skill curve time axis is unlabeled.** The mapping from skill rank to curve `Time` is inferred._
- **12. Still Not Pulled / Limitations**  →  _**Unnamed fields.** Some fields in the challenge tables are unnamed ("unnamed field"). Their meaning is inferred from values only._

### [Wardogs_MoverTesting_v2.md](Wardogs_MoverTesting_v2.html)

- **8. Still Not Pulled / Limitations**  →  _**Unnamed keys.** Some properties use hashed keys (for example the ragdoll bone lists, the body-drag trace channel, and the ragdoll value 200). Their values are reported by position and value, and their property names are not known._

### [Wardogs_Plugin_BHFramework_v2.md](Wardogs_Plugin_BHFramework_v2.html)

- **8. Still not pulled / limitations**  →  _**Enum labels.** Discrete settings store raw values (for example `0`, `1`, `251`). The labels (what each value means) come from the `BHUserSettingEnumDiscreteValues` sub-exports keyed by localised strings. The labels were not resolved in this pass, so the raw values above are shown as-is._

### [Wardogs_Tools_v2.md](Wardogs_Tools_v2.html)

- **3. Still Not Pulled / Limitations**  →  _**The enum `EToolFonts` is not in this dump.** The enum entries are shown as exported (`NewEnumerator0`, `1`, `2`, `3`, `5`). Entry `4` is absent from the table, and its meaning cannot be checked._

### [Wardogs_TreeRewardTrack_PlatformMastery_v1.md](Wardogs_TreeRewardTrack_PlatformMastery_v1.html)

- **6. Still not pulled / limitations**  →  _**Hashed keys:** several keys (for example `10B5F07C…`) are not localization keys: none of the 121 `STRINGS_*` tables pulled contain them. They look like Blueprint property names. Their meaning is not resolved in this doc._

### [Wardogs_VFX_v2.md](Wardogs_VFX_v2.html)

- **11. Still Not Pulled / Limitations**  →  _**Unnamed enum.** `SmokeType = NewEnumerator1` on six smoke grenades does not say which behavior it selects._
- **11. Still Not Pulled / Limitations**  →  _**Unnamed property names.** Some keys in the timing sequences are suffixed with hash tokens (for example `ExplosionData_9_FB01A97E496F...`). They were trimmed to their readable part. The mapping is one-to-one, so the meaning is unchanged, but the raw keys are not reproduced here._

### [Wardogs_Weapons_v2.md](Wardogs_Weapons_v2.html)

- **6. Still Not Pulled / Limitations**  →  _Two unnamed fields on the SKS and Judge have no known meaning. Values: SKS 1.0 and 2.5, Judge 2.0._

## Change log

| Date | Change |
|---|---|
| 2026-10-18 | `data/` re-exported with the v2 usmap (names only; values unchanged): the cited hashed keys and key forms are updated. |
