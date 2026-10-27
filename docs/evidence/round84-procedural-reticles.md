# Round 84: procedural sight reticles

Goal: an image of the reticle for every sight in the Loadout Builder. Command (one run regenerates all images and
`assets/data/scope-reticles.json`):

    python -I _tools/scope_reticles.py <dump-dir> <png-dir>      # then: python -I _tools/loadout_extras.py

`<dump-dir>` = WdExtract `dump` (normal-order.usmap) of DT_ScopeReticleTypes, the W_ScopeReticle_* widgets, the M_*/MI_* materials
named below; `<png-dir>` = the four T_UI_*_Scope_SDF textures. Generator: `_tools/scope_reticles_procedural.py`.

## Finding: the material graph is not in the cooked files

The task assumed the material expression nodes could be read from the material exports. They cannot. Every `M_*` export
(M_SGHT_026_Reticle ... M_UI_ReticleMask*, M_Reticle_Master) holds only `CachedExpressionData`: the parameter names, their
master default values (`ScalarValues`, `VectorValues`), referenced textures and function names. No expression objects
exist (the only `MaterialExpression` string in the whole set is a `ScreenPosition` entry in M_UI_ReticleMask). The math is
compiled into shaders. So no reticle can be evaluated from its graph. What is stored, per sight: the parameter set of the material instance
(master defaults overlaid by the instance's overrides) and the UMG widget layout.

Method used: draw the shapes the parameter names describe (centre dot, ring, crosshair with flair posts, range stem and ticks,
T2 dot, Kobra chevron) with the stored numbers, in centred UV space, +y down, then crop square around the aim point. Which side a
`*_Pos` is measured from, radius vs diameter, the arm length, `GlobalScale` and the HDR emissive multiplier are shader
choices that are not stored, so every procedural image is approximate in shape and size. Colours: the instance's colour
vector (`DotColor`, `CircleColor`, `CenterColor`, `EmissiveColor`), with HDR values normalised to a largest channel of 1 (hue exact, brightness not).
Lines without a colour parameter are black, as in the texture images. The JSON marks these `"source": "procedural"`
and lists the parameters used (`used`) and not used (`unused`); the 5 texture images keep `"source": "texture"` and are byte-identical.

## Per sight

Exact = the shape and its stored sizes come straight from a texture (the 5 texture scopes). Approximate = drawn from parameters.

| Sight | Chain | Result | Used | Not drawn (missing) |
|---|---|---|---|---|
| 3x Spitfire, 4x Elcan Spectr, 3-6x, 2.5x OPT_08, SGHT_011 | DT row -> W_ScopeReticle_* -> MI_ScopeReticleTempTextures_* -> T_UI_*_Scope_SDF | texture, exact (unchanged) | alpha line test | |
| SGHT_009 Kobra Reflex | lens MI_SGHT_009_Reticle (M_Reticle_Master, Reticle_Index 1, Kobra_Center_Size 0.09, Kobra_Line_Width 0.08) | chevron, approximate | EmissiveColor (1, 0.022, 0) | the shader's chevron arm lengths; drawn from the Gunsmith `T_Reticle_KobraSight_Greyscale` texture (name match with the Kobra_* parameters, not a stored link) |
| SGHT_025, 027, 033, 038 | lens MI_SGHT_025_Reticle / MI_SGHT_027_Lens / MI_Optics_SGHT_033_Lens / MI_Optics_SGHT_038_Lens (Reticle_Index 0, `T2_Dot_Size` 0.025 / 0.003 / 0.005 / 0.0045) | dot, shape exact, size not | EmissiveColor | absolute size: ReticleSize / ReticleSize_SDF multipliers; every dot is drawn at 5 % of the frame |
| SGHT_026 Tricon | W_ScopeReticle_SGHT_026 -> MI_SGHT_026_Reticle -> M_SGHT_026_Reticle | orange ring, dot, stem | CenterRingSize/LineWidth, CenterDotSize, CircleColor/DotColor, RangeHeight*, RangeLine*, RangeLineThickness | CenterRingCutSize (ring gap), CenterDotHeight_Pos (default 0.3, would put the dot outside the ring), numbers (T_UI_NumberSpinner_Medium_SDF, NumbersScale 0) |
| SGHT_028 CQ-2x | W_ScopeReticle_SGHT_028 -> MI_SGHT_028_Reticle | ring, dot, stem, ticks | CenterRing_Pos/Size/LineWidth, CenterDot_Pos/Size, DotColor, Range* | ArrowLength/Width, CenterDotSpacing (dot count unknown) |
| SGHT_029 | W_ScopeReticle_SGHT_029 -> MI_SGHT_029_Reticle | crosshair, flair posts, ring, ticks | CrosshairLineWidth, Flair*, CenterRing*, Range* | arrows, CenterColorMask (red centre), CenterRingCutSize |
| SGHT_030 | W_ScopeReticle_030 -> MI_SGHT_030_Reticle | crosshair, flair posts, ticks | CrosshairLineWidth, Flair*, Range*, CenterColor | CenterColorSize/Feather (red centre disc), numbers; the S_Aim02 reflex dot (MI_SGHT_030_Lens) not drawn |
| SGHT_031 | W_ScopeReticle_SGHT_031 -> MI_SGHT_031_Reticle | crosshair, flair posts, red dot, 2 ticks | all but Feather/GlobalScale | none |
| SGHT_036 | W_ScopeReticle_SGHT_036 -> MI_SGHT_036_Reticle | crosshair, flair posts, red dot, 8 range ticks | CrosshairLineWidth, FlairOuter*, RangeLine01..08_Pos, BasePipWidth, DotColor | FlairInner*, GuideLine* (5 guide lines), numbers; S_Aim02 top dot (MI_SGHT_036_Top_Lens) not drawn |

## Sights still without an image

| Sight | Why |
|---|---|
| SGHT_034 PGO-7 | M_SGHT_034_Reticle draws a ballistic curve (`CurveStart_Y`, `CurveMid_*`, `CurveEnd_Y`) and number columns; grid box and crosses alone would not be the reticle, so nothing is shown |
| SGHT_032 Frontier | its sizes are in mixed units (`Circle_Scale` 0.25, `FlairInnerCut_Height` 21.7, `FlairDashes_Width` 14) that need the shader to interpret |
| SGHT_039, SGHT_040 | `FlareAngle`, `FlareGapSize`, `FlairCutWidth` and the flair width are in pixels with an angle; the flare geometry is not derivable from names |
| SGHT_016 Four Reticle Reflex | `Reticle_Index` 2 selects one of several shapes inside M_Reticle_Master; only `FourReticleReflex_Center_Size/Dot_Size/Line_Width` are stored |
| SGHT_023 OKP 7 | `OKP7_*` outer/center/arrow boxes (0.65 x 0.5, 0.2 x 0.2, arrow 0.2 x 0.01): the way they combine is shader-only |
| 6-10x MOA (ID_10xScopeMoa) | the widget is a composite of M_UI_Reticle_Modular01/03/06/07 images plus TextBlocks; the Modular materials' parameters (Tiling, Segments, SegmentWidth, PanOffset) have no stored meaning |
| Canted irons, SGHT_037 MMGL | iron sights, no reticle material |

## Counts

Sights in the Loadout Builder: 29. With a through-the-scope image: before 5, after 16. With any reticle image (adding the
older Gunsmith lens images for 10x MRAD, 4x Hybrid, Eotech, Compact T-2): before 9, after 20.

## Checks

`python -I _tools/scope_reticles.py E:/r84/work/ret/dump E:/r84/work/ret/png` (16 scopes, 15 images); `python -I _tools/loadout_extras.py --check`;
`python -I _tools/check_links.py` (0 broken). Visual spot check of the new PNGs against the parameter values done on SGHT_009, 026, 028, 029, 031, 036, 027.
