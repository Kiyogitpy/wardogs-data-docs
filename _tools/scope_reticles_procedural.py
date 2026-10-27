"""Procedural through-the-scope / lens reticles, drawn from material parameters only (called by scope_reticles.py).

The cooked game files hold NO material graph: M_* masters export only CachedExpressionData (parameter names and
default values, referenced textures); the expression nodes are compiled into shader code. So a reticle here is the
parameter set of the sight's material instance (master defaults overlaid by the instance's overrides) drawn with the
shape the parameter NAMES describe. Positions and sizes are the stored numbers in the material's centred UV space
(+y down, aim point at the origin); how the shader combines them (which side a Pos is measured from, whether a size is a
radius or a diameter, the extent of the crosshair arms, the HDR emissive multiplier) is not stored, so every image
made here is approximate (source "procedural"). docs/evidence/round84-procedural-reticles.md lists, per sight, which
parameters were used and which were not. The images are cropped square around the aim point, like the texture ones.

Families (each is a few primitives, all sizes from the sight's parameters):
  mask   M_SGHT_026/028/029/030/031/036_Reticle (full-screen UMG image drawn with the material instance MI_SGHT_0xx_Reticle)
  lens   M_Reticle_Master instances; Reticle_Index 0 = T2 dot (T2_Dot_Size), 1 = Kobra chevron (Kobra_* params;
         drawn from the Gunsmith Kobra reticle texture, tinted with EmissiveColor)
"""
import json
import os

import numpy as np
from PIL import Image, ImageDraw

HI = 4096          # supersampled canvas
SIZE = 512


def jl(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def mat_export(dump, name):
    p = os.path.join(dump, name + ".json")
    if not os.path.exists(p):
        return None
    return next((e for e in jl(p) if e.get("Name") == name), None)


def params(dump, mi_name):
    """Master defaults overlaid by the instance's scalar/vector overrides -> ({name: float}, {name: [r,g,b]})."""
    mi = mat_export(dump, mi_name)
    if mi is None:
        return None, None
    props = mi.get("Properties") or {}
    scal, vec = {}, {}
    parent = (props.get("Parent") or {}).get("ObjectName", "")
    master = parent.split("'")[1] if "'" in parent else None
    mm = mat_export(dump, master) if master else None
    if mm:
        c = mm["CachedExpressionData"]
        names = [p["Name"] for p in c["RuntimeEntries"]["ParameterInfoSet"]]
        scal.update(zip(names, c["ScalarValues"]))
    for x in props.get("ScalarParameterValues", []):
        scal[x["ParameterInfo"]["Name"]] = x["ParameterValue"]
    for x in props.get("VectorParameterValues", []):
        v = x["ParameterValue"]
        vec[x["ParameterInfo"]["Name"]] = [v["R"], v["G"], v["B"]]
    return scal, vec


def norm_color(rgb):
    """Emissive/HDR colours exceed 1; keep the hue, scale the largest channel to 1."""
    m = max(rgb) or 1.0
    return tuple(int(round(255 * c / m)) for c in rgb)


class Canvas:
    def __init__(self):
        self.layers = {}          # colour -> list of (kind, args) drawing ops

    def px(self, x, y, k):
        return HI / 2 + x * k, HI / 2 + y * k


    def finish(self, extent):
        """Render every layer with <extent> UV units mapped to half the image."""
        k = HI / 2 / extent
        out = Image.new("RGBA", (HI, HI), (0, 0, 0, 0))
        for col, ops in self.layers.items():
            m = Image.new("L", (HI, HI), 0)
            d = ImageDraw.Draw(m)
            for kind, a in ops:
                if kind == "rect":
                    x0, y0, x1, y1 = a
                    d.rectangle([*self.px(x0, y0, k), *self.px(x1, y1, k)], fill=255)
                elif kind == "disc":
                    cx, cy, r = a
                    d.ellipse([*self.px(cx - r, cy - r, k), *self.px(cx + r, cy + r, k)], fill=255)
                elif kind == "ring":
                    cx, cy, r, w = a
                    ro, ri = r + w / 2, max(r - w / 2, 0)
                    d.ellipse([*self.px(cx - ro, cy - ro, k), *self.px(cx + ro, cy + ro, k)], fill=255)
                    d.ellipse([*self.px(cx - ri, cy - ri, k), *self.px(cx + ri, cy + ri, k)], fill=0)
                elif kind == "poly":
                    d.polygon([self.px(x, y, k) for x, y in a], fill=255)
            out.alpha_composite(Image.merge("RGBA", [Image.new("L", (HI, HI), c) for c in col] + [m]))
        return out.resize((SIZE, SIZE), Image.LANCZOS)


def add(c, col, kind, *a):
    c.layers.setdefault(col, []).append((kind, a))


def new():
    return Canvas()


BLACK = (0, 0, 0)


def thick_line(c, col, x0, y0, x1, y1, w):
    """Axis-aligned bar between two points, w thick."""
    add(c, col, "rect", min(x0, x1) - (w / 2 if x0 == x1 else 0), min(y0, y1) - (w / 2 if y0 == y1 else 0),
        max(x0, x1) + (w / 2 if x0 == x1 else 0), max(y0, y1) + (w / 2 if y0 == y1 else 0))


# ---- mask family -----------------------------------------------------------------------------------------------

def mask_reticle(p, v, used):
    """Shapes named by the M_SGHT_0xx_Reticle parameters. `used` collects the parameter names that drew something."""
    g = lambda n, d=None: p.get(n, d)
    col_main = BLACK
    illum_col = None
    for n in ("DotColor", "CircleColor", "CenterColor"):
        if n in v:
            illum_col = norm_color(v[n])
            used.add(n)
    c = new()
    dot_col = illum_col or BLACK
    feat = 0.0   # extent of the non-arm features (UV units)

    def U(*names):
        used.update(n for n in names if n in p)

    # centre dot (+ optional vertical offset)
    if g("CenterDotSize"):
        # CenterDotHeight_Pos (master default 0.3) is not applied: with the ring it would put the dot far outside it
        add(c, dot_col, "disc", 0, 0, g("CenterDotSize"))
        U("CenterDotSize")
        feat = max(feat, g("CenterDotSize"))
    # centre ring (026, 028, 029)
    if g("CenterRingSize") and g("CenterRingLineWidth"):
        cy = g("CenterRing_Pos", 0.0)
        r, w = g("CenterRingSize"), g("CenterRingLineWidth")
        add(c, dot_col if "CircleColor" in v else col_main, "ring", 0, cy, r, w)
        U("CenterRingSize", "CenterRingLineWidth", "CenterRing_Pos", "CircleColor")
        feat = max(feat, abs(cy) + r + w / 2)
    if "CenterDot_Pos" in p and g("CenterDotSize"):
        add(c, dot_col, "disc", 0, g("CenterDot_Pos"), g("CenterDotSize"))
        U("CenterDot_Pos")
        feat = max(feat, abs(g("CenterDot_Pos")) + g("CenterDotSize"))
    # range stem and ticks (stadia)
    rt = g("RangeLineThickness")
    stem_top = stem_bot = None
    if rt and g("RangeHeightScale") is not None and "RangeHeight_Pos" in p:
        half = g("RangeHeightScale") / 2
        cy = g("RangeHeight_Pos")
        stem_top, stem_bot = cy - half, cy + half
        # ticks: Line01/04 at the stem ends, 02/03 at their Pos relative to the stem centre; widths are full tick length
        ticks = [(stem_top, g("RangeLine01_Width", 0)), (cy + g("RangeLine02_Pos", 0), g("RangeLine02_Width", 0)),
                 (cy + g("RangeLine03_Pos", 0), g("RangeLine03_Width", 0)), (stem_bot, g("RangeLine04_Width", 0))]
        any_tick = False
        for y, wd in ticks:
            if wd:
                add(c, col_main, "rect", -wd / 2, y - rt / 2, wd / 2, y + rt / 2)
                any_tick = True
        if g("RangeHeightScale") > 0:
            add(c, col_main, "rect", -rt / 2, stem_top, rt / 2, stem_bot)
        U("RangeLineThickness", "RangeHeightScale", "RangeHeight_Pos", "RangeLine01_Width", "RangeLine02_Pos",
          "RangeLine02_Width", "RangeLine03_Pos", "RangeLine03_Width", "RangeLine04_Width")
        feat = max(feat, abs(stem_top), abs(stem_bot))
    # 031 / 036: range ticks given only by Pos
    if "RangeLineWidth" in p and "RangeLine01_Pos" in p:
        for n in ("RangeLine01_Pos", "RangeLine02_Pos"):
            y = -g(n)
            add(c, col_main, "rect", -g("RangeLineWidth") / 2, y - g("RangeLineThickness") / 2,
                g("RangeLineWidth") / 2, y + g("RangeLineThickness") / 2)
            feat = max(feat, abs(y))
        U("RangeLineWidth", "RangeLine01_Pos", "RangeLine02_Pos", "RangeLineThickness")
    # 036: eight range ticks (Pos only) of BasePipWidth
    if "BasePipWidth" in p:
        for i in range(1, 9):
            n = f"RangeLine0{i}_Pos"
            if n in p:
                y = g(n)
                add(c, col_main, "rect", -g("BasePipWidth") / 2, y - g("CrosshairLineWidth", 0.004), g("BasePipWidth") / 2,
                    y + g("CrosshairLineWidth", 0.004))
                U(n)
                feat = max(feat, abs(y))
        U("BasePipWidth")
    # crosshair with flair posts (029, 030, 031, 036)
    if "CrosshairLineWidth" in p and "FlairLineWidth" in p:
        cw, fw = g("CrosshairLineWidth"), g("FlairLineWidth")
        cutw = g("FlairCutWidth", g("FlairOuterCutWidth", 0.2))
        cuth = g("FlairCutHeight", g("FlairOuterCutHeight", 0.2))
        arm = 1.35 * max(feat, cutw / 2, cuth / 2, 0.05) if feat else 1.35 * max(cutw / 2, cuth / 2)
        arm = max(arm, 1.6 * max(cutw, cuth) / 2)
        # thin cross through the whole field, thick posts outside the cut
        add(c, col_main, "rect", -arm, -cw / 2, arm, cw / 2)
        add(c, col_main, "rect", -cw / 2, -arm, cw / 2, arm)
        add(c, col_main, "rect", -arm, -fw / 2, -cutw / 2, fw / 2)
        add(c, col_main, "rect", cutw / 2, -fw / 2, arm, fw / 2)
        add(c, col_main, "rect", -fw / 2, cuth / 2, fw / 2, arm)
        # which posts exist is not stored; all four are drawn
        add(c, col_main, "rect", -fw / 2, -arm, fw / 2, -cuth / 2)
        U("CrosshairLineWidth", "FlairLineWidth", "FlairCutWidth", "FlairCutHeight", "FlairOuterCutWidth",
          "FlairOuterCutHeight")
        feat = max(feat, arm)
    return c, feat


MASKS = {
    "M_SGHT_026_Reticle": mask_reticle, "M_SGHT_028_Reticle": mask_reticle, "M_SGHT_029_Reticle": mask_reticle,
    "M_SGHT_030_Reticle": mask_reticle, "M_SGHT_031_Reticle": mask_reticle, "M_SGHT_036_Reticle": mask_reticle,
}


def render_mask(dump, mi_name):
    p, v = params(dump, mi_name)
    if p is None:
        return None
    parent = (mat_export(dump, mi_name)["Properties"].get("Parent") or {}).get("ObjectName", "")
    master = parent.split("'")[1]
    fn = MASKS.get(master)
    if not fn:
        return None
    used = set()
    c, feat = fn(p, v, used)
    # the crosshair arms of the flair family were sized from feat; frame the image at 1.1 x the arm
    if not c.layers:
        return None
    ext = feat * 1.1 or 0.5
    img = c.finish(ext)
    unused = sorted(n for n in p if n not in used and n not in ("Feather", "GlobalScale", "RefractionDepthBias",
                                                                 "GlobalVerticalOffset"))
    return img, {"master": master, "used": sorted(used), "unused": unused}


# ---- lens family -------------------------------------------------------------------------------------------------

def render_lens(dump, mi_name, kobra_png):
    p, v = params(dump, mi_name)
    if p is None:
        return None
    col = norm_color(v.get("EmissiveColor", [1, 0, 0]))
    idx = int(p.get("Reticle_Index", 0)) if "Reticle_Index" in p else None
    if "T2_Dot_Size" in p and not any(k.startswith(("FourReticle", "OKP7", "Holographic", "Kobra")) for k in p):
        # a single dot; its size multiplier (ReticleSize / ReticleSize_SDF) is not stored as a fixed number, so the
        # dot is drawn at a fixed 5 % of the frame
        c = new()
        add(c, col, "disc", 0, 0, 0.05)
        return c.finish(0.5), {"kind": "T2 dot", "used": ["T2_Dot_Size", "EmissiveColor"],
                               "color": col, "reticle_index": idx, "dot_size": p["T2_Dot_Size"]}
    if "Kobra_Center_Size" in p and os.path.exists(kobra_png):
        a = np.asarray(Image.open(kobra_png).convert("RGBA"))[..., 3].astype(np.float32) / 255.0
        ys, xs = np.nonzero(a > 0.05)
        cy, cx = a.shape[0] // 2, a.shape[1] // 2
        r = int(max(abs(ys - cy).max(), abs(xs - cx).max()) * 1.12) + 8
        crop = a[cy - r:cy + r, cx - r:cx + r]
        rgba = np.zeros(crop.shape + (4,), np.uint8)
        rgba[..., :3] = col
        rgba[..., 3] = (crop * 255).astype(np.uint8)
        return Image.fromarray(rgba).resize((SIZE, SIZE), Image.LANCZOS), {
            "kind": "Kobra chevron (Gunsmith texture)", "used": ["Reticle_Index", "EmissiveColor"], "color": col,
            "reticle_index": idx}
    return None


# sight ItemId tag -> (family, material instance). Mask sights find theirs through the widget, see below.
LENS_SIGHTS = {
    "Id.Item.SGHT_009": "MI_SGHT_009_Reticle",
    "Id.Item.SGHT_025": "MI_SGHT_025_Reticle",
    "Id.Item.SGHT_027": "MI_SGHT_027_Lens",
    "Id.Item.SGHT_033": "MI_Optics_SGHT_033_Lens",
    "Id.Item.SGHT_038": "MI_Optics_SGHT_038_Lens",
}
