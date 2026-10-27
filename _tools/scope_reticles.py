"""Scope reticles as seen through the scope: the HUD reticle textures behind DT_ScopeReticleTypes.

    python -I _tools/scope_reticles.py <dump-dir> <png-dir>

<dump-dir> holds WdExtract `dump` output (normal-order.usmap) of DT_ScopeReticleTypes, the W_ScopeReticle_*
widgets and the MI_ScopeReticleTempTextures_* materials; <png-dir> holds WdExtract `textures` output of the
T_UI_*_Scope_SDF textures those materials name. Static extraction only, no game run.

Sights whose reticle is not a texture are drawn by scope_reticles_procedural.py from the material parameters
(items get "source": "procedural"; the cooked files hold no material graph, so those images are approximate, see
docs/evidence/round84-procedural-reticles.md). One command regenerates every image and the JSON.

Chain: DT_ScopeReticleTypes row (AllowedSubSlotItems = the scope's ItemId) -> WidgetClass W_ScopeReticle_*
-> the material instance the widget draws -> its ScopeTexture parameter. Only the widgets drawn from such a
texture get an image; the others (10x, MOA, Cross and the SGHT_0xx scopes) build their reticle procedurally in
the material graph and have no texture to show.

The texture's alpha channel is the reticle line field. The image is the material's line test,
alpha >= 1 - AlphaLineWidth (softened by AlphaLineFeather), drawn black on transparent and cropped square
around the texture centre (the aim point). Writes assets/img/icons/scope-reticles/<texture>.png and
assets/data/scope-reticles.json ({ItemId tag: {texture, png, widget, material}}).
"""
import glob
import json
import os
import re
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scope_reticles_procedural as proc  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_IMG = os.path.join(ROOT, "assets", "img", "icons", "scope-reticles")
OUT_JSON = os.path.join(ROOT, "assets", "data", "scope-reticles.json")
SIZE = 512


def exports(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def short(obj_path):
    return obj_path.rsplit("/", 1)[-1].split(".", 1)[0]


def render(png, width, feather):
    a = np.asarray(Image.open(png))[..., 3].astype(np.float32) / 255.0
    t = 1.0 - width
    lo, hi = t - feather / 2, t + feather / 2
    line = np.clip((a - lo) / max(hi - lo, 1e-6), 0, 1) if feather > 0 else (a >= t).astype(np.float32)
    ys, xs = np.nonzero(line > 0.02)
    h, w = line.shape
    cy, cx = h // 2, w // 2
    r = int(max(abs(ys - cy).max(), abs(xs - cx).max()) * 1.12) + 8
    crop = line[cy - r:cy + r, cx - r:cx + r]
    rgba = np.zeros(crop.shape + (4,), np.uint8)
    rgba[..., 3] = (crop * 255).astype(np.uint8)
    return Image.fromarray(rgba).resize((SIZE, SIZE), Image.LANCZOS)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    dump, pngs = sys.argv[1], sys.argv[2]
    rows = {}
    for ex in exports(os.path.join(dump, "DT_ScopeReticleTypes.json")):
        rows.update(ex.get("Rows") or {})
    mats = {}
    for p in glob.glob(os.path.join(dump, "MI_ScopeReticleTempTextures_*.json")):
        for ex in exports(p):
            props = ex.get("Properties") or {}
            tex = [x["ParameterValue"]["ObjectPath"] for x in props.get("TextureParameterValues", [])
                   if x["ParameterInfo"]["Name"] == "ScopeTexture"]
            scal = {x["ParameterInfo"]["Name"]: x["ParameterValue"] for x in props.get("ScalarParameterValues", [])}
            if tex:
                mats[ex["Name"]] = {"texture": short(tex[0]), "width": scal.get("AlphaLineWidth"),
                                    "feather": scal.get("AlphaLineFeather", 0.0)}
    os.makedirs(OUT_IMG, exist_ok=True)
    out, done = {}, {}
    for tag, row in sorted(rows.items()):
        widget = short(row["ScopeReticleWidgetParams"]["WidgetClass"]["AssetPathName"]).removesuffix("_C")
        wpath = os.path.join(dump, widget + ".json")
        if not os.path.exists(wpath):
            continue
        text = open(wpath, encoding="utf-8").read()
        mat = next((m for m in mats if f"'{m}'" in text), None)
        if not mat:
            # procedural widget: the full-screen image draws a material instance of a parametric master
            mi = re.search(r"MaterialInstanceConstant'(MI_SGHT_\d+_Reticle)'", text)
            if mi:
                res = proc.render_mask(dump, mi.group(1))
                if res:
                    img, info = res
                    rel = f"assets/img/icons/scope-reticles/{mi.group(1)}.png"
                    img.save(os.path.join(ROOT, rel), optimize=True)
                    for item in row["FilterRules"]["AllowedSubSlotItems"]:
                        out[item] = {"png": rel, "source": "procedural", "family": "mask", "widget": widget,
                                     "material": mi.group(1), "master": info["master"], "row": tag,
                                     "used": info["used"], "unused": info["unused"]}
                    done[mi.group(1)] = rel
            continue
        m = mats[mat]
        rel = f"assets/img/icons/scope-reticles/{m['texture']}.png"
        if m["texture"] not in done:
            src = glob.glob(os.path.join(pngs, "**", m["texture"] + ".png"), recursive=True)
            if not src:
                sys.exit(f"missing texture PNG {m['texture']}")
            render(src[0], m["width"], m["feather"]).save(os.path.join(ROOT, rel), optimize=True)
            done[m["texture"]] = rel
        for item in row["FilterRules"]["AllowedSubSlotItems"]:
            out[item] = {"texture": m["texture"], "png": rel, "source": "texture", "widget": widget, "material": mat,
                         "row": tag}
    kobra = os.path.join(ROOT, "assets", "img", "icons", "other-sights-reticles", "T_Reticle_KobraSight_Greyscale.png")
    for item, mi in proc.LENS_SIGHTS.items():
        res = proc.render_lens(dump, mi, kobra)
        if not res:
            continue
        img, info = res
        rel = f"assets/img/icons/scope-reticles/{mi}.png"
        img.save(os.path.join(ROOT, rel), optimize=True)
        done[mi] = rel
        out[item] = {"png": rel, "source": "procedural", "family": "lens", "material": mi, "kind": info["kind"],
                     "used": info["used"], "color": list(info["color"])}
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"_note": __doc__.strip().splitlines()[0], "items": out}, f, indent=1, sort_keys=True)
        f.write("\n")
    print(f"{len(done)} reticle images, {len(out)} scopes -> {os.path.relpath(OUT_JSON, ROOT)}")


if __name__ == "__main__":
    main()
