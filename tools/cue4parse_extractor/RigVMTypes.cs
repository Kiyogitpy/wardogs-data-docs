using System.IO.Hashing;
using System.Text;
using CUE4Parse.FileProvider;
using CUE4Parse.MappingsProvider;
using CUE4Parse.UE4.Assets;
using CUE4Parse.UE4.Objects.RigVM;
using CUE4Parse.UE4.Objects.StructUtils;
using CUE4Parse.UE4.Versions;

static class RigVMTypes
{
    public static int Apply(DefaultFileProvider provider, TypeMappings mappings, List<string> log)
    {
        var pending = new Dictionary<(string owner, int slot), PropertyType>();
        var payloads = new Dictionary<string, byte[]>();
        var conflicts = new HashSet<string>();
        var files = provider.Files.Values.Where(f => f.Extension.Equals("uasset", StringComparison.OrdinalIgnoreCase)
            || f.Extension.Equals("umap", StringComparison.OrdinalIgnoreCase)).OrderBy(f => f.Path).ToArray();
        int loaded = 0, targets = 0, bags = 0, failures = 0;
        foreach (var file in files)
        {
            try
            {
                var package = provider.LoadPackage(file.PathWithoutExtension);
                loaded++;
                if (package is not IoPackage io) continue;
                for (int i = 0; i < io.ExportMap.Length; i++)
                {
                    var classPath = io.ResolveObjectIndex(io.ExportMap[i].ClassIndex)?.GetPathName();
                    if (classPath is not ("/Script/RigVM.RigVM" or "/Script/RigVM.RigVMBlueprintGeneratedClass"
                        or "/Script/ControlRig.ControlRigBlueprintGeneratedClass")) continue;
                    try
                    {
                        targets++;
                        var export = package.ExportsLazy[i].Value;
                        var vm = export as URigVM ?? (export as URigVMBlueprintGeneratedClass)?.VM;
                        if (vm == null) continue;
                        var version = package.Summary.CustomVersionContainer?.GetVersion(FPropertyBagCustomVersion.GUID) ?? -1;
                        // This extractor uses GAME_UE5_7; its missing-version fallback is MetaClass (3).
                        if (version < 0) version = (int)FPropertyBagCustomVersion.Type.MetaClass;
                        if (version > (int)FPropertyBagCustomVersion.Type.MetaClass)
                        {
                            log.Add($"skip {file.PathWithoutExtension}: unsupported PropertyBag custom version {version}");
                            continue;
                        }
                        Visit(vm.LiteralMemoryStorage, "LiteralMemoryStorage");
                        Visit(vm.DefaultWorkMemoryStorage, "DefaultWorkMemoryStorage");
                        Visit(vm.DefaultDebugMemoryStorage, "DefaultDebugMemoryStorage");
                        void Visit(FRigVMMemoryStorageStruct bag, string memory)
                        {
                            if (bag == null || bag.PropertyDescs.Length == 0) return;
                            bags++;
                            var payload = HashPayload(bag.PropertyDescs, version);
                            var owner = "PropertyBag_" + XxHash3.HashToUInt64(payload).ToString("x");
                            if (!mappings.Types.TryGetValue(owner, out var schema)) return;
                            if (payloads.TryGetValue(owner, out var previous))
                            {
                                if (!previous.SequenceEqual(payload))
                                {
                                    conflicts.Add(owner);
                                    log.Add($"skip {owner}: conflicting descriptor payloads");
                                }
                                return;
                            }
                            payloads[owner] = payload;
                            var fields = bag.PropertyDescs.Select(FieldType).ToArray();
                            if (schema.PropertyCount != fields.Length || schema.Properties.Count != fields.Length
                                || Enumerable.Range(0, fields.Length).Any(slot =>
                                    !schema.Properties.TryGetValue(slot, out var property) || property.Index != 0
                                    || (property.ArraySize ?? 1) != 1 || property.Name != bag.PropertyDescs[slot].Name.Text
                                    || !TypeRecovery.Complete(fields[slot], mappings)
                                    || !TypeRecovery.CompatibleKnown(property.MappingType, fields[slot])))
                            {
                                log.Add($"skip {owner}: descriptor/schema layout or known-type mismatch");
                                return;
                            }
                            for (int slot = 0; slot < fields.Length; slot++)
                            {
                                var property = schema.Properties[slot];
                                if (property.MappingType.Type != "ArrayProperty" || property.MappingType.InnerType?.Type != "Unknown") continue;
                                pending[(owner, slot)] = fields[slot];
                                log.Add($"type {owner}[{slot}] {property.Name}: Array<Unknown> -> {TypeRecovery.Describe(fields[slot])} from {file.PathWithoutExtension}:{export.Name}/{memory}");
                            }
                        }
                    }
                    catch (Exception e)
                    {
                        failures++;
                        log.Add($"failure {file.PathWithoutExtension} export {i}: {e.GetType().Name}");
                    }
                }
            }
            catch (Exception e)
            {
                failures++;
                log.Add($"failure {file.PathWithoutExtension}: {e.GetType().Name}");
            }
            if (loaded % 10000 == 0) Console.WriteLine($"RigVM scan: {loaded}/{files.Length}, {bags} bags, {failures} failures");
        }
        int filled = 0;
        foreach (var ((owner, slot), type) in pending)
        {
            if (conflicts.Contains(owner)) continue;
            var property = mappings.Types[owner].Properties[slot];
            mappings.Types[owner].Properties[slot] = new PropertyInfo(property.Index, property.Name, type, property.ArraySize);
            filled++;
        }
        log.Add($"scan: {loaded}/{files.Length} packages, {targets} exports, {bags} bags, {payloads.Count} matching hashes, {failures} failures; {filled} fills");
        return filled;
    }

    static byte[] HashPayload(FPropertyBagPropertyDesc[] descriptors, int version)
    {
        using var bytes = new MemoryStream();
        using var writer = new BinaryWriter(bytes, Encoding.Unicode, true);
        foreach (var desc in descriptors)
        {
            writer.Write(desc.ID.A); writer.Write(desc.ID.B); writer.Write(desc.ID.C); writer.Write(desc.ID.D);
            writer.Write((byte)desc.ValueType);
            var containers = desc.ContainerTypes.Types ?? [];
            if (containers.Length > 2) throw new InvalidDataException("unsupported container depth");
            writer.Write(containers.Length > 0 ? (byte)containers[0] : (byte)0);
            writer.Write(containers.Length > 1 ? (byte)containers[1] : (byte)0);
            writer.Write((byte)containers.Length);
            // Target CL516586 registers version 3; native descriptor flags default to CPF_Edit (1).
            writer.Write(version < (int)FPropertyBagCustomVersion.Type.PropertyFlags ? 1UL : (ulong)desc.PropertyFlags);
            string path = "";
            if (!desc.ValueTypeObject.IsNull)
                path = desc.ValueTypeObject.ResolvedObject?.GetPathName() ?? throw new InvalidDataException("unresolved value type object");
            writer.Write(Encoding.Unicode.GetBytes(desc.Name.Text + path));
        }
        return bytes.ToArray();
    }

    static PropertyType FieldType(FPropertyBagPropertyDesc desc)
    {
        var name = desc.ValueTypeObject.ResolvedObject?.Name.Text;
        string primitive = desc.ValueType switch
        {
            EPropertyBagPropertyType.Bool => "BoolProperty", EPropertyBagPropertyType.Byte => "ByteProperty",
            EPropertyBagPropertyType.Int32 => "IntProperty", EPropertyBagPropertyType.Int64 => "Int64Property",
            EPropertyBagPropertyType.UInt32 => "UInt32Property", EPropertyBagPropertyType.UInt64 => "UInt64Property",
            EPropertyBagPropertyType.Float => "FloatProperty", EPropertyBagPropertyType.Double => "DoubleProperty",
            EPropertyBagPropertyType.Name => "NameProperty", EPropertyBagPropertyType.String => "StrProperty",
            EPropertyBagPropertyType.Text => "TextProperty", EPropertyBagPropertyType.Object => "ObjectProperty",
            EPropertyBagPropertyType.SoftObject => "SoftObjectProperty", EPropertyBagPropertyType.Class => "ClassProperty",
            EPropertyBagPropertyType.SoftClass => "SoftClassProperty", _ => null
        };
        var type = desc.ValueType switch
        {
            EPropertyBagPropertyType.Struct => new PropertyType("StructProperty", structType: name),
            EPropertyBagPropertyType.Enum => new PropertyType("EnumProperty", innerType: new PropertyType("ByteProperty"), enumName: name),
            _ => new PropertyType(primitive ?? "Unknown")
        };
        foreach (var container in (desc.ContainerTypes.Types ?? []).Reverse())
        {
            if (container != EPropertyBagContainerType.Array) return new PropertyType("Unknown");
            type = new PropertyType("ArrayProperty", innerType: type);
        }
        return type;
    }
}
