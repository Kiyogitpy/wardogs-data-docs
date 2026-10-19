"""Recover component grouping for the existing reference-pose vehicle collision models.

Reads owned module exports and GLB JSON only. No new geometry or game execution.
"""
import json
from pathlib import Path
import re
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import damage_tables as dt
import vehicle_models as models


def glb_json(path):
    with path.open("rb") as stream:
        stream.seek(12)
        length, kind = struct.unpack("<II", stream.read(8))
        if kind != 0x4E4F534A:
            raise ValueError(f"Missing GLB JSON: {path}")
        return json.loads(stream.read(length))


def main():
    root = Path(dt.ROOT)
    source = json.loads((root / dt.JSON_OUT).read_text(encoding="utf-8"))
    vehicles = source["vehicles"]
    variants = {Path(p).stem[3:]: p for p in dt.variants()}
    output = {"models": {}, "source_data_tree": source["meta"]["source_data_tree"],
              "generator": "python -I _tools/vehicle_impact_metadata.py",
              "scope": "Reference-pose placed components; excludes unpublished collision geometry."}
    unresolved = []
    for vehicle in vehicles:
        for model in vehicle["models"]:
            for selected in [model, model.get("wheels_destroyed")]:
                if not selected:
                    continue
                path = selected["path"]
                gltf = glb_json(root / path)
                per_variant = []
                for variant in selected["variants"]:
                    vpath = variants.get(variant)
                    if not vpath:
                        raise ValueError(f"Unknown model variant: {variant}")
                    module_files, _, _ = dt.assemble(vpath)
                    state = "destroyed" if "--wheels-destroyed" in path else "intact"
                    candidates = models.components(module_files) + models.wheel_components(module_files, state)[0]
                    nodes = {}
                    for index, node in enumerate(gltf.get("nodes", [])):
                        if "mesh" not in node:
                            continue
                        extras = node.get("extras", {})
                        def matches(component):
                            mesh = (component.get("mesh") or "").rsplit("/", 1)[-1].split(".")[0]
                            if mesh != extras.get("render_mesh") or component["module"] != extras.get("module"):
                                return False
                            wheel = component.get("wheel")
                            return (wheel["index"] == extras.get("wheel", {}).get("index") if wheel
                                    else not extras.get("wheel"))
                        found = [c for c in candidates if matches(c)]
                        if len(found) > 1:
                            attach = extras.get("attach")
                            found = [c for c in found if attach == (
                                f"{c['source'] or 'Chassis'}:{c['socket']}"
                                if c["source"] or c.get("root_socket") else None)]
                        if len(found) != 1:
                            unresolved.append(f"{path}:{index}:{variant}: {len(found)} candidates")
                            nodes[str(index)] = {"component": None, "reason": "Source component match is ambiguous"}
                            continue
                        c = found[0]
                        fragment = re.sub(r"\[\d+\]$", "", c["fragment"]) if c.get("wheel") else c["fragment"]
                        nodes[str(index)] = {"component": c["module"] + ":" + fragment,
                                             "fragment": c["fragment"], "wheel_instance": c.get("wheel", {}).get("index")}
                    per_variant.append(nodes)
                if any(nodes != per_variant[0] for nodes in per_variant[1:]):
                    raise ValueError(f"Shared geometry has differing source components: {path}")
                output["models"][path] = per_variant[0]
    target = root / "assets/data/vehicle-impact-components.json"
    target.write_text(json.dumps(output, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(output['models'])} models; {len(unresolved)} unresolved component matches")
    for message in unresolved:
        print(message)
    return bool(unresolved)


if __name__ == "__main__":
    raise SystemExit(main())
