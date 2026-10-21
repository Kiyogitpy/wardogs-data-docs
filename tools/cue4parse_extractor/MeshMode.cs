// mesh mode: export vehicle collision meshes (the CC_* hitbox slots) as untextured GLB, never render meshes.
// Usage: WdExtract ... mesh <listFile | asset...>
//   UStaticMesh with ComplexCollisionMesh set -> exports that collision mesh (the render mesh itself is not written)
//   UStaticMesh under .../ComplexCollision(s)/ or named CC_* -> exported as is (stationary ComplexProxy fragments)
//   any other UStaticMesh                     -> skipped ("no collision mesh")
//   USkeletalMesh                             -> reference-pose bones and sockets (component space) into "bones"
// Every input static mesh's sockets (mesh-local) go to "staticMeshSockets", collision mesh or not.
// LOD0 only, positions + indices only (no normals, UVs, colours, textures, images or samplers). One primitive and one
// material per collision slot, material name = FStaticMaterial.MaterialSlotName, baseColorFactor only.
// Axes: glTF = M * UE / 100 with M = [[0,-1,0],[0,0,1],[1,0,0]], i.e. (x,y,z)_gltf = (-Y, Z, X)_ue / 100.
// UE forward (+X) -> glTF +Z (the glTF "front"), UE up (+Z) -> +Y, UE right (+Y) -> -X. det M = -1 flips handedness.
// Index order is kept: UE's cooked triangles are clockwise seen from outside when read as right-handed numbers (signed
// volume < 0), and the det -1 map turns that into glTF's counter-clockwise front faces (signed volume > 0, logged).
using System.Numerics;
using CUE4Parse.FileProvider;
using CUE4Parse.UE4.Assets.Exports;
using CUE4Parse.UE4.Assets.Exports.SkeletalMesh;
using CUE4Parse.UE4.Assets.Exports.StaticMesh;
using CUE4Parse.UE4.Objects.Core.Math;
using CUE4Parse.UE4.Objects.UObject;
using CUE4Parse_Conversion.Dto;
using CUE4Parse_Conversion.Options;
using Newtonsoft.Json;
using SharpGLTF.Schema2;

static class MeshMode
{
    // UE cm (left-handed, Z up) -> glTF m (right-handed, Y up).
    internal static Vector3 ToGltf(FVector v) => new(-v.Y / 100f, v.Z / 100f, v.X / 100f);
    // Rotations: R' = M R M^T. For det M = -1 the quaternion's vector part maps by -M: (x,y,z,w) -> (y,-z,-x,w).
    internal static Quaternion ToGltf(FQuat q) => new(q.Y, -q.Z, -q.X, q.W);

    internal static string PackageOf(UObject o) => o.Owner?.Name ?? o.GetPathName();

    public static int Run(AbstractFileProvider provider, string[] assets, string outDir)
    {
        var meshes = new Dictionary<string, Dictionary<string, object>>(StringComparer.OrdinalIgnoreCase); // by collision package
        var bones = new Dictionary<string, object>();
        var smSockets = new Dictionary<string, object>();
        var skipped = new List<string>();
        var failures = new List<string>();
        foreach (var a in assets.Distinct(StringComparer.OrdinalIgnoreCase))
        {
            try
            {
                var exports = provider.LoadPackage(a).GetExports().ToList();
                if (exports.OfType<USkeletalMesh>().FirstOrDefault() is { } sk) { bones[a] = Bones(sk); continue; }
                var sm = exports.OfType<UStaticMesh>().FirstOrDefault() ?? throw new Exception("no UStaticMesh export");
                var socks = (sm.Sockets ?? []).Select(i => i.Load<UStaticMeshSocket>()).Where(k => k != null)
                    .Select(k => Socket(k.SocketName.Text, null, Xf.Identity.Then(Xf.FromUe(k.RelativeLocation, k.RelativeRotation.Quaternion(), k.RelativeScale)))).ToList();
                if (socks.Count > 0) smSockets[a] = socks;
                UStaticMesh cc; string render = null;
                var ccIndex = sm.GetOrDefault<FPackageIndex>("ComplexCollisionMesh");
                if (ccIndex != null && !ccIndex.IsNull)
                {
                    if (!ccIndex.TryLoad<UStaticMesh>(out cc)) throw new Exception($"ComplexCollisionMesh {ccIndex.Name} does not load");
                    // Some render meshes name themselves as their complex collision: that is render geometry, not exported.
                    if (string.Equals(PackageOf(cc), PackageOf(sm), StringComparison.OrdinalIgnoreCase))
                    { skipped.Add($"{a}\tComplexCollisionMesh is the render mesh itself (render geometry, not exported)"); continue; }
                    render = a;
                }
                else if (a.Contains("/ComplexCollision", StringComparison.OrdinalIgnoreCase) || sm.Name.StartsWith("CC_", StringComparison.OrdinalIgnoreCase))
                    cc = sm;
                else { skipped.Add($"{a}\tno collision mesh"); continue; }
                var key = PackageOf(cc);
                if (!meshes.TryGetValue(key, out var entry))
                {
                    entry = Export(cc, key, outDir);
                    meshes[key] = entry;
                    Console.WriteLine($"{cc.Name}: {entry["triangles"]} tris, {((List<object>)entry["slots"]).Count} slots");
                }
                if (render != null) ((List<string>)entry["renderMeshes"]).Add(render);
            }
            catch (Exception e) { failures.Add($"{a}\t{e.GetType().Name}: {e.Message}"); Console.WriteLine($"FAIL {a}: {e.GetType().Name}: {e.Message}"); }
        }
        var manifest = new Dictionary<string, object> {
            ["axes"] = "glTF metres, +Y up, right-handed, front +Z: (x,y,z) = (-Y, Z, X)_ue / 100; UE triangle index order kept",
            ["collisionMeshes"] = meshes.Values.OrderBy(m => (string)m["name"]).ToList(),
            ["bones"] = bones,
            ["staticMeshSockets"] = smSockets,
            ["skipped"] = skipped,
        };
        File.WriteAllText(Path.Combine(outDir, "manifest.json"), JsonConvert.SerializeObject(manifest, Formatting.Indented));
        File.WriteAllLines(Path.Combine(outDir, "_failures.txt"), failures);
        Console.WriteLine($"mesh: exported={meshes.Count} skipped={skipped.Count} bones={bones.Count} fail={failures.Count}");
        return failures.Count > 0 ? 2 : 0;
    }

    static Dictionary<string, object> Export(UStaticMesh cc, string package, string outDir)
    {
        var dto = new StaticMeshDto(cc, EMeshQuality.Highest, ENaniteMeshFormat.NoNanite);
        var lod = dto.LODs.FirstOrDefault() ?? throw new Exception($"{cc.Name}: no LOD");
        if (lod.SourceLodIndex != 0) throw new Exception($"{cc.Name}: first LOD is {lod.SourceLodIndex}, not 0");
        // Slot names come from the mesh's FStaticMaterial, not the DTO (which prefers the material instance name).
        string Slot(int mi) => mi >= 0 && mi < cc.StaticMaterials.Length
            ? (cc.StaticMaterials[mi].MaterialSlotName.Text ?? $"MaterialSlot_{mi}") : $"MaterialSlot_{mi}";
        string MatName(int mi) => mi >= 0 && mi < cc.StaticMaterials.Length ? cc.StaticMaterials[mi].MaterialInterface?.Name : null;
        string MatPath(int mi) => mi >= 0 && mi < cc.StaticMaterials.Length ? cc.StaticMaterials[mi].MaterialInterface?.ResolvedObject?.GetPathName() : null;

        var model = ModelRoot.CreateModel();
        model.Asset.Generator = "WdExtract mesh (CUE4Parse-Conversion StaticMeshDto)";
        var mesh = model.CreateMesh(cc.Name);
        var slots = new List<object>();
        var min = new Vector3(float.MaxValue); var max = new Vector3(float.MinValue);
        double volUe = 0, volGltf = 0; int tris = 0;
        foreach (var g in lod.Sections.Where(s => s.NumFaces > 0).GroupBy(s => Slot(s.MaterialIndex)).OrderBy(g => g.Min(s => s.FirstIndex)))
        {
            var remap = new Dictionary<uint, int>(); var pos = new List<Vector3>(); var idx = new List<int>();
            int Vert(uint i)
            {
                if (remap.TryGetValue(i, out var r)) return r;
                var p = ToGltf(lod.Vertices[i].Position); pos.Add(p); min = Vector3.Min(min, p); max = Vector3.Max(max, p);
                return remap[i] = pos.Count - 1;
            }
            int n = 0;
            foreach (var s in g)
                for (int t = 0; t < s.NumFaces; t++)
                {
                    uint i0 = lod.Indices[s.FirstIndex + t * 3], i1 = lod.Indices[s.FirstIndex + t * 3 + 1], i2 = lod.Indices[s.FirstIndex + t * 3 + 2];
                    FVector a = lod.Vertices[i0].Position, b = lod.Vertices[i1].Position, c = lod.Vertices[i2].Position;
                    volUe += (a | (b ^ c)) / 6e6;
                    idx.Add(Vert(i0)); idx.Add(Vert(i1)); idx.Add(Vert(i2));   // order kept: see header
                    Vector3 ga = ToGltf(a), gb = ToGltf(b), gc = ToGltf(c);
                    volGltf += Vector3.Dot(ga, Vector3.Cross(gb, gc)) / 6.0;
                    n++;
                }
            var mat = model.CreateMaterial(g.Key).WithDefault(SlotColor(g.Key));
            mesh.CreatePrimitive().WithMaterial(mat)
                .WithVertexAccessor("POSITION", pos)
                .WithIndicesAccessor(PrimitiveType.TRIANGLES, idx);
            var mis = g.Select(x => x.MaterialIndex).Distinct().ToArray();
            slots.Add(new { name = g.Key, collisionMaterial = MatName(mis[0]), collisionMaterialPath = MatPath(mis[0]),
                            materialIndices = mis, triangles = n, vertices = pos.Count });
            tris += n;
        }
        model.UseScene("Scene").CreateNode(cc.Name).WithMesh(mesh);
        var file = cc.Name + ".glb";
        model.SaveGLB(Path.Combine(outDir, file));
        // Closed meshes: signed volume of the UE numbers is negative, of the glTF output positive (outward CCW).
        Console.WriteLine($"  {cc.Name}: signed volume UE order {volUe:F3} m3, glTF {volGltf:F3} m3");
        return new Dictionary<string, object> {
            ["name"] = cc.Name, ["collisionMesh"] = package, ["file"] = file, ["renderMeshes"] = new List<string>(),
            ["lod"] = 0, ["triangles"] = tris, ["slots"] = slots,
            ["boundsMin"] = new[] { R(min.X), R(min.Y), R(min.Z) }, ["boundsMax"] = new[] { R(max.X), R(max.Y), R(max.Z) },
            ["signedVolumeM3"] = R((float)volGltf),
        };
    }

    // A transform in the glTF frame: p' = t + q * (s * p). Then(child) composes like UE's child * parent.
    internal readonly record struct Xf(Vector3 T, Quaternion Q, Vector3 S)
    {
        public static readonly Xf Identity = new(Vector3.Zero, Quaternion.Identity, Vector3.One);
        // CUE4Parse's FQuat.Normalize uses an approximate InvSqrt, so normalize here in double precision.
        public static Xf FromUe(FVector t, FQuat q, FVector s)
        {
            var len = Math.Sqrt((double)q.X * q.X + (double)q.Y * q.Y + (double)q.Z * q.Z + (double)q.W * q.W);
            var uq = new FQuat((float)(q.X / len), (float)(q.Y / len), (float)(q.Z / len), (float)(q.W / len));
            var gq = ToGltf(uq);
            var probe = new FVector(30, 70, 110);   // check R' = M R M^T on a probe vector
            if (Vector3.Distance(Vector3.Transform(ToGltf(probe), gq), ToGltf(uq.RotateVector(probe))) > 1e-4f)
                throw new Exception("quaternion conversion check failed");
            return new(ToGltf(t), gq, new Vector3((float)s.Y, (float)s.Z, (float)s.X));   // scale permutes with |M|
        }
        public Xf Then(Xf c) => new(T + Vector3.Transform(S * c.T, Q), Quaternion.Normalize(Q * c.Q), S * c.S);
    }

    internal static Dictionary<string, object> Socket(string name, string bone, Xf x)
    {
        var m = Matrix4x4.CreateScale(x.S) * Matrix4x4.CreateFromQuaternion(x.Q); m.Translation = x.T;   // row-vector layout
        var d = new Dictionary<string, object> { ["name"] = name };
        if (bone != null) d["bone"] = bone;
        d["translation"] = new[] { R(x.T.X), R(x.T.Y), R(x.T.Z) }; d["rotation"] = new[] { R(x.Q.X), R(x.Q.Y), R(x.Q.Z), R(x.Q.W) };
        d["scale"] = new[] { R(x.S.X), R(x.S.Y), R(x.S.Z) };
        // glTF column-major 4x4 (= System.Numerics row-major memory order)
        d["matrix"] = new[] { m.M11, m.M12, m.M13, m.M14, m.M21, m.M22, m.M23, m.M24, m.M31, m.M32, m.M33, m.M34, m.M41, m.M42, m.M43, m.M44 }.Select(R).ToArray();
        return d;
    }

    // Reference pose in component space, converted to the glTF frame above; the chain is composed there
    // (R -> M R M^T commutes with composition). Sockets: the mesh's and its skeleton's, placed on their bone.
    internal static object Bones(USkeletalMesh sk)
    {
        var info = sk.ReferenceSkeleton.FinalRefBoneInfo; var pose = sk.ReferenceSkeleton.FinalRefBonePose;
        var comp = new Xf[info.Length]; var res = new List<object>();
        for (int i = 0; i < info.Length; i++)
        {
            var p = info[i].ParentIndex;
            Xf local;
            try { local = Xf.FromUe(pose[i].Translation, pose[i].Rotation, pose[i].Scale3D); }
            catch (Exception e) { throw new Exception($"{info[i].Name.Text}: {e.Message}"); }
            comp[i] = p >= 0 ? comp[p].Then(local) : local;
            var b = Socket(info[i].Name.Text, null, comp[i]);
            b["parent"] = p >= 0 ? info[p].Name.Text : null;
            b["decoded_ue_local"] = new {
                parent_index = p,
                translation_cm = DecodedScalars(pose[i].Translation.X, pose[i].Translation.Y, pose[i].Translation.Z),
                rotation_xyzw = DecodedScalars(pose[i].Rotation.X, pose[i].Rotation.Y, pose[i].Rotation.Z, pose[i].Rotation.W),
                scale = DecodedScalars(pose[i].Scale3D.X, pose[i].Scale3D.Y, pose[i].Scale3D.Z)
            };
            res.Add(b);
        }
        var sockets = new List<object>();
        var idx = sk.ReferenceSkeleton.FinalNameToIndexMap;
        var skel = sk.Skeleton.TryLoad<CUE4Parse.UE4.Assets.Exports.Animation.USkeleton>(out var s) ? s : null;
        foreach (var (src, list) in new[] { ("mesh", sk.Sockets ?? []), ("skeleton", skel?.Sockets ?? []) })
            foreach (var k in list.Select(i => i.Load<USkeletalMeshSocket>()).Where(k => k != null))
            {
                var bone = k.BoneName.Text;
                var parent = idx.TryGetValue(bone, out var bi) ? comp[bi] : Xf.Identity;
                var x = parent.Then(Xf.FromUe(k.RelativeLocation, k.RelativeRotation.Quaternion(), k.RelativeScale));
                var d = Socket(k.SocketName.Text, bone, x);
                d["source"] = src; d["boneFound"] = idx.ContainsKey(bone);
                d["decoded_ue_local"] = new {
                    translation_cm = DecodedScalars(k.RelativeLocation.X, k.RelativeLocation.Y, k.RelativeLocation.Z),
                    rotation_degrees_pitch_yaw_roll = DecodedScalars(k.RelativeRotation.Pitch, k.RelativeRotation.Yaw, k.RelativeRotation.Roll),
                    scale = DecodedScalars(k.RelativeScale.X, k.RelativeScale.Y, k.RelativeScale.Z)
                };
                sockets.Add(d);
            }
        return new { skeletalMesh = PackageOf(sk), skeleton = skel != null ? PackageOf(skel) : null,
                     space = "component, reference pose", bones = res, sockets,
                     decoded_ue_local_format = "CUE4Parse binary32 values before exporter rounding; bit patterns authoritative for signed zero. Not original serialized precision." };
    }

    static object DecodedScalars(params float[] values)
    {
        if (values.Any(v => !float.IsFinite(v))) throw new Exception("Non-finite decoded reference-pose scalar");
        return new {
            values = values.Select(v => (double)v).ToArray(),
            ieee754_binary32 = values.Select(v => BitConverter.SingleToUInt32Bits(v).ToString("x8")).ToArray()
        };
    }

    internal static double R(float v) => Math.Round(v, 5);

    // Stable colour per slot name (viewers recolour by section anyway).
    static Vector4 SlotColor(string slot)
    {
        uint h = 2166136261; foreach (var ch in slot) h = (h ^ ch) * 16777619;
        float hue = (h % 360) / 360f, s = 0.55f, v = 0.85f;
        float f(int k) { var x = (k + hue * 6) % 6; return v - v * s * Math.Max(0, Math.Min(Math.Min(x, 4 - x), 1)); }
        return new Vector4(f(5), f(3), f(1), 1);
    }
}
