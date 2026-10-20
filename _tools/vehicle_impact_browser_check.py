"""Exercise local impact-viewer assets using installed Playwright and Chromium.

The harness uses the deployed theme CSS, plus the new rules as native nested CSS.
It does not replace a Jekyll/Sass build. Screenshots go to the supplied directory.
"""
import argparse
import json
from pathlib import Path
import re
import urllib.request
import markdown
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://kiyogitpy.github.io/wardogs-data-docs"
MAIN_SECTION = "Attribute.Gameplay.Health"


def section_label(section):
    return "Main health" if section == MAIN_SECTION else section.removeprefix(MAIN_SECTION + ".")


def ui_number(value):
    magnitude = abs(value)
    if magnitude >= 100:
        rendered = f"{value:.0f}"
    elif magnitude >= 10:
        rendered = f"{value:.1f}"
    elif magnitude >= 1:
        rendered = f"{value:.2f}"
    else:
        rendered = f"{value:.3g}"
    return rendered.rstrip("0").rstrip(".") if "." in rendered else rendered


def expected_routing(slot):
    if slot.get("section") == MAIN_SECTION:
        return ["is the main health: the vehicle is destroyed when it reaches 0"]
    routing = slot.get("routing") or {}
    lines = []
    to_main = False

    def target(tag):
        return "the main health" if tag == MAIN_SECTION else "the " + section_label(tag)

    for entry in routing.get("pre", []):
        to_main |= entry["to"] == MAIN_SECTION
        prefix = "once destroyed, passes " if entry.get("only_when_depleted") else "passes "
        lines.append(prefix + ui_number(entry["scalar"] * 100) + "% of each hit to " + target(entry["to"]) + " first")
    for entry in routing.get("simultaneous", []):
        to_main |= entry["to"] == MAIN_SECTION
        suffix = " once destroyed" if entry.get("only_when_depleted") else ""
        lines.append("copies " + ui_number(entry["scalar"] * 100) + "% of the damage it absorbs to " + target(entry["to"]) + suffix)
    for entry in routing.get("post", []):
        to_main |= entry["to"] == MAIN_SECTION
        if entry.get("only_when_depleted"):
            text = "passes " + ui_number(entry["scalar"] * 100) + "% of further damage to " + target(entry["to"]) + " once destroyed"
        else:
            text = "passes " + ui_number(entry["scalar"] * 100) + "% of the damage it doesn't absorb to " + target(entry["to"])
        lines.append(text)
    if not lines:
        lines.append("never passes damage to the main health")
    elif not to_main:
        lines.append("does not pass damage to the main health directly")
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--no-screenshots", action="store_true")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    vehicle_data = json.loads((ROOT / "assets/data/vehicle-hitboxes.json").read_text(encoding="utf-8"))
    viewer_js = (ROOT / "assets/js/vehicle-viewer.js").read_text(encoding="utf-8")
    palette = dict(re.findall(r'"(Attribute\.Gameplay\.Health(?:\.[A-Za-z0-9]+)*)": "(#[0-9a-fA-F]{6})"', viewer_js))
    all_sections = {section for vehicle in vehicle_data["vehicles"] for section in vehicle["sections"]}
    assert all_sections <= palette.keys(), f"Unmapped health sections: {sorted(all_sections - palette.keys())}"
    assert len({palette[section] for section in all_sections}) == len(all_sections), "Health section colors are not unique"
    deployed = urllib.request.urlopen(SITE + "/pipelines/vehicle-viewer.html").read().decode()
    styles = re.findall(r'<link[^>]+href="([^"]+\.css[^\"]*)"', deployed)
    page = (ROOT / "pipelines/vehicle-viewer.md").read_text(encoding="utf-8")
    content = page[page.index('<div class="vv"'):page.index("## How the models are built")]
    content = re.sub(r"{{\s*'([^']+)'\s*\|\s*relative_url\s*}}", lambda m: "/wardogs-data-docs" + m[1], content)
    content = re.sub(r"{{.*?}}", "local", content)
    variables = dict(re.findall(r"\$([\w-]+):\s*([^;]+);", (ROOT / "_sass/custom/custom.scss").read_text()))
    css = (ROOT / "_sass/custom/vehicle-viewer.scss").read_text()
    css = css[css.index(".vv-is-placing"):css.index(".vv-status {")]
    css = re.sub(r"\$([\w-]+)", lambda m: variables[m[1]], css)
    content = markdown.markdown(content, extensions=["extra"])
    html = ('<!doctype html><html class="js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            + ''.join(f'<link rel="stylesheet" href="{href}">' for href in styles)
            + '<style>body{margin:0;background:#101014}.main-content{max-width:1400px;margin:auto;padding:20px}'
            + css + '</style></head><body><main class="main-content"><h1>Vehicle Hitbox Viewer</h1>'
            + content + '</main></body></html>')
    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", args=["--enable-unsafe-swiftshader", "--use-angle=swiftshader"])
        context = browser.new_context(viewport={"width": 1440, "height": 1100}, ignore_https_errors=True)
        def route(request):
            url = request.request.url.split("?", 1)[0]
            relative = url.removeprefix(SITE + "/")
            if relative == "pipelines/vehicle-viewer.html":
                request.fulfill(body=html, content_type="text/html")
            elif relative.startswith(("assets/js/", "assets/data/", "assets/models/", "assets/images/")):
                target = (ROOT / relative).resolve()
                if target.is_relative_to(ROOT) and target.is_file():
                    types = {".js": "text/javascript", ".json": "application/json", ".glb": "model/gltf-binary", ".svg": "image/svg+xml"}
                    request.fulfill(path=target, content_type=types.get(target.suffix, "application/octet-stream"))
                else:
                    request.continue_()
            else:
                request.continue_()
        context.route(SITE + "/**", route)
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(SITE + "/pipelines/vehicle-viewer.html", wait_until="networkidle", timeout=60000)
        page.wait_for_function("document.querySelector('#vv-model').loaded === true", timeout=45000)
        assert page.locator("#vv-model").evaluate("e => !e.dispatchEvent(new MouseEvent('mousedown',{button:1,bubbles:true,cancelable:true}))"), "Middle-button autoscroll was not cancelled"
        assert page.locator("body").evaluate("e => e.dispatchEvent(new MouseEvent('mousedown',{button:1,bubbles:true,cancelable:true}))"), "Middle-button handling escaped the viewer"
        page.select_option("#vv-caliber", "Item.Caliber.84mm")
        page.wait_for_function("!document.querySelector('#vv-placeGround').disabled", timeout=20000)
        page.fill("#vv-impactX", "1")
        page.fill("#vv-impactZ", "1")
        page.click("#vv-placeGround")
        summary = page.locator("#vv-impactSummary")
        assert "Splash" in summary.inner_text() and "Reference-pose estimate" in summary.inner_text()
        assert page.locator("#vv-impactOverlay path").count() >= 3
        assert page.locator("#vv-impactOverlay").is_visible(), "Blast overlay is hidden"
        first = summary.inner_text()
        page.click("#vv-placeGround")
        assert summary.inner_text() == first, "Repeated placement accumulated health"
        # The public hotspot projection supplies a reliable screen location on the displayed mesh.
        page.locator("#vv-model").scroll_into_view_if_needed()
        hit = page.evaluate("""() => { const m=document.querySelector('#vv-model'), r=m.getBoundingClientRect();
          for(const p of m.querySelectorAll('.vv-hotspot')) { const h=m.queryHotspot(p.slot);
            if(h && h.canvasPosition.z<1) { const q=h.canvasPosition;
              if(m.positionAndNormalFromPoint(r.left+q.x,r.top+q.y)) return {x:q.x,y:q.y}; }} return null; }""")
        assert hit, "No displayed surface point found"
        rect = page.locator("#vv-model").bounding_box()
        page.mouse.click(rect["x"] + hit["x"], rect["y"] + hit["y"])
        assert summary.inner_text().startswith("Direct hit"), summary.inner_text()
        if not args.no_screenshots:
            page.screenshot(path=args.out / "desktop.png", full_page=True)
        # A background click must select the ground plane rather than require numeric placement.
        background = page.locator("#vv-model").evaluate("""m => { const r=m.getBoundingClientRect();
          for(const x of [.08,.92]) for(const y of [.9,.8]) {
            const px=r.left+x*r.width, py=r.top+y*r.height;
            if(!m.positionAndNormalFromPoint(px,py)) return {x:px,y:py}; } return null; }""")
        assert background, "No ground-placement screen point found"
        page.mouse.click(background["x"], background["y"])
        assert summary.inner_text().startswith("Splash"), "Background click did not place splash"
        page.select_option("#vv-caliber", "Actor.c4")
        page.wait_for_function("!document.querySelector('#vv-placeGround').disabled")
        page.click("#vv-placeGround")
        assert "Splash" in summary.inner_text()
        other = page.locator("#vv-vehicle").evaluate("e => Array.from(e.options).find(o => o.value!==e.value).value")
        page.select_option("#vv-vehicle", other)
        assert "Place an impact" in summary.inner_text(), "Vehicle changes retained the old shot"
        page.set_viewport_size({"width": 360, "height": 1000})
        page.wait_for_function("document.querySelector('#vv-model').loaded === true")
        page.wait_for_function("!document.querySelector('#vv-placeGround').disabled")
        page.click("#vv-placeGround")
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), "Horizontal overflow at 360px"
        if not args.no_screenshots:
            page.screenshot(path=args.out / "mobile.png", full_page=True)
        page.click("#vv-clearImpact")
        assert "Place an impact" in summary.inner_text()
        page.select_option("#vv-caliber", "Item.Caliber.556mm")
        assert page.locator("#vv-impactControls").is_hidden()
        assert page.locator("#vv-blastMode").count() == 0

        # The reviewed front-surface MAAWS hit also exercises health routing into a hidden FuelTank.
        gepard = next(v for v in vehicle_data["vehicles"] if v["id"] == "land-tracked-tnk-01-antiair")
        gepard_model = gepard["models"][0]["path"]
        page.select_option("#vv-vehicle", gepard["id"])
        page.select_option("#vv-caliber", "Item.Caliber.84mm")
        page.wait_for_function("(path) => { const m=document.querySelector('#vv-model'); return m.loaded && m.getAttribute('src') && m.getAttribute('src').endsWith(path); }",
                               arg=gepard_model, timeout=45000)
        page.wait_for_function("!document.querySelector('#vv-placeGround').disabled", timeout=20000)
        front = page.evaluate("""async () => {
          const base=document.querySelector('#vv').dataset.base;
          const buffer=await (await fetch(base+'assets/models/vehicles/land-tracked-tnk-01-antiair.glb')).arrayBuffer();
          const geometry=await VehicleImpactGeometry.load(buffer, window.MeshoptDecoder);
          const hit=geometry.ray([0,1,8],[0,0,-1]);
          return hit && {position:Array.from(hit.position), material:hit.material.name};
        }""")
        assert front and front["material"] == "CC_MainBody", front
        projection = page.evaluate("""async (position) => {
          const m=document.querySelector('#vv-model'), b=document.createElement('button');
          b.type='button'; b.slot='hotspot-impact-check'; b.dataset.position=position.join(' ');
          b.dataset.normal='0 0 1'; b.dataset.visibilityAttribute='visible';
          b.style.cssText='width:24px;height:24px;padding:0;border:0;opacity:.01'; m.appendChild(b);
          await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
          const h=m.queryHotspot(b.slot); return h && h.canvasPosition;
        }""", front["position"])
        assert projection and projection["z"] < 1, f"Gepard front point is not visible: {projection}"
        rect = page.locator("#vv-model").bounding_box()
        page.mouse.click(rect["x"] + projection["x"], rect["y"] + projection["y"])
        assert summary.inner_text().startswith("Direct hit"), summary.inner_text()
        facts = dict(zip(page.locator("#vv-impactSummary dt").all_text_contents(),
                         page.locator("#vv-impactSummary dd").all_text_contents()))
        assert "using authored damage-query sockets" in summary.inner_text()
        assert "Some contacts are reached from an offset blast trace" in summary.text_content()
        assert facts.get("Damage applications", "").startswith("1 applied; 4 repeat contacts skipped"), facts
        # The UI rounds values >= 100 to whole damage; the numerical fixture check retains 267.9.
        assert facts.get("Main health damage") == "268", facts
        fuel = next((line for line in page.locator("#vv-impactSummary li").all_text_contents() if line.startswith("FuelTank:")), "")
        assert "14.1 damage routed from Main health" in fuel, fuel

        # All three SPW radar assemblies use authored bounds rather than exposed CC corners.
        page.set_viewport_size({"width": 1440, "height": 1100})
        spw_models = 0
        for vehicle in vehicle_data["vehicles"]:
            if not vehicle["id"].startswith("land-tracked-leopard-spawn-"):
                continue
            page.select_option("#vv-vehicle", vehicle["id"])
            for index, model in enumerate(vehicle["models"]):
                if len(vehicle["models"]) > 1:
                    page.select_option("#vv-variant", str(index))
                page.wait_for_function("path => { const m=document.querySelector('#vv-model'); return m.loaded && m.getAttribute('src').endsWith(path); }",
                                       arg=model["path"], timeout=45000)
                page.wait_for_function("!document.querySelector('#vv-placeGround').disabled", timeout=20000)
                page.locator("#vv-model").scroll_into_view_if_needed()
                projection = page.evaluate("""async path => {
                  const m=document.querySelector('#vv-model'), base=document.querySelector('#vv').dataset.base;
                  const buffer=await (await fetch(base+path)).arrayBuffer();
                  const g=await VehicleImpactGeometry.load(buffer, window.MeshoptDecoder);
                  const hit=g.ray([0,1,g.bounds.max[2]+2],[0,0,-1]);
                  if(!hit || hit.material.name!=='CC_MainBody') return null;
                  const b=document.createElement('button'); b.type='button'; b.slot='hotspot-spw-check';
                  b.dataset.position=hit.position.join(' '); b.dataset.normal='0 0 1';
                  b.dataset.visibilityAttribute='visible';
                  b.style.cssText='width:24px;height:24px;padding:0;border:0;opacity:.01'; m.appendChild(b);
                  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
                  const h=m.queryHotspot(b.slot); return h && h.canvasPosition;
                }""", model["path"])
                assert projection and projection["z"] < 1, (model["path"], projection)
                rect = page.locator("#vv-model").bounding_box()
                page.mouse.click(rect["x"] + projection["x"], rect["y"] + projection["y"])
                assert summary.inner_text().startswith("Direct hit"), summary.inner_text()
                assert "using authored component bounds" in summary.inner_text()
                assert "Detonation is 12.7 cm back" in summary.inner_text()
                assert "Impact point (m):" in summary.text_content() and "Detonation centre (m):" in summary.text_content()
                assert page.locator("#vv-impactOverlay .vv-blast-label").text_content() == "Detonation"
                facts = dict(zip(page.locator("#vv-impactSummary dt").all_text_contents(),
                                 page.locator("#vv-impactSummary dd").all_text_contents()))
                assert facts.get("Damage applications", "").startswith("1 applied;"), (model["path"], facts)
                assert facts.get("Blast contacts", "").endswith("not reached"), facts
                assert facts.get("Main health damage") == "361", (model["path"], facts)
                fuel = next((line for line in page.locator("#vv-impactSummary li").all_text_contents() if line.startswith("FuelTank:")), "")
                assert "19 damage routed from Main health" in fuel, fuel
                page.locator("[slot='hotspot-spw-check']").evaluate("e => e.remove()")
                spw_models += 1
        assert spw_models == 3

        # Every published vehicle renders its own full section list, with unique colors and slot swatches.
        page.select_option("#vv-caliber", "Item.Caliber.556mm")
        for vehicle in vehicle_data["vehicles"]:
            page.select_option("#vv-vehicle", vehicle["id"])
            page.wait_for_function("args => document.querySelector('#vv-vehicle').value===args.id && document.querySelectorAll('#vv-slots .vv-slot').length===args.slots",
                                   arg={"id": vehicle["id"], "slots": len(vehicle["slots"])})
            if not vehicle["models"]:
                assert page.locator("#vv-fallback").is_visible(), (vehicle["id"], "fallback table not visible")
                assert page.locator("#vv-placeGround").is_disabled(), (vehicle["id"], "impact placement should be disabled without a model")
            expected_tags = set(vehicle["sections"])
            expected_tags.update(s["section"] for s in vehicle["slots"] if s.get("section") and s["section"] != "None")
            expected_labels = [section_label(tag) for tag in sorted(expected_tags, key=lambda tag: (tag != MAIN_SECTION, section_label(tag)))]
            rendered = page.locator("#vv-legend .vv-key").evaluate_all("els => els.map(e => { const s=e.querySelector('.vv-swatch'); return {label:e.textContent.trim(), color:s.style.backgroundColor, computed:getComputedStyle(s).background}; })")
            rendered = [entry for entry in rendered if entry["label"] != "no section: hits do nothing"]
            assert [entry["label"] for entry in rendered] == expected_labels, (vehicle["id"], expected_labels, rendered)
            colors = [entry["color"] for entry in rendered]
            assert len(set(colors)) == len(expected_labels), (vehicle["id"], rendered)
            assert all(entry["computed"] and entry["computed"].startswith("rgb(") for entry in rendered), (vehicle["id"], rendered)
            expected_color = {section_label(tag): "rgb({}, {}, {})".format(*[int(palette[tag][i:i+2], 16) for i in (1, 3, 5)])
                              for tag in expected_tags}
            assert all(entry["color"] == expected_color[entry["label"]] for entry in rendered), (vehicle["id"], rendered)
            slot_colors = page.locator("#vv-slots .vv-slot").evaluate_all("els => els.map(e => ({index:+e.dataset.slot, color:e.querySelector('.vv-swatch').style.backgroundColor}))")
            for slot in slot_colors:
                section = vehicle["slots"][slot["index"]].get("section")
                if section and section != "None":
                    assert slot["color"] == expected_color[section_label(section)], (vehicle["id"], slot, section)
            for index, slot in enumerate(vehicle["slots"]):
                page.locator("#vv-slots .vv-slot").nth(index).click()
                actual = page.locator("#vv-panel-body").evaluate("root => { const facts=[...root.querySelectorAll('.vv-facts')]; const sectionRow=facts.flatMap(dl=>[...dl.querySelectorAll('dt')].map(dt=>[dt,dt.nextElementSibling])).find(([dt])=>dt.textContent==='Section'); const routingRow=facts.flatMap(dl=>[...dl.querySelectorAll('dt')].map(dt=>[dt,dt.nextElementSibling])).find(([dt])=>dt.textContent==='Routing'); return {section:sectionRow && sectionRow[1].textContent, routing:routingRow && [...routingRow[1].querySelectorAll('li')].map(li=>li.textContent)}; }")
                section = slot.get("section") or "?"
                assert actual["section"] == section, (vehicle["id"], index, section, actual)
                assert actual["routing"] == expected_routing(slot), (vehicle["id"], index, slot.get("routing"), actual)

        # 30 mm's newly restored blast entry must expose impact placement in the fresh page state.
        page.select_option("#vv-caliber", "Item.Caliber.30mm")
        assert page.locator("#vv-blastField").is_visible(), "30 mm blast interaction selector is hidden"
        assert page.locator("#vv-interaction option[value='impact']").count() == 1
        page.select_option("#vv-interaction", "impact")
        page.wait_for_function("!document.querySelector('#vv-placeGround').disabled", timeout=20000)
        page.fill("#vv-impactX", "0")
        page.fill("#vv-impactZ", "0")
        page.click("#vv-placeGround")
        assert "Splash" in summary.inner_text(), summary.inner_text()
        browser.close()
    assert not errors, errors
    print(json.dumps({"browser": "passed", "desktop": 1440, "mobile": 360,
                      "section_vehicles": len(vehicle_data["vehicles"]), "gepard_84mm_transfer": "passed",
                      "spw_84mm_front_models": spw_models,
                      "routing_slots": sum(len(v["slots"]) for v in vehicle_data["vehicles"]),
                      "30mm_blast_ui": "passed",
                      "screenshots": str(args.out)}))


if __name__ == "__main__":
    main()
