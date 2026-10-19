"""Audit every cooked ModularVehicleVariant against the exported viewer data.

Read-only except for the explicitly requested, create-new JSON report. Uses the
repository's source-data evaluators; it does not establish native-engine parity.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import glob
import hashlib
import json
import math
from pathlib import Path
import struct
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import damage_tables as dt
import vehicle_models as vm

ROOT = Path(dt.ROOT)
FLAG_FIELDS = ("_aaachkphmgcampdlhdkkf", "_aaacikmpjffpcggjhonpl", "_aaadafjbjhkkggmmjaeba")
ROUTES = (("pre", "PreDamageRouting"), ("post", "PostDamageRouting"), ("simultaneous", "SimultaneousDamageRouting"))


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def discover_variants():
    try:
        result = subprocess.run(["rg", "-l", "-F", "-g", "*.json", '"Type": "ModularVehicleVariant"', str(ROOT / "data")],
                                check=True, capture_output=True, text=True)
        return sorted(Path(line) for line in result.stdout.splitlines()), "typed export census with rg"
    except FileNotFoundError:
        return sorted(Path(p) for p in glob.glob(str(ROOT / "data/**/VV_*.json"), recursive=True)), "VV filename census (rg unavailable)"


def enabled_health(module_files):
    """Keep all raw tags and route settings, including fields the viewer reduces."""
    output = []
    for path in module_files:
        objects = {obj.get("Name"): obj for obj in dt.exports(path)}
        owner = next((o for o in objects.values() if o.get("Type") in ("ModularVehiclePlatform", "ModularVehiclePart")), {})
        for fragment in owner.get("Properties", {}).get("Fragments", []):
            value = fragment["Value"]
            if not value.get("bEnabled", True):
                continue
            name = value["Fragment"]["ObjectName"].split(":")[-1].rstrip("'")
            obj = objects.get(name, {})
            if obj.get("Type") == "MVF_HealthSections":
                for pair in obj.get("Properties", {}).get("HealthSections", []):
                    output.append({"key": dt.tag(pair["Key"]), "source": relative(path),
                                   "fragment": fragment["Key"], "value": pair["Value"]})
    return output


def nondefault(value):
    if isinstance(value, dict):
        return any(nondefault(v) for v in value.values())
    if isinstance(value, list):
        return any(nondefault(v) for v in value)
    return value not in (None, False, 0, "", "None")


def glb_json(path):
    data = Path(path).read_bytes()
    if len(data) < 20 or struct.unpack_from("<III", data) != (0x46546C67, 2, len(data)):
        raise ValueError("invalid GLB header")
    length, kind = struct.unpack_from("<II", data, 12)
    if kind != 0x4E4F534A or 20 + length > len(data):
        raise ValueError("missing or truncated JSON chunk")
    return json.loads(data[20:20 + length])


def resolve_material(name, slots):
    parts = name.split("|")
    group = "ComplexSurface.Group." + (parts[1] if len(parts) > 1 else "Default")
    while group.startswith("ComplexSurface.Group."):
        for key in (parts[0], "(default)"):
            for slot in slots:
                if slot["group"] == group and slot["slot"] == key:
                    return slot["section"]
        group = group.rsplit(".", 1)[0]
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", "--report", dest="out", type=Path, required=True, help="New report path; existing files are refused")
    parser.add_argument("--expect-variants", type=int, help="Fail if the typed source census differs from this count")
    parser.add_argument("--collision-metadata", type=Path, help="Optional collision-mode metadata for raw-body coverage")
    args = parser.parse_args()
    if args.out.exists():
        parser.error("report already exists; choose a new path")
    viewer_path = ROOT / "assets/data/vehicle-hitboxes.json"
    metadata_path = ROOT / "assets/data/vehicle-impact-components.json"
    viewer = json.loads(viewer_path.read_text(encoding="utf-8"))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    collision = json.loads(args.collision_metadata.read_text(encoding="utf-8")) if args.collision_metadata else {}
    collision_names = {item["objectPath"].rsplit(".", 1)[-1] for item in collision.get("staticMeshes", [])}
    projectiles = dt.projectiles()
    generic, damage_rows = dt.vehicle_tables()
    current_discovery = {Path(p).resolve() for p in dt.variants()}
    paths, discovery = discover_variants()
    by_variant = defaultdict(list)
    for vehicle in viewer["vehicles"]:
        for name in vehicle["variants"]:
            by_variant[name].append(vehicle)
    records, findings, excluded, model_reports = [], [], [], {}
    checks = Counter()

    def finding(record, code, detail, severity="error"):
        entry = {"severity": severity, "code": code, "detail": detail}
        record["findings"].append(entry)
        findings.append({"variant": record["variant"], **entry})

    for path in paths:
        source_variant = next((o for o in dt.exports(path) if o.get("Type") == "ModularVehicleVariant"), None)
        if source_variant is None:
            excluded.append({"path": relative(path), "reason": "No ModularVehicleVariant export"})
            continue
        name = source_variant["Name"].removeprefix("VV_")
        record = {"variant": name, "source": relative(path), "in_generator_discovery": path.resolve() in current_discovery,
                  "findings": [], "models": []}
        records.append(record)
        try:
            modules, missing, variant_tag = dt.assemble(path)
            sections, flags = dt.sections(modules), dt.section_radial_flags(modules)
            slots = dt.surface_maps(modules)
            damage_tag = dt.damage_tag(modules)
            record.update({"variant_tag": variant_tag, "damage_row": damage_tag, "modules": [relative(p) for p in modules],
                           "missing_modules": missing, "section_count": len(sections), "slot_count": len(slots),
                           "sections": {}, "duplicate_hit_location_tags": {}, "unsupported_route_settings": []})
            if missing:
                finding(record, "missing_modules", missing)
            raw = enabled_health(modules)
            occurrences = Counter(item["key"] for item in raw)
            if any(count > 1 for count in occurrences.values()):
                finding(record, "section_definitions_overwritten", {k: n for k, n in occurrences.items() if n > 1}, "warning")
            hit_tags = defaultdict(list)
            for item in raw:
                key, value = item["key"], item["value"]
                tags = [t for t in value.get("Tags", []) if t.startswith("Meta.Damage.HitLocation.")]
                record["sections"][key] = {"max_health": value["MaxHealth"], "hit_location_tags": tags,
                                           "source_module": Path(item["source"]).stem, "source_fragment": item["fragment"],
                                           "routes": {kind: [{"to": dt.tag(r["Key"]), "scalar": r["Value"]["Scalar"]["Value"],
                                                              "only_when_depleted": r["Value"]["bOnlyWhenDepleted"]}
                                                             for r in value.get(field, [])] for kind, field in ROUTES},
                                           "radial_skip_flags": dict(zip(("pre", "post", "simultaneous"), (bool(value.get(f, False)) for f in FLAG_FIELDS)))}
                for tag in tags:
                    hit_tags[tag].append(key)
                if len(tags) > 1:
                    finding(record, "multiple_hit_tags_reduced_to_first", {"section": key, "tags": tags}, "warning")
                if not isinstance(value["MaxHealth"], (int, float)) or not math.isfinite(value["MaxHealth"]) or value["MaxHealth"] < 0:
                    finding(record, "invalid_max_health", {"section": key, "value": value["MaxHealth"]})
                for kind, field in ROUTES:
                    for route in value.get(field, []):
                        target, settings = dt.tag(route["Key"]), route["Value"]
                        checks["routes"] += 1
                        if target not in sections:
                            finding(record, "route_target_missing", {"section": key, "route": kind, "target": target})
                        scalar = settings.get("Scalar", {}).get("Value")
                        if not isinstance(scalar, (int, float)) or not math.isfinite(scalar):
                            finding(record, "invalid_route_scalar", {"section": key, "route": kind, "value": scalar})
                        elif not 0 <= scalar <= 1:
                            finding(record, "route_scalar_requires_clamp", {"section": key, "route": kind, "value": scalar}, "warning")
                        reduced = {k: v for k, v in settings.items() if k not in ("Scalar", "bOnlyWhenDepleted")}
                        scalar_extra = {k: v for k, v in settings.get("Scalar", {}).items() if k != "Value"}
                        if nondefault(reduced) or nondefault(scalar_extra):
                            detail = {"section": key, "route": kind, "target": target, "settings": settings}
                            record["unsupported_route_settings"].append(detail)
                            finding(record, "lossy_route_settings", detail, "warning")
            record["duplicate_hit_location_tags"] = {tag: sorted(set(keys)) for tag, keys in hit_tags.items() if len(set(keys)) > 1}
            definitions = defaultdict(list)
            for fragment in dt.fragments(modules):
                if fragment.get("Type") != "MVF_HealthSections":
                    continue
                for pair in fragment.get("Properties", {}).get("ComplexSurfaceMappings", {}).get("SurfaceGroups", []):
                    group, value = dt.tag(pair["Key"]), pair["Value"]
                    for slot in value.get("SlotMap", []):
                        definitions[(group, slot["Key"])].append(dt.tag(slot["Value"]))
                    if value.get("bUseDefault"):
                        definitions[(group, "(default)")].append(dt.tag(value.get("Default")))
            record["duplicate_source_slot_keys"] = [{"group": key[0], "slot": key[1], "sections": values}
                                                     for key, values in definitions.items() if len(values) > 1]
            if record["duplicate_source_slot_keys"]:
                finding(record, "source_slot_definitions_overwritten", record["duplicate_source_slot_keys"], "warning")
            record["registered_components"] = []
            components = vm.components(modules) + vm.wheel_components(modules)[0]
            record["skeletal_components_without_display_geometry"] = [{"module": c["module"], "fragment": c["fragment"], "mesh": c.get("mesh")}
                                                                        for c in components if c["kind"] == "skeletal"]
            for component in components:
                if component.get("register"):
                    record["registered_components"].append({"module": component["module"], "fragment": component["fragment"],
                        "mesh": component.get("mesh"), "kind": component["kind"], "surface_group": component.get("group")})
            if not sections or not slots or not damage_tag:
                record["status"] = "unsupported_source_definition"
                record["unsupported_reason"] = {"no_health_sections": not bool(sections), "no_slot_map": not bool(slots), "no_damage_tag": not bool(damage_tag)}
                finding(record, "unsupported_source_definition", record["unsupported_reason"], "limitation")
                continue
            exported = by_variant.get(name, [])
            if len(exported) != 1:
                record["status"] = "missing_or_ambiguous_viewer_export"
                finding(record, "viewer_variant_count", {"expected": 1, "actual": len(exported)})
                continue
            vehicle = exported[0]
            record["viewer_id"] = vehicle["id"]
            record["status"] = "audited_export"
            if vehicle["damage_row"] != damage_tag:
                finding(record, "damage_row_mismatch", {"source": damage_tag, "export": vehicle["damage_row"]})
            if vehicle["main_health"] != sections.get(dt.MAIN, (None,))[0]:
                finding(record, "main_health_mismatch", {"source": sections.get(dt.MAIN, (None,))[0], "export": vehicle["main_health"]})
            expected_sections = {key: {"max_health": v[0], "pre": v[2], "post": v[3], "simultaneous": v[4],
                "radial_routing_skips": dict(zip(("pre", "post", "simultaneous"), flags.get(key, (False, False, False))))} for key, v in sections.items()}
            checks["sections"] += len(sections)
            if json.loads(json.dumps(expected_sections)) != vehicle["sections"]:
                finding(record, "section_export_mismatch", {"source": expected_sections, "export": vehicle["sections"]})
            expected_flags = {key: dict(zip(("pre", "post", "simultaneous"), value)) for key, value in flags.items()}
            if vehicle.get("radial_routing_skips_by_variant", {}).get(name) != expected_flags:
                finding(record, "per_variant_radial_flags_mismatch", {"source": expected_flags, "export": vehicle.get("radial_routing_skips_by_variant", {}).get(name)})
            exported_slots = {(s["group"], s["slot"]): s for s in vehicle["slots"]}
            if len(exported_slots) != len(vehicle["slots"]):
                finding(record, "duplicate_export_slot_keys", "Duplicate (group, slot) entries")
            if {key: s["section"] for key, s in exported_slots.items()} != slots:
                finding(record, "slot_map_mismatch", {"source": [[*key, value] for key, value in sorted(slots.items())]})
            entries = dt.row_entries(damage_tag, damage_rows) + generic
            for key, slot in exported_slots.items():
                checks["slots"] += 1
                section = sections.get(slot["section"])
                if not section:
                    finding(record, "slot_section_missing", {"slot": list(key), "section": slot["section"]})
                    continue
                if slot["hit_location"] != section[1] or slot["max_health"] != section[0]:
                    finding(record, "slot_health_or_tag_mismatch", list(key))
                expected_routes = {kind: [{"to": target, "scalar": scalar, "only_when_depleted": depleted} for target, scalar, depleted in routes]
                                   for kind, routes in zip(("pre", "post", "simultaneous"), section[2:])}
                if slot["routing"] != expected_routes or slot["radial_routing_skips"] != expected_flags.get(slot["section"]):
                    finding(record, "slot_routing_or_flags_mismatch", list(key))
                for caliber in viewer["meta"]["calibers"]:
                    cid = caliber["id"]
                    expected = round(dt.vehicle_rule_factor(entries, cid, section[1], projectiles), 6)
                    checks["direct_factors"] += 1
                    if slot["rule_factor"].get(cid) != expected:
                        finding(record, "direct_factor_mismatch", {"slot": list(key), "source": cid, "expected": expected, "actual": slot["rule_factor"].get(cid)})
                    if caliber.get("blast"):
                        expected = [round(dt.vehicle_rule_factor(entries, cid, section[1], projectiles, radius), 6) for radius in ("Inner", "Outer")]
                        checks["radial_factor_pairs"] += 1
                        if slot["blast_factor"].get(cid) != expected:
                            finding(record, "radial_factor_mismatch", {"slot": list(key), "source": cid, "expected": expected})
                for actor in viewer["meta"].get("explosives", []):
                    expected = [round(dt.source_rule_factor(entries, actor["source_context"] + [actor["source_tag"], "Meta.Damage.Explosive.Radius." + radius], section[1]), 6) for radius in ("Inner", "Outer")]
                    checks["actor_factor_pairs"] += 1
                    if slot.get("explosion_factor", {}).get(actor["id"]) != expected:
                        finding(record, "actor_factor_mismatch", {"slot": list(key), "source": actor["id"], "expected": expected})
            models = [m for m in vehicle["models"] if name in m["variants"]]
            if not models:
                finding(record, "no_reference_pose_geometry", "Table data only; no model declared for this variant", "limitation")
            for base_model in models:
                for model in [base_model] + ([base_model["wheels_destroyed"]] if base_model.get("wheels_destroyed") else []):
                    model_path = model["path"]
                    record["models"].append(model_path)
                    if model_path not in model_reports:
                        gltf = glb_json(ROOT / model_path)
                        nodes = {str(i): node for i, node in enumerate(gltf.get("nodes", [])) if "mesh" in node}
                        mapped = metadata.get("models", {}).get(model_path, {})
                        if set(nodes) != set(mapped):
                            finding(record, "geometry_component_map_coverage", {"model": model_path, "nodes": sorted(nodes), "mapped": sorted(mapped)})
                        names = [m.get("name", "") for m in gltf.get("materials", [])]
                        model_reports[model_path] = {"sha256": digest(ROOT / model_path), "placed_mesh_nodes": len(nodes),
                            "materials": [{"name": value, "section": resolve_material(value, vehicle["slots"])} for value in names],
                            "notes": model.get("notes", []), "native_component_ids": sorted({m.get("component") for m in mapped.values() if m.get("component")}),
                            "raw_static_body_metadata_names": sorted({node.get("extras", {}).get("render_mesh") for node in nodes.values()} & collision_names)}
                        for index, node in nodes.items():
                            mapping = mapped.get(index, {})
                            if not mapping.get("component") or not mapping.get("fragment"):
                                finding(record, "geometry_native_component_unresolved", {"model": model_path, "node": index})
                        checks["geometry_models"] += 1
            represented = {(node.get("extras", {}).get("module"), node.get("extras", {}).get("render_mesh"))
                           for m in models for node in glb_json(ROOT / m["path"]).get("nodes", []) if "mesh" in node}
            record["registered_component_geometry_omissions"] = [c for c in record["registered_components"]
                if (c["module"], (c["mesh"] or "").rsplit("/", 1)[-1].split(".")[0]) not in represented]
            if record["registered_component_geometry_omissions"]:
                finding(record, "registered_component_geometry_omissions", {"count": len(record["registered_component_geometry_omissions"])}, "limitation")
            record["raw_static_body_metadata_coverage"] = {
                "render_mesh_names": sorted({name for path in record["models"] for name in model_reports[path]["raw_static_body_metadata_names"]}),
                "scope": "Optional extraction only; skeletal bodies and query behavior are not validated by this coverage field"}
            for index, entry in enumerate(entries):
                modification = entry["OutModification"]
                if entry.get("InstigatorRequirements") or entry.get("TargetRequirements") or modification.get("CustomOperation") not in (None, "None", "EDamageCustomOperation::None"):
                    record.setdefault("conditional_rule_entries", []).append(index)
        except Exception as error:
            record["status"] = "audit_failed"
            finding(record, "audit_exception", f"{type(error).__name__}: {error}")

    source_names = {r["variant"] for r in records}
    if args.expect_variants is not None and len(records) != args.expect_variants:
        findings.append({"variant": "(catalog)", "severity": "error", "code": "unexpected_variant_count",
                         "detail": {"expected": args.expect_variants, "actual": len(records)}})
    source_catalog_checks = []
    blast_parameters = dt.blast_params()
    expected_actors = {actor["id"]: actor for actor in dt.actor_explosives()}
    for caliber in viewer["meta"]["calibers"]:
        pid = caliber["id"]
        expected = {"source_tag": projectiles[pid][0], "source_context": projectiles[pid][1], "base_damage": projectiles[pid][2]}
        expected["blast"] = blast_parameters[pid] if blast_parameters.get(pid, {}).get("radius", 0) > 0 else None
        differences = {key: {"source": value, "export": caliber.get(key)} for key, value in expected.items() if caliber.get(key) != value}
        source_catalog_checks.append({"id": pid, "differences": differences})
    for actor in viewer["meta"].get("explosives", []):
        expected = expected_actors[actor["id"]]
        differences = {key: {"source": expected[key], "export": actor.get(key)} for key in ("base_damage", "source_tag", "source_context", "blast")
                       if actor.get(key) != expected[key]}
        source_catalog_checks.append({"id": actor["id"], "differences": differences})
    for check in source_catalog_checks:
        if check["differences"]:
            findings.append({"variant": "(catalog)", "severity": "error", "code": "source_catalog_mismatch", "detail": check})
    orphan_names = sorted(set(by_variant) - source_names)
    declared_models = set(model_reports)
    shipped_models = {p.relative_to(ROOT).as_posix() for p in (ROOT / dt.MODELS).glob("*.glb")}
    counts = Counter(item["code"] for item in findings)
    errors = sum(item["severity"] == "error" for item in findings)
    for record in records:
        record["registered_component_count"] = len(record.pop("registered_components", []))
    report = {"generated_utc": datetime.now(timezone.utc).isoformat(), "discovery": discovery,
        "inputs": {"viewer_sha256": digest(viewer_path), "component_map_sha256": digest(metadata_path),
                   "source_data_tree": viewer["meta"].get("source_data_tree"),
                   "collision_metadata": str(args.collision_metadata) if args.collision_metadata else None,
                   "collision_metadata_sha256": digest(args.collision_metadata) if args.collision_metadata else None},
        "summary": {"source_variants": len(records), "generator_discovered_variants": len(current_discovery),
                    "viewer_groups": len(viewer["vehicles"]), "viewer_variants": sum(len(v["variants"]) for v in viewer["vehicles"]),
                    "unique_exported_slots": sum(len(v["slots"]) for v in viewer["vehicles"]),
                    "profile_section_count": sum(len(v["sections"]) for v in viewer["vehicles"]),
                    "profile_route_counts": {kind: sum(len(s[kind]) for v in viewer["vehicles"] for s in v["sections"].values()) for kind, _ in ROUTES},
                    "profile_radial_skip_flag_counts": {kind: sum(bool(s["radial_routing_skips"][kind]) for v in viewer["vehicles"] for s in v["sections"].values()) for kind, _ in ROUTES},
                    "source_status_counts": dict(Counter(r["status"] for r in records)), "errors": errors,
                    "findings_by_code": dict(counts), "checks": dict(checks), "check_count_basis": "Per source variant, except distinct geometry_models",
                    "all_post_routes_only_when_depleted": all(route["only_when_depleted"] for r in records for s in r.get("sections", {}).values() for route in s["routes"]["post"]),
                    "nondefault_curve_absolute_or_other_route_settings": sum(len(r.get("unsupported_route_settings", [])) for r in records),
                    "shipped_models": len(shipped_models), "audited_models": len(model_reports),
                    "variants_with_duplicate_hit_tags": sum(bool(r.get("duplicate_hit_location_tags")) for r in records),
                    "variants_with_raw_static_body_metadata": sum(bool(r.get("raw_static_body_metadata_coverage", {}).get("render_mesh_names")) for r in records),
                    "registered_component_geometry_omissions": sum(len(r.get("registered_component_geometry_omissions", [])) for r in records)},
        "source_catalog_checks": source_catalog_checks,
        "partial_blast_parameters_without_explicit_radius": [{"id": pid, "parameters": parameters}
            for pid, parameters in sorted(blast_parameters.items())
            if not parameters.get("radius") and any(key != "prefer_upwards" for key in parameters)],
        "unused_damage_rows": sorted(set(damage_rows) - {r.get("damage_row") for r in records}),
        "viewer_variants_without_source": orphan_names, "unreferenced_geometry": sorted(shipped_models - declared_models),
        "excluded_non_vehicle_assets": excluded, "variants": records, "models": model_reports,
        "finding_index": [{key: item[key] for key in ("variant", "severity", "code")} for item in findings],
        "limitations": ["Export comparisons reuse repository source evaluators and do not prove those evaluators against native code.",
                        "Factor comparisons retain the exported hostile/no-extra-tags assumptions; conditional/custom rules are not fully evaluated.",
                        "Geometry checks inspect GLB structure, materials and component-map coverage; they do not reproduce cooked Chaos queries or runtime placement.",
                        "Raw collision-body coverage is limited to the optional extraction supplied; matching render names do not establish collision or explosion parity.",
                        "No live game, server, runtime memory, or IDA database was used."]}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps(report["summary"], indent=2))
    return 1 if errors or orphan_names else 0


if __name__ == "__main__":
    raise SystemExit(main())
