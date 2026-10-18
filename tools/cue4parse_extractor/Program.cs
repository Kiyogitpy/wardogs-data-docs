// WdExtract: offline static export of cooked Wardogs assets via CUE4Parse.
// Usage: WdExtract <paksDir> <aesKeyFile> <usmap> <outDir> <oodleDll> <mode> [args...] [--names <donor.usmap>]
//   list <prefix>                  -> <outDir>/files.txt: every .uasset whose name starts with <prefix> (e.g. GE_)
//   schema <substr...>             -> <outDir>/usmap_schema.json: usmap struct/enum layouts whose name contains a substring
//   findname <pathPrefix> <text>   -> <outDir>/findname.txt: packages under the prefix whose name map contains the text
//   dump <listFile | asset...>     -> <outDir>/<name>.json per package (all exports, Blueprint bytecode included)
//   mesh <listFile | asset...>     -> <outDir>/<collision mesh>.glb + manifest.json: collision meshes only (MeshMode.cs)
//   deobfuscate <out.usmap>        -> writes a deobfuscated copy of <usmap> (needs --names; --sdk <sdk/raw> adds the SDK pass); no paks are read
// The AES key is read from <aesKeyFile> (hex, one line) and never printed. Oodle is loaded from <oodleDll>;
// nothing is downloaded. The game is not run.
using System.Text;
using CUE4Parse.Compression;
using CUE4Parse.Encryption.Aes;
using CUE4Parse.FileProvider;
using CUE4Parse.MappingsProvider;
using CUE4Parse.MappingsProvider.Usmap;
using CUE4Parse.UE4.Objects.Core.Misc;
using CUE4Parse.UE4.Versions;
using Newtonsoft.Json;
using Serilog;

if (args.Length < 6)
{
    Console.WriteLine("usage: WdExtract <paksDir> <aesKeyFile> <usmap> <outDir> <oodleDll> <list|schema|findname|dump|mesh|deobfuscate> [args...] [--names <usmap>]");
    return 1;
}
string paksDir = args[0], keyFile = args[1], usmap = args[2], outDir = args[3], oodle = args[4], mode = args[5];
var rest = args.Skip(6).ToList();
string namesUsmap = null;
var ni = rest.IndexOf("--names");
if (ni >= 0) { namesUsmap = rest[ni + 1]; rest.RemoveRange(ni, 2); }
string sdkDir = null;  // deobfuscate only: Dumper-style SDK headers (sdk/raw) of this same build
var si = rest.IndexOf("--sdk");
if (si >= 0) { sdkDir = rest[si + 1]; rest.RemoveRange(si, 2); }
string typesUsmap = null;  // deobfuscate only: fill Unknown element types from this usmap (export usmap)
var ti = rest.IndexOf("--types");
if (ti >= 0) { typesUsmap = rest[ti + 1]; rest.RemoveRange(ti, 2); }
string fillNamesUsmap = null;  // deobfuscate only: names for tokens still hashed, from this usmap (export usmap)
var fi = rest.IndexOf("--fill-names");
if (fi >= 0) { fillNamesUsmap = rest[fi + 1]; rest.RemoveRange(fi, 2); }
Log.Logger = new LoggerConfiguration().MinimumLevel.Warning().WriteTo.Console().CreateLogger();
Directory.CreateDirectory(outDir);

if (mode == "deobfuscate")
{
    if (namesUsmap == null || rest.Count < 1) { Console.WriteLine("usage: ... deobfuscate <out.usmap> --names <donor.usmap> [--sdk <sdk/raw>] [--types <usmap>] [--fill-names <usmap>]"); return 1; }
    var live = new UsmapParser(usmap).Mappings;
    var donor = new UsmapParser(namesUsmap).Mappings;
    var before = UsmapStats.Count(live);
    var log = new List<string>();
    var rawNames = SdkNames.Snapshot(live);  // this build's own names, before anything is borrowed
    NameDonor.Apply(live, donor, log);
    if (sdkDir != null) SdkNames.Apply(live, rawNames, sdkDir, log);
    KnownPatches.Apply(live.Types, log);
    UsmapWriter.Write(live, rest[0]);
    if (typesUsmap != null || fillNamesUsmap != null)
    {
        // The export usmap: the file above, read back, then the fills, written over it.
        var baseUsmap = new UsmapParser(rest[0]).Mappings;
        if (typesUsmap != null) ExportFill.Types(baseUsmap, new UsmapParser(typesUsmap).Mappings, log);
        if (fillNamesUsmap != null) ExportFill.Names(baseUsmap, rawNames, new UsmapParser(fillNamesUsmap).Mappings, log);
        UsmapWriter.Write(baseUsmap, rest[0]);
    }
    var check = new UsmapParser(rest[0]).Mappings;  // round trip through CUE4Parse's own reader
    var after = UsmapStats.Count(check);
    File.WriteAllLines(Path.Combine(outDir, "_deobfuscate_log.txt"), log);
    Console.WriteLine($"structs {check.Types.Count}, enums {check.Enums.Count}");
    Console.WriteLine($"hashed property names: {before.hashedProps} -> {after.hashedProps}; Unknown types: {before.unknown} -> {after.unknown}; hashed enum values: {before.hashedEnumValues} -> {after.hashedEnumValues}");
    return 0;
}

if (!File.Exists(oodle)) { Console.WriteLine("oodle dll missing"); return 1; }
OodleHelper.Initialize(new OodleDotNet.Oodle(oodle));
var provider = new DefaultFileProvider(paksDir, SearchOption.TopDirectoryOnly, new VersionContainer(EGame.GAME_UE5_7));
provider.ReadScriptData = true;  // keep Blueprint ScriptBytecode in the dumps
provider.Initialize();
provider.MappingsContainer = new FileUsmapTypeMappingsProvider(usmap);
provider.SubmitKey(new FGuid(), new FAesKey(File.ReadAllText(keyFile).Trim()));
Console.WriteLine($"Mounted {provider.MountedVfs.Count} vfs, {provider.Files.Count} files");

if (namesUsmap != null)
{
    var log = new List<string>();
    NameDonor.Apply(provider.MappingsForGame, new UsmapParser(namesUsmap).Mappings, log);
    Console.WriteLine($"--names: {log.Count} changes (see _names_log.txt)");
    File.WriteAllLines(Path.Combine(outDir, "_names_log.txt"), log);
}

if (mode == "list")
{
    var prefix = rest.Count > 0 ? rest[0] : "";
    var files = provider.Files.Values
        .Where(f => f.Extension.Equals("uasset", StringComparison.OrdinalIgnoreCase)
                 && f.NameWithoutExtension.StartsWith(prefix, StringComparison.OrdinalIgnoreCase))
        .Select(f => f.PathWithoutExtension).Distinct().OrderBy(p => p, StringComparer.OrdinalIgnoreCase).ToList();
    File.WriteAllLines(Path.Combine(outDir, "files.txt"), files);
    Console.WriteLine($"{prefix}* packages: {files.Count}");
    return 0;
}
if (mode == "schema")
{
    var m = provider.MappingsForGame;
    var res = new Dictionary<string, object>();
    foreach (var kv in m.Types)
        if (rest.Any(r => kv.Key.Contains(r, StringComparison.OrdinalIgnoreCase)))
            res["struct:" + kv.Key] = new {
                kv.Value.SuperType, kv.Value.PropertyCount,
                Props = kv.Value.Properties.OrderBy(p => p.Key).Select(p => new {
                    p.Key, p.Value.Name, p.Value.ArraySize,
                    Type = p.Value.MappingType?.Type, StructType = p.Value.MappingType?.StructType,
                    Inner = p.Value.MappingType?.InnerType?.Type + "/" + p.Value.MappingType?.InnerType?.StructType,
                    Enum = p.Value.MappingType?.EnumName ?? p.Value.MappingType?.InnerType?.EnumName })
            };
    foreach (var kv in m.Enums)
        if (rest.Any(r => kv.Key.Contains(r, StringComparison.OrdinalIgnoreCase)))
            res["enum:" + kv.Key] = kv.Value;
    File.WriteAllText(Path.Combine(outDir, "usmap_schema.json"), JsonConvert.SerializeObject(res, Formatting.Indented));
    Console.WriteLine($"schema entries: {res.Count}");
    return 0;
}
if (mode == "findname")
{
    var prefix = rest[0]; var needle = rest[1];
    var hits = new List<string>();
    foreach (var f in provider.Files.Values.Where(f => f.Path.StartsWith(prefix, StringComparison.OrdinalIgnoreCase)
                                                    && (f.Extension.Equals("uasset", StringComparison.OrdinalIgnoreCase)
                                                     || f.Extension.Equals("umap", StringComparison.OrdinalIgnoreCase))))
    {
        try
        {
            var pkg = provider.LoadPackage(f.PathWithoutExtension);
            var names = pkg.NameMap.Select(n => n.Name).Where(n => n != null && n.Contains(needle, StringComparison.OrdinalIgnoreCase)).ToList();
            if (names.Count > 0) hits.Add($"{f.PathWithoutExtension}\t{string.Join(", ", names)}");
        }
        catch (Exception e) { hits.Add($"{f.PathWithoutExtension}\tFAIL {e.GetType().Name}: {e.Message}"); }
    }
    File.WriteAllLines(Path.Combine(outDir, "findname.txt"), hits);
    Console.WriteLine($"packages matching: {hits.Count}");
    return 0;
}
if (mode != "dump" && mode != "mesh") { Console.WriteLine($"unknown mode {mode}"); return 1; }

// dump and mesh share the known usmap patches (KnownPatches below).
{
    var log = new List<string>();
    KnownPatches.Apply(provider.MappingsForGame.Types, log);
    File.WriteAllLines(Path.Combine(outDir, "_usmap_patches.txt"), log);
}
var assets = rest.Count == 1 && File.Exists(rest[0]) ? File.ReadAllLines(rest[0]).Where(l => l.Trim().Length > 0).ToArray() : rest.ToArray();
if (mode == "mesh") return MeshMode.Run(provider, assets, outDir);
int ok = 0, fail = 0;
var failures = new List<string>();
foreach (var a in assets)
{
    var name = a.Contains('/') ? a[(a.LastIndexOf('/') + 1)..] : a;
    if (name.Contains('.')) name = name[..name.IndexOf('.')];
    try
    {
        var exports = provider.LoadPackage(a).GetExports().ToList();
        File.WriteAllText(Path.Combine(outDir, name + ".json"), JsonConvert.SerializeObject(exports, Formatting.Indented));
        ok++;
    }
    catch (Exception e) { fail++; failures.Add($"{a}\t{e.GetType().Name}: {e.Message}"); Console.WriteLine($"FAIL {a}: {e.GetType().Name}: {e.Message}"); }
}
File.WriteAllLines(Path.Combine(outDir, "_failures.txt"), failures);
Console.WriteLine($"dump: ok={ok} fail={fail}");
return fail > 0 ? 2 : 0;


// The 5.7.4 usmap hashes many property names and leaves some array element types as Unknown. These fixes are
// by property index, following the SDK declaration order (sdk/raw/BHGameplayEffects_*.hpp, BHGameplayTag_structs.hpp,
// BHFramework_structs.hpp) and UE's own; the closed-beta usmap confirms them. Without them GE modifiers, tag queries
// and static-mesh render data do not decode. They only change names that are still hashed and types still Unknown.
static class KnownPatches
{
    public static void Apply(Dictionary<string, Struct> types, List<string> log)
    {
        var renames = new Dictionary<string, string[]> {
            ["BHGameplayEffect"] = new[] { "Duration", "MaxStacks", "StackDurationRefreshPolicy", "StackExpirationPolicy", "Modifiers", "GrantedTags",
                "ApplicationRequirements", "OngoingRequirements", "RemovalRequirements", "Tags", "bAllowClientPredictedApplication",
                "bAllowClientPredictedModification", "ClientInstigatedApplicationPolicy", "ClientInstigatedModifyPolicy" },
            ["BHGameplayTagRequirements"] = new[] { "RequireTags", "IgnoreTags", "TagQuery" },
            ["BHAttributeMod_Scalar"] = new[] { "Scalar", "CurveIndexing" },
            ["BHAttributeMod_Attribute"] = new[] { "BackingAttribute", "AttributeMode", "CurveTable", "bScaleByDuration", "ScaleDurationEnd" },
            ["BHAttributeMod_SetByCaller"] = new[] { "DataTag", "Coefficient", "bAllowFallback", "FallbackValue", "bScaleByDuration", "ScaleDurationEnd" },
            ["CurveTableRowHandle"] = new[] { "CurveTable", "RowName" },
        };
        foreach (var (t, names) in renames)
        {
            if (!types.TryGetValue(t, out var s)) { log.Add($"patch {t}: not in usmap, skipped"); continue; }
            if (s.Properties.Count != names.Length) { log.Add($"patch {t}: {s.Properties.Count} props, expected {names.Length}; skipped"); continue; }
            for (int i = 0; i < names.Length; i++) Rename(types, t, i, names[i], log);
        }
        PatchArray(types, "BHGameplayEffect", 4, "StructProperty", "BHAttributeModifier", log);   // TArray<FBHAttributeModifier> Modifiers
        PatchArray(types, "GameplayTagQuery", 1, "StructProperty", "GameplayTag", log);           // TArray<FGameplayTag> TagDictionary
        PatchArray(types, "GameplayTagQuery", 2, "ByteProperty", null, log);                      // TArray<uint8> QueryTokenStream
        PatchArray(types, "StaticMesh", 3, "StructProperty", "StaticMaterial", log);             // TArray<FStaticMaterial> StaticMaterials
        PatchArray(types, "StaticMesh", 23, "ObjectProperty", null, log);                        // TArray<UStaticMeshSocket*> Sockets
        PatchArray(types, "StaticMesh", 27, "ObjectProperty", null, log);                        // TArray<UAssetUserData*> AssetUserData
        Rename(types, "StaticMesh", 28, "ComplexCollisionMesh", log);                            // UE5 order: ..., ComplexCollisionMesh, NavCollision
        Rename(types, "StaticMaterial", 1, "MaterialSlotName", log);
        Rename(types, "StaticMaterial", 3, "UVChannelData", log);
    }

    static void Rename(Dictionary<string, Struct> types, string t, int idx, string name, List<string> log)
    {
        if (!types.TryGetValue(t, out var s) || !s.Properties.TryGetValue(idx, out var p)) { log.Add($"patch {t}[{idx}] missing"); return; }
        if (p.Name == name || !NameDonor.Hashed(p.Name)) return;
        log.Add($"patch {t}[{idx}] {p.Name} -> {name}");
        p.Name = name;
    }

    static void PatchArray(Dictionary<string, Struct> types, string t, int idx, string innerType, string innerStruct, List<string> log)
    {
        if (!types.TryGetValue(t, out var s) || !s.Properties.TryGetValue(idx, out var p)) { log.Add($"patch {t}[{idx}] missing"); return; }
        if (p.MappingType.Type != "ArrayProperty" || p.MappingType.InnerType?.Type != "Unknown") return;
        log.Add($"patch {t}[{idx}] {p.Name} array inner Unknown -> {innerType} {innerStruct}");
        s.Properties[idx] = new PropertyInfo(p.Index, p.Name,
            new PropertyType("ArrayProperty", null, new PropertyType(innerType, innerStruct), null, null, null), p.ArraySize);
    }
}

// Borrows names and element types from a donor usmap (an older, unobfuscated build). For each struct present in
// both, properties are paired only inside segments that line up exactly: segments are bounded by "anchor"
// properties whose readable names occur once in each struct, in the same order, and a segment is paired position
// by position only when both sides have the same length and compatible types. A name is borrowed only when this
// build's is hashed and the donor's is readable and unique in its struct; an element type only replaces Unknown.
static class NameDonor
{
    public static bool Hashed(string n) => n != null && n.StartsWith("_aaa");

    // An obfuscated name is "_" + 21 letters a-p, i.e. base 16 of (name length << 64 | 64-bit hash), optionally followed
    // by an FName number "_N". The hash depends only on the name, so the same token means the same name everywhere.
    static readonly System.Text.RegularExpressions.Regex Token = new(@"^(_[a-p]{21})(_\d+)?$");

    public static int? TokenLength(string n)
    {
        var m = Token.Match(n ?? "");
        if (!m.Success) return null;
        int len = 0;
        for (int i = 1; i <= 5; i++) len = (len << 4) | (m.Groups[1].Value[i] - 'a');
        return len;
    }

    public static bool LengthOk(string hashed, string real)
    {
        var len = TokenLength(hashed);
        if (len == null) return true;  // not a plain token (e.g. Blueprint names with GUID suffixes): no check possible
        var m = Token.Match(hashed);
        var realBase = m.Groups[2].Success && real.EndsWith(m.Groups[2].Value) ? real[..^m.Groups[2].Value.Length] : real;
        return realBase.Length == len;
    }

    public static bool HasUnknown(PropertyType t) => t != null && (t.Type == "Unknown" || HasUnknown(t.InnerType) || HasUnknown(t.ValueType));

    // Exact type equality; Unknown on this build's side matches anything.
    static bool StrictSame(PropertyType a, PropertyType b)
    {
        if (a == null || b == null) return a == null && b == null;
        if (a.Type == "Unknown") return true;
        if (a.Type != b.Type || a.StructType != b.StructType || a.EnumName != b.EnumName) return false;
        return StrictSame(a.InnerType, b.InnerType) && StrictSame(a.ValueType, b.ValueType);
    }

    static bool Compatible(PropertyType a, PropertyType b)
    {
        if (a == null || b == null) return a == null && b == null;
        if (a.Type == "Unknown" || b.Type == "Unknown") return true;
        if (a.Type != b.Type) return false;
        if (a.StructType != null && b.StructType != null && a.StructType != b.StructType && !Hashed(a.StructType) && !Hashed(b.StructType)) return false;
        return Compatible(a.InnerType, b.InnerType) && Compatible(a.ValueType, b.ValueType);
    }

    public static void Apply(TypeMappings live, TypeMappings donor, List<string> log)
    {
        int names = 0, types = 0, structs = 0, lengthRejects = 0;
        var resolved = new Dictionary<string, HashSet<string>>();  // token -> real names seen for it
        foreach (var (structName, s) in live.Types)
        {
            if (!donor.Types.TryGetValue(structName, out var d)) continue;
            var lp = s.Properties.Where(kv => kv.Value.Index == 0).OrderBy(kv => kv.Key).ToList();
            var dp = d.Properties.Where(kv => kv.Value.Index == 0).OrderBy(kv => kv.Key).ToList();
            var donorDup = dp.GroupBy(kv => kv.Value.Name).Where(g => g.Count() > 1).Select(g => g.Key).ToHashSet();
            var liveDup = lp.GroupBy(kv => kv.Value.Name).Where(g => g.Count() > 1).Select(g => g.Key).ToHashSet();

            // anchors: readable names unique on both sides, kept only while their order agrees
            var dIndex = dp.Select((kv, i) => (kv.Value.Name, i)).Where(x => !Hashed(x.Name) && !donorDup.Contains(x.Name)).ToDictionary(x => x.Name, x => x.i);
            var anchors = new List<(int l, int d)>();
            for (int i = 0; i < lp.Count; i++)
            {
                var n = lp[i].Value.Name;
                if (Hashed(n) || liveDup.Contains(n) || !dIndex.TryGetValue(n, out var j)) continue;
                if (anchors.Count == 0 || j > anchors[^1].d) anchors.Add((i, j));
            }
            anchors.Add((lp.Count, dp.Count));
            if (Environment.GetEnvironmentVariable("WD_DEBUG_STRUCT") == structName)
                log.Add($"debug {structName}: live {lp.Count} donor {dp.Count}; anchors " + string.Join(" ", anchors.Select(a => $"({a.l},{a.d})")));

            bool changed = false;
            int ls = 0, ds = 0;
            var usedNames = lp.Select(kv => kv.Value.Name).ToHashSet();
            foreach (var (la, da) in anchors)
            {
                int len = la - ls;
                if (len > 0 && len == da - ds && Enumerable.Range(0, len).All(k => Compatible(lp[ls + k].Value.MappingType, dp[ds + k].Value.MappingType)))
                {
                    for (int k = 0; k < len; k++)
                    {
                        var (key, l) = lp[ls + k]; var dn = dp[ds + k].Value;
                        bool rename = Hashed(l.Name) && !Hashed(dn.Name) && !donorDup.Contains(dn.Name) && !usedNames.Contains(dn.Name);
                        if (rename && !LengthOk(l.Name, dn.Name)) { rename = false; lengthRejects++; log.Add($"length-reject {structName}[{key}] {l.Name} (len {TokenLength(l.Name)}) vs {dn.Name}"); }
                        if (rename && Token.Match(l.Name) is { Success: true } tm && !tm.Groups[2].Success)
                        {
                            if (!resolved.TryGetValue(l.Name, out var set)) resolved[l.Name] = set = new HashSet<string>();
                            set.Add(dn.Name);
                        }
                        bool retype = HasUnknown(l.MappingType) && !HasUnknown(dn.MappingType);
                        if (!rename && !retype) continue;
                        var newName = rename ? dn.Name : l.Name;
                        var newType = retype ? dn.MappingType : l.MappingType;
                        for (int e = 0; e < (l.ArraySize ?? 1); e++)
                            if (s.Properties.TryGetValue(key + e, out var el))
                                s.Properties[key + e] = new PropertyInfo(el.Index, newName, newType, el.ArraySize);
                        if (rename) { usedNames.Add(dn.Name); names++; log.Add($"name {structName}[{key}] {l.Name} -> {dn.Name}"); }
                        if (retype) { types++; log.Add($"type {structName}[{key}] {l.Name}: Unknown -> donor"); }
                        changed = true;
                    }
                }
                // the anchor itself already has a readable name, but may still carry an Unknown element type
                if (la < lp.Count)
                {
                    var (key, l) = lp[la]; var dn = dp[da].Value;
                    if (HasUnknown(l.MappingType) && !HasUnknown(dn.MappingType) && Compatible(l.MappingType, dn.MappingType))
                    {
                        for (int e = 0; e < (l.ArraySize ?? 1); e++)
                            if (s.Properties.TryGetValue(key + e, out var el))
                                s.Properties[key + e] = new PropertyInfo(el.Index, el.Name, dn.MappingType, el.ArraySize);
                        types++; changed = true;
                        log.Add($"type {structName}[{key}] {l.Name}: Unknown -> donor (anchor)");
                    }
                }
                ls = la + 1; ds = da + 1;
            }
            if (changed) structs++;
        }

        // Alignment pass for structs whose layout changed between builds: an order-preserving alignment (dynamic
        // programming) over the whole property lists, where a hashed property may only pair with a donor name of
        // exactly the same type and of the length encoded in its token, and equal readable names pair as anchors.
        // Candidates only feed the token dictionary below, so its consistency checks apply to them too.
        int alignCandidates = 0;
        foreach (var (structName, s) in live.Types)
        {
            if (!donor.Types.TryGetValue(structName, out var d)) continue;
            var lp = s.Properties.Where(kv => kv.Value.Index == 0).OrderBy(kv => kv.Key).Select(kv => kv.Value).ToList();
            if (!lp.Any(p => TokenLength(p.Name) != null)) continue;
            var dp = d.Properties.Where(kv => kv.Value.Index == 0).OrderBy(kv => kv.Key).Select(kv => kv.Value).ToList();
            var donorDup = dp.GroupBy(p => p.Name).Where(g => g.Count() > 1).Select(g => g.Key).ToHashSet();
            var liveReadable = lp.Where(p => !Hashed(p.Name)).Select(p => p.Name).ToHashSet();
            int n = lp.Count, m = dp.Count;
            int W(int i, int j)
            {
                var a = lp[i]; var b = dp[j];
                if (!Hashed(a.Name) && a.Name == b.Name) return 3;
                if (TokenLength(a.Name) != null && !Hashed(b.Name) && !donorDup.Contains(b.Name) && !liveReadable.Contains(b.Name)
                    && StrictSame(a.MappingType, b.MappingType) && LengthOk(a.Name, b.Name)) return 2;
                return int.MinValue;
            }
            var score = new int[n + 1, m + 1];
            for (int i = 1; i <= n; i++)
                for (int j = 1; j <= m; j++)
                {
                    int best = Math.Max(score[i - 1, j], score[i, j - 1]);
                    int w = W(i - 1, j - 1);
                    if (w != int.MinValue) best = Math.Max(best, score[i - 1, j - 1] + w);
                    score[i, j] = best;
                }
            for (int i = n, j = m; i > 0 && j > 0;)
            {
                int w = W(i - 1, j - 1);
                if (w != int.MinValue && score[i, j] == score[i - 1, j - 1] + w)
                {
                    if (w == 2 && Token.Match(lp[i - 1].Name) is { Success: true } tm && !tm.Groups[2].Success)
                    {
                        if (!resolved.TryGetValue(lp[i - 1].Name, out var set)) resolved[lp[i - 1].Name] = set = new HashSet<string>();
                        if (set.Add(dp[j - 1].Name)) alignCandidates++;
                    }
                    i--; j--;
                }
                else if (score[i, j] == score[i - 1, j]) i--;
                else j--;
            }
        }

        // Global pass: a token resolved in one struct names the same property everywhere. Keep only tokens with one
        // candidate name, and drop names claimed by two different tokens (the same string always hashes the same).
        var dict = resolved.Where(kv => kv.Value.Count == 1).ToDictionary(kv => kv.Key, kv => kv.Value.First());
        foreach (var dup in dict.GroupBy(kv => kv.Value).Where(g => g.Count() > 1).SelectMany(g => g.Select(kv => kv.Key)).ToList())
            dict.Remove(dup);
        int globalNames = 0;
        foreach (var (structName, s) in live.Types)
        {
            var present = s.Properties.Values.Select(p => p.Name).ToHashSet();
            foreach (var key in s.Properties.Keys.OrderBy(k => k).ToList())
            {
                var p = s.Properties[key];
                var m = Token.Match(p.Name);
                if (!m.Success || !dict.TryGetValue(m.Groups[1].Value, out var real)) continue;
                var newName = real + (m.Groups[2].Success ? m.Groups[2].Value : "");
                if (present.Contains(newName) && newName != p.Name) continue;
                s.Properties[key] = new PropertyInfo(p.Index, newName, p.MappingType, p.ArraySize);
                if (p.Index == 0) { globalNames++; log.Add($"global {structName}[{key}] {p.Name} -> {newName}"); }
                present.Add(newName);
            }
        }

        int enumValues = 0;
        foreach (var (enumName, values) in live.Enums)
        {
            if (!donor.Enums.TryGetValue(enumName, out var dv) || !values.Keys.ToHashSet().SetEquals(dv.Keys)) continue;
            foreach (var k in values.Keys.ToList())
                if (Hashed(values[k]) && !Hashed(dv[k])) { values[k] = dv[k]; enumValues++; }
        }
        log.Insert(0, $"donor: {names} names and {types} element types in {structs} structs; {globalNames} more names from the token dictionary " +
                      $"({dict.Count} tokens, {alignCandidates} alignment candidates considered); {lengthRejects} positional names rejected by the length check; {enumValues} enum values");
    }
}

// Restores names (and Unknown element types) from the Dumper-style SDK headers of this same build: sdk/raw/
// *_classes.hpp and *_structs.hpp list each class's and struct's own properties with real names, C++ types and
// offsets. Each usmap struct is matched to the declaration whose "// ScriptStruct Pkg.Name" (or Class, ...) header
// has its name. This build's own readable names, and tokens printed by both, are anchors; the properties between
// two anchors are paired in order only when both sides have the same count and every pair agrees: compatible type,
// same static-array size, same readable name, same token, and an SDK name of the length the token encodes. Any
// disagreement rejects the whole segment. Pairs feed a token dictionary (one token = one name), which is applied
// everywhere; a token given two names, or a name claimed by two tokens (including names the donor gave), is
// dropped. Where the donor (an older build, paired by position) gave a token a different name than the SDK does at
// the same offset, the SDK name wins: the donor cannot see fields that were reordered between builds.
static class SdkNames
{
    record Member(string Type, string Name, int Dim, bool Bit);
    class Decl { public string Kind; public List<Member> Members = new(); }

    static readonly System.Text.RegularExpressions.Regex Hdr = new(@"^// (\w+) (\S+\.\S+)$");
    static readonly System.Text.RegularExpressions.Regex CppDecl = new(@"^(?:struct|class) (\S+?)(?: final)?(?: :.*)?$");
    static readonly System.Text.RegularExpressions.Regex Mem = new(@"^\t(.+?)\s+(\w+)(\[0x([0-9A-Fa-f]+)\])?(\s*:\s*1)?;\s*// 0x[0-9A-Fa-f]+\(0x[0-9A-Fa-f]+\)(.*)$");
    static readonly System.Text.RegularExpressions.Regex Token = new(@"^(_[a-p]{21})(_\d+)?$");
    static readonly System.Text.RegularExpressions.Regex Generic = new(@"^(\w+)<(.*)>$");
    static readonly System.Text.RegularExpressions.Regex NonIdent = new(@"[^A-Za-z0-9_]");

    public static Dictionary<string, List<(int key, string name)>> Snapshot(TypeMappings m) =>
        m.Types.ToDictionary(kv => kv.Key, kv => kv.Value.Properties.Where(p => p.Value.Index == 0).OrderBy(p => p.Key)
            .Select(p => (p.Key, p.Value.Name)).ToList());

    static Dictionary<string, Decl> Load(string dir, HashSet<string> ambiguous, Dictionary<string, string> cppToUe)
    {
        var decls = new Dictionary<string, Decl>(StringComparer.Ordinal);
        var cppDup = new HashSet<string>();
        var files = Directory.GetFiles(dir, "*.hpp").Where(f => f.EndsWith("_classes.hpp") || f.EndsWith("_structs.hpp"))
            .OrderBy(f => f, StringComparer.Ordinal);
        foreach (var f in files)
        {
            Decl cur = null; string ue = null; bool wantCpp = false;
            foreach (var line in File.ReadLines(f))
            {
                var h = Hdr.Match(line);
                if (h.Success)
                {
                    var kind = h.Groups[1].Value; var full = h.Groups[2].Value;
                    cur = null; wantCpp = false;
                    if (!(kind.EndsWith("Class") || kind.EndsWith("Struct") || kind == "PropertyBag")) continue;
                    ue = full[(full.LastIndexOf('.') + 1)..];
                    cur = new Decl { Kind = kind }; wantCpp = true;
                    if (!decls.TryAdd(ue, cur)) ambiguous.Add(ue);
                    continue;
                }
                if (cur == null) continue;
                if (wantCpp && CppDecl.Match(line) is { Success: true } c)
                {
                    var cpp = c.Groups[1].Value;
                    if (cppToUe.TryGetValue(cpp, out var prev) && prev != ue) cppDup.Add(cpp); else cppToUe[cpp] = ue;
                    wantCpp = false; continue;
                }
                if (line.StartsWith("};")) { cur = null; continue; }
                var m = Mem.Match(line);
                if (!m.Success) continue;
                var name = m.Groups[2].Value;
                if ((name.StartsWith("Pad_") || name.StartsWith("BitPad_")) && m.Groups[6].Value.Contains("Dumper-7")) continue;
                cur.Members.Add(new Member(m.Groups[1].Value.Trim(), name,
                    m.Groups[4].Success ? Convert.ToInt32(m.Groups[4].Value, 16) : 1, m.Groups[5].Success));
            }
        }
        foreach (var d in cppDup) cppToUe.Remove(d);
        return decls;
    }

    // The usmap type a declared C++ type stands for. "Any" = the SDK does not know (FNone_); null = not understood.
    static PropertyType ToType(string t, bool bit, Dictionary<string, string> cppToUe)
    {
        t = t.Trim();
        if (bit) return new PropertyType("BoolProperty");
        switch (t)
        {
            case "FNone_": return new PropertyType("Any");
            case "bool": return new PropertyType("BoolProperty");
            case "float": return new PropertyType("FloatProperty");
            case "double": return new PropertyType("DoubleProperty");
            case "uint8": return new PropertyType("ByteProperty");
            case "int8": return new PropertyType("Int8Property");
            case "int16": return new PropertyType("Int16Property");
            case "uint16": return new PropertyType("UInt16Property");
            case "int32": return new PropertyType("IntProperty");
            case "uint32": return new PropertyType("UInt32Property");
            case "int64": return new PropertyType("Int64Property");
            case "uint64": return new PropertyType("UInt64Property");
            case "class FName": return new PropertyType("NameProperty");
            case "class FString": return new PropertyType("StrProperty");
            case "class FText": return new PropertyType("TextProperty");
            case "FUtf8String": return new PropertyType("Utf8StrProperty");
            case "FAnsiString": return new PropertyType("AnsiStrProperty");
            case "FMulticastSparseDelegateProperty_": return new PropertyType("MulticastDelegateProperty");
        }
        if (t.StartsWith("struct "))
        {
            var cpp = t[7..].Trim();
            if (!cppToUe.TryGetValue(cpp, out var ue)) ue = cpp.StartsWith('F') ? cpp[1..] : cpp;
            return new PropertyType("StructProperty", ue);
        }
        if (t.StartsWith("class ") && t.EndsWith("*") && !t[6..^1].Contains(' ')) return new PropertyType("ObjectProperty");
        var g = Generic.Match(t);
        if (g.Success)
        {
            var arg = g.Groups[2].Value;
            switch (g.Groups[1].Value)
            {
                case "TArray": case "TSet": case "TOptional":
                    var inner = ToType(arg, false, cppToUe);
                    if (inner == null) return null;
                    return new PropertyType(g.Groups[1].Value == "TArray" ? "ArrayProperty" : g.Groups[1].Value == "TSet" ? "SetProperty" : "OptionalProperty", null, inner);
                case "TMap":
                    int depth = 0, split = -1;
                    for (int i = 0; i < arg.Length; i++)
                    {
                        if (arg[i] == '<') depth++; else if (arg[i] == '>') depth--;
                        else if (arg[i] == ',' && depth == 0) { split = i; break; }
                    }
                    if (split < 0) return null;
                    var k = ToType(arg[..split], false, cppToUe); var v = ToType(arg[(split + 1)..], false, cppToUe);
                    return k == null || v == null ? null : new PropertyType("MapProperty", null, k, v);
                case "TSubclassOf": return new PropertyType("ObjectProperty");
                case "TSoftObjectPtr": case "TSoftClassPtr": return new PropertyType("SoftObjectProperty");
                case "TWeakObjectPtr": return new PropertyType("WeakObjectProperty");
                case "TLazyObjectPtr": return new PropertyType("LazyObjectProperty");
                case "TScriptInterface": return new PropertyType("InterfaceProperty");
                case "TDelegate": return new PropertyType("DelegateProperty");
                case "TMulticastInlineDelegate": return new PropertyType("MulticastDelegateProperty");
                case "TFieldPath": return new PropertyType("FieldPathProperty");
            }
            return null;
        }
        if (System.Text.RegularExpressions.Regex.IsMatch(t, @"^E\w+$")) return new PropertyType("EnumProperty", enumName: t);
        return null;
    }

    static bool Compatible(PropertyType u, PropertyType s)
    {
        if (u == null || s == null) return u == null && s == null;
        if (s.Type == "Any" || u.Type == "Unknown") return true;
        if (s.Type == "EnumProperty") return u.Type == "ByteProperty" || (u.Type == "EnumProperty" && u.EnumName == s.EnumName);
        if (u.Type != s.Type) return false;
        if (u.Type == "StructProperty") return string.Equals(u.StructType, s.StructType, StringComparison.OrdinalIgnoreCase);
        return Compatible(u.InnerType, s.InnerType) && Compatible(u.ValueType, s.ValueType);
    }

    // Replaces Unknown parts of u with what the SDK declares, when that is fully known and exists in the usmap.
    static PropertyType Fill(PropertyType u, PropertyType s, TypeMappings live, Dictionary<string, PropertyType> enumInner)
    {
        if (u == null || s == null) return null;
        if (u.Type == "Unknown") return Known(s, live, enumInner);
        if (u.Type is not ("ArrayProperty" or "SetProperty" or "OptionalProperty" or "MapProperty")) return null;
        var i = Fill(u.InnerType, s.InnerType, live, enumInner);
        var v = Fill(u.ValueType, s.ValueType, live, enumInner);
        if (i == null && v == null) return null;
        return new PropertyType(u.Type, u.StructType, i ?? u.InnerType, v ?? u.ValueType, u.EnumName, u.IsEnumAsByte, u.Bool);
    }

    static PropertyType Known(PropertyType s, TypeMappings live, Dictionary<string, PropertyType> enumInner)
    {
        switch (s.Type)
        {
            case "Any": return null;
            case "StructProperty":
                var hit = live.Types.Keys.Where(k => string.Equals(k, s.StructType, StringComparison.OrdinalIgnoreCase)).ToList();
                return hit.Count == 1 ? new PropertyType("StructProperty", hit[0]) : null;
            case "EnumProperty":
                return live.Enums.ContainsKey(s.EnumName) && enumInner.TryGetValue(s.EnumName, out var ei)
                    ? new PropertyType("EnumProperty", null, ei, null, s.EnumName) : null;
            case "ArrayProperty": case "SetProperty": case "OptionalProperty": case "MapProperty":
                return null;  // UE has no nested containers here; leave them alone
            default: return new PropertyType(s.Type);
        }
    }

    static bool NameEq(string u, string s, string structName)
    {
        if (string.Equals(u, s, StringComparison.OrdinalIgnoreCase)) return true;
        var san = NonIdent.Replace(u, "_");  // Dumper-7 turns characters C++ cannot hold (spaces, '?') into '_'
        if (string.Equals(san, s, StringComparison.OrdinalIgnoreCase)) return true;
        if (!s.StartsWith(san + "_", StringComparison.OrdinalIgnoreCase)) return false;
        var rest = s[(san.Length + 1)..];  // ... and suffixes names that collide: _0, _<Class>
        return rest.All(char.IsDigit) || structName.Contains(rest, StringComparison.OrdinalIgnoreCase) || rest.Contains(structName, StringComparison.OrdinalIgnoreCase);
    }

    public static void Apply(TypeMappings live, Dictionary<string, List<(int key, string name)>> raw, string dir, List<string> log)
    {
        var ambiguous = new HashSet<string>();
        var cppToUe = new Dictionary<string, string>(StringComparer.Ordinal);
        var decls = Load(dir, ambiguous, cppToUe);
        var enumInner = new Dictionary<string, PropertyType>();
        void CollectEnum(PropertyType t)
        {
            if (t == null) return;
            if (t.Type == "EnumProperty" && t.EnumName != null && t.InnerType != null && !enumInner.ContainsKey(t.EnumName)) enumInner[t.EnumName] = t.InnerType;
            CollectEnum(t.InnerType); CollectEnum(t.ValueType);
        }
        foreach (var s in live.Types.Values) foreach (var p in s.Properties.Values) CollectEnum(p.MappingType);

        var cand = new Dictionary<string, HashSet<string>>(StringComparer.Ordinal);  // base token -> SDK names
        var direct = new HashSet<(string, int)>();
        var retypes = new List<(string s, int key, PropertyType t)>();
        int matched = 0, segOk = 0, segRejected = 0, caseOnly = 0, outOfOrder = 0, unalignedTokens = 0, bpUnderscore = 0, unparsed = 0, anchorTypeMismatch = 0;
        var rejectWhy = new Dictionary<string, int>();
        foreach (var (structName, s) in live.Types)
        {
            if (ambiguous.Contains(structName) || !decls.TryGetValue(structName, out var d)) continue;
            matched++;
            var keys = raw[structName];
            var lp = keys.Select(k => s.Properties[k.key]).ToList();
            var sp = d.Members;
            var spT = sp.Select(m => ToType(m.Type, m.Bit, cppToUe)).ToList();
            unparsed += spT.Count(t => t == null);
            bool blueprint = d.Kind.Contains("Blueprint") || d.Kind.StartsWith("UserDefined") || structName.EndsWith("_C");

            var anchors = new List<(int l, int d)>();
            for (int i = 0; i < lp.Count; i++)
            {
                var r = keys[i].name;
                int j = -1, hits = 0;
                for (int k = 0; k < sp.Count; k++)
                    if (NameDonor.Hashed(r) ? sp[k].Name == r : NameEq(r, sp[k].Name, structName)) { j = k; hits++; }
                if (hits != 1) continue;
                if (anchors.Count == 0 || j > anchors[^1].d) { anchors.Add((i, j)); if (!NameDonor.Hashed(r) && r != sp[j].Name && string.Equals(r, sp[j].Name, StringComparison.OrdinalIgnoreCase)) caseOnly++; }
                else outOfOrder++;
            }
            anchors.Add((lp.Count, sp.Count));

            int ls = 0, ds = 0;
            foreach (var (la, da) in anchors)
            {
                int len = la - ls;
                if (len > 0 && len != da - ds)
                {
                    unalignedTokens += Enumerable.Range(ls, len).Count(i => NameDonor.Hashed(keys[i].name));
                }
                else if (len > 0)
                {
                    string why = null;
                    var pairs = new List<(string token, string name, int key)>();
                    for (int k = 0; k < len && why == null; k++)
                    {
                        var r = keys[ls + k].name; var cur = lp[ls + k]; var m = sp[ds + k]; var mt = spT[ds + k];
                        if (mt == null) why = "SDK type not understood";
                        else if ((cur.ArraySize ?? 1) != m.Dim) why = "static array size";
                        else if (!Compatible(cur.MappingType, mt)) why = "type";
                        else if (!NameDonor.Hashed(r)) { if (!NameEq(r, m.Name, structName)) why = "readable names differ"; }
                        else if (Token.Match(r) is not { Success: true } tm) why = "unrecognised token";
                        else if (NameDonor.Hashed(m.Name)) { if (m.Name != r) why = "tokens differ"; }
                        else
                        {
                            var suffix = tm.Groups[2].Success ? tm.Groups[2].Value : "";
                            if (!m.Name.EndsWith(suffix)) { why = "FName number"; break; }
                            var baseName = m.Name[..^suffix.Length];
                            if (baseName.Length != NameDonor.TokenLength(r)) why = "length";
                            else pairs.Add((tm.Groups[1].Value, baseName, keys[ls + k].key));
                        }
                    }
                    if (why != null)
                    {
                        segRejected++; rejectWhy[why] = rejectWhy.GetValueOrDefault(why) + 1;
                        log.Add($"sdk reject {structName}[{keys[ls].key}..{keys[la - 1].key}]: {why}");
                    }
                    else
                    {
                        segOk++;
                        foreach (var (token, name, key) in pairs)
                        {
                            if (blueprint && name.Contains('_')) { bpUnderscore++; log.Add($"sdk skip {structName}[{key}] {token} -> {name}: Blueprint name with '_' may be sanitized"); continue; }
                            if (!cand.TryGetValue(token, out var set)) cand[token] = set = new HashSet<string>(StringComparer.Ordinal);
                            set.Add(name); direct.Add((structName, key));
                        }
                        for (int k = 0; k < len; k++)
                            if (Fill(lp[ls + k].MappingType, spT[ds + k], live, enumInner) is { } nt) retypes.Add((structName, keys[ls + k].key, nt));
                    }
                }
                if (la < lp.Count)
                {
                    var cur = lp[la]; var mt = spT[da];
                    if (mt != null && Compatible(cur.MappingType, mt))
                    {
                        if (Fill(cur.MappingType, mt, live, enumInner) is { } nt) retypes.Add((structName, keys[la].key, nt));
                    }
                    else if (mt != null) { anchorTypeMismatch++; log.Add($"sdk anchor type mismatch {structName}[{keys[la].key}] {keys[la].name}"); }
                }
                ls = la + 1; ds = da + 1;
            }
        }

        // token dictionary: one name per token, one token per name (counting names the donor gave other tokens)
        var dict = new Dictionary<string, string>(StringComparer.Ordinal);
        int multiName = 0;
        foreach (var (t, set) in cand.OrderBy(kv => kv.Key, StringComparer.Ordinal))
            if (set.Count == 1) dict[t] = set.First();
            else { multiName++; log.Add($"sdk conflict: token {t} given {set.Count} names: {string.Join(", ", set.OrderBy(x => x, StringComparer.Ordinal))}"); }
        var donorNames = new Dictionary<string, HashSet<string>>(StringComparer.Ordinal);
        foreach (var (structName, s) in live.Types)
            foreach (var (key, r) in raw[structName])
                if (Token.Match(r) is { Success: true } tm && !NameDonor.Hashed(s.Properties[key].Name))
                {
                    var n = s.Properties[key].Name; var suffix = tm.Groups[2].Success ? tm.Groups[2].Value : "";
                    if (!n.EndsWith(suffix)) continue;
                    if (!donorNames.TryGetValue(tm.Groups[1].Value, out var set)) donorNames[tm.Groups[1].Value] = set = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
                    set.Add(n[..^suffix.Length]);
                }
        // Two SDK tokens with one name: both dropped. An SDK token and a token only the donor named: the SDK wins
        // (it pairs by this build's offsets) and the donor's name is withdrawn, so that token is hashed again.
        int nameClaimed = 0;
        var withdraw = new HashSet<string>(StringComparer.Ordinal);
        {
            var sdkClaims = dict.GroupBy(kv => kv.Value, StringComparer.OrdinalIgnoreCase).Where(g => g.Count() > 1).ToList();
            foreach (var g in sdkClaims.OrderBy(g => g.Key, StringComparer.Ordinal))
            {
                var ts = g.Select(kv => kv.Key).OrderBy(x => x, StringComparer.Ordinal).ToList();
                nameClaimed += ts.Count;
                log.Add($"sdk conflict: name {g.Key} claimed by SDK tokens {string.Join(", ", ts)}; all dropped");
                foreach (var t in ts) dict.Remove(t);
            }
            var byName = dict.ToDictionary(kv => kv.Value, kv => kv.Key, StringComparer.OrdinalIgnoreCase);
            foreach (var (t, set) in donorNames.OrderBy(kv => kv.Key, StringComparer.Ordinal))
            {
                if (dict.ContainsKey(t)) continue;
                foreach (var n in set.OrderBy(x => x, StringComparer.Ordinal))
                    if (byName.TryGetValue(n, out var st))
                    {
                        withdraw.Add(t);
                        log.Add($"sdk conflict: name {n} is SDK token {st}'s; the donor's {t} -> {n} withdrawn");
                    }
            }
        }
        int withdrawn = 0;
        foreach (var (structName, s) in live.Types)
            foreach (var (key, r) in raw[structName])
            {
                if (Token.Match(r) is not { Success: true } tm || !withdraw.Contains(tm.Groups[1].Value)) continue;
                var p = s.Properties[key];
                if (p.Name == r) continue;
                withdrawn++; log.Add($"sdk withdraw {structName}[{key}] {p.Name} -> {r}");
                for (int e = 0; e < (p.ArraySize ?? 1); e++)
                    if (s.Properties.TryGetValue(key + e, out var el)) s.Properties[key + e] = new PropertyInfo(el.Index, r, el.MappingType, el.ArraySize);
            }

        int aligned = 0, propagated = 0, corrected = 0, confirmed = 0, dupReverts = 0;
        foreach (var (structName, s) in live.Types)
        {
            var change = new Dictionary<int, string>();
            foreach (var (key, r) in raw[structName])
            {
                if (Token.Match(r) is not { Success: true } tm || !dict.TryGetValue(tm.Groups[1].Value, out var n)) continue;
                var newName = n + (tm.Groups[2].Success ? tm.Groups[2].Value : "");
                // FNames compare without case, and the SDK prints the casing the name pool stored first (CONSTANT, ability):
                // a name that differs only in case is the same name, so the donor's casing is kept.
                if (string.Equals(s.Properties[key].Name, newName, StringComparison.OrdinalIgnoreCase)) { confirmed++; continue; }
                change[key] = newName;
            }
            if (change.Count == 0) continue;
            var names = raw[structName].Select(x => change.TryGetValue(x.key, out var c) ? c : s.Properties[x.key].Name).ToList();
            var dups = names.GroupBy(x => x, StringComparer.OrdinalIgnoreCase).Where(g => g.Count() > 1).Select(g => g.Key).ToHashSet(StringComparer.OrdinalIgnoreCase);
            foreach (var key in change.Keys.OrderBy(k => k).ToList())
            {
                var p = s.Properties[key]; var newName = change[key];
                if (dups.Contains(newName)) { dupReverts++; log.Add($"sdk conflict: {structName}[{key}] {newName} would repeat a name in the struct; kept {p.Name}"); continue; }
                if (NameDonor.Hashed(p.Name)) { if (direct.Contains((structName, key))) aligned++; else propagated++; log.Add($"sdk {(direct.Contains((structName, key)) ? "name" : "global")} {structName}[{key}] {p.Name} -> {newName}"); }
                else { corrected++; log.Add($"sdk correct {structName}[{key}] {p.Name} -> {newName} (donor name replaced)"); }
                for (int e = 0; e < (p.ArraySize ?? 1); e++)
                    if (s.Properties.TryGetValue(key + e, out var el)) s.Properties[key + e] = new PropertyInfo(el.Index, newName, el.MappingType, el.ArraySize);
            }
        }

        int typesFixed = 0;
        foreach (var (structName, key, t) in retypes.Distinct())
        {
            var s = live.Types[structName]; var p = s.Properties[key];
            if (!NameDonor.HasUnknown(p.MappingType)) continue;
            for (int e = 0; e < (p.ArraySize ?? 1); e++)
                if (s.Properties.TryGetValue(key + e, out var el)) s.Properties[key + e] = new PropertyInfo(el.Index, el.Name, t, el.ArraySize);
            typesFixed++; log.Add($"sdk type {structName}[{key}] {p.Name}: Unknown -> SDK");
        }
        log.Insert(1, $"sdk: {matched} structs matched to SDK declarations ({ambiguous.Count} SDK names ambiguous, skipped); segments {segOk} paired, {segRejected} rejected " +
                      $"({string.Join(", ", rejectWhy.OrderBy(kv => kv.Key, StringComparer.Ordinal).Select(kv => $"{kv.Key} {kv.Value}"))}); {unalignedTokens} tokens in unequal segments; " +
                      $"{outOfOrder} anchors out of order (skipped); {caseOnly} anchors that differ only in case; {unparsed} SDK types not understood; {anchorTypeMismatch} anchor type mismatches; {bpUnderscore} Blueprint names with '_' skipped; " +
                      $"dictionary {dict.Count} tokens ({multiName} given two names and {nameClaimed} sharing a name: dropped; {withdraw.Count} donor tokens whose name the SDK gives another token: {withdrawn} names withdrawn); " +
                      $"names: {aligned} by alignment, {propagated} by the dictionary, {corrected} donor names corrected, {confirmed} confirmed, {dupReverts} kept to avoid a repeated name; " +
                      $"{typesFixed} Unknown element types filled");
    }
}

// Turns the deobfuscated usmap into the one data/ is exported with. Both fills compare a struct only with the
// same-named struct of the other usmap that has the same number of property entries, key by key, and need
// the same outer property type (and static-array size, and struct type when this side names one).
//   Types: a property whose type still contains Unknown takes the other side's fully known type. Without this,
//          CUE4Parse stops reading a struct at its first Unknown array and the rest of the export is lost.
//   Names: a property whose name is still a plain token takes the other side's readable name, if the name has
//          the length the token encodes, is not readable anywhere in this build's own usmap (such names are
//          not obfuscated, so no token can stand for them), is not given by the deobfuscated usmap to another
//          token, is not already in the struct, and the token gets one name and the name one token across all
//          structs. A name the deobfuscated usmap already has is never replaced.
static class ExportFill
{
    static readonly System.Text.RegularExpressions.Regex Plain = new(@"^_[a-p]{21}$");

    static bool SameSlot(PropertyInfo a, PropertyInfo b) =>
        a.MappingType.Type == b.MappingType.Type && a.ArraySize == b.ArraySize
        && (a.MappingType.StructType == null || a.MappingType.StructType == b.MappingType.StructType);

    public static void Types(TypeMappings m, TypeMappings donor, List<string> log)
    {
        int filled = 0, left = 0;
        foreach (var (sn, st) in m.Types)
        {
            donor.Types.TryGetValue(sn, out var dt);
            foreach (var key in st.Properties.Keys.ToList())
            {
                var pa = st.Properties[key];
                if (!NameDonor.HasUnknown(pa.MappingType)) continue;
                PropertyInfo pb = null;
                bool ok = dt != null && dt.Properties.Count == st.Properties.Count
                    && dt.Properties.TryGetValue(key, out pb) && !NameDonor.HasUnknown(pb.MappingType) && SameSlot(pa, pb);
                if (!ok) { left++; continue; }
                st.Properties[key] = new PropertyInfo(pa.Index, pa.Name, pb.MappingType, pa.ArraySize);
                filled++; log.Add($"export type {sn}[{key}] {pa.Name}: Unknown -> donor");
            }
        }
        log.Add($"export types: {filled} filled, {left} left Unknown");
    }

    public static void Names(TypeMappings m, Dictionary<string, List<(int key, string name)>> raw, TypeMappings donor, List<string> log)
    {
        var readableLive = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var owner = new Dictionary<string, HashSet<string>>(StringComparer.OrdinalIgnoreCase);  // name -> raw tokens
        foreach (var (sn, list) in raw)
            foreach (var (key, name) in list)
            {
                if (!NameDonor.Hashed(name)) { readableLive.Add(name); continue; }
                if (m.Types.TryGetValue(sn, out var st) && st.Properties.TryGetValue(key, out var p) && !NameDonor.Hashed(p.Name))
                {
                    if (!owner.TryGetValue(p.Name, out var set)) owner[p.Name] = set = new HashSet<string>();
                    set.Add(name);
                }
            }
        var cands = new List<(string sn, int key, string token, string name)>();
        int lengthRejects = 0, liveRejects = 0, ownerRejects = 0, dupRejects = 0;
        foreach (var (sn, st) in m.Types)
        {
            if (!donor.Types.TryGetValue(sn, out var dt) || dt.Properties.Count != st.Properties.Count) continue;
            var inStruct = new HashSet<string>(st.Properties.Values.Select(p => p.Name), StringComparer.OrdinalIgnoreCase);
            foreach (var (key, pa) in st.Properties.Where(kv => kv.Value.Index == 0).OrderBy(kv => kv.Key))
            {
                if (!Plain.IsMatch(pa.Name ?? "") || !dt.Properties.TryGetValue(key, out var pb)) continue;
                if (pb.Name == null || NameDonor.Hashed(pb.Name) || !SameSlot(pa, pb)) continue;
                if (!NameDonor.LengthOk(pa.Name, pb.Name)) { lengthRejects++; continue; }
                if (readableLive.Contains(pb.Name)) { liveRejects++; continue; }
                if (owner.TryGetValue(pb.Name, out var owners) && !(owners.Count == 1 && owners.Contains(pa.Name))) { ownerRejects++; continue; }
                if (inStruct.Contains(pb.Name)) { dupRejects++; continue; }
                cands.Add((sn, key, pa.Name, pb.Name));
            }
        }
        var tokenNames = cands.GroupBy(c => c.token).ToDictionary(g => g.Key, g => g.Select(c => c.name).Distinct(StringComparer.OrdinalIgnoreCase).Count());
        var nameTokens = cands.GroupBy(c => c.name, StringComparer.OrdinalIgnoreCase).ToDictionary(g => g.Key, g => g.Select(c => c.token).Distinct().Count(), StringComparer.OrdinalIgnoreCase);
        int named = 0, inconsistent = 0;
        var tokens = new HashSet<string>();
        foreach (var (sn, key, token, name) in cands)
        {
            if (tokenNames[token] > 1 || nameTokens[name] > 1) { inconsistent++; log.Add($"export name rejected (not one-to-one) {sn}[{key}] {token} -> {name}"); continue; }
            var st = m.Types[sn];
            var pa = st.Properties[key];
            for (int e = 0; e < (pa.ArraySize ?? 1); e++)
                if (st.Properties.TryGetValue(key + e, out var el))
                    st.Properties[key + e] = new PropertyInfo(el.Index, name, el.MappingType, el.ArraySize);
            named++; tokens.Add(token);
            log.Add($"export name {sn}[{key}] {token} -> {name}");
        }
        log.Add($"export names: {named} properties ({tokens.Count} tokens) named; rejected: length {lengthRejects}, readable in this build {liveRejects}, given to another token {ownerRejects}, already in the struct {dupRejects}, not one-to-one {inconsistent}");
    }
}

static class UsmapStats
{
    public static (int hashedProps, int unknown, int hashedEnumValues) Count(TypeMappings m)
    {
        int h = 0, u = 0, e = 0;
        bool Unk(PropertyType t) => t != null && (t.Type == "Unknown" || Unk(t.InnerType) || Unk(t.ValueType));
        foreach (var s in m.Types.Values)
            foreach (var p in s.Properties.Values.Where(p => p.Index == 0))
            {
                if (NameDonor.Hashed(p.Name)) h++;
                if (Unk(p.MappingType)) u++;
            }
        foreach (var v in m.Enums.Values) e += v.Values.Count(NameDonor.Hashed);
        return (h, u, e);
    }
}

// Writes a usmap that CUE4Parse's UsmapParser reads back: version ExplicitEnumValues, no package versioning,
// no compression. Mirrors UsmapParser / UsmapProperties field for field.
static class UsmapWriter
{
    public static void Write(TypeMappings m, string path)
    {
        var names = new List<string>();
        var index = new Dictionary<string, int>(StringComparer.Ordinal);
        int N(string s)
        {
            if (s == null) return -1;
            if (!index.TryGetValue(s, out var i)) { i = names.Count; names.Add(s); index[s] = i; }
            return i;
        }

        using var payload = new MemoryStream();
        using (var w = new BinaryWriter(payload, Encoding.UTF8, true))
        {
            w.Write((uint)m.Enums.Count);
            foreach (var (enumName, values) in m.Enums)
            {
                w.Write(N(enumName));
                w.Write((ushort)values.Count);
                foreach (var (v, n) in values) { w.Write((ulong)v); w.Write(N(n)); }
            }
            w.Write((uint)m.Types.Count);
            foreach (var s in m.Types.Values)
            {
                w.Write(N(s.Name));
                w.Write(N(s.SuperType));
                var firsts = s.Properties.Where(kv => kv.Value.Index == 0).OrderBy(kv => kv.Key).ToList();
                w.Write((ushort)s.PropertyCount);
                w.Write((ushort)firsts.Count);
                foreach (var (key, p) in firsts)
                {
                    w.Write((ushort)key);
                    w.Write((byte)(p.ArraySize ?? 1));
                    w.Write(N(p.Name));
                    WriteType(w, p.MappingType, N);
                }
            }
        }

        using var body = new MemoryStream();
        using (var w = new BinaryWriter(body, Encoding.UTF8, true))
        {
            w.Write((uint)names.Count);
            foreach (var n in names) { var b = Encoding.UTF8.GetBytes(n); w.Write((ushort)b.Length); w.Write(b); }
            w.Write(payload.ToArray());
        }
        var data = body.ToArray();
        using var f = new BinaryWriter(File.Create(path));
        f.Write((ushort)0x30C4);
        f.Write((byte)EUsmapVersion.ExplicitEnumValues);
        f.Write(0);                        // no package versioning (UE bool: 4 bytes)
        f.Write((byte)EUsmapCompressionMethod.None);
        f.Write((uint)data.Length);
        f.Write((uint)data.Length);
        f.Write(data);
    }

    static void WriteType(BinaryWriter w, PropertyType t, Func<string, int> N)
    {
        var e = Enum.TryParse<EPropertyType>(t?.Type, out var parsed) ? parsed : EPropertyType.Unknown;
        w.Write((byte)e);
        switch (e)
        {
            case EPropertyType.EnumProperty:
                WriteType(w, t.InnerType ?? new PropertyType("ByteProperty"), N);
                w.Write(N(t.EnumName));
                break;
            case EPropertyType.StructProperty:
                w.Write(N(t.StructType));
                break;
            case EPropertyType.SetProperty:
            case EPropertyType.ArrayProperty:
            case EPropertyType.OptionalProperty:
                WriteType(w, t.InnerType ?? new PropertyType("Unknown"), N);
                break;
            case EPropertyType.MapProperty:
                WriteType(w, t.InnerType ?? new PropertyType("Unknown"), N);
                WriteType(w, t.ValueType ?? new PropertyType("Unknown"), N);
                break;
        }
    }
}
