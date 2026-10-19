using CUE4Parse.FileProvider;
using CUE4Parse.MappingsProvider;
using CUE4Parse.UE4.Objects.UObject;

static class BlueprintTypes
{
    public static int Apply(DefaultFileProvider provider, TypeMappings mappings, List<string> log)
    {
        var files = provider.Files.Values
            .Where(f => f.Extension.Equals("uasset", StringComparison.OrdinalIgnoreCase))
            .GroupBy(f => Path.GetFileNameWithoutExtension(f.Path), StringComparer.Ordinal)
            .ToDictionary(g => g.Key, g => g.ToArray(), StringComparer.Ordinal);
        int filled = 0;
        foreach (var (owner, schema) in mappings.Types)
        {
            var slots = schema.Properties.Where(p => p.Value.Index == 0
                && p.Value.MappingType.Type == "ArrayProperty"
                && p.Value.MappingType.InnerType?.Type == "Unknown").ToArray();
            if (slots.Length == 0 || !owner.EndsWith("_C", StringComparison.Ordinal)) continue;
            if (!files.TryGetValue(owner[..^2], out var packages) || packages.Length != 1)
            {
                log.Add($"skip {owner}: no unique matching package");
                continue;
            }
            var path = packages[0].PathWithoutExtension;
            UClass type;
            try
            {
                var package = provider.LoadPackage(path);
                var index = package.GetExportIndex(owner);
                type = index < 0 ? null : package.ExportsLazy[index].Value as UClass;
                if (type == null) { log.Add($"skip {owner}: matching class export absent"); continue; }
            }
            catch (Exception e)
            {
                log.Add($"skip {owner}: {e.GetType().Name} loading {path}");
                continue;
            }
            var childFields = (type.ChildProperties ?? []).OfType<FProperty>().ToArray();
            foreach (var (slot, property) in slots)
            {
                // ChildProperties are serialized FFields, not inferred from the input usmap.
                var fields = childFields
                    .Where(p => p.Name.Text == property.Name).ToArray();

                FProperty field;
                if (fields.Length == 1)
                {
                    field = fields[0];
                }
                else if (fields.Length == 0)
                {
                    var caseMatches = childFields.Select((candidate, position) => (candidate, position))
                        .Where(x => AsciiCaseEqual(x.candidate.Name.Text, property.Name)).ToArray();
                    if (caseMatches.Length != 1 || childFields.Length != (type.ChildProperties?.Length ?? 0)
                        || !OwnerLayoutMatches(childFields, schema))
                    {
                        log.Add($"skip {owner}[{slot}] {property.Name}: field name/owner layout is not an exact or unique ASCII-case match");
                        continue;
                    }

                    var candidate = caseMatches[0];
                    if (!TryOwnerPosition(childFields, slot, out var expectedPosition)
                        || expectedPosition != candidate.position)
                    {
                        log.Add($"skip {owner}[{slot}] {property.Name}: ASCII-case field does not occupy the schema owner position");
                        continue;
                    }
                    field = candidate.candidate;
                    log.Add($"case identity {owner}[{slot}] {property.Name} == cooked {field.Name.Text} at child {candidate.position}, owner slot {slot}");
                }
                else
                {
                    log.Add($"skip {owner}[{slot}] {property.Name}: field name/shape is not an exact match");
                    continue;
                }

                if (field is not FArrayProperty array
                    || array.ArrayDim < 1 || array.ArrayDim != (property.ArraySize ?? 1))
                {
                    log.Add($"skip {owner}[{slot}] {property.Name}: field name/shape is not an exact match");
                    continue;
                }
                if (!Enumerable.Range(0, array.ArrayDim).All(element =>
                    schema.Properties.TryGetValue(slot + element, out var expanded)
                    && expanded.Index == element && expanded.Name == property.Name
                    && expanded.ArraySize == property.ArraySize
                    && expanded.MappingType.Type == "ArrayProperty"
                    && expanded.MappingType.InnerType?.Type == "Unknown"))
                {
                    log.Add($"skip {owner}[{slot}] {property.Name}: inconsistent expanded static-array slots");
                    continue;
                }
                PropertyType inner;
                try { inner = array.Inner == null ? null : new PropertyType(array.Inner); }
                catch (Exception e)
                {
                    log.Add($"skip {owner}[{slot}] {property.Name}: {e.GetType().Name} resolving inner field");
                    continue;
                }
                if (!TypeRecovery.Complete(inner, mappings))
                {
                    log.Add($"skip {owner}[{slot}] {property.Name}: incomplete inner type");
                    continue;
                }
                for (int element = 0; element < (property.ArraySize ?? 1); element++)
                {
                    var existing = schema.Properties[slot + element];
                    var replacement = new PropertyType("ArrayProperty", innerType: inner);
                    schema.Properties[slot + element] = new PropertyInfo(existing.Index, existing.Name, replacement, existing.ArraySize);
                }
                filled++;
                log.Add($"type {owner}[{slot}] {property.Name}: Array<Unknown> -> Array<{TypeRecovery.Describe(inner)}> from {path}");
            }
        }
        return filled;
    }

    static bool OwnerLayoutMatches(FProperty[] fields, Struct schema)
    {
        int total = fields.Sum(field => field.ArrayDim);
        if (fields.Any(field => field.ArrayDim < 1)
            || schema.PropertyCount != total || schema.Properties.Count != total) return false;

        int slot = 0;
        foreach (var field in fields)
        {
            if (!IsAscii(field.Name.Text)
                || !schema.Properties.TryGetValue(slot, out var primary)
                || primary.Index != 0
                || (primary.ArraySize ?? 1) != field.ArrayDim
                || !AsciiCaseEqual(primary.Name, field.Name.Text)) return false;

            for (int element = 0; element < field.ArrayDim; element++)
            {
                if (!schema.Properties.TryGetValue(slot + element, out var expanded)
                    || expanded.Index != element
                    || (expanded.ArraySize ?? 1) != (primary.ArraySize ?? 1)
                    || !AsciiCaseEqual(expanded.Name, field.Name.Text)) return false;
            }
            slot += field.ArrayDim;
        }
        return slot == total;
    }

    static bool TryOwnerPosition(FProperty[] fields, int targetSlot, out int position)
    {
        int slot = 0;
        for (int i = 0; i < fields.Length; i++)
        {
            if (slot == targetSlot)
            {
                position = i;
                return true;
            }
            slot += fields[i].ArrayDim;
        }
        position = -1;
        return false;
    }

    static bool IsAscii(string value) => value != null && value.All(c => c <= 0x7F);

    static bool AsciiCaseEqual(string left, string right) =>
        IsAscii(left) && IsAscii(right) && StringComparer.OrdinalIgnoreCase.Equals(left, right);
}
