// collision mode: preserve BodySetup properties and cooked collision payloads for offline inspection.
// No render geometry is exported. Existing metadata and payload files are never overwritten.
using System.Security.Cryptography;
using System.Text;
using CUE4Parse.FileProvider;
using CUE4Parse.UE4.Assets.Exports.StaticMesh;
using CUE4Parse.UE4.Objects.PhysicsEngine;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

static class CollisionMode
{
    public static int Run(AbstractFileProvider provider, string[] assets, string outDir)
    {
        var metadataPath = Path.Combine(outDir, "collision.json");
        FileStream metadata;
        try { metadata = new FileStream(metadataPath, FileMode.CreateNew, FileAccess.Write, FileShare.None); }
        catch (Exception error)
        {
            Console.WriteLine($"FAIL collision output: {error.GetType().Name}: {error.Message}");
            return 2;
        }

        using (metadata)
        {
            var bodies = new Dictionary<string, JObject>(StringComparer.OrdinalIgnoreCase);
            var staticMeshMetadata = new JArray();
            var skipped = new JArray();
            var failures = new JArray();
            var payloadCount = 0;

            void Failure(string asset, string bodyPath, string format, Exception error)
            {
                failures.Add(new JObject {
                    ["asset"] = asset, ["bodySetupPath"] = bodyPath, ["format"] = format,
                    ["error"] = $"{error.GetType().Name}: {error.Message}"
                });
                Console.WriteLine($"FAIL {asset} {bodyPath} {format}: {error.GetType().Name}: {error.Message}");
            }

            void ExportBody(UBodySetup body, string asset)
            {
                var objectPath = body.GetPathName();
                if (bodies.TryGetValue(objectPath, out var previous))
                {
                    var sources = (JArray) previous["sourceAssets"];
                    if (!sources.Values<string>().Contains(asset, StringComparer.OrdinalIgnoreCase)) sources.Add(asset);
                    return;
                }

                var formats = new JArray();
                var entry = new JObject {
                    ["package"] = body.Owner?.Name,
                    ["bodySetup"] = body.Name,
                    ["objectPath"] = objectPath,
                    ["bodySetupGuid"] = body.BodySetupGuid.ToString(),
                    ["sourceAssets"] = new JArray(asset),
                    ["formats"] = formats
                };
                bodies.Add(objectPath, entry);
                try
                {
                    var serialized = JObject.FromObject(body);
                    var properties = serialized["Properties"] as JObject ?? new JObject();
                    entry["exportType"] = serialized["Type"];
                    entry["properties"] = properties;
                    entry["aggGeom"] = properties["AggGeom"]?.DeepClone();
                    entry["shapeCoordinates"] = "Unreal asset-local centimetres, as cooked; no component or bone placement applied";
                    if (body.CookedFormatData == null || body.CookedFormatData.Formats.Count == 0)
                    {
                        entry["status"] = "noCookedFormats";
                        return;
                    }
                    entry["status"] = "exported";
                    foreach (var (formatName, bulk) in body.CookedFormatData.Formats)
                    {
                        var format = formatName.Text;
                        var payload = new JObject { ["format"] = format };
                        formats.Add(payload);
                        try
                        {
                            payload["header"] = JObject.FromObject(bulk.Header);
                            var bytes = bulk.Data ?? throw new InvalidDataException("Cooked bulk payload could not be read");
                            if (bytes.Length != bulk.Header.ElementCount)
                                throw new InvalidDataException($"Bulk payload length {bytes.Length} differs from header ElementCount {bulk.Header.ElementCount}");
                            var filename = Hash(Encoding.UTF8.GetBytes(objectPath + "\n" + format)) + ".bin";
                            payload["byteCount"] = bytes.Length;
                            payload["sha256"] = Hash(bytes);
                            payload["file"] = filename;
                            using (var output = new FileStream(Path.Combine(outDir, filename), FileMode.CreateNew, FileAccess.Write, FileShare.None))
                                output.Write(bytes);
                            payload["status"] = "exported";
                            payloadCount++;
                        }
                        catch (Exception error)
                        {
                            entry["status"] = "failed";
                            payload["status"] = "failed";
                            payload["error"] = $"{error.GetType().Name}: {error.Message}";
                            Failure(asset, objectPath, format, error);
                        }
                    }
                }
                catch (Exception error)
                {
                    entry["status"] = "failed";
                    entry["error"] = $"{error.GetType().Name}: {error.Message}";
                    Failure(asset, objectPath, null, error);
                }
            }

            foreach (var asset in assets.Distinct(StringComparer.OrdinalIgnoreCase))
            {
                try
                {
                    var exports = provider.LoadPackage(asset).GetExports().ToList();
                    var packageBodies = exports.OfType<UBodySetup>().ToList();
                    var staticMeshes = exports.OfType<UStaticMesh>().ToList();
                    foreach (var body in packageBodies) ExportBody(body, asset);
                    foreach (var mesh in staticMeshes)
                    {
                        try
                        {
                            if (mesh.BodySetup == null || mesh.BodySetup.IsNull)
                                throw new InvalidDataException($"{mesh.Name}: BodySetup reference is absent");
                            var body = mesh.BodySetup.Load<UBodySetup>()
                                ?? throw new InvalidDataException($"{mesh.Name}: BodySetup reference could not be loaded");
                            var meshEntry = new JObject {
                                ["assetPath"] = asset,
                                ["objectPath"] = mesh.GetPathName(),
                                ["bodySetupPath"] = body.GetPathName(),
                                ["bounds"] = mesh.RenderData?.Bounds == null ? null : JObject.FromObject(mesh.RenderData.Bounds),
                                ["boundsCoordinates"] = "FStaticMeshRenderData.Bounds, Unreal asset-local centimetres; no component placement applied"
                            };
                            foreach (var property in mesh.Properties.Where(property =>
                                property.Name.Text is "ExtendedBounds" or "PositiveBoundsExtension" or "NegativeBoundsExtension"))
                                meshEntry[property.Name.Text] = property.Tag == null ? null : JToken.FromObject(property.Tag);
                            staticMeshMetadata.Add(meshEntry);
                            ExportBody(body, asset);
                        }
                        catch (Exception error) { Failure(asset, mesh.GetPathName(), null, error); }
                    }
                    if (packageBodies.Count == 0 && staticMeshes.Count == 0)
                        skipped.Add(new JObject { ["asset"] = asset, ["reason"] = "No StaticMesh or BodySetup exports" });
                }
                catch (Exception error) { Failure(asset, null, null, error); }
            }

            var manifest = new JObject {
                ["scope"] = "Cooked BodySetup properties and collision bulk payloads; no render geometry",
                ["payloadEncoding"] = "FByteBulkData.Data bytes after any bulk-level decompression; collision format is not decoded",
                ["bodies"] = new JArray(bodies.Values.OrderBy(body => (string) body["objectPath"], StringComparer.Ordinal)),
                ["staticMeshes"] = staticMeshMetadata,
                ["payloadCount"] = payloadCount,
                ["skipped"] = skipped,
                ["failures"] = failures
            };
            using var writer = new StreamWriter(metadata, new UTF8Encoding(false), 1024, leaveOpen: true);
            using var jsonWriter = new JsonTextWriter(writer) { Formatting = Formatting.Indented };
            manifest.WriteTo(jsonWriter);
            jsonWriter.Flush();
            Console.WriteLine($"collision: bodies={bodies.Count} payloads={payloadCount} skipped={skipped.Count} fail={failures.Count}");
            return failures.Count > 0 ? 2 : 0;
        }
    }

    static string Hash(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
}
