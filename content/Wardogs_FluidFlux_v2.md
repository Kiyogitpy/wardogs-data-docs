---
title: "Fluid Flux"
redirect_from: ["/Wardogs_FluidFlux_v2.html", "/Wardogs_FluidFlux_v2"]
parent: "World, Visuals & Audio"
description: "The waterline gradient curve and the file map of the fluid assets."
---

# Wardogs: FluidFlux Data Reference
*Extracted from cooked game data (`Wardogs/Content/FluidFlux`, 2 files). Values are raw curve keys.*

> **Scope:** the underwater surface waterline gradient. FluidFlux is a fluid-simulation plugin, and this folder holds only its waterline colour data. No simulation settings are present.

---

## 1. File Map

| File | Asset type | Role |
|---|---|---|
| Surface/Underwater/Curves/C_Waterline.json | CurveLinearColor | Four-channel colour curve (the gradient itself) |
| Surface/Underwater/Curves/CA_Waterline.json | CurveLinearColorAtlas | Atlas that stores the gradient as a 256 x 1 strip |

---

## 2. Waterline Gradient (`C_Waterline`)

`C_Waterline` is a `CurveLinearColor` with four float channels. The export does not label the channels. Under the Unreal `CurveLinearColor` convention they are R, G, B and A, and the labels below use that reading.

| Channel (inferred) | Keys (time, value) | Interpolation |
|---|---|---|
| channel 0 | (0, 1), (0.2, 1.075), (0.7, 1), (1, 1) | RCIM_Cubic x4 |
| channel 1 | (0, 1.481e-08), (0.1, 1), (0.96, 1), (1, 1.481e-08) | RCIM_Linear x4 |
| channel 2 | (0, 1.468e-07), (0.3, 1), (0.6, -0.25), (1, 1.468e-07) | RCIM_Linear x4 |
| channel 3 | (-0.2, -7.604e-08), (0.1, -7.604e-08), (0.2, 0.375), (0.3, 0.625), (0.7, -1.018e-07), (0.9, -1.018e-07) | RCIM_Linear x3, RCIM_Cubic x3 |

- `CA_Waterline` points at `C_Waterline` and is imported at 256 x 1. The atlas is most likely the baked form of the gradient, so the curve time axis would map across the 256 pixels (inferred).
- Channel 0 is nearly flat at 1.0, with a small bump to 1.075 at t=0.2. Channel 1 ramps up to 1 at t=0.1 and falls to 0 at t=1. Channel 2 peaks at 1.0 at t=0.3 and dips to -0.25 at t=0.6. Channel 3 rises from 0 at t=0.1 to 0.625 at t=0.3, and is back to 0 by t=0.7.
- Values fall outside 0 to 1 in two places (1.075 and -0.25). Curves allow this. Whether a colour channel clamps it depends on how the atlas is sampled, which is not in the export.

---

## 3. How Values Combine

The atlas holds the gradient over time (the time axis of the curve). The underwater surface shader reads it to colour the waterline. The curve's four channels are combined as one colour per sample.

---

## 4. Still Not Pulled / Limitations

- **The shader and material that read the atlas are not in this dump.** The time axis of the gradient and the surface-to-time mapping (what drives the position along the curve) are inferred, not read.
- **Channel labels are inferred** from the Unreal convention, not from the export.
- **No simulation parameters.** FluidFlux settings, the fluid solver, and any wave or flow data are not in this folder.

