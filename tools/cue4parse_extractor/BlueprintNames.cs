using CUE4Parse.FileProvider;
using CUE4Parse.MappingsProvider;
using CUE4Parse.MappingsProvider.Usmap;
using CUE4Parse.UE4.Objects.UObject;

// Names hashed property tokens from cooked Blueprint class exports. A cooked UBlueprintGeneratedClass keeps its
// serialized ChildProperties with real FNames, so a hashed usmap slot of a "_C" owner can be read directly. A slot is
// accepted only when the cooked field count equals the owner's property count, every non-hashed property has the same
// name (ASCII case-insensitive) at the same ordinal, the hashed ordinal's field kind equals the usmap kind, and the
// real name has the length the token encodes. A token that would get two names, or a name claimed by two tokens, is
// dropped. Accepted tokens (one token is one name everywhere) then rename every other property carrying that token,
// unless the struct already has a property with that name. Types are never changed.
static class BlueprintNames
{
    public static int Apply(DefaultFileProvider provider, TypeMappings mappings, List<string> log)
    {
        var files = provider.Files.Values
            .Where(f => f.Extension.Equals("uasset", StringComparison.OrdinalIgnoreCase))
            .GroupBy(f => Path.GetFileNameWithoutExtension(f.Path), StringComparer.Ordinal)
            .ToDictionary(g => g.Key, g => g.ToArray(), StringComparer.Ordinal);
        var found = new Dictionary<string, HashSet<string>>(StringComparer.Ordinal);
        foreach (var (owner, schema) in mappings.Types.OrderBy(x => x.Key, StringComparer.Ordinal))
        {
            if (!owner.EndsWith("_C", StringComparison.Ordinal)) continue;
            var own = schema.Properties.Where(p => p.Value.Index == 0).OrderBy(p => p.Key).Select(p => p.Value).ToArray();
            if (!own.Any(p => NameDonor.Hashed(p.Name))) continue;
            if (!files.TryGetValue(owner[..^2], out var packages) || packages.Length != 1) { log.Add($"bp-names skip {owner}: no unique matching package"); continue; }
            FProperty[] fields;
            try
            {
                var package = provider.LoadPackage(packages[0].PathWithoutExtension);
                var index = package.GetExportIndex(owner);
                if (index < 0 || package.ExportsLazy[index].Value is not UStruct type) { log.Add($"bp-names skip {owner}: class export absent"); continue; }
                fields = (type.ChildProperties ?? []).OfType<FProperty>().ToArray();
                if (fields.Length != (type.ChildProperties?.Length ?? 0)) { log.Add($"bp-names skip {owner}: non-property child field"); continue; }
            }
            catch (Exception e) { log.Add($"bp-names skip {owner}: {e.GetType().Name}"); continue; }
            if (fields.Length != own.Length) { log.Add($"bp-names skip {owner}: {fields.Length} cooked fields vs {own.Length} map properties"); continue; }
            bool layout = true;
            for (int i = 0; i < own.Length && layout; i++)
                if (!NameDonor.Hashed(own[i].Name) && !string.Equals(own[i].Name, fields[i].Name.Text, StringComparison.OrdinalIgnoreCase)) layout = false;
            if (!layout) { log.Add($"bp-names skip {owner}: non-hashed names differ from the cooked layout"); continue; }
            for (int i = 0; i < own.Length; i++)
            {
                if (!NameDonor.Hashed(own[i].Name)) continue;
                var real = fields[i].Name.Text;
                var kind = fields[i].GetType().Name[1..];
                if (kind != own[i].MappingType?.Type || !NameDonor.LengthOk(own[i].Name, real) || NameDonor.TokenLength(own[i].Name) == null)
                { log.Add($"bp-names reject {owner}.{own[i].Name}: cooked {real} ({kind}) fails kind or token length"); continue; }
                if (!found.TryGetValue(own[i].Name, out var set)) found[own[i].Name] = set = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
                set.Add(real);
                log.Add($"bp-names source {owner}.{own[i].Name} = {real}");
            }
        }
        var tokens = found.Where(kv => kv.Value.Count == 1).ToDictionary(kv => kv.Key, kv => kv.Value.First(), StringComparer.Ordinal);
        foreach (var kv in found.Where(kv => kv.Value.Count > 1)) log.Add($"bp-names drop token {kv.Key}: names {string.Join(",", kv.Value)}");
        foreach (var grp in tokens.GroupBy(kv => kv.Value, StringComparer.OrdinalIgnoreCase).Where(g => g.Count() > 1).ToList())
            foreach (var kv in grp) { tokens.Remove(kv.Key); log.Add($"bp-names drop token {kv.Key}: name {kv.Value} claimed by {grp.Count()} tokens"); }
        int renamed = 0;
        foreach (var (owner, schema) in mappings.Types.OrderBy(x => x.Key, StringComparer.Ordinal))
            foreach (var key in schema.Properties.Where(p => tokens.ContainsKey(p.Value.Name)).Select(p => p.Key).ToList())
            {
                var p = schema.Properties[key];
                var real = tokens[p.Name];
                if (schema.Properties.Values.Any(q => !ReferenceEquals(q, p) && q.Name != p.Name && string.Equals(q.Name, real, StringComparison.OrdinalIgnoreCase)))
                { log.Add($"bp-names skip {owner}[{key}] {p.Name}: {real} already used in this struct"); continue; }
                schema.Properties[key] = new PropertyInfo(p.Index, real, p.MappingType, p.ArraySize);
                log.Add($"bp-names rename {owner}[{key}] {p.Name} -> {real}");
                renamed++;
            }
        log.Add($"bp-names: {tokens.Count} tokens, {renamed} property renames");
        return renamed;
    }
}
