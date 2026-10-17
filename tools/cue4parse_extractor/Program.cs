// WdExtract: offline static export of cooked Wardogs assets via CUE4Parse.
// Usage: WdExtract <paksDir> <aesKeyFile> <usmap> <outDir> <oodleDll> <mode> [args...] [--names <donor.usmap>]
//   list <prefix>                  -> <outDir>/files.txt: every .uasset whose name starts with <prefix> (e.g. GE_)
//   schema <substr...>             -> <outDir>/usmap_schema.json: usmap struct/enum layouts whose name contains a substring
//   findname <pathPrefix> <text>   -> <outDir>/findname.txt: packages under the prefix whose name map contains the text
//   dump <listFile | asset...>     -> <outDir>/<name>.json per package (all exports, Blueprint bytecode included)
//   mesh <listFile | asset...>     -> <outDir>/<collision mesh>.glb + manifest.json: collision meshes only (MeshMode.cs)
//   deobfuscate <out.usmap>        -> writes a deobfuscated copy of <usmap> (needs --names); no paks are read
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
Log.Logger = new LoggerConfiguration().MinimumLevel.Warning().WriteTo.Console().CreateLogger();
Directory.CreateDirectory(outDir);

if (mode == "deobfuscate")
{
    if (namesUsmap == null || rest.Count < 1) { Console.WriteLine("usage: ... deobfuscate <out.usmap> --names <donor.usmap>"); return 1; }
    var live = new UsmapParser(usmap).Mappings;
    var donor = new UsmapParser(namesUsmap).Mappings;
    var before = UsmapStats.Count(live);
    var log = new List<string>();
    NameDonor.Apply(live, donor, log);
    KnownPatches.Apply(live.Types, log);
    UsmapWriter.Write(live, rest[0]);
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

    static bool LengthOk(string hashed, string real)
    {
        var len = TokenLength(hashed);
        if (len == null) return true;  // not a plain token (e.g. Blueprint names with GUID suffixes): no check possible
        var m = Token.Match(hashed);
        var realBase = m.Groups[2].Success && real.EndsWith(m.Groups[2].Value) ? real[..^m.Groups[2].Value.Length] : real;
        return realBase.Length == len;
    }

    static bool HasUnknown(PropertyType t) => t != null && (t.Type == "Unknown" || HasUnknown(t.InnerType) || HasUnknown(t.ValueType));

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
