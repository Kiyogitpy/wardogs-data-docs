---
title: "Characters"
parent: "Content"
---

# Wardogs: Characters Data Reference
*Extracted from cooked game data ([`Wardogs/Content/Characters`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Characters), 3 files). Values are raw asset values.*

> **Scope:** the third-person character LOD policy and the physics bone-constraint assets for the ghillie suit. The skeletal meshes, materials and armour meshes themselves are not in this folder.

---

## 1. File Map

| File | Asset type | What it controls |
|---|---|---|
| Default_PlayerMesh/TP/LOD_TPCharacter.json | SkeletalMeshLODSettings | LOD reduction and streaming for the third-person player mesh |
| Player/Armour/Ghillie/000/ABP_GhilliArmour_000_KawaiiDataTable.json | KawaiiPhysicsBoneConstraintsDataAsset | Secondary-motion (Kawaii) constraints for the ghillie armour |
| Player/Armour/Ghillie/000/ABP_GhilliHead_000_KawaiiDataTable.json | KawaiiPhysicsBoneConstraintsDataAsset | Secondary-motion (Kawaii) constraints for the ghillie head piece |

---

## 2. Third-Person LOD Policy

`bOverrideLODStreamingSettings` is **true** and `bSupportLODStreaming` is **true**. The asset has five LOD groups. Every group uses `BaseLOD = 0` and removes bones through the bone-filter option, with an empty bone list.

| LOD | Screen size (switch at) | Hysteresis | Triangle % | Vertex % | Max verts | Max deviation % | Morph targets remapped | Lock edges | Recalc normals |
|---|---|---|---|---|---|---|---|---|---|
| LOD0 | 1.0 | 0.02 | 1.0 | 1.0 | 9,999,999 | 0.0 | no | yes | True |
| LOD1 | 0.5 | 0.0 | 0.7 | 0.5 | 80,000 | 0.5 | yes | no | True |
| LOD2 | 0.1 | 0.0 | 0.5 | 0.5 | 3,000 | 0.5 | no | no | True |
| LOD3 | 0.05 | 0.0 | 0.4 | 0.5 | 2,001 | 0.5 | no | no | True |
| LOD4 | 0.025 | 0.0 | 0.2 | 0.5 | 1,000 | 0.5 | no | no | True |

**Notes**
- LOD0 keeps 100% of triangles and is the only group that locks edges and has hysteresis (0.02).
- The reduction criterion is `SMTC_NumOfTriangles`, so the triangle percentage drives the reduction. `MaxNumOfTriangles` is 4 in every group and appears unused under this criterion.
- Morph targets are remapped only in LOD1. The others drop them.
- Screen-size thresholds step down 1.0, 0.5, 0.1, 0.05, 0.025. The largest single step is from 0.5 to 0.1.

---

## 3. Ghillie Physics Constraints (Kawaii)

| Asset | Constraints | Bone stems (BoneReference1) | Compliance | Overrides |
|---|---|---|---|---|
| Ghillie armour (000) | 8 | ghille_dyn_back_l, ghille_dyn_back_m | Leather x8 | 0 |
| Ghillie head (000) | 49 | ghille_dyn_head_l, ghille_dyn_head_r | Leather x49 | 0 |

Each constraint links two bones (`BoneReference1` and `BoneReference2`, named like `ghille_dyn_back_l_C1` and `ghille_dyn_back_m_C1`) with a compliance type. The `_C1` to `_C4` suffixes repeat across the back constraints. `BoneName1` is `None` in every constraint, so the bone references carry the link data. All constraints use `EXPBDComplianceType::Leather` and none overrides compliance.

The head set has 49 constraints (27 with a `ghille_dyn_head_l` first bone and 22 with `ghille_dyn_head_r`), which is more than the armour set (8). The name prefix `ghille_dyn` suggests dynamic (secondary-motion) bones for the ghillie suit.

---

## 4. How Values Combine

- LOD: the screen size selects the LOD group. The triangle percentage sets how much of the base mesh remains. Streaming is on, so the lower LODs can be streamed separately (the streaming budget is not in this asset).
- Kawaii: each constraint keeps two bones at a rest distance, with the given compliance (generic behaviour of a distance constraint). A softer compliance (Leather) gives more give; an override would replace it per constraint. The per-frame behaviour is in the animation blueprint, which is not in this dump.

---

## 5. Still Not Pulled / Limitations

- **Only the third-person LOD and one armour set are in this folder.** The first-person mesh, the other armour variants and the skeletal meshes are not here.
- **Streaming budget and bone list** are not in the LOD asset (`BoneList` is empty everywhere), so the effect of the bone filter cannot be shown.
- **Kawaii runtime settings.** The constraint stiffness and damping are not in these assets. Only the bone pairs and compliance type are recorded.
- **Armour variant 000 only.** Only the `000` ghillie variant is present.

