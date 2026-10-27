---
title: "Animation"
redirect_from: ["/Wardogs_Animation_v2.html", "/Wardogs_Animation_v2"]
parent: "Player & Movement"
description: "Folder Map, Motion Matching, First-Person Mirroring, Animation Curves"
---

# Wardogs: Animation Data Reference
*Extracted from cooked game data (`Wardogs/Content/Animation`, 10 files). Motion-matching and mirroring tables are read directly; curve semantics are inferred from asset names unless stated.*

> **Scope:** the animation support data: motion-matching schemas and databases, the first-person mirroring table, animation curves and the curve-compression setting. The actual animation sequences and `PSD_*` pose-search databases are not in this folder (see section 7).

---

## 1. Folder Map

| File | Asset type | Exports in file |
|---|---|---|
| Blueprints/ACLAnimCurveCompressionUniformSettings.json | AnimCurveCompressionSettings | 2 |
| Blueprints/Character/Curves/CF_ADS_AnimSpringStrength.json | CurveFloat | 1 |
| Blueprints/Character/Curves/CRV_PitchOffsetBlend.json | CurveFloat | 1 |
| Blueprints/Character/Curves/CR_ADS_CR_Alpha.json | CurveFloat | 1 |
| Blueprints/Character/Layers/DT_FP_Mirroring.json | MirrorDataTable | 1 |
| Characters/MotionMatching/PSN_TPCharacter.json | PoseSearchNormalizationSet | 1 |
| Characters/MotionMatching/PSN_TPCharacter_Walk.json | PoseSearchNormalizationSet | 1 |
| Characters/MotionMatching/PSS_TPCharacter.json | PoseSearchSchema | 7 |
| Characters/MotionMatching/PSS_TPCharacter_Traversal.json | PoseSearchSchema | 10 |
| Characters/MotionMatching/PSS_TPCharacter_Turns.json | PoseSearchSchema | 7 |

Four files hold more than one export (a settings asset plus its codec, or a schema plus its channel objects). Each export is parsed separately.

---

## 2. Motion Matching (`Characters/MotionMatching/`)

Motion matching picks poses by searching a database of recorded poses against a feature vector (trajectory, velocity, heading, foot positions). Three schemas define the feature channels; two normalization sets group the databases that share them.

### 2a. Schemas

| Schema | Skeleton | Mirror table | Top-level channels |
|---|---|---|---|
| PSS_TPCharacter | SKEL_TP_Character_Refactor | none | PoseSearchFeatureChannel_Trajectory, PoseSearchFeatureChannel_Group |
| PSS_TPCharacter_Traversal | SKEL_TP_Character_Refactor | none | PoseSearchFeatureChannel_Trajectory, PoseSearchFeatureChannel_Group, PoseSearchFeatureChannel_Group |
| PSS_TPCharacter_Turns | SKEL_TP_Character_Refactor | none | PoseSearchFeatureChannel_Trajectory, PoseSearchFeatureChannel_Group |

Every schema points at the skeleton `SKEL_TP_Character_Refactor`, and none of them wires a mirror table. See section 3 for the mirror table's own skeleton.

### 2b. Feature channels

| Schema | Channel | Bone(s) | Settings |
|---|---|---|---|
| PSS_TPCharacter | Trajectory | (root) | 5 samples at offsets -0.05, 0.0, 0.35, 0.7, 1.0 (flags 32 to 176) |
| PSS_TPCharacter | Group: Position + 2 Velocity | foot_l, foot_r | Position origin = foot_r; velocities on foot_l and foot_r |
| PSS_TPCharacter_Turns | Trajectory | (root) | 5 samples at offsets -0.05 to 1.0 (same layout as the base schema) |
| PSS_TPCharacter_Turns | Heading | pelvis | Axis Y, strip Z, origin time offset 0.2 s |
| PSS_TPCharacter_Turns | Group: Position + 2 Velocity | foot_l, foot_r | Same as base schema |
| PSS_TPCharacter_Traversal | Trajectory | (root) | 3 samples at offsets -0.4, 0.0, 0.5 |
| PSS_TPCharacter_Traversal | Ledge heading (BHMover custom) | attach | Custom channel class `BHMoverPoseSearchChannel_LedgeHeading` |
| PSS_TPCharacter_Traversal | Ledge position (BHMover custom) | attach | Custom channel class `BHMoverPoseSearchChannel_LedgePosition` |
| PSS_TPCharacter_Traversal | Group: Position + 3 Velocity | foot_l, foot_r | Position origin foot_r; velocity channels on foot_l (origin foot_r), foot_l, and foot_r |

Sample `Flags` values are the trajectory sample flags exported as bitmasks. Their meaning is not labeled in the export.

### 2c. Normalization sets (database groups)

| Normalization set | Databases | Database assets (names) |
|---|---|---|
| PSN_TPCharacter | 6 | PSD_Rifle_Running_Loop, PSD_Rifle_Running_Start, PSD_Rifle_Running_Stop, PSD_Rifle_Vault_Run_Over, PSD_Rifle_Mantle_Run_On, PSD_Rifle_Standing_Turns |
| PSN_TPCharacter_Walk | 4 | PSD_Rifle_Vault_Walk_Over, PSD_Rifle_Walking_Loop, PSD_Rifle_Walking_Start, PSD_Rifle_Walking_Stop |

The base set `PSN_TPCharacter` covers running (loop, start, stop), the run-over vault, the run-on mantle and standing turns. `PSN_TPCharacter_Walk` covers the walk loop, start and stop, and the walk-over vault. All database names are Rifle variants (`PSD_Rifle_*`).

---

## 3. First-Person Mirroring (`Blueprints/Character/Layers/DT_FP_Mirroring.json`)

`MirrorDataTable` used to mirror poses (left and right). It has two parts: 21 find-and-replace expressions and 175 row entries.

**Expressions**

| Find | Replace | Method |
|---|---|---|
| r_ | l_ | Prefix |
| l_ | r_ | Prefix |
| R_ | L_ | Prefix |
| L_ | R_ | Prefix |
| _l | _r | Suffix |
| _r | _l | Suffix |
| _R | _L | Suffix |
| _L | _R | Suffix |
| right | left | Prefix |
| left | right | Prefix |
| Right | Left | Prefix |
| Left | Right | Prefix |

The table also holds 9 regular-expression rules (for example `([^}]*)_l_([^}]*)` to `$1_r_$2`). The last rule keeps the spine, root, pelvis, neck, head and `ik_hand_gun` names unchanged, so they are not mirrored.

**Rows**

- 175 rows: 157 bones and 18 curves (`MirrorEntryType`).
- 154 rows map to a different name (for example `clavicle_l` to `clavicle_r`, `ik_foot_l` to `ik_foot_r`). 21 rows map to themselves (centre bones and `ik_hand_gun`).
- Skeleton reference: `SKEL_TPCharacter`. The motion-matching schemas use `SKEL_TP_Character_Refactor`. The two skeleton names differ.

---

## 4. Animation Curves (`Blueprints/Character/Curves/`)

| Curve | Key points (input, output) |
|---|---|
| CF_ADS_AnimSpringStrength | (0, 3.75), (1, 6) |
| CRV_PitchOffsetBlend | (0, 0), (0.7, 0.475), (1, 1) |
| CR_ADS_CR_Alpha | (0, 0), (0.4149, 0.2395), (0.6821, 0.842), (1, 1) |

- `CF_ADS_AnimSpringStrength`: rises from 3.75 to 6.0 over input 0 to 1. The name suggests it sets spring strength during ADS (aim down sights). The input is not named in the export.
- `CRV_PitchOffsetBlend`: a non-linear blend on pitch offset (0 at 0, 0.475 at 0.7, 1 at 1). The name suggests it blends a pitch offset in as the input rises.
- `CR_ADS_CR_Alpha`: an alpha ramp for ADS (0 to 1, with keys at 0.415 and 0.682 that bend the ramp). The `CR_` prefix plus `ADS` suggests a control-rig layer alpha.

---

## 5. Curve Compression (`Blueprints/ACLAnimCurveCompressionUniformSettings.json`)

Two exports: an `AnimCurveCompressionSettings` asset that points at an `AnimCurveCompressionCodec_UniformIndexable` codec. The codec has no exposed properties in this export, so only the codec choice is recorded: uniform indexable ACL curve compression.

---

## 6. How Values Combine

- Motion matching: the schema channels form a feature vector per pose. The normalization set weights the features across its databases. The search then returns the closest pose and the pose player blends into it.
- Mirroring: the mirror table is applied when a left-side pose is needed from right-side data (or the reverse). The find-and-replace rules name the mirrored bones, and the row entries say what each bone maps to.
- ADS curves: `CF_ADS_AnimSpringStrength` and `CR_ADS_CR_Alpha` both depend on an ADS input that is not in this folder.

---

## 7. Still Not Pulled / Limitations

- **No animation sequences and no `PSD_*` databases.** The normalization sets reference databases (for example `PSD_Rifle_Running_Loop`) that live outside this folder. The pose data itself cannot be read from this dump.
- **Mirror table is not wired.** The `MirrorDataTable` field on every schema is `null`, so this table is not referenced by any motion-matching schema in this dump. It may be used by a different system (for example a control rig or first-person layer).
  - **See [`docs/CROSS_REFERENCE.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/CROSS_REFERENCE.md)** for the project-wide cross-reference index of where referenced assets are defined.
- **Skeleton mismatch.** The mirror table targets `SKEL_TPCharacter` and the schemas target `SKEL_TP_Character_Refactor`. Whether the names are an intentional rename is not in the export.
- **Curve inputs unnamed.** The curves in section 4 have no input names. Their meanings are inferred from asset names.
- **Channel flags.** Trajectory sample `Flags` values are exported as numbers and have no labels.

## 8. Item, grenade and weapon animation sets (round 73)

*Added in round 73 for the `BHAnimationSet` assets no other page named. Each is a `UPrimaryDataAsset` with one `Animations` array: gameplay tag (`Animation.Asset.` prefix dropped below) to a first-person and a third-person montage. The "Entries" column counts that array. Several are leftovers or tests: `AnimSet_ArtilleryBarrelTest`, `AnimSet_LeapordBarrel` (spelling as exported) and `AnimSet_Resuscitator` (under `Enox/.../ResuscitatorTest`) sit in test folders, and `AnimSet_GoldM67Grenade` carries only 4 of the standard grenade's 8 slots.*

| Asset | Owner | Entries | Slots |
|---|---|---:|---|
| `AnimSet_ATMine` | Items/AT_mine | 4 | `Appliable.PrimaryUse`, `Holdable.Inspect`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction` |
| `AnimSet_BinocularsStandard` | Items/Binoculars | 3 | `Holdable.Inspect`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction` |
| `AnimSet_C4Trigger` | Items/C4 | 6 | `Throwable.Overarm`, `Holdable.Trigger`, `Holdable.Inspect`, `Inventory.Weapon.Base`, `Throwable.Underarm`, `Holdable.DoorInteraction` |
| `AnimSet_Claymore` | Items/Claymore | 4 | `Appliable.PrimaryUse`, `Holdable.Inspect`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction` |
| `AnimSet_Crowbar` | Items/Crowbar | 5 | `Weapon.MeleeBash`, `BuildTool.ForceOpenDoor.Right`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction`, `BuildTool.ForceOpenDoor.Left` |
| `AnimSet_DefibrillatorStandard` | Items/Defibrillator | 8 | `Holdable.Inspect`, `Appliable.PrimaryUse`, `Weapon.Reload.Empty`, `Weapon.Reload.Tactical`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction`, `Holdable.Inspect.Empty`, `Holdable.Inspect.Fallback` |
| `AnimSet_EnoxStandard` | Items/Enox | 4 | `Appliable.SecondaryUse`, `Holdable.Inspect`, `Appliable.SecondaryUse.Release`, `Inventory.Weapon.Base` |
| `AnimSet_Resuscitator` | Items/Enox | 5 | `Appliable.PrimaryUse`, `Holdable.Inspect`, `Appliable.PrimaryUse.Release`, `Holdable.DoorInteraction`, `Inventory.Weapon.Base` |
| `AnimSet_FuelCan` | Items/FuelCanister | 5 | `Holdable.Inspect`, `Appliable.PrimaryUse`, `Appliable.SecondaryUse`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction` |
| `AnimSet_IED` | Items/IED | 5 | `Appliable.PrimaryUse`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction`, `Holdable.Trigger`, `Weapon.Reload.Discarding` |
| `AnimSet_MedKitStandard` | Items/MedKit | 4 | `Inventory.Weapon.Base`, `Appliable.PrimaryUse`, `Appliable.SecondaryUse`, `Holdable.DoorInteraction` |
| `AnimSet_RangeFinderExpensive` | Items/RangeFinder | 5 | `Holdable.Inspect`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction`, `Weapon.Reload.Empty`, `Weapon.Reload.Tactical` |
| `AnimSet_RangeFinderStandard` | Items/RangeFinder | 3 | `Holdable.Inspect`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction` |
| `AnimSet_SmokeGrenade` | Items/SmokeGrenade | 7 | `Holdable.Equip`, `Holdable.Holster`, `Throwable.Overarm`, `Throwable.Underarm`, `Holdable.Inspect`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction` |
| `AnimSet_StimPen` | Items/StimPen | 5 | `Appliable.SecondaryUse`, `Holdable.Inspect`, `Inventory.Weapon.Base`, `Appliable.PrimaryUse`, `Holdable.DoorInteraction` |
| `AnimSet_GoldM67Grenade` | Items/Throwable/Grenades | 4 | `Holdable.Equip`, `Holdable.Holster`, `Throwable.Overarm`, `Throwable.Underarm` |
| `AnimSet_M67Grenade` | Items/Throwable/Grenades | 8 | `Holdable.Equip`, `Holdable.Holster`, `Throwable.Overarm`, `Throwable.Underarm`, `Throwable.ThrowBack`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction`, `Holdable.Inspect` |
| `AnimSet_ArtilleryBarrelTest` | Items/Weapons/Launcher | 4 | `Weapon.Reload.Empty`, `Weapon.MeleeBash`, `Weapon.Fire`, `Holdable.Inspect` |
| `AnimSet_LeapordBarrel` | Items/Weapons/Launcher | 4 | `Weapon.Reload.Empty`, `Weapon.MeleeBash`, `Weapon.Fire`, `Holdable.Inspect` |
| `AnimSet_RFB` | Weapons/DMR | 52 | `Weapon.Reload.Empty`, `Weapon.Reload.Tactical`, `Weapon.MeleeBash`, `Weapon.Fire`, `Weapon.Chamber`, `Holdable.Inspect`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction`, `Attachment.Bipod.Unfold`, `Attachment.Bipod.Fold`, `Weapon.Pose.Foregrip`, `Weapon.Pose.Foregrip.FGP_02`, and 40 more |
| `AnimSet_LMG_02` | Weapons/LMG | 15 | `Weapon.Reload.Empty`, `Weapon.Reload.Tactical`, `Weapon.MeleeBash`, `Weapon.Fire`, `Weapon.Chamber`, `Holdable.Inspect`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction`, `Attachment.Bipod.Unfold`, `Attachment.Bipod.Fold`, `Weapon.Reload.Discarding.Empty`, `Weapon.Reload.Discarding.Tactical`, and 3 more |
| `AnimSet_MP43` | Weapons/Shotgun | 11 | `Weapon.Reload.Empty`, `Weapon.MeleeBash`, `Weapon.Fire`, `Weapon.Chamber`, `Holdable.Inspect`, `Weapon.Reload.Tactical`, `Inventory.Weapon.Base`, `Holdable.DoorInteraction`, `Holdable.Inspect.Empty`, `Holdable.Inspect.Fallback`, `Character.PickUp` |

### 8b. Engine default curve-compression settings

Two engine assets only name a codec and carry no tuning values: `DefaultAnimCurveCompressionSettings` (codec `AnimCurveCompressionCodec_CompressedRichCurve`, the stock engine default) and `ACLAnimCurveCompressionSettings` (codec `AnimCurveCompressionCodec_ACL`, from the ACL plugin). They are plain engine defaults; the game's own settings are the uniform ACL asset in section 5.
