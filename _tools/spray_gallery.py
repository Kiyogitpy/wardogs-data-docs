"""Spray (recoil) pattern gallery: one SVG per weapon plus the gallery page.

Reads assets/data/spray-patterns.json and writes:

    assets/images/spray/<weaponId>.svg    one chart per weapon (both seasons on the same axes)
    game-features/Wardogs_SprayPatterns_v1.md    the gallery page (whole file is generated)

    python -I _tools/spray_gallery.py          # dry run: print what would be written
    python -I _tools/spray_gallery.py --write  # write the SVGs and the page

Chart: x = yaw in degrees (right +), y = pitch in degrees (up +). The cumulative spray path is drawn as
numbered dots joined by a line; the p10 to p90 band is a translucent area. Season 1 is blue, dashed, with
round markers; Season 2 is green, solid, with square markers, so the two read apart without colour.
Each SVG carries its own light and dark palette (prefers-color-scheme inside the file), so it reads the same
whether it is inlined or used as an image.
"""
import html
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "assets", "data", "spray-patterns.json")
SVG_DIR = os.path.join(ROOT, "assets", "images", "spray")
PAGE = os.path.join(ROOT, "game-features", "Wardogs_SprayPatterns_v1.md")

W, H = 640, 372
PX0, PX1, PY0, PY1 = 70, 620, 64, 330
CLIMB_SHOTS = (10, 20, 30)
CLASS_TITLES = {
    "AR": "Assault rifles", "DMR": "Marksman rifles", "LMG": "Light machine guns", "SMG": "Submachine guns",
    "Pistol": "Pistols", "Shotgun": "Shotguns", "Sniper": "Sniper rifles", "Bow": "Bows",
    "Launcher": "Launchers", "Unclassified": "Unclassified",
}
STYLE = """<style>
.bg{fill:#ffffff;stroke:#8a8a8a;stroke-width:1}
.plot{fill:none;stroke:#8a8a8a;stroke-width:1}
.grid{stroke:#e2e2e2;stroke-width:1}
.axis{stroke:#444;stroke-width:1.2}
.ref{stroke:#9a9a9a;stroke-width:1;stroke-dasharray:2 3}
.tick{font:11px sans-serif;fill:#333}
.lbl{font:12px sans-serif;fill:#333}
.ttl{font:600 15px sans-serif;fill:#111}
.num1{font:10px sans-serif;fill:#2b6cb0}
.num2{font:10px sans-serif;fill:#2f855a}
.note{font:13px sans-serif;fill:#555}
.mk1{stroke:#2b6cb0;fill:#2b6cb0}
.mk2{stroke:#2f855a;fill:#2f855a}
.ln1{fill:none;stroke:#2b6cb0;stroke-width:2;stroke-dasharray:7 4}
.ln2{fill:none;stroke:#2f855a;stroke-width:2}
.band1{fill:#2b6cb0;fill-opacity:.18;stroke:none}
.band2{fill:#2f855a;fill-opacity:.18;stroke:none}
@media (prefers-color-scheme: dark){
.bg{fill:#1c1f24;stroke:#6b7280}
.plot{stroke:#6b7280}
.grid{stroke:#333842}
.axis{stroke:#c9ced6}
.ref{stroke:#7b8190}
.tick,.lbl{fill:#d7dbe2}
.ttl{fill:#f1f3f6}
.note{fill:#aab1bd}
.num1{fill:#63a6e6}
.num2{fill:#68c48f}
.mk1{stroke:#63a6e6;fill:#63a6e6}
.mk2{stroke:#68c48f;fill:#68c48f}
.ln1{stroke:#63a6e6}
.ln2{stroke:#68c48f}
.band1{fill:#63a6e6;fill-opacity:.22}
.band2{fill:#68c48f;fill-opacity:.22}
}
</style>"""


def esc(s):
    return html.escape(str(s), quote=True)


def fmt(v):
    if abs(v) < 5e-10:
        return "0"
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s


def nice_step(span, target=6):
    raw = span / target
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if m * mag >= raw:
            return m * mag
    return 10 * mag


def axis_range(values):
    lo, hi = min(values + [0.0]), max(values + [0.0])
    if hi - lo < 1e-9:
        hi = lo + 1.0
    pad = 0.08 * (hi - lo)
    lo, hi = lo - pad, hi + pad
    step = nice_step(hi - lo)
    first = math.ceil(lo / step - 1e-9) * step
    ticks = []
    t = first
    while t <= hi + 1e-9:
        ticks.append(round(t, 10))
        t += step
    return lo, hi, ticks


def season_points(season):
    """(path, band_lower, band_upper) as lists of (x, y); empty when the season has no path."""
    if not season:
        return [], [], []
    path = [(p["x"], p["y"]) for p in season.get("expectedPath") or []]
    band = season.get("band") or {}
    lo = [(p["x"], p["y"]) for p in band.get("p10") or []]
    hi = [(p["x"], p["y"]) for p in band.get("p90") or []]
    return path, lo, hi


def svg_for(weapon):
    seasons = [("Season 1", "1", weapon["seasons"].get("s1")), ("Season 2", "2", weapon["seasons"].get("s2"))]
    data = [(label, key, season_points(s)) for label, key, s in seasons if s]
    xs, ys = [], []
    for _, _, (path, lo, hi) in data:
        for x, y in path + lo + hi:
            xs.append(x)
            ys.append(y)
    has_path = any(path for _, _, (path, _, _) in data)
    if not xs:
        xs, ys = [0.0], [0.0]
    xlo, xhi, xt = axis_range(xs)
    ylo, yhi, yt = axis_range(ys)

    def sx(x):
        return PX0 + (x - xlo) / (xhi - xlo) * (PX1 - PX0)

    def sy(y):
        return PY1 - (y - ylo) / (yhi - ylo) * (PY1 - PY0)

    name = weapon["name"]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-labelledby="t d">',
         f'<title id="t">{esc(name)} spray pattern</title>',
         f'<desc id="d">Cumulative pitch and yaw of each shot in the spray pattern. '
         f'{"Season 1 is blue dashed; Season 2 is green solid." if any(k == "1" for _, k, _ in data) else "Season 2 only; no Season 1 data."}</desc>',
         STYLE,
         f'<rect class="bg" x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6"/>',
         f'<text class="ttl" x="{PX0}" y="26">{esc(name)}</text>']

    # Legend row (season shape and colour).
    lx = PX0
    for label, key, _ in data:
        o.append(f'<line class="ln{key}" x1="{lx}" y1="46" x2="{lx + 26}" y2="46"/>')
        if key == "1":
            o.append(f'<circle class="mk1" cx="{lx + 13}" cy="46" r="3.2"/>')
        else:
            o.append(f'<rect class="mk2" x="{lx + 10}" y="43" width="6" height="6"/>')
        o.append(f'<text class="lbl" x="{lx + 34}" y="50">{label}</text>')
        lx += 130

    # Grid and ticks.
    for t in xt:
        o.append(f'<line class="grid" x1="{sx(t):.2f}" y1="{PY0}" x2="{sx(t):.2f}" y2="{PY1}"/>')
        o.append(f'<text class="tick" x="{sx(t):.2f}" y="{PY1 + 15}" text-anchor="middle">{fmt(t)}</text>')
    for t in yt:
        o.append(f'<line class="grid" x1="{PX0}" y1="{sy(t):.2f}" x2="{PX1}" y2="{sy(t):.2f}"/>')
        o.append(f'<text class="tick" x="{PX0 - 8}" y="{sy(t) + 4:.2f}" text-anchor="end">{fmt(t)}</text>')
    o.append(f'<rect class="plot" x="{PX0}" y="{PY0}" width="{PX1 - PX0}" height="{PY1 - PY0}"/>')
    if xlo < 0 < xhi:
        o.append(f'<line class="ref" x1="{sx(0):.2f}" y1="{PY0}" x2="{sx(0):.2f}" y2="{PY1}"/>')
    if ylo < 0 < yhi:
        o.append(f'<line class="ref" x1="{PX0}" y1="{sy(0):.2f}" x2="{PX1}" y2="{sy(0):.2f}"/>')
    o.append(f'<text class="lbl" x="{(PX0 + PX1) / 2}" y="{PY1 + 34}" text-anchor="middle">'
             f'Yaw (degrees, right +)</text>')
    o.append(f'<text class="lbl" transform="translate(18 {(PY0 + PY1) / 2}) rotate(-90)" text-anchor="middle">'
             f'Pitch (degrees, up +)</text>')

    if not has_path:
        o.append(f'<text class="note" x="{(PX0 + PX1) / 2}" y="{(PY0 + PY1) / 2}" text-anchor="middle">'
                 f'No recoil pattern in the exported data</text>')

    # Bands first (under the paths), then paths, then dots and numbers.
    for label, key, (path, lo, hi) in data:
        if lo and hi and len(lo) == len(hi):
            pts = lo + list(reversed(hi))
            d = " ".join(f"{sx(x):.2f},{sy(y):.2f}" for x, y in pts)
            o.append(f'<polygon class="band{key}" points="{d}"/>')
    for label, key, (path, lo, hi) in data:
        if not path:
            continue
        d = " ".join(f"{sx(x):.2f},{sy(y):.2f}" for x, y in path)
        o.append(f'<polyline class="ln{key}" points="{d}"/>')
        n = len(path)
        for i, (x, y) in enumerate(path, 1):
            cx, cy = sx(x), sy(y)
            if key == "1":
                o.append(f'<circle class="mk1" cx="{cx:.2f}" cy="{cy:.2f}" r="3.2"/>')
            else:
                o.append(f'<rect class="mk2" x="{cx - 3:.2f}" y="{cy - 3:.2f}" width="6" height="6"/>')
            if i == 1 or i % 5 == 0 or i == n:
                dy = -6 if key == "1" else 12
                o.append(f'<text class="num{key}" x="{cx + 5:.2f}" y="{cy + dy:.2f}">{i}</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def pair(a, b, f=fmt):
    return f"{'—' if a is None else f(a)} -> {'—' if b is None else f(b)}"


def season_val(weapon, key):
    return weapon["seasons"].get(key) or None


def climb(season, k):
    if not season:
        return None
    path = season.get("expectedPath") or []
    if not path:
        return None
    if len(path) < k:
        return "n/a"
    return path[k - 1]["y"]


def row(weapon):
    s1, s2 = season_val(weapon, "s1"), season_val(weapon, "s2")
    shots_cell = pair(len(s1.get("pattern") or []) if s1 else None,
                      len(s2.get("pattern") or []) if s2 else None, lambda v: str(v) if v else "none")
    parts = []
    for k in CLIMB_SHOTS:
        a = climb(s1, k)
        b = climb(s2, k)
        f = lambda v: v if isinstance(v, str) else fmt(v)
        parts.append(f"{f(a) if a is not None else '—'} -> {f(b) if b is not None else '—'}")
    climb_cell = " / ".join(parts)
    rpm_cell = pair(s1 and s1.get("rpm"), s2 and s2.get("rpm"), lambda v: str(int(v)) if float(v).is_integer() else fmt(v))
    rt = pair(s1 and s1.get("recoilPatternResetTime_s"), s2 and s2.get("recoilPatternResetTime_s"),
              lambda v: f"{fmt(v)} s")
    name = weapon["name"].replace("|", "\\|")
    img = f"![{name} spray pattern](../assets/images/spray/{weapon['id']}.svg)"
    cls = (weapon.get("class") or "Unclassified").replace("|", "\\|")
    return f"| {name} | {cls} | {shots_cell} | {climb_cell} | {rpm_cell} | {rt} | {img} |"


HEADER = ["| Name | Class | Shots in pattern | Vertical climb after 10 / 20 / 30 shots, degrees (S1 -> S2) "
          "| RPM (S1 -> S2) | Reset time (S1 -> S2) | Pattern image |",
          "|---|---|---:|---|---:|---:|---|"]


def table(weapons):
    return HEADER + [row(w) for w in weapons]


def page(data):
    weapons = data["weapons"]
    inf = [w for w in weapons if w.get("category") == "infantry"]
    other = [w for w in weapons if w.get("category") != "infantry"]
    by_class = {}
    for w in inf:
        by_class.setdefault(w.get("class") or "Unclassified", []).append(w)
    status = (data.get("meta") or {}).get("status")
    o = [
        "---",
        'title: "Spray Patterns Gallery"',
        'redirect_from: ["/Wardogs_SprayPatterns_v1.html", "/Wardogs_SprayPatterns_v1"]',
        'parent: "Weapons & Ammo"',
        'description: "Recoil spray pattern of every weapon, Season 1 against Season 2: the climb after 10, 20 and 30 shots, fire rate, reset time and a picture of each pattern"',
        "---",
        "",
        "# Spray Patterns Gallery",
        "",
        f"Every weapon's recoil spray pattern, one picture each, with Season 1 and Season 2 on the same axes. "
        f"{len(inf)} infantry weapons are in the tables below by class; {len(other)} vehicle, stationary and test "
        f"entries are in the collapsed section at the end.",
        "",
        "The interactive viewer is at [Spray Pattern Viewer](../pipelines/spray-viewer.html).",
        "",
    ]
    if status and status != "final":
        o += [f"> **Data status:** {status.lower()}. The Season 1 columns and some values will change when the "
              "final export is merged.", ""]
    o += [
        "## Legend",
        "",
        "- **Blue, dashed, round markers** = Season 1. **Green, solid, square markers** = Season 2.",
        "- **Numbers on the path** = shot number (1, every 5th shot, and the last shot).",
        "- **Shaded band** = the p10 to p90 range of the simulated spray (the area where most shots land).",
        "- **x axis** = yaw in degrees, right is +. **y axis** = pitch in degrees, up is +. "
        "Each chart has its own scale, so read the tick labels.",
        "- **Vertical climb** = how far the aim has risen after that many shots, in degrees.",
        "- **RPM** = rounds per minute. **Reset time** = seconds of no fire before the pattern starts again.",
        "- A dash (—) means the value is not in the exported data for that season.",
        "",
    ]
    for cls in sorted(by_class, key=lambda c: (c not in CLASS_TITLES, c)):
        ws = sorted(by_class[cls], key=lambda w: w["name"].lower())
        o += [f"## {CLASS_TITLES.get(cls, cls)}", ""] + table(ws) + [""]
    o += [
        '<details markdown="1">',
        "<summary>Vehicle, stationary and test weapons (%d)</summary>" % len(other),
        "",
    ] + table(sorted(other, key=lambda w: (w.get("class") or "", w["name"].lower()))) + ["", "</details>", ""]
    return "\n".join(o)


def main():
    args = sys.argv[1:]
    write = "--write" in args
    with open(DATA, encoding="utf-8") as fh:
        data = json.load(fh)
    weapons = data["weapons"]
    ids = [w["id"] for w in weapons]
    if len(set(ids)) != len(ids):
        raise SystemExit("duplicate weapon ids in spray-patterns.json")
    pages = page(data)
    svgs = {w["id"]: svg_for(w) for w in weapons}
    if not write:
        print(f"dry run: {len(svgs)} SVGs to {os.path.relpath(SVG_DIR, ROOT)}/, page {os.path.relpath(PAGE, ROOT)} "
              f"({len(pages.splitlines())} lines). Pass --write to write.")
        return 0
    os.makedirs(SVG_DIR, exist_ok=True)
    for wid, text in svgs.items():
        with open(os.path.join(SVG_DIR, f"{wid}.svg"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    with open(PAGE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(pages)
    print(f"wrote {len(svgs)} SVGs to {os.path.relpath(SVG_DIR, ROOT)}/ and {os.path.relpath(PAGE, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
