"""Checks for the object viewer (pipelines/object-viewer.md).

    python -I _tools/object_models_check.py            # data and GLBs
    python -I _tools/object_models_check.py --browser  # also drive the page in Chromium (Playwright, network for model-viewer)

Data and GLBs: every object's GLB exists and holds no images, textures or samplers; its materials are exactly the
materials the data names (stage pieces "S<n>|<mesh>", props their body names); every node has a mesh; the data's
stage-piece tables match data/ (object_models.py --check); no GLB is over the size budget.
"""
import http.server
import json
import os
import re
import struct
import sys
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
BUDGET = 150_000


def glb_json(path):
    with open(path, "rb") as fh:
        magic, version, _ = struct.unpack("<III", fh.read(12))
        assert magic == 0x46546C67 and version == 2, path
        size, kind = struct.unpack("<II", fh.read(8))
        assert kind == 0x4E4F534A
        return json.loads(fh.read(size))


def check_data():
    doc = json.load(open(os.path.join(ROOT, "assets", "data", "object-collision.json"), encoding="utf-8"))
    errors, files = [], set()
    for o in doc["objects"]:
        if not o["glb"]:
            continue
        path = os.path.join(ROOT, o["glb"])
        files.add(os.path.basename(path))
        if not os.path.exists(path):
            errors.append(f"{o['id']}: {o['glb']} missing")
            continue
        if os.path.getsize(path) > BUDGET:
            errors.append(f"{o['id']}: {os.path.getsize(path)} bytes, over the budget")
        g = glb_json(path)
        for key in ("images", "textures", "samplers"):
            if g.get(key):
                errors.append(f"{o['id']}: GLB has {key}")
        for m in g.get("materials", []):
            pbr = m.get("pbrMetallicRoughness", {})
            if set(m) - {"name", "pbrMetallicRoughness"} or set(pbr) - {"baseColorFactor", "metallicFactor", "roughnessFactor"}:
                errors.append(f"{o['id']}: material {m.get('name')} has more than a colour")
        have = {m["name"] for m in g["materials"]}
        want = {p["material"] for s in o["stages"] for p in s["pieces"] if p.get("material") and p["status"] == "ok"}
        if have != want:
            errors.append(f"{o['id']}: materials differ: {sorted(have ^ want)[:4]}")
        for n in g["nodes"][1:]:
            if "mesh" not in n:
                errors.append(f"{o['id']}: node {n.get('name')} has no mesh")
    on_disk = {f for f in os.listdir(os.path.join(ROOT, "assets", "models", "objects")) if f.endswith(".glb")}
    if on_disk != files:
        errors.append(f"GLBs on disk and in the data differ: {sorted(on_disk ^ files)}")
    return doc, errors


def check_browser(doc):
    from playwright.sync_api import sync_playwright
    page_md = open(os.path.join(ROOT, "pipelines", "object-viewer.md"), encoding="utf-8").read()
    body = page_md.split("---", 2)[2]
    body = re.sub(r"\{\{\s*'([^']*)'\s*\|\s*relative_url\s*\}\}", r"\1", body)
    body = re.sub(r"\{\{[^}]*\}\}", "0", body)
    body = body.replace("poster=\"/assets/images/vehicle-viewer-poster.svg\"", "")
    html = ("<!doctype html><meta charset=utf-8><style>.vv-box{height:420px;position:relative}.vv-model{width:100%;height:100%}"
            "[hidden]{display:none!important}</style>" + body)
    tmp = os.path.join(ROOT, "_objcheck.html")
    open(tmp, "w", encoding="utf-8").write(html)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=ROOT, **k)

        def log_message(self, *a):
            pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    errors = []
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(channel=os.environ.get("PW_CHANNEL") or None, args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
            pg = b.new_page()
            logs = []
            pg.on("pageerror", lambda e: logs.append(str(e)))
            pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/_objcheck.html#sandbagwall/3")
            pg.wait_for_function("document.getElementById('ov-object').options.length > 5", timeout=20000)
            n = pg.evaluate("document.getElementById('ov-object').options.length")
            if n != len(doc["objects"]):
                errors.append(f"object list has {n} options, data has {len(doc['objects'])}")
            if pg.evaluate("document.getElementById('ov-object').value") != "sandbagwall":
                errors.append("hash did not select the sandbag wall")
            for o in doc["objects"]:
                pg.select_option("#ov-object", o["id"])
                pieces = pg.evaluate("document.querySelectorAll('#ov-slots li').length")
                if pieces != len(o["stages"][-1]["pieces"]):
                    errors.append(f"{o['id']}: {pieces} list entries")
            pg.select_option("#ov-object", "sandbagwall")
            pg.wait_for_function("document.getElementById('ov-model').model", timeout=60000)
            pg.click("#ov-slots li button")
            if "Static mesh" not in pg.inner_text("#ov-panel-body"):
                errors.append("selecting a piece did not show its detail")
            errors += [f"page error: {m}" for m in logs]
            b.close()
    finally:
        srv.shutdown()
        os.remove(tmp)
    return errors


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    doc, errors = check_data()
    if "--browser" in sys.argv:
        errors += check_browser(doc)
    for e in errors:
        print("FAIL", e)
    if errors:
        sys.exit(1)
    n = sum(1 for o in doc["objects"] if o["glb"])
    print(f"object viewer: {len(doc['objects'])} objects, {n} GLBs, no images or textures"
          + (", browser check passed" if "--browser" in sys.argv else ""))


if __name__ == "__main__":
    main()
