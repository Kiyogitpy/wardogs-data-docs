"""Recover component grouping for the existing reference-pose vehicle collision models.

Reads owned module exports and GLB JSON only. No new geometry or game execution.
"""
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import damage_tables as dt
import vehicle_models as models


SAMPLING_FIXTURE = Path(__file__).resolve().with_name("vehicle-impact-sampling.json")
SPW_VARIANTS = {"SPW_01", "SPW_02", "SPW_03"}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_point(value, label):
    if (not isinstance(value, list) or len(value) != 3 or
            any(not isinstance(x, (int, float)) or not math.isfinite(x) for x in value)):
        raise ValueError(f"Invalid finite 3-vector for {label}")


def load_sampling_fixture(root, vehicles):
    if not SAMPLING_FIXTURE.is_file():
        raise ValueError(f"Missing required sampling fixture: {SAMPLING_FIXTURE}")
    fixture = json.loads(SAMPLING_FIXTURE.read_text(encoding="utf-8"))
    if fixture.get("format") != 1:
        raise ValueError("Unsupported point-sampling fixture format")
    expected = {
        model["path"]: model
        for vehicle in vehicles if vehicle["id"].startswith("land-tracked-leopard-spawn-spw-")
        for model in vehicle["models"] if set(model["variants"]) & SPW_VARIANTS
    }
    models_fixture = fixture.get("models")
    if not isinstance(models_fixture, dict) or set(models_fixture) != set(expected):
        raise ValueError("SPW point-sampling fixture paths do not match the published SPW models")

    sources = fixture.get("source", {})
    required_sources = ("reference_inputs", "static_mesh_socket_manifest", "collision_manifest", "skeletal_manifest")
    for name in required_sources:
        evidence = sources.get(name)
        if not isinstance(evidence, dict) or not {"path", "sha256"} <= evidence.keys():
            raise ValueError(f"Missing point-sampling source evidence: {name}")
        path = Path(evidence["path"])
        if not path.is_file() or sha256(path) != evidence.get("sha256"):
            raise ValueError(f"Stale or missing point-sampling source evidence: {path}")
    socket_manifest = json.loads(Path(sources["static_mesh_socket_manifest"]["path"]).read_text(encoding="utf-8"))
    if socket_manifest.get("staticMeshSockets") != {}:
        raise ValueError("SPW no-socket policy does not match the fresh mesh manifest")

    for model_path, model in expected.items():
        sampling = models_fixture[model_path]
        glb_path = root / model_path
        if not glb_path.is_file() or sha256(glb_path) != sampling.get("glb_sha256"):
            raise ValueError(f"Stale or missing point-sampling GLB: {model_path}")
        if sampling.get("variants") != model["variants"]:
            raise ValueError(f"Stale point-sampling variant identity: {model_path}")
        for component in sampling.get("components", {}).values():
            raw_dump = Path(component["source_static_mesh_dump"])
            if not raw_dump.is_file() or sha256(raw_dump) != component.get("source_static_mesh_sha256"):
                raise ValueError(f"Stale or missing source static-mesh dump: {raw_dump}")
            validate_point(component.get("bounds_origin"), model_path)
            points = component.get("points")
            if not isinstance(points, list) or len(points) != 1:
                raise ValueError(f"Expected one native bounds point for {model_path}")
            validate_point(points[0], model_path)
            if points[0] != component["bounds_origin"]:
                raise ValueError(f"Point does not match the native bounds origin for {model_path}")
            if (component.get("method") != "native-bounds" or component.get("angle_degrees") != 10 or
                    component.get("socket_count") != 0):
                raise ValueError(f"Unexpected native point-sampling policy for {model_path}")
    return fixture


def attach_point_sampling(root, path, gltf, metadata_nodes, fixture_model, variants):
    if fixture_model.get("variants") != variants:
        raise ValueError(f"Point-sampling variants differ from model variants: {path}")
    components = fixture_model.get("components", {})
    expected_indices = set()
    for index, node in enumerate(gltf.get("nodes", [])):
        if "mesh" not in node:
            continue
        record = metadata_nodes.get(str(index))
        if not record or not record.get("component"):
            raise ValueError(f"Unmapped SPW model node cannot receive sampling metadata: {path}:{index}")
        key = record["component"]
        sample = components.get(key)
        extras = node.get("extras", {})
        if (sample is None or sample.get("node_index") != index or sample.get("component") != key or
                sample.get("module") != extras.get("module") or
                sample.get("render_mesh") != extras.get("render_mesh") or
                sample.get("fragment") != record.get("fragment")):
            raise ValueError(f"SPW sampling identity mismatch for {path}:{index}:{key}")
        expected_indices.add(index)
        record["point_sampling"] = {
            "bounds_origin": sample["bounds_origin"],
            "points": sample["points"],
            "angle_degrees": sample["angle_degrees"],
            "method": sample["method"],
            "socket_count": sample["socket_count"],
        }
    if len(expected_indices) != fixture_model.get("represented_node_count"):
        raise ValueError(f"SPW represented node count changed for {path}")
    fixture_indices = {sample.get("node_index") for sample in components.values()}
    if fixture_indices != expected_indices:
        raise ValueError(f"SPW fixture has missing or extra component nodes for {path}")


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
    sampling_fixture = load_sampling_fixture(root, vehicles)
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
                        component_key = c["module"] + ":" + fragment
                        if path in sampling_fixture["models"]:
                            sample = sampling_fixture["models"][path]["components"].get(component_key)
                            if (sample is None or sample.get("module") != c["module"] or
                                    sample.get("fragment") != c["fragment"] or sample.get("source_asset") != c.get("mesh")):
                                raise ValueError(f"SPW source component mismatch for {path}:{index}:{component_key}")
                        nodes[str(index)] = {"component": component_key,
                                             "fragment": c["fragment"], "wheel_instance": c.get("wheel", {}).get("index")}
                    if path in sampling_fixture["models"]:
                        attach_point_sampling(root, path, gltf, nodes,
                                              sampling_fixture["models"][path], selected["variants"])
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
