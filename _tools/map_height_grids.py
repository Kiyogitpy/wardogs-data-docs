"""Decode the water height grids (WDWaterHeightGridAsset) and publish them (round 89, V4-22).

Reads the 40 Fluid Flux grids under Content/Environment/Water/FluidFlux/** and the Water Gym grid under
Content/Maps/Gyms/Water, and writes
  assets/data/map-height-grids.json          per grid and per map: grid size, cell size, world extent, water surface
                                              minimum and maximum in metres, wet cell count
  assets/img/maps/<map>-water-height.png     water surface height per map (bakurani, ozeti) and the gym (gym)
  the generated table between the height-grids markers in content/Wardogs_Environment_v2.md (section 13b)

Decode (verified in docs/evidence/round89-map.md):
  Heights is row-major, GridHeight rows of GridWidth values, row 0 at world Y = worldmin.Y, +Y with the row index.
  Cell size is WorldSize.X / GridWidth by WorldSize.Y / GridHeight (cm).
  65535 = no water. Any other value v: z_cm = zmin + v / 65534 * (zmax - zmin), with zmin and zmax the two unnamed
  doubles (_aaaajahedjfgkemenmnfj, _aaaajbpajedfcbkcoihjn). The smallest wet value is always 0 and the largest 65534.

Usage (needs numpy and Pillow):  python -I _tools/map_height_grids.py [--check]
"""
import argparse, glob, json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLUX = os.path.join(ROOT, 'data/Wardogs/Content/Environment/Water/FluidFlux')
GYM = os.path.join(ROOT, 'data/Wardogs/Content/Maps/Gyms/Water')
OUT_JSON = os.path.join(ROOT, 'assets/data/map-height-grids.json')
OUT_IMG = os.path.join(ROOT, 'assets/img/maps')
ENV_MD = os.path.join(ROOT, 'content/Wardogs_Environment_v2.md')
BEGIN, END = '<!-- height-grids:begin -->', '<!-- height-grids:end -->'
K0, K1, KS = '_aaaajahedjfgkemenmnfj', '_aaaajbpajedfcbkcoihjn', '_aaabflcohlopnaadhglfk'
DRY = 65535
MAPS = {'bakurani': ('Kavkazi', 'Bakurani'), 'ozeti': ('Europe', 'Ozeti')}
PX_CM = 1600          # image pixel size in cm
DRYCOL = (28, 30, 36)
STOPS = [(0.0, (20, 60, 150)), (0.25, (30, 150, 200)), (0.5, (70, 180, 90)), (0.75, (235, 215, 80)), (1.0, (250, 250, 245))]


def load(p):
    t = open(p, encoding='utf8').read()
    return json.JSONDecoder().raw_decode(t[t.index('{'):])[0]['Properties']


def read_grid(path, world):
    j = load(path)
    W, H = j['GridWidth'], j['GridHeight']
    h = np.array(j['Heights'], dtype=np.int64)
    assert h.size == W * H, path
    h = h.reshape(H, W)
    wet = h != DRY
    z0, z1 = j[K0], j[K1]
    assert h[wet].min() == 0 and h[wet].max() == 65534, path
    z = np.where(wet, z0 + h / 65534.0 * (z1 - z0), np.nan)
    ws = j['WorldSize']
    name = os.path.basename(path)[:-5]
    g = dict(name=name, world=world, grid_w=W, grid_h=H, cell_x_cm=ws['X'] / W, cell_y_cm=ws['Y'] / H,
             x0_cm=j['worldmin']['X'], y0_cm=j['worldmin']['Y'], size_x_cm=ws['X'], size_y_cm=ws['Y'],
             z0_cm=z0, z1_cm=z1, wet=int(wet.sum()), state=j[KS]['AssetPathName'].rsplit('/', 1)[-1].split('.')[0])
    sp = os.path.join(os.path.dirname(path), g['state'] + '.json')
    if os.path.exists(sp):
        s = load(sp)
        loc, sz = s['AreaLocation'], s['AreaSize']
        g['sim_centre_matches'] = bool(abs(loc['X'] - (g['x0_cm'] + ws['X'] / 2)) < 1 and abs(loc['Y'] - (g['y0_cm'] + ws['Y'] / 2)) < 1)
        g['in_sim_box'] = bool(loc['Z'] - sz['Z'] <= z0 and z1 <= loc['Z'])
    return g, z


def cmap(t):
    t = np.clip(t, 0, 1)
    out = np.zeros(t.shape + (3,), np.float64)
    xs = [s[0] for s in STOPS]
    for c in range(3):
        out[..., c] = np.interp(t, xs, [s[1][c] for s in STOPS])
    return out.astype(np.uint8)


def font(sz):
    for n in ('arial.ttf', 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(n, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def pool(z, b):
    """Block-average the wet samples of z by b x b (nan where a block has no water)."""
    H, W = z.shape
    H2, W2 = H // b * b, W // b * b
    blk = z[:H2, :W2].reshape(H2 // b, b, W2 // b, b)
    cnt = np.sum(~np.isnan(blk), axis=(1, 3))
    tot = np.nansum(blk, axis=(1, 3))
    out = np.full(cnt.shape, np.nan)
    ok = cnt > 0
    out[ok] = tot[ok] / cnt[ok]
    return out


def render(grids, extra_box, title, px_cm):
    """Mosaic of the water surface height. grids: list of (g, z). Returns (Image, summary)."""
    x0 = min(g['x0_cm'] for g, _ in grids); x1 = max(g['x0_cm'] + g['size_x_cm'] for g, _ in grids)
    y0 = min(g['y0_cm'] for g, _ in grids); y1 = max(g['y0_cm'] + g['size_y_cm'] for g, _ in grids)
    if extra_box:
        x0 = min(x0, extra_box[0]); x1 = max(x1, extra_box[1]); y0 = min(y0, extra_box[2]); y1 = max(y1, extra_box[3])
    zmin = min(np.nanmin(z) for _, z in grids); zmax = max(np.nanmax(z) for _, z in grids)
    w, h = int(np.ceil((x1 - x0) / px_cm)), int(np.ceil((y1 - y0) / px_cm))
    acc = np.zeros((h, w)); cnt = np.zeros((h, w))
    for g, z in grids:
        b = max(1, int(round(px_cm / g['cell_x_cm'])))
        p = pool(z, b)
        ox = int(round((g['x0_cm'] - x0) / px_cm)); oy = int(round((g['y0_cm'] - y0) / px_cm))
        ph, pw = p.shape
        ph2, pw2 = min(ph, h - oy), min(pw, w - ox)
        sub = p[:ph2, :pw2]
        ok = ~np.isnan(sub)
        acc[oy:oy + ph2, ox:ox + pw2][ok] += sub[ok]
        cnt[oy:oy + ph2, ox:ox + pw2][ok] += 1
    img = np.zeros((h, w, 3), np.uint8); img[:] = DRYCOL
    ok = cnt > 0
    zz = np.where(ok, acc / np.maximum(cnt, 1), 0)
    img[ok] = cmap((zz[ok] - zmin) / (zmax - zmin))
    im = Image.fromarray(img)
    d = ImageDraw.Draw(im)
    if extra_box:
        d.rectangle([(extra_box[0] - x0) / px_cm, (extra_box[2] - y0) / px_cm, (extra_box[1] - x0) / px_cm, (extra_box[3] - y0) / px_cm], outline=(255, 255, 255))
    f = font(12)
    pad = 6
    lw = min(200, w - 2 * pad)
    for i in range(lw):
        d.line([(pad + i, h - 22), (pad + i, h - 14)], fill=tuple(int(c) for c in cmap(np.array([i / max(1, lw - 1)]))[0]))
    d.text((pad, h - 38), f'{zmin / 100:.0f} m', fill=(255, 255, 255), font=f)
    d.text((pad + lw - 40, h - 38), f'{zmax / 100:.0f} m', fill=(255, 255, 255), font=f)
    d.text((pad, 4), title, fill=(255, 255, 255), font=f)
    return im, dict(zmin_m=round(zmin / 100, 2), zmax_m=round(zmax / 100, 2), px_m=px_cm / 100)


def build():
    maps = {}
    for key, (world, label) in MAPS.items():
        paths = sorted(glob.glob(os.path.join(FLUX, world, 'WHG_*.json')))
        maps[key] = [read_grid(p, world) for p in paths]
    gym = [read_grid(os.path.join(GYM, 'WHG_PDA_Flux_Gym_Water.json'), 'Gym')]
    bounds = json.load(open(os.path.join(ROOT, 'assets/data/map-boundaries.json')))['maps']
    result = {'_note': 'Round 89. Water height grids decoded: z_cm = z0 + v/65534*(z1-z0), 65535 = no water, row-major with row 0 at worldmin.Y. Generated by _tools/map_height_grids.py. Heights in metres on the game height scale; extents in world metres.',
              'maps': {}, 'grids': []}
    images = {}
    for key, gl in list(maps.items()) + [('gym', gym)]:
        bm = None
        if key in MAPS:
            pb = bounds[MAPS[key][1]]['play_box_m']
            bm = (pb['x_min'] * 100, pb['x_max'] * 100, pb['y_min'] * 100, pb['y_max'] * 100)
        label = MAPS[key][1] if key in MAPS else 'Water Gym'
        im, s = render(gl, bm, f'{label}: water surface height (m)', PX_CM if key != 'gym' else 800)
        images[key] = im
        gs = [g for g, _ in gl]
        cells = sum(g['wet'] for g in gs)
        area = sum(g['wet'] * g['cell_x_cm'] * g['cell_y_cm'] for g in gs) / 1e10
        result['maps'][key] = dict(
            map=label, grids=len(gs), wet_cells=cells, wet_area_km2_sum=round(area, 2),
            cell_sizes_m=sorted({g['cell_x_cm'] / 100 for g in gs}),
            extent_m=dict(x_min=round(min(g['x0_cm'] for g in gs) / 100), x_max=round(max(g['x0_cm'] + g['size_x_cm'] for g in gs) / 100),
                          y_min=round(min(g['y0_cm'] for g in gs) / 100), y_max=round(max(g['y0_cm'] + g['size_y_cm'] for g in gs) / 100)),
            water_min_m=round(min(np.nanmin(z) for _, z in gl) / 100, 2), water_max_m=round(max(np.nanmax(z) for _, z in gl) / 100, 2),
            image=f'assets/img/maps/{key}-water-height.png')
        for g, z in gl:
            result['grids'].append(dict(
                map=label, name=g['name'], state=g['state'], grid=[g['grid_w'], g['grid_h']],
                cell_m=[g['cell_x_cm'] / 100, g['cell_y_cm'] / 100],
                origin_m=[round(g['x0_cm'] / 100, 2), round(g['y0_cm'] / 100, 2)],
                size_m=[g['size_x_cm'] / 100, g['size_y_cm'] / 100],
                z0_m=round(g['z0_cm'] / 100, 2), z1_m=round(g['z1_cm'] / 100, 2),
                wet_cells=g['wet'], wet_share=round(g['wet'] / (g['grid_w'] * g['grid_h']), 4),
                centre_matches_sim=g.get('sim_centre_matches'), range_in_sim_box=g.get('in_sim_box')))
    return result, images


def table(result):
    rows = ['| Grid asset | Map | Grid (W x H) | Cell (m) | Origin X, Y (m) | Size X x Y (m) | Water surface min to max (m) | Wet cells |',
            '|---|---|---|---|---|---|---|---|']
    for g in result['grids']:
        if g['map'] == 'Water Gym':
            continue
        cell = f"{g['cell_m'][0]:g}" if g['cell_m'][0] == g['cell_m'][1] else f"{g['cell_m'][0]:g} x {g['cell_m'][1]:g}"
        rows.append(f"| {g['name']} | {g['map']} | {g['grid'][0]} x {g['grid'][1]} | {cell} | {g['origin_m'][0]:,.0f}, {g['origin_m'][1]:,.0f} | "
                    f"{g['size_m'][0]:,.0f} x {g['size_m'][1]:,.0f} | {g['z0_m']:,.1f} to {g['z1_m']:,.1f} | {g['wet_cells']:,} ({g['wet_share'] * 100:.1f}%) |")
    return '\n'.join(rows)


def png_equal(path, im):
    if not os.path.exists(path):
        return False
    a = Image.open(path).convert('RGB')
    return a.size == im.size and a.tobytes() == im.tobytes()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    result, images = build()
    js = json.dumps(result, indent=1, ensure_ascii=False) + '\n'
    md = open(ENV_MD, encoding='utf8', newline='').read()
    nl = '\r\n' if '\r\n' in md else '\n'
    i, k = md.index(BEGIN), md.index(END)
    new_md = md[:i + len(BEGIN)] + nl + table(result).replace('\n', nl) + nl + md[k:]
    stale = []
    if not os.path.exists(OUT_JSON) or open(OUT_JSON, encoding='utf8', newline='').read().replace('\r\n', '\n') != js:
        stale.append(OUT_JSON)
    if new_md != md:
        stale.append(ENV_MD)
    for key, im in images.items():
        p = os.path.join(OUT_IMG, f'{key}-water-height.png')
        if not png_equal(p, im):
            stale.append(p)
    if a.check:
        for s in stale:
            print('stale:', os.path.relpath(s, ROOT))
        sys.exit(1 if stale else 0)
    open(OUT_JSON, 'w', encoding='utf8', newline='\n').write(js)
    open(ENV_MD, 'w', encoding='utf8', newline='').write(new_md)
    for key, im in images.items():
        im.save(os.path.join(OUT_IMG, f'{key}-water-height.png'), optimize=True)
    print('wrote', len(result['grids']), 'grids,', len(images), 'images')
    for k, v in result['maps'].items():
        print(k, v['grids'], v['water_min_m'], v['water_max_m'], v['extent_m'], v['cell_sizes_m'], v['wet_area_km2_sum'])
    bad = [g['name'] for g in result['grids'] if g['centre_matches_sim'] is False or g['range_in_sim_box'] is False]
    print('sim box / centre mismatches:', bad)


main()
