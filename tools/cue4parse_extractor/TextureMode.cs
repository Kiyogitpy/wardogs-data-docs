// textures mode: decode UTexture2D packages to PNG (highest mip). Usage: WdExtract ... textures <listFile | package...>
// BC7 icons need Detex.dll next to the exe (see below). Output: <outDir>/<package path without leading slash>.png plus _textures_log.txt (ok/fail per package).
using CUE4Parse.FileProvider;
using CUE4Parse.UE4.Assets.Exports.Texture;
using CUE4Parse_Conversion.Textures;
using CUE4Parse_Conversion.Textures.BC;
using SkiaSharp;

static class TextureMode
{
    public static int Run(AbstractFileProvider provider, string[] assets, string outDir)
    {
        // BC6/BC7 (and ETC) go through the native Detex library; it ships with CUE4Parse-Conversion/Resources/Detex.dll.
        // Copy it next to WdExtract.exe (or point WDEXTRACT_DETEX at it).
        DetexHelper.Initialize(Environment.GetEnvironmentVariable("WDEXTRACT_DETEX") ?? Path.Combine(AppContext.BaseDirectory, "Detex.dll"));
        int ok = 0, fail = 0;
        var log = new List<string>();
        foreach (var a in assets.Distinct(StringComparer.OrdinalIgnoreCase))
        {
            try
            {
                var exports = provider.LoadPackage(a).GetExports().ToList();
                var tex = exports.OfType<UTexture2D>().FirstOrDefault() ?? throw new Exception("no UTexture2D export");
                var bmp = tex.Decode() ?? throw new Exception("decode returned null");
                using var sk = bmp.ToSkBitmap();
                using var img = SKImage.FromBitmap(sk);
                using var data = img.Encode(SKEncodedImageFormat.Png, 100) ?? throw new Exception("encode returned null");
                var rel = a.TrimStart('/');
                var path = Path.Combine(outDir, rel + ".png");
                Directory.CreateDirectory(Path.GetDirectoryName(path));
                File.WriteAllBytes(path, data.ToArray());
                log.Add($"OK\t{a}\t{bmp.Width}x{bmp.Height}");
                ok++;
            }
            catch (Exception e) { log.Add($"FAIL\t{a}\t{e.Message}"); fail++; }
        }
        File.WriteAllLines(Path.Combine(outDir, "_textures_log.txt"), log);
        Console.WriteLine($"textures: {ok} ok, {fail} failed");
        return fail == 0 ? 0 : 2;
    }
}
