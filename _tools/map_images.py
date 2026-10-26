"""Build the map images for the wiki map articles (round 78).

Reads the extracted world minimap textures (WdExtract `textures` mode, 16,384 px PNG per world) and draws, on a crop
of the play box, the zone region polygons, the Hot Zone Magnet towers (numbered) and the three spawn areas (edge arrows
when they fall outside the crop). Writes assets/img/maps/<map>.jpg (overlay), <map>-plain.jpg (crop only) and
<map>-overview.jpg (whole minimap, play box and spawn areas), plus jutari.jpg and jutari-plain.jpg.

Usage (needs Pillow):
  python -I _tools/map_images.py [--tex-dir DIR] [--out DIR]
Extract the textures first (paks, key and usmap as in the round 36 brief), e.g.
  WdExtract <Paks> <keyfile> <usmap> <TEXDIR> <Paks>/oo2core_9_win64.dll textures
    Wardogs/Content/UI/Tools/WorldCapture/Textures/<World>/T_UI_<World>_VT   (World = Kavkazi, Europe, NorthAmerica, Russia)
Inputs: minimap bounds (content/Wardogs_UI_v2.md section 2, restated in BOUNDS), assets/data/map-magnets-extents.json,
assets/data/vehicle-spawns.json and the DA_ControlZoneRegionsConfig_* region polygons under data/.
Transform: u = (X - xmin) / (xmax - xmin), v = (Y - ymin) / (ymax - ymin); pixel = (u, v) * size, so +Y runs down the image.
The data has no north: orientation is as in the game's minimap.
"""
import argparse, json, math, os, sys
from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(ROOT, 'data/Wardogs/Plugins/GameFeatures/ControlZoneRegions/Content/Data/Config/')
# minimap bounds in cm (content/Wardogs_UI_v2.md section 2): x0, x1, y0, y1
BOUNDS = {
    'Kavkazi': (-1632000, 0, -2040000, -408000),
    'Europe': (-1616000, 16000, -1616000, 16000),
    'NorthAmerica': (-819200, 819200, -819200, 819200),
    'Russia': (-816000, 816000, -816000, 816000),
}
REGION_FILE = {'Kavkazi': CFG + 'DA_ControlZoneRegionsConfig_Kavkazi.json',
               'Europe': CFG + 'Europe/DA_ControlZoneRegionsConfig_Europe.json',
               'NorthAmerica': CFG + 'NorthAmerica/DA_ControlZoneRegionsConfig_NorthAmerica.json'}
# map -> (world, magnets key, spawn areas with the side names the wiki uses)
MAPS = {
    'bakurani': ('Kavkazi', 'Bakurani', [('Baghi', 'Lonestar'), ('Khevuli', 'Valkyra'), ('Chuta', 'Manticore')]),
    'ozeti': ('Europe', 'Ozeti', [('Granada', 'Lonestar'), ('Barcelona', 'Valkyra'), ('Malaga', 'Manticore')]),
    'zestafona': ('NorthAmerica', 'Zestafona', [('Boston', 'Lonestar'), ('Austin', 'Valkyra'), ('Chicago', 'Manticore')]),
    'saburtulo': ('Russia', 'Saburtulo', [('Kuzminki', 'Lonestar'), ('Rostokino', 'Valkyra'), ('Ramenki', 'Manticore')]),
}
SIDE_COL = {'Lonestar': (90, 160, 255), 'Valkyra': (255, 100, 100), 'Manticore': (255, 175, 40)}
TOWER_COL = (255, 40, 200)
MARGIN_M = 500
MAXPX = 1600


def font(sz):
    for n in ('arialbd.ttf', 'arial.ttf', 'DejaVuSans-Bold.ttf'):
        try:
            return ImageFont.truetype(n, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def load_regions(world):
    t = open(REGION_FILE[world], encoding='utf8').read()
    j = json.JSONDecoder().raw_decode(t[t.index('{'):])[0]
    return [(r['ControlZoneRegionName'], [(p['X'] / 100.0, p['Y'] / 100.0) for p in r['ControlZoneRegionPoints']])
            for r in j['Properties']['ControlZoneRegionsData']]


def spawn_pos(world, area):
    d = json.load(open(os.path.join(ROOT, 'assets/data/vehicle-spawns.json')))
    for m in d['infantry_spawn_managers']:
        if m['world'] == world and m['data_layers'] == ['DL_%sSpawn' % area]:
            return m['location'][0] / 100.0, m['location'][1] / 100.0
    raise KeyError(area)


class Frame:
    """World metres -> pixels of a crop (box = x0, x1, y0, y1 in metres; s = output px per metre)."""
    def __init__(self, world, box, s):
        self.b = [v / 100.0 for v in BOUNDS[world]]
        self.box, self.s = box, s

    def px(self, x, y):
        return (x - self.box[0]) * self.s, (y - self.box[2]) * self.s


def crop_world(img, world, box):
    n = img.width
    b = [v / 100.0 for v in BOUNDS[world]]
    def t(x, y):
        return (x - b[0]) / (b[1] - b[0]) * n, (y - b[2]) / (b[3] - b[2]) * n
    x0, y0 = t(box[0], box[2])
    x1, y1 = t(box[1], box[3])
    c = img.crop((round(x0), round(y0), round(x1), round(y1))).convert('RGB')
    k = min(1.0, MAXPX / max(c.size))
    c = c.resize((round(c.width * k), round(c.height * k)), Image.LANCZOS)
    return c, c.width / (box[1] - box[0])


def edge_arrow(d, size, fr, pos, label, col, f):
    """Arrow on the crop edge pointing toward an off-crop world position."""
    w, h = size
    cx, cy = w / 2, h / 2
    px, py = fr.px(*pos)
    dx, dy = px - cx, py - cy
    t = min((w / 2 - 70) / abs(dx) if dx else 1e9, (h / 2 - 50) / abs(dy) if dy else 1e9)
    ax, ay = cx + dx * t, cy + dy * t
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    tip = (ax + ux * 22, ay + uy * 22)
    base = (ax - ux * 18, ay - uy * 18)
    p = (-uy, ux)
    d.polygon([tip, (base[0] + p[0] * 15, base[1] + p[1] * 15), (base[0] - p[0] * 15, base[1] - p[1] * 15)],
              fill=col + (255,), outline=(0, 0, 0, 255))
    tw = d.textlength(label, font=f)
    lx = min(max(ax - ux * 34 - tw / 2 - (tw / 2) * ux, 6), w - tw - 10)
    ly = min(max(ay - uy * 34 - 10 - 10 * uy, 6), h - 28)
    d.rectangle((lx - 4, ly - 2, lx + tw + 4, ly + 20), fill=(0, 0, 0, 175))
    d.text((lx, ly), label, font=f, fill=col + (255,))
    return (min(lx, ax - 24) - 6, min(ly, ay - 24) - 4, max(lx + tw, ax + 24) + 6, max(ly + 22, ay + 24) + 4)


def overlaps(a, b):
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


def pick(rects, cands):
    """First candidate rectangle that touches none of the label rectangles (else the last one)."""
    for c in cands:
        if not any(overlaps(c, r) for r in rects):
            return c
    return cands[-1]


def scale_bar(d, size, fr, f, rects=()):
    w, h = size
    for m in (1000, 500, 250, 100):
        if m * fr.s < w * 0.3:
            break
    L = m * fr.s
    bw = L + 28
    cands = [(w - bw - 4, h - 34, w - 4, h - 4), (4, h - 34, 4 + bw, h - 4), (w - bw - 4, 4, w - 4, 34)]
    r = pick(rects, cands)
    d.rectangle(r, fill=(0, 0, 0, 175))
    x0, y1 = r[0] + 14, r[3] - 8
    d.line((x0, y1, x0 + L, y1), fill='white', width=3)
    d.line((x0, y1 - 5, x0, y1 + 5), fill='white', width=3)
    d.line((x0 + L, y1 - 5, x0 + L, y1 + 5), fill='white', width=3)
    d.text((x0, y1 - 22), '%d m' % m, font=f, fill='white')
    return r


def legend(d, items, f, rects=(), size=None):
    wmax = max(d.textlength(t, font=f) for _, _, t in items)
    bw, bh = wmax + 46, 8 + 22 * len(items)
    w, h = size
    r = pick(rects, [(8, 8, 8 + bw, 8 + bh), (8, h - 8 - bh, 8 + bw, h - 8), (w - 8 - bw, 8, w - 8, 8 + bh)])
    d.rectangle(r, fill=(0, 0, 0, 190))
    for i, (kind, col, t) in enumerate(items):
        x, y = r[0] + 8, r[1] + 8 + 22 * i
        if kind == 'poly':
            d.rectangle((x, y + 2, x + 18, y + 14), outline=col, width=2)
        elif kind == 'tower':
            d.ellipse((x + 1, y, x + 17, y + 16), fill=col, outline='black')
        elif kind == 'arrow':
            d.polygon([(x, y + 14), (x + 18, y + 7), (x, y)], fill=col, outline='black')
        elif kind == 'circle':
            d.ellipse((x + 1, y, x + 17, y + 16), outline=col, width=3)
        d.text((x + 26, y), t, font=f, fill='white')
    return r


def draw_towers(d, fr, towers, f, r=15):
    for n, x, y in towers:
        px, py = fr.px(x, y)
        d.ellipse((px - r, py - r, px + r, py + r), fill=TOWER_COL + (255,), outline=(0, 0, 0, 255), width=2)
        tw = d.textlength(str(n), font=f)
        d.text((px - tw / 2, py - 9), str(n), font=f, fill='white')


def save(im, path, q=70):
    im.save(path, quality=q, optimize=True, progressive=True)


def build_map(name, tex_dir, out_dir):
    world, key, spawns = MAPS[name]
    mg = json.load(open(os.path.join(ROOT, 'assets/data/map-magnets-extents.json')))
    towers = [(r['tower'], r['x_m'], r['y_m']) for r in mg['magnets'][key]['rows']]
    pb = mg['extents'][key]['play_box_m']
    box = (pb['x_min'] - MARGIN_M, pb['x_max'] + MARGIN_M, pb['y_min'] - MARGIN_M, pb['y_max'] + MARGIN_M)
    regions = load_regions(world) if world in REGION_FILE else []
    img = Image.open(os.path.join(tex_dir, 'Wardogs/Content/UI/Tools/WorldCapture/Textures/%s/T_UI_%s_VT.png' % (world, world)))
    crop, s = crop_world(img, world, box)
    save(crop, os.path.join(out_dir, name + '-plain.jpg'), 55)
    fr = Frame(world, box, s)
    ov = Image.new('RGBA', crop.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    f, fs = font(17), font(15)
    for rn, pts in regions:
        tw = rn.upper().startswith('TOWER')
        d.polygon([fr.px(*p) for p in pts], outline=(255, 255, 255, 255) if tw else (255, 255, 255, 130),
                  width=3 if tw else 1, fill=TOWER_COL + (45,) if tw else None)
    items = []
    if regions:
        items.append(('poly', (255, 255, 255), 'Zone regions (named polygons)'))
    draw_towers(d, fr, towers, f)
    items.append(('tower', TOWER_COL, 'Hot Zone Magnet tower (number)'))
    rects = []
    cxm, cym = (box[0] + box[1]) / 2, (box[2] + box[3]) / 2
    for area, side in spawns:
        pos = spawn_pos(world, area)
        col = SIDE_COL[side]
        px, py = fr.px(*pos)
        if 0 <= px < crop.width and 0 <= py < crop.height:
            d.ellipse((px - 12, py - 12, px + 12, py + 12), fill=col + (255,), outline=(0, 0, 0, 255), width=2)
            d.text((px + 16, py - 9), '%s (%s)' % (area, side), font=f, fill=col + (255,))
        else:
            km = math.hypot(pos[0] - cxm, pos[1] - cym) / 1000.0
            rects.append(edge_arrow(d, crop.size, fr, pos, '%s (%s) %.1f km' % (area, side, km), col, fs))
    items.append(('arrow', (210, 210, 210), 'Spawn area direction (side name, distance)'))
    rects.append(scale_bar(d, crop.size, fr, fs, rects))
    legend(d, items, fs, rects, crop.size)
    save(Image.alpha_composite(crop.convert('RGBA'), ov).convert('RGB'), os.path.join(out_dir, name + '.jpg'))
    # overview: the whole minimap with the play box and the three spawn areas
    ow = 800
    ovw = img.convert('RGB').resize((ow, ow), Image.LANCZOS)
    od = ImageDraw.Draw(ovw, 'RGBA')
    def t(x, y):
        return (x - fr.b[0]) / (fr.b[1] - fr.b[0]) * ow, (y - fr.b[2]) / (fr.b[3] - fr.b[2]) * ow
    a, b = t(box[0], box[2]), t(box[1], box[3])
    od.rectangle((a[0], a[1], b[0], b[1]), outline=(255, 255, 255, 255), width=3)
    od.text((a[0], max(0, a[1] - 20)), 'play box', font=fs, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
    for area, side in spawns:
        x, y = t(*spawn_pos(world, area))
        od.ellipse((x - 9, y - 9, x + 9, y + 9), fill=SIDE_COL[side] + (255,), outline=(0, 0, 0, 255), width=2)
        od.text((x + 12, y - 8), '%s (%s)' % (area, side), font=fs, fill=SIDE_COL[side] + (255,), stroke_width=2, stroke_fill=(0, 0, 0, 255))
    ovw.save(os.path.join(out_dir, name + '-overview.jpg'), quality=68, optimize=True, progressive=True)


def build_jutari(tex_dir, out_dir):
    world = 'Kavkazi'
    zx, zy = -6726.88, -11170.98  # Sniper Showdown zone object (round 65 item 2c: cm -672,688 / -1,117,098)
    half = 750
    box = (zx - half, zx + half, zy - half, zy + half)
    img = Image.open(os.path.join(tex_dir, 'Wardogs/Content/UI/Tools/WorldCapture/Textures/Kavkazi/T_UI_Kavkazi_VT.png'))
    crop, s = crop_world(img, world, box)
    save(crop, os.path.join(out_dir, 'jutari-plain.jpg'), 55)
    fr = Frame(world, box, s)
    ov = Image.new('RGBA', crop.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    fs = font(15)
    cx, cy = fr.px(zx, zy)
    for diam, col in ((350, (255, 255, 255, 255)), (75, TOWER_COL + (255,))):
        r = diam / 2 * s
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=3)
    rects = [scale_bar(d, crop.size, fr, fs)]
    legend(d, [('circle', (255, 255, 255), 'Control Zone, 350 m across'), ('circle', TOWER_COL, 'Hot Zone, 75 m across')], fs, rects, crop.size)
    save(Image.alpha_composite(crop.convert('RGBA'), ov).convert('RGB'), os.path.join(out_dir, 'jutari.jpg'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tex-dir', default='E:/r78/mm_tex')
    ap.add_argument('--out', default=os.path.join(ROOT, 'assets/img/maps'))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for n in MAPS:
        build_map(n, a.tex_dir, a.out)
        print('built', n)
    build_jutari(a.tex_dir, a.out)
    print('built jutari')


if __name__ == '__main__':
    sys.exit(main())
