// physics mode: export physics-asset bodies (simple collision primitives) and skeletal-mesh reference skeletons as JSON.
// Usage: WdExtract ... physics <listFile | asset...> --names <donor.usmap>
//   UPhysicsAsset -> "physicsAssets": every USkeletalBodySetup in SkeletalBodySetups order: bone, the body's collision
//                    settings as cooked (PhysicsType, CollisionReponse, CollisionTraceFlag, PhysMaterial, DefaultInstance)
//                    and its AggGeom elements (sphyl, sphere, box, tapered capsule, convex)
//   USkeletalMesh -> "skeletalMeshes": its PhysicsAsset, Skeleton and reference-pose bones in component space (as `mesh`)
// Everything goes to <outDir>/physics.json; failures to _failures.txt. No render geometry is read: a physics asset holds
// only primitives and convex hulls, and of a skeletal mesh only the reference skeleton is used.
// Elements keep their raw UE values (centimetres, FRotator degrees, bone-local) under "ue"; "local" is the same element
// frame in the glTF axes of `mesh` (metres, (x,y,z) = (-Y, Z, X)_ue / 100), relative to its bone. A bone's component-space
// frame from "skeletalMeshes" composed with "local" places the element (p' = t + q * p, no scale on these frames).
// Values a cooked asset leaves out are its class defaults; they are written as such and marked "(default)".
using CUE4Parse.FileProvider;
using CUE4Parse.UE4.Assets.Exports;
using CUE4Parse.UE4.Assets.Exports.SkeletalMesh;
using CUE4Parse.UE4.Objects.Core.Math;
using CUE4Parse.UE4.Objects.PhysicsEngine;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

static class PhysicsMode
{
    // AggGeom array -> shape type written to the JSON (UE's element classes FKSphylElem, FKSphereElem, ...).
    static readonly (string array, string type)[] Elems = {
        ("SphylElems", "sphyl"), ("SphereElems", "sphere"), ("BoxElems", "box"),
        ("TaperedCapsuleElems", "taperedCapsule"), ("ConvexElems", "convex"), ("LevelSetElems", "levelSet"),
        ("SkinnedLevelSetElems", "skinnedLevelSet"), ("MLLevelSetElems", "mlLevelSet"), ("SkinnedTriangleMeshElems", "skinnedTriangleMesh"),
    };

    public static int Run(AbstractFileProvider provider, string[] assets, string outDir)
    {
        var pas = new List<object>(); var sks = new List<object>(); var skipped = new List<string>(); var failures = new List<string>();
        foreach (var a in assets.Distinct(StringComparer.OrdinalIgnoreCase))
        {
            try
            {
                var exports = provider.LoadPackage(a).GetExports().ToList();
                if (exports.OfType<UPhysicsAsset>().FirstOrDefault() is { } pa) { pas.Add(PhysicsAsset(pa, a)); continue; }
                if (exports.OfType<USkeletalMesh>().FirstOrDefault() is { } sk)
                {
                    var o = JObject.FromObject(MeshMode.Bones(sk));
                    o["package"] = a;
                    o["physicsAsset"] = sk.PhysicsAsset?.ResolvedObject?.GetPathName();
                    o["shadowPhysicsAsset"] = sk.GetOrDefault<CUE4Parse.UE4.Objects.UObject.FPackageIndex>("ShadowPhysicsAsset")?.ResolvedObject?.GetPathName();
                    sks.Add(o);
                    Console.WriteLine($"{sk.Name}: {((JArray)o["bones"]).Count} bones, physics asset {o["physicsAsset"]}");
                    continue;
                }
                skipped.Add($"{a}\tneither a PhysicsAsset nor a SkeletalMesh");
            }
            catch (Exception e) { failures.Add($"{a}\t{e.GetType().Name}: {e.Message}"); Console.WriteLine($"FAIL {a}: {e.GetType().Name}: {e.Message}"); }
        }
        var manifest = new Dictionary<string, object> {
            ["axes"] = "ue: centimetres, bone-local, as cooked. local and bones: glTF metres, +Y up, right-handed, (x,y,z) = (-Y, Z, X)_ue / 100",
            ["physicsAssets"] = pas, ["skeletalMeshes"] = sks, ["skipped"] = skipped,
        };
        File.WriteAllText(Path.Combine(outDir, "physics.json"), JsonConvert.SerializeObject(manifest, Formatting.Indented));
        File.WriteAllLines(Path.Combine(outDir, "_failures.txt"), failures);
        Console.WriteLine($"physics: assets={pas.Count} skeletalMeshes={sks.Count} skipped={skipped.Count} fail={failures.Count}");
        return failures.Count > 0 ? 2 : 0;
    }

    static object PhysicsAsset(UPhysicsAsset pa, string package)
    {
        var bodies = new List<object>(); var counts = new SortedDictionary<string, int>(StringComparer.Ordinal);
        for (int i = 0; i < pa.SkeletalBodySetups.Length; i++)
        {
            var bs = pa.SkeletalBodySetups[i].Load<USkeletalBodySetup>() ?? throw new Exception($"SkeletalBodySetups[{i}] does not load");
            // The cooked tagged properties as CUE4Parse serialises them: enum values as "EType::Value", structs as objects.
            var props = (JObject)JObject.Parse(JsonConvert.SerializeObject(bs))["Properties"] ?? new JObject();
            string Or(string key, string dflt) => props[key]?.ToString() ?? dflt + " (default)";
            var shapes = new List<object>();
            var agg = props["AggGeom"] as JObject ?? new JObject();
            foreach (var (array, type) in Elems)
                foreach (var el in agg[array] as JArray ?? new JArray())
                {
                    var e = (JObject)el;
                    if (type is not ("sphyl" or "sphere" or "box" or "taperedCapsule" or "convex"))
                        throw new Exception($"{bs.BoneName.Text}: {array} is not exported by this mode");
                    shapes.Add(Shape(type, e));
                    counts[type] = counts.GetValueOrDefault(type) + 1;
                }
            foreach (var p in agg.Properties())
                if (!Elems.Any(x => x.array == p.Name) && p.Value is JArray { Count: > 0 })
                    throw new Exception($"{bs.BoneName.Text}: unknown AggGeom array {p.Name}");
            bodies.Add(new Dictionary<string, object> {
                ["index"] = i, ["bodySetup"] = bs.Name, ["boneName"] = bs.BoneName.Text,
                // UE spells the property CollisionReponse.
                ["physicsType"] = Or("PhysicsType", "EPhysicsType::PhysType_Default"),
                ["collisionResponse"] = Or("CollisionReponse", "EBodyCollisionResponse::BodyCollision_Enabled"),
                ["collisionTraceFlag"] = Or("CollisionTraceFlag", "ECollisionTraceFlag::CTF_UseDefault"),
                ["physMaterial"] = props["PhysMaterial"]?["ObjectPath"]?.ToString(),
                ["physMaterialOverride"] = props["DefaultInstance"]?["PhysMaterialOverride"]?["ObjectPath"]?.ToString(),
                ["defaultInstance"] = props["DefaultInstance"] ?? new JObject(),
                ["shapes"] = shapes,
            });
        }
        Console.WriteLine($"{pa.Name}: {bodies.Count} bodies, {string.Join(", ", counts.Select(c => $"{c.Value} {c.Key}"))}");
        return new Dictionary<string, object> {
            ["name"] = pa.Name, ["package"] = package, ["bodyCount"] = bodies.Count, ["shapeCounts"] = counts,
            ["boundsBodies"] = pa.BoundsBodies, ["constraints"] = pa.ConstraintSetup.Length, ["bodies"] = bodies,
        };
    }

    static object Shape(string type, JObject e)
    {
        float F(string k) => e[k]?.Value<float>() ?? 0f;
        FVector V(JToken t) => t == null ? FVector.ZeroVector : new FVector(t["X"].Value<float>(), t["Y"].Value<float>(), t["Z"].Value<float>());
        MeshMode.Xf local;
        if (type == "convex")
        {
            // FKConvexElem: hull vertices in the element frame, placed by its FTransform.
            var t = e["Transform"];
            var q = t?["Rotation"] is { } r ? new FQuat(r["X"].Value<float>(), r["Y"].Value<float>(), r["Z"].Value<float>(), r["W"].Value<float>()) : FQuat.Identity;
            var s = t?["Scale3D"] is { } sc ? V(sc) : new FVector(1, 1, 1);
            local = MeshMode.Xf.FromUe(V(t?["Translation"]), q, s);
        }
        else
        {
            // The other elements: Center (cm) and Rotation (FRotator, degrees) in the bone frame; a sphere has no rotation.
            var r = e["Rotation"];
            var rot = r == null ? new FRotator(0, 0, 0) : new FRotator(r["Pitch"].Value<float>(), r["Yaw"].Value<float>(), r["Roll"].Value<float>());
            local = MeshMode.Xf.FromUe(V(e["Center"]), rot.Quaternion(), new FVector(1, 1, 1));
        }
        var d = new Dictionary<string, object> {
            ["type"] = type, ["name"] = e["Name"]?.ToString(),
            ["collisionEnabled"] = e["CollisionEnabled"]?.ToString() ?? "ECollisionEnabled::QueryAndPhysics (default)",
            ["local"] = new Dictionary<string, object> {
                ["translation"] = new[] { MeshMode.R(local.T.X), MeshMode.R(local.T.Y), MeshMode.R(local.T.Z) },
                ["rotation"] = new[] { MeshMode.R(local.Q.X), MeshMode.R(local.Q.Y), MeshMode.R(local.Q.Z), MeshMode.R(local.Q.W) },
                ["scale"] = new[] { MeshMode.R(local.S.X), MeshMode.R(local.S.Y), MeshMode.R(local.S.Z) },
            },
        };
        // Sizes in metres; axes of the element frame in glTF terms. UE: a sphyl/tapered capsule runs along its local Z
        // (glTF local +Y after the axis map); a box's X/Y/Z are full extents along UE local X/Y/Z (glTF local z/x/y).
        switch (type)
        {
            case "sphyl": d["radius"] = MeshMode.R(F("Radius") / 100); d["length"] = MeshMode.R(F("Length") / 100); break;
            case "sphere": d["radius"] = MeshMode.R(F("Radius") / 100); break;
            case "box": d["size"] = new[] { MeshMode.R(F("Y") / 100), MeshMode.R(F("Z") / 100), MeshMode.R(F("X") / 100) }; break;
            case "taperedCapsule":
                d["radius0"] = MeshMode.R(F("Radius0") / 100); d["radius1"] = MeshMode.R(F("Radius1") / 100); d["length"] = MeshMode.R(F("Length") / 100); break;
            case "convex":
                d["vertices"] = (e["VertexData"] as JArray ?? new JArray()).Select(v => MeshMode.ToGltf(V(v)))
                    .Select(p => new[] { MeshMode.R(p.X), MeshMode.R(p.Y), MeshMode.R(p.Z) }).ToList();
                d["indices"] = e["IndexData"]?.ToObject<int[]>() ?? Array.Empty<int>();
                break;
        }
        d["ue"] = e;
        return d;
    }
}
