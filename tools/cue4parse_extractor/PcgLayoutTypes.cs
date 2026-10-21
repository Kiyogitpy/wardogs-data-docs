using CUE4Parse.MappingsProvider;
using CUE4Parse.MappingsProvider.Usmap;

// Map-only pass: fills unknown array element types of generated PropertyBag_* owners from the
// native PCGSettings descendant whose own+inherited field layout they reproduce. It reads no packages.
// A bag owner is accepted only when (1) the ordered property names and static-array sizes equal a
// class's fields (derived class first, then each super class, stopping before PCGSettings; a class
// MapProperty may be dropped, as the native bag generator drops unsupported value types), (2) every
// already-typed bag slot agrees with that class (same kind, struct, enum name, element types), and
// (3) every class that matches this way gives the same complete element type for the slot.
// This is layout evidence, not a descriptor-hash proof; the audit log lists every candidate class.
static class PcgLayoutTypes
{
    public static int Apply(TypeMappings m, List<string> log)
    {
        var classes = new Dictionary<string, List<PropertyInfo>>();
        foreach (var name in m.Types.Keys)
        {
            var chain = new List<string>();
            var cur = name; bool pcg = false;
            while (cur != null && m.Types.TryGetValue(cur, out var s) && chain.Count < 32)
            {
                if (cur == "PCGSettings") { pcg = true; break; }
                chain.Add(cur); cur = s.SuperType;
            }
            if (!pcg || chain.Count == 0) continue;
            classes[name] = chain.SelectMany(c => m.Types[c].Properties.Values.Where(p => p.Index == 0)
                ).ToList();
        }
        int filled = 0, owners = 0;
        foreach (var bag in m.Types.Keys.Where(k => k.StartsWith("PropertyBag_")).OrderBy(k => k, StringComparer.Ordinal).ToList())
        {
            var slots = m.Types[bag].Properties.OrderBy(p => p.Key).Where(p => p.Value.Index == 0).ToList();
            var unknown = slots.Where(p => IsUnknownArray(p.Value.MappingType)).ToList();
            if (unknown.Count == 0) continue;
            var matches = Match(classes, slots.Select(p => p.Value).ToList(), dropMaps: false);
            if (matches.Count == 0) matches = Match(classes, slots.Select(p => p.Value).ToList(), dropMaps: true);
            if (matches.Count == 0) { log.Add($"pcg-layout skip {bag}: no class layout match"); continue; }
            bool any = false;
            foreach (var (key, info) in unknown)
            {
                var types = matches.Select(c => FieldAt(classes[c.cls], c.dropMaps, info.Name)).ToList();
                var shapes = types.Select(t => t != null && t.Type == "ArrayProperty" && TypeRecovery.Complete(t.InnerType, m) ? TypeRecovery.Describe(t) : null).Distinct().ToList();
                if (shapes.Count != 1 || shapes[0] == null) { log.Add($"pcg-layout skip {bag}.{info.Name}: candidates disagree or incomplete ({string.Join(" | ", shapes.Select(s => s ?? "null"))}) from {string.Join(",", matches.Select(c => c.cls))}"); continue; }
                m.Types[bag].Properties[key] = new PropertyInfo(info.Index, info.Name, types[0], info.ArraySize);
                log.Add($"pcg-layout fill {bag}[{key}].{info.Name} -> {shapes[0]} from {string.Join(",", matches.Select(c => c.cls))}");
                filled++; any = true;
            }
            if (any) owners++;
        }
        log.Add($"pcg-layout: {filled} fills across {owners} owners");
        return filled;
    }

    static List<(string cls, bool dropMaps)> Match(Dictionary<string, List<PropertyInfo>> classes, List<PropertyInfo> bag, bool dropMaps)
    {
        var res = new List<(string, bool)>();
        foreach (var (cls, fields0) in classes)
        {
            var fields = dropMaps ? fields0.Where(f => f.MappingType?.Type != "MapProperty").ToList() : fields0;
            if (fields.Count != bag.Count) continue;
            bool ok = true;
            for (int i = 0; i < bag.Count && ok; i++)
                ok = fields[i].Name == bag[i].Name && fields[i].ArraySize == bag[i].ArraySize && Agrees(bag[i].MappingType, fields[i].MappingType);
            if (ok) res.Add((cls, dropMaps));
        }
        return res.OrderBy(r => r.Item1, StringComparer.Ordinal).ToList();
    }

    static PropertyType FieldAt(List<PropertyInfo> fields, bool dropMaps, string name) =>
        (dropMaps ? fields.Where(f => f.MappingType?.Type != "MapProperty") : fields).First(f => f.Name == name).MappingType;

    static bool IsUnknownArray(PropertyType t) => t != null && t.Type == "ArrayProperty" && t.InnerType != null && t.InnerType.Type == "Unknown";

    // Already-typed bag slot vs class field. Unknown on the bag side agrees; an enum's stored underlying
    // width is ignored (the bag always uses a byte), its enum name must match.
    static bool Agrees(PropertyType bag, PropertyType cls)
    {
        if (bag == null || cls == null) return bag == null && cls == null;
        if (bag.Type == "Unknown") return true;
        if (bag.Type != cls.Type || bag.StructType != cls.StructType || bag.EnumName != cls.EnumName) return false;
        if (bag.Type == "EnumProperty") return true;
        return Agrees(bag.InnerType, cls.InnerType) && Agrees(bag.ValueType, cls.ValueType);
    }
}
