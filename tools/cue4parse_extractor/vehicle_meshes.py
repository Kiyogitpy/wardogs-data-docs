# vehicle_meshes.py: per-vehicle collision-mesh export around WdExtract's mesh mode.
# Usage:
#   python -I vehicle_meshes.py plan   <repo> <files.txt> <outRoot> [vehicle id...]
#   WdExtract <Paks> <key> <usmap> <outRoot>/<id> <oodle> mesh <outRoot>/<id>/_inputs.txt --names <usmap>
#   python -I vehicle_meshes.py finish <repo> <outRoot> [vehicle id...]
# plan: for each vehicle in assets/data/vehicle-hitboxes.json, assembles its first variant (damage_tables.assemble:
#   platform + slot parts) from the repo's data/ and writes <outRoot>/<id>/_inputs.txt (static, destructible, wheel and
#   skeletal meshes for WdExtract) and _plan.json (every mesh-bearing fragment: attach query, relative transform,
#   surface group, IndexedSlotNames, ...; the wheel setup from the vehicle config's axles; the slot map).
#   <files.txt> is WdExtract's `list ""` output, used to turn /Plugin/... asset paths into package paths.
# finish: merges _plan.json into the manifest.json WdExtract wrote, compares the meshes' slot names with the slot map,
#   checks every GLB (materials = slots, no textures; negative signed volume is a warning) and writes _DONE.txt when
#   all pass. Variant CustomFragmentData mesh overrides (e.g. the chassis skeletal mesh) are applied in plan.
import json, os, re, struct, sys

HASHED = re.compile(r"^_aaa")


def load_dt(repo):
    sys.path.insert(0, os.path.join(repo, "_tools"))
    import damage_tables
    return damage_tables


def package_map(files_txt):
    """/Plugin/rest and /Game/rest asset roots (lower case: asset references differ in case) -> package path."""
    out = {}
    for p in open(files_txt, encoding="utf-8").read().split():
        m = re.match(r"^(?:.*/)?([^/]+)/Content/(.*)$", p)
        if p.startswith("Wardogs/Content/"):
            out[("/Game/" + p[len("Wardogs/Content/"):]).lower()] = p
        elif p.startswith("Engine/Content/"):
            out[("/Engine/" + p[len("Engine/Content/"):]).lower()] = p
        elif m:
            out.setdefault(("/%s/%s" % (m.group(1), m.group(2))).lower(), p)
    return out


def asset_name(path):
    return re.split(r"[/\\]", path)[-1].split(".")[0] if path else None


def ue_to_gltf(t):
    """RelativeTransform (UE cm, quaternion) -> glTF frame, same as MeshMode.cs."""
    tr, q, s = t.get("Translation", {}), t.get("Rotation", {}), t.get("Scale3D", {"X": 1, "Y": 1, "Z": 1})
    qx, qy, qz, qw = (q.get(k, 0.0) for k in "XYZW")
    n = (qx * qx + qy * qy + qz * qz + qw * qw) ** 0.5 or 1.0
    r = lambda v: round(v, 5)
    return {"translation": [r(-tr.get("Y", 0) / 100), r(tr.get("Z", 0) / 100), r(tr.get("X", 0) / 100)],
            "rotation": [r(qy / n), r(-qz / n), r(-qx / n), r(qw / n)],
            "scale": [r(s.get("Y", 1)), r(s.get("Z", 1)), r(s.get("X", 1))]}


def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, p + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, "%s[%d]" % (p, i))
    else:
        yield p, o


def attach(cs):
    q = (cs or {}).get("AttachQuery")
    if not q:
        return None
    return {k: q[k] for k in ("SourceMode", "SourceId", "SocketMode", "SocketName") if k in q}


MESH_KEYS = ("StaticMesh", "Mesh", "WheelMesh", "SkeletalMesh")


def mesh_records(obj, path=""):
    """Dicts inside a fragment that name a mesh, with their key path."""
    if isinstance(obj, dict):
        if any(isinstance(obj.get(k), dict) and obj[k].get("AssetPathName") for k in MESH_KEYS):
            yield path, obj
        for k, v in obj.items():
            if k not in ("Constraint", "BodyInstance"):
                yield from mesh_records(v, path + "." + k if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from mesh_records(v, "%s[%d]" % (path, i))


def record(dt, pkgs, module, ftype, fname, enabled, path, d, frag_props):
    key = next(k for k in MESH_KEYS if isinstance(d.get(k), dict) and d[k].get("AssetPathName"))
    asset = d[key]["AssetPathName"]
    cs = d.get("ComponentSettings", {})
    rt = d.get("RelativeTransform") or cs.get("RelativeTransform")
    tag = lambda v: v.get("TagName") if isinstance(v, dict) else v
    r = {"module": module, "fragmentType": ftype, "fragment": fname, "enabled": enabled, "path": path,
         "meshKey": key, "mesh": asset, "meshPackage": pkgs.get(asset.split(".")[0].lower()),
         "meshType": d.get("MeshType") or ("SkeletalMesh" if key == "SkeletalMesh" else "StaticMesh"),
         "componentTags": cs.get("Tags"), "identifier": cs.get("Identifier"), "attach": attach(cs),
         "relativeTransformUe": rt, "relativeTransform": ue_to_gltf(rt) if rt else None,
         "registerComplexSurface": d.get("bRegisterComplexSurface"), "hitEvents": d.get("bHitEvents"),
         "surfaceGroup": tag(d.get("SurfaceGroup")), "surfaceType": d.get("SurfaceType"),
         "collisionProfile": {k: v for k, v in (d.get("CollisionProfile", {}).get("Settings") or {}).items() if k in ("Type", "Profile")} or None}
    for k in ("IndexedSlotNames", "PerWheelSurfaceGroups", "DestructionMesh", "MeshTag", "PhysicsAssetOverride"):
        if k in d:
            r[k[0].lower() + k[1:]] = tag(d[k]) if k == "MeshTag" else (d[k].get("AssetPathName") if isinstance(d[k], dict) and "AssetPathName" in d[k] else d[k])
    m = re.match(r"^DestructibleMeshesData\[(\d+)\]", path)
    if m:
        grp = frag_props["DestructibleMeshesData"][int(m.group(1))]
        r["destructibleGroup"] = tag(grp.get("DestructibleMeshGroupTag"))
        r["groupAttach"] = attach(frag_props.get("DestructibleMeshesComponentSettings"))
    un = {k: v for k, v in leaves(d) if any(HASHED.match(p) for p in re.split(r"[.\[\]]", k) if p)
          and not re.search(r"Constraint|BodyInstance", k)}
    if un:
        r["unresolved"] = dict(list(un.items())[:40])
    return r


def plan(repo, files_txt, out_root, ids):
    dt = load_dt(repo)
    pkgs = package_map(files_txt)
    vehicles = json.load(open(os.path.join(repo, "assets/data/vehicle-hitboxes.json"), encoding="utf-8"))["vehicles"]
    vpaths = {os.path.basename(p)[3:-5]: p for p in dt.variants()}
    for v in vehicles:
        if ids and v["id"] not in ids:
            continue
        vfile = vpaths[v["variants"][0]]
        modules, missing, _ = dt.assemble(vfile)
        frags, others, configs = [], [], []
        for f in modules:
            objs = {o.get("Name"): o for o in dt.exports(f)}
            owner = next((o for o in objs.values() if o.get("Type") in ("ModularVehiclePlatform", "ModularVehiclePart")), None)
            for fr in (owner or {}).get("Properties", {}).get("Fragments", []):
                fname = fr["Value"]["Fragment"]["ObjectName"].split(":")[-1].rstrip("'")
                obj = objs.get(fname, {}); t = obj.get("Type"); props = obj.get("Properties", {})
                enabled = fr["Value"].get("bEnabled", True)
                if t == "MVF_VehicleConfig" and enabled:
                    configs.append(props.get("VehicleConfig", {}).get("AssetPathName"))
                recs = list(mesh_records(props))
                for path, d in recs:
                    frags.append(record(dt, pkgs, asset_name(f), t, fname, enabled, path, d, props))
                if not recs and t in ("MVF_ActorFragment", "MVF_DeployStateCollision"):
                    others.append({"module": asset_name(f), "fragmentType": t, "fragment": fname, "enabled": enabled,
                                   "properties": dict(list(leaves(props))[:60])})
        # Variant fragment overrides: CustomFragmentData Path "<slot path>:<component tag>" with an OverrideMesh
        # (e.g. ":Chassis" -> the variant's chassis skeletal mesh). Materials are ignored (render only).
        vprops = next(o for o in dt.exports(vfile) if o.get("Type") == "ModularVehicleVariant")["Properties"]
        overrides = []
        for o in vprops["AssemblyData"].get("CustomData", {}).get("CustomFragmentData", []):
            mesh = ((o.get("Data") or {}).get("OverrideMesh") or {}).get("AssetPathName")
            slot, _, ctag = o["Path"]["Path"].rpartition(":")
            if not mesh:
                continue
            hit = [r for r in frags if ctag in (r["componentTags"] or []) + [r["identifier"]]
                   and (slot or r["module"] == asset_name(modules[0]))]
            for r in hit:
                r["meshOverriddenFrom"] = r["mesh"]; r["mesh"] = mesh
                r["meshPackage"] = pkgs.get(mesh.split(".")[0].lower()); r["variantOverride"] = o["Path"]["Path"]
            overrides.append({"path": o["Path"]["Path"], "mesh": mesh, "applied": len(hit)})
        wheels = []
        for c in configs:
            cf = dt.asset_file(c) if c else None
            cfg = dt.exports(cf)[0].get("Properties", {}) if cf else {}
            for ai, ax in enumerate(cfg.get("AxleDataAssets") or []):
                af = dt.asset_file(ax["ObjectPath"].split(".")[0])
                for w in (dt.exports(af)[0].get("Properties", {}).get("WheelSetup", []) if af else []):
                    wheels.append({"index": len(wheels), "axle": asset_name(ax["ObjectPath"]), "side": w.get("Side"),
                                   "bone": w.get("BoneName"), "tyreHealth": (w.get("TyreHealthAttribute") or {}).get("TagName"),
                                   "wheelTags": w.get("WheelTags")})
        inputs = []
        for r in frags:
            if not r["enabled"] or not r["meshPackage"]:
                continue
            if r["meshType"].endswith("SkeletalMesh") or r["registerComplexSurface"] is not False or r["fragmentType"] == "MVF_StaticMesh":
                inputs.append(r["meshPackage"])
            # The destroyed-tyre mesh (Vehicle §3.2 wheel mesh swap), for the viewer's damage-state models.
            if r["fragmentType"] == "MVF_InstancedWheels" and r.get("destructionMesh"):
                inputs.append(pkgs.get(r["destructionMesh"].split(".")[0].lower()) or r["destructionMesh"])
        d = os.path.join(out_root, v["id"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "_inputs.txt"), "w", encoding="utf-8").write("\n".join(dict.fromkeys(inputs)) + "\n")
        p = {"vehicle": v["id"], "variant": v["variants"][0], "variants": v["variants"], "damageRow": v["damage_row"],
             "modules": [asset_name(m) for m in modules], "modulesMissing": missing, "vehicleConfig": configs,
             "wheels": wheels, "slotMap": [{"group": s["group"], "slot": s["slot"], "section": s["section"]} for s in v["slots"]],
             "variantMeshOverrides": overrides, "fragments": frags, "otherFragments": others,
             "unresolvedAssets": sorted({r["mesh"] for r in frags if not r["meshPackage"]})}
        json.dump(p, open(os.path.join(d, "_plan.json"), "w", encoding="utf-8"), indent=1)
        print(v["id"], "modules", len(modules), "fragments", len(frags), "inputs", len(set(inputs)), "wheels", len(wheels),
              "overrides", overrides, "unresolved", p["unresolvedAssets"])


def glb_check(path, slots):
    raw = open(path, "rb").read()
    jl = struct.unpack_from("<I", raw, 12)[0]
    g = json.loads(raw[20:20 + jl]); binc = raw[28 + jl:]
    errs = [k for k in ("textures", "images", "samplers") if g.get(k)]
    mats = [m["name"] for m in g.get("materials", [])]
    if mats != slots:
        errs.append("materials %s != slots %s" % (mats, slots))
    vol = 0.0
    for prim in g["meshes"][0]["primitives"]:
        if set(prim["attributes"]) != {"POSITION"}:
            errs.append("attributes")
        def acc(i, n, f):
            a = g["accessors"][i]; bv = g["bufferViews"][a["bufferView"]]
            v = struct.unpack_from("<" + f * (a["count"] * n), binc, bv.get("byteOffset", 0) + a.get("byteOffset", 0))
            return [v[k:k + n] for k in range(0, len(v), n)] if n > 1 else v
        pos = acc(prim["attributes"]["POSITION"], 3, "f")
        ia = g["accessors"][prim["indices"]]
        idx = acc(prim["indices"], 1, {5125: "I", 5123: "H", 5121: "B"}[ia["componentType"]])
        for t in range(0, len(idx), 3):
            a, b, c = pos[idx[t]], pos[idx[t + 1]], pos[idx[t + 2]]
            vol += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6
    return errs, vol


def finish(repo, out_root, ids):
    vehicles = json.load(open(os.path.join(repo, "assets/data/vehicle-hitboxes.json"), encoding="utf-8"))["vehicles"]
    for v in vehicles:
        d = os.path.join(out_root, v["id"])
        if (ids and v["id"] not in ids) or not os.path.exists(os.path.join(d, "manifest.json")):
            continue
        man = json.load(open(os.path.join(d, "manifest.json"), encoding="utf-8"))
        p = json.load(open(os.path.join(d, "_plan.json"), encoding="utf-8"))
        by_pkg = {}
        for c in man["collisionMeshes"]:
            by_pkg[c["collisionMesh"].lower()] = c["name"]
            for rm in c["renderMeshes"]:
                by_pkg[rm.lower()] = c["name"]
        skipped = {s.split("\t")[0].lower(): s.split("\t")[1] for s in man.get("skipped", [])}
        for r in p["fragments"]:
            k = (r["meshPackage"] or "").lower()
            r["collisionMeshName"] = by_pkg.get(k)
            if not r["collisionMeshName"] and not r["meshType"].endswith("SkeletalMesh"):
                r["noCollisionReason"] = skipped.get(k) or ("not exported (disabled or bRegisterComplexSurface false)" if r["meshPackage"] else "asset path not found in paks")
        # Slot check: slots on meshes that register a complex surface vs the vehicle's slot map.
        cm = {c["name"]: c for c in man["collisionMeshes"]}
        on_mesh, indexed = {}, set()
        for r in p["fragments"]:
            if r["enabled"] and r.get("collisionMeshName") and r["registerComplexSurface"] is not False:
                for s in cm[r["collisionMeshName"]]["slots"]:
                    on_mesh.setdefault(s["name"], set()).add(r["collisionMeshName"])
                for n in r.get("indexedSlotNames") or []:
                    indexed.add(n)
        nwheels = len(p["wheels"])
        produced = set(on_mesh) | {"%s_%d" % (n, i) for n in indexed for i in range(nwheels)}
        mapped = {s["slot"] for s in p["slotMap"] if s["slot"] != "(default)"}
        check = {"meshSlots": {k: sorted(v) for k, v in sorted(on_mesh.items())}, "indexedSlotNames": sorted(indexed),
                 "wheelCount": nwheels, "mapSlotsMissingOnMeshes": sorted(mapped - produced),
                 "meshSlotsNotInMap": sorted(set(on_mesh) - mapped - indexed),
                 "note": "indexed names expand to <name>_<wheel index> over the vehicle config's wheels (assumed, "
                         "matches the slot maps' CC_Wheel_N / CC_Tyre_N); slots not in the map take the group default"}
        errs, warns = [], []
        for c in man["collisionMeshes"]:
            e, vol = glb_check(os.path.join(d, c["file"]), [s["name"] for s in c["slots"]])
            errs += ["%s: %s" % (c["name"], x) for x in e]
            if vol <= 0:   # same in the source numbers (the transform is uniform): an open or inward-facing mesh
                warns.append("%s: signed volume %.4f m3 (open or inward-facing in the source)" % (c["name"], vol))
        check["warnings"] = warns
        fails = open(os.path.join(d, "_failures.txt"), encoding="utf-8").read().strip() if os.path.exists(os.path.join(d, "_failures.txt")) else ""
        man.update({"vehicle": p["vehicle"], "variant": p["variant"], "variants": p["variants"], "damageRow": p["damageRow"],
                    "modules": p["modules"], "vehicleConfig": p["vehicleConfig"], "wheels": p["wheels"],
                    "slotMap": p["slotMap"], "slotCheck": check, "fragments": p["fragments"],
                    "otherFragments": p["otherFragments"], "unresolvedAssets": p["unresolvedAssets"]})
        json.dump(man, open(os.path.join(d, "manifest.json"), "w", encoding="utf-8"), indent=1)
        tris = sum(c["triangles"] for c in man["collisionMeshes"])
        status = "OK" if not errs and not fails and man["collisionMeshes"] else "FAIL"
        print("%-36s %s meshes=%d tris=%d bones=%d missing=%s extra=%s %s%s%s" % (
            v["id"], status, len(man["collisionMeshes"]), tris, len(man["bones"]), check["mapSlotsMissingOnMeshes"],
            check["meshSlotsNotInMap"], "; ".join(errs), (" failures: " + fails.replace("\n", " | ")) if fails else "",
            (" WARN " + "; ".join(warns)) if warns else ""))
        done = os.path.join(d, "_DONE.txt")
        if status == "OK":
            open(done, "w", encoding="utf-8").write(
                "%s: %d collision meshes, %d triangles, %d skeletal meshes (bones), %d fragments. GLBs checked: materials = slots, "
                "no textures/images/samplers, signed volume > 0 unless warned.\nSlot map missing on meshes: %s\n"
                "Mesh slots not in map: %s\nWarnings: %s\n"
                % (v["id"], len(man["collisionMeshes"]), tris, len(man["bones"]), len(p["fragments"]),
                   check["mapSlotsMissingOnMeshes"] or "none", check["meshSlotsNotInMap"] or "none", "; ".join(warns) or "none"))
        elif os.path.exists(done):
            os.remove(done)


if __name__ == "__main__":
    if sys.argv[1] == "plan":
        plan(sys.argv[2], sys.argv[3], sys.argv[4], set(sys.argv[5:]))
    elif sys.argv[1] == "finish":
        finish(sys.argv[2], sys.argv[3], set(sys.argv[4:]))
    else:
        sys.exit(__doc__)
