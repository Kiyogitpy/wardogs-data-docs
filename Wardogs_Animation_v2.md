---
title: "Animation"
parent: "Content"
---

# Wardogs: Animation Data Reference
*Extracted from cooked game data ([`Wardogs/Content/Animation`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Animation), 10 files). Motion-matching and mirroring tables are read directly; curve semantics are inferred from asset names unless stated.*

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

## 2. Motion Matching ([`Characters/MotionMatching/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Animation/Characters/MotionMatching))

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

The base set [`PSN_TPCharacter`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Animation/Characters/MotionMatching/PSN_TPCharacter.json) covers running (loop, start, stop), the run-over vault, the run-on mantle and standing turns. [`PSN_TPCharacter_Walk`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Animation/Characters/MotionMatching/PSN_TPCharacter_Walk.json) covers the walk loop, start and stop, and the walk-over vault. All database names are Rifle variants (`PSD_Rifle_*`).

---

## 3. First-Person Mirroring ([`Blueprints/Character/Layers/DT_FP_Mirroring.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Animation/Blueprints/Character/Layers/DT_FP_Mirroring.json))

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

## 4. Animation Curves ([`Blueprints/Character/Curves/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Animation/Blueprints/Character/Curves))

| Curve | Key points (input, output) |
|---|---|
| CF_ADS_AnimSpringStrength | (0, 3.75), (1, 6) |
| CRV_PitchOffsetBlend | (0, 0), (0.7, 0.475), (1, 1) |
| CR_ADS_CR_Alpha | (0, 0), (0.4149, 0.2395), (0.6821, 0.842), (1, 1) |

- [`CF_ADS_AnimSpringStrength`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Animation/Blueprints/Character/Curves/CF_ADS_AnimSpringStrength.json): rises from 3.75 to 6.0 over input 0 to 1. The name suggests it sets spring strength during ADS (aim down sights). The input is not named in the export.
- [`CRV_PitchOffsetBlend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Animation/Blueprints/Character/Curves/CRV_PitchOffsetBlend.json): a non-linear blend on pitch offset (0 at 0, 0.475 at 0.7, 1 at 1). The name suggests it blends a pitch offset in as the input rises.
- [`CR_ADS_CR_Alpha`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Animation/Blueprints/Character/Curves/CR_ADS_CR_Alpha.json): an alpha ramp for ADS (0 to 1, with keys at 0.415 and 0.682 that bend the ramp). The `CR_` prefix plus `ADS` suggests a control-rig layer alpha.

---

## 5. Curve Compression ([`Blueprints/ACLAnimCurveCompressionUniformSettings.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Animation/Blueprints/ACLAnimCurveCompressionUniformSettings.json))

Two exports: an `AnimCurveCompressionSettings` asset that points at an `AnimCurveCompressionCodec_UniformIndexable` codec. The codec has no exposed properties in this export, so only the codec choice is recorded: uniform indexable ACL curve compression.

---

## 6. How Values Combine

- Motion matching: the schema channels form a feature vector per pose. The normalization set weights the features across its databases. The search then returns the closest pose and the pose player blends into it.
- Mirroring: the mirror table is applied when a left-side pose is needed from right-side data (or the reverse). The find-and-replace rules name the mirrored bones, and the row entries say what each bone maps to.
- ADS curves: [`CF_ADS_AnimSpringStrength`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Animation/Blueprints/Character/Curves/CF_ADS_AnimSpringStrength.json) and [`CR_ADS_CR_Alpha`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Animation/Blueprints/Character/Curves/CR_ADS_CR_Alpha.json) both depend on an ADS input that is not in this folder.

---

## 7. Still Not Pulled / Limitations

- **No animation sequences and no `PSD_*` databases.** The normalization sets reference databases (for example `PSD_Rifle_Running_Loop`) that live outside this folder. The pose data itself cannot be read from this dump.
- **Mirror table is not wired.** The `MirrorDataTable` field on every schema is `null`, so this table is not referenced by any motion-matching schema in this dump. It may be used by a different system (for example a control rig or first-person layer).
  - **See [`docs/CROSS_REFERENCE.md`](docs/CROSS_REFERENCE.md)** for the project-wide cross-reference index of where referenced assets are defined.
- **Skeleton mismatch.** The mirror table targets `SKEL_TPCharacter` and the schemas target `SKEL_TP_Character_Refactor`. Whether the names are an intentional rename is not in the export.
- **Curve inputs unnamed.** The curves in section 4 have no input names. Their meanings are inferred from asset names.
- **Channel flags.** Trajectory sample `Flags` values are exported as numbers and have no labels.

