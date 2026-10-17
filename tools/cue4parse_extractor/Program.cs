// WdExtract: offline static export of cooked Wardogs assets via CUE4Parse.
// Usage: WdExtract <paksDir> <aesKeyFile> <usmap> <outDir> <oodleDll> <mode> [args...]
//   list <prefix>                  -> <outDir>/files.txt: every .uasset whose name starts with <prefix> (e.g. GE_)
//   schema <substr...>             -> <outDir>/usmap_schema.json: usmap struct/enum layouts whose name contains a substring
//   dump <listFile | asset...>     -> <outDir>/<name>.json per package (all exports, Blueprint bytecode included)
// The AES key is read from <aesKeyFile> (hex, one line) and never printed. Oodle is loaded from <oodleDll>;
// nothing is downloaded. The game is not run.
using CUE4Parse.Compression;
using CUE4Parse.Encryption.Aes;
using CUE4Parse.FileProvider;
using CUE4Parse.UE4.Objects.Core.Misc;
using CUE4Parse.UE4.Versions;
using Newtonsoft.Json;
using Serilog;

if (args.Length < 6)
{
    Console.WriteLine("usage: WdExtract <paksDir> <aesKeyFile> <usmap> <outDir> <oodleDll> <list|schema|dump> [args...]");
    return 1;
}
string paksDir = args[0], keyFile = args[1], usmap = args[2], outDir = args[3], oodle = args[4], mode = args[5];
var rest = args.Skip(6).ToArray();
Log.Logger = new LoggerConfiguration().MinimumLevel.Warning().WriteTo.Console().CreateLogger();
if (!File.Exists(oodle)) { Console.WriteLine("oodle dll missing"); return 1; }
OodleHelper.Initialize(new OodleDotNet.Oodle(oodle));

var provider = new DefaultFileProvider(paksDir, SearchOption.TopDirectoryOnly, new VersionContainer(EGame.GAME_UE5_7));
provider.ReadScriptData = true;  // keep Blueprint ScriptBytecode in the dumps
provider.Initialize();
provider.MappingsContainer = new CUE4Parse.MappingsProvider.Usmap.FileUsmapTypeMappingsProvider(usmap);
provider.SubmitKey(new FGuid(), new FAesKey(File.ReadAllText(keyFile).Trim()));
Console.WriteLine($"Mounted {provider.MountedVfs.Count} vfs, {provider.Files.Count} files");
Directory.CreateDirectory(outDir);

if (mode == "list")
{
    var prefix = rest.Length > 0 ? rest[0] : "";
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
if (mode != "dump") { Console.WriteLine($"unknown mode {mode}"); return 1; }

// The 5.7.4 usmap hashes some property names and leaves some array inner types as Unknown. Restore them by
// property index, which follows the SDK declaration order (sdk/raw/BHGameplayEffects_*.hpp,
// BHGameplayTag_structs.hpp, BHFramework_structs.hpp). Without this, GE modifiers and tag queries do not decode.
{
    var types = provider.MappingsForGame.Types;
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
    var log = new List<string>();
    foreach (var (t, names) in renames)
    {
        if (!types.TryGetValue(t, out var s)) { log.Add($"{t}: not in usmap, skipped"); continue; }
        if (s.Properties.Count != names.Length) throw new Exception($"{t}: usmap has {s.Properties.Count} props, expected {names.Length}");
        for (int i = 0; i < names.Length; i++)
            if (s.Properties[i].Name != names[i]) { log.Add($"{t}[{i}] {s.Properties[i].Name} -> {names[i]} ({s.Properties[i].MappingType.Type})"); s.Properties[i].Name = names[i]; }
    }
    void PatchArray(string t, int idx, string innerType, string innerStruct)
    {
        var p = types[t].Properties[idx];
        var inner = new CUE4Parse.MappingsProvider.PropertyType(innerType, innerStruct, null, null, null, null, null);
        log.Add($"{t}[{idx}] {p.Name} array inner {p.MappingType.InnerType?.Type} -> {innerType} {innerStruct}");
        types[t].Properties[idx] = new CUE4Parse.MappingsProvider.PropertyInfo(p.Index, p.Name,
            new CUE4Parse.MappingsProvider.PropertyType("ArrayProperty", null, inner, null, null, null, null), p.ArraySize);
    }
    PatchArray("BHGameplayEffect", 4, "StructProperty", "BHAttributeModifier");   // TArray<FBHAttributeModifier> Modifiers
    PatchArray("GameplayTagQuery", 1, "StructProperty", "GameplayTag");           // TArray<FGameplayTag> TagDictionary
    PatchArray("GameplayTagQuery", 2, "ByteProperty", null);                      // TArray<uint8> QueryTokenStream
    File.WriteAllLines(Path.Combine(outDir, "_usmap_patches.txt"), log);
}

var assets = rest.Length == 1 && File.Exists(rest[0]) ? File.ReadAllLines(rest[0]).Where(l => l.Trim().Length > 0).ToArray() : rest;
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
