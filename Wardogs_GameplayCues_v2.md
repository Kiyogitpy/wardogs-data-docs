---
title: "GameplayCues"
parent: "Content"
---

# Wardogs: GameplayCues Data Reference (v2)
*Extracted from cooked game data ([`Wardogs/Content/GameplayCues`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameplayCues), 1 file). Values are raw asset values.*

> **Scope:** one VFX data asset for the vehicle countermeasure smoke screen. The folder name says gameplay cue, but the asset is a smoke-grenade VFX configuration instance.

---

## 1. File Map

| File | Asset type (class) | Parent (template) |
|---|---|---|
| Vehicles/Countermeasures/DA_SmokeScreen.json | PDA_SmokeGrenade_C (Blueprint data asset) | /Game/VFX/Shared/PDA_SmokeGrenade (shared smoke-grenade VFX) |

---

## 2. Smoke Screen Values ([`DA_SmokeScreen`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameplayCues/Vehicles/Countermeasures/DA_SmokeScreen.json))

| Property | Value | Note |
|---|---|---|
| Diameter | 0.1 | Very small for a smoke cloud. Probably a scale factor, not a size in cm (unclear) |
| Total Duration | 6.0 | Seconds the smoke is visible in total |
| Fade In Time | 2.0 | Seconds to reach full density |
| Fade Out Time | 2.0 | Seconds to fade out at the end |
| Full-density hold (derived) | 2.0 | Total minus both fades, so 2.0 s at full density |
| SpriteMaxSize | 1,500 | Largest sprite size for the smoke particles (units not stated, likely Unreal units) |

The timing is a 2 s fade in, a 2 s hold and a 2 s fade out, for a 6 s total (2 + 2 + 2 = 6).

---

## 3. How Values Combine

The data asset feeds the shared smoke-grenade VFX. Its timing values set the visible life of one smoke cloud, and `SpriteMaxSize` sets the largest particle. The `Diameter` value sits alongside them. The shared VFX Blueprint is not in this dump, so the way `Diameter` is applied is unknown.

---

## 4. Still Not Pulled / Limitations

- **The shared VFX Blueprint (`PDA_SmokeGrenade`) is not in this dump.** Its logic, the particle systems and the emitter settings are unknown.
- **Only one cue.** The folder holds a single smoke-screen asset. Other cues (muzzle flash, hit markers, explosions) are not in this folder.
- **Diameter units are unclear.** A value of 0.1 is too small to be a cloud diameter in cm, so it is probably a scale factor.

