// CueDump: writes data/ — one .json per package that has a DataTable, DataAsset or Curve export, holding every
// export of that package as "--- export: <class> / <name> ---" followed by Newtonsoft's indented JSON.
// Usage: CueDump <paksDir> <aesKeyFile> <usmap> <outDir> [pathFilter]
// The key is read from <aesKeyFile> (hex, one line) and never printed. Offline: the game is not run and nothing
// is downloaded. Progress, errors and CUE4Parse warnings go to <outDir>_progress.log next to <outDir>.
// The export logic is the original CueDump's, unchanged; only the inputs became arguments.
using CUE4Parse.FileProvider;
using CUE4Parse.UE4.Versions;
using CUE4Parse.Encryption.Aes;
using CUE4Parse.UE4.Objects.Core.Misc;
using Newtonsoft.Json;
using Serilog;
using Serilog.Core;
using Serilog.Events;

if (args.Length < 4) { Console.WriteLine("usage: CueDump <paksDir> <aesKeyFile> <usmap> <outDir> [pathFilter]"); return 1; }
string paksDir = args[0];
string aesKeyHex = File.ReadAllText(args[1]).Trim();
string usmapPath = args[2];
string outDir = args[3];
string? pathFilter = args.Length > 4 ? args[4] : null;   // only packages whose path contains this
string logPath = Path.Combine(Path.GetDirectoryName(outDir.TrimEnd((char)92, '/'))!, Path.GetFileName(outDir.TrimEnd((char)92, '/')) + "_progress.log");

var versions = new VersionContainer(EGame.GAME_UE5_7);
var provider = new DefaultFileProvider(paksDir, SearchOption.TopDirectoryOnly, versions);
provider.Initialize();
provider.MappingsContainer = new CUE4Parse.MappingsProvider.Usmap.FileUsmapTypeMappingsProvider(usmapPath);
var aesKey = new FAesKey(aesKeyHex);
provider.SubmitKey(new FGuid(), aesKey);
if (provider.MountedVfs.Count < 10) { Console.WriteLine($"Only {provider.MountedVfs.Count} containers mounted - wrong key or unsupported format. Aborting."); return 1; }

Directory.CreateDirectory(outDir);
using var log = new StreamWriter(logPath, append: false) { AutoFlush = true };
// CUE4Parse reports exports it didn't consume exactly ("Did not read X correctly") through Serilog. A wrong usmap
// does not always trigger it, so diff known assets as well.
string currentFile = "";
int warnings = 0;
Serilog.Log.Logger = new LoggerConfiguration().MinimumLevel.Warning()
    .WriteTo.Sink(new ActionSink(e => { warnings++; log.WriteLine($"WARN [{currentFile}]: {e.RenderMessage()}"); }))
    .CreateLogger();

void Log(string s)
{
    Console.WriteLine(s);
    log.WriteLine(s);
}

Log($"Mounted {provider.MountedVfs.Count} vfs, {provider.Files.Count} files");

var uassetFiles = provider.Files.Values
    .Where(f => f.Path.EndsWith(".uasset", StringComparison.OrdinalIgnoreCase))
    .Where(f => pathFilter == null || f.Path.Contains(pathFilter, StringComparison.OrdinalIgnoreCase))
    .ToList();

Log($"Total .uasset candidates: {uassetFiles.Count}");

int ok = 0, skipped = 0, errored = 0, processed = 0;
var interestingTypes = new HashSet<string> { "DataTable", "DataAsset", "CurveTable", "CurveFloat", "CurveVector", "CurveLinearColor" };

foreach (var file in uassetFiles)
{
    processed++;
    currentFile = file.Path;
    if (processed % 2000 == 0)
        Log($"...progress {processed}/{uassetFiles.Count} (ok={ok} skipped={skipped} errored={errored})");

    try
    {
        var pkg = provider.LoadPackage(file.Path);
        var exports = pkg.GetExports().ToList();

        bool anyInteresting = exports.Any(e => interestingTypes.Contains(e.ExportType)
            || e.GetType().Name.Contains("DataTable")
            || e.GetType().Name.Contains("DataAsset")
            || e.GetType().Name.Contains("Curve"));

        if (!anyInteresting)
        {
            skipped++;
            continue;
        }

        var relPath = file.Path.Replace("\\", "/");
        var outPath = Path.Combine(outDir, relPath.Replace(".uasset", ".json"));
        Directory.CreateDirectory(Path.GetDirectoryName(outPath)!);

        using var writer = new StreamWriter(outPath);
        foreach (var export in exports)
        {
            writer.WriteLine($"--- export: {export.GetType().Name} / {export.Name} ---");
            var json = JsonConvert.SerializeObject(export, Formatting.Indented);
            writer.WriteLine(json);
        }
        ok++;
    }
    catch (Exception e)
    {
        errored++;
        log.WriteLine($"ERROR [{file.Path}]: {e.GetType().Name}: {e.Message}");
    }
}

Log($"DONE. processed={processed} ok={ok} skipped={skipped} errored={errored} warnings={warnings}");
return 0;

class ActionSink(Action<LogEvent> emit) : ILogEventSink
{
    public void Emit(LogEvent e) => emit(e);
}
