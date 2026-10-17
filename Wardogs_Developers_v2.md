---
title: "Developers"
parent: "Content"
---

# Wardogs: Developers Data Reference
*Extracted from cooked game data ([`Wardogs/Content/Developers`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Developers), 1 file). This is a single developer-owned settings asset.*

> **Scope:** one asset. It is a personal developer folder with no shared content, so this doc is short.

---

## 1. File Map

| File | Asset type | Exports |
|---|---|---|
| Celesteneukirchen/Demolition/Settings/DA_Demolition_CS_Default.json | BHDemolitionComponentSettings | 1 |

---

## 2. Demolition Component Settings (`DA_Demolition_CS_Default`)

| Property | Value | Note |
|---|---|---|
| InstanceStartCullDistance | 101,000 | Instances start to cull at this distance (Unreal units, likely cm, so about 1,010 m) |
| InstanceEndCullDistance | 101,100 | Instances are fully culled at this distance (about 1,011 m) |
| Cull band width | 100 | The gap between start and end (100 units) is a fade band, inferred from the names |
| CollisionProfileName | BHDemolition | Collision profile applied to the demolition instances |

The settings target the `BHDemolitionComponentSettings` class. The name suggests the component handles demolition instances. The cull distances are very large, which suggests the instances are meant to stay visible across most of a map (inferred).

---

## 3. Still Not Pulled / Limitations

- **The demolition component and its instances are not in this dump.** The meshes, the destruction logic and the collision profile definition itself are outside this folder.
- **Units are assumed to be Unreal units (cm by default).** The conversion to metres above is an assumption.
  - **See [`docs/UNITS.md`](docs/UNITS.md)** for the project-wide units reference (UE 5.7 defaults + Wardogs-specific suffixes).
- **Single asset.** Nothing else in the Developers folder is available to cross-check.

