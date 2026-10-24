// Round 36 probe (not part of WdExtract): writes the raw bytes of a package from the paks for byte-level inspection.
// Build: a console project (net10.0) referencing CUE4Parse.dll, Oodle.NET.dll, GenericReader.dll and Newtonsoft.Json.dll from the WdExtract bin folder,
// with the rest of that folder copied next to the output. Run: pb <package path> <outfile> [<package path> <outfile> ...]
// Why: CUE4Parse reads a StateTree/Challenge "Parameters" property bag as descriptors + SerialSize and skips the value bytes.
using System.Text;
using CUE4Parse.Compression;
using CUE4Parse.Encryption.Aes;
using CUE4Parse.FileProvider;
using CUE4Parse.MappingsProvider;
using CUE4Parse.MappingsProvider.Usmap;
using CUE4Parse.UE4.Objects.Core.Misc;
using CUE4Parse.UE4.Versions;
// pb <package path> <outfile> : write the raw bytes of the package (IoStore chunk) for byte-level inspection
var paks=@"E:/Steam/steamapps/common/Wardogs/Wardogs/Content/Paks";
OodleHelper.Initialize(new OodleDotNet.Oodle(paks+@"\oo2core_9_win64.dll"));
var provider = new DefaultFileProvider(paks, SearchOption.TopDirectoryOnly, new VersionContainer(EGame.GAME_UE5_7));
provider.Initialize();
provider.MappingsContainer = new FileUsmapTypeMappingsProvider(@"E:/Reverse_Engineer/wardogs_analysis/round8_propertybags_20261019/wardogs.recovered.usmap");
provider.SubmitKey(new FGuid(), new FAesKey(File.ReadAllText(@"E:/WardogsConversion/CueDump/aes.txt").Trim()));
for (int i=0;i<args.Length;i+=2){
  var p=args[i];
  var ok=provider.TryGetGameFile(p.EndsWith(".uasset")?p:p+".uasset", out var gf);
  Console.WriteLine(p+" "+ok);
  if(!ok) continue;
  var b=gf.Read();
  File.WriteAllBytes(args[i+1], b);
  Console.WriteLine(b.Length);
  // also uexp
  Console.WriteLine(string.Join(",", provider.Files.Keys.Where(k=>k.Contains("DT_WagerChallenges")))); if(provider.TryGetGameFile(p.Replace(".uasset","")+".uexp", out var g2)) {var b2=g2.Read(); File.WriteAllBytes(args[i+1]+".uexp", b2); Console.WriteLine("uexp "+b2.Length);}
}
