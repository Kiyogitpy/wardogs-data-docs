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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--no-screenshots", action="store_true")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
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
        browser.close()
    assert not errors, errors
    print(json.dumps({"browser": "passed", "desktop": 1440, "mobile": 360, "screenshots": str(args.out)}))


if __name__ == "__main__":
    main()
